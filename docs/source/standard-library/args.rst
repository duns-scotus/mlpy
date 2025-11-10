Command-Line Arguments (args)
=============================

.. module:: args
   :synopsis: Parse command-line arguments with support for flags, options, and positional arguments

The ``args`` module provides comprehensive command-line argument parsing capabilities,
essential for building CLI tools and scripts in ML. It supports flags, options, positional
arguments, and automatic help text generation.

Required Capabilities
--------------------

- ``args.read`` - Read command-line arguments

Quick Start
-----------

.. code-block:: ml

   import args;
   import console;

   // Create parser
   parser = args.create_parser("File Processor", "Process text files");

   // Add arguments
   parser.add_flag("verbose", "v", "Enable verbose output");
   parser.add_option("output", "o", "Output file", "output.txt");
   parser.add_positional("input", "Input file to process", true);

   // Parse arguments
   parsed = parser.parse();

   // Use parsed values
   if (parsed.get_bool("verbose")) {
       console.log("Processing: " + parsed.get("input"));
   }

   input_file = parsed.get("input");
   output_file = parsed.get("output");

API Reference
-------------

Basic Functions
~~~~~~~~~~~~~~

all()
^^^^^

Get all command-line arguments including script name.

**Returns:** array[string] - All command-line arguments

**Capabilities Required:** ``args.read``

**Example:**

.. code-block:: ml

   import args;

   all_args = args.all();
   // Returns: ["script.ml", "--verbose", "input.txt"]

script()
^^^^^^^^

Get the script name (first argument).

**Returns:** string - Script name or empty string

**Capabilities Required:** ``args.read``

**Example:**

.. code-block:: ml

   import args;

   name = args.script();
   // Returns: "script.ml"

rest()
^^^^^^

Get arguments without the script name.

**Returns:** array[string] - Arguments excluding script name

**Capabilities Required:** ``args.read``

**Example:**

.. code-block:: ml

   import args;

   rest = args.rest();
   // Returns: ["--verbose", "input.txt"]

create_parser(name, description)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a new argument parser for structured argument parsing.

**Parameters:**

- ``name`` (string, optional) - Program name for help text
- ``description`` (string, optional) - Program description for help text

**Returns:** ArgParser - New parser instance

**Capabilities Required:** None

**Example:**

.. code-block:: ml

   parser = args.create_parser("Data Processor", "Process CSV files");

ArgParser Class
~~~~~~~~~~~~~~~

The ArgParser class provides structured argument parsing with schema validation.

add_flag(name, short, help_text)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Add a boolean flag argument (e.g., ``--verbose`` or ``-v``).

**Parameters:**

- ``name`` (string) - Long flag name (used with ``--``)
- ``short`` (string or null) - Short flag name (used with ``-``), or null
- ``help_text`` (string) - Description for help text

**Example:**

.. code-block:: ml

   parser.add_flag("verbose", "v", "Enable verbose output");
   parser.add_flag("debug", null, "Enable debug mode");

add_option(name, short, help_text, default)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Add an option argument that takes a value (e.g., ``--output file.txt`` or ``-o file.txt``).

**Parameters:**

- ``name`` (string) - Long option name (used with ``--``)
- ``short`` (string or null) - Short option name (used with ``-``), or null
- ``help_text`` (string) - Description for help text
- ``default`` (any) - Default value if not provided

**Example:**

.. code-block:: ml

   parser.add_option("output", "o", "Output file path", "output.txt");
   parser.add_option("format", null, "Output format", "json");
   parser.add_option("config", "c", "Config file", null);

add_positional(name, help_text, required)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Add a positional argument (values not preceded by flags).

**Parameters:**

- ``name`` (string) - Argument name
- ``help_text`` (string) - Description for help text
- ``required`` (boolean) - Whether argument is required

**Example:**

.. code-block:: ml

   parser.add_positional("input", "Input file to process", true);
   parser.add_positional("extra", "Additional files", false);

parse(argv)
^^^^^^^^^^^

Parse command-line arguments according to the defined schema.

**Parameters:**

- ``argv`` (array[string], optional) - Arguments to parse (defaults to actual command-line args)

**Returns:** ParsedArgs - Parsed arguments container

**Throws:** ValueError if arguments are invalid or required arguments are missing

**Example:**

.. code-block:: ml

   // Parse actual command-line arguments
   parsed = parser.parse();

   // Parse custom arguments (useful for testing)
   parsed = parser.parse(["-v", "--output", "result.txt", "input.txt"]);

**Error Handling:**

.. code-block:: ml

   try {
       parsed = parser.parse();
   } except (error) {
       console.log("Error: " + error.message);
       console.log(parser.help());
   }

help()
^^^^^^

Generate formatted help text showing all available arguments.

**Returns:** string - Formatted help text

**Example:**

.. code-block:: ml

   parser = args.create_parser("My Tool", "Does cool things");
   parser.add_flag("verbose", "v", "Enable verbose output");
   parser.add_option("output", "o", "Output file", "out.txt");
   parser.add_positional("input", "Input file", true);

   help_text = parser.help();
   console.log(help_text);

   // Output:
   // My Tool
   // Does cool things
   //
   // Usage: script.ml [options] <input>
   //
   // Positional Arguments:
   //   input              Input file (required)
   //
   // Options:
   //   -v, --verbose      Enable verbose output
   //   -o, --output VALUE Output file (default: out.txt)
   //   -h, --help         Show this help message

ParsedArgs Class
~~~~~~~~~~~~~~~~

The ParsedArgs class holds parsed argument values and provides methods to access them.

has(name)
^^^^^^^^^

Check if a flag, option, or positional argument is present.

**Parameters:**

- ``name`` (string) - Argument name

**Returns:** boolean - True if present, False otherwise

**Example:**

.. code-block:: ml

   if (parsed.has("verbose")) {
       console.log("Verbose mode enabled");
   }

   if (parsed.has("help")) {
       console.log(parser.help());
   }

get(name, default)
^^^^^^^^^^^^^^^^^^

Get the value of an option or positional argument.

**Parameters:**

- ``name`` (string) - Argument name
- ``default`` (any, optional) - Default value if not found

**Returns:** any - Argument value or default

**Example:**

.. code-block:: ml

   output_file = parsed.get("output");           // Get option value
   input_file = parsed.get("input");             // Get positional value
   config = parsed.get("config", "default.cfg"); // Get with default

get_bool(name)
^^^^^^^^^^^^^^

Get the boolean value of a flag.

**Parameters:**

- ``name`` (string) - Flag name

**Returns:** boolean - True if flag present, False otherwise

**Example:**

.. code-block:: ml

   is_verbose = parsed.get_bool("verbose");
   is_forced = parsed.get_bool("force");

   if (is_verbose) {
       console.log("Verbose mode enabled");
   }

flags()
^^^^^^^

Get all flags as a dictionary.

**Returns:** object - Dictionary mapping flag names to boolean values

**Example:**

.. code-block:: ml

   all_flags = parsed.flags();
   // Returns: {verbose: true, force: false}

options()
^^^^^^^^^

Get all options as a dictionary.

**Returns:** object - Dictionary mapping option names to their values

**Example:**

.. code-block:: ml

   all_options = parsed.options();
   // Returns: {output: "result.txt", format: "json"}

positionals()
^^^^^^^^^^^^^

Get all positional argument values as a list.

**Returns:** array - List of positional argument values in order

**Example:**

.. code-block:: ml

   positional_values = parsed.positionals();
   // Returns: ["input.txt", "output.txt"]

Common Patterns
---------------

Help Flag Handling
~~~~~~~~~~~~~~~~~~

Always check for help flag and display help text:

.. code-block:: ml

   import args;
   import console;

   parser = args.create_parser("My Tool", "Tool description");
   parser.add_flag("verbose", "v", "Verbose output");
   parser.add_option("output", "o", "Output file", "out.txt");

   parsed = parser.parse();

   // Check for help flag
   if (parsed.has("help")) {
       console.log(parser.help());
       // Exit or return early
   }

   // Continue with normal processing
   process_data();

Error Handling
~~~~~~~~~~~~~~

Gracefully handle argument parsing errors:

.. code-block:: ml

   import args;
   import console;

   parser = args.create_parser("Data Processor");
   parser.add_positional("input", "Input file", true);

   try {
       parsed = parser.parse();
       input_file = parsed.get("input");
       // Process input file
   } except (error) {
       console.log("Error: " + error.message);
       console.log("");
       console.log(parser.help());
       // Exit with error
   }

Combining Flags and Options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Build flexible CLI tools with multiple argument types:

.. code-block:: ml

   import args;
   import console;
   import file;

   parser = args.create_parser("File Converter", "Convert files between formats");

   // Flags
   parser.add_flag("verbose", "v", "Enable verbose output");
   parser.add_flag("force", "f", "Force overwrite existing files");
   parser.add_flag("dry-run", null, "Show what would be done without doing it");

   // Options
   parser.add_option("output", "o", "Output directory", ".");
   parser.add_option("format", null, "Output format: json, xml, csv", "json");
   parser.add_option("encoding", "e", "File encoding", "utf-8");

   // Positionals
   parser.add_positional("input", "Input file to convert", true);

   parsed = parser.parse();

   // Use flags for behavior
   verbose = parsed.get_bool("verbose");
   force = parsed.get_bool("force");
   dry_run = parsed.get_bool("dry-run");

   // Use options for configuration
   output_dir = parsed.get("output");
   format = parsed.get("format");
   encoding = parsed.get("encoding");

   // Use positional for required input
   input_file = parsed.get("input");

   if (verbose) {
       console.log("Converting: " + input_file);
       console.log("Format: " + format);
       console.log("Output: " + output_dir);
   }

   if (dry_run) {
       console.log("DRY RUN: Would convert " + input_file);
   } else {
       // Perform actual conversion
       convert_file(input_file, output_dir, format);
   }

Configuration with Defaults
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Provide sensible defaults for all options:

.. code-block:: ml

   import args;
   import env;

   parser = args.create_parser("Web Server");

   // Options with environment-aware defaults
   default_port = env.get_int("PORT", 8080);
   default_host = env.get("HOST", "localhost");

   parser.add_option("port", "p", "Server port", str(default_port));
   parser.add_option("host", "h", "Server host", default_host);
   parser.add_option("workers", "w", "Number of workers", "4");

   parsed = parser.parse();

   port = int(parsed.get("port"));
   host = parsed.get("host");
   workers = int(parsed.get("workers"));

   console.log("Starting server on " + host + ":" + str(port));
   console.log("Workers: " + str(workers));

Complete CLI Tool Example
--------------------------

Here's a complete example of a data processing CLI tool:

.. code-block:: ml

   import args;
   import console;
   import file;
   import csv;
   import log;
   import env;

   // Configure logging from environment
   log_level = env.get("LOG_LEVEL", "INFO");
   log.set_level(log_level);

   // Create argument parser
   parser = args.create_parser(
       "Data Processor",
       "Process CSV files with filtering and transformation"
   );

   // Add flags
   parser.add_flag("verbose", "v", "Enable verbose output");
   parser.add_flag("header", "h", "Input file has header row");
   parser.add_flag("append", "a", "Append to output file instead of overwriting");

   // Add options
   parser.add_option("input", "i", "Input CSV file", null);
   parser.add_option("output", "o", "Output CSV file", "output.csv");
   parser.add_option("delimiter", "d", "CSV delimiter", ",");
   parser.add_option("filter", "f", "Filter rows by column value", null);

   // Add positional (alternative to --input)
   parser.add_positional("file", "Input file (alternative to --input)", false);

   // Parse arguments
   parsed = parser.parse();

   // Handle help
   if (parsed.has("help")) {
       console.log(parser.help());
       // Exit
   }

   // Configure verbose mode
   verbose = parsed.get_bool("verbose");
   if (verbose) {
       log.set_level("DEBUG");
   }

   // Get input file (from option or positional)
   input_file = parsed.get("input");
   if (input_file == null) {
       input_file = parsed.get("file");
   }

   if (input_file == null) {
       console.log("Error: Input file required");
       console.log("");
       console.log(parser.help());
       // Exit with error
   }

   // Get other options
   output_file = parsed.get("output");
   delimiter = parsed.get("delimiter");
   has_header = parsed.get_bool("header");
   should_append = parsed.get_bool("append");
   filter_expr = parsed.get("filter");

   log.info("Starting data processing");
   log.debug("Input: " + input_file);
   log.debug("Output: " + output_file);
   log.debug("Delimiter: " + delimiter);

   // Read input CSV
   data = csv.read(input_file, delimiter, has_header);
   log.info("Read " + str(len(data)) + " rows");

   // Apply filter if specified
   if (filter_expr != null) {
       // Apply filtering logic here
       log.info("Applying filter: " + filter_expr);
   }

   // Write output CSV
   csv.write(output_file, data, delimiter);
   log.info("Wrote output to " + output_file);

   log.info("Processing complete");

Best Practices
--------------

1. **Always Provide Help Text**

   Make your CLI tools self-documenting with clear help text:

   .. code-block:: ml

      parser.add_flag("verbose", "v", "Enable verbose output with detailed logging");
      parser.add_option("timeout", "t", "Request timeout in seconds", "30");

2. **Use Sensible Defaults**

   Provide defaults for all optional arguments:

   .. code-block:: ml

      parser.add_option("format", "f", "Output format", "json");
      parser.add_option("output", "o", "Output file", "output.txt");

3. **Handle Errors Gracefully**

   Always wrap parse() in try-except and show help on errors:

   .. code-block:: ml

      try {
          parsed = parser.parse();
      } except (error) {
          console.log("Error: " + error.message);
          console.log(parser.help());
      }

4. **Support Help Flag**

   Always check for and handle the help flag:

   .. code-block:: ml

      if (parsed.has("help")) {
          console.log(parser.help());
          // Exit early
      }

5. **Use Environment Variables for Defaults**

   Combine args with env module for flexible configuration:

   .. code-block:: ml

      import env;
      default_port = env.get_int("PORT", 8080);
      parser.add_option("port", "p", "Server port", str(default_port));

6. **Validate Required Arguments**

   Mark critical arguments as required:

   .. code-block:: ml

      parser.add_positional("input", "Input file (required)", true);

Security Considerations
-----------------------

**Command Injection**
   Never pass user-supplied argument values directly to shell commands without validation.

**Path Traversal**
   Validate file paths from arguments to prevent accessing files outside intended directories.

**Resource Limits**
   Validate numeric arguments to prevent resource exhaustion (e.g., memory limits, timeouts).

**Example - Safe Path Validation:**

.. code-block:: ml

   import args;
   import path;

   parser = args.create_parser("File Tool");
   parser.add_option("output", "o", "Output directory", ".");

   parsed = parser.parse();
   output_dir = parsed.get("output");

   // Validate path is safe
   if (!path.is_safe(output_dir)) {
       console.log("Error: Invalid output directory");
       // Exit
   }

See Also
--------

- :doc:`env` - Environment variable access for configuration
- :doc:`log` - Logging for CLI tool output
- :doc:`csv` - CSV file processing
- :doc:`/user-guide/cli-tools` - Building complete CLI applications
