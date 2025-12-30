---
title: RAG Chatbot for AI Textbook
emoji: 🤖
colorFrom: blue
colorTo: red
sdk: docker
pinned: false
license: apache-2.0
---

# RAG Chatbot for AI Textbook

This Space provides a chatbot interface for an AI textbook on Physical AI and Humanoid Robotics, powered by Retrieval-Augmented Generation (RAG).

## Setup

This Space runs a FastAPI backend that processes queries using:

- Cohere embeddings for document retrieval
- Qdrant vector database for storing embeddings
- Google Gemini for response generation

## Environment Variables

You'll need to set the following environment variables in the Space settings:

- `COHERE_API_KEY`: Your Cohere API key
- `GEMINI_API_KEY`: Your Google Gemini API key
- `QDRANT_URL`: Qdrant database URL (optional, defaults to local)
- `QDRANT_API_KEY`: Qdrant API key (if using cloud Qdrant)
- `COLLECTION_NAME`: Name of the Qdrant collection to use