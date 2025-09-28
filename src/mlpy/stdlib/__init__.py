"""ML Standard Library - Auto-imported functionality for ML programs."""

# Core console functionality
from .console_bridge import console

# Functional programming library
from .functional_bridge import functional

# String operations library
from .string_bridge import string

# DateTime operations library
from .datetime_bridge import datetime

# Math operations library
from .math_bridge import math

# Random operations library
from .random_bridge import random

# Collections library
from .collections_bridge import collections

# Regex operations library
from .regex_bridge import regex

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


def int(value):
    """Convert value to integer (ML built-in function)."""
    # Simpler implementation to avoid isinstance issues
    try:
        if value is True:
            return 1
        elif value is False:
            return 0
        elif hasattr(value, '__int__'):
            return value.__int__()
        else:
            # Try string conversion first
            return __builtins__['int'](value)
    except:
        return 0  # Default for any conversion error


def float(value):
    """Convert value to float (ML built-in function)."""
    try:
        if value is True:
            return 1.0
        elif value is False:
            return 0.0
        elif hasattr(value, '__float__'):
            return value.__float__()
        else:
            return __builtins__['float'](value)
    except:
        return 0.0  # Default for any conversion error


def str(value):
    """Convert value to string (ML built-in function)."""
    try:
        if value is True:
            return "true"
        elif value is False:
            return "false"
        elif hasattr(value, '__str__'):
            return value.__str__()
        else:
            return __builtins__['str'](value)
    except:
        return __builtins__['str'](value)


# Export all standard library symbols
__all__ = [
    "console",
    "functional",
    "string",
    "datetime",
    "math",
    "random",
    "collections",
    "regex",
    "int_module",
    "float_module",
    "getCurrentTime",
    "processData",
    "typeof",
    "int",
    "float",
    "str"
]
