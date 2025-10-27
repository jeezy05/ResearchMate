# LLMService - Complete Guide

## Overview

The `LLMService` provides Ollama integration with LangChain for retrieval-augmented generation (RAG). It handles LLM interactions, creates RetrievalQA chains, and generates responses based on retrieved context from documents.

## Location

```python
from app.services.llm_service import LLMService
```

## Key Technologies

- **Ollama** - Local LLM runtime
- **LangChain** - LLM orchestration framework
- **RetrievalQA Chain** - RAG implementation

---

## Class: LLMService

### Initialization

```python
llm_service = LLMService()
```

**What happens on initialization:**

1. ✓ Loads configuration from settings
2. ✓ Validates Ollama connection
3. ✓ Initializes Ollama LLM via LangChain
4. ✓ Creates custom prompt template for research papers
5. ✓ Validates model availability

**Configuration from Settings:**
- `OLLAMA_BASE_URL` - Ollama server URL (default: http://localhost:11434)
- `OLLAMA_MODEL` - Model name (default: llama3.2)
- Temperature: 0.7 (hardcoded)

**Raises:**
- `ConnectionError` - If Ollama is not accessible
- `ConnectionError` - If model is not pulled

---

## Methods

### 1. `__init__()`

Initialize LLM Service with Ollama.

**Features:**
- ✓ Connection validation before initialization
- ✓ Model availability check
- ✓ Helpful error messages
- ✓ Custom prompt template setup

**Error Messages:**

If Ollama is not running:
```
Cannot connect to Ollama at http://localhost:11434
Please ensure Ollama is running:
  1. Install Ollama from https://ollama.ai
  2. Start Ollama: ollama serve
  3. Pull model: ollama pull llama3.2
```

If model is not available:
```
Model 'llama3.2' not found in Ollama.
Available models: ['llama2', 'mistral']
Pull the model with: ollama pull llama3.2
```

---

### 2. `generate_response()`

Generate a response using RAG (Retrieval-Augmented Generation).

**Signature:**
```python
def generate_response(self, query: str, vector_store: VectorStoreService) -> dict
```

**Parameters:**
- `query` (str): The user's question
- `vector_store` (VectorStoreService): Vector store instance for retrieval

**Returns:**
```python
{
    "answer": str,                    # Generated response
    "source_documents": List[dict],   # Sources used
    "query": str                      # Original question
}
```

**Source Documents Format:**
```python
{
    "content": "Document text...",
    "metadata": {"filename": "...", "chunk_id": "...", ...},
    "source": "document.pdf"
}
```

**Features:**
- ✓ Validates Ollama connection before generating
- ✓ Creates retriever from vector store
- ✓ Builds RetrievalQA chain with custom prompt
- ✓ Returns answer with source attribution
- ✓ Uses `TOP_K_RETRIEVAL` from settings

**How It Works:**

1. **Retrieve** - Gets relevant documents from vector store
2. **Create Chain** - Builds RetrievalQA chain with LLM and retriever
3. **Generate** - LLM generates answer based on context
4. **Format** - Returns structured response with sources

**Example:**
```python
from app.services.llm_service import LLMService
from app.services.vector_store import VectorStoreService

llm_service = LLMService()
vector_store = VectorStoreService()

# Assume documents are already in vector store

response = llm_service.generate_response(
    query="What is machine learning?",
    vector_store=vector_store
)

print(f"Answer: {response['answer']}")
print(f"Sources: {len(response['source_documents'])}")

for src in response['source_documents']:
    print(f"  - {src['source']}: {src['content'][:100]}...")
```

---

### 3. `check_connection()`

Check if Ollama is accessible.

**Signature:**
```python
def check_connection(self) -> bool
```

**Returns:**
- `True` if Ollama is running and accessible
- `False` otherwise

**Example:**
```python
llm_service = LLMService()

if llm_service.check_connection():
    print("✓ Ollama is running")
else:
    print("✗ Ollama is not accessible")
```

---

### 4. `get_available_models()`

Get list of available Ollama models.

**Signature:**
```python
def get_available_models(self) -> list
```

**Returns:**
- List of model names (e.g., `["llama2", "llama3.2", "mistral"]`)

**Example:**
```python
llm_service = LLMService()
models = llm_service.get_available_models()

print(f"Available models: {models}")
```

---

## Custom Prompt Template

The LLMService uses a specialized prompt template for research papers:

```
You are a helpful AI assistant specialized in explaining research papers and ML/DS concepts.
Use the following context to answer the question. If you don't know the answer, say so.

Context: {context}

Question: {question}

Answer:
```

**Key Features:**
- Specialized for research papers and ML/DS concepts
- Instructs to use only provided context
- Encourages honesty when answer is unknown

---

## Complete Usage Examples

### Example 1: Full RAG Pipeline

```python
from app.services.document_service import DocumentProcessor
from app.services.vector_store import VectorStoreService
from app.services.llm_service import LLMService

# 1. Process document
processor = DocumentProcessor()
doc_result = processor.process_document(
    file_path="research_paper.pdf",
    filename="research_paper.pdf"
)

# 2. Add to vector store
vector_store = VectorStoreService()
vec_result = vector_store.add_documents(
    chunks=doc_result['chunks'],
    metadata={"filename": "research_paper.pdf"}
)

# 3. Generate response with LLM
llm_service = LLMService()
response = llm_service.generate_response(
    query="What are the main findings of this paper?",
    vector_store=vector_store
)

# 4. Display results
print(f"Question: {response['query']}")
print(f"\nAnswer:\n{response['answer']}")
print(f"\nSources ({len(response['source_documents'])}):")
for i, src in enumerate(response['source_documents'], 1):
    print(f"{i}. {src['source']}")
```

### Example 2: Multiple Queries

```python
from app.services.llm_service import LLMService
from app.services.vector_store import get_vector_store

llm_service = LLMService()
vector_store = get_vector_store()

queries = [
    "What is the methodology used?",
    "What are the key results?",
    "What are the limitations?",
    "What future work is suggested?"
]

for query in queries:
    print(f"\nQ: {query}")
    print("-" * 70)
    
    response = llm_service.generate_response(query, vector_store)
    print(f"A: {response['answer']}\n")
```

### Example 3: Error Handling

```python
from app.services.llm_service import LLMService
from app.services.vector_store import VectorStoreService

try:
    # Initialize LLM service
    llm_service = LLMService()
    vector_store = VectorStoreService()
    
    # Generate response
    response = llm_service.generate_response(
        query="Explain the algorithm",
        vector_store=vector_store
    )
    
    print(response['answer'])
    
except ConnectionError as e:
    print(f"Ollama Connection Error: {e}")
    print("Please start Ollama: ollama serve")
    
except Exception as e:
    print(f"Error: {e}")
```

---

## Configuration

### Environment Variables

Set in `.env`:

```bash
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

# Retrieval Configuration
TOP_K_RETRIEVAL=5
```

### LLM Parameters

**Temperature:** 0.7 (hardcoded)
- Controls randomness in generation
- 0.0 = deterministic
- 1.0 = more creative
- 0.7 = good balance

**Timeout:** 300 seconds (5 minutes)
- Allows for longer responses
- Prevents hanging on complex queries

**Chain Type:** "stuff"
- Puts all retrieved documents into context
- Simple and effective for most cases
- Alternative: "map_reduce", "refine"

---

## RetrievalQA Chain

The service uses LangChain's `RetrievalQA` chain:

```python
qa_chain = RetrievalQA.from_chain_type(
    llm=self.llm,                      # Ollama LLM
    chain_type="stuff",                # Concatenate all docs
    retriever=retriever,               # From vector store
    return_source_documents=True,      # Include sources
    chain_type_kwargs={
        "prompt": self.prompt_template  # Custom prompt
    }
)
```

**Benefits:**
- Automatic context management
- Source document tracking
- Prompt template integration
- Error handling

---

## Ollama Setup

### Installation

```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai
```

### Start Ollama

```bash
ollama serve
```

### Pull Models

```bash
# Pull llama3.2 (recommended)
ollama pull llama3.2

# Or other models
ollama pull llama2
ollama pull mistral
ollama pull codellama
```

### List Models

```bash
ollama list
```

---

## Performance

### Response Time

- **Simple query:** 2-5 seconds
- **Complex query:** 5-15 seconds
- **Very long context:** 15-30 seconds

Factors affecting speed:
- Model size (llama2:7b vs llama2:13b)
- Number of retrieved documents
- Query complexity
- Hardware (CPU vs GPU)

### Optimization Tips

1. **Use smaller models** for faster responses
   ```bash
   ollama pull llama2:7b  # Faster
   ollama pull llama2:13b # Better quality
   ```

2. **Adjust TOP_K_RETRIEVAL**
   - Fewer docs = faster
   - More docs = better context

3. **GPU Acceleration**
   - Ollama automatically uses GPU if available
   - Significantly faster than CPU

---

## Troubleshooting

### Issue: "Cannot connect to Ollama"

**Cause:** Ollama is not running

**Solution:**
```bash
# Start Ollama
ollama serve

# Verify it's running
curl http://localhost:11434/api/tags
```

### Issue: "Model not found"

**Cause:** Model not pulled

**Solution:**
```bash
ollama pull llama3.2
```

### Issue: "Timeout during generation"

**Cause:** Query too complex or model too slow

**Solution:**
- Use smaller model
- Reduce TOP_K_RETRIEVAL
- Increase timeout in code

### Issue: "Out of memory"

**Cause:** Model too large for available RAM

**Solution:**
- Use quantized model (Q4 or Q5)
- Close other applications
- Use smaller model

---

## Best Practices

1. ✓ **Validate Ollama connection** before starting app
2. ✓ **Pull models in advance** during setup
3. ✓ **Use appropriate models** for your hardware
4. ✓ **Handle ConnectionError** gracefully in production
5. ✓ **Monitor response times** and optimize if needed
6. ✓ **Provide source attribution** to users
7. ✓ **Test with various query types** before deployment

---

## Testing

Run the test suite:

```bash
cd backend

# Make sure Ollama is running
ollama serve

# Pull model
ollama pull llama3.2

# Run tests
python test_llm_service.py
```

Tests include:
- ✓ Ollama connection validation
- ✓ Model availability check
- ✓ RAG pipeline testing
- ✓ Response generation
- ✓ Error handling

---

## API Summary

| Method | Parameters | Returns | Purpose |
|--------|------------|---------|---------|
| `__init__()` | - | - | Initialize with Ollama |
| `generate_response()` | query, vector_store | dict | Generate RAG response |
| `check_connection()` | - | bool | Check Ollama status |
| `get_available_models()` | - | List[str] | List available models |

---

## Integration Points

### With VectorStoreService

```python
# LLMService uses VectorStore's retriever
retriever = vector_store.vectorstore.as_retriever(
    search_kwargs={"k": settings.TOP_K_RETRIEVAL}
)
```

### With DocumentProcessor

```python
# Process → Store → Query
processor = DocumentProcessor()
doc_result = processor.process_document("doc.pdf", "doc.pdf")

vector_store = VectorStoreService()
vector_store.add_documents(doc_result['chunks'], {...})

llm_service = LLMService()
response = llm_service.generate_response("question", vector_store)
```

---

**Version**: 1.0.0  
**LangChain**: 0.1.0  
**Ollama**: Latest  
**Default Model**: llama3.2


