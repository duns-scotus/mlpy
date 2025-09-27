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
]
