# ADR-001: Adoption of OpenAI Agents SDK with Qdrant Integration

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-17
- **Feature:** openai-agents-qdrant-rag
- **Context:** The feature specification calls for creating an OpenAI Agents SDK capable of retrieving information from Qdrant and answering questions strictly on the embedded book content. A decision was needed to select the appropriate agent framework that provides good tool-calling support and integration with Qdrant vector database.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

Use OpenAI Agents SDK for the RAG system with the following components:

- **Agent Framework**: OpenAI Agents SDK for orchestration and reasoning
- **Vector Database**: Qdrant for storing and retrieving book content embeddings
- **Integration Pattern**: Custom retrieval tools that connect OpenAI agents to Qdrant
- **Response Generation**: OpenAI language models for grounded response generation
- **Retrieval Strategy**: Semantic search in Qdrant with top-k results for context
- **Embedding Service**: Cohere for generating document embeddings (separate from agent framework)

## Consequences

### Positive

- Leverages OpenAI's strong agent orchestration and tool-calling capabilities
- Provides excellent integration with OpenAI's language models
- Enables complex multi-step reasoning workflows
- Preserves existing Qdrant integration architecture
- Enables grounded responses without hallucinations
- Takes advantage of OpenAI's tool calling and function execution features

## Alternatives Considered

**Alternative A: LangChain Agent Framework** - Use LangChain's agent system instead of OpenAI Agents
- Why rejected: OpenAI Agents provide more native integration with OpenAI's models
- Would require additional abstraction layers

**Alternative B: Custom Agent Framework** - Build a custom agent system using OpenAI APIs
- Why rejected: Would require significant development effort
- Would reinvent existing functionality available in OpenAI's framework

**Alternative C: Cohere Tools** - Use Cohere's tool calling capabilities instead of OpenAI Agents
- Why rejected: OpenAI Agents provide more mature agent orchestration features
- Would create inconsistency with primary LLM provider

## References

- Feature Spec: F:/Maryam/Quarter_4/book_hackathon/ai-textbook/specs/003-openai-agents-qdrant-rag/spec.md
- Implementation Plan: F:/Maryam/Quarter_4/book_hackathon/ai-textbook/specs/003-openai-agents-qdrant-rag/plan.md
- Related ADRs: None
- Evaluator Evidence: F:/Maryam/Quarter_4/book_hackathon/ai-textbook/history/prompts/openai-agents-qdrant-rag/2-create-cohere-rag-agent-plan.plan.prompt.md