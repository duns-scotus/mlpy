"""Core ML debugger using sys.settrace().

This module implements the main debugging functionality using Python's
built-in tracing mechanism, allowing line-by-line debugging of ML programs
without code instrumentation.
"""

import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Optional, Union

from .source_map_index import SourceMapIndex
from .safe_expression_eval import get_safe_evaluator
from .import_hook import MLDebuggerImportManager


class StepMode(Enum):
    """Stepping mode for debugger control flow."""

    NONE = "none"  # Not stepping (only break at breakpoints)
    NEXT = "next"  # Step to next ML line (step over function calls)
    STEP = "step"  # Step into functions
    OUT = "out"  # Step out of current function


@dataclass
class Breakpoint:
    """Represents an active breakpoint in ML source code.

    Attributes:
        id: Unique breakpoint identifier
        ml_file: ML source file path
        ml_line: ML line number (1-indexed)
        py_lines: Corresponding Python line numbers
        enabled: Whether the breakpoint is active
        condition: Optional ML expression to evaluate
        hit_count: Number of times breakpoint has been hit
    """

    id: int
    ml_file: str
    ml_line: int
    py_lines: list[int]
    enabled: bool = True
    condition: Optional[str] = None
    hit_count: int = 0


@dataclass
class PendingBreakpoint:
    """Represents a breakpoint waiting for module to load.

    This allows setting breakpoints in files that haven't been imported yet.
    When the module loads, the pending breakpoint is resolved to an active breakpoint.

    Attributes:
        id: Unique breakpoint identifier
        ml_file: ML source file path (may be relative or absolute)
        ml_line: ML line number (1-indexed)
        condition: Optional ML expression to evaluate
    """

    id: int
    ml_file: str
    ml_line: int
    condition: Optional[str] = None


# Global counter to verify trace function is called
_trace_call_count = 0

class MLDebugger:
    """Interactive debugger for ML programs using sys.settrace().

    This debugger provides line-by-line execution control without modifying
    the generated Python code. It uses source maps to translate between
    ML and Python positions.

    Example:
        >>> debugger = MLDebugger(ml_file, source_index, py_code)
        >>> bp = debugger.set_breakpoint("example.ml", 5)
        >>> debugger.on_pause = lambda: repl.cmdloop()
        >>> debugger.run()
    """

    def __init__(
        self, ml_file: str, source_map_index: SourceMapIndex, py_code: str, py_globals: Optional[dict] = None
    ):
        """Initialize debugger.

        Args:
            ml_file: Path to ML source file being debugged
            source_map_index: Indexed source map for position lookups
            py_code: Compiled Python code to execute
            py_globals: Optional global namespace for execution
        """
        self.ml_file = ml_file
        self.source_map_index = source_map_index
        self.py_code = py_code
        self.py_globals = py_globals or {}

        # Breakpoint management
        self.breakpoints: dict[int, Breakpoint] = {}  # Active breakpoints
        self.pending_breakpoints: dict[int, PendingBreakpoint] = {}  # Pending breakpoints
        self.next_bp_id = 1

        # Python lines with breakpoints (for fast lookup in trace)
        self._breakpoint_py_lines: set[int] = set()

        # Multi-file debugging support
        self.loaded_source_maps: dict[str, SourceMapIndex] = {}  # ml_file → source map index
        # Add main file with normalized path
        main_file_normalized = str(Path(ml_file).resolve())
        self.loaded_source_maps[main_file_normalized] = source_map_index

        # Watch expressions
        self.watches: dict[int, str] = {}  # watch_id → expression
        self.next_watch_id = 1

        # Execution state
        self.step_mode = StepMode.NONE
        self.running = False
        self.current_frame = None
        self.current_ml_position: Optional[tuple[str, int, int]] = None

        # Step tracking
        self._step_start_ml_line: Optional[int] = None
        self._step_start_depth: int = 0
        self._current_depth: int = 0

        # Exception breakpoints
        self.break_on_exceptions = False
        self.exception_filters: set[str] = set()  # Filter by exception type names
        self.last_exception: Optional[tuple[type, Any, Any]] = None  # (type, value, traceback)

        # Call stack navigation
        self.stack_frames: list = []  # Stack of frames
        self.current_frame_index: int = 0  # Index in stack (0 = current, 1 = caller, etc.)

        # Pause callback (set by REPL)
        self.on_pause: Optional[Callable] = None

        # Program execution finished flag
        self.finished = False

        # Automatic import detection for multi-file debugging
        self.import_manager = MLDebuggerImportManager(self)

        # Debug logging flag (set to True to enable detailed step debugging logs)
        self.debug_stepping = False

    def set_breakpoint(self, ml_file: str, ml_line: int, condition: Optional[str] = None) -> Optional[Union[Breakpoint, PendingBreakpoint]]:
        """Set breakpoint at ML source line (may be pending if file not loaded).

        This implements deferred breakpoint resolution - breakpoints can be set
        in files that haven't been imported yet. When the module loads, the
        pending breakpoint will be automatically activated.

        Args:
            ml_file: ML source file path
            ml_line: ML line number (1-indexed)
            condition: Optional conditional expression

        Returns:
            Breakpoint if immediately resolved, PendingBreakpoint if waiting for module load,
            or None if the line is invalid (not executable and can't be pending)
        """
        # Normalize file path (SourceMapIndex now stores normalized paths)
        ml_file_normalized = str(Path(ml_file).resolve())

        # Try to resolve immediately if source map is available
        source_index = self._get_source_index_for_file(ml_file_normalized)

        if source_index:
            # Source map is available for this file
            if source_index.is_ml_line_executable(ml_file_normalized, ml_line):
                # Line is executable - create active breakpoint
                first_py_line = source_index.ml_line_to_first_py_line(ml_file_normalized, ml_line)

                if first_py_line:
                    bp = Breakpoint(
                        id=self.next_bp_id,
                        ml_file=ml_file_normalized,
                        ml_line=ml_line,
                        py_lines=[first_py_line],
                        condition=condition,
                    )

                    self.breakpoints[self.next_bp_id] = bp
                    self.next_bp_id += 1

                    # Update fast lookup set
                    self._breakpoint_py_lines.add(first_py_line)

                    return bp  # Active breakpoint
            else:
                # Source map exists but line is not executable - invalid line
                return None
        else:
            # Source map not available - create pending breakpoint (file not loaded yet)
            pending_bp = PendingBreakpoint(
                id=self.next_bp_id, ml_file=ml_file_normalized, ml_line=ml_line, condition=condition
            )

            self.pending_breakpoints[self.next_bp_id] = pending_bp
            self.next_bp_id += 1

            return pending_bp  # Pending breakpoint

    def _get_source_index_for_file(self, ml_file: str) -> Optional[SourceMapIndex]:
        """Get source map index for a specific ML file.

        Args:
            ml_file: ML source file path

        Returns:
            SourceMapIndex if file is loaded, None otherwise
        """
        # Normalize path
        ml_file_normalized = str(Path(ml_file).resolve())

        # Check if it matches the main file
        main_file_normalized = str(Path(self.ml_file).resolve())
        if ml_file_normalized == main_file_normalized:
            return self.source_map_index

        # Check if we have this file in loaded maps
        if ml_file_normalized in self.loaded_source_maps:
            return self.loaded_source_maps[ml_file_normalized]

        # Also check non-normalized path (backward compatibility)
        if ml_file in self.loaded_source_maps:
            return self.loaded_source_maps[ml_file]

        return None

    def delete_breakpoint(self, bp_id: int) -> bool:
        """Delete breakpoint by ID (active or pending).

        Args:
            bp_id: Breakpoint identifier

        Returns:
            True if breakpoint was deleted, False if not found
        """
        # Try active breakpoints first
        bp = self.breakpoints.pop(bp_id, None)
        if bp:
            # Rebuild fast lookup set
            self._rebuild_breakpoint_index()
            return True

        # Try pending breakpoints
        pending_bp = self.pending_breakpoints.pop(bp_id, None)
        if pending_bp:
            return True

        return False

    def enable_breakpoint(self, bp_id: int) -> bool:
        """Enable a breakpoint."""
        if bp_id in self.breakpoints:
            self.breakpoints[bp_id].enabled = True
            self._rebuild_breakpoint_index()
            return True
        return False

    def disable_breakpoint(self, bp_id: int) -> bool:
        """Disable a breakpoint."""
        if bp_id in self.breakpoints:
            self.breakpoints[bp_id].enabled = False
            self._rebuild_breakpoint_index()
            return True
        return False

    def _rebuild_breakpoint_index(self):
        """Rebuild the fast lookup set of Python lines with breakpoints."""
        self._breakpoint_py_lines.clear()
        for bp in self.breakpoints.values():
            if bp.enabled:
                self._breakpoint_py_lines.update(bp.py_lines)

    # === Multi-File Debugging: Source Map Loading ===

    def load_source_map_for_file(self, ml_file: str) -> bool:
        """Load source map from .ml.map file for on-demand debugging.

        This implements lazy source map loading - files are only loaded
        when needed (e.g., when a breakpoint is set or module is imported).

        Args:
            ml_file: ML source file path

        Returns:
            True if source map loaded successfully, False otherwise
        """
        import json
        from mlpy.ml.codegen.enhanced_source_maps import EnhancedSourceMap

        # Normalize path
        ml_file_path = Path(ml_file).resolve()
        ml_file = str(ml_file_path)

        # Check if already loaded
        if ml_file in self.loaded_source_maps:
            return True

        # Look for .ml.map file
        map_file = ml_file_path.with_suffix('.ml.map')

        if not map_file.exists():
            # Try loading from transpiled .py location
            py_file = ml_file_path.with_suffix('.py')
            if py_file.exists():
                map_file = py_file.with_suffix('.ml.map')

        if not map_file.exists():
            return False

        try:
            # Load source map JSON
            source_map_data = json.loads(map_file.read_text(encoding='utf-8'))

            # Rebuild EnhancedSourceMap from JSON
            source_map = EnhancedSourceMap()

            if "debugInfo" in source_map_data and "detailedMappings" in source_map_data["debugInfo"]:
                mappings = source_map_data["debugInfo"]["detailedMappings"]
                for mapping_dict in mappings:
                    gen = mapping_dict.get("generated", {})
                    orig = mapping_dict.get("original", {})

                    if orig:
                        # Only add mappings that have original position info
                        source_file = mapping_dict.get("source_file", ml_file)
                        source_map.add_mapping(
                            generated_line=gen.get("line", 1),
                            generated_column=gen.get("column", 0),
                            original_line=orig.get("line"),
                            original_column=orig.get("column"),
                            source_file=source_file,
                            name=mapping_dict.get("name"),
                            node_type=mapping_dict.get("node_type")
                        )
            else:
                # No detailed mappings found
                pass

            # Create source map index
            py_file = ml_file_path.with_suffix('.py')
            source_index = SourceMapIndex.from_source_map(source_map, str(py_file))

            # Store in loaded maps
            self.loaded_source_maps[ml_file] = source_index

            # Try to activate pending breakpoints for this file
            self._activate_pending_breakpoints_for_file(ml_file)

            return True

        except Exception as e:
            print(f"Warning: Failed to load source map for {ml_file}: {e}")
            return False

    def _activate_pending_breakpoints_for_file(self, ml_file: str):
        """Activate pending breakpoints for a newly loaded file.

        Args:
            ml_file: ML file that was just loaded
        """
        ml_file = str(Path(ml_file).resolve())

        # Find pending breakpoints for this file
        to_activate = []
        for bp_id, pending_bp in self.pending_breakpoints.items():
            pending_file = str(Path(pending_bp.ml_file).resolve())
            if pending_file == ml_file:
                to_activate.append((bp_id, pending_bp))

        # Activate each pending breakpoint
        for bp_id, pending_bp in to_activate:
            source_index = self.loaded_source_maps.get(ml_file)
            if not source_index:
                continue

            # Check if line is executable
            if source_index.is_ml_line_executable(ml_file, pending_bp.ml_line):
                first_py_line = source_index.ml_line_to_first_py_line(ml_file, pending_bp.ml_line)
                if first_py_line:
                    # Create active breakpoint
                    bp = Breakpoint(
                        id=bp_id,
                        ml_file=ml_file,
                        ml_line=pending_bp.ml_line,
                        py_lines=[first_py_line],
                        condition=pending_bp.condition,
                    )

                    # Move from pending to active
                    del self.pending_breakpoints[bp_id]
                    self.breakpoints[bp_id] = bp

                    # Update fast lookup set
                    self._breakpoint_py_lines.add(first_py_line)

                    print(f"Breakpoint {bp_id} activated: {ml_file}:{pending_bp.ml_line}")

    def get_all_breakpoints(self) -> dict[int, tuple[str, int, str, Optional[str], bool]]:
        """Get all breakpoints (active and pending).

        Returns:
            Dictionary mapping bp_id → (ml_file, ml_line, status, condition, enabled)
            status is "active" or "pending"
        """
        result = {}

        # Add active breakpoints
        for bp_id, bp in self.breakpoints.items():
            result[bp_id] = (bp.ml_file, bp.ml_line, "active", bp.condition, bp.enabled)

        # Add pending breakpoints
        for bp_id, pending_bp in self.pending_breakpoints.items():
            result[bp_id] = (pending_bp.ml_file, pending_bp.ml_line, "pending", pending_bp.condition, True)

        return result

    # === Watch Expression Management ===

    def add_watch(self, expression: str) -> int:
        """Add a watch expression.

        Args:
            expression: Expression to watch (e.g., "x", "count * 2")

        Returns:
            Watch ID
        """
        watch_id = self.next_watch_id
        self.watches[watch_id] = expression
        self.next_watch_id += 1
        return watch_id

    def remove_watch(self, watch_id: int) -> bool:
        """Remove a watch expression.

        Args:
            watch_id: ID of watch to remove

        Returns:
            True if watch was removed, False if not found
        """
        if watch_id in self.watches:
            del self.watches[watch_id]
            return True
        return False

    def get_watch_values(self) -> dict[int, tuple[str, Any, bool]]:
        """Get current values of all watch expressions SECURELY.

        This uses the safe expression evaluator to prevent security violations.

        Returns:
            Dictionary mapping watch_id → (expression, value, success)
            success is False if evaluation failed
        """
        results = {}
        evaluator = get_safe_evaluator()

        for watch_id, expression in self.watches.items():
            if not self.current_frame:
                results[watch_id] = (expression, None, False)
                continue

            # Use safe evaluator
            value, success, error_msg = evaluator.evaluate(
                expression,
                self.current_frame.f_locals,
                self.current_frame.f_globals
            )

            if success:
                results[watch_id] = (expression, value, True)
            else:
                results[watch_id] = (expression, f"<Error: {error_msg}>", False)

        return results

    def trace_function(self, frame, event, arg):
        """Trace callback - called by Python for every line execution.

        This is the heart of the debugger! It maps Python execution back
        to ML source positions and decides when to pause.

        Args:
            frame: Current execution frame
            event: Event type ('line', 'call', 'return', etc.)
            arg: Event-specific argument

        Returns:
            The trace function to continue tracing
        """
        # Increment global counter (this MUST work)
        global _trace_call_count
        _trace_call_count += 1

        # Handle different events
        if event == "call":
            self._current_depth += 1
            # Update stack frames for navigation
            self.stack_frames.append(frame)
            return self.trace_function
        elif event == "return":
            self._current_depth -= 1
            # DEBUG: Log depth change for step out to file
            if self.debug_stepping and self.step_mode == StepMode.OUT:
                try:
                    import os
                    log_file = os.path.join(os.path.dirname(__file__), '..', '..', 'dap_debug.log')
                    with open(log_file, 'a', encoding='utf-8') as f:
                        f.write(f"[RETURN] Depth decreased to {self._current_depth}, step_start_depth={self._step_start_depth}, function={frame.f_code.co_name}\n")
                        f.flush()
                except:
                    pass
            # Pop from stack frames
            if self.stack_frames and self.stack_frames[-1] == frame:
                self.stack_frames.pop()
                # Reset frame index if we were looking at a frame that's returning
                if self.current_frame_index >= len(self.stack_frames):
                    self.current_frame_index = max(0, len(self.stack_frames) - 1)
            # For step out, we keep the OUT mode active so we break at the next line
            # in the caller's frame (handled in _should_break for 'line' events)
            return self.trace_function
        elif event == "exception":
            # Handle exception events
            if self.break_on_exceptions:
                exc_type, exc_value, exc_traceback = arg
                self.last_exception = (exc_type, exc_value, exc_traceback)

                # Check if we should break for this exception type
                if self._should_break_on_exception(exc_type):
                    self.current_frame = frame
                    # Try to map to ML position
                    py_file = frame.f_code.co_filename
                    py_line = frame.f_lineno
                    ml_pos = self.source_map_index.py_line_to_ml(py_file, py_line)
                    if ml_pos:
                        self.current_ml_position = ml_pos
                    self._pause_execution()
            return self.trace_function
        elif event != "line":
            return self.trace_function

        # Only process 'line' events from here on

        # Get Python position
        py_file = frame.f_code.co_filename
        py_line = frame.f_lineno

        # Try to find source map for this Python file (multi-file support)
        source_index = self._find_source_index_for_py_file(py_file)

        if source_index is None:
            # Not one of our generated files - skip
            return self.trace_function

        # Map Python position → ML position
        ml_pos = source_index.py_line_to_ml(py_file, py_line)

        if ml_pos is None:
            # No ML mapping (generated helper code, etc.)
            # SPECIAL CASE: For step OUT, even without ML mapping, check if we've returned
            # This handles lines that don't have ML mappings (like some return statements)
            if self.step_mode == StepMode.OUT and self._current_depth < self._step_start_depth:
                # We've stepped out of the function, but this line has no ML mapping
                # BREAK IMMEDIATELY - this is likely the return statement we want to stop at
                if self.debug_stepping:
                    try:
                        import os
                        log_file = os.path.join(os.path.dirname(__file__), '..', '..', 'dap_debug.log')
                        with open(log_file, 'a', encoding='utf-8') as f:
                            f.write(f"[STEP OUT BREAK] No ML mapping at py_line={py_line}, but stepped out, breaking here\n")
                            f.flush()
                    except:
                        pass

                self.step_mode = StepMode.NONE
                self.current_frame = frame
                # Create a synthetic ML position using the Python position
                # This allows the debugger to show SOME context even without perfect mapping
                self.current_ml_position = (py_file.replace('.py', '.ml'), py_line, 0)
                self._pause_execution()
            return self.trace_function

        ml_file, ml_line, ml_col = ml_pos

        # Check if should break at this position
        if self._should_break(ml_file, ml_line, py_line):
            self.current_frame = frame
            self.current_ml_position = ml_pos
            self._pause_execution()

        return self.trace_function

    def _find_source_index_for_py_file(self, py_file: str) -> Optional[SourceMapIndex]:
        """Find the source map index for a given Python file.

        Args:
            py_file: Python file path

        Returns:
            SourceMapIndex if found, None otherwise
        """
        # Check main source map
        if py_file == self.source_map_index.py_file:
            return self.source_map_index

        # Check all loaded source maps
        for source_index in self.loaded_source_maps.values():
            if source_index.py_file == py_file:
                return source_index

        return None

    def _should_break(self, ml_file: str, ml_line: int, py_line: int) -> bool:
        """Check if execution should break at this ML position.

        Args:
            ml_file: ML source file
            ml_line: ML line number
            py_line: Python line number (for fast breakpoint check)

        Returns:
            True if should pause execution
        """
        # Normalize file path for comparison with stored breakpoints
        ml_file_normalized = str(Path(ml_file).resolve())

        # Fast path: check if there's any reason to break
        if self.step_mode == StepMode.NONE and py_line not in self._breakpoint_py_lines:
            return False

        # Check breakpoints
        if py_line in self._breakpoint_py_lines:
            for bp in self.breakpoints.values():
                if bp.enabled and bp.ml_file == ml_file_normalized and bp.ml_line == ml_line:
                    # Evaluate condition if present
                    if bp.condition:
                        if not self._evaluate_condition(bp.condition):
                            continue  # Condition not met, don't break
                    bp.hit_count += 1
                    return True

        # Check step mode
        if self.step_mode == StepMode.NEXT:
            # Step over: break if on different ML line AND at same or shallower depth
            # This prevents stepping INTO function calls (which would increase depth)
            if self._step_start_ml_line is not None and ml_line != self._step_start_ml_line:
                # Only break if we're at the same depth or shallower (not deeper)
                if self._current_depth <= self._step_start_depth:
                    self.step_mode = StepMode.NONE
                    return True

        elif self.step_mode == StepMode.STEP:
            # Step into: break at any new ML line
            # If _step_start_ml_line is None, break at ANY ML line (used after step out with no ML mapping)
            if self._step_start_ml_line is None or ml_line != self._step_start_ml_line:
                self.step_mode = StepMode.NONE
                return True

        elif self.step_mode == StepMode.OUT:
            # Step out: after returning from function (handled in 'return' event),
            # break at the next line we encounter
            # DEBUG: Log depth check to file
            if self.debug_stepping:
                try:
                    import os
                    log_file = os.path.join(os.path.dirname(__file__), '..', '..', 'dap_debug.log')
                    with open(log_file, 'a', encoding='utf-8') as f:
                        f.write(f"[STEP OUT] Checking: current_depth={self._current_depth}, start_depth={self._step_start_depth}, ml_line={ml_line}, should_break={self._current_depth < self._step_start_depth}\n")
                        f.flush()
                except:
                    pass

            if self._current_depth < self._step_start_depth:
                # We've returned from the function, break at this line
                if self.debug_stepping:
                    try:
                        import os
                        log_file = os.path.join(os.path.dirname(__file__), '..', '..', 'dap_debug.log')
                        with open(log_file, 'a', encoding='utf-8') as f:
                            f.write(f"[STEP OUT] BREAKING at ML line {ml_line}\n")
                            f.flush()
                    except:
                        pass
                self.step_mode = StepMode.NONE
                return True

        return False

    def _pause_execution(self):
        """Pause execution and invoke callback (typically REPL)."""
        if self.on_pause:
            self.on_pause()

    def _evaluate_condition(self, condition: str) -> bool:
        """Evaluate a breakpoint condition expression SECURELY.

        This uses the safe expression evaluator which:
        - Parses condition as ML expression
        - Runs security analysis
        - Evaluates in restricted namespace
        - Prevents sandbox escape

        Args:
            condition: ML expression to evaluate (e.g., "x > 10")

        Returns:
            True if condition evaluates to truthy value, False otherwise
        """
        if not self.current_frame:
            return False

        # Use safe evaluator to prevent security violations
        evaluator = get_safe_evaluator()
        value, success, error_msg = evaluator.evaluate(
            condition,
            self.current_frame.f_locals,
            self.current_frame.f_globals
        )

        if not success:
            # Security violation or evaluation error
            print(f"Warning: Condition evaluation failed: {error_msg}")
            return False

        return bool(value)

    def get_variable(self, name: str) -> Any:
        """Get variable value from current stack frame.

        This respects stack navigation - if you've navigated up the stack,
        it will return variables from that frame.

        Args:
            name: Variable name

        Returns:
            Variable value, or None if not found
        """
        frame = self.get_current_stack_frame()
        if not frame:
            return None

        # Check locals first
        if name in frame.f_locals:
            return frame.f_locals[name]

        # Check globals
        if name in frame.f_globals:
            return frame.f_globals[name]

        return None

    def get_all_locals(self) -> dict[str, Any]:
        """Get all local variables from current stack frame."""
        frame = self.get_current_stack_frame()
        if not frame:
            return {}

        # Filter out internal variables
        return {
            k: v
            for k, v in frame.f_locals.items()
            if not k.startswith("__") and not k.startswith("_ml_")
        }

    def get_all_globals(self) -> dict[str, Any]:
        """Get all global variables from current stack frame."""
        frame = self.get_current_stack_frame()
        if not frame:
            return {}

        # Filter out builtins and internal variables
        return {
            k: v
            for k, v in frame.f_globals.items()
            if not k.startswith("__")
            and not k.startswith("_ml_")
            and k not in ["print", "len", "range", "str", "int", "float", "bool"]
        }

    def show_source_context(self, lines_before: int = 2, lines_after: int = 2) -> str:
        """Display source code around current position.

        Args:
            lines_before: Number of lines to show before current
            lines_after: Number of lines to show after current

        Returns:
            Formatted source context string
        """
        if not self.current_ml_position:
            return "Not currently paused"

        ml_file, ml_line, ml_col = self.current_ml_position

        # Read source file
        source_path = Path(ml_file)
        if not source_path.exists():
            return f"Source file not found: {ml_file}"

        try:
            lines = source_path.read_text(encoding="utf-8").splitlines()
        except Exception as e:
            return f"Error reading source file: {e}"

        # Calculate range
        start = max(0, ml_line - lines_before - 1)
        end = min(len(lines), ml_line + lines_after)

        # Build output
        output = [f"\nAt {ml_file}:{ml_line}"]

        for i in range(start, end):
            line_num = i + 1
            marker = "=> " if line_num == ml_line else "   "
            output.append(f"{marker}{line_num:4} | {lines[i]}")

        output.append("")
        return "\n".join(output)

    def step_next(self):
        """Step to next ML line (step over function calls)."""
        if self.current_ml_position:
            self.step_mode = StepMode.NEXT
            self._step_start_ml_line = self.current_ml_position[1]
            self._step_start_depth = self._current_depth

    def step_into(self):
        """Step into function calls."""
        if self.current_ml_position:
            self.step_mode = StepMode.STEP
            self._step_start_ml_line = self.current_ml_position[1]

    def step_out(self):
        """Step out of current function."""
        self.step_mode = StepMode.OUT
        self._step_start_depth = self._current_depth
        # DEBUG: Log step out initiation to file
        if self.debug_stepping:
            try:
                import os
                log_file = os.path.join(os.path.dirname(__file__), '..', '..', 'dap_debug.log')
                with open(log_file, 'a', encoding='utf-8') as f:
                    f.write(f"[STEP OUT] Initiated at depth {self._current_depth}\n")
                    f.flush()
            except:
                pass

    def continue_execution(self):
        """Continue execution until next breakpoint."""
        self.step_mode = StepMode.NONE

    def start(self):
        """Start debugging (enable trace function and import monitoring).

        This activates:
        - sys.settrace() for line-by-line tracing (~10-15% overhead)
        - Import hook for automatic source map loading (minimal overhead)
        """
        sys.settrace(self.trace_function)
        self.import_manager.start()  # Start monitoring imports
        self.running = True

    def stop(self):
        """Stop debugging (disable trace function and import monitoring).

        This removes all overhead - program returns to full speed.
        """
        sys.settrace(None)
        self.import_manager.stop()  # Stop monitoring imports
        self.running = False

    def run(self):
        """Execute the ML program under debugger.

        This compiles and executes the Python code with tracing enabled.
        """
        self.start()

        try:
            # Compile the Python code
            compiled_code = compile(self.py_code, self.source_map_index.py_file, "exec")

            # Setup globals with __name__ = '__main__'
            exec_globals = {"__name__": "__main__"}
            exec_globals.update(self.py_globals)

            # Execute
            exec(compiled_code, exec_globals)

            self.finished = True

        except Exception as e:
            # Program terminated with exception
            print(f"\nProgram terminated with exception: {e}")
            import traceback

            traceback.print_exc()
            self.finished = True

        finally:
            self.stop()

    def get_call_stack(self) -> list[tuple[str, int, str]]:
        """Get call stack with ML source positions.

        Returns:
            List of (ml_file, ml_line, function_name) tuples
        """
        if not self.current_frame:
            return []

        stack = []
        frame = self.current_frame

        while frame is not None:
            py_file = frame.f_code.co_filename
            py_line = frame.f_lineno
            func_name = frame.f_code.co_name

            # Try to map to ML position
            ml_pos = self.source_map_index.py_line_to_ml(py_file, py_line)

            if ml_pos:
                ml_file, ml_line, _ = ml_pos
                stack.append((ml_file, ml_line, func_name))

            frame = frame.f_back

        return stack

    # === Exception Breakpoints ===

    def enable_exception_breakpoints(self, exception_type: Optional[str] = None):
        """Enable breaking on exceptions.

        Args:
            exception_type: Optional exception type name to filter (e.g., "ValueError")
                           If None, breaks on all exceptions
        """
        self.break_on_exceptions = True
        if exception_type:
            self.exception_filters.add(exception_type)

    def disable_exception_breakpoints(self):
        """Disable breaking on exceptions."""
        self.break_on_exceptions = False
        self.exception_filters.clear()

    def add_exception_filter(self, exception_type: str):
        """Add an exception type to the filter list.

        Args:
            exception_type: Exception type name (e.g., "ValueError", "KeyError")
        """
        self.exception_filters.add(exception_type)

    def remove_exception_filter(self, exception_type: str):
        """Remove an exception type from the filter list.

        Args:
            exception_type: Exception type name to remove
        """
        self.exception_filters.discard(exception_type)

    def _should_break_on_exception(self, exc_type: type) -> bool:
        """Check if we should break for this exception type.

        Args:
            exc_type: Exception type that was raised

        Returns:
            True if we should pause execution for this exception
        """
        # If no filters, break on all exceptions
        if not self.exception_filters:
            return True

        # Check if exception type matches any filter
        exc_name = exc_type.__name__
        return exc_name in self.exception_filters

    def get_exception_info(self) -> Optional[dict]:
        """Get information about the last exception.

        Returns:
            Dictionary with exception info, or None if no exception
        """
        if not self.last_exception:
            return None

        exc_type, exc_value, exc_traceback = self.last_exception
        return {
            "type": exc_type.__name__,
            "value": str(exc_value),
            "message": str(exc_value),
        }

    # === Call Stack Navigation ===

    def get_frame_at_index(self, index: int):
        """Get frame at a specific stack index.

        Args:
            index: Stack index (0 = current, 1 = caller, etc.)

        Returns:
            Frame object or None if index out of range
        """
        # Build stack from current frame
        if not self.current_frame:
            return None

        stack = []
        frame = self.current_frame
        while frame is not None:
            stack.append(frame)
            frame = frame.f_back

        # Return frame at index (reversed so 0 is current)
        if 0 <= index < len(stack):
            return stack[index]
        return None

    def navigate_up_stack(self) -> bool:
        """Navigate up one level in the call stack (towards caller).

        Returns:
            True if navigation successful, False if already at top
        """
        new_index = self.current_frame_index + 1
        frame = self.get_frame_at_index(new_index)
        if frame:
            self.current_frame_index = new_index
            return True
        return False

    def navigate_down_stack(self) -> bool:
        """Navigate down one level in the call stack (towards current).

        Returns:
            True if navigation successful, False if already at bottom
        """
        if self.current_frame_index > 0:
            self.current_frame_index -= 1
            return True
        return False

    def reset_stack_navigation(self):
        """Reset stack navigation to current frame."""
        self.current_frame_index = 0

    def get_current_stack_frame(self):
        """Get the frame at the current navigation position.

        Returns:
            Frame object at current stack position
        """
        return self.get_frame_at_index(self.current_frame_index)

    def get_stack_depth(self) -> int:
        """Get the depth of the current call stack.

        Returns:
            Number of frames in the stack
        """
        if not self.current_frame:
            return 0

        depth = 0
        frame = self.current_frame
        while frame is not None:
            depth += 1
            frame = frame.f_back
        return depth

    # === DAP Support Methods ===

    def get_call_stack_with_frames(self) -> list[dict[str, Any]]:
        """Get call stack with frames and ML positions for DAP protocol.

        This enhanced version returns complete frame information needed
        by the Debug Adapter Protocol, including frame objects for
        variable inspection.

        Returns:
            List of dictionaries with:
                - frame: Python frame object
                - ml_position: (ml_file, ml_line, ml_col) tuple
                - function_name: Function name
        """
        if not self.current_frame:
            return []

        stack = []
        frame = self.current_frame

        while frame is not None:
            py_file = frame.f_code.co_filename
            py_line = frame.f_lineno
            func_name = frame.f_code.co_name

            # Try to map to ML position using all loaded source maps
            ml_pos = None

            # First try current source map
            if self.source_map_index:
                ml_pos = self.source_map_index.py_line_to_ml(py_file, py_line)

            # If not found, try other loaded source maps (multi-file debugging)
            if not ml_pos:
                for source_index in self.loaded_source_maps.values():
                    ml_pos = source_index.py_line_to_ml(py_file, py_line)
                    if ml_pos:
                        break

            if ml_pos:
                ml_file, ml_line, ml_col = ml_pos
                stack.append({
                    'frame': frame,
                    'ml_position': (ml_file, ml_line, ml_col),
                    'function_name': func_name
                })

            frame = frame.f_back

        return stack

    def get_locals(self, frame_id: int = 0) -> dict[str, Any]:
        """Get local variables for specific stack frame.

        Args:
            frame_id: Stack frame index (0 = current, 1 = caller, etc.)

        Returns:
            Dictionary of local variable names to values
        """
        stack = self.get_call_stack_with_frames()

        if frame_id < len(stack):
            frame = stack[frame_id]['frame']
            return frame.f_locals.copy()

        return {}

    def get_globals(self, frame_id: int = 0) -> dict[str, Any]:
        """Get global variables for specific stack frame.

        Args:
            frame_id: Stack frame index (0 = current, 1 = caller, etc.)

        Returns:
            Dictionary of global variable names to values
        """
        stack = self.get_call_stack_with_frames()

        if frame_id < len(stack):
            frame = stack[frame_id]['frame']
            return frame.f_globals.copy()

        return {}

    def evaluate_expression(self, expression: str, frame_id: int = 0) -> Any:
        """Evaluate ML expression in context of stack frame.

        Uses SafeExpressionEvaluator to ensure security while evaluating
        expressions in the debug context.

        Args:
            expression: ML expression to evaluate
            frame_id: Stack frame index (0 = current, 1 = caller, etc.)

        Returns:
            Result of expression evaluation

        Raises:
            ValueError: If frame_id is invalid
            Exception: If expression evaluation fails
        """
        stack = self.get_call_stack_with_frames()

        if frame_id >= len(stack):
            raise ValueError(f'Invalid frame ID: {frame_id}')

        frame = stack[frame_id]['frame']

        # Use SafeExpressionEvaluator for secure evaluation
        evaluator = get_safe_evaluator(frame.f_locals, frame.f_globals)
        return evaluator.evaluate(expression)

    def remove_breakpoint(self, bp_id: int) -> bool:
        """Remove breakpoint by ID (alias for delete_breakpoint for DAP compatibility).

        Args:
            bp_id: Breakpoint identifier

        Returns:
            True if breakpoint was removed, False if not found
        """
        return self.delete_breakpoint(bp_id)

    def set_on_break_callback(self, callback: Optional[Callable]):
        """Set callback to be called when debugger hits a breakpoint.

        The callback is invoked when the debugger pauses execution at a breakpoint,
        allowing external systems (like DAP server) to be notified.

        Args:
            callback: Function to call when breakpoint is hit (no arguments)
        """
        self.on_pause = callback
