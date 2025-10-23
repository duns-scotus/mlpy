"""Interactive REPL (Read-Eval-Print Loop) for mlpy.

This module provides an interactive shell for executing ML code,
similar to Python's interactive interpreter or Node.js REPL.

Performance Optimization:
- Uses incremental compilation (caches transpiled Python per statement)
- Maintains symbol tracking separately from transpilation
- O(1) performance regardless of session length (vs O(n²) cumulative)
"""

import ast
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Any

from mlpy.ml.errors.exceptions import MLError
from mlpy.ml.transpiler import MLTranspiler


@dataclass
class REPLStatement:
    """Represents a single REPL statement with cached transpilation.

    Attributes:
        ml_source: Original ML source code
        python_code: Cached transpiled Python code
        symbol_table: Symbols defined by this statement (variables, functions)
        timestamp: When this statement was executed
        execution_time_ms: Time taken to execute in milliseconds
    """

    ml_source: str
    python_code: str
    symbol_table: dict[str, str] = field(default_factory=dict)
    timestamp: float = 0.0
    execution_time_ms: float = 0.0


@dataclass
class REPLResult:
    """Result of REPL code execution.

    Attributes:
        success: Whether execution succeeded
        value: The returned value from execution (None if error)
        error: Error message if execution failed
        transpiled_python: The Python code that was generated
        execution_time_ms: Time taken to execute in milliseconds
        cached: Whether this result came from cache
    """

    success: bool
    value: Any = None
    error: str | None = None
    transpiled_python: str = ""
    execution_time_ms: float = 0.0
    cached: bool = False


class SymbolTracker:
    """Tracks symbols (variables, functions) defined in REPL session.

    This allows the REPL to know what's defined without re-transpiling
    all previous code. Symbols are extracted from Python AST after
    each successful execution.
    """

    def __init__(self):
        """Initialize empty symbol table."""
        self.symbols: dict[str, str] = {}  # name -> type ('variable' or 'function')

    def update(self, new_symbols: dict[str, str]):
        """Update symbol table with new definitions.

        Args:
            new_symbols: Dictionary of symbol names to types
        """
        self.symbols.update(new_symbols)

    def get_symbols(self) -> list[str]:
        """Get list of all defined symbol names.

        Returns:
            List of symbol names (sorted alphabetically)
        """
        return sorted(self.symbols.keys())

    def get_symbol_type(self, name: str) -> str | None:
        """Get type of a symbol.

        Args:
            name: Symbol name

        Returns:
            Symbol type ('variable' or 'function') or None if not found
        """
        return self.symbols.get(name)

    def clear(self):
        """Clear all symbols."""
        self.symbols.clear()


class MLREPLSession:
    """Manages a persistent REPL session with ML→Python execution.

    The REPL session maintains:
    - A persistent Python namespace for variable definitions
    - ML transpiler instance
    - Cached transpiled statements (for incremental compilation)
    - Symbol tracker (for tracking defined variables/functions)
    - Command history with FIFO eviction
    - Security and profiling settings

    Performance:
    - Incremental compilation: O(1) per statement (vs O(n²) cumulative)
    - Symbol tracking avoids re-parsing for completion
    - Statement cache with configurable history limit
    """

    def __init__(
        self,
        security_enabled: bool = True,
        profile: bool = False,
        max_history: int = 1000,
        extension_paths: list[str] | None = None,
        ml_module_paths: list[str] | None = None,
    ):
        """Initialize REPL session.

        Args:
            security_enabled: Enable security analysis (default: True)
            profile: Enable profiling (default: False)
            max_history: Maximum number of statements to keep in history (default: 1000)
            extension_paths: Paths to Python extension module directories (default: None)
            ml_module_paths: Paths to ML module directories (default: None)
        """
        # Create transpiler in REPL mode for true incremental compilation
        # Pass extension paths to enable custom module imports
        self.transpiler = MLTranspiler(repl_mode=True, python_extension_paths=extension_paths)
        self.python_namespace = {}  # Persistent namespace for variables
        self.security_enabled = security_enabled
        self.profile = profile
        self.max_history = max_history
        self.ml_module_paths = ml_module_paths or []  # Store for transpiler import_paths

        # Register ML module paths with the global registry
        if ml_module_paths:
            from mlpy.stdlib.module_registry import get_registry
            registry = get_registry()
            registry.add_ml_module_paths(ml_module_paths)

        # Use deque for automatic FIFO eviction when max_history reached
        self.statements: deque[REPLStatement] = deque(maxlen=max_history)
        self.history: deque[str] = deque(maxlen=max_history)  # ML source only

        # Symbol tracking for auto-completion and variable inspection
        self.symbol_tracker = SymbolTracker()

        # Capability management for runtime security control
        self.granted_capabilities: set[str] = set()
        self.capability_audit_log: list[tuple[str, str, float]] = []  # (action, capability, timestamp)

        # Error recovery tracking
        self.last_failed_code: str | None = None
        self.last_error: str | None = None

        # Initialize namespace with built-in functions
        self._init_namespace()

    def _init_namespace(self):
        """Initialize the Python namespace with standard library imports."""
        # Add standard Python built-ins that ML code might use
        self.python_namespace["__builtins__"] = __builtins__

        # Pre-import ML builtin module - provides typeof, len, print, etc.
        try:
            from mlpy.stdlib.builtin import builtin

            # Make all builtin functions available directly in namespace
            # This allows: typeof(x), len(arr), print(msg) without "builtin." prefix
            self.python_namespace["builtin"] = builtin
            self.python_namespace["typeof"] = builtin.typeof
            self.python_namespace["len"] = builtin.len
            self.python_namespace["print"] = builtin.print
            self.python_namespace["input"] = builtin.input
            self.python_namespace["int"] = builtin.int
            self.python_namespace["float"] = builtin.float
            self.python_namespace["str"] = builtin.str
            self.python_namespace["bool"] = builtin.bool
            self.python_namespace["range"] = builtin.range
            self.python_namespace["abs"] = builtin.abs
            self.python_namespace["min"] = builtin.min
            self.python_namespace["max"] = builtin.max
            self.python_namespace["round"] = builtin.round
            self.python_namespace["sorted"] = builtin.sorted
            self.python_namespace["sum"] = builtin.sum
            self.python_namespace["keys"] = builtin.keys
            self.python_namespace["values"] = builtin.values
        except Exception as e:
            # If builtin import fails, REPL won't have basic functions
            print(f"Warning: Failed to import builtin module: {e}")
            pass

        # Pre-import commonly used ML standard library modules
        # This makes them available without explicit import in REPL
        try:
            from mlpy.stdlib import console, json, math, datetime, functional, regex

            # Make these available as modules in the namespace
            self.python_namespace["console"] = console
            self.python_namespace["json"] = json
            self.python_namespace["math"] = math
            self.python_namespace["datetime"] = datetime
            self.python_namespace["functional"] = functional
            self.python_namespace["regex"] = regex
        except Exception as e:
            # If imports fail, REPL will still work, just without pre-loaded modules
            print(f"Warning: Failed to import stdlib modules: {e}")
            pass

    def execute_ml_line(self, ml_code: str) -> REPLResult:
        """Execute a single line of ML code with incremental compilation.

        Uses incremental compilation for performance:
        1. Transpile ONLY the new ML code
        2. Cache the transpiled Python
        3. Execute in persistent namespace
        4. Track symbols for auto-completion

        Args:
            ml_code: ML source code to execute

        Returns:
            REPLResult with execution status and result
        """
        if not ml_code or ml_code.strip() == "":
            return REPLResult(success=True, value=None)

        # ML grammar requires semicolons - add one if missing
        # Skip auto-semicolon for:
        # 1. Lines ending with { (multi-line start)
        # 2. Block statements ending with } (function, for, while, if, try)
        # But object literals like { x: 10 } need semicolons
        stripped = ml_code.rstrip()
        needs_semicolon = not stripped.endswith(";")

        # Check if this is a block statement (function, for, while, if, elif, else, try, except, finally)
        # These end with } but should NOT get a semicolon
        block_keywords = ("function ", "for ", "while ", "if ", "elif ", "else", "try", "except", "finally")
        is_block_statement = any(stripped.startswith(kw) for kw in block_keywords) and stripped.endswith("}")

        if needs_semicolon and not stripped.endswith("{") and not is_block_statement:
            ml_code = stripped + ";"

        # Add to history (deque automatically handles max_history)
        self.history.append(ml_code)

        start_time = time.time()

        try:
            # === TRUE INCREMENTAL COMPILATION ===
            # Transpile ONLY the new ML code (not cumulative)
            # This is the key performance optimization: O(1) vs O(n)
            # REPL mode in transpiler assumes variables from previous statements exist
            python_code, issues, source_map = self.transpiler.transpile_to_python(
                ml_code,  # Just this statement!
                source_file=f"<repl:{len(self.statements)}>",
                import_paths=self.ml_module_paths  # Pass import paths for ML module resolution
            )

            # Handle transpilation failure
            if python_code is None:
                # Track failed command for .retry
                self.last_failed_code = ml_code

                # Check if we have error information in issues
                error_msg = "Parse Error: Invalid ML syntax"
                if issues:
                    # Issues might be ErrorContext objects or dicts
                    if hasattr(issues, "error") and hasattr(issues.error, "message"):
                        # Single ErrorContext object
                        error_msg = f"Error: {issues.error.message}"
                    elif isinstance(issues, list) and len(issues) > 0:
                        # List of ErrorContext objects or dicts
                        errors = []
                        for issue in issues[:3]:  # Show first 3 errors
                            if hasattr(issue, "error") and hasattr(issue.error, "message"):
                                # ErrorContext object
                                errors.append(issue.error.message)
                            elif isinstance(issue, dict):
                                errors.append(issue.get("message", "Unknown issue"))
                            elif hasattr(issue, "message"):
                                errors.append(issue.message)
                            else:
                                errors.append(str(issue))

                        if len(errors) == 1:
                            error_msg = f"Error: {errors[0]}"
                        else:
                            error_msg = "Errors detected:\n" + "\n".join(
                                f"  - {err}" for err in errors
                            )
                else:
                    # No specific error info, provide helpful message
                    error_msg = f"{error_msg}\nTip: Check for missing semicolons, unmatched braces, or typos"

                # Store error for .retry
                self.last_error = error_msg

                return REPLResult(success=False, error=error_msg, transpiled_python="")

            # Check for security issues if enabled
            if self.security_enabled and issues:
                # Handle both dict and object formats
                critical_issues = []
                for issue in issues if isinstance(issues, list) else [issues]:
                    severity = None
                    if isinstance(issue, dict):
                        severity = issue.get("severity")
                    elif hasattr(issue, "severity"):
                        severity = issue.severity

                    if severity == "CRITICAL":
                        critical_issues.append(issue)

                if critical_issues:
                    # Track failed command for .retry
                    self.last_failed_code = ml_code

                    error_msg = "SECURITY: Critical security violation detected:\n"
                    for issue in critical_issues:
                        if isinstance(issue, dict):
                            msg = issue.get("message", "Unknown security issue")
                        elif hasattr(issue, "message"):
                            msg = issue.message
                        else:
                            msg = str(issue)
                        error_msg += f"  - {msg}\n"

                    # Store error for .retry
                    self.last_error = error_msg

                    return REPLResult(
                        success=False, error=error_msg, transpiled_python=python_code or ""
                    )

            # Extract the actual code (skip header, but keep ML stdlib imports)
            # The transpiler adds a standard header and boilerplate imports
            lines = python_code.split("\n")
            code_lines = []

            for line in lines:
                # Skip docstring
                if line.startswith('"""'):
                    continue
                # Skip comments
                if line.strip().startswith("#"):
                    continue

                # Handle imports: ALWAYS keep essential imports
                if line.strip().startswith("from ") or line.strip().startswith("import "):
                    # Keep whitelist validator import (_safe_call)
                    if "whitelist_validator" in line or "_safe_call" in line:
                        code_lines.append(line)
                        continue
                    # Keep builtin module import (auto-generated for builtin functions)
                    if "from mlpy.stdlib.builtin import builtin" in line:
                        code_lines.append(line)
                        continue
                    # Keep ML stdlib bridge imports (regex, string, etc.)
                    if "mlpy.stdlib" in line and "_bridge import" in line:
                        code_lines.append(line)
                        continue
                    # Keep runtime helper imports (needed for _safe_attr_access, etc.)
                    if "runtime_helpers" in line:
                        code_lines.append(line)
                        continue
                    # Keep sys and Path imports (needed for ML module path setup)
                    if "import sys" in line or "from pathlib import Path" in line:
                        code_lines.append(line)
                        continue
                    # Keep user module imports (plain import statements without 'from')
                    # These are generated by _generate_user_module_import for ML modules
                    if line.strip().startswith("import ") and "from " not in line and "mlpy" not in line:
                        code_lines.append(line)
                        continue
                    # Skip other boilerplate imports
                    continue

                # Skip empty lines
                if not line.strip():
                    continue

                # Everything else is actual code
                code_lines.append(line)

            actual_code = "\n".join(code_lines).strip()

            # === EXECUTE CODE ===
            # Execute only the NEW Python code in persistent namespace
            # Strategy: Capture the last expression's value without re-executing it
            result = None

            try:
                # Check if the last line is an expression that should be captured
                code_lines_stripped = [line for line in code_lines if line.strip()]
                if code_lines_stripped:
                    last_line = code_lines_stripped[-1].strip()

                    # Check if last line looks like an expression (not a statement)
                    # Expressions: variable access, function calls, operations, literals
                    # Statements: assignments, function defs, class defs, control flow, imports
                    is_expression = (
                        not last_line.startswith(('def ', 'class ', 'if ', 'for ', 'while ', 'try:', 'with ', 'import ', 'from ')) and
                        '=' not in last_line.split('#')[0] or  # Assignment (but not in comments)
                        last_line.startswith(('return ', 'yield '))
                    )

                    # For expressions, capture the value in a temporary variable to avoid re-execution
                    if is_expression and not last_line.startswith(('return ', 'yield ')):
                        # Modify code to capture last expression's value
                        code_without_last = "\n".join(code_lines_stripped[:-1])
                        modified_code = f"{code_without_last}\n__repl_last_value__ = {last_line}" if code_without_last else f"__repl_last_value__ = {last_line}"

                        # Execute modified code
                        exec(modified_code, self.python_namespace)

                        # Get the captured value
                        result = self.python_namespace.pop('__repl_last_value__', None)
                    else:
                        # For statements, just execute normally
                        exec(actual_code, self.python_namespace)

            except Exception as runtime_error:
                # Track failed command for .retry
                self.last_failed_code = ml_code
                # Runtime error during execution - format nicely
                result = self._format_runtime_error(runtime_error, ml_code)
                self.last_error = result.error
                return result

            execution_time = (time.time() - start_time) * 1000  # Convert to ms

            # === SYMBOL TRACKING ===
            # Extract symbols from the executed Python code for auto-completion
            new_symbols = self._extract_symbols(actual_code)
            self.symbol_tracker.update(new_symbols)

            # === CACHE STATEMENT ===
            # Store the transpiled statement for future reference
            stmt = REPLStatement(
                ml_source=ml_code,
                python_code=python_code,
                symbol_table=new_symbols,
                timestamp=time.time(),
                execution_time_ms=execution_time,
            )
            self.statements.append(stmt)  # deque automatically handles max_history

            # Clear error tracking on successful execution
            self.last_failed_code = None
            self.last_error = None

            return REPLResult(
                success=True,
                value=result,
                transpiled_python=python_code,
                execution_time_ms=execution_time,
                cached=False,
            )

        except MLError as e:
            # ML language error - format nicely
            return REPLResult(
                success=False, error=f"ML Language Error: {str(e)}", transpiled_python=""
            )
        except Exception as e:
            # Unexpected error - format nicely
            return self._format_unexpected_error(e, ml_code)

    def _extract_symbols(self, python_code: str) -> dict[str, str]:
        """Extract variable and function names defined in Python code.

        Uses AST parsing to find:
        - Function definitions (def name(...))
        - Variable assignments (name = ...)
        - Class definitions (class Name(...))

        Args:
            python_code: Python source code to analyze

        Returns:
            Dictionary mapping symbol names to types ('function', 'variable', 'class')
        """
        symbols = {}

        try:
            # Parse Python code into AST
            tree = ast.parse(python_code)

            # Walk the AST to find definitions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Function definition: def name(...)
                    symbols[node.name] = "function"
                elif isinstance(node, ast.ClassDef):
                    # Class definition: class Name(...)
                    symbols[node.name] = "class"
                elif isinstance(node, ast.Assign):
                    # Variable assignment: name = ...
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            symbols[target.id] = "variable"
                        elif isinstance(target, ast.Tuple):
                            # Tuple unpacking: a, b = ...
                            for elt in target.elts:
                                if isinstance(elt, ast.Name):
                                    symbols[elt.id] = "variable"
                elif isinstance(node, ast.AnnAssign):
                    # Annotated assignment: name: type = ...
                    if isinstance(node.target, ast.Name):
                        symbols[node.target.id] = "variable"

        except SyntaxError:
            # If parsing fails, return empty dict (will retry next time)
            pass

        return symbols

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
            success=False, error=f"{friendly_msg}\n{suggestion}", transpiled_python=""
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
            transpiled_python="",
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

    def grant_capability(self, capability: str) -> bool:
        """Grant a capability for this REPL session.

        Args:
            capability: Capability name (e.g., "file.read", "network.http")

        Returns:
            True if capability was granted, False if invalid
        """
        # Validate capability name format
        if not capability or "." not in capability:
            return False

        # Add to granted capabilities
        self.granted_capabilities.add(capability)

        # Audit log
        self.capability_audit_log.append(("GRANT", capability, time.time()))

        return True

    def revoke_capability(self, capability: str) -> bool:
        """Revoke a previously granted capability.

        Args:
            capability: Capability name to revoke

        Returns:
            True if capability was revoked, False if not found
        """
        if capability not in self.granted_capabilities:
            return False

        self.granted_capabilities.remove(capability)

        # Audit log
        self.capability_audit_log.append(("REVOKE", capability, time.time()))

        return True

    def get_capabilities(self) -> list[str]:
        """Get list of all granted capabilities.

        Returns:
            Sorted list of capability names
        """
        return sorted(self.granted_capabilities)

    def reset_session(self):
        """Clear namespace and restart session.

        Clears:
        - Python namespace (variables, functions)
        - Statement cache
        - Command history
        - Symbol tracker
        - Granted capabilities
        - Error recovery state

        Then re-initializes namespace with builtins.
        """
        self.python_namespace.clear()
        self.statements.clear()
        self.history.clear()
        self.symbol_tracker.clear()
        self.granted_capabilities.clear()
        self.capability_audit_log.clear()
        self.last_failed_code = None
        self.last_error = None
        self._init_namespace()

    def get_variables(self) -> dict[str, Any]:
        """Get all user-defined variables in the namespace.

        Returns:
            Dictionary of variable names to values (excluding built-ins)
        """
        # Exclude builtin module, stdlib modules, builtin functions, and runtime helpers
        excluded = {
            "builtin",
            "console",
            "json",
            "math",
            "datetime",
            "functional",
            "regex",
            "typeof",
            "len",
            "print",
            "input",
            "int",
            "float",
            "str",
            "bool",
            "range",
            "abs",
            "min",
            "max",
            "round",
            "sorted",
            "sum",
            "keys",
            "values",
            "_safe_call",
        }
        return {
            k: v
            for k, v in self.python_namespace.items()
            if not k.startswith("__") and k not in excluded
        }

    # Development Mode Commands

    def toggle_dev_mode(self) -> tuple[bool, str]:
        """Toggle development mode on/off.

        Returns:
            Tuple of (new_state, message)
        """
        from mlpy.stdlib.module_registry import get_registry
        registry = get_registry()

        if not registry._performance_mode:
            registry.enable_performance_mode()
            return (True, "Development mode: ENABLED\n  - Performance monitoring active\n  - Detailed logging enabled")
        else:
            registry.disable_performance_mode()
            return (False, "Development mode: DISABLED")

    def reload_module(self, module_name: str) -> tuple[bool, str]:
        """Reload a specific module.

        Args:
            module_name: Name of module to reload

        Returns:
            Tuple of (success, message)
        """
        from mlpy.stdlib.module_registry import get_registry
        registry = get_registry()

        if not module_name:
            return (False, "Usage: .reload <module_name>\nExample: .reload math")

        if module_name not in registry._discovered:
            return (False, f"Module '{module_name}' not found")

        success = registry.reload_module(module_name)
        if success:
            return (True, f"✓ Reloaded module: {module_name}")
        else:
            return (False, f"✗ Failed to reload: {module_name}")

    def reload_all_modules(self) -> tuple[bool, str]:
        """Reload all loaded modules.

        Returns:
            Tuple of (success, message)
        """
        from mlpy.stdlib.module_registry import get_registry
        registry = get_registry()

        results = registry.reload_all_modules()

        if not results:
            return (True, "No modules currently loaded")

        successes = [name for name, success in results.items() if success]
        failures = [name for name, success in results.items() if not success]

        msg = f"Reloaded {len(successes)}/{len(results)} modules"
        if successes:
            msg += "\n  Successfully reloaded:"
            for name in successes:
                msg += f"\n    - {name}"
        if failures:
            msg += "\n  Failed to reload:"
            for name in failures:
                msg += f"\n    - {name}"

        return (True, msg)

    def refresh_modules(self) -> tuple[bool, str]:
        """Refresh module discovery (re-scan directories).

        Returns:
            Tuple of (success, message)
        """
        from mlpy.stdlib.module_registry import get_registry
        registry = get_registry()

        result = registry.refresh_all()

        msg = f"Refreshed module list:\n"
        msg += f"  Total modules: {result['total_modules']}\n"
        msg += f"  Reloaded: {result['reloaded_modules']}"
        if result['reload_failures'] > 0:
            msg += f"\n  Failed: {result['reload_failures']}"

        return (True, msg)

    def get_performance_summary(self) -> tuple[bool, str]:
        """Get performance monitoring summary with module type breakdown.

        Returns:
            Tuple of (success, message)
        """
        from mlpy.stdlib.module_registry import get_registry, ModuleType
        registry = get_registry()

        if not registry._performance_mode:
            return (False, "Performance monitoring not enabled\nUse .devmode to enable")

        summary = registry.get_performance_summary()

        # Separate metrics by module type
        python_loads = []
        ml_loads = []

        for module_name, load_time in summary.get('slowest_loads', []):
            metadata = registry._discovered.get(module_name)
            if metadata:
                if metadata.module_type == ModuleType.PYTHON_BRIDGE:
                    python_loads.append((module_name, load_time))
                elif metadata.module_type == ModuleType.ML_SOURCE:
                    ml_loads.append((module_name, load_time))

        msg = "Performance Summary:\n\n"
        msg += f"  Overall:\n"
        msg += f"    Total scans: {summary['total_scans']}\n"
        msg += f"    Avg scan time: {summary['avg_scan_time_ms']:.2f}ms\n"
        msg += f"    Total module loads: {summary['total_loads']}\n"
        msg += f"    Avg load time: {summary['avg_load_time_ms']:.2f}ms"

        if python_loads:
            msg += "\n\n  Python Bridge Modules:\n"
            avg_python = sum(t for _, t in python_loads) / len(python_loads)
            msg += f"    Total loads: {len(python_loads)}\n"
            msg += f"    Avg load time: {avg_python*1000:.2f}ms"

            if len(python_loads) <= 5:
                for name, time_val in python_loads:
                    msg += f"\n      - {name}: {time_val*1000:.2f}ms"

        if ml_loads:
            msg += "\n\n  ML Modules:\n"
            avg_ml = sum(t for _, t in ml_loads) / len(ml_loads)
            msg += f"    Total transpilations: {len(ml_loads)}\n"
            msg += f"    Avg transpilation time: {avg_ml*1000:.2f}ms"

            slowest_ml = sorted(ml_loads, key=lambda x: x[1], reverse=True)[:3]
            if slowest_ml:
                msg += "\n    Slowest transpilations:"
                for name, time_val in slowest_ml:
                    warning = " ⚠️ SLOW" if time_val > 0.1 else ""
                    msg += f"\n      - {name}: {time_val*1000:.2f}ms{warning}"

        if summary['reload_counts']:
            msg += "\n\n  Module Reloads:"
            for name, count in sorted(summary['reload_counts'].items()):
                msg += f"\n    - {name}: {count} reload(s)"

        return (True, msg)

    def get_memory_report(self) -> tuple[bool, str]:
        """Get memory usage report with module type breakdown.

        Returns:
            Tuple of (success, message)
        """
        from mlpy.stdlib.module_registry import get_registry, ModuleType
        registry = get_registry()

        report = registry.get_memory_report()

        if report['total_loaded'] == 0:
            return (True, "No modules currently loaded")

        # Separate modules by type
        python_modules = []
        ml_modules = []
        python_size = 0
        ml_size = 0

        for module_info in report['modules']:
            module_name = module_info['name']
            metadata = registry._discovered.get(module_name)

            if metadata:
                if metadata.module_type == ModuleType.PYTHON_BRIDGE:
                    python_modules.append(module_info)
                    python_size += module_info['size_bytes']
                elif metadata.module_type == ModuleType.ML_SOURCE:
                    ml_modules.append(module_info)
                    ml_size += module_info['size_bytes']

        msg = f"Memory Report:\n\n"
        msg += f"  Overall:\n"
        msg += f"    Total loaded modules: {report['total_loaded']}\n"
        msg += f"    Total memory: {report['total_size_mb']:.2f} MB"

        if python_modules:
            msg += f"\n\n  Python Bridge Modules ({len(python_modules)} loaded):\n"
            msg += f"    Memory usage: {python_size / (1024 * 1024):.2f} MB"

            if len(python_modules) <= 5:
                msg += "\n    Modules:"
                for module in python_modules:
                    msg += f"\n      - {module['name']}: {module['size_kb']:.2f} KB"

        if ml_modules:
            msg += f"\n\n  ML Modules ({len(ml_modules)} loaded):\n"
            msg += f"    Memory usage: {ml_size / (1024 * 1024):.2f} MB"

            # Sort ML modules by size and show top 5
            ml_modules_sorted = sorted(ml_modules, key=lambda x: x['size_bytes'], reverse=True)[:5]
            if ml_modules_sorted:
                msg += "\n    Top memory consumers:"
                for module in ml_modules_sorted:
                    msg += f"\n      - {module['name']}: {module['size_kb']:.2f} KB"

        return (True, msg)


def format_repl_value(value: Any, max_lines: int = 50, use_pager: bool = True) -> str:
    """Format a Python value for REPL display with optional paging.

    Args:
        value: Value to format
        max_lines: Maximum lines before triggering pager (default: 50)
        use_pager: Enable paging for large output (default: True)

    Returns:
        Formatted string representation
    """
    if value is None:
        return ""  # Don't display None

    # Format the value
    formatted = None

    if isinstance(value, dict):
        import json

        try:
            formatted = json.dumps(value, indent=2)
        except:
            formatted = repr(value)
    elif isinstance(value, list):
        if len(value) == 0:
            formatted = "[]"
        elif len(value) <= 10:
            formatted = f"[{', '.join(repr(v) for v in value)}]"
        else:
            # For very long lists, show more detail with paging
            if len(value) > 100:
                # Show full list in paged output
                items = ",\n  ".join(repr(v) for v in value)
                formatted = f"[\n  {items}\n]"
            else:
                # Medium lists - show all inline
                formatted = f"[{', '.join(repr(v) for v in value)}]"
    elif isinstance(value, str):
        formatted = f'"{value}"'
    elif isinstance(value, bool):
        formatted = "true" if value else "false"  # ML-style booleans
    else:
        formatted = repr(value)

    # Check if output needs paging
    if use_pager and formatted and formatted.count("\n") > max_lines:
        return _page_output(formatted)

    return formatted


def _page_output(content: str) -> str:
    """Display content in a pager (like 'less').

    Args:
        content: Content to display

    Returns:
        Empty string (content already displayed)
    """
    try:
        # Try to use prompt_toolkit's pager
        from prompt_toolkit import print_formatted_text
        from prompt_toolkit.formatted_text import FormattedText

        lines = content.split("\n")
        print(f"\n--- Output ({len(lines)} lines) - Press Space to scroll, Q to quit ---")
        print_formatted_text(FormattedText([("", content)]), pager=True)
        return ""
    except ImportError:
        # Fallback: use system pager (less on Unix, more on Windows)
        import subprocess
        import sys
        import tempfile

        try:
            # Write to temp file
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".txt", delete=False, encoding="utf-8"
            ) as f:
                f.write(content)
                temp_path = f.name

            # Determine pager command
            if sys.platform == "win32":
                # Windows: use 'more'
                subprocess.call(["more", temp_path], shell=True)
            else:
                # Unix: use 'less' with options
                subprocess.call(["less", "-R", temp_path])

            # Clean up
            import os

            os.unlink(temp_path)
            return ""
        except:
            # Final fallback: just print with truncation notice
            lines = content.split("\n")
            print(f"\n--- Output ({len(lines)} lines) - Showing first 50 lines ---")
            print("\n".join(lines[:50]))
            print(f"... ({len(lines) - 50} more lines)")
            return ""


def run_repl(
    security: bool = True,
    profile: bool = False,
    fancy: bool = True,
    extension_paths: list[str] | None = None,
    ml_module_paths: list[str] | None = None,
):
    """Start the interactive REPL.

    Args:
        security: Enable security analysis (default: True)
        profile: Enable profiling (default: False)
        fancy: Enable fancy terminal features (syntax highlighting, auto-completion)
               Set to False for basic mode or if prompt_toolkit unavailable
        extension_paths: Paths to Python extension module directories (default: None)
        ml_module_paths: Paths to ML module directories (default: None)
    """
    if fancy:
        try:
            run_fancy_repl(
                security=security,
                profile=profile,
                extension_paths=extension_paths,
                ml_module_paths=ml_module_paths,
            )
        except ImportError:
            print("Warning: prompt_toolkit not available, falling back to basic REPL")
            run_basic_repl(
                security=security,
                profile=profile,
                extension_paths=extension_paths,
                ml_module_paths=ml_module_paths,
            )
        except Exception as e:
            print(f"Warning: Fancy REPL failed ({e}), falling back to basic REPL")
            run_basic_repl(
                security=security,
                profile=profile,
                extension_paths=extension_paths,
                ml_module_paths=ml_module_paths,
            )
    else:
        run_basic_repl(
            security=security,
            profile=profile,
            extension_paths=extension_paths,
            ml_module_paths=ml_module_paths,
        )


def run_fancy_repl(
    security: bool = True,
    profile: bool = False,
    extension_paths: list[str] | None = None,
    ml_module_paths: list[str] | None = None,
):
    """Start the REPL with modern terminal features.

    Features:
    - Syntax highlighting
    - Auto-completion (Tab)
    - History navigation (Up/Down arrows)
    - History search (Ctrl+R)
    - Multi-line editing

    Args:
        security: Enable security analysis
        profile: Enable profiling
        extension_paths: Paths to Python extension module directories
        ml_module_paths: Paths to ML module directories
    """
    from prompt_toolkit import PromptSession
    from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
    from prompt_toolkit.history import FileHistory
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.lexers import PygmentsLexer
    from prompt_toolkit.styles import Style

    from .repl_completer import MLCompleter
    from .repl_lexer import MLLexer, ML_STYLE

    session = MLREPLSession(
        security_enabled=security,
        profile=profile,
        extension_paths=extension_paths,
        ml_module_paths=ml_module_paths,
    )

    # Create prompt session with all features
    import os

    history_file = os.path.expanduser("~/.mlpy_history")
    prompt_session = PromptSession(
        history=FileHistory(history_file),
        auto_suggest=AutoSuggestFromHistory(),
        enable_history_search=True,
        lexer=PygmentsLexer(MLLexer),
        completer=MLCompleter(session),
        complete_while_typing=True,
        style=Style.from_dict(ML_STYLE),
    )

    # Custom key bindings
    bindings = KeyBindings()

    @bindings.add("c-d")  # Ctrl+D to exit
    def _(event):
        event.app.exit()

    # Print welcome message
    security_status = "[secure]" if security else "[unsafe]"
    print(f"mlpy REPL v2.1 - Interactive ML Shell {security_status}")
    print("Features: Syntax highlighting, auto-completion (Tab), history (↑↓)")
    print("Type .help for commands, .exit to quit (or Ctrl+D)")
    print()

    # Track multi-line input
    buffer = []

    while True:
        try:
            # Security indicator in prompt
            if security:
                prompt_style = "class:prompt"
                indicator = "[secure]"
            else:
                # Red color for unsafe mode
                prompt_style = "fg:ansired bold"
                indicator = "[unsafe]"

            # Show different prompt for multi-line input
            if buffer:
                prompt_text = [("class:continuation", "... ")]
            else:
                prompt_text = [(prompt_style, f"ml{indicator}> ")]

            # Get input with all fancy features
            line = prompt_session.prompt(prompt_text, key_bindings=bindings)

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
            if line.startswith("."):
                command = line[1:].strip().lower()

                if command == "exit" or command == "quit":
                    print("Goodbye!")
                    break
                elif command == "help":
                    print_help()
                elif command == "vars":
                    show_variables(session)
                elif command == "clear" or command == "reset":
                    session.reset_session()
                    buffer.clear()
                    print("Session cleared")
                elif command == "history":
                    show_history(session)
                elif command == "capabilities":
                    show_capabilities(session)
                elif command.startswith("grant "):
                    capability = line[7:].strip()  # Get capability after ".grant "
                    handle_grant_command(session, capability)
                elif command.startswith("revoke "):
                    capability = line[8:].strip()  # Get capability after ".revoke "
                    handle_revoke_command(session, capability)
                elif command == "retry":
                    handle_retry_command(session, buffer)
                elif command == "edit":
                    handle_edit_command(session)
                elif command == "modules":
                    show_modules()
                elif command.startswith("modinfo "):
                    module_name = line[9:].strip()  # Get module name after ".modinfo "
                    show_module_info(module_name)
                elif command.startswith("addpath "):
                    path = line[9:].strip()  # Get path after ".addpath "
                    add_extension_path(path)
                elif command == "devmode":
                    _, msg = session.toggle_dev_mode()
                    print(msg)
                elif command.startswith("reload "):
                    module_name = line[8:].strip()  # Get module name after ".reload "
                    _, msg = session.reload_module(module_name)
                    print(msg)
                elif command == "reloadall":
                    _, msg = session.reload_all_modules()
                    print(msg)
                elif command == "refresh":
                    _, msg = session.refresh_modules()
                    print(msg)
                elif command == "perfmon":
                    _, msg = session.get_performance_summary()
                    print(msg)
                elif command == "memreport":
                    _, msg = session.get_memory_report()
                    print(msg)
                else:
                    print(f"Unknown command: .{command}")
                    print("Type .help for available commands")
                continue

            # Check if line ends with opening brace (multi-line start)
            if line.rstrip().endswith("{"):
                buffer.append(line)
                continue

            # If we're in multi-line mode, add to buffer
            if buffer:
                buffer.append(line)
                # Check if line ends with closing brace (multi-line end)
                if line.rstrip().endswith("}"):
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


def run_basic_repl(
    security: bool = True,
    profile: bool = False,
    extension_paths: list[str] | None = None,
    ml_module_paths: list[str] | None = None,
):
    """Start the REPL in basic mode (no fancy features).

    Uses plain input() for compatibility when prompt_toolkit is unavailable.

    Args:
        security: Enable security analysis (default: True)
        profile: Enable profiling (default: False)
        extension_paths: Paths to Python extension module directories (default: None)
        ml_module_paths: Paths to ML module directories (default: None)
    """
    session = MLREPLSession(
        security_enabled=security,
        profile=profile,
        extension_paths=extension_paths,
        ml_module_paths=ml_module_paths,
    )

    # Print welcome message
    security_status = "[secure]" if security else "[unsafe]"
    print(f"mlpy REPL v2.1 - Interactive ML Shell {security_status}")
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
            if line.startswith("."):
                command = line[1:].strip().lower()

                if command == "exit" or command == "quit":
                    print("Goodbye!")
                    break
                elif command == "help":
                    print_help()
                elif command == "vars":
                    show_variables(session)
                elif command == "clear" or command == "reset":
                    session.reset_session()
                    buffer.clear()
                    print("Session cleared")
                elif command == "history":
                    show_history(session)
                elif command == "capabilities":
                    show_capabilities(session)
                elif command.startswith("grant "):
                    capability = line[7:].strip()  # Get capability after ".grant "
                    handle_grant_command(session, capability)
                elif command.startswith("revoke "):
                    capability = line[8:].strip()  # Get capability after ".revoke "
                    handle_revoke_command(session, capability)
                elif command == "retry":
                    handle_retry_command(session, buffer)
                elif command == "edit":
                    handle_edit_command(session)
                elif command == "modules":
                    show_modules()
                elif command.startswith("modinfo "):
                    module_name = line[9:].strip()  # Get module name after ".modinfo "
                    show_module_info(module_name)
                elif command.startswith("addpath "):
                    path = line[9:].strip()  # Get path after ".addpath "
                    add_extension_path(path)
                elif command == "devmode":
                    _, msg = session.toggle_dev_mode()
                    print(msg)
                elif command.startswith("reload "):
                    module_name = line[8:].strip()  # Get module name after ".reload "
                    _, msg = session.reload_module(module_name)
                    print(msg)
                elif command == "reloadall":
                    _, msg = session.reload_all_modules()
                    print(msg)
                elif command == "refresh":
                    _, msg = session.refresh_modules()
                    print(msg)
                elif command == "perfmon":
                    _, msg = session.get_performance_summary()
                    print(msg)
                elif command == "memreport":
                    _, msg = session.get_memory_report()
                    print(msg)
                else:
                    print(f"Unknown command: .{command}")
                    print("Type .help for available commands")
                continue

            # Check if line ends with opening brace (multi-line start)
            if line.rstrip().endswith("{"):
                buffer.append(line)
                continue

            # If we're in multi-line mode, add to buffer
            if buffer:
                buffer.append(line)
                # Check if line ends with closing brace (multi-line end)
                if line.rstrip().endswith("}"):
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


def show_capabilities(session: MLREPLSession):
    """Show all granted capabilities."""
    caps = session.get_capabilities()

    if not caps:
        print("No capabilities granted (security-restricted mode)")
        return

    print("Active Capabilities:")
    for cap in caps:
        print(f"  • {cap}")


def handle_grant_command(session: MLREPLSession, capability: str):
    """Handle .grant command with confirmation.

    Args:
        session: REPL session
        capability: Capability to grant
    """
    if not capability:
        print("Usage: .grant <capability>")
        print("Example: .grant file.read")
        return

    # Check if already granted
    if capability in session.granted_capabilities:
        print(f"Capability '{capability}' is already granted")
        return

    # Security confirmation
    print(f"\n⚠️  Security Warning: Granting capability '{capability}'")
    print("This will allow ML code to access restricted functionality.")
    response = input("Grant this capability? [y/N]: ")

    if response.lower() == "y":
        success = session.grant_capability(capability)
        if success:
            print(f"✓ Granted capability: {capability}")
        else:
            print(f"✗ Invalid capability name: {capability}")
            print("Capability names must be in format: module.action (e.g., file.read)")
    else:
        print("Cancelled.")


def handle_revoke_command(session: MLREPLSession, capability: str):
    """Handle .revoke command.

    Args:
        session: REPL session
        capability: Capability to revoke
    """
    if not capability:
        print("Usage: .revoke <capability>")
        print("Example: .revoke file.read")
        return

    success = session.revoke_capability(capability)
    if success:
        print(f"✓ Revoked capability: {capability}")
    else:
        print(f"✗ Capability '{capability}' is not granted")


def handle_retry_command(session: MLREPLSession, buffer: list[str]):
    """Handle .retry command to re-execute last failed statement.

    Args:
        session: REPL session
        buffer: Multi-line input buffer (will be cleared if retry executed)
    """
    if not session.last_failed_code:
        print("No previous error to retry")
        return

    print(f"Retrying: {session.last_failed_code}")
    result = session.execute_ml_line(session.last_failed_code)

    if result.success:
        if result.value is not None:
            print(f"=> {format_repl_value(result.value)}")
        print("✓ Success!")
    else:
        print(f"✗ Failed again: {result.error}")


def handle_edit_command(session: MLREPLSession):
    """Handle .edit command to edit last statement in external editor.

    Args:
        session: REPL session
    """
    import os
    import subprocess
    import tempfile

    # Get last executed code
    if not session.statements:
        print("No previous statement to edit")
        return

    last_code = session.statements[-1].ml_source

    # Write to temp file
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".ml", delete=False, encoding="utf-8"
    ) as f:
        f.write(last_code)
        temp_path = f.name

    try:
        # Open in editor
        editor = os.environ.get("EDITOR", "notepad" if os.name == "nt" else "vim")
        subprocess.call([editor, temp_path])

        # Read edited code
        with open(temp_path, "r", encoding="utf-8") as f:
            edited_code = f.read()

        # Execute edited code
        if edited_code.strip() and edited_code != last_code:
            print("Executing edited code...")
            result = session.execute_ml_line(edited_code)

            if result.success:
                if result.value is not None:
                    print(f"=> {format_repl_value(result.value)}")
                print("✓ Done")
            else:
                print(f"✗ Error: {result.error}")
        else:
            print("No changes made")

    finally:
        # Clean up temp file
        try:
            os.unlink(temp_path)
        except:
            pass


def print_help():
    """Print REPL help message."""
    print(
        """
REPL Commands:
  .help              Show this help message
  .vars              Show defined variables
  .clear, .reset     Clear session and reset namespace
  .history           Show command history
  .capabilities      Show granted capabilities
  .grant <cap>       Grant a capability (requires confirmation)
  .revoke <cap>      Revoke a capability
  .retry             Retry last failed command
  .edit              Edit last statement in external editor
  .modules           List all available modules
  .modinfo <name>    Show detailed info about a module
  .addpath <path>    Add extension directory for custom modules
  .exit, .quit       Exit REPL (or Ctrl+D)

Development Mode Commands:
  .devmode           Toggle development mode (performance monitoring)
  .reload <module>   Reload a specific module without restart
  .reloadall         Reload all currently loaded modules
  .refresh           Re-scan directories and reload all modules
  .perfmon           Show performance monitoring summary
  .memreport         Show memory usage report for loaded modules

Usage:
  - Type ML code and press Enter to execute
  - Results are displayed with => prefix
  - Variables persist across commands
  - Multi-line input: lines ending with { start a block
  - Empty line executes buffered multi-line input

Examples:
  ml> x = 42
  ml> x + 10
  => 52

  ml> function add(a, b) {
  ...   return a + b;
  ... }

  ml> add(5, 7)
  => 12

  ml> typeof(42)
  => "number"

  ml> arr = [1, 2, 3]
  ml> len(arr)
  => 3

Development Mode Examples:
  ml> .devmode
  Development mode: ENABLED

  ml> .perfmon
  Performance Summary:
    Total loads: 3
    Avg load time: 12.3ms

  ml> .reload math
  ✓ Reloaded module: math
"""
    )


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


def show_modules():
    """Show all available modules (both Python bridges and ML modules)."""
    from mlpy.stdlib.module_registry import get_registry, ModuleType

    registry = get_registry()
    all_modules = registry.get_all_modules()

    if not all_modules:
        print("No modules available")
        return

    # Separate modules by type
    python_modules = {}
    ml_modules = {}

    for name, metadata in all_modules.items():
        if metadata.module_type == ModuleType.PYTHON_BRIDGE:
            python_modules[name] = metadata
        elif metadata.module_type == ModuleType.ML_SOURCE:
            ml_modules[name] = metadata

    print(f"Available Modules ({len(all_modules)} total):")
    print()

    # Show Python bridge modules
    if python_modules:
        print(f"  Python Bridge Modules ({len(python_modules)}):")
        # Group by category
        categorized = {
            "Core": [],
            "Data": [],
            "I/O": [],
            "Utilities": [],
            "Other": [],
        }

        for mod_name in python_modules.keys():
            # Simple categorization based on name
            if mod_name in ["math", "random"]:
                categorized["Core"].append(mod_name)
            elif mod_name in ["json", "datetime", "collections", "functional"]:
                categorized["Data"].append(mod_name)
            elif mod_name in ["file", "console", "http", "path"]:
                categorized["I/O"].append(mod_name)
            elif mod_name in ["regex", "string"]:
                categorized["Utilities"].append(mod_name)
            else:
                categorized["Other"].append(mod_name)

        for category, mods in categorized.items():
            if mods:
                print(f"    {category}:")
                for mod in sorted(mods):
                    print(f"      • {mod}")

        print()

    # Show ML source modules
    if ml_modules:
        print(f"  ML Source Modules ({len(ml_modules)}):")
        for mod_name in sorted(ml_modules.keys()):
            print(f"    • {mod_name}")
        print()

    print("Use .modinfo <name> to get details about a specific module")


def show_module_info(module_name: str):
    """Show detailed information about a module (unified for all types)."""
    from mlpy.stdlib.module_registry import get_registry

    if not module_name:
        print("Usage: .modinfo <module_name>")
        print("Example: .modinfo math")
        return

    registry = get_registry()
    info = registry.get_module_info(module_name)

    if info is None:
        print(f"Module '{module_name}' not found")
        print()
        print("Use .modules to see all available modules")
        return

    # Display basic information
    print(f"Module: {info['name']}")
    print(f"Type: {info['type']}")
    print(f"File Path: {info['file_path']}")
    print(f"Loaded: {'Yes' if info['loaded'] else 'No'}")
    print(f"Reload Count: {info['reload_count']}")

    # Type-specific information
    if info['type'] == 'ml_source':
        print(f"Transpiled Path: {info.get('transpiled_path', 'N/A')}")
        print(f"Needs Recompilation: {'Yes' if info.get('needs_recompilation', False) else 'No'}")
        if 'source_modified' in info:
            print(f"Source Modified: {info['source_modified']}")

    if 'load_time_ms' in info:
        print(f"Load Time: {info['load_time_ms']:.2f}ms")

    print()

    # Show functions for Python bridge modules
    functions = info.get('functions', {})
    if functions:
        print(f"Functions ({len(functions)}):")
        for func_name, func_info in sorted(functions.items())[:10]:  # Show first 10
            desc = func_info.get('description', 'No description')
            print(f"  • {func_name}() - {desc}")

        if len(functions) > 10:
            print(f"  ... and {len(functions) - 10} more functions")
        print()

    # Show classes for Python bridge modules
    classes = info.get('classes', {})
    if classes:
        print(f"Classes ({len(classes)}):")
        for class_name, class_info in sorted(classes.items()):
            desc = class_info.get('description', 'No description')
            print(f"  • {class_name} - {desc}")
        print()


def add_extension_path(path: str):
    """Add an extension path for custom modules."""
    from mlpy.stdlib.module_registry import get_registry
    from pathlib import Path

    if not path:
        print("Usage: .addpath <directory_path>")
        print("Example: .addpath ./my_modules")
        return

    # Validate path
    path_obj = Path(path).resolve()

    if not path_obj.exists():
        print(f"Error: Path '{path}' does not exist")
        return

    if not path_obj.is_dir():
        print(f"Error: Path '{path}' is not a directory")
        return

    # Add to registry
    registry = get_registry()
    registry.add_extension_paths([str(path_obj)])

    print(f"✓ Added extension path: {path_obj}")
    print()
    print("Extension modules are now available for import")
    print("Use .modules to see all available modules")


if __name__ == "__main__":
    # Allow running directly for testing
    run_repl()
