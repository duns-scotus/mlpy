# ML Integration Testing Examples

This directory contains comprehensive examples demonstrating how to use the ML Integration Toolkit's testing utilities for thorough, efficient testing of ML-integrated Python applications.

## Overview

The ML Integration Toolkit provides three main categories of testing utilities:

1. **IntegrationTestHelper** - High-level test assertions for async execution and callbacks
2. **Mock Objects** - Fast, isolated unit testing without actual ML execution
3. **PerformanceTester** - Statistical performance benchmarking

## Examples

### 1. Async Execution Testing (`test_async_execution_example.py`)

Demonstrates testing async ML code execution:

```python
from mlpy.integration.testing import IntegrationTestHelper

helper = IntegrationTestHelper()

# Test simple execution
await helper.assert_async_execution(
    ml_code="result = 2 + 2;",
    expected_result=4
)

# Track execution history
history = helper.get_execution_history()
```

**Key Features:**
- Testing simple and complex ML code
- Tracking multiple executions
- Execution timing verification
- String, array, and object operations

**Run Examples:**
```bash
pytest test_async_execution_example.py -v
```

### 2. Callback Testing (`test_callback_example.py`)

Demonstrates testing Python-to-ML callbacks:

```python
from mlpy.integration.testing import IntegrationTestHelper

helper = IntegrationTestHelper()
session = helper.create_test_repl()

# Define ML function
session.execute_ml_line("function double(x) { return x * 2; }")

# Test callback
helper.assert_callback_works(
    session=session,
    function_name="double",
    args=(5,),
    expected_result=10
)
```

**Key Features:**
- Simple and complex callback testing
- Multiple arguments and return values
- String manipulation and array processing
- Object manipulation and validation logic
- Business logic testing scenarios

**Run Examples:**
```bash
pytest test_callback_example.py -v
```

### 3. Mock-Based Testing (`test_mock_example.py`)

Demonstrates fast, isolated testing with mocks:

```python
from mlpy.integration.testing import MockAsyncExecutor, MockREPLSession

# Mock async executor
mock = MockAsyncExecutor()
mock.mock_result = {"status": "success", "value": 42}
result = await mock.execute("test code")

# Mock REPL session
mock_repl = MockREPLSession()
result = mock_repl.execute("let x = 5;")
assert result.success is True
```

**Key Features:**
- MockAsyncExecutor for async execution testing
- MockREPLSession for REPL simulation
- MockCapabilityManager for security testing
- Execution failure simulation
- State tracking and reset functionality

**Run Examples:**
```bash
pytest test_mock_example.py -v
```

### 4. Performance Benchmarking (`test_performance_example.py`)

Demonstrates performance testing and optimization:

```python
from mlpy.integration.testing import PerformanceTester, quick_benchmark

tester = PerformanceTester()

# Benchmark execution
results = await tester.benchmark_async_execution(
    ml_code="result = 2 + 2;",
    iterations=100
)

print(f"Mean: {results['mean'] * 1000:.2f}ms")
print(f"Median: {results['median'] * 1000:.2f}ms")

# Quick benchmark
results = await quick_benchmark("result = 42;")
```

**Key Features:**
- Statistical benchmarking (mean, median, std dev)
- Concurrent execution testing
- Callback overhead measurement
- Scalability testing
- Performance regression detection

**Run Examples:**
```bash
pytest test_performance_example.py -v -s
```

## Running All Examples

Run all examples together:

```bash
# Run all tests
pytest examples/integration/testing/ -v

# Run with output (for performance results)
pytest examples/integration/testing/ -v -s

# Run specific example
pytest examples/integration/testing/test_async_execution_example.py -v
```

## Test Fixtures

All examples use pytest fixtures for clean setup/teardown:

```python
@pytest.fixture
def helper(self):
    """Create a test helper and clean up after each test."""
    helper = IntegrationTestHelper()
    yield helper
    helper.cleanup()
```

## Best Practices

### 1. Use IntegrationTestHelper for High-Level Tests

**Good:**
```python
await helper.assert_async_execution(
    ml_code="result = calculate_total();",
    expected_result=100
)
```

**When to use:** End-to-end integration tests, user acceptance tests

### 2. Use Mocks for Unit Tests

**Good:**
```python
mock = MockAsyncExecutor()
mock.mock_result = {"valid": True}
result = await my_validator.validate(data)
```

**When to use:** Unit testing business logic, fast test execution

### 3. Use PerformanceTester for Benchmarks

**Good:**
```python
results = await tester.benchmark_async_execution(
    ml_code=optimized_code,
    iterations=100
)
assert results["mean"] < threshold
```

**When to use:** Performance regression tests, optimization validation

### 4. Always Clean Up Resources

**Good:**
```python
helper = IntegrationTestHelper()
try:
    # Run tests
    pass
finally:
    helper.cleanup()
```

Or use fixtures:
```python
@pytest.fixture
def helper(self):
    helper = IntegrationTestHelper()
    yield helper
    helper.cleanup()
```

### 5. Use Appropriate Iterations for Benchmarks

- **Quick tests:** 10-30 iterations
- **Standard benchmarks:** 50-100 iterations
- **Detailed analysis:** 100-1000 iterations

```python
# Quick check
results = await quick_benchmark(ml_code)

# Detailed benchmark
results = await tester.benchmark_async_execution(
    ml_code=ml_code,
    iterations=100
)
```

## Common Testing Patterns

### Testing Error Handling

```python
# Test execution failure
with pytest.raises(RuntimeError):
    await helper.assert_async_execution(
        ml_code="invalid syntax",
        expected_result=None
    )
```

### Testing Multiple Scenarios

```python
test_cases = [
    ("result = 1;", 1),
    ("result = 2;", 2),
    ("result = 3;", 3),
]

for ml_code, expected in test_cases:
    await helper.assert_async_execution(ml_code, expected)
```

### Comparing Performance

```python
original = await tester.benchmark_async_execution(original_code)
optimized = await tester.benchmark_async_execution(optimized_code)

speedup = original["mean"] / optimized["mean"]
assert speedup > 1.5  # At least 50% faster
```

## Dependencies

All examples require:
- `pytest` - Test framework
- `pytest-anyio` - Async test support
- `mlpy` - ML Integration Toolkit

Install with:
```bash
pip install pytest pytest-anyio
pip install -e .  # Install mlpy from source
```

## Further Reading

- [Integration Toolkit Documentation](../../../docs/source/integration-guide/)
- [Testing Best Practices Guide](../../../docs/source/integration-guide/testing/best-practices.rst)
- [API Reference](../../../docs/source/integration-guide/api/)

## Contributing

When adding new testing examples:

1. Follow the existing naming convention: `test_*_example.py`
2. Include comprehensive docstrings
3. Add examples to this README
4. Ensure all tests pass with `pytest -v`
5. Include both simple and complex usage examples
