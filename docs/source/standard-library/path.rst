path - Filesystem Path Operations
==================================

The ``path`` module provides comprehensive filesystem path manipulation and directory management operations. All path functions work cross-platform, automatically handling Windows vs Unix path differences.

**Security Model:**

- Most path manipulation functions require no capabilities (join, dirname, basename, etc.)
- Directory listing requires ``path.read`` capability
- Directory creation/deletion requires ``path.write`` capability
- Path canonicalization prevents directory traversal attacks

Overview
--------

The path module provides three main categories of operations:

1. **Path Manipulation** - Join, split, normalize, and convert paths
2. **Filesystem Queries** - Check existence, file type, and path properties
3. **Directory Operations** - List, create, and remove directories

Import the module:

.. code-block:: ml

   import path;

   // Path manipulation (no capabilities required)
   fullPath = path.join("data", "files", "report.pdf");

   // Directory listing (requires path.read)
   files = path.listDir("/data");

   // Directory management (requires path.write)
   path.createDir("/output/results", true);

Path Manipulation Functions
---------------------------

These functions manipulate path strings without accessing the filesystem. No capabilities required.

join()
~~~~~~

.. code-block:: ml

   path.join(segment1, segment2, ...) -> string

Joins path segments using the correct separator for the operating system.

**Parameters:**

- Variable number of path segments (strings)

**Returns:**

- Combined path using OS-specific separator (``/`` on Unix, ``\`` on Windows)

**Examples:**

.. code-block:: ml

   import path;

   // Basic joining
   fullPath = path.join("home", "user", "documents");
   console.log(fullPath);  // "home/user/documents" on Unix

   // Build file path
   configPath = path.join("etc", "app", "config.json");

   // Join many segments
   deepPath = path.join("a", "b", "c", "d", "e", "file.txt");

**Best Practices:**

- Always use ``join()`` instead of string concatenation for cross-platform compatibility
- Accepts any number of arguments
- Automatically uses correct separator for the operating system

dirname()
~~~~~~~~~

.. code-block:: ml

   path.dirname(path) -> string

Extracts the directory portion of a path.

**Parameters:**

- ``path`` (string) - File path to analyze

**Returns:**

- Directory portion of the path

**Examples:**

.. code-block:: ml

   import path;

   fullPath = "/home/user/documents/report.pdf";
   dir = path.dirname(fullPath);
   console.log(dir);  // "/home/user/documents"

   // Works with relative paths
   relPath = "data/files/config.json";
   dir2 = path.dirname(relPath);
   console.log(dir2);  // "data/files"

basename()
~~~~~~~~~~

.. code-block:: ml

   path.basename(path) -> string

Extracts the filename portion of a path.

**Parameters:**

- ``path`` (string) - File path to analyze

**Returns:**

- Filename portion of the path (including extension)

**Examples:**

.. code-block:: ml

   import path;

   fullPath = "/home/user/documents/report.pdf";
   filename = path.basename(fullPath);
   console.log(filename);  // "report.pdf"

   // Just the directory name
   dirPath = "/var/log/app";
   name = path.basename(dirPath);
   console.log(name);  // "app"

extname()
~~~~~~~~~

.. code-block:: ml

   path.extname(path) -> string

Extracts the file extension from a path.

**Parameters:**

- ``path`` (string) - File path to analyze

**Returns:**

- File extension including the dot (e.g., ``.pdf``), or empty string if no extension

**Examples:**

.. code-block:: ml

   import path;

   // File with extension
   path1 = "/data/report.pdf";
   ext1 = path.extname(path1);
   console.log(ext1);  // ".pdf"

   // Multiple dots
   path2 = "archive.tar.gz";
   ext2 = path.extname(path2);
   console.log(ext2);  // ".gz"

   // No extension
   path3 = "/usr/bin/application";
   ext3 = path.extname(path3);
   console.log(ext3);  // ""

split()
~~~~~~~

.. code-block:: ml

   path.split(path) -> array

Splits a path into its component parts.

**Parameters:**

- ``path`` (string) - Path to split

**Returns:**

- Array of path components

**Examples:**

.. code-block:: ml

   import path;

   fullPath = "/home/user/documents/report.pdf";
   parts = path.split(fullPath);

   // parts = ["/", "home", "user", "documents", "report.pdf"]
   console.log("Components: " + str(len(parts)));

   // Iterate over parts
   i = 0;
   while (i < len(parts)) {
       console.log("  [" + str(i) + "] " + parts[i]);
       i = i + 1;
   }

normalize()
~~~~~~~~~~~

.. code-block:: ml

   path.normalize(path) -> string

Normalizes a path by removing redundant separators and resolving ``.`` and ``..`` references.

**Parameters:**

- ``path`` (string) - Path to normalize

**Returns:**

- Normalized path

**Examples:**

.. code-block:: ml

   import path;

   // Remove redundant separators
   messy1 = "/home//user///documents";
   clean1 = path.normalize(messy1);
   console.log(clean1);  // "/home/user/documents"

   // Resolve . and ..
   messy2 = "/home/user/./documents/../files/data.txt";
   clean2 = path.normalize(messy2);
   console.log(clean2);  // "/home/user/files/data.txt"

   // Relative paths
   messy3 = "src/./mlpy/../stdlib/path.ml";
   clean3 = path.normalize(messy3);
   console.log(clean3);  // "src/stdlib/path.ml"

**Security Note:**

Always normalize user-provided paths to prevent directory traversal attacks.

absolute()
~~~~~~~~~~

.. code-block:: ml

   path.absolute(path) -> string

Converts a relative path to an absolute path.

**Parameters:**

- ``path`` (string) - Relative or absolute path

**Returns:**

- Absolute path (based on current working directory if relative)

**Examples:**

.. code-block:: ml

   import path;

   // Convert relative to absolute
   relPath = "data/files/config.json";
   absPath = path.absolute(relPath);
   console.log(absPath);  // "/current/dir/data/files/config.json"

   // Already absolute (returns unchanged)
   absPath2 = path.absolute("/etc/config.json");
   console.log(absPath2);  // "/etc/config.json"

relative()
~~~~~~~~~~

.. code-block:: ml

   path.relative(from, to) -> string

Computes the relative path from one location to another.

**Parameters:**

- ``from`` (string) - Starting location
- ``to`` (string) - Target location

**Returns:**

- Relative path from ``from`` to ``to``

**Examples:**

.. code-block:: ml

   import path;

   from = "/home/user/projects/mlpy/src";
   to = "/home/user/projects/mlpy/docs/guide.md";

   relPath = path.relative(from, to);
   console.log(relPath);  // "../../docs/guide.md"

   // Within same directory
   from2 = "/var/www/html";
   to2 = "/var/www/html/index.html";
   relPath2 = path.relative(from2, to2);
   console.log(relPath2);  // "index.html"

Filesystem Query Functions
--------------------------

These functions check filesystem properties. No capabilities required.

exists()
~~~~~~~~

.. code-block:: ml

   path.exists(path) -> boolean

Checks if a path exists (file or directory).

**Parameters:**

- ``path`` (string) - Path to check

**Returns:**

- ``true`` if path exists, ``false`` otherwise

**Examples:**

.. code-block:: ml

   import path;

   if (path.exists("/etc/hosts")) {
       console.log("File exists");
   }

   // Check before reading
   configPath = "/etc/app/config.json";
   if (path.exists(configPath)) {
       content = file.read(configPath);
   } else {
       console.log("Config not found");
   }

isFile()
~~~~~~~~

.. code-block:: ml

   path.isFile(path) -> boolean

Checks if a path exists and is a regular file.

**Parameters:**

- ``path`` (string) - Path to check

**Returns:**

- ``true`` if path is a file, ``false`` otherwise

**Examples:**

.. code-block:: ml

   import path;

   if (path.isFile("/etc/hosts")) {
       console.log("It's a file");
   }

   // Distinguish files from directories
   if (path.exists(somePath)) {
       if (path.isFile(somePath)) {
           content = file.read(somePath);
       } elif (path.isDirectory(somePath)) {
           files = path.listDir(somePath);
       }
   }

isDirectory()
~~~~~~~~~~~~~

.. code-block:: ml

   path.isDirectory(path) -> boolean

Checks if a path exists and is a directory.

**Parameters:**

- ``path`` (string) - Path to check

**Returns:**

- ``true`` if path is a directory, ``false`` otherwise

**Examples:**

.. code-block:: ml

   import path;

   if (path.isDirectory("/var/log")) {
       console.log("It's a directory");
       files = path.listDir("/var/log");
   }

   // Safe directory listing
   dataDir = "/data";
   if (path.exists(dataDir) && path.isDirectory(dataDir)) {
       files = path.listDir(dataDir);
       console.log("Found " + str(len(files)) + " files");
   }

isAbsolute()
~~~~~~~~~~~~

.. code-block:: ml

   path.isAbsolute(path) -> boolean

Checks if a path is absolute (starts with root).

**Parameters:**

- ``path`` (string) - Path to check

**Returns:**

- ``true`` if path is absolute, ``false`` if relative

**Examples:**

.. code-block:: ml

   import path;

   console.log(path.isAbsolute("/home/user"));  // true
   console.log(path.isAbsolute("relative/path"));  // false

   // Ensure absolute paths
   userPath = "data/config.json";
   if (!path.isAbsolute(userPath)) {
       userPath = path.absolute(userPath);
   }

Directory Listing Functions
---------------------------

These functions list directory contents. Require ``path.read`` capability.

listDir()
~~~~~~~~~

.. code-block:: ml

   path.listDir(dirPath = ".") -> array

Lists files and directories in a directory (non-recursive).

**Parameters:**

- ``dirPath`` (string, optional) - Directory path (default: current directory)

**Returns:**

- Array of filenames (not full paths), sorted alphabetically

**Capability Required:**

- ``path.read`` or ``path.read:<path-pattern>``

**Examples:**

.. code-block:: ml

   import path;

   // List current directory
   files = path.listDir(".");
   console.log("Found " + str(len(files)) + " files");

   // List specific directory
   dataFiles = path.listDir("/data");
   i = 0;
   while (i < len(dataFiles)) {
       console.log("  " + dataFiles[i]);
       i = i + 1;
   }

   // Build full paths
   baseDir = "/data";
   files = path.listDir(baseDir);
   i = 0;
   while (i < len(files)) {
       fullPath = path.join(baseDir, files[i]);
       console.log(fullPath);
       i = i + 1;
   }

**Security:**

- Returns only filenames, not full paths
- Does not traverse subdirectories
- Results are sorted for consistency

glob()
~~~~~~

.. code-block:: ml

   path.glob(pattern) -> array

Lists files matching a glob pattern (supports recursive matching).

**Parameters:**

- ``pattern`` (string) - Glob pattern with wildcards

**Returns:**

- Array of matching file paths, sorted alphabetically

**Capability Required:**

- ``path.read`` or ``path.read:<path-pattern>``

**Glob Patterns:**

- ``*`` - Matches any characters
- ``?`` - Matches single character
- ``[abc]`` - Matches a, b, or c
- ``**`` - Matches directories recursively

**Examples:**

.. code-block:: ml

   import path;

   // Find all text files
   txtFiles = path.glob("*.txt");
   console.log("Found " + str(len(txtFiles)) + " .txt files");

   // Find all ML files recursively
   mlFiles = path.glob("**/*.ml");

   // Find files with specific pattern
   dataFiles = path.glob("data/file[0-9].txt");
   // Matches: data/file0.txt, data/file1.txt, etc.

   // Complex patterns
   configFiles = path.glob("**/config/*.{json,yaml}");

**Use Cases:**

- Finding files by extension
- Recursive file searches
- Pattern-based file selection
- Build system file discovery

walk()
~~~~~~

.. code-block:: ml

   path.walk(dirPath, maxDepth = -1) -> array

Walks a directory tree and returns all file paths (recursive).

**Parameters:**

- ``dirPath`` (string) - Root directory to walk
- ``maxDepth`` (number, optional) - Maximum depth (-1 for unlimited)

**Returns:**

- Array of file paths relative to ``dirPath``, sorted alphabetically

**Capability Required:**

- ``path.read`` or ``path.read:<path-pattern>``

**Examples:**

.. code-block:: ml

   import path;

   // Walk entire directory tree
   allFiles = path.walk("/data");
   console.log("Total files: " + str(len(allFiles)));

   // Limit depth
   shallowFiles = path.walk("/data", 1);  // Only 1 level deep

   // Find all files with specific extension
   allFiles = path.walk("/project");
   mlFiles = [];
   i = 0;
   while (i < len(allFiles)) {
       file = allFiles[i];
       if (path.extname(file) == ".ml") {
           mlFiles = mlFiles + [file];
       }
       i = i + 1;
   }
   console.log("Found " + str(len(mlFiles)) + " ML files");

**Security:**

- Respects ``maxDepth`` limit
- Returns relative paths for safety
- Does not follow symbolic links

Directory Management Functions
------------------------------

These functions create and remove directories. Require ``path.write`` capability.

createDir()
~~~~~~~~~~~

.. code-block:: ml

   path.createDir(dirPath, parents = true) -> void

Creates a directory (and parent directories if needed).

**Parameters:**

- ``dirPath`` (string) - Directory path to create
- ``parents`` (boolean, optional) - Create parent directories (default: ``true``)

**Capability Required:**

- ``path.write`` or ``path.write:<path-pattern>``

**Examples:**

.. code-block:: ml

   import path;

   // Create single directory
   path.createDir("/data/output");

   // Create directory with parents
   path.createDir("/a/b/c/d/e", true);  // Creates all parents

   // Idempotent (safe to call multiple times)
   path.createDir("/data/cache");
   path.createDir("/data/cache");  // No error if exists

   // Create project structure
   dirs = [
       "/project/src",
       "/project/tests",
       "/project/docs",
       "/project/build"
   ];
   i = 0;
   while (i < len(dirs)) {
       path.createDir(dirs[i], true);
       i = i + 1;
   }

**Best Practices:**

- Always create parent directories by default
- Safe to call on existing directories
- Use absolute paths for clarity

removeDir()
~~~~~~~~~~~

.. code-block:: ml

   path.removeDir(dirPath) -> void

Removes a directory (must be empty).

**Parameters:**

- ``dirPath`` (string) - Directory path to remove

**Capability Required:**

- ``path.write`` or ``path.write:<path-pattern>``

**Examples:**

.. code-block:: ml

   import path;

   // Remove empty directory
   path.removeDir("/tmp/empty");

   // Safe removal pattern
   tempDir = "/tmp/cache";
   if (path.exists(tempDir) && path.isDirectory(tempDir)) {
       path.removeDir(tempDir);
   }

**Important:**

- Only removes empty directories
- Use ``removeDirRecursive()`` for non-empty directories
- Throws error if directory is not empty

removeDirRecursive()
~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   path.removeDirRecursive(dirPath) -> void

Removes a directory and all its contents recursively.

**Parameters:**

- ``dirPath`` (string) - Directory path to remove

**Capability Required:**

- ``path.write`` or ``path.write:<path-pattern>``

**Examples:**

.. code-block:: ml

   import path;

   // Remove directory and contents
   path.removeDirRecursive("/tmp/data");

   // Safe removal with confirmation
   oldDir = "/data/archive/2020";
   if (path.exists(oldDir)) {
       console.log("Removing: " + oldDir);
       path.removeDirRecursive(oldDir);
   }

   // Clean and recreate
   buildDir = "/project/build";
   if (path.exists(buildDir)) {
       path.removeDirRecursive(buildDir);
   }
   path.createDir(buildDir, true);

**⚠️  WARNING:**

- **DANGEROUS**: Removes all contents recursively
- No confirmation or undo
- Use with extreme caution
- Double-check path before calling

Path Utility Functions
----------------------

These functions provide system information. No capabilities required.

cwd()
~~~~~

.. code-block:: ml

   path.cwd() -> string

Gets the current working directory.

**Returns:**

- Current working directory absolute path

**Examples:**

.. code-block:: ml

   import path;

   current = path.cwd();
   console.log("Working in: " + current);

   // Build path relative to current directory
   configPath = path.join(path.cwd(), "config.json");

home()
~~~~~~

.. code-block:: ml

   path.home() -> string

Gets the user's home directory.

**Returns:**

- User home directory path

**Examples:**

.. code-block:: ml

   import path;

   homeDir = path.home();
   console.log("Home: " + homeDir);

   // Build config path in home directory
   configPath = path.join(homeDir, ".config", "app", "settings.json");

tempDir()
~~~~~~~~~

.. code-block:: ml

   path.tempDir() -> string

Gets the system temporary directory.

**Returns:**

- System temporary directory path

**Examples:**

.. code-block:: ml

   import path;

   tmp = path.tempDir();
   console.log("Temp directory: " + tmp);

   // Create temporary file path
   sessionId = "session-123";
   tempFile = path.join(tmp, sessionId + ".tmp");

separator()
~~~~~~~~~~~

.. code-block:: ml

   path.separator() -> string

Gets the path separator for the current operating system.

**Returns:**

- Path separator (``"/"`` on Unix, ``"\\"`` on Windows)

**Examples:**

.. code-block:: ml

   import path;

   sep = path.separator();
   console.log("Separator: '" + sep + "'");

   // Manual path construction (avoid - use join instead)
   parts = ["home", "user", "file.txt"];
   // Don't do this: path = parts[0] + sep + parts[1] + sep + parts[2]
   // Do this instead: path = path.join("home", "user", "file.txt")

delimiter()
~~~~~~~~~~~

.. code-block:: ml

   path.delimiter() -> string

Gets the path list delimiter for the current operating system.

**Returns:**

- Path delimiter (``":"`` on Unix, ``";"`` on Windows)

**Examples:**

.. code-block:: ml

   import path;

   delim = path.delimiter();
   console.log("Delimiter: '" + delim + "'");

   // Used in PATH-like environment variables
   // Unix: "/usr/bin:/usr/local/bin:/home/user/bin"
   // Windows: "C:\Windows;C:\Program Files;C:\Users\user\bin"

Common Patterns
---------------

Path Validation
~~~~~~~~~~~~~~~

.. code-block:: ml

   import path;

   function validatePath(userPath) {
       // Step 1: Normalize
       normalized = path.normalize(userPath);

       // Step 2: Make absolute
       absolute = path.absolute(normalized);

       // Step 3: Check if absolute
       if (!path.isAbsolute(absolute)) {
           console.log("Path is not absolute");
           return "";
       }

       return absolute;
   }

   safePath = validatePath("../data/config.json");

Directory Traversal Prevention
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import path;

   function isSafePath(basePath, userInput) {
       // Normalize user input
       normalized = path.normalize(userInput);

       // Join with base path
       fullPath = path.join(basePath, normalized);

       // Make absolute
       absolute = path.absolute(fullPath);

       // Ensure still under base path
       baseAbs = path.absolute(basePath);

       // Check if absolute path starts with base path
       // (implementation would verify this)

       return absolute;
   }

   baseDir = "/data/files";
   userFile = "../../../etc/passwd";  // Attack attempt
   safePath = isSafePath(baseDir, userFile);

File Finding by Extension
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import path;

   function findFilesByExtension(dir, extension) {
       allFiles = path.walk(dir);
       matching = [];

       i = 0;
       while (i < len(allFiles)) {
           file = allFiles[i];
           if (path.extname(file) == extension) {
               matching = matching + [file];
           }
           i = i + 1;
       }

       return matching;
   }

   jsonFiles = findFilesByExtension("/data", ".json");
   console.log("Found " + str(len(jsonFiles)) + " JSON files");

Project Structure Creation
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import path;

   function createProject(projectName) {
       base = path.join(path.cwd(), projectName);

       structure = [
           "src",
           "tests",
           "docs",
           "data/input",
           "data/output",
           "logs",
           "build"
       ];

       i = 0;
       while (i < len(structure)) {
           dir = path.join(base, structure[i]);
           path.createDir(dir, true);
           console.log("Created: " + dir);
           i = i + 1;
       }
   }

   createProject("my-ml-app");

Backup Management
~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import path;

   function createBackup(sourceDir, backupName) {
       backupBase = path.join(path.cwd(), "backups");
       backupPath = path.join(backupBase, backupName);

       // Create backup directory
       path.createDir(backupPath, true);

       console.log("Backup created at: " + backupPath);
       return backupPath;
   }

   function cleanOldBackups(keepCount) {
       backupDir = path.join(path.cwd(), "backups");
       backups = path.listDir(backupDir);

       if (len(backups) > keepCount) {
           removeCount = len(backups) - keepCount;
           console.log("Removing " + str(removeCount) + " old backups");

           // Remove oldest backups
           i = 0;
           while (i < removeCount) {
               oldBackup = path.join(backupDir, backups[i]);
               path.removeDirRecursive(oldBackup);
               i = i + 1;
           }
       }
   }

   createBackup("/data", "backup-2024-01-15");
   cleanOldBackups(5);  // Keep last 5 backups

Temporary Workspace
~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import path;

   function setupTempWorkspace(sessionId) {
       tmpBase = path.tempDir();
       workspace = path.join(tmpBase, "session-" + sessionId);

       // Create workspace structure
       dirs = ["input", "processing", "output", "logs"];
       i = 0;
       while (i < len(dirs)) {
           dir = path.join(workspace, dirs[i]);
           path.createDir(dir, true);
           i = i + 1;
       }

       return workspace;
   }

   function cleanupWorkspace(workspace) {
       if (path.exists(workspace)) {
           path.removeDirRecursive(workspace);
           console.log("Cleaned up: " + workspace);
       }
   }

   workspace = setupTempWorkspace("12345");
   // ... do work ...
   cleanupWorkspace(workspace);

Best Practices
--------------

Path Manipulation
~~~~~~~~~~~~~~~~~

1. **Always use path.join()** - Never concatenate paths with ``+``
2. **Normalize user input** - Call ``normalize()`` on user-provided paths
3. **Use absolute paths** - Convert to absolute for clarity and safety
4. **Check path type** - Use ``isAbsolute()`` to validate paths

Directory Operations
~~~~~~~~~~~~~~~~~~~~

1. **Create parents by default** - Use ``createDir(path, true)``
2. **Check before removing** - Verify path exists and is directory
3. **Be cautious with recursive removal** - Double-check paths before calling ``removeDirRecursive()``
4. **Handle errors gracefully** - Check ``exists()`` before operations

File Discovery
~~~~~~~~~~~~~~

1. **Use listDir() for simple listings** - Non-recursive directory contents
2. **Use glob() for patterns** - Efficient pattern-based file matching
3. **Use walk() for recursion** - Complete directory tree traversal
4. **Limit walk() depth** - Use ``maxDepth`` parameter for large trees

Security
~~~~~~~~

1. **Validate user paths** - Normalize and check they stay within allowed directories
2. **Use capability restrictions** - Apply path patterns to limit access
3. **Prevent traversal attacks** - Check paths don't escape base directory
4. **Canonicalize paths** - Use ``absolute()`` and ``normalize()`` together

Performance
~~~~~~~~~~~

1. **Cache directory listings** - Store results if listing same directory repeatedly
2. **Use appropriate method** - ``listDir()`` is faster than ``walk()`` for single directory
3. **Filter early** - Use glob patterns instead of listing all files
4. **Process in batches** - Handle large directories in chunks

Cross-Platform
~~~~~~~~~~~~~~

1. **Use path utilities** - Let ``separator()`` and ``delimiter()`` handle OS differences
2. **Test on both platforms** - Windows and Unix have different path formats
3. **Avoid hardcoded separators** - Always use ``join()`` and path functions
4. **Handle case sensitivity** - Unix is case-sensitive, Windows is not

Complete Example
----------------

.. literalinclude:: ../../ml_snippets/standard-library/path/05_comprehensive_example.ml
   :language: ml

See Also
--------

- :doc:`file` - File I/O operations with capability-based security
- :doc:`console` - Logging and output for debugging path operations
- :doc:`json` - Configuration file parsing for path-based settings
