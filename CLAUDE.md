# mlpy v2.0: Security-First ML Language Compiler

## Project Overview
Revolutionary ML-to-Python transpiler combining capability-based security with production-ready tooling and native-level developer experience.

## Architecture Overview
**Compilation Pipeline:** ML Source → Lark Parser → AST → Security Analysis → IR → Optimizations → Python AST + Source Maps

### Core Innovation: Capability-Based Security
- **Capability Tokens:** Fine-grained access control with resource patterns
- **Subprocess Sandbox:** True process isolation with resource limits
- **Static Security Analysis:** Compile-time detection of security vulnerabilities
- **Safe Built-ins:** Hardened runtime environment

## Development Environment
- **Python:** 3.12+ (required for optimal performance)
- **Build:** `make setup-dev` → `nox -s tests`
- **Test:** `make test` (95%+ Coverage requirement)
- **Security:** `make security` (Exploit-Prevention Tests)
- **Benchmark:** `make benchmarks` (Performance Regression Detection)

## Current Sprint Context
- **Sprint Status:** Sprint 1 - Foundation & Rich Errors
- **Current Focus:** Project setup, error system, profiling foundation
- **Blockers:** None - fresh start
- **Next Tasks:** Complete project structure, implement rich error system

## Coding Standards & Quality Gates
- **Test Coverage:** Minimum 95% for Core components
- **Security:** Zero vulnerabilities in Security tests
- **Performance:** <10ms Transpilation for typical programs
- **Code Quality:** Black + Ruff + MyPy strict compliance
- **Documentation:** All Public APIs with docstrings + examples

## Key Components Deep-Dive

### 1. ML Language Grammar (src/mlpy/ml/grammar/)
- **Lark-based Grammar:** Complete ML language features
- **Security Extensions:** Capability statements, security annotations
- **Performance:** Optimized for fast parsing of large files

### 2. Security Analysis (src/mlpy/ml/analysis/)
- **Dangerous Operation Detection:** Eval, Import, Reflection blocking
- **Capability Requirements:** Automatic capability detection
- **CWE-Mapping:** Security Issues with Common Weakness Enumeration

### 3. Capability System (src/mlpy/runtime/capabilities/)
- **Token-Based Access:** Granular resource control
- **Context Hierarchy:** Parent-child capability inheritance
- **Runtime Validation:** Performance-optimized capability checks

### 4. Sandbox Execution (src/mlpy/runtime/sandbox/)
- **Subprocess Isolation:** True process separation
- **Resource Limits:** CPU, Memory, File Size, Network controls
- **Security Monitoring:** Violation tracking and prevention

## Sprint-Specific Context
### Sprint 1: Foundation & Rich Errors (CURRENT)
- **Focus:** Project setup, error system, profiling foundation
- **Key Files:** src/mlpy/ml/errors/, src/mlpy/runtime/profiling/
- **Quality Gate:** Rich error formatting + profiling data collection

### Sprint 2: Security-First Parser (NEXT)
- **Focus:** Complete grammar, security analysis integration
- **Key Files:** src/mlpy/ml/grammar/, src/mlpy/ml/analysis/
- **Quality Gate:** All dangerous operations blocked + source positions accurate

## Implementation Principles
- **Security-First:** Every feature designed with security implications in mind
- **Performance-Conscious:** Sub-10ms transpilation target for typical programs
- **Developer-Friendly:** Rich errors, source maps, IDE integration
- **Production-Ready:** Comprehensive testing, benchmarking, documentation
- **Capability-Based:** Fine-grained access control throughout the system

## Key Performance Targets
| Component | Target Performance | Priority |
|-----------|-------------------|----------|
| **Parse Simple** | < 0.1ms | High |
| **Security Analysis** | < 1ms | High |
| **Capability Check** | < 0.01ms | High |
| **Full Transpilation** | < 10ms | Critical |
| **Sandbox Startup** | < 100ms | Medium |
| **Cache Lookup** | < 1ms | Medium |

## Security Requirements
- **Zero Dangerous Operations:** Complete blocking of eval, exec, dangerous imports
- **Capability Enforcement:** All system access must go through capability tokens
- **Sandbox Isolation:** True process-level isolation for code execution
- **Static Analysis:** Compile-time security validation with CWE mapping
- **Runtime Protection:** Dynamic security boundary enforcement

## Development Workflow
- **Branch Strategy:** Feature branches for each sprint component
- **Code Review:** Mandatory review for all core component changes
- **Testing:** Unit + integration + security tests before merge
- **Performance:** Benchmark validation for performance-critical changes
- **Documentation:** All public APIs documented with examples

## Quality Assurance
- **Test Coverage:** 95%+ for core compiler components
- **Security Testing:** Comprehensive exploit prevention test suite
- **Performance Testing:** Regression detection with baseline comparisons
- **Code Quality:** Automated linting, formatting, and type checking
- **Documentation:** Complete API documentation with usage examples