# ML Language Debugger Implementation Proposal - Revised (sys.settrace() Approach)

## Executive Summary

This revised proposal outlines a **practical, incremental debugging system** for the ML language using Python's built-in `sys.settrace()` mechanism. The strategy prioritizes:

1. **Proof of Concept First** - Simple REPL debugger in 3-5 days
2. **Zero Production Overhead** - Pay for debugging only when debugging
3. **Pythonic Implementation** - Leverage standard library (settrace, cProfile)
4. **Incremental Enhancement** - CLI → DAP → IDE integration

**Key Decision:** Use `sys.settrace()` instead of AST instrumentation because:
- ✅ **Zero overhead when not debugging** (same generated code)
- ✅ **Simpler implementation** (200-300 LOC vs 500-800 LOC)
- ✅ **Live variable access** (real frames, not snapshots)
- ✅ **Standard Python debugging** (proven approach)
- ✅ **Faster time-to-value** (PoC in days, not weeks)

**Bonus:** Easy-win profiling with `cProfile` (5-minute implementation, 2-5% overhead)

---

## Architecture: sys.settrace() Based Debugging

### How It Works

```python
# 1. Transpile ML to Python (ONCE - no debug mode needed)
$ mlpy compile example.ml → example.py

# 2. Run normally - 0% overhead
$ mlpy run example.ml
# Just executes Python, no trace function

# 3. Debug when needed - 10-15% overhead
$ mlpy debug example.ml
# Sets sys.settrace(), enables debugging

# Trace function maps Python → ML positions:
def trace_callback(frame, event, arg):
    if event == 'line':
        py_line = frame.f_lineno
        ml_pos = source_map.py_to_ml(frame.f_code.co_filename, py_line)

        if ml_pos and debugger.should_break(ml_pos):
            debugger.pause_at(ml_pos, frame)  # Live frame access!

    return trace_callback

sys.settrace(trace_callback)
```

**Key Insight:** Same Python code runs at full speed OR with debugging - just toggle settrace()!

---

## Phase 1: Proof of Concept REPL Debugger (Days 1-3)

### Goal: Working CLI debugger for basic ML programs

**Deliverables:**
- Basic REPL debugger with essential commands
- Breakpoint support (line-based)
- Variable inspection (ML representation)
- Step execution (next/step/continue)
- Source map-based ML↔Python position mapping

### Implementation Plan

#### Day 1: Source Map Foundation (Building on Sprint 7)

**Status:** 40% complete via `enhanced_source_maps.py`

**Tasks:**
1. Extend `EnhancedSourceMap` to ensure all AST nodes record mappings
2. Create `SourceMapIndex` for bidirectional lookups:

```python
# src/mlpy/debugging/source_map_index.py

from dataclasses import dataclass
from collections import defaultdict
from mlpy.ml.codegen.enhanced_source_maps import EnhancedSourceMap

@dataclass
class SourceMapIndex:
    """Fast bidirectional ML↔Python position lookup."""

    # Forward: (ml_file, ml_line) → [py_lines]
    ml_to_py: dict[tuple[str, int], list[int]]

    # Reverse: (py_file, py_line) → (ml_file, ml_line, ml_col)
    py_to_ml: dict[tuple[str, int], tuple[str, int, int]]

    py_file: str

    @classmethod
    def from_source_map(cls, source_map: EnhancedSourceMap, py_file: str):
        """Build O(1) lookup index from source map."""
        ml_to_py = defaultdict(list)
        py_to_ml = {}

        for mapping in source_map.mappings:
            if mapping.original and mapping.source_file:
                # Forward lookup
                ml_key = (mapping.source_file, mapping.original.line)
                ml_to_py[ml_key].append(mapping.generated.line)

                # Reverse lookup
                py_key = (py_file, mapping.generated.line)
                py_to_ml[py_key] = (
                    mapping.source_file,
                    mapping.original.line,
                    mapping.original.column
                )

        # Sort Python lines for each ML line
        for ml_key in ml_to_py:
            ml_to_py[ml_key].sort()

        return cls(
            ml_to_py=dict(ml_to_py),
            py_to_ml=py_to_ml,
            py_file=py_file
        )

    def ml_line_to_first_py_line(self, ml_file: str, ml_line: int) -> int | None:
        """Get first Python line for ML line (for breakpoints)."""
        py_lines = self.ml_to_py.get((ml_file, ml_line), [])
        return py_lines[0] if py_lines else None

    def py_line_to_ml(self, py_file: str, py_line: int) -> tuple[str, int, int] | None:
        """Get ML position for Python line."""
        return self.py_to_ml.get((py_file, py_line))
```

**Test Coverage:**
- Test ML→Python mapping for all statement types
- Test Python→ML reverse lookup
- Test edge cases (comments, whitespace, multi-statement lines)

#### Day 2: Core Debugger Implementation

```python
# src/mlpy/debugging/debugger.py

import sys
from dataclasses import dataclass
from enum import Enum
from typing import Any

class StepMode(Enum):
    NONE = "none"
    NEXT = "next"      # Step to next ML line
    STEP = "step"      # Step into functions
    OUT = "out"        # Step out of function

@dataclass
class Breakpoint:
    """ML breakpoint."""
    id: int
    ml_file: str
    ml_line: int
    py_lines: list[int]  # Corresponding Python lines
    enabled: bool = True
    condition: str | None = None
    hit_count: int = 0

class MLDebugger:
    """Simple REPL debugger using sys.settrace()."""

    def __init__(self, ml_file: str, source_map_index: SourceMapIndex):
        self.ml_file = ml_file
        self.source_map_index = source_map_index
        self.breakpoints: dict[int, Breakpoint] = {}
        self.next_bp_id = 1
        self.step_mode = StepMode.NONE
        self.running = False
        self.current_frame = None
        self.current_ml_position: tuple[str, int, int] | None = None

    def set_breakpoint(self, ml_file: str, ml_line: int) -> Breakpoint | None:
        """Set breakpoint at ML line."""
        first_py_line = self.source_map_index.ml_line_to_first_py_line(ml_file, ml_line)

        if first_py_line is None:
            print(f"Error: Line {ml_line} is not executable")
            return None

        bp = Breakpoint(
            id=self.next_bp_id,
            ml_file=ml_file,
            ml_line=ml_line,
            py_lines=[first_py_line]
        )

        self.breakpoints[self.next_bp_id] = bp
        self.next_bp_id += 1

        print(f"Breakpoint {bp.id} set at {ml_file}:{ml_line}")
        return bp

    def trace_function(self, frame, event, arg):
        """Trace callback - checks breakpoints and stepping."""

        if event != 'line':
            return self.trace_function

        # Get Python position
        py_file = frame.f_code.co_filename
        py_line = frame.f_lineno

        # Skip if not our generated file
        if py_file != self.source_map_index.py_file:
            return self.trace_function

        # Map to ML position
        ml_pos = self.source_map_index.py_line_to_ml(py_file, py_line)

        if ml_pos is None:
            return self.trace_function

        ml_file, ml_line, ml_col = ml_pos

        # Check if should break
        if self._should_break(ml_file, ml_line, frame):
            self.current_frame = frame
            self.current_ml_position = ml_pos
            self._pause_execution()

        return self.trace_function

    def _should_break(self, ml_file: str, ml_line: int, frame) -> bool:
        """Check if should break at this position."""

        # Check breakpoints
        for bp in self.breakpoints.values():
            if bp.enabled and bp.ml_file == ml_file and bp.ml_line == ml_line:
                bp.hit_count += 1
                return True

        # Check step mode
        if self.step_mode == StepMode.NEXT:
            # Break at next ML line
            if self.current_ml_position:
                if ml_line != self.current_ml_position[1]:
                    self.step_mode = StepMode.NONE
                    return True

        return False

    def _pause_execution(self):
        """Pause and enter REPL."""
        self._show_current_location()

        # Enter command loop (will be implemented in Day 3)
        from .repl import DebuggerREPL
        repl = DebuggerREPL(self)
        repl.cmdloop()

    def _show_current_location(self):
        """Display current source location."""
        if not self.current_ml_position:
            return

        ml_file, ml_line, ml_col = self.current_ml_position

        # Read source file and show context
        with open(ml_file, 'r') as f:
            lines = f.readlines()

        # Show 2 lines before and after
        start = max(0, ml_line - 3)
        end = min(len(lines), ml_line + 2)

        print(f"\nBreakpoint at {ml_file}:{ml_line}")
        for i in range(start, end):
            marker = "=> " if i + 1 == ml_line else "   "
            print(f"{marker}{i+1:4} | {lines[i]}", end='')
        print()

    def get_variable(self, name: str) -> Any:
        """Get variable value from current frame."""
        if not self.current_frame:
            return None

        # Check locals first
        if name in self.current_frame.f_locals:
            return self.current_frame.f_locals[name]

        # Check globals
        if name in self.current_frame.f_globals:
            return self.current_frame.f_globals[name]

        return None

    def start(self):
        """Start debugging."""
        sys.settrace(self.trace_function)
        self.running = True

    def stop(self):
        """Stop debugging."""
        sys.settrace(None)
        self.running = False
```

#### Day 3: REPL Interface

```python
# src/mlpy/debugging/repl.py

import cmd
import sys

class DebuggerREPL(cmd.Cmd):
    """Interactive REPL for debugger."""

    intro = "ML Debugger - Type 'help' for commands"
    prompt = "[mldb] "

    def __init__(self, debugger):
        super().__init__()
        self.debugger = debugger

    def do_break(self, arg):
        """Set breakpoint: break <file>:<line> or break <line>"""
        if ':' in arg:
            file_part, line_part = arg.rsplit(':', 1)
            ml_file = file_part
        else:
            ml_file = self.debugger.ml_file
            line_part = arg

        try:
            ml_line = int(line_part)
            self.debugger.set_breakpoint(ml_file, ml_line)
        except ValueError:
            print(f"Invalid line number: {line_part}")

    def do_continue(self, arg):
        """Continue execution: continue or c"""
        self.debugger.step_mode = StepMode.NONE
        return True  # Exit cmdloop, resume execution

    do_c = do_continue  # Alias

    def do_next(self, arg):
        """Step to next line: next or n"""
        self.debugger.step_mode = StepMode.NEXT
        return True

    do_n = do_next

    def do_print(self, arg):
        """Print variable: print <var> or p <var>"""
        if not arg:
            print("Usage: print <variable>")
            return

        value = self.debugger.get_variable(arg)
        if value is None:
            print(f"{arg} = undefined")
        else:
            print(f"{arg} = {value} ({type(value).__name__})")

    do_p = do_print

    def do_list(self, arg):
        """Show source code: list"""
        self.debugger._show_current_location()

    do_l = do_list

    def do_info(self, arg):
        """Show info: info breakpoints"""
        if arg == "breakpoints" or arg == "b":
            if not self.debugger.breakpoints:
                print("No breakpoints set")
            else:
                print("Breakpoints:")
                for bp_id, bp in self.debugger.breakpoints.items():
                    status = "enabled" if bp.enabled else "disabled"
                    print(f"  {bp_id}: {bp.ml_file}:{bp.ml_line} ({status}, hit {bp.hit_count} times)")
        else:
            print("Usage: info breakpoints")

    def do_quit(self, arg):
        """Exit debugger: quit or q"""
        self.debugger.stop()
        sys.exit(0)

    do_q = do_quit

    def do_help(self, arg):
        """Show help"""
        if not arg:
            print("""
Available commands:
  break <line>      - Set breakpoint at line
  continue (c)      - Continue execution
  next (n)          - Step to next line
  print <var> (p)   - Print variable value
  list (l)          - Show source code
  info breakpoints  - List breakpoints
  quit (q)          - Exit debugger
  help              - Show this help
            """)
        else:
            super().do_help(arg)
```

#### CLI Integration

```python
# src/mlpy/cli/commands.py - Add DebugCommand

class DebugCommand(BaseCommand):
    """Debug ML programs interactively."""

    def register_parser(self, subparsers):
        parser = subparsers.add_parser(
            'debug',
            help='Debug ML programs interactively',
            description='Launch interactive debugging session'
        )
        parser.add_argument('source', help='ML source file to debug')
        parser.add_argument('args', nargs='*', help='Program arguments')
        parser.add_argument('--break-on-entry', action='store_true',
                          help='Stop at program entry')

    def execute(self, args):
        from mlpy.debugging.debugger import MLDebugger
        from mlpy.debugging.source_map_index import SourceMapIndex
        from mlpy.ml.codegen.enhanced_source_maps import EnhancedSourceMap

        # Transpile ML to Python
        print(f"Transpiling {args.source}...")
        from mlpy.ml.transpiler import transpile

        result = transpile(args.source)

        # Load source map
        source_map = result.source_map  # Assuming transpiler returns source map
        source_index = SourceMapIndex.from_source_map(source_map, result.output_file)

        # Create debugger
        debugger = MLDebugger(args.source, source_index)

        print("ML Debugger - Type 'help' for commands")
        print("Set breakpoints with 'break <line>', then 'continue' to start")

        # Enter initial REPL (to set breakpoints before running)
        from mlpy.debugging.repl import DebuggerREPL
        repl = DebuggerREPL(debugger)

        # Start with trace enabled
        debugger.start()

        # Read user commands until 'continue'
        repl.cmdloop()

        return 0
```

**PoC Success Criteria:**
- ✅ Can set breakpoints by ML line number
- ✅ Execution stops at breakpoints
- ✅ Can inspect variables
- ✅ Can step through ML code
- ✅ Source display shows ML code, not Python

---

## Phase 2: Enhanced Debugging Features (Days 4-7)

### Goal: Professional debugging experience

**Features:**
- Conditional breakpoints
- Call stack navigation
- Watch expressions
- Better variable formatting (ML objects/arrays)
- Multi-file debugging
- Exception breakpoints

**Implementation:** Extend PoC with advanced features

---

## Phase 3: Profiling Integration (Days 8-9)

### Goal: Zero-effort profiling using cProfile

**Easy Win Implementation:**

```python
# src/mlpy/runtime/profiler.py

import cProfile
import pstats
from io import StringIO

class MLProfiler:
    """Zero-instrumentation profiling using cProfile."""

    def __init__(self, source_map_index=None):
        self.profiler = cProfile.Profile()
        self.source_map_index = source_map_index

    def start(self):
        """Start profiling (2-5% overhead)."""
        self.profiler.enable()

    def stop(self):
        """Stop profiling."""
        self.profiler.disable()

    def print_stats(self, sort_by='cumulative', limit=20):
        """Print profiling statistics."""
        stream = StringIO()
        stats = pstats.Stats(self.profiler, stream=stream)
        stats.sort_stats(sort_by)
        stats.print_stats(limit)

        print(stream.getvalue())

    def get_ml_stats(self):
        """Translate Python function names to ML names."""
        stats = pstats.Stats(self.profiler)

        # Get raw stats
        for func, (cc, nc, tt, ct, callers) in stats.stats.items():
            filename, lineno, funcname = func

            # Look up ML function name
            if self.source_map_index:
                ml_pos = self.source_map_index.py_line_to_ml(filename, lineno)
                if ml_pos:
                    ml_file, ml_line, _ = ml_pos
                    # Find ML function name from source map
                    # ... translate and format

        # Return formatted ML statistics
```

**CLI Integration:**

```python
# Add --profile flag to run command
class RunCommand(BaseCommand):
    def register_parser(self, subparsers):
        parser = subparsers.add_parser('run', ...)
        parser.add_argument('--profile', action='store_true',
                          help='Enable profiling')
        parser.add_argument('--profile-sort', default='cumulative',
                          choices=['cumulative', 'time', 'calls'],
                          help='Sort profiling output')

    def execute(self, args):
        if args.profile:
            from mlpy.runtime.profiler import MLProfiler
            profiler = MLProfiler()
            profiler.start()

        # Run program
        result = self._run_ml_program(args.source)

        if args.profile:
            profiler.stop()
            print("\n=== Profiling Results ===")
            profiler.print_stats(sort_by=args.profile_sort)

        return result
```

**Usage:**
```bash
$ mlpy run --profile fibonacci.ml

=== Profiling Results ===
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
      100    0.003    0.000    0.015    0.000 fibonacci.py:15(fibonacci)
        1    0.000    0.000    0.015    0.015 fibonacci.py:1(<module>)
```

**Overhead:** Only 2-5% when `--profile` flag used, 0% otherwise!

---

## Phase 4: DAP Server (Days 10-15)

### Goal: Universal IDE integration via Debug Adapter Protocol

**Implementation:** Wrap debugger in DAP protocol handlers

**Key Advantage:** DAP works with VS Code, vim, Emacs, IntelliJ, etc.

---

## Phase 5: VS Code Extension Enhancement (Days 16-18)

### Goal: Native debugging in VS Code

**Implementation:** Add debug adapter to existing extension

---

## Performance Characteristics

### Overhead Analysis

| Mode | sys.settrace() | cProfile | AST Instrumentation |
|------|---------------|----------|---------------------|
| **Normal Run** | 0% | 0% | 1-3% |
| **Debugging** | 10-15% | N/A | 2-5% |
| **Profiling** | N/A | 2-5% | 2-5% (if implemented) |

**Key Insight:** With settrace/cProfile, you pay ONLY when using the feature!

### Lookup Performance

```python
# Breakpoint check (in trace function):
if py_line in breakpoint_py_lines:  # O(1) set membership - 50ns
    ml_pos = source_map.py_to_ml[(py_file, py_line)]  # O(1) dict - 100ns
    # Total: 150ns per traced line
```

**Typical program:** 100K lines executed → 15ms total overhead → 0.015% of execution time

**Real overhead comes from:** Python calling trace function (~1μs per line) → 100K × 1μs = 100ms

**10-15% overhead is from the tracing mechanism itself, not our code!**

---

## Implementation Timeline - Revised

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| **Phase 1: PoC REPL Debugger** | 3 days | Working CLI debugger |
| **Phase 2: Enhanced Features** | 4 days | Professional debugger |
| **Phase 3: Profiling** | 2 days | cProfile integration |
| **Phase 4: DAP Server** | 6 days | IDE-ready debugger |
| **Phase 5: VS Code Integration** | 3 days | Native VS Code debugging |
| **Total** | **18 days** | Full debugging suite |

**vs Original Proposal:** 18 days vs 25 days (7 days faster!)

---

## Success Metrics

### PoC Phase (Phase 1):
- ✅ Breakpoints work for all ML statement types
- ✅ Variable inspection shows correct values
- ✅ Stepping respects ML semantics
- ✅ <15% overhead during debugging
- ✅ 0% overhead when not debugging

### Production Phase (Phases 2-5):
- ✅ Professional debugging experience (DAP, IDE integration)
- ✅ Profiling with 2-5% overhead
- ✅ >95% test coverage
- ✅ Works in VS Code, vim, etc.

---

## Risks and Mitigations

### Risk 1: Source Map Completeness
**Risk:** Some ML constructs don't have Python mappings
**Mitigation:** Ensure all AST nodes record mappings during code generation
**Effort:** 1 day to audit and fix

### Risk 2: settrace() Overhead Too High
**Risk:** 15% overhead unacceptable for some use cases
**Mitigation:**
- Optimization: Only trace when breakpoints set
- Fallback: Hybrid approach (minimal instrumentation + settrace)
**Likelihood:** Low (15% is standard for Python debuggers)

### Risk 3: Complex Stepping Logic
**Risk:** ML line maps to multiple Python lines
**Mitigation:** Use "first Python line" strategy for breakpoints
**Status:** Solved in design

---

## Next Steps

1. **Approve revised proposal** using sys.settrace() approach
2. **Implement Phase 1 PoC** (3 days)
3. **Validate approach** with real ML programs
4. **Decide:** Continue to Phase 2 or adjust based on learnings

---

## Appendix: Why sys.settrace() Wins

### Technical Comparison

| Criterion | sys.settrace() | AST Instrumentation |
|-----------|---------------|---------------------|
| **Production Overhead** | 0% ✅ | 1-3% (or need dual build) |
| **Debug Overhead** | 10-15% | 2-5% ✅ |
| **Implementation** | 200-300 LOC ✅ | 500-800 LOC |
| **Variable Access** | Live frames ✅ | Snapshots (locals()) |
| **Code Bloat** | None ✅ | +20-40% |
| **Maintainability** | Simple ✅ | Complex (grammar coupled) |
| **Time to PoC** | 3 days ✅ | 2 weeks |

**Conclusion:** settrace() is the clear winner for initial implementation!

### Profiling Comparison

| Approach | Implementation | Overhead | When Active |
|----------|---------------|----------|-------------|
| **cProfile** | 5 minutes ✅ | 2-5% ✅ | Only with --profile ✅ |
| **sys.setprofile()** | 2 hours | 3-7% | Only when profiling |
| **AST Instrumentation** | 1 week | 2-5% | Always (unless dual build) |

**Conclusion:** cProfile is a massive easy win!

---

## References

- [Python sys.settrace() documentation](https://docs.python.org/3/library/sys.html#sys.settrace)
- [Python cProfile documentation](https://docs.python.org/3/library/profile.html)
- [Debug Adapter Protocol specification](https://microsoft.github.io/debug-adapter-protocol/)
- [Enhanced Source Maps (Sprint 7)](../ml/codegen/enhanced_source_maps.py)
