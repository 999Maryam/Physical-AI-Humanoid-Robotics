# Development Tasks: AI-native Textbook with RAG Chatbot

**Feature Branch**: `1-ai-textbook-rag` | **Date**: 2025-12-02 | **Spec**: specs/1-ai-textbook-rag/spec.md | **Plan**: specs/1-ai-textbook-rag/plan.md

This document outlines the development tasks for building the AI-native textbook with a RAG chatbot, organized by phases and user stories, with priorities and clear file paths.

## Phase 1: Setup

- [ ] T001 Set up backend Python environment and dependencies in `backend/requirements.txt`
- [ ] T002 Set up frontend Node.js environment and dependencies in `frontend/package.json`
- [ ] T003 Configure Docker Compose for Qdrant and Neon databases in `docker-compose.yaml`

## Phase 2: Foundational

- [ ] T004 Initialize Docusaurus project structure in `frontend/`
- [ ] T005 Initialize FastAPI project structure in `backend/`
- [ ] T006 Integrate free-tier embedding model for content processing in `backend/src/services/embedding_service.py`
- [ ] T007 Implement initial content ingestion pipeline to Qdrant/Neon for textbook content in `backend/src/services/ingestion_service.py`

## Phase 3: User Story 1 - Read Textbook Content (Priority: P1)

**Goal**: As a student, I want to read the AI-native textbook chapters so I can learn about Physical AI, Robotics, and related topics.
**Independent Test**: Can be fully tested by navigating through all provided chapters and verifying content display.

- [ ] T008 [US1] Create Docusaurus page for "Introduction to Physical AI" in `frontend/docs/introduction-to-physical-ai.mdx`
- [ ] T009 [US1] Create Docusaurus page for "Basics of Humanoid Robotics" in `frontend/docs/basics-of-humanoid-robotics.mdx`
- [ ] T010 [US1] Create Docusaurus page for "ROS 2 Fundamentals" in `frontend/docs/ros-2-fundamentals.mdx`
- [ ] T011 [US1] Create Docusaurus page for "Digital Twin Simulation (Gazebo + Isaac)" in `frontend/docs/digital-twin-simulation.mdx`
- [ ] T012 [US1] Create Docusaurus page for "Vision-Language-Action Systems" in `frontend/docs/vision-language-action-systems.mdx`
- [ ] T013 [US1] Create Docusaurus page for "Capstone" in `frontend/docs/capstone.mdx`
- [ ] T014 [US1] Configure Docusaurus `sidebars.js` for automatic sidebar generation in `frontend/sidebars.js`
- [ ] T015 [US1] Implement Playwright E2E test for navigating chapters in `frontend/tests/e2e/chapter_navigation.spec.js`

## Phase 4: User Story 2 - Interact with RAG C
hatbot (Priority: P1)

**Goal**: As a student, I want to ask questions about the textbook content and receive relevant answers from an AI chatbot so I can deepen my understanding and clarify concepts.
**Independent Test**: Can be fully tested by asking a range of questions related to textbook content and evaluating chatbot responses for accuracy and relevance.

- [ ] T016 [P] [US2] Create `UserQuery` Pydantic model in `backend/src/models/user_query.py`
- [ ] T017 [P] [US2] Create `ChatbotResponse` Pydantic model in `backend/src/models/chatbot_response.py`
- [ ] T018 [US2] Implement RAG service logic (Qdrant, Neon integration) in `backend/src/services/rag_service.py`
- [ ] T019 [US2] Create FastAPI endpoint `/chat/query` in `backend/src/api/chatbot.py`
- [ ] T020 [P] [US2] Implement unit tests for `UserQuery` model in `backend/tests/unit/test_user_query.py`
- [ ] T021 [P] [US2] Implement unit tests for `ChatbotResponse` model in `backend/tests/unit/test_chatbot_response.py`
- [ ] T022 [US2] Implement unit/API tests for RAG service logic in `backend/tests/api/test_rag_service.py`
- [ ] T023 [US2] Create chatbot UI component in `frontend/src/components/Chatbot.jsx`
- [ ] T024 [US2] Integrate chatbot component with backend API in `frontend/src/services/chatbot_api.js`
- [ ] T025 [US2] Implement Playwright E2E test for chatbot interaction in `frontend/tests/e2e/chatbot_interaction.spec.js`

## Phase 5: User Story 3 - Urdu Translation (Priority: P2)


**Goal**: As an Urdu-speaking student, I want to read the textbook content in Urdu so I can learn in my native language.
**Independent Test**: Can be fully tested by switching the display language to Urdu and verifying that all provided textbook content is translated.

- [ ] T026 [US3] Implement translation service in `backend/src/services/translation_service.py`
- [ ] T027 [US3] Create FastAPI endpoint `/chapters/{chapter_id}/translate` in `backend/src/api/translation.py`
- [ ] T028 [P] [US3] Implement unit tests for translation service in `backend/tests/unit/test_translation_service.py`
- [ ] T029 [US3] Create language switcher UI component in `frontend/src/components/LanguageSwitcher.jsx`
- [ ] T030 [US3] Implement content display with translation in `frontend/src/theme/DocItem/Content/index.jsx` (or similar Docusaurus content rendering)
- [ ] T031 [US3] Implement Playwright E2E test for Urdu translation in `frontend/tests/e2e/urdu_translation.spec.js`

## Phase 6: User Story 4 - Personalized Chapter (Priority: P2)

**Goal**: As a student, I want to experience a personalized chapter so the content adapts to my learning style or previous interactions.
**Independent Test**: Can be fully tested by enabling personalization and observing content adaptation across a sample chapter.

- [ ] T032 [US4] Create `UserProfile` Pydantic model in `backend/src/models/user_profile.py`
- [ ] T033 [US4] Implement personalization logic (learning style, reading history, quiz performance) in `backend/src/services/personalization_service.py`
- [ ] T034 [P] [US4] Implement unit tests for `UserProfile` model in `backend/tests/unit/test_user_profile.py`
- [ ] T035 [US4] Implement unit tests for personalization service in `backend/tests/api/test_personalization_service.py`
- [ ] T036 [US4] Create user profile/preferences UI in `frontend/src/components/UserProfileSettings.jsx`
- [ ] T037 [US4] Implement dynamic content adaptation in `frontend/src/theme/DocItem/Content/index.jsx` (or similar Docusaurus content rendering)
- [ ] T038 [US4] Implement Playwright E2E test for personalization in `frontend/tests/e2e/personalization.spec.js`

## Dependencies


- Phase 1 (Setup) must be completed before Phase 2 (Foundational).
- Phase 2 (Foundational) must be completed before any User Story Phase (Phase 3-6).
- User Story Phases (3, 4, 5, 6) can largely be developed in parallel after Foundational tasks, with the exception of inter-story dependencies (e.g., personalization might leverage RAG features if expanding upon user behavior).
- Within each User Story Phase, tasks are ordered by internal dependencies (e.g., models before services, services before API endpoints, API before UI integration, and UI before E2E tests).

## Parallel Execution Opportunities

- **Foundational**: T004, T005 (Docusaurus and FastAPI project initialization) can run in parallel.
- **User Story 2 (RAG Chatbot)**: T016, T017, T020, T021 can run in parallel.
- **User Story 3 (Urdu Translation)**: T028 can run in parallel with T026/T027 development.
- **User Story 4 (Personalized Chapter)**: T034 can run in parallel with T032/T033 development.

## Implementation Strategy

Development will follow an MVP-first approach, prioritizing User Story 1 (Read Textbook Content) and User Story 2 (Interact with RAG Chatbot) as the core functionality. Subsequent user stories (Urdu Translation and Personalized Chapter) will be implemented incrementally. Each user story phase is designed to be independently testable and deliver value.

## Overall Task Summary

- **Total Tasks**: 41
- **Tasks per User Story**:
    - US1 (Read Textbook Content): 8 tasks
    - US2 (Interact with RAG Chatbot): 10 tasks
    - US3 (Urdu Translation): 6 tasks
    - US4 (Personalized Chapter): 7 tasks
- **Setup/Foundational/Polish**: 10 tasks
- **Parallel Opportunities**: Identified within Foundational and each User Story phase.
- **MVP Scope**: User Story 1 and User Story 2.
- **Independent Test Criteria**: Each user story defines clear independent test criteria for verification.
- **Format Validation**: All tasks follow the required checklist format with IDs, labels, and file paths.