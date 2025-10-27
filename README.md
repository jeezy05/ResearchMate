# 📚 ResearchMate - RAG End-to-End Application

A production-grade Retrieval-Augmented Generation (RAG) application for ML/DS research paper Q&A, built with FastAPI, Streamlit, and Ollama.

## 🎯 Overview

ResearchMate is a comprehensive RAG system that allows users to:
- Upload PDF research papers
- Ask questions about the content
- Get AI-powered answers with source citations
- Manage document collections
- Track conversation history

## 🏗️ Architecture

```
ResearchMate/
├── backend/           # FastAPI backend
│   ├── app/
│   │   ├── api/       # API routes
│   │   ├── core/      # Configuration
│   │   ├── models/    # Pydantic schemas
│   │   └── services/  # Business logic
│   └── requirements.txt
├── frontend/          # Streamlit frontend
│   ├── app.py         # Main Streamlit app
│   └── requirements.txt
├── data/              # Data storage
│   ├── raw/           # Uploaded PDFs
│   └── processed/     # Processed chunks
├── scripts/           # Utility scripts
└── docker-compose.yml # Container orchestration
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Ollama installed and running
- Required Python packages

### 1. Install Ollama
```bash
# Download and install Ollama from https://ollama.ai
# Then pull a model:
ollama pull llama2
```

### 2. Install Dependencies
```bash
# Backend dependencies
cd backend
pip install -r requirements.txt

# Frontend dependencies
cd ../frontend
pip install -r requirements.txt
```

### 3. Start Services

#### Option A: Automated Startup (Recommended)
```bash
# From the ResearchMate root directory
./start_services.ps1    # PowerShell (Windows)
# or
./start_services.bat    # Batch (Windows)
```

#### Option B: Manual Startup
```bash
# Terminal 1 - Backend
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd frontend
streamlit run app.py --server.port 8501 --server.address localhost
```

### 4. Access the Application
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🎨 Features

### Backend (FastAPI)
- **Document Processing**: PDF text extraction and chunking
- **Vector Store**: ChromaDB with HuggingFace embeddings
- **LLM Integration**: Ollama for text generation
- **RAG Pipeline**: Retrieval-augmented generation
- **API Endpoints**: RESTful API with comprehensive documentation
- **Health Monitoring**: System status and diagnostics

### Frontend (Streamlit)
- **Beautiful UI**: Gradient headers and custom styling
- **Document Upload**: PDF file processing with progress tracking
- **Chat Interface**: Question-answer with conversation history
- **Source Citations**: Expandable source sections with relevance scores
- **Session Management**: Persistent user sessions
- **Error Handling**: Comprehensive error messages and recovery

## 📋 API Endpoints

### Core Endpoints
- `POST /api/v1/upload` - Upload and process PDF documents
- `POST /api/v1/query` - Ask questions about documents
- `GET /api/v1/health` - System health check
- `DELETE /api/v1/reset` - Clear database and files

### Utility Endpoints
- `GET /api/v1/status` - Detailed system status
- `GET /api/v1/models` - Available Ollama models
- `GET /` - API information
- `GET /health` - Simple health check

## 🔧 Configuration

### Environment Variables
```bash
# Backend Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
CHROMA_PERSIST_DIRECTORY=./chroma_db
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RETRIEVAL=5
MAX_UPLOAD_SIZE_MB=10
CORS_ORIGINS=["http://localhost:8501"]

# Frontend Configuration
API_BASE_URL=http://localhost:8000
```

### Settings File
The backend uses Pydantic BaseSettings for configuration management. All settings can be overridden via environment variables or a `.env` file.

## 🧪 Testing

### Backend Tests
```bash
cd backend
python test_config.py           # Configuration tests
python test_document_processor.py  # Document processing tests
python test_vector_store.py     # Vector store tests
python test_llm_service.py      # LLM service tests
python test_schemas.py          # Schema validation tests
python test_api_routes.py       # API route tests
python test_main_app.py         # Main application tests
```

### Frontend Tests
```bash
cd frontend
python test_frontend.py        # Frontend tests
```

## 📚 Documentation

### Backend Documentation
- `backend/CONFIG_GUIDE.md` - Configuration guide
- `backend/DOCUMENT_PROCESSOR_GUIDE.md` - Document processing
- `backend/VECTOR_STORE_GUIDE.md` - Vector store operations
- `backend/LLM_SERVICE_GUIDE.md` - LLM service integration
- `backend/SCHEMAS_GUIDE.md` - Pydantic schemas
- `backend/API_ROUTES_GUIDE.md` - API endpoints
- `backend/MAIN_APP_GUIDE.md` - Main application

### Frontend Documentation
- `frontend/FRONTEND_GUIDE.md` - Complete frontend guide

## 🐳 Docker Deployment

### Using Docker Compose
```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build

# Stop services
docker-compose down
```

### Individual Containers
```bash
# Backend only
cd backend
docker build -t researchmate-backend .
docker run -p 8000:8000 researchmate-backend

# Frontend only
cd frontend
docker build -t researchmate-frontend .
docker run -p 8501:8501 researchmate-frontend
```

## 🔍 Troubleshooting

### Common Issues

#### Backend Connection Failed
```
❌ Cannot connect to API. Please check if the backend is running.
```
**Solution**: Start the backend server
```bash
cd backend
python -m uvicorn app.main:app --reload
```

#### Ollama Model Not Found
```
❌ Model 'llama2' not found
```
**Solution**: Install the model
```bash
ollama pull llama2
```

#### Unicode Encoding Errors
```
UnicodeEncodeError: 'charmap' codec can't encode character
```
**Solution**: These are cosmetic logging errors on Windows. The application still functions correctly.

#### Import Errors
```
ModuleNotFoundError: No module named 'app'
```
**Solution**: Run commands from the correct directory (backend/ for backend, frontend/ for frontend)

### Debug Mode
```bash
# Backend debug
cd backend
python -m uvicorn app.main:app --reload --log-level debug

# Frontend debug
cd frontend
streamlit run app.py --logger.level debug
```

## 📊 Performance

### Optimization Tips
1. **File Size**: Keep PDFs under 10MB for optimal processing
2. **Chunk Size**: Adjust chunk size based on document type
3. **Model Selection**: Choose appropriate Ollama model for your use case
4. **Hardware**: Use GPU acceleration when available

### Monitoring
- **Processing Time**: Displayed for each query
- **Chunk Count**: Track document processing
- **API Status**: Real-time connection monitoring
- **Error Rates**: Automatic error tracking

## 🔒 Security

### Input Validation
- **File Types**: PDF-only uploads
- **File Size**: Configurable size limits
- **API Endpoints**: URL validation
- **User Input**: Question sanitization

### Session Security
- **State Management**: Secure session state handling
- **API Keys**: No sensitive data in frontend
- **CORS**: Proper cross-origin configuration

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### Code Style
- Follow PEP 8 for Python code
- Use type hints for function signatures
- Add docstrings for all functions
- Include comprehensive error handling

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **FastAPI** - Modern, fast web framework for building APIs
- **Streamlit** - The fastest way to build data apps
- **Ollama** - Local LLM inference
- **ChromaDB** - Vector database for embeddings
- **LangChain** - Framework for LLM applications
- **HuggingFace** - Transformers and embeddings

## 📞 Support

### Getting Help
1. **Check Logs**: Review error messages in the console
2. **Test Backend**: Verify API connectivity at http://localhost:8000/docs
3. **Update Dependencies**: Ensure latest packages are installed
4. **Restart Services**: Restart both frontend and backend

### Common Commands
```bash
# Check backend health
curl http://localhost:8000/health

# View API documentation
open http://localhost:8000/docs

# Check Ollama status
ollama list

# View application logs
tail -f researchmate.log
```

## 🎉 Conclusion

ResearchMate provides a comprehensive, production-ready RAG system for research paper Q&A. With its beautiful interface, robust backend, and seamless integration, it offers an excellent solution for researchers and students working with academic papers.

The modular architecture makes it easy to extend and customize, while the comprehensive testing ensures reliability and performance. Whether you're uploading research papers, asking complex questions, or managing your document collection, ResearchMate provides all the tools you need for effective research assistance.

---

**Built with ❤️ for ML/DS Research**