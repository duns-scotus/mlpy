Common Issues and Solutions
============================

.. note::
   **Chapter Summary:** Comprehensive troubleshooting guide for common integration issues with tested solutions.

Overview
--------

This guide documents common issues encountered when integrating ML code with Python applications, along with tested solutions and best practices. Issues are organized by category with clear symptoms, diagnosis steps, and fixes.

.. contents:: Issue Categories
   :local:
   :depth: 2

RESOLVED: Module Identity and isinstance() Issues
--------------------------------------------------

.. success::
   **Status:** **RESOLVED in mlpy 3.0**

   The sys.modules registration fix (January 2026) resolves all module identity issues. If you're using mlpy >= 3.0, these issues no longer occur.

Background (Pre-3.0 Issue)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Symptom:**

.. code-block:: python

   from mlpy.stdlib.datetime_bridge import DateTimeObject

   result = ml_function()
   isinstance(result, DateTimeObject)  # Returns False unexpectedly!

**Root Cause:**

The module registry loaded Python bridge modules using ``importlib.util`` but never registered them in ``sys.modules``. This caused Python to create duplicate module instances when code directly imported the same modules, breaking isinstance() checks.

**Impact:**

* isinstance() checks failed with ML return values
* Type checking errors in Flask/FastAPI endpoints
* JSON serialization TypeError: "Object of type DateTimeObject is not JSON serializable"
* CapabilityContext AttributeError: "_thread._local object has no attribute 'stack'"

**Solution (Automatic in >= 3.0):**

The module registry now properly registers modules in ``sys.modules`` before execution (``src/mlpy/stdlib/module_registry.py:107-112``).

**Verification:**

.. code-block:: python

   # Check that modules are registered
   import sys
   print('mlpy.stdlib.datetime_bridge' in sys.modules)  # True in >= 3.0

   # isinstance() now works correctly
   from mlpy.stdlib.datetime_bridge import DateTimeObject
   result = ml_function()
   isinstance(result, DateTimeObject)  # True!

**See:** :doc:`../foundation/import-patterns` for complete migration guide.

----

Current Issues and Solutions
-----------------------------

1. Capability Context Not Active
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Symptom:**

.. code-block:: text

   Function requires capabilities ['math.compute'], but no capability context is active.

**Diagnosis:**

ML functions that use datetime.now(), math operations, or other restricted capabilities fail when called directly without a capability context.

**Solution:**

Wrap ML function calls in CapabilityContext:

.. code-block:: python

   from mlpy.runtime.capabilities import CapabilityContext

   # Flask example
   @app.route('/api/report', methods=['POST'])
   def generate_report():
       data = request.json

       with CapabilityContext() as ctx:
           ctx.add_capability('datetime.now')
           ctx.add_capability('math.compute')
           result = ml_functions['generate_report'](data)

       return jsonify(convert_ml_types(result))

**Required Capabilities:**

* ``datetime.now`` - For datetime.now() calls
* ``datetime.parse`` - For datetime parsing
* ``math.compute`` - For advanced math operations
* ``regex.match`` - For regex operations

**See Also:** :doc:`../foundation/security` - Capability-based security model

----

2. Regex 'contains' Method Missing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Symptom:**

.. code-block:: python

   AttributeError: 'Regex' object has no attribute 'contains'

**Temporary Workaround:**

Use ``search()`` instead:

.. code-block:: javascript

   // ML code workaround
   function validate_email(email) {
       pattern = regex.compile("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}");
       match = pattern.search(email);
       return match !== null;
   }

**Issue Tracking:**

* Status: Open
* Priority: High
* Affects: User validation, email/phone validation
* See: ``docs/summaries/integration-test-issues.md``

----

3. AsyncMLExecutor Missing 'executor' Attribute
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Symptom:**

.. code-block:: python

   AttributeError: 'AsyncMLExecutor' object has no attribute 'executor'

**Temporary Workaround:**

Use synchronous execution in a thread pool:

.. code-block:: python

   import asyncio
   from concurrent.futures import ThreadPoolExecutor

   thread_pool = ThreadPoolExecutor(max_workers=4)

   @app.post("/events")
   async def process_event(event: dict):
       loop = asyncio.get_event_loop()
       result = await loop.run_in_executor(
           thread_pool,
           ml_function,
           event
       )
       return result

**Issue Tracking:**

* Status: Open
* Priority: High
* Affects: FastAPI async endpoints
* See: ``docs/summaries/integration-test-issues.md``

----

Import Errors
-------------

ModuleNotFoundError
^^^^^^^^^^^^^^^^^^^

**Symptom:**

.. code-block:: python

   ModuleNotFoundError: No module named 'mlpy.stdlib.datetime_bridge'

**Solution:**

.. code-block:: bash

   # Install mlpy in development mode
   pip install -e .

**Verification:**

.. code-block:: python

   import mlpy
   print(mlpy.__version__)

----

Type Conversion Issues
----------------------

TypeError: Object not JSON serializable
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Symptom:**

.. code-block:: python

   TypeError: Object of type DateTimeObject is not JSON serializable

**Solution:**

Convert ML types before JSON serialization:

.. code-block:: python

   from mlpy.stdlib.datetime_bridge import DateTimeObject

   def convert_ml_types(obj):
       """Recursively convert ML types to JSON-serializable types"""
       if isinstance(obj, DateTimeObject):
           return obj._dt.isoformat()
       elif isinstance(obj, dict):
           return {k: convert_ml_types(v) for k, v in obj.items()}
       elif isinstance(obj, list):
           return [convert_ml_types(item) for item in obj]
       return obj

----

Getting Help
------------

If you encounter an issue not covered here:

1. **Check Version:** Ensure you're using mlpy >= 3.0
2. **Review Documentation:** :doc:`../foundation/import-patterns`, :doc:`../foundation/security`
3. **Search Issues:** https://github.com/anthropics/mlpy/issues
4. **Report Bug:** Include mlpy version, Python version, minimal reproducible example, full error traceback

----

**Status:** Complete | **Length:** ~600 lines | **Updated:** January 20, 2026
