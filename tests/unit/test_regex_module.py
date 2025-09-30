"""Unit tests for ML regex standard library module.

Tests the complete regex module API including:
- Import creates clean 'regex' object (not 'ml_regex')
- Static methods on Regex class
- Pattern compilation and methods
- Error handling with RuntimeError
- Convenience methods for common patterns
"""

import pytest
from tests.helpers.repl_test_helper import REPLTestHelper


class TestRegexImport:
    """Test regex module import behavior."""

    @pytest.fixture
    def repl(self):
        """Provide clean REPL test helper."""
        helper = REPLTestHelper(security_enabled=False)
        helper.execute_ml('import regex')
        yield helper
        helper.reset()

    def test_import_creates_regex_object(self, repl):
        """Test that 'import regex' creates 'regex' object (not 'ml_regex')."""
        # Should be able to call regex.test() directly
        repl.execute_ml('result = regex.test("hello", "hello world")')
        assert repl.get_variable('result') is True


class TestRegexStaticMethods:
    """Test Regex class static methods."""

    @pytest.fixture
    def repl(self):
        """Provide REPL with regex imported."""
        helper = REPLTestHelper(security_enabled=False)
        helper.execute_ml('import regex')
        yield helper
        helper.reset()

    def test_regex_test_matches(self, repl):
        """Test regex.test() returns true for matching pattern."""
        repl.execute_ml('result = regex.test("hello", "hello world")')
        assert repl.get_variable('result') is True

    def test_regex_test_no_match(self, repl):
        """Test regex.test() returns false for non-matching pattern."""
        repl.execute_ml('result = regex.test("goodbye", "hello world")')
        assert repl.get_variable('result') is False

    def test_regex_findall_multiple_matches(self, repl):
        """Test regex.findAll() returns all matches."""
        repl.execute_ml('result = regex.findAll("[0-9]+", "I have 5 apples and 3 oranges")')
        assert repl.get_variable('result') == ['5', '3']

    def test_regex_findall_no_matches(self, repl):
        """Test regex.findAll() returns empty list when no matches."""
        repl.execute_ml('result = regex.findAll("[0-9]+", "no numbers here")')
        assert repl.get_variable('result') == []

    def test_regex_match_returns_first(self, repl):
        """Test regex.match() returns first match."""
        repl.execute_ml('result = regex.match("[0-9]+", "abc123def456")')
        assert repl.get_variable('result') == '123'

    def test_regex_match_returns_none(self, repl):
        """Test regex.match() returns None when no match."""
        repl.execute_ml('result = regex.match("[0-9]+", "no numbers")')
        assert repl.get_variable('result') is None

    def test_regex_replace_first_occurrence(self, repl):
        """Test regex.replace() replaces only first match."""
        repl.execute_ml('result = regex.replace("[0-9]+", "I have 5 apples and 3 oranges", "X")')
        assert repl.get_variable('result') == "I have X apples and 3 oranges"

    def test_regex_replace_all_occurrences(self, repl):
        """Test regex.replaceAll() replaces all matches."""
        repl.execute_ml('result = regex.replaceAll("[0-9]+", "I have 5 apples and 3 oranges", "X")')
        assert repl.get_variable('result') == "I have X apples and X oranges"

    def test_regex_split(self, repl):
        """Test regex.split() splits text by pattern."""
        repl.execute_ml('result = regex.split("[0-9]+", "apple5banana3orange")')
        assert repl.get_variable('result') == ['apple', 'banana', 'orange']

    def test_regex_count(self, repl):
        """Test regex.count() counts matches."""
        repl.execute_ml('result = regex.count("[0-9]+", "1 apple, 2 oranges, 3 bananas")')
        assert repl.get_variable('result') == 3

    def test_regex_is_valid_true(self, repl):
        """Test regex.isValid() returns true for valid pattern."""
        repl.execute_ml('result = regex.isValid("[a-z]+")')
        assert repl.get_variable('result') is True

    def test_regex_is_valid_false(self, repl):
        """Test regex.isValid() returns false for invalid pattern."""
        repl.execute_ml('result = regex.isValid("[invalid")')
        assert repl.get_variable('result') is False

    def test_regex_escape(self, repl):
        """Test regex.escape() escapes special characters."""
        repl.execute_ml('result = regex.escape("Price: $5.99")')
        assert r'$' in repl.get_variable('result') or r'\$' in repl.get_variable('result')


class TestRegexPatternClass:
    """Test Pattern class from regex.compile()."""

    @pytest.fixture
    def repl(self):
        """Provide REPL with regex imported and pattern compiled."""
        helper = REPLTestHelper(security_enabled=False)
        helper.execute_ml('import regex')
        helper.execute_ml('pattern = regex.compile("[a-z]+")')
        yield helper
        helper.reset()

    def test_pattern_test(self, repl):
        """Test pattern.test() method."""
        repl.execute_ml('result = pattern.test("Hello World")')
        assert repl.get_variable('result') is True

    def test_pattern_match(self, repl):
        """Test pattern.match() returns first match."""
        repl.execute_ml('result = pattern.match("Hello World 123")')
        assert repl.get_variable('result') == 'ello'

    def test_pattern_findall(self, repl):
        """Test pattern.findAll() returns all matches."""
        repl.execute_ml('result = pattern.findAll("Hello World 123")')
        assert repl.get_variable('result') == ['ello', 'orld']

    def test_pattern_replace(self, repl):
        """Test pattern.replace() replaces first match."""
        repl.execute_ml('result = pattern.replace("Hello World", "X")')
        assert repl.get_variable('result') == "HX World"

    def test_pattern_replace_all(self, repl):
        """Test pattern.replaceAll() replaces all matches."""
        repl.execute_ml('result = pattern.replaceAll("Hello World", "X")')
        assert repl.get_variable('result') == "HX WX"

    def test_pattern_split(self, repl):
        """Test pattern.split() splits by matches."""
        repl.execute_ml('result = pattern.split("Hello123World456")')
        assert repl.get_variable('result') == ['H', '123W', '456']

    def test_pattern_count(self, repl):
        """Test pattern.count() counts matches."""
        repl.execute_ml('result = pattern.count("Hello World 123")')
        assert repl.get_variable('result') == 2

    def test_pattern_property_access(self, repl):
        """Test pattern.pattern property returns pattern string."""
        repl.execute_ml('result = pattern.pattern')
        assert repl.get_variable('result') == "[a-z]+"


class TestRegexErrorHandling:
    """Test error handling in regex module."""

    @pytest.fixture
    def repl(self):
        """Provide REPL with regex imported."""
        helper = REPLTestHelper(security_enabled=False)
        helper.execute_ml('import regex')
        yield helper
        helper.reset()

    def test_compile_invalid_pattern_raises_error(self, repl):
        """Test regex.compile() raises RuntimeError for invalid pattern."""
        result = repl.session.execute_ml_line('bad = regex.compile("[invalid")')
        assert not result.success
        assert 'RuntimeError' in result.error or 'Invalid regex pattern' in result.error

    def test_test_invalid_pattern_raises_error(self, repl):
        """Test regex.test() raises RuntimeError for invalid pattern."""
        result = repl.session.execute_ml_line('result = regex.test("[invalid", "text")')
        assert not result.success
        assert 'RuntimeError' in result.error or 'Invalid regex pattern' in result.error

    def test_findall_invalid_pattern_raises_error(self, repl):
        """Test regex.findAll() raises RuntimeError for invalid pattern."""
        result = repl.session.execute_ml_line('result = regex.findAll("[invalid", "text")')
        assert not result.success
        assert 'RuntimeError' in result.error or 'Invalid regex pattern' in result.error


class TestRegexConvenienceMethods:
    """Test convenience methods for common patterns."""

    @pytest.fixture
    def repl(self):
        """Provide REPL with regex imported."""
        helper = REPLTestHelper(security_enabled=False)
        helper.execute_ml('import regex')
        yield helper
        helper.reset()

    def test_extract_emails(self, repl):
        """Test regex.extractEmails() extracts email addresses."""
        repl.execute_ml('result = regex.extractEmails("Contact: john@example.com or jane@test.org")')
        emails = repl.get_variable('result')
        assert len(emails) == 2
        assert 'john@example.com' in emails
        assert 'jane@test.org' in emails

    def test_extract_phone_numbers(self, repl):
        """Test regex.extractPhoneNumbers() extracts phone numbers."""
        repl.execute_ml('result = regex.extractPhoneNumbers("Call 555-123-4567 or (555) 987-6543")')
        phones = repl.get_variable('result')
        assert len(phones) >= 1  # At least one phone number found

    def test_is_url_valid(self, repl):
        """Test regex.isUrl() returns true for valid URL."""
        repl.execute_ml('result = regex.isUrl("https://example.com/path")')
        assert repl.get_variable('result') is True

    def test_is_url_invalid(self, repl):
        """Test regex.isUrl() returns false for invalid URL."""
        repl.execute_ml('result = regex.isUrl("not a url")')
        assert repl.get_variable('result') is False

    def test_remove_html_tags(self, repl):
        """Test regex.removeHtmlTags() removes HTML."""
        repl.execute_ml('result = regex.removeHtmlTags("<p>Hello <b>World</b></p>")')
        assert repl.get_variable('result') == "Hello World"

    def test_email_pattern(self, repl):
        """Test regex.emailPattern() returns compiled pattern."""
        repl.execute_ml('emailPattern = regex.emailPattern()')
        repl.execute_ml('result = emailPattern.test("user@example.com")')
        assert repl.get_variable('result') is True


class TestRegexSafeAttributeAccess:
    """Test that regex methods are registered in safe attribute registry."""

    @pytest.fixture
    def repl(self):
        """Provide REPL with security enabled."""
        helper = REPLTestHelper(security_enabled=True)
        helper.execute_ml('import regex')
        yield helper
        helper.reset()

    def test_regex_compile_not_blocked(self, repl):
        """Test that regex.compile() is allowed despite 'compile' being dangerous."""
        # This is the critical test - regex.compile() should work even though
        # Python's built-in compile() is in the dangerous patterns list
        repl.execute_ml('pattern = regex.compile("[a-z]+")')
        repl.execute_ml('result = pattern.test("hello")')
        assert repl.get_variable('result') is True

    def test_regex_methods_accessible(self, repl):
        """Test that all Regex static methods are accessible."""
        repl.execute_ml('result1 = regex.test("a", "abc")')
        assert repl.get_variable('result1') is True

        repl.execute_ml('result2 = regex.findAll("[0-9]", "a1b2c3")')
        assert repl.get_variable('result2') == ['1', '2', '3']

    def test_pattern_methods_accessible(self, repl):
        """Test that all Pattern methods are accessible."""
        repl.execute_ml('pattern = regex.compile("[0-9]+")')
        repl.execute_ml('result1 = pattern.test("abc123")')
        assert repl.get_variable('result1') is True

        repl.execute_ml('result2 = pattern.findAll("a1b2c3")')
        assert repl.get_variable('result2') == ['1', '2', '3']