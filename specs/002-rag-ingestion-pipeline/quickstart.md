# Quickstart: RAG Ingestion Pipeline

## Prerequisites

- Python 3.11 or higher
- UV package manager
- Cohere API key
- Qdrant Cloud account (or local instance)

## Setup

1. **Create backend directory and initialize project:**
```bash
mkdir backend
cd backend
uv init
```

2. **Install dependencies:**
```bash
uv add requests beautifulsoup4 cohere qdrant-client python-dotenv tiktoken
```

3. **Set up environment variables:**
Create a `.env` file with:
```
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
```

## Running the Pipeline

1. **Execute the main pipeline:**
```bash
python main.py
```

2. **The pipeline will:**
   - Crawl the deployed Docusaurus site at https://physical-ai-humanoid-robotics-eight-snowy.vercel.app/
   - Extract clean text from all accessible pages
   - Chunk content with token-aware processing and overlap
   - Generate embeddings using Cohere
   - Store vectors with metadata in Qdrant
   - Validate via similarity search

## Configuration

The main.py file contains configurable parameters:
- `CHUNK_SIZE`: Size of text chunks (default: 512 tokens)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 50 tokens)
- `COHERE_MODEL`: Embedding model to use (default: embed-english-v3.0)
- `COLLECTION_NAME`: Qdrant collection name (default: rag_embedding)

## Verification

After running, verify the pipeline worked by:
1. Checking Qdrant dashboard for the "rag_embedding" collection
2. Confirming document chunks were stored with metadata
3. Running a test similarity search to validate embeddings