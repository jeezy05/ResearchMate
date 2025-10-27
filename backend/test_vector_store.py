#!/usr/bin/env python3
"""
Test Vector Store Service
Demonstrates ChromaDB integration with LangChain and HuggingFace embeddings
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.vector_store import VectorStoreService, get_vector_store
from app.core.config import settings


def test_singleton_pattern():
    """Test that VectorStoreService implements singleton pattern"""
    print("=" * 70)
    print("Test 1: Singleton Pattern")
    print("=" * 70)
    
    # Create multiple instances
    store1 = VectorStoreService()
    store2 = VectorStoreService()
    store3 = get_vector_store()
    
    # All should be the same instance
    assert store1 is store2, "Instances should be the same (singleton)"
    assert store1 is store3, "get_vector_store should return same instance"
    
    print("✓ Singleton pattern working correctly")
    print(f"  - Instance ID: {id(store1)}")
    print(f"  - Collection: {store1.collection_name}")
    print(f"  - Embedding Model: {store1.embedding_model_name}")
    print()


def test_initialization():
    """Test VectorStoreService initialization"""
    print("=" * 70)
    print("Test 2: Initialization")
    print("=" * 70)
    
    store = VectorStoreService()
    
    # Check initialization
    assert hasattr(store, 'embeddings'), "Should have embeddings"
    assert hasattr(store, 'vectorstore'), "Should have vectorstore"
    assert hasattr(store, 'client'), "Should have client"
    assert hasattr(store, 'collection'), "Should have collection"
    
    print("✓ Vector store initialized successfully")
    print(f"  - Persist directory: {store.persist_directory}")
    print(f"  - Collection name: {store.collection_name}")
    print(f"  - Embedding model: {store.embedding_model_name}")
    print(f"  - Current documents: {store.collection.count()}")
    print()


def test_add_documents():
    """Test adding documents to vector store"""
    print("=" * 70)
    print("Test 3: Add Documents")
    print("=" * 70)
    
    store = VectorStoreService()
    
    # Sample documents
    chunks = [
        "Artificial intelligence is transforming the world of technology.",
        "Machine learning is a subset of artificial intelligence.",
        "Deep learning uses neural networks with multiple layers.",
        "Natural language processing enables computers to understand human language.",
        "Computer vision allows machines to interpret visual information."
    ]
    
    # Metadata
    metadata = {
        "filename": "test_document.txt",
        "source": "test"
    }
    
    # Add documents
    print("Adding 5 test documents...")
    result = store.add_documents(chunks=chunks, metadata=metadata)
    
    print(f"✓ Documents added successfully")
    print(f"  - Status: {result['status']}")
    print(f"  - Documents added: {result['documents_added']}")
    print(f"  - Collection: {result['collection']}")
    print(f"  - Embedding model: {result['embedding_model']}")
    print()


def test_similarity_search():
    """Test similarity search"""
    print("=" * 70)
    print("Test 4: Similarity Search")
    print("=" * 70)
    
    store = VectorStoreService()
    
    # Perform searches
    queries = [
        "What is machine learning?",
        "Tell me about neural networks",
        "How do computers understand language?"
    ]
    
    for query in queries:
        print(f"\nQuery: '{query}'")
        results = store.similarity_search(query=query, k=3)
        
        print(f"✓ Found {len(results)} results:")
        for i, doc in enumerate(results, 1):
            print(f"  {i}. Score: {doc['score']:.4f}")
            print(f"     Content: {doc['content'][:60]}...")
            print(f"     Metadata: {doc['metadata']}")
    
    print()


def test_get_status():
    """Test getting vector store status"""
    print("=" * 70)
    print("Test 5: Get Status")
    print("=" * 70)
    
    store = VectorStoreService()
    status = store.get_status()
    
    print("✓ Vector store status:")
    print(f"  - Healthy: {status['healthy']}")
    print(f"  - Document count: {status['document_count']}")
    print(f"  - Collection: {status['collection_name']}")
    print(f"  - Embedding model: {status['embedding_model']}")
    print(f"  - Persist directory: {status['persist_directory']}")
    print()


def test_collection_info():
    """Test getting collection information"""
    print("=" * 70)
    print("Test 6: Collection Info")
    print("=" * 70)
    
    store = VectorStoreService()
    info = store.get_collection_info()
    
    print("✓ Collection information:")
    for key, value in info.items():
        print(f"  - {key}: {value}")
    print()


def test_delete_collection():
    """Test deleting collection"""
    print("=" * 70)
    print("Test 7: Delete Collection")
    print("=" * 70)
    
    store = VectorStoreService()
    
    # Get count before deletion
    before_count = store.collection.count()
    print(f"Documents before deletion: {before_count}")
    
    # Delete collection
    result = store.delete_collection()
    
    # Get count after deletion
    after_count = store.collection.count()
    
    print(f"✓ Collection deleted and recreated")
    print(f"  - Status: {result['status']}")
    print(f"  - Message: {result['message']}")
    print(f"  - Documents after: {after_count}")
    print()


def print_usage_examples():
    """Print usage examples"""
    print("\n" + "=" * 70)
    print("Usage Examples")
    print("=" * 70)
    print()
    
    print("Example 1: Basic Usage")
    print("-" * 70)
    print("""
from app.services.vector_store import VectorStoreService

# Get singleton instance
store = VectorStoreService()

# Add documents
chunks = ["Text chunk 1", "Text chunk 2", "Text chunk 3"]
metadata = {"filename": "document.pdf"}
result = store.add_documents(chunks=chunks, metadata=metadata)

print(f"Added {result['documents_added']} documents")
    """)
    print()
    
    print("Example 2: Similarity Search")
    print("-" * 70)
    print("""
from app.services.vector_store import get_vector_store

# Get vector store
store = get_vector_store()

# Search for similar documents
query = "What is artificial intelligence?"
results = store.similarity_search(query=query, k=5)

for doc in results:
    print(f"Score: {doc['score']:.4f}")
    print(f"Content: {doc['content']}")
    print(f"Metadata: {doc['metadata']}")
    """)
    print()
    
    print("Example 3: Integration with Document Processor")
    print("-" * 70)
    print("""
from app.services.document_service import DocumentProcessor
from app.services.vector_store import VectorStoreService

# Process document
processor = DocumentProcessor()
result = processor.process_document("research.pdf", "research.pdf")

# Add to vector store
store = VectorStoreService()
vector_result = store.add_documents(
    chunks=result['chunks'],
    metadata={"filename": result['filename']}
)

print(f"Added {vector_result['documents_added']} chunks to vector store")
    """)
    print()


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("VectorStoreService Test Suite")
    print("=" * 70)
    print()
    
    try:
        # Run tests
        test_singleton_pattern()
        test_initialization()
        test_add_documents()
        test_similarity_search()
        test_get_status()
        test_collection_info()
        test_delete_collection()
        
        # Print examples
        print_usage_examples()
        
        print("=" * 70)
        print("✓ All tests passed!")
        print("=" * 70)
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())


