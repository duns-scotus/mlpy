"""Unit tests for string_bridge module migration."""

import pytest
from mlpy.stdlib.string_bridge import String, string
from mlpy.stdlib.decorators import get_module_metadata, _MODULE_REGISTRY


class TestStringModuleRegistration:
    """Test that String module is properly registered with decorators."""

    def test_string_module_registered(self):
        """Test that string module is in global registry."""
        assert "string" in _MODULE_REGISTRY
        assert _MODULE_REGISTRY["string"] == String

    def test_string_module_metadata(self):
        """Test string module metadata is correct."""
        metadata = get_module_metadata("string")
        assert metadata is not None
        assert metadata.name == "string"
        assert metadata.description == "String manipulation and utility functions"
        assert "string.read" in metadata.capabilities
        assert metadata.version == "1.0.0"

    def test_string_has_function_metadata(self):
        """Test that string module has many registered functions."""
        metadata = get_module_metadata("string")

        # Check some key methods are registered
        assert "upper" in metadata.functions
        assert "lower" in metadata.functions
        assert "reverse" in metadata.functions
        assert "split" in metadata.functions
        assert "join" in metadata.functions
        assert "trim" in metadata.functions
        assert "replace" in metadata.functions

        # Should have many functions (70+)
        assert len(metadata.functions) > 50

    def test_string_function_capabilities(self):
        """Test that string functions have correct capabilities."""
        metadata = get_module_metadata("string")

        # All string functions require string.read
        assert metadata.functions["upper"].capabilities == ["string.read"]
        assert metadata.functions["lower"].capabilities == ["string.read"]
        assert metadata.functions["reverse"].capabilities == ["string.read"]


class TestStringCoreFunctionality:
    """Test core string manipulation functions."""

    def test_string_upper(self):
        """Test string.upper() converts to uppercase."""
        result = string.upper("hello")
        assert result == "HELLO"

    def test_string_lower(self):
        """Test string.lower() converts to lowercase."""
        result = string.lower("WORLD")
        assert result == "world"

    def test_string_capitalize(self):
        """Test string.capitalize() capitalizes first character."""
        result = string.capitalize("hello")
        assert result == "Hello"

    def test_string_reverse(self):
        """Test string.reverse() reverses string."""
        result = string.reverse("hello")
        assert result == "olleh"

    def test_string_repeat(self):
        """Test string.repeat() repeats string."""
        result = string.repeat("ab", 3)
        assert result == "ababab"

    def test_string_length(self):
        """Test string.length() returns correct length."""
        result = string.length("hello")
        assert result == 5


class TestStringCaseConversion:
    """Test case conversion functions."""

    def test_to_camel_case(self):
        """Test toCamelCase conversion."""
        result = string.toCamelCase("hello_world")
        assert result == "helloWorld"

    def test_to_pascal_case(self):
        """Test toPascalCase conversion."""
        result = string.toPascalCase("hello_world")
        assert result == "HelloWorld"

    def test_to_snake_case(self):
        """Test toSnakeCase conversion."""
        result = string.toSnakeCase("helloWorld")
        assert result == "hello_world"

    def test_to_kebab_case(self):
        """Test toKebabCase conversion."""
        result = string.toKebabCase("helloWorld")
        assert result == "hello-world"


class TestStringSearchAndValidation:
    """Test string search and validation functions."""

    def test_starts_with(self):
        """Test startsWith() detection."""
        assert string.startsWith("hello world", "hello") is True
        assert string.startsWith("hello world", "world") is False

    def test_ends_with(self):
        """Test endsWith() detection."""
        assert string.endsWith("hello world", "world") is True
        assert string.endsWith("hello world", "hello") is False

    def test_contains(self):
        """Test contains() detection."""
        assert string.contains("hello world", "lo wo") is True
        assert string.contains("hello world", "xyz") is False

    def test_is_empty(self):
        """Test isEmpty() validation."""
        assert string.isEmpty("") is True
        assert string.isEmpty("hello") is False

    def test_is_alpha(self):
        """Test isAlpha() validation."""
        assert string.isAlpha("hello") is True
        assert string.isAlpha("hello123") is False

    def test_is_numeric(self):
        """Test isNumeric() validation."""
        assert string.isNumeric("123") is True
        assert string.isNumeric("abc") is False


class TestStringSplitJoin:
    """Test string splitting and joining functions."""

    def test_split(self):
        """Test split() with delimiter."""
        result = string.split("a,b,c", ",")
        assert result == ["a", "b", "c"]

    def test_split_empty_delimiter(self):
        """Test split() with empty delimiter."""
        result = string.split("abc", "")
        assert result == ["a", "b", "c"]

    def test_join(self):
        """Test join() with delimiter."""
        result = string.join(",", ["a", "b", "c"])
        assert result == "a,b,c"


class TestStringTrimAndPad:
    """Test string trimming and padding functions."""

    def test_trim(self):
        """Test trim() removes whitespace."""
        result = string.trim("  hello  ")
        assert result == "hello"

    def test_lstrip(self):
        """Test lstrip() removes left whitespace."""
        result = string.lstrip("  hello  ")
        assert result == "hello  "

    def test_rstrip(self):
        """Test rstrip() removes right whitespace."""
        result = string.rstrip("  hello  ")
        assert result == "  hello"

    def test_pad_left(self):
        """Test padLeft() pads on left."""
        result = string.padLeft("hi", 5)
        assert result == "   hi"

    def test_pad_right(self):
        """Test padRight() pads on right."""
        result = string.padRight("hi", 5)
        assert result == "hi   "

    def test_pad_center(self):
        """Test padCenter() centers string."""
        result = string.padCenter("hi", 6)
        assert result == "  hi  "


class TestStringConversion:
    """Test string type conversion functions."""

    def test_to_int(self):
        """Test toInt() conversion."""
        result = string.toInt("123")
        assert result == 123

    def test_to_int_invalid(self):
        """Test toInt() returns 0 for invalid input."""
        result = string.toInt("abc")
        assert result == 0

    def test_to_float(self):
        """Test toFloat() conversion."""
        result = string.toFloat("12.5")
        assert result == 12.5

    def test_to_float_invalid(self):
        """Test toFloat() returns 0.0 for invalid input."""
        result = string.toFloat("abc")
        assert result == 0.0

    def test_to_string_bool(self):
        """Test toString() converts boolean correctly."""
        assert string.toString(True) == "true"
        assert string.toString(False) == "false"


class TestStringReplacementAndSearch:
    """Test string replacement and search functions."""

    def test_replace(self):
        """Test replace() replaces first occurrence."""
        result = string.replace("hello hello", "hello", "hi")
        assert result == "hi hello"

    def test_replace_all(self):
        """Test replaceAll() replaces all occurrences."""
        result = string.replaceAll("hello hello", "hello", "hi")
        assert result == "hi hi"

    def test_find(self):
        """Test find() returns index of substring."""
        result = string.find("hello world", "world")
        assert result == 6

    def test_find_not_found(self):
        """Test find() returns -1 when not found."""
        result = string.find("hello world", "xyz")
        assert result == -1

    def test_count(self):
        """Test count() counts occurrences."""
        result = string.count("hello hello hello", "hello")
        assert result == 3


class TestStringInstance:
    """Test global string instance."""

    def test_string_is_instance_of_string_class(self):
        """Test that string is an instance of String."""
        assert isinstance(string, String)

    def test_string_has_decorated_methods(self):
        """Test that string instance has decorated methods with metadata."""
        assert hasattr(string, "upper")
        assert hasattr(string, "lower")
        assert hasattr(string, "reverse")

        # Check they have metadata
        assert hasattr(string.upper, "_ml_function_metadata")
        assert hasattr(string.lower, "_ml_function_metadata")
        assert hasattr(string.reverse, "_ml_function_metadata")
