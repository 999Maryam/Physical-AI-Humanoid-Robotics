# AI-native Textbook - Physical AI and Humanoid Robotics

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Docusaurus](https://img.shields.io/badge/Powered%20by-Docusaurus-blue)](https://docusaurus.io/)
[![GitHub Pages](https://img.shields.io/badge/Deployed%20on-GitHub%20Pages-orange)](https://999maryam.github.io/Physical-AI-Humanoid-Robotics/)
[![Python](https://img.shields.io/badge/Made%20with-Python-3776ab.svg)](https://www.python.org/)
[![JavaScript](https://img.shields.io/badge/Made%20with-JavaScript-F7DF1E.svg)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/)

> An interactive, comprehensive textbook covering the fundamentals and advanced concepts of Physical AI and Humanoid Robotics with integrated backend services and vector database support

## 🚀 Overview

Welcome to the AI-native Textbook for Physical AI and Humanoid Robotics! This comprehensive educational platform provides an in-depth exploration of cutting-edge concepts at the intersection of artificial intelligence and robotics.

The project features:
- **Frontend**: Docusaurus-based interactive textbook with rich content and search capabilities
- **Backend**: FastAPI-powered API services for enhanced functionality
- **Vector Database**: Qdrant integration for AI-powered search and content retrieval
- **Database**: Neon PostgreSQL for structured data storage
- **Deployment**: GitHub Pages for static content and containerized backend services

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend       │    │   Databases     │
│  (Docusaurus)   │◄──►│   (FastAPI)      │◄──►│  (Qdrant/Neon)  │
│                 │    │                  │    │                 │
│ • Interactive   │    │ • API Services   │    │ • Vector Search │
│ • Documentation │    │ • Content APIs   │    │ • Data Storage  │
│ • Search        │    │ • AI Integration │    │ • Semantic      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### 📁 Project Structure

```
ai-textbook/
├── frontend/                 # Docusaurus-based textbook frontend
│   ├── docs/                 # Textbook content in Markdown
│   ├── src/                  # Custom components and styling
│   ├── static/               # Static assets
│   └── docusaurus.config.js  # Site configuration
├── backend/                  # FastAPI backend services
│   ├── main.py              # Main API application
│   ├── src/                 # Backend modules
│   └── requirements.txt     # Python dependencies
├── docker-compose.yaml      # Container orchestration
└── README.md               # This file
```

## ✨ Features

- **Interactive Learning**: Engaging content with code examples and visualizations
- **AI-Powered Search**: Vector database integration for semantic search capabilities
- **Multi-language Support**: Available in multiple languages
- **Responsive Design**: Optimized for all devices and screen sizes
- **Searchable Content**: Powerful search functionality to find topics quickly
- **Version Control**: Maintained with Git for collaborative development
- **Continuous Deployment**: Automatically deployed to GitHub Pages
- **Containerized Services**: Docker Compose for easy local development
- **Vector Database**: Qdrant for AI-powered content retrieval and recommendations

## 🛠️ Tech Stack

### Frontend
- **Framework**: [Docusaurus v3](https://docusaurus.io/) - Static site generator
- **Languages**: Markdown, JavaScript, React, CSS
- **Deployment**: GitHub Pages
- **Build Tool**: Node.js with npm

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - High-performance Python web framework
- **Languages**: Python
- **API Documentation**: Automatic OpenAPI/Swagger docs
- **Type Safety**: Built-in Pydantic validation

### Infrastructure
- **Vector Database**: [Qdrant](https://qdrant.tech/) - Vector search engine
- **SQL Database**: [Neon](https://neon.tech/) - Serverless PostgreSQL
- **Containerization**: Docker & Docker Compose
- **Deployment**: GitHub Actions + GitHub Pages

## 🚀 Quick Start

### Prerequisites

- [Node.js](https://nodejs.org/) (v18 or higher) for frontend
- [Python](https://python.org/) (v3.8 or higher) for backend
- [Docker](https://docker.com/) and [Docker Compose](https://docs.docker.com/compose/) for databases
- [Git](https://git-scm.com/)

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/999Maryam/Physical-AI-Humanoid-Robotics.git
   cd Physical-AI-Humanoid-Robotics
   ```

2. **Start database services with Docker Compose:**
   ```bash
   docker-compose up -d
   ```

3. **Set up the frontend (textbook):**
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. **Set up the backend in a new terminal:**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

5. **Access the applications:**
   - Textbook: [http://localhost:3000](http://localhost:3000)
   - Backend API: [http://localhost:8000](http://localhost:8000)
   - Backend docs: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Qdrant dashboard: [http://localhost:6333/dashboard](http://localhost:6333/dashboard)

### Development Commands

#### Frontend (Docusaurus)
```bash
# Start development server
cd frontend
npm start

# Build for production
npm run build

# Serve production build locally
npm run serve

# Clear cache
npm run clear

# Deploy to GitHub Pages
npm run deploy
```

#### Backend (FastAPI)
```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run development server
uvicorn main:app --reload

# Run tests
python -m pytest tests/
```

#### Infrastructure (Docker)
```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Reset databases
docker-compose down -v && docker-compose up -d
```

## 🌐 Deployment

### GitHub Pages (Frontend)
The frontend textbook is automatically deployed to GitHub Pages. The live version can be accessed at: [https://999maryam.github.io/Physical-AI-Humanoid-Robotics/](https://999maryam.github.io/Physical-AI-Humanoid-Robotics/)

### Manual Deployment
To deploy manually:

1. Build the frontend:
   ```bash
   cd frontend
   npm run build
   ```

2. Deploy to GitHub Pages:
   ```bash
   npm run deploy
   ```

### Backend Deployment
The backend can be containerized and deployed to cloud platforms like:
- AWS ECS/EKS
- Google Cloud Run
- Azure Container Instances
- Railway
- Render

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

### Content Guidelines
- Write in clear, accessible language
- Include practical examples and code snippets
- Follow the existing document structure
- Use appropriate headings and formatting
- Add relevant images and diagrams when helpful
- Ensure all content is properly attributed and licensed

### Development Guidelines
- Follow PEP 8 for Python code
- Use TypeScript for new frontend components
- Write tests for backend API endpoints
- Update documentation when adding new features
- Use semantic commit messages

## 📊 API Documentation

The backend API provides endpoints for:
- Content management
- AI-powered search
- User authentication
- Progress tracking
- Analytics and insights

API documentation is automatically generated at `/docs` endpoint when the backend is running.

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the backend directory:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/textbook
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your_api_key
SECRET_KEY=your_secret_key
DEBUG=true
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support & Contact

- **Project Link**: [https://github.com/999Maryam/Physical-AI-Humanoid-Robotics](https://github.com/999Maryam/Physical-AI-Humanoid-Robotics)
- **Live Site**: [https://999maryam.github.io/Physical-AI-Humanoid-Robotics/](https://999maryam.github.io/Physical-AI-Humanoid-Robotics/)
- **Issues**: [GitHub Issues](https://github.com/999Maryam/Physical-AI-Humanoid-Robotics/issues)
- **Discussions**: [GitHub Discussions](https://github.com/999Maryam/Physical-AI-Humanoid-Robotics/discussions)

## 🙏 Acknowledgments

- Built with [Docusaurus](https://docusaurus.io/) for the frontend textbook
- Powered by [FastAPI](https://fastapi.tiangolo.com/) for backend services
- Hosted on [GitHub Pages](https://pages.github.com/) for static content
- Enhanced with [Qdrant](https://qdrant.tech/) vector database
- Supported by [Neon](https://neon.tech/) serverless PostgreSQL
- Inspired by the growing field of Physical AI and Humanoid Robotics

## 📈 Project Status

- ✅ Interactive textbook frontend
- ✅ FastAPI backend services
- ✅ Vector database integration
- ✅ Docker containerization
- ✅ GitHub Pages deployment
- 🔄 AI-powered content recommendations
- 🔄 User progress tracking
- 🔄 Collaborative editing features

---

⭐ If you find this textbook helpful, please give it a star on GitHub!