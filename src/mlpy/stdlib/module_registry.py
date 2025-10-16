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
from typing import Dict, Optional, Set
import importlib.util
import ast
import threading
import logging

logger = logging.getLogger(__name__)


class ModuleMetadata:
    """Lightweight metadata for a discovered module."""

    def __init__(self, name: str, file_path: Path, module_class: Optional[type] = None):
        self.name = name
        self.file_path = file_path
        self.module_class = module_class  # Loaded lazily
        self.instance = None  # Loaded lazily

    def load(self):
        """Lazy-load the module class and instance."""
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
        self._extension_dirs: list[Path] = []

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

            # Scan stdlib directory
            self._scan_directory(self._stdlib_dir)

            # Scan extension directories
            for ext_dir in self._extension_dirs:
                if ext_dir.exists():
                    self._scan_directory(ext_dir)

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

                # Register new module
                metadata = ModuleMetadata(module_name, bridge_file)
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

        Args:
            module_name: Name of the module to reload

        Returns:
            True if reload successful, False otherwise
        """
        import time
        import sys
        import importlib

        if module_name not in self._discovered:
            logger.warning(f"Cannot reload '{module_name}': module not found")
            return False

        metadata = self._discovered[module_name]
        start = time.perf_counter()

        try:
            # Clear cached state
            metadata.instance = None
            metadata.module_class = None

            # Force re-import (Python module reload)
            module_path = f"mlpy.stdlib.{metadata.file_path.stem}"
            if module_path in sys.modules:
                del sys.modules[module_path]

            # Re-load module
            module_instance = metadata.load()

            if module_instance:
                # Re-register with security system
                metadata._register_with_security_system()

                elapsed = time.perf_counter() - start
                self._record_timing("reload", module_name, elapsed)

                logger.info(f"Successfully reloaded module: {module_name} ({elapsed*1000:.2f}ms)")
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
            "avg_scan_time_ms": (sum(scan_times) / len(scan_times) * 1000) if scan_times else 0,
            "total_loads": len(load_times),
            "avg_load_time_ms": (sum(load_times) / len(load_times) * 1000) if load_times else 0,
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
