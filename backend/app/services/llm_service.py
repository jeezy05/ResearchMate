"""
LLM Service - Handles interactions with Ollama using LangChain

This module provides LLM functionality for the RAG pipeline using Ollama
with LangChain integration for retrieval-augmented generation.
"""
from typing import Dict, Any, Optional
import logging
import requests

# LangChain imports
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.schema import Document

# Internal imports
from app.core.config import settings
from app.services.vector_store import VectorStoreService

logger = logging.getLogger(__name__)


class LLMService:
    """
    Service for interacting with Ollama LLM using LangChain
    
    Provides retrieval-augmented generation capabilities by combining
    Ollama LLM with vector store retrieval for answering questions
    about research papers and ML/DS concepts.
    """
    
    def __init__(self):
        """
        Initialize LLM Service with Ollama
        
        Sets up:
        - Ollama LLM with configuration from settings
        - Custom prompt template for research paper Q&A
        - Connection validation
        """
        logger.info("Initializing LLMService with Ollama...")
        
        # Configuration
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
        self.temperature = 0.7
        
        # Validate Ollama connection before proceeding
        self._validate_ollama_connection()
        
        # Initialize Ollama LLM with LangChain
        try:
            self.llm = Ollama(
                base_url=self.base_url,
                model=self.model,
                temperature=self.temperature,
                timeout=300  # 5 minutes timeout
            )
            logger.info(f"✓ Ollama LLM initialized: {self.model} at {self.base_url}")
        except Exception as e:
            error_msg = (
                f"Failed to initialize Ollama LLM: {str(e)}\n"
                f"Make sure Ollama is running at {self.base_url}\n"
                f"Start Ollama with: ollama serve\n"
                f"Pull model with: ollama pull {self.model}"
            )
            logger.error(error_msg)
            raise ConnectionError(error_msg)
        
        # Create custom prompt template for research paper Q&A
        self.prompt_template = PromptTemplate(
            template="""You are a helpful AI assistant specialized in explaining research papers and ML/DS concepts.
Use the following context to answer the question. If you don't know the answer, say so.

Context: {context}

Question: {question}

Answer:""",
            input_variables=["context", "question"]
        )
        
        logger.info("✓ LLMService initialized successfully")
    
    def _validate_ollama_connection(self) -> None:
        """
        Validate that Ollama is running and accessible
        
        Raises:
            ConnectionError: If Ollama is not accessible
        """
        try:
            logger.info(f"Validating Ollama connection at {self.base_url}...")
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            response.raise_for_status()
            
            # Check if model is available
            models_data = response.json()
            available_models = [m.get('name', '').split(':')[0] for m in models_data.get('models', [])]
            
            if self.model not in available_models and not any(self.model in m for m in available_models):
                logger.warning(
                    f"Model '{self.model}' not found in Ollama. "
                    f"Available models: {available_models}\n"
                    f"Pull the model with: ollama pull {self.model}"
                )
            
            logger.info(f"✓ Ollama is accessible at {self.base_url}")
            
        except requests.exceptions.ConnectionError:
            error_msg = (
                f"Cannot connect to Ollama at {self.base_url}\n"
                f"Please ensure Ollama is running:\n"
                f"  1. Install Ollama from https://ollama.ai\n"
                f"  2. Start Ollama: ollama serve\n"
                f"  3. Pull model: ollama pull {self.model}"
            )
            logger.error(error_msg)
            raise ConnectionError(error_msg)
        except requests.exceptions.Timeout:
            error_msg = f"Timeout connecting to Ollama at {self.base_url}"
            logger.error(error_msg)
            raise ConnectionError(error_msg)
        except Exception as e:
            error_msg = f"Error validating Ollama connection: {str(e)}"
            logger.error(error_msg)
            raise ConnectionError(error_msg)
    
    def generate_response(self, query: str, vector_store: VectorStoreService) -> dict:
        """
        Generate a response using RAG (Retrieval-Augmented Generation)
        
        This method:
        1. Retrieves relevant documents from the vector store
        2. Creates a RetrievalQA chain with the LLM and retriever
        3. Generates a response based on the retrieved context
        4. Returns the answer with source documents
        
        Args:
            query: The user's question
            vector_store: VectorStoreService instance for retrieval
            
        Returns:
            Dictionary containing:
            {
                "answer": str,                    # Generated response
                "source_documents": List[dict],   # Sources used
                "query": str                      # Original question
            }
            
        Raises:
            ConnectionError: If Ollama is not accessible
            Exception: For other errors during generation
        """
        try:
            logger.info(f"Generating response for query: {query[:100]}...")
            
            # Validate Ollama is still accessible
            self._validate_ollama_connection()
            
            # Get retriever from vector store
            # LangChain expects a retriever interface
            retriever = vector_store.vectorstore.as_retriever(
                search_kwargs={"k": settings.TOP_K_RETRIEVAL}
            )
            
            # Create RetrievalQA chain
            logger.info("Creating RetrievalQA chain...")
            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",  # "stuff" puts all docs into context
                retriever=retriever,
                return_source_documents=True,
                chain_type_kwargs={
                    "prompt": self.prompt_template
                },
                verbose=False
            )
            
            # Generate response
            logger.info("Generating answer with LLM...")
            result = qa_chain.invoke({"query": query})
            
            # Format source documents
            source_documents = []
            for doc in result.get("source_documents", []):
                source_documents.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "source": doc.metadata.get("filename", "Unknown")
                })
            
            response = {
                "answer": result.get("result", "").strip(),
                "source_documents": source_documents,
                "query": query
            }
            
            logger.info(
                f"✓ Generated response with {len(source_documents)} source documents"
            )
            
            return response
            
        except ConnectionError:
            raise
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
    
    def check_connection(self) -> bool:
        """
        Check if Ollama is accessible
        
        Returns:
            True if Ollama is running and accessible, False otherwise
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Ollama connection check failed: {str(e)}")
            return False
    
    def get_available_models(self) -> list:
        """
        Get list of available Ollama models
        
        Returns:
            List of model names
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            return [m.get('name', '') for m in data.get('models', [])]
        except Exception as e:
            logger.error(f"Error getting available models: {str(e)}")
            return []

