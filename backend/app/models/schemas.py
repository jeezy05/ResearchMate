"""
Pydantic Models and Schemas for ResearchMate RAG API
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator
from datetime import datetime


# ============================================================================
# REQUEST/RESPONSE SCHEMAS
# ============================================================================

class UploadResponse(BaseModel):
    """Upload response schema"""
    filename: str = Field(..., description="Name of the uploaded file")
    total_chunks: int = Field(..., ge=0, description="Number of text chunks created")
    message: str = Field(..., description="Status message")
    status: str = Field(..., description="Upload status (success/error)")
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate status field"""
        allowed_statuses = ['success', 'error', 'processing']
        if v.lower() not in allowed_statuses:
            raise ValueError(f"Status must be one of: {allowed_statuses}")
        return v.lower()


class QueryRequest(BaseModel):
    """Query request schema"""
    question: str = Field(..., min_length=1, max_length=2000, description="The question to ask")
    max_results: Optional[int] = Field(default=5, ge=1, le=10, description="Maximum number of results to return")
    
    @field_validator('question')
    @classmethod
    def validate_question(cls, v: str) -> str:
        """Validate question is not empty and properly formatted"""
        if not v or not v.strip():
            raise ValueError("Question cannot be empty")
        return v.strip()


class QueryResponse(BaseModel):
    """Query response schema"""
    question: str = Field(..., description="The original question")
    answer: str = Field(..., description="The generated answer")
    sources: List[Dict[str, Any]] = Field(..., description="List of source documents with content and metadata")
    processing_time: float = Field(..., ge=0, description="Processing time in seconds")
    
    @field_validator('sources')
    @classmethod
    def validate_sources(cls, v: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validate sources contain required fields"""
        for source in v:
            if not isinstance(source, dict):
                raise ValueError("Each source must be a dictionary")
            if 'content' not in source:
                raise ValueError("Each source must have 'content' field")
            if 'metadata' not in source:
                raise ValueError("Each source must have 'metadata' field")
        return v


class HealthResponse(BaseModel):
    """Health check response schema"""
    status: str = Field(..., description="Overall system status")
    ollama_connected: bool = Field(..., description="Whether Ollama is connected")
    vector_store_ready: bool = Field(..., description="Whether vector store is ready")
    model: str = Field(..., description="Current LLM model name")
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate status field"""
        allowed_statuses = ['healthy', 'unhealthy', 'degraded']
        if v.lower() not in allowed_statuses:
            raise ValueError(f"Status must be one of: {allowed_statuses}")
        return v.lower()


# ============================================================================
# ADDITIONAL SCHEMAS
# ============================================================================

class DocumentBase(BaseModel):
    """Base document schema"""
    filename: str = Field(..., description="Name of the document")
    content_type: str = Field(..., description="MIME type of the document")
    size: int = Field(..., ge=0, description="Size of the document in bytes")


class DocumentCreate(DocumentBase):
    """Document creation schema"""
    pass


class Document(DocumentBase):
    """Document response schema"""
    id: str = Field(..., description="Unique document identifier")
    upload_date: datetime = Field(..., description="When the document was uploaded")
    processed: bool = Field(default=False, description="Whether the document has been processed")
    chunk_count: Optional[int] = Field(default=None, ge=0, description="Number of chunks created from the document")
    
    class Config:
        from_attributes = True


class SourceDocument(BaseModel):
    """Source document metadata"""
    filename: str = Field(..., description="Name of the source document")
    page: Optional[int] = Field(default=None, ge=1, description="Page number if applicable")
    chunk_id: str = Field(..., description="Unique identifier for the text chunk")
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="Relevance score (0-1)")
    content_preview: str = Field(..., max_length=500, description="Preview of the content")


class ErrorResponse(BaseModel):
    """Error response schema"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(default=None, description="Detailed error information")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the error occurred")


class ConversationMessage(BaseModel):
    """Conversation message schema"""
    role: str = Field(..., description="Role of the message sender (user/assistant)")
    content: str = Field(..., description="Content of the message")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the message was sent")
    
    @field_validator('role')
    @classmethod
    def validate_role(cls, v: str) -> str:
        """Validate role field"""
        allowed_roles = ['user', 'assistant', 'system']
        if v.lower() not in allowed_roles:
            raise ValueError(f"Role must be one of: {allowed_roles}")
        return v.lower()


class ConversationHistory(BaseModel):
    """Conversation history schema"""
    conversation_id: str = Field(..., description="Unique conversation identifier")
    messages: List[ConversationMessage] = Field(..., description="List of messages in the conversation")
    created_at: datetime = Field(..., description="When the conversation was created")
    updated_at: datetime = Field(..., description="When the conversation was last updated")


# ============================================================================
# LEGACY SCHEMAS (for backward compatibility)
# ============================================================================

class HealthCheck(BaseModel):
    """Legacy health check response (deprecated - use HealthResponse)"""
    status: str
    ollama_connected: bool
    vector_store_status: str
    documents_indexed: int


