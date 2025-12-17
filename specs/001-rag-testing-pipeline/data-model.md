# Data Model: RAG Data Retrieval Testing

## Core Entities

### Document
**Description**: Represents an ingested document with text content and metadata
- `id`: Unique identifier for the document (UUID/string)
- `content`: Text content of the document (string)
- `metadata`: Dictionary containing source information (dict)
  - `source`: Original document source (string)
  - `format`: Document format (PDF, DOCX, TXT) (string)
  - `ingestion_timestamp`: When document was ingested (datetime)
  - `page_number`: Page number if from multi-page document (int, optional)
- `embedding`: Vector representation of document content (list[float])
- `collection_name`: Name of Qdrant collection containing this document (string)

### QueryResult
**Description**: Contains retrieved documents with relevance scores
- `id`: Document ID from Qdrant collection (string)
- `content`: Retrieved document content (string)
- `score`: Relevance score from similarity search (float)
- `metadata`: Document metadata from original ingestion (dict)
- `position`: Position in results list (int)

### RetrievalRequest
**Description**: Input for retrieval operations
- `query_text`: Text to search for similar documents (string)
- `top_k`: Number of results to return (int, default: 5)
- `collection_name`: Qdrant collection to search in (string)
- `min_score`: Minimum relevance score threshold (float, optional)

### RetrievalResponse
**Description**: Output from retrieval operations
- `query`: Original query text (string)
- `results`: List of QueryResult objects (list[QueryResult])
- `total_count`: Total number of results found (int)
- `execution_time`: Time taken for retrieval (float, seconds)

### ValidationResult
**Description**: Result of validation operations
- `is_valid`: Whether validation passed (bool)
- `message`: Description of validation result (string)
- `details`: Additional validation details (dict, optional)
- `timestamp`: When validation was performed (datetime)

## Relationships

```
RetrievalRequest 1 -> * QueryResult
QueryResult 1 -> 1 Document
Document 1 -> 1 ValidationResult
```

## Validation Rules

### Document Validation
- Content must not be empty
- Embedding must be a valid vector (list of floats)
- Metadata must contain required fields (source, format, ingestion_timestamp)

### QueryResult Validation
- Score must be between 0 and 1
- Content must not be empty
- Position must be non-negative

### RetrievalRequest Validation
- Query text must not be empty
- Top_k must be positive integer
- Collection name must exist in Qdrant

## State Transitions

### Document States
- `INGESTED`: Successfully stored in Qdrant
- `VALIDATED`: Confirmed retrievable with correct content
- `INVALID`: Failed validation checks

### ValidationResult States
- `PENDING`: Validation requested but not completed
- `PASS`: Validation successful
- `FAIL`: Validation failed with errors