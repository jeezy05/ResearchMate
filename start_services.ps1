#!/usr/bin/env pwsh
"""
ResearchMate Services Startup Script
Starts both backend and frontend services
"""

Write-Host "🚀 Starting ResearchMate Services" -ForegroundColor Green
Write-Host "=" * 50

# Check if we're in the right directory
if (-not (Test-Path "backend") -or -not (Test-Path "frontend")) {
    Write-Host "❌ Please run this script from the ResearchMate root directory" -ForegroundColor Red
    Write-Host "   Current directory: $(Get-Location)" -ForegroundColor Yellow
    Write-Host "   Expected structure: ResearchMate/backend/ and ResearchMate/frontend/" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Directory structure looks good" -ForegroundColor Green

# Start Backend
Write-Host "`n🔧 Starting Backend Server..." -ForegroundColor Cyan
Write-Host "   - Directory: backend/" -ForegroundColor Gray
Write-Host "   - URL: http://localhost:8000" -ForegroundColor Gray
Write-Host "   - API Docs: http://localhost:8000/docs" -ForegroundColor Gray

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

# Wait a moment for backend to start
Write-Host "⏳ Waiting for backend to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Start Frontend
Write-Host "`n🎨 Starting Frontend Server..." -ForegroundColor Cyan
Write-Host "   - Directory: frontend/" -ForegroundColor Gray
Write-Host "   - URL: http://localhost:8501" -ForegroundColor Gray

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; streamlit run app.py --server.port 8501 --server.address localhost"

# Wait a moment for frontend to start
Write-Host "⏳ Waiting for frontend to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host "`n🎉 Services Started Successfully!" -ForegroundColor Green
Write-Host "=" * 50
Write-Host "📚 ResearchMate is now running:" -ForegroundColor White
Write-Host "   - Frontend: http://localhost:8501" -ForegroundColor Cyan
Write-Host "   - Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "   - API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "`n💡 Tips:" -ForegroundColor Yellow
Write-Host "   - Upload PDF documents in the frontend" -ForegroundColor Gray
Write-Host "   - Ask questions about your documents" -ForegroundColor Gray
Write-Host "   - Check API documentation at /docs" -ForegroundColor Gray
Write-Host "`n🛑 To stop services: Close the PowerShell windows" -ForegroundColor Red

Write-Host "`nPress any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

