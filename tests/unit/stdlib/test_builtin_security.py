"""Security tests for builtin module dynamic introspection.

These tests verify that hasattr(), getattr(), and call() cannot be used
to bypass security controls or access dangerous object internals.
"""

import pytest
from mlpy.stdlib.builtin import Builtin, builtin


class TestDynamicIntrospectionSecurity:
    """Security tests for hasattr/getattr/call."""

    # =====================================================================
    # hasattr() Security Tests
    # =====================================================================

    def test_hasattr_blocks_class_attribute(self):
        """Verify __class__ is blocked by hasattr."""
        assert builtin.hasattr("test", "__class__") is False
        assert builtin.hasattr([], "__class__") is False
        assert builtin.hasattr({}, "__class__") is False

    def test_hasattr_blocks_dict_attribute(self):
        """Verify __dict__ is blocked by hasattr."""
        class TestObj:
            pass
        obj = TestObj()
        assert builtin.hasattr(obj, "__dict__") is False

    def test_hasattr_blocks_globals_attribute(self):
        """Verify __globals__ is blocked by hasattr."""
        def test_func():
            pass
        assert builtin.hasattr(test_func, "__globals__") is False

    def test_hasattr_blocks_subclasses_attribute(self):
        """Verify __subclasses__ is blocked by hasattr."""
        assert builtin.hasattr(object, "__subclasses__") is False
        assert builtin.hasattr(str, "__subclasses__") is False

    def test_hasattr_blocks_mro_attribute(self):
        """Verify __mro__ is blocked by hasattr."""
        assert builtin.hasattr(str, "__mro__") is False
        assert builtin.hasattr(list, "__mro__") is False

    def test_hasattr_blocks_code_attribute(self):
        """Verify __code__ is blocked by hasattr."""
        def test_func():
            pass
        assert builtin.hasattr(test_func, "__code__") is False

    def test_hasattr_blocks_all_dunder_attributes(self):
        """Verify ALL dunder attributes are blocked."""
        dangerous_attrs = [
            "__class__", "__dict__", "__globals__", "__bases__",
            "__mro__", "__subclasses__", "__code__", "__closure__",
            "__defaults__", "__kwdefaults__", "__annotations__",
            "__module__", "__qualname__", "__doc__", "__weakref__",
            "__getattribute__", "__setattr__", "__delattr__"
        ]

        test_obj = "test"
        for attr in dangerous_attrs:
            assert builtin.hasattr(test_obj, attr) is False, \
                f"hasattr should block {attr}"

    def test_hasattr_only_reveals_safe_attributes(self):
        """Verify hasattr only returns True for safe whitelisted attributes."""
        # Safe: "upper" is in string whitelist
        assert builtin.hasattr("test", "upper") is True

        # Safe: "append" is in list whitelist
        assert builtin.hasattr([], "append") is True

        # Unsafe: arbitrary attribute not in whitelist
        assert builtin.hasattr("test", "arbitrary_method") is False

    # =====================================================================
    # getattr() Security Tests
    # =====================================================================

    def test_getattr_blocks_class_access(self):
        """Verify getattr blocks __class__ access."""
        result = builtin.getattr("test", "__class__", "BLOCKED")
        assert result == "BLOCKED"

    def test_getattr_blocks_globals_access(self):
        """Verify getattr blocks __globals__ access."""
        def test_func():
            pass
        result = builtin.getattr(test_func, "__globals__", "BLOCKED")
        assert result == "BLOCKED"

    def test_getattr_blocks_dict_access(self):
        """Verify getattr blocks __dict__ access."""
        class TestObj:
            pass
        obj = TestObj()
        result = builtin.getattr(obj, "__dict__", "BLOCKED")
        assert result == "BLOCKED"

    def test_getattr_blocks_subclasses_traversal(self):
        """Verify getattr blocks __subclasses__ access."""
        result = builtin.getattr(object, "__subclasses__", "BLOCKED")
        assert result == "BLOCKED"

    def test_getattr_blocks_mro_access(self):
        """Verify getattr blocks __mro__ access."""
        result = builtin.getattr(str, "__mro__", "BLOCKED")
        assert result == "BLOCKED"

    def test_getattr_blocks_code_access(self):
        """Verify getattr blocks __code__ access."""
        def test_func():
            pass
        result = builtin.getattr(test_func, "__code__", "BLOCKED")
        assert result == "BLOCKED"

    def test_getattr_blocks_all_dunder_attributes(self):
        """Verify getattr blocks ALL dunder attributes."""
        dangerous_attrs = [
            "__class__", "__dict__", "__globals__", "__bases__",
            "__mro__", "__subclasses__", "__code__", "__closure__",
            "__defaults__", "__kwdefaults__", "__annotations__"
        ]

        test_obj = "test"
        for attr in dangerous_attrs:
            result = builtin.getattr(test_obj, attr, "BLOCKED")
            assert result == "BLOCKED", \
                f"getattr should block {attr}"

    def test_getattr_only_allows_safe_registry_attributes(self):
        """Verify getattr only allows SafeAttributeRegistry attributes."""
        # Safe: "upper" is in string whitelist
        result = builtin.getattr("test", "upper")
        assert result is not None
        assert callable(result)

        # Unsafe: arbitrary attribute not in whitelist
        result = builtin.getattr("test", "arbitrary_attr", "DEFAULT")
        assert result == "DEFAULT"

    def test_getattr_safe_attribute_works(self):
        """Verify getattr works correctly for safe attributes."""
        # String method
        upper_method = builtin.getattr("hello", "upper")
        assert callable(upper_method)

        # List method
        append_method = builtin.getattr([], "append")
        assert callable(append_method)

        # Dict method
        keys_method = builtin.getattr({}, "keys")
        assert callable(keys_method)

    # =====================================================================
    # Penetration Testing Scenarios
    # =====================================================================

    def test_no_sandbox_escape_via_class_traversal(self):
        """Attempt class hierarchy traversal - should fail at first step."""
        # Try to get __class__
        cls = builtin.getattr("", "__class__", None)
        assert cls is None  # Blocked at first step

        # Even if we had cls, can't get __bases__
        if cls is not None:  # Won't execute, but shows attack pattern
            bases = builtin.getattr(cls, "__bases__", None)
            assert bases is None

    def test_no_sandbox_escape_via_subclasses(self):
        """Attempt __subclasses__ traversal - should fail."""
        # Try to get object class
        obj_cls = builtin.getattr(object, "__class__", None)
        assert obj_cls is None  # Blocked

        # Try to get __subclasses__ directly
        subclasses = builtin.getattr(object, "__subclasses__", None)
        assert subclasses is None  # Blocked

    def test_no_code_execution_via_getattr(self):
        """Verify getattr doesn't enable access to eval/exec."""
        # Even if we tried to get builtins
        import builtins as py_builtins

        # These should return None (not in whitelist)
        eval_func = builtin.getattr(py_builtins, "eval", None)
        assert eval_func is None  # Blocked

        exec_func = builtin.getattr(py_builtins, "exec", None)
        assert exec_func is None  # Blocked

        compile_func = builtin.getattr(py_builtins, "compile", None)
        assert compile_func is None  # Blocked

    def test_no_globals_access_via_function_introspection(self):
        """Verify function __globals__ is blocked."""
        def test_function():
            secret = "confidential"
            return secret

        # Try to access function internals
        globals_dict = builtin.getattr(test_function, "__globals__", None)
        assert globals_dict is None  # Blocked

        code = builtin.getattr(test_function, "__code__", None)
        assert code is None  # Blocked

    def test_no_module_file_path_leakage(self):
        """Verify __file__ and __path__ are blocked."""
        import os

        file_attr = builtin.getattr(os, "__file__", None)
        assert file_attr is None  # Blocked

    def test_hasattr_getattr_consistency(self):
        """Verify hasattr and getattr are consistent."""
        test_attrs = [
            ("hello", "upper", True),  # Safe
            ("hello", "__class__", False),  # Dangerous
            ([], "append", True),  # Safe
            ([], "__dict__", False),  # Dangerous
        ]

        for obj, attr, should_exist in test_attrs:
            has_it = builtin.hasattr(obj, attr)
            assert has_it == should_exist, \
                f"hasattr({obj}, {attr}) should be {should_exist}"

            # If hasattr returns True, getattr should work
            if has_it:
                result = builtin.getattr(obj, attr, None)
                assert result is not None
            else:
                # If hasattr returns False, getattr should return default
                result = builtin.getattr(obj, attr, "DEFAULT")
                assert result == "DEFAULT"

    # =====================================================================
    # call() Security Tests
    # =====================================================================

    def test_call_works_with_safe_functions(self):
        """Verify call() works correctly with safe ML functions."""
        # Call with lambda (user-defined function)
        result = builtin.call(lambda x: x * 2, 10)
        assert result == 20

        # Call with ML builtin.abs instead of Python abs
        result = builtin.call(builtin.abs, -5)
        assert result == 5

    def test_call_rejects_non_callable(self):
        """Verify call() rejects non-callable objects."""
        with pytest.raises(TypeError):
            builtin.call(42, "arg")

        with pytest.raises(TypeError):
            builtin.call("not a function")

    def test_call_cannot_bypass_security(self):
        """Verify call() doesn't enable access to blocked functions."""
        # Since we never expose eval/exec to ML code,
        # call() can't help an attacker
        # This test documents that call() is only as dangerous
        # as the functions available to it

        # call() with safe function works
        result = builtin.call(builtin.abs, -10)
        assert result == 10

        # But call() can't magically access eval
        # (because eval is never provided to ML code)

    def test_call_with_methods_obtained_via_getattr(self):
        """Verify call() works with methods from getattr."""
        # Get safe method via getattr
        upper_method = builtin.getattr("hello", "upper", None)
        assert upper_method is not None

        # Call it via call()
        result = builtin.call(upper_method)
        assert result == "HELLO"

    # =====================================================================
    # Combined Attack Scenarios
    # =====================================================================

    def test_combined_hasattr_getattr_call_attack(self):
        """Test combined attack using all three functions."""
        # Attacker tries to:
        # 1. Check if object has __class__
        has_class = builtin.hasattr("", "__class__")
        assert has_class is False  # Blocked

        # 2. Try to get __class__ anyway
        cls = builtin.getattr("", "__class__", None)
        assert cls is None  # Blocked

        # 3. Try to call something dangerous (can't because we don't have it)
        # This demonstrates defense in depth

    def test_whitelist_enforcement_comprehensive(self):
        """Comprehensive test of whitelist enforcement."""
        # Test various object types and attributes
        test_cases = [
            # (object, safe_attr, unsafe_attr)
            ("hello", "upper", "__class__"),
            ([1, 2, 3], "append", "__dict__"),
            ({"a": 1}, "keys", "__class__"),
            (42, None, "__class__"),  # int has no safe attrs in whitelist
        ]

        for obj, safe_attr, unsafe_attr in test_cases:
            # Unsafe attribute always blocked
            assert builtin.hasattr(obj, unsafe_attr) is False
            assert builtin.getattr(obj, unsafe_attr, "BLOCKED") == "BLOCKED"

            # Safe attribute works (if it exists)
            if safe_attr:
                assert builtin.hasattr(obj, safe_attr) is True
                assert builtin.getattr(obj, safe_attr) is not None


class TestSecurityRegressions:
    """Tests to prevent security regressions."""

    def test_no_private_attribute_leakage(self):
        """Verify private attributes are completely blocked."""
        class SecretClass:
            def __init__(self):
                self._private = "secret"
                self.__very_private = "top secret"

        obj = SecretClass()

        # Both should be blocked
        assert builtin.hasattr(obj, "_private") is False
        assert builtin.hasattr(obj, "__very_private") is False

        assert builtin.getattr(obj, "_private", "BLOCKED") == "BLOCKED"
        assert builtin.getattr(obj, "__very_private", "BLOCKED") == "BLOCKED"

    def test_no_timing_attack_via_hasattr(self):
        """Verify hasattr doesn't leak info via timing."""
        # Both dangerous attrs should return False immediately
        import time

        # Measure time for dangerous attribute
        start = time.time()
        for _ in range(1000):
            builtin.hasattr("test", "__class__")
        dangerous_time = time.time() - start

        # Measure time for non-existent safe attribute
        start = time.time()
        for _ in range(1000):
            builtin.hasattr("test", "nonexistent")
        safe_time = time.time() - start

        # Times should be similar (both check _ prefix first)
        # Not a strict requirement, but good defense
        assert abs(dangerous_time - safe_time) < 0.1

    def test_getattr_returns_default_not_none_on_error(self):
        """Verify getattr properly returns custom default."""
        # This prevents accidentally using None checks to probe for attributes
        custom_default = {"sentinel": "value"}

        result = builtin.getattr("test", "__class__", custom_default)
        assert result is custom_default
        assert result != None

    def test_no_import_mechanism_bypass(self):
        """Verify __import__ cannot be accessed."""
        import builtins as py_builtins

        # Try to get __import__
        import_func = builtin.getattr(py_builtins, "__import__", None)
        assert import_func is None  # Blocked
