"""ML Standard Library - Bridge module imports only.

Ad-hoc functions have been removed. They will be properly implemented
in the new module system with decorators (Phase 1-4).

Note: int, float, string, and array primitives are handled by the builtin module.
These are primitive types, not importable modules.
"""

# Collections library
from .collections_bridge import collections
from .console_bridge import console

# DateTime operations library
from .datetime_bridge import datetime

# Functional programming library
from .functional_bridge import functional

# JSON operations library
from .json_bridge import json

# Math operations library
from .math_bridge import math

# Random operations library
from .random_bridge import random

# Regex operations library
from .regex_bridge import regex

# File I/O library
from .file_bridge import file

# Path/Filesystem library
from .path_bridge import path

# HTTP client library
from .http_bridge import http


# Export all standard library bridge modules
__all__ = [
    "console",
    "functional",
    "datetime",
    "json",
    "math",
    "random",
    "collections",
    "regex",
    "file",
    "path",
    "http",
]
