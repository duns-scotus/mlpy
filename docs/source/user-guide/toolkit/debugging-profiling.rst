====================================
ML Debugging and Profiling
====================================

.. note::
   **Production Ready: Interactive Debugger Available!**

   mlpy now includes a production-ready interactive debugger with multi-file support, automatic import detection, and professional IDE-style debugging capabilities.

This guide covers mlpy's debugging and profiling tools for identifying and fixing issues in ML programs.

.. contents::
   :local:
   :depth: 2

Overview
========

**Status:** Debugger Production Ready | Profiling Planned

mlpy provides comprehensive debugging tools to help you:

- ✅ **Interactive Debugging** - Set breakpoints, step through code, inspect variables
- ✅ **Multi-File Debugging** - Debug across your entire ML project
- ✅ **Automatic Import Detection** - Breakpoints activate when modules load
- ✅ **Source Map Persistence** - Debug cached transpiled code
- ✅ **Conditional Breakpoints** - Break only when conditions are met
- ✅ **Watch Expressions** - Monitor variable values automatically
- ✅ **Stack Navigation** - Navigate call stack and inspect frames
- 🚧 **Performance Profiling** - Coming soon
- 🚧 **Memory Analysis** - Planned for future release

Interactive Debugger
====================

**Status:** ✅ Production Ready

mlpy includes a full-featured interactive debugger that uses Python's ``sys.settrace()`` mechanism for line-by-line debugging without code instrumentation.

Quick Start
-----------

Start debugging any ML program:

.. code-block:: bash

   mlpy debug program.ml

This launches the interactive debugger with a command-line interface where you can set breakpoints, step through code, and inspect variables.

Basic Debugging Workflow
-------------------------

**Example debugging session:**

.. code-block:: text

   $ mlpy debug fibonacci.ml

   Transpiling fibonacci.ml...
   Cached: fibonacci.py + fibonacci.ml.map

   ML Debugger - Interactive Debugging Session
   Type 'help' for available commands

   # Set breakpoints before running
   (mldb) break fibonacci.ml:6
   Breakpoint 1 set at fibonacci.ml:6

   (mldb) break fibonacci.ml:12
   Breakpoint 2 set at fibonacci.ml:12

   # Start execution
   (mldb) continue
   Starting ML program...

   Breakpoint 1 hit
   => 6 | function fibonacci(n) {

   # Inspect variables
   (mldb) print n
   n = 10 (number)

   # Step through code
   (mldb) next
   => 7 |     if (n <= 1) {

   (mldb) step
   => 10 |     return fibonacci(n - 1) + fibonacci(n - 2);

   # Continue to next breakpoint
   (mldb) continue
   Breakpoint 2 hit
   => 12 | result = fibonacci(10);

Core Debugger Commands
-----------------------

Execution Control
~~~~~~~~~~~~~~~~~

.. code-block:: text

   continue (c)      - Continue execution until next breakpoint
   step (s)          - Step into function calls
   next (n)          - Step over function calls (next line)
   return (r)        - Continue until current function returns
   quit (q)          - Exit debugger

Breakpoints
~~~~~~~~~~~

.. code-block:: text

   break <line>              - Set breakpoint at line in current file
   break <file>:<line>       - Set breakpoint in specific file
   condition <id> <expr>     - Add condition to breakpoint
   delete <id>               - Delete breakpoint
   enable <id>               - Enable breakpoint
   disable <id>              - Disable breakpoint
   info breakpoints          - List all breakpoints (active and pending)

Variable Inspection
~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   print <var>         - Print variable value
   watch <expr>        - Add watch expression
   unwatch <id>        - Remove watch expression
   info watches        - Show all watch expressions
   info locals         - Show local variables
   info globals        - Show global variables
   info args           - Show function arguments

Stack Navigation
~~~~~~~~~~~~~~~~

.. code-block:: text

   where                - Show call stack
   up                   - Move up one stack frame
   down                 - Move down one stack frame
   frame <n>            - Jump to specific stack frame

Source Code Display
~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   list [n]            - Show source code (n lines of context)
   eval <expr>         - Evaluate ML expression safely

Multi-File Debugging
====================

**Status:** ✅ Production Ready with Automatic Import Detection

One of mlpy's most powerful features is the ability to debug across multiple ML files with automatic breakpoint activation.

Setting Breakpoints in Any File
--------------------------------

You can set breakpoints in **any ML file** in your project, even files that haven't been imported yet:

.. code-block:: bash

   $ mlpy debug main.ml

   (mldb) break main.ml:5
   Breakpoint 1 set at main.ml:5

   # Set breakpoint in unloaded module
   (mldb) break utils.ml:15
   Breakpoint 2 set at utils.ml:15 [PENDING - file not loaded yet]

   (mldb) break helpers.ml:42
   Breakpoint 3 set at helpers.ml:42 [PENDING - file not loaded yet]

   # View all breakpoints
   (mldb) info breakpoints
   Breakpoints:
     1: main.ml:5 [ACTIVE] (enabled, hit 0 times)
     2: utils.ml:15 [PENDING - file not loaded]
     3: helpers.ml:42 [PENDING - file not loaded]

   Total: 1 active, 2 pending

Automatic Import Detection
---------------------------

The debugger automatically detects when modules are imported and activates pending breakpoints:

.. code-block:: text

   (mldb) continue
   Starting ML program...

   # When your code runs: import utils
   Breakpoint 2 activated: utils.ml:15

   # When your code runs: import helpers
   Breakpoint 3 activated: helpers.ml:42

   Breakpoint 2 hit
   => 15 | function helper(a, b) {

**How It Works:**

1. Debugger wraps Python's ``__import__`` function
2. Detects when modules are loaded at runtime
3. Checks for corresponding ``.ml.map`` source map files
4. Automatically loads source maps and activates breakpoints
5. No user action required - completely automatic!

Manual Source Map Loading
--------------------------

If you need to manually load a source map before running:

.. code-block:: text

   (mldb) loadmap utils.ml
   Source map loaded for utils.ml
   Breakpoint 2 activated: utils.ml:15

Source Map Persistence
======================

**Status:** ✅ Production Ready

Source maps are automatically cached alongside transpiled Python files, enabling debugging of cached code without retranspilation.

How It Works
------------

When you compile or run ML programs, ``.ml.map`` files are created:

.. code-block:: bash

   mlpy compile program.ml --source-maps
   # Creates:
   #   program.py      (transpiled Python code)
   #   program.ml.map  (source map JSON file)

**Cache Workflow:**

.. code-block:: text

   program.ml  (modified at 10:00)
       ↓ transpile
   program.py       (created at 10:00)
   program.ml.map   (created at 10:00)

   --- User modifies program.ml at 10:30 ---

   program.ml  (modified at 10:30)  ← newer than .py/.ml.map
       ↓ timestamp check triggers retranspile
   program.py       (updated at 10:31)
   program.ml.map   (updated at 10:31)  ← regenerated together

Automatic Generation
--------------------

Source maps are generated automatically:

- ``mlpy compile --source-maps`` - Explicit source map generation
- ``mlpy run`` - Automatic generation for multi-file programs
- ``mlpy debug`` - Always generates and caches source maps

**Benefits:**

- Debug cached Python files without retranspilation
- Source maps regenerate when source changes
- Follows JavaScript/TypeScript ``.js.map`` convention
- Zero configuration required

Conditional Breakpoints
=======================

**Status:** ✅ Production Ready

Break only when specific conditions are met:

.. code-block:: text

   (mldb) break fibonacci.ml:10
   Breakpoint 1 set at fibonacci.ml:10

   # Add condition
   (mldb) condition 1 n > 5
   Breakpoint 1 condition set to: n > 5

   # Breakpoint only hits when n > 5
   (mldb) continue
   Breakpoint 1 hit (n = 6)
   => 10 | return fibonacci(n - 1) + fibonacci(n - 2);

   # Remove condition
   (mldb) condition 1
   Breakpoint 1 is now unconditional

**Conditional Pending Breakpoints:**

Conditions work even on pending breakpoints:

.. code-block:: text

   (mldb) break utils.ml:15
   Breakpoint 2 set [PENDING]

   (mldb) condition 2 value > 100
   Pending breakpoint 2 condition set to: value > 100

   # When module loads, condition is preserved
   (mldb) continue
   Breakpoint 2 activated: utils.ml:15
   => 15 | function process(value) {  // Only breaks when value > 100

Watch Expressions
=================

**Status:** ✅ Production Ready

Monitor variable values automatically at every pause:

.. code-block:: text

   (mldb) watch x
   Watch 1 added: x

   (mldb) watch count * 2
   Watch 2 added: count * 2

   (mldb) continue
   Breakpoint 1 hit

   Watches:
     1: x = 42 (number)
     2: count * 2 = 20 (number)

   # View all watches
   (mldb) info watches
   Watch Expressions:
     1: x = 42
     2: count * 2 = 20

   # Remove watch
   (mldb) unwatch 1
   Watch 1 removed

Stack Navigation
================

**Status:** ✅ Production Ready

Navigate the call stack and inspect different frames:

.. code-block:: text

   (mldb) where
   Call Stack:
     #0: helper() at utils.ml:15
     #1: process() at main.ml:28
     #2: main() at main.ml:42

   # Move up the stack
   (mldb) up
   Now in frame #1: process() at main.ml:28

   # Inspect variables in this frame
   (mldb) info locals
   Local variables:
     data = [1, 2, 3, 4, 5] (array)
     result = 0 (number)

   # Move down
   (mldb) down
   Now in frame #0: helper() at utils.ml:15

   # Jump to specific frame
   (mldb) frame 2
   Now in frame #2: main() at main.ml:42

Exception Breakpoints
=====================

**Status:** ✅ Production Ready

Break when exceptions are raised:

.. code-block:: text

   (mldb) break-on-exception
   Will break on all exceptions

   # Filter by exception type
   (mldb) break-on-exception ValueError
   Will break on ValueError exceptions

   (mldb) continue
   Exception breakpoint hit: ValueError
   => 25 | raise ValueError("Invalid input");

   # View exception details
   (mldb) exception
   Exception: ValueError
   Message: Invalid input

Architecture
============

The ML debugger is built on Python's ``sys.settrace()`` mechanism with several key components:

**Core Components:**

- **MLDebugger** - Main debugger using ``sys.settrace()`` (800+ LOC)
- **Import Hook System** - Automatic module load detection (200 LOC)
- **SourceMapIndex** - Bidirectional ML↔Python position mapping (160 LOC)
- **DebuggerREPL** - Interactive command-line interface (450+ LOC)
- **Safe Expression Evaluator** - Secure variable inspection
- **Variable Formatter** - ML-style variable display

**How It Works:**

.. code-block:: text

   ML Source (program.ml)
           ↓ Transpile
   Python Code + Source Map
           ↓ Execute with sys.settrace()
   Trace Function (every line)
           ↓ Map Python line → ML line
   Breakpoint Check
           ↓ If should pause
   REPL Interface (user commands)

**Key Design Decisions:**

- **Zero overhead when not debugging** - No code instrumentation
- **Live variable access** - Real frame inspection, not snapshots
- **Professional debugger pattern** - Deferred breakpoint resolution like VS Code, gdb
- **Security-first** - Safe expression evaluation prevents sandbox escape

Performance
===========

**Overhead:**

- **When not debugging:** 0% overhead (no code modification)
- **During debugging:** ~10-15% overhead (expected for any debugger)
- **Import hook:** Minimal overhead (< 1%)

**Optimization:**

- Fast breakpoint lookup with hash sets
- Lazy source map loading (only when needed)
- Cached source map reuse across sessions

Security
========

The debugger includes security features to prevent sandbox escape:

**Safe Expression Evaluation:**

.. code-block:: text

   (mldb) print x + 10          # ✅ Safe - arithmetic
   (mldb) print user.name       # ✅ Safe - property access
   (mldb) eval dangerous_code   # ❌ Blocked - security violation

**Restricted Operations:**

- No ``eval`` or ``exec`` in expressions
- No ``__import__`` or dangerous builtins
- No file system access through debugger
- No reflection abuse (``__class__``, ``__bases__``, etc.)

**Capabilities Integration:**

Debugger respects capability-based security - expressions are evaluated within the program's capability context.

Examples
========

Debugging Recursive Functions
------------------------------

.. code-block:: text

   $ mlpy debug fibonacci.ml

   (mldb) break fibonacci.ml:6
   Breakpoint 1 set

   (mldb) condition 1 n == 3

   (mldb) continue
   Breakpoint 1 hit (n = 3)
   => 6 | function fibonacci(n) {

   (mldb) print n
   n = 3 (number)

   (mldb) step
   => 7 |     if (n <= 1) {

   (mldb) where
   Call Stack:
     #0: fibonacci(n=3) at fibonacci.ml:6
     #1: fibonacci(n=4) at fibonacci.ml:10
     #2: fibonacci(n=5) at fibonacci.ml:10
     #3: main() at fibonacci.ml:15

Debugging Multi-File Projects
------------------------------

.. code-block:: text

   $ mlpy debug main.ml

   # Set breakpoints across multiple files
   (mldb) break main.ml:10
   Breakpoint 1 set at main.ml:10

   (mldb) break utils.ml:25
   Breakpoint 2 set at utils.ml:25 [PENDING]

   (mldb) break helpers.ml:42
   Breakpoint 3 set at helpers.ml:42 [PENDING]

   # Add watches
   (mldb) watch data.length
   Watch 1 added: data.length

   # Run program
   (mldb) continue

   Breakpoint 2 activated: utils.ml:25
   Breakpoint 1 hit
   => 10 | result = process(data);

   Watches:
     1: data.length = 100

   (mldb) step
   Breakpoint 2 hit
   => 25 | function process(data) {

   (mldb) list 5

      23 | }
      24 |
   => 25 | function process(data) {
      26 |     filtered = filter(data);
      27 |     sorted = sort(filtered);
      28 |     return sorted;
      29 | }

Debugging with Conditional Logic
---------------------------------

.. code-block:: text

   $ mlpy debug sort.ml

   (mldb) break quicksort.ml:15
   Breakpoint 1 set

   # Only break when array has specific length
   (mldb) condition 1 len(arr) > 100

   (mldb) continue
   Breakpoint 1 hit (len(arr) = 150)
   => 15 | pivot = arr[len(arr) / 2];

   (mldb) print arr.length
   arr.length = 150 (number)

   (mldb) print pivot
   pivot = 42 (number)

Best Practices
==============

Effective Debugging Workflow
-----------------------------

1. **Start with targeted breakpoints**

   .. code-block:: text

      # Don't break everywhere - be specific
      (mldb) break process_data.ml:42  # Where issue occurs
      (mldb) condition 1 data.size > 1000  # Narrow it down

2. **Use watch expressions for monitoring**

   .. code-block:: text

      (mldb) watch data.length
      (mldb) watch is_valid
      (mldb) watch cache.hits / cache.total  # Calculated expressions

3. **Navigate the stack strategically**

   .. code-block:: text

      (mldb) where            # See full call chain
      (mldb) up               # Check caller context
      (mldb) info locals      # Inspect caller's variables

4. **Use conditional breakpoints to reduce noise**

   .. code-block:: text

      # Instead of breaking 1000 times
      (mldb) break loop.ml:10
      (mldb) condition 1 i == 999  # Break only on last iteration

5. **Leverage source map caching**

   .. code-block:: bash

      # First debug session transpiles and caches
      mlpy debug program.ml

      # Subsequent sessions load from cache (faster startup)
      mlpy debug program.ml

Debugging Common Issues
-----------------------

**Undefined Variables:**

.. code-block:: text

   (mldb) break error_location.ml:25
   (mldb) continue
   => 25 | result = calculate(value);

   (mldb) print value
   value = <undefined>

   (mldb) info locals  # Check what's actually defined
   (mldb) up           # Check if defined in parent scope

**Infinite Loops:**

.. code-block:: text

   (mldb) break loop.ml:15
   (mldb) condition 1 counter > 1000  # Detect runaway loop
   (mldb) continue

   # When hits:
   (mldb) print counter
   counter = 10523  # Ah, loop condition is wrong!

**Wrong Results:**

.. code-block:: text

   (mldb) watch expected_value
   (mldb) watch actual_result
   (mldb) break calculation.ml:50
   (mldb) continue

   Watches:
     1: expected_value = 100
     2: actual_result = 42  # Discrepancy!

   (mldb) step  # Trace where it goes wrong

Limitations
===========

Current Limitations
-------------------

- **No hot reload** - Code changes require restart
- **No reverse debugging** - Can't step backwards
- **No data breakpoints** - Can't break on variable changes
- **Python internals visible** - Stack includes Python frames

Workarounds
-----------

**For hot reload:** Use the REPL for quick testing

.. code-block:: bash

   mlpy repl  # Test changes interactively

**For understanding changes:** Use watches heavily

.. code-block:: text

   (mldb) watch @before value  # Track value changes
   (mldb) watch @after value

Planned Features
================

Performance Profiling
---------------------

**Coming in Future Release**

Comprehensive performance profiling tools:

- Function-level timing
- Line-by-line profiling
- Call graph generation
- Hot spot identification
- Flamegraph visualization

Memory Analysis
---------------

**Coming in Future Release**

Track memory usage and identify leaks:

- Memory snapshots
- Allocation tracking
- Leak detection
- Object retention analysis

Code Coverage
-------------

**Coming in Future Release**

Analyze test coverage:

- Line coverage
- Branch coverage
- Coverage reports (HTML, JSON)

Related Documentation
======================

- :doc:`repl-guide` - Interactive REPL for testing
- :doc:`transpilation` - Source maps and compilation
- :doc:`capabilities` - Security and capability system
- CLI Reference - ``mlpy debug`` command options

For the complete technical documentation and architecture details, see: ``docs/PoC-Debug.md`` in the mlpy repository.

Troubleshooting
===============

Debugger Won't Start
--------------------

.. code-block:: bash

   # Check ML file exists
   ls program.ml

   # Try with verbose output
   mlpy debug program.ml --verbose

Breakpoints Not Hitting
------------------------

.. code-block:: text

   # Check if line is executable
   (mldb) list
   # Look for actual code, not comments/whitespace

   # For pending breakpoints, check file loaded
   (mldb) info breakpoints
   # Manually load if needed
   (mldb) loadmap utils.ml

Source Maps Missing
-------------------

.. code-block:: bash

   # Regenerate source maps
   mlpy compile program.ml --source-maps

   # Check map file exists
   ls program.ml.map

Variables Show as Undefined
----------------------------

.. code-block:: text

   (mldb) info locals   # Check local scope
   (mldb) info globals  # Check global scope
   (mldb) where         # Verify you're in right frame
   (mldb) up            # Try parent frame

Summary
=======

The mlpy debugger provides production-ready interactive debugging with:

✅ **Available Now:**

- Interactive debugging with breakpoints
- Multi-file debugging across entire projects
- Automatic import detection
- Conditional breakpoints and watch expressions
- Stack navigation and variable inspection
- Source map persistence and caching
- Secure expression evaluation

🚧 **Coming Soon:**

- Performance profiling
- Memory analysis
- Code coverage

**Get Started:**

.. code-block:: bash

   mlpy debug program.ml

**Set breakpoints anywhere, debug everywhere!**
