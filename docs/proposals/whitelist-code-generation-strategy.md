# Whitelist Code Generation Strategy: Only Allow Known Safe Functions

**Date**: January 2025
**Proposal**: Comprehensive whitelist-based code generation
**Status**: RECOMMENDED - Superior to blacklist approach

---

## Executive Summary

**Question**: How do we ensure only stdlib functions get transpiled, blocking everything else?

**Answer**: **Whitelist strategy** - Only allow explicitly known safe functions, block everything else.

**Key Insight**: Instead of trying to blacklist dangerous Python functions (incomplete and fragile), we whitelist ONLY known ML functions (complete and secure).

---

## The Problem with Blacklist Approach

### Blacklist Strategy (What We Considered)

```python
DANGEROUS_PYTHON_BUILTINS = {
    'eval', 'exec', 'open', 'type', 'id', ...
}

if func_name in DANGEROUS_PYTHON_BUILTINS:
    raise Error("Blocked")
else:
    return f"{func_name}({args})"  # ❌ Still allows unknown functions!
```

**Problems**:
1. ❌ **Incomplete** - Can't list every dangerous function
2. ❌ **Fragile** - New Python versions add new builtins
3. ❌ **Reactive** - Must update list when threats discovered
4. ❌ **Allows unknowns** - Anything not in blacklist is allowed

**Example Failure**:
```python
# Blacklist misses this new Python 3.14 dangerous function
result = new_dangerous_builtin()  # ❌ Not in blacklist, allowed!
```

---

## The Whitelist Approach (RECOMMENDED)

### Whitelist Strategy

```python
# Only allow explicitly known safe functions
if is_ml_builtin_function(func_name):
    return f"builtin.{func_name}({args})"  # ✅ Known safe
elif is_user_defined_function(func_name):
    return f"{func_name}({args})"  # ✅ Known safe
elif is_imported_stdlib_function(func_name):
    return f"{module}.{func_name}({args})"  # ✅ Known safe
else:
    raise CodeGenError(f"Unknown function '{func_name}'")  # ✅ Block everything else
```

**Advantages**:
1. ✅ **Complete** - Only allows explicitly defined functions
2. ✅ **Secure by default** - Unknown = blocked
3. ✅ **Proactive** - No updates needed for new threats
4. ✅ **Leverages existing metadata** - Uses decorator system

**Example Success**:
```python
# Any unknown function is blocked
result = unknown_function()  # ✅ CodeGenError at compile time!
```

---

## How It Works: Three Categories of Allowed Functions

### Category 1: ML Builtin Functions (Auto-Imported)

**Source**: `@ml_function` decorators in `builtin.py`

```python
# ML code
x = int("42");
t = typeof(x);
```

**Detection**:
```python
metadata = get_module_metadata("builtin")
if func_name in metadata.functions:
    # This is a known ML builtin
    return f"builtin.{func_name}({args})"
```

**Generated Python**:
```python
from mlpy.stdlib.builtin import builtin

x = builtin.int("42")
t = builtin.typeof(x)
```

**Security**: ✅ Only calls functions explicitly defined in ML builtin module

---

### Category 2: User-Defined Functions

**Source**: Functions defined in the ML code itself

```python
// ML code
function myFunc(x) {
    return x * 2;
}

y = myFunc(5);  // User-defined, allowed
```

**Detection**:
```python
# Track during AST traversal
class CodeGenContext:
    defined_functions: set[str] = field(default_factory=set)

# During function definition visit
def visit_function_declaration(self, node):
    self.context.defined_functions.add(node.name)

# During function call generation
if func_name in self.context.defined_functions:
    return f"{func_name}({args})"  # User-defined, allowed
```

**Generated Python**:
```python
def myFunc(x):
    return (x * 2)

y = myFunc(5)  # Direct call, safe
```

**Security**: ✅ Only calls functions user explicitly defined in their code

---

### Category 3: Imported Stdlib Module Functions

**Source**: `@ml_function` decorators in imported stdlib modules

```python
// ML code
import string;

upper = string.upper("hello");
```

**Detection**:
```python
# Track imported modules
class CodeGenContext:
    imported_modules: dict[str, ModuleMetadata] = field(default_factory=dict)

# During import statement
def visit_import_statement(self, node):
    metadata = get_module_metadata(node.module_name)
    if metadata:
        self.context.imported_modules[node.alias] = metadata

# During function call generation
if isinstance(expr.function, MemberAccess):
    module_name = expr.object.name
    if module_name in self.context.imported_modules:
        module_metadata = self.context.imported_modules[module_name]
        if func_name in module_metadata.functions:
            # Known stdlib function
            return f"{module_name}.{func_name}({args})"
        else:
            raise CodeGenError(
                f"Module '{module_name}' has no function '{func_name}'"
            )
```

**Generated Python**:
```python
from mlpy.stdlib.string_bridge import string_module as string

upper = string.upper("hello")  # Known stdlib function, allowed
```

**Security**: ✅ Only calls functions explicitly defined in stdlib module metadata

---

### Category 4: Everything Else (BLOCKED)

**Any function not in categories 1-3 is blocked**:

```python
// ML code with unknown function
x = unknown_func();      // ❌ Not builtin, not user-defined, not imported
y = open("file.txt");    // ❌ Not in ML builtin
z = eval("1 + 1");       // ❌ Not in ML builtin
```

**Detection**:
```python
def _generate_function_call(self, expr: FunctionCall) -> str:
    func_name = self._extract_function_name(expr)

    # Check all allowed categories
    if self._is_ml_builtin(func_name):
        return self._generate_builtin_call(expr)
    elif self._is_user_defined(func_name):
        return self._generate_user_call(expr)
    elif self._is_imported_stdlib(expr):
        return self._generate_stdlib_call(expr)
    else:
        # NOT ALLOWED - block at compile time
        raise CodeGenError(
            f"Unknown function '{func_name}'.\n"
            f"Available functions:\n"
            f"  - ML builtins: {self._list_builtins()}\n"
            f"  - User-defined: {self._list_user_functions()}\n"
            f"  - Import stdlib modules to access more functions"
        )
```

**Result**: Compile-time error with helpful message

---

## Implementation Design

### Component 1: Comprehensive Function Registry

**File**: `src/mlpy/ml/codegen/function_registry.py`

```python
"""Function registry for whitelist-based code generation.

This module provides utilities to determine if a function call is allowed,
leveraging the existing decorator metadata system.
"""

from dataclasses import dataclass, field
from typing import Optional, Set, Dict
from mlpy.stdlib.decorators import get_module_metadata, get_all_modules


@dataclass
class AllowedFunctionsRegistry:
    """Registry of all allowed functions in current compilation context.

    This is the WHITELIST - only functions in this registry can be called.
    """

    # ML builtin functions (always available)
    builtin_functions: Set[str] = field(default_factory=set)

    # User-defined functions (from current ML file)
    user_defined_functions: Set[str] = field(default_factory=set)

    # Imported stdlib modules and their functions
    imported_modules: Dict[str, ModuleMetadata] = field(default_factory=dict)

    def __post_init__(self):
        """Initialize builtin functions from metadata."""
        builtin_metadata = get_module_metadata("builtin")
        if builtin_metadata:
            self.builtin_functions = set(builtin_metadata.functions.keys())

    def is_allowed_builtin(self, func_name: str) -> bool:
        """Check if function is an ML builtin."""
        return func_name in self.builtin_functions

    def is_user_defined(self, func_name: str) -> bool:
        """Check if function is user-defined."""
        return func_name in self.user_defined_functions

    def is_imported_function(self, module_name: str, func_name: str) -> bool:
        """Check if function exists in imported module."""
        if module_name not in self.imported_modules:
            return False

        module_metadata = self.imported_modules[module_name]
        return func_name in module_metadata.functions

    def add_user_function(self, func_name: str) -> None:
        """Register a user-defined function."""
        self.user_defined_functions.add(func_name)

    def add_imported_module(self, module_alias: str, module_name: str) -> bool:
        """Register an imported stdlib module.

        Args:
            module_alias: The name used in code (e.g., 'str' for 'import string as str')
            module_name: The actual module name (e.g., 'string')

        Returns:
            True if module exists and was added, False otherwise
        """
        metadata = get_module_metadata(module_name)
        if metadata:
            self.imported_modules[module_alias] = metadata
            return True
        return False

    def get_available_functions(self) -> Dict[str, list[str]]:
        """Get all available functions for error messages."""
        return {
            "builtins": sorted(self.builtin_functions),
            "user_defined": sorted(self.user_defined_functions),
            "imported": {
                module: sorted(metadata.functions.keys())
                for module, metadata in self.imported_modules.items()
            }
        }

    def suggest_alternatives(self, func_name: str) -> list[str]:
        """Suggest similar function names for typos."""
        from difflib import get_close_matches

        # Collect all available function names
        all_functions = list(self.builtin_functions)
        all_functions.extend(self.user_defined_functions)
        for metadata in self.imported_modules.values():
            all_functions.extend(metadata.functions.keys())

        # Find close matches
        matches = get_close_matches(func_name, all_functions, n=3, cutoff=0.6)
        return matches
```

---

### Component 2: Enhanced Code Generator

**File**: `src/mlpy/ml/codegen/python_generator.py` (modifications)

```python
from mlpy.ml.codegen.function_registry import AllowedFunctionsRegistry

class PythonCodeGenerator(ASTVisitor):
    def __init__(self, source_file: str = ""):
        # ... existing init ...
        self.function_registry = AllowedFunctionsRegistry()

    def visit_function_declaration(self, node: FunctionDeclaration):
        """Register user-defined function in whitelist."""
        self.function_registry.add_user_function(node.name)
        # ... existing code generation ...

    def visit_import_statement(self, node: ImportStatement):
        """Register imported module in whitelist."""
        module_name = node.module_path
        alias = node.alias if node.alias else module_name

        if self.function_registry.add_imported_module(alias, module_name):
            # Module found in ML stdlib, generate import
            # ... existing import generation ...
        else:
            # Unknown module - not in ML stdlib
            raise CodeGenError(
                f"Unknown module '{module_name}'.\n"
                f"Available ML stdlib modules: {self._list_stdlib_modules()}"
            )

    def _generate_function_call(self, expr: FunctionCall) -> str:
        """Generate function call with whitelist enforcement.

        This is the CORE of the whitelist strategy - only generate code
        for explicitly allowed functions.
        """

        # Extract function name and context
        if isinstance(expr.function, Identifier):
            func_name = expr.function.name

            # Category 1: ML Builtin
            if self.function_registry.is_allowed_builtin(func_name):
                self.context.builtin_functions_used.add(func_name)
                args = [self._generate_expression(arg) for arg in expr.arguments]
                return f"builtin.{func_name}({', '.join(args)})"

            # Category 2: User-defined
            elif self.function_registry.is_user_defined(func_name):
                args = [self._generate_expression(arg) for arg in expr.arguments]
                return f"{self._safe_identifier(func_name)}({', '.join(args)})"

            # Category 4: BLOCKED - not in whitelist
            else:
                self._raise_unknown_function_error(func_name)

        elif isinstance(expr.function, MemberAccess):
            # Category 3: Imported stdlib function
            module_name = self._get_module_name(expr.function.object)
            func_name = expr.function.member

            if self.function_registry.is_imported_function(module_name, func_name):
                args = [self._generate_expression(arg) for arg in expr.arguments]
                return f"{module_name}.{func_name}({', '.join(args)})"
            else:
                self._raise_unknown_module_function_error(module_name, func_name)

        else:
            # Complex expression (lambda, etc.) - allow
            func_code = self._generate_expression(expr.function)
            args = [self._generate_expression(arg) for arg in expr.arguments]
            return f"{func_code}({', '.join(args)})"

    def _raise_unknown_function_error(self, func_name: str) -> None:
        """Raise helpful error for unknown function."""
        available = self.function_registry.get_available_functions()
        suggestions = self.function_registry.suggest_alternatives(func_name)

        error_msg = f"Unknown function '{func_name}'.\n"

        if suggestions:
            error_msg += f"\nDid you mean: {', '.join(suggestions)}?\n"

        error_msg += f"\nAvailable functions:\n"
        error_msg += f"  ML Builtins: {', '.join(available['builtins'][:10])}"
        if len(available['builtins']) > 10:
            error_msg += f" ... ({len(available['builtins'])} total)"
        error_msg += f"\n"

        if available['user_defined']:
            error_msg += f"  User-defined: {', '.join(available['user_defined'])}\n"

        if available['imported']:
            error_msg += f"  Imported modules:\n"
            for module, funcs in available['imported'].items():
                error_msg += f"    {module}: {', '.join(funcs[:5])}"
                if len(funcs) > 5:
                    error_msg += f" ... ({len(funcs)} total)"
                error_msg += f"\n"

        error_msg += f"\nTo use additional functions, import the appropriate module:\n"
        error_msg += f"  import string;  // For string manipulation\n"
        error_msg += f"  import math;    // For mathematical operations\n"

        raise CodeGenError(error_msg)

    def _raise_unknown_module_function_error(self, module_name: str, func_name: str):
        """Raise helpful error for unknown module function."""
        if module_name not in self.function_registry.imported_modules:
            raise CodeGenError(
                f"Module '{module_name}' not imported or doesn't exist.\n"
                f"Available imported modules: {list(self.function_registry.imported_modules.keys())}"
            )

        module_metadata = self.function_registry.imported_modules[module_name]
        available_funcs = list(module_metadata.functions.keys())
        suggestions = get_close_matches(func_name, available_funcs, n=3, cutoff=0.6)

        error_msg = f"Module '{module_name}' has no function '{func_name}'.\n"

        if suggestions:
            error_msg += f"Did you mean: {', '.join(suggestions)}?\n"

        error_msg += f"\nAvailable functions in '{module_name}':\n"
        error_msg += f"  {', '.join(available_funcs)}"

        raise CodeGenError(error_msg)

    def _list_stdlib_modules(self) -> list[str]:
        """Get list of available ML stdlib modules."""
        all_modules = get_all_modules()
        return sorted(all_modules.keys())
```

---

## Security Analysis: Whitelist vs Blacklist

### Attack Surface Comparison

| Scenario | Blacklist Approach | Whitelist Approach |
|----------|-------------------|-------------------|
| **New Python builtin** | ❌ Allowed (not in blacklist) | ✅ Blocked (not in whitelist) |
| **Typo in function name** | ❌ Might allow | ✅ Blocked with suggestion |
| **Unknown stdlib module** | ❌ Might import | ✅ Blocked at import time |
| **Unknown module function** | ❌ Might call | ✅ Blocked at call time |
| **Python 3.15 new builtins** | ❌ Need update | ✅ Automatically blocked |

### Whitelist Security Guarantees

**Guarantee 1: Complete Coverage**
```python
# With whitelist, these are ALL blocked:
unknown()           # ✅ Blocked
open("file")        # ✅ Blocked
eval("code")        # ✅ Blocked
type(obj)           # ✅ Blocked
future_builtin()    # ✅ Blocked
```

**Guarantee 2: Explicit Allowance**
```python
# Only these are allowed:
builtin.int()       # ✅ Explicitly in ML builtin
myFunc()            # ✅ Explicitly user-defined
string.upper()      # ✅ Explicitly imported
```

**Guarantee 3: No Surprises**
- Can't accidentally allow dangerous function
- Can't forget to add to blacklist
- Can't be surprised by new Python versions

---

## Example: Complete Flow

### ML Code

```javascript
// ML code
import string;

function double(x) {
    return x * 2;
}

// Test various function calls
a = int("42");              // ML builtin - ALLOWED
b = typeof(a);              // ML builtin - ALLOWED
c = double(5);              // User-defined - ALLOWED
d = string.upper("hello");  // Imported stdlib - ALLOWED
e = open("file.txt");       // Unknown - BLOCKED
f = eval("1+1");            // Unknown - BLOCKED
g = myTypo(10);             // Unknown - BLOCKED
```

### Transpilation Process

**Phase 1: Registration**
```python
# During AST traversal
registry.add_imported_module("string", "string")  # ✅ Found in stdlib
registry.add_user_function("double")              # ✅ User-defined

# builtin functions already registered at init
```

**Phase 2: Code Generation**

```python
# For: a = int("42")
func_name = "int"
if registry.is_allowed_builtin("int"):  # ✅ Yes
    return "builtin.int('42')"

# For: b = typeof(a)
func_name = "typeof"
if registry.is_allowed_builtin("typeof"):  # ✅ Yes
    return "builtin.typeof(a)"

# For: c = double(5)
func_name = "double"
if registry.is_user_defined("double"):  # ✅ Yes
    return "double(5)"

# For: d = string.upper("hello")
module = "string", func = "upper"
if registry.is_imported_function("string", "upper"):  # ✅ Yes
    return "string.upper('hello')"

# For: e = open("file.txt")
func_name = "open"
if registry.is_allowed_builtin("open"):  # ❌ No
if registry.is_user_defined("open"):     # ❌ No
# Not imported module function either
raise CodeGenError(
    "Unknown function 'open'.\n"
    "Did you mean: one (from user functions)?\n"
    "Available ML builtins: abs, all, any, bin, bool, ... \n"
    "To access files, use the file module (requires capabilities)"
)  # ✅ BLOCKED

# For: f = eval("1+1")
func_name = "eval"
# Same checks fail
raise CodeGenError(
    "Unknown function 'eval'.\n"
    "No suggestions found.\n"
    "Available functions: ...\n"
)  # ✅ BLOCKED

# For: g = myTypo(10)
func_name = "myTypo"
# Same checks fail
raise CodeGenError(
    "Unknown function 'myTypo'.\n"
    "Did you mean: double?\n"  # ✅ Helpful suggestion
    "Available functions: ...\n"
)  # ✅ BLOCKED
```

**Phase 3: Generated Code (for allowed functions only)**

```python
from mlpy.stdlib.builtin import builtin
from mlpy.stdlib.string_bridge import string_module as string

def double(x):
    return (x * 2)

a = builtin.int('42')
b = builtin.typeof(a)
c = double(5)
d = string.upper('hello')
# e, f, g never generated - compilation failed
```

---

## Advantages of Whitelist Strategy

### 1. Security by Default

**Blacklist** (insecure):
```python
if func_name not in BLOCKED:
    allow()  # ❌ Default is ALLOW
```

**Whitelist** (secure):
```python
if func_name in ALLOWED:
    allow()
else:
    block()  # ✅ Default is BLOCK
```

### 2. Leverages Existing Infrastructure

Uses the decorator system you already have:
- `@ml_module` - Defines available modules
- `@ml_function` - Defines available functions
- `get_module_metadata()` - Access function lists
- `_MODULE_REGISTRY` - Global module registry

No new infrastructure needed!

### 3. Comprehensive and Complete

**Blacklist** - Must enumerate threats:
```python
BLOCKED = ['eval', 'exec', 'open', ...]  # ❌ Will we remember everything?
```

**Whitelist** - Automatically complete:
```python
# All @ml_function decorated functions are automatically in whitelist
# Everything else is automatically blocked
# No maintenance needed!
```

### 4. Great Error Messages

```
Unknown function 'opne'.
Did you mean: open? No - 'open' is not available in ML.
For file operations, import the file module (requires FILE_READ capability).

Available functions:
  ML Builtins: abs, all, any, bin, bool, chr, enumerate, float, format, ...
  User-defined: double, triple
  Imported modules:
    string: upper, lower, trim, split, join, ...
```

### 5. Scales to All Modules

Works the same way for:
- builtin module (auto-imported)
- string module (imported)
- math module (imported)
- file module (imported with capabilities)
- datetime module (imported)
- regex module (imported)
- ANY future module

---

## Feasibility Analysis

### Is This Feasible? **YES** ✅

**Reason 1: Infrastructure Exists**
- Decorator system already tracks all functions
- `_MODULE_REGISTRY` already populated
- `get_module_metadata()` already works
- Just need to check against it!

**Reason 2: Performance Impact Low**
- O(1) hash table lookups
- Only during compilation (not runtime)
- Cache decorator metadata at init
- Minimal overhead

**Reason 3: Implementation Straightforward**
- ~200 lines of new code (`function_registry.py`)
- ~100 lines of modifications (`python_generator.py`)
- Clear logic and flow
- Easy to test

**Reason 4: Better Than Alternatives**
- Simpler than blacklist (don't need to list threats)
- More secure than blacklist (default deny)
- Easier to maintain (automatic from decorators)
- Better UX (helpful error messages)

---

## Implementation Complexity

### Phase 1: Core Registry (2 hours)

**Files to Create**:
- `src/mlpy/ml/codegen/function_registry.py` (~200 lines)

**Implementation**:
1. Create `AllowedFunctionsRegistry` class
2. Load builtin functions from metadata
3. Add methods for registration and checking
4. Add suggestion system for typos

**Testing**:
```python
def test_builtin_functions_registered():
    registry = AllowedFunctionsRegistry()
    assert registry.is_allowed_builtin("int")
    assert registry.is_allowed_builtin("typeof")
    assert not registry.is_allowed_builtin("eval")

def test_user_function_registration():
    registry = AllowedFunctionsRegistry()
    registry.add_user_function("myFunc")
    assert registry.is_user_defined("myFunc")

def test_import_module():
    registry = AllowedFunctionsRegistry()
    assert registry.add_imported_module("string", "string")
    assert registry.is_imported_function("string", "upper")
```

### Phase 2: Code Generator Integration (2 hours)

**Files to Modify**:
- `src/mlpy/ml/codegen/python_generator.py` (~100 lines modified)

**Implementation**:
1. Add `AllowedFunctionsRegistry` to code generator
2. Register user functions during AST traversal
3. Register imports during import processing
4. Update `_generate_function_call()` with whitelist checks
5. Add error generation methods

**Testing**:
```python
def test_unknown_function_blocked():
    with pytest.raises(CodeGenError) as exc:
        transpile('x = open("file");')
    assert "Unknown function 'open'" in str(exc.value)

def test_imported_function_allowed():
    code = transpile('import string; x = string.upper("test");')
    assert "string.upper" in code
```

### Phase 3: Error Messages (1 hour)

**Implementation**:
1. Implement suggestion system (difflib)
2. Create comprehensive error messages
3. Add helpful hints for common mistakes

### Phase 4: Testing & Documentation (2 hours)

**Testing**:
- Unit tests for registry
- Integration tests for code generation
- Security tests for blocking

**Documentation**:
- Update developer guide
- Document whitelist strategy
- Add examples

**Total**: 7 hours for complete implementation

---

## Migration Path

### Phase 1: Implement Whitelist (Non-Breaking)

Initially, make whitelist opt-in with warning:

```python
# Flag to enable strict mode
STRICT_MODE = False

if not in_whitelist and STRICT_MODE:
    raise CodeGenError("Unknown function")
elif not in_whitelist:
    warnings.warn(f"Unknown function '{func_name}' - will be blocked in future")
    return f"{func_name}({args})"  # Still allow for now
```

### Phase 2: Enable by Default with Override

```python
STRICT_MODE = True  # Now on by default

# But allow override for migration
@transpile_option(allow_unknown_functions=True)
def migrate_old_code():
    # Old code with unknown functions still works
    pass
```

### Phase 3: Remove Override (Fully Strict)

```python
# Remove allow_unknown_functions option
# Whitelist now fully enforced
```

---

## Comparison with Current Proposal

### Current Proposal (v2)

```python
if is_builtin_function(func_name):
    return f"builtin.{func_name}({args})"
else:
    return f"{func_name}({args})"  # ❌ Allows everything else
```

**Issues**:
- ❌ Python builtins still accessible
- ❌ Typos generate broken code
- ❌ No protection outside sandbox

### Whitelist Enhancement

```python
if is_builtin_function(func_name):
    return f"builtin.{func_name}({args})"
elif is_user_defined(func_name):
    return f"{func_name}({args})"
elif is_imported_stdlib(expr):
    return f"{module}.{func_name}({args})"
else:
    raise CodeGenError("Unknown function")  # ✅ Blocks everything else
```

**Improvements**:
- ✅ Python builtins blocked at compile time
- ✅ Typos caught immediately
- ✅ Protection even outside sandbox
- ✅ Better error messages

---

## Recommendation

### Should We Do This? **YES** ✅

**Reasoning**:

1. **More Secure**: Default deny > default allow
2. **Easier to Implement**: Simpler than maintaining blacklist
3. **Better UX**: Helpful errors at compile time
4. **Leverages Existing**: Uses decorator metadata
5. **Scales**: Works for all current and future modules
6. **Low Risk**: Fails fast, easy to debug

### Implementation Priority

**CRITICAL** - Should be part of Phase 1 of the auto-import implementation.

**Timeline**:
- Core registry: 2 hours
- Integration: 2 hours
- Testing: 2 hours
- Documentation: 1 hour
- **Total: 7 hours**

### Integration with Original Proposal

**Original Proposal (v2)**: 6-9 hours
**+ Whitelist Enhancement**: +7 hours
**Total**: 13-16 hours

**But**: Whitelist replaces dangerous builtin blacklist (saves 2-3 hours)
**Actual Total**: ~11-13 hours for complete, secure solution

---

## Conclusion

**Question**: Should we whitelist only known stdlib functions?

**Answer**: **YES - Absolutely**

**Why**:
- ✅ More secure than blacklist
- ✅ Simpler to implement
- ✅ Easier to maintain
- ✅ Better error messages
- ✅ Leverages existing decorator system
- ✅ Scales to all modules
- ✅ Feasible within reasonable timeline

**Strategy**: Implement whitelist as core part of auto-import mechanism, not an afterthought.

**Result**: True "once and for all" solution that is:
- Secure by default
- Complete and comprehensive
- Maintainable and scalable
- User-friendly

**Recommendation**: **ADOPT WHITELIST STRATEGY** as the foundation of code generation security.
