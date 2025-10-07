# ML Language Documentation Rewrite Proposal

**Status:** Draft (Updated with REPL-First Approach)
**Created:** 2025-10-06
**Updated:** 2025-10-07 (Added REPL integration)
**Author:** Documentation Team
**Version:** 2.0 - REPL-First Edition

## Version 2.0 Updates

**Major Changes:**
- ✨ **REPL-First Learning Approach** - Start users in the REPL immediately
- ✨ **Complete REPL Guide** - Comprehensive documentation of mlpy REPL v2.3 features
- ✨ **REPL-Integrated Tutorial** - Every concept demonstrated in REPL sessions first
- ✨ **Getting Started Rewrite** - REPL-centric onboarding (productive in 5 minutes)
- ✨ **REPL Transcripts** - 50+ interactive REPL sessions showing real development
- ✨ **Progressive Learning** - REPL experimentation → File-based development

**Rationale:**
The mlpy REPL v2.3 is enterprise-grade (6.93ms execution, capability management, error recovery, editor integration). This powerful tool should be the PRIMARY learning and experimentation interface, not a secondary feature.

## Executive Summary

This proposal outlines a comprehensive rewrite of the ML language documentation to reflect the significant evolution of mlpy v2.0. The current documentation structure is outdated and doesn't accurately represent the implemented features, new decorator-based module system, evolved architecture, and comprehensive standard library.

**Note:** mlpy already has complete Sphinx infrastructure with ML syntax highlighting (`ml_lexer.py`), so we can focus entirely on content creation and executable snippet development.

**Key Objectives:**

1. **Complete Language Reference Rewrite** - Accurately document all implemented ML language features based on current grammar and integration tests
2. **Standard Library Documentation** - Comprehensive documentation of all 11 stdlib modules with decorator syntax
3. **Three-Tier Documentation Structure** - Streamlined organization for different user personas
4. **Updated Integration Patterns** - Document new decorator-based module development workflow
5. **Architecture Documentation** - Reflect current pipeline, security, and runtime systems

**Scope:** Complete rewrite of ~80% of documentation content with new structure and organization.

---

## Documentation Principles

To ensure documentation quality, maintainability, and accuracy, we establish the following core principles:

### Principle 1: Executable ML Code Snippets

**Rule:** All ML code snippets in documentation MUST be stored in the `docs/ml_snippets/` directory structure, not inlined in `.rst` files.

**Requirements:**
- Every ML code example must be a complete, executable `.ml` file
- Snippets must successfully parse, transpile, and execute
- RST files reference snippets using Sphinx `.. literalinclude::` directive
- Organize snippets by topic matching documentation structure

**Directory Structure:**
```
docs/ml_snippets/
├── language-reference/
│   ├── control-flow/
│   │   ├── if_elif_else.ml
│   │   ├── while_loop.ml
│   │   └── for_loop.ml
│   ├── functions/
│   │   ├── named_function.ml
│   │   ├── arrow_function.ml
│   │   └── closures.ml
│   └── exceptions/
│       └── try_except_finally.ml
├── stdlib/
│   ├── builtin/
│   │   ├── typeof_usage.ml
│   │   └── type_conversions.ml
│   ├── console/
│   │   └── console_log.ml
│   └── [other stdlib modules]/
└── integration/
    ├── python_interop.ml
    └── module_import.ml
```

**Example RST Usage:**
```rst
Basic if/elif/else example:

.. literalinclude:: ../../ml_snippets/language-reference/control-flow/if_elif_else.ml
   :language: ml
   :lines: 1-10
```

**Syntax Highlighting:**
- ML syntax highlighting is **already implemented** in `docs/source/ml_lexer.py`
- Registered with Sphinx in `docs/source/conf.py`
- Supports all ML language features: keywords, operators, types, pattern matching, capabilities
- Use `:language: ml` directive for automatic syntax highlighting

### Principle 2: Executable Python Code Snippets

**Rule:** All Python code snippets in documentation MUST be stored in the `docs/py_snippets/` directory structure, not inlined in `.rst` files.

**Requirements:**
- Every Python example must be a complete, executable `.py` file
- Snippets must run without errors using Python 3.12+
- Include necessary imports and setup code
- RST files reference snippets using Sphinx `.. literalinclude::` directive

**Directory Structure:**
```
docs/py_snippets/
├── integration/
│   ├── basic_transpilation.py
│   ├── capability_context.py
│   └── sandbox_execution.py
├── stdlib-development/
│   ├── simple_module.py
│   ├── crypto_module_complete.py
│   └── capability_enforcement.py
├── bridge-system/
│   ├── type_bridge.py
│   └── custom_bridge.py
└── testing/
    ├── unit_test_example.py
    └── integration_test.py
```

**Example RST Usage:**
```rst
Creating a custom stdlib module with decorators:

.. literalinclude:: ../../py_snippets/stdlib-development/simple_module.py
   :language: python
   :lines: 1-30
```

### Principle 3: REPL Transcript Snippets

**Rule:** All REPL interaction examples in documentation MUST be stored in the `docs/repl_snippets/` directory structure as doctest-style transcript files.

**Requirements:**
- Every REPL example must be a complete, executable transcript file
- Transcripts must use doctest-style format with `ml[secure]>` prompt
- Files must have `.transcript` extension
- Transcripts must successfully execute via REPL doctest runner
- RST files reference transcripts using Sphinx `.. literalinclude::` directive
- Organize snippets by topic matching documentation structure

**Directory Structure:**
```
docs/repl_snippets/
├── getting-started/
│   ├── first_steps.transcript
│   └── basic_math.transcript
├── tutorial/
│   ├── variables_and_types.transcript
│   ├── control_flow.transcript
│   └── functions.transcript
├── capabilities/
│   ├── granting_capabilities.transcript
│   └── capability_errors.transcript
└── debugging/
    ├── using_vars.transcript
    └── retry_command.transcript
```

**Doctest-Style Format:**
```transcript
# first_steps.transcript - Getting started with ML REPL

ml[secure]> x = 10;
✓ x = 10

ml[secure]> y = 20;
✓ y = 20

ml[secure]> result = x + y;
✓ result = 30

ml[secure]> print(result);
30
✓

ml[secure]> .vars
Variables:
  x = 10
  y = 20
  result = 30
```

**REPL Doctest Runner:** `tests/repl_doctest_runner.py`

**Functionality:**
- Discover all `.transcript` files in `docs/repl_snippets/` directory
- Parse doctest-style format with expected prompts and outputs
- Execute each command through actual REPL instance
- Verify outputs match expected results
- Support REPL commands (`.vars`, `.history`, `.clear`, etc.)
- Generate test report with pass/fail status
- Integrate into CI/CD pipeline

**Runner Usage:**
```bash
# Run all REPL doctests
python tests/repl_doctest_runner.py

# Run specific category
python tests/repl_doctest_runner.py --category tutorial

# Verbose output
python tests/repl_doctest_runner.py --verbose

# Generate HTML report
python tests/repl_doctest_runner.py --html-report repl-tests.html
```

**Runner Implementation Features:**
- Start fresh REPL instance for each transcript
- Parse transcript files for commands and expected outputs
- Execute commands and capture actual outputs
- Compare actual vs expected with diff reporting
- Handle REPL special commands (`.vars`, `.grant`, etc.)
- Support comment lines (lines starting with `#`)
- Timeout protection for long-running commands
- Colored output for pass/fail status

**Example RST Usage:**
```rst
Let's explore basic arithmetic in the REPL:

.. literalinclude:: ../../repl_snippets/getting-started/basic_math.transcript
   :language: text
   :lines: 3-15
```

**Benefits:**
- **Interactive Examples:** Show real REPL sessions
- **Verified Accuracy:** All REPL examples tested automatically
- **User Experience:** Readers see exactly what they'll type and see
- **Regression Testing:** REPL behavior changes caught immediately
- **Teaching Tool:** Progressive learning through interactive sessions

---

### Principle 4: Language Understanding Before Writing

**Rule:** Before writing any ML code snippets, documentation authors MUST read and understand the ML language grammar and existing test examples.

**Requirements:**
- **Read the grammar first:** Study `src/mlpy/ml/grammar/ml.lark` to understand ML language syntax
- **Study integration tests:** Review `tests/ml_integration/` test files to see real working ML code
- **Understand builtin functionality:** Read `src/mlpy/stdlib/builtin.py` to know what's available
- **Use builtins appropriately:** Prefer builtin functions over reimplementing functionality
- **Follow ML idioms:** Write code that matches patterns seen in integration tests
- **Verify syntax correctness:** Ensure snippets use correct ML syntax from grammar

**Why This Matters:**
- ML syntax differs from JavaScript/Python in subtle ways
- Grammar is the source of truth for what's valid ML code
- Integration tests demonstrate idiomatic ML code patterns
- Using builtins makes examples simpler and more correct
- Prevents documentation from showing invalid or non-idiomatic code

**Example Workflow:**
1. Read `src/mlpy/ml/grammar/ml.lark` to understand control flow syntax
2. Review `tests/ml_integration/ml_core/08_control_structures.ml` for examples
3. Check `src/mlpy/stdlib/builtin.py` for available builtin functions
4. Write snippet using correct syntax and appropriate builtins
5. Test snippet with mlpy to verify it executes

**Anti-Pattern to Avoid:**
```ml
// BAD: Guessing syntax without checking grammar
function example() {
    catch (e) {  // ❌ Wrong! ML uses "except", not "catch"
        print e;
    }
}
```

**Correct Pattern:**
```ml
// GOOD: Verified against grammar and test examples
function example() {
    try {
        risky_operation();
    } except (e) {  // ✓ Correct ML syntax
        print(e.message);
    }
}
```

---

### Principle 5: Automated Verification with Testing Tools

**Rule:** Automated testing tools verify all code snippets and REPL transcripts in documentation.

**Three Verification Tools:**

#### Tool 1: ML Code Snippet Validator - `tests/ml_snippet_validator.py`

**Purpose:** Validate all ML code snippets in `docs/ml_snippets/`

**Functionality:**
- Discover all `.ml` files in `ml_snippets/` directory
- Run each snippet through complete pipeline:
  1. Parse (verify syntax)
  2. Security analysis (detect issues)
  3. Transpile to Python (code generation)
  4. Execute in sandbox (runtime verification)
- Track success/failure for each stage
- Generate detailed validation report
- Integrate into CI/CD pipeline

**Usage:**
```bash
# Validate all ML snippets
python tests/ml_snippet_validator.py

# Validate specific category
python tests/ml_snippet_validator.py --category language-reference

# Verbose output with pipeline details
python tests/ml_snippet_validator.py --verbose

# Generate HTML report
python tests/ml_snippet_validator.py --html-report ml-validation.html

# Fail fast on first error
python tests/ml_snippet_validator.py --fail-fast
```

**Validation Stages:**
```
ML Snippet: docs/ml_snippets/tutorial/functions.ml
├─ ✅ Parse      (15.2ms) - Syntax valid
├─ ✅ Security   (8.4ms)  - No threats detected
├─ ✅ Transpile  (42.1ms) - Python code generated
└─ ✅ Execute    (125ms)  - Output: "Hello, World!"

Result: PASS (4/4 stages)
```

**Output Report:**
```
╭─────────────────────────────────────────────╮
│ ML Snippet Validation Report                │
│ Generated: 2025-10-07 15:45:33             │
╰─────────────────────────────────────────────╯

Summary:
  Total snippets: 127
  Passed: 125 (98.4%)
  Failed: 2 (1.6%)

Failed Snippets:
  ❌ ml_snippets/advanced/async_await.ml
     Stage: Execute
     Error: Async/await not yet implemented

  ❌ ml_snippets/stdlib/http_advanced.ml
     Stage: Execute
     Error: Network access requires capability

Recommendations:
  - Mark async_await.ml as "Future Feature"
  - Add capability grant to http_advanced.ml
```

#### Tool 2: REPL Doctest Runner - `tests/repl_doctest_runner.py`

**Purpose:** Execute and verify REPL transcript files in `docs/repl_snippets/`

**Functionality:**
- Discover all `.transcript` files in `repl_snippets/` directory
- Parse doctest-style format (prompts, commands, expected outputs)
- Start fresh REPL instance for each transcript
- Execute commands and capture outputs
- Compare actual vs expected outputs with diff
- Handle REPL special commands (`.vars`, `.grant`, `.capabilities`, etc.)
- Generate test report with pass/fail status
- Support transcript sections and comments
- Timeout protection for commands

**Usage:**
```bash
# Run all REPL doctests
python tests/repl_doctest_runner.py

# Run specific category
python tests/repl_doctest_runner.py --category tutorial

# Verbose output with full transcripts
python tests/repl_doctest_runner.py --verbose

# Generate HTML report
python tests/repl_doctest_runner.py --html-report repl-tests.html

# Show diffs for failures
python tests/repl_doctest_runner.py --show-diffs
```

**Transcript Execution:**
```
Transcript: docs/repl_snippets/tutorial/variables.transcript
├─ Line 3:  ml[secure]> x = 10;
│  Expected: ✓ x = 10
│  Actual:   ✓ x = 10
│  Status:   ✅ MATCH
│
├─ Line 6:  ml[secure]> print(x);
│  Expected: 10
│  Actual:   10
│  Status:   ✅ MATCH
│
└─ Line 10: ml[secure]> .vars
   Expected: Variables:\n  x = 10
   Actual:   Variables:\n  x = 10
   Status:   ✅ MATCH

Result: PASS (3/3 commands)
```

**Output Report:**
```
╭─────────────────────────────────────────────╮
│ REPL Doctest Report                         │
│ Generated: 2025-10-07 15:45:41             │
╰─────────────────────────────────────────────╯

Summary:
  Total transcripts: 45
  Passed: 43 (95.6%)
  Failed: 2 (4.4%)
  Total commands: 312
  Commands passed: 306 (98.1%)

Failed Transcripts:
  ❌ repl_snippets/capabilities/grant_error.transcript
     Line: 15
     Command: .grant file.read
     Expected: ✓ Granted capability: file.read
     Actual:   ❌ Error: Capability grants not yet implemented

  ❌ repl_snippets/debugging/watch.transcript
     Line: 8
     Command: .watch x
     Expected: Watching: x
     Actual:   ❌ Unknown command: .watch
```

#### Tool 3: Python Code Snippet Validator - `tests/py_snippet_validator.py`

**Purpose:** Validate all Python code snippets in `docs/py_snippets/`

**Functionality:**
- Discover all `.py` files in `py_snippets/` directory
- Execute each Python file in isolated environment
- Verify execution completes without errors
- Capture and validate output when expected
- Check for proper imports and dependencies
- Generate validation report
- Integrate into CI/CD pipeline

**Usage:**
```bash
# Validate all Python snippets
python tests/py_snippet_validator.py

# Validate specific category
python tests/py_snippet_validator.py --category integration

# Verbose output
python tests/py_snippet_validator.py --verbose

# Check syntax only (no execution)
python tests/py_snippet_validator.py --syntax-only
```

### Unified Verification Command

**Script:** `tests/verify_all_docs.py`

**Purpose:** Run all three validation tools together

**Usage:**
```bash
# Validate everything
python tests/verify_all_docs.py

# Generate combined HTML report
python tests/verify_all_docs.py --html-report docs-validation.html

# CI/CD mode (exit code 1 if any failures)
python tests/verify_all_docs.py --ci
```

**Combined Report:**
```
╭─────────────────────────────────────────────╮
│ Documentation Validation Report             │
│ All Snippets and Transcripts               │
╰─────────────────────────────────────────────╯

ML Code Snippets:     125/127 (98.4%) ✅
REPL Transcripts:      43/45  (95.6%) ✅
Python Snippets:       38/38  (100%)  ✅

Overall Success Rate: 206/210 (98.1%) ✅

Status: PASS (meets 95% threshold)
```

**Benefits:**
- **Accuracy:** All examples guaranteed to work with current implementation
- **Maintainability:** Code changes that break examples trigger CI failures
- **Developer Confidence:** Documentation always reflects actual behavior
- **User Trust:** Examples are reliable and copy-pasteable
- **Regression Prevention:** Documentation tests catch breaking changes
- **Quality Assurance:** 95%+ success rate required for documentation release

**CI/CD Integration:**
```yaml
# .github/workflows/docs-validation.yml
name: Validate Documentation

on: [push, pull_request]

jobs:
  validate-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: pip install -e .
      - name: Validate ML snippets
        run: python tests/ml_snippet_validator.py --ci
      - name: Validate REPL transcripts
        run: python tests/repl_doctest_runner.py --ci
      - name: Validate Python snippets
        run: python tests/py_snippet_validator.py --ci
      - name: Generate combined report
        run: python tests/verify_all_docs.py --html-report validation.html
      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: validation-report
          path: validation.html
```

---

## Existing Infrastructure

### Sphinx Documentation System

mlpy already has a complete Sphinx documentation infrastructure in place:

**Configuration:** `docs/source/conf.py`
- Sphinx version: Latest
- Theme: `sphinx_rtd_theme` (Read the Docs)
- Extensions: autodoc, viewcode, napoleon, intersphinx, todo, coverage, githubpages, myst_parser
- Custom CSS: `docs/source/_static/custom.css`

**ML Syntax Highlighting:** `docs/source/ml_lexer.py`
- **Full Pygments lexer** for ML language (195 lines)
- **Comprehensive token support:**
  - Keywords: if, elif, else, while, for, function, async, try, except, finally, import, etc.
  - Operators: arithmetic, comparison, logical, bitwise, pipeline (`|>`), arrow (`=>`)
  - Built-in types: number, string, boolean, Array, Object, Promise, Result, Option
  - Built-in functions: print, typeof, int, float, str, etc.
  - Standard library modules: console, math, datetime, regex, functional
  - Pattern matching: match, when
  - Capability system: capability, secure, sandbox
  - Comments: single-line (`//`) and multi-line (`/* */`)
  - Strings: double, single, backtick, template literals
  - Numbers: integer, float, hex, binary, octal, scientific notation

**Registration:**
```python
# In docs/source/conf.py
from ml_lexer import MLLexer
from sphinx.highlighting import lexers
lexers['ml'] = MLLexer()
highlight_language = 'ml'  # Default highlighting language
```

**Usage in RST Files:**
```rst
.. code-block:: ml

   function fibonacci(n) {
       if (n <= 1) {
           return n;
       }
       return fibonacci(n - 1) + fibonacci(n - 2);
   }

.. literalinclude:: ../../ml_snippets/examples/fibonacci.ml
   :language: ml
   :lines: 1-10
   :linenos:
```

**Theme Customization:**
- Responsive design with mobile support
- Collapsible navigation
- Search functionality
- Syntax highlighting with line numbers
- Copy-to-clipboard for code blocks

### What This Means for the Rewrite

✅ **Already Have:**
- Complete Sphinx setup and configuration
- Professional ML syntax highlighting
- Read the Docs theme with customizations
- Build infrastructure

⚠️ **Need to Add:**
- `docs/ml_snippets/` directory structure
- `docs/py_snippets/` directory structure
- `docs/verify_snippets.py` verification tool
- Actual snippet files and updated RST documentation

**Advantage:** We can focus entirely on content creation and snippet development, not infrastructure setup.

---

## Current State Analysis

### Existing Documentation Structure

```
docs/source/
├── user-guide/
│   ├── tutorial.rst              # 721 lines - OBSOLETE: Delete and rewrite (language/builtin incompatibilities)
│   ├── language-reference.rst    # Partially outdated, grammar mismatch
│   ├── standard-library.rst      # Missing: file, path, http modules
│   └── cli-reference.rst         # Good, needs minor updates
├── integration-guide/
│   ├── python-integration.rst    # 1294 lines - Good foundation, needs API updates
│   ├── ide-integration.rst       # Good, needs VS Code extension coverage
│   └── api-reference.rst         # Incomplete, needs expansion
├── developer-guide/
│   ├── architecture.rst          # Outdated - pipeline evolved significantly
│   ├── writing-stdlib-modules.rst # OUTDATED - still shows old pattern, not decorators
│   ├── bridge-system-guide.rst   # Good foundation, needs updates
│   └── security-model.rst        # Needs expansion with latest patterns
└── standard-library/
    ├── builtin-functions.rst     # Missing: typeof, int(), float(), str()
    ├── array.rst, string.rst     # Reference old ad-hoc functions
    ├── collections.rst through regex.rst # Good structure, need updates
    └── [MISSING] file.rst, path.rst, http.rst
```

### Critical Gaps Identified

1. **Tutorial:**
   - **COMPLETE REWRITE REQUIRED:** Existing tutorial has language syntax incompatibilities (uses outdated syntax)
   - **Builtin incompatibilities:** Tutorial uses functions/patterns that no longer match current builtin implementation
   - **Must delete and rewrite from scratch:** Cannot salvage existing content
   - **New tutorial must:** Follow current grammar, use current builtins, demonstrate idiomatic ML code

2. **Language Reference:**
   - Grammar features not documented: elif, nonlocal, arrow functions (fn), destructuring
   - Control flow section incomplete
   - Exception handling syntax outdated (catch vs except)
   - Missing: slice expressions, ternary operators

3. **Standard Library:**
   - **Missing Modules:** file, path, http (newly implemented)
   - **Outdated Modules:** array, string (show ad-hoc functions instead of removed primitives)
   - **Incomplete Builtin Documentation:** Missing typeof(), int(), float(), str()
   - No capability requirements documented for I/O operations

3. **Integration Guide:**
   - Module development shows OLD pattern (manual classes)
   - Decorator syntax (@ml_module, @ml_function, @ml_class) not documented
   - Capability enforcement patterns not shown
   - AllowedFunctionsRegistry not covered

4. **Developer Guide:**
   - Architecture diagrams show old 4-stage pipeline (now 10 stages)
   - Security analysis missing: parallel_analyzer, pattern_detector updates
   - Code generation doesn't cover enhanced assignment support
   - Test runner not documented

---

## Proposed Documentation Structure

### Three-Tier Organization

```
docs/source/
│
├── index.rst                          # Main landing page with quick navigation
│
├── user-guide/                        # TIER 1: ML Language Users
│   ├── index.rst                      # User guide overview
│   ├── getting-started.rst            # NEW: Installation, first program, REPL basics
│   ├── repl-guide.rst                 # NEW: Complete REPL reference (commands, features, v2.3)
│   ├── tutorial.rst                   # COMPLETE REWRITE: REPL-first tutorial from scratch
│   ├── language-reference/            # NEW: Comprehensive reference
│   │   ├── index.rst                  # Language reference overview
│   │   ├── lexical-structure.rst      # NEW: Comments, identifiers, keywords, literals
│   │   ├── data-types.rst             # NEW: Numbers, strings, booleans, arrays, objects
│   │   ├── expressions.rst            # NEW: Operators, precedence, ternary, calls
│   │   ├── statements.rst             # NEW: Assignments, control flow, loops
│   │   ├── functions.rst              # NEW: Function definitions, arrow functions, closures
│   │   ├── control-flow.rst           # NEW: if/elif/else, while, for, break, continue
│   │   ├── exception-handling.rst     # NEW: try/except/finally, throw
│   │   ├── destructuring.rst          # NEW: Array and object destructuring
│   │   ├── advanced-features.rst      # NEW: Slicing, nonlocal, decorators
│   │   └── capability-system.rst      # NEW: Capability declarations, patterns
│   ├── standard-library/              # Comprehensive stdlib reference
│   │   ├── index.rst                  # Stdlib overview with quick reference table
│   │   ├── builtin-functions.rst      # REWRITE: typeof, int, float, str, len, range, print
│   │   ├── console.rst                # UPDATE: Add capability requirements
│   │   ├── math.rst                   # UPDATE: Complete method listing
│   │   ├── string.rst                 # REWRITE: Remove ad-hoc functions, document properly
│   │   ├── array.rst                  # REWRITE: Remove ad-hoc functions, document properly
│   │   ├── datetime.rst               # UPDATE: Add timestamp(), add_days()
│   │   ├── json.rst                   # Good, minor updates
│   │   ├── collections.rst            # Good, minor updates
│   │   ├── functional.rst             # UPDATE: Add curry2, partition, ifElse, cond, etc.
│   │   ├── regex.rst                  # UPDATE: Add extract_emails, is_url, etc.
│   │   ├── random.rst                 # Good, minor updates
│   │   ├── file.rst                   # NEW: Complete file I/O module
│   │   ├── path.rst                   # NEW: Path manipulation module
│   │   └── http.rst                   # NEW: HTTP client module
│   ├── cli-reference.rst              # UPDATE: Add lsp command, new features
│   ├── ide-integration.rst            # UPDATE: Add VS Code extension
│   ├── security-guide.rst             # NEW: User-facing security concepts
│   └── faq.rst                        # NEW: Common questions and answers
│
├── integration-guide/                 # TIER 2: Python Developers Integrating ML
│   ├── index.rst                      # Integration guide overview
│   ├── quick-start.rst                # NEW: 5-minute integration tutorial
│   ├── python-integration.rst         # UPDATE: API changes, new patterns
│   ├── transpilation-api.rst          # NEW: Transpiler API reference
│   ├── sandbox-execution.rst          # NEW: Safe execution patterns
│   ├── capability-management.rst      # NEW: Managing capabilities from Python
│   ├── writing-stdlib-modules.rst     # REWRITE: Decorator-based module development
│   ├── bridge-system.rst              # UPDATE: Latest bridge patterns
│   ├── security-integration.rst       # NEW: Security analysis from Python
│   ├── ide-tooling.rst                # NEW: LSP server, VS Code extension integration
│   ├── testing-ml-code.rst            # NEW: Testing strategies for ML code
│   ├── deployment.rst                 # NEW: Deploying ML-powered applications
│   └── api-reference.rst              # UPDATE: Complete API documentation
│
└── developer-guide/                   # TIER 3: mlpy Core Developers
    ├── index.rst                      # Developer guide overview
    ├── architecture/                  # NEW: Comprehensive architecture docs
    │   ├── index.rst                  # Architecture overview
    │   ├── compilation-pipeline.rst   # REWRITE: 10-stage pipeline
    │   ├── grammar-parser.rst         # NEW: Lark grammar, AST generation
    │   ├── ast-transformation.rst     # NEW: AST validation and transformation
    │   ├── type-system.rst            # NEW: Type checking and inference
    │   ├── security-analysis.rst      # REWRITE: Parallel analyzer, pattern detection
    │   ├── optimization.rst           # NEW: Optimization passes
    │   ├── code-generation.rst        # REWRITE: Python AST generation, enhanced assignments
    │   ├── source-maps.rst            # NEW: Source map generation
    │   └── runtime-systems.rst        # UPDATE: Capabilities, sandbox, whitelist
    ├── extending-mlpy/                # NEW: How to extend the compiler
    │   ├── index.rst                  # Extension guide overview
    │   ├── adding-language-features.rst # NEW: Grammar extensions, AST nodes
    │   ├── writing-stdlib-modules.rst # REWRITE: Complete decorator guide with crypto example
    │   ├── custom-security-rules.rst  # NEW: Extending security analysis
    │   ├── optimization-passes.rst    # NEW: Adding custom optimizations
    │   └── code-generator-extensions.rst # NEW: Extending code generation
    ├── testing/                       # NEW: Comprehensive testing infrastructure
    │   ├── index.rst                  # Testing overview
    │   ├── ml-test-runner.rst         # NEW: Unified ML pipeline test runner (COMPREHENSIVE)
    │   ├── repl-test-runner.rst       # NEW: REPL integration test runner (COMPREHENSIVE)
    │   ├── unit-testing.rst           # NEW: Unit test patterns
    │   ├── integration-testing.rst    # NEW: ML integration test suite
    │   └── security-testing.rst       # NEW: Security audit tests
    ├── development-workflow/          # NEW: Contributing and development
    │   ├── index.rst                  # Workflow overview
    │   ├── setup.rst                  # NEW: Development environment setup
    │   ├── coding-standards.rst       # UPDATE: Black, Ruff, MyPy standards
    │   ├── git-workflow.rst           # NEW: Branch strategy, commits, PRs
    │   └── release-process.rst        # NEW: Versioning, changelog, releases
    └── api-reference/                 # NEW: Internal API docs
        ├── index.rst                  # API overview
        ├── transpiler-api.rst         # Auto-generated from docstrings
        ├── runtime-api.rst            # Auto-generated from docstrings
        ├── stdlib-api.rst             # Auto-generated from docstrings
        └── utilities-api.rst          # Auto-generated from docstrings
```

---

## Detailed Content Outlines

### TIER 1: ML User Guide

#### 1.1 Getting Started (NEW - REPL-FIRST APPROACH)

**Purpose:** Zero to productive development in 5 minutes using REPL
**Length:** ~500 lines

**Philosophy:** Start with REPL for immediate experimentation, THEN introduce file-based development

**Content Structure:**

**Section 1: Installation (50 lines)**
```bash
pip install mlpy
mlpy --version
```

**Section 2: Your First ML Code - Using the REPL (200 lines)**
- **Start REPL immediately:** `mlpy repl`
- **Interactive prompt:** Understanding `ml[secure]>`
- **First expression:** `2 + 2`
- **First variable:** `name = "Alice"`
- **First function:** Define and call functions interactively
- **Why REPL first:** Immediate feedback, experimentation, learning

```ml
$ mlpy repl
Welcome to mlpy REPL v2.3!
Type .help for available commands.
ml[secure]> 2 + 2
=> 4

ml[secure]> name = "Alice";
ml[secure]> print("Hello, " + name);
Hello, Alice

ml[secure]> function greet(person) {
...   return "Hello, " + person + "!";
... }
ml[secure]> greet(name);
=> "Hello, Alice!"

ml[secure]> greet("Bob");
=> "Hello, Bob!"
```

**Section 3: Exploring with REPL Commands (150 lines)**
- **`.help`** - Discover available commands
- **`.history`** - Review your session
- **`.vars`** - See defined variables
- **`.clear`** - Start fresh
- **Quick experimentation cycle:** Try → Refine → Test

```ml
ml[secure]> .help
Available commands:
  .help           Show this help message
  .exit, .quit    Exit the REPL
  .vars           Show all defined variables
  .clear          Clear all variables
  .reset          Reset REPL session
  .history        Show command history
  .capabilities   Show granted capabilities
  .grant <cap>    Grant capability
  .revoke <cap>   Revoke capability
  .retry          Retry last failed command
  .edit           Edit last statement in editor

ml[secure]> .vars
Variables:
  name = "Alice"
  greet = <function>

ml[secure]> .history
  [1] 2 + 2
  [2] name = "Alice";
  [3] print("Hello, " + name);
  [4] function greet(person) { return "Hello, " + person + "!"; }
  [5] greet(name);
  [6] greet("Bob");
```

**Section 4: When to Use Files (100 lines)**
- **REPL for:** Learning, testing, quick scripts
- **Files for:** Programs you want to save, larger projects, reusable code
- **Transition:** Save your REPL experiments to files

**Creating your first file:**
```ml
// hello.ml - Save your REPL experiments!
function greet(person) {
    return "Hello, " + person + "!";
}

print(greet("Alice"));
print(greet("Bob"));
```

**Running files:**
```bash
mlpy run hello.ml
# Hello, Alice!
# Hello, Bob!
```

**Section 5: Next Steps (50 lines)**
- **Continue with REPL:** Follow tutorial in REPL first
- **Try the tutorial:** Interactive learning with REPL examples
- **Learn REPL features:** Read REPL Guide for advanced features
- **Start projects:** Use `mlpy init` for larger applications

**Key Message:** **Start experimenting in the REPL right now** - no files needed!

**Example Code Snippets:**
```
docs/ml_snippets/getting-started/
├── first_repl_session.md      # REPL transcript showing first session
├── variables_in_repl.md       # REPL session: variables and expressions
├── functions_in_repl.md       # REPL session: defining functions
├── hello.ml                   # First file (transition from REPL)
└── exploring_repl.md          # REPL session: using commands
```

---

#### 1.2 REPL Guide (NEW - COMPREHENSIVE REFERENCE)

**Purpose:** Complete reference for mlpy REPL v2.3 with all features
**Length:** ~1200 lines
**Primary Sources:**
- `docs/summaries/repl-v2.3-implementation-summary.md`
- `src/mlpy/cli/repl.py` implementation
- REPL feature proposals

**Content Structure:**

**Section 1: Introduction (~100 lines)**
- What is the REPL
- Why use the REPL for ML development
- REPL vs file-based development
- When to use each approach
- Performance: <10ms average execution (v2.3)

**Section 2: Getting Started with REPL (~150 lines)**
- Starting the REPL: `mlpy repl`
- Understanding the prompt: `ml[secure]>`
- Security indicator meaning
- First commands
- Exiting the REPL

**Section 3: Basic REPL Usage (~200 lines)**
- **Entering Expressions:** Single-line and multi-line
- **Variable Persistence:** Variables persist across commands
- **Function Definitions:** Define functions interactively
- **Multi-line Input:** Automatic continuation prompt
- **Execution Feedback:** Result display and formatting

```ml
ml[secure]> x = 42;
ml[secure]> y = x + 10;
ml[secure]> y
=> 52

ml[secure]> function factorial(n) {
...   if (n <= 1) {
...     return 1;
...   }
...   return n * factorial(n - 1);
... }
ml[secure]> factorial(5);
=> 120
```

**Section 4: REPL Commands Reference (~400 lines)**

**Help and Information:**
- **`.help`** - Show all available commands
- **`.vars`** - List all defined variables with values
- **`.history`** - Show command history with line numbers

**Session Management:**
- **`.clear`** - Clear all variables (keep session)
- **`.reset`** - Complete session reset
- **`.exit` / `.quit`** - Exit REPL

**Error Recovery (v2.2+):**
- **`.retry`** - Re-execute last failed statement
- Use case: Fix syntax errors quickly
- Tracks last failed code and error message

```ml
ml[secure]> x = [1, 2, 3
Error: Parse Error: Invalid ML syntax
Tip: Check for missing semicolons, unmatched braces, or typos

ml[secure]> .retry
Retrying: x = [1, 2, 3
✗ Failed again: Parse Error: Invalid ML syntax

ml[secure]> x = [1, 2, 3];
ml[secure]> .retry
Retrying: x = [1, 2, 3];
✓ Success!
```

**External Editor Integration (v2.2+):**
- **`.edit`** - Edit last statement in external editor
- Respects `$EDITOR` environment variable
- Defaults: `notepad` (Windows), `vim` (Unix)
- Auto-execute after editing

```ml
ml[secure]> function complex_function() {
...   // Some complex logic
... }

ml[secure]> .edit
# Opens in notepad/vim
# Edit the function
# Save and close
Executing edited code...
✓ Done
```

**Capability Management (v2.2+):**
- **`.capabilities`** - List all granted capabilities
- **`.grant <capability>`** - Grant runtime capability
- **`.revoke <capability>`** - Revoke capability
- Security confirmation required for grants
- Audit logging for all capability changes

```ml
ml[secure]> .capabilities
No capabilities granted (security-restricted mode)

ml[secure]> .grant file.read

⚠️  Security Warning: Granting capability 'file.read'
This will allow ML code to access restricted functionality.
Grant this capability? [y/N]: y
✓ Granted capability: file.read

ml[secure]> .capabilities
Active Capabilities:
  • file.read

ml[secure]> import file;
ml[secure]> content = file.read("data.txt");
✓ Allowed - capability granted

ml[secure]> .revoke file.read
✓ Revoked capability: file.read
```

**Section 5: Advanced REPL Features (~300 lines)**

**Terminal Features (v2.1+):**
- **Syntax Highlighting:** Real-time ML syntax coloring
- **Auto-completion:** Tab-completion for variables, functions, modules
- **Command History:** Up/down arrows to navigate history
- **Persistent History:** Saved across sessions
- **Search History:** Ctrl+R for reverse search
- **Line Editing:** Emacs/Vi keybindings support

**Output Paging (v2.2+):**
- **Automatic paging:** Results >50 lines trigger pager
- **Interactive pager:** Space to scroll, Q to quit
- **Fallback system:** prompt_toolkit → system pager → truncation
- **Configurable threshold:** Adjust max_lines if needed

```ml
ml[secure]> large_array = range(0, 200);
--- Output (202 lines) - Press Space to scroll, Q to quit ---
[
  0,
  1,
  2,
  ...
]
# Interactive pager shown
```

**Performance (v2.3+):**
- **Incremental Transpilation:** Each statement transpiled independently
- **Sub-10ms execution:** 6.93ms average (10.8x faster than v2.2)
- **O(1) complexity:** Constant time per statement
- **100% success rate:** All statements execute reliably

**Security (v2.3+):**
- **Namespace Protection:** Blocks access to `__builtins__`, `eval`, `exec`, etc.
- **35+ dangerous identifiers blocked:** Comprehensive security
- **ML builtin wrappers safe:** `input()`, `help()` use safe wrappers
- **Full security analysis:** Same security as file-based compilation
- **Audit trail:** All capability grants/revokes logged

**Section 6: REPL Workflows and Patterns (~150 lines)**

**Learning ML:**
```ml
# Try concepts immediately
ml[secure]> x = [1, 2, 3, 4, 5];
ml[secure]> x[1:3]
=> [2, 3]

# Experiment with syntax
ml[secure]> result = x[0] > 5 ? "big" : "small";
=> "small"
```

**Prototyping Functions:**
```ml
# Develop function iteratively
ml[secure]> function isPrime(n) {
...   if (n <= 1) { return false; }
...   if (n <= 3) { return true; }
...   // Test with small values first
...   return true;
... }

ml[secure]> isPrime(5);
=> true

# Refine with .edit
ml[secure]> .edit
# Add complete implementation
# Test again
```

**Testing Standard Library:**
```ml
# Explore modules interactively
ml[secure]> import math;
ml[secure]> math.sqrt(16);
=> 4.0

ml[secure]> math.pi;
=> 3.141592653589793

# Try different approaches
ml[secure]> import datetime;
ml[secure]> now = datetime.now();
ml[secure]> now.year;
=> 2025
```

**Debugging:**
```ml
# Inspect values step by step
ml[secure]> data = [1, 2, 3, 4, 5];
ml[secure]> typeof(data);
=> "array"

ml[secure]> len(data);
=> 5

# Use .retry after errors
ml[secure]> result = data[10];
Error: Index out of range

ml[secure]> result = data[len(data) - 1];
ml[secure]> result
=> 5
```

**Section 7: Tips and Best Practices (~100 lines)**

**DO:**
- ✅ Use REPL for learning and experimentation
- ✅ Save successful experiments to files
- ✅ Use `.vars` to track your session state
- ✅ Use `.retry` to fix errors quickly
- ✅ Use `.edit` for complex multi-line code
- ✅ Use `.history` to review and replay commands
- ✅ Grant capabilities only when needed
- ✅ Use tab-completion to discover functionality

**DON'T:**
- ❌ Don't rely on REPL for production code
- ❌ Don't grant capabilities unnecessarily
- ❌ Don't forget to `.revoke` capabilities when done
- ❌ Don't assume REPL state persists after exit
- ❌ Don't try to access `__builtins__` or Python internals

**Performance Tips:**
- REPL v2.3 is fast: 6.93ms average execution
- No performance penalty for experimentation
- Variables persist efficiently across commands
- Functions compile once, execute many times

**Keyboard Shortcuts:**
- **Tab:** Auto-complete
- **Up/Down:** Command history
- **Ctrl+R:** Search history
- **Ctrl+C:** Cancel current input
- **Ctrl+D:** Exit REPL (Unix)

---

#### 1.3 Tutorial (COMPLETE REWRITE - REPL-FIRST LEARNING)

**CRITICAL REQUIREMENT:** Delete existing `tutorial.rst` entirely - it contains language and builtin incompatibilities and cannot be salvaged.

**Purpose:** Comprehensive REPL-first tutorial teaching ML programming from scratch
**Length:** ~1800-2200 lines
**Primary Sources:**
- **Grammar:** `src/mlpy/ml/grammar/ml.lark` - Source of truth for ML syntax
- **Integration Tests:** `tests/ml_integration/` - Examples of idiomatic ML code
- **Builtin Implementation:** `src/mlpy/stdlib/builtin.py` - Available builtin functions
- **REPL Implementation:** `src/mlpy/cli/repl.py` - REPL features and commands
- **DO NOT reference old tutorial** - complete rewrite required

**NEW PEDAGOGICAL APPROACH - REPL-FIRST:**
- **Every concept demonstrated in REPL first**
- **REPL sessions show learning in action**
- **Immediate experimentation encouraged**
- **Files introduced after REPL mastery**
- **"Try it now!" prompts throughout**

**Why Complete Rewrite is Required:**
1. **Syntax Incompatibilities:** Old tutorial uses `catch` instead of `elif`, missing features like `elif`, incorrect exception syntax
2. **Builtin Incompatibilities:** Old tutorial may reference builtins that don't exist or use them incorrectly
3. **Grammar Mismatch:** ML grammar has evolved; old examples may not parse correctly
4. **Missing Features:** No coverage of arrow functions, destructuring, enhanced assignments, REPL
5. **Best Practices Changed:** Current idiomatic ML code differs from old patterns
6. **No REPL Integration:** Old tutorial is file-focused, missing interactive learning

**Tutorial Structure:**

**Section 1: Introduction to ML (~200 lines)**
- What is ML and why use it
- Installing mlpy
- **Starting the REPL immediately** (PRIMARY LEARNING TOOL)
- Your first expressions in the REPL
- When to use REPL vs files

**REPL-First Approach:**
```ml
# Install and start REPL in <1 minute
$ pip install mlpy
$ mlpy repl
ml[secure]> print("Hello, ML!");
Hello, ML!
ml[secure]> 2 + 2
=> 4
```

**Section 2: Basic Syntax in the REPL (~350 lines)**
- Comments and code structure
- Variables and assignment **[REPL SESSION]**
- Data types (numbers, strings, booleans) **[REPL EXPERIMENTS]**
- Basic operators **[LIVE CALCULATIONS]**
- print() for output **[IMMEDIATE FEEDBACK]**
- Using `.vars` to inspect your session **[REPL COMMAND]**
- **Source:** Study `src/mlpy/ml/grammar/ml.lark` for syntax rules
- **Examples:** From `tests/ml_integration/ml_core/` basic tests

**REPL Learning Session Example:**
```ml
ml[secure]> // This is a comment
ml[secure]> x = 42;  // Variables
ml[secure]> name = "Alice";
ml[secure]> active = true;

ml[secure]> .vars  // Inspect what we've created
Variables:
  x = 42
  name = "Alice"
  active = true

ml[secure]> // Try different types
ml[secure]> typeof(x);
=> "number"
ml[secure]> typeof(name);
=> "string"
ml[secure]> typeof(active);
=> "boolean"

ml[secure]> // Basic math
ml[secure]> x + 10;
=> 52
ml[secure]> x * 2;
=> 84
```

**"Try It Now!" Prompt:**
> **Try it yourself!** Start the REPL and experiment with different data types. What happens when you add a number and a string? Try it!

**Section 3: Control Flow in the REPL (~400 lines)**
- if statements **[REPL EXPERIMENTATION]**
- elif clauses (newly implemented!) **[REPL EXAMPLES]**
- else clauses
- Comparison operators **[LIVE TESTING]**
- Logical operators (&&, ||, !) **[IMMEDIATE RESULTS]**
- Ternary operator **[QUICK CONDITIONALS]**
- Using `.history` to review your experiments **[REPL COMMAND]**
- **Source:** Review `tests/ml_integration/ml_core/08_control_structures.ml`
- **Examples:** Real control flow patterns from integration tests

**REPL Learning Session Example:**
```ml
ml[secure]> score = 85;
ml[secure]> if (score >= 90) {
...   print("A");
... } elif (score >= 80) {
...   print("B");
... } else {
...   print("C");
... }
B

ml[secure]> // Try ternary operator
ml[secure]> grade = score >= 80 ? "Pass" : "Fail";
=> "Pass"

ml[secure]> // Experiment with different scores
ml[secure]> score = 92;
ml[secure]> .history  // See your experiments
[... previous commands ...]
```

**Section 4: Loops and Iteration in the REPL (~350 lines)**
- while loops **[REPL EXECUTION]**
- for loops (for item in collection) **[IMMEDIATE ITERATION]**
- break and continue **[LIVE EXAMPLES]**
- range() builtin for numeric iteration **[REPL TESTING]**
- Iterating over arrays and objects
- **Source:** Review `tests/ml_integration/ml_core/12_for_loops.ml`
- **Builtins:** Use range() from `src/mlpy/stdlib/builtin.py`

**REPL Learning Session Example:**
```ml
ml[secure]> // Try range() interactively
ml[secure]> range(5);
=> [0, 1, 2, 3, 4]

ml[secure]> // Use in for loop
ml[secure]> for (i in range(5)) {
...   print(i);
... }
0
1
2
3
4

ml[secure]> // Build array with loop
ml[secure]> squares = [];
ml[secure]> for (i in range(1, 6)) {
...   squares = squares + [i * i];
... }
ml[secure]> squares;
=> [1, 4, 9, 16, 25]
```

**Section 5: Functions in the REPL (~450 lines)**
- Function definitions **[DEFINE INTERACTIVELY]**
- Parameters and return values **[IMMEDIATE TESTING]**
- Arrow functions (fn syntax) **[QUICK FUNCTIONS]**
- Closures and scope **[LIVE EXPERIMENTATION]**
- Recursion examples **[STEP-BY-STEP DEBUGGING]**
- Higher-order functions **[REPL COMPOSITION]**
- Using `.edit` for complex functions **[REPL COMMAND]**
- **Source:** Review `tests/ml_integration/ml_core/14_arrow_functions.ml`, `07_closures_functions.ml`
- **Examples:** fibonacci, factorial, map/filter patterns

**REPL Learning Session Example:**
```ml
ml[secure]> // Define function interactively
ml[secure]> function factorial(n) {
...   if (n <= 1) {
...     return 1;
...   }
...   return n * factorial(n - 1);
... }
ml[secure]> factorial(5);
=> 120

ml[secure]> // Arrow functions
ml[secure]> double = fn(x) => x * 2;
ml[secure]> double(21);
=> 42

ml[secure]> // Edit complex function
ml[secure]> .edit  // Opens editor for refinement
```

**Section 6: Data Structures in the REPL (~400 lines)**
- Arrays: creation, indexing, slicing **[LIVE MANIPULATION]**
- Objects: creation, property access, methods **[INTERACTIVE OBJECTS]**
- Array methods (from builtin) **[IMMEDIATE RESULTS]**
- Object methods (from builtin) **[PROPERTY EXPLORATION]**
- Destructuring assignment **[REPL EXAMPLES]**
- **Source:** Review `tests/ml_integration/ml_core/15_destructuring.ml`
- **Builtins:** len(), keys(), values(), entries() from builtin.py

**REPL Learning Session Example:**
```ml
ml[secure]> // Arrays in REPL
ml[secure]> nums = [1, 2, 3, 4, 5];
ml[secure]> nums[1:3];
=> [2, 3]

ml[secure]> // Objects interactively
ml[secure]> person = {name: "Alice", age: 30};
ml[secure]> person.name;
=> "Alice"

ml[secure]> // Use .vars to track data structures
ml[secure]> .vars
Variables:
  nums = [1, 2, 3, 4, 5]
  person = {name: "Alice", age: 30}
```

**Section 7: Working with Builtins in the REPL (~350 lines)**
- Type checking with typeof() **[INSTANT TYPE INFO]**
- Type conversion: int(), float(), str() **[LIVE CONVERSION]**
- Collection operations: len(), range() **[IMMEDIATE USE]**
- Math utilities: abs(), min(), max(), sum() **[QUICK CALCULATIONS]**
- Testing builtins interactively **[REPL EXPLORATION]**
- **Source:** Comprehensive coverage from `src/mlpy/stdlib/builtin.py`
- **Examples:** From `tests/ml_integration/ml_builtin/` test files

**REPL Learning Session Example:**
```ml
ml[secure]> // Explore type system
ml[secure]> typeof(42);
=> "number"
ml[secure]> typeof([1,2,3]);
=> "array"

ml[secure]> // Type conversions
ml[secure]> int("42");
=> 42
ml[secure]> str(42);
=> "42"

ml[secure]> // Math utilities
ml[secure]> numbers = [1, 5, 3, 9, 2];
ml[secure]> sum(numbers);
=> 20
ml[secure]> max(numbers);
=> 9
```

**Section 8: Exception Handling in the REPL (~300 lines)**
- try/except/finally blocks **[SAFE EXPERIMENTATION]**
- Throwing exceptions **[REPL TESTING]**
- Error objects and messages **[IMMEDIATE FEEDBACK]**
- Using `.retry` for error recovery **[REPL COMMAND]**
- Exception handling patterns
- **CRITICAL:** Use `except`, NOT `catch` (common mistake in old docs)
- **Source:** Review `tests/ml_integration/ml_core/16_exceptions_complete.ml`

**REPL Learning Session Example:**
```ml
ml[secure]> // Try error handling
ml[secure]> try {
...   result = 10 / 0;
... } except (e) {
...   print("Error: " + e.message);
... }
Error: division by zero

ml[secure]> // Use .retry for quick fixes
ml[secure]> x = [1, 2, 3
Error: Parse Error: Unterminated array

ml[secure]> .retry
Retrying: x = [1, 2, 3
✗ Failed again

ml[secure]> x = [1, 2, 3];
ml[secure]> x;
=> [1, 2, 3]
```

**Section 9: Working with Modules in the REPL (~350 lines)**
- Importing standard library modules **[LIVE IMPORTS]**
- Using console module for output **[IMMEDIATE USE]**
- Using math module for calculations **[REPL MATH]**
- Using json module for data **[JSON EXPLORATION]**
- Testing modules interactively **[SAFE EXPERIMENTATION]**
- Practical examples combining modules
- **Source:** Integration test examples using stdlib modules

**REPL Learning Session Example:**
```ml
ml[secure]> // Import and use modules
ml[secure]> import math;
ml[secure]> math.sqrt(16);
=> 4.0

ml[secure]> math.pi;
=> 3.141592653589793

ml[secure]> // JSON module
ml[secure]> import json;
ml[secure]> data = {name: "Alice", age: 30};
ml[secure]> json_string = json.stringify(data);
=> '{"name": "Alice", "age": 30}'
```

**Section 10: From REPL to Files (~300 lines)**
- **When to save your code** (reusable programs, larger projects)
- **Saving REPL experiments to files**
- **Running files:** `mlpy run script.ml`
- **Transitioning workflow:** REPL prototype → File implementation
- **Best practices:** Use REPL for testing, files for production

**Workflow Example:**
```ml
# 1. Prototype in REPL
ml[secure]> function isPrime(n) {
...   // Develop and test here
... }
ml[secure]> isPrime(7);
=> true

# 2. Save to file once working
# prime.ml
function isPrime(n) {
    if (n <= 1) { return false; }
    if (n <= 3) { return true; }
    // ... complete implementation
}

# Test with multiple values
for (num in range(2, 20)) {
    if (isPrime(num)) {
        print(num);
    }
}

# 3. Run file
$ mlpy run prime.ml
```

**Section 11: Practical Projects (REPL + Files) (~600 lines)**
- **Project 1:** Number guessing game **[REPL DEVELOPMENT → FILE]**
  - Build interactively in REPL
  - Save working version to file
  - Add features and iterate
- **Project 2:** Todo list manager **[REPL PROTOTYPING]**
  - Test data structures in REPL
  - Prototype functions interactively
  - Save complete implementation
- **Project 3:** Simple calculator **[REPL TESTING]**
  - Test operators and functions in REPL
  - Build error handling interactively
  - Create file-based calculator
- **Project 4:** Data analysis script **[REPL → PRODUCTION]**
  - Explore data in REPL
  - Test analysis functions interactively
  - Build complete analysis pipeline in file

**Each project demonstrates:**
- REPL for rapid prototyping
- Interactive testing and refinement
- Transition to file-based code
- Best practices for both approaches

**Tutorial Development Process:**

1. **FIRST:** Read and study ML grammar (`src/mlpy/ml/grammar/ml.lark`)
2. **SECOND:** Review all integration tests in `tests/ml_integration/ml_core/`
3. **THIRD:** Study builtin implementation in `src/mlpy/stdlib/builtin.py`
4. **FOURTH:** Write tutorial sections using verified syntax and builtins
5. **FIFTH:** Create executable snippets in `docs/ml_snippets/tutorial/`
6. **SIXTH:** Test all tutorial code with mlpy to ensure it executes
7. **SEVENTH:** Verify tutorial teaches current best practices

**Code Snippet Organization (REPL-INTEGRATED):**
```
docs/ml_snippets/tutorial/
├── 01_introduction/
│   ├── first_repl_session.transcript    # REPL session: First commands
│   ├── hello_world.ml
│   └── first_program.ml
├── 02_basic_syntax/
│   ├── variables_repl.transcript        # REPL session: Exploring variables
│   ├── variables.ml
│   ├── data_types_repl.transcript       # REPL session: Type experiments
│   ├── data_types.ml
│   └── operators.ml
├── 03_control_flow/
│   ├── if_elif_else_repl.transcript     # REPL session: Testing conditionals
│   ├── if_elif_else.ml
│   ├── ternary_repl.transcript          # REPL session: Ternary experiments
│   ├── ternary.ml
│   └── comparisons.ml
├── 04_loops/
│   ├── for_loop_repl.transcript         # REPL session: Interactive loops
│   ├── while_loop.ml
│   ├── for_loop.ml
│   └── range_iteration_repl.transcript  # REPL session: Range experiments
├── 05_functions/
│   ├── function_repl.transcript         # REPL session: Define and test functions
│   ├── basic_function.ml
│   ├── arrow_function_repl.transcript   # REPL session: Arrow function experiments
│   ├── arrow_function.ml
│   ├── closures.ml
│   └── recursion_repl.transcript        # REPL session: Debugging recursion
├── 06_data_structures/
│   ├── arrays_repl.transcript           # REPL session: Array manipulation
│   ├── arrays.ml
│   ├── objects_repl.transcript          # REPL session: Object exploration
│   ├── objects.ml
│   ├── slicing.ml
│   └── destructuring.ml
├── 07_builtins/
│   ├── typeof_repl.transcript           # REPL session: Type exploration
│   ├── typeof_usage.ml
│   ├── conversions_repl.transcript      # REPL session: Type conversion tests
│   ├── conversions.ml
│   ├── collections.ml
│   └── utilities.ml
├── 08_exceptions/
│   ├── error_handling_repl.transcript   # REPL session: Using .retry command
│   ├── try_except.ml
│   ├── finally_clause.ml
│   └── throwing.ml
├── 09_modules/
│   ├── modules_repl.transcript          # REPL session: Exploring stdlib
│   ├── console_examples.ml
│   ├── math_examples.ml
│   └── json_examples.ml
├── 10_repl_to_files/
│   ├── development_workflow.transcript  # REPL session: Prototype → File
│   ├── prime_prototype_repl.transcript
│   └── prime_final.ml
└── 11_projects/
    ├── guessing_game_dev.transcript     # REPL session: Building game
    ├── guessing_game.ml
    ├── todo_list_prototype.transcript
    ├── todo_list.ml
    ├── calculator_repl.transcript
    ├── calculator.ml
    ├── data_analysis_repl.transcript
    └── data_analysis.ml
```

**NEW: REPL Transcript Format (.transcript files)**
- REPL sessions showing interactive development
- Demonstrate REPL commands (`.help`, `.vars`, `.history`, `.retry`, `.edit`)
- Show learning process with trial and error
- Include "Try it now!" prompts
- Validate that transcripts are accurate REPL sessions

**Quality Requirements:**
- ✅ Every code snippet must execute successfully with current mlpy
- ✅ All syntax verified against `src/mlpy/ml/grammar/ml.lark`
- ✅ All builtins verified against `src/mlpy/stdlib/builtin.py`
- ✅ Follow patterns from `tests/ml_integration/` for idiomatic code
- ✅ Progressive difficulty: each section builds on previous
- ✅ Practical examples: real-world use cases, not toy examples
- ✅ Zero references to old tutorial content

---

#### 1.3 Language Reference (MAJOR REWRITE)

##### 1.3.1 Lexical Structure (NEW - ~400 lines)

**Content:**
- **Source Code Encoding:** UTF-8, BOM handling
- **Comments:** Single-line (`//`), multi-line patterns
- **Identifiers:** Naming rules, conventions, case sensitivity
- **Keywords:** Complete reserved word list with examples
- **Literals:**
  - Number literals: integers, floats, scientific notation (1.5e6, 6.626e-34)
  - String literals: single/double quotes, escape sequences
  - Boolean literals: true, false
  - Null literal: null

**Comprehensive Examples from Integration Tests:**
```ml
// Number literals (from ml_core tests)
integer = 42;
negative = -17;
float_num = 3.14159;
scientific = 1.5e6;           // 1,500,000
planck = 6.626e-34;           // Very small
avogadro = 6.022e23;          // Avogadro's number

// String literals
single_quote = 'Hello';
double_quote = "World";
escaped = "Line 1\nLine 2\tTabbed";

// Identifiers
userName = "Alice";
_privateVar = 42;
MAX_CONSTANT = 100;
```

---

##### 1.3.2 Data Types (NEW - ~500 lines)

**Content:**
- **Primitive Types:**
  - Numbers (integer and float unified)
  - Strings (immutable sequences)
  - Booleans (true/false)
  - Null (absence of value)
- **Composite Types:**
  - Arrays: ordered, mutable, heterogeneous
  - Objects: key-value pairs, dynamic properties
- **Type Checking:** typeof() function
- **Type Conversions:** int(), float(), str()

**Examples from Builtin Tests:**
```ml
// Type checking
typeof(42);          // "number"
typeof("hello");     // "string"
typeof(true);        // "boolean"
typeof([1,2,3]);     // "array"
typeof({a: 1});      // "object"
typeof(main);        // "function"

// Type conversions
int("42");           // 42
int(3.7);            // 3
int(true);           // 1
float("3.14");       // 3.14
float(42);           // 42.0
str(42);             // "42"
str(true);           // "true"
str([1,2,3]);        // "[1, 2, 3]"

// Arrays
numbers = [1, 2, 3, 4, 5];
mixed = [42, "hello", true, [1,2], {a: 1}];
empty = [];

// Objects
person = {
    name: "Alice",
    age: 30,
    active: true
};
```

---

##### 1.3.3 Expressions (NEW - ~600 lines)

**Content:**
- **Operator Precedence Table:** Complete reference
- **Arithmetic Operators:** +, -, *, /, //, %
- **Comparison Operators:** ==, !=, <, >, <=, >=
- **Logical Operators:** &&, ||, !
- **Ternary Operator:** condition ? true_val : false_val
- **Member Access:** obj.property
- **Array Access:** arr[index]
- **Slice Expressions:** arr[start:end:step]
- **Function Calls:** func(arg1, arg2)

**Operator Precedence (Highest to Lowest):**
1. Member access (.), array access ([])
2. Function calls ()
3. Unary operators (!, -)
4. Multiplication, division (*, /, //, %)
5. Addition, subtraction (+, -)
6. Comparison (<, >, <=, >=)
7. Equality (==, !=)
8. Logical AND (&&)
9. Logical OR (||)
10. Ternary (?:)

**Slicing Examples from Tests:**
```ml
// Array slicing
arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
arr[2:5];        // [2, 3, 4]
arr[:3];         // [0, 1, 2]
arr[7:];         // [7, 8, 9]
arr[::2];        // [0, 2, 4, 6, 8]
arr[1:8:2];      // [1, 3, 5, 7]
arr[-3:];        // [7, 8, 9]

// String slicing
text = "Hello World";
text[0:5];       // "Hello"
text[6:];        // "World"
text[::-1];      // "dlroW olleH"
```

---

##### 1.3.4 Statements (NEW - ~400 lines)

**Content:**
- **Expression Statements:** expr;
- **Assignment Statements:** var = value;
- **Enhanced Assignments:**
  - Array element: arr[i] = value;
  - Object property: obj.prop = value;
- **Destructuring Assignments:**
  - Array: [a, b, c] = array;
  - Object: {x, y, z} = object;

**Destructuring Examples from Tests:**
```ml
// Array destructuring
[first, second, third] = [1, 2, 3];
// first = 1, second = 2, third = 3

// Object destructuring
{name, age, city} = {name: "Alice", age: 30, city: "NYC"};
// name = "Alice", age = 30, city = "NYC"

// Enhanced assignments
arr = [1, 2, 3];
arr[1] = 99;                  // arr = [1, 99, 3]

obj = {x: 10, y: 20};
obj.x = 100;                  // obj = {x: 100, y: 20}
obj.z = 30;                   // obj = {x: 100, y: 20, z: 30}
```

---

##### 1.3.5 Functions (NEW - ~550 lines)

**Content:**
- **Function Definitions:**
  - Named functions: function name(params) { body }
  - Parameters and return values
- **Arrow Functions:**
  - Syntax: fn(params) => expression
  - Block syntax: fn(params) => { statements }
  - Use cases and limitations
- **Function Calls:** func(args)
- **Closures:** Capturing outer scope
- **Recursion:** Direct and indirect

**Function Examples from Core Tests:**
```ml
// Named function definition
function add(a, b) {
    return a + b;
}

// Arrow function (expression body)
double = fn(x) => x * 2;

// Arrow function (block body)
factorial = fn(n) => {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
};

// Closures
function makeCounter() {
    count = 0;
    return fn() => {
        count = count + 1;
        return count;
    };
}
counter = makeCounter();
counter();  // 1
counter();  // 2

// Higher-order functions
function map(arr, func) {
    result = [];
    for (item in arr) {
        result = result + [func(item)];
    }
    return result;
}
numbers = [1, 2, 3, 4, 5];
doubled = map(numbers, fn(x) => x * 2);  // [2, 4, 6, 8, 10]
```

---

##### 1.3.6 Control Flow (NEW - ~450 lines)

**Content:**
- **If Statements:** if (condition) { ... }
- **Elif Clauses:** elif (condition) { ... }
- **Else Clauses:** else { ... }
- **While Loops:** while (condition) { ... }
- **For Loops:** for (var in iterable) { ... }
- **Break Statement:** break;
- **Continue Statement:** continue;
- **Return Statement:** return value;

**Control Flow Examples from Tests:**
```ml
// If-elif-else (newly implemented!)
function getGrade(score) {
    if (score >= 90) {
        return "A";
    } elif (score >= 80) {
        return "B";
    } elif (score >= 70) {
        return "C";
    } elif (score >= 60) {
        return "D";
    } else {
        return "F";
    }
}

// While loop
count = 0;
while (count < 5) {
    print(count);
    count = count + 1;
}

// For loop
numbers = [1, 2, 3, 4, 5];
for (num in numbers) {
    print(num);
}

// Break and continue
for (i in range(10)) {
    if (i == 3) { continue; }  // Skip 3
    if (i == 7) { break; }     // Stop at 7
    print(i);  // Prints: 0, 1, 2, 4, 5, 6
}
```

---

##### 1.3.7 Exception Handling (NEW - ~400 lines)

**Content:**
- **Try-Except-Finally:** Exception handling syntax
- **Throw Statement:** Throwing exceptions
- **Error Objects:** Structure and properties
- **Best Practices:** When and how to use exceptions

**Exception Examples from Tests:**
```ml
// Basic try-except
try {
    result = 10 / 0;
} except (error) {
    print("Error occurred: " + error.message);
}

// Multiple except clauses
try {
    risky_operation();
} except (e1) {
    print("First handler");
} except (e2) {
    print("Second handler");
}

// Finally clause (always executes)
try {
    file = open("data.txt");
    process(file);
} except (e) {
    print("Error: " + e.message);
} finally {
    close(file);
}

// Throwing exceptions
function divide(a, b) {
    if (b == 0) {
        throw {message: "Division by zero", code: "DIV_ZERO"};
    }
    return a / b;
}
```

---

##### 1.3.8 Advanced Features (NEW - ~350 lines)

**Content:**
- **Nonlocal Statement:** Modifying outer scope variables
- **Scope Rules:** Local, nonlocal, global
- **Dynamic Features:** Runtime introspection

**Nonlocal Examples from Tests:**
```ml
// Nonlocal statement
function outer() {
    count = 0;

    function increment() {
        nonlocal count;
        count = count + 1;
        return count;
    }

    function get_count() {
        return count;
    }

    return {inc: increment, get: get_count};
}

counter = outer();
counter.inc();  // 1
counter.inc();  // 2
counter.get();  // 2
```

---

##### 1.3.9 Capability System - Language Reference (NEW - ~800 lines)

**Purpose:** Complete language-level reference for capability declarations and patterns in ML
**Audience:** ML developers who need to declare and use capabilities in their code

**Note:** This system is not fully implemented yet. The syntax shown here is the planned design and will need updates as implementation progresses.

**Content Structure:**

**Section 1: Capability Declaration Syntax (~200 lines)**

**Basic Declaration:**
```ml
// Declare a capability block (future syntax - not yet implemented)
capability CapabilityName {
    allow operation "pattern";
    allow operation "pattern2";
}
```

**Current Implementation (Python API):**
```ml
// Currently, capabilities are granted via:
// 1. REPL commands: .grant capability.type
// 2. Python API: CapabilityContext and CapabilityToken
// 3. Not yet declarable in ML syntax
```

**Planned ML Syntax:**
```ml
// Future: Declare capabilities at module level
capability FileAccess {
    description: "Access to data files";
    allow file.read "/data/*";
    allow file.write "/output/*";
}

capability APIAccess {
    description: "External API access";
    allow network.https "https://api.example.com/*";
    expires: datetime.now().add_hours(24);
}

// Use in module
require capability FileAccess;

import file;
data = file.read("/data/input.txt");  // ✓ Allowed by capability
```

**Section 2: Capability Types and Operations (~200 lines)**

**File System Capabilities:**
```ml
// File operations
capability FileOps {
    allow file.read "/path/to/files/*";      // Read files
    allow file.write "/path/to/output/*";    // Write/create files
    allow file.append "/path/to/logs/*.log"; // Append to files
    allow file.delete "/tmp/cache/*";        // Delete files
}

// Path operations
capability PathOps {
    allow path.read "/data/";        // Query directory structure
    allow path.write "/output/";     // Create directories
}
```

**Network Capabilities:**
```ml
capability NetworkOps {
    allow network.http "http://internal.api/*";      // HTTP requests
    allow network.https "https://api.example.com/*"; // HTTPS requests (more secure)
}
```

**Console and Cryptography:**
```ml
capability ConsoleOps {
    allow console.write;   // Standard output
    allow console.error;   // Error output
}

capability CryptoOps {
    allow crypto.hash;     // Cryptographic hashing
    allow crypto.random;   // Secure random generation
}
```

**Complete Capability Type Reference:**
```ml
// All capability types in mlpy

// File system
file.read       // Read file contents
file.write      // Create or modify files
file.append     // Append to existing files
file.delete     // Delete files
path.read       // Query paths (exists, is_dir, etc.)
path.write      // Create/modify directory structure

// Network
network.http    // HTTP requests
network.https   // HTTPS requests

// Console
console.write   // Write to stdout
console.error   // Write to stderr

// Cryptography
crypto.hash     // Cryptographic hashing
crypto.random   // Secure random generation
```

**Section 3: Resource Pattern Syntax (~200 lines)**

**Pattern Matching Rules:**
```ml
// Exact match
allow file.read "/data/config.json";  // Only this specific file

// Wildcard match - single directory level
allow file.read "/data/*";            // All files in /data/
                                      // Does NOT match /data/subdir/file.txt

// Recursive wildcard - all subdirectories
allow file.read "/data/**/*";         // All files in /data/ and subdirectories
                                      // Matches /data/file.txt
                                      // Matches /data/subdir/file.txt
                                      // Matches /data/a/b/c/file.txt

// Prefix matching
allow file.read "/tmp/session_*";     // All files starting with session_
                                      // Matches /tmp/session_123.dat
                                      // Matches /tmp/session_abc.tmp

// Extension filtering
allow file.read "/data/**/*.csv";     // All CSV files recursively
allow file.write "/output/**/*.json"; // All JSON files recursively

// Multiple patterns in one capability
capability DataAccess {
    allow file.read "/data/**/*.csv";
    allow file.read "/config/*.conf";
    allow file.read "/input/**/*.txt";
    allow file.write "/output/**/*";
    allow file.write "/logs/*.log";
}
```

**Network Pattern Examples:**
```ml
capability APIAccess {
    // Domain-specific access
    allow network.https "https://api.example.com/*";

    // Subdomain wildcard
    allow network.https "https://*.example.com/*";

    // Specific endpoints
    allow network.https "https://api.example.com/users/*";
    allow network.https "https://api.example.com/data/*";

    // Port-specific (future feature)
    allow network.http "http://localhost:8080/*";
}
```

**Section 4: Capability Constraints (~200 lines)**

**Time-Based Constraints:**
```ml
// Expiration time (future syntax)
capability TemporaryAccess {
    allow file.read "/data/*";
    expires: datetime.now().add_hours(1);  // Valid for 1 hour
}

// Usage count limit (future syntax)
capability LimitedAccess {
    allow file.read "/data/*";
    max_uses: 10;  // Can only be used 10 times
}
```

**Resource Limits:**
```ml
// File size limits (future syntax)
capability RestrictedFileAccess {
    allow file.read "/data/*";
    max_file_size: 10 * 1024 * 1024;  // 10 MB limit
}

// Memory limits (future syntax)
capability MemoryRestrictedOps {
    allow file.read "/large_data/*";
    max_memory: 100 * 1024 * 1024;  // 100 MB memory limit
}
```

**Combined Constraints:**
```ml
capability StrictAccess {
    description: "Strictly limited data access";

    // Resource patterns
    allow file.read "/data/**/*.csv";

    // Time constraint
    expires: datetime.now().add_days(7);

    // Usage constraint
    max_uses: 100;

    // Size constraint
    max_file_size: 50 * 1024 * 1024;  // 50 MB
}
```

**Section 5: Capability Usage in Code (~100 lines)**

**Import-Time Capability Checks:**
```ml
// Importing modules that require capabilities
import file;   // Requires file.read or file.write capability
import http;   // Requires network.http or network.https capability
import path;   // Requires path.read or path.write capability
```

**Runtime Capability Checks:**
```ml
// Operations check capabilities at runtime
import file;

// Each operation validates capability
file.read("/data/input.txt");    // Checks file.read capability + pattern match
file.write("/output/result.txt", data); // Checks file.write capability + pattern match

// DENIED operations raise errors
try {
    file.read("/etc/passwd");  // Not in allowed pattern
} except (e) {
    print("Access denied: " + e.message);
    // Error: Capability violation - resource not in allowed pattern
}
```

**Capability Error Handling:**
```ml
import file;

function safe_read_file(filepath) {
    try {
        return file.read(filepath);
    } except (e) {
        // Handle capability errors gracefully
        if (typeof(e.code) == "string" && e.code == "CAPABILITY_DENIED") {
            print("Permission denied for: " + filepath);
            return null;
        }
        throw e;  // Re-throw other errors
    }
}
```

**Example Code Snippets for Language Reference:**
```
docs/ml_snippets/language-reference/capabilities/
├── basic_declaration.ml       # Basic capability syntax (future)
├── file_capabilities.ml       # File system capabilities
├── network_capabilities.ml    # Network access capabilities
├── pattern_matching.ml        # Resource pattern examples
├── constraints.ml             # Time/usage/size constraints
├── error_handling.ml          # Capability error handling
└── complete_example.ml        # Full working example
```

---

#### 1.4 Standard Library Documentation

**CRITICAL REQUIREMENTS:**

1. **Complete Rewrite Required:** Existing standard library documentation is COMPLETELY OBSOLETE and must be deleted entirely. Do not reference or reuse any existing stdlib documentation content.

2. **One File Per Module:** Create a separate `.rst` file for each standard library module in `docs/source/standard-library/`:
   - `builtin-functions.rst` (FIRST - document separately)
   - `console.rst`
   - `math.rst`
   - `string.rst` (not documented as module, document string methods available on string values)
   - `array.rst` (not documented as module, document array methods available on array values)
   - `datetime.rst`
   - `json.rst`
   - `collections.rst`
   - `functional.rst`
   - `regex.rst`
   - `random.rst`
   - `file.rst` (NEW)
   - `path.rst` (NEW)
   - `http.rst` (NEW)

3. **Primary Sources for Documentation:**
   - **For builtin:** Consult `src/mlpy/stdlib/builtin.py` for implementation and `tests/ml_integration/ml_builtin/*.ml` for practical examples
   - **For each stdlib module:** Consult the corresponding Python bridge module (`src/mlpy/stdlib/{module}_bridge.py`) and integration test files (`tests/ml_integration/ml_stdlib/*.ml`)
   - **Do NOT reference existing documentation** - it is outdated and incorrect

4. **Documentation Order:** Document `builtin-functions.rst` FIRST and separately, as all builtin functionality is fundamental and stored in `src/mlpy/stdlib/builtin.py`.

##### Format for Each Module

**Consistent Structure:**
```rst
Module Name
===========

Overview paragraph describing the module.

**Module:** ``module_name``
**Implementation:** ``src/mlpy/stdlib/{module}_bridge.py``
**Test Suite:** ``tests/ml_integration/ml_stdlib/{test_files}.ml``
**Capabilities Required:** capability.type

Quick Reference
---------------

.. table:: Function Quick Reference
   :widths: auto

   =====================  ================================  ====================
   Function               Description                       Capability
   =====================  ================================  ====================
   func1(args)            Brief description                 cap.required
   func2(args)            Brief description                 cap.required
   =====================  ================================  ====================

Functions
---------

function_name()
^^^^^^^^^^^^^^^

.. code-block:: ml

   result = module.function_name(arg1, arg2)

Detailed description.

**Parameters:**

- ``arg1`` (type) - Description
- ``arg2`` (type) - Description

**Returns:** (type) Description

**Capability:** capability.required

**Examples:**

.. literalinclude:: ../../ml_snippets/stdlib/{module}/{example_file}.ml
   :language: ml
   :lines: 1-20

**See Also:** Related functions
```

---

##### 1.4.1 Builtin Functions (COMPLETE REWRITE - ~800 lines)

**PRIORITY: DOCUMENT FIRST**

**Primary Sources:**
- **Implementation:** `src/mlpy/stdlib/builtin.py` - Complete builtin implementation
- **Test Suite:** `tests/ml_integration/ml_builtin/*.ml` - 17 comprehensive test files covering all builtin functionality
- **DO NOT reference old documentation** - complete rewrite required

**Test Files to Consult:**
```
tests/ml_integration/ml_builtin/
├── 01_type_conversion.ml          # int(), float(), str() conversions
├── 02_type_checking.ml            # typeof() usage patterns
├── 03_collection_functions.ml     # len(), range()
├── 04_print_functions.ml          # print() variations
├── 05_math_utilities.ml           # abs(), min(), max(), sum()
├── 06_array_utilities.ml          # map(), filter(), reduce()
├── 07_object_utilities.ml         # keys(), values(), entries()
├── 08_predicate_functions.ml      # all(), any(), none()
├── 09_sum_function.ml             # sum() advanced usage
├── 10_char_conversions.ml         # ord(), chr()
├── 11_number_base_conversions.ml  # bin(), hex(), oct()
├── 12_string_representations.ml   # repr(), ascii()
├── 13_reversed_function.ml        # reversed()
├── 14_dynamic_introspection.ml    # hasattr(), getattr(), setattr()
├── 15_edge_cases.ml               # Edge cases and error handling
├── 16_comprehensive_integration.ml # Complex integration scenarios
└── 17_iterator_functions.ml       # enumerate(), zip()
```

**All Builtin Functions:**
```ml
// Type checking
typeof(value)         // Returns: "number", "string", "boolean", "array", "object", "function"

// Type conversions
int(value)            // Convert to integer
float(value)          // Convert to float
str(value)            // Convert to string

// Collection operations
len(collection)       // Length of string, array, or object
range(stop)           // range(5) => [0, 1, 2, 3, 4]
range(start, stop)    // range(2, 5) => [2, 3, 4]
range(start, stop, step)  // range(0, 10, 2) => [0, 2, 4, 6, 8]

// Output
print(...values)      // Print values to stdout
```

**Comprehensive Examples:**
```ml
// typeof examples
typeof(42);           // "number"
typeof(3.14);         // "number"
typeof("hello");      // "string"
typeof(true);         // "boolean"
typeof([1, 2, 3]);    // "array"
typeof({x: 1});       // "object"
typeof(myFunc);       // "function"
typeof(null);         // "unknown"

// Type conversion examples
int("42");            // 42
int("  -17  ");       // -17
int("3.7");           // 3 (truncates)
int(3.99);            // 3
int(true);            // 1
int(false);           // 0

float("3.14");        // 3.14
float("42");          // 42.0
float(42);            // 42.0
float(true);          // 1.0

str(42);              // "42"
str(3.14);            // "3.14"
str(true);            // "true"
str(false);           // "false"
str([1, 2, 3]);       // "[1, 2, 3]"

// Collection operations
len("hello");         // 5
len([1, 2, 3, 4]);    // 4
len({a: 1, b: 2});    // 2

range(5);             // [0, 1, 2, 3, 4]
range(2, 8);          // [2, 3, 4, 5, 6, 7]
range(0, 10, 2);      // [0, 2, 4, 6, 8]
range(10, 0, -2);     // [10, 8, 6, 4, 2]
```

---

##### 1.4.2 Console Module (COMPLETE REWRITE - ~400 lines)

**Primary Sources:**
- **Implementation:** `src/mlpy/stdlib/console_module.py` - Console module implementation
- **Test Suite:** `tests/ml_integration/ml_stdlib/01_console_basic.ml`, `02_console_formatting.ml`
- **DO NOT reference old documentation** - complete rewrite required

Consult implementation and test files for complete function list and usage patterns.

---

##### 1.4.3 Math Module (COMPLETE REWRITE - ~500 lines)

**Primary Sources:**
- **Implementation:** `src/mlpy/stdlib/math_bridge.py` - Math module implementation
- **Test Suite:** `tests/ml_integration/ml_stdlib/03_math_basic.ml`, `04_math_trigonometry.ml`, `05_math_advanced.ml`
- **DO NOT reference old documentation** - complete rewrite required

Consult implementation and test files for complete function list including basic operations, trigonometry, and advanced functions.

---

##### 1.4.4 Datetime Module (COMPLETE REWRITE - ~550 lines)

**Primary Sources:**
- **Implementation:** `src/mlpy/stdlib/datetime_bridge.py` - Datetime module implementation
- **Test Suite:** `tests/ml_integration/ml_stdlib/09_datetime_objects.ml`, `10_datetime_arithmetic.ml`, `11_datetime_timezone.ml`
- **DO NOT reference old documentation** - complete rewrite required

Consult implementation and test files for complete function list including object creation, arithmetic, and timezone handling.

---

##### 1.4.5 JSON Module (COMPLETE REWRITE - ~450 lines)

**Primary Sources:**
- **Implementation:** `src/mlpy/stdlib/json_bridge.py` - JSON module implementation
- **Test Suite:** `tests/ml_integration/ml_stdlib/18_json_parse_stringify.ml`, `19_json_utilities.ml`
- **DO NOT reference old documentation** - complete rewrite required

Consult implementation and test files for complete function list including parsing, stringification, and utility functions.

---

##### 1.4.6 Collections Module (COMPLETE REWRITE - ~450 lines)

**Primary Sources:**
- **Implementation:** `src/mlpy/stdlib/collections_bridge.py` - Collections module implementation
- **Test Suite:** `tests/ml_integration/ml_stdlib/12_collections_basic.ml`, `13_collections_advanced.ml`
- **DO NOT reference old documentation** - complete rewrite required

Consult implementation and test files for complete function list including collection operations and data structures.

---

##### 1.4.7 Functional Module (COMPLETE REWRITE - ~600 lines)

**Primary Sources:**
- **Implementation:** `src/mlpy/stdlib/functional_bridge.py` - Functional programming module implementation
- **Test Suite:** `tests/ml_integration/ml_stdlib/14_functional_composition.ml`, `15_functional_advanced.ml`
- **DO NOT reference old documentation** - complete rewrite required

**Note:** This module was significantly enhanced in Phase 5 with new functions:
- `curry2()` - Curry 2-arg function
- `partition()` - Split by predicate
- `ifElse()` - Conditional application
- `cond()` - Multi-condition dispatch
- `times()` - Execute N times
- `zipWith()` - Zip with combiner
- `takeWhile()` - Take while true
- `juxt()` - Apply all functions

Consult implementation and test files for complete function list and usage patterns.

---

##### 1.4.8 Regex Module (COMPLETE REWRITE - ~550 lines)

**Primary Sources:**
- **Implementation:** `src/mlpy/stdlib/regex_bridge.py` - Regular expression module implementation
- **Test Suite:** `tests/ml_integration/ml_stdlib/06_regex_match_objects.ml`, `07_regex_flags.ml`, `08_regex_utilities.ml`
- **DO NOT reference old documentation** - complete rewrite required

**Note:** This module was enhanced with new utility methods:
- `extract_emails()` - Extract email addresses
- `extract_phone_numbers()` - Extract phone numbers
- `is_url()` - Check if valid URL
- `find_first()` - Find first match
- `remove_html_tags()` - Strip HTML tags

Consult implementation and test files for complete function list and usage patterns.

---

##### 1.4.9 Random Module (COMPLETE REWRITE - ~450 lines)

**Primary Sources:**
- **Implementation:** `src/mlpy/stdlib/random_bridge.py` - Random number generation module implementation
- **Test Suite:** `tests/ml_integration/ml_stdlib/16_random_generation.ml`, `17_random_distributions.ml`
- **DO NOT reference old documentation** - complete rewrite required

Consult implementation and test files for complete function list including basic random generation and statistical distributions.

---

##### 1.4.10 File Module (NEW - ~800 lines)

**Primary Sources:**
- **Implementation:** `src/mlpy/stdlib/file_bridge.py` - File I/O module implementation
- **Test Suite:** `tests/ml_integration/ml_stdlib/20_file_operations.ml`
- **This is a NEW module** - no old documentation exists

**Capabilities Required:** file.read, file.write, file.append, file.delete

Consult implementation and test files for complete function list including:
- Basic read/write operations
- Line-based operations
- Binary file operations
- File metadata operations
- File system operations (copy, move, delete)

---

##### 1.4.11 Path Module (NEW - ~700 lines)

**Primary Sources:**
- **Implementation:** `src/mlpy/stdlib/path_bridge.py` - Path manipulation module implementation
- **Test Suite:** `tests/ml_integration/ml_stdlib/21_path_operations.ml`
- **This is a NEW module** - no old documentation exists

**Capabilities Required:** path.read, path.write

Consult implementation and test files for complete function list including:
- Path construction and manipulation
- Path queries and checks
- Directory operations
- File system traversal
- Platform-specific utilities

---

##### 1.4.12 HTTP Module (NEW - ~650 lines)

**Primary Sources:**
- **Implementation:** `src/mlpy/stdlib/http_bridge.py` - HTTP client module implementation
- **Test Suite:** `tests/ml_integration/ml_stdlib/22_http_utilities.ml`
- **This is a NEW module** - no old documentation exists

**Capabilities Required:** network.http, network.https

Consult implementation and test files for complete function list including:
- HTTP request methods (GET, POST, PUT, DELETE, PATCH, HEAD)
- Response handling
- URL encoding/decoding
- Query string operations

---

##### 1.4.13 String Methods (DOCUMENTATION - ~400 lines)

**Note:** String is NOT an importable module. Document string methods available on string primitive values.

**Primary Sources:**
- **Implementation:** String methods are available directly on string values (no bridge module)
- **Test Suite:** Various test files demonstrating string operations
- **DO NOT reference old documentation** - complete rewrite required

Document string methods that can be called directly on string values (e.g., `"hello".toUpperCase()`).

---

##### 1.4.14 Array Methods (DOCUMENTATION - ~400 lines)

**Note:** Array is NOT an importable module. Document array methods available on array primitive values.

**Primary Sources:**
- **Implementation:** Array methods are available directly on array values (no bridge module)
- **Test Suite:** Various test files demonstrating array operations
- **DO NOT reference old documentation** - complete rewrite required

Document array methods that can be called directly on array values (e.g., `[1,2,3].length()`, array slicing, etc.).

---

#### 1.5 Understanding Capabilities - Security Guide (NEW - ~1000 lines)

**Purpose:** User-facing conceptual introduction to the capability-based security model in mlpy
**Length:** ~1000 lines
**Audience:** ML language users who need to understand and work with capabilities

**Note:** This system is not fully implemented yet and documentation will need updates as implementation progresses.

**Content Structure:**

##### Section 1: What Are Capabilities? (~150 lines)

**Conceptual Introduction:**
- Traditional security: All-or-nothing permissions (run with full access or no access)
- Capability-based security: Fine-grained, token-based permissions
- Analogy: Physical keys - each key only opens specific doors, can be revoked, can expire
- Benefits: Principle of least privilege, explicit permissions, auditability

**Why Capabilities Matter:**
- **Prevent accidental damage:** ML code can't delete files it shouldn't access
- **Security by default:** All dangerous operations require explicit permission
- **Explicit contracts:** Code declares what it needs upfront
- **Revocable access:** Permissions can be granted and revoked at runtime
- **Pattern-based restrictions:** Fine-grained control (e.g., read `/data/*` but not `/etc/*`)

**Real-World Analogy:**
```
Traditional Security:
  - Like giving someone the master key to your house
  - They can access everything or nothing
  - No audit trail of what they accessed

Capability-Based Security:
  - Like giving someone specific keys for specific rooms
  - Each key has specific permissions (read-only closet, read-write garage)
  - Keys can expire after certain time or uses
  - You can track every time a key is used
  - You can revoke keys without changing all locks
```

##### Section 2: Capability Types in mlpy (~200 lines)

**File System Capabilities:**
```ml
// File operations require capabilities
file.read       // Read file contents
file.write      // Write or create files
file.append     // Append to existing files
file.delete     // Delete files
```

**Path Manipulation Capabilities:**
```ml
path.read       // Query path information (exists, is_dir, etc.)
path.write      // Create/modify directory structures
```

**Network Capabilities:**
```ml
network.http    // Make HTTP requests
network.https   // Make HTTPS requests
```

**Console Capabilities:**
```ml
console.write   // Write to stdout
console.error   // Write to stderr
```

**Capability Hierarchy:**
- Some capabilities imply others
- `file.write` includes ability to create files
- `network.https` is more restrictive than `network.http`

**Complete Capability Reference Table:**
```rst
.. table:: mlpy Capability Types
   :widths: auto

   =====================  ========================================  ===================
   Capability Type        Purpose                                   Example Resources
   =====================  ========================================  ===================
   file.read              Read file contents                        /data/input.txt
   file.write             Create or overwrite files                 /output/result.csv
   file.append            Append to existing files                  /logs/app.log
   file.delete            Delete files                              /temp/cache.tmp
   path.read              Query path metadata                       /data/
   path.write             Create/modify directories                 /output/reports/
   network.http           HTTP requests                             http://api.example.com
   network.https          HTTPS requests (secure)                   https://api.example.com
   console.write          Standard output                           stdout
   console.error          Error output                              stderr
   crypto.hash            Cryptographic hashing                     N/A
   crypto.random          Secure random generation                  N/A
   =====================  ========================================  ===================
```

##### Section 3: Using Capabilities in ML Code (~300 lines)

**Basic Pattern - Import Requires Capability:**
```ml
// ❌ This will fail without file.read capability
import file;
content = file.read("/data/input.txt");
// Error: Missing capability 'file.read'

// ✓ Grant capability before import
// (Done via REPL .grant command or Python API)
import file;
content = file.read("/data/input.txt");  // ✓ Allowed
```

**REPL Capability Management:**
```ml
// Check current capabilities
ml[secure]> .capabilities
No capabilities granted (security-restricted mode)

// Grant capability interactively
ml[secure]> .grant file.read

⚠️  Security Warning: Granting capability 'file.read'
This will allow ML code to access restricted functionality.
Grant this capability? [y/N]: y
✓ Granted capability: file.read

// Now file operations work
ml[secure]> import file;
ml[secure]> content = file.read("/data/example.txt");
✓ Success

// Revoke when done
ml[secure]> .revoke file.read
✓ Revoked capability: file.read
```

**Resource Pattern Matching (Advanced):**
```ml
// Capability with resource pattern restriction
// (Configured from Python API, see Integration Guide)
//
// Example: file.read granted with pattern "/data/*"
//
import file;

file.read("/data/input.txt");       // ✓ Matches pattern
file.read("/data/subdir/data.csv"); // ✓ Matches pattern
file.read("/etc/passwd");           // ❌ DENIED - doesn't match pattern

// Pattern examples:
// "/data/*"           - All files in /data/ directory
// "/data/**/*.csv"    - All CSV files in /data/ and subdirectories
// "/tmp/session_*"    - All files starting with session_ in /tmp/
// "https://api.example.com/*"  - All HTTPS requests to this domain
```

**Capability-Aware Error Messages:**
```ml
ml[secure]> import file;
ml[secure]> content = file.read("/secret/password.txt");

❌ Error: Capability Required
  Operation: file.read
  Resource: /secret/password.txt
  Status: DENIED

  Reason: Missing capability 'file.read'

  To fix:
    1. Grant capability in REPL: .grant file.read
    2. OR configure capability in Python code (see Integration Guide)
    3. OR request capability in your ML module declaration

  Security Note: This file access is blocked for your protection.
  Only grant capabilities to code you trust.
```

##### Section 4: Working with Capabilities (~200 lines)

**Development Workflow:**

**Step 1: Write Code Without Capabilities**
```ml
// Start by writing your logic
function process_data(filename) {
    import file;
    content = file.read(filename);
    // ... process content ...
    return result;
}
```

**Step 2: Identify Required Capabilities**
- Run code in REPL or from file
- Note capability errors
- Understand why each capability is needed

**Step 3: Grant Capabilities (Development)**
```ml
// In REPL - temporary grant for testing
ml[secure]> .grant file.read
ml[secure]> .grant file.write
```

**Step 4: Configure Capabilities (Production)**
```python
# In Python integration code
from mlpy.runtime.capabilities.context import CapabilityContext
from mlpy.runtime.capabilities.tokens import CapabilityToken, CapabilityConstraint
from mlpy.ml.transpiler import MLTranspiler

# Create context with specific capabilities
context = CapabilityContext(name="data-processor")

# Grant file.read with pattern restriction
constraint = CapabilityConstraint(
    resource_patterns=["/data/*", "/input/*"],
    allowed_operations={"read"}
)
token = CapabilityToken(
    capability_type="file.read",
    constraints=constraint,
    description="Read data files only"
)
context.add_capability(token)

# Execute ML code with capabilities
transpiler = MLTranspiler()
result, issues = transpiler.execute_with_sandbox(
    ml_code,
    context=context
)
```

**Best Practices:**
- ✅ **Principle of Least Privilege:** Only grant capabilities your code actually needs
- ✅ **Use Resource Patterns:** Restrict capabilities to specific files/URLs
- ✅ **Revoke After Use:** Remove capabilities when no longer needed
- ✅ **Audit Capability Usage:** Review what capabilities your code requests
- ❌ **Don't Grant Broad Access:** Avoid patterns like `"/*"` or `"*"`
- ❌ **Don't Grant Permanent Capabilities:** Use expiration for sensitive operations

##### Section 5: Common Capability Patterns (~150 lines)

**Pattern 1: Read-Only Data Access**
```ml
// Task: Read configuration file
// Capabilities needed: file.read
// Resource pattern: /config/app.conf

import file;
config = file.read("/config/app.conf");
```

**Pattern 2: Data Processing Pipeline**
```ml
// Task: Read input, process, write output
// Capabilities needed: file.read, file.write
// Resource patterns: /input/*, /output/*

import file;

function process_file(input_path, output_path) {
    // Read (requires file.read on input_path)
    data = file.read(input_path);

    // Process data
    result = transform(data);

    // Write (requires file.write on output_path)
    file.write(output_path, result);
}
```

**Pattern 3: API Integration**
```ml
// Task: Fetch data from external API
// Capabilities needed: network.https
// Resource pattern: https://api.example.com/*

import http;

function fetch_user_data(user_id) {
    url = "https://api.example.com/users/" + str(user_id);
    response = http.get(url);
    return response.json();
}
```

**Pattern 4: Logging**
```ml
// Task: Append to log file
// Capabilities needed: file.append
// Resource pattern: /logs/app.log

import file;

function log_message(message) {
    import datetime;
    timestamp = datetime.now().isoformat();
    entry = timestamp + " - " + message + "\n";
    file.append("/logs/app.log", entry);
}
```

**Pattern 5: Mixed Capabilities**
```ml
// Task: Download data and save locally
// Capabilities needed: network.https, file.write
// Resource patterns: https://data.example.com/*, /downloads/*

import http;
import file;

function download_dataset(url, local_path) {
    // Fetch from network (requires network.https)
    response = http.get(url);

    // Save locally (requires file.write)
    file.write(local_path, response.text());

    print("Downloaded to " + local_path);
}
```

---

#### 1.6 Working with the Transpiler (~800 lines)

**Purpose:** Introduce the transpilation concept and explain how to compile ML code to Python
**Length:** ~800 lines
**Audience:** ML developers who need to understand compilation and code generation

**Content Structure:**

##### Section 1: What is Transpilation? (~150 lines)

**Conceptual Introduction:**
- **Compilation vs. Transpilation:** ML code → Python code (source-to-source)
- **Why Transpile:** Execute ML on Python runtime, leverage Python ecosystem
- **The ML Compilation Pipeline:** Parse → Analyze → Optimize → Generate Python
- **Output Artifacts:** Python code, source maps, module caches

**Transpilation Workflow:**
```
ML Source Code (.ml)
   ↓
Parse & Validate
   ↓
Security Analysis
   ↓
Code Optimization
   ↓
Python Generation
   ↓
Python Code (.py) + Source Maps + Caches
```

**When to Transpile:**
- **Development:** Use REPL for quick experimentation
- **Production:** Transpile to Python for deployment
- **Integration:** Generate Python for embedding in Python applications
- **Distribution:** Ship transpiled Python code to users

##### Section 2: Basic Transpilation (~200 lines)

**Simple Transpilation:**
```bash
# Transpile single file
mlpy transpile hello.ml

# Output: hello.py (generated Python code)
```

**Specifying Output:**
```bash
# Custom output file
mlpy transpile src/main.ml -o dist/app.py

# Custom output directory
mlpy transpile src/ -o dist/
```

**Transpilation Options:**
```bash
# With source maps (for debugging)
mlpy transpile code.ml --source-maps

# With optimization
mlpy transpile code.ml -O 2

# With strict security
mlpy transpile code.ml --security-level strict
```

**Example ML Code:**
```ml
// hello.ml
function greet(name) {
    return "Hello, " + name + "!";
}

print(greet("World"));
```

**Generated Python Code:**
```python
# hello.py (transpiled from hello.ml)

def greet(name):
    return "Hello, " + name + "!"

print(greet("World"))
```

##### Section 3: Emit Code Modes (~250 lines)

**Understanding Emit Modes:**

mlpy supports three code emission modes that control how modules and imports are handled:

**Mode 1: Silent (`--emit-code silent`)**
- **Purpose:** Validate compilation without generating files
- **Use Case:** CI/CD validation, syntax checking
- **Behavior:** Transpiles code, validates, but writes nothing to disk
- **Module Handling:** All modules inlined in memory

```bash
# Validate without file output
mlpy transpile code.ml --emit-code silent

# Output:
# [OK] Compiled code.ml (silent mode - no files written)
```

**Mode 2: Single-File (`--emit-code single-file`)**
- **Purpose:** Generate one standalone Python file
- **Use Case:** Simple deployment, embedding, single-script distribution
- **Behavior:** All code (including modules) inlined into one `.py` file
- **Module Handling:** User modules embedded directly in output

```bash
# Generate single Python file
mlpy transpile app.ml --emit-code single-file -o dist/app.py

# Output: dist/app.py (all code in one file)
```

**Single-File Example:**
```ml
// app.ml
import mylib;

result = mylib.process_data([1, 2, 3]);
print(result);
```

```ml
// mylib.ml
export function process_data(arr) {
    return arr.map(function(x) { return x * 2; });
}
```

**Generated app.py (single-file mode):**
```python
# app.py - Generated from app.ml (single-file mode)

# === Inlined Module: mylib ===
class MyLibModule:
    @staticmethod
    def process_data(arr):
        return [x * 2 for x in arr]

mylib = MyLibModule()

# === Main Code ===
result = mylib.process_data([1, 2, 3])
print(result)
```

**Mode 3: Multi-File (`--emit-code multi-file`) [DEFAULT]**
- **Purpose:** Generate separate files with module caching
- **Use Case:** Development, large projects, module reuse
- **Behavior:** Main file + separate `.py` files for each user module
- **Module Handling:** Modules cached as separate files, imported normally

```bash
# Generate multiple Python files (default)
mlpy transpile app.ml --emit-code multi-file

# or simply:
mlpy transpile app.ml

# Output:
# - app.py (main file)
# - mylib.py (cached module)
```

**Multi-File Example:**
```python
# app.py - Generated from app.ml (multi-file mode)
import mylib  # Imports cached mylib.py

result = mylib.process_data([1, 2, 3])
print(result)
```

```python
# mylib.py - Generated from mylib.ml (cached module)
def process_data(arr):
    return [x * 2 for x in arr]
```

**Comparison Table:**
```rst
.. table:: Emit Code Modes Comparison
   :widths: auto

   ==============  ==============  =================  ==================  ================
   Mode            Files Created   Module Handling    Use Case            Performance
   ==============  ==============  =================  ==================  ================
   silent          None            Inlined (memory)   Validation/Testing  Fastest
   single-file     One .py         Embedded inline    Simple deployment   Fast
   multi-file      Multiple .py    Separate files     Development/Large   Cache benefits
   ==============  ==============  =================  ==================  ================
```

##### Section 4: Source Maps (~100 lines)

**What are Source Maps?**
- Map generated Python code back to original ML source
- Enable debugging in ML context
- Support IDE integration
- Track line/column mapping

**Generating Source Maps:**
```bash
# Generate source map
mlpy transpile code.ml --source-maps

# Output:
# - code.py (Python code)
# - code.py.map (source map)
```

**Source Map Structure:**
```json
{
  "version": 3,
  "file": "code.py",
  "sourceRoot": "",
  "sources": ["code.ml"],
  "names": [],
  "mappings": "AAAA;AACA;AACA..."
}
```

**Using Source Maps:**
- IDEs can show ML source when debugging Python
- Error messages show ML line numbers
- Profiling tools can attribute to ML source

##### Section 5: Advanced Transpilation (~100 lines)

**Security Levels:**
```bash
# Strict security (default) - fail on any security issue
mlpy transpile code.ml --security-level strict

# Normal security - warn on medium issues
mlpy transpile code.ml --security-level normal

# Permissive security - only block critical issues
mlpy transpile code.ml --security-level permissive
```

**Optimization Levels:**
```bash
# No optimization (fastest compilation)
mlpy transpile code.ml -O 0

# Basic optimization (default)
mlpy transpile code.ml -O 1

# Advanced optimization
mlpy transpile code.ml -O 2

# Aggressive optimization
mlpy transpile code.ml -O 3
```

**Capability Declaration:**
```bash
# Declare required capabilities
mlpy transpile app.ml --capabilities "file.read,file.write,network.https"
```

**Batch Transpilation:**
```bash
# Transpile entire directory
mlpy transpile src/ -o dist/

# Transpile with pattern
mlpy transpile "src/**/*.ml" -o dist/
```

---

#### 1.7 Project Setup and Organization (~900 lines)

**Purpose:** Guide ML developers on creating, structuring, and managing ML projects
**Length:** ~900 lines
**Audience:** ML developers building applications and libraries

**Content Structure:**

##### Section 1: Creating a New Project (~200 lines)

**Using `mlpy init`:**
```bash
# Create new project
mlpy --init my-project

# Create with specific template
mlpy --init my-web-app --template web

# Create in specific directory
mlpy --init my-lib --template library --dir ~/projects/
```

**Project Templates:**

**1. Basic Template (default):**
```
my-project/
├── mlpy.json              # Project configuration
├── README.md              # Project documentation
├── src/
│   └── main.ml            # Entry point
├── tests/
│   └── test_main.ml       # Test files
└── .gitignore             # Git ignore patterns
```

**2. Web Template:**
```
my-web-app/
├── mlpy.json
├── src/
│   ├── routes/            # Web routes
│   ├── models/            # Data models
│   ├── views/             # View templates
│   └── main.ml            # Application entry
├── public/                # Static files
├── tests/
└── README.md
```

**3. CLI Template:**
```
my-cli-tool/
├── mlpy.json
├── src/
│   ├── commands/          # CLI commands
│   ├── utils/             # Utilities
│   └── main.ml            # CLI entry point
├── tests/
└── README.md
```

**4. Library Template:**
```
my-lib/
├── mlpy.json
├── src/
│   ├── lib.ml             # Library exports
│   └── internal/          # Internal modules
├── tests/
├── docs/                  # Library documentation
├── examples/              # Usage examples
└── README.md
```

##### Section 2: Project Configuration (~200 lines)

**mlpy.json Configuration:**
```json
{
  "name": "my-project",
  "version": "1.0.0",
  "description": "My ML project",
  "author": "Your Name",
  "license": "MIT",

  "main": "src/main.ml",
  "source": "src/",
  "output": "dist/",

  "compile": {
    "emit": "multi-file",
    "sourceMaps": true,
    "optimization": 1,
    "security": "strict"
  },

  "capabilities": [
    "file.read:/data/*",
    "file.write:/output/*",
    "network.https:https://api.example.com/*"
  ],

  "imports": {
    "paths": ["src/lib/", "src/modules/"],
    "allowCurrentDir": true
  },

  "tests": {
    "directory": "tests/",
    "pattern": "**/*.ml"
  },

  "scripts": {
    "build": "mlpy transpile src/main.ml -o dist/app.py",
    "test": "mlpy test",
    "dev": "mlpy run src/main.ml --watch"
  }
}
```

**Configuration Fields:**

**Project Metadata:**
- `name`: Project identifier
- `version`: Semantic version
- `description`: Project description
- `author`: Author name/email
- `license`: License type

**Build Settings:**
- `main`: Entry point file
- `source`: Source directory
- `output`: Build output directory
- `compile.emit`: Emit code mode
- `compile.sourceMaps`: Generate source maps
- `compile.optimization`: Optimization level (0-3)
- `compile.security`: Security level

**Capabilities:**
- List of required capabilities with patterns
- Format: `"type:pattern"`
- Example: `"file.read:/data/*"`

**Import Configuration:**
- `imports.paths`: Module search paths
- `imports.allowCurrentDir`: Allow current directory imports

**Testing:**
- `tests.directory`: Test directory location
- `tests.pattern`: Test file pattern

##### Section 3: Code Organization (~250 lines)

**Directory Structure Best Practices:**

**Small Project:**
```
my-app/
├── mlpy.json
├── src/
│   ├── main.ml            # Entry point
│   ├── utils.ml           # Utilities
│   └── config.ml          # Configuration
└── tests/
    └── test_main.ml
```

**Medium Project:**
```
my-app/
├── mlpy.json
├── src/
│   ├── main.ml
│   ├── core/              # Core business logic
│   │   ├── processor.ml
│   │   └── validator.ml
│   ├── utils/             # Utilities
│   │   ├── string_utils.ml
│   │   └── math_utils.ml
│   └── models/            # Data models
│       ├── user.ml
│       └── product.ml
├── tests/
│   ├── core/
│   └── utils/
└── README.md
```

**Large Project:**
```
my-app/
├── mlpy.json
├── src/
│   ├── main.ml
│   ├── app/               # Application code
│   │   ├── controllers/
│   │   ├── services/
│   │   └── middleware/
│   ├── domain/            # Business domain
│   │   ├── models/
│   │   ├── repositories/
│   │   └── validators/
│   ├── infrastructure/    # Infrastructure
│   │   ├── database/
│   │   ├── cache/
│   │   └── logging/
│   └── shared/            # Shared utilities
│       ├── utils/
│       ├── constants/
│       └── types/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docs/
└── examples/
```

##### Section 4: Creating Libraries (~250 lines)

**Library Structure:**
```
my-lib/
├── mlpy.json
├── src/
│   ├── lib.ml             # Public API
│   ├── core/              # Core functionality
│   │   ├── algorithm.ml
│   │   └── processor.ml
│   └── internal/          # Internal (not exported)
│       └── helpers.ml
├── tests/
├── examples/
│   ├── basic_usage.ml
│   └── advanced_usage.ml
└── README.md
```

**Library Entry Point (`src/lib.ml`):**
```ml
// lib.ml - Public API for my-lib

// Import internal modules
import core.algorithm;
import core.processor;

// Export public functions
export function process(data) {
    return processor.run(data);
}

export function analyze(data) {
    return algorithm.analyze(data);
}

// Export constants
export PI = 3.14159;
export VERSION = "1.0.0";
```

**Using Your Library:**
```ml
// app.ml
import mylib;

result = mylib.process([1, 2, 3]);
print(mylib.VERSION);
```

**Publishing Libraries:**
```bash
# Build library for distribution
mlpy transpile src/lib.ml -o dist/mylib.py --emit-code single-file

# Package structure
dist/
├── mylib.py           # Transpiled library
├── README.md
└── examples/
```

---

#### 1.8 CLI Reference - Complete Command Reference (~1500 lines)

**Purpose:** Exhaustive reference for all mlpy CLI commands
**Length:** ~1500 lines
**Audience:** All ML developers using mlpy tooling

**Content Structure:**

##### Section 1: Global Options (~150 lines)

**Usage:**
```bash
mlpy [OPTIONS] COMMAND [ARGS]...
```

**Global Options:**

**`--version, -v`**
- Show mlpy version and exit
- Example: `mlpy --version`

**`--status, -s`**
- Show development status and component success rates
- Example: `mlpy --status`

**`--verbose`**
- Enable verbose output for debugging
- Example: `mlpy --verbose transpile code.ml`

**`--help`**
- Show help message and exit
- Example: `mlpy --help`

**Special Flags:**

**`--init PROJECT_NAME`**
- Initialize new ML project
- Example: `mlpy --init my-project`

**`--lsp`**
- Start Language Server Protocol server for IDE integration
- Example: `mlpy --lsp`

**`--serve-docs`**
- Serve documentation locally on HTTP server
- Example: `mlpy --serve-docs`

##### Section 2: Core Commands (~600 lines)

**`mlpy transpile` - Transpile ML to Python**

**Synopsis:**
```bash
mlpy transpile SOURCE [OPTIONS]
```

**Description:**
Transpile ML source files to Python with security analysis, optimization, and source map generation.

**Arguments:**
- `SOURCE`: Source file or directory to compile

**Options:**
- `-o, --output FILE`: Output file or directory
- `-O, --optimize LEVEL`: Optimization level (0-3, default: 1)
  - `0`: No optimization (fastest compilation)
  - `1`: Basic optimization (default)
  - `2`: Advanced optimization
  - `3`: Aggressive optimization
- `--source-maps`: Generate source maps for debugging
- `--security-level LEVEL`: Security analysis level
  - `strict`: Fail on any security issue (default)
  - `normal`: Warn on medium issues
  - `permissive`: Only block critical issues
- `--capabilities CAPS`: Required capabilities (comma-separated)
- `--emit-code MODE`: Code emission mode
  - `silent`: No files written (validation only)
  - `single-file`: One Python file with inlined modules
  - `multi-file`: Separate Python files with module caching (default)

**Examples:**
```bash
# Basic transpilation
mlpy transpile main.ml

# Custom output with source maps
mlpy transpile src/app.ml -o dist/app.py --source-maps

# Single-file mode
mlpy transpile app.ml --emit-code single-file -o dist/app.py

# With optimization and capabilities
mlpy transpile app.ml -O 2 --capabilities "file.read,network.https"

# Strict security with multi-file mode
mlpy transpile src/main.ml --security-level strict --emit-code multi-file
```

**`mlpy run` - Execute ML Programs**

**Synopsis:**
```bash
mlpy run SOURCE [ARGS] [OPTIONS]
```

**Description:**
Compile and execute ML programs in a secure sandbox environment with resource limits and capability management.

**Arguments:**
- `SOURCE`: ML source file to execute
- `ARGS`: Arguments to pass to the ML program (optional)

**Options:**
- `--sandbox / --no-sandbox`: Run in sandbox (default: enabled)
- `--timeout SECONDS`: Execution timeout in seconds (default: 30)
- `--memory-limit MB`: Memory limit in megabytes (default: 100)
- `--no-network`: Disable network access
- `--emit-code MODE`: Code emission mode
  - `silent`: No files, inline execution (default for run)
  - `single-file`: Generate one Python file
  - `multi-file`: Generate separate files with caching

**Examples:**
```bash
# Run ML program
mlpy run app.ml

# Run with arguments
mlpy run script.ml arg1 arg2 arg3

# Run with resource limits
mlpy run app.ml --timeout 60 --memory-limit 200

# Run without network access
mlpy run app.ml --no-network

# Run with multi-file caching
mlpy run app.ml --emit-code multi-file
```

**`mlpy audit` - Security Audit**

**Synopsis:**
```bash
mlpy audit SOURCE [OPTIONS]
```

**Description:**
Run comprehensive security audit on ML source code with pattern detection, data flow analysis, and CWE mapping.

**Arguments:**
- `SOURCE`: Source file or directory to audit

**Options:**
- `--deep-analysis`: Enable deep security analysis (slower, more thorough)
- `--json`: Output results in JSON format
- `--report FILE`: Save audit report to file

**Examples:**
```bash
# Basic security audit
mlpy audit code.ml

# Deep analysis with JSON output
mlpy audit src/ --deep-analysis --json

# Generate audit report
mlpy audit app.ml --deep-analysis --report security-report.json
```

**`mlpy repl` - Interactive REPL**

**Synopsis:**
```bash
mlpy repl [OPTIONS]
```

**Description:**
Start interactive ML REPL shell with command history, auto-completion, and capability management.

**Options:**
- `--no-history`: Disable command history
- `--no-color`: Disable syntax highlighting

**REPL Commands:**
- `.help`: Show REPL commands
- `.exit, .quit`: Exit REPL
- `.vars`: Show defined variables
- `.clear`: Clear variables
- `.history`: Show command history
- `.capabilities`: Show granted capabilities
- `.grant <cap>`: Grant capability
- `.revoke <cap>`: Revoke capability
- `.retry`: Retry last failed command
- `.edit`: Edit last statement in external editor

**Examples:**
```bash
# Start REPL
mlpy repl

# Start without history
mlpy repl --no-history
```

##### Section 3: Analysis & Testing Commands (~300 lines)

**`mlpy parse` - Parse and Show AST**

**Synopsis:**
```bash
mlpy parse SOURCE [OPTIONS]
```

**Description:**
Parse ML source code and display the Abstract Syntax Tree for debugging and analysis.

**Arguments:**
- `SOURCE`: Source file to parse

**Options:**
- `--json`: Output AST in JSON format
- `--verbose`: Show detailed AST information

**Examples:**
```bash
# Parse and show AST
mlpy parse code.ml

# Output as JSON
mlpy parse code.ml --json > ast.json
```

**`mlpy security-analyze` - Advanced Security Analysis**

**Synopsis:**
```bash
mlpy security-analyze SOURCE [OPTIONS]
```

**Description:**
Run comprehensive Phase 1 security analysis with pattern detection, data flow tracking, and parallel processing.

**Arguments:**
- `SOURCE`: Source file to analyze

**Options:**
- `--deep-analysis`: Enable deep security analysis
- `--parallel`: Use parallel analysis (default: enabled)
- `--json`: Output in JSON format

**Examples:**
```bash
# Run security analysis
mlpy security-analyze code.ml

# Deep analysis with parallel processing
mlpy security-analyze app.ml --deep-analysis --parallel
```

**`mlpy test` - Run Tests**

**Synopsis:**
```bash
mlpy test [PATTERN] [OPTIONS]
```

**Description:**
Run ML project tests with pattern matching and reporting.

**Arguments:**
- `PATTERN`: Test file pattern (default: `tests/**/*.ml`)

**Options:**
- `--verbose`: Verbose test output
- `--coverage`: Generate coverage report
- `--parallel`: Run tests in parallel

**Examples:**
```bash
# Run all tests
mlpy test

# Run specific tests
mlpy test "tests/unit/*.ml"

# Run with coverage
mlpy test --coverage --verbose
```

##### Section 4: Development Tools (~300 lines)

**`mlpy cache` - Manage Caches**

**Synopsis:**
```bash
mlpy cache SUBCOMMAND [OPTIONS]
```

**Subcommands:**
- `--clear-cache`: Clear all execution caches
- `--show-stats`: Show cache statistics
- `--list`: List cached items

**Examples:**
```bash
# Clear all caches
mlpy cache --clear-cache

# Show cache statistics
mlpy cache --show-stats
```

**`mlpy profiling` - Manage Profiling**

**Synopsis:**
```bash
mlpy profiling SUBCOMMAND
```

**Subcommands:**
- `enable`: Enable profiling
- `disable`: Disable profiling
- `status`: Show profiling status

**Examples:**
```bash
# Enable profiling
mlpy profiling enable

# Check status
mlpy profiling status
```

**`mlpy profile-report` - Generate Profile Report**

**Synopsis:**
```bash
mlpy profile-report [OPTIONS]
```

**Description:**
Generate comprehensive profiling report with execution times, memory usage, and performance metrics.

**Options:**
- `--format FORMAT`: Output format (text, json, html)
- `--output FILE`: Save report to file

**Examples:**
```bash
# Generate text report
mlpy profile-report

# Generate HTML report
mlpy profile-report --format html --output report.html
```

**`mlpy clear-profiles` - Clear Profiling Data**

**Synopsis:**
```bash
mlpy clear-profiles
```

**Description:**
Clear all stored profiling data and reset performance metrics.

**Examples:**
```bash
# Clear all profiling data
mlpy clear-profiles
```

##### Section 5: Advanced Features (~150 lines)

**`mlpy demo-errors` - Demonstrate Error System**

**Synopsis:**
```bash
mlpy demo-errors
```

**Description:**
Demonstrate the rich error system with example errors, CWE mapping, and source highlighting.

**Examples:**
```bash
# Show error system demo
mlpy demo-errors
```

**Exit Codes:**
- `0`: Success
- `1`: General error
- `2`: Parse error
- `3`: Security error
- `4`: Execution error
- `130`: Interrupted by user (Ctrl+C)

**Environment Variables:**
- `MLPY_CONFIG`: Path to mlpy configuration file
- `MLPY_CACHE_DIR`: Cache directory location
- `MLPY_PROFILE_DIR`: Profiling data directory
- `EDITOR`: External editor for `.edit` REPL command

**Configuration Files:**
- `mlpy.json`: Project configuration (JSON format)
- `mlpy.yaml`: Project configuration (YAML format - alternative)
- `.mlpyrc`: User-level configuration

---

#### 1.9 Debugging and Profiling ML Code (~1200 lines)

**Purpose:** Guide ML developers on debugging, profiling, and optimizing ML programs
**Length:** ~1200 lines
**Audience:** ML developers who need to debug and optimize their code

**Note:** This system is partially implemented. Source maps and basic profiling are available, but advanced debugging features and IDE integration are still in development. This documentation will be updated as features become available.

**Content Structure:**

##### Section 1: Debugging ML Code (~300 lines)

**Current Implementation Status:**
- ✅ Source maps generation available
- ✅ Rich error messages with CWE mapping
- ✅ Stack traces with line numbers
- 🔄 IDE debugger integration (in development)
- 🔄 Breakpoint support (planned)
- 🔄 Variable inspection (planned)

**Using Source Maps for Debugging:**

Source maps allow you to debug transpiled Python code while viewing the original ML source.

```bash
# Generate source maps during transpilation
mlpy transpile app.ml --source-maps

# Output:
# - app.py (Python code)
# - app.py.map (source map file)
```

**Source Map Benefits:**
- Error messages show ML line numbers instead of Python
- Stack traces reference ML source files
- IDEs can display ML code during Python debugging
- Profiling tools attribute performance to ML source

**Reading Error Messages:**

```ml
// error.ml
function divide(a, b) {
    return a / b;  // Line 2
}

result = divide(10, 0);  // Line 5 - Division by zero
```

**Error Output (with source maps):**
```
❌ Runtime Error: Division by zero
   File: error.ml
   Line: 2, Column: 12

   1 | function divide(a, b) {
   2 |     return a / b;  // Line 2
                    ^^^
   3 | }

   Called from:
   Line: 5, Column: 10
   5 | result = divide(10, 0);
              ^^^^^^^^^^^^^^^

Suggestions:
  - Check for zero divisor before division
  - Use conditional logic: if (b != 0) { ... }
  - Add input validation to your function
```

**REPL Debugging:**

The REPL provides immediate feedback for debugging:

```ml
ml[secure]> x = 10;
✓ x = 10

ml[secure]> y = 0;
✓ y = 0

ml[secure]> result = x / y;
❌ Error: Division by zero
   Line: 1, Column: 10

ml[secure]> .retry
# Edit the last command
ml[secure]> result = if (y != 0) { x / y } else { 0 };
✓ result = 0
```

**Debug Workflow:**
1. **Write code in REPL** - Test small pieces interactively
2. **Check variables** - Use `.vars` to inspect state
3. **Reproduce errors** - Isolate problematic code
4. **Use `.retry`** - Fix and re-execute failed statements
5. **Move to files** - Once working, save to .ml files

##### Section 2: Source Map Integration (CURRENT) (~200 lines)

**How Source Maps Work:**

```
ML Source (app.ml)          Python Output (app.py)
Line 1: function add(a,b)   Line 3: def add(a, b):
Line 2:   return a + b;     Line 4:     return a + b
Line 3:                     Line 5:
Line 4: print(add(5, 3));   Line 6: print(add(5, 3))

Source Map (app.py.map)
Mappings: 3→1, 4→2, 6→4
```

**Source Map Format:**
```json
{
  "version": 3,
  "file": "app.py",
  "sourceRoot": "",
  "sources": ["app.ml"],
  "names": [],
  "mappings": "AAAA;AACA;AACA;AADA",
  "sourcesContent": ["function add(a,b) {\n  return a + b;\n}\nprint(add(5, 3));"]
}
```

**Using Source Maps with Python Debuggers:**

```python
# Install source map support (future feature)
pip install mlpy-debug-tools

# Run with debugger
python -m mlpy.debug app.py

# Debugger shows ML source instead of Python
# Breakpoints set on ML lines
# Variable names match ML code
```

**IDE Integration (Planned):**
- VS Code: ML source view during debugging
- PyCharm: Source map plugin (in development)
- Other IDEs: Generic source map support

##### Section 3: Profiling ML Code (CURRENT) (~300 lines)

**Current Implementation Status:**
- ✅ Basic profiling with `@profile_parser` and `@profile_security`
- ✅ Execution time tracking
- ✅ Profile reports generation
- 🔄 Memory profiling (basic implementation)
- 🔄 Function-level profiling (planned)
- 🔄 Line-by-line profiling (planned)

**Enabling Profiling:**

```bash
# Enable profiling for all operations
mlpy profiling enable

# Run your code
mlpy run app.ml

# Profiling data is collected automatically

# Generate report
mlpy profile-report
```

**Profile Report Output:**
```
╭─────────────────────────────────────────────────────────╮
│ mlpy Profiling Report                                   │
│ Generated: 2025-10-07 14:32:15                         │
╰─────────────────────────────────────────────────────────╯

Parsing Performance:
  - Total parse time: 45.23ms
  - Average per file: 5.6ms
  - Files parsed: 8

Security Analysis Performance:
  - Total analysis time: 142.5ms
  - Average per file: 17.8ms
  - Deep analysis enabled: Yes
  - Threats detected: 0

Code Generation Performance:
  - Total generation time: 234.1ms
  - Average per file: 29.3ms
  - Optimization level: 1

Execution Performance:
  - Total runtime: 1.23s
  - User CPU time: 0.95s
  - System CPU time: 0.28s
  - Peak memory: 45.6 MB
```

**Performance Profiling in Code (Planned):**

```ml
// Future: Built-in profiling decorators
@profile
function expensive_operation(data) {
    result = process_data(data);
    return result;
}

@profile_memory
function memory_intensive(large_array) {
    return transform(large_array);
}

// Profiling data collected automatically
```

**Manual Performance Measurement:**

```ml
// Current approach using datetime module
import datetime;

start_time = datetime.now();

// Your code here
result = expensive_computation();

end_time = datetime.now();
duration = end_time.timestamp() - start_time.timestamp();

print("Execution time: " + str(duration) + "s");
```

##### Section 4: Performance Optimization (~250 lines)

**Profiling-Driven Optimization:**

**Step 1: Identify Bottlenecks**
```bash
# Run with profiling
mlpy profiling enable
mlpy run app.ml
mlpy profile-report --format html --output profile.html
```

**Step 2: Analyze Report**
- Look for slow functions
- Identify memory-intensive operations
- Find repeated computations

**Step 3: Optimize Code**
```ml
// Before: Repeated computation
function process_items(items) {
    result = [];
    for (item in items) {
        // Expensive computation called many times
        value = expensive_transform(item);
        result.push(value);
    }
    return result;
}

// After: Use functional programming (more efficient)
import functional;

function process_items(items) {
    return functional.map(items, expensive_transform);
}
```

**Common Optimization Patterns:**

**Pattern 1: Memoization (Caching Results)**
```ml
// Cache expensive computations
cache = {};

function fibonacci(n) {
    if (n <= 1) return n;

    // Check cache
    cache_key = "fib_" + str(n);
    if (cache.hasKey(cache_key)) {
        return cache[cache_key];
    }

    // Compute and cache
    result = fibonacci(n - 1) + fibonacci(n - 2);
    cache[cache_key] = result;
    return result;
}
```

**Pattern 2: Avoid Repeated Lookups**
```ml
// Before: Repeated array access
function sum_nested(data) {
    total = 0;
    for (i in range(data.length())) {
        total = total + data[i].value;  // Repeated lookup
    }
    return total;
}

// After: Cache references
function sum_nested(data) {
    total = 0;
    for (item in data) {
        total = total + item.value;  // Direct reference
    }
    return total;
}
```

**Pattern 3: Lazy Evaluation (Future)**
```ml
// Planned: Lazy sequences for large datasets
// Process only what's needed
import collections;

function process_large_file(filepath) {
    // Don't load entire file into memory
    lines = collections.lazyRead(filepath);

    // Process line by line
    for (line in lines) {
        if (matches_criteria(line)) {
            process(line);
        }
    }
}
```

##### Section 5: Memory Profiling (PLANNED) (~200 lines)

**Note:** Advanced memory profiling is not yet implemented. Basic memory limits are available via sandbox configuration.

**Current Memory Management:**

```bash
# Run with memory limit
mlpy run app.ml --memory-limit 200  # 200 MB limit

# Program will be terminated if it exceeds limit
```

**Planned Memory Profiling Features:**

**Feature 1: Memory Snapshots**
```ml
// Future: Take memory snapshots
import profiling;

profiling.snapshot("before");

// Allocate memory
large_data = create_large_structure();

profiling.snapshot("after");

// Compare snapshots
diff = profiling.compare("before", "after");
print("Memory increased by: " + str(diff.delta) + " MB");
```

**Feature 2: Memory Leak Detection**
```bash
# Future: Detect memory leaks
mlpy run app.ml --detect-leaks

# Output:
# ⚠️  Potential memory leak detected:
#    Function: process_loop (line 45)
#    Growing object: cache (line 12)
#    Suggestion: Implement cache eviction policy
```

**Feature 3: Object Allocation Tracking**
```ml
// Future: Track object allocations
@track_allocations
function process_data(items) {
    results = [];
    for (item in items) {
        results.push(transform(item));
    }
    return results;
}

// Report shows:
// - Number of objects allocated
// - Total memory used
// - Object lifetimes
```

**Memory Optimization Tips:**

**Tip 1: Reuse Objects**
```ml
// Instead of creating new arrays
function filter_data(items) {
    result = [];  // New allocation
    for (item in items) {
        if (condition(item)) {
            result.push(item);
        }
    }
    return result;
}

// Consider using functional programming (may be more efficient)
import functional;
filtered = functional.filter(items, condition);
```

**Tip 2: Clear Unused Data**
```ml
// Clear large objects when done
large_cache = {};

// Use the cache
process_with_cache(large_cache);

// Clear when done
large_cache = {};  // Allow garbage collection
```

##### Section 6: Debugging Tools Reference (CURRENT & PLANNED) (~150 lines)

**Available Now:**

**REPL Debugging Commands:**
- `.vars` - Show all defined variables and their values
- `.history` - Show command history for debugging session
- `.retry` - Retry the last failed command with edits
- `.edit` - Edit last statement in external editor
- `.clear` - Clear all variables and start fresh

**CLI Debugging Tools:**
- `mlpy parse code.ml` - Show AST for debugging parsing issues
- `mlpy audit code.ml` - Security analysis with detailed warnings
- `mlpy transpile code.ml --source-maps` - Generate debugging source maps

**Error System:**
- Rich error messages with context
- CWE (Common Weakness Enumeration) mapping
- Actionable suggestions for fixes
- Source highlighting at error location

**Planned Features:**

**Interactive Debugger:**
```bash
# Future: ML debugger
mlpy debug app.ml

# Debugger commands:
(mldb) break 15          # Set breakpoint at line 15
(mldb) run               # Run until breakpoint
(mldb) step              # Step to next line
(mldb) next              # Step over function call
(mldb) print x           # Print variable value
(mldb) watch x           # Watch variable for changes
(mldb) continue          # Continue execution
```

**Watch Expressions:**
```ml
// Future: Watch variables during execution
@watch(x, y, result)
function complex_calculation(a, b) {
    x = transform_a(a);
    y = transform_b(b);
    result = combine(x, y);
    return result;
}

// Debugger shows x, y, result at each step
```

**Conditional Breakpoints:**
```ml
// Future: Break when condition is true
function process_loop(items) {
    for (item in items) {
        result = process(item);
        @breakpoint_if(result < 0)  // Break if negative
        store(result);
    }
}
```

**Best Practices for Debugging:**

1. **Use REPL for Quick Tests**
   - Test functions interactively
   - Verify assumptions immediately
   - Build complex logic incrementally

2. **Enable Source Maps**
   - Always generate source maps for production code
   - Keep .ml files alongside .py files
   - Use consistent file paths

3. **Add Logging**
   ```ml
   import console;

   function debug_function(x) {
       console.log("Input: " + str(x));
       result = process(x);
       console.log("Output: " + str(result));
       return result;
   }
   ```

4. **Use Assertions (Planned)**
   ```ml
   // Future: Built-in assertions
   function divide(a, b) {
       assert(b != 0, "Divisor cannot be zero");
       return a / b;
   }
   ```

5. **Profile Before Optimizing**
   - Don't guess where slowdowns are
   - Measure first, then optimize
   - Verify optimizations with profiling

---

### TIER 2: Integration Guide

#### 2.1 Writing Standard Library Modules (COMPLETE REWRITE - ~1200 lines)

**Current Issue:** Documentation shows OLD pattern (manual classes without decorators)

**New Content Structure:**

1. **Overview** - Decorator-based module system
2. **Quick Start** - Minimal working module example
3. **Module Decorator (@ml_module)** - Complete reference
4. **Function Decorator (@ml_function)** - Complete reference
5. **Class Decorator (@ml_class)** - Complete reference
6. **Capability Integration** - Security patterns
7. **Complete Example** - Crypto module (from Developer Guide)
8. **Testing Your Module** - Unit and integration tests
9. **Best Practices** - Patterns and anti-patterns

**Complete Crypto Module Example:**
```python
"""Cryptography module for ML with capability-based security."""

import hashlib
import hmac
import secrets
from typing import Any

from mlpy.stdlib.decorators import ml_module, ml_function, ml_class


@ml_class(description="Cryptographic hash result")
class HashResult:
    """Result of a cryptographic hash operation."""

    def __init__(self, algorithm: str, digest_hex: str, digest_bytes: bytes):
        self._algorithm = algorithm
        self._digest_hex = digest_hex
        self._digest_bytes = digest_bytes

    @ml_function(description="Get hash algorithm name")
    def algorithm(self) -> str:
        """Get the name of the hash algorithm used."""
        return self._algorithm

    @ml_function(description="Get hash as hexadecimal string")
    def hex(self) -> str:
        """Get the hash digest as a hexadecimal string."""
        return self._digest_hex

    @ml_function(description="Get hash as bytes")
    def bytes(self) -> bytes:
        """Get the raw hash digest as bytes."""
        return self._digest_bytes

    @ml_function(description="Get hash length in bytes")
    def size(self) -> int:
        """Get the size of the hash in bytes."""
        return len(self._digest_bytes)


@ml_module(
    name="crypto",
    description="Cryptographic operations for hashing, encryption, and secure random generation",
    capabilities=["crypto.hash", "crypto.random"],
    version="1.0.0"
)
class CryptoModule:
    """Cryptography operations with capability-based security.

    Provides secure hashing, HMAC, and random number generation.
    All operations are designed to be cryptographically secure.
    """

    # Supported hash algorithms
    ALGORITHMS = ["md5", "sha1", "sha224", "sha256", "sha384", "sha512"]

    @ml_function(
        description="Compute cryptographic hash of data",
        capabilities=["crypto.hash"]
    )
    def hash(self, data: str, algorithm: str = "sha256") -> HashResult:
        """Compute cryptographic hash of data.

        Args:
            data: String data to hash
            algorithm: Hash algorithm (sha256, sha512, md5, sha1, etc.)

        Returns:
            HashResult object with hex() and bytes() methods

        Capability:
            Requires: crypto.hash

        Examples:
            hash_result = crypto.hash("secret data", "sha256")
            hex_digest = hash_result.hex()

        Raises:
            ValueError: If algorithm is not supported
        """
        if algorithm not in self.ALGORITHMS:
            raise ValueError(f"Unsupported algorithm: {algorithm}")

        hasher = hashlib.new(algorithm)
        hasher.update(data.encode('utf-8'))

        digest_bytes = hasher.digest()
        digest_hex = hasher.hexdigest()

        return HashResult(algorithm, digest_hex, digest_bytes)

    @ml_function(
        description="Compute HMAC of data with secret key",
        capabilities=["crypto.hash"]
    )
    def hmac(self, data: str, key: str, algorithm: str = "sha256") -> str:
        """Compute HMAC (Hash-based Message Authentication Code).

        Args:
            data: Message to authenticate
            key: Secret key
            algorithm: Hash algorithm to use

        Returns:
            HMAC digest as hexadecimal string

        Capability:
            Requires: crypto.hash

        Examples:
            signature = crypto.hmac("message", "secret_key", "sha256")
        """
        if algorithm not in self.ALGORITHMS:
            raise ValueError(f"Unsupported algorithm: {algorithm}")

        mac = hmac.new(
            key.encode('utf-8'),
            data.encode('utf-8'),
            hashlib.new(algorithm)
        )
        return mac.hexdigest()

    @ml_function(
        description="Generate cryptographically secure random bytes",
        capabilities=["crypto.random"]
    )
    def randomBytes(self, length: int) -> bytes:
        """Generate cryptographically secure random bytes.

        Args:
            length: Number of random bytes to generate

        Returns:
            Random bytes

        Capability:
            Requires: crypto.random

        Examples:
            random_data = crypto.randomBytes(32)
        """
        if length <= 0:
            raise ValueError("Length must be positive")
        return secrets.token_bytes(length)

    @ml_function(
        description="Generate cryptographically secure random hex string",
        capabilities=["crypto.random"]
    )
    def randomHex(self, length: int) -> str:
        """Generate cryptographically secure random hexadecimal string.

        Args:
            length: Number of random bytes (resulting string is 2x length)

        Returns:
            Random hexadecimal string

        Capability:
            Requires: crypto.random

        Examples:
            token = crypto.randomHex(16)  // 32-character hex string
        """
        if length <= 0:
            raise ValueError("Length must be positive")
        return secrets.token_hex(length)


# Global module instance
crypto = CryptoModule()

__all__ = ["CryptoModule", "HashResult", "crypto"]
```

**Complete Module Registration:**
```python
# In src/mlpy/stdlib/__init__.py
from .crypto_bridge import crypto

__all__ = [
    # ... existing modules ...
    "crypto",
]
```

**Code Generator Registration:**
```python
# In src/mlpy/ml/codegen/python_generator.py
if module_path in [
    "math", "json", "datetime", "random", "collections", "console",
    "string", "array", "functional", "regex",
    "file", "path", "http",
    "crypto",  # Add new module here
]:
```

**Unit Tests Example:**
```python
"""Unit tests for crypto_bridge module."""

import pytest
from mlpy.stdlib.crypto_bridge import CryptoModule, crypto
from mlpy.stdlib.decorators import get_module_metadata, _MODULE_REGISTRY


class TestCryptoModuleRegistration:
    """Test that Crypto module is properly registered."""

    def test_crypto_module_registered(self):
        """Test that crypto module is in global registry."""
        assert "crypto" in _MODULE_REGISTRY
        assert _MODULE_REGISTRY["crypto"] == CryptoModule

    def test_crypto_module_metadata(self):
        """Test crypto module metadata."""
        metadata = get_module_metadata("crypto")
        assert metadata.name == "crypto"
        assert "crypto.hash" in metadata.capabilities
        assert "crypto.random" in metadata.capabilities

    def test_crypto_has_function_metadata(self):
        """Test that crypto module has registered functions."""
        metadata = get_module_metadata("crypto")

        assert "hash" in metadata.functions
        assert "hmac" in metadata.functions
        assert "randomBytes" in metadata.functions
        assert "randomHex" in metadata.functions


class TestHashOperations:
    """Test cryptographic hash operations."""

    def test_sha256_hash(self):
        """Test SHA-256 hashing."""
        result = crypto.hash("hello world", "sha256")

        assert result.algorithm() == "sha256"
        assert len(result.hex()) == 64  # SHA-256 produces 64 hex chars
        assert result.size() == 32      # 32 bytes

    def test_hash_result_methods(self):
        """Test HashResult methods."""
        result = crypto.hash("test", "sha256")

        hex_digest = result.hex()
        bytes_digest = result.bytes()

        assert isinstance(hex_digest, str)
        assert isinstance(bytes_digest, bytes)
        assert len(hex_digest) == 64
        assert len(bytes_digest) == 32
```

---

#### 2.2 Capability Management - Designing and Testing (NEW - ~1500 lines)

**Purpose:** Guide Python developers on designing, implementing, and testing capability-based security for ML code execution
**Length:** ~1500 lines
**Audience:** Python developers integrating ML code execution into their applications

**Note:** This system is not fully implemented yet and documentation will need updates as implementation progresses.

**Content Structure:**

##### Section 1: Capability Context Setup (~300 lines)

**Creating a Capability Context:**
```python
from mlpy.runtime.capabilities.context import CapabilityContext
from mlpy.runtime.capabilities.tokens import CapabilityToken, CapabilityConstraint

# Create a new capability context
context = CapabilityContext(name="data-processor")

# Context has unique ID and tracks creation time
print(context.context_id)    # UUID
print(context.created_at)    # Timestamp
print(context.thread_id)     # Thread-safe operations
```

**Context Hierarchy:**
```python
# Parent context with broad permissions
parent_context = CapabilityContext(name="parent")
parent_token = CapabilityToken(capability_type="file.read")
parent_context.add_capability(parent_token)

# Child context inherits parent's capabilities
child_context = CapabilityContext(
    name="child",
    parent_context=parent_context
)

# Child can access parent's capabilities
assert child_context.has_capability("file.read")  # True from parent
assert child_context.has_capability("file.write")  # False
```

**Thread-Safe Capability Management:**
```python
import threading

context = CapabilityContext(name="shared-context")

# Add capabilities from multiple threads safely
def add_file_capability():
    token = CapabilityToken(capability_type="file.read")
    context.add_capability(token)  # Thread-safe

threads = [threading.Thread(target=add_file_capability) for _ in range(10)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

# Context maintains consistency
assert context.has_capability("file.read")
```

##### Section 2: Creating Capability Tokens (~400 lines)

**Basic Token Creation:**
```python
from mlpy.runtime.capabilities.tokens import CapabilityToken

# Simple capability token
token = CapabilityToken(
    capability_type="file.read",
    description="Read access to data files"
)

# Token has unique ID and tracks usage
print(token.token_id)       # UUID
print(token.created_at)     # Timestamp
print(token.usage_count)    # 0 initially
print(token.is_valid())     # True
```

**Token with Resource Patterns:**
```python
from mlpy.runtime.capabilities.tokens import CapabilityConstraint

# Create constraint with resource patterns
constraint = CapabilityConstraint(
    resource_patterns=[
        "/data/*.csv",
        "/data/reports/*.json",
        "/input/**/*"
    ],
    allowed_operations={"read"}
)

# Create token with constraints
token = CapabilityToken(
    capability_type="file.read",
    constraints=constraint,
    description="Limited file read access"
)

# Check if token allows specific resource access
assert token.can_access_resource("/data/input.csv", "read")  # True
assert token.can_access_resource("/data/reports/q1.json", "read")  # True
assert token.can_access_resource("/etc/passwd", "read")  # False - not in patterns
assert token.can_access_resource("/data/input.csv", "write")  # False - wrong operation
```

**Time-Based Token Expiration:**
```python
from datetime import datetime, timedelta

# Token that expires in 1 hour
constraint = CapabilityConstraint(
    resource_patterns=["/tmp/*"],
    expires_at=datetime.now() + timedelta(hours=1)
)

token = CapabilityToken(
    capability_type="file.write",
    constraints=constraint,
    description="Temporary write access"
)

# Check validity
assert token.is_valid()  # True now

# After expiration
# time.sleep(3601)  # Wait 1 hour and 1 second
# assert not token.is_valid()  # False - expired
```

**Usage-Limited Tokens:**
```python
# Token that can be used only 10 times
constraint = CapabilityConstraint(
    resource_patterns=["/api/*"],
    max_usage_count=10
)

token = CapabilityToken(
    capability_type="network.https",
    constraints=constraint,
    description="Limited API access"
)

# Use token multiple times
for i in range(10):
    token.use_token("/api/endpoint", "https")
    print(f"Usage count: {token.usage_count}")

# Token is now exhausted
assert not token.is_valid()  # False - max uses reached
```

**Resource Limits:**
```python
# Token with file size and memory limits
constraint = CapabilityConstraint(
    resource_patterns=["/data/*"],
    max_file_size=10 * 1024 * 1024,  # 10 MB
    max_memory=100 * 1024 * 1024,    # 100 MB
    allowed_operations={"read"}
)

token = CapabilityToken(
    capability_type="file.read",
    constraints=constraint,
    description="Size-limited file access"
)
```

**Token Integrity Validation:**
```python
# Tokens have built-in integrity checking
token = CapabilityToken(capability_type="file.read")

# Validate integrity (checksum verification)
assert token.validate_integrity()  # True

# Tampering detection (internal mechanism prevents modification)
assert token.is_valid()  # Checks integrity + expiration + usage
```

##### Section 3: Executing ML Code with Capabilities (~400 lines)

**Basic Execution with Capabilities:**
```python
from mlpy.ml.transpiler import MLTranspiler
from mlpy.runtime.capabilities.context import CapabilityContext
from mlpy.runtime.capabilities.tokens import CapabilityToken

# ML code that requires file access
ml_code = """
import file;
content = file.read("/data/input.txt");
print(content);
"""

# Create context with file.read capability
context = CapabilityContext(name="file-reader")
token = CapabilityToken(capability_type="file.read")
context.add_capability(token)

# Execute with capability context
transpiler = MLTranspiler()
result, issues = transpiler.execute_with_sandbox(
    ml_code,
    context=context,
    strict_security=True
)

if result and result.success:
    print("Execution successful!")
    print(result.output)
else:
    print("Execution failed:", issues)
```

**Pattern-Restricted Execution:**
```python
from mlpy.runtime.capabilities.tokens import CapabilityConstraint

# ML code that tries to access multiple files
ml_code = """
import file;

// This should succeed
data1 = file.read("/data/input.csv");

// This should fail (not in pattern)
data2 = file.read("/etc/passwd");
"""

# Context with pattern restriction
context = CapabilityContext(name="restricted-reader")
constraint = CapabilityConstraint(
    resource_patterns=["/data/*"],
    allowed_operations={"read"}
)
token = CapabilityToken(
    capability_type="file.read",
    constraints=constraint
)
context.add_capability(token)

# Execute - second file.read will be denied
transpiler = MLTranspiler()
result, issues = transpiler.execute_with_sandbox(
    ml_code,
    context=context,
    strict_security=True
)

# Check for capability violations in issues
capability_violations = [
    issue for issue in issues
    if "capability" in issue.error.message.lower()
]
```

**Multiple Capabilities:**
```python
# ML code needing both file and network access
ml_code = """
import http;
import file;

// Fetch data from API
response = http.get("https://api.example.com/data");

// Save to file
file.write("/output/result.json", response.text());
"""

# Create context with multiple capabilities
context = CapabilityContext(name="data-fetcher")

# Network capability
network_constraint = CapabilityConstraint(
    resource_patterns=["https://api.example.com/*"]
)
network_token = CapabilityToken(
    capability_type="network.https",
    constraints=network_constraint
)
context.add_capability(network_token)

# File capability
file_constraint = CapabilityConstraint(
    resource_patterns=["/output/*"],
    allowed_operations={"write"}
)
file_token = CapabilityToken(
    capability_type="file.write",
    constraints=file_constraint
)
context.add_capability(file_token)

# Execute with both capabilities
transpiler = MLTranspiler()
result, issues = transpiler.execute_with_sandbox(
    ml_code,
    context=context
)
```

**Dynamic Capability Granting:**
```python
# Start with minimal capabilities
context = CapabilityContext(name="dynamic")

# Execute code that will fail initially
ml_code = "import file; content = file.read('/data/input.txt');"

transpiler = MLTranspiler()
result1, issues1 = transpiler.execute_with_sandbox(ml_code, context=context)
assert not result1.success  # Fails - no capability

# Grant capability dynamically
token = CapabilityToken(capability_type="file.read")
context.add_capability(token)

# Retry with capability
result2, issues2 = transpiler.execute_with_sandbox(ml_code, context=context)
assert result2.success  # Succeeds - capability granted

# Revoke capability
context.remove_capability("file.read")

# Fails again without capability
result3, issues3 = transpiler.execute_with_sandbox(ml_code, context=context)
assert not result3.success  # Fails - capability revoked
```

##### Section 4: Testing Capability Security (~300 lines)

**Unit Testing Capability Checks:**
```python
import pytest
from mlpy.runtime.capabilities.context import CapabilityContext
from mlpy.runtime.capabilities.tokens import CapabilityToken, CapabilityConstraint
from mlpy.runtime.capabilities.exceptions import CapabilityNotFoundError

class TestCapabilityContext:
    """Test capability context functionality."""

    def test_add_and_check_capability(self):
        """Test adding and checking capabilities."""
        context = CapabilityContext(name="test")
        token = CapabilityToken(capability_type="file.read")

        context.add_capability(token)

        assert context.has_capability("file.read")
        assert not context.has_capability("file.write")

    def test_remove_capability(self):
        """Test removing capabilities."""
        context = CapabilityContext(name="test")
        token = CapabilityToken(capability_type="file.read")

        context.add_capability(token)
        assert context.has_capability("file.read")

        context.remove_capability("file.read")
        assert not context.has_capability("file.read")

    def test_get_missing_capability_raises(self):
        """Test that getting missing capability raises error."""
        context = CapabilityContext(name="test")

        with pytest.raises(CapabilityNotFoundError):
            context.get_capability("file.read")

    def test_parent_context_inheritance(self):
        """Test capability inheritance from parent."""
        parent = CapabilityContext(name="parent")
        parent_token = CapabilityToken(capability_type="file.read")
        parent.add_capability(parent_token)

        child = CapabilityContext(name="child", parent_context=parent)

        # Child inherits parent's capability
        assert child.has_capability("file.read")

class TestCapabilityTokens:
    """Test capability token functionality."""

    def test_resource_pattern_matching(self):
        """Test resource pattern matching."""
        constraint = CapabilityConstraint(
            resource_patterns=["/data/*.csv"],
            allowed_operations={"read"}
        )
        token = CapabilityToken(
            capability_type="file.read",
            constraints=constraint
        )

        assert token.can_access_resource("/data/input.csv", "read")
        assert not token.can_access_resource("/etc/passwd", "read")
        assert not token.can_access_resource("/data/input.csv", "write")

    def test_token_expiration(self):
        """Test token expiration."""
        from datetime import datetime, timedelta

        constraint = CapabilityConstraint(
            expires_at=datetime.now() - timedelta(hours=1)
        )
        token = CapabilityToken(
            capability_type="file.read",
            constraints=constraint
        )

        assert not token.is_valid()  # Expired

    def test_usage_count_limit(self):
        """Test usage count limitation."""
        constraint = CapabilityConstraint(max_usage_count=3)
        token = CapabilityToken(
            capability_type="file.read",
            constraints=constraint
        )

        assert token.is_valid()

        # Use 3 times
        for _ in range(3):
            token.use_token("/data/file.txt", "read")

        assert not token.is_valid()  # Exhausted
```

**Integration Testing Capability Enforcement:**
```python
import pytest
from mlpy.ml.transpiler import MLTranspiler
from mlpy.runtime.capabilities.context import CapabilityContext
from mlpy.runtime.capabilities.tokens import CapabilityToken, CapabilityConstraint

class TestCapabilityEnforcement:
    """Test that capabilities are enforced during execution."""

    def test_file_read_requires_capability(self):
        """Test that file.read requires capability."""
        ml_code = 'import file; content = file.read("/data/test.txt");'

        # Without capability - should fail
        context_no_cap = CapabilityContext(name="no-cap")
        transpiler = MLTranspiler()

        result, issues = transpiler.execute_with_sandbox(
            ml_code,
            context=context_no_cap
        )

        assert not result.success
        assert any("capability" in str(issue).lower() for issue in issues)

    def test_resource_pattern_enforcement(self):
        """Test that resource patterns are enforced."""
        ml_code = 'import file; content = file.read("/etc/passwd");'

        # With restricted capability
        context = CapabilityContext(name="restricted")
        constraint = CapabilityConstraint(
            resource_patterns=["/data/*"]
        )
        token = CapabilityToken(
            capability_type="file.read",
            constraints=constraint
        )
        context.add_capability(token)

        transpiler = MLTranspiler()
        result, issues = transpiler.execute_with_sandbox(
            ml_code,
            context=context
        )

        # Should fail - /etc/passwd not in pattern
        assert not result.success

    def test_multiple_capabilities_work_together(self):
        """Test multiple capabilities work together."""
        ml_code = '''
        import file;
        import http;

        response = http.get("https://api.example.com/data");
        file.write("/output/result.txt", response.text());
        '''

        context = CapabilityContext(name="multi-cap")

        # Add network capability
        network_token = CapabilityToken(capability_type="network.https")
        context.add_capability(network_token)

        # Add file capability
        file_token = CapabilityToken(capability_type="file.write")
        context.add_capability(file_token)

        transpiler = MLTranspiler()
        result, issues = transpiler.execute_with_sandbox(
            ml_code,
            context=context
        )

        # Should succeed with both capabilities
        assert result.success or len(issues) == 0  # Network might fail in tests
```

##### Section 5: Best Practices and Patterns (~100 lines)

**Design Principles:**
- ✅ **Principle of Least Privilege:** Grant only required capabilities
- ✅ **Use Resource Patterns:** Restrict access to specific paths/URLs
- ✅ **Set Expiration:** Use time-based limits for temporary access
- ✅ **Validate Token Integrity:** Always check token validity before use
- ✅ **Audit Capability Usage:** Log all capability grants and uses
- ❌ **Don't Grant Broad Patterns:** Avoid `"/*"` or `"*"` patterns
- ❌ **Don't Reuse Tokens:** Create new tokens for different contexts
- ❌ **Don't Skip Validation:** Always validate capabilities at runtime

**Example: Secure File Processing Application:**
```python
from mlpy.runtime.capabilities.context import CapabilityContext
from mlpy.runtime.capabilities.tokens import CapabilityToken, CapabilityConstraint
from mlpy.ml.transpiler import MLTranspiler

class SecureMLFileProcessor:
    """Secure ML code executor with capability-based file access."""

    def __init__(self, input_dir: str, output_dir: str):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.transpiler = MLTranspiler()

    def process_file(self, ml_code: str) -> bool:
        """Execute ML code with restricted file access."""
        # Create context with restricted capabilities
        context = CapabilityContext(name="file-processor")

        # Input directory - read only
        input_constraint = CapabilityConstraint(
            resource_patterns=[f"{self.input_dir}/**/*"],
            allowed_operations={"read"}
        )
        input_token = CapabilityToken(
            capability_type="file.read",
            constraints=input_constraint,
            description="Read input files"
        )
        context.add_capability(input_token)

        # Output directory - write only
        output_constraint = CapabilityConstraint(
            resource_patterns=[f"{self.output_dir}/**/*"],
            allowed_operations={"write"}
        )
        output_token = CapabilityToken(
            capability_type="file.write",
            constraints=output_constraint,
            description="Write output files"
        )
        context.add_capability(output_token)

        # Execute with strict security
        result, issues = self.transpiler.execute_with_sandbox(
            ml_code,
            context=context,
            strict_security=True
        )

        return result and result.success

# Usage
processor = SecureMLFileProcessor("/data/input", "/data/output")
success = processor.process_file("""
import file;
data = file.read("/data/input/data.csv");
result = process(data);  // User's processing logic
file.write("/data/output/result.txt", result);
""")
```

**Code Snippets for Integration Guide:**
```
docs/py_snippets/capabilities/
├── basic_context.py           # Basic CapabilityContext usage
├── token_creation.py          # Creating CapabilityTokens
├── pattern_matching.py        # Resource pattern examples
├── execution_with_caps.py     # Executing ML code with capabilities
├── testing_capabilities.py    # Unit tests for capabilities
├── secure_processor.py        # Complete secure file processor example
└── advanced_patterns.py       # Advanced capability patterns
```

---

### TIER 3: Developer Guide

#### 3.0 Testing Infrastructure (NEW - CRITICAL IMPORTANCE)

The mlpy project includes two comprehensive test runners that provide end-to-end integration testing of the entire ML compilation and execution pipeline. These tools are ESSENTIAL for developers to validate changes and understand system behavior.

##### 3.0.1 ML Test Runner (NEW - ~1000 lines)

**File:** `tests/ml_test_runner.py`
**Purpose:** Unified end-to-end pipeline testing with 10-stage validation and detailed result matrices

**Importance:** This is the PRIMARY tool for validating the complete ML compilation pipeline from parsing through execution. Essential for understanding pipeline behavior and debugging integration issues.

**Content Structure:**

**Section 1: Overview (~100 lines)**
- What the ML Test Runner does
- Why it's critical for development
- When to use it (after changes to parser, AST, security, codegen, etc.)
- Complete 10-stage pipeline validation

**Section 2: Pipeline Stages (~200 lines)**

The test runner validates all 10 stages of the ML compilation pipeline:

1. **Parse** - ML source parsing and AST generation
   - Tests: Lark grammar parsing
   - Validates: Syntax correctness

2. **AST** - AST creation and basic structure
   - Tests: AST node construction
   - Validates: AST structure integrity

3. **AST_V** - AST validation and integrity checking
   - Tests: Semantic validation
   - Validates: AST correctness and completeness

4. **Trans** - AST transformation and normalization
   - Tests: AST transformations
   - Validates: Normalized AST output

5. **Type** - Static type checking and inference
   - Tests: Type system
   - Validates: Type correctness

6. **Sec_D** - Enhanced security analysis with type awareness
   - Tests: Deep security analysis
   - Validates: Advanced threat detection

7. **Opt** - Code optimization and performance enhancement
   - Tests: Optimization passes
   - Validates: Optimized AST

8. **Security** - Original security analysis and threat detection
   - Tests: Pattern-based security
   - Validates: Security compliance

9. **CodeGen** - Python code generation
   - Tests: Python AST generation
   - Validates: Correct Python output

10. **Exec** - Sandboxed execution testing
    - Tests: Runtime execution
    - Validates: Correct program behavior

**Section 3: CLI Reference (~300 lines)**

**Complete CLI Interface:**

```bash
# Basic usage
python tests/ml_test_runner.py --help

# Modes
--parse              # Parse validation only (fast)
--full               # Complete pipeline testing (all 10 stages)

# Output options
--matrix             # Show result matrix (visual stage-by-stage results)
--details            # Include error details in matrix
--show-failures      # Show only failed files with detailed errors
--output FILE        # Save results to JSON file

# Filtering
--dir DIR            # Custom test directory (default: tests/ml_integration)
--category CAT       # Test specific category only
                     # Options: ml_core, ml_builtin, ml_stdlib, ml_module
```

**Usage Examples:**

```bash
# Quick parse validation (fast feedback on syntax changes)
python tests/ml_test_runner.py --parse

# Complete pipeline testing with visual matrix
python tests/ml_test_runner.py --full --matrix

# Detailed failure analysis
python tests/ml_test_runner.py --full --matrix --details

# Show only failures for quick debugging
python tests/ml_test_runner.py --full --show-failures

# Test specific category
python tests/ml_test_runner.py --full --category ml_core

# Export results for CI/CD
python tests/ml_test_runner.py --full --output results.json
```

**Section 4: Understanding Results (~200 lines)**

**Result Matrix Legend:**
- `+` = Pass - Stage completed successfully
- `X` = Fail - Stage failed validation
- `E` = Error - Exception during stage
- `-` = Skipped - Stage not executed

**Example Result Matrix:**
```
File: 08_control_structures.ml
Stages: Parse  AST  AST_V  Trans  Type  Sec_D  Opt  Security  CodeGen  Exec
Result:   +     +     +      +      +      +     +      +        +       +
Time:   5ms   2ms   1ms    3ms    4ms    2ms   1ms    3ms      8ms     15ms
```

**Interpreting Results:**
- **All `+`:** File passes complete pipeline (ready for production)
- **Early failure (Parse, AST):** Syntax or grammar issue
- **Mid failure (Type, Sec_D):** Semantic or security issue
- **Late failure (CodeGen, Exec):** Code generation or runtime issue

**Section 5: Test Categories (~150 lines)**

**ml_core:** Core ML language features
- Control flow (if/elif/else, while, for)
- Functions (definitions, arrow functions, closures)
- Data structures (arrays, objects, destructuring)
- Exception handling (try/except/finally)
- Advanced features (nonlocal, slicing)

**ml_builtin:** Built-in functions
- Type checking (typeof)
- Type conversion (int, float, str)
- Collection operations (len, range, keys, values)
- Array/object utilities
- Math utilities (abs, min, max, sum)

**ml_stdlib:** Standard library modules
- Console, math, datetime, json
- Collections, functional, regex, random
- File, path, http modules

**ml_module:** User module system
- Module imports and exports
- Module aliasing
- Dependency resolution

**Section 6: Developer Workflows (~50 lines)**

**Daily Development:**
```bash
# Quick validation after grammar changes
python tests/ml_test_runner.py --parse

# Full validation before committing
python tests/ml_test_runner.py --full --matrix
```

**Debugging Pipeline Issues:**
```bash
# See exactly where failures occur
python tests/ml_test_runner.py --full --matrix --details

# Focus on failures only
python tests/ml_test_runner.py --full --show-failures
```

**CI/CD Integration:**
```bash
# Generate machine-readable results
python tests/ml_test_runner.py --full --output ci_results.json

# Exit code indicates pass/fail
echo $?  # 0 = success, 1 = failures
```

---

##### 3.0.2 REPL Test Runner (NEW - ~800 lines)

**File:** `tests/ml_repl_test_runner.py`
**Purpose:** Comprehensive REPL integration testing with statement-level validation and performance benchmarking

**Importance:** This tool validates the REPL's ability to execute hundreds of ML statements incrementally, test variable persistence, stdlib imports, and REPL command functionality. Essential for REPL development and v2.3 performance validation.

**Content Structure:**

**Section 1: Overview (~100 lines)**
- What the REPL Test Runner does
- Why it's critical for REPL development
- When to use it (after REPL changes, transpiler updates, stdlib additions)
- Statement-level incremental execution testing

**Section 2: Test Categories (~200 lines)**

**REPL Commands:** Tests REPL-specific commands
- `.help` - Command help
- `.vars` - Variable inspection
- `.history` - Command history
- `.clear` - Clear variables
- `.reset` - Session reset
- `.capabilities` - Capability management (v2.2+)
- `.retry` - Error recovery (v2.2+)
- `.edit` - External editor (v2.2+)

**Builtin Functions:** Tests all ML builtin functions
- typeof, int, float, str
- len, range, keys, values, entries
- print, abs, min, max, sum
- All 50+ builtin functions

**Core Language Features:** Tests core ML syntax
- Variables and expressions
- Control flow (if/elif/else)
- Loops (while, for)
- Functions (named, arrow)
- Data structures (arrays, objects)
- Exception handling

**Standard Library:** Tests stdlib module imports
- Import statements
- Module method calls
- Capability enforcement
- Module interoperability

**Section 3: CLI Reference (~250 lines)**

**Complete CLI Interface:**

```bash
# Basic usage
python tests/ml_repl_test_runner.py --help

# Test categories (can combine)
--builtin            # Test builtin functions only
--core               # Test core language features only
--stdlib             # Test stdlib imports only
--commands           # Test REPL commands only

# Execution control
--limit N            # Limit to N statements (default: 200)
                     # Useful for quick validation

# Output control
--verbose, -v        # Show detailed output for all statements
--no-color           # Disable colored output (for CI/CD)
```

**Usage Examples:**

```bash
# Run all tests (comprehensive validation)
python tests/ml_repl_test_runner.py

# Test only builtin functions (after builtin changes)
python tests/ml_repl_test_runner.py --builtin

# Test core language features (after grammar changes)
python tests/ml_repl_test_runner.py --core

# Test stdlib imports (after stdlib additions)
python tests/ml_repl_test_runner.py --stdlib

# Test REPL commands (after REPL feature additions)
python tests/ml_repl_test_runner.py --commands

# Quick validation (50 statements)
python tests/ml_repl_test_runner.py --limit 50

# Detailed output for debugging
python tests/ml_repl_test_runner.py --verbose

# CI/CD friendly output
python tests/ml_repl_test_runner.py --no-color

# Combined: Test builtins with limited statements
python tests/ml_repl_test_runner.py --builtin --limit 50
```

**Section 4: Understanding Results (~150 lines)**

**Output Format:**

```
Running REPL Integration Tests
==============================

REPL Commands
  Test REPL-specific commands (.help, .vars, .history, etc.)
  Results: 4 passed, 0 failed, 4 total
  Success Rate: 100.0%
  Duration: 0.05s (avg: 12.50ms per statement)

Builtin Functions & Variables
  Test builtin module functions (typeof, len, etc.) and variables
  Results: 50 passed, 0 failed, 50 total
  Success Rate: 100.0%
  Duration: 0.80s (avg: 16.00ms per statement)

Core Language Features
  Test core ML syntax (variables, functions, control flow)
  Results: 100 passed, 0 failed, 100 total
  Success Rate: 100.0%
  Duration: 0.83s (avg: 8.30ms per statement)

Overall Results:
  Total Statements: 154
  Passed: 154
  Failed: 0
  Success Rate: 100.0%

Timing Summary:
  Total Elapsed Time: 1.68s
  Test Execution Time: 1.68s
  Average per Statement: 10.91ms
  Throughput: 91.6 statements/second
```

**Performance Metrics:**
- **Average per Statement:** Indicates REPL performance (<10ms target for v2.3)
- **Throughput:** Statements per second (higher is better)
- **Success Rate:** Percentage of passing statements
- **Duration:** Time per category (helps identify slow areas)

**Section 5: Performance Validation (~100 lines)**

**REPL v2.3 Performance Targets:**
- **Sub-10ms execution:** Average <10ms per statement
- **100% success rate:** All statements execute correctly
- **Variable persistence:** State maintained across statements
- **Incremental compilation:** O(1) transpilation complexity

**Benchmarking Workflow:**
```bash
# Baseline performance measurement
python tests/ml_repl_test_runner.py --limit 200

# After optimization changes
python tests/ml_repl_test_runner.py --limit 200

# Compare average per statement times
# v2.2: ~75ms  →  v2.3: ~6.93ms (10.8x improvement)
```

**Section 6: Developer Workflows (~100 lines)**

**After REPL Changes:**
```bash
# Validate REPL commands still work
python tests/ml_repl_test_runner.py --commands

# Full REPL validation
python tests/ml_repl_test_runner.py
```

**After Transpiler Changes:**
```bash
# Ensure incremental compilation works
python tests/ml_repl_test_runner.py --core

# Check performance impact
python tests/ml_repl_test_runner.py --limit 100
```

**After Stdlib Changes:**
```bash
# Validate new modules work in REPL
python tests/ml_repl_test_runner.py --stdlib
```

**Performance Regression Testing:**
```bash
# Benchmark current performance
python tests/ml_repl_test_runner.py --limit 200 > baseline.txt

# After changes, compare
python tests/ml_repl_test_runner.py --limit 200 > current.txt

# Check if "Average per Statement" increased
diff baseline.txt current.txt
```

---

#### 3.1 Architecture - Compilation Pipeline (REWRITE - ~800 lines)

**Current Issue:** Documents old 4-stage pipeline, now we have 10 stages

**New 10-Stage Pipeline Documentation:**

```
ML Source Code
      ↓
┌─────────────────────────────────────────────────────────┐
│ STAGE 1: PARSE                                          │
│ - Lark parser with ml.lark grammar                     │
│ - Lexical analysis and tokenization                    │
│ - Syntax tree construction                             │
│ Output: Lark Tree                                      │
└─────────────────────────────────────────────────────────┘
      ↓
┌─────────────────────────────────────────────────────────┐
│ STAGE 2: AST CONSTRUCTION                               │
│ - Convert Lark tree to ML AST nodes                    │
│ - AST node classes in ml/ast_nodes.py                  │
│ Output: ML AST                                         │
└─────────────────────────────────────────────────────────┘
      ↓
┌─────────────────────────────────────────────────────────┐
│ STAGE 3: AST VALIDATION                                 │
│ - Structural validation                                 │
│ - Semantic checks                                       │
│ Output: Validated AST + Issues                         │
└─────────────────────────────────────────────────────────┘
      ↓
┌─────────────────────────────────────────────────────────┐
│ STAGE 4: TRANSFORMATION                                 │
│ - AST transformations and normalization                │
│ - Desugaring complex constructs                        │
│ Output: Transformed AST                                │
└─────────────────────────────────────────────────────────┘
      ↓
┌─────────────────────────────────────────────────────────┐
│ STAGE 5: TYPE CHECKING                                  │
│ - Type inference and validation                        │
│ - Symbol table construction                            │
│ Output: Typed AST + Symbol Table                      │
└─────────────────────────────────────────────────────────┘
      ↓
┌─────────────────────────────────────────────────────────┐
│ STAGE 6: SECURITY ANALYSIS (DEEP)                       │
│ - Pattern detection (pattern_detector.py)              │
│ - Data flow analysis (data_flow_tracker.py)           │
│ - Parallel processing (parallel_analyzer.py)           │
│ Output: Security Threats (if any, compilation stops)   │
└─────────────────────────────────────────────────────────┘
      ↓
┌─────────────────────────────────────────────────────────┐
│ STAGE 7: OPTIMIZATION                                   │
│ - AST optimizations                                     │
│ - Dead code elimination                                │
│ - Constant folding                                     │
│ Output: Optimized AST + Optimization Report            │
└─────────────────────────────────────────────────────────┘
      ↓
┌─────────────────────────────────────────────────────────┐
│ STAGE 8: SECURITY ANALYSIS (FINAL)                      │
│ - Final security check on optimized code               │
│ - Ensures optimizations didn't introduce issues        │
│ Output: Security Validation                            │
└─────────────────────────────────────────────────────────┘
      ↓
┌─────────────────────────────────────────────────────────┐
│ STAGE 9: CODE GENERATION                                │
│ - Python AST generation (python_generator.py)          │
│ - Enhanced assignment support                          │
│ - Whitelist enforcement injection                      │
│ - Source map generation                                │
│ Output: Python Code + Source Maps                      │
└─────────────────────────────────────────────────────────┘
      ↓
┌─────────────────────────────────────────────────────────┐
│ STAGE 10: EXECUTION (Optional)                          │
│ - Sandbox execution (sandbox.py)                       │
│ - Capability context setup                             │
│ - Resource monitoring                                  │
│ Output: Execution Results                              │
└─────────────────────────────────────────────────────────┘
      ↓
Python Code / Execution Results
```

**Each Stage Documentation Includes:**
- Purpose and responsibilities
- Input/output specifications
- Key classes and functions
- Error handling
- Performance considerations
- Examples from test suite

---

#### 3.2 Security Analysis (MAJOR UPDATE - ~900 lines)

**Document Current Implementation:**

1. **Parallel Security Analyzer** (parallel_analyzer.py)
   - Thread-local analyzer instances
   - 97.8% performance improvement
   - Intelligent caching (98% hit rate)
   - Sub-millisecond analysis

2. **Pattern Detector** (pattern_detector.py)
   - 40+ security patterns
   - 6 reflection detection patterns
   - False positive elimination strategies
   - Pattern exclusions for safe stdlib

3. **Data Flow Tracker** (data_flow_tracker.py)
   - 47 taint sources
   - Complex propagation analysis
   - Cross-function tracking

4. **AST Analyzer** (ast_analyzer.py)
   - Comprehensive AST traversal
   - Security violation detection
   - Visitor pattern implementation

**Example Security Patterns:**
```python
# Code injection
pattern=r"(?<!regex\.)\b(eval|exec|compile)\s*\("

# Class hierarchy traversal (reflection)
pattern=r"__class__\.__bases__|\.__mro__|\.__subclasses__\s*\("

# File system access (with stdlib exclusion)
pattern=r"\b(open)\s*\(.*['\"].*['\"].*\)|pathlib\.|os\.path\.|shutil\."
# Note: Excludes 'file' module which has capability enforcement

# Network access (with stdlib exclusion)
pattern=r"\b(urllib|requests|socket)\."
# Note: Excludes 'http' module which has capability enforcement
```

---

#### 3.3 Capability System - Implementation and Configuration (NEW - ~1200 lines)

**Purpose:** Guide mlpy core developers on the capability system architecture, implementation, and configuration
**Length:** ~1200 lines
**Audience:** mlpy core developers extending or modifying the capability system

**Note:** This system is not fully implemented yet. This documentation describes the current implementation status and planned architecture.

**Content Structure:**

##### Section 1: Capability System Architecture (~250 lines)

**System Overview:**
```
Capability System Architecture
├── Tokens (src/mlpy/runtime/capabilities/tokens.py)
│   ├── CapabilityToken: Token with UUID, type, constraints
│   ├── CapabilityConstraint: Resource patterns, permissions, limits
│   └── Token validation and integrity checking
├── Context (src/mlpy/runtime/capabilities/context.py)
│   ├── CapabilityContext: Token container with hierarchy
│   ├── Thread-safe token management
│   └── Parent-child context inheritance
├── Exceptions (src/mlpy/runtime/capabilities/exceptions.py)
│   ├── CapabilityError: Base exception class
│   ├── CapabilityNotFoundError: Missing capability
│   ├── CapabilityExpiredError: Expired token
│   └── CapabilityValidationError: Invalid token
└── Integration Points
    ├── MLTranspiler: execute_with_sandbox()
    ├── MLSandbox: Runtime capability enforcement
    └── Standard Library: Module-level capability checks
```

**Core Concepts:**

**1. Capability Tokens:**
- UUID-based identity
- Capability type (e.g., "file.read", "network.https")
- Constraints (patterns, operations, limits)
- Usage tracking (count, last used)
- Integrity validation (SHA-256 checksum)

**2. Capability Context:**
- Named container for tokens
- Thread-safe operations (RLock)
- Parent-child hierarchy
- Capability inheritance
- Dynamic grant/revoke

**3. Resource Pattern Matching:**
- fnmatch-based patterns
- Supports wildcards (`*`, `**`)
- Path and URL matching
- Operation filtering

**Design Principles:**
- **Fine-Grained:** Per-resource and per-operation control
- **Revocable:** Capabilities can be removed at any time
- **Auditable:** Full tracking of grants, uses, revocations
- **Hierarchical:** Contexts inherit from parents
- **Thread-Safe:** Safe for concurrent use

##### Section 2: CapabilityToken Implementation (~300 lines)

**Token Data Structure:**
```python
# src/mlpy/runtime/capabilities/tokens.py

@dataclass
class CapabilityConstraint:
    """Constraint on capability usage."""

    # Resource matching
    resource_patterns: list[str] = field(default_factory=list)

    # Permission levels
    allowed_operations: set[str] = field(default_factory=set)

    # Time constraints
    max_usage_count: int | None = None
    expires_at: datetime | None = None

    # Resource limits
    max_file_size: int | None = None  # bytes
    max_memory: int | None = None     # bytes
    max_cpu_time: float | None = None # seconds

    # Network constraints
    allowed_hosts: list[str] = field(default_factory=list)
    allowed_ports: list[int] = field(default_factory=list)

    def matches_resource(self, resource_path: str) -> bool:
        """Check if resource matches patterns."""
        if not self.resource_patterns:
            return True  # No restrictions

        return any(
            fnmatch.fnmatch(resource_path, pattern)
            for pattern in self.resource_patterns
        )

    def allows_operation(self, operation: str) -> bool:
        """Check if operation is allowed."""
        if not self.allowed_operations:
            return True  # No restrictions

        return operation in self.allowed_operations


@dataclass
class CapabilityToken:
    """Capability token with validation."""

    # Core identity
    token_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    capability_type: str = ""

    # Constraints
    constraints: CapabilityConstraint = field(default_factory=CapabilityConstraint)

    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    created_by: str = "system"
    description: str = ""

    # Usage tracking
    usage_count: int = 0
    last_used_at: datetime | None = None

    # Security
    _checksum: str | None = field(default=None, init=False)

    def _calculate_checksum(self) -> str:
        """Calculate integrity checksum."""
        token_data = {
            "token_id": self.token_id,
            "capability_type": self.capability_type,
            "created_at": self.created_at.isoformat(),
            # ... include all immutable fields
        }
        token_json = json.dumps(token_data, sort_keys=True)
        return hashlib.sha256(token_json.encode()).hexdigest()

    def validate_integrity(self) -> bool:
        """Validate token hasn't been tampered with."""
        return self._calculate_checksum() == self._checksum

    def is_valid(self) -> bool:
        """Check if token is valid for use."""
        # Check integrity
        if not self.validate_integrity():
            return False

        # Check expiration
        if self.constraints.is_expired():
            return False

        # Check usage count
        if (
            self.constraints.max_usage_count is not None
            and self.usage_count >= self.constraints.max_usage_count
        ):
            return False

        return True

    def can_access_resource(self, resource_path: str, operation: str) -> bool:
        """Check if token allows resource access."""
        if not self.is_valid():
            return False

        if not self.constraints.matches_resource(resource_path):
            return False

        if not self.constraints.allows_operation(operation):
            return False

        return True

    def use_token(self, resource_path: str, operation: str) -> None:
        """Use the token for resource access."""
        if not self.can_access_resource(resource_path, operation):
            raise CapabilityViolationError(
                f"Access denied to {resource_path} for operation {operation}"
            )

        self.usage_count += 1
        self.last_used_at = datetime.now()
```

**Key Implementation Details:**
- Immutable token ID (UUID)
- Checksum prevents tampering
- Lazy expiration checking
- Thread-safe usage tracking
- Resource pattern matching with fnmatch
- Operation-level granularity

##### Section 3: CapabilityContext Implementation (~300 lines)

**Context Data Structure:**
```python
# src/mlpy/runtime/capabilities/context.py

@dataclass
class CapabilityContext:
    """Thread-safe capability context with inheritance."""

    # Core identity
    context_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""

    # Capability storage
    _tokens: dict[str, CapabilityToken] = field(default_factory=dict, init=False)

    # Context hierarchy
    parent_context: Optional["CapabilityContext"] = None
    child_contexts: list["CapabilityContext"] = field(default_factory=list, init=False)

    # Thread safety
    _lock: threading.RLock = field(default_factory=threading.RLock, init=False)

    # Metadata
    created_at: float = field(default_factory=time.time)
    thread_id: int | None = field(
        default_factory=lambda: threading.current_thread().ident,
        init=False
    )

    def add_capability(self, token: CapabilityToken) -> None:
        """Add capability token (thread-safe)."""
        with self._lock:
            if not token.is_valid():
                raise CapabilityContextError(f"Invalid token: {token.token_id}")

            self._tokens[token.capability_type] = token

    def remove_capability(self, capability_type: str) -> bool:
        """Remove capability (thread-safe)."""
        with self._lock:
            return self._tokens.pop(capability_type, None) is not None

    def has_capability(self, capability_type: str, check_parents: bool = True) -> bool:
        """Check for capability (with inheritance)."""
        with self._lock:
            # Check local capabilities
            if capability_type in self._tokens:
                token = self._tokens[capability_type]
                if token.is_valid():
                    return True
                else:
                    # Clean up expired token
                    del self._tokens[capability_type]

            # Check parent contexts
            if check_parents and self.parent_context:
                return self.parent_context.has_capability(
                    capability_type,
                    check_parents=True
                )

            return False

    def get_capability(self, capability_type: str, check_parents: bool = True) -> CapabilityToken:
        """Get capability token (with inheritance)."""
        with self._lock:
            # Check local capabilities
            if capability_type in self._tokens:
                token = self._tokens[capability_type]
                if token.is_valid():
                    return token
                else:
                    del self._tokens[capability_type]

            # Check parent contexts
            if check_parents and self.parent_context:
                return self.parent_context.get_capability(
                    capability_type,
                    check_parents=True
                )

            raise CapabilityNotFoundError(capability_type)

    @contextmanager
    def temporary_capability(self, token: CapabilityToken):
        """Context manager for temporary capability."""
        self.add_capability(token)
        try:
            yield
        finally:
            self.remove_capability(token.capability_type)
```

**Key Implementation Details:**
- Thread-safe with RLock
- Parent-child hierarchy
- Automatic expired token cleanup
- Context manager support
- Capability inheritance

##### Section 4: Integration with MLTranspiler (~200 lines)

**Transpiler Integration:**
```python
# src/mlpy/ml/transpiler.py

class MLTranspiler:
    def execute_with_sandbox(
        self,
        source_code: str,
        source_file: str | None = None,
        capabilities: list[CapabilityToken] | None = None,
        context: CapabilityContext | None = None,
        sandbox_config: SandboxConfig | None = None,
        strict_security: bool = True,
    ) -> tuple[SandboxResult | None, list[ErrorContext]]:
        """Execute ML code in sandbox with capabilities."""

        # Parse and analyze
        ast, security_issues = self.parse_with_security_analysis(
            source_code,
            source_file
        )

        if ast is None:
            return None, security_issues

        # Check security issues
        critical_issues = [
            issue for issue in security_issues
            if issue.error.severity.value in ["critical", "high"]
        ]

        if strict_security and critical_issues:
            return None, security_issues

        # Execute in sandbox with capability context
        config = sandbox_config or self.default_sandbox_config

        with MLSandbox(config) as sandbox:
            result = sandbox.execute(
                source_code,
                capabilities,
                context  # Pass capability context to sandbox
            )

            return result, security_issues
```

**Sandbox Integration:**
```python
# src/mlpy/runtime/sandbox.py

class MLSandbox:
    def execute(
        self,
        source_code: str,
        capabilities: list[CapabilityToken] | None = None,
        context: CapabilityContext | None = None,
    ) -> SandboxResult:
        """Execute code with capability enforcement."""

        # Create or use provided context
        if context is None:
            context = CapabilityContext(name="sandbox")

        # Add provided capabilities
        if capabilities:
            for token in capabilities:
                context.add_capability(token)

        # Transpile code
        python_code, issues, _ = self.transpiler.transpile_to_python(source_code)

        if python_code is None:
            return SandboxResult(success=False, error="Transpilation failed")

        # Execute with capability context in globals
        execution_globals = {
            "__capability_context__": context,
            # ... other sandbox globals
        }

        try:
            exec(python_code, execution_globals)
            return SandboxResult(success=True)
        except Exception as e:
            return SandboxResult(success=False, error=str(e))
```

##### Section 5: Standard Library Integration (~150 lines)

**Module-Level Capability Checks:**
```python
# src/mlpy/stdlib/file_bridge.py (example)

from mlpy.runtime.capabilities.context import get_current_context
from mlpy.runtime.capabilities.exceptions import CapabilityNotFoundError

class FileModule:
    """File I/O with capability enforcement."""

    @ml_function(
        description="Read file contents",
        capabilities=["file.read"]
    )
    def read(self, filepath: str) -> str:
        """Read file with capability check."""
        # Get current capability context
        context = get_current_context()

        # Check for file.read capability
        if not context.has_capability("file.read"):
            raise CapabilityNotFoundError("file.read")

        # Get token and validate resource pattern
        token = context.get_capability("file.read")
        if not token.can_access_resource(filepath, "read"):
            raise CapabilityViolationError(
                f"Access denied: {filepath} not in allowed patterns"
            )

        # Perform operation and track usage
        token.use_token(filepath, "read")

        # Actual file read
        with open(filepath, 'r') as f:
            return f.read()
```

**Context Accessor:**
```python
# src/mlpy/runtime/capabilities/context.py

# Thread-local storage for current context
_current_context: threading.local = threading.local()

def get_current_context() -> CapabilityContext:
    """Get the current thread's capability context."""
    if not hasattr(_current_context, "context"):
        # Create default empty context
        _current_context.context = CapabilityContext(name="default")

    return _current_context.context

def set_current_context(context: CapabilityContext) -> None:
    """Set the current thread's capability context."""
    _current_context.context = context

@contextmanager
def capability_context(context: CapabilityContext):
    """Context manager for temporarily setting capability context."""
    old_context = get_current_context()
    set_current_context(context)
    try:
        yield context
    finally:
        set_current_context(old_context)
```

**Best Practices for Core Developers:**
- ✅ Always validate tokens before granting access
- ✅ Use thread-local context for current execution
- ✅ Log all capability violations for auditing
- ✅ Clean up expired tokens automatically
- ✅ Use context managers for temporary capabilities
- ❌ Don't bypass capability checks in stdlib
- ❌ Don't store contexts in global variables
- ❌ Don't allow token modification after creation

---

## Migration Plan

### Phase 1: Foundation (Week 1-2)

**Goals:** Set up new structure, migrate existing good content, establish snippet infrastructure

**Tasks:**
1. Create new directory structure
2. **Create snippet directories:** `docs/ml_snippets/` and `docs/py_snippets/` with category subdirectories
3. Migrate tutorial.rst (excellent, keep as-is)
4. Migrate cli-reference.rst with updates
5. Set up Sphinx configuration for new structure
6. **Verify ML syntax highlighting** works correctly (already implemented in `ml_lexer.py`)
7. **Test literalinclude directive** with `:language: ml` for ML snippets

**Deliverables:**
- New directory structure created
- Snippet directories established with category organization
- 2 complete sections migrated
- Build system working with ML syntax support (using existing `ml_lexer.py`)
- Sample ML snippet verified to render with syntax highlighting

---

### Phase 2: Tutorial & Language Reference (Week 3-5)

**Goals:** Complete rewrite of tutorial and language reference with executable examples

**CRITICAL PREPARATION:**
- **FIRST:** Read and study `src/mlpy/ml/grammar/ml.lark` thoroughly
- **SECOND:** Review all integration tests in `tests/ml_integration/ml_core/` and `tests/ml_integration/ml_builtin/`
- **THIRD:** Study builtin implementation in `src/mlpy/stdlib/builtin.py`
- This preparation is MANDATORY before writing any ML code snippets

**Tasks:**

**Week 3: Tutorial (COMPLETE REWRITE - REPL-FIRST)**
1. **DELETE** existing `tutorial.rst` entirely (language and builtin incompatibilities)
2. **Study sources:**
   - Read `src/mlpy/ml/grammar/ml.lark` for correct ML syntax
   - Review `tests/ml_integration/ml_core/` for idiomatic ML code patterns
   - Study `src/mlpy/stdlib/builtin.py` for available builtin functions
   - Review `src/mlpy/cli/repl.py` for REPL commands and features
3. Write new **REPL-first** tutorial.rst (11 sections, ~1800-2200 lines) + **create ML snippets AND REPL transcripts** in `ml_snippets/tutorial/`
   - Section 1: Introduction to ML with REPL (~200 lines)
   - Section 2: Basic Syntax in the REPL (~350 lines)
   - Section 3: Control Flow in the REPL (~400 lines)
   - Section 4: Loops and Iteration in the REPL (~350 lines)
   - Section 5: Functions in the REPL (~450 lines)
   - Section 6: Data Structures in the REPL (~400 lines)
   - Section 7: Working with Builtins in the REPL (~350 lines)
   - Section 8: Exception Handling in the REPL (~300 lines)
   - Section 9: Working with Modules in the REPL (~350 lines)
   - Section 10: From REPL to Files (~300 lines)
   - Section 11: Practical Projects (REPL + Files) (~600 lines)
4. Create **~50 executable tutorial snippets + ~30 REPL transcripts** organized by section
5. Integrate REPL commands (`.help`, `.vars`, `.history`, `.retry`, `.edit`, `.capabilities`) throughout
6. Test all tutorial code with mlpy and REPL to ensure it executes correctly

**Weeks 4-5: Language Reference**
6. Write lexical-structure.rst + **create ML snippets** in `ml_snippets/language-reference/lexical/`
7. Write data-types.rst + **create ML snippets** in `ml_snippets/language-reference/types/`
8. Write expressions.rst + **create ML snippets** in `ml_snippets/language-reference/expressions/`
9. Write statements.rst + **create ML snippets** in `ml_snippets/language-reference/statements/`
10. Write functions.rst + **create ML snippets** in `ml_snippets/language-reference/functions/`
11. Write control-flow.rst + **create ML snippets** in `ml_snippets/language-reference/control-flow/`
12. Write exception-handling.rst + **create ML snippets** in `ml_snippets/language-reference/exceptions/`
13. Write destructuring.rst + **create ML snippets** in `ml_snippets/language-reference/destructuring/`
14. Write advanced-features.rst + **create ML snippets** in `ml_snippets/language-reference/advanced/`
15. Write capability-system.rst + **create ML snippets** in `ml_snippets/language-reference/capabilities/`

**Deliverables:**
- **Getting Started guide** (~500 lines, REPL-first approach)
- **Complete REPL Guide** (~1200 lines, comprehensive v2.3 reference)
- **Complete REPL-first tutorial from scratch** (~1800-2200 lines, 11 sections)
- **~50 executable tutorial snippets + ~30 REPL transcripts** demonstrating progressive learning
- **Complete language reference** (10 sections, ~4000 lines)
- **~50-70 executable language reference snippets** in organized directories
- **All syntax verified** against `src/mlpy/ml/grammar/ml.lark`
- **All builtins verified** against `src/mlpy/stdlib/builtin.py`
- **All REPL features verified** against `src/mlpy/cli/repl.py`
- All examples tested and verified to execute
- Cross-references established between REPL guide and tutorial
- **Zero reuse** of old tutorial content

---

### Phase 3: Standard Library (Week 6-7)

**Goals:** Document all stdlib modules + builtin with executable examples from scratch

**CRITICAL:** Delete ALL existing standard library documentation files - they are completely obsolete. This is a full rewrite consulting only implementation and test files.

**Tasks (IN ORDER):**

1. **DELETE** all existing stdlib documentation files in `docs/source/standard-library/`
2. **FIRST:** Rewrite `builtin-functions.rst` + **create ML snippets** in `ml_snippets/stdlib/builtin/`
   - Consult: `src/mlpy/stdlib/builtin.py` and `tests/ml_integration/ml_builtin/*.ml` (17 test files)
   - Document separately and first - fundamental to all ML programs
3. Rewrite `console.rst` + **create ML snippets** in `ml_snippets/stdlib/console/`
   - Consult: `src/mlpy/stdlib/console_module.py` and `tests/ml_integration/ml_stdlib/01_console_basic.ml`, `02_console_formatting.ml`
4. Rewrite `math.rst` + **create ML snippets** in `ml_snippets/stdlib/math/`
   - Consult: `src/mlpy/stdlib/math_bridge.py` and `tests/ml_integration/ml_stdlib/03_math_basic.ml`, `04_math_trigonometry.ml`, `05_math_advanced.ml`
5. Rewrite `datetime.rst` + **create ML snippets** in `ml_snippets/stdlib/datetime/`
   - Consult: `src/mlpy/stdlib/datetime_bridge.py` and `tests/ml_integration/ml_stdlib/09_datetime_objects.ml`, `10_datetime_arithmetic.ml`, `11_datetime_timezone.ml`
6. Rewrite `json.rst` + **create ML snippets** in `ml_snippets/stdlib/json/`
   - Consult: `src/mlpy/stdlib/json_bridge.py` and `tests/ml_integration/ml_stdlib/18_json_parse_stringify.ml`, `19_json_utilities.ml`
7. Rewrite `collections.rst` + **create ML snippets** in `ml_snippets/stdlib/collections/`
   - Consult: `src/mlpy/stdlib/collections_bridge.py` and `tests/ml_integration/ml_stdlib/12_collections_basic.ml`, `13_collections_advanced.ml`
8. Rewrite `functional.rst` + **create ML snippets** in `ml_snippets/stdlib/functional/`
   - Consult: `src/mlpy/stdlib/functional_bridge.py` and `tests/ml_integration/ml_stdlib/14_functional_composition.ml`, `15_functional_advanced.ml`
9. Rewrite `regex.rst` + **create ML snippets** in `ml_snippets/stdlib/regex/`
   - Consult: `src/mlpy/stdlib/regex_bridge.py` and `tests/ml_integration/ml_stdlib/06_regex_match_objects.ml`, `07_regex_flags.ml`, `08_regex_utilities.ml`
10. Rewrite `random.rst` + **create ML snippets** in `ml_snippets/stdlib/random/`
    - Consult: `src/mlpy/stdlib/random_bridge.py` and `tests/ml_integration/ml_stdlib/16_random_generation.ml`, `17_random_distributions.ml`
11. Write `file.rst` (NEW) + **create ML snippets** in `ml_snippets/stdlib/file/`
    - Consult: `src/mlpy/stdlib/file_bridge.py` and `tests/ml_integration/ml_stdlib/20_file_operations.ml`
12. Write `path.rst` (NEW) + **create ML snippets** in `ml_snippets/stdlib/path/`
    - Consult: `src/mlpy/stdlib/path_bridge.py` and `tests/ml_integration/ml_stdlib/21_path_operations.ml`
13. Write `http.rst` (NEW) + **create ML snippets** in `ml_snippets/stdlib/http/`
    - Consult: `src/mlpy/stdlib/http_bridge.py` and `tests/ml_integration/ml_stdlib/22_http_utilities.ml`
14. Document `string-methods.rst` + **create ML snippets** in `ml_snippets/stdlib/string/`
    - Note: NOT a module, document methods available on string primitive values
15. Document `array-methods.rst` + **create ML snippets** in `ml_snippets/stdlib/array/`
    - Note: NOT a module, document methods available on array primitive values

**Deliverables:**
- **OLD documentation deleted** - clean slate
- **Complete stdlib documentation from scratch** (14 sections, ~7500 lines)
- **~100-120 executable ML snippets** demonstrating each module/type
- Quick reference table for each module
- Capability requirements documented for all I/O operations
- All examples sourced from actual implementation and integration tests
- **Zero reuse** of old documentation content

---

### Phase 4: Integration Guide (Week 8)

**Goals:** Update for new APIs and decorator syntax with executable Python examples

**Tasks:**
1. Update python-integration.rst + **create Python snippets** in `py_snippets/integration/`
2. Write writing-stdlib-modules.rst (COMPLETE REWRITE) + **create Python snippets** in `py_snippets/stdlib-development/`
3. Update bridge-system.rst + **create Python snippets** in `py_snippets/bridge-system/`
4. Write sandbox-execution.rst (NEW) + **create Python snippets** in `py_snippets/sandbox/`
5. Write capability-management.rst (NEW) + **create Python snippets** in `py_snippets/capabilities/`
6. Write testing-ml-code.rst (NEW) + **create Python snippets** in `py_snippets/testing/`

**Deliverables:**
- Complete integration guide updates (~3000 lines)
- **~30-40 executable Python snippets** demonstrating integration patterns
- Crypto module example working and included in snippets
- All Python API examples tested and verified

---

### Phase 5: Developer Guide (Week 9-10)

**Goals:** Document evolved architecture and systems

**Tasks:**
1. Rewrite compilation-pipeline.rst (10 stages)
2. Rewrite security-analysis.rst (parallel analyzer, patterns)
3. Rewrite code-generation.rst (enhanced assignments)
4. Write test-runner.rst (NEW - unified test runner)
5. Update all architecture documents

**Deliverables:**
- Complete developer guide updates
- Architecture diagrams
- API reference (auto-generated)

---

### Phase 6: Verification & Polish (Week 11)

**Goals:** Build verification tool, final review, cross-references

**Tasks:**
1. **Build `docs/verify_snippets.py` verification tool:**
   - Discover and execute all ML snippets
   - Discover and execute all Python snippets
   - Generate verification report
   - Integrate into CI/CD pipeline
2. **Run verification tool on all snippets** and fix any broken examples
3. Review all documentation for consistency
4. Generate API reference from docstrings
5. Create cross-reference index
6. Build and test HTML/PDF output
7. Spell check and grammar review

**Deliverables:**
- **Automated snippet verification tool** (`docs/verify_snippets.py`)
- **100% snippet verification pass rate** (all ~150-200 snippets execute successfully)
- Complete, tested documentation
- CI/CD integration to prevent broken examples
- Published HTML documentation
- PDF documentation
- Migration complete

---

## Success Criteria

### Quality Metrics

1. **Completeness:**
   - ✅ All language features documented
   - ✅ All 11 stdlib modules documented
   - ✅ All builtin functions documented
   - ✅ All integration patterns documented

2. **Accuracy:**
   - ✅ All ML examples are executable snippets (not inlined)
   - ✅ All Python examples are executable snippets (not inlined)
   - ✅ 100% snippet verification pass rate
   - ✅ Grammar reference matches ml.lark
   - ✅ API documentation matches implementation
   - ✅ Capability requirements accurate

3. **Organization:**
   - ✅ Clear three-tier structure
   - ✅ Logical navigation
   - ✅ Comprehensive cross-references
   - ✅ Quick reference tables

4. **Usability:**
   - ✅ Search functionality
   - ✅ Syntax highlighting
   - ✅ Copy-paste ready examples
   - ✅ Mobile-friendly HTML

### Validation Process

1. **Automated Snippet Verification:**
   - **`docs/verify_snippets.py`** runs on all ML and Python snippets
   - All ML snippets must parse, transpile, and execute successfully
   - All Python snippets must run without errors
   - CI/CD pipeline runs verification on every commit
   - Zero tolerance for broken examples

2. **Technical Review:**
   - All API calls must match implementation
   - All grammar references must match ml.lark
   - All capability requirements verified
   - All decorators and syntax patterns accurate

3. **User Testing:**
   - New users can complete tutorial in <30 minutes
   - Integration developers can write module in <1 hour
   - Core developers can navigate architecture in <5 minutes

4. **Automated Documentation Checks:**
   - Sphinx build with no warnings
   - All links valid
   - All literalinclude paths resolve correctly
   - Spell check passes

---

## Resource Requirements

### Time Estimate

- **Total Effort:** 11 weeks (1 person full-time)
- **Phase 1:** 2 weeks (Foundation)
- **Phase 2:** 3 weeks (Tutorial + Language Reference)
- **Phase 3:** 2 weeks (Standard Library)
- **Phase 4:** 1 week (Integration Guide)
- **Phase 5:** 2 weeks (Developer Guide)
- **Phase 6:** 1 week (Verification & Polish)

### Tools Required

- **Sphinx:** Documentation generator (already configured)
- **reStructuredText:** Markup language
- **Pygments with ML Lexer:** Syntax highlighting for ML code
  - **Existing:** `docs/source/ml_lexer.py` - Full ML language lexer with 195 lines
  - **Features:** Keywords, operators, types, pattern matching, capabilities, comments, strings, numbers
  - **Integration:** Already registered in `docs/source/conf.py` via `lexers['ml'] = MLLexer()`
  - **Usage:** Use `:language: ml` in `.. literalinclude::` and `.. code-block::` directives
- **mlpy:** For executing and verifying all ML snippets
- **Custom Verification Tool:** `docs/verify_snippets.py` (to be built in Phase 6)
- **CI/CD Integration:** GitHub Actions or similar for automated verification

---

## Appendix: Quick Reference Template

### Module Documentation Template

```rst
============
Module Name
============

One-paragraph overview of the module and its purpose.

**Module:** ``module_name``
**Capabilities Required:** capability.type, capability.type2

Quick Reference
===============

.. list-table:: Function Reference
   :widths: 30 50 20
   :header-rows: 1

   * - Function
     - Description
     - Capability
   * - ``func1(arg)``
     - Brief description
     - cap.required
   * - ``func2(arg1, arg2)``
     - Brief description
     - cap.required

Installation
============

.. code-block:: ml

   import module_name;

Functions
=========

functionName()
--------------

.. code-block:: ml

   result = module_name.functionName(arg1, arg2);

Detailed description of what the function does.

**Parameters:**

- ``arg1`` (*type*) - Description of first argument
- ``arg2`` (*type*) - Description of second argument

**Returns:** (*type*) Description of return value

**Capability:** capability.required

**Examples:**

.. code-block:: ml

   // Example 1: Basic usage
   result = module_name.functionName(value1, value2);

   // Example 2: Advanced usage
   for (item in collection) {
       result = module_name.functionName(item, default);
   }

**Raises:**

- ``ValueError`` - When invalid argument provided

**See Also:**

- :func:`relatedFunction` - Related functionality
- :doc:`/user-guide/capability-system` - Capability system guide

Examples
========

Complete Example
----------------

.. code-block:: ml

   import module_name;

   function processData() {
       // Complete working example
       data = module_name.getData();
       result = module_name.process(data);
       return result;
   }

Best Practices
==============

✅ **Do:**
- Follow these patterns
- Use capabilities correctly

❌ **Don't:**
- Avoid these anti-patterns
- Don't bypass security
```

---

## Conclusion

This comprehensive documentation rewrite will transform the ML language documentation from its current outdated state into a world-class, **REPL-first**, three-tier documentation system that accurately reflects the mature, production-ready mlpy v2.0 implementation with its enterprise-grade REPL (v2.3).

**Revolutionary REPL-First Approach:**
- **Immediate experimentation:** Users start coding in seconds, not minutes
- **Interactive learning:** Every concept demonstrated in live REPL sessions
- **Progressive complexity:** REPL → Files → Projects
- **Professional tooling:** v2.3 features (sub-10ms execution, capability management, error recovery, editor integration)

By adopting **executable code snippets, REPL transcripts, and automated verification**, we ensure that documentation remains accurate, trustworthy, and maintainable as the language evolves.

**Key Benefits:**

1. **New Users** get REPL-first onboarding with immediate experimentation and instant feedback
2. **ML Language Users** get accurate, comprehensive language and stdlib documentation with REPL examples and reliable, copy-pasteable code
3. **Python Integrators** get up-to-date module development guides with decorator syntax and working code samples
4. **Core Developers** get accurate architecture and system documentation
5. **Everyone** benefits from improved organization, REPL-driven learning, navigation, and confidence in example accuracy
6. **Maintainers** get automated verification that prevents broken examples from entering documentation

**Innovation Highlights:**

✨ **REPL-First Learning:** Industry-leading approach to language onboarding
✨ **REPL v2.3 Documentation:** Comprehensive guide to enterprise-grade REPL features
✨ **Interactive Transcripts:** 50+ real REPL sessions showing development in action
✨ **Executable Examples:** 200+ verified code snippets that actually work
✨ **Automated Verification:** CI/CD integration ensures examples never break

**Next Steps:**

1. Review and approve this proposal
2. Assign documentation team/person
3. Begin Phase 1 (Foundation + REPL Guide)
4. Establish weekly review checkpoints
5. Target completion: 11 weeks from approval

---

**Approval Required:** YES
**Estimated Documentation LOC:** ~29,500 lines of RST documentation
  - Getting Started (REPL-first): ~500 lines
  - REPL Guide (comprehensive v2.3): ~1,200 lines
  - Tutorial (REPL-first): ~1,800-2,200 lines
  - Language Reference: ~4,000 lines
  - Standard Library: ~7,500 lines
  - Integration Guide: ~3,000 lines
  - Developer Guide: ~11,500 lines

**Estimated Snippet LOC:** ~5,000-7,000 lines of executable ML/Python code
  - ML code snippets: ~50 tutorial + ~150-200 other = ~200-250 snippets (~3,500-4,500 lines)
  - REPL transcripts: ~30 tutorial + ~20 getting started = ~50 transcripts (~1,000-1,500 lines)
  - Python snippets: ~30-40 integration examples (~500-1,000 lines)

**Estimated Total LOC:** ~34,500-36,500 lines
**NEW Components:** REPL-first learning approach, comprehensive REPL guide, REPL transcripts
**Impact:** HIGH - Critical for adoption, usability, and learning experience
