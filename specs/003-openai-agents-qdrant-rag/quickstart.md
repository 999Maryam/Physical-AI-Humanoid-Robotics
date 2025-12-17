# Quickstart: OpenAI Agents SDK with Qdrant Integration

## Prerequisites

- Python 3.11+
- Qdrant vector database instance (local or cloud)
- OpenAI API key
- Cohere API key (for embeddings)
- Poetry for dependency management

## Setup

### 1. Environment Configuration

```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Install dependencies
poetry install

# Set up environment variables
cp .env.example .env
# Edit .env with your OpenAI and Cohere API keys and Qdrant configuration
```

### 2. Environment Variables

Create/update `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION_NAME=book_embeddings
```

### 3. Run the Service

```bash
# Activate virtual environment
poetry shell

# Start the backend service
cd backend
poetry run uvicorn main:app --reload --port 8000
```

## Usage

### Query the RAG Agent

```bash
# Send a query to the agent
curl -X POST http://localhost:8000/api/v1/agent/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the main concept of humanoid robotics?",
    "session_id": "optional-session-id"
  }'
```

### Example Response

```json
{
  "response": "Humanoid robotics is a field that focuses on creating robots with human-like characteristics...",
  "sources": [
    {
      "source_url": "book://chapter-2/section-1",
      "content": "Humanoid robots are designed to resemble and mimic human behavior...",
      "score": 0.87
    }
  ],
  "confidence": 0.92,
  "timestamp": "2025-12-17T10:30:00Z"
}
```

## Development

### Running Tests

```bash
# Run unit tests
poetry run pytest tests/unit/

# Run integration tests
poetry run pytest tests/integration/

# Run all tests
poetry run pytest
```

### Adding New Features

1. Create new endpoints in `backend/src/api/v1/router.py`
2. Implement services in `backend/src/services/`
3. Add models in `backend/src/models/`
4. Write tests in the appropriate test directories

## Architecture

The RAG agent follows a service-oriented architecture:

```
API Layer (FastAPI)
  ↓
Service Layer (OpenAI Agent Service)
  ↓
Tool Layer (Qdrant Retrieval Tool)
  ↓
Data Layer (Qdrant Vector Database)
```

The agent uses OpenAI's language model capabilities combined with custom tools that retrieve information from Qdrant vector database to provide grounded responses based on book content. Cohere is used specifically for generating document embeddings.