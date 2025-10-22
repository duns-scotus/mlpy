"""Example: Using Mocks for Fast, Isolated Testing.

This example demonstrates how to use mock objects for unit testing
without requiring actual ML execution or REPL sessions.
"""

import pytest
import asyncio
from mlpy.integration.testing import (
    MockAsyncExecutor,
    MockREPLSession,
    MockCapabilityManager,
)


class TestMockAsyncExecutorExamples:
    """Examples using MockAsyncExecutor for fast testing."""

    def test_basic_mock_execution(self):
        """Test basic mock async execution."""
        mock = MockAsyncExecutor()

        # Configure mock
        mock.mock_result = {"status": "success", "value": 42}

        # Run async execution synchronously in test
        async def run_test():
            result = await mock.execute("test code")
            return result

        result = asyncio.run(run_test())

        assert result == {"status": "success", "value": 42}
        assert mock.get_execution_count() == 1

    def test_mock_execution_failure(self):
        """Test mock execution failure."""
        mock = MockAsyncExecutor()
        mock.should_fail = True

        async def run_test():
            await mock.execute("failing code")

        with pytest.raises(RuntimeError, match="Mock execution failure"):
            asyncio.run(run_test())

        # Execution was recorded even though it failed
        assert mock.get_execution_count() == 1

    def test_mock_execution_with_delay(self):
        """Test mock execution with simulated delay."""
        import time

        mock = MockAsyncExecutor()
        mock.execution_delay = 0.1  # 100ms delay

        async def run_test():
            start = time.perf_counter()
            await mock.execute("delayed code")
            end = time.perf_counter()
            return end - start

        duration = asyncio.run(run_test())

        assert duration >= 0.1
        assert mock.get_execution_count() == 1

    def test_tracking_multiple_executions(self):
        """Test tracking multiple mock executions."""
        mock = MockAsyncExecutor()

        async def run_test():
            await mock.execute("code 1")
            await mock.execute("code 2")
            await mock.execute("code 3")

        asyncio.run(run_test())

        assert mock.get_execution_count() == 3

        # Check individual executions
        executions = mock.executions
        assert executions[0].ml_code == "code 1"
        assert executions[1].ml_code == "code 2"
        assert executions[2].ml_code == "code 3"

    def test_custom_mock_results(self):
        """Test custom mock results for different scenarios."""
        mock = MockAsyncExecutor()

        async def run_test():
            # Test scenario 1: Simple value
            mock.mock_result = 100
            result1 = await mock.execute("scenario 1")

            # Test scenario 2: Complex object
            mock.mock_result = {"data": [1, 2, 3], "count": 3}
            result2 = await mock.execute("scenario 2")

            return result1, result2

        result1, result2 = asyncio.run(run_test())

        assert result1 == 100
        assert result2 == {"data": [1, 2, 3], "count": 3}


class TestMockREPLSessionExamples:
    """Examples using MockREPLSession for fast testing."""

    def test_basic_repl_execution(self):
        """Test basic REPL mock execution."""
        mock = MockREPLSession()

        result = mock.execute("let x = 5;")

        assert result.success is True
        assert len(mock.executed_lines) == 1
        assert mock.executed_lines[0] == "let x = 5;"

    def test_function_calls(self):
        """Test mocking ML function calls."""
        mock = MockREPLSession()

        # Test built-in mock functions
        result = mock.call_function("double", (5,), {})
        assert result == 10

        result = mock.call_function("add", (3, 7), {})
        assert result == 10

        # Check tracking
        assert mock.get_function_call_count() == 2

    def test_simulating_execution_flow(self):
        """Test simulating a complete execution flow."""
        mock = MockREPLSession()

        # Define functions
        mock.execute("function double(x) { return x * 2; }")
        mock.execute("function triple(x) { return x * 3; }")

        # Call functions
        result1 = mock.call_function("double", (5,), {})
        result2 = mock.call_function("triple", (5,), {})

        # Verify
        assert result1 == 10
        assert result2 == 15
        assert mock.get_execution_count() == 2
        assert mock.get_function_call_count() == 2

    def test_execution_failure_simulation(self):
        """Test simulating execution failures."""
        mock = MockREPLSession()
        mock.should_fail = True

        with pytest.raises(RuntimeError, match="Mock execution failure"):
            mock.execute("failing code")

    def test_reset_functionality(self):
        """Test resetting mock state."""
        mock = MockREPLSession()

        # Execute some code
        mock.execute("line 1")
        mock.execute("line 2")
        mock.call_function("test", (), {})

        assert mock.get_execution_count() == 2
        assert mock.get_function_call_count() == 1

        # Reset
        mock.reset()

        # Verify state is cleared
        assert mock.get_execution_count() == 0
        assert mock.get_function_call_count() == 0


class TestMockCapabilityManagerExamples:
    """Examples using MockCapabilityManager for testing security."""

    def test_capability_context_tracking(self):
        """Test tracking capability contexts."""
        from mlpy.runtime.capabilities.context import CapabilityContext

        mock = MockCapabilityManager()

        context = CapabilityContext(name="test", parent_context=None)
        mock.set_context(context)

        assert mock.get_context() == context
        assert len(mock.contexts) == 1

    def test_capability_checks(self):
        """Test capability checking with mock."""
        from mlpy.runtime.capabilities.context import CapabilityContext
        from mlpy.runtime.capabilities.tokens import (
            CapabilityToken,
            CapabilityConstraint,
        )

        mock = MockCapabilityManager()

        # Create context with file capability
        constraint = CapabilityConstraint(resource_patterns=["/data/*"])
        file_cap = CapabilityToken(capability_type="file", constraints=constraint)
        context = CapabilityContext(name="test", parent_context=None)
        context.add_capability(file_cap)

        mock.set_context(context)

        # Test capability checks
        assert mock.has_capability("file") is True
        assert mock.has_capability("file", "/data/*") is True
        assert mock.has_capability("file", "/etc/*") is False
        assert mock.has_capability("network") is False

    def test_violation_tracking(self):
        """Test tracking capability violations."""
        mock = MockCapabilityManager()

        # Record violations
        mock.record_violation("file", "/etc/passwd", "read")
        mock.record_violation("network", "api.example.com", "http")

        assert mock.get_violation_count() == 2

        violations = mock.violations
        assert violations[0].capability_type == "file"
        assert violations[0].pattern == "/etc/passwd"
        assert violations[1].capability_type == "network"

    def test_context_hierarchy(self):
        """Test managing context hierarchy."""
        from mlpy.runtime.capabilities.context import CapabilityContext

        mock = MockCapabilityManager()

        # Create parent and child contexts
        parent = CapabilityContext(name="parent", parent_context=None)
        child = CapabilityContext(name="child", parent_context=parent)

        # Track context switches
        mock.set_context(parent)
        mock.set_context(child)

        assert mock.current_context == child
        assert len(mock.contexts) == 2


def test_combining_mocks_in_test():
    """Example: Combining multiple mocks in a single test."""
    mock_executor = MockAsyncExecutor()
    mock_repl = MockREPLSession()
    mock_caps = MockCapabilityManager()

    # Configure mocks
    mock_executor.mock_result = {"status": "success"}
    mock_repl.execute("function test() { return 42; }")

    # Use mocks together
    async def run_test():
        result = await mock_executor.execute("test code")
        return result

    result = asyncio.run(run_test())

    # Verify interactions
    assert result == {"status": "success"}
    assert mock_executor.get_execution_count() == 1
    assert mock_repl.get_execution_count() == 1


def test_mock_for_unit_testing_business_logic():
    """Example: Using mocks to unit test business logic."""

    class OrderValidator:
        """Business logic that uses ML execution."""

        def __init__(self, executor):
            self.executor = executor

        async def validate_order(self, order_data):
            """Validate order using ML code."""
            ml_code = f"validate_order({order_data});"
            result = await self.executor.execute(ml_code)
            return result

    # Create mock executor
    mock_executor = MockAsyncExecutor()
    mock_executor.mock_result = {"valid": True, "errors": []}

    # Test business logic
    validator = OrderValidator(mock_executor)

    async def run_test():
        result = await validator.validate_order({"item": "book", "qty": 1})
        return result

    result = asyncio.run(run_test())

    # Verify
    assert result == {"valid": True, "errors": []}
    assert mock_executor.get_execution_count() == 1


if __name__ == "__main__":
    # Run with: pytest test_mock_example.py -v
    pytest.main([__file__, "-v"])
