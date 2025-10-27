#!/usr/bin/env python3
"""
Test Document Processor
Demonstrates the DocumentProcessor class functionality
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.document_service import DocumentProcessor
from app.core.config import settings


def test_document_processor():
    """Test the DocumentProcessor class"""
    
    print("=" * 70)
    print("Testing DocumentProcessor Class")
    print("=" * 70)
    print()
    
    # Initialize processor
    print("1. Initializing DocumentProcessor...")
    processor = DocumentProcessor(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP
    )
    print(f"   ✓ Initialized with chunk_size={processor.chunk_size}, "
          f"chunk_overlap={processor.chunk_overlap}")
    print()
    
    # Test text chunking
    print("2. Testing chunk_text() method...")
    sample_text = """
    This is a sample document for testing the chunking functionality.
    
    It contains multiple paragraphs to demonstrate how the RecursiveCharacterTextSplitter
    works with the LangChain library.
    
    The splitter should intelligently break the text at natural boundaries like
    paragraphs, sentences, and words.
    
    Each chunk will have some overlap to maintain context between chunks.
    """ * 10  # Repeat to create enough text for multiple chunks
    
    try:
        chunks = processor.chunk_text(sample_text)
        print(f"   ✓ Created {len(chunks)} chunks from {len(sample_text)} characters")
        print(f"   ✓ First chunk length: {len(chunks[0])}")
        print(f"   ✓ First chunk preview: {chunks[0][:100]}...")
        print()
    except Exception as e:
        print(f"   ✗ Error: {e}")
        print()
    
    # Test empty text handling
    print("3. Testing error handling with empty text...")
    try:
        processor.chunk_text("")
        print("   ✗ Should have raised ValueError")
    except ValueError as e:
        print(f"   ✓ Correctly raised ValueError: {e}")
    print()
    
    # Test PDF extraction (if a sample PDF exists)
    print("4. Testing extract_text_from_pdf() method...")
    sample_pdf_path = "sample.pdf"
    
    if os.path.exists(sample_pdf_path):
        try:
            text = processor.extract_text_from_pdf(sample_pdf_path)
            print(f"   ✓ Extracted {len(text)} characters from PDF")
            print(f"   ✓ Text preview: {text[:200]}...")
            print()
        except Exception as e:
            print(f"   ✗ Error: {e}")
            print()
    else:
        print(f"   ⚠ Skipped (no sample.pdf found in current directory)")
        print()
    
    # Test process_document full pipeline
    print("5. Testing process_document() method...")
    if os.path.exists(sample_pdf_path):
        try:
            result = processor.process_document(sample_pdf_path, "sample.pdf")
            print(f"   ✓ Document processed successfully!")
            print(f"   ✓ Filename: {result['filename']}")
            print(f"   ✓ Total chunks: {result['total_chunks']}")
            print(f"   ✓ Text length: {result['text_length']}")
            print(f"   ✓ Processing time: {result['processing_time_seconds']:.2f}s")
            print(f"   ✓ Timestamp: {result['timestamp']}")
            print()
        except Exception as e:
            print(f"   ✗ Error: {e}")
            print()
    else:
        print(f"   ⚠ Skipped (no sample.pdf found)")
        print()
    
    # Test with custom chunk parameters
    print("6. Testing chunk_text() with custom parameters...")
    try:
        custom_chunks = processor.chunk_text(
            sample_text,
            chunk_size=500,
            chunk_overlap=50
        )
        print(f"   ✓ Created {len(custom_chunks)} chunks with custom settings")
        print(f"   ✓ Chunk size: 500, overlap: 50")
        print()
    except Exception as e:
        print(f"   ✗ Error: {e}")
        print()
    
    print("=" * 70)
    print("✓ DocumentProcessor testing complete!")
    print("=" * 70)
    print()
    
    # Print usage examples
    print_usage_examples()


def print_usage_examples():
    """Print usage examples"""
    print("\n" + "=" * 70)
    print("Usage Examples")
    print("=" * 70)
    print()
    
    print("Example 1: Basic Usage")
    print("-" * 70)
    print("""
from app.services.document_service import DocumentProcessor

# Initialize processor
processor = DocumentProcessor()

# Extract text from PDF
text = processor.extract_text_from_pdf("document.pdf")

# Chunk the text
chunks = processor.chunk_text(text)

print(f"Created {len(chunks)} chunks")
    """)
    print()
    
    print("Example 2: Full Pipeline")
    print("-" * 70)
    print("""
from app.services.document_service import DocumentProcessor

# Initialize processor with custom settings
processor = DocumentProcessor(chunk_size=1500, chunk_overlap=300)

# Process entire document
result = processor.process_document(
    file_path="research_paper.pdf",
    filename="research_paper.pdf"
)

print(f"Filename: {result['filename']}")
print(f"Total chunks: {result['total_chunks']}")
print(f"Text length: {result['text_length']}")
print(f"Processing time: {result['processing_time_seconds']:.2f}s")

# Access the chunks
for i, chunk in enumerate(result['chunks']):
    print(f"Chunk {i}: {chunk[:50]}...")
    """)
    print()
    
    print("Example 3: Custom Chunk Parameters")
    print("-" * 70)
    print("""
from app.services.document_service import DocumentProcessor

processor = DocumentProcessor()

# Extract text
text = processor.extract_text_from_pdf("document.pdf")

# Create chunks with custom parameters
small_chunks = processor.chunk_text(text, chunk_size=500, chunk_overlap=100)
large_chunks = processor.chunk_text(text, chunk_size=2000, chunk_overlap=400)

print(f"Small chunks: {len(small_chunks)}")
print(f"Large chunks: {len(large_chunks)}")
    """)
    print()


def main():
    """Main function"""
    try:
        test_document_processor()
        return 0
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

