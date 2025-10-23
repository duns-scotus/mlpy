Standard Library
================

The ML standard library provides essential functionality for everyday programming. All modules use the ``@ml_module``, ``@ml_function``, and ``@ml_class`` decorator system, ensuring consistent security and metadata.

.. toctree::
   :maxdepth: 2

   builtin
   console
   math
   regex
   datetime
   collections
   functional
   random
   json
   file
   http
   path

Library Overview
----------------

The standard library consists of 12 modules organized by functionality:

Core Modules
~~~~~~~~~~~~

:doc:`builtin`
   **47 functions** - The language foundation, always available without import.

   Type conversion, type checking, collections, I/O, introspection, utilities.

   **Key capabilities:** Dynamic typing, safe introspection, type validation.

:doc:`console`
   **6 functions** - Console logging and debugging output.

   Different log levels (log, error, warn, info, debug) for structured logging.

   **Key capabilities:** Stdout/stderr routing, severity-based filtering.

:doc:`math`
   **27 functions + 2 constants** - Mathematical operations.

   Basic math, trigonometry, logarithms, rounding, number theory.

   **Key capabilities:** Full math operations, no external dependencies.

:doc:`regex`
   **48 methods** - Regular expression pattern matching.

   Search, match, replace, split operations with OOP pattern compilation.

   **Key capabilities:** Complete regex support, named groups, flags.

Data & Time Modules
~~~~~~~~~~~~~~~~~~~

:doc:`datetime`
   **5 OOP classes, 94 methods** - Date and time handling.

   Date, Time, DateTime, TimeDelta, TimeZone classes for comprehensive temporal operations.

   **Key capabilities:** Timezone-aware dates, arithmetic, formatting.

:doc:`random`
   **25 methods** - Pseudo-random number generation.

   Various distributions, seed management, shuffle operations.

   **Key capabilities:** Reproducible randomness, multiple distributions.

Data Processing Modules
~~~~~~~~~~~~~~~~~~~~~~~~

:doc:`collections`
   **31 functions** - Functional list operations.

   Pure functional operations on lists without mutation.

   **Key capabilities:** Map, filter, reduce patterns, immutable operations.

:doc:`functional`
   **38 functions** - Advanced functional programming utilities.

   Composition, currying, higher-order functions, advanced FP patterns.

   **Key capabilities:** Function composition, partial application.

:doc:`json`
   **17 functions** - JSON parsing and serialization.

   Parse JSON strings, serialize ML objects, validate structure.

   **Key capabilities:** Bidirectional JSON conversion, validation.

I/O & System Modules
~~~~~~~~~~~~~~~~~~~~

:doc:`file`
   **16 functions** - File system operations.

   Read, write, append, file operations with capability requirements.

   **Key capabilities:** Capability-controlled file access, text and binary modes.

:doc:`path`
   **24 functions** - Path manipulation utilities.

   Join, split, normalize paths, file existence checks.

   **Key capabilities:** Cross-platform path handling.

:doc:`http`
   **20 functions** - HTTP requests and responses.

   GET, POST, PUT, DELETE requests with capability requirements.

   **Key capabilities:** Capability-controlled network access, response parsing.

Using the Standard Library
---------------------------

**No Import Required - builtin**

The ``builtin`` module is always available:

.. code-block:: ml

   // No import needed
   age = int("25");
   print(typeof(age));  // "number"

**Standard Imports**

All other modules require explicit imports:

.. code-block:: ml

   import console;
   import math;
   import regex;

   console.log("Pi is approximately " + str(math.pi));

**Security and Capabilities**

Some modules require capabilities for security-sensitive operations:

.. code-block:: ml

   // File operations require capabilities
   import file with ["file.read", "file.write"];

   content = file.read("data.txt");
   file.write("output.txt", content);

See individual module documentation for capability requirements.

Module Conventions
------------------

**Function Naming**

* camelCase for functions: ``console.log()``, ``math.sqrt()``
* lowercase for boolean constants: ``true``, ``false``
* UPPERCASE for constants: ``math.PI``, ``regex.IGNORECASE()``

**Return Values**

* Errors return sensible defaults (0, empty string, null) not exceptions
* Use null to indicate missing/not-found values
* Boolean functions return ``true``/``false`` (lowercase)

**Parameter Conventions**

* Optional parameters have defaults: ``range(stop)``, ``range(start, stop)``
* Variadic functions use ``*args``: ``print(*values)``
* Flag functions: ``sorted(array, reverse=false)``

**Method Chaining**

OOP modules support method chaining where appropriate:

.. code-block:: ml

   pattern = regex.compile('\\d+');
   result = pattern.search(text);

Common Patterns
---------------

**Type-Safe Operations**

.. code-block:: ml

   function processValue(val) {
       if (isinstance(val, "number")) {
           return val * 2;
       } elif (isinstance(val, "string")) {
           return int(val) * 2;
       }
       return 0;
   }

**Safe Error Handling**

.. code-block:: ml

   // int() returns 0 on error, no exception
   age = int(userInput);
   if (age > 0) {
       console.log("Valid age: " + str(age));
   } else {
       console.error("Invalid input");
   }

**Introspection-Driven Development**

.. code-block:: ml

   import math;

   // Discover capabilities
   print(methods(math));    // List all math functions
   print(help(math.sqrt));  // Get function documentation

**Collection Processing**

.. code-block:: ml

   numbers = range(10);
   doubled = [n * 2 for n in numbers];  // Future: list comprehension
   total = sum(doubled);
   average = total / len(doubled);

Security Model
--------------

**Capability Requirements**

Modules that access system resources require capabilities:

* **file module**: ``file.read``, ``file.write``, ``file.delete``
* **http module**: ``http.request``, ``http.connect``
* **No capabilities**: builtin, console, math, regex, datetime, collections, functional, random, json

**Safe by Default**

Standard library functions:

* Never execute arbitrary code (no eval/exec)
* Block reflection abuse (no ``__class__`` access)
* Validate inputs (type checking built-in)
* Return safe defaults on errors

**Introspection Safety**

Built-in introspection functions (``hasattr``, ``getattr``, ``help``, ``methods``) route through security whitelists, preventing access to dangerous object internals.

Module Development Status
--------------------------

All 12 modules are implemented with the decorator system:

* ✅ **builtin** - Documented (47 functions)
* ✅ **console** - Documented (6 functions)
* ✅ **math** - Documented (27 functions + 2 constants)
* ✅ **regex** - Documented (48 methods across 3 classes)
* 🚧 **datetime** - Implementation complete, documentation pending
* 🚧 **collections** - Implementation complete, documentation pending
* 🚧 **functional** - Implementation complete, documentation pending
* 🚧 **random** - Implementation complete, documentation pending
* 🚧 **json** - Implementation complete, documentation pending
* 🚧 **file** - Implementation complete, documentation pending
* 🚧 **http** - Implementation complete, documentation pending
* 🚧 **path** - Implementation complete, documentation pending

Next Steps
----------

* Start with :doc:`builtin` - The language foundation
* Explore :doc:`console` for debugging and logging
* Learn :doc:`math` for calculations
* Master :doc:`regex` for text processing

For learning ML basics, see the :doc:`../user-guide/tutorial/index`.
