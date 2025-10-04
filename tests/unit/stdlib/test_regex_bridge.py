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
        assert metadata.description == "Regular expression pattern matching and text manipulation"
        assert "regex.compile" in metadata.capabilities
        assert "regex.match" in metadata.capabilities
        assert metadata.version == "1.0.0"

    def test_regex_has_function_metadata(self):
        """Test that regex module has registered functions."""
        metadata = get_module_metadata("regex")

        # Check key methods are registered
        assert "compile" in metadata.functions
        assert "test" in metadata.functions
        assert "match" in metadata.functions
        assert "findAll" in metadata.functions
        assert "replace" in metadata.functions
        assert "replaceAll" in metadata.functions
        assert "split" in metadata.functions
        assert "escape" in metadata.functions
        assert "isValid" in metadata.functions

        # Should have many functions (20+)
        assert len(metadata.functions) >= 20


class TestRegexBasicOperations:
    """Test basic regex operations."""

    def test_regex_test(self):
        """Test regex.test() method."""
        assert regex.test("hello", "hello world") is True
        assert regex.test("goodbye", "hello world") is False
        assert regex.test("\\d+", "abc 123") is True
        assert regex.test("\\d+", "abc") is False

    def test_regex_match(self):
        """Test regex.match() method."""
        result = regex.match("\\d+", "abc 123 def")
        assert result == "123"

        result = regex.match("\\d+", "abc")
        assert result is None

    def test_regex_find_all(self):
        """Test regex.findAll() method."""
        results = regex.findAll("\\d+", "a1 b2 c3")
        assert results == ["1", "2", "3"]

        results = regex.findAll("\\d+", "abc")
        assert results == []

    def test_regex_replace(self):
        """Test regex.replace() method."""
        result = regex.replace("\\d+", "a1 b2 c3", "X")
        assert result == "aX b2 c3"  # Only first match

    def test_regex_replace_all(self):
        """Test regex.replaceAll() method."""
        result = regex.replaceAll("\\d+", "a1 b2 c3", "X")
        assert result == "aX bX cX"  # All matches

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

    def test_pattern_match(self):
        """Test Pattern.match() method."""
        pattern = regex.compile("\\d+")
        result = pattern.match("abc 123 def")
        assert result == "123"

        result = pattern.match("abc")
        assert result is None

    def test_pattern_find_all(self):
        """Test Pattern.findAll() method."""
        pattern = regex.compile("\\d+")
        results = pattern.findAll("a1 b2 c3")
        assert results == ["1", "2", "3"]

    def test_pattern_replace(self):
        """Test Pattern.replace() method."""
        pattern = regex.compile("\\d+")
        result = pattern.replace("a1 b2", "X")
        assert result == "aX b2"

    def test_pattern_replace_all(self):
        """Test Pattern.replaceAll() method."""
        pattern = regex.compile("\\d+")
        result = pattern.replaceAll("a1 b2 c3", "X")
        assert result == "aX bX cX"

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

    def test_email_pattern(self):
        """Test regex.emailPattern() method."""
        pattern = regex.emailPattern()
        assert isinstance(pattern, Pattern)
        assert pattern.test("user@example.com") is True
        assert pattern.test("invalid") is False

    def test_extract_emails(self):
        """Test regex.extractEmails() method."""
        text = "Contact us at support@example.com or sales@company.org"
        emails = regex.extractEmails(text)
        assert len(emails) == 2
        assert "support@example.com" in emails
        assert "sales@company.org" in emails

    def test_extract_phone_numbers(self):
        """Test regex.extractPhoneNumbers() method."""
        text = "Call 555-123-4567 or (555) 987-6543"
        phones = regex.extractPhoneNumbers(text)
        assert len(phones) >= 1  # At least one phone number found

    def test_is_url(self):
        """Test regex.isUrl() method."""
        assert regex.isUrl("https://example.com") is True
        assert regex.isUrl("http://example.com/path") is True
        assert regex.isUrl("not a url") is False

    def test_remove_html_tags(self):
        """Test regex.removeHtmlTags() method."""
        html = "<p>Hello <strong>world</strong>!</p>"
        result = regex.removeHtmlTags(html)
        assert result == "Hello world!"
        assert "<" not in result
        assert ">" not in result


class TestRegexSnakeCaseAliases:
    """Test snake_case aliases for all methods."""

    def test_find_all_alias(self):
        """Test find_all() alias."""
        results = regex.findAll("\\d+", "a1 b2")
        assert results == ["1", "2"]

    def test_replace_all_alias(self):
        """Test replace_all() alias."""
        result = regex.replaceAll("\\d+", "a1 b2", "X")
        assert result == "aX bX"

    def test_find_first_alias(self):
        """Test find_first() alias."""
        result = regex.find_first("\\d+", "a1 b2")
        assert result == "1"


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
        assert hasattr(pattern.findAll, "_ml_function_metadata")
        assert hasattr(pattern.replace, "_ml_function_metadata")


class TestRegexErrorHandling:
    """Test error handling for invalid patterns."""

    def test_invalid_pattern_compile(self):
        """Test that invalid pattern raises RuntimeError."""
        with pytest.raises(RuntimeError) as exc_info:
            regex.compile("(unclosed")
        assert "Invalid regex pattern" in str(exc_info.value)

    def test_invalid_pattern_test(self):
        """Test that invalid pattern in test() raises RuntimeError."""
        with pytest.raises(RuntimeError) as exc_info:
            regex.test("(unclosed", "text")
        assert "Invalid regex pattern" in str(exc_info.value)
