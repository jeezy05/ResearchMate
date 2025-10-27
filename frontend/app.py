"""
ResearchMate - Streamlit Frontend
A beautiful interface for document Q&A using RAG
"""
import streamlit as st
import requests
import os
import time
from datetime import datetime
from typing import Optional, Dict, Any

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_V1_URL = f"{API_BASE_URL}/api/v1"

# Page configuration
st.set_page_config(
    page_title="ResearchMate",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful UI
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Subtitle styling */
    .subtitle {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
        font-style: italic;
    }
    
    /* Source card styling */
    .source-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        border-left: 5px solid #667eea;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    
    .source-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Answer box styling */
    .answer-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Sidebar styling */
    .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Status indicators */
    .status-online {
        color: #28a745;
        font-weight: bold;
    }
    
    .status-offline {
        color: #dc3545;
        font-weight: bold;
    }
    
    /* Processing animation */
    .processing {
        display: inline-block;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        color: #6c757d;
        font-size: 0.9rem;
        margin-top: 2rem;
        padding: 1rem;
        border-top: 1px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables"""
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "uploaded_documents" not in st.session_state:
        st.session_state.uploaded_documents = []
    if "api_endpoint" not in st.session_state:
        st.session_state.api_endpoint = "http://localhost:8000"


def check_api_health(api_url: str) -> Dict[str, Any]:
    """Check if the API is accessible and get health status"""
    try:
        # Check simple health endpoint
        response = requests.get(f"{api_url}/health", timeout=5)
        if response.status_code == 200:
            # Try to get detailed health status
            try:
                health_response = requests.get(f"{api_url}/api/v1/health", timeout=5)
                if health_response.status_code == 200:
                    return {"status": "online", "details": health_response.json()}
            except:
                pass
            return {"status": "online", "details": {"status": "healthy"}}
    except:
        pass
    return {"status": "offline", "details": None}


def upload_document(file, api_url: str) -> Optional[dict]:
    """Upload a document to the API"""
    try:
        files = {"file": (file.name, file.getvalue(), file.type)}
        response = requests.post(
            f"{api_url}/api/v1/upload",
            files=files,
            timeout=300
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"❌ Error uploading document: {str(e)}")
        return None


def query_documents(question: str, api_url: str, max_results: int = 5) -> Optional[dict]:
    """Query documents using RAG"""
    try:
        payload = {
            "question": question,
            "max_results": max_results
        }
        response = requests.post(
            f"{api_url}/api/v1/query",
            json=payload,
            timeout=300
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"❌ Error querying documents: {str(e)}")
        return None


def reset_database(api_url: str) -> bool:
    """Reset the database by clearing all data"""
    try:
        response = requests.delete(f"{api_url}/api/v1/reset", timeout=30)
        response.raise_for_status()
        return True
    except Exception as e:
        st.error(f"❌ Error resetting database: {str(e)}")
        return False


def render_sidebar():
    """Render the sidebar with document management and settings"""
    with st.sidebar:
        # Header
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.markdown("## 📚 ResearchMate")
        st.markdown("### ML/DS Research Paper Assistant")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # API Configuration
        st.markdown("### 🔧 API Configuration")
        api_endpoint = st.text_input(
            "API Endpoint",
            value=st.session_state.api_endpoint,
            help="Enter the backend API URL"
        )
        st.session_state.api_endpoint = api_endpoint
        
        # Health Check
        health_status = check_api_health(api_endpoint)
        if health_status["status"] == "online":
            st.markdown('<span class="status-online">🟢 API Online</span>', unsafe_allow_html=True)
            if health_status["details"]:
                details = health_status["details"]
                st.caption(f"Status: {details.get('status', 'unknown')}")
                if details.get('model'):
                    st.caption(f"Model: {details['model']}")
        else:
            st.markdown('<span class="status-offline">🔴 API Offline</span>', unsafe_allow_html=True)
            st.error("⚠️ Cannot connect to API. Please check if the backend is running.")
        
        st.markdown("---")
        
        # Document Upload
        st.markdown("### 📤 Upload Documents")
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=["pdf"],
            help="Upload a PDF document to add to your knowledge base",
            key="file_uploader"
        )
        
        if uploaded_file is not None:
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("📤 Upload & Process", key="upload_btn"):
                    with st.spinner("🔄 Processing document..."):
                        result = upload_document(uploaded_file, api_endpoint)
                        if result:
                            st.success(f"✅ {result['message']}")
                            st.info(f"📊 Created {result['total_chunks']} chunks")
                            # Add to session state
                            st.session_state.uploaded_documents.append({
                                "filename": result['filename'],
                                "chunks": result['total_chunks'],
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            })
                            st.rerun()
            
            with col2:
                if st.button("❌ Cancel", key="cancel_btn"):
                    st.rerun()
        
        # Uploaded Documents
        if st.session_state.uploaded_documents:
            st.markdown("### 📚 Uploaded Documents")
            for i, doc in enumerate(st.session_state.uploaded_documents):
                with st.expander(f"📄 {doc['filename'][:30]}..."):
                    st.write(f"**Chunks:** {doc['chunks']}")
                    st.write(f"**Uploaded:** {doc['timestamp']}")
                    if st.button(f"🗑️ Remove", key=f"remove_{i}"):
                        st.session_state.uploaded_documents.pop(i)
                        st.rerun()
        
        st.markdown("---")
        
        # Database Management
        st.markdown("### 🗄️ Database Management")
        if st.button("🗑️ Clear Database", key="clear_db_btn"):
            if st.session_state.get("confirm_clear", False):
                with st.spinner("🔄 Clearing database..."):
                    if reset_database(api_endpoint):
                        st.success("✅ Database cleared successfully!")
                        st.session_state.uploaded_documents = []
                        st.session_state.messages = []
                        st.session_state.conversation_id = None
                        st.session_state.confirm_clear = False
                        st.rerun()
            else:
                st.session_state.confirm_clear = True
                st.warning("⚠️ Click again to confirm database reset")
        
        if st.session_state.get("confirm_clear", False):
            if st.button("✅ Confirm Clear", key="confirm_clear_btn"):
                st.session_state.confirm_clear = False
                st.rerun()
        
        # Settings
        st.markdown("### ⚙️ Settings")
        if st.button("🔄 New Conversation", key="new_conv_btn"):
            st.session_state.messages = []
            st.session_state.conversation_id = None
            st.success("✅ Started new conversation!")
            st.rerun()


def render_main_interface():
    """Render the main chat interface"""
    # Header
    st.markdown('<h1 class="main-header">📚 ResearchMate</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Ask Questions About Your Research Papers</p>', unsafe_allow_html=True)
    
    # Check API health
    api_url = st.session_state.api_endpoint
    health_status = check_api_health(api_url)
    
    if health_status["status"] != "online":
        st.error("⚠️ Cannot connect to the API. Please ensure the backend is running.")
        st.info(f"API URL: {api_url}")
        st.markdown("### 🚀 Quick Start Guide")
        st.markdown("""
        1. **Start the Backend**: 
           ```bash
           cd backend
           python -m uvicorn app.main:app --reload
           ```
        2. **Verify API**: Check http://localhost:8000/docs
        3. **Refresh this page** once the API is running
        """)
        return
    
    # Display conversation history
    if st.session_state.messages:
        st.markdown("### 💬 Conversation History")
        for message in st.session_state.messages:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.markdown(message["content"])
            else:
                with st.chat_message("assistant"):
                    st.markdown(message["content"])
                    
                    # Display sources if available
                    if "sources" in message and message["sources"]:
                        with st.expander("📖 View Sources"):
                            for idx, source in enumerate(message["sources"], 1):
                                st.markdown(f"""
                                <div class="source-card">
                                    <strong>📄 Source {idx}:</strong> {source.get('filename', 'Unknown')}<br>
                                    <strong>🎯 Relevance:</strong> {source.get('relevance_score', 0):.2%}<br>
                                    <strong>📝 Content:</strong> {source.get('content', 'No content available')[:200]}...
                                </div>
                                """, unsafe_allow_html=True)
    
    # Chat input
    st.markdown("### 🤖 Ask a Question")
    question = st.text_area(
        "Enter your question about the uploaded documents:",
        placeholder="e.g., What is machine learning? How does deep learning work?",
        height=100,
        key="question_input"
    )
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        submit_question = st.button("🚀 Submit Question", key="submit_btn", type="primary")
    
    with col2:
        max_results = st.selectbox("Max Results", [3, 5, 10], index=1, key="max_results")
    
    with col3:
        if st.button("🗑️ Clear Chat", key="clear_chat_btn"):
            st.session_state.messages = []
            st.session_state.conversation_id = None
            st.success("✅ Chat cleared!")
            st.rerun()
    
    # Process question
    if submit_question and question.strip():
        # Add user message
        st.session_state.messages.append({"role": "user", "content": question})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(question)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                start_time = time.time()
                response = query_documents(question, api_url, max_results)
                processing_time = time.time() - start_time
                
                if response:
                    # Display answer in a beautiful box
                    st.markdown(f"""
                    <div class="answer-box">
                        <h4>🎯 Answer:</h4>
                        <p>{response['answer']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display sources
                    if response.get("sources"):
                        st.markdown("### 📚 Sources")
                        with st.expander("📖 View All Sources", expanded=True):
                            for idx, source in enumerate(response["sources"], 1):
                                st.markdown(f"""
                                <div class="source-card">
                                    <strong>📄 Source {idx}:</strong> {source.get('filename', 'Unknown')}<br>
                                    <strong>🎯 Relevance:</strong> {source.get('relevance_score', 0):.2%}<br>
                                    <strong>📝 Content:</strong> {source.get('content', 'No content available')}
                                </div>
                                """, unsafe_allow_html=True)
                    
                    # Display processing info
                    st.caption(f"⏱️ Processed in {response.get('processing_time', processing_time):.2f}s")
                    
                    # Add assistant message to history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response["answer"],
                        "sources": response.get("sources", [])
                    })
                else:
                    st.error("❌ Failed to get response from the API")
    
    # Show upload status
    if st.session_state.uploaded_documents:
        st.markdown("### 📊 Document Status")
        total_chunks = sum(doc['chunks'] for doc in st.session_state.uploaded_documents)
        st.info(f"📚 {len(st.session_state.uploaded_documents)} documents uploaded • 📊 {total_chunks} total chunks")


def main():
    """Main application"""
    init_session_state()
    
    # Render sidebar and main interface
    render_sidebar()
    render_main_interface()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <strong>ResearchMate v1.0.0</strong> | 
        Powered by FastAPI, Streamlit & Ollama | 
        Built with ❤️ for ML/DS Research
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

