# Default Value Semantics: Final Decision

**Date:** November 5, 2025
**Issue:** Default field value evaluation timing
**Decision:** Per-Instance Evaluation
**Status:** RESOLVED ✅

---

## Executive Summary

**Decision:** Default expressions are evaluated **each time** a struct instance is created (per-instance evaluation).

**Why:** Safe for mutable defaults, intuitive, matches industry standards (JavaScript, TypeScript, Rust).

---

## The Question

```ml
struct Config {
    id: string = generate_uuid(),
    items: array = []
}

c1 = Config{};
c2 = Config{};

// Are c1.id and c2.id the same or different?
```

---

## The Answer

**Different!** Each instance gets a fresh evaluation of defaults.

```ml
print(c1.id == c2.id);  // false (different UUIDs)
c1.items.append(1);
print(c2.items);        // [] (separate arrays)
```

---

## Why Per-Instance?

### ✅ Safety

No shared mutable state:

```ml
struct TodoList {
    items: array = []
}

list1 = TodoList{};
list2 = TodoList{};

list1.items.append("Buy milk");
print(list2.items);  // [] ✅ Correct (separate arrays)

// If per-struct evaluation:
// print(list2.items);  // ["Buy milk"] ❌ WRONG! (shared array)
```

---

### ✅ Dynamic Values Work

```ml
struct Event {
    id: string = generate_uuid(),
    timestamp: number = time.now()
}

e1 = Event{};
e2 = Event{};

print(e1.id == e2.id);  // false ✅ Different UUIDs
print(e1.timestamp == e2.timestamp);  // false ✅ Different timestamps
```

---

### ✅ Matches Industry Standards

| Language | Evaluation | Example |
|----------|-----------|---------|
| **JavaScript** | Per-instance | `items = []` → fresh array |
| **TypeScript** | Per-instance | `items: string[] = []` → fresh array |
| **Rust** | Per-instance | `#[derive(Default)]` → fresh values |
| **Python** | Per-instance (recommended) | `def __init__(self, items=None): self.items = items or []` |
| **Go** | N/A (no defaults) | Use factory functions |

ML aligns with modern language design.

---

### ✅ Intuitive for Developers

When developers write:

```ml
items: array = []
```

They expect **each instance** to get its own empty array, not share one array across all instances.

Per-instance evaluation matches this expectation.

---

## Rejected Alternatives

### ❌ Per-Struct Evaluation

**Problem:** Shared mutable state

```ml
// All instances share same array - DANGEROUS!
struct Config {
    items: array = []
}

c1 = Config{};
c2 = Config{};
c1.items.append(1);
print(c2.items);  // [1] ❌ Unexpected!
```

This is Python's infamous mutable default argument pitfall. We explicitly avoid it.

---

### ❌ Lazy Evaluation

**Problem:** Complex, non-obvious timing

```ml
struct Config {
    connection = expensive_connect()  // When is this called?
}

c = Config{};
// Has expensive_connect() run yet? Unclear!

c.connection.send("data");  // Does it run now?
```

Too complex for developers to reason about.

---

### 🟡 Constants Only

**Alternative:** Only allow literal constants as defaults

```ml
// Allowed
host: string = "localhost"
port: number = 8080

// Forbidden
id: string = generate_uuid()  // ERROR: Not a constant
```

**Pros:** Simple, no evaluation issues

**Cons:** Too limited, forces workarounds

**Status:** Viable alternative, but less convenient than per-instance

---

## Implementation

### Python Code Generation

**ML Code:**
```ml
struct Event {
    id: string = generate_uuid(),
    items: array = []
}
```

**Generated Python:**
```python
@dataclass
class Event:
    id: str = None
    items: list = None

    def __post_init__(self):
        # Evaluate defaults per-instance
        if self.id is None:
            self.id = generate_uuid()  # Called EACH TIME

        if self.items is None:
            self.items = []  # Fresh array EACH TIME

        # Type checking
        _check_type(self.id, 'string', 'Event.id')
```

---

## Best Practices

### ✅ Good: Use Defaults for Cheap Values

```ml
struct Config {
    host: string = "localhost",     // ✅ Constant literal
    port: number = 8080,             // ✅ Constant literal
    debug: boolean = false,          // ✅ Constant literal
    items: array = [],               // ✅ Cheap (empty array)
    metadata: object = {}            // ✅ Cheap (empty object)
}
```

---

### ⚠️ Caution: Dynamic Defaults Execute Every Time

```ml
struct Event {
    id: string = generate_uuid(),    // ⚠️ Runs on EVERY instance creation
    timestamp: number = time.now()   // ⚠️ Runs on EVERY instance creation
}

// This is fine - generate_uuid() and time.now() are cheap
```

---

### ❌ Bad: Expensive Defaults

```ml
// ❌ Bad: Expensive operation runs EVERY time
struct Service {
    connection = expensive_connect()  // Slow! Runs on every Service{}
}

// Every instance creation is slow:
s1 = Service{};  // Slow (calls expensive_connect)
s2 = Service{};  // Slow (calls expensive_connect)
s3 = Service{};  // Slow (calls expensive_connect)
```

**Solution:** Use factory function instead:

```ml
// ✅ Good: Explicit factory function
struct Service {
    connection  // No default
}

function new_service(): Service {
    conn = expensive_connect();  // Clear, explicit cost
    return Service{connection: conn};
}

s = new_service();  // Slow (expected)
```

---

### ⚠️ Side Effects Execute Every Time

```ml
counter = 0;

struct Event {
    id: number = (counter = counter + 1)  // Side effect!
}

e1 = Event{};  // counter = 1
e2 = Event{};  // counter = 2
e3 = Event{};  // counter = 3
```

This is allowed but use with caution. Side effects make code harder to reason about.

---

## Edge Cases

### 1. Recursive Defaults

```ml
struct Node {
    value: number = 0,
    next: Node = Node{}  // Infinite recursion!
}

n = Node{};  // ERROR: Stack overflow
```

**Solution:** Runtime error on infinite recursion detection.

---

### 2. Defaults Referencing Other Fields

```ml
struct Rectangle {
    width: number,
    height: number,
    area: number = width * height  // ERROR: Can't reference other fields
}
```

**Solution:** Compile error - defaults can't reference other fields (fields don't exist yet during default evaluation).

**Workaround:** Use method or property:

```ml
struct Rectangle {
    width: number,
    height: number
}

function (r: Rectangle) area(): number {
    return r.width * r.height;
}
```

---

## Documentation Updates

### Added to Proposal

**Section:** "Language Features → Struct Definitions → Default Field Values"

**Key points added:**
1. Per-instance evaluation semantics
2. Code examples showing separate instances
3. Best practices (cheap vs expensive defaults)
4. Side effect warnings
5. Rationale for decision

**Cross-references:**
- `default-semantics-analysis.md` - Full analysis of all options
- `default-semantics-decision.md` - This document

---

## Summary

| Question | Answer |
|----------|--------|
| **When are defaults evaluated?** | Each time an instance is created |
| **Are mutable defaults safe?** | Yes (each instance gets fresh copy) |
| **Do dynamic values work?** | Yes (generate_uuid() different each time) |
| **Performance cost?** | Minimal (only affects instance creation) |
| **What about expensive defaults?** | Use factory functions instead |
| **Any language precedent?** | Yes (JavaScript, TypeScript, Rust) |

---

## Final Verdict

**Decision:** ✅ Per-Instance Evaluation

**Rationale:**
- Safe for mutable defaults
- Intuitive for developers
- Matches industry standards
- Correct dynamic value behavior
- Simple implementation

**Status:** RESOLVED and documented in proposal

**Date:** November 5, 2025
