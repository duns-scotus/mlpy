"""CLI import configuration for ML module resolution."""

import os
from pathlib import Path
from typing import List, Optional

from mlpy.ml.resolution.resolver import ModuleResolver, get_default_resolver, set_default_resolver
from mlpy.runtime.capabilities.manager import get_capability_manager
from mlpy.stdlib.registry import get_stdlib_registry


class ImportConfiguration:
    """Configuration for ML import system."""

    def __init__(self,
                 import_paths: List[str] = None,
                 allow_current_dir: bool = False,
                 stdlib_mode: str = "native",
                 python_whitelist: List[str] = None):
        """Initialize import configuration.

        Args:
            import_paths: List of directories to search for modules
            allow_current_dir: Whether to allow imports from current directory
            stdlib_mode: Standard library mode ("native" or "python")
            python_whitelist: Additional Python modules to allow
        """
        self.import_paths = import_paths or []
        self.allow_current_dir = allow_current_dir
        self.stdlib_mode = stdlib_mode
        self.python_whitelist = python_whitelist or []

        # Validate configuration
        self._validate_config()

    def _validate_config(self) -> None:
        """Validate import configuration."""
        # Validate import paths
        valid_paths = []
        for path in self.import_paths:
            abs_path = os.path.abspath(path)
            if os.path.isdir(abs_path):
                valid_paths.append(abs_path)
            else:
                print(f"Warning: Import path '{path}' does not exist or is not a directory")

        self.import_paths = valid_paths

        # Validate stdlib mode
        if self.stdlib_mode not in ["native", "python"]:
            raise ValueError(f"Invalid stdlib_mode: {self.stdlib_mode}. Must be 'native' or 'python'")

    def create_resolver(self) -> ModuleResolver:
        """Create a module resolver with this configuration.

        Returns:
            Configured ModuleResolver instance
        """
        capability_manager = get_capability_manager()

        resolver = ModuleResolver(
            import_paths=self.import_paths,
            capability_manager=capability_manager,
            allow_current_dir=self.allow_current_dir
        )

        # Configure Python whitelist if in python mode
        if self.stdlib_mode == "python":
            # Add configured python modules to whitelist
            resolver.python_whitelist.update(self.python_whitelist)

        return resolver

    def apply_global_config(self) -> None:
        """Apply this configuration as the global default."""
        resolver = self.create_resolver()
        set_default_resolver(resolver)

    def get_config_summary(self) -> dict:
        """Get configuration summary for display."""
        return {
            "import_paths": self.import_paths,
            "import_paths_count": len(self.import_paths),
            "allow_current_dir": self.allow_current_dir,
            "stdlib_mode": self.stdlib_mode,
            "python_whitelist": self.python_whitelist,
            "python_whitelist_count": len(self.python_whitelist)
        }


def parse_import_paths(paths_string: str) -> List[str]:
    """Parse colon-separated import paths string.

    Args:
        paths_string: Colon-separated paths (e.g., "./modules:./lib")

    Returns:
        List of paths
    """
    if not paths_string:
        return []

    # Support both colon and semicolon separators for cross-platform compatibility
    if ';' in paths_string and ':' not in paths_string:
        separator = ';'
    else:
        separator = ':'

    paths = [path.strip() for path in paths_string.split(separator)]
    return [path for path in paths if path]  # Filter out empty strings


def validate_import_paths(paths: List[str]) -> List[str]:
    """Validate and normalize import paths.

    Args:
        paths: List of paths to validate

    Returns:
        List of valid, absolute paths
    """
    valid_paths = []

    for path in paths:
        try:
            abs_path = os.path.abspath(path)

            # Security check: ensure path exists and is a directory
            if not os.path.exists(abs_path):
                print(f"Warning: Import path '{path}' does not exist")
                continue

            if not os.path.isdir(abs_path):
                print(f"Warning: Import path '{path}' is not a directory")
                continue

            # Security check: ensure path is readable
            if not os.access(abs_path, os.R_OK):
                print(f"Warning: Import path '{path}' is not readable")
                continue

            valid_paths.append(abs_path)

        except (OSError, IOError) as e:
            print(f"Warning: Cannot access import path '{path}': {e}")

    return valid_paths


def create_import_config_from_cli(import_paths: Optional[str] = None,
                                  allow_current_dir: bool = False,
                                  stdlib_mode: str = "native",
                                  allow_python_modules: Optional[str] = None) -> ImportConfiguration:
    """Create import configuration from CLI arguments.

    Args:
        import_paths: Colon-separated import paths
        allow_current_dir: Whether to allow current directory imports
        stdlib_mode: Standard library mode
        allow_python_modules: Comma-separated additional Python modules

    Returns:
        ImportConfiguration instance
    """
    # Parse import paths
    paths = parse_import_paths(import_paths) if import_paths else []
    validated_paths = validate_import_paths(paths)

    # Parse Python whitelist
    python_modules = []
    if allow_python_modules:
        python_modules = [mod.strip() for mod in allow_python_modules.split(',')]
        python_modules = [mod for mod in python_modules if mod]  # Filter empty

    return ImportConfiguration(
        import_paths=validated_paths,
        allow_current_dir=allow_current_dir,
        stdlib_mode=stdlib_mode,
        python_whitelist=python_modules
    )


def get_default_import_config() -> ImportConfiguration:
    """Get secure default import configuration.

    Returns:
        Default ImportConfiguration with no file system access
    """
    return ImportConfiguration(
        import_paths=[],  # No file system access by default
        allow_current_dir=False,  # Don't allow current directory access
        stdlib_mode="native",  # Use native ML standard library
        python_whitelist=[]  # No additional Python modules
    )


def apply_import_config(config: ImportConfiguration) -> None:
    """Apply import configuration globally.

    Args:
        config: ImportConfiguration to apply
    """
    # Apply to module resolver
    config.apply_global_config()

    # Initialize standard library registry if using native mode
    if config.stdlib_mode == "native":
        registry = get_stdlib_registry()
        # Registry is auto-initialized with core modules


def print_import_config(config: ImportConfiguration) -> None:
    """Print import configuration summary.

    Args:
        config: ImportConfiguration to display
    """
    summary = config.get_config_summary()

    print("Import Configuration:")
    print(f"  Standard Library Mode: {summary['stdlib_mode']}")
    print(f"  Import Paths ({summary['import_paths_count']}):")

    if summary['import_paths']:
        for path in summary['import_paths']:
            print(f"    - {path}")
    else:
        print("    (none - file system imports disabled)")

    print(f"  Current Directory Access: {summary['allow_current_dir']}")

    if summary['python_whitelist']:
        print(f"  Additional Python Modules ({summary['python_whitelist_count']}):")
        for module in summary['python_whitelist']:
            print(f"    - {module}")
    else:
        print("  Additional Python Modules: (none)")