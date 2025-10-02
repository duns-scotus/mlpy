# Nonlocal Statement Implementation

**Date:** October 2, 2025
**Session:** ML Core Language Enhancement
**Status:** ✅ Complete and Tested

## Overview

Added explicit `nonlocal` statement to ML language to handle closure variable modification, matching Python's scope control mechanism.

## Problem

Closures that modify outer scope variables were failing with `UnboundLocalError`:

```ml
function create_counter(initial) {
    count = initial;
    function increment() {
        count = count + 1;  // ERROR: UnboundLocalError
        return count;
    }
    return increment;
}
```

**Root Cause:** Python requires explicit `nonlocal` declaration to modify variables from enclosing scopes. Without it, assignment creates a new local variable, but reading before assignment causes error.

## Solution

Added explicit `nonlocal` statement to ML language rather than implementing complex automatic scope inference.

### Grammar Extension

```lark
// Statements
?statement: ...
          | nonlocal_statement

// Scope Control
nonlocal_statement: "nonlocal" IDENTIFIER ("," IDENTIFIER)* ";"
```

### AST Node

```python
class NonlocalStatement(Statement):
    """Nonlocal statement for closure variable access."""
    def __init__(self, variables: list[str], ...):
        self.variables = variables
```

### Code Generation

Emits Python `nonlocal` declarations directly:

```python
def visit_nonlocal_statement(self, node: NonlocalStatement):
    variables = ", ".join(node.variables)
    self._emit_line(f"nonlocal {variables}", node)
```

## Usage

```ml
function create_counter(initial) {
    count = initial;

    function increment() {
        nonlocal count;  // Explicit declaration required
        count = count + 1;
        return count;
    }

    return increment;
}

counter = create_counter(10);
result1 = counter();  // 11
result2 = counter();  // 12
result3 = counter();  // 13
```

### Multiple Variables

```ml
function create_account(balance) {
    transactions = 0;

    function deposit(amount) {
        nonlocal balance, transactions;  // Multiple variables
        balance = balance + amount;
        transactions = transactions + 1;
        return balance;
    }

    return deposit;
}
```

## Implementation Details

### Files Modified

1. **`src/mlpy/ml/grammar/ml.lark`**
   - Added `nonlocal_statement` to statement types
   - Added grammar rule with comma-separated identifiers

2. **`src/mlpy/ml/grammar/ast_nodes.py`**
   - Added `NonlocalStatement` class with `variables` list

3. **`src/mlpy/ml/grammar/transformer.py`**
   - Added `nonlocal_statement()` transformer method
   - Handles both Token and Identifier node types

4. **`src/mlpy/ml/codegen/python_generator.py`**
   - Added `visit_nonlocal_statement()` code generator
   - Emits Python `nonlocal` declarations

5. **`src/mlpy/ml/analysis/security_analyzer.py`**
   - Added `visit_nonlocal_statement()` visitor (no-op)
   - No security concerns with nonlocal declarations

### Test Files

1. **`tests/ml_integration/ml_core/test_nonlocal.ml`** - New test demonstrating basic usage
2. **`tests/ml_integration/ml_core/07_closures_functions.ml`** - Updated with nonlocal declarations

## Results

### Test Success Rate
- **Before:** 20/24 passing (83.3%)
- **After:** 21/25 passing (84.0%)
- **Fixed:** `07_closures_functions.ml` (was UnboundLocalError)

### Closure Tests Passing
- ✅ Simple counter closures
- ✅ Account with multiple closure functions
- ✅ Sequence generators with state
- ✅ Person objects with private variables
- ✅ Independent closure instances

## Design Rationale

### Why Explicit `nonlocal`?

**Considered Alternatives:**
1. **Automatic scope inference** - Would require complex static analysis to detect:
   - Which variables are assigned in nested functions
   - Whether those variables exist in parent scopes
   - Handling deeply nested scopes (3+ levels)

2. **Different syntax** - Would diverge from Python semantics, causing confusion

**Chosen Approach:**
- Explicit `nonlocal` statement matching Python
- Simpler implementation (no scope tracking needed)
- Clear developer intent
- Familiar to Python developers
- Prevents accidental shadowing

### Advantages
- ✅ Simple and explicit
- ✅ Matches Python semantics exactly
- ✅ No complex scope analysis required
- ✅ Clear code intent
- ✅ Prevents bugs from implicit behavior

### Trade-offs
- ⚠️ Requires developer to write `nonlocal` declarations
- ⚠️ More verbose than automatic inference
- ✅ But: Makes closure behavior explicit and obvious

## TODO: Documentation

**⚠️ IMPORTANT:** The `nonlocal` statement needs to be documented in the Language Reference.

### Documentation Tasks

1. **Language Reference (`docs/source/language_reference.rst`)**
   - Add "Nonlocal Statement" section under "Statements"
   - Explain scope rules and when nonlocal is required
   - Provide examples of closure patterns
   - Document syntax: `nonlocal var1, var2, ...;`
   - Note differences from Python (semicolon required)

2. **Tutorial Updates (`docs/source/tutorial.rst`)**
   - Add closure examples using nonlocal
   - Explain common closure patterns
   - Show error messages without nonlocal

3. **Migration Guide**
   - Note for users: Closures require explicit nonlocal
   - Provide error diagnostic examples
   - Show before/after code examples

### Documentation Sections Needed

```rst
Nonlocal Statement
==================

The ``nonlocal`` statement declares that variables are from an enclosing
function scope, allowing inner functions to modify outer variables.

Syntax
------

.. code-block:: ml

   nonlocal identifier [, identifier]* ;

Usage
-----

When an inner function needs to modify a variable from an outer function:

.. code-block:: ml

   function create_counter(start) {
       count = start;

       function increment() {
           nonlocal count;  // Required to modify 'count'
           count = count + 1;
           return count;
       }

       return increment;
   }

Scope Rules
-----------

- Variables in inner functions are local by default
- Reading outer variables works without ``nonlocal``
- Modifying outer variables requires ``nonlocal`` declaration
- ``nonlocal`` searches enclosing function scopes (not global)
```

## Related Issues

- **Closures:** This resolves the fundamental closure variable modification issue
- **Scope Control:** Provides explicit scope control mechanism
- **Python Compatibility:** Maintains semantic alignment with Python

## Future Enhancements

Potential future improvements (not currently planned):

1. **Automatic nonlocal insertion** - Transpiler could detect and auto-insert (but reduces explicitness)
2. **Global statement** - For module-level variable modification
3. **Scope diagnostics** - Better error messages suggesting nonlocal when needed

## Conclusion

The `nonlocal` statement implementation successfully resolves closure variable modification issues by adopting Python's explicit scope control approach. This provides a simple, clear, and familiar mechanism for ML developers while avoiding the complexity of automatic scope inference.

**Status:** Production-ready, needs documentation in Language Reference.
