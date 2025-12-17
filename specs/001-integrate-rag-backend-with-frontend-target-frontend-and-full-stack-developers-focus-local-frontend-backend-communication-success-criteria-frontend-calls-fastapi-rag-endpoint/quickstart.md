# Quickstart Guide: RAG Backend-Frontend Integration

## Overview
This guide explains how to set up and run the RAG backend with a simple frontend interface for local development and testing.

## Prerequisites
- Python 3.11+
- pip package manager
- Access to API keys:
  - Cohere API key for embeddings
  - Qdrant credentials (URL and API key) for vector storage
  - Google Gemini API key for response generation

## Setup Instructions

### 1. Environment Configuration
Create a `.env` file in the backend directory with the following variables:
```bash
COHERE_API_KEY=your_cohere_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
GEMINI_API_KEY=your_gemini_api_key
COLLECTION_NAME=your_collection_name
```

### 2. Backend Setup
1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install fastapi uvicorn python-dotenv cohere qdrant-client openai
```

3. Run the API server:
```bash
uvicorn api:app --reload --port=8000
```

### 3. Frontend Setup
The frontend is a simple static HTML file that can be opened directly in a browser:
1. Open `frontend/index.html` in your web browser
2. Ensure the backend server is running on `http://localhost:8000`

## API Endpoints

### Health Check
- **GET** `/`
- Returns: `{"message": "RAG API is running"}`

### Query Endpoint
- **POST** `/ask`
- Request body: `{"query": "your question here"}`
- Response: `{"response": "grounded answer", "status": "success"}`

## Usage Example
1. Start the backend server: `uvicorn api:app --reload --port=8000`
2. Open `frontend/index.html` in a browser
3. Enter a question in the text area
4. Click "Ask" to get a response from the RAG system

## Troubleshooting
- If you get CORS errors, ensure the backend server is running
- If API keys are missing, ensure your `.env` file is properly configured
- If Qdrant connection fails, verify your Qdrant credentials and collection exists
- If responses are "I don't know", verify that relevant documents exist in your Qdrant collection

## Development Notes
- The backend reuses the `create_rag_response()` function from `agent.py` to ensure consistency
- Responses are grounded in retrieved documents with "I don't know" fallback when no relevant documents are found
- The frontend includes loading states and error handling for better user experience