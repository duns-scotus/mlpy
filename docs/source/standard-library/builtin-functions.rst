==================
Built-in Functions
==================

Built-in functions are available in all ML programs without requiring any imports. They provide essential functionality for type checking, output, and basic operations.

.. contents:: Contents
   :local:
   :depth: 2

Overview
========

ML provides several built-in functions that are automatically available:

- **typeof()** - Universal type checking function
- **print()** - Console output (Python's built-in)
- **getCurrentTime()** - Current timestamp
- **processData()** - Data processing helper

These functions are part of the core runtime and do not require import statements or capability declarations.

Type System Functions
=====================

.. function:: typeof(value)

   Return the type of a value as a string. This is the universal type checking function available in all ML programs.

   :param value: Any value to check the type of
   :type value: any
   :return: Type name as string
   :rtype: string

   **Return Values:**

   - ``"boolean"`` - for boolean values (true/false)
   - ``"number"`` - for integers and floating-point numbers
   - ``"string"`` - for text strings
   - ``"array"`` - for arrays/lists
   - ``"object"`` - for dictionaries/objects
   - ``"function"`` - for callable functions
   - ``"unknown"`` - for any other type

   .. code-block:: ml

      // Type checking examples
      type1 = typeof(42);          // "number"
      type2 = typeof("hello");     // "string"
      type3 = typeof(true);        // "boolean"
      type4 = typeof([1, 2, 3]);   // "array"
      type5 = typeof({x: 1});      // "object"

   **Usage Patterns:**

   .. code-block:: ml

      // Type validation
      function processValue(value) {
          if (typeof(value) == "number") {
              return value * 2;
          } elif (typeof(value) == "string") {
              return "processed: " + value;
          } else {
              return "unsupported type: " + typeof(value);
          }
      }

      // Type-safe operations
      function safeAdd(a, b) {
          if (typeof(a) == "number" && typeof(b) == "number") {
              return a + b;
          } else {
              print("Error: both arguments must be numbers");
              return 0;
          }
      }

   **Implementation Details:**

   - Available universally across all ML programs
   - Added to standard library in January 2025 session
   - Resolves type checking needs across comprehensive test suite
   - Zero-overhead implementation using Python's isinstance()

Console Output Functions
========================

.. function:: print(message)

   Output text to the console. This is Python's built-in print function.

   :param message: Text or value to display
   :type message: any
   :return: None
   :rtype: void

   .. code-block:: ml

      print("Hello, World!");
      print("Number: " + 42);
      print("Result: " + (10 + 20));

   **Features:**

   - Automatic string conversion for all types
   - Newline automatically added
   - Works with any data type
   - Direct mapping to Python's print()

   **Advanced Usage:**

   .. code-block:: ml

      // Print variables
      name = "Alice";
      age = 30;
      print("Name: " + name + ", Age: " + age);

      // Print calculation results
      result = 5 * 8;
      print("5 * 8 = " + result);

      // Print object information
      user = {name: "Bob", score: 95};
      print("User: " + user.name + " scored " + user.score);

Utility Functions
=================

.. function:: getCurrentTime()

   Get the current timestamp as an ISO format string.

   :return: Current date and time in ISO format
   :rtype: string

   .. code-block:: ml

      timestamp = getCurrentTime();
      print("Current time: " + timestamp);
      // Output: "Current time: 2025-01-15T14:30:45.123456"

   **Format:** ISO 8601 format (YYYY-MM-DDTHH:MM:SS.microseconds)

   **Use Cases:**

   .. code-block:: ml

      // Logging with timestamps
      function logMessage(message) {
          time = getCurrentTime();
          print("[" + time + "] " + message);
      }

      // Measuring execution time (basic)
      start_time = getCurrentTime();
      // ... some operations ...
      end_time = getCurrentTime();
      print("Started: " + start_time);
      print("Ended: " + end_time);

.. function:: processData(data)

   Process input data with a simple transformation (placeholder implementation).

   :param data: Data to process
   :type data: any
   :return: Processed data with "processed_" prefix
   :rtype: string

   .. code-block:: ml

      result = processData("input");
      print(result);  // "processed_input"

      result = processData(123);
      print(result);  // "processed_123"

   **Note:** This is a placeholder function provided for testing and examples.

Type Checking Patterns
======================

The ``typeof()`` function enables powerful type checking patterns:

Runtime Type Validation
-----------------------

.. code-block:: ml

   function validateInput(value, expectedType) {
       actualType = typeof(value);
       if (actualType == expectedType) {
           return true;
       } else {
           print("Type error: expected " + expectedType +
                 ", got " + actualType);
           return false;
       }
   }

   // Usage
   if (validateInput(userInput, "number")) {
       result = userInput * 2;
   }

Polymorphic Functions
--------------------

.. code-block:: ml

   function smartConcat(a, b) {
       type_a = typeof(a);
       type_b = typeof(b);

       if (type_a == "string" || type_b == "string") {
           return a + b;  // String concatenation
       } elif (type_a == "number" && type_b == "number") {
           return a + b;  // Numeric addition
       } elif (type_a == "array" && type_b == "array") {
           return a + b;  // Array concatenation
       } else {
           return "Cannot combine " + type_a + " and " + type_b;
       }
   }

Type-Safe Data Processing
------------------------

.. code-block:: ml

   function processArray(arr) {
       if (typeof(arr) != "array") {
           print("Error: expected array, got " + typeof(arr));
           return [];
       }

       result = [];
       for (i = 0; i < arr.length; i++) {
           item = arr[i];
           if (typeof(item) == "number") {
               result.push(item * 2);
           } elif (typeof(item) == "string") {
               result.push("processed: " + item);
           } else {
               result.push("unknown type: " + typeof(item));
           }
       }
       return result;
   }

Error Handling with Types
=========================

Using built-in functions for robust error handling:

.. code-block:: ml

   function safeOperation(input) {
       try {
           if (typeof(input) == "unknown") {
               print("Warning: unknown input type at " + getCurrentTime());
               return processData("fallback");
           }

           if (typeof(input) == "number") {
               return input * input;  // Square the number
           } elif (typeof(input) == "string") {
               return processData(input);
           } else {
               print("Unsupported type: " + typeof(input));
               return null;
           }
       } catch (error) {
           print("Error occurred at " + getCurrentTime() + ": " + error);
           return processData("error_recovery");
       }
   }

Performance Considerations
==========================

**typeof() Performance:**
- Zero-overhead type checking
- Direct mapping to Python's isinstance()
- No string parsing or reflection overhead
- Cached type lookups for common types

**print() Performance:**
- Direct call to Python's print()
- No formatting overhead unless string concatenation used
- Minimal memory allocation

**Utility Functions:**
- getCurrentTime(): Uses Python's datetime.now().isoformat()
- processData(): Simple string formatting operation

Best Practices
==============

Type Checking Guidelines
-----------------------

.. code-block:: ml

   // ✅ Good: Clear type checking
   if (typeof(value) == "number") {
       // handle number
   }

   // ❌ Avoid: String comparison errors
   if (typeof(value) == "Number") {  // Wrong case
       // this will never match
   }

   // ✅ Good: Defensive programming
   function calculate(x, y) {
       if (typeof(x) != "number" || typeof(y) != "number") {
           print("Error: calculate() requires numbers");
           return 0;
       }
       return x + y;
   }

Output Formatting
----------------

.. code-block:: ml

   // ✅ Good: Clear, informative output
   print("Processing user " + user.id + " at " + getCurrentTime());

   // ✅ Good: Structured logging
   function debug(level, message) {
       if (typeof(level) == "string" && typeof(message) == "string") {
           print("[" + level + "] " + getCurrentTime() + ": " + message);
       }
   }

   debug("INFO", "System initialized");
   debug("ERROR", "Failed to process data");

Security Considerations
======================

Built-in functions are designed with security in mind:

**Type Safety:**
- typeof() prevents type confusion attacks
- Returns safe string values, never throws exceptions
- Consistent behavior across all data types

**Output Security:**
- print() safely converts all types to strings
- No code injection possible through print statements
- Automatic escaping of special characters

**Utility Security:**
- getCurrentTime() uses system time, no external dependencies
- processData() performs safe string operations only
- No capability requirements for built-in functions

Examples and Use Cases
======================

Data Validation System
----------------------

.. code-block:: ml

   function validateUser(user) {
       if (typeof(user) != "object") {
           print("Invalid user: expected object, got " + typeof(user));
           return false;
       }

       if (typeof(user.name) != "string") {
           print("Invalid user.name: expected string, got " + typeof(user.name));
           return false;
       }

       if (typeof(user.age) != "number") {
           print("Invalid user.age: expected number, got " + typeof(user.age));
           return false;
       }

       print("User validation passed at " + getCurrentTime());
       return true;
   }

   // Usage
   user1 = {name: "Alice", age: 30};
   user2 = {name: "Bob", age: "invalid"};

   validateUser(user1);  // true
   validateUser(user2);  // false, prints error

Dynamic Function Dispatch
-------------------------

.. code-block:: ml

   function dynamicProcess(data) {
       timestamp = getCurrentTime();
       print("Processing data at " + timestamp);

       dataType = typeof(data);

       if (dataType == "array") {
           return processArray(data);
       } elif (dataType == "object") {
           return processObject(data);
       } elif (dataType == "string") {
           return processData(data);
       } else {
           print("Unsupported data type: " + dataType);
           return processData("unsupported");
       }
   }

See Also
========

- :doc:`string` - String manipulation functions
- :doc:`console` - Advanced console operations
- :doc:`../user-guide/language-reference` - ML language syntax reference