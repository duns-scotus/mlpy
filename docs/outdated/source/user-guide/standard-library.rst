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
  Comprehensive string manipulation utilities with case conversion, validation, and formatting.

  **Capabilities:** ``execute:string_operations``

**datetime** (``datetime.ml``)
  Complete date and time operations with timezone support and business day calculations.

  **Capabilities:** ``read:system_time``, ``read:timezone_data``

**regex** (``regex.ml``)
  Regular expression pattern matching with security validation and ReDoS protection.

  **Capabilities:** ``execute:regex_operations``, ``read:pattern_data``

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

string Module
=============

The ``string`` module provides comprehensive string manipulation utilities with security validation.

**Capability Requirements:**
- ``execute:string_operations``

**ML Source:** ``string.ml``
**Python Bridge:** ``mlpy.stdlib.string_bridge``

Import Statement
----------------

.. code-block:: ml

   import string;

Basic String Functions
----------------------

length(text)
~~~~~~~~~~~~

Get the length of a string.

.. code-block:: ml

   name = "Alice"
   name_length = string.length(name)  // 5

**Parameters:**
- ``text`` (string): Input string

**Returns:** number (length of string)

upper(text) / lower(text)
~~~~~~~~~~~~~~~~~~~~~~~~~

Convert string to uppercase or lowercase.

.. code-block:: ml

   greeting = "Hello World"
   uppercase = string.upper(greeting)    // "HELLO WORLD"
   lowercase = string.lower(greeting)    // "hello world"

**Parameters:**
- ``text`` (string): Input string

**Returns:** string (converted case)

trim(text) / strip(text)
~~~~~~~~~~~~~~~~~~~~~~~~

Remove whitespace from both ends of a string.

.. code-block:: ml

   padded = "  hello world  "
   cleaned = string.trim(padded)  // "hello world"

**Parameters:**
- ``text`` (string): Input string

**Returns:** string (trimmed string)

String Search Functions
-----------------------

contains(text, pattern)
~~~~~~~~~~~~~~~~~~~~~~~

Check if string contains a substring.

.. code-block:: ml

   message = "Hello, World!"
   has_world = string.contains(message, "World")  // true

**Parameters:**
- ``text`` (string): String to search in
- ``pattern`` (string): Substring to find

**Returns:** boolean (true if pattern exists)

starts_with(text, prefix) / ends_with(text, suffix)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Check if string starts or ends with a pattern.

.. code-block:: ml

   filename = "document.pdf"
   is_pdf = string.ends_with(filename, ".pdf")  // true
   is_doc = string.starts_with(filename, "doc")  // true

**Parameters:**
- ``text`` (string): String to check
- ``prefix/suffix`` (string): Pattern to match

**Returns:** boolean (true if matches)

find(text, pattern) / index_of(text, pattern)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Find the position of a substring.

.. code-block:: ml

   text = "The quick brown fox"
   position = string.find(text, "quick")  // 4
   not_found = string.find(text, "slow")  // -1

**Parameters:**
- ``text`` (string): String to search in
- ``pattern`` (string): Substring to find

**Returns:** number (position of first occurrence, -1 if not found)

String Modification Functions
-----------------------------

replace(text, old_pattern, new_pattern)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Replace first occurrence of a pattern.

.. code-block:: ml

   text = "Hello World"
   result = string.replace(text, "World", "Universe")  // "Hello Universe"

**Parameters:**
- ``text`` (string): Source string
- ``old_pattern`` (string): Pattern to replace
- ``new_pattern`` (string): Replacement text

**Returns:** string (modified string)

replace_all(text, old_pattern, new_pattern)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Replace all occurrences of a pattern.

.. code-block:: ml

   text = "foo bar foo"
   result = string.replace_all(text, "foo", "baz")  // "baz bar baz"

split(text, delimiter) / join(separator, parts)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Split string into array or join array into string.

.. code-block:: ml

   csv_data = "apple,banana,orange"
   fruits = string.split(csv_data, ",")  // ["apple", "banana", "orange"]
   rejoined = string.join(", ", fruits)  // "apple, banana, orange"

**Parameters:**
- ``text`` (string): String to split
- ``delimiter`` (string): Split pattern
- ``separator`` (string): Join pattern
- ``parts`` (array): Array to join

**Returns:** array (for split) or string (for join)

Advanced String Functions
-------------------------

Case Conversion Utilities
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   text = "hello_world"
   snake = string.snake_case("HelloWorld")     // "hello_world"
   camel = string.camel_case("hello_world")    // "helloWorld"
   pascal = string.pascal_case("hello_world")  // "HelloWorld"
   kebab = string.kebab_case("HelloWorld")     // "hello-world"

String Validation Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   string.is_empty("")           // true
   string.is_alpha("Hello")      // true
   string.is_numeric("123")      // true
   string.is_alphanumeric("abc123")  // true
   string.is_whitespace("   ")   // true

Character Functions
~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   text = "Hello"
   first_char = string.char_at(text, 0)        // "H"
   char_code = string.char_code_at(text, 0)    // 72
   from_code = string.from_char_code(65)       // "A"

String Formatting
~~~~~~~~~~~~~~~~~

.. code-block:: ml

   template = "Hello, {0}! You have {1} messages."
   formatted = string.format(template, "Alice", 5)
   // "Hello, Alice! You have 5 messages."

datetime Module (Enhanced)
===========================

The enhanced ``datetime`` module provides comprehensive date and time operations.

**Capability Requirements:**
- ``read:system_time``
- ``read:timezone_data``

**ML Source:** ``datetime.ml``
**Python Bridge:** ``datetime``, ``mlpy.stdlib.datetime_bridge``

Import Statement
----------------

.. code-block:: ml

   import datetime;

Current Date/Time Functions
---------------------------

now() / utc_now()
~~~~~~~~~~~~~~~~~

Get current timestamp or UTC timestamp.

.. code-block:: ml

   current = datetime.now()          // Current timestamp
   utc_current = datetime.utc_now()  // UTC timestamp

**Returns:** number (Unix timestamp)

today() / utcnow()
~~~~~~~~~~~~~~~~~~

Get current date string or datetime string.

.. code-block:: ml

   today_str = datetime.today()      // "2024-03-15"
   now_str = datetime.utcnow()       // "2024-03-15T10:30:00Z"

**Returns:** string (formatted date/time)

Date Creation Functions
-----------------------

create_date(year, month, day)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a date from components.

.. code-block:: ml

   birthday = datetime.create_date(1990, 12, 25)  // Christmas 1990

**Parameters:**
- ``year`` (number): Year (e.g., 2024)
- ``month`` (number): Month (1-12)
- ``day`` (number): Day (1-31)

**Returns:** number (timestamp)

create_datetime(year, month, day, hour, minute, second)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a datetime from components.

.. code-block:: ml

   meeting = datetime.create_datetime(2024, 3, 15, 14, 30, 0)
   // March 15, 2024 at 2:30 PM

**Parameters:**
- ``year, month, day`` (number): Date components
- ``hour, minute, second`` (number): Time components

**Returns:** number (timestamp)

Date Arithmetic Functions
-------------------------

add_days(timestamp, days) / add_hours(timestamp, hours)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add time periods to a date.

.. code-block:: ml

   today = datetime.now()
   next_week = datetime.add_days(today, 7)
   in_two_hours = datetime.add_hours(today, 2)

**Parameters:**
- ``timestamp`` (number): Starting timestamp
- ``days/hours`` (number): Amount to add (can be negative)

**Returns:** number (new timestamp)

days_between(start, end) / hours_between(start, end)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Calculate time differences.

.. code-block:: ml

   start_date = datetime.create_date(2024, 1, 1)
   end_date = datetime.create_date(2024, 12, 31)
   days_in_year = datetime.days_between(start_date, end_date)  // 365

**Parameters:**
- ``start`` (number): Start timestamp
- ``end`` (number): End timestamp

**Returns:** number (difference in days/hours)

Enhanced Date Functions
-----------------------

Business Day Functions
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   today = datetime.now()
   is_workday = datetime.is_business_day(today)
   next_business_day = datetime.add_business_days(today, 1)
   work_days = datetime.business_days_between(start_date, end_date)

Date Range Functions
~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   timestamp = datetime.now()
   start_of_today = datetime.start_of_day(timestamp)
   end_of_month = datetime.end_of_month(timestamp)
   start_of_year = datetime.start_of_year(timestamp)

Date Component Extraction
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   timestamp = datetime.now()
   year = datetime.get_year(timestamp)
   month = datetime.get_month(timestamp)
   month_name = datetime.get_month_name(month)  // "March"
   weekday = datetime.get_weekday(timestamp)
   day_name = datetime.get_weekday_name(weekday)  // "Friday"

Age and Comparison Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   birth_date = datetime.create_date(1990, 5, 15)
   current_date = datetime.now()
   age = datetime.age_in_years(birth_date, current_date)

   same_day = datetime.is_same_day(date1, date2)
   same_month = datetime.is_same_month(date1, date2)

regex Module
============

The ``regex`` module provides regular expression pattern matching with security validation.

**Capability Requirements:**
- ``execute:regex_operations``
- ``read:pattern_data``

**ML Source:** ``regex.ml``
**Python Bridge:** ``mlpy.stdlib.regex_bridge``

Import Statement
----------------

.. code-block:: ml

   import regex;

Basic Pattern Matching
----------------------

test(pattern, text)
~~~~~~~~~~~~~~~~~~~

Test if a pattern matches text.

.. code-block:: ml

   email_pattern = "^[\\w._%+-]+@[\\w.-]+\\.[A-Za-z]{2,}$"
   is_email = regex.test(email_pattern, "user@example.com")  // true

**Parameters:**
- ``pattern`` (string): Regular expression pattern
- ``text`` (string): Text to test against

**Returns:** boolean (true if pattern matches)

**Security:** Pattern is validated to prevent ReDoS attacks

match(pattern, text) / find_first(pattern, text)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Find the first match of a pattern.

.. code-block:: ml

   text = "Phone: 123-456-7890"
   phone_pattern = "\\d{3}-\\d{3}-\\d{4}"
   phone_number = regex.match(phone_pattern, text)  // "123-456-7890"

**Parameters:**
- ``pattern`` (string): Regular expression pattern
- ``text`` (string): Text to search in

**Returns:** string (first match or empty string if not found)

find_all(pattern, text)
~~~~~~~~~~~~~~~~~~~~~~~

Find all matches of a pattern.

.. code-block:: ml

   text = "Emails: alice@test.com, bob@example.org"
   email_pattern = "[\\w._%+-]+@[\\w.-]+\\.[A-Za-z]{2,}"
   emails = regex.find_all(email_pattern, text)
   // ["alice@test.com", "bob@example.org"]

**Parameters:**
- ``pattern`` (string): Regular expression pattern
- ``text`` (string): Text to search in

**Returns:** array (all matches)

Pattern Replacement
-------------------

replace(pattern, text, replacement)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Replace first occurrence of pattern.

.. code-block:: ml

   text = "Hello world, hello universe"
   result = regex.replace("hello", text, "hi")  // "hi world, hello universe"

**Parameters:**
- ``pattern`` (string): Pattern to replace
- ``text`` (string): Source text
- ``replacement`` (string): Replacement text

**Returns:** string (modified text)

replace_all(pattern, text, replacement)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Replace all occurrences of pattern.

.. code-block:: ml

   text = "foo bar foo baz foo"
   result = regex.replace_all("foo", text, "qux")  // "qux bar qux baz qux"

Text Splitting
--------------

split(pattern, text) / split_with_limit(pattern, text, max_splits)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Split text using pattern as delimiter.

.. code-block:: ml

   csv_data = "apple,banana,orange,grape"
   fruits = regex.split(",", csv_data)  // ["apple", "banana", "orange", "grape"]
   first_two = regex.split_with_limit(",", csv_data, 2)  // ["apple", "banana", "orange,grape"]

Advanced Pattern Functions
--------------------------

Compiled Patterns (for performance)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   pattern_id = regex.compile_pattern("\\d+")  // Compile once
   has_numbers1 = regex.test_compiled(pattern_id, "abc 123")  // true
   has_numbers2 = regex.test_compiled(pattern_id, "no digits")  // false

Group Matching
~~~~~~~~~~~~~~

.. code-block:: ml

   text = "Date: 2024-03-15"
   date_pattern = "(\\d{4})-(\\d{2})-(\\d{2})"
   matches = regex.find_with_groups(date_pattern, text)
   // [["2024-03-15", "2024", "03", "15"]]

Position Information
~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   text = "The quick brown fox"
   matches = regex.find_with_positions("\\b\\w{5}\\b", text)
   // [{"text": "quick", "start": 4, "end": 9, "groups": []}]

Common Pattern Validators
------------------------

Built-in Validation Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   regex.is_email("user@example.com")     // true
   regex.is_url("https://example.com")    // true
   regex.is_phone_number("+1234567890")   // true
   regex.is_ipv4("192.168.1.1")          // true
   regex.is_uuid("550e8400-e29b-41d4-a716-446655440000")  // true
   regex.is_hex_color("#FF5733")          // true

Text Extraction Helpers
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   text = "Contact: user@test.com, phone: +1-555-0123, visit: https://example.com"

   emails = regex.extract_emails(text)        // ["user@test.com"]
   phones = regex.extract_phone_numbers(text) // ["+1-555-0123"]
   urls = regex.extract_urls(text)            // ["https://example.com"]
   numbers = regex.extract_numbers(text)      // ["1", "555", "0123"]

Security Features
-----------------

Pattern Validation
~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   safe_pattern = "\\d+"
   dangerous_pattern = "(a+)+$"  // ReDoS risk

   regex.is_valid_pattern(safe_pattern)       // true
   regex.is_valid_pattern(dangerous_pattern)  // false (security risk)

Text Sanitization
~~~~~~~~~~~~~~~~~

.. code-block:: ml

   user_input = "Hello <script>alert('xss')</script> world"
   clean_text = regex.remove_html_tags(user_input)  // "Hello  world"
   normalized = regex.normalize_whitespace(clean_text)  // "Hello world"

Security Pattern Detection
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   suspicious_sql = "'; DROP TABLE users; --"
   has_sql_injection = regex.contains_sql_injection_patterns(suspicious_sql)  // true

   suspicious_js = "<img src=x onerror=alert(1)>"
   has_xss = regex.contains_xss_patterns(suspicious_js)  // true

Utility Functions
-----------------

.. code-block:: ml

   // Escape special regex characters
   literal_text = "Price: $19.99 (20% off!)"
   escaped = regex.escape_string(literal_text)
   // "Price: \\$19\\.99 \\(20% off!\\)"

   // Count matches
   text = "The cat sat on the mat"
   word_count = regex.count_matches("\\bthe\\b", text)  // 2

Future Modules
==============

Planned additions to the standard library:

**crypto Module**
  Cryptographic functions and secure hashing

**http Module**
  HTTP client functionality with capability restrictions

**filesystem Module**
  File system operations with capability integration

This completes the ML Standard Library Reference. For more information:

- :doc:`tutorial` for practical examples
- :doc:`language-reference` for syntax details
- :doc:`../developer-guide/security-model` for security architecture