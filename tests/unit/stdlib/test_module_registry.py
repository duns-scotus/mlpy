"""Unit tests for ModuleRegistry.

Tests cover:
- Module discovery and scanning
- Lazy loading behavior
- Caching mechanisms
- Thread safety
- Extension path handling
- Performance characteristics
"""

import pytest
from pathlib import Path
from mlpy.stdlib.module_registry import ModuleRegistry, ModuleMetadata, get_registry


class TestModuleMetadata:
    """Test ModuleMetadata class."""

    def test_metadata_creation(self):
        """Test creating ModuleMetadata instance."""
        metadata = ModuleMetadata("test", Path("test_bridge.py"))

        assert metadata.name == "test"
        assert metadata.file_path == Path("test_bridge.py")
        assert metadata.module_class is None
        assert metadata.instance is None

    def test_metadata_lazy_loading_flag(self):
        """Test that metadata is created without loading."""
        metadata = ModuleMetadata("math", Path("math_bridge.py"))

        # Should not be loaded yet
        assert metadata.instance is None


class TestModuleRegistry:
    """Test module registry discovery and caching."""

    def test_registry_initialization(self):
        """Test ModuleRegistry initialization."""
        registry = ModuleRegistry()

        assert registry._stdlib_dir.name == "stdlib"
        assert len(registry._extension_dirs) == 0
        assert len(registry._discovered) == 0
        assert registry._scanned is False

    def test_stdlib_discovery(self):
        """Test that stdlib modules are discovered."""
        registry = ModuleRegistry()

        # Should discover all stdlib modules
        assert registry.is_available("math")
        assert registry.is_available("json")
        assert registry.is_available("datetime")

    def test_lazy_scanning(self):
        """Test that scanning happens lazily."""
        registry = ModuleRegistry()

        # Should not have scanned yet
        assert not registry._scanned

        # First access triggers scan
        registry.is_available("math")
        assert registry._scanned

    def test_lazy_loading(self):
        """Test that modules are loaded lazily."""
        registry = ModuleRegistry()

        # Check availability (scan only, no import)
        assert registry.is_available("math")
        metadata = registry._discovered["math"]
        assert metadata.instance is None  # Not loaded yet

        # Get module (triggers import)
        math_module = registry.get_module("math")
        assert math_module is not None
        assert metadata.instance is not None  # Now loaded

    def test_module_not_found(self):
        """Test behavior when module doesn't exist."""
        registry = ModuleRegistry()

        assert not registry.is_available("nonexistent_module")
        assert registry.get_module("nonexistent_module") is None

    def test_all_module_names(self):
        """Test getting all available module names."""
        registry = ModuleRegistry()

        names = registry.get_all_module_names()
        assert "math" in names
        assert "json" in names
        assert isinstance(names, set)
        assert len(names) >= 10  # Should have many stdlib modules

    def test_metadata_extraction(self, tmp_path):
        """Test extracting module name from bridge file."""
        registry = ModuleRegistry()

        # Create a test bridge file
        test_content = '''
from mlpy.stdlib.decorators import ml_module

@ml_module(name="testmod", description="Test module")
class TestModule:
    pass

testmod = TestModule()
'''

        test_file = tmp_path / "test_bridge.py"
        test_file.write_text(test_content)

        module_name = registry._extract_module_name(test_file)
        assert module_name == "testmod"

    def test_cache_invalidation(self):
        """Test cache invalidation."""
        registry = ModuleRegistry()

        # Trigger scan
        registry.is_available("math")
        assert registry._scanned
        assert len(registry._discovered) > 0

        # Invalidate cache
        registry.invalidate_cache()
        assert not registry._scanned
        assert len(registry._discovered) == 0

    def test_module_loading_with_actual_stdlib(self):
        """Test loading actual stdlib modules."""
        registry = ModuleRegistry()

        # Load math module
        math_module = registry.get_module("math")
        assert math_module is not None
        assert hasattr(math_module, "sqrt")

        # Load json module
        json_module = registry.get_module("json")
        assert json_module is not None
        assert hasattr(json_module, "stringify")


class TestExtensionPaths:
    """Test extension path functionality."""

    def test_add_extension_paths(self, tmp_path):
        """Test adding extension paths."""
        registry = ModuleRegistry()

        ext_path = tmp_path / "extensions"
        ext_path.mkdir()

        registry.add_extension_paths([str(ext_path)])
        assert ext_path in registry._extension_dirs

    def test_extension_module_discovery(self, tmp_path):
        """Test discovering modules from extension path."""
        # Create extension directory
        ext_dir = tmp_path / "extensions"
        ext_dir.mkdir()

        # Create test extension module
        test_module = ext_dir / "custom_bridge.py"
        test_module.write_text('''
from mlpy.stdlib.decorators import ml_module, ml_function

@ml_module(name="custom", description="Custom module")
class CustomModule:
    @ml_function(description="Custom function")
    def process(self, x: int) -> int:
        return x * 2

custom = CustomModule()
''')

        # Register and discover
        registry = ModuleRegistry()
        registry.add_extension_paths([str(ext_dir)])

        assert registry.is_available("custom")

        # Load and test
        custom_module = registry.get_module("custom")
        assert custom_module is not None
        assert custom_module.process(5) == 10

    def test_stdlib_precedence_over_extensions(self, tmp_path):
        """Test that stdlib modules take precedence over extensions."""
        # Create extension with conflicting name
        ext_dir = tmp_path / "extensions"
        ext_dir.mkdir()

        conflict_module = ext_dir / "math_bridge.py"
        conflict_module.write_text('''
from mlpy.stdlib.decorators import ml_module

@ml_module(name="math", description="Conflicting math module")
class ConflictMath:
    def fake_method(self):
        return "fake"

math = ConflictMath()
''')

        registry = ModuleRegistry()
        registry.add_extension_paths([str(ext_dir)])

        # Stdlib math should take precedence
        math_module = registry.get_module("math")
        assert hasattr(math_module, "sqrt")  # Stdlib math has sqrt
        assert not hasattr(math_module, "fake_method")  # Should not have extension method

    def test_invalid_extension_path_warning(self, tmp_path):
        """Test that invalid paths are handled gracefully."""
        registry = ModuleRegistry()

        # Non-existent path
        registry.add_extension_paths(["/nonexistent/path"])

        # Should not crash, just log warning
        assert len(registry._extension_dirs) == 0

    def test_file_as_extension_path_warning(self, tmp_path):
        """Test that file paths (not directories) are rejected."""
        registry = ModuleRegistry()

        # Create a file
        file_path = tmp_path / "somefile.txt"
        file_path.write_text("test")

        registry.add_extension_paths([str(file_path)])

        # Should not add file as directory
        assert len(registry._extension_dirs) == 0


class TestPerformance:
    """Test performance characteristics."""

    def test_lazy_loading_performance(self):
        """Verify lazy loading doesn't impact startup."""
        import time

        start = time.perf_counter()
        registry = ModuleRegistry()
        init_time = time.perf_counter() - start

        assert init_time < 0.01  # <10ms

        start = time.perf_counter()
        registry.is_available("math")  # First scan
        scan_time = time.perf_counter() - start

        assert scan_time < 0.1  # <100ms for full stdlib

        start = time.perf_counter()
        registry.is_available("json")  # Second query (cached)
        lookup_time = time.perf_counter() - start

        assert lookup_time < 0.001  # <1ms for cached lookup

    def test_performance_logging(self):
        """Test performance logging functionality."""
        registry = ModuleRegistry()
        registry.enable_performance_logging()

        # Load a module
        registry.get_module("math")

        # Check performance report
        report = registry.get_performance_report()
        assert report["total_modules"] > 0
        assert report["loaded_modules"] >= 1
        assert "math" in report["load_times"]
        assert report["avg_load_time"] >= 0


class TestErrorHandling:
    """Test error handling in module discovery."""

    def test_invalid_decorator_syntax(self, tmp_path):
        """Test handling of malformed @ml_module decorator."""
        ext_dir = tmp_path / "ext"
        ext_dir.mkdir()

        # Module with invalid decorator
        (ext_dir / "broken_bridge.py").write_text('''
@ml_module()  # Missing required 'name' parameter
class Broken:
    pass
''')

        registry = ModuleRegistry()
        registry.add_extension_paths([str(ext_dir)])

        # Should not crash, just skip the module
        modules = registry.get_all_module_names()
        assert "broken" not in modules

    def test_missing_module_instance(self, tmp_path):
        """Test handling when module instance variable is missing."""
        ext_dir = tmp_path / "ext"
        ext_dir.mkdir()

        # Module class but no instance
        (ext_dir / "no_instance_bridge.py").write_text('''
from mlpy.stdlib.decorators import ml_module

@ml_module(name="noinst", description="No instance")
class NoInstance:
    pass

# Missing: noinst = NoInstance()
''')

        registry = ModuleRegistry()
        registry.add_extension_paths([str(ext_dir)])

        # Should discover but fail to load
        assert registry.is_available("noinst")
        module = registry.get_module("noinst")
        assert module is None

    def test_malformed_python_file(self, tmp_path):
        """Test handling of malformed Python files."""
        ext_dir = tmp_path / "ext"
        ext_dir.mkdir()

        # File with syntax errors
        (ext_dir / "syntax_error_bridge.py").write_text('''
from mlpy.stdlib.decorators import ml_module

@ml_module(name="broken"
class Broken:  # Missing closing parenthesis
    pass
''')

        registry = ModuleRegistry()
        registry.add_extension_paths([str(ext_dir)])

        # Should not crash, just skip the module
        modules = registry.get_all_module_names()
        assert "broken" not in modules


class TestGlobalRegistry:
    """Test global registry singleton."""

    def test_get_registry_singleton(self):
        """Test that get_registry returns singleton."""
        registry1 = get_registry()
        registry2 = get_registry()

        assert registry1 is registry2

    def test_get_registry_thread_safe(self):
        """Test thread-safe singleton creation."""
        import threading

        registries = []

        def get_and_store():
            registries.append(get_registry())

        threads = [threading.Thread(target=get_and_store) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # All threads should get the same registry
        assert all(r is registries[0] for r in registries)


class TestNamespaceCollisions:
    """Test handling of module name collisions."""

    def test_first_wins_precedence(self, tmp_path):
        """Test that first extension path wins in collisions."""
        ext1 = tmp_path / "ext1"
        ext2 = tmp_path / "ext2"
        ext1.mkdir()
        ext2.mkdir()

        # Same module name in both paths
        (ext1 / "shared_bridge.py").write_text('''
from mlpy.stdlib.decorators import ml_module, ml_function

@ml_module(name="shared", description="From ext1")
class Shared:
    @ml_function(description="Version")
    def version(self):
        return "ext1"

shared = Shared()
''')

        (ext2 / "shared_bridge.py").write_text('''
from mlpy.stdlib.decorators import ml_module, ml_function

@ml_module(name="shared", description="From ext2")
class Shared:
    @ml_function(description="Version")
    def version(self):
        return "ext2"

shared = Shared()
''')

        registry = ModuleRegistry()
        registry.add_extension_paths([str(ext1), str(ext2)])

        module = registry.get_module("shared")
        assert module is not None
        assert module.version() == "ext1"  # First path wins
