# API Contract: OpenAI Agents RAG

## Agent Query Endpoint

### POST /api/v1/agent/query

#### Description
Submit a query to the OpenAI RAG agent for processing. The agent will retrieve relevant information from Qdrant vector database and generate a grounded response.

#### Request

**Headers**
- `Content-Type: application/json`
- `Authorization: Bearer {api_key}` (optional, depending on auth requirements)

**Body**
```json
{
  "query": {
    "type": "string",
    "description": "The natural language question from the user",
    "example": "What are the key principles of humanoid robotics?",
    "minLength": 1,
    "maxLength": 1000
  },
  "session_id": {
    "type": "string",
    "description": "Optional session identifier for maintaining conversation context",
    "example": "session-12345",
    "pattern": "^[a-zA-Z0-9-_]+$",
    "maxLength": 64,
    "required": false
  }
}
```

#### Response

**Success Response (200 OK)**
```json
{
  "response": {
    "type": "string",
    "description": "The agent's answer based on retrieved information",
    "example": "Humanoid robotics is a field that focuses on creating robots with human-like characteristics..."
  },
  "sources": {
    "type": "array",
    "description": "List of source documents used in the response",
    "items": {
      "type": "object",
      "properties": {
        "source_url": {
          "type": "string",
          "description": "URL or identifier of the source document",
          "example": "book://chapter-2/section-1"
        },
        "content": {
          "type": "string",
          "description": "The actual content that was retrieved",
          "example": "Humanoid robots are designed to resemble and mimic human behavior..."
        },
        "score": {
          "type": "number",
          "description": "Relevance score from Qdrant (0.0-1.0)",
          "example": 0.87,
          "minimum": 0.0,
          "maximum": 1.0
        },
        "page_number": {
          "type": "integer",
          "description": "Page number if from a book",
          "example": 45,
          "required": false
        },
        "section_title": {
          "type": "string",
          "description": "Title of the section",
          "example": "Introduction to Humanoid Design",
          "required": false
        }
      }
    }
  },
  "confidence": {
    "type": "number",
    "description": "Confidence score for the response (0.0-1.0)",
    "example": 0.92,
    "minimum": 0.0,
    "maximum": 1.0
  },
  "timestamp": {
    "type": "string",
    "format": "date-time",
    "description": "When the response was generated",
    "example": "2025-12-17T10:30:00Z"
  }
}
```

**Error Response (400 Bad Request)**
```json
{
  "error": {
    "type": "string",
    "description": "Error message describing the issue",
    "example": "Query must not be empty"
  },
  "code": {
    "type": "string",
    "description": "Error code",
    "example": "INVALID_QUERY"
  }
}
```

**Error Response (500 Internal Server Error)**
```json
{
  "error": {
    "type": "string",
    "description": "Error message describing the issue",
    "example": "Failed to process query due to internal error"
  },
  "code": {
    "type": "string",
    "description": "Error code",
    "example": "INTERNAL_ERROR"
  }
}
```

#### Example Request
```bash
curl -X POST http://localhost:8000/api/v1/agent/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the main concept of humanoid robotics?",
    "session_id": "session-12345"
  }'
```

#### Example Response
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

## Session Management

### GET /api/v1/agent/session/{session_id}

#### Description
Retrieve information about a specific agent session.

#### Response
```json
{
  "session_id": "string",
  "created_at": "string",
  "last_accessed": "string",
  "conversation_history": [
    {
      "user_query": "string",
      "agent_response": "string",
      "timestamp": "string",
      "sources_used": "array"
    }
  ]
}
```

### DELETE /api/v1/agent/session/{session_id}

#### Description
Delete a specific agent session and its conversation history.