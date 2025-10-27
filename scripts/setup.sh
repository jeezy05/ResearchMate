#!/bin/bash

# ResearchMate Setup Script
# This script helps set up the development environment

set -e

echo "=========================================="
echo "   ResearchMate RAG - Setup Script"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Check if Docker is installed
echo "Checking prerequisites..."
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi
print_success "Docker is installed"

if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi
print_success "Docker Compose is installed"

# Check if Ollama is running
echo ""
echo "Checking Ollama..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    print_success "Ollama is running"
else
    print_error "Ollama is not running on port 11434"
    print_info "Please install and start Ollama from https://ollama.ai"
    print_info "After installation, run: ollama serve"
    exit 1
fi

# Create .env file if it doesn't exist
echo ""
echo "Setting up environment..."
if [ ! -f .env ]; then
    print_info "Creating .env file from .env.example"
    cp .env.example .env
    print_success ".env file created"
else
    print_info ".env file already exists"
fi

# Create necessary directories
echo ""
echo "Creating directories..."
mkdir -p data/raw
mkdir -p data/processed/chroma_db
print_success "Directories created"

# Pull required Ollama models
echo ""
echo "Checking Ollama models..."
print_info "Checking for llama2 model..."
if ollama list | grep -q "llama2"; then
    print_success "llama2 model is available"
else
    print_info "Pulling llama2 model (this may take a while)..."
    ollama pull llama2
    print_success "llama2 model downloaded"
fi

print_info "Checking for nomic-embed-text model..."
if ollama list | grep -q "nomic-embed-text"; then
    print_success "nomic-embed-text model is available"
else
    print_info "Pulling nomic-embed-text model..."
    ollama pull nomic-embed-text
    print_success "nomic-embed-text model downloaded"
fi

# Test Ollama connection
echo ""
echo "Testing Ollama connection..."
python3 scripts/test_ollama.py
if [ $? -eq 0 ]; then
    print_success "Ollama connection test passed"
else
    print_error "Ollama connection test failed"
    exit 1
fi

# Build Docker images
echo ""
echo "Building Docker images..."
docker-compose build
print_success "Docker images built successfully"

echo ""
echo "=========================================="
print_success "Setup completed successfully!"
echo "=========================================="
echo ""
echo "To start the application, run:"
echo "  docker-compose up -d"
echo ""
echo "Then access:"
echo "  Frontend: http://localhost:8501"
echo "  Backend API: http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo ""


