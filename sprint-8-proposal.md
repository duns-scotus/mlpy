# Sprint 8: Production Readiness & Developer Experience

## Sprint Overview

**Duration:** 2-3 weeks
**Focus:** Transform mlpy from a functional compiler into a production-ready development tool with excellent developer experience
**Success Criteria:** Developers can easily create, develop, and deploy ML projects with comprehensive IDE support

## Current State Analysis

### ✅ **Strengths (Sprint 1-7 Foundations)**
- Core transpilation pipeline (94.1% success rate)
- Enterprise-grade security analysis (100% exploit prevention)
- Performance benchmarking infrastructure established
- Basic CLI with compile/check/parse commands
- Rich error formatting system
- Enhanced source maps with debugging support

### ❌ **Gaps for Production Use**
- No project initialization or management workflows
- Limited IDE integration (empty LSP implementation)
- No testing framework for ML code
- Incomplete developer documentation
- No package management or dependency system
- Missing standard project templates and examples

## Sprint 8 Goals & Implementation Plan

### 🎯 **Primary Goal 1: Enhanced CLI & Project Management**

**Objective:** Transform the basic CLI into a comprehensive project management tool

**Current:** `mlpy compile`, `mlpy check`, `mlpy parse`
**Target:** Full project lifecycle support

#### 1.1 New CLI Commands Implementation

```bash
# Project Management
mlpy init <project-name>        # Create new ML project with template
mlpy new <template-name>        # Create from specific template
mlpy build                      # Build entire project with dependencies
mlpy run [file.ml]             # Compile and execute (current + project support)
mlpy test                       # Run project test suite
mlpy dev                        # Development mode with watch/reload

# Enhanced Development Tools
mlpy format                     # Code formatter for ML files
mlpy lint                       # Advanced linting beyond security
mlpy deps                       # Dependency management
mlpy clean                      # Clean build artifacts

# IDE Support
mlpy lsp                        # Start Language Server Protocol server
mlpy docs                       # Generate project documentation
```

#### 1.2 Project Configuration System

**File:** `src/mlpy/cli/project.py`

```python
# mlpy.toml configuration support
[project]
name = "my-ml-project"
version = "0.1.0"
description = "My ML Project"

[build]
entry = "src/main.ml"
output = "dist/"
source_maps = true
optimization_level = 2

[security]
capabilities = ["file:read", "network:http"]
sandbox_enabled = true
threat_detection = "strict"

[dev]
watch_paths = ["src/", "tests/"]
auto_reload = true
```

#### 1.3 Project Templates

**Directory:** `src/mlpy/templates/`

- `basic/` - Simple ML project structure
- `web-app/` - Web application with HTTP capabilities
- `data-analysis/` - Data processing pipeline
- `cli-tool/` - Command-line application
- `library/` - Reusable ML library

**Implementation Files:**
- `src/mlpy/cli/init.py` - Project initialization logic
- `src/mlpy/cli/templates/` - Template definitions
- `src/mlpy/cli/config.py` - Configuration file parsing

### 🎯 **Primary Goal 2: Language Server Protocol (LSP)**

**Objective:** Enable rich IDE integration with VS Code, IntelliJ, Vim, Emacs

#### 2.1 LSP Core Features

**File:** `src/mlpy/lsp/server.py`

```python
# LSP Features Implementation:
class MLPYLanguageServer:
    def text_document_completion(self)      # Autocomplete
    def text_document_hover(self)           # Type info on hover
    def text_document_definition(self)      # Go to definition
    def text_document_references(self)      # Find references
    def text_document_rename(self)          # Symbol renaming
    def text_document_diagnostic(self)      # Real-time errors
    def text_document_formatting(self)      # Code formatting
    def text_document_semantic_tokens(self) # Syntax highlighting
```

#### 2.2 IDE Integration Features

- **Real-time Error Checking:** Security issues, syntax errors, type mismatches
- **Intelligent Completion:** Context-aware suggestions based on available functions, variables
- **Symbol Navigation:** Jump to definitions, find all references
- **Refactoring Support:** Safe rename operations with scope analysis
- **Inline Documentation:** Hover tooltips with type information and docs

#### 2.3 VS Code Extension

**Directory:** `editors/vscode/`

```json
// package.json for VS Code extension
{
  "name": "mlpy-lang-support",
  "displayName": "mlpy Language Support",
  "version": "1.0.0",
  "engines": { "vscode": "^1.74.0" },
  "categories": ["Programming Languages"],
  "contributes": {
    "languages": [{
      "id": "mlpy",
      "aliases": ["mlpy", "ML"],
      "extensions": [".ml"],
      "configuration": "./language-configuration.json"
    }],
    "grammars": [{
      "language": "mlpy",
      "scopeName": "source.mlpy",
      "path": "./syntaxes/mlpy.tmGrammar.json"
    }]
  }
}
```

**Implementation Files:**
- `src/mlpy/lsp/server.py` - Main LSP server
- `src/mlpy/lsp/protocol.py` - LSP protocol handling
- `src/mlpy/lsp/diagnostics.py` - Error reporting integration
- `src/mlpy/lsp/completion.py` - Autocomplete engine
- `editors/vscode/` - VS Code extension

### 🎯 **Primary Goal 3: Testing Framework for ML**

**Objective:** Enable developers to write and run tests for ML code

#### 3.1 ML Testing Syntax

```ml
// tests/math_test.ml
import "assert" as assert;
import "../src/math_utils.ml" as math;

test "addition works correctly" {
    result = math.add(2, 3);
    assert.equal(result, 5);
}

test "division handles zero" {
    assert.throws(() => math.divide(10, 0), "Division by zero");
}

test "factorial computation" {
    assert.equal(math.factorial(5), 120);
    assert.equal(math.factorial(0), 1);
}
```

#### 3.2 Test Runner Integration

**File:** `src/mlpy/testing/runner.py`

```python
class MLTestRunner:
    def discover_tests(self, paths: List[str]) -> List[TestCase]
    def run_tests(self, test_cases: List[TestCase]) -> TestReport
    def generate_coverage_report(self) -> CoverageReport
    def watch_mode(self, paths: List[str]) -> None  # Auto-run on changes
```

**CLI Integration:**
```bash
mlpy test                    # Run all tests
mlpy test --watch           # Continuous testing
mlpy test --coverage        # Generate coverage report
mlpy test tests/math_test.ml # Run specific test file
```

**Implementation Files:**
- `src/mlpy/testing/` - Test framework core
- `src/mlpy/stdlib/assert.py` - Assertion library
- `src/mlpy/testing/coverage.py` - Code coverage tracking

### 🎯 **Primary Goal 4: Comprehensive Three-Tier Documentation System**

**Objective:** Create professional, audience-specific documentation that serves ML programmers, Python integrators, and system developers

#### 4.1 Documentation Architecture

The mlpy documentation follows a three-tier structure targeting distinct audiences with specific needs:

```
docs/
├── user-guide/          # 📘 ML User Guide - For ML Programmers
├── integration-guide/   # 🔗 Integration Guide - For Python Developers
└── developer-guide/     # 🏗️ Developer Guide - For Contributors & Architects
```

#### 4.2 **📘 ML User Guide** - *Complete ML Programming Reference*

**Target Audience:** Developers writing ML code, learning the language, using standard libraries

**Structure:**
```
docs/user-guide/
├── tutorial/
│   ├── 01-getting-started.md           # First ML program in 5 minutes
│   ├── 02-basic-syntax.md              # Variables, functions, control flow
│   ├── 03-data-structures.md           # Arrays, objects, pattern matching
│   ├── 04-functions-closures.md        # Advanced function features
│   ├── 05-security-capabilities.md     # Understanding capability system
│   ├── 06-error-handling.md            # Try/catch, Result types, Option types
│   ├── 07-async-programming.md         # Async/await, Promises
│   ├── 08-testing-debugging.md         # Writing tests, debugging ML code
│   └── 09-project-structure.md         # Organizing larger ML projects
├── language-reference/
│   ├── syntax.md                       # Complete syntax reference
│   ├── types.md                        # Type system, generics, inference
│   ├── operators.md                    # All operators and precedence
│   ├── control-flow.md                 # if/else, loops, match expressions
│   ├── functions.md                    # Function definition, lambda, closures
│   ├── modules.md                      # Import/export, module system
│   ├── pattern-matching.md             # Match expressions, destructuring
│   ├── capabilities.md                 # Security model, capability declarations
│   └── advanced-features.md            # Metaprogramming, macros
└── stdlib-reference/
    ├── core/                           # Built-in functions and types
    │   ├── array.md                    # Array manipulation functions
    │   ├── object.md                   # Object utilities
    │   ├── string.md                   # String processing
    │   ├── math.md                     # Mathematical functions
    │   └── console.md                  # I/O operations
    ├── collections/
    │   ├── list.md                     # List data structure
    │   ├── set.md                      # Set operations
    │   ├── map.md                      # Key-value mappings
    │   └── queue.md                    # Queue implementations
    ├── async/
    │   ├── promise.md                  # Promise API
    │   ├── stream.md                   # Async streams
    │   └── timer.md                    # Time-based operations
    ├── security/
    │   ├── crypto.md                   # Cryptographic functions
    │   ├── auth.md                     # Authentication utilities
    │   └── sandbox.md                  # Sandbox configuration
    └── examples/
        ├── cookbook.md                 # Common patterns and recipes
        ├── real-world-projects.md      # Complete example applications
        └── performance-tips.md         # Optimization guidelines
```

**Content Examples:**

```ml
// From tutorial/03-data-structures.md
// Working with Arrays
numbers = [1, 2, 3, 4, 5];
doubled = map(numbers, x => x * 2);
sum = reduce(numbers, (acc, x) => acc + x, 0);

// Pattern Matching (Advanced)
match response {
    {status: 200, data} => handleSuccess(data);
    {status: 404} => handleNotFound();
    {status, error} when status >= 500 => handleServerError(error);
    _ => handleUnexpectedResponse();
}
```

#### 4.3 **🔗 Integration Guide** - *Embedding ML in Python Projects*

**Target Audience:** Python developers integrating mlpy transpiler, embedding ML code, building tooling

**Structure:**
```
docs/integration-guide/
├── quick-start/
│   ├── installation.md                 # pip install, requirements
│   ├── first-integration.md            # Embed ML in Python in 10 minutes
│   └── configuration.md                # Basic transpiler configuration
├── python-api/
│   ├── transpiler-api.md               # MLTranspiler class reference
│   ├── security-analysis.md            # SecurityAnalyzer integration
│   ├── capability-system.md            # Capability management from Python
│   ├── sandbox-execution.md            # Sandboxed ML execution
│   └── error-handling.md               # Exception handling, error contexts
├── advanced-integration/
│   ├── custom-builtins.md              # Extending ML with Python functions
│   ├── performance-tuning.md           # Optimization for production use
│   ├── caching-strategies.md           # Compilation and execution caching
│   ├── multi-file-projects.md          # Handling complex ML projects
│   └── async-integration.md            # Async ML execution in Python
├── deployment/
│   ├── web-frameworks.md               # Flask, FastAPI, Django integration
│   ├── cloud-deployment.md             # AWS, GCP, Azure deployment patterns
│   ├── containerization.md             # Docker, Kubernetes integration
│   └── monitoring.md                   # Production monitoring and logging
└── examples/
    ├── flask-ml-api.py                 # REST API serving ML code
    ├── jupyter-integration.py          # Jupyter notebook integration
    ├── cli-tool-builder.py             # Building CLI tools with ML
    └── microservice-example/           # Complete microservice project
```

**Python API Examples:**

```python
# From python-api/transpiler-api.md
from mlpy import MLTranspiler, CapabilityContext

# Basic transpilation
transpiler = MLTranspiler()
python_code, issues, source_map = transpiler.transpile_to_python(
    ml_source="x = 42; print(x);",
    generate_source_maps=True
)

# Advanced: Secure execution with capabilities
from mlpy.runtime.capabilities import FileReadToken, NetworkToken

capability_context = CapabilityContext()
capability_context.add_token(FileReadToken("data/*.json"))
capability_context.add_token(NetworkToken("api.example.com"))

result = transpiler.execute_with_sandbox(
    ml_source=ml_code,
    context=capability_context,
    strict_security=True
)
```

#### 4.4 **🏗️ Developer Guide** - *System Architecture & Extension Development*

**Target Audience:** Contributors, standard library developers, security architects, tooling builders

**Structure:**
```
docs/developer-guide/
├── architecture/
│   ├── overview.md                     # System architecture overview
│   ├── compilation-pipeline.md         # Parse → AST → IR → Python flow
│   ├── security-model.md               # Capability system deep-dive
│   ├── performance-design.md           # Performance considerations
│   └── extension-points.md             # Where and how to extend mlpy
├── core-components/
│   ├── parser-grammar.md               # Lark grammar modification
│   ├── ast-nodes.md                    # AST node definitions and visitors
│   ├── security-analysis.md            # Pattern detection, data flow analysis
│   ├── code-generation.md              # Python AST generation
│   ├── capability-system.md            # Token validation, context management
│   └── sandbox-runtime.md              # Process isolation, resource limits
├── stdlib-development/
│   ├── module-guidelines.md            # Standards for new stdlib modules
│   ├── security-requirements.md        # Security review process
│   ├── testing-standards.md            # Testing requirements for stdlib
│   ├── api-design-patterns.md          # Consistent API design
│   └── examples/
│       ├── custom-module-template/     # Template for new modules
│       ├── http-module-example/        # Complete module implementation
│       └── testing-module-example/     # Module with comprehensive tests
├── security-architecture/
│   ├── threat-model.md                 # Security threat analysis
│   ├── capability-design.md            # Capability token system design
│   ├── static-analysis.md              # Security pattern detection
│   ├── runtime-protection.md           # Sandbox and runtime security
│   ├── vulnerability-disclosure.md     # Security issue reporting
│   └── security-review-checklist.md    # Code review security checklist
├── development-process/
│   ├── contributing.md                 # How to contribute to mlpy
│   ├── coding-standards.md             # Python code style, ML code style
│   ├── testing-strategy.md             # Unit, integration, security testing
│   ├── performance-benchmarking.md     # How to measure and improve performance
│   ├── documentation-guidelines.md     # Writing good documentation
│   └── release-process.md              # How releases are managed
└── reference/
    ├── internal-apis.md                # Internal API documentation
    ├── plugin-system.md                # Plugin architecture (future)
    ├── lsp-protocol.md                 # Language Server Protocol implementation
    └── build-system.md                 # Build and deployment internals
```

**Architecture Content Examples:**

```python
# From stdlib-development/module-guidelines.md
"""Standard Library Module Template

Security Requirements:
- All functions must validate inputs using capability tokens
- No direct system access without explicit capability
- All exceptions must inherit from MLError hierarchy

Performance Requirements:
- Functions should complete in <1ms for typical inputs
- Memory usage must be bounded and predictable
- All operations must be thread-safe
"""

from mlpy.runtime.capabilities import requires_capability, NetworkToken
from mlpy.stdlib.base import MLStandardLibraryModule

class HttpModule(MLStandardLibraryModule):
    """HTTP client functionality with capability-based security."""

    @requires_capability(NetworkToken)
    def get(self, url: str, headers: dict = None) -> dict:
        """Perform HTTP GET request.

        Requires: NetworkToken with matching domain
        Returns: {status: int, headers: dict, body: str}
        Raises: NetworkError, SecurityError
        """
        # Implementation with security validation
        pass
```

#### 4.5 Professional Sphinx Documentation System

**Overview:** Sphinx-based documentation with custom ML syntax highlighting, validated examples, and professional themes

**Sphinx Configuration Architecture:**
```
docs/
├── source/
│   ├── conf.py                        # Sphinx configuration
│   ├── index.rst                      # Documentation root
│   ├── user-guide/                    # ML User Guide (RST files)
│   ├── integration-guide/             # Integration Guide (RST files)
│   ├── developer-guide/               # Developer Guide (RST files)
│   └── _static/
│       ├── css/mlpy-theme.css         # Custom styling
│       ├── js/mlpy-interactive.js     # Interactive features
│       └── logo/                      # Brand assets
├── examples/                          # Validated ML code examples
│   ├── user-guide/
│   │   ├── tutorial/
│   │   │   ├── 01-getting-started/
│   │   │   │   ├── hello-world.ml     # Code example files
│   │   │   │   ├── variables.ml
│   │   │   │   └── test_examples.py   # Test validation
│   │   │   ├── 02-basic-syntax/
│   │   │   └── ... (organized by chapter)
│   │   └── stdlib-reference/
│   │       ├── array/
│   │       │   ├── map-example.ml
│   │       │   ├── filter-example.ml
│   │       │   └── test_array_examples.py
│   │       └── ... (organized by module)
│   ├── integration-guide/
│   │   ├── quick-start/
│   │   │   ├── first-integration.py   # Python integration examples
│   │   │   ├── basic-transpile.py
│   │   │   └── test_integration.py
│   │   └── ... (organized by section)
│   └── developer-guide/
│       ├── stdlib-development/
│       │   ├── custom-module-template.py
│       │   └── test_custom_modules.py
│       └── ... (organized by section)
└── _build/                            # Generated documentation
```

**ML Syntax Highlighting System:**

**File:** `src/mlpy/docs/sphinx_extensions/ml_lexer.py`
```python
"""Custom Pygments lexer for ML language syntax highlighting."""

from pygments.lexer import RegexLexer, words
from pygments.token import *

class MLLexer(RegexLexer):
    """Pygments lexer for mlpy ML language."""

    name = 'ML'
    aliases = ['ml', 'mlpy']
    filenames = ['*.ml']
    mimetypes = ['text/x-ml']

    # ML Language keywords
    keywords = [
        'function', 'return', 'if', 'else', 'while', 'for', 'in',
        'try', 'catch', 'finally', 'throw', 'match', 'when',
        'import', 'export', 'as', 'capability', 'async', 'await',
        'let', 'const', 'type', 'interface'
    ]

    builtins = [
        'print', 'len', 'map', 'filter', 'reduce', 'range',
        'parseInt', 'parseFloat', 'toString', 'typeof'
    ]

    operators = [
        r'\+', r'-', r'\*', r'/', r'%', r'==', r'!=', r'<', r'>',
        r'<=', r'>=', r'&&', r'\|\|', r'!', r'=', r'=>', r'\|>'
    ]

    tokens = {
        'root': [
            # Comments
            (r'//.*?$', Comment.Single),
            (r'/\*.*?\*/', Comment.Multiline),

            # Strings
            (r'"([^"\\\\]|\\\\.)*"', String.Double),
            (r"'([^'\\\\]|\\\\.)*'", String.Single),

            # Numbers
            (r'\d+\.\d+([eE][+-]?\d+)?', Number.Float),
            (r'\d+([eE][+-]?\d+)?', Number.Integer),

            # Keywords
            (words(keywords, suffix=r'\b'), Keyword),
            (words(builtins, suffix=r'\b'), Name.Builtin),

            # Capability declarations (security highlighting)
            (r'\b(capability)\s+([a-zA-Z_][a-zA-Z0-9_]*)',
             bygroups(Keyword.Namespace, Name.Class)),

            # Function definitions
            (r'\b(function)\s+([a-zA-Z_][a-zA-Z0-9_]*)',
             bygroups(Keyword, Name.Function)),

            # Operators
            (r'(\+|-|\*|/|%|==|!=|<|>|<=|>=|&&|\|\||!|=|=>|\|>)', Operator),

            # Identifiers
            (r'[a-zA-Z_][a-zA-Z0-9_]*', Name),

            # Punctuation
            (r'[{}()\[\];,.]', Punctuation),

            # Whitespace
            (r'\s+', Text),
        ]
    }
```

**File:** `src/mlpy/docs/sphinx_extensions/ml_domain.py`
```python
"""Sphinx domain for ML language documentation."""

from sphinx import addnodes
from sphinx.domains import Domain, ObjType
from sphinx.directives import ObjectDescription
from sphinx.roles import XRefRole
from sphinx.util.nodes import make_refnode

class MLFunction(ObjectDescription):
    """Directive for documenting ML functions."""

    def add_target_and_index(self, name, sig, signode):
        targetname = f'ml-function-{name}'
        if targetname not in self.state.document.ids:
            signode['ids'].append(targetname)
            self.env.domaindata['ml']['functions'][name] = self.env.docname

class MLDomain(Domain):
    """Sphinx domain for ML language."""

    name = 'ml'
    label = 'ML Language'
    object_types = {
        'function': ObjType('function', 'func'),
        'type': ObjType('type', 'type'),
        'module': ObjType('module', 'mod'),
    }

    directives = {
        'function': MLFunction,
    }

    roles = {
        'func': XRefRole(),
        'type': XRefRole(),
        'mod': XRefRole(),
    }

    initial_data = {
        'functions': {},  # name -> docname
        'types': {},      # name -> docname
        'modules': {},    # name -> docname
    }
```

**Example Integration Directive:**

**File:** `src/mlpy/docs/sphinx_extensions/ml_examples.py`
```python
"""Sphinx extension for validated ML code examples."""

from sphinx.util.docutils import SphinxDirective
from docutils import nodes
from docutils.parsers.rst import directives
import os
import subprocess

class MLExampleDirective(SphinxDirective):
    """Directive for including validated ML code examples."""

    has_content = False
    required_arguments = 1  # example file path
    optional_arguments = 0
    option_spec = {
        'language': directives.unchanged,
        'linenos': directives.flag,
        'caption': directives.unchanged,
        'test': directives.flag,  # Whether to run test validation
    }

    def run(self):
        example_file = self.arguments[0]
        example_path = os.path.join(self.env.srcdir, 'examples', example_file)

        if not os.path.exists(example_path):
            error = self.state_machine.reporter.error(
                f'Example file not found: {example_file}',
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno
            )
            return [error]

        # Read example content
        with open(example_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Validate example if test flag is set
        if 'test' in self.options:
            if not self._validate_example(example_path):
                warning = self.state_machine.reporter.warning(
                    f'Example validation failed: {example_file}',
                    line=self.lineno
                )

        # Create code block
        code_block = nodes.literal_block(content, content)
        code_block['language'] = self.options.get('language', 'ml')
        code_block['linenos'] = 'linenos' in self.options

        if 'caption' in self.options:
            caption_node = nodes.caption('', self.options['caption'])
            container = nodes.container('', caption_node, code_block)
            container['classes'].append('code-example')
            return [container]

        return [code_block]

    def _validate_example(self, example_path):
        """Validate ML example using mlpy transpiler."""
        try:
            result = subprocess.run([
                'python', '-m', 'mlpy.cli', 'check', example_path
            ], capture_output=True, text=True, timeout=30)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
```

**CLI Commands:**
```bash
# Sphinx Documentation Commands
mlpy docs build                        # sphinx-build with ML extensions
mlpy docs serve                        # sphinx-autobuild with live reload
mlpy docs clean                        # Clean build artifacts

# Example Management
mlpy docs test-examples                 # Test all documentation examples
mlpy docs test-examples --user-guide   # Test specific guide examples
mlpy docs extract-examples             # Extract examples from docs to files

# Advanced Features
mlpy docs linkcheck                     # Sphinx linkcheck
mlpy docs coverage                      # Documentation coverage report
mlpy docs pdf                          # Generate PDF documentation
```

**Sphinx Configuration:**

**File:** `docs/source/conf.py`
```python
# Sphinx configuration for mlpy documentation

project = 'mlpy'
copyright = '2024, mlpy Contributors'
author = 'mlpy Contributors'
version = '2.0.0'
release = '2.0.0'

# Extensions
extensions = [
    'sphinx.ext.autodoc',           # Auto-generate API docs
    'sphinx.ext.napoleon',          # Google/NumPy style docstrings
    'sphinx.ext.viewcode',          # Source code links
    'sphinx.ext.intersphinx',       # Cross-project references
    'sphinx.ext.todo',              # TODO items
    'sphinx_copybutton',            # Copy code button
    'sphinx_tabs.tabs',             # Tabbed content
    'myst_parser',                  # Markdown support
    'mlpy.docs.sphinx_extensions.ml_lexer',      # ML syntax highlighting
    'mlpy.docs.sphinx_extensions.ml_domain',     # ML language domain
    'mlpy.docs.sphinx_extensions.ml_examples',   # Validated examples
]

# Theme configuration
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'analytics_id': '',
    'logo_only': True,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': True,
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

# Custom CSS and JavaScript
html_static_path = ['_static']
html_css_files = ['css/mlpy-theme.css']
html_js_files = ['js/mlpy-interactive.js']

# Syntax highlighting
pygments_style = 'default'
pygments_dark_style = 'github-dark'

# ML language registration
def setup(app):
    from mlpy.docs.sphinx_extensions.ml_lexer import MLLexer
    app.add_lexer('ml', MLLexer)
    app.add_lexer('mlpy', MLLexer)
```

**Implementation Architecture:**
```
src/mlpy/docs/
├── sphinx_extensions/
│   ├── ml_lexer.py                    # ML syntax highlighting
│   ├── ml_domain.py                   # ML language Sphinx domain
│   ├── ml_examples.py                 # Validated example directive
│   └── example_runner.py              # Example test runner
├── templates/
│   ├── conf_template.py               # Sphinx configuration template
│   └── rst_templates/                 # RST file templates
├── generators/
│   ├── sphinx_generator.py            # Main Sphinx documentation generator
│   ├── api_generator.py               # Auto-generate API documentation
│   └── example_extractor.py           # Extract examples to separate files
└── themes/
    └── mlpy_theme/                     # Custom Sphinx theme
        ├── theme.conf
        ├── layout.html
        └── static/
            ├── css/
            └── js/
```

**Example Testing Infrastructure:**

**File:** `docs/examples/test_runner.py`
```python
"""Test runner for documentation examples."""

import os
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Any

class DocumentationExampleRunner:
    """Test runner for all documentation examples."""

    def __init__(self, examples_dir: Path):
        self.examples_dir = examples_dir
        self.results: Dict[str, Any] = {}

    def discover_examples(self) -> List[Path]:
        """Discover all .ml example files."""
        return list(self.examples_dir.rglob("*.ml"))

    def run_ml_example(self, example_file: Path) -> Dict[str, Any]:
        """Run a single ML example and return results."""
        try:
            # Transpile check
            result = subprocess.run([
                'python', '-m', 'mlpy.cli', 'check', str(example_file)
            ], capture_output=True, text=True, timeout=30)

            transpile_success = result.returncode == 0

            # Try compilation if check passes
            compile_success = False
            if transpile_success:
                compile_result = subprocess.run([
                    'python', '-m', 'mlpy.cli', 'compile', str(example_file)
                ], capture_output=True, text=True, timeout=30)
                compile_success = compile_result.returncode == 0

            return {
                'file': str(example_file),
                'transpile_success': transpile_success,
                'compile_success': compile_success,
                'error_output': result.stderr if result.stderr else None,
                'duration_ms': 0  # Could measure actual time
            }

        except subprocess.TimeoutExpired:
            return {
                'file': str(example_file),
                'transpile_success': False,
                'compile_success': False,
                'error_output': 'Timeout exceeded',
                'duration_ms': 30000
            }

    def run_all_examples(self) -> Dict[str, Any]:
        """Run all examples and generate report."""
        examples = self.discover_examples()
        results = []

        for example in examples:
            result = self.run_ml_example(example)
            results.append(result)
            print(f"{'✓' if result['transpile_success'] else '✗'} {example.name}")

        # Generate summary
        total = len(results)
        transpile_success = sum(1 for r in results if r['transpile_success'])
        compile_success = sum(1 for r in results if r['compile_success'])

        return {
            'summary': {
                'total_examples': total,
                'transpile_success_count': transpile_success,
                'compile_success_count': compile_success,
                'transpile_success_rate': transpile_success / total if total > 0 else 0,
                'compile_success_rate': compile_success / total if total > 0 else 0,
            },
            'results': results
        }

if __name__ == '__main__':
    runner = DocumentationExampleRunner(Path('docs/examples'))
    report = runner.run_all_examples()

    # Save report
    with open('docs/example-test-report.json', 'w') as f:
        json.dump(report, f, indent=2)

    print(f"\nSummary:")
    print(f"Total examples: {report['summary']['total_examples']}")
    print(f"Transpile success: {report['summary']['transpile_success_rate']:.1%}")
    print(f"Compile success: {report['summary']['compile_success_rate']:.1%}")
```

**Usage Examples in RST Documentation:**

```rst
Tutorial: Working with Arrays
=============================

Arrays are a fundamental data structure in ML. Here's how to work with them:

.. ml-example:: user-guide/tutorial/02-basic-syntax/arrays.ml
   :caption: Basic Array Operations
   :linenos:
   :test:

The :ml:func:`map` function applies a transformation to each element:

.. ml-example:: user-guide/stdlib-reference/array/map-example.ml
   :caption: Using map() to transform arrays
   :test:

You can also use :ml:func:`filter` to select elements:

.. code-block:: ml

   numbers = [1, 2, 3, 4, 5, 6];
   evens = filter(numbers, x => x % 2 == 0);
   print(evens);  // Output: [2, 4, 6]

Cross-references work seamlessly with :ml:type:`Array` types and :ml:mod:`collections`.
```

**CI/CD Integration:**

**File:** `.github/workflows/documentation.yml`
```yaml
name: Documentation Build and Test

on: [push, pull_request]

jobs:
  test-examples:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install -e .[dev,docs]

      - name: Test documentation examples
        run: |
          mlpy docs test-examples

      - name: Build documentation
        run: |
          mlpy docs build

      - name: Check links
        run: |
          mlpy docs linkcheck

      - name: Deploy documentation
        if: github.ref == 'refs/heads/main'
        run: |
          mlpy docs deploy --github-pages

  documentation-coverage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check documentation coverage
        run: |
          mlpy docs coverage --fail-under=90
```

#### 4.6 Content Quality Assurance & Professional Features

**Automated Validation Pipeline:**
- **Example Testing:** All `.ml` files in `docs/examples/` validated with `mlpy check` and `mlpy compile`
- **Link Checking:** Internal cross-references and external links validated
- **API Accuracy:** Generated API docs automatically synced with actual implementation
- **Completeness Tracking:** Coverage reports showing documented vs undocumented APIs
- **Performance Testing:** Documentation examples included in performance regression tests

**Professional Sphinx Features:**
- **ReadTheDocs Theme:** Professional appearance with dark/light mode support
- **Copy-to-Clipboard:** All code examples have copy buttons
- **Tabbed Content:** Multi-language examples (ML + Python integration)
- **Search Integration:** Full-text search across all documentation
- **PDF Generation:** Professional PDF documentation for offline use
- **Mobile Responsive:** Documentation works on all device sizes

**Development Workflow Integration:**
```bash
# Developer workflow with live reload
mlpy docs serve --auto-reload      # Sphinx-autobuild with ML extension support

# Example development and testing
mlpy docs extract-examples         # Extract inline examples to files
mlpy docs test-examples --watch    # Continuous example testing
mlpy docs validate --fix           # Auto-fix common documentation issues

# Quality assurance
mlpy docs coverage --missing        # Show undocumented APIs
mlpy docs linkcheck --broken        # Show broken links
mlpy docs spelling --suggestions    # Spell check with suggestions
```

**Internationalization Support:**
```
docs/
├── source/
│   ├── locale/
│   │   ├── en/                     # English (default)
│   │   ├── es/                     # Spanish
│   │   └── zh/                     # Chinese
│   └── conf.py                     # i18n configuration
```

**Implementation Files:**
- `src/mlpy/docs/sphinx_extensions/` - Custom Sphinx extensions for ML
- `docs/source/` - RST documentation source files
- `docs/examples/` - Validated ML and Python example code
- `docs/source/_static/` - Custom CSS, JavaScript, and assets
- `scripts/validate-docs.py` - Comprehensive documentation validation
- `.github/workflows/documentation.yml` - CI/CD for documentation

### 🎯 **Primary Goal 5: Enhanced Developer Experience**

**Objective:** Improve error messages, debugging, and workflow efficiency

#### 5.1 Enhanced Error Messages

**Current:** Basic error reporting
**Target:** Contextual, helpful error messages with suggestions

```
Error: Undefined variable 'lenght'
  → src/main.ml:5:15
    |
 5  |   array_size = lenght(data);
    |                ^^^^^^
    |
Help: Did you mean 'length'?
Suggestion: Available functions: length, map, filter, reduce

Security Warning: Potential SQL injection detected
  → src/database.ml:12:20
    |
12  |   query = "SELECT * FROM users WHERE id = " + user_id;
    |                                               ^^^^^^^
    |
Help: Use parameterized queries instead:
    | query = "SELECT * FROM users WHERE id = ?";
    | execute(query, [user_id]);
```

#### 5.2 Interactive Development Mode

```bash
mlpy dev                    # Start development mode
# Features:
# - File watching with auto-recompile
# - Real-time error feedback
# - Performance metrics
# - Hot reload for supported scenarios
```

#### 5.3 Debugging Integration

- **Source Map Integration:** Step-through debugging of original ML code
- **Variable Inspection:** Runtime variable values and types
- **Stack Trace Enhancement:** Clear error locations in ML code
- **Performance Profiling:** Identify bottlenecks in ML programs

**Implementation Files:**
- `src/mlpy/cli/dev.py` - Development mode
- `src/mlpy/debugging/debugger.py` - Debugging integration
- `src/mlpy/cli/enhanced_errors.py` - Improved error formatting

## Implementation Strategy

### **Phase 1: Foundation (Week 1)**
1. ✅ Enhanced CLI commands (`init`, `build`, `test`, `dev`)
2. ✅ Project configuration system (`mlpy.toml`)
3. ✅ Basic project templates
4. ✅ Testing framework core

### **Phase 2: IDE Integration (Week 2)**
1. ✅ LSP server implementation
2. ✅ VS Code extension development
3. ✅ Real-time diagnostics integration
4. ✅ Completion engine

### **Phase 3: Polish & Documentation (Week 3)**
1. ✅ Documentation generation system
2. ✅ Enhanced error messages
3. ✅ Interactive examples and tutorials
4. ✅ Development mode features

## Success Metrics

### **Developer Experience Metrics**
- ⭐ **Time to First Project:** < 5 minutes from install to running code
- ⭐ **IDE Integration:** Real-time errors, autocomplete, go-to-definition working
- ⭐ **Error Quality:** Helpful, actionable error messages with suggestions
- ⭐ **Testing Coverage:** >90% of CLI features covered by tests

### **Technical Metrics**
- 📊 **LSP Performance:** <100ms response time for completion requests
- 📊 **Build Performance:** <2s for typical project builds
- 📊 **Memory Usage:** <100MB for LSP server under normal usage
- 📊 **Integration Tests:** 100% success rate maintained

### **Documentation Metrics**
- 📚 **Comprehensive Guide:** Getting started guide covering all basic workflows
- 📚 **API Coverage:** 100% of public APIs documented with examples
- 📚 **Tutorial Quality:** 5+ working tutorial projects demonstrating key features

## Risk Assessment & Mitigation

### **High Risk: LSP Complexity**
- **Risk:** LSP implementation is complex and time-consuming
- **Mitigation:** Start with basic features (diagnostics, completion), expand iteratively
- **Fallback:** Focus on CLI improvements if LSP blocks progress

### **Medium Risk: VS Code Extension**
- **Risk:** Extension development and publishing process
- **Mitigation:** Use established TypeScript LSP client libraries
- **Fallback:** Provide generic LSP server that works with any editor

### **Low Risk: Documentation Scope**
- **Risk:** Documentation generation might be too ambitious
- **Mitigation:** Manual documentation for Sprint 8, auto-generation in future sprints

## Dependencies & Prerequisites

### **Required:**
- Current Sprint 7 state (94.1% integration test success)
- Existing CLI infrastructure (Rich, Click)
- Core transpilation pipeline

### **Optional:**
- VS Code development environment for extension testing
- Additional editor support (IntelliJ, Vim) can be deferred

## Deliverables

### **Core Components**
1. ✅ Enhanced CLI with project management (`src/mlpy/cli/`)
2. ✅ Language Server Protocol implementation (`src/mlpy/lsp/`)
3. ✅ Testing framework for ML (`src/mlpy/testing/`)
4. ✅ VS Code extension (`editors/vscode/`)
5. ✅ Project templates (`src/mlpy/templates/`)
6. ✅ Documentation system (`src/mlpy/docs/`, `docs/`)

### **User-Facing**
1. 🚀 `mlpy init` creates fully functional projects in <30 seconds
2. 🚀 VS Code provides real-time ML syntax checking and autocomplete
3. 🚀 `mlpy test` runs ML unit tests with clear reporting
4. 🚀 `mlpy docs` generates beautiful, navigable documentation
5. 🚀 Enhanced error messages guide users to solutions

### **Quality Assurance**
1. ✅ Integration tests for all new CLI commands
2. ✅ LSP protocol compliance testing
3. ✅ VS Code extension functionality verification
4. ✅ Documentation accuracy and completeness review
5. ✅ Performance regression testing for new features

## Sprint 8 Success Definition

> **"A new developer can install mlpy, create their first project, write working ML code with IDE support, run tests, and deploy to production within 30 minutes using only the official documentation."**

This Sprint 8 transforms mlpy from a functional compiler into a production-ready development platform that rivals modern language toolchains in terms of developer experience and productivity.

## Next Steps (Sprint 9 Preview)

After Sprint 8 completion:
- **Advanced Feature Implementation:** Pattern matching, generics, async/await from Sprint 7 designs
- **Package Management:** Dependency resolution and module system
- **Performance Optimizations:** Based on Sprint 7 benchmarking data
- **Production Deployment:** Docker containers, CI/CD integrations, cloud deployments