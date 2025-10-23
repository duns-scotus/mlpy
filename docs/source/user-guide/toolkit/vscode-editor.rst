========================
VS Code Editor Support
========================

Visual Studio Code provides the most comprehensive editing experience for ML programs through its support for standard protocols. The ML language extension integrates with VS Code's Language Server Protocol (LSP) and Debug Adapter Protocol (DAP) to deliver professional IDE features.

.. contents::
   :local:
   :depth: 2

Why VS Code
===========

VS Code is the recommended editor for ML development because it supports industry-standard protocols that mlpy implements:

**Language Server Protocol (LSP)**
  Provides intelligent code editing features like auto-completion, hover information, and diagnostics through a standardized protocol.

**Debug Adapter Protocol (DAP)**
  Enables native debugging with breakpoints, variable inspection, and step execution through VS Code's integrated debugger.

These standard protocols ensure that ML development benefits from VS Code's mature tooling infrastructure without requiring custom implementations.

Installation
============

Building the Extension
-----------------------

From the mlpy project directory:

.. code-block:: bash

   cd ext/vscode
   npm install
   npm run compile
   npm run package

This creates ``mlpy-language-support-2.0.0.vsix`` in the ``ext/vscode`` directory.

Installing in VS Code
---------------------

**Method 1: Command Line**

.. code-block:: bash

   code --install-extension mlpy-language-support-2.0.0.vsix

**Method 2: VS Code UI**

1. Open VS Code
2. Press ``Ctrl+Shift+P`` (``Cmd+Shift+P`` on Mac)
3. Type "Extensions: Install from VSIX"
4. Select the ``.vsix`` file

**Method 3: Development Mode**

For testing changes to the extension:

.. code-block:: bash

   cd ext/vscode
   code .

Press ``F5`` to launch the Extension Development Host with your changes loaded.

Verifying Installation
----------------------

1. Open a ``.ml`` file in VS Code
2. Check the bottom-right corner for "ML" language indicator
3. Verify syntax highlighting is active
4. Open Command Palette (``Ctrl+Shift+P``) and type "ML" to see available commands

Language Features (LSP)
=======================

The extension provides intelligent editing features through the Language Server Protocol.

Syntax Highlighting
-------------------

**Semantic Tokens**
  Context-aware highlighting via LSP semantic tokens for accurate representation of ML constructs.

**TextMate Grammar**
  Fallback syntax highlighting for keywords, strings, numbers, and operators when the language server is unavailable.

**ML-Specific Highlighting**
  - Capability declarations (``capability file.read``)
  - Security annotations
  - Pattern matching expressions
  - Function definitions and calls

Auto-Completion (IntelliSense)
-------------------------------

**Trigger IntelliSense:**
  - Type and pause (automatic)
  - Press ``Ctrl+Space`` (manual)

**Completion Types:**
  - Keywords (``function``, ``if``, ``while``)
  - Standard library modules (``console``, ``math``, ``string``)
  - Built-in functions (``print``, ``len``, ``typeof``)
  - Variables and functions in scope
  - Module members after import

**Example:**

.. code-block:: ml

   import math;

   x = math.  // IntelliSense shows: pi, sqrt, abs, floor, ceil, etc.

Hover Information
-----------------

Hover over any symbol to see:

- **Functions:** Signature and parameter types
- **Variables:** Current value and type
- **Imports:** Module documentation
- **Keywords:** Syntax explanation

**Shortcut:** Hover mouse or press ``Ctrl+K Ctrl+I``

Real-Time Diagnostics
---------------------

The extension reports errors and warnings as you type:

**Error Types:**
  - Syntax errors (parse failures)
  - Type mismatches
  - Undefined variables
  - Security violations
  - Import errors

**Warning Types:**
  - Unused variables
  - Missing capabilities
  - Potential security issues

**View Problems:**
  - Problems panel: ``Ctrl+Shift+M``
  - Inline squiggles in editor
  - Error count in status bar

Code Snippets
-------------

The extension includes 30+ code snippets for common ML patterns:

**Function Snippets:**
  - ``fn`` → Function definition
  - ``afn`` → Arrow function
  - ``method`` → Method definition

**Control Flow:**
  - ``if`` → If statement
  - ``elif`` → Elif clause
  - ``for`` → For loop
  - ``while`` → While loop

**Usage:** Type prefix and press ``Tab`` to expand.

Debugging (DAP)
===============

Native debugging support through the Debug Adapter Protocol enables professional debugging workflows.

Starting a Debug Session
-------------------------

**Method 1: F5 Key**

1. Open an ML file
2. Press ``F5``
3. Program runs with debugger attached

**Method 2: Debug View**

1. Click Debug icon in Activity Bar (left sidebar)
2. Click "Run and Debug" button
3. Select "Debug Current ML File"

**Method 3: Launch Configuration**

Create ``.vscode/launch.json``:

.. code-block:: json

   {
     "version": "0.2.0",
     "configurations": [
       {
         "type": "ml",
         "request": "launch",
         "name": "Debug ML File",
         "program": "${file}",
         "stopOnEntry": false
       }
     ]
   }

Setting Breakpoints
-------------------

**Adding Breakpoints:**
  Click in the gutter (left of line numbers) to toggle a red breakpoint dot.

**Keyboard Shortcut:**
  ``F9`` on current line

**Breakpoint Types:**

1. **Line Breakpoints**
   Stop execution at a specific line.

2. **Conditional Breakpoints**
   Right-click breakpoint → "Edit Breakpoint" → Enter condition

   Example: ``x > 10``

3. **Exception Breakpoints**
   Break when exceptions are thrown

   Configure in Breakpoints pane

**Managing Breakpoints:**
  - View all: Breakpoints pane in Debug view
  - Disable: Uncheck in Breakpoints pane
  - Remove: Click breakpoint dot again

Execution Control
-----------------

When paused at a breakpoint, use these controls:

**Debug Toolbar:**

.. code-block:: text

   Continue (F5)     Resume until next breakpoint
   Step Over (F10)   Execute current line, skip function internals
   Step Into (F11)   Enter function calls to debug them
   Step Out (⇧F11)   Exit current function
   Restart (⇧⌘F5)    Restart debugging session
   Stop (⇧F5)        End debugging session

**Keyboard Shortcuts:**
  - ``F5`` - Continue
  - ``F10`` - Step Over
  - ``F11`` - Step Into
  - ``Shift+F11`` - Step Out

Variable Inspection
-------------------

**Variables Panel:**
  View local and global variables in the Debug sidebar.

**Scopes:**
  - **Locals:** Variables in current function
  - **Globals:** Module-level variables

**Hover Inspection:**
  Hover over variables in the editor to see their current values.

**Watch Expressions:**
  Add expressions to the Watch pane to monitor them continuously.

  Example watches:
  - ``x + y``
  - ``items.length``
  - ``typeof(value)``

Call Stack
----------

The Call Stack pane shows:

- Current execution point (top of stack)
- Function call hierarchy
- ML source positions

**Navigation:**
  Click any frame to view its variables and source location.

Debug Console
-------------

Evaluate expressions in the paused program context:

**Access:** Debug Console tab in bottom panel

**Features:**
  - Evaluate ML expressions
  - View expression results
  - Test conditions
  - Inspect complex objects

**Example:**

.. code-block:: ml

   > x + 5
   47
   > items.length
   10
   > typeof(value)
   "string"

**Security:** All expressions evaluated through SafeExpressionEvaluator to prevent sandbox escape.

Configuration
=============

Extension Settings
------------------

Configure in VS Code settings (``Ctrl+,``):

**Language Server**

.. code-block:: json

   {
     "ml.languageServer.enabled": true,
     "ml.languageServer.stdio": true,
     "ml.languageServer.trace": "verbose",
     "ml.languageServer.host": "127.0.0.1",
     "ml.languageServer.port": 2087
   }

**Options:**
  - ``enabled`` - Enable/disable language server (default: ``true``)
  - ``stdio`` - Use stdio communication (default: ``true``)
  - ``trace`` - Logging level: ``off``, ``messages``, ``verbose`` (default: ``off``)
  - ``host`` - TCP host for language server (if not using stdio)
  - ``port`` - TCP port for language server (if not using stdio)

**Security Analysis**

.. code-block:: json

   {
     "ml.security.enableAnalysis": true
   }

**Options:**
  - ``enableAnalysis`` - Enable real-time security scanning (default: ``true``)

**Debugging**

.. code-block:: json

   {
     "ml.debug.trace": false,
     "ml.debug.pythonPath": "python",
     "ml.debug.mlpyPath": "${workspaceFolder}"
   }

**Options:**
  - ``trace`` - Enable debug adapter logging (default: ``false``)
  - ``pythonPath`` - Python interpreter path (default: auto-detected)
  - ``mlpyPath`` - Path to mlpy installation (default: workspace folder)

Launch Configurations
---------------------

Create ``.vscode/launch.json`` for debugging:

**Basic Configuration:**

.. code-block:: json

   {
     "version": "0.2.0",
     "configurations": [
       {
         "type": "ml",
         "request": "launch",
         "name": "Debug Current File",
         "program": "${file}",
         "stopOnEntry": false
       }
     ]
   }

**Advanced Configuration:**

.. code-block:: json

   {
     "version": "0.2.0",
     "configurations": [
       {
         "type": "ml",
         "request": "launch",
         "name": "Debug Main",
         "program": "${workspaceFolder}/main.ml",
         "args": ["--verbose"],
         "stopOnEntry": false,
         "cwd": "${workspaceFolder}",
         "pythonPath": "python",
         "trace": false
       },
       {
         "type": "ml",
         "request": "launch",
         "name": "Debug and Stop on Entry",
         "program": "${file}",
         "stopOnEntry": true
       }
     ]
   }

**Configuration Properties:**

``type`` (required)
  Always ``"ml"`` for ML programs.

``request`` (required)
  Always ``"launch"`` (attach mode not supported).

``name`` (required)
  Configuration name shown in debug dropdown.

``program`` (required)
  Path to ML file to debug. Use variables:
  - ``${file}`` - Current open file
  - ``${workspaceFolder}`` - Workspace root
  - ``${workspaceFolder}/path/to/file.ml`` - Specific file

``stopOnEntry`` (optional, default: ``false``)
  Pause at first line of program.

``args`` (optional, default: ``[]``)
  Command-line arguments passed to program.

``cwd`` (optional, default: ``${workspaceFolder}``)
  Working directory for program execution.

``pythonPath`` (optional, default: auto-detected)
  Python interpreter to use.

``mlpyPath`` (optional, default: ``${workspaceFolder}``)
  Path to mlpy installation root.

``trace`` (optional, default: ``false``)
  Enable debug adapter protocol logging.

Commands
========

Extension commands available via Command Palette (``Ctrl+Shift+P``):

**Language Server:**
  - ``ML: Restart Language Server`` - Restart LSP server

**Security:**
  - ``ML: Run Security Analysis`` - Analyze current file (``Ctrl+Shift+S``)

**Transpilation:**
  - ``ML: Transpile to Python`` - Convert ML to Python (``Ctrl+Shift+T``)

**Execution:**
  - ``ML: Run in Sandbox`` - Execute in secure sandbox (``Ctrl+Shift+R``)

**Debugging:**
  - ``ML: Start Debugging`` - Start debug session
  - ``ML: Start Debugging (Stop on Entry)`` - Debug with immediate pause

**Formatting:**
  - ``ML: Format Code`` - Format current file (``Ctrl+Shift+F``)

**Project:**
  - ``ML: Initialize ML Project`` - Create new project structure

Keyboard Shortcuts
==================

Default keyboard shortcuts:

.. list-table::
   :header-rows: 1
   :widths: 30 40 30

   * - Shortcut
     - Command
     - Description
   * - ``F5``
     - Start Debugging
     - Begin debug session
   * - ``F9``
     - Toggle Breakpoint
     - Add/remove breakpoint
   * - ``F10``
     - Step Over
     - Execute current line
   * - ``F11``
     - Step Into
     - Enter function call
   * - ``Shift+F11``
     - Step Out
     - Exit function
   * - ``Ctrl+Shift+T``
     - Transpile
     - Convert to Python
   * - ``Ctrl+Shift+R``
     - Run in Sandbox
     - Execute securely
   * - ``Ctrl+Shift+S``
     - Security Analysis
     - Check for threats
   * - ``Ctrl+Shift+F``
     - Format Code
     - Apply formatting
   * - ``Ctrl+Space``
     - IntelliSense
     - Show completions
   * - ``Ctrl+Shift+M``
     - Problems Panel
     - View errors/warnings

Troubleshooting
===============

Language Server Not Starting
-----------------------------

**Symptoms:**
  - No syntax highlighting
  - No auto-completion
  - No diagnostics

**Solutions:**

1. **Check Python Installation:**

   .. code-block:: bash

      python --version  # Should be 3.12+

2. **Verify mlpy Installation:**

   .. code-block:: bash

      python -m mlpy --version

3. **Check Extension Logs:**

   - Open Output panel: ``Ctrl+Shift+U``
   - Select "ML Language Server" from dropdown
   - Review startup logs for errors

4. **Restart Language Server:**

   - Command Palette → "ML: Restart Language Server"

5. **Reload VS Code:**

   - Command Palette → "Developer: Reload Window"

Debugging Not Working
---------------------

**Symptoms:**
  - Breakpoints not hit
  - Debug session fails to start
  - Variables not showing

**Solutions:**

1. **Verify Debug Adapter Command:**

   .. code-block:: bash

      python -m mlpy debug-adapter --help

2. **Check Python Path:**

   Ensure ``ml.debug.pythonPath`` setting points to correct Python installation.

3. **Check mlpy Path:**

   Ensure ``ml.debug.mlpyPath`` setting points to mlpy project root.

4. **Enable Debug Logging:**

   In ``launch.json``:

   .. code-block:: json

      {
        "trace": true
      }

   Check Debug Console for error messages.

5. **Verify File Transpiles:**

   .. code-block:: bash

      python -m mlpy transpile yourfile.ml

   Fix any transpilation errors before debugging.

Syntax Highlighting Issues
---------------------------

**Solutions:**

1. **Force Language Mode:**

   - Click language indicator in status bar
   - Select "ML" from list

2. **Check File Extension:**

   Ensure file has ``.ml`` extension.

3. **Reinstall Extension:**

   .. code-block:: bash

      code --uninstall-extension mlpy-language-support
      code --install-extension mlpy-language-support-2.0.0.vsix

Performance Issues
------------------

**Symptoms:**
  - Slow auto-completion
  - Laggy editing
  - High CPU usage

**Solutions:**

1. **Disable Verbose Logging:**

   .. code-block:: json

      {
        "ml.languageServer.trace": "off"
      }

2. **Reduce File Size:**

   Large files (>1000 lines) may experience slowdown.

3. **Check Resource Usage:**

   - Open Task Manager / Activity Monitor
   - Look for ``python`` or ``node`` processes
   - If high CPU, restart language server

Best Practices
==============

Project Setup
-------------

**Create Workspace:**

1. Open project folder in VS Code
2. Create ``.vscode/`` directory
3. Add ``settings.json`` and ``launch.json``
4. Configure capabilities in ``mlpy.json``

**Example Structure:**

.. code-block:: text

   my-project/
   ├── .vscode/
   │   ├── settings.json      # VS Code settings
   │   └── launch.json        # Debug configurations
   ├── mlpy.json              # mlpy configuration
   ├── src/
   │   ├── main.ml
   │   └── utils.ml
   └── tests/
       └── test_main.ml

Development Workflow
--------------------

**1. Write Code with IntelliSense:**

   - Let auto-completion guide you
   - Use hover for documentation
   - Check Problems panel regularly

**2. Debug Early:**

   - Set breakpoints while writing
   - Test functions incrementally
   - Use Debug Console for experiments

**3. Use Security Analysis:**

   - Run ``Ctrl+Shift+S`` before commits
   - Fix security warnings immediately
   - Review capability requirements

**4. Format Consistently:**

   - Use ``Ctrl+Shift+F`` before saving
   - Configure format-on-save if desired

Debugging Workflow
------------------

**1. Set Breakpoints First:**

   Place breakpoints at key points before running.

**2. Use Step Over Primarily:**

   Step Into only when investigating specific functions.

**3. Watch Critical Variables:**

   Add important variables to Watch pane.

**4. Check Call Stack:**

   Understand execution flow by examining stack frames.

**5. Use Debug Console:**

   Test hypotheses with expression evaluation.

Performance Tips
----------------

**Language Server:**
  - Keep trace logging off in production
  - Restart server if it becomes slow
  - Use stdio mode (faster than TCP)

**Debugging:**
  - Remove unnecessary breakpoints
  - Use conditional breakpoints sparingly
  - Close debug sessions when done

**General:**
  - Close unused editor tabs
  - Disable unnecessary extensions
  - Keep VS Code updated

Next Steps
==========

**Learn More:**

- :doc:`debugging-profiling` - Interactive REPL debugger
- :doc:`../tutorial/index` - ML language tutorial
- :doc:`../language-reference/index` - Complete syntax reference

**Get Help:**

- VS Code documentation: https://code.visualstudio.com/docs
- mlpy issues: https://github.com/your-org/mlpy/issues
- Language Server Protocol: https://microsoft.github.io/language-server-protocol/
- Debug Adapter Protocol: https://microsoft.github.io/debug-adapter-protocol/

**Quick Reference:**

.. code-block:: bash

   # Build extension
   cd ext/vscode && npm run package

   # Install extension
   code --install-extension mlpy-language-support-2.0.0.vsix

   # Start debugging
   # Press F5 in VS Code with .ml file open

   # Check logs
   # Output panel → "ML Language Server"
