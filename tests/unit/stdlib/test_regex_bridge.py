"""Unit tests for regex_bridge module migration."""

import pytest
from mlpy.stdlib.regex_bridge import Regex, Pattern, regex
from mlpy.stdlib.decorators import get_module_metadata, _MODULE_REGISTRY


class TestRegexModuleRegistration:
    """Test that Regex module is properly registered with decorators."""

    def test_regex_module_registered(self):
        """Test that regex module is in global registry."""
        assert "regex" in _MODULE_REGISTRY
        assert _MODULE_REGISTRY["regex"] == Regex

    def test_regex_module_metadata(self):
        """Test regex module metadata is correct."""
        metadata = get_module_metadata("regex")
        assert metadata is not None
        assert metadata.name == "regex"
        assert metadata.description == "Regular expression pattern matching with full Python re module support"
        assert metadata.version == "2.0.0"

    def test_regex_has_function_metadata(self):
        """Test that regex module has registered functions."""
        metadata = get_module_metadata("regex")

        # Check key methods are registered (using actual snake_case names)
        assert "compile" in metadata.functions
        assert "test" in metadata.functions
        assert "match" in metadata.functions
        assert "findall" in metadata.functions  # snake_case
        assert "split" in metadata.functions
        assert "escape" in metadata.functions
        assert "isValid" in metadata.functions

        # Should have multiple functions
        assert len(metadata.functions) >= 10


class TestRegexBasicOperations:
    """Test basic regex operations."""

    def test_regex_test(self):
        """Test regex.test() method."""
        assert regex.test("hello", "hello world") is True
        assert regex.test("goodbye", "hello world") is False
        assert regex.test("\\d+", "abc 123") is True
        assert regex.test("\\d+", "abc") is False

    def test_regex_search(self):
        """Test regex.search() method returns Match object."""
        match_obj = regex.search("\\d+", "abc 123 def")
        assert match_obj is not None
        assert match_obj.group(0) == "123"

        match_obj = regex.search("\\d+", "abc")
        assert match_obj is None

    def test_regex_find_all(self):
        """Test regex.findall() method (snake_case)."""
        results = regex.findall("\\d+", "a1 b2 c3")
        assert results == ["1", "2", "3"]

        results = regex.findall("\\d+", "abc")
        assert results == []

    def test_regex_sub(self):
        """Test regex.sub() method (replaces first match)."""
        result = regex.sub("\\d+", "X", "a1 b2 c3")
        assert result == "aX bX cX"  # sub replaces all by default in Python re

    def test_regex_split(self):
        """Test regex.split() method."""
        results = regex.split(",\\s*", "a, b,  c,d")
        assert results == ["a", "b", "c", "d"]

    def test_regex_count(self):
        """Test regex.count() method."""
        count = regex.count("\\d+", "a1 b2 c3")
        assert count == 3

        count = regex.count("\\d+", "abc")
        assert count == 0


class TestPatternClass:
    """Test Pattern class OOP functionality."""

    def test_pattern_compile(self):
        """Test compiling a pattern."""
        pattern = regex.compile("\\d+")
        assert isinstance(pattern, Pattern)
        assert pattern.pattern == "\\d+"

    def test_pattern_test(self):
        """Test Pattern.test() method."""
        pattern = regex.compile("\\d+")
        assert pattern.test("abc 123") is True
        assert pattern.test("abc") is False

    def test_pattern_search(self):
        """Test Pattern.search() method returns Match."""
        pattern = regex.compile("\\d+")
        match_obj = pattern.search("abc 123 def")
        assert match_obj is not None
        assert match_obj.group(0) == "123"

        match_obj = pattern.search("abc")
        assert match_obj is None

    def test_pattern_find_all(self):
        """Test Pattern.findall() method (snake_case)."""
        pattern = regex.compile("\\d+")
        results = pattern.findall("a1 b2 c3")
        assert results == ["1", "2", "3"]

    def test_pattern_sub(self):
        """Test Pattern.sub() method."""
        pattern = regex.compile("\\d+")
        result = pattern.sub("X", "a1 b2")
        assert result == "aX bX"

    def test_pattern_split(self):
        """Test Pattern.split() method."""
        pattern = regex.compile(",\\s*")
        results = pattern.split("a, b,  c")
        assert results == ["a", "b", "c"]

    def test_pattern_count(self):
        """Test Pattern.count() method."""
        pattern = regex.compile("\\d+")
        count = pattern.count("a1 b2 c3")
        assert count == 3

    def test_pattern_to_string(self):
        """Test Pattern.toString() method."""
        pattern = regex.compile("\\d+")
        result = pattern.toString()
        assert "\\d+" in result


class TestRegexUtilityMethods:
    """Test regex utility and convenience methods."""

    def test_escape(self):
        """Test regex.escape() method."""
        result = regex.escape("Price: $5.99")
        assert "$" in result
        assert "\\" in result  # Escaped

    def test_is_valid(self):
        """Test regex.isValid() method."""
        assert regex.isValid("\\d+") is True
        assert regex.isValid("[a-z]+") is True
        assert regex.isValid("(unclosed") is False
        assert regex.isValid("[unclosed") is False


class TestRegexInstance:
    """Test global regex instance."""

    def test_regex_is_instance_of_regex_class(self):
        """Test that regex is an instance of Regex."""
        assert isinstance(regex, Regex)

    def test_regex_has_decorated_methods(self):
        """Test that regex instance has decorated methods with metadata."""
        assert hasattr(regex, "compile")
        assert hasattr(regex, "test")
        assert hasattr(regex, "match")

        # Check they have metadata
        assert hasattr(regex.compile, "_ml_function_metadata")
        assert hasattr(regex.test, "_ml_function_metadata")
        assert hasattr(regex.match, "_ml_function_metadata")


class TestPatternMetadata:
    """Test Pattern class metadata."""

    def test_pattern_class_has_metadata(self):
        """Test that Pattern class has metadata."""
        assert hasattr(Pattern, "_ml_class_metadata")

    def test_pattern_methods_have_metadata(self):
        """Test that Pattern methods have metadata."""
        pattern = regex.compile("test")
        assert hasattr(pattern.test, "_ml_function_metadata")
        # Use actual method names that exist
        assert hasattr(pattern.findall, "_ml_function_metadata")
        assert hasattr(pattern.sub, "_ml_function_metadata")


class TestRegexErrorHandling:
    """Test error handling for invalid patterns."""

    def test_invalid_pattern_compile(self):
        """Test that invalid pattern raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            regex.compile("(unclosed")
        assert "Invalid regex pattern" in str(exc_info.value)

    def test_invalid_pattern_test(self):
        """Test that invalid pattern in test() raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            regex.test("(unclosed", "text")
        assert "Invalid regex pattern" in str(exc_info.value)
