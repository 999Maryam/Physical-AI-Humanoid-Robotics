<!-- Sync Impact Report:
Version change: None → 1.0.0
List of modified principles:
- [PRINCIPLE_1_NAME] → Simplicity
- [PRINCIPLE_2_NAME] → Accuracy
- [PRINCIPLE_3_NAME] → Minimalism
- [PRINCIPLE_4_NAME] → Fast Builds
- [PRINCIPLE_5_NAME] → Free-tier Architecture
- [PRINCIPLE_6_NAME] → RAG Answers ONLY from Book Text
Added sections: Scope and Constraints, Success Criteria
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md: ⚠ pending
- .specify/templates/spec-template.md: ⚠ pending
- .specify/templates/tasks-template.md: ⚠ pending
- .specify/templates/commands/*.md: ⚠ pending
- README.md: ⚠ pending
- docs/quickstart.md: ⚠ pending
Follow-up TODOs: None
-->
# Physical AI & Humanoid Robotics — Essentials Constitution

## Core Principles

### I. Simplicity
The textbook and its associated tools must be easy to understand, use, and maintain. Solutions should prioritize clarity and directness over unnecessary complexity.

### II. Accuracy
All information presented in the textbook and provided by the RAG chatbot must be factually correct and up-to-date with current best practices in Physical AI and Humanoid Robotics.

### III. Minimalism
Design and implementation should focus on core functionality, avoiding extraneous features or bloat. This applies to code, content, and infrastructure.

### IV. Fast Builds
The Docusaurus build process must be optimized for speed to ensure rapid iteration and deployment, minimizing developer friction.

### V. Free-tier Architecture
All components and services used must be compatible with free-tier usage limits to ensure accessibility and minimize operational costs for users. This includes database, hosting, and AI services.

### VI. RAG Answers ONLY from Book Text
The RAG chatbot must strictly derive its answers solely from the content within the textbook. It must not generate information outside of the provided corpus.

## Scope and Constraints

### Scope
- 6 short chapters: Introduction to Physical AI, Basics of Humanoid Robotics, ROS 2 Fundamentals, Digital Twin Simulation (Gazebo + Isaac), Vision-Language-Action Systems, Capstone: Simple AI-Robot Pipeline
- Clean Docusaurus UI
- Free-tier friendly
- Lightweight embeddings
- Docusaurus textbook
- RAG chatbot (Qdrant + Neon + FastAPI)
- Select-text → Ask AI
- Optional Urdu / Personalize features

### Constraints
- No heavy GPU usage
- Minimal embeddings

## Success Criteria

- Build success
- Accurate chatbot (RAG answers ONLY from book text)
- Clean UI
- Smooth GitHub Pages deployment

## Governance
Constitution supersedes all other project documentation and practices. Amendments require a documented proposal, review, and approval by project stakeholders. Compliance with this constitution will be reviewed regularly by the core development team. All changes to the constitution will result in a version bump following semantic versioning.

**Version**: 1.0.0 | **Ratified**: 2025-12-02 | **Last Amended**: 2025-12-02
