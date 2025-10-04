"""ML Standard Library Decorator System.

This module provides decorators for creating ML stdlib modules with:
- Automatic metadata extraction and documentation
- Capability-based security integration
- Safe attribute registry integration for sandbox access
- Introspection support (dir, info, help)

Usage:
    @ml_module(
        name="string",
        description="String manipulation functions",
        capabilities=["string.read", "string.write"]
    )
    class StringModule:
        @ml_function(
            description="Convert string to uppercase",
            capabilities=["string.read"]
        )
        def upper(self, s: str) -> str:
            return s.upper()
"""

from typing import Any, Callable, List, Optional, Type
from functools import wraps


# Global registry of all ML modules
_MODULE_REGISTRY = {}


class ModuleMetadata:
    """Metadata for an ML module."""

    def __init__(
        self,
        name: str,
        description: str,
        capabilities: Optional[List[str]] = None,
        version: str = "1.0.0",
    ):
        self.name = name
        self.description = description
        self.capabilities = capabilities or []
        self.version = version
        self.functions = {}
        self.classes = {}

    def to_dict(self) -> dict:
        """Convert metadata to dictionary for introspection."""
        return {
            "name": self.name,
            "description": self.description,
            "capabilities": self.capabilities,
            "version": self.version,
            "functions": {
                name: {
                    "description": meta.description,
                    "capabilities": meta.capabilities,
                    "params": meta.params,
                    "returns": meta.returns,
                }
                for name, meta in self.functions.items()
            },
            "classes": {
                name: {
                    "description": meta.description,
                    "capabilities": meta.capabilities,
                    "methods": list(meta.methods.keys()),
                }
                for name, meta in self.classes.items()
            },
        }


class FunctionMetadata:
    """Metadata for an ML function."""

    def __init__(
        self,
        name: str,
        description: str,
        capabilities: Optional[List[str]] = None,
        params: Optional[List[dict]] = None,
        returns: Optional[str] = None,
    ):
        self.name = name
        self.description = description
        self.capabilities = capabilities or []
        self.params = params or []
        self.returns = returns


class ClassMetadata:
    """Metadata for an ML class."""

    def __init__(
        self,
        name: str,
        description: str,
        capabilities: Optional[List[str]] = None,
    ):
        self.name = name
        self.description = description
        self.capabilities = capabilities or []
        self.methods = {}


def ml_module(
    name: str,
    description: str,
    capabilities: Optional[List[str]] = None,
    version: str = "1.0.0",
) -> Callable:
    """Decorator for ML stdlib modules.

    Marks a Python class as an ML module and registers it with metadata.

    Args:
        name: Module name (e.g., "string", "math", "datetime")
        description: Human-readable description
        capabilities: Required capabilities for the module
        version: Module version string

    Returns:
        Decorated class with metadata attached

    Example:
        @ml_module(name="string", description="String operations")
        class StringModule:
            @ml_function(description="Convert to uppercase")
            def upper(self, s: str) -> str:
                return s.upper()
    """
    def decorator(cls: Type) -> Type:
        # Create metadata object
        metadata = ModuleMetadata(name, description, capabilities, version)

        # Scan class for decorated methods
        for attr_name in dir(cls):
            if attr_name.startswith("_"):
                continue

            attr = getattr(cls, attr_name)

            # Check if function has metadata (decorated with @ml_function)
            if hasattr(attr, "_ml_function_metadata"):
                func_meta = attr._ml_function_metadata
                metadata.functions[attr_name] = func_meta

            # Check if class has metadata (decorated with @ml_class)
            elif hasattr(attr, "_ml_class_metadata"):
                class_meta = attr._ml_class_metadata
                metadata.classes[attr_name] = class_meta

        # Attach metadata to class
        cls._ml_module_metadata = metadata
        cls._ml_module_name = name

        # Register in global registry
        _MODULE_REGISTRY[name] = cls

        return cls

    return decorator


def ml_function(
    description: str,
    capabilities: Optional[List[str]] = None,
    params: Optional[List[dict]] = None,
    returns: Optional[str] = None,
) -> Callable:
    """Decorator for ML module functions.

    Marks a method as an ML function with metadata for introspection.

    Args:
        description: Human-readable description
        capabilities: Required capabilities for the function
        params: List of parameter descriptions [{"name": "s", "type": "str", "description": "..."}]
        returns: Return type description

    Returns:
        Decorated function with metadata attached

    Example:
        @ml_function(
            description="Convert string to uppercase",
            params=[{"name": "s", "type": "str", "description": "Input string"}],
            returns="str"
        )
        def upper(self, s: str) -> str:
            return s.upper()
    """
    def decorator(func: Callable) -> Callable:
        # Create metadata object
        metadata = FunctionMetadata(
            name=func.__name__,
            description=description,
            capabilities=capabilities,
            params=params,
            returns=returns,
        )

        # Attach metadata to function
        func._ml_function_metadata = metadata

        # Wrap function to preserve behavior
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Future: Add capability validation here
            return func(*args, **kwargs)

        # Transfer metadata to wrapper
        wrapper._ml_function_metadata = metadata

        return wrapper

    return decorator


def ml_class(
    description: str,
    capabilities: Optional[List[str]] = None,
) -> Callable:
    """Decorator for ML classes.

    Marks a class as an ML class with metadata for introspection.

    Args:
        description: Human-readable description
        capabilities: Required capabilities for the class

    Returns:
        Decorated class with metadata attached

    Example:
        @ml_class(description="Regular expression pattern")
        class Pattern:
            def test(self, text: str) -> bool:
                return bool(self.pattern.match(text))
    """
    def decorator(cls: Type) -> Type:
        # Create metadata object
        metadata = ClassMetadata(
            name=cls.__name__,
            description=description,
            capabilities=capabilities,
        )

        # Scan class for decorated methods
        for attr_name in dir(cls):
            if attr_name.startswith("_"):
                continue

            attr = getattr(cls, attr_name)

            # Check if method has metadata (decorated with @ml_function)
            if hasattr(attr, "_ml_function_metadata"):
                func_meta = attr._ml_function_metadata
                metadata.methods[attr_name] = func_meta

        # Attach metadata to class
        cls._ml_class_metadata = metadata

        return cls

    return decorator


def get_module_metadata(module_name: str) -> Optional[ModuleMetadata]:
    """Get metadata for a registered module.

    Args:
        module_name: Name of the module (e.g., "string", "math")

    Returns:
        ModuleMetadata object or None if not found
    """
    module_cls = _MODULE_REGISTRY.get(module_name)
    if module_cls and hasattr(module_cls, "_ml_module_metadata"):
        return module_cls._ml_module_metadata
    return None


def get_all_modules() -> dict:
    """Get all registered ML modules.

    Returns:
        Dictionary mapping module names to their metadata
    """
    return {
        name: cls._ml_module_metadata.to_dict()
        for name, cls in _MODULE_REGISTRY.items()
        if hasattr(cls, "_ml_module_metadata")
    }


__all__ = [
    "ml_module",
    "ml_function",
    "ml_class",
    "ModuleMetadata",
    "FunctionMetadata",
    "ClassMetadata",
    "get_module_metadata",
    "get_all_modules",
]
