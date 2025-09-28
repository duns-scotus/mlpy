"""ML Standard Library - Auto-imported functionality for ML programs."""

# Core console functionality
from .console_bridge import console

# Functional programming library
from .functional_bridge import functional

# String operations library
from .string_bridge import string as string_module

# DateTime operations library
from .datetime_bridge import datetime as datetime_module

# Math operations library
from .math_bridge import math as math_module

# Random operations library
from .random_bridge import random as random_module

# Collections library
from .collections_bridge import collections as collections_module

# Integer operations library
from .int_bridge import int_module

# Float operations library
from .float_bridge import float_module


# Built-in functions that should be available in ML programs
def getCurrentTime():
    """Get current timestamp as string."""
    import datetime

    return datetime.datetime.now().isoformat()


def processData(data):
    """Process input data (placeholder implementation)."""
    return f"processed_{data}"


def typeof(value):
    """Get the type of a value as a string (ML built-in function)."""
    if isinstance(value, bool):
        return "boolean"
    elif isinstance(value, int) or isinstance(value, float):
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


# Export all standard library symbols
__all__ = [
    "console",
    "functional",
    "string_module",
    "datetime_module",
    "math_module",
    "random_module",
    "collections_module",
    "int_module",
    "float_module",
    "getCurrentTime",
    "processData",
    "typeof"
]
