"""Expression generation helper methods for code generation.

This mixin provides helper methods for generating Python code from ML expressions.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mlpy.ml.grammar.ast_nodes import Expression, SliceExpression


class ExpressionHelpersMixin:
    """Mixin providing expression generation helper methods.

    This mixin contains helper methods for:
    - Expression type detection and analysis
    - Slice expression generation
    - Assignment target generation
    - Safe attribute access
    - Runtime helper imports
    """

    # ========================================================================
    # Expression Analysis Helpers
    # ========================================================================

    def _could_be_string_expression(self, expr: 'Expression') -> bool:
        """Check if an expression could evaluate to a string value."""
        from mlpy.ml.grammar.ast_nodes import BinaryExpression, StringLiteral

        if isinstance(expr, StringLiteral):
            return True

        # If it's a binary expression with +, and either operand could be a string,
        # then the whole expression could be a string concatenation
        if isinstance(expr, BinaryExpression) and expr.operator == "+":
            return self._could_be_string_expression(expr.left) or self._could_be_string_expression(
                expr.right
            )

        # For all other expressions (numbers, identifiers, function calls, etc.),
        # assume they are NOT strings unless proven otherwise.
        # This is a more conservative approach that avoids converting math operations to strings.
        return False

    def _detect_object_type(self, expr: 'Expression') -> type | None:
        """Compile-time type detection for expressions."""
        from mlpy.ml.grammar.ast_nodes import (
            ArrayLiteral,
            BooleanLiteral,
            Identifier,
            NumberLiteral,
            ObjectLiteral,
            StringLiteral,
        )

        if isinstance(expr, StringLiteral):
            return str
        elif isinstance(expr, ArrayLiteral):
            return list
        elif isinstance(expr, ObjectLiteral):
            return dict
        elif isinstance(expr, NumberLiteral):
            return int if isinstance(expr.value, int) else float
        elif isinstance(expr, BooleanLiteral):
            return bool
        elif isinstance(expr, Identifier):
            # Try to infer from context/assignments (future enhancement)
            return None
        return None

    def _is_safe_builtin_access(self, obj_type: type, attr_name: str) -> bool:
        """Check if builtin type access is safe."""
        from mlpy.ml.codegen.safe_attribute_registry import get_safe_registry
        registry = get_safe_registry()
        return registry.is_safe_access(obj_type, attr_name)

    def _is_ml_object_pattern(self, expr: 'Expression') -> bool:
        """Determine if expression represents an ML object (dictionary pattern)."""
        from mlpy.ml.grammar.ast_nodes import ObjectLiteral

        # ML objects are typically ObjectLiterals or identifiers that might be objects
        if isinstance(expr, ObjectLiteral):
            return True
        # Could add more sophisticated analysis here
        return False

    # ========================================================================
    # Code Generation Helpers
    # ========================================================================

    def _generate_slice(self, slice_expr: 'SliceExpression') -> str:
        """Generate Python slice notation from SliceExpression."""
        # Generate each part (empty string if None)
        start_code = self._generate_expression(slice_expr.start) if slice_expr.start else ""
        end_code = self._generate_expression(slice_expr.end) if slice_expr.end else ""
        step_code = self._generate_expression(slice_expr.step) if slice_expr.step else ""

        # Build slice notation
        if step_code:
            return f"{start_code}:{end_code}:{step_code}"
        else:
            return f"{start_code}:{end_code}"

    def _generate_assignment_target(self, expr: 'Expression') -> str:
        """Generate assignment target code (preserves original dictionary access for ML objects)."""
        from mlpy.ml.grammar.ast_nodes import ArrayAccess, MemberAccess

        if isinstance(expr, ArrayAccess):
            # Array assignment: arr[index] = value
            array_code = self._generate_expression(expr.array)
            index_code = self._generate_expression(expr.index)
            return f"{array_code}[{index_code}]"
        elif isinstance(expr, MemberAccess):
            # Member assignment: obj.property = value
            obj_code = self._generate_expression(expr.object)
            if isinstance(expr.member, str):
                # For assignments, always use dictionary access for ML objects
                # This preserves the original behavior where obj.prop = val becomes obj['prop'] = val
                member_key = repr(expr.member)  # Properly quote the key
                return f"{obj_code}[{member_key}]"
            else:
                # Dynamic member assignment
                member = self._generate_expression(expr.member)
                return f"{obj_code}[{member}]"
        else:
            # Fall back to expression generation for other types
            return self._generate_expression(expr)

    def _generate_safe_attribute_access(self, obj_code: str, attr_name: str, obj_type: type) -> str:
        """Generate safe attribute access code."""
        # Direct Python attribute access for whitelisted methods
        return f"{obj_code}.{attr_name}"

    # ========================================================================
    # Import Management
    # ========================================================================

    def _ensure_runtime_helpers_imported(self) -> None:
        """Ensure runtime helpers are imported for safe attribute access."""
        if not self.context.runtime_helpers_imported:
            self.context.runtime_helpers_imported = True
            self.context.imports_needed.add("mlpy.stdlib.runtime_helpers")

    # ========================================================================
    # Main Expression Generation
    # ========================================================================

    def _generate_expression(self, expr: 'Expression') -> str:
        """Generate Python code for an expression.

        This is the main expression generation method that handles all expression types.
        It delegates to visitor methods for complex constructs like arrow functions.
        """
        from mlpy.ml.grammar.ast_nodes import (
            ArrayAccess,
            ArrayLiteral,
            ArrowFunction,
            BinaryExpression,
            BooleanLiteral,
            FunctionCall,
            FunctionDefinition,
            Identifier,
            MemberAccess,
            NumberLiteral,
            ObjectLiteral,
            SliceExpression,
            StringLiteral,
            TernaryExpression,
            UnaryExpression,
        )

        if expr is None:
            return "None"

        if isinstance(expr, BinaryExpression):
            left = self._generate_expression(expr.left)
            right = self._generate_expression(expr.right)
            # Map ML operators to Python operators
            op_map = {
                "&&": "and",
                "||": "or",
                "==": "==",
                "!=": "!=",
                "<=": "<=",
                ">=": ">=",
                "<": "<",
                ">": ">",
                "+": "+",
                "-": "-",
                "*": "*",
                "/": "/",
                "//": "//",
                "%": "%",
            }
            python_op = op_map.get(expr.operator, expr.operator)

            # Special handling for string concatenation with + operator
            if expr.operator == "+":
                # Check if either operand could be a string (literal or complex expression)
                left_could_be_string = self._could_be_string_expression(expr.left)
                right_could_be_string = self._could_be_string_expression(expr.right)

                # If at least one operand could be a string, wrap both in str() to handle type coercion
                if left_could_be_string or right_could_be_string:
                    return f"(str({left}) + str({right}))"

            return f"({left} {python_op} {right})"

        elif isinstance(expr, UnaryExpression):
            operand = self._generate_expression(expr.operand)
            op_map = {"!": "not", "-": "-", "+": "+"}
            python_op = op_map.get(expr.operator, expr.operator)
            # No space for +/- operators, space for 'not'
            if python_op in ("-", "+"):
                return f"({python_op}{operand})"
            else:
                return f"({python_op} {operand})"

        elif isinstance(expr, Identifier):
            # Validate identifier and route appropriately
            name = expr.name

            # Check if identifier is known in current scope
            # 1. User-defined variables
            if name in self.symbol_table['variables']:
                return self._safe_identifier(name)

            # 2. User-defined functions
            if name in self.symbol_table['functions']:
                return self._safe_identifier(name)

            # 3. Function parameters (check all scopes in stack)
            for param_scope in self.symbol_table['parameters']:
                if name in param_scope:
                    return self._safe_identifier(name)

            # 4. Imported modules
            if name in self.symbol_table['imports']:
                return self._safe_identifier(name)

            # 5. ML builtin functions - route to builtin module
            if name in self.symbol_table['ml_builtins']:
                self.context.builtin_functions_used.add(name)
                return f"builtin.{name}"

            # 5.5. ML language literals (null, undefined, etc.)
            if name == "null":
                return "None"
            if name == "undefined":
                return "None"

            # 6. REPL mode - allow undefined identifiers (will be checked at runtime)
            if self.repl_mode:
                # Extra security: block dangerous Python built-ins even in REPL mode
                dangerous_identifiers = {
                    # Code execution
                    'eval', 'exec', 'compile', '__import__', 'vars', 'globals', 'locals',
                    'dir', 'getattr', 'setattr', 'delattr', 'hasattr',
                    # Reflection abuse
                    '__dict__', '__bases__', '__subclasses__', '__mro__', '__class__', '__builtins__',
                    # Code object access
                    '__code__', '__globals__', '__closure__',
                    # Module internals
                    '__name__', '__file__', '__package__', '__path__',
                    # Dangerous builtins (open can be dangerous, __input__ is Python internal)
                    # Note: 'input' and 'help' are excluded - they're safe ML builtin wrappers
                    'open', '__input__',
                    # System access
                    'exit', 'quit', 'copyright', 'credits', 'license'
                }

                if name in dangerous_identifiers:
                    raise ValueError(
                        f"Security: Direct access to '{name}' is not allowed.\n"
                        f"This identifier provides access to Python internals and bypasses ML security.\n"
                        f"Suggestions:\n"
                        f"  - Use ML standard library functions instead\n"
                        f"  - Request appropriate capabilities for system access\n"
                        f"  - Avoid direct Python namespace manipulation"
                    )

                # In REPL mode, assume unknown identifiers are variables from previous statements
                # Python's runtime will raise NameError if the variable truly doesn't exist
                return self._safe_identifier(name)

            # 7. Unknown identifier - SECURITY: Block at compile time
            # This prevents access to Python builtins like eval, exec, open, __import__
            raise ValueError(
                f"Unknown identifier '{name}' at line {expr.line if hasattr(expr, 'line') else '?'}. "
                f"Not a variable, function, parameter, import, or ML builtin. "
                f"\n\nPossible causes:"
                f"\n  - Typo in identifier name"
                f"\n  - Python builtin (use ML stdlib instead: e.g., builtin.len())"
                f"\n  - Undefined variable (ensure it's assigned before use)"
                f"\n\nKnown identifiers:"
                f"\n  Variables: {sorted(list(self.symbol_table['variables']))[:5]}"
                f"\n  Functions: {sorted(list(self.symbol_table['functions']))[:5]}"
                f"\n  Imports: {sorted(list(self.symbol_table['imports']))[:5]}"
                f"\n  ML builtins: abs, len, max, min, sum, ... (use via calls: abs(-5))"
            )

        elif isinstance(expr, FunctionCall):
            # Delegate to function call generation (remains in main class)
            return self._generate_function_call_wrapped(expr)

        elif isinstance(expr, ArrayAccess):
            array_code = self._generate_expression(expr.array)
            # Check if index is a slice expression
            if isinstance(expr.index, SliceExpression):
                index_code = self._generate_slice(expr.index)
            else:
                index_code = self._generate_expression(expr.index)
            return f"{array_code}[{index_code}]"

        elif isinstance(expr, SliceExpression):
            # This shouldn't be called directly, but handle it just in case
            return self._generate_slice(expr)

        elif isinstance(expr, MemberAccess):
            obj_code = self._generate_expression(expr.object)
            # Handle member as either string or expression
            if isinstance(expr.member, str):
                # 0. NEW: Check if accessing builtin module and track usage
                if isinstance(expr.object, Identifier) and expr.object.name == "builtin":
                    # Track builtin module usage for auto-import
                    self.context.builtin_functions_used.add(expr.member)

                # 1. Check if object is an imported module (existing logic)
                is_imported_module = False
                if (
                    isinstance(expr.object, Identifier)
                    and expr.object.name in self.context.imported_modules
                ):
                    is_imported_module = True
                    # Check if there's a variable mapping for this module (e.g. collections -> ml_collections)
                    if expr.object.name in self.context.variable_mappings:
                        obj_code = self.context.variable_mappings[expr.object.name]

                # 0b. NEW: Also check if accessing builtin (needs to be treated as imported module)
                if isinstance(expr.object, Identifier) and expr.object.name == "builtin":
                    is_imported_module = True

                if is_imported_module:
                    # Use dot notation for imported modules (e.g., ml_collections.append)
                    return f"{obj_code}.{expr.member}"

                # 2. NEW: Detect compile-time type for safe attribute access
                obj_type = self._detect_object_type(expr.object)

                if obj_type and self._is_safe_builtin_access(obj_type, expr.member):
                    # 3. NEW: Direct Python attribute access for safe built-ins
                    return self._generate_safe_attribute_access(obj_code, expr.member, obj_type)

                elif obj_type is dict or self._is_ml_object_pattern(expr.object):
                    # 4. ML objects use dictionary access (existing)
                    member_key = repr(expr.member)  # Properly quote the key
                    return f"{obj_code}[{member_key}]"

                else:
                    # 5. NEW: Runtime type checking for unknown objects
                    self._ensure_runtime_helpers_imported()
                    return f"_safe_attr_access({obj_code}, {repr(expr.member)})"
            else:
                # Dynamic member access (e.g., obj[computed_key])
                member = self._generate_expression(expr.member)
                return f"{obj_code}[{member}]"

        elif isinstance(expr, NumberLiteral):
            return str(expr.value)

        elif isinstance(expr, StringLiteral):
            # Escape Python string literals properly
            escaped = repr(expr.value)
            return escaped

        elif isinstance(expr, BooleanLiteral):
            return "True" if expr.value else "False"

        elif isinstance(expr, ArrayLiteral):
            elements = [self._generate_expression(elem) for elem in expr.elements]
            return f"[{', '.join(elements)}]"

        elif isinstance(expr, ObjectLiteral):
            properties = []
            for key, value in expr.properties.items():
                # Handle key properly - could be string or Identifier
                if isinstance(key, str):
                    key_str = repr(key)  # String literal key
                elif hasattr(key, "name"):
                    key_str = repr(key.name)  # Identifier key
                else:
                    key_str = repr(str(key))
                value_str = self._generate_expression(value)
                properties.append(f"{key_str}: {value_str}")
            return f"{{{', '.join(properties)}}}"

        elif isinstance(expr, ArrowFunction):
            # Handle arrow functions by calling the visitor method (remains in main class)
            return self.visit_arrow_function(expr)

        elif isinstance(expr, FunctionDefinition):
            # Handle function definitions as lambda expressions when used in expressions
            # Delegate to lambda generation (remains in main class for now)
            return self._generate_lambda_from_function_def(expr)

        elif isinstance(expr, TernaryExpression):
            # Handle ternary expressions (condition ? true_value : false_value)
            condition_code = self._generate_expression(expr.condition)
            true_code = self._generate_expression(expr.true_value)
            false_code = self._generate_expression(expr.false_value)
            # Python ternary syntax: true_value if condition else false_value
            return f"{true_code} if {condition_code} else {false_code}"

        else:
            return f"# UNKNOWN_EXPRESSION: {type(expr).__name__}"


__all__ = ['ExpressionHelpersMixin']
