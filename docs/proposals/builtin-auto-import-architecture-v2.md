# Builtin Auto-Import Architecture v2: Decorator-Driven Approach

## Executive Summary

**Revision**: This proposal replaces the manual registry approach with a **metadata-driven architecture** that leverages the existing `@ml_function` decorator system.

**Key Insight**: We already have all the metadata we need through decorators. The transpiler should **introspect** the builtin module at initialization, not maintain a separate registry.

**CRITICAL SECURITY & SEMANTIC ISSUE**: The transpiler generates Python code that directly calls Python's built-in functions instead of ML's stdlib builtin module, creating security vulnerabilities and semantic mismatches.

**Solution**: Decorator-driven auto-import with compile-time function call routing.

---

## Part 1: Leveraging Existing Infrastructure

### What We Already Have

#### Decorator System (`src/mlpy/stdlib/decorators.py`)

```python
# Global registry of ALL ML modules
_MODULE_REGISTRY = {}

@ml_module(name="builtin", description="...", capabilities=[], version="1.0.0")
class Builtin:
    @ml_function(description="Convert value to integer", capabilities=[])
    def int(self, value: Any) -> int:
        # Implementation...

    @ml_function(description="Get type of value", capabilities=[])
    def typeof(self, value: Any) -> str:
        # Implementation...

    # ... 36 more decorated functions
```

#### Metadata Access

```python
def get_module_metadata(module_name: str) -> Optional[ModuleMetadata]:
    """Get metadata for a registered module."""
    module_cls = _MODULE_REGISTRY.get(module_name)
    if module_cls and hasattr(module_cls, "_ml_module_metadata"):
        return module_cls._ml_module_metadata
    return None

class ModuleMetadata:
    def __init__(self, name, description, capabilities, version):
        self.name = name
        self.description = description
        self.capabilities = capabilities
        self.version = version
        self.functions = {}  # Dict[str, FunctionMetadata]
        self.classes = {}
```

#### Builtin Module Instance (`src/mlpy/stdlib/builtin.py`)

```python
@ml_module(
    name="builtin",
    description="Core builtin functions always available without import",
    capabilities=[],
    version="1.0.0"
)
class Builtin:
    # All 38 functions decorated with @ml_function
    pass

# Singleton instance
builtin = Builtin()
```

### Why This Is Better Than a Manual Registry

| Approach | Single Source of Truth | Auto-Updates | Extensible | Metadata-Rich |
|----------|------------------------|--------------|------------|---------------|
| **Manual Registry** ❌ | No (duplicates decorators) | No (manual maintenance) | Limited | No |
| **Decorator-Driven** ✅ | Yes (`@ml_function`) | Yes (automatic) | Yes (any module) | Yes (full metadata) |

---

## Part 2: Improved Architecture

### Component 1: Builtin Function Cache (NOT Registry)

**Create**: `src/mlpy/ml/codegen/builtin_introspection.py`

```python
"""Builtin function introspection for code generation.

This module provides utilities to discover ML builtin functions by introspecting
the decorator metadata, rather than maintaining a separate registry.
"""

from typing import Set, Optional, Dict, Any
from mlpy.stdlib.decorators import get_module_metadata, _MODULE_REGISTRY


class BuiltinFunctionCache:
    """Cache of builtin function names derived from decorator metadata.

    This is a CACHE, not a registry - the single source of truth is the
    @ml_function decorators in src/mlpy/stdlib/builtin.py.
    """

    def __init__(self):
        """Initialize the cache by introspecting decorator metadata."""
        self._function_names: Set[str] = set()
        self._metadata: Optional[Any] = None
        self._initialized = False

    def _ensure_initialized(self) -> None:
        """Lazy initialization - introspect builtin module metadata."""
        if self._initialized:
            return

        # Ensure builtin module is imported and registered
        try:
            from mlpy.stdlib import builtin
        except ImportError:
            # Builtin module not available (testing scenario?)
            self._initialized = True
            return

        # Get metadata from decorator system
        self._metadata = get_module_metadata("builtin")

        if self._metadata is None:
            # Module not properly decorated or registered
            raise RuntimeError(
                "Builtin module not found in registry. "
                "Ensure @ml_module decorator is applied."
            )

        # Extract all function names from metadata
        self._function_names = set(self._metadata.functions.keys())
        self._initialized = True

    def is_builtin_function(self, func_name: str) -> bool:
        """Check if a function name is an ML builtin function.

        Args:
            func_name: Name of the function to check

        Returns:
            True if the function is a decorated ML builtin function

        Example:
            >>> cache = BuiltinFunctionCache()
            >>> cache.is_builtin_function("int")
            True
            >>> cache.is_builtin_function("typeof")
            True
            >>> cache.is_builtin_function("my_custom_func")
            False
        """
        self._ensure_initialized()
        return func_name in self._function_names

    def get_all_builtin_functions(self) -> Set[str]:
        """Get complete set of builtin function names.

        Returns:
            Set of all ML builtin function names
        """
        self._ensure_initialized()
        return self._function_names.copy()

    def get_function_metadata(self, func_name: str) -> Optional[Any]:
        """Get metadata for a specific builtin function.

        Args:
            func_name: Name of the function

        Returns:
            FunctionMetadata object or None if not found
        """
        self._ensure_initialized()
        if self._metadata:
            return self._metadata.functions.get(func_name)
        return None

    def get_required_capabilities(self, func_name: str) -> list[str]:
        """Get required capabilities for a builtin function.

        Args:
            func_name: Name of the function

        Returns:
            List of required capability strings
        """
        func_meta = self.get_function_metadata(func_name)
        if func_meta:
            return func_meta.capabilities
        return []


# Singleton instance for global use
_builtin_cache = BuiltinFunctionCache()


def is_builtin_function(func_name: str) -> bool:
    """Check if a function name is an ML builtin function.

    This is a convenience wrapper around the singleton cache.
    """
    return _builtin_cache.is_builtin_function(func_name)


def get_all_builtin_functions() -> Set[str]:
    """Get complete set of builtin function names."""
    return _builtin_cache.get_all_builtin_functions()


def get_builtin_metadata(func_name: str) -> Optional[Any]:
    """Get metadata for a builtin function."""
    return _builtin_cache.get_function_metadata(func_name)


__all__ = [
    "BuiltinFunctionCache",
    "is_builtin_function",
    "get_all_builtin_functions",
    "get_builtin_metadata",
]
```

### Why This Is Better

**Before (Manual Registry)**:
```python
# PROBLEM: Duplicates information already in decorators
ML_BUILTIN_FUNCTIONS = {
    'int', 'float', 'str', 'bool',  # ❌ Manually maintained
    'typeof', 'isinstance',          # ❌ Can get out of sync
    # ... must remember to update this list
}
```

**After (Decorator-Driven)**:
```python
# SOLUTION: Single source of truth is the decorator
@ml_function(description="Convert value to integer", capabilities=[])
def int(self, value: Any) -> int:  # ✅ Automatically discovered
    pass

# Cache is derived, not manually maintained
cache = BuiltinFunctionCache()  # ✅ Introspects decorators
cache.is_builtin_function("int")  # ✅ Always in sync
```

### Benefits of This Approach

1. **Single Source of Truth**: `@ml_function` decorators define what's a builtin
2. **Zero Duplication**: No manual list to maintain
3. **Automatic Extension**: Add `@ml_function` → automatically recognized
4. **Metadata-Rich**: Access to capabilities, descriptions, params, returns
5. **Testable**: Can verify cache matches decorators
6. **Extensible**: Same pattern works for ANY module, not just builtin

---

## Part 3: Enhanced Code Generator (Same as Before)

### Modify: `src/mlpy/ml/codegen/python_generator.py`

#### Add Import and Cache

```python
from mlpy.ml.codegen.builtin_introspection import is_builtin_function
```

#### Add Tracking Field

```python
@dataclass
class CodeGenContext:
    """Context for code generation."""
    # ... existing fields ...

    # Track which builtin functions are actually used
    builtin_functions_used: set[str] = field(default_factory=set)
    builtin_import_added: bool = False
```

#### Enhance Function Call Generation

```python
elif isinstance(expr, FunctionCall):
    # Extract function name
    if isinstance(expr.function, str):
        func_name = expr.function
    elif isinstance(expr.function, Identifier):
        func_name = expr.function.name
    elif isinstance(expr.function, MemberAccess):
        # Method call - don't transform
        func_name = None
        member_call_code = self._generate_expression(expr.function)
        args = [self._generate_expression(arg) for arg in expr.arguments]
        return f"{member_call_code}({', '.join(args)})"
    else:
        func_name = None

    # Check if this is an ML builtin function (uses decorator metadata!)
    if func_name and self._should_route_to_builtin(func_name):
        # Track usage for import generation
        self.context.builtin_functions_used.add(func_name)
        # Route to builtin module
        args = [self._generate_expression(arg) for arg in expr.arguments]
        return f"builtin.{func_name}({', '.join(args)})"
    else:
        # User-defined function or other callable
        if func_name:
            func_code = self._safe_identifier(func_name)
        else:
            func_code = self._generate_expression(expr.function)
        args = [self._generate_expression(arg) for arg in expr.arguments]
        return f"{func_code}({', '.join(args)})"
```

#### Add Scope-Aware Routing

```python
def _should_route_to_builtin(self, func_name: str) -> bool:
    """Determine if function call should route to builtin module.

    Uses decorator metadata to check if function is a builtin, and
    scope analysis to avoid transforming user-defined functions.

    Args:
        func_name: Name of the function being called

    Returns:
        True if should route to builtin module, False otherwise
    """
    # Check decorator metadata (via cache)
    if not is_builtin_function(func_name):
        return False

    # Check if user defined a function with the same name
    if self._is_user_defined_function(func_name):
        return False

    # Route to builtin module
    return True

def _is_user_defined_function(self, func_name: str) -> bool:
    """Check if a function is user-defined in current scope.

    Args:
        func_name: Name of the function

    Returns:
        True if function is defined in the current module
    """
    # Check if it's defined in the current module
    return func_name in self.context.defined_functions
```

#### Auto-Import Method

```python
def _ensure_builtin_imported(self) -> None:
    """Ensure builtin module is imported if any builtin functions are used."""
    if self.context.builtin_functions_used and not self.context.builtin_import_added:
        self.context.builtin_import_added = True
        self.context.imports_needed.add("from mlpy.stdlib.builtin import builtin")
```

#### Update Import Emission

```python
def _emit_imports(self):
    """Emit necessary Python imports."""
    # Ensure builtin import is added if needed
    self._ensure_builtin_imported()

    for import_name in sorted(self.context.imports_needed):
        # ... existing import logic ...
```

---

## Part 4: Extensibility - Works for ALL Modules

### Key Advantage: Unified Pattern

This approach isn't just for `builtin` - it works for **any decorated module**!

```python
def is_stdlib_function(module_name: str, func_name: str) -> bool:
    """Check if a function belongs to any ML stdlib module.

    Args:
        module_name: Name of the module (e.g., "string", "math")
        func_name: Name of the function

    Returns:
        True if function is decorated with @ml_function in that module
    """
    metadata = get_module_metadata(module_name)
    if metadata:
        return func_name in metadata.functions
    return False

def get_all_stdlib_modules() -> dict[str, set[str]]:
    """Get all ML stdlib modules and their functions.

    Returns:
        Dict mapping module names to sets of function names
    """
    from mlpy.stdlib.decorators import _MODULE_REGISTRY

    result = {}
    for module_name, module_cls in _MODULE_REGISTRY.items():
        if hasattr(module_cls, "_ml_module_metadata"):
            metadata = module_cls._ml_module_metadata
            result[module_name] = set(metadata.functions.keys())

    return result
```

### Example: String Module Auto-Import

**Future enhancement** (same pattern):

```python
# ML code
import string;
upper_text = string.upper("hello");  # Method call, not transformed
standalone_call = upper("hello");    # Could auto-import if desired
```

```python
# Generated code (if we enable auto-import for string module)
from mlpy.stdlib.string_bridge import string_module

upper_text = string_module.upper("hello")
```

---

## Part 5: Implementation Plan (Revised)

### Phase 1: Decorator-Driven Cache (2-3 hours)

**Priority: CRITICAL**

1. ✅ Create `builtin_introspection.py` with `BuiltinFunctionCache`
2. ✅ Implement lazy initialization with decorator introspection
3. ✅ Add `is_builtin_function()` convenience wrapper
4. ✅ Add unit tests verifying cache matches decorators
5. ✅ Verify all 38 builtin functions are discovered

**Success Criteria**:
- Cache contains exactly the functions with `@ml_function` decorators
- Adding/removing `@ml_function` automatically updates cache
- Unit tests pass

### Phase 2: Code Generator Integration (1-2 hours)

**Priority: CRITICAL**

1. ✅ Import `is_builtin_function` in python_generator.py
2. ✅ Add tracking fields to `CodeGenContext`
3. ✅ Enhance FunctionCall generation with `_should_route_to_builtin()`
4. ✅ Implement `_is_user_defined_function()` for scope awareness
5. ✅ Add `_ensure_builtin_imported()` method
6. ✅ Update `_emit_imports()` to call it

**Success Criteria**:
- All 16 ml_builtin integration tests pass (currently 5/16)
- Generated code includes `from mlpy.stdlib.builtin import builtin`
- Builtin calls transformed to `builtin.function()`

### Phase 3: Scope Analysis (1-2 hours)

**Priority: HIGH**

1. ✅ Track user-defined functions during AST traversal
2. ✅ Implement function shadowing detection
3. ✅ Test user-defined `int()` function not transformed
4. ✅ Test nested scope handling

**Success Criteria**:
- User functions with builtin names not transformed
- Scoping rules correctly enforced
- No false positive transformations

### Phase 4: Security & Testing (2-3 hours)

**Priority: HIGH**

1. ✅ Implement sandbox builtin restrictions
2. ✅ Add security bypass tests
3. ✅ Verify capability system integration
4. ✅ Comprehensive unit tests for cache
5. ✅ Integration tests for all scenarios

**Success Criteria**:
- Cannot access `eval`, `exec`, `__import__` from ML
- All security tests pass
- Cache-decorator consistency tests pass

### Phase 5: Documentation (1 hour)

**Priority: MEDIUM**

1. ✅ Document decorator-driven architecture
2. ✅ Explain cache vs registry distinction
3. ✅ Add examples of adding new builtin functions
4. ✅ Update developer guide

**Total Effort**: 7-11 hours

---

## Part 6: Testing the Decorator-Driven Approach

### Unit Tests for Cache

**Create**: `tests/unit/codegen/test_builtin_introspection.py`

```python
"""Tests for decorator-driven builtin function discovery."""

import pytest
from mlpy.ml.codegen.builtin_introspection import (
    BuiltinFunctionCache,
    is_builtin_function,
    get_all_builtin_functions,
)
from mlpy.stdlib.decorators import get_module_metadata


class TestBuiltinFunctionCache:
    """Test builtin function cache introspection."""

    def test_cache_matches_decorator_metadata(self):
        """Verify cache contains exactly the decorated functions."""
        # Get metadata directly from decorators
        metadata = get_module_metadata("builtin")
        assert metadata is not None, "Builtin module should be registered"

        decorated_functions = set(metadata.functions.keys())

        # Get cached functions
        cached_functions = get_all_builtin_functions()

        # Should be identical
        assert cached_functions == decorated_functions

    def test_all_expected_builtins_present(self):
        """Verify expected builtin functions are discovered."""
        expected = {
            'int', 'float', 'str', 'bool',       # Type conversion
            'typeof', 'isinstance',               # Type checking
            'len', 'range', 'enumerate',          # Collections
            'print', 'input',                     # I/O
            'abs', 'min', 'max', 'round', 'sum',  # Math
            'sorted', 'reversed', 'zip',          # Arrays
            'keys', 'values',                     # Objects
            'all', 'any', 'callable',             # Predicates
            'chr', 'ord',                         # Characters
            'hex', 'bin', 'oct',                  # Base conversion
            'repr', 'format',                     # String repr
            'hasattr', 'getattr', 'call',         # Introspection
        }

        cache = BuiltinFunctionCache()
        actual = cache.get_all_builtin_functions()

        # All expected functions should be present
        assert expected.issubset(actual)

    def test_is_builtin_function_positive(self):
        """Test that known builtins are identified."""
        assert is_builtin_function("int") is True
        assert is_builtin_function("typeof") is True
        assert is_builtin_function("enumerate") is True

    def test_is_builtin_function_negative(self):
        """Test that non-builtins are rejected."""
        assert is_builtin_function("my_custom_func") is False
        assert is_builtin_function("undefined") is False
        assert is_builtin_function("") is False

    def test_cache_lazy_initialization(self):
        """Test that cache initializes lazily."""
        cache = BuiltinFunctionCache()
        assert cache._initialized is False

        # First call triggers initialization
        cache.is_builtin_function("int")
        assert cache._initialized is True

    def test_get_function_metadata(self):
        """Test retrieving metadata for specific function."""
        cache = BuiltinFunctionCache()
        meta = cache.get_function_metadata("int")

        assert meta is not None
        assert meta.name == "int"
        assert "integer" in meta.description.lower()
        assert isinstance(meta.capabilities, list)

    def test_get_required_capabilities(self):
        """Test getting capabilities for builtin functions."""
        cache = BuiltinFunctionCache()

        # Builtin functions have empty capabilities
        caps = cache.get_required_capabilities("int")
        assert caps == []
```

### Integration Test Updates

**No changes needed** - existing tests in `tests/ml_integration/ml_builtin/` will validate!

Expected results:
- **Before**: 5/16 passing (31.2%)
- **After**: 16/16 passing (100%)

---

## Part 7: Adding New Builtin Functions

### The Old Way (Manual Registry) ❌

```python
# Step 1: Add function to builtin.py
@ml_function(description="New function")
def my_new_func(self, x):
    return x * 2

# Step 2: Remember to update registry ❌
ML_BUILTIN_FUNCTIONS = {
    'int', 'float', ...,
    'my_new_func',  # ❌ Easy to forget!
}

# Step 3: Hope you didn't forget
```

### The New Way (Decorator-Driven) ✅

```python
# Step 1: Add function to builtin.py
@ml_function(description="New function", capabilities=[])
def my_new_func(self, x: Any) -> Any:
    """New ML builtin function."""
    return x * 2

# That's it! Automatically discovered ✅
```

**Verification**:
```python
# Unit test automatically verifies it's in cache
def test_cache_matches_decorators():
    metadata = get_module_metadata("builtin")
    cache = get_all_builtin_functions()
    assert set(metadata.functions.keys()) == cache  # ✅ Passes!
```

---

## Part 8: Comparison with Manual Registry Approach

### Code Comparison

#### Manual Registry (v1)
```python
# builtin_registry.py - SEPARATE FILE
ML_BUILTIN_FUNCTIONS = {  # ❌ Duplicates decorator info
    'int', 'float', 'str', 'bool',
    'typeof', 'isinstance',
    # ... must manually maintain 38 entries
}

def is_ml_builtin(func_name: str) -> bool:
    return func_name in ML_BUILTIN_FUNCTIONS  # ❌ Can get out of sync
```

**Problems**:
- ❌ Duplicates information from decorators
- ❌ Can get out of sync
- ❌ Manual maintenance required
- ❌ No metadata access
- ❌ Doesn't scale to other modules

#### Decorator-Driven (v2)
```python
# builtin_introspection.py - INTROSPECTION
class BuiltinFunctionCache:
    def _ensure_initialized(self):
        metadata = get_module_metadata("builtin")  # ✅ Single source of truth
        self._function_names = set(metadata.functions.keys())  # ✅ Derived

def is_builtin_function(func_name: str) -> bool:
    return _cache.is_builtin_function(func_name)  # ✅ Always in sync
```

**Advantages**:
- ✅ Single source of truth (decorators)
- ✅ Always in sync
- ✅ Zero manual maintenance
- ✅ Full metadata access
- ✅ Scales to all modules

---

## Part 9: Conclusion

### Why Decorator-Driven Is Superior

| Aspect | Manual Registry | Decorator-Driven |
|--------|----------------|------------------|
| **Source of Truth** | Duplicated | Single (`@ml_function`) |
| **Maintenance** | Manual | Automatic |
| **Extensibility** | Limited to builtin | Works for all modules |
| **Metadata** | None | Full access |
| **Sync Risk** | High | Zero |
| **DRY Principle** | Violated | Followed |
| **Testing** | Hard to verify | Easy to verify |

### Implementation Summary

1. **Create**: `builtin_introspection.py` with cache (NOT registry)
2. **Introspect**: Use `get_module_metadata("builtin")` at init
3. **Cache**: Build function name set from `metadata.functions.keys()`
4. **Route**: Check cache in code generator
5. **Auto-Import**: Add import when builtins used

### Expected Outcomes (Same)

- **Integration Tests**: 31.2% → 100%
- **Security**: Zero Python builtin bypass
- **Semantics**: 100% ML correctness
- **Maintainability**: Zero-maintenance (automatic sync)
- **Extensibility**: Pattern works for any module

---

**Proposal Status**: READY FOR IMPLEMENTATION (Revised)
**Priority**: CRITICAL
**Estimated Effort**: 7-11 hours
**Key Improvement**: Uses existing decorator metadata instead of manual registry
