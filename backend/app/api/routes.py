"""
FastAPI Routes - Consolidated API Endpoints
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List
import time
import os
import logging

# Import services
from app.services.document_service import DocumentService
from app.services.vector_store import VectorStoreService
from app.services.llm_service import LLMService
from app.services.rag_service import RAGService

# Import schemas
from app.models.schemas import (
    UploadResponse, QueryRequest, QueryResponse, HealthResponse,
    ErrorResponse
)

# Import config
from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


# ============================================================================
# DEPENDENCY INJECTION
# ============================================================================

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


# ============================================================================
# UPLOAD ENDPOINT
# ============================================================================

@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    document_service: DocumentService = Depends(get_document_service)
):
    """
    Upload and process a PDF document
    
    Args:
        file: The uploaded PDF file
        
    Returns:
        UploadResponse with processing results
    """
    try:
        # Validate file type (must be PDF)
        if not file.filename or not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed"
            )
        
        # Read file content
        contents = await file.read()
        
        # Validate file size
        file_size_mb = len(contents) / (1024 * 1024)
        if file_size_mb > settings.MAX_UPLOAD_SIZE_MB:
            raise HTTPException(
                status_code=400,
                detail=f"File size {file_size_mb:.2f}MB exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE_MB}MB"
            )
        
        # Ensure upload directory exists
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        
        # Process document
        logger.info(f"Processing document: {file.filename}")
        result = await document_service.process_document(
            filename=file.filename,
            content=contents
        )
        
        return UploadResponse(
            filename=file.filename,
            total_chunks=result.get("chunks_created", 0),
            message="Document uploaded and processed successfully",
            status="success"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing document: {str(e)}"
        )


# ============================================================================
# QUERY ENDPOINT
# ============================================================================

@router.post("/query", response_model=QueryResponse)
async def query_documents(
    request: QueryRequest,
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    Query documents using RAG
    
    Args:
        request: Query request with question and parameters
        
    Returns:
        QueryResponse with answer and sources
    """
    try:
        start_time = time.time()
        
        # Validate question is not empty (additional validation)
        if not request.question or not request.question.strip():
            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty"
            )
        
        logger.info(f"Processing query: {request.question[:50]}...")
        
        # Process query through RAG pipeline
        result = await rag_service.query(
            question=request.question,
            max_results=request.max_results or settings.TOP_K_RETRIEVAL
        )
        
        processing_time = time.time() - start_time
        
        return QueryResponse(
            question=request.question,
            answer=result["answer"],
            sources=result["sources"],
            processing_time=processing_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )


# ============================================================================
# HEALTH ENDPOINT
# ============================================================================

@router.get("/health", response_model=HealthResponse)
async def health_check(
    llm_service: LLMService = Depends(get_llm_service),
    vector_store: VectorStoreService = Depends(get_vector_store_service)
):
    """
    Comprehensive health check for all services
    
    Returns:
        HealthResponse with all service statuses
    """
    try:
        # Check Ollama connection (try a simple ping)
        ollama_connected = False
        model_name = "unknown"
        
        try:
            ollama_connected = llm_service.check_connection()
            model_name = settings.OLLAMA_MODEL
        except Exception as e:
            logger.warning(f"Ollama connection check failed: {str(e)}")
        
        # Check vector store status
        vector_store_ready = False
        try:
            vector_status = vector_store.get_status()
            vector_store_ready = vector_status.get("healthy", False)
        except Exception as e:
            logger.warning(f"Vector store check failed: {str(e)}")
        
        # Determine overall status
        if ollama_connected and vector_store_ready:
            status = "healthy"
        elif ollama_connected or vector_store_ready:
            status = "degraded"
        else:
            status = "unhealthy"
        
        return HealthResponse(
            status=status,
            ollama_connected=ollama_connected,
            vector_store_ready=vector_store_ready,
            model=model_name
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return HealthResponse(
            status="unhealthy",
            ollama_connected=False,
            vector_store_ready=False,
            model="unknown"
        )


# ============================================================================
# RESET ENDPOINT
# ============================================================================

@router.delete("/reset")
async def reset_system(
    vector_store: VectorStoreService = Depends(get_vector_store_service)
):
    """
    Reset the system by clearing vector store and uploaded files
    
    Returns:
        Success message
    """
    try:
        # Clear vector store collection
        logger.info("Clearing vector store collection...")
        vector_store.delete_collection()
        
        # Delete files from /data/raw
        logger.info("Clearing uploaded files...")
        if os.path.exists(settings.UPLOAD_DIR):
            for filename in os.listdir(settings.UPLOAD_DIR):
                file_path = os.path.join(settings.UPLOAD_DIR, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    logger.info(f"Deleted file: {filename}")
        
        return {
            "message": "System reset successfully",
            "details": {
                "vector_store_cleared": True,
                "files_deleted": True,
                "upload_directory": settings.UPLOAD_DIR
            }
        }
        
    except Exception as e:
        logger.error(f"Error resetting system: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error resetting system: {str(e)}"
        )


# ============================================================================
# ADDITIONAL UTILITY ENDPOINTS
# ============================================================================

@router.get("/status")
async def get_system_status(
    vector_store: VectorStoreService = Depends(get_vector_store_service)
):
    """
    Get detailed system status
    
    Returns:
        Detailed system status information
    """
    try:
        # Get vector store info
        vector_info = vector_store.get_collection_info()
        
        # Count uploaded files
        file_count = 0
        if os.path.exists(settings.UPLOAD_DIR):
            file_count = len([f for f in os.listdir(settings.UPLOAD_DIR) 
                            if os.path.isfile(os.path.join(settings.UPLOAD_DIR, f))])
        
        return {
            "vector_store": vector_info,
            "upload_directory": settings.UPLOAD_DIR,
            "uploaded_files_count": file_count,
            "max_upload_size_mb": settings.MAX_UPLOAD_SIZE_MB,
            "allowed_extensions": settings.ALLOWED_EXTENSIONS
        }
        
    except Exception as e:
        logger.error(f"Error getting system status: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting system status: {str(e)}"
        )


@router.get("/models")
async def get_available_models(
    llm_service: LLMService = Depends(get_llm_service)
):
    """
    Get available Ollama models
    
    Returns:
        List of available models
    """
    try:
        models = llm_service.get_available_models()
        return {
            "available_models": models,
            "current_model": settings.OLLAMA_MODEL
        }
        
    except Exception as e:
        logger.error(f"Error getting available models: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting available models: {str(e)}"
        )
