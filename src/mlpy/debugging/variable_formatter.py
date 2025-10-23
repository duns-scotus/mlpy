"""Enhanced variable formatting for ML debugger.

This module provides pretty-printing and intelligent formatting of ML values
in the debugger, making variables easier to read and understand.
"""

from typing import Any


class VariableFormatter:
    """Format variables for display in the debugger.

    Features:
    - Pretty-print objects (dictionaries) with indentation
    - Format arrays with intelligent truncation
    - Truncate long strings and nested structures
    - Type-aware formatting (shows types for clarity)
    - Configurable max depth and width
    """

    def __init__(
        self,
        max_depth: int = 3,
        max_array_items: int = 10,
        max_string_length: int = 100,
        max_dict_items: int = 10,
        indent: str = "  "
    ):
        """Initialize formatter with display limits.

        Args:
            max_depth: Maximum nesting depth to display
            max_array_items: Maximum array elements to show
            max_string_length: Maximum string length before truncation
            max_dict_items: Maximum dictionary entries to show
            indent: Indentation string for nested structures
        """
        self.max_depth = max_depth
        self.max_array_items = max_array_items
        self.max_string_length = max_string_length
        self.max_dict_items = max_dict_items
        self.indent = indent

    def format_value(self, value: Any, depth: int = 0) -> str:
        """Format a value for display.

        Args:
            value: The value to format
            depth: Current nesting depth (for recursion)

        Returns:
            Formatted string representation
        """
        # Check depth limit
        if depth >= self.max_depth:
            return self._format_truncated(value)

        # Format based on type
        if value is None:
            return "null"
        elif isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, int):
            return str(value)
        elif isinstance(value, float):
            return self._format_float(value)
        elif isinstance(value, str):
            return self._format_string(value)
        elif isinstance(value, list):
            return self._format_array(value, depth)
        elif isinstance(value, dict):
            return self._format_object(value, depth)
        elif callable(value):
            return self._format_function(value)
        else:
            # Unknown type - use repr
            return repr(value)

    def _format_float(self, value: float) -> str:
        """Format float with appropriate precision."""
        # Use shorter representation for common values
        if value == int(value):
            return f"{int(value)}.0"
        else:
            # Use up to 6 decimal places, strip trailing zeros
            formatted = f"{value:.6f}".rstrip('0').rstrip('.')
            return formatted

    def _format_string(self, value: str) -> str:
        """Format string with truncation and escaping."""
        # Escape special characters
        escaped = repr(value)

        # Truncate if too long
        if len(escaped) > self.max_string_length:
            # Show first part + "..." + last part
            half = (self.max_string_length - 5) // 2
            return f"{escaped[:half]}...{escaped[-half:]}"

        return escaped

    def _format_array(self, value: list, depth: int) -> str:
        """Format array with intelligent truncation."""
        if len(value) == 0:
            return "[]"

        # Small arrays on one line
        if len(value) <= 3 and depth < self.max_depth - 1:
            items = [self.format_value(item, depth + 1) for item in value[:3]]
            inline = "[" + ", ".join(items) + "]"
            if len(inline) < 60:
                return inline

        # Larger arrays - show first N items
        lines = ["["]
        shown_items = min(len(value), self.max_array_items)

        for i in range(shown_items):
            item_str = self.format_value(value[i], depth + 1)
            lines.append(f"{self.indent}{item_str},")

        # Show truncation indicator if needed
        if len(value) > self.max_array_items:
            remaining = len(value) - self.max_array_items
            lines.append(f"{self.indent}... {remaining} more items")

        lines.append("]")
        return "\n".join(lines)

    def _format_object(self, value: dict, depth: int) -> str:
        """Format object/dictionary with pretty printing."""
        if len(value) == 0:
            return "{}"

        # Small objects on one line
        if len(value) <= 2 and depth < self.max_depth - 1:
            items = []
            for k, v in list(value.items())[:2]:
                v_str = self.format_value(v, depth + 1)
                items.append(f"{k}: {v_str}")
            inline = "{" + ", ".join(items) + "}"
            if len(inline) < 60:
                return inline

        # Larger objects - pretty print
        lines = ["{"]
        shown_items = min(len(value), self.max_dict_items)

        for i, (k, v) in enumerate(list(value.items())[:shown_items]):
            v_str = self.format_value(v, depth + 1)
            # Handle multi-line values
            if "\n" in v_str:
                lines.append(f"{self.indent}{k}: {v_str},")
            else:
                lines.append(f"{self.indent}{k}: {v_str},")

        # Show truncation indicator if needed
        if len(value) > self.max_dict_items:
            remaining = len(value) - self.max_dict_items
            lines.append(f"{self.indent}... {remaining} more properties")

        lines.append("}")
        return "\n".join(lines)

    def _format_function(self, value: callable) -> str:
        """Format function with name and signature."""
        try:
            name = value.__name__
            return f"<function {name}>"
        except:
            return "<function>"

    def _format_truncated(self, value: Any) -> str:
        """Format value at max depth (truncated)."""
        if isinstance(value, list):
            return f"<array[{len(value)}]>"
        elif isinstance(value, dict):
            return f"<object with {len(value)} properties>"
        else:
            type_name = type(value).__name__
            return f"<{type_name}>"

    def format_type(self, value: Any) -> str:
        """Get ML type name for a value.

        Returns:
            ML type name: "number", "string", "boolean", "array", "object", "function", "null"
        """
        if value is None:
            return "null"
        elif isinstance(value, bool):
            return "boolean"
        elif isinstance(value, (int, float)):
            return "number"
        elif isinstance(value, str):
            return "string"
        elif isinstance(value, list):
            return "array"
        elif isinstance(value, dict):
            return "object"
        elif callable(value):
            return "function"
        else:
            return "unknown"


# Default formatter instance
_default_formatter = VariableFormatter()


def format_value(value: Any, max_depth: int = 3) -> str:
    """Format a value using the default formatter.

    This is a convenience function for quick formatting.

    Args:
        value: The value to format
        max_depth: Maximum nesting depth

    Returns:
        Formatted string
    """
    formatter = VariableFormatter(max_depth=max_depth)
    return formatter.format_value(value)


def format_variable_with_type(name: str, value: Any) -> str:
    """Format a variable with its name, type, and value.

    Args:
        name: Variable name
        value: Variable value

    Returns:
        Formatted string like "name: string = \"Alice\""
    """
    formatter = _default_formatter
    type_name = formatter.format_type(value)
    value_str = formatter.format_value(value)

    # Single line or multi-line
    if "\n" in value_str:
        return f"{name}: {type_name} =\n{value_str}"
    else:
        return f"{name}: {type_name} = {value_str}"
