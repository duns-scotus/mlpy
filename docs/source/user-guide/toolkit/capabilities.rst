====================================
Introduction to Capabilities
====================================

ML programs run in a security-restricted environment by default. This guide introduces the capability-based security system that controls what programs can access.

.. contents::
   :local:
   :depth: 3

What Are Capabilities?
======================

**Capabilities** are permission tokens that grant ML programs access to specific system resources. Think of them as keys that unlock particular operations:

- **File I/O capability** → Read/write files
- **Network capability** → Make HTTP requests
- **Console capability** → Print output
- **Path capability** → List directories

Without the appropriate capability, programs cannot perform privileged operations. This ensures that:

- **Untrusted code runs safely** without risking your system
- **Programs have minimal permissions** following the principle of least privilege
- **Security violations are caught early** with clear error messages
- **Audit trails exist** for all capability grants and operations

Why Capability-Based Security?
===============================

Traditional Security Problems
-------------------------------

Traditional programming languages often operate under an "all-or-nothing" security model:

**Problem 1: Unrestricted Code Execution**

.. code-block:: python

   # Python script can do ANYTHING:
   import os
   import shutil

   # Delete your entire home directory
   shutil.rmtree(os.path.expanduser("~"))

   # Execute arbitrary system commands
   os.system("rm -rf /")

   # Access any file on your system
   with open("/etc/passwd") as f:
       passwords = f.read()

**Problem 2: Third-Party Code Risks**

When you install a Python package, it can:

- Read all your files (including SSH keys, browser cookies, passwords)
- Send data to any server on the internet
- Modify or delete critical system files
- Run background processes

**Problem 3: Debugging Nightmare**

When something goes wrong, it's hard to know:

- What resources did the program access?
- What permissions did it have?
- Where did the security violation occur?

The Capability Solution
------------------------

ML's capability system solves these problems:

**1. Default Deny**

Programs start with **zero permissions**. They must explicitly request capabilities:

.. code-block:: ml

   // This fails - no console capability
   console.log("Hello");
   // ❌ Error: Missing capability 'console.write'

   // Grant capability first
   // In REPL: .grant console.write

   // Now it works
   console.log("Hello");
   // ✅ Prints: Hello

**2. Fine-Grained Control**

Capabilities can restrict access to specific resources:

.. code-block:: ml

   // Can only read files in /data/ directory
   // Capability: file.read:/data/*

   file.read("/data/config.json");  // ✅ Allowed
   file.read("/etc/passwd");         // ❌ Blocked

**3. Audit Trail**

All capability grants are tracked and logged:

.. code-block:: ml

   ml[secure]> .capabilities
   Granted Capabilities:
     ✓ console.write
     ✓ file.read:/data/*
     ✓ network.http:api.example.com

**4. Safe Third-Party Code**

When running untrusted code, you control exactly what it can access:

.. code-block:: bash

   # Run with only console output capability
   echo '{"capabilities": ["console.write"]}' > mlpy.json
   mlpy run untrusted_script.ml

The Capability Security Model
===============================

How Capabilities Work
----------------------

ML's capability system operates at multiple levels:

**1. Static Analysis (Compile-Time)**

When you transpile ML code, the security analyzer:

- Scans for dangerous operations (eval, exec, __import__)
- Detects capability requirements for standard library functions
- Reports security violations before execution

.. code-block:: ml

   // Static analysis detects this
   eval("malicious_code()");
   // ❌ Security Error: eval() is forbidden

**2. Runtime Validation**

During execution, the runtime:

- Checks capabilities before each privileged operation
- Validates resource patterns (file paths, URLs, etc.)
- Enforces capability constraints

.. code-block:: ml

   // Runtime checks capability token
   file.read("/data/users.json");
   // 1. Check: Has file.read capability?
   // 2. Check: Does /data/users.json match resource pattern?
   // 3. If both pass → Allow operation

**3. Sandbox Isolation**

For maximum security, programs run in sandboxed subprocesses:

- Separate process space (cannot access parent process memory)
- Resource limits (CPU time, memory, file size)
- System call filtering (blocks dangerous operations)

Capability Lifecycle
---------------------

Capabilities follow a clear lifecycle:

**1. Request** - Program or developer identifies needed capabilities

.. code-block:: ml

   // I need to read configuration files
   import file;
   config = file.read("config.json");

**2. Grant** - Capability is explicitly granted

.. code-block:: ml

   // REPL session
   ml[secure]> .grant file.read:*.json

   // Or in mlpy.json
   {
     "capabilities": ["file.read:*.json"]
   }

**3. Validate** - Runtime validates each operation

.. code-block:: ml

   file.read("config.json");    // ✅ Matches *.json pattern
   file.read("secrets.txt");     // ❌ Doesn't match pattern

**4. Revoke** - Capability can be revoked during REPL session

.. code-block:: ml

   ml[secure]> .revoke file.read
   ml[secure]> file.read("config.json");
   // ❌ Error: Missing capability 'file.read'

Runtime Capability Exploration
================================

ML provides built-in functions to explore and detect capabilities at runtime. This enables defensive programming, graceful degradation, and better debugging.

Why Runtime Introspection?
----------------------------

**Problem: Exception-Based Detection**

Without introspection, the only way to check capabilities is to attempt an operation and catch the error:

.. code-block:: ml

   // ❌ Clumsy exception-based detection
   try {
       content = file.read("config.json");
       hasFileAccess = true;
   } except (e) {
       hasFileAccess = false;
   }

**Solution: Explicit Capability Queries**

With introspection functions, you can check capabilities before attempting operations:

.. code-block:: ml

   // ✅ Clean capability check
   if (hasCapability("file.read")) {
       content = file.read("config.json");
   } else {
       print("File reading not available");
   }

**Benefits:**

- **Defensive Programming** - Check before attempting operations
- **Graceful Degradation** - Provide fallbacks when capabilities are missing
- **Feature Detection** - Enable/disable features based on available permissions
- **Better Debugging** - Inspect execution environment at runtime
- **Self-Documenting Code** - Explicit permission requirements

Introspection Functions
------------------------

ML provides three builtin functions for capability introspection:

hasCapability(name)
^^^^^^^^^^^^^^^^^^^^

Check if a specific capability is available.

**Signature:**

.. code-block:: ml

   hasCapability(name: string) -> boolean

**Parameters:**

- ``name`` - Capability type (e.g., "file.read", "network.http")

**Returns:**

- ``true`` if capability is available and valid
- ``false`` if capability is not available or expired

**Examples:**

.. code-block:: ml

   // Check single capability
   if (hasCapability("file.read")) {
       content = file.read("data.txt");
   }

   // Check multiple capabilities
   canProcess = hasCapability("file.read") &&
                hasCapability("file.write");

   if (canProcess) {
       processFiles();
   }

   // Feature detection
   hasNetwork = hasCapability("network.http");
   if (hasNetwork) {
       syncWithServer();
   } else {
       print("Running in offline mode");
   }

getCapabilities()
^^^^^^^^^^^^^^^^^^

Get a list of all available capabilities.

**Signature:**

.. code-block:: ml

   getCapabilities() -> array[string]

**Returns:**

- Sorted array of capability type strings
- Empty array if no capabilities are granted
- Includes capabilities inherited from parent contexts

**Examples:**

.. code-block:: ml

   // List all capabilities
   caps = getCapabilities();
   print("Available capabilities: " + str(caps));
   // Output: ["file.read", "file.write", "network.http"]

   // Check total capability count
   capCount = len(getCapabilities());
   if (capCount == 0) {
       print("Running in restricted mode");
   }

   // Iterate over capabilities
   caps = getCapabilities();
   for (cap in caps) {
       print("  - " + cap);
   }

getCapabilityInfo(name)
^^^^^^^^^^^^^^^^^^^^^^^^

Get detailed information about a specific capability.

**Signature:**

.. code-block:: ml

   getCapabilityInfo(name: string) -> object | null

**Parameters:**

- ``name`` - Capability type to query

**Returns:**

Dictionary with capability details, or ``null`` if not available:

.. code-block:: ml

   {
       type: "file.read",              // Capability type
       available: true,                 // Is currently valid?
       patterns: ["*.txt", "data/*"],  // Resource patterns (or null)
       operations: ["read"],            // Allowed operations (or null)
       expires_at: null,                // Expiration time (or null)
       usage_count: 5,                  // Times capability has been used
       max_usage: null                  // Max usage limit (or null)
   }

**Examples:**

.. code-block:: ml

   // Get basic info
   info = getCapabilityInfo("file.read");
   if (info != null) {
       print("File read capability:");
       print("  Available: " + str(info.available));
       print("  Usage: " + str(info.usage_count) + " times");
   }

   // Check resource restrictions
   info = getCapabilityInfo("file.read");
   if (info != null && info.patterns != null) {
       print("Can only read files matching:");
       for (pattern in info.patterns) {
           print("  - " + pattern);
       }
   }

   // Check usage limits
   info = getCapabilityInfo("network.http");
   if (info != null && info.max_usage != null) {
       remaining = info.max_usage - info.usage_count;
       print("HTTP requests remaining: " + str(remaining));
   }

   // Check expiration
   info = getCapabilityInfo("file.read");
   if (info != null && info.expires_at != null) {
       print("Capability expires at: " + info.expires_at);
   }

Common Patterns
----------------

Pattern 1: Defensive Programming
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Check capabilities before attempting operations:

.. code-block:: ml

   function loadData(source) {
       if (hasCapability("file.read")) {
           return loadFromFile(source);
       } elif (hasCapability("network.http")) {
           return loadFromUrl(source);
       } else {
           print("ERROR: No data loading capabilities");
           print("Required: file.read OR network.http");
           return null;
       }
   }

   data = loadData("config.json");

Pattern 2: Graceful Degradation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Provide fallbacks when capabilities are missing:

.. code-block:: ml

   function saveData(data) {
       if (hasCapability("file.write")) {
           file.write("data.json", data);
           return "saved to file";
       } elif (hasCapability("network.http")) {
           http.post("https://api.example.com/save", {body: data});
           return "uploaded to server";
       } else {
           print("WARNING: Cannot persist data");
           return "memory-only";
       }
   }

   result = saveData(processedData);
   print("Data: " + result);

Pattern 3: Feature Detection
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Enable features based on available capabilities:

.. code-block:: ml

   // Configure features at startup
   features = [];

   if (hasCapability("file.read")) {
       features = features + ["load-files"];
   }

   if (hasCapability("file.write")) {
       features = features + ["save-files"];
   }

   if (hasCapability("network.http")) {
       features = features + ["sync-cloud", "auto-update"];
   }

   if (hasCapability("gui.create")) {
       features = features + ["gui-mode"];
   } else {
       features = features + ["cli-mode"];
   }

   print("Enabled features: " + str(features));

Pattern 4: Startup Validation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Verify required capabilities at program start:

.. code-block:: ml

   function validateEnvironment() {
       required = ["file.read", "file.write", "console.write"];
       missing = [];

       for (cap in required) {
           if (!hasCapability(cap)) {
               missing = missing + [cap];
           }
       }

       if (len(missing) > 0) {
           print("ERROR: Missing required capabilities:");
           for (cap in missing) {
               print("  - " + cap);
           }
           print("\nTo grant capabilities:");
           print("  mlpy run program.ml \\");
           for (cap in missing) {
               print("    --grant " + cap + " \\");
           }
           return false;
       }

       print("All required capabilities available");
       return true;
   }

   // Validate at startup
   if (!validateEnvironment()) {
       throw "Cannot run without required capabilities";
   }

   // Continue with main program
   main();

Pattern 5: Debug Environment Info
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Print execution environment for debugging:

.. code-block:: ml

   function debugEnvironment() {
       print("=== Execution Environment ===");
       print("");

       caps = getCapabilities();
       print("Capabilities (" + str(len(caps)) + "):");

       if (len(caps) == 0) {
           print("  (none - running in restricted mode)");
       } else {
           for (cap in caps) {
               info = getCapabilityInfo(cap);
               if (info != null) {
                   status = info.available ? "valid" : "expired";
                   print("  - " + cap + " (" + status + ")");

                   if (info.patterns != null) {
                       print("    Patterns: " + str(info.patterns));
                   }

                   if (info.max_usage != null) {
                       remaining = info.max_usage - info.usage_count;
                       usage = str(info.usage_count) + "/" +
                               str(info.max_usage);
                       print("    Usage: " + usage +
                             " (remaining: " + str(remaining) + ")");
                   }

                   if (info.expires_at != null) {
                       print("    Expires: " + info.expires_at);
                   }
               }
           }
       }

       print("");
   }

   // Call at program start or on demand
   debugEnvironment();

Pattern 6: Smart Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Adapt program behavior to available capabilities:

.. code-block:: ml

   function configureApp() {
       config = {
           mode: "unknown",
           features: [],
           dataSource: "none"
       };

       // Determine mode based on capabilities
       if (hasCapability("gui.create")) {
           config.mode = "gui";
       } elif (hasCapability("network.http")) {
           config.mode = "networked";
       } else {
           config.mode = "minimal";
       }

       // Configure data source
       if (hasCapability("file.read")) {
           config.dataSource = "file";
           config.features = config.features + ["load-config"];
       } elif (hasCapability("network.http")) {
           config.dataSource = "network";
           config.features = config.features + ["fetch-remote"];
       }

       // Add persistence if available
       if (hasCapability("file.write")) {
           config.features = config.features + ["save-data"];
       }

       return config;
   }

   appConfig = configureApp();
   print("Application mode: " + appConfig.mode);
   print("Data source: " + appConfig.dataSource);
   print("Features: " + str(appConfig.features));

Pattern 7: Constraint Checking
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Check capability constraints before operations:

.. code-block:: ml

   function canProcessFile(filepath) {
       info = getCapabilityInfo("file.read");

       if (info == null) {
           print("File reading not available");
           return false;
       }

       if (!info.available) {
           print("File read capability has expired");
           return false;
       }

       // Check resource pattern restrictions
       if (info.patterns != null) {
           // In real code, would check if filepath matches patterns
           print("File access restricted to: " + str(info.patterns));
       }

       // Check usage limits
       if (info.max_usage != null) {
           remaining = info.max_usage - info.usage_count;
           if (remaining <= 0) {
               print("File read quota exceeded");
               return false;
           }
           print("File reads remaining: " + str(remaining));
       }

       return true;
   }

   if (canProcessFile("data.txt")) {
       content = file.read("data.txt");
       processData(content);
   }

Best Practices
---------------

**1. Check Before Use**

Always verify capabilities before attempting operations:

.. code-block:: ml

   // ✅ Good - check first
   if (hasCapability("file.write")) {
       file.write("output.txt", data);
   } else {
       print("Cannot save: file.write not permitted");
   }

   // ❌ Avoid - exception-based detection
   try {
       file.write("output.txt", data);
   } except (e) {
       print("Cannot save: " + str(e));
   }

**2. Provide Clear Error Messages**

Use capability info to explain limitations:

.. code-block:: ml

   if (!hasCapability("file.write")) {
       print("Cannot save file: file.write capability not granted");
       print("This program is running in read-only mode");
       print("");
       print("To enable file writing:");
       print("  mlpy run program.ml --grant file.write");
   } else {
       info = getCapabilityInfo("file.write");
       if (info.patterns != null) {
           print("Can only write to: " + str(info.patterns));
       }
   }

**3. Validate on Startup**

Check required capabilities when program starts:

.. code-block:: ml

   required = ["file.read", "network.http"];
   missing = [];

   for (cap in required) {
       if (!hasCapability(cap)) {
           missing = missing + [cap];
       }
   }

   if (len(missing) > 0) {
       print("ERROR: Missing capabilities: " + str(missing));
       throw "Cannot run without required capabilities";
   }

**4. Document Capability Requirements**

Make permission requirements explicit in your code:

.. code-block:: ml

   /**
    * Data Sync Module
    *
    * Required Capabilities:
    *   - file.read:/data/*.json
    *   - file.write:/data/*.json
    *   - network.http:api.example.com
    *
    * Recommended Configuration:
    *   {
    *     "capabilities": [
    *       "file.read:/data/*.json",
    *       "file.write:/data/*.json",
    *       "network.http:api.example.com"
    *     ]
    *   }
    */

   // Validate requirements at startup
   if (!hasCapability("file.read") ||
       !hasCapability("file.write") ||
       !hasCapability("network.http")) {
       throw "Missing required capabilities - see module documentation";
   }

**5. Use Feature Flags**

Control program behavior based on capabilities:

.. code-block:: ml

   // Global feature flags
   FEATURES = {
       canLoadFiles: hasCapability("file.read"),
       canSaveFiles: hasCapability("file.write"),
       canSyncCloud: hasCapability("network.http"),
       hasGuiSupport: hasCapability("gui.create")
   };

   // Use throughout program
   if (FEATURES.canLoadFiles) {
       loadConfigFromFile();
   } else if (FEATURES.canSyncCloud) {
       loadConfigFromCloud();
   } else {
       useDefaultConfig();
   }

Security Considerations
------------------------

**Capability Disclosure is Safe**

Introspection functions reveal what capabilities are available, which might seem like a security concern. However:

1. **Code Already Has Capabilities** - If code is running with capabilities, it can already use them. Knowing about them doesn't add attack surface.

2. **Try-Catch Alternative Exists** - Malicious code can already probe capabilities via exception handling. Introspection is more explicit and auditable.

3. **Transparency Improves Security** - Users can see what permissions their code is running with, making debugging easier and reducing frustration.

4. **No Privilege Escalation** - Knowing about capabilities doesn't grant them. You can only check what you already have.

5. **Self-Documenting Code** - Explicit capability checks make permission requirements clear, improving code review and security audits.

**Introspection vs Try-Catch**

Both approaches can detect capabilities:

.. code-block:: ml

   // Introspection approach (recommended)
   if (hasCapability("file.read")) {
       content = file.read("data.txt");
   }

   // Try-catch approach (works but verbose)
   try {
       content = file.read("data.txt");
   } except (e) {
       // Handle missing capability
   }

Introspection is preferred because it's:

- More explicit and readable
- Avoids exception overhead
- Enables better error messages
- Self-documenting

Capability Patterns Reference
===============================

This section documents all capability patterns for ML standard library modules.

Console Capabilities
---------------------

Control program output and logging.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Capability
     - Description
   * - ``console.write``
     - Log messages to stdout (console.log, console.info, console.debug)
   * - ``console.error``
     - Log error/warning messages to stderr (console.error, console.warn)

**Required For:**

- ``console.log()`` - Print messages
- ``console.info()`` - Info logging
- ``console.debug()`` - Debug logging
- ``console.error()`` - Error messages
- ``console.warn()`` - Warnings

**Security Notes:**

- Console output is generally safe but can leak sensitive information
- In production, consider restricting console capabilities for untrusted code
- Debug logging should be disabled in production

**Examples:**

.. code-block:: ml

   // Grant console capabilities
   // REPL: .grant console.write
   // REPL: .grant console.error

   // Use console functions
   console.log("Application started");
   console.info("Processing data...");
   console.warn("Low memory warning");
   console.error("Failed to load config");

File Capabilities
------------------

Control file system read/write operations.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Capability
     - Description
   * - ``file.read``
     - Read any file on the system
   * - ``file.read:<pattern>``
     - Read files matching glob pattern (e.g., ``file.read:/data/*.json``)
   * - ``file.write``
     - Write to any file
   * - ``file.write:<pattern>``
     - Write files matching pattern (e.g., ``file.write:/tmp/*``)
   * - ``file.delete``
     - Delete any file
   * - ``file.delete:<pattern>``
     - Delete files matching pattern
   * - ``file.append``
     - Append to any file
   * - ``file.append:<pattern>``
     - Append to files matching pattern

**Required For:**

- ``file.read(path)`` - Read file contents
- ``file.readBytes(path)`` - Read binary file
- ``file.readLines(path)`` - Read file as lines
- ``file.write(path, content)`` - Write file
- ``file.writeBytes(path, data)`` - Write binary
- ``file.append(path, content)`` - Append to file
- ``file.delete(path)`` - Delete file
- ``file.copy(src, dest)`` - Copy file (requires read + write)

**No Capability Required:**

- ``file.exists(path)`` - Check if file exists (safe operation)

**Security Notes:**

- Always use path patterns to restrict access
- Be careful with write/delete capabilities
- Path patterns support wildcards: ``*``, ``?``, ``[abc]``
- All paths are canonicalized to prevent directory traversal

**Examples:**

.. code-block:: ml

   // Read configuration files only
   // Capability: file.read:/config/*.json

   config = file.read("/config/app.json");        // ✅ Allowed
   users = file.read("/config/users.json");       // ✅ Allowed
   secrets = file.read("/secrets/api-keys.txt");  // ❌ Blocked

   // Write to output directory only
   // Capability: file.write:/output/*

   file.write("/output/results.txt", data);       // ✅ Allowed
   file.write("/etc/hosts", malicious);           // ❌ Blocked

**Common Patterns:**

.. code-block:: ml

   // Pattern                    Matches
   file.read:/data/*           All files in /data/ (not subdirectories)
   file.read:/data/**          All files in /data/ and subdirectories
   file.read:*.json            All JSON files in current directory
   file.read:**/*.json         All JSON files recursively
   file.write:/tmp/*           Write anywhere in /tmp/
   file.read:/home/user/*      User's home directory

HTTP Capabilities
------------------

Control network HTTP/HTTPS requests.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Capability
     - Description
   * - ``network.http``
     - Make HTTP requests to any server
   * - ``network.https``
     - Make HTTPS requests to any server
   * - ``network.http:<domain>``
     - Requests to specific domain (e.g., ``network.http:api.example.com``)
   * - ``network.http:<pattern>``
     - Requests matching pattern (e.g., ``network.http:*.example.com``)
   * - ``network.http:<url>``
     - Requests to URL pattern (e.g., ``network.http:https://api.example.com/*``)

**Required For:**

- ``http.get(url)`` - GET request
- ``http.post(url, options)`` - POST request
- ``http.put(url, options)`` - PUT request
- ``http.delete(url)`` - DELETE request
- ``http.request(options)`` - Generic request

**Security Notes:**

- Always restrict to specific domains in production
- Use HTTPS for sensitive data
- Timeouts are enforced by default
- Response size limits prevent memory exhaustion
- Dangerous headers are filtered automatically

**Examples:**

.. code-block:: ml

   // Allow only company API
   // Capability: network.http:https://api.company.com/*

   response = http.get("https://api.company.com/users");  // ✅ Allowed
   response = http.get("https://evil.com/malware");       // ❌ Blocked

   // Allow any API subdomain
   // Capability: network.http:*.api.company.com

   http.get("https://users.api.company.com/list");   // ✅ Allowed
   http.get("https://data.api.company.com/query");   // ✅ Allowed
   http.get("https://www.company.com/");             // ❌ Blocked

**Common Patterns:**

.. code-block:: ml

   // Pattern                                    Matches
   network.http:api.example.com              api.example.com only
   network.http:*.example.com                All subdomains of example.com
   network.http:https://api.example.com/*    All HTTPS paths on api.example.com
   network.https:*                           Any HTTPS request
   network.http:localhost:8080               Local development server

Path Capabilities
------------------

Control filesystem metadata operations (directories, file info).

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Capability
     - Description
   * - ``path.read``
     - List directories and read metadata
   * - ``path.read:<pattern>``
     - Read directory structure matching pattern
   * - ``path.write``
     - Create/remove directories
   * - ``path.write:<pattern>``
     - Modify directories matching pattern

**Required For:**

- ``path.listDir(dirPath)`` - List directory contents
- ``path.readDir(dirPath)`` - Read directory with metadata
- ``path.isFile(path)`` - Check if path is file
- ``path.isDir(path)`` - Check if path is directory
- ``path.stat(path)`` - Get file metadata
- ``path.createDir(path)`` - Create directory
- ``path.removeDir(path)`` - Remove directory

**No Capability Required:**

- ``path.join(...)`` - Join path components (pure function)
- ``path.dirname(path)`` - Get directory name
- ``path.basename(path)`` - Get filename
- ``path.extname(path)`` - Get file extension
- ``path.resolve(path)`` - Resolve absolute path

**Security Notes:**

- Path capabilities are separate from file capabilities for granularity
- Metadata operations require ``path.read``
- Directory modification requires ``path.write``
- Path patterns work the same as file patterns

**Examples:**

.. code-block:: ml

   // List data directory structure
   // Capability: path.read:/data/*

   files = path.listDir("/data");               // ✅ Allowed
   info = path.stat("/data/users.json");       // ✅ Allowed
   home = path.listDir("/home/user");          // ❌ Blocked

   // Create output directories
   // Capability: path.write:/output/*

   path.createDir("/output/reports");           // ✅ Allowed
   path.createDir("/system/critical");          // ❌ Blocked

Standard Library Capabilities
-------------------------------

Most standard library modules require **no capabilities** as they perform safe operations:

**No Capabilities Required:**

- **builtin** - Core language functions (len, range, typeof, etc.)
- **math** - Mathematical operations (sqrt, sin, cos, etc.)
- **string** - String manipulation (upper, lower, split, etc.)
- **regex** - Pattern matching (match, test, replace, etc.)
- **datetime** - Date/time operations (now, format, parse, etc.)
- **json** - JSON parsing/serialization (parse, stringify)
- **collections** - Data structures (Map, Set, etc.)
- **functional** - Functional programming (map, filter, reduce, etc.)
- **random** - Random number generation

**Capabilities Required:**

- **console** - Requires ``console.write`` or ``console.error``
- **file** - Requires ``file.read``, ``file.write``, etc.
- **http** - Requires ``network.http`` or ``network.https``
- **path** - Requires ``path.read`` or ``path.write``

Granting Capabilities
======================

There are three ways to grant capabilities to ML programs:

1. **REPL Commands** - Interactive capability management
2. **Project Configuration** - File-based capability grants
3. **Command-Line Flags** - One-time capability grants

REPL Capability Commands
--------------------------

The REPL provides commands for interactive capability management.

View Granted Capabilities
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: ml

   ml[secure]> .capabilities

   Granted Capabilities:
     ✓ console.write
     ✓ file.read:/data/*.json

   No capabilities granted - program runs in secure mode.

Grant a Capability
^^^^^^^^^^^^^^^^^^

.. code-block:: ml

   ml[secure]> .grant console.write

   ⚠️  Capability Grant Request

   Capability: console.write
   Risk Level: LOW
   Description: Allow writing to console/stdout

   This will allow the program to:
     • Print messages with console.log()
     • Output information to stdout

   Grant this capability? [y/N]: y

   ✓ Granted capability: console.write

**With Resource Pattern:**

.. code-block:: ml

   ml[secure]> .grant file.read:/data/*.json

   ⚠️  Capability Grant Request

   Capability: file.read:/data/*.json
   Risk Level: MEDIUM
   Resource Pattern: /data/*.json

   This will allow the program to:
     • Read files matching pattern /data/*.json
     • Access: /data/config.json ✓
     • Blocked: /data/secrets.txt ✓
     • Blocked: /etc/passwd ✓

   Grant this capability? [y/N]: y

   ✓ Granted capability: file.read:/data/*.json

Revoke a Capability
^^^^^^^^^^^^^^^^^^^

.. code-block:: ml

   ml[secure]> .revoke file.read

   ✓ Revoked capability: file.read

   // Now file operations will fail
   ml[secure]> file.read("/data/config.json");
   ❌ Error: Missing required capability 'file.read'

**REPL Capability Workflow:**

.. code-block:: ml

   // 1. Start REPL - no capabilities
   ml[secure]> import file;
   ml[secure]> file.read("data.txt");
   ❌ Error: Missing capability 'file.read'

   // 2. Grant capability
   ml[secure]> .grant file.read
   ✓ Granted capability: file.read

   // 3. Operation succeeds
   ml[secure]> file.read("data.txt");
   => "file contents..."

   // 4. Revoke when done
   ml[secure]> .revoke file.read
   ✓ Revoked capability: file.read

Project Configuration
----------------------

For file-based programs, define capabilities in ``mlpy.json`` or ``mlpy.yaml``.

Basic Configuration (mlpy.json)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: json

   {
     "capabilities": [
       "console.write",
       "file.read:/data/**",
       "file.write:/output/**",
       "network.http:api.example.com"
     ]
   }

YAML Configuration (mlpy.yaml)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

   capabilities:
     - console.write
     - console.error
     - file.read:/data/**
     - file.write:/output/**
     - network.http:https://api.example.com/*

Advanced Configuration
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: json

   {
     "capabilities": [
       "console.write",
       "file.read:/data/**"
     ],
     "sandbox": {
       "enabled": true,
       "memory_limit": "200MB",
       "cpu_timeout": 60,
       "max_file_size": "10MB"
     },
     "security": {
       "strict_mode": true,
       "block_dangerous_imports": true,
       "allow_eval": false
     }
   }

**Configuration Locations:**

The transpiler searches for configuration in this order:

1. ``mlpy.json`` in current directory
2. ``mlpy.yaml`` in current directory
3. ``.mlpy/config.json`` in home directory
4. Default: No capabilities (secure mode)

**Running with Configuration:**

.. code-block:: bash

   # Uses mlpy.json in current directory
   mlpy run program.ml

   # Specify custom config file
   mlpy run program.ml --config my-config.json

   # Override config with command line
   mlpy run program.ml --grant console.write --grant file.read:/data/*

Command-Line Flags
-------------------

Grant capabilities directly from the command line:

.. code-block:: bash

   # Single capability
   mlpy run program.ml --grant console.write

   # Multiple capabilities
   mlpy run program.ml \
     --grant console.write \
     --grant file.read:/data/* \
     --grant network.http:api.example.com

   # Resource patterns
   mlpy run program.ml --grant "file.read:/data/**/*.json"

**Command-Line vs Configuration:**

- **Command-line flags** override configuration file
- Use for one-time executions or testing
- Useful for CI/CD pipelines
- Configuration files better for persistent settings

Writing Secure Programs
========================

Best Practices
---------------

**1. Principle of Least Privilege**

Request only the capabilities you actually need:

❌ **Too Broad:**

.. code-block:: json

   {
     "capabilities": [
       "file.read",          // Can read ANY file
       "file.write",         // Can write ANY file
       "network.http"        // Can contact ANY server
     ]
   }

✅ **Correctly Scoped:**

.. code-block:: json

   {
     "capabilities": [
       "file.read:/data/*.json",           // Only JSON files in /data/
       "file.write:/output/reports/*",     // Only output reports
       "network.http:api.company.com"      // Only company API
     ]
   }

**2. Separate Capabilities by Function**

Organize code to minimize capability scope:

.. code-block:: ml

   // File: data_loader.ml
   // Capabilities: file.read:/data/*
   import file;

   function loadData() {
       return file.read("/data/config.json");
   }

.. code-block:: ml

   // File: data_processor.ml
   // Capabilities: none (pure computation)

   function processData(data) {
       // No file access needed
       return data.filter(item => item.active);
   }

.. code-block:: ml

   // File: data_saver.ml
   // Capabilities: file.write:/output/*
   import file;

   function saveResults(results) {
       file.write("/output/results.json", json.stringify(results));
   }

**3. Validate External Input**

Never trust data from files or HTTP requests:

.. code-block:: ml

   import file;
   import json;

   // ❌ Dangerous: No validation
   config = json.parse(file.read("config.json"));
   file.delete(config.fileToDelete);  // Could delete anything!

   // ✅ Safe: Validate and constrain
   configText = file.read("config.json");
   config = json.parse(configText);

   // Validate structure
   if (typeof(config.fileToDelete) != "string") {
       throw "Invalid config";
   }

   // Validate path is in safe directory
   if (!config.fileToDelete.startsWith("/tmp/")) {
       throw "Can only delete files in /tmp/";
   }

   file.delete(config.fileToDelete);  // Now safe

**4. Use Path Patterns Defensively**

Always constrain file/network capabilities:

.. code-block:: ml

   // ✅ Good patterns
   file.read:/data/config/*.json      // Only config JSONs
   file.write:/output/reports/*       // Only in reports dir
   network.http:api.example.com       // Only company API
   network.http:*.amazonaws.com       // Only AWS services

   // ❌ Avoid broad patterns
   file.read:*                         // Everything!
   file.write:/*                       // System files!
   network.http:*                      // Entire internet!

**5. Document Required Capabilities**

Make capability requirements clear:

.. code-block:: ml

   /**
    * Data Export Module
    *
    * Required Capabilities:
    *   - file.read:/data/exports/*.json
    *   - file.write:/output/exports/*.json
    *   - network.http:https://api.example.com/*
    *
    * Configuration:
    *   mlpy run export.ml \
    *     --grant file.read:/data/exports/*.json \
    *     --grant file.write:/output/exports/*.json \
    *     --grant network.http:https://api.example.com/*
    */

   import file;
   import http;
   import json;

   // ... implementation

Common Patterns
----------------

**Pattern 1: Configuration Loading**

.. code-block:: ml

   // Capability: file.read:/config/*.json
   import file;
   import json;

   function loadConfig(env) {
       configFile = "/config/" + env + ".json";
       return json.parse(file.read(configFile));
   }

   config = loadConfig("production");

**Pattern 2: API Client**

.. code-block:: ml

   // Capability: network.http:api.example.com
   import http;
   import json;

   function apiRequest(endpoint, data) {
       response = http.post("https://api.example.com/" + endpoint, {
           body: json.stringify(data),
           headers: {"Content-Type": "application/json"}
       });

       if (!response.ok()) {
           throw "API error: " + str(response.status());
       }

       return response.json();
   }

   result = apiRequest("users", {name: "Alice"});

**Pattern 3: Report Generation**

.. code-block:: ml

   // Capabilities:
   //   - file.read:/data/**/*.csv
   //   - file.write:/output/reports/*
   //   - console.write

   import file;
   import path;
   import console;

   function generateReport(dataDir, outputFile) {
       console.log("Scanning " + dataDir + "...");

       // Read all CSV files
       files = path.listDir(dataDir)
           .filter(f => f.endsWith(".csv"));

       console.log("Found " + str(len(files)) + " files");

       // Process data
       allData = files.map(f => file.read(path.join(dataDir, f)));
       report = processData(allData);

       // Write report
       file.write(outputFile, report);
       console.log("Report saved to " + outputFile);
   }

   generateReport("/data/exports", "/output/reports/summary.txt");

**Pattern 4: Temporary Elevated Privileges**

Use narrowly-scoped scripts for privileged operations:

.. code-block:: ml

   // File: cleanup.ml
   // Capability: file.delete:/tmp/ml-*
   // Purpose: Clean up temporary files only

   import file;
   import path;

   function cleanupTempFiles() {
       tempDir = "/tmp";
       files = path.listDir(tempDir);

       deleted = 0;
       for (f in files) {
           if (f.startsWith("ml-")) {
               file.delete(path.join(tempDir, f));
               deleted = deleted + 1;
           }
       }

       return deleted;
   }

   count = cleanupTempFiles();
   console.log("Deleted " + str(count) + " temp files");

Run with:

.. code-block:: bash

   mlpy run cleanup.ml --grant file.delete:/tmp/ml-* --grant console.write

Security Considerations
------------------------

**1. Never Disable Security Features**

❌ **Don't Do This:**

.. code-block:: json

   {
     "security": {
       "strict_mode": false,           // ❌ Disables security checks
       "allow_eval": true,              // ❌ Enables dangerous eval()
       "block_dangerous_imports": false // ❌ Allows __import__
     }
   }

✅ **Keep Security Enabled:**

.. code-block:: json

   {
     "security": {
       "strict_mode": true,
       "allow_eval": false,
       "block_dangerous_imports": true
     }
   }

**2. Capability Creep**

Resist the temptation to keep adding capabilities:

.. code-block:: json

   // ❌ Capability creep over time
   {
     "capabilities": [
       "console.write",
       "file.read",         // Added for config
       "file.write",        // Added for logs
       "file.delete",       // Added for cleanup
       "network.http",      // Added for API
       "path.write"         // Added for dirs
     ]
   }

   // ✅ Minimal capabilities with patterns
   {
     "capabilities": [
       "console.write",
       "file.read:/config/*.json",
       "file.write:/logs/*.log",
       "network.http:api.example.com"
     ]
   }

**3. Production vs Development**

Use different capability profiles:

.. code-block:: json

   // development.json - More permissive for debugging
   {
     "capabilities": [
       "console.write",
       "console.error",
       "file.read:/data/**",
       "file.write:/output/**"
     ]
   }

.. code-block:: json

   // production.json - Minimal capabilities
   {
     "capabilities": [
       "file.read:/data/config.json",
       "network.http:api.company.com"
     ],
     "sandbox": {
       "enabled": true,
       "memory_limit": "200MB",
       "cpu_timeout": 30
     }
   }

Run with appropriate config:

.. code-block:: bash

   # Development
   mlpy run app.ml --config development.json

   # Production
   mlpy run app.ml --config production.json

Troubleshooting
===============

Common Capability Errors
-------------------------

**Error: Missing required capability**

.. code-block:: text

   ❌ Error: Missing required capability 'console.write'

   Function: console.log()
   Location: program.ml:5:4

   To fix, grant the capability:
     • REPL: .grant console.write
     • Config: Add "console.write" to capabilities list
     • CLI: mlpy run program.ml --grant console.write

**Solution:**

.. code-block:: ml

   // In REPL
   ml[secure]> .grant console.write

   // Or in mlpy.json
   {
     "capabilities": ["console.write"]
   }

   // Or command line
   mlpy run program.ml --grant console.write

**Error: Capability pattern doesn't match resource**

.. code-block:: text

   ❌ Error: Capability pattern mismatch

   Attempted: file.read("/home/user/data.txt")
   Granted: file.read:/data/*.txt

   The path "/home/user/data.txt" does not match pattern "/data/*.txt"

**Solution:**

Either adjust the pattern or move the file:

.. code-block:: ml

   // Option 1: Grant broader pattern
   .grant file.read:/home/user/*.txt

   // Option 2: Move file to match existing pattern
   // cp /home/user/data.txt /data/data.txt
   file.read("/data/data.txt");  // Now matches /data/*.txt

**Error: Invalid capability syntax**

.. code-block:: text

   ❌ Error: Invalid capability syntax: 'file:read'

   Expected format: 'type.operation' or 'type.operation:pattern'

   Examples:
     • file.read
     • file.read:/data/*
     • network.http:api.example.com

**Solution:**

Use correct capability syntax:

.. code-block:: ml

   // ❌ Wrong
   .grant file:read
   .grant network-http

   // ✅ Correct
   .grant file.read
   .grant network.http

Debugging Capability Issues
----------------------------

**1. Check Granted Capabilities**

.. code-block:: ml

   ml[secure]> .capabilities

   Granted Capabilities:
     ✓ console.write
     ✓ file.read:/data/*.json

**2. Verify Resource Patterns**

.. code-block:: ml

   ml[secure]> .grant file.read:/data/*.json

   // Test different paths
   ml[secure]> file.read("/data/config.json");   // ✅ Match
   ml[secure]> file.read("/data/users.json");    // ✅ Match
   ml[secure]> file.read("/config/app.json");    // ❌ No match

**3. Check Configuration Files**

.. code-block:: bash

   # Display current configuration
   mlpy config show

   # Validate configuration syntax
   mlpy config validate mlpy.json

   # Show effective capabilities for a file
   mlpy run program.ml --dry-run --show-capabilities

**4. Enable Debug Logging**

.. code-block:: bash

   # Run with debug output
   mlpy run program.ml --debug --log-level DEBUG

   # Shows:
   # - Which capabilities are checked
   # - Which patterns are matched
   # - Why operations succeed or fail

Getting Help
-------------

**REPL Help:**

.. code-block:: ml

   ml[secure]> .help

   // Shows all REPL commands including capability commands

**Capability System Documentation:**

- This guide: ``docs/user-guide/toolkit/capabilities.rst``
- REPL guide: ``docs/user-guide/toolkit/repl-guide.rst``
- Standard library docs: See individual module documentation

**Command-Line Help:**

.. code-block:: bash

   mlpy run --help          # Execution options
   mlpy config --help       # Configuration help
   mlpy capabilities --help # Capability management

**Security Questions:**

If you're unsure about capability requirements:

1. Start with **zero capabilities** and add as needed
2. Use the **REPL** to experiment interactively
3. Check the **error messages** - they suggest required capabilities
4. Review **standard library docs** for each module's capability requirements

Summary
========

Key Takeaways
--------------

1. **Capabilities are permission tokens** that grant access to system resources
2. **Default deny** - programs start with zero permissions
3. **Fine-grained control** - restrict capabilities with resource patterns
4. **Three ways to grant** - REPL commands, configuration files, command-line flags
5. **Principle of least privilege** - request only what you need
6. **Use path patterns** - constrain file and network access
7. **Security is mandatory** - cannot be disabled without explicit configuration

Capability Quick Reference
---------------------------

.. code-block:: ml

   // Console
   console.write            // console.log(), .info(), .debug()
   console.error            // console.error(), .warn()

   // File System
   file.read                // Read any file
   file.read:<pattern>      // Read matching files
   file.write               // Write any file
   file.write:<pattern>     // Write matching files
   file.delete              // Delete any file
   file.append              // Append to any file

   // Network
   network.http             // HTTP requests
   network.https            // HTTPS requests
   network.http:<domain>    // Specific domain
   network.http:<pattern>   // Domain pattern

   // Path Operations
   path.read                // List directories
   path.read:<pattern>      // List matching paths
   path.write               // Create/remove directories
   path.write:<pattern>     // Modify matching paths

REPL Command Quick Reference
------------------------------

.. code-block:: ml

   .capabilities            # Show granted capabilities
   .grant <capability>      # Grant a capability
   .revoke <capability>     # Revoke a capability
   .help                    # Show all commands

Next Steps
-----------

Now that you understand capabilities:

1. **Practice in the REPL** - Experiment with granting/revoking capabilities
2. **Write secure programs** - Apply the best practices from this guide
3. **Review standard library docs** - Understand each module's capability requirements
4. **Read the REPL Guide** - Learn more about interactive development: :doc:`repl-guide`
5. **Study the Transpilation Guide** - Understand deployment and configuration: :doc:`transpilation`

**Example Projects:**

See ``docs/examples/`` for complete programs demonstrating capability patterns:

- ``data-processing/`` - File I/O with path patterns
- ``api-client/`` - HTTP capabilities with domain restrictions
- ``configuration/`` - Safe configuration loading
- ``reporting/`` - Multi-capability program with least privilege

**Additional Resources:**

- Tutorial: :doc:`../tutorial/index`
- Language Reference: :doc:`../language-reference/index`
- Standard Library: :doc:`../../standard-library/index`
