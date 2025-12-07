# Data Model: AI-native Textbook with RAG Chatbot

## Entities

### Chapter
- **Description**: Represents a distinct section of the textbook.
- **Attributes**:
    - `id`: Unique identifier for the chapter.
    - `title`: Title of the chapter.
    - `content`: The main textual and multimedia content of the chapter.
    - `order`: Numeric value to define the sequential order of the chapter within the book.
    - `related_topics`: List of keywords or links to related topics for RAG context.

### UserQuery
- **Description**: Represents a question or prompt submitted by a user to the RAG chatbot.
- **Attributes**:
    - `id`: Unique identifier for the query.
    - `text`: The actual text of the user's question.
    - `timestamp`: Time when the query was made.
    - `user_id` (Optional): Identifier for the user making the query (if authenticated/personalized).
    - `context` (Optional): Current chapter or section the user is viewing when the query is made.

### ChatbotResponse
- **Description**: Represents the AI-generated answer provided by the RAG chatbot.
- **Attributes**:
    - `id`: Unique identifier for the response.
    - `query_id`: Reference to the `UserQuery` this response is answering.
    - `text`: The AI-generated answer.
    - `source_references`: List of specific sections/paragraphs in the textbook that support the answer.
    - `timestamp`: Time when the response was generated.
    - `relevance_score` (Optional): An internal score indicating how relevant the response is to the query.

### UserProfile (Conditional - if personalization is enabled)
- **Description**: Stores user-specific data used to adapt chapter content for personalization.
- **Attributes**:
    - `user_id`: Unique identifier for the user.
    - `learning_style`: User's preferred learning style (e.g., visual, auditory, kinesthetic).
    - `reading_history`: Log of chapters/sections read, time spent, and completion status.
    - `quiz_performance`: Records of quiz scores, strengths, and weaknesses.
    - `preferences`: Other user-defined preferences that might influence content delivery.

## Relationships

- `UserQuery` has a one-to-one relationship with `ChatbotResponse` (a response answers a specific query).
- `ChatbotResponse` references `Chapter` content through `source_references` (many-to-many implicit relationship based on content).
- `UserProfile` (if enabled) influences how `Chapter` content is presented to a specific `user_id`.
