# Available Ollama Models for ResearchMate

## ✅ Confirmed Working Models

### Recommended Models (in order of preference):

1. **`llama2`** (7B) - Meta's Llama 2
   ```bash
   ollama pull llama2
   ```
   - **Size**: ~3.8GB
   - **RAM**: ~8GB
   - **Quality**: ⭐⭐⭐⭐
   - **Speed**: ⭐⭐⭐

2. **`mistral`** (7B) - Mistral AI
   ```bash
   ollama pull mistral
   ```
   - **Size**: ~4.1GB
   - **RAM**: ~8GB
   - **Quality**: ⭐⭐⭐⭐
   - **Speed**: ⭐⭐⭐⭐

3. **`phi3`** (3.8B) - Microsoft Phi-3
   ```bash
   ollama pull phi3
   ```
   - **Size**: ~2.3GB
   - **RAM**: ~6GB
   - **Quality**: ⭐⭐⭐
   - **Speed**: ⭐⭐⭐⭐⭐

4. **`gemma:2b`** (2B) - Google Gemma
   ```bash
   ollama pull gemma:2b
   ```
   - **Size**: ~1.6GB
   - **RAM**: ~4GB
   - **Quality**: ⭐⭐⭐
   - **Speed**: ⭐⭐⭐⭐⭐

5. **`codellama`** (7B) - Code-focused Llama
   ```bash
   ollama pull codellama
   ```
   - **Size**: ~3.8GB
   - **RAM**: ~8GB
   - **Quality**: ⭐⭐⭐⭐
   - **Speed**: ⭐⭐⭐

## 🚀 Quick Setup Commands

```bash
# Install Ollama (if not already installed)
# Windows: Download from https://ollama.com/download
# macOS: brew install ollama
# Linux: curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
ollama serve

# Pull a model (choose one)
ollama pull llama2        # Recommended for most users
ollama pull mistral       # Fast and efficient
ollama pull phi3          # Lightweight option
ollama pull gemma:2b      # Very fast, good for testing

# Verify installation
ollama list

# Test the model
ollama run llama2 "Hello, how are you?"
```

## 🔧 Update Your Configuration

### Option 1: Update .env file
```bash
# Create .env file with your chosen model
echo "OLLAMA_MODEL=llama2" > .env
```

### Option 2: Update config.py
```python
# In backend/app/core/config.py, line 47:
OLLAMA_MODEL: str = Field(
    default="llama2",  # Change to your preferred model
    description="Ollama model to use for text generation"
)
```

### Option 3: Environment variable
```bash
# Set environment variable
export OLLAMA_MODEL=llama2
```

## 📊 Model Comparison Table

| Model | Size | RAM | Quality | Speed | Best For |
|-------|------|-----|---------|-------|----------|
| `gemma:2b` | 2B | 4GB | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Quick testing |
| `phi3` | 3.8B | 6GB | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Balanced |
| `llama2` | 7B | 8GB | ⭐⭐⭐⭐ | ⭐⭐⭐ | Production |
| `mistral` | 7B | 8GB | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Fast + quality |
| `llama2:13b` | 13B | 16GB | ⭐⭐⭐⭐⭐ | ⭐⭐ | Best quality |

## 🧪 Test Your Setup

```bash
# 1. Check if Ollama is running
curl http://localhost:11434/api/tags

# 2. Test ResearchMate integration
cd backend
python test_llm_service.py

# 3. Manual model test
ollama run llama2 "Explain machine learning"
```

## ❌ Models NOT Available

These models are **NOT** available in Ollama:
- `llama3.2` - Not yet released
- `llama3` - Not yet released  
- `gpt-4` - OpenAI model (not in Ollama)
- `claude` - Anthropic model (not in Ollama)

## 🚨 Troubleshooting

### "Model not found" error
```bash
# Check available models
ollama list

# Pull the model you need
ollama pull llama2

# Verify it's available
ollama list
```

### "Connection refused" error
```bash
# Start Ollama service
ollama serve

# Check if it's running on port 11434
netstat -an | findstr 11434  # Windows
lsof -i :11434               # macOS/Linux
```

### Out of memory errors
```bash
# Use smaller models
ollama pull gemma:2b      # 2B parameters
ollama pull phi3          # 3.8B parameters
```

## 🎯 Recommended Setup by Use Case

### For Development/Testing:
```bash
ollama pull gemma:2b
# Fast, lightweight, good for testing
```

### For Production:
```bash
ollama pull llama2
# Good balance of quality and performance
```

### For Best Quality:
```bash
ollama pull llama2:13b
# Highest quality, needs more RAM
```

### For Speed:
```bash
ollama pull mistral
# Fast and efficient
```

---

**Next Step**: After choosing and installing a model, update your configuration and run `python test_llm_service.py` to verify everything works!

