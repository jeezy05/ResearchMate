#!/usr/bin/env python3
"""
Test LLM Service
Demonstrates Ollama integration with LangChain for RAG
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.llm_service import LLMService
from app.services.vector_store import VectorStoreService
from app.core.config import settings


def test_ollama_connection():
    """Test Ollama connection"""
    print("=" * 70)
    print("Test 1: Ollama Connection")
    print("=" * 70)
    
    try:
        llm_service = LLMService()
        print("✓ LLMService initialized successfully")
        print(f"  - Model: {llm_service.model}")
        print(f"  - Base URL: {llm_service.base_url}")
        print(f"  - Temperature: {llm_service.temperature}")
        print()
        return llm_service
    except ConnectionError as e:
        print(f"✗ Connection Error: {e}")
        print()
        return None
    except Exception as e:
        print(f"✗ Error: {e}")
        print()
        return None


def test_check_connection(llm_service):
    """Test connection check method"""
    print("=" * 70)
    print("Test 2: Check Connection Method")
    print("=" * 70)
    
    if llm_service is None:
        print("⚠ Skipping (LLMService not initialized)")
        print()
        return
    
    is_connected = llm_service.check_connection()
    if is_connected:
        print("✓ Ollama is accessible")
    else:
        print("✗ Ollama is not accessible")
    print()


def test_get_available_models(llm_service):
    """Test getting available models"""
    print("=" * 70)
    print("Test 3: Available Models")
    print("=" * 70)
    
    if llm_service is None:
        print("⚠ Skipping (LLMService not initialized)")
        print()
        return
    
    models = llm_service.get_available_models()
    print(f"✓ Found {len(models)} model(s):")
    for model in models:
        print(f"  - {model}")
    print()


def test_generate_response(llm_service):
    """Test RAG response generation"""
    print("=" * 70)
    print("Test 4: Generate Response (RAG)")
    print("=" * 70)
    
    if llm_service is None:
        print("⚠ Skipping (LLMService not initialized)")
        print()
        return
    
    # Setup vector store with sample documents
    print("Setting up vector store with sample documents...")
    vector_store = VectorStoreService()
    
    # Add some test documents
    sample_docs = [
        "Machine learning is a subset of artificial intelligence that focuses on learning from data.",
        "Deep learning uses neural networks with multiple layers to learn hierarchical representations.",
        "Natural language processing enables computers to understand and generate human language.",
        "Computer vision allows machines to interpret and analyze visual information from images.",
        "Reinforcement learning involves training agents through trial and error with rewards."
    ]
    
    metadata = {"filename": "ml_basics.txt", "source": "test"}
    result = vector_store.add_documents(chunks=sample_docs, metadata=metadata)
    print(f"✓ Added {result['documents_added']} test documents")
    print()
    
    # Test queries
    test_queries = [
        "What is machine learning?",
        "Explain deep learning",
        "How does NLP work?"
    ]
    
    for query in test_queries:
        print(f"Query: '{query}'")
        print("-" * 70)
        
        try:
            response = llm_service.generate_response(query, vector_store)
            
            print(f"✓ Answer generated:")
            print(f"  {response['answer'][:200]}...")
            print(f"\n  Sources used: {len(response['source_documents'])}")
            for i, src in enumerate(response['source_documents'][:2], 1):
                print(f"    {i}. {src['source']}: {src['content'][:60]}...")
            print()
            
        except Exception as e:
            print(f"✗ Error: {e}")
            print()
    
    # Cleanup test data
    print("Cleaning up test data...")
    vector_store.delete_collection()
    print("✓ Test data cleaned up")
    print()


def print_usage_examples():
    """Print usage examples"""
    print("\n" + "=" * 70)
    print("Usage Examples")
    print("=" * 70)
    print()
    
    print("Example 1: Basic RAG Pipeline")
    print("-" * 70)
    print("""
from app.services.llm_service import LLMService
from app.services.vector_store import VectorStoreService

# Initialize services
llm_service = LLMService()
vector_store = VectorStoreService()

# Add documents to vector store
chunks = ["Document text 1...", "Document text 2..."]
vector_store.add_documents(chunks=chunks, metadata={"filename": "doc.pdf"})

# Generate response
response = llm_service.generate_response(
    query="What is this document about?",
    vector_store=vector_store
)

print(f"Answer: {response['answer']}")
print(f"Sources: {len(response['source_documents'])}")
    """)
    print()
    
    print("Example 2: Integration with DocumentProcessor")
    print("-" * 70)
    print("""
from app.services.document_service import DocumentProcessor
from app.services.vector_store import VectorStoreService
from app.services.llm_service import LLMService

# Process PDF
processor = DocumentProcessor()
doc_result = processor.process_document("paper.pdf", "paper.pdf")

# Add to vector store
vector_store = VectorStoreService()
vector_store.add_documents(
    chunks=doc_result['chunks'],
    metadata={"filename": "paper.pdf"}
)

# Query with LLM
llm_service = LLMService()
response = llm_service.generate_response(
    query="What are the main findings?",
    vector_store=vector_store
)

print(response['answer'])
    """)
    print()


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("LLMService Test Suite")
    print("=" * 70)
    print()
    
    print("⚠ IMPORTANT: Make sure Ollama is running!")
    print(f"  - URL: {settings.OLLAMA_BASE_URL}")
    print(f"  - Model: {settings.OLLAMA_MODEL}")
    print()
    print("Start Ollama: ollama serve")
    print(f"Pull model: ollama pull {settings.OLLAMA_MODEL}")
    print()
    
    try:
        # Run tests
        llm_service = test_ollama_connection()
        test_check_connection(llm_service)
        test_get_available_models(llm_service)
        
        # Only run RAG test if connection successful
        if llm_service is not None:
            response = input("Run RAG test? This will test full pipeline (y/n): ")
            if response.lower() == 'y':
                test_generate_response(llm_service)
        
        # Print examples
        print_usage_examples()
        
        print("=" * 70)
        if llm_service is not None:
            print("✓ All tests passed!")
        else:
            print("⚠ Tests completed with warnings (Ollama not accessible)")
        print("=" * 70)
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())


