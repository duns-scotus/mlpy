====================================
Transpilation, Execution & Deployment
====================================

ML programs are transpiled to Python before execution. Understanding this process helps you run programs efficiently, debug issues, and deploy to production.

.. contents::
   :local:
   :depth: 3

Introduction
============

How ML Code Runs
----------------

ML programs go through a multi-stage pipeline before execution:

1. **Parse** - ML source code is parsed into an Abstract Syntax Tree (AST)
2. **Analyze** - Security analysis detects potential threats
3. **Transpile** - AST is converted to equivalent Python code
4. **Execute** - Python code runs in a controlled environment

This design provides:

- **Security** - Static analysis catches issues before execution
- **Performance** - Python's JIT compilation and optimizations
- **Interoperability** - ML code can call Python libraries
- **Debugging** - Source maps connect ML code to Python code

Why Transpile to Python?
-------------------------

**Advantages:**

- **Leverage Python ecosystem** - Access to millions of Python packages
- **Mature runtime** - Python's VM is highly optimized
- **Familiar debugging** - Use Python debugging tools
- **Easy deployment** - Deploy to any Python environment
- **Performance** - Python's JIT and native extensions

**Trade-offs:**

- **Compilation overhead** - Transpilation adds startup time (~100ms typical)
- **Python dependency** - Requires Python 3.12+ runtime
- **Debugging indirection** - Need source maps to map errors back to ML

Execution Modes
===============

mlpy provides multiple ways to execute ML code, each suited for different use cases.

Direct Execution
----------------

Run ML programs immediately without creating intermediate files.

**Command:**

.. code-block:: bash

   mlpy run program.ml

**Use Cases:**

- Development and testing
- Running scripts
- Quick validation
- Prototyping

**Example:**

.. code-block:: bash

   # Create a simple ML program
   $ cat hello.ml
   import console;
   console.log("Hello, ML!");

   # Run it directly
   $ mlpy run hello.ml
   Hello, ML!

**Performance:**

- Parse + Security + Transpile + Execute: ~150ms for typical programs
- Results cached for subsequent runs
- No intermediate files created

Compilation
-----------

Transpile ML code to Python files for deployment or inspection.

**Command:**

.. code-block:: bash

   mlpy transpile program.ml -o output.py

**Use Cases:**

- Production deployment
- Inspecting generated Python code
- Integration with Python projects
- Performance optimization

**Example:**

.. code-block:: bash

   # Transpile ML to Python
   $ mlpy transpile geometry.ml -o geometry.py

   # Inspect generated code
   $ cat geometry.py
   # (Python code with ML runtime wrappers)

   # Run compiled Python
   $ python geometry.py

**Output Options:**

.. code-block:: bash

   # Specify output file
   mlpy transpile input.ml -o output.py

   # Generate source maps (for debugging)
   mlpy transpile input.ml -o output.py --sourcemap

   # Strict security mode (fail on any security issues)
   mlpy transpile input.ml -o output.py --strict

REPL Mode
---------

Interactive execution with immediate feedback (covered in :doc:`repl-guide`).

**Command:**

.. code-block:: bash

   mlpy repl

**Use Cases:**

- Learning ML syntax
- Testing code snippets
- Exploring modules
- Rapid prototyping

**Performance:**

- Incremental transpilation: ~7ms per statement (v2.3)
- No file I/O overhead
- Variables persist across commands

Import Mode
-----------

Use ML modules from Python code.

**From Python:**

.. code-block:: python

   from mlpy import transpile_and_import

   # Import ML module
   mymodule = transpile_and_import("mymodule.ml")

   # Call ML functions from Python
   result = mymodule.my_function(42)

**Use Cases:**

- Embedding ML in Python applications
- Gradual migration from Python to ML
- Reusing ML code in Python projects

Transpilation Process
=====================

Understanding the Pipeline
--------------------------

The transpilation pipeline has four main stages:

**Stage 1: Parsing**

ML source code is parsed into an Abstract Syntax Tree (AST):

.. code-block:: ml

   x = 10 + 20;

Becomes:

.. code-block:: text

   Program
     ├─ VariableDeclaration
     │   ├─ Identifier: "x"
     │   └─ BinaryExpression
     │       ├─ Number: 10
     │       ├─ Operator: "+"
     │       └─ Number: 20

**Stage 2: Security Analysis**

The AST is analyzed for security threats:

- Pattern matching for dangerous operations
- Data flow tracking for taint propagation
- Capability requirement detection
- Resource usage validation

**Stage 3: Code Generation**

The AST is converted to equivalent Python code:

.. code-block:: ml

   x = 10 + 20;

Generates:

.. code-block:: python

   x = (10 + 20)

**Stage 4: Runtime Wrapping**

Security wrappers are added for capability-restricted operations:

.. code-block:: ml

   import console;
   console.log("Hello!");

Generates:

.. code-block:: python

   import sys
   from mlpy.stdlib import console_bridge as console

   # Capability check occurs at import time
   console.log("Hello!")

Source Maps
-----------

Source maps connect generated Python code back to original ML code for debugging.

**Enabling Source Maps:**

.. code-block:: bash

   mlpy transpile program.ml -o program.py --sourcemap

**Generated Files:**

.. code-block:: text

   program.py          # Generated Python code
   program.py.map      # Source map file

**Usage in Debugging:**

When an error occurs in Python code, source maps allow debuggers to show the corresponding ML source location:

.. code-block:: text

   Error at program.py:42
   → Maps to program.ml:15

**Source Map Format:**

Source maps use the standard JSON format compatible with debugging tools:

.. code-block:: json

   {
     "version": 3,
     "sources": ["program.ml"],
     "mappings": "...",
     "names": [...]
   }

Running ML Programs
===================

Basic Execution
---------------

Run ML programs with default security settings:

.. code-block:: bash

   mlpy run program.ml

**Default Behavior:**

- Sandbox execution enabled
- Memory limit: 100MB
- CPU timeout: 30 seconds
- Network access: disabled
- File access: current directory only

Example Program
---------------

Create a simple ML program:

.. code-block:: ml

   // calculate.ml
   import console;
   import math;

   function calculateCircle(radius) {
       area = math.pi * radius * radius;
       circumference = 2 * math.pi * radius;

       console.log("Radius: " + str(radius));
       console.log("Area: " + str(area));
       console.log("Circumference: " + str(circumference));
   }

   calculateCircle(5);

Run it:

.. code-block:: bash

   $ mlpy run calculate.ml
   Radius: 5
   Area: 78.53981633974483
   Circumference: 31.41592653589793

Configuration Options
---------------------

Sandbox Configuration
~~~~~~~~~~~~~~~~~~~~~

Control resource limits and security settings:

.. code-block:: bash

   # Increase memory limit
   mlpy run program.ml --memory-limit 500MB

   # Increase CPU timeout
   mlpy run program.ml --cpu-timeout 60

   # Disable network (default)
   mlpy run program.ml --disable-network

**Memory Limits:**

.. code-block:: bash

   mlpy run program.ml --memory-limit 100MB   # 100 megabytes
   mlpy run program.ml --memory-limit 1GB     # 1 gigabyte
   mlpy run program.ml --memory-limit 50KB    # 50 kilobytes

**CPU Timeouts:**

.. code-block:: bash

   mlpy run program.ml --cpu-timeout 10      # 10 seconds
   mlpy run program.ml --cpu-timeout 120     # 2 minutes
   mlpy run program.ml --cpu-timeout 0.5     # 500 milliseconds

File Access Patterns
~~~~~~~~~~~~~~~~~~~~

Control which files programs can access:

.. code-block:: bash

   # Allow access to specific directory
   mlpy run program.ml --file-patterns "/data/**"

   # Allow multiple patterns
   mlpy run program.ml --file-patterns "/data/**" --file-patterns "/config/**"

   # Allow specific files
   mlpy run program.ml --file-patterns "/data/input.txt"

**Pattern Syntax:**

- ``**`` - Matches any subdirectories
- ``*`` - Matches any characters in filename
- ``?`` - Matches single character
- ``[abc]`` - Matches a, b, or c

**Examples:**

.. code-block:: bash

   # All .txt files in /data
   --file-patterns "/data/**/*.txt"

   # Specific configuration files
   --file-patterns "/config/{app,db}.json"

   # All files in current directory
   --file-patterns "./**"

Network Access
~~~~~~~~~~~~~~

Enable and restrict network access:

.. code-block:: bash

   # Enable network for specific hosts
   mlpy run program.ml --allow-hosts "api.example.com"

   # Multiple hosts
   mlpy run program.ml --allow-hosts "api.example.com" --allow-hosts "cdn.example.com"

   # Specific ports
   mlpy run program.ml --allow-ports 80 --allow-ports 443

**Example - API Client:**

.. code-block:: bash

   mlpy run api_client.ml \
     --allow-hosts "api.github.com" \
     --allow-ports 443

Import Configuration
~~~~~~~~~~~~~~~~~~~~

Configure module import behavior:

.. code-block:: bash

   # Add custom import paths
   mlpy run program.ml --import-paths "/path/to/modules"

   # Multiple paths (colon-separated)
   mlpy run program.ml --import-paths "/path1:/path2:/path3"

   # Allow imports from current directory (default)
   mlpy run program.ml --allow-current-dir

   # Disable current directory imports
   mlpy run program.ml --no-allow-current-dir

**Standard Library Mode:**

.. code-block:: bash

   # Use native ML standard library (default)
   mlpy run program.ml --stdlib-mode native

   # Use Python whitelisting mode (advanced)
   mlpy run program.ml --stdlib-mode python

**Allow Additional Python Modules:**

.. code-block:: bash

   # Allow specific Python modules
   mlpy run program.ml --allow-python-modules "requests,numpy"

Project Configuration
=====================

Using mlpy.json
---------------

Configure project settings in ``mlpy.json`` to avoid repetitive command-line flags.

**Creating Configuration:**

.. code-block:: bash

   # Initialize new project with config
   mlpy --init my-project

**Configuration File:**

``mlpy.json``:

.. code-block:: json

   {
     "name": "my-ml-project",
     "version": "1.0.0",
     "capabilities": [
       "console.write",
       "file.read:/data/**",
       "http.request:https://api.example.com/**"
     ],
     "sandbox": {
       "memory_limit": "200MB",
       "cpu_timeout": 60,
       "network_enabled": true,
       "allowed_hosts": ["api.example.com"],
       "allowed_ports": [80, 443]
     },
     "imports": {
       "paths": ["/lib/ml_modules"],
       "allow_current_dir": true
     }
   }

**Using Configuration:**

When ``mlpy.json`` exists in the current directory, settings are automatically applied:

.. code-block:: bash

   # Uses settings from mlpy.json
   mlpy run program.ml

Configuration Sections
----------------------

**Capabilities:**

.. code-block:: json

   "capabilities": [
     "console.write",
     "console.error",
     "file.read:/data/**",
     "file.write:/output/**",
     "http.request:https://api.example.com/**"
   ]

**Sandbox Settings:**

.. code-block:: json

   "sandbox": {
     "memory_limit": "200MB",
     "cpu_timeout": 60,
     "network_enabled": false,
     "file_patterns": ["/data/**", "/config/**"]
   }

**Import Configuration:**

.. code-block:: json

   "imports": {
     "paths": ["/lib/ml_modules", "./local_modules"],
     "allow_current_dir": true,
     "stdlib_mode": "native"
   }

**Security Settings:**

.. code-block:: json

   "security": {
     "strict_mode": true,
     "audit_enabled": true
   }

Deployment
==========

Deployment Strategies
---------------------

Choose a deployment strategy based on your requirements:

**Strategy 1: Direct Execution**

Deploy ML source files and run with ``mlpy run``:

.. code-block:: bash

   # Copy ML files to server
   scp *.ml server:/app/

   # Run on server
   ssh server "cd /app && mlpy run main.ml"

**Pros:**

- Simple deployment
- Source code visibility
- Easy updates

**Cons:**

- Requires mlpy on server
- Transpilation overhead on startup

**Strategy 2: Pre-Compiled Python**

Transpile to Python locally, deploy Python files:

.. code-block:: bash

   # Transpile locally
   mlpy transpile main.ml -o main.py

   # Deploy Python file
   scp main.py server:/app/

   # Run on server (only Python needed)
   ssh server "cd /app && python main.py"

**Pros:**

- No mlpy dependency on server
- Faster startup (no transpilation)
- Smaller deployment size

**Cons:**

- Less readable (generated code)
- Harder to debug without source maps

**Strategy 3: Containerized Deployment**

Use Docker for consistent environments:

.. code-block:: dockerfile

   # Dockerfile
   FROM python:3.12

   # Install mlpy
   RUN pip install mlpy

   # Copy ML source
   COPY *.ml /app/
   COPY mlpy.json /app/

   WORKDIR /app

   # Run ML program
   CMD ["mlpy", "run", "main.ml"]

Build and deploy:

.. code-block:: bash

   # Build image
   docker build -t my-ml-app .

   # Run container
   docker run --rm my-ml-app

**Strategy 4: Compiled Modules**

Transpile ML modules for import from Python:

.. code-block:: bash

   # Transpile ML module
   mlpy transpile mymodule.ml -o mymodule.py

   # Deploy alongside Python code
   # Import from Python
   import mymodule
   result = mymodule.my_function()

Production Checklist
--------------------

Before deploying to production:

**1. Security Review**

.. code-block:: bash

   # Run comprehensive security audit
   mlpy audit program.ml

   # Check for security issues
   mlpy security-analyze program.ml --deep-analysis

**2. Performance Testing**

.. code-block:: bash

   # Profile execution
   mlpy run program.ml --profile

   # Generate performance report
   mlpy profile-report

**3. Resource Limits**

Ensure appropriate resource limits in ``mlpy.json``:

.. code-block:: json

   "sandbox": {
     "memory_limit": "500MB",
     "cpu_timeout": 120
   }

**4. Capability Minimization**

Grant only required capabilities:

.. code-block:: json

   "capabilities": [
     "console.write",
     "file.read:/data/input/**",
     "file.write:/data/output/**"
   ]

**5. Error Handling**

Ensure proper error handling in ML code:

.. code-block:: ml

   // Use try/except for error recovery
   try {
       result = riskyOperation();
   } except (e) {
       console.error("Operation failed: " + str(e));
       result = null;
   }

**6. Logging**

Enable audit logging:

.. code-block:: json

   "security": {
     "audit_enabled": true
   }

**7. Dependencies**

Document Python version and dependencies:

.. code-block:: text

   requirements.txt:
   mlpy>=2.3.0
   (any additional Python dependencies)

Deployment Examples
-------------------

Example 1: Web Service
~~~~~~~~~~~~~~~~~~~~~~

Deploy an ML-based web service:

**Project Structure:**

.. code-block:: text

   /app
   ├── main.ml              # ML application
   ├── mlpy.json            # Configuration
   ├── requirements.txt     # Python dependencies
   └── Dockerfile           # Container definition

**main.ml:**

.. code-block:: ml

   import console;
   import http;

   function handleRequest(request) {
       console.log("Processing request");
       response = {
           status: 200,
           body: "Hello from ML!"
       };
       return response;
   }

   // Start server (simplified)
   console.log("Server running on port 8080");

**Dockerfile:**

.. code-block:: dockerfile

   FROM python:3.12
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 8080
   CMD ["mlpy", "run", "main.ml"]

**Deploy:**

.. code-block:: bash

   docker build -t ml-service .
   docker run -p 8080:8080 ml-service

Example 2: Data Processing Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Deploy a batch data processing job:

**Structure:**

.. code-block:: text

   /pipeline
   ├── process.ml
   ├── mlpy.json
   └── data/
       ├── input/
       └── output/

**process.ml:**

.. code-block:: ml

   import console;
   import file;
   import path;

   function processFiles() {
       // Read input files
       files = path.listDir("data/input");

       i = 0;
       while (i < len(files)) {
           filename = files[i];
           inputPath = path.join("data/input", filename);
           content = file.read(inputPath);

           // Process content
           processed = processData(content);

           // Write output
           outputPath = path.join("data/output", filename);
           file.write(outputPath, processed);

           console.log("Processed: " + filename);
           i = i + 1;
       }
   }

   processFiles();

**mlpy.json:**

.. code-block:: json

   {
     "capabilities": [
       "console.write",
       "file.read:data/input/**",
       "file.write:data/output/**",
       "path.read:data/input",
       "path.write:data/output"
     ],
     "sandbox": {
       "memory_limit": "1GB",
       "cpu_timeout": 300
     }
   }

**Run:**

.. code-block:: bash

   mlpy run process.ml

Example 3: Scheduled Task
~~~~~~~~~~~~~~~~~~~~~~~~~~

Deploy as a cron job:

**Crontab Entry:**

.. code-block:: text

   # Run every hour
   0 * * * * cd /app && mlpy run task.ml >> /var/log/ml-task.log 2>&1

**task.ml:**

.. code-block:: ml

   import console;
   import datetime;

   function runScheduledTask() {
       now = datetime.now();
       console.log("Task started at: " + now.format("%Y-%m-%d %H:%M:%S"));

       // Perform task
       performWork();

       console.log("Task completed");
   }

   runScheduledTask();

Performance Optimization
========================

Compilation Performance
-----------------------

**Typical Performance:**

- Parse: 20-50ms
- Security Analysis: 5-15ms
- Code Generation: 30-80ms
- **Total:** ~100-150ms for medium programs

**Caching:**

Compilation results are cached automatically:

.. code-block:: bash

   # First run (includes compilation)
   $ time mlpy run program.ml
   real    0m0.180s

   # Second run (uses cache)
   $ time mlpy run program.ml
   real    0m0.012s

**Cache Management:**

.. code-block:: bash

   # Clear all caches
   mlpy cache --clear-cache

   # Show cache statistics
   mlpy cache --stats

Runtime Performance
-------------------

**Optimization Tips:**

1. **Avoid Repeated Transpilation**

Pre-compile for production:

.. code-block:: bash

   mlpy transpile program.ml -o program.py

2. **Use Efficient Data Structures**

.. code-block:: ml

   // Prefer arrays for ordered data
   items = [1, 2, 3, 4, 5];

   // Use objects for key-value pairs
   config = {host: "localhost", port: 8080};

3. **Minimize Capability Checks**

Grant capabilities at program start, not per-operation:

.. code-block:: json

   "capabilities": ["console.write"]

4. **Batch Operations**

.. code-block:: ml

   // Instead of multiple writes
   file.write("output.txt", line1);
   file.write("output.txt", line2);

   // Write once
   content = line1 + "\n" + line2;
   file.write("output.txt", content);

5. **Profile Execution**

.. code-block:: bash

   # Enable profiling
   mlpy run program.ml --profile

   # Generate report
   mlpy profile-report

Memory Management
-----------------

**Memory Limits:**

Set appropriate limits for your workload:

.. code-block:: bash

   # Small programs
   mlpy run program.ml --memory-limit 50MB

   # Data processing
   mlpy run program.ml --memory-limit 500MB

   # Large datasets
   mlpy run program.ml --memory-limit 2GB

**Monitoring:**

.. code-block:: bash

   # Profile memory usage
   mlpy run program.ml --profile

**Best Practices:**

- Process data in batches for large datasets
- Clear large arrays when no longer needed
- Use streaming for file I/O when possible

Debugging
=========

Common Issues
-------------

**Issue: Transpilation Fails**

.. code-block:: text

   Error: Parse Error: Invalid ML syntax

**Solution:** Check ML syntax:

.. code-block:: bash

   # Parse only (no execution)
   mlpy parse program.ml

---

**Issue: Security Analysis Fails**

.. code-block:: text

   Error: Security issue detected

**Solution:** Run security analysis:

.. code-block:: bash

   mlpy audit program.ml
   mlpy security-analyze program.ml

---

**Issue: Runtime Error**

.. code-block:: text

   Error: NameError: name 'x' is not defined

**Solution:** Generate source maps and inspect Python code:

.. code-block:: bash

   mlpy transpile program.ml -o program.py --sourcemap
   python program.py  # See full Python traceback

---

**Issue: Capability Error**

.. code-block:: text

   Error: Missing capability: file.read

**Solution:** Add capability to configuration:

.. code-block:: json

   "capabilities": ["file.read"]

Debugging Tools
---------------

**Parse Tree Inspection:**

.. code-block:: bash

   mlpy parse program.ml

**Security Analysis:**

.. code-block:: bash

   mlpy audit program.ml
   mlpy security-analyze program.ml --deep-analysis

**Generated Python Code:**

.. code-block:: bash

   mlpy transpile program.ml -o program.py
   cat program.py

**Profiling:**

.. code-block:: bash

   mlpy run program.ml --profile
   mlpy profile-report

**Verbose Output:**

.. code-block:: bash

   mlpy --verbose run program.ml

Summary
=======

Key Concepts
------------

**Transpilation Process:**

1. Parse ML to AST
2. Analyze security
3. Generate Python code
4. Execute with runtime wrappers

**Execution Modes:**

- **Direct** - ``mlpy run`` for development
- **Compiled** - ``mlpy transpile`` for deployment
- **REPL** - ``mlpy repl`` for interactive
- **Import** - Use ML from Python

**Configuration:**

- Use ``mlpy.json`` for project settings
- Grant minimal required capabilities
- Set appropriate resource limits

**Deployment:**

- Choose strategy based on requirements
- Pre-compile for production
- Use containers for consistency
- Follow production checklist

Best Practices
--------------

**Development:**

- Use REPL for experimentation
- Use ``mlpy run`` for testing
- Enable source maps for debugging

**Production:**

- Pre-compile with ``mlpy transpile``
- Use ``mlpy.json`` for configuration
- Set resource limits appropriately
- Grant minimal capabilities
- Enable audit logging

**Performance:**

- Cache compilation results
- Batch operations
- Profile execution
- Monitor resource usage

Next Steps
----------

- :doc:`repl-guide` - Interactive development
- :doc:`capabilities` - Understanding security
- :doc:`../../standard-library/index` - Module reference
