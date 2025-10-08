============
User Guide
============

Complete guide for ML language programmers, covering everything from basic concepts to advanced features.

.. toctree::
   :maxdepth: 2

   tutorial
   language-reference
   cli-reference
   ../standard-library/index

Overview
--------

The ML programming language is a modern, security-first language that transpiles to Python. It combines familiar syntax with advanced security features like capability-based access control.

Key Features
------------

🔒 **Security First**
   Built-in capability system prevents unauthorized access to system resources

⚡ **High Performance**
   Sub-10ms transpilation to optimized Python code

🎯 **Type Safe**
   Optional static typing with inference for better code quality

📦 **Rich Standard Library**
   Comprehensive standard library with secure defaults

🔧 **Developer Friendly**
   Excellent tooling support with IDE integration

Getting Started
---------------

The fastest way to get started with ML is through the command-line interface:

.. code-block:: bash

   # Install mlpy
   pip install mlpy

   # Create a new project
   mlpy init my-project
   cd my-project

   # Run your first program
   mlpy run src/main.ml

This creates a basic project structure and runs your first ML program.

What's Next?
------------

- Follow the :doc:`tutorial` for a hands-on introduction
- Check the :doc:`language-reference` for complete syntax documentation
- Learn about the :doc:`cli-reference` for development workflows
- Explore the :doc:`standard-library` for built-in functionality