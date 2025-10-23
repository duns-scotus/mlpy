=================
Integration Guide
=================

Complete guide for Python developers integrating mlpy into their projects and workflows.

.. toctree::
   :maxdepth: 2

   python-integration
   ide-integration
   api-reference
   examples

Overview
--------

mlpy is designed to integrate seamlessly with existing Python ecosystems. Whether you're adding ML capabilities to an existing application or building new tools, mlpy provides flexible integration options.

Integration Approaches
----------------------

**1. Command-Line Integration**
   Use mlpy CLI tools in build scripts and CI/CD pipelines

**2. Python API Integration**
   Embed mlpy transpiler directly in Python applications

**3. IDE Integration**
   Full development environment support with Language Server Protocol

**4. Library Integration**
   Use mlpy-generated Python modules as regular Python packages

Quick Start
-----------

.. code-block:: python

   from mlpy.transpiler import MLTranspiler

   # Initialize transpiler
   transpiler = MLTranspiler()

   # Transpile ML code
   ml_code = '''
   function greet(name) {
       return "Hello, " + name + "!"
   }

   message = greet("World")
   print(message)
   '''

   result = transpiler.transpile_string(ml_code)
   if result.success:
       print("Generated Python:")
       print(result.python_code)

       # Execute the code
       exec(result.python_code)

Use Cases
---------

**Configuration Management**
   Use ML for type-safe configuration files

**Domain-Specific Languages**
   Build custom DSLs on top of ML

**Scripting and Automation**
   Secure scripting with capability-based access control

**Educational Tools**
   Teaching programming with enhanced security

**Embedded Systems**
   Safe scripting for resource-constrained environments