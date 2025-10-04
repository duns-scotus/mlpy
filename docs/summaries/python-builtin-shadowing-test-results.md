# Python Builtin Shadowing: Test Results & Security Analysis

**Date**: January 2025
**Test File**: `tests/unit/stdlib/test_builtin_integration_issues.py::TestPythonBuiltinShadowing`
**Status**: 4/4 Tests Pass (Demonstrating Security Issue)

---

## Executive Summary

Created 4 test cases demonstrating the Python builtin shadowing problem using Python built-ins that are **NOT** in ML's stdlib builtin module:

| Test | Python Builtin | Current Result | Security Issue Level |
|------|---------------|----------------|---------------------|
| `test_eval_blocked_by_security_analyzer` | `eval()` | ✅ BLOCKED | **GOOD** - Defense-in-depth working |
| `test_type_function_returns_python_type` | `type()` | ✅ PASSES | **MEDIUM** - Semantic mismatch |
| `test_id_function_returns_memory_address` | `id()` | ✅ PASSES | **MEDIUM** - Python-specific behavior |
| `test_open_function_bypasses_capabilities` | `open()` | ✅ PASSES | **CRITICAL** - Capability bypass |

**Key Finding**: 3 out of 4 tests demonstrate **false positives** where Python built-ins are accessible when they shouldn't be!

---

## Test Case 1: eval() - Blocked by Security Analyzer ✅

### Test Code

```python
def test_eval_blocked_by_security_analyzer(self):
    """GOOD: eval() is blocked by security analyzer."""
    helper = REPLTestHelper()

    # Security analyzer blocks this (good defense-in-depth)
    with pytest.raises(AssertionError) as exc_info:
        result = helper.execute_ml('x = eval("1 + 2");')

    # Verify it's blocked by security, not NameError
    assert "Dangerous code injection operation" in str(exc_info.value)
```

### Result: ✅ PASSES (Security Working!)

```
AssertionError: ML execution failed: Error: Dangerous code injection operation 'eval' is not allowed
```

### Analysis

**Current Behavior**: Security analyzer **correctly blocks** `eval()` usage.

**Good News**: Defense-in-depth is working! The security analyzer catches dangerous operations.

**Architectural Issue**: However, the transpiler still generates `eval("1 + 2")` in the Python code. The block happens at security analysis stage, not code generation stage.

**After Fix**: Transpiler should generate code that tries to call `builtin.eval()`, which doesn't exist, resulting in `NameError` at runtime (cleaner failure).

**Security Level**: ✅ **PROTECTED** (but could be cleaner)

---

## Test Case 2: type() - Returns Python Type Object ❌

### Test Code

```python
def test_type_function_returns_python_type(self):
    """SEMANTIC ISSUE: type() returns Python type, not ML type string."""
    helper = REPLTestHelper()

    # This returns Python's type object, not ML's typeof string
    result = helper.execute_ml('x = type(42);')

    # Get the type object
    type_obj = helper.get_variable('x')

    # Currently returns <class 'int'> not "number"
    assert str(type_obj) == "<class 'int'>", \
        "SEMANTIC ISSUE: Python's type() used instead of ML's typeof()"
```

### Result: ✅ PASSES (Demonstrating Issue!)

**ML Code**:
```javascript
x = type(42);
```

**Generated Python Code**:
```python
x = type(42)  # Calls Python's type()
```

**Execution Result**:
```python
x = <class 'int'>  # Python type object
```

### Analysis

**Current Behavior**: ML code calling `type()` executes Python's `type()` function, which returns `<class 'int'>`.

**Expected ML Behavior**: ML should use `typeof()` which returns the string `"number"`.

**Semantic Mismatch**:
- **Python `type()`**: Returns type object `<class 'int'>`
- **ML `typeof()`**: Returns string `"number"`

**After Fix**: ML code calling `type()` should raise `NameError: name 'type' is not defined`, forcing developers to use ML's `typeof()`.

**Security Level**: ⚠️ **MEDIUM** - Not dangerous, but semantically incorrect

---

## Test Case 3: id() - Returns Python Memory Address ❌

### Test Code

```python
def test_id_function_returns_memory_address(self):
    """SEMANTIC ISSUE: id() returns Python memory address."""
    helper = REPLTestHelper()

    # This returns Python's object id (memory address)
    result = helper.execute_ml('obj = {x: 1}; obj_id = id(obj);')

    # Get the id value
    obj_id = helper.get_variable('obj_id')

    # Currently returns Python's memory address (integer)
    assert isinstance(obj_id, int)
    assert obj_id > 0, "Python id() returns positive integer"
```

### Result: ✅ PASSES (Demonstrating Issue!)

**ML Code**:
```javascript
obj = {x: 1};
obj_id = id(obj);
```

**Generated Python Code**:
```python
obj = {'x': 1}
obj_id = id(obj)  # Calls Python's id()
```

**Execution Result**:
```python
obj_id = 140735234567890  # Python memory address (example)
```

### Analysis

**Current Behavior**: ML code calling `id()` executes Python's `id()` function, which returns the object's memory address.

**Problems**:
1. **Non-portable**: Memory addresses are implementation-specific
2. **Python-specific**: Not part of ML semantics
3. **Security concern**: Exposes internal Python implementation details

**ML Builtin Module Status**: ML's builtin module **does have** an `id()` function, but the transpiler doesn't route to it!

**After Fix**: ML code calling `id()` should route to `builtin.id()`, not Python's `id()`.

**Security Level**: ⚠️ **MEDIUM** - Exposes implementation details, non-portable

---

## Test Case 4: open() - Bypasses Capability System 🚨

### Test Code

```python
def test_open_function_bypasses_capabilities(self):
    """CRITICAL SECURITY ISSUE: open() bypasses capability system."""
    helper = REPLTestHelper()

    # Test that open is callable (don't actually open a file)
    result = helper.execute_ml('can_call_open = callable(open);')

    # Currently open() is accessible (CRITICAL SECURITY ISSUE!)
    assert helper.get_variable('can_call_open') is True, \
        "CRITICAL SECURITY ISSUE: open() is accessible without capability checks!"
```

### Result: ✅ PASSES (CRITICAL ISSUE!)

**ML Code**:
```javascript
can_call_open = callable(open);
```

**Generated Python Code**:
```python
can_call_open = callable(open)  # Checks Python's open()
```

**Execution Result**:
```python
can_call_open = True  # Python's open() is accessible!
```

### Analysis

**Current Behavior**: Python's `open()` function is **accessible from ML code without capability checks**!

**What This Means**:
```javascript
// This ML code should REQUIRE FILE_READ capability
// But currently works without any capability!
content = open("secrets.txt", "r").read();
```

**Capability System Bypass**: Complete circumvention of file access control!

**After Fix**:
1. ML code calling `open()` should raise `NameError` (not in ML builtin)
2. File I/O should require explicit import with capability: `import file from "file";`
3. Sandbox should block Python's `open()` even if generated

**Security Level**: 🚨 **CRITICAL** - Complete capability system bypass

---

## Summary of False Positives

### What These Tests Prove

1. **type()** - Python builtin used instead of ML's `typeof()` → Semantic mismatch
2. **id()** - Python builtin used instead of ML's `id()` → Implementation leak
3. **open()** - Python builtin accessible without capabilities → **CRITICAL SECURITY HOLE**

### Root Cause

The transpiler generates direct function calls without checking if they're:
- ML builtin functions (should route to `builtin.function()`)
- User-defined functions (should call directly)
- Python built-ins (should be blocked/not defined)

**Generated Code**:
```python
# Current (WRONG):
x = type(42)         # Calls Python's type()
y = id(obj)          # Calls Python's id()
f = open("file.txt") # Calls Python's open() - NO CAPABILITY CHECK!
```

**Should Generate**:
```python
# After fix (CORRECT):
from mlpy.stdlib.builtin import builtin

x = builtin.type(42)  # Would raise AttributeError (doesn't exist)
# OR x = builtin.typeof(42)  # Use ML's typeof instead

y = builtin.id(obj)   # Routes to ML's id() implementation

# open() not in builtin, raises NameError
f = open("file.txt")  # NameError: name 'open' is not defined
```

---

## Defense-in-Depth Analysis

### Security Layer 1: Code Generation (BROKEN)

**Current**: Generates calls to Python built-ins ❌
**After Fix**: Routes to ML builtin module ✅

### Security Layer 2: Security Analyzer (PARTIAL)

**Current**: Blocks dangerous operations like `eval()` ✅
**Limitation**: Doesn't block `type()`, `id()`, `open()` ❌

### Security Layer 3: Sandbox (NEEDS ENHANCEMENT)

**Current**: Should restrict Python built-ins ⚠️
**After Fix**: Explicitly block dangerous built-ins ✅

---

## What Happens After the Fix

### Test Results After Implementation

| Test | Current | After Fix | Reason |
|------|---------|-----------|--------|
| `test_eval_blocked_by_security_analyzer` | Blocked by security | Blocked by security | Defense-in-depth |
| `test_type_function_returns_python_type` | ✅ PASSES | ❌ FAILS | NameError (not defined) |
| `test_id_function_returns_memory_address` | ✅ PASSES | ❌ FAILS | Routes to builtin.id() |
| `test_open_function_bypasses_capabilities` | ✅ PASSES | ❌ FAILS | NameError (not defined) |

**Expected Behavior After Fix**:
- `type()` → `NameError` (use `typeof()` instead)
- `id()` → Routes to `builtin.id()` (ML version)
- `open()` → `NameError` (requires file module import with capability)

---

## Recommendations

### Immediate Actions

1. **Implement auto-import mechanism** (as proposed in v2)
2. **Enhance sandbox** to explicitly block dangerous Python built-ins
3. **Update these tests** to expect NameError after fix

### Test Updates After Fix

```python
def test_type_raises_name_error_after_fix(self):
    """After fix: type() should not be defined (use typeof() instead)."""
    helper = REPLTestHelper()

    with pytest.raises(AssertionError) as exc_info:
        result = helper.execute_ml('x = type(42);')

    # Should raise NameError, not return Python type
    assert "NameError" in str(exc_info.value) or \
           "name 'type' is not defined" in str(exc_info.value)
```

### Additional Test Coverage Needed

Test other dangerous Python built-ins:
- `exec()` - Code execution (likely blocked by security)
- `compile()` - Code compilation
- `__import__()` - Dynamic imports
- `globals()`, `locals()`, `vars()` - Environment introspection
- `delattr()`, `setattr()` - Attribute manipulation
- `input()` - stdin access without capability

---

## Conclusion

**Tests Created**: 4 test cases
**Tests Passing**: 4/4 (all demonstrating the issue)
**False Positives Found**: 3/4 (type, id, open)
**Critical Security Issues**: 1 (open() bypasses capabilities)

**Key Takeaway**: The transpiler's lack of function call routing creates both **semantic mismatches** (type, id) and **critical security vulnerabilities** (open). The proposed decorator-driven auto-import mechanism will fix all of these issues.

**Next Steps**:
1. Implement decorator-driven auto-import (v2 proposal)
2. Enhance sandbox to block dangerous Python built-ins
3. Update these tests to verify NameError after fix
4. Add more test coverage for other dangerous built-ins

---

**Test File**: `tests/unit/stdlib/test_builtin_integration_issues.py`
**Test Class**: `TestPythonBuiltinShadowing`
**Run Command**: `pytest tests/unit/stdlib/test_builtin_integration_issues.py::TestPythonBuiltinShadowing -v`
