Environment Variables (env)
===========================

.. module:: env
   :synopsis: Access and manage environment variables

The ``env`` module provides functions for reading and writing environment variables,
essential for configuration management and secret handling in ML applications.

Required Capabilities
--------------------

- ``env.read`` - Read environment variables (may expose secrets)
- ``env.write`` - Modify environment variables (affects process state)

.. warning::
   Environment variables may contain sensitive information such as API keys,
   passwords, and database credentials. Always handle them with care and avoid
   logging them directly.

Quick Start
-----------

.. code-block:: ml

   import env;

   // Read environment variable with default
   api_key = env.get("API_KEY", "default-key");

   // Get required variable (throws if missing)
   db_url = env.require("DATABASE_URL");

   // Type conversion
   port = env.get_int("PORT", 8080);
   debug = env.get_bool("DEBUG", false);
   timeout = env.get_float("TIMEOUT", 30.0);

API Reference
-------------

Reading Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

get(key, default)
^^^^^^^^^^^^^^^^^

Get environment variable with optional default value.

**Parameters:**

- ``key`` (string) - Environment variable name
- ``default`` (string, optional) - Default value if not set (defaults to null)

**Returns:** string or null

**Capabilities Required:** ``env.read``

**Example:**

.. code-block:: ml

   // With default value
   api_url = env.get("API_URL", "https://api.example.com");

   // Without default (returns null if not set)
   optional_var = env.get("OPTIONAL_VAR");

require(key)
^^^^^^^^^^^^

Get required environment variable or throw error if missing.

**Parameters:**

- ``key`` (string) - Environment variable name

**Returns:** string

**Throws:** RuntimeError if variable not set

**Capabilities Required:** ``env.read``

**Example:**

.. code-block:: ml

   // This will throw if DATABASE_URL is not set
   db_url = env.require("DATABASE_URL");

has(key)
^^^^^^^^

Check if environment variable is set.

**Parameters:**

- ``key`` (string) - Environment variable name

**Returns:** boolean - True if variable exists, False otherwise

**Capabilities Required:** ``env.read``

**Example:**

.. code-block:: ml

   if (env.has("API_KEY")) {
       api_key = env.get("API_KEY");
       // Use API key
   } else {
       console.log("API_KEY not configured");
   }

all()
^^^^^

Get all environment variables as dictionary.

**Returns:** object - Dictionary of all environment variables

**Capabilities Required:** ``env.read``

**Security Warning:** This exposes all environment variables, including potentially
sensitive ones. Use with extreme caution.

**Example:**

.. code-block:: ml

   all_vars = env.all();
   console.log("Total variables: " + str(len(all_vars)));

Type Conversion Functions
~~~~~~~~~~~~~~~~~~~~~~~~~

get_int(key, default)
^^^^^^^^^^^^^^^^^^^^^

Get environment variable as integer with type conversion.

**Parameters:**

- ``key`` (string) - Environment variable name
- ``default`` (integer, optional) - Default value if not set or invalid (defaults to 0)

**Returns:** integer

**Capabilities Required:** ``env.read``

**Example:**

.. code-block:: ml

   port = env.get_int("PORT", 8080);
   max_retries = env.get_int("MAX_RETRIES", 3);

   // Invalid values return default
   env.set("INVALID", "not_a_number");
   value = env.get_int("INVALID", 42);  // Returns 42

get_bool(key, default)
^^^^^^^^^^^^^^^^^^^^^^

Get environment variable as boolean with type conversion.

Treats ``"true"``, ``"1"``, ``"yes"``, ``"on"`` as True (case-insensitive).
All other values are treated as False.

**Parameters:**

- ``key`` (string) - Environment variable name
- ``default`` (boolean, optional) - Default value if not set (defaults to false)

**Returns:** boolean

**Capabilities Required:** ``env.read``

**Example:**

.. code-block:: ml

   debug = env.get_bool("DEBUG", false);
   cache_enabled = env.get_bool("CACHE_ENABLED", true);

   // Various true values
   env.set("FLAG1", "true");   // → true
   env.set("FLAG2", "1");      // → true
   env.set("FLAG3", "yes");    // → true
   env.set("FLAG4", "on");     // → true
   env.set("FLAG5", "false");  // → false
   env.set("FLAG6", "0");      // → false

get_float(key, default)
^^^^^^^^^^^^^^^^^^^^^^^

Get environment variable as floating-point number with type conversion.

**Parameters:**

- ``key`` (string) - Environment variable name
- ``default`` (float, optional) - Default value if not set or invalid (defaults to 0.0)

**Returns:** float

**Capabilities Required:** ``env.read``

**Example:**

.. code-block:: ml

   timeout = env.get_float("TIMEOUT", 30.0);
   rate_limit = env.get_float("RATE_LIMIT", 100.0);

   // Supports scientific notation
   env.set("SMALL", "1.5e-3");
   value = env.get_float("SMALL");  // Returns 0.0015

Writing Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

set(key, value)
^^^^^^^^^^^^^^^

Set environment variable.

**Parameters:**

- ``key`` (string) - Variable name
- ``value`` (string) - Variable value (automatically converted to string)

**Returns:** None

**Capabilities Required:** ``env.write``

**Example:**

.. code-block:: ml

   env.set("DEBUG", "true");
   env.set("MAX_CONNECTIONS", "100");

   // Values are automatically converted to strings
   env.set("PORT", 8080);  // Stored as "8080"

delete(key)
^^^^^^^^^^^

Delete environment variable if it exists.

**Parameters:**

- ``key`` (string) - Variable name

**Returns:** None

**Capabilities Required:** ``env.write``

**Example:**

.. code-block:: ml

   env.delete("TEMP_VAR");

   // Safe to delete non-existent variables
   env.delete("DOES_NOT_EXIST");  // No error

Common Patterns
---------------

Configuration Management
~~~~~~~~~~~~~~~~~~~~~~~~

Load application configuration from environment variables:

.. code-block:: ml

   import env;

   config = {
       api_url: env.require("API_URL"),
       api_key: env.require("API_KEY"),
       timeout: env.get_int("TIMEOUT", 30),
       debug: env.get_bool("DEBUG", false),
       max_retries: env.get_int("MAX_RETRIES", 3)
   };

   console.log("Configuration loaded");
   console.log("API URL: " + config.api_url);
   console.log("Debug mode: " + str(config.debug));

Feature Flags
~~~~~~~~~~~~~

Use environment variables for feature toggles:

.. code-block:: ml

   import env;

   enable_cache = env.get_bool("ENABLE_CACHE", true);
   enable_analytics = env.get_bool("ENABLE_ANALYTICS", false);

   if (enable_cache) {
       // Initialize cache
       console.log("Cache enabled");
   }

   if (enable_analytics) {
       // Setup analytics
       console.log("Analytics enabled");
   }

Environment-Specific Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Different settings for development, staging, and production:

.. code-block:: ml

   import env;

   environment = env.get("ENV", "development");

   if (environment == "production") {
       log_level = "INFO";
       debug_mode = false;
       api_url = env.require("PROD_API_URL");
   } elif (environment == "staging") {
       log_level = "DEBUG";
       debug_mode = true;
       api_url = env.require("STAGING_API_URL");
   } else {
       log_level = "DEBUG";
       debug_mode = true;
       api_url = "http://localhost:3000";
   }

Database Connection Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configure database connections using environment variables:

.. code-block:: ml

   import env;

   db_config = {
       host: env.get("DB_HOST", "localhost"),
       port: env.get_int("DB_PORT", 5432),
       database: env.require("DB_NAME"),
       user: env.require("DB_USER"),
       password: env.require("DB_PASSWORD"),
       ssl: env.get_bool("DB_SSL", true),
       max_connections: env.get_int("DB_MAX_CONNECTIONS", 10),
       timeout: env.get_float("DB_TIMEOUT", 30.0)
   };

Security Considerations
-----------------------

Never Log Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Environment variables often contain secrets. Avoid logging them:

.. code-block:: ml

   import env;
   import log;

   // ❌ BAD - Logs all env vars including secrets
   log.info("Environment", env.all());

   // ✅ GOOD - Log only specific non-sensitive values
   log.info("Configuration", {
       api_url: env.get("API_URL"),
       debug: env.get_bool("DEBUG")
   });

Use .env Files for Development
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For local development, use ``.env`` files to manage environment variables.
**Never commit .env files to version control!**

Example ``.env`` file:

.. code-block:: bash

   # .env - Local development configuration
   API_URL=http://localhost:3000
   API_KEY=dev_key_12345
   DEBUG=true
   PORT=8080

Add to ``.gitignore``:

.. code-block:: text

   .env
   .env.local
   .env.*.local

Production Secret Management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In production, use secure secret management systems:

- **AWS Secrets Manager** - For AWS deployments
- **HashiCorp Vault** - For multi-cloud or on-premise
- **Azure Key Vault** - For Azure deployments
- **Google Secret Manager** - For GCP deployments

Required vs Optional Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ``require()`` for critical configuration and ``get()`` with defaults for optional settings:

.. code-block:: ml

   import env;

   // Critical - must be set
   api_key = env.require("API_KEY");
   db_url = env.require("DATABASE_URL");

   // Optional - has sensible defaults
   timeout = env.get_int("TIMEOUT", 30);
   debug = env.get_bool("DEBUG", false);

Validate Configuration Early
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Validate all required environment variables at application startup:

.. code-block:: ml

   import env;
   import console;

   function validate_config() {
       required_vars = ["API_KEY", "DATABASE_URL", "SECRET_KEY"];
       missing = [];

       for (var_name in required_vars) {
           if (!env.has(var_name)) {
               missing.append(var_name);
           }
       }

       if (len(missing) > 0) {
           console.error("Missing required environment variables:");
           for (var_name in missing) {
               console.error("  - " + var_name);
           }
           throw "Configuration error: missing required variables";
       }

       console.log("Configuration validation passed");
   }

   validate_config();

Integration with Other Modules
-------------------------------

With Logging
~~~~~~~~~~~~

Configure logging based on environment:

.. code-block:: ml

   import env;
   import log;

   // Configure log level from environment
   log_level = env.get("LOG_LEVEL", "INFO");
   log.set_level(log_level);

   // Configure log format
   if (env.get("ENV") == "production") {
       log.set_format("json");
       log.add_file("app.log");
   } else {
       log.set_format("text");
   }

With HTTP Client
~~~~~~~~~~~~~~~~

Configure HTTP client from environment:

.. code-block:: ml

   import env;
   import http;

   api_url = env.require("API_URL");
   api_key = env.require("API_KEY");

   headers = {
       "Authorization": "Bearer " + api_key,
       "Content-Type": "application/json"
   };

   response = http.get(api_url + "/users", headers);

With File Operations
~~~~~~~~~~~~~~~~~~~~

Configure file paths from environment:

.. code-block:: ml

   import env;
   import file;

   data_dir = env.get("DATA_DIR", "./data");
   log_dir = env.get("LOG_DIR", "./logs");

   // Ensure directories exist
   if (!path.exists(data_dir)) {
       path.mkdir(data_dir);
   }

   // Read from configured location
   config_file = data_dir + "/config.json";
   if (file.exists(config_file)) {
       config = json.parse(file.read(config_file));
   }

Error Handling
--------------

Handle Missing Required Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import env;
   import console;

   try {
       api_key = env.require("API_KEY");
       // Use API key
   } except (error) {
       console.error("Error: API_KEY environment variable not set");
       console.error("Please set API_KEY before running this application");
       // Handle error gracefully
   }

Handle Invalid Type Conversions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Type conversion functions return defaults for invalid values:

.. code-block:: ml

   import env;

   env.set("INVALID_INT", "not_a_number");

   // Returns default value for invalid input
   port = env.get_int("INVALID_INT", 8080);
   console.log("Port: " + str(port));  // Prints: Port: 8080

Performance Considerations
--------------------------

Caching Configuration
~~~~~~~~~~~~~~~~~~~~~

For frequently accessed configuration, cache values at startup:

.. code-block:: ml

   import env;

   // Cache configuration at startup
   CONFIG = {
       api_url: env.require("API_URL"),
       api_key: env.require("API_KEY"),
       timeout: env.get_int("TIMEOUT", 30),
       debug: env.get_bool("DEBUG", false)
   };

   // Use cached values throughout application
   function make_api_call() {
       response = http.get(CONFIG.api_url, {
           "Authorization": "Bearer " + CONFIG.api_key
       });
       return response;
   }

Environment Variable Overhead
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Reading environment variables is fast (< 1 microsecond), but for high-frequency
access in tight loops, consider caching the value:

.. code-block:: ml

   import env;

   // ❌ INEFFICIENT - Reads env var on every iteration
   for (i = 0; i < 10000; i = i + 1) {
       debug = env.get_bool("DEBUG");
       if (debug) {
           // Debug code
       }
   }

   // ✅ EFFICIENT - Read once, use many times
   debug = env.get_bool("DEBUG");
   for (i = 0; i < 10000; i = i + 1) {
       if (debug) {
           // Debug code
       }
   }

See Also
--------

- :doc:`log` - Logging module (configure from environment)
- :doc:`crypto` - Cryptography module (for hashing secrets)
- :doc:`file` - File operations (for .env file handling)
- :doc:`json` - JSON parsing (for complex configuration)

Examples
--------

Complete Application Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import env;
   import log;
   import console;

   // Validate and load configuration
   function load_config() {
       // Validate required variables
       required = ["API_URL", "API_KEY", "DB_URL"];
       for (var_name in required) {
           if (!env.has(var_name)) {
               console.error("Missing required variable: " + var_name);
               throw "Configuration error";
           }
       }

       // Build configuration object
       config = {
           // API Configuration
           api_url: env.require("API_URL"),
           api_key: env.require("API_KEY"),
           api_timeout: env.get_float("API_TIMEOUT", 30.0),

           // Database Configuration
           db_url: env.require("DB_URL"),
           db_pool_size: env.get_int("DB_POOL_SIZE", 10),
           db_timeout: env.get_float("DB_TIMEOUT", 30.0),

           // Application Configuration
           environment: env.get("ENV", "development"),
           debug: env.get_bool("DEBUG", false),
           port: env.get_int("PORT", 8080),
           host: env.get("HOST", "0.0.0.0"),

           // Feature Flags
           enable_cache: env.get_bool("ENABLE_CACHE", true),
           enable_metrics: env.get_bool("ENABLE_METRICS", false),

           // Logging Configuration
           log_level: env.get("LOG_LEVEL", "INFO"),
           log_format: env.get("LOG_FORMAT", "text")
       };

       // Configure logging based on config
       log.set_level(config.log_level);
       log.set_format(config.log_format);

       console.log("Configuration loaded successfully");
       console.log("Environment: " + config.environment);
       console.log("Debug mode: " + str(config.debug));

       return config;
   }

   // Load configuration at startup
   CONFIG = load_config();
