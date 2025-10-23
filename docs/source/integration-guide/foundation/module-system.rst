Unified Module System
======================

.. note::
   **Chapter Summary:** Deep dive into the unified module registry that manages both Python bridge modules and ML source modules. Learn auto-detection, lazy loading, hot reloading, and performance monitoring.

The ML module system provides a **unified registry** for both Python bridge modules (Python code callable from ML) and ML source modules (ML code in `.ml` files). This chapter explains how to extend ML with custom modules, configure module paths, and use development tools for rapid iteration.

.. contents:: Chapter Contents
   :local:
   :depth: 2

----

Introduction
------------

ML's module system solves a critical problem: **how to extend the language with custom functionality while maintaining security and developer productivity.**

Traditional Approach: 6 Manual Steps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before the unified module system, adding a custom module required:

.. code-block:: python

   # Step 1: Create module file
   # Step 2: Define functions with @ml_function decorator
   # Step 3: Register with ModuleRegistry manually
   # Step 4: Add to SafeAttributeRegistry
   # Step 5: Update import resolver
   # Step 6: Restart REPL/application

**Result:** 50+ lines of boilerplate, error-prone, slow iteration.

Modern Approach: 1 Decorator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With the unified module system:

.. code-block:: python

   from src.mlpy.stdlib.decorators import ml_module

   @ml_module("mymodule")
   class MyModule:
       @staticmethod
       def my_function(x):
           return x * 2

**Result:** Auto-detected, lazy-loaded, hot-reloadable. **6 steps → 1 decorator!**

Key Innovations
~~~~~~~~~~~~~~~

The unified module system provides:

1. **Single Registry:** Both Python bridges and ML modules tracked together
2. **Auto-Detection:** Modules discovered automatically in configured paths
3. **Lazy Loading:** Modules loaded only when imported
4. **Hot Reloading:** Changes applied without restart (`.reload` command)
5. **Type-Aware Monitoring:** Performance tracking by module type
6. **Nested Support:** ML modules in nested directories (`user.utils.math`)

----

Unified Module Registry Architecture
-------------------------------------

The `ModuleRegistry` is the central component managing all modules.

Architecture Overview
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   ┌───────────────────────────────────────────────────────────┐
   │                    ModuleRegistry                          │
   │                                                            │
   │  ┌──────────────────────┐  ┌──────────────────────┐      │
   │  │  Python Bridge       │  │  ML Source           │      │
   │  │  Modules             │  │  Modules             │      │
   │  │                      │  │                      │      │
   │  │  • math_bridge.py    │  │  • user_utils.ml     │      │
   │  │  • crypto_bridge.py  │  │  • algorithms.ml     │      │
   │  │  • custom_module.py  │  │  • data_proc.ml      │      │
   │  └──────────────────────┘  └──────────────────────┘      │
   │                                                            │
   │  Unified Metadata:                                        │
   │  • Module name                                            │
   │  • Module type (python_bridge | ml_source)               │
   │  • Load time / Transpilation time                        │
   │  • Memory usage                                           │
   │  • Reload count                                           │
   └───────────────────────────────────────────────────────────┘

**Key Distinction:**

* **Python Bridge Modules:** Python code that ML can call (standard library, custom extensions)
* **ML Source Modules:** ML code in `.ml` files (user-defined utilities, libraries)

Module Metadata
~~~~~~~~~~~~~~~

Each registered module stores comprehensive metadata:

.. code-block:: python

   @dataclass
   class UnifiedModuleMetadata:
       name: str                    # Module name (e.g., "math", "user.utils")
       module_type: str             # "python_bridge" or "ml_source"
       file_path: Optional[str]     # Path to .py or .ml file

       # Performance tracking
       load_time: float             # For Python bridges
       transpilation_time: float    # For ML modules
       memory_usage: int            # Bytes used
       reload_count: int            # Number of hot reloads

       # Type-specific fields
       functions: List[str]         # Available functions
       capabilities_required: List[str]  # Required capabilities

Module Discovery Process
~~~~~~~~~~~~~~~~~~~~~~~~

The registry discovers modules through these steps:

**1. Scan Configured Paths**

.. code-block:: python

   # Python bridge modules
   python_extension_paths = [
       "/project/extensions",
       "/custom/modules"
   ]

   # ML source modules
   ml_module_paths = [
       "/project/ml_modules",
       "/user/ml_libs"
   ]

**2. Auto-Detect Modules**

.. code-block:: python

   # For Python bridges: Look for @ml_module decorator
   for py_file in scan_path(python_extension_paths, "*.py"):
       if has_ml_module_decorator(py_file):
           register_python_bridge(py_file)

   # For ML modules: Look for .ml files
   for ml_file in scan_path(ml_module_paths, "*.ml"):
       register_ml_source(ml_file)

**3. Lazy Registration**

.. code-block:: python

   # Modules registered but NOT loaded yet
   registry.register_module(
       name="user.algorithms",
       module_type="ml_source",
       file_path="/user/ml_libs/algorithms.ml",
       loaded=False  # Lazy loading
   )

**4. Load on Import**

.. code-block:: ml

   // First import triggers loading
   import user.algorithms;  // Registry loads and transpiles now

   result = user.algorithms.quicksort(data);

**Performance:** Discovery completes in <100ms for 100 modules.

Thread Safety
~~~~~~~~~~~~~

The registry uses thread-local storage for concurrent safety:

.. code-block:: python

   import threading

   class ModuleRegistry:
       def __init__(self):
           self._modules = {}
           self._lock = threading.RLock()  # Reentrant lock

       def register_module(self, metadata):
           with self._lock:
               self._modules[metadata.name] = metadata

       def get_module(self, name):
           with self._lock:
               return self._modules.get(name)

**Guarantee:** Multiple threads can load different modules concurrently without conflicts.

----

Creating Custom Python Bridge Modules
--------------------------------------

Python bridge modules allow you to expose Python functionality to ML code.

The @ml_module Decorator
~~~~~~~~~~~~~~~~~~~~~~~~

The simplest way to create a module:

.. code-block:: python

   # File: my_extensions/crypto_module.py
   from src.mlpy.stdlib.decorators import ml_module

   @ml_module("crypto")
   class CryptoModule:
       """Custom cryptography module for ML"""

       @staticmethod
       def hash_sha256(data: str) -> str:
           import hashlib
           return hashlib.sha256(data.encode()).hexdigest()

       @staticmethod
       def generate_uuid() -> str:
           import uuid
           return str(uuid.uuid4())

       @staticmethod
       def random_bytes(n: int) -> str:
           import secrets
           return secrets.token_hex(n)

**Usage in ML:**

.. code-block:: ml

   import crypto;

   function secure_id() {
       return crypto.generate_uuid();
   }

   function hash_password(password) {
       return crypto.hash_sha256(password);
   }

**Benefits:**

* ✅ Auto-detected by registry
* ✅ Lazy-loaded on first import
* ✅ Hot-reloadable with `.reload crypto`
* ✅ Performance tracked in `.perfmon`

Complete Example: Database Module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A production-ready module with capability requirements:

.. code-block:: python

   # File: extensions/database.py
   from src.mlpy.stdlib.decorators import ml_module, ml_function
   from src.mlpy.runtime.capabilities import require_capability
   import sqlite3

   @ml_module("database")
   class DatabaseModule:
       """Database operations for ML"""

       def __init__(self):
           self.connections = {}

       @ml_function
       @require_capability("database:connect")
       def connect(self, db_path: str) -> str:
           """Connect to SQLite database"""
           conn_id = f"conn_{len(self.connections)}"
           conn = sqlite3.connect(db_path)
           self.connections[conn_id] = conn
           return conn_id

       @ml_function
       @require_capability("database:read")
       def query(self, conn_id: str, sql: str) -> list:
           """Execute SELECT query"""
           if conn_id not in self.connections:
               raise ValueError(f"Invalid connection: {conn_id}")

           conn = self.connections[conn_id]
           cursor = conn.cursor()
           cursor.execute(sql)

           # Return as list of dicts
           columns = [desc[0] for desc in cursor.description]
           results = []
           for row in cursor.fetchall():
               results.append(dict(zip(columns, row)))

           return results

       @ml_function
       @require_capability("database:write")
       def execute(self, conn_id: str, sql: str) -> int:
           """Execute INSERT/UPDATE/DELETE"""
           if conn_id not in self.connections:
               raise ValueError(f"Invalid connection: {conn_id}")

           conn = self.connections[conn_id]
           cursor = conn.cursor()
           cursor.execute(sql)
           conn.commit()

           return cursor.rowcount

       @ml_function
       def close(self, conn_id: str):
           """Close database connection"""
           if conn_id in self.connections:
               self.connections[conn_id].close()
               del self.connections[conn_id]

**Usage in ML:**

.. code-block:: ml

   import database;

   function get_users() {
       conn = database.connect("/data/users.db");
       users = database.query(conn, "SELECT * FROM users");
       database.close(conn);
       return users;
   }

   function add_user(name, email) {
       conn = database.connect("/data/users.db");
       sql = "INSERT INTO users (name, email) VALUES ('" + name + "', '" + email + "')";
       database.execute(conn, sql);
       database.close(conn);
   }

**Security Note:** This module requires capabilities:
- `database:connect` - To open connections
- `database:read` - To execute SELECT
- `database:write` - To execute INSERT/UPDATE/DELETE

Registering Functions with Type Hints
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Type hints improve error messages and IDE support:

.. code-block:: python

   @ml_module("validation")
   class ValidationModule:
       @staticmethod
       def validate_email(email: str) -> bool:
           """Validate email format"""
           import re
           pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
           return bool(re.match(pattern, email))

       @staticmethod
       def validate_phone(phone: str, country: str = "US") -> bool:
           """Validate phone number for country"""
           patterns = {
               "US": r'^\+?1?\d{10}$',
               "UK": r'^\+?44\d{10}$',
               "EU": r'^\+?[1-9]\d{8,14}$'
           }
           pattern = patterns.get(country, patterns["EU"])
           import re
           return bool(re.match(pattern, phone))

**ML Usage:**

.. code-block:: ml

   import validation;

   function check_contact(email, phone) {
       email_valid = validation.validate_email(email);
       phone_valid = validation.validate_phone(phone, "US");

       return {
           email_valid: email_valid,
           phone_valid: phone_valid,
           both_valid: email_valid && phone_valid
       };
   }

Module Configuration Options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configure modules with metadata:

.. code-block:: python

   @ml_module(
       name="advanced_math",
       version="1.0.0",
       description="Advanced mathematical functions",
       capabilities_required=["math:advanced"],
       allow_eval=False  # Security: block eval in this module
   )
   class AdvancedMath:
       @staticmethod
       def factorial(n: int) -> int:
           if n <= 1:
               return 1
           return n * AdvancedMath.factorial(n - 1)

       @staticmethod
       def fibonacci(n: int) -> int:
           if n <= 1:
               return n
           a, b = 0, 1
           for _ in range(2, n + 1):
               a, b = b, a + b
           return b

**Metadata is tracked by registry and visible in `.modinfo` command.**

----

Writing ML Source Modules
--------------------------

ML source modules are `.ml` files that other ML code can import.

Basic ML Module Structure
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   // File: ml_modules/utilities.ml

   // Module-level imports (required!)
   import math;
   import console;

   // Exported functions
   function square(x) {
       return x * x;
   }

   function cube(x) {
       return x * x * x;
   }

   function hypotenuse(a, b) {
       return math.sqrt(square(a) + square(b));
   }

   // Private helper (by convention, starts with _)
   function _internal_helper(x) {
       return x + 1;
   }

**Usage:**

.. code-block:: ml

   // In another ML file
   import utilities;

   result = utilities.square(5);        // 25
   diagonal = utilities.hypotenuse(3, 4);  // 5.0

**Key Rule:** All imports must be at module level, not inside functions!

Nested ML Modules
~~~~~~~~~~~~~~~~~

Organize ML modules in nested directories:

.. code-block:: text

   ml_modules/
   ├── algorithms/
   │   ├── sorting.ml
   │   ├── searching.ml
   │   └── graph.ml
   ├── data_structures/
   │   ├── stack.ml
   │   ├── queue.ml
   │   └── tree.ml
   └── utils/
       ├── string_utils.ml
       └── array_utils.ml

**Import Syntax:**

.. code-block:: ml

   import algorithms.sorting;
   import data_structures.stack;
   import utils.string_utils;

   sorted_data = algorithms.sorting.quicksort(data);
   my_stack = data_structures.stack.create();
   cleaned = utils.string_utils.trim(text);

**Registry Naming:** Dots become module hierarchy (`algorithms.sorting`)

Complete Example: ML Data Processing Library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   // File: ml_modules/data_processing.ml
   import math;
   import functional;

   // Statistical functions
   function mean(numbers) {
       if (len(numbers) == 0) {
           return 0;
       }
       sum = functional.reduce(numbers, function(acc, x) { return acc + x; }, 0);
       return sum / len(numbers);
   }

   function median(numbers) {
       if (len(numbers) == 0) {
           return 0;
       }

       sorted = functional.sort(numbers);
       mid = len(sorted) / 2;

       if (len(sorted) % 2 == 0) {
           // Even: average of two middle values
           return (sorted[mid - 1] + sorted[mid]) / 2;
       } else {
           // Odd: middle value
           return sorted[math.floor(mid)];
       }
   }

   function std_deviation(numbers) {
       if (len(numbers) == 0) {
           return 0;
       }

       avg = mean(numbers);
       squared_diffs = functional.map(numbers, function(x) {
           diff = x - avg;
           return diff * diff;
       });

       variance = mean(squared_diffs);
       return math.sqrt(variance);
   }

   // Data transformation
   function normalize(numbers) {
       if (len(numbers) == 0) {
           return [];
       }

       min_val = functional.reduce(numbers, function(acc, x) {
           return x < acc ? x : acc;
       }, numbers[0]);

       max_val = functional.reduce(numbers, function(acc, x) {
           return x > acc ? x : acc;
       }, numbers[0]);

       range = max_val - min_val;
       if (range == 0) {
           return functional.map(numbers, function(x) { return 0; });
       }

       return functional.map(numbers, function(x) {
           return (x - min_val) / range;
       });
   }

   // Outlier detection
   function detect_outliers(numbers, threshold) {
       if (len(numbers) == 0) {
           return [];
       }

       avg = mean(numbers);
       std = std_deviation(numbers);

       outliers = functional.filter(numbers, function(x) {
           z_score = math.abs((x - avg) / std);
           return z_score > threshold;
       });

       return outliers;
   }

**Usage:**

.. code-block:: ml

   import data_processing;

   function analyze_sales(sales_data) {
       avg_sales = data_processing.mean(sales_data);
       median_sales = data_processing.median(sales_data);
       std_sales = data_processing.std_deviation(sales_data);

       // Normalize to 0-1 range
       normalized = data_processing.normalize(sales_data);

       // Detect outliers (> 2 standard deviations)
       outliers = data_processing.detect_outliers(sales_data, 2.0);

       return {
           mean: avg_sales,
           median: median_sales,
           std_dev: std_sales,
           normalized: normalized,
           outliers: outliers
       };
   }

ML-to-ML Imports
~~~~~~~~~~~~~~~~

ML modules can import other ML modules:

.. code-block:: ml

   // File: ml_modules/validation.ml
   import utils.string_utils;

   function validate_username(username) {
       // Use imported ML module
       cleaned = utils.string_utils.trim(username);
       return len(cleaned) >= 3 && len(cleaned) <= 20;
   }

**Transpilation Process:**

1. Registry detects `import utils.string_utils`
2. Checks if `utils/string_utils.ml` exists
3. Transpiles `string_utils.ml` if needed
4. Makes functions available to `validation.ml`

**Performance:** Transpilation is cached, so repeated imports are instant.

Module Naming Conventions
~~~~~~~~~~~~~~~~~~~~~~~~~~

Follow these conventions for consistency:

.. code-block:: text

   GOOD:
   - user_utils.ml          (snake_case for file names)
   - data_processing.ml
   - algorithms/sorting.ml  (nested with /))

   BAD:
   - UserUtils.ml           (PascalCase - avoid)
   - data-processing.ml     (kebab-case - avoid)
   - algorithms.sorting.ml  (dots in filename - breaks imports)

**Import Mapping:**

.. code-block:: ml

   import user_utils;           // File: user_utils.ml
   import algorithms.sorting;   // File: algorithms/sorting.ml
   import data.processing.core; // File: data/processing/core.ml

----

Configuration
-------------

Configure module paths for both Python and ML modules.

Python Extension Paths
~~~~~~~~~~~~~~~~~~~~~~

Configure where to find Python bridge modules:

**1. Project Configuration File:**

.. code-block:: json

   {
     "python_extension_paths": [
       "/project/extensions",
       "/shared/modules"
     ]
   }

**2. CLI Flag:**

.. code-block:: bash

   mlpy repl -E /project/extensions -E /shared/modules

**3. Environment Variable:**

.. code-block:: bash

   export MLPY_PYTHON_EXTENSION_PATHS="/project/extensions:/shared/modules"
   mlpy repl

**Discovery:** All `.py` files with `@ml_module` decorator in these paths are auto-detected.

ML Module Paths
~~~~~~~~~~~~~~~

Configure where to find ML source modules:

**1. Project Configuration File:**

.. code-block:: json

   {
     "ml_module_paths": [
       "/project/ml_modules",
       "/user/libraries"
     ]
   }

**2. CLI Flag:**

.. code-block:: bash

   mlpy repl -M /project/ml_modules -M /user/libraries

**3. Environment Variable:**

.. code-block:: bash

   export MLPY_ML_MODULE_PATHS="/project/ml_modules:/user/libraries"
   mlpy repl

**Discovery:** All `.ml` files in these paths become importable modules.

Configuration Priority
~~~~~~~~~~~~~~~~~~~~~~

Configuration sources are applied in this order (highest to lowest priority):

.. code-block:: text

   1. CLI Flags (-E, -M)           ← Highest priority
   2. Project Config (mlpy.json)
   3. Environment Variables
   4. Default Paths                ← Lowest priority

**Example:**

.. code-block:: bash

   # CLI overrides project config
   mlpy repl -M /tmp/test_modules  # Uses /tmp/test_modules, not mlpy.json

Unified Configuration Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Complete project configuration:

.. code-block:: json

   {
     "project_name": "myapp",
     "python_extension_paths": [
       "extensions",           // Relative to project root
       "/opt/shared/modules"   // Absolute path
     ],
     "ml_module_paths": [
       "ml_libs",              // Project ML modules
       "vendor/ml_packages"    // Third-party ML modules
     ],
     "capabilities": {
       "file:read": ["/data/*.json"],
       "file:write": ["/output/*.json"],
       "database:connect": ["sqlite:///data/*.db"]
     },
     "security": {
       "strict_security": true,
       "allow_eval": false
     }
   }

**Usage:**

.. code-block:: bash

   # Loads config automatically if mlpy.json exists in current directory
   mlpy repl

Path Resolution
~~~~~~~~~~~~~~~

Relative paths are resolved relative to project root:

.. code-block:: python

   # Project structure:
   /home/user/myproject/
   ├── mlpy.json
   ├── extensions/
   │   └── custom.py
   └── ml_libs/
       └── utils.ml

.. code-block:: json

   {
     "python_extension_paths": ["extensions"],  // → /home/user/myproject/extensions
     "ml_module_paths": ["ml_libs"]            // → /home/user/myproject/ml_libs
   }

**Absolute paths work too:**

.. code-block:: json

   {
     "python_extension_paths": ["/opt/mlpy/extensions"],
     "ml_module_paths": ["/opt/mlpy/modules"]
   }

----

Module Operations
-----------------

Work with modules using REPL commands and API calls.

Hot Reloading
~~~~~~~~~~~~~

Reload modules without restarting:

**REPL Command:**

.. code-block:: ml

   > .reload math
   [OK] Module 'math' reloaded (Python bridge, 5ms)

   > .reload user_utils
   [OK] Module 'user_utils' reloaded (ML source, 18ms, retranspiled)

**Python API:**

.. code-block:: python

   from src.mlpy.stdlib.module_registry import ModuleRegistry

   registry = ModuleRegistry()

   # Reload Python bridge
   registry.reload_module("crypto")

   # Reload ML module (retranspiles)
   registry.reload_module("user.algorithms")

**What Happens:**

1. **Python Bridge:** Re-imports Python module, updates function registry
2. **ML Source:** Re-reads `.ml` file, retranspiles, updates namespace

**Performance:**

* Python bridge reload: ~5ms
* ML module reload: ~20ms (includes transpilation)

Module Discovery
~~~~~~~~~~~~~~~~

View all available modules:

**REPL Command:**

.. code-block:: ml

   > .modules

   Python Bridge Modules (12):
   - builtin          (load: 2ms, memory: 45KB)
   - console          (load: 1ms, memory: 12KB)
   - math             (load: 3ms, memory: 28KB)
   - datetime         (load: 4ms, memory: 35KB)
   - crypto           (load: 8ms, memory: 52KB)  [custom]
   ...

   ML Source Modules (5):
   - user_utils       (transpile: 15ms, memory: 18KB)
   - data_processing  (transpile: 22ms, memory: 31KB)
   - algorithms.sorting (transpile: 18ms, memory: 24KB)
   ...

**Python API:**

.. code-block:: python

   # Get all modules
   all_modules = registry.list_modules()

   # Filter by type
   python_modules = registry.list_modules(module_type="python_bridge")
   ml_modules = registry.list_modules(module_type="ml_source")

   # Get module info
   info = registry.get_module_info("user_utils")
   print(f"Type: {info.module_type}")
   print(f"Transpilation time: {info.transpilation_time}ms")
   print(f"Functions: {info.functions}")

Module Information
~~~~~~~~~~~~~~~~~~

Get detailed module information:

**REPL Command:**

.. code-block:: ml

   > .modinfo data_processing

   Module: data_processing
   Type: ML Source
   Path: /project/ml_libs/data_processing.ml
   Transpilation Time: 22.5ms
   Memory Usage: 31KB
   Reload Count: 3

   Functions (6):
   - mean(numbers)
   - median(numbers)
   - std_deviation(numbers)
   - normalize(numbers)
   - detect_outliers(numbers, threshold)

   Imports:
   - math (Python bridge)
   - functional (Python bridge)

**Python API:**

.. code-block:: python

   from src.mlpy.stdlib.builtin import module_info

   # Get module info from ML code
   info = module_info("data_processing")

   # Returns dict:
   # {
   #   "name": "data_processing",
   #   "type": "ml_source",
   #   "path": "/project/ml_libs/data_processing.ml",
   #   "transpilation_time": 22.5,
   #   "memory_usage": 31744,
   #   "reload_count": 3,
   #   "functions": ["mean", "median", "std_deviation", ...]
   # }

Nested Directory Support
~~~~~~~~~~~~~~~~~~~~~~~~~

Work with nested module hierarchies:

.. code-block:: bash

   # Directory structure
   ml_modules/
   ├── algorithms/
   │   ├── sorting.ml
   │   └── graph/
   │       ├── dijkstra.ml
   │       └── bfs.ml
   └── utils/
       └── math_utils.ml

.. code-block:: ml

   // Import nested modules
   import algorithms.sorting;
   import algorithms.graph.dijkstra;
   import utils.math_utils;

   // Use
   sorted = algorithms.sorting.quicksort(data);
   path = algorithms.graph.dijkstra.shortest_path(graph, start, end);

**Registry Tracking:**

.. code-block:: ml

   > .modules

   ML Source Modules:
   - algorithms.sorting
   - algorithms.graph.dijkstra
   - algorithms.graph.bfs
   - utils.math_utils

Thread Safety
~~~~~~~~~~~~~

Module operations are thread-safe:

.. code-block:: python

   import threading

   def load_module(name):
       # Thread-safe module loading
       registry.load_module(name)

   # Concurrent module loading
   threads = [
       threading.Thread(target=load_module, args=("math",)),
       threading.Thread(target=load_module, args=("crypto",)),
       threading.Thread(target=load_module, args=("user_utils",))
   ]

   for t in threads:
       t.start()

   for t in threads:
       t.join()

**Guarantee:** No race conditions, each module loads exactly once.

----

Performance Monitoring
----------------------

Track module performance with built-in monitoring tools.

.perfmon Command
~~~~~~~~~~~~~~~~

Performance monitoring with module type breakdown:

.. code-block:: ml

   > .perfmon

   ═══════════════════════════════════════════════════════
   Module Performance Report
   ═══════════════════════════════════════════════════════

   Python Bridge Modules:
   ┌──────────────────┬────────────┬────────────┬─────────┐
   │ Module           │ Load Time  │ Reload     │ Memory  │
   ├──────────────────┼────────────┼────────────┼─────────┤
   │ math             │ 3.2ms      │ 0          │ 28KB    │
   │ datetime         │ 4.1ms      │ 0          │ 35KB    │
   │ crypto           │ 8.5ms ⚠️   │ 2          │ 52KB    │
   └──────────────────┴────────────┴────────────┴─────────┘

   ML Source Modules:
   ┌──────────────────┬────────────┬────────────┬─────────┐
   │ Module           │ Transp.    │ Reload     │ Memory  │
   ├──────────────────┼────────────┼────────────┼─────────┤
   │ user_utils       │ 15.3ms     │ 5          │ 18KB    │
   │ data_processing  │ 22.7ms     │ 1          │ 31KB    │
   │ algorithms.sort  │ 18.1ms     │ 0          │ 24KB    │
   └──────────────────┴────────────┴────────────┴─────────┘

   Summary:
   - Total modules: 6 (3 Python bridges, 3 ML sources)
   - Avg Python load time: 5.3ms
   - Avg ML transpile time: 18.7ms
   - Total memory: 188KB
   - Slowest module: crypto (8.5ms) ⚠️ SLOW

**Warnings:**

* ⚠️ SLOW - Module load/transpile > 5ms (Python) or > 20ms (ML)

Python API:
~~~~~~~~~~~

.. code-block:: python

   from src.mlpy.stdlib.builtin import performance_report

   # Get performance data
   report = performance_report()

   # Returns dict:
   # {
   #   "python_bridges": [
   #     {"name": "math", "load_time": 3.2, "reload_count": 0, ...},
   #     ...
   #   ],
   #   "ml_sources": [
   #     {"name": "user_utils", "transpilation_time": 15.3, ...},
   #     ...
   #   ],
   #   "summary": {
   #     "total_modules": 6,
   #     "avg_python_load": 5.3,
   #     "avg_ml_transpile": 18.7,
   #     "total_memory": 192512
   #   }
   # }

.memreport Command
~~~~~~~~~~~~~~~~~~

Memory usage report with module type breakdown:

.. code-block:: ml

   > .memreport

   ═══════════════════════════════════════════════════════
   Memory Usage Report
   ═══════════════════════════════════════════════════════

   By Module Type:
   ┌──────────────────┬─────────────┬────────────┐
   │ Type             │ Modules     │ Memory     │
   ├──────────────────┼─────────────┼────────────┤
   │ Python Bridges   │ 10          │ 345KB      │
   │ ML Sources       │ 8           │ 201KB      │
   └──────────────────┴─────────────┴────────────┘

   Top Memory Consumers:
   ┌──────────────────┬─────────────┬────────────┐
   │ Module           │ Type        │ Memory     │
   ├──────────────────┼─────────────┼────────────┤
   │ http             │ Python      │ 82KB       │
   │ datetime         │ Python      │ 58KB       │
   │ crypto           │ Python      │ 52KB       │
   │ data_processing  │ ML          │ 45KB       │
   │ algorithms.sort  │ ML          │ 38KB       │
   └──────────────────┴─────────────┴────────────┘

   Total Memory: 546KB
   Available: 15.4GB

**Python API:**

.. code-block:: python

   from src.mlpy.stdlib.builtin import memory_report

   report = memory_report()

   # Filter by type
   python_memory = report["by_type"]["python_bridges"]
   ml_memory = report["by_type"]["ml_sources"]

   # Top consumers
   top_5 = report["top_consumers"][:5]

Reload Count Tracking
~~~~~~~~~~~~~~~~~~~~~

Track how often modules are reloaded:

.. code-block:: python

   # Get reload stats
   info = registry.get_module_info("user_utils")
   print(f"Reloaded {info.reload_count} times")

   # High reload count indicates active development
   if info.reload_count > 10:
       print("Hot development detected!")

**Use Case:** Identify which modules are being actively developed.

Performance Targets
~~~~~~~~~~~~~~~~~~~

Recommended performance targets:

.. list-table:: Module Performance Targets
   :header-rows: 1
   :widths: 30 25 45

   * - Metric
     - Target
     - Notes
   * - Python bridge load
     - < 5ms
     - Simple modules should be instant
   * - ML module transpile
     - < 20ms
     - Cached after first load
   * - Module discovery
     - < 100ms
     - For 100 modules total
   * - Hot reload
     - < 500ms
     - Including retranspilation
   * - Memory per module
     - < 100KB
     - Unless handling large data

**Actual Performance (from testing):**

* ✅ Python bridge load: 1-4ms (avg 2.5ms)
* ✅ ML transpile: 15-25ms (avg 18ms)
* ✅ Module discovery: 45ms for 50 modules
* ✅ Hot reload: 180ms including retranspile

----

Summary
-------

Key Takeaways
~~~~~~~~~~~~~

1. **Unified Registry** manages both Python bridges and ML source modules
2. **Auto-Detection** discovers modules automatically (6 steps → 1 decorator)
3. **Lazy Loading** loads modules only when imported
4. **Hot Reloading** applies changes without restart (`.reload`)
5. **Type-Aware Monitoring** tracks performance by module type

Module Types Comparison
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Python Bridge vs ML Source Modules
   :header-rows: 1
   :widths: 30 35 35

   * - Feature
     - Python Bridge
     - ML Source
   * - **File Type**
     - ``.py`` with ``@ml_module``
     - ``.ml`` files
   * - **Load Process**
     - Import Python module
     - Transpile to Python
   * - **Load Time**
     - 1-5ms
     - 15-25ms
   * - **Hot Reload**
     - Re-import module
     - Retranspile + reload
   * - **Use Case**
     - Extend ML with Python libraries
     - User-defined ML utilities
   * - **Examples**
     - math, crypto, database
     - user_utils, algorithms

Performance Numbers to Remember
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Module discovery:   < 100ms for 100 modules
   Python load:        ~2.5ms average
   ML transpile:       ~18ms average
   Hot reload:         < 500ms including transpilation
   Memory per module:  ~30KB average

Next Steps
----------

Continue to :doc:`configuration` to learn about complete project configuration, environment variables, and multi-environment deployment strategies.

**Related Topics:**

* :doc:`configuration` - Complete configuration management
* :doc:`security` - Capability requirements for modules
* :doc:`../debugging/performance` - Module performance profiling
* :doc:`../debugging/diagnostic-tools` - `.perfmon`, `.memreport`, `.modinfo`

----

**Chapter Status:** ✅ Complete
**Reading Time:** ~35 minutes
**Complexity:** Intermediate
**Next Chapter:** :doc:`configuration`
