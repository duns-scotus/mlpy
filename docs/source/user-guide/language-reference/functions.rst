=========
Functions
=========

Functions are reusable blocks of code that perform specific tasks. ML supports both named functions and arrow functions (anonymous functions).

.. contents::
   :local:
   :depth: 2

Function Types
==============

ML provides two function syntaxes:

* **Named Functions**: Declared with ``function`` keyword
* **Arrow Functions**: Anonymous functions with ``fn() =>`` syntax

Both function types can accept parameters, return values, and create closures.

Named Function Declarations
============================

Named functions are declared with the ``function`` keyword.

Syntax
------

::

    function functionName(parameter1, parameter2, ...) {
        statements
        return value;
    }

The function name becomes available in the current scope.

Basic Function
--------------

::

    function greet() {
        console.log("Hello, World!");
    }

    greet();  // Calls the function

Functions with Parameters
-------------------------

::

    function add(a, b) {
        return a + b;
    }

    result = add(10, 20);  // 30

Parameters are local variables that receive argument values.

Functions with Return Values
-----------------------------

::

    function multiply(x, y) {
        return x * y;
    }

    product = multiply(5, 6);  // 30

Use ``return`` to send a value back to the caller. Functions without explicit return statements return ``null``.

Multiple Statements
-------------------

::

    function calculateArea(width, height) {
        area = width * height;
        console.log("Calculating area...");
        return area;
    }

Functions can contain multiple statements before returning.

Early Return
------------

::

    function divide(a, b) {
        if (b == 0) {
            return null;  // Early exit
        }
        return a / b;
    }

Use early returns to handle special cases.

Complete Named Function Example
--------------------------------

Here's a complete program demonstrating named functions:

.. literalinclude:: ../../../ml_snippets/language-reference/functions/01_function_declarations.ml
   :language: ml

This example shows:

* Functions with no parameters
* Functions with parameters
* Functions with multiple statements
* Conditional logic in functions
* Early returns
* Functions calling other functions
* Loop and accumulation patterns

Arrow Functions
===============

Arrow functions provide a concise syntax for creating anonymous functions.

Syntax
------

::

    variableName = fn(parameter1, parameter2, ...) => expression;

Arrow functions use the ``fn`` keyword followed by parameters and ``=>`` (arrow) pointing to the expression.

Basic Arrow Function
--------------------

::

    add = fn(a, b) => a + b;
    result = add(5, 3);  // 8

The expression result is automatically returned.

Single Parameter
----------------

::

    double = fn(x) => x * 2;
    value = double(7);  // 14

Parentheses are required even for single parameters.

No Parameters
-------------

::

    getMessage = fn() => "Hello";
    text = getMessage();  // "Hello"

Use empty parentheses for functions with no parameters.

Arrow Functions vs Named Functions
-----------------------------------

**Named Function**::

    function add(x, y) {
        return x + y;
    }

**Arrow Function Equivalent**::

    add = fn(x, y) => x + y;

Arrow functions are more concise for simple operations.

When to Use Arrow Functions
----------------------------

Arrow functions are ideal for:

* Short, simple operations
* Passing functions as arguments
* Functional programming patterns
* Callbacks and event handlers

Use named functions for:

* Complex logic with multiple statements
* Functions needing descriptive names
* Recursive functions

Complete Arrow Function Example
--------------------------------

Here's a complete program demonstrating arrow functions:

.. literalinclude:: ../../../ml_snippets/language-reference/functions/02_arrow_functions.ml
   :language: ml

This example shows:

* Basic arrow function syntax
* Arrow functions with different parameter counts
* Comparison with named functions
* Arrow functions for various operations (math, strings, booleans, arrays, objects)

Functional Programming with Arrow Functions
============================================

Arrow functions excel in functional programming patterns, especially with higher-order functions like ``map`` and ``filter``.

Using functional.map
--------------------

Transform each element of a collection::

    import functional;

    numbers = [1, 2, 3, 4, 5];

    // Double each number
    doubled = functional.map(fn(x) => x * 2, numbers);
    // [2, 4, 6, 8, 10]

    // Square each number
    squared = functional.map(fn(x) => x * x, numbers);
    // [1, 4, 9, 16, 25]

Using functional.filter
-----------------------

Select elements matching a condition::

    import functional;

    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

    // Filter even numbers
    evens = functional.filter(fn(x) => x % 2 == 0, values);
    // [2, 4, 6, 8, 10]

    // Filter numbers > 5
    large = functional.filter(fn(x) => x > 5, values);
    // [6, 7, 8, 9, 10]

Combining Operations
--------------------

Chain filter and map for complex transformations::

    // Get even numbers, then square them
    evens = functional.filter(fn(x) => x % 2 == 0, numbers);
    squared = functional.map(fn(x) => x * x, evens);

Working with Objects
--------------------

Process arrays of objects::

    students = [
        {name: "Alice", score: 85},
        {name: "Bob", score: 92},
        {name: "Carol", score: 78}
    ];

    // Extract names
    names = functional.map(fn(s) => s.name, students);
    // ["Alice", "Bob", "Carol"]

    // Filter high scorers
    highScorers = functional.filter(fn(s) => s.score >= 90, students);
    // [{name: "Bob", score: 92}]

Complete Functional Programming Example
----------------------------------------

Here's a comprehensive example using arrow functions with functional programming:

.. literalinclude:: ../../../ml_snippets/language-reference/functions/03_functional_programming.ml
   :language: ml

This example demonstrates:

* Using ``functional.map`` with arrow functions for transformations
* Using ``functional.filter`` with arrow functions for selection
* Chaining map and filter operations
* Processing arrays of objects
* Complex data transformations
* Predicate functions for filtering
* Real-world data processing scenarios

Closures and Scope
==================

Functions can access variables from their enclosing scope, creating closures.

Lexical Scoping
---------------

Functions have access to variables in outer scopes::

    x = 10;  // Outer scope

    function useOuter() {
        console.log(str(x));  // Can access x
    }

    useOuter();  // Prints: 10

Local Variables
---------------

Variables declared inside functions are local::

    function calculate() {
        result = 42;  // Local variable
        return result;
    }

    value = calculate();
    // result is not accessible here

The ``nonlocal`` Keyword
-------------------------

Use ``nonlocal`` to modify variables from an enclosing scope::

    function makeCounter() {
        count = 0;

        increment = fn() => {
            nonlocal count;
            count = count + 1;
            return count;
        };

        return increment;
    }

    counter = makeCounter();
    counter();  // 1
    counter();  // 2
    counter();  // 3

Without ``nonlocal``, assigning to ``count`` would create a new local variable.

Closure Example
---------------

Closures capture variables from their creation context::

    function makeAdder(x) {
        return fn(y) => x + y;
    }

    add5 = makeAdder(5);
    add10 = makeAdder(10);

    add5(3);   // 8  (5 + 3)
    add10(3);  // 13 (10 + 3)

Each closure has its own copy of the captured variables.

Practical Closures
------------------

Closures are useful for:

* Creating private state
* Factory functions
* Configuration functions
* Event handlers

Complete Closures Example
--------------------------

Here's a comprehensive example of closures and variable scope:

.. literalinclude:: ../../../ml_snippets/language-reference/functions/04_closures_and_scope.ml
   :language: ml

This example demonstrates:

* Basic closures with counters
* Closure factories (makeAdder, makeMultiplier)
* Variable scope (global, local)
* Closures with multiple variables
* Private data encapsulation
* Nested closures
* Practical applications (accounts, configuration)

Recursive Functions
===================

Functions can call themselves, enabling recursive algorithms.

Basic Recursion
---------------

::

    function factorial(n) {
        if (n <= 1) {
            return 1;  // Base case
        } else {
            return n * factorial(n - 1);  // Recursive case
        }
    }

    factorial(5);  // 120

Recursive functions need:

* **Base case**: Condition that stops recursion
* **Recursive case**: Function calls itself with modified arguments
* **Progress toward base case**: Arguments must change to eventually reach base case

Recursion Patterns
------------------

**Counting down**::

    function countdown(n) {
        if (n <= 0) {
            return;
        }
        console.log(str(n));
        countdown(n - 1);
    }

**Processing sequences**::

    function sumArray(arr, index) {
        if (index >= len(arr)) {
            return 0;
        }
        return arr[index] + sumArray(arr, index + 1);
    }

**Divide and conquer**::

    function binarySearch(arr, target, left, right) {
        if (left > right) {
            return -1;
        }
        mid = (left + right) // 2;
        if (arr[mid] == target) {
            return mid;
        } elif (arr[mid] > target) {
            return binarySearch(arr, target, left, mid - 1);
        } else {
            return binarySearch(arr, target, mid + 1, right);
        }
    }

When to Use Recursion
---------------------

Recursion is natural for:

* Tree and graph algorithms
* Divide-and-conquer problems
* Mathematical sequences (factorial, Fibonacci)
* Backtracking problems

Use iteration instead when:

* Simple counting loops
* Performance is critical (recursion has overhead)
* Stack depth might be exceeded

Complete Recursion Example
---------------------------

Here's a comprehensive example of recursive functions:

.. literalinclude:: ../../../ml_snippets/language-reference/functions/05_recursion.ml
   :language: ml

This example demonstrates:

* Factorial calculation
* Fibonacci sequence
* Recursive array operations
* Power calculation
* String reversal
* Greatest Common Divisor (GCD)
* Palindrome checking
* Binary search algorithm

Higher-Order Functions
======================

Functions that accept other functions as parameters or return functions are higher-order functions.

Functions as Arguments
----------------------

Pass functions to other functions::

    function apply(func, value) {
        return func(value);
    }

    double = fn(x) => x * 2;
    result = apply(double, 21);  // 42

Functions as Return Values
---------------------------

Return functions from functions::

    function makeMultiplier(factor) {
        return fn(x) => x * factor;
    }

    triple = makeMultiplier(3);
    result = triple(7);  // 21

Function Composition
--------------------

Combine multiple functions::

    // Apply multiple filters
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    isEven = fn(x) => x % 2 == 0;
    isLarge = fn(x) => x > 5;

    evens = functional.filter(isEven, numbers);
    largeEvens = functional.filter(isLarge, evens);
    // [6, 8, 10]

Best Practices
==============

Function Naming
---------------

Use descriptive names that indicate what the function does::

    // Good
    function calculateTotal(items) { ... }
    function isValidEmail(address) { ... }

    // Avoid
    function doStuff(x) { ... }
    function fn1(a, b) { ... }

Single Responsibility
---------------------

Each function should do one thing well::

    // Good - focused functions
    function calculateSubtotal(items) { ... }
    function calculateTax(subtotal, rate) { ... }
    function calculateTotal(subtotal, tax) { ... }

    // Avoid - does too much
    function processOrder(items, taxRate, discount) {
        // calculates everything in one function
    }

Keep Functions Small
--------------------

Shorter functions are easier to understand and test::

    // Good - small, clear function
    function isEligible(age) {
        return age >= 18;
    }

    // Avoid - too long
    function processUser(user) {
        // 50+ lines of code
    }

Use Parameters Instead of Global Variables
-------------------------------------------

::

    // Good - explicit dependencies
    function calculate(x, y, factor) {
        return (x + y) * factor;
    }

    // Avoid - hidden dependencies
    globalFactor = 2;
    function calculate(x, y) {
        return (x + y) * globalFactor;
    }

Document Complex Functions
--------------------------

Add comments for non-obvious logic::

    function calculateLeapYear(year) {
        // A year is a leap year if:
        // - Divisible by 4 AND
        // - Not divisible by 100 OR divisible by 400
        return (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0);
    }

Comprehensive Functions Example
================================

Here's a complete program demonstrating all function concepts in a practical data processing pipeline:

.. literalinclude:: ../../../ml_snippets/language-reference/functions/06_comprehensive_example.ml
   :language: ml

This comprehensive example combines:

* **Named Functions**: Statistics calculation, complex business logic
* **Arrow Functions**: Filtering, transformation, data extraction
* **Closures**: Category filters, discount calculators
* **Higher-Order Functions**: Field processing with function parameters
* **Recursion**: Transaction lookup, growth projection
* **Functional Programming**: Using map, filter for data processing
* **Function Composition**: Chaining multiple operations

The example shows how different function types and patterns work together in a real-world data processing scenario.

Summary
=======

ML functions provide:

* **Named Functions**: ``function name(params) { statements }``
* **Arrow Functions**: ``fn(params) => expression``
* **Parameters**: Pass values to functions
* **Return Values**: Send results back with ``return``
* **Closures**: Functions that capture outer scope variables
* **nonlocal**: Modify variables from enclosing scope
* **Recursion**: Functions calling themselves
* **Higher-Order Functions**: Functions as parameters and return values
* **Functional Programming**: map, filter with arrow functions

Key points:

* Use named functions for complex logic
* Use arrow functions for concise operations
* Functions create closures automatically
* Use ``nonlocal`` to modify outer scope variables
* Recursion needs base case and recursive case
* Higher-order functions enable powerful abstractions
* Arrow functions work perfectly with functional.map and functional.filter

For control flow within functions, see :doc:`control-flow`. For built-in utility functions, see :doc:`builtin-functions`.
