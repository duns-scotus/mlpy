"""REPL Test Helper for testing ML code execution.

This helper provides a clean interface for unit tests to execute ML code
and validate results, ensuring tests cover the complete pipeline:
ML parsing → Security analysis → Python generation → Execution
"""

import re
from typing import Any

from mlpy.cli.repl import MLREPLSession


class REPLTestHelper:
    """Helper for testing ML code via REPL execution.

    This class wraps MLREPLSession and provides convenient assertion methods
    for testing standard library functions and ML language features.

    Example:
        def test_string_length(repl):
            repl.assert_ml_equals(
                'import String; String.length("hello")',
                5
            )
    """

    def __init__(self, security_enabled: bool = False):
        """Initialize REPL test helper.

        Args:
            security_enabled: Enable security checks (default: False for testing)
        """
        self.session = MLREPLSession(security_enabled=security_enabled)

    def execute_ml(self, code: str) -> Any:
        """Execute ML code and return result.

        Args:
            code: ML code to execute

        Returns:
            Result value from execution

        Raises:
            AssertionError: If execution fails
        """
        result = self.session.execute_ml_line(code)
        if not result.success:
            raise AssertionError(
                f"ML execution failed: {result.error}\n"
                f"Code: {code}\n"
                f"Transpiled: {result.transpiled_python}"
            )
        return result.value

    def execute_ml_lines(self, lines: list[str]) -> list[Any]:
        """Execute multiple ML lines, return list of results.

        Args:
            lines: List of ML code lines to execute

        Returns:
            List of result values (one per line)
        """
        return [self.execute_ml(line) for line in lines]

    def assert_ml_equals(self, ml_code: str, expected: Any, msg: str | None = None):
        """Execute ML code and assert result equals expected value.

        Args:
            ml_code: ML code to execute
            expected: Expected result value
            msg: Optional custom error message
        """
        result = self.execute_ml(ml_code)

        if result != expected:
            error_msg = msg or (
                f"Expected {repr(expected)}, got {repr(result)}\n" f"Code: {ml_code}"
            )
            raise AssertionError(error_msg)

    def assert_ml_error(self, ml_code: str, error_pattern: str):
        """Execute ML code and assert it raises error matching pattern.

        Args:
            ml_code: ML code to execute
            error_pattern: Regex pattern that should match the error message
        """
        result = self.session.execute_ml_line(ml_code)

        if result.success:
            raise AssertionError(
                f"Expected error matching '{error_pattern}', but execution succeeded\n"
                f"Code: {ml_code}\n"
                f"Result: {result.value}"
            )

        if not re.search(error_pattern, result.error):
            raise AssertionError(
                f"Error message doesn't match pattern '{error_pattern}'\n"
                f"Code: {ml_code}\n"
                f"Actual error: {result.error}"
            )

    def assert_ml_parse_error(self, ml_code: str):
        """Execute ML code and assert it raises a parse error.

        Args:
            ml_code: ML code that should fail to parse
        """
        self.assert_ml_error(ml_code, r"Parse Error")

    def assert_ml_security_error(self, ml_code: str, security_pattern: str = None):
        """Execute ML code and assert it raises a security error.

        Args:
            ml_code: ML code that should violate security
            security_pattern: Optional regex pattern for specific security error
        """
        pattern = security_pattern if security_pattern else r"(Error:|SECURITY:)"
        self.assert_ml_error(ml_code, pattern)

    def assert_ml_runtime_error(self, ml_code: str, error_type: str):
        """Execute ML code and assert it raises a specific runtime error.

        Args:
            ml_code: ML code that should fail at runtime
            error_type: Type of runtime error (e.g., 'NameError', 'TypeError')
        """
        self.assert_ml_error(ml_code, f"Runtime Error.*{error_type}")

    def assert_ml_type(self, ml_code: str, expected_type: type):
        """Execute ML code and assert result is of expected type.

        Args:
            ml_code: ML code to execute
            expected_type: Expected Python type of result
        """
        result = self.execute_ml(ml_code)

        if not isinstance(result, expected_type):
            raise AssertionError(
                f"Expected type {expected_type.__name__}, got {type(result).__name__}\n"
                f"Code: {ml_code}\n"
                f"Result: {repr(result)}"
            )

    def assert_ml_truthy(self, ml_code: str):
        """Execute ML code and assert result is truthy.

        Args:
            ml_code: ML code to execute
        """
        result = self.execute_ml(ml_code)

        if not result:
            raise AssertionError(f"Expected truthy value, got {repr(result)}\n" f"Code: {ml_code}")

    def assert_ml_falsy(self, ml_code: str):
        """Execute ML code and assert result is falsy.

        Args:
            ml_code: ML code to execute
        """
        result = self.execute_ml(ml_code)

        if result:
            raise AssertionError(f"Expected falsy value, got {repr(result)}\n" f"Code: {ml_code}")

    def get_transpiled_python(self, ml_code: str) -> str:
        """Get transpiled Python code without executing.

        Args:
            ml_code: ML code to transpile

        Returns:
            Generated Python code
        """
        result = self.session.execute_ml_line(ml_code)
        return result.transpiled_python

    def reset(self):
        """Reset session namespace (clear all variables)."""
        self.session.reset_session()

    def get_variable(self, name: str) -> Any:
        """Get value of a variable from the namespace.

        Args:
            name: Variable name

        Returns:
            Variable value

        Raises:
            KeyError: If variable doesn't exist
        """
        return self.session.python_namespace[name]

    def set_variable(self, name: str, value: Any):
        """Set a variable in the namespace (for test setup).

        Args:
            name: Variable name
            value: Variable value
        """
        self.session.python_namespace[name] = value

    def get_all_variables(self) -> dict[str, Any]:
        """Get all user-defined variables.

        Returns:
            Dictionary of variable names to values
        """
        return self.session.get_variables()
