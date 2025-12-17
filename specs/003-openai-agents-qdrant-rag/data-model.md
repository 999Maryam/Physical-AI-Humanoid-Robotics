# Data Model: OpenAI Agents SDK with Qdrant Integration

## Entities

### AgentRequest
**Purpose**: Represents a user's request to the RAG agent
- **query**: string - The natural language question from the user
- **session_id**: string (optional) - For maintaining conversation context
- **metadata**: dict (optional) - Additional context for the request

### AgentResponse
**Purpose**: Represents the agent's response to a user query
- **response**: string - The agent's answer based on retrieved information
- **sources**: list[SourceReference] - List of source documents used
- **confidence**: float - Confidence score for the response (0.0-1.0)
- **timestamp**: datetime - When the response was generated

### SourceReference
**Purpose**: Reference to a source document used in the response
- **source_url**: string - URL or identifier of the source document
- **content**: string - The actual content that was retrieved
- **score**: float - Relevance score from Qdrant (0.0-1.0)
- **page_number**: int (optional) - Page number if from a book
- **section_title**: string (optional) - Title of the section

### RetrievalResult
**Purpose**: Represents the results from Qdrant vector search
- **content**: string - The text content of the retrieved passage
- **metadata**: dict - Metadata associated with the embedded content
- **score**: float - Similarity score from vector search (0.0-1.0)
- **document_id**: string - Unique identifier for the document

### AgentSession
**Purpose**: Maintains conversation state for multi-turn interactions
- **session_id**: string - Unique identifier for the session
- **history**: list[ConversationTurn] - List of previous interactions
- **created_at**: datetime - When the session was created
- **last_accessed**: datetime - When the session was last used

### ConversationTurn
**Purpose**: Represents a single turn in a conversation
- **user_query**: string - The user's question
- **agent_response**: string - The agent's response
- **timestamp**: datetime - When the interaction occurred
- **sources_used**: list[SourceReference] - Sources referenced in this turn

## Relationships

```
AgentRequest --[1]-->[0..1] AgentSession (optional session association)
AgentRequest --[1]-->[1..*] RetrievalResult (via Qdrant search)
AgentResponse --[1]-->[0..*] SourceReference (sources used in response)
AgentSession --[1]-->[0..*] ConversationTurn (conversation history)
```

## Validation Rules

### AgentRequest Validation
- query must be between 1 and 1000 characters
- session_id must be a valid UUID if provided
- query must not be empty or contain only whitespace

### AgentResponse Validation
- response must be provided and not empty
- confidence must be between 0.0 and 1.0
- sources list must contain valid SourceReference objects

### SourceReference Validation
- source_url must be a valid URL or document identifier
- score must be between 0.0 and 1.0
- content must not be empty

## State Transitions

### AgentSession States
1. **New**: Session created, no conversation history
2. **Active**: Session has conversation history, ready for new interactions
3. **Expired**: Session has timed out due to inactivity

### Transition Rules
- New → Active: When first conversation turn is added
- Active → Active: When additional conversation turns are added
- Active → Expired: When session exceeds timeout period (e.g., 30 minutes)