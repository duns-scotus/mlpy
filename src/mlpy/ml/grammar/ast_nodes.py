"""AST node definitions for the mlpy ML language."""

from abc import ABC, abstractmethod
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

    def __init__(
        self, items: list[ASTNode], line: int | None = None, column: int | None = None
    ):
        super().__init__(line, column)
        self.items = items

    def accept(self, visitor):
        return visitor.visit_program(self)


# Capability System Nodes
class CapabilityDeclaration(ASTNode):
    """Capability declaration for security control."""

    def __init__(
        self,
        name: str,
        items: list["CapabilityItem"],
        line: int | None = None,
        column: int | None = None,
    ):
        super().__init__(line, column)
        self.name = name
        self.items = items

    def accept(self, visitor):
        return visitor.visit_capability_declaration(self)


class CapabilityItem(ASTNode):
    """Base class for capability items."""

    pass


class ResourcePattern(CapabilityItem):
    """Resource pattern in capability declaration."""

    def __init__(self, pattern: str, line: int | None = None, column: int | None = None):
        super().__init__(line, column)
        self.pattern = pattern

    def accept(self, visitor):
        return visitor.visit_resource_pattern(self)


class PermissionGrant(CapabilityItem):
    """Permission grant in capability declaration."""

    def __init__(
        self,
        permission_type: str,
        target: str | None = None,
        line: int | None = None,
        column: int | None = None,
    ):
        super().__init__(line, column)
        self.permission_type = permission_type
        self.target = target

    def accept(self, visitor):
        return visitor.visit_permission_grant(self)


# Import Statements
class ImportStatement(ASTNode):
    """Import statement with security analysis."""

    def __init__(
        self,
        target: list[str],
        alias: str | None = None,
        line: int | None = None,
        column: int | None = None,
    ):
        super().__init__(line, column)
        self.target = target
        self.alias = alias

    def accept(self, visitor):
        return visitor.visit_import_statement(self)


# Function Definitions
class FunctionDefinition(ASTNode):
    """Function definition."""

    def __init__(
        self,
        name: str,
        parameters: list["Parameter"],
        body: list["Statement"],
        line: int | None = None,
        column: int | None = None,
    ):
        super().__init__(line, column)
        self.name = name
        self.parameters = parameters
        self.body = body

    def accept(self, visitor):
        return visitor.visit_function_definition(self)


class Parameter(ASTNode):
    """Function parameter."""

    def __init__(
        self,
        name: str,
        type_annotation: str | None = None,
        line: int | None = None,
        column: int | None = None,
    ):
        super().__init__(line, column)
        self.name = name
        self.type_annotation = type_annotation

    def accept(self, visitor):
        return visitor.visit_parameter(self)


# Statements
class Statement(ASTNode):
    """Base class for statements."""

    pass


class ExpressionStatement(Statement):
    """Expression used as statement."""

    def __init__(
        self, expression: "Expression", line: int | None = None, column: int | None = None
    ):
        super().__init__(line, column)
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_expression_statement(self)


class AssignmentStatement(Statement):
    """Variable assignment."""

    def __init__(
        self,
        target: str,
        value: "Expression",
        line: int | None = None,
        column: int | None = None,
    ):
        super().__init__(line, column)
        self.target = target
        self.value = value

    def accept(self, visitor):
        return visitor.visit_assignment_statement(self)


class ReturnStatement(Statement):
    """Return statement."""

    def __init__(
        self,
        value: Optional["Expression"] = None,
        line: int | None = None,
        column: int | None = None,
    ):
        super().__init__(line, column)
        self.value = value

    def accept(self, visitor):
        return visitor.visit_return_statement(self)


class BlockStatement(Statement):
    """Block of statements."""

    def __init__(
        self, statements: list[Statement], line: int | None = None, column: int | None = None
    ):
        super().__init__(line, column)
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_block_statement(self)


class IfStatement(Statement):
    """If conditional statement."""

    def __init__(
        self,
        condition: "Expression",
        then_statement: Statement,
        else_statement: Statement | None = None,
        line: int | None = None,
        column: int | None = None,
    ):
        super().__init__(line, column)
        self.condition = condition
        self.then_statement = then_statement
        self.else_statement = else_statement

    def accept(self, visitor):
        return visitor.visit_if_statement(self)


class WhileStatement(Statement):
    """While loop statement."""

    def __init__(
        self,
        condition: "Expression",
        body: Statement,
        line: int | None = None,
        column: int | None = None,
    ):
        super().__init__(line, column)
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visit_while_statement(self)


class ForStatement(Statement):
    """For loop statement."""

    def __init__(
        self,
        variable: str,
        iterable: "Expression",
        body: Statement,
        line: int | None = None,
        column: int | None = None,
    ):
        super().__init__(line, column)
        self.variable = variable
        self.iterable = iterable
        self.body = body

    def accept(self, visitor):
        return visitor.visit_for_statement(self)


# Expressions
class Expression(ASTNode):
    """Base class for expressions."""

    pass


class BinaryExpression(Expression):
    """Binary operation expression."""

    def __init__(
        self,
        left: Expression,
        operator: str,
        right: Expression,
        line: int | None = None,
        column: int | None = None,
    ):
        super().__init__(line, column)
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary_expression(self)


class UnaryExpression(Expression):
    """Unary operation expression."""

    def __init__(
        self,
        operator: str,
        operand: Expression,
        line: int | None = None,
        column: int | None = None,
    ):
        super().__init__(line, column)
        self.operator = operator
        self.operand = operand

    def accept(self, visitor):
        return visitor.visit_unary_expression(self)


class Identifier(Expression):
    """Variable or function identifier."""

    def __init__(self, name: str, line: int | None = None, column: int | None = None):
        super().__init__(line, column)
        self.name = name

    def accept(self, visitor):
        return visitor.visit_identifier(self)


class FunctionCall(Expression):
    """Function call expression - Security Critical."""

    def __init__(
        self,
        function: str,
        arguments: list[Expression],
        line: int | None = None,
        column: int | None = None,
    ):
        super().__init__(line, column)
        self.function = function
        self.arguments = arguments

    def accept(self, visitor):
        return visitor.visit_function_call(self)


class ArrayAccess(Expression):
    """Array access expression."""

    def __init__(
        self,
        array: Expression,
        index: Expression,
        line: int | None = None,
        column: int | None = None,
    ):
        super().__init__(line, column)
        self.array = array
        self.index = index

    def accept(self, visitor):
        return visitor.visit_array_access(self)


class MemberAccess(Expression):
    """Member access expression - Security Critical."""

    def __init__(
        self,
        object: Expression,
        member: str,
        line: int | None = None,
        column: int | None = None,
    ):
        super().__init__(line, column)
        self.object = object
        self.member = member

    def accept(self, visitor):
        return visitor.visit_member_access(self)


# Literals
class Literal(Expression):
    """Base class for literal values."""

    def __init__(self, value: Any, line: int | None = None, column: int | None = None):
        super().__init__(line, column)
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal(self)


class NumberLiteral(Literal):
    """Numeric literal."""

    def accept(self, visitor):
        return visitor.visit_number_literal(self)


class StringLiteral(Literal):
    """String literal."""

    def accept(self, visitor):
        return visitor.visit_string_literal(self)


class BooleanLiteral(Literal):
    """Boolean literal."""

    def accept(self, visitor):
        return visitor.visit_boolean_literal(self)


class ArrayLiteral(Literal):
    """Array literal."""

    def __init__(
        self, elements: list[Expression], line: int | None = None, column: int | None = None
    ):
        super().__init__(elements, line, column)
        self.elements = elements

    def accept(self, visitor):
        return visitor.visit_array_literal(self)


class ObjectLiteral(Literal):
    """Object literal."""

    def __init__(
        self,
        properties: dict[str, Expression],
        line: int | None = None,
        column: int | None = None,
    ):
        super().__init__(properties, line, column)
        self.properties = properties

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
