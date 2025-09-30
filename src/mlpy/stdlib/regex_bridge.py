"""Python bridge implementations for ML regex module."""

import re
import weakref
from collections.abc import Callable

# Cache for compiled patterns (using WeakValueDictionary to avoid memory leaks)
_pattern_cache = weakref.WeakValueDictionary()


def regex_test(pattern: str, text: str) -> bool:
    """Test if pattern matches text."""
    try:
        return bool(re.search(pattern, text))
    except re.error:
        return False


def regex_match(pattern: str, text: str) -> str | None:
    """Find first match of pattern in text."""
    try:
        match = re.search(pattern, text)
        return match.group(0) if match else None
    except re.error:
        return None


def regex_find_all(pattern: str, text: str) -> list[str]:
    """Find all matches of pattern in text."""
    try:
        return re.findall(pattern, text)
    except re.error:
        return []


def regex_find_first(pattern: str, text: str) -> str:
    """Find first match of pattern in text, return empty string if not found."""
    result = regex_match(pattern, text)
    return result if result is not None else ""


def regex_replace(pattern: str, text: str, replacement: str) -> str:
    """Replace first occurrence of pattern in text."""
    try:
        return re.sub(pattern, replacement, text, count=1)
    except re.error:
        return text


def regex_replace_all(pattern: str, text: str, replacement: str) -> str:
    """Replace all occurrences of pattern in text."""
    try:
        return re.sub(pattern, replacement, text)
    except re.error:
        return text


def regex_replace_with_function(pattern: str, text: str, replacer_func: Callable) -> str:
    """Replace matches using a replacer function."""
    try:

        def replacement_wrapper(match):
            return replacer_func(match.group(0))

        return re.sub(pattern, replacement_wrapper, text)
    except (re.error, TypeError, AttributeError):
        return text


def regex_split(pattern: str, text: str) -> list[str]:
    """Split text using pattern as delimiter."""
    try:
        return re.split(pattern, text)
    except re.error:
        return [text]


def regex_split_with_limit(pattern: str, text: str, max_splits: int) -> list[str]:
    """Split text using pattern with maximum number of splits."""
    try:
        return re.split(pattern, text, maxsplit=max_splits)
    except re.error:
        return [text]


def regex_compile(pattern: str) -> str:
    """Compile pattern for reuse (returns pattern ID)."""
    try:
        compiled = re.compile(pattern)
        pattern_id = f"compiled_{id(compiled)}"
        _pattern_cache[pattern_id] = compiled
        return pattern_id
    except re.error:
        return ""


def regex_test_compiled(pattern_id: str, text: str) -> bool:
    """Test compiled pattern against text."""
    try:
        compiled = _pattern_cache.get(pattern_id)
        if compiled is None:
            return False
        return bool(compiled.search(text))
    except (KeyError, AttributeError):
        return False


def regex_match_compiled(pattern_id: str, text: str) -> str | None:
    """Match compiled pattern against text."""
    try:
        compiled = _pattern_cache.get(pattern_id)
        if compiled is None:
            return None
        match = compiled.search(text)
        return match.group(0) if match else None
    except (KeyError, AttributeError):
        return None


def regex_find_with_groups(pattern: str, text: str) -> list[list[str]]:
    """Find matches with capture groups."""
    try:
        matches = []
        for match in re.finditer(pattern, text):
            groups = [match.group(0)]  # Full match
            groups.extend(match.groups())  # Capture groups
            matches.append(groups)
        return matches
    except re.error:
        return []


def regex_find_all_with_groups(pattern: str, text: str) -> list[list[str]]:
    """Find all matches with capture groups."""
    return regex_find_with_groups(pattern, text)


def regex_find_with_positions(pattern: str, text: str) -> list[dict]:
    """Find matches with position information."""
    try:
        matches = []
        for match in re.finditer(pattern, text):
            match_info = {
                "text": match.group(0),
                "start": match.start(),
                "end": match.end(),
                "groups": list(match.groups()),
            }
            matches.append(match_info)
        return matches
    except re.error:
        return []


def regex_is_valid(pattern: str) -> bool:
    """Check if pattern is valid."""
    try:
        re.compile(pattern)
        return True
    except re.error:
        return False


def regex_escape(text: str) -> str:
    """Escape special regex characters in text."""
    return re.escape(text)


class RegexPattern:
    """Safe Pattern object for ML with accessible methods."""

    def __init__(self, pattern: str):
        """Initialize pattern object."""
        self.pattern = pattern
        self._compiled = None
        try:
            self._compiled = re.compile(pattern)
            self._valid = True
        except re.error:
            self._valid = False

    def test(self, text: str) -> bool:
        """Test if pattern matches text."""
        if not self._valid:
            return False
        return regex_test(self.pattern, text)

    def find_all(self, text: str) -> list[str]:
        """Find all matches in text."""
        if not self._valid:
            return []
        return regex_find_all(self.pattern, text)

    def find_first(self, text: str) -> str:
        """Find first match in text."""
        if not self._valid:
            return ""
        return regex_find_first(self.pattern, text)

    def toString(self) -> str:
        """Return string representation of pattern."""
        return f"RegexPattern({repr(self.pattern)})"

    def is_valid(self) -> bool:
        """Check if pattern is valid."""
        return self._valid


def regex_count_matches(pattern: str, text: str) -> int:
    """Count number of matches."""
    try:
        return len(re.findall(pattern, text))
    except re.error:
        return 0


# Security validation functions
def validate_regex_pattern(pattern: str) -> bool:
    """Validate regex pattern for security (prevent ReDoS attacks)."""
    # Basic validation to prevent some ReDoS patterns
    dangerous_patterns = [
        r"\([^)]*\+[^)]*\+[^)]*\)",  # Nested quantifiers
        r"\([^)]*\*[^)]*\*[^)]*\)",  # Nested quantifiers
        r"\(\?\#.*\)",  # Comment groups (can be exploited)
    ]

    for dangerous in dangerous_patterns:
        if re.search(dangerous, pattern):
            return False

    # Check for excessively complex patterns
    if len(pattern) > 1000:  # Arbitrary limit
        return False

    # Check for valid pattern compilation
    try:
        compiled = re.compile(pattern)
        # Test with a small string to catch some ReDoS patterns
        test_string = "a" * 100
        # Set a reasonable timeout equivalent (not directly possible with re module)
        # In a production system, you'd want to implement timeout handling
        compiled.search(test_string)
        return True
    except re.error:
        return False
    except Exception:
        # Catch any other exceptions that might indicate problematic patterns
        return False


# Helper function to safely execute regex operations
def safe_regex_operation(func: Callable, *args, **kwargs):
    """Safely execute regex operation with error handling."""
    try:
        return func(*args, **kwargs)
    except re.error:
        return None
    except Exception:
        return None


class Regex:
    """Regex module interface for ML compatibility."""

    @staticmethod
    def test(pattern: str, text: str) -> bool:
        """Test if pattern matches text."""
        return regex_test(pattern, text)

    @staticmethod
    def match(pattern: str, text: str) -> str | None:
        """Find first match of pattern in text."""
        return regex_match(pattern, text)

    @staticmethod
    def find_all(pattern: str, text: str) -> list[str]:
        """Find all matches of pattern in text."""
        return regex_find_all(pattern, text)

    @staticmethod
    def find_first(pattern: str, text: str) -> str:
        """Find first match of pattern in text."""
        return regex_find_first(pattern, text)

    @staticmethod
    def replace(pattern: str, text: str, replacement: str) -> str:
        """Replace first occurrence of pattern in text."""
        return regex_replace(pattern, text, replacement)

    @staticmethod
    def replace_all(pattern: str, text: str, replacement: str) -> str:
        """Replace all occurrences of pattern in text."""
        return regex_replace_all(pattern, text, replacement)

    @staticmethod
    def split(pattern: str, text: str) -> list[str]:
        """Split text using pattern as delimiter."""
        return regex_split(pattern, text)

    @staticmethod
    def is_valid(pattern: str) -> bool:
        """Check if pattern is valid."""
        return regex_is_valid(pattern)

    @staticmethod
    def escape(text: str) -> str:
        """Escape special regex characters in text."""
        return regex_escape(text)

    @staticmethod
    def count_matches(pattern: str, text: str) -> int:
        """Count number of matches."""
        return regex_count_matches(pattern, text)

    @staticmethod
    def email_pattern() -> RegexPattern:
        """Create an email pattern object."""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return RegexPattern(email_pattern)

    @staticmethod
    def extract_emails(text: str) -> list[str]:
        """Extract email addresses from text."""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return regex_find_all(email_pattern, text)

    @staticmethod
    def extract_phone_numbers(text: str) -> list[str]:
        """Extract phone numbers from text."""
        phone_pattern = r'(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}'
        return regex_find_all(phone_pattern, text)

    @staticmethod
    def is_url(text: str) -> bool:
        """Check if text is a valid URL."""
        url_pattern = r'^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:\w*))?)?$'
        return regex_test(url_pattern, text)

    @staticmethod
    def find_first(pattern: str, text: str) -> str:
        """Find first match (alias for regex_find_first)."""
        return regex_find_first(pattern, text)

    @staticmethod
    def remove_html_tags(text: str) -> str:
        """Remove HTML tags from text."""
        html_pattern = r'<[^<]+?>'
        return regex_replace_all(html_pattern, text, '')


# Create global regex instance for ML compatibility
regex = Regex()

# Export all bridge functions
__all__ = [
    "Regex",
    "RegexPattern",
    "regex",
    "regex_test",
    "regex_match",
    "regex_find_all",
    "regex_find_first",
    "regex_replace",
    "regex_replace_all",
    "regex_replace_with_function",
    "regex_split",
    "regex_split_with_limit",
    "regex_compile",
    "regex_test_compiled",
    "regex_match_compiled",
    "regex_find_with_groups",
    "regex_find_all_with_groups",
    "regex_find_with_positions",
    "regex_is_valid",
    "regex_escape",
    "regex_count_matches",
    "validate_regex_pattern",
    "safe_regex_operation",
]
