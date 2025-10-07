=========
Functions
=========

Functions let you organize code into reusable pieces. Define a function once and call it many times with different inputs.

.. contents::
   :local:
   :depth: 2

Why Use Functions
=================

Functions help you:

* **Avoid repetition**: Write code once, use it many times
* **Organize logic**: Group related operations together
* **Improve readability**: Name complex operations clearly
* **Test independently**: Verify each piece works correctly
* **Build abstractions**: Hide complexity behind simple interfaces

Defining Functions
==================

Basic Syntax
------------

Define a function with the ``function`` keyword:

.. code-block:: ml

    function greet() {
        console.log("Hello!");
    }

Call the function by name:

.. code-block:: ml

    greet();  // Prints "Hello!"

Functions with Parameters
-------------------------

Parameters let functions work with different inputs:

.. code-block:: ml

    function greetPerson(name) {
        console.log("Hello, " + name + "!");
    }

    greetPerson("Alice");  // Prints "Hello, Alice!"
    greetPerson("Bob");    // Prints "Hello, Bob!"

Multiple Parameters
-------------------

Functions can take several parameters:

.. code-block:: ml

    function add(a, b) {
        return a + b;
    }

    result = add(10, 20);  // result is 30

Separate parameters with commas. Call the function with values in the same order.

Return Values
=============

The ``return`` statement sends a value back to the caller.

Basic Returns
-------------

.. code-block:: ml

    function square(x) {
        return x * x;
    }

    value = square(5);  // value is 25

Use the returned value in calculations:

.. code-block:: ml

    total = square(3) + square(4);  // total is 25

Functions Without Return
------------------------

Functions without ``return`` complete their work but don't provide a result:

.. code-block:: ml

    function printMessage(msg) {
        console.log(msg);
    }

    printMessage("Hello");  // Prints but returns nothing

Early Return
------------

Use ``return`` to exit a function early:

.. code-block:: ml

    function findFirst(numbers, target) {
        for (num in numbers) {
            if (num > target) {
                return num;  // Exit immediately when found
            }
        }
        return -1;  // Not found
    }

Complete Example
================

Here's a program demonstrating function basics:

.. literalinclude:: ../../../ml_snippets/tutorial/10_basic_functions.ml
   :language: ml

Run this to see::

    === Function Calls ===
    Hello from a function!
    Hello, Alice!

    === Functions with Return Values ===
    square(5) = 25
    add(10, 20) = 30
    addSquares(3, 4) = 25

    === Rectangle Calculations ===
    Width: 5, Height: 3
    Area: 15
    Perimeter: 16

Function Patterns
=================

Functions with Conditionals
---------------------------

Functions can contain any statements, including conditionals:

.. code-block:: ml

    function max(a, b) {
        if (a > b) {
            return a;
        } else {
            return b;
        }
    }

    largest = max(10, 25);  // largest is 25

Functions with Loops
--------------------

Process arrays with loops inside functions:

.. code-block:: ml

    function sumArray(numbers) {
        total = 0;
        for (num in numbers) {
            total = total + num;
        }
        return total;
    }

    values = [10, 20, 30, 40, 50];
    result = sumArray(values);  // result is 150

Functions that Build Arrays
---------------------------

Create new arrays based on inputs:

.. code-block:: ml

    function doubleValues(numbers) {
        result = [];
        for (num in numbers) {
            result = result + [num * 2];
        }
        return result;
    }

    original = [1, 2, 3, 4, 5];
    doubled = doubleValues(original);  // [2, 4, 6, 8, 10]

.. note::
   Remember to use array concatenation (``result = result + [value]``) when building arrays. Index assignment doesn't work on empty arrays.

Functions that Filter
---------------------

Select elements matching criteria:

.. code-block:: ml

    function getEvens(numbers) {
        evens = [];
        for (num in numbers) {
            if (num % 2 == 0) {
                evens = evens + [num];
            }
        }
        return evens;
    }

    allNumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    evenNumbers = getEvens(allNumbers);  // [2, 4, 6, 8, 10]

Practical Examples
==================

Here's a program showing common function patterns:

.. literalinclude:: ../../../ml_snippets/tutorial/11_function_patterns.ml
   :language: ml

This demonstrates:

* **Conditional logic**: Finding maximum values
* **Array processing**: Summing, doubling, filtering
* **Early returns**: Stopping when found
* **Composing functions**: Calling functions from other functions

Variable Scope
==============

Understanding Scope
-------------------

Variables defined inside a function are **local** to that function. Variables defined outside functions are **global**.

.. code-block:: ml

    globalValue = 100;  // Global variable

    function useLocal() {
        localValue = 50;  // Local to this function
        console.log(str(localValue));
    }

    useLocal();  // Prints 50

Functions can read global variables:

.. code-block:: ml

    globalValue = 100;

    function showGlobal() {
        console.log(str(globalValue));  // Reads global
    }

    showGlobal();  // Prints 100

Scope Example
-------------

Here's a program demonstrating scope:

.. literalinclude:: ../../../ml_snippets/tutorial/12_function_scope.ml
   :language: ml

Built-in Functions
==================

ML provides built-in functions for common tasks.

Type Conversion
---------------

Convert between types:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-13-builtin-functions.transcript
   :language: text
   :lines: 7-14

* ``str(value)`` - Convert to string
* ``int(value)`` - Convert to integer
* ``float(value)`` - Convert to floating point

Type Checking
-------------

Check value types:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-13-builtin-functions.transcript
   :language: text
   :lines: 16-25

* ``typeof(value)`` - Returns type as string

Array and String Functions
---------------------------

Get lengths:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-13-builtin-functions.transcript
   :language: text
   :lines: 27-34

* ``len(value)`` - Returns length of array or string

Math Functions
--------------

Basic comparisons:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-13-builtin-functions.transcript
   :language: text
   :lines: 36-43

* ``min(a, b)`` - Returns smaller value
* ``max(a, b)`` - Returns larger value

Common Patterns
===============

Calculator Pattern
------------------

Group related calculations:

.. code-block:: ml

    function calculateArea(width, height) {
        return width * height;
    }

    function calculatePerimeter(width, height) {
        return 2 * (width + height);
    }

    w = 5;
    h = 3;
    area = calculateArea(w, h);
    perimeter = calculatePerimeter(w, h);

Validation Pattern
------------------

Check inputs before processing:

.. code-block:: ml

    function isValidAge(age) {
        if (age < 0) {
            return false;
        }
        if (age > 150) {
            return false;
        }
        return true;
    }

    if (isValidAge(userAge)) {
        // Process age
    }

Transform Pattern
-----------------

Convert data from one form to another:

.. code-block:: ml

    function celsiusToFahrenheit(celsius) {
        return (celsius * 9 / 5) + 32;
    }

    tempC = 25;
    tempF = celsiusToFahrenheit(tempC);

Helper Function Pattern
-----------------------

Break complex operations into smaller functions:

.. code-block:: ml

    function isEven(num) {
        return num % 2 == 0;
    }

    function countEvens(numbers) {
        count = 0;
        for (num in numbers) {
            if (isEven(num)) {
                count = count + 1;
            }
        }
        return count;
    }

Best Practices
==============

**Naming**: Use verb names for functions: ``calculateTotal``, ``findMaximum``, ``validateInput``.

**Single Purpose**: Each function should do one thing well.

**Parameters**: Keep parameter lists short. More than 3-4 parameters suggests the function is doing too much.

**Return Values**: Be consistent about what functions return. Always return the same type.

**Side Effects**: Functions that modify global state are harder to test and understand. Prefer functions that take inputs and return outputs.

**Documentation**: Name your functions clearly so their purpose is obvious. Well-named functions are self-documenting.

**Testing**: Test functions independently with different inputs to verify they work correctly.

Next Steps
==========

You now understand:

* Defining and calling functions
* Parameters and return values
* Function patterns (conditionals, loops, filtering)
* Variable scope
* Built-in functions

Continue to :doc:`working-with-data` to learn advanced array and object techniques.
