# mlpy v2.0: Security-First ML Language Compiler

> Revolutionary ML-to-Python transpiler combining capability-based security with production-ready tooling and native-level developer experience.

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 🎯 Project Overview

**mlpy v2.0** represents a breakthrough in programming language security, featuring:

- ✅ **Capability-based Security** - Token-controlled system access
- ✅ **Subprocess Sandbox** - True process isolation
- ✅ **Rich Developer Experience** - Source maps, profiling, IDE integration
- ✅ **Production-Ready Architecture** - Smart caching, comprehensive testing
- ✅ **Security-First Design** - Static analysis, runtime protection

## 🚀 Quick Start

### Prerequisites

- **Python 3.12+** (required for optimal performance)
- **Git** for version control
- **Make** for automation (optional but recommended)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/mlpy-v2.git
cd mlpy-v2

# Setup development environment
make setup-dev

# Verify installation
python -c "import mlpy; print(f'mlpy version: {mlpy.__version__}')"
```

### Basic Usage

```bash
# Create a simple ML program
echo 'function greet(name) { return `Hello, ${name}!` }' > hello.ml

# Transpile to Python (when implemented)
mlpy transpile hello.ml

# Run security audit (when implemented)
mlpy audit hello.ml
```

## 🏗️ Development

### Environment Setup

```bash
# Run all quality checks
make ci-test

# Run specific checks
make lint          # Code linting
make test          # Test suite
make security      # Security checks
make docs          # Build documentation
```

### Project Structure

```
mlpy-v2/
├── src/mlpy/                    # Main source code
│   ├── ml/                      # ML language core
│   ├── runtime/                 # Runtime system
│   ├── cli/                     # Command-line interface
│   └── ...
├── tests/                       # Test suite
├── docs/                        # Documentation
├── benchmarks/                  # Performance benchmarks
└── examples/                    # Example programs
```

## 🔒 Security Features

### Capability-Based Access Control

```ml
// ML code with capability-based security
with capability("file_write", path="./output/*") {
    message = greet("World")
    write_file("greeting.txt", message)
}
```

### Exploit Prevention

mlpy automatically blocks dangerous operations:
- `eval()` and `exec()` calls
- Unauthorized file system access
- Dangerous module imports
- Reflection-based attacks

## 📊 Development Status

**Current Sprint:** Foundation & Rich Errors (Sprint 1/7)

| Component | Status | Coverage |
|-----------|--------|----------|
| **Project Setup** | ✅ Complete | 100% |
| **Rich Error System** | 🔧 In Progress | - |
| **ML Parser** | 📋 Planned | - |
| **Security Analysis** | 📋 Planned | - |
| **Capability System** | 📋 Planned | - |
| **Sandbox Execution** | 📋 Planned | - |
| **IDE Integration** | 📋 Planned | - |

## 🧪 Testing

```bash
# Run all tests
make test

# Run specific test categories
make test-unit           # Unit tests
make test-integration    # Integration tests
make test-security       # Security tests
make test-performance    # Performance tests
```

## 📚 Documentation

- **Architecture Guide**: [docs/architecture/](docs/architecture/)
- **Security Model**: [docs/security/](docs/security/)
- **API Reference**: [docs/api/](docs/api/)
- **Examples**: [examples/](examples/)

## 🤝 Contributing

1. **Fork the repository** and create your feature branch
2. **Follow code style** guidelines (black, ruff, mypy)
3. **Write comprehensive tests** with 95%+ coverage
4. **Document your changes** with docstrings and examples
5. **Run security tests** to ensure no new vulnerabilities
6. **Submit a pull request** with detailed description

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🎯 Performance Targets

| Component | Target Performance | Priority |
|-----------|-------------------|----------|
| **Parse Simple** | < 0.1ms | High |
| **Security Analysis** | < 1ms | High |
| **Full Transpilation** | < 10ms | Critical |
| **Sandbox Startup** | < 100ms | Medium |

---

**Ready to revolutionize programming language security! 🚀🔒**