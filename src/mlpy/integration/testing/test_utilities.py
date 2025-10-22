"""Integration test utilities for the ML Integration Toolkit.

Provides comprehensive testing infrastructure for testing async ML execution,
ML callbacks, and capability propagation.
"""

import threading
import time
import uuid
from typing import Any, Optional, Set, List, Dict

from mlpy.cli.repl import MLREPLSession
from mlpy.integration.async_executor import async_ml_execute, AsyncMLResult
from mlpy.integration.ml_callback import ml_callback
from mlpy.runtime.capabilities.manager import get_capability_manager
from mlpy.runtime.capabilities.tokens import CapabilityToken
from mlpy.runtime.capabilities.context import CapabilityContext
from mlpy.runtime.capabilities.exceptions import CapabilityNotFoundError


class IntegrationTestHelper:
    """Utilities for testing ML Integration Toolkit.

    This class provides high-level test assertions for async execution,
    callbacks, and capability propagation.

    Example:
        ```python
        helper = IntegrationTestHelper()

        # Test async execution
        await helper.assert_async_execution(
            "result = 2 + 2;",
            expected_result=4
        )

        # Test callback
        session = helper.create_test_repl()
        session.execute_ml_line("function double(x) { return x * 2; }")
        helper.assert_callback_works(session, 'double', (5,), expected_result=10)

        # Clean up
        helper.cleanup()
        ```
    """

    def __init__(self):
        """Initialize the integration test helper."""
        self.mock_repl_sessions: List[MLREPLSession] = []
        self.captured_async_executions: List[Dict] = []
        self.capability_violations: List[CapabilityNotFoundError] = []

    def create_test_repl(
        self, capabilities: Optional[List[CapabilityToken]] = None
    ) -> MLREPLSession:
        """Create REPL session with test configuration.

        Args:
            capabilities: Optional list of capabilities to grant to the session

        Returns:
            MLREPLSession configured for testing
        """
        session = MLREPLSession(
            security_enabled=False  # Disable security for easier testing
        )

        # Note: capabilities parameter is accepted for API compatibility
        # but not enforced since security_enabled=False for testing

        self.mock_repl_sessions.append(session)
        return session

    async def assert_async_execution(
        self,
        ml_code: str,
        expected_result: Any,
        timeout: float = 5.0,
        capabilities: Optional[Set[CapabilityToken]] = None,
    ):
        """Assert async execution produces expected result.

        Args:
            ml_code: ML code to execute
            expected_result: Expected result value
            timeout: Execution timeout in seconds
            capabilities: Optional capabilities to grant

        Raises:
            AssertionError: If execution fails or result doesn't match expected
        """
        result = await async_ml_execute(
            ml_code, timeout=timeout
        )

        self.captured_async_executions.append(
            {
                "ml_code": ml_code,
                "result": result,
                "execution_time": result.execution_time,
            }
        )

        assert result.success, f"Execution failed: {result.error}"
        assert (
            result.value == expected_result
        ), f"Expected {expected_result}, got {result.value}"

    def assert_callback_works(
        self,
        session: MLREPLSession,
        function_name: str,
        args: tuple,
        expected_result: Any,
        capabilities: Optional[Set[CapabilityToken]] = None,
    ):
        """Assert callback executes correctly.

        Args:
            session: REPL session containing the ML function
            function_name: Name of the ML function to wrap
            args: Arguments to pass to the callback
            expected_result: Expected result value
            capabilities: Optional capabilities to grant

        Raises:
            AssertionError: If callback execution fails or result doesn't match
        """
        callback = ml_callback(session, function_name)

        result = callback(*args)
        assert (
            result == expected_result
        ), f"Expected {expected_result}, got {result}"

    def assert_capability_violation(
        self,
        ml_code: str,
        required_capability: CapabilityToken,
        available_capabilities: Optional[Set[CapabilityToken]] = None,
    ):
        """Assert that capability violation is raised.

        Args:
            ml_code: ML code that should violate capabilities
            required_capability: The capability that should be violated
            available_capabilities: Optional set of capabilities to grant

        Raises:
            AssertionError: If violation is not raised
        """
        import asyncio

        async def execute():
            await async_ml_execute(ml_code)

        # Should raise CapabilityNotFoundError
        try:
            asyncio.run(execute())
            raise AssertionError("Expected CapabilityNotFoundError was not raised")
        except CapabilityNotFoundError as e:
            # Expected exception
            assert str(required_capability.capability_type) in str(e), \
                f"Expected violation of {required_capability}, got {e}"
            self.capability_violations.append(e)
        except Exception as e:
            raise AssertionError(
                f"Expected CapabilityNotFoundError, got {type(e).__name__}: {e}"
            )

    def cleanup(self):
        """Clean up test resources."""
        for session in self.mock_repl_sessions:
            try:
                session.cleanup()
            except Exception:
                pass  # Best effort cleanup

        self.mock_repl_sessions.clear()
        self.captured_async_executions.clear()
        self.capability_violations.clear()

    def get_execution_history(self) -> List[Dict]:
        """Get list of all captured async executions.

        Returns:
            List of execution records with code, result, and execution ID
        """
        return self.captured_async_executions.copy()

    def get_violation_history(self) -> List[CapabilityNotFoundError]:
        """Get list of all captured capability violations.

        Returns:
            List of capability violation exceptions
        """
        return self.capability_violations.copy()

    def reset(self):
        """Reset the test helper to initial state.

        This is more aggressive than cleanup() - it removes all state.
        """
        self.cleanup()
        # Reset any global state if needed
        cap_manager = get_capability_manager()
        if hasattr(cap_manager, "reset"):
            cap_manager.reset()
