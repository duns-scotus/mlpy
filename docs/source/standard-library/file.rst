====
file
====

.. module:: file
   :synopsis: File I/O operations with capability-based security

The ``file`` module provides secure file system operations with fine-grained capability-based access control. All file operations require explicit capabilities and support path-based patterns for precise permission management.

Overview
========

The file module enables ML programs to read, write, copy, move, and delete files through a comprehensive set of functions. Every operation enforces security through capability tokens, ensuring that file system access is explicitly controlled.

Key Features
------------

- **Reading**: Text files, binary data, line-by-line reading
- **Writing**: Text files, binary data, line arrays, appending
- **Management**: Copy, move, delete, existence checking
- **Information**: Size, modification time, type checking
- **Security**: Capability-based access control with path patterns
- **Safety**: Path canonicalization prevents directory traversal

Security Model
==============

Capability-Based Access
-----------------------

All file operations require explicit capability grants:

.. code-block:: ml

    // Capabilities required:
    file.read         // Read file contents
    file.write        // Write to files
    file.delete       // Delete files
    file.append       // Append to files

    // Operations without capability requirements (safe metadata):
    file.exists()     // Check existence
    file.size()       // Get file size
    file.isFile()     // Check if file
    file.isDirectory()  // Check if directory

Path Patterns
-------------

Capabilities can be restricted by path patterns:

- ``file.read`` - Read any file
- ``file.read:/data/*`` - Read only from /data/ directory
- ``file.write:/output/*`` - Write only to /output/ directory
- ``file.delete:/temp/*`` - Delete only from /temp/ directory

Path Security
-------------

- All paths are canonicalized to prevent directory traversal
- Symlinks are resolved (or rejected, configurable)
- Path patterns support wildcards: ``*``, ``?``, ``[abc]``
- Dangerous operations denied by default (system directories)

Usage
=====

Import the file module to access all file operations:

.. code-block:: ml

    import file;

    // Read entire file
    content = file.read("data.txt");

    // Write file
    file.write("output.txt", "Hello World");

    // Read lines
    lines = file.readLines("config.txt");

    // Check existence (no capability needed)
    if (file.exists("file.txt")) {
        console.log("File exists");
    }

File Reading Operations
=======================

read
^^^^

.. function:: read(path, encoding="utf-8")

   Read entire file contents as string.

   :param path: File path to read
   :type path: string
   :param encoding: Text encoding (default: utf-8)
   :type encoding: string
   :return: File contents as string
   :rtype: string
   :raises: FileNotFoundError if file doesn't exist, PermissionError if not readable, UnicodeDecodeError if encoding wrong
   :capability: file.read or file.read:<path-pattern>

   **Examples:**

   .. code-block:: ml

       // Read text file
       content = file.read("data.txt");
       console.log("Content: " + content);

       // Read JSON file
       jsonStr = file.read("config.json", "utf-8");

       // Read with error handling
       if (file.exists("file.txt")) {
           data = file.read("file.txt");
       }

   **Use Cases:**

   - Loading configuration files
   - Reading data files
   - Processing text documents
   - Loading JSON/XML data

   **Security:**
   - Path is canonicalized to prevent directory traversal
   - Symlinks are resolved
   - Capability can be restricted by path pattern

readBytes
^^^^^^^^^

.. function:: readBytes(path)

   Read entire file as binary bytes.

   :param path: File path to read
   :type path: string
   :return: File contents as bytes
   :rtype: bytes
   :capability: file.read or file.read:<path-pattern>

   **Examples:**

   .. code-block:: ml

       // Read binary file
       imageData = file.readBytes("image.png");
       console.log("Image size: " + str(len(imageData)) + " bytes");

       // Read any binary data
       binaryData = file.readBytes("data.bin");

   **Use Cases:**

   - Reading image files
   - Loading binary data files
   - Processing non-text formats
   - Reading encoded data

readLines
^^^^^^^^^

.. function:: readLines(path, encoding="utf-8")

   Read file as array of lines (newlines stripped).

   :param path: File path to read
   :type path: string
   :param encoding: Text encoding (default: utf-8)
   :type encoding: string
   :return: List of lines (without newline characters)
   :rtype: array
   :capability: file.read or file.read:<path-pattern>

   **Examples:**

   .. code-block:: ml

       // Read configuration file
       lines = file.readLines("config.txt");
       console.log("Lines: " + str(len(lines)));

       // Process each line
       i = 0;
       while (i < len(lines)) {
           console.log("Line " + str(i + 1) + ": " + lines[i]);
           i = i + 1;
       }

       // Read CSV file
       csvLines = file.readLines("data.csv");
       header = csvLines[0];
       // Process data rows starting from index 1

   **Use Cases:**

   - Reading configuration files
   - Processing CSV data
   - Reading log files
   - Line-by-line text processing

File Writing Operations
=======================

write
^^^^^

.. function:: write(path, content, encoding="utf-8")

   Write string content to file (overwrites existing).

   :param path: File path to write
   :type path: string
   :param content: String content to write
   :type content: string
   :param encoding: Text encoding (default: utf-8)
   :type encoding: string
   :capability: file.write or file.write:<path-pattern>

   **Examples:**

   .. code-block:: ml

       // Write text file
       file.write("output.txt", "Hello World");

       // Write configuration
       config = "name=MyApp\nversion=1.0.0\ndebug=true";
       file.write("config.txt", config);

       // Overwrite existing file
       file.write("data.txt", "New content");

   **Use Cases:**

   - Saving application data
   - Writing configuration files
   - Creating reports
   - Exporting data

   **Security:**
   - Creates parent directories if they don't exist
   - Overwrites existing files without warning
   - Path is canonicalized

writeBytes
^^^^^^^^^^

.. function:: writeBytes(path, data)

   Write binary data to file.

   :param path: File path to write
   :type path: string
   :param data: Binary data to write
   :type data: bytes
   :capability: file.write or file.write:<path-pattern>

   **Examples:**

   .. code-block:: ml

       // Write binary data
       file.writeBytes("image.png", binaryImageData);

       // Write encoded data
       file.writeBytes("data.bin", encodedData);

   **Use Cases:**

   - Saving images
   - Writing binary file formats
   - Storing encoded data
   - Creating binary files

writeLines
^^^^^^^^^^

.. function:: writeLines(path, lines, encoding="utf-8")

   Write array of lines to file (adds newlines).

   :param path: File path to write
   :type path: string
   :param lines: Array of strings (newlines added automatically)
   :type lines: array
   :param encoding: Text encoding (default: utf-8)
   :type encoding: string
   :capability: file.write or file.write:<path-pattern>

   **Examples:**

   .. code-block:: ml

       // Write multiple lines
       lines = ["Line 1", "Line 2", "Line 3"];
       file.writeLines("output.txt", lines);

       // Write CSV data
       csvLines = [
           "id,name,score",
           "1,Alice,95",
           "2,Bob,87"
       ];
       file.writeLines("data.csv", csvLines);

       // Write log entries
       logLines = [
           "[INFO] Application started",
           "[INFO] User logged in",
           "[WARN] High memory usage"
       ];
       file.writeLines("app.log", logLines);

   **Use Cases:**

   - Writing CSV files
   - Creating log files
   - Generating reports
   - Writing structured text data

append
^^^^^^

.. function:: append(path, content, encoding="utf-8")

   Append string to end of file.

   :param path: File path to append to
   :type path: string
   :param content: String content to append
   :type content: string
   :param encoding: Text encoding (default: utf-8)
   :type encoding: string
   :capability: file.append or file.append:<path-pattern>

   **Examples:**

   .. code-block:: ml

       // Append to log file
       file.append("app.log", "[INFO] New log entry\n");

       // Add data to file
       file.append("data.txt", "Additional line\n");

       // Continuous logging
       i = 0;
       while (i < 5) {
           file.append("log.txt", "Entry " + str(i) + "\n");
           i = i + 1;
       }

   **Use Cases:**

   - Appending log entries
   - Adding records to files
   - Continuous data collection
   - Event logging

   **Security:**
   - Creates parent directories if needed
   - Creates file if it doesn't exist
   - Does not require file.write capability

File Management Operations
==========================

exists
^^^^^^

.. function:: exists(path)

   Check if file or directory exists.

   :param path: Path to check
   :type path: string
   :return: True if exists, False otherwise
   :rtype: boolean
   :capability: None required (safe read-only operation)

   **Examples:**

   .. code-block:: ml

       // Check before reading
       if (file.exists("config.json")) {
           config = file.read("config.json");
       } else {
           console.log("Config not found");
       }

       // Conditional creation
       if (!file.exists("data.txt")) {
           file.write("data.txt", "Initial content");
       }

   **Use Cases:**

   - Checking file existence before operations
   - Conditional file creation
   - Validating paths
   - Error prevention

delete
^^^^^^

.. function:: delete(path)

   Delete file.

   :param path: File path to delete
   :type path: string
   :return: True if deleted, False if didn't exist
   :rtype: boolean
   :capability: file.delete or file.delete:<path-pattern>

   **Examples:**

   .. code-block:: ml

       // Delete temporary file
       file.delete("temp.txt");

       // Conditional deletion
       if (file.exists("old_data.txt")) {
           deleted = file.delete("old_data.txt");
           console.log("Deleted: " + str(deleted));
       }

       // Cleanup multiple files
       file.delete("temp1.txt");
       file.delete("temp2.txt");
       file.delete("temp3.txt");

   **Use Cases:**

   - Removing temporary files
   - Cleaning up old data
   - File maintenance
   - Resource management

   **Security:**
   - Only deletes files, not directories
   - Use path.removeDir() for directories
   - Returns false if file doesn't exist

copy
^^^^

.. function:: copy(source, destination)

   Copy file from source to destination.

   :param source: Source file path
   :type source: string
   :param destination: Destination file path
   :type destination: string
   :capability: file.read (for source) and file.write (for destination)

   **Examples:**

   .. code-block:: ml

       // Create backup
       file.copy("important.txt", "important_backup.txt");

       // Duplicate file
       file.copy("original.txt", "copy.txt");

       // Verify copy
       file.copy("data.txt", "data_copy.txt");
       original = file.read("data.txt");
       copied = file.read("data_copy.txt");
       console.log("Match: " + str(original == copied));

   **Use Cases:**

   - Creating backups
   - Duplicating files
   - File versioning
   - Data preservation

   **Security:**
   - Requires both read and write capabilities
   - Creates destination parent directories if needed
   - Overwrites destination if exists

move
^^^^

.. function:: move(source, destination)

   Move or rename file.

   :param source: Source file path
   :type source: string
   :param destination: Destination file path
   :type destination: string
   :capability: file.read, file.write, file.delete

   **Examples:**

   .. code-block:: ml

       // Rename file
       file.move("old_name.txt", "new_name.txt");

       // Move to directory (in path with directory)
       file.move("file.txt", "archive/file.txt");

       // Archive with timestamp
       file.move("log.txt", "log_20240115.txt");

   **Use Cases:**

   - Renaming files
   - Moving files between directories
   - File archiving
   - Reorganizing files

   **Security:**
   - Requires read, write, and delete capabilities
   - Creates destination parent directories
   - Source is removed after move

File Information Operations
===========================

size
^^^^

.. function:: size(path)

   Get file size in bytes.

   :param path: File path
   :type path: string
   :return: File size in bytes
   :rtype: number
   :capability: None required (safe metadata operation)

   **Examples:**

   .. code-block:: ml

       // Get file size
       bytes = file.size("data.txt");
       console.log("Size: " + str(bytes) + " bytes");

       // Convert to KB
       kb = bytes / 1024;
       console.log("Size: " + str(kb) + " KB");

       // Size comparison
       size1 = file.size("file1.txt");
       size2 = file.size("file2.txt");
       if (size1 > size2) {
           console.log("file1.txt is larger");
       }

   **Use Cases:**

   - Checking file sizes
   - Storage management
   - Size-based processing decisions
   - Quota enforcement

modifiedTime
^^^^^^^^^^^^

.. function:: modifiedTime(path)

   Get file last modification time as Unix timestamp.

   :param path: File path
   :type path: string
   :return: Unix timestamp (seconds since epoch)
   :rtype: number
   :capability: None required (safe metadata operation)

   **Examples:**

   .. code-block:: ml

       // Get modification time
       timestamp = file.modifiedTime("file.txt");
       console.log("Last modified: " + str(timestamp));

   **Use Cases:**

   - Checking file age
   - Modified time comparison
   - Change detection
   - File synchronization

isFile
^^^^^^

.. function:: isFile(path)

   Check if path is a file (not directory).

   :param path: Path to check
   :type path: string
   :return: True if file, False otherwise
   :rtype: boolean
   :capability: None required

   **Examples:**

   .. code-block:: ml

       // Type checking
       if (file.isFile("data.txt")) {
           content = file.read("data.txt");
       } else {
           console.log("Not a file");
       }

   **Use Cases:**

   - Type validation
   - Conditional operations
   - Path verification
   - Error prevention

isDirectory
^^^^^^^^^^^

.. function:: isDirectory(path)

   Check if path is a directory.

   :param path: Path to check
   :type path: string
   :return: True if directory, False otherwise
   :rtype: boolean
   :capability: None required

   **Examples:**

   .. code-block:: ml

       // Directory checking
       if (file.isDirectory("data")) {
           console.log("It's a directory");
       }

   **Use Cases:**

   - Type validation
   - Directory vs file distinction
   - Path verification
   - Conditional logic

Practical Examples
==================

Configuration Manager
---------------------

Save and load application configuration:

.. code-block:: ml

    import console;
    import file;

    function saveConfig(filename, appName, version, debug) {
        lines = [
            "# Application Configuration",
            "app_name=" + appName,
            "version=" + version,
            "debug=" + str(debug)
        ];
        file.writeLines(filename, lines);
        console.log("Saved configuration to " + filename);
    }

    function loadConfig(filename) {
        if (!file.exists(filename)) {
            console.log("Config not found");
            return null;
        }
        return file.readLines(filename);
    }

    // Save configuration
    saveConfig("app.cfg", "MyApp", "1.0.0", true);

    // Load configuration
    config = loadConfig("app.cfg");
    if (config != null) {
        console.log("Loaded " + str(len(config)) + " lines");
    }

Data Logger
-----------

Structured logging system:

.. code-block:: ml

    import console;
    import file;

    function logMessage(logFile, level, message) {
        entry = "[" + level + "] " + message + "\n";
        file.append(logFile, entry);
    }

    // Initialize log
    logFile = "app.log";
    file.write(logFile, "");

    // Log messages
    logMessage(logFile, "INFO", "Application started");
    logMessage(logFile, "WARN", "High memory usage");
    logMessage(logFile, "ERROR", "Connection timeout");

    // Display log
    logContents = file.read(logFile);
    console.log(logContents);

Backup System
-------------

Create and verify file backups:

.. code-block:: ml

    import console;
    import file;

    function createBackup(sourceFile) {
        if (!file.exists(sourceFile)) {
            console.log("Source not found");
            return false;
        }

        backupFile = sourceFile + ".backup";
        file.copy(sourceFile, backupFile);
        console.log("Backup created: " + backupFile);

        // Verify backup
        sourceSize = file.size(sourceFile);
        backupSize = file.size(backupFile);
        return sourceSize == backupSize;
    }

    // Create important file
    file.write("data.txt", "Critical data");

    // Backup and verify
    verified = createBackup("data.txt");
    console.log("Backup verified: " + str(verified));

CSV Processor
-------------

Read and write CSV data:

.. code-block:: ml

    import console;
    import file;

    // Write CSV
    csvLines = [
        "id,name,department",
        "1,Alice,Engineering",
        "2,Bob,Marketing",
        "3,Charlie,Sales"
    ];
    file.writeLines("employees.csv", csvLines);

    // Read CSV
    data = file.readLines("employees.csv");
    header = data[0];
    console.log("Header: " + header);

    // Process records
    i = 1;
    while (i < len(data)) {
        console.log("Record " + str(i) + ": " + data[i]);
        i = i + 1;
    }

Log Rotation
------------

Rotate logs based on size:

.. code-block:: ml

    import console;
    import file;

    function rotateLog(logFile, maxSize) {
        if (!file.exists(logFile)) {
            return false;
        }

        currentSize = file.size(logFile);
        if (currentSize >= maxSize) {
            // Archive old log
            archiveName = logFile + ".old";
            if (file.exists(archiveName)) {
                file.delete(archiveName);
            }

            file.move(logFile, archiveName);
            file.write(logFile, "");
            console.log("Log rotated");
            return true;
        }

        return false;
    }

    // Create log
    file.write("app.log", "");

    // Add entries
    i = 0;
    while (i < 10) {
        file.append("app.log", "Entry " + str(i) + "\n");
        i = i + 1;
    }

    // Try rotation
    rotateLog("app.log", 50);

File Statistics
---------------

Analyze file system usage:

.. code-block:: ml

    import console;
    import file;

    files = ["file1.txt", "file2.txt", "file3.txt"];

    // Create test files
    file.write("file1.txt", "Small");
    file.write("file2.txt", "Medium content");
    file.write("file3.txt", "Large content with more data");

    // Calculate statistics
    totalSize = 0;
    i = 0;
    while (i < len(files)) {
        if (file.exists(files[i])) {
            size = file.size(files[i]);
            totalSize = totalSize + size;
            console.log(files[i] + ": " + str(size) + " bytes");
        }
        i = i + 1;
    }

    console.log("Total: " + str(totalSize) + " bytes");

Common Patterns
===============

Safe File Reading
-----------------

Always check existence before reading:

.. code-block:: ml

    if (file.exists("data.txt")) {
        content = file.read("data.txt");
        console.log("Content: " + content);
    } else {
        console.log("File not found");
    }

Atomic File Updates
-------------------

Update files safely with backups:

.. code-block:: ml

    // 1. Create backup
    file.copy("important.txt", "important.txt.bak");

    // 2. Update original
    file.write("important.txt", "Updated content");

    // 3. Verify update
    if (file.exists("important.txt")) {
        // Success - cleanup backup
        file.delete("important.txt.bak");
    }

Conditional File Creation
--------------------------

Create files only if they don't exist:

.. code-block:: ml

    if (!file.exists("config.txt")) {
        file.write("config.txt", "Default configuration");
        console.log("Created default config");
    }

Batch File Operations
---------------------

Process multiple files efficiently:

.. code-block:: ml

    files = ["file1.txt", "file2.txt", "file3.txt"];

    // Create all files
    i = 0;
    while (i < len(files)) {
        file.write(files[i], "Content " + str(i));
        i = i + 1;
    }

    // Process all files
    i = 0;
    while (i < len(files)) {
        if (file.exists(files[i])) {
            content = file.read(files[i]);
            console.log(files[i] + ": " + content);
        }
        i = i + 1;
    }

Performance Considerations
==========================

Reading Performance
-------------------

- ``read()`` loads entire file into memory - suitable for small/medium files
- ``readLines()`` also loads entire file - use for line-based processing
- ``readBytes()`` for binary data - same memory considerations

Writing Performance
-------------------

- ``write()`` overwrites entire file - single operation
- ``writeLines()`` writes all lines at once - efficient for batch writes
- ``append()`` adds to end - efficient for continuous logging

File Operations
---------------

- ``copy()`` reads source and writes destination - two I/O operations
- ``move()`` typically just renames - fast within same filesystem
- ``delete()`` is fast - single filesystem operation

Metadata Operations
-------------------

- ``exists()``, ``size()``, ``isFile()``, ``isDirectory()`` are fast
- No capability checks required
- Minimal overhead for checking file metadata

Best Practices
==============

Security
--------

1. **Request Minimal Capabilities**: Only request file.read if you don't need writing
2. **Use Path Patterns**: Restrict capabilities to specific directories
3. **Validate Paths**: Check paths before operations to prevent errors
4. **Handle Errors**: File operations can fail - check exists() first

Error Handling
--------------

1. **Check Existence**: Use ``exists()`` before reading/deleting
2. **Verify Types**: Use ``isFile()`` to ensure path is a file
3. **Handle Missing Files**: Provide defaults or error messages
4. **Atomic Operations**: Use backups for critical file updates

File Management
---------------

1. **Clean Up Temporary Files**: Delete temporary files when done
2. **Use Descriptive Names**: Clear file names improve maintainability
3. **Implement Backups**: Backup important files before modifications
4. **Rotate Logs**: Prevent log files from growing indefinitely

Data Integrity
--------------

1. **Verify Copies**: Check sizes or hashes after copying
2. **Use Backups**: Create backups before destructive operations
3. **Atomic Updates**: Write to temp file, then move to final location
4. **Validate Content**: Check file content after reading

See Also
========

- :doc:`path` - Path operations and directory management
- :doc:`json` - JSON parsing for structured data files
- :doc:`console` - Logging and output functions

.. note::

   All file operations require explicit capability grants except for metadata operations (``exists``, ``size``, ``isFile``, ``isDirectory``). This ensures secure, controlled access to the file system.
