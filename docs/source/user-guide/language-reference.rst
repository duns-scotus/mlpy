==================
Language Reference
==================

Complete ML language specification and syntax reference for mlpy v2.0.

.. contents:: Table of Contents
   :local:
   :depth: 3

Overview
========

ML is a security-first programming language that transpiles to Python. It combines familiar syntax with capability-based security, static analysis, and modern language features.

**Key Characteristics:**

- **Security-First Design**: Capability system prevents unauthorized resource access
- **Static Analysis**: Compile-time detection of security vulnerabilities and code issues
- **Python Interoperability**: Transpiles to readable, optimized Python code
- **Modern Syntax**: Support for pattern matching, generics, and advanced control flow
- **Type Safety**: Optional static typing with inference

Basic Syntax
============

Comments
--------

ML supports single-line comments using ``//``:

.. code-block:: ml

   // This is a single-line comment
   x = 42  // Comment after code

   // Multi-line comments can be created
   // by using multiple single-line comments

Identifiers
-----------

Identifiers must start with a letter or underscore, followed by letters, digits, or underscores:

.. code-block:: ml

   // Valid identifiers
   userName
   _privateVar
   counter123
   MAX_SIZE

   // Invalid identifiers
   // 123invalid  // Cannot start with digit
   // user-name   // Hyphens not allowed

Keywords
--------

Reserved words in ML:

.. code-block:: text

   and          as           break        capability   continue
   elif         else         except       execute      false
   finally      fn           for          function     if
   import       in           network      null         or
   read         return       system       true         try
   while        write

Literals
========

Number Literals
---------------

ML supports integers, floats, and scientific notation:

.. code-block:: ml

   // Integer literals
   count = 42
   negative = -17
   zero = 0

   // Float literals
   price = 19.99
   percentage = 0.75
   pi = 3.14159

   // Scientific notation
   large_number = 1.5e6      // 1,500,000
   small_number = 6.626e-34  // Very small number
   avogadro = 6.022e23       // Avogadro's number

String Literals
---------------

Strings can use single or double quotes:

.. code-block:: ml

   // String literals
   name = "Alice"
   greeting = 'Hello, World!'

   // Escape sequences
   message = "She said, \"Hello!\""
   path = "C:\\Users\\Documents"
   newline = "Line 1\nLine 2"

Boolean Literals
----------------

ML has two boolean values:

.. code-block:: ml

   is_active = true
   is_disabled = false

Null Literal
------------

The absence of a value:

.. code-block:: ml

   result = null

Data Types
==========

Primitive Types
---------------

**Numbers**
  All numeric values (integers and floats)

**Strings**
  Text data with UTF-8 support

**Booleans**
  ``true`` or ``false`` values

**Null**
  Represents absence of value

Collection Types
----------------

Arrays
~~~~~~

Ordered collections of values:

.. code-block:: ml

   // Array creation
   numbers = [1, 2, 3, 4, 5]
   mixed = [42, "hello", true, null]
   empty = []

   // Array access
   first = numbers[0]        // 1
   last = numbers[4]         // 5

   // Array modification
   numbers[0] = 10          // [10, 2, 3, 4, 5]

Objects
~~~~~~~

Key-value collections (similar to dictionaries/maps):

.. code-block:: ml

   // Object creation
   person = {
       name: "Alice",
       age: 30,
       active: true
   }

   // Property access (dot notation)
   name = person.name        // "Alice"

   // Property access (bracket notation)
   age = person["age"]       // 30

   // Property assignment
   person.email = "alice@example.com"
   person["phone"] = "555-1234"

Variables
=========

Declaration and Assignment
--------------------------

Variables are declared through assignment:

.. code-block:: ml

   // Basic assignment
   x = 42
   name = "Alice"
   active = true

   // Variables can be reassigned
   x = 100
   name = "Bob"

Type Annotations (Optional)
---------------------------

You can optionally specify types for better documentation and error checking:

.. code-block:: ml

   // Explicit type annotations
   count: number = 0
   message: string = "Hello"
   active: boolean = true

   // Array types
   scores: number[] = [85, 90, 78]
   names: string[] = ["Alice", "Bob", "Carol"]

   // Object types (future feature)
   // user: User = { name: "Alice", age: 30 }

Operators
=========

Arithmetic Operators
--------------------

.. code-block:: ml

   // Basic arithmetic
   sum = a + b              // Addition
   difference = a - b       // Subtraction
   product = a * b          // Multiplication
   quotient = a / b         // Division
   remainder = a % b        // Modulo

   // Unary operators
   positive = +x            // Unary plus
   negative = -x            // Unary minus

Comparison Operators
--------------------

.. code-block:: ml

   // Equality
   equal = (a == b)         // Equal
   not_equal = (a != b)     // Not equal

   // Relational
   less_than = (a < b)      // Less than
   greater_than = (a > b)   // Greater than
   less_equal = (a <= b)    // Less than or equal
   greater_equal = (a >= b) // Greater than or equal

Logical Operators
-----------------

.. code-block:: ml

   // Logical operations
   and_result = (a && b)    // Logical AND
   or_result = (a || b)     // Logical OR
   not_result = !a          // Logical NOT

String Concatenation
--------------------

The ``+`` operator concatenates strings:

.. code-block:: ml

   greeting = "Hello, " + name + "!"
   full_path = directory + "/" + filename

Control Flow
============

Conditional Statements
----------------------

If-Elif-Else
~~~~~~~~~~~~

.. code-block:: ml

   // Simple if statement
   if (score >= 90) {
       grade = "A"
   }

   // If-else statement
   if (temperature > 30) {
       print("It's hot!")
   } else {
       print("It's not hot.")
   }

   // If-elif-else chain
   if (score >= 90) {
       grade = "A"
   } elif (score >= 80) {
       grade = "B"
   } elif (score >= 70) {
       grade = "C"
   } elif (score >= 60) {
       grade = "D"
   } else {
       grade = "F"
   }

Ternary Operator (Future Feature)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   // Planned feature
   // result = condition ? true_value : false_value

Loops
-----

While Loops
~~~~~~~~~~~

.. code-block:: ml

   // Basic while loop
   i = 0
   while (i < 10) {
       print("Count: " + i)
       i = i + 1
   }

   // Condition-based loop
   running = true
   while (running) {
       input = getUserInput()
       if (input == "quit") {
           running = false
       }
       processInput(input)
   }

For Loops
~~~~~~~~~

.. code-block:: ml

   // For-in loop (array iteration)
   numbers = [1, 2, 3, 4, 5]
   for (num in numbers) {
       print("Number: " + num)
   }

   // Traditional for loop (future feature)
   // for (i = 0; i < 10; i = i + 1) {
   //     print("Index: " + i)
   // }

Loop Control
~~~~~~~~~~~~

.. code-block:: ml

   // Break statement
   for (item in items) {
       if (item == "stop") {
           break
       }
       processItem(item)
   }

   // Continue statement
   for (number in numbers) {
       if (number % 2 == 0) {
           continue  // Skip even numbers
       }
       print("Odd number: " + number)
   }

Functions
=========

Function Definition
-------------------

.. code-block:: ml

   // Basic function
   function greet(name) {
       return "Hello, " + name + "!"
   }

   // Function with multiple parameters
   function calculateArea(width, height) {
       return width * height
   }

   // Function with type annotations
   function add(a: number, b: number): number {
       return a + b
   }

Function Calls
--------------

.. code-block:: ml

   // Function invocation
   greeting = greet("Alice")
   area = calculateArea(10, 5)
   sum = add(3, 7)

   // Functions can be stored in variables
   operation = add
   result = operation(5, 3)  // Same as add(5, 3)

Return Statements
-----------------

.. code-block:: ml

   // Explicit return
   function multiply(a, b) {
       result = a * b
       return result
   }

   // Early return
   function divide(a, b) {
       if (b == 0) {
           return null  // Handle division by zero
       }
       return a / b
   }

   // Functions without return statement return null
   function printMessage(message) {
       print(message)
       // Implicitly returns null
   }

Arrow Functions (Future Feature)
--------------------------------

.. code-block:: ml

   // Planned feature
   // multiply = fn(a, b) => a * b
   // square = fn(x) => x * x

Exception Handling
==================

Try-Except-Finally
-------------------

.. code-block:: ml

   // Basic exception handling
   try {
       result = riskyOperation()
       print("Success: " + result)
   } except {
       print("An error occurred")
   }

   // Exception with variable binding
   try {
       data = parseJSON(input)
       processData(data)
   } except (error) {
       print("Parse error: " + error)
   }

   // Try-except-finally
   try {
       file = openFile("data.txt")
       content = readFile(file)
       return content
   } except (error) {
       print("File error: " + error)
       return null
   } finally {
       closeFile(file)  // Always executed
   }

Capability System
=================

Capability Declarations
-----------------------

Functions that access restricted resources must declare capabilities:

.. code-block:: ml

   // File operations require capabilities
   capability file_read;
   capability file_write;

   function saveUserData(data, filename) {
       // This function can read and write files
       existing = readFile(filename)
       updated = mergeData(existing, data)
       writeFile(filename, updated)
   }

   // Network operations
   capability network;

   function fetchData(url) {
       response = httpGet(url)
       return response.body
   }

Built-in Capabilities
---------------------

ML defines several standard capabilities:

**file_read**
  Permission to read files from disk

**file_write**
  Permission to write files to disk

**network**
  Permission to make network requests

**execute**
  Permission to execute system commands

**system**
  Permission to access system resources

Resource Patterns (Future Feature)
-----------------------------------

.. code-block:: ml

   // Planned: Fine-grained resource control
   // capability file_read("./data/*.json");
   // capability network("https://api.example.com/*");

Import System
=============

Import Statements
-----------------

.. code-block:: ml

   // Import standard library modules
   import collections;
   import math;
   import random;

   // Import with alias
   import collections as col;

   // Using imported modules
   list = collections.append([], "item")
   sqrt_value = math.sqrt(16)
   random_num = random.randomInt(1, 100)

Standard Library Modules
-------------------------

**collections**
  Array and object manipulation functions

**math**
  Mathematical functions and constants

**random**
  Random number generation

**console**
  Console output and formatting

**datetime**
  Date and time operations

Pattern Matching (Future Feature)
==================================

Match Expressions
-----------------

.. code-block:: ml

   // Planned feature
   // function processResponse(response) {
   //     match response.status {
   //         200 => handleSuccess(response.data);
   //         404 => handleNotFound();
   //         status when status >= 500 => handleServerError(status);
   //         _ => handleUnexpected(response.status);
   //     }
   // }

Advanced Features (Future)
==========================

Generics
--------

.. code-block:: ml

   // Planned feature
   // function<T> identity(value: T): T {
   //     return value
   // }

Async/Await
-----------

.. code-block:: ml

   // Planned feature
   // async function fetchUserData(userId) {
   //     user = await fetchUser(userId)
   //     profile = await fetchProfile(userId)
   //     return { user, profile }
   // }

Module System
-------------

.. code-block:: ml

   // Planned feature
   // export function publicFunction() { ... }
   // export { func1, func2 }
   //
   // import { publicFunction } from "./module"

Grammar Summary
===============

This is the complete ML grammar in EBNF notation:

.. code-block:: ebnf

   program := (capability_declaration | import_statement | statement)*

   capability_declaration := "capability" capability_name "{" capability_item* "}"
   capability_name := IDENTIFIER
   capability_item := resource_pattern ";" | permission_grant ";"
   resource_pattern := "resource" STRING
   permission_grant := "allow" permission_type permission_target?
   permission_type := "read" | "write" | "execute" | "network" | "system"

   import_statement := "import" import_target ("as" IDENTIFIER)? ";"
   import_target := IDENTIFIER ("." IDENTIFIER)*

   function_definition := "function" IDENTIFIER "(" parameter_list? ")" "{" statement* "}"
   parameter_list := parameter ("," parameter)*
   parameter := IDENTIFIER (":" type_annotation)?
   type_annotation := IDENTIFIER

   statement := expression_statement
             | assignment_statement
             | function_definition
             | if_statement
             | while_statement
             | for_statement
             | return_statement
             | try_statement
             | break_statement
             | continue_statement

   if_statement := "if" "(" expression ")" statement_block elif_clause* ("else" statement_block)?
   elif_clause := "elif" "(" expression ")" statement_block
   statement_block := "{" statement* "}"

   while_statement := "while" "(" expression ")" "{" statement* "}"
   for_statement := "for" "(" IDENTIFIER "in" expression ")" "{" statement* "}"

   try_statement := "try" "{" statement* "}" except_clause* finally_clause?
   except_clause := "except" ("(" IDENTIFIER ")")? "{" statement* "}"
   finally_clause := "finally" "{" statement* "}"

   expression := ternary
   ternary := logical_or | logical_or "?" expression ":" expression
   logical_or := logical_and | logical_or "||" logical_and
   logical_and := equality | logical_and "&&" equality
   equality := comparison | equality ("==" | "!=") comparison
   comparison := addition | comparison ("<" | ">" | "<=" | ">=") addition
   addition := multiplication | addition ("+" | "-") multiplication
   multiplication := unary | multiplication ("*" | "/" | "%") unary
   unary := primary | ("!" | "-") unary

   primary := literal | IDENTIFIER | function_call | array_access | member_access | "(" expression ")"

   function_call := (IDENTIFIER | member_access) "(" argument_list? ")"
   argument_list := expression ("," expression)*
   array_access := primary "[" expression "]"
   member_access := primary "." IDENTIFIER

   literal := NUMBER | STRING | BOOLEAN | array_literal | object_literal
   array_literal := "[" (expression ("," expression)*)? "]"
   object_literal := "{" (object_property ("," object_property)*)? "}"
   object_property := (IDENTIFIER | STRING) ":" expression

   // Tokens
   BOOLEAN := "true" | "false"
   IDENTIFIER := /[a-zA-Z_][a-zA-Z0-9_]*/
   NUMBER := /\d+(\.\d+)?([eE][+-]?\d+)?/
   STRING := /"([^"\\]|\\.)*"/ | /'([^'\\]|\\.)*'/

Best Practices
==============

Naming Conventions
------------------

.. code-block:: ml

   // Variables and functions: camelCase
   userName = "alice"
   calculateTotal = function() { ... }

   // Constants: UPPER_CASE
   MAX_RETRIES = 3
   API_BASE_URL = "https://api.example.com"

   // Capabilities: snake_case
   capability file_read;
   capability network_access;

Code Organization
-----------------

.. code-block:: ml

   // 1. Capability declarations at top
   capability file_read;
   capability network;

   // 2. Import statements
   import collections;
   import math;

   // 3. Constants
   MAX_ITEMS = 100
   DEFAULT_TIMEOUT = 5000

   // 4. Function definitions
   function processData(input) {
       // Function implementation
   }

   // 5. Main execution code
   main()

Security Guidelines
------------------

1. **Principle of Least Privilege**: Only declare capabilities you actually need
2. **Validate Input**: Always check user input for security issues
3. **Use Parameterized Queries**: Avoid string concatenation for SQL queries
4. **Handle Errors Gracefully**: Don't expose sensitive information in error messages

Error Handling Patterns
-----------------------

.. code-block:: ml

   // Return result objects for error handling
   function safeOperation(input) {
       if (input == null) {
           return {
               success: false,
               error: "Input cannot be null"
           }
       }

       try {
           result = performOperation(input)
           return {
               success: true,
               data: result
           }
       } except (error) {
           return {
               success: false,
               error: "Operation failed: " + error
           }
       }
   }

   // Usage
   result = safeOperation(userInput)
   if (result.success) {
       processData(result.data)
   } else {
       print("Error: " + result.error)
   }

This completes the ML Language Reference. For additional information, see:

- :doc:`tutorial` for hands-on learning
- :doc:`standard-library` for built-in functions
- :doc:`../developer-guide/security-model` for security details