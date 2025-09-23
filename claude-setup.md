# mlpy v2.0 Claude Code Setup Guide
## Optimales Setup für Security-First ML Language Compiler

> **Ziel:** Claude Code optimal für die mlpy v2.0 Entwicklung konfigurieren - von Foundation bis Production-Ready Release

---

## 📋 Inhaltsverzeichnis

1. [Projekt-Setup für mlpy v2.0](#projekt-setup-für-mlpy-v20)
2. [Claude Code Konfiguration](#claude-code-konfiguration)
3. [Custom Commands für ML Compiler](#custom-commands-für-ml-compiler)
4. [Context Management Strategy](#context-management-strategy)
5. [MCP Server Integration](#mcp-server-integration)
6. [7-Sprint Development Workflow](#7-sprint-development-workflow)
7. [Quality Gates & Automation](#quality-gates--automation)
8. [Performance Optimization](#performance-optimization)

---

## 🚀 Projekt-Setup für mlpy v2.0

### Essential Project Structure

```
mlpy-v2/
├── CLAUDE.md                          # Haupt-Projektbeschreibung für Claude
├── .claude/
│   ├── settings.json                  # Claude Code Projekteinstellungen
│   ├── settings.local.json            # Persönliche Overrides (gitignored)
│   ├── commands/                      # Custom Slash Commands
│   │   ├── sprint/
│   │   │   ├── foundation.md          # Sprint 1: Foundation Commands
│   │   │   ├── parser.md              # Sprint 2: Parser Commands
│   │   │   ├── ir-sourcemaps.md       # Sprint 3: IR + Source Maps
│   │   │   ├── capabilities.md        # Sprint 4: Capability System
│   │   │   ├── sandbox.md             # Sprint 5: Sandbox Commands
│   │   │   ├── ide-integration.md     # Sprint 6: LSP/DAP Commands
│   │   │   └── production.md          # Sprint 7: Production Polish
│   │   ├── ml-compiler/
│   │   │   ├── transpile-test.md      # ML → Python Transpilation
│   │   │   ├── security-audit.md     # Security Analysis Commands
│   │   │   ├── performance-bench.md   # Performance Benchmarking
│   │   │   └── debug-pipeline.md     # Debug Transpilation Pipeline
│   │   ├── development/
│   │   │   ├── setup-env.md           # Environment Setup
│   │   │   ├── run-tests.md           # Test Execution
│   │   │   ├── code-review.md         # Code Review Checklist
│   │   │   └── deploy-package.md      # Package Deployment
│   │   └── security/
│   │       ├── capability-test.md     # Capability System Testing
│   │       ├── sandbox-verify.md     # Sandbox Security Verification
│   │       └── exploit-prevention.md # Exploit Prevention Testing
│   ├── agents/                       # Specialized AI Subagents
│   │   ├── security-expert.md        # Security Analysis Specialist
│   │   ├── ml-compiler-expert.md     # ML Language Expert
│   │   ├── python-transpiler.md      # Python Code Generation Expert
│   │   ├── performance-engineer.md   # Performance Optimization
│   │   └── test-engineer.md          # Testing Strategy Expert
│   └── hooks.mjs                     # Workflow Automation Hooks
├── .mcp.json                         # MCP Server Configuration
├── .pre-commit-config.yaml           # Quality Gates Integration
├── src/mlpy/                         # Main source code
│   ├── CLAUDE.md                     # Source-spezifische Guidelines
│   ├── ml/                           # ML language core
│   │   ├── CLAUDE.md                 # ML Core Context
│   │   ├── grammar/
│   │   │   └── CLAUDE.md             # Grammar Development Context
│   │   ├── ast/
│   │   │   └── CLAUDE.md             # AST Implementation Context
│   │   ├── analysis/
│   │   │   └── CLAUDE.md             # Security Analysis Context
│   │   └── parser/
│   │       └── CLAUDE.md             # Parser Implementation Context
│   ├── runtime/                      # Runtime system
│   │   ├── CLAUDE.md                 # Runtime Context
│   │   ├── capabilities/
│   │   │   └── CLAUDE.md             # Capability System Context
│   │   └── sandbox/
│   │       └── CLAUDE.md             # Sandbox Implementation Context
│   └── cli/
│       └── CLAUDE.md                 # CLI Development Context
└── tests/
    ├── CLAUDE.md                     # Testing Strategy Context
    ├── unit/
    ├── integration/
    ├── security/
    └── performance/
```

### Haupt-CLAUDE.md für mlpy v2.0

```markdown
# mlpy v2.0: Security-First ML Language Compiler

## Projekt Overview
Revolutionary ML-to-Python transpiler combining capability-based security with production-ready tooling and native-level developer experience.

## Architecture Overview
**Compilation Pipeline:** ML Source → Lark Parser → AST → Security Analysis → IR → Optimizations → Python AST + Source Maps

### Core Innovation: Capability-Based Security
- **Capability Tokens:** Fine-grained access control with resource patterns
- **Subprocess Sandbox:** True process isolation with resource limits
- **Static Security Analysis:** Compile-time detection of security vulnerabilities
- **Safe Built-ins:** Hardened runtime environment

## Development Environment
- **Python:** 3.12+ (empfohlen für optimale Performance)
- **Build:** `make setup-dev` → `nox -s tests`
- **Test:** `make test` (95%+ Coverage-Anforderung)
- **Security:** `make security` (Exploit-Prevention Tests)
- **Benchmark:** `make benchmarks` (Performance Regression Detection)

## Current Sprint Context
- **Sprint Status:** [Wird von Claude aktualisiert]
- **Current Focus:** [Aktueller Sprint-Fokus]
- **Blockers:** [Aktuelle Blocker]
- **Next Tasks:** [Nächste Aufgaben]

## Coding Standards & Quality Gates
- **Test Coverage:** Minimum 95% für Core-Komponenten
- **Security:** Zero vulnerabilities in Security-Tests
- **Performance:** <10ms Transpilation für typische Programme
- **Code Quality:** Black + Ruff + MyPy strict compliance
- **Documentation:** Alle Public APIs mit docstrings + Beispielen

## Key Components Deep-Dive

### 1. ML Language Grammar (src/mlpy/ml/grammar/)
- **Lark-basierte Grammar:** Vollständige ML-Sprachfeatures
- **Security Extensions:** Capability statements, security annotations
- **Performance:** Optimiert für schnelles Parsing großer Dateien

### 2. Security Analysis (src/mlpy/ml/analysis/)
- **Dangerous Operation Detection:** Eval, Import, Reflection blocking
- **Capability Requirements:** Automatische Capability-Erkennung
- **CWE-Mapping:** Security Issues mit Common Weakness Enumeration

### 3. Capability System (src/mlpy/runtime/capabilities/)
- **Token-Based Access:** Granulare Ressourcen-Kontrolle
- **Context Hierarchy:** Parent-Child Capability-Vererbung
- **Runtime Validation:** Performance-optimierte Capability-Checks

### 4. Sandbox Execution (src/mlpy/runtime/sandbox/)
- **Subprocess Isolation:** Echte Prozess-Trennung
- **Resource Limits:** CPU, Memory, File Size, Network Controls
- **Security Monitoring:** Violation Tracking und Prevention

## Sprint-Specific Context
### Sprint 1: Foundation & Rich Errors
- **Focus:** Project setup, error system, profiling foundation
- **Key Files:** src/mlpy/ml/errors/, src/mlpy/runtime/profiling/
- **Quality Gate:** Rich error formatting + profiling data collection

### Sprint 2: Security-First Parser  
- **Focus:** Complete grammar, security analysis integration
- **Key Files:** src/mlpy/ml/grammar/, src/mlpy/ml/analysis/
- **Quality Gate:** All dangerous operations blocked + source positions accurate

### Sprint 3: IR System + Source Maps
- **Focus:** Intermediate representation, transpiler cache, source maps
- **Key Files:** src/mlpy/ml/ir/, src/mlpy/codegen/, src/mlpy/cache/
- **Quality Gate:** Source maps enable debugging + cache reduces compilation time

### Sprint 4: Capability System
- **Focus:** Production-ready capability-based security
- **Key Files:** src/mlpy/runtime/capabilities/, src/mlpy/runtime/system_modules/
- **Quality Gate:** Capability tokens prevent unauthorized access

### Sprint 5: Sandbox Execution
- **Focus:** Secure subprocess-based execution
- **Key Files:** src/mlpy/runtime/sandbox/
- **Quality Gate:** Sandbox prevents escape attempts + resource limits enforced

### Sprint 6: IDE Integration
- **Focus:** LSP/DAP for professional IDE support
- **Key Files:** src/mlpy/lsp/, src/mlpy/dap/
- **Quality Gate:** LSP diagnostics + DAP debugging functional

### Sprint 7: Production Polish
- **Focus:** Documentation, benchmarks, security hardening
- **Key Files:** docs/, benchmarks/, deployment configs
- **Quality Gate:** Production-ready release with comprehensive docs
```

---

## ⚙️ Claude Code Konfiguration

### Advanced Settings Configuration

```json
{
  "projects": {
    "/path/to/mlpy-v2": {
      "mcpServers": {
        "filesystem": {
          "command": "npx",
          "args": ["-y", "@modelcontextprotocol/server-filesystem", 
                   "./src", "./tests", "./docs", "./benchmarks", "./examples"]
        },
        "memory": {
          "command": "npx", 
          "args": ["-y", "@modelcontextprotocol/server-memory"]
        },
        "sequential-thinking": {
          "command": "npx",
          "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
        },
        "github": {
          "command": "npx",
          "args": ["-y", "@modelcontextprotocol/server-github"],
          "env": {
            "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
          }
        }
      },
      "allowedTools": [
        "Task", "Bash(make *)", "Bash(nox *)", "Bash(python *)", "Bash(pytest *)",
        "Bash(git *)", "Glob", "Grep", "Read", "Edit", "MultiEdit", "Write"
      ],
      "permissions": {
        "allow": [
          "Bash(make test)", "Bash(make lint)", "Bash(make setup-dev)",
          "Bash(nox -s *)", "Bash(pytest tests/)", "Bash(python -m mlpy *)",
          "Read(src/**)", "Write(src/**)", "Read(tests/**)", "Write(tests/**)",
          "Read(docs/**)", "Write(docs/**)", "Read(benchmarks/**)", "Write(benchmarks/**)"
        ],
        "deny": [
          "Bash(rm -rf *)", "Bash(pip install *)", "Read(.env*)", 
          "Write(pyproject.toml)", "Write(.github/workflows/**)"
        ]
      }
    }
  }
}
```

### Quality Gates Integration

```yaml
# .pre-commit-config.yaml (Enhanced für Claude Code)
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml

  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black
        language_version: python3.12

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.0.287
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]

  - repo: local
    hooks:
      - id: mlpy-core-tests
        name: mlpy Core Tests
        entry: nox -s tests
        language: system
        files: '^src/mlpy/.*\.py$'
        pass_filenames: false

      - id: mlpy-security-audit
        name: mlpy Security Audit
        entry: nox -s security
        language: system
        pass_filenames: false

      - id: mlpy-performance-check
        name: Performance Regression Check
        entry: make benchmarks
        language: system
        files: '^(src|benchmarks)/.*\.py$'
        pass_filenames: false
```

---

## 🛠️ Custom Commands für ML Compiler

### Sprint-Specific Commands

```markdown
# .claude/commands/sprint/foundation.md
# Sprint 1: Foundation & Rich Errors

Setup und Implementation der Projekt-Foundation mit Rich Error System.

Usage: /sprint:foundation [component]

## Implementation Process:
1. **Project Structure**: Erstelle vollständige Verzeichnisstruktur
2. **Virtual Environment**: Setup Python 3.12 venv + dependencies  
3. **Rich Error System**: Implementiere ErrorContext mit source lines + suggestions
4. **Profiling Foundation**: Profiling decorators für alle Komponenten
5. **CLI Interface**: Basic CLI mit Rich-Interface
6. **Quality Gates**: Pre-commit hooks, nox sessions, CI/CD basis

## Quality Validation:
- 100% test coverage für implementierte Komponenten
- Rich error formatting funktional
- Profiling data collection aktiv
- Alle pre-commit hooks passing

Focus: Solide Foundation für nachfolgende Sprints.
```

```markdown
# .claude/commands/sprint/parser.md
# Sprint 2: Security-First Parser

Implementation des ML Parsers mit integrierter Security Analysis.

Usage: /sprint:parser [focus-area]

## Implementation Process:
1. **Complete Grammar**: Vollständige Lark grammar (nicht minimal)
2. **Parse Tree → AST**: Transformer mit Source Position Tracking
3. **Security Analysis**: SecurityAnalyzer mit dangerous operation detection
4. **AST Integration**: Rich AST nodes mit UUIDs + source positions
5. **Error Integration**: Security errors mit CWE-mapping + suggestions
6. **CLI Integration**: Parser commands mit security reporting

## Security Focus Areas:
- **Dangerous Builtins**: eval, exec, __import__, open blocking
- **Reflection Abuse**: __class__, __bases__ access prevention  
- **Import Control**: Dangerous module import detection
- **Capability Requirements**: Automatische capability detection

## Quality Validation:
- Parser handles alle ML language features
- Security analysis blocks alle dangerous operations  
- Source positions accurate für debugging
- Rich errors für syntax issues

Focus: Security-First von der ersten Zeile Code.
```

```markdown
# .claude/commands/sprint/capabilities.md
# Sprint 4: Capability System

Implementation des production-ready Capability-Systems.

Usage: /sprint:capabilities [component]

## Implementation Process:
1. **Core Capability System**: CapabilityToken mit constraints + expiration
2. **Capability Manager**: Thread-safe context hierarchy management
3. **Runtime Integration**: Decorators + context managers für sichere API calls
4. **System Modules**: Safe built-ins mit capability integration
5. **CallbackBridge**: Secure System ↔ ML communication
6. **Example Modules**: math_safe, file_safe implementation

## Security Architecture:
- **Token-Based Access**: Granulare resource patterns + constraints
- **Context Hierarchy**: Parent-child capability inheritance
- **Runtime Validation**: Performance-optimierte capability checks
- **Safe Built-ins**: Hardened replacements für dangerous functions

## Integration Points:
- **Parser Integration**: Capability statements in ML grammar
- **Security Analysis**: Automatic capability requirement detection
- **Runtime System**: Safe execution environment mit capability checks
- **System Modules**: Controlled access zu system functions

## Quality Validation:
- Capability tokens prevent unauthorized access
- System modules work securely
- Runtime validation ist performant
- Callback bridge maintains security boundaries

Focus: Zero-Trust Security Model mit usable API.
```

### ML Compiler Commands

```markdown
# .claude/commands/ml-compiler/transpile-test.md
# ML → Python Transpilation Testing

Comprehensive testing of ML to Python transpilation pipeline.

Usage: /ml-compiler:transpile-test [test-category]

## Test Categories:
1. **Basic Syntax**: Variables, functions, control flow
2. **Security Features**: Capability statements, security annotations
3. **Advanced Features**: Lambda expressions, template strings, classes
4. **Edge Cases**: Complex nesting, error conditions, performance limits

## Transpilation Process:
1. Parse ML source with full error handling
2. Run security analysis with capability detection
3. Generate IR with optimization passes
4. Create Python AST with source map generation
5. Validate generated Python syntax + semantics
6. Test execution in sandbox environment

## Validation Steps:
- Source maps provide accurate ML ↔ Python mapping
- Security restrictions properly enforced
- Generated Python is readable + maintainable
- Performance meets target (<10ms for typical programs)
- Cache system reduces repeat transpilation time

Generate comprehensive test report mit specific fixes für failures.
```

```markdown
# .claude/commands/ml-compiler/security-audit.md
# ML Language Security Audit

Comprehensive security analysis of ML language features and runtime.

Usage: /ml-compiler:security-audit [scope]

## Audit Scope:
1. **Language Features**: Security implications of all ML constructs
2. **Runtime Security**: Capability system, sandbox, safe built-ins
3. **Transpilation Security**: Code injection prevention, output validation
4. **System Integration**: MCP servers, CLI tools, IDE integration

## Security Analysis Process:
1. **Static Analysis**: Scan all dangerous operation patterns
2. **Dynamic Testing**: Execute exploit test suite
3. **Capability Validation**: Test capability system boundaries
4. **Sandbox Testing**: Verify process isolation + resource limits
5. **Penetration Testing**: Attempt known bypass techniques

## Exploit Prevention Testing:
- **Code Injection**: eval(), exec(), compile() bypasses
- **Reflection Abuse**: __class__, __globals__ access attempts
- **Import Bypasses**: sys.modules, importlib manipulation
- **Sandbox Escapes**: Process isolation, resource limit bypasses
- **Capability Bypasses**: Token manipulation, context pollution

## Report Generation:
- Security issue summary mit CWE mappings
- Exploit test results mit prevention verification
- Performance impact of security measures
- Recommendations für security hardening

Focus: Comprehensive security validation mit zero tolerance für bypasses.
```

### Development Workflow Commands

```markdown
# .claude/commands/development/setup-env.md
# Development Environment Setup

Complete setup of mlpy v2.0 development environment.

Usage: /development:setup-env

## Setup Process:
1. **Python Environment**: Python 3.12 venv creation + activation
2. **Dependencies**: Install development dependencies via pip
3. **Pre-commit**: Setup hooks für code quality gates
4. **Development Tools**: Configure nox, black, ruff, mypy
5. **Testing Framework**: Setup pytest mit coverage requirements
6. **Documentation**: Configure Sphinx mit RTD theme
7. **Benchmarking**: Setup performance benchmarking infrastructure

## Validation Steps:
- Python 3.12+ verfügbar und aktiv
- Alle development dependencies installiert
- Pre-commit hooks funktional
- Test suite läuft mit 95%+ coverage
- Documentation builds erfolgreich
- CLI commands funktional (mlpy --help)

## Environment Variables:
```bash
export PYTHONPATH=/path/to/mlpy-v2/src
export MLPY_CACHE_DIR=/tmp/mlpy_cache  
export ANTHROPIC_API_KEY=your_key_here
```

Generate setup verification report mit troubleshooting steps.
```

---

## 📚 Context Management Strategy

### Hierarchical Context System

```markdown
# src/mlpy/CLAUDE.md (Source-Level Context)

## mlpy Source Code Architecture

### Module Organization
- **ml/**: Core ML language implementation (parser, AST, analysis)
- **runtime/**: Runtime system (capabilities, sandbox, profiling)
- **cli/**: Command-line interface mit Rich integration
- **cache/**: Transpilation caching system
- **debugging/**: Source maps, error formatting, DAP integration

### Coding Standards
- **Type Hints**: Alle functions mit complete type annotations
- **Error Handling**: Comprehensive error handling mit MLError hierarchy
- **Documentation**: Docstrings für alle public APIs + usage examples
- **Testing**: 95%+ coverage requirement für core components
- **Security**: Security-first design in allen components

### Development Workflow
- **Branch Strategy**: Feature branches für jeden Sprint
- **Code Review**: Mandatory review für alle core component changes
- **Testing**: Unit + integration + security tests vor merge
- **Performance**: Benchmark validation für performance-critical changes

### Integration Points
- **Parser ↔ Security**: AST nodes mit security metadata
- **IR ↔ Codegen**: Source map generation während code generation
- **Runtime ↔ CLI**: Profiling data collection + reporting
- **Sandbox ↔ Capabilities**: Secure execution environment
```

```markdown
# src/mlpy/ml/CLAUDE.md (ML Core Context)

## ML Language Core Implementation

### Language Features
- **Syntax**: Python-inspired mit security extensions
- **Type System**: Dynamic typing mit optional static analysis
- **Security**: Capability statements, safe built-ins, sandbox execution
- **Performance**: Optimiert für fast transpilation + execution

### Grammar Architecture  
- **Base Grammar**: Standard programming constructs (functions, classes, control flow)
- **Security Extensions**: `with capability()` statements, security annotations
- **Template Features**: Template strings mit interpolation
- **Advanced Features**: Lambda expressions, destructuring, async/await

### AST Design
- **Node Hierarchy**: Comprehensive AST node types mit security metadata
- **Source Positions**: Accurate source position tracking für debugging
- **Security Metadata**: Capability requirements, security annotations
- **Optimization Hints**: Performance optimization markers

### Security Analysis Pipeline
1. **Dangerous Operation Detection**: eval, exec, __import__ blocking
2. **Capability Analysis**: Automatic capability requirement detection  
3. **Flow Analysis**: Security constraint propagation
4. **Error Generation**: Rich security errors mit CWE mapping + suggestions

Focus: Comprehensive language implementation mit security-first design.
```

### Strategic Context Loading Patterns

```bash
# Focused context loading für specific work
claude "Analyze only the capability system" @src/mlpy/runtime/capabilities/

# Multi-file context für integration work
claude "Review parser-security interface" @src/mlpy/ml/parser/ @src/mlpy/ml/analysis/

# Sprint-specific context loading
claude "Load Sprint 4 context" @CLAUDE.md @src/mlpy/runtime/capabilities/ @.claude/commands/sprint/capabilities.md

# Context priming für security work
> Load security context from @src/mlpy/ml/analysis/CLAUDE.md
> Focus on capability integration in @src/mlpy/runtime/capabilities/
> Review security test patterns in @tests/security/
> Now design the security annotation validation system

# Performance-focused context
> Load performance context from @benchmarks/
> Compare current metrics with @benchmarks/baselines/
> Focus on transpilation pipeline in @src/mlpy/ml/
> Optimize hot paths identified in profiling data
```

---

## 🔧 MCP Server Integration

### Essential MCP Servers für mlpy v2.0

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", 
               "./src", "./tests", "./docs", "./benchmarks", "./examples"]
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    "sequential-thinking": {
      "command": "npx", 
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "web-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "${BRAVE_API_KEY}"
      }
    },
    "python-execution": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-python"],
      "env": {
        "PYTHON_VENV_PATH": "./venv"
      }
    }
  }
}
```

### Advanced MCP Workflows für Research + Development

```bash
# Research aktuelle compiler techniques
> @web-search "Python AST manipulation security 2024"
> @github:python/cpython analyze recent security fixes in Python AST

# Cross-reference mit academic papers für capability systems  
> @web-search "capability-based security programming languages 2024"
> Compare approaches with our implementation in @src/mlpy/runtime/capabilities/

# Performance research für transpilation optimization
> @web-search "fast Python AST generation techniques"
> @github:lark-parser/lark check latest optimization approaches
> Apply findings to @src/mlpy/ml/parser/ implementation
```

---

## 🏗️ 7-Sprint Development Workflow

### Plan Mode für Complex Architectural Decisions

```bash
# Activate plan mode with Shift+Tab twice
[Plan Mode Activated]

# Sprint 4 Capability System Planning
> Read Sprint 4 requirements from @docs/sprints/sprint-4-goals.md
> Analyze current capability system architecture in @src/mlpy/runtime/capabilities/
> Review security requirements from @src/mlpy/ml/analysis/security.py
> Propose detailed implementation plan for:
  - Advanced capability token system mit constraints
  - Context hierarchy für capability inheritance  
  - Runtime validation mit performance optimization
  - System module integration für safe built-ins
  - CallbackBridge für secure system communication
> Estimate effort in story points (Fibonacci scale)
> Identify dependencies auf other components (parser, runtime, CLI)
> Create risk mitigation strategies für complex security algorithms
> Generate comprehensive testing strategy including exploit prevention
> Plan integration with existing security analysis pipeline
```

### Multi-Agent Sprint Orchestration

```bash
# Sprint planning mit specialized agents
> use the security-expert agent to analyze Sprint 4 capability requirements
> use the ml-compiler-expert agent to design capability integration points
> use the performance-engineer agent to review proposed capability validation system
> use the test-engineer agent to create comprehensive exploit test strategy

# Implementation coordination
> use the python-transpiler agent für safe built-in replacements
> use the security-expert agent für capability token validation
> use the performance-engineer agent für optimization of hot paths
```

### ROADMAP.md-Driven Development

```markdown
# mlpy v2.0 Development Roadmap

## Sprint Progress Convention
- `[ ]` Todo | `[-]` In Progress 🏗️ | `[x]` Completed ✅

## Sprint 4/7: Capability System (Current)
- [-] **Core Capability Token System** 🏗️
  - Token-based access control mit resource patterns + constraints
  - Est: 13 points | Started: 2025/01/15 | ETA: 2025/01/22
  - Dependencies: Security analysis integration
  - Risks: Performance impact, complexity management

- [-] **Capability Manager Implementation** 🏗️  
  - Thread-safe context hierarchy mit parent-child inheritance
  - Est: 8 points | Dependencies: Token system

- [ ] **System Module Integration**
  - Safe built-ins mit capability checks (math_safe, file_safe)
  - Est: 8 points | Dependencies: Capability manager

- [ ] **CallbackBridge Implementation**
  - Secure System ↔ ML communication bridge
  - Est: 5 points | Dependencies: System modules

## Recently Completed
- [x] **Rich Error System** ✅ Sprint 1 Completed 2025/01/08
  - ErrorContext mit source lines + suggestions + CWE mapping
  - Performance: 5x faster error reporting, Rich formatting
- [x] **Security-First Parser** ✅ Sprint 2 Completed 2025/01/15
  - Complete Lark grammar + SecurityAnalyzer integration
  - Security: All dangerous operations blocked, 100% coverage

## Sprint 5/7: Sandbox Execution (Planned)
- [ ] **Subprocess Sandbox Implementation**
- [ ] **Resource Limits + Security Monitoring**
- [ ] **Platform-Specific Isolation** (Linux/macOS/Windows)

## Sprint 6/7: IDE Integration (Planned)  
- [ ] **LSP Server Implementation**
- [ ] **DAP Adapter mit Source Map Integration**
- [ ] **VSCode Extension + Configuration**

## Sprint 7/7: Production Polish (Planned)
- [ ] **Comprehensive Documentation**
- [ ] **Performance Benchmarking + Optimization**
- [ ] **Security Hardening + Penetration Testing**
- [ ] **Package Distribution + Deployment**
```

---

## ⚡ Quality Gates & Automation

### Workflow Automation mit Hooks

```javascript
// .claude/hooks.mjs
import { execSync } from 'child_process';

export async function preEdit({ filePath, oldContent, newContent }) {
  // Protect critical mlpy core files
  const criticalFiles = [
    'src/mlpy/__init__.py',
    'pyproject.toml', 
    'src/mlpy/ml/grammar/ml.lark',
    'src/mlpy/runtime/capabilities/manager.py'
  ];
  
  if (criticalFiles.includes(filePath)) {
    console.log('⚠️ Editing critical mlpy core file - review carefully');
  }

  // Validate Python syntax before editing
  if (filePath.endsWith('.py')) {
    try {
      execSync(`python -m py_compile "${filePath}"`, { stdio: 'pipe' });
    } catch (e) {
      console.log('⚠️ Python syntax errors detected');
    }
  }

  // Validate Lark grammar syntax
  if (filePath.endsWith('.lark')) {
    try {
      execSync(`python -c "from lark import Lark; Lark(open('${filePath}').read())"`, { stdio: 'pipe' });
    } catch (e) {
      console.log('⚠️ Lark grammar syntax errors detected');
    }
  }

  return { proceed: true };
}

export async function postEdit({ filePath, success }) {
  if (!success) return;

  // Auto-format Python code
  if (filePath.endsWith('.py')) {
    try {
      execSync(`black "${filePath}"`, { stdio: 'pipe' });
      execSync(`ruff check --fix "${filePath}"`, { stdio: 'pipe' });
    } catch (e) {
      console.log('⚠️ Code formatting failed - manual formatting needed');
    }
  }

  // Run quick tests für core modules
  if (filePath.includes('src/mlpy/ml/') || filePath.includes('src/mlpy/runtime/')) {
    try {
      execSync('nox -s tests -- --tb=short -x', { stdio: 'pipe' });
    } catch (e) {
      console.log('⚠️ Core tests failed - review changes');
    }
  }

  // Security validation für capability system changes
  if (filePath.includes('capabilities/') || filePath.includes('security/')) {
    try {
      execSync('nox -s tests_security -- --tb=short', { stdio: 'pipe' });
    } catch (e) {
      console.log('⚠️ Security tests failed - critical security review needed');
    }
  }
}
```

### Automated Quality Gates

```markdown
# .claude/commands/quality/sprint-health-check.md
# Sprint Quality Health Check

Analyze code quality metrics across the current sprint.

Usage: /quality:sprint-health-check

## Quality Metrics für mlpy v2.0:
1. **Test Coverage**: Minimum 95% für core compiler components
2. **Security Coverage**: Zero vulnerabilities in security test suite
3. **Performance**: No regressions >5% in transpilation speed
4. **Code Quality**: Black + Ruff + MyPy strict compliance
5. **Documentation**: All public APIs documented mit examples

## Analysis Process:
- Generate coverage report: `nox -s tests -- --cov-report=html`
- Run security audit: `nox -s security`
- Performance benchmarks: `make benchmarks`
- Code quality check: `nox -s lint mypy`
- Documentation validation: `nox -s docs`

## mlpy-Specific Checks:
- **ML Grammar Validation**: Lark grammar syntax + completeness
- **Security Analysis Coverage**: All dangerous operations detected
- **Capability System Tests**: Token validation + context hierarchy
- **Sandbox Security**: Process isolation + resource limits
- **Source Map Accuracy**: ML ↔ Python mapping validation

Generate comprehensive quality dashboard mit specific improvement recommendations.
```

### CI/CD Integration mit Claude Automation

```yaml
# .github/workflows/claude-assisted-mlpy-ci.yml
name: Claude-Assisted mlpy v2.0 CI

on: [push, pull_request]

jobs:
  claude-security-analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python 3.12
        uses: actions/setup-python@v4
        with:
          python-version: "3.12"
        
      - name: Install Claude Code
        run: curl -fsSL https://claude.ai/install.sh | sh
        
      - name: mlpy Security Analysis
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude -p "
          Analyze this mlpy v2.0 codebase for:
          1. Security vulnerabilities in ML parsing/transpilation
          2. Capability system implementation security
          3. Sandbox escape prevention effectiveness
          4. Runtime security boundary validation
          
          Focus on changes in this PR and provide specific security fixes.
          Generate exploit prevention test cases für any identified issues.
          " @src/mlpy/ @tests/security/ > claude-security-analysis.md
          
      - name: Comment Security Analysis on PR
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const analysis = fs.readFileSync('claude-security-analysis.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## 🛡️ Claude Security Analysis für mlpy v2.0\n\n${analysis}`
            });

  claude-performance-analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python 3.12
        uses: actions/setup-python@v4
        with:
          python-version: "3.12"
          
      - name: Install Dependencies
        run: |
          pip install -e .[dev]
          
      - name: Performance Analysis mit Claude
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          make benchmarks
          claude -p "
          Analyze mlpy v2.0 performance benchmarks:
          1. Transpilation speed performance (target: <10ms)
          2. Security analysis overhead (target: <5% total time)
          3. Memory usage patterns (target: <128MB für typical programs)
          4. Cache effectiveness (target: 90%+ cache hit rate)
          
          Compare with baseline metrics and identify bottlenecks.
          Provide specific optimization recommendations.
          " @benchmarks/results/ > claude-performance-analysis.md
```

---

## 🚀 Performance Optimization

### Token-Efficient Development Patterns

```bash
# Focused context loading statt broad analysis
> Load capability system context from @src/mlpy/runtime/capabilities/manager.py
> Compare with security requirements in @src/mlpy/ml/analysis/security.py
> Focus on: token validation performance, context hierarchy optimization

# Strategic model selection für different tasks
export ANTHROPIC_MODEL="claude-sonnet-4-20250514"  # For implementation work
claude --model opus "Design the overall capability system architecture"  # For planning
claude --model haiku "Format this Python code according to PEP 8"  # For simple tasks

# Batch operations für efficiency
> Analyze all security components: @src/mlpy/ml/analysis/ @src/mlpy/runtime/capabilities/ @tests/security/
> Generate comprehensive security review mit optimization recommendations
```

### Context Management für Long Sessions

```bash
# Periodic context compaction
> /compact focus on current capability system implementation

# Context checkpointing vor major changes
> Update CLAUDE.md with current capability system decisions before refactoring
> Document key implementation insights in @docs/architecture/capability-system.md

# Sprint transition context management
> Save Sprint 4 context to @.claude/sprint-4-context.md
> Load Sprint 5 context from @.claude/commands/sprint/sandbox.md
> Transition focus: capability system → sandbox execution
```

### Performance Monitoring Commands

```markdown
# .claude/commands/performance/benchmark-comprehensive.md
# Comprehensive mlpy Performance Benchmarking

Run full performance analysis of mlpy v2.0 compilation pipeline.

Usage: /performance:benchmark-comprehensive

## Benchmark Categories:
1. **Transpilation Speed**: ML → Python conversion time
2. **Security Analysis**: Time für security validation
3. **Memory Usage**: Peak memory during compilation
4. **Cache Effectiveness**: Hit rate + lookup performance
5. **Sandbox Startup**: Process creation + initialization time

## mlpy-Specific Benchmarks:
- **ML Parsing**: Lark parser performance on various ML programs
- **AST → IR**: Transformation speed + memory efficiency
- **Python Codegen**: AST generation + source map creation
- **Capability Validation**: Runtime capability check performance
- **Sandbox Execution**: Subprocess creation + communication overhead

## Regression Detection:
- Compare against baseline metrics in `benchmarks/baselines/`
- Flag performance regressions >5% in any category
- Generate detailed reports mit flamegraphs
- Suggest optimization opportunities based on profiling
- Create performance regression tests für CI/CD

## Output Format:
- Performance dashboard mit trend analysis
- Specific optimization recommendations
- Resource usage patterns + bottleneck identification
- Comparison mit industry benchmarks (if available)
```

---

## 👥 Team Collaboration & Handoff

### Shared Configuration für Team Consistency

```json
// .claude/settings.json (Version controlled)
{
  "permissions": {
    "allow": [
      "Bash(make test)", "Bash(make lint)", "Bash(make setup-dev)",
      "Bash(nox -s *)", "Bash(python -m mlpy *)",
      "Read(src/**)", "Edit(src/**)", "Write(tests/**)"
    ],
    "deny": [
      "Bash(pip install *)", "Edit(pyproject.toml)", 
      "Write(.github/workflows/**)", "Bash(rm -rf *)"
    ]
  },
  "hooks": {
    "postEdit": {
      "matcher": "*.py",
      "command": "black --check"
    },
    "preEdit": {
      "matcher": "src/mlpy/runtime/capabilities/*",
      "warning": "⚠️ Editing critical security component - extensive testing required"
    }
  },
  "customCommands": [
    "/ml-compiler:transpile-test",
    "/ml-compiler:security-audit", 
    "/sprint:foundation",
    "/sprint:capabilities",
    "/quality:sprint-health-check"
  ]
}
```

### Human-to-Human Handoff Documentation

```markdown
# .claude/handoffs/sprint-4-capability-system.md

## Sprint 4 Context Summary
Working on production-ready capability-based security system für mlpy v2.0.

## Current State
- Core CapabilityToken system implemented in `src/mlpy/runtime/capabilities/manager.py`
- Context hierarchy 60% complete mit parent-child inheritance
- Safe built-ins integration in progress
- Remaining: CallbackBridge implementation, comprehensive security testing

## Claude Code Sessions Used
- Session Focus: `capability-system-implementation`
- Key Agents: security-expert, ml-compiler-expert, performance-engineer
- Commands Used: `/sprint:capabilities`, `/ml-compiler:security-audit`, `/performance:benchmark-comprehensive`

## Implementation Decisions Made
- **Token Design**: UUID-based tokens mit JSON constraints + expiration
- **Context Architecture**: Thread-safe hierarchy mit RLock protection
- **Performance Strategy**: O(1) capability lookups via hashmap caching
- **Security Model**: Whitelist-based access mit capability token validation

## Next Developer Tasks
1. Implement CallbackBridge in `runtime/system_modules/bridge.py`
2. Add comprehensive exploit prevention tests in `tests/security/capability_exploits.py`
3. Performance optimization: capability lookup caching + batch validation
4. Integration testing: parser → security analysis → capability detection pipeline

## Known Issues & Risks
- Current capability check performance: ~0.1ms (target: <0.01ms)
- Thread safety in context switching needs stress testing
- Windows compatibility für subprocess sandbox needs verification
- Memory usage scaling with large capability context hierarchies

## Quality Gates Status
- ✅ Core capability token system functional
- ✅ Context hierarchy implemented + tested
- ⏳ Security exploit prevention tests (in progress)
- ❌ Performance targets not yet met (optimization needed)
- ❌ CallbackBridge implementation pending
```

---

## 🎯 Immediate Setup Actions

### 1. **Projekt-Initialisierung mit Claude Code**

```bash
# 1. Repository setup
git clone https://github.com/your-username/mlpy-v2.git
cd mlpy-v2

# 2. Claude Code Project-Konfiguration
mkdir -p .claude/{commands,agents}
mkdir -p .claude/commands/{sprint,ml-compiler,development,security,quality,performance}

# 3. Copy configuration files
curl -o .claude/settings.json https://raw.githubusercontent.com/your-repo/mlpy-claude-config/main/settings.json
curl -o .mcp.json https://raw.githubusercontent.com/your-repo/mlpy-claude-config/main/mcp.json

# 4. Environment setup
python3.12 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
make setup-dev

# 5. Claude Code verification
claude "Load mlpy v2.0 project context from @CLAUDE.md and verify setup"
```

### 2. **Custom Commands Installation**

```bash
# Download und install alle custom commands
for cmd in foundation parser ir-sourcemaps capabilities sandbox ide-integration production; do
  curl -o .claude/commands/sprint/$cmd.md \
    https://raw.githubusercontent.com/your-repo/mlpy-claude-commands/main/sprint/$cmd.md
done

for cmd in transpile-test security-audit performance-bench debug-pipeline; do
  curl -o .claude/commands/ml-compiler/$cmd.md \
    https://raw.githubusercontent.com/your-repo/mlpy-claude-commands/main/ml-compiler/$cmd.md
done

# Install agents
for agent in security-expert ml-compiler-expert python-transpiler performance-engineer test-engineer; do
  curl -o .claude/agents/$agent.md \
    https://raw.githubusercontent.com/your-repo/mlpy-claude-agents/main/$agent.md
done
```

### 3. **Context Setup + Validation**

```bash
# Initial context loading + project analysis
claude "
Load complete mlpy v2.0 project context:
- Main project overview from @CLAUDE.md
- Sprint roadmap from @docs/sprints/
- Current implementation status from @src/mlpy/

Analyze:
1. Current project state + next priority tasks
2. Architecture decisions that need Claude input
3. Implementation challenges in current sprint
4. Testing gaps that need attention
5. Performance optimization opportunities

Generate action plan für immediate Claude Code usage.
"
```

### 4. **Sprint-Specific Claude Setup**

```bash
# Für Sprint 1 (Foundation)
claude "/sprint:foundation analyze current project setup and implement missing foundation components"

# Für Sprint 2 (Parser)  
claude "/sprint:parser implement complete ML grammar with security analysis integration"

# Für Sprint 4 (Capabilities)
claude "/sprint:capabilities design and implement production-ready capability system"

# Security-focused analysis
claude "/ml-compiler:security-audit comprehensive analyze current security implementation"

# Performance baseline establishment
claude "/performance:benchmark-comprehensive establish baseline performance metrics"
```

---

## 🏆 Success Metrics für Claude Code Integration

### Technical Productivity Metrics
- **Development Speed:** 3-5x faster implementation mit Claude Code assistance
- **Code Quality:** 95%+ test coverage maintained throughout all sprints
- **Security Coverage:** 100% dangerous operation detection + prevention
- **Documentation:** Complete API documentation mit examples für all components

### Claude Code Utilization Metrics
- **Context Efficiency:** <10% token waste durch strategic context loading
- **Command Usage:** Regular usage of custom commands für routine tasks
- **Agent Coordination:** Effective multi-agent workflows für complex decisions
- **Quality Gates:** Automated quality validation mit Claude-generated reports

### Project Success Indicators
- **Sprint Velocity:** Consistent sprint completion within 1-week timeframes
- **Architecture Quality:** Clean, maintainable architecture decisions
- **Security Excellence:** Zero security vulnerabilities in final implementation
- **Performance Targets:** All performance benchmarks met or exceeded

---

## 🎯 Fazit: Claude Code als Development Accelerator

Mit dieser umfassenden Claude Code Konfiguration wird **mlpy v2.0** von einem 12-18 Monat Projekt zu einem **2-4 Monat Projekt**. Die strategische Kombination aus:

- **Project-specific Configuration:** Optimiert für ML compiler development
- **Custom Commands:** Automatisierte Workflows für repetitive Tasks  
- **Strategic Context Management:** Efficient knowledge loading + retention
- **Quality Automation:** Continuous validation + security monitoring
- **Multi-Agent Orchestration:** Specialized expertise für complex decisions

...transformiert Claude Code von einem einfachen Coding Assistant zu einem **sophisticated development platform** für security-first language implementation.

**Immediate Next Steps:**
1. **Setup** der .claude/ configuration files
2. **Install** aller custom commands + agents  
3. **Load** initial project context mit @CLAUDE.md
4. **Start** mit Sprint 1 foundation implementation
5. **Iterate** mit Claude-assisted development workflow

**Ready to accelerate mlpy v2.0 development mit Claude Code! 🚀🔒**