"""Python code generator from ML AST with source map support."""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from mlpy.ml.grammar.ast_nodes import *
from mlpy.runtime.profiling.decorators import profile_parser


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

        # First pass: analyze AST to determine what imports are needed
        temp_context = self.context
        ast.accept(self)

        # Reset for actual generation
        self.context = temp_context
        self.output_lines = []

        # Generate header
        self._emit_header()

        # Generate imports if needed (but exclude contextlib as it's in header)
        remaining_imports = self.context.imports_needed - {"contextlib"}
        if remaining_imports:
            for import_name in sorted(remaining_imports):
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
        if module_path in ["math", "json", "datetime", "random"]:
            # Safe standard library modules
            if node.alias:
                self._emit_line(
                    f"import {module_path} as {self._safe_identifier(node.alias)}", node
                )
            else:
                self._emit_line(f"import {module_path}", node)
        else:
            # Unknown modules get a runtime import check
            self._emit_line(f"# WARNING: Import '{module_path}' requires security review", node)
            self._emit_line(f"# import {module_path}", node)

    def visit_function_definition(self, node: FunctionDefinition):
        """Generate code for function definition."""
        func_name = self._safe_identifier(
            node.name.name if hasattr(node.name, "name") else str(node.name)
        )

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
        target = self._safe_identifier(
            node.target.name if hasattr(node.target, "name") else str(node.target)
        )
        value_code = self._generate_expression(node.value)
        self._emit_line(f"{target} = {value_code}", node)

    def visit_return_statement(self, node: ReturnStatement):
        """Generate code for return statement."""
        if node.value:
            value_code = self._generate_expression(node.value)
            self._emit_line(f"return {value_code}", node)
        else:
            self._emit_line("return", node)

    def visit_block_statement(self, node: BlockStatement):
        """Generate code for block statement."""
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

        if node.else_statement:
            self._emit_line("else:")
            self._indent()
            node.else_statement.accept(self)
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
        var_name = self._safe_identifier(node.variable)
        iterable_code = self._generate_expression(node.iterable)
        self._emit_line(f"for {var_name} in {iterable_code}:", node)

        self._indent()
        if node.body:
            node.body.accept(self)
        else:
            self._emit_line("pass")
        self._dedent()

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
                "%": "%",
            }
            python_op = op_map.get(expr.operator, expr.operator)
            return f"({left} {python_op} {right})"

        elif isinstance(expr, UnaryExpression):
            operand = self._generate_expression(expr.operand)
            op_map = {"!": "not", "-": "-", "+": "+"}
            python_op = op_map.get(expr.operator, expr.operator)
            return f"({python_op} {operand})"

        elif isinstance(expr, Identifier):
            return self._safe_identifier(expr.name)

        elif isinstance(expr, FunctionCall):
            func_name = self._safe_identifier(expr.function)
            args = [self._generate_expression(arg) for arg in expr.arguments]
            return f"{func_name}({', '.join(args)})"

        elif isinstance(expr, ArrayAccess):
            array_code = self._generate_expression(expr.array)
            index_code = self._generate_expression(expr.index)
            return f"{array_code}[{index_code}]"

        elif isinstance(expr, MemberAccess):
            obj_code = self._generate_expression(expr.object)
            member = self._safe_identifier(expr.member)
            return f"{obj_code}.{member}"

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
                key_str = repr(key)  # Ensure proper string escaping
                value_str = self._generate_expression(value)
                properties.append(f"{key_str}: {value_str}")
            return f"{{{', '.join(properties)}}}"

        else:
            return f"# UNKNOWN_EXPRESSION: {type(expr).__name__}"

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
    return generator.generate(ast)
