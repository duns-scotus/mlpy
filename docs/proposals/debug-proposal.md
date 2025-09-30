# ML Language Debugger Implementation Proposal - Enhanced Strategy

## Executive Summary

This enhanced proposal outlines a comprehensive debugging system for the ML language, focusing on **core debugging facilities first** with incremental enhancement toward full IDE integration. The strategy prioritizes immediate developer value through CLI debugging, then builds systematically toward enterprise-grade debugging with VS Code integration and Debug Adapter Protocol (DAP) server support.

## Architecture Decision: Hybrid CLI Integration

### **Recommended Approach: Integrated CLI with Dedicated Debug Sessions**

```bash
mlpy debug main.ml                    # Launch debugging session
[mldb] step                          # Dedicated debugging prompt
[mldb] break main.ml:10              # Debugging-specific commands
[mldb] print variable_name           # Variable inspection
[mldb] quit                          # Return to shell
```

### **Benefits of Hybrid Integration**
- **Consistent Experience**: Follows mlpy CLI patterns (`mlpy run`, `mlpy test`, `mlpy debug`)
- **Shared Infrastructure**: Leverages existing project loading, configuration, error handling
- **Dedicated Debug Environment**: Professional debugging experience once launched
- **Single Tool Maintenance**: One tool to install, configure, and maintain
- **Universal Access**: CLI works in any environment, IDE integration adds convenience

---

## Implementation Strategy - Revised Priorities

### **Phase 1: Source Mapping Foundation** (Days 1-3)
**Priority: CRITICAL - Everything depends on robust source mapping**

#### **Core Focus**
Establish bulletproof bidirectional ML ↔ Python source mapping that forms the foundation for all debugging operations.

#### **Key Components**

**`src/mlpy/debugging/source_mapping.py`**
```python
class SourceMapGenerator:
    """Generates comprehensive debug info during transpilation"""
    def generate_debug_info(self, ml_ast: MLASTNode, python_code: str) -> DebugInfo
    def add_line_mapping(self, ml_line: int, ml_col: int, py_line: int, py_col: int)
    def add_function_mapping(self, ml_func: str, ml_range: Range, py_range: Range)
    def add_variable_mapping(self, ml_name: str, py_name: str, scope: str)
    def mark_breakpoint_location(self, ml_line: int, is_valid: bool)

class SourceMapResolver:
    """Fast bidirectional source location resolution"""
    def ml_to_python(self, ml_file: str, ml_line: int, ml_col: int) -> PythonLocation
    def python_to_ml(self, py_file: str, py_line: int, py_col: int) -> MLLocation
    def get_ml_context(self, py_location: PythonLocation) -> MLContext
    def validate_breakpoint_location(self, ml_file: str, ml_line: int) -> bool
    def get_function_context(self, location: Location) -> FunctionContext
    def get_variable_mapping(self, ml_name: str, context: ExecutionContext) -> str
```

**`src/mlpy/debugging/debug_info.py`**
```python
@dataclass
class DebugInfo:
    """Enhanced debug information format"""
    version: str = "1.0"
    source_files: List[str]
    line_mappings: List[LineMapping]
    function_mappings: List[FunctionMapping]
    variable_mappings: List[VariableMapping]
    breakpoint_locations: List[int]  # Valid ML line numbers
    execution_paths: List[ExecutionPath]  # For step execution

@dataclass
class LineMapping:
    ml_line: int
    ml_column: int
    python_line: int
    python_column: int
    ml_file_index: int
    statement_type: str  # 'expression', 'assignment', 'control_flow'
    is_breakpoint_valid: bool

@dataclass
class FunctionMapping:
    ml_function_name: str
    python_function_name: str
    ml_start_line: int
    ml_end_line: int
    python_start_line: int
    python_end_line: int
    parameters: List[ParameterMapping]
    return_type: str

@dataclass
class VariableMapping:
    ml_name: str
    python_name: str
    scope: str  # 'local', 'global', 'closure'
    ml_type: str
    python_type: str
    is_mutable: bool
```

#### **Transpiler Integration**
```python
# Enhanced python_generator.py
class PythonGenerator:
    def __init__(self, debug_mode: bool = False):
        self.debug_mode = debug_mode
        self.debug_info = DebugInfo() if debug_mode else None
        self.source_map_generator = SourceMapGenerator() if debug_mode else None

    def generate_module(self, ml_module: ModuleNode) -> str:
        python_ast = self._convert_module(ml_module)
        if self.debug_mode:
            self.debug_info = self.source_map_generator.generate_debug_info(
                ml_module, python_ast
            )
            python_code = self._generate_python_code(python_ast)
            # Embed debug info as base64-encoded comment
            return python_code + f"\n# DEBUG_INFO: {self._encode_debug_info()}"
        return self._generate_python_code(python_ast)
```

#### **Success Criteria**
- 100% accurate bidirectional mapping for all ML constructs
- Sub-millisecond lookup performance for location resolution
- Comprehensive test coverage with complex ML programs
- Valid breakpoint location detection with 100% accuracy

---

### **Phase 2: CLI Debugger Core** (Days 4-7)
**Priority: HIGH - Immediate developer value and validation platform**

#### **Core Focus**
Create a professional, interactive CLI debugger that provides immediate debugging capabilities and serves as a testing platform for all debugging features.

#### **Key Components**

**`src/mlpy/debugging/cli_debugger.py`**
```python
class MLDebugger:
    """Main CLI debugger implementation"""
    def __init__(self, ml_file: str, args: List[str] = None, stop_on_entry: bool = False):
        self.ml_file = ml_file
        self.args = args or []
        self.stop_on_entry = stop_on_entry
        self.session = None
        self.command_processor = DebuggerCommandProcessor(self)
        self.source_map = None

    def start_interactive_session(self) -> int:
        """Start interactive debugging session"""

    def load_program(self) -> bool:
        """Load and prepare ML program for debugging"""

    def execute_command(self, command: str) -> DebugResult:
        """Execute debugger command and return result"""

    def show_current_location(self) -> None:
        """Display current execution location with source context"""

    def show_prompt(self) -> str:
        """Display debugger prompt with current state info"""
```

**`src/mlpy/debugging/debugger_commands.py`**
```python
class DebuggerCommandProcessor:
    """Process and execute debugger commands"""
    COMMANDS = {
        # Execution control
        'run': RunCommand,           # Start/restart execution
        'continue': ContinueCommand, # Continue execution
        'step': StepCommand,         # Step one line
        'next': NextCommand,         # Step over function calls
        'finish': FinishCommand,     # Step out of current function
        'until': UntilCommand,       # Continue until line

        # Breakpoints
        'break': BreakCommand,       # Set breakpoint
        'delete': DeleteCommand,     # Delete breakpoint
        'disable': DisableCommand,   # Disable breakpoint
        'enable': EnableCommand,     # Enable breakpoint
        'info': InfoCommand,         # Show breakpoint info

        # Inspection
        'print': PrintCommand,       # Print variable
        'pprint': PrettyPrintCommand,# Pretty print variable
        'list': ListCommand,         # Show source code
        'where': WhereCommand,       # Show call stack
        'up': UpCommand,             # Move up stack frame
        'down': DownCommand,         # Move down stack frame

        # Advanced
        'watch': WatchCommand,       # Watch expression
        'eval': EvalCommand,         # Evaluate expression
        'help': HelpCommand,         # Show help
        'quit': QuitCommand,         # Exit debugger
    }

    def parse_command(self, input_line: str) -> Command:
        """Parse user input into debugger command"""

    def execute_command(self, command: Command) -> CommandResult:
        """Execute parsed command and return result"""

    def get_command_help(self, command_name: str = None) -> str:
        """Get help for specific command or all commands"""

    def handle_autocomplete(self, partial_command: str) -> List[str]:
        """Provide command autocompletion"""
```

**`src/mlpy/debugging/debug_session.py`**
```python
class DebugSession:
    """Core debugging session management"""
    def __init__(self, ml_file: str, source_map: SourceMapResolver):
        self.ml_file = ml_file
        self.source_map = source_map
        self.execution_state = ExecutionState.NOT_STARTED
        self.current_frame = None
        self.call_stack = []
        self.breakpoints = BreakpointManager()
        self.variable_inspector = VariableInspector(source_map)

    def start_execution(self, stop_on_entry: bool = False) -> ExecutionResult:
        """Start ML program execution with debugging"""

    def pause_execution(self) -> ExecutionState:
        """Pause execution at current location"""

    def resume_execution(self) -> ExecutionState:
        """Resume execution until next breakpoint or completion"""

    def step_execution(self, step_type: StepType) -> ExecutionState:
        """Execute single step (line, over, into, out)"""

    def terminate_session(self) -> None:
        """Clean up and end debugging session"""

    def get_current_state(self) -> ExecutionState:
        """Get current execution state and location"""

    def get_call_stack(self) -> List[StackFrame]:
        """Get current call stack with ML context"""

    def set_current_frame(self, frame_index: int) -> bool:
        """Set current frame for variable inspection"""
```

#### **CLI Command Integration**
**`src/mlpy/cli/debug.py`**
```python
class DebugCommand(BaseCommand):
    """CLI debug command implementation"""

    def register_parser(self, subparsers) -> None:
        parser = subparsers.add_parser(
            'debug',
            help='Debug ML programs interactively',
            description='Launch interactive debugging session for ML programs'
        )
        parser.add_argument('source', help='ML source file to debug')
        parser.add_argument('args', nargs='*', help='Arguments to pass to ML program')
        parser.add_argument('--break-on-entry', action='store_true',
                          help='Stop execution at program entry')
        parser.add_argument('--batch', help='Execute debug commands from file')
        parser.add_argument('--dap', action='store_true',
                          help='Start DAP server instead of CLI debugger')
        parser.add_argument('--dap-port', type=int, default=0,
                          help='DAP server port (0 for stdio)')

    def execute(self, args: Any) -> int:
        if args.dap:
            # Start DAP server (Phase 5)
            from ..debugging.dap_server import MLDebugAdapterProtocol
            dap_server = MLDebugAdapterProtocol(
                port=args.dap_port if args.dap_port > 0 else None
            )
            return dap_server.start_server()
        else:
            # Start CLI debugger
            debugger = MLDebugger(
                args.source,
                args.args,
                stop_on_entry=args.break_on_entry
            )
            if args.batch:
                return debugger.execute_batch(args.batch)
            else:
                return debugger.start_interactive_session()
```

#### **Example CLI Session**
```bash
$ mlpy debug examples/calculator.ml
Loading ML program: examples/calculator.ml
ML Debugger v2.0 - Type 'help' for commands

[mldb] break calculator.ml:15
Breakpoint 1 set at calculator.ml:15

[mldb] run
Starting program...
Breakpoint 1 hit at calculator.ml:15 in function calculate()
   13 | function calculate(operation, a, b) {
   14 |     print("Calculating: " + operation);
=> 15 |     if (operation == "add") {
   16 |         return a + b;
   17 |     } elif (operation == "subtract") {

[mldb] print operation
operation = "add" (string)

[mldb] print a, b
a = 10 (number)
b = 5 (number)

[mldb] step
   16 |         return a + b;

[mldb] print a + b
15 (number)

[mldb] continue
Result: 15
Program terminated successfully.

[mldb] quit
```

#### **Success Criteria**
- Functional CLI debugger for basic ML programs
- All essential debugging commands working
- Accurate source location display
- Variable inspection in ML format
- Session lifecycle management

---

### **Phase 3: Runtime Instrumentation** (Days 8-11)
**Priority: HIGH - Core debugging functionality foundation**

#### **Core Focus**
Implement efficient Python runtime instrumentation that enables debugging with minimal performance overhead while providing comprehensive debugging capabilities.

#### **Key Components**

**`src/mlpy/debugging/runtime_hooks.py`**
```python
class DebugRuntimeHooks:
    """Debugging hooks injected into generated Python code"""
    def __init__(self, debug_session: 'DebugSession'):
        self.session = debug_session
        self.breakpoint_manager = debug_session.breakpoints
        self.variable_inspector = debug_session.variable_inspector
        self.call_stack = debug_session.call_stack

    def line_executed(self, ml_file: str, ml_line: int, local_vars: Dict) -> None:
        """Called before each executable ML line"""
        # Check for breakpoints
        if self.breakpoint_manager.should_break_at(ml_file, ml_line, local_vars):
            self._pause_execution(ml_file, ml_line, local_vars)

        # Handle step execution
        if self.session.step_mode != StepMode.NONE:
            self._handle_step_execution(ml_file, ml_line)

    def function_entered(self, ml_func_name: str, py_func_name: str,
                        ml_line: int, args: Dict) -> None:
        """Called when entering ML function"""
        frame = StackFrame(
            ml_function_name=ml_func_name,
            python_function_name=py_func_name,
            ml_line=ml_line,
            arguments=args,
            local_variables={}
        )
        self.call_stack.append(frame)

    def function_exited(self, ml_func_name: str, return_value: Any) -> None:
        """Called when exiting ML function"""
        if self.call_stack:
            frame = self.call_stack.pop()
            frame.return_value = return_value

    def exception_raised(self, exception: Exception, ml_file: str, ml_line: int) -> None:
        """Called when exception occurs in ML code"""
        self.session.handle_exception(exception, ml_file, ml_line)

    def variable_assigned(self, ml_name: str, py_name: str, value: Any,
                         scope: str) -> None:
        """Called when variable is assigned (for watch expressions)"""
        if self.session.has_watch_expression(ml_name):
            self.session.evaluate_watch_expressions()

    def _pause_execution(self, ml_file: str, ml_line: int, local_vars: Dict) -> None:
        """Pause execution and wait for debugger commands"""
        self.session.pause_at_location(ml_file, ml_line, local_vars)

    def _handle_step_execution(self, ml_file: str, ml_line: int) -> None:
        """Handle step mode execution control"""
        if self.session.should_pause_for_step(ml_file, ml_line):
            self.session.pause_for_step(ml_file, ml_line)
```

**`src/mlpy/debugging/instrumentation.py`**
```python
class DebugInstrumentation:
    """Inject debugging hooks into generated Python code"""

    def __init__(self, debug_info: DebugInfo):
        self.debug_info = debug_info

    def inject_debug_hooks(self, python_ast: ast.AST) -> ast.AST:
        """Inject debug hooks into Python AST"""
        # Add debug runtime initialization
        python_ast = self._add_debug_setup(python_ast)

        # Transform all functions to include debug hooks
        python_ast = self._transform_functions(python_ast)

        # Add line hooks to executable statements
        python_ast = self._add_line_hooks(python_ast)

        return python_ast

    def _add_debug_setup(self, module_ast: ast.Module) -> ast.Module:
        """Add debug runtime setup at module level"""
        setup_code = """
# Debug runtime setup
import sys
sys.path.append('{mlpy_path}')
from src.mlpy.debugging.runtime_hooks import DebugRuntimeHooks
from src.mlpy.debugging.debug_session import DebugSession

__debug_session__ = DebugSession.get_current_session()
__debug_hooks__ = DebugRuntimeHooks(__debug_session__) if __debug_session__ else None
        """.strip()

        setup_ast = ast.parse(setup_code)
        module_ast.body = setup_ast.body + module_ast.body
        return module_ast

    def _transform_functions(self, ast_node: ast.AST) -> ast.AST:
        """Add function entry/exit hooks"""
        transformer = FunctionHookTransformer(self.debug_info)
        return transformer.visit(ast_node)

    def _add_line_hooks(self, ast_node: ast.AST) -> ast.AST:
        """Add line execution hooks to statements"""
        transformer = LineHookTransformer(self.debug_info)
        return transformer.visit(ast_node)

class FunctionHookTransformer(ast.NodeTransformer):
    """Transform functions to add entry/exit hooks"""

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        ml_func_info = self.debug_info.get_function_mapping(node.name)
        if not ml_func_info:
            return node

        # Add function entry hook
        entry_hook = self._create_function_entry_hook(ml_func_info, node)

        # Add function exit hook (wrap return statements)
        node = self._add_function_exit_hooks(node, ml_func_info)

        # Insert entry hook at beginning
        node.body.insert(0, entry_hook)

        return node

class LineHookTransformer(ast.NodeTransformer):
    """Add line execution hooks to statements"""

    def visit_stmt(self, node: ast.stmt) -> ast.stmt:
        ml_line = self.debug_info.get_ml_line(node.lineno)
        if ml_line is None:
            return node

        # Create line hook call
        hook_call = ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id='__debug_hooks__', ctx=ast.Load()),
                    attr='line_executed',
                    ctx=ast.Load()
                ),
                args=[
                    ast.Constant(value=self.debug_info.ml_file),
                    ast.Constant(value=ml_line),
                    ast.Call(
                        func=ast.Name(id='locals', ctx=ast.Load()),
                        args=[],
                        keywords=[]
                    )
                ],
                keywords=[]
            )
        )

        # Return compound statement with hook + original
        return [hook_call, node]
```

**`src/mlpy/debugging/variable_inspector.py`**
```python
class VariableInspector:
    """Translate Python runtime state to ML variable representation"""

    def __init__(self, source_map: SourceMapResolver):
        self.source_map = source_map

    def inspect_variable(self, ml_name: str, frame: StackFrame) -> VariableInfo:
        """Get ML representation of variable"""
        py_name = self.source_map.get_python_name(ml_name, frame)
        if not py_name:
            return VariableInfo(ml_name, None, "undefined", "Variable not found")

        py_value = frame.get_variable(py_name)
        ml_value = self.translate_python_to_ml(py_value)

        return VariableInfo(
            ml_name=ml_name,
            ml_value=ml_value,
            ml_type=self.infer_ml_type(ml_value),
            description=self.format_for_display(ml_value)
        )

    def translate_python_to_ml(self, py_value: Any) -> MLValue:
        """Convert Python value to ML representation"""
        if isinstance(py_value, dict) and '_ml_object_type' in py_value:
            # ML object represented as Python dict
            return MLObject(py_value)
        elif isinstance(py_value, list) and hasattr(py_value, '_ml_array_type'):
            # ML array represented as Python list
            return MLArray(py_value)
        elif callable(py_value) and hasattr(py_value, '_ml_function_info'):
            # ML function
            return MLFunction(py_value)
        else:
            # Primitive value
            return MLPrimitive(py_value)

    def enumerate_scope_variables(self, frame: StackFrame, scope: str) -> Dict[str, VariableInfo]:
        """Get all variables in specified scope"""
        variables = {}

        if scope == 'local':
            py_vars = frame.local_variables
        elif scope == 'global':
            py_vars = frame.global_variables
        else:
            return variables

        for py_name, py_value in py_vars.items():
            ml_name = self.source_map.get_ml_name(py_name, frame)
            if ml_name:
                variables[ml_name] = self.inspect_variable(ml_name, frame)

        return variables

    def format_for_display(self, ml_value: MLValue, max_depth: int = 3) -> str:
        """Format ML value for debugger display"""
        if isinstance(ml_value, MLPrimitive):
            return f"{ml_value.value} ({ml_value.type})"
        elif isinstance(ml_value, MLArray):
            if len(ml_value.items) <= 5:
                items = [self.format_for_display(item, max_depth-1) for item in ml_value.items]
                return f"[{', '.join(items)}] (array[{len(ml_value.items)}])"
            else:
                return f"[...{len(ml_value.items)} items...] (array)"
        elif isinstance(ml_value, MLObject):
            if max_depth <= 0:
                return f"{{...}} (object)"
            props = []
            for key, value in list(ml_value.properties.items())[:3]:
                props.append(f"{key}: {self.format_for_display(value, max_depth-1)}")
            if len(ml_value.properties) > 3:
                props.append("...")
            return f"{{{', '.join(props)}}} (object)"
        elif isinstance(ml_value, MLFunction):
            return f"function {ml_value.name}({', '.join(ml_value.parameters)}) (function)"
        else:
            return str(ml_value)
```

**`src/mlpy/debugging/breakpoint_manager.py`**
```python
class BreakpointManager:
    """Manage breakpoint lifecycle and evaluation"""

    def __init__(self):
        self.breakpoints: Dict[int, Breakpoint] = {}
        self.next_id = 1

    def add_breakpoint(self, ml_file: str, ml_line: int, condition: str = None) -> Breakpoint:
        """Add breakpoint at ML location"""
        bp = Breakpoint(
            id=self.next_id,
            ml_file=ml_file,
            ml_line=ml_line,
            condition=condition,
            enabled=True,
            hit_count=0
        )
        self.breakpoints[self.next_id] = bp
        self.next_id += 1
        return bp

    def remove_breakpoint(self, breakpoint_id: int) -> bool:
        """Remove breakpoint by ID"""
        return self.breakpoints.pop(breakpoint_id, None) is not None

    def should_break_at(self, ml_file: str, ml_line: int, local_vars: Dict) -> bool:
        """Check if execution should break at location"""
        for bp in self.breakpoints.values():
            if (bp.enabled and
                bp.ml_file == ml_file and
                bp.ml_line == ml_line):

                if bp.condition:
                    if self.evaluate_condition(bp.condition, local_vars):
                        bp.hit_count += 1
                        return True
                else:
                    bp.hit_count += 1
                    return True

        return False

    def evaluate_condition(self, condition: str, local_vars: Dict) -> bool:
        """Evaluate breakpoint condition"""
        try:
            # Parse and evaluate ML expression in current context
            # This is a simplified version - full implementation in Phase 4
            return eval(condition, {}, local_vars)
        except Exception:
            return False  # Invalid condition defaults to False

    def list_breakpoints(self) -> List[Breakpoint]:
        """Get list of all breakpoints"""
        return list(self.breakpoints.values())
```

#### **Enhanced Code Generation**
```python
# Integration with existing python_generator.py
class PythonGenerator:
    def __init__(self, debug_mode: bool = False):
        self.debug_mode = debug_mode
        self.debug_info = DebugInfo() if debug_mode else None
        self.debug_instrumentation = DebugInstrumentation(self.debug_info) if debug_mode else None

    def generate_function(self, ml_func: FunctionNode) -> ast.FunctionDef:
        python_func = self._convert_function(ml_func)

        if self.debug_mode:
            # Add debug info for function
            self.debug_info.add_function_mapping(
                ml_function_name=ml_func.name,
                python_function_name=python_func.name,
                ml_start_line=ml_func.location.line,
                ml_end_line=ml_func.end_location.line,
                python_start_line=python_func.lineno,
                python_end_line=python_func.end_lineno
            )

        return python_func

    def finalize_module(self, python_ast: ast.Module) -> str:
        if self.debug_mode and self.debug_instrumentation:
            # Inject debug hooks
            python_ast = self.debug_instrumentation.inject_debug_hooks(python_ast)

        python_code = self._ast_to_code(python_ast)

        if self.debug_mode:
            # Embed debug info
            debug_info_json = json.dumps(asdict(self.debug_info), indent=2)
            debug_info_b64 = base64.b64encode(debug_info_json.encode()).decode()
            python_code += f"\n\n# DEBUG_INFO\n# {debug_info_b64}\n"

        return python_code
```

#### **Success Criteria**
- Can step through ML execution with line-by-line precision
- Variables display correctly in ML representation
- Call stack navigation works with ML function context
- <5% performance overhead when debugging enabled
- Breakpoint hit detection is 100% accurate

---

### **Phase 4: Advanced CLI Features** (Days 12-14)
**Priority: MEDIUM - Professional debugging experience**

#### **Core Focus**
Enhance CLI debugger with advanced features that provide a professional debugging experience comparable to established debuggers like GDB or Python's PDB.

#### **Key Components**

**`src/mlpy/debugging/expression_evaluator.py`**
```python
class MLExpressionEvaluator:
    """Evaluate ML expressions in debugging context"""

    def __init__(self, debug_session: 'DebugSession'):
        self.session = debug_session
        self.ml_parser = MLParser()

    def evaluate_expression(self, expr: str, frame: StackFrame) -> EvaluationResult:
        """Evaluate ML expression in current debugging context"""
        try:
            # Parse ML expression
            ml_expr = self.ml_parser.parse_expression(expr)

            # Convert to Python and execute in frame context
            py_code = self._convert_to_python(ml_expr, frame)
            result = self._execute_in_frame_context(py_code, frame)

            # Convert result back to ML representation
            ml_result = self.session.variable_inspector.translate_python_to_ml(result)

            return EvaluationResult(
                success=True,
                result=ml_result,
                ml_type=self._infer_ml_type(ml_result),
                display_value=self._format_result(ml_result)
            )

        except Exception as e:
            return EvaluationResult(
                success=False,
                error=str(e),
                error_type=type(e).__name__
            )

    def _convert_to_python(self, ml_expr: MLExpression, frame: StackFrame) -> str:
        """Convert ML expression to executable Python code"""
        # This uses the same transpilation logic as the main compiler
        # but in expression context with variable name mapping
        converter = ExpressionConverter(self.session.source_map, frame)
        return converter.convert(ml_expr)

    def _execute_in_frame_context(self, py_code: str, frame: StackFrame) -> Any:
        """Execute Python code in frame's variable context"""
        local_vars = frame.local_variables.copy()
        global_vars = frame.global_variables.copy()

        # Execute in isolated context
        result = eval(py_code, global_vars, local_vars)
        return result

    def evaluate_watch_expression(self, watch_expr: WatchExpression,
                                frame: StackFrame) -> WatchResult:
        """Evaluate watch expression and track changes"""
        current_result = self.evaluate_expression(watch_expr.expression, frame)

        # Compare with previous value
        changed = (watch_expr.last_value != current_result.result
                  if watch_expr.last_value is not None else True)

        watch_expr.last_value = current_result.result
        watch_expr.evaluation_count += 1

        return WatchResult(
            expression=watch_expr.expression,
            result=current_result,
            changed=changed,
            evaluation_count=watch_expr.evaluation_count
        )
```

**`src/mlpy/debugging/debug_console.py`**
```python
class DebugConsole:
    """Interactive debugging console with ML REPL capabilities"""

    def __init__(self, debug_session: 'DebugSession'):
        self.session = debug_session
        self.evaluator = MLExpressionEvaluator(debug_session)
        self.history = []
        self.completion_enabled = True

    def start_console_mode(self) -> None:
        """Start interactive console mode within debugger"""
        print("Entering debug console mode. Type 'exit' to return to debugger.")
        print("You can execute ML expressions and statements in the current context.")

        while True:
            try:
                # Get current frame info for prompt
                frame_info = self._get_frame_info()
                prompt = f"(ml-console:{frame_info}) >>> "

                # Read input with history and completion
                user_input = self._read_input_with_completion(prompt)

                if user_input.strip().lower() in ['exit', 'quit']:
                    break

                if user_input.strip() == '':
                    continue

                # Add to history
                self.history.append(user_input)

                # Execute input
                result = self._execute_console_input(user_input)
                self._display_result(result)

            except KeyboardInterrupt:
                print("\nUse 'exit' to leave console mode.")
            except EOFError:
                break

        print("Exiting debug console mode.")

    def _execute_console_input(self, user_input: str) -> ConsoleResult:
        """Execute user input in console"""
        current_frame = self.session.get_current_frame()

        if self._is_expression(user_input):
            # Evaluate as expression
            eval_result = self.evaluator.evaluate_expression(user_input, current_frame)
            return ConsoleResult(
                type='expression',
                success=eval_result.success,
                result=eval_result.result if eval_result.success else None,
                error=eval_result.error if not eval_result.success else None,
                display_value=eval_result.display_value if eval_result.success else None
            )
        else:
            # Execute as statement
            return self._execute_statement(user_input, current_frame)

    def _execute_statement(self, statement: str, frame: StackFrame) -> ConsoleResult:
        """Execute ML statement in current context"""
        try:
            # Parse and transpile ML statement
            ml_stmt = self.session.ml_parser.parse_statement(statement)
            py_code = self._convert_statement_to_python(ml_stmt, frame)

            # Execute in frame context
            local_vars = frame.local_variables.copy()
            global_vars = frame.global_variables.copy()

            exec(py_code, global_vars, local_vars)

            # Update frame variables with any changes
            frame.update_variables(local_vars, global_vars)

            return ConsoleResult(
                type='statement',
                success=True,
                result=None,
                display_value="Statement executed successfully"
            )

        except Exception as e:
            return ConsoleResult(
                type='statement',
                success=False,
                error=str(e),
                error_type=type(e).__name__
            )

    def _handle_autocomplete(self, partial_input: str) -> List[str]:
        """Provide autocompletion for console input"""
        # Complete variable names from current scope
        frame = self.session.get_current_frame()
        completions = []

        # Add local variable names
        for var_name in frame.local_variables.keys():
            ml_name = self.session.source_map.get_ml_name(var_name, frame)
            if ml_name and ml_name.startswith(partial_input):
                completions.append(ml_name)

        # Add ML keywords and built-in functions
        ml_keywords = ['function', 'if', 'else', 'elif', 'while', 'for', 'return', 'true', 'false']
        ml_builtins = ['print', 'typeof', 'length', 'toString']

        for keyword in ml_keywords + ml_builtins:
            if keyword.startswith(partial_input):
                completions.append(keyword)

        return sorted(set(completions))
```

**Enhanced Debugger Commands**
```python
class ConditionalBreakCommand(Command):
    """Set conditional breakpoint: break file:line if condition"""

    def execute(self, args: List[str], debugger: MLDebugger) -> CommandResult:
        if len(args) < 3 or args[1] != 'if':
            return CommandResult(False, "Usage: break location if condition")

        location = args[0]
        condition = ' '.join(args[2:])

        # Parse location (file:line)
        if ':' in location:
            file_part, line_part = location.rsplit(':', 1)
            try:
                line_num = int(line_part)
            except ValueError:
                return CommandResult(False, f"Invalid line number: {line_part}")
        else:
            file_part = debugger.session.ml_file
            try:
                line_num = int(location)
            except ValueError:
                return CommandResult(False, f"Invalid line number: {location}")

        # Validate condition syntax
        try:
            debugger.session.expression_evaluator.parse_ml_expression(condition)
        except Exception as e:
            return CommandResult(False, f"Invalid condition syntax: {e}")

        # Set conditional breakpoint
        bp = debugger.session.breakpoints.add_breakpoint(file_part, line_num, condition)
        return CommandResult(True, f"Conditional breakpoint {bp.id} set at {file_part}:{line_num}")

class WatchCommand(Command):
    """Watch expression: watch expression_name"""

    def execute(self, args: List[str], debugger: MLDebugger) -> CommandResult:
        if not args:
            # List current watch expressions
            watches = debugger.session.get_watch_expressions()
            if not watches:
                return CommandResult(True, "No watch expressions defined")

            output = "Watch expressions:\n"
            for i, watch in enumerate(watches):
                status = "changed" if watch.last_changed else "unchanged"
                output += f"  {i+1}: {watch.expression} = {watch.last_value} ({status})\n"
            return CommandResult(True, output.rstrip())
        else:
            # Add watch expression
            expression = ' '.join(args)
            try:
                watch = debugger.session.add_watch_expression(expression)
                return CommandResult(True, f"Watch expression added: {expression}")
            except Exception as e:
                return CommandResult(False, f"Invalid watch expression: {e}")

class InfoCommand(Command):
    """Show information: info locals|globals|stack|breakpoints"""

    def execute(self, args: List[str], debugger: MLDebugger) -> CommandResult:
        if not args:
            return CommandResult(False, "Usage: info locals|globals|stack|breakpoints")

        info_type = args[0].lower()

        if info_type == 'locals':
            return self._show_local_variables(debugger)
        elif info_type == 'globals':
            return self._show_global_variables(debugger)
        elif info_type == 'stack':
            return self._show_call_stack(debugger)
        elif info_type == 'breakpoints':
            return self._show_breakpoints(debugger)
        else:
            return CommandResult(False, f"Unknown info type: {info_type}")

    def _show_local_variables(self, debugger: MLDebugger) -> CommandResult:
        frame = debugger.session.get_current_frame()
        variables = debugger.session.variable_inspector.enumerate_scope_variables(frame, 'local')

        if not variables:
            return CommandResult(True, "No local variables")

        output = "Local variables:\n"
        for name, var_info in variables.items():
            output += f"  {name} = {var_info.description}\n"
        return CommandResult(True, output.rstrip())
```

#### **Success Criteria**
- Conditional breakpoints work correctly
- Expression evaluation handles complex ML expressions
- Watch expressions track variable changes
- Debug console provides REPL-like experience
- Advanced commands provide comprehensive debugging info

---

### **Phase 5: DAP Server Foundation** (Days 15-18)
**Priority: MEDIUM - Universal IDE integration infrastructure**

#### **Core Focus**
Implement Debug Adapter Protocol (DAP) server that provides standardized debugging interface for universal IDE support, building on the robust CLI debugging foundation.

#### **Key Components**

**`src/mlpy/debugging/dap_server.py`**
```python
class MLDebugAdapterProtocol:
    """Debug Adapter Protocol server for ML debugging"""

    def __init__(self, port: int = None):
        self.port = port  # None for stdio mode
        self.input_stream = None
        self.output_stream = None
        self.debug_session = None
        self.request_handlers = DAPRequestHandlerRegistry()
        self.sequence_number = 1
        self.is_running = False

    def start_server(self) -> int:
        """Start DAP server (stdio or TCP mode)"""
        try:
            if self.port is None:
                # STDIO mode for VS Code integration
                self.input_stream = sys.stdin.buffer
                self.output_stream = sys.stdout.buffer
                self._log("Starting ML DAP server in stdio mode")
            else:
                # TCP mode for debugging and other IDEs
                self._start_tcp_server()
                self._log(f"Starting ML DAP server on port {self.port}")

            self._run_message_loop()
            return 0

        except Exception as e:
            self._log(f"DAP server error: {e}")
            return 1

    def _run_message_loop(self) -> None:
        """Main message processing loop"""
        self.is_running = True

        while self.is_running:
            try:
                # Read DAP message
                message = self._read_dap_message()
                if message is None:
                    break

                # Process message
                response = self._process_message(message)

                # Send response if needed
                if response:
                    self._send_dap_message(response)

            except Exception as e:
                self._log(f"Message processing error: {e}")
                self._send_error_response(f"Internal error: {e}")

    def _process_message(self, message: DAPMessage) -> Optional[DAPMessage]:
        """Process incoming DAP message"""
        self._log(f"Received: {message.command}")

        if message.type == 'request':
            return self._handle_request(message)
        elif message.type == 'response':
            return self._handle_response(message)
        else:
            self._log(f"Unknown message type: {message.type}")
            return None

    def _handle_request(self, request: DAPRequest) -> DAPResponse:
        """Handle DAP request"""
        handler = self.request_handlers.get_handler(request.command)
        if handler:
            try:
                return handler.handle(request, self.debug_session)
            except Exception as e:
                return self._create_error_response(request, str(e))
        else:
            return self._create_error_response(request, f"Unknown command: {request.command}")

    def send_event(self, event: DAPEvent) -> None:
        """Send DAP event to client"""
        self._send_dap_message(event)

    def shutdown(self) -> None:
        """Shutdown DAP server"""
        self.is_running = False
        if self.debug_session:
            self.debug_session.terminate_session()
```

**`src/mlpy/debugging/dap_handlers.py`**
```python
class DAPRequestHandlerRegistry:
    """Registry for DAP request handlers"""

    def __init__(self):
        self.handlers = {
            'initialize': InitializeHandler(),
            'launch': LaunchHandler(),
            'attach': AttachHandler(),
            'setBreakpoints': SetBreakpointsHandler(),
            'continue': ContinueHandler(),
            'next': NextHandler(),
            'stepIn': StepInHandler(),
            'stepOut': StepOutHandler(),
            'pause': PauseHandler(),
            'stackTrace': StackTraceHandler(),
            'scopes': ScopesHandler(),
            'variables': VariablesHandler(),
            'evaluate': EvaluateHandler(),
            'disconnect': DisconnectHandler(),
            'terminate': TerminateHandler(),
        }

    def get_handler(self, command: str) -> Optional[DAPRequestHandler]:
        return self.handlers.get(command)

class InitializeHandler(DAPRequestHandler):
    """Handle DAP initialize request"""

    def handle(self, request: DAPRequest, session: DebugSession) -> DAPResponse:
        capabilities = {
            'supportsConfigurationDoneRequest': True,
            'supportsFunctionBreakpoints': False,
            'supportsConditionalBreakpoints': True,
            'supportsHitConditionalBreakpoints': False,
            'supportsEvaluateForHovers': True,
            'exceptionBreakpointFilters': [],
            'supportsStepBack': False,
            'supportsSetVariable': False,
            'supportsRestartFrame': False,
            'supportsGotoTargetsRequest': False,
            'supportsStepInTargetsRequest': False,
            'supportsCompletionsRequest': True,
            'completionTriggerCharacters': ['.', '['],
            'supportsModulesRequest': False,
            'additionalModuleColumns': [],
            'supportedChecksumAlgorithms': [],
            'supportsRestartRequest': False,
            'supportsExceptionOptions': False,
            'supportsValueFormattingOptions': True,
            'supportsExceptionInfoRequest': False,
            'supportTerminateDebuggee': True,
            'supportSuspendDebuggee': True,
            'supportsDelayedStackTraceLoading': False,
            'supportsLoadedSourcesRequest': False,
            'supportsLogPoints': False,
            'supportsTerminateThreadsRequest': False,
            'supportsSetExpression': False,
            'supportsTerminateRequest': True,
            'supportsDataBreakpoints': False,
            'supportsReadMemoryRequest': False,
            'supportsWriteMemoryRequest': False,
            'supportsDisassembleRequest': False,
            'supportsCancelRequest': False,
            'supportsBreakpointLocationsRequest': True,
            'supportsClipboardContext': False,
            'supportsSteppingGranularity': False,
            'supportsInstructionBreakpoints': False,
            'supportsExceptionFilterOptions': False,
            'supportsSingleThreadExecutionRequests': False
        }

        return DAPResponse(
            request_seq=request.seq,
            success=True,
            command=request.command,
            body=capabilities
        )

class LaunchHandler(DAPRequestHandler):
    """Handle DAP launch request"""

    def handle(self, request: DAPRequest, session: DebugSession) -> DAPResponse:
        args = request.arguments

        # Extract launch configuration
        ml_program = args.get('program')
        ml_args = args.get('args', [])
        stop_on_entry = args.get('stopOnEntry', False)
        capabilities = args.get('capabilities', [])

        if not ml_program:
            return DAPResponse(
                request_seq=request.seq,
                success=False,
                command=request.command,
                message="Missing 'program' in launch configuration"
            )

        try:
            # Create debug session
            session = DebugSession(ml_program)
            session.set_capabilities(capabilities)

            # Start debugging
            session.start_execution(stop_on_entry=stop_on_entry)

            # Send initialized event
            self._send_initialized_event()

            return DAPResponse(
                request_seq=request.seq,
                success=True,
                command=request.command
            )

        except Exception as e:
            return DAPResponse(
                request_seq=request.seq,
                success=False,
                command=request.command,
                message=f"Failed to launch program: {e}"
            )

class SetBreakpointsHandler(DAPRequestHandler):
    """Handle DAP setBreakpoints request"""

    def handle(self, request: DAPRequest, session: DebugSession) -> DAPResponse:
        args = request.arguments
        source = args.get('source', {})
        lines = args.get('lines', [])
        breakpoints = args.get('breakpoints', [])

        source_path = source.get('path')
        if not source_path:
            return DAPResponse(
                request_seq=request.seq,
                success=False,
                command=request.command,
                message="Missing source path"
            )

        # Clear existing breakpoints for this file
        session.breakpoints.clear_file_breakpoints(source_path)

        # Set new breakpoints
        result_breakpoints = []
        for i, line in enumerate(lines):
            bp_info = breakpoints[i] if i < len(breakpoints) else {}
            condition = bp_info.get('condition')

            # Validate breakpoint location
            if session.source_map.validate_breakpoint_location(source_path, line):
                bp = session.breakpoints.add_breakpoint(source_path, line, condition)
                result_breakpoints.append({
                    'id': bp.id,
                    'verified': True,
                    'line': line,
                    'source': source
                })
            else:
                result_breakpoints.append({
                    'verified': False,
                    'line': line,
                    'message': 'Invalid breakpoint location'
                })

        return DAPResponse(
            request_seq=request.seq,
            success=True,
            command=request.command,
            body={'breakpoints': result_breakpoints}
        )

class StackTraceHandler(DAPRequestHandler):
    """Handle DAP stackTrace request"""

    def handle(self, request: DAPRequest, session: DebugSession) -> DAPResponse:
        args = request.arguments
        thread_id = args.get('threadId')
        start_frame = args.get('startFrame', 0)
        levels = args.get('levels', 0)

        try:
            call_stack = session.get_call_stack()

            # Apply pagination
            if levels > 0:
                stack_frames = call_stack[start_frame:start_frame + levels]
            else:
                stack_frames = call_stack[start_frame:]

            # Convert to DAP format
            dap_frames = []
            for i, frame in enumerate(stack_frames):
                dap_frame = {
                    'id': start_frame + i,
                    'name': frame.ml_function_name,
                    'source': {
                        'name': os.path.basename(frame.ml_file),
                        'path': frame.ml_file
                    },
                    'line': frame.ml_line,
                    'column': 1
                }
                dap_frames.append(dap_frame)

            return DAPResponse(
                request_seq=request.seq,
                success=True,
                command=request.command,
                body={
                    'stackFrames': dap_frames,
                    'totalFrames': len(call_stack)
                }
            )

        except Exception as e:
            return DAPResponse(
                request_seq=request.seq,
                success=False,
                command=request.command,
                message=f"Failed to get stack trace: {e}"
            )
```

**`src/mlpy/debugging/dap_types.py`**
```python
@dataclass
class DAPMessage:
    """Base DAP message"""
    seq: int
    type: str  # 'request', 'response', 'event'

@dataclass
class DAPRequest(DAPMessage):
    """DAP request message"""
    command: str
    arguments: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self.type = 'request'

@dataclass
class DAPResponse(DAPMessage):
    """DAP response message"""
    request_seq: int
    success: bool
    command: str
    message: str = ""
    body: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self.type = 'response'

@dataclass
class DAPEvent(DAPMessage):
    """DAP event message"""
    event: str
    body: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self.type = 'event'

# ML-specific launch configuration
@dataclass
class MLLaunchConfiguration:
    """ML debugging launch configuration"""
    program: str
    args: List[str] = field(default_factory=list)
    stop_on_entry: bool = False
    capabilities: List[str] = field(default_factory=list)
    sandbox_config: Dict[str, Any] = field(default_factory=dict)
    working_directory: str = ""
    environment_variables: Dict[str, str] = field(default_factory=dict)
```

#### **Enhanced CLI Integration**
```python
# Updated debug command to support DAP mode
class DebugCommand(BaseCommand):
    """Enhanced debug command with DAP support"""

    def register_parser(self, subparsers) -> None:
        parser = subparsers.add_parser(
            'debug',
            help='Debug ML programs',
            description='Launch debugging session (CLI or DAP server)'
        )
        parser.add_argument('source', nargs='?', help='ML source file to debug')
        parser.add_argument('args', nargs='*', help='Arguments to pass to ML program')

        # CLI debugging options
        parser.add_argument('--break-on-entry', action='store_true',
                          help='Stop execution at program entry')
        parser.add_argument('--batch', help='Execute debug commands from file')

        # DAP server options
        parser.add_argument('--dap', action='store_true',
                          help='Start DAP server for IDE integration')
        parser.add_argument('--dap-port', type=int, default=0,
                          help='DAP server port (0 for stdio)')
        parser.add_argument('--dap-log-file', help='DAP server log file')

    def execute(self, args: Any) -> int:
        if args.dap:
            # Start DAP server
            from ..debugging.dap_server import MLDebugAdapterProtocol
            dap_server = MLDebugAdapterProtocol(
                port=args.dap_port if args.dap_port > 0 else None
            )

            if args.dap_log_file:
                dap_server.set_log_file(args.dap_log_file)

            return dap_server.start_server()
        else:
            # Start CLI debugger
            if not args.source:
                print("Error: source file required for CLI debugging")
                return 1

            debugger = MLDebugger(
                args.source,
                args.args,
                stop_on_entry=args.break_on_entry
            )

            if args.batch:
                return debugger.execute_batch(args.batch)
            else:
                return debugger.start_interactive_session()
```

#### **Success Criteria**
- DAP server responds correctly to all standard protocol messages
- Can launch debugging session via DAP from command line
- Protocol compliance validated with DAP client testing tools
- Basic IDE communication established and functional

---

### **Phase 6: VS Code Integration** (Days 19-21)
**Priority: MEDIUM - Primary IDE integration for enhanced developer experience**

#### **Core Focus**
Enhance existing VS Code extension with comprehensive debugging support, providing native debugging experience that leverages all the debugging infrastructure built in previous phases.

#### **VS Code Extension Enhancement**

**Enhanced `ext/vscode/package.json`**
```json
{
  "contributes": {
    "debuggers": [{
      "type": "ml",
      "label": "ML",
      "program": "./out/debug/mlDebugAdapter.js",
      "runtime": "node",
      "configurationAttributes": {
        "launch": {
          "required": ["program"],
          "properties": {
            "program": {
              "type": "string",
              "description": "Absolute path to the ML file to debug",
              "default": "${workspaceFolder}/main.ml"
            },
            "args": {
              "type": "array",
              "description": "Command line arguments passed to the program",
              "default": []
            },
            "stopOnEntry": {
              "type": "boolean",
              "description": "Automatically stop after launch",
              "default": false
            },
            "capabilities": {
              "type": "array",
              "description": "ML capabilities required by the program",
              "items": {"type": "string"},
              "default": []
            },
            "workingDirectory": {
              "type": "string",
              "description": "Working directory for program execution",
              "default": "${workspaceFolder}"
            },
            "sandbox": {
              "type": "object",
              "description": "Sandbox configuration",
              "properties": {
                "enabled": {"type": "boolean", "default": true},
                "maxMemoryMB": {"type": "number", "default": 100},
                "maxCpuTimeSeconds": {"type": "number", "default": 30},
                "networkAccess": {"type": "boolean", "default": false}
              },
              "default": {"enabled": true, "maxMemoryMB": 100}
            },
            "profiling": {
              "type": "object",
              "description": "Profiling configuration",
              "properties": {
                "enabled": {"type": "boolean", "default": false},
                "memoryTracking": {"type": "boolean", "default": true},
                "performanceAnalysis": {"type": "boolean", "default": true}
              },
              "default": {"enabled": false}
            },
            "trace": {
              "type": "boolean",
              "description": "Enable debug adapter trace logging",
              "default": false
            }
          }
        },
        "attach": {
          "required": ["port"],
          "properties": {
            "port": {
              "type": "number",
              "description": "Port to attach to running ML debug server",
              "default": 2087
            },
            "host": {
              "type": "string",
              "description": "Host to connect to",
              "default": "localhost"
            }
          }
        }
      },
      "initialConfigurations": [
        {
          "type": "ml",
          "request": "launch",
          "name": "Debug ML Program",
          "program": "${workspaceFolder}/main.ml",
          "stopOnEntry": false,
          "capabilities": [],
          "sandbox": {
            "enabled": true,
            "maxMemoryMB": 100,
            "maxCpuTimeSeconds": 30
          }
        }
      ],
      "configurationSnippets": [
        {
          "label": "ML: Launch Program",
          "description": "Debug an ML program",
          "body": {
            "type": "ml",
            "request": "launch",
            "name": "Debug ML Program",
            "program": "^\"\\${workspaceFolder}/\\${1:main.ml}\"",
            "stopOnEntry": false
          }
        },
        {
          "label": "ML: Launch with Capabilities",
          "description": "Debug ML program with specific capabilities",
          "body": {
            "type": "ml",
            "request": "launch",
            "name": "Debug ML Program (with capabilities)",
            "program": "^\"\\${workspaceFolder}/\\${1:main.ml}\"",
            "capabilities": ["^\"\\${2:file:read:source}\""],
            "stopOnEntry": false
          }
        }
      ]
    }],
    "breakpoints": [{
      "language": "ml"
    }],
    "commands": [
      {
        "command": "ml.debug.startDebugging",
        "title": "Start Debugging",
        "category": "ML Debug"
      },
      {
        "command": "ml.debug.runToCursor",
        "title": "Run to Cursor",
        "category": "ML Debug"
      },
      {
        "command": "ml.debug.toggleBreakpoint",
        "title": "Toggle Breakpoint",
        "category": "ML Debug"
      }
    ],
    "menus": {
      "editor/context": [
        {
          "when": "resourceLangId == ml && !inDebugMode",
          "command": "ml.debug.startDebugging",
          "group": "ml@5"
        },
        {
          "when": "resourceLangId == ml && inDebugMode",
          "command": "ml.debug.runToCursor",
          "group": "ml@6"
        },
        {
          "when": "resourceLangId == ml",
          "command": "ml.debug.toggleBreakpoint",
          "group": "ml@7"
        }
      ]
    },
    "keybindings": [
      {
        "command": "ml.debug.startDebugging",
        "key": "f5",
        "when": "resourceLangId == ml && !inDebugMode"
      },
      {
        "command": "ml.debug.toggleBreakpoint",
        "key": "f9",
        "when": "resourceLangId == ml"
      }
    ]
  }
}
```

**`ext/vscode/src/debug/mlDebugAdapter.ts`**
```typescript
import * as vscode from 'vscode';
import { spawn, ChildProcess } from 'child_process';
import * as path from 'path';

export class MLDebugAdapterFactory implements vscode.DebugAdapterDescriptorFactory {

    createDebugAdapterDescriptor(
        session: vscode.DebugSession,
        executable: vscode.DebugAdapterExecutable | undefined
    ): vscode.ProviderResult<vscode.DebugAdapterDescriptor> {

        // Get workspace root to find mlpy CLI
        const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
        if (!workspaceFolder) {
            throw new Error('No workspace folder found');
        }

        const workspaceRoot = workspaceFolder.uri.fsPath;
        const pythonPath = this.getPythonPath();

        // Start DAP server using mlpy CLI
        const dapServerArgs = [
            '-m', 'src.mlpy.cli.main',
            'debug',
            '--dap'
        ];

        // Add trace logging if enabled
        if (session.configuration.trace) {
            const logFile = path.join(workspaceRoot, '.vscode', 'ml-debug.log');
            dapServerArgs.push('--dap-log-file', logFile);
        }

        return new vscode.DebugAdapterExecutable(pythonPath, dapServerArgs, {
            cwd: workspaceRoot,
            env: {
                ...process.env,
                PYTHONPATH: workspaceRoot
            }
        });
    }

    private getPythonPath(): string {
        // Try to get Python path from VS Code Python extension
        const pythonConfig = vscode.workspace.getConfiguration('python');
        const pythonPath = pythonConfig.get<string>('defaultInterpreterPath') ||
                          pythonConfig.get<string>('pythonPath') ||
                          'python';
        return pythonPath;
    }
}

export class MLDebugConfigurationProvider implements vscode.DebugConfigurationProvider {

    /**
     * Resolve debug configuration before debugging starts
     */
    resolveDebugConfiguration(
        folder: vscode.WorkspaceFolder | undefined,
        config: vscode.DebugConfiguration,
        token?: vscode.CancellationToken
    ): vscode.ProviderResult<vscode.DebugConfiguration> {

        // If no configuration provided, create default
        if (!config.type && !config.request && !config.name) {
            const editor = vscode.window.activeTextEditor;
            if (editor && editor.document.languageId === 'ml') {
                config.type = 'ml';
                config.name = 'Debug ML Program';
                config.request = 'launch';
                config.program = editor.document.fileName;
                config.stopOnEntry = false;
            }
        }

        // Resolve program path
        if (config.program) {
            config.program = this.resolvePath(config.program, folder);
        }

        // Resolve working directory
        if (config.workingDirectory) {
            config.workingDirectory = this.resolvePath(config.workingDirectory, folder);
        } else if (folder) {
            config.workingDirectory = folder.uri.fsPath;
        }

        // Validate configuration
        if (!config.program) {
            vscode.window.showErrorMessage('Cannot debug: no ML program specified');
            return undefined;
        }

        if (!require('fs').existsSync(config.program)) {
            vscode.window.showErrorMessage(`Cannot debug: ML program '${config.program}' does not exist`);
            return undefined;
        }

        return config;
    }

    /**
     * Provide initial debug configurations
     */
    provideDebugConfigurations(
        folder: vscode.WorkspaceFolder | undefined,
        token?: vscode.CancellationToken
    ): vscode.ProviderResult<vscode.DebugConfiguration[]> {

        const configs: vscode.DebugConfiguration[] = [
            {
                type: 'ml',
                request: 'launch',
                name: 'Debug ML Program',
                program: '${workspaceFolder}/main.ml',
                stopOnEntry: false,
                capabilities: []
            },
            {
                type: 'ml',
                request: 'launch',
                name: 'Debug Current File',
                program: '${file}',
                stopOnEntry: false,
                capabilities: []
            },
            {
                type: 'ml',
                request: 'launch',
                name: 'Debug with Sandbox',
                program: '${workspaceFolder}/main.ml',
                stopOnEntry: false,
                sandbox: {
                    enabled: true,
                    maxMemoryMB: 50,
                    maxCpuTimeSeconds: 15,
                    networkAccess: false
                }
            }
        ];

        return configs;
    }

    private resolvePath(filePath: string, folder: vscode.WorkspaceFolder | undefined): string {
        if (path.isAbsolute(filePath)) {
            return filePath;
        }

        if (folder) {
            return path.join(folder.uri.fsPath, filePath);
        }

        return filePath;
    }
}
```

**`ext/vscode/src/debug/mlDebugCommands.ts`**
```typescript
import * as vscode from 'vscode';

export class MLDebugCommands {

    static register(context: vscode.ExtensionContext): void {

        // Start debugging command
        const startDebuggingCommand = vscode.commands.registerCommand(
            'ml.debug.startDebugging',
            () => this.startDebugging()
        );

        // Run to cursor command
        const runToCursorCommand = vscode.commands.registerCommand(
            'ml.debug.runToCursor',
            () => this.runToCursor()
        );

        // Toggle breakpoint command
        const toggleBreakpointCommand = vscode.commands.registerCommand(
            'ml.debug.toggleBreakpoint',
            () => this.toggleBreakpoint()
        );

        context.subscriptions.push(
            startDebuggingCommand,
            runToCursorCommand,
            toggleBreakpointCommand
        );
    }

    private static async startDebugging(): Promise<void> {
        const editor = vscode.window.activeTextEditor;
        if (!editor || editor.document.languageId !== 'ml') {
            vscode.window.showWarningMessage('Please open an ML file to start debugging');
            return;
        }

        // Check if launch.json exists, if not create one
        const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
        if (workspaceFolder) {
            const launchJsonPath = path.join(workspaceFolder.uri.fsPath, '.vscode', 'launch.json');
            if (!require('fs').existsSync(launchJsonPath)) {
                await this.createLaunchJson(workspaceFolder);
            }
        }

        // Start debugging with default configuration
        const debugConfig: vscode.DebugConfiguration = {
            type: 'ml',
            name: 'Debug Current File',
            request: 'launch',
            program: editor.document.fileName,
            stopOnEntry: false
        };

        await vscode.debug.startDebugging(workspaceFolder, debugConfig);
    }

    private static async runToCursor(): Promise<void> {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            return;
        }

        const activeSession = vscode.debug.activeDebugSession;
        if (!activeSession) {
            vscode.window.showWarningMessage('No active debugging session');
            return;
        }

        // Set temporary breakpoint at cursor position
        const line = editor.selection.active.line + 1; // VS Code lines are 0-based
        const uri = editor.document.uri;

        // This will be handled by the debug adapter
        await vscode.commands.executeCommand('editor.debug.action.runToCursor');
    }

    private static async toggleBreakpoint(): Promise<void> {
        await vscode.commands.executeCommand('editor.debug.action.toggleBreakpoint');
    }

    private static async createLaunchJson(workspaceFolder: vscode.WorkspaceFolder): Promise<void> {
        const vscodeDir = path.join(workspaceFolder.uri.fsPath, '.vscode');
        const launchJsonPath = path.join(vscodeDir, 'launch.json');

        // Create .vscode directory if it doesn't exist
        if (!require('fs').existsSync(vscodeDir)) {
            require('fs').mkdirSync(vscodeDir, { recursive: true });
        }

        const launchConfig = {
            version: "0.2.0",
            configurations: [
                {
                    type: "ml",
                    request: "launch",
                    name: "Debug ML Program",
                    program: "${workspaceFolder}/main.ml",
                    stopOnEntry: false,
                    capabilities: []
                }
            ]
        };

        require('fs').writeFileSync(launchJsonPath, JSON.stringify(launchConfig, null, 2));

        // Open launch.json for editing
        const doc = await vscode.workspace.openTextDocument(launchJsonPath);
        await vscode.window.showTextDocument(doc);
    }
}
```

**Enhanced Main Extension File `ext/vscode/src/extension.ts`**
```typescript
// Add to existing extension.ts

import { MLDebugAdapterFactory, MLDebugConfigurationProvider } from './debug/mlDebugAdapter';
import { MLDebugCommands } from './debug/mlDebugCommands';

export async function activate(context: vscode.ExtensionContext) {
    // ... existing activation code ...

    // Register debug adapter factory
    const debugAdapterFactory = new MLDebugAdapterFactory();
    context.subscriptions.push(
        vscode.debug.registerDebugAdapterDescriptorFactory('ml', debugAdapterFactory)
    );

    // Register debug configuration provider
    const debugConfigProvider = new MLDebugConfigurationProvider();
    context.subscriptions.push(
        vscode.debug.registerDebugConfigurationProvider('ml', debugConfigProvider)
    );

    // Register debug commands
    MLDebugCommands.register(context);

    // ... rest of existing activation code ...
}
```

#### **Debug Launch Configurations**

**`.vscode/launch.json` Templates**
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "ml",
            "request": "launch",
            "name": "Debug ML Program",
            "program": "${workspaceFolder}/main.ml",
            "stopOnEntry": false,
            "capabilities": ["file:read:source"]
        },
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
            "name": "Debug with Arguments",
            "program": "${workspaceFolder}/calculator.ml",
            "args": ["add", "10", "5"],
            "stopOnEntry": false
        },
        {
            "type": "ml",
            "request": "launch",
            "name": "Debug in Sandbox",
            "program": "${workspaceFolder}/main.ml",
            "sandbox": {
                "enabled": true,
                "maxMemoryMB": 50,
                "maxCpuTimeSeconds": 15,
                "networkAccess": false
            },
            "stopOnEntry": true
        },
        {
            "type": "ml",
            "request": "attach",
            "name": "Attach to ML Debug Server",
            "port": 2087,
            "host": "localhost"
        }
    ]
}
```

#### **User Experience Features**

1. **One-Click Debugging**
   - F5 starts debugging current ML file
   - Automatic launch.json creation
   - Smart default configurations

2. **Breakpoint Management**
   - F9 toggles breakpoints
   - Conditional breakpoint support
   - Breakpoint validation

3. **Debug Views Integration**
   - Variables view shows ML variables in native format
   - Call stack displays ML function names
   - Watch expressions support ML syntax

4. **Debug Console**
   - Evaluate ML expressions
   - Execute ML statements
   - Access debugging commands

#### **Success Criteria**
- One-click debugging from VS Code (F5)
- Breakpoints work correctly in ML source files
- Variables display in VS Code Variables view with ML formatting
- Step execution works with ML semantic granularity
- Debug console allows ML expression evaluation

---

### **Phase 7: Advanced Features** (Days 22-25)
**Priority: LOW - Enterprise-grade debugging enhancements**

#### **Core Focus**
Add enterprise-grade debugging features that provide production-level debugging capabilities including performance profiling, advanced breakpoint types, and comprehensive debugging analytics.

#### **Key Components**

**`src/mlpy/debugging/profiler.py`**
```python
class MLDebugProfiler:
    """Real-time performance profiling during debugging"""

    def __init__(self, debug_session: 'DebugSession'):
        self.session = debug_session
        self.profiling_enabled = False
        self.function_metrics = {}
        self.line_metrics = {}
        self.memory_tracking = {}
        self.start_time = None

    def start_profiling(self) -> None:
        """Start performance profiling"""
        self.profiling_enabled = True
        self.start_time = time.perf_counter()
        self.function_metrics.clear()
        self.line_metrics.clear()
        self.memory_tracking.clear()

    def stop_profiling(self) -> ProfilingReport:
        """Stop profiling and generate report"""
        self.profiling_enabled = False
        total_time = time.perf_counter() - self.start_time if self.start_time else 0

        return ProfilingReport(
            total_execution_time=total_time,
            function_metrics=self.function_metrics.copy(),
            line_metrics=self.line_metrics.copy(),
            memory_metrics=self.memory_tracking.copy(),
            hotspots=self._identify_hotspots()
        )

    def record_function_entry(self, func_name: str, ml_line: int) -> None:
        """Record function entry for profiling"""
        if not self.profiling_enabled:
            return

        if func_name not in self.function_metrics:
            self.function_metrics[func_name] = FunctionMetrics(
                name=func_name,
                call_count=0,
                total_time=0.0,
                min_time=float('inf'),
                max_time=0.0,
                entry_line=ml_line
            )

        metrics = self.function_metrics[func_name]
        metrics.call_count += 1
        metrics.last_entry_time = time.perf_counter()

    def record_function_exit(self, func_name: str, return_value: Any) -> None:
        """Record function exit for profiling"""
        if not self.profiling_enabled or func_name not in self.function_metrics:
            return

        metrics = self.function_metrics[func_name]
        if hasattr(metrics, 'last_entry_time'):
            execution_time = time.perf_counter() - metrics.last_entry_time
            metrics.total_time += execution_time
            metrics.min_time = min(metrics.min_time, execution_time)
            metrics.max_time = max(metrics.max_time, execution_time)

    def record_line_execution(self, ml_file: str, ml_line: int) -> None:
        """Record line execution for hotspot analysis"""
        if not self.profiling_enabled:
            return

        line_key = f"{ml_file}:{ml_line}"
        if line_key not in self.line_metrics:
            self.line_metrics[line_key] = LineMetrics(
                file=ml_file,
                line=ml_line,
                hit_count=0,
                total_time=0.0
            )

        self.line_metrics[line_key].hit_count += 1
        self.line_metrics[line_key].last_hit_time = time.perf_counter()

    def record_memory_usage(self, context: str) -> None:
        """Record memory usage at specific points"""
        if not self.profiling_enabled:
            return

        try:
            import psutil
            process = psutil.Process()
            memory_info = process.memory_info()

            self.memory_tracking[context] = MemorySnapshot(
                timestamp=time.perf_counter(),
                rss_bytes=memory_info.rss,
                vms_bytes=memory_info.vms,
                context=context
            )
        except ImportError:
            pass  # psutil not available

    def _identify_hotspots(self) -> List[Hotspot]:
        """Identify performance hotspots"""
        hotspots = []

        # Function hotspots (by total time)
        for func_name, metrics in self.function_metrics.items():
            if metrics.total_time > 0.1:  # Functions taking > 100ms
                hotspots.append(Hotspot(
                    type='function',
                    location=f"function {func_name}",
                    metric_value=metrics.total_time,
                    metric_type='total_time',
                    severity='high' if metrics.total_time > 1.0 else 'medium'
                ))

        # Line hotspots (by hit count)
        for line_key, metrics in self.line_metrics.items():
            if metrics.hit_count > 1000:  # Lines executed > 1000 times
                hotspots.append(Hotspot(
                    type='line',
                    location=line_key,
                    metric_value=metrics.hit_count,
                    metric_type='hit_count',
                    severity='high' if metrics.hit_count > 10000 else 'medium'
                ))

        return sorted(hotspots, key=lambda h: h.metric_value, reverse=True)
```

**`src/mlpy/debugging/capability_monitor.py`**
```python
class CapabilityMonitor:
    """Monitor capability usage during debugging"""

    def __init__(self, debug_session: 'DebugSession'):
        self.session = debug_session
        self.capability_usage = {}
        self.security_events = []
        self.monitoring_enabled = True

    def record_capability_usage(self, capability: str, operation: str,
                              location: MLLocation, granted: bool) -> None:
        """Record capability usage event"""
        if not self.monitoring_enabled:
            return

        event = CapabilityUsageEvent(
            timestamp=time.time(),
            capability=capability,
            operation=operation,
            location=location,
            granted=granted,
            call_stack=self.session.get_call_stack().copy()
        )

        if capability not in self.capability_usage:
            self.capability_usage[capability] = []
        self.capability_usage[capability].append(event)

        # Record security event if access denied
        if not granted:
            self.security_events.append(SecurityEvent(
                timestamp=event.timestamp,
                event_type='capability_denied',
                capability=capability,
                operation=operation,
                location=location,
                severity='warning'
            ))

    def get_capability_report(self) -> CapabilityReport:
        """Generate capability usage report"""
        usage_summary = {}
        for capability, events in self.capability_usage.items():
            granted_count = sum(1 for e in events if e.granted)
            denied_count = sum(1 for e in events if not e.granted)

            usage_summary[capability] = CapabilityUsageSummary(
                capability=capability,
                total_attempts=len(events),
                granted_count=granted_count,
                denied_count=denied_count,
                unique_locations=len(set(e.location for e in events)),
                first_usage=min(e.timestamp for e in events) if events else 0,
                last_usage=max(e.timestamp for e in events) if events else 0
            )

        return CapabilityReport(
            usage_summary=usage_summary,
            security_events=self.security_events.copy(),
            monitoring_duration=time.time() - self.session.start_time
        )

    def show_capability_warnings(self) -> List[str]:
        """Get capability-related warnings for display"""
        warnings = []

        # Check for frequently denied capabilities
        for capability, events in self.capability_usage.items():
            denied_events = [e for e in events if not e.granted]
            if len(denied_events) > 5:
                warnings.append(
                    f"Capability '{capability}' denied {len(denied_events)} times. "
                    f"Consider adding to program capabilities."
                )

        # Check for unused declared capabilities
        declared_caps = set(self.session.get_declared_capabilities())
        used_caps = set(self.capability_usage.keys())
        unused_caps = declared_caps - used_caps

        for cap in unused_caps:
            warnings.append(
                f"Declared capability '{cap}' is not used. "
                f"Consider removing from capability list."
            )

        return warnings
```

**Advanced Breakpoint Types**
```python
class AdvancedBreakpointManager(BreakpointManager):
    """Enhanced breakpoint manager with advanced breakpoint types"""

    def add_data_breakpoint(self, variable_name: str, access_type: str = 'write') -> DataBreakpoint:
        """Add data breakpoint that triggers on variable access"""
        bp = DataBreakpoint(
            id=self.next_id,
            variable_name=variable_name,
            access_type=access_type,  # 'read', 'write', 'readwrite'
            enabled=True,
            hit_count=0
        )
        self.breakpoints[self.next_id] = bp
        self.next_id += 1
        return bp

    def add_exception_breakpoint(self, exception_types: List[str],
                               caught: bool = True, uncaught: bool = True) -> ExceptionBreakpoint:
        """Add breakpoint that triggers on exceptions"""
        bp = ExceptionBreakpoint(
            id=self.next_id,
            exception_types=exception_types,
            break_on_caught=caught,
            break_on_uncaught=uncaught,
            enabled=True,
            hit_count=0
        )
        self.breakpoints[self.next_id] = bp
        self.next_id += 1
        return bp

    def add_function_breakpoint(self, function_name: str,
                              entry: bool = True, exit: bool = False) -> FunctionBreakpoint:
        """Add breakpoint that triggers on function entry/exit"""
        bp = FunctionBreakpoint(
            id=self.next_id,
            function_name=function_name,
            break_on_entry=entry,
            break_on_exit=exit,
            enabled=True,
            hit_count=0
        )
        self.breakpoints[self.next_id] = bp
        self.next_id += 1
        return bp

    def check_data_breakpoint(self, variable_name: str, access_type: str,
                            old_value: Any, new_value: Any) -> bool:
        """Check if data breakpoint should trigger"""
        for bp in self.breakpoints.values():
            if (isinstance(bp, DataBreakpoint) and
                bp.enabled and
                bp.variable_name == variable_name and
                (bp.access_type == access_type or bp.access_type == 'readwrite')):

                # For write access, check if value actually changed
                if access_type == 'write' and old_value == new_value:
                    continue

                bp.hit_count += 1
                return True

        return False
```

**Debug Analytics and Reporting**
```python
class DebugAnalytics:
    """Comprehensive debugging analytics and reporting"""

    def __init__(self, debug_session: 'DebugSession'):
        self.session = debug_session
        self.analytics_data = DebugAnalyticsData()

    def generate_session_report(self) -> DebugSessionReport:
        """Generate comprehensive debugging session report"""
        # Collect profiling data
        profiling_report = self.session.profiler.stop_profiling() if self.session.profiler else None

        # Collect capability data
        capability_report = self.session.capability_monitor.get_capability_report()

        # Collect debugging statistics
        debug_stats = self._collect_debug_statistics()

        # Generate insights and recommendations
        insights = self._generate_insights()

        return DebugSessionReport(
            session_duration=time.time() - self.session.start_time,
            program_file=self.session.ml_file,
            profiling_report=profiling_report,
            capability_report=capability_report,
            debug_statistics=debug_stats,
            insights=insights,
            generated_at=time.time()
        )

    def _collect_debug_statistics(self) -> DebugStatistics:
        """Collect debugging session statistics"""
        return DebugStatistics(
            total_breakpoints_set=len(self.session.breakpoints.list_breakpoints()),
            total_breakpoint_hits=sum(bp.hit_count for bp in self.session.breakpoints.list_breakpoints()),
            step_commands_executed=self.analytics_data.step_count,
            expressions_evaluated=self.analytics_data.expression_count,
            variables_inspected=self.analytics_data.variable_inspection_count,
            exceptions_caught=self.analytics_data.exception_count,
            max_call_stack_depth=self.analytics_data.max_stack_depth
        )

    def _generate_insights(self) -> List[DebugInsight]:
        """Generate debugging insights and recommendations"""
        insights = []

        # Performance insights
        if self.session.profiler:
            hotspots = self.session.profiler._identify_hotspots()
            if hotspots:
                insights.append(DebugInsight(
                    type='performance',
                    severity='medium',
                    title='Performance Hotspots Detected',
                    description=f"Found {len(hotspots)} performance hotspots in your code",
                    recommendations=[
                        f"Review {hotspot.location} ({hotspot.metric_type}: {hotspot.metric_value})"
                        for hotspot in hotspots[:3]
                    ]
                ))

        # Capability insights
        cap_warnings = self.session.capability_monitor.show_capability_warnings()
        if cap_warnings:
            insights.append(DebugInsight(
                type='security',
                severity='warning',
                title='Capability Usage Issues',
                description='Potential capability configuration issues detected',
                recommendations=cap_warnings
            ))

        # Debugging efficiency insights
        if self.analytics_data.step_count > 100:
            insights.append(DebugInsight(
                type='debugging',
                severity='info',
                title='Debugging Efficiency',
                description='Consider using more breakpoints instead of extensive stepping',
                recommendations=[
                    'Set breakpoints at key locations instead of stepping through each line',
                    'Use conditional breakpoints to stop only when specific conditions are met',
                    'Consider using watch expressions to monitor variable changes'
                ]
            ))

        return insights
```

#### **CLI Integration of Advanced Features**
```python
# Enhanced debugger commands for advanced features
class ProfileCommand(Command):
    """Start/stop profiling: profile start|stop|report"""

    def execute(self, args: List[str], debugger: MLDebugger) -> CommandResult:
        if not args:
            return CommandResult(False, "Usage: profile start|stop|report")

        action = args[0].lower()

        if action == 'start':
            debugger.session.profiler.start_profiling()
            return CommandResult(True, "Profiling started")
        elif action == 'stop':
            report = debugger.session.profiler.stop_profiling()
            return CommandResult(True, f"Profiling stopped. Total time: {report.total_execution_time:.3f}s")
        elif action == 'report':
            report = debugger.session.profiler.get_current_report()
            return CommandResult(True, self._format_profiling_report(report))
        else:
            return CommandResult(False, f"Unknown profile action: {action}")

class CapabilityCommand(Command):
    """Show capability usage: capability usage|warnings|report"""

    def execute(self, args: List[str], debugger: MLDebugger) -> CommandResult:
        if not args:
            args = ['usage']

        action = args[0].lower()

        if action == 'usage':
            report = debugger.session.capability_monitor.get_capability_report()
            return CommandResult(True, self._format_capability_usage(report))
        elif action == 'warnings':
            warnings = debugger.session.capability_monitor.show_capability_warnings()
            if warnings:
                return CommandResult(True, "Capability warnings:\n" + "\n".join(f"  • {w}" for w in warnings))
            else:
                return CommandResult(True, "No capability warnings")
        elif action == 'report':
            report = debugger.session.capability_monitor.get_capability_report()
            return CommandResult(True, self._format_full_capability_report(report))
```

#### **Success Criteria**
- Real-time performance profiling during debugging
- Capability usage monitoring and reporting
- Advanced breakpoint types (data, exception, function breakpoints)
- Comprehensive debugging analytics and insights
- Professional debugging reports with actionable recommendations

---

## Comprehensive Testing Strategy

### **Testing Architecture**
```
tests/debugging/
├── unit/                           # Component unit tests
│   ├── test_source_mapping.py
│   ├── test_cli_debugger.py
│   ├── test_breakpoint_manager.py
│   ├── test_variable_inspector.py
│   ├── test_expression_evaluator.py
│   ├── test_dap_server.py
│   ├── test_dap_handlers.py
│   └── test_profiler.py
├── integration/                    # End-to-end workflow tests
│   ├── test_cli_debugging_workflow.py
│   ├── test_dap_server_workflow.py
│   ├── test_vscode_integration.py
│   └── test_debugging_pipeline.py
├── fixtures/                      # Test ML programs
│   ├── simple_program.ml
│   ├── complex_functions.ml
│   ├── nested_calls.ml
│   ├── error_handling.ml
│   ├── loops_and_conditions.ml
│   ├── object_manipulation.ml
│   └── capability_usage.ml
├── mocks/                         # Mock implementations
│   ├── mock_python_execution.py
│   ├── mock_ide_client.py
│   ├── mock_dap_client.py
│   └── mock_profiler.py
├── performance/                   # Performance regression tests
│   ├── test_debugging_overhead.py
│   ├── benchmark_source_mapping.py
│   ├── test_breakpoint_performance.py
│   └── test_variable_inspection_performance.py
└── compliance/                    # Protocol compliance tests
    ├── test_dap_compliance.py
    └── validate_dap_messages.py
```

### **Testing Categories**

#### **1. Source Mapping Tests**
```python
class TestSourceMapping(unittest.TestCase):
    def test_line_mapping_accuracy(self):
        """Test accurate line-by-line mapping"""

    def test_function_boundary_mapping(self):
        """Test precise function start/end mapping"""

    def test_variable_name_mapping(self):
        """Test ML to Python variable name mapping"""

    def test_complex_expression_mapping(self):
        """Test mapping for nested expressions"""

    def test_breakpoint_location_validation(self):
        """Test valid breakpoint location identification"""

    def test_bidirectional_mapping_consistency(self):
        """Test ML->Python->ML mapping consistency"""
```

#### **2. CLI Debugger Tests**
```python
class TestCLIDebugger(unittest.TestCase):
    def test_debugger_initialization(self):
        """Test debugger startup and session creation"""

    def test_breakpoint_setting_and_hitting(self):
        """Test breakpoint lifecycle"""

    def test_step_execution_control(self):
        """Test step, next, continue commands"""

    def test_variable_inspection(self):
        """Test variable display in ML format"""

    def test_call_stack_navigation(self):
        """Test stack frame navigation"""

    def test_expression_evaluation(self):
        """Test ML expression evaluation in debug context"""
```

#### **3. DAP Protocol Tests**
```python
class TestDAPCompliance(unittest.TestCase):
    def test_initialize_request_response(self):
        """Test DAP initialize message handling"""

    def test_launch_configuration(self):
        """Test debug session launch via DAP"""

    def test_breakpoint_synchronization(self):
        """Test breakpoint setting/removal via DAP"""

    def test_execution_control(self):
        """Test continue/step/pause via DAP"""

    def test_variable_inspection_dap(self):
        """Test variable retrieval via DAP"""

    def test_stack_trace_dap(self):
        """Test stack trace via DAP"""
```

#### **4. Performance Tests**
```python
class TestDebuggingPerformance(unittest.TestCase):
    def test_debugging_overhead(self):
        """Ensure <5% performance overhead"""

    def test_source_mapping_lookup_speed(self):
        """Test fast location resolution"""

    def test_breakpoint_hit_detection_speed(self):
        """Test efficient breakpoint checking"""

    def test_variable_inspection_performance(self):
        """Test variable translation performance"""
```

#### **5. Integration Tests**
```python
class TestVSCodeIntegration(unittest.TestCase):
    def test_vscode_debug_session_launch(self):
        """Test launching debug session from VS Code"""

    def test_breakpoint_synchronization_vscode(self):
        """Test breakpoint sync between VS Code and debugger"""

    def test_variable_view_integration(self):
        """Test VS Code Variables view integration"""

    def test_debug_console_integration(self):
        """Test VS Code Debug Console integration"""
```

---

## Documentation Strategy

### **User Documentation Structure**

#### **`docs/debugging/getting-started.md`**
```markdown
# Getting Started with ML Debugging

## Overview
Learn the basics of debugging ML programs using both CLI and IDE interfaces.

## Quick Start
1. Setting up debugging environment
2. Your first debugging session
3. Setting breakpoints and stepping through code
4. Inspecting variables and expressions

## Common Workflows
- Debugging compilation errors
- Tracing program execution
- Finding performance bottlenecks
- Debugging capability issues
```

#### **`docs/debugging/cli-debugger.md`**
```markdown
# CLI Debugger Reference

## Starting the Debugger
```bash
mlpy debug program.ml              # Start debugging
mlpy debug program.ml arg1 arg2    # With arguments
mlpy debug --break-on-entry program.ml  # Stop at entry
```

## Debugger Commands
### Execution Control
- `run` - Start/restart program execution
- `continue` - Continue execution
- `step` - Execute next line
- `next` - Step over function calls
- `finish` - Step out of current function

### Breakpoints
- `break file:line` - Set breakpoint
- `break file:line if condition` - Conditional breakpoint
- `info breakpoints` - List breakpoints
- `delete N` - Delete breakpoint N

### Inspection
- `print variable` - Show variable value
- `list` - Show source code context
- `where` - Show call stack
- `info locals` - Show local variables
```

#### **`docs/debugging/ide-integration.md`**
```markdown
# IDE Integration Guide

## VS Code Setup
1. Install ML Language Support extension
2. Configure launch.json
3. Set breakpoints and start debugging

## Debug Configurations
### Basic Launch Configuration
```json
{
    "type": "ml",
    "request": "launch",
    "name": "Debug ML Program",
    "program": "${workspaceFolder}/main.ml"
}
```

### Advanced Configuration with Capabilities
```json
{
    "type": "ml",
    "request": "launch",
    "name": "Debug with Capabilities",
    "program": "${workspaceFolder}/main.ml",
    "capabilities": ["file:read:source", "net:http"],
    "sandbox": {
        "enabled": true,
        "maxMemoryMB": 100
    }
}
```
```

#### **`docs/debugging/advanced-features.md`**
```markdown
# Advanced Debugging Features

## Performance Profiling
- Enable profiling during debugging
- Identify performance hotspots
- Analyze function execution times
- Memory usage monitoring

## Capability Monitoring
- Track capability usage
- Identify capability violations
- Optimize capability declarations

## Advanced Breakpoints
- Conditional breakpoints
- Data breakpoints (variable access)
- Exception breakpoints
- Function entry/exit breakpoints

## Debug Analytics
- Session reports and insights
- Debugging efficiency metrics
- Performance recommendations
```

### **Developer Documentation Structure**

#### **`docs/development/debugging-architecture.md`**
```markdown
# Debugging System Architecture

## Component Overview
- Source Mapping System
- Debug Session Management
- Runtime Instrumentation
- DAP Server Implementation
- Variable Inspection Engine

## Integration Points
- Transpiler integration
- CLI integration
- VS Code extension integration

## Extension Points
- Adding new debugger commands
- Custom variable formatters
- Additional DAP capabilities
```

#### **`docs/development/extending-debugger.md`**
```markdown
# Extending the Debugger

## Adding New Commands
```python
class CustomCommand(Command):
    def execute(self, args, debugger):
        # Implementation
        pass
```

## Custom Variable Inspectors
```python
class CustomVariableInspector(VariableInspector):
    def format_for_display(self, value):
        # Custom formatting
        pass
```

## DAP Extensions
```python
class CustomDAPHandler(DAPRequestHandler):
    def handle(self, request, session):
        # Custom DAP capability
        pass
```
```

### **API Documentation**
Auto-generated API documentation covering:
- **DebugSession API**: Session management interface
- **SourceMapping API**: Location mapping interface
- **VariableInspector API**: Variable inspection interface
- **DAP Server API**: Debug Adapter Protocol interface
- **Profiler API**: Performance profiling interface

---

## Security Considerations

### **Capability-Aware Debugging**
- Debugging sessions inherit program's capability context
- Cannot access resources beyond program's declared capabilities
- Debug operations logged for security audit trail
- Capability usage visible and monitored during debugging

### **Secure Debug Protocol**
- DAP communication can be secured with authentication
- Debug access requires appropriate development capabilities
- No information leakage through debug interface
- Sandbox restrictions apply to debugging operations

### **Code Injection Prevention**
- Expression evaluation runs in isolated context
- No arbitrary code execution beyond ML language scope
- Debug console restricted to ML language constructs
- Proper validation of all debug inputs

---

## Performance Considerations

### **Optimization Strategies**
1. **Conditional Compilation**: Debug hooks only when debugging enabled
2. **Lazy Evaluation**: Variable inspection only on demand
3. **Efficient Mapping**: LRU cache for source mapping lookups
4. **Minimal Overhead**: <5% performance impact target
5. **Memory Management**: Proper cleanup of debug resources

### **Performance Monitoring**
- Continuous monitoring of debugging overhead
- Performance regression testing in CI/CD
- Benchmark comparisons with other debugging systems
- User-reported performance feedback integration

---

## Risk Assessment & Mitigation

### **Technical Risks**
1. **Performance Impact**: Mitigated through conditional compilation and optimization
2. **IDE Compatibility**: Standard DAP protocol ensures universal support
3. **Source Mapping Accuracy**: Extensive testing with complex ML programs
4. **Security Boundaries**: Careful capability integration and access control

### **Development Risks**
1. **Complexity Underestimation**: Phased approach with clear milestones
2. **IDE-Specific Issues**: Early testing with multiple IDEs
3. **User Experience Problems**: Regular usability testing and feedback
4. **Maintenance Overhead**: Well-documented architecture and automated tests

---

## Success Metrics

### **Functional Metrics**
- ✅ Can debug ML programs in CLI and VS Code
- ✅ Breakpoints work correctly in ML source code
- ✅ Variable inspection shows ML-native representation
- ✅ Step execution respects ML language semantics
- ✅ Performance profiling provides actionable insights

### **Quality Metrics**
- ✅ <5% execution overhead when debugging enabled
- ✅ >95% test coverage for debugging components
- ✅ Documentation covers all debugging features
- ✅ User feedback indicates positive debugging experience
- ✅ Security analysis shows no capability leakage

### **Adoption Metrics**
- ✅ CLI debugger available and functional
- ✅ VS Code extension provides complete debugging experience
- ✅ Documentation enables self-service debugging setup
- ✅ Advanced features (profiling, analytics) functional
- ✅ Integration with existing mlpy development workflow

---

## Implementation Timeline & Resource Allocation

### **Timeline Summary**
- **Total Duration**: 25 working days (5 weeks)
- **Phase 1-2**: Foundation (Days 1-7) - Source mapping + CLI debugger
- **Phase 3-4**: Core features (Days 8-14) - Runtime + Advanced CLI
- **Phase 5-6**: IDE integration (Days 15-21) - DAP server + VS Code
- **Phase 7**: Advanced features (Days 22-25) - Profiling + Analytics

### **Resource Requirements**
- **Core Team**: 1-2 experienced developers
- **Dependencies**: Existing transpiler, VS Code extension, DAP specification
- **Infrastructure**: Testing environments, CI/CD integration
- **External Dependencies**: VS Code debug APIs, DAP compliance tools

### **Delivery Milestones**
- **Day 7**: Working CLI debugger for basic programs
- **Day 14**: Professional CLI debugging with advanced features
- **Day 21**: Full VS Code debugging integration
- **Day 25**: Enterprise-ready debugging suite with analytics

---

## Conclusion

This enhanced debugging proposal provides a comprehensive roadmap for implementing a world-class debugging system for the ML language. The strategy prioritizes immediate developer value through CLI debugging while building systematically toward a complete, enterprise-grade debugging solution.

**Key Success Factors:**
- **Incremental Value Delivery**: Useful debugging capabilities from early phases
- **Foundation-First Approach**: Robust source mapping and CLI debugging as foundation
- **Universal Compatibility**: Standard DAP protocol for broad IDE support
- **Performance Focus**: <5% overhead maintains production viability
- **Comprehensive Testing**: Quality assurance across all components
- **Professional Documentation**: Complete user and developer guides

The proposed system will significantly enhance the developer experience for mlpy, providing debugging capabilities that match or exceed those of established programming languages while maintaining the security-first principles that make ML unique.

**Expected Outcome**: A production-ready debugging system that enables efficient development of complex ML programs with professional-grade debugging tools and enterprise-level security monitoring.