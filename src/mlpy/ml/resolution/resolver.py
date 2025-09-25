"""Module resolution engine with security validation."""

import os
import time
from dataclasses import dataclass

from mlpy.ml.errors.exceptions import CWECategory, MLError
from mlpy.ml.grammar.ast_nodes import Program
from mlpy.ml.grammar.parser import parse_ml_code
from mlpy.runtime.capabilities.manager import CapabilityManager, get_capability_manager

from .cache import get_module_cache


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
                "Check file system permissions for import directories",
            ],
            context={
                "module_path": module_path,
                "search_paths": search_paths,
                "import_type": "user_module",
            },
            **kwargs,
        )


@dataclass
class ModuleInfo:
    """Information about a resolved module."""

    name: str
    module_path: str
    ast: Program
    source_code: str
    file_path: str | None = None
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

    def __init__(
        self,
        import_paths: list[str] = None,
        capability_manager: CapabilityManager = None,
        allow_current_dir: bool = False,
    ):
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
            "math",
            "json",
            "datetime",
            "random",
            "string",
            "re",
            "collections",
            "itertools",
            "functools",
            "operator",
            "hashlib",
            "base64",
            "uuid",
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
            source_file=source_file,
        )

    def _check_cache(self, module_path: str) -> ModuleInfo | None:
        """Check if module is cached and valid."""
        cached_module = self.cache.get(module_path)
        if not cached_module:
            return None

        # Validate cache freshness for file-based modules
        if cached_module.file_path:
            try:
                file_stat = os.stat(cached_module.file_path)
                file_mtime = file_stat.st_mtime

                # If file is newer than cache, invalidate
                if file_mtime > cached_module.resolved_timestamp:
                    self.cache.invalidate(module_path)
                    return None
            except (OSError, FileNotFoundError):
                # File no longer exists, invalidate cache
                self.cache.invalidate(module_path)
                return None

        # Check dependency freshness
        if self._dependencies_changed(cached_module):
            self.cache.invalidate(module_path)
            return None

        return cached_module

    def _dependencies_changed(self, module_info: ModuleInfo) -> bool:
        """Check if any dependencies have changed since module was cached."""
        for dep_name in module_info.dependencies:
            # Try to resolve dependency and check if it's changed
            try:
                current_dep = self.cache.get(dep_name)
                if not current_dep:
                    # Dependency not in cache, assume changed
                    return True

                # Compare timestamps - if dependency is newer, module needs refresh
                if current_dep.resolved_timestamp > module_info.resolved_timestamp:
                    return True

            except Exception:
                # Error checking dependency, assume changed for safety
                return True

        return False

    def _resolve_stdlib_module(self, module_path: str) -> ModuleInfo | None:
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

    def _resolve_user_module(self, import_target: list[str], source_file: str) -> ModuleInfo | None:
        """Try to resolve user module from import paths."""
        if not self.import_paths:
            return None

        module_filename = import_target[-1] + ".ml"

        # Handle nested modules (e.g., utils.math -> utils/math.ml)
        if len(import_target) > 1:
            subpath = os.path.join(*import_target[:-1])
            candidates = [
                os.path.join(path, subpath, module_filename) for path in self.import_paths
            ]
        else:
            candidates = [os.path.join(path, module_filename) for path in self.import_paths]

        # Also try directory-based modules (e.g., utils -> utils/__init__.ml)
        if len(import_target) == 1:
            init_candidates = [
                os.path.join(path, import_target[0], "__init__.ml") for path in self.import_paths
            ]
            candidates.extend(init_candidates)

        for candidate in candidates:
            if self._validate_file_access(candidate):
                module_path = ".".join(import_target)
                return self._load_ml_file(candidate, module_path)

        return None

    def _resolve_current_dir_module(self, import_target: list[str]) -> ModuleInfo | None:
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

        except OSError:
            return False

    def _load_ml_file(self, file_path: str, module_path: str) -> ModuleInfo:
        """Load and parse an ML file."""
        try:
            with open(file_path, encoding="utf-8") as f:
                source_code = f.read()

            # Parse the ML code
            ast = parse_ml_code(source_code, file_path)

            # Extract dependencies (imports within the module)
            dependencies = self._extract_dependencies(ast)

            # Detect circular dependencies
            self._check_circular_dependencies(module_path, dependencies)

            return ModuleInfo(
                name=module_path.split(".")[-1],
                module_path=module_path,
                ast=ast,
                source_code=source_code,
                file_path=file_path,
                is_stdlib=False,
                is_python=False,
                dependencies=dependencies,
            )

        except OSError as e:
            raise ImportError(
                f"Failed to read module file '{file_path}': {e}",
                module_path=module_path,
                search_paths=self.import_paths,
                source_file=file_path,
            )
        except Exception as e:
            raise ImportError(
                f"Failed to parse module '{module_path}': {e}",
                module_path=module_path,
                search_paths=self.import_paths,
                source_file=file_path,
            )

    def _extract_dependencies(self, ast: Program) -> list[str]:
        """Extract import dependencies from AST with enhanced pattern detection."""
        dependencies = []

        for item in ast.items:
            # Handle ImportStatement AST nodes
            if (
                hasattr(item, "target")
                and hasattr(item, "__class__")
                and "Import" in item.__class__.__name__
            ):
                dep_path = (
                    ".".join(item.target) if isinstance(item.target, list) else str(item.target)
                )
                dependencies.append(dep_path)

            # Also check for dynamic imports in function calls (for completeness)
            elif hasattr(item, "accept") and hasattr(item, "body"):
                # Recursively check function bodies for import statements
                self._extract_nested_dependencies(item, dependencies)

        return list(set(dependencies))  # Remove duplicates

    def _extract_nested_dependencies(self, node, dependencies: list[str]) -> None:
        """Recursively extract dependencies from nested AST nodes."""
        if hasattr(node, "body") and isinstance(node.body, list):
            for stmt in node.body:
                if (
                    hasattr(stmt, "target")
                    and hasattr(stmt, "__class__")
                    and "Import" in stmt.__class__.__name__
                ):
                    dep_path = (
                        ".".join(stmt.target) if isinstance(stmt.target, list) else str(stmt.target)
                    )
                    dependencies.append(dep_path)
                elif hasattr(stmt, "body"):
                    self._extract_nested_dependencies(stmt, dependencies)

    def _check_circular_dependencies(self, module_path: str, dependencies: list[str]) -> None:
        """Check for circular dependencies using enhanced cycle detection."""
        # Update dependency graph
        self._dependency_graph[module_path] = set(dependencies)

        # Check for cycles using DFS with recursion stack tracking
        def has_cycle_dfs(
            node: str, visited: set, rec_stack: set, path: list[str]
        ) -> list[str] | None:
            """DFS-based cycle detection with path tracking."""
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            # Visit all dependencies of current node
            for neighbor in self._dependency_graph.get(node, set()):
                if neighbor not in visited:
                    cycle_path = has_cycle_dfs(neighbor, visited, rec_stack, path.copy())
                    if cycle_path:
                        return cycle_path
                elif neighbor in rec_stack:
                    # Found cycle - return the cycle path
                    cycle_start = path.index(neighbor)
                    return path[cycle_start:] + [neighbor]

            rec_stack.remove(node)
            return None

        # Check for cycles starting from the current module
        visited = set()
        rec_stack = set()
        cycle_path = has_cycle_dfs(module_path, visited, rec_stack, [])

        if cycle_path:
            cycle_str = " → ".join(cycle_path)
            raise ImportError(
                f"Circular dependency detected: {cycle_str}",
                module_path=module_path,
                search_paths=self.import_paths,
                context={
                    "circular_dependency_path": cycle_path,
                    "cycle_length": len(cycle_path) - 1,
                },
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
            capabilities_required=self._get_python_module_capabilities(module_path),
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
            "uuid": ["read:system_info", "execute:uuid_generation"],
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
                file_path=module_info.file_path,
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
            "cache_stats": self.cache.get_stats(),
        }


# Global resolver instance
_default_resolver: ModuleResolver | None = None


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
