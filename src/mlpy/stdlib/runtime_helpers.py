"""Runtime helpers for safe attribute access with type checking.

Provides runtime functions that enable secure Python-style attribute access
from transpiled ML code, with comprehensive type validation and security checks.
"""

from typing import Any

from ..ml.codegen.safe_attribute_registry import AttributeAccessType, get_safe_registry


class SecurityError(Exception):
    """Raised when a security violation is detected in attribute access."""

    pass


def safe_attr_access(obj: Any, attr_name: str, *args, **kwargs) -> Any:
    """
    Runtime helper for safe attribute access with type checking.

    Args:
        obj: The object to access attributes on
        attr_name: Name of the attribute to access
        *args: Arguments to pass if attribute is callable
        **kwargs: Keyword arguments to pass if attribute is callable

    Returns:
        The result of the attribute access or method call

    Raises:
        SecurityError: If access to dangerous attribute is attempted
        AttributeError: If attribute is not accessible on this type
    """
    registry = get_safe_registry()
    obj_type = type(obj)

    # Special case: ML objects (dicts with string keys) use dictionary access
    if is_ml_object(obj):
        # For ML objects, use dictionary access
        # Return None for missing keys (similar to JavaScript undefined)
        return obj.get(attr_name, None)

    # Check if access is safe for built-in types
    if not registry.is_safe_access(obj_type, attr_name):
        if attr_name.startswith("__") and attr_name.endswith("__"):
            raise SecurityError(f"Access to dangerous attribute '{attr_name}' is forbidden")
        else:
            raise AttributeError(
                f"'{obj_type.__name__}' object has no accessible attribute '{attr_name}'"
            )

    # Special handling for length property - map to len() function
    if attr_name == "length":
        return get_safe_length(obj)

    # Perform the actual access
    try:
        attr = getattr(obj, attr_name)
        if callable(attr):
            # If we have args/kwargs, call the method immediately
            if args or kwargs:
                return attr(*args, **kwargs)
            else:
                # Return a wrapper that will call the method when invoked
                return lambda *a, **kw: attr(*a, **kw)
        return attr
    except AttributeError:
        # This shouldn't happen if our whitelist is correct, but handle gracefully
        raise AttributeError(f"'{obj_type.__name__}' object has no attribute '{attr_name}'")


def safe_method_call(obj: Any, method_name: str, *args, **kwargs) -> Any:
    """
    Specialized helper for method calls.

    Args:
        obj: Object to call method on
        method_name: Name of the method to call
        *args: Method arguments
        **kwargs: Method keyword arguments

    Returns:
        Result of method call
    """
    registry = get_safe_registry()
    obj_type = type(obj)

    # Special case: ML objects (dicts) with function properties
    # For ML objects, obj.method(args) means: get obj['method'] and call it
    if is_ml_object(obj):
        # Access the property from the dict
        if method_name not in obj:
            raise AttributeError(
                f"ML object has no property '{method_name}'"
            )

        func = obj[method_name]

        # Check if it's callable
        if not callable(func):
            raise TypeError(
                f"Property '{method_name}' is not callable (got {type(func).__name__})"
            )

        # Call the function with the provided arguments
        return func(*args, **kwargs)

    # For Python objects, verify this is a safe method call
    attr_info = registry.get_attribute_info(obj_type, method_name)
    if not attr_info or attr_info.access_type != AttributeAccessType.METHOD:
        raise AttributeError(
            f"'{obj_type.__name__}' object has no accessible method '{method_name}'"
        )

    # Special handling for length
    if method_name == "length":
        return get_safe_length(obj)

    # Call the method
    try:
        method = getattr(obj, method_name)
        return method(*args, **kwargs)
    except AttributeError:
        raise AttributeError(f"'{obj_type.__name__}' object has no method '{method_name}'")


def get_safe_length(obj: Any) -> int:
    """
    Safe length access that maps to Python's len().

    Args:
        obj: Object to get length of

    Returns:
        Length of the object

    Raises:
        TypeError: If object has no length
    """
    try:
        return len(obj)
    except TypeError:
        raise TypeError(f"object of type '{type(obj).__name__}' has no len()")


def is_ml_object(obj: Any) -> bool:
    """
    Detect if object is an ML object (dict with string keys).

    Args:
        obj: Object to check

    Returns:
        True if object appears to be an ML object
    """
    return isinstance(obj, dict) and all(isinstance(k, str) for k in obj.keys())


def get_object_type_name(obj: Any) -> str:
    """
    Get a user-friendly type name for error messages.

    Args:
        obj: Object to get type name for

    Returns:
        Human-readable type name
    """
    obj_type = type(obj)
    if obj_type == dict and is_ml_object(obj):
        return "ML object"
    return obj_type.__name__


# Public API for transpiled ML code
__all__ = [
    "safe_attr_access",
    "safe_method_call",
    "get_safe_length",
    "is_ml_object",
    "SecurityError",
]
