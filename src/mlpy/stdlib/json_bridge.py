"""Python bridge implementation for ML JSON module.

The json module provides JSON parsing, serialization, and validation capabilities.
When imported in ML code as 'import json;', it creates a 'json' object with
methods for working with JSON data.

Usage in ML:
    import json;

    // Parse JSON string
    data = json.parse('{"name": "Alice", "age": 30}');
    name = data.name;

    // Stringify object to JSON
    obj = {x: 10, y: 20};
    jsonStr = json.stringify(obj);

    // Pretty print with indentation
    pretty = json.prettyPrint(obj, 2);

    // Validate JSON string
    if (json.validate('{"valid": true}')) {
        // Valid JSON
    }

    // Type checking
    if (json.isObject(data)) {
        // It's an object
    }
"""

import json as _json  # Use underscore to avoid naming collision with ML 'json' object
from typing import Any
from mlpy.stdlib.decorators import ml_module, ml_function


def _validate_depth(obj: Any, max_depth: int, current_depth: int = 0) -> None:
    """Recursively validate JSON object depth for security.

    Args:
        obj: Object to validate
        max_depth: Maximum allowed depth
        current_depth: Current recursion depth

    Raises:
        ValueError: If depth exceeds maximum
    """
    if current_depth > max_depth:
        raise ValueError(f"JSON object depth exceeds maximum allowed ({max_depth})")

    if isinstance(obj, dict):
        for value in obj.values():
            _validate_depth(value, max_depth, current_depth + 1)
    elif isinstance(obj, list):
        for item in obj:
            _validate_depth(item, max_depth, current_depth + 1)


@ml_module(
    name="json",
    description="JSON parsing, serialization, and validation utilities",
    capabilities=["json.parse", "json.serialize"],
    version="1.0.0"
)
class JSON:
    """JSON module interface for ML code.

    This class provides comprehensive JSON functionality including:
    - Parsing JSON strings to objects
    - Serializing objects to JSON strings
    - Pretty printing with indentation
    - Safe parsing with depth validation
    - Type checking utilities
    - JSON validation
    """

    # =====================================================================
    # Parsing and Serialization
    # =====================================================================

    @ml_function(
        description="Parse JSON string to object",
        capabilities=["json.parse"]
    )
    def parse(self, json_string: str) -> Any:
        """Parse JSON string to ML object (dict/array/primitive).

        Args:
            json_string: Valid JSON string to parse

        Returns:
            Parsed object, array, or primitive value

        Raises:
            ValueError: If JSON string is invalid

        Examples:
            obj = json.parse('{"name": "Alice", "age": 30}')
            arr = json.parse('[1, 2, 3]')
            num = json.parse('42')
        """
        try:
            return _json.loads(json_string)
        except (_json.JSONDecodeError, TypeError) as e:
            raise ValueError(f"JSON parsing failed: {e}")

    @ml_function(
        description="Parse JSON string with depth validation for security",
        capabilities=["json.parse"]
    )
    def safeParse(self, json_string: str, max_depth: int = 100) -> Any:
        """Parse JSON string with depth validation to prevent deep nesting attacks.

        Args:
            json_string: Valid JSON string to parse
            max_depth: Maximum allowed nesting depth (default 100, max 100)

        Returns:
            Parsed object with validated depth

        Raises:
            ValueError: If JSON is invalid or depth exceeds maximum

        Security:
            Prevents deeply nested JSON attacks that can cause stack overflow

        Examples:
            obj = json.safeParse('{"a": {"b": {"c": 1}}}', 10)
        """
        # Enforce maximum depth limit for security
        if max_depth > 100:
            max_depth = 100

        try:
            result = _json.loads(json_string)
            _validate_depth(result, max_depth)
            return result
        except (_json.JSONDecodeError, TypeError) as e:
            raise ValueError(f"JSON parsing failed: {e}")

    @ml_function(
        description="Serialize object to JSON string",
        capabilities=["json.serialize"]
    )
    def stringify(self, obj: Any) -> str:
        """Serialize ML object to compact JSON string.

        Args:
            obj: Object, array, or primitive to serialize

        Returns:
            Compact JSON string representation

        Raises:
            ValueError: If object cannot be serialized to JSON

        Examples:
            json.stringify({name: "Alice", age: 30})  // '{"name":"Alice","age":30}'
            json.stringify([1, 2, 3])                 // '[1,2,3]'
        """
        try:
            return _json.dumps(obj)
        except (TypeError, ValueError) as e:
            raise ValueError(f"JSON serialization failed: {e}")

    @ml_function(
        description="Serialize object to pretty-printed JSON string",
        capabilities=["json.serialize"]
    )
    def prettyPrint(self, obj: Any, indent: int = 4) -> str:
        """Serialize ML object to pretty-printed JSON string with indentation.

        Args:
            obj: Object, array, or primitive to serialize
            indent: Number of spaces for indentation (default 4)

        Returns:
            Pretty-printed JSON string with indentation

        Raises:
            ValueError: If object cannot be serialized to JSON

        Examples:
            json.prettyPrint({name: "Alice", age: 30}, 2)
            // {
            //   "name": "Alice",
            //   "age": 30
            // }
        """
        try:
            return _json.dumps(obj, indent=indent)
        except (TypeError, ValueError) as e:
            raise ValueError(f"JSON serialization failed: {e}")

    # =====================================================================
    # Validation
    # =====================================================================

    @ml_function(
        description="Validate if string is valid JSON",
        capabilities=["json.parse"]
    )
    def validate(self, json_string: str) -> bool:
        """Check if a string is valid JSON without parsing.

        Args:
            json_string: String to validate

        Returns:
            True if valid JSON, False otherwise

        Examples:
            json.validate('{"valid": true}')  // true
            json.validate('{invalid}')        // false
        """
        try:
            _json.loads(json_string)
            return True
        except (_json.JSONDecodeError, TypeError):
            return False

    # =====================================================================
    # Type Checking Utilities
    # =====================================================================

    @ml_function(
        description="Check if value is a JSON object (dict)",
        capabilities=[]
    )
    def isObject(self, value: Any) -> bool:
        """Check if value is a JSON object (ML dict).

        Args:
            value: Value to check

        Returns:
            True if value is an object/dict, False otherwise

        Examples:
            json.isObject({a: 1})     // true
            json.isObject([1, 2, 3])  // false
        """
        return isinstance(value, dict)

    @ml_function(
        description="Check if value is a JSON array (list)",
        capabilities=[]
    )
    def isArray(self, value: Any) -> bool:
        """Check if value is a JSON array (ML array).

        Args:
            value: Value to check

        Returns:
            True if value is an array/list, False otherwise

        Examples:
            json.isArray([1, 2, 3])  // true
            json.isArray({a: 1})     // false
        """
        return isinstance(value, list)

    @ml_function(
        description="Check if value is a JSON string",
        capabilities=[]
    )
    def isString(self, value: Any) -> bool:
        """Check if value is a JSON string.

        Args:
            value: Value to check

        Returns:
            True if value is a string, False otherwise

        Examples:
            json.isString("hello")  // true
            json.isString(42)       // false
        """
        return isinstance(value, str)

    @ml_function(
        description="Check if value is a JSON number",
        capabilities=[]
    )
    def isNumber(self, value: Any) -> bool:
        """Check if value is a JSON number (int or float, excluding boolean).

        Args:
            value: Value to check

        Returns:
            True if value is a number (not boolean), False otherwise

        Examples:
            json.isNumber(42)      // true
            json.isNumber(3.14)    // true
            json.isNumber(true)    // false (boolean, not number)
        """
        return isinstance(value, (int, float)) and not isinstance(value, bool)

    @ml_function(
        description="Check if value is a JSON boolean",
        capabilities=[]
    )
    def isBoolean(self, value: Any) -> bool:
        """Check if value is a JSON boolean.

        Args:
            value: Value to check

        Returns:
            True if value is a boolean, False otherwise

        Examples:
            json.isBoolean(true)   // true
            json.isBoolean(false)  // true
            json.isBoolean(1)      // false
        """
        return isinstance(value, bool)

    @ml_function(
        description="Check if value is JSON null",
        capabilities=[]
    )
    def isNull(self, value: Any) -> bool:
        """Check if value is JSON null (None).

        Args:
            value: Value to check

        Returns:
            True if value is null/None, False otherwise

        Examples:
            json.isNull(null)  // true (if null is None)
            json.isNull(0)     // false
        """
        return value is None

    # =====================================================================
    # Utility Methods
    # =====================================================================

    @ml_function(
        description="Get all keys from JSON object",
        capabilities=[]
    )
    def keys(self, obj: dict) -> list:
        """Get all keys from JSON object as array.

        Args:
            obj: JSON object (dict)

        Returns:
            Array of all keys

        Examples:
            json.keys({name: "Alice", age: 30})  // ["name", "age"]
        """
        if not isinstance(obj, dict):
            return []
        return list(obj.keys())

    @ml_function(
        description="Get all values from JSON object",
        capabilities=[]
    )
    def values(self, obj: dict) -> list:
        """Get all values from JSON object as array.

        Args:
            obj: JSON object (dict)

        Returns:
            Array of all values

        Examples:
            json.values({name: "Alice", age: 30})  // ["Alice", 30]
        """
        if not isinstance(obj, dict):
            return []
        return list(obj.values())

    @ml_function(
        description="Check if JSON object has key",
        capabilities=[]
    )
    def hasKey(self, obj: dict, key: str) -> bool:
        """Check if JSON object has a specific key.

        Args:
            obj: JSON object (dict)
            key: Key to check for

        Returns:
            True if key exists, False otherwise

        Examples:
            json.hasKey({name: "Alice"}, "name")  // true
            json.hasKey({name: "Alice"}, "age")   // false
        """
        if not isinstance(obj, dict):
            return False
        return key in obj

    @ml_function(
        description="Get value from JSON object with default",
        capabilities=[]
    )
    def get(self, obj: dict, key: str, default: Any = None) -> Any:
        """Get value from JSON object with optional default.

        Args:
            obj: JSON object (dict)
            key: Key to get value for
            default: Default value if key not found (default None)

        Returns:
            Value at key, or default if key doesn't exist

        Examples:
            json.get({name: "Alice"}, "name", "Unknown")      // "Alice"
            json.get({name: "Alice"}, "age", 0)               // 0
        """
        if not isinstance(obj, dict):
            return default
        return obj.get(key, default)

    @ml_function(
        description="Merge two JSON objects",
        capabilities=[]
    )
    def merge(self, obj1: dict, obj2: dict) -> dict:
        """Merge two JSON objects (obj2 overwrites obj1 for duplicate keys).

        Args:
            obj1: First JSON object
            obj2: Second JSON object (takes precedence)

        Returns:
            New merged object

        Examples:
            a = {x: 1, y: 2};
            b = {y: 3, z: 4};
            json.merge(a, b)  // {x: 1, y: 3, z: 4}
        """
        if not isinstance(obj1, dict):
            obj1 = {}
        if not isinstance(obj2, dict):
            obj2 = {}

        result = obj1.copy()
        result.update(obj2)
        return result


# Global json instance for ML import
# This is imported by ML code as: import json;
json = JSON()


# Export public API
__all__ = [
    "JSON",
    "json",
]
