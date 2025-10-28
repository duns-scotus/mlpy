"""Comprehensive unit tests for blanket dunder blocking policy.

Security Policy: ML code should NEVER use identifiers starting with '__'
(dunder names) as these are Python implementation details and potential
security risks. This applies to ALL contexts: variables, functions,
parameters, attributes, methods, and calls.
"""

import pytest
from mlpy.ml.transpiler import MLTranspiler


class TestDunderBlockingPolicy:
    """Test that ALL dunder names are blocked in ALL contexts."""

    def setup_method(self):
        """Set up test fixtures."""
        self.repl_transpiler = MLTranspiler(repl_mode=True)
        self.normal_transpiler = MLTranspiler(repl_mode=False)

    def test_block_dunder_variable_assignment(self):
        """Test that dunder variable names are blocked."""
        test_cases = [
            "__builtins__",
            "__custom__",
            "__my_var__",
            "__secret",
            "__x",
        ]

        for dunder in test_cases:
            code = f"x = {dunder};"
            python_code, issues, _ = self.repl_transpiler.transpile_to_python(code)
            assert python_code is None, f"Dunder variable '{dunder}' should be blocked"

    def test_block_dunder_function_names(self):
        """Test that dunder function names are blocked."""
        test_cases = [
            "__init__",
            "__new__",
            "__custom_func__",
            "__my_function",
        ]

        for dunder in test_cases:
            code = f"function {dunder}() {{ return 42; }}"
            python_code, issues, _ = self.repl_transpiler.transpile_to_python(code)
            assert python_code is None, f"Dunder function name '{dunder}' should be blocked"

    def test_block_dunder_parameter_names(self):
        """Test that dunder parameter names are blocked."""
        test_cases = [
            "__param__",
            "__arg",
            "__self__",
        ]

        for dunder in test_cases:
            code = f"function test({dunder}) {{ return {dunder}; }}"
            python_code, issues, _ = self.repl_transpiler.transpile_to_python(code)
            assert python_code is None, f"Dunder parameter name '{dunder}' should be blocked"

    def test_block_dunder_attribute_access(self):
        """Test that dunder attribute access is blocked."""
        test_cases = [
            "__dict__",
            "__class__",
            "__bases__",
            "__custom_attr__",
        ]

        for dunder in test_cases:
            code = f"x = obj.{dunder};"
            python_code, issues, _ = self.repl_transpiler.transpile_to_python(code)
            assert python_code is None, f"Dunder attribute access '{dunder}' should be blocked"

    def test_block_dunder_method_calls(self):
        """Test that dunder method calls are blocked."""
        test_cases = [
            "__init__",
            "__str__",
            "__repr__",
            "__custom_method__",
        ]

        for dunder in test_cases:
            code = f"x = obj.{dunder}();"
            python_code, issues, _ = self.repl_transpiler.transpile_to_python(code)
            assert python_code is None, f"Dunder method call '{dunder}' should be blocked"

    def test_block_dunder_function_calls(self):
        """Test that dunder function calls are blocked."""
        test_cases = [
            "__import__",
            "__builtins__",
            "__custom__",
        ]

        for dunder in test_cases:
            code = f"{dunder}();"
            python_code, issues, _ = self.repl_transpiler.transpile_to_python(code)
            assert python_code is None, f"Dunder function call '{dunder}' should be blocked"

    def test_allow_non_dunder_identifiers(self):
        """Test that regular identifiers are allowed."""
        allowed_cases = [
            "variable",
            "my_var",
            "_private",
            "_internal_var",  # Single underscore prefix is OK
            "custom_function",
        ]

        for identifier in allowed_cases:
            code = f"x = {identifier};"
            python_code, issues, _ = self.repl_transpiler.transpile_to_python(code)
            # Should either transpile successfully or fail for a different reason (undefined variable)
            # but NOT due to dunder blocking
            if issues:
                for issue in issues:
                    assert "dunder" not in issue.message.lower(), \
                        f"Regular identifier '{identifier}' should not trigger dunder blocking"

    def test_block_mixed_dunder_cases(self):
        """Test complex cases with multiple dunders."""
        code = """
        function test() {
            x = __builtins__;
            y = obj.__dict__;
            return __import__("os");
        }
        """
        python_code, issues, _ = self.repl_transpiler.transpile_to_python(code)
        assert python_code is None, "Code with multiple dunders should be blocked"

    def test_dunder_blocking_in_expressions(self):
        """Test dunder blocking in complex expressions."""
        test_cases = [
            "x = __custom__ + 5;",
            "if (__flag__) { return 1; }",
            "arr = [__item__, 2, 3];",
            "obj = {key: __value__};",
        ]

        for code in test_cases:
            python_code, issues, _ = self.repl_transpiler.transpile_to_python(code)
            assert python_code is None, f"Dunder in expression should be blocked: {code}"

    def test_known_dangerous_dunders_still_blocked(self):
        """Verify that all previously known dangerous dunders are still blocked."""
        dangerous_dunders = [
            "__builtins__", "__import__", "__loader__", "__spec__",
            "__name__", "__file__", "__package__", "__path__",
            "__dict__", "__class__", "__bases__", "__subclasses__", "__mro__",
            "__init__", "__new__", "__call__",
            "__code__", "__globals__", "__closure__",
        ]

        for dunder in dangerous_dunders:
            code = f"x = {dunder};"
            python_code, issues, _ = self.repl_transpiler.transpile_to_python(code)
            assert python_code is None, f"Known dangerous dunder '{dunder}' should still be blocked"

    def test_non_dunder_dangerous_builtins_blocked(self):
        """Test that dangerous non-dunder builtins are also blocked."""
        dangerous_builtins = [
            "eval", "exec", "compile", "execfile",
            "globals", "locals", "vars", "dir",
            "open",
            "exit", "quit",
        ]

        for builtin in dangerous_builtins:
            code = f"x = {builtin};"
            python_code, issues, _ = self.repl_transpiler.transpile_to_python(code)
            assert python_code is None, f"Dangerous builtin '{builtin}' should be blocked"

    def test_safe_builtins_allowed(self):
        """Test that safe ML builtins are NOT blocked."""
        safe_builtins = [
            "input",  # Safe ML wrapper
            "help",   # Safe ML wrapper
            # Note: getattr, setattr, hasattr have runtime validation
        ]

        for builtin in safe_builtins:
            code = f"x = {builtin};"
            python_code, issues, _ = self.repl_transpiler.transpile_to_python(code)
            # Should not be blocked by dunder/builtin blocking
            # (may fail for other reasons like undefined, but not security)
            if python_code is None and issues:
                for issue in issues:
                    assert "dunder" not in issue.message.lower(), \
                        f"Safe builtin '{builtin}' should not be blocked"
                    assert "builtin" not in issue.message.lower(), \
                        f"Safe builtin '{builtin}' should not be blocked"

    def test_dunder_blocking_both_repl_and_normal_mode(self):
        """Test that dunder blocking works in both REPL and normal transpiler mode."""
        code = "x = __builtins__;"

        # REPL mode
        repl_result, repl_issues, _ = self.repl_transpiler.transpile_to_python(code)
        assert repl_result is None, "Dunders should be blocked in REPL mode"

        # Normal mode
        normal_result, normal_issues, _ = self.normal_transpiler.transpile_to_python(code)
        assert normal_result is None, "Dunders should be blocked in normal mode too"

    def test_error_messages_helpful(self):
        """Test that error messages are clear and helpful."""
        code = "x = __custom__;"
        python_code, issues, _ = self.repl_transpiler.transpile_to_python(code)

        assert python_code is None
        # Note: issues might be empty if transpilation fails early
        # This test just verifies the blocking happens

    def test_nested_dunder_access(self):
        """Test that nested dunder access is blocked."""
        test_cases = [
            "x = obj.__dict__.__class__;",
            "x = obj.method().__dict__;",
            "x = obj[0].__class__;",
        ]

        for code in test_cases:
            python_code, issues, _ = self.repl_transpiler.transpile_to_python(code)
            assert python_code is None, f"Nested dunder access should be blocked: {code}"


class TestDunderBlockingEdgeCases:
    """Test edge cases for dunder blocking."""

    def setup_method(self):
        """Set up test fixtures."""
        self.transpiler = MLTranspiler(repl_mode=True)

    def test_single_underscore_allowed(self):
        """Test that single underscore identifiers are allowed."""
        allowed_cases = [
            "_private",
            "_internal",
            "_x",
            "_my_function",
        ]

        for identifier in allowed_cases:
            code = f"function test() {{ {identifier} = 42; return {identifier}; }}"
            python_code, issues, _ = self.transpiler.transpile_to_python(code)
            # Should not be blocked by dunder check (single underscore is OK)
            if python_code is None and issues:
                for issue in issues:
                    assert "dunder" not in issue.message.lower(), \
                        f"Single underscore identifier '{identifier}' should not trigger dunder blocking"

    def test_triple_underscore_blocked(self):
        """Test that triple underscores are also blocked (start with __)."""
        code = "x = ___custom___;"
        python_code, issues, _ = self.transpiler.transpile_to_python(code)
        assert python_code is None, "Triple underscore should be blocked (starts with __)"

    def test_underscore_only_not_dunder(self):
        """Test that single underscore is not a dunder."""
        code = "_ = 42;"
        python_code, issues, _ = self.transpiler.transpile_to_python(code)
        # Single underscore should not be blocked as dunder
        if python_code is None and issues:
            for issue in issues:
                assert "dunder" not in issue.message.lower(), \
                    "Single underscore '_' should not be treated as dunder"

    def test_empty_identifier_edge_case(self):
        """Test handling of edge cases with identifier checking."""
        # This test ensures the code doesn't crash on edge cases
        # The actual parsing may fail, but should not cause exceptions
        try:
            code = "x = __;"
            python_code, issues, _ = self.transpiler.transpile_to_python(code)
            # Just ensure no crash happens
            assert True
        except Exception as e:
            # Should not raise exceptions, but if it does, fail the test
            pytest.fail(f"Dunder checking caused exception: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
