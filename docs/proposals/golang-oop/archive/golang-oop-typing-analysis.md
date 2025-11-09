# Typing Analysis: Golang-Style OOP in an Untyped Language

**Context:** Evaluating the Go-style OOP proposal for ML, an untyped language
**Date:** November 4, 2025
**Status:** Critical Design Analysis

---

## The Fundamental Question

**Can Go-style OOP (from a statically typed language) work well in ML (a dynamically typed language)?**

Go's struct system assumes:
- ✅ Compile-time type checking
- ✅ Method dispatch resolved at compile time
- ✅ Interface satisfaction checked at compile time
- ✅ Type safety guarantees

ML's reality:
- ❌ No compile-time type checking
- ❌ No static analysis of types
- ❌ Duck typing everywhere
- ❌ Type annotations exist but are **completely unused** (0 occurrences in 80+ test files!)

---

## Current State: ML is Completely Untyped

### Grammar Reality Check

```lark
// Type annotations exist in grammar:
parameter: IDENTIFIER (":" type_annotation)?
type_annotation: IDENTIFIER
```

**But they are NEVER used:**
- ✅ Searched 80+ ML test files
- ❌ Found **0 uses** of type annotations
- ❌ Grammar supports them, but nobody writes them
- ❌ Transpiler ignores them completely

### Current ML Code Style

```ml
// NO type annotations anywhere
function create_account(initial_balance) {
    balance = initial_balance;

    function deposit(amount) {
        nonlocal balance;
        balance = balance + amount;
        return balance;
    }

    return {
        deposit: deposit,
        balance: function() { return balance; }
    };
}

// Objects are just dictionaries
account = create_account(1000);
account.deposit(500);
```

**Observations:**
1. Functions have no parameter types
2. No return type annotations
3. Objects are dictionaries with function properties
4. Duck typing is the norm
5. Runtime errors if you call missing methods

---

## The Core Tension: Static Syntax in Dynamic Language

### What the Proposal Suggests

```ml
// Explicit struct type
struct BankAccount {
    balance: number,
    owner: string
}

// Method with typed receiver
function (acc: BankAccount) deposit(amount: number) {
    acc.balance = acc.balance + amount;
}

// Usage
account = BankAccount{balance: 1000, owner: "Alice"};
account.deposit(500);
```

### Critical Questions

1. **What does `balance: number` mean if we don't check types?**
   - Is it documentation only?
   - Do we check at runtime?
   - Do we validate field types on struct creation?

2. **What does `function (acc: BankAccount)` mean?**
   - Do we check that `acc` is actually a BankAccount?
   - What if someone passes a plain dictionary?
   - What if they pass a different struct type?

3. **How do structs interact with plain objects?**
   ```ml
   // Current code: plain object
   obj1 = {balance: 1000, owner: "Bob"};

   // New code: struct instance
   obj2 = BankAccount{balance: 1000, owner: "Bob"};

   // Are these interchangeable?
   // Can I pass obj1 to a function expecting BankAccount?
   ```

4. **What happens in Python?**
   ```python
   # Struct transpiles to:
   @dataclass
   class BankAccount:
       balance: Union[int, float]
       owner: str

   # But Python type hints are also optional!
   # So we still have no runtime enforcement unless we add it
   ```

---

## Design Option 1: Type Annotations Are Documentation Only

### Approach
- Struct fields have type annotations
- Method receivers have type annotations
- **But**: No checking at parse/transpile/runtime
- Pure documentation for humans and IDEs

### Example
```ml
struct Point {
    x: number,  // Documentation only
    y: number
}

function (p: Point) distance() {  // No checking that p is a Point
    return math.sqrt(p.x * p.x + p.y * p.y);
}

// All of these work (no errors):
p1 = Point{x: 3, y: 4};
p2 = {x: 3, y: 4};  // Plain object
p3 = {x: "hello", y: "world"};  // Wrong types!

p1.distance();  // Works
p2.distance();  // Also works (duck typing)
p3.distance();  // Runtime error: can't multiply strings
```

### Pros
- ✅ Simple to implement
- ✅ No performance overhead
- ✅ Backward compatible (structs work like fancy objects)
- ✅ IDEs can use types for autocomplete
- ✅ Documentation value

### Cons
- ❌ Types are meaningless (just comments in disguise)
- ❌ No safety guarantees
- ❌ Can't distinguish struct instances from plain objects
- ❌ No benefit over current dictionary approach except syntax
- ❌ False sense of security

### Verdict: **Questionable Value**
If types aren't checked, why have struct syntax at all? Current dictionaries work fine.

---

## Design Option 2: Runtime Type Checking (Gradual Typing)

### Approach
- Type annotations are **enforced at runtime**
- Struct creation validates field types
- Method calls validate receiver type
- Bridge between untyped and typed worlds

### Example
```ml
struct Point {
    x: number,
    y: number
}

// Runtime checks on creation
p1 = Point{x: 3, y: 4};        // ✅ OK
p2 = Point{x: "hello", y: 4};  // ❌ TypeError: x must be number

// Runtime checks on method calls
function (p: Point) distance() {
    return math.sqrt(p.x * p.x + p.y * p.y);
}

p1.distance();  // ✅ OK (p1 is a Point)

plain_obj = {x: 3, y: 4};
plain_obj.distance();  // ❌ TypeError: receiver must be Point
```

### Implementation in Python
```python
@dataclass
class Point:
    x: Union[int, float]
    y: Union[int, float]

    def __post_init__(self):
        # Runtime type checking
        if not isinstance(self.x, (int, float)):
            raise TypeError(f"Field 'x' must be number, got {type(self.x)}")
        if not isinstance(self.y, (int, float)):
            raise TypeError(f"Field 'y' must be number, got {type(self.y)}")

def Point_distance(self):
    if not isinstance(self, Point):
        raise TypeError(f"Method receiver must be Point, got {type(self)}")
    return math.sqrt(self.x * self.x + self.y * self.y)

Point.distance = Point_distance
```

### Pros
- ✅ **Real type safety** (at runtime)
- ✅ Catch type errors early
- ✅ Struct instances are distinct from plain objects
- ✅ Clear error messages
- ✅ Gradual migration path (plain objects still work elsewhere)
- ✅ IDE can trust type annotations

### Cons
- ⚠️ Performance overhead (runtime checks)
- ⚠️ More complex implementation
- ⚠️ Breaking change (can't pass plain objects to typed methods)
- ⚠️ Need to handle untyped fields (what if no type annotation?)

### Verdict: **Promising**
Provides real value while maintaining dynamic flexibility.

---

## Design Option 3: Optional Type Checking (Type Hints)

### Approach
- Type annotations are **optional** on struct fields
- If present, checked at runtime
- If absent, no checking (dynamic)
- Best of both worlds?

### Example
```ml
// Fully typed struct (runtime checks)
struct StrictPoint {
    x: number,
    y: number
}

// Partially typed struct (only name checked)
struct Person {
    name: string,
    age,           // No type - accepts anything
    metadata       // No type - dynamic field
}

// Untyped struct (no checks, just shape)
struct Config {
    host,
    port,
    options
}

// Method with typed receiver but untyped parameters
function (p: StrictPoint) move(dx, dy) {  // dx, dy not checked
    p.x = p.x + dx;
    p.y = p.y + dy;
}
```

### Pros
- ✅ Flexibility: choose when to use types
- ✅ Gradual adoption: add types over time
- ✅ Backward compatible
- ✅ Performance: only pay for what you use

### Cons
- ⚠️ Inconsistent: some code typed, some not
- ⚠️ Confusing: when should you add types?
- ⚠️ Partial safety: types only help where used

### Verdict: **Most Practical**
Matches ML's pragmatic philosophy.

---

## Design Option 4: Structural Typing (Duck Typing++)

### Approach
- Structs define **shape** not **type**
- Type annotations are **interface contracts**
- Any object with matching fields satisfies the struct
- True duck typing: "if it walks like a duck..."

### Example
```ml
struct Point {
    x: number,
    y: number
}

function (p: Point) distance() {
    // Checks: does p have x and y fields that are numbers?
    // Doesn't care if p is a Point instance or plain object
    return math.sqrt(p.x * p.x + p.y * p.y);
}

// All of these work:
p1 = Point{x: 3, y: 4};           // Struct instance
p2 = {x: 3, y: 4};                 // Plain object
p3 = Vector{x: 3, y: 4, z: 0};    // Different struct with x, y

p1.distance();  // ✅ Has x, y numbers
p2.distance();  // ✅ Has x, y numbers
p3.distance();  // ✅ Has x, y numbers (ignores z)

p4 = {x: "hello", y: 4};
p4.distance();  // ❌ Runtime error: x not a number
```

### Implementation
```python
def Point_distance(self):
    # Structural type checking
    if not hasattr(self, 'x') or not isinstance(self.x, (int, float)):
        raise TypeError("Receiver must have numeric 'x' field")
    if not hasattr(self, 'y') or not isinstance(self.y, (int, float)):
        raise TypeError("Receiver must have numeric 'y' field")
    return math.sqrt(self.x * self.x + self.y * self.y)
```

### Pros
- ✅ **True duck typing**: works with any compatible object
- ✅ Backward compatible: plain objects work fine
- ✅ Flexible: struct instances not special
- ✅ Matches Python philosophy
- ✅ Matches ML's untyped nature
- ✅ Gradual: can add more type checks over time

### Cons
- ⚠️ Slower: must check field existence and types
- ⚠️ Less clear: struct instances not distinct
- ⚠️ Can't tell if object is "intended" to be a Point
- ⚠️ Error messages less precise

### Verdict: **Most ML-like**
Fits the untyped, dynamic philosophy perfectly.

---

## Interaction with Existing Code

### Question: How do structs work with current ML code?

**Scenario 1: Calling struct methods on plain objects**
```ml
// New code defines struct and method
struct Person {
    name: string,
    age: number
}

function (p: Person) greet() {
    return "Hi, I'm " + p.name;
}

// Old code uses plain objects
person = {name: "Alice", age: 30};

// Can this work?
person.greet();  // Depends on design choice!
```

**Options:**
- **Option 1 (Documentation Only):** ✅ Works (method just checks for fields)
- **Option 2 (Runtime Type Check):** ❌ TypeError (person is not a Person instance)
- **Option 3 (Optional Types):** Depends on whether Person fields have types
- **Option 4 (Structural):** ✅ Works (has name and age)

**Scenario 2: Mixing struct instances and plain objects**
```ml
people = [
    Person{name: "Alice", age: 30},     // Struct instance
    {name: "Bob", age: 25},             // Plain object
    Employee{name: "Carol", age: 35, id: 123}  // Different struct
];

for (p in people) {
    print(p.name);  // Works for all?
}
```

**Design Impact:**
- **Structural typing:** All work (all have `name` field)
- **Nominal typing:** Only Person instances work in Person methods
- **Duck typing:** All work, no type checking

---

## Type Hints in Function Parameters

### Current State
```ml
// ML today: parameters have NO types
function add(a, b) {
    return a + b;
}
```

### With Go-Style OOP
```ml
// Would we encourage this?
function add(a: number, b: number): number {
    return a + b;
}

// Or this?
function process(user: User, config: Config): Result {
    // ...
}
```

### Questions
1. **Are parameter types enforced?**
   - If yes: need runtime checks on every function call (expensive!)
   - If no: why write them?

2. **Are return types enforced?**
   - If yes: need runtime checks on every return (expensive!)
   - If no: just documentation

3. **Mixing typed and untyped?**
   ```ml
   function process(user: User, data, config: Config, callback) {
       // Some typed, some not - confusing?
   }
   ```

4. **Type inference?**
   ```ml
   function (p: Point) move(dx, dy) {
       // Should dx and dy be inferred as numbers?
       // Or are they dynamic?
   }
   ```

---

## Recommendation: Hybrid Approach (Structural + Optional)

### Proposed Design

**1. Structs define structural contracts**
```ml
struct Point {
    x: number,   // Optional type annotation
    y: number
}

struct Config {
    host,        // No type - accepts anything
    port
}
```

**2. Runtime structural type checking**
- When type annotations present: check field types at creation and method calls
- When type annotations absent: no checking (fully dynamic)
- Works with plain objects if they have matching fields

**3. Method receivers use structural matching**
```ml
function (p: Point) distance() {
    // At runtime: check p has x, y fields (with types if annotated)
    // Works if p is Point instance OR plain object with x, y numbers
    return math.sqrt(p.x * p.x + p.y * p.y);
}
```

**4. Type annotations optional everywhere**
```ml
// Fully typed
function add(a: number, b: number): number {
    return a + b;  // Runtime check a, b are numbers
}

// Partially typed
function process(user: User, data) {
    // user checked, data not
}

// Untyped (like today)
function calculate(x, y, z) {
    return x + y * z;
}
```

### Benefits

✅ **Backward Compatible:** Plain objects work with struct methods
✅ **Gradual Typing:** Add types where needed, omit elsewhere
✅ **Real Safety:** Types are checked when present
✅ **Performance:** Only pay for checking where you use types
✅ **Clear Intent:** Struct definitions document data shape
✅ **IDE Support:** Type annotations enable autocomplete
✅ **Duck Typing:** Works with ML's dynamic philosophy
✅ **No False Security:** Types mean something (runtime checks)

### Implementation Strategy

1. **Struct Creation**
   ```python
   @dataclass
   class Point:
       x: Union[int, float]
       y: Union[int, float]

       def __post_init__(self):
           # Only check if type annotation present in ML
           self._check_types()
   ```

2. **Method Dispatch**
   ```python
   def Point_distance(self):
       # Structural check: has x, y with correct types?
       _check_structural_type(self, Point)
       return math.sqrt(self.x * self.x + self.y * self.y)
   ```

3. **Type Registry**
   ```python
   # Store struct definitions with field type info
   type_registry = {
       'Point': StructDef(
           fields={'x': 'number', 'y': 'number'},
           required_types=True
       ),
       'Config': StructDef(
           fields={'host': None, 'port': None},
           required_types=False
       )
   }
   ```

---

## Answering the Original Questions

### 1. Is Go-style OOP useful for an untyped language?

**Yes, BUT** only with significant modifications:
- ✅ Struct syntax provides **clear data shape** (better than dictionaries)
- ✅ Methods organized by type (better than closures)
- ✅ IDE autocomplete and tooling support
- ❌ Can't use Go's compile-time type checking
- ✅ Can use **runtime structural type checking** instead
- ✅ Types become **optional gradual contracts**, not requirements

### 2. How do existing datatypes work with new syntax?

**Structural typing makes them compatible:**
```ml
// Old code
old_point = {x: 3, y: 4};

// New code
struct Point { x: number, y: number }
function (p: Point) distance() { ... }

// Compatibility via structural matching
old_point.distance();  // ✅ Works! Has x, y fields
```

### 3. What about type hints in function parameters?

**Make them optional and checked at runtime:**
```ml
// Typed parameters (runtime checked)
function add(a: number, b: number) {
    return a + b;  // TypeError if a or b not number
}

// Untyped parameters (like today)
function process(data) {
    return data * 2;  // No checks, full dynamic
}

// Mixed (gradually typed)
function handle(user: User, raw_data, config: Config) {
    // user and config checked, raw_data not
}
```

---

## Implementation Complexity Assessment

| Design Choice | Implementation Effort | Runtime Cost | Safety | Compatibility |
|--------------|---------------------|-------------|--------|--------------|
| **Documentation Only** | Low (1-2 days) | None | None | 100% |
| **Runtime Nominal** | Medium (3-4 days) | Medium | High | Breaking |
| **Optional Checking** | Medium (3-4 days) | Low | Medium | High |
| **Structural Typing** | High (5-6 days) | Medium | Medium | 100% |
| **Hybrid (Recommended)** | High (6-8 days) | Low-Med | Med-High | 100% |

---

## Conclusion

**The Go-style OOP proposal CAN work for ML, but needs adaptation:**

### Key Changes from Original Proposal

1. **Type annotations must be optional** (not required)
2. **Use structural typing** (not nominal typing like Go)
3. **Runtime type checking** (not compile-time like Go)
4. **Duck typing compatibility** (plain objects work with struct methods)
5. **Gradual typing philosophy** (add types where helpful, omit elsewhere)

### Recommended Next Steps

1. **Prototype structural type checker** (2 days)
2. **Update proposal** with hybrid approach (1 day)
3. **Test compatibility** with existing ML code (1 day)
4. **Implement runtime checking** for structs (3 days)
5. **Add IDE type hints** for tooling support (2 days)

### Final Recommendation

✅ **Proceed with MODIFIED proposal:**
- Use struct syntax for clear data modeling
- Make type annotations **optional** with **runtime checking**
- Use **structural typing** for compatibility
- Maintain backward compatibility with plain objects
- Position as "better dictionaries with optional safety" not "static type system"

This gives ML developers the benefits of structured data and optional type safety while preserving the language's dynamic, pragmatic nature.
