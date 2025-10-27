"""
Health Check API Endpoints
"""
from fastapi import APIRouter, Depends
from app.models.schemas import HealthCheck
from app.services.llm_service import LLMService
from app.services.vector_store import VectorStoreService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=HealthCheck)
async def health_check():
    """
    Comprehensive health check for all services
    
    Returns:
        Health status of all components
    """
    try:
        # Check Ollama connection
        llm_service = LLMService()
        ollama_status = await llm_service.check_connection()
        
        # Check Vector Store
        vector_store = VectorStoreService()
        vector_status = vector_store.get_status()
        
        return HealthCheck(
            status="healthy" if ollama_status and vector_status["healthy"] else "degraded",
            ollama_connected=ollama_status,
            vector_store_status="connected" if vector_status["healthy"] else "disconnected",
            documents_indexed=vector_status.get("document_count", 0)
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return HealthCheck(
            status="unhealthy",
            ollama_connected=False,
            vector_store_status="error",
            documents_indexed=0
        )


