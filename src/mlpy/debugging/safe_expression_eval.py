"""Safe expression evaluation for debugger.

This module provides secure evaluation of ML expressions in the debugger,
applying the same security principles as the main transpiler.
"""

from typing import Any, Optional
from mlpy.ml.grammar.parser import MLParser
from mlpy.ml.analysis.security_analyzer import SecurityAnalyzer
from mlpy.ml.codegen.python_generator import PythonCodeGenerator


class SafeExpressionEvaluator:
    """Secure expression evaluator for debugger conditions and watches.

    This evaluator:
    1. Parses expressions as ML code
    2. Runs security analysis
    3. Transpiles to Python with security
    4. Evaluates in restricted namespace
    """

    # Safe built-ins allowed in debugger expressions
    SAFE_BUILTINS = {
        # Type conversions
        'bool': bool,
        'int': int,
        'float': float,
        'str': str,
        # Collections
        'len': len,
        'list': list,
        'dict': dict,
        'tuple': tuple,
        'set': set,
        # Math
        'abs': abs,
        'min': min,
        'max': max,
        'sum': sum,
        'round': round,
        # Iteration
        'range': range,
        'enumerate': enumerate,
        'zip': zip,
        'all': all,
        'any': any,
        # Type checking
        'isinstance': isinstance,
        'type': type,
        # String
        'ord': ord,
        'chr': chr,
        # Comparison
        'sorted': sorted,
        'reversed': reversed,
    }

    def __init__(self):
        """Initialize the safe expression evaluator."""
        self.parser = MLParser()
        self.security_analyzer = SecurityAnalyzer()

    def evaluate(
        self,
        expression: str,
        local_vars: dict[str, Any],
        global_vars: dict[str, Any]
    ) -> tuple[Any, bool, str]:
        """Safely evaluate an ML expression.

        Args:
            expression: ML expression to evaluate (e.g., "x > 10")
            local_vars: Local variables from current frame
            global_vars: Global variables from current frame

        Returns:
            Tuple of (value, success, error_message)
            - value: Result of evaluation (or error message if failed)
            - success: True if evaluation succeeded
            - error_message: Error description if failed, empty string if succeeded
        """
        try:
            # Step 1: Parse as ML expression
            # Pre-declare all local variables so transpiler knows about them
            # ML uses simple assignment syntax: name = value;
            var_declarations = "\n".join(
                f"{name} = 0;" for name in local_vars.keys()
            )

            # Wrap in a simple statement so parser accepts it
            ml_code = f"{var_declarations}\n_debug_expr = {expression};"

            try:
                ast = self.parser.parse(ml_code, "<debugger>")
            except Exception as e:
                return None, False, f"Parse error: {str(e)}"

            # Step 2: Security analysis
            issues = self.security_analyzer.analyze(ast)

            # Filter out issues that are just warnings
            critical_issues = [
                issue for issue in issues
                if issue.severity in ("critical", "high")
            ]

            if critical_issues:
                # Security violation detected
                error_msg = f"Security violation: {critical_issues[0].message}"
                return None, False, error_msg

            # Step 3: Transpile to Python
            generator = PythonCodeGenerator(
                source_file="<debugger>",
                generate_source_maps=False
            )

            try:
                python_code, _ = generator.generate(ast)
            except Exception as e:
                return None, False, f"Transpilation error: {str(e)}"

            # Step 4: Clean generated code
            # Remove:
            # - Import statements (we'll provide runtime modules in namespace)
            # - Variable initialization lines (x=0, y=0) that overwrite real values
            # Keep only the expression assignment: _debug_expr = <expression>
            python_lines = python_code.split('\n')
            filtered_lines = []

            for line in python_lines:
                stripped = line.strip()

                # Skip import statements
                if stripped.startswith('from ') or stripped.startswith('import '):
                    continue

                # Skip variable initializations (but keep the _debug_expr line)
                if '=' in stripped and not stripped.startswith('_debug_expr'):
                    # Check if this is a simple variable initialization
                    # Format: "varname = 0" or "varname = None"
                    parts = stripped.split('=')
                    if len(parts) == 2:
                        var_name = parts[0].strip()
                        var_value = parts[1].strip()
                        # Skip if it's one of our pre-declared variables
                        if var_name in local_vars and (var_value == '0' or var_value == 'None'):
                            continue

                filtered_lines.append(line)

            cleaned_code = '\n'.join(filtered_lines)

            # Create safe namespace with runtime modules pre-imported
            safe_globals = self._create_safe_namespace(global_vars)
            safe_locals = dict(local_vars)  # Copy to avoid modification

            # Execute the generated code in restricted namespace
            try:
                exec(cleaned_code, safe_globals, safe_locals)
                result = safe_locals.get('_debug_expr')
                return result, True, ""
            except Exception as e:
                return None, False, f"Execution error: {str(e)}"

        except Exception as e:
            # Catch-all for unexpected errors
            return None, False, f"Unexpected error: {str(e)}"

    def _create_safe_namespace(self, global_vars: dict[str, Any]) -> dict[str, Any]:
        """Create a restricted namespace for expression evaluation.

        Args:
            global_vars: Global variables from current frame

        Returns:
            Safe namespace dictionary with restricted builtins
        """
        # Start with safe builtins only
        safe_namespace = {
            '__builtins__': self.SAFE_BUILTINS.copy(),
            '__name__': '__debugger__',
            '__doc__': None,
        }

        # Pre-import runtime modules needed by generated code
        # The transpiler wraps all function calls with _safe_call
        try:
            from mlpy.runtime.whitelist_validator import safe_call
            safe_namespace['_safe_call'] = safe_call
        except ImportError:
            # If runtime not available, create a passthrough wrapper
            safe_namespace['_safe_call'] = lambda func, *args, **kwargs: func(*args, **kwargs)

        # Import runtime helpers for property access, method calls, etc.
        try:
            from mlpy.stdlib.runtime_helpers import safe_attr_access, safe_method_call, get_safe_length
            safe_namespace['_safe_attr_access'] = safe_attr_access
            safe_namespace['_safe_method_call'] = safe_method_call
            safe_namespace['get_safe_length'] = get_safe_length
        except ImportError:
            # Provide minimal implementations
            safe_namespace['_safe_attr_access'] = lambda obj, attr: getattr(obj, attr)
            safe_namespace['_safe_method_call'] = lambda obj, method, *args, **kwargs: getattr(obj, method)(*args, **kwargs)
            safe_namespace['get_safe_length'] = len

        # Import builtin module for len(), max(), etc.
        # Generated code uses: builtin.len, builtin.max, etc.
        try:
            from mlpy.stdlib.builtin import builtin
            safe_namespace['builtin'] = builtin
        except ImportError:
            # Provide a minimal builtin object with safe functions
            class MinimalBuiltin:
                len = len
                max = max
                min = min
                sum = sum
                abs = abs
                int = int
                float = float
                str = str
                bool = bool
            safe_namespace['builtin'] = MinimalBuiltin()

        # Add safe global variables (filter out dangerous ones)
        for name, value in global_vars.items():
            # Skip module objects and dangerous names
            if name.startswith('__'):
                continue
            if name in ('eval', 'exec', 'compile', 'open', '__import__'):
                continue
            # Skip module types
            if hasattr(value, '__file__'):
                continue

            safe_namespace[name] = value

        return safe_namespace

    def evaluate_simple(
        self,
        expression: str,
        local_vars: dict[str, Any],
        global_vars: dict[str, Any]
    ) -> Any:
        """Simplified evaluation that returns value or None on error.

        This is a convenience wrapper around evaluate() that's easier to use
        for simple cases where you just want the value.

        Args:
            expression: ML expression to evaluate
            local_vars: Local variables
            global_vars: Global variables

        Returns:
            Evaluated value, or None if evaluation failed
        """
        value, success, _ = self.evaluate(expression, local_vars, global_vars)
        return value if success else None


# Singleton instance for use throughout debugger
_evaluator_instance: Optional[SafeExpressionEvaluator] = None


def get_safe_evaluator() -> SafeExpressionEvaluator:
    """Get the singleton safe expression evaluator."""
    global _evaluator_instance
    if _evaluator_instance is None:
        _evaluator_instance = SafeExpressionEvaluator()
    return _evaluator_instance
