============
Basic Syntax
============

This guide covers the fundamental syntax elements of ML: data types, operators, and control structures. Each concept includes interactive examples you can try in the REPL.

.. contents::
   :local:
   :depth: 2

Understanding Data Types
========================

ML has several built-in data types. You can check any value's type using the ``typeof()`` function.

Numbers
-------

ML treats all numbers uniformly, whether they're integers or decimals:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-04-data-types.transcript
   :language: text
   :lines: 9-16

Strings
-------

Strings represent text and can use either single or double quotes:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-04-data-types.transcript
   :language: text
   :lines: 18-24

Booleans
--------

Boolean values represent true or false:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-04-data-types.transcript
   :language: text
   :lines: 26-32

Type Checking
-------------

Use ``typeof()`` to check any value's type:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-04-data-types.transcript
   :language: text
   :lines: 34-45

Working with Collections
========================

ML provides arrays and objects for storing multiple values.

Arrays
------

Arrays store ordered lists of values. Access elements by their numeric index (starting from 0):

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-05-arrays-objects.transcript
   :language: text
   :lines: 9-23

Objects
-------

Objects store key-value pairs. Access properties using dot notation:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-05-arrays-objects.transcript
   :language: text
   :lines: 25-32

Nested Structures
-----------------

You can nest arrays inside objects and objects inside arrays:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-05-arrays-objects.transcript
   :language: text
   :lines: 34-41

A Complete Example
------------------

Here's a program demonstrating all data types together:

.. literalinclude:: ../../../ml_snippets/tutorial/04_working_with_types.ml
   :language: ml

Run this to see::

    Age: 25 (type: number)
    Price: 19.99 (type: number)
    Full name: John Doe
    Is student: true
    Has license: false
    First score: 85
    Last score: 88
    Book: ML Programming by Jane Smith
    Published: 2024 (350 pages)

Operators and Expressions
==========================

Operators let you perform calculations and comparisons.

Arithmetic Operators
--------------------

The standard arithmetic operators work as expected:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-06-operators.transcript
   :language: text
   :lines: 9-21

* ``+`` Addition
* ``-`` Subtraction
* ``*`` Multiplication
* ``/`` Division
* ``%`` Modulo (remainder)

Comparison Operators
--------------------

Comparison operators evaluate to boolean values:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-06-operators.transcript
   :language: text
   :lines: 23-39

* ``==`` Equal to
* ``!=`` Not equal to
* ``<`` Less than
* ``>`` Greater than
* ``<=`` Less than or equal
* ``>=`` Greater than or equal

Logical Operators
-----------------

Logical operators work with boolean values:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-06-operators.transcript
   :language: text
   :lines: 41-53

* ``&&`` Logical AND (true if both sides are true)
* ``||`` Logical OR (true if either side is true)
* ``!`` Logical NOT (inverts the boolean value)

Combining Operators
-------------------

You can combine operators in complex expressions:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-06-operators.transcript
   :language: text
   :lines: 55-66

Operator precedence follows standard mathematical rules. Use parentheses to make your intent clear.

Practical Example
-----------------

Here's a program using operators in a realistic scenario:

.. literalinclude:: ../../../ml_snippets/tutorial/05_operators_and_expressions.ml
   :language: ml

Comments and Control Flow
==========================

Comments help explain your code. Control flow statements let your program make decisions.

Adding Comments
---------------

Use ``//`` for single-line comments. Comments are ignored by the ML compiler:

.. code-block:: ml

    // This is a comment
    x = 10;  // Comments can appear after code too

    // Comments help explain complex logic
    result = (price * quantity) - (price * quantity * discount);

Control Flow Statements
-----------------------

Control flow lets your program make decisions based on conditions.

Simple If Statements
^^^^^^^^^^^^^^^^^^^^

The ``if`` statement executes code when a condition is true:

.. code-block:: ml

    if (temperature > 30) {
        console.log("It's hot outside!");
    }

If-Else Statements
^^^^^^^^^^^^^^^^^^

The ``else`` clause handles the case when the condition is false:

.. code-block:: ml

    if (temperature > 25) {
        console.log("Weather is warm");
    } else {
        console.log("Weather is cool");
    }

If-Elif-Else Chains
^^^^^^^^^^^^^^^^^^^

Use ``elif`` to check multiple conditions:

.. code-block:: ml

    if (score >= 90) {
        grade = "A";
    } elif (score >= 80) {
        grade = "B";
    } elif (score >= 70) {
        grade = "C";
    } else {
        grade = "F";
    }

Complete Example
----------------

Here's a program showing comments and control flow together:

.. literalinclude:: ../../../ml_snippets/tutorial/06_comments_and_control_flow.ml
   :language: ml

Run this program to see::

    === Simple If Statement ===
    === If-Else Statement ===
    Weather is warm (28°C)
    === If-Elif-Else Chain ===
    Temperature: 28°C - Comfort level: comfortable
    === Nested Conditions ===
    Warm and dry - nice day
    === Grade Calculator ===
    Score: 87
    Grade: B
    Feedback: Good job!

Best Practices
==============

**Semicolons**: End statements with semicolons. This makes your code clear and prevents parsing errors.

**Variable Names**: Use descriptive names like ``userAge`` instead of ``x``. This makes code easier to read.

**Spacing**: Add spaces around operators for readability: ``x + y`` not ``x+y``.

**Comments**: Explain why code does something, not what it does. The code itself shows what happens.

**Braces**: Always use braces ``{}`` with if statements, even for single statements. This prevents errors.

Next Steps
==========

You now understand:

* All basic data types (numbers, strings, booleans)
* Collections (arrays and objects)
* Operators (arithmetic, comparison, logical)
* Comments and control flow

Continue to :doc:`functions` to learn how to organize code into reusable pieces.
