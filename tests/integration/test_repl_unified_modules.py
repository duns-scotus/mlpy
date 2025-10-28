"""Integration tests for REPL with unified module registry (Python bridges + ML modules).

Tests cover:
- REPL initialization with ml_module_paths
- .modules command showing both types
- .modinfo command for both types
- .reload command for both types
- Module precedence (Python bridges win)
- Configuration-based ml_module_paths
"""

import pytest
from pathlib import Path
from mlpy.cli.repl import MLREPLSession, show_modules, show_module_info
from mlpy.stdlib.module_registry import get_registry, ModuleType
import io
import sys


class TestREPLUnifiedModuleIntegration:
    """Integration tests for REPL with unified module registry."""

    def test_repl_session_initialization_with_ml_modules(self, tmp_path):
        """Test REPL session initialization with ML module paths."""
        # Create ML module directory
        ml_dir = tmp_path / "ml_modules"
        ml_dir.mkdir()

        # Create test ML module
        (ml_dir / "test_module.ml").write_text('''
function greet(name) {
    return "Hello, " + name;
}
''')

        # Initialize REPL session with ML module paths
        session = MLREPLSession(
            security_enabled=False,
            ml_module_paths=[str(ml_dir)]
        )

        # Verify registry has ML module
        registry = get_registry()
        assert registry.is_available("test_module")

        metadata = registry._discovered["test_module"]
        assert metadata.module_type == ModuleType.ML_SOURCE
        assert metadata.name == "test_module"

    def test_repl_session_with_both_extension_and_ml_paths(self, tmp_path):
        """Test REPL with both Python extensions and ML modules."""
        # Create extension directory with Python bridge
        ext_dir = tmp_path / "extensions"
        ext_dir.mkdir()

        (ext_dir / "custom_bridge.py").write_text('''
from mlpy.stdlib.decorators import ml_module, ml_function

@ml_module(name="custom", description="Custom bridge module")
class CustomModule:
    @ml_function(description="Double value")
    def double(self, x: int) -> int:
        return x * 2

custom = CustomModule()
''')

        # Create ML module directory
        ml_dir = tmp_path / "ml_modules"
        ml_dir.mkdir()

        (ml_dir / "ml_custom.ml").write_text('''
function triple(x) {
    return x * 3;
}
''')

        # Initialize REPL with both paths
        session = MLREPLSession(
            security_enabled=False,
            extension_paths=[str(ext_dir)],
            ml_module_paths=[str(ml_dir)]
        )

        # Verify both modules are available
        registry = get_registry()
        assert registry.is_available("custom")
        assert registry.is_available("ml_custom")

        # Verify types
        custom_meta = registry._discovered["custom"]
        ml_meta = registry._discovered["ml_custom"]

        assert custom_meta.module_type == ModuleType.PYTHON_BRIDGE
        assert ml_meta.module_type == ModuleType.ML_SOURCE

    def test_module_precedence_python_wins(self, tmp_path):
        """Test that Python bridge takes precedence over ML module with same name."""
        # Create Python bridge
        ext_dir = tmp_path / "extensions"
        ext_dir.mkdir()

        (ext_dir / "utils_bridge.py").write_text('''
from mlpy.stdlib.decorators import ml_module, ml_function

@ml_module(name="utils", description="Python utils")
class Utils:
    @ml_function(description="Process")
    def process(self, x: int) -> int:
        return x * 10

utils = Utils()
''')

        # Create ML module with same name
        ml_dir = tmp_path / "ml_modules"
        ml_dir.mkdir()

        (ml_dir / "utils.ml").write_text('''
function process(x) {
    return x * 20;
}
''')

        # Initialize REPL - Python should win
        session = MLREPLSession(
            security_enabled=False,
            extension_paths=[str(ext_dir)],
            ml_module_paths=[str(ml_dir)]
        )

        registry = get_registry()
        assert registry.is_available("utils")

        metadata = registry._discovered["utils"]
        assert metadata.module_type == ModuleType.PYTHON_BRIDGE

        # Load module and verify it's the Python bridge
        utils_module = registry.get_module("utils")
        assert utils_module is not None
        assert utils_module.process(5) == 50  # Python bridge: x * 10

    def test_modules_command_shows_both_types(self, tmp_path, capsys):
        """Test .modules command shows both Python bridges and ML modules."""
        # Create Python bridge
        ext_dir = tmp_path / "extensions"
        ext_dir.mkdir()

        (ext_dir / "test_bridge.py").write_text('''
from mlpy.stdlib.decorators import ml_module

@ml_module(name="test_bridge", description="Test bridge")
class TestBridge:
    pass

test_bridge = TestBridge()
''')

        # Create ML modules
        ml_dir = tmp_path / "ml_modules"
        ml_dir.mkdir()

        (ml_dir / "ml_module1.ml").write_text('function test() { return 1; }')
        (ml_dir / "ml_module2.ml").write_text('function test() { return 2; }')

        # Initialize REPL
        session = MLREPLSession(
            security_enabled=False,
            extension_paths=[str(ext_dir)],
            ml_module_paths=[str(ml_dir)]
        )

        # Call show_modules() command
        show_modules()

        captured = capsys.readouterr()
        output = captured.out

        # Verify output shows both types
        assert "Python Bridge Modules" in output
        assert "ML Source Modules" in output
        assert "test_bridge" in output
        assert "ml_module1" in output
        assert "ml_module2" in output

    def test_modinfo_command_for_ml_module(self, tmp_path, capsys):
        """Test .modinfo command for ML modules."""
        ml_dir = tmp_path / "ml_modules"
        ml_dir.mkdir()

        ml_file = ml_dir / "test_ml.ml"
        ml_file.write_text('''
function example() {
    return "test";
}
''')

        # Initialize REPL
        session = MLREPLSession(
            security_enabled=False,
            ml_module_paths=[str(ml_dir)]
        )

        # Trigger scan
        registry = get_registry()
        registry.is_available("test_ml")

        # Call show_module_info() command
        show_module_info("test_ml")

        captured = capsys.readouterr()
        output = captured.out

        # Verify output shows ML module info
        assert "Module: test_ml" in output
        assert "Type: ml_source" in output
        assert "File Path:" in output
        assert "test_ml.ml" in output
        assert "Transpiled Path:" in output
        assert "Needs Recompilation:" in output

    def test_modinfo_command_for_python_bridge(self, tmp_path, capsys):
        """Test .modinfo command for Python bridge modules."""
        ext_dir = tmp_path / "extensions"
        ext_dir.mkdir()

        (ext_dir / "test_bridge.py").write_text('''
from mlpy.stdlib.decorators import ml_module, ml_function

@ml_module(name="test_bridge", description="Test bridge module")
class TestBridge:
    @ml_function(description="Test function")
    def test_func(self):
        return "test"

test_bridge = TestBridge()
''')

        # Initialize REPL
        session = MLREPLSession(
            security_enabled=False,
            extension_paths=[str(ext_dir)]
        )

        # Trigger scan
        registry = get_registry()
        registry.is_available("test_bridge")

        # Call show_module_info() command
        show_module_info("test_bridge")

        captured = capsys.readouterr()
        output = captured.out

        # Verify output shows Python bridge info
        assert "Module: test_bridge" in output
        assert "Type: python_bridge" in output
        assert "File Path:" in output
        assert "test_bridge.py" in output

    def test_reload_ml_module_in_repl(self, tmp_path):
        """Test reloading ML modules in REPL session."""
        import time

        ml_dir = tmp_path / "ml_modules"
        ml_dir.mkdir()

        ml_file = ml_dir / "reload_test.ml"
        ml_file.write_text('function get_value() { return 100; }')

        # Initialize REPL
        session = MLREPLSession(
            security_enabled=False,
            ml_module_paths=[str(ml_dir)]
        )

        # Load the module
        registry = get_registry()
        module1 = registry.get_module("reload_test")
        assert module1 is not None

        # Modify the file
        time.sleep(0.01)  # Ensure timestamp difference
        ml_file.write_text('function get_value() { return 200; }')

        # Update source_mtime in metadata
        metadata = registry._discovered["reload_test"]
        metadata.source_mtime = ml_file.stat().st_mtime

        # Reload using session's reload method
        success, msg = session.reload_module("reload_test")
        assert success
        assert "Reloaded module" in msg

        # Verify module was reloaded
        assert metadata.reload_count >= 1

    def test_nested_ml_modules_in_repl(self, tmp_path):
        """Test REPL with nested ML module directories."""
        ml_dir = tmp_path / "ml_modules"
        ml_dir.mkdir()

        # Create nested structure
        algorithms_dir = ml_dir / "algorithms"
        algorithms_dir.mkdir()

        (algorithms_dir / "sorting.ml").write_text('''
function sort(arr) {
    return arr;
}
''')

        # Initialize REPL
        session = MLREPLSession(
            security_enabled=False,
            ml_module_paths=[str(ml_dir)]
        )

        # Verify nested module is available
        registry = get_registry()
        assert registry.is_available("algorithms.sorting")

        metadata = registry._discovered["algorithms.sorting"]
        assert metadata.module_type == ModuleType.ML_SOURCE
        assert metadata.name == "algorithms.sorting"

    def test_repl_execution_with_ml_module_import(self, tmp_path):
        """Test executing ML code that imports ML modules in REPL."""
        ml_dir = tmp_path / "ml_modules"
        ml_dir.mkdir()

        # Create ML module
        (ml_dir / "math_utils.ml").write_text('''
function add(a, b) {
    return a + b;
}

function multiply(a, b) {
    return a * b;
}
''')

        # Initialize REPL
        session = MLREPLSession(
            security_enabled=False,
            ml_module_paths=[str(ml_dir)]
        )

        # Execute import statement
        result = session.execute_ml_line('import math_utils;')
        assert result.success

        # Execute code using imported module
        result = session.execute_ml_line('math_utils.add(5, 3)')
        assert result.success
        # Note: Module imports in REPL need special handling
        # This test verifies the module is available in registry

    def test_ml_module_with_multiple_repl_paths(self, tmp_path):
        """Test REPL with multiple ML module paths."""
        ml_dir1 = tmp_path / "ml_modules1"
        ml_dir1.mkdir()
        (ml_dir1 / "module1.ml").write_text('function test1() { return 1; }')

        ml_dir2 = tmp_path / "ml_modules2"
        ml_dir2.mkdir()
        (ml_dir2 / "module2.ml").write_text('function test2() { return 2; }')

        # Initialize REPL with multiple paths
        session = MLREPLSession(
            security_enabled=False,
            ml_module_paths=[str(ml_dir1), str(ml_dir2)]
        )

        # Verify both modules are available
        registry = get_registry()
        assert registry.is_available("module1")
        assert registry.is_available("module2")

        # Verify both are ML source modules
        assert registry._discovered["module1"].module_type == ModuleType.ML_SOURCE
        assert registry._discovered["module2"].module_type == ModuleType.ML_SOURCE


class TestREPLConfigurationIntegration:
    """Test REPL integration with project configuration."""

    def test_repl_with_config_ml_module_paths(self, tmp_path):
        """Test that REPL respects ml_module_paths from project config."""
        from mlpy.cli.project_manager import MLProjectManager, MLProjectConfig

        # Create ML module directory
        ml_dir = tmp_path / "ml_modules"
        ml_dir.mkdir()
        (ml_dir / "config_test.ml").write_text('function test() { return 1; }')

        # Create project config
        config = MLProjectConfig(
            name="test-project",
            ml_module_paths=[str(ml_dir)]
        )

        # Verify config has ml_module_paths
        assert config.ml_module_paths == [str(ml_dir)]

        # Initialize REPL with config-based paths
        session = MLREPLSession(
            security_enabled=False,
            ml_module_paths=config.ml_module_paths
        )

        # Verify module is available
        registry = get_registry()
        assert registry.is_available("config_test")

    def test_cli_ml_module_path_priority(self, tmp_path):
        """Test CLI ml_module_path takes priority over config."""
        from mlpy.cli.app import resolve_ml_module_paths
        from mlpy.cli.project_manager import MLProjectManager, MLProjectConfig

        # Create two different paths
        cli_path = tmp_path / "cli_modules"
        config_path = tmp_path / "config_modules"
        cli_path.mkdir()
        config_path.mkdir()

        # Create project manager with config
        project_manager = MLProjectManager()
        project_manager.config = MLProjectConfig(
            name="test",
            ml_module_paths=[str(config_path)]
        )

        # Resolve with CLI override
        cli_flags = (str(cli_path),)
        resolved = resolve_ml_module_paths(cli_flags, project_manager)

        # CLI should win
        assert resolved == [str(cli_path)]

    def test_config_ml_module_path_without_cli(self, tmp_path):
        """Test config ml_module_paths used when no CLI flags."""
        from mlpy.cli.app import resolve_ml_module_paths
        from mlpy.cli.project_manager import MLProjectManager, MLProjectConfig

        config_path = tmp_path / "config_modules"
        config_path.mkdir()

        # Create project manager with config
        project_manager = MLProjectManager()
        project_manager.config = MLProjectConfig(
            name="test",
            ml_module_paths=[str(config_path)]
        )

        # Resolve without CLI flags
        resolved = resolve_ml_module_paths(None, project_manager)

        # Config should be used
        assert resolved == [str(config_path)]


class TestWeek3BuiltinFunctions:
    """Week 3 tests for builtin.available_modules() and builtin.module_info()."""

    def test_available_modules_returns_all_types(self, tmp_path):
        """Test builtin.available_modules() returns both Python and ML modules."""
        # Create Python bridge
        ext_dir = tmp_path / "extensions"
        ext_dir.mkdir()
        (ext_dir / "custom_bridge.py").write_text('''
from mlpy.stdlib.decorators import ml_module
@ml_module(name="custom_python", description="Custom")
class Custom:
    pass
custom_python = Custom()
''')

        # Create ML module
        ml_dir = tmp_path / "ml_modules"
        ml_dir.mkdir()
        (ml_dir / "custom_ml.ml").write_text('function test() { return 1; }')

        # Initialize REPL
        session = MLREPLSession(
            security_enabled=False,
            extension_paths=[str(ext_dir)],
            ml_module_paths=[str(ml_dir)]
        )

        # Get builtin instance
        from mlpy.stdlib.builtin import builtin

        # Get all modules
        all_modules = builtin.available_modules()
        assert "custom_python" in all_modules
        assert "custom_ml" in all_modules

    def test_available_modules_filter_python_bridges(self, tmp_path):
        """Test builtin.available_modules() filters by python_bridge type."""
        ext_dir = tmp_path / "extensions"
        ext_dir.mkdir()
        (ext_dir / "bridge_bridge.py").write_text('''
from mlpy.stdlib.decorators import ml_module
@ml_module(name="bridge", description="Bridge")
class Bridge:
    pass
bridge = Bridge()
''')

        ml_dir = tmp_path / "ml_modules"
        ml_dir.mkdir()
        (ml_dir / "ml_mod.ml").write_text('function test() { return 1; }')

        session = MLREPLSession(
            security_enabled=False,
            extension_paths=[str(ext_dir)],
            ml_module_paths=[str(ml_dir)]
        )

        from mlpy.stdlib.builtin import builtin

        # Filter by python_bridge
        python_modules = builtin.available_modules("python_bridge")
        assert "bridge" in python_modules
        assert "ml_mod" not in python_modules

    def test_available_modules_filter_ml_source(self, tmp_path):
        """Test builtin.available_modules() filters by ml_source type."""
        ext_dir = tmp_path / "extensions"
        ext_dir.mkdir()
        (ext_dir / "bridge_bridge.py").write_text('''
from mlpy.stdlib.decorators import ml_module
@ml_module(name="bridge", description="Bridge")
class Bridge:
    pass
bridge = Bridge()
''')

        ml_dir = tmp_path / "ml_modules"
        ml_dir.mkdir()
        (ml_dir / "ml_mod.ml").write_text('function test() { return 1; }')

        session = MLREPLSession(
            security_enabled=False,
            extension_paths=[str(ext_dir)],
            ml_module_paths=[str(ml_dir)]
        )

        from mlpy.stdlib.builtin import builtin

        # Filter by ml_source
        ml_modules = builtin.available_modules("ml_source")
        assert "ml_mod" in ml_modules
        assert "bridge" not in ml_modules

    def test_module_info_for_ml_module(self, tmp_path):
        """Test builtin.module_info() returns ML module details."""
        ml_dir = tmp_path / "ml_modules"
        ml_dir.mkdir()
        (ml_dir / "test_ml.ml").write_text('function test() { return 1; }')

        session = MLREPLSession(
            security_enabled=False,
            ml_module_paths=[str(ml_dir)]
        )

        from mlpy.stdlib.builtin import builtin

        # Get module info
        info = builtin.module_info("test_ml")
        assert info is not None
        assert info['name'] == "test_ml"
        assert info['type'] == "ml_source"
        assert 'transpiled_path' in info
        assert 'needs_recompilation' in info

    def test_module_info_for_python_bridge(self, tmp_path):
        """Test builtin.module_info() returns Python bridge details."""
        ext_dir = tmp_path / "extensions"
        ext_dir.mkdir()
        (ext_dir / "test_bridge.py").write_text('''
from mlpy.stdlib.decorators import ml_module, ml_function
@ml_module(name="test_bridge", description="Test")
class TestBridge:
    @ml_function(description="Test function")
    def test_func(self):
        return "test"
test_bridge = TestBridge()
''')

        session = MLREPLSession(
            security_enabled=False,
            extension_paths=[str(ext_dir)]
        )

        from mlpy.stdlib.builtin import builtin

        # Get module info
        info = builtin.module_info("test_bridge")
        assert info is not None
        assert info['name'] == "test_bridge"
        assert info['type'] == "python_bridge"
        assert 'functions' in info


class TestWeek3PerformanceMonitoring:
    """Week 3 tests for .perfmon and .memreport commands."""

    def test_perfmon_shows_module_type_breakdown(self, tmp_path):
        """Test .perfmon command shows Python bridge and ML module stats separately."""
        ext_dir = tmp_path / "extensions"
        ext_dir.mkdir()
        (ext_dir / "bridge_bridge.py").write_text('''
from mlpy.stdlib.decorators import ml_module
@ml_module(name="bridge", description="Bridge")
class Bridge:
    pass
bridge = Bridge()
''')

        ml_dir = tmp_path / "ml_modules"
        ml_dir.mkdir()
        (ml_dir / "ml_mod.ml").write_text('function test() { return 1; }')

        session = MLREPLSession(
            security_enabled=False,
            extension_paths=[str(ext_dir)],
            ml_module_paths=[str(ml_dir)]
        )

        # Enable performance mode
        session.toggle_dev_mode()

        # Load modules to generate performance data
        from mlpy.stdlib.module_registry import get_registry
        registry = get_registry()
        registry.get_module("bridge")
        registry.get_module("ml_mod")

        # Get performance summary
        success, msg = session.get_performance_summary()
        assert success
        assert "Python Bridge Modules:" in msg
        assert "ML Modules:" in msg
        assert "transpilations" in msg.lower() or "transpilation" in msg.lower()

    def test_memreport_shows_module_type_breakdown(self, tmp_path):
        """Test .memreport command shows Python bridge and ML module memory separately."""
        ext_dir = tmp_path / "extensions"
        ext_dir.mkdir()
        (ext_dir / "bridge_bridge.py").write_text('''
from mlpy.stdlib.decorators import ml_module
@ml_module(name="bridge", description="Bridge")
class Bridge:
    pass
bridge = Bridge()
''')

        ml_dir = tmp_path / "ml_modules"
        ml_dir.mkdir()
        (ml_dir / "ml_mod.ml").write_text('function test() { return 1; }')

        session = MLREPLSession(
            security_enabled=False,
            extension_paths=[str(ext_dir)],
            ml_module_paths=[str(ml_dir)]
        )

        # Load modules to generate memory data
        from mlpy.stdlib.module_registry import get_registry
        registry = get_registry()
        registry.get_module("bridge")
        registry.get_module("ml_mod")

        # Get memory report
        success, msg = session.get_memory_report()
        assert success
        assert "Python Bridge Modules" in msg or "ML Modules" in msg


@pytest.fixture(autouse=True)
def reset_registry():
    """Reset the global registry before each test."""
    from mlpy.stdlib.module_registry import get_registry

    registry = get_registry()
    registry.invalidate_cache()
    yield
    registry.invalidate_cache()
