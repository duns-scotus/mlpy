"""Python bridge implementations for ML regex module.

The regex module provides pattern matching and text manipulation capabilities.
When imported in ML code as 'import regex;', it creates a 'regex' object with
methods for pattern matching, text replacement, and pattern compilation.

Usage in ML:
    import regex;

    // Test pattern
    if (regex.test("hello", "hello world")) { ... }

    // Compile pattern for reuse
    pattern = regex.compile("\\d+");
    numbers = pattern.findAll("I have 5 apples and 3 oranges");
"""

import re as _re  # Use underscore to avoid naming collision with ML 'regex' object
from mlpy.stdlib.decorators import ml_module, ml_function, ml_class


@ml_class(description="Compiled regular expression pattern")
class Pattern:
    """Compiled regex pattern for efficient reuse.

    This class represents a compiled regular expression pattern that can be
    used multiple times without recompiling.
    """

    def __init__(self, pattern: str):
        """Create a compiled pattern.

        Args:
            pattern: Regular expression pattern string

        Raises:
            RuntimeError: If pattern is invalid
        """
        self.pattern = pattern
        try:
            self._compiled = _re.compile(pattern)
        except _re.error as e:
            raise RuntimeError(f"Invalid regex pattern '{pattern}': {e}")

    @ml_function(description="Test if pattern matches text")
    def test(self, text: str) -> bool:
        """Test if pattern matches text.

        Args:
            text: String to test against pattern

        Returns:
            True if pattern matches, False otherwise
        """
        return bool(self._compiled.search(text))

    @ml_function(description="Find first match of pattern")
    def match(self, text: str) -> str | None:
        """Find first match of pattern in text.

        Args:
            text: String to search

        Returns:
            First match as string, or None if no match
        """
        match = self._compiled.search(text)
        return match.group(0) if match else None

    @ml_function(description="Find all matches of pattern")
    def findAll(self, text: str) -> list[str]:
        """Find all matches of pattern in text.

        Args:
            text: String to search

        Returns:
            List of all matches (empty list if no matches)
        """
        return self._compiled.findall(text)

    @ml_function(description="Replace first occurrence of pattern")
    def replace(self, text: str, replacement: str) -> str:
        """Replace first occurrence of pattern in text.

        Args:
            text: String to search and replace in
            replacement: Replacement string

        Returns:
            String with first match replaced
        """
        return self._compiled.sub(replacement, text, count=1)

    @ml_function(description="Replace all occurrences of pattern")
    def replaceAll(self, text: str, replacement: str) -> str:
        """Replace all occurrences of pattern in text.

        Args:
            text: String to search and replace in
            replacement: Replacement string

        Returns:
            String with all matches replaced
        """
        return self._compiled.sub(replacement, text)

    @ml_function(description="Split text using pattern as delimiter")
    def split(self, text: str) -> list[str]:
        """Split text using pattern as delimiter.

        Args:
            text: String to split

        Returns:
            List of split strings
        """
        return self._compiled.split(text)

    @ml_function(description="Count number of matches")
    def count(self, text: str) -> int:
        """Count number of matches in text.

        Args:
            text: String to search

        Returns:
            Number of matches found
        """
        return len(self._compiled.findall(text))

    @ml_function(description="Get string representation of pattern")
    def toString(self) -> str:
        """Get string representation of pattern.

        Returns:
            String representation
        """
        return f"Pattern({repr(self.pattern)})"

    # Snake_case aliases for convenience
    @ml_function(description="Find all matches (snake_case alias)")
    def find_all(self, text: str) -> list[str]:
        """Alias for findAll()."""
        return self.findAll(text)

    @ml_function(description="Replace all occurrences (snake_case alias)")
    def replace_all(self, text: str, replacement: str) -> str:
        """Alias for replaceAll()."""
        return self.replaceAll(text, replacement)

    @ml_function(description="Get string representation (snake_case alias)")
    def to_string(self) -> str:
        """Alias for toString()."""
        return self.toString()


@ml_module(
    name="regex",
    description="Regular expression pattern matching and text manipulation",
    capabilities=["regex.compile", "regex.match"],
    version="1.0.0"
)
class Regex:
    """Regex module interface for ML code.

    This class provides the main API for regular expression operations in ML.
    All methods are static and can be called directly on the regex object.
    """

    @ml_function(description="Compile regex pattern", capabilities=["regex.compile"])
    def compile(self, pattern: str) -> Pattern:
        """Compile a pattern for efficient reuse.

        Args:
            pattern: Regular expression pattern string

        Returns:
            Compiled Pattern object

        Raises:
            RuntimeError: If pattern is invalid

        Example:
            pattern = regex.compile("\\d+");
            numbers = pattern.findAll("I have 5 apples");
        """
        return Pattern(pattern)

    @ml_function(description="Test if pattern matches text", capabilities=["regex.match"])
    def test(self, pattern: str, text: str) -> bool:
        """Test if pattern matches text.

        Args:
            pattern: Regular expression pattern
            text: String to test

        Returns:
            True if pattern matches, False otherwise

        Raises:
            RuntimeError: If pattern is invalid
        """
        try:
            return bool(_re.search(pattern, text))
        except _re.error as e:
            raise RuntimeError(f"Invalid regex pattern '{pattern}': {e}")

    @ml_function(description="Find first match of pattern", capabilities=["regex.match"])
    def match(self, pattern: str, text: str) -> str | None:
        """Find first match of pattern in text.

        Args:
            pattern: Regular expression pattern
            text: String to search

        Returns:
            First match as string, or None if no match

        Raises:
            RuntimeError: If pattern is invalid
        """
        try:
            match = _re.search(pattern, text)
            return match.group(0) if match else None
        except _re.error as e:
            raise RuntimeError(f"Invalid regex pattern '{pattern}': {e}")

    @ml_function(description="Find all matches of pattern", capabilities=["regex.match"])
    def findAll(self, pattern: str, text: str) -> list[str]:
        """Find all matches of pattern in text.

        Args:
            pattern: Regular expression pattern
            text: String to search

        Returns:
            List of all matches (empty list if no matches)

        Raises:
            RuntimeError: If pattern is invalid
        """
        try:
            return _re.findall(pattern, text)
        except _re.error as e:
            raise RuntimeError(f"Invalid regex pattern '{pattern}': {e}")

    @ml_function(description="Replace first occurrence", capabilities=["regex.match"])
    def replace(self, pattern: str, text: str, replacement: str) -> str:
        """Replace first occurrence of pattern in text.

        Args:
            pattern: Regular expression pattern
            text: String to search and replace in
            replacement: Replacement string

        Returns:
            String with first match replaced

        Raises:
            RuntimeError: If pattern is invalid
        """
        try:
            return _re.sub(pattern, replacement, text, count=1)
        except _re.error as e:
            raise RuntimeError(f"Invalid regex pattern '{pattern}': {e}")

    @ml_function(description="Replace all occurrences", capabilities=["regex.match"])
    def replaceAll(self, pattern: str, text: str, replacement: str) -> str:
        """Replace all occurrences of pattern in text.

        Args:
            pattern: Regular expression pattern
            text: String to search and replace in
            replacement: Replacement string

        Returns:
            String with all matches replaced

        Raises:
            RuntimeError: If pattern is invalid
        """
        try:
            return _re.sub(pattern, replacement, text)
        except _re.error as e:
            raise RuntimeError(f"Invalid regex pattern '{pattern}': {e}")

    @ml_function(description="Split text by pattern", capabilities=["regex.match"])
    def split(self, pattern: str, text: str) -> list[str]:
        """Split text using pattern as delimiter.

        Args:
            pattern: Regular expression pattern
            text: String to split

        Returns:
            List of split strings

        Raises:
            RuntimeError: If pattern is invalid
        """
        try:
            return _re.split(pattern, text)
        except _re.error as e:
            raise RuntimeError(f"Invalid regex pattern '{pattern}': {e}")

    @ml_function(description="Escape special regex characters")
    def escape(self, text: str) -> str:
        """Escape special regex characters in text.

        Args:
            text: String to escape

        Returns:
            String with special characters escaped

        Example:
            escaped = regex.escape("Price: $5.99");
            // Returns: "Price: \\$5\\.99"
        """
        return _re.escape(text)

    @ml_function(description="Check if pattern is valid regex")
    def isValid(self, pattern: str) -> bool:
        """Check if pattern is a valid regex.

        Args:
            pattern: Regular expression pattern to validate

        Returns:
            True if pattern is valid, False otherwise
        """
        try:
            _re.compile(pattern)
            return True
        except _re.error:
            return False

    @ml_function(description="Count pattern matches", capabilities=["regex.match"])
    def count(self, pattern: str, text: str) -> int:
        """Count number of pattern matches in text.

        Args:
            pattern: Regular expression pattern
            text: String to search

        Returns:
            Number of matches found

        Raises:
            RuntimeError: If pattern is invalid
        """
        try:
            return len(_re.findall(pattern, text))
        except _re.error as e:
            raise RuntimeError(f"Invalid regex pattern '{pattern}': {e}")

    # Convenience methods for common patterns

    @ml_function(description="Get email validation pattern", capabilities=["regex.compile"])
    def emailPattern(self, ) -> Pattern:
        """Get a pre-compiled email validation pattern.

        Returns:
            Pattern object for matching email addresses
        """
        email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        return Pattern(email_regex)

    @ml_function(description="Extract email addresses from text", capabilities=["regex.match"])
    def extractEmails(self, text: str) -> list[str]:
        """Extract email addresses from text.

        Args:
            text: String to search for emails

        Returns:
            List of email addresses found
        """
        email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        return _re.findall(email_regex, text)

    @ml_function(description="Extract phone numbers from text", capabilities=["regex.match"])
    def extractPhoneNumbers(self, text: str) -> list[str]:
        """Extract phone numbers from text.

        Args:
            text: String to search for phone numbers

        Returns:
            List of phone numbers found
        """
        phone_regex = r"(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}"
        return _re.findall(phone_regex, text)

    @ml_function(description="Check if text is valid URL", capabilities=["regex.match"])
    def isUrl(self, text: str) -> bool:
        """Check if text is a valid URL.

        Args:
            text: String to validate as URL

        Returns:
            True if text is a valid URL, False otherwise
        """
        url_regex = (
            r"^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:\w*))?)?$"
        )
        return bool(_re.match(url_regex, text))

    @ml_function(description="Remove HTML tags from text", capabilities=["regex.match"])
    def removeHtmlTags(self, text: str) -> str:
        """Remove HTML tags from text.

        Args:
            text: String containing HTML

        Returns:
            String with all HTML tags removed
        """
        return _re.sub(r"<[^<]+?>", "", text)

    # Snake_case aliases for backward compatibility and convenience

    @ml_function(description="Get email pattern (snake_case alias)", capabilities=["regex.compile"])
    def email_pattern(self) -> Pattern:
        """Alias for emailPattern()."""
        return self.emailPattern()

    @ml_function(description="Extract emails (snake_case alias)", capabilities=["regex.match"])
    def extract_emails(self, text: str) -> list[str]:
        """Alias for extractEmails()."""
        return self.extractEmails(text)

    @ml_function(description="Extract phone numbers (snake_case alias)", capabilities=["regex.match"])
    def extract_phone_numbers(self, text: str) -> list[str]:
        """Alias for extractPhoneNumbers()."""
        return self.extractPhoneNumbers(text)

    @ml_function(description="Check URL (snake_case alias)", capabilities=["regex.match"])
    def is_url(self, text: str) -> bool:
        """Alias for isUrl()."""
        return self.isUrl(text)

    @ml_function(description="Remove HTML tags (snake_case alias)", capabilities=["regex.match"])
    def remove_html_tags(self, text: str) -> str:
        """Alias for removeHtmlTags()."""
        return self.removeHtmlTags(text)

    @ml_function(description="Replace all (snake_case alias)", capabilities=["regex.match"])
    def replace_all(self, pattern: str, text: str, replacement: str) -> str:
        """Alias for replaceAll()."""
        return self.replaceAll(pattern, text, replacement)

    @ml_function(description="Find first match (snake_case alias)", capabilities=["regex.match"])
    def find_first(self, pattern: str, text: str) -> str | None:
        """Alias for match() - finds first match."""
        return self.match(pattern, text)


# Create global regex instance for ML import
# When ML code does 'import regex;', this creates the 'regex' object
regex = Regex()

# Export public API
__all__ = [
    "Regex",
    "Pattern",
    "regex",
]
