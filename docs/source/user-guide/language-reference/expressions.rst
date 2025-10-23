===========
Expressions
===========

Expressions compute values. Every expression has a type and produces a result when evaluated.

.. contents::
   :local:
   :depth: 2

Expression Categories
=====================

ML provides several categories of expressions:

* **Primary**: Literals, identifiers, parenthesized expressions
* **Arithmetic**: Mathematical operations
* **Comparison**: Value comparisons
* **Logical**: Boolean operations
* **Member Access**: Object and array access
* **Function Calls**: Invoking functions
* **Ternary**: Conditional expressions
* **Slicing**: Substring and subarray extraction

Primary Expressions
===================

Literals
--------

Literals represent fixed values:

**Number Literals**::

    42
    3.14
    1.5e6
    -100

**String Literals**::

    "Hello, World!"
    'Single quotes work too'
    "Escape sequences: \n \t \\"

**Boolean Literals**::

    true
    false

**Null Literal**::

    null

**Array Literals**::

    []
    [1, 2, 3]
    [10, 20, 30, 40, 50]
    [1, "mixed", true, [nested]]

**Object Literals**::

    {}
    {x: 10, y: 20}
    {name: "Alice", age: 25, scores: [85, 90]}

**Function Literals** (arrow functions)::

    fn(x) => x * 2
    fn(a, b) => a + b
    fn() => console.log("Hello")

Identifiers
-----------

Identifiers refer to variables and functions::

    x
    userName
    calculate_total
    _privateValue

An identifier evaluates to the value stored in that variable.

Parenthesized Expressions
--------------------------

Use parentheses to group expressions and control evaluation order::

    (2 + 3) * 4      // 20, not 14
    (x > 10) && (y < 20)

Parentheses override operator precedence.

Arithmetic Expressions
======================

Arithmetic operators combine numeric values.

Binary Operators
----------------

::

    10 + 20      // Addition: 30
    15 - 5       // Subtraction: 10
    4 * 5        // Multiplication: 20
    20 / 4       // Division: 5.0
    20 // 3      // Floor division: 6
    17 % 5       // Modulo: 2

**Division** always produces a floating-point result:

::

    10 / 2       // 5.0 (not 5)
    15 / 4       // 3.75

**Floor Division** produces an integer result::

    15 // 4      // 3
    20 // 3      // 6
    -7 // 2      // -4

**Modulo** returns the remainder::

    17 % 5       // 2
    10 % 3       // 1
    20 % 4       // 0

Unary Operators
---------------

**Negation** reverses the sign::

    -42          // Negative 42
    -(10 + 5)    // -15

    x = 10;
    -x           // -10

String Concatenation
--------------------

The ``+`` operator concatenates strings::

    "Hello" + " " + "World"        // "Hello World"
    "Value: " + str(42)            // "Value: 42"
    "Count: " + str(len([1, 2]))  // "Count: 2"

Non-string values must be converted with ``str()`` before concatenation.

Array Concatenation
-------------------

The ``+`` operator combines arrays::

    [1, 2] + [3, 4]              // [1, 2, 3, 4]
    [10] + [20, 30] + [40]       // [10, 20, 30, 40]
    arr = [];
    arr = arr + [1];             // [1]

Comparison Expressions
======================

Comparison operators compare values and return booleans.

Equality Operators
------------------

::

    10 == 10     // true
    10 == 20     // false
    10 != 20     // true
    10 != 10     // false

**Type Matters**::

    42 == "42"       // false (different types)
    true == 1        // false (different types)
    null == null     // true

Relational Operators
--------------------

::

    10 < 20      // true
    15 > 10      // true
    10 <= 10     // true
    20 >= 30     // false

**String Comparison** (lexicographic order)::

    "apple" < "banana"     // true
    "cat" > "car"          // true
    "hello" == "hello"     // true

**Array Comparison**::

    [1, 2] == [1, 2]       // true
    [1, 2] == [2, 1]       // false

Logical Expressions
===================

Logical operators combine boolean values.

Logical AND
-----------

Returns ``true`` if both operands are truthy::

    true && true      // true
    true && false     // false
    false && true     // false
    false && false    // false

**Short-Circuit Evaluation**: If the left operand is falsy, the right operand is not evaluated::

    x > 0 && y / x > 10   // Safe: y/x only evaluated if x > 0

Logical OR
----------

Returns ``true`` if either operand is truthy::

    true || false     // true
    false || true     // true
    true || true      // true
    false || false    // false

**Short-Circuit Evaluation**: If the left operand is truthy, the right operand is not evaluated::

    hasValue || getDefaultValue()   // getDefaultValue() not called if hasValue is true

Logical NOT
-----------

Inverts a boolean value::

    !true       // false
    !false      // true
    !(x > 10)   // true if x <= 10

Truthiness
----------

Non-boolean values are coerced to boolean in logical contexts:

**Falsy Values**::

    false
    0
    ""           // Empty string
    null
    []           // Empty array

**Truthy Values**::

    true
    42           // Non-zero numbers
    "hello"      // Non-empty strings
    [1, 2]       // Non-empty arrays
    {x: 10}      // All objects
    fn(x) => x   // All functions

Example::

    x = 10;
    if (x) {                    // x is truthy
        console.log("Truthy");
    }

    arr = [];
    if (!arr) {                 // Empty array is falsy
        console.log("Empty");
    }

Member Access Expressions
==========================

Access elements of arrays and properties of objects.

Array Indexing
--------------

Use bracket notation with zero-based indices::

    arr = [10, 20, 30, 40];
    arr[0]      // 10 (first element)
    arr[2]      // 30 (third element)
    arr[3]      // 40 (last element)

**Negative Indices** are not supported in ML. Use positive indices only.

**Nested Arrays**::

    matrix = [[1, 2], [3, 4], [5, 6]];
    matrix[0]       // [1, 2]
    matrix[1][0]    // 3
    matrix[2][1]    // 6

Object Property Access
----------------------

**Dot Notation** for identifier keys::

    person = {name: "Alice", age: 25};
    person.name     // "Alice"
    person.age      // 25

**Bracket Notation** for string keys or computed names::

    person["name"]           // "Alice"

    key = "age";
    person[key]              // 25

**Nested Objects**::

    user = {
        profile: {
            email: "alice@example.com",
            location: {city: "Boston"}
        }
    };

    user.profile.email              // "alice@example.com"
    user.profile.location.city      // "Boston"

**Arrays in Objects**::

    student = {name: "Bob", scores: [85, 90, 78]};
    student.scores[0]       // 85
    student.scores[2]       // 78

**Objects in Arrays**::

    students = [
        {name: "Alice", grade: 85},
        {name: "Bob", grade: 92}
    ];

    students[0].name        // "Alice"
    students[1].grade       // 92

Function Call Expressions
==========================

Invoke functions with arguments.

Basic Function Calls
--------------------

::

    console.log("Hello");
    len([1, 2, 3])
    str(42)
    typeof(value)

**No Arguments**::

    getCurrentTime()
    getRandomNumber()

**Multiple Arguments**::

    add(10, 20)
    substring("hello", 0, 3)
    range(1, 10, 2)

Function Call Chaining
-----------------------

Chain calls on return values::

    str(len([1, 2, 3]))    // "3"

    value = getSomething().process().getResult();

Calling Functions Stored in Variables
--------------------------------------

Functions are first-class values::

    add = fn(a, b) => a + b;
    result = add(10, 20);    // 30

    operations = {
        multiply: fn(a, b) => a * b
    };
    operations.multiply(5, 6);   // 30

Ternary Expressions
===================

The ternary operator provides conditional expressions.

Syntax
------

::

    condition ? value_if_true : value_if_false

The condition is evaluated. If truthy, the first value is returned. Otherwise, the second value is returned.

Examples
--------

**Simple Ternary**::

    age = 20;
    status = age >= 18 ? "adult" : "minor";   // "adult"

**Nested Ternary**::

    score = 85;
    grade = score >= 90 ? "A" :
            score >= 80 ? "B" :
            score >= 70 ? "C" : "F";   // "B"

**In Function Calls**::

    console.log(x > 0 ? "Positive" : "Non-positive");

**Ternary in Expressions**::

    maxValue = a > b ? a : b;
    discount = isPremium ? price * 0.2 : price * 0.1;

Use ternary for simple conditionals. For complex logic, use ``if`` statements instead.

Slicing Expressions
===================

Extract subsequences from strings and arrays.

Slice Syntax
------------

::

    sequence[start:end]
    sequence[start:]
    sequence[:end]
    sequence[:]

* ``start``: Starting index (inclusive)
* ``end``: Ending index (exclusive)
* Omit ``start`` to begin at the start
* Omit ``end`` to continue to the end

String Slicing
--------------

::

    text = "Hello, World!";
    text[0:5]       // "Hello"
    text[7:12]      // "World"
    text[7:]        // "World!"
    text[:5]        // "Hello"
    text[:]         // "Hello, World!" (copy)

Array Slicing
-------------

::

    numbers = [10, 20, 30, 40, 50];
    numbers[1:4]    // [20, 30, 40]
    numbers[2:]     // [30, 40, 50]
    numbers[:3]     // [10, 20, 30]
    numbers[:]      // [10, 20, 30, 40, 50] (copy)

Slicing creates a new sequence without modifying the original.

Operator Precedence
===================

When expressions combine multiple operators, precedence determines evaluation order.

Precedence Table
----------------

From highest to lowest precedence:

.. list-table::
   :widths: 10 40 20 30
   :header-rows: 1

   * - Level
     - Operators
     - Associativity
     - Example
   * - 1
     - ``()`` ``[]`` ``.``
     - Left to right
     - ``arr[i].prop``
   * - 2
     - ``!`` ``-`` (unary)
     - Right to left
     - ``!isActive``
   * - 3
     - ``*`` ``/`` ``//`` ``%``
     - Left to right
     - ``3 * 4 / 2``
   * - 4
     - ``+`` ``-``
     - Left to right
     - ``10 + 20 - 5``
   * - 5
     - ``<`` ``>`` ``<=`` ``>=``
     - Left to right
     - ``x > 10``
   * - 6
     - ``==`` ``!=``
     - Left to right
     - ``a == b``
   * - 7
     - ``&&``
     - Left to right
     - ``a && b``
   * - 8
     - ``||``
     - Left to right
     - ``a || b``
   * - 9
     - ``? :``
     - Right to left
     - ``x > 0 ? 1 : -1``
   * - 10
     - ``=``
     - Right to left
     - ``x = 10``

Precedence Examples
-------------------

**Multiplication before addition**::

    2 + 3 * 4        // 14 (not 20)
    // Evaluated as: 2 + (3 * 4)

**Comparison before logical**::

    x > 10 && y < 20
    // Evaluated as: (x > 10) && (y < 20)

**Member access first**::

    arr[i].value * 2
    // Evaluated as: ((arr[i]).value) * 2

**Ternary has low precedence**::

    x > 0 ? y + 1 : y - 1
    // Evaluated as: x > 0 ? (y + 1) : (y - 1)

Using Parentheses
-----------------

Parentheses override precedence::

    (2 + 3) * 4      // 20
    x > (10 && y)    // Forces evaluation of && first
    (x > 10) && (y < 20)   // Explicit grouping for clarity

Use parentheses liberally for clarity, even when not required by precedence rules.

Expression Evaluation Order
============================

Left-to-Right Evaluation
------------------------

Expressions with the same precedence level evaluate left to right (except for right-associative operators)::

    10 + 20 + 30           // (10 + 20) + 30 = 60
    x.y.z                  // (x.y).z
    func1(func2(func3()))  // func3 first, then func2, then func1

Short-Circuit Evaluation
-------------------------

**Logical AND** (``&&``): If the left operand is falsy, the right operand is not evaluated::

    false && dangerousFunction()   // dangerousFunction() not called

**Logical OR** (``||``): If the left operand is truthy, the right operand is not evaluated::

    true || expensiveComputation()   // expensiveComputation() not called

This is useful for safe conditional evaluation::

    x != 0 && y / x > 10   // Safe: y/x only if x != 0
    value || getDefaultValue()   // Use default if value is falsy

Side Effects
------------

Expressions with side effects (function calls that modify state) evaluate in order::

    console.log("First") + console.log("Second");
    // Prints "First", then "Second"

Function arguments evaluate left to right::

    compute(getValue1(), getValue2(), getValue3());
    // getValue1() executes first, then getValue2(), then getValue3()

Common Expression Patterns
===========================

Default Values
--------------

Use ``||`` to provide default values::

    name = userName || "Guest";
    count = itemCount || 0;

Null Checking
-------------

Check for null before accessing properties::

    result = obj != null ? obj.value : defaultValue;

Range Checking
--------------

Check if a value is within bounds::

    isValid = x >= 0 && x <= 100;
    inRange = value > min && value < max;

Type Checking
-------------

Use ``typeof()`` for type guards::

    isNumber = typeof(value) == "number";
    isArray = typeof(collection) == "array";

Conditional Assignment
----------------------

Assign different values based on conditions::

    discount = isPremium ? 0.2 : isMember ? 0.1 : 0.05;
    status = count == 0 ? "empty" : count == 1 ? "single" : "multiple";

Summary
=======

ML expressions provide:

* **Primary Expressions**: Literals, identifiers, parentheses
* **Arithmetic**: ``+``, ``-``, ``*``, ``/``, ``//``, ``%``
* **Comparison**: ``==``, ``!=``, ``<``, ``>``, ``<=``, ``>=``
* **Logical**: ``&&``, ``||``, ``!`` with short-circuit evaluation
* **Member Access**: ``arr[i]``, ``obj.prop``, ``obj["key"]``
* **Function Calls**: ``func(args)``
* **Ternary**: ``condition ? true_val : false_val``
* **Slicing**: ``sequence[start:end]``
* **Operator Precedence**: Function calls highest, assignment lowest
* **Evaluation Order**: Left-to-right with short-circuiting for logical operators

Understanding operator precedence and evaluation order is essential for writing correct expressions. Use parentheses to make complex expressions clear.

Next, see :doc:`statements` for how expressions form executable statements.
