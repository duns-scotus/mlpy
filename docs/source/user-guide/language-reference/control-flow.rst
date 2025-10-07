============
Control Flow
============

Control flow statements determine the execution order of code. They enable conditional execution, repetition, and exception handling.

.. contents::
   :local:
   :depth: 2

Control Flow Statements
=======================

ML provides these control flow constructs:

* **Conditionals**: ``if``, ``elif``, ``else``
* **Loops**: ``while``, ``for..in``
* **Loop Control**: ``break``, ``continue``
* **Exception Handling**: ``try``, ``except``, ``finally``
* **Function Returns**: ``return``

Conditional Statements
======================

Conditional statements execute code based on boolean conditions.

if Statement
------------

Execute code when a condition is true.

**Syntax**::

    if (condition) {
        statements
    }

**Example**::

    x = 10;
    if (x > 5) {
        console.log("x is greater than 5");
    }

The condition is evaluated. If truthy, the statement block executes.

if-else Statement
-----------------

Execute one block if true, another if false.

**Syntax**::

    if (condition) {
        statements_if_true
    } else {
        statements_if_false
    }

**Example**::

    age = 20;
    if (age >= 18) {
        console.log("Adult");
    } else {
        console.log("Minor");
    }

if-elif-else Statement
----------------------

Test multiple conditions in sequence.

**Syntax**::

    if (condition1) {
        statements1
    } elif (condition2) {
        statements2
    } elif (condition3) {
        statements3
    } else {
        statements_default
    }

**Example**::

    score = 85;
    if (score >= 90) {
        grade = "A";
    } elif (score >= 80) {
        grade = "B";
    } elif (score >= 70) {
        grade = "C";
    } elif (score >= 60) {
        grade = "D";
    } else {
        grade = "F";
    }

Conditions are tested in order. The first true condition executes its block, then control skips to after the entire if statement.

Nested Conditionals
-------------------

Conditionals can be nested inside other conditionals::

    if (x > 0) {
        if (y > 0) {
            console.log("Both positive");
        } else {
            console.log("x positive, y non-positive");
        }
    } else {
        console.log("x non-positive");
    }

Use elif for sequential tests instead of nesting when possible::

    // Prefer this:
    if (x > 10) {
        result = "large";
    } elif (x > 5) {
        result = "medium";
    } else {
        result = "small";
    }

    // Over this:
    if (x > 10) {
        result = "large";
    } else {
        if (x > 5) {
            result = "medium";
        } else {
            result = "small";
        }
    }

Complete Conditional Example
-----------------------------

Here's a complete program demonstrating conditional statements:

.. literalinclude:: ../../../../ml_snippets/language-reference/control-flow/01_conditionals.ml
   :language: ml

This example shows:

* Simple if statements
* if-else branching
* if-elif-else chains for multiple conditions
* Nested conditionals
* Preferring elif over nested ifs

While Loops
===========

While loops repeat code while a condition remains true.

Syntax
------

::

    while (condition) {
        statements
    }

The condition is tested before each iteration. If true, the statements execute. This repeats until the condition becomes false.

Basic While Loop
----------------

::

    count = 0;
    while (count < 5) {
        console.log(str(count));
        count = count + 1;
    }
    // Prints: 0, 1, 2, 3, 4

Loop Initialization
-------------------

Initialize loop variables before the loop::

    sum = 0;
    i = 1;
    while (i <= 10) {
        sum = sum + i;
        i = i + 1;
    }
    // sum is now 55

Loop Conditions
---------------

The condition can be any expression that evaluates to a boolean::

    // Loop until value is too large
    value = 1;
    while (value < 1000) {
        value = value * 2;
    }

    // Loop while not empty
    items = [1, 2, 3];
    while (len(items) > 0) {
        items = items[:-1];  // Remove last element
    }

Infinite Loops
--------------

A loop with a condition that never becomes false runs forever::

    // Infinite loop (use with caution!)
    while (true) {
        console.log("Forever");
    }

Infinite loops require a ``break`` statement to exit (see below).

Complete While Loop Example
----------------------------

Here's a complete program demonstrating while loops:

.. literalinclude:: ../../../../ml_snippets/language-reference/control-flow/02_while_loops.ml
   :language: ml

This example shows:

* Basic counting with while loops
* Accumulation patterns (calculating sums)
* Condition-based iteration (powers of 2)
* Countdown loops
* Practical applications (factorial calculation)

For Loops
=========

For loops iterate over collections (arrays, strings).

Syntax
------

::

    for (variable in collection) {
        statements
    }

The loop variable takes each value from the collection in sequence.

Array Iteration
---------------

::

    numbers = [10, 20, 30, 40, 50];
    for (num in numbers) {
        console.log(str(num));
    }
    // Prints: 10, 20, 30, 40, 50

String Iteration
----------------

::

    text = "Hello";
    for (char in text) {
        console.log(char);
    }
    // Prints: H, e, l, l, o

Using range()
-------------

Generate sequences of numbers with ``range()``::

    // Count from 0 to 4
    for (i in range(5)) {
        console.log(str(i));
    }

    // Count from 1 to 10
    for (i in range(1, 11)) {
        console.log(str(i));
    }

    // Count by 2s
    for (i in range(0, 10, 2)) {
        console.log(str(i));  // 0, 2, 4, 6, 8
    }

Nested For Loops
----------------

::

    for (i in range(3)) {
        for (j in range(3)) {
            console.log(str(i) + "," + str(j));
        }
    }
    // Prints all pairs: 0,0  0,1  0,2  1,0  1,1  1,2  2,0  2,1  2,2

Loop with Index and Value
--------------------------

Use ``enumerate()`` to get both index and value::

    items = ["apple", "banana", "cherry"];
    for (pair in enumerate(items)) {
        index = pair[0];
        value = pair[1];
        console.log(str(index) + ": " + value);
    }
    // Prints: 0: apple, 1: banana, 2: cherry

Complete For Loop Example
--------------------------

Here's a complete program demonstrating for loops:

.. literalinclude:: ../../../../ml_snippets/language-reference/control-flow/03_for_loops.ml
   :language: ml

This example shows:

* Array and string iteration
* Using ``range()`` with different parameters
* Nested for loops
* Using ``enumerate()`` for index and value
* Accumulation patterns with for loops

Break Statement
===============

The ``break`` statement exits a loop immediately.

Syntax
------

::

    break;

Break terminates the innermost containing loop, transferring control to the statement after the loop.

Breaking from While
-------------------

::

    count = 0;
    while (true) {
        console.log(str(count));
        count = count + 1;
        if (count >= 5) {
            break;  // Exit loop
        }
    }
    // Prints: 0, 1, 2, 3, 4

Breaking from For
-----------------

::

    numbers = [1, 5, 8, 3, 9, 2];
    for (num in numbers) {
        if (num > 7) {
            break;  // Stop when we find a large number
        }
        console.log(str(num));
    }
    // Prints: 1, 5

Search Pattern
--------------

Break is useful for search operations::

    found = false;
    target = 42;
    items = [10, 20, 42, 30, 40];

    for (item in items) {
        if (item == target) {
            found = true;
            break;
        }
    }

    if (found) {
        console.log("Found target");
    }

Nested Loop Break
-----------------

Break only exits the innermost loop::

    for (i in range(3)) {
        for (j in range(3)) {
            console.log(str(i) + "," + str(j));
            if (j == 1) {
                break;  // Exits inner loop only
            }
        }
    }
    // Prints: 0,0  0,1  1,0  1,1  2,0  2,1

Continue Statement
==================

The ``continue`` statement skips to the next loop iteration.

Syntax
------

::

    continue;

Continue skips the remaining statements in the loop body and proceeds to the next iteration.

Continue in While
-----------------

::

    count = 0;
    while (count < 10) {
        count = count + 1;
        if (count % 2 == 0) {
            continue;  // Skip even numbers
        }
        console.log(str(count));
    }
    // Prints: 1, 3, 5, 7, 9

Continue in For
---------------

::

    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    for (num in numbers) {
        if (num % 3 == 0) {
            continue;  // Skip multiples of 3
        }
        console.log(str(num));
    }
    // Prints: 1, 2, 4, 5, 7, 8, 10

Filter Pattern
--------------

Continue is useful for filtering::

    values = [-5, 3, -2, 8, -1, 6];
    sum = 0;
    for (value in values) {
        if (value < 0) {
            continue;  // Skip negative values
        }
        sum = sum + value;
    }
    // sum is 17 (3 + 8 + 6)

Break vs Continue
-----------------

* **break**: Exits the loop completely
* **continue**: Skips to next iteration

::

    // Break example
    for (i in range(10)) {
        if (i == 5) {
            break;  // Stops loop entirely
        }
        console.log(str(i));
    }
    // Prints: 0, 1, 2, 3, 4

    // Continue example
    for (i in range(10)) {
        if (i == 5) {
            continue;  // Skips only i=5
        }
        console.log(str(i));
    }
    // Prints: 0, 1, 2, 3, 4, 6, 7, 8, 9

Complete Break and Continue Example
------------------------------------

Here's a complete program demonstrating break and continue:

.. literalinclude:: ../../../../ml_snippets/language-reference/control-flow/04_break_continue.ml
   :language: ml

This example shows:

* Breaking from infinite while loops
* Breaking from for loops (search pattern)
* Skipping iterations with continue
* Filtering patterns with continue
* Practical applications (summing positive numbers)
* Nested loops with break

Return Statement
================

The ``return`` statement exits a function and optionally returns a value.

Syntax
------

::

    return;              // Return without value
    return expression;   // Return with value

Return With Value
-----------------

::

    function add(a, b) {
        return a + b;
    }

    result = add(10, 20);  // 30

Return Without Value
--------------------

::

    function printGreeting(name) {
        console.log("Hello, " + name);
        return;  // Optional - function ends anyway
    }

Functions without explicit return statements return ``null`` implicitly.

Early Return
------------

Use return to exit early based on conditions::

    function divide(a, b) {
        if (b == 0) {
            return null;  // Early exit
        }
        return a / b;
    }

Multiple Returns
----------------

Functions can have multiple return statements::

    function classify(value) {
        if (value < 0) {
            return "negative";
        } elif (value == 0) {
            return "zero";
        } else {
            return "positive";
        }
    }

Return in Loops
---------------

Return immediately exits the function, terminating any loops::

    function findFirst(items, target) {
        for (item in items) {
            if (item == target) {
                return item;  // Exit function
            }
        }
        return null;  // Not found
    }

Exception Handling
==================

Exception handling manages errors gracefully.

Try-Except Statement
--------------------

Catch and handle exceptions.

**Syntax**::

    try {
        statements
    } except (error) {
        error_handling
    }

**Example**::

    try {
        result = riskyOperation();
    } except (err) {
        console.log("Error occurred: " + str(err));
        result = null;
    }

If an exception occurs in the try block, control transfers to the except block. The exception value is bound to the variable (``err`` in the example).

Try-Except-Finally
------------------

Finally block always executes, whether or not an exception occurred.

**Syntax**::

    try {
        statements
    } except (error) {
        error_handling
    } finally {
        cleanup
    }

**Example**::

    file = null;
    try {
        file = openFile("data.txt");
        data = file.read();
    } except (err) {
        console.log("File error: " + str(err));
    } finally {
        if (file != null) {
            file.close();  // Always runs
        }
    }

The finally block is useful for cleanup operations (closing files, releasing resources).

Throw Statement
---------------

Raise exceptions manually.

**Syntax**::

    throw expression;

**Example**::

    function divide(a, b) {
        if (b == 0) {
            throw "Division by zero";
        }
        return a / b;
    }

    try {
        result = divide(10, 0);
    } except (err) {
        console.log("Error: " + str(err));
    }

Multiple Except Clauses
------------------------

ML does not support multiple except clauses with different exception types. Use a single except block and check the error::

    try {
        result = operation();
    } except (err) {
        // Handle all errors here
        console.log("Error: " + str(err));
    }

Complete Exception Handling Example
------------------------------------

Here's a complete program demonstrating exception handling:

.. literalinclude:: ../../../../ml_snippets/language-reference/control-flow/05_exceptions.ml
   :language: ml

This example shows:

* Basic try-except for error handling
* try-except-finally with cleanup code
* Functions that throw exceptions
* Input validation with exceptions
* Nested try-except blocks

Control Flow Best Practices
============================

Prefer Early Returns
--------------------

Exit functions early for error cases::

    // Good
    function process(value) {
        if (value == null) {
            return null;
        }
        if (value < 0) {
            return 0;
        }
        return value * 2;
    }

    // Avoid
    function process(value) {
        result = null;
        if (value != null) {
            if (value >= 0) {
                result = value * 2;
            } else {
                result = 0;
            }
        }
        return result;
    }

Avoid Deep Nesting
------------------

Use elif and early returns instead of nesting::

    // Good
    if (x < 0) {
        return "negative";
    } elif (x == 0) {
        return "zero";
    } else {
        return "positive";
    }

    // Avoid
    if (x < 0) {
        return "negative";
    } else {
        if (x == 0) {
            return "zero";
        } else {
            return "positive";
        }
    }

Use Break for Search
--------------------

Exit loops early when you find what you need::

    found = false;
    for (item in items) {
        if (item.id == targetId) {
            result = item;
            found = true;
            break;  // Stop searching
        }
    }

Avoid Infinite Loops
--------------------

Ensure loop conditions eventually become false::

    // Good - condition will eventually be false
    count = 0;
    while (count < 10) {
        count = count + 1;
    }

    // Bad - infinite loop
    count = 0;
    while (count < 10) {
        // Forgot to increment count!
    }

Initialize Loop Variables
-------------------------

Always initialize variables before loops::

    // Good
    sum = 0;
    for (num in numbers) {
        sum = sum + num;
    }

    // Bad
    for (num in numbers) {
        sum = sum + num;  // ERROR: sum not defined
    }

Use Appropriate Loops
---------------------

* **for**: Known number of iterations or iterating collections
* **while**: Unknown number of iterations based on condition

::

    // Use for when iterating collections
    for (item in items) {
        process(item);
    }

    // Use while when condition-based
    while (hasMoreData()) {
        processNext();
    }

Common Control Flow Patterns
=============================

Loop and Accumulate
-------------------

Build up a result through iteration::

    sum = 0;
    for (num in numbers) {
        sum = sum + num;
    }

    product = 1;
    for (factor in factors) {
        product = product * factor;
    }

Loop and Filter
---------------

Select items matching criteria::

    evens = [];
    for (num in numbers) {
        if (num % 2 == 0) {
            evens = evens + [num];
        }
    }

Loop and Transform
------------------

Convert each item::

    doubled = [];
    for (num in numbers) {
        doubled = doubled + [num * 2];
    }

Search Loop
-----------

Find first matching item::

    found = null;
    for (item in items) {
        if (matches(item)) {
            found = item;
            break;
        }
    }

Count Loop
----------

Count matching items::

    count = 0;
    for (item in items) {
        if (condition(item)) {
            count = count + 1;
        }
    }

Validation Loop
---------------

Check all items meet criteria::

    allValid = true;
    for (item in items) {
        if (!isValid(item)) {
            allValid = false;
            break;
        }
    }

Comprehensive Control Flow Example
===================================

Here's a complete program demonstrating multiple control flow patterns working together in a practical application:

.. literalinclude:: ../../../../ml_snippets/language-reference/control-flow/06_comprehensive_example.ml
   :language: ml

This comprehensive example demonstrates:

* **Conditionals**: Grade determination with if-elif-else
* **For Loops**: Iterating over student data
* **Functions**: Reusable logic for calculations
* **Exception Handling**: Safe processing with try-except
* **Break and Continue**: Early loop exit and filtering
* **Accumulation**: Tracking statistics across iterations
* **Search Patterns**: Finding top performers
* **Validation**: Checking for special conditions

The example shows how control flow statements combine to create a complete student grade analysis system, processing data, handling errors, and generating reports.

Summary
=======

ML control flow provides:

* **Conditionals**: ``if``, ``elif``, ``else`` for branching
* **While Loops**: Repeat while condition is true
* **For Loops**: Iterate over collections with ``for..in``
* **Break**: Exit loop immediately
* **Continue**: Skip to next iteration
* **Return**: Exit function with optional value
* **Try-Except-Finally**: Handle exceptions gracefully
* **Throw**: Raise exceptions

Key points:

* Use elif for sequential conditions, not nested ifs
* Initialize loop variables before use
* Use break for early exit, continue to skip iterations
* Finally blocks always execute (cleanup)
* Prefer early returns for clearer code
* Choose the right loop type (for vs while)

For function control flow details, see :doc:`functions`. For loop iterations over collections, see :doc:`data-types`.
