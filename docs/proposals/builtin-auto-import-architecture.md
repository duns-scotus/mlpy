# Builtin Auto-Import Architecture: Problem Analysis & Solution Design

## Executive Summary

**CRITICAL SECURITY & SEMANTIC ISSUE IDENTIFIED**: The transpiler generates Python code that directly calls Python's built-in functions instead of ML's stdlib builtin module. This creates:
1. **Security vulnerability**: Uncontrolled access to Python built-ins bypasses the capability system
2. **Semantic mismatches**: Python built-ins don't match ML's expected behavior
3. **Missing functions**: ML builtin functions don't exist in Python (`typeof`, standalone `keys`/`values`)
4. **Accidental success**: 31.2% of tests pass only because Python happens to match ML semantics

**Recommended Solution**: Implement compile-time function call routing with auto-import of `mlpy.stdlib.builtin`.

---

## Part 1: Problem Analysis

### Current Architecture

#### Code Generation (Lines 666-680 in `python_generator.py`)

```python
elif isinstance(expr, FunctionCall):
    if isinstance(expr.function, Identifier):
        func_name = self._safe_identifier(expr.function.name)

    args = [self._generate_expression(arg) for arg in expr.arguments]
    return f"{func_name}({', '.join(args)})"  # ❌ PROBLEM: Direct call
```

**What happens:**
- ML code: `int("3.14")`
- Generated Python: `int("3.14")`
- Actual execution: Calls **Python's `int()`**, not **ML's `builtin.int()`**

### Security Implications

#### Capability System Bypass

The ML language's security model relies on controlling all system access through the capability system:
```python
# INTENDED: All system operations require capabilities
file = File.open("data.txt", capabilities=[READ_FILE])

# ACTUAL: Python built-ins bypass capability checks
open("data.txt", "r")  # No capability check!
```

#### Python Builtin Access Without Control

Currently accessible Python built-ins that bypass security:
- **eval()**, **exec()**, **compile()** - Code execution
- **__import__()**, **globals()**, **locals()** - Introspection
- **open()** - File I/O without capability checks
- **input()** - Unrestricted stdin access
- **type()**, **isinstance()** - Unrestricted type introspection

**Risk Level**: HIGH - Direct security model violation

### Semantic Mismatches

#### Type Conversion Failures

**int() with float strings:**
```python
# ML expectation:
int("3.14")  # → 3 (converts via float)

# Python reality:
int("3.14")  # ValueError: invalid literal for int() with base 10: '3.14'
```

**str() with booleans:**
```python
# ML expectation:
str(true)  # → "true" (lowercase for ML compatibility)

# Python reality:
str(True)  # → "True" (Python's capitalized boolean)
```

#### Iterator vs List Returns

**enumerate():**
```python
# ML expectation:
e = enumerate(['a', 'b', 'c'])
len(e)  # → 3 (enumerate returns list)

# Python reality:
e = enumerate(['a', 'b', 'c'])
len(e)  # TypeError: object of type 'enumerate' has no len()
```

**reversed():**
```python
# ML expectation:
r = reversed([1, 2, 3])
r[0]  # → 3 (reversed returns list)

# Python reality:
r = reversed([1, 2, 3])
r[0]  # TypeError: 'list_reverseiterator' object is not subscriptable
```

#### Missing Functions

**typeof():**
```python
# ML code:
t = typeof(42)  # Should return "number"

# Generated Python:
t = typeof(42)  # NameError: name 'typeof' is not defined
```

**keys() / values():**
```python
# ML code:
k = keys({a: 1, b: 2})  # Should return ["a", "b"]

# Python reality:
k = keys({a: 1, b: 2})  # NameError: name 'keys' is not defined
# (keys() is a dict method, not a standalone function)
```

### Why 31.2% "Accidentally" Pass

Integration tests passing because Python built-ins match ML semantics:

| Test File | Functions Used | Why It Passes |
|-----------|---------------|---------------|
| 08_predicate_functions.ml | callable(), all(), any() | Python built-ins identical to ML |
| 09_sum_function.ml | sum() | Python built-in identical to ML |
| 10_char_conversions.ml | chr(), ord() | Python built-ins identical to ML |
| 11_number_base_conversions.ml | hex(), bin(), oct() | Python built-ins identical to ML |
| 12_string_representations.ml | repr(), format() | Python built-ins close enough to ML |

**Critical observation**: These pass **by accident**, not by design. If Python changes these functions, ML programs break.

### Test Results Analysis

#### Execution Failures (11/16 tests = 68.8%)

All failures traced to:
1. Python built-in called instead of ML builtin → semantic mismatch or NameError
2. No auto-import of `mlpy.stdlib.builtin` module

| Test File | Failure Reason |
|-----------|---------------|
| 01_type_conversion.ml | `int("3.14")` ValueError |
| 02_type_checking.ml | `typeof` not defined |
| 03_collection_functions.ml | `enumerate()` returns iterator |
| 04_print_functions.ml | `typeof` not defined |
| 05_math_utilities.ml | `min(1,2,3)` fails (expects iterable) |
| 06_array_utilities.ml | `sorted(arr, true)` wrong parameter |
| 07_object_utilities.ml | `keys`/`values` not defined |
| 13_reversed_function.ml | `reversed()` returns iterator |
| 14_dynamic_introspection.ml | Security blocks + functions not defined |
| 15_edge_cases.ml | `keys`/`typeof` not defined |
| 16_comprehensive_integration.ml | Multiple undefined functions |

---

## Part 2: Solution Design

### Design Principles

1. **Security-First**: All function calls must be controllable and auditable
2. **Explicit Routing**: Clear separation between ML builtins, user functions, and Python operations
3. **Compile-Time Transformation**: Transform during transpilation, not at runtime
4. **Minimal Performance Impact**: Registry lookup should be O(1), minimal overhead
5. **Maintainability**: Single source of truth for builtin function definitions

### Recommended Approach: Hybrid Architecture

#### Component 1: Builtin Function Registry

**Create**: `src/mlpy/ml/codegen/builtin_registry.py`

```python
"""Registry of ML built-in functions that require auto-import and routing."""

# Complete list of ML builtin functions
ML_BUILTIN_FUNCTIONS = {
    # Type conversion (4)
    'int', 'float', 'str', 'bool',

    # Type checking (2)
    'typeof', 'isinstance',

    # Collections (3)
    'len', 'range', 'enumerate',

    # I/O (2)
    'print', 'input',

    # Introspection (3)
    'id', 'hash', 'dir',

    # Dynamic introspection (3)
    'hasattr', 'getattr', 'call',

    # Math utilities (5)
    'abs', 'min', 'max', 'round', 'sum',

    # Array utilities (3)
    'sorted', 'reversed', 'zip',

    # Object utilities (2)
    'keys', 'values',

    # Predicates (3)
    'all', 'any', 'callable',

    # Character conversions (2)
    'chr', 'ord',

    # Number base conversions (3)
    'hex', 'bin', 'oct',

    # String representations (2)
    'repr', 'format',
}

def is_ml_builtin(func_name: str) -> bool:
    """Check if a function name is an ML builtin function."""
    return func_name in ML_BUILTIN_FUNCTIONS

def get_all_builtins() -> set[str]:
    """Get the complete set of ML builtin function names."""
    return ML_BUILTIN_FUNCTIONS.copy()
```

**Rationale**:
- Single source of truth
- Easy to maintain and extend
- Fast O(1) lookup
- Explicit and auditable

#### Component 2: Enhanced Code Generator

**Modify**: `src/mlpy/ml/codegen/python_generator.py`

##### Add Tracking Field

```python
@dataclass
class CodeGenContext:
    """Context for code generation."""
    # ... existing fields ...

    # NEW: Track which builtin functions are used
    builtin_functions_used: set[str] = field(default_factory=set)
    builtin_import_added: bool = False
```

##### Enhance Function Call Generation (Lines 666-680)

```python
elif isinstance(expr, FunctionCall):
    # Handle function name
    if isinstance(expr.function, str):
        func_name = expr.function
    elif isinstance(expr.function, Identifier):
        func_name = expr.function.name
    elif isinstance(expr.function, MemberAccess):
        # Method calls - don't transform
        func_name = None
        member_call_code = self._generate_expression(expr.function)
        args = [self._generate_expression(arg) for arg in expr.arguments]
        return f"{member_call_code}({', '.join(args)})"
    else:
        func_name = None

    # NEW: Check if this is an ML builtin function
    if func_name and is_ml_builtin(func_name):
        # Track usage for import generation
        self.context.builtin_functions_used.add(func_name)
        # Generate call to builtin module
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

##### Add Auto-Import Method

```python
def _ensure_builtin_imported(self) -> None:
    """Ensure builtin module is imported if any builtin functions are used."""
    if self.context.builtin_functions_used and not self.context.builtin_import_added:
        self.context.builtin_import_added = True
        # Use 'builtin' as the import name (lowercase to avoid conflict)
        self.context.imports_needed.add("from mlpy.stdlib.builtin import builtin")
```

##### Update Import Emission (Line 123)

```python
def _emit_imports(self):
    """Emit necessary Python imports."""
    # NEW: Ensure builtin import is added if needed
    self._ensure_builtin_imported()

    for import_name in sorted(self.context.imports_needed):
        # Handle both "import xyz" and "from xyz import abc" statements
        if import_name.startswith("from ") or import_name.startswith("import "):
            self._emit_line(import_name)
        elif import_name == "mlpy.stdlib.runtime_helpers":
            self._emit_line(
                "from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access, get_safe_length"
            )
        else:
            self._emit_line(f"import {import_name}")
```

#### Component 3: Scope-Aware Analysis (Prevents False Positives)

**Problem**: User-defined function named `int` would be incorrectly transformed.

**Solution**: Check variable scope before transformation.

```python
def _is_user_defined_function(self, func_name: str) -> bool:
    """Check if a function name is user-defined in current scope."""
    # Check if it's defined in the current module
    return func_name in self.context.defined_functions

def _should_route_to_builtin(self, func_name: str) -> bool:
    """Determine if function call should route to builtin module."""
    # Route to builtin if:
    # 1. It's in the builtin registry
    # 2. It's NOT user-defined in the current scope
    return is_ml_builtin(func_name) and not self._is_user_defined_function(func_name)
```

### Expected Code Generation

#### Before (Current - Broken):

**ML Code:**
```javascript
x = int("3.14");
t = typeof(x);
print(t);
```

**Generated Python:**
```python
"""Generated Python code from mlpy ML transpiler."""

x = int("3.14")  # ❌ ValueError
t = typeof(x)    # ❌ NameError
print(t)         # ❌ Never reached
```

#### After (Fixed):

**ML Code:**
```javascript
x = int("3.14");
t = typeof(x);
print(t);
```

**Generated Python:**
```python
"""Generated Python code from mlpy ML transpiler."""

from mlpy.stdlib.builtin import builtin

x = builtin.int("3.14")  # ✅ Returns 3
t = builtin.typeof(x)    # ✅ Returns "number"
builtin.print(t)         # ✅ Prints "number"
```

---

## Part 3: Security Enhancements

### Sandbox Builtin Restrictions

**Enhance**: `src/mlpy/runtime/sandbox/sandbox.py`

```python
# Restricted __builtins__ for ML code execution
SAFE_BUILTINS = {
    # Math (safe)
    'abs', 'round', 'min', 'max', 'sum',
    # Types (safe)
    'bool', 'int', 'float', 'str', 'list', 'dict', 'tuple', 'set',
    # Utility (safe)
    'len', 'range', 'enumerate', 'zip', 'reversed', 'sorted',
    # Needed internally
    'Exception', 'ValueError', 'TypeError', 'AttributeError',
}

BLOCKED_BUILTINS = {
    # Code execution
    'eval', 'exec', 'compile',
    # Imports
    '__import__', 'import',
    # Introspection
    'globals', 'locals', 'vars', 'dir',
    # File I/O
    'open',
    # Dangerous
    'breakpoint', 'help', 'input',
}

def create_safe_namespace():
    """Create a restricted namespace for ML code execution."""
    safe_builtins = {
        name: __builtins__[name]
        for name in SAFE_BUILTINS
        if name in __builtins__
    }
    return {'__builtins__': safe_builtins}
```

**Rationale**: Defense in depth - even if code generation fails, sandbox prevents dangerous operations.

---

## Part 4: Implementation Plan

### Phase 1: Core Implementation (2-3 hours)

**Priority: CRITICAL**

1. ✅ Create `builtin_registry.py` with all 38 ML builtin functions
2. ✅ Modify `PythonCodeGenerator.__init__()` to add tracking fields
3. ✅ Enhance `_generate_expression()` FunctionCall handling (lines 666-680)
4. ✅ Add `_ensure_builtin_imported()` method
5. ✅ Update `_emit_imports()` to call `_ensure_builtin_imported()`
6. ✅ Run integration tests - expect 68.8% → 100% improvement

**Success Criteria**:
- All 16 ml_builtin integration tests pass (currently 5/16)
- Generated Python code includes `from mlpy.stdlib.builtin import builtin`
- All builtin function calls transformed to `builtin.function()`

### Phase 2: Scope Analysis (1-2 hours)

**Priority: HIGH**

1. ✅ Add `defined_functions` tracking to CodeGenContext
2. ✅ Implement `_is_user_defined_function()` method
3. ✅ Implement `_should_route_to_builtin()` method
4. ✅ Update function call generation to use scope analysis
5. ✅ Create test cases for shadowed builtin names

**Success Criteria**:
- User-defined `int()` function not transformed
- Scope-sensitive routing works correctly
- No false positives in transformation

### Phase 3: Security Hardening (2-3 hours)

**Priority: HIGH**

1. ✅ Implement `SAFE_BUILTINS` and `BLOCKED_BUILTINS` lists
2. ✅ Update sandbox to use restricted namespace
3. ✅ Add security tests for builtin bypass attempts
4. ✅ Verify capability system integration
5. ✅ Test defense-in-depth security model

**Success Criteria**:
- Cannot access `eval`, `exec`, `__import__` from ML code
- Sandbox blocks dangerous built-ins even if generated
- All security tests pass

### Phase 4: Edge Cases & Testing (1-2 hours)

**Priority: MEDIUM**

1. ✅ Test method calls vs function calls (obj.method() not transformed)
2. ✅ Test lambda/nested scopes
3. ✅ Test import name conflicts
4. ✅ Comprehensive unit test suite
5. ✅ Performance benchmarking

**Success Criteria**:
- All edge cases handled correctly
- Performance impact < 5%
- 100% test coverage for new code

### Phase 5: Documentation (1 hour)

**Priority: MEDIUM**

1. ✅ Update developer guide with auto-import mechanism
2. ✅ Document builtin function registry maintenance
3. ✅ Add code generation examples
4. ✅ Update security model documentation

---

## Part 5: Testing Strategy

### Unit Tests

**Create**: `tests/unit/codegen/test_builtin_routing.py`

```python
def test_builtin_function_transformed():
    """Test that builtin functions are routed to builtin module."""
    ml_code = 'x = int("42");'
    result = transpile(ml_code)
    assert 'builtin.int' in result.python_code
    assert 'from mlpy.stdlib.builtin import builtin' in result.python_code

def test_user_function_not_transformed():
    """Test that user-defined functions are not transformed."""
    ml_code = '''
    function int(x) { return x * 2; }
    y = int(5);
    '''
    result = transpile(ml_code)
    assert 'builtin.int' not in result.python_code  # Should call user int()

def test_method_call_not_transformed():
    """Test that method calls are not transformed."""
    ml_code = 'x = obj.int();'
    result = transpile(ml_code)
    assert 'obj.int()' in result.python_code
    assert 'builtin.int' not in result.python_code

def test_import_only_when_needed():
    """Test that import is only added when builtins are used."""
    ml_code = 'x = 5;'  # No builtin calls
    result = transpile(ml_code)
    assert 'from mlpy.stdlib.builtin import builtin' not in result.python_code
```

### Integration Tests

**Existing**: `tests/ml_integration/ml_builtin/` (16 files)

Expected results after fix:
- **Before**: 5/16 passing (31.2%)
- **After**: 16/16 passing (100%)

### Security Tests

**Create**: `tests/security/test_builtin_bypass.py`

```python
def test_cannot_access_eval_directly():
    """Test that eval cannot be accessed from ML code."""
    ml_code = 'x = eval("1+1");'
    with pytest.raises(SecurityError):
        execute_ml(ml_code)

def test_cannot_access_exec_directly():
    """Test that exec cannot be accessed from ML code."""
    ml_code = 'exec("print(1)");'
    with pytest.raises(SecurityError):
        execute_ml(ml_code)

def test_cannot_bypass_with_getattr():
    """Test that getattr cannot bypass builtin restrictions."""
    ml_code = 'f = getattr(__builtins__, "eval");'
    with pytest.raises(SecurityError):
        execute_ml(ml_code)
```

---

## Part 6: Risk Assessment & Mitigation

### Implementation Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Breaking user code with `int()` function | Low | Medium | Scope analysis to detect user-defined functions |
| Performance degradation | Low | Low | Benchmark tests, O(1) registry lookup |
| Import name conflicts | Low | Low | Use unique import alias `_mlpy_builtin` if needed |
| Security bypass | Medium | CRITICAL | Defense-in-depth: sandbox + code gen + analysis |
| False positive transformations | Medium | Medium | Scope-aware routing, comprehensive testing |

### Backward Compatibility

**Breaking Changes**:
- Existing transpiled Python code will need regeneration
- ML source code **unchanged** - fully backward compatible

**Migration Path**:
1. Update mlpy compiler
2. Re-transpile all ML source files
3. No ML source code changes needed

### Performance Impact

**Expected Overhead**:
- Registry lookup: O(1) hash check - negligible
- Extra function call: `builtin.int()` vs Python's `int()` - ~1-2% overhead
- Import overhead: One-time at module load - negligible

**Benchmarking**:
- Target: < 5% performance degradation
- Measure: Transpilation time + execution time
- Monitor: Integration test execution times

---

## Part 7: Alternative Approaches Considered

### Option A: Runtime Namespace Shadowing ❌ REJECTED

**How it works**: Override `__builtins__` at runtime

**Pros**:
- No code transformation needed
- Simpler code generation

**Cons**:
- Complex runtime setup
- Hard to debug
- Security risk if shadowing fails
- Interferes with legitimate Python code
- Performance overhead on every call

**Verdict**: Too risky, too complex

### Option B: Explicit Import Requirement ❌ REJECTED

**How it works**: Require `import { int, str } from builtin;` in ML code

**Pros**:
- Explicit dependencies
- Clear imports

**Cons**:
- Breaks "no imports needed" design goal
- User-unfriendly
- Verbose ML code
- Not backward compatible

**Verdict**: Violates design principles

### Option C: Hybrid Approach (Recommended) ✅ ACCEPTED

**How it works**: Compile-time routing + auto-import + defense-in-depth security

**Pros**:
- Security-first by default
- User-friendly (no ML code changes)
- Clear separation of concerns
- Maintainable
- Performant

**Cons**:
- Requires maintaining function registry
- Slight code generation complexity

**Verdict**: Best balance of security, usability, and maintainability

---

## Part 8: Success Metrics

### Immediate Success Criteria

1. ✅ All 16 ml_builtin integration tests pass (currently 5/16)
2. ✅ Generated Python code includes builtin import when needed
3. ✅ All builtin function calls transformed correctly
4. ✅ No false positive transformations
5. ✅ Security tests pass - no builtin bypass

### Long-Term Success Criteria

1. ✅ Zero security vulnerabilities related to Python builtin access
2. ✅ 100% semantic correctness for ML builtins vs Python builtins
3. ✅ Maintainable: Easy to add new builtin functions
4. ✅ Performance: < 5% overhead
5. ✅ Developer-friendly: Clear error messages, good documentation

### Regression Prevention

1. ✅ Unit tests for builtin routing
2. ✅ Integration tests for all 38 builtins
3. ✅ Security tests for bypass attempts
4. ✅ Performance benchmarks
5. ✅ Documentation with examples

---

## Part 9: Conclusion

### Critical Issues Summary

1. **Security Vulnerability**: Direct Python builtin access bypasses capability system
2. **Semantic Incorrectness**: Python builtins don't match ML specifications
3. **Accidental Success**: 31.2% of tests pass by coincidence, not design
4. **Missing Functions**: ML builtins don't exist in Python

### Recommended Action

**Implement Hybrid Approach** (Option C):
- Compile-time function call routing
- Auto-import of `mlpy.stdlib.builtin`
- Scope-aware transformation
- Defense-in-depth security

### Expected Outcomes

- **Integration Tests**: 31.2% → 100% pass rate
- **Security**: Zero Python builtin bypass vulnerabilities
- **Semantics**: 100% correct ML builtin behavior
- **Performance**: < 5% overhead
- **Maintainability**: Single registry, clear architecture

### Timeline

- **Phase 1 (Core)**: 2-3 hours - CRITICAL PRIORITY
- **Phase 2 (Scope)**: 1-2 hours - HIGH PRIORITY
- **Phase 3 (Security)**: 2-3 hours - HIGH PRIORITY
- **Phase 4 (Edge Cases)**: 1-2 hours - MEDIUM PRIORITY
- **Phase 5 (Docs)**: 1 hour - MEDIUM PRIORITY
- **Total**: 7-11 hours for complete implementation

### Next Steps

1. Review this proposal with team
2. Approve implementation approach
3. Begin Phase 1 (Core Implementation)
4. Run integration tests to validate
5. Proceed with remaining phases

---

**Proposal Status**: READY FOR IMPLEMENTATION
**Priority**: CRITICAL - Security & Correctness Issue
**Estimated Effort**: 7-11 hours
**Expected Impact**: HIGH - Fixes 68.8% test failures + security vulnerabilities
