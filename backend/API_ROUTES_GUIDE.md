# FastAPI Routes Guide for ResearchMate

## 📋 Overview

This guide covers all the FastAPI endpoints in `/backend/app/api/routes.py` for the ResearchMate RAG application. The API provides endpoints for document upload, querying, health checks, and system management.

## 🚀 API Endpoints

### Base URL
All endpoints are prefixed with `/api/v1` when included in the main application.

### 1. POST /upload

**Purpose**: Upload and process PDF documents

**Request**:
- **Content-Type**: `multipart/form-data`
- **Body**: PDF file upload
- **File Size Limit**: Configurable via `MAX_UPLOAD_SIZE_MB` (default: 10MB)

**Response**: `UploadResponse`
```json
{
  "filename": "research_paper.pdf",
  "total_chunks": 15,
  "message": "Document uploaded and processed successfully",
  "status": "success"
}
```

**Validation**:
- ✅ File must be PDF format
- ✅ File size must be ≤ `MAX_UPLOAD_SIZE_MB`
- ✅ File must not be empty

**Error Codes**:
- `400`: Invalid file type or size
- `500`: Processing error

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v1/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@research_paper.pdf"
```

### 2. POST /query

**Purpose**: Query documents using RAG (Retrieval-Augmented Generation)

**Request**: `QueryRequest`
```json
{
  "question": "What is machine learning?",
  "max_results": 5
}
```

**Response**: `QueryResponse`
```json
{
  "question": "What is machine learning?",
  "answer": "Machine learning is a subset of artificial intelligence...",
  "sources": [
    {
      "content": "Machine learning algorithms...",
      "metadata": {
        "filename": "ml_paper.pdf",
        "page": 1,
        "chunk_id": "chunk_001"
      }
    }
  ],
  "processing_time": 1.5
}
```

**Validation**:
- ✅ Question must not be empty (1-2000 chars)
- ✅ Max results must be 1-10 (default: 5)

**Error Codes**:
- `400`: Invalid question or parameters
- `500`: RAG processing error

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is machine learning?", "max_results": 5}'
```

### 3. GET /health

**Purpose**: Comprehensive health check for all services

**Response**: `HealthResponse`
```json
{
  "status": "healthy",
  "ollama_connected": true,
  "vector_store_ready": true,
  "model": "llama2"
}
```

**Status Values**:
- `healthy`: All services working
- `degraded`: Some services working
- `unhealthy`: Critical services down

**Checks Performed**:
- ✅ Ollama connection (ping test)
- ✅ Vector store status
- ✅ Model availability

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v1/health"
```

### 4. DELETE /reset

**Purpose**: Reset the system by clearing all data

**Response**:
```json
{
  "message": "System reset successfully",
  "details": {
    "vector_store_cleared": true,
    "files_deleted": true,
    "upload_directory": "./data/raw"
  }
}
```

**Actions Performed**:
- ✅ Clear vector store collection
- ✅ Delete all uploaded files
- ✅ Reset system state

**Example**:
```bash
curl -X DELETE "http://localhost:8000/api/v1/reset"
```

### 5. GET /status

**Purpose**: Get detailed system status information

**Response**:
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

**Information Provided**:
- ✅ Vector store statistics
- ✅ File system status
- ✅ Configuration details

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v1/status"
```

### 6. GET /models

**Purpose**: Get available Ollama models

**Response**:
```json
{
  "available_models": ["llama2:latest"],
  "current_model": "llama2"
}
```

**Information Provided**:
- ✅ List of available models
- ✅ Currently configured model

**Example**:
```bash
curl -X GET "http://localhost:8000/api/v1/models"
```

## 🔧 Implementation Details

### Dependency Injection

All endpoints use FastAPI's dependency injection system:

```python
def get_document_service():
    """Dependency to get document service instance"""
    return DocumentService()

def get_vector_store_service():
    """Dependency to get vector store service instance"""
    return VectorStoreService()

def get_llm_service():
    """Dependency to get LLM service instance"""
    return LLMService()

def get_rag_service():
    """Dependency to get RAG service instance"""
    return RAGService()
```

### Error Handling

All endpoints include comprehensive error handling:

```python
try:
    # Endpoint logic
    return response
except HTTPException:
    raise  # Re-raise HTTP exceptions
except Exception as e:
    logger.error(f"Error in endpoint: {str(e)}")
    raise HTTPException(
        status_code=500,
        detail=f"Error processing request: {str(e)}"
    )
```

### Validation

Request validation is handled by Pydantic schemas:

- **QueryRequest**: Question validation, max_results range
- **UploadResponse**: Status validation, chunk count validation
- **HealthResponse**: Status value validation

### Logging

All endpoints include structured logging:

```python
logger.info(f"Processing query: {request.question[:50]}...")
logger.error(f"Error processing query: {str(e)}")
```

## 📊 Response Schemas

### UploadResponse
```python
class UploadResponse(BaseModel):
    filename: str                    # Name of uploaded file
    total_chunks: int               # Number of chunks created (≥0)
    message: str                   # Status message
    status: str                    # Upload status (success/error/processing)
```

### QueryResponse
```python
class QueryResponse(BaseModel):
    question: str                    # Original question
    answer: str                     # Generated answer
    sources: List[Dict[str, Any]]   # Source documents
    processing_time: float          # Processing time in seconds (≥0)
```

### HealthResponse
```python
class HealthResponse(BaseModel):
    status: str                    # System status (healthy/degraded/unhealthy)
    ollama_connected: bool         # Ollama connection status
    vector_store_ready: bool       # Vector store status
    model: str                     # Current model name
```

## 🧪 Testing

### Running Tests

```bash
cd backend
python test_routes_simple.py
```

### Test Coverage

The test suite covers:
- ✅ Route imports and initialization
- ✅ Schema validation
- ✅ Dependency injection
- ✅ Route definitions
- ✅ Error handling

### Example Test Output

```
🚀 Testing FastAPI Routes (Simple)
==================================================
🧪 Testing route imports...
✅ Route imports working
🧪 Testing schema validation...
✅ Schema validation working
🧪 Testing dependency injection...
✅ Dependency injection working
🧪 Testing route definitions...
✅ All required routes found
🧪 Testing error handling...
✅ Error handling working
📊 Test Results: 5/5 tests passed
🎉 All route tests passed!
```

## 🚀 Usage Examples

### Complete Workflow

1. **Check System Health**:
   ```bash
   curl -X GET "http://localhost:8000/api/v1/health"
   ```

2. **Upload Document**:
   ```bash
   curl -X POST "http://localhost:8000/api/v1/upload" \
     -F "file=@research_paper.pdf"
   ```

3. **Query Documents**:
   ```bash
   curl -X POST "http://localhost:8000/api/v1/query" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is machine learning?"}'
   ```

4. **Check Status**:
   ```bash
   curl -X GET "http://localhost:8000/api/v1/status"
   ```

### Python Client Example

```python
import requests

# Health check
response = requests.get("http://localhost:8000/api/v1/health")
print(response.json())

# Upload file
with open("research_paper.pdf", "rb") as f:
    files = {"file": f}
    response = requests.post("http://localhost:8000/api/v1/upload", files=files)
    print(response.json())

# Query documents
query_data = {
    "question": "What is machine learning?",
    "max_results": 5
}
response = requests.post("http://localhost:8000/api/v1/query", json=query_data)
print(response.json())
```

## 🔍 Troubleshooting

### Common Issues

1. **File Upload Fails**:
   - Check file is PDF format
   - Verify file size < MAX_UPLOAD_SIZE_MB
   - Ensure upload directory exists

2. **Query Fails**:
   - Check Ollama is running: `ollama serve`
   - Verify model is available: `ollama list`
   - Check vector store has documents

3. **Health Check Fails**:
   - Start Ollama: `ollama serve`
   - Check vector store initialization
   - Verify model is pulled: `ollama pull llama2`

### Debug Tips

1. **Check Logs**: Look for error messages in application logs
2. **Test Services**: Use individual service tests
3. **Verify Configuration**: Check settings in config.py
4. **Test Dependencies**: Ensure all services are running

## 📚 API Documentation

### OpenAPI/Swagger

The API automatically generates OpenAPI documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

### Interactive Testing

Use the Swagger UI for interactive API testing:

1. Navigate to `http://localhost:8000/docs`
2. Click on any endpoint
3. Click "Try it out"
4. Fill in parameters and execute

---

**Status**: ✅ Complete and tested  
**Coverage**: All core endpoints with validation  
**Testing**: 5/5 tests passing  
**Documentation**: Comprehensive guide with examples

