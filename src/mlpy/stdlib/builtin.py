"""Python bridge implementation for ML builtin module.

The builtin module provides core functions that are always available in ML code
without requiring explicit import. These functions cover:
- Type conversion (int, float, str, bool)
- Type checking (typeof, isinstance)
- Collections (len, range)
- I/O (print, input)
- Introspection (help, methods, modules)
- Math utilities (abs, min, max, round)

These functions are auto-imported by the code generator and available globally.
"""

from typing import Any, Callable
from mlpy.stdlib.decorators import ml_module, ml_function, _MODULE_REGISTRY


@ml_module(
    name="builtin",
    description="Core builtin functions always available without import",
    capabilities=[],  # Builtin functions don't require capabilities
    version="1.0.0"
)
class Builtin:
    """Builtin module providing core ML functions.

    This module is auto-imported and provides essential functionality
    that should be available in all ML programs.
    """

    # =====================================================================
    # Type Conversion Functions
    # =====================================================================

    @ml_function(description="Convert value to integer", capabilities=[])
    def int(self, value: Any) -> int:
        """Convert value to integer with ML-compatible semantics.

        Args:
            value: Value to convert (bool, str, float, int)

        Returns:
            Integer representation of value, or 0 on error

        Examples:
            int(3.14) => 3
            int("42") => 42
            int(true) => 1
            int(false) => 0
        """
        try:
            # Handle boolean explicitly (before int check)
            if isinstance(value, bool):
                return 1 if value else 0

            # Handle numeric types
            if isinstance(value, (int, float)):
                return int(value)

            # Handle strings
            if isinstance(value, str):
                # Try float first (handles "3.14" -> 3)
                try:
                    return int(float(value))
                except ValueError:
                    return int(value)

            # Default conversion attempt
            return int(value)
        except (ValueError, TypeError):
            return 0

    @ml_function(description="Convert value to float", capabilities=[])
    def float(self, value: Any) -> float:
        """Convert value to float with ML-compatible semantics.

        Args:
            value: Value to convert (bool, str, int, float)

        Returns:
            Float representation of value, or 0.0 on error

        Examples:
            float(42) => 42.0
            float("3.14") => 3.14
            float(true) => 1.0
            float(false) => 0.0
        """
        try:
            # Handle boolean explicitly (before float check)
            if isinstance(value, bool):
                return 1.0 if value else 0.0

            # Handle numeric types
            if isinstance(value, (int, float)):
                return float(value)

            # Handle strings
            if isinstance(value, str):
                return float(value)

            # Default conversion attempt
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    @ml_function(description="Convert value to string", capabilities=[])
    def str(self, value: Any) -> str:
        """Convert value to string with ML-compatible boolean formatting.

        Args:
            value: Value to convert

        Returns:
            String representation of value

        Examples:
            str(42) => "42"
            str(3.14) => "3.14"
            str(true) => "true"  (NOT "True")
            str(false) => "false"  (NOT "False")
        """
        # ML uses lowercase true/false
        if isinstance(value, bool):
            return "true" if value else "false"

        return str(value)

    @ml_function(description="Convert value to boolean", capabilities=[])
    def bool(self, value: Any) -> bool:
        """Convert value to boolean with ML-compatible semantics.

        Args:
            value: Value to convert

        Returns:
            Boolean representation of value

        Examples:
            bool(1) => true
            bool(0) => false
            bool("") => false
            bool("hello") => true
        """
        return bool(value)

    # =====================================================================
    # Type Checking Functions
    # =====================================================================

    @ml_function(description="Get type of value with class metadata awareness", capabilities=[])
    def typeof(self, value: Any) -> str:
        """Get type of value with @ml_class metadata integration.

        This function recognizes decorated classes from Phase 1-3 and returns
        their ML class names instead of generic "object".

        Args:
            value: Value to check type of

        Returns:
            Type name: "boolean", "number", "string", "array", "object",
                      "function", or custom class name (e.g., "Pattern", "DateTimeObject")

        Examples:
            typeof(true) => "boolean"
            typeof(42) => "number"
            typeof("hello") => "string"
            typeof([1,2,3]) => "array"
            typeof({a: 1}) => "object"
            typeof(pattern) => "Pattern"  (if Pattern is @ml_class decorated)
        """
        # Check for @ml_class metadata (from Phase 1-3)
        if hasattr(type(value), '_ml_class_metadata'):
            return type(value)._ml_class_metadata.name

        # Standard type detection
        if isinstance(value, bool):
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

    @ml_function(description="Check if value is instance of type", capabilities=[])
    def isinstance(self, value: Any, type_name: str) -> bool:
        """Check if value is instance of given type name.

        Supports both primitive types and custom @ml_class decorated classes.

        Args:
            value: Value to check
            type_name: Type name to check against

        Returns:
            True if value is of given type

        Examples:
            isinstance(42, "number") => true
            isinstance("hello", "string") => true
            isinstance(pattern, "Pattern") => true
        """
        actual_type = self.typeof(value)
        return actual_type == type_name

    # =====================================================================
    # Collection Functions
    # =====================================================================

    @ml_function(description="Get length of collection", capabilities=[])
    def len(self, collection: Any) -> int:
        """Get length of string, array, or object.

        Args:
            collection: String, array, or object to measure

        Returns:
            Length/size of collection, or 0 if not a collection

        Examples:
            len("hello") => 5
            len([1,2,3]) => 3
            len({a:1, b:2}) => 2
        """
        try:
            return len(collection)
        except TypeError:
            return 0

    @ml_function(description="Generate range of numbers", capabilities=[])
    def range(self, *args) -> list:
        """Generate range of numbers.

        Args:
            start: Start value (or stop if only one arg)
            stop: Stop value (exclusive)
            step: Step size (default 1)

        Returns:
            List of numbers in range

        Examples:
            range(5) => [0, 1, 2, 3, 4]
            range(1, 5) => [1, 2, 3, 4]
            range(0, 10, 2) => [0, 2, 4, 6, 8]
        """
        return list(range(*args))

    @ml_function(description="Enumerate array with indices", capabilities=[])
    def enumerate(self, array: list, start: int = 0) -> list:
        """Enumerate array returning (index, value) pairs.

        Args:
            array: Array to enumerate
            start: Starting index (default 0)

        Returns:
            List of (index, value) tuples

        Examples:
            enumerate(['a', 'b', 'c']) => [(0, 'a'), (1, 'b'), (2, 'c')]
        """
        return list(enumerate(array, start))

    # =====================================================================
    # I/O Functions
    # =====================================================================

    @ml_function(description="Print value to console", capabilities=[])
    def print(self, *values: Any) -> None:
        """Print values to console.

        Args:
            *values: Values to print

        Examples:
            print("Hello", "World") => prints "Hello World"
        """
        # Use ML-compatible boolean formatting
        formatted = []
        for val in values:
            if isinstance(val, bool):
                formatted.append("true" if val else "false")
            else:
                formatted.append(str(val))

        print(*formatted)

    @ml_function(description="Read input from console", capabilities=[])
    def input(self, prompt: str = "") -> str:
        """Read string input from console.

        Args:
            prompt: Prompt to display

        Returns:
            User input as string

        Examples:
            name = input("Enter name: ")
        """
        return input(prompt)

    # =====================================================================
    # Introspection Functions
    # =====================================================================

    @ml_function(description="Get help for function or module", capabilities=[])
    def help(self, target: Any) -> str:
        """Show documentation for function, method, or module.

        Args:
            target: Function, method, or module to get help for

        Returns:
            Documentation string

        Examples:
            help(string.upper) => "Convert string to uppercase"
            help(console) => "Console output and logging module"
        """
        # Check for @ml_function metadata
        if hasattr(target, '_ml_function_metadata'):
            metadata = target._ml_function_metadata
            return metadata.description if metadata.description else 'No description available'

        # Check for @ml_module metadata
        if hasattr(target, '_ml_module_metadata'):
            metadata = target._ml_module_metadata
            return metadata.description if metadata.description else 'No description available'

        # Check for @ml_class metadata
        if hasattr(type(target), '_ml_class_metadata'):
            metadata = type(target)._ml_class_metadata
            return metadata.description if metadata.description else 'No description available'

        # Fallback to docstring
        if hasattr(target, '__doc__') and target.__doc__:
            return target.__doc__.strip()

        return f"No help available for {target}"

    @ml_function(description="List all methods available on value", capabilities=[])
    def methods(self, value: Any) -> list:
        """List all available methods for a value type.

        Args:
            value: Value to get methods for

        Returns:
            List of method names

        Examples:
            methods("hello") => ["upper", "lower", "split", ...]
            methods([1,2,3]) => ["map", "filter", "push", ...]
        """
        # This would integrate with SafeAttributeRegistry
        # For now, return basic implementation
        type_name = self.typeof(value)

        # Get all non-private attributes
        methods = [attr for attr in dir(value) if not attr.startswith('_')]
        return sorted(methods)

    @ml_function(description="List all imported modules", capabilities=[])
    def modules(self) -> list:
        """List all currently imported modules.

        Returns:
            List of module names

        Examples:
            modules() => ["console", "math", "regex", "datetime"]
        """
        return sorted(list(_MODULE_REGISTRY.keys()))

    # =====================================================================
    # Math Utility Functions
    # =====================================================================

    @ml_function(description="Get absolute value", capabilities=[])
    def abs(self, value: float) -> float:
        """Get absolute value of number.

        Args:
            value: Number to get absolute value of

        Returns:
            Absolute value

        Examples:
            abs(-5) => 5
            abs(3.14) => 3.14
        """
        return abs(value)

    @ml_function(description="Get minimum value", capabilities=[])
    def min(self, *values) -> Any:
        """Get minimum value from arguments.

        Args:
            *values: Values to compare (or single array)

        Returns:
            Minimum value

        Examples:
            min(1, 2, 3) => 1
            min([5, 2, 8]) => 2
        """
        # Handle single array argument
        if len(values) == 1 and isinstance(values[0], list):
            return min(values[0]) if values[0] else None
        return min(values) if values else None

    @ml_function(description="Get maximum value", capabilities=[])
    def max(self, *values) -> Any:
        """Get maximum value from arguments.

        Args:
            *values: Values to compare (or single array)

        Returns:
            Maximum value

        Examples:
            max(1, 2, 3) => 3
            max([5, 2, 8]) => 8
        """
        # Handle single array argument
        if len(values) == 1 and isinstance(values[0], list):
            return max(values[0]) if values[0] else None
        return max(values) if values else None

    @ml_function(description="Round number to precision", capabilities=[])
    def round(self, value: float, precision: int = 0) -> float:
        """Round number to given precision.

        Args:
            value: Number to round
            precision: Number of decimal places (default 0)

        Returns:
            Rounded number

        Examples:
            round(3.14159) => 3.0
            round(3.14159, 2) => 3.14
        """
        return round(value, precision)

    @ml_function(description="Zip multiple arrays", capabilities=[])
    def zip(self, *arrays) -> list:
        """Zip multiple arrays into tuples.

        Args:
            *arrays: Arrays to zip together

        Returns:
            List of tuples

        Examples:
            zip([1,2,3], ['a','b','c']) => [(1,'a'), (2,'b'), (3,'c')]
        """
        return list(zip(*arrays))

    @ml_function(description="Get sorted copy of array", capabilities=[])
    def sorted(self, array: list, reverse: bool = False) -> list:
        """Return sorted copy of array.

        Args:
            array: Array to sort
            reverse: Sort in descending order (default false)

        Returns:
            New sorted array

        Examples:
            sorted([3, 1, 2]) => [1, 2, 3]
            sorted([3, 1, 2], true) => [3, 2, 1]
        """
        return sorted(array, reverse=reverse)

    @ml_function(description="Get object keys", capabilities=[])
    def keys(self, obj: dict) -> list:
        """Get all keys from object.

        Args:
            obj: Object to get keys from

        Returns:
            List of keys

        Examples:
            keys({a: 1, b: 2}) => ["a", "b"]
        """
        return list(obj.keys())

    @ml_function(description="Get object values", capabilities=[])
    def values(self, obj: dict) -> list:
        """Get all values from object.

        Args:
            obj: Object to get values from

        Returns:
            List of values

        Examples:
            values({a: 1, b: 2}) => [1, 2]
        """
        return list(obj.values())


# Global builtin instance for ML import
# This is auto-imported by the code generator
builtin = Builtin()


# Helper functions for direct use (maintains backward compatibility)
def typeof_helper(value: Any) -> str:
    """Helper function for typeof()."""
    return builtin.typeof(value)


def len_helper(collection: Any) -> int:
    """Helper function for len()."""
    return builtin.len(collection)


def print_helper(*values: Any) -> None:
    """Helper function for print()."""
    return builtin.print(*values)


# Export public API
__all__ = [
    "Builtin",
    "builtin",
    "typeof_helper",
    "len_helper",
    "print_helper",
]
