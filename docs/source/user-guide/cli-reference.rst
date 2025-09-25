==============
CLI Reference
==============

The mlpy command-line interface provides a comprehensive set of tools for ML development, from project initialization to production deployment.

Installation
============

.. code-block:: bash

   pip install mlpy

Basic Usage
===========

.. code-block:: bash

   mlpy [OPTIONS] COMMAND [ARGS]...

Global Options
==============

.. program:: mlpy

.. option:: --version, -V

   Show version and exit

.. option:: --verbose, -v

   Increase verbosity (use -vv for debug output)

.. option:: --quiet, -q

   Suppress all output except errors

.. option:: --config PATH

   Path to configuration file

.. option:: --project-root PATH

   Override project root directory

Commands
========

init - Create New Project
--------------------------

Create a new ML project with the specified template and configuration.

.. code-block:: bash

   mlpy init [OPTIONS] PROJECT_NAME

.. program:: mlpy init

.. option:: --template {basic,web,cli,library}

   Project template to use (default: basic)

.. option:: --dir PATH

   Directory to create project in (default: current directory)

.. option:: --description TEXT

   Project description

.. option:: --author TEXT

   Project author

.. option:: --license TEXT

   Project license (default: MIT)

**Examples:**

.. code-block:: bash

   # Create a basic project
   mlpy init my-project

   # Create a web application
   mlpy init my-web-app --template web

   # Create a CLI tool
   mlpy init my-tool --template cli --author "Your Name"

compile - Transpile ML to Python
---------------------------------

Compile ML source files to Python with optimization and security analysis.

.. code-block:: bash

   mlpy compile [OPTIONS] SOURCE

.. program:: mlpy compile

.. option:: --output, -o PATH

   Output file or directory

.. option:: --optimize, -O LEVEL

   Optimization level (0-3, default: 1)

.. option:: --source-maps

   Generate source maps for debugging

.. option:: --security-level {strict,normal,permissive}

   Security analysis level (default: strict)

.. option:: --capabilities TEXT

   Required capabilities (comma-separated)

**Examples:**

.. code-block:: bash

   # Compile single file
   mlpy compile src/main.ml

   # Compile with optimization
   mlpy compile src/main.ml --optimize 2

   # Compile entire project
   mlpy compile src/ --output dist/

run - Compile and Execute
-------------------------

Compile and execute ML programs in a secure sandbox environment.

.. code-block:: bash

   mlpy run [OPTIONS] SOURCE [ARGS]...

.. program:: mlpy run

.. option:: --sandbox

   Run in sandboxed environment (default: true)

.. option:: --timeout SECONDS

   Execution timeout (default: 30)

.. option:: --memory-limit MB

   Memory limit in MB (default: 100)

.. option:: --no-network

   Disable network access

**Examples:**

.. code-block:: bash

   # Run a program
   mlpy run src/main.ml

   # Run with arguments
   mlpy run src/main.ml arg1 arg2

   # Run with custom limits
   mlpy run src/main.ml --timeout 60 --memory-limit 200

test - Run Tests
----------------

Execute project tests with coverage reporting and security validation.

.. code-block:: bash

   mlpy test [OPTIONS] [PATTERN]

.. program:: mlpy test

.. option:: --coverage

   Generate coverage report

.. option:: --security

   Include security tests

.. option:: --timeout SECONDS

   Test timeout (default: 30)

.. option:: --parallel, -j JOBS

   Run tests in parallel

**Examples:**

.. code-block:: bash

   # Run all tests
   mlpy test

   # Run specific test pattern
   mlpy test "test_*.ml"

   # Run with coverage
   mlpy test --coverage

analyze - Security Analysis
---------------------------

Perform comprehensive security analysis on ML code.

.. code-block:: bash

   mlpy analyze [OPTIONS] [PATH]

.. program:: mlpy analyze

.. option:: --security

   Run security analysis (default: true)

.. option:: --performance

   Include performance analysis

.. option:: --format {text,json,html}

   Output format (default: text)

.. option:: --output, -o PATH

   Output file

**Examples:**

.. code-block:: bash

   # Analyze current project
   mlpy analyze

   # Analyze specific file
   mlpy analyze src/main.ml

   # Generate HTML report
   mlpy analyze --format html --output report.html

watch - Development Server
--------------------------

Watch files for changes and automatically recompile/test.

.. code-block:: bash

   mlpy watch [OPTIONS] [PATH]

.. program:: mlpy watch

.. option:: --pattern TEXT

   File patterns to watch (default: "**/*.ml")

.. option:: --ignore TEXT

   Patterns to ignore

.. option:: --command TEXT

   Command to run on changes (default: compile)

**Examples:**

.. code-block:: bash

   # Watch and compile
   mlpy watch src/

   # Watch and test
   mlpy watch --command test

serve - Development Services
----------------------------

Start development servers for various purposes.

.. code-block:: bash

   mlpy serve [OPTIONS] SERVICE

.. program:: mlpy serve

.. option:: --host TEXT

   Host to bind to (default: 127.0.0.1)

.. option:: --port INTEGER

   Port to bind to

.. option:: --debug

   Enable debug mode

**Services:**

- ``lsp`` - Language Server Protocol server for IDE integration
- ``docs`` - Documentation server with live reload
- ``api`` - Development API server

**Examples:**

.. code-block:: bash

   # Start LSP server
   mlpy serve lsp --port 2087

   # Start documentation server
   mlpy serve docs --port 8080

format - Code Formatting
------------------------

Format ML code according to style guidelines.

.. code-block:: bash

   mlpy format [OPTIONS] [PATH]

.. program:: mlpy format

.. option:: --check

   Check if files are formatted (exit code 1 if not)

.. option:: --diff

   Show formatting changes

.. option:: --line-length INTEGER

   Maximum line length (default: 100)

**Examples:**

.. code-block:: bash

   # Format all files
   mlpy format

   # Check formatting
   mlpy format --check

   # Show what would change
   mlpy format --diff

doc - Documentation
-------------------

Build and manage project documentation.

.. code-block:: bash

   mlpy doc [OPTIONS] COMMAND

.. program:: mlpy doc

**Commands:**

- ``build`` - Build documentation
- ``serve`` - Serve documentation locally
- ``clean`` - Clean documentation build

**Examples:**

.. code-block:: bash

   # Build documentation
   mlpy doc build

   # Serve locally
   mlpy doc serve

   # Clean build files
   mlpy doc clean

lsp - Language Server
---------------------

Start the ML Language Server for IDE integration.

.. code-block:: bash

   mlpy lsp [OPTIONS]

.. program:: mlpy lsp

.. option:: --stdio

   Use stdio communication (default)

.. option:: --tcp

   Use TCP communication

.. option:: --host TEXT

   TCP host (default: 127.0.0.1)

.. option:: --port INTEGER

   TCP port (default: 2087)

**Examples:**

.. code-block:: bash

   # Start with stdio (for IDE integration)
   mlpy lsp

   # Start TCP server for debugging
   mlpy lsp --tcp --port 2087

Configuration
=============

mlpy uses configuration files in JSON or YAML format. The CLI automatically searches for:

- ``mlpy.json``
- ``mlpy.yaml`` / ``mlpy.yml``
- ``.mlpy.json``

Example configuration:

.. code-block:: json

   {
     "name": "my-project",
     "version": "1.0.0",
     "source_dir": "src",
     "output_dir": "dist",
     "security_level": "strict",
     "allowed_capabilities": ["file_read", "file_write"],
     "watch_patterns": ["**/*.ml"],
     "auto_format": true
   }

Project Structure
=================

mlpy projects follow a standard structure:

.. code-block:: text

   my-project/
   ├── mlpy.json              # Project configuration
   ├── src/                   # ML source files
   │   └── main.ml
   ├── tests/                 # Test files
   │   └── test_main.ml
   ├── dist/                  # Compiled output
   ├── docs/                  # Documentation
   └── .mlpy/                 # Cache and metadata

Environment Variables
=====================

.. envvar:: MLPY_CONFIG

   Path to configuration file

.. envvar:: MLPY_CACHE_DIR

   Cache directory location

.. envvar:: MLPY_LOG_LEVEL

   Logging level (DEBUG, INFO, WARNING, ERROR)

.. envvar:: MLPY_SECURITY_LEVEL

   Default security level

Exit Codes
==========

- ``0`` - Success
- ``1`` - General error
- ``2`` - Configuration error
- ``3`` - Compilation error
- ``4`` - Security violation
- ``130`` - Interrupted by user (Ctrl+C)