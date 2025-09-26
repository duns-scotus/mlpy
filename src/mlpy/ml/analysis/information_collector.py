"""
Information Collector - Phase 2 Pipeline Stage (Replaces Type Checker)

Lightweight information collector that gathers type hints and data flow information
for security analysis and developer tooling WITHOUT blocking the pipeline.

Core Philosophy: "Collect, Don't Reject" - gather information to help other stages
while allowing all dynamically valid programs to proceed.
"""

import time
from dataclasses import dataclass, field
from enum import Enum

from ..grammar.ast_nodes import (
    ArrayLiteral,
    AssignmentStatement,
    ASTNode,
    BinaryExpression,
    BooleanLiteral,
    ExpressionStatement,
    FunctionCall,
    FunctionDefinition,
    Identifier,
    IfStatement,
    Literal,
    NumberLiteral,
    ObjectLiteral,
    Program,
    StringLiteral,
    UnaryExpression,
    WhileStatement,
)


class BasicType(Enum):
    """Basic type categories for information collection."""

    NUMBER = "number"
    STRING = "string"
    BOOLEAN = "boolean"
    ARRAY = "array"
    OBJECT = "object"
    FUNCTION = "function"
    UNKNOWN = "unknown"


class TaintLevel(Enum):
    """Data taint levels for security analysis."""

    CLEAN = "clean"  # Safe data
    USER_INPUT = "user_input"  # Data from user input
    EXTERNAL = "external"  # Data from external sources
    COMPUTED = "computed"  # Derived from other data


@dataclass
class ExpressionInfo:
    """Information about an expression."""

    basic_type: BasicType
    taint_level: TaintLevel = TaintLevel.CLEAN
    confidence: float = 0.5  # How confident we are (0.0 - 1.0)
    source_location: str | None = None

    def to_dict(self):
        """Convert to JSON-serializable dictionary."""
        return {
            "basic_type": self.basic_type.value,
            "taint_level": self.taint_level.value,
            "confidence": self.confidence,
            "source_location": self.source_location,
        }


@dataclass
class VariableInfo:
    """Information about a variable's usage."""

    name: str
    assignments: list[ExpressionInfo] = field(default_factory=list)
    last_assignment: ExpressionInfo | None = None
    is_function_param: bool = False

    def to_dict(self):
        """Convert to JSON-serializable dictionary."""
        return {
            "name": self.name,
            "assignments": [a.to_dict() for a in self.assignments],
            "last_assignment": self.last_assignment.to_dict() if self.last_assignment else None,
            "is_function_param": self.is_function_param,
        }


@dataclass
class FunctionInfo:
    """Information about a function."""

    name: str
    parameters: list[str] = field(default_factory=list)
    calls_external: bool = False  # Calls external/dangerous functions
    returns_tainted: bool = False  # May return tainted data

    def to_dict(self):
        """Convert to JSON-serializable dictionary."""
        return {
            "name": self.name,
            "parameters": self.parameters,
            "calls_external": self.calls_external,
            "returns_tainted": self.returns_tainted,
        }


@dataclass
class InformationResult:
    """Result of information collection."""

    expressions: dict[str, ExpressionInfo] = field(default_factory=dict)
    variables: dict[str, VariableInfo] = field(default_factory=dict)
    functions: dict[str, FunctionInfo] = field(default_factory=dict)
    taint_sources: list[str] = field(default_factory=list)
    external_calls: list[str] = field(default_factory=list)
    nodes_analyzed: int = 0
    collection_time_ms: float = 0.0

    # Always succeeds - never blocks pipeline
    is_valid: bool = True
    issues: list[str] = field(default_factory=list)  # Informational only

    def to_dict(self):
        """Convert to JSON-serializable dictionary."""
        return {
            "expressions": {k: v.to_dict() for k, v in self.expressions.items()},
            "variables": {k: v.to_dict() for k, v in self.variables.items()},
            "functions": {k: v.to_dict() for k, v in self.functions.items()},
            "taint_sources": self.taint_sources,
            "external_calls": self.external_calls,
            "nodes_analyzed": self.nodes_analyzed,
            "collection_time_ms": self.collection_time_ms,
            "is_valid": self.is_valid,
            "issues": self.issues,
        }


class MLInformationCollector:
    """
    Lightweight information collector for ML language.

    Collects type hints and data flow information for:
    - Security analysis enhancement
    - Developer tooling and IDE support
    - Pipeline optimization

    Never rejects programs - only collects information.
    """

    # Functions that introduce taint
    TAINT_SOURCES = {
        "get_input",
        "read_file",
        "http_get",
        "http_post",
        "database_query",
        "user_input",
        "external_api",
    }

    def __init__(self):
        self.result = InformationResult()
        self.current_function = None
        self.node_counter = 0

    def collect_information(self, ast: ASTNode) -> InformationResult:
        """
        Collect information from AST without rejecting any programs.

        Args:
            ast: Root AST node to analyze

        Returns:
            InformationResult with collected data
        """
        start_time = time.perf_counter()

        # Reset state
        self.result = InformationResult()
        self.current_function = None
        self.node_counter = 0

        # Collect information
        self._collect_from_node(ast)

        # Finalize result
        self.result.collection_time_ms = (time.perf_counter() - start_time) * 1000
        self.result.nodes_analyzed = self.node_counter

        return self.result

    def _collect_from_node(self, node: ASTNode):
        """Recursively collect information from AST node."""
        if node is None:
            return

        self.node_counter += 1

        # Collect information based on node type
        if isinstance(node, Program):
            self._collect_from_program(node)
        elif isinstance(node, FunctionDefinition):
            self._collect_from_function(node)
        elif isinstance(node, AssignmentStatement):
            self._collect_from_assignment(node)
        elif isinstance(node, FunctionCall):
            self._collect_from_function_call(node)
        elif isinstance(node, Literal):
            self._collect_from_literal(node)
        elif isinstance(node, Identifier):
            self._collect_from_identifier(node)
        elif isinstance(node, BinaryExpression):
            self._collect_from_binary_expression(node)
        elif isinstance(node, ArrayLiteral):
            self._collect_from_array_literal(node)
        elif isinstance(node, ObjectLiteral):
            self._collect_from_object_literal(node)

        # Recursively process children
        self._collect_from_children(node)

    def _collect_from_program(self, node: Program):
        """Collect information from program root."""
        # Just process all items
        pass

    def _collect_from_function(self, node: FunctionDefinition):
        """Collect information from function definition."""
        func_info = FunctionInfo(
            name=node.name,
            parameters=[
                param.name if hasattr(param, "name") else str(param)
                for param in (node.parameters or [])
            ],
        )

        self.result.functions[node.name] = func_info

        # Track parameters as variables
        for param_name in func_info.parameters:
            var_info = VariableInfo(
                name=param_name,
                is_function_param=True,
                last_assignment=ExpressionInfo(
                    basic_type=BasicType.UNKNOWN,
                    taint_level=TaintLevel.USER_INPUT,  # Parameters are potentially tainted
                    confidence=0.3,
                ),
            )
            self.result.variables[param_name] = var_info

        # Enter function scope
        prev_function = self.current_function
        self.current_function = node.name

        # Process function body
        if node.body:
            for stmt in node.body:
                self._collect_from_node(stmt)

        # Exit function scope
        self.current_function = prev_function

    def _collect_from_assignment(self, node: AssignmentStatement):
        """Collect information from assignment."""
        if isinstance(node.target, Identifier):
            var_name = node.target.name

            # Analyze the assigned value
            value_info = self._analyze_expression(node.value)

            # Update variable information
            if var_name not in self.result.variables:
                self.result.variables[var_name] = VariableInfo(name=var_name)

            var_info = self.result.variables[var_name]
            var_info.assignments.append(value_info)
            var_info.last_assignment = value_info

    def _collect_from_function_call(self, node: FunctionCall):
        """Collect information from function call."""
        func_name = node.function if isinstance(node.function, str) else str(node.function)

        # Track external/taint-introducing function calls
        if func_name in self.TAINT_SOURCES:
            self.result.taint_sources.append(func_name)
            if self.current_function and self.current_function in self.result.functions:
                self.result.functions[self.current_function].returns_tainted = True

        # Track all external function calls
        self.result.external_calls.append(func_name)

    def _collect_from_literal(self, node: Literal):
        """Collect information from literal values."""
        if isinstance(node, NumberLiteral):
            basic_type = BasicType.NUMBER
        elif isinstance(node, StringLiteral):
            basic_type = BasicType.STRING
        elif isinstance(node, BooleanLiteral):
            basic_type = BasicType.BOOLEAN
        else:
            basic_type = BasicType.UNKNOWN

        # Store expression info (though literals are rarely referenced directly)
        expr_info = ExpressionInfo(
            basic_type=basic_type,
            taint_level=TaintLevel.CLEAN,
            confidence=1.0,  # High confidence for literals
        )

        node_id = f"literal_{self.node_counter}"
        self.result.expressions[node_id] = expr_info

    def _collect_from_identifier(self, node: Identifier):
        """Collect information from identifier references."""
        var_name = node.name

        # If we have info about this variable, propagate it
        if var_name in self.result.variables:
            var_info = self.result.variables[var_name]
            if var_info.last_assignment:
                node_id = f"identifier_{var_name}_{self.node_counter}"
                self.result.expressions[node_id] = var_info.last_assignment

    def _collect_from_binary_expression(self, node: BinaryExpression):
        """Collect information from binary expressions."""
        # Analyze operands
        left_info = self._analyze_expression(node.left)
        right_info = self._analyze_expression(node.right)

        # Infer result type based on operation
        result_type = self._infer_binary_result_type(node.operator, left_info, right_info)

        # Propagate taint (if either operand is tainted, result is tainted)
        result_taint = TaintLevel.CLEAN
        if left_info.taint_level != TaintLevel.CLEAN or right_info.taint_level != TaintLevel.CLEAN:
            result_taint = max(left_info.taint_level, right_info.taint_level, key=lambda x: x.value)

        expr_info = ExpressionInfo(
            basic_type=result_type,
            taint_level=result_taint,
            confidence=min(left_info.confidence, right_info.confidence) * 0.9,
        )

        node_id = f"binary_expr_{self.node_counter}"
        self.result.expressions[node_id] = expr_info

    def _collect_from_array_literal(self, node: ArrayLiteral):
        """Collect information from array literals."""
        expr_info = ExpressionInfo(
            basic_type=BasicType.ARRAY, taint_level=TaintLevel.CLEAN, confidence=0.8
        )

        # Check if any elements are tainted
        if node.elements:
            for element in node.elements:
                element_info = self._analyze_expression(element)
                if element_info.taint_level != TaintLevel.CLEAN:
                    expr_info.taint_level = element_info.taint_level
                    break

        node_id = f"array_literal_{self.node_counter}"
        self.result.expressions[node_id] = expr_info

    def _collect_from_object_literal(self, node: ObjectLiteral):
        """Collect information from object literals."""
        expr_info = ExpressionInfo(
            basic_type=BasicType.OBJECT, taint_level=TaintLevel.CLEAN, confidence=0.8
        )

        node_id = f"object_literal_{self.node_counter}"
        self.result.expressions[node_id] = expr_info

    def _analyze_expression(self, expr: ASTNode) -> ExpressionInfo:
        """Analyze an expression and return its information."""
        if isinstance(expr, NumberLiteral):
            return ExpressionInfo(BasicType.NUMBER, TaintLevel.CLEAN, 1.0)
        elif isinstance(expr, StringLiteral):
            return ExpressionInfo(BasicType.STRING, TaintLevel.CLEAN, 1.0)
        elif isinstance(expr, BooleanLiteral):
            return ExpressionInfo(BasicType.BOOLEAN, TaintLevel.CLEAN, 1.0)
        elif isinstance(expr, ArrayLiteral):
            return ExpressionInfo(BasicType.ARRAY, TaintLevel.CLEAN, 0.8)
        elif isinstance(expr, ObjectLiteral):
            return ExpressionInfo(BasicType.OBJECT, TaintLevel.CLEAN, 0.8)
        elif isinstance(expr, Identifier):
            # Look up variable information
            if expr.name in self.result.variables:
                var_info = self.result.variables[expr.name]
                if var_info.last_assignment:
                    return var_info.last_assignment
            return ExpressionInfo(BasicType.UNKNOWN, TaintLevel.CLEAN, 0.2)
        elif isinstance(expr, FunctionCall):
            func_name = expr.function if isinstance(expr.function, str) else str(expr.function)
            taint = TaintLevel.USER_INPUT if func_name in self.TAINT_SOURCES else TaintLevel.CLEAN
            return ExpressionInfo(BasicType.UNKNOWN, taint, 0.3)
        else:
            return ExpressionInfo(BasicType.UNKNOWN, TaintLevel.CLEAN, 0.1)

    def _infer_binary_result_type(
        self, operator: str, left: ExpressionInfo, right: ExpressionInfo
    ) -> BasicType:
        """Infer the result type of a binary operation."""
        # String concatenation
        if operator == "+" and (
            left.basic_type == BasicType.STRING or right.basic_type == BasicType.STRING
        ):
            return BasicType.STRING

        # Numeric operations
        if (
            operator in ["+", "-", "*", "/", "%"]
            and left.basic_type == BasicType.NUMBER
            and right.basic_type == BasicType.NUMBER
        ):
            return BasicType.NUMBER

        # Comparison operations
        if operator in ["==", "!=", "<", ">", "<=", ">=", "&&", "||"]:
            return BasicType.BOOLEAN

        # Default: unknown
        return BasicType.UNKNOWN

    def _collect_from_children(self, node: ASTNode):
        """Recursively collect from child nodes."""
        if isinstance(node, Program) and node.items:
            for item in node.items:
                self._collect_from_node(item)
        elif isinstance(node, FunctionDefinition):
            # Function body handled in _collect_from_function
            pass
        elif isinstance(node, AssignmentStatement):
            self._collect_from_node(node.target)
            self._collect_from_node(node.value)
        elif isinstance(node, BinaryExpression):
            self._collect_from_node(node.left)
            self._collect_from_node(node.right)
        elif isinstance(node, UnaryExpression):
            self._collect_from_node(node.operand)
        elif isinstance(node, FunctionCall):
            self._collect_from_node(node.function)
            if node.arguments:
                for arg in node.arguments:
                    self._collect_from_node(arg)
        elif isinstance(node, ArrayLiteral) and node.elements:
            for element in node.elements:
                self._collect_from_node(element)
        elif isinstance(node, IfStatement):
            self._collect_from_node(node.condition)
            self._collect_from_node(node.then_statement)
            if node.elif_clauses:
                for elif_clause in node.elif_clauses:
                    self._collect_from_node(elif_clause)
            if node.else_statement:
                self._collect_from_node(node.else_statement)
        elif isinstance(node, WhileStatement):
            self._collect_from_node(node.condition)
            self._collect_from_node(node.body)
        elif isinstance(node, ExpressionStatement):
            self._collect_from_node(node.expression)
        # Add more node types as needed
