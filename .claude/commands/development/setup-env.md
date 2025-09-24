# Development Environment Setup

Complete setup of mlpy v2.0 development environment with all required dependencies, tools, and configurations.

Usage: `/development:setup-env`

## Setup Process

### 1. Python Environment Setup
```bash
# Create virtual environment
python3.12 -m venv .venv

# Activate environment (Windows)
.venv\Scripts\Activate.ps1

# Install mlpy in development mode
pip install -e .[dev,test,docs,benchmarks]
```

### 2. Development Tools Configuration
```bash
# Install pre-commit hooks
pre-commit install

# Configure nox sessions
nox --list

# Expected sessions:
# - tests: Run test suite with coverage
# - lint: Code linting (ruff)
# - format: Code formatting (black)
# - type-check: Type checking (mypy)
```

### 3. CLI Verification
```bash
# Verify mlpy CLI
mlpy --help
mlpy --version
mlpy --status

# Test basic functionality
echo 'function test() { return 42; }' > test.ml
mlpy transpile test.ml --sourcemap
rm test.*
```

## Validation Checklist

```
📋 Development Environment Checklist:
═══════════════════════════════════════

✅ Python 3.12+ installed and active
✅ Virtual environment created and activated
✅ Core packages installed (lark, pytest, rich, click)
✅ Development tools installed (black, ruff, mypy)
✅ Pre-commit hooks installed and working
✅ Test suite runs successfully
✅ mlpy CLI functional
✅ Documentation builds successfully
```

**Ready for mlpy v2.0 development! 🚀**