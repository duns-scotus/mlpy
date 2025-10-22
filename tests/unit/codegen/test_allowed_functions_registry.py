"""
Unit tests for allowed_functions_registry.py - Whitelist-based function security.

Tests cover:
- AllowedFunctionsRegistry initialization and lazy loading
- Builtin function whitelisting (ML stdlib)
- User-defined function registration
- Imported module function validation
- Whitelist validation methods
- Debugging and introspection
"""

import pytest
from mlpy.ml.codegen.allowed_functions_registry import AllowedFunctionsRegistry


class TestAllowedFunctionsRegistryInitialization:
    """Test registry initialization and lazy loading."""

    def test_registry_creation(self):
        """Test creating empty registry."""
        registry = AllowedFunctionsRegistry()

        assert registry.user_defined_functions == set()
        assert registry.imported_modules == {}
        assert registry._initialized is False

    def test_lazy_initialization(self):
        """Test lazy initialization on first access."""
        registry = AllowedFunctionsRegistry()

        # Should not be initialized yet
        assert registry._initialized is False

        # First access triggers initialization
        result = registry.is_allowed_builtin("len")

        # Now should be initialized
        assert registry._initialized is True
        assert registry._builtin_metadata is not None
        assert len(registry.builtin_functions) > 0

    def test_builtin_functions_loaded(self):
        """Test that builtin functions are loaded from decorators."""
        registry = AllowedFunctionsRegistry()
        registry._ensure_initialized()

        # Common builtins should be present
        expected_builtins = ["len", "print", "range", "str", "int", "float"]
        for func in expected_builtins:
            assert func in registry.builtin_functions


class TestBuiltinFunctions:
    """Test ML builtin function whitelisting."""

    @pytest.fixture
    def registry(self):
        """Create initialized registry."""
        reg = AllowedFunctionsRegistry()
        reg._ensure_initialized()
        return reg

    def test_is_allowed_builtin_valid(self, registry):
        """Test checking valid builtin functions."""
        assert registry.is_allowed_builtin("len") is True
        assert registry.is_allowed_builtin("print") is True
        assert registry.is_allowed_builtin("range") is True

    def test_is_allowed_builtin_invalid(self, registry):
        """Test checking invalid builtin functions."""
        assert registry.is_allowed_builtin("eval") is False
        assert registry.is_allowed_builtin("exec") is False
        assert registry.is_allowed_builtin("nonexistent") is False

    def test_get_builtin_capabilities_with_caps(self, registry):
        """Test getting capabilities for builtin with requirements."""
        # print requires CONSOLE_WRITE capability
        caps = registry.get_builtin_capabilities("print")
        assert isinstance(caps, list)
        # May or may not have capabilities depending on implementation

    def test_get_builtin_capabilities_no_caps(self, registry):
        """Test getting capabilities for builtin without requirements."""
        caps = registry.get_builtin_capabilities("len")
        assert isinstance(caps, list)

    def test_get_builtin_capabilities_nonexistent(self, registry):
        """Test getting capabilities for nonexistent builtin."""
        caps = registry.get_builtin_capabilities("nonexistent")
        assert caps == []


class TestUserDefinedFunctions:
    """Test user-defined function registration."""

    @pytest.fixture
    def registry(self):
        """Create empty registry."""
        return AllowedFunctionsRegistry()

    def test_register_user_function(self, registry):
        """Test registering user-defined function."""
        registry.register_user_function("myFunc")

        assert "myFunc" in registry.user_defined_functions
        assert registry.is_user_defined("myFunc") is True

    def test_register_multiple_user_functions(self, registry):
        """Test registering multiple user functions."""
        functions = ["func1", "func2", "func3"]

        for func in functions:
            registry.register_user_function(func)

        for func in functions:
            assert registry.is_user_defined(func) is True

    def test_is_user_defined_not_registered(self, registry):
        """Test checking unregistered user function."""
        assert registry.is_user_defined("notRegistered") is False

    def test_user_functions_isolated_from_builtins(self, registry):
        """Test that user functions don't interfere with builtins."""
        registry.register_user_function("customFunc")

        # User function exists
        assert registry.is_user_defined("customFunc") is True

        # But is not a builtin
        assert registry.is_allowed_builtin("customFunc") is False


class TestImportedModules:
    """Test imported module function validation."""

    @pytest.fixture
    def registry(self):
        """Create registry."""
        # Import math_bridge to register it
        from mlpy.stdlib import math_bridge
        return AllowedFunctionsRegistry()

    def test_register_import_valid_module(self, registry):
        """Test registering valid ML stdlib module."""
        result = registry.register_import("math")

        assert result is True
        assert "math" in registry.imported_modules
        assert registry.is_imported_module("math") is True

    def test_register_import_with_alias(self, registry):
        """Test registering module with alias."""
        result = registry.register_import("math", alias="m")

        assert result is True
        assert "m" in registry.imported_modules
        assert registry.is_imported_module("m") is True
        assert "math" not in registry.imported_modules  # Only alias is stored

    def test_register_import_invalid_module(self, registry):
        """Test registering nonexistent module."""
        result = registry.register_import("nonexistent_module")

        assert result is False
        assert "nonexistent_module" not in registry.imported_modules

    def test_is_imported_function_valid(self, registry):
        """Test checking valid imported function."""
        registry.register_import("math")

        # math.sqrt should be available
        assert registry.is_imported_function("math", "sqrt") is True
        assert registry.is_imported_function("math", "floor") is True

    def test_is_imported_function_invalid_function(self, registry):
        """Test checking invalid function from imported module."""
        registry.register_import("math")

        assert registry.is_imported_function("math", "nonexistent") is False

    def test_is_imported_function_not_imported_module(self, registry):
        """Test checking function from non-imported module."""
        assert registry.is_imported_function("math", "sqrt") is False

    def test_get_imported_function_capabilities(self, registry):
        """Test getting capabilities for imported function."""
        registry.register_import("math")

        caps = registry.get_imported_function_capabilities("math", "sqrt")
        assert isinstance(caps, list)

    def test_get_imported_function_capabilities_nonexistent(self, registry):
        """Test getting capabilities for nonexistent imported function."""
        registry.register_import("math")

        caps = registry.get_imported_function_capabilities("math", "nonexistent")
        assert caps == []

    def test_get_imported_function_capabilities_not_imported(self, registry):
        """Test getting capabilities for non-imported module."""
        caps = registry.get_imported_function_capabilities("not_imported", "func")
        assert caps == []


class TestWhitelistValidation:
    """Test whitelist validation methods."""

    @pytest.fixture
    def registry(self):
        """Create registry with test data."""
        # Import math_bridge to register it
        from mlpy.stdlib import math_bridge
        reg = AllowedFunctionsRegistry()
        reg._ensure_initialized()
        reg.register_user_function("myFunc")
        reg.register_import("math")
        return reg

    def test_is_allowed_simple_call_builtin(self, registry):
        """Test simple call validation for builtin."""
        assert registry.is_allowed_simple_call("len") is True
        assert registry.is_allowed_simple_call("print") is True

    def test_is_allowed_simple_call_user_defined(self, registry):
        """Test simple call validation for user-defined."""
        assert registry.is_allowed_simple_call("myFunc") is True

    def test_is_allowed_simple_call_invalid(self, registry):
        """Test simple call validation for invalid function."""
        assert registry.is_allowed_simple_call("eval") is False
        assert registry.is_allowed_simple_call("nonexistent") is False

    def test_is_allowed_member_call_valid(self, registry):
        """Test member call validation for imported function."""
        assert registry.is_allowed_member_call("math", "sqrt") is True
        assert registry.is_allowed_member_call("math", "floor") is True

    def test_is_allowed_member_call_invalid_function(self, registry):
        """Test member call validation for invalid function."""
        assert registry.is_allowed_member_call("math", "nonexistent") is False

    def test_is_allowed_member_call_not_imported(self, registry):
        """Test member call validation for non-imported module."""
        assert registry.is_allowed_member_call("string", "upper") is False

    def test_get_call_category_builtin(self, registry):
        """Test categorizing builtin function call."""
        assert registry.get_call_category("len") == "builtin"
        assert registry.get_call_category("print") == "builtin"

    def test_get_call_category_user_defined(self, registry):
        """Test categorizing user-defined function call."""
        assert registry.get_call_category("myFunc") == "user_defined"

    def test_get_call_category_unknown(self, registry):
        """Test categorizing unknown function call."""
        assert registry.get_call_category("eval") == "unknown"
        assert registry.get_call_category("nonexistent") == "unknown"


class TestDebuggingAndIntrospection:
    """Test debugging and introspection methods."""

    @pytest.fixture
    def registry(self):
        """Create registry with test data."""
        # Import modules to register them
        from mlpy.stdlib import math_bridge, regex_bridge
        reg = AllowedFunctionsRegistry()
        reg._ensure_initialized()
        reg.register_user_function("func1")
        reg.register_user_function("func2")
        reg.register_import("math")
        reg.register_import("regex", alias="r")
        return reg

    def test_get_all_allowed_functions(self, registry):
        """Test getting all allowed simple function names."""
        all_funcs = registry.get_all_allowed_functions()

        # Should contain builtins
        assert "len" in all_funcs
        assert "print" in all_funcs

        # Should contain user-defined
        assert "func1" in all_funcs
        assert "func2" in all_funcs

    def test_get_statistics(self, registry):
        """Test getting registry statistics."""
        stats = registry.get_statistics()

        assert "builtin_count" in stats
        assert "user_defined_count" in stats
        assert "imported_modules_count" in stats
        assert "builtin_functions" in stats
        assert "user_defined_functions" in stats
        assert "imported_modules" in stats

        # Verify counts
        assert stats["builtin_count"] > 0
        assert stats["user_defined_count"] == 2
        assert stats["imported_modules_count"] == 2

        # Verify user-defined functions
        assert "func1" in stats["user_defined_functions"]
        assert "func2" in stats["user_defined_functions"]

        # Verify imported modules (including alias)
        assert "math" in stats["imported_modules"]
        assert "r" in stats["imported_modules"]

    def test_repr(self, registry):
        """Test string representation."""
        repr_str = repr(registry)

        assert "AllowedFunctionsRegistry" in repr_str
        assert "builtins=" in repr_str
        assert "user_defined=" in repr_str
        assert "imported_modules=" in repr_str

    def test_statistics_sorted(self, registry):
        """Test that statistics return sorted lists."""
        stats = registry.get_statistics()

        # Lists should be sorted
        assert stats["builtin_functions"] == sorted(stats["builtin_functions"])
        assert stats["user_defined_functions"] == sorted(stats["user_defined_functions"])
        assert stats["imported_modules"] == sorted(stats["imported_modules"])


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_registry_statistics(self):
        """Test statistics on empty registry."""
        registry = AllowedFunctionsRegistry()
        stats = registry.get_statistics()

        assert stats["user_defined_count"] == 0
        assert stats["imported_modules_count"] == 0
        assert stats["user_defined_functions"] == []
        assert stats["imported_modules"] == []

    def test_duplicate_user_function_registration(self):
        """Test registering same user function twice."""
        registry = AllowedFunctionsRegistry()

        registry.register_user_function("func")
        registry.register_user_function("func")  # Duplicate

        # Should still work (set handles duplicates)
        assert registry.is_user_defined("func") is True
        assert len(registry.user_defined_functions) == 1

    def test_duplicate_import_registration(self):
        """Test importing same module twice."""
        # Import math_bridge to register it
        from mlpy.stdlib import math_bridge
        registry = AllowedFunctionsRegistry()

        result1 = registry.register_import("math")
        result2 = registry.register_import("math")  # Duplicate

        assert result1 is True
        assert result2 is True
        assert len(registry.imported_modules) == 1

    def test_import_with_same_alias_as_module_name(self):
        """Test importing with alias same as module name."""
        # Import math_bridge to register it
        from mlpy.stdlib import math_bridge
        registry = AllowedFunctionsRegistry()

        result = registry.register_import("math", alias="math")

        assert result is True
        assert "math" in registry.imported_modules
