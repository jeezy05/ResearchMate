# ResearchMate RAG API Startup Guide

## 🚀 Quick Start

### Prerequisites

1. **Ollama Running**: Make sure Ollama is installed and running
   ```bash
   # Start Ollama
   ollama serve
   
   # Verify it's running
   curl http://localhost:11434/api/tags
   ```

2. **Model Available**: Ensure the model is installed
   ```bash
   # Check available models
   ollama list
   
   # If llama2 is not installed, pull it
   ollama pull llama2
   ```

### Starting the Server

#### Option 1: Using the Startup Script (Recommended)
```bash
cd backend
python start_server.py
```

#### Option 2: Using Batch File (Windows)
```cmd
cd backend
start_server.bat
```

#### Option 3: Direct Uvicorn Command
```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Option 4: Direct Python Execution
```bash
cd backend
python app/main.py
```

## 🔍 Verification

### Check Server Status

Once the server is running, verify it's working:

1. **Root Endpoint**: http://localhost:8000/
2. **Health Check**: http://localhost:8000/api/v1/health
3. **API Documentation**: http://localhost:8000/docs

### Test with cURL

```bash
# Root endpoint
curl http://localhost:8000/

# Health check
curl http://localhost:8000/api/v1/health

# Detailed status
curl http://localhost:8000/api/v1/status

# Available models
curl http://localhost:8000/api/v1/models
```

## 📚 API Endpoints

### Core Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/` | API information |
| `GET` | `/health` | Simple health check |
| `GET` | `/api/v1/health` | Comprehensive health check |
| `GET` | `/api/v1/status` | Detailed system status |
| `GET` | `/api/v1/models` | Available models |
| `POST` | `/api/v1/upload` | Upload PDF documents |
| `POST` | `/api/v1/query` | Query documents with RAG |
| `DELETE` | `/api/v1/reset` | Reset system data |

### Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🧪 Testing the API

### 1. Health Check
```bash
curl -X GET "http://localhost:8000/api/v1/health"
```

Expected response:
```json
{
  "status": "healthy",
  "ollama_connected": true,
  "vector_store_ready": true,
  "model": "llama2"
}
```

### 2. Upload Document
```bash
curl -X POST "http://localhost:8000/api/v1/upload" \
  -F "file=@your_document.pdf"
```

### 3. Query Documents
```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is machine learning?", "max_results": 5}'
```

## 🔧 Troubleshooting

### Common Issues

#### 1. "ModuleNotFoundError: No module named 'app'"
**Solution**: Use the correct startup method:
```bash
# ❌ Wrong
python app/main.py

# ✅ Correct
python -m uvicorn app.main:app --reload
```

#### 2. "Ollama connection failed"
**Solution**: Start Ollama first:
```bash
ollama serve
```

#### 3. "Model not found"
**Solution**: Install the model:
```bash
ollama pull llama2
```

#### 4. "Port already in use"
**Solution**: Use a different port:
```bash
python -m uvicorn app.main:app --port 8001
```

#### 5. Unicode encoding errors
**Note**: These are cosmetic logging issues on Windows and don't affect functionality. The server works correctly despite these warnings.

### Debug Mode

Enable debug mode for detailed logging:
```bash
# Set environment variable
export DEBUG=true

# Or create .env file
echo "DEBUG=true" > .env
```

### Log Files

Check the log file for detailed information:
```bash
# View recent logs
tail -f researchmate.log

# Search for errors
grep -i error researchmate.log
```

## 🚀 Production Deployment

### Using Uvicorn with Workers
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Docker
```bash
# Build image
docker build -t researchmate-api .

# Run container
docker run -p 8000:8000 researchmate-api
```

### Using Docker Compose
```bash
docker-compose up -d
```

## 📊 Monitoring

### Health Endpoints

1. **Simple Health**: `/health` - Basic service status
2. **Comprehensive Health**: `/api/v1/health` - Full system status
3. **Detailed Status**: `/api/v1/status` - System metrics

### Log Monitoring

```bash
# Real-time logs
tail -f researchmate.log

# Error monitoring
grep -i error researchmate.log

# Performance monitoring
grep -i "processing time" researchmate.log
```

## 🔄 Development Workflow

### Local Development

1. **Start Ollama**:
   ```bash
   ollama serve
   ```

2. **Start API Server**:
   ```bash
   cd backend
   python start_server.py
   ```

3. **Test Endpoints**:
   - Open http://localhost:8000/docs
   - Test endpoints interactively

4. **Upload Documents**:
   - Use the Swagger UI to upload PDFs
   - Or use cURL commands

5. **Query Documents**:
   - Ask questions about uploaded documents
   - Get RAG-powered answers

### Hot Reload

The server runs with `--reload` flag, so code changes are automatically detected and the server restarts.

## 📝 Configuration

### Environment Variables

Create a `.env` file in the backend directory:
```bash
# Application settings
DEBUG=false
HOST=0.0.0.0
PORT=8000

# Ollama settings
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# Vector store settings
CHROMA_PERSIST_DIRECTORY=./chroma_db
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# File upload settings
MAX_UPLOAD_SIZE_MB=10
UPLOAD_DIR=./data/raw
```

### CORS Settings

Update CORS origins in `app/core/config.py`:
```python
CORS_ORIGINS: List[str] = [
    "http://localhost:8501",  # Streamlit frontend
    "http://localhost:3000", # React frontend
    "http://localhost:8080"  # Vue frontend
]
```

## 🎯 Next Steps

Once the server is running:

1. **Test the API**: Use the Swagger UI at http://localhost:8000/docs
2. **Upload Documents**: Upload PDF files for processing
3. **Query Documents**: Ask questions about your documents
4. **Integrate Frontend**: Connect your Streamlit/React frontend
5. **Monitor Performance**: Check logs and health endpoints

## 📞 Support

If you encounter issues:

1. **Check Logs**: Look at `researchmate.log` for errors
2. **Verify Services**: Ensure Ollama is running
3. **Test Endpoints**: Use the health check endpoints
4. **Check Configuration**: Verify settings in config.py

---

**Status**: ✅ Server ready to start  
**Prerequisites**: Ollama running with llama2 model  
**Access**: http://localhost:8000/docs for interactive testing

