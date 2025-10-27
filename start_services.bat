@echo off
echo 🚀 Starting ResearchMate Services
echo ==================================================

REM Check if we're in the right directory
if not exist "backend" (
    echo ❌ Please run this script from the ResearchMate root directory
    echo    Current directory: %CD%
    echo    Expected structure: ResearchMate/backend/ and ResearchMate/frontend/
    pause
    exit /b 1
)

if not exist "frontend" (
    echo ❌ Please run this script from the ResearchMate root directory
    echo    Current directory: %CD%
    echo    Expected structure: ResearchMate/backend/ and ResearchMate/frontend/
    pause
    exit /b 1
)

echo ✅ Directory structure looks good

echo.
echo 🔧 Starting Backend Server...
echo    - Directory: backend/
echo    - URL: http://localhost:8000
echo    - API Docs: http://localhost:8000/docs

start "ResearchMate Backend" cmd /k "cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo ⏳ Waiting for backend to start...
timeout /t 3 /nobreak > nul

echo.
echo 🎨 Starting Frontend Server...
echo    - Directory: frontend/
echo    - URL: http://localhost:8501

start "ResearchMate Frontend" cmd /k "cd frontend && streamlit run app.py --server.port 8501 --server.address localhost"

echo ⏳ Waiting for frontend to start...
timeout /t 3 /nobreak > nul

echo.
echo 🎉 Services Started Successfully!
echo ==================================================
echo 📚 ResearchMate is now running:
echo    - Frontend: http://localhost:8501
echo    - Backend:  http://localhost:8000
echo    - API Docs: http://localhost:8000/docs
echo.
echo 💡 Tips:
echo    - Upload PDF documents in the frontend
echo    - Ask questions about your documents
echo    - Check API documentation at /docs
echo.
echo 🛑 To stop services: Close the command windows
echo.
pause

