# Research: RAG Backend to Frontend Integration

## Decision: FastAPI RAG Endpoint Implementation
**Rationale**: The existing codebase has two different RAG implementations:
1. `backend/agent.py` - Uses Cohere embeddings with Qdrant and Google Gemini API for RAG responses
2. `backend/main.py` - Contains a FastAPI application with retrieval endpoints but no RAG generation

The user requirement specifically asks to reuse `create_rag_response()` which exists in `backend/agent.py`. Therefore, I will create a new FastAPI endpoint that integrates the `create_rag_response()` function from `agent.py`.

## Existing Architecture Analysis

### Current RAG Components
- **Agent Module** (`backend/agent.py`): Contains the complete RAG pipeline with `create_rag_response()` function
  - Uses Cohere API for embeddings
  - Uses Qdrant for vector storage and retrieval
  - Uses Google Gemini via OpenAI-compatible endpoint for response generation
  - Implements grounded response generation with "I don't know" fallback

- **Main FastAPI App** (`backend/main.py`): Contains retrieval-only endpoints
  - Provides `/` health check endpoint
  - Provides `/api/list-collections`, `/api/validate-storage`, `/api/retrieve` endpoints
  - Uses CORS middleware allowing all origins

### Integration Approach
The plan is to create a new file `backend/api.py` that:
1. Imports the `create_rag_response()` function from `agent.py`
2. Creates a FastAPI app with CORS enabled
3. Exposes a POST `/ask` endpoint that accepts `{"query": str}` and returns the RAG response
4. Includes a GET `/` health check endpoint

## Technical Decisions

### Decision: Reuse Existing RAG Function
- **Chosen**: Import and reuse `create_rag_response()` from `agent.py`
- **Rationale**: Avoids duplicating complex RAG logic, maintains consistency with existing grounded response behavior
- **Implementation**: Use import statement to access the function directly

### Decision: New API File Structure
- **Chosen**: Create `backend/api.py` as a standalone FastAPI application
- **Rationale**: Keeps integration separate from existing ingestion and retrieval code
- **Alternatives considered**:
  - Modifying `main.py` to add the endpoint (rejected - would mix ingestion/retrieval concerns)
  - Creating as a module within existing structure (rejected - standalone approach is cleaner)

### Decision: CORS Configuration
- **Chosen**: Enable CORS for local development (similar to existing main.py)
- **Rationale**: Allows frontend to communicate with backend during local development
- **Security note**: In production, origins should be restricted

### Decision: Error Handling
- **Chosen**: Wrap the RAG call in try-catch to handle potential errors gracefully
- **Rationale**: The existing `create_rag_response()` already handles errors internally, but additional API-level error handling provides better user experience

## Dependencies and Requirements

### Required Dependencies
- FastAPI
- uvicorn (for running the server)
- python-multipart (for FastAPI)
- The existing dependencies from `agent.py` (cohere, qdrant-client, openai, python-dotenv)

### Environment Variables Needed
- `COHERE_API_KEY` - for embeddings
- `QDRANT_URL` and `QDRANT_API_KEY` - for vector database access
- `GEMINI_API_KEY` - for response generation
- `COLLECTION_NAME` - for specifying Qdrant collection

## Frontend Integration Plan

### Decision: Static HTML Frontend
- **Chosen**: Create `frontend/index.html` with basic UI
- **Components**:
  - Textarea for question input
  - Submit button
  - Div for displaying answer
  - Loading state indicator
  - Basic CSS styling

### Decision: Client-Side Technology
- **Chosen**: Use vanilla JavaScript fetch API to call backend
- **Rationale**: Simple, lightweight, no additional dependencies
- **Endpoint**: `http://localhost:8000/ask`

## Risks and Mitigations

### Risk: Environment Configuration
- **Issue**: Missing API keys could cause the RAG system to fail
- **Mitigation**: Clear error messages in the API response when environment variables are missing

### Risk: Qdrant Connection
- **Issue**: Qdrant may not be running or accessible
- **Mitigation**: Proper error handling in the API with user-friendly messages

### Risk: Cross-Origin Issues
- **Issue**: Frontend may not be able to communicate with backend
- **Mitigation**: Proper CORS configuration in FastAPI

## Alternatives Considered

### Alternative 1: Modify existing main.py
- **Pros**: Reuses existing infrastructure
- **Cons**: Mixes ingestion/retrieval concerns with RAG generation, potentially confusing architecture
- **Decision**: Rejected in favor of separation of concerns

### Alternative 2: Create as part of existing backend package
- **Pros**: Follows existing code organization
- **Cons**: May complicate existing backend functionality
- **Decision**: Rejected - standalone approach is cleaner for this specific integration task