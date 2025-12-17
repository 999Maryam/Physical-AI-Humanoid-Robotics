# API Contract: RAG Ingestion Pipeline

## Endpoints

### GET /health
**Description**: Check the health status of the ingestion service
**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-15T10:00:00Z"
}
```

### POST /ingest
**Description**: Trigger the ingestion pipeline for a given website URL
**Request**:
```json
{
  "website_url": "https://physical-ai-humanoid-robotics-eight-snowy.vercel.app/",
  "collection_name": "rag_embedding",
  "chunk_size": 512,
  "chunk_overlap": 50
}
```

**Response**:
```json
{
  "job_id": "ingest_12345",
  "status": "started",
  "total_documents": 42,
  "estimated_completion": "2025-12-15T10:05:00Z"
}
```

### GET /ingest/{job_id}
**Description**: Get the status of an ingestion job
**Response**:
```json
{
  "job_id": "ingest_12345",
  "status": "completed",
  "processed_documents": 42,
  "processed_chunks": 128,
  "start_time": "2025-12-15T10:00:00Z",
  "end_time": "2025-12-15T10:03:15Z",
  "errors": []
}
```

### POST /search
**Description**: Perform similarity search against the vector database
**Request**:
```json
{
  "query": "What is humanoid robotics?",
  "collection_name": "rag_embedding",
  "top_k": 5
}
```

**Response**:
```json
{
  "query": "What is humanoid robotics?",
  "results": [
    {
      "id": "chunk_123",
      "content": "Humanoid robotics is a field of robotics focused on creating robots with human-like characteristics...",
      "source_url": "https://physical-ai-humanoid-robotics-eight-snowy.vercel.app/introduction",
      "similarity_score": 0.87
    }
  ]
}
```