# Default Value Semantics: Deep Analysis

**Date:** November 5, 2025
**Issue:** Default field values evaluation strategy
**Status:** Needs decision

---

## The Problem

The proposal allows default field values but doesn't specify **when** they are evaluated:

```ml
struct Config {
    id: string = generate_uuid(),
    timestamp: number = time.now(),
    items: array = []
}

c1 = Config{};
c2 = Config{};

// Question: Are c1.id and c2.id the same or different?
```

This is **not a trivial detail** - it affects:
- Correctness (mutable defaults)
- Performance (evaluation overhead)
- Developer expectations
- Security (predictable vs unpredictable values)

---

## Option 1: Per-Struct Evaluation (Class Variable Pattern)

**Semantics:** Default expressions evaluated **once** when struct is defined, shared across all instances.

### Example

```ml
struct Counter {
    id: string = generate_uuid(),
    items: array = []
}

c1 = Counter{};
c2 = Counter{};

print(c1.id == c2.id);  // true (SAME UUID!)
c1.items.append(1);
print(c2.items);  // [1] (SHARED ARRAY!)
```

### How It Works

```python
# Transpiled Python (pseudocode)
class Counter:
    # Defaults evaluated at class definition time
    _default_id = generate_uuid()  # Evaluated ONCE
    _default_items = []             # Evaluated ONCE

    def __init__(self, id=None, items=None):
        self.id = id if id is not None else Counter._default_id
        self.items = items if items is not None else Counter._default_items  # SHARED!
```

### Pros

✅ **Performance** - Defaults evaluated only once
✅ **Constant defaults** - Efficient for immutable values
✅ **Simple implementation** - No special handling needed

### Cons

❌ **Mutable default disaster** - Arrays/objects shared across instances (Python's infamous pitfall)
❌ **Surprising behavior** - `[]` default means ALL instances share same array
❌ **Dynamic values broken** - `generate_uuid()` generates same UUID for all instances
❌ **Security issue** - Predictable "random" values
❌ **Violates expectations** - Most developers expect fresh defaults

### When It Breaks

```ml
// BROKEN: All counters share same items array
struct TodoList {
    items: array = []
}

list1 = TodoList{};
list2 = TodoList{};

list1.items.append("Buy milk");
print(list2.items);  // ["Buy milk"] - UNEXPECTED!
```

**Verdict:** ❌ **REJECT** - Too dangerous, violates expectations

---

## Option 2: Per-Instance Evaluation (Constructor Pattern)

**Semantics:** Default expressions evaluated **every time** an instance is created.

### Example

```ml
struct Counter {
    id: string = generate_uuid(),
    items: array = []
}

c1 = Counter{};
c2 = Counter{};

print(c1.id == c2.id);  // false (DIFFERENT UUIDs)
c1.items.append(1);
print(c2.items);  // [] (SEPARATE ARRAYS)
```

### How It Works

```python
# Transpiled Python (pseudocode)
class Counter:
    def __init__(self, id=None, items=None):
        # Defaults evaluated at instance creation time
        self.id = id if id is not None else generate_uuid()  # Evaluated EACH TIME
        self.items = items if items is not None else []      # Fresh array EACH TIME
```

### Pros

✅ **Correct mutable defaults** - Each instance gets fresh array/object
✅ **Dynamic values work** - `generate_uuid()` generates different UUID each time
✅ **Intuitive** - Matches developer expectations (like Python `__init__`)
✅ **Safe** - No shared mutable state
✅ **Secure** - Unpredictable dynamic values

### Cons

⚠️ **Performance cost** - Defaults evaluated on every instantiation
⚠️ **Expensive defaults** - `expensive_computation()` runs every time

### When It Works Well

```ml
// CORRECT: Each todo list has its own items
struct TodoList {
    id: string = generate_uuid(),
    items: array = []
}

list1 = TodoList{};
list2 = TodoList{};

list1.items.append("Buy milk");
print(list2.items);  // [] - EXPECTED!
print(list1.id == list2.id);  // false - EXPECTED!
```

**Verdict:** ✅ **RECOMMENDED** - Safe, intuitive, matches expectations

---

## Option 3: Hybrid (Lazy Evaluation)

**Semantics:** Defaults evaluated on **first access** per instance.

### Example

```ml
struct Config {
    connection = expensive_connect()  // Only evaluated when accessed
}

c = Config{};
// No connection made yet

c.connection.send("data");  // NOW expensive_connect() is called
```

### How It Works

```python
# Transpiled Python (pseudocode)
class Config:
    def __init__(self, connection=None):
        self._connection = connection
        self._connection_initialized = connection is not None

    @property
    def connection(self):
        if not self._connection_initialized:
            self._connection = expensive_connect()
            self._connection_initialized = True
        return self._connection
```

### Pros

✅ **Lazy** - Expensive defaults only evaluated if accessed
✅ **Efficient** - Skip unused defaults
✅ **Deferred costs** - Spread initialization over time

### Cons

❌ **Complexity** - Requires property getters
❌ **Confusing** - Non-obvious evaluation timing
❌ **Side effects** - When do side effects happen?
❌ **Thread safety** - Race conditions on first access

**Verdict:** ❌ **REJECT** - Too complex for MVP, confusing semantics

---

## Option 4: Restricted Defaults (Constants Only)

**Semantics:** Only allow **constant literal** defaults, forbid expressions.

### Example

```ml
// ALLOWED: Literal constants
struct Config {
    host: string = "localhost",
    port: number = 8080,
    debug: boolean = false
}

// FORBIDDEN: Expressions/function calls
struct Counter {
    id: string = generate_uuid(),  // ERROR: Not a constant
    items: array = []               // OK: Empty array is constant
}
```

### How It Works

- Parser validates default expressions
- Only literals allowed: numbers, strings, booleans, `[]`, `{}`
- No function calls, no variable references

### Pros

✅ **Simple** - No evaluation timing issues
✅ **Safe** - No shared mutable state (empty `[]` is fine)
✅ **Fast** - Literals are cheap
✅ **Predictable** - Defaults always same

### Cons

❌ **Limited** - Can't use `generate_uuid()`, `time.now()`, etc.
❌ **Workarounds needed** - Factory functions for dynamic defaults
❌ **Less convenient** - Common use cases require more code

### Workaround Pattern

```ml
// Instead of defaults, use factory function
function new_counter(): Counter {
    return Counter{
        id: generate_uuid(),
        items: []
    };
}

c1 = new_counter();
c2 = new_counter();
```

**Verdict:** 🟡 **VIABLE ALTERNATIVE** - Simple, safe, but limited

---

## Comparison Table

| Aspect | Per-Struct | Per-Instance | Lazy | Constants Only |
|--------|------------|--------------|------|----------------|
| **Mutable defaults safe?** | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes |
| **Dynamic values work?** | ❌ No | ✅ Yes | ✅ Yes | ❌ No |
| **Performance** | ✅ Fast | ⚠️ Slower | ✅ Fast | ✅ Fast |
| **Complexity** | ✅ Simple | ✅ Simple | ❌ Complex | ✅ Simple |
| **Intuitive?** | ❌ No | ✅ Yes | ⚠️ Maybe | ✅ Yes |
| **Secure?** | ❌ Predictable | ✅ Unpredictable | ✅ Unpredictable | ⚠️ Predictable |

---

## Real-World Language Precedents

### Python

```python
# Per-instance (with mutable default pitfall)
class Config:
    def __init__(self, items=[]):  # WRONG! Shared default
        self.items = items

# Correct way
class Config:
    def __init__(self, items=None):
        self.items = items if items is not None else []  # Per-instance
```

**Lesson:** Python uses per-instance but mutable defaults are a famous pitfall.

---

### JavaScript

```javascript
// Per-instance
class Config {
    constructor(items = []) {  // Fresh array each time
        this.items = items;
    }
}
```

**Lesson:** JavaScript uses per-instance, works well.

---

### Go

```go
// No defaults - use factory functions
type Config struct {
    Items []string
}

func NewConfig() Config {
    return Config{
        Items: make([]string, 0),  // Fresh slice
    }
}
```

**Lesson:** Go has no defaults, forces factory functions (Option 4 workaround).

---

### Rust

```rust
// Derive Default trait
#[derive(Default)]
struct Config {
    items: Vec<String>,  // Empty vec on Default::default()
}
```

**Lesson:** Rust uses trait-based defaults, effectively per-instance.

---

### TypeScript

```typescript
class Config {
    items: string[] = [];  // Per-instance (fresh array each time)
}
```

**Lesson:** TypeScript uses per-instance.

---

## Recommendation: Option 2 (Per-Instance)

### Why Per-Instance?

1. **Safety First** - No shared mutable state
2. **Developer Expectations** - Matches all major languages (JS, TS, Rust)
3. **Correctness** - Dynamic defaults work correctly
4. **Simplicity** - No complex lazy evaluation
5. **Security** - Unpredictable UUIDs, timestamps

### Performance Concerns Addressed

**Q: Won't this be slow?**

A: Not significantly:

```ml
// Expensive default example
struct Connection {
    socket = expensive_connect()  // Evaluated each time
}

// If performance matters, don't use defaults:
struct Connection {
    socket  // No default
}

function connect(): Connection {
    socket = expensive_connect();  // Explicit, clear cost
    return Connection{socket: socket};
}
```

**Rule:** Use defaults for **cheap** values (primitives, empty arrays). For expensive operations, use explicit factory functions.

---

## Specification

### Default Value Semantics (FINAL)

**Evaluation Timing:** Per-Instance (Constructor Pattern)

**Rule:** Default expressions are evaluated **each time** a struct instance is created.

**Examples:**

```ml
// Primitives - safe and cheap
struct Config {
    host: string = "localhost",     // String literal
    port: number = 8080,             // Number literal
    debug: boolean = false           // Boolean literal
}

// Empty collections - safe
struct Container {
    items: array = [],               // Fresh empty array each time
    data: object = {}                // Fresh empty object each time
}

// Dynamic values - correct behavior
struct Event {
    id: string = generate_uuid(),    // Different UUID per instance
    timestamp: number = time.now(),  // Different timestamp per instance
    counter: number = random.randint(1, 100)  // Different random number
}

// Nested structs - fresh instances
struct Point { x: number = 0, y: number = 0 }
struct Circle {
    center: Point = Point{},         // Fresh Point instance each time
    radius: number = 1.0
}
```

**Test Case:**

```ml
struct Counter {
    value: number = random.randint(1, 100),
    items: array = []
}

c1 = Counter{};
c2 = Counter{};

// Different random values
print(c1.value == c2.value);  // false (different random numbers)

// Separate arrays
c1.items.append(1);
print(len(c2.items));  // 0 (c2.items is separate array)
```

---

## Implementation

### Python Code Generation

**ML Code:**
```ml
struct Config {
    host: string = "localhost",
    port: number = 8080,
    items: array = []
}
```

**Generated Python:**
```python
@dataclass
class Config:
    host: str = None
    port: Union[int, float] = None
    items: list = None

    def __post_init__(self):
        # Evaluate defaults per-instance
        if self.host is None:
            self.host = "localhost"  # Constant literal

        if self.port is None:
            self.port = 8080  # Constant literal

        if self.items is None:
            self.items = []  # Fresh list each time

        # Type checking
        _check_type(self.host, 'string', 'Config.host')
        _check_type(self.port, 'number', 'Config.port')
```

**For dynamic defaults:**
```ml
struct Event {
    id: string = generate_uuid()
}
```

**Generated Python:**
```python
@dataclass
class Event:
    id: str = None

    def __post_init__(self):
        if self.id is None:
            self.id = generate_uuid()  # Evaluated per-instance

        _check_type(self.id, 'string', 'Event.id')
```

---

## Edge Cases

### 1. Expensive Defaults

**Problem:**
```ml
struct Connection {
    socket = expensive_connect()  // Slow!
}

// Every instance creation is slow
c1 = Connection{};  // Slow
c2 = Connection{};  // Slow
```

**Solution:** Document best practice - don't use defaults for expensive operations.

**Recommended:**
```ml
struct Connection {
    socket  // No default
}

function connect(): Connection {
    socket = expensive_connect();  // Explicit, clear
    return Connection{socket: socket};
}
```

---

### 2. Side Effects

**Problem:**
```ml
counter = 0;

struct Event {
    id: number = (counter = counter + 1)  // Side effect!
}

e1 = Event{};  // counter = 1
e2 = Event{};  // counter = 2
```

**Solution:** Document that defaults can have side effects, use with caution.

---

### 3. Recursive Defaults

**Problem:**
```ml
struct Node {
    value: number = 0,
    next: Node = Node{}  // Infinite recursion!
}
```

**Solution:** Runtime error on infinite recursion.

---

## Documentation Updates

### Add to Proposal

**Section:** "Default Field Values"

**Content:**

```markdown
### Default Value Semantics

**Evaluation Timing:** Per-Instance

Default expressions are evaluated **each time** a struct instance is created, not when the struct is defined.

**Rationale:**
- Safe for mutable defaults (each instance gets fresh array/object)
- Dynamic values work correctly (different UUID per instance)
- Matches developer expectations from other languages (JavaScript, TypeScript, Rust)

**Examples:**

```ml
struct Config {
    id: string = generate_uuid(),    // Different UUID each time
    timestamp: number = time.now(),  // Different timestamp each time
    items: array = []                // Fresh array each time
}

c1 = Config{};
c2 = Config{};

print(c1.id == c2.id);  // false (different UUIDs)
c1.items.append(1);
print(c2.items);        // [] (separate arrays)
```

**Best Practices:**

1. **Use defaults for cheap values:**
   - Primitives: `port: number = 8080`
   - Empty collections: `items: array = []`
   - Small objects: `point: Point = Point{}`

2. **Avoid defaults for expensive operations:**
   ```ml
   // Don't do this
   struct Connection {
       socket = expensive_connect()  // Evaluated every time!
   }

   // Do this instead
   function connect(): Connection {
       socket = expensive_connect();
       return Connection{socket: socket};
   }
   ```

3. **Be aware of side effects:**
   - Defaults can have side effects
   - Executed on every instance creation
   - Use caution with stateful defaults
```

---

## Summary

**Decision:** Per-Instance Evaluation (Option 2)

**Rationale:**
- ✅ Safe for mutable defaults
- ✅ Intuitive for developers
- ✅ Matches industry standards
- ✅ Correct dynamic value behavior
- ✅ Simple implementation

**Trade-offs:**
- ⚠️ Slight performance cost (acceptable)
- ⚠️ Can't use for expensive defaults (use factory functions instead)

**Implementation:**
- Evaluate defaults in `__post_init__` (Python)
- Generate code to check if field is None, then evaluate default
- Document best practices for cheap vs expensive defaults

**Status:** Ready for proposal update
