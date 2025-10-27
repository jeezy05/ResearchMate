# Installation Guide - Python Version Compatibility

## Issue: Python 3.13 Compatibility

You're encountering installation errors because you're using **Python 3.13.2**, which is very new (released October 2024). Many Python packages don't yet have pre-built wheels for Python 3.13, causing `pydantic-core` and other packages to attempt compilation from source, which requires Rust.

---

## ✅ Recommended Solutions

### Option 1: Use Python 3.11 (RECOMMENDED)

Python 3.11 has the best compatibility with all our dependencies and pre-built wheels.

**Steps:**

1. **Install Python 3.11** from [python.org](https://www.python.org/downloads/)

2. **Create a virtual environment with Python 3.11:**
   ```bash
   # Windows
   py -3.11 -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3.11 -m venv venv
   source venv/bin/activate
   ```

3. **Upgrade pip:**
   ```bash
   python -m pip install --upgrade pip
   ```

4. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

---

### Option 2: Use Conda with Python 3.11

Since you have Miniconda installed:

```bash
# Create new environment with Python 3.11
conda create -n researchmate python=3.11 -y

# Activate the environment
conda activate researchmate

# Navigate to backend
cd backend

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

---

### Option 3: Continue with Python 3.13 (Advanced)

If you want to use Python 3.13, you have two approaches:

#### 3a. Install Rust (Required for building from source)

1. **Install Rust from [rustup.rs](https://rustup.rs/)**
   - Download and run: `rustup-init.exe`
   - Follow the installation prompts
   - Restart your terminal after installation

2. **Verify Rust installation:**
   ```bash
   rustc --version
   cargo --version
   ```

3. **Try installation again:**
   ```bash
   cd backend
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

#### 3b. Use Flexible Version Requirements

1. **Use the Python 3.13 compatible requirements:**
   ```bash
   cd backend
   pip install --upgrade pip
   pip install -r requirements-python313.txt
   ```

This uses flexible version constraints (`>=`) that will install the latest compatible versions.

---

## Current Versions in Your Environment

Based on the error output:
- **Python Version:** 3.13.2 (cp313)
- **OS:** Windows (win_amd64)
- **pip Version:** 25.1.1 (update available to 25.2)

---

## Quick Fix Commands

### For Python 3.11 with Conda (RECOMMENDED):

```bash
# Create and activate new environment
conda create -n researchmate python=3.11 -y
conda activate researchmate

# Navigate and install
cd backend
pip install --upgrade pip
pip install -r requirements.txt

# Verify installation
python --version  # Should show 3.11.x
pip list
```

### For Python 3.13 with Flexible Versions:

```bash
cd backend
python -m pip install --upgrade pip
pip install -r requirements-python313.txt
```

---

## Verification

After successful installation, verify with:

```bash
python -c "import fastapi; import pydantic; import langchain; print('✓ All packages imported successfully')"
```

---

## Why Python 3.11 is Recommended

1. **Pre-built wheels** - All packages have pre-built wheels for Python 3.11
2. **Stable** - Python 3.11 has been out since October 2022
3. **Performance** - Python 3.11 has significant performance improvements over 3.10
4. **Compatibility** - Better ecosystem support than 3.13

Python 3.13 benefits:
- Latest features
- Better performance
- But: Limited package ecosystem support (will improve over time)

---

## Troubleshooting

### Issue: "Rust not found" error

**Solution:** Either:
- Use Python 3.11 (recommended)
- Install Rust from https://rustup.rs/

### Issue: "Microsoft Visual C++ 14.0 is required"

**Solution:** Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022)

Or use Python 3.11 which has pre-built wheels.

### Issue: Conda environment activation issues

**Solution:**
```bash
# Initialize conda for PowerShell (Windows)
conda init powershell

# Restart terminal, then:
conda activate researchmate
```

---

## Testing Installation

After successful installation:

```bash
# Test configuration
cd backend
python test_config.py

# Test document processor
python test_document_processor.py

# Start the server
uvicorn app.main:app --reload
```

---

## Docker Alternative

If you prefer to avoid Python version issues entirely, use Docker:

```bash
# Build and run with Docker
docker-compose up --build

# This uses Python 3.11 in the container
```

The Dockerfile already specifies Python 3.11-slim, avoiding these compatibility issues.

---

## Summary

**Quick Answer:** Use Python 3.11 with Conda:

```bash
conda create -n researchmate python=3.11 -y
conda activate researchmate
cd backend
pip install --upgrade pip
pip install -r requirements.txt
```

This will resolve all installation issues! 🎉

