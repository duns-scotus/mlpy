"""
ML Builtin Module - Core functionality for all ML programs.

This module demonstrates the future decorator-based module system for mlpy.
It provides essential built-in functions that are automatically available
in all ML programs without requiring explicit import.

Author: mlpy development team
Version: 2.0.0
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

    Args:
        name: Module name for ML imports
        capabilities: List of required capabilities
        description: Module description (uses class docstring if None)
        version: Module version
        auto_import: If True, automatically imported in all ML programs
    """
    def decorator(cls):
        # In real implementation, this would:
        # 1. Register module with ModuleRegistry
        # 2. Extract metadata from class
        # 3. Create capability-checking wrappers
        # 4. Make module discoverable
        cls._ml_module_metadata = {
            'name': name,
            'capabilities': capabilities or [],
            'description': description or cls.__doc__,
            'version': version,
            'auto_import': auto_import,
            'members': {},
        }
        return cls
    return decorator


def ml_function(func: Callable = None, *, name: str = None, capabilities: list[str] = None,
                params: dict[str, type] = None, returns: type = None,
                description: str = None, examples: list[str] = None):
    """
    Decorator for ML-exposed functions/methods.

    Args:
        name: ML function name (uses Python name if None)
        capabilities: Required capabilities (inherits from module if None)
        params: Parameter type specifications for validation
        returns: Return type for documentation
        description: Function description (uses docstring if None)
        examples: Usage examples for documentation
    """
    def decorator(fn):
        # In real implementation, this would:
        # 1. Add metadata to function
        # 2. Create capability-checking wrapper
        # 3. Add parameter validation
        # 4. Register with parent module
        fn._ml_function_metadata = {
            'name': name or fn.__name__,
            'capabilities': capabilities or [],
            'params': params or {},
            'returns': returns,
            'description': description or fn.__doc__,
            'examples': examples or [],
            'exposed': True,
        }

        # Simplified wrapper (real implementation would check capabilities)
        def wrapper(*args, **kwargs):
            # TODO: Check has_capability(cap) for cap in capabilities
            # TODO: Validate parameters against params specification
            # TODO: use_capability(...) to track usage
            return fn(*args, **kwargs)

        wrapper._ml_function_metadata = fn._ml_function_metadata
        wrapper.__name__ = fn.__name__
        wrapper.__doc__ = fn.__doc__
        return wrapper

    if func is None:
        return decorator
    else:
        return decorator(func)


def ml_constant(name: str = None, description: str = None, immutable: bool = True):
    """
    Decorator for ML-exposed constants.

    Args:
        name: ML constant name
        description: Constant description
        immutable: Whether constant can be modified from ML
    """
    def decorator(value):
        # In real implementation, this would create a property that
        # prevents modification if immutable=True
        return value
    return decorator


# ============================================================================
# Builtin Module Implementation
# ============================================================================

@ml_module(
    name="builtin",
    capabilities=[],  # No capabilities required - core functionality
    description="Core built-in functions and utilities for ML programs",
    version="2.0.0",
    auto_import=True  # Automatically available in all ML programs
)
class Builtin:
    """
    ML Built-in Module.

    This module provides essential functionality that every ML program needs:
    - Type conversion: int(), float(), str(), bool()
    - Type checking: type(), typeof(), isinstance()
    - Introspection: dir(), info(), hasattr(), getattr(), setattr()
    - Container utilities: len()
    - I/O: print(), input()
    - Object manipulation: del(), call()
    - System: exit(), version()

    All functions in this module are automatically available in ML programs
    without requiring an explicit import statement.
    """

    # ========================================================================
    # Type Conversion Functions
    # ========================================================================

    @ml_function(
        params={"value": Any},
        returns=int,
        description="Convert value to integer with ML semantics",
        examples=[
            'int("42") // 42',
            'int(3.14) // 3',
            'int(true) // 1',
            'int(false) // 0',
            'int("invalid") // 0  // Returns 0 on error'
        ]
    )
    def int(self, value: Any) -> int:
        """
        Convert value to integer.

        Handles special ML semantics:
        - Booleans: true -> 1, false -> 0
        - Strings: Parses numeric strings, returns 0 on error
        - Floats: Truncates to integer
        - Invalid values: Returns 0 (ML error handling)

        Args:
            value: Value to convert

        Returns:
            Integer representation of value, or 0 if conversion fails
        """
        try:
            if value is True:
                return 1
            elif value is False:
                return 0
            elif isinstance(value, str):
                # Handle float strings like "3.14" -> 3
                if '.' in value:
                    return int(float(value))
                return int(value)
            elif hasattr(value, '__int__'):
                return value.__int__()
            else:
                return int(value)
        except (ValueError, TypeError):
            return 0  # ML error semantics: default to 0

    @ml_function(
        params={"value": Any},
        returns=float,
        description="Convert value to floating-point number",
        examples=[
            'float("3.14") // 3.14',
            'float(42) // 42.0',
            'float(true) // 1.0',
            'float("invalid") // 0.0'
        ]
    )
    def float(self, value: Any) -> float:
        """
        Convert value to floating-point number.

        Handles special ML semantics:
        - Booleans: true -> 1.0, false -> 0.0
        - Strings: Parses numeric strings, returns 0.0 on error
        - Integers: Converts to float
        - Invalid values: Returns 0.0 (ML error handling)

        Args:
            value: Value to convert

        Returns:
            Float representation of value, or 0.0 if conversion fails
        """
        try:
            if value is True:
                return 1.0
            elif value is False:
                return 0.0
            elif hasattr(value, '__float__'):
                return value.__float__()
            else:
                return float(value)
        except (ValueError, TypeError):
            return 0.0  # ML error semantics

    @ml_function(
        params={"value": Any},
        returns=str,
        description="Convert value to string with ML semantics",
        examples=[
            'str(42) // "42"',
            'str(true) // "true"  // Note: lowercase, not "True"',
            'str(false) // "false"',
            'str(3.14) // "3.14"'
        ]
    )
    def str(self, value: Any) -> str:
        """
        Convert value to string.

        Special ML semantics:
        - Booleans: true -> "true", false -> "false" (lowercase!)
        - Numbers: Standard string conversion
        - Arrays: JSON-like representation
        - Objects: JSON-like representation

        Args:
            value: Value to convert

        Returns:
            String representation of value
        """
        try:
            if value is True:
                return "true"  # ML uses lowercase
            elif value is False:
                return "false"  # ML uses lowercase
            elif isinstance(value, (list, dict)):
                # TODO: Implement proper ML-style string representation
                import json
                return json.dumps(value)
            elif hasattr(value, '__str__'):
                return value.__str__()
            else:
                return str(value)
        except Exception:
            return str(value)  # Fallback to Python str()

    @ml_function(
        params={"value": Any},
        returns=bool,
        description="Convert value to boolean",
        examples=[
            'bool(1) // true',
            'bool(0) // false',
            'bool("text") // true',
            'bool("") // false',
            'bool([1,2,3]) // true',
            'bool([]) // false'
        ]
    )
    def bool(self, value: Any) -> bool:
        """
        Convert value to boolean.

        Truthy values: non-zero numbers, non-empty strings/arrays/objects
        Falsy values: 0, empty string, empty array, empty object, None

        Args:
            value: Value to convert

        Returns:
            Boolean representation
        """
        return bool(value)

    # ========================================================================
    # Type Checking Functions
    # ========================================================================

    @ml_function(
        params={"value": Any},
        returns=str,
        description="Get the type of a value as a string",
        examples=[
            'type(42) // "number"',
            'type("hello") // "string"',
            'type(true) // "boolean"',
            'type([1,2,3]) // "array"',
            'type({a: 1}) // "object"',
            'type(print) // "function"'
        ]
    )
    def type(self, value: Any) -> str:
        """
        Get the type of a value as a string.

        Returns ML type names:
        - "boolean" for bool
        - "number" for int/float
        - "string" for str
        - "array" for list
        - "object" for dict
        - "function" for callable
        - "module" for modules
        - "class" for classes
        - "unknown" for anything else

        Args:
            value: Value to check

        Returns:
            Type name as string
        """
        if isinstance(value, bool):
            return "boolean"
        elif isinstance(value, (int, float)):
            return "number"
        elif isinstance(value, str):
            return "string"
        elif isinstance(value, list):
            return "array"
        elif isinstance(value, dict):
            return "object"
        elif callable(value):
            return "function"
        elif hasattr(value, '__module__'):
            return "module"
        elif isinstance(value, type):
            return "class"
        else:
            return "unknown"

    @ml_function(
        params={"value": Any},
        returns=str,
        description="Alias for type() - get the type of a value"
    )
    def typeof(self, value: Any) -> str:
        """Alias for type(). Returns type of value as string."""
        return self.type(value)

    @ml_function(
        params={"value": Any, "type_name": str},
        returns=bool,
        description="Check if value is of specified type",
        examples=[
            'isinstance(42, "number") // true',
            'isinstance("hello", "string") // true',
            'isinstance([1,2], "array") // true',
            'isinstance(42, "string") // false'
        ]
    )
    def isinstance(self, value: Any, type_name: str) -> bool:
        """
        Check if value is of specified type.

        Args:
            value: Value to check
            type_name: Type name ("number", "string", "boolean", etc.)

        Returns:
            True if value is of specified type
        """
        return self.type(value) == type_name

    # ========================================================================
    # Introspection Functions
    # ========================================================================

    @ml_function(
        params={"obj": Any},
        returns=list,
        description="List available attributes and methods of an object or module",
        examples=[
            'members = dir(math) // ["pi", "e", "sqrt", "sin", "cos", ...]',
            'methods = dir("hello") // String methods',
            'props = dir({a: 1, b: 2}) // ["a", "b"]'
        ]
    )
    def dir(self, obj: Any) -> list:
        """
        List available members of an object or module.

        For ML modules: Returns decorated members (functions, constants)
        For Python objects: Returns public attributes (no _ prefix)
        For dicts: Returns keys
        For arrays: Returns ["length", "push", "pop", ...] (future)

        Args:
            obj: Object or module to inspect

        Returns:
            List of member names as strings
        """
        if hasattr(obj, '_ml_module_metadata'):
            # ML module - return registered members
            metadata = obj._ml_module_metadata
            return sorted(metadata.get('members', {}).keys())

        elif isinstance(obj, dict):
            # Dictionary - return keys
            return sorted(obj.keys())

        elif hasattr(obj, '__dict__'):
            # Python object - return public attributes
            return sorted([
                name for name in dir(obj)
                if not name.startswith('_')
            ])

        else:
            return []

    @ml_function(
        params={"obj": Any},
        returns=str,
        description="Get documentation for an object, function, or module",
        examples=[
            'doc = info(math.sqrt) // Function documentation',
            'module_doc = info(math) // Module documentation',
            'class_doc = info(String) // Class documentation'
        ]
    )
    def info(self, obj: Any) -> str:
        """
        Get formatted documentation for an object.

        Returns rich documentation including:
        - Signature (for functions)
        - Description
        - Examples (if available)
        - Required capabilities (if any)
        - Parameters and return types

        Args:
            obj: Object to document

        Returns:
            Formatted documentation string
        """
        if hasattr(obj, '_ml_function_metadata'):
            # ML function - format metadata
            meta = obj._ml_function_metadata
            doc = f"{meta['name']}("

            # Build parameter list
            if meta['params']:
                param_parts = []
                for param_name, param_type in meta['params'].items():
                    type_name = param_type.__name__ if hasattr(param_type, '__name__') else str(param_type)
                    param_parts.append(f"{param_name}: {type_name}")
                doc += ", ".join(param_parts)

            doc += ")"

            # Add return type
            if meta['returns']:
                return_type = meta['returns'].__name__ if hasattr(meta['returns'], '__name__') else str(meta['returns'])
                doc += f" -> {return_type}"

            doc += "\n\n"

            # Add description
            doc += meta['description'] or obj.__doc__ or "No documentation available."

            # Add examples
            if meta['examples']:
                doc += "\n\nExamples:\n"
                for ex in meta['examples']:
                    doc += f"  {ex}\n"

            # Add capabilities
            if meta['capabilities']:
                doc += f"\n\nRequires capabilities: {', '.join(meta['capabilities'])}"

            return doc

        elif hasattr(obj, '_ml_module_metadata'):
            # ML module - format metadata
            meta = obj._ml_module_metadata
            doc = f"Module: {meta['name']} (v{meta['version']})\n\n"
            doc += meta['description'] or "No documentation available."

            if meta['capabilities']:
                doc += f"\n\nRequires capabilities: {', '.join(meta['capabilities'])}"

            # List functions
            functions = [name for name, member in meta.get('members', {}).items()
                        if hasattr(member, '_ml_function_metadata')]
            if functions:
                doc += f"\n\nFunctions: {', '.join(sorted(functions))}"

            return doc

        else:
            # Fallback to Python docstring
            return obj.__doc__ or "No documentation available."

    @ml_function(
        params={"obj": Any, "attr": str},
        returns=bool,
        description="Check if object has attribute",
        examples=[
            'hasattr(math, "pi") // true',
            'hasattr(math, "nonexistent") // false',
            'hasattr({a: 1}, "a") // true'
        ]
    )
    def hasattr(self, obj: Any, attr: str) -> bool:
        """
        Check if object has specified attribute.

        Works with:
        - ML modules (checks decorated members)
        - Python objects (checks attributes)
        - Dictionaries (checks keys)

        Args:
            obj: Object to check
            attr: Attribute name

        Returns:
            True if attribute exists
        """
        if isinstance(obj, dict):
            return attr in obj
        else:
            return hasattr(obj, attr)

    @ml_function(
        params={"obj": Any, "attr": str},
        returns=Any,
        description="Get attribute value from object dynamically",
        examples=[
            'value = getattr(math, "pi") // Same as math.pi',
            'func = getattr(math, "sqrt") // Get function reference',
            'val = getattr({a: 1}, "a") // Same as obj.a or obj["a"]'
        ]
    )
    def getattr(self, obj: Any, attr: str, default: Any = None):
        """
        Get attribute value dynamically.

        Enables dynamic property access without requiring capability escape.
        Respects ML module security boundaries.

        Args:
            obj: Object to access
            attr: Attribute name
            default: Default value if attribute doesn't exist

        Returns:
            Attribute value, or default if not found
        """
        if isinstance(obj, dict):
            return obj.get(attr, default)
        else:
            return getattr(obj, attr, default)

    @ml_function(
        params={"obj": Any, "attr": str, "value": Any},
        description="Set attribute value on object dynamically",
        examples=[
            'setattr(obj, "name", "John") // Same as obj.name = "John"',
            'setattr(config, "timeout", 30)'
        ]
    )
    def setattr(self, obj: Any, attr: str, value: Any) -> None:
        """
        Set attribute value dynamically.

        Args:
            obj: Object to modify
            attr: Attribute name
            value: Value to set
        """
        if isinstance(obj, dict):
            obj[attr] = value
        else:
            setattr(obj, attr, value)

    @ml_function(
        params={"func": Callable, "args": list},
        returns=Any,
        description="Call a function with array of arguments",
        examples=[
            'result = call(math.sqrt, [16]) // 4.0',
            'call(print, ["Hello", "World"]) // print("Hello", "World")',
            'func = getattr(math, "pow"); call(func, [2, 8]) // 256'
        ]
    )
    def call(self, func: Callable, args: list):
        """
        Call a function with array of arguments.

        Enables dynamic function calling without capability escape.
        Capabilities are checked when the actual function executes.

        Args:
            func: Function to call
            args: Array of arguments

        Returns:
            Function return value
        """
        if not callable(func):
            raise TypeError(f"Object is not callable: {type(func)}")

        return func(*args)

    # ========================================================================
    # Container Functions
    # ========================================================================

    @ml_function(
        params={"container": Any},
        returns=int,
        description="Get length of string, array, or object",
        examples=[
            'len("hello") // 5',
            'len([1, 2, 3]) // 3',
            'len({a: 1, b: 2, c: 3}) // 3'
        ]
    )
    def len(self, container: Any) -> int:
        """
        Get length of a container.

        Works with:
        - Strings: number of characters
        - Arrays: number of elements
        - Objects/Dicts: number of keys
        - Any object with __len__

        Args:
            container: Container to measure

        Returns:
            Length as integer

        Raises:
            TypeError: If container doesn't support len()
        """
        try:
            return len(container)
        except TypeError:
            raise TypeError(f"Object of type '{type(container).__name__}' has no len()")

    # ========================================================================
    # I/O Functions
    # ========================================================================

    @ml_function(
        description="Print values to console",
        examples=[
            'print("Hello, World!")',
            'print("Result:", 42)',
            'print("Values:", x, y, z)',
            'print()  // Empty line'
        ]
    )
    def print(self, *args, **kwargs) -> None:
        """
        Print values to console.

        Values are converted to strings using ML str() semantics
        (lowercase "true"/"false" for booleans).

        Multiple arguments are separated by spaces.

        Args:
            *args: Values to print
            **kwargs: Options (sep, end, file) - passed to Python print()
        """
        # Convert boolean values to ML string representation
        ml_args = []
        for arg in args:
            if arg is True:
                ml_args.append("true")
            elif arg is False:
                ml_args.append("false")
            else:
                ml_args.append(arg)

        print(*ml_args, **kwargs)

    @ml_function(
        params={"prompt": str},
        returns=str,
        description="Read line of input from user",
        examples=[
            'name = input("Enter your name: ")',
            'age = int(input("Enter age: "))',
            'choice = input("Continue? (y/n): ")'
        ]
    )
    def input(self, prompt: str = "") -> str:
        """
        Read a line of input from the user.

        Args:
            prompt: Prompt to display (optional)

        Returns:
            User input as string (without trailing newline)
        """
        return input(prompt)

    # ========================================================================
    # Object Manipulation
    # ========================================================================

    @ml_function(
        params={"obj": Any},
        description="Delete object reference",
        examples=[
            'del(temp_var)  // Remove reference',
            'del(cache[key])  // Delete from dict'
        ]
    )
    def del_obj(self, obj: Any) -> None:
        """
        Delete object reference.

        Note: This only removes the reference, not the underlying object
        if other references exist. Use with caution.

        Args:
            obj: Object reference to delete
        """
        # In Python, we can't actually delete from outside the namespace
        # This would need special handling in the transpiler
        # For now, this is a placeholder
        pass

    # ========================================================================
    # System Functions
    # ========================================================================

    @ml_function(
        params={"code": int},
        description="Exit program with status code",
        examples=[
            'exit(0)  // Exit successfully',
            'exit(1)  // Exit with error',
            'if (error) { exit(1); }'
        ]
    )
    def exit(self, code: int = 0) -> None:
        """
        Exit the program with specified status code.

        Args:
            code: Exit status code (0 = success, non-zero = error)
        """
        sys.exit(code)

    @ml_function(
        returns=str,
        description="Get mlpy version information",
        examples=[
            'v = version() // "mlpy 2.0.0"',
            'print("Running:", version())'
        ]
    )
    def version(self) -> str:
        """
        Get mlpy version information.

        Returns:
            Version string like "mlpy 2.0.0"
        """
        # In real implementation, would import from mlpy.__version__
        return "mlpy 2.0.0"


# ============================================================================
# Module Instance and Exports
# ============================================================================

# Create singleton instance
builtin = Builtin()

# Export all public functions for auto-import
__all__ = [
    'builtin',
    # Type conversion
    'int',
    'float',
    'str',
    'bool',
    # Type checking
    'type',
    'typeof',
    'isinstance',
    # Introspection
    'dir',
    'info',
    'hasattr',
    'getattr',
    'setattr',
    'call',
    # Container
    'len',
    # I/O
    'print',
    'input',
    # Object manipulation
    'del_obj',
    # System
    'exit',
    'version',
]


# ============================================================================
# Convenience: Make functions available at module level
# ============================================================================
# This allows both `builtin.int(x)` and `int(x)` to work

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
del_obj = builtin.del_obj
exit = builtin.exit
version = builtin.version


# ============================================================================
# Testing and Demonstration
# ============================================================================

if __name__ == "__main__":
    """
    Demonstration of builtin module functionality.
    Run this file directly to see how the module works.
    """
    print("=" * 60)
    print("ML Builtin Module Demonstration")
    print("=" * 60)
    print()

    # Type conversion
    print("Type Conversion:")
    print(f"  int('42') = {builtin.int('42')}")
    print(f"  float('3.14') = {builtin.float('3.14')}")
    print(f"  str(True) = {builtin.str(True)}")  # "true" not "True"
    print(f"  bool(0) = {builtin.bool(0)}")
    print()

    # Type checking
    print("Type Checking:")
    print(f"  type(42) = {builtin.type(42)}")
    print(f"  type('hello') = {builtin.type('hello')}")
    print(f"  type([1,2,3]) = {builtin.type([1,2,3])}")
    print(f"  isinstance(42, 'number') = {builtin.isinstance(42, 'number')}")
    print()

    # Introspection
    print("Introspection:")
    test_obj = {"a": 1, "b": 2, "c": 3}
    print(f"  dir({test_obj}) = {builtin.dir(test_obj)}")
    print(f"  hasattr(builtin, 'int') = {builtin.hasattr(builtin, 'int')}")
    print(f"  getattr({test_obj}, 'a') = {builtin.getattr(test_obj, 'a')}")
    print()

    # Function info
    print("Function Documentation:")
    print(builtin.info(builtin.int))
    print()

    # Container operations
    print("Container Operations:")
    print(f"  len('hello') = {builtin.len('hello')}")
    print(f"  len([1,2,3,4,5]) = {builtin.len([1,2,3,4,5])}")
    print(f"  len({test_obj}) = {builtin.len(test_obj)}")
    print()

    # Dynamic function calling
    print("Dynamic Function Calling:")

    def sample_func(x, y):
        return x + y

    print(f"  call(sample_func, [10, 20]) = {builtin.call(sample_func, [10, 20])}")
    print()

    # Version info
    print(f"Version: {builtin.version()}")
    print()

    print("=" * 60)
    print("All demonstrations completed successfully!")
    print("=" * 60)
