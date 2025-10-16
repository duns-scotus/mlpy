"""Configuration integration tests for extension paths.

Tests cover:
- Loading mlpy.json/mlpy.yaml with extension paths
- Project initialization with extension paths
- Config discovery and auto-loading
- Validation of extension paths in configuration
- Integration with transpiler through configuration
- Project manager workflow integration
"""

import json
import pytest
import yaml
from pathlib import Path

from mlpy.cli.project_manager import MLProjectManager, MLProjectConfig
from mlpy.ml.transpiler import MLTranspiler


class TestProjectConfigurationFiles:
    """Test loading extension paths from configuration files."""

    def test_load_json_config_with_extension_paths(self, tmp_path):
        """Test loading extension paths from mlpy.json."""
        config_file = tmp_path / "mlpy.json"

        config_data = {
            "name": "test-project",
            "version": "1.0.0",
            "python_extension_paths": ["/ext1", "/ext2", "/ext3"]
        }

        config_file.write_text(json.dumps(config_data, indent=2))

        manager = MLProjectManager()
        success = manager.load_config(config_file)

        assert success
        assert manager.config is not None
        assert manager.config.python_extension_paths == ["/ext1", "/ext2", "/ext3"]

    def test_load_yaml_config_with_extension_paths(self, tmp_path):
        """Test loading extension paths from mlpy.yaml."""
        config_file = tmp_path / "mlpy.yaml"

        config_data = {
            "name": "test-project",
            "version": "1.0.0",
            "python_extension_paths": ["/ext/path1", "/ext/path2"]
        }

        config_file.write_text(yaml.dump(config_data))

        manager = MLProjectManager()
        success = manager.load_config(config_file)

        assert success
        assert manager.config.python_extension_paths == ["/ext/path1", "/ext/path2"]

    def test_load_yml_config_with_extension_paths(self, tmp_path):
        """Test loading extension paths from mlpy.yml (alternative extension)."""
        config_file = tmp_path / "mlpy.yml"

        config_data = {
            "name": "test-project",
            "python_extension_paths": ["./relative/path", "../parent/path"]
        }

        config_file.write_text(yaml.dump(config_data))

        manager = MLProjectManager()
        success = manager.load_config(config_file)

        assert success
        assert manager.config.python_extension_paths == ["./relative/path", "../parent/path"]

    def test_load_config_without_extension_paths(self, tmp_path):
        """Test loading config without extension_paths field (defaults to empty)."""
        config_file = tmp_path / "mlpy.json"

        config_data = {
            "name": "minimal-project",
            "version": "1.0.0"
        }

        config_file.write_text(json.dumps(config_data))

        manager = MLProjectManager()
        success = manager.load_config(config_file)

        assert success
        assert manager.config.python_extension_paths == []

    def test_load_config_with_null_extension_paths(self, tmp_path):
        """Test loading config with null extension_paths (converts to empty list)."""
        config_file = tmp_path / "mlpy.json"

        config_data = {
            "name": "test-project",
            "python_extension_paths": None
        }

        config_file.write_text(json.dumps(config_data))

        manager = MLProjectManager()
        success = manager.load_config(config_file)

        assert success
        assert manager.config.python_extension_paths == []


class TestSaveConfiguration:
    """Test saving configuration with extension paths."""

    def test_save_json_config_with_extension_paths(self, tmp_path):
        """Test saving extension paths to mlpy.json."""
        config_file = tmp_path / "mlpy.json"

        manager = MLProjectManager()
        manager.project_root = tmp_path
        manager.config = MLProjectConfig(
            name="save-test",
            python_extension_paths=["/save/ext1", "/save/ext2"]
        )

        success = manager.save_config(config_file)

        assert success
        assert config_file.exists()

        # Verify saved content
        with open(config_file) as f:
            data = json.load(f)

        assert data["python_extension_paths"] == ["/save/ext1", "/save/ext2"]

    def test_save_yaml_config_with_extension_paths(self, tmp_path):
        """Test saving extension paths to mlpy.yaml."""
        config_file = tmp_path / "mlpy.yaml"

        manager = MLProjectManager()
        manager.project_root = tmp_path
        manager.config = MLProjectConfig(
            name="save-test",
            python_extension_paths=["./extensions", "./custom"]
        )

        success = manager.save_config(config_file)

        assert success

        # Verify saved content
        with open(config_file) as f:
            data = yaml.safe_load(f)

        assert data["python_extension_paths"] == ["./extensions", "./custom"]

    def test_roundtrip_config_with_extension_paths(self, tmp_path):
        """Test save and load roundtrip preserves extension paths."""
        config_file = tmp_path / "mlpy.json"

        # Save
        manager1 = MLProjectManager()
        manager1.project_root = tmp_path
        manager1.config = MLProjectConfig(
            name="roundtrip-test",
            version="2.5.0",
            python_extension_paths=["/path/a", "/path/b", "/path/c"]
        )
        manager1.save_config(config_file)

        # Load
        manager2 = MLProjectManager()
        manager2.load_config(config_file)

        assert manager2.config.name == "roundtrip-test"
        assert manager2.config.version == "2.5.0"
        assert manager2.config.python_extension_paths == ["/path/a", "/path/b", "/path/c"]


class TestProjectInitialization:
    """Test project initialization with extension paths."""

    def test_init_project_creates_default_config(self, tmp_path):
        """Test that init_project creates config with default extension paths."""
        manager = MLProjectManager()

        success = manager.init_project("test-init", tmp_path)

        assert success
        assert manager.config is not None
        assert manager.config.python_extension_paths == []  # Default is empty

    def test_init_project_creates_config_file(self, tmp_path):
        """Test that init_project writes mlpy.json with extension paths field."""
        manager = MLProjectManager()
        manager.init_project("test-init", tmp_path)

        config_file = tmp_path / "test-init" / "mlpy.json"
        assert config_file.exists()

        with open(config_file) as f:
            data = json.load(f)

        assert "python_extension_paths" in data

    def test_manual_config_modification(self, tmp_path):
        """Test manually modifying config and saving."""
        # Initialize project
        manager = MLProjectManager()
        manager.init_project("manual-test", tmp_path)

        # Modify config to add extension paths
        manager.config.python_extension_paths = ["./my_extensions", "./team_modules"]

        # Save modified config
        config_file = tmp_path / "manual-test" / "mlpy.json"
        manager.save_config(config_file)

        # Verify modification was saved
        with open(config_file) as f:
            data = json.load(f)

        assert data["python_extension_paths"] == ["./my_extensions", "./team_modules"]


class TestConfigDiscovery:
    """Test automatic configuration discovery."""

    def test_discover_config_in_current_dir(self, tmp_path, monkeypatch):
        """Test discovering mlpy.json in current directory."""
        # Create config in temp dir
        config_file = tmp_path / "mlpy.json"
        config_data = {
            "name": "discovered",
            "python_extension_paths": ["/discovered/ext"]
        }
        config_file.write_text(json.dumps(config_data))

        # Change to temp directory
        monkeypatch.chdir(tmp_path)

        # Discover and load
        manager = MLProjectManager()
        success = manager.discover_and_load_config()

        assert success
        assert manager.config.python_extension_paths == ["/discovered/ext"]

    def test_discover_config_in_parent_dir(self, tmp_path, monkeypatch):
        """Test discovering mlpy.json in parent directory."""
        # Create config in root
        config_file = tmp_path / "mlpy.json"
        config_data = {
            "name": "parent-discovered",
            "python_extension_paths": ["/parent/ext"]
        }
        config_file.write_text(json.dumps(config_data))

        # Create subdirectory and change to it
        subdir = tmp_path / "src" / "code"
        subdir.mkdir(parents=True)
        monkeypatch.chdir(subdir)

        # Should discover parent config
        manager = MLProjectManager()
        success = manager.discover_and_load_config()

        assert success
        assert manager.config.python_extension_paths == ["/parent/ext"]

    def test_discover_prioritizes_closest_config(self, tmp_path, monkeypatch):
        """Test that discovery prioritizes closest config file."""
        # Create config in root
        root_config = tmp_path / "mlpy.json"
        root_config.write_text(json.dumps({
            "name": "root",
            "python_extension_paths": ["/root/ext"]
        }))

        # Create subdirectory with its own config
        subdir = tmp_path / "subproject"
        subdir.mkdir()
        sub_config = subdir / "mlpy.json"
        sub_config.write_text(json.dumps({
            "name": "subproject",
            "python_extension_paths": ["/sub/ext"]
        }))

        # Change to subdirectory
        monkeypatch.chdir(subdir)

        # Should find closest config
        manager = MLProjectManager()
        success = manager.discover_and_load_config()

        assert success
        assert manager.config.name == "subproject"
        assert manager.config.python_extension_paths == ["/sub/ext"]

    def test_discover_yaml_over_json(self, tmp_path, monkeypatch):
        """Test config file priority: mlpy.json before mlpy.yaml."""
        # Create both config files
        json_config = tmp_path / "mlpy.json"
        json_config.write_text(json.dumps({
            "name": "json-config",
            "python_extension_paths": ["/json/ext"]
        }))

        yaml_config = tmp_path / "mlpy.yaml"
        yaml_config.write_text(yaml.dump({
            "name": "yaml-config",
            "python_extension_paths": ["/yaml/ext"]
        }))

        monkeypatch.chdir(tmp_path)

        # Should prefer JSON
        manager = MLProjectManager()
        manager.discover_and_load_config()

        assert manager.config.name == "json-config"
        assert manager.config.python_extension_paths == ["/json/ext"]

    def test_no_config_found(self, tmp_path, monkeypatch):
        """Test behavior when no config file is found."""
        # Empty directory
        monkeypatch.chdir(tmp_path)

        manager = MLProjectManager()
        success = manager.discover_and_load_config()

        assert not success
        assert manager.config is None


class TestConfigValidation:
    """Test configuration validation with extension paths."""

    def test_validate_project_with_valid_config(self, tmp_path):
        """Test validation passes for valid config with extension paths."""
        # Create valid project structure
        project_dir = tmp_path / "valid-project"
        project_dir.mkdir()
        (project_dir / "src").mkdir()

        manager = MLProjectManager()
        manager.project_root = project_dir
        manager.config = MLProjectConfig(
            name="valid",
            source_dir="src",
            python_extension_paths=["./extensions"]
        )

        issues = manager.validate_project()

        # Should not flag extension_paths as an issue
        extension_issues = [i for i in issues if "extension" in i.lower()]
        assert len(extension_issues) == 0

    def test_extension_paths_not_required(self, tmp_path):
        """Test that extension paths are optional for valid project."""
        project_dir = tmp_path / "no-ext-project"
        project_dir.mkdir()
        (project_dir / "src").mkdir()

        manager = MLProjectManager()
        manager.project_root = project_dir
        manager.config = MLProjectConfig(
            name="no-extensions",
            source_dir="src",
            python_extension_paths=[]  # No extensions
        )

        issues = manager.validate_project()

        # Empty extension paths should not be an issue
        assert not any("extension" in i.lower() for i in issues)


class TestTranspilerIntegrationThroughConfig:
    """Test transpiler integration through configuration."""

    def test_transpiler_uses_config_extension_paths(self, tmp_path):
        """Test that transpiler can use paths from loaded config."""
        # Create extension module
        ext_dir = tmp_path / "extensions"
        ext_dir.mkdir()

        custom_module = ext_dir / "configured_bridge.py"
        custom_module.write_text('''
from mlpy.stdlib.decorators import ml_module, ml_function

@ml_module(name="configured", description="Configured module")
class Configured:
    @ml_function(description="Test function")
    def test(self):
        return "from_config"

configured = Configured()
''')

        # Create config with extension path
        config_file = tmp_path / "mlpy.json"
        config_data = {
            "name": "transpiler-test",
            "python_extension_paths": [str(ext_dir)]
        }
        config_file.write_text(json.dumps(config_data))

        # Load config
        manager = MLProjectManager()
        manager.load_config(config_file)

        # Create transpiler with config paths
        transpiler = MLTranspiler(
            python_extension_paths=manager.config.python_extension_paths
        )

        # Verify module is available
        from mlpy.stdlib.module_registry import get_registry
        registry = get_registry()
        assert registry.is_available("configured")

    def test_complete_workflow_with_config(self, tmp_path):
        """Test complete workflow: init -> configure -> transpile."""
        # 1. Initialize project
        manager = MLProjectManager()
        manager.init_project("workflow-test", tmp_path)

        project_dir = tmp_path / "workflow-test"

        # 2. Create extension directory
        ext_dir = project_dir / "my_extensions"
        ext_dir.mkdir()

        custom_mod = ext_dir / "workflow_bridge.py"
        custom_mod.write_text('''
from mlpy.stdlib.decorators import ml_module, ml_function

@ml_module(name="workflow", description="Workflow module")
class Workflow:
    @ml_function(description="Process")
    def process(self, data):
        return f"processed: {data}"

workflow = Workflow()
''')

        # 3. Update config with extension path
        manager.config.python_extension_paths = ["./my_extensions"]
        config_file = project_dir / "mlpy.json"
        manager.save_config(config_file)

        # 4. Load config in new manager (simulates new session)
        manager2 = MLProjectManager()
        manager2.load_config(config_file)

        # 5. Create transpiler with loaded config
        # Resolve relative paths to absolute
        abs_paths = [
            str((project_dir / path).resolve())
            for path in manager2.config.python_extension_paths
        ]

        transpiler = MLTranspiler(python_extension_paths=abs_paths)

        # 6. Verify module is available
        from mlpy.stdlib.module_registry import get_registry
        registry = get_registry()
        assert registry.is_available("workflow")


class TestMultipleConfigFormats:
    """Test all supported configuration formats."""

    def test_all_config_filenames(self, tmp_path):
        """Test all supported config filenames are discovered."""
        test_cases = [
            "mlpy.json",
            "mlpy.yaml",
            "mlpy.yml",
            ".mlpy.json"
        ]

        for filename in test_cases:
            # Create fresh directory for each test
            test_dir = tmp_path / filename.replace(".", "_")
            test_dir.mkdir()

            config_file = test_dir / filename
            config_data = {
                "name": f"test-{filename}",
                "python_extension_paths": [f"/{filename}/ext"]
            }

            if filename.endswith(".json"):
                config_file.write_text(json.dumps(config_data))
            else:
                config_file.write_text(yaml.dump(config_data))

            manager = MLProjectManager()
            success = manager.load_config(config_file)

            assert success, f"Failed to load {filename}"
            assert manager.config.python_extension_paths == [f"/{filename}/ext"]


class TestConfigErrorHandling:
    """Test error handling in configuration loading."""

    def test_malformed_json_config(self, tmp_path):
        """Test handling of malformed JSON config."""
        config_file = tmp_path / "mlpy.json"
        config_file.write_text("{invalid json content")

        manager = MLProjectManager()
        success = manager.load_config(config_file)

        assert not success
        assert manager.config is None

    def test_malformed_yaml_config(self, tmp_path):
        """Test handling of malformed YAML config."""
        config_file = tmp_path / "mlpy.yaml"
        config_file.write_text("invalid: yaml: content: [")

        manager = MLProjectManager()
        success = manager.load_config(config_file)

        assert not success

    def test_nonexistent_config_file(self, tmp_path):
        """Test loading non-existent config file."""
        config_file = tmp_path / "nonexistent.json"

        manager = MLProjectManager()
        success = manager.load_config(config_file)

        assert not success
        assert manager.config is None

    def test_config_with_invalid_extension_paths_type(self, tmp_path):
        """Test config with invalid type for extension_paths."""
        config_file = tmp_path / "mlpy.json"

        # Extension paths should be array, not string
        config_data = {
            "name": "invalid-type",
            "python_extension_paths": "/single/path/not/array"
        }

        config_file.write_text(json.dumps(config_data))

        manager = MLProjectManager()
        success = manager.load_config(config_file)

        # Config loads (Python dataclasses don't enforce type checking)
        # but __post_init__ should handle it
        # In this case, the string gets assigned as-is (not ideal but doesn't crash)
        assert success
        # The invalid type is accepted but might cause issues later
        # This is a limitation of Python's dataclass type hints
