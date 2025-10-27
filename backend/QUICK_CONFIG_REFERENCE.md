# Quick Configuration Reference

## Settings Class Location
```python
from app.core.config import settings
```

## All Configuration Fields

### 🔧 Ollama Settings
```python
OLLAMA_BASE_URL: str = "http://localhost:11434"  # ✓ URL validation
OLLAMA_MODEL: str = "llama3.2"
```

### 🧠 Embedding Settings
```python
EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
```

### 💾 Vector Store Settings
```python
CHROMA_PERSIST_DIRECTORY: str = "./chroma_db"    # ✓ Auto-created
COLLECTION_NAME: str = "researchmate_docs"
```

### 📄 Document Processing
```python
CHUNK_SIZE: int = 1000          # Range: 100-10000
CHUNK_OVERLAP: int = 200        # Range: 0-1000, must be < CHUNK_SIZE
TOP_K_RETRIEVAL: int = 5        # Range: 1-20
```

### 📤 File Upload
```python
UPLOAD_DIR: str = "./data/raw"           # ✓ Auto-created
MAX_UPLOAD_SIZE_MB: int = 10             # Range: 1-100
ALLOWED_EXTENSIONS: List[str] = [".pdf", ".txt", ".md", ".docx"]
```

### 🌐 CORS Settings
```python
CORS_ORIGINS: List[str] = [
    "http://localhost:8501",
    "http://localhost:3000"
]  # ✓ URL validation
```

### 🤖 LLM Parameters
```python
LLM_TEMPERATURE: float = 0.7     # Range: 0.0-2.0
LLM_MAX_TOKENS: int = 2000       # Range: 100-8000
LLM_CONTEXT_WINDOW: int = 4096   # Range: 512-32768
```

### 🖥️ Application Settings
```python
DEBUG: bool = False
HOST: str = "0.0.0.0"
PORT: int = 8000                 # Range: 1-65535
PROJECT_NAME: str = "ResearchMate RAG API"
VERSION: str = "0.1.0"
```

## Validators Summary

| Field | Validation Rule |
|-------|----------------|
| `OLLAMA_BASE_URL` | Must start with http:// or https:// |
| `CHUNK_OVERLAP` | Must be < CHUNK_SIZE |
| `CORS_ORIGINS` | Cannot be empty, must be valid URLs |
| `CHROMA_PERSIST_DIRECTORY` | Cannot be empty |
| `UPLOAD_DIR` | Cannot be empty |
| `ALLOWED_EXTENSIONS` | Auto-normalized (lowercase, dot prefix) |
| `PORT` | Range: 1-65535 |
| All numeric fields | Specific min/max ranges enforced |

## Environment Variable Override

Create `.env` file in project root:

```bash
# Minimal .env example
OLLAMA_MODEL=llama3.2
CHUNK_SIZE=1500
TOP_K_RETRIEVAL=10
MAX_UPLOAD_SIZE_MB=20
```

## Quick Test

```bash
cd backend
python test_config.py
```

## Access in Code

```python
from app.core.config import settings

# Type-safe access
model = settings.OLLAMA_MODEL        # str
chunk_size = settings.CHUNK_SIZE     # int
origins = settings.CORS_ORIGINS      # List[str]
```

## Common Issues & Fixes

| Error | Fix |
|-------|-----|
| `OLLAMA_BASE_URL must start with http://` | Use full URL: `http://localhost:11434` |
| `CHUNK_OVERLAP must be less than CHUNK_SIZE` | Decrease overlap or increase size |
| `CORS_ORIGINS cannot be empty` | Add at least one origin |
| `PORT must be <= 65535` | Use valid port (1-65535) |

---
**Legend**: ✓ = Automatic feature (validation, creation, normalization)


