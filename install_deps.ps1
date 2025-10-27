# Quick Installation Script for Windows PowerShell
# This script sets up the Python 3.11 environment and installs dependencies

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ResearchMate RAG - Dependency Installer" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if conda is available
if (!(Get-Command conda -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Conda not found. Please install Miniconda or Anaconda first." -ForegroundColor Red
    exit 1
}

Write-Host "✓ Conda found" -ForegroundColor Green
Write-Host ""

# Create conda environment with Python 3.11
Write-Host "Creating conda environment 'researchmate' with Python 3.11..." -ForegroundColor Yellow
conda create -n researchmate python=3.11 -y

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to create conda environment" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Environment created" -ForegroundColor Green
Write-Host ""

# Activate environment and install dependencies
Write-Host "Installing backend dependencies..." -ForegroundColor Yellow
Write-Host ""

# Run installation in the conda environment
conda run -n researchmate python -m pip install --upgrade pip
conda run -n researchmate pip install -r backend/requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    Write-Host ""
    Write-Host "Try activating the environment manually:" -ForegroundColor Yellow
    Write-Host "  conda activate researchmate" -ForegroundColor White
    Write-Host "  cd backend" -ForegroundColor White
    Write-Host "  pip install --upgrade pip" -ForegroundColor White
    Write-Host "  pip install -r requirements.txt" -ForegroundColor White
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✓ Installation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "To activate the environment, run:" -ForegroundColor Cyan
Write-Host "  conda activate researchmate" -ForegroundColor White
Write-Host ""
Write-Host "Then start the backend:" -ForegroundColor Cyan
Write-Host "  cd backend" -ForegroundColor White
Write-Host "  uvicorn app.main:app --reload" -ForegroundColor White
Write-Host ""

