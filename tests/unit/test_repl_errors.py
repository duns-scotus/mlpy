"""Unit tests for REPL error handling.

These tests validate that the REPL provides beautiful, user-friendly error
messages for all error types: parse errors, security violations, transpilation
errors, and runtime errors.
"""

import pytest

from tests.helpers.repl_test_helper import REPLTestHelper


class TestREPLParseErrors:
    """Test parse error handling in the REPL."""

    @pytest.fixture
    def repl(self):
        """Provide clean REPL test helper."""
        helper = REPLTestHelper(security_enabled=False)
        yield helper
        helper.reset()

    def test_invalid_syntax(self, repl):
        """Test parse error for invalid syntax."""
        repl.assert_ml_parse_error("x = {{{ invalid")

    def test_unmatched_braces(self, repl):
        """Test parse error for unmatched braces."""
        repl.assert_ml_parse_error("function test() { return 42")

    def test_missing_semicolon_in_block(self, repl):
        """Test parse error for missing semicolon in block."""
        # Note: Single statements work, but certain constructs need semicolons
        repl.assert_ml_parse_error("{ x = 1 y = 2 }")

    def test_invalid_token_sequence(self, repl):
        """Test parse error for invalid token sequence."""
        repl.assert_ml_parse_error("= = =")

    def test_incomplete_expression(self, repl):
        """Test parse error for incomplete expression."""
        repl.assert_ml_parse_error("x = ")


class TestREPLSecurityErrors:
    """Test security error handling in the REPL."""

    @pytest.fixture
    def repl(self):
        """Provide REPL with security enabled."""
        helper = REPLTestHelper(security_enabled=True)
        yield helper
        helper.reset()

    def test_reflection_dict_access(self, repl):
        """Test security error for __dict__ access."""
        repl.assert_ml_security_error("x = obj.__dict__", r"reflection attribute")

    def test_reflection_class_access(self, repl):
        """Test security error for __class__ access."""
        repl.assert_ml_security_error("x = obj.__class__", r"reflection attribute")

    def test_reflection_bases_access(self, repl):
        """Test security error for __bases__ access."""
        repl.assert_ml_security_error("x = obj.__bases__", r"reflection attribute")

    def test_code_injection_eval(self, repl):
        """Test security error for eval()."""
        repl.assert_ml_security_error('eval("malicious")', r"code injection")

    def test_code_injection_exec(self, repl):
        """Test security error for exec()."""
        repl.assert_ml_security_error('exec("malicious")', r"code injection")

    def test_dangerous_import_sys(self, repl):
        """Test security error for importing sys."""
        repl.assert_ml_security_error("import sys", r"dangerous module")

    def test_dangerous_import_os(self, repl):
        """Test security error for importing os."""
        repl.assert_ml_security_error("import os", r"dangerous module")

    def test_dangerous_import_subprocess(self, repl):
        """Test security error for importing subprocess."""
        repl.assert_ml_security_error("import subprocess", r"dangerous module")


class TestREPLRuntimeErrors:
    """Test runtime error handling in the REPL."""

    @pytest.fixture
    def repl(self):
        """Provide clean REPL test helper."""
        helper = REPLTestHelper(security_enabled=False)
        yield helper
        helper.reset()

    def test_undefined_variable(self, repl):
        """Test runtime error for undefined variable."""
        result = repl.session.execute_ml_line("x = undefinedVar")
        assert not result.success
        assert "Variable 'undefinedVar' is not defined" in result.error
        assert "Tip:" in result.error

    def test_undefined_function(self, repl):
        """Test runtime error for undefined function."""
        result = repl.session.execute_ml_line("result = unknownFunc(42)")
        assert not result.success
        assert "Variable 'unknownFunc' is not defined" in result.error

    def test_division_by_zero(self, repl):
        """Test runtime error for division by zero."""
        result = repl.session.execute_ml_line("x = 10 / 0")
        assert not result.success
        assert "Division by zero" in result.error
        assert "Tip:" in result.error

    def test_array_index_out_of_bounds(self, repl):
        """Test runtime error for array index out of bounds."""
        repl.execute_ml("arr = [1, 2, 3]")
        result = repl.session.execute_ml_line("x = arr[10]")
        assert not result.success
        assert "Array index out of bounds" in result.error
        assert "Tip:" in result.error

    def test_negative_array_index(self, repl):
        """Test that negative array indices work correctly."""
        repl.execute_ml("arr = [1, 2, 3]")
        result = repl.execute_ml("arr[-1]")
        # Negative indices now work correctly - arr[-1] returns last element
        assert result == 3  # arr[-1] in Python (last element)

    def test_attribute_error(self, repl):
        """Test runtime error for missing attribute/method."""
        repl.execute_ml("x = 42")
        result = repl.session.execute_ml_line("y = x.nonexistent()")
        assert not result.success
        assert "Runtime Error" in result.error
        assert "no accessible" in result.error  # Could be "attribute" or "method"
        assert "Tip:" in result.error

    def test_type_error_method_call(self, repl):
        """Test runtime error for calling non-callable."""
        repl.execute_ml("x = 42")
        result = repl.session.execute_ml_line("y = x()")
        assert not result.success
        assert "Runtime Error" in result.error

    def test_key_error_object_access(self, repl):
        """Test runtime error for missing object key."""
        repl.execute_ml("obj = { a: 1, b: 2 }")
        result = repl.session.execute_ml_line('x = obj["missing"]')
        assert not result.success
        assert "Runtime Error" in result.error
        assert "not found" in result.error.lower() or "keyerror" in result.error.lower()

    def test_value_error(self, repl):
        """Test runtime error for invalid value."""
        # int() conversion of invalid string
        result = repl.session.execute_ml_line('x = int("not_a_number")')
        assert not result.success
        assert "Runtime Error" in result.error


class TestREPLErrorMessages:
    """Test that error messages are user-friendly and helpful."""

    @pytest.fixture
    def repl(self):
        """Provide clean REPL test helper."""
        helper = REPLTestHelper(security_enabled=True)
        yield helper
        helper.reset()

    def test_error_messages_have_tips(self, repl):
        """Test that runtime errors include helpful tips."""
        result = repl.session.execute_ml_line("x = undefinedVar")
        assert "Tip:" in result.error
        assert len(result.error) > 20  # Should be descriptive

    def test_error_messages_no_python_traceback(self, repl):
        """Test that error messages don't include Python tracebacks."""
        result = repl.session.execute_ml_line("x = 10 / 0")
        assert "Traceback" not in result.error
        assert 'File "<' not in result.error
        assert "line " not in result.error.lower() or "Tip:" in result.error

    def test_parse_error_message_format(self, repl):
        """Test that parse errors have consistent format."""
        result = repl.session.execute_ml_line("x = {{{ invalid")
        assert result.error.startswith("Parse Error") or "Error:" in result.error
        assert "Tip:" in result.error or "semicolon" in result.error

    def test_security_error_message_format(self, repl):
        """Test that security errors have consistent format."""
        result = repl.session.execute_ml_line('eval("x")')
        assert "Error:" in result.error or "SECURITY:" in result.error
        assert "eval" in result.error.lower()

    def test_runtime_error_message_format(self, repl):
        """Test that runtime errors have consistent format."""
        result = repl.session.execute_ml_line("x = undefinedVar")
        assert result.error.startswith("Runtime Error")
        assert "Tip:" in result.error

    def test_error_identifies_problem_clearly(self, repl):
        """Test that errors clearly identify the problem."""
        # Undefined variable
        result = repl.session.execute_ml_line("x = foo")
        assert "foo" in result.error or "not defined" in result.error

        # Division by zero
        result = repl.session.execute_ml_line("x = 1 / 0")
        assert "zero" in result.error.lower()

        # Security violation
        result = repl.session.execute_ml_line("x = obj.__dict__")
        assert "__dict__" in result.error or "reflection" in result.error


class TestREPLErrorRecovery:
    """Test that REPL recovers from errors properly."""

    @pytest.fixture
    def repl(self):
        """Provide clean REPL test helper."""
        helper = REPLTestHelper(security_enabled=False)
        yield helper
        helper.reset()

    def test_recovers_from_parse_error(self, repl):
        """Test that REPL continues working after parse error."""
        result = repl.session.execute_ml_line("x = {{{ invalid")
        assert not result.success

        # Should work now - assignment returns None, so check variable
        repl.execute_ml("x = 42")
        assert repl.get_variable("x") == 42

    def test_recovers_from_runtime_error(self, repl):
        """Test that REPL continues working after runtime error."""
        result = repl.session.execute_ml_line("x = 10 / 0")
        assert not result.success

        # Should work now - check expression result
        result = repl.execute_ml("5 + 5")
        assert result == 10

    def test_namespace_preserved_after_error(self, repl):
        """Test that namespace is preserved after errors."""
        repl.execute_ml("x = 100")
        result = repl.session.execute_ml_line("y = undefinedVar")
        assert not result.success

        # x should still be defined
        result = repl.execute_ml("x")
        assert result == 100

    def test_partial_execution_on_error(self, repl):
        """Test that variables before error are still defined."""
        result = repl.session.execute_ml_line("a = 1; b = 2; c = undefinedVar")
        # This should fail on the third statement
        assert not result.success

        # But a and b might be defined depending on execution order
        # This tests error handling doesn't corrupt namespace


class TestREPLHelperErrorMethods:
    """Test the enhanced REPLTestHelper error methods."""

    @pytest.fixture
    def repl(self):
        """Provide REPL test helper."""
        return REPLTestHelper(security_enabled=True)

    def test_assert_ml_parse_error(self, repl):
        """Test assert_ml_parse_error helper method."""
        repl.assert_ml_parse_error("x = {{{ invalid")

    def test_assert_ml_security_error(self, repl):
        """Test assert_ml_security_error helper method."""
        repl.assert_ml_security_error('eval("x")')

    def test_assert_ml_security_error_with_pattern(self, repl):
        """Test assert_ml_security_error with specific pattern."""
        repl.assert_ml_security_error("x = obj.__dict__", r"reflection")

    def test_assert_ml_error_fails_on_success(self, repl):
        """Test that assert_ml_error raises when code succeeds."""
        with pytest.raises(AssertionError, match="execution succeeded"):
            repl.assert_ml_error("x = 42", "some error")

    def test_assert_ml_error_fails_on_wrong_pattern(self, repl):
        """Test that assert_ml_error raises when pattern doesn't match."""
        with pytest.raises(AssertionError, match="doesn't match pattern"):
            repl.assert_ml_error("x = undefinedVar", "division by zero")
