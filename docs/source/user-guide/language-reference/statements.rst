==========
Statements
==========

Statements are executable units of code. They perform actions but do not produce values (unlike expressions).

.. contents::
   :local:
   :depth: 2

Statement Types
===============

ML provides several statement types:

* **Expression Statements**: Evaluate expressions for side effects
* **Variable Declarations**: Create and initialize variables
* **Assignments**: Update variable values
* **Import Statements**: Load modules
* **Function Declarations**: Define named functions
* **Control Flow**: Conditionals and loops (see :doc:`control-flow`)

Expression Statements
=====================

An expression followed by a semicolon becomes a statement.

Syntax
------

::

    expression;

The expression is evaluated and its result is discarded.

Examples
--------

**Function Calls**::

    console.log("Hello, World!");
    math.sqrt(16);
    len([1, 2, 3]);

**Arithmetic Expressions**::

    x + y;
    counter * 2;
    total / count;

**Assignments** (see next section)::

    x = 10;
    result = calculate(value);

Expression statements are useful for:

* Calling functions for side effects (logging, I/O)
* Triggering operations
* Updating variables

Variable Declarations
=====================

Variables store values. ML uses implicit declaration - a variable is created when first assigned.

Simple Assignment
-----------------

::

    identifier = expression;

The identifier is created (or updated) with the value of the expression.

Examples
--------

**Numbers**::

    x = 10;
    pi = 3.14159;
    count = 0;

**Strings**::

    name = "Alice";
    message = "Hello, " + name;
    empty = "";

**Booleans**::

    isActive = true;
    hasError = false;
    result = x > 10;

**Arrays**::

    numbers = [1, 2, 3, 4, 5];
    empty_list = [];
    mixed = [1, "two", true, [3, 4]];

**Objects**::

    person = {name: "Bob", age: 25};
    point = {x: 10, y: 20};
    config = {};

**Functions**::

    add = fn(a, b) => a + b;
    double = fn(x) => x * 2;

Variable Naming Rules
---------------------

* Must start with a letter (``a-z``, ``A-Z``) or underscore (``_``)
* Can contain letters, digits (``0-9``), underscores
* Cannot be a reserved keyword
* Case-sensitive: ``myVar`` and ``myvar`` are different

**Valid Names**::

    x
    userName
    user_name
    _private
    value123

**Invalid Names**::

    123value     // Cannot start with digit
    user-name    // Hyphens not allowed
    if           // Reserved keyword
    my.var       // Dots not allowed

Variable Scope
--------------

Variables declared at the top level are **global**::

    x = 10;       // Global variable

    function test() {
        console.log(str(x));  // Can access x
    }

Variables declared inside functions are **local**::

    function calculate() {
        result = 42;   // Local to calculate()
        return result;
    }

    // result is not accessible here

Use ``nonlocal`` to modify outer scope variables (see :doc:`functions`).

Assignment Statements
=====================

Assignments update existing variables or create new ones.

Simple Assignment
-----------------

::

    identifier = expression;

Updates the variable with the new value.

Example::

    x = 10;
    x = x + 5;    // x is now 15
    x = x * 2;    // x is now 30

Array Element Assignment
------------------------

Update individual array elements:

::

    array[index] = expression;

The index must be within the array bounds.

Examples::

    numbers = [10, 20, 30];
    numbers[0] = 100;       // [100, 20, 30]
    numbers[2] = 300;       // [100, 20, 300]

.. important::
   Arrays do not auto-extend. You cannot assign to an index beyond the array's current length. To add elements, use ``arr = arr + [value]`` or the ``append()`` function.

**Invalid** (out of bounds)::

    arr = [1, 2, 3];
    arr[5] = 10;         // ERROR: Index out of range

**Valid** (append with concatenation)::

    arr = [1, 2, 3];
    arr = arr + [10];    // [1, 2, 3, 10]

Object Property Assignment
--------------------------

Update or add object properties:

::

    object.property = expression;
    object["key"] = expression;

**Dot Notation**::

    person = {name: "Alice", age: 25};
    person.age = 26;              // Update existing property
    person.email = "alice@example.com";  // Add new property

**Bracket Notation**::

    person["age"] = 27;
    key = "email";
    person[key] = "newemail@example.com";

Bracket notation is useful when:

* Property names are computed at runtime
* Property names contain special characters
* Property names are stored in variables

Destructuring Assignment
------------------------

Extract values from arrays and objects into variables.

**Array Destructuring**::

    [a, b, c] = [1, 2, 3];
    // a = 1, b = 2, c = 3

    [first, second] = [10, 20, 30, 40];
    // first = 10, second = 20, remaining values ignored

**Object Destructuring**::

    {x, y} = {x: 10, y: 20, z: 30};
    // x = 10, y = 20, z is ignored

    {name, age} = {name: "Bob", age: 30, city: "Boston"};
    // name = "Bob", age = 30, city is ignored

Destructuring is useful for:

* Extracting multiple values in one statement
* Function return values (returning multiple values)
* Swapping variables (not directly supported, use temporary)

Assignment Operators
--------------------

ML supports only the basic assignment operator ``=``.

Unlike some languages, ML does **not** have compound assignment operators like ``+=``, ``-=``, ``*=``, etc.

**Instead of compound operators, use explicit assignment**::

    // Other languages:
    // x += 5;

    // ML equivalent:
    x = x + 5;

    // Other languages:
    // count *= 2;

    // ML equivalent:
    count = count * 2;

Import Statements
=================

Import statements load modules and make their functionality available.

Basic Import
------------

::

    import module_name;

After importing, access module members with dot notation:

::

    import math;
    result = math.sqrt(16);  // 4.0
    pi_value = math.pi;      // 3.141592653589793

Import with Alias
-----------------

::

    import module_name as alias;

Use the alias to access module members:

::

    import datetime as dt;
    now = dt.now();
    today = dt.today();

Aliasing is useful when:

* Module names are long
* Avoiding name conflicts
* Following naming conventions

Multiple Imports
----------------

Import multiple modules with separate statements::

    import console;
    import math;
    import datetime;

    console.log("Starting calculations...");
    result = math.sqrt(100);
    timestamp = datetime.now();

Available Modules
-----------------

ML provides these standard library modules:

* **console** - Logging and output
* **math** - Mathematical operations
* **datetime** - Date and time handling
* **string** - String manipulation
* **regex** - Regular expressions
* **collections** - Collection utilities
* **functional** - Functional programming utilities
* **random** - Random number generation
* **json** - JSON parsing and serialization

See the :doc:`../standard-library/index` for complete module documentation.

Import Behavior
---------------

**Modules are loaded once**: The first import loads and initializes the module. Subsequent imports reference the same module instance.

**Module Capabilities**: Some modules require capabilities to function. For example, ``console.log()`` requires the ``console.write`` capability.

Statement Termination
=====================

Semicolons
----------

Most statements end with a semicolon (``;``)::

    x = 10;
    console.log("Hello");
    result = calculate(value);

**Exception**: Block statements (if, while, for, function definitions) do not require semicolons::

    if (x > 10) {
        console.log("Large");
    }  // No semicolon

    function greet() {
        console.log("Hello");
    }  // No semicolon

Empty Statements
----------------

A semicolon by itself is an empty statement::

    ;  // Does nothing

Empty statements are rarely useful. They may appear by accident with extra semicolons::

    x = 10;;  // Second semicolon is empty statement (harmless but unnecessary)

Statement Blocks
================

Blocks group multiple statements together.

Syntax
------

::

    {
        statement1;
        statement2;
        ...
    }

Blocks are used in:

* Function bodies
* Control flow structures (if, while, for)
* Try/except/finally

Examples
--------

**Function Block**::

    function calculate(x, y) {
        sum = x + y;
        product = x * y;
        return product;
    }

**Conditional Block**::

    if (score >= 90) {
        grade = "A";
        console.log("Excellent!");
    }

**Loop Block**::

    while (count < 10) {
        console.log(str(count));
        count = count + 1;
    }

Single Statement Blocks
-----------------------

Blocks with one statement can omit the braces in some contexts::

    if (x > 0)
        console.log("Positive");

However, using braces is recommended for clarity::

    if (x > 0) {
        console.log("Positive");
    }

Statement Order
===============

Statements execute in sequence, from top to bottom::

    x = 10;           // Executes first
    y = x + 5;        // Executes second, x is 10
    result = y * 2;   // Executes third, y is 15

Function Declarations
---------------------

Function declarations are available throughout their containing scope, even before the declaration appears::

    result = calculate(10);  // Works!

    function calculate(x) {
        return x * 2;
    }

This is called "hoisting" - function declarations are processed before statement execution begins.

Variable Initialization Order
------------------------------

Variables must be assigned before use::

    console.log(str(x));  // ERROR: x not defined

    x = 10;
    console.log(str(x));  // OK: x is 10

Common Statement Patterns
==========================

Initialization Pattern
----------------------

Initialize variables before use::

    count = 0;
    total = 0;
    items = [];

    for (value in data) {
        count = count + 1;
        total = total + value;
        items = items + [value * 2];
    }

Accumulation Pattern
--------------------

Build up results incrementally::

    sum = 0;
    for (num in numbers) {
        sum = sum + num;
    }

    product = 1;
    for (num in factors) {
        product = product * num;
    }

Guard Pattern
-------------

Check conditions before operations::

    if (denominator != 0) {
        result = numerator / denominator;
    } else {
        result = 0;
    }

Flag Pattern
------------

Use boolean variables to track state::

    found = false;
    for (item in items) {
        if (item == target) {
            found = true;
            break;
        }
    }

    if (found) {
        console.log("Target found");
    }

Best Practices
==============

**Initialize Variables**: Always initialize variables before use::

    // Good
    count = 0;
    count = count + 1;

    // Bad
    count = count + 1;  // ERROR: count not defined

**Use Descriptive Names**: Choose clear, meaningful variable names::

    // Good
    totalPrice = calculateTotal(items);
    userName = getUserInput();

    // Avoid
    x = calc(y);
    tmp = get();

**One Statement Per Line**: Keep statements on separate lines for readability::

    // Good
    x = 10;
    y = 20;
    z = x + y;

    // Avoid
    x = 10; y = 20; z = x + y;

**Group Related Statements**: Organize related operations together::

    // Initialize
    count = 0;
    total = 0;
    average = 0;

    // Process
    for (value in values) {
        count = count + 1;
        total = total + value;
    }

    // Finalize
    average = total / count;

**Avoid Empty Statements**: Remove unnecessary semicolons::

    // Good
    x = 10;

    // Unnecessary
    x = 10;;

Summary
=======

ML statements provide:

* **Expression Statements**: Evaluate expressions for side effects
* **Variable Declarations**: Implicit declaration on first assignment
* **Simple Assignment**: ``identifier = expression``
* **Array Element Assignment**: ``array[index] = expression`` (within bounds only)
* **Object Property Assignment**: ``object.property = expression``
* **Destructuring**: Extract array and object values
* **Import Statements**: ``import module`` or ``import module as alias``
* **Statement Blocks**: Group statements with ``{ }``
* **Semicolon Termination**: Most statements end with ``;``

Key limitations:

* Arrays do not auto-extend - use concatenation or ``append()``
* No compound assignment operators (``+=``, ``-=``, etc.)
* Variables must be initialized before use
* Array indices must be in bounds for assignment

Next, see :doc:`control-flow` for conditional and loop statements.
