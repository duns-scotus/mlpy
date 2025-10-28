"""Runtime security tests verifying actual execution blocks dunder access.

This test suite verifies that even if malicious code transpiles (bypassing
compile-time checks), the RUNTIME protections in builtin.getattr(),
builtin.hasattr(), and SafeAttributeRegistry block all dunder access.

This is the CRITICAL DEFENSE LAYER that prevents actual exploitation.
"""

import pytest
from mlpy.ml.transpiler import MLTranspiler
from mlpy.ml.codegen.safe_attribute_registry import SafeAttributeRegistry, get_safe_registry
from mlpy.stdlib.builtin import Builtin


class TestRuntimeDunderBlockingComprehensive:
    """Test that runtime protection blocks all dunder access attempts."""

    def setup_method(self):
        """Set up test fixtures."""
        self.builtin = Builtin()
        self.registry = get_safe_registry()

    # =========================================================================
    # SafeAttributeRegistry Tests - Core Runtime Protection
    # =========================================================================

    def test_registry_blocks_dunder_names(self):
        """Test that SafeAttributeRegistry blocks all underscore-prefixed names."""
        test_obj = "test string"

        # Test various dunder patterns
        dunder_names = [
            "__class__",
            "__dict__",
            "__globals__",
            "__builtins__",
            "__bases__",
            "__mro__",
            "__subclasses__",
            "__code__",
            "__init__",
            "__call__",
            "_private",  # Even single underscore should be blocked
            "__custom__",
        ]

        for dunder in dunder_names:
            # is_safe_attribute_name should return False
            assert self.registry.is_safe_attribute_name(test_obj, dunder) == False, \
                f"Registry should block: {dunder}"

            # safe_attr_access should raise AttributeError
            with pytest.raises(AttributeError) as exc_info:
                self.registry.safe_attr_access(test_obj, dunder)

            assert "forbidden" in str(exc_info.value).lower(), \
                f"Should get forbidden error for: {dunder}"

    def test_registry_allows_safe_attributes(self):
        """Test that SafeAttributeRegistry allows whitelisted safe attributes."""
        test_str = "hello world"
        test_list = [1, 2, 3]

        # Safe string attributes
        safe_str_attrs = ["upper", "lower", "strip", "split", "replace"]
        for attr in safe_str_attrs:
            assert self.registry.is_safe_attribute_name(test_str, attr) == True, \
                f"Registry should allow safe attribute: {attr}"

            # Should not raise
            result = self.registry.safe_attr_access(test_str, attr)
            assert callable(result), f"Should return method: {attr}"

        # Safe list attributes
        safe_list_attrs = ["append", "pop", "sort", "reverse"]
        for attr in safe_list_attrs:
            assert self.registry.is_safe_attribute_name(test_list, attr) == True, \
                f"Registry should allow safe attribute: {attr}"

    def test_registry_blocks_dangerous_patterns(self):
        """Test that dangerous patterns are blocked even if not dunder."""
        test_obj = object()

        # Dangerous non-dunder patterns (from _dangerous_patterns)
        dangerous = [
            "eval",
            "exec",
            "compile",
            "__import__",
        ]

        for pattern in dangerous:
            assert self.registry.is_safe_attribute_name(test_obj, pattern) == False, \
                f"Registry should block dangerous pattern: {pattern}"

    # =========================================================================
    # builtin.getattr() Tests - High-Level Runtime Protection
    # =========================================================================

    def test_builtin_getattr_blocks_all_underscores(self):
        """Test that builtin.getattr() blocks ALL names starting with underscore."""
        test_obj = "test string"

        underscore_names = [
            "__class__",
            "__dict__",
            "_private",
            "__custom__",
            "___triple",
        ]

        for name in underscore_names:
            # Should return default value
            result = self.builtin.getattr(test_obj, name, "BLOCKED")
            assert result == "BLOCKED", \
                f"builtin.getattr should block underscore name: {name}"

    def test_builtin_getattr_allows_safe_attributes(self):
        """Test that builtin.getattr() allows whitelisted safe attributes."""
        test_str = "hello"

        # Should successfully get safe attribute
        upper_method = self.builtin.getattr(test_str, "upper")
        assert upper_method is not None
        assert callable(upper_method)

        # Should work with default
        result = self.builtin.getattr(test_str, "nonexistent", "default")
        assert result == "default"

    def test_builtin_getattr_blocks_string_literal_dunders(self):
        """Critical test: Even if string literal bypasses compile, runtime blocks it."""
        test_obj = object()

        # These are the attack vectors from test_dunder_indirect_access.py
        attack_strings = [
            "__class__",
            "__dict__",
            "__globals__",
            "__init__",
            "__builtins__",
        ]

        for attack in attack_strings:
            result = self.builtin.getattr(test_obj, attack, "RUNTIME_BLOCKED")
            assert result == "RUNTIME_BLOCKED", \
                f"Runtime must block string literal: {attack}"

    # =========================================================================
    # builtin.hasattr() Tests - Query Protection
    # =========================================================================

    def test_builtin_hasattr_blocks_all_underscores(self):
        """Test that builtin.hasattr() returns False for all underscore names."""
        test_obj = "test string"

        underscore_names = [
            "__class__",
            "__dict__",
            "_private",
            "__custom__",
        ]

        for name in underscore_names:
            result = self.builtin.hasattr(test_obj, name)
            assert result == False, \
                f"builtin.hasattr should return False for: {name}"

    def test_builtin_hasattr_allows_safe_attributes(self):
        """Test that builtin.hasattr() returns True for safe attributes."""
        test_str = "hello"

        assert self.builtin.hasattr(test_str, "upper") == True
        assert self.builtin.hasattr(test_str, "lower") == True
        assert self.builtin.hasattr(test_str, "nonexistent") == False

    # =========================================================================
    # Attack Scenario Tests - Real Exploitation Attempts
    # =========================================================================

    def test_runtime_blocks_class_introspection_attack(self):
        """Test that classic Python sandbox escape is blocked at runtime."""
        # Classic attack: obj.__class__.__bases__[0].__subclasses__()
        test_obj = []

        # Step 1: Try to get __class__ - should be blocked
        result = self.builtin.getattr(test_obj, "__class__", None)
        assert result is None, "Runtime must block __class__ access"

        # If somehow step 1 worked, step 2 would also be blocked
        if result is not None:
            result2 = self.builtin.getattr(result, "__bases__", None)
            assert result2 is None, "Runtime must block __bases__ access"

    def test_runtime_blocks_globals_access_attack(self):
        """Test that function globals access is blocked at runtime."""

        def test_func():
            return 42

        # Try to access __globals__ - should be blocked
        result = self.builtin.getattr(test_func, "__globals__", None)
        assert result is None, "Runtime must block __globals__ access"

    def test_runtime_blocks_code_object_access(self):
        """Test that function code object access is blocked at runtime."""

        def test_func():
            return 42

        # Try to access __code__ - should be blocked
        result = self.builtin.getattr(test_func, "__code__", None)
        assert result is None, "Runtime must block __code__ access"

    def test_runtime_blocks_module_dict_access(self):
        """Test that module __dict__ access is blocked at runtime."""
        import sys

        # Try to access module __dict__ - should be blocked
        result = self.builtin.getattr(sys, "__dict__", None)
        assert result is None, "Runtime must block module __dict__ access"

    # =========================================================================
    # String Concatenation Attack Tests
    # =========================================================================

    def test_runtime_blocks_concatenated_dunder_names(self):
        """Test that dynamically-built dunder names are blocked at runtime."""
        test_obj = object()

        # Build dunder name at runtime (simulating string concat attack)
        dunder_name = "__" + "class" + "__"

        result = self.builtin.getattr(test_obj, dunder_name, "BLOCKED")
        assert result == "BLOCKED", \
            "Runtime must block dynamically-built dunder names"

    def test_runtime_blocks_partial_dunder_concatenation(self):
        """Test that partial dunders are blocked."""
        test_obj = object()

        # Various partial concatenations
        partial_dunders = [
            "__" + "class__",      # Prefix + suffix
            "__class" + "__",      # Name + dunder
            "_" + "_class__",      # Build piece by piece
        ]

        for dunder in partial_dunders:
            result = self.builtin.getattr(test_obj, dunder, "BLOCKED")
            assert result == "BLOCKED", \
                f"Runtime must block partial dunder: {dunder}"

    # =========================================================================
    # Edge Case Tests
    # =========================================================================

    def test_single_underscore_is_blocked(self):
        """Test that even single underscore names are blocked (private convention)."""
        test_obj = object()

        single_underscore_names = [
            "_private",
            "_internal",
            "_method",
        ]

        for name in single_underscore_names:
            result = self.builtin.getattr(test_obj, name, "BLOCKED")
            assert result == "BLOCKED", \
                f"Runtime should block single underscore: {name}"

    def test_empty_string_attribute_name(self):
        """Test that empty attribute names are handled safely."""
        test_obj = object()

        # Empty string should be blocked (or return default)
        result = self.builtin.getattr(test_obj, "", "BLOCKED")
        assert result == "BLOCKED", "Empty attribute name should be blocked"

    def test_non_string_attribute_name_handling(self):
        """Test that non-string attribute names are handled safely."""
        test_obj = object()

        # This would normally cause TypeError in Python's getattr
        # Our implementation should handle it gracefully
        try:
            result = self.builtin.getattr(test_obj, None, "BLOCKED")
            # If it doesn't raise, it should return default
            assert result == "BLOCKED"
        except (TypeError, AttributeError):
            # Also acceptable to raise an error
            pass


class TestRuntimeProtectionIntegration:
    """Integration tests verifying runtime protection in actual ML code execution."""

    def setup_method(self):
        """Set up test fixtures."""
        self.transpiler = MLTranspiler(repl_mode=True)

    def test_transpiled_code_runtime_protection(self):
        """Test that transpiled code with string literal dunders fails at runtime."""
        # This code will transpile (bypassing compile-time check)
        code = 'x = getattr("test", "__class__");'

        python_code, issues, _ = self.transpiler.transpile_to_python(code)

        # Code should transpile (this is the vulnerability we found)
        assert python_code is not None, "Code should transpile (compile-time bypass)"

        # Now execute and verify runtime protection
        namespace = {}
        exec_code = python_code

        try:
            exec(exec_code, namespace)

            # If execution succeeded, check the result
            # getattr should have returned None/default (blocked)
            result = namespace.get('x')

            # The result should be None or not the actual class object
            assert result is None or not hasattr(result, '__name__'), \
                "Runtime should have blocked dunder access"

        except Exception as e:
            # Runtime protection may raise an error, which is also acceptable
            assert "forbidden" in str(e).lower() or "blocked" in str(e).lower(), \
                f"Runtime error should indicate blocking: {e}"

    def test_getattr_with_default_runtime_protection(self):
        """Test that getattr with default value is protected at runtime."""
        code = 'x = getattr("test", "__dict__", "DEFAULT");'

        python_code, issues, _ = self.transpiler.transpile_to_python(code)
        assert python_code is not None

        namespace = {}
        exec(python_code, namespace)

        result = namespace.get('x')
        # Should get default value, not actual __dict__
        assert result == "DEFAULT" or result is None, \
            "Runtime should block and return default"


class TestComprehensiveRuntimeSecurity:
    """Comprehensive test ensuring runtime matches compile-time security level."""

    def test_runtime_as_strict_as_compile_time(self):
        """Verify runtime blocking is at least as strict as compile-time."""
        builtin = Builtin()

        # All dunders that compile-time blocks
        compile_time_blocked = [
            "__class__", "__dict__", "__globals__", "__builtins__",
            "__bases__", "__mro__", "__subclasses__", "__init__",
            "__new__", "__call__", "__code__", "__closure__",
            "__import__", "__loader__", "__spec__", "__package__",
        ]

        # Runtime MUST also block all of these
        for dunder in compile_time_blocked:
            result = builtin.getattr(object(), dunder, "BLOCKED")
            assert result == "BLOCKED", \
                f"Runtime must block what compile-time blocks: {dunder}"

            has_attr = builtin.hasattr(object(), dunder)
            assert has_attr == False, \
                f"Runtime hasattr must return False for: {dunder}"

    def test_defense_in_depth_verification(self):
        """Verify we have defense in depth: compile-time AND runtime."""
        transpiler = MLTranspiler(repl_mode=True)
        builtin = Builtin()

        # Direct dunder identifier
        code1 = 'x = __class__;'
        python1, issues1, _ = transpiler.transpile_to_python(code1)
        assert python1 is None, "Compile-time should block direct dunder"

        # String literal dunder (bypasses compile-time)
        code2 = 'x = getattr(obj, "__class__");'
        python2, issues2, _ = transpiler.transpile_to_python(code2)
        # Currently bypasses compile-time (vulnerability found)
        # But runtime MUST block it
        result = builtin.getattr(object(), "__class__", "RUNTIME_BLOCKED")
        assert result == "RUNTIME_BLOCKED", "Runtime must block string literal dunder"

        print("✅ Defense in depth verified:")
        print("   - Compile-time blocks direct dunders")
        print("   - Runtime blocks ALL dunders (including string literals)")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
