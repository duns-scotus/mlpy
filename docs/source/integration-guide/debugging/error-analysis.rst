Error Analysis and Recovery
============================

.. note::
   **Chapter Summary:** Comprehensive guide to understanding, analyzing, and recovering from errors in ML-Python integration.

.. contents:: In This Chapter
   :local:
   :depth: 2

Overview
--------

Error analysis is crucial for building robust ML-Python integrations. This chapter provides systematic approaches to understanding error types, analyzing stack traces, implementing recovery strategies, and building production-ready error handling.

**What You'll Learn:**

* ML error type classification and characteristics
* Stack trace analysis across the ML-Python boundary
* Error recovery patterns and strategies
* Custom error handler implementation
* Production error reporting and monitoring
* Building fault-tolerant integrations

**Prerequisites:**

* Understanding of Python exception handling
* Familiarity with ML language execution model
* Basic knowledge of the Integration Toolkit

Error Types and Classification
-------------------------------

ML Runtime Errors
^^^^^^^^^^^^^^^^^

**ParseError - Syntax Issues**

Occurs during ML code parsing when syntax is invalid.

.. code-block:: python

   from mlpy.ml.transpiler import MLTranspiler
   from mlpy.ml.errors.exceptions import ParseError

   transpiler = MLTranspiler()

   try:
       result = transpiler.transpile("function add(a, b { return a + b; }")
       # Missing closing parenthesis before {
   except ParseError as e:
       print(f"Parse error: {e}")
       print(f"Line: {e.line}")
       print(f"Column: {e.column}")
       print(f"Expected: {e.expected}")

**Error Details:**

===============================  ================================================
Attribute                         Description
===============================  ================================================
``e.message``                     Human-readable error message
``e.line``                        Line number where error occurred
``e.column``                      Column number in the line
``e.expected``                    What the parser expected
``e.context``                     Surrounding code context
``e.suggestions``                 Suggested fixes
===============================  ================================================

**Common Parse Errors:**

1. **Missing Parentheses/Braces:**

   .. code-block:: ml

      // Error: Missing )
      function add(a, b { return a + b; }

      // Correct:
      function add(a, b) { return a + b; }

2. **Invalid Token:**

   .. code-block:: ml

      // Error: @ is not a valid token
      result = 5 @ 3;

      // Correct:
      result = 5 + 3;

3. **Unexpected End of Input:**

   .. code-block:: ml

      // Error: Unclosed string
      message = "Hello, world;

      // Correct:
      message = "Hello, world";

**TranspilationError - Code Generation Issues**

Occurs during Python code generation from ML AST.

.. code-block:: python

   from mlpy.ml.errors.exceptions import TranspilationError

   try:
       result = transpiler.transpile(ml_code)
   except TranspilationError as e:
       print(f"Transpilation error: {e}")
       print(f"AST node type: {e.node_type}")
       print(f"Reason: {e.reason}")

**Common Transpilation Errors:**

1. **Unsupported Language Feature:**

   .. code-block:: ml

      // Error: Decorators not yet supported
      @cached
      function expensive() { ... }

2. **Invalid AST Structure:**

   .. code-block:: text

      TranspilationError: Invalid AST node: expected Expression, got Statement

**RuntimeError - Execution Errors**

Occurs during ML code execution in Python.

.. code-block:: python

   from mlpy.ml.errors.exceptions import RuntimeError

   try:
       result = transpiler.execute("result = 1 / 0;", {})
   except RuntimeError as e:
       print(f"Runtime error: {e}")
       print(f"Error type: {e.error_type}")  # 'ZeroDivisionError'
       print(f"Stack trace: {e.stack_trace}")

**Common Runtime Errors:**

1. **Division by Zero:**

   .. code-block:: ml

      result = 10 / 0;  // ZeroDivisionError

2. **Undefined Variable:**

   .. code-block:: ml

      result = unknownVar + 5;  // NameError: 'unknownVar' is not defined

3. **Type Error:**

   .. code-block:: ml

      result = "hello" - 5;  // TypeError: unsupported operand type(s)

4. **Index Out of Bounds:**

   .. code-block:: ml

      arr = [1, 2, 3];
      result = arr[10];  // IndexError: list index out of range

Security Errors
^^^^^^^^^^^^^^^

**SecurityError - Policy Violations**

Occurs when ML code attempts unauthorized operations.

.. code-block:: python

   from mlpy.ml.errors.exceptions import SecurityError

   try:
       result = transpiler.execute("import os; os.system('rm -rf /');", {})
   except SecurityError as e:
       print(f"Security violation: {e}")
       print(f"Violation type: {e.violation_type}")
       print(f"Blocked operation: {e.operation}")
       print(f"Required capability: {e.required_capability}")

**Security Error Types:**

1. **Unauthorized Module Import:**

   .. code-block:: ml

      import os;  // SecurityError: Module 'os' not allowed

   **Required Fix:** Grant capability or use safe alternative:

   .. code-block:: python

      # Option 1: Grant capability (if safe)
      from mlpy.runtime.capabilities.tokens import CapabilityToken

      caps = {CapabilityToken('import', pattern='os')}
      result = transpiler.execute(ml_code, {}, capabilities=caps)

      # Option 2: Use safe alternative
      result = transpiler.execute("import file; file.read('/data.txt');", {})

2. **Unauthorized File Access:**

   .. code-block:: ml

      import file;
      content = file.read('/etc/passwd');  // SecurityError: No read capability

   **Required Fix:**

   .. code-block:: python

      from mlpy.runtime.capabilities.manager import file_capability_context

      with file_capability_context(action='read', pattern='/data/*'):
          result = transpiler.execute(ml_code, {})

3. **Unauthorized Network Access:**

   .. code-block:: ml

      import http;
      response = http.get('http://evil.com');  // SecurityError: No network capability

   **Required Fix:**

   .. code-block:: python

      from mlpy.runtime.capabilities.manager import network_capability_context

      with network_capability_context(action='http', pattern='api.example.com'):
          result = transpiler.execute(ml_code, {})

**CapabilityError - Permission Issues**

Occurs when required capabilities are missing or invalid.

.. code-block:: python

   from mlpy.ml.errors.exceptions import CapabilityError

   try:
       # Try to access file without capability
       result = transpiler.execute("import file; file.write('/tmp/test', 'data');", {})
   except CapabilityError as e:
       print(f"Capability error: {e}")
       print(f"Required capability: {e.required_capability}")
       print(f"Available capabilities: {e.available_capabilities}")

Integration Errors
^^^^^^^^^^^^^^^^^^

**CallbackError - Callback Execution Issues**

Occurs when ML callbacks fail.

.. code-block:: python

   from mlpy.integration.ml_callback import ml_callback, CallbackError
   from mlpy.cli.repl import MLREPLSession

   session = MLREPLSession()
   session.execute_ml_line("function validate(x) { return x > 0; }")

   callback = ml_callback(session, 'validate')

   try:
       result = callback("not a number")  // Type error
   except CallbackError as e:
       print(f"Callback error: {e}")
       print(f"Function name: {e.function_name}")
       print(f"Arguments: {e.arguments}")
       print(f"Original error: {e.original_error}")

**AsyncExecutionError - Async Issues**

Occurs during asynchronous ML execution.

.. code-block:: python

   from mlpy.integration import async_ml_execute, AsyncExecutionError
   import asyncio

   async def process():
       try:
           result = await async_ml_execute("while(true) {}", timeout=5.0)
       except AsyncExecutionError as e:
           print(f"Async execution error: {e}")
           print(f"Timeout: {e.timeout}")
           print(f"Elapsed time: {e.elapsed_time}")
           print(f"Error type: {e.error_type}")  # 'TimeoutError'

**TimeoutError - Execution Timeout**

Occurs when ML execution exceeds timeout limit.

.. code-block:: python

   import asyncio

   async def long_running():
       try:
           result = await async_ml_execute(
               """
               // Simulate long computation
               total = 0;
               for (i = 0; i < 100000000; i = i + 1) {
                   total = total + i;
               }
               result = total;
               """,
               timeout=1.0  // 1 second timeout
           )
       except asyncio.TimeoutError as e:
           print("Execution timed out after 1 second")
           # Implement recovery strategy

Stack Trace Analysis
--------------------

Understanding ML Stack Traces
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ML errors generate stack traces that span both ML and Python code.

**Example Error:**

.. code-block:: ml

   function processOrder(order) {
       return calculateTotal(order.items);
   }

   function calculateTotal(items) {
       total = 0;
       for (i = 0; i < items.length; i = i + 1) {
           total = total + items[i].price * items[i].quantity;
       }
       return total;
   }

   result = processOrder({items: [{price: "invalid"}]});

**Generated Stack Trace:**

.. code-block:: text

   Traceback (most recent call last):
     File "<ml_execution>", line 12, in <module>
       result = processOrder({items: [{price: "invalid"}]})
     File "<ml_execution>", line 2, in processOrder
       return calculateTotal(order.items)
     File "<ml_execution>", line 7, in calculateTotal
       total = total + items[i].price * items[i].quantity
   TypeError: can't multiply sequence by non-int of type 'str'

   ML Source Context:
     Line 7:     total = total + items[i].price * items[i].quantity;
                                      ^^^^^^^^^^^^^^^^^^^

**Analyzing the Stack Trace:**

1. **Error Location:** Line 7 in calculateTotal function
2. **Error Type:** TypeError (type mismatch)
3. **Root Cause:** items[i].price is "invalid" (string), not a number
4. **Call Chain:** processOrder → calculateTotal

Mapping Python Traces to ML Source
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Using Source Maps:**

.. code-block:: python

   from mlpy.ml.transpiler import MLTranspiler
   import traceback

   transpiler = MLTranspiler()
   ml_code = """
   function divide(a, b) {
       return a / b;
   }

   result = divide(10, 0);
   """

   try:
       result = transpiler.execute(ml_code, {})
   except Exception as e:
       # Get Python traceback
       tb_lines = traceback.format_exception(type(e), e, e.__traceback__)

       # Map to ML source using source map
       for line in tb_lines:
           print(line)

       # Get ML-specific context
       if hasattr(e, 'ml_context'):
           print(f"\nML Context:")
           print(f"  File: {e.ml_context.filename}")
           print(f"  Line: {e.ml_context.line}")
           print(f"  Column: {e.ml_context.column}")
           print(f"  Source: {e.ml_context.source_line}")

**Enhanced Error Context:**

.. code-block:: python

   from mlpy.ml.errors.context import create_error_context
   from mlpy.debugging.error_formatter import error_formatter

   try:
       result = transpiler.execute(ml_code, {})
   except Exception as e:
       # Create rich error context
       error_context = create_error_context(e)

       # Format and display
       error_formatter.print_error(error_context)

       # Programmatic access
       print(f"Error type: {error_context.error_type}")
       print(f"Message: {error_context.message}")
       print(f"Suggestions: {error_context.suggestions}")
       print(f"Code snippet: {error_context.code_snippet}")

Identifying Root Causes
^^^^^^^^^^^^^^^^^^^^^^^^

**Systematic Root Cause Analysis:**

1. **Read Error Message:**

   .. code-block:: text

      TypeError: unsupported operand type(s) for +: 'int' and 'str'

   → Type mismatch: trying to add int and str

2. **Examine Stack Trace:**

   .. code-block:: text

      File "<ml>", line 15, in calculateTotal
        total = total + item.price

   → Error occurs at line 15 in calculateTotal

3. **Check Variable Types:**

   .. code-block:: python

      # Add debug logging
      ml_code_with_debug = """
      function calculateTotal(items) {
          total = 0;
          for (i = 0; i < items.length; i = i + 1) {
              console.log("item.price type: " + typeof(items[i].price));
              console.log("item.price value: " + items[i].price);
              total = total + items[i].price;
          }
          return total;
      }
      """

4. **Trace Data Flow:**

   .. code-block:: text

      Input: {items: [{price: "10.99"}]}
                              ^^^^^^^ String, not number!

5. **Identify Fix:**

   .. code-block:: ml

      // Option 1: Convert to number in ML
      total = total + parseFloat(items[i].price);

      // Option 2: Validate input in Python
      items = [{'price': float(item['price'])} for item in raw_items]

Error Recovery Strategies
--------------------------

Retry Patterns
^^^^^^^^^^^^^^

**Simple Retry:**

.. code-block:: python

   def execute_with_retry(ml_code, max_retries=3):
       """Execute ML code with automatic retry on failure."""
       for attempt in range(max_retries):
           try:
               result = execute_ml_code_sandbox(ml_code)
               return result
           except Exception as e:
               if attempt == max_retries - 1:
                   # Last attempt failed
                   raise
               else:
                   print(f"Attempt {attempt + 1} failed: {e}")
                   print(f"Retrying... ({max_retries - attempt - 1} attempts left)")
                   time.sleep(1)  # Wait before retry

**Exponential Backoff:**

.. code-block:: python

   import time

   def execute_with_backoff(ml_code, max_retries=5):
       """Execute with exponential backoff."""
       for attempt in range(max_retries):
           try:
               result = execute_ml_code_sandbox(ml_code)
               return result
           except Exception as e:
               if attempt == max_retries - 1:
                   raise

               # Exponential backoff: 1s, 2s, 4s, 8s, 16s
               wait_time = 2 ** attempt
               print(f"Attempt {attempt + 1} failed, waiting {wait_time}s before retry")
               time.sleep(wait_time)

**Selective Retry (only for transient errors):**

.. code-block:: python

   from mlpy.ml.errors.exceptions import TimeoutError, NetworkError

   RETRYABLE_ERRORS = (TimeoutError, NetworkError, ConnectionError)

   def execute_with_selective_retry(ml_code, max_retries=3):
       """Retry only for transient errors."""
       for attempt in range(max_retries):
           try:
               result = execute_ml_code_sandbox(ml_code)
               return result
           except RETRYABLE_ERRORS as e:
               if attempt == max_retries - 1:
                   raise
               print(f"Transient error: {e}, retrying...")
               time.sleep(1)
           except Exception as e:
               # Don't retry for non-transient errors
               print(f"Non-retryable error: {e}")
               raise

Fallback Strategies
^^^^^^^^^^^^^^^^^^^

**Default Value Fallback:**

.. code-block:: python

   def execute_with_default(ml_code, default_value=None):
       """Return default value on error."""
       try:
           result = execute_ml_code_sandbox(ml_code)
           return result
       except Exception as e:
           print(f"Error executing ML code: {e}")
           print(f"Returning default value: {default_value}")
           return default_value

   # Usage
   result = execute_with_default(
       "result = riskyOperation();",
       default_value={'status': 'error', 'value': None}
   )

**Alternative Implementation Fallback:**

.. code-block:: python

   def calculate_with_fallback(items):
       """Try ML calculation, fall back to Python if it fails."""
       ml_code = """
       function calculateTotal(items) {
           total = 0;
           for (i = 0; i < items.length; i = i + 1) {
               total = total + items[i].price * items[i].quantity;
           }
           return total;
       }

       result = calculateTotal(items);
       """

       try:
           # Try ML implementation
           result = execute_ml_code_sandbox(ml_code, context={'items': items})
           return result
       except Exception as e:
           print(f"ML calculation failed: {e}")
           print("Falling back to Python implementation")

           # Fallback to Python
           total = sum(item['price'] * item['quantity'] for item in items)
           return total

**Graceful Degradation:**

.. code-block:: python

   def process_with_degradation(data):
       """Degrade functionality gracefully on error."""
       results = {
           'processed': False,
           'data': None,
           'validation': None,
           'enrichment': None
       }

       try:
           # Core processing (required)
           ml_result = execute_ml_code_sandbox(
               "result = processData(data);",
               context={'data': data}
           )
           results['processed'] = True
           results['data'] = ml_result

       except Exception as e:
           print(f"Core processing failed: {e}")
           return results  # Return partial results

       try:
           # Validation (optional)
           validation = execute_ml_code_sandbox(
               "result = validateData(data);",
               context={'data': ml_result}
           )
           results['validation'] = validation
       except Exception as e:
           print(f"Validation failed: {e} (continuing without validation)")

       try:
           # Enrichment (optional)
           enriched = execute_ml_code_sandbox(
               "result = enrichData(data);",
               context={'data': ml_result}
           )
           results['enrichment'] = enriched
       except Exception as e:
           print(f"Enrichment failed: {e} (continuing without enrichment)")

       return results

Circuit Breaker Pattern
^^^^^^^^^^^^^^^^^^^^^^^^

**Preventing Cascade Failures:**

.. code-block:: python

   from enum import Enum
   from datetime import datetime, timedelta

   class CircuitState(Enum):
       CLOSED = "closed"      # Normal operation
       OPEN = "open"          # Failure threshold exceeded
       HALF_OPEN = "half_open"  # Testing recovery

   class CircuitBreaker:
       """Circuit breaker for ML execution."""

       def __init__(self, failure_threshold=5, timeout=60):
           self.failure_threshold = failure_threshold
           self.timeout = timeout  # Seconds before trying again
           self.failure_count = 0
           self.last_failure_time = None
           self.state = CircuitState.CLOSED

       def call(self, ml_code):
           """Execute ML code through circuit breaker."""
           if self.state == CircuitState.OPEN:
               # Check if timeout has passed
               if datetime.now() - self.last_failure_time > timedelta(seconds=self.timeout):
                   self.state = CircuitState.HALF_OPEN
                   print("Circuit breaker: Entering HALF_OPEN state")
               else:
                   raise Exception("Circuit breaker is OPEN - service unavailable")

           try:
               result = execute_ml_code_sandbox(ml_code)

               # Success - reset on HALF_OPEN
               if self.state == CircuitState.HALF_OPEN:
                   self.state = CircuitState.CLOSED
                   self.failure_count = 0
                   print("Circuit breaker: Service recovered, back to CLOSED state")

               return result

           except Exception as e:
               self.failure_count += 1
               self.last_failure_time = datetime.now()

               if self.failure_count >= self.failure_threshold:
                   self.state = CircuitState.OPEN
                   print(f"Circuit breaker: OPEN after {self.failure_count} failures")

               raise

   # Usage
   breaker = CircuitBreaker(failure_threshold=5, timeout=60)

   try:
       result = breaker.call("result = processData(data);")
   except Exception as e:
       print(f"Call failed: {e}")

Custom Error Handlers
---------------------

Global Error Handler
^^^^^^^^^^^^^^^^^^^^

**Registering Global Handler:**

.. code-block:: python

   from mlpy.ml.transpiler import MLTranspiler

   class CustomErrorHandler:
       """Custom error handler for ML execution."""

       def handle_parse_error(self, error):
           """Handle parse errors."""
           print(f"[PARSE ERROR] {error.message}")
           print(f"  Location: Line {error.line}, Column {error.column}")
           print(f"  Expected: {error.expected}")

           # Log to external service
           self.log_error('parse_error', error)

           # Return formatted error response
           return {
               'error_type': 'parse_error',
               'message': error.message,
               'line': error.line,
               'column': error.column
           }

       def handle_runtime_error(self, error):
           """Handle runtime errors."""
           print(f"[RUNTIME ERROR] {error.message}")
           print(f"  Type: {error.error_type}")
           print(f"  Stack: {error.stack_trace}")

           # Log to external service
           self.log_error('runtime_error', error)

           return {
               'error_type': 'runtime_error',
               'message': error.message,
               'stack_trace': error.stack_trace
           }

       def handle_security_error(self, error):
           """Handle security violations."""
           print(f"[SECURITY ERROR] {error.message}")
           print(f"  Violation: {error.violation_type}")
           print(f"  Operation: {error.operation}")

           # Security incidents require special handling
           self.log_security_incident(error)

           return {
               'error_type': 'security_error',
               'message': 'Operation not permitted',
               'violation_type': error.violation_type
           }

       def log_error(self, error_type, error):
           """Log error to external service."""
           # Example: Send to logging service
           import logging
           logger = logging.getLogger('mlpy.errors')
           logger.error(f"{error_type}: {error.message}", extra={
               'error_type': error_type,
               'error_details': str(error)
           })

       def log_security_incident(self, error):
           """Log security incident."""
           # Security incidents need special attention
           import logging
           logger = logging.getLogger('mlpy.security')
           logger.critical(f"Security violation: {error.message}", extra={
               'violation_type': error.violation_type,
               'operation': error.operation,
               'required_capability': error.required_capability
           })

   # Register handler
   error_handler = CustomErrorHandler()

   def execute_with_error_handling(ml_code):
       """Execute ML code with custom error handling."""
       from mlpy.ml.errors.exceptions import ParseError, RuntimeError, SecurityError

       try:
           transpiler = MLTranspiler()
           result = transpiler.execute(ml_code, {})
           return {'success': True, 'result': result}

       except ParseError as e:
           return error_handler.handle_parse_error(e)

       except SecurityError as e:
           return error_handler.handle_security_error(e)

       except RuntimeError as e:
           return error_handler.handle_runtime_error(e)

       except Exception as e:
           # Catch-all for unexpected errors
           print(f"[UNEXPECTED ERROR] {e}")
           error_handler.log_error('unexpected_error', e)
           return {
               'error_type': 'unexpected_error',
               'message': str(e)
           }

Context-Specific Handlers
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Web Framework Error Handler:**

.. code-block:: python

   from flask import Flask, jsonify
   from mlpy.ml.errors.exceptions import MLError

   app = Flask(__name__)

   @app.errorhandler(MLError)
   def handle_ml_error(error):
       """Handle ML errors in Flask."""
       response = {
           'error': 'ML execution failed',
           'message': error.message,
           'type': error.error_type,
           'details': error.context
       }

       # Different status codes for different errors
       status_code = {
           'ParseError': 400,  # Bad Request
           'SecurityError': 403,  # Forbidden
           'RuntimeError': 500,  # Internal Server Error
           'TimeoutError': 504  # Gateway Timeout
       }.get(error.error_type, 500)

       return jsonify(response), status_code

   @app.route('/execute', methods=['POST'])
   def execute():
       """Execute ML code endpoint."""
       from flask import request

       ml_code = request.json.get('code')

       # This will be caught by handle_ml_error if it fails
       result = execute_ml_code_sandbox(ml_code)

       return jsonify({'success': True, 'result': result})

**Async Error Handler:**

.. code-block:: python

   import asyncio
   from mlpy.integration import async_ml_execute

   async def execute_with_async_error_handling(ml_code):
       """Async execution with comprehensive error handling."""
       try:
           result = await async_ml_execute(ml_code, timeout=30.0)
           return {'success': True, 'result': result.value}

       except asyncio.TimeoutError:
           return {
               'success': False,
               'error': 'timeout',
               'message': 'ML execution timed out after 30 seconds'
           }

       except Exception as e:
           return {
               'success': False,
               'error': 'execution_failed',
               'message': str(e)
           }

Production Error Monitoring
----------------------------

Structured Error Logging
^^^^^^^^^^^^^^^^^^^^^^^^^

**Using structlog:**

.. code-block:: python

   import structlog

   logger = structlog.get_logger()

   def execute_with_structured_logging(ml_code, context=None):
       """Execute ML code with structured logging."""
       logger.info("ml_execution_started", ml_code_length=len(ml_code))

       try:
           result = execute_ml_code_sandbox(ml_code, context=context or {})

           logger.info("ml_execution_success",
                      execution_time=result.execution_time,
                      result_type=type(result).__name__)

           return result

       except Exception as e:
           logger.error("ml_execution_failed",
                       error_type=type(e).__name__,
                       error_message=str(e),
                       ml_code_snippet=ml_code[:100])
           raise

Error Aggregation
^^^^^^^^^^^^^^^^^

**Sentry Integration:**

.. code-block:: python

   import sentry_sdk
   from sentry_sdk.integrations.logging import LoggingIntegration

   # Configure Sentry
   sentry_sdk.init(
       dsn="your-sentry-dsn",
       integrations=[LoggingIntegration()],
       traces_sample_rate=0.1,
       environment="production"
   )

   def execute_with_sentry(ml_code):
       """Execute ML code with Sentry error tracking."""
       try:
           result = execute_ml_code_sandbox(ml_code)
           return result

       except Exception as e:
           # Capture exception with context
           with sentry_sdk.push_scope() as scope:
               scope.set_tag("component", "ml_integration")
               scope.set_context("ml_code", {
                   "length": len(ml_code),
                   "snippet": ml_code[:200]
               })
               sentry_sdk.capture_exception(e)

           raise

**Custom Error Metrics:**

.. code-block:: python

   from prometheus_client import Counter, Histogram

   # Define metrics
   ml_errors_total = Counter(
       'ml_errors_total',
       'Total number of ML execution errors',
       ['error_type']
   )

   ml_execution_duration = Histogram(
       'ml_execution_duration_seconds',
       'ML execution duration',
       buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 5.0]
   )

   def execute_with_metrics(ml_code):
       """Execute ML code with metrics collection."""
       import time

       start = time.time()

       try:
           result = execute_ml_code_sandbox(ml_code)

           # Record success duration
           ml_execution_duration.observe(time.time() - start)

           return result

       except Exception as e:
           # Record error
           error_type = type(e).__name__
           ml_errors_total.labels(error_type=error_type).inc()

           # Record failure duration
           ml_execution_duration.observe(time.time() - start)

           raise

Summary
-------

**Key Takeaways:**

* Understand ML error taxonomy: Parse, Runtime, Security, Integration errors
* Analyze stack traces systematically using source maps
* Implement recovery strategies: retry, fallback, circuit breaker
* Use custom error handlers for production-grade error management
* Monitor errors with structured logging and aggregation tools

**Error Handling Best Practices:**

1. **Catch Specific Exceptions:** Don't use bare ``except:``
2. **Log With Context:** Include ML code snippet, arguments, environment
3. **Fail Fast:** Don't hide errors, surface them appropriately
4. **Recover Gracefully:** Use fallback strategies for non-critical failures
5. **Monitor Production:** Track error rates, types, and trends

**Next Steps:**

* Read :doc:`performance` for performance troubleshooting
* See :doc:`security-debugging` for security-specific debugging
* Check :doc:`common-issues` for known issues and solutions

----

**Related Documentation:**

* :doc:`/integration-guide/foundation/security` - Security model details
* :doc:`/integration-guide/testing/best-practices` - Testing error scenarios
* :doc:`/user-guide/errors/error-reference` - Complete error reference
