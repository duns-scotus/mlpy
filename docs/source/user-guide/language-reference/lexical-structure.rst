=================
Lexical Structure
=================

This chapter describes the lexical elements that make up ML source code. The lexical structure defines how characters combine to form tokens like identifiers, keywords, literals, and operators.

.. contents::
   :local:
   :depth: 2

Source Code and Encoding
========================

ML source files use UTF-8 encoding. Source code is a sequence of characters that the lexical analyzer divides into tokens.

Whitespace
==========

Whitespace separates tokens and is otherwise ignored. Whitespace includes:

* Space (U+0020)
* Tab (U+0009)
* Newline (U+000A)
* Carriage return (U+000D)

ML allows flexible formatting. Use whitespace to make code readable.

Comments
========

Comments document code and are ignored by the compiler.

Single-Line Comments
--------------------

Use ``//`` to start a comment that extends to the end of the line::

    // This is a comment
    x = 10;  // Comment after code

    // Comments can span multiple lines
    // by starting each line with //

ML has no multi-line comment syntax. Use ``//`` at the start of each line.

Identifiers
===========

Identifiers name variables, functions, and parameters.

Syntax
------

An identifier starts with a letter or underscore, followed by letters, digits, or underscores::

    validName
    _privateVar
    value123
    snake_case_name
    camelCaseName

**Rules:**

* Must start with ``a-z``, ``A-Z``, or ``_``
* Can contain ``a-z``, ``A-Z``, ``0-9``, or ``_``
* Case-sensitive: ``myVar`` and ``myvar`` are different
* Cannot be a reserved keyword

Reserved Keywords
=================

These words have special meaning and cannot be used as identifiers:

Control Flow Keywords
---------------------

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Keyword
     - Purpose
   * - ``if``
     - Start conditional statement
   * - ``elif``
     - Additional conditional branch
   * - ``else``
     - Default conditional branch
   * - ``while``
     - Start while loop
   * - ``for``
     - Start for loop
   * - ``in``
     - For loop iterator keyword
   * - ``break``
     - Exit loop early
   * - ``continue``
     - Skip to next iteration

Function Keywords
-----------------

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Keyword
     - Purpose
   * - ``function``
     - Define named function
   * - ``fn``
     - Arrow function keyword
   * - ``return``
     - Return from function

Exception Keywords
------------------

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Keyword
     - Purpose
   * - ``try``
     - Start exception handler
   * - ``except``
     - Catch exceptions
   * - ``finally``
     - Cleanup code
   * - ``throw``
     - Raise exception

Other Keywords
--------------

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Keyword
     - Purpose
   * - ``import``
     - Import module
   * - ``as``
     - Import alias
   * - ``capability``
     - Define capability
   * - ``nonlocal``
     - Access outer scope variable

Boolean Literals
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Keyword
     - Purpose
   * - ``true``
     - Boolean true value
   * - ``false``
     - Boolean false value

Literals
========

Literals represent fixed values in source code.

Number Literals
---------------

Numbers can be integers or floating-point values.

**Integer Literals**::

    42
    0
    -100
    1000000

**Floating-Point Literals**::

    3.14
    -0.5
    2.0

**Scientific Notation**::

    1.5e6      // 1,500,000
    6.626e-34  // 0.0000000000000000000000000000000000006626
    3.0e8      // 300,000,000

ML treats all numbers as the ``number`` type. There is no separate integer type.

String Literals
---------------

Strings represent text and are enclosed in quotes.

**Double Quotes**::

    "Hello, World!"
    "ML Programming"
    ""  // Empty string

**Single Quotes**::

    'Hello, World!'
    'ML Programming'
    ''  // Empty string

Both quote styles work the same way. Choose one and be consistent.

**Escape Sequences**

Use backslash to include special characters:

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Sequence
     - Meaning
   * - ``\n``
     - Newline
   * - ``\t``
     - Tab
   * - ``\\``
     - Backslash
   * - ``\"``
     - Double quote
   * - ``\'``
     - Single quote

Example::

    message = "Line one\nLine two";
    path = "C:\\Program Files\\App";
    quote = "He said \"Hello\"";

Boolean Literals
----------------

Boolean values represent true or false::

    true
    false

Use lowercase. These are keywords, not identifiers.

Null Literal
------------

The ``null`` value represents the absence of a value::

    x = null;

Operators and Punctuation
==========================

Operators
---------

ML provides these operators:

**Arithmetic**::

    +    Addition
    -    Subtraction
    *    Multiplication
    /    Division
    //   Floor division
    %    Modulo

**Comparison**::

    ==   Equal to
    !=   Not equal to
    <    Less than
    >    Greater than
    <=   Less than or equal
    >=   Greater than or equal

**Logical**::

    &&   Logical AND
    ||   Logical OR
    !    Logical NOT

**Assignment**::

    =    Assign value

**Ternary**::

    ?    Ternary condition
    :    Ternary separator

**Member Access**::

    .    Object property access
    []   Array/object bracket access

**Slice**::

    :    Slice separator (inside brackets)

Punctuation
-----------

::

    ;    Statement terminator
    ,    Separator (arguments, parameters, elements)
    ()   Grouping, function calls
    {}   Blocks, objects
    []   Arrays, access

Semicolons
----------

Semicolons terminate most statements::

    x = 10;
    console.log("Hello");
    return value;

Statements ending with a block don't need semicolons::

    if (x > 10) {
        console.log("Large");
    }  // No semicolon needed

    function greet() {
        console.log("Hello");
    }  // No semicolon needed

Operator Precedence
===================

When expressions combine multiple operators, precedence determines evaluation order.

Precedence Table
----------------

From highest to lowest precedence:

.. list-table::
   :widths: 20 50 30
   :header-rows: 1

   * - Level
     - Operators
     - Associativity
   * - 1 (highest)
     - ``()`` ``[]`` ``.``
     - Left to right
   * - 2
     - ``!`` ``-`` (unary)
     - Right to left
   * - 3
     - ``*`` ``/`` ``//`` ``%``
     - Left to right
   * - 4
     - ``+`` ``-``
     - Left to right
   * - 5
     - ``<`` ``>`` ``<=`` ``>=``
     - Left to right
   * - 6
     - ``==`` ``!=``
     - Left to right
   * - 7
     - ``&&``
     - Left to right
   * - 8
     - ``||``
     - Left to right
   * - 9
     - ``? :`` (ternary)
     - Right to left
   * - 10 (lowest)
     - ``=``
     - Right to left

Examples
--------

Multiplication before addition::

    2 + 3 * 4  // 14, not 20

Comparison before logical::

    x > 10 && y < 20  // Compares first, then AND

Use parentheses for clarity::

    (2 + 3) * 4  // 20
    x > 10 && (y < 20 || z == 0)

Summary
=======

* **Identifiers**: Start with letter or underscore, contain letters, digits, underscores
* **Keywords**: Reserved words with special meaning
* **Literals**: Numbers, strings, booleans, null
* **Comments**: Single-line with ``//``
* **Operators**: Arithmetic, comparison, logical, assignment
* **Precedence**: Function calls highest, assignment lowest
* **Semicolons**: Terminate most statements

Next, see :doc:`data-types` for the ML type system.
