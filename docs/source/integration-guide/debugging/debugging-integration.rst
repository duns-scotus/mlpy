Debugging Integration Issues
=============================

.. note::
   **Chapter Summary:** Comprehensive guide to debugging ML-Python integration issues with practical tools, techniques, and real-world solutions.

.. contents:: In This Chapter
   :local:
   :depth: 2

Overview
--------

Debugging ML-Python integration requires understanding both the ML language runtime and Python execution environment. This chapter provides systematic approaches to identifying and resolving integration issues.

**What You'll Learn:**

* Common integration problems and their root causes
* Debugging tools and techniques
* Source map usage for accurate stack traces
* Logging and tracing across the ML-Python boundary
* Performance profiling and optimization
* Memory leak detection and analysis

**Prerequisites:**

* Basic understanding of Python debugging (pdb, logging)
* Familiarity with ML language syntax
* Understanding of the Integration Toolkit (async_ml_execute, ml_callback)

Common Integration Problems
----------------------------

Module Import Issues
^^^^^^^^^^^^^^^^^^^^

**Problem: Module Not Found**

.. code-block:: python

   # Python code
   result = transpile_ml_code("import mymodule; mymodule.process(data);")

   # Error: ModuleNotFoundError: No module named 'mymodule'

**Diagnosis:**

1. Check module registry configuration:

   .. code-block:: python

      from mlpy.stdlib.module_registry import get_registry

      registry = get_registry()
      print(f"Available modules: {registry.get_all_module_names()}")
      print(f"Extension paths: {registry._extension_dirs}")
      print(f"ML module paths: {registry._ml_module_dirs}")

2. Verify module discovery:

   .. code-block:: python

      # Check if module exists but isn't scanned
      registry._ensure_scanned()
      print(f"Is 'mymodule' available? {registry.is_available('mymodule')}")

**Solutions:**

1. **Add extension path** (for Python bridge modules):

   .. code-block:: python

      registry = get_registry()
      registry.add_extension_paths(["/path/to/custom/modules"])

2. **Add ML module path** (for .ml files):

   .. code-block:: python

      registry = get_registry()
      registry.add_ml_module_paths(["/path/to/ml/modules"])

3. **Configure via mlpy.json**:

   .. code-block:: json

      {
        "project_name": "my_app",
        "python_extension_paths": [
          "./custom_modules",
          "/usr/local/lib/mlpy/extensions"
        ],
        "ml_module_paths": [
          "./ml_modules",
          "./user_modules"
        ]
      }

4. **Invalidate cache** after adding paths:

   .. code-block:: python

      registry.invalidate_cache()

**Problem: Module Found but Import Fails**

.. code-block:: text

   SecurityError: Module 'os' is not allowed
   Blocked modules: os, sys, subprocess, socket

**Diagnosis:**

The module exists but is blocked by security policy. Check security configuration.

**Solutions:**

1. **Grant capability** (if module requires system access):

   .. code-block:: python

      from mlpy.runtime.capabilities.manager import file_capability_context

      with file_capability_context(action='read', pattern='/data/*'):
          result = transpile_ml_code("import file; file.read('/data/config.json');")

2. **Use safe alternative** (recommended):

   Instead of importing dangerous modules, use ML stdlib:

   .. code-block:: ml

      import file;  // Safe, capability-controlled file access
      content = file.read('/data/config.json');

Type Conversion Issues
^^^^^^^^^^^^^^^^^^^^^^

**Problem: Python → ML Type Conversion Fails**

.. code-block:: python

   from mlpy.ml.transpiler import execute_ml_code_sandbox

   result = execute_ml_code_sandbox(
       "function process(items) { return items.length; }",
       context={'items': {'a': 1, 'b': 2}}  # Dict, not list!
   )

   # Error: AttributeError: 'dict' object has no attribute 'length'

**Diagnosis:**

ML expects an array (list) but received an object (dict).

**Type Mapping Reference:**

=================  ==================  ==================
Python Type        ML Type             Notes
=================  ==================  ==================
list               array               Direct mapping
dict               object              Direct mapping
str                string              Direct mapping
int/float          number              Unified numeric type
bool               boolean             Direct mapping
None               null                Direct mapping
datetime           DateTime object     Via datetime module
Custom objects     object              Requires serialization
=================  ==================  ==================

**Solutions:**

1. **Convert to correct type**:

   .. code-block:: python

      result = execute_ml_code_sandbox(
          "function process(items) { return items.length; }",
          context={'items': [1, 2, 3]}  # List, not dict
      )

2. **Handle both types in ML**:

   .. code-block:: ml

      function process(items) {
          if (typeof(items) == "array") {
              return items.length;
          } else if (typeof(items) == "object") {
              return Object.keys(items).length;
          }
          return 0;
      }

3. **Use explicit conversion**:

   .. code-block:: python

      import json

      data = {'a': 1, 'b': 2}
      items_list = list(data.values())

      result = execute_ml_code_sandbox(
          "function process(items) { return items.length; }",
          context={'items': items_list}
      )

**Problem: ML → Python Type Conversion Fails**

.. code-block:: python

   result = execute_ml_code_sandbox("result = {name: 'Alice', age: 30};")

   # Expecting: {'name': 'Alice', 'age': 30}
   # Getting: Some object that's not a dict?

**Diagnosis:**

Check if the result is properly extracted:

.. code-block:: python

   print(f"Result type: {type(result)}")
   print(f"Result value: {result}")
   print(f"Result attributes: {dir(result)}")

**Solutions:**

1. **Access result from execution context**:

   .. code-block:: python

      from mlpy.ml.transpiler import MLTranspiler

      transpiler = MLTranspiler()
      context = {}
      transpiler.execute("result = {name: 'Alice', age: 30};", context)

      # Extract from context
      result = context.get('result')
      print(result)  # {'name': 'Alice', 'age': 30}

2. **Use return statement**:

   .. code-block:: python

      code = """
      function getData() {
          return {name: 'Alice', age: 30};
      }

      result = getData();
      """

      transpiler.execute(code, context)
      print(context['result'])

Callback Issues
^^^^^^^^^^^^^^^

**Problem: Callback Not Found**

.. code-block:: python

   from mlpy.integration import ml_callback
   from mlpy.cli.repl import MLREPLSession

   session = MLREPLSession()
   session.execute_ml_line("function validate(x) { return x > 0; }")

   callback = ml_callback(session, 'validator')  # Wrong name!

   # Error: Function 'validator' not found in session namespace

**Diagnosis:**

Function name mismatch - defined as 'validate' but referenced as 'validator'.

**Solutions:**

1. **Use correct function name**:

   .. code-block:: python

      callback = ml_callback(session, 'validate')  # Matches definition

2. **Verify function exists**:

   .. code-block:: python

      # List all functions in session
      vars = session.get_variables()
      print(f"Available functions: {list(vars.keys())}")

3. **Check function type**:

   .. code-block:: python

      if 'validate' in vars:
          import inspect
          print(f"Is callable: {callable(vars['validate'])}")

**Problem: Callback Arguments Mismatch**

.. code-block:: python

   session.execute_ml_line("function add(a, b) { return a + b; }")
   callback = ml_callback(session, 'add')

   result = callback(5)  # Missing second argument!

   # Error: TypeError: add() missing 1 required positional argument: 'b'

**Diagnosis:**

ML function expects 2 arguments but only 1 was provided.

**Solutions:**

1. **Provide all arguments**:

   .. code-block:: python

      result = callback(5, 10)  # Correct: 2 arguments

2. **Use default parameters in ML**:

   .. code-block:: ml

      function add(a, b) {
          if (typeof(b) == "undefined") {
              b = 0;
          }
          return a + b;
      }

3. **Use varargs pattern**:

   .. code-block:: ml

      function add(...args) {
          result = 0;
          for (i = 0; i < args.length; i = i + 1) {
              result = result + args[i];
          }
          return result;
      }

Async Execution Issues
^^^^^^^^^^^^^^^^^^^^^^^

**Problem: Async Execution Timeout**

.. code-block:: python

   from mlpy.integration import async_ml_execute
   import asyncio

   async def process():
       result = await async_ml_execute(
           "while (true) { x = x + 1; }",  # Infinite loop!
           timeout=5.0
       )

   # Error: asyncio.TimeoutError: ML execution exceeded 5.0 seconds

**Diagnosis:**

ML code is taking too long to execute (infinite loop, heavy computation).

**Solutions:**

1. **Increase timeout** (if legitimate long-running task):

   .. code-block:: python

      result = await async_ml_execute(ml_code, timeout=60.0)

2. **Fix infinite loop** in ML code:

   .. code-block:: ml

      // Bad: Infinite loop
      while (true) { x = x + 1; }

      // Good: Bounded loop
      i = 0;
      while (i < 1000) {
          x = x + 1;
          i = i + 1;
      }

3. **Add progress callback** for long tasks:

   .. code-block:: python

      async def process_with_progress():
          from mlpy.integration import AsyncMLExecutor

          executor = AsyncMLExecutor()

          # Use progress tracking
          ml_code = """
          for (i = 0; i < 1000000; i = i + 1) {
              if (i % 100000 == 0) {
                  console.log("Progress: " + i + "/1000000");
              }
              // ... heavy computation ...
          }
          """

          result = await executor.execute(ml_code, timeout=120.0)

**Problem: Concurrent Execution Errors**

.. code-block:: python

   async def process_batch(items):
       tasks = [async_ml_execute(f"process({item});") for item in items]
       results = await asyncio.gather(*tasks)

   # Some tasks fail with: "Cannot call function from multiple threads"

**Diagnosis:**

ML session state is not thread-safe for concurrent access.

**Solutions:**

1. **Use separate sessions** for concurrent execution:

   .. code-block:: python

      from mlpy.cli.repl import MLREPLSession

      async def process_item(item):
          session = MLREPLSession()  # New session per task
          session.execute_ml_line("function process(x) { return x * 2; }")
          callback = ml_callback(session, 'process')
          return callback(item)

      async def process_batch(items):
          tasks = [process_item(item) for item in items]
          results = await asyncio.gather(*tasks)

2. **Use session pool**:

   .. code-block:: python

      from queue import Queue

      class SessionPool:
          def __init__(self, size=10):
              self.pool = Queue()
              for _ in range(size):
                  session = MLREPLSession()
                  session.execute_ml_line("function process(x) { return x * 2; }")
                  self.pool.put(session)

          def get(self):
              return self.pool.get()

          def release(self, session):
              self.pool.put(session)

      pool = SessionPool(size=5)

      async def process_item(item):
          session = pool.get()
          try:
              callback = ml_callback(session, 'process')
              return callback(item)
          finally:
              pool.release(session)

3. **Use AsyncMLExecutor** (recommended):

   .. code-block:: python

      from mlpy.integration import AsyncMLExecutor

      executor = AsyncMLExecutor(max_workers=5)

      async def process_batch(items):
          ml_code = "function process(x) { return x * 2; }"

          tasks = [
              executor.execute(f"{ml_code}; result = process({item});")
              for item in items
          ]

          results = await asyncio.gather(*tasks)
          return [r.value for r in results if r.success]

Memory Issues
^^^^^^^^^^^^^

**Problem: Memory Leak in Long-Running Integration**

.. code-block:: python

   # Memory grows over time
   for i in range(100000):
       result = execute_ml_code_sandbox(f"result = {i} * 2;")
       # Memory not released!

**Diagnosis:**

Check memory growth:

.. code-block:: python

   import psutil
   import os

   process = psutil.Process(os.getpid())

   initial_memory = process.memory_info().rss / 1024 / 1024  # MB

   for i in range(10000):
       result = execute_ml_code_sandbox(f"result = {i} * 2;")

       if i % 1000 == 0:
           current_memory = process.memory_info().rss / 1024 / 1024
           print(f"Iteration {i}: Memory = {current_memory:.2f} MB "
                 f"(+{current_memory - initial_memory:.2f} MB)")

**Solutions:**

1. **Use context manager** for cleanup:

   .. code-block:: python

      from mlpy.ml.transpiler import MLTranspiler

      for i in range(100000):
          transpiler = MLTranspiler()  # New instance per iteration
          context = {}
          transpiler.execute(f"result = {i} * 2;", context)
          result = context['result']
          # transpiler cleaned up when out of scope

2. **Reuse transpiler with clear context**:

   .. code-block:: python

      transpiler = MLTranspiler()

      for i in range(100000):
          context = {}  # Fresh context each time
          transpiler.execute(f"result = {i} * 2;", context)
          result = context['result']

3. **Explicit garbage collection** (if needed):

   .. code-block:: python

      import gc

      for i in range(100000):
          result = execute_ml_code_sandbox(f"result = {i} * 2;")

          if i % 1000 == 0:
              gc.collect()  # Force garbage collection

4. **Use batch processing**:

   .. code-block:: python

      # Instead of processing one at a time:
      for item in items:
          result = execute_ml_code_sandbox(f"process({item});")

      # Process in batches:
      ml_code = """
      function processBatch(items) {
          results = [];
          for (i = 0; i < items.length; i = i + 1) {
              results.push(process(items[i]));
          }
          return results;
      }
      """

      batch_size = 100
      for i in range(0, len(items), batch_size):
          batch = items[i:i+batch_size]
          results = execute_ml_code_sandbox(
              f"{ml_code}; result = processBatch({batch});"
          )

**Problem: Large Data Transfer**

.. code-block:: python

   # Passing huge dataset
   data = list(range(1000000))  # 1 million items

   result = execute_ml_code_sandbox(
       "function sum(arr) { total = 0; for(i=0; i<arr.length; i++) total += arr[i]; return total; }",
       context={'arr': data}
   )

   # Slow and memory-intensive!

**Solutions:**

1. **Process in chunks**:

   .. code-block:: python

      chunk_size = 10000
      total = 0

      for i in range(0, len(data), chunk_size):
          chunk = data[i:i+chunk_size]
          result = execute_ml_code_sandbox(
              "function sum(arr) { ... }",
              context={'arr': chunk}
          )
          total += result

2. **Use Python for heavy processing**:

   .. code-block:: python

      # Instead of ML:
      result = execute_ml_code_sandbox("...", context={'arr': huge_data})

      # Use Python:
      total = sum(data)  # Native Python is faster!

      # Use ML only for business logic:
      result = execute_ml_code_sandbox(
          "function calculateTax(total) { return total * 0.15; }",
          context={'total': total}
      )

3. **Stream data** instead of loading all at once:

   .. code-block:: python

      def process_stream(data_generator):
          ml_code = "function process(item) { return item * 2; }"

          for batch in data_generator:
              results = execute_ml_code_sandbox(
                  f"{ml_code}; result = batch.map(process);",
                  context={'batch': batch}
              )
              yield results

Debugging Tools and Techniques
-------------------------------

Using Source Maps
^^^^^^^^^^^^^^^^^

ML-to-Python transpilation includes source maps for accurate error reporting.

**Accessing Source Maps:**

.. code-block:: python

   from mlpy.ml.transpiler import MLTranspiler

   transpiler = MLTranspiler()
   result = transpiler.transpile("function add(a, b) { return a + b; }")

   print(f"Transpiled Python code:\n{result.python_code}")
   print(f"\nSource map:\n{result.source_map}")

**Understanding Source Map Format:**

.. code-block:: json

   {
     "version": 3,
     "sources": ["input.ml"],
     "mappings": [
       {"ml_line": 1, "ml_col": 0, "py_line": 1, "py_col": 0},
       {"ml_line": 1, "ml_col": 18, "py_line": 2, "py_col": 4}
     ]
   }

**Using Source Maps for Error Location:**

.. code-block:: python

   try:
       result = transpiler.execute(ml_code, context)
   except Exception as e:
       import traceback

       # Get Python traceback
       tb = traceback.extract_tb(e.__traceback__)

       # Map back to ML source
       for frame in tb:
           if frame.filename.endswith('.ml'):
               ml_line = result.source_map.map_py_to_ml(frame.lineno)
               print(f"Error at ML line {ml_line}: {frame.line}")

Logging and Tracing
^^^^^^^^^^^^^^^^^^^

**Enable ML Execution Logging:**

.. code-block:: python

   import logging

   # Configure logging
   logging.basicConfig(level=logging.DEBUG)

   # Enable ML transpiler logging
   ml_logger = logging.getLogger('mlpy.ml.transpiler')
   ml_logger.setLevel(logging.DEBUG)

   # Enable integration logging
   integration_logger = logging.getLogger('mlpy.integration')
   integration_logger.setLevel(logging.DEBUG)

**Custom Logging in ML Code:**

.. code-block:: ml

   function processOrder(order) {
       console.log("Processing order: " + order.id);

       if (!validateOrder(order)) {
           console.error("Order validation failed: " + order.id);
           return {success: false, error: "Invalid order"};
       }

       console.log("Order validated successfully");
       return {success: true};
   }

**Capture ML Console Output:**

.. code-block:: python

   import io
   import sys

   # Capture console output
   captured_output = io.StringIO()
   sys.stdout = captured_output

   try:
       result = execute_ml_code_sandbox(ml_code)
   finally:
       sys.stdout = sys.__stdout__

   # Get logged output
   console_log = captured_output.getvalue()
   print(f"ML console output:\n{console_log}")

**Distributed Tracing:**

.. code-block:: python

   from opentelemetry import trace
   from opentelemetry.sdk.trace import TracerProvider
   from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

   # Configure tracing
   provider = TracerProvider()
   processor = SimpleSpanProcessor(ConsoleSpanExporter())
   provider.add_span_processor(processor)
   trace.set_tracer_provider(provider)

   tracer = trace.get_tracer(__name__)

   # Trace ML execution
   with tracer.start_as_current_span("ml_execution"):
       with tracer.start_as_current_span("transpile"):
           result = transpiler.transpile(ml_code)

       with tracer.start_as_current_span("execute"):
           output = transpiler.execute(result.python_code, context)

Performance Profiling
^^^^^^^^^^^^^^^^^^^^^^

**Profile ML Execution Time:**

.. code-block:: python

   import time

   # Simple timing
   start = time.perf_counter()
   result = execute_ml_code_sandbox(ml_code)
   end = time.perf_counter()

   print(f"Execution time: {(end - start) * 1000:.3f}ms")

**Detailed Profiling:**

.. code-block:: python

   from mlpy.runtime.profiler import MLProfiler

   profiler = MLProfiler()
   profiler.enable()

   result = execute_ml_code_sandbox(ml_code)

   profiler.disable()
   stats = profiler.get_stats()

   print(f"Transpilation time: {stats['transpile_time']:.3f}ms")
   print(f"Execution time: {stats['execute_time']:.3f}ms")
   print(f"Total time: {stats['total_time']:.3f}ms")

**Using cProfile:**

.. code-block:: python

   import cProfile
   import pstats

   profiler = cProfile.Profile()
   profiler.enable()

   result = execute_ml_code_sandbox(ml_code)

   profiler.disable()

   # Print stats
   stats = pstats.Stats(profiler)
   stats.sort_stats('cumulative')
   stats.print_stats(20)  # Top 20 functions

**Memory Profiling:**

.. code-block:: python

   from memory_profiler import profile

   @profile
   def process_ml():
       for i in range(1000):
           result = execute_ml_code_sandbox(f"result = {i} * 2;")

   process_ml()

**Integration Toolkit Performance Testing:**

.. code-block:: python

   from mlpy.integration.testing.performance import PerformanceTester

   tester = PerformanceTester()

   # Benchmark async execution
   results = await tester.benchmark_async_execution(
       ml_code,
       iterations=100
   )

   print(f"Mean: {results['mean']*1000:.3f}ms")
   print(f"Median: {results['median']*1000:.3f}ms")
   print(f"Std Dev: {results['std_dev']*1000:.3f}ms")

   # Benchmark concurrent execution
   results = await tester.benchmark_concurrent_executions(
       ml_code,
       concurrency=50
   )

   print(f"Throughput: {results['throughput']:.2f} exec/sec")

REPL Debugging
^^^^^^^^^^^^^^

**Interactive Debugging with REPL:**

.. code-block:: python

   from mlpy.cli.repl import MLREPLSession

   session = MLREPLSession()

   # Define function interactively
   session.execute_ml_line("function calculateTax(amount) {")
   session.execute_ml_line("  rate = 0.15;")
   session.execute_ml_line("  return amount * rate;")
   session.execute_ml_line("}")

   # Test function
   result = session.execute_ml_line("calculateTax(100);")
   print(f"Result: {result}")

   # Inspect variables
   vars = session.get_variables()
   print(f"Variables: {vars.keys()}")

**REPL Commands for Debugging:**

.. code-block:: text

   mlpy> .help
   Available commands:
     .async <code>     - Execute ML code asynchronously
     .callback <func>  - Create Python callback from ML function
     .benchmark <code> - Benchmark ML code execution
     .vars             - Show all variables
     .modules          - Show loaded modules
     .reload <module>  - Reload a module
     .perfmon          - Show performance metrics

**Debugging Callbacks:**

.. code-block:: python

   session = MLREPLSession()
   session.execute_ml_line("function validate(x) { return x > 0; }")

   from mlpy.integration import ml_callback

   callback = ml_callback(session, 'validate')

   # Add debug wrapper
   def debug_callback(*args, **kwargs):
       print(f"Calling validate with args={args}, kwargs={kwargs}")
       result = callback(*args, **kwargs)
       print(f"Result: {result}")
       return result

   # Use debug wrapper
   result = debug_callback(42)

Best Practices
--------------

Systematic Debugging Approach
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. **Reproduce the Issue:**

   Create minimal reproduction case:

   .. code-block:: python

      # Minimal test case
      ml_code = "result = 2 + 2;"
      result = execute_ml_code_sandbox(ml_code)
      assert result == 4

2. **Isolate the Problem:**

   Test each component separately:

   .. code-block:: python

      # Test transpilation
      transpiler = MLTranspiler()
      transpile_result = transpiler.transpile(ml_code)
      print(f"Transpiled: {transpile_result.python_code}")

      # Test execution
      exec_result = transpiler.execute(transpile_result.python_code, {})

3. **Add Logging:**

   .. code-block:: python

      import logging
      logging.basicConfig(level=logging.DEBUG)

      result = execute_ml_code_sandbox(ml_code)

4. **Use Debugging Tools:**

   * Python debugger (pdb)
   * REPL for interactive testing
   * Performance profiler
   * Memory profiler

5. **Check Common Issues:**

   * Module not found?
   * Type conversion error?
   * Security violation?
   * Timeout?

6. **Document the Solution:**

   Once fixed, document for future reference.

Development vs Production Debugging
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Development:**

.. code-block:: python

   # Enable all debugging
   import logging
   logging.basicConfig(level=logging.DEBUG)

   # Use REPL for interactive testing
   from mlpy.cli.repl import MLREPLSession
   session = MLREPLSession()

   # Enable performance monitoring
   from mlpy.stdlib.module_registry import get_registry
   registry = get_registry()
   registry.enable_performance_mode()

**Production:**

.. code-block:: python

   # Minimal logging
   import logging
   logging.basicConfig(level=logging.WARNING)

   # Structured logging
   import structlog
   logger = structlog.get_logger()

   try:
       result = execute_ml_code_sandbox(ml_code)
       logger.info("ml_execution_success", execution_time=result.execution_time)
   except Exception as e:
       logger.error("ml_execution_failed", error=str(e), ml_code=ml_code)
       raise

**Error Monitoring:**

.. code-block:: python

   # Sentry integration
   import sentry_sdk

   sentry_sdk.init(dsn="your-dsn-here")

   try:
       result = execute_ml_code_sandbox(ml_code)
   except Exception as e:
       sentry_sdk.capture_exception(e)
       raise

Summary
-------

**Key Takeaways:**

* Use systematic debugging approach: reproduce, isolate, log, debug, document
* Leverage ML-specific tools: REPL, source maps, Integration Toolkit utilities
* Understand common issues: module imports, type conversion, callbacks, async
* Profile performance and memory for optimization
* Different strategies for development vs production debugging

**Next Steps:**

* Read :doc:`error-analysis` for detailed error handling strategies
* See :doc:`performance` for performance troubleshooting techniques
* Check :doc:`common-issues` for specific problem solutions

----

**Related Documentation:**

* :doc:`/integration-guide/patterns/async-integration` - Async execution patterns
* :doc:`/integration-guide/patterns/callbacks` - ML callback usage
* :doc:`/user-guide/toolkit/repl-guide` - REPL reference
* :doc:`/integration-guide/testing/best-practices` - Testing strategies
