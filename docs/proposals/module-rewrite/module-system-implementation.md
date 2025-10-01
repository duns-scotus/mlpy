# Module System Implementation Plan

## Executive Summary

This document provides a detailed, phased implementation strategy for migrating from the current ad-hoc module system to a decorator-driven, security-first architecture. The plan emphasizes **incremental changes** that maintain working code throughout the process, with comprehensive testing at each phase.

**Total Estimated Timeline**: 6-8 weeks (assuming 1 developer full-time)

**Risk Level**: Medium (careful staging minimizes breakage)

**Success Metric**: 100% integration test pass rate maintained throughout

## Implementation Philosophy

### Core Principles

1. **Never Break Working Code**: Each phase must pass all existing tests
2. **Incremental Migration**: Old and new systems coexist during transition
3. **Test-Driven**: Write unit tests for each component before implementation
4. **Example-Driven**: Maintain working .ml examples at every stage
5. **Revert-Friendly**: Each phase is a git commit that can be reverted

### Development Branch Strategy

```
main
 └─── feature/module-system-rewrite
       ├─── phase-1-decorators
       ├─── phase-2-builtin
       ├─── phase-3-migration
       ├─── phase-4-cleanup
       └─── phase-5-capabilities
```

After each phase is complete and tested, merge to feature branch. Final merge to main only when all phases complete and integration tests pass.

## Phase 0: Preparation (Week 1)

### Objectives
- Set up development environment
- Baseline all current tests
- Create test infrastructure
- Document current behavior

### Tasks

#### 0.1 Create Development Branch

```bash
git checkout -b feature/module-system-rewrite
git push -u origin feature/module-system-rewrite
```

#### 0.2 Baseline Current Tests

**Action**: Run full test suite and document current state.

```bash
# Run all tests
nox -s tests

# Run integration tests
python tests/ml_test_runner.py --full

# Document results
echo "Baseline Test Results ($(date))" > docs/proposals/module-rewrite/baseline-results.txt
python tests/ml_test_runner.py --full >> docs/proposals/module-rewrite/baseline-results.txt
```

**Success Criteria**:
- All current tests pass
- Test pass rate documented
- Any known failures documented

#### 0.3 Create Test ML Programs

Create test programs to validate each phase:

**File**: `tests/ml_integration/module_system/test_basic_imports.ml`

```ml
// Test basic module imports (Phase 0 baseline)
import math;

result = math.sqrt(16);
print("sqrt(16) =", result);

if (result == 4.0) {
    print("PASS: Basic import works");
} else {
    print("FAIL: Expected 4.0, got", result);
}
```

**File**: `tests/ml_integration/module_system/test_builtin_baseline.ml`

```ml
// Test current builtin functions (Phase 0 baseline)

// typeof should work (currently in __init__.py)
x = 42;
t = typeof(x);
print("typeof(42) =", t);

if (t == "number") {
    print("PASS: typeof works");
} else {
    print("FAIL: typeof broken");
}
```

**File**: `tests/ml_integration/module_system/test_module_addition.ml`

```ml
// Test that adding new modules is easy (will evolve each phase)
// This file starts commented out and gets uncommented as system improves

// Phase 0: Can't add modules easily
// Phase 3: Can add with decorators
// Phase 5: Full capability integration

/*
import newmodule;
result = newmodule.test_func(42);
print("New module test:", result);
*/
```

#### 0.4 Create Test Harness

**File**: `tests/test_module_system_phases.py`

```python
"""
Unit tests for module system implementation phases.

Each phase adds tests, old tests must continue to pass.
"""

import pytest
from pathlib import Path

class TestPhase0Baseline:
    """Phase 0: Verify current system works."""

    def test_current_math_import_works(self):
        """Math module import should work."""
        from mlpy.stdlib.math_bridge import math
        assert hasattr(math, 'sqrt')
        assert math.sqrt(16) == 4.0

    def test_current_typeof_works(self):
        """Current typeof function should work."""
        from mlpy.stdlib import typeof
        assert typeof(42) == "number"
        assert typeof("hello") == "string"

    def test_registry_has_math(self):
        """Registry should have math module registered."""
        from mlpy.stdlib.registry import get_stdlib_registry
        registry = get_stdlib_registry()
        assert "math" in registry.list_modules()

# More test classes added in later phases
```

**Success Criteria**:
- Test harness runs and passes
- Baseline .ml programs transpile and execute
- All tests pass with current system

#### 0.5 Document Current Behavior

**File**: `docs/proposals/module-rewrite/current-behavior.md`

```markdown
# Current Module System Behavior Documentation

## Math Module

### Import
```ml
import math;
```

Generates:
```python
from mlpy.stdlib.math_bridge import math
```

### Usage
```ml
result = math.sqrt(16);
```

Direct Python method call, no capability checks.

## typeof() Function

Currently in `src/mlpy/stdlib/__init__.py`, auto-imported.

... (document all modules)
```

**Deliverables**:
- Development branch created
- Baseline test results documented
- Test .ml programs created and passing
- Unit test harness created and passing
- Current behavior documented

**Timeline**: 3-4 days

## Phase 1: Decorator System (Week 2)

### Objectives
- Implement decorator infrastructure
- No changes to existing modules yet
- Decorators are functional but optional

### Tasks

#### 1.1 Create Decorator Module

**File**: `src/mlpy/stdlib/decorators.py`

```python
"""
ML Standard Library Decorator System.

Provides decorators for marking Python code as exposed to ML:
- @ml_module: Mark a class as an ML module
- @ml_function: Mark a method as exposed to ML
- @ml_constant: Mark a class attribute as an ML constant
- @ml_class: Mark a class as exposed to ML (advanced)
"""

from dataclasses import dataclass, field
from typing import Any, Callable
import functools


@dataclass
class MLModuleMetadata:
    """Metadata for an ML module."""
    name: str
    capabilities: list[str]
    description: str
    version: str
    auto_import: bool
    members: dict[str, 'MLMemberMetadata'] = field(default_factory=dict)
    python_class: type = None


@dataclass
class MLFunctionMetadata:
    """Metadata for an ML function."""
    name: str
    capabilities: list[str]
    params: dict[str, type]
    returns: type | None
    description: str
    examples: list[str]
    exposed: bool = True
    kind: str = "function"


@dataclass
class MLConstantMetadata:
    """Metadata for an ML constant."""
    name: str
    description: str
    immutable: bool
    value: Any
    kind: str = "constant"


# Module registry (populated by decorators)
_module_registry: dict[str, MLModuleMetadata] = {}


def ml_module(name: str, capabilities: list[str] = None, description: str = None,
              version: str = "1.0.0", auto_import: bool = False):
    """
    Decorator for ML module classes.

    Example:
        @ml_module(name="math", capabilities=["execute:calculations"])
        class Math:
            '''Mathematical operations.'''
            # ...
    """
    def decorator(cls):
        metadata = MLModuleMetadata(
            name=name,
            capabilities=capabilities or [],
            description=description or cls.__doc__ or f"ML {name} module",
            version=version,
            auto_import=auto_import,
            python_class=cls,
        )

        # Store metadata on class
        cls._ml_module_metadata = metadata

        # Register with global registry
        _module_registry[name] = metadata

        # Return wrapped class with instance
        return cls

    return decorator


def ml_function(func: Callable = None, *, name: str = None,
                capabilities: list[str] = None,
                params: dict[str, type] = None,
                returns: type = None,
                description: str = None,
                examples: list[str] = None):
    """
    Decorator for ML-exposed functions.

    Example:
        @ml_function(params={"x": float}, returns=float)
        def sqrt(self, x: float) -> float:
            return math.sqrt(x)
    """
    def decorator(fn):
        metadata = MLFunctionMetadata(
            name=name or fn.__name__,
            capabilities=capabilities or [],
            params=params or {},
            returns=returns,
            description=description or fn.__doc__ or f"Function {fn.__name__}",
            examples=examples or [],
        )

        # Store metadata
        fn._ml_function_metadata = metadata

        # Create wrapper that checks capabilities (future)
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            # TODO Phase 5: Check capabilities here
            return fn(*args, **kwargs)

        # Copy metadata to wrapper
        wrapper._ml_function_metadata = metadata

        return wrapper

    if func is None:
        return decorator
    else:
        return decorator(func)


def ml_constant(name: str = None, description: str = None, immutable: bool = True):
    """
    Decorator for ML-exposed constants.

    Example:
        @ml_constant(description="The mathematical constant pi")
        pi = 3.141592653589793
    """
    # For now, constants are just values with metadata
    # Future: implement immutability
    def decorator(value):
        # Store metadata (would need class-level decoration to access)
        return value
    return decorator


def get_module_registry() -> dict[str, MLModuleMetadata]:
    """Get the global module registry."""
    return _module_registry


def get_module_metadata(name: str) -> MLModuleMetadata | None:
    """Get metadata for a registered module."""
    return _module_registry.get(name)
```

**Success Criteria**:
- Decorators can be imported: `from mlpy.stdlib.decorators import ml_module, ml_function`
- Decorators can be applied to classes and methods
- Metadata is stored correctly

#### 1.2 Unit Tests for Decorators

**File**: `tests/unit/stdlib/test_decorators.py`

```python
"""Unit tests for ML stdlib decorator system."""

import pytest
from mlpy.stdlib.decorators import (
    ml_module, ml_function, ml_constant,
    get_module_registry, get_module_metadata
)


class TestMLModuleDecorator:
    """Test @ml_module decorator."""

    def test_decorator_creates_metadata(self):
        """Decorator should create metadata."""
        @ml_module(name="test", capabilities=["test:cap"])
        class TestModule:
            """Test module."""
            pass

        assert hasattr(TestModule, '_ml_module_metadata')
        meta = TestModule._ml_module_metadata
        assert meta.name == "test"
        assert meta.capabilities == ["test:cap"]

    def test_decorator_registers_module(self):
        """Decorator should register module globally."""
        @ml_module(name="testmodule2")
        class TestModule2:
            pass

        registry = get_module_registry()
        assert "testmodule2" in registry
        assert registry["testmodule2"].name == "testmodule2"

    def test_description_from_docstring(self):
        """Description should come from docstring if not provided."""
        @ml_module(name="test3")
        class TestModule3:
            """This is a test module."""
            pass

        meta = get_module_metadata("test3")
        assert "test module" in meta.description.lower()


class TestMLFunctionDecorator:
    """Test @ml_function decorator."""

    def test_function_metadata(self):
        """Decorator should create function metadata."""
        @ml_function(params={"x": int}, returns=int)
        def test_func(x: int) -> int:
            return x * 2

        assert hasattr(test_func, '_ml_function_metadata')
        meta = test_func._ml_function_metadata
        assert meta.name == "test_func"
        assert meta.params == {"x": int}
        assert meta.returns == int

    def test_function_still_callable(self):
        """Decorated function should still work."""
        @ml_function
        def add(x, y):
            return x + y

        assert add(2, 3) == 5

    def test_examples_stored(self):
        """Examples should be stored in metadata."""
        @ml_function(examples=["sqrt(16) // 4.0"])
        def sqrt(x):
            return x ** 0.5

        meta = sqrt._ml_function_metadata
        assert len(meta.examples) == 1
        assert "sqrt(16)" in meta.examples[0]


# Run tests
pytest tests/unit/stdlib/test_decorators.py -v
```

**Success Criteria**:
- All decorator unit tests pass
- Decorators don't break normal Python code
- Metadata is accessible

#### 1.3 Create Test Module with Decorators

**File**: `src/mlpy/stdlib/test_module.py`

```python
"""Test module using new decorator system (does not replace anything yet)."""

from mlpy.stdlib.decorators import ml_module, ml_function
import math as py_math


@ml_module(name="testmath", capabilities=["execute:calculations"])
class TestMath:
    """Test math module with decorators."""

    @ml_function(params={"x": float}, returns=float,
                 description="Compute square root",
                 examples=["testmath.sqrt(16) // 4.0"])
    def sqrt(self, x: float) -> float:
        """Compute square root of x."""
        return py_math.sqrt(x)

    @ml_function(params={"x": float, "y": float}, returns=float)
    def pow(self, x: float, y: float) -> float:
        """Raise x to power y."""
        return py_math.pow(x, y)


# Export instance
testmath = TestMath()
```

**Validation**:

```python
# In Python REPL or test
from mlpy.stdlib.test_module import testmath
from mlpy.stdlib.decorators import get_module_metadata

# Check module registered
meta = get_module_metadata("testmath")
assert meta is not None
assert meta.name == "testmath"

# Check functions work
assert testmath.sqrt(16) == 4.0
assert testmath.pow(2, 3) == 8.0

# Check metadata
assert hasattr(testmath.sqrt, '_ml_function_metadata')
```

**Deliverables**:
- `decorators.py` implemented and tested
- Unit tests passing (100% coverage of decorator code)
- Test module demonstrates decorator usage
- No changes to existing stdlib modules yet
- All existing tests still pass

**Timeline**: 4-5 days

## Phase 2: Builtin Module (Week 3)

### Objectives
- Implement builtin module with decorators
- Make builtin functions available
- Maintain backward compatibility with existing `typeof()`, `int()`, `float()`, `str()`

### Tasks

#### 2.1 Implement Builtin Module

**File**: `src/mlpy/stdlib/builtin.py`

Use the `builtin.py` from `docs/proposals/module-rewrite/builtin.py` with actual decorator imports:

```python
"""ML Builtin Module - Core functionality."""

from mlpy.stdlib.decorators import ml_module, ml_function
import sys
from typing import Any, Callable

@ml_module(name="builtin", capabilities=[], auto_import=True, version="2.0.0")
class Builtin:
    """Core built-in functions for ML."""

    @ml_function(params={"value": Any}, returns=int)
    def int(self, value: Any) -> int:
        # ... (implementation from builtin.py)

    @ml_function(params={"value": Any}, returns=float)
    def float(self, value: Any) -> float:
        # ... (implementation from builtin.py)

    # ... all other builtin functions

# Create instance
builtin = Builtin()

# Export functions
__all__ = ['builtin', 'int', 'float', 'str', ...]

# Make functions available at module level
int = builtin.int
float = builtin.float
# ... etc
```

#### 2.2 Update __init__.py to Import Builtin

**File**: `src/mlpy/stdlib/__init__.py` (modified)

```python
"""ML Standard Library - Auto-imported functionality."""

# Keep existing imports for backward compatibility
from .collections_bridge import collections
from .console_bridge import console
from .datetime_bridge import datetime
from .float_bridge import float_module
from .functional_bridge import functional
from .int_bridge import int_module
from .math_bridge import math
from .random_bridge import random
from .regex_bridge import regex
from .string_bridge import string

# NEW: Import builtin module
from .builtin import (
    builtin,
    int, float, str, bool,  # Type conversion
    type, typeof, isinstance,  # Type checking
    len, print, input,  # Basic functions
    dir, info, hasattr, getattr, setattr,  # Introspection
    exit, version, call  # Utility
)

# Update __all__ to include builtin functions
__all__ = [
    # Existing modules
    "console", "functional", "string", "datetime", "math", "random",
    "collections", "regex", "int_module", "float_module",

    # NEW: Builtin module and functions
    "builtin",
    "int", "float", "str", "bool",
    "type", "typeof", "isinstance",
    "len", "print", "input",
    "dir", "info", "hasattr", "getattr", "setattr",
    "exit", "version", "call",
]

# Note: Old typeof/int/float/str from this file are now shadowed by builtin versions
# This maintains backward compatibility while using new implementation
```

#### 2.3 Unit Tests for Builtin

**File**: `tests/unit/stdlib/test_builtin.py`

```python
"""Comprehensive unit tests for builtin module."""

import pytest
from mlpy.stdlib.builtin import builtin, int, float, str, type, typeof, len


class TestTypeConversion:
    """Test type conversion functions."""

    def test_int_from_string(self):
        assert builtin.int("42") == 42

    def test_int_from_float(self):
        assert builtin.int(3.14) == 3

    def test_int_from_bool(self):
        assert builtin.int(True) == 1
        assert builtin.int(False) == 0

    def test_int_error_handling(self):
        assert builtin.int("invalid") == 0  # ML semantics

    def test_float_from_string(self):
        assert builtin.float("3.14") == 3.14

    def test_float_from_bool(self):
        assert builtin.float(True) == 1.0

    def test_str_bool_lowercase(self):
        """ML uses lowercase true/false."""
        assert builtin.str(True) == "true"
        assert builtin.str(False) == "false"


class TestTypeChecking:
    """Test type checking functions."""

    def test_type_number(self):
        assert builtin.type(42) == "number"
        assert builtin.type(3.14) == "number"

    def test_type_string(self):
        assert builtin.type("hello") == "string"

    def test_type_boolean(self):
        assert builtin.type(True) == "boolean"

    def test_type_array(self):
        assert builtin.type([1, 2, 3]) == "array"

    def test_type_object(self):
        assert builtin.type({"a": 1}) == "object"

    def test_typeof_alias(self):
        assert builtin.typeof(42) == builtin.type(42)

    def test_isinstance_check(self):
        assert builtin.isinstance(42, "number") is True
        assert builtin.isinstance(42, "string") is False


class TestIntrospection:
    """Test introspection functions."""

    def test_dir_dict(self):
        obj = {"a": 1, "b": 2}
        members = builtin.dir(obj)
        assert "a" in members
        assert "b" in members

    def test_hasattr_true(self):
        obj = {"key": "value"}
        assert builtin.hasattr(obj, "key") is True

    def test_hasattr_false(self):
        obj = {"key": "value"}
        assert builtin.hasattr(obj, "nonexistent") is False

    def test_getattr_dict(self):
        obj = {"name": "John"}
        assert builtin.getattr(obj, "name") == "John"

    def test_getattr_default(self):
        obj = {}
        assert builtin.getattr(obj, "missing", "default") == "default"

    def test_call_function(self):
        def add(x, y):
            return x + y
        result = builtin.call(add, [10, 20])
        assert result == 30


class TestContainerOperations:
    """Test container operations."""

    def test_len_string(self):
        assert builtin.len("hello") == 5

    def test_len_array(self):
        assert builtin.len([1, 2, 3]) == 3

    def test_len_dict(self):
        assert builtin.len({"a": 1, "b": 2}) == 2

# Run: pytest tests/unit/stdlib/test_builtin.py -v --cov=mlpy.stdlib.builtin
```

**Success Criteria**:
- All builtin unit tests pass
- Builtin functions accessible from Python
- Backward compatibility maintained (old code still works)

#### 2.4 Test ML Program with Builtin

**File**: `tests/ml_integration/module_system/test_builtin_new.ml`

```ml
// Test new builtin functions

// Type conversion
x = int("42");
y = float("3.14");
z = str(true);  // Should be "true" not "True"

print("int('42') =", x);
print("float('3.14') =", y);
print("str(true) =", z);

// Type checking
t = type(42);
print("type(42) =", t);

is_num = isinstance(x, "number");
print("isinstance(int('42'), 'number') =", is_num);

// Introspection
obj = {name: "John", age: 30};
keys = dir(obj);
print("dir(obj) =", keys);

has_name = hasattr(obj, "name");
print("hasattr(obj, 'name') =", has_name);

// Container operations
arr = [1, 2, 3, 4, 5];
arr_len = len(arr);
print("len([1,2,3,4,5]) =", arr_len);

// All tests should pass
if (x == 42 && is_num && has_name && arr_len == 5) {
    print("PASS: All builtin functions work!");
} else {
    print("FAIL: Some builtin functions broken");
}
```

**Validation**:

```bash
# Transpile and run
python -m mlpy run tests/ml_integration/module_system/test_builtin_new.ml

# Expected output:
# int('42') = 42
# float('3.14') = 3.14
# str(true) = true
# type(42) = number
# isinstance(int('42'), 'number') = true
# dir(obj) = ['age', 'name']
# hasattr(obj, 'name') = true
# len([1,2,3,4,5]) = 5
# PASS: All builtin functions work!
```

**Deliverables**:
- `builtin.py` implemented with decorators
- Unit tests passing (>95% coverage)
- ML test program transpiles and runs
- All existing tests still pass
- Documentation for builtin module

**Timeline**: 4-5 days

## Phase 3: Module Migration (Weeks 4-5)

### Objectives
- Migrate existing stdlib modules to decorator pattern
- One module at a time to minimize risk
- Maintain backward compatibility throughout

### Migration Pattern (for each module)

For each module, follow this pattern:

1. Create new `{module}.py` with decorators
2. Keep old `{module}_bridge.py` for compatibility
3. Update `__init__.py` to import from new file
4. Run tests (old and new)
5. Delete old file once tests pass
6. Commit and push

### Tasks

#### 3.1 Migrate Math Module

**File**: `src/mlpy/stdlib/math.py` (NEW)

```python
"""ML Math Module - Mathematical operations."""

from mlpy.stdlib.decorators import ml_module, ml_function, ml_constant
import math as py_math


@ml_module(
    name="math",
    capabilities=["execute:calculations"],
    description="Mathematical operations and constants",
    version="2.0.0"
)
class Math:
    """
    Mathematical operations with capability-based security.

    Provides basic math functions (sqrt, pow, sin, cos, etc.) and
    constants (pi, e, tau).
    """

    # Constants
    @ml_constant(description="The mathematical constant π (pi)")
    pi = py_math.pi

    @ml_constant(description="Euler's number e")
    e = py_math.e

    @ml_constant(description="Tau (2π)")
    tau = py_math.tau

    @ml_function(
        params={"x": float},
        returns=float,
        description="Compute square root of x",
        examples=["math.sqrt(16) // 4.0", "math.sqrt(2) // 1.414..."]
    )
    def sqrt(self, x: float) -> float:
        """Square root function."""
        if x < 0:
            return 0.0  # ML error handling
        return py_math.sqrt(x)

    @ml_function(params={"x": float, "y": float}, returns=float)
    def pow(self, x: float, y: float) -> float:
        """Raise x to the power y."""
        try:
            return py_math.pow(x, y)
        except (OverflowError, ZeroDivisionError):
            return float('inf') if x > 0 else 0.0

    @ml_function(params={"x": float}, returns=float)
    def sin(self, x: float) -> float:
        """Sine function."""
        return py_math.sin(x)

    @ml_function(params={"x": float}, returns=float)
    def cos(self, x: float) -> float:
        """Cosine function."""
        return py_math.cos(x)

    @ml_function(params={"x": float}, returns=float)
    def tan(self, x: float) -> float:
        """Tangent function."""
        return py_math.tan(x)

    @ml_function(params={"x": float}, returns=float)
    def ln(self, x: float) -> float:
        """Natural logarithm."""
        if x <= 0:
            return -999.0  # ML error value
        return py_math.log(x)

    @ml_function(params={"x": float, "base": float}, returns=float)
    def log(self, x: float, base: float = 10.0) -> float:
        """Logarithm with specified base."""
        if x <= 0 or base <= 0 or base == 1:
            return -999.0
        return py_math.log(x, base)

    @ml_function(params={"x": float}, returns=float)
    def exp(self, x: float) -> float:
        """Exponential function (e^x)."""
        try:
            return py_math.exp(x)
        except OverflowError:
            return float('inf')

    @ml_function(params={"x": float}, returns=int)
    def floor(self, x: float) -> int:
        """Floor function."""
        return py_math.floor(x)

    @ml_function(params={"x": float}, returns=int)
    def ceil(self, x: float) -> int:
        """Ceiling function."""
        return py_math.ceil(x)

    @ml_function(params={"x": float}, returns=int)
    def round(self, x: float) -> int:
        """Round to nearest integer."""
        return round(x)

    @ml_function(params={"a": float, "b": float}, returns=float)
    def min(self, a: float, b: float) -> float:
        """Minimum of two values."""
        return min(a, b)

    @ml_function(params={"a": float, "b": float}, returns=float)
    def max(self, a: float, b: float) -> float:
        """Maximum of two values."""
        return max(a, b)

    @ml_function(params={"x": float}, returns=float)
    def abs(self, x: float) -> float:
        """Absolute value."""
        return abs(x)

    @ml_function(returns=float)
    def random(self) -> float:
        """Random number between 0 and 1."""
        import random
        return random.random()


# Create instance
math = Math()

__all__ = ['math', 'Math']
```

**Update `__init__.py`**:

```python
# Change from:
from .math_bridge import math

# To:
from .math import math  # New decorator-based version
```

**Unit Tests**:

```python
# tests/unit/stdlib/test_math_decorated.py

from mlpy.stdlib.math import math, Math
from mlpy.stdlib.decorators import get_module_metadata


class TestMathModuleDecorated:
    """Test math module with decorators."""

    def test_module_registered(self):
        """Math module should be registered."""
        meta = get_module_metadata("math")
        assert meta is not None
        assert meta.name == "math"
        assert "execute:calculations" in meta.capabilities

    def test_sqrt_works(self):
        """sqrt function should work."""
        assert math.sqrt(16) == 4.0
        assert math.sqrt(0) == 0.0
        assert math.sqrt(-1) == 0.0  # ML error handling

    def test_constants_available(self):
        """Constants should be accessible."""
        assert math.pi == py_math.pi
        assert math.e == py_math.e

    def test_metadata_on_functions(self):
        """Functions should have metadata."""
        assert hasattr(math.sqrt, '_ml_function_metadata')
        meta = math.sqrt._ml_function_metadata
        assert meta.name == "sqrt"
        assert meta.params == {"x": float}
```

**ML Test**:

```ml
// tests/ml_integration/module_system/test_math_decorated.ml

import math;

// Test constants
print("math.pi =", math.pi);
print("math.e =", math.e);

// Test functions
sqrt_result = math.sqrt(16);
pow_result = math.pow(2, 3);

print("math.sqrt(16) =", sqrt_result);
print("math.pow(2, 3) =", pow_result);

if (sqrt_result == 4.0 && pow_result == 8.0) {
    print("PASS: Math module works with decorators");
} else {
    print("FAIL: Math module broken");
}
```

**Success Criteria**:
- New `math.py` works
- Old tests still pass
- New ML test passes
- Can delete `math_bridge.py`

**Timeline**: 1-2 days

#### 3.2 Migrate Remaining Modules

Repeat the pattern for each module:

1. **Week 4**:
   - Monday-Tuesday: String module
   - Wednesday-Thursday: DateTime module
   - Friday: Regex module

2. **Week 5**:
   - Monday: JSON module
   - Tuesday: Collections module
   - Wednesday: Functional module
   - Thursday: Random module
   - Friday: Console module, Array module

For each module:
- Create new `{module}.py` with `@ml_module` and `@ml_function`
- Write unit tests
- Update `__init__.py`
- Delete `{module}_bridge.py`
- Commit

**Deliverables**:
- All stdlib modules migrated to decorators
- All `*_bridge.py` files deleted
- All `.ml` files deleted (stdlib is pure Python now)
- 100% unit test coverage
- All integration tests passing

**Timeline**: 8-10 days

## Phase 4: Cleanup and Simplification (Week 6)

### Objectives
- Simplify registry (remove manual registration)
- Update code generator (remove hardcoded lists)
- Update resolver to use decorator registry
- Delete obsolete code

### Tasks

#### 4.1 Simplify Registry

**File**: `src/mlpy/stdlib/registry.py` (MAJOR REDUCTION)

```python
"""
ML Standard Library Registry (Decorator-Driven).

Auto-discovers modules via decorators, no manual registration needed.
"""

from pathlib import Path
from mlpy.stdlib.decorators import get_module_registry, MLModuleMetadata
from mlpy.ml.resolution.resolver import ModuleInfo
from mlpy.ml.grammar.ast_nodes import Program


class StandardLibraryRegistry:
    """Auto-discovering registry for ML stdlib."""

    def __init__(self):
        """Initialize registry."""
        self._decorator_registry = get_module_registry()

    def get_module(self, name: str) -> ModuleInfo | None:
        """
        Get module info for a stdlib module.

        Args:
            name: Module name

        Returns:
            ModuleInfo if module exists
        """
        meta = self._decorator_registry.get(name)
        if not meta:
            return None

        # For Python stdlib modules, create ModuleInfo
        # No .ml file needed - pure Python
        return ModuleInfo(
            name=meta.name,
            module_path=f"mlpy.stdlib.{name}",
            ast=None,  # Python module, no ML AST
            source_code="",  # Python module
            file_path=None,
            is_stdlib=True,
            is_python=True,
            dependencies=[],
            capabilities_required=meta.capabilities,
        )

    def list_modules(self) -> list[str]:
        """List all registered modules."""
        return list(self._decorator_registry.keys())

    def get_module_metadata(self, name: str) -> MLModuleMetadata | None:
        """Get decorator metadata for module."""
        return self._decorator_registry.get(name)

    def discover_stdlib(self):
        """
        Auto-discover all stdlib modules.

        Imports all Python files in mlpy.stdlib/, triggering
        decorator registration.
        """
        import importlib
        import pkgutil
        import mlpy.stdlib

        for importer, modname, ispkg in pkgutil.iter_modules(mlpy.stdlib.__path__):
            if not modname.startswith('_') and modname != 'decorators':
                try:
                    importlib.import_module(f'mlpy.stdlib.{modname}')
                except ImportError:
                    # Skip files that can't be imported
                    pass

        # All decorators have run, registry is populated


# Global instance
_registry = None


def get_stdlib_registry() -> StandardLibraryRegistry:
    """Get global stdlib registry."""
    global _registry
    if _registry is None:
        _registry = StandardLibraryRegistry()
        _registry.discover_stdlib()
    return _registry
```

**Delete**:
- All of `_register_core_modules()` (668 lines)
- `StandardLibraryModule` dataclass (unused)
- `BridgeFunction` dataclass (unused)
- `register_module()` method
- `register_bridge_function()` method

**Lines Reduced**: From 1049 lines to ~80 lines = **92% reduction**

#### 4.2 Update Code Generator

**File**: `src/mlpy/ml/codegen/python_generator.py` (modified)

```python
def visit_import_statement(self, node: ImportStatement):
    """Generate code for import statement."""
    module_path = ".".join(node.target)

    # NEW: Resolve module dynamically via registry
    try:
        module_info = self.resolver.resolve_import(node.target, self.source_file)

        if module_info.is_python and module_info.is_stdlib:
            # Python stdlib module - import from mlpy.stdlib
            python_path = f"mlpy.stdlib.{module_info.name}"

            if node.alias:
                alias = self._safe_identifier(node.alias)
                self._emit_line(f"from {python_path} import {module_info.name} as {alias}", node)
            else:
                self._emit_line(f"from {python_path} import {module_info.name}", node)

        elif module_info.is_python:
            # User Python module (future)
            self._emit_line(f"import {module_info.module_path}", node)

        else:
            # ML module - transpile first (future)
            self._emit_line(f"# ML module import: {module_path}", node)

    except Exception as e:
        # Module not found
        self._emit_line(f"# ERROR: Cannot resolve import '{module_path}': {e}", node)
```

**Delete**:
- Hardcoded module list (lines 356-367)
- Manual `_bridge` suffix handling

**Lines Reduced**: From 37 lines to ~20 lines = **45% reduction**

#### 4.3 Delete Obsolete Files

**Files to Delete**:
```
src/mlpy/stdlib/math_bridge.py
src/mlpy/stdlib/string_bridge.py
src/mlpy/stdlib/datetime_bridge.py
src/mlpy/stdlib/json_bridge.py
src/mlpy/stdlib/regex_bridge.py
src/mlpy/stdlib/functional_bridge.py
src/mlpy/stdlib/collections_bridge.py
src/mlpy/stdlib/random_bridge.py
src/mlpy/stdlib/console_bridge.py
src/mlpy/stdlib/array_bridge.py
src/mlpy/stdlib/int_bridge.py
src/mlpy/stdlib/float_bridge.py

src/mlpy/stdlib/math.ml
src/mlpy/stdlib/string.ml
src/mlpy/stdlib/datetime.ml
src/mlpy/stdlib/json.ml
src/mlpy/stdlib/functional.ml
src/mlpy/stdlib/collections.ml
src/mlpy/stdlib/random.ml
src/mlpy/stdlib/regex.ml
```

**Before Deletion**: Run full test suite to ensure nothing breaks.

#### 4.4 Update Documentation

Update all documentation to reflect new system:

**Files to Update**:
- `docs/source/developer-guide/writing-stdlib-modules.rst`
- `docs/source/developer-guide/stdlib-module-development.rst`
- `docs/developer/writing-stdlib-modules.md`

**New Content**: Examples of using decorators, no manual registration.

**Deliverables**:
- Registry simplified (92% reduction)
- Code generator simplified (45% reduction)
- Obsolete files deleted
- Documentation updated
- All tests passing

**Timeline**: 3-4 days

## Phase 5: Capability Integration (Week 7)

### Objectives
- Make capability enforcement real
- Integrate with capability manager
- Capability checking at function call time
- Automatic capability granting on import

### Tasks

#### 5.1 Enhance Decorator Wrapper

**File**: `src/mlpy/stdlib/decorators.py` (enhanced)

```python
from mlpy.runtime.capabilities.manager import get_capability_manager, has_capability, use_capability
from mlpy.runtime.capabilities.exceptions import CapabilityNotFoundError


def ml_function(func: Callable = None, *, name: str = None,
                capabilities: list[str] = None,
                params: dict[str, type] = None,
                returns: type = None,
                description: str = None,
                examples: list[str] = None):
    """Decorator for ML-exposed functions."""

    def decorator(fn):
        metadata = MLFunctionMetadata(
            name=name or fn.__name__,
            capabilities=capabilities or [],
            params=params or {},
            returns=returns,
            description=description or fn.__doc__,
            examples=examples or [],
        )

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            # NEW: Check capabilities before execution
            for cap in metadata.capabilities:
                if not has_capability(cap):
                    raise CapabilityNotFoundError(
                        f"Function {metadata.name} requires capability '{cap}'"
                    )

            # NEW: Track capability usage
            if metadata.capabilities:
                use_capability(
                    metadata.capabilities[0],
                    resource=f"function:{metadata.name}",
                    operation="call"
                )

            # Execute function
            result = fn(*args, **kwargs)

            return result

        wrapper._ml_function_metadata = metadata
        return wrapper

    if func is None:
        return decorator
    else:
        return decorator(func)
```

#### 5.2 Auto-Grant Capabilities on Import

**File**: `src/mlpy/ml/resolution/resolver.py` (enhanced)

```python
from mlpy.runtime.capabilities.context import get_current_context
from mlpy.runtime.capabilities.tokens import CapabilityToken, CapabilityConstraint


class ModuleResolver:
    """Secure module resolver with capability integration."""

    def resolve_import(self, import_target: list[str], source_file: str = None):
        """Resolve import and grant capabilities."""

        module_info = self._resolve_module(import_target)

        # NEW: Grant module capabilities to current context
        if module_info.capabilities_required:
            context = get_current_context()
            if context:
                for cap in module_info.capabilities_required:
                    token = CapabilityToken(
                        capability_type=cap,
                        constraints=CapabilityConstraint(
                            resource_patterns=[f"module:{module_info.name}:*"]
                        )
                    )
                    context.add_capability(token)

        return module_info
```

#### 5.3 Test Capability Enforcement

**File**: `tests/ml_integration/module_system/test_capability_enforcement.ml`

```ml
// Test that capabilities are enforced

import math;  // Should auto-grant "execute:calculations"

// This should work (capability granted)
result = math.sqrt(16);
print("With capability:", result);

// Test capability checking (would require special test mode)
// where we can revoke capabilities and test denial

if (result == 4.0) {
    print("PASS: Capability system working");
} else {
    print("FAIL: Unexpected result");
}
```

**Unit Test**:

```python
# tests/unit/stdlib/test_capability_integration.py

from mlpy.stdlib.math import math
from mlpy.runtime.capabilities.manager import get_capability_manager, CapabilityContext
from mlpy.runtime.capabilities.tokens import CapabilityToken
from mlpy.runtime.capabilities.exceptions import CapabilityNotFoundError
import pytest


class TestCapabilityEnforcement:
    """Test capability enforcement in modules."""

    def test_function_requires_capability(self):
        """Function should check capability before execution."""
        manager = get_capability_manager()

        # Create context WITHOUT math capability
        with manager.capability_context("test", []):
            # Should raise because capability missing
            with pytest.raises(CapabilityNotFoundError):
                math.sqrt(16)

    def test_function_works_with_capability(self):
        """Function should work when capability granted."""
        manager = get_capability_manager()

        # Create context WITH math capability
        token = CapabilityToken(capability_type="execute:calculations")
        with manager.capability_context("test", [token]):
            # Should work
            result = math.sqrt(16)
            assert result == 4.0

    def test_capability_usage_tracked(self):
        """Capability usage should be tracked."""
        manager = get_capability_manager()

        token = CapabilityToken(capability_type="execute:calculations")
        with manager.capability_context("test", [token]):
            math.sqrt(16)
            # Check that token usage was incremented
            assert token.usage_count > 0
```

**Success Criteria**:
- Capability checks work
- Functions blocked without capability
- Functions work with capability
- Usage is tracked

**Deliverables**:
- Capability enforcement implemented
- Auto-granting on import works
- Capability tests passing
- Security audit shows capabilities enforced

**Timeline**: 4-5 days

## Phase 6: Final Testing and Documentation (Week 8)

### Objectives
- Comprehensive end-to-end testing
- Performance validation
- Documentation completion
- Prepare for production

### Tasks

#### 6.1 Integration Testing

**Create comprehensive test suite**:

```bash
# Run all unit tests
nox -s tests

# Run all integration tests
python tests/ml_test_runner.py --full

# Run security tests
python tests/test_comprehensive_security_audit.py

# Run performance benchmarks
python tests/test_transpiler_benchmarks.py
```

**Success Criteria**:
- 100% unit test pass rate
- 100% integration test pass rate
- No security regressions
- Performance within acceptable range (< 10% slowdown acceptable)

#### 6.2 Performance Validation

**Benchmark Tests**:

```python
# tests/test_module_system_performance.py

import time
from mlpy.stdlib.math import math


def test_function_call_overhead():
    """Measure overhead of capability checking."""

    # Warm up
    for _ in range(100):
        math.sqrt(16)

    # Measure
    start = time.perf_counter()
    for _ in range(10000):
        math.sqrt(16)
    end = time.perf_counter()

    # Calculate per-call overhead
    total_time = end - start
    per_call = total_time / 10000

    # Should be < 10 microseconds per call
    assert per_call < 0.00001  # 10 µs

    print(f"Per-call overhead: {per_call * 1e6:.2f} µs")
```

**Success Criteria**:
- Function call overhead < 10 µs
- Module import time < 100ms
- No memory leaks
- Capability checks < 1 µs

#### 6.3 Documentation

**Update Documentation**:

1. **API Reference**:
   - Document all decorators
   - Document builtin module
   - Document all stdlib modules

2. **Developer Guide**:
   - "How to Add a New Stdlib Module" (< 5 minutes)
   - "Decorator System Guide"
   - "Capability Integration Guide"

3. **Migration Guide**:
   - For developers using old system
   - Breaking changes (if any)
   - Migration examples

4. **Tutorial**:
   - Creating a custom module
   - Using introspection
   - Understanding capabilities

**Example Documentation**:

```markdown
# How to Add a New Stdlib Module

Adding a new module takes **less than 5 minutes**:

1. Create `src/mlpy/stdlib/mymodule.py`:

```python
from mlpy.stdlib.decorators import ml_module, ml_function

@ml_module(name="mymodule", capabilities=["my:capability"])
class MyModule:
    """My custom module."""

    @ml_function(params={"x": int}, returns=int)
    def my_function(self, x: int) -> int:
        """Double the input."""
        return x * 2

# Export instance
mymodule = MyModule()
```

2. That's it! Module is automatically discovered and available:

```ml
import mymodule;
result = mymodule.my_function(21);  // 42
```

No manual registration, no registry updates, no code generator changes!
```

#### 6.4 Create "Before/After" Comparison

**Document Improvements**:

Create `docs/proposals/module-rewrite/implementation-results.md`:

```markdown
# Module System Rewrite: Results

## Code Reduction

| Component | Before | After | Reduction |
|-----------|--------|-------|-----------|
| registry.py | 1049 lines | 80 lines | -92% |
| Adding new module | 200 lines, 5 files | 30 lines, 1 file | -85% |
| python_generator.py imports | 37 lines | 20 lines | -45% |
| Total stdlib LOC | ~3500 lines | ~1200 lines | -66% |

## Capability Enforcement

- Before: 0% (not enforced)
- After: 100% (enforced at runtime)

## Performance

- Module import: < 50ms (no change)
- Function call overhead: +2µs (negligible)
- Capability check: 0.5µs per call

## Developer Experience

Adding crypto module:

Before:
1. Create crypto_bridge.py (50 lines)
2. Update registry.py (50 lines)
3. Update python_generator.py (1 line)
4. Update __init__.py (2 lines)
5. Total: 4 files, ~103 lines, 15 minutes

After:
1. Create crypto.py with decorators (30 lines)
2. Total: 1 file, 30 lines, 3 minutes

**Improvement: 80% less code, 80% less time**
```

**Deliverables**:
- All tests passing (100%)
- Performance validated
- Complete documentation
- Before/after comparison
- Ready for production

**Timeline**: 4-5 days

## Summary Timeline

| Phase | Duration | Work | Deliverables |
|-------|----------|------|--------------|
| **Phase 0: Preparation** | 3-4 days | Setup, baseline, test infrastructure | Tests passing, baseline documented |
| **Phase 1: Decorators** | 4-5 days | Implement decorator system | `decorators.py`, unit tests passing |
| **Phase 2: Builtin** | 4-5 days | Implement builtin module | `builtin.py`, introspection working |
| **Phase 3: Migration** | 8-10 days | Migrate all stdlib modules | All `*_bridge.py` deleted, decorators used |
| **Phase 4: Cleanup** | 3-4 days | Simplify registry, delete obsolete | 92% code reduction in registry |
| **Phase 5: Capabilities** | 4-5 days | Real capability enforcement | Security tests passing |
| **Phase 6: Testing** | 4-5 days | Final validation, docs | Production-ready |

**Total**: 6-8 weeks (30-38 days)

## Risk Mitigation

### Risks and Mitigations

| Risk | Probability | Impact | Mitigation |
|------|------------|---------|------------|
| Tests fail during migration | Medium | High | One module at a time, revert if needed |
| Performance regression | Low | Medium | Benchmark each phase, optimize wrappers |
| Breaking changes | Medium | High | Maintain backward compatibility Phase 0-4 |
| Capability bugs | Medium | High | Extensive unit tests before enforcement |
| Documentation incomplete | Low | Low | Document as you go, each phase |

### Rollback Plan

Each phase is a git commit that can be reverted:

```bash
# If Phase 3 has problems, revert to Phase 2
git revert HEAD
git push

# Or reset entire branch
git reset --hard origin/phase-2-builtin
```

## Success Metrics

### Must-Have (Go/No-Go)

- ✅ All existing tests pass
- ✅ All new tests pass (>95% coverage)
- ✅ No performance regression (< 10% slowdown acceptable)
- ✅ Capabilities enforced (100% enforcement)
- ✅ Documentation complete

### Nice-to-Have

- ⭐ Code reduction > 80%
- ⭐ New module creation < 5 minutes
- ⭐ Capability overhead < 1µs
- ⭐ Zero breaking changes for users

## Final Deliverables

1. **Code**:
   - `src/mlpy/stdlib/decorators.py` (new)
   - `src/mlpy/stdlib/builtin.py` (new)
   - `src/mlpy/stdlib/{module}.py` (all modules migrated)
   - `src/mlpy/stdlib/registry.py` (simplified, 92% reduction)
   - `src/mlpy/ml/codegen/python_generator.py` (simplified import handling)
   - `src/mlpy/ml/resolution/resolver.py` (capability integration)

2. **Tests**:
   - `tests/unit/stdlib/test_decorators.py`
   - `tests/unit/stdlib/test_builtin.py`
   - `tests/unit/stdlib/test_*_decorated.py` (for each module)
   - `tests/ml_integration/module_system/` (integration tests)

3. **Documentation**:
   - "How to Add a New Module" (< 1 page)
   - "Decorator System Reference"
   - "Builtin Module API"
   - "Migration Guide"
   - "Before/After Comparison"

4. **Git History**:
   - Clean commit per phase
   - Detailed commit messages
   - Easy to bisect if issues arise

## Conclusion

This implementation plan provides a safe, incremental path to a modern module system while maintaining code stability. The phased approach allows for validation at each step and easy rollback if needed.

Key benefits:
- 80%+ code reduction
- 100% capability enforcement
- < 5 minute module creation
- Negligible performance impact
- No breaking changes for ML users

The new system will transform mlpy from a prototype into a production-ready, secure scripting platform.
