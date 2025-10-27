#!/usr/bin/env python3
"""
Test script for FastAPI routes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from app.main import app
from app.models.schemas import QueryRequest
import json

def test_health_endpoint():
    """Test health check endpoint"""
    print("🧪 Testing /health endpoint...")
    
    client = TestClient(app)
    
    try:
        response = client.get("/api/v1/health")
        print(f"   - Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   - Status: {data.get('status')}")
            print(f"   - Ollama Connected: {data.get('ollama_connected')}")
            print(f"   - Vector Store Ready: {data.get('vector_store_ready')}")
            print(f"   - Model: {data.get('model')}")
            print("✅ Health endpoint working")
            return True
        else:
            print(f"❌ Health endpoint failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False

def test_status_endpoint():
    """Test status endpoint"""
    print("\n🧪 Testing /status endpoint...")
    
    client = TestClient(app)
    
    try:
        response = client.get("/api/v1/status")
        print(f"   - Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   - Upload Directory: {data.get('upload_directory')}")
            print(f"   - Uploaded Files: {data.get('uploaded_files_count')}")
            print(f"   - Max Upload Size: {data.get('max_upload_size_mb')}MB")
            print("✅ Status endpoint working")
            return True
        else:
            print(f"❌ Status endpoint failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Status endpoint error: {e}")
        return False

def test_models_endpoint():
    """Test models endpoint"""
    print("\n🧪 Testing /models endpoint...")
    
    client = TestClient(app)
    
    try:
        response = client.get("/api/v1/models")
        print(f"   - Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   - Available Models: {data.get('available_models')}")
            print(f"   - Current Model: {data.get('current_model')}")
            print("✅ Models endpoint working")
            return True
        else:
            print(f"❌ Models endpoint failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Models endpoint error: {e}")
        return False

def test_query_endpoint():
    """Test query endpoint"""
    print("\n🧪 Testing /query endpoint...")
    
    client = TestClient(app)
    
    try:
        # Test valid query
        query_data = {
            "question": "What is machine learning?",
            "max_results": 3
        }
        
        response = client.post("/api/v1/query", json=query_data)
        print(f"   - Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   - Question: {data.get('question')}")
            print(f"   - Answer Length: {len(data.get('answer', ''))}")
            print(f"   - Sources: {len(data.get('sources', []))}")
            print(f"   - Processing Time: {data.get('processing_time')}s")
            print("✅ Query endpoint working")
            return True
        else:
            print(f"❌ Query endpoint failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Query endpoint error: {e}")
        return False

def test_query_validation():
    """Test query endpoint validation"""
    print("\n🧪 Testing query validation...")
    
    client = TestClient(app)
    
    # Test empty question
    try:
        query_data = {"question": "", "max_results": 5}
        response = client.post("/api/v1/query", json=query_data)
        
        if response.status_code == 422:  # Validation error
            print("✅ Empty question validation working")
        else:
            print(f"❌ Empty question should have failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Empty question test error: {e}")
        return False
    
    # Test invalid max_results
    try:
        query_data = {"question": "Test question", "max_results": 15}
        response = client.post("/api/v1/query", json=query_data)
        
        if response.status_code == 422:  # Validation error
            print("✅ Max results validation working")
        else:
            print(f"❌ Max results should have failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Max results test error: {e}")
        return False
    
    return True

def test_reset_endpoint():
    """Test reset endpoint"""
    print("\n🧪 Testing /reset endpoint...")
    
    client = TestClient(app)
    
    try:
        response = client.delete("/api/v1/reset")
        print(f"   - Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   - Message: {data.get('message')}")
            print(f"   - Vector Store Cleared: {data.get('details', {}).get('vector_store_cleared')}")
            print(f"   - Files Deleted: {data.get('details', {}).get('files_deleted')}")
            print("✅ Reset endpoint working")
            return True
        else:
            print(f"❌ Reset endpoint failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Reset endpoint error: {e}")
        return False

def test_upload_endpoint():
    """Test upload endpoint (without actual file)"""
    print("\n🧪 Testing /upload endpoint validation...")
    
    client = TestClient(app)
    
    try:
        # Test without file
        response = client.post("/api/v1/upload")
        print(f"   - Status Code (no file): {response.status_code}")
        
        if response.status_code == 422:  # Validation error
            print("✅ Upload validation working (no file)")
        else:
            print(f"❌ Upload should require file: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Upload test error: {e}")
        return False
    
    return True

def test_api_documentation():
    """Test API documentation endpoints"""
    print("\n🧪 Testing API documentation...")
    
    client = TestClient(app)
    
    try:
        # Test OpenAPI schema
        response = client.get("/openapi.json")
        print(f"   - OpenAPI Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ OpenAPI schema available")
        else:
            print(f"❌ OpenAPI schema failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ OpenAPI test error: {e}")
        return False
    
    return True

def main():
    """Run all API tests"""
    print("🚀 Testing FastAPI Routes")
    print("=" * 50)
    print("⚠ IMPORTANT: Make sure Ollama is running!")
    print("  - Start Ollama: ollama serve")
    print("  - Model should be available: ollama list")
    print("=" * 50)
    
    tests = [
        test_health_endpoint,
        test_status_endpoint,
        test_models_endpoint,
        test_query_endpoint,
        test_query_validation,
        test_reset_endpoint,
        test_upload_endpoint,
        test_api_documentation
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
        print("🎉 All API tests passed!")
        print("✅ FastAPI routes are working correctly")
        print("✅ Endpoint validation is functioning")
        print("✅ Error handling is working")
    else:
        print("❌ Some tests failed!")
        print("Please check:")
        print("1. Ollama is running: ollama serve")
        print("2. Model is available: ollama list")
        print("3. All services are properly configured")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
