"""
Debug Test Handler for automated debugging feature testing.

This module provides a comprehensive testing infrastructure for the ML debugger,
allowing automated testing of breakpoints, stepping, variable inspection, and
source map functionality.

Usage:
    handler = DebugTestHandler()
    handler.load_program("tests/ml_integration/ml_debug/main.ml")
    handler.set_breakpoint("main.ml", 10)
    handler.run()
    handler.step_over()
    vars = handler.get_variables()
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass


@dataclass
class BreakpointInfo:
    """Information about a breakpoint."""
    file: str
    line: int
    condition: Optional[str] = None
    enabled: bool = True
    hit_count: int = 0


@dataclass
class DebugState:
    """Current state of the debugger."""
    stopped: bool = False
    current_file: Optional[str] = None
    current_line: Optional[int] = None
    call_stack: List[Dict[str, Any]] = None
    variables: Dict[str, Any] = None
    reason: Optional[str] = None  # 'breakpoint', 'step', 'exception'

    def __post_init__(self):
        if self.call_stack is None:
            self.call_stack = []
        if self.variables is None:
            self.variables = {}


class DebugTestHandler:
    """
    Handler for automated debugging tests.

    This class provides a REPL-style interface for testing debugger features
    programmatically, enabling comprehensive unit tests for all debugging
    functionality.
    """

    def __init__(self):
        """Initialize the debug test handler."""
        from mlpy.debugging.debugger import MLDebugger
        from mlpy.debugging.source_map_index import SourceMapIndex
        from mlpy.ml.transpiler import transpile_ml_file

        self.MLDebugger = MLDebugger
        self.SourceMapIndex = SourceMapIndex
        self.transpile_ml_file = transpile_ml_file

        self.debugger: Optional[MLDebugger] = None
        self.source_map_index: Optional[SourceMapIndex] = None
        self.ml_file: Optional[str] = None
        self.py_file: Optional[str] = None
        self.py_code: Optional[str] = None
        self.breakpoints: Dict[int, BreakpointInfo] = {}
        self.state = DebugState()
        self.exec_globals: Dict[str, Any] = {}

        # Execution control
        self.running = False
        self.continue_requested = False

    def load_program(self, ml_file: str, force_retranspile: bool = False) -> Tuple[bool, str]:
        """
        Load and transpile an ML program for debugging.

        Args:
            ml_file: Path to ML source file
            force_retranspile: If True, delete cached files and force fresh transpilation

        Returns:
            Tuple of (success, message)
        """
        self.ml_file = os.path.abspath(ml_file)

        if not os.path.exists(self.ml_file):
            return False, f"File not found: {ml_file}"

        # Delete cached files if requested
        if force_retranspile:
            ml_path = Path(self.ml_file)
            cached_py = ml_path.with_suffix('.py')
            cached_map = ml_path.with_suffix('.py.map')

            if cached_py.exists():
                cached_py.unlink()
            if cached_map.exists():
                cached_map.unlink()

        try:
            # Transpile ML file
            py_code, issues, source_map = self.transpile_ml_file(
                self.ml_file,
                output_path=None,
                strict_security=False,
                generate_source_maps=True
            )

            if not py_code:
                error_msgs = [issue.error.message for issue in issues] if issues else ['Unknown error']
                return False, f"Transpilation failed: {'; '.join(error_msgs)}"

            # Store transpiled code
            self.py_file = os.path.splitext(self.ml_file)[0] + '.py'
            self.py_code = py_code

            # Build source map index
            if isinstance(source_map, dict):
                # Reconstruct from dict format
                from mlpy.ml.codegen.enhanced_source_maps import (
                    EnhancedSourceMap, SourceMapping, SourceLocation
                )

                enhanced_map = EnhancedSourceMap()

                if 'sourceMap' in source_map:
                    enhanced_map.sources = source_map['sourceMap'].get('sources', [])

                if 'debugInfo' in source_map and 'detailedMappings' in source_map['debugInfo']:
                    for mapping_dict in source_map['debugInfo']['detailedMappings']:
                        gen = mapping_dict.get('generated', {})
                        orig = mapping_dict.get('original')

                        generated_loc = SourceLocation(
                            line=gen.get('line', 0),
                            column=gen.get('column', 0)
                        )

                        original_loc = None
                        if orig:
                            original_loc = SourceLocation(
                                line=orig.get('line', 0),
                                column=orig.get('column', 0)
                            )

                        mapping = SourceMapping(
                            generated=generated_loc,
                            original=original_loc,
                            source_file=mapping_dict.get('source_file')
                        )
                        enhanced_map.mappings.append(mapping)

                source_map = enhanced_map

            self.source_map_index = self.SourceMapIndex.from_source_map(
                source_map,
                self.py_file
            )

            # Create debugger instance
            self.debugger = self.MLDebugger(
                ml_file=self.ml_file,
                source_map_index=self.source_map_index,
                py_code=py_code,
                py_globals={}
            )

            # Set callback for breakpoint hits
            self.debugger.set_on_break_callback(self._on_break)

            return True, f"Loaded: {ml_file}"

        except Exception as e:
            return False, f"Error loading program: {str(e)}"

    def set_breakpoint(self, file: str, line: int, condition: Optional[str] = None) -> Tuple[int, bool]:
        """
        Set a breakpoint at the specified location.

        Args:
            file: ML source file (can be basename or full path)
            line: Line number in ML source
            condition: Optional condition expression

        Returns:
            Tuple of (breakpoint_id, is_pending)
        """
        if not self.debugger:
            return -1, False

        # Resolve file path
        if not os.path.isabs(file):
            # Try to find file relative to current ML file
            if self.ml_file:
                base_dir = os.path.dirname(self.ml_file)
                full_path = os.path.join(base_dir, file)
                if os.path.exists(full_path):
                    file = full_path
                elif os.path.basename(self.ml_file) == file:
                    file = self.ml_file

        result = self.debugger.set_breakpoint(file, line, condition=condition)

        if result:
            bp_id, is_pending = result
            bp_info = BreakpointInfo(file=file, line=line, condition=condition)
            self.breakpoints[bp_id] = bp_info
            return bp_id, is_pending
        else:
            return -1, False

    def remove_breakpoint(self, breakpoint_id: int) -> Tuple[bool, str]:
        """
        Remove a breakpoint.

        Args:
            breakpoint_id: ID of breakpoint to remove

        Returns:
            Tuple of (success, message)
        """
        if not self.debugger or breakpoint_id not in self.breakpoints:
            return False, f"Breakpoint {breakpoint_id} not found"

        if hasattr(self.debugger, 'remove_breakpoint'):
            self.debugger.remove_breakpoint(breakpoint_id)

        del self.breakpoints[breakpoint_id]
        return True, f"Breakpoint {breakpoint_id} removed"

    def run(self) -> Tuple[bool, str]:
        """
        Start program execution.

        Returns:
            Tuple of (success, message)
        """
        if not self.debugger or not self.py_code:
            return False, "No program loaded"

        try:
            self.running = True
            self.debugger.start()

            # Set trace for current thread
            sys.settrace(self.debugger.trace_function)

            # Create execution namespace
            self.exec_globals = {
                '__name__': '__main__',
                '__file__': self.py_file
            }

            # Execute program
            exec(compile(self.py_code, self.py_file, 'exec'), self.exec_globals)

            self.running = False
            return True, "Program completed"

        except Exception as e:
            self.running = False
            self.state.stopped = True
            self.state.reason = 'exception'
            return False, f"Execution error: {str(e)}"

    def continue_execution(self) -> Tuple[bool, str]:
        """
        Continue execution after hitting a breakpoint.

        Returns:
            Tuple of (success, message)
        """
        if not self.debugger:
            return False, "No program loaded"

        self.state.stopped = False
        self.debugger.continue_execution()
        return True, "Continuing execution"

    def step_over(self) -> Tuple[bool, str]:
        """
        Step over (execute current line, don't enter functions).

        Returns:
            Tuple of (success, message)
        """
        if not self.debugger:
            return False, "No program loaded"

        self.state.stopped = False
        self.debugger.step_next()
        return True, "Stepping over"

    def step_into(self) -> Tuple[bool, str]:
        """
        Step into (enter function calls).

        Returns:
            Tuple of (success, message)
        """
        if not self.debugger:
            return False, "No program loaded"

        self.state.stopped = False
        self.debugger.step_into()
        return True, "Stepping into"

    def step_out(self) -> Tuple[bool, str]:
        """
        Step out (return from current function).

        Returns:
            Tuple of (success, message)
        """
        if not self.debugger:
            return False, "No program loaded"

        self.state.stopped = False
        self.debugger.step_out()
        return True, "Stepping out"

    def get_call_stack(self) -> List[Dict[str, Any]]:
        """
        Get current call stack.

        Returns:
            List of stack frames with file, line, and function info
        """
        if not self.debugger:
            return []

        return self.debugger.get_call_stack_with_frames()

    def get_variables(self, frame_index: int = 0) -> Dict[str, Any]:
        """
        Get variables in specified stack frame.

        Args:
            frame_index: Index of stack frame (0 = current frame)

        Returns:
            Dictionary of variable names to values
        """
        if not self.debugger:
            return {}

        try:
            locals_dict = self.debugger.get_locals(frame_index)
            return locals_dict
        except Exception:
            return {}

    def evaluate_expression(self, expression: str, frame_index: int = 0) -> Tuple[bool, Any]:
        """
        Evaluate an expression in the context of a stack frame.

        Args:
            expression: Expression to evaluate
            frame_index: Stack frame index

        Returns:
            Tuple of (success, result or error message)
        """
        if not self.debugger:
            return False, "No program loaded"

        try:
            result = self.debugger.evaluate_expression(expression, frame_index)
            return True, result
        except Exception as e:
            return False, str(e)

    def get_state(self) -> DebugState:
        """Get current debugger state."""
        if self.debugger and self.debugger.current_frame:
            # Update state from debugger
            if self.debugger.current_ml_position:
                self.state.current_file = self.debugger.current_ml_position[0]
                self.state.current_line = self.debugger.current_ml_position[1]

            self.state.call_stack = self.get_call_stack()
            self.state.variables = self.get_variables()

        return self.state

    def verify_source_maps_exist(self) -> Tuple[bool, Dict[str, bool]]:
        """
        Verify that source maps are generated and cached.

        Returns:
            Tuple of (all exist, detailed status dict)
        """
        if not self.ml_file:
            return False, {}

        ml_path = Path(self.ml_file)
        py_path = ml_path.with_suffix('.py')
        map_path = ml_path.with_suffix('.py.map')

        status = {
            'ml_file': ml_path.exists(),
            'py_file': py_path.exists(),
            'map_file': map_path.exists(),
            'source_map_index': self.source_map_index is not None
        }

        return all(status.values()), status

    def _on_break(self):
        """Callback when debugger hits a breakpoint."""
        self.state.stopped = True
        self.state.reason = 'breakpoint'

        # Update state
        if self.debugger.current_ml_position:
            self.state.current_file = self.debugger.current_ml_position[0]
            self.state.current_line = self.debugger.current_ml_position[1]

    def reset(self):
        """Reset handler state for new test."""
        self.debugger = None
        self.source_map_index = None
        self.ml_file = None
        self.py_file = None
        self.py_code = None
        self.breakpoints.clear()
        self.state = DebugState()
        self.exec_globals.clear()
        self.running = False

    # === Watch Expression Methods ===

    def add_watch(self, expression: str) -> int:
        """Add a watch expression."""
        if not self.debugger:
            return -1
        return self.debugger.add_watch(expression)

    def remove_watch(self, watch_id: int) -> bool:
        """Remove a watch expression."""
        if not self.debugger:
            return False
        return self.debugger.remove_watch(watch_id)

    def get_watch_values(self) -> Dict[int, Tuple[str, Any, bool]]:
        """Get current values of all watch expressions."""
        if not self.debugger:
            return {}
        return self.debugger.get_watch_values()

    # === Stack Navigation Methods ===

    def navigate_up_stack(self) -> bool:
        """Navigate up one level in the call stack."""
        if not self.debugger:
            return False
        return self.debugger.navigate_up_stack()

    def navigate_down_stack(self) -> bool:
        """Navigate down one level in the call stack."""
        if not self.debugger:
            return False
        return self.debugger.navigate_down_stack()

    def reset_stack_navigation(self):
        """Reset stack navigation to current frame."""
        if self.debugger:
            self.debugger.reset_stack_navigation()

    def get_stack_depth(self) -> int:
        """Get the depth of the current call stack."""
        if not self.debugger:
            return 0
        return self.debugger.get_stack_depth()

    def get_frame_at_index(self, index: int):
        """Get frame at a specific stack index."""
        if not self.debugger:
            return None
        return self.debugger.get_frame_at_index(index)

    # === Exception Breakpoint Methods ===

    def enable_exception_breakpoints(self, exception_type: Optional[str] = None):
        """Enable breaking on exceptions."""
        if self.debugger:
            self.debugger.enable_exception_breakpoints(exception_type)

    def disable_exception_breakpoints(self):
        """Disable breaking on exceptions."""
        if self.debugger:
            self.debugger.disable_exception_breakpoints()

    def add_exception_filter(self, exception_type: str):
        """Add an exception type to the filter list."""
        if self.debugger:
            self.debugger.add_exception_filter(exception_type)

    def remove_exception_filter(self, exception_type: str):
        """Remove an exception type from the filter list."""
        if self.debugger:
            self.debugger.remove_exception_filter(exception_type)

    def get_exception_info(self) -> Optional[Dict]:
        """Get information about the last exception."""
        if not self.debugger:
            return None
        return self.debugger.get_exception_info()

    # === Source Context Method ===

    def show_source_context(self, lines_before: int = 2, lines_after: int = 2) -> str:
        """Display source code around current position."""
        if not self.debugger:
            return "No program loaded"
        return self.debugger.show_source_context(lines_before, lines_after)

    # === Multi-File Methods ===

    def load_source_map_for_file(self, ml_file: str) -> bool:
        """Load source map for additional file."""
        if not self.debugger:
            return False
        return self.debugger.load_source_map_for_file(ml_file)

    def get_all_breakpoints(self) -> Dict[int, Tuple[str, int, str, Optional[str], bool]]:
        """Get all breakpoints (active and pending)."""
        if not self.debugger:
            return {}
        return self.debugger.get_all_breakpoints()

    def get_all_locals(self) -> Dict[str, Any]:
        """Get all local variables from current stack frame."""
        if not self.debugger:
            return {}
        return self.debugger.get_all_locals()

    def get_all_globals(self) -> Dict[str, Any]:
        """Get all global variables from current stack frame."""
        if not self.debugger:
            return {}
        return self.debugger.get_all_globals()
