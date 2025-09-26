================
Standard Library
================

ML standard library reference with security-focused built-ins and comprehensive module documentation based on the actual mlpy implementation.

.. contents:: Library Modules
   :local:
   :depth: 3

Overview
========

The ML standard library provides a comprehensive set of modules for common programming tasks, designed with security-first principles. The library uses a hybrid approach:

- **ML Source Modules**: Core functionality written in ML (`.ml` files)
- **Python Bridge Modules**: High-performance implementations in Python (`.py` files)
- **Capability-Based Security**: All modules require explicit capability declarations
- **Registry System**: Centralized module management with security validation

**Key Features:**

- **Hybrid Architecture**: ML interfaces with Python implementations for performance
- **Security-First Design**: All functions require appropriate capabilities
- **Capability System Integration**: Resource access controlled at module level
- **Python Bridge Functions**: Direct access to Python ecosystem when needed
- **Error Handling**: Safe error modes (e.g., returning null instead of throwing exceptions)

Architecture
============

The ML standard library uses a sophisticated module system:

.. code-block:: text

   ML Program
   └── import math;
       └── Registry loads math.ml (ML interface)
           └── Bridges to math.py (Python implementation)
               └── Validates capabilities
                   └── Executes with security checks

Module Registration
-------------------

Each module is registered with:

- **Name**: Module identifier (e.g., "math", "collections")
- **ML Source**: Interface definition in ML (e.g., "math.ml")
- **Python Bridge**: Implementation module (e.g., "mlpy.stdlib.math")
- **Capabilities Required**: Security permissions needed
- **Bridge Functions**: Python functions exposed to ML

Using Standard Library Modules
===============================

Import standard library modules at the beginning of your ML program:

.. code-block:: ml

   // Import individual modules
   import collections;
   import math;
   import random;

   // Import with alias
   import collections as col;

   // Use imported functions
   result = math.sqrt(16)
   list = collections.append([], "item")
   number = random.randomInt(1, 100)

The transpiler automatically converts these to Python imports:

.. code-block:: python

   # Generated Python code
   from mlpy.stdlib.math import math as ml_math
   from mlpy.stdlib.collections import collections as ml_collections
   from mlpy.stdlib.random import random as ml_random

Built-in Functions
==================

These functions are available without importing any modules (from ``mlpy.stdlib``):

print(message)
--------------

Output text to the console (Python's built-in print function).

.. code-block:: ml

   print("Hello, World!")
   print("Number: " + 42)

**Parameters:**
- ``message`` (string): Text to display

**Returns:** null

**Implementation:** Uses Python's ``print()`` function

getCurrentTime()
----------------

Get the current timestamp as ISO format string.

.. code-block:: ml

   timestamp = getCurrentTime()
   print("Current time: " + timestamp)

**Returns:** string (ISO 8601 formatted datetime)

**Implementation:** Returns ``datetime.datetime.now().isoformat()``

**Capability Required:** None (time access is considered safe)

processData(data)
-----------------

Generic data processing function (placeholder implementation).

.. code-block:: ml

   cleaned_data = processData(raw_input)

**Parameters:**
- ``data`` (any): Data to process

**Returns:** string (formatted as "processed_{data}")

**Implementation:** Simple placeholder that returns ``f"processed_{data}"``

collections Module
==================

The ``collections`` module provides functions for working with arrays (lists) safely and efficiently.

**Capability Requirements:**
- ``execute:collection_operations``

**ML Source:** ``collections.ml``
**Python Bridge:** ``mlpy.stdlib.collections``

Import Statement
----------------

.. code-block:: ml

   import collections;

Core List Functions
-------------------

length(list)
~~~~~~~~~~~~

Get the number of items in a list.

.. code-block:: ml

   numbers = [1, 2, 3, 4, 5]
   count = collections.length(numbers)  // 5

**Parameters:**
- ``list`` (array): List to measure

**Returns:** number (count of items)

**Implementation:** Uses Python's ``len()`` function

append(list, element)
~~~~~~~~~~~~~~~~~~~~~

Add an element to the end of a list, returning a new list.

.. code-block:: ml

   numbers = [1, 2, 3]
   new_numbers = collections.append(numbers, 4)
   // new_numbers is [1, 2, 3, 4]

**Parameters:**
- ``list`` (array): Source list
- ``element`` (any): Element to add

**Returns:** New list with element appended

**Implementation:** ``return lst + [element]`` (immutable operation)

prepend(list, element)
~~~~~~~~~~~~~~~~~~~~~~

Add an element to the beginning of a list, returning a new list.

.. code-block:: ml

   numbers = [2, 3, 4]
   new_numbers = collections.prepend(numbers, 1)
   // new_numbers is [1, 2, 3, 4]

**Parameters:**
- ``list`` (array): Source list
- ``element`` (any): Element to add

**Returns:** New list with element prepended

**Implementation:** ``return [element] + lst``

contains(list, element)
~~~~~~~~~~~~~~~~~~~~~~~

Check if a list contains a specific element.

.. code-block:: ml

   fruits = ["apple", "banana", "orange"]
   has_banana = collections.contains(fruits, "banana")  // true

**Parameters:**
- ``list`` (array): List to search
- ``element`` (any): Element to find

**Returns:** boolean (true if element exists)

**Implementation:** ``return element in lst``

indexOf(list, element)
~~~~~~~~~~~~~~~~~~~~~~

Find the index of an element in a list.

.. code-block:: ml

   fruits = ["apple", "banana", "orange"]
   index = collections.indexOf(fruits, "banana")  // 1
   not_found = collections.indexOf(fruits, "grape")  // -1

**Parameters:**
- ``list`` (array): List to search
- ``element`` (any): Element to find

**Returns:** number (index of element, or -1 if not found)

**Implementation:** Uses Python's ``list.index()`` with exception handling

Additional Functions
--------------------

The collections module also provides:

- ``concat(list1, list2)`` - Concatenate two lists
- ``get(list, index)`` - Safe element access (returns null if out of bounds)
- ``first(list)`` - Get first element
- ``last(list)`` - Get last element
- ``slice(list, start, end)`` - Extract list slice
- ``reverse(list)`` - Reverse list
- ``filter(list, predicate)`` - Filter elements
- ``map(list, transform)`` - Transform elements
- ``find(list, predicate)`` - Find first matching element
- ``reduce(list, reducer, initial)`` - Reduce to single value
- ``removeAt(list, index)`` - Remove element at index

math Module
===========

The ``math`` module provides mathematical functions and constants with safe error handling.

**Capability Requirements:**
- ``read:math_constants``
- ``execute:calculations``

**ML Source:** ``math.ml``
**Python Bridge:** ``mlpy.stdlib.math``

Import Statement
----------------

.. code-block:: ml

   import math;

Constants
---------

pi
~~

The mathematical constant π (pi).

.. code-block:: ml

   circle_area = math.pi * radius * radius

**Value:** 3.141592653589793

**Implementation:** ``py_math.pi``

e
~

The mathematical constant e (Euler's number).

.. code-block:: ml

   exponential_growth = math.e * growth_rate

**Value:** 2.718281828459045

**Implementation:** ``py_math.e``

Basic Functions
---------------

sqrt(x)
~~~~~~~

Calculate the square root with safe error handling.

.. code-block:: ml

   root = math.sqrt(16)        // 4
   safe = math.sqrt(-1)        // 0 (safe error mode)

**Parameters:**
- ``x`` (number): Input value

**Returns:** number (square root, or 0 for negative inputs)

**Implementation:** ``py_math.sqrt(x)`` with negative input returning 0

abs(x)
~~~~~~

Get the absolute value of a number.

.. code-block:: ml

   positive = math.abs(-42)    // 42

**Parameters:**
- ``x`` (number): Input value

**Returns:** number (absolute value)

**Implementation:** Python's built-in ``abs()``

min(a, b) / max(a, b)
~~~~~~~~~~~~~~~~~~~~~

Return the smaller or larger of two numbers.

.. code-block:: ml

   smaller = math.min(10, 20)  // 10
   larger = math.max(10, 20)   // 20

**Parameters:**
- ``a``, ``b`` (number): Values to compare

**Returns:** number (minimum or maximum value)

**Implementation:** Python's built-in ``min()`` and ``max()``

Additional Math Functions
-------------------------

The math module also provides these functions (see ``math.py`` for complete implementations):

- ``floor(x)``, ``ceil(x)``, ``round(x)`` - Rounding functions
- ``sin(x)``, ``cos(x)``, ``tan(x)`` - Trigonometric functions
- ``ln(x)``, ``log(x, base)``, ``exp(x)`` - Logarithmic functions (with safe error modes)
- ``pow(x, y)`` - Power function
- ``degToRad(degrees)``, ``radToDeg(radians)`` - Angle conversion
- ``random()`` - Random number generation (0-1)

random Module
=============

The ``random`` module provides secure random number generation.

**Capability Requirements:**
- ``execute:random_operations``
- ``read:system_entropy``

**ML Source:** ``random.ml``
**Python Bridge:** ``mlpy.stdlib.random``

Key Functions
-------------

.. code-block:: ml

   import random;

   // Basic random functions
   float_val = random.randomFloat()           // 0.0 to 1.0
   int_val = random.randomInt(1, 100)         // 1 to 100 (inclusive)
   bool_val = random.randomBool()             // true or false

   // Advanced functions
   random.setSeed(123)                        // Set seed for testing
   choice = random.choice(["a", "b", "c"])    // Choose from list
   shuffled = random.shuffle([1, 2, 3, 4])    // Shuffle list
   sample = random.sample([1, 2, 3, 4, 5], 3) // Random sample

**Implementation:** All functions use Python's ``random`` module with safe defaults.

console Module
==============

The ``console`` module provides enhanced logging functionality.

**Available from:** ``mlpy.stdlib.console``

Functions
---------

.. code-block:: ml

   // Note: console is imported by default, no import needed
   console.log("Info message")
   console.error("Error message")
   console.warn("Warning message")
   console.debug("Debug message")

**Implementation:** Uses Python's ``print()`` with appropriate output streams (stdout/stderr).

Additional Modules
==================

The ML standard library also includes these modules (see source files for details):

**functional** (``functional.ml``)
  Comprehensive functional programming utilities including ``map``, ``filter``, ``reduce``, and advanced higher-order functions.

  **Capabilities:** ``execute:functional_operations``, ``read:function_data``

**json** (``json.ml``)
  JSON encoding and decoding with security validation.

  **Capabilities:** ``read:json_data``, ``write:json_data``

**string** (``string.ml``)
  String manipulation utilities.

  **Capabilities:** ``execute:string_operations``

**datetime** (``datetime.ml``)
  Date and time operations.

  **Capabilities:** ``read:system_time``, ``read:timezone_data``

Module Registry System
======================

All standard library modules are managed through a central registry system (``registry.py``) that:

1. **Validates Capabilities**: Ensures required permissions are available
2. **Bridges ML to Python**: Maps ML functions to Python implementations
3. **Provides Security**: Validates function calls and arguments
4. **Manages Dependencies**: Handles module loading and dependencies

The registry automatically handles:

- Module discovery and registration
- Capability validation
- Function bridging between ML and Python
- Error handling and safe defaults
- Performance optimization

Security Model
==============

The standard library implements ML's capability-based security model:

**Capability Requirements**
  Each module declares required capabilities that must be granted by the calling program.

**Safe Error Modes**
  Functions return safe values (like 0 or null) instead of throwing exceptions for invalid inputs.

**Input Validation**
  All bridge functions validate inputs before calling Python implementations.

**Sandboxed Execution**
  Python bridge functions execute within ML's security sandbox.

This completes the ML Standard Library Reference based on the actual implementation. For more information:

- **ML Source Files**: ``src/mlpy/stdlib/*.ml`` - ML interface definitions
- **Python Implementations**: ``src/mlpy/stdlib/*.py`` - Bridge implementations
- **Registry System**: ``src/mlpy/stdlib/registry.py`` - Module management
   negative = math.floor(-2.3) // -3

**Parameters:**
- ``number`` (number): Input value

**Returns:** number (rounded down integer)

ceil(number)
~~~~~~~~~~~~

Round up to the nearest integer.

.. code-block:: ml

   up = math.ceil(4.2)         // 5
   negative = math.ceil(-2.7)  // -2

**Parameters:**
- ``number`` (number): Input value

**Returns:** number (rounded up integer)

round(number)
~~~~~~~~~~~~~

Round to the nearest integer.

.. code-block:: ml

   rounded = math.round(4.6)   // 5
   exact = math.round(4.5)     // 5

**Parameters:**
- ``number`` (number): Input value

**Returns:** number (rounded integer)

Power and Root Functions
------------------------

pow(base, exponent)
~~~~~~~~~~~~~~~~~~~

Raise a number to a power.

.. code-block:: ml

   squared = math.pow(5, 2)    // 25
   cubed = math.pow(3, 3)      // 27

**Parameters:**
- ``base`` (number): Base value
- ``exponent`` (number): Power to raise to

**Returns:** number (result of base^exponent)

sqrt(number)
~~~~~~~~~~~~

Calculate the square root.

.. code-block:: ml

   root = math.sqrt(16)        // 4
   hypotenuse = math.sqrt(a*a + b*b)

**Parameters:**
- ``number`` (number): Input value (must be non-negative)

**Returns:** number (square root)

**Error:** Returns null for negative inputs

Trigonometric Functions
-----------------------

sin(radians)
~~~~~~~~~~~~

Calculate the sine of an angle.

.. code-block:: ml

   sine_value = math.sin(math.pi / 2)  // 1

**Parameters:**
- ``radians`` (number): Angle in radians

**Returns:** number (sine value)

cos(radians)
~~~~~~~~~~~~

Calculate the cosine of an angle.

.. code-block:: ml

   cosine_value = math.cos(0)  // 1

**Parameters:**
- ``radians`` (number): Angle in radians

**Returns:** number (cosine value)

tan(radians)
~~~~~~~~~~~~

Calculate the tangent of an angle.

.. code-block:: ml

   tangent_value = math.tan(math.pi / 4)  // 1

**Parameters:**
- ``radians`` (number): Angle in radians

**Returns:** number (tangent value)

random Module
=============

The ``random`` module provides secure random number generation.

Import Statement
----------------

.. code-block:: ml

   import random;

Random Number Functions
-----------------------

randomFloat()
~~~~~~~~~~~~~

Generate a random floating-point number between 0 and 1.

.. code-block:: ml

   chance = random.randomFloat()    // 0.0 to 1.0
   percentage = random.randomFloat() * 100

**Returns:** number (0.0 ≤ value < 1.0)

**Security:** Uses cryptographically secure random generation.

randomInt(min, max)
~~~~~~~~~~~~~~~~~~~

Generate a random integer within a range.

.. code-block:: ml

   dice_roll = random.randomInt(1, 6)      // 1 to 6
   lottery_number = random.randomInt(1, 49) // 1 to 49

**Parameters:**
- ``min`` (number): Minimum value (inclusive)
- ``max`` (number): Maximum value (inclusive)

**Returns:** number (random integer in range)

**Security:** Uses cryptographically secure random generation.

Seed Functions
--------------

setSeed(seed)
~~~~~~~~~~~~~

Set the random number generator seed (for testing only).

.. code-block:: ml

   random.setSeed(123)  // Reproducible random numbers
   first = random.randomInt(1, 100)
   second = random.randomInt(1, 100)

**Parameters:**
- ``seed`` (number): Seed value

**Returns:** null

**Warning:** Only use for testing! Reduces security for cryptographic purposes.

datetime Module
===============

The ``datetime`` module provides date and time functionality.

Import Statement
----------------

.. code-block:: ml

   import datetime;

Date Functions
--------------

now()
~~~~~

Get the current date and time.

.. code-block:: ml

   current = datetime.now()
   print("Current time: " + current)

**Returns:** string (formatted date/time)

**Format:** ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)

formatDate(timestamp, format)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Format a timestamp using a format string.

.. code-block:: ml

   timestamp = getCurrentTime()
   formatted = datetime.formatDate(timestamp, "YYYY-MM-DD")
   print("Today: " + formatted)

**Parameters:**
- ``timestamp`` (number): Unix timestamp
- ``format`` (string): Format pattern

**Returns:** string (formatted date)

**Format Patterns:**
- ``YYYY``: 4-digit year
- ``MM``: 2-digit month
- ``DD``: 2-digit day
- ``HH``: 2-digit hour (24-hour)
- ``mm``: 2-digit minute
- ``ss``: 2-digit second

parseDate(dateString)
~~~~~~~~~~~~~~~~~~~~~

Parse a date string into a timestamp.

.. code-block:: ml

   date_str = "2024-03-15T10:30:00Z"
   timestamp = datetime.parseDate(date_str)

**Parameters:**
- ``dateString`` (string): Date in ISO format

**Returns:** number (Unix timestamp) or null if invalid

console Module
==============

The ``console`` module provides enhanced console output functions.

Import Statement
----------------

.. code-block:: ml

   import console;

Output Functions
----------------

log(message, level)
~~~~~~~~~~~~~~~~~~~

Log a message with a specific level.

.. code-block:: ml

   console.log("Application started", "info")
   console.log("Warning: Low disk space", "warning")
   console.log("Error: Database connection failed", "error")

**Parameters:**
- ``message`` (string): Message to log
- ``level`` (string): Log level ("info", "warning", "error", "debug")

**Returns:** null

**Security:** Automatically sanitizes log output to prevent injection.

error(message)
~~~~~~~~~~~~~~

Log an error message.

.. code-block:: ml

   console.error("Critical system failure")

**Parameters:**
- ``message`` (string): Error message

**Returns:** null

warn(message)
~~~~~~~~~~~~~

Log a warning message.

.. code-block:: ml

   console.warn("Deprecated function used")

**Parameters:**
- ``message`` (string): Warning message

**Returns:** null

debug(message)
~~~~~~~~~~~~~~

Log a debug message (only shown in debug mode).

.. code-block:: ml

   console.debug("Variable x = " + x)

**Parameters:**
- ``message`` (string): Debug message

**Returns:** null

Security Considerations
=======================

Input Validation
-----------------

All standard library functions perform input validation:

.. code-block:: ml

   // Safe - input is validated
   result = math.sqrt(16)

   // Safe - negative input returns null
   invalid = math.sqrt(-1)  // null

   // Safe - out-of-bounds access returns null
   arr = [1, 2, 3]
   missing = arr[10]  // null

Output Sanitization
-------------------

Output functions automatically prevent injection attacks:

.. code-block:: ml

   user_input = "<script>alert('xss')</script>"
   print("User said: " + user_input)
   // Output: User said: &lt;script&gt;alert('xss')&lt;/script&gt;

Capability Integration
----------------------

Functions respect the ML capability system:

.. code-block:: ml

   capability file_read;

   // This would work - we have file_read capability
   content = readFile("data.txt")

   // This would fail - no file_write capability declared
   // writeFile("output.txt", "data")  // Error: Missing file_write capability

Error Handling Best Practices
==============================

Standard library functions use consistent error handling patterns:

.. code-block:: ml

   // Check for null returns
   result = math.sqrt(-1)
   if (result == null) {
       print("Invalid input for square root")
   } else {
       print("Square root: " + result)
   }

   // Handle array bounds safely
   arr = [1, 2, 3]
   index = 5
   if (index < collections.length(arr)) {
       value = arr[index]
       print("Value: " + value)
   } else {
       print("Index out of bounds")
   }

   // Validate object properties
   person = { name: "Alice" }
   if (collections.hasKey(person, "email")) {
       print("Email: " + person.email)
   } else {
       print("No email address available")
   }

Performance Notes
=================

The ML standard library is optimized for performance:

- **Collections**: Array operations use efficient algorithms
- **Math**: Mathematical functions use optimized implementations
- **Memory**: Functions minimize memory allocation where possible
- **Caching**: Frequently used values are cached appropriately

Future Modules
==============

Planned additions to the standard library:

**crypto Module**
  Cryptographic functions and secure hashing

**http Module**
  HTTP client functionality with capability restrictions

**json Module**
  JSON parsing and generation with security validation

**regex Module**
  Regular expression support with safety checks

**string Module**
  Advanced string manipulation functions

**filesystem Module**
  File system operations with capability integration

This completes the ML Standard Library Reference. For more information:

- :doc:`tutorial` for practical examples
- :doc:`language-reference` for syntax details
- :doc:`../developer-guide/security-model` for security architecture