# Whitelist Security Vulnerabilities Report

**Date**: January 2025
**Status**: CRITICAL ISSUES IDENTIFIED
**Priority**: IMMEDIATE ACTION REQUIRED

---

## Executive Summary

Investigation of the mlpy whitelist enforcement system has revealed **CRITICAL security vulnerabilities** that allow complete bypass of the compile-time whitelist through runtime execution paths. An attacker can execute arbitrary Python code, access the filesystem, and import restricted modules.

**Severity**: 🔴 **CRITICAL** - Complete security bypass possible
**Affected Components**: builtin.call(), REPL execution, runtime validation
**Attack Complexity**: LOW - Simple one-liner exploits
**User Interaction**: NONE - Can be embedded in ML code

---

## Vulnerability 1: builtin.call() Runtime Bypass

### Classification
- **Severity**: 🔴 **CRITICAL**
- **CWE**: CWE-502 (Deserialization of Untrusted Data) / CWE-20 (Improper Input Validation)
- **CVSS Score**: 9.8 (Critical)

### Description

The `builtin.call()` function accepts ANY callable and executes it without validating against the whitelist. This completely bypasses compile-time security checks.

### Location
- **File**: `src/mlpy/stdlib/builtin.py`
- **Lines**: 463-492
- **Function**: `Builtin.call()`

### Vulnerable Code
```python
@ml_function(description="Call function dynamically with arguments", capabilities=[])
def call(self, func: Callable, *args, **kwargs) -> Any:
    """Call function dynamically with arguments."""
    if not callable(func):
        raise TypeError(f"'{type(func).__name__}' object is not callable")

    return func(*args, **kwargs)  # ⚠️ NO WHITELIST CHECK!
```

### Proof of Concept

#### Exploit 1: Execute eval() via call()
```javascript
// ML Code (SHOULD BE BLOCKED)
builtin.call(eval, "print('Security bypassed!')");
```

**Result**: Executes arbitrary Python code

#### Exploit 2: File system access via open()
```javascript
// ML Code (SHOULD BE BLOCKED)
let file = builtin.call(open, "secrets.txt");
builtin.call(print, file.read());
```

**Result**: Reads arbitrary files from filesystem

#### Exploit 3: Import system bypass via __import__
```javascript
// ML Code (SHOULD BE BLOCKED)
let os = builtin.call(__import__, "os");
builtin.call(os.system, "ls -la");
```

**Result**: Executes arbitrary shell commands

### Root Cause

The `call()` function was designed for functional programming patterns but assumes the function argument is already validated. However:

1. Compile-time validation only checks function NAMES (e.g., `eval()` is blocked)
2. But `call(eval, ...)` passes because:
   - `call` is whitelisted as a builtin
   - `eval` as an argument is just an identifier, not a call
3. At runtime, `call()` receives the Python builtin `eval` function and executes it

### Impact Assessment

| Impact Category | Severity | Details |
|----------------|----------|---------|
| **Code Execution** | CRITICAL | Can execute arbitrary Python via eval/exec |
| **File System Access** | CRITICAL | Can read/write files via open() |
| **Module Import** | CRITICAL | Can import any Python module via __import__ |
| **Capability Bypass** | CRITICAL | Bypasses entire capability system |
| **Data Exfiltration** | HIGH | Can access sensitive data and send it externally |

---

## Vulnerability 2: REPL __builtins__ Exposure

### Classification
- **Severity**: 🔴 **HIGH**
- **CWE**: CWE-749 (Exposed Dangerous Method or Function)
- **CVSS Score**: 8.6 (High)

### Description

The REPL execution environment exposes Python's `__builtins__` directly in the namespace, making ALL Python built-in functions accessible, completely bypassing the whitelist.

### Location
- **File**: `src/mlpy/cli/repl.py`
- **Lines**: 59-62
- **Function**: `MLREPLSession._init_namespace()`

### Vulnerable Code
```python
def _init_namespace(self):
    """Initialize the Python namespace with standard library imports."""
    # Add standard Python built-ins that ML code might use
    self.python_namespace["__builtins__"] = __builtins__  # ⚠️ EXPOSES ALL PYTHON BUILTINS!
```

### Proof of Concept

**REPL Session**:
```
ml> builtin.call(help);
Welcome to Python's help system!  # ⚠️ Python help, not ML help

ml> builtin.call(eval, "2 + 2");
=> 4  # ⚠️ Arbitrary code execution

ml> builtin.call(open, "file.txt");
=> <_io.TextIOWrapper ...>  # ⚠️ File access
```

### Root Cause

The REPL was designed to support Python interoperability but inadvertently exposed the entire Python standard library through `__builtins__`. When combined with Vulnerability 1 (call() bypass), this creates a complete security hole.

### Impact Assessment

| Impact Category | Severity | Details |
|----------------|----------|---------|
| **REPL Security** | CRITICAL | REPL has no security enforcement |
| **Development Risk** | HIGH | Developers might accidentally use unsafe functions |
| **Production Risk** | MEDIUM | REPL typically not used in production |
| **Testing Impact** | HIGH | Security tests in REPL don't reflect actual security |

---

## Vulnerability 3: Variable Function Call Validation Mismatch

### Classification
- **Severity**: 🟡 **MEDIUM**
- **CWE**: CWE-704 (Incorrect Type Conversion or Cast)
- **CVSS Score**: 5.3 (Medium)

### Description

The compiler performs NAME-based whitelist validation on function calls, not CONTENT-based validation. This prevents legitimate use cases (storing whitelisted functions in variables) while not preventing actual attacks (via call() bypass).

### Location
- **File**: `src/mlpy/ml/codegen/python_generator.py`
- **Lines**: 686-696, 1111-1140
- **Functions**: `_generate_expression()`, `_generate_simple_function_call()`

### Vulnerable Code
```python
elif isinstance(expr, FunctionCall):
    if isinstance(expr.function, Identifier):
        # Checks if the IDENTIFIER NAME is in whitelist
        return self._generate_simple_function_call(expr.function.name, expr.arguments)
```

### Proof of Concept

#### Scenario 1: Legitimate code fails
```javascript
// ML Code
let myLen = builtin.len;  // Store whitelisted function
let result = myLen([1, 2, 3]);  // ❌ FAILS: "myLen not in whitelist"
```

**Expected**: Should work (len is whitelisted)
**Actual**: Compilation error

#### Scenario 2: Attack succeeds via call()
```javascript
// ML Code
builtin.call(eval, "malicious()");  // ✅ SUCCEEDS via different vulnerability
```

### Root Cause

Mismatch between compile-time and runtime validation:
- **Compile-time**: Checks if variable NAME is a known function
- **Runtime**: No validation of what the variable contains
- **Bypass**: Use call() to invoke functions without naming them

### Impact Assessment

| Impact Category | Severity | Details |
|----------------|----------|---------|
| **Developer Experience** | MEDIUM | Cannot use functional programming patterns |
| **Security Effectiveness** | LOW | Doesn't prevent actual attacks |
| **False Security** | MEDIUM | Gives impression of security without providing it |

---

## Vulnerability 4: getattr() Security Status Unknown

### Classification
- **Severity**: 🟠 **NEEDS INVESTIGATION**
- **CWE**: CWE-266 (Incorrect Privilege Assignment)
- **CVSS Score**: TBD (Pending investigation)

### Description

The `builtin.getattr()` function routes through `SafeAttributeRegistry`, but its effectiveness against determined attackers is unclear. Combined with call(), it might enable additional bypasses.

### Location
- **File**: `src/mlpy/stdlib/builtin.py`
- **Lines**: 424-462
- **Function**: `Builtin.getattr()`

### Code to Investigate
```python
@ml_function(description="Get safe attribute from object", capabilities=[])
def getattr(self, obj: Any, name: str, default: Any = None) -> Any:
    # Block ALL dunder attributes immediately
    if name.startswith('_'):
        return default

    registry = get_safe_registry()
    try:
        return registry.safe_attr_access(obj, name)
    except (AttributeError, Exception):
        return default
```

### Potential Attack Vectors

```javascript
// Test 1: getattr + call chain
let method = builtin.getattr(some_obj, "dangerous_method");
builtin.call(method);  // Does this work?

// Test 2: Accessing non-whitelisted attributes
let hidden = builtin.getattr(some_obj, "secret_data");

// Test 3: Module introspection
let module_dict = builtin.getattr(math, "__dict__");
```

### Required Investigation

1. ✅ Does SafeAttributeRegistry block __class__, __globals__, __dict__?
2. ❓ Can getattr() return non-whitelisted functions?
3. ❓ What happens when getattr() result is passed to call()?
4. ❓ Can we access module internals via getattr()?
5. ❓ Are there any reflection paths through getattr()?

---

## Architecture Analysis: Compile-time vs Runtime

### Current Architecture (BROKEN)

```
┌─────────────────────────────────────────────────────────────┐
│                     ML Source Code                           │
│  • Direct calls: len([1,2,3])                               │
│  • Bypass: builtin.call(eval, "code")                      │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              Compile-Time Whitelist Enforcement              │
│  ✅ Blocks: eval(), exec(), open(), __import__()            │
│  ✅ Allows: builtin.call(...)                              │
│  ❌ PROBLEM: Doesn't validate arguments!                    │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  Generated Python Code                       │
│  builtin.call(eval, "malicious code")                      │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Runtime Execution                         │
│  ❌ NO VALIDATION - executes anything!                      │
│  ❌ REPL has full __builtins__ access                      │
└─────────────────────────────────────────────────────────────┘
```

### Required Architecture (DEFENSE IN DEPTH)

```
┌─────────────────────────────────────────────────────────────┐
│                     ML Source Code                           │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│         Layer 1: Compile-Time Whitelist (CURRENT)            │
│  • Block direct dangerous calls                              │
│  • Register user-defined functions                           │
│  • Track imported modules                                    │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│         Layer 2: Code Generation Hardening (NEW)             │
│  • Embed whitelist in generated code                         │
│  • Add runtime validation wrappers                           │
│  • Generate capability checks                                │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│         Layer 3: Runtime Whitelist Validation (NEW)          │
│  • builtin.call() validates against whitelist                │
│  • getattr() enforces SafeAttributeRegistry                  │
│  • Function calls check AllowedFunctionsRegistry             │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│         Layer 4: Sandbox Restrictions (CURRENT)              │
│  • Process isolation                                         │
│  • Resource limits                                           │
│  • Restricted __builtins__                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Recommended Fixes

### Priority 1: IMMEDIATE (Critical Fixes)

#### Fix 1.1: Secure builtin.call()

**File**: `src/mlpy/stdlib/builtin.py:463-492`

```python
@ml_function(description="Call function dynamically with arguments", capabilities=[])
def call(self, func: Callable, *args, **kwargs) -> Any:
    """Call function dynamically with arguments.

    SECURITY: Validates function against whitelist before execution.
    """
    if not callable(func):
        raise TypeError(f"'{type(func).__name__}' object is not callable")

    # NEW: Validate function against whitelist
    from mlpy.ml.codegen.allowed_functions_registry import AllowedFunctionsRegistry

    # Check if function is a whitelisted builtin
    func_name = getattr(func, '__name__', None)

    # Block Python built-in functions that aren't in ML whitelist
    if func_name and func.__module__ == 'builtins':
        registry = AllowedFunctionsRegistry()
        if not registry.is_allowed_builtin(func_name):
            raise SecurityError(
                f"Cannot call Python builtin '{func_name}' - not in ML whitelist. "
                f"Only whitelisted ML builtin functions can be called dynamically."
            )

    # Check if function is from a non-whitelisted module
    if hasattr(func, '__module__') and func.__module__:
        # Allow user-defined functions (no module or __main__)
        if func.__module__ not in ('__main__', None):
            # Check if it's from a whitelisted ML stdlib module
            # TODO: Validate against imported modules registry
            pass

    return func(*args, **kwargs)
```

#### Fix 1.2: Secure REPL __builtins__

**File**: `src/mlpy/cli/repl.py:59-62`

```python
def _init_namespace(self):
    """Initialize the Python namespace with standard library imports."""
    # Create RESTRICTED __builtins__ with only safe functions
    from mlpy.ml.codegen.allowed_functions_registry import AllowedFunctionsRegistry

    registry = AllowedFunctionsRegistry()
    restricted_builtins = {}

    # Only include builtins that are in ML whitelist
    # (These should map to ML builtin equivalents)
    safe_builtins = {
        'True': True,
        'False': False,
        'None': None,
        # Explicitly do NOT include: eval, exec, compile, open, __import__
    }

    self.python_namespace["__builtins__"] = safe_builtins

    # Pre-import ML stdlib modules (already safe)
    # ... rest of code
```

### Priority 2: ENHANCEMENT (Runtime Validation)

#### Fix 2.1: Runtime Whitelist System

Create new file: `src/mlpy/runtime/whitelist_validator.py`

```python
"""Runtime whitelist validation system.

Validates dynamic function calls against compile-time whitelist.
"""

class RuntimeWhitelistValidator:
    """Validates function calls at runtime against whitelist."""

    def __init__(self, allowed_functions_registry):
        self.registry = allowed_functions_registry

    def validate_function_call(self, func, context="unknown"):
        """Validate that function is allowed to be called.

        Args:
            func: Function to validate
            context: Where the call is happening (for error messages)

        Raises:
            SecurityError: If function is not whitelisted
        """
        # Implementation
        pass
```

#### Fix 2.2: Pass Whitelist to Runtime

Modify code generator to embed whitelist in generated code:

```python
# Generated Python code should include:
_ALLOWED_FUNCTIONS = {"len", "print", "range", ...}
_ALLOWED_MODULES = {"math": ["sqrt", "abs"], ...}

# Runtime helpers use this for validation
```

### Priority 3: TESTING (Comprehensive Validation)

#### Test 3.1: Security Bypass Test Suite

Create: `tests/security/test_whitelist_bypasses.py`

```python
"""Test suite for whitelist bypass attempts.

All these tests should FAIL (be blocked by security).
"""

def test_call_bypass_eval():
    """Attempt to call eval via builtin.call() should be blocked."""
    code = 'builtin.call(eval, "2+2");'
    with pytest.raises(SecurityError):
        transpile_and_execute(code)

def test_call_bypass_exec():
    """Attempt to call exec via builtin.call() should be blocked."""
    code = 'builtin.call(exec, "import os");'
    with pytest.raises(SecurityError):
        transpile_and_execute(code)

def test_call_bypass_open():
    """Attempt to call open via builtin.call() should be blocked."""
    code = 'builtin.call(open, "file.txt");'
    with pytest.raises(SecurityError):
        transpile_and_execute(code)

# ... many more tests
```

---

## Timeline for Remediation

### Week 1: Critical Fixes
- [ ] Day 1-2: Fix builtin.call() validation
- [ ] Day 3-4: Fix REPL __builtins__ exposure
- [ ] Day 5: Create security bypass test suite
- [ ] Day 6-7: Test and verify fixes

### Week 2: Runtime Enhancement
- [ ] Day 1-3: Implement RuntimeWhitelistValidator
- [ ] Day 4-5: Modify code generator to embed whitelist
- [ ] Day 6-7: Integration testing

### Week 3: Comprehensive Testing
- [ ] Day 1-3: Expand security test suite
- [ ] Day 4-5: Penetration testing
- [ ] Day 6-7: Documentation and review

---

## Conclusion

The current whitelist implementation has **CRITICAL security vulnerabilities** that allow complete bypass through runtime execution paths. The `builtin.call()` function and REPL `__builtins__` exposure create a security hole that undermines the entire compile-time whitelist system.

**Immediate action required** to:
1. Fix `builtin.call()` to validate functions before execution
2. Secure REPL by restricting `__builtins__`
3. Implement runtime whitelist validation as defense-in-depth

Without these fixes, the security promises of mlpy's whitelist system are **false security** - giving users a false sense of protection while remaining vulnerable to trivial exploits.

---

**Report Status**: COMPLETE
**Next Action**: Begin Priority 1 fixes immediately
**Follow-up**: Create runtime-whitelist-enforcement-proposal.md with detailed design
