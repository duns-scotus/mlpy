CSV File Processing (csv)
==========================

.. module:: csv
   :synopsis: CSV file reading and writing with support for headers

The ``csv`` module provides functions for reading and writing CSV (Comma-Separated Values) files,
supporting both dictionary and array formats with configurable delimiters.

Required Capabilities
--------------------

- ``file.read`` - Read CSV files
- ``file.write`` - Write CSV files

Quick Start
-----------

.. code-block:: ml

   import csv;

   // Read CSV as array of objects
   users = csv.read("users.csv");
   // [{name: "Alice", age: "30"}, {name: "Bob", age: "25"}]

   // Write CSV from objects
   new_users = [{name: "Charlie", age: "35"}];
   csv.write("output.csv", new_users);

   // Process CSV data
   for (user in users) {
       console.log(user.name + " is " + user.age);
   }

API Reference
-------------

Reading CSV Files
~~~~~~~~~~~~~~~~~

read(file_path, delimiter, headers, encoding)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Read CSV file and return as array of objects or arrays.

**Parameters:**

- ``file_path`` (string) - Path to CSV file
- ``delimiter`` (string, optional) - Field delimiter (default: ",")
- ``headers`` (boolean, optional) - If True, use first row as keys (default: True)
- ``encoding`` (string, optional) - File encoding (default: "utf-8")

**Returns:** array - Array of objects (if headers=True) or array of arrays (if headers=False)

**Capabilities Required:** ``file.read``

**Example:**

.. code-block:: ml

   import csv;

   // Read with headers (returns array of objects)
   users = csv.read("users.csv");
   console.log(users[0].name);  // Access by key

   // Read without headers (returns array of arrays)
   data = csv.read("data.csv", ",", false);
   console.log(data[0][0]);  // Access by index

   // Read with custom delimiter (semicolon)
   european_data = csv.read("data.csv", ";");

read_string(csv_string, delimiter, headers)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Parse CSV from string.

**Parameters:**

- ``csv_string`` (string) - CSV content as string
- ``delimiter`` (string, optional) - Field delimiter (default: ",")
- ``headers`` (boolean, optional) - If True, use first row as keys (default: True)

**Returns:** array - Array of objects or arrays

**Capabilities Required:** None

**Example:**

.. code-block:: ml

   import csv;

   csv_text = "name,age\nAlice,30\nBob,25";
   data = csv.read_string(csv_text);

   console.log(data[0].name);  // "Alice"
   console.log(len(data));     // 2

get_headers(file_path, delimiter, encoding)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get header row from CSV file.

**Parameters:**

- ``file_path`` (string) - Path to CSV file
- ``delimiter`` (string, optional) - Field delimiter (default: ",")
- ``encoding`` (string, optional) - File encoding (default: "utf-8")

**Returns:** array - Array of header names

**Capabilities Required:** ``file.read``

**Example:**

.. code-block:: ml

   import csv;

   headers = csv.get_headers("users.csv");
   // ["name", "age", "city", "email"]

   console.log("CSV has " + str(len(headers)) + " columns");

count_rows(file_path, delimiter, encoding)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Count number of data rows in CSV file (excluding header).

**Parameters:**

- ``file_path`` (string) - Path to CSV file
- ``delimiter`` (string, optional) - Field delimiter (default: ",")
- ``encoding`` (string, optional) - File encoding (default: "utf-8")

**Returns:** integer - Number of data rows

**Capabilities Required:** ``file.read``

**Example:**

.. code-block:: ml

   import csv;

   count = csv.count_rows("large_file.csv");
   console.log("File contains " + str(count) + " records");

Writing CSV Files
~~~~~~~~~~~~~~~~~

write(file_path, data, delimiter, headers, encoding)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Write data to CSV file.

**Parameters:**

- ``file_path`` (string) - Path to output CSV file
- ``data`` (array) - Array of objects or array of arrays
- ``delimiter`` (string, optional) - Field delimiter (default: ",")
- ``headers`` (boolean, optional) - If True, write headers from object keys (default: True)
- ``encoding`` (string, optional) - File encoding (default: "utf-8")

**Capabilities Required:** ``file.write``

**Example:**

.. code-block:: ml

   import csv;

   // Write array of objects (headers auto-generated)
   users = [
       {name: "Alice", age: "30", city: "NYC"},
       {name: "Bob", age: "25", city: "LA"}
   ];
   csv.write("users.csv", users);

   // Write array of arrays without headers
   data = [
       ["Name", "Age"],
       ["Alice", "30"],
       ["Bob", "25"]
   ];
   csv.write("data.csv", data, ",", false);

write_string(data, delimiter, headers)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Convert data to CSV string.

**Parameters:**

- ``data`` (array) - Array of objects or array of arrays
- ``delimiter`` (string, optional) - Field delimiter (default: ",")
- ``headers`` (boolean, optional) - If True, include headers from object keys (default: True)

**Returns:** string - CSV formatted string

**Capabilities Required:** None

**Example:**

.. code-block:: ml

   import csv;

   users = [{name: "Alice", age: "30"}];
   csv_text = csv.write_string(users);

   console.log(csv_text);
   // Output:
   // name,age
   // Alice,30

append(file_path, row, delimiter, encoding)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Append a single row to existing CSV file.

**Parameters:**

- ``file_path`` (string) - Path to CSV file
- ``row`` (object or array) - Object or array to append
- ``delimiter`` (string, optional) - Field delimiter (default: ",")
- ``encoding`` (string, optional) - File encoding (default: "utf-8")

**Capabilities Required:** ``file.read``, ``file.write``

**Example:**

.. code-block:: ml

   import csv;

   // Append object (matches existing columns)
   new_user = {name: "Charlie", age: "35", city: "SF"};
   csv.append("users.csv", new_user);

   // Append array
   new_row = ["David", "40", "Seattle"];
   csv.append("users.csv", new_row);

Common Patterns
---------------

Data Import and Export
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import csv;
   import console;

   // Import data
   users = csv.read("input.csv");
   console.log("Loaded " + str(len(users)) + " users");

   // Process data
   for (user in users) {
       // Add computed field
       user.full_name = user.first_name + " " + user.last_name;
   }

   // Export processed data
   csv.write("output.csv", users);
   console.log("Exported processed data");

Data Filtering
~~~~~~~~~~~~~~

.. code-block:: ml

   import csv;

   // Read all users
   users = csv.read("users.csv");

   // Filter by criteria
   adults = [];
   for (user in users) {
       age = int(user.age);
       if (age >= 18) {
           adults.append(user);
       }
   }

   // Write filtered data
   csv.write("adults.csv", adults);
   console.log("Found " + str(len(adults)) + " adults");

Data Transformation
~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import csv;

   // Read source data
   source = csv.read("sales.csv");

   // Transform to new format
   transformed = [];
   for (row in source) {
       new_row = {
           product: row.product_name,
           revenue: row.price + " USD",
           date: row.order_date
       };
       transformed.append(new_row);
   }

   // Write transformed data
   csv.write("sales_report.csv", transformed);

Merging CSV Files
~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import csv;

   // Read multiple files
   file1 = csv.read("users_2023.csv");
   file2 = csv.read("users_2024.csv");

   // Merge data
   all_users = [];
   for (user in file1) {
       all_users.append(user);
   }
   for (user in file2) {
       all_users.append(user);
   }

   // Write combined data
   csv.write("all_users.csv", all_users);
   console.log("Merged " + str(len(all_users)) + " users");

Data Validation
~~~~~~~~~~~~~~~

.. code-block:: ml

   import csv;
   import console;

   users = csv.read("users.csv");
   valid_users = [];
   errors = [];

   for (user in users) {
       // Validate required fields
       if (user.name == "" || user.email == "") {
           errors.append("Missing data for user: " + user.name);
       } else {
           valid_users.append(user);
       }
   }

   // Write valid data
   csv.write("valid_users.csv", valid_users);

   // Report errors
   console.log("Valid: " + str(len(valid_users)));
   console.log("Errors: " + str(len(errors)));

ETL Pipeline
~~~~~~~~~~~~

.. code-block:: ml

   import csv;
   import console;

   console.log("ETL Pipeline starting...");

   // Extract
   raw_data = csv.read("raw_data.csv");
   console.log("Extracted " + str(len(raw_data)) + " records");

   // Transform
   transformed = [];
   for (row in raw_data) {
       cleaned_row = {
           id: row.user_id,
           name: row.first_name + " " + row.last_name,
           email: row.email,
           status: row.is_active == "1" ? "active" : "inactive"
       };
       transformed.append(cleaned_row);
   }
   console.log("Transformed " + str(len(transformed)) + " records");

   // Load
   csv.write("processed_data.csv", transformed);
   console.log("Loaded to processed_data.csv");

Working with Different Delimiters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import csv;

   // European CSV (semicolon delimiter)
   european_data = csv.read("european.csv", ";");

   // Tab-delimited (TSV)
   // Note: Use actual tab character in string
   tsv_data = csv.read("data.tsv", "\t");

   // Pipe-delimited
   pipe_data = csv.read("data.psv", "|");

   // Convert between formats
   csv.write("output.csv", european_data, ",");

Array-Based CSV (No Headers)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import csv;

   // Read as arrays
   data = csv.read("matrix.csv", ",", false);

   // Process as 2D array
   for (row in data) {
       console.log("Row has " + str(len(row)) + " columns");
       for (col in row) {
           // Process cell value
       }
   }

   // Write arrays
   matrix = [
       [1, 2, 3],
       [4, 5, 6],
       [7, 8, 9]
   ];
   csv.write("matrix_out.csv", matrix, ",", false);

Integration with Other Modules
-------------------------------

With Crypto Module
~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import csv;
   import crypto;

   // Read users
   users = csv.read("users.csv");

   // Add secure IDs and hash emails
   for (user in users) {
       user.id = crypto.uuid();
       user.email_hash = crypto.sha256(user.email);
   }

   // Write with security info
   csv.write("users_secure.csv", users);

With Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import csv;
   import env;

   // Get file paths from environment
   input_file = env.require("INPUT_CSV");
   output_file = env.get("OUTPUT_CSV", "output.csv");

   // Process
   data = csv.read(input_file);
   // ... transform data ...
   csv.write(output_file, data);

With File Operations
~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import csv;
   import file;
   import path;

   // Check if file exists
   if (file.exists("data.csv")) {
       data = csv.read("data.csv");
       console.log("Loaded existing data");
   } else {
       data = [];
       console.log("Starting fresh");
   }

   // Create directory if needed
   output_dir = "output";
   if (!path.exists(output_dir)) {
       path.mkdir(output_dir);
   }

   csv.write(output_dir + "/result.csv", data);

Performance Considerations
--------------------------

Large File Handling
~~~~~~~~~~~~~~~~~~~

For large CSV files, consider processing in chunks:

.. code-block:: ml

   import csv;
   import console;

   // Check file size first
   row_count = csv.count_rows("large_file.csv");
   console.log("File has " + str(row_count) + " rows");

   if (row_count > 10000) {
       console.log("Large file detected, process carefully");
   }

   // Read and process
   data = csv.read("large_file.csv");
   // Process data...

Memory Usage
~~~~~~~~~~~~

CSV reading loads entire file into memory:

.. code-block:: ml

   import csv;

   // ❌ BAD - Will use lots of memory for large files
   big_data = csv.read("100MB_file.csv");

   // ✅ BETTER - Check size first
   row_count = csv.count_rows("file.csv");
   if (row_count < 10000) {
       data = csv.read("file.csv");
   } else {
       console.log("File too large, process differently");
   }

Incremental Writing
~~~~~~~~~~~~~~~~~~~~

Use ``append()`` for incremental writes:

.. code-block:: ml

   import csv;

   // Initialize file with headers
   initial_data = [{name: "Alice", age: "30"}];
   csv.write("results.csv", initial_data);

   // Append rows as you process
   for (i = 0; i < 100; i = i + 1) {
       new_row = {name: "User" + str(i), age: str(20 + i)};
       csv.append("results.csv", new_row);
   }

Error Handling
--------------

File Not Found
~~~~~~~~~~~~~~

.. code-block:: ml

   import csv;
   import file;
   import console;

   try {
       data = csv.read("data.csv");
   } except (error) {
       console.error("Failed to read CSV: " + str(error));
       // Handle missing file
       data = [];
   }

   // Or check first
   if (file.exists("data.csv")) {
       data = csv.read("data.csv");
   }

Invalid CSV Format
~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import csv;
   import console;

   try {
       data = csv.read("malformed.csv");

       // Validate data structure
       if (len(data) == 0) {
           console.log("Warning: CSV file is empty");
       }

   } except (error) {
       console.error("CSV parsing error: " + str(error));
   }

Encoding Issues
~~~~~~~~~~~~~~~

.. code-block:: ml

   import csv;
   import console;

   // Try different encodings
   try {
       data = csv.read("data.csv", ",", true, "utf-8");
   } except (error) {
       console.log("UTF-8 failed, trying latin-1");
       try {
           data = csv.read("data.csv", ",", true, "latin-1");
       } except (error2) {
           console.error("Could not read file with any encoding");
       }
   }

Best Practices
--------------

Always Include Headers
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import csv;

   // ✅ GOOD - Include headers for clarity
   users = [
       {name: "Alice", age: "30", email: "alice@example.com"}
   ];
   csv.write("users.csv", users);  // Headers included by default

   // ❌ BAD - Arrays without headers are harder to work with
   data = [["Alice", "30"]];
   csv.write("data.csv", data, ",", false);

Consistent Column Order
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import csv;

   // Ensure consistent key order in objects
   users = [
       {name: "Alice", age: "30", city: "NYC"},
       {name: "Bob", age: "25", city: "LA"},
       {name: "Charlie", age: "35", city: "SF"}
   ];

   csv.write("users.csv", users);
   // All objects have same keys in same order

Validate Data Before Writing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import csv;
   import console;

   function validate_user(user) {
       if (user.name == "" || user.email == "") {
           return false;
       }
       return true;
   }

   users = [...];  // Your data

   // Validate before writing
   valid = true;
   for (user in users) {
       if (!validate_user(user)) {
           console.error("Invalid user: " + user.name);
           valid = false;
       }
   }

   if (valid) {
       csv.write("users.csv", users);
   }

Use Descriptive File Names
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import csv;
   import datetime;

   // ✅ GOOD - Descriptive names with timestamps
   timestamp = str(datetime.now().year) + "-" +
               str(datetime.now().month);
   filename = "sales_report_" + timestamp + ".csv";
   csv.write(filename, sales_data);

   // ❌ BAD - Generic names
   csv.write("output.csv", data);

See Also
--------

- :doc:`file` - File operations (check existence, get size)
- :doc:`json` - JSON file processing (alternative format)
- :doc:`crypto` - Cryptography (for hashing sensitive data)
- :doc:`env` - Environment variables (for file paths)

Examples
--------

Complete Data Processing Script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import csv;
   import console;
   import file;

   console.log("=== CSV Data Processing Pipeline ===");

   // 1. Load source data
   if (!file.exists("source.csv")) {
       console.error("Source file not found");
   } else {
       console.log("[1/4] Loading source data...");
       source = csv.read("source.csv");
       console.log("Loaded " + str(len(source)) + " records");

       // 2. Clean and transform
       console.log("[2/4] Transforming data...");
       cleaned = [];
       for (row in source) {
           if (row.status == "active") {
               cleaned_row = {
                   id: row.user_id,
                   name: row.full_name,
                   email: row.email,
                   joined: row.created_date
               };
               cleaned.append(cleaned_row);
           }
       }
       console.log("Cleaned " + str(len(cleaned)) + " active records");

       // 3. Save results
       console.log("[3/4] Saving results...");
       csv.write("active_users.csv", cleaned);

       // 4. Generate summary
       console.log("[4/4] Generating summary...");
       summary = [{
           total_source: str(len(source)),
           total_active: str(len(cleaned)),
           total_inactive: str(len(source) - len(cleaned))
       }];
       csv.write("summary.csv", summary);

       console.log("=== Processing Complete ===");
   }
