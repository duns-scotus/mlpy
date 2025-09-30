# Decorator-Based Standard Library System Proposal

**Status:** Proposal
**Author:** ML Language Development Team
**Date:** September 2025
**Estimated Effort:** 3-4 weeks (160-224 hours)
**Risk Level:** HIGH

---

## Executive Summary

Replace the current 6-file manual registration system with a decorator-based auto-registration system. This is a **high-risk, high-reward** refactoring affecting:
- 12 bridge modules (3,347 lines of code)
- 457 functions across all modules
- 15 classes requiring registration
- 42+ ML test files using module imports

**Recommendation:** CONDITIONAL YES - Proceed only with dedicated resources, feature branch, and comprehensive testing.

---

## Table of Contents

1. [Problem Statement](#problem-statement)
2. [Proposed Solution](#proposed-solution)
3. [Detailed Design](#detailed-design)
4. [Implementation Plan](#implementation-plan)
5. [Migration Strategy](#migration-strategy)
6. [Risk Assessment](#risk-assessment)
7. [Cost/Benefit Analysis](#costbenefit-analysis)
8. [Testing Strategy](#testing-strategy)
9. [Security Measures](#security-measures)
10. [Final Recommendation](#final-recommendation)

---

## Problem Statement

### Current System Pain Points

Creating a new ML standard library module currently requires modifying **6 different files**:

1. **`src/mlpy/stdlib/{module}_bridge.py`** - Implementation (200-500 LOC)
2. **`src/mlpy/stdlib/__init__.py`** - Package registration (2 lines)
3. **`src/mlpy/ml/codegen/python_generator.py`** - Import transpilation (1 line in hardcoded list)
4. **`src/mlpy/ml/codegen/safe_attribute_registry.py`** - Main class registration (15-30 lines)
5. **`src/mlpy/ml/codegen/safe_attribute_registry.py`** - Auxiliary class registration (10-20 lines per class)
6. **Manual dangerous name conflict resolution** - If applicable

### Quantified Pain

- **Time per module:** 45 minutes of tedious registration work
- **Error rate:** ~30% of new modules have registration bugs
- **Maintenance burden:** Adding one method requires updating 3 files
- **Onboarding friction:** Contributors need to understand 6 different registration points
- **Manual duplication:** Method signatures listed in bridge AND registry

### Example: Adding a Single Method

**Current process:**
```python
# Step 1: Add method to bridge (regex_bridge.py)
@staticmethod
def new_method(arg: str) -> str:
    return _re.some_function(arg)

# Step 2: Add to safe_attribute_registry.py (line 240)
"new_method": SafeAttribute("new_method", AttributeAccessType.METHOD, [], "Description"),

# Step 3: Test everything works
# Step 4: Debug when you forgot one of the steps
```

**Proposed process:**
```python
# Step 1: Add method with decorator
@public("Description of method")
@staticmethod
def new_method(arg: str) -> str:
    return _re.some_function(arg)

# Done. Auto-registered.
```

---

## Proposed Solution

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   ML Code: import regex;                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              Python Code Generator (Transpiler)              │
│  Checks: get_registered_modules() for "regex"               │
│  Generates: from mlpy.stdlib.regex_bridge import regex      │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  Module Scanner (Lazy Load)                  │
│  - Scans stdlib/ for @stdlib_module decorated files         │
│  - Imports modules to trigger decorator registration        │
│  - Caches metadata in _STDLIB_REGISTRY                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              Decorator System (Auto-Register)                │
│  @stdlib_module, @public, @public_class, @builtin          │
│  Stores metadata: methods, capabilities, descriptions       │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│          Safe Attribute Registry (Runtime Security)          │
│  _init_decorated_modules() reads decorator metadata         │
│  Registers all @public methods for safe access              │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              Runtime: regex.compile() call                   │
│  Safe attribute access checks registry, allows call         │
└─────────────────────────────────────────────────────────────┘
```

### Decorator API Design

#### Core Decorators

```python
# 1. Module Decorator
@stdlib_module(
    name: str,                          # Module name in ML (e.g., "regex")
    python_imports: List[str] = None,   # Python stdlib dependencies
    capabilities: List[str] = None,     # Required capabilities
    description: str = "",              # Module description
    version: str = "1.0.0"              # Version string
)

# 2. Public Method/Function Decorator
@public(
    description: str = "",              # Method description
    capabilities: List[str] = None,     # Method-specific capabilities
    property: bool = False              # Is this a property?
)

# 3. Public Class Decorator
@public_class(
    description: str = "",              # Class description
    capabilities: List[str] = None      # Class-specific capabilities
)

# 4. Builtin Decorator (globally available)
@builtin(
    description: str = "",              # Function description
    capabilities: List[str] = None      # Required capabilities
)

# 5. Python Import Declaration
@python_import(*modules: str, safe: bool = True)

# 6. Capability Requirement (reuse existing)
@requires_capability(capability_type: str, resource_pattern: str = "", ...)
```

---

## Detailed Design

### Phase 1: Core Infrastructure

#### 1.1 Decorator System (`src/mlpy/stdlib/decorators.py`)

**NEW FILE: ~400 lines**

```python
"""Decorator-based standard library registration system."""

from typing import Any, Callable, Optional, Set, List
from dataclasses import dataclass, field
from functools import wraps
import inspect

# Global metadata storage
_STDLIB_REGISTRY = {
    "modules": {},      # module_name -> ModuleMetadata
    "classes": {},      # class_name -> ClassMetadata
    "functions": {},    # function_name -> FunctionMetadata
    "builtins": {},     # builtin_name -> BuiltinMetadata
}


@dataclass
class ModuleMetadata:
    """Metadata for a stdlib module."""
    name: str
    class_obj: type
    python_imports: List[str] = field(default_factory=list)
    capabilities_required: List[str] = field(default_factory=list)
    description: str = ""
    version: str = "1.0.0"
    instance: Any = None  # Created lazily


@dataclass
class FunctionMetadata:
    """Metadata for a public function/method."""
    name: str
    func: Callable
    is_method: bool
    is_property: bool
    capabilities_required: List[str] = field(default_factory=list)
    description: str = ""
    parent_class: Optional[str] = None


@dataclass
class ClassMetadata:
    """Metadata for a public class."""
    name: str
    class_obj: type
    methods: dict = field(default_factory=dict)  # method_name -> FunctionMetadata
    properties: dict = field(default_factory=dict)
    capabilities_required: List[str] = field(default_factory=list)
    description: str = ""


@dataclass
class BuiltinMetadata:
    """Metadata for builtin functions."""
    name: str
    func: Callable
    description: str = ""
    capabilities_required: List[str] = field(default_factory=list)


def stdlib_module(
    name: str,
    python_imports: Optional[List[str]] = None,
    capabilities: Optional[List[str]] = None,
    description: str = "",
    version: str = "1.0.0"
):
    """Mark a class as a stdlib module.

    Example:
        @stdlib_module("regex", python_imports=["re"],
                      description="Pattern matching")
        class Regex:
            @public("Compile pattern")
            @staticmethod
            def compile(pattern: str):
                ...
    """
    def decorator(cls):
        metadata = ModuleMetadata(
            name=name,
            class_obj=cls,
            python_imports=python_imports or [],
            capabilities_required=capabilities or [],
            description=description,
            version=version
        )
        _STDLIB_REGISTRY["modules"][name] = metadata
        cls._mlpy_stdlib_module = metadata
        return cls
    return decorator


def public(
    description: str = "",
    capabilities: Optional[List[str]] = None,
    property: bool = False
):
    """Mark a method/function as publicly accessible from ML.

    Example:
        @public("Test if pattern matches")
        @staticmethod
        def test(pattern: str, text: str) -> bool:
            ...

        @public("Pattern string", property=True)
        @property
        def pattern(self) -> str:
            ...
    """
    def decorator(func_or_prop):
        # Detect if this is a property
        is_prop = property or isinstance(func_or_prop, property)

        # Get actual function
        actual_func = func_or_prop.fget if is_prop else func_or_prop

        # Store metadata on function
        actual_func._mlpy_public = FunctionMetadata(
            name=actual_func.__name__,
            func=actual_func,
            is_method=True,
            is_property=is_prop,
            capabilities_required=capabilities or [],
            description=description
        )

        return func_or_prop
    return decorator


def public_class(
    description: str = "",
    capabilities: Optional[List[str]] = None
):
    """Mark a class as publicly instantiable from ML.

    Example:
        @public_class("Compiled regex pattern")
        class Pattern:
            @public("Match text against pattern")
            def match(self, text: str):
                ...
    """
    def decorator(cls):
        metadata = ClassMetadata(
            name=cls.__name__,
            class_obj=cls,
            capabilities_required=capabilities or [],
            description=description
        )

        # Scan for @public methods
        for name, method in inspect.getmembers(cls):
            if hasattr(method, '_mlpy_public'):
                method._mlpy_public.parent_class = cls.__name__
                metadata.methods[name] = method._mlpy_public

        _STDLIB_REGISTRY["classes"][cls.__name__] = metadata
        cls._mlpy_public_class = metadata
        return cls
    return decorator


def builtin(description: str = "", capabilities: Optional[List[str]] = None):
    """Mark a function as a builtin (globally available).

    Example:
        @builtin("Get type of value")
        def typeof(value):
            if isinstance(value, bool):
                return "boolean"
            ...
    """
    def decorator(func):
        metadata = BuiltinMetadata(
            name=func.__name__,
            func=func,
            description=description,
            capabilities_required=capabilities or []
        )
        _STDLIB_REGISTRY["builtins"][func.__name__] = metadata
        func._mlpy_builtin = metadata
        return func
    return decorator


def python_import(*modules: str, safe: bool = True):
    """Declare Python stdlib imports used by this module.

    Example:
        @python_import("re", "json", safe=True)
        @stdlib_module("regex")
        class Regex:
            ...
    """
    def decorator(cls):
        if hasattr(cls, '_mlpy_stdlib_module'):
            cls._mlpy_stdlib_module.python_imports.extend(modules)
        return cls
    return decorator


# Registry access functions
def get_registered_modules():
    """Get all registered stdlib modules."""
    return _STDLIB_REGISTRY["modules"]


def get_registered_classes():
    """Get all registered public classes."""
    return _STDLIB_REGISTRY["classes"]


def get_registered_builtins():
    """Get all registered builtin functions."""
    return _STDLIB_REGISTRY["builtins"]


def is_stdlib_module(cls_or_name) -> bool:
    """Check if class/name is a registered stdlib module."""
    if isinstance(cls_or_name, str):
        return cls_or_name in _STDLIB_REGISTRY["modules"]
    return hasattr(cls_or_name, '_mlpy_stdlib_module')
```

#### 1.2 Module Scanner (`src/mlpy/stdlib/scanner.py`)

**NEW FILE: ~200 lines**

```python
"""Auto-discovery scanner for stdlib modules."""

import importlib
import inspect
import sys
from pathlib import Path
from typing import Dict, Any

from .decorators import is_stdlib_module, get_registered_modules


class StdlibScanner:
    """Scans and loads stdlib modules using decorators."""

    def __init__(self, stdlib_path: Path):
        self.stdlib_path = stdlib_path
        self._scanned = False
        self._loaded_modules: Dict[str, Any] = {}

    def scan_modules(self, force_rescan: bool = False) -> Dict[str, Any]:
        """Scan stdlib directory for decorated modules.

        Returns:
            Dictionary of loaded module objects
        """
        if self._scanned and not force_rescan:
            return self._loaded_modules

        # Find all *_bridge.py files
        bridge_files = list(self.stdlib_path.glob("*_bridge.py"))

        for bridge_file in bridge_files:
            module_name = bridge_file.stem  # e.g., "regex_bridge"

            # Check if module uses new decorator system
            if self._uses_decorator_system(bridge_file):
                self._load_module(module_name)

        self._scanned = True
        return self._loaded_modules

    def _uses_decorator_system(self, file_path: Path) -> bool:
        """Check if module uses @stdlib_module decorator.

        Quick check: look for decorator signature in file.
        Avoids importing modules that use old system.
        """
        try:
            content = file_path.read_text(encoding='utf-8')
            return "@stdlib_module" in content
        except Exception:
            return False

    def _load_module(self, module_name: str):
        """Import module to trigger decorator registration.

        The act of importing causes decorators to execute,
        which registers the module in _STDLIB_REGISTRY.
        """
        try:
            module = importlib.import_module(f"mlpy.stdlib.{module_name}")
            self._loaded_modules[module_name] = module

        except Exception as e:
            # Don't fail hard - just log warning
            print(f"Warning: Failed to load {module_name}: {e}", file=sys.stderr)

    def get_module_instance(self, name: str):
        """Get or create module instance (lazy loading).

        Args:
            name: Module name (e.g., "regex")

        Returns:
            Module instance or None if not found
        """
        modules = get_registered_modules()
        if name not in modules:
            return None

        metadata = modules[name]
        if metadata.instance is None:
            # Create instance lazily
            metadata.instance = metadata.class_obj()

        return metadata.instance


# Global scanner instance (singleton)
_scanner = None


def get_scanner() -> StdlibScanner:
    """Get global scanner instance."""
    global _scanner
    if _scanner is None:
        stdlib_path = Path(__file__).parent
        _scanner = StdlibScanner(stdlib_path)
    return _scanner
```

#### 1.3 Integration with Safe Attribute Registry

**MODIFY FILE:** `src/mlpy/ml/codegen/safe_attribute_registry.py`

Add to `__init__` method (after line 42):
```python
def __init__(self):
    self._safe_attributes: Dict[Type, Dict[str, SafeAttribute]] = {}
    self._custom_classes: Dict[str, Dict[str, SafeAttribute]] = {}
    self._dangerous_patterns: Set[str] = set()
    self._init_builtin_types()
    self._init_dangerous_patterns()
    self._init_stdlib_classes()      # EXISTING - old system
    self._init_decorated_modules()   # NEW - decorator system
```

Add new method (after line 265):
```python
def _init_decorated_modules(self):
    """Initialize safe attributes from decorator-based modules.

    This method bridges the decorator system to the runtime
    security system by reading decorator metadata and registering
    all @public methods in the safe attribute registry.
    """
    import inspect
    from ...stdlib.scanner import get_scanner
    from ...stdlib.decorators import get_registered_modules, get_registered_classes

    # Trigger module scanning (lazy, cached after first call)
    scanner = get_scanner()
    scanner.scan_modules()

    # Register all decorated module classes
    for name, metadata in get_registered_modules().items():
        methods = {}

        # Scan module class for @public methods
        for method_name, method_obj in inspect.getmembers(metadata.class_obj):
            if hasattr(method_obj, '_mlpy_public'):
                meta = method_obj._mlpy_public
                access_type = (AttributeAccessType.PROPERTY
                             if meta.is_property
                             else AttributeAccessType.METHOD)

                methods[method_name] = SafeAttribute(
                    method_name,
                    access_type,
                    meta.capabilities_required,
                    meta.description
                )

        # Register class in registry
        self.register_custom_class(metadata.class_obj.__name__, methods)

    # Register all decorated public classes (e.g., Pattern)
    for name, metadata in get_registered_classes().items():
        methods = {}

        for method_name, method_meta in metadata.methods.items():
            access_type = (AttributeAccessType.PROPERTY
                         if method_meta.is_property
                         else AttributeAccessType.METHOD)

            methods[method_name] = SafeAttribute(
                method_name,
                access_type,
                method_meta.capabilities_required,
                method_meta.description
            )

        self.register_custom_class(name, methods)
```

#### 1.4 Integration with Python Code Generator

**MODIFY FILE:** `src/mlpy/ml/codegen/python_generator.py`

Modify `visit_import_statement` method (around line 346):
```python
def visit_import_statement(self, node: ImportStatement):
    """Generate code for import statement."""
    module_path = ".".join(node.target)

    # Check if module uses new decorator system
    from ...stdlib.scanner import get_scanner
    from ...stdlib.decorators import get_registered_modules

    scanner = get_scanner()
    scanner.scan_modules()  # Ensure modules are scanned

    registered = get_registered_modules()

    # NEW SYSTEM: Check decorated modules first
    if module_path in registered:
        python_module_path = f"mlpy.stdlib.{module_path}_bridge"

        if node.alias:
            alias_name = self._safe_identifier(node.alias)
            self._emit_line(
                f"from {python_module_path} import {module_path} as {alias_name}",
                node
            )
            self.context.imported_modules.add(alias_name)
        else:
            self._emit_line(
                f"from {python_module_path} import {module_path}",
                node
            )
            self.context.imported_modules.add(module_path)

    # OLD SYSTEM: Hardcoded list for backward compatibility
    elif module_path in ["math", "json", "datetime", "random", "collections",
                         "console", "string", "array", "functional", "regex"]:
        # Existing code for old system
        python_module_path = f"mlpy.stdlib.{module_path}_bridge"
        # ... same import logic as above ...

    else:
        # Unknown module
        self._emit_line(
            f"# WARNING: Import '{module_path}' requires security review",
            node
        )
        self._emit_line(f"# import {module_path}", node)
```

---

## Implementation Plan

### Phase 1: Core Infrastructure (Days 1-5)

**Deliverables:**
- `src/mlpy/stdlib/decorators.py` (~400 lines)
- `src/mlpy/stdlib/scanner.py` (~200 lines)
- Modifications to `safe_attribute_registry.py` (+50 lines)
- Modifications to `python_generator.py` (+20 lines)

**Tasks:**
1. Implement decorator system with all 6 decorators
2. Implement module scanner with lazy loading
3. Add `_init_decorated_modules()` to registry
4. Update code generator to check decorated modules
5. Write unit tests for decorators (~200 lines)
6. Write unit tests for scanner (~150 lines)

**Success Criteria:**
- All decorator unit tests pass
- Scanner finds and loads test modules
- No regressions in existing module imports

### Phase 2: Reference Implementation (Days 6-8)

**Deliverables:**
- `src/mlpy/stdlib/regex_bridge.py` (REWRITTEN with decorators)
- `src/mlpy/stdlib/builtins.py` (NEW, ~150 lines)
- `tests/unit/test_regex_module.py` (updated if needed)

**Tasks:**
1. Rewrite `regex_bridge.py` with decorator system
2. Create `builtins.py` with @builtin decorators
3. Remove manual registration from `safe_attribute_registry.py` (lines 233-265)
4. Test regex module works identically to before
5. Run full ML integration test suite

**Example: Rewritten regex_bridge.py**

```python
"""ML regex module - Decorator-based implementation."""

import re as _re  # Underscore prefix avoids collision

from .decorators import stdlib_module, public, public_class, python_import


@public_class("Compiled regex pattern for efficient reuse")
class Pattern:
    """Compiled regex pattern."""

    def __init__(self, pattern: str):
        self.pattern_str = pattern
        try:
            self._compiled = _re.compile(pattern)
        except _re.error as e:
            raise RuntimeError(f"Invalid regex pattern '{pattern}': {e}")

    @public("Test if pattern matches text")
    def test(self, text: str) -> bool:
        return bool(self._compiled.search(text))

    @public("Find first match in text")
    def match(self, text: str) -> str | None:
        match = self._compiled.search(text)
        return match.group(0) if match else None

    @public("Find all matches in text")
    def findAll(self, text: str) -> list[str]:
        return self._compiled.findall(text)

    @public("Replace first occurrence")
    def replace(self, text: str, replacement: str) -> str:
        return self._compiled.sub(replacement, text, count=1)

    @public("Replace all occurrences")
    def replaceAll(self, text: str, replacement: str) -> str:
        return self._compiled.sub(replacement, text)

    @public("Split text by pattern")
    def split(self, text: str) -> list[str]:
        return self._compiled.split(text)

    @public("Count matches in text")
    def count(self, text: str) -> int:
        return len(self._compiled.findall(text))

    @public("Get string representation")
    def toString(self) -> str:
        return f"Pattern({repr(self.pattern_str)})"

    @public("Pattern string", property=True)
    @property
    def pattern(self) -> str:
        return self.pattern_str


@python_import("re")
@stdlib_module(
    "regex",
    description="Regular expression pattern matching and text manipulation",
    version="2.0.0"
)
class Regex:
    """Regex module interface for ML code."""

    @public("Compile pattern for efficient reuse")
    @staticmethod
    def compile(pattern: str) -> Pattern:
        return Pattern(pattern)

    @public("Test if pattern matches text")
    @staticmethod
    def test(pattern: str, text: str) -> bool:
        try:
            return bool(_re.search(pattern, text))
        except _re.error as e:
            raise RuntimeError(f"Invalid regex pattern '{pattern}': {e}")

    @public("Find first match")
    @staticmethod
    def match(pattern: str, text: str) -> str | None:
        try:
            match = _re.search(pattern, text)
            return match.group(0) if match else None
        except _re.error as e:
            raise RuntimeError(f"Invalid regex pattern '{pattern}': {e}")

    @public("Find all matches")
    @staticmethod
    def findAll(pattern: str, text: str) -> list[str]:
        try:
            return _re.findall(pattern, text)
        except _re.error as e:
            raise RuntimeError(f"Invalid regex pattern '{pattern}': {e}")

    @public("Replace first occurrence")
    @staticmethod
    def replace(pattern: str, text: str, replacement: str) -> str:
        try:
            return _re.sub(pattern, replacement, text, count=1)
        except _re.error as e:
            raise RuntimeError(f"Invalid regex pattern '{pattern}': {e}")

    @public("Replace all occurrences")
    @staticmethod
    def replaceAll(pattern: str, text: str, replacement: str) -> str:
        try:
            return _re.sub(pattern, replacement, text)
        except _re.error as e:
            raise RuntimeError(f"Invalid regex pattern '{pattern}': {e}")

    @public("Split text by pattern")
    @staticmethod
    def split(pattern: str, text: str) -> list[str]:
        try:
            return _re.split(pattern, text)
        except _re.error as e:
            raise RuntimeError(f"Invalid regex pattern '{pattern}': {e}")

    @public("Escape special regex characters")
    @staticmethod
    def escape(text: str) -> str:
        return _re.escape(text)

    @public("Check if pattern is valid")
    @staticmethod
    def isValid(pattern: str) -> bool:
        try:
            _re.compile(pattern)
            return True
        except _re.error:
            return False

    @public("Count matches in text")
    @staticmethod
    def count(pattern: str, text: str) -> int:
        try:
            return len(_re.findall(pattern, text))
        except _re.error as e:
            raise RuntimeError(f"Invalid regex pattern '{pattern}': {e}")

    @public("Get pre-compiled email pattern")
    @staticmethod
    def emailPattern() -> Pattern:
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return Pattern(email_regex)

    @public("Extract email addresses from text")
    @staticmethod
    def extractEmails(text: str) -> list[str]:
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return _re.findall(email_regex, text)

    @public("Extract phone numbers from text")
    @staticmethod
    def extractPhoneNumbers(text: str) -> list[str]:
        phone_regex = r'(?:\+?1[-.\\s]?)?\\(?[0-9]{3}\\)?[-.\\s]?[0-9]{3}[-.\\s]?[0-9]{4}'
        return _re.findall(phone_regex, text)

    @public("Check if text is valid URL")
    @staticmethod
    def isUrl(text: str) -> bool:
        url_regex = r'^https?://(?:[-\\w.])+(?:[:\\d]+)?(?:/(?:[\\w/_.])*(?:\\?(?:[\\w&=%.])*)?(?:#(?:\\w*))?)?$'
        return bool(_re.match(url_regex, text))

    @public("Remove HTML tags from text")
    @staticmethod
    def removeHtmlTags(text: str) -> str:
        return _re.sub(r'<[^<]+?>', '', text)


# Create module instance
regex = Regex()

# Export (for backward compatibility)
__all__ = ["Regex", "Pattern", "regex"]
```

**Success Criteria:**
- All 34 regex module unit tests pass
- All ML integration tests still pass
- No performance regression

### Phase 3: Migration Tools (Days 9-10)

**Deliverables:**
- `scripts/migrate_to_decorators.py` (~300 lines)
- `scripts/validate_decorators.py` (~150 lines)

**Tasks:**
1. Build automated migration script
2. Build validation script
3. Test on regex module (already migrated manually)
4. Document migration process

**Success Criteria:**
- Migration script generates 80% correct code
- Validation script catches common errors
- Clear migration documentation

### Phase 4: Testing Infrastructure (Days 11-13)

**Deliverables:**
- `tests/unit/test_stdlib_decorators.py` (~400 lines)
- `tests/unit/test_stdlib_scanner.py` (~200 lines)
- `tests/integration/test_decorated_modules.py` (~300 lines)

**Tasks:**
1. Write comprehensive decorator unit tests
2. Write scanner unit tests
3. Write integration tests comparing old vs new systems
4. Document testing approach

**Success Criteria:**
- 100% coverage of decorator system
- All integration tests pass
- Performance benchmarks documented

### Phase 5: Gradual Migration (Days 14-28)

**Migration Order (Risk-Based):**

| Week | Modules | LOC | Methods | Classes | Risk |
|------|---------|-----|---------|---------|------|
| 1 | regex (done), math, console | 4,485 | 29 | 2 | LOW |
| 2 | random, json | 8,757 | 34 | 2 | LOW |
| 3 | string, datetime | 29,455 | 135 | 4 | MEDIUM |
| 4 | functional, int, float, collections, array | 43,974 | 259 | 7 | HIGH |

**Per-Module Checklist:**
- [ ] Backup: `cp X_bridge.py X_bridge_old.py`
- [ ] Run migration script: `python scripts/migrate_to_decorators.py src/mlpy/stdlib/X_bridge.py`
- [ ] Manually add @public decorators to all methods
- [ ] Add descriptions to all decorators
- [ ] Verify Python imports use underscore prefix
- [ ] Remove manual registration from `safe_attribute_registry.py`
- [ ] Keep `__init__.py` import unchanged
- [ ] Run module unit tests: `pytest tests/unit/test_X_module.py -v`
- [ ] Run integration tests: `python tests/ml_test_runner.py --full`
- [ ] Validate: `python scripts/validate_decorators.py`
- [ ] Git commit: `git commit -m "migrate(stdlib): Convert X to decorators"`

**Success Criteria Per Module:**
- All unit tests pass (100%)
- All integration tests pass (100%)
- No performance regression (>5%)
- Code review approved

---

## Migration Strategy

### Backward Compatibility Strategy

**Dual-System Support:**
- Old system continues to work (hardcoded list in code generator)
- New system checks decorated modules first
- No breaking changes during migration
- Feature flag for disabling old system (post-migration)

**Migration Phases:**

1. **Phase 1: Coexistence (Weeks 1-4)**
   - Both systems active
   - New modules use decorators
   - Old modules unchanged

2. **Phase 2: Gradual Migration (Weeks 2-4)**
   - Migrate one module at a time
   - Full test suite after each module
   - Roll back if any failures

3. **Phase 3: Deprecation (Future)**
   - Mark old system deprecated
   - Add warnings for unmigrated modules
   - Set deadline for migration

4. **Phase 4: Removal (Far Future)**
   - Remove hardcoded module list
   - Remove old registration code
   - Simplify codebase

### Migration Decision Tree

```
Are you creating a NEW module?
├─ YES → Use decorator system (mandatory)
└─ NO → Is existing module being modified?
    ├─ YES → Migrate to decorators (recommended)
    └─ NO → Leave as-is (legacy support)
```

---

## Risk Assessment

### HIGH RISKS ⚠️

#### 1. Test Suite Breakage
**Description:** 42+ ML test files import modules, any breakage fails tests
**Probability:** 60%
**Impact:** HIGH - blocks deployment
**Mitigation:**
- Migrate one module at a time
- Run full test suite after each migration
- Keep backups of original modules
- Use feature branch with easy rollback

#### 2. Runtime Attribute Access Failures
**Description:** Safe attribute registry integration breaks, methods inaccessible
**Probability:** 40%
**Impact:** CRITICAL - breaks all module access
**Mitigation:**
- Comprehensive unit tests for registry integration
- Manual REPL testing before committing
- Staged rollout starting with regex

#### 3. Import Ordering Issues
**Description:** Decorator registration happens after code generator runs
**Probability:** 30%
**Impact:** HIGH - imports fail silently
**Mitigation:**
- Scanner runs early in `__init__.py`
- Explicit initialization in code generator
- Integration tests for import timing

#### 4. Circular Import Dependencies
**Description:** `decorators.py` ↔ `safe_attribute_registry.py` circular import
**Probability:** 50%
**Impact:** MEDIUM - breaks imports
**Mitigation:**
- Careful dependency management
- Lazy imports where possible
- Registry reads decorator metadata (one-way)

#### 5. Performance Regression
**Description:** Module scanning adds startup time
**Probability:** 70%
**Impact:** LOW - likely <100ms
**Mitigation:**
- Lazy loading (scan only when needed)
- Caching (scan once per session)
- Benchmark before/after

### MEDIUM RISKS ⚡

#### 6. Incomplete Migration
**Description:** Some modules stay on old system indefinitely
**Probability:** 80%
**Impact:** MEDIUM - technical debt
**Mitigation:**
- Deprecation warnings for old system
- Set migration deadline
- Automated detection of unmigrated modules

#### 7. Documentation Drift
**Description:** Docs don't match new decorator system
**Probability:** 90%
**Impact:** LOW - confuses contributors
**Mitigation:**
- Update developer guide immediately
- Add migration guide
- Include examples in proposal

### LOW RISKS ✓

#### 8. Decorator API Changes
**Description:** Need to change decorator signatures after release
**Probability:** 30%
**Impact:** LOW - refactor wrapper code only
**Mitigation:**
- Thorough API design review
- Beta period for feedback
- Versioned decorator system

---

## Cost/Benefit Analysis

### Costs (Detailed)

**Development Time:**
- Phase 1 (Infrastructure): 40 hours
- Phase 2 (Reference): 24 hours
- Phase 3 (Tools): 16 hours
- Phase 4 (Testing): 24 hours
- Phase 5 (Migration): 80 hours (12 modules × 6-7 hours each)
- **Total: 184 hours (4.6 weeks @ 40hr/week)**

**Risk Costs:**
- Bug fixes from breakage: 20 hours (estimated)
- Performance tuning: 10 hours
- Documentation updates: 10 hours
- **Total Risk Buffer: 40 hours**

**Grand Total: 224 hours (5.6 weeks)**

**Other Costs:**
- Learning curve: 2 hours per new contributor
- Code complexity: +1,000 LOC infrastructure
- Opportunity cost: Could build features instead

### Benefits (Detailed)

**Time Savings Per Module:**
- Old system: 45 minutes registration
- New system: 8 minutes (decorators only)
- **Savings: 37 minutes per module (82% reduction)**

**Maintenance Savings:**
- Adding method: 5 steps → 1 decorator
- Estimated 20 method additions/year
- **Savings: ~50 hours/year**

**Quality Improvements:**
- 30% reduction in registration bugs (estimated)
- Self-documenting code
- Faster onboarding
- Better introspection

**Long-Term Value:**
- Scales to 100+ modules without complexity increase
- Enables future metaprogramming features
- Cleaner codebase architecture

### Break-Even Analysis

**Initial Investment:** 224 hours
**Annual Savings:** 50 hours
**Break-Even:** 4.5 years

**Sensitivity Analysis:**
- If 40 methods/year: Break-even in 2.2 years
- If 10 methods/year: Break-even in 9 years

### Verdict: Marginally Positive

**Proceed if:**
- ✅ Planning 2+ years active development
- ✅ Expecting >20 modules in stdlib
- ✅ Prioritizing code quality over short-term velocity

**Skip if:**
- ❌ Project is near feature-complete
- ❌ Stdlib is stable (few additions)
- ❌ Short-term delivery pressure

---

## Testing Strategy

### Test Pyramid

```
        ┌─────────────────┐
        │  E2E Tests (12) │  Full ML programs
        └────────┬────────┘
               │
        ┌──────┴──────────┐
        │ Integration (30) │  Module + Registry + Codegen
        └──────┬───────────┘
              │
    ┌─────────┴──────────┐
    │  Unit Tests (200)   │  Decorators, Scanner, Each Module
    └─────────────────────┘
```

### Unit Tests

**`tests/unit/test_stdlib_decorators.py`** (~400 lines)
- Test @stdlib_module registration
- Test @public method marking
- Test @public_class registration
- Test @builtin registration
- Test metadata storage
- Test decorator combinations

**`tests/unit/test_stdlib_scanner.py`** (~200 lines)
- Test module discovery
- Test lazy loading
- Test caching
- Test error handling

**Per-Module Tests** (existing + updates)
- Test all public methods accessible
- Test error handling
- Test capability integration

### Integration Tests

**`tests/integration/test_decorated_modules.py`** (~300 lines)
- Test decorator system integrates with registry
- Test code generator finds decorated modules
- Test runtime attribute access works
- Test backward compatibility (old + new)

### End-to-End Tests

**Use existing ML integration tests:**
- Run `python tests/ml_test_runner.py --full`
- Verify all 42+ test files still pass
- No regressions in test results

### Performance Tests

**Benchmark startup time:**
```python
import time

# Before decorator system
start = time.time()
from mlpy.stdlib import regex
end = time.time()
print(f"Old system: {(end-start)*1000:.2f}ms")

# After decorator system
start = time.time()
from mlpy.stdlib import regex  # Uses decorators
end = time.time()
print(f"New system: {(end-start)*1000:.2f}ms")

# Acceptable: <100ms regression
```

### Regression Testing

**Test Matrix:**
| Test Category | Old System | New System | Gate |
|---------------|------------|------------|------|
| Unit tests | 100% pass | 100% pass | HARD |
| Integration tests | 100% pass | 100% pass | HARD |
| ML tests (42 files) | 100% pass | 100% pass | HARD |
| Performance | Baseline | <100ms slower | SOFT |
| Coverage | ≥95% | ≥95% | HARD |

---

## Security Measures

### Git Branch Strategy

```bash
# Create feature branch
git checkout -b feature/stdlib-decorators

# Tag current state for rollback
git tag pre-decorator-migration

# Work on feature branch
git commit -m "feat(stdlib): Add decorator infrastructure"
git commit -m "migrate(stdlib): Convert regex to decorators"

# After each module migration, run full tests
pytest tests/ --tb=short
python tests/ml_test_runner.py --full

# If tests fail, revert last commit
git revert HEAD

# When all migrations complete
git checkout master
git merge feature/stdlib-decorators
```

### Backup Strategy

**Before migration:**
```bash
# Backup entire stdlib directory
cp -r src/mlpy/stdlib src/mlpy/stdlib_backup

# Backup individual module
cp src/mlpy/stdlib/regex_bridge.py src/mlpy/stdlib/regex_bridge_old.py
```

**Emergency rollback:**
```bash
# Revert to pre-migration state
git checkout pre-decorator-migration

# Or restore from backup
cp src/mlpy/stdlib_backup/* src/mlpy/stdlib/
```

### Testing Gates

**Gate 1: Unit Tests**
```bash
pytest tests/unit/test_stdlib_decorators.py -v
pytest tests/unit/test_stdlib_scanner.py -v
# Must pass 100%
```

**Gate 2: Module-Specific Tests**
```bash
pytest tests/unit/test_regex_module.py -v
# Must pass 100%
```

**Gate 3: Integration Tests**
```bash
pytest tests/integration/ -v
# Must pass 100%
```

**Gate 4: ML Integration Tests**
```bash
python tests/ml_test_runner.py --full
# Must pass 100% (same as before migration)
```

**Gate 5: Performance**
```bash
python scripts/benchmark_startup.py
# Must be <100ms slower than baseline
```

### Code Review Process

**Review Checklist:**
- [ ] All @public decorators present
- [ ] All methods have descriptions
- [ ] Python imports use underscore prefix
- [ ] No manual registration remains
- [ ] All tests pass
- [ ] No performance regression
- [ ] Documentation updated

**Review Assignments:**
- Infrastructure (decorators, scanner): Senior developer
- Each migrated module: Peer review
- Integration: Security review

---

## Implementation Recommendation

### Final Verdict: **CONDITIONAL YES**

**Proceed if ALL conditions met:**
1. ✅ Team has 3-4 weeks dedicated bandwidth
2. ✅ Project has 2+ years active maintenance planned
3. ✅ Willing to accept 60% risk of temporary test breakage
4. ✅ Can assign senior developer for oversight
5. ✅ Stable feature branch workflow available

**Do NOT proceed if ANY condition true:**
1. ❌ Project near feature-freeze or release
2. ❌ Team understaffed or under pressure
3. ❌ Can't afford 3-4 week project delay
4. ❌ Risk tolerance is low
5. ❌ Stdlib is feature-complete (no new modules planned)

### Alternative Approach: Opportunistic Migration

If full migration is too risky, consider **hybrid approach:**

1. **Immediate:** Implement decorator system (Phases 1-4)
2. **Require:** All NEW modules use decorators (mandatory)
3. **Opportunistic:** Migrate old modules only when touched for other reasons
4. **Long-term:** Eventually remove old system (2+ years)

**Benefits:**
- Spreads cost over time
- Reduces risk concentration
- Provides immediate value for new modules
- No forced migration deadline

---

## Files Touched (Complete List)

### NEW FILES (8 files, ~2,100 lines)

1. `src/mlpy/stdlib/decorators.py` (~400 lines)
2. `src/mlpy/stdlib/scanner.py` (~200 lines)
3. `src/mlpy/stdlib/builtins.py` (~150 lines)
4. `scripts/migrate_to_decorators.py` (~300 lines)
5. `scripts/validate_decorators.py` (~150 lines)
6. `tests/unit/test_stdlib_decorators.py` (~400 lines)
7. `tests/unit/test_stdlib_scanner.py` (~200 lines)
8. `tests/integration/test_decorated_modules.py` (~300 lines)

### MODIFIED FILES (16 files, ~3,400 lines)

**Core Infrastructure:**
1. `src/mlpy/stdlib/__init__.py` (+3 lines)
2. `src/mlpy/ml/codegen/safe_attribute_registry.py` (+50 lines, -33 lines)
3. `src/mlpy/ml/codegen/python_generator.py` (+20 lines)

**Bridge Modules (12 files, REWRITE with decorators):**
4. `src/mlpy/stdlib/regex_bridge.py` (+20 decorators)
5. `src/mlpy/stdlib/math_bridge.py` (+25 decorators)
6. `src/mlpy/stdlib/console_bridge.py` (+8 decorators)
7. `src/mlpy/stdlib/random_bridge.py` (+18 decorators)
8. `src/mlpy/stdlib/json_bridge.py` (+15 decorators)
9. `src/mlpy/stdlib/string_bridge.py` (+90 decorators)
10. `src/mlpy/stdlib/datetime_bridge.py` (+45 decorators)
11. `src/mlpy/stdlib/functional_bridge.py` (+35 decorators)
12. `src/mlpy/stdlib/int_bridge.py` (+30 decorators)
13. `src/mlpy/stdlib/float_bridge.py` (+55 decorators)
14. `src/mlpy/stdlib/collections_bridge.py` (+20 decorators)
15. `src/mlpy/stdlib/array_bridge.py` (+28 decorators)

**Documentation:**
16. `docs/developer/writing-stdlib-modules.md` (UPDATE with decorator examples)

### DELETED CODE (~400 lines)

**From `safe_attribute_registry.py`:**
- Lines 233-265: Hardcoded regex registration (removed)
- Similar blocks for other modules as they migrate

**Net Code Change:** +2,100 new + 3,400 modified - 400 deleted = **+5,100 lines**

---

## Timeline Summary

| Week | Focus | Deliverables | Risk |
|------|-------|--------------|------|
| 1 | Infrastructure | Decorators, Scanner, Integration | MEDIUM |
| 2 | Reference + Tools | regex migration, Migration tools | HIGH |
| 3 | Testing | Full test suite, Performance benchmarks | LOW |
| 4 | Migration (Simple) | math, console, random, json | MEDIUM |
| 5 | Migration (Complex) | string, datetime, functional | HIGH |
| 6 | Migration (Finish) | int, float, collections, array | MEDIUM |

**Total: 4-6 weeks depending on issue resolution**

---

## Success Criteria

### Must-Have (Hard Requirements)
- [ ] All 12 modules migrated to decorator system
- [ ] 100% test passage (no regressions)
- [ ] Zero breaking changes to ML code
- [ ] Performance <100ms regression
- [ ] Complete documentation

### Nice-to-Have (Soft Goals)
- [ ] Migration tools work 90%+ automatically
- [ ] Code review process smooth
- [ ] Contributors find system intuitive
- [ ] Performance actually improves

---

## Conclusion

This proposal presents a well-designed but expensive refactoring that will significantly improve the developer experience for standard library modules. The decorator-based system is elegant and aligns with Python best practices, but the migration cost is substantial.

**Key Decision Factors:**
1. **Long-term value:** Excellent (50 hours/year savings)
2. **Short-term cost:** High (224 hours)
3. **Risk level:** High (60% chance of temporary breakage)
4. **Break-even:** 4.5 years

**Recommendation:** Implement if you're committed to long-term project maintenance. Consider opportunistic migration if risk tolerance is moderate.

---

## Appendix A: Decorator Usage Examples

### Example 1: Simple Module (Math)

```python
"""ML math module - Decorator-based implementation."""

import math as _math

from .decorators import stdlib_module, public, python_import


@python_import("math")
@stdlib_module("math", description="Mathematical operations")
class Math:
    """ML math operations."""

    # Constants
    pi = _math.pi
    e = _math.e

    @public("Square root function")
    @staticmethod
    def sqrt(x: float) -> float:
        return _math.sqrt(max(0, x))  # Safe for ML

    @public("Absolute value")
    @staticmethod
    def abs(x: float) -> float:
        return abs(x)

    @public("Sine function")
    @staticmethod
    def sin(x: float) -> float:
        return _math.sin(x)


math = Math()
__all__ = ["Math", "math"]
```

### Example 2: Complex Module with Classes (Regex)

See Phase 2 section for complete regex example.

### Example 3: Builtin Functions

```python
"""ML builtin functions."""

from .decorators import builtin


@builtin("Get type of value as string")
def typeof(value):
    """Return type as string."""
    if isinstance(value, bool):
        return "boolean"
    elif isinstance(value, (int, float)):
        return "number"
    elif isinstance(value, str):
        return "string"
    elif isinstance(value, list):
        return "array"
    elif isinstance(value, dict):
        return "object"
    elif callable(value):
        return "function"
    return "unknown"


@builtin("Convert value to integer")
def int(value):
    """Convert to int."""
    try:
        return int(value) if value is not True and value is not False else (1 if value else 0)
    except:
        return 0
```

---

## Appendix B: Migration Script Example

See Phase 3 for complete migration script code.

---

## Appendix C: Testing Checklist

**Pre-Migration:**
- [ ] Tag current state: `git tag pre-decorator-migration`
- [ ] Run baseline tests: All pass
- [ ] Measure baseline performance

**Per-Module Migration:**
- [ ] Backup original: `cp X_bridge.py X_bridge_old.py`
- [ ] Run migration script
- [ ] Add @public decorators manually
- [ ] Add descriptions
- [ ] Remove old registration
- [ ] Run unit tests: 100% pass
- [ ] Run integration tests: 100% pass
- [ ] Run ML tests: 100% pass
- [ ] Validate: `python scripts/validate_decorators.py`
- [ ] Code review
- [ ] Commit: `git commit -m "migrate(stdlib): X module"`

**Post-Migration:**
- [ ] All modules migrated
- [ ] All tests pass
- [ ] Performance acceptable
- [ ] Documentation updated
- [ ] Deprecate old system

---

**End of Proposal**