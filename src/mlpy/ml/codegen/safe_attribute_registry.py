"""Safe Attribute Registry - Core Infrastructure for Secure Python Attribute Access

Provides centralized whitelist-based control over which Python attributes/methods
can be safely accessed from ML code, preventing dangerous introspection and
maintaining security while enabling natural object-oriented syntax.
"""

from dataclasses import dataclass, field
from enum import Enum


class AttributeAccessType(Enum):
    """Types of attribute access allowed."""

    METHOD = "method"  # Callable attribute
    PROPERTY = "property"  # Non-callable attribute
    FORBIDDEN = "forbidden"  # Explicitly blocked


@dataclass
class SafeAttribute:
    """Represents a safe attribute with access control information."""

    name: str
    access_type: AttributeAccessType
    capabilities_required: list[str] = field(default_factory=list)
    description: str = ""


class SafeAttributeRegistry:
    """
    Centralized registry for safe attribute access control.

    Maintains whitelists of allowed attributes for Python built-in types
    and custom ML classes, ensuring only safe operations are permitted.
    """

    def __init__(self):
        self._safe_attributes: dict[type, dict[str, SafeAttribute]] = {}
        self._custom_classes: dict[str, dict[str, SafeAttribute]] = {}
        self._dangerous_patterns: set[str] = set()
        self._init_builtin_types()
        self._init_dangerous_patterns()
        self._init_stdlib_classes()

    def register_builtin_type(self, python_type: type, attributes: dict[str, SafeAttribute]):
        """Register safe attributes for Python built-in type."""
        self._safe_attributes[python_type] = attributes.copy()

    def register_custom_class(self, class_name: str, attributes: dict[str, SafeAttribute]):
        """Allow stdlib modules to register custom classes."""
        self._custom_classes[class_name] = attributes.copy()

    def is_safe_access(self, obj_type: type, attr_name: str) -> bool:
        """Check if attribute access is safe for given type."""
        # Check built-in type whitelist first
        if obj_type in self._safe_attributes:
            attr_info = self._safe_attributes[obj_type].get(attr_name)
            return attr_info is not None and attr_info.access_type != AttributeAccessType.FORBIDDEN

        # Check custom class whitelist by class name
        # Custom classes take precedence over dangerous patterns
        # (e.g., regex.compile() is safe even though Python's compile() is dangerous)
        class_name = getattr(obj_type, "__name__", str(obj_type))
        if class_name in self._custom_classes:
            attr_info = self._custom_classes[class_name].get(attr_name)
            return attr_info is not None and attr_info.access_type != AttributeAccessType.FORBIDDEN

        # Check dangerous patterns last (only for unknown types)
        # This prevents access to dangerous built-ins like compile(), eval(), exec()
        if attr_name in self._dangerous_patterns:
            return False

        return False

    def get_attribute_info(self, obj_type: type, attr_name: str) -> SafeAttribute | None:
        """Get detailed information about safe attribute."""
        if obj_type in self._safe_attributes:
            return self._safe_attributes[obj_type].get(attr_name)

        # Check custom class whitelist by class name
        class_name = getattr(obj_type, "__name__", str(obj_type))
        if class_name in self._custom_classes:
            return self._custom_classes[class_name].get(attr_name)

        return None

    def _init_builtin_types(self):
        """Initialize whitelists for Python built-in types."""

        # String methods (28 safe methods)
        str_safe_methods = {
            "upper": SafeAttribute("upper", AttributeAccessType.METHOD, [], "Convert to uppercase"),
            "lower": SafeAttribute("lower", AttributeAccessType.METHOD, [], "Convert to lowercase"),
            "strip": SafeAttribute("strip", AttributeAccessType.METHOD, [], "Remove whitespace"),
            "lstrip": SafeAttribute(
                "lstrip", AttributeAccessType.METHOD, [], "Remove left whitespace"
            ),
            "rstrip": SafeAttribute(
                "rstrip", AttributeAccessType.METHOD, [], "Remove right whitespace"
            ),
            "replace": SafeAttribute(
                "replace", AttributeAccessType.METHOD, [], "Replace substring"
            ),
            "split": SafeAttribute("split", AttributeAccessType.METHOD, [], "Split string"),
            "rsplit": SafeAttribute("rsplit", AttributeAccessType.METHOD, [], "Right split string"),
            "join": SafeAttribute("join", AttributeAccessType.METHOD, [], "Join strings"),
            "startswith": SafeAttribute(
                "startswith", AttributeAccessType.METHOD, [], "Check start pattern"
            ),
            "endswith": SafeAttribute(
                "endswith", AttributeAccessType.METHOD, [], "Check end pattern"
            ),
            "find": SafeAttribute("find", AttributeAccessType.METHOD, [], "Find substring index"),
            "rfind": SafeAttribute(
                "rfind", AttributeAccessType.METHOD, [], "Find substring from right"
            ),
            "index": SafeAttribute("index", AttributeAccessType.METHOD, [], "Get substring index"),
            "rindex": SafeAttribute(
                "rindex", AttributeAccessType.METHOD, [], "Get substring index from right"
            ),
            "count": SafeAttribute("count", AttributeAccessType.METHOD, [], "Count occurrences"),
            "isdigit": SafeAttribute("isdigit", AttributeAccessType.METHOD, [], "Check if digits"),
            "isalpha": SafeAttribute(
                "isalpha", AttributeAccessType.METHOD, [], "Check if alphabetic"
            ),
            "isalnum": SafeAttribute(
                "isalnum", AttributeAccessType.METHOD, [], "Check if alphanumeric"
            ),
            "isspace": SafeAttribute(
                "isspace", AttributeAccessType.METHOD, [], "Check if whitespace"
            ),
            "istitle": SafeAttribute(
                "istitle", AttributeAccessType.METHOD, [], "Check if title case"
            ),
            "isupper": SafeAttribute(
                "isupper", AttributeAccessType.METHOD, [], "Check if uppercase"
            ),
            "islower": SafeAttribute(
                "islower", AttributeAccessType.METHOD, [], "Check if lowercase"
            ),
            "capitalize": SafeAttribute(
                "capitalize", AttributeAccessType.METHOD, [], "Capitalize first letter"
            ),
            "title": SafeAttribute(
                "title", AttributeAccessType.METHOD, [], "Convert to title case"
            ),
            "swapcase": SafeAttribute("swapcase", AttributeAccessType.METHOD, [], "Swap case"),
            "center": SafeAttribute("center", AttributeAccessType.METHOD, [], "Center string"),
            "ljust": SafeAttribute("ljust", AttributeAccessType.METHOD, [], "Left justify"),
            "rjust": SafeAttribute("rjust", AttributeAccessType.METHOD, [], "Right justify"),
            # Add length as a property that maps to len()
            "length": SafeAttribute(
                "length", AttributeAccessType.PROPERTY, [], "Get string length"
            ),
        }

        # List methods (12 safe methods)
        list_safe_methods = {
            "append": SafeAttribute("append", AttributeAccessType.METHOD, [], "Append element"),
            "extend": SafeAttribute(
                "extend", AttributeAccessType.METHOD, [], "Extend with iterable"
            ),
            "insert": SafeAttribute("insert", AttributeAccessType.METHOD, [], "Insert at index"),
            "remove": SafeAttribute(
                "remove", AttributeAccessType.METHOD, [], "Remove first occurrence"
            ),
            "pop": SafeAttribute(
                "pop", AttributeAccessType.METHOD, [], "Remove and return element"
            ),
            "index": SafeAttribute("index", AttributeAccessType.METHOD, [], "Find element index"),
            "count": SafeAttribute("count", AttributeAccessType.METHOD, [], "Count occurrences"),
            "sort": SafeAttribute("sort", AttributeAccessType.METHOD, [], "Sort in place"),
            "reverse": SafeAttribute("reverse", AttributeAccessType.METHOD, [], "Reverse in place"),
            "clear": SafeAttribute("clear", AttributeAccessType.METHOD, [], "Remove all elements"),
            "copy": SafeAttribute("copy", AttributeAccessType.METHOD, [], "Shallow copy"),
            # Add length as a property that maps to len()
            "length": SafeAttribute("length", AttributeAccessType.PROPERTY, [], "Get list length"),
        }

        # Dict methods (9 safe methods)
        dict_safe_methods = {
            "get": SafeAttribute("get", AttributeAccessType.METHOD, [], "Get value with default"),
            "keys": SafeAttribute("keys", AttributeAccessType.METHOD, [], "Get keys view"),
            "values": SafeAttribute("values", AttributeAccessType.METHOD, [], "Get values view"),
            "items": SafeAttribute("items", AttributeAccessType.METHOD, [], "Get items view"),
            "pop": SafeAttribute("pop", AttributeAccessType.METHOD, [], "Remove and return value"),
            "popitem": SafeAttribute(
                "popitem", AttributeAccessType.METHOD, [], "Remove and return item"
            ),
            "update": SafeAttribute(
                "update", AttributeAccessType.METHOD, [], "Update with another dict"
            ),
            "clear": SafeAttribute("clear", AttributeAccessType.METHOD, [], "Remove all items"),
            "setdefault": SafeAttribute(
                "setdefault", AttributeAccessType.METHOD, [], "Get or set default"
            ),
            # Add length as a property that maps to len()
            "length": SafeAttribute("length", AttributeAccessType.PROPERTY, [], "Get dict length"),
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
            "error": SafeAttribute(
                "error", AttributeAccessType.METHOD, [], "Log error messages to stderr"
            ),
            "warn": SafeAttribute("warn", AttributeAccessType.METHOD, [], "Log warning messages"),
            "info": SafeAttribute("info", AttributeAccessType.METHOD, [], "Log info messages"),
            "debug": SafeAttribute("debug", AttributeAccessType.METHOD, [], "Log debug messages"),
        }

        # RegexPattern class safe methods
        regex_pattern_safe_methods = {
            "test": SafeAttribute(
                "test", AttributeAccessType.METHOD, [], "Test if pattern matches text"
            ),
            "find_all": SafeAttribute(
                "find_all", AttributeAccessType.METHOD, [], "Find all matches in text"
            ),
            "find_first": SafeAttribute(
                "find_first", AttributeAccessType.METHOD, [], "Find first match in text"
            ),
            "toString": SafeAttribute(
                "toString", AttributeAccessType.METHOD, [], "Return string representation"
            ),
            "is_valid": SafeAttribute(
                "is_valid", AttributeAccessType.METHOD, [], "Check if pattern is valid"
            ),
        }

        # Register by class name to avoid eager loading of modules
        # The classes will be resolved at runtime when actually needed
        self._custom_classes["Console"] = console_safe_methods
        self._custom_classes["RegexPattern"] = regex_pattern_safe_methods

        # Functional class safe methods
        functional_safe_methods = {
            "map": SafeAttribute("map", AttributeAccessType.METHOD, [], "Map function over iterable"),
            "filter": SafeAttribute("filter", AttributeAccessType.METHOD, [], "Filter iterable with predicate"),
            "reduce": SafeAttribute("reduce", AttributeAccessType.METHOD, [], "Reduce iterable with function"),
            "forEach": SafeAttribute("forEach", AttributeAccessType.METHOD, [], "Execute function for each element"),
            "find": SafeAttribute("find", AttributeAccessType.METHOD, [], "Find first matching element"),
            "some": SafeAttribute("some", AttributeAccessType.METHOD, [], "Test if some elements match"),
            "every": SafeAttribute("every", AttributeAccessType.METHOD, [], "Test if all elements match"),
            "compose": SafeAttribute("compose", AttributeAccessType.METHOD, [], "Compose functions right to left"),
            "pipe": SafeAttribute("pipe", AttributeAccessType.METHOD, [], "Pipe functions left to right"),
            "curry": SafeAttribute("curry", AttributeAccessType.METHOD, [], "Curry a function"),
            "curry2": SafeAttribute("curry2", AttributeAccessType.METHOD, [], "Curry two-argument function"),
            "partition": SafeAttribute("partition", AttributeAccessType.METHOD, [], "Partition array by predicate"),
            "zipWith": SafeAttribute("zipWith", AttributeAccessType.METHOD, [], "Zip arrays with combiner"),
            "takeWhile": SafeAttribute("takeWhile", AttributeAccessType.METHOD, [], "Take elements while predicate true"),
            "juxt": SafeAttribute("juxt", AttributeAccessType.METHOD, [], "Apply multiple functions"),
            "times": SafeAttribute("times", AttributeAccessType.METHOD, [], "Execute function N times"),
            "ifElse": SafeAttribute("ifElse", AttributeAccessType.METHOD, [], "Conditional function application"),
            "cond": SafeAttribute("cond", AttributeAccessType.METHOD, [], "Multi-condition function application"),
        }

        # Register by class name to avoid eager loading of modules
        # The class will be resolved at runtime when actually needed
        self._custom_classes["Functional"] = functional_safe_methods

    def is_safe_attribute_name(self, obj_or_type, attr_name: str) -> bool:
        """Check if attribute name is safe for given object/type.

        Used by builtin.hasattr() to check attribute safety.

        Args:
            obj_or_type: Object instance or type
            attr_name: Attribute name to check

        Returns:
            True if attribute is safe, False otherwise
        """
        # Block ALL dunder attributes immediately
        if attr_name.startswith('_'):
            return False

        # Get type from object if needed
        obj_type = obj_or_type if isinstance(obj_or_type, type) else type(obj_or_type)

        # Check if attribute is in dangerous patterns
        if attr_name in self._dangerous_patterns:
            return False

        # Use existing is_safe_access method
        return self.is_safe_access(obj_type, attr_name)

    def safe_attr_access(self, obj, attr_name: str):
        """Safely get attribute from object.

        Used by builtin.getattr() to route all attribute access through
        SafeAttributeRegistry whitelist.

        Args:
            obj: Object to get attribute from
            attr_name: Attribute name

        Returns:
            Attribute value if safe

        Raises:
            AttributeError: If attribute doesn't exist or is not safe
        """
        # Block ALL dunder attributes immediately
        if attr_name.startswith('_'):
            raise AttributeError(f"Access to private attribute '{attr_name}' is forbidden")

        # Check if attribute is in dangerous patterns
        if attr_name in self._dangerous_patterns:
            raise AttributeError(f"Access to dangerous attribute '{attr_name}' is forbidden")

        # Check if attribute is in whitelist
        obj_type = type(obj)
        if not self.is_safe_access(obj_type, attr_name):
            raise AttributeError(
                f"Attribute '{attr_name}' is not in safe attribute whitelist for type '{obj_type.__name__}'"
            )

        # Attribute is safe - use Python's getattr
        return getattr(obj, attr_name)

    def _init_dangerous_patterns(self):
        """Initialize patterns that are always forbidden."""
        self._dangerous_patterns = {
            # Dunder methods (introspection)
            "__class__",
            "__dict__",
            "__globals__",
            "__bases__",
            "__mro__",
            "__subclasses__",
            "__code__",
            "__closure__",
            "__defaults__",
            "__kwdefaults__",
            "__annotations__",
            "__module__",
            "__qualname__",
            "__doc__",
            "__weakref__",
            "__getattribute__",
            "__setattr__",
            "__delattr__",
            "__getattr__",
            "__dir__",
            "__repr__",
            "__str__",
            # Dynamic attribute access (we provide safe versions)
            # Note: "getattr", "setattr", "delattr", "hasattr" removed from here
            # because we provide safe builtin versions
            # Import and execution
            "__import__",
            "exec",
            "eval",
            "compile",
            # File system
            "__file__",
            "__path__",
            # Other dangerous patterns
            "gi_frame",
            "gi_code",
            "cr_frame",
            "cr_code",
        }

    def _init_stdlib_classes(self):
        """Initialize safe attributes for ML standard library classes."""

        # Regex module class from regex_bridge
        regex_methods = {
            "compile": SafeAttribute(
                "compile", AttributeAccessType.METHOD, [], "Compile regex pattern"
            ),
            "test": SafeAttribute(
                "test", AttributeAccessType.METHOD, [], "Test if pattern matches"
            ),
            "match": SafeAttribute("match", AttributeAccessType.METHOD, [], "Find first match"),
            "findAll": SafeAttribute("findAll", AttributeAccessType.METHOD, [], "Find all matches"),
            "replace": SafeAttribute(
                "replace", AttributeAccessType.METHOD, [], "Replace first occurrence"
            ),
            "replaceAll": SafeAttribute(
                "replaceAll", AttributeAccessType.METHOD, [], "Replace all occurrences"
            ),
            "split": SafeAttribute("split", AttributeAccessType.METHOD, [], "Split by pattern"),
            "escape": SafeAttribute(
                "escape", AttributeAccessType.METHOD, [], "Escape special characters"
            ),
            "isValid": SafeAttribute(
                "isValid", AttributeAccessType.METHOD, [], "Check pattern validity"
            ),
            "count": SafeAttribute("count", AttributeAccessType.METHOD, [], "Count matches"),
            "emailPattern": SafeAttribute(
                "emailPattern", AttributeAccessType.METHOD, [], "Get email pattern"
            ),
            "extractEmails": SafeAttribute(
                "extractEmails", AttributeAccessType.METHOD, [], "Extract emails"
            ),
            "extractPhoneNumbers": SafeAttribute(
                "extractPhoneNumbers", AttributeAccessType.METHOD, [], "Extract phone numbers"
            ),
            "isUrl": SafeAttribute("isUrl", AttributeAccessType.METHOD, [], "Check if valid URL"),
            "removeHtmlTags": SafeAttribute(
                "removeHtmlTags", AttributeAccessType.METHOD, [], "Remove HTML tags"
            ),
            # Snake_case aliases for convenience
            "email_pattern": SafeAttribute(
                "email_pattern", AttributeAccessType.METHOD, [], "Get email pattern (alias)"
            ),
            "extract_emails": SafeAttribute(
                "extract_emails", AttributeAccessType.METHOD, [], "Extract emails (alias)"
            ),
            "extract_phone_numbers": SafeAttribute(
                "extract_phone_numbers",
                AttributeAccessType.METHOD,
                [],
                "Extract phone numbers (alias)",
            ),
            "is_url": SafeAttribute(
                "is_url", AttributeAccessType.METHOD, [], "Check if valid URL (alias)"
            ),
            "remove_html_tags": SafeAttribute(
                "remove_html_tags", AttributeAccessType.METHOD, [], "Remove HTML tags (alias)"
            ),
            "replace_all": SafeAttribute(
                "replace_all", AttributeAccessType.METHOD, [], "Replace all occurrences (alias)"
            ),
            "find_first": SafeAttribute(
                "find_first", AttributeAccessType.METHOD, [], "Find first match (alias)"
            ),
        }
        self.register_custom_class("Regex", regex_methods)

        # Regex Pattern class from regex_bridge module
        pattern_methods = {
            "test": SafeAttribute(
                "test", AttributeAccessType.METHOD, [], "Test if pattern matches text"
            ),
            "match": SafeAttribute("match", AttributeAccessType.METHOD, [], "Find first match"),
            "findAll": SafeAttribute("findAll", AttributeAccessType.METHOD, [], "Find all matches"),
            "replace": SafeAttribute(
                "replace", AttributeAccessType.METHOD, [], "Replace first occurrence"
            ),
            "replaceAll": SafeAttribute(
                "replaceAll", AttributeAccessType.METHOD, [], "Replace all occurrences"
            ),
            "split": SafeAttribute(
                "split", AttributeAccessType.METHOD, [], "Split text by pattern"
            ),
            "count": SafeAttribute("count", AttributeAccessType.METHOD, [], "Count matches"),
            "toString": SafeAttribute(
                "toString", AttributeAccessType.METHOD, [], "Get string representation"
            ),
            "pattern": SafeAttribute("pattern", AttributeAccessType.PROPERTY, [], "Pattern string"),
            # Snake_case aliases
            "find_all": SafeAttribute(
                "find_all", AttributeAccessType.METHOD, [], "Find all matches (alias)"
            ),
            "replace_all": SafeAttribute(
                "replace_all", AttributeAccessType.METHOD, [], "Replace all occurrences (alias)"
            ),
            "to_string": SafeAttribute(
                "to_string", AttributeAccessType.METHOD, [], "Get string representation (alias)"
            ),
        }
        self.register_custom_class("Pattern", pattern_methods)

        # Math module class from math_bridge
        math_methods = {
            "sqrt": SafeAttribute("sqrt", AttributeAccessType.METHOD, [], "Square root"),
            "abs": SafeAttribute("abs", AttributeAccessType.METHOD, [], "Absolute value"),
            "sin": SafeAttribute("sin", AttributeAccessType.METHOD, [], "Sine function"),
            "cos": SafeAttribute("cos", AttributeAccessType.METHOD, [], "Cosine function"),
            "tan": SafeAttribute("tan", AttributeAccessType.METHOD, [], "Tangent function"),
            "ln": SafeAttribute("ln", AttributeAccessType.METHOD, [], "Natural logarithm"),
            "log": SafeAttribute("log", AttributeAccessType.METHOD, [], "Logarithm with base"),
            "exp": SafeAttribute("exp", AttributeAccessType.METHOD, [], "Exponential function"),
            "pow": SafeAttribute("pow", AttributeAccessType.METHOD, [], "Power function"),
            "floor": SafeAttribute("floor", AttributeAccessType.METHOD, [], "Floor function"),
            "ceil": SafeAttribute("ceil", AttributeAccessType.METHOD, [], "Ceiling function"),
            "round": SafeAttribute("round", AttributeAccessType.METHOD, [], "Round function"),
            "min": SafeAttribute("min", AttributeAccessType.METHOD, [], "Minimum value"),
            "max": SafeAttribute("max", AttributeAccessType.METHOD, [], "Maximum value"),
            "random": SafeAttribute("random", AttributeAccessType.METHOD, [], "Random number"),
            "pi": SafeAttribute("pi", AttributeAccessType.PROPERTY, [], "Pi constant"),
            "e": SafeAttribute("e", AttributeAccessType.PROPERTY, [], "Euler's number"),
        }
        self.register_custom_class("Math", math_methods)

        # DateTime module class from datetime_bridge
        datetime_methods = {
            "now": SafeAttribute("now", AttributeAccessType.METHOD, [], "Get current timestamp"),
            "timestamp": SafeAttribute(
                "timestamp", AttributeAccessType.METHOD, [], "Get current timestamp"
            ),
            "createTimestamp": SafeAttribute(
                "createTimestamp",
                AttributeAccessType.METHOD,
                [],
                "Create timestamp from components",
            ),
            "create_datetime_timestamp": SafeAttribute(
                "create_datetime_timestamp",
                AttributeAccessType.METHOD,
                [],
                "Create timestamp from components",
            ),
            "addTimedelta": SafeAttribute(
                "addTimedelta", AttributeAccessType.METHOD, [], "Add time delta"
            ),
            "add_timedelta": SafeAttribute(
                "add_timedelta", AttributeAccessType.METHOD, [], "Add time delta"
            ),
            "add_days": SafeAttribute(
                "add_days", AttributeAccessType.METHOD, [], "Add days to timestamp"
            ),
            "start_of_day": SafeAttribute(
                "start_of_day", AttributeAccessType.METHOD, [], "Start of day"
            ),
            "end_of_day": SafeAttribute("end_of_day", AttributeAccessType.METHOD, [], "End of day"),
            "startOfDay": SafeAttribute(
                "startOfDay", AttributeAccessType.METHOD, [], "Start of day"
            ),
            "endOfDay": SafeAttribute("endOfDay", AttributeAccessType.METHOD, [], "End of day"),
            "startOfMonth": SafeAttribute(
                "startOfMonth", AttributeAccessType.METHOD, [], "Start of month"
            ),
            "endOfMonth": SafeAttribute(
                "endOfMonth", AttributeAccessType.METHOD, [], "End of month"
            ),
            "startOfYear": SafeAttribute(
                "startOfYear", AttributeAccessType.METHOD, [], "Start of year"
            ),
            "endOfYear": SafeAttribute("endOfYear", AttributeAccessType.METHOD, [], "End of year"),
            "daysInMonth": SafeAttribute(
                "daysInMonth", AttributeAccessType.METHOD, [], "Days in month"
            ),
            "calculateAgeYears": SafeAttribute(
                "calculateAgeYears", AttributeAccessType.METHOD, [], "Calculate age in years"
            ),
            "isSameDay": SafeAttribute(
                "isSameDay", AttributeAccessType.METHOD, [], "Check if same day"
            ),
            "addBusinessDays": SafeAttribute(
                "addBusinessDays", AttributeAccessType.METHOD, [], "Add business days"
            ),
            "businessDaysBetween": SafeAttribute(
                "businessDaysBetween", AttributeAccessType.METHOD, [], "Business days between"
            ),
            "convertTimezone": SafeAttribute(
                "convertTimezone", AttributeAccessType.METHOD, [], "Convert timezone"
            ),
        }
        self.register_custom_class("DateTime", datetime_methods)

        # String module class from string_bridge
        string_methods = {
            "upper": SafeAttribute("upper", AttributeAccessType.METHOD, [], "Convert to uppercase"),
            "lower": SafeAttribute("lower", AttributeAccessType.METHOD, [], "Convert to lowercase"),
            "capitalize": SafeAttribute(
                "capitalize", AttributeAccessType.METHOD, [], "Capitalize first letter"
            ),
            "trim": SafeAttribute("trim", AttributeAccessType.METHOD, [], "Remove whitespace"),
            "split": SafeAttribute("split", AttributeAccessType.METHOD, [], "Split string"),
            "join": SafeAttribute("join", AttributeAccessType.METHOD, [], "Join strings"),
            "replace": SafeAttribute(
                "replace", AttributeAccessType.METHOD, [], "Replace substring"
            ),
            "contains": SafeAttribute(
                "contains", AttributeAccessType.METHOD, [], "Check if contains"
            ),
            "startsWith": SafeAttribute(
                "startsWith", AttributeAccessType.METHOD, [], "Check if starts with"
            ),
            "endsWith": SafeAttribute(
                "endsWith", AttributeAccessType.METHOD, [], "Check if ends with"
            ),
            "indexOf": SafeAttribute(
                "indexOf", AttributeAccessType.METHOD, [], "Find index of substring"
            ),
            "substring": SafeAttribute(
                "substring", AttributeAccessType.METHOD, [], "Extract substring"
            ),
            "repeat": SafeAttribute("repeat", AttributeAccessType.METHOD, [], "Repeat string"),
            "padLeft": SafeAttribute("padLeft", AttributeAccessType.METHOD, [], "Pad left"),
            "padRight": SafeAttribute("padRight", AttributeAccessType.METHOD, [], "Pad right"),
            "reverse": SafeAttribute("reverse", AttributeAccessType.METHOD, [], "Reverse string"),
            "toCamelCase": SafeAttribute(
                "toCamelCase", AttributeAccessType.METHOD, [], "Convert to camelCase"
            ),
            "camel_case": SafeAttribute(
                "camel_case", AttributeAccessType.METHOD, [], "Convert to camelCase"
            ),
            "toSnakeCase": SafeAttribute(
                "toSnakeCase", AttributeAccessType.METHOD, [], "Convert to snake_case"
            ),
            "snake_case": SafeAttribute(
                "snake_case", AttributeAccessType.METHOD, [], "Convert to snake_case"
            ),
            "toKebabCase": SafeAttribute(
                "toKebabCase", AttributeAccessType.METHOD, [], "Convert to kebab-case"
            ),
            "kebab_case": SafeAttribute(
                "kebab_case", AttributeAccessType.METHOD, [], "Convert to kebab-case"
            ),
            "toPascalCase": SafeAttribute(
                "toPascalCase", AttributeAccessType.METHOD, [], "Convert to PascalCase"
            ),
            "pascal_case": SafeAttribute(
                "pascal_case", AttributeAccessType.METHOD, [], "Convert to PascalCase"
            ),
        }
        self.register_custom_class("String", string_methods)


# Global registry instance
_safe_registry = None


def get_safe_registry() -> SafeAttributeRegistry:
    """Get the global safe attribute registry instance."""
    global _safe_registry
    if _safe_registry is None:
        _safe_registry = SafeAttributeRegistry()
    return _safe_registry
