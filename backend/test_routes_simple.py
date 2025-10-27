#!/usr/bin/env python3
"""
Simple test for FastAPI routes without TestClient
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.api.routes import router
from app.models.schemas import QueryRequest, UploadResponse, HealthResponse
import asyncio

def test_route_imports():
    """Test that routes can be imported and initialized"""
    print("🧪 Testing route imports...")
    
    try:
        # Test that router is properly initialized
        print(f"   - Router: {router}")
        print(f"   - Router routes: {len(router.routes)}")
        
        # List all routes
        for route in router.routes:
            if hasattr(route, 'path') and hasattr(route, 'methods'):
                print(f"   - {route.methods} {route.path}")
        
        print("✅ Route imports working")
        return True
        
    except Exception as e:
        print(f"❌ Route import error: {e}")
        return False

def test_schema_validation():
    """Test schema validation"""
    print("\n🧪 Testing schema validation...")
    
    try:
        # Test QueryRequest validation
        valid_request = QueryRequest(
            question="What is machine learning?",
            max_results=5
        )
        print(f"   - Valid QueryRequest: {valid_request.question}")
        
        # Test UploadResponse validation
        valid_upload = UploadResponse(
            filename="test.pdf",
            total_chunks=5,
            message="Success",
            status="success"
        )
        print(f"   - Valid UploadResponse: {valid_upload.filename}")
        
        # Test HealthResponse validation
        valid_health = HealthResponse(
            status="healthy",
            ollama_connected=True,
            vector_store_ready=True,
            model="llama2"
        )
        print(f"   - Valid HealthResponse: {valid_health.status}")
        
        print("✅ Schema validation working")
        return True
        
    except Exception as e:
        print(f"❌ Schema validation error: {e}")
        return False

def test_dependency_injection():
    """Test dependency injection functions"""
    print("\n🧪 Testing dependency injection...")
    
    try:
        from app.api.routes import (
            get_document_service, get_vector_store_service,
            get_llm_service, get_rag_service
        )
        
        # Test that dependency functions exist
        print(f"   - get_document_service: {get_document_service}")
        print(f"   - get_vector_store_service: {get_vector_store_service}")
        print(f"   - get_llm_service: {get_llm_service}")
        print(f"   - get_rag_service: {get_rag_service}")
        
        print("✅ Dependency injection working")
        return True
        
    except Exception as e:
        print(f"❌ Dependency injection error: {e}")
        return False

def test_route_definitions():
    """Test that all required routes are defined"""
    print("\n🧪 Testing route definitions...")
    
    try:
        required_routes = [
            ("POST", "/upload"),
            ("POST", "/query"),
            ("GET", "/health"),
            ("DELETE", "/reset"),
            ("GET", "/status"),
            ("GET", "/models")
        ]
        
        found_routes = []
        for route in router.routes:
            if hasattr(route, 'path') and hasattr(route, 'methods'):
                for method in route.methods:
                    if method != 'HEAD':  # Skip HEAD methods
                        found_routes.append((method, route.path))
        
        print(f"   - Found {len(found_routes)} routes:")
        for method, path in found_routes:
            print(f"     {method} {path}")
        
        # Check for required routes
        missing_routes = []
        for required_method, required_path in required_routes:
            if (required_method, required_path) not in found_routes:
                missing_routes.append((required_method, required_path))
        
        if missing_routes:
            print(f"❌ Missing routes: {missing_routes}")
            return False
        else:
            print("✅ All required routes found")
            return True
            
    except Exception as e:
        print(f"❌ Route definition error: {e}")
        return False

def test_error_handling():
    """Test error handling in schemas"""
    print("\n🧪 Testing error handling...")
    
    try:
        # Test invalid QueryRequest
        try:
            invalid_request = QueryRequest(question="", max_results=15)
            print("❌ Should have failed with invalid request")
            return False
        except Exception as e:
            print(f"   - Invalid QueryRequest correctly rejected: {type(e).__name__}")
        
        # Test invalid UploadResponse
        try:
            invalid_upload = UploadResponse(
                filename="test.pdf",
                total_chunks=-1,  # Invalid
                message="Success",
                status="invalid_status"  # Invalid
            )
            print("❌ Should have failed with invalid upload")
            return False
        except Exception as e:
            print(f"   - Invalid UploadResponse correctly rejected: {type(e).__name__}")
        
        print("✅ Error handling working")
        return True
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False

def main():
    """Run all simple tests"""
    print("🚀 Testing FastAPI Routes (Simple)")
    print("=" * 50)
    
    tests = [
        test_route_imports,
        test_schema_validation,
        test_dependency_injection,
        test_route_definitions,
        test_error_handling
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
        print("🎉 All route tests passed!")
        print("✅ FastAPI routes are properly defined")
        print("✅ Schema validation is working")
        print("✅ Dependency injection is set up")
        print("✅ Error handling is functioning")
    else:
        print("❌ Some tests failed!")
        print("Please check the route definitions and imports")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())

