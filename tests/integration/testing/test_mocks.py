"""Tests for integration testing mock classes."""

import asyncio
import pytest
import time

from mlpy.integration.testing.mocks import (
    MockAsyncExecutor,
    MockREPLSession,
    MockCapabilityManager,
    MockExecutionRecord,
    MockFunctionCall,
    MockCapabilityViolation,
)
from mlpy.runtime.capabilities.context import CapabilityContext
from mlpy.runtime.capabilities.tokens import CapabilityToken, CapabilityConstraint


class TestMockAsyncExecutor:
    """Tests for MockAsyncExecutor."""

    def test_initialization(self):
        """Test mock executor initializes correctly."""
        mock = MockAsyncExecutor()

        assert len(mock.executions) == 0
        assert mock.should_fail is False
        assert mock.execution_delay == 0.0
        assert mock.mock_result == {"status": "success", "mock": True}

    @pytest.mark.anyio
    async def test_successful_execution(self):
        """Test successful mock execution."""
        mock = MockAsyncExecutor()

        result = await mock.execute("test code", timeout=5.0)

        assert result == {"status": "success", "mock": True}
        assert len(mock.executions) == 1
        assert mock.executions[0].ml_code == "test code"
        assert mock.executions[0].timeout == 5.0
        assert mock.executions[0].result == result

    @pytest.mark.anyio
    async def test_execution_failure(self):
        """Test mock execution failure."""
        mock = MockAsyncExecutor()
        mock.should_fail = True

        with pytest.raises(RuntimeError, match="Mock execution failure"):
            await mock.execute("failing code")

        assert len(mock.executions) == 1
        assert mock.executions[0].exception is not None

    @pytest.mark.anyio
    async def test_execution_delay(self):
        """Test execution delay simulation."""
        mock = MockAsyncExecutor()
        mock.execution_delay = 0.1

        start = time.perf_counter()
        await mock.execute("delayed code")
        end = time.perf_counter()

        assert (end - start) >= 0.1

    @pytest.mark.anyio
    async def test_custom_mock_result(self):
        """Test custom mock result."""
        mock = MockAsyncExecutor()
        mock.mock_result = {"custom": "result"}

        result = await mock.execute("code")

        assert result == {"custom": "result"}

    def test_reset(self):
        """Test reset clears state."""
        mock = MockAsyncExecutor()
        mock.executions.append(MockExecutionRecord(
            ml_code="test", timeout=None, context=None, timestamp=time.time()
        ))
        mock.should_fail = True
        mock.execution_delay = 0.5

        mock.reset()

        assert len(mock.executions) == 0
        assert mock.should_fail is False
        assert mock.execution_delay == 0.0

    def test_get_execution_count(self):
        """Test execution count tracking."""
        mock = MockAsyncExecutor()

        assert mock.get_execution_count() == 0

        mock.executions.append(MockExecutionRecord(
            ml_code="test", timeout=None, context=None, timestamp=time.time()
        ))

        assert mock.get_execution_count() == 1

    @pytest.mark.anyio
    async def test_get_last_execution(self):
        """Test getting last execution."""
        mock = MockAsyncExecutor()

        assert mock.get_last_execution() is None

        await mock.execute("first")
        await mock.execute("second")

        last = mock.get_last_execution()
        assert last is not None
        assert last.ml_code == "second"


class TestMockREPLSession:
    """Tests for MockREPLSession."""

    def test_initialization(self):
        """Test mock REPL session initializes correctly."""
        mock = MockREPLSession()

        assert len(mock.variables) == 0
        assert len(mock.executed_lines) == 0
        assert len(mock.function_calls) == 0
        assert mock.should_fail is False

    def test_execute(self):
        """Test mock code execution."""
        mock = MockREPLSession()

        result = mock.execute("let x = 5;")

        assert result.success is True
        assert result.value is None  # No function call in this code
        assert len(mock.executed_lines) == 1
        assert mock.executed_lines[0] == "let x = 5;"

    def test_execute_ml_line_alias(self):
        """Test execute_ml_line alias."""
        mock = MockREPLSession()

        result = mock.execute_ml_line("let y = 10;")

        assert result.success is True
        assert len(mock.executed_lines) == 1

    def test_execute_failure(self):
        """Test mock execution failure."""
        mock = MockREPLSession()
        mock.should_fail = True

        with pytest.raises(RuntimeError, match="Mock execution failure"):
            mock.execute("failing code")

    def test_call_function_validate_order(self):
        """Test calling validate_order function."""
        mock = MockREPLSession()

        result = mock.call_function("validate_order", (), {})

        assert result == {"valid": True}
        assert len(mock.function_calls) == 1
        assert mock.function_calls[0].function_name == "validate_order"

    def test_call_function_calculate_total(self):
        """Test calling calculate_total function."""
        mock = MockREPLSession()

        result = mock.call_function("calculate_total", (), {})

        assert result == 100.50

    def test_call_function_double(self):
        """Test calling double function."""
        mock = MockREPLSession()

        result = mock.call_function("double", (5,), {})

        assert result == 10

    def test_call_function_add(self):
        """Test calling add function."""
        mock = MockREPLSession()

        result = mock.call_function("add", (3, 7), {})

        assert result == 10

    def test_call_function_unknown(self):
        """Test calling unknown function."""
        mock = MockREPLSession()

        result = mock.call_function("unknown", (), {})

        assert result is None

    def test_reset(self):
        """Test reset clears state."""
        mock = MockREPLSession()
        mock.variables["x"] = 5
        mock.executed_lines.append("let x = 5;")
        mock.function_calls.append(MockFunctionCall(
            function_name="test", args=(), kwargs={}, timestamp=time.time()
        ))
        mock.should_fail = True

        mock.reset()

        assert len(mock.variables) == 0
        assert len(mock.executed_lines) == 0
        assert len(mock.function_calls) == 0
        assert mock.should_fail is False

    def test_get_execution_count(self):
        """Test execution count tracking."""
        mock = MockREPLSession()

        assert mock.get_execution_count() == 0

        mock.execute("line 1")
        mock.execute("line 2")

        assert mock.get_execution_count() == 2

    def test_get_function_call_count(self):
        """Test function call count tracking."""
        mock = MockREPLSession()

        assert mock.get_function_call_count() == 0

        mock.call_function("func1", (), {})
        mock.call_function("func2", (), {})

        assert mock.get_function_call_count() == 2

    def test_cleanup(self):
        """Test cleanup alias for reset."""
        mock = MockREPLSession()
        mock.executed_lines.append("test")

        mock.cleanup()

        assert len(mock.executed_lines) == 0


class TestMockCapabilityManager:
    """Tests for MockCapabilityManager."""

    def test_initialization(self):
        """Test mock capability manager initializes correctly."""
        mock = MockCapabilityManager()

        assert len(mock.contexts) == 0
        assert len(mock.violations) == 0
        assert mock.current_context is None

    def test_set_and_get_context(self):
        """Test setting and getting context."""
        mock = MockCapabilityManager()
        context = CapabilityContext(
            name="test",
            parent_context=None
        )

        mock.set_context(context)

        assert mock.get_context() == context
        assert len(mock.contexts) == 1

    def test_multiple_contexts(self):
        """Test multiple context setting."""
        mock = MockCapabilityManager()

        context1 = CapabilityContext(name="ctx1", parent_context=None)
        context2 = CapabilityContext(name="ctx2", parent_context=None)

        mock.set_context(context1)
        mock.set_context(context2)

        assert mock.current_context == context2
        assert len(mock.contexts) == 2

    def test_record_violation(self):
        """Test recording capability violation."""
        mock = MockCapabilityManager()

        mock.record_violation("file", "/etc/passwd", "read")

        assert len(mock.violations) == 1
        assert mock.violations[0].capability_type == "file"
        assert mock.violations[0].pattern == "/etc/passwd"
        assert mock.violations[0].operation == "read"

    def test_clear_context(self):
        """Test clearing current context."""
        mock = MockCapabilityManager()
        context = CapabilityContext(name="test", parent_context=None)

        mock.set_context(context)
        assert mock.current_context is not None

        mock.clear_context()
        assert mock.current_context is None

    def test_reset(self):
        """Test reset clears all state."""
        mock = MockCapabilityManager()
        context = CapabilityContext(name="test", parent_context=None)

        mock.set_context(context)
        mock.record_violation("file", "/test", "write")

        mock.reset()

        assert len(mock.contexts) == 0
        assert len(mock.violations) == 0
        assert mock.current_context is None

    def test_get_violation_count(self):
        """Test violation count tracking."""
        mock = MockCapabilityManager()

        assert mock.get_violation_count() == 0

        mock.record_violation("file", "/test1", "read")
        mock.record_violation("network", "api.com", "http")

        assert mock.get_violation_count() == 2

    def test_has_capability_no_context(self):
        """Test has_capability with no context."""
        mock = MockCapabilityManager()

        assert mock.has_capability("file") is False

    def test_has_capability_with_context(self):
        """Test has_capability with granted capability."""
        mock = MockCapabilityManager()

        constraint = CapabilityConstraint(resource_patterns=["/data/*"])
        file_cap = CapabilityToken(capability_type="file", constraints=constraint)
        context = CapabilityContext(
            name="test",
            parent_context=None
        )
        context.add_capability(file_cap)

        mock.set_context(context)

        assert mock.has_capability("file") is True
        assert mock.has_capability("file", "/data/*") is True
        assert mock.has_capability("file", "/etc/*") is False
        assert mock.has_capability("network") is False
