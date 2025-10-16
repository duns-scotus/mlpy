==========
REPL Guide
==========

The mlpy REPL (Read-Eval-Print Loop) is an interactive environment for writing and testing ML code. It provides immediate feedback, making it ideal for learning, experimentation, and rapid prototyping.

.. contents::
   :local:
   :depth: 3

Introduction
============

What is the REPL?
-----------------

The REPL is an interactive programming environment that:

1. **Reads** your ML code input
2. **Evaluates** the code immediately
3. **Prints** the result
4. **Loops** back to read more input

This immediate feedback loop makes the REPL perfect for:

- **Learning ML** - Try new syntax and see results instantly
- **Testing code** - Verify function behavior interactively
- **Prototyping** - Experiment with algorithms before writing files
- **Debugging** - Inspect values and test fixes quickly
- **Exploring modules** - Discover standard library APIs
- **Quick calculations** - Use ML as a powerful calculator

Why Use the REPL?
------------------

**Immediate Feedback**

No need to create files, save, and run. Type code and see results instantly:

.. code-block:: ml

   ml[secure]> 2 + 2
   => 4

   ml[secure]> "Hello, " + "ML!"
   => "Hello, ML!"

**Persistent State**

Variables and functions remain available across commands:

.. code-block:: ml

   ml[secure]> x = 42;
   ml[secure]> y = x + 10;
   ml[secure]> y
   => 52

**Experimentation**

Try different approaches without consequences:

.. code-block:: ml

   ml[secure]> math.sqrt(16);
   => 4.0

   ml[secure]> math.sqrt(-1);
   Error: Math domain error

   ml[secure]> // No problem - try something else

**Safe Environment**

The REPL includes the same capability-based security as file-based programs:

.. code-block:: ml

   ml[secure]> import file;
   Error: Missing required capabilities: ['file.read']

   ml[secure]> .grant file.read
   ✓ Granted capability: file.read

   ml[secure]> import file;
   // Now it works

REPL vs File-Based Development
-------------------------------

**Use the REPL when:**

- Learning ML syntax and features
- Testing small code snippets
- Exploring standard library modules
- Debugging specific functions
- Performing quick calculations
- Prototyping algorithms

**Use files when:**

- Building complete applications
- Writing reusable code
- Creating production programs
- Working on team projects
- Version controlling your code
- Deploying to servers

**Best Practice:** Start in the REPL, then move working code to files.

Getting Started
===============

Starting the REPL
-----------------

Start the mlpy REPL from your terminal:

.. code-block:: bash

   $ mlpy repl

You'll see the welcome message and prompt:

.. code-block:: text

   Welcome to mlpy REPL v2.3!
   Type .help for available commands, .exit to quit (or Ctrl+D)
   ml[secure]>

**Alternative Start Methods:**

.. code-block:: bash

   # Using Python module
   $ python -m mlpy.cli.repl

   # From Python code
   >>> from mlpy.cli.repl import run_repl
   >>> run_repl()

Starting with Extension Paths
-------------------------------

Load custom Python extension modules when starting the REPL:

.. code-block:: bash

   # Single extension path
   $ mlpy repl -E /path/to/extensions

   # Multiple extension paths
   $ mlpy repl -E /ext1 -E /ext2 -E /ext3

   # Full form
   $ mlpy repl --extension-path /path/to/extensions

**Extension Path Priority:**

Extension paths can be configured three ways (priority order):

1. **CLI flags** (highest priority):

   .. code-block:: bash

      $ mlpy repl -E /override/path

2. **Project configuration** (medium priority):

   In ``mlpy.json`` or ``mlpy.yaml``:

   .. code-block:: json

      {
        "python_extension_paths": ["./extensions"]
      }

3. **Environment variable** (lowest priority):

   .. code-block:: bash

      # Unix/macOS (colon-separated)
      export MLPY_EXTENSION_PATHS=/ext1:/ext2
      mlpy repl

      # Windows (semicolon-separated)
      set MLPY_EXTENSION_PATHS=C:\ext1;C:\ext2
      mlpy repl

**Dynamic Path Addition:**

You can also add extension paths during the REPL session using the ``.addpath`` command (see :ref:`Module Exploration Commands` for details).

.. code-block:: ml

   ml[secure]> .addpath ./my_modules
   ✓ Added extension path: C:\Users\user\project\my_modules

Understanding the Prompt
-------------------------

The REPL prompt shows your current state:

**Single-Line Prompt:**

.. code-block:: text

   ml[secure]>

- ``ml`` - You're in the ML REPL
- ``[secure]`` - Security mode active (capability system enabled)
- ``>`` - Ready for single-line input

**Multi-Line Prompt:**

.. code-block:: text

   ml[secure]> function add(a, b) {
   ...

- ``...`` - Continuation prompt (multi-line input mode)
- Press Enter with empty line to execute buffered input

Exiting the REPL
-----------------

Exit the REPL using any of these methods:

.. code-block:: text

   ml[secure]> .exit
   ml[secure]> .quit
   ml[secure]> # Or press Ctrl+D (Unix) / Ctrl+Z then Enter (Windows)

Basic Usage
===========

Entering Expressions
--------------------

Type ML expressions and press Enter to evaluate:

**Simple Expressions:**

.. code-block:: ml

   ml[secure]> 2 + 2
   => 4

   ml[secure]> "Hello" + " " + "World"
   => "Hello World"

   ml[secure]> 10 > 5
   => true

**Results Display:**

- Results are displayed with ``=>`` prefix
- ``null`` values are not displayed
- Errors show error messages with suggestions

Variable Assignment
-------------------

Variables persist across commands:

.. code-block:: ml

   ml[secure]> x = 10;
   ml[secure]> y = 20;
   ml[secure]> x + y
   => 30

   ml[secure]> name = "Alice";
   ml[secure]> "Hello, " + name
   => "Hello, Alice"

**Variable Inspection:**

Use ``.vars`` to see all defined variables:

.. code-block:: ml

   ml[secure]> .vars
   Variables:
     x = 10
     y = 20
     name = "Alice"

Multi-Line Input
----------------

Enter multi-line code for functions, loops, and conditionals:

**Function Definitions:**

.. code-block:: ml

   ml[secure]> function greet(name) {
   ...   return "Hello, " + name + "!";
   ... }

   ml[secure]> greet("Bob")
   => "Hello, Bob!"

**Control Flow:**

.. code-block:: ml

   ml[secure]> if (x > 5) {
   ...   console.log("x is big");
   ... } else {
   ...   console.log("x is small");
   ... }
   x is big

**Loops:**

.. code-block:: ml

   ml[secure]> for (i in range(3)) {
   ...   console.log(i);
   ... }
   0
   1
   2

**Multi-Line Triggers:**

Lines ending with these characters start multi-line mode:

- ``{`` - Block start
- ``(`` - Unmatched opening parenthesis
- ``[`` - Array literal start
- ``,`` - Continuation expected

**Executing Multi-Line Input:**

- Press Enter on an empty line to execute
- Or complete the construct and press Enter

Importing Modules
-----------------

Import standard library modules to access their functions:

.. code-block:: ml

   ml[secure]> import math;
   ml[secure]> math.sqrt(16)
   => 4.0

   ml[secure]> math.pi
   => 3.141592653589793

**Module Discovery:**

.. code-block:: ml

   ml[secure]> import console;
   ml[secure]> console.log("Hello!");
   Hello!

   ml[secure]> import datetime;
   ml[secure]> now = datetime.now();
   ml[secure]> now.year
   => 2025

REPL Commands
=============

The REPL provides special commands for session management, debugging, and capability control. All commands start with a dot (``.``).

Help Command
------------

``.help``
~~~~~~~~~

Shows all available REPL commands with examples.

**Usage:**

.. code-block:: text

   ml[secure]> .help

**Output:**

.. code-block:: text

   REPL Commands:
     .help              Show this help message
     .vars              Show defined variables
     .clear, .reset     Clear session and reset namespace
     .history           Show command history
     .capabilities      Show granted capabilities
     .grant <cap>       Grant a capability (requires confirmation)
     .revoke <cap>      Revoke a capability
     .retry             Retry last failed command
     .edit              Edit last statement in external editor
     .modules           List all available modules
     .modinfo <name>    Show detailed info about a module
     .addpath <path>    Add extension directory for custom modules
     .exit, .quit       Exit REPL (or Ctrl+D)

   Usage:
     - Type ML code and press Enter to execute
     - Results are displayed with => prefix
     - Variables persist across commands
     - Multi-line input: lines ending with { start a block
     - Empty line executes buffered multi-line input

   Examples:
     ml> x = 42
     ml> x + 10
     => 52

Session Management Commands
---------------------------

``.vars``
~~~~~~~~~

Lists all variables in the current session with their values.

**Usage:**

.. code-block:: text

   ml[secure]> .vars

**Example:**

.. code-block:: ml

   ml[secure]> x = 10;
   ml[secure]> name = "Alice";
   ml[secure]> active = true;

   ml[secure]> .vars
   Variables:
     x = 10
     name = "Alice"
     active = true

**When to Use:**

- Check what variables are defined
- Verify variable values
- Debug state issues
- Review session contents before saving

``.clear`` / ``.reset``
~~~~~~~~~~~~~~~~~~~~~~~

Clears all variables and resets the session to a clean state.

**Usage:**

.. code-block:: text

   ml[secure]> .clear
   Session reset. All variables cleared.

   ml[secure]> .reset
   Session reset. All variables cleared.

**What Gets Cleared:**

- All variables and functions
- Command history
- Granted capabilities
- Symbol tracking
- Execution state

**Example:**

.. code-block:: ml

   ml[secure]> x = 42;
   ml[secure]> y = 100;

   ml[secure]> .vars
   Variables:
     x = 42
     y = 100

   ml[secure]> .clear
   Session reset. All variables cleared.

   ml[secure]> .vars
   No variables defined

   ml[secure]> x
   Error: NameError: name 'x' is not defined

**When to Use:**

- Start fresh after experiments
- Clear state before testing
- Fix corrupted session state
- Begin new topic/task

``.history``
~~~~~~~~~~~~

Shows the command history for the current session.

**Usage:**

.. code-block:: text

   ml[secure]> .history

**Example:**

.. code-block:: ml

   ml[secure]> x = 10;
   ml[secure]> y = 20;
   ml[secure]> x + y

   ml[secure]> .history
   [1] x = 10;
   [2] y = 20;
   [3] x + y

**Features:**

- Line numbers for reference
- Excludes REPL commands (only ML code)
- Cleared by ``.reset``
- Available for review and replay

**When to Use:**

- Review what you've tried
- Find successful experiments
- Copy commands for files
- Debug command sequences

Debugging Commands
------------------

``.retry``
~~~~~~~~~~

Re-executes the last failed command, useful for fixing syntax errors.

**Usage:**

.. code-block:: text

   ml[secure]> .retry

**Example - Fixing Syntax Error:**

.. code-block:: ml

   ml[secure]> x = [1, 2, 3

   Error: Parse Error: Invalid ML syntax
   Tip: Check for missing semicolons, unmatched braces, or typos

   ml[secure]> .retry
   Retrying: x = [1, 2, 3
   ✗ Failed again: Parse Error: Invalid ML syntax

   ml[secure]> x = [1, 2, 3];

   ml[secure]> .retry
   Retrying: x = [1, 2, 3];
   ✓ Success!

**Example - Quick Fix Workflow:**

.. code-block:: ml

   ml[secure]> result = divide(10, 0);
   Error: Division by zero

   # Fix the function, then retry
   ml[secure]> function divide(a, b) {
   ...   if (b == 0) { return null; }
   ...   return a / b;
   ... }

   ml[secure]> .retry
   Retrying: result = divide(10, 0);
   ✓ Success!

   ml[secure]> result
   => null

**When to Use:**

- Fix syntax errors quickly
- Test error handling
- Verify fixes work
- Save typing for complex commands

``.edit``
~~~~~~~~~

Opens the last statement in your external editor for complex multi-line editing.

**Usage:**

.. code-block:: text

   ml[secure]> .edit

**Editor Selection:**

The REPL respects your ``$EDITOR`` environment variable:

- **Unix/Linux:** Usually ``vim``, ``emacs``, or ``nano``
- **Windows:** Defaults to ``notepad``
- **Custom:** Set ``$EDITOR`` to your preferred editor

**Example Workflow:**

.. code-block:: ml

   ml[secure]> function complexAlgorithm(data) {
   ...   // Some complex logic here
   ... }

   ml[secure]> .edit
   # Opens in your editor:
   #   function complexAlgorithm(data) {
   #     // Edit here with full editor features
   #   }
   # Save and close

   Executing edited code...
   ✓ Done

**Features:**

- Full editor capabilities (syntax highlighting, search, replace)
- Edit complex multi-line code comfortably
- Auto-executes after saving and closing
- Saves last statement for editing

**When to Use:**

- Complex function definitions
- Multi-line algorithms
- Fixing syntax in long code blocks
- When multi-line REPL input is awkward

Module Exploration Commands
----------------------------

mlpy v2.4+ includes powerful module discovery commands that help you explore available modules interactively.

``.modules``
~~~~~~~~~~~~

Lists all available modules (both imported and unimported).

**Usage:**

.. code-block:: text

   ml[secure]> .modules

**Example:**

.. code-block:: ml

   ml[secure]> .modules
   Available Modules (11 total):

     Core:
       • math
       • random
     Data:
       • collections
       • datetime
       • functional
       • json
     I/O:
       • console
       • file
       • http
       • path
     Utilities:
       • regex

   Use .modinfo <name> to get details about a specific module

**Features:**

- Shows ALL available modules (not just imported ones)
- Categorized by type (Core, Data, I/O, Utilities)
- Uses automatic module discovery system
- Cached for fast subsequent calls

**When to Use:**

- Discover what standard library modules are available
- Find modules for specific tasks
- Verify module availability before importing
- Explore the ML standard library

``.modinfo <module>``
~~~~~~~~~~~~~~~~~~~~~

Shows detailed information about a specific module.

**Usage:**

.. code-block:: text

   ml[secure]> .modinfo <module-name>

**Example:**

.. code-block:: ml

   ml[secure]> .modinfo math
   Module: math
   Description: Mathematical operations and constants
   Version: 1.0.0
   Loaded: Yes

   Functions (27):
     • abs() - Absolute value
     • acos() - Arccosine function
     • asin() - Arcsine function
     • atan() - Arctangent function
     • atan2() - Two-argument arctangent
     • ceil() - Ceiling function
     • cos() - Cosine function
     • degToRad() - Convert degrees to radians
     • degrees() - Convert radians to degrees
     • exp() - Exponential (e^x)
     ... and 17 more functions

**Information Shown:**

- Module name and description
- Version number
- Loaded status (imported or not)
- Available functions with descriptions
- Available classes (if any)

**When to Use:**

- Learn about a module before importing
- Discover available functions
- Check module capabilities
- Get quick reference documentation
- Verify module version

**Example Workflow:**

.. code-block:: ml

   ml[secure]> .modules
   # Discover "regex" module exists

   ml[secure]> .modinfo regex
   # Learn about regex module functions

   ml[secure]> import regex;
   # Import now that you know what it does

   ml[secure]> .modinfo regex
   # Check again - now shows "Loaded: Yes"

``.addpath <directory>``
~~~~~~~~~~~~~~~~~~~~~~~~

Adds an extension directory for loading custom modules.

**Usage:**

.. code-block:: text

   ml[secure]> .addpath <directory-path>

**Example:**

.. code-block:: ml

   ml[secure]> .addpath ./my_modules
   ✓ Added extension path: C:\Users\user\project\my_modules

   Extension modules are now available for import
   Use .modules to see all available modules

   ml[secure]> .modules
   Available Modules (13 total):
     # Now includes modules from ./my_modules

**Path Validation:**

The command validates the path before adding:

.. code-block:: ml

   ml[secure]> .addpath ./nonexistent
   Error: Path './nonexistent' does not exist

   ml[secure]> .addpath file.txt
   Error: Path 'file.txt' is not a directory

**Features:**

- Resolves relative paths to absolute paths
- Validates path exists and is a directory
- Invalidates module cache (forces re-scan)
- Extensions immediately available for import

**When to Use:**

- Load custom extension modules
- Add project-specific modules
- Test third-party ML modules
- Organize large codebases with custom modules

**Example - Custom Modules:**

.. code-block:: ml

   # Create custom module in ./extensions/
   # File: ./extensions/my_utils_bridge.py
   #
   # @ml_module(name="my_utils")
   # class MyUtils:
   #     @ml_function(description="Custom function")
   #     def custom_func(self):
   #         return "Hello from custom module"

   ml[secure]> .addpath ./extensions
   ✓ Added extension path: C:\project\extensions

   ml[secure]> .modules
   # Shows "my_utils" in the list

   ml[secure]> import my_utils;
   ml[secure]> my_utils.custom_func()
   => "Hello from custom module"

**Multiple Paths:**

You can add multiple extension paths:

.. code-block:: ml

   ml[secure]> .addpath ./extensions
   ml[secure]> .addpath ../shared_modules
   ml[secure]> .addpath /opt/ml_modules

   # All three paths are now searched for modules

Capability Management Commands
------------------------------

``.capabilities``
~~~~~~~~~~~~~~~~~

Lists all currently granted capabilities.

**Usage:**

.. code-block:: text

   ml[secure]> .capabilities

**Example - No Capabilities:**

.. code-block:: ml

   ml[secure]> .capabilities
   No capabilities granted (security-restricted mode)

**Example - With Capabilities:**

.. code-block:: ml

   ml[secure]> .grant console.write
   ✓ Granted capability: console.write

   ml[secure]> .grant file.read
   ✓ Granted capability: file.read

   ml[secure]> .capabilities
   Active Capabilities:
     • console.write
     • file.read

**When to Use:**

- Verify granted capabilities
- Check security permissions
- Debug capability errors
- Review session security state

``.grant <capability>``
~~~~~~~~~~~~~~~~~~~~~~~

Grants a capability to allow access to restricted functionality.

**Usage:**

.. code-block:: text

   ml[secure]> .grant <capability-name>

**Security Confirmation:**

Granting capabilities requires explicit confirmation:

.. code-block:: ml

   ml[secure]> .grant file.read

   ⚠️  Security Warning: Granting capability 'file.read'
   This will allow ML code to access restricted functionality.
   Grant this capability? [y/N]: y
   ✓ Granted capability: file.read

**Common Capabilities:**

.. code-block:: ml

   # Console output
   ml[secure]> .grant console.write

   # File system
   ml[secure]> .grant file.read
   ml[secure]> .grant file.write

   # HTTP requests
   ml[secure]> .grant http.request

   # Path operations
   ml[secure]> .grant path.read
   ml[secure]> .grant path.write

**Capability Patterns:**

Grant capabilities with path/domain restrictions:

.. code-block:: ml

   # File access to specific directory
   ml[secure]> .grant file.read:/data/**

   # HTTP to specific domain
   ml[secure]> .grant http.request:https://api.example.com/**

**Example Workflow:**

.. code-block:: ml

   ml[secure]> import console;
   Error: Missing required capabilities: ['console.write']

   ml[secure]> .grant console.write
   ⚠️  Security Warning: Granting capability 'console.write'
   This will allow ML code to access restricted functionality.
   Grant this capability? [y/N]: y
   ✓ Granted capability: console.write

   ml[secure]> import console;
   ml[secure]> console.log("Hello!");
   Hello!

**When to Use:**

- Before importing modules that require capabilities
- When you get "Missing capability" errors
- To enable file I/O, network access, or system operations
- For testing code that needs special permissions

``.revoke <capability>``
~~~~~~~~~~~~~~~~~~~~~~~~

Revokes a previously granted capability.

**Usage:**

.. code-block:: text

   ml[secure]> .revoke <capability-name>

**Example:**

.. code-block:: ml

   ml[secure]> .capabilities
   Active Capabilities:
     • console.write
     • file.read

   ml[secure]> .revoke file.read
   ✓ Revoked capability: file.read

   ml[secure]> .capabilities
   Active Capabilities:
     • console.write

**When to Use:**

- Remove unnecessary permissions
- Test code with limited capabilities
- Enforce least-privilege security
- Clean up after experiments

Exit Commands
-------------

``.exit`` / ``.quit``
~~~~~~~~~~~~~~~~~~~~~

Exits the REPL and returns to the shell.

**Usage:**

.. code-block:: text

   ml[secure]> .exit
   ml[secure]> .quit

**Alternative:** Press ``Ctrl+D`` (Unix) or ``Ctrl+Z`` then Enter (Windows)

**What Happens:**

- Session state is lost (not saved)
- All variables are cleared
- Capabilities are reset
- History is cleared

**Saving Work Before Exit:**

The REPL doesn't automatically save your session. To preserve work:

1. **Copy commands from history** for reuse
2. **Save successful experiments to files** manually
3. **Document important findings** before exiting

Advanced Features
=================

Terminal Features
-----------------

mlpy REPL v2.1+ includes professional terminal features powered by ``prompt_toolkit``.

**Syntax Highlighting**

ML keywords, strings, numbers, and operators are highlighted in real-time:

.. code-block:: ml

   ml[secure]> function add(a, b) { return a + b; }
   #           ^^^^^^^^      ^     ^^^^^^
   #           keyword       |     keyword
   #                         identifier

**Auto-Completion**

Press ``Tab`` to autocomplete:

- **Variables:** Shows defined variable names
- **Functions:** Shows defined function names
- **Modules:** Shows imported module names
- **Keywords:** Shows ML language keywords

.. code-block:: ml

   ml[secure]> x = 10;
   ml[secure]> y = 20;
   ml[secure]> x[Tab]
   # Completes to: x or shows: x, y (if multiple matches)

**Command History**

Navigate previous commands with arrow keys:

- **Up Arrow:** Previous command
- **Down Arrow:** Next command
- **Ctrl+R:** Reverse search history

.. code-block:: ml

   ml[secure]> x = 42;
   ml[secure]> y = 100;
   # Press Up Arrow -> y = 100;
   # Press Up Arrow -> x = 42;

**Persistent History**

Command history is saved across REPL sessions (when terminal features are available).

**Line Editing**

Standard line editing with Emacs-style keybindings:

- **Ctrl+A:** Beginning of line
- **Ctrl+E:** End of line
- **Ctrl+K:** Kill to end of line
- **Ctrl+U:** Kill to beginning of line
- **Ctrl+W:** Kill previous word
- **Alt+Backspace:** Kill previous word

Output Paging
-------------

Results longer than 50 lines automatically trigger the pager (mlpy REPL v2.2+).

**Automatic Paging:**

.. code-block:: ml

   ml[secure]> large_array = range(0, 200);
   --- Output (202 lines) - Press Space to scroll, Q to quit ---
   [
     0,
     1,
     2,
     ...
   ]

**Pager Controls:**

- **Space:** Scroll down one page
- **Enter:** Scroll down one line
- **Q:** Quit pager and return to prompt
- **B:** Scroll back one page

**Pager System:**

The REPL uses a fallback system for maximum compatibility:

1. **prompt_toolkit pager** (best experience)
2. **System pager** (``less`` on Unix, ``more`` on Windows)
3. **Truncation** (fallback if no pager available)

**Configuration:**

Adjust the paging threshold (default: 50 lines):

.. code-block:: python

   # In session (if needed)
   # The threshold is configurable in mlpy.json for projects

Performance
-----------

mlpy REPL v2.3 Performance Characteristics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Execution Speed:**

- **Average:** 6.93ms per statement
- **Improvement:** 10.8x faster than v2.2 (was 75ms)
- **Complexity:** O(1) - constant time per statement
- **Scalability:** Performance doesn't degrade with session size

**Incremental Transpilation:**

Each statement is transpiled independently, not cumulatively:

.. code-block:: ml

   ml[secure]> x = 10;        # ~7ms
   ml[secure]> y = 20;        # ~7ms (still fast!)
   ml[secure]> z = x + y;     # ~7ms (still fast!)
   # ... 100 more statements
   ml[secure]> result = z * 2; # Still ~7ms!

**No Performance Penalty:**

- Variables persist efficiently
- Functions compile once, execute many times
- No performance reason to avoid REPL experimentation

**Memory Usage:**

The REPL maintains a single Python namespace for all statements, providing:

- Efficient variable storage
- Fast variable lookup
- Minimal memory overhead

Security
========

Security Model
--------------

The REPL includes the same capability-based security system as file-based programs.

**Default Security State:**

Programs start in security-restricted mode:

.. code-block:: ml

   ml[secure]> import file;
   Error: Missing required capabilities: ['file.read']

**Explicit Capability Grants:**

Capabilities must be explicitly granted:

.. code-block:: ml

   ml[secure]> .grant file.read
   ⚠️  Security Warning: Granting capability 'file.read'
   This will allow ML code to access restricted functionality.
   Grant this capability? [y/N]: y
   ✓ Granted capability: file.read

   ml[secure]> import file;
   ml[secure]> content = file.read("data.txt");
   ✓ Allowed - capability granted

Namespace Protection
--------------------

The REPL blocks access to dangerous Python internals:

**Blocked Identifiers (35+ total):**

- ``__builtins__`` - Access to Python builtins
- ``eval`` - Dynamic code execution
- ``exec`` - Dynamic code execution
- ``compile`` - Code compilation
- ``open`` - File I/O (use ``file`` module instead)
- ``__import__`` - Dynamic imports
- And 29 more dangerous functions

**Safe Wrappers:**

Some Python builtins are wrapped with ML-safe versions:

.. code-block:: ml

   ml[secure]> input("Enter name: ")
   # Uses ML's safe input() wrapper

   ml[secure]> help(math)
   # Uses ML's safe help() wrapper

**Security Violations:**

Attempts to access blocked identifiers fail:

.. code-block:: ml

   ml[secure]> __builtins__
   Error: Access to '__builtins__' is not allowed

   ml[secure]> eval("x = 10")
   Error: Access to 'eval' is not allowed

Capability Audit Trail
----------------------

All capability grants and revocations are logged:

.. code-block:: ml

   ml[secure]> .grant console.write
   # Logged: ("GRANT", "console.write", timestamp)

   ml[secure]> .revoke console.write
   # Logged: ("REVOKE", "console.write", timestamp)

**Audit Log Contents:**

- Action type (GRANT or REVOKE)
- Capability name
- Timestamp

**Session Isolation:**

- Audit log cleared on ``.reset``
- Each REPL session is independent
- No persistent state between sessions

Workflows and Patterns
======================

Learning ML
-----------

Use the REPL to learn ML syntax interactively:

**Experiment with Types:**

.. code-block:: ml

   ml[secure]> x = 42;
   ml[secure]> typeof(x)
   => "number"

   ml[secure]> name = "Alice";
   ml[secure]> typeof(name)
   => "string"

   ml[secure]> active = true;
   ml[secure]> typeof(active)
   => "boolean"

**Try Control Flow:**

.. code-block:: ml

   ml[secure]> score = 85;
   ml[secure]> if (score >= 90) {
   ...   "A"
   ... } elif (score >= 80) {
   ...   "B"
   ... } else {
   ...   "C"
   ... }
   => "B"

   ml[secure]> // Try different values
   ml[secure]> score = 95;
   ml[secure]> // Press Up Arrow twice to recall if statement

**Explore Operators:**

.. code-block:: ml

   ml[secure]> 10 > 5
   => true

   ml[secure]> "Hello" + " " + "World"
   => "Hello World"

   ml[secure]> [1, 2, 3] + [4, 5]
   => [1, 2, 3, 4, 5]

Prototyping Functions
---------------------

Develop functions incrementally in the REPL:

**Start Simple:**

.. code-block:: ml

   ml[secure]> function isPrime(n) {
   ...   if (n <= 1) { return false; }
   ...   if (n <= 3) { return true; }
   ...   return true;  // Placeholder
   ... }

   ml[secure]> isPrime(5)
   => true  # Works for now

**Refine Iteratively:**

.. code-block:: ml

   ml[secure]> .edit
   # Add complete implementation
   function isPrime(n) {
     if (n <= 1) { return false; }
     if (n <= 3) { return true; }
     i = 2;
     while (i * i <= n) {
       if (n % i == 0) { return false; }
       i = i + 1;
     }
     return true;
   }

   ml[secure]> isPrime(17)
   => true

   ml[secure]> isPrime(18)
   => false

**Test Edge Cases:**

.. code-block:: ml

   ml[secure]> isPrime(1)
   => false

   ml[secure]> isPrime(2)
   => true

   ml[secure]> isPrime(100)
   => false

Testing Standard Library
-------------------------

Explore standard library modules interactively:

**Math Module:**

.. code-block:: ml

   ml[secure]> import math;

   ml[secure]> math.sqrt(16)
   => 4.0

   ml[secure]> math.pow(2, 10)
   => 1024.0

   ml[secure]> math.sin(math.pi / 2)
   => 1.0

**Datetime Module:**

.. code-block:: ml

   ml[secure]> import datetime;

   ml[secure]> now = datetime.now();
   ml[secure]> now.year
   => 2025

   ml[secure]> now.month
   => 1

   ml[secure]> now.format("%Y-%m-%d")
   => "2025-01-07"

**Collections Module:**

.. code-block:: ml

   ml[secure]> import collections;

   ml[secure]> numbers = [1, 2, 3, 4, 5];
   ml[secure]> collections.map(numbers, fn(x) => x * 2)
   => [2, 4, 6, 8, 10]

   ml[secure]> collections.filter(numbers, fn(x) => x > 3)
   => [4, 5]

Debugging
---------

Use the REPL to debug issues step by step:

**Inspect Values:**

.. code-block:: ml

   ml[secure]> data = [1, 2, 3, 4, 5];
   ml[secure]> typeof(data)
   => "array"

   ml[secure]> len(data)
   => 5

   ml[secure]> data[0]
   => 1

**Test Functions:**

.. code-block:: ml

   ml[secure]> function average(arr) {
   ...   sum = 0;
   ...   i = 0;
   ...   while (i < len(arr)) {
   ...     sum = sum + arr[i];
   ...     i = i + 1;
   ...   }
   ...   return sum / len(arr);
   ... }

   ml[secure]> average([1, 2, 3, 4, 5])
   => 3.0

   ml[secure]> average([10])
   => 10.0

   ml[secure]> average([])
   Error: Division by zero  # Found a bug!

**Fix and Retry:**

.. code-block:: ml

   ml[secure]> function average(arr) {
   ...   if (len(arr) == 0) { return 0; }
   ...   sum = 0;
   ...   i = 0;
   ...   while (i < len(arr)) {
   ...     sum = sum + arr[i];
   ...     i = i + 1;
   ...   }
   ...   return sum / len(arr);
   ... }

   ml[secure]> average([])
   => 0  # Fixed!

Tips and Best Practices
========================

Do's
----

✅ **Use REPL for Learning**

Start every new concept in the REPL to understand it interactively.

✅ **Save Successful Experiments**

Copy working code from ``.history`` to files for reuse.

✅ **Use .vars to Track State**

Check what's defined regularly to avoid confusion.

✅ **Use .retry for Quick Fixes**

Fix syntax errors quickly without retyping.

✅ **Use .edit for Complex Code**

Edit complex functions in your full-featured editor.

✅ **Grant Capabilities Only When Needed**

Use least-privilege security - only grant what's required.

✅ **Use Tab-Completion**

Press Tab to discover available variables and functions.

✅ **Review .history**

Check history to remember what worked.

Don'ts
------

❌ **Don't Rely on REPL for Production**

REPL is for development - use files for production code.

❌ **Don't Grant Capabilities Unnecessarily**

Only grant capabilities you actually need.

❌ **Don't Forget to .revoke**

Revoke capabilities when you're done with them.

❌ **Don't Assume State Persists After Exit**

REPL state is lost on exit - save important work to files.

❌ **Don't Try to Access Python Internals**

The REPL blocks ``__builtins__``, ``eval``, ``exec``, etc. for security.

❌ **Don't Skip Security Warnings**

Read capability grant warnings carefully.

Performance Tips
----------------

**REPL v2.3 is Fast:**

- No performance penalty for experimentation
- 6.93ms average execution time
- Suitable for interactive development
- O(1) complexity per statement

**Variables Persist Efficiently:**

Defining many variables doesn't slow down the REPL.

**Functions Compile Once:**

Function definitions are fast, repeated calls are even faster.

Keyboard Shortcuts
------------------

**Navigation:**

- ``Tab`` - Auto-complete
- ``Up/Down Arrows`` - Command history
- ``Ctrl+R`` - Search history

**Editing:**

- ``Ctrl+A`` - Beginning of line
- ``Ctrl+E`` - End of line
- ``Ctrl+K`` - Kill to end of line
- ``Ctrl+U`` - Kill to beginning of line

**Control:**

- ``Ctrl+C`` - Cancel current input
- ``Ctrl+D`` - Exit REPL (Unix)
- ``Ctrl+Z + Enter`` - Exit REPL (Windows)

Common Patterns
===============

Quick Calculations
------------------

Use ML as a powerful calculator:

.. code-block:: ml

   ml[secure]> 42 * 365
   => 15330

   ml[secure]> import math;
   ml[secure]> math.sqrt(144)
   => 12.0

   ml[secure]> math.pow(2, 10)
   => 1024.0

Data Exploration
----------------

Explore data structures interactively:

.. code-block:: ml

   ml[secure]> data = [10, 25, 30, 15, 40];
   ml[secure]> len(data)
   => 5

   ml[secure]> import math;
   ml[secure]> math.max(data)
   => 40

   ml[secure]> math.min(data)
   => 10

   ml[secure]> import collections;
   ml[secure]> collections.sort(data)
   => [10, 15, 25, 30, 40]

Algorithm Prototyping
---------------------

Develop algorithms step by step:

.. code-block:: ml

   ml[secure]> // Bubble sort algorithm
   ml[secure]> function bubbleSort(arr) {
   ...   n = len(arr);
   ...   i = 0;
   ...   while (i < n) {
   ...     j = 0;
   ...     while (j < n - 1) {
   ...       if (arr[j] > arr[j + 1]) {
   ...         temp = arr[j];
   ...         arr[j] = arr[j + 1];
   ...         arr[j + 1] = temp;
   ...       }
   ...       j = j + 1;
   ...     }
   ...     i = i + 1;
   ...   }
   ...   return arr;
   ... }

   ml[secure]> bubbleSort([5, 2, 8, 1, 9])
   => [1, 2, 5, 8, 9]

Module Discovery
----------------

Explore module APIs interactively with the new module exploration commands:

**Using .modules and .modinfo:**

.. code-block:: ml

   ml[secure]> .modules
   Available Modules (11 total):
     Core:
       • math
       • random
     Data:
       • json
       • datetime
       • ...

   ml[secure]> .modinfo regex
   Module: regex
   Description: Regular expression pattern matching
   Version: 1.0.0
   Loaded: No

   Functions (8):
     • compile() - Compile regex pattern
     • match() - Match pattern against string
     • search() - Search for pattern in string
     ...

   ml[secure]> import regex;

   ml[secure]> pattern = regex.compile("[0-9]+");
   ml[secure]> pattern.match("Hello 123 World")
   => <Match object>

**Using builtin functions:**

.. code-block:: ml

   ml[secure]> // Check if module exists before importing
   ml[secure]> if (has_module("json")) {
   ...   import json;
   ...   json.stringify({name: "Alice", age: 30})
   ... }
   => "{\"name\":\"Alice\",\"age\":30}"

   ml[secure]> // Get all available modules
   ml[secure]> allModules = available_modules();
   ml[secure]> len(allModules)
   => 11

   ml[secure]> // Get detailed module info
   ml[secure]> info = module_info("math");
   ml[secure]> info.description
   => "Mathematical operations and constants"

Troubleshooting
===============

Common Issues
-------------

**Issue: Module Import Fails**

.. code-block:: ml

   ml[secure]> import file;
   Error: Missing required capabilities: ['file.read']

**Solution:** Grant required capabilities:

.. code-block:: ml

   ml[secure]> .grant file.read
   ml[secure]> import file;

---

**Issue: Variable Not Defined**

.. code-block:: ml

   ml[secure]> y
   Error: NameError: name 'y' is not defined

**Solution:** Check ``.vars`` to see what's defined, or define the variable:

.. code-block:: ml

   ml[secure]> .vars
   Variables:
     x = 10
   ml[secure]> y = 20;

---

**Issue: Lost Session State**

.. code-block:: ml

   ml[secure]> # Accidentally ran .clear
   ml[secure]> x
   Error: NameError: name 'x' is not defined

**Solution:** Variables are gone after ``.clear``. Redefine them or avoid using ``.clear`` unless you want to start fresh.

---

**Issue: Slow REPL Performance**

If you're on mlpy v2.2 or earlier, upgrade to v2.3 for 10.8x faster performance.

Error Messages
--------------

**Parse Errors:**

.. code-block:: ml

   ml[secure]> x = [1, 2, 3
   Error: Parse Error: Invalid ML syntax
   Tip: Check for missing semicolons, unmatched braces, or typos

**Security Errors:**

.. code-block:: ml

   ml[secure]> __builtins__
   Error: Access to '__builtins__' is not allowed

**Runtime Errors:**

.. code-block:: ml

   ml[secure]> 10 / 0
   Error: Division by zero

Getting Help
------------

**Within REPL:**

.. code-block:: text

   ml[secure]> .help

**Documentation:**

- :doc:`../tutorial/index` - ML language tutorial
- :doc:`../language-reference/index` - Complete syntax reference
- :doc:`../../standard-library/index` - Standard library modules

**Commands Quick Reference:**

- ``.help`` - Show all commands
- ``.vars`` - Show variables
- ``.history`` - Show history
- ``.modules`` - List available modules
- ``.modinfo <name>`` - Show module details
- ``.addpath <path>`` - Add extension directory
- ``.capabilities`` - Show capabilities
- ``.exit`` - Exit REPL

Summary
=======

The mlpy REPL is a powerful interactive environment for ML development. It provides:

**Key Features:**

- Immediate feedback for learning and experimentation
- Persistent variables across commands
- Multi-line input for complex code
- 14 powerful commands for session management and module exploration
- Capability-based security
- Professional terminal features
- Sub-10ms performance (v2.3)
- Automatic module discovery system

**Best For:**

- Learning ML syntax
- Testing code snippets
- Prototyping algorithms
- Debugging functions
- Exploring standard library
- Quick calculations

**Remember:**

- Start experiments in the REPL
- Move working code to files
- Use commands to manage your session
- Grant capabilities only when needed
- Review history to find successful code

**Next Steps:**

- :doc:`../tutorial/getting-started` - Start learning ML
- :doc:`transpilation` - Learn about running ML programs
- :doc:`capabilities` - Understand the security model
