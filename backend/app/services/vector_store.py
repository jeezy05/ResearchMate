"""
Vector Store Service - Manages document embeddings and similarity search

This module provides ChromaDB integration with LangChain and HuggingFace embeddings.
Implements a singleton pattern to ensure only one vector store instance exists.
"""
from typing import List, Dict, Optional, Any
from datetime import datetime
import logging
import uuid

# ChromaDB
import chromadb
from chromadb.config import Settings as ChromaSettings

# LangChain Integration
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Internal imports
from app.core.config import settings

logger = logging.getLogger(__name__)


class VectorStoreService:
    """
    Singleton Vector Store Service using ChromaDB with LangChain integration
    
    Features:
    - HuggingFace embeddings for document vectorization
    - ChromaDB for persistent vector storage
    - LangChain Chroma wrapper for easy integration
    - Singleton pattern to ensure single instance
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """
        Singleton pattern implementation
        Ensures only one instance of VectorStoreService exists
        """
        if cls._instance is None:
            cls._instance = super(VectorStoreService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """
        Initialize Vector Store Service
        
        Sets up:
        - HuggingFace embeddings model
        - ChromaDB persistent client
        - Collection for research papers
        """
        # Only initialize once (singleton pattern)
        if VectorStoreService._initialized:
            return
        
        logger.info("Initializing VectorStoreService...")
        
        # Configuration
        self.persist_directory = settings.CHROMA_PERSIST_DIRECTORY
        self.collection_name = "research_papers"
        self.embedding_model_name = settings.EMBEDDING_MODEL
        
        # Initialize HuggingFace embeddings
        logger.info(f"Loading HuggingFace embeddings model: {self.embedding_model_name}")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.embedding_model_name,
            model_kwargs={'device': 'cpu'},  # Use 'cuda' if GPU available
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Initialize ChromaDB client
        logger.info(f"Setting up ChromaDB at: {self.persist_directory}")
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=ChromaSettings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Initialize LangChain Chroma vector store
        self.vectorstore = Chroma(
            client=self.client,
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
        )
        
        # Get collection for direct access if needed
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
        # Mark as initialized
        VectorStoreService._initialized = True
        
        document_count = self.collection.count()
        logger.info(
            f"✓ VectorStoreService initialized successfully\n"
            f"  - Collection: {self.collection_name}\n"
            f"  - Documents: {document_count}\n"
            f"  - Embedding model: {self.embedding_model_name}"
        )
    
    def add_documents(self, chunks: List[str], metadata: dict) -> dict:
        """
        Add documents to ChromaDB with metadata
        
        Generates embeddings using HuggingFace and stores them in ChromaDB.
        Each chunk gets enhanced metadata including filename, chunk_id, and timestamp.
        
        Args:
            chunks: List of text chunks to add
            metadata: Base metadata dict (typically contains filename)
            
        Returns:
            Dictionary with status and count:
            {
                "status": "success",
                "documents_added": int,
                "collection": str,
                "embedding_model": str
            }
        """
        try:
            if not chunks:
                logger.warning("No chunks provided to add_documents")
                return {
                    "status": "skipped",
                    "documents_added": 0,
                    "message": "No chunks provided"
                }
            
            logger.info(f"Adding {len(chunks)} documents to vector store...")
            
            # Prepare metadata for each chunk
            metadatas = []
            ids = []
            
            for i, chunk in enumerate(chunks):
                chunk_id = str(uuid.uuid4())
                chunk_metadata = {
                    **metadata,  # Include base metadata (e.g., filename)
                    "chunk_id": chunk_id,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "timestamp": datetime.utcnow().isoformat(),
                }
                metadatas.append(chunk_metadata)
                ids.append(chunk_id)
            
            # Add documents using LangChain Chroma
            # This automatically generates embeddings using HuggingFaceEmbeddings
            logger.info("Generating embeddings and adding to ChromaDB...")
            self.vectorstore.add_texts(
                texts=chunks,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(
                f"✓ Successfully added {len(chunks)} documents\n"
                f"  - Collection: {self.collection_name}\n"
                f"  - Embedding model: {self.embedding_model_name}"
            )
            
            return {
                "status": "success",
                "documents_added": len(chunks),
                "collection": self.collection_name,
                "embedding_model": self.embedding_model_name
            }
            
        except Exception as e:
            error_msg = f"Error adding documents to vector store: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
    
    def similarity_search(self, query: str, k: int = None) -> List[dict]:
        """
        Perform similarity search on ChromaDB
        
        Uses HuggingFace embeddings to find the most relevant documents
        for the given query.
        
        Args:
            query: Search query string
            k: Number of results to return (defaults to settings.TOP_K_RETRIEVAL)
            
        Returns:
            List of dictionaries containing:
            {
                "content": str,          # Document text
                "metadata": dict,        # Document metadata
                "score": float,          # Similarity score (0-1)
                "id": str                # Document ID
            }
        """
        try:
            # Use settings default if k not provided
            if k is None:
                k = settings.TOP_K_RETRIEVAL
            
            logger.info(f"Performing similarity search for query (top {k} results)")
            logger.debug(f"Query: {query[:100]}...")
            
            # Perform similarity search using LangChain Chroma
            # This automatically generates query embedding and searches
            results = self.vectorstore.similarity_search_with_score(
                query=query,
                k=k
            )
            
            # Format results
            documents = []
            for doc, score in results:
                # Convert distance to similarity score (assuming cosine distance)
                # ChromaDB returns distance, so we convert to similarity
                similarity_score = 1 - score if score < 1 else 0.0
                
                documents.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": similarity_score,
                    "id": doc.metadata.get("chunk_id", "unknown")
                })
            
            logger.info(
                f"✓ Found {len(documents)} relevant documents\n"
                f"  - Top score: {documents[0]['score']:.4f}" if documents else "  - No results"
            )
            
            return documents
            
        except Exception as e:
            error_msg = f"Error searching vector store: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
    
    def delete_collection(self) -> dict:
        """
        Clear all documents from the collection
        
        Useful for testing and resetting the vector store.
        This deletes the entire collection and recreates it.
        
        Returns:
            Dictionary with operation status:
            {
                "status": "success",
                "message": str,
                "collection": str
            }
        """
        try:
            logger.warning(f"Deleting collection: {self.collection_name}")
            
            # Delete the collection
            self.client.delete_collection(name=self.collection_name)
            
            # Recreate the collection
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            
            # Reinitialize the vectorstore
            self.vectorstore = Chroma(
                client=self.client,
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
            )
            
            logger.info(f"✓ Collection '{self.collection_name}' deleted and recreated")
            
            return {
                "status": "success",
                "message": f"Collection '{self.collection_name}' cleared successfully",
                "collection": self.collection_name
            }
            
        except Exception as e:
            error_msg = f"Error deleting collection: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
    
    # Additional utility methods
    
    def delete_documents(self, ids: List[str]) -> dict:
        """
        Delete specific documents by IDs
        
        Args:
            ids: List of document IDs to delete
            
        Returns:
            Dictionary with operation status
        """
        try:
            self.collection.delete(ids=ids)
            logger.info(f"Deleted {len(ids)} documents from vector store")
            return {
                "status": "success",
                "documents_deleted": len(ids)
            }
        except Exception as e:
            logger.error(f"Error deleting documents: {str(e)}")
            raise
    
    def delete_by_source(self, source: str) -> dict:
        """
        Delete all documents from a specific source
        
        Args:
            source: Source filename to delete
            
        Returns:
            Dictionary with operation status
        """
        try:
            self.collection.delete(where={"filename": source})
            logger.info(f"Deleted documents from source: {source}")
            return {
                "status": "success",
                "source": source
            }
        except Exception as e:
            logger.error(f"Error deleting documents by source: {str(e)}")
            raise
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get vector store status and statistics
        
        Returns:
            Status dictionary with health and statistics
        """
        try:
            count = self.collection.count()
            return {
                "healthy": True,
                "document_count": count,
                "collection_name": self.collection_name,
                "embedding_model": self.embedding_model_name,
                "persist_directory": self.persist_directory
            }
        except Exception as e:
            logger.error(f"Error getting vector store status: {str(e)}")
            return {
                "healthy": False,
                "document_count": 0,
                "error": str(e)
            }
    
    def get_collection_info(self) -> dict:
        """
        Get detailed information about the collection
        
        Returns:
            Dictionary with collection details
        """
        try:
            count = self.collection.count()
            return {
                "collection_name": self.collection_name,
                "document_count": count,
                "embedding_model": self.embedding_model_name,
                "embedding_dimension": 384,  # all-MiniLM-L6-v2 dimension
                "persist_directory": self.persist_directory,
                "distance_metric": "cosine"
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {str(e)}")
            raise


# Singleton instance getter
def get_vector_store() -> VectorStoreService:
    """
    Get the singleton instance of VectorStoreService
    
    Returns:
        VectorStoreService instance
    """
    return VectorStoreService()

