"""
Configuration Settings
"""
import os
from typing import List
from pydantic import Field, field_validator, ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings with environment variable support
    
    All settings can be overridden via environment variables or .env file
    """
    
    # Application
    PROJECT_NAME: str = "ResearchMate RAG API"
    VERSION: str = "0.1.0"
    DEBUG: bool = Field(
        default=False,
        description="Enable debug mode"
    )
    HOST: str = Field(
        default="0.0.0.0",
        description="Host to bind the server"
    )
    PORT: int = Field(
        default=8000,
        ge=1,
        le=65535,
        description="Port to bind the server"
    )
    
    # CORS - Frontend Connection
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:8501", "http://localhost:3000"],
        description="Allowed CORS origins for frontend connection"
    )
    
    # Ollama Configuration
    OLLAMA_BASE_URL: str = Field(
        default="http://localhost:11434",
        description="Base URL for Ollama API"
    )
    OLLAMA_MODEL: str = Field(
        default="llama2",
        description="Ollama model to use for text generation"
    )
    
    # Embedding Configuration
    EMBEDDING_MODEL: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        description="Embedding model for document vectorization"
    )
    
    # Vector Store - ChromaDB
    CHROMA_PERSIST_DIRECTORY: str = Field(
        default="./chroma_db",
        description="Directory to persist ChromaDB data"
    )
    COLLECTION_NAME: str = Field(
        default="researchmate_docs",
        description="ChromaDB collection name"
    )
    
    # Document Processing
    CHUNK_SIZE: int = Field(
        default=1000,
        ge=100,
        le=10000,
        description="Size of text chunks for processing"
    )
    CHUNK_OVERLAP: int = Field(
        default=200,
        ge=0,
        le=1000,
        description="Overlap between consecutive chunks"
    )
    TOP_K_RETRIEVAL: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of top documents to retrieve"
    )
    
    # File Upload
    UPLOAD_DIR: str = Field(
        default="./data/raw",
        description="Directory for uploaded files"
    )
    MAX_UPLOAD_SIZE_MB: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Maximum upload file size in MB"
    )
    ALLOWED_EXTENSIONS: List[str] = Field(
        default=[".pdf", ".txt", ".md", ".docx"],
        description="Allowed file extensions for upload"
    )
    
    # LLM Parameters
    LLM_TEMPERATURE: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Temperature for LLM generation (0.0-2.0)"
    )
    LLM_MAX_TOKENS: int = Field(
        default=2000,
        ge=100,
        le=8000,
        description="Maximum tokens to generate"
    )
    LLM_CONTEXT_WINDOW: int = Field(
        default=4096,
        ge=512,
        le=32768,
        description="LLM context window size"
    )
    
    # Pydantic v2 Configuration
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    
    # Validators
    @field_validator("OLLAMA_BASE_URL")
    @classmethod
    def validate_ollama_url(cls, v: str) -> str:
        """Validate Ollama base URL format"""
        if not v.startswith(("http://", "https://")):
            raise ValueError("OLLAMA_BASE_URL must start with http:// or https://")
        return v.rstrip("/")
    
    @field_validator("CHUNK_OVERLAP")
    @classmethod
    def validate_chunk_overlap(cls, v: int, info) -> int:
        """Ensure chunk overlap is less than chunk size"""
        chunk_size = info.data.get("CHUNK_SIZE", 1000)
        if v >= chunk_size:
            raise ValueError(f"CHUNK_OVERLAP ({v}) must be less than CHUNK_SIZE ({chunk_size})")
        return v
    
    @field_validator("CORS_ORIGINS")
    @classmethod
    def validate_cors_origins(cls, v: List[str]) -> List[str]:
        """Validate CORS origins are valid URLs or wildcards"""
        if not v:
            raise ValueError("CORS_ORIGINS cannot be empty")
        for origin in v:
            if origin != "*" and not origin.startswith(("http://", "https://")):
                raise ValueError(f"Invalid CORS origin: {origin}. Must start with http:// or https://")
        return v
    
    @field_validator("CHROMA_PERSIST_DIRECTORY", "UPLOAD_DIR")
    @classmethod
    def validate_directory(cls, v: str) -> str:
        """Ensure directory paths are valid"""
        if not v or v.strip() == "":
            raise ValueError("Directory path cannot be empty")
        return v
    
    @field_validator("ALLOWED_EXTENSIONS")
    @classmethod
    def validate_extensions(cls, v: List[str]) -> List[str]:
        """Ensure all extensions start with a dot"""
        validated = []
        for ext in v:
            if not ext.startswith("."):
                ext = f".{ext}"
            validated.append(ext.lower())
        return validated
    
    def create_directories(self) -> None:
        """Create necessary directories if they don't exist"""
        directories = [
            self.CHROMA_PERSIST_DIRECTORY,
            self.UPLOAD_DIR
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)


# Initialize settings instance
settings = Settings()

# Create necessary directories on startup
settings.create_directories()

