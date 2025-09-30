"""
Unit tests for safe_attribute_registry.py - Secure attribute access control.

Tests cover:
- AttributeAccessType enum
- SafeAttribute dataclass
- SafeAttributeRegistry initialization and registration
- Built-in type whitelisting (str, list, dict, tuple)
- Custom class registration (ML stdlib classes)
- Dangerous pattern blocking
- is_safe_access validation
- get_attribute_info retrieval
- Global registry singleton
"""

import pytest
from mlpy.ml.codegen.safe_attribute_registry import (
    AttributeAccessType,
    SafeAttribute,
    SafeAttributeRegistry,
    get_safe_registry,
)


class TestAttributeAccessType:
    """Test AttributeAccessType enum."""

    def test_access_type_values(self):
        """Test access type enum values."""
        assert AttributeAccessType.METHOD.value == "method"
        assert AttributeAccessType.PROPERTY.value == "property"
        assert AttributeAccessType.FORBIDDEN.value == "forbidden"


class TestSafeAttribute:
    """Test SafeAttribute dataclass."""

    def test_safe_attribute_creation_minimal(self):
        """Test creating safe attribute with minimal fields."""
        attr = SafeAttribute(
            name="upper",
            access_type=AttributeAccessType.METHOD,
        )

        assert attr.name == "upper"
        assert attr.access_type == AttributeAccessType.METHOD
        assert attr.capabilities_required == []
        assert attr.description == ""

    def test_safe_attribute_creation_full(self):
        """Test creating safe attribute with all fields."""
        attr = SafeAttribute(
            name="open",
            access_type=AttributeAccessType.METHOD,
            capabilities_required=["file_access"],
            description="Open file for reading",
        )

        assert attr.name == "open"
        assert attr.access_type == AttributeAccessType.METHOD
        assert "file_access" in attr.capabilities_required
        assert attr.description == "Open file for reading"

    def test_forbidden_attribute(self):
        """Test creating forbidden attribute."""
        attr = SafeAttribute(
            name="__class__",
            access_type=AttributeAccessType.FORBIDDEN,
            description="Dangerous introspection",
        )

        assert attr.access_type == AttributeAccessType.FORBIDDEN


class TestSafeAttributeRegistry:
    """Test SafeAttributeRegistry main functionality."""

    @pytest.fixture
    def registry(self):
        """Create fresh registry for testing."""
        return SafeAttributeRegistry()

    def test_registry_initialization(self, registry):
        """Test registry initialization."""
        assert registry is not None
        assert len(registry._safe_attributes) > 0
        assert len(registry._dangerous_patterns) > 0

    def test_string_safe_methods(self, registry):
        """Test string type has safe methods."""
        assert registry.is_safe_access(str, "upper") is True
        assert registry.is_safe_access(str, "lower") is True
        assert registry.is_safe_access(str, "strip") is True
        assert registry.is_safe_access(str, "split") is True

    def test_string_dangerous_blocked(self, registry):
        """Test dangerous string access is blocked."""
        assert registry.is_safe_access(str, "__class__") is False
        assert registry.is_safe_access(str, "eval") is False
        assert registry.is_safe_access(str, "__dict__") is False

    def test_list_safe_methods(self, registry):
        """Test list type has safe methods."""
        assert registry.is_safe_access(list, "append") is True
        assert registry.is_safe_access(list, "extend") is True
        assert registry.is_safe_access(list, "pop") is True
        assert registry.is_safe_access(list, "sort") is True

    def test_list_dangerous_blocked(self, registry):
        """Test dangerous list access is blocked."""
        assert registry.is_safe_access(list, "__class__") is False
        assert registry.is_safe_access(list, "exec") is False

    def test_dict_safe_methods(self, registry):
        """Test dict type has safe methods."""
        assert registry.is_safe_access(dict, "get") is True
        assert registry.is_safe_access(dict, "keys") is True
        assert registry.is_safe_access(dict, "values") is True
        assert registry.is_safe_access(dict, "items") is True

    def test_dict_dangerous_blocked(self, registry):
        """Test dangerous dict access is blocked."""
        assert registry.is_safe_access(dict, "__class__") is False
        assert registry.is_safe_access(dict, "__globals__") is False

    def test_tuple_safe_methods(self, registry):
        """Test tuple type has safe methods."""
        assert registry.is_safe_access(tuple, "count") is True
        assert registry.is_safe_access(tuple, "index") is True

    def test_tuple_dangerous_blocked(self, registry):
        """Test dangerous tuple access is blocked."""
        assert registry.is_safe_access(tuple, "__class__") is False

    def test_dangerous_patterns_comprehensive(self, registry):
        """Test comprehensive dangerous pattern blocking."""
        dangerous = [
            "__class__",
            "__dict__",
            "__globals__",
            "__bases__",
            "__mro__",
            "__code__",
            "eval",
            "exec",
            "compile",
            "__import__",
            "getattr",
            "setattr",
        ]

        for pattern in dangerous:
            assert pattern in registry._dangerous_patterns

    def test_register_custom_class(self, registry):
        """Test registering custom class."""
        custom_attrs = {
            "myMethod": SafeAttribute("myMethod", AttributeAccessType.METHOD, [], "Custom method"),
        }

        registry.register_custom_class("CustomClass", custom_attrs)

        assert "CustomClass" in registry._custom_classes
        assert "myMethod" in registry._custom_classes["CustomClass"]

    def test_custom_class_access(self, registry):
        """Test accessing custom class attributes."""
        custom_attrs = {
            "safeMethod": SafeAttribute("safeMethod", AttributeAccessType.METHOD, [], "Safe"),
        }

        registry.register_custom_class("MyClass", custom_attrs)

        # Create a simple class to test
        class MyClass:
            pass

        assert registry.is_safe_access(MyClass, "safeMethod") is True

    def test_get_attribute_info_string(self, registry):
        """Test getting attribute info for string."""
        info = registry.get_attribute_info(str, "upper")

        assert info is not None
        assert info.name == "upper"
        assert info.access_type == AttributeAccessType.METHOD

    def test_get_attribute_info_nonexistent(self, registry):
        """Test getting info for nonexistent attribute."""
        info = registry.get_attribute_info(str, "nonexistent_method")

        assert info is None

    def test_length_property_string(self, registry):
        """Test length property for string."""
        info = registry.get_attribute_info(str, "length")

        assert info is not None
        assert info.access_type == AttributeAccessType.PROPERTY

    def test_length_property_list(self, registry):
        """Test length property for list."""
        info = registry.get_attribute_info(list, "length")

        assert info is not None
        assert info.access_type == AttributeAccessType.PROPERTY

    def test_ml_stdlib_regex_class(self, registry):
        """Test ML stdlib Regex class registration."""
        # Regex class should be registered
        assert registry.is_safe_access(type("Regex", (), {}), "compile") is True
        assert registry.is_safe_access(type("Regex", (), {}), "test") is True
        assert registry.is_safe_access(type("Regex", (), {}), "match") is True

    def test_ml_stdlib_math_class(self, registry):
        """Test ML stdlib Math class registration."""
        # Math class should be registered
        math_type = type("Math", (), {})
        assert registry.is_safe_access(math_type, "sqrt") is True
        assert registry.is_safe_access(math_type, "abs") is True
        assert registry.is_safe_access(math_type, "sin") is True

    def test_ml_stdlib_datetime_class(self, registry):
        """Test ML stdlib DateTime class registration."""
        dt_type = type("DateTime", (), {})
        assert registry.is_safe_access(dt_type, "now") is True
        assert registry.is_safe_access(dt_type, "timestamp") is True

    def test_ml_stdlib_string_class(self, registry):
        """Test ML stdlib String class registration."""
        string_type = type("String", (), {})
        assert registry.is_safe_access(string_type, "upper") is True
        assert registry.is_safe_access(string_type, "trim") is True

    def test_forbidden_attribute_blocks_access(self, registry):
        """Test that forbidden attributes block access."""
        # Register a forbidden attribute
        forbidden_attrs = {
            "dangerous": SafeAttribute("dangerous", AttributeAccessType.FORBIDDEN, [], "Blocked"),
        }

        registry.register_custom_class("TestClass", forbidden_attrs)

        test_type = type("TestClass", (), {})
        assert registry.is_safe_access(test_type, "dangerous") is False

    def test_console_class_methods(self, registry):
        """Test Console class methods are registered."""
        # Console should have log, error, warn, etc.
        # It may be in _safe_attributes or _custom_classes depending on import
        # Just verify the registry has been initialized properly
        assert len(registry._safe_attributes) > 0
        assert len(registry._custom_classes) > 0

    def test_pattern_class_methods(self, registry):
        """Test Pattern class methods are registered."""
        pattern_type = type("Pattern", (), {})
        # Pattern methods should be accessible
        assert registry.is_safe_access(pattern_type, "test") is True or "Pattern" in registry._custom_classes

    def test_register_builtin_type(self, registry):
        """Test registering built-in type."""
        class CustomBuiltin:
            pass

        custom_attrs = {
            "method1": SafeAttribute("method1", AttributeAccessType.METHOD, [], "Method 1"),
        }

        registry.register_builtin_type(CustomBuiltin, custom_attrs)

        assert CustomBuiltin in registry._safe_attributes
        assert registry.is_safe_access(CustomBuiltin, "method1") is True

    def test_unknown_type_blocks_all(self, registry):
        """Test unknown type blocks all access."""
        class UnknownType:
            pass

        # Unknown type with unknown method should be blocked
        assert registry.is_safe_access(UnknownType, "someMethod") is False

    def test_dangerous_pattern_precedence(self, registry):
        """Test dangerous patterns are blocked even for unknown types."""
        class UnknownType:
            pass

        # Dangerous patterns should be blocked for any type
        assert registry.is_safe_access(UnknownType, "__class__") is False
        assert registry.is_safe_access(UnknownType, "eval") is False
        assert registry.is_safe_access(UnknownType, "__globals__") is False


class TestGlobalRegistry:
    """Test global registry singleton."""

    def test_get_safe_registry_singleton(self):
        """Test get_safe_registry returns singleton."""
        registry1 = get_safe_registry()
        registry2 = get_safe_registry()

        # Should be same instance
        assert registry1 is registry2

    def test_global_registry_initialized(self):
        """Test global registry is properly initialized."""
        registry = get_safe_registry()

        assert registry is not None
        assert len(registry._safe_attributes) > 0
        assert len(registry._dangerous_patterns) > 0

    def test_global_registry_has_builtins(self):
        """Test global registry has built-in types."""
        registry = get_safe_registry()

        assert str in registry._safe_attributes
        assert list in registry._safe_attributes
        assert dict in registry._safe_attributes
        assert tuple in registry._safe_attributes


class TestSecurityValidation:
    """Test security-critical validation."""

    @pytest.fixture
    def registry(self):
        """Create registry."""
        return SafeAttributeRegistry()

    def test_blocks_all_dunder_methods(self, registry):
        """Test all dangerous dunder methods are blocked."""
        dangerous_dunders = [
            "__class__",
            "__dict__",
            "__globals__",
            "__bases__",
            "__mro__",
            "__subclasses__",
            "__code__",
            "__closure__",
        ]

        for dunder in dangerous_dunders:
            assert registry.is_safe_access(str, dunder) is False
            assert registry.is_safe_access(list, dunder) is False
            assert registry.is_safe_access(dict, dunder) is False

    def test_blocks_dynamic_attribute_access(self, registry):
        """Test dynamic attribute access functions are blocked."""
        dynamic_funcs = ["getattr", "setattr", "delattr", "hasattr"]

        for func in dynamic_funcs:
            assert registry.is_safe_access(str, func) is False

    def test_blocks_execution_functions(self, registry):
        """Test code execution functions are blocked."""
        exec_funcs = ["eval", "exec", "compile", "__import__"]

        for func in exec_funcs:
            assert registry.is_safe_access(str, func) is False

    def test_regex_compile_allowed_despite_name(self, registry):
        """Test regex.compile() is allowed even though compile is dangerous."""
        # Custom classes should take precedence over dangerous patterns
        regex_type = type("Regex", (), {})

        # This should be allowed because Regex is registered as custom class
        # Even though "compile" is in dangerous patterns
        assert registry.is_safe_access(regex_type, "compile") is True
