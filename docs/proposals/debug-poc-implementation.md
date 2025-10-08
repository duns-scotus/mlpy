# Debug PoC Implementation Guide - 3-Day Sprint

## Goal
Working REPL debugger using sys.settrace() in 3 days

## Prerequisites
- ✅ Sprint 7's `EnhancedSourceMap` (already exists)
- ✅ Working transpiler with source map generation
- ✅ CLI infrastructure (BaseCommand pattern)

---

## Day 1: Source Map Index (4-6 hours)

### Task 1.1: Create SourceMapIndex Class (2 hours)

**File:** `src/mlpy/debugging/source_map_index.py`

```python
"""Bidirectional ML↔Python source position lookup."""

from dataclasses import dataclass
from collections import defaultdict
from typing import Optional
from mlpy.ml.codegen.enhanced_source_maps import EnhancedSourceMap


@dataclass
class SourceMapIndex:
    """Fast O(1) bidirectional source position lookup."""

    # Forward: (ml_file, ml_line) → [py_lines]
    ml_to_py: dict[tuple[str, int], list[int]]

    # Reverse: (py_file, py_line) → (ml_file, ml_line, ml_col)
    py_to_ml: dict[tuple[str, int], tuple[str, int, int]]

    # Generated Python filename
    py_file: str

    @classmethod
    def from_source_map(cls, source_map: EnhancedSourceMap, py_file: str) -> 'SourceMapIndex':
        """Build lookup index from source map.

        Args:
            source_map: Enhanced source map from transpilation
            py_file: Path to generated Python file

        Returns:
            Indexed source map for fast lookups
        """
        ml_to_py = defaultdict(list)
        py_to_ml = {}

        for mapping in source_map.mappings:
            if mapping.original and mapping.source_file:
                # Forward lookup: ML → Python
                ml_key = (mapping.source_file, mapping.original.line)
                py_line = mapping.generated.line
                ml_to_py[ml_key].append(py_line)

                # Reverse lookup: Python → ML
                py_key = (py_file, py_line)
                py_to_ml[py_key] = (
                    mapping.source_file,
                    mapping.original.line,
                    mapping.original.column
                )

        # Sort Python lines for each ML line (handle multi-line statements)
        for ml_key in ml_to_py:
            ml_to_py[ml_key].sort()

        return cls(
            ml_to_py=dict(ml_to_py),
            py_to_ml=py_to_ml,
            py_file=py_file
        )

    def ml_line_to_first_py_line(self, ml_file: str, ml_line: int) -> Optional[int]:
        """Get first Python line for an ML line (for breakpoints).

        Args:
            ml_file: ML source file path
            ml_line: ML line number (1-indexed)

        Returns:
            First Python line number, or None if line not executable
        """
        py_lines = self.ml_to_py.get((ml_file, ml_line), [])
        return py_lines[0] if py_lines else None

    def ml_line_to_all_py_lines(self, ml_file: str, ml_line: int) -> list[int]:
        """Get all Python lines for an ML line.

        Useful for complex statements that generate multiple Python lines.
        """
        return self.ml_to_py.get((ml_file, ml_line), [])

    def py_line_to_ml(self, py_file: str, py_line: int) -> Optional[tuple[str, int, int]]:
        """Get ML position for a Python line.

        Args:
            py_file: Python file path
            py_line: Python line number

        Returns:
            Tuple of (ml_file, ml_line, ml_col) or None
        """
        return self.py_to_ml.get((py_file, py_line))

    def is_ml_line_executable(self, ml_file: str, ml_line: int) -> bool:
        """Check if ML line is executable (has Python mapping)."""
        return (ml_file, ml_line) in self.ml_to_py

    def get_next_ml_line(self, ml_file: str, current_ml_line: int) -> Optional[int]:
        """Get next executable ML line after current line.

        Useful for stepping to next line.
        """
        # Get all ML lines in this file
        ml_lines = sorted(set(
            ml_line for (mf, ml_line) in self.ml_to_py.keys()
            if mf == ml_file
        ))

        # Find next line
        for ml_line in ml_lines:
            if ml_line > current_ml_line:
                return ml_line

        return None  # No next line (end of file)
```

**Test:** `tests/unit/debugging/test_source_map_index.py`

```python
"""Test source map indexing."""

import pytest
from mlpy.debugging.source_map_index import SourceMapIndex
from mlpy.ml.codegen.enhanced_source_maps import (
    EnhancedSourceMap,
    SourceMapping,
    SourceLocation
)


def test_bidirectional_lookup():
    """Test ML→Python and Python→ML lookups."""
    source_map = EnhancedSourceMap()

    # Add mappings
    source_map.add_mapping(SourceMapping(
        generated=SourceLocation(line=10, column=0),
        original=SourceLocation(line=5, column=0),
        source_file='test.ml',
        node_type='assignment'
    ))

    source_map.add_mapping(SourceMapping(
        generated=SourceLocation(line=11, column=0),
        original=SourceLocation(line=6, column=0),
        source_file='test.ml',
        node_type='return'
    ))

    # Build index
    index = SourceMapIndex.from_source_map(source_map, 'test.py')

    # Test forward lookup
    assert index.ml_line_to_first_py_line('test.ml', 5) == 10
    assert index.ml_line_to_first_py_line('test.ml', 6) == 11

    # Test reverse lookup
    assert index.py_line_to_ml('test.py', 10) == ('test.ml', 5, 0)
    assert index.py_line_to_ml('test.py', 11) == ('test.ml', 6, 0)

    # Test invalid lookups
    assert index.ml_line_to_first_py_line('test.ml', 99) is None
    assert index.py_line_to_ml('test.py', 99) is None


def test_multi_line_statement():
    """Test ML line that generates multiple Python lines."""
    source_map = EnhancedSourceMap()

    # ML line 5 generates Python lines 10, 11, 12
    for py_line in [10, 11, 12]:
        source_map.add_mapping(SourceMapping(
            generated=SourceLocation(line=py_line, column=0),
            original=SourceLocation(line=5, column=0),
            source_file='test.ml'
        ))

    index = SourceMapIndex.from_source_map(source_map, 'test.py')

    # Should get first Python line
    assert index.ml_line_to_first_py_line('test.ml', 5) == 10

    # Should get all Python lines
    assert index.ml_line_to_all_py_lines('test.ml', 5) == [10, 11, 12]

    # All Python lines map back to same ML line
    assert index.py_line_to_ml('test.py', 10) == ('test.ml', 5, 0)
    assert index.py_line_to_ml('test.py', 11) == ('test.ml', 5, 0)
    assert index.py_line_to_ml('test.py', 12) == ('test.ml', 5, 0)


def test_next_line():
    """Test finding next executable ML line."""
    source_map = EnhancedSourceMap()

    # Add non-consecutive ML lines (comments/whitespace skipped)
    for ml_line, py_line in [(5, 10), (7, 11), (10, 12)]:
        source_map.add_mapping(SourceMapping(
            generated=SourceLocation(line=py_line, column=0),
            original=SourceLocation(line=ml_line, column=0),
            source_file='test.ml'
        ))

    index = SourceMapIndex.from_source_map(source_map, 'test.py')

    # Test next line navigation
    assert index.get_next_ml_line('test.ml', 5) == 7
    assert index.get_next_ml_line('test.ml', 7) == 10
    assert index.get_next_ml_line('test.ml', 10) is None  # End of file
```

**Acceptance Criteria:**
- ✅ Can map ML line → Python line(s)
- ✅ Can map Python line → ML line
- ✅ Handles multi-line ML statements
- ✅ All tests pass

---

## Day 2: Core Debugger (6-8 hours)

### Task 2.1: Create Core Debugger (4 hours)

**File:** `src/mlpy/debugging/debugger.py`

```python
"""Core ML debugger using sys.settrace()."""

import sys
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, Callable
from pathlib import Path

from .source_map_index import SourceMapIndex


class StepMode(Enum):
    """Stepping mode for debugger."""
    NONE = "none"      # Not stepping
    NEXT = "next"      # Step to next ML line (step over)
    STEP = "step"      # Step into functions
    OUT = "out"        # Step out of current function


@dataclass
class Breakpoint:
    """ML source breakpoint."""
    id: int
    ml_file: str
    ml_line: int
    py_lines: list[int]  # Corresponding Python line(s)
    enabled: bool = True
    condition: Optional[str] = None
    hit_count: int = 0


class MLDebugger:
    """Interactive debugger using sys.settrace()."""

    def __init__(self, ml_file: str, source_map_index: SourceMapIndex, py_code: str):
        """Initialize debugger.

        Args:
            ml_file: Path to ML source file
            source_map_index: Indexed source map for position lookups
            py_code: Compiled Python code to execute
        """
        self.ml_file = ml_file
        self.source_map_index = source_map_index
        self.py_code = py_code

        # Breakpoint management
        self.breakpoints: dict[int, Breakpoint] = {}
        self.next_bp_id = 1

        # Execution state
        self.step_mode = StepMode.NONE
        self.running = False
        self.current_frame = None
        self.current_ml_position: Optional[tuple[str, int, int]] = None

        # Pause callback (set by REPL)
        self.on_pause: Optional[Callable] = None

    def set_breakpoint(self, ml_file: str, ml_line: int) -> Optional[Breakpoint]:
        """Set breakpoint at ML source line.

        Args:
            ml_file: ML source file
            ml_line: ML line number (1-indexed)

        Returns:
            Breakpoint object, or None if line not executable
        """
        # Check if line is executable
        if not self.source_map_index.is_ml_line_executable(ml_file, ml_line):
            return None

        # Get first Python line for this ML line
        first_py_line = self.source_map_index.ml_line_to_first_py_line(ml_file, ml_line)

        bp = Breakpoint(
            id=self.next_bp_id,
            ml_file=ml_file,
            ml_line=ml_line,
            py_lines=[first_py_line]
        )

        self.breakpoints[self.next_bp_id] = bp
        self.next_bp_id += 1

        return bp

    def delete_breakpoint(self, bp_id: int) -> bool:
        """Delete breakpoint by ID."""
        return self.breakpoints.pop(bp_id, None) is not None

    def trace_function(self, frame, event, arg):
        """Trace callback - called by Python for every line.

        This is where the magic happens!
        """
        if event != 'line':
            return self.trace_function

        # Get Python position
        py_file = frame.f_code.co_filename
        py_line = frame.f_lineno

        # Skip if not our generated file
        if py_file != self.source_map_index.py_file:
            return self.trace_function

        # Map Python position → ML position
        ml_pos = self.source_map_index.py_line_to_ml(py_file, py_line)

        if ml_pos is None:
            # No ML mapping (generated code)
            return self.trace_function

        ml_file, ml_line, ml_col = ml_pos

        # Check if should break
        if self._should_break(ml_file, ml_line):
            self.current_frame = frame
            self.current_ml_position = ml_pos
            self._pause_execution()

        return self.trace_function

    def _should_break(self, ml_file: str, ml_line: int) -> bool:
        """Check if should break at this ML position."""

        # Check breakpoints
        for bp in self.breakpoints.values():
            if bp.enabled and bp.ml_file == ml_file and bp.ml_line == ml_line:
                # TODO: Evaluate condition if present
                bp.hit_count += 1
                return True

        # Check step mode
        if self.step_mode != StepMode.NONE:
            if self.current_ml_position:
                current_ml_line = self.current_ml_position[1]

                if self.step_mode == StepMode.NEXT:
                    # Break if on different ML line
                    if ml_line != current_ml_line:
                        self.step_mode = StepMode.NONE
                        return True

        return False

    def _pause_execution(self):
        """Pause execution and invoke callback (REPL)."""
        if self.on_pause:
            self.on_pause()

    def get_variable(self, name: str) -> Any:
        """Get variable value from current frame.

        This is why settrace() is awesome - live frame access!
        """
        if not self.current_frame:
            return None

        # Check locals
        if name in self.current_frame.f_locals:
            return self.current_frame.f_locals[name]

        # Check globals
        if name in self.current_frame.f_globals:
            return self.current_frame.f_globals[name]

        return None

    def show_source_context(self, lines_before: int = 2, lines_after: int = 2):
        """Display source code around current position."""
        if not self.current_ml_position:
            print("Not currently paused")
            return

        ml_file, ml_line, ml_col = self.current_ml_position

        # Read source file
        source_path = Path(ml_file)
        if not source_path.exists():
            print(f"Source file not found: {ml_file}")
            return

        lines = source_path.read_text().splitlines()

        # Calculate range
        start = max(0, ml_line - lines_before - 1)
        end = min(len(lines), ml_line + lines_after)

        # Display with line numbers
        print(f"\nAt {ml_file}:{ml_line}")
        for i in range(start, end):
            line_num = i + 1
            marker = "=> " if line_num == ml_line else "   "
            print(f"{marker}{line_num:4} | {lines[i]}")
        print()

    def start(self):
        """Start debugging (enable trace function)."""
        sys.settrace(self.trace_function)
        self.running = True

    def stop(self):
        """Stop debugging (disable trace function)."""
        sys.settrace(None)
        self.running = False

    def run(self):
        """Execute the ML program under debugger."""
        self.start()

        try:
            # Execute Python code
            exec(self.py_code, {'__name__': '__main__'})
        except Exception as e:
            print(f"Program terminated with exception: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.stop()
```

**Acceptance Criteria:**
- ✅ Can set/delete breakpoints
- ✅ Trace function maps Python → ML positions
- ✅ Execution pauses at breakpoints
- ✅ Can access variables via live frames

---

## Day 3: REPL Interface (4-6 hours)

### Task 3.1: Create Interactive REPL (3 hours)

**File:** `src/mlpy/debugging/repl.py`

```python
"""Interactive REPL for ML debugger."""

import cmd
import sys


class DebuggerREPL(cmd.Cmd):
    """Interactive debugging REPL."""

    intro = "ML Debugger v2.0 - Type 'help' for commands"
    prompt = "[mldb] "

    def __init__(self, debugger):
        super().__init__()
        self.debugger = debugger
        self.should_continue = False

    # === Execution Control ===

    def do_continue(self, arg):
        """Continue execution until next breakpoint.

        Usage: continue
        Aliases: c
        """
        self.debugger.step_mode = StepMode.NONE
        self.should_continue = True
        return True  # Exit cmdloop

    do_c = do_continue

    def do_next(self, arg):
        """Step to next ML line (step over function calls).

        Usage: next
        Aliases: n
        """
        self.debugger.step_mode = StepMode.NEXT
        self.should_continue = True
        return True

    do_n = do_next

    # === Breakpoints ===

    def do_break(self, arg):
        """Set breakpoint at ML source line.

        Usage:
            break <line>         - Set breakpoint at line in current file
            break <file>:<line>  - Set breakpoint at line in specific file

        Examples:
            break 42
            break example.ml:42
        """
        if not arg:
            print("Usage: break <line> or break <file>:<line>")
            return

        # Parse argument
        if ':' in arg:
            file_part, line_part = arg.rsplit(':', 1)
            ml_file = file_part
        else:
            ml_file = self.debugger.ml_file
            line_part = arg

        try:
            ml_line = int(line_part)
        except ValueError:
            print(f"Invalid line number: {line_part}")
            return

        # Set breakpoint
        bp = self.debugger.set_breakpoint(ml_file, ml_line)

        if bp:
            print(f"Breakpoint {bp.id} set at {ml_file}:{ml_line}")
        else:
            print(f"Cannot set breakpoint: line {ml_line} is not executable")

    do_b = do_break

    def do_delete(self, arg):
        """Delete breakpoint by ID.

        Usage: delete <id>
        """
        if not arg:
            print("Usage: delete <breakpoint_id>")
            return

        try:
            bp_id = int(arg)
        except ValueError:
            print(f"Invalid breakpoint ID: {arg}")
            return

        if self.debugger.delete_breakpoint(bp_id):
            print(f"Breakpoint {bp_id} deleted")
        else:
            print(f"No breakpoint with ID {bp_id}")

    # === Inspection ===

    def do_print(self, arg):
        """Print variable value.

        Usage: print <variable>
        Aliases: p
        """
        if not arg:
            print("Usage: print <variable>")
            return

        value = self.debugger.get_variable(arg)

        if value is None:
            print(f"{arg} = <undefined>")
        else:
            type_name = type(value).__name__
            print(f"{arg} = {value!r} ({type_name})")

    do_p = do_print

    def do_list(self, arg):
        """Show source code around current position.

        Usage: list
        Aliases: l
        """
        self.debugger.show_source_context()

    do_l = do_list

    def do_info(self, arg):
        """Show debugging information.

        Usage:
            info breakpoints  - List all breakpoints
            info locals       - List local variables
        """
        if not arg:
            print("Usage: info breakpoints|locals")
            return

        if arg.startswith('b'):  # breakpoints
            if not self.debugger.breakpoints:
                print("No breakpoints set")
            else:
                print("Breakpoints:")
                for bp in self.debugger.breakpoints.values():
                    status = "enabled" if bp.enabled else "disabled"
                    print(f"  {bp.id}: {bp.ml_file}:{bp.ml_line} "
                          f"({status}, hit {bp.hit_count} times)")

        elif arg.startswith('l'):  # locals
            if not self.debugger.current_frame:
                print("No current frame")
                return

            locals_dict = self.debugger.current_frame.f_locals
            if not locals_dict:
                print("No local variables")
            else:
                print("Local variables:")
                for name, value in locals_dict.items():
                    if not name.startswith('__'):
                        print(f"  {name} = {value!r}")

    # === Exit ===

    def do_quit(self, arg):
        """Exit debugger.

        Usage: quit
        Aliases: q
        """
        print("Exiting debugger")
        self.debugger.stop()
        sys.exit(0)

    do_q = do_quit

    def emptyline(self):
        """Don't repeat last command on empty line."""
        pass
```

### Task 3.2: CLI Integration (2 hours)

**File:** `src/mlpy/cli/commands.py` - Add DebugCommand

```python
class DebugCommand(BaseCommand):
    """Debug ML programs interactively."""

    def register_parser(self, subparsers):
        parser = subparsers.add_parser(
            'debug',
            help='Debug ML programs interactively',
            description='Launch interactive debugging session for ML programs'
        )
        parser.add_argument('source', help='ML source file to debug')
        parser.add_argument('args', nargs='*', help='Arguments to pass to program')

    def execute(self, args):
        from mlpy.debugging.debugger import MLDebugger
        from mlpy.debugging.source_map_index import SourceMapIndex
        from mlpy.debugging.repl import DebuggerREPL
        from mlpy.ml.transpiler import transpile

        # Transpile ML to Python
        print(f"Transpiling {args.source}...")

        result = transpile(args.source)

        if not result.success:
            print("Transpilation failed!")
            return 1

        # Build source map index
        source_index = SourceMapIndex.from_source_map(
            result.source_map,
            result.output_file
        )

        # Create debugger
        debugger = MLDebugger(
            args.source,
            source_index,
            result.python_code
        )

        # Set up REPL callback
        repl = DebuggerREPL(debugger)

        def on_pause():
            """Called when execution pauses."""
            debugger.show_source_context()
            repl.cmdloop()
            # After REPL exits, resume if should_continue
            if not repl.should_continue:
                debugger.stop()
                sys.exit(0)

        debugger.on_pause = on_pause

        # Show intro
        print(repl.intro)
        print("Set breakpoints with 'break <line>', then 'continue' to start\n")

        # Initial REPL (to set breakpoints before running)
        try:
            repl.cmdloop()
        except KeyboardInterrupt:
            print("\nExiting")
            return 0

        return 0
```

**Acceptance Criteria:**
- ✅ `mlpy debug example.ml` launches REPL
- ✅ Can set breakpoints, continue, step
- ✅ Can inspect variables
- ✅ Clean exit with quit command

---

## Testing Strategy

### Unit Tests

```
tests/unit/debugging/
├── test_source_map_index.py   - Index building and lookup
├── test_debugger.py            - Breakpoint logic
└── test_repl.py                - Command parsing
```

### Integration Tests

```python
# tests/integration/test_debugger_integration.py

def test_basic_debugging():
    """Test end-to-end debugging flow."""

    # Create simple ML program
    ml_code = """
    function add(a, b) {
        return a + b;
    }

    let result = add(5, 3);
    print(result);
    """

    # Transpile
    result = transpile_string(ml_code)

    # Build debugger
    index = SourceMapIndex.from_source_map(result.source_map, 'test.py')
    debugger = MLDebugger('test.ml', index, result.python_code)

    # Set breakpoint
    bp = debugger.set_breakpoint('test.ml', 2)  # return statement
    assert bp is not None

    # Run with trace
    # ... verify breakpoint hit
```

---

## Success Criteria for PoC

### Day 1 Complete When:
- ✅ SourceMapIndex class implemented
- ✅ Unit tests pass
- ✅ Can map ML↔Python positions

### Day 2 Complete When:
- ✅ MLDebugger class implemented
- ✅ sys.settrace() integration works
- ✅ Breakpoints pause execution
- ✅ Can access live variables

### Day 3 Complete When:
- ✅ REPL interface functional
- ✅ CLI integration complete
- ✅ Can run: `mlpy debug example.ml`
- ✅ Basic debugging workflow works:
  - Set breakpoint
  - Continue
  - Hit breakpoint
  - Print variable
  - Step next
  - Continue

---

## Demo Script

After 3 days, you should be able to do this:

```bash
$ cat fibonacci.ml
function fibonacci(n) {
    if (n <= 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

let result = fibonacci(5);
print(result);

$ mlpy debug fibonacci.ml
Transpiling fibonacci.ml...
ML Debugger v2.0 - Type 'help' for commands
Set breakpoints with 'break <line>', then 'continue' to start

[mldb] break 2
Breakpoint 1 set at fibonacci.ml:2

[mldb] continue

Breakpoint 1 hit at fibonacci.ml:2
   1 | function fibonacci(n) {
=> 2 |     if (n <= 1) {
   3 |         return n;
   4 |     }

[mldb] print n
n = 5 (int)

[mldb] next

   3 |         return n;
   4 |     }
=> 5 |     return fibonacci(n - 1) + fibonacci(n - 2);
   6 | }

[mldb] continue

5
Program completed

[mldb] quit
```

**That's a working debugger in 3 days!** 🎉

---

## Next Steps After PoC

1. **Validate approach** with real ML programs
2. **Get feedback** from team
3. **Decide:** Continue to Phase 2 (enhanced features) or adjust
4. **Document learnings** for future phases

---

## Risk Mitigation

### If Day 1 Takes Too Long
- Simplify SourceMapIndex (just ML→Py, skip Py→ML initially)
- Use existing source map directly (optimize later)

### If Day 2 Takes Too Long
- Skip condition evaluation for breakpoints
- Simplify stepping (just NEXT, skip STEP/OUT)

### If Day 3 Takes Too Long
- Use minimal REPL (just break, continue, print, quit)
- Skip info commands and fancy formatting

**Core PoC Goal:** Prove sys.settrace() works for ML debugging!
