# Unified Module Registry Proposal

**Document Version:** 1.2
**Date:** January 2026
**Status:** ✅ **COMPLETE** - All 3 Weeks Implemented
**Priority:** High - Developer Experience Enhancement
**Depends On:** None (extends existing module system)

## ✅ **IMPLEMENTATION COMPLETE**

**Status:** All phases complete (Week 1, 2, 3)
**Critical Bugfix:** Resolved (see [repl-import-bugfix.md](./repl-import-bugfix.md))
**Impact:** Full unified module experience for both Python bridges and ML modules
**Total Implementation Time:** ~9 hours (Week 1-2: 5h + Week 3: 4h)

---

## Executive Summary

This proposal unifies module detection, inspection, and reloading for both **Python extension modules** (`*_bridge.py`) and **user-defined ML modules** (`*.ml`) while maintaining separate search path configurations. The goal is to provide a seamless developer experience where REPL commands (`.modules`, `.reload`, `.modinfo`, etc.) work consistently across both module types.

**Current State:**
- ✅ Python bridge modules: Full auto-detection, hot reloading, REPL commands
- ✅ ML modules: Import system works, nested directories supported
- ❌ ML modules: Invisible to REPL commands, no hot reloading, not in registry

**Target State:**
- ✅ **Unified registry** tracking both Python bridges AND ML modules
- ✅ **Separate search paths** maintained (security + organization)
- ✅ **REPL commands** work seamlessly with both module types
- ✅ **Hot reloading** for ML modules without REPL restart
- ✅ **Performance monitoring** across all loaded modules

---

## Problem Statement

### Current Architecture: Two Parallel Systems

#### System 1: Python Bridge Modules (`*_bridge.py`)
**Search Path:** `python_extension_paths` / `extension_paths`

```python
# Configuration
MLTranspiler(python_extension_paths=["/path/to/extensions"])
MLREPLSession(extension_paths=["/path/to/extensions"])

# Registry Integration
ModuleRegistry.add_extension_paths(paths)  # Auto-discovers *_bridge.py
ModuleRegistry.reload_module("math")       # Hot reload works
```

**REPL Commands:**
- ✅ `.modules` - Lists all Python bridge modules
- ✅ `.modinfo <name>` - Shows module details
- ✅ `.reload <module>` - Hot reload without restart
- ✅ `.perfmon` - Performance metrics
- ✅ `.memreport` - Memory usage
- ✅ `.addpath <path>` - Add extension directory

#### System 2: User ML Modules (`*.ml`)
**Search Path:** `import_paths` (in PythonCodeGenerator only!)

```python
# Configuration (NOT in REPL!)
PythonCodeGenerator(
    import_paths=["/path/to/user/modules"],
    allow_current_dir=True
)

# Import Resolution (works!)
import user_modules.sorting  # ✅ Finds user_modules/sorting.ml
import algorithms.quicksort  # ✅ Nested directories work
```

**REPL Commands:**
- ❌ `.modules` - ML modules NOT listed
- ❌ `.modinfo utils` - "Module not found"
- ❌ `.reload utils` - "Module not found"
- ❌ `.perfmon` - ML modules NOT tracked
- ❌ `.memreport` - ML modules NOT counted
- ❌ `.addpath <path>` - Only scans for `*_bridge.py`

### The Disconnect

```python
mlpy> .addpath ./my_app
✓ Added extension path: /projects/my_app  # Scans for *_bridge.py only

mlpy> import my_app.utils  # ✅ WORKS (transpiler finds utils.ml)

mlpy> .modules
Available Modules (8 total):  # ❌ utils NOT LISTED
  • math, random, json, datetime...

mlpy> .reload my_app.utils
Module 'my_app.utils' not found  # ❌ Not in ModuleRegistry

# Edit my_app/utils.ml...
mlpy> import my_app.utils  # ❌ Still uses old code (no hot reload)
```

**Developer Impact:**
- Confusing: Two configuration systems (`python_extension_paths` vs `import_paths`)
- Incomplete: REPL commands don't work with user code
- Frustrating: Must restart REPL to reload changed `.ml` files
- Inconsistent: Same `import` statement, different registry behaviors

---

## Design Philosophy

### Core Principles

1. **Separate Search Paths = Good Design**
   - Python extensions: Trusted third-party code, system-wide
   - ML modules: User project code, project-specific
   - Security: Different trust levels, different sandboxing
   - Organization: Clear separation of concerns

2. **Unified Module Interface = Essential**
   - Import statement works the same for both types
   - REPL commands work the same for both types
   - Developers shouldn't care about implementation details

3. **Registry Tracks All Modules**
   - Single source of truth for "what's available"
   - Consistent inspection and introspection
   - Unified performance monitoring

### What We Keep

✅ **Separate Configuration:**
```python
MLREPLSession(
    extension_paths=["/usr/local/mlpy/extensions"],  # Python bridges
    ml_module_paths=["./src", "./lib"]              # User .ml modules
)
```

✅ **Security Boundaries:**
- Python bridges: Require `@ml_module` decorator, registered with SafeAttributeRegistry
- ML modules: Full transpilation + security analysis, capability enforcement

✅ **Different Discovery Mechanisms:**
- Python bridges: AST-based decorator scanning
- ML modules: File system `.ml` file discovery

### What We Unify

✅ **Module Registry:**
- Single `ModuleRegistry` tracks both types
- Metadata distinguishes module source type
- Common interface for inspection/reloading

✅ **REPL Commands:**
- `.modules` shows ALL available modules (both types)
- `.reload <module>` works for both (different reload strategies)
- `.perfmon` / `.memreport` track all loaded modules

✅ **Developer Experience:**
- Consistent import behavior
- Predictable hot reloading
- Clear module visibility

---

## Proposed Architecture

### 1. Enhanced Module Metadata

```python
from enum import Enum
from pathlib import Path
from typing import Optional

class ModuleType(Enum):
    """Module source type."""
    PYTHON_BRIDGE = "python_bridge"  # *_bridge.py with @ml_module
    ML_SOURCE = "ml_source"          # *.ml user module
    BUILTIN = "builtin"              # Core ML builtins

@dataclass
class UnifiedModuleMetadata:
    """Unified metadata for all module types."""

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
```

### 2. Unified Module Registry

```python
class UnifiedModuleRegistry:
    """Central registry for ALL module types.

    This registry provides:
    - Auto-discovery of Python bridge modules (*_bridge.py)
    - Auto-discovery of ML source modules (*.ml)
    - Lazy loading for both types
    - Hot reloading for both types
    - Unified inspection and monitoring
    """

    def __init__(self):
        self._stdlib_dir = Path(__file__).parent
        self._python_extension_dirs: list[Path] = []   # For *_bridge.py
        self._ml_module_dirs: list[Path] = []          # For *.ml

        # Unified discovery cache
        self._discovered: Dict[str, UnifiedModuleMetadata] = {}
        self._scanned: bool = False
        self._lock = threading.Lock()

        # Performance tracking (all modules)
        self._performance_mode = False
        self._metrics = {
            "scan_times": [],
            "load_times": {},
            "reload_times": {},
            "transpile_times": {},  # NEW: ML transpilation times
        }

    def add_python_extension_paths(self, paths: list[str]):
        """Add directories to scan for Python bridge modules."""
        for path_str in paths:
            path = Path(path_str)
            if path.exists() and path.is_dir():
                self._python_extension_dirs.append(path)

        self.invalidate_cache()

    def add_ml_module_paths(self, paths: list[str]):
        """Add directories to scan for ML source modules."""
        for path_str in paths:
            path = Path(path_str)
            if path.exists() and path.is_dir():
                self._ml_module_dirs.append(path)

        self.invalidate_cache()

    def _ensure_scanned(self):
        """Ensure all directories have been scanned (lazy, thread-safe)."""
        if self._scanned:
            return

        with self._lock:
            if self._scanned:
                return

            # Scan stdlib directory for Python bridges
            self._scan_python_bridges(self._stdlib_dir)

            # Scan extension directories for Python bridges
            for ext_dir in self._python_extension_dirs:
                self._scan_python_bridges(ext_dir)

            # Scan ML module directories
            for ml_dir in self._ml_module_dirs:
                self._scan_ml_modules(ml_dir)

            self._scanned = True

    def _scan_python_bridges(self, directory: Path):
        """Scan directory for *_bridge.py modules (existing logic)."""
        for bridge_file in directory.glob("*_bridge.py"):
            if bridge_file.stem == "__init__":
                continue

            # Extract module name from @ml_module decorator
            module_name = self._extract_python_module_name(bridge_file)

            if module_name:
                if module_name in self._discovered:
                    self._handle_name_collision(module_name, bridge_file)
                    continue

                # Register Python bridge module
                metadata = UnifiedModuleMetadata(
                    name=module_name,
                    module_type=ModuleType.PYTHON_BRIDGE,
                    file_path=bridge_file,
                )
                self._discovered[module_name] = metadata

    def _scan_ml_modules(self, directory: Path, prefix: str = ""):
        """Recursively scan directory for *.ml modules.

        Args:
            directory: Directory to scan
            prefix: Module name prefix for nested directories
        """
        for ml_file in directory.glob("*.ml"):
            # Build module name: prefix + filename
            module_name = f"{prefix}.{ml_file.stem}" if prefix else ml_file.stem

            if module_name in self._discovered:
                self._handle_name_collision(module_name, ml_file)
                continue

            # Register ML source module
            metadata = UnifiedModuleMetadata(
                name=module_name,
                module_type=ModuleType.ML_SOURCE,
                file_path=ml_file,
                transpiled_path=ml_file.with_suffix('.py'),
                source_mtime=ml_file.stat().st_mtime,
            )
            self._discovered[module_name] = metadata

        # Recursively scan subdirectories
        for subdir in directory.iterdir():
            if subdir.is_dir() and not subdir.name.startswith('.'):
                # Build nested module prefix: prefix.subdir
                nested_prefix = f"{prefix}.{subdir.name}" if prefix else subdir.name
                self._scan_ml_modules(subdir, nested_prefix)

    def reload_module(self, module_name: str) -> bool:
        """Reload a module (works for both Python and ML modules)."""
        self._ensure_scanned()

        metadata = self._discovered.get(module_name)
        if not metadata:
            return False

        import time
        start = time.perf_counter()

        try:
            # Delegate to type-specific reload
            success = metadata.reload()

            if success:
                elapsed = time.perf_counter() - start
                self._record_timing("reload", module_name, elapsed)
                metadata.reload_count += 1
                logger.info(f"Reloaded {metadata.module_type.value} module: {module_name} ({elapsed*1000:.2f}ms)")
                return True
        except Exception as e:
            logger.error(f"Failed to reload module '{module_name}': {e}", exc_info=True)

        return False

    def get_module_info(self, module_name: str) -> Optional[dict]:
        """Get detailed information about a module (unified for all types)."""
        self._ensure_scanned()

        metadata = self._discovered.get(module_name)
        if not metadata:
            return None

        info = {
            'name': metadata.name,
            'type': metadata.module_type.value,
            'file_path': str(metadata.file_path),
            'loaded': metadata.instance is not None or metadata.transpiled_path is not None,
            'reload_count': metadata.reload_count,
        }

        # Type-specific info
        if metadata.module_type == ModuleType.ML_SOURCE:
            info['transpiled_path'] = str(metadata.transpiled_path) if metadata.transpiled_path else None
            info['needs_recompilation'] = metadata.needs_recompilation()
            info['source_modified'] = datetime.fromtimestamp(metadata.source_mtime).isoformat() if metadata.source_mtime else None
        elif metadata.module_type == ModuleType.PYTHON_BRIDGE:
            if metadata.instance:
                # Get functions/classes from bridge instance
                info['functions'] = self._extract_bridge_functions(metadata.instance)

        # Performance info (if available)
        if metadata.load_time:
            info['load_time_ms'] = metadata.load_time * 1000

        return info

    def get_all_modules(self, include_type: Optional[ModuleType] = None) -> dict[str, UnifiedModuleMetadata]:
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
```

### 3. ML Module Loading Implementation

```python
class UnifiedModuleMetadata:
    # ... (existing fields) ...

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
            import importlib.util
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

    def _load_python_bridge(self) -> Optional[object]:
        """Load a Python bridge module (existing logic)."""
        # ... existing Python bridge loading code ...
        pass

    def _reload_python_bridge(self) -> bool:
        """Reload a Python bridge module (existing logic)."""
        # ... existing Python bridge reload code ...
        pass
```

---

## Implementation Plan

### ✅ Phase 1: Registry Enhancement (Week 1) - **COMPLETE**
**Goal:** Extend ModuleRegistry to support ML modules

**Tasks:**
1. ✅ Add `UnifiedModuleMetadata` dataclass with `ModuleType` enum
2. ✅ Add `_ml_module_dirs` to `ModuleRegistry`
3. ✅ Implement `_scan_ml_modules()` with nested directory support
4. ✅ Add `add_ml_module_paths()` method
5. ✅ Update `get_module_info()` to handle both types

**Deliverables:**
- ✅ Registry discovers both `*_bridge.py` AND `*.ml` files
- ✅ ML modules appear in `_discovered` dict
- ✅ Separate path configuration maintained

**Testing:**
- ✅ Unit tests: ML module discovery with nested directories
- ✅ Verify collision detection between module types
- ✅ Test lazy loading for both types

### ✅ Phase 2: ML Module Loading (Week 1) - **COMPLETE**
**Goal:** Implement lazy loading and hot reloading for ML modules

**Tasks:**
1. ✅ Implement `_load_ml_module()` with transpilation
2. ✅ Implement `_reload_ml_module()` with cache invalidation
3. ✅ Add `needs_recompilation()` timestamp checking
4. ✅ Integrate with `sys.modules` for Python import compatibility

**Deliverables:**
- ✅ ML modules can be loaded on-demand
- ✅ Timestamp-based recompilation
- ✅ Hot reload without REPL restart

**Testing:**
- ✅ Test ML module loading from registry
- ✅ Test hot reload after file modification
- ✅ Test cached .py file reuse when source unchanged

### ✅ Phase 3: REPL Integration (Week 2) - **COMPLETE**
**Goal:** Make REPL commands work with both module types

**Tasks:**
1. ✅ Update `MLREPLSession.__init__()` to accept `ml_module_paths`
2. ✅ Connect `ml_module_paths` to registry via transpiler
3. ✅ Update `.modules` command to show all module types
4. ✅ Update `.modinfo` command to handle ML modules
5. ✅ Update `.reload` command to delegate by module type
6. ✅ Update `.addpath` to detect path type (Python vs ML)

**Deliverables:**
- ✅ REPL commands work seamlessly with both types
- ✅ Clear type indicators in `.modules` output
- ✅ Hot reload works for user `.ml` modules

**Testing:**
- ✅ Integration tests: REPL with mixed module types (12/13 passing)
- ✅ Test `.reload` on both Python and ML modules
- ✅ Verify `.modinfo` shows correct type-specific details
- ❌ **FAILING:** `test_repl_execution_with_ml_module_import` - discovered critical bug

### ✅ Phase 4: Configuration Unification (Week 2) - **COMPLETE**
**Goal:** Unified configuration across CLI, REPL, and project files

**Tasks:**
1. ✅ Add `ml_module_paths` to `ProjectConfig` dataclass
2. ✅ Update CLI argument parsing for `--ml-module-path`
3. ✅ Update `mlpy.json` / `mlpy.yaml` schema
4. ✅ Document configuration precedence rules

**Deliverables:**
- ✅ Consistent configuration across all entry points
- ✅ Project files support both path types
- ✅ CLI help documentation updated

**Testing:**
- ✅ Test project config loading with both path types
- ✅ Verify CLI argument precedence
- ✅ Test REPL initialization from project config

### ⚠️ **CRITICAL BUGFIX REQUIRED** - **IMMEDIATE PRIORITY**
**See:** [repl-import-bugfix.md](./repl-import-bugfix.md)

**Issue:** ML modules cannot import other ML modules
**Root Cause:** Transpiler doesn't distinguish between Python bridges and ML sources
**Impact:** Breaks modular ML development
**Timeline:** 4-7 hours
**Priority:** Must fix before Week 3

**Tasks:**
1. Add `_get_ml_module_info()` helper to PythonCodeGenerator
2. Update `visit_import_statement()` to check `ModuleType`
3. Route Python bridges to `from mlpy.stdlib import`
4. Route ML sources to `_generate_user_module_import()`
5. Fix failing test: `test_repl_execution_with_ml_module_import`

### ✅ Phase 5: Performance Monitoring (Week 3) - **COMPLETE**
**Goal:** Unified performance tracking for all modules

**Tasks:**
1. ✅ Track transpilation times for ML modules
2. ✅ Update `.perfmon` to show both Python and ML stats
3. ✅ Update `.memreport` to estimate ML module memory
4. ✅ Add type-specific performance insights
5. ✅ Update `builtin.available_modules()` to support module_type filtering
6. ✅ Update `builtin.module_info()` to query unified registry

**Deliverables:**
- ✅ Performance monitoring covers all module types
- ✅ Separate metrics for transpilation vs loading
- ✅ Identify slow transpilations and reloads
- ✅ Builtin functions query unified registry
- ✅ ML code can filter modules by type

**Testing:**
- ✅ Benchmark ML module transpilation times
- ✅ Verify performance tracking accuracy
- ✅ Test memory reporting for mixed module types
- ✅ Test builtin function filtering
- ✅ Test `.perfmon` and `.memreport` with module type breakdown

**Completion Date:** January 2026
**Implementation Time:** ~4 hours

---

## API Changes

### MLREPLSession (New Parameter)

```python
# OLD:
MLREPLSession(
    security_enabled=True,
    profile=False,
    extension_paths=["/path/to/extensions"]  # Only Python bridges
)

# NEW:
MLREPLSession(
    security_enabled=True,
    profile=False,
    extension_paths=["/path/to/extensions"],   # Python bridges
    ml_module_paths=["./src", "./lib"]         # NEW: ML modules
)
```

### MLTranspiler (New Parameter)

```python
# OLD:
MLTranspiler(
    repl_mode=False,
    python_extension_paths=[...]  # Only Python bridges
)

# NEW:
MLTranspiler(
    repl_mode=False,
    python_extension_paths=[...],  # Python bridges
    ml_module_paths=[...]          # NEW: ML modules
)
```

### Project Configuration (Extended Schema)

```yaml
# mlpy.yaml
name: "my-project"
version: "1.0.0"

# Python extension modules (trusted third-party)
python_extension_paths:
  - "/usr/local/mlpy/extensions"
  - "./extensions"

# ML user modules (project code) - NEW
ml_module_paths:
  - "./src"
  - "./lib"
  - "./modules"

# Security settings
allowed_capabilities:
  - "file_read"
  - "file_write"
```

### CLI Arguments (New Flag)

```bash
# OLD:
mlpy run main.ml --extension-path /path/to/extensions

# NEW:
mlpy run main.ml \
  --extension-path /path/to/extensions \
  --ml-module-path ./src:./lib       # NEW: Colon-separated paths
```

---

## Builtin Stdlib Functions Integration

### Current Limitation

The ML language provides builtin functions for runtime module detection, but they currently only query Python bridge modules from the registry:

```ml
// Current implementation (incomplete)
modules = builtin.available_modules();  // Only returns Python bridges!
print(modules);  // ["math", "random", "json", "datetime", ...]

info = builtin.module_info("math");  // Works for Python bridges
print(info);  // {name: "math", type: "python_bridge", loaded: true}

ml_info = builtin.module_info("user_modules.sorting");
print(ml_info);  // null - ML module not found! ❌
```

### Required Changes

The builtin functions must be updated to query the **unified registry** instead of just the Python bridge registry:

#### 1. `builtin.available_modules()` - Enhanced Implementation

**Location:** `src/mlpy/stdlib/builtin_bridge.py`

```python
# OLD implementation (Python bridges only):
@ml_function(name="available_modules")
def _available_modules(self) -> list[str]:
    """Get list of available Python bridge modules."""
    from mlpy.stdlib.module_registry import get_registry
    registry = get_registry()
    return sorted(registry.get_all_module_names())  # Only Python bridges!

# NEW implementation (unified registry):
@ml_function(name="available_modules")
def _available_modules(self, module_type: Optional[str] = None) -> list[str]:
    """Get list of available modules, optionally filtered by type.

    Args:
        module_type: Optional filter - "python_bridge", "ml_source", or null for all

    Returns:
        Sorted list of module names

    Examples:
        available_modules()              // All modules
        available_modules("python_bridge")  // Only Python bridges
        available_modules("ml_source")      // Only ML modules
    """
    from mlpy.stdlib.module_registry import get_registry, ModuleType
    registry = get_registry()

    if module_type is None:
        # Return all modules
        return sorted(registry.get_all_module_names())

    # Filter by type
    type_enum = ModuleType(module_type)
    modules = registry.get_all_modules(include_type=type_enum)
    return sorted(modules.keys())
```

**ML Usage Examples:**

```ml
// Get all modules (both types)
all_modules = builtin.available_modules();
print(all_modules);
// ["data.models", "datetime", "json", "math", "user_modules.sorting", "utils", ...]

// Get only Python bridge modules
python_modules = builtin.available_modules("python_bridge");
print(python_modules);
// ["datetime", "json", "math", "random", ...]

// Get only ML source modules
ml_modules = builtin.available_modules("ml_source");
print(ml_modules);
// ["data.models", "user_modules.sorting", "utils", ...]

// Use in conditionals
if (builtin.available_modules("ml_source").includes("utils")) {
    import utils;
    utils.helper_function();
}
```

#### 2. `builtin.module_info()` - Enhanced Implementation

**Location:** `src/mlpy/stdlib/builtin_bridge.py`

```python
# OLD implementation (Python bridges only):
@ml_function(name="module_info")
def _module_info(self, module_name: str) -> Optional[dict]:
    """Get information about a Python bridge module."""
    from mlpy.stdlib.module_registry import get_registry
    registry = get_registry()

    if not registry.is_available(module_name):
        return None

    # Returns limited Python bridge info only
    return {
        'name': module_name,
        'loaded': True  # Simplified
    }

# NEW implementation (unified registry):
@ml_function(name="module_info")
def _module_info(self, module_name: str) -> Optional[dict]:
    """Get detailed information about any module (Python or ML).

    Args:
        module_name: Name of the module to query

    Returns:
        Dictionary with module metadata or null if not found

    Examples:
        module_info("math")                    // Python bridge info
        module_info("user_modules.sorting")    // ML module info
    """
    from mlpy.stdlib.module_registry import get_registry
    registry = get_registry()

    # Query unified registry (handles both types)
    return registry.get_module_info(module_name)
```

**ML Usage Examples:**

```ml
// Query Python bridge module
math_info = builtin.module_info("math");
print(math_info);
// {
//   name: "math",
//   type: "python_bridge",
//   file_path: "/usr/local/mlpy/stdlib/math_bridge.py",
//   loaded: true,
//   reload_count: 0,
//   load_time_ms: 2.1,
//   functions: ["sqrt", "pow", "sin", "cos", ...]
// }

// Query ML source module
utils_info = builtin.module_info("user_modules.sorting");
print(utils_info);
// {
//   name: "user_modules.sorting",
//   type: "ml_source",
//   file_path: "/project/src/user_modules/sorting.ml",
//   transpiled_path: "/project/src/user_modules/sorting.py",
//   loaded: true,
//   needs_recompilation: false,
//   source_modified: "2026-01-15T14:23:45",
//   reload_count: 2,
//   load_time_ms: 45.2
// }

// Check if module needs recompilation
info = builtin.module_info("utils");
if (info && info.needs_recompilation) {
    print("Warning: utils.ml has been modified and needs recompilation");
}

// Defensive programming
module_name = "my_module";
info = builtin.module_info(module_name);

if (info == null) {
    print("Module not found: " + module_name);
} else if (info.type == "ml_source" && info.needs_recompilation) {
    print("Reloading " + module_name + "...");
    // Trigger reload via REPL command or programmatic API
}
```

#### 3. New Builtin Function: `builtin.reload_module()` (Optional)

**Programmatic Module Reloading from ML Code:**

```python
# NEW function for programmatic hot reload
@ml_function(name="reload_module")
def _reload_module(self, module_name: str) -> dict:
    """Programmatically reload a module (Python or ML).

    Args:
        module_name: Name of the module to reload

    Returns:
        Dictionary with reload status and timing

    Examples:
        reload_module("user_modules.sorting")  // Hot reload ML module
        reload_module("math")                  // Reload Python bridge
    """
    from mlpy.stdlib.module_registry import get_registry
    import time

    registry = get_registry()
    start = time.perf_counter()

    success = registry.reload_module(module_name)
    elapsed = (time.perf_counter() - start) * 1000  # Convert to ms

    return {
        'success': success,
        'module_name': module_name,
        'reload_time_ms': elapsed
    }
```

**ML Usage Example:**

```ml
// Programmatic hot reload from ML code
function reload_if_changed(module_name) {
    info = builtin.module_info(module_name);

    if (info && info.needs_recompilation) {
        print("Reloading " + module_name + "...");
        result = builtin.reload_module(module_name);

        if (result.success) {
            print("✓ Reloaded in " + result.reload_time_ms + "ms");
        } else {
            print("✗ Reload failed");
        }
    }
}

// Auto-reload workflow
reload_if_changed("user_modules.sorting");
reload_if_changed("utils");
reload_if_changed("helpers.validation");
```

### Integration with REPL Commands

The REPL commands (`.modules`, `.modinfo`, `.reload`) should use the **same builtin functions** under the hood to ensure consistency:

```python
# src/mlpy/cli/repl.py

def _cmd_modules(self):
    """List all available modules."""
    # Use builtin function for consistency
    from mlpy.stdlib.builtin_bridge import get_builtin_module
    builtin = get_builtin_module()

    all_modules = builtin._available_modules()  # All types
    python_modules = builtin._available_modules("python_bridge")
    ml_modules = builtin._available_modules("ml_source")

    print(f"Available Modules ({len(all_modules)} total):\n")

    if python_modules:
        print(f"  Python Bridges ({len(python_modules)}):")
        for name in python_modules:
            print(f"    • {name}")

    if ml_modules:
        print(f"\n  ML Modules ({len(ml_modules)}):")
        for name in ml_modules:
            print(f"    • {name}")

def _cmd_modinfo(self, module_name: str):
    """Show detailed module information."""
    from mlpy.stdlib.builtin_bridge import get_builtin_module
    builtin = get_builtin_module()

    info = builtin._module_info(module_name)  # Use builtin function

    if not info:
        print(f"Module '{module_name}' not found")
        return

    # Format and display info...
    print(f"Module: {info['name']}")
    print(f"Type: {info['type']}")
    # ... etc
```

### Testing Requirements

**Unit Tests for Builtin Functions:**

```python
# tests/unit/stdlib/test_builtin_module_detection.py

def test_available_modules_returns_all_types():
    """Test that available_modules() returns both Python and ML modules."""
    builtin = get_builtin_module()

    # Should include both types
    all_modules = builtin._available_modules()
    assert "math" in all_modules  # Python bridge
    assert "user_modules.sorting" in all_modules  # ML module

def test_available_modules_filters_by_type():
    """Test filtering by module type."""
    builtin = get_builtin_module()

    python_only = builtin._available_modules("python_bridge")
    assert "math" in python_only
    assert "user_modules.sorting" not in python_only

    ml_only = builtin._available_modules("ml_source")
    assert "user_modules.sorting" in ml_only
    assert "math" not in ml_only

def test_module_info_returns_ml_module_details():
    """Test that module_info() works for ML modules."""
    builtin = get_builtin_module()

    info = builtin._module_info("user_modules.sorting")
    assert info is not None
    assert info['type'] == "ml_source"
    assert info['file_path'].endswith(".ml")
    assert 'transpiled_path' in info
    assert 'needs_recompilation' in info

def test_module_info_returns_none_for_missing():
    """Test that module_info() returns None for non-existent modules."""
    builtin = get_builtin_module()

    info = builtin._module_info("nonexistent_module")
    assert info is None
```

**Integration Tests:**

```python
# tests/integration/test_builtin_module_detection.py

def test_ml_code_can_query_modules():
    """Test ML code using builtin.available_modules()."""
    ml_code = """
    modules = builtin.available_modules();
    print(modules.length);
    """

    result = run_ml_code(ml_code)
    assert result.success
    assert int(result.output) > 0  # At least some modules found

def test_ml_code_can_check_module_info():
    """Test ML code using builtin.module_info()."""
    ml_code = """
    info = builtin.module_info("math");
    if (info != null) {
        print(info.type);
    }
    """

    result = run_ml_code(ml_code)
    assert result.success
    assert result.output.strip() == "python_bridge"
```

### Migration Impact

**Backward Compatibility:** ✅ Maintained

Existing ML code using `builtin.available_modules()` and `builtin.module_info()` will continue to work:

```ml
// OLD code (still works):
modules = builtin.available_modules();  // Now returns ALL modules

// NEW code (enhanced functionality):
modules = builtin.available_modules("python_bridge");  // Filter by type
info = builtin.module_info("user_modules.sorting");  // Now works for ML modules!
```

**No Breaking Changes:**
- Function signatures extended with optional parameters
- Return values enhanced but maintain same structure
- Existing code gets improved functionality automatically

---

## REPL Command Examples

### Unified .modules Command

```python
mlpy> .modules
Available Modules (15 total):

  Python Bridges (8):
    • math
    • random
    • json
    • datetime
    • functional
    • regex
    • console
    • http

  ML Modules (7):
    • user_modules.sorting
    • user_modules.algorithms.quicksort
    • utils
    • helpers.validation
    • helpers.formatting
    • data.models
    • data.transforms

Use .modinfo <name> to see details
```

### Enhanced .modinfo Command

```python
mlpy> .modinfo user_modules.sorting
Module: user_modules.sorting
Type: ML Source Module
File: /project/src/user_modules/sorting.ml
Transpiled: /project/src/user_modules/sorting.py
Loaded: Yes
Needs Recompilation: No
Last Modified: 2026-01-15 14:23:45
Reload Count: 2
Load Time: 45.2ms

Functions (5):
  • swap(arr, i, j) - Swap two array elements
  • quicksort(arr) - Quick sort implementation
  • bubble_sort(arr) - Bubble sort implementation
  • is_sorted(arr) - Check if array is sorted
  • reverse(arr) - Reverse array in place

mlpy> .modinfo math
Module: math
Type: Python Bridge Module
File: /usr/local/mlpy/stdlib/math_bridge.py
Loaded: Yes
Reload Count: 0
Load Time: 2.1ms

Functions (15):
  • sqrt(x) - Square root
  • pow(base, exp) - Power function
  • sin(x) - Sine function
  ... (12 more)
```

### Unified .reload Command

```python
# Edit user_modules/sorting.ml...

mlpy> .reload user_modules.sorting
[Transpiling user_modules/sorting.ml...]
[Recompiling to Python...]
[Reloading module...]
✓ Reloaded ML module: user_modules.sorting (48.3ms)

mlpy> .reload math
✓ Reloaded Python bridge module: math (2.5ms)
```

### Smart .addpath Command

```python
mlpy> .addpath /path/to/extensions
[Scanning for Python bridge modules (*_bridge.py)...]
✓ Found 3 Python bridge modules
✓ Added extension path: /path/to/extensions

mlpy> .addpath ./my_modules
[Scanning for ML source modules (*.ml)...]
✓ Found 5 ML modules (including nested)
✓ Added ML module path: ./my_modules

mlpy> .addpath ./mixed_modules --auto-detect
[Auto-detecting module types...]
✓ Found 2 Python bridge modules
✓ Found 3 ML modules
✓ Added to appropriate registries
```

### Enhanced .perfmon Command

```python
mlpy> .perfmon
Performance Summary:

  Python Bridge Modules:
    Total loads: 5
    Avg load time: 3.2ms
    Slowest: regex (5.1ms)

  ML Modules:
    Total transpilations: 3
    Avg transpilation time: 42.8ms
    Total reloads: 7
    Avg reload time: 38.5ms
    Slowest transpile: user_modules.algorithms.quicksort (87.2ms) ⚠️ SLOW

  Overall:
    Total module operations: 15
    Cache hit rate: 73%
```

---

## Migration Guide

### For Existing Projects

#### Step 1: Update Configuration Files

```yaml
# OLD mlpy.yaml:
python_extension_paths:
  - "./extensions"

# NEW mlpy.yaml:
python_extension_paths:
  - "./extensions"

ml_module_paths:  # ADD THIS
  - "./src"
  - "./lib"
```

#### Step 2: Update REPL Initialization

```python
# OLD:
from mlpy.cli.repl import run_repl
run_repl(extension_paths=["./extensions"])

# NEW:
from mlpy.cli.repl import run_repl
run_repl(
    extension_paths=["./extensions"],      # Python bridges
    ml_module_paths=["./src", "./lib"]    # ML modules
)
```

#### Step 3: Use Enhanced REPL Commands

```python
# Now works!
mlpy> .modules  # Shows BOTH Python bridges and ML modules
mlpy> .reload my_ml_module  # Hot reload works!
mlpy> .modinfo my_ml_module  # Shows ML module details
```

### Backward Compatibility

✅ **No Breaking Changes:**
- Existing `python_extension_paths` still works
- Import statements unchanged
- Python bridge modules unaffected
- Existing projects continue working

✅ **Opt-In Enhancement:**
- ML modules work as before (via transpiler `import_paths`)
- Adding `ml_module_paths` enables enhanced REPL features
- Gradual migration supported

---

## Security Considerations

### Separate Trust Boundaries

**Python Bridge Modules:**
- Require `@ml_module` decorator (explicit opt-in)
- Registered with `SafeAttributeRegistry`
- Assumed trusted (vetted third-party code)
- Security validation at decoration time

**ML Modules:**
- Full transpilation pipeline with security analysis
- Capability enforcement at runtime
- Assumed untrusted (user code)
- Security validation at compile time

### Path Isolation

**Python Extension Paths:**
- Typically system-wide or project-wide
- Example: `/usr/local/mlpy/extensions`, `./node_modules/@mlpy/`
- High trust level

**ML Module Paths:**
- Project-specific source directories
- Example: `./src`, `./lib`, `./modules`
- User code trust level

### Collision Handling

When both a Python bridge and ML module have the same name:

```python
# Priority: Python bridges win (more specific/trusted)
# Warning logged for visibility

logger.warning(
    f"Module name collision: '{name}' found as both "
    f"Python bridge ({bridge_file}) and ML module ({ml_file}). "
    f"Using Python bridge module."
)
```

**Rationale:**
- Python bridges are explicitly decorated (intentional)
- ML modules may have generic names (accidental collision)
- Developers can rename ML modules easily

---

## Testing Strategy

### Unit Tests (New)

1. **ML Module Discovery:**
   - Test recursive directory scanning
   - Test nested module name construction
   - Test collision detection

2. **ML Module Loading:**
   - Test transpilation on first load
   - Test cached .py file reuse
   - Test timestamp-based recompilation

3. **ML Module Reloading:**
   - Test source modification detection
   - Test sys.modules invalidation
   - Test AST cache clearing

### Integration Tests (New)

1. **Mixed Module Registry:**
   - Load both Python bridges and ML modules
   - Verify unified `.modules` output
   - Test `.reload` on both types

2. **REPL Workflow:**
   - Initialize REPL with both path types
   - Import mixed module types
   - Hot reload ML module after edit
   - Verify performance tracking

3. **CLI Integration:**
   - Test `--ml-module-path` argument
   - Test project config loading
   - Verify path precedence rules

### Performance Tests (New)

1. **ML Transpilation Benchmarks:**
   - Measure transpilation overhead
   - Test cache effectiveness
   - Profile hot reload performance

2. **Registry Scalability:**
   - Test with 100+ ML modules
   - Measure scan time impact
   - Verify lazy loading benefits

---

## Success Criteria

### Functional Requirements

- [ ] ML modules appear in `.modules` command output
- [ ] `.reload <ml_module>` hot reloads ML modules
- [ ] `.modinfo <ml_module>` shows ML module details
- [ ] `.perfmon` tracks ML module transpilation times
- [ ] `.addpath` detects ML modules automatically
- [ ] Nested ML modules work (`user.submodule.name`)
- [ ] Import statements work for both module types

### Performance Requirements

- [ ] ML module discovery: <100ms for 100 modules
- [ ] ML module hot reload: <500ms including transpilation
- [ ] Registry overhead: <10ms for 100 modules
- [ ] Cache hit rate: >90% for unchanged ML modules

### User Experience Requirements

- [ ] Clear type indicators in `.modules` output
- [ ] Helpful error messages for collisions
- [ ] Consistent command syntax across module types
- [ ] Zero breaking changes for existing projects

---

## Future Enhancements

### Phase 2 (Post-Initial Release)

1. **File Watching:**
   ```python
   mlpy> .watch user_modules.sorting
   [Watching /project/src/user_modules/sorting.ml]
   [File changed - auto-transpiling...]
   ✓ Module reloaded automatically
   ```

2. **Dependency Tracking:**
   ```python
   mlpy> .modinfo utils
   Dependencies (3):
     • helpers.validation
     • data.models
     • math (Python bridge)

   Dependents (2):
     • main
     • user_modules.sorting
   ```

3. **Module Groups:**
   ```python
   mlpy> .reloadgroup data
   [Reloading module group 'data'...]
   ✓ data.models (ML)
   ✓ data.transforms (ML)
   ✓ data.validation (ML)
   ```

4. **Smart Caching:**
   - AST cache persistence across REPL sessions
   - Incremental transpilation for changed functions
   - Shared .py cache across multiple REPL sessions

---

## Conclusion

This proposal unifies the module detection, inspection, and reloading experience across **Python extension modules** and **user-defined ML modules** while maintaining the architectural benefits of separate search path configuration.

**Key Benefits:**
- ✅ Seamless developer experience: REPL commands work with all modules
- ✅ Clear separation: Different trust levels, different paths
- ✅ Hot reloading: No REPL restart needed for ML module changes
- ✅ Performance monitoring: Unified tracking across all module types
- ✅ Zero breaking changes: Backward compatible with existing code

**Implementation Timeline:** 3 weeks
- Week 1: Registry enhancement + ML loading
- Week 2: REPL integration + configuration
- Week 3: Performance monitoring + testing

**Priority:** High - Significantly improves developer experience for ML module development without compromising security or architectural clarity.

---

**Document Status:** Ready for Review
**Next Steps:** Team review → Approval → Implementation kickoff
**Questions/Feedback:** Contact Architecture Team
