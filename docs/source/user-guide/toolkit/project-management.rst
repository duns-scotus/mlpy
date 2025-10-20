====================================
Project Management & User Modules
====================================

This guide covers mlpy project setup, user-defined modules, and code organization for building scalable ML applications.

.. contents::
   :local:
   :depth: 3

Overview
========

mlpy provides comprehensive project management tools for:

- **Project Initialization** - Create structured ML projects with templates
- **User Modules** - Build reusable code libraries with imports
- **Code Organization** - Organize projects with nested module hierarchies
- **Deployment Strategies** - Choose transpilation modes for different use cases

**Why Project Management Matters:**

As your ML programs grow beyond simple scripts, you need:

- Organized code structure (not everything in one file)
- Reusable modules across projects
- Clear separation of concerns
- Flexible deployment options

mlpy's project system provides industry-standard tools for professional development.

Project Initialization
======================

Creating New Projects
----------------------

Use ``mlpy --init`` to create a new project with complete structure:

.. code-block:: bash

   # Create new project
   mlpy --init my-project

   # Result
   my-project/
   ├── mlpy.json              # Project configuration
   ├── README.md              # Project documentation
   ├── .gitignore             # Git ignore rules
   ├── src/                   # Source code directory
   │   └── main.ml            # Main program
   ├── dist/                  # Compiled output
   ├── tests/                 # Test files
   │   └── test_main.ml       # Example test
   ├── docs/                  # Documentation
   ├── examples/              # Example code
   └── .mlpy/                 # mlpy cache and metadata

**Project is created with:**

- Complete directory structure
- Configuration file with sensible defaults
- Example ML program
- Example test file
- README with usage instructions
- .gitignore for version control

Default Project Template
-------------------------

The basic template creates this ``src/main.ml``:

.. code-block:: ml

   // Main ML program
   function main() {
       message = "Hello, ML World!";
       print(message);
   }

   main();

And this ``tests/test_main.ml``:

.. code-block:: ml

   // Test file example
   import { assert } from "std/testing";

   function test_basic() {
       result = 2 + 2;
       assert.equal(result, 4, "Basic arithmetic should work");
   }

   test_basic();
   print("All tests passed!");

Running Your Project
--------------------

Once created, use these commands:

.. code-block:: bash

   cd my-project

   # Run main program
   mlpy run src/main.ml

   # Compile to Python
   mlpy compile src/main.ml

   # Run tests
   mlpy run tests/test_main.ml

Project Configuration
======================

Configuration Files
-------------------

mlpy projects use ``mlpy.json`` or ``mlpy.yaml`` for configuration.

**Basic mlpy.json:**

.. code-block:: json

   {
     "name": "my-project",
     "version": "1.0.0",
     "description": "ML project: my-project",
     "author": "",
     "license": "MIT",

     "source_dir": "src",
     "output_dir": "dist",
     "test_dir": "tests",

     "target": "python",
     "optimization_level": 1,
     "source_maps": true,

     "enable_security_analysis": true,
     "security_level": "strict",
     "allowed_capabilities": [
       "file_read",
       "file_write",
       "network"
     ]
   }

**YAML Format (mlpy.yaml):**

.. code-block:: yaml

   name: my-project
   version: 1.0.0
   description: ML project with user modules

   source_dir: src
   output_dir: dist
   test_dir: tests

   # Compilation
   target: python
   optimization_level: 1
   source_maps: true

   # Security
   enable_security_analysis: true
   security_level: strict
   allowed_capabilities:
     - console.write
     - file.read:/data/**
     - file.write:/output/**

Configuration Sections
-----------------------

**Project Metadata:**

.. code-block:: json

   {
     "name": "my-project",
     "version": "1.0.0",
     "description": "Project description",
     "author": "Your Name",
     "license": "MIT"
   }

**Directory Structure:**

.. code-block:: json

   {
     "source_dir": "src",
     "output_dir": "dist",
     "test_dir": "tests",
     "doc_source": "docs/source",
     "doc_output": "docs/build"
   }

**Compilation Settings:**

.. code-block:: json

   {
     "target": "python",
     "optimization_level": 1,
     "source_maps": true
   }

- ``target``: Transpilation target (currently "python")
- ``optimization_level``: 0-3 (higher = more optimizations)
- ``source_maps``: Generate source maps for debugging

**Security Settings:**

.. code-block:: json

   {
     "enable_security_analysis": true,
     "security_level": "strict",
     "allowed_capabilities": [
       "console.write",
       "file.read:/data/**"
     ]
   }

- ``security_level``: "strict", "normal", or "permissive"
- ``allowed_capabilities``: List of capability patterns

**Extension Module Paths:**

.. code-block:: json

   {
     "python_extension_paths": [
       "./extensions",
       "./custom_modules",
       "/usr/local/ml_extensions"
     ],
     "ml_module_paths": [
       "./ml_modules",
       "./lib/ml_src",
       "../shared_ml_modules"
     ]
   }

**Python Extension Paths:**

Configure directories containing custom Python extension modules:

- Paths searched for `*_bridge.py` modules that extend ML functionality
- Python modules that provide additional builtin functionality
- Relative paths resolved from project root
- Loaded modules available for import in all ML programs

**ML Module Paths:**

Configure directories containing ML source modules:

- Paths searched for `*.ml` modules that can be imported
- ML modules written in the ML language itself
- Supports nested directory structures (e.g., ``algorithms/sorting.ml``)
- Automatically transpiled and cached for performance
- Precedence: Python bridges win over ML modules if same name

**Priority System:**

Both types of module paths can be configured three ways (highest to lowest priority):

1. **CLI flags** - Per-command override

   - ``-E`` / ``--extension-path`` for Python extensions
   - ``-M`` / ``--ml-module-path`` for ML modules

2. **Project configuration** (``mlpy.json`` / ``mlpy.yaml``) - Project defaults
3. **Environment variables** - System-wide fallback

   - ``MLPY_EXTENSION_PATHS`` for Python extensions
   - ``MLPY_ML_MODULE_PATHS`` for ML modules

**Example with CLI override:**

.. code-block:: bash

   # Project has paths in mlpy.json
   # Override with CLI flags for testing
   mlpy run src/main.ml -E /tmp/test_extensions -M /tmp/test_ml_modules

   # REPL with module paths
   mlpy repl -M ./ml_modules -E ./extensions

**Environment variable format:**

.. code-block:: bash

   # Unix/macOS (colon-separated)
   export MLPY_EXTENSION_PATHS=/ext1:/ext2:/ext3
   export MLPY_ML_MODULE_PATHS=/ml1:/ml2:/ml3
   mlpy run src/main.ml

   # Windows (semicolon-separated)
   set MLPY_EXTENSION_PATHS=C:\ext1;C:\ext2;C:\ext3
   set MLPY_ML_MODULE_PATHS=C:\ml1;C:\ml2;C:\ml3
   mlpy run src/main.ml

**Development Settings:**

.. code-block:: json

   {
     "watch_patterns": ["**/*.ml", "**/*.py"],
     "auto_format": true,
     "lint_on_save": true
   }

**Testing Settings:**

.. code-block:: json

   {
     "test_pattern": "**/test_*.ml",
     "test_timeout": 30,
     "coverage_threshold": 0.8
   }

User-Defined Modules
=====================

What Are User Modules?
-----------------------

User modules are reusable ML code files that you can import into your programs. They enable:

- **Code Reuse** - Write once, use everywhere
- **Organization** - Break large programs into manageable pieces
- **Collaboration** - Share modules across team projects
- **Maintainability** - Update modules independently

**Before User Modules:**

.. code-block:: ml

   // Everything in one file - 500+ lines
   function quicksort(arr) {
       /* 50 lines of sorting logic */
   }

   function merge_sort(arr) {
       /* 40 lines of merge logic */
   }

   function bubble_sort(arr) {
       /* 30 lines of bubble sort */
   }

   // Main program
   data = [5, 2, 8, 1, 9];
   sorted = quicksort(data);

**With User Modules:**

.. code-block:: ml

   // Clean, organized main.ml
   import user_modules.sorting;

   data = [5, 2, 8, 1, 9];
   sorted = user_modules.sorting.quicksort(data);

Creating Your First Module
----------------------------

**Step 1: Create Module Directory**

.. code-block:: bash

   mkdir -p src/user_modules
   cd src/user_modules

**Step 2: Write Module (sorting.ml)**

.. code-block:: ml

   // sorting.ml - Sorting utilities

   function swap(arr, i, j) {
       temp = arr[i];
       arr[i] = arr[j];
       arr[j] = temp;
   }

   function quicksort(arr) {
       if (len(arr) <= 1) {
           return arr;
       }

       pivot = arr[len(arr) / 2];
       left = [];
       middle = [];
       right = [];

       i = 0;
       while (i < len(arr)) {
           if (arr[i] < pivot) {
               left.push(arr[i]);
           } elif (arr[i] == pivot) {
               middle.push(arr[i]);
           } else {
               right.push(arr[i]);
           }
           i = i + 1;
       }

       return quicksort(left) + middle + quicksort(right);
   }

   function is_sorted(arr) {
       i = 0;
       while (i < len(arr) - 1) {
           if (arr[i] > arr[i + 1]) {
               return false;
           }
           i = i + 1;
       }
       return true;
   }

**Step 3: Import and Use (src/main.ml)**

.. code-block:: ml

   import user_modules.sorting;

   data = [64, 34, 25, 12, 22, 11, 90];

   sorted_data = user_modules.sorting.quicksort(data);

   if (user_modules.sorting.is_sorted(sorted_data)) {
       print("Sorting successful!");
       print(sorted_data);
   }

**Step 4: Run**

.. code-block:: bash

   cd src
   mlpy run main.ml

Module Organization
====================

File Structure
---------------

Organize modules with clear directory structure:

.. code-block:: text

   src/
   ├── main.ml                    # Main program
   └── user_modules/              # User module root
       ├── sorting.ml             # Simple module
       ├── math_utils.ml          # Math utilities
       ├── algorithms/            # Algorithm submodule
       │   ├── bubble.ml
       │   ├── quicksort.ml
       │   └── heapsort.ml
       └── data_structures/       # Data structures
           ├── linked_list.ml
           ├── binary_tree.ml
           └── graph.ml

Nested Module Hierarchies
---------------------------

Create nested modules with subdirectories:

**Directory Structure:**

.. code-block:: text

   src/user_modules/algorithms/
   ├── bubble.ml
   ├── quicksort.ml
   └── heapsort.ml

**Import Nested Modules:**

.. code-block:: ml

   // Import specific algorithms
   import user_modules.algorithms.bubble;
   import user_modules.algorithms.quicksort;
   import user_modules.algorithms.heapsort;

   data = [5, 2, 8, 1, 9];

   // Use different algorithms
   bubble_sorted = user_modules.algorithms.bubble.sort(data);
   quick_sorted = user_modules.algorithms.quicksort.sort(data);
   heap_sorted = user_modules.algorithms.heapsort.sort(data);

Module Naming Conventions
---------------------------

Follow these conventions for clarity:

**Module File Names:**

- Use lowercase: ``sorting.ml``, ``math_utils.ml``
- Use underscores for multi-word: ``string_utils.ml``
- Be descriptive: ``pathfinding.ml`` not ``pf.ml``

**Module Paths:**

.. code-block:: ml

   // Good - clear and descriptive
   import user_modules.sorting;
   import user_modules.algorithms.quicksort;
   import user_modules.data_structures.binary_tree;

   // Avoid - unclear
   import user_modules.s;
   import user_modules.alg.qs;

**Namespace Usage:**

.. code-block:: ml

   // Always use full qualified names for clarity
   result = user_modules.sorting.quicksort(data);

   // This prevents confusion about where functions come from
   // (Future feature: import aliases will enable shorter names)

Module Search and Resolution
==============================

How Module Resolution Works
-----------------------------

When you write ``import user_modules.sorting;``, mlpy searches for the module in this order:

**1. ML Standard Library**

First checks built-in modules:

- console, math, datetime, string, etc.
- Located in ``mlpy.stdlib`` package

**2. User Modules from Import Paths**

Searches directories specified in import paths:

.. code-block:: bash

   # Explicit import paths
   mlpy run main.ml --import-paths "./src/user_modules:./lib:./packages"

**3. Source File Directory (if allowed)**

Searches directory containing the source file:

.. code-block:: bash

   # Allow current directory imports
   mlpy run main.ml --allow-current-dir

**4. Resolution Algorithm:**

For ``import user_modules.sorting;``:

1. Convert to file path: ``user_modules/sorting.ml``
2. Search each import path for this file
3. Load and parse the ``.ml`` file
4. Transpile to Python
5. Cache for future use

**Example:**

.. code-block:: bash

   # With import path: ./src/user_modules
   import user_modules.sorting;

   # Resolves to: ./src/user_modules/sorting.ml

   # With nested path
   import user_modules.algorithms.quicksort;

   # Resolves to: ./src/user_modules/algorithms/quicksort.ml

Configuring Import Paths
--------------------------

**Method 1: Command Line**

.. code-block:: bash

   # Single path
   mlpy run main.ml --import-paths "./src/user_modules"

   # Multiple paths (colon-separated on Unix, semicolon on Windows)
   mlpy run main.ml --import-paths "./src/user_modules:./lib:./third_party"

   # With current directory
   mlpy run main.ml --import-paths "./lib" --allow-current-dir

**Method 2: Project Configuration**

Add to ``mlpy.json``:

.. code-block:: json

   {
     "name": "my-project",
     "import_paths": [
       "./src/user_modules",
       "./lib",
       "./packages"
     ],
     "allow_current_dir": false
   }

**Method 3: Environment Variable (Future)**

.. code-block:: bash

   export MLPY_PATH="./src/user_modules:./lib"
   mlpy run main.ml

Module Caching
---------------

mlpy caches compiled modules for performance:

**Cache Location:**

- Per-project cache: ``<project>/.mlpy/cache/``
- Global cache: ``~/.mlpy/cache/``

**Cache Invalidation:**

Automatic invalidation based on file timestamps:

1. Check if ``.py`` file exists for module
2. Compare timestamps: ``.ml`` vs ``.py``
3. If ``.ml`` is newer, recompile
4. Otherwise, use cached ``.py``

**Cache Benefits:**

.. code-block:: bash

   # First run: Compiles all modules
   mlpy run main.ml
   # Time: 2300ms

   # Second run: Uses cached modules
   mlpy run main.ml
   # Time: 450ms (80% faster!)

   # After editing sorting.ml: Only recompiles sorting
   mlpy run main.ml
   # Time: 600ms (only modified module retranspiled)

**Manual Cache Management:**

.. code-block:: bash

   # Clear project cache
   mlpy cache --clear-cache

   # Clear specific module
   mlpy cache --clear-module user_modules.sorting

   # Show cache statistics
   mlpy cache --stats

Transpilation and Deployment
==============================

Code Emission Modes
--------------------

mlpy provides three transpilation modes for different use cases:

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Mode
     - Use Case
     - Characteristics
   * - **multi-file**
     - Development, production
     - Separate .py files, cached, fast
   * - **single-file**
     - Distribution, deployment
     - One .py file, portable, self-contained
   * - **silent**
     - Testing, CI/CD
     - In-memory only, no files written

1. Multi-File Mode (Default)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Best for:** Development and production deployments

Creates separate Python files for each module with caching:

.. code-block:: bash

   mlpy compile main.ml --emit-code multi-file

**Generated Structure:**

.. code-block:: text

   src/
   ├── main.ml
   ├── main.py                    # Main program
   └── user_modules/
       ├── __init__.py            # Auto-generated
       ├── sorting.ml
       ├── sorting.py             # Cached transpiled module
       └── algorithms/
           ├── __init__.py        # Auto-generated
           ├── quicksort.ml
           └── quicksort.py       # Cached transpiled module

**Advantages:**

- ✅ **Fast** - Cached modules not retranspiled (80%+ speedup)
- ✅ **Clean** - Standard Python module structure
- ✅ **Debuggable** - Stack traces show actual file locations
- ✅ **Modular** - Easy to update individual modules

**Performance:**

.. code-block:: text

   First run:  2300ms (full transpilation)
   Second run: 450ms  (cached - 80% faster)
   After edit: 600ms  (only modified module retranspiled)

**Example:**

.. code-block:: bash

   # Compile with multi-file output
   mlpy compile src/main.ml --emit-code multi-file

   # Run generated Python
   python src/main.py

2. Single-File Mode (Portable)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Best for:** Distribution, deployment as single file

Inlines all modules into one Python file:

.. code-block:: bash

   mlpy compile main.ml --emit-code single-file -o dist/app.py

**Generated Structure:**

.. code-block:: python

   # dist/app.py - Everything in one file

   # Runtime helpers
   class _ModuleNamespace:
       _ml_user_module = True

   # User module: sorting
   def _umod_sorting_swap(arr, i, j):
       temp = arr[i]
       arr[i] = arr[j]
       arr[j] = temp

   def _umod_sorting_quicksort(arr):
       if len(arr) <= 1:
           return arr
       # Uses _umod_sorting_swap() internally
       # ... implementation
       return result

   # Create module namespace
   user_modules_sorting = _ModuleNamespace()
   user_modules_sorting.swap = _umod_sorting_swap
   user_modules_sorting.quicksort = _umod_sorting_quicksort

   # Main program
   data = [5, 2, 8, 1, 9]
   sorted_data = user_modules_sorting.quicksort(data)
   print(sorted_data)

**Advantages:**

- ✅ **Portable** - Single file distribution
- ✅ **Simple** - No directory structure needed
- ✅ **Self-contained** - All dependencies bundled
- ✅ **Embeddable** - Easy to embed in larger applications

**Disadvantages:**

- ⚠️ Large files for big projects
- ⚠️ No caching (full retranspilation each time)
- ⚠️ Harder debugging (all code in one file)

**Example:**

.. code-block:: bash

   # Create single-file distribution
   mlpy compile src/main.ml --emit-code single-file -o dist/app.py

   # Distribute just app.py
   python dist/app.py

3. Silent Mode (Testing)
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Best for:** Quick testing, CI/CD, validation

Transpiles to memory only, no files written:

.. code-block:: bash

   mlpy run main.ml --emit-code silent

**Advantages:**

- ✅ **Fast** - No file I/O overhead
- ✅ **Clean** - No filesystem artifacts
- ✅ **Safe** - Perfect for CI/CD pipelines
- ✅ **Testing** - Validate without side effects

**Use Cases:**

.. code-block:: bash

   # Quick execution (default for run command)
   mlpy run src/main.ml

   # CI/CD validation
   mlpy compile src/main.ml --emit-code silent
   if [ $? -eq 0 ]; then
       echo "Code validated successfully"
   fi

   # Security audit without generating files
   mlpy audit src/main.ml --emit-code silent

Choosing the Right Mode
-------------------------

**Decision Tree:**

.. code-block:: text

   Are you developing?
   ├─ Yes → Use multi-file (fast iteration, caching)
   └─ No → Are you deploying?
       ├─ Yes → Need single file?
       │   ├─ Yes → Use single-file (portable distribution)
       │   └─ No → Use multi-file (efficient, standard structure)
       └─ No → Testing/CI?
           └─ Use silent (clean, no artifacts)

**Practical Examples:**

.. code-block:: bash

   # Development workflow
   mlpy compile src/main.ml --emit-code multi-file
   python src/main.py

   # Create portable distribution
   mlpy compile src/main.ml --emit-code single-file -o dist/app.py
   # Ship dist/app.py to customers

   # CI/CD pipeline
   mlpy run src/main.ml --emit-code silent
   mlpy run tests/test_main.ml --emit-code silent

   # Production deployment (containerized)
   mlpy compile src/main.ml --emit-code multi-file
   docker build -t myapp .
   # Dockerfile copies src/*.py and src/user_modules/*.py

Deployment Strategies
======================

Strategy 1: Direct Execution
------------------------------

Execute ML files directly with mlpy:

**Setup:**

.. code-block:: bash

   # Install mlpy on production server
   pip install mlpy

   # Deploy ML source files
   scp -r src/ user@server:/app/

   # Run on server
   ssh user@server "cd /app && mlpy run src/main.ml"

**Advantages:**

- Simple deployment (just copy .ml files)
- Automatic transpilation and caching
- Easy updates (edit .ml files)

**Disadvantages:**

- Requires mlpy installed on server
- Transpilation overhead on first run

**Best For:** Internal tools, development servers, rapid iteration

Strategy 2: Pre-Compiled Deployment
-------------------------------------

Compile to Python files, deploy compiled code:

**Setup:**

.. code-block:: bash

   # Compile locally
   mlpy compile src/main.ml --emit-code multi-file

   # Deploy Python files only
   scp -r src/*.py src/user_modules/*.py user@server:/app/

   # Run on server (no mlpy needed!)
   ssh user@server "cd /app && python main.py"

**Advantages:**

- No mlpy required on server
- Python-only deployment
- Standard Python execution

**Disadvantages:**

- Must recompile and redeploy for changes
- Deploy multiple files

**Best For:** Production servers, customer deployments, environments without mlpy

Strategy 3: Single-File Distribution
--------------------------------------

Compile to single portable file:

**Setup:**

.. code-block:: bash

   # Compile to single file
   mlpy compile src/main.ml --emit-code single-file -o dist/app.py

   # Deploy single file
   scp dist/app.py user@server:/app/

   # Run on server
   ssh user@server "python /app/app.py"

**Advantages:**

- Single file to deploy
- No mlpy required
- Portable and self-contained

**Disadvantages:**

- Large file for big projects
- Full recompilation for any change

**Best For:** Embedded applications, simple deployment, distribution to end users

Strategy 4: Containerized Deployment
--------------------------------------

Use Docker for consistent environments:

**Dockerfile:**

.. code-block:: dockerfile

   FROM python:3.12-slim

   # Install mlpy
   RUN pip install mlpy

   # Copy source code
   COPY src/ /app/src/
   WORKDIR /app

   # Pre-compile modules (optional - for faster startup)
   RUN mlpy compile src/main.ml --emit-code multi-file

   # Run application
   CMD ["python", "src/main.py"]

**Build and Deploy:**

.. code-block:: bash

   # Build image
   docker build -t myapp:1.0 .

   # Run container
   docker run -d myapp:1.0

   # Or use docker-compose.yml
   docker-compose up -d

**Advantages:**

- Consistent environment
- Easy scaling
- Includes all dependencies

**Best For:** Cloud deployments, microservices, production applications

Configuration for Deployment
==============================

Production Configuration
-------------------------

Create separate configs for different environments:

**development.json:**

.. code-block:: json

   {
     "name": "my-project",
     "security_level": "normal",
     "allowed_capabilities": [
       "console.write",
       "console.error",
       "file.read:/data/**",
       "file.write:/output/**",
       "network.http:*"
     ],
     "optimization_level": 1,
     "source_maps": true
   }

**production.json:**

.. code-block:: json

   {
     "name": "my-project",
     "security_level": "strict",
     "allowed_capabilities": [
       "console.write",
       "file.read:/data/config.json",
       "network.http:api.company.com"
     ],
     "optimization_level": 3,
     "source_maps": false
   }

**Usage:**

.. code-block:: bash

   # Development
   mlpy run src/main.ml --config development.json

   # Production
   mlpy compile src/main.ml --config production.json --emit-code multi-file

Environment Variables
----------------------

Use environment variables for sensitive configuration:

**mlpy.json:**

.. code-block:: json

   {
     "name": "my-project",
     "database_url": "${DATABASE_URL}",
     "api_key": "${API_KEY}",
     "allowed_capabilities": [
       "network.http:${API_HOST}"
     ]
   }

**Deployment:**

.. code-block:: bash

   export DATABASE_URL="postgresql://localhost/mydb"
   export API_KEY="secret-key-here"
   export API_HOST="api.company.com"

   mlpy run src/main.ml

Best Practices
===============

Module Organization
--------------------

**1. Single Responsibility**

Each module should have one clear purpose:

.. code-block:: ml

   // ✅ Good - focused modules
   user_modules/sorting.ml          // Only sorting algorithms
   user_modules/searching.ml        // Only search algorithms
   user_modules/data_validation.ml // Only validation functions

   // ❌ Bad - unfocused
   user_modules/utilities.ml        // Too generic, everything mixed

**2. Logical Grouping**

Group related functionality in subdirectories:

.. code-block:: text

   user_modules/
   ├── algorithms/
   │   ├── sorting.ml
   │   ├── searching.ml
   │   └── graph.ml
   ├── data_structures/
   │   ├── linked_list.ml
   │   ├── binary_tree.ml
   │   └── hash_table.ml
   └── utilities/
       ├── string_utils.ml
       ├── math_utils.ml
       └── date_utils.ml

**3. Avoid Deep Nesting**

Keep hierarchy shallow (2-3 levels maximum):

.. code-block:: text

   ✅ Good depth
   user_modules/algorithms/sorting.ml

   ❌ Too deep
   user_modules/algorithms/comparison/sorting/advanced/optimized/quicksort.ml

Module Design
--------------

**1. Clear Function Names**

.. code-block:: ml

   // ✅ Good - descriptive
   function calculate_median(numbers) { ... }
   function validate_email_address(email) { ... }
   function convert_to_uppercase(text) { ... }

   // ❌ Bad - unclear
   function calc(nums) { ... }
   function check(e) { ... }
   function conv(t) { ... }

**2. Documentation**

Add comments explaining module purpose:

.. code-block:: ml

   // sorting.ml - Sorting algorithm implementations
   //
   // Provides multiple sorting algorithms:
   // - quicksort: Fast O(n log n) average case
   // - merge_sort: Stable O(n log n) guaranteed
   // - bubble_sort: Simple O(n²) for small arrays
   //
   // All functions work on arrays of numbers.

   function quicksort(arr) {
       // Quicksort using Lomuto partition scheme
       // Returns new sorted array (non-mutating)
       ...
   }

**3. Module Independence**

Minimize module dependencies:

.. code-block:: ml

   // ✅ Good - independent module
   // sorting.ml - No external dependencies
   function quicksort(arr) {
       // Pure sorting logic
       ...
   }

   // ⚠️ Okay - documented dependency
   // advanced_sorting.ml
   import user_modules.sorting;  // Requires sorting module

   function adaptive_sort(arr) {
       // Uses user_modules.sorting.quicksort internally
       ...
   }

   // ❌ Bad - circular dependency
   // module_a.ml imports module_b.ml
   // module_b.ml imports module_a.ml
   // ❌ Will fail to compile

Version Control
----------------

**What to Commit:**

.. code-block:: bash

   # Commit these
   git add src/*.ml
   git add src/user_modules/**/*.ml
   git add mlpy.json
   git add README.md
   git add tests/*.ml

**What to .gitignore:**

.. code-block:: bash

   # .gitignore
   # Compiled output
   dist/
   *.py
   __pycache__/
   *.pyc

   # Cache
   .mlpy/cache/
   .mlpy/logs/

   # IDE files
   .vscode/
   .idea/

Performance Tips
-----------------

**1. Use Multi-File Mode in Development**

.. code-block:: bash

   # Fast iteration with caching
   mlpy compile src/main.ml --emit-code multi-file

**2. Organize for Selective Import (Future)**

Prepare for future selective import feature:

.. code-block:: ml

   // When selective imports arrive:
   // import { quicksort, merge_sort } from user_modules.sorting;

   // For now, organize modules so each has focused functionality
   // This makes future refactoring easier

**3. Profile Module Load Times**

.. code-block:: bash

   # Check which modules are slow
   mlpy run src/main.ml --profile --emit-code multi-file

   # Shows time spent in each module

Troubleshooting
================

Common Issues
--------------

**Issue: Module Not Found**

.. code-block:: text

   ❌ Error: Module 'user_modules.sorting' not found

**Solutions:**

.. code-block:: bash

   # 1. Check file exists
   ls src/user_modules/sorting.ml

   # 2. Specify import path
   mlpy run main.ml --import-paths "./src/user_modules"

   # 3. Use --allow-current-dir if module in same directory
   mlpy run main.ml --allow-current-dir

**Issue: Import Path Not Working**

.. code-block:: text

   ❌ Error: Cannot resolve import path

**Solutions:**

.. code-block:: bash

   # Use absolute paths
   mlpy run main.ml --import-paths "$(pwd)/src/user_modules"

   # Check path separators (: on Unix, ; on Windows)
   # Unix/Linux/Mac:
   mlpy run main.ml --import-paths "./lib:./modules"

   # Windows:
   mlpy run main.ml --import-paths "./lib;./modules"

**Issue: Circular Dependencies**

.. code-block:: ml

   // module_a.ml
   import user_modules.module_b;  // imports B

   // module_b.ml
   import user_modules.module_a;  // imports A
   ❌ Error: Circular dependency detected

**Solution: Refactor to shared module:**

.. code-block:: ml

   // Create module_shared.ml with common code
   function shared_function() { ... }

   // module_a.ml
   import user_modules.module_shared;

   // module_b.ml
   import user_modules.module_shared;

**Issue: Cache Stale After External Edit**

.. code-block:: bash

   # Module changed by external tool but cache not updated

   # Force cache clear
   mlpy cache --clear-cache

   # Or delete specific cached file
   rm src/user_modules/sorting.py

Debug Tips
-----------

**1. Check Generated Python Code**

.. code-block:: bash

   # Compile to see generated Python
   mlpy compile src/main.ml --emit-code multi-file

   # Examine generated module
   cat src/user_modules/sorting.py

**2. Use Single-File Mode for Debugging**

.. code-block:: bash

   # Everything in one file makes it easier to see full picture
   mlpy compile src/main.ml --emit-code single-file -o debug.py

   # Examine debug.py to understand module integration

**3. Enable Source Maps**

.. code-block:: bash

   mlpy compile src/main.ml --source-maps

   # Source maps help trace Python errors back to ML code

Summary
========

Key Takeaways
--------------

**Project Management:**

- ✅ Use ``mlpy --init`` to create structured projects
- ✅ Configure via ``mlpy.json`` or ``mlpy.yaml``
- ✅ Organize code in ``src/``, tests in ``tests/``

**User Modules:**

- ✅ Create reusable modules in ``user_modules/`` directory
- ✅ Import with: ``import user_modules.module_name;``
- ✅ Use nested hierarchies for organization
- ✅ Automatic caching speeds up repeated compilations

**Transpilation Modes:**

- ✅ **multi-file** - Development and production (cached, fast)
- ✅ **single-file** - Portable distribution (self-contained)
- ✅ **silent** - Testing and CI/CD (no files)

**Deployment:**

- ✅ Multiple strategies: direct execution, pre-compiled, containerized
- ✅ Separate configs for development vs production
- ✅ Security-first with capability configuration

Quick Reference
----------------

.. code-block:: bash

   # Initialize project
   mlpy --init my-project

   # Create user module
   mkdir -p src/user_modules
   # Write src/user_modules/mymodule.ml

   # Import in main.ml
   # import user_modules.mymodule;

   # Compile with caching
   mlpy compile src/main.ml --emit-code multi-file

   # Create portable distribution
   mlpy compile src/main.ml --emit-code single-file -o dist/app.py

   # Quick test
   mlpy run src/main.ml --emit-code silent

   # Clear cache
   mlpy cache --clear-cache

Next Steps
-----------

**Master User Modules:**

1. Create your first user module
2. Build a library of reusable utilities
3. Organize modules into logical hierarchies
4. Share modules across projects

**Explore Other Guides:**

- :doc:`repl-guide` - Interactive development
- :doc:`transpilation` - Execution and deployment details
- :doc:`capabilities` - Security configuration
- :doc:`../language-reference/index` - ML language syntax

**Advanced Topics:**

- Module exports and privacy (future feature)
- Package manager integration (planned)
- HTTP module imports (future enhancement)
