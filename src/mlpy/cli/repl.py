"""Interactive REPL (Read-Eval-Print Loop) for mlpy.

This module provides an interactive shell for executing ML code,
similar to Python's interactive interpreter or Node.js REPL.
"""

import sys
import traceback
from dataclasses import dataclass
from typing import Any, Optional

from mlpy.ml.transpiler import MLTranspiler
from mlpy.ml.errors.exceptions import MLError


@dataclass
class REPLResult:
    """Result of REPL code execution.

    Attributes:
        success: Whether execution succeeded
        value: The returned value from execution (None if error)
        error: Error message if execution failed
        transpiled_python: The Python code that was generated
        execution_time_ms: Time taken to execute in milliseconds
    """
    success: bool
    value: Any = None
    error: Optional[str] = None
    transpiled_python: str = ""
    execution_time_ms: float = 0.0


class MLREPLSession:
    """Manages a persistent REPL session with ML→Python execution.

    The REPL session maintains:
    - A persistent Python namespace for variable definitions
    - ML transpiler instance
    - Command history
    - Security and profiling settings
    """

    def __init__(self, security_enabled: bool = True, profile: bool = False):
        """Initialize REPL session.

        Args:
            security_enabled: Enable security analysis (default: True)
            profile: Enable profiling (default: False)
        """
        self.transpiler = MLTranspiler()
        self.python_namespace = {}  # Persistent namespace for variables
        self.security_enabled = security_enabled
        self.profile = profile
        self.history = []

        # Initialize namespace with built-in functions
        self._init_namespace()

    def _init_namespace(self):
        """Initialize the Python namespace with standard library imports."""
        # Add standard Python built-ins that ML code might use
        self.python_namespace['__builtins__'] = __builtins__

        # Pre-import commonly used ML standard library modules
        # This makes them available without explicit import in REPL
        try:
            from mlpy.stdlib import (
                string_bridge, array_bridge, math_bridge,
                console_bridge, json_bridge
            )
            # Make these available as modules in the namespace
            self.python_namespace['String'] = string_bridge.String()
            self.python_namespace['Array'] = array_bridge.Array()
            self.python_namespace['Math'] = math_bridge.Math()
            self.python_namespace['Console'] = console_bridge.Console()
            self.python_namespace['JSON'] = json_bridge.JSON()
        except Exception:
            # If imports fail, REPL will still work, just without pre-loaded modules
            pass

    def execute_ml_line(self, ml_code: str) -> REPLResult:
        """Execute a single line of ML code and return result.

        Args:
            ml_code: ML source code to execute

        Returns:
            REPLResult with execution status and result
        """
        import time

        if not ml_code or ml_code.strip() == "":
            return REPLResult(success=True, value=None)

        # ML grammar requires semicolons - add one if missing
        # Skip auto-semicolon for:
        # 1. Lines ending with { (multi-line start)
        # 2. Function definitions ending with }
        # But object literals like { x: 10 } need semicolons
        stripped = ml_code.rstrip()
        needs_semicolon = not stripped.endswith(';')

        # Check if this is a function definition (starts with 'function' keyword)
        is_function_def = stripped.startswith('function ') and stripped.endswith('}')

        if needs_semicolon and not stripped.endswith('{') and not is_function_def:
            ml_code = stripped + ';'

        # Add to history
        self.history.append(ml_code)

        start_time = time.time()

        try:
            # Transpile ML code to Python
            python_code, issues, source_map = self.transpiler.transpile_to_python(
                ml_code,
                source_file="<repl>"
            )

            # Handle transpilation failure
            if python_code is None:
                # Check if we have error information in issues
                error_msg = "Parse Error: Invalid ML syntax"
                if issues:
                    # Issues might be ErrorContext objects or dicts
                    if hasattr(issues, 'error') and hasattr(issues.error, 'message'):
                        # Single ErrorContext object
                        error_msg = f"Error: {issues.error.message}"
                    elif isinstance(issues, list) and len(issues) > 0:
                        # List of ErrorContext objects or dicts
                        errors = []
                        for issue in issues[:3]:  # Show first 3 errors
                            if hasattr(issue, 'error') and hasattr(issue.error, 'message'):
                                # ErrorContext object
                                errors.append(issue.error.message)
                            elif isinstance(issue, dict):
                                errors.append(issue.get('message', 'Unknown issue'))
                            elif hasattr(issue, 'message'):
                                errors.append(issue.message)
                            else:
                                errors.append(str(issue))

                        if len(errors) == 1:
                            error_msg = f"Error: {errors[0]}"
                        else:
                            error_msg = "Errors detected:\n" + "\n".join(f"  - {err}" for err in errors)
                else:
                    # No specific error info, provide helpful message
                    error_msg = f"{error_msg}\nTip: Check for missing semicolons, unmatched braces, or typos"

                return REPLResult(
                    success=False,
                    error=error_msg,
                    transpiled_python=""
                )

            # Check for security issues if enabled
            if self.security_enabled and issues:
                # Handle both dict and object formats
                critical_issues = []
                for issue in issues if isinstance(issues, list) else [issues]:
                    severity = None
                    if isinstance(issue, dict):
                        severity = issue.get('severity')
                    elif hasattr(issue, 'severity'):
                        severity = issue.severity

                    if severity == 'CRITICAL':
                        critical_issues.append(issue)

                if critical_issues:
                    error_msg = "SECURITY: Critical security violation detected:\n"
                    for issue in critical_issues:
                        if isinstance(issue, dict):
                            msg = issue.get('message', 'Unknown security issue')
                        elif hasattr(issue, 'message'):
                            msg = issue.message
                        else:
                            msg = str(issue)
                        error_msg += f"  - {msg}\n"

                    return REPLResult(
                        success=False,
                        error=error_msg,
                        transpiled_python=python_code or ""
                    )

            # Extract the actual code (skip header, but keep ML stdlib imports)
            # The transpiler adds a standard header and boilerplate imports
            lines = python_code.split('\n')
            code_lines = []
            skip_boilerplate_imports = True

            for line in lines:
                # Skip docstring
                if line.startswith('"""'):
                    continue
                # Skip comments
                if line.strip().startswith('#'):
                    continue

                # Handle imports: skip boilerplate, but keep essential imports
                if line.strip().startswith('from ') or line.strip().startswith('import '):
                    # Keep ML stdlib bridge imports (regex, string, etc.)
                    # Pattern 1: from mlpy.stdlib.X_bridge import X (new style)
                    # Pattern 2: from mlpy.stdlib.X_bridge import X as ml_X (old style)
                    # But skip console_bridge - it's boilerplate already in namespace
                    if 'mlpy.stdlib' in line and '_bridge import' in line and 'console_bridge' not in line:
                        code_lines.append(line)
                        continue
                    # Keep runtime helper imports (needed for _safe_attr_access, etc.)
                    if 'runtime_helpers' in line:
                        code_lines.append(line)
                        continue
                    # Skip boilerplate imports (console, getCurrentTime, typeof, etc.)
                    if skip_boilerplate_imports:
                        continue

                # Skip empty lines
                if not line.strip():
                    continue

                # Everything else is actual code
                code_lines.append(line)

            actual_code = '\n'.join(code_lines).strip()

            # Execute the Python code in persistent namespace
            # Use eval for expressions, exec for statements
            try:
                # Try eval first (for expressions that return values)
                result = eval(actual_code, self.python_namespace)
            except SyntaxError:
                # If eval fails, try exec (for statements)
                try:
                    exec(actual_code, self.python_namespace)
                    result = None
                except Exception as runtime_error:
                    # Runtime error during exec - format nicely
                    return self._format_runtime_error(runtime_error, ml_code)
            except Exception as runtime_error:
                # Runtime error during eval - format nicely
                return self._format_runtime_error(runtime_error, ml_code)

            execution_time = (time.time() - start_time) * 1000  # Convert to ms

            return REPLResult(
                success=True,
                value=result,
                transpiled_python=python_code,
                execution_time_ms=execution_time
            )

        except MLError as e:
            # ML language error - format nicely
            return REPLResult(
                success=False,
                error=f"ML Language Error: {str(e)}",
                transpiled_python=""
            )
        except Exception as e:
            # Unexpected error - format nicely
            return self._format_unexpected_error(e, ml_code)

    def _format_runtime_error(self, error: Exception, ml_code: str) -> REPLResult:
        """Format a runtime error with user-friendly message.

        Args:
            error: The exception that occurred
            ml_code: The ML code that caused the error

        Returns:
            REPLResult with formatted error message
        """
        error_type = type(error).__name__
        error_msg = str(error)

        # Provide user-friendly error messages for common errors
        if isinstance(error, NameError):
            var_name = error_msg.split("'")[1] if "'" in error_msg else "unknown"
            friendly_msg = f"Runtime Error: Variable '{var_name}' is not defined"
            suggestion = "Tip: Make sure you've defined the variable before using it"
        elif isinstance(error, TypeError):
            friendly_msg = f"Runtime Error: Type mismatch - {error_msg}"
            suggestion = "Tip: Check that you're using the right types for this operation"
        elif isinstance(error, AttributeError):
            friendly_msg = f"Runtime Error: {error_msg}"
            suggestion = "Tip: Check that the object has this attribute or method"
        elif isinstance(error, IndexError):
            friendly_msg = f"Runtime Error: Array index out of bounds - {error_msg}"
            suggestion = "Tip: Array indices start at 0 and must be less than the array length"
        elif isinstance(error, KeyError):
            key = error_msg.strip("'\"")
            friendly_msg = f"Runtime Error: Key '{key}' not found in object"
            suggestion = "Tip: Check that the key exists before accessing it"
        elif isinstance(error, ZeroDivisionError):
            friendly_msg = "Runtime Error: Division by zero"
            suggestion = "Tip: Check that the divisor is not zero before dividing"
        elif isinstance(error, ValueError):
            friendly_msg = f"Runtime Error: Invalid value - {error_msg}"
            suggestion = "Tip: Check that the value is valid for this operation"
        else:
            friendly_msg = f"Runtime Error ({error_type}): {error_msg}"
            suggestion = "Tip: Check the error message for details"

        return REPLResult(
            success=False,
            error=f"{friendly_msg}\n{suggestion}",
            transpiled_python=""
        )

    def _format_unexpected_error(self, error: Exception, ml_code: str) -> REPLResult:
        """Format an unexpected error with debugging information.

        Args:
            error: The exception that occurred
            ml_code: The ML code that caused the error

        Returns:
            REPLResult with formatted error message
        """
        error_type = type(error).__name__
        error_msg = str(error)

        return REPLResult(
            success=False,
            error=f"Unexpected Error ({error_type}): {error_msg}\n"
                  f"Tip: This might be a bug in the transpiler. Consider reporting it.",
            transpiled_python=""
        )

    def execute_ml_block(self, ml_lines: list[str]) -> REPLResult:
        """Execute a multi-line ML block.

        Args:
            ml_lines: List of ML source code lines

        Returns:
            REPLResult with execution status and result
        """
        # Join lines and execute as single block
        ml_code = "\n".join(ml_lines)
        return self.execute_ml_line(ml_code)

    def reset_session(self):
        """Clear namespace and restart session."""
        self.python_namespace.clear()
        self.history.clear()
        self._init_namespace()

    def get_variables(self) -> dict[str, Any]:
        """Get all user-defined variables in the namespace.

        Returns:
            Dictionary of variable names to values (excluding built-ins)
        """
        return {
            k: v for k, v in self.python_namespace.items()
            if not k.startswith('__') and k not in ['String', 'Array', 'Math', 'Console', 'JSON']
        }


def format_repl_value(value: Any) -> str:
    """Format a Python value for REPL display.

    Args:
        value: Value to format

    Returns:
        Formatted string representation
    """
    if value is None:
        return ""  # Don't display None
    elif isinstance(value, dict):
        import json
        try:
            return json.dumps(value, indent=2)
        except:
            return repr(value)
    elif isinstance(value, list):
        if len(value) == 0:
            return "[]"
        elif len(value) <= 10:
            return f"[{', '.join(repr(v) for v in value)}]"
        else:
            # Truncate long lists
            first_5 = ', '.join(repr(v) for v in value[:5])
            return f"[{first_5}, ... ({len(value)} items)]"
    elif isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, bool):
        return "true" if value else "false"  # ML-style booleans
    else:
        return repr(value)


def run_repl(security: bool = True, profile: bool = False):
    """Start the interactive REPL.

    Args:
        security: Enable security analysis (default: True)
        profile: Enable profiling (default: False)
    """
    session = MLREPLSession(security_enabled=security, profile=profile)

    # Print welcome message
    print("mlpy REPL v2.0 - Interactive ML Shell")
    print("Type .help for commands, .exit to quit")
    print()

    # Track multi-line input
    buffer = []

    while True:
        try:
            # Show different prompt for multi-line input
            if buffer:
                line = input("... ")
            else:
                line = input("ml> ")

            # Handle empty input
            if not line.strip():
                if buffer:
                    # Execute buffered multi-line input
                    result = session.execute_ml_block(buffer)
                    buffer.clear()

                    if result.success:
                        if result.value is not None:
                            print(f"=> {format_repl_value(result.value)}")
                    else:
                        print(f"Error: {result.error}")
                continue

            # Handle special commands
            if line.startswith('.'):
                command = line[1:].strip().lower()

                if command == 'exit' or command == 'quit':
                    print("Goodbye!")
                    break
                elif command == 'help':
                    print_help()
                elif command == 'vars':
                    show_variables(session)
                elif command == 'clear' or command == 'reset':
                    session.reset_session()
                    buffer.clear()
                    print("Session cleared")
                elif command == 'history':
                    show_history(session)
                else:
                    print(f"Unknown command: .{command}")
                    print("Type .help for available commands")
                continue

            # Check if line ends with opening brace (multi-line start)
            if line.rstrip().endswith('{'):
                buffer.append(line)
                continue

            # If we're in multi-line mode, add to buffer
            if buffer:
                buffer.append(line)
                # Check if line ends with closing brace (multi-line end)
                if line.rstrip().endswith('}'):
                    # Execute the full block
                    result = session.execute_ml_block(buffer)
                    buffer.clear()

                    if result.success:
                        if result.value is not None:
                            print(f"=> {format_repl_value(result.value)}")
                    else:
                        print(f"Error: {result.error}")
                continue

            # Execute single line
            result = session.execute_ml_line(line)

            if result.success:
                if result.value is not None:
                    print(f"=> {format_repl_value(result.value)}")
            else:
                print(f"Error: {result.error}")

        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            import traceback
            traceback.print_exc()


def print_help():
    """Print REPL help message."""
    print("""
REPL Commands:
  .help              Show this help message
  .vars              Show defined variables
  .clear, .reset     Clear session and reset namespace
  .history           Show command history
  .exit, .quit       Exit REPL (or Ctrl+D)

Usage:
  - Type ML code and press Enter to execute
  - Results are displayed with => prefix
  - Variables persist across commands
  - Multi-line input: lines ending with { start a block
  - Empty line executes buffered multi-line input

Examples:
  ml> let x = 42
  ml> x + 10
  => 52

  ml> let add = function(a, b) {
  ...   return a + b
  ... }

  ml> add(5, 7)
  => 12
""")


def show_variables(session: MLREPLSession):
    """Show all user-defined variables."""
    vars_dict = session.get_variables()

    if not vars_dict:
        print("No variables defined")
        return

    print("Variables:")
    for name, value in vars_dict.items():
        formatted_value = format_repl_value(value)
        if len(formatted_value) > 50:
            formatted_value = formatted_value[:50] + "..."
        print(f"  {name} = {formatted_value}")


def show_history(session: MLREPLSession):
    """Show command history."""
    if not session.history:
        print("No history")
        return

    print("History:")
    for i, cmd in enumerate(session.history[-20:], 1):  # Show last 20
        print(f"  {i}. {cmd}")


if __name__ == "__main__":
    # Allow running directly for testing
    run_repl()