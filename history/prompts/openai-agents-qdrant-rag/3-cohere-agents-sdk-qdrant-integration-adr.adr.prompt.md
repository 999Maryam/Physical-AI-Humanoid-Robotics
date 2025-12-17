---
id: 3
title: "OpenAI Agents SDK Qdrant Integration ADR"
stage: adr
date: 2025-12-17
surface: agent
model: Claude Sonnet 4.5
feature: openai-agents-qdrant-rag
branch: 003-openai-agents-qdrant-rag
user: Claude Code
command: /sp.adr
labels:
  - architecture
  - decision
  - cohere
  - qdrant
  - rag
links:
  spec: "F:/Maryam/Quarter_4/book_hackathon/ai-textbook/specs/003-openai-agents-qdrant-rag/spec.md"
  plan: "F:/Maryam/Quarter_4/book_hackathon/ai-textbook/specs/003-openai-agents-qdrant-rag/plan.md"
  adr: "F:/Maryam/Quarter_4/book_hackathon/ai-textbook/history/adr/ADR-001-cohere-agents-sdk-with-qdrant-integration.md"
  ticket: null
  pr: null
files:
  - "F:/Maryam/Quarter_4/book_hackathon/ai-textbook/history/adr/ADR-001-cohere-agents-sdk-with-qdrant-integration.md"
tests: []
---

## Prompt Text

OpenAI-Agents-SDK-with-Qdrant-Integration

## Response Text

Created an Architecture Decision Record (ADR) documenting the decision to use Cohere's agent framework instead of OpenAI Agents for the RAG system. This decision was necessary to maintain compliance with the project constitution which requires using Cohere API for all LLM interactions and avoiding OpenAI dependencies.

The ADR documents:
- The context of the constitution conflict
- The decision to use Cohere's agent framework with Qdrant integration
- Positive and negative consequences of this approach
- Alternative approaches that were considered and rejected
- References to related artifacts

This ADR ensures architectural decisions are properly documented for future reference and team alignment.

## Outcome

ADR successfully created and documented, providing clear rationale for the architectural decision to use Cohere instead of OpenAI for the RAG agent system.