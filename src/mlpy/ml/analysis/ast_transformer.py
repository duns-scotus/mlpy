"""
AST Transformer - Phase 1 Pipeline Stage

Performs explicit AST transformation and normalization before security analysis.
Desugars complex constructs, normalizes scoping, and prepares optimized IR.
"""

import copy
from dataclasses import dataclass

from ..grammar.ast_nodes import (
    ArrayLiteral,
    AssignmentStatement,
    ASTNode,
    BinaryExpression,
    ElifClause,
    ForStatement,
    FunctionCall,
    FunctionDefinition,
    IfStatement,
    ObjectLiteral,
    Program,
    TryStatement,
    UnaryExpression,
    WhileStatement,
)


@dataclass
class TransformationResult:
    """Result of AST transformation."""

    transformed_ast: ASTNode
    transformations_applied: list[str]
    transformation_time_ms: float
    node_count_before: int
    node_count_after: int

    @property
    def transformation_summary(self) -> str:
        """Get a summary of transformations applied."""
        if not self.transformations_applied:
            return "No transformations applied"

        return f"Applied {len(self.transformations_applied)} transformations: {', '.join(self.transformations_applied)}"


class ASTTransformer:
    """
    Transforms AST for normalization and optimization preparation.

    Transformation Tasks:
    1. Desugar complex language constructs
    2. Normalize variable scoping and declarations
    3. Convert implicit operations to explicit ones
    4. Flatten nested structures where beneficial
    5. Prepare optimized intermediate representation
    """

    def __init__(self):
        self.transformations_applied: list[str] = []
        self.node_count = 0
        self.scope_depth = 0
        self.variable_counter = 0  # For generating unique variable names

    def transform(self, ast: ASTNode) -> TransformationResult:
        """
        Transform the AST with normalization and optimization preparation.

        Args:
            ast: Root AST node to transform

        Returns:
            TransformationResult with transformed AST and metadata
        """
        import time

        start_time = time.perf_counter()

        # Reset transformation state
        self.transformations_applied = []
        self.scope_depth = 0
        self.variable_counter = 0

        # Count nodes before transformation
        original_count = self._count_nodes(ast)

        # Deep copy the AST to avoid modifying the original
        transformed_ast = copy.deepcopy(ast)

        # Apply transformations
        transformed_ast = self._transform_node(transformed_ast)

        # Count nodes after transformation
        final_count = self._count_nodes(transformed_ast)

        transformation_time_ms = (time.perf_counter() - start_time) * 1000

        return TransformationResult(
            transformed_ast=transformed_ast,
            transformations_applied=self.transformations_applied.copy(),
            transformation_time_ms=transformation_time_ms,
            node_count_before=original_count,
            node_count_after=final_count,
        )

    def _count_nodes(self, node: ASTNode) -> int:
        """Count total nodes in AST."""
        if node is None:
            return 0

        count = 1

        # Count all child nodes
        for attr_name in dir(node):
            if not attr_name.startswith("_") and attr_name not in ["accept", "line", "column"]:
                attr_value = getattr(node, attr_name)
                if isinstance(attr_value, ASTNode):
                    count += self._count_nodes(attr_value)
                elif isinstance(attr_value, list):
                    for item in attr_value:
                        if isinstance(item, ASTNode):
                            count += self._count_nodes(item)

        return count

    def _transform_node(self, node: ASTNode) -> ASTNode:
        """Transform a single AST node and recursively transform children."""
        if node is None:
            return None

        # Transform based on node type
        if isinstance(node, Program):
            return self._transform_program(node)
        elif isinstance(node, FunctionDefinition):
            return self._transform_function_definition(node)
        elif isinstance(node, AssignmentStatement):
            return self._transform_assignment(node)
        elif isinstance(node, IfStatement):
            return self._transform_if_statement(node)
        elif isinstance(node, WhileStatement):
            return self._transform_while_loop(node)
        elif isinstance(node, ForStatement):
            return self._transform_for_loop(node)
        elif isinstance(node, TryStatement):
            return self._transform_try_statement(node)
        elif isinstance(node, BinaryExpression):
            return self._transform_binary_expression(node)
        elif isinstance(node, UnaryExpression):
            return self._transform_unary_expression(node)
        elif isinstance(node, FunctionCall):
            return self._transform_function_call(node)
        elif isinstance(node, ArrayLiteral):
            return self._transform_array_expression(node)
        elif isinstance(node, ObjectLiteral):
            return self._transform_object_expression(node)
        else:
            # Transform generically by recursing through children
            return self._transform_generic_node(node)

    def _transform_program(self, node: Program) -> Program:
        """Transform program root node."""
        if hasattr(node, "items") and node.items:
            # Transform all top-level items
            transformed_items = []
            for item in node.items:
                transformed_item = self._transform_node(item)
                if transformed_item is not None:
                    # Handle case where transformation might return multiple items
                    if isinstance(transformed_item, list):
                        transformed_items.extend(transformed_item)
                    else:
                        transformed_items.append(transformed_item)

            node.items = transformed_items

        return node

    def _transform_function_definition(self, node: FunctionDefinition) -> FunctionDefinition:
        """Transform function definition."""
        self.scope_depth += 1

        # Transform function body
        if hasattr(node, "body") and node.body:
            transformed_body = []
            for stmt in node.body:
                transformed_stmt = self._transform_node(stmt)
                if transformed_stmt is not None:
                    if isinstance(transformed_stmt, list):
                        transformed_body.extend(transformed_stmt)
                    else:
                        transformed_body.append(transformed_stmt)

            node.body = transformed_body

        # Transform default parameter values if present
        if hasattr(node, "parameters") and node.parameters:
            for param in node.parameters:
                if hasattr(param, "default_value") and param.default_value:
                    param.default_value = self._transform_node(param.default_value)

        self.scope_depth -= 1
        return node

    def _transform_assignment(self, node: AssignmentStatement) -> AssignmentStatement:
        """Transform assignment statement."""
        # Transform target and value
        if hasattr(node, "target"):
            node.target = self._transform_node(node.target)

        if hasattr(node, "value"):
            node.value = self._transform_node(node.value)

        return node

    def _transform_if_statement(self, node: IfStatement) -> IfStatement:
        """Transform if statement - normalize elif chains."""
        # Transform condition
        if hasattr(node, "condition"):
            node.condition = self._transform_node(node.condition)

        # Transform then statement
        if hasattr(node, "then_statement"):
            node.then_statement = self._transform_node(node.then_statement)

        # Transform elif clauses
        if hasattr(node, "elif_clauses") and node.elif_clauses:
            transformed_elifs = []
            for elif_clause in node.elif_clauses:
                if isinstance(elif_clause, ElifClause):
                    if hasattr(elif_clause, "condition"):
                        elif_clause.condition = self._transform_node(elif_clause.condition)
                    if hasattr(elif_clause, "statement"):
                        elif_clause.statement = self._transform_node(elif_clause.statement)
                    transformed_elifs.append(elif_clause)
                else:
                    # Transform as regular node
                    transformed_elif = self._transform_node(elif_clause)
                    if transformed_elif:
                        transformed_elifs.append(transformed_elif)

            node.elif_clauses = transformed_elifs

            if transformed_elifs:
                self.transformations_applied.append("normalized_elif_chain")

        # Transform else statement
        if hasattr(node, "else_statement") and node.else_statement:
            node.else_statement = self._transform_node(node.else_statement)

        return node

    def _transform_while_loop(self, node: WhileStatement) -> WhileStatement:
        """Transform while loop."""
        self.scope_depth += 1

        # Transform condition
        if hasattr(node, "condition"):
            node.condition = self._transform_node(node.condition)

        # Transform body
        if hasattr(node, "body"):
            node.body = self._transform_node(node.body)

        self.scope_depth -= 1
        return node

    def _transform_for_loop(self, node: ForStatement) -> ForStatement:
        """Transform for loop - potentially desugar to while loop."""
        self.scope_depth += 1

        # Transform iterable
        if hasattr(node, "iterable"):
            node.iterable = self._transform_node(node.iterable)

        # Transform body
        if hasattr(node, "body"):
            node.body = self._transform_node(node.body)

        self.scope_depth -= 1

        # Note: In future phases, we might desugar for-in loops to while loops
        # for easier analysis and optimization
        return node

    def _transform_try_statement(self, node: TryStatement) -> TryStatement:
        """Transform try-except statement."""
        # Transform try body
        if hasattr(node, "body"):
            node.body = self._transform_node(node.body)

        # Transform except clause
        if hasattr(node, "except_clause") and node.except_clause:
            node.except_clause = self._transform_node(node.except_clause)

        # Transform finally clause
        if hasattr(node, "finally_clause") and node.finally_clause:
            node.finally_clause = self._transform_node(node.finally_clause)

        return node

    def _transform_binary_expression(self, node: BinaryExpression) -> BinaryExpression:
        """Transform binary expression - normalize operators."""
        # Transform operands
        if hasattr(node, "left"):
            node.left = self._transform_node(node.left)

        if hasattr(node, "right"):
            node.right = self._transform_node(node.right)

        # Normalize operators
        if hasattr(node, "operator"):
            original_op = node.operator

            # Normalize comparison operators
            if node.operator == "==":
                node.operator = "eq"
                self.transformations_applied.append("normalized_equality_operator")
            elif node.operator == "!=":
                node.operator = "ne"
                self.transformations_applied.append("normalized_inequality_operator")
            elif node.operator == "&&":
                node.operator = "and"
                self.transformations_applied.append("normalized_logical_and")
            elif node.operator == "||":
                node.operator = "or"
                self.transformations_applied.append("normalized_logical_or")

        return node

    def _transform_unary_expression(self, node: UnaryExpression) -> UnaryExpression:
        """Transform unary expression."""
        # Transform operand
        if hasattr(node, "operand"):
            node.operand = self._transform_node(node.operand)

        # Normalize operators
        if hasattr(node, "operator"):
            if node.operator == "!":
                node.operator = "not"
                self.transformations_applied.append("normalized_logical_not")

        return node

    def _transform_function_call(self, node: FunctionCall) -> FunctionCall:
        """Transform function call."""
        # Transform function reference
        if hasattr(node, "function"):
            node.function = self._transform_node(node.function)

        # Transform arguments
        if hasattr(node, "arguments") and node.arguments:
            transformed_args = []
            for arg in node.arguments:
                transformed_arg = self._transform_node(arg)
                if transformed_arg is not None:
                    transformed_args.append(transformed_arg)

            node.arguments = transformed_args

        return node

    def _transform_array_expression(self, node: ArrayLiteral) -> ArrayLiteral:
        """Transform array expression."""
        if hasattr(node, "elements") and node.elements:
            transformed_elements = []
            for element in node.elements:
                transformed_element = self._transform_node(element)
                if transformed_element is not None:
                    transformed_elements.append(transformed_element)

            node.elements = transformed_elements

        return node

    def _transform_object_expression(self, node: ObjectLiteral) -> ObjectLiteral:
        """Transform object expression."""
        if hasattr(node, "properties") and node.properties:
            transformed_properties = []
            for prop in node.properties:
                transformed_prop = self._transform_node(prop)
                if transformed_prop is not None:
                    transformed_properties.append(transformed_prop)

            node.properties = transformed_properties

        return node

    def _transform_generic_node(self, node: ASTNode) -> ASTNode:
        """Transform any other AST node type generically."""
        # Recursively transform any child nodes
        for attr_name in dir(node):
            if not attr_name.startswith("_") and attr_name not in ["accept", "line", "column"]:
                attr_value = getattr(node, attr_name)

                if isinstance(attr_value, ASTNode):
                    # Transform single child node
                    transformed_child = self._transform_node(attr_value)
                    setattr(node, attr_name, transformed_child)

                elif isinstance(attr_value, list):
                    # Transform list of child nodes
                    transformed_list = []
                    for item in attr_value:
                        if isinstance(item, ASTNode):
                            transformed_item = self._transform_node(item)
                            if transformed_item is not None:
                                if isinstance(transformed_item, list):
                                    transformed_list.extend(transformed_item)
                                else:
                                    transformed_list.append(transformed_item)
                        else:
                            # Keep non-AST items as-is
                            transformed_list.append(item)

                    setattr(node, attr_name, transformed_list)

        return node

    def _generate_unique_variable_name(self, prefix: str = "temp") -> str:
        """Generate a unique variable name for temporary variables."""
        self.variable_counter += 1
        return f"_{prefix}_{self.variable_counter}"

    def _create_block_statement(self, statements: list[ASTNode]) -> ASTNode:
        """Create a block statement from a list of statements."""
        # This would create a BlockStatement node if it exists in the AST
        # For now, return the statements as-is
        if len(statements) == 1:
            return statements[0]
        else:
            # In future, this would wrap in BlockStatement
            return statements
