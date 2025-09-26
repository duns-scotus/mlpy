"""Python bridge implementations for ML string module."""

import re
from typing import Any, List


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


def str_format(template: str, args: List[Any]) -> str:
    """Format string with arguments."""
    try:
        return template.format(*args)
    except (IndexError, KeyError, ValueError):
        return template


def to_snake_case(text: str) -> str:
    """Convert to snake_case."""
    # Insert underscore before uppercase letters that follow lowercase letters
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    # Insert underscore before uppercase letters that follow lowercase or digits
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def to_camel_case(text: str) -> str:
    """Convert to camelCase."""
    components = text.replace('-', '_').split('_')
    return components[0].lower() + ''.join(word.capitalize() for word in components[1:])


def to_pascal_case(text: str) -> str:
    """Convert to PascalCase."""
    components = text.replace('-', '_').split('_')
    return ''.join(word.capitalize() for word in components)


def to_kebab_case(text: str) -> str:
    """Convert to kebab-case."""
    # Insert hyphen before uppercase letters that follow lowercase letters
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', text)
    # Insert hyphen before uppercase letters that follow lowercase or digits
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()


# Export all bridge functions
__all__ = [
    "reverse_string",
    "str_repeat",
    "str_char_at",
    "str_char_code_at",
    "str_format",
    "to_snake_case",
    "to_camel_case",
    "to_pascal_case",
    "to_kebab_case"
]