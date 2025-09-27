"""Python bridge implementations for ML json module."""

import json as python_json
from typing import Any


def json_dumps(obj: Any) -> str:
    """Serialize object to JSON string."""
    try:
        return python_json.dumps(obj)
    except (TypeError, ValueError) as e:
        raise ValueError(f"JSON serialization failed: {e}")


def json_dumps_pretty(obj: Any, indent: int = 4) -> str:
    """Serialize object to JSON string with pretty formatting."""
    try:
        return python_json.dumps(obj, indent=indent)
    except (TypeError, ValueError) as e:
        raise ValueError(f"JSON serialization failed: {e}")


def json_loads(json_string: str) -> Any:
    """Parse JSON string to object."""
    try:
        return python_json.loads(json_string)
    except (python_json.JSONDecodeError, TypeError) as e:
        raise ValueError(f"JSON parsing failed: {e}")


def json_safe_loads(json_string: str, max_depth: int = 100) -> Any:
    """Safe JSON parsing with depth validation."""
    if max_depth > 100:
        max_depth = 100

    try:
        # Parse and validate depth
        result = python_json.loads(json_string)
        _validate_depth(result, max_depth, 0)
        return result
    except (python_json.JSONDecodeError, TypeError) as e:
        raise ValueError(f"JSON parsing failed: {e}")


def _validate_depth(obj: Any, max_depth: int, current_depth: int) -> None:
    """Recursively validate JSON object depth."""
    if current_depth > max_depth:
        raise ValueError(f"JSON object depth exceeds maximum allowed ({max_depth})")

    if isinstance(obj, dict):
        for value in obj.values():
            _validate_depth(value, max_depth, current_depth + 1)
    elif isinstance(obj, list):
        for item in obj:
            _validate_depth(item, max_depth, current_depth + 1)


def json_is_valid(json_string: str) -> bool:
    """Check if a string is valid JSON."""
    try:
        python_json.loads(json_string)
        return True
    except (python_json.JSONDecodeError, TypeError):
        return False


def json_is_object(obj: Any) -> bool:
    """Check if object is a JSON object (dict)."""
    return isinstance(obj, dict)


def json_is_array(obj: Any) -> bool:
    """Check if object is a JSON array (list)."""
    return isinstance(obj, list)


def json_is_string(obj: Any) -> bool:
    """Check if object is a JSON string."""
    return isinstance(obj, str)


def json_is_number(obj: Any) -> bool:
    """Check if object is a JSON number."""
    return isinstance(obj, (int, float)) and not isinstance(obj, bool)


def json_is_boolean(obj: Any) -> bool:
    """Check if object is a JSON boolean."""
    return isinstance(obj, bool)


def json_is_null(obj: Any) -> bool:
    """Check if object is JSON null."""
    return obj is None


class JSON:
    """JSON module interface for ML compatibility."""

    @staticmethod
    def dumps(obj: Any) -> str:
        """Serialize object to JSON string."""
        return json_dumps(obj)

    @staticmethod
    def dumps_pretty(obj: Any, indent: int = 4) -> str:
        """Serialize object to JSON string with pretty formatting."""
        return json_dumps_pretty(obj, indent)

    @staticmethod
    def loads(json_string: str) -> Any:
        """Parse JSON string to object."""
        return json_loads(json_string)

    @staticmethod
    def safe_loads(json_string: str, max_depth: int = 100) -> Any:
        """Safe JSON parsing with depth validation."""
        return json_safe_loads(json_string, max_depth)

    @staticmethod
    def is_valid(json_string: str) -> bool:
        """Check if a string is valid JSON."""
        return json_is_valid(json_string)

    @staticmethod
    def is_object(obj: Any) -> bool:
        """Check if object is a JSON object."""
        return json_is_object(obj)

    @staticmethod
    def is_array(obj: Any) -> bool:
        """Check if object is a JSON array."""
        return json_is_array(obj)

    @staticmethod
    def is_string(obj: Any) -> bool:
        """Check if object is a JSON string."""
        return json_is_string(obj)

    @staticmethod
    def is_number(obj: Any) -> bool:
        """Check if object is a JSON number."""
        return json_is_number(obj)

    @staticmethod
    def is_boolean(obj: Any) -> bool:
        """Check if object is a JSON boolean."""
        return json_is_boolean(obj)

    @staticmethod
    def is_null(obj: Any) -> bool:
        """Check if object is JSON null."""
        return json_is_null(obj)


# Create global json instance for ML compatibility
json = JSON()

# Export all bridge functions and the json object
__all__ = [
    "json",
    "json_dumps",
    "json_dumps_pretty",
    "json_loads",
    "json_safe_loads",
    "json_is_valid",
    "json_is_object",
    "json_is_array",
    "json_is_string",
    "json_is_number",
    "json_is_boolean",
    "json_is_null",
]