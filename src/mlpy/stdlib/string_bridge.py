"""Python bridge implementations for ML string module."""

import re
from typing import Any


def reverse_string(text: str) -> str:
    """Reverse a string."""
    return text[::-1]


def str_repeat(text: str, count: int) -> str:
    """Repeat a string count times."""
    return text * count


def str_char_at(text: str, index: int) -> str:
    """Get character at specific index."""
    if 0 <= index < len(text):
        return text[index]
    return ""


def str_char_code_at(text: str, index: int) -> int:
    """Get character code at specific index."""
    if 0 <= index < len(text):
        return ord(text[index])
    return 0


def str_format(template: str, args: list[Any]) -> str:
    """Format string with arguments."""
    try:
        return template.format(*args)
    except (IndexError, KeyError, ValueError):
        return template


def to_snake_case(text: str) -> str:
    """Convert to snake_case."""
    # Insert underscore before uppercase letters that follow lowercase letters
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", text)
    # Insert underscore before uppercase letters that follow lowercase or digits
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def to_camel_case(text: str) -> str:
    """Convert to camelCase."""
    components = text.replace("-", "_").split("_")
    return components[0].lower() + "".join(word.capitalize() for word in components[1:])


def to_pascal_case(text: str) -> str:
    """Convert to PascalCase."""
    components = text.replace("-", "_").split("_")
    return "".join(word.capitalize() for word in components)


def to_kebab_case(text: str) -> str:
    """Convert to kebab-case."""
    # Insert hyphen before uppercase letters that follow lowercase letters
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1-\2", text)
    # Insert hyphen before uppercase letters that follow lowercase or digits
    return re.sub("([a-z0-9])([A-Z])", r"\1-\2", s1).lower()


def to_chars(text: str) -> list[str]:
    """Convert string to array of characters."""
    return list(text)


# String trimming functions
def str_trim(text: str) -> str:
    """Remove whitespace from both ends of string."""
    return text.strip()


def str_lstrip(text: str) -> str:
    """Remove whitespace from left end of string."""
    return text.lstrip()


def str_rstrip(text: str) -> str:
    """Remove whitespace from right end of string."""
    return text.rstrip()


# String padding functions
def str_pad_left(text: str, width: int, fill_char: str = " ") -> str:
    """Pad string on the left to specified width."""
    if len(fill_char) == 0:
        fill_char = " "
    return text.rjust(width, fill_char[0])


def str_pad_right(text: str, width: int, fill_char: str = " ") -> str:
    """Pad string on the right to specified width."""
    if len(fill_char) == 0:
        fill_char = " "
    return text.ljust(width, fill_char[0])


def str_pad_center(text: str, width: int, fill_char: str = " ") -> str:
    """Pad string on both sides to center it within specified width."""
    if len(fill_char) == 0:
        fill_char = " "
    return text.center(width, fill_char[0])


# String validation functions
def str_is_empty(text: str) -> bool:
    """Check if string is empty."""
    return len(text) == 0


def str_is_whitespace(text: str) -> bool:
    """Check if string contains only whitespace characters."""
    return len(text) > 0 and text.isspace()


def str_is_alpha(text: str) -> bool:
    """Check if string contains only alphabetic characters."""
    return len(text) > 0 and text.isalpha()


def str_is_numeric(text: str) -> bool:
    """Check if string contains only numeric characters."""
    return len(text) > 0 and text.isdigit()


def str_is_alphanumeric(text: str) -> bool:
    """Check if string contains only alphanumeric characters."""
    return len(text) > 0 and text.isalnum()


# String search functions
def str_starts_with(text: str, prefix: str) -> bool:
    """Check if string starts with specified prefix."""
    return text.startswith(prefix)


def str_ends_with(text: str, suffix: str) -> bool:
    """Check if string ends with specified suffix."""
    return text.endswith(suffix)


def str_find(text: str, substring: str) -> int:
    """Find first occurrence of substring. Returns -1 if not found."""
    return text.find(substring)


def str_rfind(text: str, substring: str) -> int:
    """Find last occurrence of substring. Returns -1 if not found."""
    return text.rfind(substring)


def str_index_of(text: str, substring: str) -> int:
    """Find first occurrence of substring (alias for find)."""
    return text.find(substring)


def str_last_index_of(text: str, substring: str) -> int:
    """Find last occurrence of substring (alias for rfind)."""
    return text.rfind(substring)


def str_count(text: str, substring: str) -> int:
    """Count non-overlapping occurrences of substring."""
    return text.count(substring)


# String replacement functions
def str_replace(text: str, old: str, new: str) -> str:
    """Replace first occurrence of old with new."""
    return text.replace(old, new, 1)


def str_replace_all(text: str, old: str, new: str) -> str:
    """Replace all occurrences of old with new."""
    return text.replace(old, new)


# String splitting and joining functions
def str_split(text: str, delimiter: str) -> list[str]:
    """Split string by delimiter."""
    if delimiter == "":
        return list(text)
    return text.split(delimiter)


def str_join(delimiter: str, items: list[str]) -> str:
    """Join list of strings with delimiter."""
    return delimiter.join(str(item) for item in items)


# Type conversion functions
def str_to_int(text: str) -> int:
    """Convert string to integer. Returns 0 if conversion fails."""
    try:
        return int(text)
    except (ValueError, TypeError):
        return 0


def str_to_float(text: str) -> float:
    """Convert string to float. Returns 0.0 if conversion fails."""
    try:
        return float(text)
    except (ValueError, TypeError):
        return 0.0


def int_to_str(value: int) -> str:
    """Convert integer to string."""
    return str(value)


def float_to_str(value: float) -> str:
    """Convert float to string."""
    return str(value)


def bool_to_str(value: bool) -> str:
    """Convert boolean to string."""
    return "true" if value else "false"


# String substring functions
def str_substring(text: str, start: int, end: int = None) -> str:
    """Extract substring from start to end index."""
    if end is None:
        return text[start:]
    return text[start:end]


def str_slice(text: str, start: int, end: int = None) -> str:
    """Extract slice of string (alias for substring)."""
    if end is None:
        return text[start:]
    return text[start:end]


class String:
    """String module interface for ML compatibility."""

    @staticmethod
    def reverse(text: str) -> str:
        """Reverse a string."""
        return reverse_string(text)

    @staticmethod
    def repeat(text: str, count: int) -> str:
        """Repeat a string count times."""
        return str_repeat(text, count)

    @staticmethod
    def charAt(text: str, index: int) -> str:
        """Get character at specific index."""
        return str_char_at(text, index)

    @staticmethod
    def charCodeAt(text: str, index: int) -> int:
        """Get character code at specific index."""
        return str_char_code_at(text, index)

    @staticmethod
    def format(template: str, args: list[Any]) -> str:
        """Format string with arguments."""
        return str_format(template, args)

    @staticmethod
    def toSnakeCase(text: str) -> str:
        """Convert to snake_case."""
        return to_snake_case(text)

    @staticmethod
    def toCamelCase(text: str) -> str:
        """Convert to camelCase."""
        return to_camel_case(text)

    @staticmethod
    def toPascalCase(text: str) -> str:
        """Convert to PascalCase."""
        return to_pascal_case(text)

    @staticmethod
    def toKebabCase(text: str) -> str:
        """Convert to kebab-case."""
        return to_kebab_case(text)

    @staticmethod
    def upper(text: str) -> str:
        """Convert string to uppercase."""
        return text.upper()

    @staticmethod
    def lower(text: str) -> str:
        """Convert string to lowercase."""
        return text.lower()

    @staticmethod
    def capitalize(text: str) -> str:
        """Capitalize the first character of string."""
        return text.capitalize()

    @staticmethod
    def contains(text: str, substring: str) -> bool:
        """Check if string contains substring."""
        return substring in text

    @staticmethod
    def compare(str1: str, str2: str) -> int:
        """Compare two strings lexicographically.
        Returns: -1 if str1 < str2, 0 if str1 == str2, 1 if str1 > str2"""
        if str1 < str2:
            return -1
        elif str1 > str2:
            return 1
        else:
            return 0

    @staticmethod
    def length(text: str) -> int:
        """Get the length of a string."""
        return len(text)

    @staticmethod
    def toChars(text: str) -> list[str]:
        """Convert string to array of characters."""
        return to_chars(text)

    # Trimming methods
    @staticmethod
    def trim(text: str) -> str:
        """Remove whitespace from both ends."""
        return str_trim(text)

    @staticmethod
    def lstrip(text: str) -> str:
        """Remove whitespace from left end."""
        return str_lstrip(text)

    @staticmethod
    def rstrip(text: str) -> str:
        """Remove whitespace from right end."""
        return str_rstrip(text)

    # Padding methods
    @staticmethod
    def padLeft(text: str, width: int, fill_char: str = " ") -> str:
        """Pad string on the left."""
        return str_pad_left(text, width, fill_char)

    @staticmethod
    def padRight(text: str, width: int, fill_char: str = " ") -> str:
        """Pad string on the right."""
        return str_pad_right(text, width, fill_char)

    @staticmethod
    def padCenter(text: str, width: int, fill_char: str = " ") -> str:
        """Pad string on both sides to center it."""
        return str_pad_center(text, width, fill_char)

    # Validation methods
    @staticmethod
    def isEmpty(text: str) -> bool:
        """Check if string is empty."""
        return str_is_empty(text)

    @staticmethod
    def isWhitespace(text: str) -> bool:
        """Check if string contains only whitespace."""
        return str_is_whitespace(text)

    @staticmethod
    def isAlpha(text: str) -> bool:
        """Check if string contains only alphabetic characters."""
        return str_is_alpha(text)

    @staticmethod
    def isNumeric(text: str) -> bool:
        """Check if string contains only numeric characters."""
        return str_is_numeric(text)

    @staticmethod
    def isAlphanumeric(text: str) -> bool:
        """Check if string contains only alphanumeric characters."""
        return str_is_alphanumeric(text)

    # Search methods
    @staticmethod
    def startsWith(text: str, prefix: str) -> bool:
        """Check if string starts with prefix."""
        return str_starts_with(text, prefix)

    @staticmethod
    def endsWith(text: str, suffix: str) -> bool:
        """Check if string ends with suffix."""
        return str_ends_with(text, suffix)

    @staticmethod
    def find(text: str, substring: str) -> int:
        """Find first occurrence of substring."""
        return str_find(text, substring)

    @staticmethod
    def indexOf(text: str, substring: str) -> int:
        """Find first occurrence of substring (alias)."""
        return str_index_of(text, substring)

    @staticmethod
    def lastIndexOf(text: str, substring: str) -> int:
        """Find last occurrence of substring."""
        return str_last_index_of(text, substring)

    @staticmethod
    def count(text: str, substring: str) -> int:
        """Count occurrences of substring."""
        return str_count(text, substring)

    # Replacement methods
    @staticmethod
    def replace(text: str, old: str, new: str) -> str:
        """Replace first occurrence."""
        return str_replace(text, old, new)

    @staticmethod
    def replaceAll(text: str, old: str, new: str) -> str:
        """Replace all occurrences."""
        return str_replace_all(text, old, new)

    # Splitting and joining
    @staticmethod
    def split(text: str, delimiter: str) -> list[str]:
        """Split string by delimiter."""
        return str_split(text, delimiter)

    @staticmethod
    def join(delimiter: str, items: list[str]) -> str:
        """Join list with delimiter."""
        return str_join(delimiter, items)

    # Type conversion methods
    @staticmethod
    def toInt(text: str) -> int:
        """Convert string to integer."""
        return str_to_int(text)

    @staticmethod
    def toFloat(text: str) -> float:
        """Convert string to float."""
        return str_to_float(text)

    @staticmethod
    def toString(value: Any) -> str:
        """Convert value to string."""
        if isinstance(value, bool):
            return bool_to_str(value)
        elif isinstance(value, int):
            return int_to_str(value)
        elif isinstance(value, float):
            return float_to_str(value)
        else:
            return str(value)

    # Substring methods
    @staticmethod
    def substring(text: str, start: int, end: int = None) -> str:
        """Extract substring."""
        return str_substring(text, start, end)

    @staticmethod
    def slice(text: str, start: int, end: int = None) -> str:
        """Extract slice (alias for substring)."""
        return str_slice(text, start, end)

    # Snake_case aliases for ML compatibility
    @staticmethod
    def to_chars(text: str) -> list[str]:
        """Convert string to array of characters (snake_case alias)."""
        return to_chars(text)

    @staticmethod
    def char_at(text: str, index: int) -> str:
        """Get character at specific index (snake_case alias)."""
        return str_char_at(text, index)

    @staticmethod
    def char_code_at(text: str, index: int) -> int:
        """Get character code at specific index (snake_case alias)."""
        return str_char_code_at(text, index)

    @staticmethod
    def from_char_code(code: int) -> str:
        """Create character from character code."""
        try:
            return chr(code)
        except ValueError:
            return ""

    @staticmethod
    def to_string(value: Any) -> str:
        """Convert value to string (snake_case alias)."""
        return String.toString(value)

    @staticmethod
    def pad_left(text: str, width: int, fill_char: str = " ") -> str:
        """Pad string on the left (snake_case alias)."""
        return str_pad_left(text, width, fill_char)

    @staticmethod
    def pad_right(text: str, width: int, fill_char: str = " ") -> str:
        """Pad string on the right (snake_case alias)."""
        return str_pad_right(text, width, fill_char)

    @staticmethod
    def pad_center(text: str, width: int, fill_char: str = " ") -> str:
        """Pad string on both sides (snake_case alias)."""
        return str_pad_center(text, width, fill_char)

    @staticmethod
    def is_empty(text: str) -> bool:
        """Check if string is empty (snake_case alias)."""
        return str_is_empty(text)

    @staticmethod
    def is_whitespace(text: str) -> bool:
        """Check if string is whitespace (snake_case alias)."""
        return str_is_whitespace(text)

    @staticmethod
    def is_alpha(text: str) -> bool:
        """Check if string is alphabetic (snake_case alias)."""
        return str_is_alpha(text)

    @staticmethod
    def is_numeric(text: str) -> bool:
        """Check if string is numeric (snake_case alias)."""
        return str_is_numeric(text)

    @staticmethod
    def is_alphanumeric(text: str) -> bool:
        """Check if string is alphanumeric (snake_case alias)."""
        return str_is_alphanumeric(text)

    @staticmethod
    def starts_with(text: str, prefix: str) -> bool:
        """Check if string starts with prefix (snake_case alias)."""
        return str_starts_with(text, prefix)

    @staticmethod
    def ends_with(text: str, suffix: str) -> bool:
        """Check if string ends with suffix (snake_case alias)."""
        return str_ends_with(text, suffix)

    @staticmethod
    def index_of(text: str, substring: str) -> int:
        """Find first occurrence (snake_case alias)."""
        return str_index_of(text, substring)

    @staticmethod
    def last_index_of(text: str, substring: str) -> int:
        """Find last occurrence (snake_case alias)."""
        return str_last_index_of(text, substring)

    @staticmethod
    def replace_all(text: str, old: str, new: str) -> str:
        """Replace all occurrences (snake_case alias)."""
        return str_replace_all(text, old, new)

    @staticmethod
    def to_int(text: str) -> int:
        """Convert to integer (snake_case alias)."""
        return str_to_int(text)

    @staticmethod
    def to_float(text: str) -> float:
        """Convert to float (snake_case alias)."""
        return str_to_float(text)


# Create global string instance for ML compatibility
string = String()

# Export all bridge functions and the string object
__all__ = [
    "string",
    "reverse_string",
    "str_repeat",
    "str_char_at",
    "str_char_code_at",
    "str_format",
    "to_snake_case",
    "to_camel_case",
    "to_pascal_case",
    "to_kebab_case",
    "to_chars",
    "str_trim",
    "str_lstrip",
    "str_rstrip",
    "str_pad_left",
    "str_pad_right",
    "str_pad_center",
    "str_is_empty",
    "str_is_whitespace",
    "str_is_alpha",
    "str_is_numeric",
    "str_is_alphanumeric",
    "str_starts_with",
    "str_ends_with",
    "str_find",
    "str_rfind",
    "str_index_of",
    "str_last_index_of",
    "str_count",
    "str_replace",
    "str_replace_all",
    "str_split",
    "str_join",
    "str_to_int",
    "str_to_float",
    "int_to_str",
    "float_to_str",
    "bool_to_str",
    "str_substring",
    "str_slice",
]