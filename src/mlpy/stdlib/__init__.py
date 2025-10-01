"""ML Standard Library - Auto-imported functionality for ML programs."""

# Core console functionality
# Collections library
from .collections_bridge import collections
from .console_bridge import console

# DateTime operations library
from .datetime_bridge import datetime

# Float operations library
from .float_bridge import float_module

# Functional programming library
from .functional_bridge import functional

# Integer operations library
from .int_bridge import int_module

# Math operations library
from .math_bridge import math

# Random operations library
from .random_bridge import random

# Regex operations library
from .regex_bridge import regex

# String operations library
from .string_bridge import string


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
    import builtins

    if isinstance(value, builtins.bool):
        return "boolean"
    elif isinstance(value, builtins.int) or isinstance(value, builtins.float):
        return "number"
    elif isinstance(value, builtins.str):
        return "string"
    elif isinstance(value, builtins.list):
        return "array"
    elif isinstance(value, builtins.dict):
        return "object"
    elif callable(value):
        return "function"
    else:
        return "unknown"


def int(value):
    """Convert value to integer (ML built-in function)."""
    import builtins

    # Use explicit builtins reference to avoid shadowing issues
    try:
        if value is True:
            return 1
        elif value is False:
            return 0
        elif hasattr(value, "__int__"):
            return value.__int__()
        else:
            # Try string conversion first
            return builtins.int(value)
    except:
        return 0  # Default for any conversion error


def float(value):
    """Convert value to float (ML built-in function)."""
    import builtins

    try:
        if value is True:
            return 1.0
        elif value is False:
            return 0.0
        elif hasattr(value, "__float__"):
            return value.__float__()
        else:
            return builtins.float(value)
    except:
        return 0.0  # Default for any conversion error


def str(value):
    """Convert value to string (ML built-in function)."""
    import builtins

    try:
        if value is True:
            return "true"
        elif value is False:
            return "false"
        elif hasattr(value, "__str__"):
            return value.__str__()
        else:
            return builtins.str(value)
    except:
        return builtins.str(value)


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
    "str",
]
