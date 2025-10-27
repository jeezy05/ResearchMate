"""
RAG Service - Orchestrates retrieval and generation
"""
from typing import Dict, List, Optional, Any
from app.services.llm_service import LLMService
from app.services.vector_store import VectorStoreService
from app.models.schemas import SourceDocument, ConversationHistory, ConversationMessage
from app.core.config import settings
import uuid
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class RAGService:
    """RAG Service for document Q&A"""
    
    def __init__(self):
        self.llm_service = LLMService()
        self.vector_store = VectorStoreService()
        self.conversations: Dict[str, ConversationHistory] = {}
    
    async def query(
        self,
        question: str,
        conversation_id: Optional[str] = None,
        max_results: int = 5,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Process a query through the RAG pipeline
        
        Args:
            question: User's question
            conversation_id: Optional conversation ID for context
            max_results: Number of relevant documents to retrieve
            temperature: LLM temperature setting
            
        Returns:
            Dictionary with answer, sources, and metadata
        """
        try:
            # Generate or use existing conversation ID
            if not conversation_id:
                conversation_id = str(uuid.uuid4())
            
            # Retrieve relevant documents
            logger.info(f"Retrieving relevant documents for: {question[:50]}...")
            retrieved_docs = self.vector_store.similarity_search(
                query=question,
                k=max_results
            )
            
            if not retrieved_docs:
                return {
                    "answer": "I couldn't find any relevant information in the documents to answer your question.",
                    "sources": [],
                    "conversation_id": conversation_id
                }
            
            # Build context from retrieved documents
            context = self._build_context(retrieved_docs)
            
            # Get conversation history if exists
            conversation_context = ""
            if conversation_id in self.conversations:
                conversation_context = self._format_conversation_history(
                    self.conversations[conversation_id]
                )
            
            # Generate answer using LLM
            logger.info("Generating answer with LLM...")
            result = self.llm_service.generate_response(
                query=question,
                vector_store=self.vector_store
            )
            answer = result.get("answer", "")
            
            # Format sources
            sources = self._format_sources(retrieved_docs)
            
            # Update conversation history
            self._update_conversation(conversation_id, question, answer)
            
            return {
                "answer": answer,
                "sources": sources,
                "conversation_id": conversation_id
            }
            
        except Exception as e:
            logger.error(f"Error in RAG query: {str(e)}")
            raise
    
    def _build_context(self, documents: List[Dict]) -> str:
        """Build context string from retrieved documents"""
        context_parts = []
        for i, doc in enumerate(documents, 1):
            content = doc.get("content", "")
            metadata = doc.get("metadata", {})
            source = metadata.get("source", "Unknown")
            
            context_parts.append(
                f"[Document {i} - {source}]\n{content}\n"
            )
        
        return "\n".join(context_parts)
    
    def _format_sources(self, documents: List[Dict]) -> List[SourceDocument]:
        """Format retrieved documents as source references"""
        sources = []
        for doc in documents:
            metadata = doc.get("metadata", {})
            content = doc.get("content", "")
            
            sources.append(SourceDocument(
                filename=metadata.get("source", "Unknown"),
                page=metadata.get("page"),
                chunk_id=metadata.get("chunk_id", str(uuid.uuid4())),
                relevance_score=doc.get("score", 0.0),
                content_preview=content[:200] + "..." if len(content) > 200 else content
            ))
        
        return sources
    
    def _format_conversation_history(self, conversation: ConversationHistory) -> str:
        """Format conversation history for LLM context"""
        history_parts = []
        for msg in conversation.messages[-5:]:  # Last 5 messages
            role = "User" if msg.role == "user" else "Assistant"
            history_parts.append(f"{role}: {msg.content}")
        
        return "\n".join(history_parts)
    
    def _update_conversation(self, conversation_id: str, question: str, answer: str):
        """Update conversation history"""
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = ConversationHistory(
                conversation_id=conversation_id,
                messages=[],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        
        conversation = self.conversations[conversation_id]
        conversation.messages.append(
            ConversationMessage(role="user", content=question)
        )
        conversation.messages.append(
            ConversationMessage(role="assistant", content=answer)
        )
        conversation.updated_at = datetime.utcnow()
    
    async def get_conversation_history(self, conversation_id: str) -> Optional[ConversationHistory]:
        """Retrieve conversation history by ID"""
        return self.conversations.get(conversation_id)

