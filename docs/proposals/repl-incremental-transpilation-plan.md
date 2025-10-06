# REPL Incremental Transpilation Implementation Plan

**Date:** 2025-01-07
**Target:** mlpy v2.3
**Goal:** Achieve <10ms average execution time (from current 75ms)

---

## Problem Analysis

### Current Hybrid Approach (v2.2)

```python
# In execute_ml_line()
all_ml_code = [stmt.ml_source for stmt in self.statements] + [ml_code]
full_ml_source = "\n".join(all_ml_code)

python_code = self.transpiler.transpile_to_python(
    full_ml_source, source_file=f"<repl:{len(self.statements)}>"
)
```

**Performance:** O(n) where n = number of previous statements
- Statement 1: Transpile 1 line (~10ms)
- Statement 10: Transpile 10 lines (~75ms)
- Statement 100: Transpile 100 lines (~750ms)

**Why we can't just transpile new code:**

The code generator validates all identifier references:

```python
# In PythonCodeGenerator.visit_identifier()
if not self._is_defined(identifier_name):
    raise CodeGenerationError(
        f"Unknown identifier '{identifier_name}' at line {node.line}. "
        f"Not a variable, function, parameter, import, or ML builtin."
    )
```

**Example failure:**
```ml
ml> nums = [1, 2, 3];  # Statement 1: nums defined
ml> len(nums);         # Statement 2: Transpile alone → Error: Unknown identifier 'nums'
```

---

## Solution Options

### Option 1: REPL Mode - Skip Validation ✅ **RECOMMENDED**

**Approach:** Add `repl_mode` flag to transpiler, skip undefined variable checks

**Rationale:**
- Python's runtime will catch truly undefined variables anyway
- IPython and other REPLs work this way
- Simplest implementation
- Fastest performance

**Changes Needed:**
```python
class MLTranspiler:
    def __init__(self, repl_mode: bool = False):
        self.repl_mode = repl_mode

class PythonCodeGenerator:
    def __init__(self, ..., repl_mode: bool = False):
        self.repl_mode = repl_mode

    def visit_identifier(self, node):
        name = node.value

        # Always check builtins and imports
        if self._is_builtin(name):
            return self._generate_builtin_call(name)
        if self._is_import(name):
            return name

        # In REPL mode: assume user variables exist
        # Python runtime will catch if they don't
        if self.repl_mode:
            return name

        # In normal mode: validate everything
        if not self._is_defined(name):
            raise UnknownIdentifierError(...)

        return name
```

**Pros:**
- ✅ Simple to implement (few lines of code)
- ✅ Fast (<10ms achievable)
- ✅ Proven pattern (used by IPython, etc.)
- ✅ Python provides error messages

**Cons:**
- ⚠️ Error messages less specific (Python NameError vs ML error with suggestions)
- ⚠️ Fails at runtime instead of transpile-time
- ⚠️ Might miss some typos earlier

---

### Option 2: Persistent Symbol Table

**Approach:** Maintain symbol table across executions, pass to transpiler

**Implementation:**
```python
class MLREPLSession:
    def __init__(self):
        self.repl_symbol_table = SymbolTable()

    def execute_ml_line(self, ml_code):
        # Transpile with known symbols
        python_code = self.transpiler.transpile_to_python(
            ml_code,
            known_symbols=self.repl_symbol_table
        )

        # Update symbol table after execution
        new_symbols = extract_symbols(python_code)
        self.repl_symbol_table.update(new_symbols)
```

**Pros:**
- ✅ Keep validation benefits
- ✅ Better error messages
- ✅ Catch typos at transpile-time

**Cons:**
- ❌ Complex implementation
- ❌ Symbol table can get out of sync with namespace
- ❌ Need to track variables, functions, classes separately
- ❌ What about deleted variables? (del x)

---

### Option 3: Context-Aware Transpilation

**Approach:** Extract context from previous statements, pass to transpiler

**Implementation:**
```python
@dataclass
class REPLContext:
    variables: set[str]
    functions: set[str]
    classes: set[str]
    imports: set[str]

def execute_ml_line(self, ml_code):
    # Build context from all previous statements
    context = REPLContext(
        variables={'x', 'y', 'nums'},
        functions={'add', 'fibonacci'},
        imports={'math', 'console'}
    )

    python_code = self.transpiler.transpile_to_python(
        ml_code,
        repl_context=context
    )
```

**Pros:**
- ✅ Clean separation of concerns
- ✅ Stateless transpiler

**Cons:**
- ❌ Complex context extraction
- ❌ Still O(n) to build context
- ❌ Context management overhead

---

## Recommended Approach: Option 1 (REPL Mode)

**Decision:** Implement REPL mode with skip validation

**Justification:**
1. **Performance:** Will achieve <10ms target
2. **Simplicity:** Minimal code changes
3. **Industry Standard:** How other REPLs work
4. **Error Handling:** Python errors are acceptable in REPL context

---

## Detailed Implementation Plan

### Phase 1: Transpiler Changes

**File:** `src/mlpy/ml/transpiler.py`

```python
class MLTranspiler:
    """ML to Python transpiler with optional REPL mode."""

    def __init__(
        self,
        enable_security: bool = True,
        enable_profiling: bool = False,
        repl_mode: bool = False,  # NEW
    ):
        """Initialize transpiler.

        Args:
            repl_mode: Enable REPL mode (skip undefined variable validation)
        """
        self.repl_mode = repl_mode
        # ... rest of init

    def transpile_to_python(
        self, ml_source: str, source_file: str = "<source>"
    ) -> tuple[str | None, list[Any], Any]:
        """Transpile ML to Python.

        In REPL mode, undefined variables are allowed (caught by Python runtime).
        """
        # ... existing parsing code

        # Pass repl_mode to code generator
        generator = PythonCodeGenerator(
            source_file=source_file,
            repl_mode=self.repl_mode  # NEW
        )

        # ... rest of transpilation
```

---

### Phase 2: Code Generator Changes

**File:** `src/mlpy/ml/codegen/python_generator.py`

**Change 1: Constructor**
```python
class PythonCodeGenerator:
    def __init__(
        self,
        source_file: str = "<source>",
        repl_mode: bool = False,  # NEW
    ):
        """Initialize code generator.

        Args:
            repl_mode: Skip undefined variable validation (for REPL)
        """
        self.repl_mode = repl_mode
        # ... existing init
```

**Change 2: Identifier Validation**

Find the `visit_identifier` or identifier resolution method:

```python
def visit_identifier(self, node):
    """Visit identifier node and generate Python code."""
    name = node.value

    # Priority 1: Check if it's a builtin function
    if self._is_ml_builtin(name):
        return name  # Builtin functions available directly

    # Priority 2: Check if it's an import
    if name in self.imports:
        return name

    # Priority 3: Check if it's in current scope
    if name in self.current_scope:
        return name

    # Priority 4: Check function parameters
    if self._is_parameter(name):
        return name

    # === REPL MODE: Assume variable exists ===
    if self.repl_mode:
        # Let Python runtime handle undefined variables
        return name

    # === NORMAL MODE: Strict validation ===
    # If we get here, identifier is unknown
    raise CodeGenerationError(
        f"Unknown identifier '{name}' at line {node.line}. "
        f"Not a variable, function, parameter, import, or ML builtin.\n\n"
        f"Possible causes:\n"
        f"  - Variable not yet defined\n"
        f"  - Typo in variable name\n"
        f"  - Missing import statement"
    )
```

**Change 3: Function Call Validation**

Similarly update function call validation:

```python
def visit_function_call(self, node):
    """Visit function call node."""
    func_name = node.function.value if hasattr(node.function, 'value') else None

    # Check if function is defined
    if not self.repl_mode:
        if func_name and not self._is_function_defined(func_name):
            raise CodeGenerationError(
                f"Unknown function '{func_name}' at line {node.line}"
            )

    # Generate call (REPL mode assumes it exists)
    # ... rest of code generation
```

---

### Phase 3: REPL Integration

**File:** `src/mlpy/cli/repl.py`

**Change: Use REPL Mode Transpiler**

```python
class MLREPLSession:
    def __init__(
        self,
        security_enabled: bool = True,
        profile: bool = False,
        max_history: int = 1000,
    ):
        # Create transpiler in REPL mode
        self.transpiler = MLTranspiler(
            enable_security=security_enabled,
            enable_profiling=profile,
            repl_mode=True,  # NEW: Enable REPL mode
        )
        # ... rest of init

    def execute_ml_line(self, ml_code: str) -> REPLResult:
        """Execute ML code with true incremental transpilation."""
        # ... validation code

        start_time = time.time()

        try:
            # === TRUE INCREMENTAL COMPILATION ===
            # Transpile ONLY the new ML code (not cumulative)
            python_code, issues, source_map = self.transpiler.transpile_to_python(
                ml_code,  # Just this line!
                source_file=f"<repl:{len(self.statements)}>"
            )

            # ... rest remains the same (execute in persistent namespace)
```

---

## Edge Cases & Handling

### 1. Undefined Variable (Desired Behavior)

**ML Code:**
```ml
ml> len(undefined_var)
```

**Before (Transpile Error):**
```
Error: Code generation failed: Unknown identifier 'undefined_var'
```

**After (Runtime Error):**
```python
>>> len(undefined_var)
NameError: name 'undefined_var' is not defined
```

**Formatting:**
```ml
Runtime Error: Variable 'undefined_var' is not defined
Tip: Make sure you've defined the variable before using it
```

### 2. Variable Defined in Same Statement

**ML Code:**
```ml
ml> x = 42; y = x + 10;
```

**Works:** Both `x` and `y` defined in same transpilation

### 3. Function Calling Undefined Function

**ML Code:**
```ml
ml> function caller() { return helper(); }
ml> caller();
```

**Behavior:** Fails at runtime when `caller()` is called
- This is acceptable REPL behavior
- User will see clear error message

### 4. Import Usage

**ML Code:**
```ml
ml> import math;
ml> math.sqrt(16);
```

**Works:** Code generator already tracks imports

---

## Security Analysis Implications

**Question:** Does REPL mode affect security analysis?

**Answer:** NO - Security analysis is independent

**Reason:**
- Security analyzer walks the AST
- Doesn't care about identifier resolution
- Looks for dangerous patterns (eval, exec, etc.)
- Works on single statement just fine

**Example:**
```ml
ml> x = eval("malicious code");
```

Even in REPL mode, security analyzer will detect `eval` usage.

---

## Performance Expectations

### Current (v2.2): Cumulative Transpilation

| Statements | Transpile Time | Cumulative |
|------------|----------------|------------|
| 1 | 10ms | 10ms |
| 10 | 75ms | 750ms |
| 50 | 375ms | 18,750ms |
| 100 | 750ms | 75,000ms |

**Average:** 75ms per statement

### Expected (v2.3): Incremental Transpilation

| Statements | Transpile Time | Cumulative |
|------------|----------------|------------|
| 1 | 5ms | 5ms |
| 10 | 5ms | 50ms |
| 50 | 5ms | 250ms |
| 100 | 5ms | 500ms |

**Average:** 5ms per statement

**Improvement:** **15x faster** (75ms → 5ms)

**Why <10ms?**
- No cumulative code concatenation
- No parsing of previous statements
- No validation of previous code
- Just transpile new statement

---

## Testing Strategy

### Unit Tests

**Test REPL Mode Flag:**
```python
def test_repl_mode_allows_undefined_variables():
    transpiler = MLTranspiler(repl_mode=True)
    code = "x + y;"  # x and y undefined

    python_code, issues, _ = transpiler.transpile_to_python(code)

    assert python_code is not None
    assert "x + y" in python_code

def test_normal_mode_rejects_undefined_variables():
    transpiler = MLTranspiler(repl_mode=False)
    code = "x + y;"

    python_code, issues, _ = transpiler.transpile_to_python(code)

    assert python_code is None  # Should fail
    assert any("Unknown identifier" in str(issue) for issue in issues)
```

### Integration Tests

**Test Incremental Execution:**
```python
def test_incremental_repl_execution():
    session = MLREPLSession()

    # Statement 1: Define variable
    result1 = session.execute_ml_line("x = 42;")
    assert result1.success

    # Statement 2: Use variable (incremental transpilation)
    result2 = session.execute_ml_line("y = x + 10;")
    assert result2.success

    # Statement 3: Use both variables
    result3 = session.execute_ml_line("x + y;")
    assert result3.success
    assert result3.value == 94  # 42 + 52

def test_undefined_variable_runtime_error():
    session = MLREPLSession()

    result = session.execute_ml_line("undefined_var;")

    assert not result.success
    assert "not defined" in result.error.lower()
```

### Performance Benchmarks

**Benchmark Script:**
```python
def benchmark_incremental_vs_cumulative():
    import time

    # Test incremental (v2.3)
    session_incremental = MLREPLSession()  # repl_mode=True
    start = time.time()
    for i in range(100):
        session_incremental.execute_ml_line(f"x{i} = {i};")
    incremental_time = (time.time() - start) * 1000

    print(f"Incremental: {incremental_time:.2f}ms for 100 statements")
    print(f"Average: {incremental_time/100:.2f}ms per statement")

    # Expected: ~500ms total (5ms average)
    assert incremental_time < 1000  # Should be under 1 second
```

---

## Risk Assessment

### Risk 1: Less Helpful Errors

**Impact:** Medium
**Probability:** High

**Example:**
```ml
# Typo: "nums" instead of "numbers"
ml> len(nums);
```

**Before:** `Error: Unknown identifier 'nums'. Did you mean 'numbers'?`
**After:** `NameError: name 'nums' is not defined`

**Mitigation:**
- Enhance error formatting for Python NameError
- Extract variable name from error message
- Suggest similar variables from namespace
- Still better than nothing

**Implementation:**
```python
def _format_runtime_error(self, error: Exception, ml_code: str):
    if isinstance(error, NameError):
        var_name = extract_variable_name(str(error))
        similar = find_similar_variables(var_name, self.python_namespace)

        msg = f"Variable '{var_name}' is not defined"
        if similar:
            msg += f"\nDid you mean: {', '.join(similar)}?"

        return REPLResult(success=False, error=msg)
```

### Risk 2: Function Reference Errors

**Impact:** Low
**Probability:** Medium

**Example:**
```ml
ml> function caller() { return helper(42); }
ml> caller();  # helper() doesn't exist
```

**Behavior:** Fails at runtime (acceptable)

**Mitigation:** Document expected behavior

### Risk 3: Security Analysis Gaps

**Impact:** Low
**Probability:** Low

**Analysis:**
- Security analyzer is independent of code generation
- Works on AST, not symbol table
- Should not be affected by REPL mode

**Validation:** Run full security test suite

---

## Implementation Checklist

### Code Changes
- [ ] Add `repl_mode` parameter to `MLTranspiler.__init__()`
- [ ] Pass `repl_mode` to `PythonCodeGenerator`
- [ ] Update `visit_identifier()` to skip validation in REPL mode
- [ ] Update `visit_function_call()` to skip validation in REPL mode
- [ ] Update `MLREPLSession` to use `repl_mode=True`
- [ ] Change `execute_ml_line()` to transpile only new code

### Testing
- [ ] Unit tests for REPL mode flag
- [ ] Unit tests for undefined variable handling
- [ ] Integration tests for incremental execution
- [ ] Performance benchmarks (target: <10ms avg)
- [ ] Security test suite (ensure no regressions)

### Documentation
- [ ] Update transpiler docstrings
- [ ] Document REPL mode behavior
- [ ] Add performance comparison
- [ ] Update REPL user guide

### Validation
- [ ] Run existing test suite (ensure no breaking changes)
- [ ] Run performance benchmarks
- [ ] Manual REPL testing
- [ ] Security audit

---

## Expected Outcome

**Performance:**
- Average execution: 75ms → **5ms** (15x improvement)
- Target achieved: <10ms ✅

**Functionality:**
- All existing REPL features maintained
- True incremental compilation
- Python-level error messages (acceptable)

**Trade-offs:**
- Less specific error messages (Python vs ML)
- Runtime errors instead of transpile-time
- Industry-standard behavior (same as IPython)

---

## Recommendation

✅ **PROCEED with Option 1 (REPL Mode)**

**Rationale:**
1. Simplest implementation (minimal code changes)
2. Achieves performance target (<10ms)
3. Industry-standard approach
4. Acceptable trade-offs for REPL context

**Estimated Effort:** 4-6 hours
- 2 hours: Transpiler changes
- 1 hour: REPL integration
- 1 hour: Testing
- 1 hour: Documentation

**Expected Results:**
- 15x performance improvement
- <10ms average execution time
- Production-ready v2.3 release

---

**Next Steps:**
1. Review this plan
2. Implement transpiler changes
3. Update REPL integration
4. Test and benchmark
5. Document and release v2.3
