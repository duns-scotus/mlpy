# Golang-Style Lightweight OOP for ML Language

**Status:** Draft Proposal
**Author:** Claude Code
**Date:** November 4, 2025
**Sprint:** Language Enhancement - Phase 1

---

## Executive Summary

This proposal introduces minimal, lightweight OOP features to ML inspired by Go's pragmatic approach: **structs, methods, and implicit interfaces**. The design philosophy prioritizes simplicity, composition over inheritance, and seamless integration with ML's existing functional programming features and capability-based security model.

**Key Principles:**
- ✅ **No Classes or Inheritance** - Keep complexity low
- ✅ **Composition Over Inheritance** - Struct embedding for code reuse
- ✅ **Explicit Over Implicit** - No hidden `this` binding
- ✅ **Duck Typing** - Interfaces satisfied implicitly by methods
- ✅ **Security-First** - Full integration with capability system
- ✅ **Backward Compatible** - Zero breaking changes to existing ML code

---

## Table of Contents

1. [Motivation & Use Cases](#motivation--use-cases)
2. [Language Features](#language-features)
3. [Grammar Extensions](#grammar-extensions)
4. [Implementation Architecture](#implementation-architecture)
5. [Security Integration](#security-integration)
6. [Code Examples](#code-examples)
7. [Viability Assessment](#viability-assessment)
8. [Cost-Benefit Analysis](#cost-benefit-analysis)
9. [Implementation Roadmap](#implementation-roadmap)
10. [Alternatives Considered](#alternatives-considered)

---

## Motivation & Use Cases

### Current State: Functional Programming with Objects

ML currently supports:
```ml
// Objects as dictionaries with methods via closures
function create_person(name, age) {
    person_name = name;
    person_age = age;

    function get_name() {
        return person_name;
    }

    function have_birthday() {
        nonlocal person_age;
        person_age = person_age + 1;
        return person_age;
    }

    return {
        name: get_name,
        age: person_age,
        birthday: have_birthday
    };
}

person = create_person("Alice", 25);
person.birthday();
```

**Problems with Current Approach:**
1. ❌ **Verbose** - Requires explicit closure construction for every "object"
2. ❌ **No Type Identity** - All objects are just dictionaries
3. ❌ **Poor Tooling** - IDEs can't provide meaningful autocomplete
4. ❌ **Runtime Errors** - Typos in property names only caught at runtime
5. ❌ **Code Duplication** - No clean way to share method implementations
6. ❌ **Unclear Intent** - Hard to distinguish data structures from behavior

### Proposed Solution: Lightweight Structs + Methods

```ml
// Define a struct type
struct Person {
    name: string,
    age: number
}

// Constructor function (optional convention)
function new_person(name, age) {
    return Person{name: name, age: age};
}

// Method definition - explicit receiver
function (p: Person) get_name() {
    return p.name;
}

function (p: Person) have_birthday() {
    p.age = p.age + 1;
    return p.age;
}

// Usage - clear and concise
alice = new_person("Alice", 25);
alice.have_birthday();
print(alice.name);  // "Alice"
```

**Benefits:**
- ✅ **Clear Intent** - Structs explicitly declare data shape
- ✅ **Type Safety** - Catch property typos at parse/transpile time
- ✅ **Better Tooling** - IDEs can autocomplete struct fields
- ✅ **Less Boilerplate** - No need for manual closure construction
- ✅ **Familiar Syntax** - Looks like Go, TypeScript, Rust
- ✅ **Performance** - Transpiles to efficient Python classes

---

## Language Features

### Feature 1: Struct Definitions

**Syntax:**
```ml
struct TypeName {
    field1: type,
    field2: type,
    ...
}
```

**Semantics:**
- Structs are named types with fixed fields
- Fields have optional type annotations (for documentation/future type checking)
- Structs are immutable by default unless fields are reassigned
- Transpiles to Python `dataclass` or simple class

**Example:**
```ml
struct Point {
    x: number,
    y: number
}

struct Rectangle {
    top_left: Point,
    width: number,
    height: number
}

// Struct literal - field names required
origin = Point{x: 0, y: 0};
rect = Rectangle{
    top_left: origin,
    width: 100,
    height: 50
};

// Field access
print(rect.top_left.x);  // 0
print(rect.width);        // 100

// Field mutation
rect.width = 200;
print(rect.width);        // 200
```

**Type Annotations (Optional):**
- `number` - numeric types (int/float)
- `string` - text
- `boolean` - true/false
- `array` - array type
- `any` - any type (default if not specified)
- Custom struct types (e.g., `Point`, `Rectangle`)

---

### Feature 2: Methods with Explicit Receivers

**Syntax:**
```ml
function (receiver: Type) method_name(param1, param2, ...) {
    // method body
}
```

**Semantics:**
- Methods are functions with a named receiver parameter
- Receiver is **explicit** (like Python's `self`, Go's receiver)
- Methods are called using dot notation: `instance.method(args)`
- Transpiles to Python instance methods

**Example:**
```ml
struct Vector {
    x: number,
    y: number
}

// Method definitions
function (v: Vector) magnitude() {
    import math;
    return math.sqrt(v.x * v.x + v.y * v.y);
}

function (v: Vector) add(other: Vector) {
    return Vector{
        x: v.x + other.x,
        y: v.y + other.y
    };
}

function (v: Vector) scale(factor: number) {
    v.x = v.x * factor;
    v.y = v.y * factor;
}

// Usage
v1 = Vector{x: 3, y: 4};
print(v1.magnitude());  // 5.0

v2 = Vector{x: 1, y: 2};
v3 = v1.add(v2);
print(v3.x);  // 4

v1.scale(2);
print(v1.x);  // 6
```

**Method Resolution:**
- Methods are looked up in a method registry by (Type, MethodName)
- No method hiding or overriding (no inheritance)
- Clear error if method doesn't exist on type

---

### Feature 3: Implicit Interfaces (Duck Typing)

**Syntax:**
```ml
interface InterfaceName {
    method1(params...): return_type;
    method2(params...): return_type;
    ...
}
```

**Semantics:**
- Interfaces define a set of method signatures
- Types **implicitly** satisfy interfaces if they have matching methods
- No explicit `implements` keyword (Go-style)
- Interfaces used for type checking and documentation
- Runtime uses duck typing (Python style)

**Example:**
```ml
// Interface definition
interface Drawable {
    draw(): string;
    area(): number;
}

// Circle struct
struct Circle {
    radius: number
}

function (c: Circle) draw() {
    return "Drawing circle with radius " + str(c.radius);
}

function (c: Circle) area() {
    return 3.14159 * c.radius * c.radius;
}

// Rectangle struct
struct Rectangle {
    width: number,
    height: number
}

function (r: Rectangle) draw() {
    return "Drawing rectangle " + str(r.width) + "x" + str(r.height);
}

function (r: Rectangle) area() {
    return r.width * r.height;
}

// Function accepting interface (duck typing)
function render_shape(shape: Drawable) {
    print(shape.draw());
    print("Area: " + str(shape.area()));
}

// Both Circle and Rectangle satisfy Drawable interface
circle = Circle{radius: 5};
rect = Rectangle{width: 10, height: 20};

render_shape(circle);  // Works!
render_shape(rect);    // Works!
```

**Interface Checking:**
- **Compile-time (optional):** Type checker verifies interface satisfaction
- **Runtime:** Duck typing - call method and catch errors if missing
- Interfaces are purely for documentation/tooling initially

---

### Feature 4: Struct Embedding (Composition)

**Syntax:**
```ml
struct DerivedType {
    BaseType,           // Embedded struct (anonymous field)
    extra_field: type,
    ...
}
```

**Semantics:**
- Embedded struct fields are "promoted" to parent struct
- Can access embedded fields directly on parent
- No method inheritance - must explicitly forward or re-implement
- Composition over inheritance

**Example:**
```ml
struct Engine {
    horsepower: number,
    fuel_type: string
}

function (e: Engine) start() {
    print("Engine starting... " + str(e.horsepower) + " HP");
}

function (e: Engine) stop() {
    print("Engine stopping...");
}

struct Car {
    Engine,              // Embedded Engine
    make: string,
    model: string
}

// Car automatically gets Engine fields
honda = Car{
    Engine: Engine{horsepower: 200, fuel_type: "gasoline"},
    make: "Honda",
    model: "Civic"
};

// Access embedded fields directly
print(honda.horsepower);    // 200 (promoted from Engine)
print(honda.fuel_type);     // "gasoline"
print(honda.make);          // "Honda"

// Access embedded struct explicitly if needed
print(honda.Engine.horsepower);  // 200

// Methods on embedded type can be called
honda.Engine.start();  // "Engine starting... 200 HP"
```

**Field Promotion Rules:**
- Embedded struct fields are accessible via parent
- Name conflicts: explicit access required (e.g., `honda.Engine.field`)
- Methods are NOT automatically promoted (explicit forwarding needed)

---

### Feature 5: Constructor Functions (Convention)

**Syntax:**
```ml
function new_TypeName(params...) {
    // validation and initialization
    return TypeName{field1: value1, field2: value2};
}
```

**Semantics:**
- Constructors are just regular functions (by convention start with `new_`)
- Allow validation, default values, computed fields
- Can enforce invariants before creating struct

**Example:**
```ml
struct BankAccount {
    account_number: string,
    balance: number,
    owner: string
}

function new_bank_account(owner: string, initial_deposit: number) {
    // Validation
    if (initial_deposit < 0) {
        throw {message: "Initial deposit must be non-negative"};
    }

    // Generate account number
    account_num = "ACC" + str(random.randint(10000, 99999));

    return BankAccount{
        account_number: account_num,
        balance: initial_deposit,
        owner: owner
    };
}

function (acc: BankAccount) deposit(amount: number) {
    if (amount <= 0) {
        throw {message: "Deposit amount must be positive"};
    }
    acc.balance = acc.balance + amount;
}

function (acc: BankAccount) withdraw(amount: number) {
    if (amount <= 0) {
        throw {message: "Withdrawal amount must be positive"};
    }
    if (amount > acc.balance) {
        throw {message: "Insufficient funds"};
    }
    acc.balance = acc.balance - amount;
}

// Usage
account = new_bank_account("Alice", 1000);
account.deposit(500);
account.withdraw(200);
print(account.balance);  // 1300
```

---

## Grammar Extensions

### Struct Declaration Grammar

```lark
// Add to statement rules
?statement: ...
          | struct_declaration
          | interface_declaration

// Struct definition
struct_declaration: "struct" IDENTIFIER "{" struct_field* "}"
struct_field: IDENTIFIER (":" type_annotation)? ("," | ";")

// Method definition (function with receiver)
function_definition: "function" method_receiver? IDENTIFIER "(" parameter_list? ")" "{" statement* "}"
method_receiver: "(" IDENTIFIER ":" IDENTIFIER ")"

// Struct literal (already supported as object_literal, add type prefix)
struct_literal: IDENTIFIER "{" (struct_property ("," struct_property)*)? "}"
struct_property: IDENTIFIER ":" expression

// Interface definition (optional, for type checking/docs)
interface_declaration: "interface" IDENTIFIER "{" interface_method* "}"
interface_method: IDENTIFIER "(" parameter_types? ")" (":" type_annotation)? ";"
parameter_types: type_annotation ("," type_annotation)*

// Type annotations (extend existing)
type_annotation: IDENTIFIER                    // Simple type or struct name
               | type_annotation "[]"          // Array type
               | "(" type_annotation ")"       // Grouped type
```

### Grammar Changes Impact

**Minimal Changes:**
1. Add `struct` keyword (must come before IDENTIFIER in tokens)
2. Add `interface` keyword (optional, Phase 2)
3. Extend `function_definition` to support receiver parameter
4. Add `struct_literal` rule (similar to object_literal with type prefix)

**No Breaking Changes:**
- Existing code continues to work
- New keywords are context-specific
- Backward compatible with all existing ML programs

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
    location: Location

@dataclass
class StructLiteral:
    struct_type: str
    properties: Dict[str, Expression]
    location: Location

@dataclass
class InterfaceDeclaration:  # Phase 2
    name: str
    methods: List[InterfaceMethod]
    location: Location
```

**Transformer Updates:**

```python
class MLTransformer(Transformer):
    def struct_declaration(self, items):
        name = items[0].value
        fields = items[1:]
        return StructDeclaration(name, fields, self.get_location())

    def method_receiver(self, items):
        receiver_name = items[0].value
        receiver_type = items[1].value
        return (receiver_name, receiver_type)

    def function_definition(self, items):
        receiver = None
        if isinstance(items[0], tuple):  # Has receiver
            receiver = items[0]
            items = items[1:]

        if receiver:
            return MethodDefinition(
                receiver_name=receiver[0],
                receiver_type=receiver[1],
                method_name=items[0].value,
                parameters=items[1] if len(items) > 1 else [],
                body=items[2] if len(items) > 2 else [],
                location=self.get_location()
            )
        else:
            # Existing function_definition logic
            ...
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
        self.interfaces: Dict[str, InterfaceDeclaration] = {}

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
                f"Method '{method.method_name}' already defined for type '{method.receiver_type}'"
            )
        self.methods[key] = method

    def get_method(self, type_name: str, method_name: str) -> Optional[MethodDefinition]:
        """Look up a method for a type"""
        return self.methods.get((type_name, method_name))

    def check_interface_satisfaction(self, type_name: str, interface_name: str) -> bool:
        """Check if type satisfies interface (duck typing)"""
        interface = self.interfaces.get(interface_name)
        if not interface:
            return False

        for method_sig in interface.methods:
            method = self.get_method(type_name, method_sig.name)
            if not method:
                return False
            # TODO: Check parameter/return type compatibility

        return True
```

**Usage in Transpiler:**

```python
class Transpiler:
    def __init__(self):
        self.type_registry = TypeRegistry()

    def transpile(self, source: str) -> TranspileResult:
        # Parse
        ast = self.parser.parse(source)

        # First pass: Register all struct and interface declarations
        for node in ast:
            if isinstance(node, StructDeclaration):
                self.type_registry.register_struct(node)
            elif isinstance(node, InterfaceDeclaration):
                self.type_registry.register_interface(node)

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

        # Option 1: dataclass (cleaner, more Pythonic)
        fields = []
        for field in struct.fields:
            type_hint = self.map_type(field.type_annotation) if field.type_annotation else "Any"
            fields.append(f"    {field.name}: {type_hint}")

        code = f"""
@dataclass
class {struct.name}:
{chr(10).join(fields)}
"""
        return code

        # Option 2: Simple class (more compatible)
        # class Point:
        #     def __init__(self, x, y):
        #         self.x = x
        #         self.y = y

    def generate_method(self, method: MethodDefinition) -> str:
        """Generate Python instance method"""

        # Convert ML method to Python method
        params = [method.receiver_name] + [p.name for p in method.parameters]
        param_str = ", ".join(params)

        body = self.generate_statements(method.body)

        code = f"""
def {method.method_name}(self, {param_str}):
{self.indent(body)}
"""
        return code

    def generate_struct_literal(self, literal: StructLiteral) -> str:
        """Generate struct instantiation"""

        # Point{x: 10, y: 20} => Point(x=10, y=20)
        args = []
        for key, value in literal.properties.items():
            value_code = self.generate_expression(value)
            args.append(f"{key}={value_code}")

        return f"{literal.struct_type}({', '.join(args)})"

    def map_type(self, ml_type: str) -> str:
        """Map ML type annotation to Python type hint"""
        type_map = {
            "number": "Union[int, float]",
            "string": "str",
            "boolean": "bool",
            "array": "list",
            "any": "Any"
        }
        return type_map.get(ml_type, ml_type)  # Custom structs use their name
```

**Example Transpilation:**

ML Code:
```ml
struct Point {
    x: number,
    y: number
}

function (p: Point) distance_from_origin() {
    import math;
    return math.sqrt(p.x * p.x + p.y * p.y);
}

origin = Point{x: 0, y: 0};
point = Point{x: 3, y: 4};
dist = point.distance_from_origin();
```

Generated Python:
```python
from dataclasses import dataclass
from typing import Union, Any
import math

@dataclass
class Point:
    x: Union[int, float]
    y: Union[int, float]

def Point_distance_from_origin(self):
    return math.sqrt(self.x * self.x + self.y * self.y)

# Bind method to class
Point.distance_from_origin = Point_distance_from_origin

origin = Point(x=0, y=0)
point = Point(x=3, y=4)
dist = point.distance_from_origin()
```

---

### Phase 4: Security Integration

**Capability Enforcement:**

Struct operations must respect the capability system:

```python
class SecurityAnalyzer:
    def analyze_struct_literal(self, literal: StructLiteral, capabilities: CapabilityContext):
        """Analyze struct instantiation for security"""

        # Check if struct type requires special capabilities
        struct_def = self.type_registry.structs.get(literal.struct_type)
        if not struct_def:
            raise SecurityError(f"Unknown struct type: {literal.struct_type}")

        # Check field initializers for security issues
        for field_name, value_expr in literal.properties.items():
            self.analyze_expression(value_expr, capabilities)

    def analyze_method_call(self, call: MethodCall, capabilities: CapabilityContext):
        """Analyze method call for security"""

        # Determine receiver type
        receiver_type = self.infer_type(call.receiver)

        # Get method definition
        method = self.type_registry.get_method(receiver_type, call.method_name)
        if not method:
            raise SecurityError(f"Method '{call.method_name}' not found on type '{receiver_type}'")

        # Analyze method body with receiver's capabilities
        self.analyze_statements(method.body, capabilities)
```

**Capability Annotations on Structs:**

```ml
// Future enhancement: Require capabilities for certain structs
struct FileHandle {
    capability: file_read,
    path: string,
    handle: any
}

function new_file_handle(path: string) {
    // Automatically checks file_read capability
    return FileHandle{path: path, handle: open(path)};
}
```

---

## Security Integration

### Capability-Based Access Control

**Struct Creation:**
- Struct instantiation is allowed by default
- Sensitive structs can require specific capabilities (future enhancement)

**Method Calls:**
- Methods inherit capabilities from call site
- No special privileges for methods
- Security analysis traverses method bodies

**Field Access:**
- Reading fields: always allowed
- Writing fields: requires mutable reference (future: capability annotation)

**Example with Capabilities:**

```ml
capability file_ops {
    resource "*.txt";
    allow read;
    allow write;
}

struct TextFile {
    path: string,
    content: string
}

function (f: TextFile) read_from_disk() {
    // Requires file_ops capability
    import file;
    f.content = file.read(f.path);
}

function (f: TextFile) write_to_disk() {
    // Requires file_ops capability
    import file;
    file.write(f.path, f.content);
}

// Usage
file = TextFile{path: "data.txt", content: ""};
file.read_from_disk();  // Security check: file_ops capability required
print(file.content);
```

**Security Analysis Pass:**
1. Parse struct/method definitions
2. Analyze method bodies for dangerous operations
3. Propagate capability requirements
4. Enforce at call sites

---

## Code Examples

### Example 1: Simple Data Modeling

```ml
struct User {
    id: number,
    username: string,
    email: string,
    created_at: number
}

function new_user(username: string, email: string) {
    import datetime;
    return User{
        id: random.randint(1, 1000000),
        username: username,
        email: email,
        created_at: datetime.timestamp()
    };
}

function (u: User) display() {
    return "User: " + u.username + " (" + u.email + ")";
}

function (u: User) is_valid_email() {
    import regex;
    pattern = regex.compile("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}");
    return regex.is_match(pattern, u.email);
}

// Create users
alice = new_user("alice", "alice@example.com");
bob = new_user("bob", "invalid-email");

print(alice.display());
print("Alice email valid: " + str(alice.is_valid_email()));  // true
print("Bob email valid: " + str(bob.is_valid_email()));      // false
```

---

### Example 2: Composition with Embedding

```ml
struct Address {
    street: string,
    city: string,
    zip_code: string
}

function (a: Address) format() {
    return a.street + ", " + a.city + " " + a.zip_code;
}

struct Person {
    name: string,
    age: number,
    Address  // Embedded struct
}

function new_person(name: string, age: number, street: string, city: string, zip: string) {
    return Person{
        name: name,
        age: age,
        Address: Address{street: street, city: city, zip_code: zip}
    };
}

function (p: Person) introduce() {
    return "Hi, I'm " + p.name + ", " + str(p.age) + " years old";
}

function (p: Person) full_info() {
    return p.introduce() + ", living at " + p.Address.format();
}

// Usage
alice = new_person("Alice", 30, "123 Main St", "Springfield", "12345");

// Access embedded fields directly
print(alice.city);        // "Springfield" (promoted from Address)
print(alice.zip_code);    // "12345"

// Access embedded struct explicitly
print(alice.Address.format());  // "123 Main St, Springfield 12345"

// Call methods
print(alice.introduce());
print(alice.full_info());
```

---

### Example 3: Interface-Based Polymorphism

```ml
// Define interface
interface Shape {
    area(): number;
    perimeter(): number;
}

// Circle struct
struct Circle {
    radius: number
}

function (c: Circle) area() {
    return 3.14159 * c.radius * c.radius;
}

function (c: Circle) perimeter() {
    return 2 * 3.14159 * c.radius;
}

// Rectangle struct
struct Rectangle {
    width: number,
    height: number
}

function (r: Rectangle) area() {
    return r.width * r.height;
}

function (r: Rectangle) perimeter() {
    return 2 * (r.width + r.height);
}

// Triangle struct
struct Triangle {
    side_a: number,
    side_b: number,
    side_c: number
}

function (t: Triangle) area() {
    // Heron's formula
    s = (t.side_a + t.side_b + t.side_c) / 2;
    import math;
    return math.sqrt(s * (s - t.side_a) * (s - t.side_b) * (s - t.side_c));
}

function (t: Triangle) perimeter() {
    return t.side_a + t.side_b + t.side_c;
}

// Function accepting any Shape
function print_shape_info(shape: Shape) {
    print("Area: " + str(shape.area()));
    print("Perimeter: " + str(shape.perimeter()));
}

// All types satisfy Shape interface implicitly
shapes = [
    Circle{radius: 5},
    Rectangle{width: 10, height: 20},
    Triangle{side_a: 3, side_b: 4, side_c: 5}
];

for (shape in shapes) {
    print_shape_info(shape);
}
```

---

### Example 4: State Management

```ml
struct Counter {
    value: number,
    step: number
}

function new_counter(initial: number, step: number) {
    return Counter{value: initial, step: step};
}

function (c: Counter) increment() {
    c.value = c.value + c.step;
    return c.value;
}

function (c: Counter) decrement() {
    c.value = c.value - c.step;
    return c.value;
}

function (c: Counter) reset() {
    c.value = 0;
}

function (c: Counter) get() {
    return c.value;
}

// Usage
counter = new_counter(0, 5);
print(counter.increment());  // 5
print(counter.increment());  // 10
print(counter.increment());  // 15
counter.reset();
print(counter.get());        // 0

counter2 = new_counter(100, 10);
print(counter2.decrement());  // 90
```

---

### Example 5: Builder Pattern

```ml
struct HttpRequest {
    method: string,
    url: string,
    headers: any,
    body: string
}

function new_http_request() {
    return HttpRequest{
        method: "GET",
        url: "",
        headers: {},
        body: ""
    };
}

function (req: HttpRequest) set_method(method: string) {
    req.method = method;
    return req;  // Fluent interface
}

function (req: HttpRequest) set_url(url: string) {
    req.url = url;
    return req;
}

function (req: HttpRequest) add_header(key: string, value: string) {
    req.headers[key] = value;
    return req;
}

function (req: HttpRequest) set_body(body: string) {
    req.body = body;
    return req;
}

function (req: HttpRequest) send() {
    import http;
    if (req.method == "GET") {
        return http.get(req.url, req.headers);
    } elif (req.method == "POST") {
        return http.post(req.url, req.body, req.headers);
    }
    throw {message: "Unsupported HTTP method: " + req.method};
}

// Usage - fluent API
response = new_http_request()
    .set_method("POST")
    .set_url("https://api.example.com/users")
    .add_header("Content-Type", "application/json")
    .set_body("{\"name\": \"Alice\"}")
    .send();

print(response.status);
```

---

## Viability Assessment

### Technical Feasibility: ✅ **HIGH**

**Pros:**
1. ✅ **Grammar Extensions Are Minimal** - Only 4 new rules needed
2. ✅ **No Breaking Changes** - Fully backward compatible
3. ✅ **Transpiles to Python Classes** - Natural mapping exists
4. ✅ **Builds on Existing Features** - Objects and functions already work
5. ✅ **Similar to Go/TypeScript** - Proven design patterns
6. ✅ **Type Registry is Simple** - Dict-based lookup is efficient

**Cons:**
1. ⚠️ **Type System Complexity** - Need to track struct types across compilation units
2. ⚠️ **Method Resolution** - Need global method registry
3. ⚠️ **Interface Checking** - Duck typing is easy, static checking is hard

**Risk Level:** **LOW** - Core features are straightforward to implement

---

### Integration with Existing ML: ✅ **EXCELLENT**

**Existing Features That Help:**
- ✅ Object literals already exist (`{key: value}`)
- ✅ Dot notation for property access (`obj.prop`)
- ✅ First-class functions enable methods
- ✅ Type annotations already in grammar (optional)
- ✅ Security analyzer already traverses AST

**No Conflicts:**
- ✅ No keyword collisions (`struct`, `interface` are new)
- ✅ No syntax ambiguities (struct literal has type prefix)
- ✅ Existing code continues to work unchanged

**Enhancement to Existing Code:**
- ✅ Can gradually refactor closure-based objects to structs
- ✅ Better documentation with explicit struct definitions
- ✅ Improved IDE support and autocomplete

---

### Security Model Integration: ✅ **SEAMLESS**

**Capability System:**
- ✅ Struct operations go through same security analysis
- ✅ Method calls inherit call-site capabilities
- ✅ Can add capability annotations to structs (future)
- ✅ No new security holes introduced

**Security Analysis:**
- ✅ Struct definitions are static (parsed once)
- ✅ Method bodies are analyzed like regular functions
- ✅ Type registry enables compile-time checking

**No Security Degradation:**
- ✅ All existing security checks still apply
- ✅ No eval/exec/reflection needed for structs
- ✅ Clean transpilation to safe Python code

---

### Developer Experience: ✅ **MAJOR IMPROVEMENT**

**Benefits:**
1. ✅ **Clearer Intent** - Explicit data structures vs. ad-hoc objects
2. ✅ **Less Boilerplate** - No manual closure construction
3. ✅ **Better Errors** - Catch typos at parse time, not runtime
4. ✅ **IDE Support** - Autocomplete struct fields and methods
5. ✅ **Familiar Syntax** - Similar to Go, TypeScript, Rust, Swift
6. ✅ **Documentation** - Structs serve as API contracts

**Learning Curve:**
- ✅ **Minimal** - Concepts are familiar to most programmers
- ✅ Existing functional code still works
- ✅ Can adopt incrementally (no forced migration)

---

### Performance Impact: ✅ **NEUTRAL TO POSITIVE**

**Transpilation:**
- ✅ Structs -> Python dataclasses (efficient)
- ✅ Methods -> instance methods (standard Python)
- ✅ No runtime overhead for type checking (transpile-time only)

**Runtime:**
- ✅ Python classes are well-optimized
- ✅ No reflection or dynamic dispatch needed
- ✅ Possibly faster than closure-based objects (fewer closures created)

**Compilation:**
- ⚠️ Need to build type registry (one-time cost)
- ✅ Type lookups are O(1) with dict-based registry
- ✅ Minimal impact on overall transpile time

---

## Cost-Benefit Analysis

### Implementation Cost

**Development Effort Estimate:**

| Phase | Effort | Complexity |
|-------|---------|------------|
| **Phase 1: Grammar + Parser** | 2-3 days | Low |
| - Add struct/interface keywords | 2 hours | Low |
| - Extend grammar rules | 4 hours | Low |
| - Add AST nodes | 2 hours | Low |
| - Update transformer | 8 hours | Medium |
| - Write parser tests | 4 hours | Low |
| | | |
| **Phase 2: Type Registry** | 2-3 days | Medium |
| - Implement TypeRegistry class | 4 hours | Low |
| - Struct registration | 2 hours | Low |
| - Method registration | 4 hours | Medium |
| - Interface checking (optional) | 8 hours | Medium |
| - Write registry tests | 4 hours | Low |
| | | |
| **Phase 3: Code Generation** | 3-4 days | Medium |
| - Generate Python dataclasses | 8 hours | Medium |
| - Generate instance methods | 6 hours | Medium |
| - Handle struct literals | 4 hours | Low |
| - Method binding logic | 6 hours | Medium |
| - Write codegen tests | 8 hours | Medium |
| | | |
| **Phase 4: Security Integration** | 2-3 days | Medium |
| - Analyze struct definitions | 4 hours | Low |
| - Analyze method calls | 6 hours | Medium |
| - Capability enforcement | 6 hours | Medium |
| - Write security tests | 6 hours | Medium |
| | | |
| **Phase 5: Testing & Documentation** | 3-4 days | Low |
| - Integration tests | 8 hours | Medium |
| - Example programs | 8 hours | Low |
| - Update language reference | 4 hours | Low |
| - Update developer guide | 4 hours | Low |
| | | |
| **Total** | **12-17 days** | **Medium** |

**Testing Requirements:**
- ✅ Unit tests for parser (30+ test cases)
- ✅ Unit tests for type registry (20+ test cases)
- ✅ Unit tests for code generator (40+ test cases)
- ✅ Security tests (15+ test cases)
- ✅ Integration tests (25+ complex programs)
- ✅ Backward compatibility tests (all existing tests must pass)

**Documentation Updates:**
- Language reference (struct syntax, methods, interfaces)
- Tutorial with examples
- Developer guide (implementing types)
- Migration guide (closures -> structs)

---

### Benefits

**Immediate Benefits:**

1. **Better Code Organization** ⭐⭐⭐⭐⭐
   - Clear data structures with explicit fields
   - Methods grouped by type
   - Reduced boilerplate

2. **Improved Type Safety** ⭐⭐⭐⭐
   - Catch field typos at parse time
   - Type annotations for documentation
   - Future: full static type checking

3. **Enhanced Developer Experience** ⭐⭐⭐⭐⭐
   - IDE autocomplete for fields/methods
   - Clearer error messages
   - Familiar syntax (Go/TypeScript-like)

4. **Better Performance** ⭐⭐⭐
   - Python classes are efficient
   - Less closure creation overhead
   - Optimized field access

5. **Simplified Codebase** ⭐⭐⭐⭐
   - Replace closure-based patterns
   - Less nesting in code
   - Clearer intent

**Long-Term Benefits:**

1. **Foundation for Advanced Features** ⭐⭐⭐⭐⭐
   - Generic types (Phase 2)
   - Pattern matching on structs
   - Trait system (like Rust)
   - Enum types with data

2. **Enterprise Adoption** ⭐⭐⭐⭐
   - Familiar OOP concepts
   - Better code maintainability
   - Easier onboarding

3. **Tooling Ecosystem** ⭐⭐⭐⭐⭐
   - LSP can provide rich completions
   - Static analyzers can find bugs
   - Code generators can emit structs
   - Documentation tools can parse types

4. **Library Ecosystem** ⭐⭐⭐⭐
   - Standard library can use structs
   - Third-party libraries have clear APIs
   - Better reusability

---

### Cost-Benefit Summary

| Metric | Score |
|--------|-------|
| **Implementation Cost** | Medium (12-17 days) |
| **Technical Complexity** | Low-Medium |
| **Risk Level** | Low |
| **Immediate Value** | ⭐⭐⭐⭐⭐ |
| **Long-Term Value** | ⭐⭐⭐⭐⭐ |
| **Developer Experience** | ⭐⭐⭐⭐⭐ |
| **Backward Compatibility** | ⭐⭐⭐⭐⭐ (100%) |
| **Security Impact** | ⭐⭐⭐⭐⭐ (Neutral/Positive) |

**Verdict:** ✅ **HIGHLY RECOMMENDED**

The benefits far outweigh the costs. This feature:
- Significantly improves developer experience
- Has low implementation risk
- Integrates seamlessly with existing language
- Provides foundation for future enhancements
- Maintains 100% backward compatibility

---

## Implementation Roadmap

### Sprint 1: Grammar & Parser (Days 1-3)

**Goals:**
- ✅ Add struct/interface keywords
- ✅ Extend grammar with struct/method rules
- ✅ Create new AST nodes
- ✅ Update transformer to build AST
- ✅ Write comprehensive parser tests

**Deliverables:**
- Updated `ml.lark` grammar file
- New AST node classes in `ast_nodes.py`
- Updated `MLTransformer` in parser
- 30+ parser unit tests

**Success Criteria:**
- All struct/method syntax parses correctly
- AST nodes have proper structure
- Existing tests continue to pass (100%)

---

### Sprint 2: Type Registry (Days 4-6)

**Goals:**
- ✅ Implement TypeRegistry class
- ✅ Register structs, methods, interfaces
- ✅ Method lookup by (type, name)
- ✅ Interface satisfaction checking
- ✅ Write registry unit tests

**Deliverables:**
- `type_registry.py` module
- Integration with Transpiler class
- 20+ type registry unit tests

**Success Criteria:**
- Structs can be registered and retrieved
- Methods can be looked up by type
- Duplicate definitions are caught
- Interface checking works (duck typing)

---

### Sprint 3: Code Generation (Days 7-10)

**Goals:**
- ✅ Generate Python dataclasses from structs
- ✅ Generate instance methods
- ✅ Handle struct literals
- ✅ Bind methods to classes
- ✅ Write codegen unit tests

**Deliverables:**
- Updated `python_generator.py`
- Struct/method generation logic
- 40+ code generation unit tests

**Success Criteria:**
- Structs transpile to valid Python dataclasses
- Methods transpile to instance methods
- Struct literals work correctly
- Generated code runs successfully

---

### Sprint 4: Security Integration (Days 11-13)

**Goals:**
- ✅ Analyze struct definitions for security
- ✅ Analyze method calls
- ✅ Enforce capability requirements
- ✅ Write security tests

**Deliverables:**
- Updated `security_analyzer.py`
- Struct/method security checks
- 15+ security unit tests

**Success Criteria:**
- Struct operations respect capabilities
- Method bodies are analyzed
- Security tests pass (100%)
- No new vulnerabilities introduced

---

### Sprint 5: Testing & Documentation (Days 14-17)

**Goals:**
- ✅ Write integration tests (25+ programs)
- ✅ Create example programs
- ✅ Update language reference
- ✅ Update developer guide
- ✅ Migration guide for existing code

**Deliverables:**
- 25+ integration test programs
- Example programs demonstrating features
- Updated documentation
- Migration guide

**Success Criteria:**
- All integration tests pass
- Documentation is comprehensive
- Examples are clear and educational
- Existing tests pass (100%)

---

### Sprint 6 (Optional): Advanced Features

**Phase 2 Enhancements:**
- Generic types: `struct Stack<T> { ... }`
- Enum types: `enum Color { Red, Green, Blue }`
- Pattern matching on structs
- Trait system (interface + default implementations)
- Method receivers: value vs reference semantics

---

## Alternatives Considered

### Alternative 1: Classical Classes with Inheritance

**Syntax:**
```ml
class Person {
    name: string;
    age: number;

    constructor(name, age) {
        this.name = name;
        this.age = age;
    }

    introduce() {
        return "Hi, I'm " + this.name;
    }
}

class Employee extends Person {
    company: string;

    constructor(name, age, company) {
        super(name, age);
        this.company = company;
    }
}
```

**Pros:**
- ✅ Familiar to Java/C#/JavaScript developers
- ✅ Inheritance allows code reuse

**Cons:**
- ❌ **Too Complex** - Classes, inheritance, super, this
- ❌ **Inheritance Issues** - Diamond problem, fragile base class
- ❌ **Not Aligned with ML Philosophy** - Functional-first language
- ❌ **Security Concerns** - Subclassing can bypass security
- ❌ **Implicit Behavior** - `this` binding is confusing

**Verdict:** ❌ **Rejected** - Too complex, doesn't fit ML's functional nature

---

### Alternative 2: Prototype-Based Objects (JavaScript-style)

**Syntax:**
```ml
Person = {
    create: function(name, age) {
        obj = Object.create(Person);
        obj.name = name;
        obj.age = age;
        return obj;
    },

    introduce: function() {
        return "Hi, I'm " + this.name;
    }
};

alice = Person.create("Alice", 30);
alice.introduce();
```

**Pros:**
- ✅ Flexible and dynamic
- ✅ No need for class declarations

**Cons:**
- ❌ **No Type Identity** - Objects are just dictionaries
- ❌ **Poor Tooling** - Can't autocomplete or type-check
- ❌ **Confusing Semantics** - Prototype chains are hard to reason about
- ❌ **Performance** - Prototype lookups are slow

**Verdict:** ❌ **Rejected** - Doesn't improve over current closure-based approach

---

### Alternative 3: Type Classes (Haskell-style)

**Syntax:**
```ml
typeclass Drawable a {
    draw: a -> string;
    area: a -> number;
}

data Circle = Circle { radius: number }

instance Drawable Circle {
    draw = function(c) { ... };
    area = function(c) { ... };
}
```

**Pros:**
- ✅ Powerful abstraction mechanism
- ✅ Ad-hoc polymorphism
- ✅ Type-safe

**Cons:**
- ❌ **Very Complex** - Requires advanced type system
- ❌ **Steep Learning Curve** - Not familiar to most developers
- ❌ **Implementation Difficulty** - Type inference is hard
- ❌ **Overkill** - ML is not Haskell

**Verdict:** ❌ **Rejected** - Too complex for ML's pragmatic goals

---

### Alternative 4: Duck Typing Only (Current State)

**Keep closure-based objects:**
```ml
function create_person(name, age) {
    return {
        name: name,
        age: age,
        introduce: function() { return "Hi, I'm " + name; }
    };
}
```

**Pros:**
- ✅ Already works
- ✅ No implementation needed
- ✅ Maximally flexible

**Cons:**
- ❌ **Verbose** - Lots of boilerplate
- ❌ **No Type Information** - Can't distinguish data types
- ❌ **Poor Tooling** - No autocomplete or type checking
- ❌ **Runtime Errors** - Typos not caught until runtime

**Verdict:** ❌ **Rejected** - Current approach is limiting for larger programs

---

## Why Golang-Style Structs Win

**The Goldilocks Solution:**
- ✅ **Not Too Simple** - More structured than duck typing
- ✅ **Not Too Complex** - No inheritance, classes, or prototypes
- ✅ **Just Right** - Structs + methods + interfaces (implicit)

**Key Advantages:**
1. **Familiar Syntax** - Looks like TypeScript, Go, Rust
2. **Easy to Learn** - Simple mental model
3. **Pragmatic** - Solves real problems without over-engineering
4. **Performant** - Clean transpilation to Python classes
5. **Extensible** - Foundation for generics, enums, traits
6. **Secure** - Integrates with capability system
7. **Backward Compatible** - Doesn't break existing code

---

## Conclusion

**Recommendation:** ✅ **PROCEED WITH IMPLEMENTATION**

Golang-style structs, methods, and interfaces are an excellent fit for ML:
- **Low Risk** - Minimal grammar changes, no breaking changes
- **High Value** - Dramatically improves developer experience
- **Good Foundation** - Enables future type system enhancements
- **Natural Integration** - Builds on existing features
- **Proven Design** - Success in Go, TypeScript, Rust, Swift

**Next Steps:**
1. Review proposal with stakeholders
2. Get approval for 12-17 day implementation sprint
3. Begin Sprint 1: Grammar & Parser extensions
4. Iterate based on feedback from early testing

**Estimated Timeline:** 12-17 days for full implementation + testing + docs

**Success Metrics:**
- ✅ 100% backward compatibility maintained
- ✅ 95%+ test coverage for new features
- ✅ <5% impact on transpilation performance
- ✅ 0 new security vulnerabilities
- ✅ Positive developer feedback on syntax

---

## Appendix: Advanced Features (Future Work)

### Generic Types

```ml
struct Stack<T> {
    items: array,
    capacity: number
}

function (s: Stack<T>) push(item: T) {
    s.items = s.items + [item];
}

function (s: Stack<T>) pop(): T {
    item = s.items[len(s.items) - 1];
    s.items = s.items[0:len(s.items) - 1];
    return item;
}

// Usage with type parameter
int_stack = Stack<number>{items: [], capacity: 100};
int_stack.push(42);
```

---

### Enum Types with Data

```ml
enum Result<T, E> {
    Ok(T),
    Err(E)
}

function divide(a: number, b: number): Result<number, string> {
    if (b == 0) {
        return Result.Err("Division by zero");
    }
    return Result.Ok(a / b);
}

result = divide(10, 2);
// Pattern matching (future)
match result {
    Result.Ok(value) => print("Success: " + str(value)),
    Result.Err(msg) => print("Error: " + msg)
}
```

---

### Trait System (Interfaces + Default Implementations)

```ml
trait Printable {
    print(): string;

    // Default implementation
    println(): string {
        return this.print() + "\n";
    }
}

struct Person {
    name: string
}

// Implement trait for Person
impl Printable for Person {
    print(): string {
        return "Person: " + this.name;
    }
    // println() inherited from trait
}

alice = Person{name: "Alice"};
print(alice.println());  // Uses default impl from trait
```

---

### Method Receivers: Value vs Reference

```ml
struct Counter {
    value: number
}

// Value receiver - doesn't modify original
function (c: Counter) get(): number {
    return c.value;
}

// Mutable receiver - modifies original (explicit &)
function (c: &Counter) increment() {
    c.value = c.value + 1;
}

counter = Counter{value: 0};
counter.increment();  // Modifies counter
print(counter.get());  // 1
```

---

**End of Proposal**
