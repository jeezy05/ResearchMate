# Ollama Setup Guide for ResearchMate

## 🚀 Quick Start

### 1. Install Ollama

**Windows:**
```bash
# Download from https://ollama.com/download
# Or use winget
winget install Ollama.Ollama
```

**macOS:**
```bash
# Download from https://ollama.com/download
# Or use Homebrew
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Start Ollama Service

```bash
# Start Ollama (this will run in background)
ollama serve
```

### 3. Install Available Models

**Recommended Models (in order of preference):**

```bash
# Option 1: Llama 2 (7B) - Good balance of performance/size
ollama pull llama2

# Option 2: Llama 2 (13B) - Better quality, larger size
ollama pull llama2:13b

# Option 3: Mistral (7B) - Fast and efficient
ollama pull mistral

# Option 4: Phi-3 (3.8B) - Microsoft's model, very fast
ollama pull phi3

# Option 5: Gemma (2B) - Google's model, very lightweight
ollama pull gemma:2b
```

### 4. Verify Installation

```bash
# Check if Ollama is running
ollama list

# Test a model
ollama run llama2 "Hello, how are you?"
```

## 📋 Available Models Reference

### ✅ Confirmed Available Models

| Model | Size | Description | Command |
|-------|------|-------------|---------|
| `llama2` | 7B | Meta's Llama 2 (7B) | `ollama pull llama2` |
| `llama2:13b` | 13B | Meta's Llama 2 (13B) | `ollama pull llama2:13b` |
| `mistral` | 7B | Mistral AI's model | `ollama pull mistral` |
| `phi3` | 3.8B | Microsoft's Phi-3 | `ollama pull phi3` |
| `gemma:2b` | 2B | Google's Gemma (2B) | `ollama pull gemma:2b` |
| `gemma:7b` | 7B | Google's Gemma (7B) | `ollama pull gemma:7b` |
| `codellama` | 7B | Code-focused Llama | `ollama pull codellama` |
| `neural-chat` | 7B | Intel's model | `ollama pull neural-chat` |
| `orca-mini` | 3B | Microsoft's Orca | `ollama pull orca-mini` |

### ❌ NOT Available (as of 2024)

- `llama3.2` - Not yet available in Ollama
- `llama3` - Not yet available in Ollama
- `gpt-4` - Not available (OpenAI model)
- `claude` - Not available (Anthropic model)

## 🔧 Configuration Options

### Update Your Model in ResearchMate

**Option 1: Update .env file**
```bash
# Create/update .env file
echo "OLLAMA_MODEL=llama2" >> .env
```

**Option 2: Update config.py directly**
```python
# In backend/app/core/config.py
OLLAMA_MODEL: str = Field(
    default="llama2",  # Change this to your preferred model
    description="Ollama model to use for text generation"
)
```

**Option 3: Environment variable**
```bash
# Set environment variable
export OLLAMA_MODEL=llama2
```

## 🧪 Testing Your Setup

### 1. Test Ollama Connection

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Should return JSON with available models
```

### 2. Test ResearchMate Integration

```bash
cd backend
python test_llm_service.py
```

### 3. Manual Model Test

```bash
# Test your chosen model
ollama run llama2 "Explain machine learning in simple terms"
```

## 🚨 Troubleshooting

### Problem: "ollama: command not found"
**Solution:**
```bash
# Add Ollama to PATH (Windows)
# Add C:\Users\{username}\AppData\Local\Programs\Ollama to PATH

# Or restart your terminal after installation
```

### Problem: "Connection refused" or "Connection error"
**Solution:**
```bash
# Start Ollama service
ollama serve

# Check if it's running
netstat -an | findstr 11434  # Windows
lsof -i :11434               # macOS/Linux
```

### Problem: "Model not found"
**Solution:**
```bash
# List available models
ollama list

# Pull the model you need
ollama pull llama2

# Verify it's available
ollama list
```

### Problem: "Out of memory" errors
**Solution:**
```bash
# Use smaller models
ollama pull gemma:2b      # 2B parameters
ollama pull orca-mini     # 3B parameters
ollama pull phi3          # 3.8B parameters

# Or reduce context window in config
```

## 📊 Model Comparison

| Model | Size | Speed | Quality | Memory | Best For |
|-------|------|-------|---------|--------|----------|
| `gemma:2b` | 2B | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Quick responses |
| `phi3` | 3.8B | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Balanced |
| `orca-mini` | 3B | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | General purpose |
| `llama2` | 7B | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | Good quality |
| `mistral` | 7B | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | Fast + quality |
| `llama2:13b` | 13B | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | Best quality |

## 🎯 Recommended Setup

### For Development/Testing:
```bash
ollama pull gemma:2b
# Update OLLAMA_MODEL=gemma:2b
```

### For Production:
```bash
ollama pull llama2
# Update OLLAMA_MODEL=llama2
```

### For Best Quality:
```bash
ollama pull llama2:13b
# Update OLLAMA_MODEL=llama2:13b
```

## 🔄 Switching Models

```bash
# Pull new model
ollama pull mistral

# Update your configuration
# In .env file: OLLAMA_MODEL=mistral

# Restart your application
```

## 📝 Notes

- **First run**: Models are downloaded on first use (can take 5-30 minutes)
- **Storage**: Models are stored in `~/.ollama/models/` (can be several GB)
- **Memory**: Larger models need more RAM (13B needs ~16GB+ RAM)
- **Performance**: GPU acceleration available if you have CUDA-compatible GPU

## 🆘 Getting Help

- **Ollama Documentation**: https://ollama.com/docs
- **Model Library**: https://ollama.com/library
- **Community**: https://github.com/ollama/ollama/discussions

---

**Next Steps**: After setting up Ollama, run `python test_llm_service.py` to verify everything works!

