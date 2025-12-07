# Implementation Plan: AI-native Textbook with RAG Chatbot

**Branch**: `1-ai-textbook-rag` | **Date**: 2025-12-02 | **Spec**: specs/1-ai-textbook-rag/spec.md
**Input**: Feature specification from `/specs/1-ai-textbook-rag/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This feature involves building an AI-native textbook with Docusaurus, including a RAG chatbot for interactive learning. The chatbot will leverage Qdrant for vector storage, Neon for relational data, and free-tier embedding models to provide answers exclusively from the textbook content. Optional Urdu translation and personalized chapter experiences are also planned.

## Technical Context

**Language/Version**: Python (for RAG backend), JavaScript/TypeScript (for Docusaurus frontend)
**Primary Dependencies**: Docusaurus, Qdrant, Neon, FastAPI, Free-tier Embedding models
**Storage**: Qdrant (vector database), Neon (relational database)
**Testing**: Frontend: Jest, React Testing Library, Playwright (E2E). Backend: pytest, httpx, TestClient. Integration: Playwright for E2E across frontend and backend.
**Target Platform**: Web (Docusaurus hosted), Cloud environment (for RAG backend services)
**Project Type**: Web application (Frontend + Backend)
**Performance Goals**: Users can navigate between any two main book chapters within 5 seconds on average. RAG chatbot provides a relevant and accurate answer to 90% of in-context questions within 10 seconds.
**Constraints**: Free-tier compatible architecture, No heavy GPU usage, Minimal embeddings, RAG answers ONLY from book text.
**Scale/Scope**: 6 short chapters, supporting interactive RAG chatbot, optional Urdu translation, optional personalized chapters.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Simplicity**: The design prioritizes clarity with Docusaurus and explicit RAG architecture. Pass.
- **II. Accuracy**: RAG chatbot strictly derives answers from textbook content. Pass.
- **III. Minimalism**: Focus on core textbook and RAG chatbot features, avoiding bloat. Pass.
- **IV. Fast Builds**: Docusaurus is chosen for its efficient build process. Pass.
- **V. Free-tier Architecture**: All chosen components (Qdrant, Neon, free-tier embeddings) are compatible with free-tier usage. Pass.
- **VI. RAG Answers ONLY from Book Text**: This is a strict constraint and functional requirement. Pass.

## Project Structure

### Documentation (this feature)

```text
specs/1-ai-textbook-rag/
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
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/
```

**Structure Decision**: The project will adopt a monorepo-like structure with distinct `backend/` and `frontend/` directories to separate the Docusaurus application from the FastAPI RAG backend services, aligning with Option 2: Web application.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
|           |            |                                     |