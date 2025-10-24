"""Unit tests for runtime_helpers module - safe attribute access."""

import types

import pytest

from mlpy.stdlib.runtime_helpers import (
    SecurityError,
    get_object_type_name,
    get_safe_length,
    is_ml_object,
    safe_attr_access,
    safe_method_call,
)


class TestIsMLObject:
    """Test ML object detection."""

    def test_dict_with_string_keys_is_ml_object(self):
        """Test that dict with string keys is detected as ML object."""
        obj = {"name": "Alice", "age": 30}
        assert is_ml_object(obj) is True

    def test_empty_dict_is_ml_object(self):
        """Test that empty dict is ML object."""
        obj = {}
        assert is_ml_object(obj) is True

    def test_dict_with_non_string_keys_not_ml_object(self):
        """Test that dict with non-string keys is not ML object."""
        obj = {1: "one", 2: "two"}
        assert is_ml_object(obj) is False

    def test_dict_with_mixed_keys_not_ml_object(self):
        """Test that dict with mixed key types is not ML object."""
        obj = {"name": "Alice", 1: "one"}
        assert is_ml_object(obj) is False

    def test_non_dict_not_ml_object(self):
        """Test that non-dict objects are not ML objects."""
        assert is_ml_object([1, 2, 3]) is False
        assert is_ml_object("string") is False
        assert is_ml_object(42) is False
        assert is_ml_object(None) is False


class TestGetSafeLength:
    """Test safe length access function."""

    def test_length_of_list(self):
        """Test getting length of a list."""
        assert get_safe_length([1, 2, 3]) == 3

    def test_length_of_string(self):
        """Test getting length of a string."""
        assert get_safe_length("hello") == 5

    def test_length_of_dict(self):
        """Test getting length of a dict."""
        assert get_safe_length({"a": 1, "b": 2}) == 2

    def test_length_of_empty_list(self):
        """Test getting length of empty list."""
        assert get_safe_length([]) == 0

    def test_length_of_tuple(self):
        """Test getting length of tuple."""
        assert get_safe_length((1, 2, 3, 4)) == 4

    def test_length_of_object_without_len_raises_error(self):
        """Test that objects without len() raise TypeError."""
        with pytest.raises(TypeError) as exc_info:
            get_safe_length(42)
        assert "has no len()" in str(exc_info.value)


class TestGetObjectTypeName:
    """Test object type name retrieval."""

    def test_ml_object_type_name(self):
        """Test that ML objects return 'ML object'."""
        obj = {"name": "Alice"}
        assert get_object_type_name(obj) == "ML object"

    def test_list_type_name(self):
        """Test list type name."""
        assert get_object_type_name([1, 2, 3]) == "list"

    def test_string_type_name(self):
        """Test string type name."""
        assert get_object_type_name("hello") == "str"

    def test_int_type_name(self):
        """Test int type name."""
        assert get_object_type_name(42) == "int"

    def test_dict_with_non_string_keys_type_name(self):
        """Test that non-ML dict returns 'dict'."""
        obj = {1: "one", 2: "two"}
        assert get_object_type_name(obj) == "dict"


class TestSafeAttrAccessMLObjects:
    """Test safe attribute access on ML objects (dicts)."""

    def test_access_existing_property(self):
        """Test accessing existing property on ML object."""
        obj = {"name": "Alice", "age": 30}
        assert safe_attr_access(obj, "name") == "Alice"
        assert safe_attr_access(obj, "age") == 30

    def test_access_missing_property_returns_none(self):
        """Test that accessing missing property returns None."""
        obj = {"name": "Alice"}
        assert safe_attr_access(obj, "missing") is None

    def test_access_nested_object(self):
        """Test accessing property that is another ML object."""
        obj = {"user": {"name": "Bob"}}
        user = safe_attr_access(obj, "user")
        assert user == {"name": "Bob"}

    def test_access_array_property(self):
        """Test accessing property that is an array."""
        obj = {"items": [1, 2, 3]}
        items = safe_attr_access(obj, "items")
        assert items == [1, 2, 3]


class TestSafeAttrAccessBuiltInTypes:
    """Test safe attribute access on built-in Python types."""

    def test_access_string_method(self):
        """Test accessing method on string."""
        s = "hello"
        # Should return a callable wrapper
        upper_fn = safe_attr_access(s, "upper")
        assert callable(upper_fn)
        assert upper_fn() == "HELLO"

    def test_access_string_method_with_args(self):
        """Test accessing method with immediate call."""
        s = "hello world"
        result = safe_attr_access(s, "split", " ")
        assert result == ["hello", "world"]

    def test_access_list_method(self):
        """Test accessing method on list."""
        lst = [1, 2, 3]
        append_fn = safe_attr_access(lst, "append")
        assert callable(append_fn)
        append_fn(4)
        assert lst == [1, 2, 3, 4]

    def test_length_property_on_list(self):
        """Test that 'length' property maps to len()."""
        lst = [1, 2, 3, 4, 5]
        assert safe_attr_access(lst, "length") == 5

    def test_length_property_on_string(self):
        """Test that 'length' property works on strings."""
        s = "hello"
        assert safe_attr_access(s, "length") == 5

    def test_dangerous_dunder_attribute_raises_error(self):
        """Test that accessing dangerous dunder attributes is forbidden."""
        obj = "test"
        with pytest.raises(SecurityError) as exc_info:
            safe_attr_access(obj, "__class__")
        assert "dangerous attribute" in str(exc_info.value)

    def test_unsafe_attribute_raises_attribute_error(self):
        """Test that unsafe non-dunder attributes raise AttributeError."""
        # Attempt to access an attribute not in the safe registry
        obj = "test"
        # Most attributes should be safe on strings, but let's test with an object
        # that has no accessible attributes in the registry
        class CustomObject:
            def __init__(self):
                self.value = 42

        custom = CustomObject()
        with pytest.raises(AttributeError) as exc_info:
            safe_attr_access(custom, "value")
        assert "no accessible attribute" in str(exc_info.value)


class TestSafeAttrAccessModules:
    """Test safe attribute access on modules."""

    def test_access_module_attribute(self):
        """Test that module attributes are accessible."""
        import math

        pi_value = safe_attr_access(math, "pi")
        assert abs(pi_value - 3.14159) < 0.001

    def test_access_module_function(self):
        """Test that module functions are accessible."""
        import math

        sqrt_fn = safe_attr_access(math, "sqrt")
        assert callable(sqrt_fn)
        assert sqrt_fn(16) == 4.0


class TestSafeAttrAccessMLClass:
    """Test safe attribute access on @ml_class decorated objects."""

    def test_ml_class_attribute_access(self):
        """Test that @ml_class objects allow attribute access."""

        class Person:
            _ml_class_metadata = {"name": "Person"}

            def __init__(self, name):
                self.name = name

        person = Person("Alice")
        # Should allow access because of _ml_class_metadata
        result = safe_attr_access(person, "name")
        assert result == "Alice"


class TestSafeMethodCallMLObjects:
    """Test safe method calls on ML objects."""

    def test_call_function_property(self):
        """Test calling a function stored in ML object."""

        def greet(name):
            return f"Hello, {name}!"

        obj = {"greet": greet, "name": "Alice"}
        result = safe_method_call(obj, "greet", "Bob")
        assert result == "Hello, Bob!"

    def test_call_missing_method_raises_error(self):
        """Test that calling missing method raises AttributeError."""
        obj = {"name": "Alice"}
        with pytest.raises(AttributeError) as exc_info:
            safe_method_call(obj, "greet")
        assert "no property 'greet'" in str(exc_info.value)

    def test_call_non_callable_property_raises_error(self):
        """Test that calling non-callable property raises TypeError."""
        obj = {"name": "Alice"}
        with pytest.raises(TypeError) as exc_info:
            safe_method_call(obj, "name")
        assert "not callable" in str(exc_info.value)


class TestSafeMethodCallBuiltInTypes:
    """Test safe method calls on built-in types."""

    def test_call_string_method(self):
        """Test calling method on string."""
        s = "hello"
        result = safe_method_call(s, "upper")
        assert result == "HELLO"

    def test_call_string_method_with_args(self):
        """Test calling string method with arguments."""
        s = "hello world"
        result = safe_method_call(s, "replace", "world", "Python")
        assert result == "hello Python"

    def test_call_list_method(self):
        """Test calling method on list."""
        lst = [3, 1, 2]
        safe_method_call(lst, "sort")
        assert lst == [1, 2, 3]

    def test_unsafe_method_raises_error(self):
        """Test that unsafe methods raise AttributeError."""

        class CustomObject:
            def custom_method(self):
                return "hello"

        obj = CustomObject()
        with pytest.raises(AttributeError) as exc_info:
            safe_method_call(obj, "custom_method")
        assert "no accessible method" in str(exc_info.value)


class TestSafeMethodCallModules:
    """Test safe method calls on modules."""

    def test_call_module_function(self):
        """Test calling function on module."""
        import math

        result = safe_method_call(math, "sqrt", 16)
        assert result == 4.0


class TestSafeMethodCallMLClass:
    """Test safe method calls on @ml_class objects."""

    def test_ml_class_method_call(self):
        """Test that @ml_class methods are callable."""

        class Calculator:
            _ml_class_metadata = {"name": "Calculator"}

            def add(self, a, b):
                return a + b

        calc = Calculator()
        result = safe_method_call(calc, "add", 5, 3)
        assert result == 8


class TestUserModuleSupport:
    """Test support for user-defined modules."""

    def test_user_module_attribute_access(self):
        """Test that objects with _ml_user_module allow attribute access."""

        class UserModule:
            _ml_user_module = True

            def __init__(self):
                self.value = 42

        module = UserModule()
        result = safe_attr_access(module, "value")
        assert result == 42

    def test_user_module_method_call(self):
        """Test that objects with _ml_user_module allow method calls."""

        class UserModule:
            _ml_user_module = True

            def greet(self, name):
                return f"Hello, {name}!"

        module = UserModule()
        result = safe_method_call(module, "greet", "Alice")
        assert result == "Hello, Alice!"


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_attribute_error_when_attribute_missing(self):
        """Test AttributeError when attribute truly doesn't exist."""
        # Even for allowed types, if attribute doesn't exist, should raise
        s = "hello"
        with pytest.raises(AttributeError):
            safe_attr_access(s, "nonexistent_method")

    def test_method_call_attribute_error(self):
        """Test AttributeError in method call when method doesn't exist."""
        s = "hello"
        with pytest.raises(AttributeError):
            safe_method_call(s, "nonexistent_method")

    def test_callable_attribute_returns_wrapper(self):
        """Test that callable attributes return wrappers when called without args."""

        class TestObj:
            _ml_class_metadata = True

            def method(self):
                return "result"

        obj = TestObj()
        wrapper = safe_attr_access(obj, "method")
        assert callable(wrapper)
        assert wrapper() == "result"

    def test_attr_access_exception_handler_for_module(self):
        """Test exception handling when getattr fails on module."""
        import types

        # Create a module with no such attribute
        test_module = types.ModuleType("test_module")
        with pytest.raises(AttributeError) as exc_info:
            safe_attr_access(test_module, "nonexistent_attr")
        assert "has no attribute" in str(exc_info.value)

    def test_method_call_exception_handler_for_module(self):
        """Test exception handling when method doesn't exist on module."""
        import types

        test_module = types.ModuleType("test_module")
        with pytest.raises(AttributeError) as exc_info:
            safe_method_call(test_module, "nonexistent_method")
        assert "has no method" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
