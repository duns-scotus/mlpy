"""AST node definitions for the mlpy ML language."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional


class ASTNode(ABC):
    """Base class for all AST nodes."""

    def __init__(self, line: int | None = None, column: int | None = None):
        self.line = line
        self.column = column

    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for the visitor pattern."""
        pass


class Program(ASTNode):
    """Root node representing the entire program."""

    def __init__(self, items: list[ASTNode], line: int | None = None, column: int | None = None):
        super().__init__(line, column)
        self.items = items

    def accept(self, visitor):
        return visitor.visit_program(self)


# Capability System Nodes
@dataclass
class CapabilityDeclaration(ASTNode):
    """Capability declaration for security control."""

    name: str
    items: list["CapabilityItem"]

    def accept(self, visitor):
        return visitor.visit_capability_declaration(self)


@dataclass
class CapabilityItem(ASTNode):
    """Base class for capability items."""

    pass


@dataclass
class ResourcePattern(CapabilityItem):
    """Resource pattern in capability declaration."""

    pattern: str

    def accept(self, visitor):
        return visitor.visit_resource_pattern(self)


@dataclass
class PermissionGrant(CapabilityItem):
    """Permission grant in capability declaration."""

    permission_type: str  # "read", "write", "execute", "network", "system"
    target: str | None = None

    def accept(self, visitor):
        return visitor.visit_permission_grant(self)


# Import Statements
@dataclass
class ImportStatement(ASTNode):
    """Import statement with security analysis."""

    target: list[str]  # Module path as list
    alias: str | None = None

    def accept(self, visitor):
        return visitor.visit_import_statement(self)


# Function Definitions
@dataclass
class FunctionDefinition(ASTNode):
    """Function definition."""

    name: str
    parameters: list["Parameter"]
    body: list["Statement"]

    def accept(self, visitor):
        return visitor.visit_function_definition(self)


@dataclass
class Parameter(ASTNode):
    """Function parameter."""

    name: str
    type_annotation: str | None = None

    def accept(self, visitor):
        return visitor.visit_parameter(self)


# Statements
@dataclass
class Statement(ASTNode):
    """Base class for statements."""

    pass


@dataclass
class ExpressionStatement(Statement):
    """Expression used as statement."""

    expression: "Expression"

    def accept(self, visitor):
        return visitor.visit_expression_statement(self)


@dataclass
class AssignmentStatement(Statement):
    """Variable assignment."""

    target: str
    value: "Expression"

    def accept(self, visitor):
        return visitor.visit_assignment_statement(self)


@dataclass
class ReturnStatement(Statement):
    """Return statement."""

    value: Optional["Expression"] = None

    def accept(self, visitor):
        return visitor.visit_return_statement(self)


@dataclass
class BlockStatement(Statement):
    """Block of statements."""

    statements: list[Statement]

    def accept(self, visitor):
        return visitor.visit_block_statement(self)


@dataclass
class IfStatement(Statement):
    """If conditional statement."""

    condition: "Expression"
    then_statement: Statement
    else_statement: Statement | None = None

    def accept(self, visitor):
        return visitor.visit_if_statement(self)


@dataclass
class WhileStatement(Statement):
    """While loop statement."""

    condition: "Expression"
    body: Statement

    def accept(self, visitor):
        return visitor.visit_while_statement(self)


@dataclass
class ForStatement(Statement):
    """For loop statement."""

    variable: str
    iterable: "Expression"
    body: Statement

    def accept(self, visitor):
        return visitor.visit_for_statement(self)


# Expressions
@dataclass
class Expression(ASTNode):
    """Base class for expressions."""

    pass


@dataclass
class BinaryExpression(Expression):
    """Binary operation expression."""

    left: Expression
    operator: str
    right: Expression

    def accept(self, visitor):
        return visitor.visit_binary_expression(self)


@dataclass
class UnaryExpression(Expression):
    """Unary operation expression."""

    operator: str
    operand: Expression

    def accept(self, visitor):
        return visitor.visit_unary_expression(self)


@dataclass
class Identifier(Expression):
    """Variable or function identifier."""

    name: str

    def accept(self, visitor):
        return visitor.visit_identifier(self)


@dataclass
class FunctionCall(Expression):
    """Function call expression - Security Critical."""

    function: str
    arguments: list[Expression]

    def accept(self, visitor):
        return visitor.visit_function_call(self)


@dataclass
class ArrayAccess(Expression):
    """Array access expression."""

    array: Expression
    index: Expression

    def accept(self, visitor):
        return visitor.visit_array_access(self)


@dataclass
class MemberAccess(Expression):
    """Member access expression - Security Critical."""

    object: Expression
    member: str

    def accept(self, visitor):
        return visitor.visit_member_access(self)


# Literals
@dataclass
class Literal(Expression):
    """Base class for literal values."""

    value: Any

    def accept(self, visitor):
        return visitor.visit_literal(self)


@dataclass
class NumberLiteral(Literal):
    """Numeric literal."""

    def accept(self, visitor):
        return visitor.visit_number_literal(self)


@dataclass
class StringLiteral(Literal):
    """String literal."""

    def accept(self, visitor):
        return visitor.visit_string_literal(self)


@dataclass
class BooleanLiteral(Literal):
    """Boolean literal."""

    def accept(self, visitor):
        return visitor.visit_boolean_literal(self)


@dataclass
class ArrayLiteral(Literal):
    """Array literal."""

    elements: list[Expression]

    def accept(self, visitor):
        return visitor.visit_array_literal(self)


@dataclass
class ObjectLiteral(Literal):
    """Object literal."""

    properties: dict[str, Expression]

    def accept(self, visitor):
        return visitor.visit_object_literal(self)


# Visitor Interface
class ASTVisitor(ABC):
    """Visitor interface for traversing AST nodes."""

    @abstractmethod
    def visit_program(self, node: Program):
        pass

    @abstractmethod
    def visit_capability_declaration(self, node: CapabilityDeclaration):
        pass

    @abstractmethod
    def visit_resource_pattern(self, node: ResourcePattern):
        pass

    @abstractmethod
    def visit_permission_grant(self, node: PermissionGrant):
        pass

    @abstractmethod
    def visit_import_statement(self, node: ImportStatement):
        pass

    @abstractmethod
    def visit_function_definition(self, node: FunctionDefinition):
        pass

    @abstractmethod
    def visit_parameter(self, node: Parameter):
        pass

    @abstractmethod
    def visit_expression_statement(self, node: ExpressionStatement):
        pass

    @abstractmethod
    def visit_assignment_statement(self, node: AssignmentStatement):
        pass

    @abstractmethod
    def visit_return_statement(self, node: ReturnStatement):
        pass

    @abstractmethod
    def visit_block_statement(self, node: BlockStatement):
        pass

    @abstractmethod
    def visit_if_statement(self, node: IfStatement):
        pass

    @abstractmethod
    def visit_while_statement(self, node: WhileStatement):
        pass

    @abstractmethod
    def visit_for_statement(self, node: ForStatement):
        pass

    @abstractmethod
    def visit_binary_expression(self, node: BinaryExpression):
        pass

    @abstractmethod
    def visit_unary_expression(self, node: UnaryExpression):
        pass

    @abstractmethod
    def visit_identifier(self, node: Identifier):
        pass

    @abstractmethod
    def visit_function_call(self, node: FunctionCall):
        pass

    @abstractmethod
    def visit_array_access(self, node: ArrayAccess):
        pass

    @abstractmethod
    def visit_member_access(self, node: MemberAccess):
        pass

    @abstractmethod
    def visit_literal(self, node: Literal):
        pass

    @abstractmethod
    def visit_number_literal(self, node: NumberLiteral):
        pass

    @abstractmethod
    def visit_string_literal(self, node: StringLiteral):
        pass

    @abstractmethod
    def visit_boolean_literal(self, node: BooleanLiteral):
        pass

    @abstractmethod
    def visit_array_literal(self, node: ArrayLiteral):
        pass

    @abstractmethod
    def visit_object_literal(self, node: ObjectLiteral):
        pass
