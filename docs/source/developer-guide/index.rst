===============
Developer Guide
===============

This guide is for contributors and advanced users who want to extend and modify mlpy. It covers the internal architecture, security model, and provides comprehensive instructions for adding new features.

.. toctree::
   :maxdepth: 2
   :caption: Architecture & Design

   architecture
   security-model
   compilation-pipeline
   runtime-systems

.. toctree::
   :maxdepth: 2
   :caption: Extending mlpy

   extending-mlpy
   writing-stdlib-modules
   bridge-system-guide
   grammar-extension-guide
   security-analysis-extension
   codegen-extension
   ide-tooling-integration

.. toctree::
   :maxdepth: 2
   :caption: Development Guidelines

   development-standards
   testing-guidelines
   security-review-process
   performance-optimization

.. toctree::
   :maxdepth: 2
   :caption: Advanced Topics

   custom-capability-systems
   cross-platform-considerations
   debugging-profiling-tools
   troubleshooting

Target Audience
===============

This documentation is intended for:

* **Core Contributors** - Developers working on mlpy itself
* **Extension Developers** - Creating standard library modules or language features
* **Integration Specialists** - Building advanced Python-ML bridges
* **Security Researchers** - Understanding and extending the security model
* **Tooling Developers** - Creating IDE plugins and development tools

Prerequisites
=============

Before diving into mlpy development, you should have:

* **Python 3.12+** with strong understanding of advanced features
* **Compiler Theory** basics (AST, parsing, code generation)
* **Security Concepts** including capability-based security
* **Testing Experience** with pytest and security testing
* **Performance Profiling** skills for optimization work

Quick Start for Contributors
============================

1. **Development Setup**::

    git clone https://github.com/your-org/mlpy
    cd mlpy
    make setup-dev
    nox -s tests

2. **Run Full Test Suite**::

    make test
    make security
    python test_comprehensive_security_audit.py

3. **Check Code Quality**::

    black src/ && ruff check src/ --fix && mypy src/mlpy/ml/analysis/

4. **Performance Validation**::

    make benchmarks
    cd tests/ml_integration && python test_runner.py

Architecture Overview
====================

mlpy uses a security-first architecture with five core components:

1. **Grammar & Parser** - Lark-based ML language parsing with AST generation
2. **Security Analysis** - Multi-threaded static analysis with threat detection
3. **Code Generation** - Python AST generation with source map support
4. **Runtime Systems** - Sandbox execution and capability management
5. **Standard Library** - Bridge system for Python interoperability

Each component is designed for extensibility while maintaining security guarantees.

Security-First Development
=========================

All mlpy development follows security-first principles:

* **Least Privilege** - Every operation requires explicit capability grants
* **Defense in Depth** - Multiple security layers from parsing to execution
* **Fail Secure** - Errors default to denying access rather than permitting
* **Audit Trail** - All security-relevant operations are logged and traceable

Performance Requirements
=======================

Core performance targets for contributions:

* **Parsing**: < 0.1ms for typical programs
* **Security Analysis**: < 1ms with parallel processing
* **Full Transpilation**: < 10ms for production code
* **Test Coverage**: 95%+ for all security-critical components

Getting Help
============

* **Development Questions**: Create GitHub discussions
* **Bug Reports**: Use GitHub issues with security label if applicable
* **Security Concerns**: Follow responsible disclosure process
* **Performance Issues**: Include benchmark data and profiling results