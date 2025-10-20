ML Programming Language Documentation
=====================================

ML is a security-first programming language that transpiles to Python. It combines familiar syntax with capability-based access control and comprehensive static security analysis.

This documentation covers the ML language, standard library, and development toolkit.

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   user-guide/tutorial/index
   user-guide/language-reference/index
   user-guide/toolkit/index

.. toctree::
   :maxdepth: 2
   :caption: Integration Guide

   integration-guide/index

.. toctree::
   :maxdepth: 2
   :caption: Standard Library

   standard-library/index

Getting Started
---------------

The fastest way to start with ML:

.. code-block:: bash

   # Install mlpy
   pip install mlpy

   # Start the REPL
   python -m mlpy.repl

   # Or run an ML file
   python -m mlpy run program.ml

Quick Example
-------------

.. code-block:: ml

   // Simple ML program
   import console;

   function greet(name) {
       return "Hello, " + name + "!";
   }

   names = ["Alice", "Bob", "Charlie"];
   for (name in names) {
       console.log(greet(name));
   }

What's Next?
------------

* **New to ML?** Start with the :doc:`user-guide/tutorial/index`
* **Integrating with Python?** See the :doc:`integration-guide/index`
* **Need syntax reference?** Check :doc:`user-guide/language-reference/index`
* **Looking for functions?** Browse the :doc:`standard-library/index`

Documentation Structure
-----------------------

**User Guide**
   Learn ML programming from basics to advanced features.

   * **Tutorial** - Step-by-step introduction to ML
   * **Language Reference** - Complete syntax and semantics documentation
   * **Toolkit** - REPL, transpilation, capabilities, project management, debugging

**Integration Guide**
   Complete reference for embedding ML in Python applications.

   * **Foundation** - Architecture, module system, configuration, security
   * **Integration Patterns** - Synchronous, async, event-driven, framework-specific
   * **Complete Examples** - PySide6, Flask, FastAPI, CLI tools, microservices
   * **Production Deployment** - Containerization, monitoring, scaling, security

**Standard Library**
   Comprehensive reference for all built-in modules and functions.

   * builtin, console, math, regex, datetime, functional, and more
   * Complete API documentation with examples
   * Security considerations for each module

Project Information
-------------------

* **Repository:** https://github.com/anthropics/mlpy
* **License:** MIT
* **Python Version:** 3.12+

Indices and Tables
==================

* :ref:`genindex`
* :ref:`search`
