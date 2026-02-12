# Quickstart: RAG Data Retrieval Testing

## Overview
This guide provides instructions for setting up and using the RAG data retrieval testing functionality. The `retrieve.py` module allows AI engineers to validate that the RAG ingestion and retrieval pipeline works correctly by connecting to Qdrant and testing data storage and retrieval.

## Prerequisites
- Python 3.11+
- Qdrant vector database instance (local or cloud)
- Access to backend configuration files
- Required Python packages (see requirements.txt)

## Setup

### 1. Environment Configuration
```bash
# Set up environment variables for Qdrant connection
export QDRANT_HOST=your-qdrant-host
export QDRANT_PORT=6333
export QDRANT_API_KEY=your-api-key  # if using cloud
```

### 2. Install Dependencies
```bash
pip install qdrant-client python-dotenv pydantic
```

### 3. Verify Backend Configuration
Ensure your backend configuration includes Qdrant connection settings in `config.py` or environment variables.

## Basic Usage

### 1. Import and Initialize
```python
from backend.retrieve import QdrantRetriever

# Initialize the retriever with configuration
retriever = QdrantRetriever()
```

### 2. Perform Similarity Search
```python
# Search for documents similar to a query
query = "What are vector embeddings?"
results = retriever.search(query, top_k=5)

for result in results:
    print(f"Content: {result.content}")
    print(f"Score: {result.score}")
    print(f"Metadata: {result.metadata}")
```

### 3. Validate Storage
```python
# Validate that documents are properly stored
validation_result = retriever.validate_storage()
print(f"Storage validation: {validation_result.is_valid}")
print(f"Message: {validation_result.message}")
```

### 4. List Available Collections
```python
collections = retriever.list_collections()
print(f"Available collections: {collections}")
```

## Testing Workflow

### 1. Verify Ingestion
```python
# Check if documents were properly ingested
collections = retriever.list_collections()
if collections:
    print("✓ Collections exist - ingestion appears successful")
else:
    print("✗ No collections found - ingestion may have failed")
```

### 2. Test Retrieval Accuracy
```python
# Test with known queries against stored content
test_query = "specific content from ingested documents"
results = retriever.search(test_query, top_k=3)

# Validate that relevant results are returned
for result in results:
    if result.score > 0.7:  # High confidence threshold
        print(f"✓ High-relevance result found: {result.score}")
    else:
        print(f"⚠ Low-relevance result: {result.score}")
```

### 3. Performance Testing
```python
import time

# Measure retrieval performance
start_time = time.time()
results = retriever.search("test query", top_k=5)
end_time = time.time()

execution_time = end_time - start_time
print(f"Retrieval time: {execution_time:.2f} seconds")

# Validate against performance requirements
if execution_time < 3.0:  # Requirement: sub-3 seconds
    print("✓ Performance requirement met")
else:
    print("⚠ Performance requirement not met")
```

## Debugging Tools

### 1. View Collection Statistics
```python
stats = retriever.get_collection_stats("documents")
print(f"Total documents: {stats['total_points']}")
print(f"Vector dimensions: {stats['vector_dim']}")
```

### 2. Inspect Individual Points
```python
# Retrieve specific document by ID
doc = retriever.get_document_by_id("specific-id", "documents")
print(f"Document content: {doc.content}")
print(f"Metadata: {doc.metadata}")
```

## Common Issues and Solutions

### Issue: Connection to Qdrant Fails
**Solution**: Verify QDRANT_HOST, QDRANT_PORT, and QDRANT_API_KEY environment variables

### Issue: No Results Returned
**Solution**: Check that documents were properly ingested and collections exist

### Issue: Low Relevance Scores
**Solution**: Verify embedding quality and consider adjusting similarity thresholds

## Next Steps
1. Integrate retrieval testing into your CI/CD pipeline
2. Create automated tests for regular validation
3. Monitor retrieval performance over time
4. Document any specific validation procedures for your use case