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

    def test(self, text: str) -> bool:
        """Test if pattern matches text.

        Args:
            text: String to test against pattern

        Returns:
            True if pattern matches, False otherwise
        """
        return bool(self._compiled.search(text))

    def match(self, text: str) -> str | None:
        """Find first match of pattern in text.

        Args:
            text: String to search

        Returns:
            First match as string, or None if no match
        """
        match = self._compiled.search(text)
        return match.group(0) if match else None

    def findAll(self, text: str) -> list[str]:
        """Find all matches of pattern in text.

        Args:
            text: String to search

        Returns:
            List of all matches (empty list if no matches)
        """
        return self._compiled.findall(text)

    def replace(self, text: str, replacement: str) -> str:
        """Replace first occurrence of pattern in text.

        Args:
            text: String to search and replace in
            replacement: Replacement string

        Returns:
            String with first match replaced
        """
        return self._compiled.sub(replacement, text, count=1)

    def replaceAll(self, text: str, replacement: str) -> str:
        """Replace all occurrences of pattern in text.

        Args:
            text: String to search and replace in
            replacement: Replacement string

        Returns:
            String with all matches replaced
        """
        return self._compiled.sub(replacement, text)

    def split(self, text: str) -> list[str]:
        """Split text using pattern as delimiter.

        Args:
            text: String to split

        Returns:
            List of split strings
        """
        return self._compiled.split(text)

    def count(self, text: str) -> int:
        """Count number of matches in text.

        Args:
            text: String to search

        Returns:
            Number of matches found
        """
        return len(self._compiled.findall(text))

    def toString(self) -> str:
        """Get string representation of pattern.

        Returns:
            String representation
        """
        return f"Pattern({repr(self.pattern)})"

    # Snake_case aliases for convenience
    def find_all(self, text: str) -> list[str]:
        """Alias for findAll()."""
        return self.findAll(text)

    def replace_all(self, text: str, replacement: str) -> str:
        """Alias for replaceAll()."""
        return self.replaceAll(text, replacement)

    def to_string(self) -> str:
        """Alias for toString()."""
        return self.toString()


class Regex:
    """Regex module interface for ML code.

    This class provides the main API for regular expression operations in ML.
    All methods are static and can be called directly on the regex object.
    """

    @staticmethod
    def compile(pattern: str) -> Pattern:
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

    @staticmethod
    def test(pattern: str, text: str) -> bool:
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

    @staticmethod
    def match(pattern: str, text: str) -> str | None:
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

    @staticmethod
    def findAll(pattern: str, text: str) -> list[str]:
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

    @staticmethod
    def replace(pattern: str, text: str, replacement: str) -> str:
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

    @staticmethod
    def replaceAll(pattern: str, text: str, replacement: str) -> str:
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

    @staticmethod
    def split(pattern: str, text: str) -> list[str]:
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

    @staticmethod
    def escape(text: str) -> str:
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

    @staticmethod
    def isValid(pattern: str) -> bool:
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

    @staticmethod
    def count(pattern: str, text: str) -> int:
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

    @staticmethod
    def emailPattern() -> Pattern:
        """Get a pre-compiled email validation pattern.

        Returns:
            Pattern object for matching email addresses
        """
        email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        return Pattern(email_regex)

    @staticmethod
    def extractEmails(text: str) -> list[str]:
        """Extract email addresses from text.

        Args:
            text: String to search for emails

        Returns:
            List of email addresses found
        """
        email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        return _re.findall(email_regex, text)

    @staticmethod
    def extractPhoneNumbers(text: str) -> list[str]:
        """Extract phone numbers from text.

        Args:
            text: String to search for phone numbers

        Returns:
            List of phone numbers found
        """
        phone_regex = r"(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}"
        return _re.findall(phone_regex, text)

    @staticmethod
    def isUrl(text: str) -> bool:
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

    @staticmethod
    def removeHtmlTags(text: str) -> str:
        """Remove HTML tags from text.

        Args:
            text: String containing HTML

        Returns:
            String with all HTML tags removed
        """
        return _re.sub(r"<[^<]+?>", "", text)

    # Snake_case aliases for backward compatibility and convenience

    @staticmethod
    def email_pattern() -> Pattern:
        """Alias for emailPattern()."""
        return Regex.emailPattern()

    @staticmethod
    def extract_emails(text: str) -> list[str]:
        """Alias for extractEmails()."""
        return Regex.extractEmails(text)

    @staticmethod
    def extract_phone_numbers(text: str) -> list[str]:
        """Alias for extractPhoneNumbers()."""
        return Regex.extractPhoneNumbers(text)

    @staticmethod
    def is_url(text: str) -> bool:
        """Alias for isUrl()."""
        return Regex.isUrl(text)

    @staticmethod
    def remove_html_tags(text: str) -> str:
        """Alias for removeHtmlTags()."""
        return Regex.removeHtmlTags(text)

    @staticmethod
    def replace_all(pattern: str, text: str, replacement: str) -> str:
        """Alias for replaceAll()."""
        return Regex.replaceAll(pattern, text, replacement)

    @staticmethod
    def find_first(pattern: str, text: str) -> str | None:
        """Alias for match() - finds first match."""
        return Regex.match(pattern, text)


# Create global regex instance for ML import
# When ML code does 'import regex;', this creates the 'regex' object
regex = Regex()

# Export public API
__all__ = [
    "Regex",
    "Pattern",
    "regex",
]
