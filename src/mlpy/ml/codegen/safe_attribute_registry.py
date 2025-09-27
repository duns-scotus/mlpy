"""Safe Attribute Registry - Core Infrastructure for Secure Python Attribute Access

Provides centralized whitelist-based control over which Python attributes/methods
can be safely accessed from ML code, preventing dangerous introspection and
maintaining security while enabling natural object-oriented syntax.
"""

from dataclasses import dataclass, field
from typing import Dict, Set, Type, Any, Optional, List
from enum import Enum


class AttributeAccessType(Enum):
    """Types of attribute access allowed."""
    METHOD = "method"      # Callable attribute
    PROPERTY = "property"  # Non-callable attribute
    FORBIDDEN = "forbidden" # Explicitly blocked


@dataclass
class SafeAttribute:
    """Represents a safe attribute with access control information."""
    name: str
    access_type: AttributeAccessType
    capabilities_required: List[str] = field(default_factory=list)
    description: str = ""


class SafeAttributeRegistry:
    """
    Centralized registry for safe attribute access control.

    Maintains whitelists of allowed attributes for Python built-in types
    and custom ML classes, ensuring only safe operations are permitted.
    """

    def __init__(self):
        self._safe_attributes: Dict[Type, Dict[str, SafeAttribute]] = {}
        self._custom_classes: Dict[str, Dict[str, SafeAttribute]] = {}
        self._dangerous_patterns: Set[str] = set()
        self._init_builtin_types()
        self._init_dangerous_patterns()

    def register_builtin_type(self, python_type: Type, attributes: Dict[str, SafeAttribute]):
        """Register safe attributes for Python built-in type."""
        self._safe_attributes[python_type] = attributes.copy()

    def register_custom_class(self, class_name: str, attributes: Dict[str, SafeAttribute]):
        """Allow stdlib modules to register custom classes."""
        self._custom_classes[class_name] = attributes.copy()

    def is_safe_access(self, obj_type: Type, attr_name: str) -> bool:
        """Check if attribute access is safe for given type."""
        # Check for dangerous patterns first
        if attr_name in self._dangerous_patterns:
            return False

        # Check built-in type whitelist
        if obj_type in self._safe_attributes:
            attr_info = self._safe_attributes[obj_type].get(attr_name)
            return attr_info is not None and attr_info.access_type != AttributeAccessType.FORBIDDEN

        return False

    def get_attribute_info(self, obj_type: Type, attr_name: str) -> Optional[SafeAttribute]:
        """Get detailed information about safe attribute."""
        if obj_type in self._safe_attributes:
            return self._safe_attributes[obj_type].get(attr_name)
        return None

    def _init_builtin_types(self):
        """Initialize whitelists for Python built-in types."""

        # String methods (28 safe methods)
        str_safe_methods = {
            "upper": SafeAttribute("upper", AttributeAccessType.METHOD, [], "Convert to uppercase"),
            "lower": SafeAttribute("lower", AttributeAccessType.METHOD, [], "Convert to lowercase"),
            "strip": SafeAttribute("strip", AttributeAccessType.METHOD, [], "Remove whitespace"),
            "lstrip": SafeAttribute("lstrip", AttributeAccessType.METHOD, [], "Remove left whitespace"),
            "rstrip": SafeAttribute("rstrip", AttributeAccessType.METHOD, [], "Remove right whitespace"),
            "replace": SafeAttribute("replace", AttributeAccessType.METHOD, [], "Replace substring"),
            "split": SafeAttribute("split", AttributeAccessType.METHOD, [], "Split string"),
            "rsplit": SafeAttribute("rsplit", AttributeAccessType.METHOD, [], "Right split string"),
            "join": SafeAttribute("join", AttributeAccessType.METHOD, [], "Join strings"),
            "startswith": SafeAttribute("startswith", AttributeAccessType.METHOD, [], "Check start pattern"),
            "endswith": SafeAttribute("endswith", AttributeAccessType.METHOD, [], "Check end pattern"),
            "find": SafeAttribute("find", AttributeAccessType.METHOD, [], "Find substring index"),
            "rfind": SafeAttribute("rfind", AttributeAccessType.METHOD, [], "Find substring from right"),
            "index": SafeAttribute("index", AttributeAccessType.METHOD, [], "Get substring index"),
            "rindex": SafeAttribute("rindex", AttributeAccessType.METHOD, [], "Get substring index from right"),
            "count": SafeAttribute("count", AttributeAccessType.METHOD, [], "Count occurrences"),
            "isdigit": SafeAttribute("isdigit", AttributeAccessType.METHOD, [], "Check if digits"),
            "isalpha": SafeAttribute("isalpha", AttributeAccessType.METHOD, [], "Check if alphabetic"),
            "isalnum": SafeAttribute("isalnum", AttributeAccessType.METHOD, [], "Check if alphanumeric"),
            "isspace": SafeAttribute("isspace", AttributeAccessType.METHOD, [], "Check if whitespace"),
            "istitle": SafeAttribute("istitle", AttributeAccessType.METHOD, [], "Check if title case"),
            "isupper": SafeAttribute("isupper", AttributeAccessType.METHOD, [], "Check if uppercase"),
            "islower": SafeAttribute("islower", AttributeAccessType.METHOD, [], "Check if lowercase"),
            "capitalize": SafeAttribute("capitalize", AttributeAccessType.METHOD, [], "Capitalize first letter"),
            "title": SafeAttribute("title", AttributeAccessType.METHOD, [], "Convert to title case"),
            "swapcase": SafeAttribute("swapcase", AttributeAccessType.METHOD, [], "Swap case"),
            "center": SafeAttribute("center", AttributeAccessType.METHOD, [], "Center string"),
            "ljust": SafeAttribute("ljust", AttributeAccessType.METHOD, [], "Left justify"),
            "rjust": SafeAttribute("rjust", AttributeAccessType.METHOD, [], "Right justify"),
        }

        # List methods (12 safe methods)
        list_safe_methods = {
            "append": SafeAttribute("append", AttributeAccessType.METHOD, [], "Append element"),
            "extend": SafeAttribute("extend", AttributeAccessType.METHOD, [], "Extend with iterable"),
            "insert": SafeAttribute("insert", AttributeAccessType.METHOD, [], "Insert at index"),
            "remove": SafeAttribute("remove", AttributeAccessType.METHOD, [], "Remove first occurrence"),
            "pop": SafeAttribute("pop", AttributeAccessType.METHOD, [], "Remove and return element"),
            "index": SafeAttribute("index", AttributeAccessType.METHOD, [], "Find element index"),
            "count": SafeAttribute("count", AttributeAccessType.METHOD, [], "Count occurrences"),
            "sort": SafeAttribute("sort", AttributeAccessType.METHOD, [], "Sort in place"),
            "reverse": SafeAttribute("reverse", AttributeAccessType.METHOD, [], "Reverse in place"),
            "clear": SafeAttribute("clear", AttributeAccessType.METHOD, [], "Remove all elements"),
            "copy": SafeAttribute("copy", AttributeAccessType.METHOD, [], "Shallow copy"),
        }

        # Dict methods (9 safe methods)
        dict_safe_methods = {
            "get": SafeAttribute("get", AttributeAccessType.METHOD, [], "Get value with default"),
            "keys": SafeAttribute("keys", AttributeAccessType.METHOD, [], "Get keys view"),
            "values": SafeAttribute("values", AttributeAccessType.METHOD, [], "Get values view"),
            "items": SafeAttribute("items", AttributeAccessType.METHOD, [], "Get items view"),
            "pop": SafeAttribute("pop", AttributeAccessType.METHOD, [], "Remove and return value"),
            "popitem": SafeAttribute("popitem", AttributeAccessType.METHOD, [], "Remove and return item"),
            "update": SafeAttribute("update", AttributeAccessType.METHOD, [], "Update with another dict"),
            "clear": SafeAttribute("clear", AttributeAccessType.METHOD, [], "Remove all items"),
            "setdefault": SafeAttribute("setdefault", AttributeAccessType.METHOD, [], "Get or set default"),
        }

        # Tuple methods (safe, immutable)
        tuple_safe_methods = {
            "count": SafeAttribute("count", AttributeAccessType.METHOD, [], "Count occurrences"),
            "index": SafeAttribute("index", AttributeAccessType.METHOD, [], "Find element index"),
        }

        # Register built-in types
        self._safe_attributes[str] = str_safe_methods
        self._safe_attributes[list] = list_safe_methods
        self._safe_attributes[dict] = dict_safe_methods
        self._safe_attributes[tuple] = tuple_safe_methods

        # Register ML stdlib classes
        self._init_ml_stdlib_types()

    def _init_ml_stdlib_types(self):
        """Initialize safe attributes for ML stdlib classes."""
        # Console class safe methods
        console_safe_methods = {
            "log": SafeAttribute("log", AttributeAccessType.METHOD, [], "Log messages to stdout"),
            "error": SafeAttribute("error", AttributeAccessType.METHOD, [], "Log error messages to stderr"),
            "warn": SafeAttribute("warn", AttributeAccessType.METHOD, [], "Log warning messages"),
            "info": SafeAttribute("info", AttributeAccessType.METHOD, [], "Log info messages"),
            "debug": SafeAttribute("debug", AttributeAccessType.METHOD, [], "Log debug messages"),
        }

        # We need to register by class type, so let's import and register the Console class
        try:
            from ...stdlib.console_bridge import Console
            self._safe_attributes[Console] = console_safe_methods
        except ImportError:
            # If import fails, register by class name for runtime lookup
            self._custom_classes["Console"] = console_safe_methods

    def _init_dangerous_patterns(self):
        """Initialize patterns that are always forbidden."""
        self._dangerous_patterns = {
            # Dunder methods (introspection)
            "__class__", "__dict__", "__globals__", "__bases__", "__mro__", "__subclasses__",
            "__code__", "__closure__", "__defaults__", "__kwdefaults__", "__annotations__",
            "__module__", "__qualname__", "__doc__", "__weakref__", "__getattribute__",
            "__setattr__", "__delattr__", "__getattr__", "__dir__", "__repr__", "__str__",

            # Dynamic attribute access
            "getattr", "setattr", "delattr", "hasattr",

            # Import and execution
            "__import__", "exec", "eval", "compile",

            # File system
            "__file__", "__path__",

            # Other dangerous patterns
            "gi_frame", "gi_code", "cr_frame", "cr_code",
        }


# Global registry instance
_safe_registry = None


def get_safe_registry() -> SafeAttributeRegistry:
    """Get the global safe attribute registry instance."""
    global _safe_registry
    if _safe_registry is None:
        _safe_registry = SafeAttributeRegistry()
    return _safe_registry