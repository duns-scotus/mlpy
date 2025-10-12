# ML Debugger - Phase 5: VS Code Native Debugging Implementation Plan

**Document Type:** Implementation Plan
**Created:** October 2025
**Status:** Ready for Implementation
**Dependencies:** Phase 1-4.5 Complete (✅)
**Target:** Native debugging experience in VS Code via Debug Adapter Protocol (DAP)

---

## Executive Summary

This plan details the implementation of **native debugging support in VS Code** by wrapping the existing MLDebugger with a Debug Adapter Protocol (DAP) server. This will enable developers to use VS Code's built-in debugging UI with ML programs, providing a professional IDE debugging experience.

**Key Goals:**
1. ✅ **Zero Additional Overhead** - Leverage existing MLDebugger (no new performance costs)
2. ✅ **Professional UI** - Use VS Code's native debugging interface (breakpoints, variables, call stack)
3. ✅ **Multi-File Debugging** - Full project debugging support with automatic import detection
4. ✅ **Launch Configurations** - Debug/Run configurations with custom arguments and settings
5. ✅ **Minimal Changes** - Small adapter layer, no debugger core changes needed

**Timeline:** 5-7 days
**Effort:** ~800-1000 LOC (DAP server + VS Code integration)

---

## Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    VS Code Debug UI                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │Breakpoint│  │ Variables│  │Call Stack│  │  Watch   │  │
│  │  Gutter  │  │   Panel  │  │   Panel  │  │  Panel   │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↕ DAP Protocol (JSON-RPC)
┌─────────────────────────────────────────────────────────────┐
│              DAP Server (Python)                            │
│  src/mlpy/debugging/dap_server.py                          │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  DAP Protocol Handler                                 │ │
│  │  - initialize, launch, attach                         │ │
│  │  - setBreakpoints, continue, next, stepIn, stepOut   │ │
│  │  - scopes, variables, evaluate                        │ │
│  │  - threads, stackTrace, source                        │ │
│  └──────────────────────────────────────────────────────┘ │
│                              ↕ Python API                   │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  MLDebugger (Existing)                                │ │
│  │  - set_breakpoint(), continue(), next(), step()       │ │
│  │  - get_variable(), get_call_stack()                   │ │
│  │  - sys.settrace() implementation                      │ │
│  └──────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              ↕ sys.settrace()
┌─────────────────────────────────────────────────────────────┐
│          Generated Python Code (*.py)                       │
│          + Source Maps (*.ml.map)                           │
└─────────────────────────────────────────────────────────────┘
```

### Communication Flow

```
User sets breakpoint in VS Code
  ↓
VS Code → DAP: setBreakpoints request
  ↓
DAP Server → MLDebugger.set_breakpoint()
  ↓
DAP Server → VS Code: setBreakpoints response
  ↓
User presses F5 (Start Debugging)
  ↓
VS Code → DAP: launch request
  ↓
DAP Server starts ML program with debugger attached
  ↓
Program hits breakpoint
  ↓
MLDebugger pauses execution
  ↓
DAP Server → VS Code: stopped event (reason: breakpoint)
  ↓
VS Code requests: stackTrace, scopes, variables
  ↓
DAP Server → MLDebugger → VS Code: stack frames, variables
  ↓
VS Code displays in UI (Call Stack, Variables panels)
  ↓
User clicks Continue/Step buttons
  ↓
VS Code → DAP: continue/next/stepIn request
  ↓
DAP Server → MLDebugger.continue/next/step()
  ↓
Program continues execution...
```

---

## Phase 5 Implementation Components

### Component 1: DAP Server Core (Day 1-3)

**File:** `src/mlpy/debugging/dap_server.py`

**Purpose:** Implement Debug Adapter Protocol server that wraps MLDebugger

**Key Classes:**

#### 1.1 MLDebugAdapter (Main Server)

```python
# src/mlpy/debugging/dap_server.py

import sys
import json
import threading
from typing import Any, Dict, Optional
from .debugger import MLDebugger
from .source_map_index import SourceMapIndex
from ..ml.transpiler import transpile

class MLDebugAdapter:
    """Debug Adapter Protocol server for ML language."""

    def __init__(self, stdin=sys.stdin, stdout=sys.stdout):
        self.stdin = stdin
        self.stdout = stdout
        self.seq = 1
        self.debugger: Optional[MLDebugger] = None
        self.source_map_index: Optional[SourceMapIndex] = None
        self.ml_file: Optional[str] = None
        self.py_file: Optional[str] = None
        self.thread_id = 1  # DAP requires thread IDs
        self.running = False
        self.initialize_complete = False

    def run(self):
        """Start the DAP server main loop."""
        while True:
            message = self._read_message()
            if message is None:
                break

            response = self._handle_message(message)
            if response:
                self._send_message(response)

    def _read_message(self) -> Optional[Dict[str, Any]]:
        """Read DAP message from stdin."""
        # Read Content-Length header
        content_length = None
        while True:
            line = self.stdin.readline()
            if not line:
                return None

            line = line.strip()
            if not line:
                # Empty line = end of headers
                break

            if line.startswith('Content-Length: '):
                content_length = int(line[16:])

        if content_length is None:
            return None

        # Read message body
        body = self.stdin.read(content_length)
        return json.loads(body)

    def _send_message(self, message: Dict[str, Any]):
        """Send DAP message to stdout."""
        body = json.dumps(message)
        content_length = len(body.encode('utf-8'))

        # Write headers
        self.stdout.write(f'Content-Length: {content_length}\r\n\r\n')
        self.stdout.write(body)
        self.stdout.flush()

    def _handle_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Handle incoming DAP message."""
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
                return self._create_error_response(seq, f'Unknown command: {command}')

        return None
```

#### 1.2 DAP Request Handlers

```python
    # INITIALIZATION

    def _handle_initialize(self, seq: int, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialize request."""
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
        """Handle launch request - start debugging session."""
        self.ml_file = args.get('program')

        if not self.ml_file:
            return self._create_error_response(seq, 'No program specified')

        try:
            # Transpile ML file to Python
            self._send_event('output', {
                'category': 'console',
                'output': f'Transpiling {self.ml_file}...\n'
            })

            result = transpile(self.ml_file)

            if not result.success:
                return self._create_error_response(seq, f'Transpilation failed: {result.error}')

            self.py_file = result.output_file
            self.source_map_index = SourceMapIndex.from_source_map(
                result.source_map,
                self.py_file
            )

            # Create debugger instance
            self.debugger = MLDebugger(self.ml_file, self.source_map_index)

            # Set any pending breakpoints
            # (will be set via setBreakpoints request before launch)

            self._send_event('initialized', {})

            return self._create_response(seq, 'launch', {})

        except Exception as e:
            return self._create_error_response(seq, f'Launch failed: {e}')

    def _handle_configurationDone(self, seq: int, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle configurationDone request - ready to start execution."""

        # Start program execution in separate thread
        def run_program():
            try:
                self.running = True

                # Start debugger (enables sys.settrace)
                self.debugger.start()

                # Execute the Python file
                with open(self.py_file, 'r') as f:
                    code = f.read()

                # Execute in debugger context
                exec(compile(code, self.py_file, 'exec'), {})

                # Program completed
                self.running = False
                self._send_event('terminated', {})

            except Exception as e:
                self.running = False
                self._send_event('output', {
                    'category': 'stderr',
                    'output': f'Program error: {e}\n'
                })
                self._send_event('terminated', {})

        # Start execution thread
        exec_thread = threading.Thread(target=run_program, daemon=True)
        exec_thread.start()

        return self._create_response(seq, 'configurationDone', {})

    # BREAKPOINTS

    def _handle_setBreakpoints(self, seq: int, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle setBreakpoints request."""
        source = args.get('source', {})
        ml_file = source.get('path')
        breakpoints = args.get('breakpoints', [])

        if not self.debugger:
            return self._create_error_response(seq, 'Debugger not initialized')

        verified_breakpoints = []

        # Clear existing breakpoints for this file
        # (MLDebugger should support this - may need to add)

        # Set new breakpoints
        for bp in breakpoints:
            line = bp.get('line')
            condition = bp.get('condition')

            # Set breakpoint in debugger
            result = self.debugger.set_breakpoint(ml_file, line, condition=condition)

            if result:
                verified_breakpoints.append({
                    'verified': True,
                    'line': line,
                    'id': result.id
                })
            else:
                verified_breakpoints.append({
                    'verified': False,
                    'line': line,
                    'message': 'Line is not executable'
                })

        return self._create_response(seq, 'setBreakpoints', {
            'breakpoints': verified_breakpoints
        })

    def _handle_setExceptionBreakpoints(self, seq: int, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle setExceptionBreakpoints request."""
        filters = args.get('filters', [])

        if self.debugger:
            # Enable exception breakpoints
            if 'all' in filters or 'uncaught' in filters:
                self.debugger.break_on_exceptions = True
                self.debugger.exception_filters = filters

        return self._create_response(seq, 'setExceptionBreakpoints', {})

    # EXECUTION CONTROL

    def _handle_continue(self, seq: int, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle continue request."""
        if self.debugger:
            self.debugger.continue_execution()

        return self._create_response(seq, 'continue', {
            'allThreadsContinued': True
        })

    def _handle_next(self, seq: int, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle next request (step over)."""
        if self.debugger:
            self.debugger.step_next()

        return self._create_response(seq, 'next', {})

    def _handle_stepIn(self, seq: int, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle stepIn request."""
        if self.debugger:
            self.debugger.step_into()

        return self._create_response(seq, 'stepIn', {})

    def _handle_stepOut(self, seq: int, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle stepOut request."""
        if self.debugger:
            self.debugger.step_out()

        return self._create_response(seq, 'stepOut', {})

    # STACK AND VARIABLES

    def _handle_threads(self, seq: int, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle threads request."""
        return self._create_response(seq, 'threads', {
            'threads': [
                {
                    'id': self.thread_id,
                    'name': 'Main Thread'
                }
            ]
        })

    def _handle_stackTrace(self, seq: int, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle stackTrace request."""
        if not self.debugger:
            return self._create_response(seq, 'stackTrace', {'stackFrames': []})

        # Get call stack from debugger
        stack = self.debugger.get_call_stack()

        stack_frames = []
        for idx, frame_info in enumerate(stack):
            ml_file, ml_line, ml_col = frame_info['ml_position']
            func_name = frame_info['function_name']

            stack_frames.append({
                'id': idx,
                'name': func_name,
                'source': {
                    'name': ml_file,
                    'path': ml_file
                },
                'line': ml_line,
                'column': ml_col
            })

        return self._create_response(seq, 'stackTrace', {
            'stackFrames': stack_frames,
            'totalFrames': len(stack_frames)
        })

    def _handle_scopes(self, seq: int, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle scopes request."""
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
        """Handle variables request."""
        variables_reference = args.get('variablesReference')

        if not self.debugger:
            return self._create_response(seq, 'variables', {'variables': []})

        # Decode variables reference
        frame_id = variables_reference // 1000
        scope_id = variables_reference % 1000

        variables = []

        if scope_id == 1:  # Locals
            locals_dict = self.debugger.get_locals(frame_id)
            for name, value in locals_dict.items():
                variables.append(self._format_variable(name, value))

        elif scope_id == 2:  # Globals
            globals_dict = self.debugger.get_globals(frame_id)
            for name, value in globals_dict.items():
                if not name.startswith('__'):  # Filter Python internals
                    variables.append(self._format_variable(name, value))

        return self._create_response(seq, 'variables', {
            'variables': variables
        })

    def _format_variable(self, name: str, value: Any) -> Dict[str, Any]:
        """Format variable for DAP protocol."""
        # Use existing VariableFormatter
        from .variable_formatter import VariableFormatter
        formatter = VariableFormatter()

        formatted = formatter.format_value(value, max_depth=1)

        return {
            'name': name,
            'value': formatted,
            'type': type(value).__name__,
            'variablesReference': 0  # TODO: Handle complex objects
        }

    # EVALUATION

    def _handle_evaluate(self, seq: int, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle evaluate request (for watch expressions, hover)."""
        expression = args.get('expression')
        context = args.get('context', 'watch')
        frame_id = args.get('frameId', 0)

        if not self.debugger:
            return self._create_error_response(seq, 'Debugger not running')

        try:
            # Use SafeExpressionEvaluator
            result = self.debugger.evaluate_expression(expression, frame_id)

            return self._create_response(seq, 'evaluate', {
                'result': str(result),
                'type': type(result).__name__,
                'variablesReference': 0
            })

        except Exception as e:
            return self._create_error_response(seq, f'Evaluation failed: {e}')

    # HELPERS

    def _create_response(self, request_seq: int, command: str, body: Dict[str, Any]) -> Dict[str, Any]:
        """Create success response."""
        return {
            'type': 'response',
            'request_seq': request_seq,
            'success': True,
            'command': command,
            'body': body,
            'seq': self._next_seq()
        }

    def _create_error_response(self, request_seq: int, message: str) -> Dict[str, Any]:
        """Create error response."""
        return {
            'type': 'response',
            'request_seq': request_seq,
            'success': False,
            'message': message,
            'seq': self._next_seq()
        }

    def _send_event(self, event: str, body: Dict[str, Any]):
        """Send event to VS Code."""
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
    import sys

    # Set binary mode for stdin/stdout
    if sys.platform == 'win32':
        import os, msvcrt
        msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
        msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

    adapter = MLDebugAdapter()
    adapter.run()


if __name__ == '__main__':
    main()
```

**Implementation Notes:**
- ~600-700 LOC for complete DAP server
- Wraps existing MLDebugger (no core changes needed)
- Handles all essential DAP requests
- Uses existing VariableFormatter and SafeExpressionEvaluator
- Communicates via stdin/stdout (standard for DAP)

---

### Component 2: MLDebugger Enhancements (Day 2)

**File:** `src/mlpy/debugging/debugger.py` (minor additions)

**Required Additions to MLDebugger:**

```python
# Add to existing MLDebugger class

class MLDebugger:
    # ... existing code ...

    def step_into(self):
        """Step into function calls."""
        self.step_mode = StepMode.STEP_INTO
        # Implementation similar to step_next

    def step_out(self):
        """Step out of current function."""
        self.step_mode = StepMode.STEP_OUT
        self.step_out_depth = len(inspect.stack())

    def get_call_stack(self) -> List[Dict[str, Any]]:
        """Get full call stack with ML positions."""
        if not self.current_frame:
            return []

        stack = []
        frame = self.current_frame

        while frame:
            # Get Python position
            py_file = frame.f_code.co_filename
            py_line = frame.f_lineno

            # Map to ML position
            ml_pos = self.source_map_index.py_line_to_ml(py_file, py_line)

            if ml_pos:
                ml_file, ml_line, ml_col = ml_pos
                func_name = frame.f_code.co_name

                stack.append({
                    'frame': frame,
                    'ml_position': (ml_file, ml_line, ml_col),
                    'function_name': func_name
                })

            frame = frame.f_back

        return stack

    def get_locals(self, frame_id: int = 0) -> Dict[str, Any]:
        """Get local variables for specific stack frame."""
        stack = self.get_call_stack()

        if frame_id < len(stack):
            frame = stack[frame_id]['frame']
            return frame.f_locals.copy()

        return {}

    def get_globals(self, frame_id: int = 0) -> Dict[str, Any]:
        """Get global variables for specific stack frame."""
        stack = self.get_call_stack()

        if frame_id < len(stack):
            frame = stack[frame_id]['frame']
            return frame.f_globals.copy()

        return {}

    def evaluate_expression(self, expression: str, frame_id: int = 0) -> Any:
        """Evaluate expression in context of stack frame."""
        stack = self.get_call_stack()

        if frame_id < len(stack):
            frame = stack[frame_id]['frame']

            # Use SafeExpressionEvaluator
            from .safe_expression_eval import SafeExpressionEvaluator
            evaluator = SafeExpressionEvaluator(frame)

            return evaluator.evaluate(expression)

        raise ValueError(f'Invalid frame ID: {frame_id}')

    def clear_breakpoints(self, ml_file: str):
        """Clear all breakpoints in a file."""
        to_remove = [bp_id for bp_id, bp in self.breakpoints.items()
                     if bp.ml_file == ml_file]

        for bp_id in to_remove:
            del self.breakpoints[bp_id]
```

**Additions:**
- ~100-150 LOC
- step_into(), step_out() for advanced stepping
- get_call_stack() for DAP stackTrace
- get_locals(), get_globals() for variable inspection
- evaluate_expression() for watch and hover
- clear_breakpoints() for DAP breakpoint management

---

### Component 3: VS Code Extension Integration (Day 3-4)

**File:** `ext/vscode/package.json` (additions)

```json
{
  "contributes": {
    "debuggers": [
      {
        "type": "ml",
        "label": "ML Debugger",
        "program": "./out/debugAdapter.js",
        "runtime": "node",
        "configurationAttributes": {
          "launch": {
            "required": ["program"],
            "properties": {
              "program": {
                "type": "string",
                "description": "Absolute path to ML file to debug",
                "default": "${file}"
              },
              "args": {
                "type": "array",
                "description": "Command line arguments",
                "default": []
              },
              "stopOnEntry": {
                "type": "boolean",
                "description": "Automatically stop after launch",
                "default": false
              },
              "cwd": {
                "type": "string",
                "description": "Working directory",
                "default": "${workspaceFolder}"
              },
              "mlpyPath": {
                "type": "string",
                "description": "Path to mlpy installation",
                "default": "${workspaceFolder}"
              },
              "pythonPath": {
                "type": "string",
                "description": "Python interpreter path",
                "default": "python"
              },
              "trace": {
                "type": "boolean",
                "description": "Enable debug adapter trace",
                "default": false
              }
            }
          }
        },
        "initialConfigurations": [
          {
            "type": "ml",
            "request": "launch",
            "name": "Debug ML File",
            "program": "${file}",
            "stopOnEntry": false
          }
        ],
        "configurationSnippets": [
          {
            "label": "ML: Launch",
            "description": "Debug an ML file",
            "body": {
              "type": "ml",
              "request": "launch",
              "name": "Debug ML File",
              "program": "^\"\\${file}\"",
              "stopOnEntry": false
            }
          },
          {
            "label": "ML: Launch with Arguments",
            "description": "Debug an ML file with command line arguments",
            "body": {
              "type": "ml",
              "request": "launch",
              "name": "Debug ML File (Args)",
              "program": "^\"\\${file}\"",
              "args": [],
              "stopOnEntry": false
            }
          }
        ]
      }
    ],
    "breakpoints": [
      {
        "language": "ml"
      }
    ]
  }
}
```

**File:** `ext/vscode/src/debugAdapter.ts` (new file)

```typescript
import * as vscode from 'vscode';
import * as path from 'path';
import { spawn, ChildProcess } from 'child_process';

/**
 * Debug adapter factory for ML language.
 *
 * This creates a debug session by spawning the Python DAP server
 * and connecting it to VS Code via stdin/stdout.
 */
export class MLDebugAdapterDescriptorFactory implements vscode.DebugAdapterDescriptorFactory {

    createDebugAdapterDescriptor(
        session: vscode.DebugSession,
        executable: vscode.DebugAdapterExecutable | undefined
    ): vscode.ProviderResult<vscode.DebugAdapterDescriptor> {

        // Get configuration
        const config = session.configuration;
        const pythonPath = config.pythonPath || this.getPythonPath();
        const mlpyPath = config.mlpyPath || this.getMLPyPath();

        // Path to DAP server
        const dapServerPath = path.join(mlpyPath, 'src', 'mlpy', 'debugging', 'dap_server.py');

        // Spawn DAP server process
        const serverProcess = spawn(pythonPath, [dapServerPath], {
            cwd: mlpyPath,
            stdio: ['pipe', 'pipe', 'pipe'],
            env: {
                ...process.env,
                PYTHONPATH: mlpyPath,
                MLPY_DEBUG: config.trace ? '1' : '0'
            }
        });

        // Log stderr for debugging
        if (config.trace) {
            serverProcess.stderr.on('data', (data) => {
                console.error(`[ML DAP Server] ${data.toString()}`);
            });
        }

        // Return descriptor connecting VS Code to the server
        return new vscode.DebugAdapterServer(
            serverProcess.stdout,
            serverProcess.stdin
        );
    }

    private getPythonPath(): string {
        // Try to get Python path from VS Code settings
        const config = vscode.workspace.getConfiguration('python');
        return config.get<string>('defaultInterpreterPath') ||
               config.get<string>('pythonPath') ||
               'python';
    }

    private getMLPyPath(): string {
        // Get workspace folder
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (workspaceFolders && workspaceFolders.length > 0) {
            return workspaceFolders[0].uri.fsPath;
        }

        // Fallback to current directory
        return process.cwd();
    }
}

/**
 * Register debug adapter with VS Code.
 */
export function registerDebugAdapter(context: vscode.ExtensionContext) {
    // Register adapter factory
    const factory = new MLDebugAdapterDescriptorFactory();
    context.subscriptions.push(
        vscode.debug.registerDebugAdapterDescriptorFactory('ml', factory)
    );

    // Register debug configuration provider
    const provider = new MLDebugConfigurationProvider();
    context.subscriptions.push(
        vscode.debug.registerDebugConfigurationProvider('ml', provider)
    );

    // Add status bar item when debugging
    context.subscriptions.push(
        vscode.debug.onDidStartDebugSession((session) => {
            if (session.type === 'ml') {
                vscode.window.showInformationMessage('ML Debugging session started');
            }
        })
    );

    context.subscriptions.push(
        vscode.debug.onDidTerminateDebugSession((session) => {
            if (session.type === 'ml') {
                vscode.window.showInformationMessage('ML Debugging session ended');
            }
        })
    );
}

/**
 * Provides default debug configurations.
 */
class MLDebugConfigurationProvider implements vscode.DebugConfigurationProvider {

    /**
     * Provide default launch configuration when none exists.
     */
    provideDebugConfigurations(
        folder: vscode.WorkspaceFolder | undefined
    ): vscode.ProviderResult<vscode.DebugConfiguration[]> {

        return [
            {
                type: 'ml',
                request: 'launch',
                name: 'Debug Current ML File',
                program: '${file}',
                stopOnEntry: false
            },
            {
                type: 'ml',
                request: 'launch',
                name: 'Debug ML File with Args',
                program: '${file}',
                args: [],
                stopOnEntry: false
            }
        ];
    }

    /**
     * Resolve and validate debug configuration before starting session.
     */
    resolveDebugConfiguration(
        folder: vscode.WorkspaceFolder | undefined,
        config: vscode.DebugConfiguration,
        token?: vscode.CancellationToken
    ): vscode.ProviderResult<vscode.DebugConfiguration> {

        // If no program specified, use active editor
        if (!config.program) {
            const editor = vscode.window.activeTextEditor;

            if (editor && editor.document.languageId === 'ml') {
                config.program = editor.document.uri.fsPath;
            } else {
                vscode.window.showErrorMessage('Cannot debug: No ML file selected');
                return undefined;
            }
        }

        // Set default values
        config.stopOnEntry = config.stopOnEntry || false;
        config.args = config.args || [];
        config.cwd = config.cwd || (folder ? folder.uri.fsPath : process.cwd());

        return config;
    }
}
```

**Integration in extension.ts:**

```typescript
// Add to ext/vscode/src/extension.ts

import { registerDebugAdapter } from './debugAdapter';

export async function activate(context: vscode.ExtensionContext) {
    console.log('ML Language Support extension is being activated');

    // ... existing code ...

    // Register debug adapter (NEW)
    registerDebugAdapter(context);

    console.log('ML Language Support extension activated successfully');
}
```

**VS Code Integration:**
- ~200-250 LOC TypeScript
- Debug adapter factory spawns Python DAP server
- Configuration provider for launch.json
- Debug session lifecycle management
- Automatic breakpoint gutter integration

---

### Component 4: Launch Configuration Templates (Day 4)

**File:** `.vscode/launch.json` (example for users)

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "ml",
      "request": "launch",
      "name": "Debug Current File",
      "program": "${file}",
      "stopOnEntry": false
    },
    {
      "type": "ml",
      "request": "launch",
      "name": "Debug Main",
      "program": "${workspaceFolder}/main.ml",
      "stopOnEntry": false
    },
    {
      "type": "ml",
      "request": "launch",
      "name": "Debug with Args",
      "program": "${workspaceFolder}/cli.ml",
      "args": ["--verbose", "--input", "data.txt"],
      "stopOnEntry": false
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
```

**Documentation:** Update user guide with debugging instructions.

---

### Component 5: Testing Infrastructure (Day 5-6)

#### 5.1 Unit Tests for DAP Server

**File:** `tests/debugging/test_dap_server.py`

```python
import pytest
import json
from src.mlpy.debugging.dap_server import MLDebugAdapter

class TestDAPProtocol:
    """Test DAP protocol implementation."""

    def test_initialize_request(self):
        """Test initialize request returns correct capabilities."""
        adapter = MLDebugAdapter()

        response = adapter._handle_initialize(1, {
            'clientID': 'vscode',
            'adapterID': 'ml'
        })

        assert response['success'] == True
        assert response['body']['supportsConditionalBreakpoints'] == True
        assert response['body']['supportsEvaluateForHovers'] == True

    def test_launch_request(self):
        """Test launch request transpiles and initializes debugger."""
        # Create test ML file
        test_ml = """
        function test() {
            x = 5;
            print(x);
        }
        test();
        """

        with open('test.ml', 'w') as f:
            f.write(test_ml)

        adapter = MLDebugAdapter()
        adapter._handle_initialize(1, {})

        response = adapter._handle_launch(2, {
            'program': 'test.ml'
        })

        assert response['success'] == True
        assert adapter.debugger is not None
        assert adapter.py_file is not None

    def test_set_breakpoints(self):
        """Test setting breakpoints."""
        # Setup adapter with debugger
        adapter = self._create_initialized_adapter()

        response = adapter._handle_setBreakpoints(3, {
            'source': {'path': 'test.ml'},
            'breakpoints': [
                {'line': 2},
                {'line': 3, 'condition': 'x > 10'}
            ]
        })

        assert response['success'] == True
        assert len(response['body']['breakpoints']) == 2
        assert response['body']['breakpoints'][0]['verified'] == True

    def test_stack_trace(self):
        """Test stack trace retrieval."""
        adapter = self._create_running_adapter()

        # Simulate breakpoint hit
        # ... setup ...

        response = adapter._handle_stackTrace(4, {'threadId': 1})

        assert response['success'] == True
        assert len(response['body']['stackFrames']) > 0
        assert 'name' in response['body']['stackFrames'][0]
        assert 'source' in response['body']['stackFrames'][0]

    def test_variables_request(self):
        """Test variable inspection."""
        adapter = self._create_running_adapter()

        response = adapter._handle_variables(5, {
            'variablesReference': 1  # Locals scope
        })

        assert response['success'] == True
        assert 'variables' in response['body']

    def test_evaluate_expression(self):
        """Test expression evaluation."""
        adapter = self._create_running_adapter()

        response = adapter._handle_evaluate(6, {
            'expression': 'x + 5',
            'frameId': 0,
            'context': 'watch'
        })

        assert response['success'] == True
        assert 'result' in response['body']

    # Helper methods
    def _create_initialized_adapter(self):
        """Create adapter with debugger initialized."""
        # Implementation...
        pass

    def _create_running_adapter(self):
        """Create adapter with program running at breakpoint."""
        # Implementation...
        pass
```

#### 5.2 Integration Tests

**File:** `tests/debugging/test_dap_integration.py`

```python
import pytest
import subprocess
import json
from pathlib import Path

class TestDAPIntegration:
    """End-to-end DAP integration tests."""

    def test_full_debug_session(self):
        """Test complete debugging session."""
        # Create test ML file
        test_file = Path('test_debug.ml')
        test_file.write_text("""
        function factorial(n) {
            if (n <= 1) {
                return 1;
            }
            return n * factorial(n - 1);
        }

        result = factorial(5);
        print(result);
        """)

        # Start DAP server
        dap_server = subprocess.Popen(
            ['python', '-m', 'src.mlpy.debugging.dap_server'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        try:
            # Send initialize request
            self._send_request(dap_server, 'initialize', {})
            response = self._read_response(dap_server)
            assert response['success'] == True

            # Send launch request
            self._send_request(dap_server, 'launch', {
                'program': str(test_file.absolute())
            })
            response = self._read_response(dap_server)
            assert response['success'] == True

            # Set breakpoint
            self._send_request(dap_server, 'setBreakpoints', {
                'source': {'path': str(test_file.absolute())},
                'breakpoints': [{'line': 3}]
            })
            response = self._read_response(dap_server)
            assert response['body']['breakpoints'][0]['verified'] == True

            # Continue execution
            self._send_request(dap_server, 'configurationDone', {})
            self._send_request(dap_server, 'continue', {'threadId': 1})

            # Wait for stopped event
            event = self._read_event(dap_server, timeout=5)
            assert event['event'] == 'stopped'
            assert event['body']['reason'] == 'breakpoint'

            # Get stack trace
            self._send_request(dap_server, 'stackTrace', {'threadId': 1})
            response = self._read_response(dap_server)
            assert len(response['body']['stackFrames']) > 0

        finally:
            dap_server.terminate()
            test_file.unlink()

    def _send_request(self, process, command, args):
        """Send DAP request."""
        message = {
            'type': 'request',
            'seq': 1,
            'command': command,
            'arguments': args
        }

        body = json.dumps(message)
        content_length = len(body.encode('utf-8'))

        header = f'Content-Length: {content_length}\r\n\r\n'
        process.stdin.write(header.encode('utf-8'))
        process.stdin.write(body.encode('utf-8'))
        process.stdin.flush()

    def _read_response(self, process):
        """Read DAP response."""
        # Read Content-Length
        line = process.stdout.readline().decode('utf-8')
        content_length = int(line.split(':')[1].strip())

        # Read empty line
        process.stdout.readline()

        # Read body
        body = process.stdout.read(content_length).decode('utf-8')
        return json.loads(body)

    def _read_event(self, process, timeout=5):
        """Read DAP event."""
        # Similar to _read_response but with timeout
        pass
```

**Test Coverage Goals:**
- ✅ All DAP request handlers (15+ tests)
- ✅ Breakpoint management (5+ tests)
- ✅ Execution control (5+ tests)
- ✅ Variable inspection (5+ tests)
- ✅ Expression evaluation (5+ tests)
- ✅ End-to-end integration (3+ tests)
- **Total:** 40+ tests

---

## Implementation Timeline

| Day | Tasks | Deliverables | Hours |
|-----|-------|--------------|-------|
| **Day 1** | DAP Server Core | MLDebugAdapter class, protocol handlers (initialize, launch) | 6-8 |
| **Day 2** | DAP Request Handlers | Breakpoints, execution control, stack/variables | 6-8 |
| **Day 2-3** | MLDebugger Enhancements | step_into, step_out, get_call_stack, variable access | 2-3 |
| **Day 3** | VS Code Extension | Debug adapter factory, configuration provider | 4-6 |
| **Day 4** | Launch Configurations | Templates, documentation, polish | 3-4 |
| **Day 5** | Unit Tests | DAP protocol tests, debugger enhancement tests | 6-8 |
| **Day 6** | Integration Tests | End-to-end debugging session tests | 4-6 |
| **Day 7** | Documentation & Polish | User guide, troubleshooting, final testing | 4-6 |
| **TOTAL** | **5-7 days** | **Complete Phase 5** | **35-49 hours** |

---

## Success Criteria

### Phase 5 Complete When:

**Core Functionality:**
- [ ] DAP Server responds to all essential requests
- [ ] Breakpoints work (set, verify, hit, clear)
- [ ] Execution control works (continue, next, step in, step out)
- [ ] Stack trace displays ML positions
- [ ] Variable inspection shows correct values
- [ ] Watch expressions work with SafeExpressionEvaluator
- [ ] Conditional breakpoints work
- [ ] Exception breakpoints work

**VS Code Integration:**
- [ ] Debug adapter registers successfully
- [ ] Breakpoint gutter works (red dots)
- [ ] Debug toolbar works (continue, step buttons)
- [ ] Variables panel shows locals/globals
- [ ] Call Stack panel shows ML frames
- [ ] Watch panel evaluates expressions
- [ ] Debug Console works for evaluation
- [ ] Launch configurations work

**Quality:**
- [ ] 40+ tests passing (100%)
- [ ] Documentation complete (user guide + troubleshooting)
- [ ] Zero production overhead (same as Phase 1-4)
- [ ] Works with multi-file projects
- [ ] Handles errors gracefully

**User Experience:**
- [ ] F5 starts debugging immediately
- [ ] Breakpoints are easy to set/remove
- [ ] Variable inspection is intuitive
- [ ] Step buttons work as expected
- [ ] Performance is acceptable (<15% overhead when debugging)

---

## User Guide Addition

### Debugging ML Programs in VS Code

#### Quick Start

1. **Open an ML file** in VS Code
2. **Click in the gutter** next to a line number to set a breakpoint (red dot appears)
3. **Press F5** or select "Run → Start Debugging"
4. **Use debug toolbar** to control execution:
   - Continue (F5)
   - Step Over (F10)
   - Step Into (F11)
   - Step Out (Shift+F11)

#### Launch Configuration

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "ml",
      "request": "launch",
      "name": "Debug ML",
      "program": "${file}"
    }
  ]
}
```

#### Features

**Breakpoints:**
- Click gutter to set/remove
- Right-click breakpoint → "Edit Breakpoint" for conditions
- Example condition: `x > 10`

**Variable Inspection:**
- View locals/globals in Variables panel
- Hover over variables for quick inspection
- Add expressions to Watch panel

**Call Stack:**
- See full ML call stack
- Click frame to inspect variables at that level

**Debug Console:**
- Evaluate ML expressions at current breakpoint
- Example: `x + 5`, `myArray.length`

---

## Risk Assessment

### Risk 1: DAP Protocol Complexity
**Risk:** Implementing full DAP protocol is complex
**Mitigation:**
- Focus on essential requests first (15-20 requests)
- Reference existing DAP implementations (Python debugpy, Node.js)
- Use DAP protocol documentation and test suite
**Likelihood:** Medium

### Risk 2: Threading Issues
**Risk:** Execution thread vs. DAP communication thread conflicts
**Mitigation:**
- Use thread-safe debugger state
- Proper synchronization for breakpoint hits
- Test with concurrent execution scenarios
**Likelihood:** Low (MLDebugger already thread-safe)

### Risk 3: VS Code Integration Issues
**Risk:** Debug adapter not registering or communicating properly
**Mitigation:**
- Follow VS Code debug adapter examples
- Test with VS Code debug adapter tester
- Enable trace logging for diagnostics
**Likelihood:** Low (well-documented pattern)

### Risk 4: Source Map Edge Cases
**Risk:** Stack trace or breakpoints fail for complex ML code
**Mitigation:**
- Leverage existing source map testing (Phase 1.5)
- Add integration tests with complex ML programs
- Ensure all AST nodes have source map entries
**Likelihood:** Low (source maps already working)

---

## References

### Debug Adapter Protocol
- [DAP Specification](https://microsoft.github.io/debug-adapter-protocol/)
- [DAP Overview](https://microsoft.github.io/debug-adapter-protocol/overview)
- [VS Code Debug Extension Guide](https://code.visualstudio.com/api/extension-guides/debugger-extension)

### Example Implementations
- [Python debugpy](https://github.com/microsoft/debugpy) - Reference DAP server
- [Node.js debug adapter](https://github.com/microsoft/vscode-node-debug2)
- [Mock Debug](https://github.com/microsoft/vscode-mock-debug) - VS Code example

### VS Code APIs
- [Debug API](https://code.visualstudio.com/api/references/vscode-api#debug)
- [DebugAdapterDescriptorFactory](https://code.visualstudio.com/api/references/vscode-api#DebugAdapterDescriptorFactory)
- [DebugConfigurationProvider](https://code.visualstudio.com/api/references/vscode-api#DebugConfigurationProvider)

---

## Next Steps

1. **Approve this proposal** - Review and approve Phase 5 plan
2. **Implement Day 1-2** - DAP Server core and request handlers
3. **Test DAP Protocol** - Verify protocol compliance with tests
4. **Implement Day 3-4** - VS Code extension integration
5. **Test End-to-End** - Full debugging session in VS Code
6. **Polish & Document** - User guide and troubleshooting
7. **Release** - Deploy Phase 5 to users

---

**Document Status:** Ready for Implementation
**Estimated Timeline:** 5-7 days
**Dependencies:** Phase 1-4.5 Complete (✅)
**Next Phase:** Phase 6 - Advanced Features (flamegraphs, line-level profiling)
