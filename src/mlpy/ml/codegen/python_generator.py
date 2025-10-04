"""Python code generator from ML AST with source map support."""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from mlpy.ml.grammar.ast_nodes import *
from mlpy.runtime.profiling.decorators import profile_parser

from .safe_attribute_registry import get_safe_registry
from .allowed_functions_registry import AllowedFunctionsRegistry


@dataclass
class SourceMapping:
    """Source map entry linking generated Python to original ML."""

    generated_line: int
    generated_column: int
    original_line: int | None = None
    original_column: int | None = None
    original_file: str | None = None
    name: str | None = None


@dataclass
class CodeGenerationContext:
    """Context for code generation with tracking."""

    indentation_level: int = 0
    current_line: int = 1
    current_column: int = 0
    source_mappings: list[SourceMapping] = field(default_factory=list)
    variable_mappings: dict[str, str] = field(default_factory=dict)
    function_mappings: dict[str, str] = field(default_factory=dict)
    imports_needed: set = field(default_factory=set)
    imported_modules: set[str] = field(default_factory=set)
    runtime_helpers_imported: bool = False
    builtin_functions_used: set[str] = field(default_factory=set)  # Track which builtins are called


class PythonCodeGenerator(ASTVisitor):
    """Generates Python code from ML AST with security and source map support."""

    def __init__(self, source_file: str | None = None, generate_source_maps: bool = True):
        """Initialize Python code generator.

        Args:
            source_file: Source ML file path for source maps
            generate_source_maps: Whether to generate source map data
        """
        self.source_file = source_file
        self.generate_source_maps = generate_source_maps
        self.context = CodeGenerationContext()
        self.output_lines: list[str] = []
        self.function_registry = AllowedFunctionsRegistry()  # Whitelist enforcement

    @profile_parser
    def generate(self, ast: Program) -> tuple[str, dict[str, Any] | None]:
        """Generate Python code from ML AST.

        Args:
            ast: Root Program AST node

        Returns:
            Tuple of (Python code string, source map data)
        """
        self.context = CodeGenerationContext()
        self.output_lines = []
        self.function_registry = AllowedFunctionsRegistry()  # Fresh registry for each compilation

        # First pass: analyze AST to determine what imports are needed
        temp_context = self.context
        temp_registry = self.function_registry
        ast.accept(self)

        # Reset for actual generation (preserve registry with user functions/imports)
        self.context = temp_context
        self.function_registry = temp_registry
        self.output_lines = []

        # Generate header
        self._emit_header()

        # Auto-import builtin module if any builtin functions were used
        if self.context.builtin_functions_used:
            self._emit_line("from mlpy.stdlib.builtin import builtin")
            self._emit_line("")

        # Generate imports if needed (but exclude contextlib as it's in header)
        remaining_imports = self.context.imports_needed - {"contextlib"}
        if remaining_imports:
            for import_name in sorted(remaining_imports):
                # Handle both "import xyz" and "from xyz import abc" statements
                if import_name.startswith("from ") or import_name.startswith("import "):
                    self._emit_line(import_name)
                elif import_name == "mlpy.stdlib.runtime_helpers":
                    # Special handling for runtime helpers to import specific functions
                    self._emit_line(
                        "from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access, get_safe_length"
                    )
                else:
                    self._emit_line(f"import {import_name}")
            self._emit_line("")

        # Generate main code
        ast.accept(self)

        # Generate footer
        self._emit_footer()

        # Combine output
        python_code = "\n".join(self.output_lines)

        # Generate source map
        source_map = self._generate_source_map() if self.generate_source_maps else None

        return python_code, source_map

    def _emit_header(self):
        """Emit Python file header."""
        self._emit_line('"""Generated Python code from mlpy ML transpiler."""')
        self._emit_line("")
        self._emit_line("# This code was automatically generated from ML source")
        self._emit_line("# Modifications to this file may be lost on regeneration")
        self._emit_line("")

        # Add contextlib import if capabilities are present
        if "contextlib" in self.context.imports_needed:
            self._emit_line("import contextlib")
            self._emit_line("")

    def _emit_imports(self):
        """Emit necessary Python imports."""
        for import_name in sorted(self.context.imports_needed):
            # Handle both "import xyz" and "from xyz import abc" statements
            if import_name.startswith("from ") or import_name.startswith("import "):
                self._emit_line(import_name)
            elif import_name == "mlpy.stdlib.runtime_helpers":
                # Special handling for runtime helpers to import specific functions
                self._emit_line(
                    "from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access, get_safe_length"
                )
            else:
                self._emit_line(f"import {import_name}")

    def _emit_footer(self):
        """Emit Python file footer."""
        self._emit_line("")
        self._emit_line("# End of generated code")

    def _emit_line(self, line: str, original_node: ASTNode | None = None):
        """Emit a line of Python code with source mapping."""
        self.output_lines.append(self._get_indentation() + line)

        if self.generate_source_maps and original_node:
            mapping = SourceMapping(
                generated_line=len(self.output_lines),
                generated_column=self.context.indentation_level * 4,
                original_line=original_node.line,
                original_column=original_node.column,
                original_file=self.source_file,
            )
            self.context.source_mappings.append(mapping)

    def _emit_raw_line(self, line: str):
        """Emit a raw line without indentation."""
        self.output_lines.append(line)

    def _get_indentation(self) -> str:
        """Get current indentation string."""
        return "    " * self.context.indentation_level

    def _indent(self):
        """Increase indentation level."""
        self.context.indentation_level += 1

    def _dedent(self):
        """Decrease indentation level."""
        self.context.indentation_level = max(0, self.context.indentation_level - 1)

    def _safe_identifier(self, name: str) -> str:
        """Convert ML identifier to safe Python identifier."""
        # Handle non-string inputs defensively
        if not isinstance(name, str):
            return f"ml_unknown_identifier_{id(name)}"

        # Handle ML-specific literals that need conversion to Python equivalents
        if name == "null":
            return "None"

        # Handle Python keywords and reserved names
        python_keywords = {
            "and",
            "as",
            "assert",
            "break",
            "class",
            "continue",
            "def",
            "del",
            "elif",
            "else",
            "except",
            "finally",
            "for",
            "from",
            "global",
            "if",
            "import",
            "in",
            "is",
            "lambda",
            "not",
            "or",
            "pass",
            "raise",
            "return",
            "try",
            "while",
            "with",
            "yield",
            "None",
            "True",
            "False",
        }

        if name in python_keywords:
            return f"ml_{name}"

        # Ensure valid Python identifier
        if not name.isidentifier():
            # Replace invalid characters with underscores
            safe_name = "".join(c if c.isalnum() or c == "_" else "_" for c in name)
            if safe_name[0].isdigit():
                safe_name = f"ml_{safe_name}"
            return safe_name

        return name

    def _generate_source_map(self) -> dict[str, Any]:
        """Generate source map data."""
        return {
            "version": 3,
            "file": f"{Path(self.source_file).stem}.py" if self.source_file else "generated.py",
            "sourceRoot": "",
            "sources": [self.source_file] if self.source_file else ["unknown.ml"],
            "names": [],
            "mappings": self._encode_mappings(),
            "sourcesContent": [self._get_source_content()] if self.source_file else [None],
        }

    def _encode_mappings(self) -> str:
        """Encode source mappings to VLQ format (simplified)."""
        # For now, return a simplified mapping representation
        # In a full implementation, this would use VLQ base64 encoding
        return json.dumps(
            [
                {
                    "generated": {"line": m.generated_line, "column": m.generated_column},
                    "original": {"line": m.original_line, "column": m.original_column},
                    "source": m.original_file,
                    "name": m.name,
                }
                for m in self.context.source_mappings
                if m.original_line is not None
            ]
        )

    def _get_source_content(self) -> str | None:
        """Get original source content for source map."""
        if not self.source_file:
            return None

        try:
            return Path(self.source_file).read_text(encoding="utf-8")
        except Exception:
            return None

    # AST Visitor Methods

    def visit_program(self, node: Program):
        """Generate code for program root."""
        for item in node.items:
            if item:
                item.accept(self)
                # Add spacing between top-level items
                if item != node.items[-1]:
                    self._emit_raw_line("")

    def visit_capability_declaration(self, node: CapabilityDeclaration):
        """Generate code for capability declaration."""
        # Add necessary imports for capability system
        self.context.imports_needed.add("contextlib")

        # Generate capability token creation
        capability_name = self._safe_identifier(node.name)

        self._emit_line(f"# Capability declaration: {node.name}", node)

        # Collect resource patterns and permissions from capability items
        resource_patterns = []
        permissions = set()

        for item in node.items:
            if hasattr(item, "pattern"):  # ResourcePattern
                resource_patterns.append(item.pattern.strip("\"'"))
            elif hasattr(item, "permission_type"):  # PermissionGrant
                permissions.add(item.permission_type)

        # Generate capability token creation function
        self._emit_line(f"def _create_{capability_name}_capability():")
        self._indent()
        self._emit_line(f'"""Create capability token for {node.name}."""')
        self._emit_line("from mlpy.runtime.capabilities import create_capability_token")
        self._emit_line("return create_capability_token(")
        self._indent()
        self._emit_line(f'capability_type="{node.name}",')
        if resource_patterns:
            patterns_str = ", ".join(f'"{p}"' for p in resource_patterns)
            self._emit_line(f"resource_patterns=[{patterns_str}],")
        if permissions:
            perms_str = ", ".join(f'"{p}"' for p in permissions)
            self._emit_line(f"allowed_operations={{{perms_str}}},")
        self._emit_line(f'description="Generated capability for {node.name}"')
        self._dedent()
        self._emit_line(")")
        self._dedent()
        self._emit_line("")

        # Generate context manager function
        self._emit_line("@contextlib.contextmanager")
        self._emit_line(f"def {capability_name}_context():")
        self._indent()
        self._emit_line(f'"""Capability context manager for {node.name}."""')
        self._emit_line("from mlpy.runtime.capabilities import get_capability_manager")
        self._emit_line("manager = get_capability_manager()")
        self._emit_line(f"token = _create_{capability_name}_capability()")
        self._emit_line(f'with manager.capability_context("{node.name}_context", [token]):')
        self._indent()
        self._emit_line("yield")
        self._dedent()
        self._dedent()
        self._emit_line("")

    def visit_resource_pattern(self, node: ResourcePattern):
        """Generate code for resource pattern."""
        self._emit_line(f"# Resource pattern: {node.pattern}", node)

    def visit_permission_grant(self, node: PermissionGrant):
        """Generate code for permission grant."""
        target_str = f" to {node.target}" if node.target else ""
        self._emit_line(f"# Grant {node.permission_type} permission{target_str}", node)

    def visit_import_statement(self, node: ImportStatement):
        """Generate code for import statement."""
        module_path = ".".join(node.target)

        # Map ML imports to Python equivalents where possible
        if module_path in [
            "math",
            "json",
            "datetime",
            "random",
            "collections",
            "console",
            "string",
            "array",
            "functional",
            "regex",
        ]:
            # Register import in whitelist registry
            alias = node.alias if node.alias else None
            if self.function_registry.register_import(module_path, alias):
                # ML standard library modules - import from mlpy.stdlib with _bridge suffix to avoid collisions
                python_module_path = f"mlpy.stdlib.{module_path}_bridge"

                if node.alias:
                    alias_name = self._safe_identifier(node.alias)
                    self._emit_line(
                        f"from {python_module_path} import {module_path} as {alias_name}", node
                    )
                    # Track the alias name as an imported module
                    self.context.imported_modules.add(alias_name)
                else:
                    # Import with original name - bridge modules use underscore prefix for Python imports
                    # (e.g., "import re as _re" in bridge) to avoid collisions, so we can use clean names
                    self._emit_line(f"from {python_module_path} import {module_path}", node)
                    # Track the module name as imported
                    self.context.imported_modules.add(module_path)
            else:
                # Module not found in registry - block it
                self._emit_line(f"# ERROR: Module '{module_path}' not found in stdlib", node)
        else:
            # Unknown modules get a runtime import check
            self._emit_line(f"# WARNING: Import '{module_path}' requires security review", node)
            self._emit_line(f"# import {module_path}", node)

    def visit_function_definition(self, node: FunctionDefinition):
        """Generate code for function definition."""
        func_name = self._safe_identifier(
            node.name.name if hasattr(node.name, "name") else str(node.name)
        )

        # Register user-defined function in whitelist
        self.function_registry.register_user_function(func_name)

        # Build parameter list
        params = []
        for param in node.parameters:
            if hasattr(param, "name"):
                param_name = self._safe_identifier(param.name)
                if hasattr(param, "type_annotation") and param.type_annotation:
                    params.append(f"{param_name}: {param.type_annotation}")
                else:
                    params.append(param_name)
            else:
                # Fallback for malformed parameters
                params.append("param")

        param_str = ", ".join(params)
        self._emit_line(f"def {func_name}({param_str}):", node)

        self._indent()

        # Generate function body
        if node.body:
            for stmt in node.body:
                if stmt:
                    stmt.accept(self)
        else:
            self._emit_line("pass")

        self._dedent()

    def visit_parameter(self, node: Parameter):
        """Visit parameter - handled by function definition."""
        pass

    def visit_expression_statement(self, node: ExpressionStatement):
        """Generate code for expression statement."""
        if node.expression:
            expr_code = self._generate_expression(node.expression)
            self._emit_line(expr_code, node)

    def visit_assignment_statement(self, node: AssignmentStatement):
        """Generate code for assignment statement."""
        # Handle different assignment target types
        if isinstance(node.target, str):
            # Simple variable assignment (legacy support)
            target_code = self._safe_identifier(node.target)
        elif hasattr(node.target, "name"):
            # Identifier node
            target_code = self._safe_identifier(node.target.name)
        else:
            # ArrayAccess or MemberAccess - generate as assignment target (NOT expression)
            target_code = self._generate_assignment_target(node.target)

        value_code = self._generate_expression(node.value)
        self._emit_line(f"{target_code} = {value_code}", node)

    def visit_return_statement(self, node: ReturnStatement):
        """Generate code for return statement."""
        if node.value:
            value_code = self._generate_expression(node.value)
            self._emit_line(f"return {value_code}", node)
        else:
            self._emit_line("return", node)

    def visit_block_statement(self, node: BlockStatement):
        """Generate code for block statement."""
        # If block is empty, emit pass to avoid IndentationError
        if not node.statements:
            self._emit_line("pass")
        else:
            for stmt in node.statements:
                if stmt:
                    stmt.accept(self)

    def visit_if_statement(self, node: IfStatement):
        """Generate code for if statement."""
        condition_code = self._generate_expression(node.condition)
        self._emit_line(f"if {condition_code}:", node)

        self._indent()
        if node.then_statement:
            node.then_statement.accept(self)
        else:
            self._emit_line("pass")
        self._dedent()

        # Generate elif clauses
        if hasattr(node, "elif_clauses") and node.elif_clauses:
            for elif_clause in node.elif_clauses:
                elif_clause.accept(self)

        if node.else_statement:
            self._emit_line("else:")
            self._indent()
            node.else_statement.accept(self)
            self._dedent()

    def visit_elif_clause(self, node):
        """Generate code for elif clause."""
        condition_code = self._generate_expression(node.condition)
        self._emit_line(f"elif {condition_code}:", node)

        self._indent()
        if node.statement:
            node.statement.accept(self)
        else:
            self._emit_line("pass")
        self._dedent()

    def visit_while_statement(self, node: WhileStatement):
        """Generate code for while statement."""
        condition_code = self._generate_expression(node.condition)
        self._emit_line(f"while {condition_code}:", node)

        self._indent()
        if node.body:
            node.body.accept(self)
        else:
            self._emit_line("pass")
        self._dedent()

    def visit_for_statement(self, node: ForStatement):
        """Generate code for for statement."""
        # Handle variable name - could be string or Identifier node
        if isinstance(node.variable, str):
            var_name = self._safe_identifier(node.variable)
        elif hasattr(node.variable, "name"):
            var_name = self._safe_identifier(node.variable.name)
        else:
            var_name = self._safe_identifier(str(node.variable))

        iterable_code = self._generate_expression(node.iterable)
        self._emit_line(f"for {var_name} in {iterable_code}:", node)

        self._indent()
        if node.body:
            node.body.accept(self)
        else:
            self._emit_line("pass")
        self._dedent()

    def visit_try_statement(self, node: TryStatement):
        """Generate code for try/except/finally statement."""
        self._emit_line("try:", node)

        self._indent()
        if node.try_body:
            for stmt in node.try_body:
                stmt.accept(self)
        else:
            self._emit_line("pass")
        self._dedent()

        # Generate except clauses
        for except_clause in node.except_clauses:
            except_clause.accept(self)

        # Generate finally clause
        if node.finally_body is not None:
            self._emit_line("finally:")
            self._indent()
            if node.finally_body:
                for stmt in node.finally_body:
                    stmt.accept(self)
            else:
                self._emit_line("pass")
            self._dedent()

    def visit_except_clause(self, node: ExceptClause):
        """Generate code for except clause."""
        if node.exception_variable:
            # ML syntax: except (error) -> Python syntax: except Exception as error
            self._emit_line(f"except Exception as {node.exception_variable}:", node)
        else:
            self._emit_line("except:", node)

        self._indent()
        if node.body:
            for stmt in node.body:
                stmt.accept(self)
        else:
            self._emit_line("pass")
        self._dedent()

    def visit_break_statement(self, node: BreakStatement):
        """Generate code for break statement."""
        self._emit_line("break", node)

    def visit_continue_statement(self, node: ContinueStatement):
        """Generate code for continue statement."""
        self._emit_line("continue", node)

    def visit_nonlocal_statement(self, node: NonlocalStatement):
        """Generate code for nonlocal statement."""
        variables = ", ".join(node.variables)
        self._emit_line(f"nonlocal {variables}", node)

    def visit_throw_statement(self, node: ThrowStatement):
        """Generate code for throw statement."""
        # Import MLUserException if needed
        self.context.imports_needed.add("from mlpy.ml.errors.exceptions import MLUserException")

        # Generate the dictionary argument
        dict_code = self._generate_expression(node.error_data)

        # Emit the raise statement
        self._emit_line(f"raise MLUserException({dict_code})", node)

    def _could_be_string_expression(self, expr: Expression) -> bool:
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

    def _generate_expression(self, expr: Expression) -> str:
        """Generate Python code for an expression."""
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
            return self._safe_identifier(expr.name)

        elif isinstance(expr, FunctionCall):
            # Handle different function call types with whitelist enforcement
            if isinstance(expr.function, MemberAccess):
                # Member function call: module.function() or object.method()
                return self._generate_member_function_call(expr.function, expr.arguments)
            elif isinstance(expr.function, Identifier):
                # Simple function call: function()
                return self._generate_simple_function_call(expr.function.name, expr.arguments)
            elif isinstance(expr.function, str):
                # Legacy string function name
                return self._generate_simple_function_call(expr.function, expr.arguments)
            else:
                # Complex expression as function (e.g., lambda call)
                func_code = self._generate_expression(expr.function)
                args = [self._generate_expression(arg) for arg in expr.arguments]
                return f"{func_code}({', '.join(args)})"

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
            # Handle arrow functions by calling the visitor method
            return self.visit_arrow_function(expr)

        elif isinstance(expr, FunctionDefinition):
            # Handle function definitions as lambda expressions when used in expressions
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

    def _generate_slice(self, slice_expr: SliceExpression) -> str:
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

    def _generate_lambda_from_function_def(self, func_def: FunctionDefinition) -> str:
        """Generate a lambda expression from a FunctionDefinition used as an expression."""
        # Build parameter list
        params = []
        for param in func_def.parameters:
            if hasattr(param, "name"):
                param_name = self._safe_identifier(param.name)
            else:
                param_name = self._safe_identifier(str(param))
            params.append(param_name)

        params_str = ", ".join(params)

        # Handle function body - for lambda, we need a single expression
        if len(func_def.body) == 1 and isinstance(func_def.body[0], ReturnStatement):
            # Single return statement - extract the expression
            return_stmt = func_def.body[0]
            body_code = self._generate_expression(return_stmt.value)
            return f"lambda {params_str}: {body_code}"
        else:
            # Multiple statements - need to handle variable substitution
            # Find the return statement and substitute variables

            # Find the last return statement
            last_return = None
            for stmt in reversed(func_def.body):
                if isinstance(stmt, ReturnStatement):
                    last_return = stmt
                    break

            if last_return and last_return.value:
                # Try to substitute variables to create a valid lambda expression
                substituted_expr = self._substitute_variables_in_lambda(
                    func_def.body, last_return.value, params
                )
                if substituted_expr:
                    return f"lambda {params_str}: {substituted_expr}"

                # Fallback: generate the expression as-is (may have undefined variables)
                body_code = self._generate_expression(last_return.value)
                return f"lambda {params_str}: {body_code}"
            else:
                # No return statement found, fall back to None
                return f"lambda {params_str}: None"

    def _substitute_variables_in_lambda(self, statements, return_expr, params):
        """Try to substitute variables in lambda to avoid undefined variable errors."""
        from mlpy.ml.grammar.ast_nodes import AssignmentStatement

        # Build a map of variable assignments
        assignments = {}
        param_names = set()

        # Get parameter names
        for param in params:
            param_names.add(param)

        # Walk through statements to find assignments
        for stmt in statements:
            if isinstance(stmt, AssignmentStatement):
                if hasattr(stmt.target, "name"):
                    var_name = stmt.target.name
                    assignments[var_name] = stmt.value

        # Try to substitute the return expression
        try:
            substituted = self._substitute_expression(
                return_expr, assignments, param_names, depth=0
            )
            if substituted:
                return self._generate_expression(substituted)
        except:
            # If substitution fails, return None to use fallback
            pass

        return None

    def _substitute_expression(self, expr, assignments, param_names, depth=0):
        """Recursively substitute variables in an expression."""
        from mlpy.ml.grammar.ast_nodes import (
            ArrayAccess,
            BinaryExpression,
            FunctionCall,
            Identifier,
            MemberAccess,
            UnaryExpression,
        )

        # Prevent infinite recursion
        if depth > 10:
            return None

        if isinstance(expr, Identifier):
            var_name = expr.name
            # If it's a parameter, keep it as-is
            if var_name in param_names:
                return expr
            # If it's an assigned variable, substitute it
            elif var_name in assignments:
                # Recursively substitute the assigned expression
                return self._substitute_expression(
                    assignments[var_name], assignments, param_names, depth + 1
                )
            else:
                # Unknown variable - might be from outer scope, keep as-is
                return expr
        elif isinstance(expr, FunctionCall):
            # Substitute arguments in function calls
            new_args = []
            for arg in expr.arguments:
                substituted_arg = self._substitute_expression(
                    arg, assignments, param_names, depth + 1
                )
                if substituted_arg is None:
                    return None  # Failed to substitute
                new_args.append(substituted_arg)

            # Create new function call with substituted arguments
            new_call = FunctionCall(expr.function, new_args)
            return new_call
        elif isinstance(expr, BinaryExpression):
            # Substitute variables in both operands of binary expressions
            left_substituted = self._substitute_expression(
                expr.left, assignments, param_names, depth + 1
            )
            right_substituted = self._substitute_expression(
                expr.right, assignments, param_names, depth + 1
            )

            if left_substituted is None or right_substituted is None:
                return None  # Failed to substitute

            # Create new binary expression with substituted operands
            new_binary = BinaryExpression(left_substituted, expr.operator, right_substituted)
            return new_binary
        elif isinstance(expr, UnaryExpression):
            # Substitute variables in unary expressions
            operand_substituted = self._substitute_expression(
                expr.operand, assignments, param_names, depth + 1
            )

            if operand_substituted is None:
                return None  # Failed to substitute

            # Create new unary expression with substituted operand
            new_unary = UnaryExpression(expr.operator, operand_substituted)
            return new_unary
        elif isinstance(expr, MemberAccess):
            # Substitute variables in member access (obj.member)
            object_substituted = self._substitute_expression(
                expr.object, assignments, param_names, depth + 1
            )

            if object_substituted is None:
                return None  # Failed to substitute

            # Create new member access with substituted object
            new_member = MemberAccess(object_substituted, expr.member)
            return new_member
        elif isinstance(expr, ArrayAccess):
            # Substitute variables in array access (arr[index])
            array_substituted = self._substitute_expression(
                expr.array, assignments, param_names, depth + 1
            )
            index_substituted = self._substitute_expression(
                expr.index, assignments, param_names, depth + 1
            )

            if array_substituted is None or index_substituted is None:
                return None  # Failed to substitute

            # Create new array access with substituted parts
            new_array_access = ArrayAccess(array_substituted, index_substituted)
            return new_array_access
        else:
            # For other expression types (literals, etc.), return as-is
            return expr

    # Additional visitor methods for literals
    def visit_binary_expression(self, node: BinaryExpression):
        pass  # Handled by _generate_expression

    def visit_unary_expression(self, node: UnaryExpression):
        pass  # Handled by _generate_expression

    def visit_identifier(self, node: Identifier):
        pass  # Handled by _generate_expression

    def visit_function_call(self, node: FunctionCall):
        pass  # Handled by _generate_expression

    def visit_array_access(self, node: ArrayAccess):
        pass  # Handled by _generate_expression

    def visit_slice_expression(self, node: SliceExpression):
        pass  # Handled by _generate_expression

    def visit_member_access(self, node: MemberAccess):
        pass  # Handled by _generate_expression

    def visit_literal(self, node: Literal):
        pass  # Handled by _generate_expression

    def visit_number_literal(self, node: NumberLiteral):
        pass  # Handled by _generate_expression

    def visit_string_literal(self, node: StringLiteral):
        pass  # Handled by _generate_expression

    def visit_boolean_literal(self, node: BooleanLiteral):
        pass  # Handled by _generate_expression

    def visit_array_literal(self, node: ArrayLiteral):
        pass  # Handled by _generate_expression

    def visit_object_literal(self, node: ObjectLiteral):
        pass  # Handled by _generate_expression

    # Advanced language constructs (Phase 2) - Stub implementations
    def visit_array_destructuring(self, node):
        """Generate Python code for array destructuring pattern."""
        # Return tuple of variable names for unpacking
        return f"({', '.join(node.elements)})"

    def visit_object_destructuring(self, node):
        """Generate Python code for object destructuring pattern."""
        # For object destructuring, we need to generate separate assignment statements
        # This method returns the pattern info that visit_destructuring_assignment will use
        return node.properties

    def visit_destructuring_assignment(self, node):
        """Generate Python code for destructuring assignment."""
        if isinstance(node.pattern, ArrayDestructuring):
            # Array destructuring: [a, b, c] = [1, 2, 3] -> a, b, c = [1, 2, 3]
            pattern_code = ", ".join(node.pattern.elements)
            value_code = self._generate_expression(node.value)
            self._emit_line(f"{pattern_code} = {value_code}", node)

        elif isinstance(node.pattern, ObjectDestructuring):
            # Object destructuring: {x, y, z} = obj -> separate assignments
            value_code = self._generate_expression(node.value)
            for key, var_name in node.pattern.properties.items():
                self._emit_line(f"{var_name} = {value_code}['{key}']", node)

        else:
            self._emit_line("# Unknown destructuring pattern", node)

    def visit_spread_element(self, node):
        """Stub implementation for spread element."""
        return "# Spread element not yet implemented"

    def visit_arrow_function(self, node):
        """Generate Python code for arrow function."""
        # Generate parameter list
        param_names = []
        for param in node.parameters:
            if hasattr(param, "name"):
                param_names.append(param.name)
            elif hasattr(param, "value"):
                param_names.append(param.value)
            else:
                param_names.append(str(param))

        params_str = ", ".join(param_names)
        body_code = self._generate_expression(node.body)

        # Generate lambda function
        return f"lambda {params_str}: {body_code}"

    def visit_match_expression(self, node):
        """Stub implementation for match expression."""
        return "# Match expression not yet implemented"

    def visit_match_case(self, node):
        """Stub implementation for match case."""
        return "# Match case not yet implemented"

    def visit_pipeline_expression(self, node):
        """Stub implementation for pipeline expression."""
        return "# Pipeline expression not yet implemented"

    def visit_ternary_expression(self, node):
        """Generate Python code for ternary expression (condition ? true_value : false_value)."""
        # Convert to Python ternary: true_value if condition else false_value
        condition_code = self._generate_expression(node.condition)
        true_code = self._generate_expression(node.true_value)
        false_code = self._generate_expression(node.false_value)

        return f"({true_code} if {condition_code} else {false_code})"

    # ============================================================================
    # Whitelist Enforcement Methods
    # ============================================================================

    def _generate_simple_function_call(self, func_name: str, arguments: list) -> str:
        """Generate simple function call with whitelist enforcement.

        Args:
            func_name: Function name (e.g., "len", "print", "myFunc")
            arguments: List of argument expressions

        Returns:
            Generated Python code for function call

        Raises:
            CodeGenError: If function is not in whitelist
        """
        args = [self._generate_expression(arg) for arg in arguments]
        args_str = ', '.join(args)

        # Category 1: ML Builtin Functions -> route to builtin module
        if self.function_registry.is_allowed_builtin(func_name):
            self.context.builtin_functions_used.add(func_name)
            return f"builtin.{func_name}({args_str})"

        # Category 2: User-Defined Functions -> direct call
        elif self.function_registry.is_user_defined(func_name):
            safe_name = self._safe_identifier(func_name)
            return f"{safe_name}({args_str})"

        # Category 3: BLOCKED - Unknown function (not in whitelist)
        else:
            self._raise_unknown_function_error(func_name, arguments)

    def _generate_member_function_call(self, member_access: MemberAccess, arguments: list) -> str:
        """Generate member function call with whitelist enforcement.

        Args:
            member_access: MemberAccess node (e.g., math.sqrt)
            arguments: List of argument expressions

        Returns:
            Generated Python code for member function call

        Handles:
            - Imported module functions: math.sqrt() -> math.sqrt()
            - Object methods: obj.method() -> obj['method']() or obj.method()
        """
        args = [self._generate_expression(arg) for arg in arguments]
        args_str = ', '.join(args)

        # Check if this is an imported module function call
        if isinstance(member_access.object, Identifier):
            module_name = member_access.object.name
            func_name = member_access.member if isinstance(member_access.member, str) else str(member_access.member)

            # Check if this is an imported module
            if self.function_registry.is_imported_module(module_name):
                # Verify function exists in module
                if self.function_registry.is_imported_function(module_name, func_name):
                    # Generate module.function() call
                    safe_module = self._safe_identifier(module_name)
                    return f"{safe_module}.{func_name}({args_str})"
                else:
                    # Function not in module - block it
                    self._raise_unknown_module_function_error(module_name, func_name, arguments)

        # Not a module call - treat as object method call
        # Use existing member access generation logic
        obj_code = self._generate_expression(member_access.object)
        if isinstance(member_access.member, str):
            member_code = member_access.member
        else:
            member_code = self._generate_expression(member_access.member)

        return f"{obj_code}.{member_code}({args_str})"

    def _raise_unknown_function_error(self, func_name: str, arguments: list) -> None:
        """Raise MLTranspilationError for unknown function call.

        Args:
            func_name: Unknown function name
            arguments: Function arguments
        """
        from mlpy.ml.errors.exceptions import MLTranspilationError

        # Build helpful error message
        message = f"Unknown function '{func_name}()' - not in whitelist.\n\n"
        message += "Allowed function categories:\n"
        message += "  1. ML builtin functions (from stdlib.builtin module)\n"
        message += "  2. User-defined functions (defined in current ML program)\n"
        message += "  3. Imported module functions (from stdlib modules)\n\n"

        # Suggest similar function names
        all_allowed = self.function_registry.get_all_allowed_functions()
        similar = [f for f in all_allowed if func_name.lower() in f.lower() or f.lower() in func_name.lower()]

        if similar:
            message += f"Did you mean one of these?\n"
            for suggestion in sorted(similar)[:5]:
                category = self.function_registry.get_call_category(suggestion)
                message += f"  - {suggestion}() [{category}]\n"

        message += f"\nRegistry status: {self.function_registry}"

        raise MLTranspilationError(message)

    def _raise_unknown_module_function_error(self, module_name: str, func_name: str, arguments: list) -> None:
        """Raise MLTranspilationError for unknown module function.

        Args:
            module_name: Module name
            func_name: Unknown function name
            arguments: Function arguments
        """
        from mlpy.ml.errors.exceptions import MLTranspilationError

        message = f"Unknown function '{module_name}.{func_name}()' - not found in module.\n\n"

        # Get module metadata
        metadata = self.function_registry.imported_modules.get(module_name)
        if metadata:
            available_functions = sorted(metadata.functions.keys())
            message += f"Available functions in '{module_name}' module:\n"
            for available_func in available_functions[:10]:
                message += f"  - {module_name}.{available_func}()\n"
            if len(available_functions) > 10:
                message += f"  ... and {len(available_functions) - 10} more\n"

        raise MLTranspilationError(message)

    # NEW: Helper methods for secure attribute access
    def _detect_object_type(self, expr: Expression) -> type | None:
        """Compile-time type detection for expressions."""
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
        registry = get_safe_registry()
        return registry.is_safe_access(obj_type, attr_name)

    def _is_ml_object_pattern(self, expr: Expression) -> bool:
        """Determine if expression represents an ML object (dictionary pattern)."""
        # ML objects are typically ObjectLiterals or identifiers that might be objects
        if isinstance(expr, ObjectLiteral):
            return True
        # Could add more sophisticated analysis here
        return False

    def _generate_safe_attribute_access(self, obj_code: str, attr_name: str, obj_type: type) -> str:
        """Generate safe attribute access code."""
        # Direct Python attribute access for whitelisted methods
        return f"{obj_code}.{attr_name}"

    def _ensure_runtime_helpers_imported(self) -> None:
        """Ensure runtime helpers are imported for safe attribute access."""
        if not self.context.runtime_helpers_imported:
            self.context.runtime_helpers_imported = True
            self.context.imports_needed.add("mlpy.stdlib.runtime_helpers")

    def _generate_assignment_target(self, expr: Expression) -> str:
        """Generate assignment target code (preserves original dictionary access for ML objects)."""
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


def generate_python_code(
    ast: Program, source_file: str | None = None, generate_source_maps: bool = True
) -> tuple[str, dict[str, Any] | None]:
    """Generate Python code from ML AST.

    Args:
        ast: Root Program AST node
        source_file: Source ML file path for source maps
        generate_source_maps: Whether to generate source map data

    Returns:
        Tuple of (Python code string, source map data)
    """
    generator = PythonCodeGenerator(source_file, generate_source_maps)
    python_code, basic_source_map = generator.generate(ast)

    # Enhanced source map generation for Sprint 7
    if generate_source_maps:
        try:
            from .enhanced_source_maps import generate_enhanced_source_map

            # Try to read the original ML source if available
            ml_source = None
            if source_file and Path(source_file).exists():
                ml_source = Path(source_file).read_text(encoding="utf-8")

            enhanced_map = generate_enhanced_source_map(ast, python_code, source_file, ml_source)
            return python_code, enhanced_map
        except ImportError:
            # Fall back to basic source map
            return python_code, basic_source_map

    return python_code, basic_source_map
