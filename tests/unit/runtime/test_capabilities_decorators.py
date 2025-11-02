"""
Comprehensive test suite for capabilities/decorators.py

Tests capability-based function protection including:
- @requires_capability decorator
- @requires_capabilities decorator for multiple capabilities
- @with_capability decorator for temporary capabilities
- @capability_safe decorator for capability restrictions
- capability_context_manager for reusable contexts
- Shorthand decorators (requires_file_access, requires_network_access, requires_math_capability)
- Function introspection utilities
"""

import pytest

from mlpy.runtime.capabilities.context import CapabilityContext
from mlpy.runtime.capabilities.decorators import (
    capability_context_manager,
    capability_safe,
    get_function_capabilities,
    is_capability_protected,
    requires_capabilities,
    requires_capability,
    requires_file_access,
    requires_math_capability,
    requires_network_access,
    with_capability,
)
from mlpy.runtime.capabilities.exceptions import CapabilityNotFoundError
from mlpy.runtime.capabilities.manager import get_capability_manager
from mlpy.runtime.capabilities.tokens import CapabilityConstraint, CapabilityToken


class TestRequiresCapabilityDecorator:
    """Test @requires_capability decorator."""

    def setup_method(self):
        """Setup capability manager for each test."""
        self.manager = get_capability_manager()
        self.manager.clear_cache()

    def teardown_method(self):
        """Cleanup after each test."""
        self.manager.clear_cache()

    def test_requires_capability_basic(self):
        """Test basic capability requirement."""
        token = CapabilityToken(capability_type="file")

        @requires_capability("file")
        def read_file():
            return "file content"

        with self.manager.capability_context("test", [token]):
            result = read_file()
            assert result == "file content"

    def test_requires_capability_missing_raises_error(self):
        """Test missing capability raises error."""

        @requires_capability("file")
        def read_file():
            return "file content"

        # No context - should raise
        with pytest.raises(CapabilityNotFoundError):
            read_file()

    def test_requires_capability_with_resource_pattern(self):
        """Test capability with resource pattern."""
        constraint = CapabilityConstraint(resource_patterns=["*.txt"])
        token = CapabilityToken(capability_type="file", constraints=constraint)

        @requires_capability("file", "test.txt", "read", auto_use=False)
        def read_file():
            return "content"

        with self.manager.capability_context("test", [token]):
            result = read_file()
            assert result == "content"

    def test_requires_capability_with_auto_use(self):
        """Test capability with auto_use."""
        constraint = CapabilityConstraint(
            resource_patterns=["*.txt"], allowed_operations={"read"}
        )
        token = CapabilityToken(capability_type="file", constraints=constraint)

        @requires_capability("file", "test.txt", "read", auto_use=True)
        def read_file():
            return "content"

        with self.manager.capability_context("test", [token]):
            result = read_file()
            assert result == "content"
            assert token.usage_count > 0

    def test_requires_capability_metadata(self):
        """Test decorator adds metadata to function."""

        @requires_capability("file", "*.txt", "read")
        def read_file():
            return "content"

        assert hasattr(read_file, "_mlpy_capability_required")
        metadata = read_file._mlpy_capability_required
        assert metadata["capability_type"] == "file"
        assert metadata["resource_pattern"] == "*.txt"
        assert metadata["operation"] == "read"

    def test_requires_capability_preserves_function_name(self):
        """Test decorator preserves function name."""

        @requires_capability("file")
        def my_function():
            return "result"

        assert my_function.__name__ == "my_function"


class TestRequiresCapabilitiesDecorator:
    """Test @requires_capabilities decorator."""

    def setup_method(self):
        """Setup capability manager for each test."""
        self.manager = get_capability_manager()
        self.manager.clear_cache()

    def teardown_method(self):
        """Cleanup after each test."""
        self.manager.clear_cache()

    def test_requires_multiple_capabilities(self):
        """Test requiring multiple capabilities."""
        file_token = CapabilityToken(capability_type="file")
        network_token = CapabilityToken(capability_type="network")

        @requires_capabilities(("file",), ("network",))
        def process_data():
            return "processed"

        with self.manager.capability_context("test", [file_token, network_token]):
            result = process_data()
            assert result == "processed"

    def test_requires_capabilities_missing_one(self):
        """Test missing one of multiple capabilities."""
        file_token = CapabilityToken(capability_type="file")

        @requires_capabilities(("file",), ("network",))
        def process_data():
            return "processed"

        with self.manager.capability_context("test", [file_token]):
            with pytest.raises(CapabilityNotFoundError):
                process_data()

    def test_requires_capabilities_metadata(self):
        """Test decorator adds metadata."""

        @requires_capabilities(("file", "*.txt", "read"), ("network", "api.com", "http"))
        def process_data():
            return "result"

        assert hasattr(process_data, "_mlpy_capabilities_required")
        specs = process_data._mlpy_capabilities_required
        assert len(specs) == 2

    def test_requires_capabilities_with_auto_use(self):
        """Test decorator automatically uses capabilities with full specs."""
        from mlpy.runtime.capabilities.tokens import CapabilityConstraint

        file_constraint = CapabilityConstraint(
            resource_patterns=["*.txt"], allowed_operations={"read"}
        )
        file_token = CapabilityToken(capability_type="file", constraints=file_constraint)

        network_constraint = CapabilityConstraint(
            resource_patterns=["api.com"], allowed_operations={"http"}
        )
        network_token = CapabilityToken(
            capability_type="network", constraints=network_constraint
        )

        @requires_capabilities(("file", "test.txt", "read"), ("network", "api.com", "http"))
        def process_data():
            return "processed"

        with self.manager.capability_context("test", [file_token, network_token]):
            result = process_data()
            assert result == "processed"
            # Verify both capabilities were used
            assert file_token.usage_count > 0
            assert network_token.usage_count > 0


class TestWithCapabilityDecorator:
    """Test @with_capability decorator."""

    def setup_method(self):
        """Setup capability manager for each test."""
        self.manager = get_capability_manager()
        self.manager.clear_cache()

    def teardown_method(self):
        """Cleanup after each test."""
        self.manager.clear_cache()

    def test_with_capability_provides_temporary(self):
        """Test decorator provides temporary capability."""

        @with_capability("file", ["temp/*.txt"], {"read", "write"})
        def process_temp_files():
            # Should have file capability within function
            return get_capability_manager().has_capability("file")

        result = process_temp_files()
        assert result is True

    def test_with_capability_metadata(self):
        """Test decorator adds metadata."""

        @with_capability("file", ["data/*.json"], {"read"})
        def load_data():
            return "data"

        assert hasattr(load_data, "_mlpy_capability_provided")
        metadata = load_data._mlpy_capability_provided
        assert metadata["capability_type"] == "file"


class TestCapabilitySafeDecorator:
    """Test @capability_safe decorator."""

    def test_capability_safe_basic(self):
        """Test basic capability_safe decorator."""

        @capability_safe(["file", "math"], strict=True)
        def safe_processor():
            return "safe"

        result = safe_processor()
        assert result == "safe"

    def test_capability_safe_metadata(self):
        """Test decorator adds metadata."""

        @capability_safe(["file", "network"], strict=False)
        def flexible_processor():
            return "flexible"

        assert hasattr(flexible_processor, "_mlpy_capability_restrictions")
        metadata = flexible_processor._mlpy_capability_restrictions
        assert metadata["allowed_capabilities"] == ["file", "network"]
        assert metadata["strict"] is False


class TestCapabilityContextManager:
    """Test capability_context_manager function."""

    def setup_method(self):
        """Setup capability manager for each test."""
        self.manager = get_capability_manager()
        self.manager.clear_cache()

    def teardown_method(self):
        """Cleanup after each test."""
        self.manager.clear_cache()

    def test_capability_context_manager_basic(self):
        """Test basic context manager creation."""
        file_access = capability_context_manager("file", ["data/*.json"], {"read"})

        with file_access():
            assert self.manager.has_capability("file")

    def test_capability_context_manager_yields_context(self):
        """Test context manager yields context object."""
        file_access = capability_context_manager("file", ["*.txt"], {"read"})

        with file_access() as ctx:
            assert isinstance(ctx, CapabilityContext)


class TestShorthandDecorators:
    """Test shorthand convenience decorators."""

    def setup_method(self):
        """Setup capability manager for each test."""
        self.manager = get_capability_manager()
        self.manager.clear_cache()

    def teardown_method(self):
        """Cleanup after each test."""
        self.manager.clear_cache()

    def test_requires_file_access_string_pattern(self):
        """Test requires_file_access with string pattern."""
        constraint = CapabilityConstraint(resource_patterns=["*.txt"])
        token = CapabilityToken(capability_type="file", constraints=constraint)

        @requires_file_access("*.txt", {"read"})
        def read_text_files():
            return "content"

        with self.manager.capability_context("test", [token]):
            result = read_text_files()
            assert result == "content"

    def test_requires_file_access_list_patterns(self):
        """Test requires_file_access with list of patterns."""
        constraint = CapabilityConstraint(resource_patterns=["*.txt", "*.md"])
        token = CapabilityToken(capability_type="file", constraints=constraint)

        @requires_file_access(["*.txt", "*.md"], {"read"})
        def read_docs():
            return "docs"

        with self.manager.capability_context("test", [token]):
            result = read_docs()
            assert result == "docs"

    def test_requires_network_access_string_host(self):
        """Test requires_network_access with string host."""
        constraint = CapabilityConstraint(resource_patterns=["api.example.com"])
        token = CapabilityToken(capability_type="network", constraints=constraint)

        @requires_network_access("api.example.com", {"http"})
        def call_api():
            return "response"

        with self.manager.capability_context("test", [token]):
            result = call_api()
            assert result == "response"

    def test_requires_math_capability(self):
        """Test requires_math_capability decorator."""
        token = CapabilityToken(capability_type="math")

        @requires_math_capability()
        def calculate():
            return 42

        with self.manager.capability_context("test", [token]):
            result = calculate()
            assert result == 42


class TestFunctionIntrospection:
    """Test function introspection utilities."""

    def test_get_function_capabilities_single(self):
        """Test getting single capability requirement."""

        @requires_capability("file", "*.txt", "read")
        def read_file():
            pass

        caps = get_function_capabilities(read_file)
        assert "required" in caps
        assert caps["required"]["capability_type"] == "file"

    def test_get_function_capabilities_multiple(self):
        """Test getting multiple capability requirements."""

        @requires_capabilities(("file", "*.txt", "read"), ("network", "api.com", "http"))
        def process_remote():
            pass

        caps = get_function_capabilities(process_remote)
        assert "required_multiple" in caps
        assert len(caps["required_multiple"]) == 2

    def test_get_function_capabilities_provided(self):
        """Test getting provided capabilities."""

        @with_capability("file", ["temp/*.txt"], {"read"})
        def temp_processor():
            pass

        caps = get_function_capabilities(temp_processor)
        assert "provided" in caps
        assert caps["provided"]["capability_type"] == "file"

    def test_get_function_capabilities_restrictions(self):
        """Test getting capability restrictions."""

        @capability_safe(["file", "math"], strict=True)
        def safe_func():
            pass

        caps = get_function_capabilities(safe_func)
        assert "restrictions" in caps
        assert "file" in caps["restrictions"]["allowed_capabilities"]

    def test_get_function_capabilities_empty(self):
        """Test getting capabilities from undecorated function."""

        def plain_function():
            pass

        caps = get_function_capabilities(plain_function)
        assert caps == {}

    def test_is_capability_protected_true(self):
        """Test is_capability_protected returns True for decorated functions."""

        @requires_capability("file")
        def protected_func():
            pass

        assert is_capability_protected(protected_func) is True

    def test_is_capability_protected_false(self):
        """Test is_capability_protected returns False for plain functions."""

        def plain_func():
            pass

        assert is_capability_protected(plain_func) is False
