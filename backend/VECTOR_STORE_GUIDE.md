## VectorStoreService - Complete Guide

## Overview

The `VectorStoreService` provides ChromaDB integration with LangChain and HuggingFace embeddings for the ResearchMate RAG application. It implements a singleton pattern to ensure efficient resource usage.

## Location

```python
from app.services.vector_store import VectorStoreService, get_vector_store
```

## Key Technologies

- **ChromaDB** - Persistent vector database
- **LangChain Chroma** - LangChain wrapper for ChromaDB
- **HuggingFace Embeddings** - sentence-transformers/all-MiniLM-L6-v2

## Singleton Pattern

The `VectorStoreService` implements the singleton pattern, ensuring only one instance exists throughout the application lifecycle.

### Why Singleton?

1. **Resource Efficiency** - Embeddings model loaded once
2. **Connection Pooling** - Single ChromaDB connection
3. **Consistency** - All components use the same vector store instance
4. **Memory Savings** - Avoids duplicate model loading

### Usage

```python
# Both create/return the same instance
store1 = VectorStoreService()
store2 = get_vector_store()

assert store1 is store2  # True
```

---

## Class: VectorStoreService

### Initialization

```python
store = VectorStoreService()
```

**What happens on initialization:**

1. ✓ Checks if already initialized (singleton)
2. ✓ Loads HuggingFace embeddings model
3. ✓ Connects to ChromaDB persistent client
4. ✓ Creates or gets "research_papers" collection
5. ✓ Initializes LangChain Chroma wrapper

**Configuration from Settings:**
- `EMBEDDING_MODEL` - HuggingFace model name
- `CHROMA_PERSIST_DIRECTORY` - Storage location
- Collection name: `"research_papers"` (hardcoded)

---

## Methods

### 1. add_documents()

Add text chunks to the vector store with automatic embedding generation.

**Signature:**
```python
def add_documents(self, chunks: List[str], metadata: dict) -> dict
```

**Parameters:**
- `chunks` (List[str]): List of text chunks to add
- `metadata` (dict): Base metadata applied to all chunks

**Returns:**
```python
{
    "status": "success",
    "documents_added": int,
    "collection": str,
    "embedding_model": str
}
```

**Features:**
- ✓ Automatic embedding generation (HuggingFace)
- ✓ Automatic chunk_id generation
- ✓ Timestamp added to each chunk
- ✓ Metadata enrichment (chunk_index, total_chunks)

**Example:**
```python
store = VectorStoreService()

chunks = [
    "First paragraph of text...",
    "Second paragraph of text...",
    "Third paragraph of text..."
]

metadata = {
    "filename": "document.pdf",
    "author": "John Doe"
}

result = store.add_documents(chunks=chunks, metadata=metadata)

print(f"Added {result['documents_added']} documents")
# Output: Added 3 documents
```

**Metadata Structure:**

Each chunk gets the following metadata:
```python
{
    # From your base metadata
    "filename": "document.pdf",
    "author": "John Doe",
    
    # Automatically added
    "chunk_id": "uuid-generated",
    "chunk_index": 0,
    "total_chunks": 3,
    "timestamp": "2024-01-01T12:00:00.000000"
}
```

---

### 2. similarity_search()

Find the most relevant documents for a query.

**Signature:**
```python
def similarity_search(self, query: str, k: int = None) -> List[dict]
```

**Parameters:**
- `query` (str): Search query
- `k` (int, optional): Number of results (defaults to `settings.TOP_K_RETRIEVAL`)

**Returns:**
```python
[
    {
        "content": str,      # Document text
        "metadata": dict,    # Document metadata
        "score": float,      # Similarity score (0-1)
        "id": str            # chunk_id
    },
    ...
]
```

**Features:**
- ✓ Automatic query embedding generation
- ✓ Cosine similarity search
- ✓ Results sorted by relevance
- ✓ Score normalization (0-1 range)

**Example:**
```python
store = VectorStoreService()

# Search with default k
results = store.similarity_search("What is machine learning?")

# Search with custom k
results = store.similarity_search("What is AI?", k=10)

for doc in results:
    print(f"Score: {doc['score']:.4f}")
    print(f"Content: {doc['content'][:100]}...")
    print(f"Source: {doc['metadata']['filename']}")
    print()
```

**Score Interpretation:**
- `1.0` - Perfect match
- `0.8-1.0` - Very relevant
- `0.6-0.8` - Relevant
- `0.4-0.6` - Somewhat relevant
- `< 0.4` - Less relevant

---

### 3. delete_collection()

Clear all documents from the collection.

**Signature:**
```python
def delete_collection(self) -> dict
```

**Returns:**
```python
{
    "status": "success",
    "message": str,
    "collection": str
}
```

**Features:**
- ✓ Deletes entire collection
- ✓ Recreates empty collection
- ✓ Reinitializes vectorstore
- ✓ Useful for testing and reset

**Example:**
```python
store = VectorStoreService()

# Delete all documents
result = store.delete_collection()

print(result['message'])
# Output: Collection 'research_papers' cleared successfully
```

**Use Cases:**
- Testing - Start with clean slate
- Reset - Clear all data
- Development - Quick cleanup

⚠️ **Warning:** This deletes ALL documents permanently!

---

## Additional Utility Methods

### 4. delete_documents()

Delete specific documents by IDs.

```python
def delete_documents(self, ids: List[str]) -> dict
```

### 5. delete_by_source()

Delete all documents from a specific filename.

```python
def delete_by_source(self, source: str) -> dict
```

### 6. get_status()

Get health and statistics of the vector store.

```python
def get_status(self) -> Dict[str, Any]
```

**Returns:**
```python
{
    "healthy": True,
    "document_count": 42,
    "collection_name": "research_papers",
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "persist_directory": "./chroma_db"
}
```

### 7. get_collection_info()

Get detailed collection information.

```python
def get_collection_info(self) -> dict
```

**Returns:**
```python
{
    "collection_name": "research_papers",
    "document_count": 42,
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "embedding_dimension": 384,
    "persist_directory": "./chroma_db",
    "distance_metric": "cosine"
}
```

---

## Complete Usage Examples

### Example 1: Basic Document Workflow

```python
from app.services.vector_store import VectorStoreService

# Initialize
store = VectorStoreService()

# Add documents
chunks = [
    "Python is a programming language.",
    "JavaScript is used for web development.",
    "SQL is for database queries."
]

metadata = {"filename": "programming.txt", "category": "tech"}
result = store.add_documents(chunks=chunks, metadata=metadata)

print(f"✓ Added {result['documents_added']} documents")

# Search
results = store.similarity_search("What is Python?", k=2)

for doc in results:
    print(f"\nScore: {doc['score']:.4f}")
    print(f"Content: {doc['content']}")
    print(f"From: {doc['metadata']['filename']}")
```

### Example 2: Integration with DocumentProcessor

```python
from app.services.document_service import DocumentProcessor
from app.services.vector_store import get_vector_store

# Process PDF
processor = DocumentProcessor()
doc_result = processor.process_document(
    file_path="research_paper.pdf",
    filename="research_paper.pdf"
)

# Add to vector store
store = get_vector_store()
vec_result = store.add_documents(
    chunks=doc_result['chunks'],
    metadata={
        "filename": doc_result['filename'],
        "processed_at": doc_result['timestamp']
    }
)

print(f"✓ Processed {doc_result['total_chunks']} chunks")
print(f"✓ Added {vec_result['documents_added']} to vector store")

# Query the document
results = store.similarity_search("What is the main conclusion?")
print(f"\nMost relevant passage:")
print(results[0]['content'])
```

### Example 3: Batch Processing Multiple Documents

```python
from app.services.vector_store import VectorStoreService
from app.services.document_service import DocumentProcessor
import os

store = VectorStoreService()
processor = DocumentProcessor()

pdf_dir = "documents/"
processed_count = 0

for filename in os.listdir(pdf_dir):
    if filename.endswith(".pdf"):
        file_path = os.path.join(pdf_dir, filename)
        
        # Process document
        doc_result = processor.process_document(file_path, filename)
        
        # Add to vector store
        vec_result = store.add_documents(
            chunks=doc_result['chunks'],
            metadata={"filename": filename}
        )
        
        processed_count += vec_result['documents_added']
        print(f"✓ {filename}: {vec_result['documents_added']} chunks")

print(f"\n✓ Total: {processed_count} chunks indexed")

# Get status
status = store.get_status()
print(f"Vector store now has {status['document_count']} total documents")
```

### Example 4: Advanced Search with Filtering

```python
store = VectorStoreService()

# Search with metadata filtering (future enhancement)
query = "machine learning algorithms"
results = store.similarity_search(query, k=10)

# Filter results by score threshold
high_quality_results = [
    doc for doc in results 
    if doc['score'] > 0.7
]

print(f"Found {len(high_quality_results)} high-quality matches:")
for doc in high_quality_results:
    print(f"\n{doc['score']:.4f} - {doc['metadata']['filename']}")
    print(f"{doc['content'][:200]}...")
```

---

## Configuration

### Environment Variables

Set in `.env`:

```bash
# Embedding model (HuggingFace)
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# ChromaDB storage
CHROMA_PERSIST_DIRECTORY=./chroma_db

# Search parameters
TOP_K_RETRIEVAL=5
```

### Collection Settings

- **Name:** `research_papers` (hardcoded)
- **Distance Metric:** Cosine similarity
- **Persistence:** Enabled (stored in `CHROMA_PERSIST_DIRECTORY`)

---

## Performance

### Embedding Model

- **Model:** sentence-transformers/all-MiniLM-L6-v2
- **Dimensions:** 384
- **Speed:** ~1000 sentences/second on CPU
- **Size:** ~80MB

### First Load Time

- **Cold start:** 2-5 seconds (model download + load)
- **Warm start:** <1 second (model cached)

### Operations

- **Add 100 chunks:** ~2-5 seconds
- **Search query:** <100ms
- **Get status:** <10ms

---

## Troubleshooting

### Issue: "Model download slow"

**Cause:** First-time model download

**Solution:** 
```bash
# Pre-download model
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"
```

### Issue: "ChromaDB locked"

**Cause:** Multiple processes accessing same directory

**Solution:** Ensure only one instance or use different directories

### Issue: "Out of memory"

**Cause:** Too many documents or large batches

**Solution:** Add documents in smaller batches

```python
# Instead of all at once
chunks = [...] # 10000 chunks

# Process in batches
batch_size = 100
for i in range(0, len(chunks), batch_size):
    batch = chunks[i:i+batch_size]
    store.add_documents(batch, metadata)
```

---

## Best Practices

1. ✓ Use singleton pattern (via `get_vector_store()`)
2. ✓ Add documents in reasonable batches (<1000 at a time)
3. ✓ Include meaningful metadata
4. ✓ Use appropriate `k` values (3-10 for most cases)
5. ✓ Monitor collection size with `get_status()`
6. ✓ Clean up test data with `delete_collection()`
7. ✓ Persist directory on reliable storage

---

## Testing

Run the test suite:

```bash
cd backend
python test_vector_store.py
```

This tests:
- ✓ Singleton pattern
- ✓ Initialization
- ✓ Adding documents
- ✓ Similarity search
- ✓ Status and info
- ✓ Collection deletion

---

## API Summary

| Method | Parameters | Returns | Purpose |
|--------|------------|---------|---------|
| `add_documents()` | chunks, metadata | dict | Add documents |
| `similarity_search()` | query, k | List[dict] | Search documents |
| `delete_collection()` | - | dict | Clear all documents |
| `delete_documents()` | ids | dict | Delete specific documents |
| `delete_by_source()` | source | dict | Delete by filename |
| `get_status()` | - | dict | Get health status |
| `get_collection_info()` | - | dict | Get collection details |

---

**Version**: 1.0.0  
**Embedding Model**: sentence-transformers/all-MiniLM-L6-v2  
**Vector DB**: ChromaDB 0.4.18  
**LangChain**: 0.1.0


