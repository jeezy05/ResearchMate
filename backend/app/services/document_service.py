"""
Document Service - Handles document processing and management
"""
from typing import Dict, List, Any
from datetime import datetime
import logging
import uuid
import os
import json

# PDF Processing
from pypdf import PdfReader

# LangChain Text Splitting
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Internal imports
from app.services.vector_store import VectorStoreService
from app.models.schemas import Document
from app.core.config import settings

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """
    Document Processor - Handles text extraction and chunking
    
    This class provides core document processing functionality:
    - PDF text extraction using pypdf
    - Text chunking using LangChain's RecursiveCharacterTextSplitter
    """
    
    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        """
        Initialize DocumentProcessor
        
        Args:
            chunk_size: Size of text chunks (defaults to settings.CHUNK_SIZE)
            chunk_overlap: Overlap between chunks (defaults to settings.CHUNK_OVERLAP)
        """
        self.chunk_size = chunk_size or settings.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP
        
        # Initialize LangChain text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        logger.info(
            f"DocumentProcessor initialized with chunk_size={self.chunk_size}, "
            f"chunk_overlap={self.chunk_overlap}"
        )
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """
        Extract all text from a PDF file
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Extracted text content
            
        Raises:
            FileNotFoundError: If file doesn't exist
            Exception: For PDF reading errors
        """
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                error_msg = f"PDF file not found: {file_path}"
                logger.error(error_msg)
                raise FileNotFoundError(error_msg)
            
            logger.info(f"Extracting text from PDF: {file_path}")
            
            # Extract text from PDF
            text_parts = []
            
            with open(file_path, 'rb') as file:
                pdf_reader = PdfReader(file)
                total_pages = len(pdf_reader.pages)
                
                logger.info(f"PDF has {total_pages} pages")
                
                for page_num, page in enumerate(pdf_reader.pages, start=1):
                    try:
                        page_text = page.extract_text()
                        if page_text and page_text.strip():
                            text_parts.append(page_text)
                            logger.debug(f"Extracted text from page {page_num}/{total_pages}")
                    except Exception as e:
                        logger.warning(f"Failed to extract text from page {page_num}: {str(e)}")
                        continue
            
            # Combine all text
            full_text = "\n\n".join(text_parts)
            
            if not full_text.strip():
                logger.warning(f"No text extracted from PDF: {file_path}")
                return ""
            
            logger.info(
                f"Successfully extracted {len(full_text)} characters from "
                f"{total_pages} pages"
            )
            
            return full_text
            
        except FileNotFoundError:
            raise
        except Exception as e:
            error_msg = f"Error extracting text from PDF {file_path}: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
    
    def chunk_text(self, text: str, chunk_size: int = None, chunk_overlap: int = None) -> List[str]:
        """
        Split text into chunks using LangChain's RecursiveCharacterTextSplitter
        
        Args:
            text: Text to split into chunks
            chunk_size: Optional override for chunk size
            chunk_overlap: Optional override for chunk overlap
            
        Returns:
            List of text chunks
            
        Raises:
            ValueError: If text is empty
        """
        try:
            if not text or not text.strip():
                error_msg = "Cannot chunk empty text"
                logger.error(error_msg)
                raise ValueError(error_msg)
            
            logger.info(f"Chunking text of length {len(text)}")
            
            # Use custom splitter if parameters provided, otherwise use default
            if chunk_size is not None or chunk_overlap is not None:
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=chunk_size or self.chunk_size,
                    chunk_overlap=chunk_overlap or self.chunk_overlap,
                    length_function=len,
                    separators=["\n\n", "\n", " ", ""]
                )
            else:
                splitter = self.text_splitter
            
            # Split text into chunks
            chunks = splitter.split_text(text)
            
            logger.info(f"Created {len(chunks)} chunks from text")
            
            # Log chunk statistics
            if chunks:
                avg_chunk_size = sum(len(chunk) for chunk in chunks) / len(chunks)
                logger.debug(
                    f"Chunk statistics: count={len(chunks)}, "
                    f"avg_size={avg_chunk_size:.0f}, "
                    f"min_size={min(len(c) for c in chunks)}, "
                    f"max_size={max(len(c) for c in chunks)}"
                )
            
            return chunks
            
        except ValueError:
            raise
        except Exception as e:
            error_msg = f"Error chunking text: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
    
    def process_document(self, file_path: str, filename: str) -> dict:
        """
        Orchestrate the full document processing pipeline
        
        This method:
        1. Extracts text from the PDF
        2. Chunks the text
        3. Returns metadata with chunks
        
        Args:
            file_path: Path to the document file
            filename: Original filename
            
        Returns:
            Dictionary containing:
                - filename: Original filename
                - total_chunks: Number of chunks created
                - chunks: List of text chunks
                - timestamp: Processing timestamp
                - file_path: Path to the file
                - text_length: Total length of extracted text
                
        Raises:
            Exception: If processing fails
        """
        try:
            logger.info(f"Processing document: {filename}")
            
            start_time = datetime.utcnow()
            
            # Step 1: Extract text from PDF
            logger.info(f"Step 1/2: Extracting text from {filename}")
            extracted_text = self.extract_text_from_pdf(file_path)
            
            if not extracted_text.strip():
                logger.warning(f"No text extracted from {filename}")
                return {
                    "filename": filename,
                    "total_chunks": 0,
                    "chunks": [],
                    "timestamp": start_time.isoformat(),
                    "file_path": file_path,
                    "text_length": 0,
                    "error": "No text could be extracted from the document"
                }
            
            # Step 2: Chunk the text
            logger.info(f"Step 2/2: Chunking text from {filename}")
            chunks = self.chunk_text(extracted_text)
            
            # Calculate processing time
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            # Build result metadata
            result = {
                "filename": filename,
                "total_chunks": len(chunks),
                "chunks": chunks,
                "timestamp": start_time.isoformat(),
                "file_path": file_path,
                "text_length": len(extracted_text),
                "processing_time_seconds": processing_time
            }
            
            logger.info(
                f"Document processing complete: {filename} - "
                f"{len(chunks)} chunks created in {processing_time:.2f}s"
            )
            
            return result
            
        except Exception as e:
            error_msg = f"Error processing document {filename}: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)


class DocumentService:
    """Service for document processing and management"""
    
    def __init__(self):
        self.vector_store = VectorStoreService()
        self.document_processor = DocumentProcessor(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )
        self.upload_dir = settings.UPLOAD_DIR
        self.metadata_file = os.path.join(settings.UPLOAD_DIR, "documents_metadata.json")
        
        # Ensure upload directory exists
        os.makedirs(self.upload_dir, exist_ok=True)
        
        # Load or create metadata
        self.documents_metadata = self._load_metadata()
    
    async def process_document(self, filename: str, content: bytes) -> Dict[str, Any]:
        """
        Process and index a document
        
        Args:
            filename: Name of the file
            content: File content as bytes
            
        Returns:
            Processing result with document_id and chunk count
        """
        try:
            document_id = str(uuid.uuid4())
            
            # Save file
            file_path = os.path.join(self.upload_dir, f"{document_id}_{filename}")
            with open(file_path, "wb") as f:
                f.write(content)
            
            # Process document using DocumentProcessor
            logger.info(f"Processing document with DocumentProcessor: {filename}")
            processing_result = self.document_processor.process_document(
                file_path=file_path,
                filename=filename
            )
            
            chunks = processing_result["chunks"]
            
            if not chunks:
                logger.warning(f"No chunks created for {filename}")
                return {
                    "document_id": document_id,
                    "chunks_created": 0,
                    "error": processing_result.get("error", "No text extracted")
                }
            
            # Prepare base metadata for all chunks
            base_metadata = {
                "filename": filename,
                "document_id": document_id,
            }
            
            # Add to vector store
            logger.info(f"Adding {len(chunks)} chunks to vector store...")
            result = self.vector_store.add_documents(
                chunks=chunks,
                metadata=base_metadata
            )
            
            # The vector store now handles chunk_id generation internally
            chunk_ids = [result.get("documents_added", len(chunks))]
            
            # Store document metadata
            self.documents_metadata[document_id] = {
                "id": document_id,
                "filename": filename,
                "upload_date": datetime.utcnow().isoformat(),
                "file_path": file_path,
                "chunk_count": len(chunks),
                "chunk_ids": chunk_ids,
                "size": len(content),
                "text_length": processing_result.get("text_length", 0),
                "processing_time": processing_result.get("processing_time_seconds", 0),
                "processed": True
            }
            self._save_metadata()
            
            logger.info(f"Document {filename} processed successfully")
            return {
                "document_id": document_id,
                "chunks_created": len(chunks)
            }
            
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            raise
    
    async def list_documents(self) -> List[Document]:
        """
        List all processed documents
        
        Returns:
            List of Document objects
        """
        documents = []
        for doc_id, metadata in self.documents_metadata.items():
            documents.append(Document(
                id=metadata["id"],
                filename=metadata["filename"],
                content_type="application/pdf",  # You can enhance this
                size=metadata["size"],
                upload_date=datetime.fromisoformat(metadata["upload_date"]),
                processed=metadata["processed"],
                chunk_count=metadata["chunk_count"]
            ))
        return documents
    
    async def delete_document(self, document_id: str):
        """
        Delete a document and its embeddings
        
        Args:
            document_id: ID of the document to delete
        """
        try:
            if document_id not in self.documents_metadata:
                raise ValueError(f"Document {document_id} not found")
            
            metadata = self.documents_metadata[document_id]
            
            # Delete from vector store
            chunk_ids = metadata.get("chunk_ids", [])
            if chunk_ids:
                self.vector_store.delete_documents(chunk_ids)
            
            # Delete file
            file_path = metadata.get("file_path")
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
            
            # Remove from metadata
            del self.documents_metadata[document_id]
            self._save_metadata()
            
            logger.info(f"Document {document_id} deleted successfully")
            
        except Exception as e:
            logger.error(f"Error deleting document: {str(e)}")
            raise
    
    def _load_metadata(self) -> Dict:
        """Load documents metadata from file"""
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading metadata: {str(e)}")
                return {}
        return {}
    
    def _save_metadata(self):
        """Save documents metadata to file"""
        try:
            with open(self.metadata_file, "w") as f:
                json.dump(self.documents_metadata, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving metadata: {str(e)}")

