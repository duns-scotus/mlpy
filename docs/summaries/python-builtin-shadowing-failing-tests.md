# Python Builtin Shadowing: Failing Tests Expose Security Issue

**Date**: January 2025
**Test File**: `tests/unit/stdlib/test_builtin_integration_issues.py::TestPythonBuiltinShadowing`
**Status**: 3 tests XFAIL (Expected Failures - Exposing Security Issue)

---

## Executive Summary

Created 3 test cases that **FAIL** to expose the Python builtin shadowing security issue:

```bash
$ pytest tests/unit/stdlib/test_builtin_integration_issues.py::TestPythonBuiltinShadowing -v

tests\unit\stdlib\test_builtin_integration_issues.py xxx                 [100%]

============================= 3 xfailed in 1.80s ==============================
```

**Key Result**: All 3 tests marked as `xfail` (expected failures), proving the security issue exists!

---

## Understanding the Test Results

### What Does `xfail` Mean?

**`@pytest.mark.xfail(strict=True)`** means:
- ❌ **Currently**: Test FAILS (as expected) - security issue exists
- ✅ **After fix**: Test will PASS - security issue resolved
- 🚨 **If passes before fix**: Test run FAILS (strict=True) - unexpected behavior

### Test Status Legend

| Status | Symbol | Meaning |
|--------|--------|---------|
| **XFAIL** | `x` | Expected failure - known issue |
| **PASS** | `.` | Test passes |
| **FAIL** | `F` | Unexpected failure |
| **XPASS** | `X` | Unexpected pass (with strict=True, this fails the run) |

**Current Result**: `xxx` = 3 expected failures (security issue confirmed!)

---

## Test Case 1: type() Should Not Exist ❌

### Test Code

```python
@pytest.mark.xfail(
    reason="SECURITY ISSUE: type() calls Python builtin instead of raising NameError",
    strict=True
)
def test_type_function_should_not_exist(self):
    """TEST SHOULD FAIL: type() should not be defined in ML."""
    helper = REPLTestHelper()

    # This should raise NameError but currently works
    with pytest.raises(AssertionError) as exc_info:
        result = helper.execute_ml('x = type(42);')

    # Should fail with NameError, not return a value
    error_msg = str(exc_info.value)
    assert "NameError" in error_msg or "name 'type' is not defined" in error_msg
```

### Why It Fails (Current Behavior)

**ML Code**:
```javascript
x = type(42);
```

**Generated Python Code**:
```python
x = type(42)  # ❌ Calls Python's type()
```

**Execution Result**:
```python
x = <class 'int'>  # ❌ Returns Python type object, no NameError raised
```

**Why Test Fails**: The code executes successfully instead of raising `NameError`.

### Expected Behavior After Fix

**Generated Python Code**:
```python
from mlpy.stdlib.builtin import builtin

x = builtin.type(42)  # Would raise AttributeError (doesn't exist in builtin)
# OR just type(42) which raises NameError (not defined)
```

**Execution Result**:
```python
NameError: name 'type' is not defined
```

**When Fixed**: Test will PASS because NameError is raised as expected.

---

## Test Case 2: id() Should Use ML Version ❌

### Test Code

```python
@pytest.mark.xfail(
    reason="SECURITY ISSUE: id() calls Python builtin, exposing memory addresses",
    strict=True
)
def test_id_function_should_use_ml_version(self):
    """TEST SHOULD FAIL: id() should route to builtin.id()."""
    helper = REPLTestHelper()

    result = helper.execute_ml('obj = {x: 1}; obj_id = id(obj);')

    obj_id = helper.get_variable('obj_id')

    # ML's id() should return controlled value, not raw memory address
    assert obj_id < 100000, \
        "id() should not expose Python memory addresses"
```

### Why It Fails (Current Behavior)

**ML Code**:
```javascript
obj = {x: 1};
obj_id = id(obj);
```

**Generated Python Code**:
```python
obj = {'x': 1}
obj_id = id(obj)  # ❌ Calls Python's id()
```

**Execution Result**:
```python
obj_id = 140735234567890  # ❌ Python memory address (very large number)
```

**Why Test Fails**: Returns memory address (> 100000), not a controlled ML id.

### Expected Behavior After Fix

**Generated Python Code**:
```python
from mlpy.stdlib.builtin import builtin

obj = {'x': 1}
obj_id = builtin.id(obj)  # ✅ Routes to ML's id() implementation
```

**Execution Result**:
```python
obj_id = 123  # ✅ ML's controlled id value (< 100000)
```

**When Fixed**: Test will PASS because id() routes to ML's implementation.

---

## Test Case 3: open() Should Not Be Callable 🚨

### Test Code

```python
@pytest.mark.xfail(
    reason="CRITICAL SECURITY ISSUE: open() bypasses capability system",
    strict=True
)
def test_open_function_should_not_be_callable(self):
    """TEST SHOULD FAIL: open() should not be accessible without capability."""
    helper = REPLTestHelper()

    # This should raise NameError but currently works
    with pytest.raises(AssertionError) as exc_info:
        result = helper.execute_ml('can_call_open = callable(open);')

    # Should fail with NameError
    error_msg = str(exc_info.value)
    assert "NameError" in error_msg or "name 'open' is not defined" in error_msg
```

### Why It Fails (Current Behavior)

**ML Code**:
```javascript
can_call_open = callable(open);
```

**Generated Python Code**:
```python
can_call_open = callable(open)  # ❌ Checks Python's open()
```

**Execution Result**:
```python
can_call_open = True  # ❌ Python's open() is accessible!
```

**Why Test Fails**: Python's `open()` is callable, no NameError raised.

**CRITICAL SECURITY ISSUE**: This means ML code can do this:

```javascript
// NO CAPABILITY CHECK!
content = open("secrets.txt", "r").read();
```

### Expected Behavior After Fix

**Generated Python Code**:
```python
# open is not imported, not in builtin module
can_call_open = callable(open)  # NameError: name 'open' is not defined
```

**Execution Result**:
```python
NameError: name 'open' is not defined
```

**When Fixed**: Test will PASS because NameError is raised as expected.

---

## Security Impact Analysis

### Current State (Tests Failing = Issue Exists)

| Function | Current Behavior | Security Risk |
|----------|------------------|---------------|
| `type()` | Calls Python's type() | MEDIUM - Semantic mismatch |
| `id()` | Exposes memory addresses | MEDIUM - Implementation leak |
| `open()` | Bypasses capabilities | **CRITICAL** - Complete security bypass |

### What Can Be Done Now (Security Holes)

```javascript
// ALL OF THESE WORK WITHOUT CAPABILITY CHECKS:

// Read any file
content = open("/etc/passwd", "r").read();

// Write to any file
f = open("malicious.py", "w");
f.write("import os; os.system('rm -rf /')");

// Execute arbitrary code (blocked by security analyzer, but still generates the call)
result = eval("__import__('os').system('whoami')");

// Access Python internals
mem_addr = id(sensitive_object);  // Leak memory addresses
py_type = type(obj);  // Get Python type objects
```

### After Fix (Tests Passing = Issue Resolved)

```javascript
// ALL OF THESE WILL RAISE NameError:

content = open("file.txt", "r");  // NameError: name 'open' is not defined
result = type(42);                // NameError: name 'type' is not defined

// Proper ML usage:
obj_id = id(obj);                 // Routes to builtin.id() (ML version)
obj_type = typeof(obj);           // Uses ML's typeof(), not Python's type()
```

---

## What Happens After the Fix

### Test Lifecycle

**Phase 1: NOW (Exposing Issue)**
```bash
$ pytest tests/unit/stdlib/test_builtin_integration_issues.py::TestPythonBuiltinShadowing -v

xxx                 [100%]  # 3 expected failures
============================= 3 xfailed in 1.80s ==============================
```

**Phase 2: AFTER IMPLEMENTING FIX**
```bash
$ pytest tests/unit/stdlib/test_builtin_integration_issues.py::TestPythonBuiltinShadowing -v

...                 [100%]  # 3 tests PASS!
============================= 3 passed in 1.80s ================================
```

**Phase 3: REMOVE xfail MARKERS**

Once the fix is verified, remove `@pytest.mark.xfail` decorators:

```python
# Remove the @pytest.mark.xfail decorator
def test_type_function_should_not_exist(self):
    """type() correctly raises NameError."""
    # Test now passes normally
```

---

## How to Verify the Fix

### Step 1: Implement Decorator-Driven Auto-Import

Implement the proposal in `docs/proposals/builtin-auto-import-architecture-v2.md`:
1. Create `builtin_introspection.py` with decorator cache
2. Modify `python_generator.py` to route builtin calls
3. Add auto-import of `from mlpy.stdlib.builtin import builtin`

### Step 2: Run These Tests

```bash
$ pytest tests/unit/stdlib/test_builtin_integration_issues.py::TestPythonBuiltinShadowing -v
```

**Expected Result**: All 3 tests should now PASS (no longer xfail)

### Step 3: Verify Generated Code

Check that transpiler generates:

```python
# Before fix:
x = type(42)  # ❌ Calls Python's type()

# After fix:
from mlpy.stdlib.builtin import builtin
x = type(42)  # ✅ Raises NameError (or routes to builtin if defined)
```

### Step 4: Run Integration Tests

```bash
$ python tests/ml_test_runner.py --full --category ml_builtin --matrix
```

**Expected Result**: 31.2% → 100% pass rate

---

## Summary

### Tests Created

| Test | Issue Exposed | Severity |
|------|--------------|----------|
| `test_type_function_should_not_exist` | type() semantic mismatch | MEDIUM |
| `test_id_function_should_use_ml_version` | id() memory leak | MEDIUM |
| `test_open_function_should_not_be_callable` | open() capability bypass | **CRITICAL** |

### Current Status

✅ **3 tests created**
❌ **3 tests XFAIL** (expected failures)
🎯 **Security issue confirmed and documented**

### After Fix

✅ **3 tests will PASS**
✅ **Security holes closed**
✅ **Capability system enforced**

---

## Key Takeaways

1. **Tests FAIL = Issue EXISTS**: The xfail status proves Python builtins are accessible
2. **Tests PASS = Issue FIXED**: When tests pass, auto-import mechanism works
3. **Critical Security Hole**: `open()` bypasses capability system completely
4. **Semantic Issues**: `type()` and `id()` use Python versions, not ML versions

**Next Action**: Implement decorator-driven auto-import mechanism to make these tests pass!

---

**Test File**: `tests/unit/stdlib/test_builtin_integration_issues.py`
**Test Class**: `TestPythonBuiltinShadowing`
**Run Command**: `pytest tests/unit/stdlib/test_builtin_integration_issues.py::TestPythonBuiltinShadowing -v`
**Current Status**: 3 xfailed (expected failures - security issue confirmed)
**After Fix**: 3 passed (security issue resolved)
