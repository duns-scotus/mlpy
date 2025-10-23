==========
Data Types
==========

ML has a dynamic type system. Variables don't have fixed types - they hold values, and each value has a type at runtime.

.. contents::
   :local:
   :depth: 2

Type System Overview
====================

ML provides seven types:

* **number** - Numeric values (integers and floating-point)
* **string** - Text sequences
* **boolean** - True or false values
* **null** - Absence of a value
* **array** - Ordered collections
* **object** - Key-value mappings
* **function** - Executable code

Dynamic Typing
--------------

Variables can hold any type and can change types during execution::

    x = 42;          // x is a number
    x = "hello";     // now x is a string
    x = [1, 2, 3];   // now x is an array

The ``typeof()`` function returns a value's type as a string::

    typeof(42)        // "number"
    typeof("hello")   // "string"
    typeof(true)      // "boolean"
    typeof([1, 2])    // "array"
    typeof({a: 1})    // "object"

Number Type
===========

The ``number`` type represents all numeric values. ML does not distinguish between integers and floating-point numbers.

Integer Values
--------------

Write integers without a decimal point::

    0
    42
    -100
    1000000

All integers are stored as numbers internally.

Floating-Point Values
---------------------

Use a decimal point for floating-point values::

    3.14
    -0.5
    2.0
    0.001

Scientific Notation
-------------------

Large or small numbers can use scientific notation::

    1.5e6       // 1,500,000
    3.0e8       // 300,000,000
    6.626e-34   // Very small number
    9.1e-31     // Another small number

The format is: ``mantissa`` ``e`` ``exponent``, which means mantissa × 10^exponent.

Special Values
--------------

Numbers can represent these special values:

* **Infinity** - Result of division by zero or very large numbers
* **-Infinity** - Negative infinity
* **NaN** - Not a Number (invalid operations)

Operations
----------

Numbers support arithmetic operations::

    10 + 20      // 30
    15 - 5       // 10
    4 * 5        // 20
    20 / 4       // 5.0
    20 // 3      // 6 (floor division)
    17 % 5       // 2 (modulo)

Comparison::

    10 < 20      // true
    15 == 15     // true
    20 > 30      // false

String Type
===========

The ``string`` type represents text sequences.

String Literals
---------------

Enclose strings in double or single quotes::

    "Hello, World!"
    'Hello, World!'
    ""   // Empty string
    ''   // Empty string

Both quote styles work identically. Choose one for consistency.

Escape Sequences
----------------

Use backslash to include special characters:

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Sequence
     - Result
   * - ``\n``
     - Newline
   * - ``\t``
     - Tab character
   * - ``\\``
     - Backslash
   * - ``\"``
     - Double quote
   * - ``\'``
     - Single quote

Example::

    message = "Line one\nLine two";
    path = "C:\\Users\\Name";
    quote = 'She said "Hello"';

String Operations
-----------------

**Concatenation** with ``+``::

    "Hello" + " " + "World"   // "Hello World"
    "Value: " + str(42)       // "Value: 42"

**Length** with ``len()``::

    len("Hello")              // 5
    len("")                   // 0

**Indexing** with brackets (zero-based)::

    text = "Hello";
    text[0]                   // "H"
    text[4]                   // "o"

**Slicing** extracts substrings::

    text = "Hello, World!";
    text[0:5]                 // "Hello"
    text[7:]                  // "World!"

Boolean Type
============

The ``boolean`` type has two values: ``true`` and ``false``.

Boolean Literals
----------------

Use lowercase keywords::

    isActive = true;
    isDone = false;

Comparison operations return booleans::

    10 > 5       // true
    3 == 5       // false

Logical Operations
------------------

Combine booleans with logical operators::

    true && false    // false (AND)
    true || false    // true (OR)
    !true            // false (NOT)

Truthiness
----------

Non-boolean values convert to boolean in conditional contexts:

**Falsy values** (convert to false):

* ``false``
* ``0``
* ``""`` (empty string)
* ``null``
* ``[]`` (empty array)

**Truthy values** (convert to true):

* ``true``
* Non-zero numbers
* Non-empty strings
* Non-empty arrays
* All objects
* All functions

Example::

    if (42) {              // Truthy, condition runs
        console.log("Yes");
    }

    if ("") {              // Falsy, condition skipped
        console.log("No");
    }

Null Type
=========

The ``null`` value represents the intentional absence of a value.

Using Null
----------

Assign ``null`` to indicate no value::

    result = null;
    user = null;

Check for null::

    if (value == null) {
        console.log("No value");
    }

``null`` is distinct from ``undefined``. Use ``null`` when you explicitly want to indicate "no value."

Array Type
==========

Arrays are ordered collections indexed by numbers starting at zero.

Array Literals
--------------

Create arrays with square brackets::

    []                    // Empty array
    [1, 2, 3]            // Three elements
    [10, 20, 30, 40, 50] // Five elements

Arrays can contain any types::

    mixed = [1, "hello", true, [1, 2], {x: 10}];

Accessing Elements
------------------

Use bracket notation with zero-based indices::

    numbers = [10, 20, 30, 40];
    numbers[0]     // 10 (first element)
    numbers[3]     // 40 (last element)

Modifying Elements
------------------

Assign to an index to change an element::

    arr = [1, 2, 3];
    arr[1] = 99;
    // arr is now [1, 99, 3]

.. important::
   Arrays do not auto-extend. You cannot assign to an index beyond the array length. Use ``arr = arr + [value]`` to append elements.

Array Operations
----------------

**Length**::

    len([10, 20, 30])     // 3

**Concatenation**::

    [1, 2] + [3, 4]       // [1, 2, 3, 4]

**Append**::

    arr = [1, 2, 3];
    arr = arr + [4];      // [1, 2, 3, 4]

**Iteration**::

    for (item in [10, 20, 30]) {
        console.log(str(item));
    }

**Slicing**::

    arr = [10, 20, 30, 40, 50];
    arr[1:4]              // [20, 30, 40]
    arr[:3]               // [10, 20, 30]
    arr[2:]               // [30, 40, 50]

Object Type
===========

Objects are unordered collections of key-value pairs.

Object Literals
---------------

Create objects with curly braces::

    {}                    // Empty object
    {x: 10, y: 20}       // Two properties
    {name: "Alice", age: 25}

Keys are identifiers or strings. Values can be any type::

    person = {
        name: "Bob",
        age: 30,
        scores: [85, 90, 78],
        address: {
            city: "Boston",
            zip: "02101"
        }
    };

Accessing Properties
--------------------

Use dot notation for identifier keys::

    person.name      // "Bob"
    person.age       // 30

Use bracket notation for string keys or computed names::

    person["name"]   // "Bob"
    key = "age";
    person[key]      // 30

Modifying Properties
--------------------

Assign to a property to change it::

    person.age = 31;
    person["city"] = "New York";

Add new properties by assigning::

    person.email = "bob@example.com";

Object Operations
-----------------

**Get keys**::

    keys({a: 1, b: 2, c: 3})    // ["a", "b", "c"]

**Number of properties**::

    len({x: 10, y: 20})         // 2

**Iteration over keys** (using ``keys()``)::

    obj = {a: 1, b: 2, c: 3};
    for (key in keys(obj)) {
        console.log(key + ": " + str(obj[key]));
    }

Function Type
=============

Functions are first-class values. You can assign them to variables and pass them as arguments.

Function Values
---------------

Functions have the type ``function``::

    function greet() {
        console.log("Hello");
    }

    typeof(greet)    // "function"

Functions as Values
-------------------

Assign functions to variables::

    add = fn(a, b) => a + b;
    typeof(add)      // "function"
    result = add(10, 20);  // 30

Pass functions as arguments::

    function apply(func, value) {
        return func(value);
    }

    double = fn(x) => x * 2;
    apply(double, 21);  // 42

Return functions from functions::

    function makeAdder(x) {
        return fn(y) => x + y;
    }

    add5 = makeAdder(5);
    add5(10);            // 15

Type Checking
=============

Check Types at Runtime
----------------------

Use ``typeof()`` to get a value's type::

    typeof(42)          // "number"
    typeof("hello")     // "string"
    typeof(true)        // "boolean"
    typeof(null)        // "object" (quirk)
    typeof([1, 2])      // "array"
    typeof({a: 1})      // "object"
    typeof(fn(x) => x)  // "function"

Use ``isinstance()`` to test against a type::

    isinstance(42, "number")        // true
    isinstance("hello", "string")   // true
    isinstance([1, 2], "array")     // true

Type Guards
-----------

Check types before operations::

    function process(value) {
        if (typeof(value) == "number") {
            return value * 2;
        } elif (typeof(value) == "string") {
            return "Text: " + value;
        } elif (typeof(value) == "array") {
            return len(value);
        } else {
            return null;
        }
    }

Type Conversion
===============

Convert Between Types
---------------------

ML provides conversion functions:

**To Number**::

    int(3.14)        // 3
    int("42")        // 42
    float(10)        // 10.0
    float("3.14")    // 3.14

**To String**::

    str(42)          // "42"
    str(3.14)        // "3.14"
    str(true)        // "true"
    str([1, 2])      // "[1, 2]"

**To Boolean**::

    bool(1)          // true
    bool(0)          // false
    bool("text")     // true
    bool("")         // false
    bool([1])        // true
    bool([])         // false

Conversion Rules
----------------

**String to Number:**

* Valid numeric strings convert to numbers
* Invalid strings become ``0`` or ``NaN``

**Number to String:**

* All numbers convert to decimal representation
* Booleans become ``"true"`` or ``"false"``

**To Boolean:**

* Zero, empty string, empty array, null → ``false``
* Everything else → ``true``

Summary
=======

ML provides seven types:

* **number**: All numeric values, including integers and floats
* **string**: Text sequences with escape sequences
* **boolean**: ``true`` or ``false``
* **null**: Absence of value
* **array**: Ordered collections with zero-based indexing
* **object**: Key-value mappings with string keys
* **function**: Executable code as first-class values

The type system is dynamic - variables can hold any type. Use ``typeof()`` to check types at runtime and conversion functions to change types explicitly.

Next, see :doc:`expressions` for how to combine values with operators.
