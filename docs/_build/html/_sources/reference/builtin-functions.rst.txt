==========================
Built-in Functions Reference
==========================

**Quick Reference for ML Standard Library** - *Essential functions for daily development*

Core Functions
==============

Output and Debugging
--------------------

.. code-block:: ml

   print(value)                    // Output value to console
   print("Hello", name, "!")      // Multiple values
   debug(object)                  // Debug output with details
   assert(condition, message)     // Assertion with custom message

   // Usage examples:
   print("User age:", age)
   debug(user_object)
   assert(age > 0, "Age must be positive")

Type Checking
-------------

.. code-block:: ml

   typeof(value)                  // Get type as string
   isString(value)                // Check if string
   isNumber(value)                // Check if number
   isBoolean(value)               // Check if boolean
   isArray(value)                 // Check if array
   isObject(value)                // Check if object
   isNull(value)                  // Check if null
   isUndefined(value)             // Check if undefined

   // Usage examples:
   type = typeof(user_input)      // Returns "string", "number", etc.
   if (isNumber(input)) {
       result = input * 2
   }

String Functions (std/strings)
==============================

String Manipulation
-------------------

.. code-block:: ml

   // Core string operations
   str.length                     // Get string length
   str.toUpperCase()             // Convert to uppercase
   str.toLowerCase()             // Convert to lowercase
   str.trim()                    // Remove whitespace
   str.replace(old, new)         // Replace substring
   str.split(delimiter)          // Split into array
   str.substring(start, end)     // Extract substring
   str.charAt(index)             // Character at index
   str.indexOf(substring)        // Find substring position

   // Advanced operations
   str.startsWith(prefix)        // Check prefix
   str.endsWith(suffix)          // Check suffix
   str.includes(substring)       // Check if contains
   str.repeat(count)             // Repeat string
   str.padStart(length, char)    // Pad at beginning
   str.padEnd(length, char)      // Pad at end

   // Usage examples:
   email = "  user@example.com  "
   clean_email = email.trim().toLowerCase()
   domain = email.split("@")[1]
   is_gmail = email.includes("gmail.com")

String Formatting
-----------------

.. code-block:: ml

   format(template, ...args)      // String formatting
   sprintf(template, ...args)     // Printf-style formatting
   template(str, variables)       // Template string replacement

   // Usage examples:
   message = format("Hello {}, you are {} years old", name, age)
   formatted = sprintf("Score: %d%%", score)

Array Functions (std/collections)
==================================

Array Operations
---------------

.. code-block:: ml

   // Modification
   arr.push(item)                // Add to end
   arr.pop()                     // Remove from end
   arr.shift()                   // Remove from start
   arr.unshift(item)             // Add to start
   arr.splice(index, count)      // Remove elements
   arr.insert(index, item)       // Insert at position

   // Access and search
   arr.length                    // Array size
   arr.indexOf(item)             // Find item index
   arr.includes(item)            // Check if contains
   arr.slice(start, end)         // Extract subarray
   arr.concat(other_arr)         // Combine arrays

   // Transformation
   arr.join(separator)           // Convert to string
   arr.reverse()                 // Reverse in place
   arr.sort()                    // Sort in place
   arr.sort(compareFn)           // Sort with custom function

   // Usage examples:
   fruits = ["apple", "banana"]
   fruits.push("orange")         // ["apple", "banana", "orange"]
   last = fruits.pop()           // "orange", fruits = ["apple", "banana"]
   text = fruits.join(", ")      // "apple, banana"

Functional Operations
--------------------

.. code-block:: ml

   // Higher-order functions
   arr.map(fn)                   // Transform each element
   arr.filter(fn)                // Keep elements matching condition
   arr.reduce(fn, initial)       // Reduce to single value
   arr.forEach(fn)               // Execute function for each element
   arr.find(fn)                  // Find first matching element
   arr.some(fn)                  // Check if any element matches
   arr.every(fn)                 // Check if all elements match

   // Usage examples:
   numbers = [1, 2, 3, 4, 5]
   doubled = numbers.map(x => x * 2)           // [2, 4, 6, 8, 10]
   evens = numbers.filter(x => x % 2 == 0)     // [2, 4]
   sum = numbers.reduce((acc, x) => acc + x, 0) // 15

Object Functions (std/collections)
===================================

Object Manipulation
-------------------

.. code-block:: ml

   Object.keys(obj)              // Get array of property names
   Object.values(obj)            // Get array of property values
   Object.entries(obj)           // Get array of [key, value] pairs
   Object.assign(target, source) // Copy properties
   Object.hasOwnProperty(obj, key) // Check if property exists

   // Usage examples:
   user = { name: "Alice", age: 25, city: "NYC" }
   names = Object.keys(user)     // ["name", "age", "city"]
   values = Object.values(user)  // ["Alice", 25, "NYC"]
   pairs = Object.entries(user)  // [["name", "Alice"], ["age", 25], ...]

Object Creation
---------------

.. code-block:: ml

   Object.create(prototype)      // Create with prototype
   Object.freeze(obj)            // Make immutable
   Object.seal(obj)              // Prevent property addition
   Object.clone(obj)             // Deep copy object

Math Functions (std/math)
=========================

Basic Math
----------

.. code-block:: ml

   // Constants
   Math.PI                       // 3.14159...
   Math.E                        // 2.71828...

   // Basic operations
   Math.abs(x)                   // Absolute value
   Math.min(a, b, ...)           // Minimum value
   Math.max(a, b, ...)           // Maximum value
   Math.round(x)                 // Round to nearest integer
   Math.floor(x)                 // Round down
   Math.ceil(x)                  // Round up
   Math.trunc(x)                 // Remove decimal part

   // Powers and roots
   Math.pow(base, exponent)      // Power operation
   Math.sqrt(x)                  // Square root
   Math.cbrt(x)                  // Cube root

   // Usage examples:
   distance = Math.abs(x2 - x1)
   area = Math.PI * Math.pow(radius, 2)
   rounded_price = Math.round(price * 100) / 100

Advanced Math
-------------

.. code-block:: ml

   // Trigonometry
   Math.sin(x)                   // Sine
   Math.cos(x)                   // Cosine
   Math.tan(x)                   // Tangent
   Math.asin(x)                  // Arc sine
   Math.acos(x)                  // Arc cosine
   Math.atan(x)                  // Arc tangent

   // Logarithms
   Math.log(x)                   // Natural logarithm
   Math.log10(x)                 // Base-10 logarithm
   Math.exp(x)                   // e^x

   // Random numbers
   Math.random()                 // Random float [0, 1)
   Math.randomInt(min, max)      // Random integer [min, max]

File Operations (std/io) 🔒
===========================

.. note::
   **Requires:** ``file_read`` and/or ``file_write`` capabilities

File Reading
------------

.. code-block:: ml

   capability (file_read) function loadData(path) {
       readFile(path)                    // Read entire file as string
       readFileLines(path)               // Read as array of lines
       readFileBytes(path)               // Read as byte array
       fileExists(path)                  // Check if file exists
       getFileSize(path)                 // Get file size in bytes
       getFileModified(path)             // Get last modified time
   }

   // Usage examples:
   config = readFile("config.json")
   lines = readFileLines("data.txt")
   if (fileExists("backup.dat")) {
       backup = readFile("backup.dat")
   }

File Writing
------------

.. code-block:: ml

   capability (file_write) function saveData(path, content) {
       writeFile(path, content)          // Write string to file
       writeFileLines(path, lines)       // Write array of lines
       appendFile(path, content)         // Append to existing file
       createDirectory(path)             // Create directory
       deleteFile(path)                  // Delete file
       copyFile(source, dest)            // Copy file
       moveFile(source, dest)            // Move/rename file
   }

   // Usage examples:
   writeFile("output.txt", processed_data)
   appendFile("log.txt", timestamp + ": " + message)
   createDirectory("results")

Network Operations (std/http) 🔒
=================================

.. note::
   **Requires:** ``network`` capability

HTTP Client
-----------

.. code-block:: ml

   capability (network) function fetchData(url) {
       httpGet(url)                      // GET request
       httpPost(url, data)               // POST request
       httpPut(url, data)                // PUT request
       httpDelete(url)                   // DELETE request
       httpRequest(method, url, options) // Custom request
   }

   // Response object properties:
   response.status                       // Status code (200, 404, etc.)
   response.headers                      // Response headers
   response.body                         // Response body
   response.ok                           // True if status 200-299

   // Usage examples:
   weather = httpGet("https://api.weather.com/current")
   if (weather.ok) {
       data = parseJSON(weather.body)
       temperature = data.temperature
   }

JSON Operations (std/json)
==========================

JSON Processing
---------------

.. code-block:: ml

   parseJSON(json_string)        // Parse JSON string to object
   stringifyJSON(object)         // Convert object to JSON string
   stringifyJSON(obj, indent)    // Pretty-print with indentation

   // Usage examples:
   config_obj = parseJSON(config_text)
   json_output = stringifyJSON(results, 2)  // 2-space indentation

Time and Date (std/time)
========================

Current Time
------------

.. code-block:: ml

   getCurrentTime()              // Current timestamp
   getCurrentDate()              // Current date object
   now()                         // Current time in milliseconds

Date Operations
---------------

.. code-block:: ml

   formatDate(date, format)      // Format date as string
   parseDate(date_string)        // Parse date from string
   addDays(date, days)           // Add days to date
   addHours(date, hours)         // Add hours to date
   getDayOfWeek(date)            // Get day of week (0-6)
   getMonth(date)                // Get month (1-12)
   getYear(date)                 // Get year

   // Usage examples:
   today = getCurrentDate()
   formatted = formatDate(today, "YYYY-MM-DD")
   next_week = addDays(today, 7)

Async Operations (std/async)
============================

Async Utilities
---------------

.. code-block:: ml

   sleep(milliseconds)           // Pause execution
   timeout(fn, milliseconds)     // Execute after delay
   interval(fn, milliseconds)    // Execute repeatedly

   // Promise utilities
   Promise.all(promises)         // Wait for all promises
   Promise.race(promises)        // Wait for first promise
   Promise.resolve(value)        // Create resolved promise
   Promise.reject(error)         // Create rejected promise

Testing Functions (std/testing)
===============================

Assertions
----------

.. code-block:: ml

   // Test assertions
   assert.equal(actual, expected, message)      // Test equality
   assert.notEqual(actual, expected, message)   // Test inequality
   assert.true(condition, message)              // Test true condition
   assert.false(condition, message)             // Test false condition
   assert.null(value, message)                  // Test null value
   assert.throws(fn, message)                   // Test exception thrown

   // Usage in tests:
   function testCalculation() {
       result = add(2, 3)
       assert.equal(result, 5, "2 + 3 should equal 5")
   }

Security Functions 🔒
=====================

.. note::
   **Requires:** Appropriate security capabilities

Cryptographic Operations
-----------------------

.. code-block:: ml

   capability (crypto) function secureOperations() {
       hash(data, algorithm)             // Hash data (SHA-256, etc.)
       encrypt(data, key, algorithm)     // Encrypt data
       decrypt(data, key, algorithm)     // Decrypt data
       generateKey(algorithm)            // Generate cryptographic key
       randomBytes(length)               // Generate random bytes
   }

Input Validation
----------------

.. code-block:: ml

   sanitizeInput(input)          // Clean user input
   validateEmail(email)          // Validate email format
   validateURL(url)              // Validate URL format
   escapeHTML(html)              // Escape HTML characters
   escapeSQLstring)             // Escape SQL string

Common Usage Patterns
====================

Error Handling with Built-ins
-----------------------------

.. code-block:: ml

   capability (file_read) function safeReadFile(path) {
       if (!fileExists(path)) {
           return { success: false, error: "File not found" }
       }

       try {
           content = readFile(path)
           return { success: true, data: content }
       } catch (error) {
           return { success: false, error: error.message }
       }
   }

Data Processing Pipeline
-----------------------

.. code-block:: ml

   function processUserData(raw_data) {
       // Parse and validate
       users = parseJSON(raw_data)
       valid_users = users.filter(user => validateEmail(user.email))

       // Transform
       processed = valid_users.map(user => ({
           id: user.id,
           name: user.name.trim().toLowerCase(),
           domain: user.email.split("@")[1]
       }))

       // Group and count
       domains = processed.reduce((acc, user) => {
           acc[user.domain] = (acc[user.domain] || 0) + 1
           return acc
       }, {})

       return {
           users: processed,
           domain_stats: domains,
           total: processed.length
       }
   }

**Remember:** Functions marked with 🔒 require explicit capabilities in your function declaration!