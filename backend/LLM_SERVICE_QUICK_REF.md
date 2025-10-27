# LLMService - Quick Reference

## Import

```python
from app.services.llm_service import LLMService
```

## Initialization

```python
# Validates Ollama connection and initializes LLM
llm_service = LLMService()

# Raises ConnectionError if Ollama not running
```

## Core Method

### Generate Response (RAG)

```python
response = llm_service.generate_response(
    query="What is machine learning?",
    vector_store=vector_store  # VectorStoreService instance
)

# Returns:
# {
#     "answer": "Machine learning is...",
#     "source_documents": [{"content": "...", "metadata": {...}, "source": "..."}],
#     "query": "What is machine learning?"
# }
```

## Utility Methods

```python
# Check Ollama connection
is_connected = llm_service.check_connection()  # bool

# Get available models
models = llm_service.get_available_models()    # List[str]
```

## Configuration

```python
# Set in .env or settings
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
TOP_K_RETRIEVAL=5  # Number of docs to retrieve
```

## Complete Workflow

```python
from app.services.document_service import DocumentProcessor
from app.services.vector_store import VectorStoreService
from app.services.llm_service import LLMService

# 1. Process document
processor = DocumentProcessor()
doc_result = processor.process_document("paper.pdf", "paper.pdf")

# 2. Add to vector store
vector_store = VectorStoreService()
vector_store.add_documents(
    chunks=doc_result['chunks'],
    metadata={"filename": "paper.pdf"}
)

# 3. Generate response
llm_service = LLMService()
response = llm_service.generate_response(
    query="What are the main findings?",
    vector_store=vector_store
)

# 4. Display
print(response['answer'])
for src in response['source_documents']:
    print(f"Source: {src['source']}")
```

## Error Handling

```python
try:
    llm_service = LLMService()
    response = llm_service.generate_response(query, vector_store)
except ConnectionError as e:
    print(f"Ollama not accessible: {e}")
    # Start Ollama: ollama serve
except Exception as e:
    print(f"Error: {e}")
```

## Ollama Setup

```bash
# Install Ollama
# Visit https://ollama.ai

# Start Ollama
ollama serve

# Pull model
ollama pull llama3.2

# Verify
ollama list
```

## Custom Prompt Template

```
You are a helpful AI assistant specialized in explaining research papers and ML/DS concepts.
Use the following context to answer the question. If you don't know the answer, say so.

Context: {context}
Question: {question}
Answer:
```

## Testing

```bash
cd backend
python test_llm_service.py
```

## Key Features

- ✅ LangChain Ollama integration
- ✅ RetrievalQA chain for RAG
- ✅ Custom prompt template
- ✅ Connection validation
- ✅ Source attribution
- ✅ Error handling with helpful messages

## Response Format

```python
{
    "answer": str,              # Generated response
    "source_documents": [       # List of sources
        {
            "content": str,     # Document text
            "metadata": dict,   # Metadata (filename, chunk_id, etc.)
            "source": str       # Filename
        }
    ],
    "query": str                # Original question
}
```

## Common Issues

| Issue | Solution |
|-------|----------|
| `ConnectionError` | Start Ollama: `ollama serve` |
| Model not found | Pull model: `ollama pull llama3.2` |
| Slow responses | Use smaller model or reduce TOP_K_RETRIEVAL |
| Out of memory | Use quantized model or smaller model |

---

**Docs**: See `LLM_SERVICE_GUIDE.md` for complete documentation


