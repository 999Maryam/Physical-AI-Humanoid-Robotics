# Quickstart Guide: AI-native Textbook with RAG Chatbot

This guide provides instructions to quickly set up and run the AI-native textbook application, which includes a Docusaurus frontend and a FastAPI RAG chatbot backend.

## 1. Prerequisites

Ensure you have the following installed:
- Node.js (LTS version recommended)
- npm or Yarn
- Python 3.9+ (`python --version`)
- pip (Python package installer)
- Docker and Docker Compose (for Qdrant and Neon databases)

## 2. Clone the Repository

First, clone the project repository:

```bash
git clone [REPOSITORY_URL]
cd ai-textbook
```

## 3. Set up the Backend (FastAPI RAG Chatbot)

Navigate to the `backend/` directory and set up the Python environment:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

### Database Setup (Qdrant & Neon)

This project uses Docker Compose to manage the Qdrant vector database and Neon (PostgreSQL-compatible) relational database.

1.  Create a `.env` file in the `backend/` directory based on `backend/.env.example` and fill in necessary environment variables (e.g., Neon connection string).
2.  Start the databases using Docker Compose:

    ```bash
    docker-compose up -d
    ```

3.  Run database migrations (if any, specific instructions will be provided in `backend/README.md`).

### Run the Backend

Once dependencies are installed and databases are running, start the FastAPI application:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The backend API will be available at `http://localhost:8000`.

## 4. Set up the Frontend (Docusaurus Textbook)

Open a new terminal, navigate to the `frontend/` directory, and install dependencies:

```bash
cd ../frontend
npm install  # or `yarn install`
```

### Run the Frontend

Start the Docusaurus development server:

```bash
npm start  # or `yarn start`
```

The Docusaurus textbook will be available at `http://localhost:3000`.

## 5. Interact with the Application

-   Open your web browser to `http://localhost:3000` to view the textbook.
-   The RAG chatbot functionality will be integrated into the frontend, making API calls to `http://localhost:8000`.

## Optional: Urdu Translation and Personalization

Details for enabling and configuring Urdu translation and personalized chapters will be provided in their respective feature documentation once implemented. This may involve specific environment variables or configuration files.