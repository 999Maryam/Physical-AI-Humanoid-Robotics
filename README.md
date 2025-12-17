# RAG Backend-Frontend Integration

This project integrates a RAG (Retrieval-Augmented Generation) backend with a simple frontend interface, allowing users to query a knowledge base and receive grounded responses.

## Architecture

- **Backend**: FastAPI server running on `http://localhost:8000`
- **Frontend**: Static HTML interface in `frontend/index.html`
- **RAG System**: Reuses existing `create_rag_response()` function from `agent.py`

## Setup

1. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. Set up environment variables in a `.env` file:
   ```
   COHERE_API_KEY=your_cohere_api_key
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key
   GEMINI_API_KEY=your_gemini_api_key
   COLLECTION_NAME=your_collection_name
   ```

3. Run the backend server:
   ```bash
   cd backend
   uvicorn api:app --reload --port=8000
   ```

4. Open `frontend/index.html` in your web browser

## Usage

1. Enter your question in the text area
2. Click "Ask" to submit the query
3. View the response from the RAG system
4. (Optional) Use "Advanced Parameters" to customize response length, search depth, and result format

## Features

- **Core Query Functionality**: Submit questions and receive grounded responses
- **Error Handling**: Proper error messages for various failure scenarios
- **Parameter Configuration**: Adjust response length, search depth, and result format
- **Loading States**: Visual feedback during query processing
- **Input Validation**: Prevents overly long queries
- **Timeout Handling**: Handles long-running queries gracefully

## Endpoints

- `GET /` - Health check
- `POST /ask` - Submit a query to the RAG system

Request format:
```json
{
  "query": "your question here",
  "response_length": 500,
  "search_depth": 5,
  "result_format": "text"
}
```

Response format:
```json
{
  "response": "the RAG-generated answer",
  "status": "success",
  "error_message": null
}
```