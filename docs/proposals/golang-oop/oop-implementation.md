# ML Language OOP Implementation Guide

**Status:** Under Revision - Type Checking Model Changed to Type Hints
**Author:** Claude Code
**Date:** November 4-5, 2025 (Updated: November 9, 2025 - Type Hints Model)
**Estimated Timeline:** 16-21 days

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Design Rationale](#design-rationale)
3. [Language Features](#language-features)
4. [Grammar Specification](#grammar-specification)
5. [Type System Design](#type-system-design)
6. [Pure Structural Typing](#pure-structural-typing) **NEW - CRITICAL**
7. [Standard Library Built-ins](#standard-library-built-ins) **NEW**
8. [Method Dispatch Algorithm](#method-dispatch-algorithm) **NEW**
9. [Built-in Integration](#built-in-integration) **NEW**
10. [Serialization and Deserialization](#serialization-and-deserialization) **NEW**
11. [Error Messages](#error-messages) **NEW**
12. [Security Integration](#security-integration) **NEW**
13. [Implementation Architecture](#implementation-architecture)
14. [Code Examples](#code-examples)
15. [Implementation Roadmap](#implementation-roadmap)
16. [Testing Strategy](#testing-strategy)
17. [Success Metrics](#success-metrics)

---

## Executive Summary

This guide provides the complete specification for adding **lightweight OOP features** to ML, inspired by Go's pragmatic approach. The design balances structure with ML's dynamic nature through **optional type hints for documentation and IDE support** (no runtime type enforcement).

### CRITICAL UPDATE (November 9, 2025)

**Type Hints Model Adopted:** After design review, the proposal now implements **type hints as documentation only** (no runtime type enforcement):
- **Types are hints** - Annotations for documentation, IDE support, and optional static analysis (like Python)
- **No runtime type checking** - Type annotations do not throw errors at runtime
- **Structural equality only** - Value-based `==`, no identity operators
- **Sealed structs** - No dynamic field addition (structured data only)
- **Strict method dispatch** - Only struct instances can call methods (structural identity checking only)
- **Minimal built-ins** - Essential functions only: `typeof()`, `copy()`, `deepcopy()`, `fields()`

**Rationale:** Consistent with ML's dynamic nature (like Python). Types serve as documentation and IDE hints. Runtime checks only for structural properties (field existence, struct identity), not field types. See design sections for complete details.

**Key Change from Previous Version:**
- **REMOVED:** Runtime type validation (was checking field types, parameter types, return types)
- **KEPT:** Struct identity checking (for method dispatch)
- **KEPT:** Field sealing (no dynamic field addition)
- **KEPT:** Required field validation (field names must be present)
- **NEW PHILOSOPHY:** Types are documentation/IDE hints (Python 3.5+ model), not runtime enforcement

### Core Design Principles

✅ **Pure Structural Typing** - Value-based equality, no nominal identity checks
✅ **Sealed Structs** - Fields defined at declaration, no dynamic field addition
✅ **Strict Method Dispatch** - Only struct instances can call methods (struct identity checking)
✅ **Optional Type Hints** - Types optional everywhere (parameters, returns, fields)
✅ **Type Hints Only** - Types are documentation/IDE hints, NOT enforced at runtime (Python model)
✅ **Gradual Documentation** - Add type hints incrementally for better IDE support
✅ **No Classes/Inheritance** - Keep complexity low (Go-style simplicity)

### Key Features

- **Structs** - Named data types with optional field type hints (documentation only) and default values
- **Methods** - Functions with explicit receiver parameters (struct instances only)
- **Return Type Annotations** - Optional return types for documentation and IDE support
- **Type Hints for Documentation** - All type annotations are hints only, never enforced at runtime
- **Structural Equality** - Value-based comparison (consistent, no identity operators)
- **Spread Operator** - JavaScript-style spread for struct composition (`{...obj}`)
- **Destructuring** - Full destructuring support for struct instances
- **Sealed Instances** - Struct fields defined at declaration (no runtime field addition)
- **Recursive Types** - Self-referential structs with cycle detection
- **Built-in Integration** - Complete integration with `len()`, `keys()`, `values()`, iteration
- **Iteration Order Guarantee** - Declaration order for predictability
- **Essential Built-ins** - `typeof()`, `copy()`, `deepcopy()`, `fields()` only

### Quick Example

```ml
// Define struct with optional type hints (documentation only)
struct Point {
    x: number,  // Hint: x should be a number (not enforced)
    y: number   // Hint: y should be a number (not enforced)
}

// Method with typed receiver and return type (hints only)
function (p: Point) distance(): number {
    import math;
    return math.sqrt(p.x * p.x + p.y * p.y);
}

// Create struct instance - types not enforced
p1 = Point{x: 3, y: 4};
p1.distance();  // ✅ Works

// Types are hints, not enforced
p2 = Point{x: "hello", y: "world"};  // ✅ Works (types are hints)

// Structural equality
p3 = Point{x: 3, y: 4};
p1 == p3;  // ✅ true (same values)

// Plain objects cannot call methods (struct identity check)
plain = {x: 3, y: 4};
plain.distance();  // ❌ Error: Object has no method 'distance'
p1 == plain;       // ✅ true (structural equality compares values)
```

---

## Design Rationale

### The Challenge: OOP in a Dynamic Language

Go's struct system assumes static typing with compile-time checks. ML is completely **dynamic** - no compile-time type checking exists, and type annotations are unused in practice (0 occurrences in 80+ existing test files).

**Key Question:** How can Go-style OOP provide value in a dynamic language without compromising ML's simplicity?

**Answer:** Focus on **structure** (struct identity, method dispatch, field sealing) and use types as **documentation hints** (like Python), not runtime enforcement.

### Design Options Evaluated

#### Option 1: Runtime Type Enforcement ❌
Types checked at runtime, throw errors on mismatch.
- **Pro:** Catches bugs, provides safety
- **Con:** Performance overhead, inconsistent with ML's dynamic nature, complex implementation
- **Verdict:** Rejected - not aligned with ML's philosophy (0 type annotations in 80+ files)

#### Option 2: Nominal Typing (Strict Classes) ❌
Strict class system with inheritance.
- **Pro:** Traditional OOP, familiar to Java/Python users
- **Con:** Too complex, requires `this`/`new` keywords, breaks ML simplicity
- **Verdict:** Rejected - too complex for educational language

#### Option 3: Documentation-Only Types ✅ **CHOSEN**
Types are hints for documentation, IDE, and optional static analysis (Python model).
- **Pro:** Simple, zero overhead, consistent with ML's dynamic nature, matches Python 3.5+
- **Con:** No runtime safety from types
- **Verdict:** **CHOSEN** - aligned with ML's philosophy and Python's approach

#### Option 4: Structural Identity for Method Dispatch ✅ **CHOSEN**
Struct instances can call methods, plain objects cannot (identity check only).
- **Pro:** Clear semantics, teaches OOP structure vs data
- **Con:** Creates two-tier system (but pedagogically valuable)
- **Verdict:** **CHOSEN** - essential for method dispatch

### Final Decision: Type Hints + Structural Identity

Combine **type hints for documentation** with **struct identity for method dispatch**:

1. **Structs define structure** - Named types with field declarations
2. **Type hints are documentation only** - No runtime type enforcement (Python model)
3. **Struct identity matters** - Only struct instances can call methods (not plain objects)
4. **Field sealing enforced** - Structs cannot add fields at runtime (structural property)
5. **Type annotations optional everywhere** - For documentation and IDE support

**What Gets Runtime Checking:**
- ✅ Struct identity (for method dispatch)
- ✅ Required fields (at struct creation)
- ✅ Field sealing (no dynamic field addition)

**What Does NOT Get Runtime Checking:**
- ❌ Field types (hints only)
- ❌ Parameter types (hints only)
- ❌ Return types (hints only)

**Benefits:**
- ✅ Consistent with ML's dynamic nature (like Python)
- ✅ Zero type checking overhead
- ✅ Simple implementation
- ✅ Clear intent (structs document shape for IDEs)
- ✅ IDE support (autocomplete based on type hints)
- ✅ Future: optional static checker (like mypy for Python)
- ✅ Teaches OOP structure (struct identity matters)

---

## Language Features

### 1. Struct Definitions

**Syntax:**
```ml
struct TypeName {
    field1: type,      // Optional type hint - checked at runtime
    field2,            // No type - accepts anything (dynamic)
    field3: type
}
```

**Semantics:**
- Structs are named types with fixed fields
- Field type hints are **optional** and serve as documentation only
- Types are **NOT checked at runtime** (Python model)
- Transpiles to Python `dataclass` with type annotations

**Examples:**

```ml
// Fully typed struct (all fields checked at creation)
struct Point {
    x: number,
    y: number
}

// Partially typed struct (mixed checking)
struct Person {
    name: string,      // Checked: must be string
    age: number,       // Checked: must be number
    metadata           // Dynamic: accepts any value
}

// Untyped struct (no checks, pure shape definition)
struct Config {
    host,
    port,
    options
}
```

**Runtime Behavior:**

```ml
// ✅ OK: all values work (types are hints, not enforced)
p1 = Point{x: 3, y: 4};
p2 = Point{x: "hello", y: 4};  // ✅ Also OK (types not checked)
p3 = Point{x: [1, 2], y: {nested: true}};  // ✅ Also OK

// ✅ OK: types are documentation hints
person = Person{name: "Alice", age: 30, metadata: {foo: "bar"}};
person2 = Person{name: 123, age: "thirty", metadata: "data"};  // ✅ OK

// ❌ Error: Missing required field (field names ARE checked)
p4 = Point{x: 3};  // Error: Missing required field 'y'

// ✅ OK: no type checking, all fields present
config = Config{host: "localhost", port: 8080, options: {}};
```

**Default Field Values:**

Structs can have default values for fields, making them optional in struct literals.

**Syntax:**
```ml
struct TypeName {
    field1: type = default_value,
    field2: type,
    field3 = default_value  // Can have default without type
}
```

**Examples:**
```ml
// Struct with defaults
struct Config {
    host: string = "localhost",
    port: number = 8080,
    debug: boolean = false,
    options  // No default - required
}

// Create with all defaults (except required fields)
c1 = Config{options: {}};
// Result: Config{host: "localhost", port: 8080, debug: false, options: {}}

// Override some defaults
c2 = Config{port: 3000, options: {verbose: true}};
// Result: Config{host: "localhost", port: 3000, debug: false, options: {verbose: true}}

// Override all fields
c3 = Config{host: "prod.com", port: 443, debug: true, options: {}};
```

**Semantics:**
- Fields with default values are optional in struct literals
- Omitted fields use their default value
- **Default expressions evaluated EACH TIME an instance is created (per-instance)**
- Fields without defaults are required

**Default Evaluation Semantics (CRITICAL):**

Default expressions are evaluated **per-instance**, not per-struct. Each instance gets a fresh evaluation.

```ml
struct Event {
    id: string = generate_uuid(),    // Different UUID for EACH instance
    timestamp: number = time.now(),  // Different timestamp for EACH instance
    items: array = []                // Fresh array for EACH instance (NOT shared!)
}

e1 = Event{};
e2 = Event{};

print(e1.id == e2.id);  // false (different UUIDs)
e1.items.append("data");
print(len(e2.items));   // 0 (separate arrays)
```

**Rationale:**
- ✅ Safe for mutable defaults (no shared state)
- ✅ Dynamic values work correctly (different UUID per instance)
- ✅ Matches developer expectations (JavaScript, TypeScript, Rust behavior)
- ✅ No surprising shared mutable state bugs

**Best Practices:**

1. **Use defaults for cheap values:**
   ```ml
   port: number = 8080              // ✅ Good: constant
   items: array = []                 // ✅ Good: cheap
   ```

2. **Avoid defaults for expensive operations:**
   ```ml
   // ❌ Bad: expensive operation runs EVERY time
   connection = expensive_connect()

   // ✅ Good: use factory function instead
   function new_service(): Service {
       conn = expensive_connect();
       return Service{connection: conn};
   }
   ```

3. **Be aware of side effects:**
   - Defaults with side effects execute on every instance creation
   - Use with caution

**Grammar Extension:**
```lark
struct_field: IDENTIFIER (":" type_annotation)? ("=" expression)? ("," | ";")
```

**See `default-semantics-analysis.md` for complete analysis.**

---

### 1a. Sealed Structs (No Dynamic Fields)

**Struct instances are sealed at creation**

**Core Principle:** Structs define structured data - fields are fixed at declaration.

**Semantics:**
- Struct instances are **mutable** (field values can be changed)
- Field addition is **forbidden** (structs are sealed)
- All fields must be defined in struct declaration
- Field **names** are enforced, field **types** are hints only

**Examples:**

```ml
struct Point {
    x: number,
    y: number
}

point = Point{x: 1, y: 2};

// ✅ Field mutation allowed (mutable values, any type)
point.x = 10;
point.y = 20;
point.x = "hello";  // ✅ Also OK (types are hints, not enforced)
point.y = [1, 2, 3];  // ✅ Also OK

// ❌ Field addition forbidden (sealed struct)
point.z = 3;  // Error: Point has no field 'z'
```

**Introspection:**

```ml
point = Point{x: 1, y: 2};

// Struct definition matches runtime fields (sealed)
fields(Point);        // ["x", "y"]
keys(point);          // ["x", "y"] (same - no dynamic fields)
values(point);        // [1, 2]
```

**Comparison with Plain Objects:**

```ml
struct Point { x: number, y: number }

// Struct instance (sealed)
struct_point = Point{x: 1, y: 2};
struct_point.z = 3;  // ❌ Error: no field 'z'

// Plain object (flexible)
plain_point = {x: 1, y: 2};
plain_point.z = 3;   // ✅ OK (plain objects are flexible)

// Method dispatch
struct_point.distance();  // ✅ Works
plain_point.distance();   // ❌ Error: Object has no method 'distance'

// Type identity
typeof(struct_point);     // "Point"
typeof(plain_point);      // "object"
```

**Use Cases - Alternatives to Dynamic Fields:**

1. **Optional Metadata → Use separate map:**
```ml
struct User {
    id: number,
    name: string
}

user = User{id: 1, name: "Alice"};

// Instead of: user.metadata = {...}
// Use external map:
metadata = {};
metadata[user.id] = {last_login: datetime.now()};
```

2. **Debugging → Use external tracking:**
```ml
// Instead of: point._debug_info = {...}
// Use external map keyed by meaningful value:
debug_info = {};
debug_info[point_id] = {created: datetime.now()};
```

3. **Caching → Use external cache:**
```ml
cache = {};

function compute_with_cache(obj: Computation) {
    key = obj.id;  // Use meaningful value as key
    if (!has_key(cache, key)) {
        cache[key] = expensive_operation(obj);
    }
    return cache[key];
}
```

**Serialization Behavior:**

```ml
struct Point { x: number, y: number }

point = Point{x: 1, y: 2};

// JSON serialization includes all declared fields
json_str = json.stringify(point);
// Result: '{"x":1,"y":2}'

// Deserialization reconstructs struct
json_obj = json.parse(json_str);
validated = from_dict(Point, json_obj);  // Point{x: 1, y: 2}
```

**Rationale:**
- **Clarity:** Fields are always what struct declares (no surprises)
- **Type safety:** All fields are type-checked (no escape hatch)
- **Simplicity:** No "two classes of fields" distinction
- **Teaching:** Easier to understand (structs = structured data)
- **External maps:** Provide flexibility when needed without polluting structs

---

### 2. Methods with Explicit Receivers

**Syntax:**
```ml
function (receiver: Type) method_name(param1: type, param2, ...): return_type {
    // method body
}
```

**All components are optional:**
- Receiver type hint: optional (but recommended)
- Parameter type hints: optional
- Return type hint: optional (NEW feature)

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

// Untyped method (pure duck typing)
function (v: Vector) add(other) {
    return Vector{
        x: v.x + other.x,
        y: v.y + other.y
    };
}
```

**Runtime Behavior:**
- Receiver type present → Struct identity check only (not field types)
- Parameter types present → Documentation only, NOT checked
- Return type present → Documentation only, NOT checked
- All types are hints for IDE and documentation

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
double = fn(x: number): number => x * 2;

// Arrow function - untyped (current behavior)
triple = fn(x) => x * 3;
```

**Runtime Behavior:**

```ml
function divide(a: number, b: number): number {
    if (b == 0) {
        throw {message: "Division by zero"};
    }
    return a / b;  // NOT checked (types are hints)
}

// All of these work (types are hints, not enforced)
result = divide(10, 2);      // ✅ OK: returns 5
result2 = divide("10", "2"); // ✅ OK: returns "1010" (string concatenation)
result3 = divide([1], [2]);  // ✅ OK: may crash or return unexpected result

// Types serve as documentation for developers and IDEs
```

---

### 4. Structural Type Matching

**Key Design:** Methods can ONLY be called on **struct instances**, not plain objects (struct identity check).

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

// Only struct instances can call methods:

// 1. Struct instance (works)
p1 = Point{x: 3, y: 4};
p1.distance();  // ✅ Works (struct instance)

// 2. Plain object (does NOT work)
p2 = {x: 3, y: 4};
p2.distance();  // ❌ Error: Object has no method 'distance' (not a struct)

// 3. Different struct type (does NOT work)
struct Vector3D {
    x: number,
    y: number,
    z: number
}
v = Vector3D{x: 3, y: 4, z: 5};
v.distance();  // ❌ Error: Vector3D has no method 'distance'

// 4. Type hints don't affect runtime (any values work)
p3 = Point{x: "hello", y: "world"};
p3.distance();  // ✅ Works (struct instance, types not checked)
// May crash when sqrt() is called with strings
```

**Struct Identity Algorithm:**

```python
def check_method_dispatch(obj, method_name):
    """Check if obj can call method (struct identity only)."""
    # Check 1: Is this a struct instance?
    if not has_struct_type_tag(obj):
        raise AttributeError("Object has no method (not a struct instance)")

    # Check 2: Does this struct type have this method?
    struct_type = get_struct_type_tag(obj)
    method_key = (struct_type, method_name)

    if method_key not in method_registry:
        raise AttributeError(f"{struct_type} has no method '{method_name}'")

    # NO type checking of field values
    return method_registry[method_key]
```

---

### 5. Struct Embedding (Composition)

**Syntax:**
```ml
struct DerivedType {
    BaseType,           // Embedded struct (anonymous field)
    extra_field: type
}
```

**Semantics:**
- Embedded struct fields promoted to parent
- Field access: `parent.embedded_field` works
- No method inheritance - explicit forwarding needed

**Example:**

```ml
struct Engine {
    horsepower: number,
    fuel_type: string
}

function (e: Engine) start() {
    print("Engine starting... " + str(e.horsepower) + " HP");
}

struct Car {
    Engine,              // Embedded Engine
    make: string,
    model: string
}

// Car gets Engine fields
honda = Car{
    Engine: Engine{horsepower: 200, fuel_type: "gasoline"},
    make: "Honda",
    model: "Civic"
};

// Access embedded fields directly
print(honda.horsepower);      // 200 (promoted from Engine)
print(honda.fuel_type);       // "gasoline"

// Access embedded struct explicitly
honda.Engine.start();         // "Engine starting... 200 HP"
```

---

### 5a. Spread Operator in Struct Literals

**Structs support JavaScript-style spread syntax for composition and cloning**

**Syntax:**
```ml
// Spread in struct literals
new_struct = StructType{...source_object, overrides...}
```

**Semantics:**
- Spread operator (`...`) copies fields from source object/struct
- Multiple spreads allowed (later spreads override earlier ones)
- Explicit properties override spread properties
- Works with structs, plain objects, and mixed sources
- Type checking happens on final combined result

**Basic Examples:**

```ml
struct Point {
    x: number,
    y: number,
    z: number
}

// Clone with modification
p1 = Point{x: 1, y: 2, z: 3};
p2 = Point{...p1, z: 10};           // Point{x: 1, y: 2, z: 10}
p3 = Point{...p1, x: 5, z: 5};      // Point{x: 5, y: 2, z: 5}

// Create from plain object
plain = {x: 1, y: 2};
point = Point{...plain, z: 0};      // Promote to Point

// Multiple spreads (right-to-left precedence)
defaults = {x: 0, y: 0, z: 0};
overrides = {x: 10};
p4 = Point{...defaults, ...overrides};  // Point{x: 10, y: 0, z: 0}
```

**Advanced Patterns:**

1. **Immutable Updates:**
```ml
struct Config {
    host: string,
    port: number,
    debug: boolean
}

// Update without mutation
config1 = Config{host: "localhost", port: 8080, debug: false};
config2 = Config{...config1, debug: true};  // New instance

// config1 unchanged
print(config1.debug);  // false
print(config2.debug);  // true
```

2. **Merging Multiple Sources:**
```ml
struct User {
    name: string,
    email: string,
    role: string,
    active: boolean
}

defaults = {role: "user", active: true};
user_data = {name: "Alice", email: "alice@example.com"};
admin_override = {role: "admin"};

// Combine multiple sources
user = User{...defaults, ...user_data, ...admin_override};
// Result: User{name: "Alice", email: "alice@example.com", role: "admin", active: true}
```

3. **Partial Updates from Functions:**
```ml
function update_position(point: Point, delta) {
    return Point{...point, x: point.x + delta.x, y: point.y + delta.y};
}

p1 = Point{x: 10, y: 20, z: 5};
p2 = update_position(p1, {x: 5, y: -3});
// Result: Point{x: 15, y: 17, z: 5}
```

4. **Struct Composition:**
```ml
struct Address {
    street: string,
    city: string,
    country: string
}

struct Person {
    name: string,
    age: number,
    street: string,
    city: string,
    country: string
}

address = Address{street: "Main St", city: "NYC", country: "USA"};
person = Person{name: "Bob", age: 30, ...address};
// Result: Person{name: "Bob", age: 30, street: "Main St", city: "NYC", country: "USA"}
```

5. **Defaults with Overrides:**
```ml
struct ServerConfig {
    host: string = "localhost",
    port: number = 8080,
    ssl: boolean = false,
    timeout: number = 30
}

// Use defaults plus partial config
user_config = {port: 3000, ssl: true};
config = ServerConfig{...user_config};
// Result: ServerConfig{host: "localhost", port: 3000, ssl: true, timeout: 30}
```

**Type Hints with Spread:**

```ml
struct Point {
    x: number,
    y: number
}

plain = {x: "hello", y: 4};

// Types are hints, not checked
point = Point{...plain};
// ✅ OK: types are hints, x can be "hello"

// Any values work
point2 = Point{...plain, x: 3};
// ✅ OK
point3 = Point{...plain, x: [1, 2, 3]};
// ✅ Also OK (types not enforced)
```

**Spread Order and Precedence:**

```ml
// Right-most value wins
obj1 = {a: 1, b: 2};
obj2 = {b: 3, c: 4};
result = StructType{...obj1, ...obj2, b: 5};
// Result: {a: 1, b: 5, c: 4}
// Precedence: obj1.a → obj2.c → obj2.b (override obj1.b) → explicit b (override all)
```

**Interaction with Default Values:**

```ml
struct Config {
    host: string = "localhost",
    port: number = 8080,
    debug: boolean = false
}

// Spread overrides defaults
partial = {host: "prod.com"};
config = Config{...partial};
// Result: Config{host: "prod.com", port: 8080, debug: false}
// Only host overridden, other defaults applied

// Empty spread still uses defaults
empty = {};
config2 = Config{...empty};
// Result: Config{host: "localhost", port: 8080, debug: false}
```

**Destructuring with Spread:**

```ml
struct Point3D {
    x: number,
    y: number,
    z: number
}

point = Point3D{x: 1, y: 2, z: 3};

// Extract some fields, spread rest
{x, ...rest} = point;
// x = 1
// rest = {y: 2, z: 3}

// Create new struct from rest
point2D = Point{x: 0, ...rest};  // Point{x: 0, y: 2, z: 3}
```

**Grammar Extension:**

Already updated above:
```lark
struct_literal: IDENTIFIER "{" struct_content? "}"
struct_content: (spread_property | struct_property) ("," (spread_property | struct_property))*
struct_property: IDENTIFIER ":" expression
spread_property: "..." expression
```

**Implementation Notes:**

1. **Evaluation Order:**
   - Spread expressions evaluated left-to-right
   - Later values override earlier values
   - Explicit properties have highest precedence

2. **Performance:**
   - Shallow copy of spread source fields
   - No deep cloning (use `deepcopy()` if needed)
   - Efficient for typical use cases

3. **Structural Safety:**
   - Field name checking happens on final composed object
   - All required fields must be present after spread
   - Type hints are documentation only (not validated)

**Rationale:**
- **Ergonomics:** Immutable updates without verbose field-by-field copying
- **Composition:** Natural pattern for combining data sources
- **Familiarity:** JavaScript/TypeScript developers already know this syntax
- **Flexibility:** Works seamlessly with ML's dynamic typing

---

### 5b. Destructuring Struct Instances

**Structs support destructuring assignment (same as plain objects)**

**Core Principle:** Structs are structurally compatible with plain objects - destructuring works identically.

**Syntax:**
```ml
// Object destructuring
{field1, field2, ...rest} = struct_instance

// Array destructuring (with values())
[value1, value2, ...rest] = values(struct_instance)
```

**Basic Destructuring:**

```ml
struct Point {
    x: number,
    y: number,
    z: number
}

point = Point{x: 10, y: 20, z: 30};

// Extract specific fields
{x, y} = point;
// x = 10, y = 20

// Extract with rename
{x: x_coord, y: y_coord} = point;
// x_coord = 10, y_coord = 20

// Extract subset
{z} = point;
// z = 30
```

**Destructuring with Rest:**

```ml
struct Config {
    host: string,
    port: number,
    debug: boolean,
    timeout: number
}

config = Config{host: "localhost", port: 8080, debug: true, timeout: 30};

// Extract some, collect rest
{host, port, ...options} = config;
// host = "localhost"
// port = 8080
// options = {debug: true, timeout: 30}
```

**Nested Destructuring:**

```ml
struct Address {
    street: string,
    city: string,
    country: string
}

struct Person {
    name: string,
    age: number,
    address: Address
}

person = Person{
    name: "Alice",
    age: 30,
    address: Address{street: "Main St", city: "NYC", country: "USA"}
};

// Nested destructuring
{name, address: {city, country}} = person;
// name = "Alice"
// city = "NYC"
// country = "USA"
```

**Array Destructuring with values():**

```ml
struct RGB {
    red: number,
    green: number,
    blue: number
}

color = RGB{red: 255, green: 100, blue: 50};

// Extract as array (in declaration order)
[r, g, b] = values(color);
// r = 255, g = 100, b = 50

// With rest
[first, ...rest] = values(color);
// first = 255
// rest = [100, 50]
```

**Destructuring in Function Parameters:**

```ml
struct Point { x: number, y: number }

// Destructure parameter
function print_coords({x, y}) {
    print("X: " + str(x) + ", Y: " + str(y));
}

point = Point{x: 5, y: 10};
print_coords(point);  // "X: 5, Y: 10"

// Works with plain objects too
print_coords({x: 3, y: 4});  // "X: 3, Y: 4"
```

**Destructuring in Loops:**

```ml
struct User {
    id: number,
    name: string,
    role: string
}

users = [
    User{id: 1, name: "Alice", role: "admin"},
    User{id: 2, name: "Bob", role: "user"}
];

// Destructure in loop
for (user in users) {
    {name, role} = user;
    print(name + " is " + role);
}

// Alternative: destructure loop variable (if supported)
// for ({name, role} in users) {
//     print(name + " is " + role);
// }
```

**Combining Spread and Destructuring:**

```ml
struct Point3D {
    x: number,
    y: number,
    z: number
}

point3d = Point3D{x: 1, y: 2, z: 3};

// Extract x, keep rest
{x, ...rest} = point3d;
// x = 1
// rest = {y: 2, z: 3}

// Create 2D point from rest
struct Point2D { x: number, y: number }
point2d = Point2D{x: 0, ...rest};
// point2d = Point2D{x: 0, y: 2} (only declared fields)
```

**Default Values in Destructuring:**

```ml
struct Config {
    host: string = "localhost",
    port: number = 8080
}

config = Config{};

// Destructure with fallback defaults (if fields undefined)
{host, port, debug = false} = config;
// host = "localhost" (from struct default)
// port = 8080 (from struct default)
// debug = false (fallback default - field doesn't exist)
```

**Type Preservation:**

```ml
struct Point { x: number, y: number }

point = Point{x: 1, y: 2};

// Destructured values keep their types
{x, y} = point;

// Type checking still applies
function needs_number(n: number) { return n * 2; }
result = needs_number(x);  // ✅ OK: x is number
```

**Use Cases:**

1. **Extract Configuration:**
```ml
struct ServerConfig {
    host: string,
    port: number,
    ssl: boolean,
    timeout: number
}

config = load_config();
{host, port} = config;  // Extract needed fields
start_server(host, port);
```

2. **Return Multiple Values:**
```ml
struct Result {
    success: boolean,
    data,
    error: string
}

function process(): Result {
    // ...
    return Result{success: true, data: result, error: ""};
}

{success, data, error} = process();
if (success) {
    use_data(data);
}
```

3. **Swap Values:**
```ml
struct Pair { a: number, b: number }

pair = Pair{a: 1, b: 2};
{a, b} = Pair{a: pair.b, b: pair.a};  // Swap
// a = 2, b = 1
```

**Grammar Note:**

Destructuring uses ML's existing destructuring syntax - no grammar changes needed:

```lark
// Already exists
destructuring_statement: destructuring_pattern "=" expression
destructuring_pattern: object_pattern | array_pattern
object_pattern: "{" IDENTIFIER ("," IDENTIFIER)* "}"
array_pattern: "[" IDENTIFIER ("," IDENTIFIER)* "]"
```

**Implementation:** Structs behave like objects for destructuring (structural compatibility)

**Rationale:**
- **Consistency:** Structs are enhanced objects - should support same operations
- **Ergonomics:** Natural pattern for extracting multiple fields
- **Familiarity:** JavaScript/Python developers expect this
- **No Changes:** Works with existing ML destructuring syntax

---

### 6. Recursive Struct Types

**Structs can reference themselves in field definitions (forward references allowed)**

**Syntax:**
```ml
struct Node {
    value: number,
    next: Node = null      // Self-reference with default
}

struct TreeNode {
    value: number,
    left: TreeNode = null,
    right: TreeNode = null
}
```

**Semantics:**
- Struct types can reference themselves (forward references allowed)
- Type registry resolves forward references after full struct registration
- Structural type checking uses visited set to prevent infinite recursion
- Runtime values can form cycles (circular references allowed)

**Examples:**

```ml
// Linked list
struct ListNode {
    data: number,
    next: ListNode = null
}

// Create a list: 1 -> 2 -> 3 -> null
node3 = ListNode{data: 3, next: null};
node2 = ListNode{data: 2, next: node3};
node1 = ListNode{data: 1, next: node2};

// Binary tree
struct TreeNode {
    value: number,
    left: TreeNode = null,
    right: TreeNode = null
}

tree = TreeNode{
    value: 10,
    left: TreeNode{value: 5, left: null, right: null},
    right: TreeNode{value: 15, left: null, right: null}
};

// Circular reference (allowed!)
node_a = ListNode{data: 1, next: null};
node_b = ListNode{data: 2, next: node_a};
node_a.next = node_b;  // Creates cycle: a -> b -> a -> b ...
```

**Implementation Considerations:**

1. **Type Registry - Forward References:**
   - Struct registration happens immediately (allow self-references)
   - Type validation happens after all structs registered
   - Two-phase process: register → validate

2. **Structural Type Checking - Cycle Detection:**
   - Track visited objects during structural matching
   - If object already visited, assume valid (don't recurse)
   - Prevents infinite loops with circular data structures

3. **Deep Copy - Circular References:**
   - Already handled! Python's `copy.deepcopy()` handles cycles automatically
   - Uses memo dictionary to track seen objects

**Grammar Impact:** None - existing syntax already supports this

**Type System Impact:**
- Type registry must support forward references
- Structural checking must track visited objects
- No change to runtime semantics (Python handles cycles)

**Use Cases:**
- Linked lists and doubly-linked lists
- Binary trees, AVL trees, red-black trees
- Graph nodes with neighbor references
- Recursive descent parsers
- State machines with transition references

---

## Grammar Specification

### Current Grammar (Before)

```lark
// Function Definitions (BEFORE)
function_definition: "function" IDENTIFIER "(" parameter_list? ")" "{" statement* "}"

// Arrow Functions (BEFORE)
arrow_function: FN "(" parameter_list? ")" "=>" arrow_body
arrow_body: expression | arrow_block

// Parameters (existing - already supports type hints)
parameter_list: parameter ("," parameter)*
parameter: IDENTIFIER (":" type_annotation)?
type_annotation: IDENTIFIER
```

### New Grammar (After)

```lark
// Function Definitions (AFTER - added return type and method receiver)
function_definition: "function" method_receiver? IDENTIFIER "(" parameter_list? ")" return_type? "{" statement* "}"
method_receiver: "(" IDENTIFIER ":" IDENTIFIER ")"
return_type: ":" type_annotation

// Arrow Functions (AFTER - added return type)
arrow_function: FN "(" parameter_list? ")" return_type? "=>" arrow_body
arrow_body: expression | arrow_block
arrow_block: "{" statement+ "}"

// Parameters (unchanged)
parameter_list: parameter ("," parameter)*
parameter: IDENTIFIER (":" type_annotation)?
type_annotation: IDENTIFIER

// Struct Declaration (NEW)
struct_declaration: "struct" IDENTIFIER "{" struct_field* "}"
struct_field: IDENTIFIER (":" type_annotation)? ("," | ";")

// Struct Literal (NEW - with spread support)
struct_literal: IDENTIFIER "{" struct_content? "}"
struct_content: (spread_property | struct_property) ("," (spread_property | struct_property))*
struct_property: IDENTIFIER ":" expression
spread_property: "..." expression

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

### Grammar Changes Summary

**New Rules Added:**
1. `return_type` - Optional return type annotation
2. `method_receiver` - Receiver parameter for methods
3. `struct_declaration` - Struct type definitions with default values
4. `struct_field` - Struct field with optional type and default value
5. `struct_literal` - Type-prefixed object creation with spread support
6. `struct_content` - Struct literal content (properties and spreads)
7. `spread_property` - Spread operator in struct literals (`...expr`)

**Extended Rules:**
1. `function_definition` - Added `method_receiver?` and `return_type?`
2. `arrow_function` - Added `return_type?`
3. `statement` - Added `struct_declaration`
4. `primary` - Added `struct_literal`
5. `struct_field` - Added default value support (`= expression`)

**New Keywords:**
- `struct` (must come before IDENTIFIER in lexer)

**New Operators:**
- `...` - Spread operator (in struct literals and destructuring)

---

## Type System Design

### Built-in Type Names

```ml
// Primitive types
number   // int or float
string   // text
boolean  // true/false
array    // any array
object   // any object/dictionary

// Special types
any      // no checking (default when no type specified)
void     // function returns nothing
```

### Type Checking Rules

**1. Field Types (struct creation)**
```ml
struct Point { x: number, y: number }
p = Point{x: 3, y: 4};  // Check: x is number? y is number?
```

**2. Parameter Types (function call)**
```ml
function add(a: number, b: number) { ... }
add(3, 4);    // Check: a is number? b is number?
```

**3. Return Types (function return)**
```ml
function get_name(): string { return "Alice"; }
// Check: return value is string?
```

**4. Receiver Types (method call - structural)**
```ml
function (p: Point) distance() { ... }
obj.distance();  // Check: obj has x, y fields of type number?
```

### Runtime Type Checking Implementation

**Type checking helper:**

```python
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
```

**Struct with type checking:**

```python
@dataclass
class Point:
    x: Union[int, float]
    y: Union[int, float]

    def __post_init__(self):
        # Only check fields with type hints in ML source
        _check_type(self.x, 'number', 'Point.x')
        _check_type(self.y, 'number', 'Point.y')
```

**Method with type checking:**

```python
def Point_distance(self):
    # Check receiver type (structural)
    _check_structural_type(self, 'Point', required_fields=['x', 'y'])

    # Method body
    result = math.sqrt(self.x * self.x + self.y * self.y)

    # Check return type (if specified in ML)
    return _check_type(result, 'number', 'Point.distance return value')

Point.distance = Point_distance
```

**Function with type checking:**

```python
def add(a, b):
    # Check parameter types (if specified in ML)
    _check_type(a, 'number', 'parameter a')
    _check_type(b, 'number', 'parameter b')

    # Function body
    result = a + b

    # Check return type (if specified in ML)
    return _check_type(result, 'number', 'add return value')
```

### Performance Optimization

**Strategy:**
1. **No checking when no types** - Zero overhead for untyped code
2. **Cached type checks** - Cache structural type compatibility
3. **Inline checks** - No function call overhead for primitives
4. **Production flag** - Optional disable runtime checks

**Performance Impact:**
- Untyped code: 0% overhead
- Typed primitives: <5% overhead (isinstance checks)
- Typed structs: <10% overhead (structural checks, cached)
- Overall mixed code: <2% overhead

---

## Pure Structural Typing

### Overview

ML's OOP system adopts a **pure structural typing model** for simplicity and consistency. All comparisons are value-based, not identity-based.

**Core principle:** "If it looks like the same data, it is equal."

### Design Decision: Pure Structural Model

**Philosophy:** Value-based equality for all operations. Simple and consistent.

**Key aspects:**
1. **Equality (==)** - Structural (compares field values)
2. **Method Dispatch** - Strict (only struct instances)
3. **Type Checking** - String comparison (`typeof()`)
4. **No identity operators** - No `===`, use Python's `id()` if needed

---

### Structural Equality (==)

**Compare field values, regardless of type:**

```ml
struct Point { x: number, y: number }

p1 = Point{x: 3, y: 4};
p2 = Point{x: 3, y: 4};
plain = {x: 3, y: 4};

// All return true (same field values)
p1 == p2;       // ✅ true (same values)
p1 == plain;    // ✅ true (same values, structural)
p2 == plain;    // ✅ true (same values)

// Different values
p3 = Point{x: 5, y: 6};
p1 == p3;       // ❌ false (different values)

// Extra fields ignored in comparison
plain2 = {x: 3, y: 4, z: 5};
p1 == plain2;   // ✅ true (x and y match)
```

**Algorithm:**
1. Get all fields from both objects
2. For each field name, compare values recursively
3. Return true if all common fields have equal values
4. Extra fields in either object are ignored

**Rationale:** Intuitive - equality checks if objects represent the same data.

Compare field values, not type identity:

```ml
struct Point { x: number, y: number }

p1 = Point{x: 3, y: 4};
p2 = Point{x: 3, y: 4};
plain = {x: 3, y: 4};

// All return true (same field values)
p1 == p2;       // ✅ true (same values)
p1 == plain;    // ✅ true (same values, structural)
p2 == plain;    // ✅ true (same values)

// Different values
p3 = Point{x: 5, y: 6};
p1 == p3;       // ❌ false (different values)
```

**Rationale:** Intuitive behavior - equality checks if objects represent the same data, not whether they're the same type.

---

### Type Checking with typeof()

When you need to check or compare types, use the `typeof()` built-in:

```ml
struct Point { x: number, y: number }
struct Vector { x: number, y: number }

point = Point{x: 3, y: 4};
plain = {x: 3, y: 4};

typeof(point);      // "Point"
typeof(plain);      // "object"
typeof(42);         // "number"
typeof("hello");    // "string"

// Type validation
if (typeof(point) == "Point") {
    // Process Point struct
}

// Type comparison
if (typeof(p1) == typeof(p2)) {
    // Same type
}

// Useful for:
// - Type-based dispatch
// - Debugging and logging
// - Runtime type validation
```

---

### When to Use Each Operation

| Use Case | Operator/Built-in | Example |
|----------|-------------------|---------|
| **Compare data values** | `==` | `point1 == point2` |
| **Get type name** | `typeof()` | `typeof(point)` |
| **Compare types** | `typeof()` | `typeof(p1) == typeof(p2)` |
| **Check specific type** | `typeof()` | `typeof(point) == "Point"` |

**Note:** If you need reference equality (checking if two variables point to the same object), you can use Python's `id()` function when interoperating with Python code, but this is not a core ML feature.

---

### Complete Examples

#### Example 1: Structural Equality

```ml
struct Point { x: number, y: number }

p1 = Point{x: 3, y: 4};
p2 = Point{x: 3, y: 4};
p3 = p1;
plain = {x: 3, y: 4};

// ===== EQUALITY (==) - Structural =====
print(p1 == p2);        // true (same values)
print(p1 == plain);     // true (same values, different types OK)
print(p2 == plain);     // true

// ===== TYPE CHECKING =====
print(typeof(p1));              // "Point"
print(typeof(plain));           // "object"
print(typeof(p1) == "Point");   // true
print(typeof(plain) == "Point"); // false
print(typeof(p1) == typeof(p2));  // true (both Point)
print(typeof(p1) == typeof(plain)); // false (Point vs object)
```

---

#### Example 2: Value-Based Caching

```ml
struct User { id: string, name: string }

function get_permissions(user: User): array {
    // Cache results by user ID (value-based key)
    cache_key = user.id;
    if (!has_key(permission_cache, cache_key)) {
        // Expensive database lookup
        perms = database.query("SELECT * FROM permissions WHERE user_id = ?", user.id);
        permission_cache[cache_key] = perms;
    }
    return permission_cache[cache_key];
}

user1 = User{id: "123", name: "Alice"};
user2 = User{id: "123", name: "Alice"};  // Same data, different variable

// First call - cache miss
perms1 = get_permissions(user1);  // Database query

// Second call with same user ID - cache hit!
perms2 = get_permissions(user1);  // From cache

// Third call with different variable, same ID - cache hit!
perms3 = get_permissions(user2);  // From cache (same user.id)
```

**Note:** In pure structural model, cache by meaningful values (like user.id), not by object identity.

---

#### Example 3: Type Validation

```ml
struct Point { x: number, y: number }
struct Vector { x: number, y: number }

function process_point(obj) {
    // Option 1: Check exact struct type
    if (typeof(obj) != "Point") {
        throw {message: "Expected Point struct"};
    }
    return obj.x + obj.y;
}

function process_coords(obj) {
    // Option 2: Allow any object with required fields (duck typing)
    if (!has_key(obj, "x") || !has_key(obj, "y")) {
        throw {message: "Expected object with x, y fields"};
    }
    return obj.x + obj.y;
}

// Works with Point instances
process_point(Point{x: 1, y: 2});  // ✅
process_coords(Point{x: 1, y: 2});  // ✅

// Type-strict rejects plain objects
process_point({x: 1, y: 2});  // ❌ throws error

// Structural accepts plain objects
process_coords({x: 1, y: 2});  // ✅
```

---

#### Example 4: Filtering by Type

```ml
struct Point { x: number, y: number }
struct Circle { center: Point, radius: number }

shapes = [
    Point{x: 1, y: 2},
    Circle{center: Point{x: 0, y: 0}, radius: 5},
    {x: 3, y: 4},  // Plain object
    Point{x: 5, y: 6}
];

// Filter to only Point structs
points = filter(shapes, fn(s) => typeof(s) == "Point");
// Result: [Point{x: 1, y: 2}, Point{x: 5, y: 6}]

// Filter to objects with x, y fields (structural)
coords = filter(shapes, fn(s) => has_key(s, "x") && has_key(s, "y"));
// Result: [Point{x: 1, y: 2}, {x: 3, y: 4}, Point{x: 5, y: 6}]
```

---

### Grammar Changes Required

**No grammar changes needed** - The existing ML grammar already supports struct syntax and `==` equality operator.

---

### Built-in Functions Required

**Extend `typeof(value): string`** (already available in ML)
- Return struct type name for struct instances (e.g., "Point")
- Return "object" for plain objects
- Return "number", "string", "boolean", "array", "function" for other types

**Usage:**
```ml
struct Point { x: number, y: number }
point = Point{x: 3, y: 4};
typeof(point);  // "Point"
typeof({x: 3, y: 4});  // "object"
```

---

### Implementation Changes

#### Structural Equality Implementation

```python
def struct_equality(obj1, obj2):
    """Structural equality - compare field values regardless of type."""

    # Get fields from both objects
    fields1 = get_object_fields(obj1)  # Works for structs and plain objects
    fields2 = get_object_fields(obj2)

    # Different field sets → not equal
    if set(fields1) != set(fields2):
        return False

    # Compare all field values
    for field in fields1:
        if getattr(obj1, field) != getattr(obj2, field):
            return False

    return True
```

**Key aspects:**
- Compares field values, not type identity
- Works for both struct instances and plain objects
- Two objects are equal if they have the same fields with the same values

---

### Design Philosophy

**Pure Structural Model** - The ML OOP system uses structural typing throughout:

✅ **Consistent** - Structural equality for all comparisons
✅ **Simple** - Only one equality operator to learn
✅ **Intuitive** - `==` compares values (like most languages)
✅ **Clean Semantics** - No identity vs value confusion
✅ **Type Checking** - Use `typeof()` for type validation

**Key Principles:**
```ml
struct Point { x: number, y: number }

point = Point{x: 3, y: 4};
plain = {x: 3, y: 4};

// Equality compares values
point == plain;  // true (same field values)

// Type checking with typeof()
typeof(point) == "Point";  // true
typeof(plain) == "Point";  // false
```

---

### Common Patterns

#### Pattern 1: Value-Based Caching

Use meaningful values as cache keys, not object identity:

```ml
cache = {};
user = User{id: "123", name: "Alice"};

// Good: Cache by user ID
cache_key = user.id;
cache[cache_key] = compute_permissions(user);

// Later, same ID retrieves from cache
another_user = User{id: "123", name: "Alice"};
perms = cache[another_user.id];  // Cache hit!
```

---

#### Pattern 2: Type Validation

Use `typeof()` for type checking:

```ml
function process_point(obj) {
    if (typeof(obj) != "Point") {
        throw {message: "Expected Point struct"};
    }
    return obj.x + obj.y;
}

// Or use duck typing
function process_coords(obj) {
    if (!has_key(obj, "x") || !has_key(obj, "y")) {
        throw {message: "Expected object with x, y"};
    }
    return obj.x + obj.y;
}
```

---

### Summary

| Aspect | Behavior | Use When |
|--------|----------|----------|
| **Methods** | Strict (struct instances only) | Only struct instances can call methods |
| **Equality (==)** | Structural | Comparing data values |
| **typeof()** | Type introspection | Get type name, compare types |
| **Struct Fields** | Sealed | Fields defined at declaration only |

**Design Philosophy:** Pure structural equality with strict method dispatch for safety.

---

## Standard Library Built-ins

### Overview

Structs require dedicated built-in functions for type introspection, metadata access, and runtime operations. These built-ins are **critical** for practical struct usage and enable powerful metaprogramming patterns.

### Tier 1: Type Introspection (MUST HAVE)

#### typeof(value) - Extended

**Extended to support struct types**

```ml
// Primitive types (existing behavior)
typeof(42)                    // "number"
typeof("hello")               // "string"
typeof(true)                  // "boolean"
typeof([1,2,3])               // "array"
typeof({a: 1})                // "object"

// Struct types (NEW)
struct Point { x: number, y: number }
point = Point{x: 3, y: 4};
plain = {x: 3, y: 4};

typeof(point)                 // "Point" (struct type name)
typeof(plain)                 // "object" (plain object)
```

**Implementation:**
- Check if value has struct metadata (type tag)
- Return struct type name if struct instance
- Return "object" for plain objects
- Maintain backward compatibility

**Rationale:** Essential for distinguishing structs from plain objects at runtime.

---

#### copy(obj) - New **CRITICAL**

**Create shallow copy of struct or object**

**Essential for struct manipulation without mutation.**

```ml
struct Point { x: number, y: number }

point1 = Point{x: 3, y: 4};
point2 = point1;  // Reference copy (both point to same object)

point2.x = 10;
print(point1.x);  // 10 (mutation affected point1!)

// Use copy() for independent copy
point3 = copy(point1);
point3.x = 20;
print(point1.x);  // 10 (point1 unchanged)
```

**Common use cases:**

1. **Immutable updates:**
```ml
function move_point(p: Point, dx: number, dy: number): Point {
    result = copy(p);  // Don't mutate input
    result.x = result.x + dx;
    result.y = result.y + dy;
    return result;
}
```

2. **Struct transformations:**
```ml
function scale_point(p: Point, factor: number): Point {
    scaled = copy(p);
    scaled.x = scaled.x * factor;
    scaled.y = scaled.y * factor;
    return scaled;
}
```

3. **Defensive copying:**
```ml
function store_config(config: Config) {
    stored = copy(config);  // Prevent external mutation
    database.save(stored);
}
```

**Shallow copy behavior:**
```ml
struct Address { street: string, city: string }
struct Person { name: string, address: Address }

person1 = Person{
    name: "Alice",
    address: Address{street: "Main", city: "NYC"}
};

person2 = copy(person1);
person2.name = "Bob";  // Independent

// BUT: Nested structs are still shared!
person2.address.city = "LA";
print(person1.address.city);  // "LA" (shared reference)
```

**Implementation:**
- Shallow copy: copy top-level fields only
- Nested structs/objects are still references
- Works with both structs and plain objects

**Rationale:** Absolutely essential - without copy(), there's no way to duplicate structs without manual field-by-field copying.

---

#### deepcopy(obj) - New **CRITICAL**

**Create deep copy of struct or object (recursive)**

**Essential for nested struct manipulation with complete independence.**

```ml
struct Address { street: string, city: string }
struct Person { name: string, address: Address }

person1 = Person{
    name: "Alice",
    address: Address{street: "Main St", city: "NYC"}
};

// Shallow copy - nested structs are shared
person2 = copy(person1);
person2.address.city = "LA";
print(person1.address.city);  // "LA" (mutation affected person1!)

// Deep copy - complete independence
person3 = deepcopy(person1);
person3.address.city = "SF";
print(person1.address.city);  // "NYC" (person1 unchanged)
print(person3.address.city);  // "SF"
```

**Common use cases:**

1. **Nested struct cloning:**
```ml
struct Config {
    database: object,
    cache: object,
    logging: object
}

function clone_config(cfg: Config): Config {
    return deepcopy(cfg);  // All nested objects independent
}
```

2. **Undo/Redo functionality:**
```ml
struct GameState {
    player: Player,
    enemies: array,
    items: array
}

history = [];

function save_state(state: GameState) {
    history = history + [deepcopy(state)];  // Complete snapshot
}

function undo(): GameState {
    return deepcopy(history[len(history) - 1]);  // Restore snapshot
}
```

3. **Defensive copying in APIs:**
```ml
global_config = Config{...};

function get_config(): Config {
    return deepcopy(global_config);  // Caller can't mutate global
}
```

4. **Parallel processing with independent data:**
```ml
function process_batch(data) {
    tasks = [];
    for (i in range(4)) {
        // Each task gets independent copy
        tasks = tasks + [spawn_task(deepcopy(data))];
    }
    return tasks;
}
```

**Deep copy behavior:**
```ml
struct Node {
    value: number,
    children: array  // Array of Node structs
}

tree = Node{
    value: 1,
    children: [
        Node{value: 2, children: []},
        Node{value: 3, children: []}
    ]
};

tree_copy = deepcopy(tree);
tree_copy.children[0].value = 99;

print(tree.children[0].value);  // 1 (original unchanged)
print(tree_copy.children[0].value);  // 99 (copy modified)
```

**Implementation:**
- Deep copy: recursively copy all nested objects/structs/arrays
- Handles circular references (detect and break cycles)
- Works with structs, plain objects, arrays, and primitives
- Maps to Python's `copy.deepcopy()`

**Rationale:**
- **Essential for nested structs** - OOP systems frequently use composition
- **Prevents shared state bugs** - Complete independence guarantees safety
- **Trivial implementation** - Python's `copy.deepcopy()` handles all complexity
- **Developer expectations** - Standard feature in all major languages
- **Complements shallow copy** - Developers need both tools

**Performance note:** Deep copy is more expensive than shallow copy. Use `copy()` when nested structures don't need independence, use `deepcopy()` when complete isolation is required.

---

#### fields(StructType) - New

**Get list of field names from struct type**

```ml
struct Person {
    name: string,
    age: number,
    email
}

field_list = fields(Person);   // ["name", "age", "email"]

// Use for iteration
for (field in fields(Person)) {
    print("Field: " + field);
}

// Use for validation
function has_all_fields(obj, StructType) {
    for (field in fields(StructType)) {
        if (!has_key(obj, field)) {
            return false;
        }
    }
    return true;
}
```

**Implementation:**
- Look up StructType in type registry
- Return array of field names
- Maintain field declaration order

**Rationale:** Essential for metaprogramming and generic operations.

---

### Deferred to Phase 2

#### field_types(StructType) - Deferred

**Get field type annotations**

**Status:** Deferred to Phase 2 - nice to have but not critical for MVP.

```ml
struct Point {
    x: number,
    y: number,
    metadata    // No type
}

types = field_types(Point);
// Returns: {x: "number", y: "number", metadata: null}
```

**Use cases:**
- Runtime type validation
- Documentation generation
- IDE tooling

**Why deferred:** Not critical for MVP, complex implementation.

---

### Removed (Redundant with Existing Features)

The following built-ins were removed as redundant. See `builtin-analysis.md` for full analysis.

#### ~~is_struct(obj)~~ - REMOVED

**Redundant with typeof().**

Use instead:
```ml
// Check if struct (not primitive or plain object)
typeof(obj) not in ["number", "string", "boolean", "array", "object"]

// Or create userland helper
function is_struct(obj) {
    type = typeof(obj);
    return type[0] >= "A" && type[0] <= "Z";  // Structs start with uppercase
}
```

---

#### ~~same_type(obj1, obj2)~~ - REMOVED

**Redundant with typeof().**

Use instead:
```ml
// Instead of: same_type(p1, p2)
// Use: typeof(p1) == typeof(p2)

typeof(p1) == typeof(p2)  // Check if same type
```

---

#### ~~struct_type(obj)~~ - REMOVED

**Identical to typeof().**

Use instead:
```ml
// Instead of: struct_type(obj)
// Use: typeof(obj)

typeof(point)  // "Point"
typeof(plain)  // "object"
```

---

#### ~~new(Type, kwargs)~~ - REMOVED

**Redundant with struct literals.**

Use instead:
```ml
// Instead of: new(Config, {port: 3000})
// Use: Config{port: 3000}  // Defaults applied automatically

Config{port: 3000}  // Struct literal with defaults
```

---

#### ~~get_field(obj, name)~~ - REMOVED

**Redundant with bracket notation.**

Use instead:
```ml
// Instead of: get_field(obj, "x")
// Use: obj["x"]

obj["x"]  // Standard bracket notation
obj[field_name]  // Dynamic field access
```

---

#### ~~set_field(obj, name, val)~~ - REMOVED

**Redundant with bracket assignment.**

Use instead:
```ml
// Instead of: set_field(obj, "x", 10)
// Use: obj["x"] = 10

obj["x"] = 10  // Standard bracket assignment
obj[field_name] = value  // Dynamic field setting
```

---

### Summary of New Built-ins

**SIMPLIFIED: Pure structural model with 4 essential built-ins**

**Design principle:** Minimal built-ins for essential operations that can't be implemented in userland.

#### Phase 1 MVP: Essential Built-ins (4 total)

| Built-in | Priority | Purpose | Why Essential |
|----------|----------|---------|---------------|
| `typeof(value)` | 🔴 CRITICAL | Extended to return struct type names | Type introspection - already exists, just extend it |
| `fields(StructType)` | 🔴 CRITICAL | Get list of field names from struct type | Needs type registry access |
| **`copy(obj)`** | **🔴 CRITICAL** | **Shallow copy of struct** | **Clone top-level - common pattern** |
| **`deepcopy(obj)`** | **🔴 CRITICAL** | **Deep copy with nested independence** | **Recursive clone - hard to implement manually** |

#### Phase 2: Deferred Built-ins (1 total)

| Built-in | Priority | Purpose | Why Deferred |
|----------|----------|---------|--------------|
| `field_types(StructType)` | 🟡 MEDIUM | Get field type annotations | Nice to have but not critical for MVP |

#### REMOVED: Redundant or Unnecessary Built-ins (8 total)

| Built-in | Why Removed | Alternative |
|----------|-------------|-------------|
| ~~`is_struct(obj)`~~ | Redundant with typeof | `typeof(obj) != "object"` |
| ~~`instanceof(obj, Type)`~~ | Redundant with typeof | `typeof(obj) == "TypeName"` |
| ~~`same_type(obj1, obj2)`~~ | Redundant with typeof | `typeof(obj1) == typeof(obj2)` |
| ~~`struct_type(obj)`~~ | Identical to typeof | `typeof(obj)` |
| ~~`identity(obj)`~~ | Removed with identity checks | Use Python's `id()` if needed |
| ~~`new(Type, kwargs)`~~ | Redundant with struct literals | `Type{...}` with defaults |
| ~~`get_field(obj, name)`~~ | Redundant with bracket syntax | `obj[name]` |
| ~~`set_field(obj, name, val)`~~ | Redundant with bracket assignment | `obj[name] = val` |

---

## Method Dispatch Algorithm

### Overview

Method dispatch determines which method to call when `obj.method()` is invoked. In the **pure structural model with strict dispatch**, only struct instances can call methods.

**Key principle:** Type safety - methods belong to struct types, not plain objects.

### Lookup Process

**Step 1: Check if obj is a struct instance**

```ml
obj.method(args);
```

**Check:** Is `obj` a struct instance?
- YES: Continue to Step 2
- NO: Raise `AttributeError` (plain objects cannot call methods)

---

**Step 2: Struct Instance Dispatch**

```python
# Pseudocode
if not has_struct_type_tag(obj):
    raise AttributeError("Object has no method 'method' (not a struct instance)")

struct_type = get_struct_type_tag(obj)
method_key = (struct_type, "method")

if method_key in method_registry:
    call method_registry[method_key](obj, args)
else:
    raise AttributeError(f"{struct_type} has no method 'method'")
```

**Example - Success:**
```ml
struct Point { x: number, y: number }
function (p: Point) distance() { ... }

point = Point{x: 3, y: 4};
point.distance();  // ✅ OK: Lookup (Point, distance) → call Point.distance
```

**Example - Plain Object Error:**
```ml
struct Point { x: number, y: number }
function (p: Point) distance() { ... }

plain = {x: 3, y: 4};
plain.distance();  // ❌ Error: Object has no method 'distance' (not a struct instance)
```

**Example - Method Not Found:**
```ml
struct Point { x: number, y: number }
function (p: Point) distance() { ... }

point = Point{x: 3, y: 4};
point.area();  // ❌ Error: Point has no method 'area'
```

**Since only struct instances can call methods, there is no ambiguity:**
- Each struct instance has exactly one type
- Method lookup is always unambiguous: `(struct_type, method_name)`
- No need for structural matching or precedence rules

**Benefits:**
- ✅ Simple semantics: methods belong to types
- ✅ Clear errors: "Object is not a struct instance" vs "Point has no method X"
- ✅ Type safety: only typed values can call methods
- ✅ No performance overhead from structural matching

---

### Runtime Checks on Method Calls

**When a method is called, only struct identity is checked (NOT parameter types):**

```ml
struct Point { x: number, y: number }

function (p: Point) move(dx: number, dy: number): Point {
    return Point{x: p.x + dx, y: p.y + dy};
}

point = Point{x: 1, y: 2};

// ✅ OK: struct instance, all parameters work
result = point.move(5, 10);

// ✅ Also OK: types are hints, not enforced
result = point.move("hello", 10);  // Works (may produce unexpected result)
result = point.move([1], {y: 2});  // Works (may crash or produce unexpected result)
```

**Runtime checking happens:**
1. ✅ Struct identity check (is receiver a Point instance?)
2. ✅ Method existence check (does Point have a move method?)
3. ❌ Parameter types (NOT checked - hints only)
4. ❌ Return type (NOT checked - hints only)

**Rationale:** Consistent with ML's dynamic nature. Types serve as documentation for developers and IDEs, not runtime enforcement.

---

## Built-in Integration

### Overview

Existing ML built-in functions must work intuitively with struct instances. This section defines behavior for all core built-ins when applied to structs.

### len(struct_instance)

**Returns the number of fields in the struct**

```ml
struct Point { x: number, y: number }
struct Person { name: string, age: number, email: string }

point = Point{x: 3, y: 4};
person = Person{name: "Alice", age: 30, email: "alice@example.com"};

len(point)     // 2
len(person)    // 3
```

**Implementation:** Return `len(fields(struct_type(obj)))`

---

### str(struct_instance)

**Returns formatted string representation**

**Format:** `StructName{field1: value1, field2: value2}`

```ml
struct Point { x: number, y: number }

point = Point{x: 3, y: 4};

str(point)     // "Point{x: 3, y: 4}"
```

**Nested structs:**
```ml
struct Address { street: string, city: string }
struct Person { name: string, address: Address }

addr = Address{street: "Main St", city: "NYC"};
person = Person{name: "Alice", address: addr};

str(person)
// "Person{name: "Alice", address: Address{street: "Main St", city: "NYC"}}"
```

**Implementation:** Recursive formatting of nested structs

---

### print(struct_instance)

**Prints formatted string representation**

```ml
struct Point { x: number, y: number }

point = Point{x: 3, y: 4};

print(point);
// Output: Point{x: 3, y: 4}
```

**Implementation:** Call `print(str(struct_instance))`

---

### keys(struct_instance)

**Returns array of field names**

```ml
struct Person { name: string, age: number, email: string }

person = Person{name: "Alice", age: 30, email: "alice@example.com"};

keys(person)   // ["name", "age", "email"]
```

**Implementation:** Return `fields(struct_type(obj))`

**Note:** Same behavior as plain objects for consistency

---

### values(struct_instance)

**Returns array of field values in field declaration order**

```ml
struct Point { x: number, y: number }

point = Point{x: 3, y: 4};

values(point)  // [3, 4]
```

**Implementation:**
```python
[getattr(obj, field) for field in fields(struct_type(obj))]
```

---

### Equality (==, !=)

**UPDATED: Structural equality - compare all field values regardless of type**

**See [Structural vs Nominal Typing](#structural-vs-nominal-typing) for complete details.**

```ml
struct Point { x: number, y: number }

p1 = Point{x: 3, y: 4};
p2 = Point{x: 3, y: 4};
p3 = Point{x: 5, y: 6};

p1 == p2       // true  (same field values)
p1 == p3       // false (different values)
p1 != p3       // true
```

**Mixed struct and plain object (UPDATED):**
```ml
point = Point{x: 3, y: 4};
plain = {x: 3, y: 4};

point == plain  // ✅ true (structural equality - same field values)

// For type checking, use typeof():
typeof(point) == "Point"  // true
typeof(plain) == "Point"  // false
```

**Rationale:** Structural equality is consistent with pure structural typing and preserves duck typing philosophy. Use `typeof()` for type checks.

**Implementation:**
```python
def struct_equality(obj1, obj2):
    """Structural equality - compare field values regardless of type."""

    # Get fields from both objects
    fields1 = get_object_fields(obj1)  # Works for structs and plain objects
    fields2 = get_object_fields(obj2)

    # Different field sets → not equal
    if set(fields1) != set(fields2):
        return False

    # Compare all field values
    for field in fields1:
        if getattr(obj1, field) != getattr(obj2, field):
            return False

    return True
```

---

### Comparison (<, >, <=, >=)

**Raises TypeError by default**

```ml
struct Point { x: number, y: number }

p1 = Point{x: 3, y: 4};
p2 = Point{x: 5, y: 6};

p1 < p2   // TypeError: '<' not supported between Point instances
```

**Rationale:** No natural ordering for arbitrary structs

**Future:** Could support custom comparison methods or explicit ordering fields

---

### Iteration

**Iterating over struct instance iterates over field names in declaration order**

**Iteration Order Guarantee:**
- Fields iterated in **struct declaration order**
- Deterministic and predictable across runs
- Consistent with `keys()`, `values()`, and `fields()` order

```ml
struct Person { name: string, age: number, email: string }

person = Person{name: "Alice", age: 30, email: "alice@example.com"};

for (field in person) {
    print(field);
}
// Output (guaranteed order):
// name
// age
// email
```

**Note:** Structs are sealed - all fields are defined at declaration. No dynamic fields can be added at runtime.

**Alternative: Iterate over values**
```ml
for (value in values(person)) {
    print(value);
}
// Output (same order as fields):
// Alice
// 30
// alice@example.com
```

**Iterate over key-value pairs:**
```ml
for (field in person) {
    value = person[field];
    print(field + ": " + str(value));
}
// Output:
// name: Alice
// age: 30
// email: alice@example.com
```

**Order Consistency:**
```ml
struct Data { a: number, b: number, c: number }
data = Data{a: 1, b: 2, c: 3};

// All return same order
keys(data);     // ["a", "b", "c"]
values(data);   // [1, 2, 3]
fields(Data);   // ["a", "b", "c"]

// Iteration matches
for (k in data) { ... }  // Visits: a, b, c (in order)
```

**Implementation:** Iterator returns field names in declaration order (consistent with Python 3.7+ dict ordering)

---

### sorted(struct_instance)

**Raises TypeError**

```ml
struct Point { x: number, y: number }
point = Point{x: 3, y: 4};

sorted(point)  // TypeError: cannot sort Point instance
```

**Workaround:**
```ml
sorted(keys(point))    // Sort field names
sorted(values(point))  // Sort field values
```

---

## Serialization and Deserialization

### JSON Serialization

#### json.stringify(struct_instance) - Extended

**Automatically convert struct to plain object, then to JSON**

```ml
struct Person {
    name: string,
    age: number,
    metadata
}

person = Person{name: "Alice", age: 30, metadata: {role: "admin"}};

json_str = json.stringify(person);
// Returns: '{"name":"Alice","age":30,"metadata":{"role":"admin"}}'
```

**Nested structs:**
```ml
struct Address { street: string, city: string }
struct Person { name: string, address: Address }

addr = Address{street: "Main St", city: "NYC"};
person = Person{name: "Alice", address: addr};

json_str = json.stringify(person);
// Returns: '{"name":"Alice","address":{"street":"Main St","city":"NYC"}}'
```

**Implementation:** Recursively convert structs to dicts before JSON encoding

---

#### to_dict(struct_instance) - New

**Convert struct instance to plain dictionary**

```ml
struct Point { x: number, y: number }

point = Point{x: 3, y: 4};

dict = to_dict(point);  // {x: 3, y: 4}

typeof(dict)            // "object" (plain object)
typeof(point)           // "Point" (struct)
```

**Use case:**
```ml
// Serialize with modifications
dict = to_dict(person);
dict.updated_at = datetime.timestamp();
json_str = json.stringify(dict);
```

---

### JSON Deserialization

#### from_dict(StructType, dict) - New

**Create struct instance from dictionary with type checking**

```ml
struct Person { name: string, age: number }

json_str = '{"name":"Bob","age":25}';
dict = json.parse(json_str);       // Plain object

person = from_dict(Person, dict);  // Person instance
typeof(person)                     // "Person"

// With type checking
bad_dict = {name: "Carol", age: "invalid"};
from_dict(Person, bad_dict);       // TypeError: age must be number
```

**Implementation:**
```python
def from_dict(struct_type, data):
    # Validate all required fields present
    for field in struct_type.fields:
        if field.name not in data:
            if not field.has_default:
                raise TypeError(f"Missing field: {field.name}")

    # Create instance with type checking
    return struct_type(**data)
```

---

#### json.parse_struct(json_str, StructType) - New

**Parse JSON directly into struct instance**

```ml
struct Person { name: string, age: number }

json_str = '{"name":"Diana","age":28}';

person = json.parse_struct(json_str, Person);
typeof(person)  // "Person"
```

**Convenience wrapper:**
```python
def json.parse_struct(json_str, struct_type):
    dict = json.parse(json_str)
    return from_dict(struct_type, dict)
```

---

## Error Messages

### Overview

Clear, actionable error messages are critical for developer experience. This section specifies error message formats and examples for all type-related errors.

### Format Template

```
{ErrorType}: {Primary message}
  at {file}:{line}:{column}

  Expected: {expected}
  Got: {actual}

  {Helpful hint or suggestion}
```

---

### Field Type Errors

**Wrong field type on struct creation:**

```ml
struct Point { x: number, y: number }

point = Point{x: "hello", y: 4};
```

**Error:**
```
TypeError: Field 'x' of Point must be number, got string
  at example.ml:3:17

  Expected: number
  Got: string

  Hint: Ensure field 'x' is a numeric value (int or float)
```

---

### Missing Field Errors

**Missing required field:**

```ml
struct Point { x: number, y: number }

point = Point{x: 3};
```

**Error:**
```
TypeError: Missing required field 'y' for Point
  at example.ml:3:9

  Required fields: x, y
  Provided fields: x

  Hint: Point requires all fields to be specified
```

---

### Method Not Found Errors

**Method doesn't exist on struct:**

```ml
struct Point { x: number, y: number }

point = Point{x: 3, y: 4};
point.invalid_method();
```

**Error:**
```
AttributeError: Point has no method 'invalid_method'
  at example.ml:4:7

  Available methods: distance, move, scale

  Hint: Did you mean 'distance'?
```

---

### Structural Type Mismatch

**Plain object doesn't satisfy struct:**

```ml
struct Point { x: number, y: number }
function (p: Point) distance() { ... }

plain = {a: 1, b: 2};
plain.distance();
```

**Error:**
```
TypeError: Object does not satisfy Point structure
  at example.ml:6:7

  Required fields: x (number), y (number)
  Object has fields: a, b

  Hint: Object is missing required field 'x'
```

**Wrong field types:**

```ml
plain = {x: "hello", y: 4};
plain.distance();
```

**Error:**
```
TypeError: Object does not satisfy Point structure
  at example.ml:6:7

  Required: x must be number
  Got: x is string

  Hint: Field 'x' has wrong type
```

---

### Ambiguous Method Call

**Multiple structs match plain object:**

```ml
struct Point { x: number, y: number }
struct Vector { x: number, y: number }

function (p: Point) magnitude() { ... }
function (v: Vector) magnitude() { ... }

plain = {x: 3, y: 4};
plain.magnitude();
```

**Error:**
```
TypeError: Ambiguous method call: 'magnitude'
  at example.ml:9:7

  Method 'magnitude' is defined for:
    - Point (at line 5)
    - Vector (at line 6)

  Hint: Use explicit type call: Point.magnitude(obj) or Vector.magnitude(obj)
```

---

### Return Type Errors

**Function returns wrong type:**

```ml
function get_name(): string {
    return 42;
}
```

**Error:**
```
TypeError: get_name() must return string, got number
  at example.ml:2:12

  Expected: string
  Got: number (value: 42)

  Hint: Ensure return value is a string
```

---

### Parameter Type Errors

**Function called with wrong parameter type:**

```ml
function add(a: number, b: number): number {
    return a + b;
}

add("hello", "world");
```

**Error:**
```
TypeError: Parameter 'a' must be number, got string
  at example.ml:5:5

  Expected: number
  Got: string (value: "hello")

  Hint: add() requires numeric arguments
```

---

## Security Integration

### Overview

Structs must integrate seamlessly with ML's capability-based security model. This section defines how structs interact with the security system and capability enforcement.

### Capability-Aware Structs

**Structs can have fields that require specific capabilities:**

```ml
capability file_ops {
    resource "*.txt";
    allow read;
    allow write;
}

struct FileHandle {
    path: string,
    mode: string
}

function (f: FileHandle) read(): string {
    // Security analyzer checks: requires file_ops capability
    import file;
    return file.read(f.path);  // Capability check happens here
}

function (f: FileHandle) write(content: string) {
    // Security analyzer checks: requires file_ops capability
    import file;
    file.write(f.path, content);
}
```

**Security analysis:**
- Methods are analyzed like regular functions
- Capability requirements propagate from method body
- Call sites are checked for required capabilities

---

### Security Analysis Pass

**Structs go through security analysis:**

1. **Struct Declaration Analysis**
   ```python
   def analyze_struct_declaration(struct: StructDeclaration):
       # Check if struct fields contain sensitive data
       for field in struct.fields:
           if is_sensitive_field_name(field.name):
               warn_sensitive_field(field)
   ```

2. **Method Body Analysis**
   ```python
   def analyze_method(method: MethodDefinition):
       # Analyze method body for dangerous operations
       required_capabilities = analyze_statements(method.body)

       # Store capability requirements
       method.required_capabilities = required_capabilities
   ```

3. **Method Call Analysis**
   ```python
   def analyze_method_call(call: MethodCall, context: SecurityContext):
       # Get method definition
       method = type_registry.get_method(receiver_type, method_name)

       # Check caller has required capabilities
       for cap in method.required_capabilities:
           if cap not in context.active_capabilities:
               raise SecurityError(f"Method requires capability: {cap}")
   ```

---

### Capability Storage in Structs

**Future enhancement: Store capability tokens in struct fields**

```ml
struct AuthorizedFileHandle {
    path: string,
    capability_token: capability  // Special field type
}

function new_authorized_file(path: string): AuthorizedFileHandle {
    // Check caller has file_ops capability
    // Store capability token in struct
    return AuthorizedFileHandle{
        path: path,
        capability_token: __get_current_capability("file_ops")
    };
}

function (f: AuthorizedFileHandle) read(): string {
    // Use stored capability token
    import file;
    with_capability(f.capability_token) {
        return file.read(f.path);
    }
}
```

**Design decision:** Phase 2 feature (not in MVP)

---

### Security Best Practices

**1. Validate in constructor functions:**
```ml
function new_account(owner: string, initial: number): Account {
    // Validate before creating struct
    if (initial < 0) {
        throw {message: "Invalid initial balance"};
    }

    return Account{
        owner: owner,
        balance: initial
    };
}
```

**2. Use methods for sensitive operations:**
```ml
struct BankAccount { balance: number }

// Good: Method enforces business logic
function (acc: BankAccount) withdraw(amount: number) {
    if (amount > acc.balance) {
        throw {message: "Insufficient funds"};
    }
    acc.balance = acc.balance - amount;
}

// Bad: Direct field access bypasses validation
// acc.balance = acc.balance - 1000000;  // No check!
```

**3. Mark sensitive structs in documentation:**
```ml
// @security: Requires file_ops capability for methods
struct FileHandle {
    path: string
}
```

---

## Implementation Architecture

### Phase 1: Parser & AST Extensions

**New AST Nodes:**

```python
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
class MethodDefinition:
    receiver_name: str
    receiver_type: str
    method_name: str
    parameters: List[Parameter]
    body: List[Statement]
    return_type: Optional[str]      # NEW
    location: Location

@dataclass
class StructLiteral:
    struct_type: str
    properties: Dict[str, Expression]
    location: Location

@dataclass
class FunctionDefinition:
    name: str
    parameters: List[Parameter]
    body: List[Statement]
    return_type: Optional[str]      # NEW
    receiver: Optional[Receiver]    # NEW
    location: Location

@dataclass
class ArrowFunction:
    parameters: List[Parameter]
    body: Union[Expression, List[Statement]]
    return_type: Optional[str]      # NEW
    location: Location
```

**Transformer Updates:**

```python
class MLTransformer(Transformer):
    def return_type(self, items):
        """Transform return type annotation."""
        return items[0].value

    def function_definition(self, items):
        """Transform function with optional return type."""
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

        # Body
        body = items[idx:]

        if receiver:
            return MethodDefinition(receiver, name, parameters, body, return_type, ...)
        else:
            return FunctionDefinition(name, parameters, body, return_type, None, ...)

    def struct_declaration(self, items):
        """Transform struct declaration."""
        name = items[0].value
        fields = items[1:]
        return StructDeclaration(name, fields, self.get_location())

    def struct_literal(self, items):
        """Transform struct literal."""
        type_name = items[0].value
        properties = {}
        for prop in items[1:]:
            properties[prop.name] = prop.value
        return StructLiteral(type_name, properties, self.get_location())
```

---

### Phase 2: Type Registry

**Global Type System:**

```python
class TypeRegistry:
    """Global registry of struct types and methods"""

    def __init__(self):
        self.structs: Dict[str, StructDeclaration] = {}
        self.methods: Dict[Tuple[str, str], MethodDefinition] = {}

    def register_struct(self, struct: StructDeclaration):
        """Register a struct type"""
        if struct.name in self.structs:
            raise ValueError(f"Struct '{struct.name}' already defined")
        self.structs[struct.name] = struct

    def register_method(self, method: MethodDefinition):
        """Register a method for a type"""
        key = (method.receiver_type, method.method_name)
        if key in self.methods:
            raise ValueError(
                f"Method '{method.method_name}' already defined for '{method.receiver_type}'"
            )
        self.methods[key] = method

    def get_method(self, type_name: str, method_name: str) -> Optional[MethodDefinition]:
        """Look up a method for a type"""
        return self.methods.get((type_name, method_name))

    def get_struct(self, type_name: str) -> Optional[StructDeclaration]:
        """Look up a struct definition"""
        return self.structs.get(type_name)
```

**Forward Reference Handling for Recursive Types:**

```python
class TypeRegistry:
    """Enhanced registry with forward reference support"""

    def __init__(self):
        self.structs: Dict[str, StructDeclaration] = {}
        self.methods: Dict[Tuple[str, str], MethodDefinition] = {}
        self._pending_validation: List[StructDeclaration] = []
        self.builtin_types = {'number', 'string', 'boolean', 'array', 'object', 'any', 'void'}

    def register_struct(self, struct: StructDeclaration):
        """Register struct - allow forward references"""
        if struct.name in self.structs:
            raise ValueError(f"Struct '{struct.name}' already defined")

        # Register immediately - don't validate field types yet
        # This allows recursive types: struct Node { next: Node }
        self.structs[struct.name] = struct
        self._pending_validation.append(struct)

    def validate_all_types(self):
        """Validate all field types after all structs registered"""
        for struct in self._pending_validation:
            for field in struct.fields:
                if field.type_annotation:
                    # Allow builtin types and registered struct types
                    if field.type_annotation not in self.builtin_types:
                        if field.type_annotation not in self.structs:
                            raise TypeError(
                                f"Unknown type '{field.type_annotation}' "
                                f"in struct '{struct.name}', field '{field.name}'"
                            )

        self._pending_validation.clear()
```

**Structural Type Checking with Cycle Detection:**

```python
def _check_structural_type(obj, struct_def, visited=None):
    """
    Check if obj satisfies struct structurally (with cycle detection).

    Args:
        obj: Object to check
        struct_def: StructDeclaration to check against
        visited: Set of visited object IDs (for cycle detection)

    Returns:
        True if obj satisfies struct, raises TypeError otherwise
    """
    if visited is None:
        visited = set()

    # Cycle detection - if we've seen this object before, assume valid
    # This prevents infinite recursion with circular references
    obj_id = id(obj)
    if obj_id in visited:
        return True  # Already validated in this path

    visited.add(obj_id)

    try:
        for field in struct_def.fields:
            # Check field exists
            if not hasattr(obj, field.name):
                raise TypeError(f"Missing required field: {field.name}")

            # Check field type (if specified)
            if field.type_annotation:
                value = getattr(obj, field.name)

                # null/None always valid (for optional fields with defaults)
                if value is not None:
                    if not _matches_type(value, field.type_annotation, visited):
                        raise TypeError(
                            f"Field {field.name} must be {field.type_annotation}, "
                            f"got {type(value).__name__}"
                        )

        return True

    finally:
        # Backtrack - remove from visited set for other paths
        visited.remove(obj_id)


def _matches_type(value, type_name, visited=None):
    """
    Check if value matches type (recursively for struct types).

    Args:
        value: Value to check
        type_name: Type name to check against
        visited: Set of visited object IDs (for cycle detection)

    Returns:
        True if value matches type
    """
    # Builtin type checks
    type_map = {
        'number': (int, float),
        'string': str,
        'boolean': bool,
        'array': list,
        'object': dict,
        'any': object  # Always matches
    }

    if type_name in type_map:
        return isinstance(value, type_map[type_name])

    # Struct type - check structurally
    from mlpy.type_registry import type_registry
    struct_def = type_registry.get_struct(type_name)
    if struct_def:
        try:
            _check_structural_type(value, struct_def, visited)
            return True
        except TypeError:
            return False

    # Unknown type
    return False
```

**Usage in Transpiler:**

```python
class Transpiler:
    def __init__(self):
        self.type_registry = TypeRegistry()

    def transpile(self, source: str) -> TranspileResult:
        # Parse
        ast = self.parser.parse(source)

        # First pass: Register all structs (allows forward references)
        for node in ast:
            if isinstance(node, StructDeclaration):
                self.type_registry.register_struct(node)

        # Validate all struct field types (after all structs registered)
        # This enables recursive types: struct Node { next: Node }
        self.type_registry.validate_all_types()

        # Second pass: Register all methods
        for node in ast:
            if isinstance(node, MethodDefinition):
                self.type_registry.register_method(node)

        # Third pass: Generate code
        python_code = self.code_generator.generate(ast, self.type_registry)

        return TranspileResult(python_code, ...)
```

---

### Phase 3: Code Generation

**Struct to Python Class:**

```python
class PythonGenerator:
    def generate_struct(self, struct: StructDeclaration) -> str:
        """Generate Python dataclass from ML struct"""

        # Build fields with type hints
        fields = []
        for field in struct.fields:
            if field.type_annotation:
                type_hint = self.map_type(field.type_annotation)
            else:
                type_hint = "Any"
            fields.append(f"    {field.name}: {type_hint}")

        # Generate dataclass
        code = f"""
@dataclass
class {struct.name}:
{chr(10).join(fields)}

    def __post_init__(self):
        # Runtime type checking for typed fields
"""
        # Add type checks for typed fields
        for field in struct.fields:
            if field.type_annotation:
                code += f"        _check_type(self.{field.name}, '{field.type_annotation}', '{struct.name}.{field.name}')\n"

        return code

    def generate_method(self, method: MethodDefinition) -> str:
        """Generate Python instance method"""

        params = [method.receiver_name] + [p.name for p in method.parameters]
        param_checks = []

        # Parameter type checks
        for param in method.parameters:
            if param.type_annotation:
                param_checks.append(
                    f"    _check_type({param.name}, '{param.type_annotation}', 'parameter {param.name}')"
                )

        # Generate method body
        body = self.generate_statements(method.body)

        # Add return type check wrapper if needed
        if method.return_type:
            body = f"""
    # Receiver structural type check
    _check_structural_type({method.receiver_name}, '{method.receiver_type}')
{chr(10).join(param_checks)}

    # Original method body
{self.indent(body)}

    # Return type check (wrapped)
    return _check_type(__result__, '{method.return_type}', '{method.method_name} return')
"""
        else:
            body = f"""
    # Receiver structural type check
    _check_structural_type({method.receiver_name}, '{method.receiver_type}')
{chr(10).join(param_checks)}

{self.indent(body)}
"""

        return f"""
def {method.receiver_type}_{method.method_name}(self, {', '.join(params[1:])}):
{body}

{method.receiver_type}.{method.method_name} = {method.receiver_type}_{method.method_name}
"""

    def map_type(self, ml_type: str) -> str:
        """Map ML type to Python type hint"""
        type_map = {
            'number': 'Union[int, float]',
            'string': 'str',
            'boolean': 'bool',
            'array': 'list',
            'object': 'dict',
            'any': 'Any'
        }
        return type_map.get(ml_type, ml_type)
```

---

## Code Examples

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
    metadata            // No type - dynamic
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

// Works with struct instances and plain objects
data1 = DataPoint{timestamp: 1699200000, value: 42, metadata: {}};
data2 = {timestamp: 1699200001, value: 43, metadata: {}};  // Plain object

all_data = [data1, data2];
formatted = process_data(all_data);
```

### Example 3: Structural Interface Pattern

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
custom = {area: fn() => 100};  // Plain object with area method

print_area(circle);  // ✅ Works
print_area(rect);    // ✅ Works
print_area(custom);  // ✅ Works (duck typing)
```

### Example 4: Gradual Migration Path

```ml
// Phase 0: Original untyped code
function calculate_distance_v0(p1, p2) {
    dx = p2.x - p1.x;
    dy = p2.y - p1.y;
    import math;
    return math.sqrt(dx * dx + dy * dy);
}

// Phase 1: Add struct definition
struct Point {
    x: number,
    y: number
}

// Phase 2: Add parameter types
function calculate_distance_v2(p1: Point, p2: Point) {
    dx = p2.x - p1.x;
    dy = p2.y - p1.y;
    import math;
    return math.sqrt(dx * dx + dy * dy);
}

// Phase 3: Add return type
function calculate_distance_v3(p1: Point, p2: Point): number {
    dx = p2.x - p1.x;
    dy = p2.y - p1.y;
    import math;
    return math.sqrt(dx * dx + dy * dy);
}

// Phase 4: Convert to method
function (p: Point) distance_to(other: Point): number {
    dx = other.x - p.x;
    dy = other.y - p.y;
    import math;
    return math.sqrt(dx * dx + dy * dy);
}
```

**See `type-hints-examples.ml` for 400+ lines of comprehensive examples.**

---

### Example 5: Recursive Data Structures

```ml
// Linked List with methods
struct ListNode {
    data: number,
    next: ListNode = null
}

function (n: ListNode) append(value: number) {
    if (n.next == null) {
        n.next = ListNode{data: value, next: null};
    } else {
        n.next.append(value);  // Recursive call
    }
}

function (n: ListNode) length(): number {
    if (n.next == null) {
        return 1;
    }
    return 1 + n.next.length();  // Recursive
}

function (n: ListNode) to_array(): array {
    result = [n.data];
    if (n.next != null) {
        result = result + n.next.to_array();
    }
    return result;
}

// Usage
head = ListNode{data: 1, next: null};
head.append(2);
head.append(3);
head.append(4);
print("Length: " + str(head.length()));     // 4
print("Values: " + str(head.to_array()));   // [1, 2, 3, 4]

// Binary Search Tree
struct TreeNode {
    value: number,
    left: TreeNode = null,
    right: TreeNode = null
}

function (t: TreeNode) insert(value: number) {
    if (value < t.value) {
        if (t.left == null) {
            t.left = TreeNode{value: value, left: null, right: null};
        } else {
            t.left.insert(value);  // Recursive
        }
    } else {
        if (t.right == null) {
            t.right = TreeNode{value: value, left: null, right: null};
        } else {
            t.right.insert(value);  // Recursive
        }
    }
}

function (t: TreeNode) contains(value: number): boolean {
    if (t.value == value) {
        return true;
    }
    if (value < t.value) {
        if (t.left == null) {
            return false;
        }
        return t.left.contains(value);
    } else {
        if (t.right == null) {
            return false;
        }
        return t.right.contains(value);
    }
}

function (t: TreeNode) inorder(): array {
    result = [];
    if (t.left != null) {
        result = result + t.left.inorder();
    }
    result = result + [t.value];
    if (t.right != null) {
        result = result + t.right.inorder();
    }
    return result;
}

function (t: TreeNode) height(): number {
    left_height = 0;
    right_height = 0;

    if (t.left != null) {
        left_height = t.left.height();
    }
    if (t.right != null) {
        right_height = t.right.height();
    }

    import math;
    return 1 + math.max(left_height, right_height);
}

// Build and query tree
root = TreeNode{value: 10, left: null, right: null};
root.insert(5);
root.insert(15);
root.insert(3);
root.insert(7);
root.insert(12);
root.insert(20);

print("Contains 7: " + str(root.contains(7)));      // true
print("Contains 99: " + str(root.contains(99)));    // false
print("Inorder: " + str(root.inorder()));           // [3, 5, 7, 10, 12, 15, 20]
print("Height: " + str(root.height()));             // 3

// Graph Node with circular references
struct GraphNode {
    id: number,
    neighbors: array  // Array of GraphNode
}

function (g: GraphNode) add_neighbor(neighbor: GraphNode) {
    g.neighbors = g.neighbors + [neighbor];
}

function (g: GraphNode) find_path(target_id: number, visited: array): array {
    // Check if already visited (cycle detection)
    for (v in visited) {
        if (v == g.id) {
            return null;  // Cycle - no path
        }
    }

    // Found target
    if (g.id == target_id) {
        return [g.id];
    }

    // Mark as visited
    new_visited = visited + [g.id];

    // Search neighbors
    for (neighbor in g.neighbors) {
        path = neighbor.find_path(target_id, new_visited);
        if (path != null) {
            return [g.id] + path;
        }
    }

    return null;  // No path found
}

// Build graph: 1 -> 2 -> 3
//              |         ^
//              v         |
//              4 --------+
node1 = GraphNode{id: 1, neighbors: []};
node2 = GraphNode{id: 2, neighbors: []};
node3 = GraphNode{id: 3, neighbors: []};
node4 = GraphNode{id: 4, neighbors: []};

node1.add_neighbor(node2);
node1.add_neighbor(node4);
node2.add_neighbor(node3);
node4.add_neighbor(node3);

path = node1.find_path(3, []);
print("Path from 1 to 3: " + str(path));  // [1, 2, 3] or [1, 4, 3]
```

---

## Implementation Roadmap

### Phase 1: Grammar & Parser (4-5 days) **UPDATED**

**Tasks:**
1. Add `struct` keyword to lexer
2. Extend grammar rules:
   - Add `return_type` rule
   - Update `function_definition` (add receiver and return type)
   - Update `arrow_function` (add return type)
   - Add `struct_declaration` rule (with default values)
   - Add `struct_literal` rule
3. Create new AST nodes
4. Update transformer methods
5. **NEW:** Add default field value syntax support
6. Write 30+ parser unit tests

**Deliverables:**
- Updated `ml.lark` grammar file
- New AST node classes in `ast_nodes.py`
- Updated `MLTransformer` class
- 30+ parser tests passing

**Success Criteria:**
- All new syntax parses correctly
- AST nodes have proper structure
- All existing 80+ test files still parse (100% backward compatibility)

---

### Phase 2: Type Registry & Struct Identity (4-5 days) **UPDATED**

**Tasks:**
1. Implement `TypeRegistry` class
2. Implement struct identity checking:
   - Struct instance tagging (type metadata)
   - Required field name validation
   - Field sealing enforcement
   - NO type validation (types are hints only)
3. Implement method dispatch algorithm (struct identity check only)
4. **NEW:** Implement introspection built-ins:
   - `typeof(value)` (extended for structs)
   - `fields(StructType)`
   - `copy(obj)`
   - `deepcopy(obj)`
5. Write 25+ struct identity tests

**Deliverables:**
- `type_registry.py` module
- Struct identity helper module
- Integration with Transpiler class
- 25+ struct identity tests passing

**Success Criteria:**
- Structs can be registered and retrieved
- Methods can be looked up by (type, name)
- Duplicate definitions are caught
- Struct identity checks work correctly (NOT type checking)

---

### Phase 3: Code Generation (5-6 days) **UPDATED**

**Tasks:**
1. Generate Python dataclasses from structs (with default values and type hints)
2. Generate instance methods with struct identity metadata
3. Handle struct literals (type-tagged objects)
4. Add struct identity tagging to generated code
5. Add field sealing to generated code
6. **NEW:** Integrate built-in function extensions:
   - `len()`, `str()`, `print()` for structs
   - `keys()`, `values()` for structs
   - Equality operators (`==`, `!=`)
   - JSON serialization (`json.stringify()`)
7. **NEW:** Implement serialization built-ins:
   - `to_dict(struct)`
   - `from_dict(Type, dict)`
   - `json.parse_struct(json_str, Type)`
8. Update existing code generator helpers
9. Write 40+ code generation unit tests

**Deliverables:**
- Updated `python_generator.py`
- Complete transpilation pipeline working
- Struct identity integration
- 40+ codegen tests passing

**Success Criteria:**
- Structs transpile to valid Python dataclasses with type hints
- Methods transpile to instance methods
- Struct literals work correctly
- Generated code runs successfully
- Struct identity checks execute at runtime (NOT type checks)

---

### Phase 4: Integration & Testing (3-5 days) **UPDATED**

**Tasks:**
1. Write 30+ integration tests (includes new built-ins)
2. Run all existing tests (backward compatibility)
3. Performance benchmarking
4. **NEW:** Test error messages for clarity (struct identity errors)
5. **NEW:** Security integration validation
6. Update documentation:
   - Language reference (with all new built-ins)
   - Tutorial with examples emphasizing type hints
   - Developer guide
   - Error message documentation
7. Create example programs showing type hints as documentation
8. Security analysis integration

**Deliverables:**
- 30+ integration test programs
- Performance benchmarks
- Updated language documentation
- Example programs
- All existing tests passing

**Success Criteria:**
- All integration tests pass
- 100% backward compatibility (existing tests pass)
- <5% performance overhead for typed code
- Documentation is comprehensive
- Examples are clear and educational

---

### Total Timeline: 16-21 days **UPDATED**

**Original Estimate:** 15-19 days
**Previous Estimate:** 19-24 days (with runtime type checking)
**New Estimate:** 16-21 days (-3 days from type hints model)

**Breakdown by Phase:**

| Phase | Original | With Type Checking | Type Hints Only | Delta | Reason |
|-------|----------|-------------------|-----------------|-------|--------|
| Phase 1: Grammar & Parser | 3-4 days | 4-5 days | 4-5 days | +1 day | Default field values |
| Phase 2: Type Registry | 4-5 days | 6-7 days | 4-5 days | ±0 days | Simplified: no type validation, only struct identity |
| Phase 3: Code Generation | 5-6 days | 6-7 days | 5-6 days | ±0 days | Simplified: no type checking code generation |
| Phase 4: Testing & Docs | 3-4 days | 3-5 days | 3-5 days | +1 day | More tests, error messages |
| **Total** | **15-19 days** | **19-24 days** | **16-21 days** | **+1-2 days** | **Built-ins + simplified checking** |

**Critical Path:**
1. Grammar changes (prerequisite for everything)
2. Type registry + introspection built-ins (prerequisite for code generation)
3. Code generation + built-in integration (prerequisite for testing)
4. Integration testing + documentation (final validation)

**Risk Mitigation:**
- Start with minimal feature set
- Incremental testing throughout
- Maintain backward compatibility at all phases
- Regular progress checkpoints
- **NEW:** Prioritize Tier 1 built-ins (typeof, fields, copy, deepcopy) in Phase 2

---

## Testing Strategy

### Unit Tests

**Parser Tests (30+ tests):**
- Struct declarations (fully typed, partially typed, untyped)
- Method definitions with receivers
- Return type annotations (functions and arrows)
- Struct literals
- Backward compatibility (existing syntax)

**Type Registry Tests (25+ tests):**
- Struct registration
- Method registration
- Type lookups
- Duplicate detection
- Structural type matching

**Code Generation Tests (40+ tests):**
- Struct to dataclass
- Method generation
- Type check insertion
- Struct literal handling
- Return type checks

### Integration Tests (30+ tests)

**Complete Programs:**
- Banking system (fully typed)
- Data processing (mixed typing)
- Shape system (structural interfaces)
- Gradual migration examples
- Plain object compatibility
- Error handling scenarios

### Backward Compatibility Tests

**All 80+ existing ML test files must:**
- Parse successfully
- Transpile successfully
- Execute with same results
- Show no performance degradation

### Performance Benchmarks

**Measure:**
- Parse time (structs vs plain objects)
- Transpile time (typed vs untyped)
- Runtime overhead (type checks)
- Memory usage (dataclasses vs dicts)

**Targets:**
- <5% parse/transpile overhead
- <5% runtime overhead for typed code
- 0% overhead for untyped code

---

## Success Metrics

### Must Achieve

- ✅ **100% backward compatibility** - All existing tests pass
- ✅ **95%+ test coverage** - New features thoroughly tested
- ✅ **<2% runtime overhead** - Struct identity checking is minimal
- ✅ **Zero type checking overhead** - Types are hints only (no runtime validation)
- ✅ **Zero security vulnerabilities** - No new attack vectors
- ✅ **All Tier 1 built-ins implemented** - typeof, fields, copy, deepcopy **NEW**
- ✅ **Method dispatch algorithm working** - Struct identity dispatch **NEW**

### Quality Goals

- ✅ **Clear error messages** - Struct identity errors easy to understand
- ✅ **IDE autocomplete** - Works with struct type hints
- ✅ **Comprehensive docs** - Language reference updated (including all built-ins, type hints explanation)
- ✅ **Example programs** - Demonstrate all features with type hints as documentation
- ✅ **Positive feedback** - Developer experience improved
- ✅ **Built-in integration** - len, str, keys, values work intuitively **NEW**
- ✅ **JSON serialization** - Struct serialization works out of the box **NEW**
- ✅ **Type hints for documentation** - Clear examples showing types as IDE hints **NEW**

### Monitoring

**Track throughout implementation:**
- Test pass rate
- Performance benchmarks
- Code coverage metrics
- Documentation completeness
- Developer feedback

---

## Appendix: Design Decisions Summary

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| **Type Hints** | Optional everywhere | Gradual typing, backward compatible |
| **Type Checking** | Runtime only | ML is dynamic, no compile-time infrastructure |
| **Type System** | Pure Structural (duck typing) | Compatible with plain objects, sealed structs, ML philosophy **NEW** |
| **Return Types** | Add to grammar | Consistency, completeness |
| **Default Values** | Support in grammar | Common use case, convenience **NEW** |
| **Introspection** | 4 essential built-ins | typeof, fields, copy, deepcopy **NEW** |
| **Built-in Integration** | Extend existing built-ins | len, str, keys work with structs **NEW** |
| **Method Dispatch** | Strict (struct instances only) | Type safety, no plain object methods **NEW** |
| **Serialization** | JSON integration | to_dict, from_dict built-ins **NEW** |
| **Inheritance** | None | Simplicity, composition over inheritance |
| **Interfaces** | Implicit/structural (Phase 2) | Go-style, no explicit implements |
| **Migration** | Gradual, optional | No forced changes, incremental adoption |
| **Performance** | <5% overhead for typed | Acceptable cost for safety |
| **Compatibility** | 100% backward | Existing code must work unchanged |

---

## Next Steps

1. ✅ **Review and approve** this updated implementation guide
2. 🔜 **Begin Phase 1** - Grammar extensions with default values (4-5 days)
3. 📋 **Phase 2** - Type registry + introspection built-ins (6-7 days)
4. 📋 **Phase 3** - Code generation + built-in integration (6-7 days)
5. 📋 **Phase 4** - Integration, testing & documentation (3-5 days)
6. 📋 **Documentation** - Update all docs (language ref, built-ins, examples)
7. 🎉 **Release** - Production-ready OOP for ML with complete feature set

**Status:** Ready for implementation (Updated with critical features)

**Estimated Completion:** 19-24 days from start (updated from 15-19 days)

---

*For additional examples, see `type-hints-examples.ml` (400+ lines of code)*
