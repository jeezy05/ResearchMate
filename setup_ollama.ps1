# Ollama Setup Script for ResearchMate
# This script helps you install Ollama and set up a model

Write-Host "🚀 ResearchMate Ollama Setup Script" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

# Check if Ollama is already installed
Write-Host "`n📋 Checking if Ollama is installed..." -ForegroundColor Yellow

try {
    $ollamaVersion = ollama --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Ollama is already installed: $ollamaVersion" -ForegroundColor Green
    } else {
        throw "Ollama not found"
    }
} catch {
    Write-Host "❌ Ollama is not installed" -ForegroundColor Red
    Write-Host "`n📥 Please install Ollama first:" -ForegroundColor Yellow
    Write-Host "1. Go to https://ollama.com/download" -ForegroundColor Cyan
    Write-Host "2. Download and install Ollama for Windows" -ForegroundColor Cyan
    Write-Host "3. Restart your terminal after installation" -ForegroundColor Cyan
    Write-Host "4. Run this script again" -ForegroundColor Cyan
    exit 1
}

# Check if Ollama service is running
Write-Host "`n🔍 Checking if Ollama service is running..." -ForegroundColor Yellow

try {
    $response = Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -Method Get -TimeoutSec 5
    Write-Host "✅ Ollama service is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Ollama service is not running" -ForegroundColor Red
    Write-Host "`n🚀 Starting Ollama service..." -ForegroundColor Yellow
    
    # Start Ollama in background
    Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
    
    # Wait a moment for service to start
    Start-Sleep -Seconds 3
    
    # Check again
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -Method Get -TimeoutSec 5
        Write-Host "✅ Ollama service started successfully" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to start Ollama service" -ForegroundColor Red
        Write-Host "Please start Ollama manually: ollama serve" -ForegroundColor Yellow
        exit 1
    }
}

# List available models
Write-Host "`n📋 Available models:" -ForegroundColor Yellow
try {
    $models = ollama list
    if ($models) {
        Write-Host $models -ForegroundColor Cyan
    } else {
        Write-Host "No models installed" -ForegroundColor Yellow
    }
} catch {
    Write-Host "Error listing models" -ForegroundColor Red
}

# Ask user which model to install
Write-Host "`n🤖 Which model would you like to install?" -ForegroundColor Yellow
Write-Host "1. llama2 (7B) - Recommended for most users" -ForegroundColor Cyan
Write-Host "2. mistral (7B) - Fast and efficient" -ForegroundColor Cyan
Write-Host "3. phi3 (3.8B) - Lightweight option" -ForegroundColor Cyan
Write-Host "4. gemma:2b (2B) - Very fast, good for testing" -ForegroundColor Cyan
Write-Host "5. Skip - I'll install manually" -ForegroundColor Cyan

$choice = Read-Host "`nEnter your choice (1-5)"

switch ($choice) {
    "1" { 
        $model = "llama2"
        Write-Host "`n📥 Installing llama2..." -ForegroundColor Yellow
    }
    "2" { 
        $model = "mistral"
        Write-Host "`n📥 Installing mistral..." -ForegroundColor Yellow
    }
    "3" { 
        $model = "phi3"
        Write-Host "`n📥 Installing phi3..." -ForegroundColor Yellow
    }
    "4" { 
        $model = "gemma:2b"
        Write-Host "`n📥 Installing gemma:2b..." -ForegroundColor Yellow
    }
    "5" { 
        Write-Host "`n⏭️ Skipping model installation" -ForegroundColor Yellow
        $model = $null
    }
    default { 
        Write-Host "`n❌ Invalid choice. Skipping model installation." -ForegroundColor Red
        $model = $null
    }
}

if ($model) {
    try {
        Write-Host "⏳ This may take several minutes (downloading model)..." -ForegroundColor Yellow
        ollama pull $model
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Successfully installed $model" -ForegroundColor Green
        } else {
            Write-Host "❌ Failed to install $model" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ Error installing $model" -ForegroundColor Red
        Write-Host "You can install it manually later with: ollama pull $model" -ForegroundColor Yellow
    }
}

# Test the model
if ($model) {
    Write-Host "`n🧪 Testing the model..." -ForegroundColor Yellow
    try {
        $testResponse = ollama run $model "Hello, how are you?" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Model test successful!" -ForegroundColor Green
        } else {
            Write-Host "⚠️ Model test failed, but model is installed" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "⚠️ Could not test model, but it should work" -ForegroundColor Yellow
    }
}

# Update configuration
Write-Host "`n⚙️ Updating configuration..." -ForegroundColor Yellow

if ($model) {
    # Create .env file with the chosen model
    $envContent = @"
# ResearchMate Configuration
OLLAMA_MODEL=$model
OLLAMA_BASE_URL=http://localhost:11434
"@
    
    try {
        $envContent | Out-File -FilePath ".env" -Encoding UTF8
        Write-Host "✅ Created .env file with OLLAMA_MODEL=$model" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ Could not create .env file automatically" -ForegroundColor Yellow
        Write-Host "Please create .env file manually with: OLLAMA_MODEL=$model" -ForegroundColor Cyan
    }
} else {
    Write-Host "⚠️ No model selected. Please update your configuration manually." -ForegroundColor Yellow
}

# Final instructions
Write-Host "`n🎉 Setup Complete!" -ForegroundColor Green
Write-Host "=================" -ForegroundColor Green

Write-Host "`n📋 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Make sure Ollama is running: ollama serve" -ForegroundColor Cyan
Write-Host "2. Test ResearchMate: cd backend; python test_llm_service.py" -ForegroundColor Cyan
Write-Host "3. Start the application: cd backend; python -m uvicorn app.main:app --reload" -ForegroundColor Cyan

Write-Host "`n📚 Documentation:" -ForegroundColor Yellow
Write-Host "- Ollama Setup Guide: backend/OLLAMA_SETUP_GUIDE.md" -ForegroundColor Cyan
Write-Host "- Available Models: backend/AVAILABLE_MODELS.md" -ForegroundColor Cyan
Write-Host "- LLM Service Guide: backend/LLM_SERVICE_GUIDE.md" -ForegroundColor Cyan

Write-Host "`n🆘 Need Help?" -ForegroundColor Yellow
Write-Host "- Check if Ollama is running: curl http://localhost:11434/api/tags" -ForegroundColor Cyan
Write-Host "- List models: ollama list" -ForegroundColor Cyan
Write-Host "- Test model: ollama run $model 'Hello'" -ForegroundColor Cyan

Write-Host "`n✨ Happy coding with ResearchMate!" -ForegroundColor Green

