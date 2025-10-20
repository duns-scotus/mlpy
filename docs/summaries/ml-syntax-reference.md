# ML Language Syntax Reference

**Created:** January 20, 2026
**Purpose:** Quick reference for ML language syntax based on grammar analysis and working test examples
**Sources:** `src/mlpy/ml/grammar/ml.lark`, `tests/ml_integration/ml_core/*.ml`, `tests/ml_integration/ml_builtin/*.ml`

---

## Core Syntax Rules

### Variable Declaration & Assignment

ML does **not** use a `let`, `var`, or `const` keyword. Variables are declared through direct assignment.

```ml
// Simple assignment
x = 5;
name = "Alice";
result = calculate(10, 20);

// Assignment to object properties
obj.property = value;
person.name = "Bob";

// Assignment to array elements
arr[0] = value;
arr[i] = i * 2;
```

**Common Mistake:**
```ml
let x = 5;        // ❌ WRONG - 'let' is not a keyword in ML
const name = "A"; // ❌ WRONG - 'const' is not a keyword in ML
x = 5;            // ✅ CORRECT
```

---

### Comments

ML supports **single-line comments only** using `//`.

```ml
// This is a comment
x = 5; // Inline comment

// Multi-line documentation
// must be written as multiple
// single-line comments
```

**Note:** Multi-line comments (`/* */`) are **not supported**.

---

### Functions

#### Named Functions

```ml
function add(a, b) {
    return a + b;
}

function fibonacci(n) {
    if (n <= 1) {
        return n;
    } else {
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
}

// Functions can have optional type annotations
function process(data: DataType) {
    return transform(data);
}
```

#### Arrow Functions

Arrow functions **require** the `fn` keyword:

```ml
// Simple arrow function
squared = fn(x) => x * x;

// Arrow function with block body
process = fn(data) => {
    result = transform(data);
    validated = check(result);
    return validated;
};

// Multiple parameters
add = fn(a, b) => a + b;
```

**Common Mistake:**
```ml
squared = (x) => x * x;      // ❌ WRONG - missing 'fn' keyword
squared = fn(x) => x * x;    // ✅ CORRECT
```

---

### Control Flow

#### If/Elif/Else

```ml
if (x < 0) {
    return "negative";
} elif (x == 0) {
    return "zero";
} elif (x < 10) {
    return "small";
} else {
    return "positive";
}

// Nested conditions
if (a > 0) {
    if (b > 0) {
        return "both positive";
    } else {
        return "a positive";
    }
} else {
    return "a non-positive";
}
```

**Note:** Use `elif`, not `else if`.

#### While Loop

```ml
i = 0;
sum = 0;
while (i < 10) {
    sum = sum + i;
    i = i + 1;
}
```

#### For-In Loop

```ml
// Iterate over arrays
for (item in array) {
    process(item);
}

// Iterate with index tracking
i = 0;
for (value in data) {
    results[i] = transform(value);
    i = i + 1;
}
```

#### Break and Continue

```ml
// Break from loop
while (true) {
    if (condition) {
        break;
    }
}

// Continue to next iteration
for (item in items) {
    if (skip_condition) {
        continue;
    }
    process(item);
}
```

---

### Exception Handling

```ml
try {
    risky_operation();
    process_data();
} except (e) {
    handle_error(e);
} finally {
    cleanup();
}

// Exception without binding
try {
    operation();
} except {
    handle();
}
```

**Common Mistake:**
```ml
except e {        // ❌ WRONG - missing parentheses
except (e) {      // ✅ CORRECT
```

---

### Data Structures

#### Arrays

```ml
// Array literals
arr = [1, 2, 3, 4, 5];
empty = [];
mixed = [1, "text", true, {key: "value"}];

// Array access
x = arr[0];
last = arr[4];

// Array slicing
subset = arr[1:3];      // Elements from index 1 to 2
all = arr[:];           // Copy entire array
from_start = arr[:3];   // First 3 elements
to_end = arr[2:];       // From index 2 to end
```

#### Objects

```ml
// Object literals
person = {name: "Alice", age: 30};
nested = {data: {value: 42, status: "ok"}};

// Property access
name = person.name;
value = nested.data.value;

// Property assignment
person.age = 31;
obj.newField = "value";
```

#### Destructuring

```ml
// Array destructuring
[a, b, c] = [1, 2, 3];

// Object destructuring
{name, age} = person;
```

---

### Operators

#### Arithmetic Operators

```ml
// Basic arithmetic
sum = a + b;
difference = a - b;
product = a * b;
quotient = a / b;
remainder = a % b;
floor_div = a // b;  // Integer division
```

**IMPORTANT:** ML does **not** have a `**` power operator.

```ml
// Power operations
x = 2 * 2 * 2;           // ✅ Manual multiplication
x = math.pow(2, 3);      // ✅ Using math module

x = 2 ** 3;              // ❌ WRONG - syntax error
```

#### Comparison Operators

```ml
// Equality
equal = (a == b);
not_equal = (a != b);

// Relational
less = (a < b);
greater = (a > b);
less_eq = (a <= b);
greater_eq = (a >= b);
```

#### Logical Operators

```ml
// Boolean logic
and_result = (a && b);
or_result = (a || b);
not_result = !condition;

// Complex conditions
if (x > 0 && x < 10 || x == 100) {
    // ...
}
```

#### Ternary Operator

```ml
result = condition ? value_if_true : value_if_false;
max = (a > b) ? a : b;
```

#### String Concatenation

```ml
// String concatenation with +
message = "Hello " + name + "!";
display = "Value: " + str(number);

// Must convert non-strings
text = "Count: " + str(42);  // ✅ CORRECT
text = "Count: " + 42;        // ❌ May cause errors
```

---

### Built-in Functions

These functions are **automatically available** without imports:

```ml
// Type conversion
x = int("42");           // String to integer
y = float("3.14");       // String to float
s = str(100);            // Number to string
b = bool(value);         // Any value to boolean

// Output
print("Hello World");
print("Value: " + str(x));

// Type checking
t = typeof(value);       // Returns: "number", "string", "boolean", "array", "object", "function"

// Array/String length (via try-catch or iteration)
function get_length(arr) {
    len = 0;
    try {
        i = 0;
        while (true) {
            temp = arr[i];
            i = i + 1;
            len = len + 1;
        }
    } except {
        // Out of bounds
    }
    return len;
}
```

---

### Importing Modules

```ml
// Simple import
import math;
result = math.pow(2, 10);

// Import with alias
import string as str_utils;
text = str_utils.upper("hello");

// Import multiple modules
import math;
import string;
import datetime;
```

**Standard Library Modules:**
- `math` - Mathematical functions
- `string` - String manipulation
- `datetime` - Date and time operations
- `regex` - Regular expressions
- `functional` - Functional programming utilities

---

## Common Pitfalls & Corrections

### 1. Variable Declaration

| ❌ Wrong | ✅ Correct |
|---------|-----------|
| `let x = 5;` | `x = 5;` |
| `const name = "A";` | `name = "A";` |
| `var count = 0;` | `count = 0;` |

### 2. Arrow Functions

| ❌ Wrong | ✅ Correct |
|---------|-----------|
| `f = (x) => x * 2` | `f = fn(x) => x * 2` |
| `(a, b) => a + b` | `fn(a, b) => a + b` |

### 3. Power Operator

| ❌ Wrong | ✅ Correct |
|---------|-----------|
| `x ** 2` | `x * x` |
| `base ** exp` | `math.pow(base, exp)` |
| `2 ** 10` | `math.pow(2, 10)` |

### 4. Exception Handling

| ❌ Wrong | ✅ Correct |
|---------|-----------|
| `except e {` | `except (e) {` |
| `catch (e) {` | `except (e) {` |

### 5. Control Flow Keywords

| ❌ Wrong | ✅ Correct |
|---------|-----------|
| `else if (...)` | `elif (...)` |
| `elseif (...)` | `elif (...)` |

### 6. Semicolons

All statements **must** end with a semicolon:

```ml
x = 5        // ❌ Missing semicolon
x = 5;       // ✅ Correct

return x     // ❌ Missing semicolon
return x;    // ✅ Correct
```

### 7. String Concatenation

```ml
// Must convert numbers to strings
msg = "Count: " + 42;         // ❌ May fail
msg = "Count: " + str(42);    // ✅ Correct

// Concatenate strings
text = "Hello" + " " + "World";  // ✅ Works
```

---

## Grammar Summary

### Statement Types

- Expression statements: `expression;`
- Assignments: `target = expression;`
- Function definitions: `function name(params) { ... }`
- Control flow: `if/elif/else`, `while`, `for`
- Exception handling: `try/except/finally`
- Loop control: `break;`, `continue;`
- Scope control: `nonlocal var1, var2;`
- Return: `return expression;`
- Throw: `throw {message: "error"};`

### Expression Precedence (highest to lowest)

1. Primary: literals, identifiers, calls, access, `(expr)`
2. Unary: `!`, `-`
3. Multiplication: `*`, `/`, `//`, `%`
4. Addition: `+`, `-`
5. Comparison: `<`, `>`, `<=`, `>=`
6. Equality: `==`, `!=`
7. Logical AND: `&&`
8. Logical OR: `||`
9. Ternary: `? :`

---

## Integration with Python

### Transpiler API

```python
from mlpy.ml.transpiler import MLTranspiler

transpiler = MLTranspiler()

# Transpile ML code
python_code, issues, source_map = transpiler.transpile_to_python(
    ml_code,
    strict_security=False  # Allow warnings
)

if python_code:
    # Execute transpiled code
    exec(python_code)
```

### Error Handling

```python
from mlpy.ml.errors.exceptions import MLError

try:
    python_code, issues, source_map = transpiler.transpile_to_python(ml_code)
except MLError as e:
    print(f"ML Error: {e}")
```

---

## References

- **Grammar File:** `src/mlpy/ml/grammar/ml.lark`
- **Core Tests:** `tests/ml_integration/ml_core/*.ml`
- **Builtin Tests:** `tests/ml_integration/ml_builtin/*.ml`
- **Examples:** `docs/examples/advanced/*.ml`

---

**Document Status:** Complete
**Last Updated:** January 20, 2026
**Maintained By:** mlpy development team
