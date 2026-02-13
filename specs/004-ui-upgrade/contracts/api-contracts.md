# API Contracts: UI Upgrade for Docusaurus Book and Chatbot

## Overview

This UI/UX improvement feature does not introduce new API endpoints. It uses existing chatbot API endpoints as defined in `frontend/src/services/chatbot_api.js`.

## Existing Endpoints Used

- **POST /api/chat** - Send user queries to the chatbot
  - Request: `{ query: string }`
  - Response: `{ text: string, source_references: string[] }`

The UI changes are purely presentational and do not modify any API contracts.