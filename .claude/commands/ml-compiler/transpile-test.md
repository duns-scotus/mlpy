# ML → Python Transpilation Testing

Comprehensive testing of the ML to Python transpilation pipeline with focus on correctness, security, and performance.

Usage: `/ml-compiler:transpile-test [test-category]`

## Test Categories

### 1. Basic Syntax Testing
**Focus:** Core ML language features transpile correctly to Python

#### Syntax Coverage
- **Variables & Literals**: Numbers, strings, booleans, arrays, objects
- **Functions**: Definition, parameters, return statements, recursion
- **Control Flow**: if/else, while loops, for loops, break/continue
- **Expressions**: Binary operations, unary operations, member access, function calls
- **Operators**: Arithmetic (+, -, *, /, %), comparison (<, >, <=, >=, ==, !=), logical (&&, ||, !)

#### Example Test Cases
```ml
// Basic function with control flow
function fibonacci(n) {
    if (n <= 1) {
        return n;
    } else {
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
}

// Object and array manipulation
function process_data(items) {
    result = {"processed": [], "count": 0};
    for (item in items) {
        if (item.value > 0) {
            result.processed = result.processed + [item.value * 2];
            result.count = result.count + 1;
        }
    }
    return result;
}
```

### 2. Security Features Testing
**Focus:** Security-specific ML features transpile with proper security enforcement

#### Security Feature Coverage
- **Capability Statements**: `capability FileAccess { ... }` → Python context managers
- **Security Annotations**: Function-level security requirements
- **Safe Built-ins**: Dangerous operations properly blocked or wrapped
- **Import Control**: Restricted imports properly handled

#### Example Test Cases
```ml
capability FileAccess {
    resource "data/*.json";
    allow read;
}

import math; // Should generate safe import

function secure_calculation(data_file) {
    // Should require FileAccess capability
    content = read_file(data_file);
    return math.sqrt(content.value);  // Should use math_safe
}
```

### 3. Advanced Features Testing
**Focus:** Complex ML language constructs and edge cases

#### Advanced Feature Coverage
- **Nested Scopes**: Complex variable scoping rules
- **Complex Expressions**: Deeply nested expressions with operator precedence
- **Error Handling**: ML error constructs → Python exception handling
- **Type Annotations**: Optional type hints → Python type annotations
- **Lambda Expressions**: Anonymous functions (if implemented)

#### Example Test Cases
```ml
function complex_processing(data: Array, filter_func, transform_func) {
    return data
        .filter(filter_func)
        .map(transform_func)
        .reduce((acc, val) => acc + val, 0);
}
```

### 4. Edge Cases & Error Conditions
**Focus:** Error handling, boundary conditions, and performance limits

#### Edge Case Coverage
- **Empty Programs**: Minimal ML code → Valid Python
- **Large Programs**: Stress testing with thousands of functions
- **Deep Nesting**: Heavily nested expressions and control structures
- **Unicode Handling**: International characters in identifiers and strings
- **Syntax Errors**: Graceful error reporting with source positions

## Transpilation Process Validation

### 1. Parse Phase Testing
```bash
# Test ML parsing with various syntax patterns
mlpy parse test_cases/basic_syntax.ml --format json
mlpy parse test_cases/security_features.ml --format tree
mlpy parse test_cases/edge_cases.ml --format json
```

### 2. Security Analysis Testing
```bash
# Verify security analysis catches dangerous patterns
mlpy audit test_cases/dangerous_code.ml --format json
mlpy audit test_cases/capability_required.ml --format text
```

### 3. Code Generation Testing
```bash
# Test transpilation with various options
mlpy transpile test_cases/comprehensive.ml --sourcemap --profile
mlpy transpile test_cases/large_program.ml --no-strict
```

### 4. Execution Validation
```bash
# Verify generated Python code executes correctly
python generated_code.py
python -m pytest generated_test_suite.py
```

## Validation Steps

### 1. Syntax Correctness
- **Python Syntax Valid**: Generated code passes `python -m py_compile`
- **Indentation Correct**: Proper Python indentation for all control structures
- **Identifier Safety**: Python keywords properly escaped (e.g., `class` → `ml_class`)
- **String Escaping**: Special characters properly escaped in Python strings

### 2. Semantic Correctness
- **Function Signatures**: Correct parameter handling and return statements
- **Variable Scoping**: ML variable scoping correctly implemented in Python
- **Expression Evaluation**: Complex expressions evaluate to same results
- **Control Flow**: if/else, loops, and function calls execute correctly

### 3. Security Enforcement
- **Capability Requirements**: Functions requiring capabilities properly wrapped
- **Dangerous Operations**: eval, exec, dangerous imports properly blocked
- **Safe Built-ins**: Math, file, network operations use safe implementations
- **Import Restrictions**: Only approved modules can be imported

### 4. Source Map Accuracy
- **Line Mapping**: ML source lines correctly map to Python lines
- **Column Mapping**: Accurate character position mapping for debugging
- **Function Mapping**: ML functions map to Python function definitions
- **Error Mapping**: Runtime errors map back to original ML source

### 5. Performance Characteristics
- **Transpilation Speed**: <10ms for typical programs (<1000 lines)
- **Memory Usage**: <128MB peak memory during transpilation
- **Generated Code Size**: Reasonable Python code size (typically 1.5-2x ML size)
- **Cache Effectiveness**: 90%+ cache hit rate for repeated transpilations

## Test Suite Organization

### Unit Tests (`tests/unit/transpilation/`)
```
test_basic_syntax.py        # Core language features
test_expressions.py         # Expression handling
test_control_flow.py        # if/else, loops, functions
test_security_features.py   # Capability statements, annotations
test_error_handling.py      # Error conditions and recovery
```

### Integration Tests (`tests/integration/transpilation/`)
```
test_full_pipeline.py       # Complete ML → Python pipeline
test_source_maps.py         # Source map generation and accuracy
test_security_integration.py # Security analysis + code generation
test_performance.py         # Performance benchmarking
```

### End-to-End Tests (`tests/e2e/transpilation/`)
```
test_real_programs.py       # Real-world ML programs
test_large_codebases.py     # Large program stress testing
test_regression.py          # Prevent regression in transpilation
```

## Test Data Organization

### Test Cases (`test_cases/`)
```
basic_syntax/               # Simple language features
  ├── functions.ml
  ├── variables.ml
  ├── control_flow.ml
  └── expressions.ml

security_features/          # Security-specific features
  ├── capabilities.ml
  ├── safe_imports.ml
  ├── dangerous_code.ml
  └── security_annotations.ml

advanced_features/          # Complex language constructs
  ├── nested_scopes.ml
  ├── complex_expressions.ml
  ├── type_annotations.ml
  └── error_handling.ml

edge_cases/                 # Boundary conditions
  ├── empty_program.ml
  ├── unicode_identifiers.ml
  ├── deep_nesting.ml
  └── large_program.ml
```

## Automated Testing Pipeline

### 1. Syntax Validation
```python
def test_python_syntax_valid():
    """Ensure all generated Python code has valid syntax."""
    for ml_file in test_cases:
        python_code = transpile_ml_file(ml_file)
        assert python_syntax_valid(python_code)
```

### 2. Execution Testing
```python
def test_execution_equivalence():
    """Verify ML and Python execution produce same results."""
    for test_case in execution_test_cases:
        ml_result = execute_ml(test_case.ml_code)
        py_result = execute_python(transpile(test_case.ml_code))
        assert ml_result == py_result
```

### 3. Security Validation
```python
def test_security_enforcement():
    """Verify security features properly enforced."""
    for security_test in security_test_cases:
        python_code = transpile_ml_file(security_test.ml_file)
        assert capability_enforcement_present(python_code)
        assert no_dangerous_operations(python_code)
```

### 4. Performance Benchmarking
```python
def test_transpilation_performance():
    """Ensure transpilation meets performance targets."""
    for benchmark in performance_benchmarks:
        start_time = time.time()
        transpile_ml_file(benchmark.ml_file)
        duration = time.time() - start_time
        assert duration < benchmark.max_duration
```

## Continuous Integration

### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
- repo: local
  hooks:
    - id: transpilation-tests
      name: ML Transpilation Tests
      entry: python -m pytest tests/unit/transpilation/ -x
      language: system
      files: '^(src/mlpy/ml/|tests/unit/transpilation/).*\.py$'
```

### CI Pipeline Integration
```yaml
# .github/workflows/transpilation-tests.yml
- name: Run Transpilation Test Suite
  run: |
    python -m pytest tests/unit/transpilation/ -v --cov=src/mlpy/ml/
    python -m pytest tests/integration/transpilation/ -v
    python -m pytest tests/e2e/transpilation/ -x
```

## Report Generation

### Test Report Format
```
📊 ML Transpilation Test Report
═══════════════════════════════

✅ Basic Syntax Tests:        45/45 passed (100%)
✅ Security Features Tests:   23/23 passed (100%)
✅ Advanced Features Tests:   18/20 passed (90%)
❌ Edge Cases Tests:          12/15 passed (80%)

🔍 Failed Tests:
- test_unicode_identifiers: Unicode handling needs improvement
- test_deep_nesting: Stack overflow on deeply nested expressions
- test_large_program: Memory usage exceeds 128MB limit

🚀 Performance Metrics:
- Average transpilation time: 2.3ms (target: <10ms) ✅
- Peak memory usage: 89MB (target: <128MB) ✅
- Cache hit rate: 94% (target: >90%) ✅

🛡️ Security Validation:
- Capability enforcement: 100% coverage ✅
- Dangerous operation blocking: 100% coverage ✅
- Safe built-in usage: 100% coverage ✅

📍 Source Map Accuracy:
- Line mapping accuracy: 98.7% ✅
- Column mapping accuracy: 95.2% ✅
- Function mapping accuracy: 100% ✅
```

## Next Steps

### Test Coverage Expansion
- Add more complex real-world ML programs
- Expand edge case coverage for error conditions
- Add stress testing for very large codebases
- Implement regression testing for each sprint

### Performance Optimization
- Profile transpilation bottlenecks
- Optimize hot paths in code generation
- Implement incremental transpilation for large programs
- Add parallel transpilation for multiple files

### Security Hardening
- Expand exploit prevention test cases
- Add penetration testing for capability system
- Validate sandbox integration security
- Test security boundary enforcement

**Focus: Comprehensive validation ensuring the ML → Python transpilation pipeline is correct, secure, and performant.**