"""Unit tests for regex_bridge module migration."""

import pytest
from mlpy.stdlib.regex_bridge import Regex, Pattern, regex
from mlpy.stdlib.decorators import get_module_metadata
from mlpy.stdlib.module_registry import get_registry


class TestRegexModuleRegistration:
    """Test that Regex module is properly registered."""

    def test_regex_module_registered(self):
        """Test that regex module is available in registry."""
        registry = get_registry()
        assert registry.is_available("regex")
        regex_instance = registry.get_module("regex")
        assert regex_instance is not None
        assert type(regex_instance).__name__ == "Regex"

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


class TestRegexMissingCoverage:
    """Test cases to improve regex_bridge coverage."""

    def test_match_groups(self):
        """Test Match.groups() method."""
        pattern = regex.compile(r"(\w+) (\w+)")
        match = pattern.search("hello world")
        groups = match.groups()
        assert groups == ["hello", "world"]

    def test_match_groupdict_with_named_groups(self):
        """Test Match.groupDict() with named groups."""
        pattern = regex.compile(r"(?P<first>\w+) (?P<second>\w+)")
        match = pattern.search("hello world")
        group_dict = match.groupDict()
        assert group_dict["first"] == "hello"
        assert group_dict["second"] == "world"

    def test_match_groupdict_with_default(self):
        """Test Match.groupDict() with default value."""
        pattern = regex.compile(r"(?P<first>\w+)(?: (?P<second>\w+))?")
        match = pattern.search("hello")
        group_dict = match.groupDict("N/A")
        assert group_dict["first"] == "hello"
        assert group_dict["second"] == "N/A"

    def test_match_value(self):
        """Test Match.value() method."""
        pattern = regex.compile(r"\w+")
        match = pattern.search("hello world")
        assert match.value() == "hello"

    def test_match_last_group(self):
        """Test Match.lastGroup() method."""
        pattern = regex.compile(r"(?P<first>\w+) (?P<second>\w+)")
        match = pattern.search("hello world")
        last_group = match.lastGroup()
        assert last_group == "second"

    def test_match_group_count(self):
        """Test Match.groupCount() method."""
        pattern = regex.compile(r"(\w+) (\w+) (\w+)")
        match = pattern.search("one two three")
        assert match.groupCount() == 3

    def test_pattern_finditer(self):
        """Test Pattern.finditer() method."""
        pattern = regex.compile(r"\d+")
        matches = pattern.finditer("There are 123 apples and 456 oranges")
        assert len(matches) == 2
        assert matches[0].value() == "123"
        assert matches[1].value() == "456"

    def test_pattern_split(self):
        """Test Pattern.split() method."""
        pattern = regex.compile(r"[,\s]+")
        result = pattern.split("apple, banana,  cherry")
        assert "apple" in result
        assert "banana" in result
        assert "cherry" in result

    def test_pattern_split_with_max(self):
        """Test Pattern.split() with maxsplit parameter."""
        pattern = regex.compile(r"\s+")
        result = pattern.split("one two three four", 2)
        assert len(result) == 3

    def test_regex_escape(self):
        """Test regex.escape() method."""
        special_chars = "a.b*c?"
        escaped = regex.escape(special_chars)
        assert r"\." in escaped
        assert r"\*" in escaped
        assert r"\?" in escaped

    def test_regex_match_method(self):
        """Test regex.match() standalone method."""
        pattern = regex.compile(r"^\w+")
        match = pattern.match("hello world")
        assert match is not None
        assert match.value() == "hello"

    def test_regex_match_no_match(self):
        """Test regex.match() returns None when no match."""
        pattern = regex.compile(r"^\d+")
        match = pattern.match("hello world")
        assert match is None

    def test_regex_search_method(self):
        """Test Pattern.search() method."""
        pattern = regex.compile(r"\d+")
        match = pattern.search("There are 123 apples")
        assert match is not None
        assert match.value() == "123"

    def test_regex_findall_standalone(self):
        """Test regex.findall() standalone method."""
        matches = regex.findall(r"\d+", "1 apple, 2 bananas, 3 cherries")
        assert len(matches) == 3
        assert "1" in matches
        assert "2" in matches
        assert "3" in matches

    def test_regex_sub_standalone(self):
        """Test regex.sub() standalone method."""
        result = regex.sub(r"\d+", "X", "There are 123 apples and 456 oranges")
        assert "X" in result
        assert "123" not in result
        assert "456" not in result

    def test_regex_split_standalone(self):
        """Test regex.split() standalone method."""
        result = regex.split(r"\s+", "one two three")
        assert len(result) == 3
        assert "one" in result
        assert "two" in result

    def test_pattern_fullmatch(self):
        """Test Pattern.fullmatch() method."""
        pattern = regex.compile(r"\w+")
        match = pattern.fullmatch("hello")
        assert match is not None
        match_partial = pattern.fullmatch("hello world")
        assert match_partial is None  # fullmatch requires complete match

    def test_pattern_subn(self):
        """Test Pattern.subn() method that returns count."""
        pattern = regex.compile(r"\d+")
        result = pattern.subn("X", "There are 123 apples and 456 oranges")
        assert "result" in result
        assert "count" in result
        assert result["count"] == 2

    def test_pattern_count(self):
        """Test Pattern.count() method."""
        pattern = regex.compile(r"\d+")
        count = pattern.count("1 apple, 2 bananas, 3 cherries")
        assert count == 3

    def test_pattern_get_pattern(self):
        """Test Pattern.getPattern() method."""
        pattern = regex.compile(r"\d+")
        pattern_str = pattern.getPattern()
        assert pattern_str == r"\d+"

    def test_pattern_get_flags(self):
        """Test Pattern.getFlags() method."""
        pattern = regex.compile(r"test", regex.IGNORECASE())
        flags = pattern.getFlags()
        assert flags is not None

    def test_match_start(self):
        """Test Match.start() method."""
        pattern = regex.compile(r"\d+")
        match = pattern.search("abc 123 def")
        start_pos = match.start()
        assert start_pos == 4

    def test_match_end(self):
        """Test Match.end() method."""
        pattern = regex.compile(r"\d+")
        match = pattern.search("abc 123 def")
        end_pos = match.end()
        assert end_pos == 7

    def test_match_span(self):
        """Test Match.span() method."""
        pattern = regex.compile(r"\d+")
        match = pattern.search("abc 123 def")
        span = match.span()
        assert span == [4, 7]

    def test_match_expand(self):
        """Test Match.expand() method with template."""
        pattern = regex.compile(r"(\w+) (\w+)")
        match = pattern.search("hello world")
        expanded = match.expand(r"\2 \1")
        assert "world hello" in expanded

    def test_match_group_invalid_index(self):
        """Test Match.group() with invalid group index returns None."""
        pattern = regex.compile(r"(\w+)")
        match = pattern.search("hello")
        # Request group 99 which doesn't exist
        result = match.group(99)
        assert result is None

    def test_match_group_invalid_name(self):
        """Test Match.group() with invalid group name returns None."""
        pattern = regex.compile(r"(?P<word>\w+)")
        match = pattern.search("hello")
        # Request non-existent named group
        result = match.group("nonexistent")
        assert result is None

    def test_match_start_invalid_group(self):
        """Test Match.start() with invalid group returns -1."""
        pattern = regex.compile(r"(\w+)")
        match = pattern.search("hello")
        # Request start of non-existent group
        result = match.start(99)
        assert result == -1

    def test_match_end_invalid_group(self):
        """Test Match.end() with invalid group returns -1."""
        pattern = regex.compile(r"(\w+)")
        match = pattern.search("hello")
        # Request end of non-existent group
        result = match.end(99)
        assert result == -1

    def test_match_span_invalid_group(self):
        """Test Match.span() with invalid group returns [-1, -1]."""
        pattern = regex.compile(r"(\w+)")
        match = pattern.search("hello")
        # Request span of non-existent group
        result = match.span(99)
        assert result == [-1, -1]
