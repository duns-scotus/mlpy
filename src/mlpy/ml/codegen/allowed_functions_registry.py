"""Allowed Functions Registry for Compile-Time Whitelist Enforcement.

This module provides a whitelist-based security system for ML code generation.
Only explicitly allowed functions can be called in generated Python code:

1. ML Builtin Functions (from stdlib.builtin module via @ml_function decorators)
2. User-Defined Functions (defined in the current ML program)
3. Imported Module Functions (from whitelisted stdlib modules)

All other function calls are blocked at compile-time with CodeGenError.
"""

from dataclasses import dataclass, field
from typing import Dict, Set, Optional

from mlpy.stdlib.decorators import get_module_metadata, ModuleMetadata


@dataclass
class AllowedFunctionsRegistry:
    """Whitelist of all allowed functions in the current compilation context.

    Security Model:
    - WHITELIST approach: Only explicitly allowed functions can be called
    - BLOCKS everything else at compile-time (no Python builtin shadowing)
    - THREE categories: ML builtins, user-defined, imported stdlib

    Usage:
        registry = AllowedFunctionsRegistry()

        # Check if function is allowed
        if registry.is_allowed_builtin("len"):
            # Generate: builtin.len(...)
        elif registry.is_user_defined("myFunc"):
            # Generate: myFunc(...)
        elif registry.is_imported_function("math", "sqrt"):
            # Generate: math.sqrt(...)
        else:
            # BLOCK: raise CodeGenError
    """

    # Category 1: ML builtin functions (from @ml_function decorators)
    builtin_functions: Set[str] = field(default_factory=set)

    # Category 2: User-defined functions (from current ML program)
    user_defined_functions: Set[str] = field(default_factory=set)

    # Category 3: Imported stdlib modules and their functions
    imported_modules: Dict[str, ModuleMetadata] = field(default_factory=dict)

    # Track builtin metadata for capabilities
    _builtin_metadata: Optional[ModuleMetadata] = field(default=None, init=False)
    _initialized: bool = field(default=False, init=False)

    def _ensure_initialized(self):
        """Lazy initialization - load builtin metadata when first needed."""
        if not self._initialized:
            # Import builtin module to trigger @ml_module decorator registration
            try:
                from mlpy.stdlib import builtin
            except ImportError:
                pass  # builtin module not available

            # Now get metadata from decorator registry
            self._builtin_metadata = get_module_metadata("builtin")

            if self._builtin_metadata:
                # Populate builtin functions from @ml_function decorators
                self.builtin_functions = set(self._builtin_metadata.functions.keys())

            self._initialized = True

    # ============================================================================
    # Category 1: ML Builtin Functions
    # ============================================================================

    def is_allowed_builtin(self, func_name: str) -> bool:
        """Check if function is an allowed ML builtin.

        Args:
            func_name: Function name (e.g., "len", "print", "range")

        Returns:
            True if function is defined in stdlib.builtin with @ml_function
        """
        self._ensure_initialized()
        return func_name in self.builtin_functions

    def get_builtin_capabilities(self, func_name: str) -> list[str]:
        """Get required capabilities for a builtin function.

        Args:
            func_name: Builtin function name

        Returns:
            List of required capability types (e.g., ["CONSOLE_WRITE"])
        """
        self._ensure_initialized()

        if not self._builtin_metadata:
            return []

        func_meta = self._builtin_metadata.functions.get(func_name)
        return func_meta.capabilities if func_meta else []

    # ============================================================================
    # Category 2: User-Defined Functions
    # ============================================================================

    def register_user_function(self, func_name: str) -> None:
        """Register a user-defined function (from function definition in ML code).

        Args:
            func_name: Function name defined by user
        """
        self.user_defined_functions.add(func_name)

    def is_user_defined(self, func_name: str) -> bool:
        """Check if function is user-defined.

        Args:
            func_name: Function name

        Returns:
            True if function was defined in current ML program
        """
        return func_name in self.user_defined_functions

    # ============================================================================
    # Category 3: Imported Stdlib Functions
    # ============================================================================

    def register_import(self, module_name: str, alias: Optional[str] = None) -> bool:
        """Register an imported ML stdlib module.

        Args:
            module_name: Module name (e.g., "math", "string", "datetime")
            alias: Optional alias (e.g., "import math as m" -> alias="m")

        Returns:
            True if module was successfully registered, False if not found
        """
        metadata = get_module_metadata(module_name)

        if metadata:
            # Use alias if provided, otherwise use module name
            registry_key = alias if alias else module_name
            self.imported_modules[registry_key] = metadata
            return True

        return False

    def is_imported_module(self, module_name: str) -> bool:
        """Check if module is imported.

        Args:
            module_name: Module name or alias

        Returns:
            True if module was imported in current ML program
        """
        return module_name in self.imported_modules

    def is_imported_function(self, module_name: str, func_name: str) -> bool:
        """Check if function belongs to an imported module.

        Args:
            module_name: Module name or alias
            func_name: Function name (e.g., "sqrt" for math.sqrt)

        Returns:
            True if module is imported and contains this function
        """
        metadata = self.imported_modules.get(module_name)

        if metadata:
            return func_name in metadata.functions

        return False

    def get_imported_function_capabilities(self, module_name: str, func_name: str) -> list[str]:
        """Get required capabilities for an imported module function.

        Args:
            module_name: Module name or alias
            func_name: Function name

        Returns:
            List of required capability types
        """
        metadata = self.imported_modules.get(module_name)

        if metadata:
            func_meta = metadata.functions.get(func_name)
            return func_meta.capabilities if func_meta else []

        return []

    # ============================================================================
    # Whitelist Validation
    # ============================================================================

    def is_allowed_simple_call(self, func_name: str) -> bool:
        """Check if a simple function call is allowed (no module prefix).

        Args:
            func_name: Function name (e.g., "len", "myFunc")

        Returns:
            True if function is allowed (builtin or user-defined)
        """
        return self.is_allowed_builtin(func_name) or self.is_user_defined(func_name)

    def is_allowed_member_call(self, module_name: str, func_name: str) -> bool:
        """Check if a member function call is allowed (module.function).

        Args:
            module_name: Module name or alias
            func_name: Function name

        Returns:
            True if module is imported and contains this function
        """
        return self.is_imported_function(module_name, func_name)

    def get_call_category(self, func_name: str) -> str:
        """Determine which category a function call belongs to.

        Args:
            func_name: Function name

        Returns:
            One of: "builtin", "user_defined", "unknown"
        """
        if self.is_allowed_builtin(func_name):
            return "builtin"
        elif self.is_user_defined(func_name):
            return "user_defined"
        else:
            return "unknown"

    # ============================================================================
    # Debugging and Introspection
    # ============================================================================

    def get_all_allowed_functions(self) -> Set[str]:
        """Get set of all allowed simple function names.

        Returns:
            Set containing all builtin and user-defined function names
        """
        self._ensure_initialized()
        return self.builtin_functions | self.user_defined_functions

    def get_statistics(self) -> dict:
        """Get registry statistics for debugging.

        Returns:
            Dictionary with counts and lists of registered items
        """
        self._ensure_initialized()
        return {
            "builtin_count": len(self.builtin_functions),
            "user_defined_count": len(self.user_defined_functions),
            "imported_modules_count": len(self.imported_modules),
            "builtin_functions": sorted(self.builtin_functions),
            "user_defined_functions": sorted(self.user_defined_functions),
            "imported_modules": sorted(self.imported_modules.keys()),
        }

    def __repr__(self) -> str:
        """String representation for debugging."""
        stats = self.get_statistics()
        return (
            f"AllowedFunctionsRegistry("
            f"builtins={stats['builtin_count']}, "
            f"user_defined={stats['user_defined_count']}, "
            f"imported_modules={stats['imported_modules_count']})"
        )


__all__ = ["AllowedFunctionsRegistry"]
