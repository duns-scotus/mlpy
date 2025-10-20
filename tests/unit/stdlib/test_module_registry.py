"""Unit tests for ModuleRegistry.

Tests cover:
- Module discovery and scanning
- Lazy loading behavior
- Caching mechanisms
- Thread safety
- Extension path handling
- Performance characteristics
- ML module discovery (nested directories)
- Unified module registry (Python bridges + ML modules)
- Precedence rules between module types
"""

import pytest
from pathlib import Path
from mlpy.stdlib.module_registry import ModuleRegistry, ModuleMetadata, ModuleType, get_registry


class TestModuleMetadata:
    """Test ModuleMetadata class."""

    def test_metadata_creation_python_bridge(self):
        """Test creating ModuleMetadata instance for Python bridge."""
        metadata = ModuleMetadata(
            name="test",
            module_type=ModuleType.PYTHON_BRIDGE,
            file_path=Path("test_bridge.py")
        )

        assert metadata.name == "test"
        assert metadata.module_type == ModuleType.PYTHON_BRIDGE
        assert metadata.file_path == Path("test_bridge.py")
        assert metadata.module_class is None
        assert metadata.instance is None

    def test_metadata_creation_ml_source(self):
        """Test creating ModuleMetadata instance for ML module."""
        metadata = ModuleMetadata(
            name="utils",
            module_type=ModuleType.ML_SOURCE,
            file_path=Path("utils.ml"),
            transpiled_path=Path("utils.py"),
            source_mtime=123.456
        )

        assert metadata.name == "utils"
        assert metadata.module_type == ModuleType.ML_SOURCE
        assert metadata.file_path == Path("utils.ml")
        assert metadata.transpiled_path == Path("utils.py")
        assert metadata.source_mtime == 123.456

    def test_metadata_lazy_loading_flag(self):
        """Test that metadata is created without loading."""
        metadata = ModuleMetadata(
            name="math",
            module_type=ModuleType.PYTHON_BRIDGE,
            file_path=Path("math_bridge.py")
        )

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


class TestMLModuleDiscovery:
    """Test ML module discovery and nested directory support."""

    def test_add_ml_module_paths(self, tmp_path):
        """Test adding ML module paths."""
        registry = ModuleRegistry()

        ml_path = tmp_path / "ml_modules"
        ml_path.mkdir()

        registry.add_ml_module_paths([str(ml_path)])
        assert ml_path in registry._ml_module_dirs

    def test_simple_ml_module_discovery(self, tmp_path):
        """Test discovering a simple ML module."""
        ml_dir = tmp_path / "ml_modules"
        ml_dir.mkdir()

        # Create simple ML module
        (ml_dir / "utils.ml").write_text('''
function add(a, b) {
    return a + b;
}
''')

        registry = ModuleRegistry()
        registry.add_ml_module_paths([str(ml_dir)])

        # Should discover the ML module
        assert registry.is_available("utils")

        # Check metadata
        metadata = registry._discovered["utils"]
        assert metadata.module_type == ModuleType.ML_SOURCE
        assert metadata.name == "utils"
        assert metadata.file_path.name == "utils.ml"

    def test_nested_directory_ml_modules(self, tmp_path):
        """Test discovering ML modules in nested directories."""
        ml_dir = tmp_path / "ml_modules"
        ml_dir.mkdir()

        # Create nested structure: ml_modules/algorithms/sorting.ml
        algorithms_dir = ml_dir / "algorithms"
        algorithms_dir.mkdir()
        (algorithms_dir / "sorting.ml").write_text('''
function quicksort(arr) {
    return arr;
}
''')

        # Create deeper nesting: ml_modules/data/transforms/normalize.ml
        data_dir = ml_dir / "data"
        data_dir.mkdir()
        transforms_dir = data_dir / "transforms"
        transforms_dir.mkdir()
        (transforms_dir / "normalize.ml").write_text('''
function normalize(x) {
    return x / 100;
}
''')

        registry = ModuleRegistry()
        registry.add_ml_module_paths([str(ml_dir)])

        # Check nested module names
        assert registry.is_available("algorithms.sorting")
        assert registry.is_available("data.transforms.normalize")

        # Verify metadata
        sorting_meta = registry._discovered["algorithms.sorting"]
        assert sorting_meta.module_type == ModuleType.ML_SOURCE
        assert sorting_meta.name == "algorithms.sorting"

        normalize_meta = registry._discovered["data.transforms.normalize"]
        assert normalize_meta.module_type == ModuleType.ML_SOURCE
        assert normalize_meta.name == "data.transforms.normalize"

    def test_ml_modules_with_multiple_files(self, tmp_path):
        """Test discovering multiple ML modules in same directory."""
        ml_dir = tmp_path / "ml_modules"
        ml_dir.mkdir()

        # Create multiple ML files
        (ml_dir / "utils.ml").write_text('function util() { return 1; }')
        (ml_dir / "helpers.ml").write_text('function help() { return 2; }')
        (ml_dir / "validators.ml").write_text('function validate() { return 3; }')

        registry = ModuleRegistry()
        registry.add_ml_module_paths([str(ml_dir)])

        # All should be discovered
        assert registry.is_available("utils")
        assert registry.is_available("helpers")
        assert registry.is_available("validators")

        # Check count
        all_modules = registry.get_all_modules(include_type=ModuleType.ML_SOURCE)
        ml_module_names = {name for name in all_modules.keys()
                          if name in ["utils", "helpers", "validators"]}
        assert len(ml_module_names) == 3

    def test_ml_module_skip_hidden_directories(self, tmp_path):
        """Test that hidden directories are skipped."""
        ml_dir = tmp_path / "ml_modules"
        ml_dir.mkdir()

        # Create hidden directory
        hidden_dir = ml_dir / ".hidden"
        hidden_dir.mkdir()
        (hidden_dir / "secret.ml").write_text('function secret() { return 1; }')

        # Create underscore directory
        private_dir = ml_dir / "_private"
        private_dir.mkdir()
        (private_dir / "internal.ml").write_text('function internal() { return 2; }')

        registry = ModuleRegistry()
        registry.add_ml_module_paths([str(ml_dir)])

        # Hidden/private modules should NOT be discovered
        assert not registry.is_available(".hidden.secret")
        assert not registry.is_available("_private.internal")

    def test_invalid_ml_module_path(self, tmp_path):
        """Test handling of invalid ML module paths."""
        registry = ModuleRegistry()

        # Non-existent path
        registry.add_ml_module_paths(["/nonexistent/ml/path"])
        assert len(registry._ml_module_dirs) == 0

        # File instead of directory
        file_path = tmp_path / "notadir.txt"
        file_path.write_text("test")
        registry.add_ml_module_paths([str(file_path)])
        assert len(registry._ml_module_dirs) == 0


class TestModulePrecedence:
    """Test precedence rules between Python bridges and ML modules."""

    def test_python_bridge_wins_over_ml_module(self, tmp_path, caplog):
        """Test that Python bridge takes precedence over ML module with same name."""
        # Create Python bridge
        ext_dir = tmp_path / "extensions"
        ext_dir.mkdir()
        (ext_dir / "utils_bridge.py").write_text('''
from mlpy.stdlib.decorators import ml_module, ml_function

@ml_module(name="utils", description="Python bridge utils")
class Utils:
    @ml_function(description="Process")
    def process(self, x: int) -> int:
        return x * 2

utils = Utils()
''')

        # Create ML module with same name
        ml_dir = tmp_path / "ml_modules"
        ml_dir.mkdir()
        (ml_dir / "utils.ml").write_text('''
function process(x) {
    return x * 3;
}
''')

        registry = ModuleRegistry()
        registry.add_extension_paths([str(ext_dir)])
        registry.add_ml_module_paths([str(ml_dir)])

        # Python bridge should win
        assert registry.is_available("utils")
        metadata = registry._discovered["utils"]
        assert metadata.module_type == ModuleType.PYTHON_BRIDGE

        # Should log warning about collision
        assert "Module name collision" in caplog.text
        assert "utils" in caplog.text

        # Load and verify it's the Python bridge
        utils = registry.get_module("utils")
        assert utils is not None
        assert utils.process(5) == 10  # Python bridge behavior (x * 2)

    def test_first_wins_among_same_type(self, tmp_path):
        """Test first-wins precedence among same module type."""
        ml_dir1 = tmp_path / "ml1"
        ml_dir2 = tmp_path / "ml2"
        ml_dir1.mkdir()
        ml_dir2.mkdir()

        # Same module name in both directories
        (ml_dir1 / "shared.ml").write_text('''
function version() { return 1; }
''')
        (ml_dir2 / "shared.ml").write_text('''
function version() { return 2; }
''')

        registry = ModuleRegistry()
        registry.add_ml_module_paths([str(ml_dir1), str(ml_dir2)])

        # First path should win
        assert registry.is_available("shared")
        metadata = registry._discovered["shared"]
        assert str(ml_dir1) in str(metadata.file_path)

    def test_no_collision_with_different_names(self, tmp_path):
        """Test that different names don't collide."""
        ext_dir = tmp_path / "extensions"
        ext_dir.mkdir()
        (ext_dir / "bridge1_bridge.py").write_text('''
from mlpy.stdlib.decorators import ml_module

@ml_module(name="bridge1", description="Bridge 1")
class Bridge1:
    pass

bridge1 = Bridge1()
''')

        ml_dir = tmp_path / "ml_modules"
        ml_dir.mkdir()
        (ml_dir / "ml1.ml").write_text('function test() { return 1; }')

        registry = ModuleRegistry()
        registry.add_extension_paths([str(ext_dir)])
        registry.add_ml_module_paths([str(ml_dir)])

        # Both should be available
        assert registry.is_available("bridge1")
        assert registry.is_available("ml1")

        # Check types
        assert registry._discovered["bridge1"].module_type == ModuleType.PYTHON_BRIDGE
        assert registry._discovered["ml1"].module_type == ModuleType.ML_SOURCE


class TestUnifiedModuleLoading:
    """Test lazy loading for both Python bridges and ML modules."""

    def test_ml_module_lazy_loading(self, tmp_path):
        """Test that ML modules are loaded lazily."""
        ml_dir = tmp_path / "ml_modules"
        ml_dir.mkdir()
        (ml_dir / "lazy.ml").write_text('''
function test() {
    return 42;
}
''')

        registry = ModuleRegistry()
        registry.add_ml_module_paths([str(ml_dir)])

        # Check availability (scan only)
        assert registry.is_available("lazy")
        metadata = registry._discovered["lazy"]
        assert metadata.instance is None  # Not loaded yet

        # Get module (triggers transpilation and import)
        lazy_module = registry.get_module("lazy")
        assert lazy_module is not None
        assert metadata.instance is not None  # Now loaded

    def test_ml_module_needs_recompilation(self, tmp_path):
        """Test needs_recompilation logic for ML modules."""
        import time

        ml_dir = tmp_path / "ml_modules"
        ml_dir.mkdir()
        ml_file = ml_dir / "test.ml"
        ml_file.write_text('function test() { return 1; }')

        registry = ModuleRegistry()
        registry.add_ml_module_paths([str(ml_dir)])

        # Trigger scan to discover the module
        assert registry.is_available("test")

        # First load - should transpile
        metadata = registry._discovered["test"]
        assert metadata.needs_recompilation()  # No transpiled file yet

        # Load it
        registry.get_module("test")
        assert not metadata.needs_recompilation()  # Transpiled file exists

        # Modify source file
        time.sleep(0.01)  # Ensure timestamp difference
        ml_file.write_text('function test() { return 2; }')
        metadata.source_mtime = ml_file.stat().st_mtime

        # Should need recompilation
        assert metadata.needs_recompilation()

    def test_get_all_modules_filtered_by_type(self, tmp_path):
        """Test filtering modules by type."""
        # Create Python bridge
        ext_dir = tmp_path / "ext"
        ext_dir.mkdir()
        (ext_dir / "bridge_bridge.py").write_text('''
from mlpy.stdlib.decorators import ml_module

@ml_module(name="bridge", description="Bridge")
class Bridge:
    pass

bridge = Bridge()
''')

        # Create ML module
        ml_dir = tmp_path / "ml"
        ml_dir.mkdir()
        (ml_dir / "mlmod.ml").write_text('function test() { return 1; }')

        registry = ModuleRegistry()
        registry.add_extension_paths([str(ext_dir)])
        registry.add_ml_module_paths([str(ml_dir)])

        # Get all modules
        all_modules = registry.get_all_modules()
        assert "bridge" in all_modules
        assert "mlmod" in all_modules

        # Filter by Python bridges
        python_modules = registry.get_all_modules(include_type=ModuleType.PYTHON_BRIDGE)
        assert "bridge" in python_modules
        assert "mlmod" not in python_modules

        # Filter by ML modules
        ml_modules = registry.get_all_modules(include_type=ModuleType.ML_SOURCE)
        assert "mlmod" in ml_modules
        assert "bridge" not in ml_modules


class TestModuleInfo:
    """Test get_module_info() for both module types."""

    def test_module_info_for_python_bridge(self):
        """Test get_module_info returns correct data for Python bridges."""
        registry = ModuleRegistry()

        # Get info for stdlib math module
        info = registry.get_module_info("math")
        assert info is not None
        assert info['name'] == "math"
        assert info['type'] == "python_bridge"
        assert 'file_path' in info
        assert 'reload_count' in info

    def test_module_info_for_ml_module(self, tmp_path):
        """Test get_module_info returns correct data for ML modules."""
        ml_dir = tmp_path / "ml"
        ml_dir.mkdir()
        (ml_dir / "test.ml").write_text('function test() { return 1; }')

        registry = ModuleRegistry()
        registry.add_ml_module_paths([str(ml_dir)])

        # Get info before loading
        info = registry.get_module_info("test")
        assert info is not None
        assert info['name'] == "test"
        assert info['type'] == "ml_source"
        assert info['file_path'].endswith("test.ml")
        assert info['loaded'] is False
        assert info['needs_recompilation'] is True
        assert 'transpiled_path' in info

        # Load the module
        registry.get_module("test")

        # Get info after loading
        info = registry.get_module_info("test")
        assert info['loaded'] is True
        assert 'load_time_ms' in info

    def test_module_info_for_nested_ml_module(self, tmp_path):
        """Test get_module_info for nested ML modules."""
        ml_dir = tmp_path / "ml"
        ml_dir.mkdir()
        subdir = ml_dir / "nested"
        subdir.mkdir()
        (subdir / "deep.ml").write_text('function test() { return 1; }')

        registry = ModuleRegistry()
        registry.add_ml_module_paths([str(ml_dir)])

        info = registry.get_module_info("nested.deep")
        assert info is not None
        assert info['name'] == "nested.deep"
        assert info['type'] == "ml_source"

    def test_module_info_nonexistent(self):
        """Test get_module_info returns None for nonexistent module."""
        registry = ModuleRegistry()

        info = registry.get_module_info("does_not_exist")
        assert info is None
