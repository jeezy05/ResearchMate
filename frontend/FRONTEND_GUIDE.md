# ResearchMate Frontend Guide

## Overview

The ResearchMate frontend is a beautiful Streamlit application that provides an intuitive interface for interacting with the RAG (Retrieval-Augmented Generation) system. It allows users to upload PDF documents, ask questions, and get AI-powered answers with source citations.

## Features

### 🎨 Beautiful UI Components
- **Gradient Headers**: Eye-catching gradient text for the main title
- **Custom CSS Styling**: Professional color scheme with hover effects
- **Responsive Layout**: Wide layout optimized for research workflows
- **Status Indicators**: Real-time API connection status
- **Loading Animations**: Smooth processing indicators

### 📚 Document Management
- **PDF Upload**: Drag-and-drop PDF file upload
- **Processing Status**: Real-time upload and processing feedback
- **Document Tracking**: Track uploaded documents and chunk counts
- **File Validation**: Automatic PDF type and size validation

### 🤖 AI Chat Interface
- **Question Input**: Large text area for detailed questions
- **Answer Display**: Beautiful formatted answer boxes
- **Source Citations**: Expandable source sections with relevance scores
- **Processing Time**: Performance metrics display
- **Conversation History**: Persistent chat history

### ⚙️ Advanced Features
- **API Configuration**: Configurable backend endpoint
- **Health Monitoring**: Real-time backend status checking
- **Database Management**: Clear database with confirmation
- **Session Management**: Persistent user sessions
- **Error Handling**: Comprehensive error messages and recovery

## File Structure

```
frontend/
├── app.py                 # Main Streamlit application
├── start_frontend.py      # Startup script
├── test_frontend.py       # Test suite
├── requirements.txt       # Python dependencies
└── FRONTEND_GUIDE.md     # This guide
```

## Installation

### Prerequisites
- Python 3.8+
- Backend API running on http://localhost:8000
- Required Python packages

### Setup Steps

1. **Install Dependencies**:
   ```bash
   cd frontend
   pip install -r requirements.txt
   ```

2. **Verify Backend**:
   ```bash
   # Check if backend is running
   curl http://localhost:8000/health
   ```

3. **Start Frontend**:
   ```bash
   # Option 1: Using startup script
   python start_frontend.py
   
   # Option 2: Direct Streamlit
   streamlit run app.py
   ```

## Usage

### 1. Access the Application
- Open your browser to: http://localhost:8501
- The application will automatically check backend connectivity

### 2. Upload Documents
1. **Select PDF File**: Use the file uploader in the sidebar
2. **Click Upload**: Press "📤 Upload & Process" button
3. **Monitor Progress**: Watch the processing spinner
4. **Verify Success**: Check the success message and chunk count

### 3. Ask Questions
1. **Enter Question**: Type your question in the text area
2. **Configure Settings**: Choose max results (3, 5, or 10)
3. **Submit**: Click "🚀 Submit Question"
4. **View Answer**: Read the AI-generated response
5. **Check Sources**: Expand the sources section for citations

### 4. Manage Data
- **Clear Chat**: Remove conversation history
- **New Conversation**: Start fresh chat session
- **Clear Database**: Remove all uploaded documents
- **View Status**: Monitor document and chunk counts

## API Integration

### Endpoints Used
- `GET /health` - Simple health check
- `GET /api/v1/health` - Detailed health status
- `POST /api/v1/upload` - Document upload
- `POST /api/v1/query` - Question answering
- `DELETE /api/v1/reset` - Database reset

### Request/Response Format

#### Upload Request
```python
files = {"file": (filename, file_content, "application/pdf")}
response = requests.post(f"{api_url}/api/v1/upload", files=files)
```

#### Upload Response
```json
{
    "filename": "research_paper.pdf",
    "total_chunks": 25,
    "message": "Document uploaded and processed successfully",
    "status": "success"
}
```

#### Query Request
```json
{
    "question": "What is machine learning?",
    "max_results": 5
}
```

#### Query Response
```json
{
    "question": "What is machine learning?",
    "answer": "Machine learning is...",
    "sources": [
        {
            "content": "Machine learning is a subset of AI...",
            "metadata": {"filename": "research_paper.pdf"},
            "relevance_score": 0.95
        }
    ],
    "processing_time": 2.34
}
```

## Configuration

### Environment Variables
- `API_BASE_URL`: Backend API URL (default: http://localhost:8000)

### Session State Variables
- `conversation_id`: Current conversation identifier
- `messages`: Chat message history
- `uploaded_documents`: List of uploaded documents
- `api_endpoint`: Configured API endpoint

## Styling

### CSS Classes
- `.main-header`: Gradient title styling
- `.subtitle`: Subtitle text styling
- `.source-card`: Source citation cards
- `.answer-box`: Answer display boxes
- `.sidebar-content`: Sidebar section styling
- `.status-online/offline`: Connection status indicators

### Color Scheme
- **Primary**: #667eea (Blue gradient)
- **Secondary**: #764ba2 (Purple gradient)
- **Success**: #28a745 (Green)
- **Error**: #dc3545 (Red)
- **Background**: #f8f9fa (Light gray)

## Error Handling

### Connection Errors
- **Backend Offline**: Clear error message with setup instructions
- **API Timeout**: Automatic retry with user feedback
- **Network Issues**: Graceful degradation with helpful messages

### Upload Errors
- **File Type**: PDF-only validation
- **File Size**: Size limit enforcement
- **Processing**: Error recovery with retry options

### Query Errors
- **Empty Questions**: Input validation
- **API Failures**: Error messages with troubleshooting
- **Timeout**: Processing time limits

## Testing

### Run Test Suite
```bash
python test_frontend.py
```

### Test Coverage
1. **Import Dependencies**: Verify all modules load
2. **App Structure**: Check function definitions
3. **API Endpoints**: Validate endpoint configuration
4. **UI Components**: Test Streamlit components
5. **Error Handling**: Verify error management
6. **Backend Connection**: Test API connectivity
7. **Syntax Validation**: Check Python syntax
8. **Requirements**: Verify package installation

### Manual Testing
1. **Upload Test**: Upload a sample PDF
2. **Query Test**: Ask questions about uploaded content
3. **Error Test**: Test error scenarios
4. **UI Test**: Verify all UI components work
5. **Session Test**: Test session persistence

## Troubleshooting

### Common Issues

#### Backend Connection Failed
```
❌ Cannot connect to API. Please check if the backend is running.
```
**Solution**: Start the backend server
```bash
cd backend
python -m uvicorn app.main:app --reload
```

#### Upload Errors
```
❌ Error uploading document: Connection timeout
```
**Solution**: Check file size and network connection

#### Query Failures
```
❌ Failed to get response from the API
```
**Solution**: Verify backend is running and Ollama is available

### Debug Mode
Enable debug logging by setting environment variable:
```bash
export STREAMLIT_LOGGER_LEVEL=debug
streamlit run app.py
```

## Performance

### Optimization Tips
1. **File Size**: Keep PDFs under 10MB
2. **Chunk Size**: Optimize chunk size for your documents
3. **Max Results**: Limit results for faster responses
4. **Session Management**: Clear old conversations regularly

### Monitoring
- **Processing Time**: Displayed for each query
- **Chunk Count**: Track document processing
- **API Status**: Real-time connection monitoring
- **Error Rates**: Automatic error tracking

## Development

### Adding Features
1. **New Components**: Add to appropriate render function
2. **API Endpoints**: Update API integration functions
3. **Styling**: Modify CSS in the style block
4. **State Management**: Update session state variables

### Code Structure
- **Functions**: Modular design with clear responsibilities
- **Error Handling**: Comprehensive try-except blocks
- **Type Hints**: Full type annotation support
- **Documentation**: Inline comments and docstrings

## Security

### Input Validation
- **File Types**: PDF-only uploads
- **File Size**: Configurable size limits
- **API Endpoints**: URL validation
- **User Input**: Question sanitization

### Session Security
- **State Management**: Secure session state handling
- **API Keys**: No sensitive data in frontend
- **CORS**: Proper cross-origin configuration

## Deployment

### Production Setup
1. **Environment**: Set production API URL
2. **Security**: Configure CORS and authentication
3. **Monitoring**: Set up logging and error tracking
4. **Scaling**: Use Streamlit Cloud or similar platform

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

## Support

### Getting Help
1. **Check Logs**: Review error messages
2. **Test Backend**: Verify API connectivity
3. **Update Dependencies**: Ensure latest packages
4. **Restart Services**: Restart both frontend and backend

### Common Commands
```bash
# Start frontend
streamlit run app.py

# Test frontend
python test_frontend.py

# Check backend
curl http://localhost:8000/health

# View logs
tail -f researchmate.log
```

## Conclusion

The ResearchMate frontend provides a comprehensive, user-friendly interface for RAG-based document Q&A. With its beautiful design, robust error handling, and seamless API integration, it offers an excellent user experience for researchers and students working with academic papers.

The modular architecture makes it easy to extend and customize, while the comprehensive testing ensures reliability and performance. Whether you're uploading research papers, asking complex questions, or managing your document collection, the frontend provides all the tools you need for effective research assistance.

