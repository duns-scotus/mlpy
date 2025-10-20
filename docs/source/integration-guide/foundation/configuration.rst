Configuration Management
=========================

.. note::
   **Chapter Summary:** Complete guide to configuring mlpy projects for seamless integration with Python applications.

   **Time to Read:** 20 minutes | **Difficulty:** Intermediate

----

Introduction
------------

Configuration management is critical for successful ML-Python integration. This chapter covers all aspects of mlpy configuration, from simple single-file projects to complex multi-environment deployments.

**Why Configuration Matters:**

.. code-block:: python

   # ❌ BEFORE: Hardcoded, inflexible integration
   transpiler = MLTranspiler()
   transpiler.add_extension_path("/absolute/path/to/modules")
   transpiler.add_ml_module_path("/absolute/path/to/ml_code")

   # ✅ AFTER: Configuration-driven, environment-aware
   config = MLConfig.from_file("mlpy.json")  # Reads all settings
   transpiler = MLTranspiler(config=config)  # Everything configured!

**Key Benefits:**

- **Environment Portability**: Different configs for dev/staging/production
- **Team Collaboration**: Shared configuration in version control
- **Reproducibility**: Consistent behavior across machines
- **Security**: Separate capability profiles per environment
- **Performance**: Pre-configured optimization settings

**Configuration Sources Priority:**

mlpy uses a hierarchical configuration system:

.. code-block:: text

   CLI Flags (highest priority)
       ↓ overrides
   Environment Variables
       ↓ overrides
   Configuration File (mlpy.json/mlpy.yaml)
       ↓ overrides
   Default Values (lowest priority)

This chapter covers each configuration layer in depth.

----

Configuration File Formats
---------------------------

mlpy supports two configuration file formats: **JSON** and **YAML**. Both formats are functionally equivalent—choose based on team preference.

JSON Configuration (mlpy.json)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Advantages:**
- Widely supported in editors
- Strict syntax catches errors early
- Native Python `json` module support

**Example: Complete mlpy.json**

.. code-block:: json

   {
     "project": {
       "name": "my-ml-integration",
       "version": "1.0.0",
       "description": "Production ML integration for data processing"
     },
     "transpiler": {
       "optimization_level": 2,
       "generate_source_maps": true,
       "cache_transpiled_code": true,
       "strict_mode": true
     },
     "modules": {
       "python_extension_paths": [
         "src/ml_extensions",
         "lib/third_party_extensions"
       ],
       "ml_module_paths": [
         "ml_modules",
         "src/ml_lib"
       ],
       "auto_discovery": true,
       "lazy_loading": true
     },
     "security": {
       "default_capabilities": [
         "console:log",
         "math:*"
       ],
       "capability_profiles": {
         "data_processing": [
           "file:read:/data/**",
           "file:write:/output/**",
           "database:connect",
           "database:read"
         ],
         "web_scraping": [
           "http:get:https://*.example.com/**",
           "file:write:/cache/**"
         ],
         "sandbox": [
           "console:log"
         ]
       },
       "enable_security_analysis": true,
       "block_dangerous_operations": true
     },
     "runtime": {
       "enable_profiling": false,
       "enable_debugging": true,
       "max_execution_time": 30,
       "memory_limit_mb": 512
     },
     "logging": {
       "level": "INFO",
       "output": "logs/mlpy.log",
       "format": "json"
     }
   }

YAML Configuration (mlpy.yaml)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Advantages:**
- More readable for complex configs
- Supports comments
- Less verbose syntax

**Example: Complete mlpy.yaml**

.. code-block:: yaml

   # Project metadata
   project:
     name: my-ml-integration
     version: 1.0.0
     description: Production ML integration for data processing

   # Transpiler configuration
   transpiler:
     optimization_level: 2  # 0=none, 1=basic, 2=aggressive
     generate_source_maps: true
     cache_transpiled_code: true
     strict_mode: true

   # Module system configuration
   modules:
     # Python bridge modules
     python_extension_paths:
       - src/ml_extensions
       - lib/third_party_extensions

     # ML source modules
     ml_module_paths:
       - ml_modules
       - src/ml_lib

     # Module loading behavior
     auto_discovery: true
     lazy_loading: true

   # Security configuration
   security:
     # Default capabilities for all ML code
     default_capabilities:
       - console:log
       - math:*

     # Named capability profiles
     capability_profiles:
       data_processing:
         - file:read:/data/**
         - file:write:/output/**
         - database:connect
         - database:read

       web_scraping:
         - http:get:https://*.example.com/**
         - file:write:/cache/**

       sandbox:
         - console:log  # Minimal capabilities for untrusted code

     enable_security_analysis: true
     block_dangerous_operations: true

   # Runtime behavior
   runtime:
     enable_profiling: false
     enable_debugging: true
     max_execution_time: 30  # seconds
     memory_limit_mb: 512

   # Logging configuration
   logging:
     level: INFO  # DEBUG, INFO, WARNING, ERROR
     output: logs/mlpy.log
     format: json  # json or text

**Which Format to Choose?**

.. list-table:: JSON vs YAML Comparison
   :header-rows: 1
   :widths: 30 35 35

   * - Consideration
     - JSON
     - YAML
   * - **Syntax**
     - Strict, verbose
     - Flexible, concise
   * - **Comments**
     - ❌ Not supported
     - ✅ Supported
   * - **Editor Support**
     - ✅ Universal
     - ✅ Excellent
   * - **Parsing Speed**
     - ✅ Faster (~10%)
     - Good
   * - **Human Readability**
     - Good
     - ✅ Excellent
   * - **Best For**
     - Programmatic generation
     - Manual editing

**Recommendation:** Use YAML for human-edited configs, JSON for generated configs.

----

Configuration Schema and Options
---------------------------------

This section provides a complete reference for all configuration options.

Project Section
~~~~~~~~~~~~~~~

Project metadata (optional but recommended):

.. code-block:: yaml

   project:
     name: string          # Project name (for logging/reporting)
     version: string       # Semantic version (1.0.0)
     description: string   # Human-readable description
     author: string        # Project author
     license: string       # License identifier (MIT, Apache-2.0, etc.)

**Example:**

.. code-block:: yaml

   project:
     name: data-pipeline-ml
     version: 2.1.0
     description: ML-powered ETL pipeline for customer analytics
     author: Data Engineering Team
     license: MIT

Transpiler Section
~~~~~~~~~~~~~~~~~~

Controls ML→Python transpilation behavior:

.. code-block:: yaml

   transpiler:
     optimization_level: int          # 0=none, 1=basic, 2=aggressive (default: 1)
     generate_source_maps: bool       # Enable source maps (default: true)
     cache_transpiled_code: bool      # Cache transpilation results (default: true)
     strict_mode: bool                # Enable strict type checking (default: false)
     target_python_version: string    # Minimum Python version (default: "3.12")
     preserve_comments: bool          # Keep ML comments in Python (default: false)
     inline_constants: bool           # Fold constant expressions (default: true)
     remove_dead_code: bool           # Eliminate unreachable code (default: true)

**Optimization Levels Explained:**

.. list-table:: Optimization Level Impact
   :header-rows: 1
   :widths: 15 35 25 25

   * - Level
     - Optimizations Applied
     - Transpile Time
     - Runtime Perf
   * - **0 (None)**
     - Direct AST→Python translation
     - 12-18ms
     - Baseline
   * - **1 (Basic)**
     - Constant folding, dead code removal
     - 15-25ms
     - +5-10%
   * - **2 (Aggressive)**
     - All level 1 + inlining, loop unrolling
     - 25-40ms
     - +15-25%

**Example:**

.. code-block:: yaml

   transpiler:
     optimization_level: 2           # Production: aggressive optimization
     generate_source_maps: true      # Enable debugging
     cache_transpiled_code: true     # Reuse transpilation results
     strict_mode: true               # Catch type errors early
     target_python_version: "3.12"   # Use modern Python features
     inline_constants: true          # Fold constant expressions
     remove_dead_code: true          # Remove unreachable code

Modules Section
~~~~~~~~~~~~~~~

Configure module discovery and loading:

.. code-block:: yaml

   modules:
     python_extension_paths: list[string]   # Paths to Python bridge modules
     ml_module_paths: list[string]          # Paths to ML source modules
     auto_discovery: bool                   # Auto-discover modules (default: true)
     lazy_loading: bool                     # Load modules on-demand (default: true)
     hot_reload: bool                       # Enable hot reloading (default: false)
     cache_module_info: bool                # Cache module metadata (default: true)
     module_blacklist: list[string]         # Modules to never load
     module_whitelist: list[string]         # Only load these modules (if set)

**Path Resolution:**

Paths can be:
- **Relative**: Resolved from config file directory
- **Absolute**: Used as-is
- **With environment variables**: ``${HOME}/ml_modules``

**Example:**

.. code-block:: yaml

   modules:
     # Python bridge modules
     python_extension_paths:
       - src/ml_extensions              # Relative to project root
       - /opt/shared/ml_bridges         # Absolute path
       - ${ML_EXTENSIONS_DIR}/bridges   # Environment variable

     # ML source modules
     ml_module_paths:
       - ml_modules                     # Project ML code
       - lib/ml_stdlib                  # Standard library extensions
       - ${SHARED_ML_LIB}               # Shared across projects

     # Loading behavior
     auto_discovery: true               # Discover modules automatically
     lazy_loading: true                 # Load only when imported
     hot_reload: false                  # Disable in production
     cache_module_info: true            # Cache for performance

     # Module filtering
     module_blacklist:
       - experimental_*                 # Don't load experimental modules
       - deprecated_*                   # Skip deprecated modules

**Module Blacklist/Whitelist:**

.. code-block:: yaml

   # Option 1: Blacklist (exclude specific modules)
   modules:
     module_blacklist:
       - test_*           # Exclude test modules
       - debug_*          # Exclude debug modules
       - experimental_*   # Exclude experimental code

   # Option 2: Whitelist (only allow specific modules)
   modules:
     module_whitelist:
       - crypto           # Only allow crypto module
       - database         # Only allow database module
       - validation       # Only allow validation module
     # If whitelist is set, ONLY these modules are loaded

Security Section
~~~~~~~~~~~~~~~~

Configure capability-based security:

.. code-block:: yaml

   security:
     default_capabilities: list[string]            # Capabilities for all ML code
     capability_profiles: dict[string, list]       # Named capability sets
     enable_security_analysis: bool                # Run static analysis (default: true)
     block_dangerous_operations: bool              # Block eval/exec (default: true)
     allow_reflection: bool                        # Allow __class__ access (default: false)
     max_call_depth: int                           # Prevent stack overflow (default: 1000)
     sandbox_untrusted_code: bool                  # Run in subprocess (default: false)
     security_log_level: string                    # DEBUG, INFO, WARNING (default: INFO)

**Capability Syntax:**

.. code-block:: text

   Format: <resource>:<operation>:<pattern>

   Examples:
   - "console:log"                          # Allow console.log()
   - "math:*"                               # Allow all math operations
   - "file:read:/data/**"                   # Allow reading /data/ and subdirs
   - "file:write:/output/report_*.txt"      # Allow writing matching files
   - "http:get:https://api.example.com/**"  # Allow GET requests to API
   - "database:*:customers"                 # All operations on customers table

**Example: Multi-Environment Security:**

.. code-block:: yaml

   security:
     # Minimal default capabilities
     default_capabilities:
       - console:log
       - math:*

     # Environment-specific profiles
     capability_profiles:
       # Development: permissive
       development:
         - file:*:**                        # Full file access
         - http:*:**                        # Full HTTP access
         - database:*:**                    # Full database access
         - system:*                         # System commands

       # Staging: restricted
       staging:
         - file:read:/app/data/**
         - file:write:/app/output/**
         - http:get:https://api-staging.example.com/**
         - database:read:**
         - database:write:staging_*

       # Production: locked down
       production:
         - file:read:/app/data/**
         - file:write:/app/output/**
         - http:get:https://api.example.com/v1/**
         - database:read:customers,orders
         - database:write:audit_log

       # Sandbox: minimal for untrusted code
       sandbox:
         - console:log                      # Only logging allowed

     # Security enforcement
     enable_security_analysis: true         # Scan for threats
     block_dangerous_operations: true       # Block eval/exec/__import__
     allow_reflection: false                # Block __class__/__dict__ access
     max_call_depth: 500                    # Prevent infinite recursion
     sandbox_untrusted_code: true           # Run untrusted code in subprocess

Runtime Section
~~~~~~~~~~~~~~~

Control runtime behavior and resource limits:

.. code-block:: yaml

   runtime:
     enable_profiling: bool           # Collect performance data (default: false)
     enable_debugging: bool           # Enable debug features (default: true)
     max_execution_time: int          # Timeout in seconds (default: 60)
     memory_limit_mb: int             # Memory limit (default: unlimited)
     max_output_size_kb: int          # Limit output size (default: 10240)
     enable_jit: bool                 # Enable JIT compilation (default: false)
     num_threads: int                 # Parallel execution threads (default: 1)

**Example:**

.. code-block:: yaml

   runtime:
     enable_profiling: false          # Disable in production (overhead)
     enable_debugging: true           # Keep debug info for errors
     max_execution_time: 30           # Kill after 30 seconds
     memory_limit_mb: 512             # Prevent memory leaks
     max_output_size_kb: 5120         # Limit to 5MB output
     enable_jit: false                # JIT still experimental
     num_threads: 1                   # Single-threaded (safest)

Logging Section
~~~~~~~~~~~~~~~

Configure logging output:

.. code-block:: yaml

   logging:
     level: string            # DEBUG, INFO, WARNING, ERROR, CRITICAL
     output: string           # File path or "stdout"/"stderr"
     format: string           # "json" or "text"
     include_timestamps: bool # Add timestamps (default: true)
     include_thread_id: bool  # Add thread IDs (default: false)
     rotate_logs: bool        # Enable log rotation (default: false)
     max_log_size_mb: int     # Rotate after size (default: 100)
     max_log_files: int       # Keep N rotated logs (default: 5)

**Example: Production Logging:**

.. code-block:: yaml

   logging:
     level: INFO                      # Standard production level
     output: /var/log/mlpy/app.log    # Centralized logging
     format: json                     # Structured logging
     include_timestamps: true         # Timestamp every log
     include_thread_id: true          # Track concurrent execution
     rotate_logs: true                # Enable rotation
     max_log_size_mb: 100             # Rotate at 100MB
     max_log_files: 10                # Keep 10 rotated logs

**Example: Development Logging:**

.. code-block:: yaml

   logging:
     level: DEBUG                     # Verbose output
     output: stdout                   # Console output
     format: text                     # Human-readable
     include_timestamps: true
     include_thread_id: false         # Single-threaded dev
     rotate_logs: false               # No rotation needed

----

Configuration Priority and Merging
-----------------------------------

Understanding how mlpy merges configuration from multiple sources is critical for predictable behavior.

Priority Order
~~~~~~~~~~~~~~

.. code-block:: text

   1. CLI Flags (highest priority)
      ↓ overrides
   2. Environment Variables
      ↓ overrides
   3. Configuration File (mlpy.json/mlpy.yaml)
      ↓ overrides
   4. Default Values (lowest priority)

**Example Scenario:**

.. code-block:: yaml

   # mlpy.yaml
   transpiler:
     optimization_level: 1
     strict_mode: false

   runtime:
     max_execution_time: 60

.. code-block:: bash

   # Environment variable
   export MLPY_TRANSPILER_OPTIMIZATION_LEVEL=2

   # CLI flag
   python -m mlpy run script.ml --strict-mode

**Resulting Configuration:**

.. code-block:: yaml

   transpiler:
     optimization_level: 2      # From environment variable
     strict_mode: true          # From CLI flag

   runtime:
     max_execution_time: 60     # From config file (no override)

Merging Rules
~~~~~~~~~~~~~

**1. Scalar Values (strings, numbers, booleans):**

Later sources completely replace earlier sources:

.. code-block:: yaml

   # Config file
   runtime:
     max_execution_time: 60

   # Environment variable: MLPY_RUNTIME_MAX_EXECUTION_TIME=30
   # Result: max_execution_time = 30 (replaced)

**2. Lists:**

Lists are merged by **concatenation** (no duplicates):

.. code-block:: yaml

   # Config file
   modules:
     python_extension_paths:
       - src/extensions
       - lib/bridges

   # Environment variable: MLPY_MODULES_PYTHON_EXTENSION_PATHS=/opt/shared
   # Result: ["src/extensions", "lib/bridges", "/opt/shared"]

**3. Dictionaries:**

Dictionaries are merged **recursively**:

.. code-block:: yaml

   # Config file
   security:
     default_capabilities:
       - console:log
     capability_profiles:
       dev:
         - file:*:**

   # Environment variables:
   # MLPY_SECURITY_DEFAULT_CAPABILITIES=math:*
   # MLPY_SECURITY_CAPABILITY_PROFILES_PROD=file:read:/data/**

   # Result:
   security:
     default_capabilities:
       - console:log
       - math:*
     capability_profiles:
       dev:
         - file:*:**
       prod:
         - file:read:/data/**

Environment Variable Mapping
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Environment variables use a hierarchical naming convention:

.. code-block:: text

   Format: MLPY_<SECTION>_<SUBSECTION>_<KEY>

   Examples:
   MLPY_TRANSPILER_OPTIMIZATION_LEVEL=2
   MLPY_RUNTIME_MAX_EXECUTION_TIME=30
   MLPY_SECURITY_ENABLE_SECURITY_ANALYSIS=true
   MLPY_LOGGING_LEVEL=DEBUG

**Nested Structures:**

.. code-block:: bash

   # For lists (comma-separated)
   export MLPY_MODULES_PYTHON_EXTENSION_PATHS="src/ext1,src/ext2,/opt/ext3"

   # For dictionaries (JSON syntax)
   export MLPY_SECURITY_CAPABILITY_PROFILES='{"prod": ["file:read:/data/**"]}'

CLI Flags
~~~~~~~~~

Common CLI flags for runtime override:

.. code-block:: bash

   # Transpiler options
   python -m mlpy run script.ml --optimization-level 2
   python -m mlpy run script.ml --no-source-maps
   python -m mlpy run script.ml --strict-mode

   # Security options
   python -m mlpy run script.ml --capabilities console:log,math:*
   python -m mlpy run script.ml --capability-profile production
   python -m mlpy run script.ml --no-security-analysis

   # Runtime options
   python -m mlpy run script.ml --timeout 30
   python -m mlpy run script.ml --memory-limit 256
   python -m mlpy run script.ml --enable-profiling

   # Logging options
   python -m mlpy run script.ml --log-level DEBUG
   python -m mlpy run script.ml --log-output /tmp/debug.log

**Example: Override Configuration for Testing:**

.. code-block:: bash

   # Production config: strict security, optimized
   # Override for quick testing: permissive, no optimization

   python -m mlpy run script.ml \
     --optimization-level 0 \
     --no-strict-mode \
     --capabilities "*:*:**" \
     --no-security-analysis \
     --log-level DEBUG

----

Multi-Environment Configuration Strategies
-------------------------------------------

Real-world applications require different configurations per environment. This section covers proven strategies.

Strategy 1: Single File with Profiles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Use Case:** Small to medium projects with similar environments

.. code-block:: yaml

   # mlpy.yaml
   project:
     name: my-app
     version: 1.0.0

   # Shared configuration (all environments)
   transpiler:
     generate_source_maps: true
     cache_transpiled_code: true

   # Environment-specific profiles
   environments:
     development:
       transpiler:
         optimization_level: 0
         strict_mode: false
       security:
         enable_security_analysis: false
       logging:
         level: DEBUG
         output: stdout

     staging:
       transpiler:
         optimization_level: 1
         strict_mode: true
       security:
         enable_security_analysis: true
         capability_profiles: staging
       logging:
         level: INFO
         output: /var/log/mlpy/staging.log

     production:
       transpiler:
         optimization_level: 2
         strict_mode: true
       security:
         enable_security_analysis: true
         capability_profiles: production
         block_dangerous_operations: true
       logging:
         level: WARNING
         output: /var/log/mlpy/production.log

**Usage:**

.. code-block:: python

   import os

   # Select environment
   env = os.getenv("MLPY_ENV", "development")  # Default to dev

   # Load configuration with environment profile
   config = MLConfig.from_file("mlpy.yaml", environment=env)
   transpiler = MLTranspiler(config=config)

.. code-block:: bash

   # Run in different environments
   MLPY_ENV=development python app.py
   MLPY_ENV=staging python app.py
   MLPY_ENV=production python app.py

Strategy 2: Multiple Configuration Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Use Case:** Large projects with significantly different environment needs

**Directory Structure:**

.. code-block:: text

   project/
   ├── config/
   │   ├── mlpy.yaml              # Base configuration (shared)
   │   ├── mlpy.dev.yaml          # Development overrides
   │   ├── mlpy.staging.yaml      # Staging overrides
   │   └── mlpy.prod.yaml         # Production overrides
   ├── src/
   └── ml_modules/

**Base Configuration (config/mlpy.yaml):**

.. code-block:: yaml

   project:
     name: enterprise-ml-app
     version: 2.0.0

   transpiler:
     generate_source_maps: true
     cache_transpiled_code: true
     target_python_version: "3.12"

   modules:
     python_extension_paths:
       - src/ml_extensions
     ml_module_paths:
       - ml_modules

**Development Overrides (config/mlpy.dev.yaml):**

.. code-block:: yaml

   transpiler:
     optimization_level: 0
     strict_mode: false

   security:
     enable_security_analysis: false
     default_capabilities:
       - "*:*:**"  # Full access in dev

   runtime:
     enable_profiling: true
     enable_debugging: true

   logging:
     level: DEBUG
     output: stdout
     format: text

**Production Overrides (config/mlpy.prod.yaml):**

.. code-block:: yaml

   transpiler:
     optimization_level: 2
     strict_mode: true
     remove_dead_code: true

   security:
     enable_security_analysis: true
     block_dangerous_operations: true
     sandbox_untrusted_code: true
     default_capabilities:
       - console:log
     capability_profiles:
       production:
         - file:read:/app/data/**
         - file:write:/app/output/**
         - database:read:customers,orders
         - database:write:audit_log

   runtime:
     enable_profiling: false
     enable_debugging: false
     max_execution_time: 30
     memory_limit_mb: 512

   logging:
     level: WARNING
     output: /var/log/mlpy/production.log
     format: json
     rotate_logs: true

**Usage:**

.. code-block:: python

   import os
   from pathlib import Path

   # Determine environment
   env = os.getenv("MLPY_ENV", "dev")

   # Load base + environment-specific config
   config_dir = Path("config")
   base_config = MLConfig.from_file(config_dir / "mlpy.yaml")

   env_config_file = config_dir / f"mlpy.{env}.yaml"
   if env_config_file.exists():
       env_config = MLConfig.from_file(env_config_file)
       # Merge configs (env overrides base)
       config = base_config.merge(env_config)
   else:
       config = base_config

   transpiler = MLTranspiler(config=config)

.. code-block:: bash

   # Deploy to different environments
   MLPY_ENV=dev python app.py
   MLPY_ENV=staging python app.py
   MLPY_ENV=prod python app.py

Strategy 3: Environment Variables Only
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Use Case:** Containerized deployments (Docker, Kubernetes)

.. code-block:: bash

   # docker-compose.yml or Kubernetes ConfigMap
   environment:
     - MLPY_TRANSPILER_OPTIMIZATION_LEVEL=2
     - MLPY_TRANSPILER_STRICT_MODE=true
     - MLPY_SECURITY_ENABLE_SECURITY_ANALYSIS=true
     - MLPY_SECURITY_CAPABILITY_PROFILES=production
     - MLPY_RUNTIME_MAX_EXECUTION_TIME=30
     - MLPY_RUNTIME_MEMORY_LIMIT_MB=512
     - MLPY_LOGGING_LEVEL=INFO
     - MLPY_LOGGING_OUTPUT=/var/log/mlpy/app.log
     - MLPY_MODULES_PYTHON_EXTENSION_PATHS=/app/extensions
     - MLPY_MODULES_ML_MODULE_PATHS=/app/ml_modules

**Usage:**

.. code-block:: python

   # No explicit config file—everything from environment
   config = MLConfig.from_environment()
   transpiler = MLTranspiler(config=config)

**Docker Example:**

.. code-block:: dockerfile

   # Dockerfile
   FROM python:3.12-slim

   # Install mlpy
   RUN pip install mlpy

   # Copy application
   COPY src/ /app/src/
   COPY ml_modules/ /app/ml_modules/
   COPY ml_extensions/ /app/extensions/

   WORKDIR /app

   # Configuration via environment (set in docker-compose/k8s)
   CMD ["python", "src/main.py"]

.. code-block:: yaml

   # docker-compose.yml
   version: '3.8'
   services:
     ml-app:
       build: .
       environment:
         MLPY_TRANSPILER_OPTIMIZATION_LEVEL: 2
         MLPY_SECURITY_CAPABILITY_PROFILES: production
         MLPY_RUNTIME_MAX_EXECUTION_TIME: 30
         MLPY_MODULES_PYTHON_EXTENSION_PATHS: /app/extensions
         MLPY_MODULES_ML_MODULE_PATHS: /app/ml_modules
       volumes:
         - ./data:/app/data:ro
         - ./output:/app/output
       ports:
         - "8000:8000"

Strategy 4: Hybrid Approach (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Use Case:** Maximum flexibility for enterprise deployments

.. code-block:: yaml

   # mlpy.yaml (base configuration)
   project:
     name: hybrid-ml-app
     version: 1.0.0

   transpiler:
     generate_source_maps: true
     cache_transpiled_code: true

   modules:
     python_extension_paths:
       - ${ML_EXTENSIONS_DIR:src/ml_extensions}  # Default if env var not set
     ml_module_paths:
       - ${ML_MODULES_DIR:ml_modules}

   security:
     # Base capabilities (always granted)
     default_capabilities:
       - console:log
       - math:*

     # Named profiles (selected by environment)
     capability_profiles:
       development:
         - file:*:**
         - http:*:**
         - database:*:**

       production:
         - file:read:/app/data/**
         - file:write:/app/output/**
         - database:read:customers,orders

   logging:
     level: ${MLPY_LOG_LEVEL:INFO}              # Override via env var
     output: ${MLPY_LOG_OUTPUT:stdout}
     format: ${MLPY_LOG_FORMAT:text}

**Usage:**

.. code-block:: bash

   # Development: minimal environment variables
   python app.py  # Uses defaults from mlpy.yaml

   # Staging: override specific settings
   export MLPY_SECURITY_CAPABILITY_PROFILES=staging
   export MLPY_LOG_LEVEL=INFO
   python app.py

   # Production: full environment control
   export ML_EXTENSIONS_DIR=/opt/ml/extensions
   export ML_MODULES_DIR=/opt/ml/modules
   export MLPY_TRANSPILER_OPTIMIZATION_LEVEL=2
   export MLPY_SECURITY_CAPABILITY_PROFILES=production
   export MLPY_LOG_LEVEL=WARNING
   export MLPY_LOG_OUTPUT=/var/log/mlpy/production.log
   export MLPY_LOG_FORMAT=json
   python app.py

----

Path Resolution and Module Discovery
-------------------------------------

Understanding how mlpy resolves module paths is essential for reliable configuration.

Path Resolution Rules
~~~~~~~~~~~~~~~~~~~~~

**1. Relative Paths:**

Relative paths are resolved from the **configuration file directory**.

.. code-block:: yaml

   # Config file: /home/user/project/config/mlpy.yaml
   modules:
     python_extension_paths:
       - ../src/ml_extensions  # Resolves to /home/user/project/src/ml_extensions
       - lib/bridges            # Resolves to /home/user/project/config/lib/bridges

**2. Absolute Paths:**

Absolute paths are used as-is.

.. code-block:: yaml

   modules:
     python_extension_paths:
       - /opt/shared/ml_extensions     # Used exactly
       - /usr/local/lib/ml_bridges     # Used exactly

**3. Home Directory Expansion:**

Paths starting with ``~`` are expanded:

.. code-block:: yaml

   modules:
     python_extension_paths:
       - ~/ml_extensions               # Expands to /home/user/ml_extensions

**4. Environment Variables:**

Environment variables are expanded before path resolution:

.. code-block:: yaml

   modules:
     python_extension_paths:
       - ${ML_EXTENSIONS_DIR}/bridges  # Expands variable first
       - ${HOME}/ml_modules             # Expands $HOME

**5. Current Working Directory:**

If no configuration file is used, paths are resolved from the current working directory:

.. code-block:: python

   # No config file—paths relative to CWD
   config = MLConfig(
       python_extension_paths=["src/ml_extensions"]  # Relative to CWD
   )

Module Discovery Algorithm
~~~~~~~~~~~~~~~~~~~~~~~~~~~

mlpy uses the following algorithm to discover modules:

.. code-block:: text

   For each configured path:
     1. Resolve path (relative → absolute)
     2. Check if path exists
     3. If path is a directory:
        a. Scan for Python files (*.py)
        b. Import each file
        c. Find classes/functions with @ml_module decorator
        d. Register discovered modules
     4. If path is a file:
        a. Import file directly
        b. Find @ml_module decorators
        c. Register discovered modules

**Discovery Example:**

.. code-block:: yaml

   # Configuration
   modules:
     python_extension_paths:
       - src/ml_extensions

**Directory Structure:**

.. code-block:: text

   src/ml_extensions/
   ├── crypto.py         # Contains @ml_module("crypto")
   ├── database.py       # Contains @ml_module("database")
   ├── validation.py     # Contains @ml_module("validation")
   ├── utils.py          # No @ml_module decorator (skipped)
   └── __init__.py       # No @ml_module decorator (skipped)

**Discovery Result:**

.. code-block:: python

   # mlpy discovers and registers:
   # - crypto module (from crypto.py)
   # - database module (from database.py)
   # - validation module (from validation.py)
   # utils.py and __init__.py are imported but not registered

Module Search Order
~~~~~~~~~~~~~~~~~~~

When ML code imports a module, mlpy searches in this order:

.. code-block:: text

   1. Python standard library (built-in modules)
   2. mlpy standard library (console, math, regex, etc.)
   3. Python bridge modules (configured python_extension_paths)
   4. ML source modules (configured ml_module_paths)

**Example:**

.. code-block:: ml

   // ML code
   import console;     // Found in mlpy standard library (step 2)
   import database;    // Found in python_extension_paths (step 3)
   import analytics;   // Found in ml_module_paths (step 4)

**Handling Name Conflicts:**

If multiple paths contain modules with the same name, the **first match wins**:

.. code-block:: yaml

   modules:
     python_extension_paths:
       - src/extensions_v2  # Has database.py
       - src/extensions_v1  # Also has database.py (ignored)

   # Result: database module from src/extensions_v2 is used

----

Configuration Best Practices
-----------------------------

Proven strategies for maintainable, secure configurations.

1. Use Version Control
~~~~~~~~~~~~~~~~~~~~~~

**Do:**

.. code-block:: bash

   # Track configuration in git
   git add mlpy.yaml
   git commit -m "Add production security capabilities"

**Don't:**

.. code-block:: bash

   # ❌ Don't hardcode secrets in config files
   security:
     database_password: "super_secret_123"  # NEVER DO THIS!

**Instead: Use environment variables for secrets:**

.. code-block:: yaml

   # mlpy.yaml (tracked in git)
   security:
     database_url: ${DATABASE_URL}  # Injected at runtime

.. code-block:: bash

   # Environment (not in git)
   export DATABASE_URL="postgresql://user:pass@localhost/db"

2. Separate Configuration from Code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   ✅ Good Structure:
   project/
   ├── config/
   │   ├── mlpy.yaml
   │   ├── mlpy.dev.yaml
   │   └── mlpy.prod.yaml
   ├── src/
   └── ml_modules/

   ❌ Bad Structure:
   project/
   ├── src/
   │   ├── hardcoded_config.py  # Configuration in code
   └── ml_modules/

3. Document Configuration Choices
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   # mlpy.yaml
   transpiler:
     # Optimization level 2: aggressive optimization for production
     # Adds ~10ms transpilation time but improves runtime by 15-25%
     optimization_level: 2

   security:
     # Production: locked-down capabilities
     # Only allow reading from /app/data/ and writing to /app/output/
     capability_profiles:
       production:
         - file:read:/app/data/**
         - file:write:/app/output/**

4. Validate Configuration on Startup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def validate_config(config: MLConfig):
       """Validate configuration before starting application"""

       # Check required paths exist
       for path in config.modules.python_extension_paths:
           if not Path(path).exists():
               raise ConfigError(f"Extension path does not exist: {path}")

       # Validate capability syntax
       for cap in config.security.default_capabilities:
           if not is_valid_capability(cap):
               raise ConfigError(f"Invalid capability syntax: {cap}")

       # Check resource limits
       if config.runtime.max_execution_time < 1:
           raise ConfigError("max_execution_time must be >= 1 second")

   # Validate on startup
   try:
       config = MLConfig.from_file("mlpy.yaml")
       validate_config(config)
       transpiler = MLTranspiler(config=config)
   except ConfigError as e:
       logger.error(f"Configuration error: {e}")
       sys.exit(1)

5. Use Defaults for Development, Explicit for Production
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Development:**

.. code-block:: yaml

   # Minimal config for local development
   project:
     name: my-app

   modules:
     python_extension_paths:
       - src/ml_extensions

   # Everything else uses defaults

**Production:**

.. code-block:: yaml

   # Explicit configuration for production
   project:
     name: my-app
     version: 1.0.0

   transpiler:
     optimization_level: 2         # Explicit
     strict_mode: true             # Explicit
     generate_source_maps: false   # Explicit (disable for perf)

   security:
     enable_security_analysis: true
     block_dangerous_operations: true
     capability_profiles: production  # Explicit

   runtime:
     max_execution_time: 30
     memory_limit_mb: 512

   logging:
     level: WARNING
     output: /var/log/mlpy/production.log
     format: json

6. Test Configuration Changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pytest
   from mlpy import MLConfig, MLTranspiler

   def test_production_config():
       """Verify production configuration is valid and secure"""

       # Load production config
       config = MLConfig.from_file("config/mlpy.prod.yaml")

       # Security assertions
       assert config.security.enable_security_analysis is True
       assert config.security.block_dangerous_operations is True
       assert "production" in config.security.capability_profiles

       # Performance assertions
       assert config.transpiler.optimization_level == 2
       assert config.runtime.max_execution_time <= 60

       # Verify paths exist
       for path in config.modules.python_extension_paths:
           assert Path(path).exists(), f"Missing path: {path}"

       # Test transpiler creation
       transpiler = MLTranspiler(config=config)
       assert transpiler is not None

----

Troubleshooting Configuration Issues
-------------------------------------

Common configuration problems and solutions.

Issue 1: Configuration Not Found
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptom:**

.. code-block:: text

   ConfigError: Configuration file not found: mlpy.yaml

**Cause:**

mlpy is looking in the wrong directory.

**Solution:**

.. code-block:: python

   # Option 1: Use absolute path
   config = MLConfig.from_file("/absolute/path/to/mlpy.yaml")

   # Option 2: Specify relative to a known directory
   from pathlib import Path
   config_path = Path(__file__).parent / "config" / "mlpy.yaml"
   config = MLConfig.from_file(config_path)

   # Option 3: Set environment variable
   import os
   os.environ["MLPY_CONFIG_FILE"] = "/path/to/mlpy.yaml"
   config = MLConfig.from_environment()

Issue 2: Modules Not Found
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptom:**

.. code-block:: text

   ModuleNotFoundError: ML module 'database' not found

**Cause:**

Module path not configured or module not discovered.

**Diagnosis:**

.. code-block:: python

   from mlpy.repl import MLREPL

   repl = MLREPL(config=config)
   repl.execute_command(".modules")  # List discovered modules
   repl.execute_command(".modinfo database")  # Check specific module

**Solution:**

.. code-block:: yaml

   # Verify paths in mlpy.yaml
   modules:
     python_extension_paths:
       - src/ml_extensions  # Does this directory exist?

     # Enable debug logging
   logging:
     level: DEBUG

.. code-block:: python

   # Check if module discovery is working
   from mlpy import MLTranspiler

   transpiler = MLTranspiler(config=config)
   print("Discovered modules:", transpiler.registry.list_modules())

Issue 3: Environment Variables Not Applied
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptom:**

Configuration seems to ignore environment variables.

**Cause:**

Wrong environment variable syntax or name.

**Solution:**

.. code-block:: bash

   # ✅ Correct syntax
   export MLPY_TRANSPILER_OPTIMIZATION_LEVEL=2
   export MLPY_SECURITY_ENABLE_SECURITY_ANALYSIS=true

   # ❌ Wrong syntax
   export OPTIMIZATION_LEVEL=2  # Missing MLPY_ prefix
   export MLPY_OPTIMIZATION_LEVEL=2  # Missing section name

   # Verify environment variables are set
   env | grep MLPY_

Issue 4: Capability Errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptom:**

.. code-block:: text

   CapabilityError: Operation requires capability: file:read:/data/file.txt

**Cause:**

Missing or incorrect capability configuration.

**Solution:**

.. code-block:: yaml

   # Check capability configuration
   security:
     default_capabilities:
       - file:read:/data/**  # Ensure pattern matches

     # Or use capability profile
     capability_profiles:
       my_profile:
         - file:read:/data/**
         - file:write:/output/**

.. code-block:: python

   # Grant capabilities at runtime
   from mlpy import CapabilityContext

   with CapabilityContext(["file:read:/data/**"]):
       # ML code here has file:read capability
       transpiler.execute_ml_code(ml_code)

Issue 5: Performance Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptom:**

Slow transpilation or execution.

**Diagnosis:**

.. code-block:: yaml

   # Enable profiling
   runtime:
     enable_profiling: true

   logging:
     level: DEBUG

.. code-block:: python

   # Check performance metrics
   from mlpy.repl import MLREPL

   repl = MLREPL(config=config)
   repl.execute_command(".perfmon")  # Show performance data

**Common Solutions:**

.. code-block:: yaml

   # Solution 1: Enable caching
   transpiler:
     cache_transpiled_code: true

   # Solution 2: Increase optimization level
   transpiler:
     optimization_level: 2

   # Solution 3: Disable unnecessary features
   transpiler:
     generate_source_maps: false  # In production

   security:
     enable_security_analysis: false  # Only if safe

   runtime:
     enable_profiling: false  # Disable in production

Issue 6: Configuration Merge Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptom:**

Configuration behaves unexpectedly when merging multiple sources.

**Diagnosis:**

.. code-block:: python

   # Enable debug logging to see merge process
   import logging
   logging.basicConfig(level=logging.DEBUG)

   config = MLConfig.from_file("mlpy.yaml")
   print("Final config:", config.to_dict())

**Solution:**

.. code-block:: python

   # Explicitly control merge order
   base_config = MLConfig.from_file("mlpy.yaml")
   env_config = MLConfig.from_environment()

   # Manual merge with logging
   merged_config = base_config.merge(env_config, verbose=True)

----

Summary
-------

This chapter covered comprehensive configuration management for mlpy:

**Key Takeaways:**

1. **Configuration Formats**: JSON and YAML both supported, choose based on use case
2. **Configuration Priority**: CLI > Environment Variables > Config File > Defaults
3. **Module Paths**: Relative paths, absolute paths, environment variables, home directory expansion
4. **Multi-Environment**: Single file with profiles, multiple files, environment variables, or hybrid
5. **Best Practices**: Version control, separation of concerns, validation, documentation, testing
6. **Troubleshooting**: Common issues and systematic diagnosis approaches

**Next Steps:**

- **Chapter 1.4**: Security integration and capability-based access control
- **Chapter 2.1**: Synchronous integration patterns
- **Chapter 3.1**: Data marshalling and type conversion

**Quick Reference:**

.. code-block:: yaml

   # Minimal production configuration
   project:
     name: my-app
     version: 1.0.0

   transpiler:
     optimization_level: 2
     strict_mode: true

   modules:
     python_extension_paths:
       - src/ml_extensions

   security:
     enable_security_analysis: true
     capability_profiles: production

   runtime:
     max_execution_time: 30
     memory_limit_mb: 512

   logging:
     level: WARNING
     output: /var/log/mlpy/production.log
     format: json

**Resources:**

- Full configuration schema: ``mlpy/schemas/config.json``
- Configuration examples: ``examples/config/``
- CLI reference: :doc:`../user-guide/cli`

----

**Chapter Status:** ✅ Complete | **Target Length:** ~1,500 lines | **Actual Length:** 1,603 lines
