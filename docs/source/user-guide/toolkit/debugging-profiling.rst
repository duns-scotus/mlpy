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

**Status:** Debugger & Profiling Production Ready

mlpy provides comprehensive debugging and profiling tools to help you:

- ✅ **Interactive Debugging** - Set breakpoints, step through code, inspect variables
- ✅ **Multi-File Debugging** - Debug across your entire ML project
- ✅ **Automatic Import Detection** - Breakpoints activate when modules load
- ✅ **Source Map Persistence** - Debug cached transpiled code
- ✅ **Conditional Breakpoints** - Break only when conditions are met
- ✅ **Watch Expressions** - Monitor variable values automatically
- ✅ **Stack Navigation** - Navigate call stack and inspect frames
- ✅ **Performance Profiling** - 5 report types with memory tracking
- ✅ **Memory Analysis** - Automatic memory profiling per function
- 🚧 **Code Coverage** - Planned for future release

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

Performance Profiling
=====================

**Status:** ✅ Production Ready with Memory Tracking

mlpy includes a comprehensive performance profiling system with audience-specific reports, memory tracking, and flexible output options.

Quick Start
-----------

Profile any ML program with a single flag:

.. code-block:: bash

   mlpy run program.ml --profile

This generates a user-focused performance report showing where your ML code spends time and memory.

Profiling Overview
------------------

**Key Features:**

✅ **5 Report Types** - Targeted insights for users and developers
✅ **Memory Profiling** - Track memory usage per function (<5% overhead)
✅ **Flexible Output** - Save reports to files or print to console
✅ **Low Overhead** - 4-7% profiling overhead (acceptable for development)
✅ **User-Friendly Default** - Focus on your code, not mlpy internals

Report Types
------------

mlpy provides five different report types for different audiences:

1. ``--ml-summary`` (DEFAULT) - ML User Summary
2. ``--ml-details`` - ML User Detailed Analysis
3. ``--dev-summary`` - Developer Summary
4. ``--dev-details`` - Developer Detailed Analysis
5. ``--raw`` - Raw cProfile Output

ML User Reports
===============

ML Summary Report (Default)
----------------------------

**Audience:** ML developers optimizing their code

**Purpose:** Shows only your ML code performance, hides mlpy overhead

**Usage:**

.. code-block:: bash

   # Default behavior
   mlpy run program.ml --profile

   # Explicit
   mlpy run program.ml --profile --report ml-summary

**What You See:**

- Total execution time
- Your ML code execution time (excluding mlpy overhead)
- Top 10 ML functions by execution time
- ML files breakdown with memory usage
- Actionable optimization recommendations

**Example Output:**

.. code-block:: text

   ======================================================================
   ML CODE PERFORMANCE SUMMARY
   ======================================================================

   Total Execution Time: 2.456s
   ML Code Execution Time: 2.000s (81.5%)
   mlpy Overhead: 0.456s (18.5%)

   Memory Usage:
     Peak Memory: 45.2 MB

   Top ML Functions (by execution time):
   +--------------------------------------------------------------------+
   | Function                               | Time   | Calls  | Memory  |
   +--------------------------------------------------------------------+
   | process_batch (data_processor.ml:25)   | 0.600s | 10,000 | 12.5 MB |
   | main (main.ml:42)                      | 0.550s |      1 | 8.2 MB  |
   | transform_data (utils.ml:15)           | 0.250s |  5,000 | 6.3 MB  |
   | validate (helpers.ml:30)               | 0.150s |  2,345 | 3.1 MB  |
   +--------------------------------------------------------------------+

   ML Files (by execution time):
   +--------------------------------------------------------------------+
   | File                      | Time   | Calls  | Memory  |
   +--------------------------------------------------------------------+
   | data_processor.ml         | 0.700s | 10,000 | 15.2 MB |
   | main.ml                   | 0.800s |  1,234 | 10.5 MB |
   | utils.ml                  | 0.300s |  5,678 | 5.8 MB  |
   | helpers.ml                | 0.200s |  2,345 | 3.3 MB  |
   +--------------------------------------------------------------------+

   OPTIMIZATION RECOMMENDATIONS:

   ▸ process_batch() (data_processor.ml:25) - 30.0% of execution time
     - This function is your main performance bottleneck
     - Consider: caching repeated calculations, reducing loop iterations
     - Memory: 12.5 MB used - check for unnecessary array copies

   ▸ main() (main.ml:42) - 27.5% of execution time
     - Second most expensive function
     - Review algorithm complexity - can this be optimized?

   ✓ Overall Assessment:
     - Your ML code is the dominant factor (>80% of time)
     - Focus optimization efforts on top 2 functions above

**When to Use:**

- Optimizing your ML code performance
- Finding performance bottlenecks in your functions
- Understanding memory usage patterns
- Getting actionable optimization suggestions

ML Details Report
-----------------

**Audience:** ML developers doing deep performance investigation

**Purpose:** Shows all ML functions grouped by module

**Usage:**

.. code-block:: bash

   mlpy run program.ml --profile --report ml-details

**What You See:**

- All ML functions (not just top 10)
- Grouped hierarchically by ML file
- Memory usage per function
- Call counts and average times per call
- Percentage breakdown within each file

**Example Output:**

.. code-block:: text

   ======================================================================
   ML CODE DETAILED ANALYSIS
   ======================================================================

   Total Execution Time: 2.456s
   ML Code Execution Time: 2.000s (81.5%)

   +--------------------------------------------------------------------+
   | data_processor.ml (0.700s, 35.0%, 12.5 MB)                         |
   +--------------------------------------------------------------------+
   | Function                 Time     % File  Calls  Memory  |
   +--------------------------------------------------------------------+
   | process_batch (line 25)  0.600s   85.7%  10,000  10.2 MB |
   | validate_input (line 5)  0.050s    7.1%   1,000   1.5 MB |
   | parse_record (line 15)   0.030s    4.3%   5,000   0.8 MB |
   | format_output (line 35)  0.020s    2.9%   1,000   0.0 MB |
   +--------------------------------------------------------------------+

   +--------------------------------------------------------------------+
   | main.ml (0.800s, 40.0%, 10.5 MB)                                   |
   +--------------------------------------------------------------------+
   | Function                 Time     % File  Calls  Memory  |
   +--------------------------------------------------------------------+
   | main (line 42)           0.550s   68.8%       1   8.0 MB |
   | initialize (line 10)     0.150s   18.8%       1   1.5 MB |
   | cleanup (line 80)        0.100s   12.5%       1   1.0 MB |
   +--------------------------------------------------------------------+

**When to Use:**

- Investigating all functions in a module
- Understanding call patterns and frequencies
- Finding hidden performance issues
- Analyzing memory usage across entire files

Developer Reports
=================

Developer Summary Report
------------------------

**Audience:** mlpy contributors optimizing the compiler/runtime

**Purpose:** Shows mlpy internal overhead breakdown

**Usage:**

.. code-block:: bash

   mlpy run program.ml --profile --report dev-summary

**What You See:**

- All categories (mlpy internals + user code)
- Parsing, transpilation, security analysis overhead
- Runtime overhead (safe_call, safe_attr_access, etc.)
- Top functions across all categories
- Memory breakdown by category

**Example Output:**

.. code-block:: text

   ======================================================================
   MLPY PERFORMANCE SUMMARY REPORT (Developer View)
   ======================================================================

   Total Execution Time: 2.456s

   Time Breakdown (by category):
   +---------------------+----------+----------+
   | Category            | Time     | % Total  |
   +---------------------+----------+----------+
   | ML Code Execution   | 2.000s   |  81.5%   |
   | Python Stdlib       | 0.456s   |  18.6%   |
   | Parsing             | 0.045s   |   1.8%   |
   | Transpilation       | 0.087s   |   3.5%   |
   | Runtime Overhead    | 0.246s   |  10.0%   |
   | Sandbox Startup     | 0.050s   |   2.0%   |
   | Security Analysis   | 0.028s   |   1.1%   |
   +---------------------+----------+----------+

   Memory Breakdown:
   +---------------------+----------+
   | Category            | Memory   |
   +---------------------+----------+
   | ML Code             | 32.8 MB  |
   | Runtime Overhead    | 8.5 MB   |
   | Parsing/Transpile   | 4.2 MB   |
   | Total Peak          | 45.2 MB  |
   +---------------------+----------+

**When to Use:**

- Optimizing mlpy compiler/runtime performance
- Understanding mlpy overhead impact
- Benchmarking mlpy improvements
- Identifying performance regressions

Developer Details Report
------------------------

**Audience:** mlpy contributors doing deep optimization

**Purpose:** Shows detailed breakdown of mlpy internal functions

**Usage:**

.. code-block:: bash

   mlpy run program.ml --profile --report dev-details

**What You See:**

- Detailed per-category function breakdown
- Top 10 functions per mlpy category
- Specific runtime overhead functions
- mlpy-specific optimization recommendations

**Example Output:**

.. code-block:: text

   ======================================================================
   MLPY INTERNAL PERFORMANCE ANALYSIS (Developer View)
   ======================================================================

   Total mlpy Overhead: 0.456s (18.6% of total)

   +--------------------------------------------------------------------+
   | RUNTIME OVERHEAD (0.246s, 10.0%, 8.5 MB)                          |
   +--------------------------------------------------------------------+
   | Function                      Time    Calls  Memory              |
   +--------------------------------------------------------------------+
   | safe_call                     0.120s  15,234  4.2 MB             |
   | safe_attr_access              0.080s  10,456  2.8 MB             |
   | safe_method_call              0.030s   3,890  1.2 MB             |
   | check_capabilities            0.016s   1,234  0.3 MB             |
   +--------------------------------------------------------------------+

   +--------------------------------------------------------------------+
   | PARSING (0.045s, 1.8%, 2.1 MB)                                     |
   +--------------------------------------------------------------------+
   | Function                      Time    Calls  Memory              |
   +--------------------------------------------------------------------+
   | parse                         0.023s       1  1.2 MB             |
   | _parse                        0.015s      75  0.6 MB             |
   | compute_lookaheads            0.007s       2  0.3 MB             |
   +--------------------------------------------------------------------+

**When to Use:**

- Identifying mlpy performance bottlenecks
- Optimizing specific mlpy components
- Understanding runtime overhead sources
- Benchmarking compiler improvements

Raw cProfile Output
-------------------

**Audience:** Advanced users, automation tools, external analyzers

**Purpose:** Standard cProfile format for further analysis

**Usage:**

.. code-block:: bash

   mlpy run program.ml --profile --report raw

**What You See:**

- Standard Python cProfile statistics
- All functions with no filtering or categorization
- Machine-parseable format
- Sortable by time/calls/name

**Example Output:**

.. code-block:: text

      ncalls  tottime  percall  cumtime  percall filename:lineno(function)
       10000    0.600    0.000    0.600    0.000 data_processor.py:25(process_batch)
           1    0.550    0.550    2.000    2.000 main.py:42(main)
        5678    0.300    0.000    0.300    0.000 utils.py:15(transform_data)
       15234    0.120    0.000    0.150    0.000 whitelist_validator.py:45(safe_call)
       10456    0.080    0.000    0.090    0.000 whitelist_validator.py:52(safe_attr_access)

**When to Use:**

- Exporting to external profiling tools
- Custom analysis with Python scripts
- Integration with CI/CD pipelines
- Comparing with other Python profilers

Multiple Reports
================

Generate Multiple Reports at Once
----------------------------------

You can request multiple report types in a single run:

.. code-block:: bash

   # Both ML and developer summaries
   mlpy run program.ml --profile --report ml-summary --report dev-summary

   # User summary and details
   mlpy run program.ml --profile --report ml-summary --report ml-details

   # All reports
   mlpy run program.ml --profile --report all

**Output:** Reports are displayed sequentially, separated by dividers.

File Output
===========

Save Reports to Files
---------------------

Instead of printing to console, save reports to a file:

.. code-block:: bash

   # Save default report
   mlpy run program.ml --profile --profile-output performance.txt

   # Save specific report type
   mlpy run program.ml --profile --report dev-summary --profile-output analysis.txt

   # Save all reports
   mlpy run program.ml --profile --report all --profile-output full_report.txt

**Benefits:**

- Keep historical performance data
- Share reports with team members
- Compare performance across versions
- Integrate with documentation systems

Advanced Usage
==============

Profiling with Force Transpile
-------------------------------

Measure cold-start performance by forcing retranspilation:

.. code-block:: bash

   # Profile with cache bypass
   mlpy run program.ml --profile --force-transpile --report dev-summary

**Use Cases:**

- Benchmarking compiler performance
- Measuring transpilation overhead
- Testing parser optimizations
- Comparing cold vs cached performance

Profiling Long-Running Programs
--------------------------------

For programs that execute significant ML code:

.. code-block:: bash

   mlpy run complex_algorithm.ml --profile --report ml-summary

**Best Practices:**

- Use ml-summary for user code optimization
- Focus on functions with >10% time share
- Check memory usage for large data structures
- Use ml-details for comprehensive analysis

Profiling with Capabilities
----------------------------

Profile programs using capability-based security:

.. code-block:: bash

   mlpy run network_app.ml --profile --allow-network --report ml-summary

**Note:** Profiling overhead includes capability checking functions.

Memory Profiling
================

Memory Tracking Features
------------------------

**Automatic Memory Profiling:**

- Tracks memory allocation per function
- Shows peak memory usage
- Identifies memory-heavy operations
- <5% overhead (using Python's tracemalloc)

**Memory Metrics:**

- **Peak Memory**: Maximum memory used during execution
- **Per-Function Memory**: Memory attributed to each function
- **Per-File Memory**: Aggregated memory by ML file

Understanding Memory Reports
-----------------------------

**Example:**

.. code-block:: text

   Memory Usage:
     Peak Memory: 45.2 MB

   Top ML Functions:
   | Function              | Time   | Memory  |
   |-----------------------|--------|---------|
   | process_batch()       | 0.600s | 12.5 MB | ← High memory!
   | main()                | 0.550s | 8.2 MB  |

**Interpreting Results:**

- Functions with high memory may be creating large data structures
- Check for unnecessary array copies
- Look for memory leaks in loops
- Consider streaming data instead of loading all at once

Optimization Tips
=================

Using Profiling for Optimization
---------------------------------

**1. Find the Hot Spots**

.. code-block:: bash

   mlpy run program.ml --profile --report ml-summary

Look at "Top ML Functions" - focus on functions using >20% of time.

**2. Drill Down with Details**

.. code-block:: bash

   mlpy run program.ml --profile --report ml-details

Examine all functions in the hot module to find hidden issues.

**3. Check Memory Usage**

Look at the Memory column - functions using >10 MB may benefit from optimization.

**4. Iterate and Measure**

.. code-block:: bash

   # Before optimization
   mlpy run program.ml --profile --profile-output before.txt

   # Make changes to your ML code

   # After optimization
   mlpy run program.ml --profile --profile-output after.txt

   # Compare the two reports

Common Optimization Patterns
-----------------------------

**Reduce Loop Iterations:**

.. code-block:: text

   ▸ process_items() - 50% of time, 10,000 calls
     → Can you batch operations or cache results?

**Optimize Algorithm Complexity:**

.. code-block:: text

   ▸ sort_data() - 40% of time
     → Consider using a more efficient sorting algorithm

**Reduce Memory Allocations:**

.. code-block:: text

   ▸ transform() - 12.5 MB memory
     → Reuse arrays instead of creating new ones

**Cache Expensive Calculations:**

.. code-block:: text

   ▸ calculate() - 30% of time, 5,000 identical calls
     → Add caching for repeated inputs

Performance Targets
===================

What's Good Performance?
------------------------

**mlpy Overhead:**

- **Excellent:** <20% mlpy overhead
- **Good:** 20-30% mlpy overhead
- **Acceptable:** 30-50% mlpy overhead
- **High:** >50% mlpy overhead (I/O-heavy programs are normal)

**User Code Focus:**

- **Goal:** Your ML code should be >50% of total time
- If mlpy overhead dominates, your code is efficient!
- Focus optimization on functions using >10% of *your* code time

Profiling Overhead
------------------

**Expected Overhead:**

- **Time Profiling Only:** 2-5% overhead
- **Time + Memory Profiling:** 4-7% overhead
- **Total:** <10% overhead (acceptable for development)

**Impact:**

- Overhead is consistent across runs
- Relative performance comparisons are accurate
- Absolute times slightly inflated by profiling

Best Practices
==============

Effective Profiling Workflow
-----------------------------

**1. Start with Default Report**

.. code-block:: bash

   mlpy run program.ml --profile

The ml-summary report shows you the most important information first.

**2. Save Baseline Performance**

.. code-block:: bash

   mlpy run program.ml --profile --profile-output baseline.txt

Keep this for comparison after optimization.

**3. Focus on Top Functions**

Don't try to optimize everything - focus on functions using >20% of time.

**4. Measure After Each Change**

.. code-block:: bash

   mlpy run program.ml --profile --profile-output v2.txt

Compare with baseline to verify improvements.

**5. Use Memory Reports**

High memory usage often correlates with slow performance.

When to Profile
---------------

**During Development:**

- After implementing new features
- When performance seems slow
- Before optimizing (measure first!)

**Before Release:**

- Profile with realistic data sizes
- Test with production-like workloads
- Identify scalability issues

**After Optimization:**

- Verify improvements with profiling
- Ensure no regressions in other areas
- Document performance characteristics

Limitations
===========

Current Limitations
-------------------

- **ML User Reports:** May show "No ML user code detected" for programs executed in sandbox (framework limitation)
- **Memory Attribution:** Memory tracked per-file, not per-line
- **Profiling Overhead:** 4-7% overhead during profiling
- **Report Formats:** Text only (no HTML/graphical visualization)

Workarounds
-----------

**For ML User Reports:**

Use developer reports (``--report dev-summary``) to see full breakdown when ML code detection fails.

**For Fine-Grained Analysis:**

Use ``--report raw`` and external profiling tools for advanced visualization.

Planned Enhancements
====================

Future improvements planned:

- Per-line profiling (show time per line of ML code)
- Flame graph visualization
- HTML report generation
- Historical performance tracking
- Comparison mode (before/after optimization)
- Integration with IDE profiling tools

Code Coverage
-------------

**Planned for Future Release**

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

mlpy provides production-ready debugging and profiling tools:

✅ **Interactive Debugger:**

- Set breakpoints, step through code, inspect variables
- Multi-file debugging across entire projects
- Automatic import detection and activation
- Conditional breakpoints and watch expressions
- Stack navigation and variable inspection
- Source map persistence and caching
- Secure expression evaluation

✅ **Performance Profiler:**

- 5 report types (ML user, developer, raw)
- Memory profiling per function (<5% overhead)
- Flexible file output
- Actionable optimization recommendations
- User-friendly default (ml-summary)

🚧 **Coming Soon:**

- Code coverage analysis
- Per-line profiling
- Flame graph visualization

**Get Started with Debugging:**

.. code-block:: bash

   mlpy debug program.ml

**Get Started with Profiling:**

.. code-block:: bash

   mlpy run program.ml --profile

**Debug everywhere, optimize everything!**
