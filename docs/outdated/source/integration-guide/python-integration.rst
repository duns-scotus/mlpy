==================
Python Integration
==================

Embed mlpy transpiler in Python applications for dynamic ML code execution, secure scripting, and bidirectional Python-ML interactions.

.. contents:: Integration Patterns
   :local:
   :depth: 3

Overview
========

The mlpy transpiler provides a powerful Python API for integrating ML code execution into your applications. This guide covers all core integration patterns from basic transpilation to complex bidirectional interactions.

**Key Integration Benefits:**

- **Secure Execution**: Capability-based security with sandboxing
- **Dynamic Compilation**: Runtime transpilation of ML code
- **Bidirectional Interaction**: Python ↔ ML function calls and data sharing
- **Performance**: Efficient transpilation with caching support
- **Error Handling**: Comprehensive error reporting and recovery

Core Integration Patterns
==========================

1. Basic Transpilation
----------------------

The simplest integration pattern: transpile ML code to Python and handle results.

### Quick Start Example

.. code-block:: python

   from mlpy.ml.transpiler import transpile_ml_code

   # Simple ML code
   ml_source = '''
   function greet(name) {
       return "Hello, " + name + "!";
   }

   message = greet("World");
   print(message);
   '''

   # Transpile to Python
   python_code, issues, source_map = transpile_ml_code(
       source_code=ml_source,
       source_file="example.ml",
       strict_security=True
   )

   if python_code:
       print("✅ Transpilation successful!")
       # Execute the generated Python code
       exec(python_code)
   else:
       print("❌ Transpilation failed:")
       for issue in issues:
           print(f"  - {issue.error.message}")

### File-Based Transpilation

.. code-block:: python

   from mlpy.ml.transpiler import transpile_ml_file
   from pathlib import Path

   def transpile_ml_project(project_dir):
       """Transpile all ML files in a project directory."""
       project_path = Path(project_dir)

       for ml_file in project_path.glob("**/*.ml"):
           output_file = ml_file.with_suffix(".py")

           python_code, issues, source_map = transpile_ml_file(
               file_path=str(ml_file),
               output_path=str(output_file),
               strict_security=True,
               generate_source_maps=True
           )

           if python_code:
               print(f"✅ {ml_file.name} → {output_file.name}")
               # Python code is automatically written to output_file
           else:
               print(f"❌ Failed to transpile {ml_file.name}:")
               for issue in issues:
                   print(f"  - Line {issue.location.line}: {issue.error.message}")

### Security Validation Only

.. code-block:: python

   from mlpy.ml.transpiler import validate_ml_security

   def validate_user_script(user_ml_code):
       """Validate ML code security without transpiling."""
       security_issues = validate_ml_security(
           source_code=user_ml_code,
           source_file="user_script.ml"
       )

       if not security_issues:
           return True, "Script is secure"

       # Categorize security issues
       critical_issues = [issue for issue in security_issues
                         if issue.severity == "critical"]

       if critical_issues:
           return False, f"Critical security issues found: {len(critical_issues)}"

       return True, f"Minor security warnings: {len(security_issues)}"

2. Sandbox Execution
--------------------

Execute ML code in a secure sandbox with resource limits and capability controls.

### Basic Sandboxed Execution

.. code-block:: python

   from mlpy.ml.transpiler import execute_ml_code_sandbox
   from mlpy.runtime.sandbox import SandboxConfig

   def run_user_script_safely(ml_code, max_runtime=5.0):
       """Execute user-provided ML code with safety limits."""

       # Configure sandbox limits
       sandbox_config = SandboxConfig(
           max_execution_time=max_runtime,
           max_memory_mb=100,
           allow_network=False,
           allow_file_system=False,
           temp_dir_only=True
       )

       # Execute with sandbox
       result = execute_ml_code_sandbox(
           source_code=ml_code,
           source_file="user_script.ml",
           capabilities=["execute:calculations"],  # Minimal capabilities
           sandbox_config=sandbox_config
       )

       if result.success:
           return {
               "output": result.output,
               "execution_time": result.execution_time,
               "memory_used": result.memory_used
           }
       else:
           return {
               "error": result.error,
               "security_violations": result.security_issues
           }

### Advanced Sandbox Configuration

.. code-block:: python

   from mlpy.runtime.sandbox import SandboxConfig, SandboxResult
   from mlpy.runtime.capabilities.tokens import CapabilityToken

   class MLScriptRunner:
       """Advanced ML script runner with configurable security."""

       def __init__(self, trusted_mode=False):
           self.trusted_mode = trusted_mode
           self.results_cache = {}

       def create_sandbox_config(self, script_type):
           """Create sandbox config based on script type."""

           if script_type == "data_processing":
               return SandboxConfig(
                   max_execution_time=30.0,
                   max_memory_mb=500,
                   allow_network=False,
                   allow_file_system=True,
                   allowed_file_patterns=["./data/**/*.csv", "./output/**/*"],
                   max_file_operations=1000
               )

           elif script_type == "web_service":
               return SandboxConfig(
                   max_execution_time=5.0,
                   max_memory_mb=50,
                   allow_network=True,
                   allowed_domains=["api.example.com"],
                   rate_limit_requests=100
               )

           else:  # Default: minimal permissions
               return SandboxConfig(
                   max_execution_time=1.0,
                   max_memory_mb=25,
                   allow_network=False,
                   allow_file_system=False
               )

       def execute_script(self, ml_code, script_type="default", context_data=None):
           """Execute ML script with appropriate security settings."""

           sandbox_config = self.create_sandbox_config(script_type)

           # Add context data to the execution environment
           if context_data:
               # Inject context as ML variables
               ml_code = self._inject_context_data(ml_code, context_data)

           result = execute_ml_code_sandbox(
               source_code=ml_code,
               capabilities=self._get_capabilities_for_type(script_type),
               sandbox_config=sandbox_config
           )

           return self._process_sandbox_result(result)

       def _inject_context_data(self, ml_code, context_data):
           """Inject Python context data as ML variables."""
           context_ml = []
           for key, value in context_data.items():
               if isinstance(value, str):
                   context_ml.append(f'{key} = "{value}";')
               elif isinstance(value, (int, float)):
                   context_ml.append(f'{key} = {value};')
               elif isinstance(value, list):
                   items = ', '.join(f'"{item}"' if isinstance(item, str) else str(item)
                                   for item in value)
                   context_ml.append(f'{key} = [{items}];')

           return '\n'.join(context_ml) + '\n\n' + ml_code

3. MLTranspiler Class Usage
---------------------------

Direct usage of the MLTranspiler class for advanced control over the transpilation process.

### Custom Transpiler Instance

.. code-block:: python

   from mlpy.ml.transpiler import MLTranspiler
   from mlpy.ml.errors.context import ErrorContext

   class ProjectMLCompiler:
       """Custom ML compiler for a specific project."""

       def __init__(self, project_config):
           self.transpiler = MLTranspiler()
           self.project_config = project_config
           self.compilation_cache = {}

       def compile_module(self, module_name, ml_source):
           """Compile an ML module with project-specific settings."""

           # Check cache first
           cache_key = f"{module_name}:{hash(ml_source)}"
           if cache_key in self.compilation_cache:
               return self.compilation_cache[cache_key]

           # Parse with security analysis
           ast, security_issues = self.transpiler.parse_with_security_analysis(
               source_code=ml_source,
               source_file=f"{module_name}.ml"
           )

           if ast is None:
               return {"success": False, "error": "Parsing failed"}

           # Apply project security policy
           if not self._validate_project_security(security_issues):
               return {"success": False, "security_issues": security_issues}

           # Transpile to Python
           python_code, trans_issues, source_map = self.transpiler.transpile_to_python(
               source_code=ml_source,
               source_file=f"{module_name}.ml",
               strict_security=self.project_config.get("strict_security", True),
               generate_source_maps=True
           )

           result = {
               "success": python_code is not None,
               "python_code": python_code,
               "source_map": source_map,
               "issues": trans_issues,
               "ast": ast
           }

           # Cache successful compilations
           if result["success"]:
               self.compilation_cache[cache_key] = result

           return result

       def _validate_project_security(self, security_issues):
           """Apply project-specific security validation."""
           policy = self.project_config.get("security_policy", "strict")

           if policy == "permissive":
               # Allow warnings, block only critical issues
               return not any(issue.severity == "critical" for issue in security_issues)

           elif policy == "strict":
               # Block any security issues
               return len(security_issues) == 0

           else:  # custom policy
               # Apply custom validation logic
               return self.project_config["security_validator"](security_issues)

4. Data Sharing Patterns
------------------------

Share data between Python and ML code execution environments.

### Context Data Injection

.. code-block:: python

   def execute_ml_with_context(ml_code, python_context):
       """Execute ML code with Python data context."""

       # Convert Python data to ML variable declarations
       context_declarations = []
       for key, value in python_context.items():
           if isinstance(value, dict):
               # Convert Python dict to ML object
               ml_obj = _python_dict_to_ml_object(value)
               context_declarations.append(f"{key} = {ml_obj};")
           elif isinstance(value, list):
               # Convert Python list to ML array
               ml_array = _python_list_to_ml_array(value)
               context_declarations.append(f"{key} = {ml_array};")
           else:
               # Simple values
               context_declarations.append(f"{key} = {repr(value)};")

       # Prepend context to ML code
       full_ml_code = '\n'.join(context_declarations) + '\n' + ml_code

       # Execute and capture results
       python_code, issues, source_map = transpile_ml_code(full_ml_code)

       if python_code:
           # Execute with result capture
           result_namespace = {}
           exec(python_code, {"__builtins__": __builtins__}, result_namespace)
           return result_namespace

       return None

   def _python_dict_to_ml_object(py_dict):
       """Convert Python dictionary to ML object literal."""
       items = []
       for key, value in py_dict.items():
           if isinstance(value, str):
               items.append(f'{key}: "{value}"')
           else:
               items.append(f'{key}: {value}')
       return "{" + ", ".join(items) + "}"

   def _python_list_to_ml_array(py_list):
       """Convert Python list to ML array literal."""
       items = []
       for item in py_list:
           if isinstance(item, str):
               items.append(f'"{item}"')
           else:
               items.append(str(item))
       return "[" + ", ".join(items) + "]"

### Standard Library Bridge Usage

.. code-block:: python

   def demonstrate_stdlib_bridge():
       """Show how ML code uses Python standard library functions."""

       ml_code = '''
       import collections;
       import math;
       import random;

       // Use Python implementations via ML interface
       numbers = [1, 2, 3, 4, 5];
       doubled = collections.map(numbers, function(x) { return x * 2; });
       total = collections.reduce(doubled, function(a, b) { return a + b; }, 0);

       sqrt_total = math.sqrt(total);
       random_factor = random.randomFloat();

       result = sqrt_total * random_factor;
       print("Final result: " + result);
       '''

       # This ML code automatically uses Python implementations
       # through the mlpy.stdlib bridge system
       python_code, issues, _ = transpile_ml_code(ml_code)

       if python_code:
           print("Generated Python with stdlib bridges:")
           print(python_code)
           exec(python_code)

5. Python / ML Interaction
--------------------------

Bidirectional interaction patterns between Python and ML code.

### Python → ML Callbacks

Expose Python functions for ML code to call during execution.

.. code-block:: python

   class MLCallbackHandler:
       """Handle callbacks from ML code to Python functions."""

       def __init__(self):
           self.callback_registry = {}
           self.call_history = []

       def register_callback(self, name, python_function, capabilities=None):
           """Register a Python function as ML-callable."""
           self.callback_registry[name] = {
               "function": python_function,
               "capabilities": capabilities or [],
               "call_count": 0
           }

       def create_ml_environment(self, ml_code):
           """Create ML code with registered callbacks available."""

           # Generate ML function declarations for Python callbacks
           callback_declarations = []
           for name, info in self.callback_registry.items():
               # Create ML function that calls Python callback
               callback_declarations.append(f'''
               function {name}(...args) {{
                   // This function bridges to Python callback
                   return __python_callback("{name}", args);
               }}
               ''')

           # Combine callbacks with user ML code
           full_ml_code = '\n'.join(callback_declarations) + '\n' + ml_code

           return full_ml_code

       def execute_with_callbacks(self, ml_code):
           """Execute ML code with Python callback support."""

           # Prepare ML code with callbacks
           enhanced_ml_code = self.create_ml_environment(ml_code)

           # Transpile to Python
           python_code, issues, _ = transpile_ml_code(enhanced_ml_code)

           if python_code:
               # Create execution environment with callback handler
               callback_env = self._create_callback_environment()

               try:
                   exec(python_code, callback_env)
                   return {"success": True, "calls": self.call_history}
               except Exception as e:
                   return {"success": False, "error": str(e)}

           return {"success": False, "transpilation_issues": issues}

       def _create_callback_environment(self):
           """Create Python execution environment with callback support."""

           def python_callback_handler(callback_name, args):
               """Handle ML calls to Python functions."""
               if callback_name in self.callback_registry:
                   info = self.callback_registry[callback_name]

                   # Record call
                   call_record = {
                       "function": callback_name,
                       "args": args,
                       "timestamp": time.time()
                   }
                   self.call_history.append(call_record)

                   # Update call count
                   info["call_count"] += 1

                   # Execute Python function
                   try:
                       return info["function"](*args)
                   except Exception as e:
                       raise RuntimeError(f"Callback {callback_name} failed: {e}")

               else:
                   raise RuntimeError(f"Unknown callback: {callback_name}")

           return {
               "__builtins__": __builtins__,
               "__python_callback": python_callback_handler,
               # Add mlpy stdlib
               "print": print,
               **self._get_stdlib_environment()
           }

   # Usage example
   def example_python_callbacks():
       """Demonstrate Python → ML callback pattern."""

       handler = MLCallbackHandler()

       # Register Python functions as ML callbacks
       handler.register_callback("fetch_data", fetch_user_data)
       handler.register_callback("log_event", log_analytics_event)
       handler.register_callback("validate_input", validate_business_rules)

       # ML code that calls Python functions
       ml_script = '''
       // ML script using Python callbacks
       user_id = 123;
       user_data = fetch_data(user_id);

       if (validate_input(user_data.email)) {
           log_event("user_login", user_data.email);
           print("User logged in: " + user_data.name);
       } else {
           log_event("invalid_login_attempt", user_id);
           print("Invalid login attempt");
       }
       '''

       result = handler.execute_with_callbacks(ml_script)
       print(f"Execution result: {result}")

### ML → Python Bridge Extensions

Extend the standard library bridge system with custom modules.

.. code-block:: python

   from mlpy.stdlib.registry import StandardLibraryRegistry, BridgeFunction

   class CustomMLBridge:
       """Create custom ML → Python bridges."""

       def __init__(self):
           self.registry = StandardLibraryRegistry()
           self._register_custom_modules()

       def _register_custom_modules(self):
           """Register custom modules with the ML standard library."""

           # Register a custom database module
           self.registry.register_module(
               name="database",
               source_file="database.ml",  # Would contain ML interface
               capabilities_required=["read:database", "write:database"],
               description="Database operations with ORM",
               python_bridge_modules=["sqlalchemy", "psycopg2"]
           )

           # Register bridge functions for database module
           db_functions = [
               ("connect", "custom_bridges.database", "create_connection", ["read:database"]),
               ("query", "custom_bridges.database", "execute_query", ["read:database"]),
               ("insert", "custom_bridges.database", "insert_record", ["write:database"]),
               ("update", "custom_bridges.database", "update_record", ["write:database"]),
           ]

           for ml_name, py_module, py_func, caps in db_functions:
               self.registry.register_bridge_function(
                   module_name="database",
                   ml_name=ml_name,
                   python_module=py_module,
                   python_function=py_func,
                   capabilities_required=caps
               )

       def execute_ml_with_custom_modules(self, ml_code):
           """Execute ML code with access to custom bridge modules."""

           # ML code can now use: import database; database.query(...);
           python_code, issues, _ = transpile_ml_code(ml_code)

           if python_code:
               # The generated Python code will automatically use our bridges
               # through the registry system
               exec(python_code)
               return True

           return False

   # Custom bridge implementation
   # custom_bridges/database.py
   """
   import sqlalchemy
   from typing import Any, Dict, List

   _connection = None

   def create_connection(database_url: str) -> bool:
       global _connection
       try:
           _connection = sqlalchemy.create_engine(database_url)
           return True
       except Exception:
           return False

   def execute_query(sql: str) -> List[Dict[str, Any]]:
       if not _connection:
           raise RuntimeError("No database connection")

       result = _connection.execute(sqlalchemy.text(sql))
       return [dict(row) for row in result]

   def insert_record(table: str, data: Dict[str, Any]) -> bool:
       # Implementation with capability checks
       pass
   """

### Bidirectional Data Flow

Complex patterns for data flowing between Python and ML in both directions.

.. code-block:: python

   class MLPythonBridge:
       """Advanced bidirectional Python ↔ ML interaction."""

       def __init__(self):
           self.shared_state = {}
           self.ml_callbacks = MLCallbackHandler()
           self.data_transformers = {}

       def setup_bidirectional_bridge(self):
           """Set up bidirectional data flow."""

           # Python → ML: Data injection
           self.ml_callbacks.register_callback("get_shared_data", self._get_shared_data)
           self.ml_callbacks.register_callback("set_shared_data", self._set_shared_data)

           # ML → Python: Result collection
           self.ml_callbacks.register_callback("emit_result", self._collect_ml_result)
           self.ml_callbacks.register_callback("emit_event", self._handle_ml_event)

       def _get_shared_data(self, key):
           """Provide Python data to ML code."""
           return self.shared_state.get(key)

       def _set_shared_data(self, key, value):
           """Receive data from ML code."""
           self.shared_state[key] = value
           return True

       def _collect_ml_result(self, result_type, data):
           """Collect results from ML computation."""
           if result_type not in self.shared_state:
               self.shared_state[result_type] = []
           self.shared_state[result_type].append(data)

       def _handle_ml_event(self, event_type, event_data):
           """Handle events emitted by ML code."""
           print(f"ML Event: {event_type} - {event_data}")
           # Could trigger Python-side event handlers

       def run_interactive_ml_session(self, ml_code):
           """Run ML code with full bidirectional interaction."""

           # Set up initial shared state
           self.shared_state.update({
               "config": {"debug": True, "max_iterations": 100},
               "input_data": [1, 2, 3, 4, 5],
               "results": []
           })

           # Execute ML code with bidirectional bridge
           result = self.ml_callbacks.execute_with_callbacks(ml_code)

           return {
               "execution_success": result["success"],
               "final_state": self.shared_state,
               "interaction_history": self.ml_callbacks.call_history
           }

   # Example usage
   def demo_bidirectional_interaction():
       """Demonstrate complex Python ↔ ML interaction."""

       bridge = MLPythonBridge()
       bridge.setup_bidirectional_bridge()

       ml_algorithm = '''
       // ML algorithm with Python interaction
       config = get_shared_data("config");
       input_data = get_shared_data("input_data");

       emit_event("algorithm_start", "Processing " + input_data.length + " items");

       processed_data = [];
       for (i = 0; i < input_data.length; i = i + 1) {
           value = input_data[i];
           processed_value = value * value;
           processed_data = collections.append(processed_data, processed_value);

           emit_event("item_processed", {"index": i, "value": processed_value});
       }

       emit_result("processed_data", processed_data);
       set_shared_data("final_count", processed_data.length);

       emit_event("algorithm_complete", "Processing finished");
       '''

       result = bridge.run_interactive_ml_session(ml_algorithm)
       print("Final result:", result)

Integration Examples
====================

1. Configuration Processing with ML
-----------------------------------

Use ML as a secure configuration language with validation and dynamic loading.

.. code-block:: python

   from mlpy.ml.transpiler import transpile_ml_code, validate_ml_security
   from pathlib import Path
   import json

   class MLConfigProcessor:
       """Process configuration files written in ML."""

       def __init__(self, config_dir="./config"):
           self.config_dir = Path(config_dir)
           self.loaded_configs = {}

       def load_config(self, config_name):
           """Load and validate ML configuration file."""
           config_file = self.config_dir / f"{config_name}.ml"

           if not config_file.exists():
               raise FileNotFoundError(f"Config file not found: {config_file}")

           ml_config = config_file.read_text()

           # Security validation first
           security_issues = validate_ml_security(ml_config, str(config_file))
           if security_issues:
               raise SecurityError(f"Config security issues: {security_issues}")

           # Transpile and execute config
           python_code, issues, _ = transpile_ml_code(
               source_code=ml_config,
               source_file=str(config_file),
               strict_security=True
           )

           if not python_code:
               raise ValueError(f"Config compilation failed: {issues}")

           # Execute config in controlled environment
           config_globals = {"__builtins__": {}}
           config_locals = {}

           exec(python_code, config_globals, config_locals)

           # Extract configuration values
           config_data = {k: v for k, v in config_locals.items()
                         if not k.startswith('__')}

           self.loaded_configs[config_name] = config_data
           return config_data

       def get_config_value(self, config_name, key_path, default=None):
           """Get nested configuration value using dot notation."""
           if config_name not in self.loaded_configs:
               self.load_config(config_name)

           config = self.loaded_configs[config_name]

           # Navigate nested keys: "database.connection.host"
           keys = key_path.split('.')
           value = config

           for key in keys:
               if isinstance(value, dict) and key in value:
                   value = value[key]
               else:
                   return default

           return value

   # Example ML configuration file (config/database.ml)
   """
   // database.ml - Database configuration in ML

   database = {
       connection: {
           host: "localhost",
           port: 5432,
           name: "myapp_production"
       },
       pool: {
           min_connections: 2,
           max_connections: 20,
           timeout: 30
       }
   };

   cache = {
       type: "redis",
       host: "cache.example.com",
       ttl: 3600
   };

   features = {
       enable_logging: true,
       debug_mode: false,
       max_upload_size: 10 * 1024 * 1024  // 10MB
   };
   """

   # Usage
   config_processor = MLConfigProcessor()
   db_host = config_processor.get_config_value("database", "database.connection.host")
   max_conns = config_processor.get_config_value("database", "database.pool.max_connections")

2. Dynamic Scripting in Python Apps
------------------------------------

Create plugin systems and user-defined business logic using ML scripts.

.. code-block:: python

   from mlpy.ml.transpiler import MLTranspiler, execute_ml_code_sandbox
   from mlpy.runtime.sandbox import SandboxConfig
   import importlib
   import tempfile
   from pathlib import Path

   class MLPluginSystem:
       """Plugin system using ML scripts for business logic."""

       def __init__(self, plugins_dir="./plugins"):
           self.plugins_dir = Path(plugins_dir)
           self.plugins_dir.mkdir(exist_ok=True)
           self.loaded_plugins = {}
           self.transpiler = MLTranspiler()

       def install_plugin(self, plugin_name, ml_source, plugin_config=None):
           """Install a new ML plugin."""

           # Validate plugin security
           security_issues = self.transpiler.validate_security_only(ml_source)
           if any(issue.severity == "critical" for issue in security_issues):
               raise SecurityError("Plugin contains critical security issues")

           # Save plugin source
           plugin_file = self.plugins_dir / f"{plugin_name}.ml"
           plugin_file.write_text(ml_source)

           # Transpile to Python for faster loading
           python_code, issues, source_map = self.transpiler.transpile_to_python(
               source_code=ml_source,
               source_file=str(plugin_file)
           )

           if not python_code:
               raise ValueError(f"Plugin compilation failed: {issues}")

           # Save transpiled Python
           python_file = self.plugins_dir / f"{plugin_name}.py"
           python_file.write_text(python_code)

           # Register plugin
           self.loaded_plugins[plugin_name] = {
               "ml_source": ml_source,
               "python_code": python_code,
               "source_map": source_map,
               "config": plugin_config or {},
               "installed": True
           }

           return True

       def execute_plugin(self, plugin_name, input_data=None, context=None):
           """Execute a plugin with input data and context."""

           if plugin_name not in self.loaded_plugins:
               self._load_plugin(plugin_name)

           plugin = self.loaded_plugins[plugin_name]

           # Create plugin execution environment
           plugin_env = {
               "__builtins__": __builtins__,
               "input_data": input_data,
               "context": context or {},
               "plugin_config": plugin.get("config", {})
           }

           # Execute plugin in sandbox
           sandbox_config = SandboxConfig(
               max_execution_time=10.0,
               max_memory_mb=100,
               allow_network=plugin["config"].get("allow_network", False)
           )

           result = execute_ml_code_sandbox(
               source_code=plugin["ml_source"],
               capabilities=plugin["config"].get("capabilities", []),
               context=plugin_env,
               sandbox_config=sandbox_config
           )

           return {
               "success": result.success,
               "output": result.output,
               "error": result.error,
               "execution_time": result.execution_time
           }

       def list_plugins(self):
           """List all available plugins."""
           plugins = []

           for ml_file in self.plugins_dir.glob("*.ml"):
               plugin_name = ml_file.stem
               plugins.append({
                   "name": plugin_name,
                   "file": str(ml_file),
                   "loaded": plugin_name in self.loaded_plugins
               })

           return plugins

       def _load_plugin(self, plugin_name):
           """Load plugin from disk."""
           plugin_file = self.plugins_dir / f"{plugin_name}.ml"

           if not plugin_file.exists():
               raise FileNotFoundError(f"Plugin not found: {plugin_name}")

           ml_source = plugin_file.read_text()
           self.install_plugin(plugin_name, ml_source)

   # Example plugin (plugins/data_validator.ml)
   """
   // data_validator.ml - Data validation plugin

   function validate_email(email) {
       // Simple email validation
       if (email.indexOf("@") == -1) {
           return false;
       }
       if (email.indexOf(".") == -1) {
           return false;
       }
       return true;
   }

   function validate_user_data(user_data) {
       errors = [];

       if (!user_data.name || user_data.name.length < 2) {
           errors = collections.append(errors, "Name must be at least 2 characters");
       }

       if (!validate_email(user_data.email)) {
           errors = collections.append(errors, "Invalid email format");
       }

       if (user_data.age < 13 || user_data.age > 120) {
           errors = collections.append(errors, "Age must be between 13 and 120");
       }

       return {
           valid: errors.length == 0,
           errors: errors
       };
   }

   // Main plugin execution
   validation_result = validate_user_data(input_data);
   plugin_output = validation_result;
   """

   # Usage
   plugin_system = MLPluginSystem()

   # User registration validation
   user_data = {"name": "John", "email": "john@example.com", "age": 25}
   result = plugin_system.execute_plugin("data_validator", user_data)

   if result["success"] and result["output"]["valid"]:
       print("User data is valid")
   else:
       print("Validation errors:", result["output"]["errors"])

3. Secure User Script Execution
-------------------------------

Execute user-provided ML code in web applications with comprehensive security.

.. code-block:: python

   from mlpy.ml.transpiler import validate_ml_security, execute_ml_code_sandbox
   from mlpy.runtime.sandbox import SandboxConfig, SandboxResult
   from mlpy.runtime.capabilities.tokens import CapabilityToken
   import time
   import hashlib
   import logging

   class SecureMLExecutor:
       """Secure execution of user-provided ML code for web applications."""

       def __init__(self, max_concurrent_executions=10):
           self.max_concurrent_executions = max_concurrent_executions
           self.execution_cache = {}
           self.active_executions = {}
           self.execution_stats = {"total": 0, "successful": 0, "failed": 0}

           # Set up logging
           logging.basicConfig(level=logging.INFO)
           self.logger = logging.getLogger(__name__)

       def execute_user_script(self, user_id, script_code, execution_context=None):
           """Execute user-provided ML script with comprehensive security."""

           # Generate execution ID
           execution_id = self._generate_execution_id(user_id, script_code)

           # Check execution limits
           if not self._check_execution_limits(user_id):
               return self._create_error_response("Execution limit exceeded")

           # Security pre-validation
           security_result = self._validate_security(script_code, execution_id)
           if not security_result["safe"]:
               return self._create_error_response(
                   "Security validation failed",
                   security_result["issues"]
               )

           # Check cache
           cache_key = self._get_cache_key(script_code, execution_context)
           if cache_key in self.execution_cache:
               cached_result = self.execution_cache[cache_key]
               if time.time() - cached_result["timestamp"] < 300:  # 5 min cache
                   return cached_result["result"]

           # Execute with monitoring
           try:
               result = self._execute_with_monitoring(
                   execution_id, user_id, script_code, execution_context
               )

               # Cache successful results
               if result["success"]:
                   self.execution_cache[cache_key] = {
                       "result": result,
                       "timestamp": time.time()
                   }

               return result

           except Exception as e:
               self.logger.error(f"Execution {execution_id} failed: {e}")
               return self._create_error_response(f"Execution failed: {str(e)}")

           finally:
               self._cleanup_execution(execution_id)

       def _validate_security(self, script_code, execution_id):
           """Comprehensive security validation."""

           self.logger.info(f"Validating security for execution {execution_id}")

           # Static security analysis
           security_issues = validate_ml_security(script_code)

           # Check for critical issues
           critical_issues = [issue for issue in security_issues
                            if issue.severity == "critical"]

           if critical_issues:
               self.logger.warning(f"Critical security issues in {execution_id}: {critical_issues}")
               return {"safe": False, "issues": critical_issues}

           # Check script complexity (prevent resource exhaustion)
           complexity_check = self._analyze_script_complexity(script_code)
           if complexity_check["too_complex"]:
               return {"safe": False, "issues": ["Script too complex"]}

           # Additional custom security rules
           custom_violations = self._check_custom_security_rules(script_code)
           if custom_violations:
               return {"safe": False, "issues": custom_violations}

           return {"safe": True, "issues": security_issues}

       def _execute_with_monitoring(self, execution_id, user_id, script_code, context):
           """Execute script with comprehensive monitoring."""

           self.logger.info(f"Starting execution {execution_id} for user {user_id}")
           start_time = time.time()

           # Track active execution
           self.active_executions[execution_id] = {
               "user_id": user_id,
               "start_time": start_time,
               "status": "running"
           }

           # Create restrictive sandbox config
           sandbox_config = SandboxConfig(
               max_execution_time=5.0,     # 5 second limit
               max_memory_mb=50,           # 50MB RAM limit
               max_output_length=10000,    # 10KB output limit
               allow_network=False,        # No network access
               allow_file_system=False,    # No file system access
               temp_dir_only=True,         # Temporary files only
               max_file_operations=100     # Limited file ops
           )

           # Minimal capabilities for user scripts
           capabilities = ["execute:calculations"]  # Only basic calculations

           # Add user context safely
           safe_context = self._sanitize_context(context or {})

           # Execute in sandbox
           result = execute_ml_code_sandbox(
               source_code=script_code,
               source_file=f"user_script_{execution_id}.ml",
               capabilities=capabilities,
               context=safe_context,
               sandbox_config=sandbox_config
           )

           # Process results
           execution_time = time.time() - start_time

           self.logger.info(f"Execution {execution_id} completed in {execution_time:.2f}s")

           # Update stats
           self.execution_stats["total"] += 1
           if result.success:
               self.execution_stats["successful"] += 1
           else:
               self.execution_stats["failed"] += 1

           return self._process_sandbox_result(result, execution_id, execution_time)

       def _sanitize_context(self, context):
           """Sanitize user-provided context data."""
           sanitized = {}

           for key, value in context.items():
               # Only allow safe keys and values
               if key.startswith("_"):
                   continue  # Skip private keys

               if isinstance(value, (str, int, float, bool)):
                   sanitized[key] = value
               elif isinstance(value, list):
                   # Only allow lists of primitive types
                   if all(isinstance(item, (str, int, float, bool)) for item in value):
                       sanitized[key] = value[:100]  # Limit list size
               elif isinstance(value, dict):
                   # Recursively sanitize nested dicts
                   sanitized[key] = self._sanitize_context(value)

           return sanitized

       def _analyze_script_complexity(self, script_code):
           """Analyze script complexity to prevent resource exhaustion."""

           # Simple complexity metrics
           line_count = len(script_code.splitlines())
           char_count = len(script_code)

           # Check for potentially expensive patterns
           expensive_patterns = [
               "while", "for", "function", "recursion"  # Could be used for loops
           ]

           pattern_count = sum(script_code.count(pattern) for pattern in expensive_patterns)

           # Complexity thresholds
           if line_count > 100:
               return {"too_complex": True, "reason": "Too many lines"}

           if char_count > 5000:
               return {"too_complex": True, "reason": "Script too long"}

           if pattern_count > 10:
               return {"too_complex": True, "reason": "Too many loops/functions"}

           return {"too_complex": False}

       def _check_custom_security_rules(self, script_code):
           """Check application-specific security rules."""
           violations = []

           # Example: Block certain function names
           forbidden_functions = ["eval", "exec", "import", "__"]
           for func in forbidden_functions:
               if func in script_code:
                   violations.append(f"Forbidden function: {func}")

           # Example: Limit string concatenation to prevent DoS
           if script_code.count("+") > 50:
               violations.append("Too many string operations")

           return violations

       def _check_execution_limits(self, user_id):
           """Check per-user execution limits."""
           # Implementation would check user's quota, rate limits, etc.
           return len(self.active_executions) < self.max_concurrent_executions

       def _process_sandbox_result(self, sandbox_result, execution_id, execution_time):
           """Process sandbox execution result."""

           if sandbox_result.success:
               return {
                   "success": True,
                   "output": sandbox_result.output[:1000],  # Limit output size
                   "execution_time": execution_time,
                   "memory_used": sandbox_result.memory_used,
                   "execution_id": execution_id
               }
           else:
               self.logger.warning(f"Execution {execution_id} failed: {sandbox_result.error}")
               return {
                   "success": False,
                   "error": str(sandbox_result.error)[:500],  # Limit error message
                   "execution_time": execution_time,
                   "execution_id": execution_id
               }

       def get_execution_stats(self):
           """Get system execution statistics."""
           return {
               **self.execution_stats,
               "active_executions": len(self.active_executions),
               "cache_size": len(self.execution_cache)
           }

   # Usage in web application (Flask example)
   from flask import Flask, request, jsonify

   app = Flask(__name__)
   ml_executor = SecureMLExecutor()

   @app.route('/execute_ml', methods=['POST'])
   def execute_ml_endpoint():
       """Web endpoint for secure ML script execution."""

       try:
           data = request.get_json()
           user_id = data.get('user_id')
           script_code = data.get('script')
           context = data.get('context', {})

           if not user_id or not script_code:
               return jsonify({"error": "user_id and script are required"}), 400

           # Execute user script securely
           result = ml_executor.execute_user_script(user_id, script_code, context)

           return jsonify(result)

       except Exception as e:
           return jsonify({"error": str(e)}), 500

   @app.route('/ml_stats')
   def ml_stats():
       """Get ML execution statistics."""
       return jsonify(ml_executor.get_execution_stats())

This completes the comprehensive Python Integration Guide covering all the core patterns you requested, with practical examples for each integration scenario. The guide shows how to use mlpy's API for everything from basic transpilation to complex bidirectional Python-ML interactions.

Would you like me to proceed with the Developer Guide next, or would you prefer any adjustments to this Integration Guide?