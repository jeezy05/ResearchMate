#!/usr/bin/env python3
"""
ResearchMate Frontend Startup Script
"""

import subprocess
import sys
import os
import time
import requests

def check_backend():
    """Check if the backend is running"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def start_frontend():
    """Start the Streamlit frontend"""
    print("🚀 Starting ResearchMate Frontend")
    print("=" * 50)
    
    # Check if backend is running
    print("🔍 Checking backend connection...")
    if check_backend():
        print("✅ Backend is running")
    else:
        print("⚠️ Backend is not running")
        print("   Please start the backend first:")
        print("   cd backend")
        print("   python -m uvicorn app.main:app --reload")
        print("   or")
        print("   python start_server.py")
        print()
        print("   Then run this script again.")
        return False
    
    print("\n📋 Frontend Information:")
    print("   - URL: http://localhost:8501")
    print("   - Backend: http://localhost:8000")
    print("   - API Docs: http://localhost:8000/docs")
    print("\n🔄 Starting Streamlit...")
    print("   (Press Ctrl+C to stop)")
    print("=" * 50)
    
    try:
        # Start Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Frontend stopped by user")
    except Exception as e:
        print(f"\n❌ Frontend error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    start_frontend()

