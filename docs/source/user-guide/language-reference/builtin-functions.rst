=================
Built-in Functions
=================

Built-in functions are core functions available in every ML program without requiring import statements. These functions provide essential capabilities for type conversion, collection manipulation, I/O operations, and more.

.. contents::
   :local:
   :depth: 2

What Are Built-in Functions?
=============================

Built-in functions are automatically available in every ML program. You don't need to import them - just use them directly:

::

    // No import needed
    length = len([1, 2, 3]);  // 3
    text = str(42);            // "42"
    value = abs(-5);           // 5

ML's built-in functions are inspired by Python but adapted to ML's syntax and security model.

Type Conversion Functions
==========================

Convert values between different types.

int()
-----

Convert values to integers::

    int(3.14)       // 3
    int("42")       // 42
    int("3.9")      // 3 (parses as float first)
    int(true)       // 1
    int(false)      // 0
    int("invalid")  // 0 (on error)

**Syntax**: ``int(value)``

**Returns**: Integer representation, or 0 if conversion fails

float()
-------

Convert values to floating-point numbers::

    float(42)       // 42.0
    float("3.14")   // 3.14
    float(true)     // 1.0
    float(false)    // 0.0
    float("bad")    // 0.0 (on error)

**Syntax**: ``float(value)``

**Returns**: Float representation, or 0.0 if conversion fails

str()
-----

Convert values to strings::

    str(42)        // "42"
    str(3.14)      // "3.14"
    str(true)      // "true"
    str(false)     // "false"
    str([1, 2])    // "[1, 2]"

**Syntax**: ``str(value)``

**Returns**: String representation

**Note**: Booleans convert to "true"/"false" (lowercase), matching ML syntax.

bool()
------

Convert values to booleans::

    bool(1)         // true
    bool(0)         // false
    bool("")        // false
    bool("hello")   // true
    bool([])        // false
    bool([1])       // true

**Syntax**: ``bool(value)``

**Returns**: Boolean representation

**Falsy values**: 0, 0.0, "", [], {}, null

**Truthy values**: Everything else

Type Conversion Example
-----------------------

Here's a practical example using type conversions:

.. literalinclude:: ../../../ml_snippets/language-reference/builtin/01_type_conversion.ml
   :language: ml

Type Checking Functions
=======================

Check the type of values at runtime.

typeof()
--------

Get the type of a value::

    typeof(true)       // "boolean"
    typeof(42)         // "number"
    typeof(3.14)       // "number"
    typeof("hello")    // "string"
    typeof([1, 2])     // "array"
    typeof({a: 1})     // "object"
    typeof(fn() => 1)  // "function"

**Syntax**: ``typeof(value)``

**Returns**: Type name string

**Type names**:
- ``"boolean"`` - true or false
- ``"number"`` - integers and floats
- ``"string"`` - text
- ``"array"`` - lists
- ``"object"`` - dictionaries
- ``"function"`` - functions
- ``"unknown"`` - unrecognized types

isinstance()
------------

Check if a value is a specific type::

    isinstance(42, "number")          // true
    isinstance("hello", "string")     // true
    isinstance([1, 2], "array")       // true
    isinstance({a: 1}, "object")      // true
    isinstance(42, "string")          // false

**Syntax**: ``isinstance(value, type_name)``

**Returns**: true if value is of given type, false otherwise

Type Checking Example
---------------------

Here's how to use type checking in practice:

.. literalinclude:: ../../../ml_snippets/language-reference/builtin/02_type_checking.ml
   :language: ml

Collection Functions
====================

Work with arrays, strings, and objects.

len()
-----

Get the length of a collection::

    len("hello")        // 5
    len([1, 2, 3])      // 3
    len({a: 1, b: 2})   // 2
    len("")             // 0
    len([])             // 0

**Syntax**: ``len(collection)``

**Returns**: Number of elements/characters

**Works with**: Strings, arrays, objects

range()
-------

Generate a range of numbers::

    range(5)           // [0, 1, 2, 3, 4]
    range(2, 5)        // [2, 3, 4]
    range(0, 10, 2)    // [0, 2, 4, 6, 8]
    range(5, 0, -1)    // [5, 4, 3, 2, 1]

**Syntax**:
- ``range(stop)`` - 0 to stop (exclusive)
- ``range(start, stop)`` - start to stop (exclusive)
- ``range(start, stop, step)`` - with custom step

**Returns**: Array of numbers

enumerate()
-----------

Get index-value pairs from an array::

    letters = ["a", "b", "c"];
    enumerate(letters)  // [(0, "a"), (1, "b"), (2, "c")]

    enumerate(letters, 1)  // [(1, "a"), (2, "b"), (3, "c")]

**Syntax**: ``enumerate(array, start=0)``

**Returns**: Array of (index, value) tuples

keys()
------

Get all keys from an object::

    obj = {name: "Alice", age: 30};
    keys(obj)  // ["name", "age"]

**Syntax**: ``keys(object)``

**Returns**: Array of key strings

values()
--------

Get all values from an object::

    obj = {name: "Alice", age: 30};
    values(obj)  // ["Alice", 30]

**Syntax**: ``values(object)``

**Returns**: Array of values

Collection Functions Example
-----------------------------

Here's a comprehensive example using collection functions:

.. literalinclude:: ../../../ml_snippets/language-reference/builtin/03_collections.ml
   :language: ml

Math Functions
==============

Mathematical operations and utilities.

abs()
-----

Get absolute value::

    abs(-5)     // 5
    abs(3.14)   // 3.14
    abs(-2.5)   // 2.5

**Syntax**: ``abs(number)``

**Returns**: Absolute value (non-negative)

min()
-----

Get minimum value::

    min(1, 2, 3)      // 1
    min([5, 2, 8])    // 2
    min(-10, 5)       // -10

**Syntax**:
- ``min(value1, value2, ...)`` - minimum of arguments
- ``min(array)`` - minimum of array elements

**Returns**: Minimum value

max()
-----

Get maximum value::

    max(1, 2, 3)      // 3
    max([5, 2, 8])    // 8
    max(-10, 5)       // 5

**Syntax**:
- ``max(value1, value2, ...)`` - maximum of arguments
- ``max(array)`` - maximum of array elements

**Returns**: Maximum value

round()
-------

Round number to precision::

    round(3.14159)      // 3.0
    round(3.14159, 2)   // 3.14
    round(3.14159, 4)   // 3.1416
    round(2.5)          // 2.0

**Syntax**: ``round(number, precision=0)``

**Returns**: Rounded number

sum()
-----

Sum numeric values::

    sum([1, 2, 3])        // 6
    sum([1.5, 2.5, 3])    // 7.0
    sum([1, 2, 3], 10)    // 16 (with start value)

**Syntax**: ``sum(array, start=0)``

**Returns**: Sum of all values plus start

Math Functions Example
----------------------

Here's a practical math example:

.. literalinclude:: ../../../ml_snippets/language-reference/builtin/04_math_functions.ml
   :language: ml

Array Functions
===============

Additional array manipulation functions.

sorted()
--------

Return sorted copy of array::

    sorted([3, 1, 2])          // [1, 2, 3]
    sorted([3, 1, 2], true)    // [3, 2, 1] (descending)
    sorted(["c", "a", "b"])    // ["a", "b", "c"]

**Syntax**: ``sorted(array, reverse=false)``

**Returns**: New sorted array (original unchanged)

reversed()
----------

Return reversed sequence::

    reversed([1, 2, 3])    // [3, 2, 1]
    reversed("hello")      // ["o", "l", "l", "e", "h"]

**Syntax**: ``reversed(sequence)``

**Returns**: Reversed array

zip()
-----

Combine multiple arrays::

    zip([1, 2, 3], ["a", "b", "c"])
    // [(1, "a"), (2, "b"), (3, "c")]

    names = ["Alice", "Bob"];
    ages = [30, 25];
    zip(names, ages)  // [("Alice", 30), ("Bob", 25)]

**Syntax**: ``zip(array1, array2, ...)``

**Returns**: Array of tuples

all()
-----

Check if all elements are truthy::

    all([true, true, true])     // true
    all([true, false, true])    // false
    all([1, 2, 3])              // true
    all([1, 0, 3])              // false

**Syntax**: ``all(array)``

**Returns**: true if all elements truthy

any()
-----

Check if any element is truthy::

    any([false, false, true])   // true
    any([false, false, false])  // false
    any([0, 0, 1])              // true

**Syntax**: ``any(array)``

**Returns**: true if any element truthy

Array Functions Example
-----------------------

Here's a comprehensive array processing example:

.. literalinclude:: ../../../ml_snippets/language-reference/builtin/05_array_functions.ml
   :language: ml

I/O Functions
=============

Input and output operations.

print()
-------

Print values to console::

    print("Hello, World!");
    print("Score:", 42);
    print("Value:", true);  // prints "Value: true"

**Syntax**: ``print(value1, value2, ...)``

**Output**: Prints values separated by spaces, followed by newline

**Note**: Booleans print as "true"/"false" (lowercase)

input()
-------

Read input from console::

    name = input("Enter your name: ");
    age = input("Enter age: ");
    ageNum = int(age);  // Convert to number

**Syntax**: ``input(prompt="")``

**Returns**: User input as string

**Note**: Always returns string. Use int() or float() to convert.

I/O Example
-----------

Here's an interactive program using I/O:

.. literalinclude:: ../../../ml_snippets/language-reference/builtin/06_io_functions.ml
   :language: ml

String Conversion Functions
============================

Convert characters and numbers.

chr()
-----

Convert code point to character::

    chr(65)     // "A"
    chr(97)     // "a"
    chr(48)     // "0"
    chr(8364)   // "€"

**Syntax**: ``chr(code_point)``

**Returns**: Character string

ord()
-----

Convert character to code point::

    ord("A")    // 65
    ord("a")    // 97
    ord("0")    // 48
    ord("€")    // 8364

**Syntax**: ``ord(character)``

**Returns**: Unicode code point integer

hex()
-----

Convert integer to hexadecimal::

    hex(255)    // "0xff"
    hex(16)     // "0x10"
    hex(0)      // "0x0"

**Syntax**: ``hex(number)``

**Returns**: Hexadecimal string with "0x" prefix

bin()
-----

Convert integer to binary::

    bin(10)     // "0b1010"
    bin(255)    // "0b11111111"
    bin(0)      // "0b0"

**Syntax**: ``bin(number)``

**Returns**: Binary string with "0b" prefix

oct()
-----

Convert integer to octal::

    oct(8)      // "0o10"
    oct(64)     // "0o100"
    oct(0)      // "0o0"

**Syntax**: ``oct(number)``

**Returns**: Octal string with "0o" prefix

format()
--------

Format values with format specifiers::

    format(3.14159, ".2f")      // "3.14"
    format(42, "05d")           // "00042"
    format(255, "x")            // "ff"
    format(1000000, ",")        // "1,000,000"

**Syntax**: ``format(value, format_spec)``

**Returns**: Formatted string

**Common format specs**:
- ``.2f`` - 2 decimal places
- ``05d`` - pad with zeros to width 5
- ``x`` - hexadecimal (lowercase)
- ``X`` - hexadecimal (uppercase)
- ``,`` - thousands separator

String Conversion Example
-------------------------

Here's a comprehensive string conversion example:

.. literalinclude:: ../../../ml_snippets/language-reference/builtin/07_string_conversions.ml
   :language: ml

Advanced Functions
==================

Introspection and advanced utilities.

callable()
----------

Check if object is callable::

    callable(print)           // true
    callable(fn() => 1)       // true
    callable(42)              // false
    callable("string")        // false

**Syntax**: ``callable(object)``

**Returns**: true if object is a function

help()
------

Get documentation for functions and modules::

    help(len)              // Shows len() documentation
    help(typeof)           // Shows typeof() documentation

**Syntax**: ``help(function_or_module)``

**Returns**: Documentation string

methods()
---------

List available methods for a value::

    methods("hello")       // ["upper", "lower", "split", ...]
    methods([1, 2, 3])     // Array methods
    methods({a: 1})        // Object methods

**Syntax**: ``methods(value)``

**Returns**: Array of method names

modules()
---------

List all imported modules::

    import console;
    import math;
    modules()  // ["console", "math", ...]

**Syntax**: ``modules()``

**Returns**: Array of module names

iter() and next()
-----------------

Create and consume iterators::

    // Create iterator
    it = iter([1, 2, 3]);

    // Get elements
    next(it)        // 1
    next(it)        // 2
    next(it)        // 3
    next(it, null)  // null (exhausted, returns default)

**Syntax**:
- ``iter(sequence)`` - create iterator
- ``next(iterator, default)`` - get next item

**Returns**: Next item, or default if exhausted

**Best practice**: Always provide default to next() to avoid errors

Secure Introspection
====================

ML provides secure introspection that prevents access to dangerous attributes.

hasattr()
---------

Check if object has safe attribute::

    hasattr("hello", "upper")      // true
    hasattr("hello", "lower")      // true
    hasattr("hello", "__class__")  // false (blocked)

**Syntax**: ``hasattr(object, attribute_name)``

**Returns**: true if safe attribute exists

**Security**: Blocks all dunder attributes (``__class__``, ``__dict__``, etc.)

getattr()
---------

Get safe attribute from object::

    getattr("hello", "upper")         // <function>
    getattr("hello", "__class__", 0)  // 0 (blocked)
    getattr(obj, "missing", null)     // null (default)

**Syntax**: ``getattr(object, name, default=null)``

**Returns**: Attribute value if safe, default otherwise

**Security**: Only allows access to whitelisted safe attributes

Comprehensive Built-in Functions Example
=========================================

Here's a complete program demonstrating many built-in functions working together:

.. literalinclude:: ../../../ml_snippets/language-reference/builtin/08_comprehensive_example.ml
   :language: ml

This example demonstrates:

* **Type Conversion**: Converting user input to appropriate types
* **Type Checking**: Validating data types with typeof() and isinstance()
* **Collections**: Processing arrays with len(), range(), enumerate()
* **Math**: Statistical calculations with sum(), min(), max()
* **Array Functions**: Sorting, filtering, and transforming data
* **I/O**: Interactive user input and formatted output
* **String Conversions**: Formatting numbers and text
* **Utility Functions**: Using all(), any(), callable()

Summary
=======

ML built-in functions provide:

**Type Conversion**
- ``int()``, ``float()``, ``str()``, ``bool()`` - Convert between types

**Type Checking**
- ``typeof()``, ``isinstance()`` - Check value types

**Collections**
- ``len()``, ``range()``, ``enumerate()`` - Collection operations
- ``keys()``, ``values()`` - Object operations

**Math**
- ``abs()``, ``min()``, ``max()``, ``round()``, ``sum()`` - Numeric operations

**Arrays**
- ``sorted()``, ``reversed()``, ``zip()`` - Array transformations
- ``all()``, ``any()`` - Boolean checks

**I/O**
- ``print()``, ``input()`` - Console interaction

**String Conversions**
- ``chr()``, ``ord()`` - Character conversion
- ``hex()``, ``bin()``, ``oct()`` - Number base conversion
- ``format()`` - Format values

**Advanced**
- ``callable()``, ``help()``, ``methods()``, ``modules()`` - Introspection
- ``iter()``, ``next()`` - Iterator protocol
- ``hasattr()``, ``getattr()`` - Safe attribute access

Key points:

* Built-in functions are automatically available (no import needed)
* Type conversion functions return sensible defaults on error
* Collection functions work with strings, arrays, and objects
* Security-first design blocks dangerous introspection
* ML uses lowercase "true"/"false" in string conversions

For more advanced functionality, see :doc:`../standard-library/index`.
