# Runtime Validation: Unified Implementation Proposal

**Date**: January 2025
**Status**: FINAL DESIGN - Ready for Implementation
**Supersedes**: All previous safe_call exploration documents

---

## Rationale

### The Security Problem

Investigation revealed **CRITICAL vulnerabilities** in the compile-time whitelist enforcement:

1. **`builtin.call()` bypass**: Can execute any Python function
   ```javascript
   builtin.call(eval, "malicious_code");  // Executes!
   builtin.call(open, "secrets.txt");     // File access!
   ```

2. **Variable function storage**: Validation checks variable NAME, not contents
   ```javascript
   let m = help;
   m();  // Fails: "m not in whitelist" (checking wrong thing)
   ```

3. **REPL `__builtins__` exposure**: Python builtins directly accessible
   ```python
   # In REPL:
   builtin.call(eval, "code")  // Works because eval is in __builtins__
   ```

**Root Cause**: Compile-time validation only checks function NAMES at call sites, but cannot validate:
- What a variable contains at runtime
- What function is passed as an argument
- What Python builtins are accessible in the namespace

### Why Runtime Validation is Required

**Compile-time cannot protect against**:
- Dynamic function calls through variables
- Functions passed as arguments to other functions
- Python builtins leaking into the namespace
- Higher-order function attacks

**Solution**: Every function call must be validated at runtime, not just compile-time.

### Why Decorator-Based Approach is Superior

We considered two approaches:

#### Approach A: Whitelist Embedding (Rejected)
```python
# Generated code embeds entire whitelist:
_ALLOWED_BUILTIN_NAMES = {'len', 'print', 'range', ...}  # 50+ names
_ALLOWED_MODULES = {
    'math': {'sqrt', 'sin', ...},  # All functions
    'string': {'upper', 'lower', ...},
}
_ALLOWED_CAPABILITIES = {
    'len': [],
    'file.read': ['FILE_READ'],
    # ... duplicate of decorator data
}

# Create validator per file:
_validator = RuntimeWhitelistValidator(_ALLOWED_BUILTIN_NAMES, ...)
```

**Problems**:
- ❌ 10KB+ overhead per generated file
- ❌ Duplicates metadata already in decorators
- ❌ Must keep whitelist synchronized with decorators
- ❌ Capability data duplicated

#### Approach B: Decorator-Based (Selected) ✅
```python
# Generated code is minimal:
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

# Validation uses existing decorator metadata:
def safe_call(func, *args, **kwargs):
    if hasattr(func, '_ml_function_metadata'):
        # Extract capabilities from decorator
        required_caps = metadata.get('capabilities', [])
        if required_caps:
            check_capabilities(required_caps)
        return func(*args, **kwargs)
```

**Advantages**:
- ✅ ~60 bytes overhead per file (single import)
- ✅ Single source of truth (decorators)
- ✅ Capability data already in `@ml_function`
- ✅ Auto-updates when decorators change
- ✅ Simpler implementation (~150 lines vs ~500 lines)

---

## Design Overview

### Validation Strategy

**Wrap ALL function calls** (except user-defined within same file) with `_safe_call()`:

```python
# Instead of:  func(args)
# Generate:    _safe_call(func, args)
```

**Wrapping Rules**:

| Call Type | Example | Wrapped? | Validation |
|-----------|---------|----------|------------|
| User-defined function | `myFunc(x)` | ❌ NO | Trusted (same file) |
| ML builtin | `builtin.len([])` | ✅ YES | Check `_ml_function_metadata` |
| Module function | `math.sqrt(x)` | ✅ YES | Check `_ml_function_metadata` |
| Variable (unknown) | `m = len; m([])` | ✅ YES | Runtime check contents |
| Method call | `str.upper()` | ✅ YES | Combined attr + call check |
| Nested call | `foo(bar())` | ✅ YES (inner) | bar() wrapped |

### Validation Logic Flow

```
Function Call: _safe_call(func, args)
    │
    ├─→ Has _ml_function_metadata?
    │   ├─→ YES: Extract capabilities from metadata
    │   │         ├─→ Capabilities required?
    │   │         │   ├─→ YES: check_capabilities()
    │   │         │   │       ├─→ Available: EXECUTE ✓
    │   │         │   │       └─→ Missing: CapabilityError ✗
    │   │         │   └─→ NO: EXECUTE ✓
    │   │
    │   └─→ NO: Check func.__module__
    │           ├─→ __main__ or None: User-defined → EXECUTE ✓
    │           ├─→ Bound method on str/list/dict: Safe type → EXECUTE ✓
    │           ├─→ Method on @ml_class object: Decorated class → EXECUTE ✓
    │           └─→ Otherwise: NOT WHITELISTED → SecurityError ✗
```

---

## Detailed Implementation Specification

### Component 1: Runtime Validator Module

**File**: `src/mlpy/runtime/whitelist_validator.py` (NEW)

**Purpose**: Single global `safe_call()` function that validates all function calls

**Size**: ~200 lines

**Full Implementation**:

```python
"""Decorator-based runtime whitelist validator with capability checking.

This module provides runtime validation of function calls by checking for
@ml_function decorator metadata and validating required capabilities.

Key Features:
- Whitelist enforcement via decorator checking
- Runtime capability validation
- Thread-safe capability context management
- Clear error messages for debugging

Author: mlpy development team
Version: 2.0.0
License: MIT
"""

from typing import Any, Callable, List, Optional
import threading


class SecurityError(Exception):
    """Raised when a non-whitelisted function call is attempted.

    This indicates that a function without @ml_function decorator
    was called from outside the user's ML code.
    """
    pass


class CapabilityError(Exception):
    """Raised when required capabilities are not available.

    This indicates that a function requires specific permissions
    that have not been granted in the current execution context.
    """
    pass


# Thread-local storage for capability context
_capability_context = threading.local()


# Safe built-in types whose methods don't require decoration
# (already validated by SafeAttributeRegistry, no dunder access)
_SAFE_BUILTIN_TYPES = (str, list, dict, int, float, bool, tuple, set, frozenset)


def get_current_capability_context():
    """Get the current capability context for this thread.

    Returns:
        CapabilityContext instance or None if no context is set

    Thread Safety:
        Uses thread-local storage, safe for concurrent execution
    """
    return getattr(_capability_context, 'context', None)


def set_capability_context(context):
    """Set the capability context for this thread.

    Args:
        context: CapabilityContext instance or None to clear

    Thread Safety:
        Sets context in thread-local storage
    """
    _capability_context.context = context


def check_capabilities(required: List[str]) -> None:
    """Check if current context has required capabilities.

    Args:
        required: List of required capability types (e.g., ["FILE_READ"])

    Raises:
        CapabilityError: If any required capability is not available

    Example:
        check_capabilities(["FILE_READ", "FILE_WRITE"])
    """
    if not required:
        # No capabilities required
        return

    # Get current context
    context = get_current_capability_context()

    if not context:
        # No context but capabilities are required
        raise CapabilityError(
            f"Function requires capabilities {required}, but no capability context is active.\n"
            f"\n"
            f"This function needs specific permissions that are not available.\n"
            f"Make sure to run this code within a proper capability context:\n"
            f"\n"
            f"  from mlpy.runtime.capabilities import CapabilityContext\n"
            f"  with CapabilityContext() as ctx:\n"
            f"      # Grant required capabilities\n"
            f"      ctx.add_capability(...)\n"
            f"      # Execute your code here\n"
        )

    # Check each required capability
    missing = []
    for cap_type in required:
        if not context.has_capability(cap_type):
            missing.append(cap_type)

    if missing:
        # Get available capabilities for error message
        available = []
        for cap_type in context.get_all_capabilities():
            available.append(cap_type)

        raise CapabilityError(
            f"Missing required capabilities: {missing}\n"
            f"Available capabilities: {available}\n"
            f"\n"
            f"This function requires permissions that have not been granted.\n"
            f"Add these capabilities to your execution context:\n"
            f"\n"
            f"  ctx.add_capability(CapabilityType(...))\n"
        )


def safe_call(func: Callable, *args, **kwargs) -> Any:
    """Validate and execute function call with whitelist and capability checking.

    This is the core security function that enforces the runtime whitelist.
    Every function call in generated ML code goes through this validator.

    Validation Rules:
    1. Function decorated with @ml_function → Check capabilities, then allow
    2. User-defined function (module __main__) → Allow (trusted)
    3. Method on safe built-in type (str, list, etc.) → Allow (pre-validated)
    4. Method on @ml_class decorated object → Allow
    5. Everything else → Block with SecurityError

    Args:
        func: Function/callable to validate and execute
        *args: Positional arguments to pass to function
        **kwargs: Keyword arguments to pass to function

    Returns:
        Result of function call if validation passes

    Raises:
        TypeError: If func is not callable
        SecurityError: If func is not whitelisted (missing @ml_function decorator)
        CapabilityError: If required capabilities are not available

    Examples:
        # ML builtin (decorated, no capabilities):
        safe_call(builtin.len, [1, 2, 3])  # ✅ Returns 3

        # ML stdlib (decorated, with capabilities):
        safe_call(file.read, "/data/file.txt")  # ✅ If FILE_READ available
                                                 # ❌ CapabilityError if not

        # User function (trusted):
        def my_func(x): return x * 2
        safe_call(my_func, 21)  # ✅ Returns 42

        # Python builtin (not decorated):
        safe_call(eval, "2+2")  # ❌ SecurityError

    Security:
        - Blocks all Python builtins (eval, exec, open, __import__, etc.)
        - Blocks functions from non-whitelisted modules
        - Enforces capability requirements at runtime
        - Prevents sandbox escape via dynamic calls
    """
    # Step 1: Type validation
    if not callable(func):
        func_type = type(func).__name__
        raise TypeError(
            f"Cannot call object of type '{func_type}': not callable\n"
            f"Expected a function, got {func_type}"
        )

    # Step 2: Check for @ml_function decorator metadata (PRIMARY CHECK)
    if hasattr(func, '_ml_function_metadata'):
        metadata = func._ml_function_metadata

        # Extract required capabilities from decorator
        required_caps = metadata.get('capabilities', [])

        # Validate capabilities if any are required
        if required_caps:
            check_capabilities(required_caps)

        # Function is whitelisted and capabilities satisfied
        return func(*args, **kwargs)

    # Step 3: Check if user-defined function (TRUSTED)
    func_module = getattr(func, '__module__', None)
    if func_module in ('__main__', None):
        # User-defined functions are trusted within the same file
        # They don't need decoration or capability checks
        # (Capability checks happen at @ml_function boundaries inside them)
        return func(*args, **kwargs)

    # Step 4: Check if method on safe built-in type
    if hasattr(func, '__self__'):
        # This is a bound method
        obj = func.__self__
        obj_type = type(obj)

        if obj_type in _SAFE_BUILTIN_TYPES:
            # Method on safe built-in type (str.upper, list.append, etc.)
            # These are pre-validated by SafeAttributeRegistry
            # Dunder methods are blocked by _safe_attr_access
            return func(*args, **kwargs)

        # Check if method on @ml_class decorated object
        if hasattr(obj_type, '_ml_class_metadata'):
            # Method on ML-decorated class instance
            # TODO: Future enhancement - check method-level capabilities?
            return func(*args, **kwargs)

    # Step 5: Check if unbound method on safe type
    if hasattr(func, '__objclass__'):
        objclass = func.__objclass__
        if objclass in _SAFE_BUILTIN_TYPES:
            # Unbound method on safe type
            return func(*args, **kwargs)

    # Step 6: Not whitelisted → BLOCK
    func_name = getattr(func, '__name__', '<unknown>')
    func_module_str = func_module if func_module else '<unknown>'

    raise SecurityError(
        f"SecurityError: Cannot call '{func_name}' from module '{func_module_str}'\n"
        f"\n"
        f"This function is NOT decorated with @ml_function.\n"
        f"\n"
        f"Allowed function sources:\n"
        f"  ✓ ML stdlib functions (decorated with @ml_function)\n"
        f"  ✓ User-defined functions (defined in your ML code)\n"
        f"  ✓ Methods on safe types (str, list, dict, etc.)\n"
        f"  ✓ Methods on @ml_class decorated objects\n"
        f"\n"
        f"Python built-in functions are BLOCKED for security:\n"
        f"  ✗ eval, exec, compile - Code execution risk\n"
        f"  ✗ open, __import__ - File/module access requires capabilities\n"
        f"  ✗ getattr, setattr, delattr - Use ML builtin equivalents\n"
        f"  ✗ help, dir, vars - Use ML builtin equivalents\n"
        f"\n"
        f"How to fix:\n"
        f"  • Use ML builtins: builtin.len() instead of len()\n"
        f"  • Import ML modules: import math; math.sqrt()\n"
        f"  • Define in ML: function {func_name}(...) {{ ... }}\n"
    )


__all__ = [
    'safe_call',
    'SecurityError',
    'CapabilityError',
    'get_current_capability_context',
    'set_capability_context',
    'check_capabilities',
]
```

**Key Design Decisions**:
1. **Single function**: One `safe_call()` handles all validation
2. **No state**: Pure function (except thread-local context)
3. **Decorator-driven**: Primary check is `hasattr(func, '_ml_function_metadata')`
4. **Capability-ready**: Extracts and checks capabilities from metadata
5. **Clear errors**: Detailed messages guide users to fix issues

---

### Component 2: Fix builtin.call() to Use safe_call

**File**: `src/mlpy/stdlib/builtin.py` (MODIFY)

**Current Code** (VULNERABLE):
```python
@ml_function(description="Call function dynamically with arguments", capabilities=[])
def call(self, func: Callable, *args, **kwargs) -> Any:
    """Call function dynamically with arguments."""
    if not callable(func):
        raise TypeError(f"'{type(func).__name__}' object is not callable")

    return func(*args, **kwargs)  # ❌ NO VALIDATION!
```

**New Code** (SECURE):
```python
@ml_function(description="Call function dynamically with arguments", capabilities=[])
def call(self, func: Callable, *args, **kwargs) -> Any:
    """Call function dynamically with arguments.

    SECURITY: Uses safe_call to validate function before execution.
    This prevents execution of non-whitelisted functions passed as arguments.

    Args:
        func: Callable to invoke
        *args: Positional arguments
        **kwargs: Keyword arguments

    Returns:
        Result of function call

    Raises:
        TypeError: If func is not callable
        SecurityError: If func is not whitelisted
        CapabilityError: If required capabilities not available

    Examples:
        call(math.abs, -5) => 5
        call(string.upper, "hello") => "HELLO"
        call(eval, "code") => SecurityError (BLOCKED!)

    Security:
        Prevents these attacks:
        - call(eval, "malicious") - Blocked
        - call(open, "secrets.txt") - Blocked
        - call(__import__, "os") - Blocked
    """
    # Import here to avoid circular dependency at module load time
    from mlpy.runtime.whitelist_validator import safe_call

    # Delegate to safe_call for validation and execution
    return safe_call(func, *args, **kwargs)
```

**Testing**:
```python
# Before fix:
builtin.call(eval, "2+2")  # ✅ Executes! (VULNERABLE)

# After fix:
builtin.call(eval, "2+2")  # ❌ SecurityError (SECURE)
```

---

### Component 3: Code Generator Modifications

**File**: `src/mlpy/ml/codegen/python_generator.py` (MODIFY)

#### Modification 1: Add safe_call Import to Generated Code

**Location**: `generate()` method header generation

**Current Code**:
```python
def generate(self, ast: Program) -> tuple[str, dict[str, Any] | None]:
    """Generate Python code from ML AST."""
    # Reset state
    self.context = CodeGenerationContext()
    self.output_lines = []
    self.function_registry = AllowedFunctionsRegistry()

    # Generate header
    self.output_lines.append('"""Generated Python code from ML source."""')
    self.output_lines.append('')

    # ... rest of generation
```

**New Code**:
```python
def generate(self, ast: Program) -> tuple[str, dict[str, Any] | None]:
    """Generate Python code from ML AST."""
    # Reset state
    self.context = CodeGenerationContext()
    self.output_lines = []
    self.function_registry = AllowedFunctionsRegistry()

    # Generate header
    self.output_lines.append('"""Generated Python code from ML source."""')
    self.output_lines.append('')

    # NEW: Add runtime validator import
    self._generate_runtime_imports()

    # ... rest of generation


def _generate_runtime_imports(self):
    """Generate runtime validator import at top of file."""
    self.output_lines.extend([
        "# ============================================================================",
        "# Runtime Whitelist Enforcement",
        "# ============================================================================",
        "from mlpy.runtime.whitelist_validator import safe_call as _safe_call",
        "",
    ])
```

#### Modification 2: Wrap Function Calls with _safe_call

**Location**: `_generate_expression()` method, FunctionCall handling

**Current Code**:
```python
def _generate_expression(self, expr) -> str:
    """Generate Python expression from ML expression node."""
    # ... other cases ...

    elif isinstance(expr, FunctionCall):
        # Handle different function call types
        if isinstance(expr.function, MemberAccess):
            return self._generate_member_function_call(expr.function, expr.arguments)
        elif isinstance(expr.function, Identifier):
            return self._generate_simple_function_call(expr.function.name, expr.arguments)
        else:
            # Expression returning function
            func_code = self._generate_expression(expr.function)
            args = [self._generate_expression(arg) for arg in expr.arguments]
            args_str = ', '.join(args)
            return f"{func_code}({args_str})"
```

**New Code**:
```python
def _generate_expression(self, expr) -> str:
    """Generate Python expression from ML expression node."""
    # ... other cases ...

    elif isinstance(expr, FunctionCall):
        # NEW: Use unified function call generation with wrapping
        return self._generate_function_call_wrapped(expr)
```

#### Modification 3: New Helper - Determine if Wrapping Needed

**Location**: New method in PythonGenerator class

```python
def _should_wrap_call(self, func_expr) -> bool:
    """Determine if function call should be wrapped with _safe_call.

    Wrapping Rules:
    - User-defined functions: NO (trusted)
    - Everything else: YES (needs validation)

    Args:
        func_expr: Function expression node (Identifier, MemberAccess, etc.)

    Returns:
        True if call should be wrapped with _safe_call
    """
    # Case 1: Simple identifier (function name)
    if isinstance(func_expr, Identifier):
        func_name = func_expr.name

        # Check if it's a user-defined function
        if self.function_registry.is_user_defined(func_name):
            return False  # User-defined, don't wrap

        # Unknown identifier (could be variable) - wrap it
        return True

    # Case 2: Member access (module.func or obj.method)
    elif isinstance(func_expr, MemberAccess):
        # Always wrap - validation will check decorator/safe type
        return True

    # Case 3: Any other expression (nested call, lambda, etc.)
    else:
        # Dynamic expression - wrap it
        return True
```

#### Modification 4: New Helper - Generate Wrapped Call

**Location**: New method in PythonGenerator class

```python
def _generate_function_call_wrapped(self, node: FunctionCall) -> str:
    """Generate function call with selective _safe_call wrapping.

    This is the main entry point for all function call generation.
    Decides whether to wrap the call based on function type.

    Args:
        node: FunctionCall AST node

    Returns:
        Generated Python code (wrapped or unwrapped)
    """
    # Determine if this call needs wrapping
    needs_wrap = self._should_wrap_call(node.function)

    if needs_wrap:
        # Generate wrapped call: _safe_call(func, args)
        return self._generate_wrapped_call(node)
    else:
        # Generate direct call: func(args)
        return self._generate_direct_call(node)


def _generate_direct_call(self, node: FunctionCall) -> str:
    """Generate direct function call without _safe_call wrapper.

    Used for user-defined functions which are trusted.

    Args:
        node: FunctionCall AST node

    Returns:
        Generated code: func(arg1, arg2, ...)
    """
    func_name = node.function.name  # Must be Identifier for user function
    safe_name = self._safe_identifier(func_name)

    args = [self._generate_expression(arg) for arg in node.arguments]
    args_str = ', '.join(args)

    return f"{safe_name}({args_str})"


def _generate_wrapped_call(self, node: FunctionCall) -> str:
    """Generate function call wrapped with _safe_call.

    Handles all cases: builtins, module functions, variables, methods.

    Args:
        node: FunctionCall AST node

    Returns:
        Generated code: _safe_call(func, arg1, arg2, ...)
    """
    # Generate function expression
    func_code = self._generate_expression(node.function)

    # Generate arguments
    args = [self._generate_expression(arg) for arg in node.arguments]

    # Combine function and arguments for _safe_call
    all_args = [func_code] + args
    args_str = ', '.join(all_args)

    return f"_safe_call({args_str})"
```

#### Modification 5: Handle Method Calls Specially

**Location**: Update `_generate_expression()` for MemberAccess in call context

```python
# When generating MemberAccess that will be called:
def _generate_expression(self, expr) -> str:
    # ... other cases ...

    elif isinstance(expr, MemberAccess):
        # Check if this member access is for a method call
        # (This is called from _generate_wrapped_call for the function part)

        # For module.function:
        if isinstance(expr.object, Identifier):
            module_name = expr.object.name
            if self.function_registry.is_imported_module(module_name):
                # It's a module function reference
                member_name = expr.member if isinstance(expr.member, str) else str(expr.member)
                safe_module = self._safe_identifier(module_name)
                return f"{safe_module}.{member_name}"

        # For object.method - use safe_attr_access
        obj_code = self._generate_expression(expr.object)
        member_name = expr.member if isinstance(expr.member, str) else str(expr.member)

        # Return attribute access (will be passed to _safe_call)
        return f"_safe_attr_access({obj_code}, {repr(member_name)})"
```

#### Summary of Code Generator Changes

**Files Modified**: 1
- `src/mlpy/ml/codegen/python_generator.py`

**Methods Modified**: 2
- `generate()` - Add runtime imports
- `_generate_expression()` - Use new call generation

**Methods Added**: 5
- `_generate_runtime_imports()` - Add safe_call import
- `_should_wrap_call()` - Decide if wrapping needed
- `_generate_function_call_wrapped()` - Main call generator
- `_generate_direct_call()` - User function calls
- `_generate_wrapped_call()` - Wrapped calls

**Lines Added**: ~100 lines
**Complexity**: Low (clear logic)

---

### Component 4: Generated Code Examples

#### Example 1: Simple Builtin Call

**ML Code**:
```javascript
let size = builtin.len([1, 2, 3]);
```

**Generated Python**:
```python
"""Generated Python code from ML source."""

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin

size = _safe_call(builtin.len, [1, 2, 3])
```

#### Example 2: User Function (Not Wrapped)

**ML Code**:
```javascript
function double(x) {
    return x * 2;
}

let result = double(21);
```

**Generated Python**:
```python
"""Generated Python code from ML source."""

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin

def double(x):
    return (x * 2)

result = double(21)  # NOT wrapped - user-defined function
```

#### Example 3: Variable Function Call

**ML Code**:
```javascript
let myLen = builtin.len;
let size = myLen([1, 2, 3]);
```

**Generated Python**:
```python
"""Generated Python code from ML source."""

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin

myLen = builtin.len  # Assignment, not a call
size = _safe_call(myLen, [1, 2, 3])  # WRAPPED - variable call
```

#### Example 4: Module Function Call

**ML Code**:
```javascript
import math;
let result = math.sqrt(16);
```

**Generated Python**:
```python
"""Generated Python code from ML source."""

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin
from mlpy.stdlib.math_bridge import math

result = _safe_call(math.sqrt, 16)  # WRAPPED - module function
```

#### Example 5: Method Call

**ML Code**:
```javascript
let str = "hello";
let upper = str.upper();
```

**Generated Python**:
```python
"""Generated Python code from ML source."""

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin
from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access

str_val = "hello"
upper = _safe_call(_safe_attr_access(str_val, 'upper'))
```

#### Example 6: Nested Calls

**ML Code**:
```javascript
let result = builtin.len(builtin.range(5));
```

**Generated Python**:
```python
"""Generated Python code from ML source."""

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin

result = _safe_call(builtin.len, _safe_call(builtin.range, 5))
```

#### Example 7: Higher-Order Function

**ML Code**:
```javascript
function apply(fn, value) {
    return fn(value);
}

function double(x) { return x * 2; }

let result = apply(double, 21);
```

**Generated Python**:
```python
"""Generated Python code from ML source."""

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin

def apply(fn, value):
    return _safe_call(fn, value)  # WRAPPED - fn is unknown

def double(x):
    return (x * 2)

result = apply(double, 21)  # NOT wrapped - user function
```

---

## Comprehensive Test Suite

### Test File 1: Whitelist Enforcement Tests

**File**: `tests/security/test_runtime_whitelist.py` (NEW)

```python
"""Test runtime whitelist enforcement.

These tests verify that the runtime validator correctly enforces
the whitelist by checking @ml_function decorator metadata.
"""

import pytest
from mlpy.runtime.whitelist_validator import (
    safe_call,
    SecurityError,
    CapabilityError,
)


class TestDecoratedFunctions:
    """Test that @ml_function decorated functions are allowed."""

    def test_builtin_len_allowed(self):
        """builtin.len is decorated and should work."""
        from mlpy.stdlib.builtin import builtin

        result = safe_call(builtin.len, [1, 2, 3])
        assert result == 3

    def test_builtin_print_allowed(self):
        """builtin.print is decorated and should work."""
        from mlpy.stdlib.builtin import builtin

        # Should not raise (print returns None)
        result = safe_call(builtin.print, "test")
        assert result is None

    def test_math_sqrt_allowed(self):
        """math.sqrt is decorated and should work."""
        from mlpy.stdlib.math_bridge import math

        result = safe_call(math.sqrt, 16)
        assert result == 4.0


class TestUserDefinedFunctions:
    """Test that user-defined functions are allowed."""

    def test_user_function_allowed(self):
        """User-defined functions should work without decorator."""

        def my_func(x):
            return x * 2

        result = safe_call(my_func, 21)
        assert result == 42

    def test_lambda_allowed(self):
        """Lambda functions should work."""
        fn = lambda x: x * 2

        result = safe_call(fn, 21)
        assert result == 42

    def test_nested_user_functions(self):
        """Nested user-defined functions should work."""

        def outer(x):
            def inner(y):
                return y * 2

            return inner(x)

        result = safe_call(outer, 21)
        assert result == 42


class TestBuiltinTypeMethods:
    """Test that methods on safe built-in types are allowed."""

    def test_string_upper(self):
        """String.upper() should work."""
        result = safe_call("hello".upper)
        assert result == "HELLO"

    def test_list_append(self):
        """List.append() should work."""
        lst = [1, 2, 3]
        result = safe_call(lst.append, 4)
        assert lst == [1, 2, 3, 4]

    def test_dict_get(self):
        """Dict.get() should work."""
        d = {"a": 1, "b": 2}
        result = safe_call(d.get, "a")
        assert result == 1


class TestPythonBuiltinsBlocked:
    """Test that Python built-in functions are blocked."""

    def test_eval_blocked(self):
        """Python's eval should be blocked."""
        with pytest.raises(SecurityError) as exc_info:
            safe_call(eval, "2+2")

        assert "not decorated" in str(exc_info.value).lower()
        assert "eval" in str(exc_info.value).lower()

    def test_exec_blocked(self):
        """Python's exec should be blocked."""
        with pytest.raises(SecurityError) as exc_info:
            safe_call(exec, "x = 1")

        assert "not decorated" in str(exc_info.value).lower()

    def test_open_blocked(self):
        """Python's open should be blocked."""
        with pytest.raises(SecurityError) as exc_info:
            safe_call(open, "test.txt")

        assert "not decorated" in str(exc_info.value).lower()

    def test_import_blocked(self):
        """Python's __import__ should be blocked."""
        with pytest.raises(SecurityError) as exc_info:
            safe_call(__import__, "os")

        assert "not decorated" in str(exc_info.value).lower()

    def test_compile_blocked(self):
        """Python's compile should be blocked."""
        with pytest.raises(SecurityError) as exc_info:
            safe_call(compile, "x=1", "test", "exec")

        assert "not decorated" in str(exc_info.value).lower()

    def test_help_blocked(self):
        """Python's help should be blocked."""
        with pytest.raises(SecurityError) as exc_info:
            safe_call(help)

        assert "not decorated" in str(exc_info.value).lower()


class TestVariableFunctionCalls:
    """Test function calls through variables."""

    def test_variable_holding_decorated_function(self):
        """Variable holding decorated function should work."""
        from mlpy.stdlib.builtin import builtin

        fn = builtin.len
        result = safe_call(fn, [1, 2, 3])
        assert result == 3

    def test_variable_holding_user_function(self):
        """Variable holding user function should work."""

        def my_func(x):
            return x * 2

        fn = my_func
        result = safe_call(fn, 21)
        assert result == 42

    def test_variable_holding_python_builtin(self):
        """Variable holding Python builtin should be blocked."""
        fn = eval

        with pytest.raises(SecurityError):
            safe_call(fn, "2+2")


class TestHigherOrderFunctions:
    """Test higher-order functions and callbacks."""

    def test_callback_with_decorated_function(self):
        """Passing decorated function as callback should work."""
        from mlpy.stdlib.builtin import builtin

        def apply(fn, value):
            return safe_call(fn, value)

        result = apply(builtin.len, [1, 2, 3])
        assert result == 3

    def test_callback_with_user_function(self):
        """Passing user function as callback should work."""

        def apply(fn, value):
            return safe_call(fn, value)

        def double(x):
            return x * 2

        result = apply(double, 21)
        assert result == 42

    def test_callback_with_python_builtin(self):
        """Passing Python builtin as callback should be blocked."""

        def apply(fn, code):
            return safe_call(fn, code)

        with pytest.raises(SecurityError):
            apply(eval, "2+2")


class TestNotCallable:
    """Test error handling for non-callable objects."""

    def test_integer_not_callable(self):
        """Trying to call an integer should raise TypeError."""
        with pytest.raises(TypeError) as exc_info:
            safe_call(42)

        assert "not callable" in str(exc_info.value).lower()

    def test_string_not_callable(self):
        """Trying to call a string should raise TypeError."""
        with pytest.raises(TypeError):
            safe_call("hello")

    def test_none_not_callable(self):
        """Trying to call None should raise TypeError."""
        with pytest.raises(TypeError):
            safe_call(None)
```

### Test File 2: Capability Enforcement Tests

**File**: `tests/security/test_runtime_capabilities.py` (NEW)

```python
"""Test runtime capability enforcement.

These tests verify that functions requiring capabilities are
properly validated against the current capability context.
"""

import pytest
from mlpy.runtime.whitelist_validator import (
    safe_call,
    CapabilityError,
    set_capability_context,
    check_capabilities,
)


class TestCapabilityChecking:
    """Test the check_capabilities() function."""

    def test_no_capabilities_required(self):
        """Functions with no capabilities should always work."""
        # Should not raise
        check_capabilities([])

    def test_capabilities_required_no_context(self):
        """Functions requiring capabilities should fail without context."""
        with pytest.raises(CapabilityError) as exc_info:
            check_capabilities(["FILE_READ"])

        assert "FILE_READ" in str(exc_info.value)
        assert "no capability context" in str(exc_info.value).lower()

    def test_capabilities_satisfied(self):
        """Functions should work when capabilities are available."""
        from mlpy.runtime.capabilities import CapabilityContext
        from mlpy.runtime.capabilities.tokens import CapabilityToken

        ctx = CapabilityContext()
        token = CapabilityToken("FILE_READ", resource_pattern="/data/*")
        ctx.add_capability(token)
        set_capability_context(ctx)

        try:
            # Should not raise
            check_capabilities(["FILE_READ"])
        finally:
            set_capability_context(None)

    def test_capabilities_missing(self):
        """Functions should fail when capabilities are missing."""
        from mlpy.runtime.capabilities import CapabilityContext

        ctx = CapabilityContext()
        # No capabilities added
        set_capability_context(ctx)

        try:
            with pytest.raises(CapabilityError) as exc_info:
                check_capabilities(["FILE_READ"])

            assert "FILE_READ" in str(exc_info.value)
            assert "missing" in str(exc_info.value).lower()
        finally:
            set_capability_context(None)


class TestFunctionsWithCapabilities:
    """Test safe_call with functions that require capabilities."""

    def test_function_no_capabilities_no_context(self):
        """Decorated function with no capabilities works without context."""
        from mlpy.stdlib.builtin import builtin

        # builtin.len requires no capabilities
        result = safe_call(builtin.len, [1, 2, 3])
        assert result == 3

    def test_function_with_capabilities_no_context(self):
        """Decorated function with capabilities fails without context."""
        # Create a mock function with capabilities
        def mock_func():
            pass

        mock_func._ml_function_metadata = {
            "name": "mock_func",
            "capabilities": ["FILE_READ"],
        }

        with pytest.raises(CapabilityError) as exc_info:
            safe_call(mock_func)

        assert "FILE_READ" in str(exc_info.value)

    def test_function_with_capabilities_satisfied(self):
        """Decorated function works when capabilities are satisfied."""
        from mlpy.runtime.capabilities import CapabilityContext
        from mlpy.runtime.capabilities.tokens import CapabilityToken

        def mock_func():
            return "success"

        mock_func._ml_function_metadata = {
            "name": "mock_func",
            "capabilities": ["FILE_READ"],
        }

        ctx = CapabilityContext()
        token = CapabilityToken("FILE_READ", resource_pattern="/data/*")
        ctx.add_capability(token)
        set_capability_context(ctx)

        try:
            result = safe_call(mock_func)
            assert result == "success"
        finally:
            set_capability_context(None)

    def test_function_with_multiple_capabilities(self):
        """Function requiring multiple capabilities."""
        from mlpy.runtime.capabilities import CapabilityContext
        from mlpy.runtime.capabilities.tokens import CapabilityToken

        def mock_func():
            return "success"

        mock_func._ml_function_metadata = {
            "name": "mock_func",
            "capabilities": ["FILE_READ", "FILE_WRITE"],
        }

        ctx = CapabilityContext()
        ctx.add_capability(CapabilityToken("FILE_READ", resource_pattern="/data/*"))
        ctx.add_capability(CapabilityToken("FILE_WRITE", resource_pattern="/data/*"))
        set_capability_context(ctx)

        try:
            result = safe_call(mock_func)
            assert result == "success"
        finally:
            set_capability_context(None)

    def test_function_missing_one_capability(self):
        """Function fails if any required capability is missing."""
        from mlpy.runtime.capabilities import CapabilityContext
        from mlpy.runtime.capabilities.tokens import CapabilityToken

        def mock_func():
            return "success"

        mock_func._ml_function_metadata = {
            "name": "mock_func",
            "capabilities": ["FILE_READ", "FILE_WRITE"],
        }

        ctx = CapabilityContext()
        ctx.add_capability(CapabilityToken("FILE_READ", resource_pattern="/data/*"))
        # FILE_WRITE missing
        set_capability_context(ctx)

        try:
            with pytest.raises(CapabilityError) as exc_info:
                safe_call(mock_func)

            assert "FILE_WRITE" in str(exc_info.value)
        finally:
            set_capability_context(None)
```

### Test File 3: Bypass Attempts (All Must Fail)

**File**: `tests/security/test_bypass_attempts.py` (NEW)

```python
"""Test that all known bypass attempts are blocked.

ALL tests in this file MUST raise SecurityError.
These are the original vulnerabilities that prompted the runtime validation.
"""

import pytest
from mlpy.ml.transpiler import MLTranspiler
from mlpy.runtime.whitelist_validator import SecurityError


def transpile_and_execute(ml_code: str) -> dict:
    """Helper to transpile and execute ML code.

    Args:
        ml_code: ML source code

    Returns:
        Execution namespace

    Raises:
        Various exceptions from transpilation/execution
    """
    transpiler = MLTranspiler()
    python_code, issues, source_map = transpiler.transpile_to_python(
        ml_code, source_file="<test>"
    )

    if python_code is None:
        raise ValueError(f"Transpilation failed: {issues}")

    namespace = {}
    exec(python_code, namespace)
    return namespace


class TestBuiltinCallBypass:
    """Test that builtin.call() bypass is blocked."""

    def test_call_eval(self):
        """builtin.call(eval, ...) should be blocked."""
        ml_code = 'let result = builtin.call(eval, "2+2");'

        with pytest.raises(SecurityError) as exc_info:
            transpile_and_execute(ml_code)

        assert "eval" in str(exc_info.value).lower()

    def test_call_exec(self):
        """builtin.call(exec, ...) should be blocked."""
        ml_code = 'builtin.call(exec, "x = 42");'

        with pytest.raises(SecurityError):
            transpile_and_execute(ml_code)

    def test_call_open(self):
        """builtin.call(open, ...) should be blocked."""
        ml_code = 'let f = builtin.call(open, "test.txt");'

        with pytest.raises(SecurityError):
            transpile_and_execute(ml_code)

    def test_call_import(self):
        """builtin.call(__import__, ...) should be blocked."""
        ml_code = 'let os = builtin.call(__import__, "os");'

        with pytest.raises(SecurityError):
            transpile_and_execute(ml_code)

    def test_call_compile(self):
        """builtin.call(compile, ...) should be blocked."""
        ml_code = 'builtin.call(compile, "x=1", "test", "exec");'

        with pytest.raises(SecurityError):
            transpile_and_execute(ml_code)

    def test_call_help(self):
        """builtin.call(help) should be blocked."""
        ml_code = "builtin.call(help);"

        with pytest.raises(SecurityError):
            transpile_and_execute(ml_code)


class TestVariableBypass:
    """Test that variable function bypass is blocked."""

    def test_variable_eval(self):
        """Storing eval in variable should be blocked when called."""
        ml_code = """
        let dangerous = eval;
        let result = dangerous("2+2");
        """

        with pytest.raises(SecurityError):
            transpile_and_execute(ml_code)

    def test_variable_help(self):
        """Storing help in variable should be blocked when called."""
        ml_code = """
        let h = help;
        h();
        """

        with pytest.raises(SecurityError):
            transpile_and_execute(ml_code)

    def test_variable_open(self):
        """Storing open in variable should be blocked when called."""
        ml_code = """
        let openFile = open;
        let f = openFile("test.txt");
        """

        with pytest.raises(SecurityError):
            transpile_and_execute(ml_code)


class TestHigherOrderBypass:
    """Test that higher-order function bypass is blocked."""

    def test_callback_eval(self):
        """Passing eval as callback should be blocked when invoked."""
        ml_code = """
        function execute(fn, arg) {
            return fn(arg);
        }

        let result = execute(eval, "2+2");
        """

        with pytest.raises(SecurityError):
            transpile_and_execute(ml_code)

    def test_callback_open(self):
        """Passing open as callback should be blocked when invoked."""
        ml_code = """
        function apply(fn, arg) {
            return fn(arg);
        }

        let f = apply(open, "test.txt");
        """

        with pytest.raises(SecurityError):
            transpile_and_execute(ml_code)


class TestNestedBypass:
    """Test that nested bypass attempts are blocked."""

    def test_nested_eval(self):
        """Nested call with eval should be blocked."""
        ml_code = """
        let result = builtin.len(builtin.call(eval, "[1,2,3]"));
        """

        with pytest.raises(SecurityError):
            transpile_and_execute(ml_code)

    def test_call_of_call(self):
        """Chained builtin.call should be blocked."""
        ml_code = """
        let result = builtin.call(builtin.call, eval, "2+2");
        """

        with pytest.raises(SecurityError):
            transpile_and_execute(ml_code)
```

### Test File 4: Legitimate Use Cases (All Must Succeed)

**File**: `tests/security/test_legitimate_usage.py` (NEW)

```python
"""Test that legitimate ML code still works with runtime validation.

ALL tests in this file MUST succeed without SecurityError.
"""

import pytest
from mlpy.ml.transpiler import MLTranspiler


def transpile_and_execute(ml_code: str) -> dict:
    """Helper to transpile and execute ML code."""
    transpiler = MLTranspiler()
    python_code, issues, source_map = transpiler.transpile_to_python(
        ml_code, source_file="<test>"
    )

    if python_code is None:
        raise ValueError(f"Transpilation failed: {issues}")

    namespace = {}
    exec(python_code, namespace)
    return namespace


class TestBuiltinFunctions:
    """Test that ML builtin functions work."""

    def test_len(self):
        """builtin.len should work."""
        ml_code = "let result = builtin.len([1, 2, 3]);"
        namespace = transpile_and_execute(ml_code)
        assert namespace["result"] == 3

    def test_print(self):
        """builtin.print should work."""
        ml_code = 'builtin.print("Hello");'
        # Should not raise
        transpile_and_execute(ml_code)

    def test_range(self):
        """builtin.range should work."""
        ml_code = "let result = builtin.range(5);"
        namespace = transpile_and_execute(ml_code)
        assert namespace["result"] == [0, 1, 2, 3, 4]


class TestUserFunctions:
    """Test that user-defined functions work."""

    def test_simple_function(self):
        """Simple user function should work."""
        ml_code = """
        function double(x) {
            return x * 2;
        }

        let result = double(21);
        """
        namespace = transpile_and_execute(ml_code)
        assert namespace["result"] == 42

    def test_recursive_function(self):
        """Recursive user function should work."""
        ml_code = """
        function factorial(n) {
            if (n <= 1) {
                return 1;
            } else {
                return n * factorial(n - 1);
            }
        }

        let result = factorial(5);
        """
        namespace = transpile_and_execute(ml_code)
        assert namespace["result"] == 120

    def test_function_calling_builtin(self):
        """User function calling builtin should work."""
        ml_code = """
        function getLength(arr) {
            return builtin.len(arr);
        }

        let result = getLength([1, 2, 3, 4]);
        """
        namespace = transpile_and_execute(ml_code)
        assert namespace["result"] == 4


class TestVariableFunctions:
    """Test that storing functions in variables works."""

    def test_variable_builtin(self):
        """Storing builtin in variable should work."""
        ml_code = """
        let myLen = builtin.len;
        let result = myLen([1, 2, 3]);
        """
        namespace = transpile_and_execute(ml_code)
        assert namespace["result"] == 3

    def test_variable_user_function(self):
        """Storing user function in variable should work."""
        ml_code = """
        function double(x) {
            return x * 2;
        }

        let fn = double;
        let result = fn(21);
        """
        namespace = transpile_and_execute(ml_code)
        assert namespace["result"] == 42


class TestHigherOrderFunctions:
    """Test that higher-order functions work."""

    def test_callback_user_function(self):
        """Passing user function as callback should work."""
        ml_code = """
        function apply(fn, x) {
            return fn(x);
        }

        function double(x) {
            return x * 2;
        }

        let result = apply(double, 21);
        """
        namespace = transpile_and_execute(ml_code)
        assert namespace["result"] == 42

    def test_callback_builtin(self):
        """Passing builtin as callback should work."""
        ml_code = """
        function apply(fn, x) {
            return fn(x);
        }

        let result = apply(builtin.len, [1, 2, 3]);
        """
        namespace = transpile_and_execute(ml_code)
        assert namespace["result"] == 3


class TestModuleFunctions:
    """Test that imported module functions work."""

    def test_math_sqrt(self):
        """math.sqrt should work."""
        ml_code = """
        import math;
        let result = math.sqrt(16);
        """
        namespace = transpile_and_execute(ml_code)
        assert namespace["result"] == 4.0

    def test_math_abs(self):
        """math.abs should work."""
        ml_code = """
        import math;
        let result = math.abs(-42);
        """
        namespace = transpile_and_execute(ml_code)
        assert namespace["result"] == 42


class TestMethodCalls:
    """Test that method calls on safe types work."""

    def test_string_upper(self):
        """String.upper() should work."""
        ml_code = """
        let str = "hello";
        let result = str.upper();
        """
        namespace = transpile_and_execute(ml_code)
        assert namespace["result"] == "HELLO"

    def test_list_append(self):
        """List.append() should work."""
        ml_code = """
        let arr = [1, 2, 3];
        arr.append(4);
        let result = builtin.len(arr);
        """
        namespace = transpile_and_execute(ml_code)
        assert namespace["result"] == 4
```

---

## Implementation Roadmap

### Phase 1: Core Implementation (Week 1)

#### Day 1: Runtime Validator
- [ ] Create `src/mlpy/runtime/whitelist_validator.py`
- [ ] Implement `safe_call()` function
- [ ] Implement `check_capabilities()` function
- [ ] Add thread-local context management
- [ ] Write unit tests for `safe_call()` logic

**Deliverable**: Working `safe_call()` function with tests

#### Day 2: Fix builtin.call()
- [ ] Modify `src/mlpy/stdlib/builtin.py`
- [ ] Update `call()` method to use `safe_call()`
- [ ] Test that bypass attempts are blocked
- [ ] Verify legitimate uses still work

**Deliverable**: Secure `builtin.call()` implementation

#### Day 3: Code Generator - Import Generation
- [ ] Add `_generate_runtime_imports()` method
- [ ] Modify `generate()` to call it
- [ ] Test generated code includes import
- [ ] Verify import doesn't break existing code

**Deliverable**: Generated code includes `_safe_call` import

#### Day 4: Code Generator - Call Wrapping
- [ ] Add `_should_wrap_call()` method
- [ ] Add `_generate_function_call_wrapped()` method
- [ ] Add `_generate_direct_call()` method
- [ ] Add `_generate_wrapped_call()` method
- [ ] Modify `_generate_expression()` to use new logic

**Deliverable**: Function calls wrapped with `_safe_call`

#### Day 5: Integration Testing
- [ ] Run bypass attempt tests (all must fail)
- [ ] Run legitimate usage tests (all must succeed)
- [ ] Test with existing ML test files
- [ ] Fix any issues discovered

**Deliverable**: All tests passing

### Phase 2: Testing and Validation (Week 1-2)

#### Day 6-7: Comprehensive Testing
- [ ] Create all test files listed above
- [ ] Test original vulnerabilities fixed:
  - [ ] `builtin.call(help)` blocked
  - [ ] `builtin.call(eval, "code")` blocked
  - [ ] `m = help; m()` blocked
  - [ ] `m = builtin.len; m([])` works
- [ ] Test capability checking (if implemented)
- [ ] Performance testing

**Deliverable**: Complete test suite passing

### Phase 3: Documentation (Week 2)

#### Day 8-9: Documentation
- [ ] Update security documentation
- [ ] Document `safe_call()` API
- [ ] Add examples of secure patterns
- [ ] Document error messages
- [ ] Update developer guide

**Deliverable**: Complete documentation

### Phase 4: REPL Security (Week 2)

#### Day 10: Secure REPL
- [ ] Modify `src/mlpy/cli/repl.py`
- [ ] Replace `__builtins__` with restricted dict
- [ ] Test REPL with new validation
- [ ] Verify bypass attempts fail in REPL

**Deliverable**: Secure REPL implementation

---

## Risk Analysis

### Risk 1: Performance Impact
**Likelihood**: High
**Impact**: Medium
**Current**: Every call has ~100-200ns overhead
**Mitigation**:
- Accept for Phase 1 (security > performance)
- Add caching in Phase 2 if needed
- User functions not wrapped (zero overhead)

### Risk 2: False Positives (Blocking Legitimate Code)
**Likelihood**: Medium
**Impact**: High
**Mitigation**:
- Comprehensive test suite
- Clear error messages
- Allow methods on safe types
- Allow user-defined functions

### Risk 3: Edge Cases We Missed
**Likelihood**: Low
**Impact**: Medium
**Mitigation**:
- Thorough testing
- Security review
- Bug bounty program (future)

### Risk 4: Compatibility with Existing Code
**Likelihood**: Low
**Impact**: Low
**Reason**: No code in the wild yet
**Mitigation**: Can change freely

---

## Success Criteria

### Security (MUST PASS)
- [ ] ✅ `builtin.call(eval)` blocked
- [ ] ✅ `builtin.call(open)` blocked
- [ ] ✅ `m = eval; m()` blocked
- [ ] ✅ All Python builtins blocked
- [ ] ✅ All bypass attempts raise SecurityError

### Functionality (MUST PASS)
- [ ] ✅ ML builtins work
- [ ] ✅ User functions work
- [ ] ✅ Module functions work
- [ ] ✅ Variable function storage works for whitelisted
- [ ] ✅ Higher-order functions work
- [ ] ✅ Methods on safe types work

### Quality (SHOULD PASS)
- [ ] ✅ Clear error messages
- [ ] ✅ <10% performance overhead (user functions)
- [ ] ✅ <3x overhead (builtin calls)
- [ ] ✅ All tests passing
- [ ] ✅ Complete documentation

---

## Recommendation

**APPROVE AND IMPLEMENT**

This proposal provides:

✅ **Complete Security**: Blocks all known bypass vectors
✅ **Simple Implementation**: ~350 new lines of code total
✅ **Minimal Overhead**: 60 bytes per generated file
✅ **Capability-Ready**: Easy to add capability checking later
✅ **Maintainable**: Single source of truth (decorators)
✅ **Well-Tested**: Comprehensive test suite specified
✅ **Clear Path**: 10-day implementation timeline

**This is the right solution.** The decorator-based approach is elegant, secure, and maintainable.

**Estimated effort**: 10 days (2 weeks calendar time)
**Complexity**: Medium (straightforward logic)
**Risk**: Low (no code in wild, can iterate)

**Recommendation**: Proceed with implementation starting Day 1.
