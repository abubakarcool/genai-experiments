import re
import pandas as pd
from datetime import datetime
from typing import List, Dict, Tuple
import nltk
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
from tqdm import tqdm

# Load environment variables
load_dotenv()

class WhatsAppChatChunker:
    def __init__(self, file_path: str, user_name: str = "Abubakar", embeddings_dir: str = "embeddings"):
        self.file_path = file_path
        self.user_name = user_name
        self.messages = []
        self.chunks = []
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(temperature=0)
        self.embeddings_dir = embeddings_dir
        
        # Create embeddings directory if it doesn't exist
        if not os.path.exists(embeddings_dir):
            os.makedirs(embeddings_dir)
    
    def get_embeddings_path(self, year: int, month: int) -> str:
        """Get the path for saving/loading embeddings for a specific year and month."""
        return os.path.join(self.embeddings_dir, f"embeddings_{year}_{month:02d}")
    
    def parse_whatsapp_chat(self, year: int = 2025, month: int = 3) -> pd.DataFrame:
        """Parse WhatsApp chat file into a structured format."""
        pattern = r'(\d{2}/\d{2}/\d{4}, \d{2}:\d{2}) - ([^:]+): (.+)'
        
        with open(self.file_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = re.match(pattern, line.strip())
                if match:
                    timestamp, sender, message = match.groups()
                    # Parse the timestamp
                    parsed_timestamp = datetime.strptime(timestamp, '%d/%m/%Y, %H:%M')
                    
                    # Only include messages from the specified year and month
                    if parsed_timestamp.year == year and parsed_timestamp.month == month:
                        # Replace emoji with user name if present
                        if "😊 😴💤" in sender:
                            sender = self.user_name
                        self.messages.append({
                            'timestamp': parsed_timestamp,
                            'sender': sender.strip(),
                            'message': message.strip()
                        })
        
        df = pd.DataFrame(self.messages)
        print(f"Parsed {len(df)} messages from {month}/{year}")
        if len(df) > 0:
            print("DataFrame columns:", df.columns.tolist())
            print("First few rows:")
            print(df.head())
            print(f"Date range: from {df['timestamp'].min()} to {df['timestamp'].max()}")
        else:
            print(f"No messages found for {month}/{year}")
        return df
    
    def create_time_based_chunks(self, df: pd.DataFrame, time_window: str = '1D') -> List[Dict]:
        """Create chunks based on time windows."""
        if df.empty:
            print("Warning: DataFrame is empty!")
            return []
            
        print("DataFrame before setting index:")
        print(df.head())
        print("Columns:", df.columns.tolist())
        
        df = df.copy()  # Create a copy to avoid modifying the original
        df.set_index('timestamp', inplace=True)
        chunks = []
        
        for name, group in df.groupby(pd.Grouper(freq=time_window)):
            if not group.empty:
                chunk = {
                    'start_time': group.index[0],
                    'end_time': group.index[-1],
                    'messages': group.reset_index().to_dict('records'),
                    'participants': group['sender'].unique().tolist(),
                    'message_count': len(group)
                }
                chunks.append(chunk)
        
        print(f"Created {len(chunks)} time-based chunks")
        return chunks
    
    def create_topic_based_chunks(self, df: pd.DataFrame, min_messages: int = 5) -> List[Dict]:
        """Create chunks based on conversation topics using TF-IDF and clustering."""
        # Combine messages into conversation threads
        conversations = []
        current_conversation = []
        
        for idx, row in df.iterrows():
            if len(current_conversation) == 0:
                current_conversation.append(f"{row['sender']}: {row['message']}")
            else:
                time_diff = (row['timestamp'] - df.iloc[idx-1]['timestamp']).total_seconds()
                if time_diff > 3600:  # New conversation if gap > 1 hour
                    if len(current_conversation) >= min_messages:
                        conversations.append(' '.join(current_conversation))
                    current_conversation = [f"{row['sender']}: {row['message']}"]
                else:
                    current_conversation.append(f"{row['sender']}: {row['message']}")
        
        if len(current_conversation) >= min_messages:
            conversations.append(' '.join(current_conversation))
        
        # Create chunks using LangChain's text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        chunks = []
        for conv in conversations:
            splits = text_splitter.split_text(conv)
            chunks.extend(splits)
        
        return chunks
    
    def analyze_chunks_with_llm(self, chunks: List[str]) -> List[Dict]:
        """Analyze chunks using LLM to extract insights and categorize them."""
        analysis_prompt = PromptTemplate(
            input_variables=["text"],
            template="""Analyze the following WhatsApp chat chunk and provide:
            1. Main topics discussed
            2. Key participants
            3. Sentiment (positive/negative/neutral)
            4. Important events or decisions
            5. Action items if any

            Chat chunk:
            {text}

            Provide the analysis in a structured format."""
        )
        
        chain = LLMChain(llm=self.llm, prompt=analysis_prompt)
        
        analyzed_chunks = []
        for chunk in tqdm(chunks, desc="Analyzing chunks"):
            analysis = chain.run(chunk)
            analyzed_chunks.append({
                'content': chunk,
                'analysis': analysis
            })
        
        return analyzed_chunks
    
    def create_searchable_index(self, analyzed_chunks: List[Dict], year: int, month: int):
        """Create a searchable FAISS index from the analyzed chunks and save it to disk."""
        texts = [chunk['content'] for chunk in analyzed_chunks]
        metadatas = [{'analysis': chunk['analysis']} for chunk in analyzed_chunks]
        
        self.vectorstore = FAISS.from_texts(
            texts=texts,
            embedding=self.embeddings,
            metadatas=metadatas
        )
        
        # Save the FAISS index and metadata
        embeddings_path = self.get_embeddings_path(year, month)
        self.vectorstore.save_local(embeddings_path)
        print(f"Saved embeddings to {embeddings_path}")
    
    def load_searchable_index(self, year: int, month: int) -> bool:
        """Load the FAISS index for the specified year and month if it exists."""
        embeddings_path = self.get_embeddings_path(year, month)
        if os.path.exists(embeddings_path):
            self.vectorstore = FAISS.load_local(embeddings_path, self.embeddings)
            print(f"Loaded existing embeddings from {embeddings_path}")
            return True
        return False
    
    def search_chunks(self, query: str, k: int = 5) -> List[Dict]:
        """Search through chunks using semantic similarity."""
        if not hasattr(self, 'vectorstore'):
            raise ValueError("Please create the searchable index first using create_searchable_index()")
        
        results = self.vectorstore.similarity_search_with_score(query, k=k)
        return results

def main():
    # Initialize the chunker with your name
    chunker = WhatsAppChatChunker('chat_group.txt', user_name="Abubakar")
    
    year, month = 2025, 3  # March 2025
    
    # Try to load existing embeddings first
    if not chunker.load_searchable_index(year, month):
        # If no existing embeddings, process the chat and create new ones
        print("Parsing WhatsApp chat for March 2025...")
        df = chunker.parse_whatsapp_chat(year=year, month=month)
        
        if len(df) == 0:
            print("No messages found for the specified period. Exiting.")
            return
        
        # Create time-based chunks
        print("Creating time-based chunks...")
        time_chunks = chunker.create_time_based_chunks(df)
        
        # Create topic-based chunks
        print("Creating topic-based chunks...")
        topic_chunks = chunker.create_topic_based_chunks(df)
        
        # Analyze chunks with LLM
        print("Analyzing chunks with LLM...")
        analyzed_chunks = chunker.analyze_chunks_with_llm(topic_chunks)
        
        # Create and save searchable index
        print("Creating and saving searchable index...")
        chunker.create_searchable_index(analyzed_chunks, year, month)
    
    # Example search
    print("\nExample search results:")
    results = chunker.search_chunks("What are the main topics discussed in the group?")
    for doc, score in results:
        print(f"\nRelevance Score: {score}")
        print(f"Content: {doc.page_content[:200]}...")
        print(f"Analysis: {doc.metadata['analysis']}")

if __name__ == "__main__":
    main() 