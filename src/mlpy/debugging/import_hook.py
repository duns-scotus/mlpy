"""Import hook system for automatic source map loading.

This module implements a Python import hook that detects when modules are
imported at runtime and automatically loads corresponding ML source maps.
This enables deferred breakpoint resolution - breakpoints can be set in
files that haven't been imported yet, and they activate automatically when
the module loads.

Architecture:
    1. MLImportHook (MetaPathFinder) installed in sys.meta_path
    2. Hook intercepts all module imports
    3. After successful import, checks for .ml.map file
    4. If found, notifies debugger to load source map
    5. Debugger activates any pending breakpoints for that file

This follows the same pattern as professional debuggers (VS Code, gdb, etc.)
"""

import sys
import importlib.abc
import importlib.machinery
from pathlib import Path
from typing import Optional, Callable


class MLImportHook(importlib.abc.MetaPathFinder):
    """Import hook that detects module loading and triggers source map loading.

    This hook monitors sys.modules to detect when new modules are imported.
    It doesn't interfere with normal import behavior - it just observes imports
    and notifies the debugger when ML-generated Python modules are loaded.

    Example:
        >>> hook = MLImportHook(on_module_loaded)
        >>> hook.install()
        >>> import utils  # Hook detects this and calls on_module_loaded("utils", "/path/to/utils.py")
    """

    def __init__(self, on_module_loaded: Optional[Callable[[str, str], None]] = None):
        """Initialize import hook.

        Args:
            on_module_loaded: Callback function called when a module is loaded.
                             Signature: on_module_loaded(module_name: str, module_file: str)
        """
        self.on_module_loaded = on_module_loaded
        self.installed = False
        self._seen_modules = set()  # Track modules we've already processed
        self._original_import = None

    def install(self):
        """Install this hook into the import system.

        We wrap __import__ to detect when modules are loaded.
        """
        if not self.installed:
            # Remember currently loaded modules
            self._seen_modules = set(sys.modules.keys())

            # Wrap __import__ to detect new imports
            # __builtins__ can be either a dict or a module
            import builtins
            self._original_import = builtins.__import__
            builtins.__import__ = self._import_wrapper
            self.installed = True

    def uninstall(self):
        """Remove this hook from the import system."""
        if self.installed:
            # Restore original __import__
            if self._original_import:
                import builtins
                builtins.__import__ = self._original_import
            self.installed = False

    def _import_wrapper(self, name, *args, **kwargs):
        """Wrapper around __import__ to detect module loads.

        Args:
            name: Module name being imported
            *args: Additional __import__ arguments
            **kwargs: Additional __import__ keyword arguments

        Returns:
            The imported module
        """
        # Call original import
        module = self._original_import(name, *args, **kwargs)

        # Check if this is a new module we haven't seen
        if name not in self._seen_modules and name in sys.modules:
            self._seen_modules.add(name)

            # Get module file
            loaded_module = sys.modules[name]
            module_file = getattr(loaded_module, '__file__', None)

            if module_file and module_file.endswith('.py'):
                # Notify callback
                if self.on_module_loaded:
                    try:
                        self.on_module_loaded(name, module_file)
                    except Exception:
                        # Don't break imports if callback fails
                        pass

        return module

    def find_spec(self, fullname, path, target=None):
        """MetaPathFinder hook - we don't actually find modules.

        Returns:
            None - let standard import system handle module finding
        """
        return None


class MLDebuggerImportManager:
    """Manages import hooks for the ML debugger.

    This class coordinates the import hook system with the debugger,
    automatically loading source maps and activating breakpoints when
    modules are imported.

    Example:
        >>> manager = MLDebuggerImportManager(debugger)
        >>> manager.start()
        # Now when code imports modules, source maps auto-load
        >>> manager.stop()
    """

    def __init__(self, debugger):
        """Initialize import manager.

        Args:
            debugger: MLDebugger instance to notify of module loads
        """
        self.debugger = debugger
        self.hook = MLImportHook(on_module_loaded=self._on_module_loaded)
        self.tracked_modules = set()  # Avoid duplicate processing

    def start(self):
        """Start monitoring imports."""
        self.hook.install()

    def stop(self):
        """Stop monitoring imports."""
        self.hook.uninstall()

    def _on_module_loaded(self, module_name: str, module_file: str):
        """Called when a module is imported.

        Args:
            module_name: Name of the imported module
            module_file: Path to the .py file
        """
        # Avoid processing the same module multiple times
        if module_file in self.tracked_modules:
            return

        self.tracked_modules.add(module_file)

        # Check if there's a corresponding .ml.map file
        py_path = Path(module_file)

        # Look for .ml.map alongside the .py file
        map_file = py_path.with_suffix('.ml.map')

        if not map_file.exists():
            # No source map - not an ML-generated module
            return

        # Infer ML source file path
        ml_file = py_path.with_suffix('.ml')

        if not ml_file.exists():
            # ML source doesn't exist (maybe deleted?)
            return

        # Load source map automatically
        try:
            success = self.debugger.load_source_map_for_file(str(ml_file))
            if success:
                # Source map loaded successfully
                # Pending breakpoints will have been activated automatically
                # by load_source_map_for_file() -> _activate_pending_breakpoints_for_file()
                pass
        except Exception as e:
            # Silently ignore errors - don't break program execution
            # Debug builds can enable verbose logging here
            pass

    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
        return False
