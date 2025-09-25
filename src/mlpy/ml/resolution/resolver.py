"""Module resolution engine with security validation."""

import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

from mlpy.ml.errors.exceptions import MLError, CWECategory
from mlpy.ml.grammar.ast_nodes import Program
from mlpy.ml.grammar.parser import parse_ml_code
from mlpy.runtime.capabilities.manager import CapabilityManager, get_capability_manager
from .cache import ModuleCache, get_module_cache

# Import stdlib registry (avoid circular import by importing lazily)
def get_stdlib_registry():
    from mlpy.stdlib.registry import get_stdlib_registry as _get_stdlib_registry
    return _get_stdlib_registry()


class ImportError(MLError):
    """ML import error with security context."""

    def __init__(self, message: str, module_path: str, search_paths: list[str], **kwargs):
        super().__init__(
            message,
            cwe=CWECategory.RESOURCE_INJECTION,
            suggestions=[
                f"Check that module '{module_path}' exists in search paths",
                "Verify import paths are configured correctly with --import-paths",
                "Ensure the module file has correct .ml extension",
                "Check file system permissions for import directories"
            ],
            context={
                "module_path": module_path,
                "search_paths": search_paths,
                "import_type": "user_module"
            },
            **kwargs
        )


@dataclass
class ModuleInfo:
    """Information about a resolved module."""

    name: str
    module_path: str
    ast: Program
    source_code: str
    file_path: Optional[str] = None
    is_stdlib: bool = False
    is_python: bool = False
    dependencies: list[str] = None
    capabilities_required: list[str] = None
    resolved_timestamp: float = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.capabilities_required is None:
            self.capabilities_required = []
        if self.resolved_timestamp is None:
            self.resolved_timestamp = time.time()


class ModuleResolver:
    """Secure module resolver with capability integration."""

    def __init__(self,
                 import_paths: list[str] = None,
                 capability_manager: CapabilityManager = None,
                 allow_current_dir: bool = False):
        """Initialize module resolver.

        Args:
            import_paths: List of directories to search for modules
            capability_manager: Capability manager for security validation
            allow_current_dir: Whether to search current directory
        """
        self.import_paths = import_paths or []
        self.capability_manager = capability_manager or get_capability_manager()
        self.allow_current_dir = allow_current_dir
        self.cache = get_module_cache()
        self._dependency_graph: dict[str, set[str]] = {}

        # Python stdlib whitelist for compatibility mode
        self.python_whitelist = {
            "math", "json", "datetime", "random", "string", "re", "collections",
            "itertools", "functools", "operator", "hashlib", "base64", "uuid"
        }

    def resolve_import(self, import_target: list[str], source_file: str = None) -> ModuleInfo:
        """Resolve an import statement to a ModuleInfo.

        Args:
            import_target: Module path components (e.g., ['math', 'advanced'])
            source_file: Source file requesting the import (for relative imports)

        Returns:
            ModuleInfo for the resolved module

        Raises:
            ImportError: If module cannot be found or accessed
        """
        module_path = ".".join(import_target)

        # Check cache first
        cached = self._check_cache(module_path)
        if cached:
            return cached

        # Try different resolution strategies
        module_info = None

        # 1. Try ML Standard Library
        module_info = self._resolve_stdlib_module(module_path)
        if module_info:
            return self._cache_and_return(module_path, module_info)

        # 2. Try user modules from import paths
        module_info = self._resolve_user_module(import_target, source_file)
        if module_info:
            return self._cache_and_return(module_path, module_info)

        # 3. Try current directory (if allowed)
        if self.allow_current_dir:
            module_info = self._resolve_current_dir_module(import_target)
            if module_info:
                return self._cache_and_return(module_path, module_info)

        # 4. Try Python whitelist (compatibility mode)
        if module_path in self.python_whitelist:
            module_info = self._create_python_module_info(module_path)
            return self._cache_and_return(module_path, module_info)

        # Module not found
        search_paths = self.import_paths.copy()
        if self.allow_current_dir:
            search_paths.append(".")
        search_paths.extend(["ML Standard Library", "Python Whitelist"])

        raise ImportError(
            f"Module '{module_path}' not found",
            module_path=module_path,
            search_paths=search_paths,
            source_file=source_file
        )

    def _check_cache(self, module_path: str) -> Optional[ModuleInfo]:
        """Check if module is cached and valid."""
        # For now, simple cache check - could be enhanced with dependency validation
        return None  # TODO: Implement cache validation with dependency tracking

    def _resolve_stdlib_module(self, module_path: str) -> Optional[ModuleInfo]:
        """Try to resolve module from ML Standard Library."""
        try:
            stdlib_registry = get_stdlib_registry()
            return stdlib_registry.get_module(module_path)
        except ImportError:
            # Avoid circular imports
            return None
        except Exception:
            # Any other error in stdlib resolution
            return None

    def _resolve_user_module(self, import_target: list[str], source_file: str) -> Optional[ModuleInfo]:
        """Try to resolve user module from import paths."""
        if not self.import_paths:
            return None

        module_filename = import_target[-1] + ".ml"

        # Handle nested modules (e.g., utils.math -> utils/math.ml)
        if len(import_target) > 1:
            subpath = os.path.join(*import_target[:-1])
            candidates = [os.path.join(path, subpath, module_filename) for path in self.import_paths]
        else:
            candidates = [os.path.join(path, module_filename) for path in self.import_paths]

        # Also try directory-based modules (e.g., utils -> utils/__init__.ml)
        if len(import_target) == 1:
            init_candidates = [os.path.join(path, import_target[0], "__init__.ml") for path in self.import_paths]
            candidates.extend(init_candidates)

        for candidate in candidates:
            if self._validate_file_access(candidate):
                module_path = ".".join(import_target)
                return self._load_ml_file(candidate, module_path)

        return None

    def _resolve_current_dir_module(self, import_target: list[str]) -> Optional[ModuleInfo]:
        """Try to resolve module from current directory."""
        module_filename = import_target[-1] + ".ml"
        candidate = os.path.join(".", module_filename)

        if self._validate_file_access(candidate):
            module_path = ".".join(import_target)
            return self._load_ml_file(candidate, module_path)

        return None

    def _validate_file_access(self, file_path: str) -> bool:
        """Validate file access through capability system."""
        try:
            # Check if file exists
            if not os.path.isfile(file_path):
                return False

            # Validate capability for file access
            # TODO: Integrate with capability system
            # For now, just check basic file access
            abs_path = os.path.abspath(file_path)

            # Security check: ensure file is within allowed paths
            for allowed_path in self.import_paths:
                abs_allowed = os.path.abspath(allowed_path)
                if abs_path.startswith(abs_allowed):
                    return True

            # Allow current directory if configured
            if self.allow_current_dir and abs_path.startswith(os.path.abspath(".")):
                return True

            return False

        except (OSError, IOError):
            return False

    def _load_ml_file(self, file_path: str, module_path: str) -> ModuleInfo:
        """Load and parse an ML file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()

            # Parse the ML code
            ast = parse_ml_code(source_code, file_path)

            # Extract dependencies (imports within the module)
            dependencies = self._extract_dependencies(ast)

            # Detect circular dependencies
            self._check_circular_dependencies(module_path, dependencies)

            return ModuleInfo(
                name=module_path.split('.')[-1],
                module_path=module_path,
                ast=ast,
                source_code=source_code,
                file_path=file_path,
                is_stdlib=False,
                is_python=False,
                dependencies=dependencies
            )

        except (OSError, IOError) as e:
            raise ImportError(
                f"Failed to read module file '{file_path}': {e}",
                module_path=module_path,
                search_paths=self.import_paths,
                source_file=file_path
            )
        except Exception as e:
            raise ImportError(
                f"Failed to parse module '{module_path}': {e}",
                module_path=module_path,
                search_paths=self.import_paths,
                source_file=file_path
            )

    def _extract_dependencies(self, ast: Program) -> list[str]:
        """Extract import dependencies from AST."""
        dependencies = []

        for item in ast.items:
            if hasattr(item, 'target') and hasattr(item, '__class__') and 'Import' in item.__class__.__name__:
                # This is an import statement
                dep_path = ".".join(item.target) if isinstance(item.target, list) else str(item.target)
                dependencies.append(dep_path)

        return dependencies

    def _check_circular_dependencies(self, module_path: str, dependencies: list[str]) -> None:
        """Check for circular dependencies."""
        # Update dependency graph
        self._dependency_graph[module_path] = set(dependencies)

        # Check for cycles using DFS
        visited = set()
        rec_stack = set()

        def has_cycle(node: str) -> bool:
            if node in rec_stack:
                return True
            if node in visited:
                return False

            visited.add(node)
            rec_stack.add(node)

            for neighbor in self._dependency_graph.get(node, []):
                if has_cycle(neighbor):
                    return True

            rec_stack.remove(node)
            return False

        if has_cycle(module_path):
            raise ImportError(
                f"Circular dependency detected involving module '{module_path}'",
                module_path=module_path,
                search_paths=self.import_paths
            )

    def _create_python_module_info(self, module_path: str) -> ModuleInfo:
        """Create module info for Python stdlib modules."""
        return ModuleInfo(
            name=module_path,
            module_path=module_path,
            ast=None,  # No AST for Python modules
            source_code="",  # No ML source code
            file_path=None,
            is_stdlib=False,
            is_python=True,
            dependencies=[],
            capabilities_required=self._get_python_module_capabilities(module_path)
        )

    def _get_python_module_capabilities(self, module_path: str) -> list[str]:
        """Get required capabilities for Python modules."""
        # Define capability requirements for known Python modules
        capability_map = {
            "math": ["read:math_constants", "execute:calculations"],
            "json": ["read:json_data", "write:json_data"],
            "datetime": ["read:system_time", "read:timezone_data"],
            "random": ["read:entropy", "execute:random_generation"],
            "hashlib": ["execute:cryptographic_operations"],
            "base64": ["execute:encoding_operations"],
            "uuid": ["read:system_info", "execute:uuid_generation"]
        }

        return capability_map.get(module_path, ["execute:python_interop"])

    def _cache_and_return(self, module_path: str, module_info: ModuleInfo) -> ModuleInfo:
        """Cache module info and return it."""
        if module_info.source_code:  # Only cache modules with source code
            self.cache.put(
                module_path=module_path,
                module_info=module_info,
                source_code=module_info.source_code,
                dependencies=module_info.dependencies,
                file_path=module_info.file_path
            )
        return module_info

    def invalidate_cache(self, module_path: str = None) -> None:
        """Invalidate cached modules."""
        if module_path:
            self.cache.invalidate(module_path)
        else:
            self.cache.clear()

    def get_resolver_stats(self) -> dict:
        """Get resolver statistics."""
        return {
            "import_paths": self.import_paths,
            "allow_current_dir": self.allow_current_dir,
            "python_whitelist_size": len(self.python_whitelist),
            "dependency_graph_size": len(self._dependency_graph),
            "cache_stats": self.cache.get_stats()
        }


# Global resolver instance
_default_resolver: Optional[ModuleResolver] = None

def get_default_resolver() -> ModuleResolver:
    """Get default module resolver instance."""
    global _default_resolver
    if _default_resolver is None:
        _default_resolver = ModuleResolver()
    return _default_resolver

def set_default_resolver(resolver: ModuleResolver) -> None:
    """Set default module resolver instance."""
    global _default_resolver
    _default_resolver = resolver