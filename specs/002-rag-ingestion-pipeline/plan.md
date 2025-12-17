# Implementation Plan: RAG Ingestion Pipeline

**Branch**: `002-rag-ingestion-pipeline` | **Date**: 2025-12-15 | **Spec**: [link to spec.md]
**Input**: Feature specification from `/specs/002-rag-ingestion-pipeline/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Create a backend pipeline to crawl deployed Docusaurus site URLs, extract clean text, chunk content with token-aware processing, generate embeddings using Cohere, and store vectors with metadata in Qdrant for similarity search. The implementation will be in a single main.py file with functions for URL crawling, text extraction, content chunking, embedding generation, and vector storage.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: requests, beautifulsoup4, cohere, qdrant-client, python-dotenv, tiktoken or sentencepiece for tokenization
**Storage**: Qdrant vector database (remote/cloud instance)
**Testing**: pytest for unit and integration tests
**Target Platform**: Linux/Windows/Mac server environment
**Project Type**: Backend/CLI tool
**Performance Goals**: Process 1000 words of content within 10 seconds (per spec requirement SC-002)
**Constraints**: Must operate within free-tier limits of Cohere API and Qdrant Cloud Free Tier
**Scale/Scope**: Handle 10,000+ document chunks (per spec requirement SC-005)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Post-Design Validation:**

1. **Book Content Accuracy**: ✅ The pipeline will extract content from the deployed Docusaurus site at https://physical-ai-humanoid-robotics-eight-snowy.vercel.app/ ensuring accuracy of source material.
2. **User-Centric Design**: ✅ The pipeline will be designed for backend/AI engineers implementing RAG ingestion as specified in the user scenarios.
3. **Scalability with Free-tier Services**: ✅ The implementation will use Cohere API and Qdrant Cloud Free Tier as required by the constitution, with rate limiting to stay within free tier limits.
4. **Security and Privacy**: ✅ API keys will be handled via environment variables in .env files and not hardcoded, following security best practices.
5. **Cohere API Adaptability**: ✅ The system will use Cohere API for embedding generation as specified in the user requirements, using cohere Python package.
6. **User-Selected Text Support**: ✅ The pipeline will support chunking and indexing content that can later be used for user-selected text queries, with proper metadata storage.

## Project Structure

### Documentation (this feature)

```text
specs/002-rag-ingestion-pipeline/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── main.py              # Single file implementation with all functions
├── pyproject.toml       # Project dependencies managed with UV
├── .env                 # Environment variables (not committed)
├── .env.example         # Example environment variables
└── requirements.txt     # Dependencies list
```

**Structure Decision**: The implementation will follow a single-file approach in main.py as specified in the user requirements, with functions for get_all_urls, extract_text_from_url, chunk_text, embed, create_collection, save_chunk_to_qdrant, and executed in the main function. The backend directory will be created as requested.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
