# Research: RAG Ingestion Pipeline

## Decision: Use Cohere for Embeddings
**Rationale**: User specifically requested to use Cohere for embedding generation, which aligns with the constitution's requirement for Cohere API adaptability (Principle V).
**Alternatives considered**: OpenAI embeddings, Hugging Face sentence transformers, Google embeddings - all rejected as Cohere was explicitly specified.

## Decision: Use Qdrant as Vector Database
**Rationale**: User specifically requested to use Qdrant for storing vectors, which aligns with the constitution's requirement for free-tier services (Qdrant Cloud Free Tier).
**Alternatives considered**: Pinecone, Weaviate, ChromaDB, PostgreSQL with pgvector - all rejected as Qdrant was explicitly specified.

## Decision: Single main.py File Structure
**Rationale**: User specifically requested a single file implementation with named functions (get_all_urls, extract_text_from_url, chunk_text, embed, create_collection, save_chunk_to_qdrant).
**Alternatives considered**: Multi-file structure with separate modules for each function - rejected as single file was explicitly specified.

## Decision: Deployed Docusaurus Site Target
**Rationale**: User provided specific deployment URL: https://physical-ai-humanoid-robotics-eight-snowy.vercel.app/
**Content source**: The pipeline will crawl this specific site to extract content as specified in the user requirements.

## Technology Research Findings

### Web Crawling and Text Extraction
- **requests**: Standard Python library for HTTP requests, suitable for fetching web pages
- **beautifulsoup4**: Industry standard for parsing HTML and extracting text content
- **Approach**: Will navigate the Docusaurus site structure to extract clean text from all accessible pages

### Content Chunking Strategy
- **tiktoken**: Recommended for token-aware chunking (though sentencepiece could also work)
- **Overlap strategy**: Overlapping chunks help maintain context across boundaries
- **Size**: Will implement configurable chunk size with overlap for optimal retrieval

### Cohere Embedding Integration
- **cohere package**: Official Python client for Cohere API
- **Embed model**: Cohere's embed-english-v3.0 or similar model for text embeddings
- **Rate limits**: Will implement proper rate limiting to stay within free tier limits

### Qdrant Vector Database Integration
- **qdrant-client**: Official Python client for Qdrant
- **Collection**: Will create a collection named "rag_embedding" as specified
- **Metadata**: Will store document source URL and chunk information with each vector
- **Similarity search**: Qdrant supports multiple similarity measures (cosine, euclidean, etc.)

### Project Initialization with UV
- **UV**: Modern Python package manager that's faster than pip
- **pyproject.toml**: Will use standard project format for dependencies
- **Virtual environment**: UV handles virtual environment management efficiently