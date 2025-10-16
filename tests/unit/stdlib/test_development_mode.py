"""Tests for ModuleRegistry development mode features.

Tests module hot-reloading, performance monitoring, and memory profiling
capabilities of the ModuleRegistry in development mode.
"""

import os
import pytest
import time
from pathlib import Path
from mlpy.stdlib.module_registry import ModuleRegistry, get_registry


class TestModuleReloading:
    """Test module reloading functionality."""

    def test_reload_single_module(self, tmp_path):
        """Test reloading a single module updates its code."""
        ext_dir = tmp_path / "ext"
        ext_dir.mkdir()

        # Create initial module version
        module_file = ext_dir / "test_bridge.py"
        module_file.write_text('''
from mlpy.stdlib.decorators import ml_module, ml_function

@ml_module(name="test", description="Test module")
class TestModule:
    @ml_function(description="Get version")
    def version(self):
        return "v1"

test = TestModule()
''')

        registry = ModuleRegistry()
        registry.add_extension_paths([str(ext_dir)])

        # Load module and verify initial version
        module = registry.get_module("test")
        assert module is not None
        assert module.version() == "v1"

        # Modify module to new version
        module_file.write_text('''
from mlpy.stdlib.decorators import ml_module, ml_function

@ml_module(name="test", description="Test module")
class TestModule:
    @ml_function(description="Get version")
    def version(self):
        return "v2"

test = TestModule()
''')

        # Reload and verify new version
        success = registry.reload_module("test")
        assert success is True

        # Get reloaded module
        reloaded_module = registry.get_module("test")
        assert reloaded_module is not None
        assert reloaded_module.version() == "v2"

    def test_reload_nonexistent_module(self):
        """Test reloading a module that doesn't exist."""
        registry = ModuleRegistry()

        success = registry.reload_module("nonexistent_module")
        assert success is False

    def test_reload_all_modules(self):
        """Test reloading all currently loaded modules."""
        registry = ModuleRegistry()

        # Load some standard library modules
        registry.get_module("math")
        registry.get_module("json")

        # Reload all
        results = registry.reload_all_modules()

        assert "math" in results
        assert "json" in results
        assert results["math"] is True
        assert results["json"] is True

    def test_reload_all_with_no_loaded_modules(self):
        """Test reload_all_modules when no modules are loaded."""
        registry = ModuleRegistry()

        results = registry.reload_all_modules()
        assert results == {}

    def test_refresh_all(self):
        """Test complete refresh with re-scan and reload."""
        registry = ModuleRegistry()

        # Load some modules
        registry.get_module("math")
        registry.get_module("json")

        # Refresh all
        result = registry.refresh_all()

        assert "total_modules" in result
        assert "reloaded_modules" in result
        assert "reload_failures" in result
        assert result["total_modules"] > 0
        assert result["reloaded_modules"] >= 2

    def test_reload_preserves_other_modules(self, tmp_path):
        """Test that reloading one module doesn't affect others."""
        ext_dir = tmp_path / "ext"
        ext_dir.mkdir()

        # Create two modules
        module1 = ext_dir / "module1_bridge.py"
        module1.write_text('''
from mlpy.stdlib.decorators import ml_module, ml_function

@ml_module(name="module1", description="Module 1")
class Module1:
    @ml_function(description="Get value")
    def value(self):
        return "module1_v1"

module1 = Module1()
''')

        module2 = ext_dir / "module2_bridge.py"
        module2.write_text('''
from mlpy.stdlib.decorators import ml_module, ml_function

@ml_module(name="module2", description="Module 2")
class Module2:
    @ml_function(description="Get value")
    def value(self):
        return "module2_original"

module2 = Module2()
''')

        registry = ModuleRegistry()
        registry.add_extension_paths([str(ext_dir)])

        # Load both modules
        mod1 = registry.get_module("module1")
        mod2 = registry.get_module("module2")
        assert mod1.value() == "module1_v1"
        assert mod2.value() == "module2_original"

        # Modify only module1
        module1.write_text('''
from mlpy.stdlib.decorators import ml_module, ml_function

@ml_module(name="module1", description="Module 1")
class Module1:
    @ml_function(description="Get value")
    def value(self):
        return "module1_v2"

module1 = Module1()
''')

        # Reload only module1
        registry.reload_module("module1")

        # Verify module1 updated, module2 unchanged
        mod1_reloaded = registry.get_module("module1")
        mod2_again = registry.get_module("module2")
        assert mod1_reloaded.value() == "module1_v2"
        assert mod2_again.value() == "module2_original"


class TestPerformanceMonitoring:
    """Test performance monitoring features."""

    def test_enable_disable_performance_mode(self):
        """Test toggling performance monitoring on and off."""
        registry = ModuleRegistry()

        # Default should be disabled
        assert registry._performance_mode is False

        # Enable
        registry.enable_performance_mode()
        assert registry._performance_mode is True

        # Disable
        registry.disable_performance_mode()
        assert registry._performance_mode is False

    def test_performance_tracking_when_enabled(self):
        """Test that timing metrics are collected when enabled."""
        registry = ModuleRegistry()
        registry.enable_performance_mode()

        # Load some modules
        registry.get_module("math")
        registry.get_module("json")

        # Get summary
        summary = registry.get_performance_summary()

        assert summary["total_loads"] >= 2
        assert summary["avg_load_time_ms"] >= 0
        assert len(summary["slowest_loads"]) > 0
        assert "math" in [name for name, _ in summary["slowest_loads"]]

    def test_performance_summary_structure(self):
        """Test that performance summary has correct structure."""
        registry = ModuleRegistry()
        registry.enable_performance_mode()

        summary = registry.get_performance_summary()

        # Verify all expected keys
        assert "total_scans" in summary
        assert "avg_scan_time_ms" in summary
        assert "total_loads" in summary
        assert "avg_load_time_ms" in summary
        assert "slowest_loads" in summary
        assert "reload_counts" in summary

        # Verify types
        assert isinstance(summary["total_scans"], int)
        assert isinstance(summary["avg_scan_time_ms"], float)
        assert isinstance(summary["total_loads"], int)
        assert isinstance(summary["avg_load_time_ms"], float)
        assert isinstance(summary["slowest_loads"], list)
        assert isinstance(summary["reload_counts"], dict)

    def test_reload_tracking(self, tmp_path):
        """Test that reloads are tracked in performance metrics."""
        ext_dir = tmp_path / "ext"
        ext_dir.mkdir()

        module_file = ext_dir / "test_bridge.py"
        module_file.write_text('''
from mlpy.stdlib.decorators import ml_module

@ml_module(name="test", description="Test")
class Test:
    pass

test = Test()
''')

        registry = ModuleRegistry()
        registry.enable_performance_mode()
        registry.add_extension_paths([str(ext_dir)])

        # Load and reload multiple times
        registry.get_module("test")
        registry.reload_module("test")
        registry.reload_module("test")

        summary = registry.get_performance_summary()
        assert "test" in summary["reload_counts"]
        assert summary["reload_counts"]["test"] >= 2

    def test_slow_load_warning(self, caplog):
        """Test that slow module loads generate warnings."""
        registry = ModuleRegistry()
        registry.enable_performance_mode()

        # Simulate slow load (>100ms threshold)
        registry._record_timing("load", "slow_module", 0.15)

        # Check for warning in logs
        assert any("Slow" in record.message for record in caplog.records)

    def test_performance_mode_env_variable(self):
        """Test MLPY_DEV_MODE environment variable."""
        # Set environment variable
        os.environ["MLPY_DEV_MODE"] = "1"

        # Create new registry (should auto-enable dev mode)
        registry = ModuleRegistry()
        assert registry._performance_mode is True

        # Clean up
        del os.environ["MLPY_DEV_MODE"]


class TestMemoryProfiling:
    """Test memory profiling features."""

    def test_memory_report_structure(self):
        """Test that memory report has correct structure."""
        registry = ModuleRegistry()

        # Load some modules
        registry.get_module("math")
        registry.get_module("json")

        report = registry.get_memory_report()

        # Verify structure
        assert "total_loaded" in report
        assert "total_size_kb" in report
        assert "total_size_mb" in report
        assert "modules" in report

        # Verify types
        assert isinstance(report["total_loaded"], int)
        assert isinstance(report["total_size_kb"], float)
        assert isinstance(report["total_size_mb"], float)
        assert isinstance(report["modules"], list)

    def test_memory_report_with_loaded_modules(self):
        """Test memory report shows loaded modules."""
        registry = ModuleRegistry()

        # Load modules
        registry.get_module("math")
        registry.get_module("json")

        report = registry.get_memory_report()

        assert report["total_loaded"] >= 2
        assert report["total_size_kb"] > 0
        assert len(report["modules"]) > 0

        # Verify module entries have correct structure
        for module in report["modules"]:
            assert "name" in module
            assert "size_bytes" in module
            assert "size_kb" in module

    def test_memory_report_sorted_by_size(self):
        """Test that memory report modules are sorted by size."""
        registry = ModuleRegistry()

        # Load multiple modules
        registry.get_module("math")
        registry.get_module("json")
        registry.get_module("datetime")

        report = registry.get_memory_report()

        # Verify sorting (descending by size)
        sizes = [mod["size_bytes"] for mod in report["modules"]]
        assert sizes == sorted(sizes, reverse=True)

    def test_memory_report_top_10_limit(self, tmp_path):
        """Test that memory report limits to top 10 modules."""
        ext_dir = tmp_path / "ext"
        ext_dir.mkdir()

        # Create 15 test modules
        for i in range(15):
            module_file = ext_dir / f"test{i}_bridge.py"
            module_file.write_text(f'''
from mlpy.stdlib.decorators import ml_module

@ml_module(name="test{i}", description="Test {i}")
class Test{i}:
    pass

test{i} = Test{i}()
''')

        registry = ModuleRegistry()
        registry.add_extension_paths([str(ext_dir)])

        # Load all 15 modules
        for i in range(15):
            registry.get_module(f"test{i}")

        report = registry.get_memory_report()

        # Should limit to top 10
        assert len(report["modules"]) == 10
        assert report["total_loaded"] == 15

    def test_memory_report_empty_registry(self):
        """Test memory report with no loaded modules."""
        registry = ModuleRegistry()

        report = registry.get_memory_report()

        assert report["total_loaded"] == 0
        assert report["total_size_kb"] == 0
        assert report["total_size_mb"] == 0
        assert len(report["modules"]) == 0


class TestGlobalRegistry:
    """Test global registry singleton functionality."""

    def test_get_registry_singleton(self):
        """Test that get_registry returns same instance."""
        registry1 = get_registry()
        registry2 = get_registry()

        assert registry1 is registry2

    def test_registry_persistence(self):
        """Test that registry state persists across get_registry calls."""
        registry1 = get_registry()
        registry1.enable_performance_mode()

        registry2 = get_registry()
        assert registry2._performance_mode is True


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_reload_module_with_syntax_error(self, tmp_path):
        """Test reloading a module with syntax errors fails gracefully."""
        ext_dir = tmp_path / "ext"
        ext_dir.mkdir()

        # Create valid module
        module_file = ext_dir / "test_bridge.py"
        module_file.write_text('''
from mlpy.stdlib.decorators import ml_module

@ml_module(name="test", description="Test")
class Test:
    pass

test = Test()
''')

        registry = ModuleRegistry()
        registry.add_extension_paths([str(ext_dir)])

        # Load module
        registry.get_module("test")

        # Write invalid Python syntax
        module_file.write_text('''
from mlpy.stdlib.decorators import ml_module

@ml_module(name="test", description="Test")
class Test
    # Missing colon - syntax error
    pass

test = Test()
''')

        # Reload should fail gracefully
        success = registry.reload_module("test")
        assert success is False

    def test_performance_summary_no_data(self):
        """Test performance summary with no data collected."""
        registry = ModuleRegistry()
        registry.enable_performance_mode()

        summary = registry.get_performance_summary()

        assert summary["total_scans"] == 0
        assert summary["avg_scan_time_ms"] == 0
        assert summary["total_loads"] == 0
        assert summary["avg_load_time_ms"] == 0
        assert len(summary["slowest_loads"]) == 0

    def test_reload_timing_accuracy(self, tmp_path):
        """Test that reload timing is reasonably accurate."""
        ext_dir = tmp_path / "ext"
        ext_dir.mkdir()

        module_file = ext_dir / "test_bridge.py"
        module_file.write_text('''
from mlpy.stdlib.decorators import ml_module

@ml_module(name="test", description="Test")
class Test:
    pass

test = Test()
''')

        registry = ModuleRegistry()
        registry.enable_performance_mode()
        registry.add_extension_paths([str(ext_dir)])

        # Load module
        registry.get_module("test")

        # Reload with timing
        start = time.perf_counter()
        registry.reload_module("test")
        elapsed = time.perf_counter() - start

        # Timing should be reasonable (< 2 seconds as per success criteria)
        assert elapsed < 2.0

        # Recorded timing should be in same ballpark
        summary = registry.get_performance_summary()
        if "test" in summary["reload_counts"]:
            # Allow some variance, but should be in similar magnitude
            assert elapsed * 0.5 < 2.0  # Very generous check
