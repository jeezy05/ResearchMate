#!/usr/bin/env python3
"""
ResearchMate Frontend Test Suite
"""

import sys
import os
import time
import requests
import subprocess
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all required modules can be imported"""
    print("=" * 60)
    print("Test 1: Import Dependencies")
    print("=" * 60)
    
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
        print(f"   Version: {st.__version__}")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import requests
        print("✅ Requests imported successfully")
        print(f"   Version: {requests.__version__}")
    except ImportError as e:
        print(f"❌ Requests import failed: {e}")
        return False
    
    try:
        from datetime import datetime
        print("✅ Datetime imported successfully")
    except ImportError as e:
        print(f"❌ Datetime import failed: {e}")
        return False
    
    try:
        from typing import Optional, Dict, Any
        print("✅ Typing imported successfully")
    except ImportError as e:
        print(f"❌ Typing import failed: {e}")
        return False
    
    return True

def test_app_structure():
    """Test if the app.py file has the correct structure"""
    print("\n" + "=" * 60)
    print("Test 2: App Structure")
    print("=" * 60)
    
    app_file = Path("app.py")
    if not app_file.exists():
        print("❌ app.py file not found")
        return False
    
    print("✅ app.py file exists")
    
    # Read the file content
    with open(app_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for required functions
    required_functions = [
        "init_session_state",
        "check_api_health", 
        "upload_document",
        "query_documents",
        "reset_database",
        "render_sidebar",
        "render_main_interface",
        "main"
    ]
    
    for func in required_functions:
        if f"def {func}(" in content:
            print(f"✅ Function {func} found")
        else:
            print(f"❌ Function {func} not found")
            return False
    
    # Check for required imports
    required_imports = [
        "import streamlit as st",
        "import requests",
        "import os",
        "import time",
        "from datetime import datetime",
        "from typing import Optional, Dict, Any"
    ]
    
    for imp in required_imports:
        if imp in content:
            print(f"✅ Import {imp.split()[-1]} found")
        else:
            print(f"❌ Import {imp.split()[-1]} not found")
            return False
    
    # Check for page config
    if "st.set_page_config" in content:
        print("✅ Page configuration found")
    else:
        print("❌ Page configuration not found")
        return False
    
    # Check for custom CSS
    if "Custom CSS" in content or "st.markdown" in content:
        print("✅ Custom CSS styling found")
    else:
        print("❌ Custom CSS styling not found")
        return False
    
    return True

def test_api_endpoints():
    """Test if the API endpoints are correctly configured"""
    print("\n" + "=" * 60)
    print("Test 3: API Endpoint Configuration")
    print("=" * 60)
    
    app_file = Path("app.py")
    with open(app_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for API configuration
    if "API_BASE_URL" in content:
        print("✅ API_BASE_URL configuration found")
    else:
        print("❌ API_BASE_URL configuration not found")
        return False
    
    if "API_V1_URL" in content:
        print("✅ API_V1_URL configuration found")
    else:
        print("❌ API_V1_URL configuration not found")
        return False
    
    # Check for endpoint usage
    endpoints = [
        "/api/v1/upload",
        "/api/v1/query", 
        "/api/v1/health",
        "/api/v1/reset"
    ]
    
    for endpoint in endpoints:
        if endpoint in content:
            print(f"✅ Endpoint {endpoint} found")
        else:
            print(f"❌ Endpoint {endpoint} not found")
            return False
    
    return True

def test_ui_components():
    """Test if UI components are properly defined"""
    print("\n" + "=" * 60)
    print("Test 4: UI Components")
    print("=" * 60)
    
    app_file = Path("app.py")
    with open(app_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for sidebar components
    sidebar_components = [
        "st.sidebar",
        "file_uploader",
        "text_input",
        "button"
    ]
    
    for component in sidebar_components:
        if component in content:
            print(f"✅ Sidebar component {component} found")
        else:
            print(f"❌ Sidebar component {component} not found")
            return False
    
    # Check for main interface components
    main_components = [
        "st.chat_message",
        "st.text_area",
        "st.selectbox",
        "st.expander"
    ]
    
    for component in main_components:
        if component in content:
            print(f"✅ Main component {component} found")
        else:
            print(f"❌ Main component {component} not found")
            return False
    
    # Check for session state usage
    if "st.session_state" in content:
        print("✅ Session state usage found")
    else:
        print("❌ Session state usage not found")
        return False
    
    return True

def test_error_handling():
    """Test if error handling is implemented"""
    print("\n" + "=" * 60)
    print("Test 5: Error Handling")
    print("=" * 60)
    
    app_file = Path("app.py")
    with open(app_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for try-except blocks
    if "try:" in content and "except" in content:
        print("✅ Try-except blocks found")
    else:
        print("❌ Try-except blocks not found")
        return False
    
    # Check for error messages
    error_indicators = [
        "st.error",
        "st.warning",
        "st.success",
        "st.info"
    ]
    
    for indicator in error_indicators:
        if indicator in content:
            print(f"✅ {indicator} usage found")
        else:
            print(f"❌ {indicator} usage not found")
            return False
    
    return True

def test_backend_connection():
    """Test if the backend is accessible"""
    print("\n" + "=" * 60)
    print("Test 6: Backend Connection")
    print("=" * 60)
    
    try:
        # Test simple health endpoint
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend health endpoint accessible")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Backend health endpoint returned {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend")
        print("   Please start the backend first:")
        print("   cd backend")
        print("   python -m uvicorn app.main:app --reload")
        return False
    except Exception as e:
        print(f"❌ Backend connection error: {e}")
        return False
    
    try:
        # Test detailed health endpoint
        response = requests.get("http://localhost:8000/api/v1/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend detailed health endpoint accessible")
            health_data = response.json()
            print(f"   Status: {health_data.get('status', 'unknown')}")
            print(f"   Ollama: {health_data.get('ollama_connected', False)}")
            print(f"   Vector Store: {health_data.get('vector_store_ready', False)}")
            print(f"   Model: {health_data.get('model', 'unknown')}")
        else:
            print(f"❌ Backend detailed health endpoint returned {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend detailed health error: {e}")
        return False
    
    return True

def test_streamlit_syntax():
    """Test if the Streamlit app has valid syntax"""
    print("\n" + "=" * 60)
    print("Test 7: Streamlit Syntax Validation")
    print("=" * 60)
    
    try:
        # Try to compile the app
        with open("app.py", 'r', encoding='utf-8') as f:
            code = f.read()
        
        compile(code, "app.py", "exec")
        print("✅ Python syntax is valid")
    except SyntaxError as e:
        print(f"❌ Python syntax error: {e}")
        return False
    except Exception as e:
        print(f"❌ Syntax validation error: {e}")
        return False
    
    return True

def test_requirements():
    """Test if all requirements are met"""
    print("\n" + "=" * 60)
    print("Test 8: Requirements Check")
    print("=" * 60)
    
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("❌ requirements.txt not found")
        return False
    
    print("✅ requirements.txt found")
    
    # Check if requirements are installed
    try:
        import streamlit
        print(f"✅ Streamlit {streamlit.__version__} installed")
    except ImportError:
        print("❌ Streamlit not installed")
        return False
    
    try:
        import requests
        print(f"✅ Requests {requests.__version__} installed")
    except ImportError:
        print("❌ Requests not installed")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🧪 ResearchMate Frontend Test Suite")
    print("=" * 60)
    
    tests = [
        ("Import Dependencies", test_imports),
        ("App Structure", test_app_structure),
        ("API Endpoints", test_api_endpoints),
        ("UI Components", test_ui_components),
        ("Error Handling", test_error_handling),
        ("Backend Connection", test_backend_connection),
        ("Streamlit Syntax", test_streamlit_syntax),
        ("Requirements", test_requirements)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 All tests passed! Frontend is ready to use.")
        print("\n🚀 To start the frontend:")
        print("   python start_frontend.py")
        print("   or")
        print("   streamlit run app.py")
    else:
        print("⚠️ Some tests failed. Please fix the issues above.")
    
    return passed == total

if __name__ == "__main__":
    main()

