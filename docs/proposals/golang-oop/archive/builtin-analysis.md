# Built-in Functions Analysis: Core vs Nice-to-Have

**Date:** November 5, 2025
**Purpose:** Determine minimal necessary built-ins for OOP implementation

---

## Current Proposal: 11 Built-ins

### Tier 1: CRITICAL (6 built-ins)
1. `typeof(value)` - Extended
2. `instanceof(obj, Type)`
3. `is_struct(obj)`
4. `fields(StructType)`
5. `same_type(obj1, obj2)`
6. `identity(obj)`

### Tier 2: HIGH (2 built-ins)
7. `field_types(StructType)`
8. `struct_type(obj)`

### Tier 3: MEDIUM (3 built-ins)
9. `new(Type, kwargs)`
10. `get_field(obj, name)`
11. `set_field(obj, name, val)`

---

## Analysis: Each Built-in

### 1. `typeof(value)` - KEEP ✅

**Status:** Already exists, just extend it

**Purpose:** Get type name
```ml
typeof(Point{x: 3, y: 4})  // "Point"
typeof({x: 3, y: 4})       // "object"
```

**Why KEEP:**
- Already exists in ML
- Zero new API surface
- Essential for type introspection
- No alternative exists

**Verdict:** ABSOLUTELY NECESSARY

---

### 2. `instanceof(obj, Type)` - KEEP ✅

**Purpose:** Check if object is instance of specific struct type
```ml
instanceof(point, Point)  // true
instanceof(plain, Point)  // false
```

**Why KEEP:**
- No alternative way to check "is this a Point instance?"
- Essential for type guards and validation
- Common pattern in OOP languages (Java, JavaScript, Python)
- Can't be implemented in userland (needs access to type metadata)

**Verdict:** ABSOLUTELY NECESSARY

---

### 3. `is_struct(obj)` - REMOVE ❌

**Purpose:** Check if object is any struct instance
```ml
is_struct(Point{x: 3, y: 4})  // true
is_struct({x: 3, y: 4})       // false
```

**Why REMOVE:**
- **REDUNDANT** with typeof()
- Can be implemented as: `typeof(obj) not in ["number", "string", "boolean", "array", "object"]`
- Or better: Check if typeof() returns a capitalized name (struct convention)

**Alternative:**
```ml
// Instead of: is_struct(obj)
// Use: typeof(obj) != "object" && typeof(obj) != "array" && ...

// Or add helper function in stdlib:
function is_struct(obj) {
    type = typeof(obj);
    // Structs start with uppercase by convention
    return type[0] >= "A" && type[0] <= "Z";
}
```

**Verdict:** REMOVE - Can be userland function

---

### 4. `fields(StructType)` - KEEP ✅

**Purpose:** Get field names from struct type
```ml
fields(Point)  // ["x", "y"]
```

**Why KEEP:**
- No alternative (needs type registry access)
- Essential for metaprogramming
- Enables generic operations
- Can't be implemented in userland

**Alternatives considered:**
- `keys(Point{...})` - NO, requires instance creation
- Reflection API - Too complex

**Verdict:** ABSOLUTELY NECESSARY

---

### 5. `same_type(obj1, obj2)` - KEEP ✅

**Purpose:** Check if two objects are same struct type
```ml
same_type(Point{x:1,y:2}, Point{x:3,y:4})  // true
same_type(Point{x:1,y:2}, Vector{x:1,y:2}) // false
```

**Why KEEP:**
- Critical for structural/nominal consistency
- Can't be easily implemented otherwise
- Common use case: filtering by type

**Could it be removed?**
```ml
// Alternative: typeof(obj1) == typeof(obj2)
same_type(p1, p2)  →  typeof(p1) == typeof(p2)
```

**Wait... this IS redundant!**

**Verdict:** REMOVE - Use `typeof(obj1) == typeof(obj2)`

---

### 6. `identity(obj)` - KEEP ✅

**Purpose:** Get unique identity hash for dict keys
```ml
cache[identity(point)] = "value"
```

**Why KEEP:**
- Critical for solving dict key collision with structural equality
- No alternative for identity-based caching
- Maps directly to Python's `id()`
- Can't be implemented in userland

**Verdict:** ABSOLUTELY NECESSARY (due to structural equality choice)

---

### 7. `field_types(StructType)` - KEEP (Phase 2) ⚠️

**Purpose:** Get field type annotations
```ml
field_types(Point)  // {x: "number", y: "number"}
```

**Why useful:**
- Runtime validation
- Documentation generation
- IDE tooling

**Why defer to Phase 2:**
- Not critical for MVP
- Complex implementation (needs type metadata)
- Limited use cases initially

**Verdict:** DEFER TO PHASE 2

---

### 8. `struct_type(obj)` - REMOVE ❌

**Purpose:** Get struct type name from instance
```ml
struct_type(point)  // "Point"
struct_type(plain)  // null
```

**Why REMOVE:**
- **TOTALLY REDUNDANT** with typeof()
- Literally the same: `struct_type(obj) === typeof(obj)`
- Confusing to have two functions for same thing

**Verdict:** REMOVE - Use `typeof(obj)`

---

### 9. `new(Type, kwargs)` - REMOVE ❌

**Purpose:** Create struct with defaults
```ml
new(Config, {port: 3000})
```

**Why REMOVE:**
- **REDUNDANT** with struct literals
- Struct literals already support defaults
- More verbose than struct syntax
- JavaScript tried this (`new Object()`), regretted it

**Alternative:**
```ml
// Instead of: new(Config, {port: 3000})
// Use: Config{port: 3000}  // Defaults applied automatically
```

**Verdict:** REMOVE - Use struct literals

---

### 10. `get_field(obj, name)` - REMOVE ❌

**Purpose:** Dynamic field access
```ml
get_field(point, "x")
```

**Why REMOVE:**
- **REDUNDANT** with bracket syntax
- ML likely already has this

**Alternative:**
```ml
// Instead of: get_field(obj, "x")
// Use: obj["x"]  // Standard bracket notation
```

**Verdict:** REMOVE - Use bracket notation

---

### 11. `set_field(obj, name, val)` - REMOVE ❌

**Purpose:** Dynamic field setting
```ml
set_field(point, "x", 10)
```

**Why REMOVE:**
- **REDUNDANT** with bracket assignment
- ML likely already has this

**Alternative:**
```ml
// Instead of: set_field(obj, "x", 10)
// Use: obj["x"] = 10  // Standard bracket assignment
```

**Verdict:** REMOVE - Use bracket notation

---

## Critical Missing Built-in: copy()

### Why `copy()` is ESSENTIAL

**Problem: Struct instances are mutable references**

```ml
p1 = Point{x: 3, y: 4};
p2 = p1;  // Reference copy or value copy?

p2.x = 10;
print(p1.x);  // 10 or 3? AMBIGUOUS!
```

**Without copy(), there's no way to duplicate a struct:**

```ml
// Want to create modified copy
point1 = Point{x: 3, y: 4};
point2 = ???  // How to copy point1?

// Manual field copying is terrible:
point2 = Point{x: point1.x, y: point1.y};  // Doesn't scale

// Need built-in:
point2 = copy(point1);
point2.x = 10;
print(point1.x);  // 3 (unchanged)
```

**Common use cases:**

1. **Immutable updates:**
```ml
function move_point(p: Point, dx: number, dy: number): Point {
    // Don't mutate input
    result = copy(p);
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
    // Store copy to prevent external mutation
    stored_config = copy(config);
    database.save(stored_config);
}
```

**Implementation:**

```python
def copy(obj):
    """Create shallow copy of struct or object."""
    if is_struct(obj):
        # Copy struct instance
        struct_type = type(obj)
        field_values = {field: getattr(obj, field) for field in fields(struct_type)}
        return struct_type(**field_values)
    else:
        # Copy plain object/dict
        return dict(obj)
```

**Variants to consider:**

1. **Shallow copy (RECOMMENDED FOR MVP):**
```ml
copy(obj)  // Copy top-level fields only
```

2. **Deep copy (Phase 2):**
```ml
deepcopy(obj)  // Recursively copy nested structs
```

**Verdict:** ADD `copy()` to Tier 1 CRITICAL

---

## Revised Built-in List

### MINIMAL CORE (4 built-ins)

| Built-in | Reason | Can't be removed because... |
|----------|--------|---------------------------|
| `typeof(value)` | Type introspection | Already exists, just extend it |
| `instanceof(obj, Type)` | Type checking | No way to check instance without it |
| `fields(Type)` | Metaprogramming | Needs type registry access |
| `identity(obj)` | Identity hashing | Needed for dict keys with structural equality |
| **`copy(obj)`** | **Struct copying** | **No way to duplicate structs otherwise** |

**Total: 5 built-ins** (down from 11)

---

### REMOVED (6 built-ins)

| Built-in | Why Removed | Alternative |
|----------|-------------|-------------|
| `is_struct(obj)` | Redundant | `typeof(obj)` or userland helper |
| `same_type(obj1, obj2)` | Redundant | `typeof(obj1) == typeof(obj2)` |
| `struct_type(obj)` | Redundant | `typeof(obj)` |
| `new(Type, kwargs)` | Redundant | `Type{...}` struct literals |
| `get_field(obj, name)` | Redundant | `obj[name]` bracket notation |
| `set_field(obj, name, val)` | Redundant | `obj[name] = val` bracket assignment |

---

### DEFERRED TO PHASE 2 (1 built-in)

| Built-in | Reason | When to add |
|----------|--------|-------------|
| `field_types(Type)` | Nice to have but not critical | Phase 2 or when users request it |

---

## Copy Semantics Deep Dive

### Should assignment be copy or reference?

**Option 1: Assignment is reference (RECOMMENDED)**
```ml
p1 = Point{x: 3, y: 4};
p2 = p1;  // Reference copy

p2.x = 10;
print(p1.x);  // 10 (both point to same object)
```

**Pros:**
- Matches Python, JavaScript, Java behavior
- More efficient (no copying)
- Predictable for developers with OOP background

**Cons:**
- Can surprise users expecting value semantics
- Mutations can affect multiple variables

---

**Option 2: Assignment is value copy**
```ml
p1 = Point{x: 3, y: 4};
p2 = p1;  // Value copy

p2.x = 10;
print(p1.x);  // 3 (separate objects)
```

**Pros:**
- More intuitive for functional programming
- No unexpected mutations

**Cons:**
- Performance overhead (copy on every assignment)
- Violates principle of least surprise for most devs
- Makes identity tracking impossible

---

**RECOMMENDATION: Option 1 (reference) with explicit copy()**

This is the standard for good reasons:
- Performance
- Matches developer expectations from other languages
- Allows both reference and value semantics via `copy()`

```ml
// Reference semantics (default)
p2 = p1;

// Value semantics (explicit)
p2 = copy(p1);
```

---

## Shallow vs Deep Copy

### Shallow Copy (RECOMMENDED FOR MVP)

```ml
struct Address { street: string, city: string }
struct Person { name: string, address: Address }

person1 = Person{
    name: "Alice",
    address: Address{street: "Main St", city: "NYC"}
};

person2 = copy(person1);
person2.name = "Bob";  // Independent

// BUT: address is still shared reference!
person2.address.city = "LA";
print(person1.address.city);  // "LA" (shared!)
```

**Pros:**
- Simple implementation
- Fast performance
- Predictable behavior

**Cons:**
- Nested structs are still shared references
- Can surprise users

---

### Deep Copy (Phase 2)

```ml
person2 = deepcopy(person1);
person2.address.city = "LA";
print(person1.address.city);  // "NYC" (independent)
```

**Pros:**
- Complete independence
- No shared references

**Cons:**
- Slower performance
- Complex implementation (circular references, etc.)
- Not always wanted (sometimes you want shallow copy)

---

**RECOMMENDATION:**
- **MVP:** Only `copy()` (shallow copy)
- **Phase 2:** Add `deepcopy()` if users request it

---

## Additional Missing Built-ins?

### freeze(obj) - Make immutable

**Use case:**
```ml
config = Config{host: "localhost", port: 8080};
frozen = freeze(config);

frozen.port = 3000;  // ERROR: Cannot modify frozen object
```

**Verdict:** Phase 2 - Nice to have but not critical

---

### merge(obj1, obj2) - Combine structs

**Use case:**
```ml
defaults = Config{host: "localhost", port: 8080};
overrides = {port: 3000};
result = merge(defaults, overrides);  // {host: "localhost", port: 3000}
```

**Verdict:** Phase 2 - Can be userland function

---

### equals(obj1, obj2) - Explicit equality

**Use case:**
```ml
// If we want both structural and nominal equality
equals(p1, p2, structural=true)   // Structural
equals(p1, p2, structural=false)  // Nominal
```

**Verdict:** NOT NEEDED - We have `==` (structural) and `===` (reference) and `instanceof()` (type)

---

## Final Recommendation

### Phase 1 MVP: 5 Built-ins

```ml
// Type introspection (1 - extended)
typeof(value)  // "Point", "object", "number", etc.

// Type checking (1 - new)
instanceof(obj, Type)  // Check if obj is Type instance

// Metaprogramming (1 - new)
fields(Type)  // ["x", "y"]

// Identity (1 - new)
identity(obj)  // Unique hash for dict keys

// Copying (1 - new) **CRITICAL ADDITION**
copy(obj)  // Shallow copy of struct
```

### Phase 2: Optional Additions

```ml
// Metadata (if requested)
field_types(Type)  // {x: "number", y: "number"}

// Deep copy (if requested)
deepcopy(obj)  // Recursive copy

// Immutability (if requested)
freeze(obj)  // Make immutable
```

### NOT ADDING (use alternatives)

```ml
// REMOVED: Use typeof() instead
is_struct(obj)  →  typeof(obj) not in primitives
same_type(obj1, obj2)  →  typeof(obj1) == typeof(obj2)
struct_type(obj)  →  typeof(obj)

// REMOVED: Use struct literals
new(Type, kwargs)  →  Type{...}

// REMOVED: Use bracket notation
get_field(obj, "x")  →  obj["x"]
set_field(obj, "x", 10)  →  obj["x"] = 10
```

---

## Summary

**From 11 built-ins → 5 built-ins (54% reduction)**

**Removed:** 6 redundant built-ins
**Deferred:** 1 nice-to-have (field_types)
**Added:** 1 critical missing built-in (copy)

**Result:** Lean, focused API with no redundancy.
