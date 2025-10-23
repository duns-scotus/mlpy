=====================
ML Syntax Cheat Sheet
=====================

**Quick Reference for ML Language Syntax** - *Print and keep handy!*

Basic Syntax
============

Variables and Types
-------------------

.. code-block:: ml

   // Variables (type inferred)
   name = "Alice"
   age = 25
   active = true
   scores = [85, 90, 78]

   // Explicit types
   name: string = "Alice"
   age: number = 25
   is_admin: boolean = false
   items: string[] = ["a", "b", "c"]

   // Objects
   user = {
       name: "Alice",
       age: 25,
       email: "alice@example.com"
   }

Functions
---------

.. code-block:: ml

   // Basic function
   function greet(name) {
       return "Hello, " + name + "!"
   }

   // Typed function
   function add(x: number, y: number): number {
       return x + y
   }

   // With capability
   capability (file_read) function loadConfig(path: string) {
       return readFile(path)
   }

Control Flow
============

Conditionals
------------

.. code-block:: ml

   // If/else
   if (score >= 90) {
       grade = "A"
   } else if (score >= 80) {
       grade = "B"
   } else {
       grade = "F"
   }

   // Ternary operator
   status = age >= 18 ? "adult" : "minor"

Loops
-----

.. code-block:: ml

   // For loop
   for (i = 0; i < items.length; i = i + 1) {
       print(items[i])
   }

   // While loop
   i = 0
   while (i < 10) {
       print(i)
       i = i + 1
   }

   // For-in loop (arrays)
   for (item in items) {
       print(item)
   }

Pattern Matching
---------------

.. code-block:: ml

   match status_code {
       200 => {
           return "Success"
       };
       404 => {
           return "Not Found"
       };
       code when code >= 500 => {
           return "Server Error"
       };
       _ => {
           return "Unknown"
       };
   }

Data Structures
===============

Arrays
------

.. code-block:: ml

   // Creation
   fruits = ["apple", "banana", "orange"]
   numbers = [1, 2, 3, 4, 5]

   // Access and modification
   first = fruits[0]              // "apple"
   fruits[1] = "blueberry"        // modify
   fruits.push("grape")           // append
   length = fruits.length         // get size

   // Common operations
   fruits.pop()                   // remove last
   fruits.slice(1, 3)             // extract subset
   fruits.join(", ")              // convert to string

Objects
-------

.. code-block:: ml

   // Creation
   person = {
       name: "Bob",
       age: 30,
       active: true
   }

   // Access
   name = person.name             // dot notation
   age = person["age"]            // bracket notation

   // Modification
   person.email = "bob@email.com" // add property
   person.age = 31                // update property
   delete person.active           // remove property

   // Check existence
   if ("email" in person) {
       print("Has email")
   }

Security Features
=================

Capabilities
------------

.. code-block:: ml

   // File operations
   capability (file_read, file_write) function processFile(path) {
       content = readFile(path)
       result = content.toUpperCase()
       writeFile(path + ".processed", result)
       return result
   }

   // Network access
   capability (network) function fetchData(url) {
       response = httpGet(url)
       return parseJSON(response.body)
   }

   // Multiple capabilities
   capability (file_read, network, database) function syncData() {
       // Can access files, network, and database
   }

Error Handling
--------------

.. code-block:: ml

   // Result pattern
   function safeDivide(a, b) {
       if (b == 0) {
           return { success: false, error: "Division by zero" }
       } else {
           return { success: true, result: a / b }
       }
   }

   // Usage
   result = safeDivide(10, 2)
   if (result.success) {
       print("Result: " + result.result)
   } else {
       print("Error: " + result.error)
   }

Operators
=========

Arithmetic
----------

.. code-block:: ml

   a + b          // addition
   a - b          // subtraction
   a * b          // multiplication
   a / b          // division
   a % b          // modulo
   a ** b         // exponentiation

Comparison
----------

.. code-block:: ml

   a == b         // equality
   a != b         // inequality
   a < b          // less than
   a <= b         // less than or equal
   a > b          // greater than
   a >= b         // greater than or equal

Logical
-------

.. code-block:: ml

   a && b         // logical AND
   a || b         // logical OR
   !a             // logical NOT
   a ?? b         // null coalescing

Assignment
----------

.. code-block:: ml

   a = b          // basic assignment
   a += b         // a = a + b
   a -= b         // a = a - b
   a *= b         // a = a * b
   a /= b         // a = a / b

Common Patterns
===============

Input Validation
----------------

.. code-block:: ml

   function validateEmail(email: string): boolean {
       return email.includes("@") && email.includes(".")
   }

   function validateAge(age: number): boolean {
       return age >= 0 && age <= 150
   }

Array Processing
----------------

.. code-block:: ml

   // Filter array
   function filterEven(numbers) {
       result = []
       for (num in numbers) {
           if (num % 2 == 0) {
               result.push(num)
           }
       }
       return result
   }

   // Transform array
   function doubleNumbers(numbers) {
       result = []
       for (num in numbers) {
           result.push(num * 2)
       }
       return result
   }

Object Processing
-----------------

.. code-block:: ml

   // Copy object
   function copyObject(obj) {
       copy = {}
       for (key in Object.keys(obj)) {
           copy[key] = obj[key]
       }
       return copy
   }

   // Merge objects
   function mergeObjects(obj1, obj2) {
       result = copyObject(obj1)
       for (key in Object.keys(obj2)) {
           result[key] = obj2[key]
       }
       return result
   }

Comments and Documentation
==========================

.. code-block:: ml

   // Single line comment

   /*
    * Multi-line comment
    * Use for function documentation
    */

   /**
    * Documentation comment for functions
    * @param name - The user's name
    * @returns A greeting message
    */
   function greet(name: string): string {
       return "Hello, " + name + "!"
   }

Type Annotations
================

.. code-block:: ml

   // Basic types
   name: string
   age: number
   active: boolean

   // Array types
   names: string[]
   scores: number[]

   // Object types
   user: {
       name: string;
       age: number;
       email: string;
   }

   // Function types
   processor: (string) => string
   calculator: (number, number) => number

   // Optional types
   email?: string          // may be undefined
   result: string | null   // may be null

**Remember:** ML prioritizes security - always declare capabilities for system operations!