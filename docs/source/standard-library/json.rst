====
json
====

.. module:: json
   :synopsis: JSON parsing, serialization, and validation with security features

The ``json`` module provides comprehensive JSON parsing, serialization, validation, and manipulation capabilities with built-in security features to protect against deeply nested JSON attacks.

Overview
========

The json module enables ML programs to work with JSON data through a complete set of parsing, validation, and utility functions. All operations follow JSON specifications while providing additional safety through depth-limited parsing and comprehensive type checking.

Key Features
------------

- **Parsing & Serialization**: Convert between JSON strings and ML objects
- **Validation**: Verify JSON syntax before parsing
- **Type Checking**: Runtime type inspection for JSON values
- **Utilities**: Object manipulation with keys, values, and merging
- **Security**: Depth-limited parsing to prevent DoS attacks
- **Pretty Printing**: Human-readable JSON formatting

Usage
=====

Import the json module to access all JSON functionality:

.. code-block:: ml

    import json;

    // Parse JSON string
    data = json.parse('{"name": "Alice", "age": 30}');
    console.log("Name: " + data.name);

    // Validate before parsing
    if (json.validate(jsonString)) {
        data = json.safeParse(jsonString, 20);
    }

    // Serialize to JSON
    jsonStr = json.stringify({status: "success", count: 42});

Core Functions
==============

Parsing and Serialization
--------------------------

parse
^^^^^

.. function:: parse(jsonString)

   Parse a JSON string into an ML object, array, or primitive value.

   :param jsonString: Valid JSON string to parse
   :type jsonString: string
   :return: Parsed ML value (object, array, string, number, boolean, or null)
   :raises: Error if JSON syntax is invalid

   **Examples:**

   .. code-block:: ml

       // Parse object
       person = json.parse('{"name": "Alice", "age": 30}');
       console.log(person.name);  // "Alice"

       // Parse array
       numbers = json.parse('[1, 2, 3, 4, 5]');
       console.log(numbers[0]);  // 1

       // Parse nested structure
       data = json.parse('{"user": {"name": "Bob", "scores": [85, 92, 78]}}');
       console.log(data.user.scores[1]);  // 92

       // Parse primitives
       num = json.parse("42");        // 42
       bool = json.parse("true");     // true
       str = json.parse('"hello"');   // "hello"

   **Use Cases:**

   - Processing API responses
   - Loading configuration files
   - Deserializing stored data
   - Reading JSON from external sources

safeParse
^^^^^^^^^

.. function:: safeParse(jsonString, maxDepth)

   Parse JSON with depth validation to prevent deeply nested JSON attacks.

   :param jsonString: JSON string to parse
   :type jsonString: string
   :param maxDepth: Maximum allowed nesting depth (default 100)
   :type maxDepth: number
   :return: Parsed ML value
   :raises: Error if depth exceeds maxDepth or syntax is invalid

   **Examples:**

   .. code-block:: ml

       // Safe parsing with depth limit
       shallow = '{"name": "Alice", "age": 30}';
       data = json.safeParse(shallow, 10);  // Success (depth 1)

       // Nested structure within limit
       nested = '{"a": {"b": {"c": {"d": "value"}}}}';
       data = json.safeParse(nested, 10);  // Success (depth 4)

       // Validate API responses safely
       apiResponse = '{"status": "success", "data": {"user": {"id": 123}}}';
       response = json.safeParse(apiResponse, 20);

   **Recommended Depth Limits:**

   - User-generated content: 10-20
   - API responses: 20-30
   - Configuration files: 15-25
   - Internal data: 50-100

   **Security Benefits:**

   - Prevents stack overflow attacks
   - Protects against DoS via deeply nested JSON
   - Ensures predictable parsing performance
   - Validates data structure complexity

stringify
^^^^^^^^^

.. function:: stringify(value)

   Convert an ML value to a compact JSON string.

   :param value: ML value to serialize
   :type value: any
   :return: JSON string representation
   :rtype: string

   **Examples:**

   .. code-block:: ml

       // Stringify object
       user = {name: "Charlie", age: 25, email: "charlie@example.com"};
       json = json.stringify(user);
       // {"name":"Charlie","age":25,"email":"charlie@example.com"}

       // Stringify array
       items = ["apple", "banana", "cherry"];
       json = json.stringify(items);
       // ["apple","banana","cherry"]

       // Stringify nested structure
       config = {
           server: {host: "localhost", port: 8080},
           enabled: true,
           features: ["auth", "cache"]
       };
       json = json.stringify(config);

   **Use Cases:**

   - Preparing data for API requests
   - Saving configuration to files
   - Serializing application state
   - Generating JSON responses

prettyPrint
^^^^^^^^^^^

.. function:: prettyPrint(value, indent)

   Convert an ML value to a formatted JSON string with indentation.

   :param value: ML value to serialize
   :type value: any
   :param indent: Number of spaces for indentation
   :type indent: number
   :return: Formatted JSON string
   :rtype: string

   **Examples:**

   .. code-block:: ml

       settings = {
           theme: "dark",
           fontSize: 14,
           notifications: {
               email: true,
               push: false
           },
           languages: ["en", "es", "fr"]
       };

       // Pretty print with 2 spaces
       formatted = json.prettyPrint(settings, 2);
       console.log(formatted);
       /* Output:
       {
         "theme": "dark",
         "fontSize": 14,
         "notifications": {
           "email": true,
           "push": false
         },
         "languages": [
           "en",
           "es",
           "fr"
         ]
       }
       */

       // Pretty print with 4 spaces
       formatted4 = json.prettyPrint(settings, 4);

   **Use Cases:**

   - Human-readable configuration files
   - Debug output
   - Log formatting
   - Documentation generation

Validation
----------

validate
^^^^^^^^

.. function:: validate(jsonString)

   Check if a string contains valid JSON syntax.

   :param jsonString: String to validate
   :type jsonString: string
   :return: true if valid JSON, false otherwise
   :rtype: boolean

   **Examples:**

   .. code-block:: ml

       // Valid JSON
       console.log(json.validate('{"name": "Alice"}'));        // true
       console.log(json.validate('[1, 2, 3]'));                // true
       console.log(json.validate('"hello"'));                  // true
       console.log(json.validate('true'));                     // true

       // Invalid JSON
       console.log(json.validate('{name: "Alice"}'));          // false (missing quotes)
       console.log(json.validate('{"name": "Alice",}'));       // false (trailing comma)
       console.log(json.validate('{incomplete'));              // false (syntax error)

       // Safe parsing pattern
       if (json.validate(userInput)) {
           data = json.parse(userInput);
           // Process data...
       } else {
           console.log("Invalid JSON provided");
       }

   **Use Cases:**

   - Input validation before parsing
   - Error prevention
   - User feedback on malformed JSON
   - Pre-processing data quality checks

Type Checking
-------------

The json module provides comprehensive runtime type checking for JSON values.

isObject
^^^^^^^^

.. function:: isObject(value)

   Check if a value is a JSON object (dictionary).

   :param value: Value to check
   :type value: any
   :return: true if value is an object, false otherwise
   :rtype: boolean

   **Note:** Arrays return false (use ``isArray`` for arrays).

   **Examples:**

   .. code-block:: ml

       console.log(json.isObject({name: "Alice"}));  // true
       console.log(json.isObject([1, 2, 3]));        // false
       console.log(json.isObject("hello"));          // false
       console.log(json.isObject(42));               // false

isArray
^^^^^^^

.. function:: isArray(value)

   Check if a value is a JSON array.

   :param value: Value to check
   :type value: any
   :return: true if value is an array, false otherwise
   :rtype: boolean

   **Examples:**

   .. code-block:: ml

       console.log(json.isArray([1, 2, 3]));         // true
       console.log(json.isArray({name: "Alice"}));   // false
       console.log(json.isArray("hello"));           // false

isString
^^^^^^^^

.. function:: isString(value)

   Check if a value is a string.

   :param value: Value to check
   :type value: any
   :return: true if value is a string, false otherwise
   :rtype: boolean

   **Examples:**

   .. code-block:: ml

       console.log(json.isString("hello"));    // true
       console.log(json.isString(42));         // false
       console.log(json.isString(true));       // false

isNumber
^^^^^^^^

.. function:: isNumber(value)

   Check if a value is a number (integer or float).

   :param value: Value to check
   :type value: any
   :return: true if value is a number, false otherwise
   :rtype: boolean

   **Note:** Booleans return false (use ``isBoolean`` for booleans).

   **Examples:**

   .. code-block:: ml

       console.log(json.isNumber(42));        // true
       console.log(json.isNumber(3.14));      // true
       console.log(json.isNumber(true));      // false
       console.log(json.isNumber("123"));     // false

isBoolean
^^^^^^^^^

.. function:: isBoolean(value)

   Check if a value is a boolean (true or false).

   :param value: Value to check
   :type value: any
   :return: true if value is a boolean, false otherwise
   :rtype: boolean

   **Note:** The numbers 0 and 1 return false.

   **Examples:**

   .. code-block:: ml

       console.log(json.isBoolean(true));     // true
       console.log(json.isBoolean(false));    // true
       console.log(json.isBoolean(1));        // false
       console.log(json.isBoolean(0));        // false

isNull
^^^^^^

.. function:: isNull(value)

   Check if a value is null.

   :param value: Value to check
   :type value: any
   :return: true if value is null, false otherwise
   :rtype: boolean

   **Note:** Other "falsy" values (0, false, "") return false.

   **Examples:**

   .. code-block:: ml

       console.log(json.isNull(null));        // true
       console.log(json.isNull(0));           // false
       console.log(json.isNull(false));       // false
       console.log(json.isNull(""));          // false

Utilities
---------

keys
^^^^

.. function:: keys(obj)

   Get an array of all keys in an object.

   :param obj: Object to extract keys from
   :type obj: object
   :return: Array of key strings
   :rtype: array

   **Examples:**

   .. code-block:: ml

       person = {name: "Alice", age: 30, city: "NYC", email: "alice@example.com"};
       personKeys = json.keys(person);
       // ["name", "age", "city", "email"]

       console.log("Number of properties: " + str(len(personKeys)));

       // Iterate over keys
       i = 0;
       while (i < len(personKeys)) {
           key = personKeys[i];
           console.log("Key: " + key);
           i = i + 1;
       }

   **Use Cases:**

   - Object introspection
   - Dynamic property access
   - Validating required fields
   - Property counting

values
^^^^^^

.. function:: values(obj)

   Get an array of all values in an object.

   :param obj: Object to extract values from
   :type obj: object
   :return: Array of values
   :rtype: array

   **Examples:**

   .. code-block:: ml

       config = {timeout: 30, retries: 3, debug: true, host: "localhost"};
       configValues = json.values(config);
       // [30, 3, true, "localhost"]

       console.log("Values: " + str(configValues));

   **Use Cases:**

   - Extracting all values for processing
   - Value aggregation
   - Bulk value operations
   - Data collection

hasKey
^^^^^^

.. function:: hasKey(obj, key)

   Check if an object has a specific key.

   :param obj: Object to check
   :type obj: object
   :param key: Key name to look for
   :type key: string
   :return: true if key exists, false otherwise
   :rtype: boolean

   **Examples:**

   .. code-block:: ml

       user = {id: 123, name: "Bob", email: "bob@example.com"};

       console.log(json.hasKey(user, "id"));       // true
       console.log(json.hasKey(user, "name"));     // true
       console.log(json.hasKey(user, "phone"));    // false
       console.log(json.hasKey(user, "address"));  // false

       // Conditional property access
       if (json.hasKey(user, "email")) {
           console.log("Email: " + user.email);
       } else {
           console.log("No email provided");
       }

   **Use Cases:**

   - Checking for optional properties
   - Validating object structure
   - Conditional logic based on properties
   - Schema validation

get
^^^

.. function:: get(obj, key, defaultValue)

   Safely get a property value with a default fallback.

   :param obj: Object to access
   :type obj: object
   :param key: Property key to retrieve
   :type key: string
   :param defaultValue: Value to return if key doesn't exist
   :type defaultValue: any
   :return: Property value if exists, otherwise defaultValue
   :rtype: any

   **Examples:**

   .. code-block:: ml

       settings = {theme: "dark", fontSize: 14, lineHeight: 1.5};

       // Existing properties
       theme = json.get(settings, "theme", "light");
       console.log("Theme: " + theme);  // "dark"

       fontSize = json.get(settings, "fontSize", 12);
       console.log("Font size: " + str(fontSize));  // 14

       // Missing properties with defaults
       language = json.get(settings, "language", "en");
       console.log("Language: " + language);  // "en" (default)

       timeout = json.get(settings, "timeout", 30);
       console.log("Timeout: " + str(timeout));  // 30 (default)

   **Use Cases:**

   - Configuration with defaults
   - Safe property access
   - Optional parameters
   - Fallback values

merge
^^^^^

.. function:: merge(obj1, obj2)

   Merge two objects, with obj2 properties overriding obj1.

   :param obj1: Base object
   :type obj1: object
   :param obj2: Override object
   :type obj2: object
   :return: New object with merged properties
   :rtype: object

   **Examples:**

   .. code-block:: ml

       defaults = {color: "blue", size: "medium", quantity: 1};
       userPrefs = {color: "red", quantity: 5};

       merged = json.merge(defaults, userPrefs);
       // {color: "red", size: "medium", quantity: 5}

       console.log("Color: " + merged.color);          // "red" (from userPrefs)
       console.log("Size: " + merged.size);            // "medium" (from defaults)
       console.log("Quantity: " + str(merged.quantity));  // 5 (from userPrefs)

   **Use Cases:**

   - Configuration merging
   - Default value application
   - Options objects
   - Settings inheritance

Practical Examples
==================

Configuration Management
------------------------

Build robust configuration systems with defaults and user overrides:

.. code-block:: ml

    import console;
    import json;

    // Default configuration
    defaultConfig = {
        server: {host: "0.0.0.0", port: 8080, timeout: 30},
        database: {host: "localhost", port: 5432},
        features: {auth: true, cache: false, logging: true}
    };

    // User configuration (partial)
    userConfig = {
        server: {port: 3000, timeout: 60},
        features: {cache: true}
    };

    // Merge configurations
    finalConfig = {
        server: json.merge(defaultConfig.server, userConfig.server),
        database: defaultConfig.database,
        features: json.merge(defaultConfig.features, userConfig.features)
    };

    console.log("Server Port: " + str(finalConfig.server.port));      // 3000
    console.log("Server Host: " + finalConfig.server.host);           // "0.0.0.0"
    console.log("Cache Enabled: " + str(finalConfig.features.cache)); // true

API Response Processing
-----------------------

Parse and validate API responses with type checking:

.. code-block:: ml

    import console;
    import json;

    apiResponseJson = '{
        "status": "success",
        "data": {
            "users": [
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"}
            ],
            "total": 2
        },
        "timestamp": "2024-01-15T10:30:00Z"
    }';

    // Parse and validate response
    response = json.parse(apiResponseJson);

    if (json.isString(response.status)) {
        console.log("Status: " + response.status);
    }

    if (json.isObject(response.data)) {
        if (json.isNumber(response.data.total)) {
            console.log("Total users: " + str(response.data.total));
        }

        if (json.isArray(response.data.users)) {
            console.log("Processing " + str(len(response.data.users)) + " users");

            i = 0;
            while (i < len(response.data.users)) {
                user = response.data.users[i];
                console.log("  User " + str(user.id) + ": " + user.name);
                i = i + 1;
            }
        }
    }

Safe User Input Validation
---------------------------

Validate untrusted JSON with depth limits and type checking:

.. code-block:: ml

    import console;
    import json;

    function validateUserInput(jsonString, maxDepth) {
        console.log("Validating user input");
        console.log("  Max depth: " + str(maxDepth));
        console.log("  Input length: " + str(len(jsonString)) + " chars");

        // Validate syntax first
        if (!json.validate(jsonString)) {
            console.log("  REJECTED: Invalid JSON syntax");
            return null;
        }

        // Parse with depth limit for security
        data = json.safeParse(jsonString, maxDepth);
        console.log("  ACCEPTED: Valid JSON within depth limit");

        return data;
    }

    // Test with valid input
    validInput = '{"name": "Diana", "data": {"score": 95}}';
    result = validateUserInput(validInput, 10);

    if (result != null) {
        if (json.hasKey(result, "name")) {
            console.log("Parsed name: " + result.name);
        }
    }

Schema Validation
-----------------

Implement custom schema validation with type checking:

.. code-block:: ml

    import console;
    import json;

    function validateUser(user) {
        console.log("Validating user: " + str(user));

        errors = [];

        // Must be object
        if (!json.isObject(user)) {
            errors = errors + ["User must be an object"];
            console.log("Errors: " + str(errors));
            return false;
        }

        // Name must be string
        if (!json.isString(user.name)) {
            errors = errors + ["name must be a string"];
        }

        // Age must be number
        if (!json.isNumber(user.age)) {
            errors = errors + ["age must be a number"];
        }

        // Active must be boolean
        if (!json.isBoolean(user.active)) {
            errors = errors + ["active must be a boolean"];
        }

        if (len(errors) > 0) {
            console.log("Validation failed:");
            i = 0;
            while (i < len(errors)) {
                console.log("  - " + errors[i]);
                i = i + 1;
            }
            return false;
        }

        console.log("Validation passed!");
        return true;
    }

    // Test validation
    validUser = {name: "Alice", age: 30, active: true};
    validateUser(validUser);  // Pass

    invalidUser = {name: 123, age: 30, active: true};
    validateUser(invalidUser);  // Fail: name must be string

Feature Flags System
--------------------

Manage feature flags with object merging:

.. code-block:: ml

    import console;
    import json;

    // Default features (all disabled)
    defaultFeatures = {
        newUI: false,
        betaFeatures: false,
        analytics: false,
        notifications: false
    };

    // User-specific overrides
    userFeatures = {newUI: true, analytics: true};

    // Merge to get active features
    activeFeatures = json.merge(defaultFeatures, userFeatures);

    console.log("Active Features:");
    featureKeys = json.keys(activeFeatures);

    i = 0;
    while (i < len(featureKeys)) {
        feature = featureKeys[i];
        enabled = json.get(activeFeatures, feature, false);

        status = "";
        if (enabled) {
            status = "ENABLED";
        } else {
            status = "disabled";
        }

        console.log("  " + feature + ": " + status);
        i = i + 1;
    }

Security Best Practices
=======================

Depth-Limited Parsing
---------------------

Always use ``safeParse`` for untrusted JSON to prevent deeply nested attacks:

.. code-block:: ml

    // DON'T: Parse untrusted JSON without depth limits
    data = json.parse(userSubmittedJson);  // Vulnerable to DoS

    // DO: Use safeParse with appropriate depth limits
    data = json.safeParse(userSubmittedJson, 20);  // Protected

**Recommended Depth Limits:**

- User-generated content: 10-20
- API responses: 20-30
- Configuration files: 15-25
- Internal data: 50-100

Validate Before Parsing
------------------------

Check JSON syntax before attempting to parse:

.. code-block:: ml

    if (json.validate(input)) {
        data = json.safeParse(input, 20);
        // Process data...
    } else {
        console.error("Invalid JSON provided");
    }

Type Checking for Safety
-------------------------

Always verify types after parsing untrusted JSON:

.. code-block:: ml

    data = json.safeParse(userInput, 20);

    if (json.isObject(data)) {
        // Safe to access properties
        if (json.hasKey(data, "email") && json.isString(data.email)) {
            // Process email safely
        }
    }

Error Handling Pattern
----------------------

Implement robust error handling for JSON operations:

.. code-block:: ml

    function safeLoadJson(jsonString, description) {
        console.log("Loading: " + description);

        // Validate first
        if (!json.validate(jsonString)) {
            console.log("ERROR: Invalid JSON format");
            return null;
        }

        // Safe parse with depth limit
        data = json.safeParse(jsonString, 20);
        console.log("SUCCESS: Loaded and validated");

        return data;
    }

Performance Considerations
==========================

Parsing Performance
-------------------

- ``parse`` is faster but has no depth protection
- ``safeParse`` adds minimal overhead (~5-10%) for depth validation
- Use ``safeParse`` for untrusted data, ``parse`` for trusted sources

Serialization Performance
-------------------------

- ``stringify`` produces compact JSON (minimal overhead)
- ``prettyPrint`` adds formatting overhead (~20-30% slower)
- Use ``stringify`` for production, ``prettyPrint`` for debugging

Type Checking Overhead
----------------------

- Type checks are fast (constant time operations)
- Batch type checks when possible
- Cache results if checking same value multiple times

Common Patterns
===============

Round-Trip Conversion
---------------------

Convert ML objects to JSON and back:

.. code-block:: ml

    original = {id: 123, title: "Test", tags: ["test", "example"]};

    // Convert to JSON
    jsonString = json.stringify(original);

    // Parse back to object
    restored = json.parse(jsonString);

    // Values match
    console.log(restored.title == original.title);  // true

Object Inspection
-----------------

Dynamically inspect object properties:

.. code-block:: ml

    document = {title: "Doc", content: "...", author: "System"};

    docKeys = json.keys(document);
    console.log("Properties: " + str(len(docKeys)));

    i = 0;
    while (i < len(docKeys)) {
        key = docKeys[i];
        if (json.hasKey(document, key)) {
            value = json.get(document, key, null);
            console.log("  " + key + ": " + str(value));
        }
        i = i + 1;
    }

Batch Processing
----------------

Process multiple JSON strings safely:

.. code-block:: ml

    jsonBatch = [
        '{"id": 1, "status": "active"}',
        '{"id": 2, "status": "pending"}',
        '{"id": 3, "status": "active"}'
    ];

    processed = 0;
    i = 0;
    while (i < len(jsonBatch)) {
        jsonStr = jsonBatch[i];

        if (json.validate(jsonStr)) {
            data = json.safeParse(jsonStr, 10);
            console.log("Item " + str(data.id) + ": " + data.status);
            processed = processed + 1;
        } else {
            console.log("Item " + str(i + 1) + ": INVALID");
        }

        i = i + 1;
    }

    console.log("Processed: " + str(processed) + "/" + str(len(jsonBatch)));

See Also
========

- :doc:`builtin` - Core built-in functions including ``str()`` and ``len()``
- :doc:`console` - Logging and output functions
- :doc:`file` - File I/O operations for JSON files

.. note::

   The json module enforces security through depth-limited parsing with ``safeParse``. Always use ``safeParse`` for untrusted JSON data to prevent deeply nested JSON attacks that could cause stack overflow or denial of service.
