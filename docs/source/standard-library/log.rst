log - Structured Logging
=========================

The ``log`` module provides structured logging capabilities with multiple log levels,
formatting options, and support for both console and file output. It enables developers
to add comprehensive logging to ML applications with minimal configuration.

.. contents:: Table of Contents
   :local:
   :depth: 2

--------

Module Overview
---------------

**Module Name:** ``log``

**Import Statement:**

.. code-block:: ml

    import log;

**Capabilities Required:**

- ``log.write`` - Writing log messages to console
- ``file.write`` - Writing log messages to files (when using ``add_file()``)

**Key Features:**

- Multiple log levels (DEBUG, INFO, WARN, ERROR, CRITICAL)
- Structured logging with data dictionaries
- JSON and text output formats
- Named loggers for different components
- File and console output
- Configurable timestamps
- Level-based filtering

--------

Quick Start
-----------

Basic Logging
~~~~~~~~~~~~~

.. code-block:: ml

    import log;

    // Simple logging
    log.info("Application started");
    log.warn("Low memory detected");
    log.error("Connection failed");

Structured Data
~~~~~~~~~~~~~~~

.. code-block:: ml

    import log;

    // Log with context data
    log.info("User logged in", {
        user_id: 123,
        ip: "192.168.1.1",
        session_id: "abc123"
    });

Named Loggers
~~~~~~~~~~~~~

.. code-block:: ml

    import log;

    // Create component-specific loggers
    db_logger = log.create_logger("database");
    api_logger = log.create_logger("api");

    db_logger.info("Query executed", {duration: 0.025});
    api_logger.error("Request failed", {status: 500});

--------

API Reference
-------------

Logging Functions
~~~~~~~~~~~~~~~~~

log.debug(message, data?)
^^^^^^^^^^^^^^^^^^^^^^^^^

Log debug level message for detailed diagnostic information.

**Parameters:**

- ``message`` (string) - Log message
- ``data`` (object, optional) - Structured data dictionary

**Returns:** None

**Example:**

.. code-block:: ml

    log.debug("Processing item", {item_id: 42, index: 10});

**Note:** Debug messages only appear when log level is set to DEBUG.

--------

log.info(message, data?)
^^^^^^^^^^^^^^^^^^^^^^^^

Log info level message for general informational events.

**Parameters:**

- ``message`` (string) - Log message
- ``data`` (object, optional) - Structured data dictionary

**Returns:** None

**Example:**

.. code-block:: ml

    log.info("Server started", {port: 8080, workers: 4});

--------

log.warn(message, data?)
^^^^^^^^^^^^^^^^^^^^^^^^

Log warning level message for potentially harmful situations.

**Parameters:**

- ``message`` (string) - Log message
- ``data`` (object, optional) - Structured data dictionary

**Returns:** None

**Example:**

.. code-block:: ml

    log.warn("Cache miss", {key: "user_123", cache_size: 1000});

--------

log.error(message, data?)
^^^^^^^^^^^^^^^^^^^^^^^^^

Log error level message for error events.

**Parameters:**

- ``message`` (string) - Log message
- ``data`` (object, optional) - Structured data dictionary

**Returns:** None

**Example:**

.. code-block:: ml

    log.error("Database connection failed", {
        host: "localhost",
        error: "Connection refused"
    });

--------

log.critical(message, data?)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Log critical level message for severe error events that may cause application failure.

**Parameters:**

- ``message`` (string) - Log message
- ``data`` (object, optional) - Structured data dictionary

**Returns:** None

**Example:**

.. code-block:: ml

    log.critical("Out of memory", {available_mb: 10, required_mb: 500});

--------

Configuration Functions
~~~~~~~~~~~~~~~~~~~~~~~

log.set_level(level)
^^^^^^^^^^^^^^^^^^^^

Set the logging level to filter messages by severity.

**Parameters:**

- ``level`` (string) - Log level: "DEBUG", "INFO", "WARN", "ERROR", or "CRITICAL"

**Returns:** None

**Example:**

.. code-block:: ml

    // Set to DEBUG to see all messages
    log.set_level("DEBUG");

    // Set to ERROR to only see errors and critical messages
    log.set_level("ERROR");

**Log Level Hierarchy:**

- ``DEBUG`` - Most verbose, includes all messages
- ``INFO`` - Informational messages and above
- ``WARN`` - Warnings and above
- ``ERROR`` - Errors and critical messages only
- ``CRITICAL`` - Only critical messages

--------

log.set_format(format_type)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Set the output format for log messages.

**Parameters:**

- ``format_type`` (string) - Format type: "text" or "json"

**Returns:** None

**Example:**

.. code-block:: ml

    // Text format (default)
    log.set_format("text");
    log.info("User action", {user_id: 123});
    // Output: [2025-11-10 14:30:22] INFO: User action | user_id=123

    // JSON format
    log.set_format("json");
    log.info("User action", {user_id: 123});
    // Output: {"message":"User action","level":"INFO","logger":"default","timestamp":"2025-11-10T14:30:22Z","data":{"user_id":123}}

--------

log.add_file(file_path)
^^^^^^^^^^^^^^^^^^^^^^^

Add a file output destination for log messages.

**Parameters:**

- ``file_path`` (string) - Path to log file (will be created if doesn't exist)

**Returns:** None

**Capabilities Required:** ``log.write``, ``file.write``

**Example:**

.. code-block:: ml

    import log;

    // Log to both console and file
    log.add_file("app.log");
    log.info("Application started");  // Appears in console AND app.log

**Note:** Log messages will be appended to the file. The file is created if it doesn't exist.

--------

log.set_timestamp(enabled)
^^^^^^^^^^^^^^^^^^^^^^^^^^

Enable or disable timestamps in log output.

**Parameters:**

- ``enabled`` (boolean) - True to include timestamps, False to omit

**Returns:** None

**Example:**

.. code-block:: ml

    // Disable timestamps
    log.set_timestamp(false);
    log.info("Message");  // Output: INFO: Message

    // Enable timestamps (default)
    log.set_timestamp(true);
    log.info("Message");  // Output: [2025-11-10 14:30:22] INFO: Message

--------

Utility Functions
~~~~~~~~~~~~~~~~~

log.is_debug()
^^^^^^^^^^^^^^

Check if debug logging is currently enabled.

**Returns:** boolean - True if debug level is active

**Example:**

.. code-block:: ml

    import log;

    if (log.is_debug()) {
        // Expensive debug computation
        debug_data = compute_detailed_stats();
        log.debug("Debug stats", debug_data);
    }

**Use Case:** Avoid expensive debug data computation when debug logging is disabled.

--------

log.create_logger(name)
^^^^^^^^^^^^^^^^^^^^^^^

Create a named logger instance for component-specific logging.

**Parameters:**

- ``name`` (string) - Logger name for identification

**Returns:** Logger - New logger instance

**Example:**

.. code-block:: ml

    import log;

    // Create component loggers
    db_logger = log.create_logger("database");
    api_logger = log.create_logger("api");
    auth_logger = log.create_logger("auth");

    // Each logger can be configured independently
    db_logger.set_level("DEBUG");
    api_logger.set_level("INFO");
    auth_logger.set_format("json");

    // Use loggers
    db_logger.debug("Query: SELECT * FROM users");
    api_logger.info("GET /api/users - 200 OK");
    auth_logger.error("Login failed", {username: "user123"});

--------

Logger Instance Methods
~~~~~~~~~~~~~~~~~~~~~~~

Named Logger objects created with ``log.create_logger()`` support all the same methods:

- ``logger.debug(message, data?)``
- ``logger.info(message, data?)``
- ``logger.warn(message, data?)``
- ``logger.error(message, data?)``
- ``logger.critical(message, data?)``
- ``logger.set_level(level)``
- ``logger.set_format(format_type)``
- ``logger.add_file(file_path)``
- ``logger.set_timestamp(enabled)``
- ``logger.is_debug()``

Each logger instance maintains independent configuration.

--------

Common Patterns
---------------

Application Logging
~~~~~~~~~~~~~~~~~~~

Set up structured logging for different application components:

.. code-block:: ml

    import log;
    import env;

    // Configure based on environment
    environment = env.get("ENV", "development");

    if (environment == "production") {
        log.set_level("INFO");
        log.set_format("json");
        log.add_file("app.log");
    } else {
        log.set_level("DEBUG");
        log.set_format("text");
    }

    log.info("Application started", {
        environment: environment,
        version: "1.0.0"
    });

Request/Response Logging
~~~~~~~~~~~~~~~~~~~~~~~~

Log HTTP requests with full context:

.. code-block:: ml

    import log;

    request_logger = log.create_logger("http");

    function handle_request(request) {
        request_id = generate_id();

        request_logger.info("Request received", {
            request_id: request_id,
            method: request.method,
            path: request.path,
            ip: request.ip
        });

        try {
            result = process_request(request);

            request_logger.info("Request completed", {
                request_id: request_id,
                status: 200,
                duration_ms: result.duration
            });

            return result;
        } except (error) {
            request_logger.error("Request failed", {
                request_id: request_id,
                error: error.message,
                status: 500
            });
            throw error;
        }
    }

Error Tracking
~~~~~~~~~~~~~~

Comprehensive error logging with context:

.. code-block:: ml

    import log;

    error_logger = log.create_logger("errors");
    error_logger.set_format("json");
    error_logger.add_file("errors.log");

    function process_data(data) {
        try {
            validate(data);
            result = transform(data);
            save(result);
            return true;
        } except (error) {
            error_logger.error("Data processing failed", {
                error_type: typeof(error),
                error_message: error.message,
                data_id: data.id,
                data_size: len(data),
                timestamp: datetime.now().format("%Y-%m-%d %H:%M:%S")
            });
            return false;
        }
    }

Performance Monitoring
~~~~~~~~~~~~~~~~~~~~~~

Track application performance metrics:

.. code-block:: ml

    import log;

    perf_logger = log.create_logger("performance");
    perf_logger.set_format("json");
    perf_logger.add_file("performance.log");

    function monitor_operation(operation_name, operation_fn) {
        start_time = datetime.now();

        try {
            result = operation_fn();
            duration = datetime.now() - start_time;

            perf_logger.info("Operation completed", {
                operation: operation_name,
                duration_ms: duration,
                status: "success"
            });

            return result;
        } except (error) {
            duration = datetime.now() - start_time;

            perf_logger.warn("Operation failed", {
                operation: operation_name,
                duration_ms: duration,
                status: "error",
                error: error.message
            });

            throw error;
        }
    }

Multi-Component Logging
~~~~~~~~~~~~~~~~~~~~~~~

Separate logs for different system components:

.. code-block:: ml

    import log;

    // Create component-specific loggers
    db_logger = log.create_logger("database");
    cache_logger = log.create_logger("cache");
    queue_logger = log.create_logger("queue");

    // Configure each independently
    db_logger.set_level("DEBUG");
    db_logger.add_file("database.log");

    cache_logger.set_level("INFO");
    cache_logger.add_file("cache.log");

    queue_logger.set_level("WARN");
    queue_logger.add_file("queue.log");

    // Use throughout application
    db_logger.debug("Query executed", {query: "SELECT...", duration: 0.023});
    cache_logger.info("Cache hit", {key: "user_123", ttl: 300});
    queue_logger.warn("Queue full", {size: 1000, max: 1000});

Conditional Debug Logging
~~~~~~~~~~~~~~~~~~~~~~~~~~

Avoid expensive operations when debug is disabled:

.. code-block:: ml

    import log;

    log.set_level("INFO");  // Debug disabled

    function process_batch(items) {
        // Check before expensive operation
        if (log.is_debug()) {
            debug_info = {
                item_count: len(items),
                item_types: collect_types(items),  // Expensive!
                memory_usage: calculate_memory(),   // Expensive!
                timing_stats: get_timing_data()     // Expensive!
            };
            log.debug("Batch processing details", debug_info);
        }

        // Process items...
        log.info("Batch processed", {count: len(items)});
    }

--------

Integration Examples
--------------------

Integration with Error Handling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Combine logging with comprehensive error handling:

.. code-block:: ml

    import log;
    import env;

    app_logger = log.create_logger("application");
    app_logger.set_level(env.get("LOG_LEVEL", "INFO"));

    function safe_operation(operation) {
        try {
            app_logger.debug("Starting operation", {name: operation.name});
            result = operation.execute();
            app_logger.info("Operation successful", {name: operation.name});
            return result;
        } except (validation_error) {
            app_logger.warn("Validation failed", {
                operation: operation.name,
                error: validation_error.message
            });
            return null;
        } except (error) {
            app_logger.error("Operation failed", {
                operation: operation.name,
                error_type: typeof(error),
                error_message: error.message,
                stack_trace: error.stack
            });
            throw error;
        }
    }

Integration with CSV Processing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Log data processing operations:

.. code-block:: ml

    import log;
    import csv;
    import file;

    data_logger = log.create_logger("data_processing");

    function process_csv_file(input_file, output_file) {
        data_logger.info("Starting CSV processing", {
            input: input_file,
            output: output_file
        });

        if (!file.exists(input_file)) {
            data_logger.error("Input file not found", {file: input_file});
            return false;
        }

        rows = csv.read(input_file);
        data_logger.debug("CSV loaded", {row_count: len(rows)});

        processed = [];
        error_count = 0;

        for (row in rows) {
            try {
                validated = validate_row(row);
                processed.append(validated);
            } except (error) {
                error_count = error_count + 1;
                data_logger.warn("Row validation failed", {
                    row_index: len(processed),
                    error: error.message
                });
            }
        }

        csv.write(output_file, processed);

        data_logger.info("CSV processing complete", {
            input_rows: len(rows),
            output_rows: len(processed),
            error_count: error_count,
            success_rate: (len(processed) / len(rows)) * 100
        });

        return true;
    }

Integration with Environment Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configure logging from environment variables:

.. code-block:: ml

    import log;
    import env;

    // Read configuration from environment
    log_level = env.get("LOG_LEVEL", "INFO");
    log_format = env.get("LOG_FORMAT", "text");
    log_file = env.get("LOG_FILE", "");
    enable_timestamps = env.get_bool("LOG_TIMESTAMPS", true);

    // Apply configuration
    log.set_level(log_level);
    log.set_format(log_format);
    log.set_timestamp(enable_timestamps);

    if (log_file != "") {
        log.add_file(log_file);
    }

    log.info("Logging configured", {
        level: log_level,
        format: log_format,
        file: log_file,
        timestamps: enable_timestamps
    });

--------

Best Practices
--------------

Log Levels
~~~~~~~~~~

**Use appropriate log levels:**

- **DEBUG**: Detailed diagnostic information for development
- **INFO**: General informational messages about application flow
- **WARN**: Warning messages for potentially harmful situations
- **ERROR**: Error events that might still allow the application to continue
- **CRITICAL**: Severe errors causing application failure

.. code-block:: ml

    // Good: Appropriate level usage
    log.debug("Cache lookup", {key: "user_123"});          // Development detail
    log.info("User logged in", {user_id: 123});            // Normal event
    log.warn("Retry attempt 3/3", {operation: "api_call"});// Potential issue
    log.error("Database query failed", {query: "SELECT"}); // Error occurred
    log.critical("Out of memory", {available_mb: 5});      // System failure

Structured Data
~~~~~~~~~~~~~~~

**Always use structured data for context:**

.. code-block:: ml

    // Bad: String concatenation
    log.info("User " + user_id + " logged in from " + ip);

    // Good: Structured data
    log.info("User logged in", {
        user_id: user_id,
        ip: ip,
        timestamp: datetime.now()
    });

**Benefits:**

- Easier to search and filter logs
- Consistent format for log aggregation tools
- Better for JSON export and analysis

Component Loggers
~~~~~~~~~~~~~~~~~

**Create separate loggers for different components:**

.. code-block:: ml

    // Create component-specific loggers
    auth_logger = log.create_logger("auth");
    db_logger = log.create_logger("database");
    api_logger = log.create_logger("api");

**Benefits:**

- Independent configuration per component
- Easier filtering and searching
- Better organization for large applications

Performance Considerations
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Use conditional logging for expensive operations:**

.. code-block:: ml

    // Check debug status before expensive work
    if (log.is_debug()) {
        expensive_data = compute_detailed_stats();
        log.debug("Detailed stats", expensive_data);
    }

Security Considerations
~~~~~~~~~~~~~~~~~~~~~~~

**Never log sensitive information:**

.. code-block:: ml

    // Bad: Logging sensitive data
    log.info("User login", {
        username: username,
        password: password  // NEVER log passwords!
    });

    // Good: Log only safe data
    log.info("User login", {
        username: username,
        ip: request_ip,
        timestamp: datetime.now()
    });

**Sensitive data to avoid:**

- Passwords, API keys, tokens
- Personal identifying information (PII)
- Credit card numbers
- Social security numbers
- Private encryption keys

Production Configuration
~~~~~~~~~~~~~~~~~~~~~~~~

**Recommended production settings:**

.. code-block:: ml

    import log;

    // Production configuration
    log.set_level("INFO");          // Don't log debug in production
    log.set_format("json");         // JSON for log aggregation
    log.add_file("app.log");        // Persistent logs
    log.set_timestamp(true);        // Always include timestamps

    // Create specialized error log
    error_logger = log.create_logger("errors");
    error_logger.set_level("ERROR");
    error_logger.set_format("json");
    error_logger.add_file("errors.log");

--------

Error Handling
--------------

File Writing Errors
~~~~~~~~~~~~~~~~~~~

When using ``add_file()``, handle potential file system errors:

.. code-block:: ml

    import log;
    import file;

    try {
        // Ensure directory exists
        log.add_file("logs/app.log");
        log.info("File logging enabled");
    } except (error) {
        // Fallback to console-only logging
        console.error("Could not create log file: " + error.message);
        log.info("Using console logging only");
    }

Invalid Configuration
~~~~~~~~~~~~~~~~~~~~~

Handle invalid log level or format:

.. code-block:: ml

    import log;
    import env;

    log_level = env.get("LOG_LEVEL", "INFO");
    valid_levels = ["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"];

    if (array.includes(valid_levels, log_level)) {
        log.set_level(log_level);
    } else {
        log.warn("Invalid log level, using INFO", {
            requested: log_level,
            valid: valid_levels
        });
        log.set_level("INFO");
    }

--------

Complete Example
----------------

Production-Ready Logging Setup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

    import log;
    import env;
    import datetime;

    // Configure logging based on environment
    function setup_logging() {
        environment = env.get("ENV", "development");

        if (environment == "production") {
            // Production: INFO level, JSON format, file output
            log.set_level("INFO");
            log.set_format("json");
            log.add_file("logs/app.log");
            log.set_timestamp(true);
        } elif (environment == "staging") {
            // Staging: DEBUG level, JSON format, file output
            log.set_level("DEBUG");
            log.set_format("json");
            log.add_file("logs/staging.log");
        } else {
            // Development: DEBUG level, text format, console only
            log.set_level("DEBUG");
            log.set_format("text");
        }

        log.info("Logging configured", {
            environment: environment,
            level: env.get("LOG_LEVEL", "INFO"),
            format: log.set_format
        });
    }

    // Application entry point
    function main() {
        setup_logging();

        // Create component loggers
        app_logger = log.create_logger("app");
        db_logger = log.create_logger("database");
        api_logger = log.create_logger("api");

        app_logger.info("Application starting", {
            version: "1.0.0",
            start_time: datetime.now().format("%Y-%m-%d %H:%M:%S")
        });

        // Application code...
        try {
            db_logger.info("Connecting to database");
            connect_database();

            api_logger.info("Starting API server", {port: 8080});
            start_server();

            app_logger.info("Application running");
        } except (error) {
            app_logger.critical("Application failed to start", {
                error: error.message,
                error_type: typeof(error)
            });
            throw error;
        }
    }

    main();

--------

See Also
--------

- :doc:`console` - Basic console output
- :doc:`env` - Environment variable configuration
- :doc:`file` - File system operations
- :doc:`datetime` - Timestamp formatting
