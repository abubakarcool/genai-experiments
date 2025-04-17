from whatsapp_chunker import WhatsAppChatChunker
import time

def search_for_zizu():
    start_time = time.time()
    
    # Initialize the chunker
    print("Initializing chunker...")
    chunker = WhatsAppChatChunker('chat_group.txt', user_name="Abubakar")
    
    # Load the existing embeddings for March 2025
    print("Loading embeddings (this may take a moment)...")
    load_start = time.time()
    if chunker.load_searchable_index(2025, 3):
        load_time = time.time() - load_start
        print(f"Embeddings loaded in {load_time:.2f} seconds")
        
        print("Searching for information about Zizu...")
        search_start = time.time()
        
        # Use a single, more specific query
        results = chunker.search_chunks("Who is Zizu? What is their role or position?", k=5)
        
        search_time = time.time() - search_start
        print(f"Search completed in {search_time:.2f} seconds")
        
        if results:
            print(f"\nFound {len(results)} relevant results:")
            for i, (doc, score) in enumerate(results, 1):
                print(f"\n--- Result {i} (Relevance: {score:.4f}) ---")
                print(f"Content: {doc.page_content[:300]}...")
                print(f"Analysis: {doc.metadata['analysis']}")
        else:
            print("No information found about Zizu in the March 2025 chat data.")
    else:
        print("No embeddings found for March 2025. Please run whatsapp_chunker.py first.")
    
    total_time = time.time() - start_time
    print(f"\nTotal execution time: {total_time:.2f} seconds")

if __name__ == "__main__":
    search_for_zizu() 