# ML Language Documentation Rewrite Proposal

**Status:** Draft
**Created:** 2025-10-06
**Author:** Documentation Team
**Version:** 1.0

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

### Principle 3: Language Understanding Before Writing

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

### Principle 4: Automated Verification

**Rule:** A verification tool will be built to automatically test all code snippets.

**Planned Verification Tool:** `docs/verify_snippets.py`

**Functionality:**
- Discover all `.ml` snippets in `ml_snippets/` directory
- Run each snippet through complete pipeline: parse → transpile → execute
- Discover all `.py` snippets in `py_snippets/` directory
- Execute each Python snippet and verify it runs without errors
- Generate verification report with pass/fail status
- Integrate into CI/CD pipeline to prevent broken examples

**Usage:**
```bash
# Verify all snippets
python docs/verify_snippets.py

# Verify specific category
python docs/verify_snippets.py --category language-reference

# Verbose output with execution details
python docs/verify_snippets.py --verbose
```

**Benefits:**
- **Accuracy:** All examples guaranteed to work with current implementation
- **Maintainability:** Code changes that break examples trigger CI failures
- **Developer Confidence:** Documentation always reflects actual behavior
- **User Trust:** Examples are reliable and copy-pasteable

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
│   ├── getting-started.rst            # NEW: Installation, first program, REPL
│   ├── tutorial.rst                   # COMPLETE REWRITE: Delete old, write from scratch
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
    ├── testing/                       # NEW: Testing infrastructure
    │   ├── index.rst                  # Testing overview
    │   ├── unit-testing.rst           # NEW: Unit test patterns
    │   ├── integration-testing.rst    # NEW: ML integration test suite
    │   ├── test-runner.rst            # NEW: Unified test runner documentation
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

#### 1.1 Getting Started (NEW)

**Purpose:** Zero to first program in 10 minutes
**Length:** ~300 lines

**Content:**
- Installation (pip install mlpy)
- Verify installation (mlpy --version)
- First ML program (Hello World)
- Running ML files (mlpy run hello.ml)
- Interactive REPL basics
- Project initialization (mlpy init)
- Next steps (links to tutorial)

**Example Code Snippets:**
```ml
// hello.ml
function main() {
    print("Hello, ML!");
}
main();
```

---

#### 1.2 Tutorial (COMPLETE REWRITE)

**CRITICAL REQUIREMENT:** Delete existing `tutorial.rst` entirely - it contains language and builtin incompatibilities and cannot be salvaged.

**Purpose:** Comprehensive tutorial teaching ML programming from scratch
**Length:** ~1500-2000 lines
**Primary Sources:**
- **Grammar:** `src/mlpy/ml/grammar/ml.lark` - Source of truth for ML syntax
- **Integration Tests:** `tests/ml_integration/` - Examples of idiomatic ML code
- **Builtin Implementation:** `src/mlpy/stdlib/builtin.py` - Available builtin functions
- **DO NOT reference old tutorial** - complete rewrite required

**Why Complete Rewrite is Required:**
1. **Syntax Incompatibilities:** Old tutorial uses `catch` instead of `elif`, missing features like `elif`, incorrect exception syntax
2. **Builtin Incompatibilities:** Old tutorial may reference builtins that don't exist or use them incorrectly
3. **Grammar Mismatch:** ML grammar has evolved; old examples may not parse correctly
4. **Missing Features:** No coverage of arrow functions, destructuring, enhanced assignments, etc.
5. **Best Practices Changed:** Current idiomatic ML code differs from old patterns

**Tutorial Structure:**

**Section 1: Introduction to ML (~200 lines)**
- What is ML and why use it
- Installing mlpy
- Your first ML program
- Running ML code (mlpy run, mlpy compile)
- Interactive REPL basics

**Section 2: Basic Syntax (~300 lines)**
- Comments and code structure
- Variables and assignment
- Data types (numbers, strings, booleans)
- Basic operators
- print() for output
- **Source:** Study `src/mlpy/ml/grammar/ml.lark` for syntax rules
- **Examples:** From `tests/ml_integration/ml_core/` basic tests

**Section 3: Control Flow (~350 lines)**
- if statements
- elif clauses (newly implemented!)
- else clauses
- Comparison operators
- Logical operators (&&, ||, !)
- Ternary operator (condition ? true_val : false_val)
- **Source:** Review `tests/ml_integration/ml_core/08_control_structures.ml`
- **Examples:** Real control flow patterns from integration tests

**Section 4: Loops and Iteration (~300 lines)**
- while loops
- for loops (for item in collection)
- break and continue
- range() builtin for numeric iteration
- Iterating over arrays and objects
- **Source:** Review `tests/ml_integration/ml_core/12_for_loops.ml`
- **Builtins:** Use range() from `src/mlpy/stdlib/builtin.py`

**Section 5: Functions (~400 lines)**
- Function definitions
- Parameters and return values
- Arrow functions (fn syntax)
- Closures and scope
- Recursion examples
- Higher-order functions
- **Source:** Review `tests/ml_integration/ml_core/14_arrow_functions.ml`, `07_closures_functions.ml`
- **Examples:** fibonacci, factorial, map/filter patterns

**Section 6: Data Structures (~350 lines)**
- Arrays: creation, indexing, slicing
- Objects: creation, property access, methods
- Array methods (from builtin)
- Object methods (from builtin)
- Destructuring assignment
- **Source:** Review `tests/ml_integration/ml_core/15_destructuring.ml`
- **Builtins:** len(), keys(), values(), entries() from builtin.py

**Section 7: Working with Builtins (~300 lines)**
- Type checking with typeof()
- Type conversion: int(), float(), str()
- Collection operations: len(), range()
- Array utilities: map(), filter(), reduce()
- Object utilities: keys(), values(), entries()
- Math utilities: abs(), min(), max(), sum()
- **Source:** Comprehensive coverage from `src/mlpy/stdlib/builtin.py`
- **Examples:** From `tests/ml_integration/ml_builtin/` test files

**Section 8: Exception Handling (~250 lines)**
- try/except/finally blocks
- Throwing exceptions
- Error objects and messages
- Exception handling patterns
- **CRITICAL:** Use `except`, NOT `catch` (common mistake in old docs)
- **Source:** Review `tests/ml_integration/ml_core/16_exceptions_complete.ml`

**Section 9: Working with Modules (~300 lines)**
- Importing standard library modules
- Using console module for output
- Using math module for calculations
- Using json module for data
- Practical examples combining modules
- **Source:** Integration test examples using stdlib modules

**Section 10: Practical Projects (~500 lines)**
- **Project 1:** Number guessing game (control flow, loops, random)
- **Project 2:** Todo list manager (arrays, objects, functions)
- **Project 3:** Simple calculator (functions, operators, error handling)
- **Project 4:** Data analysis script (file I/O, collections, math)
- Each project builds on previous tutorial sections
- **All code must be tested and executable**

**Tutorial Development Process:**

1. **FIRST:** Read and study ML grammar (`src/mlpy/ml/grammar/ml.lark`)
2. **SECOND:** Review all integration tests in `tests/ml_integration/ml_core/`
3. **THIRD:** Study builtin implementation in `src/mlpy/stdlib/builtin.py`
4. **FOURTH:** Write tutorial sections using verified syntax and builtins
5. **FIFTH:** Create executable snippets in `docs/ml_snippets/tutorial/`
6. **SIXTH:** Test all tutorial code with mlpy to ensure it executes
7. **SEVENTH:** Verify tutorial teaches current best practices

**Code Snippet Organization:**
```
docs/ml_snippets/tutorial/
├── 01_introduction/
│   ├── hello_world.ml
│   └── first_program.ml
├── 02_basic_syntax/
│   ├── variables.ml
│   ├── data_types.ml
│   └── operators.ml
├── 03_control_flow/
│   ├── if_elif_else.ml
│   ├── ternary.ml
│   └── comparisons.ml
├── 04_loops/
│   ├── while_loop.ml
│   ├── for_loop.ml
│   └── range_iteration.ml
├── 05_functions/
│   ├── basic_function.ml
│   ├── arrow_function.ml
│   ├── closures.ml
│   └── recursion.ml
├── 06_data_structures/
│   ├── arrays.ml
│   ├── objects.ml
│   ├── slicing.ml
│   └── destructuring.ml
├── 07_builtins/
│   ├── typeof_usage.ml
│   ├── conversions.ml
│   ├── collections.ml
│   └── utilities.ml
├── 08_exceptions/
│   ├── try_except.ml
│   ├── finally_clause.ml
│   └── throwing.ml
├── 09_modules/
│   ├── console_examples.ml
│   ├── math_examples.ml
│   └── json_examples.ml
└── 10_projects/
    ├── guessing_game.ml
    ├── todo_list.ml
    ├── calculator.ml
    └── data_analysis.ml
```

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

##### 1.3.9 Capability System (NEW - ~500 lines)

**Content:**
- **Capability Declarations:** Requesting permissions
- **Capability Types:**
  - file.read, file.write, file.append, file.delete
  - path.read, path.write
  - network.http, network.https
  - console.write, console.error
- **Capability Patterns:** Fine-grained restrictions
- **Security Model:** How capabilities work

**Capability Examples:**
```ml
// Capability declaration
capability DataAccess {
    allow read "/data/*";
    allow write "/output/*";
}

capability NetworkAccess {
    allow network "https://api.example.com/*";
}

// Import with capabilities
import file;
import http;

// Operations automatically check capabilities
file.read("/data/input.txt");           // ✓ Allowed by pattern
file.write("/output/result.txt", data); // ✓ Allowed by pattern
file.write("/etc/passwd", data);        // ✗ DENIED - not in pattern
http.get("https://api.example.com/users"); // ✓ Allowed
http.get("https://evil.com/");             // ✗ DENIED - not in pattern
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

### TIER 3: Developer Guide

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

**Week 3: Tutorial (COMPLETE REWRITE)**
1. **DELETE** existing `tutorial.rst` entirely (language and builtin incompatibilities)
2. **Study sources:**
   - Read `src/mlpy/ml/grammar/ml.lark` for correct ML syntax
   - Review `tests/ml_integration/ml_core/` for idiomatic ML code patterns
   - Study `src/mlpy/stdlib/builtin.py` for available builtin functions
3. Write new tutorial.rst (10 sections, ~1500-2000 lines) + **create ML snippets** in `ml_snippets/tutorial/`
   - Section 1: Introduction to ML (~200 lines)
   - Section 2: Basic Syntax (~300 lines)
   - Section 3: Control Flow (~350 lines)
   - Section 4: Loops and Iteration (~300 lines)
   - Section 5: Functions (~400 lines)
   - Section 6: Data Structures (~350 lines)
   - Section 7: Working with Builtins (~300 lines)
   - Section 8: Exception Handling (~250 lines)
   - Section 9: Working with Modules (~300 lines)
   - Section 10: Practical Projects (~500 lines)
4. Create **~40 executable tutorial snippets** organized by section
5. Test all tutorial code with mlpy to ensure it executes correctly

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
- **Complete tutorial from scratch** (~1500-2000 lines, 10 sections)
- **~40 executable tutorial snippets** demonstrating progressive learning
- **Complete language reference** (10 sections, ~4000 lines)
- **~50-70 executable language reference snippets** in organized directories
- **All syntax verified** against `src/mlpy/ml/grammar/ml.lark`
- **All builtins verified** against `src/mlpy/stdlib/builtin.py`
- All examples tested and verified to execute
- Cross-references established
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

This comprehensive documentation rewrite will transform the ML language documentation from its current outdated state into a world-class, three-tier documentation system that accurately reflects the mature, production-ready mlpy v2.0 implementation.

By adopting executable code snippets and automated verification, we ensure that documentation remains accurate, trustworthy, and maintainable as the language evolves.

**Key Benefits:**

1. **Users** get accurate, comprehensive language and stdlib documentation with reliable, copy-pasteable examples
2. **Integrators** get up-to-date module development guides with decorator syntax and working code samples
3. **Developers** get accurate architecture and system documentation
4. **Everyone** benefits from improved organization, navigation, and confidence in example accuracy
5. **Maintainers** get automated verification that prevents broken examples from entering documentation

**Next Steps:**

1. Review and approve this proposal
2. Assign documentation team/person
3. Begin Phase 1 (Foundation)
4. Establish weekly review checkpoints
5. Target completion: 11 weeks from approval

---

**Approval Required:** YES
**Estimated Documentation LOC:** ~27,000 lines of RST documentation (includes ~2000 line tutorial)
**Estimated Snippet LOC:** ~3,500-5,500 lines of executable ML/Python code snippets (~40 tutorial + 150-200 other snippets)
**Estimated Total LOC:** ~30,500-32,500 lines
**Impact:** HIGH - Critical for adoption and usability
