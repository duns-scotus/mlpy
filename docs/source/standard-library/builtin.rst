builtin - The Language Foundation
===================================

.. module:: builtin
   :synopsis: Core functions always available without import

The ``builtin`` module is the foundation of ML programming. Unlike other modules that require explicit imports, these functions are always available in every ML program. They provide the essential tools for type conversion, introspection, collection manipulation, and I/O operations.

**Philosophy:** ML's built-in functions represent the language's core philosophy - dynamic typing with safe introspection, practical utilities for daily programming, and a focus on discoverability. Every ML programmer should master these functions as they form the vocabulary of the language itself.

Quick Start
-----------

.. code-block:: ml

   // No import needed - builtin functions are always available

   // Type conversion
   age = int("25");
   price = float("19.99");
   message = str(42);

   // Type checking
   print(typeof(age));           // "number"
   print(isinstance(age, "number"));  // true

   // Introspection - discover what's available
   print(modules());             // See loaded modules
   print(methods("hello"));      // See string methods

   // Collections
   numbers = range(10);
   print(len(numbers));          // 10
   print(sum(numbers));          // 45

Overview - The Foundation
--------------------------

The builtin module provides 50 functions organized into 10 categories:

1. **Type Conversion** (4 functions) - Convert between types safely
2. **Type Checking** (2 functions) - Inspect types at runtime
3. **Collection Functions** (5 functions) - Work with arrays and objects
4. **I/O Functions** (2 functions) - Print output and read input
5. **Introspection** (6 functions) - Discover and explore the language
6. **Secure Dynamic Functions** (3 functions) - Safe runtime programming
7. **Math Utilities** (8 functions) - Essential mathematical operations
8. **Safe Utilities** (12 functions) - Character encoding, formatting, logic
9. **Iterator Functions** (2 functions) - Advanced iteration control
10. **Type System** (6 functions) - Boolean logic and data validation

**Key Principle:** All builtin functions are designed for safety. Type conversion never raises exceptions (returns sensible defaults), introspection is security-aware (blocks dangerous attributes), and I/O uses ML-compatible formatting (``true/false`` instead of ``True/False``).

Type Conversion Functions
--------------------------

Convert values between ML's fundamental types: numbers, strings, and booleans.

int()
~~~~~

.. function:: int(value)

   Convert value to integer with safe error handling.

   :param value: Value to convert (bool, str, float, int)
   :returns: Integer representation, or 0 on error

   **Conversion Rules:**

   - Booleans: ``true`` → 1, ``false`` → 0
   - Floats: Truncates decimal part
   - Strings: Parses numbers (handles "3.14" → 3)
   - Invalid: Returns 0 (never raises exceptions)

   .. code-block:: ml

      print(int(3.14));         // 3
      print(int("42"));         // 42
      print(int("3.99"));       // 3 (parses as float first)
      print(int(true));         // 1
      print(int(false));        // 0
      print(int("invalid"));    // 0 (safe fallback)

float()
~~~~~~~

.. function:: float(value)

   Convert value to floating-point number with safe error handling.

   :param value: Value to convert (bool, str, int, float)
   :returns: Float representation, or 0.0 on error

   **Conversion Rules:**

   - Booleans: ``true`` → 1.0, ``false`` → 0.0
   - Integers: Converts to float
   - Strings: Parses decimal numbers
   - Invalid: Returns 0.0 (never raises exceptions)

   .. code-block:: ml

      print(float(42));         // 42.0
      print(float("3.14"));     // 3.14
      print(float(true));       // 1.0
      print(float(false));      // 0.0
      print(float("invalid"));  // 0.0 (safe fallback)

str()
~~~~~

.. function:: str(value)

   Convert value to string with ML-compatible boolean formatting.

   :param value: Value to convert
   :returns: String representation

   **Special Behavior:**

   - Booleans: Formats as ``"true"`` and ``"false"`` (lowercase)
   - Numbers: Standard string conversion
   - Arrays/Objects: Formatted representation

   .. code-block:: ml

      print(str(42));           // "42"
      print(str(3.14));         // "3.14"
      print(str(true));         // "true" (lowercase!)
      print(str(false));        // "false" (lowercase!)
      print(str([1,2,3]));      // "[1, 2, 3]"

bool()
~~~~~~

.. function:: bool(value)

   Convert value to boolean.

   :param value: Value to convert
   :returns: Boolean representation

   **Falsy Values:** 0, 0.0, "", [], {}, null, false

   **Truthy Values:** Everything else

   .. code-block:: ml

      print(bool(1));           // true
      print(bool(0));           // false
      print(bool(""));          // false (empty string)
      print(bool("hello"));     // true
      print(bool([]));          // false (empty array)
      print(bool([1,2,3]));     // true

Type Checking Functions
-----------------------

Inspect types at runtime to enable dynamic programming patterns.

typeof()
~~~~~~~~

.. function:: typeof(value)

   Get type of value as a string.

   :param value: Value to check
   :returns: Type name as string

   **Return Values:**

   - ``"boolean"`` - true or false
   - ``"number"`` - integers and floats
   - ``"string"`` - text values
   - ``"array"`` - list collections
   - ``"object"`` - dictionary/object structures
   - ``"function"`` - callable functions
   - Custom class names for @ml_class decorated objects

   .. code-block:: ml

      print(typeof(true));      // "boolean"
      print(typeof(42));        // "number"
      print(typeof(3.14));      // "number"
      print(typeof("hello"));   // "string"
      print(typeof([1,2,3]));   // "array"
      print(typeof({a: 1}));    // "object"

      function greet() { return "hi"; }
      print(typeof(greet));     // "function"

   **Practical Use:** Type-based dispatch and polymorphic functions.

isinstance()
~~~~~~~~~~~~

.. function:: isinstance(value, type_name)

   Check if value is instance of given type.

   :param value: Value to check
   :param type_name: Type name string
   :returns: true if value is of given type

   .. code-block:: ml

      value = 42;
      print(isinstance(value, "number"));   // true
      print(isinstance(value, "string"));   // false

      text = "hello";
      print(isinstance(text, "string"));    // true

   **Pattern:** Use with typeof() for robust type validation:

   .. code-block:: ml

      function processValue(val) {
          if (isinstance(val, "number")) {
              return val * 2;
          } elif (isinstance(val, "string")) {
              return val + "!";
          } else {
              return null;
          }
      }

Collection Functions
--------------------

Universal functions for working with strings, arrays, and objects.

len()
~~~~~

.. function:: len(collection)

   Get length of string, array, or object.

   :param collection: String, array, or object
   :returns: Length/size, or 0 if not a collection

   .. code-block:: ml

      print(len("hello"));          // 5
      print(len([1,2,3,4,5]));      // 5
      print(len({a:1, b:2, c:3}));  // 3

range()
~~~~~~~

.. function:: range(start, stop, step)
              range(start, stop)
              range(stop)

   Generate array of numbers.

   :param start: Start value (or stop if only one argument)
   :param stop: Stop value (exclusive)
   :param step: Step size (default 1)
   :returns: Array of numbers

   .. code-block:: ml

      print(range(5));              // [0, 1, 2, 3, 4]
      print(range(2, 7));           // [2, 3, 4, 5, 6]
      print(range(0, 10, 2));       // [0, 2, 4, 6, 8]

      // Practical: Sum first N numbers
      print(sum(range(11)));        // 55

enumerate()
~~~~~~~~~~~

.. function:: enumerate(array, start=0)

   Create (index, value) pairs from array.

   :param array: Array to enumerate
   :param start: Starting index (default 0)
   :returns: Array of [index, value] pairs

   .. code-block:: ml

      fruits = ["apple", "banana", "cherry"];
      pairs = enumerate(fruits);

      // pairs = [[0, "apple"], [1, "banana"], [2, "cherry"]]

      // With custom start
      numbered = enumerate(fruits, 1);
      // [[1, "apple"], [2, "banana"], [3, "cherry"]]

keys()
~~~~~~

.. function:: keys(obj)

   Get array of object keys.

   :param obj: Object to extract keys from
   :returns: Array of key strings

   .. code-block:: ml

      person = {name: "Alice", age: 30, city: "NYC"};
      print(keys(person));  // ["name", "age", "city"]

values()
~~~~~~~~

.. function:: values(obj)

   Get array of object values.

   :param obj: Object to extract values from
   :returns: Array of values

   .. code-block:: ml

      person = {name: "Alice", age: 30, city: "NYC"};
      print(values(person));  // ["Alice", 30, "NYC"]

I/O Functions
-------------

Simple console input and output operations.

print()
~~~~~~~

.. function:: print(*values)

   Print values to console with ML-compatible formatting.

   :param values: Values to print (variable arguments)

   **Special Behavior:**

   - Booleans print as ``true/false`` (not ``True/False``)
   - Multiple arguments separated by spaces
   - Automatic string conversion

   .. code-block:: ml

      print("Hello, World!");
      print("Number:", 42);
      print("Boolean:", true);        // prints "Boolean: true"
      print("Array:", [1, 2, 3]);

input()
~~~~~~~

.. function:: input(prompt="")

   Read string from console.

   :param prompt: Optional prompt to display
   :returns: User input as string

   .. code-block:: ml

      name = input("Enter your name: ");
      print("Hello, " + name);

      age = int(input("Enter your age: "));
      print("You are " + str(age) + " years old");

Introspection Functions
-----------------------

**The Heart of ML:** These functions enable discovery and exploration of the language itself. They make ML a self-documenting, explorable environment where programmers can learn by experimentation.

help()
~~~~~~

.. function:: help(target)

   Get documentation for function, method, or module.

   :param target: Function, method, or module
   :returns: Documentation string

   **Works with:**

   - @ml_function decorated functions
   - @ml_module decorated modules
   - @ml_class decorated classes
   - Any object with docstrings

   .. code-block:: ml

      import console;
      import math;

      print(help(console.log));    // "Log message to console"
      print(help(math.sqrt));      // "Calculate square root"

methods()
~~~~~~~~~

.. function:: methods(value)

   List all available methods for a value.

   :param value: Value to inspect
   :returns: Sorted array of method names

   **Practical Use:** Discovery and exploration of capabilities.

   .. code-block:: ml

      // Discover string methods
      text = "hello";
      stringMethods = methods(text);
      print("String has " + str(len(stringMethods)) + " methods");
      // Common methods: upper, lower, split, replace, etc.

      // Discover array methods
      numbers = [1, 2, 3];
      arrayMethods = methods(numbers);
      // Common methods: append, pop, sort, reverse, etc.

modules()
~~~~~~~~~

.. function:: modules()

   List all currently imported modules.

   :returns: Sorted array of module names

   .. code-block:: ml

      import console;
      import math;
      import regex;

      print(modules());
      // ["builtin", "console", "math", "regex"]

   **Practical Use:** Debug import issues and verify module availability.

   **Note:** To see ALL available modules (not just imported ones), use ``available_modules()``.

available_modules()
~~~~~~~~~~~~~~~~~~~

.. function:: available_modules()

   List all available ML modules (both imported and unimported).

   :returns: Sorted array of module names

   **Discovery System:**

   This function uses ML's automatic module discovery to find:

   - Standard library modules (auto-discovered from ``*_bridge.py`` files)
   - Extension modules (from configured extension paths)
   - Already imported modules

   .. code-block:: ml

      // See all available modules without importing
      allModules = available_modules();
      print(allModules);
      // ["collections", "console", "datetime", "file",
      //  "functional", "http", "json", "math", "path",
      //  "random", "regex", ...]

      // Check what's available before import
      if (has_module("regex")) {
          import regex;
          // Use regex module
      }

   **Practical Use:**

   - Discover standard library modules without manual documentation lookup
   - Check module availability before importing
   - Build module exploration tools
   - Debug module loading issues

   **Performance:** Lazy discovery - modules are scanned on first call, then cached.

has_module()
~~~~~~~~~~~~

.. function:: has_module(module_name)

   Check if a module is available for import.

   :param module_name: Name of module to check
   :returns: true if module can be imported, false otherwise

   .. code-block:: ml

      // Check before importing
      if (has_module("math")) {
          import math;
          print(math.pi);
      }

      if (has_module("nonexistent")) {
          print("Module exists");
      } else {
          print("Module not found");  // This executes
      }

   **Practical Use:**

   - Conditional imports based on availability
   - Feature detection (check if extension modules are installed)
   - Defensive programming (avoid import errors)
   - Build cross-environment compatible code

   **Example - Optional Feature:**

   .. code-block:: ml

      // Use advanced module if available, fallback otherwise
      if (has_module("advanced_crypto")) {
          import advanced_crypto;
          hash = advanced_crypto.sha512(data);
      } else {
          import crypto;
          hash = crypto.sha256(data);  // Fallback
      }

module_info()
~~~~~~~~~~~~~

.. function:: module_info(module_name)

   Get detailed information about a module.

   :param module_name: Name of module to get info for
   :returns: Dictionary with module metadata, or null if not found

   **Returned Dictionary:**

   - ``name`` - Module name
   - ``description`` - Module description
   - ``version`` - Module version
   - ``capabilities`` - Required capabilities array
   - ``functions`` - Dictionary of functions with descriptions
   - ``classes`` - Dictionary of classes with descriptions
   - ``loaded`` - Whether module is currently imported

   .. code-block:: ml

      info = module_info("math");

      if (info != null) {
          print("Module: " + info.name);
          print("Description: " + info.description);
          print("Version: " + info.version);
          print("Loaded: " + str(info.loaded));

          // Explore functions
          functions = info.functions;
          funcNames = keys(functions);
          print("Available functions: " + str(len(funcNames)));

          // Get help on specific function
          sqrtInfo = functions.sqrt;
          print("sqrt: " + sqrtInfo.description);
      }

   **Practical Use:**

   - Module exploration and discovery
   - Generate documentation programmatically
   - Build module browsers and explorers
   - Verify module capabilities before use
   - Check function availability

   **Example - Dynamic Help System:**

   .. code-block:: ml

      function showModuleHelp(moduleName) {
          info = module_info(moduleName);

          if (info == null) {
              print("Module '" + moduleName + "' not found");
              return;
          }

          print("\n=== " + info.name + " ===");
          print(info.description);
          print("\nFunctions:");

          functions = info.functions;
          funcNames = keys(functions);
          i = 0;
          while (i < len(funcNames)) {
              fname = funcNames[i];
              finfo = functions[fname];
              print("  " + fname + "() - " + finfo.description);
              i = i + 1;
          }
      }

      // Use the help system
      showModuleHelp("math");

Secure Dynamic Functions
-------------------------

Safe runtime attribute access and function invocation with built-in security.

hasattr()
~~~~~~~~~

.. function:: hasattr(obj, name)

   Check if object has safe attribute.

   :param obj: Object to check
   :param name: Attribute name
   :returns: true if attribute exists and is safe

   **Security:**

   - Blocks ALL dunder attributes (``__class__``, ``__dict__``, etc.)
   - Only whitelisted safe attributes return true
   - Prevents object internals access

   .. code-block:: ml

      person = {name: "Alice", age: 30};

      print(hasattr(person, "name"));      // true
      print(hasattr(person, "email"));     // false
      print(hasattr(person, "__class__")); // false (blocked!)

getattr()
~~~~~~~~~

.. function:: getattr(obj, name, default=null)

   Get safe attribute from object with fallback.

   :param obj: Object to access
   :param name: Attribute name
   :param default: Value to return if not found
   :returns: Attribute value or default

   **Security:**

   - Routes through SafeAttributeRegistry
   - Blocks dangerous attributes
   - Returns default for missing/unsafe attributes

   .. code-block:: ml

      person = {name: "Alice", age: 30};

      name = getattr(person, "name", "Unknown");
      print(name);  // "Alice"

      email = getattr(person, "email", "no-email@example.com");
      print(email);  // "no-email@example.com"

      // Security: blocked attributes return default
      cls = getattr(person, "__class__", "BLOCKED");
      print(cls);  // "BLOCKED"

call()
~~~~~~

.. function:: call(func, *args, **kwargs)

   Call function dynamically with validation.

   :param func: Callable to invoke
   :param args: Positional arguments
   :param kwargs: Keyword arguments
   :returns: Function result

   **Security:**

   - Validates function is whitelisted
   - Blocks eval, exec, compile, __import__
   - Prevents arbitrary code execution

   .. code-block:: ml

      import math;

      result = call(math.abs, -5);
      print(result);  // 5

      // Security: dangerous functions blocked
      // call(eval, "malicious") → SecurityError!

Math Utility Functions
----------------------

Essential mathematical operations for everyday programming.

abs()
~~~~~

.. function:: abs(value)

   Get absolute value.

   :param value: Number
   :returns: Absolute value

   .. code-block:: ml

      print(abs(-5));      // 5
      print(abs(3.14));    // 3.14
      print(abs(-42.7));   // 42.7

min()
~~~~~

.. function:: min(*values)
              min(array)

   Get minimum value.

   :param values: Values to compare (or single array)
   :returns: Minimum value

   .. code-block:: ml

      print(min(1, 2, 3));           // 1
      print(min([5, 2, 8]));         // 2

max()
~~~~~

.. function:: max(*values)
              max(array)

   Get maximum value.

   :param values: Values to compare (or single array)
   :returns: Maximum value

   .. code-block:: ml

      print(max(1, 2, 3));           // 3
      print(max([5, 2, 8]));         // 8

round()
~~~~~~~

.. function:: round(value, precision=0)

   Round number to precision.

   :param value: Number to round
   :param precision: Decimal places (default 0)
   :returns: Rounded number

   .. code-block:: ml

      pi = 3.14159;
      print(round(pi));        // 3.0
      print(round(pi, 2));     // 3.14
      print(round(pi, 4));     // 3.1416

zip()
~~~~~

.. function:: zip(*arrays)

   Combine multiple arrays into tuples.

   :param arrays: Arrays to zip
   :returns: Array of tuples

   .. code-block:: ml

      names = ["Alice", "Bob", "Charlie"];
      ages = [25, 30, 35];

      pairs = zip(names, ages);
      // [[" Alice", 25], ["Bob", 30], ["Charlie", 35]]

sorted()
~~~~~~~~

.. function:: sorted(array, reverse=false)

   Return sorted copy of array.

   :param array: Array to sort
   :param reverse: Sort descending (default false)
   :returns: New sorted array

   .. code-block:: ml

      numbers = [3, 1, 4, 1, 5];
      print(sorted(numbers));        // [1, 1, 3, 4, 5]
      print(sorted(numbers, true));  // [5, 4, 3, 1, 1]

sum()
~~~~~

.. function:: sum(iterable, start=0)

   Sum numeric values.

   :param iterable: Array of numbers
   :param start: Starting value (default 0)
   :returns: Sum of all values

   .. code-block:: ml

      print(sum([1, 2, 3]));       // 6
      print(sum([1.5, 2.5, 3.0])); // 7.0
      print(sum([1, 2, 3], 10));   // 16

Safe Utility Functions
----------------------

Character encoding, number base conversion, and data validation utilities.

chr()
~~~~~

.. function:: chr(i)

   Convert Unicode code point to character.

   :param i: Unicode code point
   :returns: Character string

   .. code-block:: ml

      print(chr(65));      // "A"
      print(chr(97));      // "a"
      print(chr(8364));    // "€"

ord()
~~~~~

.. function:: ord(c)

   Convert character to Unicode code point.

   :param c: Single character
   :returns: Unicode code point

   .. code-block:: ml

      print(ord("A"));     // 65
      print(ord("a"));     // 97
      print(ord("€"));     // 8364

hex()
~~~~~

.. function:: hex(n)

   Convert integer to hexadecimal string.

   :param n: Integer
   :returns: Hex string with '0x' prefix

   .. code-block:: ml

      print(hex(255));     // "0xff"
      print(hex(16));      // "0x10"

bin()
~~~~~

.. function:: bin(n)

   Convert integer to binary string.

   :param n: Integer
   :returns: Binary string with '0b' prefix

   .. code-block:: ml

      print(bin(10));      // "0b1010"
      print(bin(255));     // "0b11111111"

oct()
~~~~~

.. function:: oct(n)

   Convert integer to octal string.

   :param n: Integer
   :returns: Octal string with '0o' prefix

   .. code-block:: ml

      print(oct(8));       // "0o10"
      print(oct(64));      // "0o100"

format()
~~~~~~~~

.. function:: format(value, format_spec="")

   Format value with format specifier.

   :param value: Value to format
   :param format_spec: Python-style format specification
   :returns: Formatted string

   .. code-block:: ml

      print(format(3.14159, ".2f"));   // "3.14"
      print(format(42, "05d"));        // "00042"
      print(format(255, "x"));         // "ff"

repr()
~~~~~~

.. function:: repr(obj)

   Get string representation of object.

   :param obj: Object to represent
   :returns: String representation

   .. code-block:: ml

      print(repr(42));         // "42"
      print(repr(true));       // "true"
      print(repr("hello"));    // "'hello'"

callable()
~~~~~~~~~~

.. function:: callable(obj)

   Check if object is callable.

   :param obj: Object to check
   :returns: true if callable

   .. code-block:: ml

      print(callable(print));           // true
      print(callable(42));              // false

      function greet() { return "hi"; }
      print(callable(greet));           // true

all()
~~~~~

.. function:: all(iterable)

   Check if all elements are truthy.

   :param iterable: Array to check
   :returns: true if all elements truthy

   .. code-block:: ml

      print(all([true, true, true]));    // true
      print(all([true, false, true]));   // false
      print(all([1, 2, 3]));             // true
      print(all([1, 0, 3]));             // false

any()
~~~~~

.. function:: any(iterable)

   Check if any element is truthy.

   :param iterable: Array to check
   :returns: true if any element truthy

   .. code-block:: ml

      print(any([false, false, true]));  // true
      print(any([false, false, false])); // false
      print(any([0, 0, 1]));             // true

reversed()
~~~~~~~~~~

.. function:: reversed(seq)

   Return reversed sequence.

   :param seq: Sequence to reverse
   :returns: Reversed array

   .. code-block:: ml

      print(reversed([1, 2, 3]));   // [3, 2, 1]
      print(reversed("hello"));     // ['o', 'l', 'l', 'e', 'h']

Iterator Functions
------------------

Advanced iteration control for custom iteration patterns.

iter()
~~~~~~

.. function:: iter(iterable)

   Create iterator from iterable.

   :param iterable: Sequence (array, string, etc.)
   :returns: Iterator object

   .. code-block:: ml

      it = iter([1, 2, 3]);
      print(next(it));  // 1
      print(next(it));  // 2

next()
~~~~~~

.. function:: next(iterator, default)

   Get next item from iterator.

   :param iterator: Iterator object
   :param default: Value to return if exhausted (optional)
   :returns: Next item or default

   .. code-block:: ml

      it = iter([1, 2, 3]);
      print(next(it));           // 1
      print(next(it));           // 2
      print(next(it));           // 3
      print(next(it, "done"));   // "done"

   **Best Practice:** Always provide default to avoid errors.

Complete Examples
-----------------

Type Conversion
~~~~~~~~~~~~~~~

.. literalinclude:: ../../ml_snippets/standard-library/builtin/01_type_conversion.ml
   :language: ml
   :caption: Complete type conversion examples

Type Checking and Dynamic Typing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../ml_snippets/standard-library/builtin/02_type_checking.ml
   :language: ml
   :caption: Dynamic type checking and polymorphic functions

Introspection and Discovery
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../ml_snippets/standard-library/builtin/03_introspection.ml
   :language: ml
   :caption: Discovering the language through introspection

Collections and Iteration
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../ml_snippets/standard-library/builtin/04_collections.ml
   :language: ml
   :caption: Working with collections

I/O and Formatting
~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../ml_snippets/standard-library/builtin/05_io_formatting.ml
   :language: ml
   :caption: Input/output and number formatting

Utility Functions
~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../ml_snippets/standard-library/builtin/06_utilities.ml
   :language: ml
   :caption: Mathematical and logical utilities

Comprehensive Example
~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../ml_snippets/standard-library/builtin/07_comprehensive_example.ml
   :language: ml
   :caption: Dynamic data processing system

Best Practices
--------------

1. **Type Conversion Safety**

   Rely on safe defaults instead of exception handling:

   .. code-block:: ml

      // Good - handles errors gracefully
      age = int(userInput);  // Returns 0 on error
      if (age > 0) {
          // Valid age
      }

2. **Type-Based Dispatch**

   Use typeof() for polymorphic behavior:

   .. code-block:: ml

      function process(value) {
          type = typeof(value);
          if (type == "number") {
              return value * 2;
          } elif (type == "string") {
              return value + "!";
          }
      }

3. **Introspection for Validation**

   Use hasattr() for safe object validation:

   .. code-block:: ml

      function validateUser(user) {
          if (!hasattr(user, "name") || !hasattr(user, "email")) {
              return false;
          }
          return true;
      }

4. **Discovery-Driven Development**

   Explore modules and methods interactively:

   .. code-block:: ml

      import math;

      // What modules are loaded?
      print(modules());

      // What can math do?
      print(methods(math));

      // Get help on specific functions
      print(help(math.sqrt));

5. **Safe Defaults in Introspection**

   Always provide defaults when accessing attributes:

   .. code-block:: ml

      // Good - provides fallback
      email = getattr(user, "email", "unknown@example.com");

      // Avoid - might get unexpected null
      email = getattr(user, "email");

6. **Boolean Logic with all() and any()**

   Use for elegant validation:

   .. code-block:: ml

      function validateScores(scores) {
          // Check all scores are positive
          checks = [];
          i = 0;
          while (i < len(scores)) {
              checks = checks + [scores[i] > 0];
              i = i + 1;
          }
          return all(checks);
      }

Common Patterns
---------------

Configuration Merging
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   function mergeConfig(defaults, overrides) {
       result = {};

       // Copy defaults
       defaultKeys = keys(defaults);
       i = 0;
       while (i < len(defaultKeys)) {
           key = defaultKeys[i];
           result[key] = defaults[key];
           i = i + 1;
       }

       // Apply overrides
       overrideKeys = keys(overrides);
       i = 0;
       while (i < len(overrideKeys)) {
           key = overrideKeys[i];
           if (hasattr(defaults, key)) {
               result[key] = overrides[key];
           }
           i = i + 1;
       }

       return result;
   }

Type-Safe Function Arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   function divide(a, b) {
       if (!isinstance(a, "number") || !isinstance(b, "number")) {
           return "Error: Arguments must be numbers";
       }

       if (b == 0) {
           return "Error: Division by zero";
       }

       return a / b;
   }

Data Validation Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   function validateRecord(record) {
       required = ["id", "name", "email"];
       errors = [];

       // Check required fields
       i = 0;
       while (i < len(required)) {
           field = required[i];
           if (!hasattr(record, field)) {
               errors = errors + ["Missing field: " + field];
           }
           i = i + 1;
       }

       // Type validation
       if (hasattr(record, "id") && !isinstance(record.id, "number")) {
           errors = errors + ["ID must be a number"];
       }

       return {valid: len(errors) == 0, errors: errors};
   }

Dynamic Object Exploration
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   function exploreObject(obj, objName) {
       print("\nExploring: " + objName);
       print("Type: " + typeof(obj));

       if (typeof(obj) == "object") {
           objKeys = keys(obj);
           print("Properties: " + str(len(objKeys)));

           i = 0;
           while (i < len(objKeys)) {
               key = objKeys[i];
               value = obj[key];
               valueType = typeof(value);
               print("  " + key + ": " + valueType);
               i = i + 1;
           }
       }
   }

Statistical Reduction
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   function analyzeData(values) {
       if (len(values) == 0) {
           return null;
       }

       return {
           count: len(values),
           sum: sum(values),
           min: min(values),
           max: max(values),
           average: sum(values) / len(values),
           sorted: sorted(values)
       };
   }

Security Notes
--------------

The builtin module implements several security features:

**1. Safe Type Conversion**

- ``int()``, ``float()``, ``str()``, ``bool()`` never raise exceptions
- Invalid inputs return sensible defaults (0, 0.0, "0", false)
- No code execution during conversion

**2. Secure Introspection**

- ``hasattr()`` blocks ALL dunder attributes (``__class__``, ``__dict__``, etc.)
- ``getattr()`` routes through SafeAttributeRegistry whitelist
- ``call()`` validates functions against whitelist before execution

**3. Blocked Operations**

- ``call(eval, ...)`` → SecurityError
- ``call(exec, ...)`` → SecurityError
- ``call(compile, ...)`` → SecurityError
- ``call(__import__, ...)`` → SecurityError
- ``getattr(obj, "__class__")`` → returns default value
- ``hasattr(obj, "__dict__")`` → returns false

**4. Safe Defaults**

All introspection functions provide safe fallbacks rather than raising exceptions, preventing information leakage through error messages.

Performance Tips
----------------

1. **Cache typeof() Results**

   .. code-block:: ml

      // Good - check once
      type = typeof(value);
      if (type == "number") { /* ... */ }
      elif (type == "string") { /* ... */ }

      // Avoid - repeated calls
      if (typeof(value) == "number") { /* ... */ }
      elif (typeof(value) == "string") { /* ... */ }

2. **Prefer Direct Access Over getattr()**

   .. code-block:: ml

      // Fast - direct access
      name = obj.name;

      // Slower - dynamic lookup
      name = getattr(obj, "name");

      // Use getattr() only when attribute name is dynamic

3. **Use all()/any() Instead of Loops**

   .. code-block:: ml

      // Clear and efficient
      allPositive = all([v > 0 for v in values]);

      // More verbose
      allPositive = true;
      i = 0;
      while (i < len(values)) {
          if (values[i] <= 0) {
              allPositive = false;
              break;
          }
          i = i + 1;
      }

Conclusion
----------

The ``builtin`` module is the vocabulary of ML programming. Master these 50 functions and you'll have the foundation for elegant, dynamic, and safe ML programs.

**Key Takeaways:**

- Type conversion is safe and never raises exceptions
- Introspection enables discovery-driven development
- Security is built-in, not bolted on
- Dynamic typing + safe introspection = powerful programming

**Next Steps:**

- Explore the :doc:`console` module for logging and debugging
- Learn the :doc:`math` module for mathematical operations
- Master the :doc:`regex` module for text processing
- Build complete applications using all standard library modules
