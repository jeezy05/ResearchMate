# Pydantic Schemas Guide for ResearchMate

## 📋 Overview

This guide covers all the Pydantic models and schemas used in the ResearchMate RAG API for request/response validation, data serialization, and type safety.

## 🎯 Core Request/Response Schemas

### 1. UploadResponse

**Purpose**: Response schema for file upload operations

```python
class UploadResponse(BaseModel):
    filename: str                    # Name of the uploaded file
    total_chunks: int               # Number of text chunks created (≥0)
    message: str                   # Status message
    status: str                    # Upload status (success/error/processing)
```

**Field Validators**:
- `status`: Must be one of `['success', 'error', 'processing']`
- `total_chunks`: Must be ≥ 0

**Example**:
```python
response = UploadResponse(
    filename="research_paper.pdf",
    total_chunks=15,
    message="File processed successfully",
    status="success"
)
```

### 2. QueryRequest

**Purpose**: Request schema for asking questions to the RAG system

```python
class QueryRequest(BaseModel):
    question: str                   # The question to ask (1-2000 chars)
    max_results: Optional[int] = 5  # Max results to return (1-10)
```

**Field Validators**:
- `question`: Must not be empty, stripped of whitespace
- `max_results`: Must be between 1 and 10 (inclusive)

**Example**:
```python
request = QueryRequest(
    question="What is machine learning?",
    max_results=5
)
```

### 3. QueryResponse

**Purpose**: Response schema for RAG query results

```python
class QueryResponse(BaseModel):
    question: str                    # The original question
    answer: str                     # The generated answer
    sources: List[Dict[str, Any]]   # Source documents with content and metadata
    processing_time: float          # Processing time in seconds (≥0)
```

**Field Validators**:
- `sources`: Each source must have `content` and `metadata` fields
- `processing_time`: Must be ≥ 0

**Example**:
```python
response = QueryResponse(
    question="What is machine learning?",
    answer="Machine learning is a subset of AI...",
    sources=[
        {
            "content": "ML is a subset of AI...",
            "metadata": {"filename": "ml_paper.pdf", "page": 1}
        }
    ],
    processing_time=1.5
)
```

### 4. HealthResponse

**Purpose**: System health check response

```python
class HealthResponse(BaseModel):
    status: str                    # Overall system status
    ollama_connected: bool         # Whether Ollama is connected
    vector_store_ready: bool       # Whether vector store is ready
    model: str                     # Current LLM model name
```

**Field Validators**:
- `status`: Must be one of `['healthy', 'unhealthy', 'degraded']`

**Example**:
```python
health = HealthResponse(
    status="healthy",
    ollama_connected=True,
    vector_store_ready=True,
    model="llama2"
)
```

## 📄 Additional Schemas

### DocumentBase
Base schema for document information:
```python
class DocumentBase(BaseModel):
    filename: str                   # Name of the document
    content_type: str              # MIME type of the document
    size: int                      # Size in bytes (≥0)
```

### Document
Extended document schema with metadata:
```python
class Document(DocumentBase):
    id: str                        # Unique document identifier
    upload_date: datetime          # When the document was uploaded
    processed: bool = False        # Whether the document has been processed
    chunk_count: Optional[int]    # Number of chunks created (≥0)
```

### SourceDocument
Source document metadata for RAG responses:
```python
class SourceDocument(BaseModel):
    filename: str                  # Name of the source document
    page: Optional[int]           # Page number if applicable (≥1)
    chunk_id: str                 # Unique identifier for the text chunk
    relevance_score: float        # Relevance score (0.0-1.0)
    content_preview: str          # Preview of the content (≤500 chars)
```

### ErrorResponse
Error response schema:
```python
class ErrorResponse(BaseModel):
    error: str                    # Error message
    detail: Optional[str]          # Detailed error information
    timestamp: datetime            # When the error occurred
```

### ConversationMessage
Individual conversation message:
```python
class ConversationMessage(BaseModel):
    role: str                     # Role (user/assistant/system)
    content: str                  # Content of the message
    timestamp: datetime           # When the message was sent
```

**Field Validators**:
- `role`: Must be one of `['user', 'assistant', 'system']`

### ConversationHistory
Complete conversation history:
```python
class ConversationHistory(BaseModel):
    conversation_id: str           # Unique conversation identifier
    messages: List[ConversationMessage]  # List of messages
    created_at: datetime          # When the conversation was created
    updated_at: datetime          # When the conversation was last updated
```

## 🧪 Testing Schemas

### Running Schema Tests

```bash
cd backend
python test_schemas.py
```

### Test Coverage

The test suite covers:
- ✅ Valid schema creation
- ✅ Field validation (required fields, ranges, formats)
- ✅ Invalid data rejection
- ✅ JSON serialization/deserialization
- ✅ Type safety

### Example Test Output

```
🚀 Testing Pydantic Schemas
==================================================
🧪 Testing UploadResponse...
✅ Valid UploadResponse created successfully
✅ Status validation working
🧪 Testing QueryRequest...
✅ Valid QueryRequest created successfully
✅ Question validation working
✅ Max results validation working
...
📊 Test Results: 8/8 tests passed
🎉 All schema tests passed!
```

## 🔧 Usage Examples

### API Endpoint Integration

```python
from fastapi import FastAPI
from app.models.schemas import QueryRequest, QueryResponse

app = FastAPI()

@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    # request.question is validated (not empty, 1-2000 chars)
    # request.max_results is validated (1-10)
    
    # Your RAG logic here
    answer = "Generated answer..."
    sources = [{"content": "...", "metadata": {...}}]
    
    return QueryResponse(
        question=request.question,
        answer=answer,
        sources=sources,
        processing_time=1.5
    )
```

### Data Validation

```python
from app.models.schemas import QueryRequest

# This will raise ValidationError
try:
    invalid_request = QueryRequest(
        question="",  # Empty question
        max_results=15  # Too many results
    )
except ValidationError as e:
    print(f"Validation failed: {e}")
```

### JSON Serialization

```python
from app.models.schemas import UploadResponse

# Create response
response = UploadResponse(
    filename="test.pdf",
    total_chunks=5,
    message="Success",
    status="success"
)

# Serialize to JSON
json_data = response.model_dump()
print(json.dumps(json_data, indent=2))

# Deserialize from JSON
restored = UploadResponse(**json_data)
```

## 📊 Schema Validation Rules

| Schema | Field | Validation Rules |
|--------|-------|------------------|
| `UploadResponse` | `status` | Must be: success, error, processing |
| `UploadResponse` | `total_chunks` | Must be ≥ 0 |
| `QueryRequest` | `question` | 1-2000 chars, not empty |
| `QueryRequest` | `max_results` | 1-10 (inclusive) |
| `QueryResponse` | `sources` | Each must have content + metadata |
| `QueryResponse` | `processing_time` | Must be ≥ 0 |
| `HealthResponse` | `status` | Must be: healthy, unhealthy, degraded |
| `SourceDocument` | `relevance_score` | 0.0-1.0 (inclusive) |
| `SourceDocument` | `content_preview` | Max 500 chars |
| `ConversationMessage` | `role` | Must be: user, assistant, system |

## 🚀 Benefits

### Type Safety
- ✅ Compile-time type checking
- ✅ IDE autocomplete and error detection
- ✅ Runtime validation

### Data Validation
- ✅ Automatic field validation
- ✅ Custom validator functions
- ✅ Clear error messages

### API Documentation
- ✅ Automatic OpenAPI/Swagger docs
- ✅ Request/response examples
- ✅ Field descriptions

### JSON Handling
- ✅ Automatic serialization
- ✅ Deserialization with validation
- ✅ Nested object support

## 🔍 Troubleshooting

### Common Validation Errors

1. **Empty Question**:
   ```
   ValidationError: Question cannot be empty
   ```
   **Fix**: Provide a non-empty question string

2. **Invalid Status**:
   ```
   ValidationError: Status must be one of: ['success', 'error', 'processing']
   ```
   **Fix**: Use a valid status value

3. **Invalid Max Results**:
   ```
   ValidationError: Input should be less than or equal to 10
   ```
   **Fix**: Use max_results between 1-10

4. **Missing Source Fields**:
   ```
   ValidationError: Each source must have 'metadata' field
   ```
   **Fix**: Include both 'content' and 'metadata' in sources

### Debug Tips

1. **Check Field Types**: Ensure all fields match expected types
2. **Validate Ranges**: Check numeric constraints (ge, le)
3. **Test Edge Cases**: Empty strings, boundary values
4. **Use Model Dump**: Inspect serialized data structure

---

**Status**: ✅ Complete and tested  
**Coverage**: All core schemas with validation  
**Testing**: 8/8 tests passing  
**Documentation**: Comprehensive guide with examples

