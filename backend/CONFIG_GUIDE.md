# Configuration Guide

## Overview

The ResearchMate RAG application uses a robust configuration system built with **Pydantic BaseSettings**, providing type-safe settings with automatic validation and environment variable support.

## Configuration File

Location: `backend/app/core/config.py`

## Key Features

### ✅ Environment Variable Loading
- Automatically loads from `.env` file
- Environment variables override defaults
- Case-sensitive variable names
- UTF-8 encoding support

### ✅ Type Safety
- All settings are strongly typed
- Runtime type validation
- IDE autocomplete support

### ✅ Field Validation
- Range validation for numeric fields
- URL format validation
- Directory path validation
- File extension normalization
- Custom business logic validation

### ✅ Auto-Directory Creation
- Automatically creates required directories on startup
- No manual setup needed

## Configuration Fields

### Application Settings

```python
DEBUG: bool = False                    # Enable debug mode
HOST: str = "0.0.0.0"                 # Server host
PORT: int = 8000                       # Server port (1-65535)
```

### CORS - Frontend Connection

```python
CORS_ORIGINS: List[str] = [
    "http://localhost:8501",
    "http://localhost:3000"
]
```

**Validation:** All origins must be valid URLs starting with `http://` or `https://`, or `"*"` for wildcard.

### Ollama Configuration

```python
OLLAMA_BASE_URL: str = "http://localhost:11434"
OLLAMA_MODEL: str = "llama3.2"
```

**Validation:** 
- URL must start with `http://` or `https://`
- Trailing slashes are automatically removed

### Embedding Configuration

```python
EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
```

### Vector Store - ChromaDB

```python
CHROMA_PERSIST_DIRECTORY: str = "./chroma_db"
COLLECTION_NAME: str = "researchmate_docs"
```

**Validation:** Directory path cannot be empty

### Document Processing

```python
CHUNK_SIZE: int = 1000              # Range: 100-10000
CHUNK_OVERLAP: int = 200            # Range: 0-1000
TOP_K_RETRIEVAL: int = 5            # Range: 1-20
```

**Validation:** `CHUNK_OVERLAP` must be less than `CHUNK_SIZE`

### File Upload

```python
UPLOAD_DIR: str = "./data/raw"
MAX_UPLOAD_SIZE_MB: int = 10         # Range: 1-100 MB
ALLOWED_EXTENSIONS: List[str] = [".pdf", ".txt", ".md", ".docx"]
```

**Validation:** 
- Extensions automatically normalized to lowercase
- Dot prefix added if missing

### LLM Parameters

```python
LLM_TEMPERATURE: float = 0.7         # Range: 0.0-2.0
LLM_MAX_TOKENS: int = 2000           # Range: 100-8000
LLM_CONTEXT_WINDOW: int = 4096       # Range: 512-32768
```

## Usage Examples

### Basic Usage

```python
from app.core.config import settings

# Access settings
print(settings.OLLAMA_MODEL)          # "llama3.2"
print(settings.CHUNK_SIZE)            # 1000
print(settings.CORS_ORIGINS)          # ["http://localhost:8501", ...]
```

### Environment Variable Override

Create a `.env` file:

```bash
# .env
OLLAMA_MODEL=llama3.1
CHUNK_SIZE=1500
TOP_K_RETRIEVAL=10
MAX_UPLOAD_SIZE_MB=20
```

The settings will automatically use these values instead of defaults.

### Programmatic Override

```python
from app.core.config import Settings

# Create custom settings instance
custom_settings = Settings(
    OLLAMA_MODEL="mistral",
    CHUNK_SIZE=2000,
    DEBUG=True
)
```

## Validation Examples

### ✅ Valid Configuration

```python
Settings(
    OLLAMA_BASE_URL="http://localhost:11434",
    CHUNK_SIZE=1000,
    CHUNK_OVERLAP=200,
    CORS_ORIGINS=["http://localhost:8501"]
)
```

### ❌ Invalid Configurations

```python
# Invalid URL format
Settings(OLLAMA_BASE_URL="invalid-url")
# ValidationError: OLLAMA_BASE_URL must start with http:// or https://

# Chunk overlap >= chunk size
Settings(CHUNK_SIZE=100, CHUNK_OVERLAP=100)
# ValidationError: CHUNK_OVERLAP (100) must be less than CHUNK_SIZE (100)

# Empty CORS origins
Settings(CORS_ORIGINS=[])
# ValidationError: CORS_ORIGINS cannot be empty

# Invalid CORS origin
Settings(CORS_ORIGINS=["not-a-url"])
# ValidationError: Invalid CORS origin: not-a-url

# Port out of range
Settings(PORT=70000)
# ValidationError: PORT must be <= 65535

# Chunk size too small
Settings(CHUNK_SIZE=50)
# ValidationError: CHUNK_SIZE must be >= 100
```

## Custom Validators

### 1. Ollama URL Validator

```python
@field_validator("OLLAMA_BASE_URL")
def validate_ollama_url(cls, v: str) -> str:
    if not v.startswith(("http://", "https://")):
        raise ValueError("OLLAMA_BASE_URL must start with http:// or https://")
    return v.rstrip("/")
```

### 2. Chunk Overlap Validator

```python
@field_validator("CHUNK_OVERLAP")
def validate_chunk_overlap(cls, v: int, info) -> int:
    chunk_size = info.data.get("CHUNK_SIZE", 1000)
    if v >= chunk_size:
        raise ValueError(f"CHUNK_OVERLAP ({v}) must be less than CHUNK_SIZE ({chunk_size})")
    return v
```

### 3. CORS Origins Validator

```python
@field_validator("CORS_ORIGINS")
def validate_cors_origins(cls, v: List[str]) -> List[str]:
    if not v:
        raise ValueError("CORS_ORIGINS cannot be empty")
    for origin in v:
        if origin != "*" and not origin.startswith(("http://", "https://")):
            raise ValueError(f"Invalid CORS origin: {origin}")
    return v
```

### 4. Directory Validator

```python
@field_validator("CHROMA_PERSIST_DIRECTORY", "UPLOAD_DIR")
def validate_directory(cls, v: str) -> str:
    if not v or v.strip() == "":
        raise ValueError("Directory path cannot be empty")
    return v
```

### 5. Extensions Validator

```python
@field_validator("ALLOWED_EXTENSIONS")
def validate_extensions(cls, v: List[str]) -> List[str]:
    validated = []
    for ext in v:
        if not ext.startswith("."):
            ext = f".{ext}"
        validated.append(ext.lower())
    return validated
```

## Testing Configuration

Run the test suite to verify configuration:

```bash
cd backend
python test_config.py
```

This will test:
- ✓ Default settings loading
- ✓ All validation rules
- ✓ Environment variable overrides
- ✓ Automatic directory creation

## Docker Configuration

For Docker deployments, set environment variables in `docker-compose.yml`:

```yaml
services:
  backend:
    environment:
      - OLLAMA_BASE_URL=http://host.docker.internal:11434
      - OLLAMA_MODEL=llama3.2
      - CHROMA_PERSIST_DIRECTORY=/app/chroma_db
      - DEBUG=false
```

## Best Practices

1. **Never commit `.env` files** - Use `.env.example` as template
2. **Use environment variables in production** - Don't hardcode secrets
3. **Validate early** - Settings are validated on application startup
4. **Document changes** - Update `.env.example` when adding new settings
5. **Use type hints** - Leverage IDE autocomplete for settings access
6. **Test validation** - Add tests for custom validators

## Troubleshooting

### Settings not loading from .env

- Ensure `.env` file is in the correct location (project root)
- Check file encoding is UTF-8
- Verify variable names are case-sensitive matches

### Validation errors on startup

- Check all required fields are provided
- Verify field values are within valid ranges
- Review validation error messages for details

### Directory creation fails

- Check write permissions
- Verify parent directories exist
- Review path format (relative vs absolute)

## Migration from Old Config

If updating from a previous version, map old field names to new ones:

| Old Field Name | New Field Name |
|---------------|----------------|
| `ALLOWED_ORIGINS` | `CORS_ORIGINS` |
| `CHROMA_PERSIST_DIR` | `CHROMA_PERSIST_DIRECTORY` |
| `TOP_K_RESULTS` | `TOP_K_RETRIEVAL` |
| `MAX_FILE_SIZE_MB` | `MAX_UPLOAD_SIZE_MB` |
| `OLLAMA_EMBEDDING_MODEL` | `EMBEDDING_MODEL` |

## Further Reading

- [Pydantic Settings Documentation](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [Environment Variables Best Practices](https://12factor.net/config)
- [FastAPI Configuration](https://fastapi.tiangolo.com/advanced/settings/)


