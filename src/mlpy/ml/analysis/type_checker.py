"""
Type Checker - Phase 2 Pipeline Stage

Performs static type analysis and inference to catch type mismatches early.
Provides comprehensive type checking for the ML language with detailed error reporting.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from ..grammar.ast_nodes import (
    ArrayAccess,
    ArrayLiteral,
    AssignmentStatement,
    ASTNode,
    BinaryExpression,
    BooleanLiteral,
    ForStatement,
    FunctionCall,
    FunctionDefinition,
    Identifier,
    IfStatement,
    MemberAccess,
    NumberLiteral,
    ObjectLiteral,
    Parameter,
    Program,
    ReturnStatement,
    StringLiteral,
    UnaryExpression,
    WhileStatement,
)


class MLType(Enum):
    """ML language type system."""

    NUMBER = "number"
    STRING = "string"
    BOOLEAN = "boolean"
    ARRAY = "array"
    OBJECT = "object"
    FUNCTION = "function"
    NULL = "null"
    UNDEFINED = "undefined"
    ANY = "any"  # For gradual typing
    UNKNOWN = "unknown"  # For inference failures


@dataclass
class TypeInfo:
    """Represents type information for a value or expression."""

    base_type: MLType
    element_type: Optional["TypeInfo"] = None  # For arrays
    properties: dict[str, "TypeInfo"] = None  # For objects
    parameters: list["TypeInfo"] = None  # For functions
    return_type: Optional["TypeInfo"] = None  # For functions
    nullable: bool = False

    def __post_init__(self):
        if self.properties is None:
            self.properties = {}
        if self.parameters is None:
            self.parameters = []

    def is_compatible_with(self, other: "TypeInfo") -> bool:
        """Check if this type is compatible with another type."""
        if self.base_type == MLType.ANY or other.base_type == MLType.ANY:
            return True

        if self.base_type == other.base_type:
            if self.base_type == MLType.ARRAY:
                if self.element_type and other.element_type:
                    return self.element_type.is_compatible_with(other.element_type)
                return True  # Untyped arrays are compatible
            elif self.base_type == MLType.FUNCTION:
                return self._function_compatible(other)
            return True

        # Number/boolean coercion
        if {self.base_type, other.base_type} <= {MLType.NUMBER, MLType.BOOLEAN}:
            return True

        return False

    def _function_compatible(self, other: "TypeInfo") -> bool:
        """Check function type compatibility."""
        if len(self.parameters) != len(other.parameters):
            return False

        for p1, p2 in zip(self.parameters, other.parameters, strict=False):
            if not p1.is_compatible_with(p2):
                return False

        if self.return_type and other.return_type:
            return self.return_type.is_compatible_with(other.return_type)

        return True

    def __str__(self) -> str:
        """String representation of type."""
        if self.base_type == MLType.ARRAY:
            elem_str = str(self.element_type) if self.element_type else "any"
            return f"array<{elem_str}>"
        elif self.base_type == MLType.FUNCTION:
            param_str = ", ".join(str(p) for p in self.parameters)
            ret_str = str(self.return_type) if self.return_type else "void"
            return f"({param_str}) -> {ret_str}"
        else:
            return self.base_type.value


class TypeIssue:
    """Represents a type checking issue."""

    def __init__(self, severity: str, message: str, node: ASTNode = None):
        self.severity = severity  # "error", "warning", "info"
        self.message = message
        self.node = node
        self.line = getattr(node, "line", None)
        self.column = getattr(node, "column", None)


@dataclass
class TypeCheckResult:
    """Result of type checking analysis."""

    is_valid: bool
    issues: list[TypeIssue]
    type_info: dict[ASTNode, TypeInfo]  # Type information for each node
    symbol_table: dict[str, TypeInfo]  # Variable type information
    type_check_time_ms: float
    nodes_analyzed: int

    @property
    def errors(self) -> list[TypeIssue]:
        """Get only error-level issues."""
        return [issue for issue in self.issues if issue.severity == "error"]

    @property
    def warnings(self) -> list[TypeIssue]:
        """Get only warning-level issues."""
        return [issue for issue in self.issues if issue.severity == "warning"]


class TypeChecker:
    """
    Static type checker for ML language with type inference.

    Features:
    - Type inference for literals and expressions
    - Function parameter and return type checking
    - Array element type consistency
    - Object property type tracking
    - Binary operation type compatibility
    - Variable assignment type checking
    """

    def __init__(self):
        self.issues: list[TypeIssue] = []
        self.type_info: dict[ASTNode, TypeInfo] = {}
        self.symbol_table: dict[str, TypeInfo] = {}
        self.function_table: dict[str, TypeInfo] = {}
        self.scope_stack: list[dict[str, TypeInfo]] = []
        self.current_function_return_type: TypeInfo | None = None
        self.nodes_analyzed = 0

    def check_types(self, ast: ASTNode) -> TypeCheckResult:
        """
        Perform complete type checking on the AST.

        Args:
            ast: Root AST node to type check

        Returns:
            TypeCheckResult with type checking status and issues
        """
        import time

        start_time = time.perf_counter()

        # Reset checker state
        self.issues = []
        self.type_info = {}
        self.symbol_table = {}
        self.function_table = {}
        self.scope_stack = []
        self.current_function_return_type = None
        self.nodes_analyzed = 0

        # Initialize built-in types
        self._initialize_builtins()

        # Perform type checking
        self._check_node(ast)

        type_check_time_ms = (time.perf_counter() - start_time) * 1000

        # Determine if type checking passed (no errors)
        is_valid = not any(issue.severity == "error" for issue in self.issues)

        return TypeCheckResult(
            is_valid=is_valid,
            issues=self.issues,
            type_info=self.type_info.copy(),
            symbol_table=self.symbol_table.copy(),
            type_check_time_ms=type_check_time_ms,
            nodes_analyzed=self.nodes_analyzed,
        )

    def _initialize_builtins(self):
        """Initialize built-in functions and types."""
        # Built-in functions
        self.symbol_table.update(
            {
                "console": TypeInfo(
                    MLType.OBJECT,
                    properties={
                        "log": TypeInfo(
                            MLType.FUNCTION,
                            parameters=[TypeInfo(MLType.ANY)],
                            return_type=TypeInfo(MLType.UNDEFINED),
                        )
                    },
                ),
                "Math": TypeInfo(
                    MLType.OBJECT,
                    properties={
                        "PI": TypeInfo(MLType.NUMBER),
                        "E": TypeInfo(MLType.NUMBER),
                        "sqrt": TypeInfo(
                            MLType.FUNCTION,
                            parameters=[TypeInfo(MLType.NUMBER)],
                            return_type=TypeInfo(MLType.NUMBER),
                        ),
                        "pow": TypeInfo(
                            MLType.FUNCTION,
                            parameters=[TypeInfo(MLType.NUMBER), TypeInfo(MLType.NUMBER)],
                            return_type=TypeInfo(MLType.NUMBER),
                        ),
                        "floor": TypeInfo(
                            MLType.FUNCTION,
                            parameters=[TypeInfo(MLType.NUMBER)],
                            return_type=TypeInfo(MLType.NUMBER),
                        ),
                        "ceil": TypeInfo(
                            MLType.FUNCTION,
                            parameters=[TypeInfo(MLType.NUMBER)],
                            return_type=TypeInfo(MLType.NUMBER),
                        ),
                    },
                ),
                "Array": TypeInfo(MLType.OBJECT, properties={"length": TypeInfo(MLType.NUMBER)}),
            }
        )

    def _check_node(self, node: ASTNode) -> TypeInfo | None:
        """Check types for a single node and return its inferred type."""
        if node is None:
            return None

        self.nodes_analyzed += 1

        # Check based on node type
        if isinstance(node, Program):
            return self._check_program(node)
        elif isinstance(node, FunctionDefinition):
            return self._check_function_definition(node)
        elif isinstance(node, AssignmentStatement):
            return self._check_assignment(node)
        elif isinstance(node, IfStatement):
            return self._check_if_statement(node)
        elif isinstance(node, WhileStatement):
            return self._check_while_statement(node)
        elif isinstance(node, ForStatement):
            return self._check_for_statement(node)
        elif isinstance(node, ReturnStatement):
            return self._check_return_statement(node)
        elif isinstance(node, BinaryExpression):
            return self._check_binary_expression(node)
        elif isinstance(node, UnaryExpression):
            return self._check_unary_expression(node)
        elif isinstance(node, FunctionCall):
            return self._check_function_call(node)
        elif isinstance(node, Identifier):
            return self._check_identifier(node)
        elif isinstance(node, NumberLiteral):
            return self._check_number_literal(node)
        elif isinstance(node, StringLiteral):
            return self._check_string_literal(node)
        elif isinstance(node, BooleanLiteral):
            return self._check_boolean_literal(node)
        elif isinstance(node, ArrayLiteral):
            return self._check_array_literal(node)
        elif isinstance(node, ObjectLiteral):
            return self._check_object_literal(node)
        elif isinstance(node, ArrayAccess):
            return self._check_array_access(node)
        elif isinstance(node, MemberAccess):
            return self._check_member_access(node)
        else:
            # Generic node checking
            return self._check_generic_node(node)

    def _check_program(self, node: Program) -> TypeInfo:
        """Check program root node."""
        self.scope_stack.append({})  # Global scope

        if hasattr(node, "items") and node.items:
            for item in node.items:
                self._check_node(item)

        self.scope_stack.pop()
        return TypeInfo(MLType.UNDEFINED)

    def _check_function_definition(self, node: FunctionDefinition) -> TypeInfo:
        """Check function definition and infer its type."""
        if not hasattr(node, "name") or not node.name:
            self._add_issue("error", "Function missing name", node)
            return TypeInfo(MLType.UNKNOWN)

        # Create function scope
        self.scope_stack.append({})

        # Process parameters
        param_types = []
        if hasattr(node, "parameters") and node.parameters:
            for param in node.parameters:
                if isinstance(param, Parameter):
                    param_type = self._get_parameter_type(param)
                    param_types.append(param_type)
                    # Add parameter to function scope
                    if hasattr(param, "name"):
                        self.scope_stack[-1][param.name] = param_type
                elif isinstance(param, str):
                    # Simple parameter name
                    param_type = TypeInfo(MLType.ANY)
                    param_types.append(param_type)
                    self.scope_stack[-1][param] = param_type

        # Analyze function body to infer return type
        return_type = TypeInfo(MLType.UNDEFINED)
        prev_return_type = self.current_function_return_type
        self.current_function_return_type = return_type

        if hasattr(node, "body") and node.body:
            inferred_returns = []
            for stmt in node.body:
                stmt_type = self._check_node(stmt)
                if isinstance(stmt, ReturnStatement):
                    inferred_returns.append(stmt_type or TypeInfo(MLType.UNDEFINED))

            # Unify return types
            if inferred_returns:
                return_type = self._unify_types(inferred_returns)

        self.current_function_return_type = prev_return_type

        # Create function type
        func_type = TypeInfo(MLType.FUNCTION, parameters=param_types, return_type=return_type)

        # Register function in symbol table
        self.function_table[node.name] = func_type
        if self.scope_stack:
            self.scope_stack[-1][node.name] = func_type

        self.scope_stack.pop()  # Exit function scope
        self.type_info[node] = func_type
        return func_type

    def _get_parameter_type(self, param: Parameter) -> TypeInfo:
        """Get type information for a function parameter."""
        if hasattr(param, "type_annotation") and param.type_annotation:
            return self._parse_type_annotation(param.type_annotation)
        else:
            return TypeInfo(MLType.ANY)

    def _parse_type_annotation(self, annotation: str) -> TypeInfo:
        """Parse a type annotation string into TypeInfo."""
        annotation = annotation.lower().strip()

        if annotation == "number":
            return TypeInfo(MLType.NUMBER)
        elif annotation == "string":
            return TypeInfo(MLType.STRING)
        elif annotation == "boolean":
            return TypeInfo(MLType.BOOLEAN)
        elif annotation.startswith("array"):
            # Simple array type parsing
            return TypeInfo(MLType.ARRAY, element_type=TypeInfo(MLType.ANY))
        elif annotation == "object":
            return TypeInfo(MLType.OBJECT)
        else:
            return TypeInfo(MLType.ANY)

    def _check_assignment(self, node: AssignmentStatement) -> TypeInfo:
        """Check assignment statement type compatibility."""
        if not hasattr(node, "target") or not hasattr(node, "value"):
            self._add_issue("error", "Assignment missing target or value", node)
            return TypeInfo(MLType.UNKNOWN)

        # Check value type
        value_type = self._check_node(node.value)
        if not value_type:
            value_type = TypeInfo(MLType.UNKNOWN)

        # Handle different assignment targets
        if isinstance(node.target, Identifier):
            var_name = node.target.name

            # Check if variable already exists
            existing_type = self._lookup_variable(var_name)
            if existing_type:
                # Check compatibility
                if not value_type.is_compatible_with(existing_type):
                    self._add_issue(
                        "error",
                        f"Type mismatch: cannot assign {value_type} to variable '{var_name}' of type {existing_type}",
                        node,
                    )

            # Update variable type
            if self.scope_stack:
                self.scope_stack[-1][var_name] = value_type
            else:
                self.symbol_table[var_name] = value_type

        elif isinstance(node.target, ArrayAccess):
            # Array element assignment
            self._check_node(node.target)
        elif isinstance(node.target, MemberAccess):
            # Object property assignment
            self._check_node(node.target)

        self.type_info[node] = value_type
        return value_type

    def _check_binary_expression(self, node: BinaryExpression) -> TypeInfo:
        """Check binary expression and infer result type."""
        if not hasattr(node, "left") or not hasattr(node, "right") or not hasattr(node, "operator"):
            self._add_issue("error", "Binary expression missing operands or operator", node)
            return TypeInfo(MLType.UNKNOWN)

        left_type = self._check_node(node.left)
        right_type = self._check_node(node.right)

        if not left_type or not right_type:
            return TypeInfo(MLType.UNKNOWN)

        operator = node.operator

        # Arithmetic operators
        if operator in ["+", "-", "*", "/", "%"]:
            if operator == "+":
                # String concatenation or numeric addition
                if left_type.base_type == MLType.STRING or right_type.base_type == MLType.STRING:
                    result_type = TypeInfo(MLType.STRING)
                elif left_type.base_type == MLType.NUMBER and right_type.base_type == MLType.NUMBER:
                    result_type = TypeInfo(MLType.NUMBER)
                else:
                    self._add_issue(
                        "warning",
                        f"Implicit type coercion in addition: {left_type} + {right_type}",
                        node,
                    )
                    result_type = TypeInfo(MLType.ANY)
            else:
                # Numeric operations
                if not (
                    left_type.base_type in [MLType.NUMBER, MLType.BOOLEAN]
                    and right_type.base_type in [MLType.NUMBER, MLType.BOOLEAN]
                ):
                    self._add_issue(
                        "error", f"Numeric operator {operator} requires numeric operands", node
                    )
                result_type = TypeInfo(MLType.NUMBER)

        # Comparison operators
        elif operator in ["<", ">", "<=", ">="]:
            if not (
                left_type.base_type in [MLType.NUMBER, MLType.STRING]
                and right_type.base_type in [MLType.NUMBER, MLType.STRING]
            ):
                self._add_issue("warning", f"Comparison between {left_type} and {right_type}", node)
            result_type = TypeInfo(MLType.BOOLEAN)

        # Equality operators
        elif operator in ["==", "!=", "eq", "ne"]:
            result_type = TypeInfo(MLType.BOOLEAN)

        # Logical operators
        elif operator in ["&&", "||", "and", "or"]:
            result_type = TypeInfo(MLType.BOOLEAN)

        else:
            self._add_issue("warning", f"Unknown binary operator: {operator}", node)
            result_type = TypeInfo(MLType.UNKNOWN)

        self.type_info[node] = result_type
        return result_type

    def _check_function_call(self, node: FunctionCall) -> TypeInfo:
        """Check function call and infer return type."""
        if not hasattr(node, "function"):
            self._add_issue("error", "Function call missing function", node)
            return TypeInfo(MLType.UNKNOWN)

        # Get function type
        func_type = self._check_node(node.function)
        if not func_type or func_type.base_type != MLType.FUNCTION:
            self._add_issue("error", "Cannot call non-function value", node)
            return TypeInfo(MLType.UNKNOWN)

        # Check arguments
        arg_types = []
        if hasattr(node, "arguments") and node.arguments:
            for arg in node.arguments:
                arg_type = self._check_node(arg)
                if arg_type:
                    arg_types.append(arg_type)

        # Check parameter compatibility
        if func_type.parameters:
            if len(arg_types) != len(func_type.parameters):
                self._add_issue(
                    "error",
                    f"Function expects {len(func_type.parameters)} arguments, got {len(arg_types)}",
                    node,
                )
            else:
                for i, (arg_type, param_type) in enumerate(
                    zip(arg_types, func_type.parameters, strict=False)
                ):
                    if not arg_type.is_compatible_with(param_type):
                        self._add_issue(
                            "error", f"Argument {i+1}: expected {param_type}, got {arg_type}", node
                        )

        result_type = func_type.return_type or TypeInfo(MLType.UNDEFINED)
        self.type_info[node] = result_type
        return result_type

    def _check_identifier(self, node: Identifier) -> TypeInfo:
        """Check identifier and return its type."""
        if not hasattr(node, "name"):
            self._add_issue("error", "Identifier missing name", node)
            return TypeInfo(MLType.UNKNOWN)

        var_type = self._lookup_variable(node.name)
        if not var_type:
            self._add_issue("error", f"Undefined variable: {node.name}", node)
            return TypeInfo(MLType.UNKNOWN)

        self.type_info[node] = var_type
        return var_type

    def _check_array_literal(self, node: ArrayLiteral) -> TypeInfo:
        """Check array literal and infer element type."""
        element_types = []

        if hasattr(node, "elements") and node.elements:
            for element in node.elements:
                elem_type = self._check_node(element)
                if elem_type:
                    element_types.append(elem_type)

        # Infer unified element type
        if element_types:
            unified_type = self._unify_types(element_types)
        else:
            unified_type = TypeInfo(MLType.ANY)

        result_type = TypeInfo(MLType.ARRAY, element_type=unified_type)
        self.type_info[node] = result_type
        return result_type

    def _check_number_literal(self, node: NumberLiteral) -> TypeInfo:
        """Check number literal."""
        result_type = TypeInfo(MLType.NUMBER)
        self.type_info[node] = result_type
        return result_type

    def _check_string_literal(self, node: StringLiteral) -> TypeInfo:
        """Check string literal."""
        result_type = TypeInfo(MLType.STRING)
        self.type_info[node] = result_type
        return result_type

    def _check_boolean_literal(self, node: BooleanLiteral) -> TypeInfo:
        """Check boolean literal."""
        result_type = TypeInfo(MLType.BOOLEAN)
        self.type_info[node] = result_type
        return result_type

    def _check_generic_node(self, node: ASTNode) -> TypeInfo:
        """Generic node type checking."""
        # Recursively check child nodes
        for attr_name in dir(node):
            if not attr_name.startswith("_") and attr_name not in ["accept", "line", "column"]:
                attr_value = getattr(node, attr_name)
                if isinstance(attr_value, ASTNode):
                    self._check_node(attr_value)
                elif isinstance(attr_value, list):
                    for item in attr_value:
                        if isinstance(item, ASTNode):
                            self._check_node(item)

        return TypeInfo(MLType.UNDEFINED)

    # Helper methods
    def _check_if_statement(self, node: IfStatement) -> TypeInfo:
        """Check if statement."""
        if hasattr(node, "condition"):
            self._check_node(node.condition)
        if hasattr(node, "then_statement"):
            self._check_node(node.then_statement)
        if hasattr(node, "else_statement") and node.else_statement:
            self._check_node(node.else_statement)
        return TypeInfo(MLType.UNDEFINED)

    def _check_while_statement(self, node: WhileStatement) -> TypeInfo:
        """Check while statement."""
        if hasattr(node, "condition"):
            self._check_node(node.condition)
        if hasattr(node, "body"):
            self._check_node(node.body)
        return TypeInfo(MLType.UNDEFINED)

    def _check_for_statement(self, node: ForStatement) -> TypeInfo:
        """Check for statement."""
        self.scope_stack.append({})  # Loop scope

        if hasattr(node, "iterable"):
            iterable_type = self._check_node(node.iterable)
            # Add loop variable to scope
            if hasattr(node, "variable"):
                var_name = (
                    node.variable
                    if isinstance(node.variable, str)
                    else getattr(node.variable, "name", None)
                )
                if var_name:
                    if iterable_type and iterable_type.base_type == MLType.ARRAY:
                        self.scope_stack[-1][var_name] = iterable_type.element_type or TypeInfo(
                            MLType.ANY
                        )
                    else:
                        self.scope_stack[-1][var_name] = TypeInfo(MLType.ANY)

        if hasattr(node, "body"):
            self._check_node(node.body)

        self.scope_stack.pop()
        return TypeInfo(MLType.UNDEFINED)

    def _check_return_statement(self, node: ReturnStatement) -> TypeInfo:
        """Check return statement."""
        return_type = TypeInfo(MLType.UNDEFINED)

        if hasattr(node, "value") and node.value:
            return_type = self._check_node(node.value)

        # Check against expected function return type
        if self.current_function_return_type:
            if not return_type.is_compatible_with(self.current_function_return_type):
                self._add_issue(
                    "warning", f"Return type {return_type} may not match function return type", node
                )

        return return_type

    def _check_unary_expression(self, node: UnaryExpression) -> TypeInfo:
        """Check unary expression."""
        if not hasattr(node, "operand") or not hasattr(node, "operator"):
            return TypeInfo(MLType.UNKNOWN)

        operand_type = self._check_node(node.operand)
        operator = node.operator

        if operator in ["-"]:
            result_type = TypeInfo(MLType.NUMBER)
        elif operator in ["!", "not"]:
            result_type = TypeInfo(MLType.BOOLEAN)
        else:
            result_type = TypeInfo(MLType.UNKNOWN)

        self.type_info[node] = result_type
        return result_type

    def _check_array_access(self, node: ArrayAccess) -> TypeInfo:
        """Check array access."""
        if not hasattr(node, "array") or not hasattr(node, "index"):
            return TypeInfo(MLType.UNKNOWN)

        array_type = self._check_node(node.array)
        self._check_node(node.index)  # Should be number

        if array_type and array_type.base_type == MLType.ARRAY:
            result_type = array_type.element_type or TypeInfo(MLType.ANY)
        else:
            self._add_issue("error", "Cannot index non-array value", node)
            result_type = TypeInfo(MLType.UNKNOWN)

        self.type_info[node] = result_type
        return result_type

    def _check_member_access(self, node: MemberAccess) -> TypeInfo:
        """Check member access."""
        if not hasattr(node, "object") or not hasattr(node, "property"):
            return TypeInfo(MLType.UNKNOWN)

        obj_type = self._check_node(node.object)
        prop_name = getattr(node.property, "name", str(node.property))

        if obj_type and obj_type.base_type == MLType.OBJECT:
            if prop_name in obj_type.properties:
                result_type = obj_type.properties[prop_name]
            else:
                result_type = TypeInfo(MLType.ANY)
        else:
            result_type = TypeInfo(MLType.ANY)

        self.type_info[node] = result_type
        return result_type

    def _check_object_literal(self, node: ObjectLiteral) -> TypeInfo:
        """Check object literal."""
        properties = {}

        if hasattr(node, "properties") and node.properties:
            for prop in node.properties:
                # Simplified property handling
                if hasattr(prop, "key") and hasattr(prop, "value"):
                    key_name = getattr(prop.key, "name", str(prop.key))
                    prop_type = self._check_node(prop.value)
                    if prop_type:
                        properties[key_name] = prop_type

        result_type = TypeInfo(MLType.OBJECT, properties=properties)
        self.type_info[node] = result_type
        return result_type

    def _lookup_variable(self, name: str) -> TypeInfo | None:
        """Look up variable type in scope stack."""
        # Check scope stack in reverse order (most recent first)
        for scope in reversed(self.scope_stack):
            if name in scope:
                return scope[name]

        # Check global symbol table
        return self.symbol_table.get(name)

    def _unify_types(self, types: list[TypeInfo]) -> TypeInfo:
        """Unify multiple types into a single compatible type."""
        if not types:
            return TypeInfo(MLType.UNKNOWN)

        if len(types) == 1:
            return types[0]

        # Simple unification - if all types are the same, return that type
        first_type = types[0]
        if all(t.base_type == first_type.base_type for t in types):
            return first_type

        # If types differ, return ANY for gradual typing
        return TypeInfo(MLType.ANY)

    def _add_issue(self, severity: str, message: str, node: ASTNode = None):
        """Add a type checking issue."""
        issue = TypeIssue(severity, message, node)
        self.issues.append(issue)
