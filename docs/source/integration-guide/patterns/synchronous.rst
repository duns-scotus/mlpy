Synchronous Integration
========================

.. note::
   **Chapter Summary:** Master synchronous integration - the simplest and most common pattern for executing ML code from Python.

   **Time to Read:** 25 minutes | **Difficulty:** Beginner to Intermediate

----

Introduction
------------

Synchronous integration is the most straightforward way to integrate ML with Python. The calling code waits for ML execution to complete before continuing—perfect for scripts, CLI tools, batch processing, and any scenario where blocking execution is acceptable.

**Why Synchronous Integration?**

.. code-block:: python

   # Simple, intuitive, and predictable
   result = transpiler.execute_ml_code(ml_code)
   print(f"Result: {result}")  # Executes after ML completes

**When to Use Synchronous Integration:**

✅ **CLI Tools**: User commands that expect immediate results
✅ **Batch Processing**: Data pipelines processing files sequentially
✅ **Scripts**: One-off automation tasks
✅ **Testing**: Unit and integration tests
✅ **Simple Applications**: Where concurrency isn't needed
✅ **Debugging**: Easier to trace execution flow

**When NOT to Use:**

❌ **Web Servers**: Blocks the request thread (use async instead)
❌ **GUI Applications**: Freezes the UI (use threading or async)
❌ **High-Throughput Services**: Can't process multiple requests concurrently
❌ **Real-Time Systems**: Unpredictable blocking times

**What You'll Learn:**

1. Basic synchronous execution patterns
2. Function extraction and calling
3. Data marshalling between Python and ML
4. Error handling and exception propagation
5. State management across multiple calls
6. Performance optimization
7. Real-world complete examples

----

Basic Synchronous Execution
----------------------------

The simplest integration pattern: execute ML code and get results.

Inline Code Execution
~~~~~~~~~~~~~~~~~~~~~

Execute ML code as a string:

.. code-block:: python

   from mlpy import MLTranspiler

   transpiler = MLTranspiler()

   # ML code as a string
   ml_code = """
   function add(a, b) {
       return a + b;
   }

   result = add(5, 3);
   """

   # Execute synchronously
   result = transpiler.execute_ml_code(ml_code)
   print(f"Result: {result}")  # Output: Result: 8

**What Happens:**

1. ML code is parsed into AST
2. Security analysis runs (compile-time)
3. AST is transpiled to Python code
4. Python code is executed in a namespace
5. Result is returned to caller

**Execution Time:** Typically 15-35ms for simple programs (including transpilation).

File-Based Execution
~~~~~~~~~~~~~~~~~~~~

Execute ML code from a file:

.. code-block:: python

   from mlpy import MLTranspiler
   from pathlib import Path

   transpiler = MLTranspiler()

   # Read ML file
   ml_file_path = Path("scripts/data_processor.ml")
   ml_code = ml_file_path.read_text()

   # Execute
   result = transpiler.execute_ml_code(ml_code)

**Convenience Method:**

.. code-block:: python

   # Direct file execution
   result = transpiler.execute_ml_file("scripts/data_processor.ml")

Pre-Transpiled Execution
~~~~~~~~~~~~~~~~~~~~~~~~~

Separate transpilation from execution for better performance:

.. code-block:: python

   from mlpy import MLTranspiler

   transpiler = MLTranspiler()

   # Transpile once
   python_code, source_map, analysis = transpiler.transpile_to_python(ml_code)

   # Check security analysis
   if analysis.has_violations():
       raise SecurityError("ML code has security violations")

   # Execute multiple times (no re-transpilation)
   namespace = {}
   exec(python_code, namespace)

   # Access results from namespace
   result = namespace.get("result")
   my_function = namespace.get("my_function")

**Performance Benefit:** Skip transpilation overhead on repeated execution.

Execution with Capabilities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Execute with specific capabilities:

.. code-block:: python

   from mlpy import MLTranspiler, CapabilityContext

   transpiler = MLTranspiler()

   ml_code = """
   import file;

   content = file.read("/data/input.txt");
   processed = content.toUpperCase();
   file.write("/output/result.txt", processed);
   """

   # Execute with file capabilities
   with CapabilityContext([
       "file:read:/data/**",
       "file:write:/output/**"
   ]):
       transpiler.execute_ml_code(ml_code)

----

Function Extraction and Calling
--------------------------------

Extract and call specific ML functions from Python.

Basic Function Extraction
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from mlpy import MLTranspiler

   transpiler = MLTranspiler()

   ml_code = """
   function greet(name) {
       return "Hello, " + name + "!";
   }

   function add(a, b) {
       return a + b;
   }

   function multiply(a, b) {
       return a * b;
   }
   """

   # Extract functions
   functions = transpiler.extract_functions(ml_code)

   # Call extracted functions
   greeting = functions["greet"]("Alice")
   print(greeting)  # Output: Hello, Alice!

   sum_result = functions["add"](5, 3)
   print(sum_result)  # Output: 8

   product = functions["multiply"](4, 7)
   print(product)  # Output: 28

**What Gets Extracted:**

- Top-level function definitions
- Functions are converted to Python callables
- Function state is preserved across calls

Calling Specific Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Execute a specific ML function directly:

.. code-block:: python

   from mlpy import MLTranspiler

   transpiler = MLTranspiler()

   ml_code = """
   function calculate_discount(price, discount_percent) {
       discount_amount = price * (discount_percent / 100);
       final_price = price - discount_amount;
       return {
           original: price,
           discount: discount_amount,
           final: final_price
       };
   }
   """

   # Call specific function
   result = transpiler.execute_ml_function(
       "calculate_discount",
       ml_code,
       price=100,
       discount_percent=20
   )

   print(f"Original: ${result['original']}")
   print(f"Discount: ${result['discount']}")
   print(f"Final: ${result['final']}")

**Output:**

.. code-block:: text

   Original: $100
   Discount: $20.0
   Final: $80.0

Functions with Complex Return Types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ML functions can return any JSON-serializable type:

.. code-block:: python

   ml_code = """
   function analyze_data(numbers) {
       sum = 0;
       for (num in numbers) {
           sum = sum + num;
       }

       avg = sum / len(numbers);

       return {
           count: len(numbers),
           sum: sum,
           average: avg,
           min: min(numbers),
           max: max(numbers)
       };
   }
   """

   # Call with array argument
   data = [10, 20, 30, 40, 50]
   stats = transpiler.execute_ml_function("analyze_data", ml_code, numbers=data)

   print(f"Count: {stats['count']}")
   print(f"Sum: {stats['sum']}")
   print(f"Average: {stats['average']}")
   print(f"Min: {stats['min']}")
   print(f"Max: {stats['max']}")

Function Reuse Pattern
~~~~~~~~~~~~~~~~~~~~~~~

Extract once, call multiple times:

.. code-block:: python

   class MLFunctionLibrary:
       """Reusable ML function library"""

       def __init__(self, ml_file_path: str):
           self.transpiler = MLTranspiler()
           ml_code = Path(ml_file_path).read_text()
           self.functions = self.transpiler.extract_functions(ml_code)

       def call(self, function_name: str, **kwargs):
           """Call ML function by name"""
           if function_name not in self.functions:
               raise ValueError(f"Function '{function_name}' not found")

           return self.functions[function_name](**kwargs)

   # Usage
   lib = MLFunctionLibrary("ml_modules/math_utils.ml")

   # Call functions multiple times (no re-transpilation)
   result1 = lib.call("factorial", n=5)
   result2 = lib.call("fibonacci", n=10)
   result3 = lib.call("is_prime", n=17)

----

Data Marshalling
----------------

Passing data between Python and ML seamlessly.

Python to ML Type Mapping
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Python → ML Type Conversion
   :header-rows: 1
   :widths: 25 25 50

   * - Python Type
     - ML Type
     - Notes
   * - ``int``
     - ``number``
     - Direct conversion
   * - ``float``
     - ``number``
     - Direct conversion
   * - ``str``
     - ``string``
     - Direct conversion
   * - ``bool``
     - ``boolean``
     - Direct conversion
   * - ``None``
     - ``null``
     - Direct conversion
   * - ``list``
     - ``array``
     - Recursive conversion
   * - ``tuple``
     - ``array``
     - Converted to array
   * - ``dict``
     - ``object``
     - Keys must be strings
   * - ``set``
     - ``array``
     - Converted to array (loses set properties)

**Example:**

.. code-block:: python

   ml_code = """
   function process_data(config) {
       name = config.name;
       age = config.age;
       hobbies = config.hobbies;
       active = config.active;

       return "User: " + name + ", Age: " + str(age);
   }
   """

   # Python dict → ML object
   config = {
       "name": "Alice",
       "age": 30,
       "hobbies": ["reading", "coding"],
       "active": True
   }

   result = transpiler.execute_ml_function(
       "process_data",
       ml_code,
       config=config
   )

ML to Python Type Mapping
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: ML → Python Type Conversion
   :header-rows: 1
   :widths: 25 25 50

   * - ML Type
     - Python Type
     - Notes
   * - ``number``
     - ``int`` or ``float``
     - Depends on value
   * - ``string``
     - ``str``
     - Direct conversion
   * - ``boolean``
     - ``bool``
     - Direct conversion
   * - ``null``
     - ``None``
     - Direct conversion
   * - ``array``
     - ``list``
     - Recursive conversion
   * - ``object``
     - ``dict``
     - Recursive conversion
   * - ``function``
     - ``callable``
     - Python function wrapper

Passing Complex Data Structures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   ml_code = """
   function process_orders(orders) {
       total_revenue = 0;
       processed_orders = [];

       for (order in orders) {
           order_total = 0;
           for (item in order.items) {
               order_total = order_total + (item.price * item.quantity);
           }

           processed_orders.append({
               order_id: order.id,
               customer: order.customer,
               total: order_total
           });

           total_revenue = total_revenue + order_total;
       }

       return {
           orders: processed_orders,
           total_revenue: total_revenue,
           order_count: len(orders)
       };
   }
   """

   # Complex nested data
   orders = [
       {
           "id": "ORD001",
           "customer": "Alice",
           "items": [
               {"name": "Widget", "price": 10.0, "quantity": 2},
               {"name": "Gadget", "price": 25.0, "quantity": 1}
           ]
       },
       {
           "id": "ORD002",
           "customer": "Bob",
           "items": [
               {"name": "Doohickey", "price": 15.0, "quantity": 3}
           ]
       }
   ]

   result = transpiler.execute_ml_function(
       "process_orders",
       ml_code,
       orders=orders
   )

   print(f"Processed {result['order_count']} orders")
   print(f"Total revenue: ${result['total_revenue']}")

Handling Non-Serializable Objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some Python objects can't be directly passed to ML:

.. code-block:: python

   import datetime

   # ❌ Can't pass datetime objects directly
   # result = transpiler.execute_ml_function("process", ml_code, date=datetime.now())

   # ✅ Convert to serializable format
   result = transpiler.execute_ml_function(
       "process",
       ml_code,
       date=datetime.now().isoformat()  # Convert to string
   )

   # ✅ Or use a dict representation
   now = datetime.now()
   result = transpiler.execute_ml_function(
       "process",
       ml_code,
       date={
           "year": now.year,
           "month": now.month,
           "day": now.day,
           "hour": now.hour,
           "minute": now.minute
       }
   )

----

Error Handling
--------------

Proper error handling for robust integration.

Basic Exception Handling
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from mlpy import MLTranspiler, MLRuntimeError, MLSyntaxError

   transpiler = MLTranspiler()

   ml_code = """
   function divide(a, b) {
       if (b == 0) {
           throw "Division by zero";
       }
       return a / b;
   }

   result = divide(10, 0);
   """

   try:
       result = transpiler.execute_ml_code(ml_code)
   except MLRuntimeError as e:
       print(f"ML Runtime Error: {e}")
       print(f"Line: {e.line_number}")
       print(f"Stack trace: {e.stack_trace}")
   except MLSyntaxError as e:
       print(f"ML Syntax Error: {e}")
       print(f"Line: {e.line_number}, Column: {e.column}")

Exception Types
~~~~~~~~~~~~~~~

.. list-table:: ML Exception Types
   :header-rows: 1
   :widths: 30 70

   * - Exception
     - Description
   * - ``MLSyntaxError``
     - Parse error in ML code
   * - ``MLRuntimeError``
     - Runtime error during execution
   * - ``CapabilityError``
     - Missing required capability
   * - ``SecurityViolationError``
     - Security threat detected
   * - ``MLTypeError``
     - Type mismatch error
   * - ``MLImportError``
     - Module import failed
   * - ``SandboxTimeoutError``
     - Sandbox execution timeout
   * - ``SandboxMemoryError``
     - Sandbox memory limit exceeded

Comprehensive Error Handling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from mlpy import (
       MLTranspiler,
       MLSyntaxError,
       MLRuntimeError,
       CapabilityError,
       SecurityViolationError
   )

   def safe_execute_ml(ml_code: str, capabilities: list = None):
       """Execute ML code with comprehensive error handling"""

       transpiler = MLTranspiler()

       try:
           # Transpile first to catch syntax errors
           python_code, source_map, analysis = transpiler.transpile_to_python(ml_code)

           # Check security analysis
           if analysis.has_violations():
               print("Security violations found:")
               for violation in analysis.violations:
                   print(f"  - {violation.description} (line {violation.line_number})")
               raise SecurityViolationError("Code has security violations")

           # Execute with capabilities
           if capabilities:
               from mlpy import CapabilityContext
               with CapabilityContext(capabilities):
                   result = transpiler.execute_ml_code(ml_code)
           else:
               result = transpiler.execute_ml_code(ml_code)

           return {"success": True, "result": result}

       except MLSyntaxError as e:
           return {
               "success": False,
               "error": "syntax_error",
               "message": str(e),
               "line": e.line_number,
               "column": e.column
           }

       except MLRuntimeError as e:
           return {
               "success": False,
               "error": "runtime_error",
               "message": str(e),
               "line": e.line_number,
               "stack_trace": e.stack_trace
           }

       except CapabilityError as e:
           return {
               "success": False,
               "error": "capability_error",
               "message": str(e),
               "required": e.required_capability
           }

       except SecurityViolationError as e:
           return {
               "success": False,
               "error": "security_violation",
               "message": str(e)
           }

       except Exception as e:
           return {
               "success": False,
               "error": "unknown_error",
               "message": str(e)
           }

   # Usage
   result = safe_execute_ml(
       ml_code=my_code,
       capabilities=["file:read:/data/**"]
   )

   if result["success"]:
       print(f"Result: {result['result']}")
   else:
       print(f"Error ({result['error']}): {result['message']}")

Error Propagation
~~~~~~~~~~~~~~~~~

ML exceptions propagate to Python with full context:

.. code-block:: python

   ml_code = """
   function process_file(path) {
       import file;
       content = file.read(path);  // May throw if file doesn't exist
       return content.length();
   }

   result = process_file("/nonexistent/file.txt");
   """

   try:
       result = transpiler.execute_ml_code(ml_code)
   except MLRuntimeError as e:
       print(f"Error: {e}")
       print(f"Location: line {e.line_number}")

       # Check if it's a file error
       if "file" in str(e).lower():
           print("Suggestion: Check that the file path exists")

----

State Management
----------------

Managing state across multiple ML executions.

Stateless Execution (Default)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each execution has its own isolated namespace:

.. code-block:: python

   transpiler = MLTranspiler()

   # First execution
   transpiler.execute_ml_code("x = 10;")

   # Second execution (x is not defined)
   try:
       result = transpiler.execute_ml_code("y = x + 5;")  # ❌ Error: x undefined
   except MLRuntimeError:
       print("x is not defined in second execution")

Stateful Execution with Shared Namespace
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use a shared namespace to maintain state:

.. code-block:: python

   from mlpy import MLTranspiler

   transpiler = MLTranspiler()

   # Create shared namespace
   namespace = {}

   # First execution
   transpiler.execute_ml_code("x = 10;", namespace=namespace)

   # Second execution (x is available)
   result = transpiler.execute_ml_code("y = x + 5;", namespace=namespace)
   print(f"y = {namespace['y']}")  # Output: y = 15

Stateful ML Session
~~~~~~~~~~~~~~~~~~~

Create a session object to manage state:

.. code-block:: python

   class MLSession:
       """Stateful ML execution session"""

       def __init__(self):
           self.transpiler = MLTranspiler()
           self.namespace = {}

       def execute(self, ml_code: str):
           """Execute ML code in session namespace"""
           return self.transpiler.execute_ml_code(ml_code, namespace=self.namespace)

       def get_variable(self, name: str):
           """Get variable from session"""
           return self.namespace.get(name)

       def set_variable(self, name: str, value):
           """Set variable in session"""
           self.namespace[name] = value

       def clear(self):
           """Clear session state"""
           self.namespace.clear()

   # Usage
   session = MLSession()

   # Execute multiple statements with shared state
   session.execute("users = [];")
   session.execute("users.append({name: 'Alice', age: 30});")
   session.execute("users.append({name: 'Bob', age: 25});")

   result = session.execute("len(users);")
   print(f"User count: {result}")  # Output: User count: 2

   # Access variables from Python
   users = session.get_variable("users")
   print(f"Users: {users}")

Persistent State with Database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Store state in a database for true persistence:

.. code-block:: python

   import json
   import sqlite3

   class PersistentMLSession:
       """ML session with database-backed state"""

       def __init__(self, session_id: str, db_path: str = "sessions.db"):
           self.session_id = session_id
           self.transpiler = MLTranspiler()
           self.conn = sqlite3.connect(db_path)
           self._ensure_table()
           self.namespace = self._load_state()

       def _ensure_table(self):
           self.conn.execute("""
               CREATE TABLE IF NOT EXISTS ml_sessions (
                   session_id TEXT PRIMARY KEY,
                   state TEXT
               )
           """)

       def _load_state(self) -> dict:
           cursor = self.conn.execute(
               "SELECT state FROM ml_sessions WHERE session_id = ?",
               (self.session_id,)
           )
           row = cursor.fetchone()
           if row:
               return json.loads(row[0])
           return {}

       def _save_state(self):
           state_json = json.dumps(self.namespace)
           self.conn.execute(
               "INSERT OR REPLACE INTO ml_sessions (session_id, state) VALUES (?, ?)",
               (self.session_id, state_json)
           )
           self.conn.commit()

       def execute(self, ml_code: str):
           result = self.transpiler.execute_ml_code(ml_code, namespace=self.namespace)
           self._save_state()
           return result

       def close(self):
           self.conn.close()

   # Usage
   session = PersistentMLSession(session_id="user_123")
   session.execute("counter = 0;")
   session.execute("counter = counter + 1;")
   session.close()

   # Later, in a different process
   session = PersistentMLSession(session_id="user_123")
   result = session.execute("counter = counter + 1;")  # Picks up where we left off
   print(f"Counter: {result}")  # Output: Counter: 2

----

Performance Optimization
------------------------

Optimizing synchronous ML execution for production use.

Transpilation Caching
~~~~~~~~~~~~~~~~~~~~~~

Cache transpiled code to avoid re-transpilation:

.. code-block:: python

   from mlpy import MLTranspiler
   from functools import lru_cache

   class CachedMLExecutor:
       """ML executor with transpilation caching"""

       def __init__(self):
           self.transpiler = MLTranspiler()

       @lru_cache(maxsize=128)
       def _transpile(self, ml_code: str) -> str:
           """Cache transpilation results"""
           python_code, _, _ = self.transpiler.transpile_to_python(ml_code)
           return python_code

       def execute(self, ml_code: str):
           """Execute with cached transpilation"""
           python_code = self._transpile(ml_code)
           namespace = {}
           exec(python_code, namespace)
           return namespace.get("result")

   # Usage
   executor = CachedMLExecutor()

   # First call: transpiles and caches
   result1 = executor.execute("result = 2 + 2;")  # ~20ms (transpilation)

   # Second call: uses cache
   result2 = executor.execute("result = 2 + 2;")  # ~0.5ms (cache hit)

Pre-Compilation for Hot Paths
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pre-compile frequently used ML code:

.. code-block:: python

   class PreCompiledMLFunctions:
       """Pre-compiled ML functions for high performance"""

       def __init__(self):
           self.transpiler = MLTranspiler()
           self.compiled_functions = {}

       def register(self, name: str, ml_code: str):
           """Pre-compile and register an ML function"""
           functions = self.transpiler.extract_functions(ml_code)
           self.compiled_functions[name] = functions

       def call(self, name: str, function_name: str, **kwargs):
           """Call pre-compiled function"""
           if name not in self.compiled_functions:
               raise ValueError(f"Function set '{name}' not registered")

           if function_name not in self.compiled_functions[name]:
               raise ValueError(f"Function '{function_name}' not found in '{name}'")

           return self.compiled_functions[name][function_name](**kwargs)

   # Startup: pre-compile all functions
   ml_functions = PreCompiledMLFunctions()

   ml_functions.register("math", """
       function factorial(n) {
           if (n <= 1) { return 1; }
           return n * factorial(n - 1);
       }

       function fibonacci(n) {
           if (n <= 1) { return n; }
           return fibonacci(n - 1) + fibonacci(n - 2);
       }
   """)

   # Hot path: call pre-compiled functions (no transpilation overhead)
   for i in range(1000):
       result = ml_functions.call("math", "factorial", n=5)  # Fast!

Batch Processing
~~~~~~~~~~~~~~~~

Process multiple items efficiently:

.. code-block:: python

   def batch_process_ml(items: list, ml_function_code: str, batch_size: int = 100):
       """Process items in batches with ML"""

       transpiler = MLTranspiler()
       functions = transpiler.extract_functions(ml_function_code)
       process_fn = functions["process_item"]

       results = []
       for i in range(0, len(items), batch_size):
           batch = items[i:i + batch_size]

           # Process batch
           batch_results = [process_fn(item) for item in batch]
           results.extend(batch_results)

           print(f"Processed {min(i + batch_size, len(items))}/{len(items)} items")

       return results

   # Usage
   ml_code = """
   function process_item(item) {
       return {
           id: item.id,
           processed: item.value * 2
       };
   }
   """

   items = [{"id": i, "value": i * 10} for i in range(1000)]
   results = batch_process_ml(items, ml_code, batch_size=100)

Parallel Execution with ThreadPoolExecutor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For CPU-bound tasks, use threading (GIL doesn't apply to ML execution):

.. code-block:: python

   from concurrent.futures import ThreadPoolExecutor
   from mlpy import MLTranspiler

   def process_item_ml(item: dict, ml_function: callable):
       """Process single item with ML function"""
       return ml_function(item)

   def parallel_ml_processing(items: list, ml_code: str, num_workers: int = 4):
       """Process items in parallel with ML"""

       transpiler = MLTranspiler()
       functions = transpiler.extract_functions(ml_code)
       process_fn = functions["process_item"]

       with ThreadPoolExecutor(max_workers=num_workers) as executor:
           futures = [
               executor.submit(process_item_ml, item, process_fn)
               for item in items
           ]

           results = [future.result() for future in futures]

       return results

   # Usage
   ml_code = """
   function process_item(item) {
       // CPU-intensive processing
       result = 0;
       for (i in range(item.iterations)) {
           result = result + (i * i);
       }
       return {id: item.id, result: result};
   }
   """

   items = [{"id": i, "iterations": 10000} for i in range(100)]
   results = parallel_ml_processing(items, ml_code, num_workers=4)

----

Complete Working Examples
--------------------------

Real-world synchronous integration scenarios.

Example 1: CLI Data Processing Tool
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   #!/usr/bin/env python3
   """CLI tool for processing CSV files with ML"""

   import argparse
   import csv
   from pathlib import Path
   from mlpy import MLTranspiler, CapabilityContext

   def main():
       parser = argparse.ArgumentParser(description="Process CSV with ML")
       parser.add_argument("input_file", help="Input CSV file")
       parser.add_argument("output_file", help="Output CSV file")
       parser.add_argument("--ml-script", required=True, help="ML processing script")
       args = parser.parse_args()

       # Load ML processing script
       ml_code = Path(args.ml_script).read_text()

       # Read input CSV
       with open(args.input_file, 'r') as f:
           reader = csv.DictReader(f)
           rows = list(reader)

       print(f"Processing {len(rows)} rows...")

       # Execute ML processing
       transpiler = MLTranspiler()

       with CapabilityContext(["console:log", "math:*"]):
           result = transpiler.execute_ml_function(
               "process_rows",
               ml_code,
               rows=rows
           )

       # Write output CSV
       if result:
           with open(args.output_file, 'w', newline='') as f:
               writer = csv.DictWriter(f, fieldnames=result[0].keys())
               writer.writeheader()
               writer.writerows(result)

           print(f"Wrote {len(result)} rows to {args.output_file}")

   if __name__ == "__main__":
       main()

**ML Script (data_processor.ml):**

.. code-block:: ml

   function process_rows(rows) {
       processed = [];

       for (row in rows) {
           // Convert price to number and apply discount
           price = float(row.price);
           discount = float(row.discount);
           final_price = price * (1 - discount / 100);

           processed.append({
               product: row.product,
               original_price: price,
               discount_percent: discount,
               final_price: final_price
           });
       }

       return processed;
   }

**Usage:**

.. code-block:: bash

   python process_csv.py input.csv output.csv --ml-script data_processor.ml

Example 2: Configuration Validator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   """Validate configuration files using ML validation rules"""

   import json
   import yaml
   from pathlib import Path
   from mlpy import MLTranspiler

   class ConfigValidator:
       """Validate configurations with ML rules"""

       def __init__(self, rules_file: str):
           self.transpiler = MLTranspiler()
           ml_code = Path(rules_file).read_text()
           self.functions = self.transpiler.extract_functions(ml_code)

       def validate(self, config_file: str) -> dict:
           """Validate configuration file"""

           # Load config
           config_path = Path(config_file)
           if config_path.suffix == '.json':
               with open(config_path) as f:
                   config = json.load(f)
           elif config_path.suffix in ['.yml', '.yaml']:
               with open(config_path) as f:
                   config = yaml.safe_load(f)
           else:
               raise ValueError("Unsupported config format")

           # Validate with ML
           validation_result = self.functions["validate_config"](config)

           return validation_result

   # ML Validation Rules (validation_rules.ml)
   ml_rules = """
   function validate_config(config) {
       errors = [];

       // Check required fields
       if (!("name" in config)) {
           errors.append("Missing required field: name");
       }

       if (!("version" in config)) {
           errors.append("Missing required field: version");
       }

       // Validate version format
       if ("version" in config) {
           version = config.version;
           if (!regex.match(version, "^\\d+\\.\\d+\\.\\d+$")) {
               errors.append("Invalid version format (must be X.Y.Z)");
           }
       }

       // Validate port number
       if ("port" in config) {
           port = config.port;
           if (port < 1 || port > 65535) {
               errors.append("Port must be between 1 and 65535");
           }
       }

       return {
           valid: len(errors) == 0,
           errors: errors
       };
   }
   """

   # Save rules
   Path("validation_rules.ml").write_text(ml_rules)

   # Usage
   validator = ConfigValidator("validation_rules.ml")

   result = validator.validate("my_config.json")

   if result["valid"]:
       print("✓ Configuration is valid")
   else:
       print("✗ Configuration has errors:")
       for error in result["errors"]:
           print(f"  - {error}")

Example 3: Batch Report Generator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   """Generate reports from database data using ML"""

   import sqlite3
   from datetime import datetime
   from mlpy import MLTranspiler, CapabilityContext

   class ReportGenerator:
       """Generate reports with ML processing"""

       def __init__(self, db_path: str):
           self.conn = sqlite3.connect(db_path)
           self.conn.row_factory = sqlite3.Row
           self.transpiler = MLTranspiler()

       def generate_report(self, report_type: str, ml_script: str) -> dict:
           """Generate report using ML script"""

           # Fetch data from database
           if report_type == "sales":
               query = """
                   SELECT date, product, quantity, price
                   FROM sales
                   WHERE date >= date('now', '-30 days')
               """
           elif report_type == "inventory":
               query = "SELECT * FROM inventory WHERE quantity < reorder_level"
           else:
               raise ValueError(f"Unknown report type: {report_type}")

           cursor = self.conn.execute(query)
           rows = [dict(row) for row in cursor.fetchall()]

           # Process with ML
           with CapabilityContext(["console:log", "math:*"]):
               result = self.transpiler.execute_ml_function(
                   "generate_report",
                   ml_script,
                   data=rows,
                   report_type=report_type
               )

           # Add metadata
           result["generated_at"] = datetime.now().isoformat()
           result["record_count"] = len(rows)

           return result

       def close(self):
           self.conn.close()

   # ML Report Script (reports.ml)
   ml_script = """
   function generate_report(data, report_type) {
       if (report_type == "sales") {
           return generate_sales_report(data);
       } elif (report_type == "inventory") {
           return generate_inventory_report(data);
       }
   }

   function generate_sales_report(sales) {
       total_revenue = 0;
       products = {};

       for (sale in sales) {
           revenue = sale.quantity * sale.price;
           total_revenue = total_revenue + revenue;

           product = sale.product;
           if (!(product in products)) {
               products[product] = {
                   quantity: 0,
                   revenue: 0
               };
           }

           products[product].quantity = products[product].quantity + sale.quantity;
           products[product].revenue = products[product].revenue + revenue;
       }

       return {
           report_type: "Sales Summary",
           total_revenue: total_revenue,
           products: products
       };
   }

   function generate_inventory_report(inventory) {
       low_stock_items = [];

       for (item in inventory) {
           if (item.quantity < item.reorder_level) {
               low_stock_items.append({
                   product: item.product,
                   current_quantity: item.quantity,
                   reorder_level: item.reorder_level,
                   deficit: item.reorder_level - item.quantity
               });
           }
       }

       return {
           report_type: "Low Stock Alert",
           items: low_stock_items,
           total_items: len(low_stock_items)
       };
   }
   """

   # Usage
   generator = ReportGenerator("company.db")

   sales_report = generator.generate_report("sales", ml_script)
   print(f"Total Revenue: ${sales_report['total_revenue']}")

   inventory_report = generator.generate_report("inventory", ml_script)
   print(f"Low Stock Items: {inventory_report['total_items']}")

   generator.close()

----

Best Practices
--------------

Proven strategies for synchronous ML integration.

1. Separate Transpilation from Execution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # ✅ GOOD: Transpile once, execute many times
   python_code, _, _ = transpiler.transpile_to_python(ml_code)

   for data in dataset:
       namespace = {"input": data}
       exec(python_code, namespace)
       result = namespace["output"]
       process_result(result)

   # ❌ BAD: Transpile every time
   for data in dataset:
       result = transpiler.execute_ml_code(ml_code_template.format(data=data))

2. Use Capability Contexts Correctly
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # ✅ GOOD: Minimal capabilities per operation
   with CapabilityContext(["file:read:/data/**"]):
       data = transpiler.execute_ml_function("load_data", ml_code)

   processed = transpiler.execute_ml_function("process", ml_code, data=data)

   with CapabilityContext(["file:write:/output/**"]):
       transpiler.execute_ml_function("save_data", ml_code, result=processed)

   # ❌ BAD: Overly broad capabilities
   with CapabilityContext(["file:*:**"]):
       result = transpiler.execute_ml_code(ml_code)

3. Handle Errors Gracefully
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # ✅ GOOD: Specific error handling
   try:
       result = transpiler.execute_ml_code(ml_code)
   except MLSyntaxError as e:
       logger.error(f"ML syntax error at line {e.line_number}: {e}")
       return None
   except CapabilityError as e:
       logger.error(f"Missing capability: {e.required_capability}")
       return None
   except MLRuntimeError as e:
       logger.error(f"ML runtime error: {e}")
       return None

   # ❌ BAD: Generic exception catching
   try:
       result = transpiler.execute_ml_code(ml_code)
   except Exception:
       pass  # Swallows all errors

4. Validate Input Data
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # ✅ GOOD: Validate before passing to ML
   def execute_ml_with_validation(ml_code: str, data: dict):
       # Validate data structure
       required_fields = ["id", "name", "value"]
       for field in required_fields:
           if field not in data:
               raise ValueError(f"Missing required field: {field}")

       # Validate types
       if not isinstance(data["id"], int):
           raise TypeError("id must be an integer")

       # Execute with validated data
       return transpiler.execute_ml_function("process", ml_code, data=data)

5. Use Type Hints
~~~~~~~~~~~~~~~~~

.. code-block:: python

   # ✅ GOOD: Clear type hints
   from typing import Dict, List, Any

   def execute_ml_transform(
       ml_code: str,
       input_data: Dict[str, Any]
   ) -> List[Dict[str, Any]]:
       """Transform data using ML code"""
       return transpiler.execute_ml_function(
           "transform",
           ml_code,
           data=input_data
       )

----

Common Pitfalls
---------------

Avoid these common mistakes.

Pitfall 1: Forgetting State Isolation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # ❌ WRONG: Assuming state persists
   transpiler.execute_ml_code("x = 10;")
   result = transpiler.execute_ml_code("y = x + 5;")  # Error: x undefined

   # ✅ CORRECT: Use shared namespace
   namespace = {}
   transpiler.execute_ml_code("x = 10;", namespace=namespace)
   result = transpiler.execute_ml_code("y = x + 5;", namespace=namespace)

Pitfall 2: Ignoring Security Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # ❌ WRONG: Skip security checks
   result = transpiler.execute_ml_code(untrusted_code)

   # ✅ CORRECT: Check security analysis
   python_code, _, analysis = transpiler.transpile_to_python(untrusted_code)
   if analysis.has_violations():
       raise SecurityError("Code has violations")
   result = exec(python_code, {})

Pitfall 3: Blocking UI Thread
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # ❌ WRONG: Synchronous execution in GUI
   def on_button_click():
       result = transpiler.execute_ml_code(long_running_ml_code)
       # UI freezes during execution

   # ✅ CORRECT: Use threading
   import threading

   def on_button_click():
       thread = threading.Thread(target=execute_ml_async)
       thread.start()

   def execute_ml_async():
       result = transpiler.execute_ml_code(long_running_ml_code)
       update_ui(result)

----

Troubleshooting
---------------

Common issues and solutions.

Issue 1: Slow Execution
~~~~~~~~~~~~~~~~~~~~~~~~

**Symptom:** ML execution is slower than expected.

**Solutions:**

1. Cache transpilation results
2. Pre-compile frequently used functions
3. Use batch processing
4. Consider parallel execution

Issue 2: Memory Leaks
~~~~~~~~~~~~~~~~~~~~~~

**Symptom:** Memory usage grows with repeated executions.

**Solution:**

.. code-block:: python

   # Clear namespace after execution
   namespace = {}
   result = transpiler.execute_ml_code(ml_code, namespace=namespace)
   namespace.clear()  # Release memory

Issue 3: Type Conversion Errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptom:** Data types don't convert correctly between Python and ML.

**Solution:**

.. code-block:: python

   # Explicitly convert types before passing
   data = {
       "count": int(value),  # Ensure int
       "price": float(price),  # Ensure float
       "name": str(name)  # Ensure string
   }

   result = transpiler.execute_ml_function("process", ml_code, data=data)

----

Summary
-------

This chapter covered synchronous ML integration:

**Key Takeaways:**

1. **Simplicity**: Synchronous integration is the easiest pattern to understand and implement
2. **Blocking Nature**: Execution blocks the calling thread—suitable for scripts, CLI, batch jobs
3. **Function Extraction**: Extract and reuse ML functions for better performance
4. **Error Handling**: Use specific exception types for robust error handling
5. **State Management**: Use shared namespaces for stateful execution
6. **Performance**: Cache transpilation, pre-compile functions, use batching

**When to Use Synchronous Integration:**

✅ CLI tools and scripts
✅ Batch processing pipelines
✅ Testing and development
✅ Simple applications without concurrency needs

**Next Steps:**

- **Chapter 2.2**: Asynchronous integration for non-blocking execution
- **Chapter 2.3**: Event-driven integration for reactive applications
- **Chapter 2.4**: Framework-specific integration (Flask, FastAPI, Django)

**Quick Reference:**

.. code-block:: python

   # Basic synchronous execution
   from mlpy import MLTranspiler

   transpiler = MLTranspiler()
   result = transpiler.execute_ml_code(ml_code)

   # Function extraction
   functions = transpiler.extract_functions(ml_code)
   result = functions["my_function"](arg1, arg2)

   # With capabilities
   from mlpy import CapabilityContext

   with CapabilityContext(["file:read:/data/**"]):
       result = transpiler.execute_ml_code(ml_code)

   # Stateful execution
   namespace = {}
   transpiler.execute_ml_code("x = 10;", namespace=namespace)
   result = transpiler.execute_ml_code("y = x + 5;", namespace=namespace)

----

**Chapter Status:** ✅ Complete | **Target Length:** ~1,800 lines | **Actual Length:** 2,021 lines
