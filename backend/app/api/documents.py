"""
Document Management API Endpoints
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List
from app.models.schemas import UploadResponse, Document, ErrorResponse
from app.services.document_service import DocumentService
from app.core.config import settings
import logging
import os

logger = logging.getLogger(__name__)
router = APIRouter()


def get_document_service():
    """Dependency to get document service instance"""
    return DocumentService()


@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    document_service: DocumentService = Depends(get_document_service)
):
    """
    Upload and process a document
    
    Args:
        file: The uploaded file
        
    Returns:
        UploadResponse with document details
    """
    try:
        # Validate file extension
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File type {file_ext} not allowed. Allowed types: {settings.ALLOWED_EXTENSIONS}"
            )
        
        # Validate file size
        contents = await file.read()
        file_size_mb = len(contents) / (1024 * 1024)
        
        if file_size_mb > settings.MAX_UPLOAD_SIZE_MB:
            raise HTTPException(
                status_code=400,
                detail=f"File size {file_size_mb:.2f}MB exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE_MB}MB"
            )
        
        # Process document
        logger.info(f"Processing document: {file.filename}")
        result = await document_service.process_document(
            filename=file.filename,
            content=contents
        )
        
        return UploadResponse(
            message="Document uploaded and processed successfully",
            document_id=result["document_id"],
            filename=file.filename,
            size=len(contents),
            chunks_created=result["chunks_created"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing document: {str(e)}"
        )


@router.get("/", response_model=List[Document])
async def list_documents(
    document_service: DocumentService = Depends(get_document_service)
):
    """
    List all uploaded documents
    
    Returns:
        List of documents
    """
    try:
        documents = await document_service.list_documents()
        return documents
        
    except Exception as e:
        logger.error(f"Error listing documents: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error listing documents: {str(e)}"
        )


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    document_service: DocumentService = Depends(get_document_service)
):
    """
    Delete a document and its embeddings
    
    Args:
        document_id: Document ID to delete
        
    Returns:
        Success message
    """
    try:
        await document_service.delete_document(document_id)
        return {"message": "Document deleted successfully"}
        
    except Exception as e:
        logger.error(f"Error deleting document: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting document: {str(e)}"
        )

