#!/usr/bin/env python3
"""
ResearchMate RAG API Server Startup Script
"""

import sys
import os
import subprocess
import time

def check_ollama():
    """Check if Ollama is running"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama is running")
            return True
    except:
        pass
    
    print("❌ Ollama is not running")
    print("   Please start Ollama first:")
    print("   ollama serve")
    return False

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting ResearchMate RAG API Server")
    print("=" * 50)
    
    # Check Ollama
    if not check_ollama():
        print("\n⚠️  Please start Ollama first, then run this script again")
        return False
    
    print("\n📋 Server Information:")
    print("   - API Documentation: http://localhost:8000/docs")
    print("   - Health Check: http://localhost:8000/api/v1/health")
    print("   - Root Endpoint: http://localhost:8000/")
    print("\n🔄 Starting server...")
    print("   (Press Ctrl+C to stop)")
    print("=" * 50)
    
    try:
        # Start the server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    start_server()

