"""ML Standard Library - Bridge module imports only.

Ad-hoc functions have been removed. They will be properly implemented
in the new module system with decorators (Phase 1-4).
"""

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


# Export all standard library bridge modules
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
]
