"""Mock execution environments for testing the Integration Toolkit.

Provides mock implementations of core Integration Toolkit components
for isolated, fast unit testing.
"""

import asyncio
import time
from typing import Any, Optional, Dict, List
from dataclasses import dataclass, field

from mlpy.runtime.capabilities.context import CapabilityContext
from mlpy.runtime.capabilities.tokens import CapabilityToken


@dataclass
class MockExecutionRecord:
    """Record of a mock execution."""

    ml_code: str
    timeout: Optional[float]
    context: Optional[Dict[str, Any]]
    timestamp: float
    result: Any = None
    exception: Optional[Exception] = None


class MockAsyncExecutor:
    """Mock async executor for testing.

    This mock allows tests to control execution behavior (success/failure,
    delays, results) without actually executing ML code.

    Example:
        ```python
        mock = MockAsyncExecutor()
        mock.execution_delay = 0.1
        mock.should_fail = False

        result = await mock.execute("test code")
        assert result == {"status": "success", "mock": True}
        assert len(mock.executions) == 1
        ```
    """

    def __init__(self):
        """Initialize the mock executor."""
        self.executions: List[MockExecutionRecord] = []
        self.should_fail: bool = False
        self.execution_delay: float = 0.0
        self.mock_result: Any = {"status": "success", "mock": True}

    async def execute(
        self,
        ml_code: str,
        timeout: Optional[float] = None,
        context: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Any:
        """Mock execution.

        Args:
            ml_code: ML code to "execute"
            timeout: Execution timeout (ignored)
            context: Execution context
            **kwargs: Additional arguments

        Returns:
            Mock result or raises exception if should_fail is True

        Raises:
            RuntimeError: If should_fail is True
        """
        execution_record = MockExecutionRecord(
            ml_code=ml_code,
            timeout=timeout,
            context=context,
            timestamp=time.time(),
        )
        self.executions.append(execution_record)

        if self.execution_delay > 0:
            await asyncio.sleep(self.execution_delay)

        if self.should_fail:
            exc = RuntimeError("Mock execution failure")
            execution_record.exception = exc
            raise exc

        # Return mock result
        execution_record.result = self.mock_result
        return self.mock_result

    def reset(self):
        """Reset the mock executor state."""
        self.executions.clear()
        self.should_fail = False
        self.execution_delay = 0.0
        self.mock_result = {"status": "success", "mock": True}

    def get_execution_count(self) -> int:
        """Get total number of executions."""
        return len(self.executions)

    def get_last_execution(self) -> Optional[MockExecutionRecord]:
        """Get the most recent execution record."""
        return self.executions[-1] if self.executions else None


@dataclass
class MockFunctionCall:
    """Record of a mock function call."""

    function_name: str
    args: tuple
    kwargs: dict
    timestamp: float
    result: Any = None


@dataclass
class MockExecutionResult:
    """Mock result object that mimics AsyncMLResult for testing."""

    success: bool = True
    value: Any = None
    error: Optional[str] = None


class MockREPLSession:
    """Mock REPL session for testing.

    This mock simulates a REPL session without actually transpiling or
    executing ML code.

    Example:
        ```python
        mock = MockREPLSession()
        mock.execute("let x = 5;")
        result = mock.call_function("add", (3, 7), {})

        assert len(mock.executed_lines) == 1
        assert len(mock.function_calls) == 1
        ```
    """

    def __init__(self):
        """Initialize the mock REPL session."""
        self.variables: Dict[str, Any] = {}
        self.executed_lines: List[str] = []
        self.function_calls: List[MockFunctionCall] = []
        self.should_fail: bool = False
        self.python_namespace: Dict[str, Any] = {}  # Mock namespace for MLCallbackWrapper compatibility

    def execute(self, ml_code: str) -> MockExecutionResult:
        """Mock ML code execution.

        Args:
            ml_code: ML code to "execute"

        Returns:
            Mock execution result

        Raises:
            RuntimeError: If should_fail is True
        """
        self.executed_lines.append(ml_code)

        if self.should_fail:
            raise RuntimeError("Mock execution failure")

        # Simple function definition detection - add to python_namespace
        # This allows ml_callback to find the function
        if "function " in ml_code:
            # Extract function name (very simple parser for mock purposes)
            import re
            match = re.search(r'function\s+(\w+)', ml_code)
            if match:
                func_name = match.group(1)
                # Add a simple mock callable to python_namespace
                self.python_namespace[func_name] = lambda *args, **kwargs: None

        # Return a mock result that looks like AsyncMLResult
        # Extract any simple return value from ML code like "double(5);"
        # For function calls, call our mock call_function to get result
        import re
        match = re.search(r'(\w+)\((.*?)\)', ml_code)
        if match:
            func_name = match.group(1)
            # Call our own call_function to get mock result
            result_value = self.call_function(func_name, (), {})
            return MockExecutionResult(success=True, value=result_value)

        return MockExecutionResult(success=True, value=None)

    def execute_ml_line(self, ml_code: str) -> MockExecutionResult:
        """Alias for execute() to match MLREPLSession interface.

        Args:
            ml_code: ML code to execute

        Returns:
            Mock execution result
        """
        return self.execute(ml_code)

    def call_function(
        self, function_name: str, args: tuple, kwargs: dict, **options
    ) -> Any:
        """Mock function call.

        Args:
            function_name: Name of function to call
            args: Positional arguments
            kwargs: Keyword arguments
            **options: Additional options

        Returns:
            Mock result based on function name
        """
        call_record = MockFunctionCall(
            function_name=function_name,
            args=args,
            kwargs=kwargs,
            timestamp=time.time(),
        )

        # Return different mock results based on function name
        if function_name == "validate_order":
            result = {"valid": True}
        elif function_name == "calculate_total":
            result = 100.50
        elif function_name == "double":
            result = args[0] * 2 if args else 0
        elif function_name == "add":
            result = sum(args) if args else 0
        else:
            result = None

        call_record.result = result
        self.function_calls.append(call_record)

        return result

    def reset(self):
        """Reset the mock REPL session state."""
        self.variables.clear()
        self.executed_lines.clear()
        self.function_calls.clear()
        self.should_fail = False

    def get_execution_count(self) -> int:
        """Get total number of executions."""
        return len(self.executed_lines)

    def get_function_call_count(self) -> int:
        """Get total number of function calls."""
        return len(self.function_calls)

    def cleanup(self):
        """Cleanup method to match MLREPLSession interface."""
        self.reset()


@dataclass
class MockCapabilityViolation:
    """Record of a capability violation."""

    capability_type: str
    pattern: str
    operation: str
    timestamp: float


class MockCapabilityManager:
    """Mock capability manager for testing.

    This mock tracks capability contexts and violations without enforcing
    actual security restrictions.

    Example:
        ```python
        mock = MockCapabilityManager()
        context = CapabilityContext(name="test", capabilities=set())
        mock.set_context(context)

        current = mock.get_context()
        assert current.name == "test"
        ```
    """

    def __init__(self):
        """Initialize the mock capability manager."""
        self.contexts: List[CapabilityContext] = []
        self.violations: List[MockCapabilityViolation] = []
        self.current_context: Optional[CapabilityContext] = None

    def set_context(self, context: CapabilityContext):
        """Mock set context.

        Args:
            context: Capability context to set
        """
        self.contexts.append(context)
        self.current_context = context

    def get_context(self) -> Optional[CapabilityContext]:
        """Mock get context.

        Returns:
            Current capability context or None
        """
        return self.current_context

    def record_violation(
        self, capability_type: str, pattern: str, operation: str
    ):
        """Mock record violation.

        Args:
            capability_type: Type of capability violated
            pattern: Resource pattern
            operation: Operation that was attempted
        """
        violation = MockCapabilityViolation(
            capability_type=capability_type,
            pattern=pattern,
            operation=operation,
            timestamp=time.time(),
        )
        self.violations.append(violation)

    def clear_context(self):
        """Clear the current context."""
        self.current_context = None

    def reset(self):
        """Reset the mock capability manager state."""
        self.contexts.clear()
        self.violations.clear()
        self.current_context = None

    def get_violation_count(self) -> int:
        """Get total number of recorded violations."""
        return len(self.violations)

    def has_capability(
        self, capability_type: str, pattern: Optional[str] = None
    ) -> bool:
        """Check if current context has a capability.

        Args:
            capability_type: Type of capability to check
            pattern: Optional pattern to match

        Returns:
            True if capability is granted in current context
        """
        if not self.current_context:
            return False

        # Use the context's has_capability method
        if not self.current_context.has_capability(capability_type, check_parents=False):
            return False

        # If pattern specified, check it matches against resource_patterns list
        if pattern is not None:
            try:
                token = self.current_context.get_capability(capability_type, check_parents=False)
                # Check if pattern is in the token's constraints.resource_patterns list
                return pattern in token.constraints.resource_patterns
            except:
                return False

        return True
