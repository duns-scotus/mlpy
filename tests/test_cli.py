"""
Unit tests for ML CLI application.
Tests CLI commands, project management, and configuration handling.
"""

import json
import shutil
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
import yaml

from src.mlpy.cli.main import MLCLIApp
from src.mlpy.cli.project_manager import MLProjectConfig, MLProjectManager


class TestMLProjectConfig:
    """Test ML project configuration."""

    def test_default_config(self):
        """Test default configuration values."""
        config = MLProjectConfig()

        assert config.name == "ml-project"
        assert config.version == "1.0.0"
        assert config.source_dir == "src"
        assert config.output_dir == "dist"
        assert config.test_dir == "tests"
        assert config.target == "python"
        assert config.enable_security_analysis is True
        assert config.security_level == "strict"

    def test_post_init_defaults(self):
        """Test post-initialization default values."""
        config = MLProjectConfig()

        assert config.allowed_capabilities == ["file_read", "file_write", "network"]
        assert config.watch_patterns == ["**/*.ml", "**/*.py"]

    def test_custom_config(self):
        """Test configuration with custom values."""
        config = MLProjectConfig(
            name="my-project",
            version="2.0.0",
            security_level="normal",
            allowed_capabilities=["file_read"],
        )

        assert config.name == "my-project"
        assert config.version == "2.0.0"
        assert config.security_level == "normal"
        assert config.allowed_capabilities == ["file_read"]


class TestMLProjectManager:
    """Test ML project manager functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.project_manager = MLProjectManager()
        self.temp_dir = Path(tempfile.mkdtemp())

    def teardown_method(self):
        """Clean up test fixtures."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_set_project_root(self):
        """Test setting project root directory."""
        test_path = Path("/test/path")
        self.project_manager.set_project_root(test_path)

        assert self.project_manager.project_root == test_path.resolve()

    def test_load_json_config(self):
        """Test loading JSON configuration."""
        config_file = self.temp_dir / "mlpy.json"
        config_data = {"name": "test-project", "version": "1.0.0", "security_level": "normal"}

        config_file.write_text(json.dumps(config_data))

        success = self.project_manager.load_config(config_file)
        assert success is True
        assert self.project_manager.config.name == "test-project"
        assert self.project_manager.config.security_level == "normal"

    def test_load_yaml_config(self):
        """Test loading YAML configuration."""
        config_file = self.temp_dir / "mlpy.yaml"
        config_data = {"name": "test-project", "version": "1.0.0", "source_dir": "source"}

        config_file.write_text(yaml.dump(config_data))

        success = self.project_manager.load_config(config_file)
        assert success is True
        assert self.project_manager.config.name == "test-project"
        assert self.project_manager.config.source_dir == "source"

    def test_load_nonexistent_config(self):
        """Test loading non-existent configuration file."""
        config_file = self.temp_dir / "nonexistent.json"

        success = self.project_manager.load_config(config_file)
        assert success is False

    def test_save_json_config(self):
        """Test saving JSON configuration."""
        self.project_manager.config = MLProjectConfig(name="test-project", version="1.0.0")

        config_file = self.temp_dir / "mlpy.json"
        success = self.project_manager.save_config(config_file)

        assert success is True
        assert config_file.exists()

        # Verify content
        data = json.loads(config_file.read_text())
        assert data["name"] == "test-project"
        assert data["version"] == "1.0.0"

    def test_save_yaml_config(self):
        """Test saving YAML configuration."""
        self.project_manager.config = MLProjectConfig(name="test-project", version="2.0.0")

        config_file = self.temp_dir / "mlpy.yaml"
        success = self.project_manager.save_config(config_file)

        assert success is True
        assert config_file.exists()

        # Verify content
        data = yaml.safe_load(config_file.read_text())
        assert data["name"] == "test-project"
        assert data["version"] == "2.0.0"

    def test_discover_project_root(self):
        """Test project root discovery."""
        # Create config file in temp directory
        config_file = self.temp_dir / "mlpy.json"
        config_file.write_text('{"name": "test"}')

        # Create subdirectory
        sub_dir = self.temp_dir / "sub" / "deeper"
        sub_dir.mkdir(parents=True)

        # Set current directory to subdirectory and discover
        original_cwd = Path.cwd()
        try:
            import os

            os.chdir(sub_dir)
            discovered_root = self.project_manager.discover_project_root()
            assert discovered_root == self.temp_dir
        finally:
            os.chdir(original_cwd)

    def test_init_basic_project(self):
        """Test initializing a basic project."""
        project_name = "test-project"
        success = self.project_manager.init_project(
            project_name=project_name, project_dir=self.temp_dir, template="basic"
        )

        assert success is True
        project_path = self.temp_dir / project_name

        # Check directory structure
        assert project_path.exists()
        assert (project_path / "src").exists()
        assert (project_path / "tests").exists()
        assert (project_path / "docs").exists()
        assert (project_path / "mlpy.json").exists()

        # Check files
        assert (project_path / "src" / "main.ml").exists()
        assert (project_path / "tests" / "test_main.ml").exists()
        assert (project_path / "README.md").exists()
        assert (project_path / ".gitignore").exists()

    def test_init_web_project(self):
        """Test initializing a web project template."""
        project_name = "web-project"
        success = self.project_manager.init_project(
            project_name=project_name, project_dir=self.temp_dir, template="web"
        )

        assert success is True
        project_path = self.temp_dir / project_name

        # Check web-specific directories
        assert (project_path / "static").exists()
        assert (project_path / "templates").exists()

        # Check main file contains web content
        main_file = project_path / "src" / "main.ml"
        content = main_file.read_text()
        assert "HttpServer" in content

    def test_init_cli_project(self):
        """Test initializing a CLI project template."""
        project_name = "cli-project"
        success = self.project_manager.init_project(
            project_name=project_name, project_dir=self.temp_dir, template="cli"
        )

        assert success is True
        project_path = self.temp_dir / project_name

        # Check CLI-specific directories
        assert (project_path / "bin").exists()

        # Check main file contains CLI content
        main_file = project_path / "src" / "main.ml"
        content = main_file.read_text()
        assert "Args" in content

    def test_get_source_files(self):
        """Test getting source files from project."""
        # Initialize project
        self.project_manager.init_project("test-project", self.temp_dir, "basic")
        project_path = self.temp_dir / "test-project"

        # Create additional ML files
        src_dir = project_path / "src"
        (src_dir / "utils.ml").write_text("// Utils")
        (src_dir / "subdir").mkdir()
        (src_dir / "subdir" / "helper.ml").write_text("// Helper")

        self.project_manager.set_project_root(project_path)
        self.project_manager.config = MLProjectConfig()

        source_files = self.project_manager.get_source_files()

        # Should find all .ml files
        assert len(source_files) >= 3  # main.ml, utils.ml, helper.ml
        file_names = [f.name for f in source_files]
        assert "main.ml" in file_names
        assert "utils.ml" in file_names
        assert "helper.ml" in file_names

    def test_get_test_files(self):
        """Test getting test files from project."""
        # Initialize project
        self.project_manager.init_project("test-project", self.temp_dir, "basic")
        project_path = self.temp_dir / "test-project"

        self.project_manager.set_project_root(project_path)
        self.project_manager.config = MLProjectConfig()

        test_files = self.project_manager.get_test_files()

        # Should find test files
        assert len(test_files) >= 1
        assert any("test_main.ml" in str(f) for f in test_files)

    def test_is_ml_project(self):
        """Test ML project detection."""
        # Not a project initially
        assert self.project_manager.is_ml_project() is False

        # Set up project
        self.project_manager.config = MLProjectConfig()
        self.project_manager.project_root = self.temp_dir

        assert self.project_manager.is_ml_project() is True

    def test_clean_project(self):
        """Test project cleaning functionality."""
        # Initialize project
        self.project_manager.init_project("test-project", self.temp_dir, "basic")
        project_path = self.temp_dir / "test-project"

        self.project_manager.set_project_root(project_path)
        self.project_manager.config = MLProjectConfig()

        # Create some build artifacts
        (project_path / "dist").mkdir(exist_ok=True)
        (project_path / "dist" / "output.py").write_text("# Generated")
        (project_path / ".mlpy" / "cache").mkdir(parents=True, exist_ok=True)
        (project_path / ".mlpy" / "cache" / "cached.json").write_text("{}")

        # Clean project
        success = self.project_manager.clean_project()
        assert success is True

        # Artifacts should be gone
        assert not (project_path / "dist").exists()
        assert not (project_path / ".mlpy" / "cache").exists()

    def test_validate_project(self):
        """Test project validation."""
        # Initialize valid project
        self.project_manager.init_project("test-project", self.temp_dir, "basic")
        project_path = self.temp_dir / "test-project"

        self.project_manager.set_project_root(project_path)
        self.project_manager.discover_and_load_config()

        issues = self.project_manager.validate_project()
        assert len(issues) == 0  # Should be valid

        # Test invalid project
        invalid_manager = MLProjectManager()
        issues = invalid_manager.validate_project()
        assert len(issues) > 0
        assert "Not a valid ML project" in issues[0]

        # Test project with missing source directory
        (project_path / "src").rename(project_path / "src_backup")
        issues = self.project_manager.validate_project()
        assert len(issues) > 0
        assert "Missing required directory: src" in issues[0]


class TestMLCLIApp:
    """Test ML CLI application."""

    def setup_method(self):
        """Set up test fixtures."""
        self.cli_app = MLCLIApp()

    def test_cli_initialization(self):
        """Test CLI app initialization."""
        assert self.cli_app.project_manager is not None
        assert isinstance(self.cli_app.commands, dict)
        assert len(self.cli_app.commands) > 0

    def test_parser_creation(self):
        """Test argument parser creation."""
        parser = self.cli_app.create_parser()

        assert parser.prog == "mlpy"
        assert "ML Programming Language" in parser.description

    def test_logging_configuration(self):
        """Test logging configuration."""
        # Test quiet mode
        self.cli_app.configure_logging(verbosity=0, quiet=True)
        import logging

        assert self.cli_app.logger.level == logging.ERROR

        # Test verbose mode
        self.cli_app.configure_logging(verbosity=2, quiet=False)
        assert self.cli_app.logger.level == logging.DEBUG

    def test_command_registration(self):
        """Test that all expected commands are registered."""
        expected_commands = [
            "init",
            "compile",
            "run",
            "test",
            "analyze",
            "watch",
            "serve",
            "format",
            "doc",
            "lsp",
        ]

        for cmd in expected_commands:
            assert cmd in self.cli_app.commands

    @patch("sys.argv", ["mlpy", "--version"])
    def test_version_argument(self):
        """Test version argument handling."""
        parser = self.cli_app.create_parser()

        with pytest.raises(SystemExit) as exc_info:
            parser.parse_args(["--version"])

        # Should exit with code 0 for version
        assert exc_info.value.code == 0

    def test_run_with_no_command(self):
        """Test running CLI with no command."""
        result = self.cli_app.run([])
        assert result == 1  # Should return error code

    def test_run_with_unknown_command(self):
        """Test running CLI with unknown command."""
        # Mock commands to be empty for this test
        original_commands = self.cli_app.commands
        self.cli_app.commands = {}

        result = self.cli_app.run(["unknown"])
        assert result == 1  # Should return error code

        # Restore commands
        self.cli_app.commands = original_commands

    @patch("sys.argv", ["mlpy"])
    def test_banner_printing(self):
        """Test banner printing functionality."""
        # Test that banner method exists and is callable
        assert hasattr(self.cli_app, "print_banner")
        assert callable(self.cli_app.print_banner)

        # Test banner contains expected content
        import io
        import sys

        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            self.cli_app.print_banner()
            output = captured_output.getvalue()

            assert "mlpy" in output.lower() or "ML" in output
            assert "Security-First" in output or "security" in output.lower()
        finally:
            sys.stdout = sys.__stdout__

    def test_keyboard_interrupt_handling(self):
        """Test keyboard interrupt handling."""
        # Mock command that raises KeyboardInterrupt
        mock_command = Mock()
        mock_command.execute.side_effect = KeyboardInterrupt()

        self.cli_app.commands["test_cmd"] = mock_command

        result = self.cli_app.run(["test_cmd"])
        assert result == 130  # Standard SIGINT exit code

    def test_exception_handling(self):
        """Test general exception handling."""
        # Mock command that raises generic exception
        mock_command = Mock()
        mock_command.execute.side_effect = Exception("Test error")

        self.cli_app.commands["test_cmd"] = mock_command

        result = self.cli_app.run(["test_cmd"])
        assert result == 1  # General error code


class TestCLICommands:
    """Test individual CLI commands (mock-based since commands aren't fully implemented)."""

    def setup_method(self):
        """Set up test fixtures."""
        self.cli_app = MLCLIApp()

    def test_init_command_exists(self):
        """Test that init command exists."""
        assert "init" in self.cli_app.commands
        init_cmd = self.cli_app.commands["init"]
        assert hasattr(init_cmd, "execute")

    def test_compile_command_exists(self):
        """Test that compile command exists."""
        assert "compile" in self.cli_app.commands
        compile_cmd = self.cli_app.commands["compile"]
        assert hasattr(compile_cmd, "execute")

    def test_run_command_exists(self):
        """Test that run command exists."""
        assert "run" in self.cli_app.commands
        run_cmd = self.cli_app.commands["run"]
        assert hasattr(run_cmd, "execute")

    def test_all_commands_have_register_parser(self):
        """Test that all commands can register their parsers."""
        for cmd_name, cmd_obj in self.cli_app.commands.items():
            assert hasattr(
                cmd_obj, "register_parser"
            ), f"Command {cmd_name} missing register_parser"


@pytest.mark.integration
class TestCLIIntegration:
    """Integration tests for CLI functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.original_cwd = Path.cwd()

    def teardown_method(self):
        """Clean up test fixtures."""
        import os

        os.chdir(self.original_cwd)
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_project_workflow(self):
        """Test complete project workflow."""
        import os

        os.chdir(self.temp_dir)

        project_manager = MLProjectManager()

        # Initialize project
        success = project_manager.init_project("test-project", ".", "basic")
        assert success is True

        project_path = self.temp_dir / "test-project"
        os.chdir(project_path)

        # Discover configuration
        project_manager.set_project_root(project_path)
        config_found = project_manager.discover_and_load_config()
        assert config_found is True

        # Validate project
        issues = project_manager.validate_project()
        assert len(issues) == 0

        # Get files
        source_files = project_manager.get_source_files()
        assert len(source_files) > 0

        test_files = project_manager.get_test_files()
        assert len(test_files) > 0

    def test_configuration_discovery(self):
        """Test configuration file discovery in various locations."""
        import os

        # Create nested directory structure
        deep_dir = self.temp_dir / "a" / "b" / "c"
        deep_dir.mkdir(parents=True)

        # Place config at root level
        config_file = self.temp_dir / "mlpy.json"
        config_file.write_text('{"name": "root-project"}')

        # Change to deep directory and discover
        os.chdir(deep_dir)

        project_manager = MLProjectManager()
        root = project_manager.discover_project_root()

        assert root == self.temp_dir

    def test_multiple_config_formats(self):
        """Test handling of different configuration formats."""
        project_manager = MLProjectManager()

        # Test JSON config
        json_config = self.temp_dir / "mlpy.json"
        json_config.write_text('{"name": "json-project", "version": "1.0.0"}')

        success = project_manager.load_config(json_config)
        assert success is True
        assert project_manager.config.name == "json-project"

        # Test YAML config
        yaml_config = self.temp_dir / "mlpy.yaml"
        yaml_config.write_text("name: yaml-project\nversion: 2.0.0")

        success = project_manager.load_config(yaml_config)
        assert success is True
        assert project_manager.config.name == "yaml-project"
        assert project_manager.config.version == "2.0.0"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
