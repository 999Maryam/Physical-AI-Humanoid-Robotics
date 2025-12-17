<!-- Sync Impact Report:
Version change: 1.0.0 → 1.1.0
List of modified principles:
- Simplicity → Book Content Accuracy
- Accuracy → User-Centric Design
- Minimalism → Scalability with Free-tier Services
- Fast Builds → Security and Privacy
- Free-tier Architecture → Cohere API Adaptability
- RAG Answers ONLY from Book Text → User-Selected Text Support
Added sections: Scope and Constraints, Success Criteria
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md: ✅ updated
- .specify/templates/spec-template.md: ✅ updated
- .specify/templates/tasks-template.md: ✅ updated
- .specify/templates/commands/*.md: ✅ updated
- README.md: ✅ updated
- docs/quickstart.md: ✅ updated
Follow-up TODOs: None
-->
# Integrated RAG Chatbot Development for a Published Book — Constitution

## Core Principles

### I. Book Content Accuracy
The RAG chatbot must provide accurate retrieval and generation based solely on the published book content. All answers must be grounded in retrieved book content with proper citations to source sections, ensuring no hallucinations or fabricated information.

### II. User-Centric Design
The chatbot interface must provide seamless interaction for users, including intuitive handling of selected text queries. The user experience should be responsive and accessible, meeting user expectations for clarity and usefulness.

### III. Scalability with Free-tier Services
The architecture must utilize free-tier services to ensure accessibility and cost-efficiency. All components including Cohere API, Neon Serverless Postgres, and Qdrant Cloud Free Tier must operate within free usage limits while maintaining performance.

### IV. Security and Privacy
Data handling must prioritize security and privacy, especially with user-selected text. No API key leaks or security vulnerabilities should occur. All sensitive information must be properly protected and transmitted securely.

### V. Cohere API Adaptability
The system must use Cohere API keys for all LLM interactions, avoiding any OpenAI dependencies. The architecture should be adaptable to Cohere's specific features and capabilities while maintaining flexibility for future updates.

### VI. User-Selected Text Support
The system must support queries limited to specific excerpts without requiring full book context. Users should be able to select text portions and ask questions specifically about those selections, with the chatbot responding appropriately within that scope.

## Scope and Constraints

### Scope
- RAG pipeline with FastAPI backend
- Neon Serverless Postgres for metadata storage
- Qdrant Cloud Free Tier for vector embeddings
- Cohere API integration for LLM interactions
- User-selected text querying capability
- Embedding in published book format (web or PDF with interactive elements)
- Modular, well-documented code with error handling and logging
- Unit tests for retrieval accuracy and integration tests for end-to-end flow

### Constraints
- Tech stack: Cohere API, FastAPI, Neon Serverless Postgres, Qdrant Cloud Free Tier
- No paid tiers beyond free limits; optimize for resource efficiency
- Zero API key leaks or security vulnerabilities
- Development tools: Build using spec-kit plus and claude cli for specification and generation
- Timeline: Iterative development with milestones for prototype, testing, and embedding

## Success Criteria

- Chatbot accurately answers 90%+ of book-related questions in blind tests
- Handles user-selected text queries without hallucinations
- Zero API key leaks or security vulnerabilities
- Successful embedding in published book with responsive UI
- Positive user feedback on clarity and usefulness

## Governance
Constitution supersedes all other project documentation and practices. Amendments require a documented proposal, review, and approval by project stakeholders. Compliance with this constitution will be reviewed regularly by the core development team. All changes to the constitution will result in a version bump following semantic versioning.

**Version**: 1.1.0 | **Ratified**: 2025-12-02 | **Last Amended**: 2025-12-12
