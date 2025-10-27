@echo off
echo 🚀 Starting ResearchMate RAG API Server
echo ================================================

REM Check if Ollama is running
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Ollama is not running
    echo    Please start Ollama first:
    echo    ollama serve
    echo.
    echo ⚠️  Please start Ollama first, then run this script again
    pause
    exit /b 1
)

echo ✅ Ollama is running
echo.
echo 📋 Server Information:
echo    - API Documentation: http://localhost:8000/docs
echo    - Health Check: http://localhost:8000/api/v1/health
echo    - Root Endpoint: http://localhost:8000/
echo.
echo 🔄 Starting server...
echo    (Press Ctrl+C to stop)
echo ================================================

REM Start the server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

echo.
echo 🛑 Server stopped
pause

