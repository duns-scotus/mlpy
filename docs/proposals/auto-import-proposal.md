# Auto-Import Proposal: Decorator-Driven Whitelist Architecture

**Date**: January 2025
**Status**: APPROVED - Ready for Implementation
**Priority**: CRITICAL - Security & Correctness Issue
**Estimated Effort**: 11-13 hours

---

## Executive Summary

**Problem**: The transpiler generates direct calls to Python built-ins, bypassing ML's security model and causing semantic mismatches.

**Solution**: Implement a **whitelist-based code generation system** that uses decorator metadata to:
1. Route ML builtin functions to `builtin.function()`
2. Allow user-defined functions
3. Allow imported stdlib module functions
4. **Block everything else** at compile time

**Key Innovation**: Leverages existing `@ml_function` decorator metadata - no manual registry needed.

**Security Model**: **Whitelist, not blacklist** - only explicitly known functions are allowed, everything else is blocked.

---

## Architecture Overview

### Three-Category Whitelist System

```
┌─────────────────────────────────────────────────────────────┐
│                    ALLOWED FUNCTIONS                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Category 1: ML Builtin Functions (Auto-imported)     │  │
│  │ Source: @ml_function decorators in builtin.py        │  │
│  │ Example: int(), typeof(), len()                       │  │
│  │ Generation: builtin.function()                        │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Category 2: User-Defined Functions                   │  │
│  │ Source: function declarations in ML code              │  │
│  │ Example: function myFunc(x) { ... }                  │  │
│  │ Generation: myFunc()                                  │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Category 3: Imported Stdlib Functions                │  │
│  │ Source: @ml_function decorators in imported modules  │  │
│  │ Example: import string; string.upper()               │  │
│  │ Generation: string_module.upper()                     │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    BLOCKED FUNCTIONS                         │
├─────────────────────────────────────────────────────────────┤
│  Everything else: CodeGenError at compile time              │
│  - Python builtins (open, eval, type, id)                   │
│  - Typos (intt instead of int)                              │
│  - Unknown functions                                         │
│  - Future Python built-ins                                   │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

```
ML Source Code
    ↓
Parser (Lark)
    ↓
AST
    ↓
Code Generator
    ├→ Build Whitelist:
    │   ├─ Load builtin functions from @ml_function metadata
    │   ├─ Track user-defined functions during AST traversal
    │   └─ Track imported modules from import statements
    ↓
Function Call Analysis:
    ├─ Is it in ML builtin? → Generate: builtin.func()
    ├─ Is it user-defined? → Generate: func()
    ├─ Is it in imported module? → Generate: module.func()
    └─ None of the above? → CodeGenError (BLOCKED)
    ↓
Generated Python Code (Only Allowed Functions)
```

---

## Implementation Details

### Component 1: AllowedFunctionsRegistry

**File**: `src/mlpy/ml/codegen/function_registry.py` (NEW)

**Purpose**: Whitelist of all allowed functions in current compilation context.

```python
"""Function registry for whitelist-based code generation.

This module provides utilities to determine if a function call is allowed,
leveraging the existing @ml_function decorator metadata system.
"""

from dataclasses import dataclass, field
from typing import Optional, Set, Dict, List
from difflib import get_close_matches

from mlpy.stdlib.decorators import (
    get_module_metadata,
    get_all_modules,
    ModuleMetadata,
)


@dataclass
class AllowedFunctionsRegistry:
    """Registry of all allowed functions in current compilation context.

    This is the WHITELIST - only functions in this registry can be called.
    Everything else is blocked at compile time with helpful error messages.

    The whitelist has three categories:
    1. ML builtin functions (from @ml_function in builtin.py)
    2. User-defined functions (from function declarations in ML code)
    3. Imported stdlib functions (from @ml_function in imported modules)
    """

    # Category 1: ML builtin functions (always available)
    builtin_functions: Set[str] = field(default_factory=set)

    # Category 2: User-defined functions (from current ML file)
    user_defined_functions: Set[str] = field(default_factory=set)

    # Category 3: Imported stdlib modules and their functions
    # Maps: module_alias -> ModuleMetadata
    imported_modules: Dict[str, ModuleMetadata] = field(default_factory=dict)

    def __post_init__(self):
        """Initialize builtin functions from decorator metadata."""
        self._load_builtin_functions()

    def _load_builtin_functions(self) -> None:
        """Load ML builtin functions from decorator metadata.

        This leverages the existing @ml_function decorators in builtin.py,
        ensuring we have a single source of truth.
        """
        builtin_metadata = get_module_metadata("builtin")
        if builtin_metadata:
            self.builtin_functions = set(builtin_metadata.functions.keys())
        else:
            # Failsafe: builtin module should always be registered
            raise RuntimeError(
                "Builtin module not found in registry. "
                "Ensure mlpy.stdlib.builtin is imported and decorated with @ml_module."
            )

    # =========================================================================
    # Category 1: ML Builtin Functions
    # =========================================================================

    def is_allowed_builtin(self, func_name: str) -> bool:
        """Check if function is an ML builtin function.

        Args:
            func_name: Name of the function to check

        Returns:
            True if function is decorated with @ml_function in builtin module

        Example:
            >>> registry = AllowedFunctionsRegistry()
            >>> registry.is_allowed_builtin("int")
            True
            >>> registry.is_allowed_builtin("open")  # Python builtin, not ML
            False
        """
        return func_name in self.builtin_functions

    # =========================================================================
    # Category 2: User-Defined Functions
    # =========================================================================

    def is_user_defined(self, func_name: str) -> bool:
        """Check if function is user-defined in current ML code.

        Args:
            func_name: Name of the function to check

        Returns:
            True if function was declared in the ML source being compiled
        """
        return func_name in self.user_defined_functions

    def add_user_function(self, func_name: str) -> None:
        """Register a user-defined function during AST traversal.

        Called when the code generator encounters a function declaration.

        Args:
            func_name: Name of the function being defined
        """
        self.user_defined_functions.add(func_name)

    # =========================================================================
    # Category 3: Imported Stdlib Functions
    # =========================================================================

    def is_imported_function(self, module_name: str, func_name: str) -> bool:
        """Check if function exists in an imported stdlib module.

        Args:
            module_name: The module alias used in code (e.g., 'str' for 'import string as str')
            func_name: The function name

        Returns:
            True if the module is imported and has this function

        Example:
            >>> registry = AllowedFunctionsRegistry()
            >>> registry.add_imported_module("string", "string")
            >>> registry.is_imported_function("string", "upper")
            True
            >>> registry.is_imported_function("string", "nonexistent")
            False
        """
        if module_name not in self.imported_modules:
            return False

        module_metadata = self.imported_modules[module_name]
        return func_name in module_metadata.functions

    def add_imported_module(self, module_alias: str, module_name: str) -> bool:
        """Register an imported stdlib module during import statement processing.

        Args:
            module_alias: The name used in code (e.g., 'str' for 'import string as str')
            module_name: The actual module name (e.g., 'string')

        Returns:
            True if module exists in ML stdlib and was added, False otherwise

        Example:
            >>> registry = AllowedFunctionsRegistry()
            >>> registry.add_imported_module("string", "string")
            True
            >>> registry.add_imported_module("fake", "nonexistent")
            False
        """
        metadata = get_module_metadata(module_name)
        if metadata:
            self.imported_modules[module_alias] = metadata
            return True
        return False

    def get_imported_module_functions(self, module_name: str) -> Set[str]:
        """Get all functions available in an imported module.

        Args:
            module_name: The module alias

        Returns:
            Set of function names, or empty set if module not imported
        """
        if module_name not in self.imported_modules:
            return set()
        return set(self.imported_modules[module_name].functions.keys())

    # =========================================================================
    # Helper Methods for Error Messages
    # =========================================================================

    def get_available_functions(self) -> Dict[str, any]:
        """Get all available functions for error messages.

        Returns:
            Dict with 'builtins', 'user_defined', and 'imported' keys
        """
        return {
            "builtins": sorted(self.builtin_functions),
            "user_defined": sorted(self.user_defined_functions),
            "imported": {
                module: sorted(metadata.functions.keys())
                for module, metadata in self.imported_modules.items()
            }
        }

    def suggest_alternatives(self, func_name: str) -> List[str]:
        """Suggest similar function names for typos.

        Uses difflib to find close matches among all available functions.

        Args:
            func_name: The unknown function name

        Returns:
            List of up to 3 similar function names
        """
        # Collect all available function names
        all_functions = list(self.builtin_functions)
        all_functions.extend(self.user_defined_functions)
        for metadata in self.imported_modules.values():
            all_functions.extend(metadata.functions.keys())

        # Find close matches (60% similarity threshold)
        matches = get_close_matches(func_name, all_functions, n=3, cutoff=0.6)
        return matches

    def get_available_modules(self) -> List[str]:
        """Get list of all available ML stdlib modules.

        Returns:
            Sorted list of module names
        """
        all_modules = get_all_modules()
        return sorted(all_modules.keys())


__all__ = [
    "AllowedFunctionsRegistry",
]
```

**Lines of Code**: ~200
**Estimated Time**: 2 hours (including tests)

---

### Component 2: Enhanced Python Code Generator

**File**: `src/mlpy/ml/codegen/python_generator.py` (MODIFIED)

**Changes**:

#### Change 1: Import Registry

```python
# Add to imports at top of file
from mlpy.ml.codegen.function_registry import AllowedFunctionsRegistry
```

#### Change 2: Add Registry to CodeGenContext

```python
@dataclass
class CodeGenContext:
    """Context for code generation."""
    # ... existing fields ...

    # Track which builtin functions are used (for import generation)
    builtin_functions_used: set[str] = field(default_factory=set)
    builtin_import_added: bool = False
```

#### Change 3: Initialize Registry in Generator

```python
class PythonCodeGenerator(ASTVisitor):
    def __init__(self, source_file: str = ""):
        # ... existing initialization ...

        # NEW: Initialize function whitelist
        self.function_registry = AllowedFunctionsRegistry()
```

#### Change 4: Register User Functions

```python
def visit_function_declaration(self, node: FunctionDeclaration):
    """Generate Python function definition and register in whitelist."""

    # NEW: Register user function in whitelist
    self.function_registry.add_user_function(node.name)

    # ... existing code generation ...
```

#### Change 5: Register Imported Modules

```python
def visit_import_statement(self, node: ImportStatement):
    """Generate Python import and register in whitelist."""

    module_name = node.module_path
    alias = node.alias if node.alias else module_name

    # NEW: Check if module exists in ML stdlib
    if not self.function_registry.add_imported_module(alias, module_name):
        # Unknown module - not in ML stdlib
        available_modules = self.function_registry.get_available_modules()
        raise CodeGenError(
            f"Unknown module '{module_name}'.\n"
            f"Available ML stdlib modules: {', '.join(available_modules)}\n"
            f"\nNote: Only ML stdlib modules can be imported. "
            f"Python modules are not accessible for security."
        )

    # ... existing import generation code ...
```

#### Change 6: Whitelist-Based Function Call Generation (CORE CHANGE)

```python
def _generate_expression(self, expr: Expression) -> str:
    """Generate Python code for an expression."""
    # ... existing code for other expression types ...

    elif isinstance(expr, FunctionCall):
        return self._generate_function_call(expr)

    # ... rest of method ...


def _generate_function_call(self, expr: FunctionCall) -> str:
    """Generate function call with whitelist enforcement.

    This is the CORE of the whitelist strategy. Only functions in the
    whitelist (ML builtins, user-defined, or imported stdlib) are allowed.
    Everything else is blocked at compile time.

    Args:
        expr: FunctionCall AST node

    Returns:
        Generated Python code for the function call

    Raises:
        CodeGenError: If function is not in whitelist
    """

    # Handle different function expression types
    if isinstance(expr.function, Identifier):
        # Simple function call: func()
        func_name = expr.function.name
        return self._generate_simple_function_call(func_name, expr.arguments)

    elif isinstance(expr.function, MemberAccess):
        # Method call: obj.method() or module.function()
        return self._generate_member_function_call(expr)

    else:
        # Complex expression (lambda, etc.)
        func_code = self._generate_expression(expr.function)
        args = [self._generate_expression(arg) for arg in expr.arguments]
        return f"{func_code}({', '.join(args)})"


def _generate_simple_function_call(self, func_name: str, arguments: list) -> str:
    """Generate simple function call with whitelist check.

    Checks whitelist in order:
    1. ML builtin? → Generate builtin.func()
    2. User-defined? → Generate func()
    3. None of above? → CodeGenError

    Args:
        func_name: Name of the function
        arguments: List of argument expressions

    Returns:
        Generated Python code

    Raises:
        CodeGenError: If function not in whitelist
    """
    args = [self._generate_expression(arg) for arg in arguments]
    args_str = ', '.join(args)

    # Category 1: ML Builtin Functions
    if self.function_registry.is_allowed_builtin(func_name):
        # Track for import generation
        self.context.builtin_functions_used.add(func_name)
        # Route to builtin module
        return f"builtin.{func_name}({args_str})"

    # Category 2: User-Defined Functions
    elif self.function_registry.is_user_defined(func_name):
        # Direct call to user function
        return f"{self._safe_identifier(func_name)}({args_str})"

    # Category 4: BLOCKED - Not in whitelist
    else:
        self._raise_unknown_function_error(func_name)


def _generate_member_function_call(self, expr: FunctionCall) -> str:
    """Generate member function call (module.func or obj.method).

    For module functions (e.g., string.upper), checks whitelist.
    For object methods, generates attribute access.

    Args:
        expr: FunctionCall with MemberAccess as function

    Returns:
        Generated Python code

    Raises:
        CodeGenError: If module function not in whitelist
    """
    member_access = expr.function
    args = [self._generate_expression(arg) for arg in expr.arguments]
    args_str = ', '.join(args)

    # Check if this is a module function call
    if isinstance(member_access.object, Identifier):
        obj_name = member_access.object.name
        func_name = member_access.member

        # Category 3: Imported Stdlib Module Functions
        if self.function_registry.is_imported_function(obj_name, func_name):
            # Known stdlib function
            return f"{obj_name}.{func_name}({args_str})"

        # Check if this is an imported module but unknown function
        if obj_name in self.function_registry.imported_modules:
            self._raise_unknown_module_function_error(obj_name, func_name)

    # Not a module function - treat as object method call
    # (Allow these - they're operating on runtime objects)
    obj_code = self._generate_expression(member_access.object)
    member_code = member_access.member
    return f"{obj_code}.{member_code}({args_str})"


def _raise_unknown_function_error(self, func_name: str) -> None:
    """Raise comprehensive error for unknown function.

    Provides:
    - Clear error message
    - Suggestions for similar function names (typos)
    - List of available functions
    - Hints for how to access more functions

    Args:
        func_name: The unknown function name

    Raises:
        CodeGenError: Always
    """
    available = self.function_registry.get_available_functions()
    suggestions = self.function_registry.suggest_alternatives(func_name)

    # Build comprehensive error message
    error_lines = [
        f"Unknown function '{func_name}'.",
        ""
    ]

    # Add suggestions for typos
    if suggestions:
        error_lines.append(f"Did you mean: {', '.join(suggestions)}?")
        error_lines.append("")

    # Add available functions
    error_lines.append("Available functions:")

    # ML Builtins
    builtins = available['builtins']
    if len(builtins) <= 10:
        error_lines.append(f"  ML Builtins: {', '.join(builtins)}")
    else:
        error_lines.append(f"  ML Builtins: {', '.join(builtins[:10])} ... ({len(builtins)} total)")

    # User-defined
    if available['user_defined']:
        error_lines.append(f"  User-defined: {', '.join(available['user_defined'])}")

    # Imported modules
    if available['imported']:
        error_lines.append("  Imported modules:")
        for module, funcs in available['imported'].items():
            if len(funcs) <= 5:
                error_lines.append(f"    {module}: {', '.join(funcs)}")
            else:
                error_lines.append(f"    {module}: {', '.join(funcs[:5])} ... ({len(funcs)} total)")

    # Add hints
    error_lines.append("")
    error_lines.append("To access additional functions:")
    error_lines.append("  - Import ML stdlib modules: import string; import math;")
    error_lines.append("  - Define your own functions: function myFunc(x) { ... }")
    error_lines.append("")
    error_lines.append("Note: Python built-in functions are not accessible for security.")

    raise CodeGenError('\n'.join(error_lines))


def _raise_unknown_module_function_error(self, module_name: str, func_name: str) -> None:
    """Raise error for unknown function in known module.

    Args:
        module_name: The module name
        func_name: The unknown function name

    Raises:
        CodeGenError: Always
    """
    available_funcs = list(
        self.function_registry.get_imported_module_functions(module_name)
    )
    suggestions = get_close_matches(func_name, available_funcs, n=3, cutoff=0.6)

    error_lines = [
        f"Module '{module_name}' has no function '{func_name}'.",
        ""
    ]

    if suggestions:
        error_lines.append(f"Did you mean: {', '.join(suggestions)}?")
        error_lines.append("")

    error_lines.append(f"Available functions in '{module_name}':")
    error_lines.append(f"  {', '.join(sorted(available_funcs))}")

    raise CodeGenError('\n'.join(error_lines))
```

#### Change 7: Ensure Builtin Import

```python
def _ensure_builtin_imported(self) -> None:
    """Ensure builtin module is imported if any builtin functions are used."""
    if self.context.builtin_functions_used and not self.context.builtin_import_added:
        self.context.builtin_import_added = True
        self.context.imports_needed.add("from mlpy.stdlib.builtin import builtin")


def _emit_imports(self):
    """Emit necessary Python imports."""
    # NEW: Ensure builtin import is added if needed
    self._ensure_builtin_imported()

    # ... existing import emission code ...
```

**Lines Modified**: ~150 lines (new methods + modifications)
**Estimated Time**: 3 hours (including refactoring and testing)

---

### Component 3: Enhanced Error Types

**File**: `src/mlpy/ml/errors.py` (if not already existing)

```python
class CodeGenError(Exception):
    """Error during code generation (transpilation).

    Raised when code generation fails, typically due to:
    - Unknown function calls (not in whitelist)
    - Unknown module imports
    - Invalid syntax that passed parsing but can't be transpiled
    """
    pass
```

**Lines Added**: ~10
**Estimated Time**: 15 minutes

---

## Success Criteria

### Integration Tests: ml_builtin Category

**Test Command**:
```bash
python tests/ml_test_runner.py --full --category ml_builtin --matrix
```

**Current Results** (Before Implementation):
```
Overall Results: Pass=5 (31.2%), Fail=11 (68.8%), Error=0 (0.0%)

Passing Tests:
  08_predicate_functions.ml (callable, all, any)
  09_sum_function.ml
  10_char_conversions.ml (chr, ord)
  11_number_base_conversions.ml (hex, bin, oct)
  12_string_representations.ml (repr, format)

Failing Tests:
  01_type_conversion.ml - int("3.14") fails
  02_type_checking.ml - typeof not defined
  03_collection_functions.ml - enumerate returns iterator
  04_print_functions.ml - typeof not defined
  05_math_utilities.ml - min/max parameter issues
  06_array_utilities.ml - sorted parameter issues
  07_object_utilities.ml - keys/values not defined
  13_reversed_function.ml - reversed returns iterator
  14_dynamic_introspection.ml - security blocks
  15_edge_cases.ml - keys/typeof not defined
  16_comprehensive_integration.ml - multiple issues
```

**Expected Results** (After Implementation):
```
Overall Results: Pass=16 (100%), Fail=0 (0%), Error=0 (0%)

All 16 tests should PASS:
  ✅ 01_type_conversion.ml
  ✅ 02_type_checking.ml
  ✅ 03_collection_functions.ml
  ✅ 04_print_functions.ml
  ✅ 05_math_utilities.ml
  ✅ 06_array_utilities.ml
  ✅ 07_object_utilities.ml
  ✅ 08_predicate_functions.ml
  ✅ 09_sum_function.ml
  ✅ 10_char_conversions.ml
  ✅ 11_number_base_conversions.ml
  ✅ 12_string_representations.ml
  ✅ 13_reversed_function.ml
  ✅ 14_dynamic_introspection.ml
  ✅ 15_edge_cases.ml
  ✅ 16_comprehensive_integration.ml

Execution Success Rate: 100% (16/16)
```

**Success Metric**: **31.2% → 100% pass rate (+68.8% improvement)**

---

### Unit Tests: Builtin Integration Issues

**Test File**: `tests/unit/stdlib/test_builtin_integration_issues.py`

**Test Command**:
```bash
python -m pytest tests/unit/stdlib/test_builtin_integration_issues.py -v --no-cov
```

**Current Results** (Before Implementation):
```
TestBuiltinIntegrationIssues:
  test_int_with_float_string - FAIL (ML execution fails, direct call passes)
  ... (64 other tests PASS - direct builtin calls work)

TestPythonBuiltinShadowing:
  test_type_function_should_not_exist - XFAIL (type() accessible)
  test_id_function_should_use_ml_version - XFAIL (id() exposes memory)
  test_open_function_should_not_be_callable - XFAIL (open() accessible)

Total: 64 passed, 1 failed, 3 xfailed
```

**Expected Results** (After Implementation):
```
TestBuiltinIntegrationIssues:
  test_int_with_float_string - PASS (routes to builtin.int())
  ... (all 65 tests PASS)

TestPythonBuiltinShadowing:
  test_type_function_should_not_exist - PASS (raises CodeGenError)
  test_id_function_should_use_ml_version - PASS (routes to builtin.id())
  test_open_function_should_not_be_callable - PASS (raises CodeGenError)

Total: 68 passed, 0 failed, 0 xfailed
```

**Success Metric**: **All tests pass, no xfails remain**

---

### Unit Tests: Function Registry

**Test File**: `tests/unit/codegen/test_function_registry.py` (NEW)

**Test Command**:
```bash
python -m pytest tests/unit/codegen/test_function_registry.py -v --no-cov
```

**Required Tests**:

```python
"""Unit tests for AllowedFunctionsRegistry."""

import pytest
from mlpy.ml.codegen.function_registry import AllowedFunctionsRegistry


class TestBuiltinFunctions:
    """Test ML builtin function recognition."""

    def test_builtin_functions_loaded_from_metadata(self):
        """Test that builtin functions are loaded from decorator metadata."""
        registry = AllowedFunctionsRegistry()

        # Should have all ML builtin functions
        assert len(registry.builtin_functions) > 0
        assert "int" in registry.builtin_functions
        assert "typeof" in registry.builtin_functions
        assert "len" in registry.builtin_functions

    def test_is_allowed_builtin_positive(self):
        """Test that known builtins are identified."""
        registry = AllowedFunctionsRegistry()

        assert registry.is_allowed_builtin("int") is True
        assert registry.is_allowed_builtin("typeof") is True
        assert registry.is_allowed_builtin("enumerate") is True

    def test_is_allowed_builtin_negative(self):
        """Test that non-builtins are rejected."""
        registry = AllowedFunctionsRegistry()

        assert registry.is_allowed_builtin("open") is False
        assert registry.is_allowed_builtin("eval") is False
        assert registry.is_allowed_builtin("type") is False


class TestUserDefinedFunctions:
    """Test user-defined function tracking."""

    def test_add_user_function(self):
        """Test adding user-defined functions."""
        registry = AllowedFunctionsRegistry()

        registry.add_user_function("myFunc")
        assert registry.is_user_defined("myFunc") is True

    def test_is_user_defined_negative(self):
        """Test that unknown functions are not user-defined."""
        registry = AllowedFunctionsRegistry()

        assert registry.is_user_defined("unknown") is False


class TestImportedModules:
    """Test imported stdlib module tracking."""

    def test_add_imported_module_success(self):
        """Test importing valid ML stdlib module."""
        registry = AllowedFunctionsRegistry()

        result = registry.add_imported_module("string", "string")
        assert result is True
        assert "string" in registry.imported_modules

    def test_add_imported_module_failure(self):
        """Test importing non-existent module."""
        registry = AllowedFunctionsRegistry()

        result = registry.add_imported_module("fake", "nonexistent")
        assert result is False
        assert "fake" not in registry.imported_modules

    def test_is_imported_function_positive(self):
        """Test that imported module functions are recognized."""
        registry = AllowedFunctionsRegistry()
        registry.add_imported_module("string", "string")

        # String module should have these functions
        assert registry.is_imported_function("string", "upper") is True
        assert registry.is_imported_function("string", "lower") is True

    def test_is_imported_function_negative(self):
        """Test that non-existent module functions are rejected."""
        registry = AllowedFunctionsRegistry()
        registry.add_imported_module("string", "string")

        assert registry.is_imported_function("string", "nonexistent") is False


class TestSuggestions:
    """Test suggestion system for typos."""

    def test_suggest_alternatives_typo(self):
        """Test suggestions for typos."""
        registry = AllowedFunctionsRegistry()
        registry.add_user_function("double")

        suggestions = registry.suggest_alternatives("dubble")
        assert "double" in suggestions

    def test_suggest_alternatives_no_match(self):
        """Test suggestions when no close match."""
        registry = AllowedFunctionsRegistry()

        suggestions = registry.suggest_alternatives("xyz123")
        assert len(suggestions) == 0


class TestAvailableFunctions:
    """Test getting available functions for error messages."""

    def test_get_available_functions(self):
        """Test getting all available functions."""
        registry = AllowedFunctionsRegistry()
        registry.add_user_function("myFunc")
        registry.add_imported_module("string", "string")

        available = registry.get_available_functions()

        assert "builtins" in available
        assert "user_defined" in available
        assert "imported" in available

        assert "int" in available["builtins"]
        assert "myFunc" in available["user_defined"]
        assert "string" in available["imported"]
```

**Success Metric**: **All registry tests pass**

---

### Unit Tests: Code Generation Whitelist

**Test File**: `tests/unit/codegen/test_whitelist_code_generation.py` (NEW)

**Test Command**:
```bash
python -m pytest tests/unit/codegen/test_whitelist_code_generation.py -v --no-cov
```

**Required Tests**:

```python
"""Unit tests for whitelist-based code generation."""

import pytest
from mlpy.ml.transpiler import MLTranspiler
from mlpy.ml.errors import CodeGenError


class TestBuiltinFunctionGeneration:
    """Test ML builtin function code generation."""

    def test_builtin_function_routed_correctly(self):
        """Test that ML builtin functions are routed to builtin module."""
        transpiler = MLTranspiler()

        ml_code = 'x = int("42");'
        python_code, _, _ = transpiler.transpile_to_python(ml_code)

        assert "from mlpy.stdlib.builtin import builtin" in python_code
        assert "builtin.int" in python_code
        assert python_code.count("builtin.int") == 1

    def test_multiple_builtins_routed(self):
        """Test multiple builtin functions in same code."""
        transpiler = MLTranspiler()

        ml_code = 'x = int("42"); t = typeof(x); l = len([1,2,3]);'
        python_code, _, _ = transpiler.transpile_to_python(ml_code)

        assert "builtin.int" in python_code
        assert "builtin.typeof" in python_code
        assert "builtin.len" in python_code


class TestUserDefinedFunctionGeneration:
    """Test user-defined function code generation."""

    def test_user_function_not_transformed(self):
        """Test that user-defined functions are not transformed."""
        transpiler = MLTranspiler()

        ml_code = '''
        function double(x) { return x * 2; }
        y = double(5);
        '''
        python_code, _, _ = transpiler.transpile_to_python(ml_code)

        assert "def double" in python_code
        assert "double(5)" in python_code
        assert "builtin.double" not in python_code

    def test_user_function_shadows_builtin_name(self):
        """Test that user function with builtin name is not transformed."""
        transpiler = MLTranspiler()

        ml_code = '''
        function int(x) { return x * 2; }
        y = int(5);
        '''
        python_code, _, _ = transpiler.transpile_to_python(ml_code)

        # Should call user's int(), not builtin.int()
        assert "def int" in python_code
        assert "int(5)" in python_code
        assert "builtin.int" not in python_code


class TestImportedModuleFunctionGeneration:
    """Test imported stdlib module function code generation."""

    def test_imported_function_routed(self):
        """Test that imported module functions work."""
        transpiler = MLTranspiler()

        ml_code = 'import string; x = string.upper("hello");'
        python_code, _, _ = transpiler.transpile_to_python(ml_code)

        assert "import" in python_code.lower() or "from" in python_code.lower()
        assert "string" in python_code.lower()
        assert "upper" in python_code


class TestUnknownFunctionBlocking:
    """Test that unknown functions are blocked."""

    def test_python_builtin_open_blocked(self):
        """Test that Python's open() is blocked."""
        transpiler = MLTranspiler()

        ml_code = 'f = open("file.txt");'

        with pytest.raises(CodeGenError) as exc_info:
            transpiler.transpile_to_python(ml_code)

        assert "Unknown function 'open'" in str(exc_info.value)

    def test_python_builtin_eval_blocked(self):
        """Test that Python's eval() is blocked."""
        transpiler = MLTranspiler()

        ml_code = 'x = eval("1+1");'

        with pytest.raises(CodeGenError) as exc_info:
            transpiler.transpile_to_python(ml_code)

        assert "Unknown function 'eval'" in str(exc_info.value)

    def test_python_builtin_type_blocked(self):
        """Test that Python's type() is blocked."""
        transpiler = MLTranspiler()

        ml_code = 'x = type(42);'

        with pytest.raises(CodeGenError) as exc_info:
            transpiler.transpile_to_python(ml_code)

        assert "Unknown function 'type'" in str(exc_info.value)

    def test_typo_blocked_with_suggestion(self):
        """Test that typos are blocked with helpful suggestions."""
        transpiler = MLTranspiler()

        ml_code = 'x = intt("42");'  # Typo: intt instead of int

        with pytest.raises(CodeGenError) as exc_info:
            transpiler.transpile_to_python(ml_code)

        error_msg = str(exc_info.value)
        assert "Unknown function 'intt'" in error_msg
        assert "int" in error_msg  # Should suggest 'int'


class TestUnknownModuleBlocking:
    """Test that unknown modules are blocked."""

    def test_unknown_module_blocked(self):
        """Test that importing unknown module is blocked."""
        transpiler = MLTranspiler()

        ml_code = 'import nonexistent;'

        with pytest.raises(CodeGenError) as exc_info:
            transpiler.transpile_to_python(ml_code)

        assert "Unknown module 'nonexistent'" in str(exc_info.value)


class TestUnknownModuleFunctionBlocking:
    """Test that unknown functions in known modules are blocked."""

    def test_unknown_function_in_module_blocked(self):
        """Test that unknown function in imported module is blocked."""
        transpiler = MLTranspiler()

        ml_code = 'import string; x = string.nonexistent("test");'

        with pytest.raises(CodeGenError) as exc_info:
            transpiler.transpile_to_python(ml_code)

        error_msg = str(exc_info.value)
        assert "string" in error_msg
        assert "nonexistent" in error_msg
```

**Success Metric**: **All whitelist code generation tests pass**

---

## Implementation Plan

### Phase 1: Core Implementation (5 hours)

**Tasks**:
1. Create `function_registry.py` with `AllowedFunctionsRegistry` (2 hours)
2. Modify `python_generator.py` with whitelist checks (3 hours)
   - Add registry initialization
   - Track user functions
   - Track imports
   - Implement whitelist-based function call generation
   - Add error generation

**Deliverables**:
- ✅ `src/mlpy/ml/codegen/function_registry.py`
- ✅ Enhanced `src/mlpy/ml/codegen/python_generator.py`
- ✅ Basic functionality working

**Validation**:
```bash
# Quick test that basic routing works
python -c "from mlpy.ml.transpiler import MLTranspiler; t = MLTranspiler(); code, _, _ = t.transpile_to_python('x = int(\"42\");'); print('builtin.int' in code)"
# Should print: True
```

---

### Phase 2: Error Messages & Testing (3 hours)

**Tasks**:
1. Implement comprehensive error messages (1 hour)
   - Unknown function errors
   - Unknown module errors
   - Unknown module function errors
   - Suggestions for typos
2. Write unit tests for registry (1 hour)
   - `tests/unit/codegen/test_function_registry.py`
3. Write unit tests for code generation (1 hour)
   - `tests/unit/codegen/test_whitelist_code_generation.py`

**Deliverables**:
- ✅ Helpful error messages with suggestions
- ✅ Complete unit test coverage
- ✅ All unit tests passing

**Validation**:
```bash
# Run unit tests
pytest tests/unit/codegen/test_function_registry.py -v
pytest tests/unit/codegen/test_whitelist_code_generation.py -v

# Should see: All tests passed
```

---

### Phase 3: Integration Testing (2 hours)

**Tasks**:
1. Run existing builtin integration issues tests (30 min)
2. Fix any issues discovered (30 min)
3. Run ml_builtin integration tests (30 min)
4. Fix any remaining issues (30 min)

**Deliverables**:
- ✅ All unit tests pass
- ✅ All integration tests pass
- ✅ Success criteria met

**Validation**:
```bash
# Run builtin integration issues tests
pytest tests/unit/stdlib/test_builtin_integration_issues.py -v

# Run ml_builtin integration tests
python tests/ml_test_runner.py --full --category ml_builtin --matrix

# Should see:
# - Unit tests: 68 passed
# - Integration tests: 16/16 passed (100%)
```

---

### Phase 4: Documentation & Cleanup (1 hour)

**Tasks**:
1. Update developer guide with whitelist approach (30 min)
2. Add code comments and docstrings (15 min)
3. Clean up any debug code (15 min)

**Deliverables**:
- ✅ Updated documentation
- ✅ Clean, well-commented code
- ✅ Ready for production

---

## Total Effort Estimate

| Phase | Hours | Tasks |
|-------|-------|-------|
| Phase 1: Core Implementation | 5 | Registry + Code Generator |
| Phase 2: Error Messages & Unit Tests | 3 | Errors + Tests |
| Phase 3: Integration Testing | 2 | Run tests + Fix issues |
| Phase 4: Documentation | 1 | Docs + Cleanup |
| **TOTAL** | **11 hours** | Complete implementation |

**Buffer**: Add 2 hours for unexpected issues
**Final Estimate**: **11-13 hours**

---

## Success Metrics Summary

### Integration Tests
- **Before**: 5/16 passing (31.2%)
- **After**: 16/16 passing (100%)
- **Improvement**: +68.8 percentage points

### Unit Tests
- **Before**: 64 passed, 1 failed, 3 xfailed
- **After**: 68 passed, 0 failed, 0 xfailed
- **New Tests**: ~30 additional tests for registry and whitelist

### Security
- **Before**: Python builtins accessible (open, eval, type)
- **After**: All unknown functions blocked at compile time
- **Improvement**: Complete security gap closure

### Code Quality
- **Error Messages**: Helpful with suggestions
- **Maintainability**: Uses decorator metadata (single source of truth)
- **Extensibility**: Works for all stdlib modules automatically

---

## Risk Assessment

### Implementation Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Breaking existing code | Low | Medium | Comprehensive tests, user function shadowing support |
| Performance impact | Very Low | Low | O(1) lookups, compile-time only |
| Decorator metadata not available | Very Low | High | Failsafe error, existing infrastructure |
| Edge cases in function calls | Medium | Medium | Extensive testing, handle all AST node types |

### Rollback Plan

If issues discovered after deployment:

1. **Quick Fix**: Add flag to disable whitelist temporarily
```python
STRICT_WHITELIST_MODE = False  # Temporarily disable
```

2. **Rollback**: Revert to previous commit
3. **Fix Forward**: Address issues and redeploy

---

## Post-Implementation Validation

### Validation Checklist

After implementation, verify:

- [ ] All 16 ml_builtin integration tests pass
- [ ] All 68 unit tests pass (no xfails)
- [ ] `open()` raises CodeGenError
- [ ] `eval()` raises CodeGenError
- [ ] `type()` raises CodeGenError
- [ ] `int()` routes to `builtin.int()`
- [ ] `typeof()` routes to `builtin.typeof()`
- [ ] User-defined functions not transformed
- [ ] Imported stdlib functions work
- [ ] Error messages helpful and accurate
- [ ] No performance regression (< 5% overhead)

### Performance Testing

```bash
# Benchmark transpilation time
python -m pytest tests/performance/test_transpiler_benchmarks.py -v
```

**Expected**: < 5% performance impact (whitelist lookups are O(1))

---

## Future Enhancements

### Phase 2 (Future)

1. **Capability Warnings**: Warn when importing modules requiring capabilities
2. **Function Documentation**: Show function signatures in errors
3. **IDE Integration**: Autocomplete for available functions
4. **Strict Mode Levels**: Configurable strictness (warn vs error)

---

## Conclusion

This proposal provides a **complete, secure, and maintainable solution** to the Python builtin shadowing problem.

**Key Strengths**:
- ✅ **Whitelist approach**: Secure by default
- ✅ **Leverages existing infrastructure**: Decorator metadata
- ✅ **Comprehensive testing**: 68+ tests
- ✅ **Helpful error messages**: With suggestions
- ✅ **Reasonable effort**: 11-13 hours
- ✅ **Future-proof**: Scales to all modules

**Success Criteria**:
- ✅ **Integration tests**: 31.2% → 100%
- ✅ **Unit tests**: All passing, no xfails
- ✅ **Security**: Complete gap closure

**Recommendation**: **APPROVED FOR IMPLEMENTATION**

---

**Status**: Ready to implement
**Priority**: CRITICAL
**Timeline**: 11-13 hours
**Success Metrics**: Clearly defined and measurable
**Risk**: Low with comprehensive testing
