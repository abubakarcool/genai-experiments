import os
import time
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def quick_search(query, year=2025, month=3):
    start_time = time.time()
    
    print(f"Quick search for: '{query}'")
    print("Loading embeddings...")
    
    # Initialize embeddings
    embeddings = OpenAIEmbeddings()
    
    # Path to embeddings
    embeddings_dir = "embeddings"
    embeddings_path = os.path.join(embeddings_dir, f"embeddings_{year}_{month:02d}")
    
    if not os.path.exists(embeddings_path):
        print(f"No embeddings found at {embeddings_path}")
        return
    
    # Load the vectorstore
    load_start = time.time()
    vectorstore = FAISS.load_local(
        embeddings_path, 
        embeddings,
        allow_dangerous_deserialization=True  # Allow deserialization of the pickle file
    )
    load_time = time.time() - load_start
    print(f"Embeddings loaded in {load_time:.2f} seconds")
    
    # Perform search
    print("Searching...")
    search_start = time.time()
    results = vectorstore.similarity_search_with_score(query, k=5)
    search_time = time.time() - search_start
    print(f"Search completed in {search_time:.2f} seconds")
    
    # Display results
    if results:
        print(f"\nFound {len(results)} relevant results:")
        for i, (doc, score) in enumerate(results, 1):
            print(f"\n--- Result {i} (Relevance: {score:.4f}) ---")
            print(f"Content: {doc.page_content[:300]}...")
    else:
        print("No results found.")
    
    total_time = time.time() - start_time
    print(f"\nTotal execution time: {total_time:.2f} seconds")

if __name__ == "__main__":
    # Ask for search query
    query = input("Enter your search query: ")
    quick_search(query) 