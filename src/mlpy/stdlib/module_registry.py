"""Central registry for ML stdlib and extension modules.

This module provides lazy discovery and caching of available modules.
Only scans directories when needed, only imports modules when used.

Design Principles:
- Lazy Directory Scanning: Don't scan directories until first query
- Lazy Module Loading: Only import modules when ML code uses them
- Thread-Safe: Safe for concurrent REPL usage
- Performance: Fast startup, low memory, scalable to hundreds of modules
"""

from pathlib import Path
from typing import Dict, Optional, Set, Any
from enum import Enum
from dataclasses import dataclass
import importlib.util
import ast
import threading
import logging

logger = logging.getLogger(__name__)


class ModuleType(Enum):
    """Module source type for unified registry."""
    PYTHON_BRIDGE = "python_bridge"  # *_bridge.py with @ml_module
    ML_SOURCE = "ml_source"          # *.ml user module
    BUILTIN = "builtin"              # Core ML builtins


@dataclass
class ModuleMetadata:
    """Unified metadata for all module types (Python bridges and ML modules).

    This replaces the old ModuleMetadata and supports both:
    - Python bridge modules (*_bridge.py with @ml_module decorator)
    - ML source modules (*.ml files)
    """

    # Common fields
    name: str                        # Module name (e.g., "math", "user_modules.sorting")
    module_type: ModuleType          # Source type
    file_path: Path                  # Path to source file

    # Python bridge specific
    module_class: Optional[type] = None      # Loaded class (for bridges)
    instance: Optional[object] = None        # Module instance (for bridges)

    # ML module specific
    transpiled_path: Optional[Path] = None   # Path to .py file (for ML)
    source_mtime: Optional[float] = None     # Source file modification time
    transpiled_mtime: Optional[float] = None # Transpiled file modification time
    ml_ast: Optional[Any] = None             # Cached ML AST (for fast reload)

    # Performance tracking (both types)
    load_time: Optional[float] = None        # Time to load/transpile
    reload_count: int = 0                    # Number of reloads
    memory_size: Optional[int] = None        # Estimated memory usage

    def needs_recompilation(self) -> bool:
        """Check if ML module needs recompilation."""
        if self.module_type != ModuleType.ML_SOURCE:
            return False

        if not self.transpiled_path or not self.transpiled_path.exists():
            return True

        if self.source_mtime is None or self.transpiled_mtime is None:
            return True

        return self.source_mtime > self.transpiled_mtime

    def load(self) -> Optional[object]:
        """Lazy-load the module based on type."""
        if self.module_type == ModuleType.PYTHON_BRIDGE:
            return self._load_python_bridge()
        elif self.module_type == ModuleType.ML_SOURCE:
            return self._load_ml_module()
        else:
            return None

    def reload(self) -> bool:
        """Reload the module based on type."""
        if self.module_type == ModuleType.PYTHON_BRIDGE:
            return self._reload_python_bridge()
        elif self.module_type == ModuleType.ML_SOURCE:
            return self._reload_ml_module()
        else:
            return False

    def _load_python_bridge(self) -> Optional[object]:
        """Load a Python bridge module (existing logic)."""
        if self.instance is not None:
            return self.instance

        try:
            # Import the module to trigger @ml_module decorator
            spec = importlib.util.spec_from_file_location(
                f"mlpy.stdlib.{self.file_path.stem}",
                self.file_path
            )

            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)

                # FIX: Register module in sys.modules BEFORE execution
                # This is standard practice per Python docs and ensures that
                # direct imports return the same module instance (fixes isinstance() checks)
                # https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
                import sys
                sys.modules[spec.name] = module

                spec.loader.exec_module(module)

                # Get the module instance (named same as the ML module name)
                if hasattr(module, self.name):
                    self.instance = getattr(module, self.name)
                    self.module_class = type(self.instance)

                    # Auto-register with SafeAttributeRegistry
                    self._register_with_security_system()
                else:
                    logger.warning(
                        f"Module '{self.name}' found in {self.file_path.name} "
                        f"but no instance variable '{self.name}' exists"
                    )

        except Exception as e:
            logger.error(
                f"Failed to load module '{self.name}' from {self.file_path}: {e}",
                exc_info=True
            )

        return self.instance

    def _load_ml_module(self) -> Optional[object]:
        """Load an ML source module by transpiling and importing."""
        import time
        from mlpy.ml.transpiler import MLTranspiler

        start = time.perf_counter()

        try:
            # Check if recompilation needed
            if self.needs_recompilation():
                # Transpile ML source to Python
                transpiler = MLTranspiler()

                source_code = self.file_path.read_text(encoding='utf-8')
                python_code, issues, source_map = transpiler.transpile_to_python(
                    source_code,
                    source_file=str(self.file_path)
                )

                if python_code is None:
                    logger.error(f"Failed to transpile {self.name}: {issues}")
                    return None

                # Write transpiled Python code
                self.transpiled_path.write_text(python_code, encoding='utf-8')
                self.transpiled_mtime = time.time()

                logger.debug(f"Transpiled {self.name} to {self.transpiled_path}")

            # Import the transpiled Python module
            import sys

            spec = importlib.util.spec_from_file_location(
                self.name,
                self.transpiled_path
            )

            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[self.name] = module  # Register in sys.modules
                spec.loader.exec_module(module)

                self.instance = module
                self.load_time = time.perf_counter() - start

                return module

        except Exception as e:
            logger.error(f"Failed to load ML module '{self.name}': {e}", exc_info=True)
            return None

    def _reload_python_bridge(self) -> bool:
        """Reload a Python bridge module (existing logic)."""
        import time
        import sys
        from mlpy.stdlib.decorators import _MODULE_REGISTRY

        try:
            # Clear cached state
            self.instance = None
            self.module_class = None

            # Clear from legacy MODULE_REGISTRY if present
            if self.name in _MODULE_REGISTRY:
                del _MODULE_REGISTRY[self.name]

            # Force re-import (Python module reload)
            module_path = f"mlpy.stdlib.{self.file_path.stem}"
            if module_path in sys.modules:
                del sys.modules[module_path]

            # Also try alternative module paths that might be cached
            alt_paths = [
                self.file_path.stem,
                f"mlpy_{self.file_path.stem}",
                self.name
            ]
            for alt_path in alt_paths:
                if alt_path in sys.modules:
                    del sys.modules[alt_path]

            # Invalidate Python's import cache (force reload of .pyc files)
            import importlib
            importlib.invalidate_caches()

            # Clear any __pycache__ for this specific file
            pycache_dir = self.file_path.parent / "__pycache__"
            if pycache_dir.exists():
                import glob
                pattern = f"{self.file_path.stem}.*.pyc"
                for pyc_file in pycache_dir.glob(pattern):
                    try:
                        pyc_file.unlink()
                    except:
                        pass  # Best effort

            # Re-load module
            module_instance = self._load_python_bridge()

            if module_instance:
                # Re-register with security system
                self._register_with_security_system()
                return True

        except Exception as e:
            logger.error(f"Failed to reload Python bridge module '{self.name}': {e}", exc_info=True)

        return False

    def _reload_ml_module(self) -> bool:
        """Reload an ML source module (re-transpile and re-import)."""
        import time
        import sys

        try:
            # Update source modification time
            self.source_mtime = self.file_path.stat().st_mtime

            # Clear cached instance
            self.instance = None

            # Remove from sys.modules to force re-import
            if self.name in sys.modules:
                del sys.modules[self.name]

            # Re-load (will re-transpile if needed)
            module = self._load_ml_module()

            return module is not None

        except Exception as e:
            logger.error(f"Failed to reload ML module '{self.name}': {e}", exc_info=True)
            return False

    def _register_with_security_system(self):
        """Register module with SafeAttributeRegistry for security."""
        if self.instance is None:
            return

        try:
            # Import SafeAttributeRegistry
            from mlpy.ml.codegen.safe_attribute_registry import get_safe_registry
            from mlpy.stdlib.decorators import register_module_with_safe_attributes

            # Get the global SafeAttributeRegistry instance
            registry = get_safe_registry()

            # Register module with correct parameters: (module_name: str, registry: SafeAttributeRegistry)
            register_module_with_safe_attributes(self.name, registry)

            logger.debug(f"Successfully registered module '{self.name}' with SafeAttributeRegistry")
        except ImportError as e:
            # SafeAttributeRegistry not available (during testing or migration)
            logger.debug(f"SafeAttributeRegistry not available for module '{self.name}': {e}")
        except Exception as e:
            # Log warning but don't fail module loading
            logger.warning(
                f"Failed to register module '{self.name}' with SafeAttributeRegistry: {e}"
            )


class ModuleRegistry:
    """Central registry for ML modules with lazy discovery.

    This registry provides:
    - Automatic discovery of *_bridge.py modules
    - Lazy scanning: Only scans directories when first queried
    - Lazy loading: Only imports modules when ML code uses them
    - Thread-safe operation for REPL usage
    - Extension path support for custom modules
    """

    def __init__(self):
        self._stdlib_dir = Path(__file__).parent
        self._extension_dirs: list[Path] = []       # For Python *_bridge.py
        self._ml_module_dirs: list[Path] = []       # For ML *.ml modules

        # Caches
        self._discovered: Dict[str, ModuleMetadata] = {}
        self._scanned: bool = False
        self._lock = threading.Lock()

        # Performance monitoring (development mode)
        self._performance_mode = False
        self._metrics = {
            "scan_times": [],
            "load_times": {},
            "reload_times": {},
            "transpile_times": {},  # NEW: ML transpilation times
        }

        # Legacy performance logging (kept for compatibility)
        self._enable_performance_logging = False
        self._load_times = {}

        # Check for development mode environment variable
        import os
        if os.getenv("MLPY_DEV_MODE", "").lower() in ("1", "true", "yes"):
            self.enable_performance_mode()
            logger.info("Development mode enabled via MLPY_DEV_MODE")

    def add_extension_paths(self, paths: list[str]):
        """Add extension directories to search with validation."""
        for path_str in paths:
            path = Path(path_str)

            if not path.exists():
                logger.warning(
                    f"Extension path '{path_str}' does not exist. "
                    f"No modules will be loaded from this path."
                )
                continue

            if not path.is_dir():
                logger.warning(
                    f"Extension path '{path_str}' is not a directory. "
                    f"Skipping this path."
                )
                continue

            self._extension_dirs.append(path)

        # Invalidate cache when new paths added
        self.invalidate_cache()

    def add_ml_module_paths(self, paths: list[str]):
        """Add ML module directories to search with validation.

        Args:
            paths: List of directory paths containing *.ml modules
        """
        for path_str in paths:
            path = Path(path_str)

            if not path.exists():
                logger.warning(
                    f"ML module path '{path_str}' does not exist. "
                    f"No modules will be loaded from this path."
                )
                continue

            if not path.is_dir():
                logger.warning(
                    f"ML module path '{path_str}' is not a directory. "
                    f"Skipping this path."
                )
                continue

            self._ml_module_dirs.append(path)
            logger.debug(f"Added ML module path: {path_str}")

        # Invalidate cache when new paths added
        self.invalidate_cache()

    def is_available(self, module_name: str) -> bool:
        """Check if a module is available (triggers scan if needed)."""
        self._ensure_scanned()
        return module_name in self._discovered

    def get_module(self, module_name: str) -> Optional[object]:
        """Get module instance (triggers lazy load).

        Args:
            module_name: Name of the module to load

        Returns:
            Module instance or None if not found/load failed
        """
        import time

        start_time = None
        if self._performance_mode or self._enable_performance_logging:
            start_time = time.perf_counter()

        self._ensure_scanned()

        metadata = self._discovered.get(module_name)
        result = metadata.load() if metadata else None

        if start_time and metadata:
            elapsed = time.perf_counter() - start_time

            # New performance system
            if self._performance_mode:
                self._record_timing("load", module_name, elapsed)

            # Legacy performance logging
            if self._enable_performance_logging:
                self._load_times[module_name] = elapsed
                logger.debug(f"Module '{module_name}' loaded in {elapsed*1000:.2f}ms")

        return result

    def get_all_module_names(self) -> Set[str]:
        """Get all available module names."""
        self._ensure_scanned()
        return set(self._discovered.keys())

    def get_all_modules(self, include_type: Optional[ModuleType] = None) -> dict[str, ModuleMetadata]:
        """Get all discovered modules, optionally filtered by type.

        Args:
            include_type: Filter by module type (None = all types)

        Returns:
            Dictionary of module_name -> metadata
        """
        self._ensure_scanned()

        if include_type:
            return {
                name: meta for name, meta in self._discovered.items()
                if meta.module_type == include_type
            }

        return self._discovered.copy()

    def get_module_info(self, module_name: str) -> Optional[dict]:
        """Get detailed information about a module (unified for all types).

        Args:
            module_name: Name of the module to query

        Returns:
            Dictionary with module metadata or None if not found
        """
        from datetime import datetime

        self._ensure_scanned()

        metadata = self._discovered.get(module_name)
        if not metadata:
            return None

        info = {
            'name': metadata.name,
            'type': metadata.module_type.value,
            'file_path': str(metadata.file_path),
            'loaded': metadata.instance is not None,
            'reload_count': metadata.reload_count,
        }

        # Type-specific info
        if metadata.module_type == ModuleType.ML_SOURCE:
            info['transpiled_path'] = str(metadata.transpiled_path) if metadata.transpiled_path else None
            info['needs_recompilation'] = metadata.needs_recompilation()
            if metadata.source_mtime:
                info['source_modified'] = datetime.fromtimestamp(metadata.source_mtime).isoformat()
        elif metadata.module_type == ModuleType.PYTHON_BRIDGE:
            # Extract functions from loaded instance or source file
            if metadata.instance:
                info['functions'] = self._extract_bridge_functions(metadata.instance)
            else:
                # Extract from source file without loading
                info['functions'] = self._extract_functions_from_source(metadata.file_path)

        # Performance info (if available)
        if metadata.load_time:
            info['load_time_ms'] = metadata.load_time * 1000

        return info

    def _extract_bridge_functions(self, instance: object) -> list[str]:
        """Extract function names from a Python bridge module instance.

        Args:
            instance: Module instance

        Returns:
            List of function names
        """
        functions = []
        for attr_name in dir(instance):
            if not attr_name.startswith('_'):
                attr = getattr(instance, attr_name, None)
                if callable(attr):
                    functions.append(attr_name)
        return sorted(functions)

    def _extract_functions_from_source(self, bridge_file: Path) -> list[str]:
        """Extract function names from @ml_function decorators without importing.

        Args:
            bridge_file: Path to the bridge module file

        Returns:
            List of function names decorated with @ml_function
        """
        functions = []
        try:
            source = bridge_file.read_text(encoding='utf-8')
            tree = ast.parse(source)

            # Look for methods decorated with @ml_function inside classes
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            # Check if decorated with @ml_function
                            for decorator in item.decorator_list:
                                if isinstance(decorator, ast.Call):
                                    if isinstance(decorator.func, ast.Name) and \
                                       decorator.func.id == 'ml_function':
                                        functions.append(item.name)
                                        break
                                elif isinstance(decorator, ast.Name) and decorator.id == 'ml_function':
                                    functions.append(item.name)
                                    break

        except Exception as e:
            logger.warning(f"Failed to extract functions from {bridge_file.name}: {e}")

        return sorted(functions)

    def invalidate_cache(self):
        """Invalidate cached module discovery."""
        with self._lock:
            self._scanned = False
            self._discovered.clear()

    def enable_performance_logging(self):
        """Enable performance logging for diagnostics."""
        self._enable_performance_logging = True

    def get_performance_report(self) -> dict:
        """Get performance metrics for all loaded modules."""
        return {
            "total_modules": len(self._discovered),
            "loaded_modules": len([m for m in self._discovered.values() if m.instance]),
            "load_times": self._load_times,
            "avg_load_time": sum(self._load_times.values()) / len(self._load_times) if self._load_times else 0
        }

    def _ensure_scanned(self):
        """Ensure directories have been scanned (lazy, thread-safe)."""
        if self._scanned:
            return

        with self._lock:
            # Double-check after acquiring lock
            if self._scanned:
                return

            # Scan stdlib directory for Python bridges
            self._scan_directory(self._stdlib_dir)

            # Scan extension directories for Python bridges
            for ext_dir in self._extension_dirs:
                if ext_dir.exists():
                    self._scan_directory(ext_dir)

            # Scan ML module directories for *.ml files
            for ml_dir in self._ml_module_dirs:
                if ml_dir.exists():
                    self._scan_ml_modules(ml_dir)

            self._scanned = True

    def _scan_directory(self, directory: Path):
        """Scan a directory for *_bridge.py modules (without importing).

        Args:
            directory: Directory to scan for bridge modules
        """
        for bridge_file in directory.glob("*_bridge.py"):
            if bridge_file.stem == "__init__":
                continue

            # Extract module name from file without importing
            module_name = self._extract_module_name(bridge_file)

            if module_name:
                # Check for collision
                if module_name in self._discovered:
                    existing = self._discovered[module_name]
                    logger.warning(
                        f"Module name collision: '{module_name}' found in both "
                        f"'{existing.file_path}' and '{bridge_file}'. "
                        f"Using first occurrence: '{existing.file_path}'"
                    )
                    continue  # Skip duplicate

                # Register Python bridge module
                metadata = ModuleMetadata(
                    name=module_name,
                    module_type=ModuleType.PYTHON_BRIDGE,
                    file_path=bridge_file,
                )
                self._discovered[module_name] = metadata

    def _extract_module_name(self, bridge_file: Path) -> Optional[str]:
        """Extract module name from @ml_module decorator without importing.

        Args:
            bridge_file: Path to the bridge module file

        Returns:
            Module name if found, None otherwise
        """
        try:
            source = bridge_file.read_text(encoding='utf-8')
            tree = ast.parse(source)

            # Look for @ml_module(name="...") decorator
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Call):
                            if isinstance(decorator.func, ast.Name) and \
                               decorator.func.id == 'ml_module':
                                # Extract name from decorator arguments
                                for keyword in decorator.keywords:
                                    if keyword.arg == 'name':
                                        if isinstance(keyword.value, ast.Constant):
                                            return keyword.value.value

        except Exception as e:
            # Log but don't fail on parse errors
            logger.warning(f"Failed to extract module name from {bridge_file.name}: {e}")

        return None

    def _scan_ml_modules(self, directory: Path, prefix: str = ""):
        """Recursively scan directory for *.ml modules.

        Args:
            directory: Directory to scan for ML modules
            prefix: Module name prefix for nested directories (e.g., "user_modules")
        """
        # Scan for *.ml files in current directory
        for ml_file in directory.glob("*.ml"):
            # Build module name: prefix + filename
            module_name = f"{prefix}.{ml_file.stem}" if prefix else ml_file.stem

            # Check for collision with existing modules
            if module_name in self._discovered:
                existing = self._discovered[module_name]
                logger.warning(
                    f"Module name collision: '{module_name}' found as both "
                    f"{existing.module_type.value} ({existing.file_path}) and "
                    f"ML module ({ml_file}). "
                    f"Using {existing.module_type.value} module."
                )
                continue  # Skip - Python bridges take precedence

            # Register ML source module
            metadata = ModuleMetadata(
                name=module_name,
                module_type=ModuleType.ML_SOURCE,
                file_path=ml_file,
                transpiled_path=ml_file.with_suffix('.py'),
                source_mtime=ml_file.stat().st_mtime,
            )
            self._discovered[module_name] = metadata
            logger.debug(f"Discovered ML module: {module_name} at {ml_file}")

        # Recursively scan subdirectories
        for subdir in directory.iterdir():
            if subdir.is_dir() and not subdir.name.startswith('.') and not subdir.name.startswith('_'):
                # Build nested module prefix: prefix.subdir
                nested_prefix = f"{prefix}.{subdir.name}" if prefix else subdir.name
                self._scan_ml_modules(subdir, nested_prefix)

    # Development Mode Features

    def enable_performance_mode(self):
        """Enable detailed performance tracking for development."""
        self._performance_mode = True
        self._enable_performance_logging = True  # Legacy compatibility
        logger.info("Performance monitoring enabled")

    def disable_performance_mode(self):
        """Disable performance tracking."""
        self._performance_mode = False
        self._enable_performance_logging = False
        logger.info("Performance monitoring disabled")

    def _record_timing(self, operation: str, module_name: str, elapsed: float):
        """Record timing for an operation.

        Args:
            operation: Type of operation ('load', 'reload', 'scan')
            module_name: Name of the module
            elapsed: Time elapsed in seconds
        """
        if not self._performance_mode:
            return

        if operation == "load":
            self._metrics["load_times"][module_name] = elapsed
        elif operation == "reload":
            if module_name not in self._metrics["reload_times"]:
                self._metrics["reload_times"][module_name] = []
            self._metrics["reload_times"][module_name].append(elapsed)
        elif operation == "scan":
            self._metrics["scan_times"].append(elapsed)

        # Log if slow
        threshold = 0.1  # 100ms
        if elapsed > threshold:
            logger.warning(
                f"Slow {operation} detected: {module_name} took {elapsed*1000:.2f}ms"
            )

    def reload_module(self, module_name: str) -> bool:
        """Reload a specific module from disk without restarting.

        Works for both Python bridge modules and ML source modules.

        Args:
            module_name: Name of the module to reload

        Returns:
            True if reload successful, False otherwise
        """
        import time

        if module_name not in self._discovered:
            logger.warning(f"Cannot reload '{module_name}': module not found")
            return False

        metadata = self._discovered[module_name]
        start = time.perf_counter()

        try:
            # Delegate to type-specific reload
            success = metadata.reload()

            if success:
                metadata.reload_count += 1
                elapsed = time.perf_counter() - start
                self._record_timing("reload", module_name, elapsed)

                logger.info(
                    f"Successfully reloaded {metadata.module_type.value} module: "
                    f"{module_name} ({elapsed*1000:.2f}ms)"
                )
                return True

        except Exception as e:
            logger.error(f"Failed to reload module '{module_name}': {e}", exc_info=True)

        return False

    def reload_all_modules(self) -> dict[str, bool]:
        """Reload all currently loaded modules.

        Returns:
            Dictionary mapping module names to reload success status
        """
        results = {}

        for module_name, metadata in self._discovered.items():
            if metadata.instance is not None:  # Only reload loaded modules
                results[module_name] = self.reload_module(module_name)

        return results

    def refresh_all(self) -> dict:
        """Complete refresh: re-scan directories and reload all modules.

        Returns:
            Dictionary with refresh statistics
        """
        logger.info("Starting full module refresh...")

        # Track loaded modules before refresh
        previously_loaded = {
            name for name, meta in self._discovered.items()
            if meta.instance is not None
        }

        # Invalidate and re-scan
        self.invalidate_cache()
        self._ensure_scanned()

        # Reload previously loaded modules
        reload_results = {}
        for module_name in previously_loaded:
            if module_name in self._discovered:
                reload_results[module_name] = self.reload_module(module_name)

        return {
            "total_modules": len(self._discovered),
            "reloaded_modules": len([r for r in reload_results.values() if r]),
            "reload_failures": len([r for r in reload_results.values() if not r]),
            "reload_details": reload_results
        }

    def get_performance_summary(self) -> dict:
        """Get comprehensive performance summary.

        Returns:
            Dictionary with performance metrics
        """
        load_times = list(self._metrics["load_times"].values())
        scan_times = self._metrics["scan_times"]

        # Get slowest loads
        slowest_loads = sorted(
            self._metrics["load_times"].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        return {
            "total_scans": len(scan_times),
            "avg_scan_time_ms": (sum(scan_times) / len(scan_times) * 1000) if scan_times else 0.0,
            "total_loads": len(load_times),
            "avg_load_time_ms": (sum(load_times) / len(load_times) * 1000) if load_times else 0.0,
            "slowest_loads": slowest_loads,
            "reload_counts": {
                name: len(times)
                for name, times in self._metrics["reload_times"].items()
            }
        }

    def get_memory_report(self) -> dict:
        """Get memory usage report for loaded modules.

        Returns:
            Dictionary with memory usage information
        """
        import sys

        loaded_modules = []
        total_size = 0

        for module_name, metadata in self._discovered.items():
            if metadata.instance is not None:
                # Estimate size of module instance
                size = sys.getsizeof(metadata.instance)

                # Include size of module class if available
                if metadata.module_class:
                    size += sys.getsizeof(metadata.module_class)

                loaded_modules.append({
                    "name": module_name,
                    "size_bytes": size,
                    "size_kb": size / 1024
                })

                total_size += size

        # Sort by size descending
        loaded_modules.sort(key=lambda x: x["size_bytes"], reverse=True)

        return {
            "total_loaded": len(loaded_modules),
            "total_size_kb": total_size / 1024,
            "total_size_mb": total_size / (1024 * 1024),
            "modules": loaded_modules[:10],  # Top 10
        }


# Global registry instance
_global_registry: Optional[ModuleRegistry] = None
_registry_lock = threading.Lock()


def get_registry() -> ModuleRegistry:
    """Get the global module registry (thread-safe singleton)."""
    global _global_registry

    if _global_registry is not None:
        return _global_registry

    with _registry_lock:
        # Double-check after acquiring lock
        if _global_registry is None:
            _global_registry = ModuleRegistry()

        return _global_registry
