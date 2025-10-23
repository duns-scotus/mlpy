=====================
ML Language Tutorial
=====================

Learn ML programming through hands-on examples, from your first program to building real applications with security-first design.

.. contents:: What You'll Learn
   :local:
   :depth: 2

**Time Investment:** ~2 hours to complete | **Prerequisites:** Basic programming knowledge

What Makes ML Different?
========================

ML is a modern programming language designed with **security-first principles**. Unlike traditional languages where security is an afterthought, ML builds security into every operation through its **capability system**.

Key ML Advantages:

🔒 **Built-in Security**
   Every file, network, or system operation requires explicit permission

⚡ **High Performance**
   Compiles to optimized Python with sub-10ms transpilation

🎯 **Type Safety**
   Optional static typing catches errors before runtime

🔧 **Developer Friendly**
   Excellent tooling with IDE integration and helpful error messages

Chapter 1: Getting Started
===========================

Installation and Setup
----------------------

First, install mlpy and verify it's working:

.. code-block:: bash

   # Install mlpy
   pip install mlpy

   # Verify installation
   mlpy --version

   # Create your first project
   mlpy init hello-world
   cd hello-world

Your First ML Program
---------------------

Let's write the traditional "Hello, World!" program:

.. code-block:: ml

   // hello.ml - Your first ML program
   message = "Hello, ML World!"
   print(message)

Run it with:

.. code-block:: bash

   mlpy run src/main.ml

**What's happening here:**

1. We create a variable ``message`` with a string value
2. We call the built-in ``print`` function to display it
3. ML automatically handles memory management and type inference

Understanding the Build Process
------------------------------

ML is a **transpiled language** - your ML code becomes Python code:

.. code-block:: bash

   # Compile without running
   mlpy compile src/main.ml

   # See the generated Python
   cat dist/main.py

The generated Python is optimized and includes security checks. You get the performance and ecosystem of Python with the safety of ML.

Development Workflow
-------------------

The typical ML development cycle:

.. code-block:: bash

   # 1. Edit your ML files
   vim src/main.ml

   # 2. Run with automatic compilation
   mlpy run src/main.ml

   # 3. Run tests
   mlpy test

   # 4. Format your code
   mlpy format src/

This workflow gives you fast iteration with built-in quality checks.

Chapter 2: Core Language Features
=================================

Variables and Basic Types
------------------------

ML has familiar types with some security enhancements:

.. code-block:: ml

   // Basic types
   name = "Alice"              // string
   age = 25                    // number
   is_active = true            // boolean
   scores = [85, 90, 78, 92]   // array

   // Objects (like dictionaries)
   person = {
       name: "Alice",
       age: 25,
       email: "alice@example.com"
   }

   // Accessing object properties
   print(person.name)          // "Alice"
   print(person["age"])        // 25

**Type Inference:** ML automatically determines types, but you can be explicit:

.. code-block:: ml

   name: string = "Alice"
   age: number = 25
   scores: number[] = [85, 90, 78]

Functions: The Building Blocks
-----------------------------

Functions in ML are first-class values and support modern patterns:

.. code-block:: ml

   // Basic function
   function greet(name) {
       return "Hello, " + name + "!"
   }

   // With type annotations
   function calculateGrade(scores: number[]): string {
       total = 0
       for (i = 0; i < scores.length; i = i + 1) {
           total = total + scores[i]
       }
       average = total / scores.length

       if (average >= 90) {
           return "A"
       } else if (average >= 80) {
           return "B"
       } else if (average >= 70) {
           return "C"
       } else {
           return "F"
       }
   }

   // Using the functions
   greeting = greet("Alice")
   print(greeting)

   student_scores = [85, 90, 78, 92]
   grade = calculateGrade(student_scores)
   print("Grade: " + grade)

Control Flow: Decisions and Loops
---------------------------------

ML provides familiar control structures with some enhancements:

.. code-block:: ml

   // Conditional statements
   function checkAccess(user_role) {
       if (user_role == "admin") {
           return "Full access granted"
       } else if (user_role == "user") {
           return "Limited access granted"
       } else {
           return "Access denied"
       }
   }

   // For loops
   function sumArray(numbers) {
       total = 0
       for (i = 0; i < numbers.length; i = i + 1) {
           total = total + numbers[i]
       }
       return total
   }

   // While loops
   function findFirstEven(numbers) {
       i = 0
       while (i < numbers.length) {
           if (numbers[i] % 2 == 0) {
               return numbers[i]
           }
           i = i + 1
       }
       return null
   }

Arrays and Objects: Data Structures
-----------------------------------

ML provides powerful data manipulation capabilities:

.. code-block:: ml

   // Array operations
   fruits = ["apple", "banana", "orange"]
   fruits.push("grape")            // Add element
   first_fruit = fruits[0]         // Access by index
   fruits[1] = "blueberry"         // Modify element

   // Object operations
   student = {
       name: "Bob",
       grades: [85, 90, 78],
       active: true
   }

   // Add new property
   student.email = "bob@school.edu"

   // Check if property exists
   if ("email" in student) {
       print("Email: " + student.email)
   }

Error Handling: Dealing with Problems
------------------------------------

ML encourages explicit error handling:

.. code-block:: ml

   function safeDivide(a, b) {
       if (b == 0) {
           return {
               success: false,
               error: "Division by zero"
           }
       } else {
           return {
               success: true,
               result: a / b
           }
       }
   }

   // Using the safe function
   result = safeDivide(10, 2)
   if (result.success) {
       print("Result: " + result.result)
   } else {
       print("Error: " + result.error)
   }

Chapter 3: Security-First Programming
=====================================

Understanding Capabilities
--------------------------

ML's most distinctive feature is its **capability system**. Instead of allowing any code to access any resource, ML requires explicit permission.

**Traditional Programming Problem:**

.. code-block:: python

   # Python - any code can do anything
   import os
   os.system("rm -rf /")  # Disaster!

**ML Solution:**

.. code-block:: ml

   // ML - requires explicit capability
   capability (file_write) function saveUserData(data, filename) {
       // Only functions with file_write capability can write files
       writeFile(filename, data)
   }

   // This would fail - no capability declared
   function dangerousFunction() {
       writeFile("important.txt", "deleted!")  // Error: Missing file_write capability
   }

Safe File Operations
-------------------

Working with files safely in ML:

.. code-block:: ml

   // Declare capabilities your function needs
   capability (file_read, file_write) function processConfigFile(filename) {

       // Read configuration
       config_text = readFile(filename)
       if (config_text == null) {
           print("Error: Could not read config file")
           return false
       }

       // Parse and modify configuration
       config = parseJSON(config_text)
       config.last_modified = getCurrentTime()

       // Write back safely
       result = writeFile(filename, stringifyJSON(config))
       return result.success
   }

   // Usage - ML verifies capabilities at compile time
   success = processConfigFile("app-config.json")
   if (success) {
       print("Configuration updated successfully")
   }

Network Access Control
---------------------

Network operations also require explicit permission:

.. code-block:: ml

   capability (network) function fetchWeatherData(city) {
       url = "https://api.weather.com/v1/weather?city=" + city

       response = httpGet(url)
       if (response.status == 200) {
           return parseJSON(response.body)
       } else {
           return {
               error: "Failed to fetch weather data",
               status: response.status
           }
       }
   }

   // Function without network capability cannot make requests
   function localProcessing() {
       // httpGet("http://example.com")  // Would fail at compile time
       return "This function works with local data only"
   }

Avoiding Security Pitfalls
--------------------------

ML helps you avoid common security mistakes:

.. code-block:: ml

   // SQL injection prevention
   capability (database) function getUserByEmail(email) {
       // ML encourages parameterized queries
       query = "SELECT * FROM users WHERE email = ?"
       return executeQuery(query, [email])  // Safe: parameterized

       // This would trigger a security warning:
       // unsafe_query = "SELECT * FROM users WHERE email = '" + email + "'"
       // return executeQuery(unsafe_query)  // Warning: potential injection
   }

   // XSS prevention in web applications
   function renderUserProfile(user_data) {
       // ML automatically escapes output in templates
       return templateRender("profile.html", {
           name: user_data.name,        // Automatically escaped
           bio: user_data.bio           // Safe from XSS
       })
   }

Chapter 4: Advanced Features
============================

Pattern Matching: Elegant Control Flow
--------------------------------------

ML's pattern matching makes complex logic readable:

.. code-block:: ml

   function processApiResponse(response) {
       match response.status {
           200 => {
               data = parseJSON(response.body)
               return { success: true, data: data }
           };
           404 => {
               return { success: false, error: "Resource not found" }
           };
           status when status >= 500 => {
               return { success: false, error: "Server error: " + status }
           };
           _ => {
               return { success: false, error: "Unexpected status: " + response.status }
           };
       }
   }

   // Pattern matching with data structures
   function processUserAction(action) {
       match action {
           { type: "login", username: user } => {
               return authenticateUser(user)
           };
           { type: "logout" } => {
               return clearUserSession()
           };
           { type: "update_profile", data: profile_data } => {
               return updateUserProfile(profile_data)
           };
           _ => {
               return { error: "Unknown action type" }
           };
       }
   }

Type System and Generics
-----------------------

ML supports optional typing for better code quality:

.. code-block:: ml

   // Generic function - works with any type
   function<T> identity(value: T): T {
       return value
   }

   // Type definitions for complex data
   type User = {
       id: number;
       name: string;
       email: string;
       active: boolean;
   }

   type ApiResponse<T> = {
       success: boolean;
       data?: T;
       error?: string;
   }

   // Using typed functions
   function fetchUser(userId: number): ApiResponse<User> {
       // Implementation with proper type checking
       response = apiCall("GET", "/users/" + userId)

       if (response.status == 200) {
           user_data = parseJSON(response.body)
           return {
               success: true,
               data: user_data
           }
       } else {
           return {
               success: false,
               error: "User not found"
           }
       }
   }

Asynchronous Programming
-----------------------

ML supports modern async patterns:

.. code-block:: ml

   // Async function declaration
   async function fetchMultipleUsers(userIds: number[]) {
       results = []

       for (i = 0; i < userIds.length; i = i + 1) {
           userId = userIds[i]
           user_data = await fetchUser(userId)
           results.push(user_data)
       }

       return results
   }

   // Concurrent execution
   async function fetchUsersConcurrently(userIds: number[]) {
       promises = []

       for (i = 0; i < userIds.length; i = i + 1) {
           promise = fetchUser(userIds[i])
           promises.push(promise)
       }

       // Wait for all to complete
       return await Promise.all(promises)
   }

Module System: Organizing Code
-----------------------------

ML supports modular development:

.. code-block:: ml

   // math-utils.ml
   export function add(a: number, b: number): number {
       return a + b
   }

   export function multiply(a: number, b: number): number {
       return a * b
   }

   export function factorial(n: number): number {
       if (n <= 1) {
           return 1
       } else {
           return n * factorial(n - 1)
       }
   }

   // main.ml
   import { add, multiply, factorial } from "./math-utils"

   result1 = add(5, 3)
   result2 = multiply(4, 6)
   result3 = factorial(5)

   print("5 + 3 = " + result1)
   print("4 * 6 = " + result2)
   print("5! = " + result3)

Chapter 5: Real-World Development
=================================

Project Structure Best Practices
--------------------------------

Organize your ML projects for maintainability:

.. code-block:: text

   my-ml-project/
   ├── mlpy.json              # Project configuration
   ├── src/                   # Source code
   │   ├── main.ml            # Entry point
   │   ├── models/            # Data models
   │   │   ├── user.ml
   │   │   └── product.ml
   │   ├── services/          # Business logic
   │   │   ├── auth.ml
   │   │   └── api.ml
   │   └── utils/             # Utility functions
   │       └── helpers.ml
   ├── tests/                 # Test files
   │   ├── test-models.ml
   │   └── test-services.ml
   └── docs/                  # Documentation

Testing Your ML Code
--------------------

ML includes a built-in testing framework:

.. code-block:: ml

   // test-math-utils.ml
   import { add, multiply, factorial } from "../src/math-utils"
   import { assert, assertEqual } from "std/testing"

   function testAddition() {
       result = add(2, 3)
       assertEqual(result, 5, "2 + 3 should equal 5")
   }

   function testMultiplication() {
       result = multiply(4, 5)
       assertEqual(result, 20, "4 * 5 should equal 20")
   }

   function testFactorial() {
       assert(factorial(0) == 1, "0! should equal 1")
       assert(factorial(1) == 1, "1! should equal 1")
       assert(factorial(5) == 120, "5! should equal 120")
   }

   // Run tests
   testAddition()
   testMultiplication()
   testFactorial()

   print("All tests passed!")

Run tests with:

.. code-block:: bash

   mlpy test

Performance Optimization
------------------------

ML provides tools for optimizing performance:

.. code-block:: ml

   // Use appropriate data structures
   function processLargeDataset(data) {
       // For frequent lookups, use objects instead of arrays
       index = {}
       for (i = 0; i < data.length; i = i + 1) {
           item = data[i]
           index[item.id] = item
       }
       return index
   }

   // Cache expensive computations
   calculation_cache = {}

   function expensiveCalculation(input) {
       if (input in calculation_cache) {
           return calculation_cache[input]
       }

       // Perform calculation
       result = complexMathOperation(input)

       // Cache result
       calculation_cache[input] = result
       return result
   }

Deployment Considerations
------------------------

Preparing your ML application for production:

.. code-block:: json

   // mlpy.json - Production configuration
   {
     "name": "my-app",
     "version": "1.0.0",
     "security_level": "strict",
     "allowed_capabilities": [
       "file_read",
       "network"
     ],
     "optimization_level": 2,
     "source_maps": false
   }

Build and deploy:

.. code-block:: bash

   # Build optimized version
   mlpy compile src/ --optimize 2 --output dist/

   # Run security analysis
   mlpy analyze --security --format html --output security-report.html

   # Package for deployment
   tar -czf my-app-v1.0.0.tar.gz dist/ mlpy.json

What's Next?
============

Congratulations! You've learned the fundamentals of ML programming. Here are your next steps:

📖 **Deep Dive**
   - Explore the :doc:`language-reference` for complete syntax details
   - Study the :doc:`standard-library` for available functions
   - Check out the :doc:`cli-reference` for advanced development tools

🛠️ **Practice Projects**
   - Build a simple web server
   - Create a data processing pipeline
   - Write a command-line tool

🔗 **Integration**
   - Learn about :doc:`../integration-guide/python-integration`
   - Set up :doc:`../integration-guide/ide-integration`
   - Explore :doc:`../integration-guide/examples`

🏗️ **Advanced Topics**
   - Study the :doc:`../developer-guide/architecture`
   - Understand the :doc:`../developer-guide/security-model`
   - Learn about :doc:`../developer-guide/extending-mlpy`

**Community Resources:**
   - GitHub Repository: https://github.com/mlpy-dev/mlpy
   - Documentation: https://mlpy.readthedocs.io/
   - Issue Tracker: https://github.com/mlpy-dev/mlpy/issues

Happy ML programming! 🚀