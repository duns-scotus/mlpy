# Development Environment Setup

Complete setup of mlpy v2.0 development environment.

Usage: /development:setup-env

## Setup Process:
1. **Python Environment**: Python 3.12 venv creation + activation
2. **Dependencies**: Install development dependencies via pip
3. **Pre-commit**: Setup hooks for code quality gates
4. **Development Tools**: Configure nox, black, ruff, mypy
5. **Testing Framework**: Setup pytest with coverage requirements
6. **Documentation**: Configure Sphinx with RTD theme
7. **Benchmarking**: Setup performance benchmarking infrastructure

## Validation Steps:
- Python 3.12+ available and active
- All development dependencies installed
- Pre-commit hooks functional
- Test suite runs with 95%+ coverage
- Documentation builds successfully
- CLI commands functional (mlpy --help)

## Environment Variables:
```bash
export PYTHONPATH=/path/to/mlpy/src
export MLPY_CACHE_DIR=/tmp/mlpy_cache
```

Generate setup verification report with troubleshooting steps.