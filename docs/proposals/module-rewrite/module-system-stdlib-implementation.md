# Standard Library Implementation Plan

## Executive Summary

This document provides a detailed, phased implementation plan for mlpy's standard library using the new decorator-based module system. The plan prioritizes modules by:
1. **Necessity** - Core functionality needed for basic programs
2. **Dependencies** - Build foundation modules first
3. **Security** - Simple modules before capability-intensive ones
4. **Complexity** - Easy implementations before complex ones

**Timeline**: 8-10 weeks for complete minimal stdlib (15 modules)

**Approach**: One module at a time, fully tested and documented before moving to next

---

## Module Prioritization Matrix

### Priority Calculation

| Module | Necessity | Usage | Complexity | Security | Priority Score |
|--------|-----------|-------|------------|----------|----------------|
| builtin | Critical | 100% | Low | Low | **10/10** |
| math | High | 90% | Low | Low | **9/10** |
| string | High | 85% | Low | Low | **9/10** |
| array | High | 80% | Low | Low | **8/10** |
| console | High | 75% | Low | Low | **8/10** |
| json | High | 70% | Low | Low | **8/10** |
| datetime | Medium | 60% | Medium | Low | **7/10** |
| regex | Medium | 55% | Medium | Low | **7/10** |
| random | Medium | 50% | Low | Low | **7/10** |
| functional | Medium | 65% | Low | Low | **7/10** |
| file | High | 70% | Medium | **High** | **6/10** |
| http | Medium | 50% | High | **High** | **5/10** |
| crypto | Medium | 40% | Medium | Medium | **5/10** |
| sqlite | Low | 30% | High | **High** | **4/10** |
| tcp | Low | 20% | High | **High** | **3/10** |

---

## Implementation Tiers

### Tier 1: Foundation (Weeks 1-2)

**Modules**: builtin, math, string, array, console

**Rationale**: Zero external dependencies, low security risk, essential for basic programs

**Deliverables**: 5 modules, 100+ functions, 200+ tests

### Tier 2: Data & Utilities (Weeks 3-4)

**Modules**: json, datetime, regex, random, functional

**Rationale**: Common utilities, still low security risk, enable real programs

**Deliverables**: 5 modules, 150+ functions, 250+ tests

### Tier 3: Secure I/O (Weeks 5-6)

**Modules**: file, crypto, collections

**Rationale**: Capability-intensive, require security integration

**Deliverables**: 3 modules, 80+ functions, 150+ tests

### Tier 4: Advanced (Weeks 7-8)

**Modules**: http, sqlite

**Rationale**: Complex, high security requirements, specialized use cases

**Deliverables**: 2 modules, 60+ functions, 100+ tests

### Tier 5: Specialized (Future)

**Modules**: tcp, csv, base64, xml, yaml, compression

**Rationale**: Lower priority, can be added as needed

**Deliverables**: TBD based on user demand

---

## Tier 1 Implementation (Weeks 1-2)

### Module 1.1: builtin (Week 1, Days 1-2)

**Status**: ✅ Already designed in `builtin.py`

**Purpose**: Core functionality available in all ML programs

**Implementation**:

```python
@ml_module(
    name="builtin",
    capabilities=[],  # No capabilities - core functionality
    description="Core built-in functions for ML programs",
    version="2.0.0",
    auto_import=True  # Automatically available
)
class Builtin:
    """Built-in functions and utilities."""

    # Type Conversion (4 functions)
    @ml_function(params={"value": Any}, returns=int)
    def int(self, value: Any) -> int: ...

    @ml_function(params={"value": Any}, returns=float)
    def float(self, value: Any) -> float: ...

    @ml_function(params={"value": Any}, returns=str)
    def str(self, value: Any) -> str: ...

    @ml_function(params={"value": Any}, returns=bool)
    def bool(self, value: Any) -> bool: ...

    # Type Checking (3 functions)
    @ml_function(params={"value": Any}, returns=str)
    def type(self, value: Any) -> str: ...

    @ml_function(params={"value": Any}, returns=str)
    def typeof(self, value: Any) -> str: ...

    @ml_function(params={"value": Any, "type_name": str}, returns=bool)
    def isinstance(self, value: Any, type_name: str) -> bool: ...

    # Introspection (6 functions)
    @ml_function(params={"obj": Any}, returns=list)
    def dir(self, obj: Any) -> list: ...

    @ml_function(params={"obj": Any}, returns=str)
    def info(self, obj: Any) -> str: ...

    @ml_function(params={"obj": Any, "attr": str}, returns=bool)
    def hasattr(self, obj: Any, attr: str) -> bool: ...

    @ml_function(params={"obj": Any, "attr": str}, returns=Any)
    def getattr(self, obj: Any, attr: str, default: Any = None): ...

    @ml_function(params={"obj": Any, "attr": str, "value": Any})
    def setattr(self, obj: Any, attr: str, value: Any) -> None: ...

    @ml_function(params={"func": Callable, "args": list}, returns=Any)
    def call(self, func: Callable, args: list): ...

    # Container Operations (1 function)
    @ml_function(params={"container": Any}, returns=int)
    def len(self, container: Any) -> int: ...

    # I/O (2 functions)
    @ml_function()
    def print(self, *args, **kwargs) -> None: ...

    @ml_function(params={"prompt": str}, returns=str)
    def input(self, prompt: str = "") -> str: ...

    # System (2 functions)
    @ml_function(params={"code": int})
    def exit(self, code: int = 0) -> None: ...

    @ml_function(returns=str)
    def version(self) -> str: ...
```

**Testing**:

*Python Tests* (`tests/unit/stdlib/test_builtin.py`):
```python
class TestBuiltinTypeConversion:
    def test_int_from_string(self): ...
    def test_int_from_float(self): ...
    def test_int_from_bool(self): ...
    def test_int_error_handling(self): ...
    # ... 20+ tests

class TestBuiltinTypeChecking:
    def test_type_number(self): ...
    def test_type_string(self): ...
    # ... 15+ tests

class TestBuiltinIntrospection:
    def test_dir_dict(self): ...
    def test_hasattr(self): ...
    def test_getattr(self): ...
    # ... 20+ tests
```

*ML Tests* (`tests/ml_integration/stdlib/test_builtin.ml`):
```ml
// Test type conversion
x = int("42");
assert(x == 42, "int conversion failed");

y = str(true);
assert(y == "true", "str conversion failed");

// Test type checking
t = type(42);
assert(t == "number", "type check failed");

// Test introspection
obj = {name: "John", age: 30};
keys = dir(obj);
assert(len(keys) == 2, "dir failed");

has_name = hasattr(obj, "name");
assert(has_name == true, "hasattr failed");

print("PASS: All builtin tests passed");
```

**Documentation** (`docs/api/builtin.md`):
- Function reference with signatures
- Usage examples for each function
- Type conversion semantics
- Introspection guide

**Effort**: 2 days (mostly testing, implementation exists)

---

### Module 1.2: math (Week 1, Days 3-4)

**Purpose**: Mathematical operations and constants

**Capabilities**: `["execute:calculations"]`

**Implementation**:

```python
@ml_module(
    name="math",
    capabilities=["execute:calculations"],
    description="Mathematical operations and constants",
    version="2.0.0"
)
class Math:
    """Mathematical operations with capability-based security."""

    # Constants (3)
    @ml_constant(description="Pi (π) ≈ 3.14159...")
    pi = 3.141592653589793

    @ml_constant(description="Euler's number (e) ≈ 2.71828...")
    e = 2.718281828459045

    @ml_constant(description="Tau (2π) ≈ 6.28318...")
    tau = 6.283185307179586

    # Basic Operations (8 functions)
    @ml_function(
        params={"x": float},
        returns=float,
        description="Square root of x",
        examples=["math.sqrt(16) // 4.0", "math.sqrt(2) // 1.414..."]
    )
    def sqrt(self, x: float) -> float: ...

    @ml_function(params={"x": float, "y": float}, returns=float)
    def pow(self, x: float, y: float) -> float: ...

    @ml_function(params={"x": float}, returns=float)
    def abs(self, x: float) -> float: ...

    @ml_function(params={"x": float}, returns=int)
    def floor(self, x: float) -> int: ...

    @ml_function(params={"x": float}, returns=int)
    def ceil(self, x: float) -> int: ...

    @ml_function(params={"x": float}, returns=int)
    def round(self, x: float) -> int: ...

    @ml_function(params={"a": float, "b": float}, returns=float)
    def min(self, a: float, b: float) -> float: ...

    @ml_function(params={"a": float, "b": float}, returns=float)
    def max(self, a: float, b: float) -> float: ...

    # Trigonometry (6 functions)
    @ml_function(params={"x": float}, returns=float, description="Sine of x (in radians)")
    def sin(self, x: float) -> float: ...

    @ml_function(params={"x": float}, returns=float, description="Cosine of x (in radians)")
    def cos(self, x: float) -> float: ...

    @ml_function(params={"x": float}, returns=float, description="Tangent of x (in radians)")
    def tan(self, x: float) -> float: ...

    @ml_function(params={"x": float}, returns=float, description="Arc sine (returns radians)")
    def asin(self, x: float) -> float: ...

    @ml_function(params={"x": float}, returns=float, description="Arc cosine (returns radians)")
    def acos(self, x: float) -> float: ...

    @ml_function(params={"x": float}, returns=float, description="Arc tangent (returns radians)")
    def atan(self, x: float) -> float: ...

    # Logarithms & Exponentials (4 functions)
    @ml_function(params={"x": float}, returns=float, description="Natural logarithm (base e)")
    def ln(self, x: float) -> float: ...

    @ml_function(params={"x": float, "base": float}, returns=float, description="Logarithm with base")
    def log(self, x: float, base: float = 10.0) -> float: ...

    @ml_function(params={"x": float}, returns=float, description="e^x")
    def exp(self, x: float) -> float: ...

    @ml_function(params={"x": float}, returns=float, description="2^x")
    def exp2(self, x: float) -> float: ...

    # Angle Conversion (2 functions)
    @ml_function(params={"degrees": float}, returns=float)
    def radians(self, degrees: float) -> float: ...

    @ml_function(params={"radians": float}, returns=float)
    def degrees(self, radians: float) -> float: ...

    # Advanced (4 functions)
    @ml_function(params={"x": float}, returns=float, description="Factorial (n!)")
    def factorial(self, x: int) -> int: ...

    @ml_function(params={"a": int, "b": int}, returns=int, description="Greatest common divisor")
    def gcd(self, a: int, b: int) -> int: ...

    @ml_function(params={"x": float}, returns=bool)
    def isnan(self, x: float) -> bool: ...

    @ml_function(params={"x": float}, returns=bool)
    def isinf(self, x: float) -> bool: ...
```

**Total Functions**: 27 functions, 3 constants

**Testing**:

*Python Tests* (60+ tests):
```python
class TestMathBasic:
    def test_sqrt(self): assert math.sqrt(16) == 4.0
    def test_sqrt_negative(self): assert math.sqrt(-1) == 0.0  # ML error handling
    def test_pow(self): assert math.pow(2, 3) == 8.0
    # ... 20 tests

class TestMathTrig:
    def test_sin_zero(self): assert math.sin(0) == 0.0
    def test_cos_zero(self): assert math.cos(0) == 1.0
    # ... 15 tests

class TestMathConstants:
    def test_pi(self): assert abs(math.pi - 3.14159) < 0.001
    # ... 5 tests
```

*ML Tests*:
```ml
import math;

// Test constants
assert(math.pi > 3.14 && math.pi < 3.15, "pi wrong");
assert(math.e > 2.71 && math.e < 2.72, "e wrong");

// Test basic operations
result = math.sqrt(16);
assert(result == 4.0, "sqrt failed");

pow_result = math.pow(2, 3);
assert(pow_result == 8.0, "pow failed");

// Test trigonometry
sin_zero = math.sin(0);
assert(sin_zero == 0.0, "sin failed");

// Test error handling
sqrt_neg = math.sqrt(-1);
assert(sqrt_neg == 0.0, "sqrt negative handling failed");

print("PASS: Math module tests passed");
```

**Documentation**:
- Complete function reference
- Mathematical concepts explained
- Error handling semantics
- Examples for each category

**Effort**: 2 days

---

### Module 1.3: string (Week 1, Days 5-6)

**Purpose**: String manipulation and utilities

**Capabilities**: `["execute:string_operations"]`

**Implementation**:

```python
@ml_module(
    name="string",
    capabilities=["execute:string_operations"],
    description="String manipulation utilities",
    version="2.0.0"
)
class String:
    """String manipulation with case conversion, searching, and formatting."""

    # Case Conversion (6 functions)
    @ml_function(params={"s": str}, returns=str)
    def upper(self, s: str) -> str:
        """Convert to uppercase."""
        return s.upper()

    @ml_function(params={"s": str}, returns=str)
    def lower(self, s: str) -> str:
        """Convert to lowercase."""
        return s.lower()

    @ml_function(params={"s": str}, returns=str)
    def capitalize(self, s: str) -> str:
        """Capitalize first letter."""
        return s.capitalize()

    @ml_function(params={"s": str}, returns=str)
    def title(self, s: str) -> str:
        """Title case (capitalize each word)."""
        return s.title()

    @ml_function(params={"s": str}, returns=str)
    def camel_case(self, s: str) -> str:
        """Convert to camelCase."""
        # Implementation: "hello_world" -> "helloWorld"
        ...

    @ml_function(params={"s": str}, returns=str)
    def snake_case(self, s: str) -> str:
        """Convert to snake_case."""
        # Implementation: "HelloWorld" -> "hello_world"
        ...

    # Search & Test (8 functions)
    @ml_function(params={"s": str, "substr": str}, returns=bool)
    def contains(self, s: str, substr: str) -> bool:
        """Check if string contains substring."""
        return substr in s

    @ml_function(params={"s": str, "prefix": str}, returns=bool)
    def starts_with(self, s: str, prefix: str) -> bool:
        """Check if string starts with prefix."""
        return s.startswith(prefix)

    @ml_function(params={"s": str, "suffix": str}, returns=bool)
    def ends_with(self, s: str, suffix: str) -> bool:
        """Check if string ends with suffix."""
        return s.endswith(suffix)

    @ml_function(params={"s": str, "substr": str}, returns=int)
    def index_of(self, s: str, substr: str) -> int:
        """Find first index of substring (-1 if not found)."""
        try:
            return s.index(substr)
        except ValueError:
            return -1

    @ml_function(params={"s": str, "substr": str}, returns=int)
    def last_index_of(self, s: str, substr: str) -> int:
        """Find last index of substring (-1 if not found)."""
        try:
            return s.rindex(substr)
        except ValueError:
            return -1

    @ml_function(params={"s": str, "substr": str}, returns=int)
    def count(self, s: str, substr: str) -> int:
        """Count occurrences of substring."""
        return s.count(substr)

    @ml_function(params={"s": str}, returns=bool)
    def is_alpha(self, s: str) -> bool:
        """Check if all characters are alphabetic."""
        return s.isalpha()

    @ml_function(params={"s": str}, returns=bool)
    def is_numeric(self, s: str) -> bool:
        """Check if all characters are numeric."""
        return s.isnumeric()

    # Manipulation (10 functions)
    @ml_function(params={"s": str, "old": str, "new": str}, returns=str)
    def replace(self, s: str, old: str, new: str) -> str:
        """Replace all occurrences of old with new."""
        return s.replace(old, new)

    @ml_function(params={"s": str, "sep": str}, returns=list)
    def split(self, s: str, sep: str = " ") -> list:
        """Split string by separator."""
        return s.split(sep)

    @ml_function(params={"parts": list, "sep": str}, returns=str)
    def join(self, parts: list, sep: str) -> str:
        """Join list of strings with separator."""
        return sep.join(str(p) for p in parts)

    @ml_function(params={"s": str}, returns=str)
    def trim(self, s: str) -> str:
        """Remove leading and trailing whitespace."""
        return s.strip()

    @ml_function(params={"s": str}, returns=str)
    def trim_start(self, s: str) -> str:
        """Remove leading whitespace."""
        return s.lstrip()

    @ml_function(params={"s": str}, returns=str)
    def trim_end(self, s: str) -> str:
        """Remove trailing whitespace."""
        return s.rstrip()

    @ml_function(params={"s": str}, returns=str)
    def reverse(self, s: str) -> str:
        """Reverse string."""
        return s[::-1]

    @ml_function(params={"s": str, "n": int}, returns=str)
    def repeat(self, s: str, n: int) -> str:
        """Repeat string n times."""
        return s * n

    @ml_function(params={"s": str, "width": int, "char": str}, returns=str)
    def pad_start(self, s: str, width: int, char: str = " ") -> str:
        """Pad string to width with char at start."""
        return s.rjust(width, char)

    @ml_function(params={"s": str, "width": int, "char": str}, returns=str)
    def pad_end(self, s: str, width: int, char: str = " ") -> str:
        """Pad string to width with char at end."""
        return s.ljust(width, char)

    # Slicing (2 functions)
    @ml_function(params={"s": str, "start": int, "end": int}, returns=str)
    def substring(self, s: str, start: int, end: int = None) -> str:
        """Get substring from start to end."""
        if end is None:
            return s[start:]
        return s[start:end]

    @ml_function(params={"s": str, "index": int}, returns=str)
    def char_at(self, s: str, index: int) -> str:
        """Get character at index."""
        if 0 <= index < len(s):
            return s[index]
        return ""
```

**Total Functions**: 26 functions

**Testing**: 80+ tests (Python + ML)

**Effort**: 2 days

---

### Module 1.4: array (Week 2, Days 1-2)

**Purpose**: Array/List manipulation utilities

**Capabilities**: `["execute:array_operations"]`

**Implementation**:

```python
@ml_module(
    name="array",
    capabilities=["execute:array_operations"],
    description="Array and list manipulation utilities",
    version="2.0.0"
)
class Array:
    """Array manipulation with functional programming support."""

    # Creation (4 functions)
    @ml_function(params={"size": int, "value": Any}, returns=list)
    def create(self, size: int, value: Any = None) -> list:
        """Create array of size filled with value."""
        return [value] * size

    @ml_function(params={"start": int, "end": int, "step": int}, returns=list)
    def range(self, start: int, end: int = None, step: int = 1) -> list:
        """Create array of numbers in range."""
        if end is None:
            end = start
            start = 0
        return list(range(start, end, step))

    @ml_function(params={"arr": list, "n": int}, returns=list)
    def repeat(self, arr: list, n: int) -> list:
        """Repeat array n times."""
        return arr * n

    @ml_function(params={"arr": list}, returns=list)
    def copy(self, arr: list) -> list:
        """Create shallow copy of array."""
        return arr.copy()

    # Access & Modification (8 functions)
    @ml_function(params={"arr": list, "item": Any})
    def push(self, arr: list, item: Any) -> None:
        """Add item to end of array (mutating)."""
        arr.append(item)

    @ml_function(params={"arr": list}, returns=Any)
    def pop(self, arr: list):
        """Remove and return last item."""
        return arr.pop() if arr else None

    @ml_function(params={"arr": list, "item": Any})
    def unshift(self, arr: list, item: Any) -> None:
        """Add item to start of array (mutating)."""
        arr.insert(0, item)

    @ml_function(params={"arr": list}, returns=Any)
    def shift(self, arr: list):
        """Remove and return first item."""
        return arr.pop(0) if arr else None

    @ml_function(params={"arr": list, "index": int}, returns=Any)
    def get(self, arr: list, index: int, default: Any = None):
        """Get item at index (safe with default)."""
        return arr[index] if 0 <= index < len(arr) else default

    @ml_function(params={"arr": list, "index": int, "value": Any})
    def set(self, arr: list, index: int, value: Any) -> None:
        """Set item at index."""
        if 0 <= index < len(arr):
            arr[index] = value

    @ml_function(params={"arr": list, "index": int})
    def remove_at(self, arr: list, index: int):
        """Remove item at index and return it."""
        if 0 <= index < len(arr):
            return arr.pop(index)
        return None

    @ml_function(params={"arr": list, "item": Any}, returns=bool)
    def remove(self, arr: list, item: Any) -> bool:
        """Remove first occurrence of item. Returns true if found."""
        try:
            arr.remove(item)
            return True
        except ValueError:
            return False

    # Search (5 functions)
    @ml_function(params={"arr": list, "item": Any}, returns=bool)
    def contains(self, arr: list, item: Any) -> bool:
        """Check if array contains item."""
        return item in arr

    @ml_function(params={"arr": list, "item": Any}, returns=int)
    def index_of(self, arr: list, item: Any) -> int:
        """Find index of item (-1 if not found)."""
        try:
            return arr.index(item)
        except ValueError:
            return -1

    @ml_function(params={"arr": list, "item": Any}, returns=int)
    def last_index_of(self, arr: list, item: Any) -> int:
        """Find last index of item (-1 if not found)."""
        for i in range(len(arr) - 1, -1, -1):
            if arr[i] == item:
                return i
        return -1

    @ml_function(params={"arr": list, "item": Any}, returns=int)
    def count(self, arr: list, item: Any) -> int:
        """Count occurrences of item."""
        return arr.count(item)

    @ml_function(params={"arr": list, "predicate": Callable})
    def find(self, arr: list, predicate: Callable):
        """Find first item matching predicate."""
        for item in arr:
            if predicate(item):
                return item
        return None

    # Transformation (10 functions)
    @ml_function(params={"arr": list, "func": Callable}, returns=list)
    def map(self, arr: list, func: Callable) -> list:
        """Apply function to each element."""
        return [func(item) for item in arr]

    @ml_function(params={"arr": list, "predicate": Callable}, returns=list)
    def filter(self, arr: list, predicate: Callable) -> list:
        """Filter array by predicate."""
        return [item for item in arr if predicate(item)]

    @ml_function(params={"arr": list, "func": Callable, "initial": Any}, returns=Any)
    def reduce(self, arr: list, func: Callable, initial: Any = None):
        """Reduce array to single value."""
        from functools import reduce
        if initial is None:
            return reduce(func, arr)
        return reduce(func, arr, initial)

    @ml_function(params={"arr": list}, returns=list)
    def reverse(self, arr: list) -> list:
        """Return reversed array (non-mutating)."""
        return arr[::-1]

    @ml_function(params={"arr": list})
    def sort(self, arr: list) -> None:
        """Sort array in place."""
        arr.sort()

    @ml_function(params={"arr": list, "key": Callable}, returns=list)
    def sorted(self, arr: list, key: Callable = None) -> list:
        """Return sorted array (non-mutating)."""
        return sorted(arr, key=key)

    @ml_function(params={"arr": list}, returns=list)
    def unique(self, arr: list) -> list:
        """Remove duplicates (preserves order)."""
        seen = set()
        result = []
        for item in arr:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result

    @ml_function(params={"arr": list}, returns=list)
    def flatten(self, arr: list) -> list:
        """Flatten one level of nesting."""
        result = []
        for item in arr:
            if isinstance(item, list):
                result.extend(item)
            else:
                result.append(item)
        return result

    @ml_function(params={"arr": list, "size": int}, returns=list)
    def chunk(self, arr: list, size: int) -> list:
        """Split array into chunks of size."""
        return [arr[i:i+size] for i in range(0, len(arr), size)]

    @ml_function(params={"arr": list, "n": int}, returns=list)
    def take(self, arr: list, n: int) -> list:
        """Take first n elements."""
        return arr[:n]

    # Aggregation (6 functions)
    @ml_function(params={"arr": list}, returns=Any)
    def first(self, arr: list):
        """Get first element."""
        return arr[0] if arr else None

    @ml_function(params={"arr": list}, returns=Any)
    def last(self, arr: list):
        """Get last element."""
        return arr[-1] if arr else None

    @ml_function(params={"arr": list}, returns=float)
    def sum(self, arr: list) -> float:
        """Sum of all numbers in array."""
        return sum(arr)

    @ml_function(params={"arr": list}, returns=float)
    def avg(self, arr: list) -> float:
        """Average of all numbers."""
        return sum(arr) / len(arr) if arr else 0.0

    @ml_function(params={"arr": list}, returns=Any)
    def min(self, arr: list):
        """Minimum value."""
        return min(arr) if arr else None

    @ml_function(params={"arr": list}, returns=Any)
    def max(self, arr: list):
        """Maximum value."""
        return max(arr) if arr else None
```

**Total Functions**: 33 functions

**Testing**: 100+ tests

**Effort**: 2 days

---

### Module 1.5: console (Week 2, Days 3-4)

**Purpose**: Console I/O (enhanced version of print/input from builtin)

**Capabilities**: `["io:console"]`

**Implementation**:

```python
@ml_module(
    name="console",
    capabilities=["io:console"],
    description="Console input/output operations",
    version="2.0.0"
)
class Console:
    """Console I/O with formatting and colors."""

    # Output (6 functions)
    @ml_function()
    def log(self, *args) -> None:
        """Print to console (alias for print)."""
        print(*args)

    @ml_function()
    def info(self, *args) -> None:
        """Print info message (with [INFO] prefix)."""
        print("[INFO]", *args)

    @ml_function()
    def warn(self, *args) -> None:
        """Print warning message (with [WARN] prefix)."""
        print("[WARN]", *args)

    @ml_function()
    def error(self, *args) -> None:
        """Print error message (with [ERROR] prefix)."""
        print("[ERROR]", *args)

    @ml_function()
    def debug(self, *args) -> None:
        """Print debug message (with [DEBUG] prefix)."""
        print("[DEBUG]", *args)

    @ml_function()
    def clear(self) -> None:
        """Clear console screen."""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')

    # Input (3 functions)
    @ml_function(params={"prompt": str}, returns=str)
    def read_line(self, prompt: str = "") -> str:
        """Read line of input."""
        return input(prompt)

    @ml_function(params={"prompt": str}, returns=int)
    def read_int(self, prompt: str = "") -> int:
        """Read integer from input."""
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Please enter a valid integer.")

    @ml_function(params={"prompt": str}, returns=float)
    def read_float(self, prompt: str = "") -> float:
        """Read float from input."""
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("Please enter a valid number.")

    # Formatting (4 functions)
    @ml_function(params={"obj": Any})
    def inspect(self, obj: Any) -> None:
        """Pretty-print object (like console.log in JS)."""
        import pprint
        pprint.pprint(obj)

    @ml_function(params={"data": dict})
    def table(self, data: list[dict]) -> None:
        """Print data as table."""
        # Implementation: Format list of dicts as ASCII table
        ...

    @ml_function(params={"label": str})
    def time(self, label: str = "default") -> None:
        """Start timer with label."""
        # Implementation: Store start time
        ...

    @ml_function(params={"label": str})
    def time_end(self, label: str = "default") -> None:
        """End timer and print elapsed time."""
        # Implementation: Calculate and print duration
        ...
```

**Total Functions**: 13 functions

**Testing**: 40+ tests

**Effort**: 2 days

---

## Tier 2 Implementation (Weeks 3-4)

### Module 2.1: json (Week 3, Days 1-2)

**Purpose**: JSON encoding/decoding

**Capabilities**: `["data:json"]`

**Implementation**:

```python
@ml_module(
    name="json",
    capabilities=["data:json"],
    description="JSON encoding and decoding",
    version="2.0.0"
)
class JSON:
    """JSON data format support."""

    @ml_function(params={"obj": Any}, returns=str)
    def stringify(self, obj: Any, indent: int = None) -> str:
        """Convert ML object to JSON string."""
        import json
        return json.dumps(obj, indent=indent)

    @ml_function(params={"text": str}, returns=Any)
    def parse(self, text: str):
        """Parse JSON string to ML object."""
        import json
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")

    @ml_function(params={"text": str}, returns=bool)
    def is_valid(self, text: str) -> bool:
        """Check if string is valid JSON."""
        import json
        try:
            json.loads(text)
            return True
        except json.JSONDecodeError:
            return False

    @ml_function(params={"obj": Any}, returns=str)
    def pretty(self, obj: Any) -> str:
        """Pretty-print JSON with indentation."""
        import json
        return json.dumps(obj, indent=2, sort_keys=True)
```

**Total Functions**: 4 functions

**Testing**: 25+ tests

**Effort**: 2 days

---

### Module 2.2: datetime (Week 3, Days 3-5)

**Purpose**: Date and time operations

**Capabilities**: `["time:operations", "time:system"]`

**Implementation**:

```python
@ml_module(
    name="datetime",
    capabilities=["time:operations", "time:system"],
    description="Date and time operations",
    version="2.0.0"
)
class DateTime:
    """Date and time manipulation."""

    # Creation (5 functions)
    @ml_function(returns=Any)
    def now(self):
        """Get current date and time."""
        from datetime import datetime
        return datetime.now()

    @ml_function(params={"year": int, "month": int, "day": int}, returns=Any)
    def create(self, year: int, month: int, day: int,
              hour: int = 0, minute: int = 0, second: int = 0):
        """Create datetime object."""
        from datetime import datetime
        return datetime(year, month, day, hour, minute, second)

    @ml_function(params={"timestamp": float}, returns=Any)
    def from_timestamp(self, timestamp: float):
        """Create datetime from Unix timestamp."""
        from datetime import datetime
        return datetime.fromtimestamp(timestamp)

    @ml_function(params={"text": str, "format": str}, returns=Any)
    def parse(self, text: str, format: str = "%Y-%m-%d"):
        """Parse datetime from string."""
        from datetime import datetime
        return datetime.strptime(text, format)

    @ml_function(params={"dt": Any, "format": str}, returns=str)
    def format(self, dt, format: str = "%Y-%m-%d %H:%M:%S") -> str:
        """Format datetime as string."""
        return dt.strftime(format)

    # Arithmetic (6 functions)
    @ml_function(params={"dt": Any, "days": int}, returns=Any)
    def add_days(self, dt, days: int):
        """Add days to datetime."""
        from datetime import timedelta
        return dt + timedelta(days=days)

    @ml_function(params={"dt": Any, "hours": int}, returns=Any)
    def add_hours(self, dt, hours: int):
        """Add hours to datetime."""
        from datetime import timedelta
        return dt + timedelta(hours=hours)

    @ml_function(params={"dt": Any, "minutes": int}, returns=Any)
    def add_minutes(self, dt, minutes: int):
        """Add minutes to datetime."""
        from datetime import timedelta
        return dt + timedelta(minutes=minutes)

    @ml_function(params={"dt1": Any, "dt2": Any}, returns=float)
    def diff_days(self, dt1, dt2) -> float:
        """Difference in days between two datetimes."""
        delta = dt1 - dt2
        return delta.total_seconds() / 86400

    @ml_function(params={"dt1": Any, "dt2": Any}, returns=float)
    def diff_hours(self, dt1, dt2) -> float:
        """Difference in hours."""
        delta = dt1 - dt2
        return delta.total_seconds() / 3600

    @ml_function(params={"dt1": Any, "dt2": Any}, returns=float)
    def diff_seconds(self, dt1, dt2) -> float:
        """Difference in seconds."""
        delta = dt1 - dt2
        return delta.total_seconds()

    # Properties (8 functions)
    @ml_function(params={"dt": Any}, returns=int)
    def year(self, dt) -> int:
        """Get year."""
        return dt.year

    @ml_function(params={"dt": Any}, returns=int)
    def month(self, dt) -> int:
        """Get month (1-12)."""
        return dt.month

    @ml_function(params={"dt": Any}, returns=int)
    def day(self, dt) -> int:
        """Get day of month."""
        return dt.day

    @ml_function(params={"dt": Any}, returns=int)
    def hour(self, dt) -> int:
        """Get hour (0-23)."""
        return dt.hour

    @ml_function(params={"dt": Any}, returns=int)
    def minute(self, dt) -> int:
        """Get minute (0-59)."""
        return dt.minute

    @ml_function(params={"dt": Any}, returns=int)
    def second(self, dt) -> int:
        """Get second (0-59)."""
        return dt.second

    @ml_function(params={"dt": Any}, returns=int)
    def weekday(self, dt) -> int:
        """Get day of week (0=Monday, 6=Sunday)."""
        return dt.weekday()

    @ml_function(params={"dt": Any}, returns=float)
    def timestamp(self, dt) -> float:
        """Get Unix timestamp."""
        return dt.timestamp()
```

**Total Functions**: 19 functions

**Testing**: 60+ tests

**Effort**: 3 days

---

### Module 2.3: regex (Week 4, Days 1-2)

**Purpose**: Regular expression pattern matching

**Capabilities**: `["regex:operations"]`

**Implementation**:

```python
@ml_module(
    name="regex",
    capabilities=["regex:operations"],
    description="Regular expression pattern matching",
    version="2.0.0"
)
class Regex:
    """Regular expression operations."""

    @ml_function(params={"pattern": str, "text": str}, returns=bool)
    def test(self, pattern: str, text: str) -> bool:
        """Test if pattern matches text."""
        import re
        return bool(re.search(pattern, text))

    @ml_function(params={"pattern": str, "text": str}, returns=str)
    def match(self, pattern: str, text: str):
        """Get first match or None."""
        import re
        m = re.search(pattern, text)
        return m.group(0) if m else None

    @ml_function(params={"pattern": str, "text": str}, returns=list)
    def find_all(self, pattern: str, text: str) -> list:
        """Find all matches."""
        import re
        return re.findall(pattern, text)

    @ml_function(params={"pattern": str, "replacement": str, "text": str}, returns=str)
    def replace(self, pattern: str, replacement: str, text: str) -> str:
        """Replace all matches."""
        import re
        return re.sub(pattern, replacement, text)

    @ml_function(params={"pattern": str, "text": str}, returns=list)
    def split(self, pattern: str, text: str) -> list:
        """Split text by pattern."""
        import re
        return re.split(pattern, text)

    @ml_function(params={"pattern": str}, returns=bool)
    def is_valid(self, pattern: str) -> bool:
        """Check if pattern is valid regex."""
        import re
        try:
            re.compile(pattern)
            return True
        except re.error:
            return False

    @ml_function(params={"text": str}, returns=str)
    def escape(self, text: str) -> str:
        """Escape special regex characters."""
        import re
        return re.escape(text)
```

**Total Functions**: 7 functions

**Testing**: 40+ tests

**Effort**: 2 days

---

### Module 2.4: random (Week 4, Days 3-4)

**Purpose**: Random number generation

**Capabilities**: `["random:operations", "random:entropy"]`

**Implementation**:

```python
@ml_module(
    name="random",
    capabilities=["random:operations", "random:entropy"],
    description="Random number generation",
    version="2.0.0"
)
class Random:
    """Random number generation and utilities."""

    # Basic (5 functions)
    @ml_function(returns=float)
    def random(self) -> float:
        """Random float between 0 and 1."""
        import random
        return random.random()

    @ml_function(params={"min": int, "max": int}, returns=int)
    def int(self, min: int, max: int) -> int:
        """Random integer between min and max (inclusive)."""
        import random
        return random.randint(min, max)

    @ml_function(params={"min": float, "max": float}, returns=float)
    def float(self, min: float, max: float) -> float:
        """Random float between min and max."""
        import random
        return random.uniform(min, max)

    @ml_function(returns=bool)
    def bool(self) -> bool:
        """Random boolean."""
        import random
        return random.choice([True, False])

    @ml_function(params={"seed": int})
    def set_seed(self, seed: int) -> None:
        """Set random seed for reproducibility."""
        import random
        random.seed(seed)

    # Array Operations (3 functions)
    @ml_function(params={"arr": list}, returns=Any)
    def choice(self, arr: list):
        """Pick random element from array."""
        import random
        return random.choice(arr) if arr else None

    @ml_function(params={"arr": list})
    def shuffle(self, arr: list) -> None:
        """Shuffle array in place."""
        import random
        random.shuffle(arr)

    @ml_function(params={"arr": list, "k": int}, returns=list)
    def sample(self, arr: list, k: int) -> list:
        """Pick k random elements (no replacement)."""
        import random
        return random.sample(arr, min(k, len(arr)))

    # Distributions (3 functions)
    @ml_function(params={"mean": float, "stddev": float}, returns=float)
    def gaussian(self, mean: float = 0.0, stddev: float = 1.0) -> float:
        """Random number from Gaussian distribution."""
        import random
        return random.gauss(mean, stddev)

    @ml_function(params={"size": int}, returns=list)
    def bytes(self, size: int) -> list:
        """Generate random bytes."""
        import random
        return [random.randint(0, 255) for _ in range(size)]

    @ml_function(params={"length": int, "chars": str}, returns=str)
    def string(self, length: int, chars: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") -> str:
        """Generate random string."""
        import random
        return ''.join(random.choice(chars) for _ in range(length))
```

**Total Functions**: 11 functions

**Testing**: 35+ tests

**Effort**: 2 days

---

### Module 2.5: functional (Week 4, Day 5 - Week 5, Day 1)

**Purpose**: Functional programming utilities

**Capabilities**: `["functional:operations"]`

**Implementation**: (Abbreviated - full spec too long)

```python
@ml_module(
    name="functional",
    capabilities=["functional:operations"],
    description="Functional programming utilities",
    version="2.0.0"
)
class Functional:
    """Functional programming tools."""

    # Core functional operations (already in array module, but pure versions here)
    @ml_function
    def map(self, func: Callable, arr: list) -> list: ...

    @ml_function
    def filter(self, predicate: Callable, arr: list) -> list: ...

    @ml_function
    def reduce(self, func: Callable, arr: list, initial: Any = None): ...

    # Function composition
    @ml_function
    def compose(self, *funcs: Callable) -> Callable: ...

    @ml_function
    def pipe(self, *funcs: Callable) -> Callable: ...

    @ml_function
    def curry(self, func: Callable) -> Callable: ...

    @ml_function
    def partial(self, func: Callable, *args) -> Callable: ...

    # Utility
    @ml_function
    def identity(self, x: Any) -> Any: ...

    @ml_function
    def constant(self, value: Any) -> Callable: ...

    # ... 20+ more functional utilities
```

**Total Functions**: 25 functions

**Testing**: 80+ tests

**Effort**: 2 days

---

## Tier 3 Implementation (Weeks 5-6)

### Module 3.1: file (Week 5, Days 2-4)

**Purpose**: File system operations

**Capabilities**: `["file:read", "file:write", "file:delete", "file:metadata"]`

**Security**: HIGH - Requires careful capability integration

**Implementation**:

```python
@ml_module(
    name="file",
    capabilities=["file:read", "file:write", "file:delete", "file:metadata"],
    description="File system operations with capability-based security",
    version="2.0.0"
)
class File:
    """Secure file system operations."""

    # Reading (5 functions)
    @ml_function(
        params={"path": str},
        returns=str,
        capabilities=["file:read"]
    )
    @requires_capability("file:read")
    def read_text(self, path: str, encoding: str = "utf-8") -> str:
        """Read file as text."""
        # Capability check happens in decorator
        with open(path, 'r', encoding=encoding) as f:
            return f.read()

    @ml_function(capabilities=["file:read"])
    @requires_capability("file:read")
    def read_lines(self, path: str, encoding: str = "utf-8") -> list:
        """Read file as list of lines."""
        with open(path, 'r', encoding=encoding) as f:
            return f.readlines()

    @ml_function(capabilities=["file:read"])
    @requires_capability("file:read")
    def read_bytes(self, path: str) -> bytes:
        """Read file as bytes."""
        with open(path, 'rb') as f:
            return f.read()

    @ml_function(capabilities=["file:read"])
    @requires_capability("file:read")
    def read_json(self, path: str):
        """Read and parse JSON file."""
        import json
        with open(path, 'r') as f:
            return json.load(f)

    @ml_function(capabilities=["file:read"])
    @requires_capability("file:read")
    def exists(self, path: str) -> bool:
        """Check if file exists."""
        import os
        return os.path.exists(path)

    # Writing (5 functions)
    @ml_function(capabilities=["file:write"])
    @requires_capability("file:write")
    def write_text(self, path: str, content: str, encoding: str = "utf-8") -> None:
        """Write text to file."""
        with open(path, 'w', encoding=encoding) as f:
            f.write(content)

    @ml_function(capabilities=["file:write"])
    @requires_capability("file:write")
    def write_lines(self, path: str, lines: list, encoding: str = "utf-8") -> None:
        """Write lines to file."""
        with open(path, 'w', encoding=encoding) as f:
            f.writelines(lines)

    @ml_function(capabilities=["file:write"])
    @requires_capability("file:write")
    def write_bytes(self, path: str, data: bytes) -> None:
        """Write bytes to file."""
        with open(path, 'wb') as f:
            f.write(data)

    @ml_function(capabilities=["file:write"])
    @requires_capability("file:write")
    def write_json(self, path: str, obj: Any, indent: int = 2) -> None:
        """Write object as JSON to file."""
        import json
        with open(path, 'w') as f:
            json.dump(obj, f, indent=indent)

    @ml_function(capabilities=["file:write"])
    @requires_capability("file:write")
    def append_text(self, path: str, content: str, encoding: str = "utf-8") -> None:
        """Append text to file."""
        with open(path, 'a', encoding=encoding) as f:
            f.write(content)

    # Directory Operations (6 functions)
    @ml_function(capabilities=["file:metadata"])
    @requires_capability("file:metadata")
    def list_dir(self, path: str = ".") -> list:
        """List directory contents."""
        import os
        return os.listdir(path)

    @ml_function(capabilities=["file:write"])
    @requires_capability("file:write")
    def make_dir(self, path: str) -> None:
        """Create directory."""
        import os
        os.makedirs(path, exist_ok=True)

    @ml_function(capabilities=["file:delete"])
    @requires_capability("file:delete")
    def remove(self, path: str) -> None:
        """Remove file."""
        import os
        os.remove(path)

    @ml_function(capabilities=["file:delete"])
    @requires_capability("file:delete")
    def remove_dir(self, path: str) -> None:
        """Remove directory."""
        import shutil
        shutil.rmtree(path)

    @ml_function(capabilities=["file:metadata"])
    @requires_capability("file:metadata")
    def is_file(self, path: str) -> bool:
        """Check if path is a file."""
        import os
        return os.path.isfile(path)

    @ml_function(capabilities=["file:metadata"])
    @requires_capability("file:metadata")
    def is_dir(self, path: str) -> bool:
        """Check if path is a directory."""
        import os
        return os.path.isdir(path)

    # Metadata (4 functions)
    @ml_function(capabilities=["file:metadata"])
    @requires_capability("file:metadata")
    def size(self, path: str) -> int:
        """Get file size in bytes."""
        import os
        return os.path.getsize(path)

    @ml_function(capabilities=["file:metadata"])
    @requires_capability("file:metadata")
    def modified_time(self, path: str) -> float:
        """Get last modified time (timestamp)."""
        import os
        return os.path.getmtime(path)

    @ml_function(capabilities=["file:metadata"])
    @requires_capability("file:metadata")
    def get_extension(self, path: str) -> str:
        """Get file extension."""
        import os
        return os.path.splitext(path)[1]

    @ml_function(capabilities=["file:metadata"])
    @requires_capability("file:metadata")
    def get_filename(self, path: str) -> str:
        """Get filename without path."""
        import os
        return os.path.basename(path)
```

**Total Functions**: 20 functions

**Testing**: 70+ tests (including security tests)

**Special Testing**: Capability enforcement tests crucial

**Effort**: 3 days (extra time for security)

---

### Module 3.2: crypto (Week 5, Day 5 - Week 6, Day 1)

**Purpose**: Cryptographic operations (hashing, encoding)

**Capabilities**: `["crypto:hash", "crypto:random"]`

**Implementation**:

```python
@ml_module(
    name="crypto",
    capabilities=["crypto:hash", "crypto:random"],
    description="Cryptographic operations",
    version="2.0.0"
)
class Crypto:
    """Cryptographic utilities (hashing, encoding)."""

    # Hashing (6 functions)
    @ml_function(params={"text": str}, returns=str, capabilities=["crypto:hash"])
    def md5(self, text: str) -> str:
        """MD5 hash (weak, use for non-security purposes)."""
        import hashlib
        return hashlib.md5(text.encode()).hexdigest()

    @ml_function(params={"text": str}, returns=str, capabilities=["crypto:hash"])
    def sha1(self, text: str) -> str:
        """SHA-1 hash."""
        import hashlib
        return hashlib.sha1(text.encode()).hexdigest()

    @ml_function(params={"text": str}, returns=str, capabilities=["crypto:hash"])
    def sha256(self, text: str) -> str:
        """SHA-256 hash."""
        import hashlib
        return hashlib.sha256(text.encode()).hexdigest()

    @ml_function(params={"text": str}, returns=str, capabilities=["crypto:hash"])
    def sha512(self, text: str) -> str:
        """SHA-512 hash."""
        import hashlib
        return hashlib.sha512(text.encode()).hexdigest()

    # Encoding (4 functions)
    @ml_function(params={"text": str}, returns=str)
    def base64_encode(self, text: str) -> str:
        """Encode to base64."""
        import base64
        return base64.b64encode(text.encode()).decode()

    @ml_function(params={"text": str}, returns=str)
    def base64_decode(self, text: str) -> str:
        """Decode from base64."""
        import base64
        return base64.b64decode(text.encode()).decode()

    @ml_function(params={"text": str}, returns=str)
    def url_encode(self, text: str) -> str:
        """URL encode."""
        from urllib.parse import quote
        return quote(text)

    @ml_function(params={"text": str}, returns=str)
    def url_decode(self, text: str) -> str:
        """URL decode."""
        from urllib.parse import unquote
        return unquote(text)

    # Random (3 functions)
    @ml_function(params={"length": int}, returns=str, capabilities=["crypto:random"])
    def random_hex(self, length: int) -> str:
        """Generate random hex string."""
        import secrets
        return secrets.token_hex(length // 2)

    @ml_function(params={"length": int}, returns=str, capabilities=["crypto:random"])
    def random_bytes(self, length: int) -> bytes:
        """Generate cryptographically secure random bytes."""
        import secrets
        return secrets.token_bytes(length)

    @ml_function(returns=str, capabilities=["crypto:random"])
    def uuid(self) -> str:
        """Generate UUID v4."""
        import uuid
        return str(uuid.uuid4())
```

**Total Functions**: 13 functions

**Testing**: 45+ tests

**Effort**: 2 days

---

### Module 3.3: collections (Week 6, Days 2-3)

**Purpose**: Advanced data structures (Set, OrderedDict, etc.)

**Implementation**: (Abbreviated)

```python
@ml_module(
    name="collections",
    capabilities=["collections:advanced"],
    description="Advanced collection data structures",
    version="2.0.0"
)
class Collections:
    """Advanced data structures."""

    # Set operations (10 functions)
    @ml_function
    def set_create(self, items: list = None): ...

    @ml_function
    def set_add(self, s: set, item: Any): ...

    @ml_function
    def set_union(self, s1: set, s2: set): ...

    @ml_function
    def set_intersection(self, s1: set, s2: set): ...

    # ... more set operations

    # Counter operations (5 functions)
    @ml_function
    def counter_create(self, items: list): ...

    @ml_function
    def counter_most_common(self, counter, n: int = None): ...

    # ... more counter operations

    # OrderedDict, defaultdict, etc.
```

**Total Functions**: 20 functions

**Testing**: 60+ tests

**Effort**: 2 days

---

## Tier 4 Implementation (Weeks 7-8)

### Module 4.1: http (Week 7, Days 1-3)

**Purpose**: HTTP client operations

**Capabilities**: `["network:http", "network:connect"]`

**Security**: HIGH - Network access requires strict capability control

**Implementation**:

```python
@ml_module(
    name="http",
    capabilities=["network:http", "network:connect"],
    description="HTTP client operations",
    version="2.0.0"
)
class HTTP:
    """HTTP client with capability-based security."""

    @ml_function(
        params={"url": str},
        returns=dict,
        capabilities=["network:http", "network:connect"]
    )
    @requires_capability("network:http")
    def get(self, url: str, headers: dict = None, timeout: int = 30) -> dict:
        """HTTP GET request."""
        import requests
        response = requests.get(url, headers=headers, timeout=timeout)
        return {
            "status": response.status_code,
            "headers": dict(response.headers),
            "body": response.text,
            "ok": response.ok
        }

    @ml_function(capabilities=["network:http"])
    @requires_capability("network:http")
    def post(self, url: str, data: Any = None, headers: dict = None, timeout: int = 30) -> dict:
        """HTTP POST request."""
        import requests
        response = requests.post(url, json=data, headers=headers, timeout=timeout)
        return {
            "status": response.status_code,
            "headers": dict(response.headers),
            "body": response.text,
            "ok": response.ok
        }

    # ... PUT, DELETE, PATCH, HEAD methods (6 more functions)

    @ml_function(capabilities=["network:http"])
    @requires_capability("network:http")
    def download(self, url: str, path: str) -> None:
        """Download file from URL."""
        # Requires both network:http AND file:write capabilities!
        ...
```

**Total Functions**: 10 functions

**Testing**: 50+ tests (including mock server tests)

**Effort**: 3 days

---

### Module 4.2: sqlite (Week 7, Day 4 - Week 8, Day 2)

**Purpose**: SQLite database operations

**Capabilities**: `["db:sqlite:read", "db:sqlite:write", "db:sqlite:create"]`

**Security**: HIGH - SQL injection prevention critical

**Implementation**:

```python
@ml_module(
    name="sqlite",
    capabilities=["db:sqlite:read", "db:sqlite:write", "db:sqlite:create"],
    description="SQLite database operations",
    version="2.0.0"
)
class SQLite:
    """SQLite database with parameterized queries."""

    @ml_function(
        params={"path": str},
        returns=Any,
        capabilities=["db:sqlite:create"]
    )
    @requires_capability("db:sqlite:create")
    def connect(self, path: str):
        """Connect to SQLite database."""
        import sqlite3
        return sqlite3.connect(path)

    @ml_function(capabilities=["db:sqlite:read"])
    @requires_capability("db:sqlite:read")
    def query(self, conn, sql: str, params: list = None) -> list:
        """Execute SELECT query (parameterized)."""
        cursor = conn.cursor()
        if params:
            cursor.execute(sql, params)  # Parameterized - safe!
        else:
            cursor.execute(sql)
        return cursor.fetchall()

    @ml_function(capabilities=["db:sqlite:write"])
    @requires_capability("db:sqlite:write")
    def execute(self, conn, sql: str, params: list = None) -> int:
        """Execute INSERT/UPDATE/DELETE (parameterized)."""
        cursor = conn.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        conn.commit()
        return cursor.rowcount

    # ... More database operations (12 functions total)
```

**Total Functions**: 12 functions

**Testing**: 60+ tests (including SQL injection prevention tests)

**Effort**: 3 days

---

## Implementation Schedule

### Week-by-Week Timeline

**Week 1**: Tier 1 Foundation (Part 1)
- Mon-Tue: builtin (testing, already designed)
- Wed-Thu: math (27 functions)
- Fri: string (start, 26 functions)

**Week 2**: Tier 1 Foundation (Part 2)
- Mon: string (finish)
- Tue-Wed: array (33 functions)
- Thu-Fri: console (13 functions)

**Week 3**: Tier 2 Data & Utilities (Part 1)
- Mon-Tue: json (4 functions)
- Wed-Fri: datetime (19 functions)

**Week 4**: Tier 2 Data & Utilities (Part 2)
- Mon-Tue: regex (7 functions)
- Wed-Thu: random (11 functions)
- Fri: functional (start, 25 functions)

**Week 5**: Tier 2 Finish + Tier 3 Start
- Mon: functional (finish)
- Tue-Thu: file (20 functions, HIGH SECURITY)
- Fri: crypto (start, 13 functions)

**Week 6**: Tier 3 Advanced
- Mon: crypto (finish)
- Tue-Wed: collections (20 functions)
- Thu-Fri: Buffer/catch-up

**Week 7**: Tier 4 Specialized
- Mon-Wed: http (10 functions, HIGH SECURITY)
- Thu-Fri: sqlite (start, 12 functions)

**Week 8**: Tier 4 Finish + Polish
- Mon-Tue: sqlite (finish)
- Wed-Thu: Integration testing, bug fixes
- Fri: Documentation completion, review

---

## Testing Strategy

### Python Unit Tests

For each module, create `tests/unit/stdlib/test_{module}.py`:

**Structure**:
```python
"""Unit tests for {module} stdlib module."""

import pytest
from mlpy.stdlib.{module} import {Module}
from mlpy.stdlib.decorators import get_module_metadata


class Test{Module}Registration:
    """Test module registration."""

    def test_module_registered(self):
        meta = get_module_metadata("{module}")
        assert meta is not None
        assert meta.name == "{module}"

    def test_capabilities_defined(self):
        meta = get_module_metadata("{module}")
        assert len(meta.capabilities) > 0


class Test{Module}Functions:
    """Test module functions."""

    def test_function_name(self):
        # Test each function
        ...

    def test_edge_cases(self):
        # Error handling, boundary conditions
        ...

    def test_metadata(self):
        # Check function metadata
        ...


class Test{Module}CapabilityEnforcement:
    """Test capability checks (for Tier 3+ modules)."""

    def test_requires_capability(self):
        # Test that function checks capabilities
        ...

    def test_without_capability_raises_error(self):
        # Test capability denial
        ...
```

**Coverage Target**: 95%+ per module

---

### ML Integration Tests

For each module, create `tests/ml_integration/stdlib/test_{module}.ml`:

**Structure**:
```ml
// Test {module} module

import {module};

// Test basic functionality
result1 = {module}.function1(args);
assert(result1 == expected, "function1 failed");

// Test edge cases
result2 = {module}.function2(edge_case);
assert(result2 == expected, "function2 failed");

// Test error handling
try {
    {module}.function_that_errors(bad_input);
    assert(false, "Should have thrown error");
} except (e) {
    assert(true, "Error handling works");
}

print("PASS: {module} tests passed");
```

**Validation**: All tests must transpile and execute successfully

---

### Security Tests (Tier 3+ modules)

For capability-intensive modules:

**File**: `tests/security/test_{module}_capabilities.py`

```python
"""Security tests for {module} capability enforcement."""

import pytest
from mlpy.runtime.capabilities.manager import get_capability_manager
from mlpy.runtime.capabilities.exceptions import CapabilityNotFoundError


class Test{Module}Security:
    """Test capability enforcement."""

    def test_requires_capability_for_operation(self):
        """Operation should fail without capability."""
        manager = get_capability_manager()

        with manager.capability_context("test", []):  # No capabilities
            with pytest.raises(CapabilityNotFoundError):
                # Try to use function requiring capability
                module.restricted_function(args)

    def test_works_with_capability(self):
        """Operation should work with capability."""
        from mlpy.runtime.capabilities.tokens import CapabilityToken

        manager = get_capability_manager()
        token = CapabilityToken(capability_type="required:capability")

        with manager.capability_context("test", [token]):
            # Should work now
            result = module.restricted_function(args)
            assert result is not None

    def test_capability_usage_tracked(self):
        """Capability usage should be tracked."""
        # Test that token.usage_count increments
        ...
```

---

## Documentation Requirements

### Per-Module Documentation

For each module, create `docs/api/{module}.md`:

**Structure**:

```markdown
# {Module} Module

## Overview

Brief description of module purpose and use cases.

## Capabilities Required

- `capability:name` - Description of when this capability is needed

## Functions

### {function_name}

**Signature**: `{module}.{function}(param1: type, param2: type) -> return_type`

**Description**: Detailed description of what the function does.

**Parameters**:
- `param1` (type): Description
- `param2` (type): Description

**Returns**: Description of return value

**Examples**:

```ml
import {module};

// Example 1
result = {module}.{function}(arg1, arg2);
print(result);  // Expected output

// Example 2
advanced_usage = {module}.{function}(complex_args);
```

**Errors**:
- Throws `ErrorType` if condition
- Returns default value if condition

**See Also**: Related functions

---

## Constants

### {constant_name}

**Value**: `3.14159...`

**Description**: Description of constant

---

## Security Considerations

Notes on capability requirements and security implications.

## Performance Notes

Any performance considerations or best practices.
```

---

### Master Documentation Index

**File**: `docs/api/stdlib-index.md`

```markdown
# ML Standard Library Reference

## Core Modules (Always Available)

- [builtin](builtin.md) - Core built-in functions (auto-imported)

## Tier 1: Foundation

- [math](math.md) - Mathematical operations
- [string](string.md) - String manipulation
- [array](array.md) - Array operations
- [console](console.md) - Console I/O

## Tier 2: Data & Utilities

- [json](json.md) - JSON encoding/decoding
- [datetime](datetime.md) - Date and time operations
- [regex](regex.md) - Regular expressions
- [random](random.md) - Random number generation
- [functional](functional.md) - Functional programming

## Tier 3: Advanced

- [file](file.md) - File system operations (requires capabilities)
- [crypto](crypto.md) - Cryptographic operations
- [collections](collections.md) - Advanced data structures

## Tier 4: Specialized

- [http](http.md) - HTTP client (requires capabilities)
- [sqlite](sqlite.md) - SQLite database (requires capabilities)

## Security Model

See [Capability System Guide](../security/capabilities.md) for details on how modules interact with the capability-based security system.
```

---

## Success Metrics

### Per-Module Acceptance Criteria

Before marking a module "complete":

✅ **Implementation**
- All functions implemented with decorators
- Proper error handling
- Type hints and documentation strings

✅ **Testing**
- 95%+ Python unit test coverage
- All ML integration tests pass
- Security tests pass (for Tier 3+)
- No regressions in existing tests

✅ **Documentation**
- Complete API reference written
- All functions have examples
- Security considerations documented
- Added to stdlib index

✅ **Code Review**
- Peer review completed
- Code quality standards met
- No security vulnerabilities

✅ **Performance**
- Function overhead < 10µs
- No memory leaks
- Benchmarks within targets

---

## Risk Management

### High-Risk Modules

**file, http, sqlite** - Capability enforcement critical

**Mitigation**:
- Extra security review
- Extensive capability testing
- Penetration testing
- Security audit before release

### Dependencies

**http** requires `requests` library
**sqlite** uses Python sqlite3 (built-in)

**Mitigation**: Document dependencies, test in clean environment

### Timeline Risks

**Risk**: Module takes longer than estimated

**Mitigation**:
- Buffer week built in (Week 6)
- Can defer Tier 4 if needed
- Core functionality (Tier 1-2) prioritized

---

## Conclusion

This implementation plan provides:

✅ **15 stdlib modules** (builtin + 14 more)
✅ **250+ functions** total
✅ **800+ unit tests** (Python + ML)
✅ **Complete documentation** for all modules
✅ **Security-first design** with capability integration
✅ **8-10 week timeline** with clear phases
✅ **Risk mitigation** strategies

**Deliverable**: Production-ready minimal standard library enabling real ML programs with security guarantees.

**Next Steps**: Review and approve plan, begin Week 1 implementation.
