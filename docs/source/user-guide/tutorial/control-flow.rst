==============
Control Flow
==============

Control flow statements let your programs make decisions and repeat operations. ML provides while loops, for loops, and loop control statements.

.. contents::
   :local:
   :depth: 2

While Loops
===========

While loops repeat code as long as a condition is true.

Basic Pattern
-------------

A while loop checks a condition before each iteration:

.. code-block:: ml

    count = 0;
    while (count < 5) {
        console.log("Count: " + str(count));
        count = count + 1;
    }

The loop continues until the condition becomes false. Make sure to update variables inside the loop to avoid infinite loops.

Common Patterns
---------------

**Counter Pattern**

Track how many times the loop runs:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-08-while-loops.transcript
   :language: text
   :lines: 7-18

**Accumulator Pattern**

Build up a total across iterations:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-08-while-loops.transcript
   :language: text
   :lines: 20-32

**String Building**

Concatenate strings in a loop:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-08-while-loops.transcript
   :language: text
   :lines: 34-46

While Loop Examples
-------------------

Here's a program demonstrating common while loop patterns:

.. literalinclude:: ../../../ml_snippets/tutorial/07_while_loops.ml
   :language: ml

Run this to see::

    === Basic Counter ===
    Count: 0
    Count: 1
    Count: 2
    Count: 3
    Count: 4
    === Sum of Numbers 1 to 10 ===
    Total: 55
    === Countdown ===
    5...
    4...
    3...
    2...
    1...
    Liftoff!
    === Finding First Power of 2 Greater Than 100 ===
    2^7 = 128
    === Building Pattern ===
    *
    **
    ***
    ****
    *****

For Loops
=========

For loops iterate over arrays, processing each element.

Basic Iteration
---------------

The for loop uses ``in`` to iterate over array elements:

.. code-block:: ml

    fruits = ["apple", "banana", "cherry"];
    for (fruit in fruits) {
        console.log(fruit);
    }

The loop variable (``fruit``) takes each array value in order.

Working with Arrays
-------------------

For loops make array processing straightforward.

**Accessing Elements**

You can work with array elements directly:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-09-for-loops.transcript
   :language: text
   :lines: 7-16

**Building Arrays**

Create new arrays by concatenating elements:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-09-for-loops.transcript
   :language: text
   :lines: 18-26

.. note::
   ML arrays don't auto-extend with index assignment. Use array concatenation (``arr = arr + [value]``) or the ``append()`` function to add elements.

For Loop Examples
-----------------

Here's a program showing common for loop patterns:

.. literalinclude:: ../../../ml_snippets/tutorial/08_for_loops.ml
   :language: ml

This demonstrates:

* **Iteration**: Processing each element
* **Summation**: Adding up values
* **Finding Maximum**: Comparing elements
* **Building Arrays**: Creating new arrays from existing ones
* **Filtering**: Selecting elements that match a condition
* **Object Processing**: Working with arrays of objects

Loop Control
============

Break and continue statements control loop execution.

Break Statement
---------------

The ``break`` statement exits the loop immediately:

.. code-block:: ml

    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9];
    for (num in numbers) {
        if (num > 5) {
            console.log("Found: " + str(num));
            break;
        }
    }
    // Prints "Found: 6" and exits

Use break when you've found what you're looking for and don't need to continue.

Continue Statement
------------------

The ``continue`` statement skips to the next iteration:

.. code-block:: ml

    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    for (num in numbers) {
        if (num % 2 != 0) {
            continue;
        }
        console.log(str(num));  // Only prints even numbers
    }

Use continue to skip elements that don't match your criteria.

Practical Example
-----------------

Here's a program showing loop control in action:

.. literalinclude:: ../../../ml_snippets/tutorial/09_break_and_continue.ml
   :language: ml

This program demonstrates:

* **Early Exit**: Using break to stop searching once found
* **Filtering**: Using continue to skip unwanted elements
* **Multiple Conditions**: Combining continue statements
* **Nested Loops**: Breaking out of inner loops

Common Patterns
===============

Search Pattern
--------------

Find the first element matching a condition:

.. code-block:: ml

    numbers = [3, 7, 12, 9, 15];
    found = -1;
    for (num in numbers) {
        if (num > 10) {
            found = num;
            break;
        }
    }

Filter Pattern
--------------

Collect elements matching a condition:

.. code-block:: ml

    allNumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    evenNumbers = [];
    for (n in allNumbers) {
        if (n % 2 == 0) {
            evenNumbers = evenNumbers + [n];
        }
    }

Transform Pattern
-----------------

Create a new array by transforming each element:

.. code-block:: ml

    original = [1, 2, 3, 4, 5];
    doubled = [];
    for (value in original) {
        doubled = doubled + [value * 2];
    }

Accumulator Pattern
-------------------

Build up a single value:

.. code-block:: ml

    numbers = [10, 20, 30, 40, 50];
    sum = 0;
    for (num in numbers) {
        sum = sum + num;
    }

Best Practices
==============

**Initialization**: Always initialize counters and accumulators before the loop.

**Loop Conditions**: Make sure while loop conditions eventually become false. Infinite loops freeze your program.

**Array Building**: Use ``arr = arr + [value]`` to add elements. Don't use index assignment on empty arrays.

**Break vs Return**: Use ``break`` to exit a loop. Use ``return`` to exit the entire function.

**Meaningful Names**: Use descriptive loop variable names: ``for (student in students)`` not ``for (s in students)``.

**Single Purpose**: Each loop should do one clear thing. If a loop is complex, consider breaking it into functions.

Next Steps
==========

You now understand:

* While loops for conditional repetition
* For loops for array iteration
* Break and continue for loop control
* Common loop patterns

Continue to :doc:`functions` to learn how to organize code into reusable pieces.
