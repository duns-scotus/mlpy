"""
Debug Adapter Protocol (DAP) server for ML language.

This module implements a DAP server that wraps the MLDebugger to provide
native debugging support in VS Code and other DAP-compatible IDEs.

Architecture:
    VS Code (Debug UI)
        ↕ DAP Protocol (JSON-RPC over stdin/stdout)
    DAP Server (this module)
        ↕ Python API
    MLDebugger (existing debugger implementation)
        ↕ sys.settrace()
    Generated Python Code

Usage:
    python -m mlpy.debugging.dap_server

References:
    - DAP Specification: https://microsoft.github.io/debug-adapter-protocol/
    - VS Code Debugger Extension Guide: https://code.visualstudio.com/api/extension-guides/debugger-extension
"""

import sys
import json
import os
import threading
import traceback
from typing import Any, Dict, Optional, List, TextIO
from pathlib import Path


class MLDebugAdapter:
    """
    Debug Adapter Protocol server for ML language.

    This class implements the DAP protocol by wrapping the existing MLDebugger
    with protocol handlers that communicate via stdin/stdout.
    """

    def __init__(self, stdin: TextIO = None, stdout: TextIO = None):
        """
        Initialize DAP server.

        Args:
            stdin: Input stream for DAP messages (default: sys.stdin.buffer)
            stdout: Output stream for DAP messages (default: sys.stdout.buffer)
        """
        # Use binary streams for proper protocol handling
        self.stdin = stdin or sys.stdin.buffer
        self.stdout = stdout or sys.stdout.buffer

        self.seq = 1
        self.debugger: Optional['MLDebugger'] = None
        self.source_map_index: Optional['SourceMapIndex'] = None
        self.ml_file: Optional[str] = None
        self.py_file: Optional[str] = None
        self.py_code: Optional[str] = None  # Store transpiled Python code
        self.thread_id = 1  # DAP requires thread IDs
        self.running = False
        self.initialize_complete = False
        self.stopped = False  # Track if debugger is paused
        self.breakpoints_by_file: Dict[str, List[int]] = {}  # Track breakpoint IDs by file

        # Execution control - event to pause/resume execution
        self.pause_event = threading.Event()
        self.pause_event.set()  # Start in running state

        # Debug logging flag (set to True to enable all logging: stderr + file)
        self.debug_logging = False

    def log(self, message: str):
        """Log debug message to stderr and file (only if debug_logging is enabled)."""
        if not self.debug_logging:
            return  # All logging disabled by default

        # Write to stderr
        sys.stderr.write(f"[ML DAP] {message}\n")
        sys.stderr.flush()

        # Write to file
        try:
            import os
            log_file = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'dap_debug.log')
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[ML DAP] {message}\n")
        except:
            pass  # Don't let logging errors crash the DAP server

    def run(self):
        """Start the DAP server main loop."""
        self.log("DAP server starting...")

        try:
            while True:
                message = self._read_message()
                if message is None:
                    self.log("Connection closed")
                    break

                self.log(f"Received: {message.get('command', message.get('type'))}")

                try:
                    response = self._handle_message(message)
                    if response:
                        self._send_message(response)
                except Exception as e:
                    self.log(f"Error handling message: {e}\n{traceback.format_exc()}")
                    # Send error response
                    if message.get('type') == 'request':
                        error_response = self._create_error_response(
                            message.get('seq', 0),
                            f"Internal error: {str(e)}"
                        )
                        self._send_message(error_response)

        except Exception as e:
            self.log(f"Fatal error in main loop: {e}\n{traceback.format_exc()}")
        finally:
            self.log("DAP server shutting down")

    def _read_message(self) -> Optional[Dict[str, Any]]:
        """
        Read DAP message from stdin.

        Returns:
            Parsed JSON message or None if connection closed
        """
        try:
            # Read Content-Length header
            content_length = None
            while True:
                line = self.stdin.readline()
                if not line:
                    return None

                line = line.decode('utf-8').strip()
                if not line:
                    # Empty line = end of headers
                    break

                if line.startswith('Content-Length: '):
                    content_length = int(line[16:])

            if content_length is None:
                return None

            # Read message body
            body = self.stdin.read(content_length).decode('utf-8')
            return json.loads(body)

        except Exception as e:
            self.log(f"Error reading message: {e}")
            return None

    def _send_message(self, message: Dict[str, Any]):
        """
        Send DAP message to stdout.

        Args:
            message: DAP message to send
        """
        try:
            body = json.dumps(message)
            content = body.encode('utf-8')
            content_length = len(content)

            # Write headers
            header = f'Content-Length: {content_length}\r\n\r\n'.encode('utf-8')
            self.stdout.write(header)
            self.stdout.write(content)
            self.stdout.flush()

            self.log(f"Sent: {message.get('command', message.get('event', 'response'))}")

        except Exception as e:
            self.log(f"Error sending message: {e}")

    def _handle_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Handle incoming DAP message.

        Args:
            message: Incoming DAP message

        Returns:
            Response message or None
        """
        msg_type = message.get('type')

        if msg_type == 'request':
            command = message.get('command')
            args = message.get('arguments', {})
            seq = message.get('seq')

            # Dispatch to handler
            handler_name = f'_handle_{command}'
            handler = getattr(self, handler_name, None)

            if handler:
                return handler(seq, args)
            else:
                self.log(f"Unknown command: {command}")
                return self._create_error_response(seq, f'Unknown command: {command}')

        return None

    # ========== INITIALIZATION ==========

    def _handle_initialize(self, seq: int, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle initialize request.

        This is the first request sent by the client. It declares the capabilities
        of the debug adapter.
        """
        self.log("Handling initialize request")
        self.initialize_complete = True

        return self._create_response(seq, 'initialize', {
            'supportsConfigurationDoneRequest': True,
            'supportsEvaluateForHovers': True,
            'supportsStepBack': False,
            'supportsSetVariable': False,
            'supportsRestartFrame': False,
            'supportsGotoTargetsRequest': False,
            'supportsStepInTargetsRequest': False,
            'supportsCompletionsRequest': False,
            'supportsModulesRequest': False,
            'supportsExceptionInfoRequest': True,
            'supportsExceptionOptions': True,
            'supportsConditionalBreakpoints': True,
            'supportsHitConditionalBreakpoints': False,
            'supportsLogPoints': False,
            'supportsSetExpression': False,
            'supportsDataBreakpoints': False,
            'supportsReadMemoryRequest': False,
            'supportsDisassembleRequest': False,
            'supportsCancelRequest': False,
            'supportsBreakpointLocationsRequest': False,
            'supportsClipboardContext': False,
            'supportsExceptionFilterOptions': True,
            'exceptionBreakpointFilters': [
                {
                    'filter': 'all',
                    'label': 'All Exceptions',
                    'default': False
                },
                {
                    'filter': 'uncaught',
                    'label': 'Uncaught Exceptions',
                    'default': True
                }
            ]
        })

    def _handle_launch(self, seq: int, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle launch request - start debugging session.

        Args:
            seq: Request sequence number
            args: Launch configuration arguments
                - program: ML file path to debug
                - args: Command line arguments (optional)
                - cwd: Working directory (optional)
                - stopOnEntry: Stop at first line (optional)
        """
        self.log("Handling launch request")
        self.ml_file = args.get('program')

        if not self.ml_file:
            return self._create_error_response(seq, 'No program specified')

        try:
            # Send console output
            self._send_event('output', {
                'category': 'console',
                'output': f'Transpiling {self.ml_file}...\n'
            })

            # Import here to avoid circular dependencies
            from mlpy.ml.transpiler import transpile_ml_file
            from mlpy.debugging.debugger import MLDebugger
            from mlpy.debugging.source_map_index import SourceMapIndex

            # Delete cached files to force fresh transpilation with source maps
            # This ensures we always get the latest source maps
            from pathlib import Path
            ml_path = Path(self.ml_file)
            cached_py = ml_path.with_suffix('.py')
            cached_map = ml_path.with_suffix('.py.map')

            if cached_py.exists():
                try:
                    cached_py.unlink()
                    self.log(f"Deleted cached .py file: {cached_py}")
                except Exception as e:
                    self.log(f"Warning: Could not delete cached .py file: {e}")

            if cached_map.exists():
                try:
                    cached_map.unlink()
                    self.log(f"Deleted cached .py.map file: {cached_map}")
                except Exception as e:
                    self.log(f"Warning: Could not delete cached .py.map file: {e}")

            # Transpile ML file to Python
            # transpile_ml_file returns tuple: (python_code, issues, source_map)
            self.log(f"Transpiling ML file: {self.ml_file}")
            try:
                py_code, issues, source_map = transpile_ml_file(
                    self.ml_file,
                    output_path=None,  # DAP server doesn't need to write files
                    strict_security=False,  # Allow debugging even with warnings
                    generate_source_maps=True  # Always generate source maps for debugging
                )
                self.log(f"Transpilation result: py_code={'present' if py_code else 'None'}, issues={len(issues)}, source_map={'present' if source_map else 'None'}")
            except Exception as e:
                self.log(f"Transpilation exception: {type(e).__name__}: {str(e)}")
                self.log(f"Traceback: {traceback.format_exc()}")
                return self._create_error_response(seq, f'Transpilation exception: {type(e).__name__}: {str(e)}')

            if not py_code:
                error_msgs = [issue.error.message for issue in issues] if issues else ['Unknown transpilation error']
                error_detail = "; ".join(error_msgs)
                self.log(f"Transpilation failed: {error_detail}")
                return self._create_error_response(seq, f'Transpilation failed: {error_detail}')

            # Python file path (for reference, though we use the code directly)
            import os
            self.py_file = os.path.splitext(self.ml_file)[0] + '.py'

            # Store the transpiled Python code for execution
            self.py_code = py_code

            # Create simple source map if none provided (1:1 line mapping)
            if not source_map:
                self.log("No source map generated, creating simple 1:1 mapping")
                # Read ML source to count lines
                try:
                    with open(self.ml_file, 'r', encoding='utf-8') as f:
                        ml_lines = len(f.readlines())

                    # Create simple 1:1 mapping using EnhancedSourceMap
                    from mlpy.ml.codegen.enhanced_source_maps import (
                        EnhancedSourceMap,
                        SourceMapping,
                        SourceLocation,
                    )

                    source_map = EnhancedSourceMap()
                    source_map.sources = [self.ml_file]

                    # Create 1:1 line mappings
                    for line_num in range(1, ml_lines + 1):
                        mapping = SourceMapping(
                            generated=SourceLocation(line=line_num, column=0),
                            original=SourceLocation(line=line_num, column=0),
                            source_file=self.ml_file
                        )
                        source_map.mappings.append(mapping)

                    self.log(f"Created simple source map with {len(source_map.mappings)} line mappings")
                except Exception as e:
                    self.log(f"Failed to create fallback source map: {e}")
                    self.log(f"Traceback: {traceback.format_exc()}")
                    return self._create_error_response(seq, f'Could not create source map: {str(e)}')

            # Build source map index
            # Convert dict source map to EnhancedSourceMap object if needed
            if isinstance(source_map, dict):
                # Source map is a dict from JSON serialization, need to reconstruct EnhancedSourceMap
                from mlpy.ml.codegen.enhanced_source_maps import (
                    EnhancedSourceMap,
                    SourceMapping,
                    SourceLocation,
                )

                enhanced_map = EnhancedSourceMap()

                # Extract sources and content from the dict structure
                if 'sourceMap' in source_map:
                    enhanced_map.sources = source_map['sourceMap'].get('sources', [])
                    sources_content = source_map['sourceMap'].get('sourcesContent', [])
                    for i, src in enumerate(enhanced_map.sources):
                        if i < len(sources_content):
                            enhanced_map.source_content[src] = sources_content[i]

                # Reconstruct mappings from detailedMappings
                if 'debugInfo' in source_map and 'detailedMappings' in source_map['debugInfo']:
                    for i, mapping_dict in enumerate(source_map['debugInfo']['detailedMappings']):
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

                self.log(f"Reconstructed source map: {len(enhanced_map.mappings)} mappings")
                source_map = enhanced_map

            self.log(f"Building source map index with {len(source_map.mappings)} mappings")
            self.source_map_index = SourceMapIndex.from_source_map(
                source_map,
                self.py_file
            )
            self.log(f"Source map index built: {len(self.source_map_index.ml_to_py)} ML lines mapped")

            # Create debugger instance
            self.debugger = MLDebugger(
                ml_file=self.ml_file,
                source_map_index=self.source_map_index,
                py_code=py_code,
                py_globals={}
            )

            # Set callback for breakpoint hits
            self.debugger.set_on_break_callback(self._on_breakpoint_hit)

            self._send_event('output', {
                'category': 'console',
                'output': f'Transpilation complete: {self.py_file}\n'
            })

            # Send initialized event to signal that breakpoints can be set
            self._send_event('initialized', {})

            return self._create_response(seq, 'launch', {})

        except Exception as e:
            self.log(f"Launch error: {e}\n{traceback.format_exc()}")
            return self._create_error_response(seq, f'Launch failed: {str(e)}')

    def _handle_configurationDone(self, seq: int, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle configurationDone request.

        This signals that all breakpoints have been set and the program
        is ready to start execution.
        """
        self.log("Handling configurationDone request")

        # Start program execution in separate thread
        def run_program():
            try:
                self.running = True
                self.log("Starting program execution")

                # Start debugger (enables sys.settrace)
                self.debugger.start()

                # Set callback for breakpoint hits
                self.debugger.on_break = self._on_breakpoint_hit

                # Use the transpiled Python code (not from file)
                code = self.py_code

                # Create execution namespace
                exec_globals = {
                    '__name__': '__main__',
                    '__file__': self.py_file
                }

                # CRITICAL FIX: Set trace again immediately before exec
                # This ensures the current thread has the trace function active
                import sys
                sys.settrace(self.debugger.trace_function)

                # Redirect stdout/stderr to capture print output
                import io
                old_stdout = sys.stdout
                old_stderr = sys.stderr
                captured_stdout = io.StringIO()
                captured_stderr = io.StringIO()

                try:
                    sys.stdout = captured_stdout
                    sys.stderr = captured_stderr

                    exec(compile(code, self.py_file, 'exec'), exec_globals)

                finally:
                    sys.stdout = old_stdout
                    sys.stderr = old_stderr

                    # Send captured output to VS Code
                    stdout_text = captured_stdout.getvalue()
                    stderr_text = captured_stderr.getvalue()

                    if stdout_text:
                        self._send_event('output', {
                            'category': 'stdout',
                            'output': stdout_text
                        })

                    if stderr_text:
                        self._send_event('output', {
                            'category': 'stderr',
                            'output': stderr_text
                        })

                # Program completed normally
                self.running = False
                self.log("Program execution completed")
                self._send_event('output', {
                    'category': 'console',
                    'output': '\nProgram exited normally\n'
                })
                self._send_event('terminated', {})

            except Exception as e:
                self.running = False
                self.log(f"Program execution error: {e}\n{traceback.format_exc()}")
                self._send_event('output', {
                    'category': 'stderr',
                    'output': f'Program error: {str(e)}\n'
                })
                self._send_event('terminated', {})

        # Start execution thread
        exec_thread = threading.Thread(target=run_program, daemon=True)
        exec_thread.start()

        return self._create_response(seq, 'configurationDone', {})

    # ========== BREAKPOINTS ==========

    def _handle_setBreakpoints(self, seq: int, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle setBreakpoints request.

        Args:
            seq: Request sequence number
            args: Breakpoint arguments
                - source: Source file information
                - breakpoints: List of breakpoint specifications
        """
        self.log("Handling setBreakpoints request")

        source = args.get('source', {})
        ml_file = source.get('path')
        breakpoints = args.get('breakpoints', [])

        if not self.debugger:
            return self._create_error_response(seq, 'Debugger not initialized')

        verified_breakpoints = []

        # Clear existing breakpoints for this file
        if ml_file in self.breakpoints_by_file:
            for bp_id in self.breakpoints_by_file[ml_file]:
                # Remove from debugger (need to add remove_breakpoint method)
                if hasattr(self.debugger, 'remove_breakpoint'):
                    self.debugger.remove_breakpoint(bp_id)
            self.breakpoints_by_file[ml_file] = []

        # Set new breakpoints
        for bp_spec in breakpoints:
            line = bp_spec.get('line')
            condition = bp_spec.get('condition')

            # Set breakpoint in debugger
            # set_breakpoint returns Breakpoint, PendingBreakpoint, or None
            bp = self.debugger.set_breakpoint(ml_file, line, condition=condition)

            if bp:
                from .debugger import PendingBreakpoint
                is_pending = isinstance(bp, PendingBreakpoint)

                verified_breakpoints.append({
                    'verified': not is_pending,
                    'line': line,
                    'id': bp.id,
                    'message': 'Pending (file not loaded yet)' if is_pending else None
                })

                # Track breakpoint ID
                if ml_file not in self.breakpoints_by_file:
                    self.breakpoints_by_file[ml_file] = []
                self.breakpoints_by_file[ml_file].append(bp.id)

                status = "pending" if is_pending else "active"
                self.log(f"Breakpoint set: {ml_file}:{line} (id={bp.id}, {status})")
            else:
                verified_breakpoints.append({
                    'verified': False,
                    'line': line,
                    'message': 'Line is not executable'
                })
                self.log(f"Breakpoint failed: {ml_file}:{line} (not executable)")

        return self._create_response(seq, 'setBreakpoints', {
            'breakpoints': verified_breakpoints
        })

    def _handle_setExceptionBreakpoints(self, seq: int, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle setExceptionBreakpoints request.

        Args:
            seq: Request sequence number
            args: Exception breakpoint arguments
                - filters: List of exception filter names
        """
        self.log("Handling setExceptionBreakpoints request")

        filters = args.get('filters', [])

        if self.debugger:
            # Enable exception breakpoints
            if 'all' in filters or 'uncaught' in filters:
                self.debugger.break_on_exceptions = True
                self.debugger.exception_filters = filters
                self.log(f"Exception breakpoints enabled: {filters}")

        return self._create_response(seq, 'setExceptionBreakpoints', {})

    # ========== EXECUTION CONTROL ==========

    def _handle_continue(self, seq: int, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle continue request - resume execution."""
        self.log("Handling continue request")

        if self.debugger:
            self.stopped = False
            self.debugger.continue_execution()
            # Resume the paused execution thread
            self.pause_event.set()

        return self._create_response(seq, 'continue', {
            'allThreadsContinued': True
        })

    def _handle_next(self, seq: int, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle next request - step over."""
        self.log("Handling next request")

        if self.debugger:
            self.stopped = False
            self.debugger.step_next()
            # Resume the paused execution thread
            self.pause_event.set()

        return self._create_response(seq, 'next', {})

    def _handle_stepIn(self, seq: int, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle stepIn request - step into function."""
        self.log("Handling stepIn request")

        if self.debugger:
            self.stopped = False
            self.debugger.step_into()
            # Resume the paused execution thread
            self.pause_event.set()

        return self._create_response(seq, 'stepIn', {})

    def _handle_stepOut(self, seq: int, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle stepOut request - step out of function."""
        self.log("Handling stepOut request")

        if self.debugger:
            self.stopped = False
            self.debugger.step_out()
            # Resume the paused execution thread
            self.pause_event.set()

        return self._create_response(seq, 'stepOut', {})

    def _handle_disconnect(self, seq: int, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle disconnect request - end debugging session."""
        self.log("Handling disconnect request")

        # Release any paused execution thread
        self.pause_event.set()

        # Clean up debugger
        if self.debugger:
            self.debugger.stop()
            self.debugger = None

        self.running = False

        return self._create_response(seq, 'disconnect', {})

    # ========== STACK AND VARIABLES ==========

    def _handle_threads(self, seq: int, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle threads request."""
        self.log("Handling threads request")

        return self._create_response(seq, 'threads', {
            'threads': [
                {
                    'id': self.thread_id,
                    'name': 'Main Thread'
                }
            ]
        })

    def _handle_stackTrace(self, seq: int, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle stackTrace request.

        Args:
            seq: Request sequence number
            args: Stack trace arguments
                - threadId: Thread ID
                - startFrame: Starting frame index (optional)
                - levels: Number of frames to return (optional)
        """
        self.log("Handling stackTrace request")

        if not self.debugger:
            return self._create_response(seq, 'stackTrace', {'stackFrames': [], 'totalFrames': 0})

        # Get call stack with frames from debugger
        stack = self.debugger.get_call_stack_with_frames()

        stack_frames = []
        for idx, frame_info in enumerate(stack):
            ml_file, ml_line, ml_col = frame_info['ml_position']
            func_name = frame_info['function_name']

            stack_frames.append({
                'id': idx,
                'name': func_name,
                'source': {
                    'name': Path(ml_file).name,
                    'path': ml_file
                },
                'line': ml_line,
                'column': ml_col
            })

        self.log(f"Stack trace: {len(stack_frames)} frames")

        return self._create_response(seq, 'stackTrace', {
            'stackFrames': stack_frames,
            'totalFrames': len(stack_frames)
        })

    def _handle_scopes(self, seq: int, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle scopes request.

        Args:
            seq: Request sequence number
            args: Scope arguments
                - frameId: Stack frame ID
        """
        self.log("Handling scopes request")

        frame_id = args.get('frameId', 0)

        return self._create_response(seq, 'scopes', {
            'scopes': [
                {
                    'name': 'Locals',
                    'variablesReference': frame_id * 1000 + 1,  # Unique ID
                    'expensive': False
                },
                {
                    'name': 'Globals',
                    'variablesReference': frame_id * 1000 + 2,
                    'expensive': False
                }
            ]
        })

    def _handle_variables(self, seq: int, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle variables request.

        Args:
            seq: Request sequence number
            args: Variables arguments
                - variablesReference: Scope reference ID
        """
        self.log("Handling variables request")

        variables_reference = args.get('variablesReference')

        if not self.debugger:
            return self._create_response(seq, 'variables', {'variables': []})

        # Decode variables reference
        frame_id = variables_reference // 1000
        scope_id = variables_reference % 1000

        variables = []

        try:
            if scope_id == 1:  # Locals
                locals_dict = self.debugger.get_locals(frame_id)
                for name, value in locals_dict.items():
                    variables.append(self._format_variable(name, value))

            elif scope_id == 2:  # Globals
                globals_dict = self.debugger.get_globals(frame_id)
                for name, value in globals_dict.items():
                    if not name.startswith('__'):  # Filter Python internals
                        variables.append(self._format_variable(name, value))

        except Exception as e:
            self.log(f"Error getting variables: {e}")

        self.log(f"Variables: {len(variables)} items")

        return self._create_response(seq, 'variables', {
            'variables': variables
        })

    def _format_variable(self, name: str, value: Any) -> Dict[str, Any]:
        """
        Format variable for DAP protocol.

        Args:
            name: Variable name
            value: Variable value

        Returns:
            DAP variable object
        """
        # Use existing VariableFormatter for ML-aware formatting
        try:
            from mlpy.debugging.variable_formatter import VariableFormatter
            formatter = VariableFormatter()
            formatted = formatter.format_value(value, max_depth=1)
        except Exception:
            # Fallback to simple string representation
            formatted = str(value)

        return {
            'name': name,
            'value': formatted,
            'type': type(value).__name__,
            'variablesReference': 0  # TODO: Support nested object inspection
        }

    # ========== EVALUATION ==========

    def _handle_evaluate(self, seq: int, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle evaluate request (for watch expressions, hover, debug console).

        Args:
            seq: Request sequence number
            args: Evaluate arguments
                - expression: Expression to evaluate
                - frameId: Stack frame ID (optional)
                - context: Evaluation context (watch, hover, repl)
        """
        self.log("Handling evaluate request")

        expression = args.get('expression')
        context = args.get('context', 'watch')
        frame_id = args.get('frameId', 0)

        if not self.debugger:
            return self._create_error_response(seq, 'Debugger not running')

        try:
            # Evaluate expression using SafeExpressionEvaluator
            result = self.debugger.evaluate_expression(expression, frame_id)

            return self._create_response(seq, 'evaluate', {
                'result': str(result),
                'type': type(result).__name__,
                'variablesReference': 0
            })

        except Exception as e:
            self.log(f"Evaluation error: {e}")
            return self._create_error_response(seq, f'Evaluation failed: {str(e)}')

    # ========== HELPERS ==========

    def _on_breakpoint_hit(self):
        """
        Callback when debugger hits a breakpoint.

        This is called by MLDebugger when execution pauses.
        This method BLOCKS until VS Code sends a continue/step command.
        """
        self.log("Breakpoint hit! Pausing execution...")
        self.stopped = True

        # Send stopped event to VS Code
        self._send_event('stopped', {
            'reason': 'breakpoint',
            'threadId': self.thread_id,
            'allThreadsStopped': True
        })

        # BLOCK execution until VS Code sends continue/step command
        self.pause_event.clear()  # Clear the event
        self.log("Waiting for continue/step command...")
        self.pause_event.wait()  # Block here until event is set
        self.log("Resuming execution")

    def _create_response(self, request_seq: int, command: str, body: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create success response.

        Args:
            request_seq: Original request sequence number
            command: Command name
            body: Response body

        Returns:
            DAP response message
        """
        return {
            'type': 'response',
            'request_seq': request_seq,
            'success': True,
            'command': command,
            'body': body,
            'seq': self._next_seq()
        }

    def _create_error_response(self, request_seq: int, message: str) -> Dict[str, Any]:
        """
        Create error response.

        Args:
            request_seq: Original request sequence number
            message: Error message

        Returns:
            DAP error response message
        """
        return {
            'type': 'response',
            'request_seq': request_seq,
            'success': False,
            'message': message,
            'seq': self._next_seq()
        }

    def _send_event(self, event: str, body: Dict[str, Any]):
        """
        Send event to client.

        Args:
            event: Event name
            body: Event body
        """
        message = {
            'type': 'event',
            'event': event,
            'body': body,
            'seq': self._next_seq()
        }
        self._send_message(message)

    def _next_seq(self) -> int:
        """Get next sequence number."""
        seq = self.seq
        self.seq += 1
        return seq


def main():
    """Entry point for DAP server."""
    # Ensure we're using binary mode for stdin/stdout
    if sys.platform == 'win32':
        import msvcrt
        msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
        msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

    adapter = MLDebugAdapter()
    adapter.run()


if __name__ == '__main__':
    main()
