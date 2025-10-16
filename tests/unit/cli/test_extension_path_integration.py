"""Unit tests for Phase 2 extension path CLI integration.

Tests cover:
- resolve_extension_paths() priority system (CLI > Config > Env)
- Platform-specific path separators (Windows vs Unix)
- MLProjectConfig extension_paths field
- MLTranspiler initialization with extension paths
- REPL session extension path handling
"""

import os
import sys
import pytest
from pathlib import Path
from unittest.mock import Mock, patch

# Import the resolve_extension_paths function
from mlpy.cli.app import resolve_extension_paths
from mlpy.cli.project_manager import MLProjectManager, MLProjectConfig
from mlpy.ml.transpiler import MLTranspiler
from mlpy.cli.repl import MLREPLSession


class TestResolveExtensionPaths:
    """Test the resolve_extension_paths priority system."""

    def test_cli_flags_highest_priority(self, tmp_path):
        """Test that CLI flags take precedence over config and env."""
        # Setup
        cli_paths = ("/cli/path1", "/cli/path2")

        # Create project manager with config
        project_manager = MLProjectManager()
        project_manager.config = MLProjectConfig(
            python_extension_paths=["/config/path1", "/config/path2"]
        )

        # Set environment variable
        with patch.dict(os.environ, {"MLPY_EXTENSION_PATHS": "/env/path1:/env/path2"}):
            result = resolve_extension_paths(cli_paths, project_manager)

        # CLI flags should win
        assert result == list(cli_paths)
        assert "/config/path1" not in result
        assert "/env/path1" not in result

    def test_config_second_priority(self, tmp_path):
        """Test that config takes precedence over env when no CLI flags."""
        # Setup
        project_manager = MLProjectManager()
        project_manager.config = MLProjectConfig(
            python_extension_paths=["/config/path1", "/config/path2"]
        )

        # Set environment variable
        with patch.dict(os.environ, {"MLPY_EXTENSION_PATHS": "/env/path1:/env/path2"}):
            result = resolve_extension_paths(None, project_manager)

        # Config should win
        assert result == ["/config/path1", "/config/path2"]
        assert "/env/path1" not in result

    def test_env_lowest_priority_unix(self):
        """Test environment variable as fallback with Unix separator."""
        # No CLI flags, no config
        with patch.dict(os.environ, {"MLPY_EXTENSION_PATHS": "/env/path1:/env/path2:/env/path3"}):
            with patch('sys.platform', 'linux'):
                result = resolve_extension_paths(None, None)

        assert result == ["/env/path1", "/env/path2", "/env/path3"]

    def test_env_lowest_priority_windows(self):
        """Test environment variable with Windows separator."""
        # No CLI flags, no config
        with patch.dict(os.environ, {"MLPY_EXTENSION_PATHS": "C:\\ext1;C:\\ext2;C:\\ext3"}):
            with patch('sys.platform', 'win32'):
                result = resolve_extension_paths(None, None)

        assert result == ["C:\\ext1", "C:\\ext2", "C:\\ext3"]

    def test_empty_cli_flags_tuple(self):
        """Test that empty tuple is treated as no CLI flags."""
        project_manager = MLProjectManager()
        project_manager.config = MLProjectConfig(
            python_extension_paths=["/config/path"]
        )

        result = resolve_extension_paths((), project_manager)

        # Empty tuple should fallback to config
        assert result == ["/config/path"]

    def test_no_sources_returns_empty(self):
        """Test that no sources returns empty list."""
        result = resolve_extension_paths(None, None)

        assert result == []

    def test_whitespace_trimming_in_env(self):
        """Test that environment variable paths are trimmed."""
        with patch.dict(os.environ, {"MLPY_EXTENSION_PATHS": "  /path1  :  /path2  : /path3"}):
            with patch('sys.platform', 'linux'):
                result = resolve_extension_paths(None, None)

        assert result == ["/path1", "/path2", "/path3"]

    def test_empty_segments_filtered_in_env(self):
        """Test that empty segments in env var are filtered."""
        with patch.dict(os.environ, {"MLPY_EXTENSION_PATHS": "/path1::/path2:::"}):
            with patch('sys.platform', 'linux'):
                result = resolve_extension_paths(None, None)

        assert result == ["/path1", "/path2"]

    def test_missing_env_variable(self):
        """Test that missing env variable returns empty list."""
        with patch.dict(os.environ, {}, clear=True):
            result = resolve_extension_paths(None, None)

        assert result == []

    def test_project_manager_without_config(self):
        """Test project manager without loaded config."""
        project_manager = MLProjectManager()
        # No config loaded (config = None)

        result = resolve_extension_paths(None, project_manager)

        assert result == []

    def test_config_without_extension_paths(self):
        """Test config that doesn't have extension_paths set."""
        project_manager = MLProjectManager()
        project_manager.config = MLProjectConfig()
        # Default config has empty list for python_extension_paths

        # Set env var as fallback
        with patch.dict(os.environ, {"MLPY_EXTENSION_PATHS": "/env/path"}):
            with patch('sys.platform', 'linux'):
                result = resolve_extension_paths(None, project_manager)

        # Should fallback to env since config has empty list
        assert result == ["/env/path"]


class TestMLProjectConfigExtensionPaths:
    """Test MLProjectConfig extension paths field."""

    def test_default_initialization(self):
        """Test that python_extension_paths defaults to empty list."""
        config = MLProjectConfig()

        assert config.python_extension_paths == []
        assert isinstance(config.python_extension_paths, list)

    def test_explicit_initialization(self):
        """Test explicit initialization with paths."""
        paths = ["/path1", "/path2", "/path3"]
        config = MLProjectConfig(python_extension_paths=paths)

        assert config.python_extension_paths == paths

    def test_none_initialization_converts_to_empty_list(self):
        """Test that None is converted to empty list in __post_init__."""
        config = MLProjectConfig(python_extension_paths=None)

        assert config.python_extension_paths == []

    def test_serialization_to_dict(self):
        """Test that extension paths serialize correctly."""
        from dataclasses import asdict

        config = MLProjectConfig(
            name="test-project",
            python_extension_paths=["/ext1", "/ext2"]
        )

        data = asdict(config)

        assert "python_extension_paths" in data
        assert data["python_extension_paths"] == ["/ext1", "/ext2"]

    def test_config_save_and_load(self, tmp_path):
        """Test saving and loading config with extension paths."""
        # Create config with extension paths
        config_file = tmp_path / "mlpy.json"

        manager = MLProjectManager()
        manager.project_root = tmp_path
        manager.config = MLProjectConfig(
            name="test",
            python_extension_paths=["/ext1", "/ext2"]
        )

        # Save
        success = manager.save_config(config_file)
        assert success
        assert config_file.exists()

        # Load
        manager2 = MLProjectManager()
        success = manager2.load_config(config_file)
        assert success
        assert manager2.config.python_extension_paths == ["/ext1", "/ext2"]


class TestMLTranspilerExtensionPaths:
    """Test MLTranspiler extension path initialization."""

    def test_transpiler_without_extension_paths(self):
        """Test transpiler initialization without extension paths."""
        transpiler = MLTranspiler()

        assert transpiler.python_extension_paths == []

    def test_transpiler_with_extension_paths(self, tmp_path):
        """Test transpiler initialization with extension paths."""
        ext_paths = [str(tmp_path / "ext1"), str(tmp_path / "ext2")]

        # Create the directories
        for path in ext_paths:
            Path(path).mkdir(parents=True, exist_ok=True)

        transpiler = MLTranspiler(python_extension_paths=ext_paths)

        assert transpiler.python_extension_paths == ext_paths

    def test_transpiler_registers_paths_with_registry(self, tmp_path):
        """Test that transpiler registers extension paths with module registry."""
        from mlpy.stdlib.module_registry import get_registry

        # Create extension directory with a test module
        ext_dir = tmp_path / "extensions"
        ext_dir.mkdir()

        test_module = ext_dir / "testmod_bridge.py"
        test_module.write_text('''
from mlpy.stdlib.decorators import ml_module, ml_function

@ml_module(name="testmod", description="Test module")
class TestMod:
    @ml_function(description="Test function")
    def hello(self):
        return "Hello from testmod"

testmod = TestMod()
''')

        # Create transpiler with extension path
        transpiler = MLTranspiler(python_extension_paths=[str(ext_dir)])

        # Check that registry knows about the module
        registry = get_registry()
        assert registry.is_available("testmod")

        # Verify we can load it
        mod = registry.get_module("testmod")
        assert mod is not None
        assert mod.hello() == "Hello from testmod"

    def test_transpiler_repl_mode_with_extension_paths(self, tmp_path):
        """Test REPL mode transpiler with extension paths."""
        ext_paths = [str(tmp_path / "ext")]

        # Create directory
        Path(ext_paths[0]).mkdir(parents=True, exist_ok=True)

        transpiler = MLTranspiler(repl_mode=True, python_extension_paths=ext_paths)

        assert transpiler.repl_mode is True
        assert transpiler.python_extension_paths == ext_paths


class TestMLREPLSessionExtensionPaths:
    """Test REPL session extension path handling."""

    def test_repl_session_without_extension_paths(self):
        """Test REPL session creation without extension paths."""
        session = MLREPLSession(security_enabled=False)

        assert session.transpiler.python_extension_paths == []

    def test_repl_session_with_extension_paths(self, tmp_path):
        """Test REPL session creation with extension paths."""
        ext_paths = [str(tmp_path / "ext1")]
        Path(ext_paths[0]).mkdir(parents=True, exist_ok=True)

        session = MLREPLSession(security_enabled=False, extension_paths=ext_paths)

        assert session.transpiler.python_extension_paths == ext_paths

    def test_repl_can_import_extension_modules(self, tmp_path):
        """Test that REPL can import modules from extension paths."""
        # Create extension module
        ext_dir = tmp_path / "extensions"
        ext_dir.mkdir()

        custom_module = ext_dir / "mymath_bridge.py"
        custom_module.write_text('''
from mlpy.stdlib.decorators import ml_module, ml_function

@ml_module(name="mymath", description="Custom math module")
class MyMath:
    @ml_function(description="Double a number")
    def double(self, x: int) -> int:
        return x * 2

mymath = MyMath()
''')

        # Create REPL with extension path
        session = MLREPLSession(
            security_enabled=False,
            extension_paths=[str(ext_dir)]
        )

        # Execute ML code that imports the custom module
        # Note: The transpiler should recognize "mymath" from the registry
        result = session.execute_ml_line('x = 21;')
        assert result.success

        # Verify the module is available in registry
        from mlpy.stdlib.module_registry import get_registry
        registry = get_registry()
        assert registry.is_available("mymath")


class TestPlatformSpecificBehavior:
    """Test platform-specific path separator handling."""

    def test_windows_separator(self):
        """Test Windows semicolon separator."""
        env_paths = "C:\\ext1;D:\\ext2;E:\\ext3"

        with patch.dict(os.environ, {"MLPY_EXTENSION_PATHS": env_paths}):
            with patch('sys.platform', 'win32'):
                result = resolve_extension_paths(None, None)

        assert result == ["C:\\ext1", "D:\\ext2", "E:\\ext3"]

    def test_unix_separator(self):
        """Test Unix colon separator."""
        env_paths = "/usr/local/ext1:/opt/ext2:/home/user/ext3"

        with patch.dict(os.environ, {"MLPY_EXTENSION_PATHS": env_paths}):
            with patch('sys.platform', 'linux'):
                result = resolve_extension_paths(None, None)

        assert result == ["/usr/local/ext1", "/opt/ext2", "/home/user/ext3"]

    def test_macos_separator(self):
        """Test macOS uses colon separator (Unix-like)."""
        env_paths = "/Applications/ext1:/Users/test/ext2"

        with patch.dict(os.environ, {"MLPY_EXTENSION_PATHS": env_paths}):
            with patch('sys.platform', 'darwin'):
                result = resolve_extension_paths(None, None)

        assert result == ["/Applications/ext1", "/Users/test/ext2"]


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_very_long_path_list(self):
        """Test handling of many extension paths."""
        paths = tuple(f"/path{i}" for i in range(100))

        result = resolve_extension_paths(paths, None)

        assert len(result) == 100
        assert all(f"/path{i}" in result for i in range(100))

    def test_duplicate_paths_in_cli_flags(self):
        """Test that duplicate paths are preserved (user's choice)."""
        paths = ("/ext1", "/ext2", "/ext1", "/ext3")

        result = resolve_extension_paths(paths, None)

        # Should preserve duplicates as user specified
        assert result == list(paths)

    def test_paths_with_special_characters(self):
        """Test paths with spaces and special characters."""
        paths = (
            "/path with spaces",
            "/path-with-dashes",
            "/path_with_underscores",
            "/path.with.dots"
        )

        result = resolve_extension_paths(paths, None)

        assert result == list(paths)

    def test_relative_paths_preserved(self):
        """Test that relative paths are preserved."""
        paths = ("./relative/path", "../parent/path", "current/path")

        result = resolve_extension_paths(paths, None)

        assert result == list(paths)

    def test_unicode_paths(self):
        """Test paths with Unicode characters."""
        paths = ("/путь/модули", "/路径/模块", "/パス/モジュール")

        result = resolve_extension_paths(paths, None)

        assert result == list(paths)

    def test_env_var_only_whitespace(self):
        """Test environment variable with only whitespace."""
        with patch.dict(os.environ, {"MLPY_EXTENSION_PATHS": "   :  :   "}):
            with patch('sys.platform', 'linux'):
                result = resolve_extension_paths(None, None)

        assert result == []

    def test_single_path_no_separator(self):
        """Test environment variable with single path (no separators)."""
        with patch.dict(os.environ, {"MLPY_EXTENSION_PATHS": "/single/path"}):
            with patch('sys.platform', 'linux'):
                result = resolve_extension_paths(None, None)

        assert result == ["/single/path"]


class TestIntegrationScenarios:
    """Test realistic integration scenarios."""

    def test_typical_development_workflow(self, tmp_path):
        """Test typical developer workflow with extension paths."""
        # 1. Create project with config
        project_dir = tmp_path / "myproject"
        project_dir.mkdir()

        manager = MLProjectManager()
        manager.project_root = project_dir
        manager.config = MLProjectConfig(
            name="myproject",
            python_extension_paths=["./extensions", "./custom_modules"]
        )

        # 2. Developer overrides with CLI flag
        cli_override = ("/tmp/test_modules",)

        result = resolve_extension_paths(cli_override, manager)

        # CLI should override config
        assert result == list(cli_override)

        # 3. No CLI flag, use config
        result = resolve_extension_paths(None, manager)

        assert result == ["./extensions", "./custom_modules"]

    def test_ci_environment_workflow(self, tmp_path):
        """Test CI/CD environment with environment variable."""
        # CI sets environment variable
        ci_paths = "/ci/shared/extensions:/ci/project/modules"

        with patch.dict(os.environ, {"MLPY_EXTENSION_PATHS": ci_paths}):
            with patch('sys.platform', 'linux'):
                result = resolve_extension_paths(None, None)

        assert result == ["/ci/shared/extensions", "/ci/project/modules"]

    def test_team_shared_config(self, tmp_path):
        """Test team using shared config file."""
        # Team commits mlpy.json with shared extension paths
        config_file = tmp_path / "mlpy.json"

        manager = MLProjectManager()
        manager.project_root = tmp_path
        manager.config = MLProjectConfig(
            name="team-project",
            python_extension_paths=[
                "./shared/extensions",
                "./team/modules"
            ]
        )
        manager.save_config(config_file)

        # Another developer loads the config
        manager2 = MLProjectManager()
        manager2.load_config(config_file)

        result = resolve_extension_paths(None, manager2)

        assert result == ["./shared/extensions", "./team/modules"]
