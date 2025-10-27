"""
FastAPI Main Application - ResearchMate RAG API
"""
import logging
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("researchmate.log")
    ]
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup and shutdown events
    """
    # Startup
    logger.info("🚀 Starting ResearchMate RAG API...")
    logger.info(f"   - Version: {settings.VERSION}")
    logger.info(f"   - Debug Mode: {settings.DEBUG}")
    logger.info(f"   - Host: {settings.HOST}:{settings.PORT}")
    
    # Check Ollama connection
    try:
        from app.services.llm_service import LLMService
        llm_service = LLMService()
        if llm_service.check_connection():
            logger.info("✅ Ollama connection successful")
            logger.info(f"   - Model: {settings.OLLAMA_MODEL}")
        else:
            logger.warning("⚠️ Ollama connection failed - some features may not work")
    except Exception as e:
        logger.error(f"❌ Ollama connection error: {str(e)}")
        logger.warning("⚠️ Please ensure Ollama is running: ollama serve")
    
    # Initialize vector store
    try:
        from app.services.vector_store import VectorStoreService
        vector_store = VectorStoreService()
        status = vector_store.get_status()
        if status.get("healthy", False):
            logger.info("✅ Vector store initialized successfully")
            logger.info(f"   - Collection: {settings.COLLECTION_NAME}")
        else:
            logger.warning("⚠️ Vector store initialization failed")
    except Exception as e:
        logger.error(f"❌ Vector store error: {str(e)}")
        logger.warning("⚠️ Vector store may not be available")
    
    # Create necessary directories
    try:
        settings.create_directories()
        logger.info("✅ Application directories created")
    except Exception as e:
        logger.error(f"❌ Directory creation error: {str(e)}")
    
    logger.info("🎉 ResearchMate RAG API startup complete!")
    logger.info("📚 API Documentation: http://localhost:8000/docs")
    logger.info("🔍 Health Check: http://localhost:8000/api/v1/health")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down ResearchMate RAG API...")
    logger.info("✅ Cleanup completed")


# Create FastAPI application
app = FastAPI(
    title="ResearchMate RAG API",
    description="ML/DS Research Paper Q&A Assistant with RAG and LLM",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(router, prefix="/api/v1")


@app.get("/")
async def root():
    """
    Root endpoint with API information
    """
    return {
        "message": "ResearchMate RAG API",
        "docs": "/docs",
        "health": "/api/v1/health",
        "version": "1.0.0",
        "description": "ML/DS Research Paper Q&A Assistant"
    }


@app.get("/health")
async def simple_health():
    """
    Simple health check for container orchestration
    """
    return {
        "status": "healthy",
        "service": "ResearchMate RAG API",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    
    logger.info("🚀 Starting ResearchMate RAG API server...")
    logger.info(f"   - Host: {settings.HOST}")
    logger.info(f"   - Port: {settings.PORT}")
    logger.info(f"   - Debug: {settings.DEBUG}")
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )

