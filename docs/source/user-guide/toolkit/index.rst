========================
The mlpy Toolkit
========================

The mlpy toolkit provides practical tools for working with ML programs. This section covers the interactive development environment, program execution, and security features.

.. contents::
   :local:
   :depth: 2

Overview
========

The mlpy toolkit consists of six main components:

1. **VS Code Editor** - Professional IDE integration with Language Server and Debug Adapter Protocol support
2. **REPL (Read-Eval-Print Loop)** - Interactive development environment for experimenting with ML code
3. **Transpilation & Execution** - Tools for running ML programs and deploying to production
4. **Capabilities** - Fine-grained security system for controlling program access to system resources
5. **Project Management & User Modules** - Structured project setup and reusable module system
6. **Debugging & Profiling** - Interactive debugger and performance analysis tools

These tools work together to provide a complete development and deployment experience for ML programs.

Professional IDE: VS Code Editor
=================================

Visual Studio Code provides the most comprehensive editing experience for ML programs. The ML language extension integrates with VS Code through standard protocols:

**Language Server Protocol (LSP)**
  Provides intelligent code editing features through the industry-standard protocol for language support.

**Debug Adapter Protocol (DAP)**
  Enables native debugging with breakpoints and variable inspection through VS Code's standard debugging interface.

VS Code is the recommended editor for ML development because it supports these standard protocols, making ML development benefit from mature IDE tooling without requiring custom implementations.

**Key Features:**

- **IntelliSense** - Context-aware auto-completion for ML code
- **Real-time Diagnostics** - Immediate feedback on syntax and security issues
- **Native Debugging** - Breakpoints, stepping, and variable inspection
- **Syntax Highlighting** - Semantic tokens via LSP for accurate representation
- **Code Navigation** - Go to definition, find references
- **Integrated Terminal** - Run ML programs directly from the editor

See :doc:`vscode-editor` for installation, configuration, and feature documentation.

Interactive Development: The REPL
==================================

The mlpy REPL provides an interactive environment for learning ML, testing code, and rapid prototyping. It offers:

- **Immediate feedback** - See results instantly without creating files
- **Experimentation** - Try different approaches quickly
- **Debugging** - Inspect values and test functions interactively
- **Discovery** - Explore standard library modules and their APIs

The REPL is the recommended starting point for learning ML and is ideal for:

- Learning ML syntax and features
- Testing standard library functions
- Prototyping algorithms
- Debugging issues
- Quick calculations and data processing

**Performance:** mlpy REPL v2.3 executes commands in ~7ms on average, making it suitable for interactive development.

**Security:** The REPL includes the same capability-based security system as file-based programs, allowing you to experiment safely.

See :doc:`repl-guide` for the complete REPL reference.

Program Execution: Transpilation & Deployment
==============================================

mlpy transpiles ML code to Python for execution. Understanding this process helps you:

- **Run programs** efficiently with `mlpy run`
- **Deploy applications** to production environments
- **Debug issues** by understanding the generated code
- **Optimize performance** with transpilation insights

The transpilation process:

1. **Parse** ML source code into an abstract syntax tree (AST)
2. **Analyze** the AST for security issues and optimization opportunities
3. **Generate** equivalent Python code with security wrappers
4. **Execute** the Python code in a controlled environment

mlpy provides multiple execution modes:

- **Direct execution** - Run ML files immediately
- **Compilation** - Generate Python files for deployment
- **Import system** - Use ML modules from Python
- **Sandbox execution** - Run untrusted code safely

See :doc:`transpilation` for details on transpilation, execution, and deployment.

Security: Capability-Based Access Control
==========================================

ML programs run in a security-restricted environment by default. Capabilities provide fine-grained control over what programs can access:

- **File I/O** - Control which files and directories programs can read/write
- **Network access** - Restrict which domains programs can contact
- **Console output** - Control logging and output permissions
- **System operations** - Limit access to system resources

Capabilities ensure that:

- **Untrusted code** runs safely without risking your system
- **Production applications** have minimal required permissions
- **Security violations** are detected at compile-time when possible
- **Audit trails** track all capability grants and revocations

Example capability grants:

.. code-block:: ml

   // In REPL
   ml[secure]> .grant console.write
   ml[secure]> .grant file.read:/data/**
   ml[secure]> .grant http.request:https://api.example.com/**

   // In program configuration (mlpy.json)
   {
     "capabilities": [
       "console.write",
       "file.read:/data/**",
       "http.request:https://api.example.com/**"
     ]
   }

See :doc:`capabilities` for a comprehensive introduction to the capability system.

Project Organization: Management & Modules
===========================================

As ML projects grow, you need tools for code organization and reusability. mlpy provides:

- **Project scaffolding** - ``mlpy --init`` creates structured projects
- **User modules** - Build reusable code libraries with imports
- **Module hierarchies** - Organize code in nested directory structures
- **Flexible deployment** - Choose transpilation modes for different use cases

Example project structure:

.. code-block:: text

   my-project/
   ├── mlpy.json              # Project configuration
   ├── src/
   │   ├── main.ml            # Main program
   │   └── user_modules/      # Reusable modules
   │       ├── sorting.ml
   │       └── algorithms/
   │           └── quicksort.ml
   └── tests/                 # Test files

Import and use modules:

.. code-block:: ml

   import user_modules.sorting;
   import user_modules.algorithms.quicksort;

   data = [5, 2, 8, 1, 9];
   sorted = user_modules.sorting.quicksort(data);

**Deployment flexibility:**

- **multi-file** - Separate .py files with caching (development/production)
- **single-file** - Portable single file (distribution)
- **silent** - In-memory only (testing/CI)

See :doc:`project-management` for complete project management and module documentation.

Development Tools: Debugging & Profiling
==========================================

.. note::
   **Under Development** - Comprehensive debugging and profiling tools are planned for future releases.

mlpy will provide professional debugging and profiling capabilities:

- **Interactive Debugger** - Breakpoints, stepping, variable inspection
- **Performance Profiler** - Function timing, hot spot identification, flame graphs
- **Memory Profiler** - Allocation tracking, leak detection, memory timeline
- **Code Coverage** - Test coverage analysis and reporting
- **Execution Tracer** - Follow program flow and data transformations

**Current Capabilities:**

While comprehensive tools are under development, mlpy currently provides:

- Rich error messages with context and suggestions
- Source map generation for debugging transpiled code
- Security analysis and auditing
- Basic profiling support

**Temporary Workarounds:**

.. code-block:: ml

   // Debug with console logging
   import console;

   console.log("Variable value:", x);
   console.log("Array contents:", data);

See :doc:`debugging-profiling` for planned features and current workarounds.

When to Use Each Tool
=====================

Choose the right tool for your task:

**Use VS Code when:**

- Writing complete applications
- Working on multi-file projects
- Requiring intelligent code completion
- Needing visual debugging with breakpoints
- Collaborating with teams using standard tools
- Seeking professional IDE features

**Use the REPL when:**

- Learning ML syntax and features
- Testing code snippets quickly
- Exploring standard library modules
- Debugging specific functions interactively
- Performing quick calculations
- Prototyping algorithms

**Use file-based execution when:**

- Building complete applications
- Writing reusable code
- Creating production programs
- Working on team projects
- Version controlling your code
- Deploying to servers

**Configure capabilities when:**

- Programs need file system access
- Programs need network access
- Running untrusted code
- Deploying to production
- Enforcing least-privilege security

**Use project management when:**

- Starting a new ML project
- Building applications with multiple files
- Creating reusable code libraries
- Working with team members
- Organizing complex codebases
- Deploying to production environments

**Use debugging & profiling when (planned):**

- Tracking down bugs and errors
- Optimizing program performance
- Identifying memory leaks
- Understanding program execution flow
- Testing code coverage
- Profiling production applications

Development Workflow
====================

A typical ML development workflow:

**1. Exploration Phase (REPL)**

Start in the REPL to explore ideas:

.. code-block:: ml

   ml[secure]> import math;
   ml[secure]> math.sqrt(16);
   => 4.0

   ml[secure]> function calculateArea(radius) {
   ...   return math.pi * radius * radius;
   ... }

   ml[secure]> calculateArea(5);
   => 78.53981633974483

**2. Development Phase (Files)**

Once you have working code, save it to a file:

.. code-block:: ml

   // geometry.ml
   import math;

   function calculateArea(radius) {
       return math.pi * radius * radius;
   }

   function calculateCircumference(radius) {
       return 2 * math.pi * radius;
   }

   // Test the functions
   radius = 5;
   console.log("Area: " + str(calculateArea(radius)));
   console.log("Circumference: " + str(calculateCircumference(radius)));

**3. Execution Phase**

Run your program:

.. code-block:: bash

   # Grant required capabilities
   echo '{"capabilities": ["console.write"]}' > mlpy.json

   # Run the program
   mlpy run geometry.ml

**4. Deployment Phase**

Deploy to production:

.. code-block:: bash

   # Compile to Python for deployment
   mlpy compile geometry.ml -o geometry.py

   # Run compiled version
   python geometry.py

This workflow leverages the strengths of each tool: REPL for experimentation, files for organization, and capabilities for security.

Getting Help
============

Each toolkit component has detailed documentation:

.. toctree::
   :maxdepth: 2

   vscode-editor
   repl-guide
   transpilation
   capabilities
   project-management
   debugging-profiling

Additional resources:

- :doc:`../tutorial/index` - Learn ML language basics
- :doc:`../language-reference/index` - Language syntax reference
- :doc:`../../standard-library/index` - Standard library modules

**Quick Reference:**

- Start REPL: ``mlpy repl``
- Run program: ``mlpy run program.ml``
- Compile program: ``mlpy compile program.ml -o output.py``
- Get help: ``mlpy --help``
- REPL help: ``.help`` (within REPL)

Next Steps
==========

Start with the REPL Guide to learn interactive development:

:doc:`repl-guide`

Then explore transpilation and deployment:

:doc:`transpilation`

Learn about the security model:

:doc:`capabilities`

Master project management and user modules:

:doc:`project-management`

See planned debugging and profiling features:

:doc:`debugging-profiling`
