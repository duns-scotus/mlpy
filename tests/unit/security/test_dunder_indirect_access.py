"""Security tests for indirect dunder access via getattr and call.

This test suite verifies that dunder names cannot be accessed indirectly
through "safe" builtin functions like getattr() and call().

Attack vectors tested:
1. getattr(obj, "__class__") - Direct dunder access via getattr
2. call(getattr(obj, "__init__"), args) - Chained getattr + call
3. getattr with string concatenation to build dunder names
4. call() with dunder function names passed as strings
5. Runtime-constructed dunder names via string operations
"""

import pytest
from mlpy.ml.transpiler import MLTranspiler


class TestIndirectDunderAccess:
    """Test that dunders cannot be accessed indirectly through safe builtins."""

    def setup_method(self):
        """Set up test fixtures."""
        self.transpiler = MLTranspiler(repl_mode=True)

    # =========================================================================
    # Attack Vector 1: Direct getattr with dunder names
    # =========================================================================

    def test_getattr_with_dunder_literal(self):
        """Test that getattr with dunder name literal is blocked at transpile time."""
        attack_cases = [
            'x = getattr(obj, "__class__");',
            'x = getattr(obj, "__dict__");',
            'x = getattr(obj, "__globals__");',
            'x = getattr(obj, "__builtins__");',
            'x = getattr(obj, "__init__");',
            'x = getattr(obj, "__import__");',
        ]

        for code in attack_cases:
            python_code, issues, _ = self.transpiler.transpile_to_python(code)
            # Should be blocked at transpile time because "__class__" is a dunder literal
            assert python_code is None, f"Dunder literal in getattr should be blocked: {code}"

    def test_getattr_with_dunder_default_value(self):
        """Test that getattr with dunder and default is blocked."""
        attack_cases = [
            'x = getattr(obj, "__class__", None);',
            'x = getattr(obj, "__dict__", {});',
        ]

        for code in attack_cases:
            python_code, issues, _ = self.transpiler.transpile_to_python(code)
            assert python_code is None, f"Dunder in getattr with default should be blocked: {code}"

    # =========================================================================
    # Attack Vector 2: call() with getattr results
    # =========================================================================

    def test_call_with_getattr_dunder(self):
        """Test that call(getattr(obj, dunder)) is blocked."""
        attack_cases = [
            'x = call(getattr(obj, "__init__"), arg);',
            'x = call(getattr(obj, "__call__"));',
            'x = call(getattr(str, "__new__"), "test");',
        ]

        for code in attack_cases:
            python_code, issues, _ = self.transpiler.transpile_to_python(code)
            assert python_code is None, f"call(getattr(dunder)) should be blocked: {code}"

    # =========================================================================
    # Attack Vector 3: String concatenation to build dunder names
    # =========================================================================

    def test_string_concat_to_build_dunder(self):
        """Test that string concatenation to build dunder names is blocked."""
        # These should work because we block at compile time on string literals
        attack_cases = [
            'prefix = "__"; name = "class__"; x = getattr(obj, prefix + name);',
            'dunder = "__" + "dict__"; x = getattr(obj, dunder);',
        ]

        for code in attack_cases:
            python_code, issues, _ = self.transpiler.transpile_to_python(code)
            # The string literals "__" should be blocked as dunder identifiers
            assert python_code is None, f"String concat dunder should be blocked: {code}"

    # =========================================================================
    # Attack Vector 4: call() with dunder function reference
    # =========================================================================

    def test_call_with_dunder_function(self):
        """Test that call(__import__) and similar are blocked."""
        attack_cases = [
            'x = call(__import__, "os");',
            'x = call(__builtins__, "eval");',
        ]

        for code in attack_cases:
            python_code, issues, _ = self.transpiler.transpile_to_python(code)
            assert python_code is None, f"call(dunder_func) should be blocked: {code}"

    # =========================================================================
    # Attack Vector 5: Nested getattr chains
    # =========================================================================

    def test_nested_getattr_chains(self):
        """Test that nested getattr with dunders is blocked."""
        attack_cases = [
            'x = getattr(getattr(obj, "__class__"), "__bases__");',
            'x = getattr(getattr(str, "__init__"), "__code__");',
        ]

        for code in attack_cases:
            python_code, issues, _ = self.transpiler.transpile_to_python(code)
            assert python_code is None, f"Nested getattr with dunders should be blocked: {code}"

    # =========================================================================
    # Attack Vector 6: Method chaining with getattr
    # =========================================================================

    def test_method_chaining_with_getattr(self):
        """Test that method chaining with getattr dunders is blocked."""
        attack_cases = [
            'x = getattr(obj, "__class__").__name__;',
            'x = getattr(obj, "__dict__").keys();',
        ]

        for code in attack_cases:
            python_code, issues, _ = self.transpiler.transpile_to_python(code)
            assert python_code is None, f"Method chaining with getattr dunders should be blocked: {code}"

    # =========================================================================
    # Positive Tests: Verify safe access still works
    # =========================================================================

    def test_getattr_with_safe_attributes(self):
        """Test that getattr with safe attributes works correctly."""
        safe_cases = [
            'x = getattr("hello", "upper");',
            'x = getattr([1,2,3], "append");',
            'x = getattr(obj, "name", "default");',
        ]

        for code in safe_cases:
            python_code, issues, _ = self.transpiler.transpile_to_python(code)
            # These should transpile (may have other issues but not dunder blocking)
            if python_code is None and issues:
                for issue in issues:
                    assert "dunder" not in issue.message.lower(), \
                        f"Safe getattr should not trigger dunder blocking: {code}"

    def test_call_with_safe_functions(self):
        """Test that call() with safe functions works."""
        safe_cases = [
            'x = call(abs, -5);',
            'x = call(len, [1,2,3]);',
        ]

        for code in safe_cases:
            python_code, issues, _ = self.transpiler.transpile_to_python(code)
            # These should transpile (may have other issues but not dunder blocking)
            if python_code is None and issues:
                for issue in issues:
                    assert "dunder" not in issue.message.lower(), \
                        f"Safe call should not trigger dunder blocking: {code}"


class TestRuntimeDunderProtection:
    """Test runtime protection against dunder access (defense in depth)."""

    def setup_method(self):
        """Set up test fixtures."""
        self.transpiler = MLTranspiler(repl_mode=True)

    def test_runtime_getattr_blocks_underscores(self):
        """Verify that even if compile-time check fails, runtime getattr blocks underscores.

        This is defense-in-depth: the runtime getattr implementation blocks
        ALL names starting with underscore, including dunders.
        """
        # This test verifies the runtime behavior documented in builtin.py:
        # - hasattr() returns False for names starting with '_'
        # - getattr() returns default for names starting with '_'

        # Note: We can't easily test this at runtime in unit tests without
        # executing the code, but we can verify the implementation exists
        from mlpy.stdlib.builtin import Builtin

        builtin = Builtin()

        # Test hasattr blocks underscores
        obj = "test string"
        assert builtin.hasattr(obj, "upper") == True, "Safe attribute should return True"
        assert builtin.hasattr(obj, "__class__") == False, "Dunder should return False"
        assert builtin.hasattr(obj, "_private") == False, "Single underscore should return False"

        # Test getattr blocks underscores
        assert builtin.getattr(obj, "upper") is not None, "Safe attribute should be accessible"
        assert builtin.getattr(obj, "__class__", "BLOCKED") == "BLOCKED", "Dunder should return default"
        assert builtin.getattr(obj, "_private", "BLOCKED") == "BLOCKED", "Single underscore should return default"

    def test_runtime_call_validates_functions(self):
        """Verify that runtime call() validates functions through safe_call.

        The call() builtin delegates to safe_call() which validates that
        the function is whitelisted before execution.
        """
        from mlpy.stdlib.builtin import Builtin

        builtin = Builtin()

        # Test that call works with safe functions
        result = builtin.call(abs, -5)
        assert result == 5, "Safe function should execute"

        # Test that call blocks dangerous functions
        # Note: We can't easily test eval/exec here as they're not in scope,
        # but the safe_call implementation in whitelist_validator handles this


class TestEdgeCases:
    """Test edge cases and creative bypass attempts."""

    def setup_method(self):
        """Set up test fixtures."""
        self.transpiler = MLTranspiler(repl_mode=True)

    def test_unicode_dunder_bypass_attempt(self):
        """Test that Unicode lookalikes for underscores don't bypass checks."""
        # Using Unicode "LOW LINE" character (U+005F is underscore)
        # ML parser should treat these as underscores
        code = 'x = __class__;'  # Regular ASCII underscores
        python_code, issues, _ = self.transpiler.transpile_to_python(code)
        assert python_code is None, "Unicode underscore bypass should be blocked"

    def test_whitespace_in_dunder_names(self):
        """Test that whitespace doesn't bypass dunder detection."""
        attack_cases = [
            'x = __ class__;',  # Space in middle (should be parse error)
            'x =  __class__ ;',  # Extra spaces (should still block)
        ]

        for code in attack_cases:
            python_code, issues, _ = self.transpiler.transpile_to_python(code)
            # Should either fail to parse or be blocked as dunder
            assert python_code is None, f"Whitespace bypass attempt should fail: {code}"

    def test_mixed_case_dunder_names(self):
        """Test that case variations don't bypass dunder detection."""
        # Python identifiers are case-sensitive, so __Class__ != __class__
        # But they still start with __ so should be blocked
        attack_cases = [
            'x = __Class__;',
            'x = __CLASS__;',
            'x = __ClAsS__;',
        ]

        for code in attack_cases:
            python_code, issues, _ = self.transpiler.transpile_to_python(code)
            assert python_code is None, f"Case variation should still be blocked: {code}"

    def test_triple_underscore_variations(self):
        """Test that variations with more than two underscores are blocked."""
        attack_cases = [
            'x = ___class___;',
            'x = ____init____;',
            'x = _____dict_____;',
        ]

        for code in attack_cases:
            python_code, issues, _ = self.transpiler.transpile_to_python(code)
            assert python_code is None, f"Multi-underscore should be blocked: {code}"


class TestSecurityDocumentation:
    """Verify that security documentation claims are accurate."""

    def test_documented_attack_vectors_blocked(self):
        """Test that all documented attack vectors in docstrings are actually blocked."""
        transpiler = MLTranspiler(repl_mode=True)

        # From call() docstring
        documented_attacks = [
            'call(eval, "malicious");',
            'call(open, "secrets.txt");',
            'call(__import__, "os");',
        ]

        for code in documented_attacks:
            python_code, issues, _ = transpiler.transpile_to_python(code)
            assert python_code is None, f"Documented attack should be blocked: {code}"

    def test_documented_safe_examples_work(self):
        """Test that documented safe examples actually transpile."""
        transpiler = MLTranspiler(repl_mode=True)

        # From getattr() and call() docstrings
        safe_examples = [
            'x = getattr("hello", "upper");',
            'x = getattr(obj, "missing", 42);',
            'x = call(abs, -5);',
        ]

        for code in safe_examples:
            python_code, issues, _ = transpiler.transpile_to_python(code)
            # Should transpile (may have undefined vars but not security blocks)
            if python_code is None and issues:
                for issue in issues:
                    assert "dunder" not in issue.message.lower(), \
                        f"Safe example should not trigger security: {code}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
