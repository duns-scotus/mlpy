Import Patterns and Module Identity
====================================

.. note::
   **Chapter Summary:** Best practices for importing ML standard library modules and understanding module identity in Python-ML integration.

Overview
--------

When integrating ML code with Python applications, proper import patterns are crucial for ensuring type consistency, isinstance() checks, and proper capability context management. This guide covers the recommended patterns and explains how the ML module system works with Python's import mechanism.

Understanding Module Identity
-----------------------------

Module Registry and sys.modules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ML transpiler uses a module registry to load Python bridge modules that provide ML standard library functionality. As of version 3.0, the module registry properly registers all loaded modules in Python's ``sys.modules`` cache, ensuring module identity consistency.

**Key Concept:** When a module is registered in ``sys.modules``, Python guarantees that:

1. Multiple imports of the same module return the **same module instance**
2. Class definitions within that module are **identical across imports**
3. ``isinstance()`` checks work correctly with types from that module

Before the Fix (< 3.0)
^^^^^^^^^^^^^^^^^^^^^^^

In versions prior to 3.0, the module registry loaded modules but didn't register them in ``sys.modules``:

.. code-block:: python

   # Module registry loads datetime_bridge
   registry = get_registry()
   datetime_module = registry.get_module('datetime')  # Instance A

   # Direct import creates NEW instance
   from mlpy.stdlib.datetime_bridge import DateTimeObject  # Instance B

   # Problem: A and B are different class instances!
   result = ml_function()  # Returns DateTimeObject from Instance A
   isinstance(result, DateTimeObject)  # FALSE - comparing to Instance B!

This caused:

* isinstance() failures with ML return values
* Type checking errors in web frameworks (Flask, FastAPI)
* CapabilityContext AttributeError (thread-local storage inconsistency)
* JSON serialization issues

After the Fix (>= 3.0)
^^^^^^^^^^^^^^^^^^^^^^^

As of version 3.0, modules are properly registered before execution:

.. code-block:: python

   # In module_registry.py (line 107-112)
   if spec and spec.loader:
       module = importlib.util.module_from_spec(spec)

       # FIX: Register in sys.modules BEFORE execution
       import sys
       sys.modules[spec.name] = module

       spec.loader.exec_module(module)

This ensures:

.. code-block:: python

   # Module registry loads datetime_bridge
   registry = get_registry()
   datetime_module = registry.get_module('datetime')  # Instance A

   # Direct import returns SAME instance
   from mlpy.stdlib.datetime_bridge import DateTimeObject  # Instance A

   # Success: A is A!
   result = ml_function()  # Returns DateTimeObject from Instance A
   isinstance(result, DateTimeObject)  # TRUE - same class instance!

Recommended Import Patterns
----------------------------

Pattern 1: Direct Module Import (Preferred)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use direct imports for type checking and isinstance() validation:

.. code-block:: python

   from mlpy.stdlib.datetime_bridge import DateTime, DateTimeObject
   from mlpy.stdlib.regex_bridge import Regex
   from mlpy.runtime.capabilities import CapabilityContext

   # ML function returns DateTimeObject
   result = ml_function()

   # Type checking works correctly
   if isinstance(result, DateTimeObject):
       iso_string = result._dt.isoformat()

**Advantages:**

* Clean, Pythonic code
* IDE autocomplete and type hints work
* isinstance() checks work correctly
* No module identity issues

**Use When:**

* Writing Flask/FastAPI endpoints
* Performing type checking on ML return values
* Converting ML types to Python types

Pattern 2: Module Registry Access
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use the module registry when you need dynamic module loading:

.. code-block:: python

   from mlpy.stdlib.module_registry import get_registry

   registry = get_registry()
   datetime_module = registry.get_module('datetime')

   # Functionally equivalent to direct import
   # Returns same instance as: from mlpy.stdlib import datetime

**Advantages:**

* Dynamic module discovery
* Check module availability at runtime
* Useful for plugin systems

**Use When:**

* Building dynamic ML execution systems
* Implementing REPL or interactive environments
* Module availability needs to be checked

Pattern 3: Transpiled ML Code Import
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When ML code imports standard library modules, the transpiler generates proper import statements:

.. code-block:: python

   # ML code
   import datetime;
   import regex;

   function process() {
       current_time = datetime.now();
       return current_time;
   }

   # Transpiled Python code
   from mlpy.stdlib import datetime as datetime_module
   from mlpy.stdlib import regex as regex_module

   def process():
       current_time = datetime_module.now()
       return current_time

**The transpiler ensures:**

* Imports use the correct module path (``mlpy.stdlib.{module}_bridge``)
* Module aliases avoid naming conflicts
* All imports reference the same module instances

Integration Framework Patterns
------------------------------

Flask Integration
^^^^^^^^^^^^^^^^^

Type-safe Flask endpoints with proper isinstance() checks:

.. code-block:: python

   from flask import Flask, jsonify, request
   from mlpy.ml.transpiler import MLTranspiler
   from mlpy.stdlib.datetime_bridge import DateTimeObject
   from mlpy.runtime.capabilities import CapabilityContext

   app = Flask(__name__)

   # Load and transpile ML code
   transpiler = MLTranspiler()
   with open('ml_api.ml') as f:
       ml_code = f.read()

   python_code, _, _ = transpiler.transpile_to_python(ml_code)
   ml_functions = {}
   exec(python_code, ml_functions)

   @app.route('/api/report', methods=['POST'])
   def generate_report():
       data = request.json

       # Execute ML function with capabilities
       with CapabilityContext() as ctx:
           ctx.add_capability('datetime.now')
           result = ml_functions['generate_report'](data)

       # Type-safe conversion (isinstance works!)
       def convert_datetime(obj):
           if isinstance(obj, DateTimeObject):
               return obj._dt.isoformat()
           elif isinstance(obj, dict):
               return {k: convert_datetime(v) for k, v in obj.items()}
           elif isinstance(obj, list):
               return [convert_datetime(item) for item in obj]
           return obj

       # Convert ML types to JSON-serializable types
       safe_result = convert_datetime(result)
       return jsonify(safe_result)

FastAPI Integration
^^^^^^^^^^^^^^^^^^^

Async-safe FastAPI endpoints with type validation:

.. code-block:: python

   from fastapi import FastAPI
   from pydantic import BaseModel
   from mlpy.ml.transpiler import MLTranspiler
   from mlpy.stdlib.datetime_bridge import DateTimeObject
   from mlpy.runtime.capabilities import CapabilityContext

   app = FastAPI()

   # Load ML functions
   transpiler = MLTranspiler()
   with open('ml_analytics.ml') as f:
       ml_code = f.read()

   python_code, _, _ = transpiler.transpile_to_python(ml_code)
   ml_functions = {}
   exec(python_code, ml_functions)

   class Event(BaseModel):
       id: str
       type: str
       user_id: str
       data: dict

   @app.post("/events/process")
   async def process_event(event: Event):
       # Execute ML function with capabilities
       with CapabilityContext() as ctx:
           ctx.add_capability('datetime.now')
           ctx.add_capability('math.compute')
           result = ml_functions['process_event'](event.dict())

       # Type-safe datetime conversion
       if 'processed_at' in result and isinstance(result['processed_at'], DateTimeObject):
           result['processed_at'] = result['processed_at']._dt.isoformat()

       return {"success": True, "event": result}

Common Patterns and Anti-Patterns
----------------------------------

Pattern: Type Checking Before Conversion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Always use isinstance() to check types before conversion:

.. code-block:: python

   # Good: Type-safe conversion
   from mlpy.stdlib.datetime_bridge import DateTimeObject

   def convert_ml_types(value):
       if isinstance(value, DateTimeObject):
           return value._dt.isoformat()
       elif isinstance(value, dict):
           return {k: convert_ml_types(v) for k, v in value.items()}
       return value

   # Works correctly with sys.modules fix
   result = ml_function()
   safe_result = convert_ml_types(result)

.. warning::
   **Anti-Pattern:** Type name string comparison

   .. code-block:: python

      # Bad: Fragile type checking
      if type(value).__name__ == 'DateTimeObject':
          convert(value)

      # This is unnecessary with the sys.modules fix!
      # Use isinstance() instead.

Pattern: Capability Context Wrapping
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Always wrap ML function calls in proper capability contexts:

.. code-block:: python

   from mlpy.runtime.capabilities import CapabilityContext

   # Good: Explicit capability management
   with CapabilityContext() as ctx:
       ctx.add_capability('datetime.now')
       ctx.add_capability('math.compute')
       result = ml_function(data)

.. warning::
   **Anti-Pattern:** Calling ML functions without capability context

   .. code-block:: python

      # Bad: Missing capability context
      result = ml_function(data)
      # Error: Function requires capabilities, but no context is active

Migration from Pre-3.0 Versions
--------------------------------

If you're upgrading from a version < 3.0, you can remove these workarounds:

Type Name Comparison (No Longer Needed)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Pre-3.0 workaround
   if type(obj).__name__ == 'DateTimeObject':
       convert(obj)

   # Post-3.0: Use isinstance()
   from mlpy.stdlib.datetime_bridge import DateTimeObject

   if isinstance(obj, DateTimeObject):
       convert(obj)

Manual Module Instance Sharing (No Longer Needed)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Pre-3.0 workaround: Store registry instance
   registry = get_registry()
   datetime_ref = registry.get_module('datetime')

   def check_datetime(obj):
       # Compare against stored reference
       if type(obj).__module__ == type(datetime_ref).__module__:
           convert(obj)

   # Post-3.0: Just use isinstance()
   from mlpy.stdlib.datetime_bridge import DateTimeObject

   def check_datetime(obj):
       if isinstance(obj, DateTimeObject):
           convert(obj)

Try-Except isinstance() Workarounds (No Longer Needed)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Pre-3.0 workaround: Catch isinstance failures
   try:
       if isinstance(obj, DateTimeObject):
           convert(obj)
   except TypeError:
       # Fallback to string comparison
       if 'DateTimeObject' in str(type(obj)):
           convert(obj)

   # Post-3.0: isinstance() just works
   if isinstance(obj, DateTimeObject):
       convert(obj)

Best Practices Summary
----------------------

1. **Use Direct Imports**

   * Import types directly from ``mlpy.stdlib.{module}_bridge``
   * Enables clean isinstance() checks
   * IDE support and type hints work correctly

2. **Always Use isinstance()**

   * Type checking is reliable with sys.modules fix
   * Cleaner code than string comparisons
   * Pythonic and maintainable

3. **Wrap ML Calls in CapabilityContext**

   * Required for functions using datetime.now, math, etc.
   * Prevents capability errors
   * Security best practice

4. **Convert ML Types for Web Frameworks**

   * Use isinstance() to detect ML types
   * Convert to JSON-serializable Python types
   * Handle nested structures (dicts, lists)

5. **Trust the Module System**

   * sys.modules registration ensures consistency
   * No need for workarounds or hacks
   * Standard Python patterns work correctly

Troubleshooting
---------------

If isinstance() Still Fails
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Symptom:** ``isinstance(obj, DateTimeObject)`` returns ``False`` unexpectedly

**Diagnosis:**

.. code-block:: python

   # Check if module is properly registered
   import sys
   print('mlpy.stdlib.datetime_bridge' in sys.modules)  # Should be True

   # Check class identity
   from mlpy.stdlib.datetime_bridge import DateTimeObject
   print(f"Expected class: {DateTimeObject}")
   print(f"Object class: {type(obj)}")
   print(f"Are they the same? {type(obj) is DateTimeObject}")

**Solution:**

* Ensure you're using mlpy >= 3.0
* Check that you're importing from the correct module path
* Verify the ML code transpiled correctly

CapabilityContext AttributeError
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Symptom:** ``AttributeError: '_thread._local' object has no attribute 'stack'``

**Cause:** This was caused by module identity issues in < 3.0

**Solution:**

* Upgrade to mlpy >= 3.0
* The sys.modules fix resolves this automatically
* No code changes needed

Related Documentation
--------------------

* :doc:`module-system` - Understanding the unified module system
* :doc:`../debugging/common-issues` - Troubleshooting integration issues
* :doc:`security` - Capability-based security model
* :doc:`../patterns/synchronous` - Synchronous execution patterns
* :doc:`../patterns/async` - Asynchronous execution patterns

----

**Status:** Complete | **Length:** ~700 lines | **Updated:** January 20, 2026
