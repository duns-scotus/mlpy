"""Tests for enhanced variable formatting in debugger."""

import pytest
from mlpy.debugging.variable_formatter import VariableFormatter, format_value, format_variable_with_type


class TestBasicFormatting:
    """Test basic value formatting."""

    def test_format_null(self):
        """Test null/None formatting."""
        formatter = VariableFormatter()
        assert formatter.format_value(None) == "null"

    def test_format_boolean(self):
        """Test boolean formatting."""
        formatter = VariableFormatter()
        assert formatter.format_value(True) == "true"
        assert formatter.format_value(False) == "false"

    def test_format_integer(self):
        """Test integer formatting."""
        formatter = VariableFormatter()
        assert formatter.format_value(42) == "42"
        assert formatter.format_value(0) == "0"
        assert formatter.format_value(-100) == "-100"

    def test_format_float(self):
        """Test float formatting."""
        formatter = VariableFormatter()
        assert formatter.format_value(3.14) == "3.14"
        assert formatter.format_value(10.0) == "10.0"
        assert formatter.format_value(0.123456789) == "0.123457"  # Rounded to 6 decimals

    def test_format_string(self):
        """Test string formatting."""
        formatter = VariableFormatter()
        assert formatter.format_value("hello") == "'hello'"
        assert formatter.format_value("") == "''"

    def test_format_string_with_quotes(self):
        """Test string with embedded quotes."""
        formatter = VariableFormatter()
        result = formatter.format_value("It's a test")
        assert "It's a test" in result


class TestArrayFormatting:
    """Test array/list formatting."""

    def test_format_empty_array(self):
        """Test empty array."""
        formatter = VariableFormatter()
        assert formatter.format_value([]) == "[]"

    def test_format_small_array(self):
        """Test small array on one line."""
        formatter = VariableFormatter()
        result = formatter.format_value([1, 2, 3])
        assert result == "[1, 2, 3]"

    def test_format_large_array(self):
        """Test large array with truncation."""
        formatter = VariableFormatter(max_array_items=3)
        result = formatter.format_value([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        assert "[" in result
        assert "1," in result
        assert "2," in result
        assert "3," in result
        assert "... 7 more items" in result

    def test_format_nested_array(self):
        """Test nested arrays."""
        formatter = VariableFormatter()
        result = formatter.format_value([[1, 2], [3, 4]])
        assert "[" in result
        assert "[1, 2]" in result or "1," in result

    def test_format_array_multiline(self):
        """Test multiline array formatting."""
        formatter = VariableFormatter(max_array_items=5)
        result = formatter.format_value([10, 20, 30, 40, 50])
        # Should be multiline for larger arrays
        assert "\n" in result or (len(result) < 60 and "[10, 20, 30, 40, 50]" == result)


class TestObjectFormatting:
    """Test object/dictionary formatting."""

    def test_format_empty_object(self):
        """Test empty object."""
        formatter = VariableFormatter()
        assert formatter.format_value({}) == "{}"

    def test_format_small_object(self):
        """Test small object on one line."""
        formatter = VariableFormatter()
        result = formatter.format_value({"name": "Alice", "age": 30})
        # Small objects should be on one line or multiline
        assert "{" in result
        assert "name" in result
        assert "Alice" in result

    def test_format_large_object(self):
        """Test large object with truncation."""
        formatter = VariableFormatter(max_dict_items=2)
        obj = {f"key{i}": i for i in range(10)}
        result = formatter.format_value(obj)
        assert "{" in result
        assert "... 8 more properties" in result

    def test_format_nested_object(self):
        """Test nested objects."""
        formatter = VariableFormatter()
        obj = {"user": {"name": "Bob", "age": 25}}
        result = formatter.format_value(obj)
        assert "user" in result
        assert "name" in result or "Bob" in result


class TestDepthLimiting:
    """Test depth limiting for nested structures."""

    def test_depth_limit_array(self):
        """Test depth limit on nested arrays."""
        formatter = VariableFormatter(max_depth=2)
        nested = [[[1, 2, 3]]]
        result = formatter.format_value(nested)
        # At max depth, should show truncated form
        assert "<array" in result or "[[[" not in result

    def test_depth_limit_object(self):
        """Test depth limit on nested objects."""
        formatter = VariableFormatter(max_depth=2)
        nested = {"a": {"b": {"c": {"d": 1}}}}
        result = formatter.format_value(nested)
        # At max depth, should show truncated form
        assert "<object" in result or "d" not in result


class TestStringTruncation:
    """Test string truncation for long values."""

    def test_long_string_truncated(self):
        """Test that long strings are truncated."""
        formatter = VariableFormatter(max_string_length=20)
        long_string = "a" * 100
        result = formatter.format_value(long_string)
        assert "..." in result
        assert len(result) < 100

    def test_short_string_not_truncated(self):
        """Test that short strings are not truncated."""
        formatter = VariableFormatter(max_string_length=100)
        short_string = "hello world"
        result = formatter.format_value(short_string)
        assert "..." not in result
        assert "hello world" in result


class TestFunctionFormatting:
    """Test function value formatting."""

    def test_format_function(self):
        """Test function formatting."""
        formatter = VariableFormatter()

        def my_function():
            pass

        result = formatter.format_value(my_function)
        assert "<function" in result
        assert "my_function" in result

    def test_format_lambda(self):
        """Test lambda formatting."""
        formatter = VariableFormatter()
        result = formatter.format_value(lambda x: x + 1)
        assert "<function" in result


class TestTypeDetection:
    """Test ML type detection."""

    def test_type_null(self):
        """Test null type detection."""
        formatter = VariableFormatter()
        assert formatter.format_type(None) == "null"

    def test_type_boolean(self):
        """Test boolean type detection."""
        formatter = VariableFormatter()
        assert formatter.format_type(True) == "boolean"
        assert formatter.format_type(False) == "boolean"

    def test_type_number(self):
        """Test number type detection."""
        formatter = VariableFormatter()
        assert formatter.format_type(42) == "number"
        assert formatter.format_type(3.14) == "number"

    def test_type_string(self):
        """Test string type detection."""
        formatter = VariableFormatter()
        assert formatter.format_type("hello") == "string"

    def test_type_array(self):
        """Test array type detection."""
        formatter = VariableFormatter()
        assert formatter.format_type([1, 2, 3]) == "array"

    def test_type_object(self):
        """Test object type detection."""
        formatter = VariableFormatter()
        assert formatter.format_type({"key": "value"}) == "object"

    def test_type_function(self):
        """Test function type detection."""
        formatter = VariableFormatter()
        assert formatter.format_type(lambda: None) == "function"


class TestConvenienceFunctions:
    """Test convenience functions."""

    def test_format_value_function(self):
        """Test the format_value convenience function."""
        result = format_value([1, 2, 3])
        assert "[1, 2, 3]" in result

    def test_format_variable_with_type(self):
        """Test format_variable_with_type function."""
        result = format_variable_with_type("count", 42)
        assert "count" in result
        assert "number" in result
        assert "42" in result

    def test_format_variable_with_type_multiline(self):
        """Test format_variable_with_type with multiline values."""
        large_array = list(range(20))
        result = format_variable_with_type("items", large_array)
        assert "items" in result
        assert "array" in result
        # Should handle multiline formatting
        assert "\n" in result or len(large_array) <= 3


class TestComplexScenarios:
    """Test complex real-world scenarios."""

    def test_mixed_nested_structure(self):
        """Test complex nested structure."""
        formatter = VariableFormatter()
        data = {
            "users": [
                {"name": "Alice", "age": 30, "active": True},
                {"name": "Bob", "age": 25, "active": False},
            ],
            "count": 2,
            "status": "active",
        }
        result = formatter.format_value(data)
        # Should format without errors
        assert "{" in result
        assert "users" in result

    def test_deeply_nested_truncation(self):
        """Test deeply nested structure truncation."""
        formatter = VariableFormatter(max_depth=3)

        # Create deeply nested structure
        data = {"level1": {"level2": {"level3": {"level4": {"level5": "deep"}}}}}

        result = formatter.format_value(data)
        # Should truncate at max depth
        assert "<object" in result or "level5" not in result
