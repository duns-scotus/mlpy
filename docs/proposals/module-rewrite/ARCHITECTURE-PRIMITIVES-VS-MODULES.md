# Module System Architecture: Primitives vs. Utility Modules

**Date**: January 2025
**Status**: APPROVED - Architecture Decision Record
**Impact**: Phase 3 and Phase 4 implementation strategy

## Executive Summary

This document clarifies the distinction between **primitive types with methods** (always available, no import) and **utility modules** (require explicit import). This follows Python/JavaScript conventions where primitive values have methods accessible via dot notation.

## The Problem

Initial Phase 3 implementation migrated `string_bridge` as an importable module requiring:
```ml
import string
string.upper("hello")  // Static call, requires import
```

This violates user expectations from Python/JavaScript:
```python
# Python - no import needed
"hello".upper()  # Method on string primitive
```

## Architecture Decision

### Two Categories of Standard Library

#### **Category 1: Primitive Types with Methods** (NO import needed)

These are **built-in to the language** and accessible on primitive values via dot notation:

**Primitive Types:**
- **string** - All string manipulation methods
- **int** - Integer utility methods
- **float** - Float utility methods
- **array** - Array manipulation methods (map, filter, reduce, etc.)
- **dict** - Dictionary/object methods

**How they work:**
- Methods are **registered with SafeAttributeRegistry** for each primitive type
- Available on **ALL values of that type** without import
- Accessed via **dot notation**: `value.method()`

**ML Usage:**
```ml
// No imports needed!
text = "hello,world"
parts = text.split(",")           // ✅ Method on string value
upper = text.upper()              // ✅ Method on string value
result = text.startsWith("hello") // ✅ Method on string value

numbers = [1, 2, 3, 4, 5]
evens = numbers.filter(x => x % 2 == 0)  // ✅ Method on array value
doubled = numbers.map(x => x * 2)        // ✅ Method on array value

num = 42
isEven = num.isEven()             // ✅ Method on int value
clamped = num.clamp(0, 10)        // ✅ Method on int value

value = 3.14159
rounded = value.round(2)          // ✅ Method on float value
```

#### **Category 2: Utility Modules** (require import)

These are **standalone modules** providing specialized functionality:

**Utility Modules:**
- **console** - Console output/logging
- **math** - Mathematical operations (sin, cos, sqrt, etc.)
- **regex** - Regular expression operations (returns Pattern objects)
- **datetime** - Date/time operations (returns DateTime objects)
- **collections** - Advanced data structures (Counter, OrderedDict, etc.)
- **functional** - Functional programming utilities (compose, curry, etc.)
- **random** - Random number/choice generation

**How they work:**
- Decorated with `@ml_module` decorator
- Must be **explicitly imported** in ML code
- Accessed via **module namespace**: `module.method()`
- May return **specialized objects** (Pattern, DateTime, etc.)

**ML Usage:**
```ml
import console
console.log("Hello")
console.error("Error message")

import math
result = math.sqrt(16)
angle = math.sin(math.pi / 2)

import regex
pattern = regex.compile("\\d+")      // Returns Pattern object
matches = pattern.findall("abc 123") // Method on Pattern object

import datetime
now = datetime.now()                 // Returns DateTime object
formatted = now.format("YYYY-MM-DD") // Method on DateTime object
later = now.addDays(7)               // Method on DateTime object

import random
dice = random.randint(1, 6)
choice = random.choice([1, 2, 3])
```

## Implementation Strategy

### Phase 3: Migrate Utility Modules ONLY

**Modules to migrate** (with OOP pattern):
1. ✅ **console** - Already migrated
2. ✅ **math** - Already migrated
3. ⏳ **regex** - Use OOP: `regex.compile()` returns Pattern object with methods
4. ⏳ **datetime** - Use OOP: `datetime.now()` returns DateTime object with methods
5. ⏳ **collections** - Use OOP: `collections.Counter()` returns Counter object
6. ⏳ **functional** - Pure functions (map, reduce, compose, curry)
7. ⏳ **random** - Pure functions (randint, choice, shuffle)

**Modules to REVERT/SKIP**:
- ❌ **string** - REVERT migration, will be primitive methods in Phase 4
- ❌ **int_module** - Skip migration, will be primitive methods in Phase 4
- ❌ **float_module** - Skip migration, will be primitive methods in Phase 4

### Phase 4: Builtin Module + Primitive Methods

**File**: `src/mlpy/stdlib/builtin.py`

#### 4.1 Core Type Conversion Functions

These are **always available** (auto-imported):

```python
@ml_module(name="builtin", auto_import=True)
class Builtin:
    @ml_function(description="Convert value to integer")
    def int(self, value):
        """
        Convert to integer:
        - int("123") → 123
        - int(3.14) → 3
        - int(true) → 1
        - int(false) → 0
        """
        if isinstance(value, bool):
            return 1 if value else 0
        if isinstance(value, str):
            try:
                # Handle float strings: "3.14" → 3
                if '.' in value:
                    return int(float(value))
                return int(value)
            except ValueError:
                return 0
        try:
            return int(value)
        except (ValueError, TypeError):
            return 0

    @ml_function(description="Convert value to float")
    def float(self, value):
        """
        Convert to float:
        - float("3.14") → 3.14
        - float(3) → 3.0
        - float(true) → 1.0
        """
        if isinstance(value, bool):
            return 1.0 if value else 0.0
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    @ml_function(description="Convert value to ML-compatible string")
    def str(self, value):
        """
        Convert to string with ML compatibility:
        - str(true) → "true" (NOT "True")
        - str(false) → "false" (NOT "False")
        - str(123) → "123"
        """
        if isinstance(value, bool):
            return "true" if value else "false"
        return str(value)

    @ml_function(description="Get type of value")
    def typeof(self, value):
        """
        Returns type name:
        - "string", "number", "boolean"
        - "array", "object", "function"
        - "unknown"
        """
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
        else:
            return "unknown"

    @ml_function(description="Get length of collection")
    def len(self, value):
        """Get length of string, array, or object."""
        try:
            return len(value)
        except TypeError:
            return 0

    @ml_function(description="Print values to console")
    def print(self, *args):
        """Print values with ML-compatible formatting."""
        output = []
        for arg in args:
            if isinstance(arg, bool):
                output.append("true" if arg else "false")
            else:
                output.append(str(arg))
        print(*output)
```

#### 4.2 Register Primitive Methods with SafeAttributeRegistry

**In builtin.py initialization**:

```python
def register_primitive_methods():
    """Register methods for primitive types with SafeAttributeRegistry."""
    from mlpy.ml.codegen.safe_attribute_registry import SafeAttributeRegistry
    registry = SafeAttributeRegistry()

    # ============================================================
    # STRING PRIMITIVE METHODS
    # ============================================================
    from mlpy.stdlib.string_bridge import (
        str_char_at, str_char_code_at, str_from_char_code,
        str_repeat, str_format, to_snake_case, to_camel_case,
        to_pascal_case, to_kebab_case, to_chars, str_trim,
        str_lstrip, str_rstrip, str_pad_left, str_pad_right,
        str_pad_center, str_is_empty, str_is_whitespace,
        str_is_alpha, str_is_numeric, str_is_alphanumeric,
        str_starts_with, str_ends_with, str_find, str_rfind,
        str_index_of, str_last_index_of, str_count,
        str_replace, str_replace_all, str_split, str_join,
        str_to_int, str_to_float, str_substring, str_slice,
        reverse_string
    )

    # Register all string methods on str type
    registry.register_type_method("str", "upper", lambda s: s.upper())
    registry.register_type_method("str", "lower", lambda s: s.lower())
    registry.register_type_method("str", "capitalize", lambda s: s.capitalize())
    registry.register_type_method("str", "charAt", str_char_at)
    registry.register_type_method("str", "charCodeAt", str_char_code_at)
    registry.register_type_method("str", "repeat", str_repeat)
    registry.register_type_method("str", "reverse", reverse_string)
    registry.register_type_method("str", "split", str_split)
    registry.register_type_method("str", "trim", str_trim)
    registry.register_type_method("str", "startsWith", str_starts_with)
    registry.register_type_method("str", "endsWith", str_ends_with)
    # ... all 70+ string methods

    # ============================================================
    # ARRAY PRIMITIVE METHODS
    # ============================================================
    registry.register_type_method("list", "append", lambda arr, item: arr.append(item))
    registry.register_type_method("list", "map", lambda arr, fn: [fn(x) for x in arr])
    registry.register_type_method("list", "filter", lambda arr, fn: [x for x in arr if fn(x)])
    # ... all array methods

    # ============================================================
    # INT PRIMITIVE METHODS
    # ============================================================
    from mlpy.stdlib.int_bridge import (
        int_to_string, int_to_float, int_to_bool,
        int_abs, int_min, int_max, int_pow,
        int_is_even, int_is_odd, int_is_positive,
        int_is_negative, int_is_zero, int_clamp, int_sign
    )

    registry.register_type_method("int", "toString", int_to_string)
    registry.register_type_method("int", "toFloat", int_to_float)
    registry.register_type_method("int", "isEven", int_is_even)
    registry.register_type_method("int", "isOdd", int_is_odd)
    registry.register_type_method("int", "clamp", int_clamp)
    registry.register_type_method("int", "sign", int_sign)
    # ... all int methods

    # ============================================================
    # FLOAT PRIMITIVE METHODS
    # ============================================================
    from mlpy.stdlib.float_bridge import (
        float_to_string, float_to_int, float_to_bool,
        float_abs, float_min, float_max, float_pow,
        float_sqrt, float_floor, float_ceil, float_round,
        float_is_positive, float_is_negative, float_is_zero,
        float_is_nan, float_is_finite
    )

    registry.register_type_method("float", "toString", float_to_string)
    registry.register_type_method("float", "toInt", float_to_int)
    registry.register_type_method("float", "round", float_round)
    registry.register_type_method("float", "floor", float_floor)
    registry.register_type_method("float", "ceil", float_ceil)
    registry.register_type_method("float", "sqrt", float_sqrt)
    # ... all float methods
```

#### 4.3 Auto-Import Builtin Functions

**Modify python_generator.py**:

```python
def _generate_header(self) -> str:
    """Generate Python file header with auto-imported builtins."""
    header_lines = []

    # Auto-import builtin functions (always available)
    header_lines.append("# Built-in functions (always available)")
    header_lines.append("from mlpy.stdlib.builtin import (")
    header_lines.append("    int, float, str, typeof,")
    header_lines.append("    len, print,")
    header_lines.append(")")
    header_lines.append("")

    # Initialize primitive method registry
    header_lines.append("# Initialize primitive type methods")
    header_lines.append("from mlpy.stdlib.builtin import register_primitive_methods")
    header_lines.append("register_primitive_methods()")
    header_lines.append("")

    return "\n".join(header_lines)
```

## Object-Oriented Module Design

### Regex Module (OOP Pattern)

```python
@ml_module(name="regex", description="Regular expression operations")
class RegexModule:
    @ml_function(description="Compile regex pattern")
    def compile(self, pattern: str, flags: int = 0):
        """Returns Pattern object with methods."""
        import re
        py_pattern = re.compile(pattern, flags)
        return Pattern(py_pattern)

@ml_class(description="Compiled regex pattern")
class Pattern:
    def __init__(self, py_pattern):
        self._pattern = py_pattern

    @ml_function(description="Find all matches")
    def findall(self, text: str) -> list:
        return self._pattern.findall(text)

    @ml_function(description="Test if pattern matches")
    def test(self, text: str) -> bool:
        return bool(self._pattern.search(text))

    @ml_function(description="Replace matches")
    def replace(self, text: str, replacement: str) -> str:
        return self._pattern.sub(replacement, text)
```

**ML Usage:**
```ml
import regex

pattern = regex.compile("\\d+")    // Returns Pattern object
matches = pattern.findall("a1 b2 c3")  // ["1", "2", "3"]
hasMatch = pattern.test("hello 123")   // true
replaced = pattern.replace("a1 b2", "X")  // "aX bX"
```

### DateTime Module (OOP Pattern)

```python
@ml_module(name="datetime", description="Date and time operations")
class DateTimeModule:
    @ml_function(description="Get current date/time")
    def now(self):
        """Returns DateTime object."""
        from datetime import datetime as py_datetime
        return DateTime(py_datetime.now())

    @ml_function(description="Parse date string")
    def parse(self, date_string: str, format: str = None):
        """Returns DateTime object."""
        from datetime import datetime as py_datetime
        if format:
            dt = py_datetime.strptime(date_string, format)
        else:
            # Attempt intelligent parsing
            dt = py_datetime.fromisoformat(date_string)
        return DateTime(dt)

@ml_class(description="Date/time object")
class DateTime:
    def __init__(self, py_datetime):
        self._dt = py_datetime

    @ml_function(description="Format as string")
    def format(self, format_string: str) -> str:
        return self._dt.strftime(format_string)

    @ml_function(description="Add days")
    def addDays(self, days: int):
        from datetime import timedelta
        new_dt = self._dt + timedelta(days=days)
        return DateTime(new_dt)

    @ml_function(description="Get year")
    def year(self) -> int:
        return self._dt.year

    @ml_function(description="Get month")
    def month(self) -> int:
        return self._dt.month
```

**ML Usage:**
```ml
import datetime

now = datetime.now()              // Returns DateTime object
formatted = now.format("YYYY-MM-DD")  // "2025-01-06"
nextWeek = now.addDays(7)         // DateTime object
year = now.year()                 // 2025

parsed = datetime.parse("2025-01-01")
month = parsed.month()            // 1
```

### Collections Module (OOP Pattern)

```python
@ml_module(name="collections", description="Advanced data structures")
class CollectionsModule:
    @ml_function(description="Create counter object")
    def Counter(self, iterable = None):
        """Returns Counter object."""
        from collections import Counter as PyCounter
        return Counter(PyCounter(iterable))

@ml_class(description="Counter for counting hashable objects")
class Counter:
    def __init__(self, py_counter):
        self._counter = py_counter

    @ml_function(description="Get count for item")
    def get(self, item):
        return self._counter[item]

    @ml_function(description="Get most common items")
    def mostCommon(self, n: int = None):
        return self._counter.most_common(n)

    @ml_function(description="Update counts")
    def update(self, iterable):
        self._counter.update(iterable)
```

**ML Usage:**
```ml
import collections

counter = collections.Counter(["a", "b", "a", "c", "a", "b"])
count = counter.get("a")        // 3
common = counter.mostCommon(2)  // [("a", 3), ("b", 2)]
```

## Migration Checklist

### Phase 3 - Utility Modules

- [x] console - Migrated (12 tests)
- [x] math - Migrated (28 tests)
- [x] **REVERT**: string - Remove decorators, delete tests
- [ ] regex - Migrate with Pattern OOP
- [ ] datetime - Migrate with DateTime OOP
- [ ] collections - Migrate with Counter/etc OOP
- [ ] functional - Migrate as pure functions
- [ ] random - Migrate as pure functions

### Phase 4 - Builtin + Primitives

- [ ] Create builtin.py with type conversions
- [ ] Register string methods on str type
- [ ] Register array methods on list type
- [ ] Register int methods on int type
- [ ] Register float methods on float type
- [ ] Register dict methods on dict type
- [ ] Auto-import builtin functions in python_generator.py
- [ ] Unit tests for all primitive methods
- [ ] Integration tests for OOP module patterns

## Benefits of This Architecture

1. **Intuitive**: Matches Python/JavaScript developer expectations
2. **No import overhead**: Primitive methods always available
3. **Clean separation**: Core language vs. specialized modules
4. **Performance**: Only load specialized modules when needed
5. **OOP elegance**: Pattern/DateTime objects feel natural
6. **Discoverability**: `value.` triggers autocomplete for methods

## Conclusion

This architecture provides:
- **Primitive methods** (string, int, float, array, dict) available on all values without import
- **Utility modules** (console, math, regex, datetime, etc.) requiring explicit import
- **Modern OOP patterns** for specialized objects (Pattern, DateTime, Counter)
- **Clean separation** between language core and standard library

This is the correct design for a modern, Pythonic ML language.
