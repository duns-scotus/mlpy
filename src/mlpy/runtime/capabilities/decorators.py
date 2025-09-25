"""Decorators for capability-based function protection."""

import functools
from collections.abc import Callable
from contextlib import contextmanager
from typing import Any

from .exceptions import CapabilityNotFoundError
from .manager import get_capability_manager, has_capability, use_capability
from .tokens import create_capability_token


def requires_capability(
    capability_type: str, resource_pattern: str = "", operation: str = "", auto_use: bool = True
) -> Callable[..., Any]:
    """Decorator that requires a specific capability to execute a function.

    Args:
        capability_type: Type of capability required (e.g., "file", "network")
        resource_pattern: Resource pattern to validate against
        operation: Operation type to validate
        auto_use: Whether to automatically use the capability token

    Example:
        @requires_capability("file", "*.txt", "read")
        def read_text_file(filename):
            with open(filename, 'r') as f:
                return f.read()
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Check if capability is available
            if not has_capability(capability_type, resource_pattern, operation):
                raise CapabilityNotFoundError(capability_type, resource_pattern)

            # Automatically use the capability if requested
            if auto_use and resource_pattern and operation:
                use_capability(capability_type, resource_pattern, operation)

            # Execute the function
            return func(*args, **kwargs)

        # Add metadata to the wrapper function
        wrapper._mlpy_capability_required = {
            "capability_type": capability_type,
            "resource_pattern": resource_pattern,
            "operation": operation,
            "auto_use": auto_use,
        }

        return wrapper

    return decorator


def requires_capabilities(*capability_specs) -> Callable:
    """Decorator that requires multiple capabilities.

    Args:
        *capability_specs: Tuples of (capability_type, resource_pattern, operation)

    Example:
        @requires_capabilities(
            ("file", "*.txt", "read"),
            ("network", "api.example.com", "http")
        )
        def process_remote_file():
            pass
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Check all required capabilities
            for spec in capability_specs:
                if len(spec) >= 1:
                    capability_type = spec[0]
                    resource_pattern = spec[1] if len(spec) >= 2 else ""
                    operation = spec[2] if len(spec) >= 3 else ""

                    if not has_capability(capability_type, resource_pattern, operation):
                        raise CapabilityNotFoundError(capability_type, resource_pattern)

            # Use all capabilities if they have resource patterns and operations
            for spec in capability_specs:
                if len(spec) >= 3:
                    capability_type, resource_pattern, operation = spec[:3]
                    if resource_pattern and operation:
                        use_capability(capability_type, resource_pattern, operation)

            return func(*args, **kwargs)

        # Add metadata
        wrapper._mlpy_capabilities_required = capability_specs

        return wrapper

    return decorator


def with_capability(
    capability_type: str,
    resource_patterns: list[str] = None,
    operations: set[str] = None,
    **token_kwargs,
) -> Callable:
    """Decorator that provides a temporary capability for function execution.

    This creates a capability token and adds it to the context for the duration
    of the function call.

    Args:
        capability_type: Type of capability to provide
        resource_patterns: List of resource patterns to allow
        operations: Set of operations to allow
        **token_kwargs: Additional token creation parameters

    Example:
        @with_capability("file", ["temp/*.txt"], {"read", "write"})
        def process_temp_files():
            # Function has temporary file access to temp/*.txt
            pass
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Create temporary capability token
            token = create_capability_token(
                capability_type=capability_type,
                resource_patterns=resource_patterns or [],
                allowed_operations=operations or set(),
                description=f"Temporary capability for {func.__name__}",
                **token_kwargs,
            )

            # Create capability context with the token
            manager = get_capability_manager()
            with manager.capability_context(
                name=f"temp_{capability_type}_{func.__name__}", capabilities=[token]
            ):
                return func(*args, **kwargs)

        # Add metadata
        wrapper._mlpy_capability_provided = {
            "capability_type": capability_type,
            "resource_patterns": resource_patterns or [],
            "operations": operations or set(),
        }

        return wrapper

    return decorator


def capability_safe(allowed_capabilities: list[str], strict: bool = True) -> Callable:
    """Decorator that restricts a function to only use specified capabilities.

    Args:
        allowed_capabilities: List of capability types that function may use
        strict: If True, raises error if function tries to use other capabilities

    Example:
        @capability_safe(["file", "math"], strict=True)
        def safe_file_processor():
            # Can only use file and math capabilities
            pass
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            if strict:
                # TODO: Implement capability usage monitoring during function execution
                # This would require hooking into the capability system to track usage
                pass

            return func(*args, **kwargs)

        # Add metadata
        wrapper._mlpy_capability_restrictions = {
            "allowed_capabilities": allowed_capabilities,
            "strict": strict,
        }

        return wrapper

    return decorator


def capability_context_manager(
    capability_type: str,
    resource_patterns: list[str] = None,
    operations: set[str] = None,
    **token_kwargs,
):
    """Create a context manager that provides capabilities.

    This is useful for creating reusable capability contexts that can be
    used with 'with' statements.

    Args:
        capability_type: Type of capability to provide
        resource_patterns: List of resource patterns to allow
        operations: Set of operations to allow
        **token_kwargs: Additional token creation parameters

    Example:
        file_access = capability_context_manager(
            "file", ["data/*.json"], {"read"}
        )

        with file_access():
            # Code that needs file access
            pass
    """

    @contextmanager
    def context():
        token = create_capability_token(
            capability_type=capability_type,
            resource_patterns=resource_patterns or [],
            allowed_operations=operations or set(),
            description=f"Context manager capability for {capability_type}",
            **token_kwargs,
        )

        manager = get_capability_manager()
        with manager.capability_context(name=f"cm_{capability_type}", capabilities=[token]) as ctx:
            yield ctx

    return context


# Pre-defined common capability decorators
def requires_file_access(patterns: str | list[str], operations: set[str] = None):
    """Shorthand decorator for requiring file access."""
    if isinstance(patterns, str):
        patterns = [patterns]

    return requires_capability(
        "file",
        resource_pattern=patterns[0] if patterns else "",
        operation=",".join(operations) if operations else "",
    )


def requires_network_access(hosts: str | list[str], operations: set[str] = None):
    """Shorthand decorator for requiring network access."""
    if isinstance(hosts, str):
        hosts = [hosts]

    return requires_capability(
        "network",
        resource_pattern=hosts[0] if hosts else "",
        operation=",".join(operations) if operations else "",
    )


def requires_math_capability():
    """Shorthand decorator for requiring math capabilities."""
    return requires_capability("math")


# Function introspection utilities
def get_function_capabilities(func: Callable) -> dict:
    """Get capability requirements for a function."""
    capabilities = {}

    # Single capability requirement
    if hasattr(func, "_mlpy_capability_required"):
        capabilities["required"] = func._mlpy_capability_required

    # Multiple capability requirements
    if hasattr(func, "_mlpy_capabilities_required"):
        capabilities["required_multiple"] = func._mlpy_capabilities_required

    # Provided capabilities
    if hasattr(func, "_mlpy_capability_provided"):
        capabilities["provided"] = func._mlpy_capability_provided

    # Capability restrictions
    if hasattr(func, "_mlpy_capability_restrictions"):
        capabilities["restrictions"] = func._mlpy_capability_restrictions

    return capabilities


def is_capability_protected(func: Callable) -> bool:
    """Check if a function has capability protection."""
    return bool(get_function_capabilities(func))
