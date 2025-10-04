"""Unit tests for ML stdlib decorator capability integration."""

import pytest
from mlpy.stdlib.decorators import (
    ml_module,
    ml_function,
    ml_class,
    enable_capability_validation,
    disable_capability_validation,
    is_capability_validation_enabled,
    register_module_with_safe_attributes,
    get_module_metadata,
    _MODULE_REGISTRY,
)


class TestCapabilityValidation:
    """Test capability validation in @ml_function decorator."""

    def setup_method(self):
        """Reset capability validation state before each test."""
        disable_capability_validation()
        _MODULE_REGISTRY.clear()

    def teardown_method(self):
        """Clean up after each test."""
        disable_capability_validation()
        _MODULE_REGISTRY.clear()

    def test_capability_validation_disabled_by_default(self):
        """Test that capability validation is disabled by default."""
        assert is_capability_validation_enabled() is False

    def test_enable_capability_validation(self):
        """Test enabling capability validation."""
        enable_capability_validation()
        assert is_capability_validation_enabled() is True

    def test_disable_capability_validation(self):
        """Test disabling capability validation."""
        enable_capability_validation()
        disable_capability_validation()
        assert is_capability_validation_enabled() is False

    def test_function_executes_without_validation_when_disabled(self):
        """Test that functions execute normally when validation is disabled."""

        @ml_function(description="Test function", capabilities=["test.read"])
        def test_func(x):
            return x * 2

        # Should work without capability context
        result = test_func(5)
        assert result == 10

    def test_function_executes_without_context_when_enabled_no_capabilities(self):
        """Test function with no capabilities works even when validation enabled."""
        enable_capability_validation()

        @ml_function(description="Test function")  # No capabilities
        def test_func(x):
            return x * 2

        # Should work without capability context
        result = test_func(5)
        assert result == 10

    def test_function_executes_with_valid_capability_context(self):
        """Test function execution with valid capability context."""
        enable_capability_validation()

        @ml_function(description="Test function", capabilities=["test.read"])
        def test_func(x):
            return x * 2

        # Create mock capability context
        class MockCapabilityContext:
            def has_capability(self, cap_type):
                return cap_type == "test.read"

            def pop(self, key, default=None):
                return default

        context = MockCapabilityContext()

        # Should work with valid context
        result = test_func(5, _capability_context=context)
        assert result == 10

    def test_function_raises_permission_error_without_capability(self):
        """Test function raises PermissionError when capability missing."""
        enable_capability_validation()

        @ml_function(description="Test function", capabilities=["test.write"])
        def test_func(x):
            return x * 2

        # Create mock capability context without required capability
        class MockCapabilityContext:
            def has_capability(self, cap_type):
                return False  # No capabilities

        context = MockCapabilityContext()

        # Should raise PermissionError
        with pytest.raises(PermissionError) as exc_info:
            test_func(5, _capability_context=context)

        assert "Missing required capability 'test.write'" in str(exc_info.value)
        assert "test_func()" in str(exc_info.value)

    def test_function_validates_multiple_capabilities(self):
        """Test function with multiple required capabilities."""
        enable_capability_validation()

        @ml_function(
            description="Test function",
            capabilities=["test.read", "test.write"],
        )
        def test_func(x):
            return x * 2

        # Create mock context with only one capability
        class MockCapabilityContext:
            def has_capability(self, cap_type):
                return cap_type == "test.read"  # Missing test.write

        context = MockCapabilityContext()

        # Should raise PermissionError for missing capability
        with pytest.raises(PermissionError) as exc_info:
            test_func(5, _capability_context=context)

        assert "Missing required capability 'test.write'" in str(exc_info.value)

    def test_function_with_all_required_capabilities(self):
        """Test function execution with all required capabilities."""
        enable_capability_validation()

        @ml_function(
            description="Test function",
            capabilities=["test.read", "test.write"],
        )
        def test_func(x):
            return x * 2

        # Create mock context with all capabilities
        class MockCapabilityContext:
            def has_capability(self, cap_type):
                return cap_type in ["test.read", "test.write"]

        context = MockCapabilityContext()

        # Should work with all capabilities
        result = test_func(5, _capability_context=context)
        assert result == 10

    def test_capability_context_removed_from_kwargs(self):
        """Test that _capability_context is removed from kwargs before function call."""
        enable_capability_validation()

        @ml_function(description="Test function", capabilities=["test.read"])
        def test_func(**kwargs):
            # Should not receive _capability_context in kwargs
            assert "_capability_context" not in kwargs
            return kwargs

        class MockCapabilityContext:
            def has_capability(self, cap_type):
                return True

        context = MockCapabilityContext()

        result = test_func(a=1, b=2, _capability_context=context)
        assert result == {"a": 1, "b": 2}


class TestSafeAttributeRegistryIntegration:
    """Test integration with SafeAttributeRegistry."""

    def setup_method(self):
        """Clean up before each test."""
        _MODULE_REGISTRY.clear()

    def teardown_method(self):
        """Clean up after each test."""
        _MODULE_REGISTRY.clear()

    def test_register_module_with_functions(self):
        """Test registering a module with functions to SafeAttributeRegistry."""

        @ml_module(name="testmod", description="Test module")
        class TestModule:
            @ml_function(description="Test function", capabilities=["test.read"])
            def test_func(self):
                return "test"

        # Create mock registry
        class MockRegistry:
            def __init__(self):
                self.custom_classes = {}

            def register_custom_class(self, class_name, attributes):
                self.custom_classes[class_name] = attributes

        registry = MockRegistry()

        # Register module
        register_module_with_safe_attributes("testmod", registry)

        # Check module was registered
        assert "TestModule" in registry.custom_classes
        module_attrs = registry.custom_classes["TestModule"]

        # Check function was registered
        assert "test_func" in module_attrs

        # Check function metadata
        func_attr = module_attrs["test_func"]
        assert func_attr.name == "test_func"
        assert func_attr.description == "Test function"
        assert func_attr.capabilities_required == ["test.read"]

    def test_register_module_with_nested_classes(self):
        """Test registering a module with nested classes."""

        @ml_module(name="testmod", description="Test module")
        class TestModule:
            @ml_class(description="Test class")
            class TestClass:
                @ml_function(description="Test method")
                def test_method(self):
                    return "test"

        # Create mock registry
        class MockRegistry:
            def __init__(self):
                self.custom_classes = {}

            def register_custom_class(self, class_name, attributes):
                self.custom_classes[class_name] = attributes

        registry = MockRegistry()

        # Register module
        register_module_with_safe_attributes("testmod", registry)

        # Check nested class was registered
        assert "TestClass" in registry.custom_classes
        class_attrs = registry.custom_classes["TestClass"]

        # Check method was registered
        assert "test_method" in class_attrs
        method_attr = class_attrs["test_method"]
        assert method_attr.description == "Test method"

    def test_register_module_not_found_raises_error(self):
        """Test that registering non-existent module raises ValueError."""

        class MockRegistry:
            pass

        registry = MockRegistry()

        with pytest.raises(ValueError) as exc_info:
            register_module_with_safe_attributes("nonexistent", registry)

        assert "Module 'nonexistent' not found" in str(exc_info.value)

    def test_register_module_with_mixed_content(self):
        """Test registering module with both functions and classes."""

        @ml_module(name="mixed", description="Mixed module")
        class MixedModule:
            @ml_function(
                description="Top function", capabilities=["mixed.read"]
            )
            def top_func(self):
                return "top"

            @ml_class(description="Inner class")
            class InnerClass:
                @ml_function(description="Inner method")
                def inner_method(self):
                    return "inner"

        class MockRegistry:
            def __init__(self):
                self.custom_classes = {}

            def register_custom_class(self, class_name, attributes):
                self.custom_classes[class_name] = attributes

        registry = MockRegistry()
        register_module_with_safe_attributes("mixed", registry)

        # Check module has top-level function
        assert "MixedModule" in registry.custom_classes
        assert "top_func" in registry.custom_classes["MixedModule"]

        # Check inner class registered separately
        assert "InnerClass" in registry.custom_classes
        assert "inner_method" in registry.custom_classes["InnerClass"]


class TestIntegrationScenario:
    """Integration tests combining all capability features."""

    def setup_method(self):
        """Reset state before each test."""
        disable_capability_validation()
        _MODULE_REGISTRY.clear()

    def teardown_method(self):
        """Clean up after each test."""
        disable_capability_validation()
        _MODULE_REGISTRY.clear()

    def test_complete_capability_workflow(self):
        """Test complete workflow: module creation, validation, and registry."""

        # Create module with capabilities
        @ml_module(
            name="secure",
            description="Secure module",
            capabilities=["secure.read", "secure.write"],
        )
        class SecureModule:
            @ml_function(
                description="Read data", capabilities=["secure.read"]
            )
            def read_data(self, path):
                return f"reading {path}"

            @ml_function(
                description="Write data", capabilities=["secure.write"]
            )
            def write_data(self, path, data):
                return f"writing to {path}"

        # Test without validation (default)
        instance = SecureModule()
        assert instance.read_data("/tmp/file") == "reading /tmp/file"
        assert instance.write_data("/tmp/file", "data") == "writing to /tmp/file"

        # Enable validation
        enable_capability_validation()

        # Create capability context
        class MockCapabilityContext:
            def __init__(self, capabilities):
                self.capabilities = set(capabilities)

            def has_capability(self, cap_type):
                return cap_type in self.capabilities

        # Test with valid capabilities
        read_context = MockCapabilityContext(["secure.read"])
        result = instance.read_data("/tmp/file", _capability_context=read_context)
        assert result == "reading /tmp/file"

        # Test with missing capability
        with pytest.raises(PermissionError):
            instance.write_data("/tmp/file", "data", _capability_context=read_context)

        # Test with all capabilities
        full_context = MockCapabilityContext(["secure.read", "secure.write"])
        result = instance.write_data("/tmp/file", "data", _capability_context=full_context)
        assert result == "writing to /tmp/file"

        # Register with SafeAttributeRegistry
        class MockRegistry:
            def __init__(self):
                self.custom_classes = {}

            def register_custom_class(self, class_name, attributes):
                self.custom_classes[class_name] = attributes

        registry = MockRegistry()
        register_module_with_safe_attributes("secure", registry)

        # Verify registration
        assert "SecureModule" in registry.custom_classes
        assert "read_data" in registry.custom_classes["SecureModule"]
        assert "write_data" in registry.custom_classes["SecureModule"]

        # Verify capability metadata preserved
        read_attr = registry.custom_classes["SecureModule"]["read_data"]
        assert read_attr.capabilities_required == ["secure.read"]

        write_attr = registry.custom_classes["SecureModule"]["write_data"]
        assert write_attr.capabilities_required == ["secure.write"]
