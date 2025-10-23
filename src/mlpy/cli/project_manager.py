"""
ML Project Manager
Handles project configuration, initialization, and management tasks.
"""

import json
from dataclasses import asdict, dataclass
from pathlib import Path

import yaml


@dataclass
class MLProjectConfig:
    """Configuration for an ML project."""

    name: str = "ml-project"
    version: str = "1.0.0"
    description: str = ""
    author: str = ""
    license: str = "MIT"

    # Source configuration
    source_dir: str = "src"
    output_dir: str = "dist"
    test_dir: str = "tests"

    # Compilation settings
    target: str = "python"
    optimization_level: int = 1
    source_maps: bool = True

    # Security settings
    enable_security_analysis: bool = True
    security_level: str = "strict"  # strict, normal, permissive
    allowed_capabilities: list[str] = None

    # Python extension modules
    python_extension_paths: list[str] = None

    # ML module paths (for ML source modules)
    ml_module_paths: list[str] = None

    # Development settings
    watch_patterns: list[str] = None
    auto_format: bool = True
    lint_on_save: bool = True

    # Documentation settings
    doc_source: str = "docs/source"
    doc_output: str = "docs/build"
    doc_theme: str = "sphinx_rtd_theme"

    # Testing settings
    test_pattern: str = "**/test_*.ml"
    test_timeout: int = 30
    coverage_threshold: float = 0.8

    def __post_init__(self):
        """Initialize default values."""
        if self.allowed_capabilities is None:
            self.allowed_capabilities = ["file_read", "file_write", "network"]

        if self.python_extension_paths is None:
            self.python_extension_paths = []

        if self.ml_module_paths is None:
            self.ml_module_paths = []

        if self.watch_patterns is None:
            self.watch_patterns = ["**/*.ml", "**/*.py"]


class MLProjectManager:
    """Manages ML projects and their configurations."""

    def __init__(self):
        self.project_root: Path | None = None
        self.config: MLProjectConfig | None = None
        self.config_file: Path | None = None

    def set_project_root(self, root: Path) -> None:
        """Set the project root directory."""
        self.project_root = Path(root).resolve()

    def discover_project_root(self) -> Path | None:
        """Discover project root by looking for config files."""
        current = Path.cwd()

        config_files = ["mlpy.json", "mlpy.yaml", "mlpy.yml", ".mlpy.json"]

        # Search upward from current directory
        while current != current.parent:
            for config_file in config_files:
                if (current / config_file).exists():
                    return current
            current = current.parent

        return None

    def discover_and_load_config(self) -> bool:
        """Discover and load project configuration."""
        if not self.project_root:
            self.project_root = self.discover_project_root()

        if not self.project_root:
            return False

        config_files = [
            self.project_root / "mlpy.json",
            self.project_root / "mlpy.yaml",
            self.project_root / "mlpy.yml",
            self.project_root / ".mlpy.json",
        ]

        for config_file in config_files:
            if config_file.exists():
                return self.load_config(config_file)

        return False

    def load_config(self, config_file: Path) -> bool:
        """Load configuration from file."""
        try:
            config_file = Path(config_file)
            self.config_file = config_file

            if not config_file.exists():
                return False

            with open(config_file, encoding="utf-8") as f:
                if config_file.suffix in [".yaml", ".yml"]:
                    data = yaml.safe_load(f)
                else:
                    data = json.load(f)

            # Create config object
            self.config = MLProjectConfig(**data)

            # Set project root if not already set
            if not self.project_root:
                self.project_root = config_file.parent

            return True

        except Exception as e:
            print(f"Error loading config from {config_file}: {e}")
            return False

    def save_config(self, config_file: Path | None = None) -> bool:
        """Save configuration to file."""
        if not self.config:
            return False

        if config_file is None:
            config_file = self.config_file or (self.project_root / "mlpy.json")

        try:
            config_file = Path(config_file)
            config_file.parent.mkdir(parents=True, exist_ok=True)

            data = asdict(self.config)

            with open(config_file, "w", encoding="utf-8") as f:
                if config_file.suffix in [".yaml", ".yml"]:
                    yaml.dump(data, f, default_flow_style=False, indent=2)
                else:
                    json.dump(data, f, indent=2)

            self.config_file = config_file
            return True

        except Exception as e:
            print(f"Error saving config to {config_file}: {e}")
            return False

    def init_project(self, project_name: str, project_dir: Path, template: str = "basic") -> bool:
        """Initialize a new ML project."""
        try:
            project_path = Path(project_dir) / project_name
            project_path.mkdir(parents=True, exist_ok=True)

            # Set project root
            self.project_root = project_path

            # Create default configuration
            self.config = MLProjectConfig(
                name=project_name, description=f"ML project: {project_name}"
            )

            # Create directory structure
            self._create_project_structure(template)

            # Save configuration
            self.save_config(project_path / "mlpy.json")

            # Create initial files
            self._create_initial_files(template)

            print(f"Successfully created ML project '{project_name}' in {project_path}")
            return True

        except Exception as e:
            print(f"Error creating project: {e}")
            return False

    def _create_project_structure(self, template: str) -> None:
        """Create project directory structure."""
        if not self.project_root or not self.config:
            return

        # Core directories
        dirs = [
            self.config.source_dir,
            self.config.output_dir,
            self.config.test_dir,
            "docs",
            "examples",
            ".mlpy",
        ]

        for dir_name in dirs:
            (self.project_root / dir_name).mkdir(parents=True, exist_ok=True)

        # Template-specific directories
        if template == "web":
            (self.project_root / "static").mkdir(exist_ok=True)
            (self.project_root / "templates").mkdir(exist_ok=True)
        elif template == "cli":
            (self.project_root / "bin").mkdir(exist_ok=True)
        elif template == "library":
            (self.project_root / "lib").mkdir(exist_ok=True)

    def _create_initial_files(self, template: str) -> None:
        """Create initial project files."""
        if not self.project_root or not self.config:
            return

        # Main ML file
        main_file = self.project_root / self.config.source_dir / "main.ml"
        if template == "basic":
            main_content = """// Main ML program
function main() {
    message = "Hello, ML World!"
    print(message)
}

main()
"""
        elif template == "web":
            main_content = """// Web application example
import { HttpServer } from "std/http"

function createApp() {
    server = HttpServer.create(8080)

    server.get("/", function(req, res) {
        res.html("<h1>Hello, ML Web!</h1>")
    })

    return server
}

app = createApp()
app.listen()
print("Server running on http://localhost:8080")
"""
        elif template == "cli":
            main_content = """// CLI application example
import { Args } from "std/cli"

function main() {
    args = Args.parse()

    if (args.length == 0) {
        print("Usage: mlpy run main.ml <command>")
        return
    }

    command = args[0]
    print("Running command: " + command)
}

main()
"""
        else:
            main_content = """// Basic ML program
print("Hello, World!")
"""

        main_file.write_text(main_content)

        # Test file
        test_file = self.project_root / self.config.test_dir / "test_main.ml"
        test_content = """// Test file example
import { assert } from "std/testing"

function test_basic() {
    result = 2 + 2
    assert.equal(result, 4, "Basic arithmetic should work")
}

test_basic()
print("All tests passed!")
"""
        test_file.write_text(test_content)

        # README
        readme_file = self.project_root / "README.md"
        readme_content = f"""# {self.config.name}

{self.config.description}

## Getting Started

### Prerequisites
- mlpy v2.0.0 or later

### Installation
```bash
# Clone or create the project
mlpy init {self.config.name}
cd {self.config.name}
```

### Running
```bash
# Compile and run
mlpy run {self.config.source_dir}/main.ml

# Run tests
mlpy test

# Start development server
mlpy watch {self.config.source_dir}/
```

### Building
```bash
# Build for production
mlpy compile {self.config.source_dir}/main.ml --optimize

# Build documentation
mlpy doc build
```

## Project Structure
- `{self.config.source_dir}/` - ML source files
- `{self.config.test_dir}/` - Test files
- `{self.config.output_dir}/` - Compiled output
- `docs/` - Documentation
- `examples/` - Example code

## Security

This project uses mlpy's capability-based security system.
Capabilities are configured in `mlpy.json`.

Current allowed capabilities:
{self._format_capabilities_list()}

## License

{self.config.license}
"""
        readme_file.write_text(readme_content)

        # .gitignore
        gitignore_file = self.project_root / ".gitignore"
        gitignore_content = f"""# ML compilation output
{self.config.output_dir}/
*.pyc
__pycache__/

# Development files
.mlpy/cache/
.mlpy/logs/

# Documentation build
{self.config.doc_output}/

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Dependencies
node_modules/
venv/
.env
"""
        gitignore_file.write_text(gitignore_content)

    def _format_capabilities_list(self) -> str:
        """Format capabilities list for README."""
        if not self.config or not self.config.allowed_capabilities:
            return "- None"

        return "\n".join(f"- {cap}" for cap in self.config.allowed_capabilities)

    def get_source_files(self) -> list[Path]:
        """Get all ML source files in the project."""
        if not self.project_root or not self.config:
            return []

        source_dir = self.project_root / self.config.source_dir
        if not source_dir.exists():
            return []

        return list(source_dir.rglob("*.ml"))

    def get_test_files(self) -> list[Path]:
        """Get all test files in the project."""
        if not self.project_root or not self.config:
            return []

        test_dir = self.project_root / self.config.test_dir
        if not test_dir.exists():
            return []

        return list(test_dir.glob(self.config.test_pattern))

    def is_ml_project(self) -> bool:
        """Check if current directory is an ML project."""
        return self.config is not None and self.project_root is not None

    def get_output_dir(self) -> Path:
        """Get the output directory path."""
        if not self.project_root or not self.config:
            return Path("dist")

        return self.project_root / self.config.output_dir

    def get_cache_dir(self) -> Path:
        """Get the cache directory path."""
        if not self.project_root:
            return Path.home() / ".mlpy" / "cache"

        return self.project_root / ".mlpy" / "cache"

    def clean_project(self) -> bool:
        """Clean project build artifacts."""
        try:
            import shutil

            if self.project_root and self.config:
                # Clean output directory
                output_dir = self.project_root / self.config.output_dir
                if output_dir.exists():
                    shutil.rmtree(output_dir)

                # Clean cache
                cache_dir = self.get_cache_dir()
                if cache_dir.exists():
                    shutil.rmtree(cache_dir)

                print("Project cleaned successfully")
                return True

        except Exception as e:
            print(f"Error cleaning project: {e}")

        return False

    def validate_project(self) -> list[str]:
        """Validate project configuration and structure."""
        issues = []

        if not self.is_ml_project():
            issues.append("Not a valid ML project (missing configuration)")
            return issues

        # Check required directories
        required_dirs = [self.config.source_dir]
        for dir_name in required_dirs:
            dir_path = self.project_root / dir_name
            if not dir_path.exists():
                issues.append(f"Missing required directory: {dir_name}")

        # Check for ML source files
        source_files = self.get_source_files()
        if not source_files:
            issues.append(f"No ML source files found in {self.config.source_dir}/")

        # Validate configuration
        if not self.config.name:
            issues.append("Project name is required")

        if self.config.security_level not in ["strict", "normal", "permissive"]:
            issues.append(f"Invalid security level: {self.config.security_level}")

        return issues
