# Language Reference - Implementation Plan

## Research Complete ✅

### Grammar Analysis
- Read complete ML grammar (`ml.lark`)
- Identified all implemented features and syntax
- Documented operator precedence from grammar rules
- Noted security features (capability system)

### Integration Test Study
- **ml_core tests**: 25 files covering advanced language features
- **ml_builtin tests**: 17 files covering built-in functions
- Studied arrow functions, destructuring, ternary, exceptions

## Built-in Functions Discovered

### Type System
- **Conversion**: `int()`, `float()`, `str()`, `bool()`
- **Checking**: `typeof()`, `isinstance()`

### Collections
- **Basic**: `len()`, `range()`, `enumerate()`, `keys()`
- **Array**: `append()`, `reversed()`, `sum()`
- **Utilities**: `min()`, `max()`

### String & Character
- Character conversions: `ord()`, `chr()`
- Base conversions: `bin()`, `hex()`, `oct()`
- Representations: `repr()`, `ascii()`

### Advanced
- Iterators and predicates
- Object introspection: `dir()`, `vars()`, `hasattr()`

## Language Features

### Core Constructs
1. **Functions**: Named functions, arrow functions (`fn(x) => expr`)
2. **Control Flow**: if/elif/else, while, for..in, break, continue
3. **Exception Handling**: try/except/finally, throw
4. **Destructuring**: Array `[a, b] = arr`, Object `{x, y} = obj`

### Operators
1. **Arithmetic**: `+`, `-`, `*`, `/`, `//` (floor div), `%`
2. **Comparison**: `==`, `!=`, `<`, `>`, `<=`, `>=`
3. **Logical**: `&&`, `||`, `!`
4. **Ternary**: `condition ? true_val : false_val`

### Advanced Features
1. **Slicing**: `arr[start:end:step]`
2. **Scope**: `nonlocal` statement for closures
3. **Capability System**: Fine-grained security control
4. **Scientific Notation**: `1.5e6`, `6.626e-34`

## Language Reference Structure

### Section 1: Lexical Structure
- **Identifiers**: naming rules, reserved words
- **Keywords**: Complete list with descriptions
- **Literals**: numbers, strings, booleans, null
- **Operators**: All operators listed
- **Comments**: Single-line comments with `//`

### Section 2: Data Types
- **Primitives**: number, string, boolean, null
- **Collections**: array, object
- **Functions**: function type
- **Type System**: Dynamic typing, typeof behavior

### Section 3: Expressions
- **Primary**: literals, identifiers, parentheses
- **Operators**: precedence table, associativity
- **Function Calls**: call syntax, arguments
- **Member Access**: dot notation, bracket notation
- **Ternary**: conditional expressions
- **Slicing**: array and string slicing

### Section 4: Statements
- **Expression Statements**: expression + semicolon
- **Assignments**: simple, array element, object property
- **Destructuring**: array and object patterns
- **Variable Scope**: global, local, nonlocal

### Section 5: Control Flow
- **Conditionals**: if/elif/else
- **Loops**: while, for..in
- **Loop Control**: break, continue
- **Exception Handling**: try/except/finally, throw
- **Return**: return statement

### Section 6: Functions
- **Named Functions**: syntax, parameters, return
- **Arrow Functions**: syntax with fn keyword
- **Parameters**: positional, default values (if supported)
- **Closures**: capturing variables, nonlocal
- **Higher-Order**: functions as values

### Section 7: Built-in Functions
- **Type Conversion**: int, float, str, bool
- **Type Checking**: typeof, isinstance
- **Collections**: len, range, enumerate, keys
- **Array Operations**: append, reversed, sum
- **Math**: min, max
- **String & Char**: ord, chr, bin, hex, oct
- **Introspection**: dir, vars, hasattr

## Documentation Approach

### Format
- Plain English (Principle 6)
- Complete syntax specifications
- Practical examples for each feature
- Links to tutorial for beginners

### Examples
- Short, focused examples
- Show common patterns
- Demonstrate edge cases
- Include error cases where relevant

### Cross-References
- Link related sections
- Reference tutorial for learning
- Point to standard library for modules

## Writing Order

1. **Lexical Structure** (foundational)
2. **Data Types** (type system)
3. **Expressions** (operator precedence critical)
4. **Statements** (builds on expressions)
5. **Control Flow** (builds on statements)
6. **Functions** (advanced but essential)
7. **Built-in Functions** (reference material)

## Estimated Effort

- **Lexical Structure**: Small section (~150 lines)
- **Data Types**: Medium section (~200 lines)
- **Expressions**: Large section (~300 lines)
- **Statements**: Medium section (~200 lines)
- **Control Flow**: Medium section (~250 lines)
- **Functions**: Large section (~300 lines)
- **Built-in Functions**: Very large (~400 lines)

**Total Estimate**: ~1,800 lines of language reference documentation

## Current Status

- ✅ Research complete
- ✅ Plan finalized
- ⏳ Ready to begin writing
- 🎯 Start with Lexical Structure section
