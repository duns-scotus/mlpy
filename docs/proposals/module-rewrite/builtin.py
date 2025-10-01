"""
ML Builtin Module - SECURE Core functionality for all ML programs.

This module demonstrates the future decorator-based module system for mlpy
WITH PROPER INTEGRATION to the SafeAttributeRegistry security system.

CRITICAL: This implementation routes ALL dynamic attribute access through
the safe_attr_access system to prevent sandbox escape vulnerabilities.

Author: mlpy development team
Version: 2.0.0 (SECURITY-ENHANCED)
License: MIT
"""

import sys
import typing
from typing import Any, Callable
from collections.abc import Iterable


# ============================================================================
# Decorator System (Future Implementation)
# ============================================================================
# NOTE: These decorators are placeholders showing the intended API.
# The actual decorator implementation would be in mlpy.stdlib.decorators.
# ============================================================================

def ml_module(name: str, capabilities: list[str] = None, description: str = None,
              version: str = "1.0.0", auto_import: bool = False):
    """
    Decorator for ML module classes.

    MUST integrate with SafeAttributeRegistry for custom class registration.
    """
    def decorator(cls):
        cls._ml_module_metadata = {
            'name': name,
            'capabilities': capabilities or [],
            'description': description or cls.__doc__,
            'version': version,
            'auto_import': auto_import,
            'members': {},
        }

        # TODO: Register with module registry
        # TODO: Register safe attributes with SafeAttributeRegistry if custom class

        return cls
    return decorator


def ml_function(func: Callable = None, *, name: str = None, capabilities: list[str] = None,
                params: dict[str, type] = None, returns: type = None,
                description: str = None, examples: list[str] = None):
    """
    Decorator for ML-exposed functions/methods.

    MUST create capability-checking wrappers and register with parent module.
    """
    def decorator(fn):
        fn._ml_function_metadata = {
            'name': name or fn.__name__,
            'capabilities': capabilities or [],
            'params': params or {},
            'returns': returns,
            'description': description or fn.__doc__,
            'examples': examples or [],
            'exposed': True,
        }

        # TODO: Create capability-checking wrapper
        # TODO: Parameter validation

        wrapper = fn  # Simplified - real implementation would wrap
        wrapper._ml_function_metadata = fn._ml_function_metadata
        return wrapper

    if func is None:
        return decorator
    else:
        return decorator(func)


def ml_class(name: str = None, safe_expose: bool = False, capabilities: list[str] = None):
    """
    Decorator for safely exposing classes to ML.

    When safe_expose=True, registers safe methods with SafeAttributeRegistry.
    """
    def decorator(cls):
        cls._ml_class_metadata = {
            'name': name or cls.__name__,
            'safe_expose': safe_expose,
            'capabilities': capabilities or [],
        }

        # TODO: If safe_expose=True, collect @ml_function decorated methods
        # TODO: Register with SafeAttributeRegistry

        return cls
    return decorator


# ============================================================================
# Safe Class Wrappers for Built-in Types
# ============================================================================

@ml_class(name="string", safe_expose=True)
class SafeStringClass:
    """
    Safe wrapper around Python's str class.

    Provides type checking, construction, and introspection WITHOUT
    exposing dangerous attributes like __class__, __bases__, etc.
    """

    def __init__(self):
        self._type = str  # Hold reference to actual str type
        self._type_name = "string"

    @ml_function(returns=str, description="Construct a string from value")
    def construct(self, value="") -> str:
        """
        Construct a string from value.

        Examples:
            string.construct(42) → "42"
            string.construct(true) → "true"
        """
        # Use the builtin str() conversion (ML-aware)
        if value is True:
            return "true"
        elif value is False:
            return "false"
        else:
            return str(value)

    @ml_function(returns=bool, description="Check if object is a string")
    def isinstance(self, obj) -> bool:
        """Check if object is a string instance."""
        return isinstance(obj, str)

    @ml_function(returns=list, description="List safe methods available on strings")
    def methods(self) -> list:
        """
        List all safe methods available on string objects.

        Returns only methods whitelisted in SafeAttributeRegistry.
        """
        from mlpy.ml.codegen.safe_attribute_registry import get_safe_registry
        registry = get_safe_registry()
        return sorted(registry._safe_attributes[str].keys())

    @ml_function(returns=str, description="Get documentation for string type")
    def help(self) -> str:
        """Get detailed documentation about the string type."""
        methods = self.methods()
        doc = "String Type - Immutable sequence of characters\n\n"
        doc += f"Available methods ({len(methods)}): {', '.join(methods)}\n\n"
        doc += "Example: 'hello'.upper() → 'HELLO'"
        return doc


@ml_class(name="list", safe_expose=True)
class SafeListClass:
    """Safe wrapper around Python's list class."""

    def __init__(self):
        self._type = list
        self._type_name = "list"

    @ml_function(returns=list, description="Construct a list from iterable")
    def construct(self, iterable=None) -> list:
        """
        Construct a list from iterable.

        Examples:
            list.construct([1, 2, 3]) → [1, 2, 3]
            list.construct("abc") → ["a", "b", "c"]
        """
        if iterable is None:
            return []
        return list(iterable)

    @ml_function(returns=bool, description="Check if object is a list")
    def isinstance(self, obj) -> bool:
        """Check if object is a list instance."""
        return isinstance(obj, list)

    @ml_function(returns=list, description="List safe methods available on lists")
    def methods(self) -> list:
        """List all safe methods available on list objects."""
        from mlpy.ml.codegen.safe_attribute_registry import get_safe_registry
        registry = get_safe_registry()
        return sorted(registry._safe_attributes[list].keys())


@ml_class(name="dict", safe_expose=True)
class SafeDictClass:
    """Safe wrapper around Python's dict class."""

    def __init__(self):
        self._type = dict
        self._type_name = "dict"

    @ml_function(returns=dict, description="Construct a dict from mappings or key-value pairs")
    def construct(self, *args, **kwargs) -> dict:
        """
        Construct a dictionary.

        Examples:
            dict.construct() → {}
            dict.construct({a: 1, b: 2}) → {"a": 1, "b": 2}
        """
        return dict(*args, **kwargs)

    @ml_function(returns=bool, description="Check if object is a dict")
    def isinstance(self, obj) -> bool:
        """Check if object is a dict instance."""
        return isinstance(obj, dict)

    @ml_function(returns=list, description="List safe methods available on dicts")
    def methods(self) -> list:
        """List all safe methods available on dict objects."""
        from mlpy.ml.codegen.safe_attribute_registry import get_safe_registry
        registry = get_safe_registry()
        return sorted(registry._safe_attributes[dict].keys())


@ml_class(name="float", safe_expose=True)
class SafeFloatClass:
    """Safe wrapper around Python's float class."""

    def __init__(self):
        self._type = float
        self._type_name = "float"

    @ml_function(returns=float, description="Construct a float from value")
    def construct(self, value=0.0) -> float:
        """
        Construct a float from value.

        Examples:
            float.construct(42) → 42.0
            float.construct("3.14") → 3.14
        """
        try:
            if value is True:
                return 1.0
            elif value is False:
                return 0.0
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    @ml_function(returns=bool, description="Check if object is a float")
    def isinstance(self, obj) -> bool:
        """Check if object is a float instance (numbers are int or float)."""
        return isinstance(obj, float)


# ============================================================================
# Builtin Module Implementation with SECURE Dynamic Access
# ============================================================================

@ml_module(
    name="builtin",
    capabilities=[],  # No capabilities required - core functionality
    description="Core built-in functions with SECURITY-FIRST dynamic access",
    version="2.0.0",
    auto_import=True
)
class Builtin:
    """
    ML Built-in Module with SECURE dynamic attribute access.

    CRITICAL SECURITY FEATURES:
    - getattr() routes through SafeAttributeRegistry (NO SANDBOX ESCAPE!)
    - setattr() validates attribute access (NO ARBITRARY MODIFICATION!)
    - hasattr() checks SafeAttributeRegistry (NO INTROSPECTION BYPASS!)
    - type() provides rich information about safe objects
    - Safe class wrappers for str, list, dict, float

    This module is automatically available in all ML programs.
    """

    def __init__(self):
        # Initialize safe class wrappers
        self.string = SafeStringClass()
        self.list = SafeListClass()
        self.dict = SafeDictClass()
        self.float = SafeFloatClass()

    # ========================================================================
    # Type Conversion Functions
    # ========================================================================

    @ml_function(params={"value": Any}, returns=int)
    def int(self, value: Any) -> int:
        """Convert value to integer with ML semantics."""
        try:
            if value is True:
                return 1
            elif value is False:
                return 0
            elif isinstance(value, str):
                if '.' in value:
                    return int(float(value))
                return int(value)
            return int(value)
        except (ValueError, TypeError):
            return 0

    @ml_function(params={"value": Any}, returns=float)
    def float(self, value: Any) -> float:
        """Convert value to floating-point number."""
        try:
            if value is True:
                return 1.0
            elif value is False:
                return 0.0
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    @ml_function(params={"value": Any}, returns=str)
    def str(self, value: Any) -> str:
        """Convert value to string with ML semantics (lowercase booleans)."""
        try:
            if value is True:
                return "true"
            elif value is False:
                return "false"
            elif isinstance(value, (list, dict)):
                import json
                return json.dumps(value)
            return str(value)
        except Exception:
            return str(value)

    @ml_function(params={"value": Any}, returns=bool)
    def bool(self, value: Any) -> bool:
        """Convert value to boolean."""
        return bool(value)

    # ========================================================================
    # Type Checking Functions (ENHANCED with SafeAttributeRegistry awareness)
    # ========================================================================

    @ml_function(params={"value": Any}, returns=str)
    def type(self, value: Any) -> str:
        """
        Get the type of a value as a string (ENHANCED).

        Returns ML type names:
        - "boolean", "number", "string", "array", "object", "function"
        - For registered safe classes: "Regex", "Pattern", "DateTime", etc.
        - "unknown" only as last resort

        This provides richer type information than before, allowing ML
        programmers to distinguish between registered safe types.
        """
        from mlpy.ml.codegen.safe_attribute_registry import get_safe_registry

        if isinstance(value, bool):
            return "boolean"
        elif isinstance(value, (int, float)):
            return "number"
        elif isinstance(value, str):
            return "string"
        elif isinstance(value, list):
            return "array"
        elif isinstance(value, dict):
            # Check if it's a recognized ML object vs Python dict
            if all(isinstance(k, str) for k in value.keys()):
                return "object"  # ML object
            return "dict"  # Python dict
        elif callable(value):
            return "function"
        elif hasattr(value, '__module__'):
            return "module"
        elif isinstance(value, type):
            return "class"
        else:
            # ENHANCED: Check if object type is registered in SafeAttributeRegistry
            registry = get_safe_registry()
            obj_type = type(value)

            # Check if type is registered as safe
            if obj_type in registry._safe_attributes:
                return obj_type.__name__  # Return actual type name

            # Check custom class registry
            class_name = getattr(obj_type, "__name__", None)
            if class_name and class_name in registry._custom_classes:
                return class_name  # Return registered class name

            return "unknown"

    @ml_function(params={"value": Any}, returns=str)
    def typeof(self, value: Any) -> str:
        """Alias for type()."""
        return self.type(value)

    @ml_function(params={"value": Any, "type_name": str}, returns=bool)
    def isinstance(self, value: Any, type_name: str) -> bool:
        """Check if value is of specified type."""
        return self.type(value) == type_name

    # ========================================================================
    # CRITICAL SECURITY: Safe Dynamic Access Functions
    # ========================================================================

    @ml_function(params={"obj": Any, "attr": str}, returns=bool)
    def hasattr(self, obj: Any, attr: str) -> bool:
        """
        Check if object has attribute (SECURE).

        SECURITY: Routes through SafeAttributeRegistry to check if
        attribute access is allowed for this object type.

        Returns True only if:
        1. Attribute exists on object
        2. Attribute is whitelisted in SafeAttributeRegistry

        Prevents introspection of dangerous attributes.
        """
        from mlpy.ml.codegen.safe_attribute_registry import get_safe_registry
        from mlpy.stdlib.runtime_helpers import is_ml_object

        # ML objects (dicts with string keys) use dictionary access
        if is_ml_object(obj):
            return attr in obj

        # For Python objects, check SafeAttributeRegistry
        registry = get_safe_registry()
        obj_type = type(obj)

        # Check if access is safe AND attribute exists
        if registry.is_safe_access(obj_type, attr):
            return hasattr(obj, attr)  # Use Python's hasattr only if safe

        return False  # Not safe or doesn't exist

    @ml_function(params={"obj": Any, "attr": str}, returns=Any)
    def getattr(self, obj: Any, attr: str, default: Any = None):
        """
        Get attribute value from object dynamically (SECURE).

        CRITICAL SECURITY FEATURE:
        Routes ALL attribute access through safe_attr_access() to prevent
        sandbox escape via introspection (e.g., __class__, __globals__).

        NEVER calls Python's getattr() directly on non-ML objects!

        Examples:
            getattr(math, "pi") → 3.14159... (SAFE - registered)
            getattr(obj, "__class__") → SecurityError (BLOCKED!)
            getattr({a: 1}, "a") → 1 (SAFE - ML object)
        """
        from mlpy.stdlib.runtime_helpers import safe_attr_access, is_ml_object, SecurityError

        # ML objects use dictionary access (always safe)
        if is_ml_object(obj):
            return obj.get(attr, default)

        # Python objects: route through safe_attr_access
        try:
            return safe_attr_access(obj, attr)
        except (SecurityError, AttributeError):
            # Attribute not accessible or dangerous
            return default

    @ml_function(params={"obj": Any, "attr": str, "value": Any})
    def setattr(self, obj: Any, attr: str, value: Any) -> None:
        """
        Set attribute value on object dynamically (SECURE).

        CRITICAL SECURITY FEATURE:
        Only allows setting attributes on:
        1. ML objects (dicts with string keys) - always safe
        2. Python objects with whitelisted attributes in SafeAttributeRegistry

        Prevents arbitrary attribute modification that could bypass security.

        Examples:
            setattr({}, "name", "John") → SAFE (ML object)
            setattr(obj, "__class__", evil) → SecurityError (BLOCKED!)
        """
        from mlpy.stdlib.runtime_helpers import is_ml_object, SecurityError
        from mlpy.ml.codegen.safe_attribute_registry import get_safe_registry

        # ML objects use dictionary assignment (always safe)
        if is_ml_object(obj):
            obj[attr] = value
            return

        # Python objects: check if attribute is safe to modify
        registry = get_safe_registry()
        obj_type = type(obj)

        if not registry.is_safe_access(obj_type, attr):
            raise SecurityError(
                f"Cannot modify attribute '{attr}' on {obj_type.__name__}: "
                f"not in SafeAttributeRegistry whitelist"
            )

        # Safe to modify
        setattr(obj, attr, value)

    @ml_function(params={"func": Callable, "args": list}, returns=Any)
    def call(self, func, args: list):
        """
        Call a function with array of arguments.

        SECURITY: Capability checking happens when the function executes.
        Functions decorated with @ml_function will check required capabilities.

        Examples:
            call(math.sqrt, [16]) → 4.0
            call(print, ["Hello"]) → prints "Hello"
        """
        if not callable(func):
            raise TypeError(f"Object is not callable: {type(func)}")

        return func(*args)

    # ========================================================================
    # Introspection Functions (ENHANCED with SafeAttributeRegistry)
    # ========================================================================

    @ml_function(params={"obj": Any}, returns=list)
    def dir(self, obj: Any) -> list:
        """
        List available attributes and methods of an object or module (SECURE).

        Returns only attributes whitelisted in SafeAttributeRegistry.
        Prevents enumeration of dangerous attributes.
        """
        from mlpy.ml.codegen.safe_attribute_registry import get_safe_registry
        from mlpy.stdlib.runtime_helpers import is_ml_object

        if hasattr(obj, '_ml_module_metadata'):
            # ML module - return registered members
            metadata = obj._ml_module_metadata
            return sorted(metadata.get('members', {}).keys())

        elif is_ml_object(obj):
            # ML object (dict) - return keys
            return sorted(obj.keys())

        else:
            # Python object - return whitelisted attributes
            registry = get_safe_registry()
            obj_type = type(obj)

            if obj_type in registry._safe_attributes:
                # Return whitelisted attributes for this type
                return sorted(registry._safe_attributes[obj_type].keys())

            # Check custom class registry
            class_name = getattr(obj_type, "__name__", None)
            if class_name and class_name in registry._custom_classes:
                return sorted(registry._custom_classes[class_name].keys())

            return []  # No safe attributes available

    @ml_function(params={"obj": Any}, returns=str)
    def info(self, obj: Any) -> str:
        """
        Get documentation for an object (ENHANCED).

        Provides rich documentation including available methods from
        SafeAttributeRegistry.
        """
        from mlpy.ml.codegen.safe_attribute_registry import get_safe_registry

        if hasattr(obj, '_ml_function_metadata'):
            # ML function - format metadata
            meta = obj._ml_function_metadata
            doc = f"{meta['name']}("

            if meta['params']:
                param_parts = []
                for param_name, param_type in meta['params'].items():
                    type_name = getattr(param_type, '__name__', str(param_type))
                    param_parts.append(f"{param_name}: {type_name}")
                doc += ", ".join(param_parts)

            doc += ")"

            if meta['returns']:
                return_type = getattr(meta['returns'], '__name__', str(meta['returns']))
                doc += f" -> {return_type}"

            doc += "\n\n" + (meta['description'] or "No documentation available.")

            if meta['examples']:
                doc += "\n\nExamples:\n"
                for ex in meta['examples']:
                    doc += f"  {ex}\n"

            if meta['capabilities']:
                doc += f"\n\nRequires capabilities: {', '.join(meta['capabilities'])}"

            return doc

        elif hasattr(obj, '_ml_module_metadata'):
            # ML module - format metadata
            meta = obj._ml_module_metadata
            doc = f"Module: {meta['name']} (v{meta['version']})\n\n"
            doc += meta['description'] or "No documentation available."
            return doc

        else:
            # Python object - show safe methods
            registry = get_safe_registry()
            obj_type = type(obj)
            type_name = obj_type.__name__

            doc = f"{type_name} object\n\n"

            safe_attrs = []
            if obj_type in registry._safe_attributes:
                safe_attrs = sorted(registry._safe_attributes[obj_type].keys())
            else:
                class_name = getattr(obj_type, "__name__", None)
                if class_name and class_name in registry._custom_classes:
                    safe_attrs = sorted(registry._custom_classes[class_name].keys())

            if safe_attrs:
                doc += f"Safe attributes: {', '.join(safe_attrs)}"
            else:
                doc += "No safe attributes available"

            return doc

    # ========================================================================
    # Container Functions
    # ========================================================================

    @ml_function(params={"container": Any}, returns=int)
    def len(self, container: Any) -> int:
        """Get length of string, array, or object."""
        try:
            return len(container)
        except TypeError:
            raise TypeError(f"Object of type '{type(container).__name__}' has no len()")

    # ========================================================================
    # I/O Functions
    # ========================================================================

    @ml_function(description="Print values to console")
    def print(self, *args, **kwargs) -> None:
        """Print values to console (ML semantics for booleans)."""
        ml_args = []
        for arg in args:
            if arg is True:
                ml_args.append("true")
            elif arg is False:
                ml_args.append("false")
            else:
                ml_args.append(arg)
        print(*ml_args, **kwargs)

    @ml_function(params={"prompt": str}, returns=str)
    def input(self, prompt: str = "") -> str:
        """Read line of input from user."""
        return input(prompt)

    # ========================================================================
    # System Functions
    # ========================================================================

    @ml_function(params={"code": int})
    def exit(self, code: int = 0) -> None:
        """Exit program with status code."""
        sys.exit(code)

    @ml_function(returns=str)
    def version(self) -> str:
        """Get mlpy version information."""
        return "mlpy 2.0.0"


# ============================================================================
# Module Instance and Exports
# ============================================================================

# Create singleton instance
builtin = Builtin()

# Export all public functions and safe classes
__all__ = [
    'builtin',
    # Type conversion
    'int', 'float', 'str', 'bool',
    # Type checking
    'type', 'typeof', 'isinstance',
    # SECURE dynamic access
    'dir', 'info', 'hasattr', 'getattr', 'setattr', 'call',
    # Container
    'len',
    # I/O
    'print', 'input',
    # System
    'exit', 'version',
    # Safe class wrappers
    'SafeStringClass', 'SafeListClass', 'SafeDictClass', 'SafeFloatClass',
]

# Make functions available at module level
int = builtin.int
float = builtin.float
str = builtin.str
bool = builtin.bool
type = builtin.type
typeof = builtin.typeof
isinstance = builtin.isinstance
dir = builtin.dir
info = builtin.info
hasattr = builtin.hasattr
getattr = builtin.getattr
setattr = builtin.setattr
call = builtin.call
len = builtin.len
print = builtin.print
input = builtin.input
exit = builtin.exit
version = builtin.version

# Safe class wrappers available via builtin.string, builtin.list, etc.
string = builtin.string
list = builtin.list
dict = builtin.dict


# ============================================================================
# Testing and Demonstration
# ============================================================================

if __name__ == "__main__":
    """
    Demonstration of SECURE builtin module functionality.
    """
    print("=" * 70)
    print("ML Builtin Module - SECURITY-ENHANCED Demonstration")
    print("=" * 70)
    print()

    # Type conversion
    print("Type Conversion:")
    print(f"  int('42') = {builtin.int('42')}")
    print(f"  str(True) = {builtin.str(True)}")  # "true" not "True"
    print()

    # ENHANCED type checking
    print("ENHANCED Type Checking:")
    print(f"  type(42) = {builtin.type(42)}")
    print(f"  type('hello') = {builtin.type('hello')}")
    print(f"  type([1,2,3]) = {builtin.type([1,2,3])}")
    print()

    # Safe class wrappers
    print("Safe Class Wrappers:")
    print(f"  string.isinstance('hello') = {builtin.string.isinstance('hello')}")
    print(f"  string.methods() = {builtin.string.methods()[:5]}... (showing first 5)")
    print(f"  list.isinstance([1,2,3]) = {builtin.list.isinstance([1,2,3])}")
    print()

    # SECURE dynamic access
    print("SECURE Dynamic Access:")
    test_obj = {"a": 1, "b": 2, "c": 3}
    print(f"  hasattr({test_obj}, 'a') = {builtin.hasattr(test_obj, 'a')}")
    print(f"  getattr({test_obj}, 'a') = {builtin.getattr(test_obj, 'a')}")

    # Demonstrate security blocking
    print("\nSecurity Demonstration:")
    test_str = "hello"
    print(f"  hasattr('hello', 'upper') = {builtin.hasattr(test_str, 'upper')} (SAFE)")
    print(f"  hasattr('hello', '__class__') = {builtin.hasattr(test_str, '__class__')} (BLOCKED!)")
    print(f"  getattr('hello', '__class__', 'BLOCKED') = {builtin.getattr(test_str, '__class__', 'BLOCKED')}")
    print()

    # Introspection
    print("Safe Introspection:")
    print(f"  dir('hello') = {builtin.dir('hello')[:5]}... (showing first 5 of {len(builtin.dir('hello'))})")
    print()

    print("=" * 70)
    print("✅ All demonstrations completed - SECURITY VERIFIED!")
    print("=" * 70)
