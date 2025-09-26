"""
AST Validator - Phase 1 Pipeline Stage (Simplified)

Minimal structural validation that only catches issues the grammar can't prevent:
1. Context-sensitive control flow (break/continue outside loops, return outside functions)
2. Critical null fields that would crash downstream stages
3. Stack overflow prevention for deeply nested ASTs

Everything else (semantics, types, security) is handled by later pipeline stages.
"""

from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass
from enum import Enum

from ..grammar.ast_nodes import (
    ASTNode, Program, FunctionDefinition, AssignmentStatement,
    IfStatement, ElifClause, WhileStatement, ForStatement, TryStatement,
    BinaryExpression, UnaryExpression, FunctionCall, Identifier,
    Literal, ArrayLiteral, ObjectLiteral, MemberAccess,
    ArrayAccess, ReturnStatement, BreakStatement, ContinueStatement,
    ImportStatement, ExpressionStatement, BlockStatement
)


class ValidationSeverity(Enum):
    """Severity levels for validation issues."""
    ERROR = "ERROR"      # Blocks further processing
    WARNING = "WARNING"  # Allows processing but reports issues


@dataclass
class ValidationIssue:
    """Represents a validation issue found in the AST."""
    severity: ValidationSeverity
    message: str
    node_type: str
    line: Optional[int] = None
    column: Optional[int] = None
    context: Optional[str] = None


@dataclass
class ValidationResult:
    """Result of AST validation."""
    is_valid: bool
    issues: List[ValidationIssue]
    node_count: int
    validation_time_ms: float

    @property
    def errors(self) -> List[ValidationIssue]:
        """Get only error-level issues."""
        return [issue for issue in self.issues if issue.severity == ValidationSeverity.ERROR]

    @property
    def warnings(self) -> List[ValidationIssue]:
        """Get only warning-level issues."""
        return [issue for issue in self.issues if issue.severity == ValidationSeverity.WARNING]


class ASTValidator:
    """
    Minimal AST validator for structural integrity only.

    Focuses on high-value checks that prevent crashes in downstream stages:
    - Control flow context validation (break/continue/return placement)
    - Critical field validation (prevent null pointer crashes)
    - Stack overflow prevention (recursion depth limits)
    """

    def __init__(self):
        self.issues: List[ValidationIssue] = []
        self.node_count: int = 0
        self.scope_stack: List[str] = []  # Track context: 'function', 'loop'

    def validate(self, ast: ASTNode) -> ValidationResult:
        """
        Validate the AST structure with minimal checks.

        Args:
            ast: Root AST node to validate

        Returns:
            ValidationResult with validation status and any issues found
        """
        import time
        start_time = time.perf_counter()

        # Reset validation state
        self.issues = []
        self.node_count = 0
        self.scope_stack = []

        # Perform minimal validation
        self._validate_node(ast)

        validation_time_ms = (time.perf_counter() - start_time) * 1000

        # Validation passes if no errors (warnings are OK)
        is_valid = not any(issue.severity == ValidationSeverity.ERROR for issue in self.issues)

        return ValidationResult(
            is_valid=is_valid,
            issues=self.issues,
            node_count=self.node_count,
            validation_time_ms=validation_time_ms
        )

    def _add_issue(
        self,
        severity: ValidationSeverity,
        message: str,
        node: Optional[ASTNode] = None,
        context: Optional[str] = None
    ):
        """Add a validation issue."""
        issue = ValidationIssue(
            severity=severity,
            message=message,
            node_type=type(node).__name__ if node else "Unknown",
            line=getattr(node, 'line', None),
            column=getattr(node, 'column', None),
            context=context
        )
        self.issues.append(issue)

    def _validate_node(self, node: ASTNode):
        """Validate a single AST node with minimal structural checks only."""
        if node is None:
            self._add_issue(ValidationSeverity.ERROR, "Null node encountered")
            return

        self.node_count += 1

        # Check recursion depth to prevent stack overflow
        if len(self.scope_stack) > 1000:  # MAX_SAFE_DEPTH
            self._add_issue(ValidationSeverity.ERROR, "AST too deeply nested (potential stack overflow)", node)
            return

        # Only validate critical structural issues
        self._validate_critical_fields(node)
        self._validate_control_flow_context(node)

        # Recursively validate children
        self._validate_children(node)

    def _validate_critical_fields(self, node: ASTNode):
        """Check only critical fields that would crash downstream stages."""
        if isinstance(node, Identifier):
            if not hasattr(node, 'name') or not node.name:
                self._add_issue(ValidationSeverity.ERROR, "Identifier missing name", node)
        elif isinstance(node, FunctionDefinition):
            if not hasattr(node, 'name') or not node.name:
                self._add_issue(ValidationSeverity.ERROR, "Function missing name", node)
        elif isinstance(node, ImportStatement):
            if not hasattr(node, 'target') or not node.target:
                self._add_issue(ValidationSeverity.ERROR, "Import statement missing target", node)

    def _validate_control_flow_context(self, node: ASTNode):
        """Check context-sensitive control flow that grammar can't enforce."""
        if isinstance(node, (BreakStatement, ContinueStatement)):
            if not self._in_loop_context():
                stmt_type = "break" if isinstance(node, BreakStatement) else "continue"
                self._add_issue(ValidationSeverity.ERROR, f"{stmt_type} statement outside loop", node)
        elif isinstance(node, ReturnStatement):
            if not self._in_function_context():
                self._add_issue(ValidationSeverity.ERROR, "return statement outside function", node)

    def _validate_children(self, node: ASTNode):
        """Recursively validate child nodes."""
        # Track context for control flow validation
        if isinstance(node, FunctionDefinition):
            self.scope_stack.append('function')
        elif isinstance(node, (WhileStatement, ForStatement)):
            self.scope_stack.append('loop')

        # Validate all child nodes
        for child in self._get_child_nodes(node):
            if child is not None:
                self._validate_node(child)

        # Pop context
        if isinstance(node, (FunctionDefinition, WhileStatement, ForStatement)):
            self.scope_stack.pop()

    def _in_loop_context(self) -> bool:
        """Check if currently inside a loop."""
        return 'loop' in self.scope_stack

    def _in_function_context(self) -> bool:
        """Check if currently inside a function."""
        return 'function' in self.scope_stack

    def _get_child_nodes(self, node: ASTNode) -> List[ASTNode]:
        """Get all child nodes for recursive validation."""
        children = []

        if isinstance(node, Program):
            children.extend(node.items or [])
        elif isinstance(node, FunctionDefinition):
            children.extend(node.parameters or [])
            if node.body:
                children.append(node.body)
        elif isinstance(node, BlockStatement):
            children.extend(node.statements or [])
        elif isinstance(node, IfStatement):
            if node.condition:
                children.append(node.condition)
            if node.then_statement:
                children.append(node.then_statement)
            if node.elif_clauses:
                for elif_clause in node.elif_clauses:
                    children.append(elif_clause)
            if node.else_statement:
                children.append(node.else_statement)
        elif isinstance(node, ElifClause):
            if node.condition:
                children.append(node.condition)
            if node.statement:
                children.append(node.statement)
        elif isinstance(node, WhileStatement):
            if node.condition:
                children.append(node.condition)
            if node.body:
                children.append(node.body)
        elif isinstance(node, ForStatement):
            if node.init:
                children.append(node.init)
            if node.condition:
                children.append(node.condition)
            if node.update:
                children.append(node.update)
            if node.body:
                children.append(node.body)
        elif isinstance(node, BinaryExpression):
            if node.left:
                children.append(node.left)
            if node.right:
                children.append(node.right)
        elif isinstance(node, UnaryExpression):
            if node.operand:
                children.append(node.operand)
        elif isinstance(node, FunctionCall):
            if node.function:
                children.append(node.function)
            children.extend(node.arguments or [])
        elif isinstance(node, ArrayLiteral):
            children.extend(node.elements or [])
        elif isinstance(node, ObjectLiteral):
            if hasattr(node, 'properties'):
                for prop in node.properties or []:
                    if hasattr(prop, 'value'):
                        children.append(prop.value)
        elif isinstance(node, MemberAccess):
            if node.object:
                children.append(node.object)
        elif isinstance(node, ArrayAccess):
            if node.object:
                children.append(node.object)
            if node.index:
                children.append(node.index)
        elif isinstance(node, AssignmentStatement):
            if node.target:
                children.append(node.target)
            if node.value:
                children.append(node.value)
        elif isinstance(node, ReturnStatement):
            if node.value:
                children.append(node.value)
        elif isinstance(node, ExpressionStatement):
            if node.expression:
                children.append(node.expression)
        elif isinstance(node, TryStatement):
            if node.body:
                children.append(node.body)
            if node.catch_clause and hasattr(node.catch_clause, 'body'):
                children.append(node.catch_clause.body)
            if node.finally_clause:
                children.append(node.finally_clause)

        return children