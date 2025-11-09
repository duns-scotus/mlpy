# Grammar Extensions: Return Type Annotations

**Status:** Technical Specification
**Date:** November 4, 2025
**Related:** golang-oop-final-design.md

---

## Overview

This document specifies the exact grammar changes needed to add return type annotations to ML functions. Return types are **optional** and work with both regular functions and arrow functions.

---

## Current Grammar (Before)

```lark
// Function Definitions (BEFORE)
function_definition: "function" IDENTIFIER "(" parameter_list? ")" "{" statement* "}"

// Arrow Functions (BEFORE)
arrow_function: FN "(" parameter_list? ")" "=>" arrow_body
arrow_body: expression | arrow_block
arrow_block: "{" statement+ "}"

// Parameters (existing - already supports type hints)
parameter_list: parameter ("," parameter)*
parameter: IDENTIFIER (":" type_annotation)?
type_annotation: IDENTIFIER
```

---

## New Grammar (After)

```lark
// Function Definitions (AFTER - added return type support)
function_definition: "function" method_receiver? IDENTIFIER "(" parameter_list? ")" return_type? "{" statement* "}"
method_receiver: "(" IDENTIFIER ":" IDENTIFIER ")"
return_type: ":" type_annotation

// Arrow Functions (AFTER - added return type support)
arrow_function: FN "(" parameter_list? ")" return_type? "=>" arrow_body
arrow_body: expression | arrow_block
arrow_block: "{" statement+ "}"

// Parameters (unchanged - already supports type hints)
parameter_list: parameter ("," parameter)*
parameter: IDENTIFIER (":" type_annotation)?
type_annotation: IDENTIFIER

// Struct Declaration (NEW - for OOP feature)
struct_declaration: "struct" IDENTIFIER "{" struct_field* "}"
struct_field: IDENTIFIER (":" type_annotation)? ("," | ";")

// Struct Literal (NEW - for OOP feature)
struct_literal: IDENTIFIER "{" (struct_property ("," struct_property)*)? "}"
struct_property: IDENTIFIER ":" expression
```

---

## Grammar Changes Breakdown

### Change 1: Add `return_type` Rule

**New rule:**
```lark
return_type: ":" type_annotation
```

**Purpose:** Defines the syntax for return type annotations (`: typename`)

**Examples:**
- `: number`
- `: string`
- `: Point`
- `: array`

---

### Change 2: Extend `function_definition`

**Before:**
```lark
function_definition: "function" IDENTIFIER "(" parameter_list? ")" "{" statement* "}"
```

**After:**
```lark
function_definition: "function" method_receiver? IDENTIFIER "(" parameter_list? ")" return_type? "{" statement* "}"
method_receiver: "(" IDENTIFIER ":" IDENTIFIER ")"
```

**Changes:**
1. Added `method_receiver?` - Optional receiver for methods (OOP feature)
2. Added `return_type?` - Optional return type annotation

**What this enables:**
```ml
// Regular function (before - still works)
function add(a, b) {
    return a + b;
}

// Regular function with return type (NEW)
function add(a, b): number {
    return a + b;
}

// Regular function with parameter types (already worked)
function add(a: number, b: number) {
    return a + b;
}

// Regular function fully typed (NEW)
function add(a: number, b: number): number {
    return a + b;
}

// Method with receiver (NEW - OOP feature)
function (p: Point) distance(): number {
    return math.sqrt(p.x * p.x + p.y * p.y);
}
```

---

### Change 3: Extend `arrow_function`

**Before:**
```lark
arrow_function: FN "(" parameter_list? ")" "=>" arrow_body
```

**After:**
```lark
arrow_function: FN "(" parameter_list? ")" return_type? "=>" arrow_body
```

**Changes:**
1. Added `return_type?` - Optional return type annotation

**What this enables:**
```ml
// Arrow function (before - still works)
fn(x) => x * 2

// Arrow function with parameter type (already worked)
fn(x: number) => x * 2

// Arrow function with return type (NEW)
fn(x): number => x * 2

// Arrow function fully typed (NEW)
fn(x: number): number => x * 2

// Arrow function with block body and return type (NEW)
fn(x: number, y: number): number => {
    result = x + y;
    return result;
}
```

---

### Change 4: Add `struct_declaration` (OOP Feature)

**New rule:**
```lark
struct_declaration: "struct" IDENTIFIER "{" struct_field* "}"
struct_field: IDENTIFIER (":" type_annotation)? ("," | ";")
```

**Purpose:** Define struct types with optional field type hints

**Examples:**
```ml
// Fully typed struct
struct Point {
    x: number,
    y: number
}

// Partially typed struct
struct Person {
    name: string,
    age: number,
    metadata        // No type - dynamic
}

// Untyped struct
struct Config {
    host,
    port,
    options
}
```

---

### Change 5: Add `struct_literal` (OOP Feature)

**New rule:**
```lark
struct_literal: IDENTIFIER "{" (struct_property ("," struct_property)*)? "}"
struct_property: IDENTIFIER ":" expression
```

**Purpose:** Create struct instances with type-prefixed syntax

**Examples:**
```ml
// Create struct instance
p = Point{x: 3, y: 4};

// Create with expressions
p2 = Point{x: calculate_x(), y: calculate_y()};

// Nested structs
person = Person{
    name: "Alice",
    age: 30,
    address: Address{street: "Main St", city: "NYC"}
};
```

---

## Complete Updated Grammar Section

```lark
// Function Definitions
function_definition: "function" method_receiver? IDENTIFIER "(" parameter_list? ")" return_type? "{" statement* "}"
method_receiver: "(" IDENTIFIER ":" IDENTIFIER ")"
return_type: ":" type_annotation

parameter_list: parameter ("," parameter)*
parameter: IDENTIFIER (":" type_annotation)?
type_annotation: IDENTIFIER

// Arrow Functions
arrow_function: FN "(" parameter_list? ")" return_type? "=>" arrow_body
arrow_body: expression | arrow_block
arrow_block: "{" statement+ "}"

// Struct Declarations
struct_declaration: "struct" IDENTIFIER "{" struct_field* "}"
struct_field: IDENTIFIER (":" type_annotation)? ("," | ";")

// Struct Literals (in expression context)
struct_literal: IDENTIFIER "{" (struct_property ("," struct_property)*)? "}"
struct_property: IDENTIFIER ":" expression

// Statements (add struct_declaration)
?statement: expression_statement
          | assignment_statement
          | destructuring_statement
          | function_definition
          | struct_declaration       // NEW
          | if_statement
          | while_statement
          | for_statement
          | return_statement
          | throw_statement
          | try_statement
          | break_statement
          | continue_statement
          | nonlocal_statement

// Primary expressions (add struct_literal)
?primary: literal
        | IDENTIFIER
        | function_call
        | array_access
        | member_access
        | arrow_function
        | struct_literal            // NEW
        | "(" expression ")"
```

---

## Parsing Precedence Considerations

### Potential Ambiguity: Object Literals vs Struct Literals

**Object literal (existing):**
```ml
obj = {x: 3, y: 4};  // No type prefix
```

**Struct literal (new):**
```ml
point = Point{x: 3, y: 4};  // Type prefix (IDENTIFIER before {)
```

**Resolution:**
- Object literals start with `{` directly
- Struct literals start with `IDENTIFIER` then `{`
- No ambiguity in parsing

**Grammar handling:**
```lark
?primary: ...
        | struct_literal     // IDENTIFIER "{" ... "}"
        | "(" expression ")"

?literal: ...
        | object_literal     // "{" ... "}"

// Different starting tokens - no conflict
struct_literal: IDENTIFIER "{" ... "}"
object_literal: "{" ... "}"
```

---

## AST Node Extensions

### New AST Nodes for Return Types

```python
@dataclass
class FunctionDefinition:
    name: str
    parameters: List[Parameter]
    body: List[Statement]
    return_type: Optional[str]      # NEW FIELD
    receiver: Optional[Receiver]    # NEW FIELD (for methods)
    location: Location

@dataclass
class Receiver:
    name: str
    type: str
    location: Location

@dataclass
class ArrowFunction:
    parameters: List[Parameter]
    body: Union[Expression, List[Statement]]
    return_type: Optional[str]      # NEW FIELD
    location: Location

@dataclass
class Parameter:
    name: str
    type_annotation: Optional[str]  # Existing
    location: Location

@dataclass
class StructDeclaration:
    name: str
    fields: List[StructField]
    location: Location

@dataclass
class StructField:
    name: str
    type_annotation: Optional[str]
    location: Location

@dataclass
class StructLiteral:
    type_name: str
    properties: Dict[str, Expression]
    location: Location
```

---

## Transformer Updates

### Updated Transformer Methods

```python
class MLTransformer(Transformer):

    def return_type(self, items):
        """Transform return type annotation."""
        return items[0].value  # Just the type name string

    def function_definition(self, items):
        """Transform function definition with optional return type."""
        idx = 0

        # Check for method receiver
        receiver = None
        if isinstance(items[idx], Receiver):
            receiver = items[idx]
            idx += 1

        # Function name
        name = items[idx].value
        idx += 1

        # Parameters (optional)
        parameters = []
        if idx < len(items) and isinstance(items[idx], list):
            parameters = items[idx]
            idx += 1

        # Return type (optional - NEW)
        return_type = None
        if idx < len(items) and isinstance(items[idx], str):
            return_type = items[idx]
            idx += 1

        # Body statements
        body = items[idx:] if idx < len(items) else []

        if receiver:
            return MethodDefinition(
                receiver=receiver,
                name=name,
                parameters=parameters,
                return_type=return_type,  # NEW
                body=body,
                location=self.get_location()
            )
        else:
            return FunctionDefinition(
                name=name,
                parameters=parameters,
                return_type=return_type,  # NEW
                body=body,
                location=self.get_location()
            )

    def arrow_function(self, items):
        """Transform arrow function with optional return type."""
        idx = 0

        # Parameters (optional)
        parameters = []
        if idx < len(items) and isinstance(items[idx], list):
            parameters = items[idx]
            idx += 1

        # Return type (optional - NEW)
        return_type = None
        if idx < len(items) and isinstance(items[idx], str):
            return_type = items[idx]
            idx += 1

        # Body (expression or block)
        body = items[idx]

        return ArrowFunction(
            parameters=parameters,
            return_type=return_type,  # NEW
            body=body,
            location=self.get_location()
        )

    def struct_declaration(self, items):
        """Transform struct declaration."""
        name = items[0].value
        fields = items[1:]
        return StructDeclaration(name, fields, self.get_location())

    def struct_field(self, items):
        """Transform struct field."""
        name = items[0].value
        type_annotation = items[1].value if len(items) > 1 else None
        return StructField(name, type_annotation, self.get_location())

    def struct_literal(self, items):
        """Transform struct literal."""
        type_name = items[0].value
        properties = {}
        for prop in items[1:]:
            properties[prop.name] = prop.value
        return StructLiteral(type_name, properties, self.get_location())
```

---

## Example Parse Trees

### Example 1: Simple Function with Return Type

**ML Code:**
```ml
function add(a: number, b: number): number {
    return a + b;
}
```

**Parse Tree:**
```
function_definition
├─ IDENTIFIER "add"
├─ parameter_list
│  ├─ parameter
│  │  ├─ IDENTIFIER "a"
│  │  └─ type_annotation "number"
│  └─ parameter
│     ├─ IDENTIFIER "b"
│     └─ type_annotation "number"
├─ return_type
│  └─ type_annotation "number"
└─ statement*
   └─ return_statement
      └─ add_op
         ├─ IDENTIFIER "a"
         └─ IDENTIFIER "b"
```

**AST Node:**
```python
FunctionDefinition(
    name="add",
    parameters=[
        Parameter(name="a", type_annotation="number"),
        Parameter(name="b", type_annotation="number")
    ],
    return_type="number",  # NEW
    receiver=None,
    body=[
        ReturnStatement(
            value=BinaryOp(op="+", left=Identifier("a"), right=Identifier("b"))
        )
    ]
)
```

---

### Example 2: Method with Return Type

**ML Code:**
```ml
function (p: Point) distance(): number {
    import math;
    return math.sqrt(p.x * p.x + p.y * p.y);
}
```

**Parse Tree:**
```
function_definition
├─ method_receiver
│  ├─ IDENTIFIER "p"
│  └─ IDENTIFIER "Point"
├─ IDENTIFIER "distance"
├─ parameter_list (empty)
├─ return_type
│  └─ type_annotation "number"
└─ statement*
   ├─ import_statement
   └─ return_statement
      └─ function_call
         └─ ...
```

**AST Node:**
```python
MethodDefinition(
    receiver=Receiver(name="p", type="Point"),
    name="distance",
    parameters=[],
    return_type="number",  # NEW
    body=[
        ImportStatement(...),
        ReturnStatement(...)
    ]
)
```

---

### Example 3: Arrow Function with Return Type

**ML Code:**
```ml
double = fn(x: number): number => x * 2;
```

**Parse Tree:**
```
assignment_statement
├─ IDENTIFIER "double"
└─ arrow_function
   ├─ parameter_list
   │  └─ parameter
   │     ├─ IDENTIFIER "x"
   │     └─ type_annotation "number"
   ├─ return_type
   │  └─ type_annotation "number"
   └─ arrow_body
      └─ mul_op
         ├─ IDENTIFIER "x"
         └─ NUMBER "2"
```

**AST Node:**
```python
AssignmentStatement(
    target=Identifier("double"),
    value=ArrowFunction(
        parameters=[Parameter(name="x", type_annotation="number")],
        return_type="number",  # NEW
        body=BinaryOp(op="*", left=Identifier("x"), right=Literal(2))
    )
)
```

---

## Backward Compatibility

### All Existing Syntax Still Works

**Before (no return types):**
```ml
// All of these continue to work exactly as before
function add(a, b) { return a + b; }
function multiply(a: number, b: number) { return a * b; }
fn(x) => x * 2
fn(x: number) => x * 2
```

**After (return types optional):**
```ml
// Old syntax works (backward compatible)
function add(a, b) { return a + b; }
function multiply(a: number, b: number) { return a * b; }
fn(x) => x * 2

// New syntax available (opt-in)
function add(a, b): number { return a + b; }
function multiply(a: number, b: number): number { return a * b; }
fn(x): number => x * 2
fn(x: number): number => x * 2
```

**No breaking changes** - all existing ML code continues to parse correctly.

---

## Testing Requirements

### Parser Tests Needed

1. **Regular functions with return types**
   - Function with return type only: `function f(): number { ... }`
   - Function with params and return type: `function f(x: number): string { ... }`
   - Function with untyped params and return type: `function f(x, y): array { ... }`

2. **Methods with return types**
   - Method with return type: `function (s: Shape) area(): number { ... }`
   - Method without return type: `function (s: Shape) draw() { ... }`

3. **Arrow functions with return types**
   - Arrow with return type: `fn(x): number => x * 2`
   - Arrow with params and return type: `fn(x: number): number => x * 2`
   - Arrow block with return type: `fn(x): number => { return x * 2; }`

4. **Struct declarations**
   - Fully typed struct
   - Partially typed struct
   - Untyped struct

5. **Struct literals**
   - Simple struct literal
   - Nested struct literals
   - Struct literals in expressions

6. **Backward compatibility**
   - All existing test files must still parse
   - No regressions in existing functionality

### Test Count Estimate
- Return type parsing: 15 tests
- Method syntax: 10 tests
- Struct syntax: 15 tests
- Backward compatibility: 80+ existing tests must pass
- **Total: 120+ parser tests**

---

## Implementation Checklist

### Phase 1: Grammar Changes
- [ ] Add `return_type` rule to grammar
- [ ] Update `function_definition` rule
- [ ] Update `arrow_function` rule
- [ ] Add `struct_declaration` rule
- [ ] Add `struct_literal` rule
- [ ] Add `method_receiver` rule
- [ ] Update `statement` rule to include structs
- [ ] Update `primary` rule to include struct literals
- [ ] Add `struct` keyword to lexer

### Phase 2: AST Node Updates
- [ ] Add `return_type` field to `FunctionDefinition`
- [ ] Add `receiver` field to `FunctionDefinition`
- [ ] Add `return_type` field to `ArrowFunction`
- [ ] Create `Receiver` node class
- [ ] Create `StructDeclaration` node class
- [ ] Create `StructField` node class
- [ ] Create `StructLiteral` node class
- [ ] Create `MethodDefinition` node class (or extend FunctionDefinition)

### Phase 3: Transformer Updates
- [ ] Update `function_definition` transformer method
- [ ] Update `arrow_function` transformer method
- [ ] Add `return_type` transformer method
- [ ] Add `method_receiver` transformer method
- [ ] Add `struct_declaration` transformer method
- [ ] Add `struct_field` transformer method
- [ ] Add `struct_literal` transformer method

### Phase 4: Testing
- [ ] Write return type parser tests (15 tests)
- [ ] Write method syntax parser tests (10 tests)
- [ ] Write struct syntax parser tests (15 tests)
- [ ] Run all existing tests (backward compatibility)
- [ ] Fix any regressions

### Estimated Time: 3-4 days

---

## Summary

This specification provides complete details for adding:
1. ✅ Return type annotations to regular functions
2. ✅ Return type annotations to arrow functions
3. ✅ Method receiver syntax (for OOP)
4. ✅ Struct declarations
5. ✅ Struct literals

All changes are **backward compatible** - existing ML code continues to work unchanged.

**Next Step:** Implement these grammar changes in `src/mlpy/ml/grammar/ml.lark`
