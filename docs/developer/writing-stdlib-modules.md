# Writing ML Standard Library Modules

## Overview

This document describes the current procedure for creating a new standard library module in mlpy, including all the registration steps required to make it work with the security system and attribute access controls.

## Current Process (6 Required Steps)

Creating a new standard library module currently requires modifying **6 different files** across the codebase. While this is tedious, each step serves a specific purpose in the security and compilation pipeline.

---

## Step 1: Create the Bridge Module

**File:** `src/mlpy/stdlib/{module_name}_bridge.py`

Create a Python bridge module that implements your ML standard library functionality. This module should:

### Key Principles:
1. **Import Python stdlib with underscore prefix** to avoid naming collisions
   - Example: `import re as _re` (not `import re`)
   - This allows ML code to use clean names like `regex` while the bridge uses `_re` internally

2. **Create module interface class** with static methods
   - This class provides the main API that ML code will use
   - All methods should be `@staticmethod`

3. **Create auxiliary classes** (if needed)
   - Example: `Pattern` class for compiled regex patterns
   - These classes can have instance methods and properties

4. **Create module instance** at the bottom
   - Example: `regex = Regex()`
   - This is what gets imported into ML code

5. **Use camelCase for method names** (ML convention)
   - Example: `findAll`, `replaceAll`, `toString` (not snake_case)

6. **Error handling: Use RuntimeError for invalid input**
   - Don't silently return defaults or False
   - Raise descriptive RuntimeError exceptions
   - Example: `raise RuntimeError(f"Invalid regex pattern '{pattern}': {e}")`

### Example Bridge Module Structure:

```python
"""Python bridge implementations for ML {module} module.

Description of what this module provides.

Usage in ML:
    import {module};

    result = {module}.someMethod(args);
"""

import {python_stdlib} as _{python_stdlib}  # Underscore prefix to avoid collision


class AuxiliaryClass:
    """Auxiliary class that users can instantiate."""

    def __init__(self, param: str):
        """Constructor may raise RuntimeError for invalid input."""
        try:
            self._internal = _{python_stdlib}.something(param)
        except Exception as e:
            raise RuntimeError(f"Failed to create {type}: {e}")

    def instanceMethod(self, arg: str) -> result_type:
        """Instance method with camelCase name."""
        return self._internal.do_something(arg)

    @property
    def propertyName(self) -> type:
        """Property access (no parentheses in ML)."""
        return self._value


class ModuleName:
    """Main module interface class for ML code.

    All methods are static and can be called directly on the module object.
    """

    @staticmethod
    def staticMethod(arg: type) -> return_type:
        """Static method that ML code will call.

        Raises:
            RuntimeError: If operation fails
        """
        try:
            return _{python_stdlib}.function(arg)
        except Exception as e:
            raise RuntimeError(f"Operation failed: {e}")

    @staticmethod
    def factoryMethod(arg: str) -> AuxiliaryClass:
        """Factory method that creates auxiliary class instances.

        Returns:
            Instance of AuxiliaryClass

        Raises:
            RuntimeError: If creation fails
        """
        return AuxiliaryClass(arg)


# Create global module instance for ML import
{module_name} = ModuleName()

# Export public API
__all__ = [
    "ModuleName",
    "AuxiliaryClass",
    "{module_name}",
]
```

---

## Step 2: Register in stdlib __init__.py

**File:** `src/mlpy/stdlib/__init__.py`

Add your module to the standard library package:

```python
# Import at the top (around line 25)
from .{module_name}_bridge import {module_name}

# Add to __all__ export list (around line 117)
__all__ = [
    # ... existing modules ...
    "{module_name}",
]
```

**Purpose:** Makes the module available when Python code imports from `mlpy.stdlib`.

---

## Step 3: Add to Python Code Generator

**File:** `src/mlpy/ml/codegen/python_generator.py`

Add your module name to the recognized imports list (line 351):

```python
# Around line 351 in visit_import() method
if module_path in ["math", "json", "datetime", "random", "collections",
                   "console", "string", "array", "functional", "regex",
                   "{your_module_name}"]:  # Add your module here
```

**Purpose:** Tells the transpiler to generate proper import statements for your module.

**Generated code:** `from mlpy.stdlib.{module_name}_bridge import {module_name}`

---

## Step 4: Register in Safe Attribute Registry (Main Module Class)

**File:** `src/mlpy/ml/codegen/safe_attribute_registry.py`

Add your main module class to `_init_stdlib_classes()` method (around line 230):

```python
def _init_stdlib_classes(self):
    """Initialize safe attributes for ML standard library classes."""

    # ... existing registrations ...

    # Your module class from {module_name}_bridge
    {module_name}_methods = {
        "methodOne": SafeAttribute("methodOne", AttributeAccessType.METHOD, [],
                                   "Description of method one"),
        "methodTwo": SafeAttribute("methodTwo", AttributeAccessType.METHOD, [],
                                   "Description of method two"),
        "factoryMethod": SafeAttribute("factoryMethod", AttributeAccessType.METHOD, [],
                                       "Create auxiliary class instance"),
        # ... all public static methods ...
    }
    self.register_custom_class("ModuleName", {module_name}_methods)
```

**Important:** Use the **class name** (e.g., "ModuleName"), not the instance name.

---

## Step 5: Register in Safe Attribute Registry (Auxiliary Classes)

**File:** `src/mlpy/ml/codegen/safe_attribute_registry.py`

If your module has auxiliary classes (like Pattern, DateTime, etc.), register them too:

```python
def _init_stdlib_classes(self):
    """Initialize safe attributes for ML standard library classes."""

    # ... main module registration ...

    # Auxiliary class from {module_name}_bridge module
    auxiliary_class_methods = {
        "instanceMethod": SafeAttribute("instanceMethod", AttributeAccessType.METHOD, [],
                                        "Description"),
        "anotherMethod": SafeAttribute("anotherMethod", AttributeAccessType.METHOD, [],
                                       "Description"),
        "propertyName": SafeAttribute("propertyName", AttributeAccessType.PROPERTY, [],
                                      "Property description"),
        # ... all public methods and properties ...
    }
    self.register_custom_class("AuxiliaryClass", auxiliary_class_methods)
```

**Critical:** Each class that ML code can access must be registered separately.

---

## Step 6: Handle Dangerous Name Conflicts (If Applicable)

**File:** `src/mlpy/ml/codegen/safe_attribute_registry.py`

If your module has methods with names that match dangerous Python built-ins (like `compile`, `eval`, `exec`, `open`, etc.), the registration order matters.

The `is_safe_access()` method checks in this order:
1. Built-in type whitelist (str, list, dict, tuple)
2. **Custom class whitelist** ← Your module classes checked here
3. Dangerous patterns list ← Only if not found above

**No action needed** - the current implementation already handles this correctly. Your custom classes are checked before dangerous patterns, so methods like `regex.compile()` work even though `compile()` is dangerous.

**Verification:** Check the `is_safe_access()` method (around line 53):

```python
def is_safe_access(self, obj_type: Type, attr_name: str) -> bool:
    """Check if attribute access is safe for given type."""
    # Check built-in type whitelist first
    if obj_type in self._safe_attributes:
        # ... handle built-in types ...

    # Check custom class whitelist by class name
    # Custom classes take precedence over dangerous patterns
    # (e.g., regex.compile() is safe even though Python's compile() is dangerous)
    class_name = getattr(obj_type, '__name__', str(obj_type))
    if class_name in self._custom_classes:
        attr_info = self._custom_classes[class_name].get(attr_name)
        return attr_info is not None and attr_info.access_type != AttributeAccessType.FORBIDDEN

    # Check dangerous patterns last (only for unknown types)
    if attr_name in self._dangerous_patterns:
        return False

    return False
```

---

## Complete Example: The regex Module

Let's walk through how the `regex` module was implemented:

### 1. Bridge Module (`src/mlpy/stdlib/regex_bridge.py`)

```python
"""Python bridge implementations for ML regex module."""

import re as _re  # Underscore prefix to avoid collision


class Pattern:
    """Compiled regex pattern for efficient reuse."""

    def __init__(self, pattern: str):
        self.pattern = pattern
        try:
            self._compiled = _re.compile(pattern)
        except _re.error as e:
            raise RuntimeError(f"Invalid regex pattern '{pattern}': {e}")

    def test(self, text: str) -> bool:
        """Test if pattern matches text."""
        return bool(self._compiled.search(text))

    def findAll(self, text: str) -> list[str]:
        """Find all matches of pattern in text."""
        return self._compiled.findall(text)

    # ... more methods ...


class Regex:
    """Regex module interface for ML code."""

    @staticmethod
    def compile(pattern: str) -> Pattern:
        """Compile a pattern for efficient reuse."""
        return Pattern(pattern)

    @staticmethod
    def test(pattern: str, text: str) -> bool:
        """Test if pattern matches text."""
        try:
            return bool(_re.search(pattern, text))
        except _re.error as e:
            raise RuntimeError(f"Invalid regex pattern '{pattern}': {e}")

    # ... more static methods ...


# Create global regex instance
regex = Regex()

__all__ = ["Regex", "Pattern", "regex"]
```

### 2. Stdlib Registration (`src/mlpy/stdlib/__init__.py`)

```python
# Line 25
from .regex_bridge import regex

# Line 125
__all__ = [
    # ...
    "regex",
]
```

### 3. Code Generator (`src/mlpy/ml/codegen/python_generator.py`)

```python
# Line 351
if module_path in ["math", "json", "datetime", "random", "collections",
                   "console", "string", "array", "functional", "regex"]:
```

### 4. Safe Attribute Registry - Regex Class

```python
# In _init_stdlib_classes() method
regex_methods = {
    "compile": SafeAttribute("compile", AttributeAccessType.METHOD, [],
                            "Compile regex pattern"),
    "test": SafeAttribute("test", AttributeAccessType.METHOD, [],
                         "Test if pattern matches"),
    "findAll": SafeAttribute("findAll", AttributeAccessType.METHOD, [],
                            "Find all matches"),
    # ... 15 methods total ...
}
self.register_custom_class("Regex", regex_methods)
```

### 5. Safe Attribute Registry - Pattern Class

```python
# In _init_stdlib_classes() method
pattern_methods = {
    "test": SafeAttribute("test", AttributeAccessType.METHOD, [],
                         "Test if pattern matches text"),
    "match": SafeAttribute("match", AttributeAccessType.METHOD, [],
                          "Find first match"),
    "findAll": SafeAttribute("findAll", AttributeAccessType.METHOD, [],
                            "Find all matches"),
    "pattern": SafeAttribute("pattern", AttributeAccessType.PROPERTY, [],
                            "Pattern string"),
    # ... 9 methods/properties total ...
}
self.register_custom_class("Pattern", pattern_methods)
```

### 6. Dangerous Name Handling

The `regex.compile()` method works automatically because:
- "Regex" is registered in `_custom_classes`
- `is_safe_access()` checks custom classes BEFORE dangerous patterns
- Even though "compile" is in `_dangerous_patterns`, it's allowed for the Regex class

---

## Why Is This So Tedious?

You're right to observe that this is tedious work. Each step exists for a specific architectural reason:

### Security Architecture
1. **Bridge Module:** Isolates Python standard library from ML code
2. **Stdlib Package:** Provides clean namespace management
3. **Code Generator:** Controls transpilation and import generation
4. **Safe Attribute Registry (2 registrations):** Enforces runtime security checks on every attribute access

### The Problem
- **Manual duplication:** Method signatures must be listed in bridge AND registry
- **Easy to miss steps:** Forgetting one of the 6 files breaks the module
- **No validation:** No compile-time check that all methods are registered
- **Maintenance burden:** Adding a method requires updating multiple files

---

## Potential Improvements

Here are some ways this process could be streamlined:

### Option 1: Decorator-Based Auto-Registration
```python
from mlpy.stdlib.decorators import stdlib_module, safe_method

@stdlib_module("regex")
class Regex:
    @safe_method("Compile regex pattern")
    @staticmethod
    def compile(pattern: str) -> Pattern:
        return Pattern(pattern)
```

**Benefits:** Single source of truth, auto-registration
**Challenges:** Runtime registration, dynamic imports

### Option 2: Code Generation from Declarations
```yaml
# stdlib_modules.yaml
regex:
  class: Regex
  methods:
    - name: compile
      description: Compile regex pattern
      returns: Pattern
```

**Benefits:** Centralized configuration, can validate
**Challenges:** Build step required, less flexible

### Option 3: Introspection with Whitelist
```python
# Bridge module includes metadata
class Regex:
    __ml_safe_methods__ = ["compile", "test", "findAll", ...]
```

**Benefits:** Methods defined near implementation
**Challenges:** Security review process needed

### Option 4: Current Manual Process (Status Quo)
**Benefits:**
- Complete control and visibility
- Security-first with explicit whitelisting
- No runtime surprises
- Easy to audit

**Drawbacks:**
- Tedious and error-prone
- High maintenance burden
- Easy to forget steps

---

## Testing Your Module

After implementing all 6 steps, test your module:

```python
from tests.helpers.repl_test_helper import REPLTestHelper

# Test import
r = REPLTestHelper()
r.execute_ml('import {module_name}')

# Test static method
r.execute_ml('result = {module_name}.staticMethod(args)')
print('Static method result:', r.get_variable('result'))

# Test factory/auxiliary class
r.execute_ml('obj = {module_name}.factoryMethod(args)')
r.execute_ml('result2 = obj.instanceMethod(args)')
print('Instance method result:', r.get_variable('result2'))

# Test error handling
result = r.session.execute_ml_line('{module_name}.staticMethod("invalid")')
print('Error handling:', 'RuntimeError' in result.error)
```

Create comprehensive unit tests in `tests/unit/test_{module_name}_module.py`.

---

## Checklist for New Module

- [ ] **Step 1:** Create `src/mlpy/stdlib/{module_name}_bridge.py`
  - [ ] Import Python stdlib with underscore prefix
  - [ ] Create module interface class with static methods
  - [ ] Create auxiliary classes (if needed)
  - [ ] Use camelCase for method names
  - [ ] Raise RuntimeError for invalid input
  - [ ] Create module instance at bottom
  - [ ] Define `__all__` export list

- [ ] **Step 2:** Register in `src/mlpy/stdlib/__init__.py`
  - [ ] Add import statement
  - [ ] Add to `__all__` list

- [ ] **Step 3:** Add to `src/mlpy/ml/codegen/python_generator.py`
  - [ ] Add module name to recognized imports (line 351)

- [ ] **Step 4:** Register main class in `src/mlpy/ml/codegen/safe_attribute_registry.py`
  - [ ] Add to `_init_stdlib_classes()` method
  - [ ] Use `register_custom_class()` with class name
  - [ ] List all public static methods

- [ ] **Step 5:** Register auxiliary classes in safe_attribute_registry.py
  - [ ] Add to `_init_stdlib_classes()` method
  - [ ] Use `register_custom_class()` for each auxiliary class
  - [ ] List all public methods and properties

- [ ] **Step 6:** Verify dangerous name handling (if applicable)
  - [ ] Check if any methods match dangerous built-ins
  - [ ] Confirm custom class check happens before dangerous pattern check

- [ ] **Testing:** Create unit tests
  - [ ] Test import creates correct object
  - [ ] Test all static methods
  - [ ] Test auxiliary class creation and methods
  - [ ] Test error handling raises RuntimeError
  - [ ] Test with security enabled

---

## Summary

Creating a new ML standard library module requires:
1. Writing the bridge module (implementation)
2. Registering in stdlib package (Python imports)
3. Adding to code generator (ML import transpilation)
4. Registering main class in safe attribute registry (runtime security)
5. Registering auxiliary classes in safe attribute registry (runtime security)
6. Handling dangerous name conflicts (usually automatic)

**Total: 6 files to modify, plus testing**

This process is tedious but ensures:
- Complete security control
- Explicit whitelisting of all accessible methods
- Clear separation between ML and Python namespaces
- Protection against dangerous attribute access

Future improvements could streamline this process through decorators, code generation, or introspection-based registration systems.