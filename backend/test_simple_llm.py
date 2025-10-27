#!/usr/bin/env python3
"""
Simple LLM Test - Tests Ollama connection without RAG
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.llm_service import LLMService
from app.core.config import settings

def test_simple_llm():
    """Test basic LLM functionality without RAG"""
    print("=" * 70)
    print("Simple LLM Test")
    print("=" * 70)
    
    try:
        # Initialize LLM service
        print("🔧 Initializing LLM service...")
        llm_service = LLMService()
        print(f"✅ LLM service initialized")
        print(f"   - Model: {settings.OLLAMA_MODEL}")
        print(f"   - Base URL: {settings.OLLAMA_BASE_URL}")
        
        # Test connection
        print("\n🔍 Testing Ollama connection...")
        if llm_service.check_connection():
            print("✅ Ollama is accessible")
        else:
            print("❌ Ollama connection failed")
            return False
            
        # Test available models
        print("\n📋 Checking available models...")
        models = llm_service.get_available_models()
        print(f"✅ Found {len(models)} model(s):")
        for model in models:
            print(f"   - {model}")
            
        # Test simple generation (without RAG)
        print("\n🤖 Testing simple text generation...")
        print("Query: 'What is machine learning?'")
        print("-" * 50)
        
        # Test the LLM directly
        test_prompt = "What is machine learning? Please give a brief explanation."
        
        # Use the LLM directly without RAG chain
        response = llm_service.llm.invoke(test_prompt)
        print(f"Response: {response}")
        print("-" * 50)
        
        print("✅ Simple LLM test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🚀 Starting Simple LLM Test")
    print("=" * 70)
    print("⚠ IMPORTANT: Make sure Ollama is running!")
    print(f"  - URL: {settings.OLLAMA_BASE_URL}")
    print(f"  - Model: {settings.OLLAMA_MODEL}")
    print("")
    print("Start Ollama: ollama serve")
    print(f"Pull model: ollama pull {settings.OLLAMA_MODEL}")
    print("=" * 70)
    
    success = test_simple_llm()
    
    if success:
        print("\n🎉 All tests passed!")
        print("✅ Ollama is working correctly")
        print("✅ LLM service is functional")
        print("✅ Model is responding to queries")
    else:
        print("\n❌ Tests failed!")
        print("Please check:")
        print("1. Ollama is running: ollama serve")
        print(f"2. Model is installed: ollama pull {settings.OLLAMA_MODEL}")
        print("3. Ollama is accessible at the configured URL")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())

