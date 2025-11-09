# Golang-Style OOP for ML: Final Design Document

**Status:** Approved for Implementation
**Author:** Claude Code
**Date:** November 4, 2025
**Sprint:** Language Enhancement - OOP Features

---

## Executive Summary

This document finalizes the design for **lightweight OOP features in ML** inspired by Go's pragmatic approach. After analyzing the tension between Go's static typing and ML's dynamic nature, we've adopted a **hybrid structural typing** approach with **optional runtime type checking**.

### Design Principles

✅ **Optional Type Hints** - Types are optional everywhere (parameters, returns, fields)
✅ **Runtime Type Checking** - Types checked at runtime only when provided
✅ **Structural Typing** - Methods work with any object with matching fields
✅ **Backward Compatible** - Existing plain objects work with new struct methods
✅ **Gradual Typing** - Add types where helpful, omit where unnecessary
✅ **No Classes/Inheritance** - Keep complexity low (Go-style simplicity)

---

## Core Language Extensions

### 1. Struct Definitions (with Optional Types)

**Syntax:**
```ml
struct TypeName {
    field1: type,      // Type hint - checked at runtime
    field2,            // No type - accepts anything (dynamic)
    field3: type
}
```

**Examples:**
```ml
// Fully typed struct (runtime checks on creation)
struct Point {
    x: number,
    y: number
}

// Partially typed struct (mixed checking)
struct Person {
    name: string,      // Checked: must be string
    age: number,       // Checked: must be number
    metadata           // Unchecked: accepts any value
}

// Untyped struct (no runtime checks, pure shape definition)
struct Config {
    host,
    port,
    options
}
```

**Runtime Behavior:**
```ml
// ✅ OK: matches types
p1 = Point{x: 3, y: 4};

// ❌ TypeError: x must be number
p2 = Point{x: "hello", y: 4};

// ✅ OK: metadata can be anything
person = Person{name: "Alice", age: 30, metadata: {foo: "bar"}};

// ✅ OK: no type checking
config = Config{host: "localhost", port: 8080, options: {}};
```

---

### 2. Methods with Explicit Receivers

**Syntax:**
```ml
function (receiver: Type) method_name(param1: type, param2, ...): return_type {
    // method body
}
```

**All components are optional:**
- Receiver type: optional (but recommended for methods)
- Parameter types: optional
- Return type: optional (NEW - not in current grammar)

**Examples:**
```ml
struct Vector {
    x: number,
    y: number
}

// Fully typed method
function (v: Vector) magnitude(): number {
    import math;
    return math.sqrt(v.x * v.x + v.y * v.y);
}

// Partially typed method (no return type)
function (v: Vector) scale(factor: number) {
    v.x = v.x * factor;
    v.y = v.y * factor;
}

// Untyped method (duck typing)
function (v: Vector) add(other) {
    return Vector{
        x: v.x + other.x,
        y: v.y + other.y
    };
}
```

**Runtime Type Checking:**
- **Receiver type present:** Check receiver has required fields (structural)
- **Parameter types present:** Check parameter types on call
- **Return type present:** Check return value type
- **Type absent:** No checking (fully dynamic)

---

### 3. Function Return Type Annotations (NEW)

**Extends current grammar to support return types.**

**Syntax:**
```ml
// Regular function with return type
function name(params): return_type {
    // ...
}

// Arrow function with return type
fn(params): return_type => expression
```

**Examples:**
```ml
// Regular function - fully typed
function add(a: number, b: number): number {
    return a + b;
}

// Regular function - partially typed
function process(data): string {
    return str(data);
}

// Regular function - untyped (current behavior)
function calculate(x, y, z) {
    return x + y * z;
}

// Arrow function - typed
fn(x: number): number => x * 2

// Arrow function - untyped (current behavior)
fn(x) => x * 2
```

**Runtime Behavior:**
```ml
function divide(a: number, b: number): number {
    if (b == 0) {
        throw {message: "Division by zero"};
    }
    return a / b;  // Checked: must return number
}

result = divide(10, 2);      // ✅ OK: returns 5
result2 = divide("10", "2"); // ❌ TypeError: a must be number
```

---

### 4. Structural Type Matching

**Key Innovation:** Methods work with **any object** that has the required fields (duck typing).

**Example:**
```ml
struct Point {
    x: number,
    y: number
}

function (p: Point) distance(): number {
    import math;
    return math.sqrt(p.x * p.x + p.y * p.y);
}

// All of these work (structural matching):

// 1. Struct instance
p1 = Point{x: 3, y: 4};
p1.distance();  // ✅ Works

// 2. Plain object (backward compatibility!)
p2 = {x: 3, y: 4};
p2.distance();  // ✅ Works (has x, y numbers)

// 3. Different struct with compatible fields
struct Vector3D {
    x: number,
    y: number,
    z: number
}
v = Vector3D{x: 3, y: 4, z: 5};
v.distance();  // ✅ Works (has x, y, ignores z)

// 4. Object with wrong types
p3 = {x: "hello", y: "world"};
p3.distance();  // ❌ TypeError: x must be number (runtime check)
```

**Structural Checking Algorithm:**
```python
def check_structural_type(obj, struct_def):
    """Check if obj satisfies struct_def structurally."""
    for field_name, field_type in struct_def.typed_fields:
        # Check field exists
        if not hasattr(obj, field_name):
            raise TypeError(f"Missing required field: {field_name}")

        # Check field type (only if type hint present)
        if field_type:
            value = getattr(obj, field_name)
            if not matches_type(value, field_type):
                raise TypeError(f"Field {field_name} must be {field_type}")
```

---

### 5. Implicit Interfaces (Optional - Phase 2)

**For documentation and future static analysis.**

**Syntax:**
```ml
interface Drawable {
    draw(): string;
    area(): number;
}
```

**Semantics:**
- Interfaces are purely structural (Go-style)
- No explicit `implements` keyword needed
- Any struct with matching methods satisfies interface
- Used for documentation and IDE support
- Can enable optional static checking in future

**Example:**
```ml
interface Shape {
    area(): number;
    perimeter(): number;
}

struct Circle {
    radius: number
}

function (c: Circle) area(): number {
    return 3.14159 * c.radius * c.radius;
}

function (c: Circle) perimeter(): number {
    return 2 * 3.14159 * c.radius;
}

// Circle implicitly satisfies Shape interface
// (has both area() and perimeter() methods)

function print_shape_info(s: Shape) {
    print("Area: " + str(s.area()));
    print("Perimeter: " + str(s.perimeter()));
}

circle = Circle{radius: 5};
print_shape_info(circle);  // ✅ Works (structural match)
```

---

## Grammar Extensions

### Extended Grammar Rules

```lark
// Add to statement rules
?statement: ...
          | struct_declaration
          | interface_declaration  // Phase 2

// Struct definition
struct_declaration: "struct" IDENTIFIER "{" struct_field* "}"
struct_field: IDENTIFIER (":" type_annotation)? ("," | ";")

// Function definition with optional return type (EXTENDED)
function_definition: "function" method_receiver? IDENTIFIER "(" parameter_list? ")" (":" type_annotation)? "{" statement* "}"
method_receiver: "(" IDENTIFIER ":" IDENTIFIER ")"

// Parameter with optional type (existing)
parameter_list: parameter ("," parameter)*
parameter: IDENTIFIER (":" type_annotation)?

// Arrow function with optional return type (EXTENDED)
arrow_function: FN "(" parameter_list? ")" (":" type_annotation)? "=>" arrow_body
arrow_body: expression | arrow_block

// Struct literal (type-prefixed object literal)
struct_literal: IDENTIFIER "{" (struct_property ("," struct_property)*)? "}"
struct_property: IDENTIFIER ":" expression

// Type annotation (existing, but now used more widely)
type_annotation: IDENTIFIER

// Interface definition (Phase 2 - optional)
interface_declaration: "interface" IDENTIFIER "{" interface_method* "}"
interface_method: IDENTIFIER "(" parameter_types? ")" (":" type_annotation)? ";"
parameter_types: type_annotation ("," type_annotation)*

// Keywords (add to token definitions)
// "struct", "interface" (must come before IDENTIFIER in lexer)
```

### What Changed vs Current Grammar

**Current grammar:**
```lark
function_definition: "function" IDENTIFIER "(" parameter_list? ")" "{" statement* "}"
arrow_function: FN "(" parameter_list? ")" "=>" arrow_body
```

**New grammar:**
```lark
function_definition: "function" method_receiver? IDENTIFIER "(" parameter_list? ")" (":" type_annotation)? "{" statement* "}"
method_receiver: "(" IDENTIFIER ":" IDENTIFIER ")"
arrow_function: FN "(" parameter_list? ")" (":" type_annotation)? "=>" arrow_body
```

**Key Additions:**
1. `method_receiver?` - Optional receiver parameter for methods
2. `(":" type_annotation)?` - Optional return type (after parameters)
3. `struct_declaration` - New statement type
4. `struct_literal` - Type-prefixed object creation

---

## Runtime Type Checking System

### Type System Design

**Built-in Types:**
```ml
// Primitive types
number   // int or float
string   // text
boolean  // true/false
array    // any array
object   // any object/dictionary

// Special types
any      // no checking (default when no type specified)
void     // function returns nothing (no return statement)
```

**Type Checking Rules:**

1. **Field Types (struct creation)**
   ```ml
   struct Point { x: number, y: number }
   p = Point{x: 3, y: 4};  // Check: x is number? y is number?
   ```

2. **Parameter Types (function call)**
   ```ml
   function add(a: number, b: number) { ... }
   add(3, 4);    // Check: a is number? b is number?
   ```

3. **Return Types (function return)**
   ```ml
   function get_name(): string { return "Alice"; }
   // Check: return value is string?
   ```

4. **Receiver Types (method call - structural)**
   ```ml
   function (p: Point) distance() { ... }
   obj.distance();  // Check: obj has x, y fields of type number?
   ```

### Type Checking Implementation

**Python Code Generation:**

```python
# Type checking helper
def _check_type(value, expected_type, context="value"):
    """Check if value matches expected type at runtime."""
    type_map = {
        'number': (int, float),
        'string': str,
        'boolean': bool,
        'array': list,
        'object': dict,
        'any': object  # Always matches
    }

    if expected_type not in type_map:
        # Custom struct type - check structurally
        return _check_structural_type(value, expected_type)

    expected_py_types = type_map[expected_type]
    if not isinstance(value, expected_py_types):
        raise TypeError(
            f"{context} must be {expected_type}, got {type(value).__name__}"
        )
    return value

# Struct with type checking
@dataclass
class Point:
    x: Union[int, float]
    y: Union[int, float]

    def __post_init__(self):
        # Only check fields with type hints in ML source
        _check_type(self.x, 'number', 'Point.x')
        _check_type(self.y, 'number', 'Point.y')

# Method with type checking
def Point_distance(self):
    # Check receiver type (structural)
    _check_structural_type(self, 'Point', required_fields=['x', 'y'])

    # Method body
    result = math.sqrt(self.x * self.x + self.y * self.y)

    # Check return type
    return _check_type(result, 'number', 'Point.distance return value')

Point.distance = Point_distance

# Function with type checking
def add(a, b):
    # Check parameter types
    _check_type(a, 'number', 'parameter a')
    _check_type(b, 'number', 'parameter b')

    # Function body
    result = a + b

    # Check return type
    return _check_type(result, 'number', 'add return value')
```

### Performance Considerations

**Optimization Strategy:**
1. **No checking when no types** - Zero overhead for untyped code
2. **Cached type checks** - Cache structural type compatibility
3. **Inline checks** - No function call overhead for primitive types
4. **Skip in production** - Optional flag to disable runtime checks

**Performance Impact Estimate:**
- Untyped code: 0% overhead
- Typed primitive parameters: <5% overhead (simple isinstance checks)
- Typed struct parameters: <10% overhead (structural checks, cached)
- Overall: <2% for typical mixed typed/untyped code

---

## Backward Compatibility

### Existing Code Continues to Work

**All existing ML code is untyped and will continue to work:**

```ml
// Current ML code (no changes needed)
function create_person(name, age) {
    return {
        name: name,
        age: age,
        greet: function() { return "Hi, I'm " + name; }
    };
}

person = create_person("Alice", 30);
person.greet();
```

**Can gradually migrate to structs:**

```ml
// New ML code with structs
struct Person {
    name: string,
    age: number
}

function (p: Person) greet(): string {
    return "Hi, I'm " + p.name;
}

// Still works with plain objects!
old_person = {name: "Bob", age: 25};
old_person.greet();  // ✅ Works (structural matching)

new_person = Person{name: "Alice", age: 30};
new_person.greet();  // ✅ Works
```

### Migration Path

1. **Phase 1:** Add struct definitions (documentation)
2. **Phase 2:** Add type hints to critical functions
3. **Phase 3:** Add return types to public APIs
4. **Phase 4:** Gradually refactor objects to structs

**No forced migration** - plain objects and structs coexist.

---

## Complete Examples

### Example 1: Banking System (Fully Typed)

```ml
struct Account {
    account_number: string,
    balance: number,
    owner: string
}

function new_account(owner: string, initial: number): Account {
    if (initial < 0) {
        throw {message: "Initial balance must be non-negative"};
    }

    import random;
    return Account{
        account_number: "ACC" + str(random.randint(10000, 99999)),
        balance: initial,
        owner: owner
    };
}

function (acc: Account) deposit(amount: number): number {
    if (amount <= 0) {
        throw {message: "Deposit amount must be positive"};
    }
    acc.balance = acc.balance + amount;
    return acc.balance;
}

function (acc: Account) withdraw(amount: number): number {
    if (amount <= 0) {
        throw {message: "Withdrawal amount must be positive"};
    }
    if (amount > acc.balance) {
        throw {message: "Insufficient funds"};
    }
    acc.balance = acc.balance - amount;
    return acc.balance;
}

function (acc: Account) get_balance(): number {
    return acc.balance;
}

// Usage
account = new_account("Alice", 1000);
account.deposit(500);
account.withdraw(200);
print("Balance: " + str(account.get_balance()));  // 1300
```

### Example 2: Data Processing (Mixed Typing)

```ml
struct DataPoint {
    timestamp: number,
    value,              // No type - accepts any value
    metadata
}

function (dp: DataPoint) format(): string {
    import datetime;
    time_str = datetime.from_timestamp(dp.timestamp);
    return time_str + ": " + str(dp.value);
}

function process_data(points): array {  // Untyped parameter
    results = [];
    for (point in points) {
        results = results + [point.format()];
    }
    return results;
}

// Works with both struct instances and plain objects
data1 = DataPoint{timestamp: 1699200000, value: 42, metadata: {}};
data2 = {timestamp: 1699200001, value: 43, metadata: {}};  // Plain object

all_data = [data1, data2];
formatted = process_data(all_data);
```

### Example 3: Shape System (Structural Interface)

```ml
struct Circle {
    radius: number
}

struct Rectangle {
    width: number,
    height: number
}

function (c: Circle) area(): number {
    return 3.14159 * c.radius * c.radius;
}

function (r: Rectangle) area(): number {
    return r.width * r.height;
}

// Generic function using structural typing
function print_area(shape) {  // No type - accepts anything with area()
    print("Area: " + str(shape.area()));
}

circle = Circle{radius: 5};
rect = Rectangle{width: 10, height: 20};
custom = {area: function() { return 100; }};  // Plain object with method

print_area(circle);  // ✅ Works
print_area(rect);    // ✅ Works
print_area(custom);  // ✅ Works (duck typing)
```

---

## Implementation Roadmap

### Phase 1: Grammar & Parser (3-4 days)

**Tasks:**
1. Add `struct` and `interface` keywords to lexer
2. Extend grammar rules for struct declarations
3. Add return type syntax to function definitions
4. Add return type syntax to arrow functions
5. Create new AST nodes (StructDeclaration, MethodDefinition, etc.)
6. Update transformer to build new AST nodes
7. Write 30+ parser unit tests

**Deliverables:**
- Updated `ml.lark` grammar file
- New AST node classes
- Comprehensive parser tests

### Phase 2: Type Registry & Checking (4-5 days)

**Tasks:**
1. Implement TypeRegistry class (struct + method storage)
2. Implement runtime type checking functions
3. Add structural type matching algorithm
4. Create type checking helper functions
5. Write 25+ type checking unit tests

**Deliverables:**
- `type_registry.py` module
- `runtime_type_checker.py` module
- Type checking unit tests

### Phase 3: Code Generation (5-6 days)

**Tasks:**
1. Generate Python dataclasses from structs
2. Generate instance methods with type checks
3. Handle struct literals (type-prefixed objects)
4. Add type checking to function parameters
5. Add type checking to return statements
6. Generate structural type checks for receivers
7. Write 40+ code generation unit tests

**Deliverables:**
- Updated `python_generator.py`
- Complete transpilation pipeline
- Code generation tests

### Phase 4: Integration & Testing (3-4 days)

**Tasks:**
1. Integration tests (30+ complex programs)
2. Backward compatibility tests (existing tests still pass)
3. Performance benchmarking
4. Documentation updates
5. Example programs

**Deliverables:**
- Comprehensive integration tests
- Performance benchmarks
- Updated language documentation

### Total Timeline: 15-19 days

---

## Success Metrics

**Must Achieve:**
- ✅ 100% backward compatibility (all existing tests pass)
- ✅ 95%+ test coverage for new features
- ✅ <5% runtime overhead for typed code
- ✅ <2% overhead for mixed typed/untyped code
- ✅ Zero security vulnerabilities introduced

**Quality Goals:**
- ✅ Clear error messages for type errors
- ✅ IDE autocomplete works with struct definitions
- ✅ Documentation is comprehensive
- ✅ Example programs demonstrate all features

---

## Decision Summary

| Aspect | Decision |
|--------|----------|
| **Type Hints** | Optional everywhere (parameters, returns, fields) |
| **Type Checking** | Runtime only, when types provided |
| **Type System** | Structural (duck typing compatible) |
| **Backward Compatibility** | 100% - plain objects work with struct methods |
| **Return Types** | Add to grammar (not currently supported) |
| **Inheritance** | None - composition via struct embedding only |
| **Interfaces** | Implicit/structural (Go-style), Phase 2 |
| **Migration** | Gradual - no forced changes to existing code |

---

## Next Steps

1. ✅ Review and approve this design document
2. Begin implementation with Phase 1 (grammar extensions)
3. Iterative development with continuous testing
4. Regular progress updates and design refinements

**Status:** Ready for implementation approval
