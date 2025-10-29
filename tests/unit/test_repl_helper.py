"""Unit tests for REPLTestHelper.

These tests validate that the REPL test helper works correctly
and can be used for stdlib testing.
"""

import pytest

from tests.helpers.repl_test_helper import REPLTestHelper


class TestREPLTestHelper:
    """Test cases for REPLTestHelper functionality."""

    @pytest.fixture
    def repl(self):
        """Provide clean REPL test helper."""
        helper = REPLTestHelper(security_enabled=False)
        yield helper
        helper.reset()

    def test_execute_ml_basic(self, repl):
        """Test basic ML code execution."""
        result = repl.execute_ml("42")
        assert result == 42

    def test_execute_ml_arithmetic(self, repl):
        """Test arithmetic expressions."""
        result = repl.execute_ml("10 + 20")
        assert result == 30

    def test_execute_ml_variable_assignment(self, repl):
        """Test variable assignment and retrieval."""
        repl.execute_ml("x = 100")
        result = repl.execute_ml("x")
        assert result == 100

    def test_execute_ml_function_definition(self, repl):
        """Test function definition and call."""
        repl.execute_ml("function double(n) { return n * 2; }")
        result = repl.execute_ml("double(21)")
        assert result == 42

    def test_assert_ml_equals(self, repl):
        """Test assert_ml_equals helper."""
        repl.assert_ml_equals("5 + 7", 12)
        repl.assert_ml_equals('"hello"', "hello")

    def test_assert_ml_equals_failure(self, repl):
        """Test assert_ml_equals raises on mismatch."""
        with pytest.raises(AssertionError, match="Expected 10, got 12"):
            repl.assert_ml_equals("5 + 7", 10)

    def test_assert_ml_error(self, repl):
        """Test assert_ml_error helper."""
        # Invalid syntax should produce an error
        repl.assert_ml_error("function invalid syntax", "Unexpected token")

    def test_assert_ml_type(self, repl):
        """Test assert_ml_type helper."""
        repl.assert_ml_type("42", int)
        repl.assert_ml_type('"text"', str)
        repl.assert_ml_type("[1, 2, 3]", list)

    def test_assert_ml_truthy(self, repl):
        """Test assert_ml_truthy helper."""
        repl.assert_ml_truthy("true")
        repl.assert_ml_truthy("42")
        repl.assert_ml_truthy('"text"')

    def test_assert_ml_falsy(self, repl):
        """Test assert_ml_falsy helper."""
        repl.assert_ml_falsy("false")
        repl.assert_ml_falsy("0")
        repl.assert_ml_falsy('""')

    def test_execute_ml_lines(self, repl):
        """Test executing multiple lines."""
        lines = ["a = 10", "b = 20", "a + b"]
        results = repl.execute_ml_lines(lines)
        assert results[2] == 30

    def test_get_set_variable(self, repl):
        """Test getting and setting variables."""
        repl.set_variable("test_var", 999)
        assert repl.get_variable("test_var") == 999

    def test_get_all_variables(self, repl):
        """Test getting all variables."""
        repl.execute_ml("x = 1")
        repl.execute_ml("y = 2")

        vars_dict = repl.get_all_variables()
        assert "x" in vars_dict
        assert "y" in vars_dict
        assert vars_dict["x"] == 1
        assert vars_dict["y"] == 2

    def test_reset_clears_namespace(self, repl):
        """Test reset clears all variables."""
        repl.execute_ml("x = 42")
        assert repl.get_variable("x") == 42

        repl.reset()

        with pytest.raises(KeyError):
            repl.get_variable("x")

    def test_persistent_namespace(self, repl):
        """Test that namespace persists across calls."""
        repl.execute_ml("counter = 0")
        repl.execute_ml("counter = counter + 1")
        repl.execute_ml("counter = counter + 1")

        result = repl.execute_ml("counter")
        assert result == 2

    def test_string_operations(self, repl):
        """Test string operations work."""
        repl.assert_ml_equals('"hello" + " world"', "hello world")

    def test_array_operations(self, repl):
        """Test array operations work."""
        result = repl.execute_ml("[1, 2, 3]")
        assert result == [1, 2, 3]

    def test_object_operations(self, repl):
        """Test object operations work."""
        # Assignment returns None, need to retrieve the value
        repl.execute_ml("obj = { x: 10, y: 20 }")
        result = repl.get_variable("obj")
        # Objects should be dict-like
        assert isinstance(result, dict)
        assert result["x"] == 10
        assert result["y"] == 20
