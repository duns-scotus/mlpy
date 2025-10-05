"""Decorator-based runtime whitelist validator with capability checking.

This module provides runtime validation of function calls by checking for
@ml_function decorator metadata and validating required capabilities.

Key Features:
- Whitelist enforcement via decorator checking
- Runtime capability validation
- Thread-safe capability context management
- Clear error messages for debugging

Author: mlpy development team
Version: 2.0.0
License: MIT
"""

from typing import Any, Callable, List
import threading


class SecurityError(Exception):
    """Raised when a non-whitelisted function call is attempted.

    This indicates that a function without @ml_function decorator
    was called from outside the user's ML code.
    """
    pass


class CapabilityError(Exception):
    """Raised when required capabilities are not available.

    This indicates that a function requires specific permissions
    that have not been granted in the current execution context.
    """
    pass


# Thread-local storage for capability context
_capability_context = threading.local()


# Safe built-in types whose methods don't require decoration
# (already validated by SafeAttributeRegistry, no dunder access)
_SAFE_BUILTIN_TYPES = (str, list, dict, int, float, bool, tuple, set, frozenset)


def get_current_capability_context():
    """Get the current capability context for this thread.

    Returns:
        CapabilityContext instance or None if no context is set

    Thread Safety:
        Uses thread-local storage, safe for concurrent execution
    """
    return getattr(_capability_context, 'context', None)


def set_capability_context(context):
    """Set the capability context for this thread.

    Args:
        context: CapabilityContext instance or None to clear

    Thread Safety:
        Sets context in thread-local storage
    """
    _capability_context.context = context


def check_capabilities(required: List[str]) -> None:
    """Check if current context has required capabilities.

    Args:
        required: List of required capability types (e.g., ["FILE_READ"])

    Raises:
        CapabilityError: If any required capability is not available

    Example:
        check_capabilities(["FILE_READ", "FILE_WRITE"])
    """
    if not required:
        # No capabilities required
        return

    # Get current context
    context = get_current_capability_context()

    if not context:
        # No context but capabilities are required
        raise CapabilityError(
            f"Function requires capabilities {required}, but no capability context is active.\n"
            f"\n"
            f"This function needs specific permissions that are not available.\n"
            f"Make sure to run this code within a proper capability context:\n"
            f"\n"
            f"  from mlpy.runtime.capabilities import CapabilityContext\n"
            f"  with CapabilityContext() as ctx:\n"
            f"      # Grant required capabilities\n"
            f"      ctx.add_capability(...)\n"
            f"      # Execute your code here\n"
        )

    # Check each required capability
    missing = []
    for cap_type in required:
        if not context.has_capability(cap_type):
            missing.append(cap_type)

    if missing:
        # Get available capabilities for error message
        available = []
        try:
            for cap_type in context.get_all_capabilities():
                available.append(cap_type)
        except:
            available = ["<unable to retrieve>"]

        raise CapabilityError(
            f"Missing required capabilities: {missing}\n"
            f"Available capabilities: {available}\n"
            f"\n"
            f"This function requires permissions that have not been granted.\n"
            f"Add these capabilities to your execution context:\n"
            f"\n"
            f"  ctx.add_capability(CapabilityType(...))\n"
        )


def safe_call(func: Callable, *args, **kwargs) -> Any:
    """Validate and execute function call with whitelist and capability checking.

    This is the core security function that enforces the runtime whitelist.
    Every function call in generated ML code goes through this validator.

    Validation Rules:
    1. Function decorated with @ml_function → Check capabilities, then allow
    2. User-defined function (module __main__) → Allow (trusted)
    3. Method on safe built-in type (str, list, etc.) → Allow (pre-validated)
    4. Method on @ml_class decorated object → Allow
    5. Everything else → Block with SecurityError

    Args:
        func: Function/callable to validate and execute
        *args: Positional arguments to pass to function
        **kwargs: Keyword arguments to pass to function

    Returns:
        Result of function call if validation passes

    Raises:
        TypeError: If func is not callable
        SecurityError: If func is not whitelisted (missing @ml_function decorator)
        CapabilityError: If required capabilities are not available

    Examples:
        # ML builtin (decorated, no capabilities):
        safe_call(builtin.len, [1, 2, 3])  # ✅ Returns 3

        # ML stdlib (decorated, with capabilities):
        safe_call(file.read, "/data/file.txt")  # ✅ If FILE_READ available
                                                 # ❌ CapabilityError if not

        # User function (trusted):
        def my_func(x): return x * 2
        safe_call(my_func, 21)  # ✅ Returns 42

        # Python builtin (not decorated):
        safe_call(eval, "2+2")  # ❌ SecurityError

    Security:
        - Blocks all Python builtins (eval, exec, open, __import__, etc.)
        - Blocks functions from non-whitelisted modules
        - Enforces capability requirements at runtime
        - Prevents sandbox escape via dynamic calls
    """
    # Step 1: Type validation
    if not callable(func):
        func_type = type(func).__name__
        raise TypeError(
            f"Cannot call object of type '{func_type}': not callable\n"
            f"Expected a function, got {func_type}"
        )

    # Step 2: Check for @ml_function decorator metadata (PRIMARY CHECK)
    if hasattr(func, '_ml_function_metadata'):
        metadata = func._ml_function_metadata

        # Extract required capabilities from decorator
        # metadata is a FunctionMetadata object, not a dict
        required_caps = metadata.capabilities if hasattr(metadata, 'capabilities') else []
        if required_caps is None:
            required_caps = []

        # Validate capabilities if any are required
        if required_caps:
            check_capabilities(required_caps)

        # Function is whitelisted and capabilities satisfied
        return func(*args, **kwargs)

    # Step 3: Check if user-defined function (TRUSTED)
    func_module = getattr(func, '__module__', None)
    if func_module in ('__main__', None):
        # User-defined functions are trusted within the same file
        # They don't need decoration or capability checks
        # (Capability checks happen at @ml_function boundaries inside them)
        return func(*args, **kwargs)

    # Step 4: Check if method on safe built-in type
    if hasattr(func, '__self__'):
        # This is a bound method
        obj = func.__self__
        obj_type = type(obj)

        if obj_type in _SAFE_BUILTIN_TYPES:
            # Method on safe built-in type (str.upper, list.append, etc.)
            # These are pre-validated by SafeAttributeRegistry
            # Dunder methods are blocked by _safe_attr_access
            return func(*args, **kwargs)

        # Check if method on @ml_class decorated object
        if hasattr(obj_type, '_ml_class_metadata'):
            # Method on ML-decorated class instance
            # TODO: Future enhancement - check method-level capabilities?
            return func(*args, **kwargs)

    # Step 5: Check if unbound method on safe type
    if hasattr(func, '__objclass__'):
        objclass = func.__objclass__
        if objclass in _SAFE_BUILTIN_TYPES:
            # Unbound method on safe type
            return func(*args, **kwargs)

    # Step 6: Not whitelisted → BLOCK
    func_name = getattr(func, '__name__', '<unknown>')
    func_module_str = func_module if func_module else '<unknown>'

    raise SecurityError(
        f"SecurityError: Cannot call '{func_name}' from module '{func_module_str}'\n"
        f"\n"
        f"This function is NOT decorated with @ml_function.\n"
        f"\n"
        f"Allowed function sources:\n"
        f"  ✓ ML stdlib functions (decorated with @ml_function)\n"
        f"  ✓ User-defined functions (defined in your ML code)\n"
        f"  ✓ Methods on safe types (str, list, dict, etc.)\n"
        f"  ✓ Methods on @ml_class decorated objects\n"
        f"\n"
        f"Python built-in functions are BLOCKED for security:\n"
        f"  ✗ eval, exec, compile - Code execution risk\n"
        f"  ✗ open, __import__ - File/module access requires capabilities\n"
        f"  ✗ getattr, setattr, delattr - Use ML builtin equivalents\n"
        f"  ✗ help, dir, vars - Use ML builtin equivalents\n"
        f"\n"
        f"How to fix:\n"
        f"  • Use ML builtins: builtin.len() instead of len()\n"
        f"  • Import ML modules: import math; math.sqrt()\n"
        f"  • Define in ML: function {func_name}(...) {{ ... }}\n"
    )


__all__ = [
    'safe_call',
    'SecurityError',
    'CapabilityError',
    'get_current_capability_context',
    'set_capability_context',
    'check_capabilities',
]
