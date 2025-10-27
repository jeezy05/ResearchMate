#!/usr/bin/env python3
"""
Test script for Pydantic schemas validation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models.schemas import (
    UploadResponse, QueryRequest, QueryResponse, HealthResponse,
    SourceDocument, ErrorResponse, ConversationMessage
)
from datetime import datetime
import json

def test_upload_response():
    """Test UploadResponse schema"""
    print("🧪 Testing UploadResponse...")
    
    # Valid response
    try:
        response = UploadResponse(
            filename="test.pdf",
            total_chunks=5,
            message="File uploaded successfully",
            status="success"
        )
        print("✅ Valid UploadResponse created successfully")
        print(f"   - Filename: {response.filename}")
        print(f"   - Chunks: {response.total_chunks}")
        print(f"   - Status: {response.status}")
    except Exception as e:
        print(f"❌ Error creating UploadResponse: {e}")
        return False
    
    # Test status validation
    try:
        invalid_response = UploadResponse(
            filename="test.pdf",
            total_chunks=5,
            message="File uploaded successfully",
            status="invalid_status"  # This should fail
        )
        print("❌ Should have failed with invalid status")
        return False
    except ValueError as e:
        print(f"✅ Status validation working: {e}")
    
    return True

def test_query_request():
    """Test QueryRequest schema"""
    print("\n🧪 Testing QueryRequest...")
    
    # Valid request
    try:
        request = QueryRequest(
            question="What is machine learning?",
            max_results=5
        )
        print("✅ Valid QueryRequest created successfully")
        print(f"   - Question: {request.question}")
        print(f"   - Max results: {request.max_results}")
    except Exception as e:
        print(f"❌ Error creating QueryRequest: {e}")
        return False
    
    # Test empty question validation
    try:
        invalid_request = QueryRequest(question="")  # Empty question should fail
        print("❌ Should have failed with empty question")
        return False
    except ValueError as e:
        print(f"✅ Question validation working: {e}")
    
    # Test max_results validation
    try:
        invalid_request = QueryRequest(
            question="Test question",
            max_results=15  # Should fail (max is 10)
        )
        print("❌ Should have failed with max_results > 10")
        return False
    except ValueError as e:
        print(f"✅ Max results validation working: {e}")
    
    return True

def test_query_response():
    """Test QueryResponse schema"""
    print("\n🧪 Testing QueryResponse...")
    
    # Valid response
    try:
        sources = [
            {
                "content": "Machine learning is a subset of AI...",
                "metadata": {"filename": "ml_paper.pdf", "page": 1}
            },
            {
                "content": "Deep learning uses neural networks...",
                "metadata": {"filename": "dl_paper.pdf", "page": 2}
            }
        ]
        
        response = QueryResponse(
            question="What is machine learning?",
            answer="Machine learning is a subset of artificial intelligence...",
            sources=sources,
            processing_time=1.5
        )
        print("✅ Valid QueryResponse created successfully")
        print(f"   - Question: {response.question}")
        print(f"   - Answer length: {len(response.answer)} chars")
        print(f"   - Sources: {len(response.sources)}")
        print(f"   - Processing time: {response.processing_time}s")
    except Exception as e:
        print(f"❌ Error creating QueryResponse: {e}")
        return False
    
    # Test sources validation
    try:
        invalid_sources = [
            {"content": "Test content"}  # Missing metadata
        ]
        
        invalid_response = QueryResponse(
            question="Test question",
            answer="Test answer",
            sources=invalid_sources,
            processing_time=1.0
        )
        print("❌ Should have failed with invalid sources")
        return False
    except ValueError as e:
        print(f"✅ Sources validation working: {e}")
    
    return True

def test_health_response():
    """Test HealthResponse schema"""
    print("\n🧪 Testing HealthResponse...")
    
    # Valid response
    try:
        health = HealthResponse(
            status="healthy",
            ollama_connected=True,
            vector_store_ready=True,
            model="llama2"
        )
        print("✅ Valid HealthResponse created successfully")
        print(f"   - Status: {health.status}")
        print(f"   - Ollama connected: {health.ollama_connected}")
        print(f"   - Vector store ready: {health.vector_store_ready}")
        print(f"   - Model: {health.model}")
    except Exception as e:
        print(f"❌ Error creating HealthResponse: {e}")
        return False
    
    # Test status validation
    try:
        invalid_health = HealthResponse(
            status="invalid_status",
            ollama_connected=True,
            vector_store_ready=True,
            model="llama2"
        )
        print("❌ Should have failed with invalid status")
        return False
    except ValueError as e:
        print(f"✅ Status validation working: {e}")
    
    return True

def test_source_document():
    """Test SourceDocument schema"""
    print("\n🧪 Testing SourceDocument...")
    
    # Valid source document
    try:
        source = SourceDocument(
            filename="research_paper.pdf",
            page=1,
            chunk_id="chunk_001",
            relevance_score=0.85,
            content_preview="Machine learning is a subset of artificial intelligence..."
        )
        print("✅ Valid SourceDocument created successfully")
        print(f"   - Filename: {source.filename}")
        print(f"   - Page: {source.page}")
        print(f"   - Relevance score: {source.relevance_score}")
    except Exception as e:
        print(f"❌ Error creating SourceDocument: {e}")
        return False
    
    # Test relevance score validation
    try:
        invalid_source = SourceDocument(
            filename="test.pdf",
            chunk_id="chunk_001",
            relevance_score=1.5,  # Should fail (max is 1.0)
            content_preview="Test content"
        )
        print("❌ Should have failed with relevance_score > 1.0")
        return False
    except ValueError as e:
        print(f"✅ Relevance score validation working: {e}")
    
    return True

def test_error_response():
    """Test ErrorResponse schema"""
    print("\n🧪 Testing ErrorResponse...")
    
    # Valid error response
    try:
        error = ErrorResponse(
            error="File not found",
            detail="The requested file 'test.pdf' could not be found"
        )
        print("✅ Valid ErrorResponse created successfully")
        print(f"   - Error: {error.error}")
        print(f"   - Detail: {error.detail}")
        print(f"   - Timestamp: {error.timestamp}")
    except Exception as e:
        print(f"❌ Error creating ErrorResponse: {e}")
        return False
    
    return True

def test_conversation_message():
    """Test ConversationMessage schema"""
    print("\n🧪 Testing ConversationMessage...")
    
    # Valid message
    try:
        message = ConversationMessage(
            role="user",
            content="What is machine learning?"
        )
        print("✅ Valid ConversationMessage created successfully")
        print(f"   - Role: {message.role}")
        print(f"   - Content: {message.content}")
    except Exception as e:
        print(f"❌ Error creating ConversationMessage: {e}")
        return False
    
    # Test role validation
    try:
        invalid_message = ConversationMessage(
            role="invalid_role",
            content="Test message"
        )
        print("❌ Should have failed with invalid role")
        return False
    except ValueError as e:
        print(f"✅ Role validation working: {e}")
    
    return True

def test_json_serialization():
    """Test JSON serialization of schemas"""
    print("\n🧪 Testing JSON serialization...")
    
    try:
        # Test UploadResponse serialization
        upload_response = UploadResponse(
            filename="test.pdf",
            total_chunks=5,
            message="Success",
            status="success"
        )
        
        json_data = upload_response.model_dump()
        print("✅ JSON serialization working")
        print(f"   - Serialized data: {json.dumps(json_data, indent=2)}")
        
        # Test deserialization
        restored_response = UploadResponse(**json_data)
        print("✅ JSON deserialization working")
        print(f"   - Restored filename: {restored_response.filename}")
        
    except Exception as e:
        print(f"❌ JSON serialization failed: {e}")
        return False
    
    return True

def main():
    """Run all schema tests"""
    print("🚀 Testing Pydantic Schemas")
    print("=" * 50)
    
    tests = [
        test_upload_response,
        test_query_request,
        test_query_response,
        test_health_response,
        test_source_document,
        test_error_response,
        test_conversation_message,
        test_json_serialization
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All schema tests passed!")
        print("✅ Pydantic models are working correctly")
        print("✅ Field validators are functioning")
        print("✅ JSON serialization is working")
    else:
        print("❌ Some tests failed!")
        print("Please check the schema definitions and validators")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())

