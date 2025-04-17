AAC (Advanced Agentic Chunking) is a smarter way to create chunks. Instead of just cutting data based on size (like every 1000 characters), it looks at the meaning and context.
Each chuck also stores extra helpful info like:
1. When it happened (start and end time)
2. Who was talking
3. What topics were discussed
4. Whether the mood was positive, negative, or neutral
5. Any important events that took place
This method lets the LLM understand and work like a human.

# AAC Example :-
## 1. Sample WhatsApp Messages
```bash
12/03/2025, 09:30 - Sarah: Let’s plan the trip to Dubai.
12/03/2025, 09:32 - Ali: I’m in! What dates?
12/03/2025, 09:35 - Abubakar: Preferably next weekend.
12/03/2025, 09:37 - Sarah: I’ll check hotel options.
```

## 2. Chunk Content, this is given to LLM :-
```bash
"Sarah: Let’s plan the trip to Dubai. Ali: I’m in! What dates? Abubakar: Preferably next weekend. Sarah: I’ll check hotel options."
```

## 3. LLM do Analysis and gives this as output :-
```bash
{
  "topics": ["Travel Planning", "Trip to Dubai"],
  "participants": ["Sarah", "Ali", "Abubakar"],
  "sentiment": "positive",
  "events": ["Trip planning discussion started", "Hotel search initiated"],
  "action_items": ["Check hotel options", "Finalize trip dates"]
}
```
## 4. Final Saved Chunk with Metadata :-
```bash
{
  "content": "Sarah: Let’s plan the trip to Dubai. Ali: I’m in! What dates? Abubakar: Preferably next weekend. Sarah: I’ll check hotel options.",
  "metadata": {
    "chunk_type": "topic",  # could also be "time"
    "start_time": "2025-03-12T09:30:00",
    "end_time": "2025-03-12T09:37:00",
    "participants": ["Sarah", "Ali", "Abubakar"],
    "message_count": 4,
    "topics": ["Travel Planning", "Trip to Dubai"],
    "sentiment": "positive",
    "events": ["Trip planning discussion started", "Hotel search initiated"],
    "action_items": ["Check hotel options", "Finalize trip dates"]
  }
}
```


---

# Pyton Files 
 - "quick_search.py" file faiss-vector-database 'embeddings_2025_03' ko load karti hai, phir yeh hamari di hui query par similarity search perform karti hai aur jawab mein k=5 mein se 4 results deti hai.
 - "whatsapp_chunker.py" Yeh WhatsApp chat ko parse karti hai, phir usay time aur topic-based chunks mein divide karti hai. Har chunk ka LLM se analysis hota hai aur FAISS index banakar searchable embeddings create ki jaati hain.
 - "search_zizu.py" Yeh script pehlay se banaye gaye embeddings load karti hai aur phir Zizu ke baare mein semantic search perform karti hai.


# WhatsApp Chat Chunker with LLM Analysis

This application provides advanced chunking and analysis capabilities for WhatsApp chat exports using Large Language Models (LLMs). It processes WhatsApp chat data, creates intelligent chunks based on time and topics, and provides semantic search capabilities.

## Features

- Parse WhatsApp chat exports
- Create time-based chunks
- Create topic-based chunks using conversation analysis
- Analyze chunks using LLM for insights
- Semantic search across chat history
- Extract key information, sentiment, and action items



The application will:
- Parse your WhatsApp chat
- Create time-based and topic-based chunks
- Analyze chunks using LLM
- Create a searchable index
- Perform an example search

## Customization

You can modify the following parameters in the code:
- `time_window` in `create_time_based_chunks()` to change the time-based chunking interval
- `min_messages` in `create_topic_based_chunks()` to adjust the minimum number of messages for a conversation
- `chunk_size` and `chunk_overlap` in the text splitter to adjust chunk sizes
- The LLM analysis prompt template to extract different types of information

