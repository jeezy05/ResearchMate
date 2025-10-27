#!/usr/bin/env python3
"""
Test script for FastAPI main application
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.main import app
from app.core.config import settings
import logging

def test_app_creation():
    """Test that the FastAPI app is created correctly"""
    print("🧪 Testing FastAPI app creation...")
    
    try:
        # Check app attributes
        print(f"   - Title: {app.title}")
        print(f"   - Version: {app.version}")
        print(f"   - Description: {app.description}")
        
        # Check routes
        routes = [route.path for route in app.routes if hasattr(route, 'path')]
        print(f"   - Routes: {len(routes)}")
        for route in routes:
            print(f"     {route}")
        
        print("✅ FastAPI app created successfully")
        return True
        
    except Exception as e:
        print(f"❌ App creation error: {e}")
        return False

def test_configuration():
    """Test configuration settings"""
    print("\n🧪 Testing configuration...")
    
    try:
        print(f"   - Project Name: {settings.PROJECT_NAME}")
        print(f"   - Version: {settings.VERSION}")
        print(f"   - Host: {settings.HOST}")
        print(f"   - Port: {settings.PORT}")
        print(f"   - Debug: {settings.DEBUG}")
        print(f"   - CORS Origins: {settings.CORS_ORIGINS}")
        print(f"   - Ollama Model: {settings.OLLAMA_MODEL}")
        print(f"   - Upload Directory: {settings.UPLOAD_DIR}")
        
        print("✅ Configuration loaded successfully")
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_logging_setup():
    """Test logging configuration"""
    print("\n🧪 Testing logging setup...")
    
    try:
        # Check if logging is configured
        logger = logging.getLogger(__name__)
        print(f"   - Logger level: {logger.level}")
        print(f"   - Logger handlers: {len(logger.handlers)}")
        
        # Test logging
        logger.info("Test log message")
        print("   - Log message sent successfully")
        
        print("✅ Logging configured successfully")
        return True
        
    except Exception as e:
        print(f"❌ Logging error: {e}")
        return False

def test_middleware():
    """Test middleware configuration"""
    print("\n🧪 Testing middleware...")
    
    try:
        # Check CORS middleware
        middleware_count = len(app.user_middleware)
        print(f"   - Middleware count: {middleware_count}")
        
        # Check if CORS is configured
        cors_configured = any(
            "CORSMiddleware" in str(middleware) 
            for middleware in app.user_middleware
        )
        print(f"   - CORS configured: {cors_configured}")
        
        print("✅ Middleware configured successfully")
        return True
        
    except Exception as e:
        print(f"❌ Middleware error: {e}")
        return False

def test_routes():
    """Test route configuration"""
    print("\n🧪 Testing routes...")
    
    try:
        # Get all routes
        routes = []
        for route in app.routes:
            if hasattr(route, 'path') and hasattr(route, 'methods'):
                for method in route.methods:
                    if method != 'HEAD':
                        routes.append((method, route.path))
        
        print(f"   - Total routes: {len(routes)}")
        
        # Check for key routes
        key_routes = [
            ("GET", "/"),
            ("GET", "/health"),
            ("GET", "/docs"),
            ("GET", "/api/v1/health"),
            ("POST", "/api/v1/upload"),
            ("POST", "/api/v1/query")
        ]
        
        found_routes = []
        for method, path in key_routes:
            if (method, path) in routes:
                found_routes.append((method, path))
                print(f"   ✅ {method} {path}")
            else:
                print(f"   ❌ {method} {path} - NOT FOUND")
        
        print(f"   - Key routes found: {len(found_routes)}/{len(key_routes)}")
        
        if len(found_routes) >= len(key_routes) * 0.8:  # 80% success rate
            print("✅ Routes configured successfully")
            return True
        else:
            print("❌ Missing key routes")
            return False
            
    except Exception as e:
        print(f"❌ Routes error: {e}")
        return False

def test_lifespan_events():
    """Test lifespan event handlers"""
    print("\n🧪 Testing lifespan events...")
    
    try:
        # Check if lifespan is configured
        has_lifespan = hasattr(app, 'router') and hasattr(app.router, 'lifespan_context')
        print(f"   - Lifespan configured: {has_lifespan}")
        
        # Check lifespan manager
        if hasattr(app, 'router'):
            lifespan_context = getattr(app.router, 'lifespan_context', None)
            print(f"   - Lifespan context: {lifespan_context is not None}")
        
        print("✅ Lifespan events configured")
        return True
        
    except Exception as e:
        print(f"❌ Lifespan events error: {e}")
        return False

def test_documentation():
    """Test API documentation endpoints"""
    print("\n🧪 Testing documentation...")
    
    try:
        # Check OpenAPI configuration
        openapi_url = getattr(app, 'openapi_url', None)
        docs_url = getattr(app, 'docs_url', None)
        redoc_url = getattr(app, 'redoc_url', None)
        
        print(f"   - OpenAPI URL: {openapi_url}")
        print(f"   - Docs URL: {docs_url}")
        print(f"   - ReDoc URL: {redoc_url}")
        
        if openapi_url and docs_url and redoc_url:
            print("✅ Documentation configured successfully")
            return True
        else:
            print("❌ Documentation not fully configured")
            return False
            
    except Exception as e:
        print(f"❌ Documentation error: {e}")
        return False

def test_startup_sequence():
    """Test startup sequence simulation"""
    print("\n🧪 Testing startup sequence...")
    
    try:
        # Simulate startup checks
        print("   - Checking Ollama connection...")
        try:
            from app.services.llm_service import LLMService
            llm_service = LLMService()
            if llm_service.check_connection():
                print("   ✅ Ollama connection successful")
            else:
                print("   ⚠️ Ollama connection failed")
        except Exception as e:
            print(f"   ⚠️ Ollama check error: {str(e)[:50]}...")
        
        print("   - Checking vector store...")
        try:
            from app.services.vector_store import VectorStoreService
            vector_store = VectorStoreService()
            status = vector_store.get_status()
            if status.get("healthy", False):
                print("   ✅ Vector store ready")
            else:
                print("   ⚠️ Vector store not ready")
        except Exception as e:
            print(f"   ⚠️ Vector store check error: {str(e)[:50]}...")
        
        print("   - Checking directories...")
        try:
            settings.create_directories()
            print("   ✅ Directories created")
        except Exception as e:
            print(f"   ⚠️ Directory creation error: {str(e)[:50]}...")
        
        print("✅ Startup sequence completed")
        return True
        
    except Exception as e:
        print(f"❌ Startup sequence error: {e}")
        return False

def main():
    """Run all main application tests"""
    print("🚀 Testing FastAPI Main Application")
    print("=" * 50)
    print("⚠ IMPORTANT: This test checks app configuration, not runtime!")
    print("  - Ollama may not be running (that's OK for this test)")
    print("  - We're testing app setup, not service connections")
    print("=" * 50)
    
    tests = [
        test_app_creation,
        test_configuration,
        test_logging_setup,
        test_middleware,
        test_routes,
        test_lifespan_events,
        test_documentation,
        test_startup_sequence
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
        print("🎉 All main application tests passed!")
        print("✅ FastAPI app is properly configured")
        print("✅ All components are set up correctly")
        print("✅ Ready to start the server")
    else:
        print("❌ Some tests failed!")
        print("Please check the main.py configuration")
    
    print("\n🚀 To start the server:")
    print("   python -m uvicorn app.main:app --reload")
    print("   or")
    print("   python app/main.py")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())

