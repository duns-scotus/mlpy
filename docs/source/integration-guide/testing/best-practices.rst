Testing Best Practices
=====================

This guide provides comprehensive best practices for testing ML-integrated Python applications using the Integration Toolkit's testing utilities.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
--------

The ML Integration Toolkit provides three main testing approaches:

1. **High-Level Integration Testing** - Using IntegrationTestHelper
2. **Unit Testing with Mocks** - Using MockAsyncExecutor, MockREPLSession, MockCapabilityManager
3. **Performance Testing** - Using PerformanceTester

Choosing the Right Testing Approach
-----------------------------------

Use IntegrationTestHelper When
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Suitable for:**

- End-to-end integration tests
- Testing ML code execution in real scenarios
- User acceptance testing
- Testing capability propagation
- Verifying ML-Python data flow

**Example:**

.. code-block:: python

    from mlpy.integration.testing import IntegrationTestHelper

    async def test_order_processing():
        helper = IntegrationTestHelper()

        # Test real ML execution
        await helper.assert_async_execution(
            ml_code="""
                import json;
                order = json.parse(order_json);
                result = validate_order(order);
            """,
            expected_result={"valid": True}
        )

        helper.cleanup()

Use Mocks When
~~~~~~~~~~~~~

**Suitable for:**

- Unit testing business logic
- Fast, isolated tests
- Testing without ML dependencies
- CI/CD pipeline tests
- Testing edge cases and error conditions

**Example:**

.. code-block:: python

    from mlpy.integration.testing import MockAsyncExecutor

    async def test_validator_logic():
        mock = MockAsyncExecutor()
        mock.mock_result = {"valid": True, "errors": []}

        validator = OrderValidator(mock)
        result = await validator.validate(order_data)

        assert result["valid"] is True
        assert mock.get_execution_count() == 1

Use PerformanceTester When
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Suitable for:**

- Performance benchmarking
- Regression testing
- Optimization validation
- Scalability testing
- Identifying bottlenecks

**Example:**

.. code-block:: python

    from mlpy.integration.testing import PerformanceTester

    async def test_performance_threshold():
        tester = PerformanceTester()

        results = await tester.benchmark_async_execution(
            ml_code="result = process_data(large_dataset);",
            iterations=100
        )

        # Assert performance threshold
        assert results["mean"] < 0.1  # Less than 100ms

Test Organization
----------------

Directory Structure
~~~~~~~~~~~~~~~~~~

Organize tests by type and component:

.. code-block:: text

    tests/
    ├── unit/                          # Unit tests with mocks
    │   ├── test_validators.py
    │   ├── test_processors.py
    │   └── test_business_logic.py
    ├── integration/                   # Integration tests
    │   ├── test_async_execution.py
    │   ├── test_ml_callbacks.py
    │   └── test_capability_flow.py
    └── performance/                   # Performance tests
        ├── test_benchmarks.py
        └── test_scalability.py

Test Naming Conventions
~~~~~~~~~~~~~~~~~~~~~~

**Good naming:**

.. code-block:: python

    def test_validates_email_format()          # Descriptive, action-focused
    def test_calculates_discount_correctly()   # Clear expected behavior
    def test_handles_empty_array()             # Specific edge case

**Poor naming:**

.. code-block:: python

    def test1()                                # Not descriptive
    def test_function()                        # Unclear what is tested
    def test_something()                       # Too vague

Fixture Management
-----------------

Using Pytest Fixtures
~~~~~~~~~~~~~~~~~~~~

**Pattern 1: Session-scoped fixtures for heavy resources**

.. code-block:: python

    import pytest
    from mlpy.integration.testing import IntegrationTestHelper

    @pytest.fixture(scope="session")
    def integration_helper():
        """Shared helper for all tests in session."""
        helper = IntegrationTestHelper()
        yield helper
        helper.cleanup()

**Pattern 2: Function-scoped fixtures for isolation**

.. code-block:: python

    @pytest.fixture
    def helper():
        """Fresh helper for each test."""
        helper = IntegrationTestHelper()
        yield helper
        helper.cleanup()

    @pytest.fixture
    def mock_executor():
        """Fresh mock for each test."""
        mock = MockAsyncExecutor()
        yield mock
        mock.reset()

**Pattern 3: Parametrized fixtures for test scenarios**

.. code-block:: python

    @pytest.fixture(params=[
        ("valid_email", "user@example.com", True),
        ("invalid_email", "not-an-email", False),
        ("empty_email", "", False),
    ])
    def email_test_case(request):
        """Provides email validation test cases."""
        return request.param

Async Testing Patterns
----------------------

Basic Async Test
~~~~~~~~~~~~~~~

.. code-block:: python

    import pytest

    @pytest.mark.anyio
    async def test_async_execution():
        """Test async ML execution."""
        from mlpy.integration.async_executor import async_ml_execute

        result = await async_ml_execute("result = 42;")

        assert result.success is True
        assert result.value == 42

Multiple Async Operations
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    @pytest.mark.anyio
    async def test_multiple_async_operations(helper):
        """Test multiple async executions."""
        # Execute sequentially
        await helper.assert_async_execution("result = 1;", expected_result=1)
        await helper.assert_async_execution("result = 2;", expected_result=2)

        # Verify history
        history = helper.get_execution_history()
        assert len(history) == 2

Concurrent Async Testing
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    @pytest.mark.anyio
    async def test_concurrent_execution():
        """Test concurrent ML executions."""
        import asyncio
        from mlpy.integration.async_executor import async_ml_execute

        # Execute concurrently
        tasks = [
            async_ml_execute("result = 1;"),
            async_ml_execute("result = 2;"),
            async_ml_execute("result = 3;"),
        ]

        results = await asyncio.gather(*tasks)

        assert all(r.success for r in results)
        assert [r.value for r in results] == [1, 2, 3]

Mock Testing Patterns
--------------------

Mocking Async Execution
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from mlpy.integration.testing import MockAsyncExecutor

    async def test_with_mock_executor():
        """Test using mock async executor."""
        mock = MockAsyncExecutor()
        mock.mock_result = {"status": "success", "data": [1, 2, 3]}

        # Use mock in application code
        processor = DataProcessor(executor=mock)
        result = await processor.process()

        # Verify mock was called
        assert mock.get_execution_count() == 1
        assert mock.get_last_execution().ml_code.startswith("process")

Mocking REPL Sessions
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from mlpy.integration.testing import MockREPLSession

    def test_with_mock_repl():
        """Test using mock REPL session."""
        mock = MockREPLSession()

        # Define ML functions
        mock.execute("function double(x) { return x * 2; }")

        # Call functions
        result = mock.call_function("double", (5,), {})

        # Verify behavior
        assert result == 10
        assert mock.get_execution_count() == 1
        assert mock.get_function_call_count() == 1

Simulating Failures
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def test_error_handling():
        """Test error handling with mock failures."""
        mock = MockAsyncExecutor()
        mock.should_fail = True

        # Test error handling
        with pytest.raises(RuntimeError, match="Mock execution failure"):
            await my_function(mock)

Performance Testing Patterns
---------------------------

Basic Benchmarking
~~~~~~~~~~~~~~~~~

.. code-block:: python

    from mlpy.integration.testing import PerformanceTester

    @pytest.mark.anyio
    async def test_basic_benchmark():
        """Basic performance benchmark."""
        tester = PerformanceTester()

        results = await tester.benchmark_async_execution(
            ml_code="result = 42;",
            iterations=100
        )

        print(f"Mean: {results['mean'] * 1000:.2f}ms")
        print(f"Std Dev: {results['std_dev'] * 1000:.2f}ms")

Regression Testing
~~~~~~~~~~~~~~~~~

.. code-block:: python

    @pytest.mark.anyio
    async def test_performance_regression():
        """Test for performance regressions."""
        tester = PerformanceTester()

        results = await tester.benchmark_async_execution(
            ml_code="result = complex_calculation();",
            iterations=50
        )

        # Define acceptable performance threshold
        threshold_ms = 100
        actual_ms = results["mean"] * 1000

        assert actual_ms < threshold_ms, \
            f"Performance regression: {actual_ms:.2f}ms > {threshold_ms}ms"

Comparing Implementations
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    @pytest.mark.anyio
    async def test_optimization_impact():
        """Compare original vs optimized implementation."""
        tester = PerformanceTester()

        original_results = await tester.benchmark_async_execution(
            ml_code=original_implementation,
            iterations=50
        )

        optimized_results = await tester.benchmark_async_execution(
            ml_code=optimized_implementation,
            iterations=50
        )

        speedup = original_results["mean"] / optimized_results["mean"]

        print(f"Speedup: {speedup:.2f}x")
        assert speedup > 1.5  # At least 50% improvement

Error Handling and Edge Cases
-----------------------------

Testing Error Conditions
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    @pytest.mark.anyio
    async def test_invalid_ml_code():
        """Test handling of invalid ML code."""
        from mlpy.integration.async_executor import async_ml_execute

        result = await async_ml_execute("invalid syntax here")

        assert result.success is False
        assert result.error is not None
        assert "syntax" in result.error.lower()

Testing Edge Cases
~~~~~~~~~~~~~~~~~

.. code-block:: python

    @pytest.mark.parametrize("input_value,expected", [
        (0, 0),                    # Zero
        (-1, -2),                  # Negative
        (999999, 1999998),         # Large number
        (None, None),              # Null value
    ])
    def test_edge_cases(helper, input_value, expected):
        """Test edge cases with parametrize."""
        result = helper.call_ml_function("double", input_value)
        assert result == expected

Testing Capability Propagation
------------------------------

.. code-block:: python

    from mlpy.runtime.capabilities.context import CapabilityContext
    from mlpy.runtime.capabilities.tokens import CapabilityToken, CapabilityConstraint

    @pytest.mark.anyio
    async def test_capability_propagation():
        """Test that capabilities are properly propagated."""
        helper = IntegrationTestHelper()

        # Create capability context
        constraint = CapabilityConstraint(resource_patterns=["/data/*"])
        file_cap = CapabilityToken(capability_type="file", constraints=constraint)

        # Note: Capabilities are not enforced in test mode (security_enabled=False)
        session = helper.create_test_repl(capabilities=[file_cap])

        # Execute ML code that requires file capability
        ml_code = """
        import file;
        data = file.read("/data/test.txt");
        """

        result = session.execute_ml_line(ml_code)
        assert result.success is True

        helper.cleanup()

Test Coverage Best Practices
----------------------------

What to Test
~~~~~~~~~~~

**Essential Coverage:**

1. **Happy Path** - Normal, expected scenarios
2. **Error Conditions** - Invalid inputs, exceptions
3. **Edge Cases** - Boundary values, null/empty data
4. **Integration Points** - ML-Python data flow
5. **Performance** - Execution time, resource usage

**Example Coverage:**

.. code-block:: python

    class TestEmailValidator:
        """Complete test coverage for email validator."""

        def test_valid_email(self):
            """Happy path: valid email."""
            assert validate_email("user@example.com") is True

        def test_invalid_format(self):
            """Error condition: invalid format."""
            assert validate_email("not-an-email") is False

        def test_empty_string(self):
            """Edge case: empty input."""
            assert validate_email("") is False

        def test_null_value(self):
            """Edge case: null value."""
            assert validate_email(None) is False

        @pytest.mark.anyio
        async def test_performance(self):
            """Performance: validation speed."""
            results = await quick_benchmark("validate_email('test@test.com')")
            assert results["mean"] < 0.01  # Less than 10ms

Code Coverage Targets
~~~~~~~~~~~~~~~~~~~~

**Recommended coverage levels:**

- **Critical paths:** 100% coverage
- **Business logic:** 95%+ coverage
- **Integration code:** 90%+ coverage
- **Utility functions:** 85%+ coverage

**Measure coverage:**

.. code-block:: bash

    # Run tests with coverage
    pytest --cov=src/myapp --cov-report=html

    # View coverage report
    open htmlcov/index.html

Common Testing Anti-Patterns
----------------------------

Anti-Pattern 1: Testing Implementation Details
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Bad:**

.. code-block:: python

    def test_internal_state():
        """Tests internal implementation."""
        obj = MyClass()
        obj.process()
        # Testing private internal state
        assert obj._internal_counter == 5

**Good:**

.. code-block:: python

    def test_public_behavior():
        """Tests public behavior."""
        obj = MyClass()
        result = obj.process()
        # Testing observable behavior
        assert result == expected_result

Anti-Pattern 2: Overly Complex Tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Bad:**

.. code-block:: python

    def test_everything_at_once():
        """Tests too many things."""
        # Setup 50 lines of code
        # Test 10 different scenarios
        # 20 assertions
        ...

**Good:**

.. code-block:: python

    def test_single_behavior():
        """Tests one specific behavior."""
        result = process_data(input_data)
        assert result == expected_output

Anti-Pattern 3: Not Cleaning Up Resources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Bad:**

.. code-block:: python

    def test_without_cleanup():
        """Forgets to clean up."""
        helper = IntegrationTestHelper()
        helper.assert_callback_works(...)
        # No cleanup - resource leak!

**Good:**

.. code-block:: python

    @pytest.fixture
    def helper():
        """Ensures cleanup happens."""
        h = IntegrationTestHelper()
        yield h
        h.cleanup()

    def test_with_cleanup(helper):
        """Uses fixture for automatic cleanup."""
        helper.assert_callback_works(...)

Anti-Pattern 4: Flaky Tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Bad:**

.. code-block:: python

    def test_with_timing_dependency():
        """Depends on timing."""
        start_async_process()
        time.sleep(0.5)  # Might fail if slow
        assert process_complete()

**Good:**

.. code-block:: python

    @pytest.mark.anyio
    async def test_with_proper_await():
        """Uses proper async patterns."""
        result = await async_process()
        assert result.success is True

Continuous Integration
---------------------

CI/CD Configuration
~~~~~~~~~~~~~~~~~~

**GitHub Actions Example:**

.. code-block:: yaml

    name: Tests

    on: [push, pull_request]

    jobs:
      test:
        runs-on: ubuntu-latest

        steps:
        - uses: actions/checkout@v2

        - name: Set up Python
          uses: actions/setup-python@v2
          with:
            python-version: 3.12

        - name: Install dependencies
          run: |
            pip install pytest pytest-anyio pytest-cov
            pip install -e .

        - name: Run unit tests
          run: pytest tests/unit/ -v

        - name: Run integration tests
          run: pytest tests/integration/ -v

        - name: Run performance tests
          run: pytest tests/performance/ -v

        - name: Check coverage
          run: pytest --cov=src --cov-report=xml

        - name: Upload coverage
          uses: codecov/codecov-action@v2

Test Parallelization
~~~~~~~~~~~~~~~~~~~

**Run tests in parallel:**

.. code-block:: bash

    # Install pytest-xdist
    pip install pytest-xdist

    # Run with parallel workers
    pytest -n auto  # Auto-detect CPU count

    # Run specific number of workers
    pytest -n 4

Summary
-------

**Key Takeaways:**

1. ✅ **Choose the right tool**: Helper for integration, mocks for unit tests, tester for performance
2. ✅ **Organize tests** by type and component
3. ✅ **Use fixtures** for proper setup/teardown
4. ✅ **Test thoroughly**: happy path, errors, edge cases, performance
5. ✅ **Clean up resources** to prevent leaks
6. ✅ **Avoid anti-patterns** like testing implementation details
7. ✅ **Measure coverage** and aim for 90%+ on critical code
8. ✅ **Run tests in CI/CD** to catch regressions early

**Next Steps:**

- Review the :doc:`examples <../examples>` for practical demonstrations
- Check the :doc:`API Reference <../api/testing>` for detailed documentation
- Set up your test suite using these patterns
- Integrate tests into your CI/CD pipeline

.. seealso::

   - :doc:`Testing Examples <../../examples/integration/testing/README>`
   - :doc:`Integration Testing API <../api/integration-test-helper>`
   - :doc:`Mock Objects API <../api/mocks>`
   - :doc:`Performance Testing API <../api/performance-tester>`
