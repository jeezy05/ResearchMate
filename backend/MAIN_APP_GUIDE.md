# FastAPI Main Application Guide

## 📋 Overview

This guide covers the main FastAPI application in `/backend/app/main.py` for the ResearchMate RAG API. The application provides a complete setup with startup/shutdown events, middleware, routing, and comprehensive logging.

## 🚀 Application Features

### Core Application Setup

```python
app = FastAPI(
    title="ResearchMate RAG API",
    description="ML/DS Research Paper Q&A Assistant with RAG and LLM",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)
```

### Key Features

- ✅ **FastAPI Application**: Full-featured API with documentation
- ✅ **CORS Middleware**: Cross-origin resource sharing support
- ✅ **Lifespan Events**: Startup and shutdown event handlers
- ✅ **Comprehensive Logging**: Structured logging with file output
- ✅ **Service Integration**: Ollama and vector store initialization
- ✅ **API Documentation**: Automatic OpenAPI/Swagger docs
- ✅ **Health Monitoring**: System health checks and status

## 🔧 Configuration

### Application Metadata

| Field | Value | Description |
|-------|-------|-------------|
| **Title** | "ResearchMate RAG API" | Application name |
| **Description** | "ML/DS Research Paper Q&A Assistant with RAG and LLM" | Application purpose |
| **Version** | "1.0.0" | API version |
| **Docs URL** | "/docs" | Swagger UI endpoint |
| **ReDoc URL** | "/redoc" | ReDoc documentation |
| **OpenAPI URL** | "/openapi.json" | OpenAPI schema |

### CORS Configuration

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # ["http://localhost:8501", "http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Allowed Origins**:
- `http://localhost:8501` (Streamlit frontend)
- `http://localhost:3000` (React frontend)

## 🎯 API Endpoints

### Root Endpoints

| Method | Endpoint | Purpose | Response |
|--------|----------|---------|----------|
| `GET` | `/` | API information | Basic info with links |
| `GET` | `/health` | Simple health check | Service status |

### API v1 Endpoints

All API endpoints are prefixed with `/api/v1`:

| Method | Endpoint | Purpose | Response |
|--------|----------|---------|----------|
| `POST` | `/api/v1/upload` | Upload PDF documents | `UploadResponse` |
| `POST` | `/api/v1/query` | Query documents with RAG | `QueryResponse` |
| `GET` | `/api/v1/health` | Comprehensive health check | `HealthResponse` |
| `DELETE` | `/api/v1/reset` | Reset system data | Success message |
| `GET` | `/api/v1/status` | Detailed system status | Status info |
| `GET` | `/api/v1/models` | Available models | Model list |

## 🔄 Lifespan Events

### Startup Sequence

The application performs comprehensive startup checks:

1. **Application Info**:
   ```python
   logger.info("🚀 Starting ResearchMate RAG API...")
   logger.info(f"   - Version: {settings.VERSION}")
   logger.info(f"   - Debug Mode: {settings.DEBUG}")
   logger.info(f"   - Host: {settings.HOST}:{settings.PORT}")
   ```

2. **Ollama Connection Check**:
   ```python
   llm_service = LLMService()
   if llm_service.check_connection():
       logger.info("✅ Ollama connection successful")
       logger.info(f"   - Model: {settings.OLLAMA_MODEL}")
   ```

3. **Vector Store Initialization**:
   ```python
   vector_store = VectorStoreService()
   status = vector_store.get_status()
   if status.get("healthy", False):
       logger.info("✅ Vector store initialized successfully")
   ```

4. **Directory Creation**:
   ```python
   settings.create_directories()
   logger.info("✅ Application directories created")
   ```

5. **Startup Complete**:
   ```python
   logger.info("🎉 ResearchMate RAG API startup complete!")
   logger.info("📚 API Documentation: http://localhost:8000/docs")
   logger.info("🔍 Health Check: http://localhost:8000/api/v1/health")
   ```

### Shutdown Sequence

```python
logger.info("🛑 Shutting down ResearchMate RAG API...")
logger.info("✅ Cleanup completed")
```

## 📝 Logging Configuration

### Logging Setup

```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),      # Console output
        logging.FileHandler("researchmate.log")  # File output
    ]
)
```

### Log Levels

- **INFO**: General application flow
- **WARNING**: Non-critical issues
- **ERROR**: Critical errors
- **DEBUG**: Detailed debugging (when enabled)

### Log Output

- **Console**: Real-time logging to terminal
- **File**: Persistent logging to `researchmate.log`

## 🧪 Testing

### Running Tests

```bash
cd backend
python test_main_app.py
```

### Test Coverage

The test suite covers:
- ✅ FastAPI app creation
- ✅ Configuration loading
- ✅ Logging setup
- ✅ Middleware configuration
- ✅ Route registration
- ✅ Lifespan events
- ✅ Documentation endpoints
- ✅ Startup sequence

### Example Test Output

```
🚀 Testing FastAPI Main Application
==================================================
🧪 Testing FastAPI app creation...
✅ FastAPI app created successfully
🧪 Testing configuration...
✅ Configuration loaded successfully
🧪 Testing logging setup...
✅ Logging configured successfully
🧪 Testing middleware...
✅ Middleware configured successfully
🧪 Testing routes...
✅ Routes configured successfully
🧪 Testing lifespan events...
✅ Lifespan events configured
🧪 Testing documentation...
✅ Documentation configured successfully
🧪 Testing startup sequence...
✅ Startup sequence completed
📊 Test Results: 8/8 tests passed
🎉 All main application tests passed!
```

## 🚀 Running the Application

### Development Mode

```bash
# Method 1: Direct Python execution
python app/main.py

# Method 2: Uvicorn command
python -m uvicorn app.main:app --reload

# Method 3: Uvicorn with specific host/port
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Production Mode

```bash
# Production server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker Mode

```bash
# Using Docker Compose
docker-compose up -d

# Using Docker directly
docker build -t researchmate-api .
docker run -p 8000:8000 researchmate-api
```

## 📚 API Documentation

### Interactive Documentation

Once the server is running, access:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

### API Testing

Use the Swagger UI for interactive testing:

1. Navigate to `http://localhost:8000/docs`
2. Click on any endpoint
3. Click "Try it out"
4. Fill in parameters and execute

## 🔍 Health Monitoring

### Health Check Endpoints

1. **Simple Health Check** (`/health`):
   ```json
   {
     "status": "healthy",
     "service": "ResearchMate RAG API",
     "version": "1.0.0"
   }
   ```

2. **Comprehensive Health Check** (`/api/v1/health`):
   ```json
   {
     "status": "healthy",
     "ollama_connected": true,
     "vector_store_ready": true,
     "model": "llama2"
   }
   ```

### Status Monitoring

Use the `/api/v1/status` endpoint for detailed system information:

```json
{
  "vector_store": {
    "healthy": true,
    "document_count": 5,
    "collection_name": "researchmate_docs"
  },
  "upload_directory": "./data/raw",
  "uploaded_files_count": 3,
  "max_upload_size_mb": 10,
  "allowed_extensions": [".pdf", ".txt", ".md", ".docx"]
}
```

## 🔧 Configuration Management

### Environment Variables

The application uses settings from `app.core.config`:

```python
from app.core.config import settings

# Application settings
settings.PROJECT_NAME      # "ResearchMate RAG API"
settings.VERSION          # "0.1.0"
settings.HOST             # "0.0.0.0"
settings.PORT             # 8000
settings.DEBUG            # False

# CORS settings
settings.CORS_ORIGINS     # ["http://localhost:8501", "http://localhost:3000"]

# Service settings
settings.OLLAMA_MODEL     # "llama2"
settings.UPLOAD_DIR       # "./data/raw"
```

### Configuration Files

- **`.env`**: Environment variables
- **`app/core/config.py`**: Pydantic settings
- **`researchmate.log`**: Application logs

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**:
   ```bash
   # Check what's using port 8000
   netstat -an | findstr 8000
   
   # Use different port
   uvicorn app.main:app --port 8001
   ```

2. **Ollama Connection Failed**:
   ```bash
   # Start Ollama
   ollama serve
   
   # Check if running
   curl http://localhost:11434/api/tags
   ```

3. **Vector Store Issues**:
   ```bash
   # Check ChromaDB directory
   ls -la ./chroma_db/
   
   # Reset if needed
   rm -rf ./chroma_db/
   ```

4. **Permission Errors**:
   ```bash
   # Check directory permissions
   ls -la ./data/
   
   # Create directories manually
   mkdir -p ./data/raw
   ```

### Debug Mode

Enable debug mode for detailed logging:

```python
# In .env file
DEBUG=true

# Or set environment variable
export DEBUG=true
```

### Log Analysis

Check the log file for issues:

```bash
# View recent logs
tail -f researchmate.log

# Search for errors
grep -i error researchmate.log

# Search for warnings
grep -i warning researchmate.log
```

## 📊 Performance Monitoring

### Key Metrics

- **Startup Time**: Application initialization duration
- **Memory Usage**: RAM consumption during operation
- **Response Time**: API endpoint response times
- **Error Rate**: Failed requests percentage

### Monitoring Endpoints

- **Health**: `/api/v1/health` - Service status
- **Status**: `/api/v1/status` - Detailed metrics
- **Models**: `/api/v1/models` - Available resources

## 🔄 Development Workflow

### Local Development

1. **Start Services**:
   ```bash
   # Terminal 1: Start Ollama
   ollama serve
   
   # Terminal 2: Start API
   python app/main.py
   ```

2. **Test Endpoints**:
   ```bash
   # Health check
   curl http://localhost:8000/api/v1/health
   
   # Upload document
   curl -X POST http://localhost:8000/api/v1/upload \
     -F "file=@test.pdf"
   
   # Query documents
   curl -X POST http://localhost:8000/api/v1/query \
     -H "Content-Type: application/json" \
     -d '{"question": "What is machine learning?"}'
   ```

3. **View Documentation**:
   - Open `http://localhost:8000/docs`
   - Test endpoints interactively

### Production Deployment

1. **Environment Setup**:
   ```bash
   # Set production environment
   export DEBUG=false
   export HOST=0.0.0.0
   export PORT=8000
   ```

2. **Start Production Server**:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

---

**Status**: ✅ Complete and tested  
**Coverage**: Full application setup with all features  
**Testing**: 8/8 tests passing  
**Documentation**: Comprehensive guide with examples

