# RAG Data Retrieval Testing Guide

This guide provides instructions for using the RAG data retrieval testing functionality to validate that the RAG ingestion and retrieval pipeline works correctly.

## Overview

The RAG testing module allows AI engineers to validate that:

1. Documents are properly ingested and stored in Qdrant with embeddings
2. Vector storage works correctly and similarity search returns relevant results
3. The complete RAG pipeline functions end-to-end

## API Endpoints

### List Collections
```
GET /api/list-collections
```
Returns a list of all available Qdrant collections.

### Validate Storage
```
GET /api/validate-storage
```
Validates that documents are properly stored in Qdrant with embeddings.

### Retrieve Documents
```
POST /api/retrieve
```
Performs similarity search in Qdrant to retrieve relevant documents.

Request body:
```json
{
  "query_text": "Your search query",
  "top_k": 5,
  "collection_name": "documents",
  "min_score": 0.5
}
```

## Command Line Interface

The module includes a command-line interface for testing:

### List Collections
```bash
python -m backend.retrieve list-collections
```

### Validate Storage
```bash
python -m backend.retrieve validate-storage
```

### Search
```bash
python -m backend.retrieve search --query "Your query" --top-k 5
```

### Get Document by ID
```bash
python -m backend.retrieve get-document --id "document-id"
```

### Debug Content Inspection
```bash
python -m backend.retrieve debug-inspect --collection "documents"
```

### Performance Testing
```bash
python -m backend.retrieve perf-test --queries "query1" "query2"
```

## Configuration

The module uses the following environment variables from `backend/config.py`:

- `QDRANT_URL`: URL for Qdrant instance
- `QDRANT_API_KEY`: API key for Qdrant (if required)
- `QDRANT_HOST`: Qdrant host (default: localhost)
- `QDRANT_PORT`: Qdrant port (default: 6333)
- `DEFAULT_RETRIEVAL_TOP_K`: Default number of results to return (default: 5)
- `DEFAULT_MIN_SCORE`: Default minimum relevance score (default: 0.0)

## Testing

Run the tests with pytest:

```bash
pytest backend/tests/test_retrieve.py
```

## Troubleshooting

### Connection Issues
- Verify Qdrant is running and accessible
- Check that environment variables are properly set
- Ensure network connectivity to Qdrant instance

### No Results Returned
- Verify documents were properly ingested
- Check that collections exist in Qdrant
- Validate embedding generation was successful