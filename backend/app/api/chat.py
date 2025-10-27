"""
Chat API Endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import QueryRequest, QueryResponse, ErrorResponse
from app.services.rag_service import RAGService
from app.core.config import settings
import time
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


def get_rag_service():
    """Dependency to get RAG service instance"""
    return RAGService()


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
        
        logger.info(f"Processing query: {request.question[:50]}...")
        
        # Process query through RAG pipeline
        result = await rag_service.query(
            question=request.question,
            conversation_id=request.conversation_id,
            max_results=request.max_results or settings.TOP_K_RETRIEVAL,
            temperature=request.temperature or settings.LLM_TEMPERATURE
        )
        
        processing_time = time.time() - start_time
        
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"],
            conversation_id=result["conversation_id"],
            processing_time=processing_time,
            model_used=settings.OLLAMA_MODEL
        )
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )


@router.get("/conversations/{conversation_id}")
async def get_conversation_history(
    conversation_id: str,
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    Get conversation history by ID
    
    Args:
        conversation_id: Unique conversation identifier
        
    Returns:
        Conversation history
    """
    try:
        history = await rag_service.get_conversation_history(conversation_id)
        if not history:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found"
            )
        return history
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving conversation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving conversation: {str(e)}"
        )

