===============
console Module
===============

The console module provides logging and output functionality for ML programs. It offers different logging levels and outputs to stdout and stderr appropriately.

.. contents::
   :local:
   :depth: 2

Overview
========

The console module is automatically available after import and provides five logging methods:

* ``log()`` - General output to stdout
* ``info()`` - Informational messages to stdout
* ``debug()`` - Debug messages to stdout
* ``warn()`` - Warning messages to stderr
* ``error()`` - Error messages to stderr

Import
======

::

    import console;

    console.log("Hello, World!");
    console.error("Something went wrong!");

Functions
=========

console.log()
-------------

Output messages to standard output (stdout).

**Syntax**::

    console.log(value1, value2, ...)

**Parameters:**
  * ``value1, value2, ...`` - Values to output (any type)

**Returns:** Nothing (null)

**Output:** Standard output (stdout)

**Examples**::

    import console;

    console.log("Hello, World!");
    console.log("Count:", 42);
    console.log("Values:", 1, 2, 3);

Use ``console.log()`` for general program output and informational messages.

console.info()
--------------

Output informational messages with "INFO:" prefix to stdout.

**Syntax**::

    console.info(value1, value2, ...)

**Parameters:**
  * ``value1, value2, ...`` - Values to output (any type)

**Returns:** Nothing (null)

**Output:** Standard output (stdout) with "INFO:" prefix

**Examples**::

    import console;

    console.info("Starting application");
    console.info("Processing", 100, "items");
    console.info("Task complete");

Use ``console.info()`` for informational messages that indicate program progress or status.

console.debug()
---------------

Output debug messages with "DEBUG:" prefix to stdout.

**Syntax**::

    console.debug(value1, value2, ...)

**Parameters:**
  * ``value1, value2, ...`` - Values to output (any type)

**Returns:** Nothing (null)

**Output:** Standard output (stdout) with "DEBUG:" prefix

**Examples**::

    import console;

    console.debug("Variable value:", x);
    console.debug("Function called with:", arg1, arg2);
    console.debug("Loop iteration:", i);

Use ``console.debug()`` for debugging information during development.

console.warn()
--------------

Output warning messages with "WARNING:" prefix to stderr.

**Syntax**::

    console.warn(value1, value2, ...)

**Parameters:**
  * ``value1, value2, ...`` - Values to output (any type)

**Returns:** Nothing (null)

**Output:** Standard error (stderr) with "WARNING:" prefix

**Examples**::

    import console;

    console.warn("Deprecated function used");
    console.warn("Low memory:", availableMemory);
    console.warn("Retrying operation");

Use ``console.warn()`` for warnings that don't stop program execution but indicate potential issues.

console.error()
---------------

Output error messages to stderr.

**Syntax**::

    console.error(value1, value2, ...)

**Parameters:**
  * ``value1, value2, ...`` - Values to output (any type)

**Returns:** Nothing (null)

**Output:** Standard error (stderr)

**Examples**::

    import console;

    console.error("File not found:", filename);
    console.error("Connection failed");
    console.error("Invalid input:", userInput);

Use ``console.error()`` for error messages that indicate failures or critical issues.

Usage Patterns
==============

Basic Logging
-------------

Simple output with different severity levels:

.. literalinclude:: ../../ml_snippets/standard-library/console/01_basic_logging.ml
   :language: ml

Application Logging
-------------------

Structured logging for application events:

.. literalinclude:: ../../ml_snippets/standard-library/console/02_application_logging.ml
   :language: ml

Debug Information
-----------------

Detailed debugging output:

.. literalinclude:: ../../ml_snippets/standard-library/console/03_debug_logging.ml
   :language: ml

Error Reporting
---------------

Comprehensive error reporting:

.. literalinclude:: ../../ml_snippets/standard-library/console/04_error_reporting.ml
   :language: ml

Comprehensive Example
=====================

Here's a complete example showing all console logging features in a practical application:

.. literalinclude:: ../../ml_snippets/standard-library/console/05_comprehensive_example.ml
   :language: ml

This example demonstrates:

* **Basic logging** - Using log() for general output
* **Info messages** - Tracking application progress
* **Debug output** - Detailed debugging information
* **Warnings** - Non-critical issues and deprecations
* **Error handling** - Reporting failures and exceptions
* **Structured logging** - Organizing log messages by severity

Best Practices
==============

Choosing the Right Method
--------------------------

Use the appropriate logging method for each situation:

**console.log()**
  * General program output
  * Results and data display
  * User-facing messages

**console.info()**
  * Application status updates
  * Progress indicators
  * Startup/shutdown messages

**console.debug()**
  * Variable inspection
  * Function call tracing
  * Loop iterations and intermediate values

**console.warn()**
  * Deprecated features
  * Non-critical issues
  * Recoverable errors
  * Performance concerns

**console.error()**
  * Failures and exceptions
  * Critical errors
  * Invalid states
  * Unrecoverable conditions

Formatting Messages
-------------------

::

    // Good - Clear and descriptive
    console.log("User logged in:", username);
    console.error("Failed to save file:", filename, "Error:", errorMessage);

    // Avoid - Unclear or too verbose
    console.log("Status: OK");  // What status?
    console.error("Error in function processData at line 42 in file main.ml");  // Too detailed

Message Structure
-----------------

::

    // Include context in messages
    console.info("Starting backup of", fileCount, "files");
    console.warn("Disk space low:", availableGB, "GB remaining");
    console.error("Authentication failed for user:", username);

    // Group related messages
    console.info("=== Application Startup ===");
    console.info("Loading configuration...");
    console.info("Connecting to database...");
    console.info("=== Ready ===");

Stderr vs Stdout
----------------

The console module automatically directs output to the appropriate stream:

**stdout (console.log, info, debug)**
  * Normal program output
  * Can be redirected separately
  * Suitable for processing by other programs

**stderr (console.warn, error)**
  * Error and warning messages
  * Separate from normal output
  * Always visible even when stdout is redirected

::

    // When running: mlpy run app.ml > output.txt
    console.log("This goes to output.txt");
    console.error("This still appears on screen");

Production vs Development
-------------------------

::

    // Development: Verbose debugging
    console.debug("Processing item", i, "of", total);
    console.debug("Current value:", value);

    // Production: Less verbose
    console.info("Processing", total, "items");
    console.info("Complete");

    // Always log errors
    console.error("Failed to process:", errorMessage);

Comparison with print()
=======================

The console module provides structured logging, while ``print()`` is simpler:

**console.log() vs print()**

::

    // console.log() - Same as print() for basic output
    console.log("Hello");  // stdout
    print("Hello");        // stdout

    // But console provides more options:
    console.error("Error");  // stderr
    console.info("Info");    // stdout with prefix
    console.debug("Debug");  // stdout with prefix

**When to use each:**

* **print()** - Quick output, simple scripts, examples
* **console.log()** - Applications, when you need other logging levels
* **console.error()** - Error messages that should go to stderr
* **console.warn/info/debug()** - Structured logging with severity levels

Performance
===========

Console output has minimal performance impact:

* All methods call Python's built-in ``print()``
* No buffering or formatting overhead
* Safe to use in loops and frequently-called code

::

    // Acceptable in performance-critical code
    for (i in range(1000)) {
        console.log("Processing:", i);
    }

    // For very high-frequency logging, consider:
    if (debugMode) {
        console.debug("High-frequency event:", data);
    }

Summary
=======

The console module provides:

* **Five logging methods**: log, info, debug, warn, error
* **Automatic stream selection**: stdout for normal output, stderr for errors
* **Simple API**: Import and use immediately
* **Severity levels**: Distinguish between information, warnings, and errors
* **No configuration**: Works out of the box

Key points:

* Import with ``import console;``
* Use ``log()`` for general output
* Use ``error()`` and ``warn()`` for issues
* Use ``info()`` and ``debug()`` for structured logging
* All methods accept multiple arguments
* Output goes to stdout or stderr automatically

The console module is ideal for:

* Application logging
* Error reporting
* Debug output
* Progress tracking
* Status updates

For more advanced logging, see the :doc:`../developer-guide/logging` guide.
