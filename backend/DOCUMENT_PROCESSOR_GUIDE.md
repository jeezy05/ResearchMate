# DocumentProcessor Guide

## Overview

The `DocumentProcessor` class provides robust document processing functionality for the ResearchMate RAG application. It handles PDF text extraction and intelligent text chunking using industry-standard libraries.

## Location

```python
from app.services.document_service import DocumentProcessor
```

## Key Technologies

- **pypdf** - Modern PDF text extraction (version 3.17.0)
- **LangChain RecursiveCharacterTextSplitter** - Intelligent text chunking

## Class: DocumentProcessor

### Initialization

```python
processor = DocumentProcessor(
    chunk_size: int = None,      # Defaults to settings.CHUNK_SIZE (1000)
    chunk_overlap: int = None    # Defaults to settings.CHUNK_OVERLAP (200)
)
```

**Parameters:**
- `chunk_size`: Size of text chunks in characters
- `chunk_overlap`: Number of overlapping characters between chunks

**Example:**
```python
# Use default settings
processor = DocumentProcessor()

# Custom settings
processor = DocumentProcessor(chunk_size=1500, chunk_overlap=300)
```

---

## Methods

### 1. extract_text_from_pdf()

Extract all text content from a PDF file.

**Signature:**
```python
def extract_text_from_pdf(self, file_path: str) -> str
```

**Parameters:**
- `file_path` (str): Path to the PDF file

**Returns:**
- `str`: Extracted text content

**Raises:**
- `FileNotFoundError`: If the PDF file doesn't exist
- `Exception`: For PDF reading errors

**Features:**
- ✓ Page-by-page extraction
- ✓ Graceful error handling for corrupted pages
- ✓ Detailed logging of extraction progress
- ✓ Empty page detection

**Example:**
```python
processor = DocumentProcessor()

# Extract text from PDF
text = processor.extract_text_from_pdf("research_paper.pdf")

print(f"Extracted {len(text)} characters")
```

**Error Handling:**
```python
try:
    text = processor.extract_text_from_pdf("document.pdf")
except FileNotFoundError:
    print("File not found!")
except Exception as e:
    print(f"Error extracting PDF: {e}")
```

---

### 2. chunk_text()

Split text into chunks using LangChain's RecursiveCharacterTextSplitter.

**Signature:**
```python
def chunk_text(
    self,
    text: str,
    chunk_size: int = None,
    chunk_overlap: int = None
) -> List[str]
```

**Parameters:**
- `text` (str): Text to split into chunks
- `chunk_size` (int, optional): Override default chunk size
- `chunk_overlap` (int, optional): Override default chunk overlap

**Returns:**
- `List[str]`: List of text chunks

**Raises:**
- `ValueError`: If text is empty
- `Exception`: For chunking errors

**Features:**
- ✓ Intelligent splitting at natural boundaries (paragraphs, sentences, words)
- ✓ Maintains context with overlap
- ✓ Detailed chunk statistics logging
- ✓ Per-call parameter override

**Separators Used (in order):**
1. `\n\n` - Double newlines (paragraphs)
2. `\n` - Single newlines
3. `" "` - Spaces (words)
4. `""` - Characters (fallback)

**Example:**
```python
processor = DocumentProcessor()

# Use default settings
chunks = processor.chunk_text(text)

# Custom parameters for this call
small_chunks = processor.chunk_text(
    text,
    chunk_size=500,
    chunk_overlap=100
)

print(f"Default: {len(chunks)} chunks")
print(f"Small: {len(small_chunks)} chunks")
```

**Chunk Statistics:**
```python
chunks = processor.chunk_text(text)

# Logged automatically:
# - Total chunk count
# - Average chunk size
# - Min/max chunk sizes
```

---

### 3. process_document()

Orchestrate the full document processing pipeline.

**Signature:**
```python
def process_document(
    self,
    file_path: str,
    filename: str
) -> dict
```

**Parameters:**
- `file_path` (str): Path to the document file
- `filename` (str): Original filename for metadata

**Returns:**
Dictionary containing:
```python
{
    "filename": str,                      # Original filename
    "total_chunks": int,                  # Number of chunks created
    "chunks": List[str],                  # List of text chunks
    "timestamp": str,                     # ISO format timestamp
    "file_path": str,                     # Path to the file
    "text_length": int,                   # Total characters extracted
    "processing_time_seconds": float      # Processing duration
}
```

**Raises:**
- `Exception`: If processing fails

**Pipeline Steps:**
1. Extract text from PDF
2. Chunk the text
3. Calculate statistics
4. Return metadata

**Example:**
```python
processor = DocumentProcessor()

result = processor.process_document(
    file_path="/path/to/document.pdf",
    filename="document.pdf"
)

print(f"Processed: {result['filename']}")
print(f"Created: {result['total_chunks']} chunks")
print(f"Text length: {result['text_length']} chars")
print(f"Time: {result['processing_time_seconds']:.2f}s")

# Access chunks
for i, chunk in enumerate(result['chunks']):
    print(f"Chunk {i}: {len(chunk)} chars")
```

**Handling Empty Documents:**
```python
result = processor.process_document("empty.pdf", "empty.pdf")

if result['total_chunks'] == 0:
    print(f"Warning: {result.get('error', 'No text extracted')}")
```

---

## Complete Usage Examples

### Example 1: Basic PDF Processing

```python
from app.services.document_service import DocumentProcessor

# Initialize
processor = DocumentProcessor()

# Process PDF
result = processor.process_document(
    file_path="research_paper.pdf",
    filename="research_paper.pdf"
)

# Display results
print(f"Document: {result['filename']}")
print(f"Chunks: {result['total_chunks']}")
print(f"Text length: {result['text_length']}")
print(f"Processing time: {result['processing_time_seconds']:.2f}s")

# Work with chunks
chunks = result['chunks']
for i, chunk in enumerate(chunks):
    print(f"\nChunk {i + 1}/{len(chunks)}:")
    print(chunk[:200])  # First 200 chars
```

### Example 2: Custom Chunk Sizes

```python
from app.services.document_service import DocumentProcessor

# Small chunks for detailed processing
small_processor = DocumentProcessor(chunk_size=500, chunk_overlap=50)
small_result = small_processor.process_document("doc.pdf", "doc.pdf")

# Large chunks for overview
large_processor = DocumentProcessor(chunk_size=2000, chunk_overlap=400)
large_result = large_processor.process_document("doc.pdf", "doc.pdf")

print(f"Small chunks: {small_result['total_chunks']}")
print(f"Large chunks: {large_result['total_chunks']}")
```

### Example 3: Error Handling

```python
from app.services.document_service import DocumentProcessor
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

processor = DocumentProcessor()

try:
    # Process document
    result = processor.process_document("document.pdf", "document.pdf")
    
    # Check for extraction issues
    if result['total_chunks'] == 0:
        print(f"Warning: {result.get('error', 'Unknown error')}")
    else:
        print(f"Success! Created {result['total_chunks']} chunks")
        
except FileNotFoundError:
    print("PDF file not found")
except Exception as e:
    print(f"Processing failed: {e}")
```

### Example 4: Batch Processing

```python
from app.services.document_service import DocumentProcessor
import os

processor = DocumentProcessor()

pdf_dir = "documents/"
results = []

for filename in os.listdir(pdf_dir):
    if filename.endswith(".pdf"):
        file_path = os.path.join(pdf_dir, filename)
        
        try:
            result = processor.process_document(file_path, filename)
            results.append(result)
            print(f"✓ {filename}: {result['total_chunks']} chunks")
        except Exception as e:
            print(f"✗ {filename}: {e}")

# Summary
total_chunks = sum(r['total_chunks'] for r in results)
print(f"\nProcessed {len(results)} documents, {total_chunks} total chunks")
```

### Example 5: Integration with Vector Store

```python
from app.services.document_service import DocumentProcessor
from app.services.vector_store import VectorStoreService

# Initialize services
processor = DocumentProcessor()
vector_store = VectorStoreService()

# Process document
result = processor.process_document("paper.pdf", "paper.pdf")

# Prepare metadata
metadatas = [
    {
        "source": result['filename'],
        "chunk_index": i,
        "total_chunks": result['total_chunks']
    }
    for i in range(result['total_chunks'])
]

# Add to vector store
await vector_store.add_documents(
    texts=result['chunks'],
    metadatas=metadatas
)

print(f"Added {result['total_chunks']} chunks to vector store")
```

---

## Configuration

The DocumentProcessor uses settings from `app.core.config`:

```python
# Default values from settings
CHUNK_SIZE: int = 1000          # Characters per chunk
CHUNK_OVERLAP: int = 200        # Overlap between chunks
```

Override via environment variables:
```bash
# .env file
CHUNK_SIZE=1500
CHUNK_OVERLAP=300
```

---

## Logging

The DocumentProcessor provides detailed logging:

- **INFO**: Processing steps and success messages
- **DEBUG**: Detailed chunk statistics and page extraction
- **WARNING**: Empty pages, no text extracted
- **ERROR**: Extraction and chunking errors

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## Performance Tips

1. **Chunk Size**: Larger chunks = fewer chunks but more context
2. **Chunk Overlap**: More overlap = better context but more redundancy
3. **Batch Processing**: Process multiple documents in sequence
4. **Error Recovery**: Continue processing even if some pages fail

---

## Testing

Run the test suite:
```bash
cd backend
python test_document_processor.py
```

Test with your own PDF:
```bash
# Place a PDF named 'sample.pdf' in the backend directory
python test_document_processor.py
```

---

## Troubleshooting

### Issue: No text extracted from PDF

**Cause**: PDF may be image-based (scanned)

**Solution**: Use OCR preprocessing or different PDF library

### Issue: Chunks too small/large

**Cause**: Incorrect chunk_size setting

**Solution**: Adjust CHUNK_SIZE in config or override in constructor

### Issue: Loss of context between chunks

**Cause**: Insufficient overlap

**Solution**: Increase CHUNK_OVERLAP setting

### Issue: Processing very slow

**Cause**: Large PDF with many pages

**Solution**: Consider async processing or progress tracking

---

## Best Practices

1. ✓ Use appropriate chunk sizes for your use case
2. ✓ Test with sample documents first
3. ✓ Handle errors gracefully
4. ✓ Monitor chunk statistics
5. ✓ Validate extracted text quality
6. ✓ Log processing metrics
7. ✓ Use overlap to maintain context

---

## API Reference

| Method | Input | Output | Purpose |
|--------|-------|--------|---------|
| `extract_text_from_pdf()` | file_path: str | str | Extract text from PDF |
| `chunk_text()` | text: str, chunk_size: int, chunk_overlap: int | List[str] | Split text into chunks |
| `process_document()` | file_path: str, filename: str | dict | Full processing pipeline |

---

## Related Components

- **DocumentService**: High-level service using DocumentProcessor
- **VectorStoreService**: Stores processed chunks
- **Settings**: Configuration management

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Dependencies**: pypdf 3.17.0, langchain 0.1.0


