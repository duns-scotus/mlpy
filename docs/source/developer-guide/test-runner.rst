Unified ML Test Runner
======================

The Unified ML Test Runner provides comprehensive end-to-end validation of the ML pipeline, testing everything from parsing to execution with detailed reporting and analysis.

Overview
--------

The test runner (``tests/ml_test_runner.py``) validates the complete ML transpilation pipeline across 36+ test files covering all language features, security scenarios, and edge cases.

**Key Features:**

* **End-to-End Pipeline Testing**: Validates all 10 pipeline stages
* **Comprehensive Test Coverage**: 36+ ML files across 4 categories
* **Matrix View**: Visual success/failure grid
* **Performance Metrics**: Timing and optimization analysis
* **JSON Output**: Machine-readable results for automation

Usage
-----

Basic Commands
~~~~~~~~~~~~~~

Run all tests with full pipeline::

    python tests/ml_test_runner.py --full

Parse-only testing::

    python tests/ml_test_runner.py --parse

Matrix view with detailed output::

    python tests/ml_test_runner.py --full --matrix --details

Category-specific testing::

    python tests/ml_test_runner.py --full --category legitimate_programs

Pipeline Stages
---------------

The test runner validates these 10 pipeline stages:

1. **Parse** - ML source code parsing with Lark grammar
2. **AST** - Abstract Syntax Tree generation
3. **AST_Valid** - AST structure validation
4. **Transform** - Code transformations and optimizations
5. **TypeCheck** - Static type analysis
6. **Security_Deep** - Advanced multi-pass security analysis
7. **Optimize** - Code optimization passes
8. **Security** - Parallel security threat detection
9. **CodeGen** - Python code generation with source maps
10. **Execution** - Sandbox execution with capability enforcement

Test Categories
---------------

Language Coverage (25 files)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tests core ML language features:

* **Control Flow**: if/elif/else, while, for, try/catch
* **Data Structures**: arrays, objects, comprehensive operations
* **Functions**: definitions, calls, parameters, advanced patterns
* **Mathematical Operations**: arithmetic, scientific computation
* **String Operations**: manipulation, formatting, validation
* **Standard Library**: integration and module testing

**Example Files:**

* ``comprehensive_array_operations.ml`` (758 lines)
* ``complex_algorithms_implementations.ml`` (794 lines)
* ``real_world_applications_simulation.ml`` (981 lines)

Malicious Programs (4 files)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Security threat validation:

* **Code Injection**: eval, exec, dangerous function calls
* **SQL Injection**: dynamic query construction attacks
* **Import Evasion**: dangerous module import attempts
* **Reflection Abuse**: class hierarchy traversal exploits

All malicious programs should be **blocked** (CodeGen/Execution fail).

Legitimate Programs (2 files)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Real-world application testing:

* ``data_analysis.ml`` - Statistical analysis pipeline
* ``web_scraper.ml`` - HTTP request and parsing simulation

Edge Cases (2 files)
~~~~~~~~~~~~~~~~~~~~~

Boundary condition testing:

* ``deep_nesting.ml`` - Deeply nested control structures
* ``unicode_attacks.ml`` - Unicode-based security attempts

Examples (3 files)
~~~~~~~~~~~~~~~~~~~

Documentation and capability demonstrations:

* ``capability_integration_demo.ml`` - Capability-based security
* ``standard_library_demo.ml`` - Complete stdlib showcase
* ``stdlib_simple_test.ml`` - Basic stdlib validation

Output Formats
--------------

Matrix View
~~~~~~~~~~~

Visual grid showing stage results::

    File                          Cat      Overall  Parse  AST  Security  CodeGen  Exec
    basic_features.ml            lang_c   +        +      +    +         +        +
    malicious_code.ml            mal_p    +        +      +    +         -        -

**Symbols:**
- ``+`` = Success
- ``X`` = Failure (file should pass but failed)
- ``-`` = Skipped (due to earlier failure)

Detailed Output
~~~~~~~~~~~~~~~

Per-file analysis with error messages::

    [1/36] basic_features.ml
        Parse: SUCCESS (0.05ms)
        Security: SUCCESS (0.14ms)
        CodeGen: SUCCESS (15.2ms)
        Overall: PASS

    [2/36] malicious_code.ml
        Security: BLOCKED (3 threats detected)
        CodeGen: SKIPPED (security failure)
        Overall: PASS (correctly blocked)

JSON Results
~~~~~~~~~~~~

Machine-readable output saved to ``ml_full_results.json``::

    {
      "timestamp": 1758894588.1585824,
      "total_files": 36,
      "results": [
        {
          "file_name": "basic_features.ml",
          "overall_result": "+",
          "security_threats": 0,
          "total_time_ms": 51.3
        }
      ]
    }

Performance Metrics
-------------------

Current Benchmarks
~~~~~~~~~~~~~~~~~~

**Overall Results** (as of January 2025):

* **Success Rate**: 94.4% (34/36 files)
* **Average Time**: 492ms per file
* **Total Coverage**: 11,478 lines of ML code

**Stage Success Rates**:

* Parse: 94.4% (34/36)
* Security_Deep: 94.4% (34/36)
* Security: 94.4% (34/36)
* CodeGen: 83.3% (30/36)
* Execution: 83.3% (30/36)

**Security Effectiveness**:

* Malicious Detection: 100% (4/4 blocked)
* False Positive Rate: 0% (0 legitimate programs flagged)

Integration with Development
----------------------------

Continuous Integration
~~~~~~~~~~~~~~~~~~~~~~

Add to CI pipeline::

    # .github/workflows/test.yml
    - name: Run ML Pipeline Tests
      run: |
        python tests/ml_test_runner.py --full --matrix
        if [ $? -ne 0 ]; then
          echo "Pipeline tests failed"
          exit 1
        fi

Pre-commit Hooks
~~~~~~~~~~~~~~~~

Validate changes before commit::

    #!/bin/bash
    # .git/hooks/pre-commit
    python tests/ml_test_runner.py --parse --category language_coverage
    if [ $? -ne 0 ]; then
      echo "ML parsing tests failed - commit blocked"
      exit 1
    fi

Performance Regression Detection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Monitor performance changes::

    # Compare with baseline
    python tests/ml_test_runner.py --full > current_results.txt
    python scripts/compare_performance.py baseline.txt current_results.txt

Adding New Tests
----------------

Test File Structure
~~~~~~~~~~~~~~~~~~~

Create new ML test files in appropriate directories::

    tests/ml_integration/
    ├── language_coverage/      # Core language features
    ├── malicious_programs/     # Security threats
    ├── legitimate_programs/    # Real applications
    └── edge_cases/            # Boundary conditions

**File Naming Convention:**

* Use descriptive names: ``comprehensive_array_operations.ml``
* Include complexity in filename: ``complex_algorithms_implementations.ml``
* Indicate purpose: ``malicious_sql_injection.ml``

Test Requirements
~~~~~~~~~~~~~~~~~

Each test file should:

1. **Include Category Comment**::

     // Language Coverage Test - Array Operations
     // Tests comprehensive array manipulation features

2. **Provide Realistic Examples**::

     // Real-world use case, not artificial test code
     function processUserData(users) {
         return users.filter(u => u.active).map(u => u.name);
     }

3. **Include Edge Cases**::

     // Test boundary conditions
     empty_array = [];
     large_array = range(0, 10000);

4. **Document Expected Behavior**::

     // Should transpile successfully and execute without errors
     // Expected output: processed user list

Debugging Failed Tests
----------------------

Common Issues
~~~~~~~~~~~~~

**Parse Failures:**

* Check ML syntax against grammar (``src/mlpy/ml/grammar/ml.lark``)
* Verify all language constructs are supported
* Look for typos in keywords (``funcion`` vs ``function``)

**Security Failures:**

* Review Security_Deep and Parallel analyzer logs
* Check for false positives in legitimate code
* Verify malicious code is properly blocked

**CodeGen Failures:**

* Check for missing visitor methods in PythonCodeGenerator
* Look for unsupported AST node types
* Verify abstract method implementations

**Execution Failures:**

* Check sandbox configuration and capabilities
* Verify generated Python syntax is valid
* Look for runtime import or dependency issues

Debugging Commands
~~~~~~~~~~~~~~~~~~

Run specific test with detailed output::

    python tests/ml_test_runner.py --full --details | grep -A 10 "failing_file.ml"

Test single pipeline stage::

    python -c "
    from tests.ml_test_runner import UnifiedMLTestRunner
    runner = UnifiedMLTestRunner()
    # Debug specific file
    "

Enable verbose logging::

    export ML_DEBUG=1
    python tests/ml_test_runner.py --full

Best Practices
--------------

Test Development
~~~~~~~~~~~~~~~~

1. **Start Simple**: Begin with basic language features
2. **Add Complexity Gradually**: Build up to real-world examples
3. **Include Security Cases**: Test both safe and dangerous patterns
4. **Performance Awareness**: Monitor test execution times
5. **Documentation**: Comment complex test scenarios

Quality Assurance
~~~~~~~~~~~~~~~~~

1. **Maintain 90%+ Success Rate**: Target high pipeline reliability
2. **Zero False Positives**: Legitimate code should not be blocked
3. **100% Malicious Detection**: All threats must be caught
4. **Performance Targets**: Sub-500ms average per file
5. **Comprehensive Coverage**: Test all language constructs

Troubleshooting
---------------

Common Solutions
~~~~~~~~~~~~~~~~

**"Abstract method not implemented" errors:**

* Add missing visitor methods to analyzer classes
* Check method signatures match parent class
* Implement for all AST node types

**"SecurityAnalyzer failed" errors:**

* Update context detection for new patterns
* Add safe contexts for demo/test code
* Refine threat detection patterns

**"Parse failed" errors:**

* Update ML grammar for new language features
* Check token definitions and precedence
* Verify transformer methods exist

**Performance issues:**

* Profile slow test files
* Check for infinite loops in analysis
* Optimize pattern matching regular expressions

Getting Help
~~~~~~~~~~~~

1. **Check Logs**: Enable detailed logging for diagnosis
2. **Review Documentation**: Check language reference and API docs
3. **Test Isolation**: Run single files to isolate issues
4. **Performance Profiling**: Use built-in timing analysis
5. **Security Analysis**: Examine threat detection details

The ML test runner provides comprehensive validation infrastructure ensuring the pipeline maintains production-level quality as new features are developed.