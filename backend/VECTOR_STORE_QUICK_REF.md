# VectorStoreService - Quick Reference

## Import

```python
from app.services.vector_store import VectorStoreService, get_vector_store
```

## Initialization (Singleton)

```python
# Both return the SAME instance
store = VectorStoreService()
store = get_vector_store()
```

## Core Methods

### Add Documents
```python
result = store.add_documents(
    chunks=["text1", "text2", "text3"],
    metadata={"filename": "doc.pdf"}
)
# Returns: {"status": "success", "documents_added": 3, ...}
```

### Search
```python
results = store.similarity_search(
    query="What is AI?",
    k=5  # optional, defaults to settings.TOP_K_RETRIEVAL
)
# Returns: [{"content": "...", "metadata": {...}, "score": 0.85, "id": "uuid"}, ...]
```

### Delete Collection
```python
result = store.delete_collection()
# Returns: {"status": "success", "message": "...", "collection": "research_papers"}
```

## Utility Methods

```python
# Status
status = store.get_status()
# {"healthy": True, "document_count": 42, ...}

# Collection Info
info = store.get_collection_info()
# {"collection_name": "...", "embedding_model": "...", ...}

# Delete by IDs
store.delete_documents(["id1", "id2"])

# Delete by filename
store.delete_by_source("document.pdf")
```

## Configuration

```python
# Set in .env or settings
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHROMA_PERSIST_DIRECTORY=./chroma_db
TOP_K_RETRIEVAL=5
```

## Complete Workflow

```python
from app.services.vector_store import get_vector_store
from app.services.document_service import DocumentProcessor

# 1. Get singleton instance
store = get_vector_store()

# 2. Process document
processor = DocumentProcessor()
doc_result = processor.process_document("paper.pdf", "paper.pdf")

# 3. Add to vector store
vec_result = store.add_documents(
    chunks=doc_result['chunks'],
    metadata={"filename": "paper.pdf"}
)

# 4. Search
results = store.similarity_search("What is the conclusion?")

# 5. Display results
for doc in results:
    print(f"Score: {doc['score']:.4f}")
    print(f"Content: {doc['content'][:100]}...")
```

## Testing

```bash
cd backend
python test_vector_store.py
```

## Key Features

- ✅ Singleton pattern (one instance)
- ✅ HuggingFace embeddings (local)
- ✅ ChromaDB persistence
- ✅ LangChain integration
- ✅ Automatic metadata enrichment
- ✅ Collection: "research_papers"

## Metadata Structure

```python
# You provide:
{"filename": "doc.pdf", "author": "John"}

# Automatically enriched to:
{
    "filename": "doc.pdf",
    "author": "John",
    "chunk_id": "uuid-generated",
    "chunk_index": 0,
    "total_chunks": 10,
    "timestamp": "2024-01-01T12:00:00"
}
```

## Return Values

### add_documents()
```python
{
    "status": "success",
    "documents_added": 10,
    "collection": "research_papers",
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2"
}
```

### similarity_search()
```python
[
    {
        "content": "Document text content...",
        "metadata": {"filename": "...", "chunk_id": "...", ...},
        "score": 0.8542,  # 0-1, higher is better
        "id": "uuid"
    },
    ...
]
```

### delete_collection()
```python
{
    "status": "success",
    "message": "Collection 'research_papers' cleared successfully",
    "collection": "research_papers"
}
```

## Error Handling

```python
try:
    result = store.add_documents(chunks, metadata)
except Exception as e:
    print(f"Error: {e}")
```

---

**Docs**: See `VECTOR_STORE_GUIDE.md` for complete documentation

