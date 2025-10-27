#!/usr/bin/env python3
"""
Test Configuration Settings
Demonstrates the settings validation and loading
"""

from app.core.config import Settings
from pydantic import ValidationError


def test_default_settings():
    """Test default settings load correctly"""
    print("=" * 60)
    print("Testing Default Settings")
    print("=" * 60)
    
    settings = Settings()
    
    print(f"✓ OLLAMA_BASE_URL: {settings.OLLAMA_BASE_URL}")
    print(f"✓ OLLAMA_MODEL: {settings.OLLAMA_MODEL}")
    print(f"✓ EMBEDDING_MODEL: {settings.EMBEDDING_MODEL}")
    print(f"✓ CHROMA_PERSIST_DIRECTORY: {settings.CHROMA_PERSIST_DIRECTORY}")
    print(f"✓ CHUNK_SIZE: {settings.CHUNK_SIZE}")
    print(f"✓ CHUNK_OVERLAP: {settings.CHUNK_OVERLAP}")
    print(f"✓ TOP_K_RETRIEVAL: {settings.TOP_K_RETRIEVAL}")
    print(f"✓ MAX_UPLOAD_SIZE_MB: {settings.MAX_UPLOAD_SIZE_MB}")
    print(f"✓ CORS_ORIGINS: {settings.CORS_ORIGINS}")
    print()


def test_validation_errors():
    """Test that validation catches invalid configurations"""
    print("=" * 60)
    print("Testing Validation Errors")
    print("=" * 60)
    
    # Test invalid Ollama URL
    try:
        Settings(OLLAMA_BASE_URL="invalid-url")
        print("✗ Should have failed for invalid OLLAMA_BASE_URL")
    except ValidationError as e:
        print("✓ Correctly rejected invalid OLLAMA_BASE_URL")
        print(f"  Error: {e.errors()[0]['msg']}")
    
    # Test chunk overlap >= chunk size
    try:
        Settings(CHUNK_SIZE=100, CHUNK_OVERLAP=100)
        print("✗ Should have failed for CHUNK_OVERLAP >= CHUNK_SIZE")
    except ValidationError as e:
        print("✓ Correctly rejected CHUNK_OVERLAP >= CHUNK_SIZE")
        print(f"  Error: {e.errors()[0]['msg']}")
    
    # Test empty CORS origins
    try:
        Settings(CORS_ORIGINS=[])
        print("✗ Should have failed for empty CORS_ORIGINS")
    except ValidationError as e:
        print("✓ Correctly rejected empty CORS_ORIGINS")
        print(f"  Error: {e.errors()[0]['msg']}")
    
    # Test invalid CORS origin
    try:
        Settings(CORS_ORIGINS=["invalid-origin"])
        print("✗ Should have failed for invalid CORS_ORIGINS")
    except ValidationError as e:
        print("✓ Correctly rejected invalid CORS_ORIGINS")
        print(f"  Error: {e.errors()[0]['msg']}")
    
    # Test invalid port
    try:
        Settings(PORT=70000)
        print("✗ Should have failed for invalid PORT")
    except ValidationError as e:
        print("✓ Correctly rejected invalid PORT")
        print(f"  Error: {e.errors()[0]['msg']}")
    
    # Test invalid chunk size
    try:
        Settings(CHUNK_SIZE=50)
        print("✗ Should have failed for CHUNK_SIZE < 100")
    except ValidationError as e:
        print("✓ Correctly rejected CHUNK_SIZE < 100")
        print(f"  Error: {e.errors()[0]['msg']}")
    
    print()


def test_environment_override():
    """Test that environment variables override defaults"""
    print("=" * 60)
    print("Testing Environment Variable Override")
    print("=" * 60)
    
    import os
    
    # Set environment variables
    os.environ["OLLAMA_MODEL"] = "llama3.1"
    os.environ["CHUNK_SIZE"] = "1500"
    os.environ["TOP_K_RETRIEVAL"] = "10"
    
    # Reload settings
    settings = Settings()
    
    assert settings.OLLAMA_MODEL == "llama3.1", "ENV override failed for OLLAMA_MODEL"
    assert settings.CHUNK_SIZE == 1500, "ENV override failed for CHUNK_SIZE"
    assert settings.TOP_K_RETRIEVAL == 10, "ENV override failed for TOP_K_RETRIEVAL"
    
    print("✓ Environment variables correctly override defaults")
    print(f"  OLLAMA_MODEL: {settings.OLLAMA_MODEL}")
    print(f"  CHUNK_SIZE: {settings.CHUNK_SIZE}")
    print(f"  TOP_K_RETRIEVAL: {settings.TOP_K_RETRIEVAL}")
    
    # Clean up
    del os.environ["OLLAMA_MODEL"]
    del os.environ["CHUNK_SIZE"]
    del os.environ["TOP_K_RETRIEVAL"]
    
    print()


def test_directory_creation():
    """Test that directories are created automatically"""
    print("=" * 60)
    print("Testing Automatic Directory Creation")
    print("=" * 60)
    
    import os
    import tempfile
    import shutil
    
    # Create temporary directory for testing
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Create settings with custom directories
        chroma_dir = os.path.join(temp_dir, "chroma_test")
        upload_dir = os.path.join(temp_dir, "uploads_test")
        
        settings = Settings(
            CHROMA_PERSIST_DIRECTORY=chroma_dir,
            UPLOAD_DIR=upload_dir
        )
        
        # Directories should be created automatically
        assert os.path.exists(chroma_dir), "CHROMA_PERSIST_DIRECTORY not created"
        assert os.path.exists(upload_dir), "UPLOAD_DIR not created"
        
        print(f"✓ Directories created automatically:")
        print(f"  {chroma_dir}")
        print(f"  {upload_dir}")
        
    finally:
        # Clean up
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    print()


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("ResearchMate Configuration Test Suite")
    print("=" * 60 + "\n")
    
    try:
        test_default_settings()
        test_validation_errors()
        test_environment_override()
        test_directory_creation()
        
        print("=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())


