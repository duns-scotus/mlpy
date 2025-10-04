# Builtin Auto-Import: Decorator-Driven Architecture (REVISED)

**Date**: January 2025
**Status**: Proposal Revised - Ready for Implementation
**Priority**: CRITICAL
**Key Improvement**: Uses existing decorator metadata instead of manual registry

---

## The Critical Insight

**You were absolutely right** - we shouldn't create a separate registry that duplicates information already present in the decorators!

### What We Already Have

```python
# src/mlpy/stdlib/builtin.py
@ml_module(name="builtin", description="...", version="1.0.0")
class Builtin:
    @ml_function(description="Convert value to integer", capabilities=[])
    def int(self, value: Any) -> int:
        pass

    @ml_function(description="Get type of value", capabilities=[])
    def typeof(self, value: Any) -> str:
        pass

    # ... 36 more decorated functions

builtin = Builtin()  # Singleton instance
```

### Decorator Infrastructure

```python
# src/mlpy/stdlib/decorators.py
_MODULE_REGISTRY = {}  # Global registry populated by decorators

def get_module_metadata(module_name: str) -> Optional[ModuleMetadata]:
    """Get metadata for a registered module."""
    module_cls = _MODULE_REGISTRY.get(module_name)
    return module_cls._ml_module_metadata if module_cls else None

class ModuleMetadata:
    def __init__(self, ...):
        self.functions = {}  # Dict[str, FunctionMetadata] - All @ml_function methods
```

---

## Improved Architecture: Cache, Not Registry

### Before (Manual Registry) ❌

```python
# builtin_registry.py - PROBLEM: Duplicates decorator metadata
ML_BUILTIN_FUNCTIONS = {
    'int', 'float', 'str', 'bool',      # ❌ Manually maintained
    'typeof', 'isinstance',              # ❌ Can get out of sync
    # ... 38 functions to maintain
}

def is_ml_builtin(func_name: str) -> bool:
    return func_name in ML_BUILTIN_FUNCTIONS  # ❌ Separate source of truth
```

**Problems**:
- Duplicates information already in `@ml_function` decorators
- Requires manual maintenance
- Can get out of sync with actual implementation
- No access to metadata (capabilities, descriptions, etc.)

### After (Decorator-Driven) ✅

```python
# builtin_introspection.py - SOLUTION: Introspects decorators
from mlpy.stdlib.decorators import get_module_metadata

class BuiltinFunctionCache:
    """Cache derived from decorator metadata - NOT a manual registry."""

    def _ensure_initialized(self):
        # Import triggers decorator registration
        from mlpy.stdlib import builtin

        # Get metadata from decorator system
        metadata = get_module_metadata("builtin")

        # Extract function names (DERIVED, not duplicated)
        self._function_names = set(metadata.functions.keys())

def is_builtin_function(func_name: str) -> bool:
    """Check via decorator metadata."""
    return _cache.is_builtin_function(func_name)  # ✅ Always in sync
```

**Advantages**:
- ✅ **Single Source of Truth**: `@ml_function` decorators
- ✅ **Zero Duplication**: Cache is derived
- ✅ **Automatic Updates**: Add `@ml_function` → automatically recognized
- ✅ **Metadata Access**: Full access to capabilities, params, returns
- ✅ **Extensible**: Same pattern works for ANY decorated module

---

## How It Works

### Step 1: Decorator Defines What's a Builtin

```python
# src/mlpy/stdlib/builtin.py
@ml_function(description="Convert value to integer", capabilities=[])
def int(self, value: Any) -> int:
    """This decorator IS the source of truth"""
    pass
```

### Step 2: Transpiler Introspects Decorators

```python
# At transpiler initialization
metadata = get_module_metadata("builtin")
# metadata.functions = {
#     'int': FunctionMetadata(name='int', description='...'),
#     'float': FunctionMetadata(name='float', description='...'),
#     'typeof': FunctionMetadata(name='typeof', description='...'),
#     # ... all 38 decorated functions
# }

builtin_functions = set(metadata.functions.keys())  # Cache for O(1) lookup
```

### Step 3: Code Generator Uses Cache

```python
# src/mlpy/ml/codegen/python_generator.py
from mlpy.ml.codegen.builtin_introspection import is_builtin_function

elif isinstance(expr, FunctionCall):
    func_name = expr.function.name

    # Check decorator metadata (via cache)
    if is_builtin_function(func_name):
        # Route to builtin module
        return f"builtin.{func_name}({args})"
    else:
        # User-defined function
        return f"{func_name}({args})"
```

---

## Adding New Builtin Functions

### Old Way (Manual Registry) ❌

```python
# Step 1: Add decorated function
@ml_function(description="New function")
def my_new_func(self, x):
    return x * 2

# Step 2: Update registry ❌ EASY TO FORGET!
ML_BUILTIN_FUNCTIONS.add('my_new_func')

# Step 3: Update tests
# Step 4: Hope you didn't miss anything
```

### New Way (Decorator-Driven) ✅

```python
# Step 1: Add decorated function
@ml_function(description="New function", capabilities=[])
def my_new_func(self, x: Any) -> Any:
    return x * 2

# That's it! Automatically discovered ✅
```

**Automatic Verification**:
```python
# This test ensures cache matches decorators
def test_cache_matches_decorator_metadata():
    metadata = get_module_metadata("builtin")
    decorated = set(metadata.functions.keys())

    cached = get_all_builtin_functions()

    assert decorated == cached  # ✅ Always true!
```

---

## Extensibility: Works for ALL Modules

This pattern isn't just for `builtin` - it works for **any decorated module**!

```python
# Future: String module functions could use same pattern
def is_string_function(func_name: str) -> bool:
    metadata = get_module_metadata("string")
    return func_name in metadata.functions if metadata else False

# Future: Get all stdlib modules and their functions
def get_all_stdlib_functions() -> dict[str, set[str]]:
    from mlpy.stdlib.decorators import _MODULE_REGISTRY

    result = {}
    for module_name, module_cls in _MODULE_REGISTRY.items():
        if hasattr(module_cls, "_ml_module_metadata"):
            metadata = module_cls._ml_module_metadata
            result[module_name] = set(metadata.functions.keys())

    return result
```

---

## Comparison: Manual vs Decorator-Driven

| Aspect | Manual Registry (v1) | Decorator-Driven (v2) |
|--------|---------------------|----------------------|
| **Source of Truth** | Duplicated (registry + decorators) | Single (`@ml_function`) |
| **Maintenance** | Manual | Automatic |
| **Sync Risk** | HIGH (can diverge) | ZERO (derived) |
| **Extensibility** | Only builtin | All decorated modules |
| **Metadata Access** | None | Full (capabilities, params, etc.) |
| **DRY Principle** | Violated | Followed |
| **Testing** | Hard to verify sync | Easy (test cache == decorators) |
| **Adding Functions** | 3 steps (function + registry + tests) | 1 step (just add decorator) |

---

## Implementation Plan

### Phase 1: Decorator-Driven Cache (2-3 hours)

1. Create `src/mlpy/ml/codegen/builtin_introspection.py`
2. Implement `BuiltinFunctionCache` with lazy initialization
3. Introspect `get_module_metadata("builtin")` to build cache
4. Add convenience functions: `is_builtin_function()`, etc.
5. Unit tests verifying cache matches decorators

### Phase 2: Code Generator Integration (1-2 hours)

1. Import `is_builtin_function` in `python_generator.py`
2. Add tracking fields to `CodeGenContext`
3. Enhance FunctionCall generation with cache lookup
4. Implement scope-aware routing (don't transform user functions)
5. Add auto-import generation

### Phase 3: Security & Testing (2-3 hours)

1. Sandbox builtin restrictions
2. Security bypass tests
3. Comprehensive integration tests
4. Cache consistency tests

### Phase 4: Documentation (1 hour)

1. Document decorator-driven architecture
2. Explain cache vs registry distinction
3. Add examples

**Total Effort**: 6-9 hours

---

## Files Created/Modified

### New Files
1. `src/mlpy/ml/codegen/builtin_introspection.py` - Decorator introspection cache
2. `tests/unit/codegen/test_builtin_introspection.py` - Cache verification tests
3. `tests/unit/codegen/test_builtin_routing.py` - Code generation tests

### Modified Files
1. `src/mlpy/ml/codegen/python_generator.py` - Enhanced FunctionCall handling
2. `src/mlpy/runtime/sandbox/sandbox.py` - Restricted builtins (defense-in-depth)

### NO Manual Registry File
- ❌ No `builtin_registry.py` with manual list
- ✅ Cache derived from decorators instead

---

## Expected Results (Same as Before)

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| **Integration Tests** | 5/16 (31.2%) | 16/16 (100%) | +68.8% |
| **Security** | Vulnerable | Protected | 100% |
| **Semantic Correctness** | 31.2% | 100% | +68.8% |
| **Maintenance Burden** | Manual | Automatic | -100% |
| **Sync Risk** | HIGH | ZERO | Eliminated |

---

## Why This Revision Matters

### The User Was Right

**Original concern**: "I would assume that the necessary metadata is already there - the decorators should provide what we needed"

**You were correct!** The decorators already contain:
- Function names (via `@ml_function`)
- Capabilities
- Descriptions
- Parameter info
- Return type info

Creating a separate registry would have:
- ❌ Violated DRY principle
- ❌ Created maintenance burden
- ❌ Introduced sync risk
- ❌ Limited extensibility

### Better Design Principles

1. **Single Source of Truth**: Decorators define what's a builtin
2. **DRY (Don't Repeat Yourself)**: Derive, don't duplicate
3. **Introspection over Declaration**: Use existing metadata
4. **Extensibility**: Pattern works for any module, not just builtin

---

## Next Steps

1. ✅ **Review revised proposal** - Decorator-driven approach
2. ⏭️ **Begin Phase 1** - Create introspection cache (2-3 hours)
3. ⏭️ **Verify cache** - Unit tests confirm cache matches decorators
4. ⏭️ **Integrate** - Update code generator
5. ⏭️ **Test** - Verify 100% integration test pass rate

**Status**: Ready to implement
**Priority**: CRITICAL
**Estimated Time**: 6-9 hours (reduced from 7-11 hours)
**Key Improvement**: Leverages existing decorator infrastructure
