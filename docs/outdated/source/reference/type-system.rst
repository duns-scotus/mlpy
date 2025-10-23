==================
Type System Reference
==================

**Complete Guide to ML Types, Operators, and Type System** - *Master ML's type safety features*

Basic Types
===========

Primitive Types
---------------

.. code-block:: ml

   // String type
   name: string = "Alice"
   message: string = "Hello, World!"
   empty: string = ""

   // Number type (integers and floats)
   age: number = 25
   pi: number = 3.14159
   scientific: number = 1.5e6        // Scientific notation

   // Boolean type
   is_active: boolean = true
   is_complete: boolean = false

   // Null and undefined
   data: string | null = null
   optional: string | undefined = undefined

Type Inference
--------------

.. code-block:: ml

   // ML automatically infers types
   name = "Bob"           // inferred as string
   count = 42             // inferred as number
   active = true          // inferred as boolean

   // Explicit annotation when needed
   user_id: number = getUserId()
   config: object = loadConfiguration()

Collection Types
================

Array Types
-----------

.. code-block:: ml

   // Basic array types
   names: string[] = ["Alice", "Bob", "Carol"]
   scores: number[] = [85, 92, 78, 95]
   flags: boolean[] = [true, false, true]

   // Mixed arrays (use union types)
   mixed: (string | number)[] = ["Alice", 25, "Bob", 30]

   // Nested arrays
   matrix: number[][] = [
       [1, 2, 3],
       [4, 5, 6],
       [7, 8, 9]
   ]

   // Array operations preserve types
   first_name: string = names[0]     // Type: string
   total: number = scores.length     // Type: number

Object Types
------------

.. code-block:: ml

   // Object type annotation
   user: {
       name: string;
       age: number;
       email: string;
       active: boolean;
   } = {
       name: "Alice",
       age: 25,
       email: "alice@example.com",
       active: true
   }

   // Optional properties
   profile: {
       name: string;
       bio?: string;              // Optional property
       avatar?: string;           // May be undefined
   } = {
       name: "Alice"
   }

   // Index signatures for dynamic properties
   config: {
       [key: string]: string;     // Any string key maps to string value
   } = {
       database_url: "localhost",
       api_key: "secret123"
   }

Advanced Types
==============

Union Types
-----------

.. code-block:: ml

   // Union types (value can be one of several types)
   id: string | number = "user123"    // Can be string or number
   result: string | null = getData()  // Can be string or null
   status: "pending" | "complete" | "error" = "pending"

   // Type checking with unions
   function processId(id: string | number) {
       if (typeof(id) == "string") {
           return id.toUpperCase()     // id is string here
       } else {
           return id.toString()        // id is number here
       }
   }

Function Types
--------------

.. code-block:: ml

   // Function type annotations
   calculator: (number, number) => number
   validator: (string) => boolean
   processor: (string[]) => string

   // Function type examples
   calculator = function(a: number, b: number): number {
       return a + b
   }

   validator = function(email: string): boolean {
       return email.includes("@")
   }

   // Higher-order function types
   mapper: ((number) => number) => number[]
   filter: ((string) => boolean) => string[]

Generic Types
-------------

.. code-block:: ml

   // Generic function
   function<T> identity(value: T): T {
       return value
   }

   // Usage with type inference
   str_result = identity("hello")     // T inferred as string
   num_result = identity(42)          // T inferred as number

   // Generic types for collections
   function<T> getFirst(arr: T[]): T | null {
       return arr.length > 0 ? arr[0] : null
   }

   // Multiple type parameters
   function<K, V> createMap(keys: K[], values: V[]): Map<K, V> {
       // Implementation
   }

Type Definitions
================

Custom Types
------------

.. code-block:: ml

   // Type aliases
   type UserId = string
   type Timestamp = number
   type Status = "active" | "inactive" | "pending"

   // Usage
   user_id: UserId = "user_123"
   created_at: Timestamp = getCurrentTime()
   user_status: Status = "active"

   // Complex type definitions
   type User = {
       id: UserId;
       name: string;
       email: string;
       created_at: Timestamp;
       status: Status;
   }

   type ApiResponse<T> = {
       success: boolean;
       data?: T;
       error?: string;
       timestamp: Timestamp;
   }

Interface Types
---------------

.. code-block:: ml

   // Interface for objects
   interface Drawable {
       draw(): void;
       move(x: number, y: number): void;
       getPosition(): { x: number, y: number };
   }

   // Interface for configuration
   interface DatabaseConfig {
       host: string;
       port: number;
       username: string;
       password: string;
       database: string;
   }

   // Extending interfaces
   interface AdminConfig extends DatabaseConfig {
       admin_key: string;
       backup_interval: number;
   }

Operators and Type Coercion
===========================

Arithmetic Operators
--------------------

.. code-block:: ml

   // Type-safe arithmetic
   a: number = 10
   b: number = 3

   result1: number = a + b      // 13 - addition
   result2: number = a - b      // 7 - subtraction
   result3: number = a * b      // 30 - multiplication
   result4: number = a / b      // 3.33... - division
   result5: number = a % b      // 1 - modulo
   result6: number = a ** b     // 1000 - exponentiation

   // String concatenation
   greeting: string = "Hello, " + name + "!"
   formatted: string = `User ${name} is ${age} years old`

Comparison Operators
-------------------

.. code-block:: ml

   // Type-aware comparisons
   a: number = 10
   b: number = 20
   name: string = "Alice"

   is_equal: boolean = a == b           // false - equality
   is_not_equal: boolean = a != b       // true - inequality
   is_less: boolean = a < b             // true - less than
   is_less_equal: boolean = a <= b      // true - less than or equal
   is_greater: boolean = a > b          // false - greater than
   is_greater_equal: boolean = a >= b   // false - greater than or equal

   // String comparisons
   is_same_name: boolean = name == "Alice"     // true
   comes_before: boolean = name < "Bob"        // true (alphabetical)

Logical Operators
-----------------

.. code-block:: ml

   // Boolean logic
   is_active: boolean = true
   is_verified: boolean = false
   age: number = 25

   // Logical AND
   can_access: boolean = is_active && is_verified

   // Logical OR
   needs_review: boolean = !is_verified || age < 18

   // Logical NOT
   is_inactive: boolean = !is_active

   // Null coalescing
   display_name: string = user.nickname ?? user.name ?? "Anonymous"

Type Guards and Checking
========================

Runtime Type Checking
---------------------

.. code-block:: ml

   function processValue(value: string | number | null) {
       // Type checking with typeof
       if (typeof(value) == "string") {
           return value.toUpperCase()        // value is string
       } else if (typeof(value) == "number") {
           return value * 2                  // value is number
       } else {
           return "No value provided"        // value is null
       }
   }

   // Array type checking
   function processData(data: unknown) {
       if (isArray(data)) {
           return data.length               // data is array
       } else if (isObject(data)) {
           return Object.keys(data).length  // data is object
       } else {
           return 0
       }
   }

Property Checking
-----------------

.. code-block:: ml

   // Check object properties
   function getUserEmail(user: object): string | null {
       if ("email" in user && typeof(user.email) == "string") {
           return user.email
       }
       return null
   }

   // Safe property access
   function getNestedValue(obj: object): string | null {
       if ("user" in obj && isObject(obj.user) && "profile" in obj.user) {
           profile = obj.user.profile
           if ("email" in profile && typeof(profile.email) == "string") {
               return profile.email
           }
       }
       return null
   }

Type Conversion
===============

Explicit Conversion
-------------------

.. code-block:: ml

   // String conversions
   num_str: string = toString(42)           // "42"
   bool_str: string = toString(true)        // "true"
   array_str: string = toString([1, 2, 3])  // "[1, 2, 3]"

   // Number conversions
   str_num: number = toNumber("42")         // 42
   bool_num: number = toNumber(true)        // 1
   parsed: number = parseInt("42px")        // 42
   float_parsed: number = parseFloat("3.14") // 3.14

   // Boolean conversions
   str_bool: boolean = toBoolean("true")    // true
   num_bool: boolean = toBoolean(1)         // true
   empty_bool: boolean = toBoolean("")      // false

Safe Type Conversion
--------------------

.. code-block:: ml

   // Safe conversion with validation
   function safeToNumber(value: string): number | null {
       if (isNumericString(value)) {
           return toNumber(value)
       }
       return null
   }

   function safeParseJSON(json: string): object | null {
       try {
           return parseJSON(json)
       } catch (error) {
           return null
       }
   }

Common Type Patterns
====================

Result Type Pattern
-------------------

.. code-block:: ml

   type Result<T, E> = {
       success: boolean;
       data?: T;
       error?: E;
   }

   function divideNumbers(a: number, b: number): Result<number, string> {
       if (b == 0) {
           return { success: false, error: "Division by zero" }
       }
       return { success: true, data: a / b }
   }

   // Usage
   result = divideNumbers(10, 2)
   if (result.success) {
       print("Result:", result.data)    // data is number
   } else {
       print("Error:", result.error)    // error is string
   }

Option Type Pattern
-------------------

.. code-block:: ml

   type Option<T> = T | null

   function findUser(id: string): Option<User> {
       user = database.findById(id)
       return user ?? null
   }

   // Usage with type checking
   user = findUser("123")
   if (user != null) {
       print("Found:", user.name)       // user is User, not null
   } else {
       print("User not found")
   }

Validation Types
----------------

.. code-block:: ml

   type ValidationResult = {
       valid: boolean;
       errors: string[];
   }

   function validateUser(user: object): ValidationResult {
       errors: string[] = []

       if (!("name" in user) || typeof(user.name) != "string") {
           errors.push("Name is required and must be a string")
       }

       if (!("email" in user) || !validateEmail(user.email)) {
           errors.push("Valid email is required")
       }

       if (!("age" in user) || typeof(user.age) != "number" || user.age < 0) {
           errors.push("Age must be a positive number")
       }

       return {
           valid: errors.length == 0,
           errors: errors
       }
   }

Type System Best Practices
==========================

1. **Use Type Annotations**: Be explicit with complex types
2. **Prefer Union Types**: Use `string | null` instead of any
3. **Validate at Boundaries**: Check types when data enters your system
4. **Use Result Types**: Handle errors explicitly with Result<T, E> pattern
5. **Leverage Type Guards**: Use `typeof` and custom type checking functions
6. **Define Custom Types**: Create type aliases for domain-specific data
7. **Keep Types Simple**: Complex types are harder to understand and maintain

Type System Quick Tips
======================

.. code-block:: ml

   // ✅ Good: Clear, explicit types
   function calculateTax(income: number, rate: number): number {
       return income * rate
   }

   // ✅ Good: Union types for nullable values
   function findUser(id: string): User | null {
       return database.find(id) ?? null
   }

   // ✅ Good: Type guards for safety
   function processInput(input: unknown) {
       if (typeof(input) == "string") {
           return input.trim()
       }
       return null
   }

   // ❌ Avoid: Using 'any' type equivalent (object without constraints)
   function badFunction(data) {  // Type unclear
       return data.someProperty  // Unsafe access
   }

**Remember:** ML's type system is designed for safety - embrace type annotations for better code reliability!