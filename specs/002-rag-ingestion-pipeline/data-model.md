# Data Model: RAG Ingestion Pipeline

## Entities

### Document Chunk
**Description**: Represents a segment of extracted content with associated metadata
**Fields**:
- `id` (string): Unique identifier for the chunk (auto-generated)
- `content` (string): The text content of the chunk
- `source_url` (string): URL of the original document where this chunk came from
- `chunk_index` (integer): Position of this chunk within the original document
- `document_title` (string): Title of the source document
- `created_at` (datetime): Timestamp when the chunk was created
- `token_count` (integer): Number of tokens in the chunk

### Embedding Vector
**Description**: High-dimensional numerical representation of document chunk semantics
**Fields**:
- `vector_id` (string): Unique identifier matching the document chunk ID
- `embedding` (array of floats): The actual embedding vector values
- `document_chunk_id` (string): Reference to the associated document chunk
- `model_version` (string): Version of the embedding model used

### Content Collection
**Description**: Organized group of documents from a specific Docusaurus website
**Fields**:
- `collection_name` (string): Name of the collection (e.g., "rag_embedding")
- `source_website` (string): Base URL of the source website
- `document_count` (integer): Number of documents in the collection
- `chunk_count` (integer): Total number of chunks in the collection
- `created_at` (datetime): Timestamp when the collection was created
- `updated_at` (datetime): Timestamp when the collection was last updated

## Relationships
- One Content Collection contains many Document Chunks
- One Document Chunk has one Embedding Vector
- Many Embedding Vectors belong to one Content Collection through Document Chunks

## Validation Rules
1. Document Chunk content must be non-empty and less than 10,000 characters
2. Source URL must be a valid URL format
3. Token count must be positive
4. Embedding vector must have consistent dimensions based on the model used
5. Document chunk ID and vector ID must match for proper association

## State Transitions
- Document Chunk: PENDING → PROCESSED → EMBEDDED → STORED
- Content Collection: CREATING → BUILDING → READY → UPDATING