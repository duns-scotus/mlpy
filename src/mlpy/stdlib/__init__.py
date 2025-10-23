"""ML Standard Library - Auto-discovered bridge modules.

All *_bridge.py modules in this directory are automatically discovered
and made available for import in ML code.

Design:
- Lazy Loading: Modules are only imported when ML code uses them
- Auto-Discovery: No manual registration required
- Extension Support: Custom modules can be added via python_extension_paths

Note: int, float, string, and array primitives are handled by the builtin module.
These are primitive types, not importable modules.
"""

from .module_registry import get_registry


def __getattr__(name: str):
    """Lazy module attribute access.

    When ML code does `from mlpy.stdlib.math_bridge import math`,
    this function is called to get the 'math' attribute.

    This enables:
    - Lazy loading: Only import modules when used
    - Auto-discovery: No manual imports needed
    - Extension support: Custom modules available automatically
    """
    registry = get_registry()
    module_instance = registry.get_module(name)

    if module_instance is not None:
        return module_instance

    raise AttributeError(f"Module '{name}' not found in ML stdlib")


def __dir__():
    """Return list of available modules for introspection.

    This allows tab-completion and discovery of available modules in REPL.
    """
    registry = get_registry()
    return sorted(registry.get_all_module_names())


# Eager-load builtin module (always needed for runtime)
from .builtin import builtin
__all__ = ["builtin"]
