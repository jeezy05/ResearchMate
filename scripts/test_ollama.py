#!/usr/bin/env python3
"""
Test Ollama Connection
Verifies that Ollama is running and accessible
"""

import sys
import requests
from typing import Dict, Any


class Colors:
    """ANSI color codes"""
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color


def print_success(message: str):
    """Print success message in green"""
    print(f"{Colors.GREEN}✓ {message}{Colors.NC}")


def print_error(message: str):
    """Print error message in red"""
    print(f"{Colors.RED}✗ {message}{Colors.NC}")


def print_info(message: str):
    """Print info message in yellow"""
    print(f"{Colors.YELLOW}ℹ {message}{Colors.NC}")


def test_ollama_connection(base_url: str = "http://localhost:11434") -> bool:
    """
    Test connection to Ollama server
    
    Args:
        base_url: Ollama server URL
        
    Returns:
        True if connection successful, False otherwise
    """
    try:
        print_info(f"Testing connection to {base_url}...")
        response = requests.get(f"{base_url}/api/tags", timeout=5)
        response.raise_for_status()
        print_success("Successfully connected to Ollama")
        return True
    except requests.exceptions.ConnectionError:
        print_error("Could not connect to Ollama. Is it running?")
        return False
    except requests.exceptions.Timeout:
        print_error("Connection to Ollama timed out")
        return False
    except Exception as e:
        print_error(f"Error connecting to Ollama: {str(e)}")
        return False


def list_models(base_url: str = "http://localhost:11434") -> Dict[str, Any]:
    """
    List available models
    
    Args:
        base_url: Ollama server URL
        
    Returns:
        Dictionary with models information
    """
    try:
        response = requests.get(f"{base_url}/api/tags", timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print_error(f"Error listing models: {str(e)}")
        return {"models": []}


def test_embedding_generation(base_url: str = "http://localhost:11434") -> bool:
    """
    Test embedding generation
    
    Args:
        base_url: Ollama server URL
        
    Returns:
        True if successful, False otherwise
    """
    try:
        print_info("Testing embedding generation...")
        
        response = requests.post(
            f"{base_url}/api/embeddings",
            json={
                "model": "nomic-embed-text",
                "prompt": "This is a test"
            },
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        
        if "embedding" in result and len(result["embedding"]) > 0:
            print_success(f"Embedding generation successful (dimension: {len(result['embedding'])})")
            return True
        else:
            print_error("Embedding generation failed: no embedding in response")
            return False
            
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print_error("Model 'nomic-embed-text' not found. Please run: ollama pull nomic-embed-text")
        else:
            print_error(f"HTTP error during embedding test: {str(e)}")
        return False
    except Exception as e:
        print_error(f"Error testing embedding generation: {str(e)}")
        return False


def test_text_generation(base_url: str = "http://localhost:11434") -> bool:
    """
    Test text generation
    
    Args:
        base_url: Ollama server URL
        
    Returns:
        True if successful, False otherwise
    """
    try:
        print_info("Testing text generation...")
        
        response = requests.post(
            f"{base_url}/api/generate",
            json={
                "model": "llama2",
                "prompt": "Say hello in one word:",
                "stream": False
            },
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        
        if "response" in result and len(result["response"]) > 0:
            print_success(f"Text generation successful: '{result['response'].strip()[:50]}'")
            return True
        else:
            print_error("Text generation failed: no response")
            return False
            
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print_error("Model 'llama2' not found. Please run: ollama pull llama2")
        else:
            print_error(f"HTTP error during generation test: {str(e)}")
        return False
    except Exception as e:
        print_error(f"Error testing text generation: {str(e)}")
        return False


def main():
    """Main test function"""
    print("\n" + "=" * 50)
    print("  Ollama Connection Test")
    print("=" * 50 + "\n")
    
    base_url = "http://localhost:11434"
    
    # Test connection
    if not test_ollama_connection(base_url):
        print_error("\nOllama connection test failed!")
        print_info("\nMake sure Ollama is installed and running:")
        print_info("1. Install from https://ollama.ai")
        print_info("2. Run: ollama serve")
        sys.exit(1)
    
    print()
    
    # List available models
    print_info("Listing available models...")
    models_data = list_models(base_url)
    models = models_data.get("models", [])
    
    if models:
        print_success(f"Found {len(models)} model(s):")
        for model in models:
            print(f"  • {model.get('name', 'Unknown')}")
    else:
        print_error("No models found")
    
    print()
    
    # Check for required models
    required_models = ["llama2", "nomic-embed-text"]
    model_names = [m.get("name", "").split(":")[0] for m in models]
    
    missing_models = []
    for required in required_models:
        if not any(required in name for name in model_names):
            missing_models.append(required)
    
    if missing_models:
        print_error(f"Missing required models: {', '.join(missing_models)}")
        print_info("\nTo download missing models, run:")
        for model in missing_models:
            print(f"  ollama pull {model}")
        print()
    else:
        print_success("All required models are available")
        print()
    
    # Test embedding generation if model available
    if any("nomic-embed-text" in name for name in model_names):
        if not test_embedding_generation(base_url):
            sys.exit(1)
        print()
    
    # Test text generation if model available
    if any("llama2" in name for name in model_names):
        if not test_text_generation(base_url):
            sys.exit(1)
        print()
    
    print("=" * 50)
    print_success("All tests passed!")
    print("=" * 50 + "\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())


