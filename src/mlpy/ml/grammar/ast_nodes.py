"""AST node definitions for the mlpy ML language."""

from abc import ABC, abstractmethod
from typing import Any, Optional, Union


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
    """Variable, array element, or object property assignment."""

    def __init__(
        self,
        target: Union[str, "Expression"],
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


class ElifClause(ASTNode):
    """Elif clause for if statements."""

    def __init__(
        self,
        condition: "Expression",
        statement: Statement,
        line: int | None = None,
        column: int | None = None,
    ):
        super().__init__(line, column)
        self.condition = condition
        self.statement = statement

    def accept(self, visitor):
        return visitor.visit_elif_clause(self)


class IfStatement(Statement):
    """If conditional statement with optional elif clauses."""

    def __init__(
        self,
        condition: "Expression",
        then_statement: Statement,
        elif_clauses: list[ElifClause] | None = None,
        else_statement: Statement | None = None,
        line: int | None = None,
        column: int | None = None,
    ):
        super().__init__(line, column)
        self.condition = condition
        self.then_statement = then_statement
        self.elif_clauses = elif_clauses or []
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
        variable: "Identifier",
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


class TryStatement(Statement):
    """Try/except/finally statement."""

    def __init__(
        self,
        try_body: list[Statement],
        except_clauses: list["ExceptClause"],
        finally_body: list[Statement] | None = None,
        line: int | None = None,
        column: int | None = None,
    ):
        super().__init__(line, column)
        self.try_body = try_body
        self.except_clauses = except_clauses
        self.finally_body = finally_body or []

    def accept(self, visitor):
        return visitor.visit_try_statement(self)


class ExceptClause(ASTNode):
    """Except clause in try statement."""

    def __init__(
        self,
        exception_type: str | None = None,
        exception_variable: str | None = None,
        body: list[Statement] | None = None,
        line: int | None = None,
        column: int | None = None,
    ):
        super().__init__(line, column)
        self.exception_type = exception_type
        self.exception_variable = exception_variable
        self.body = body or []

    def accept(self, visitor):
        return visitor.visit_except_clause(self)


class BreakStatement(Statement):
    """Break statement for loop control."""

    def __init__(self, line: int | None = None, column: int | None = None):
        super().__init__(line, column)

    def accept(self, visitor):
        return visitor.visit_break_statement(self)


class ContinueStatement(Statement):
    """Continue statement for loop control."""

    def __init__(self, line: int | None = None, column: int | None = None):
        super().__init__(line, column)

    def accept(self, visitor):
        return visitor.visit_continue_statement(self)


class NonlocalStatement(Statement):
    """Nonlocal statement for closure variable access."""

    def __init__(self, variables: list[str], line: int | None = None, column: int | None = None):
        super().__init__(line, column)
        self.variables = variables

    def accept(self, visitor):
        return visitor.visit_nonlocal_statement(self)


class ThrowStatement(Statement):
    """Throw statement for raising user exceptions with dictionary data."""

    def __init__(
        self,
        error_data: "ObjectLiteral",
        line: int | None = None,
        column: int | None = None,
    ):
        super().__init__(line, column)
        self.error_data = error_data

    def accept(self, visitor):
        return visitor.visit_throw_statement(self)


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


class TernaryExpression(Expression):
    """Ternary conditional expression (condition ? true_value : false_value)."""

    def __init__(
        self,
        condition: Expression,
        true_value: Expression,
        false_value: Expression,
        line: int | None = None,
        column: int | None = None,
    ):
        super().__init__(line, column)
        self.condition = condition
        self.true_value = true_value
        self.false_value = false_value

    def accept(self, visitor):
        return visitor.visit_ternary_expression(self)


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


class SliceExpression(Expression):
    """Slice expression for array/string slicing (Python-style)."""

    def __init__(
        self,
        start: Expression | None = None,
        end: Expression | None = None,
        step: Expression | None = None,
        line: int | None = None,
        column: int | None = None,
    ):
        super().__init__(line, column)
        self.start = start
        self.end = end
        self.step = step

    def accept(self, visitor):
        return visitor.visit_slice_expression(self)


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


# Advanced Language Constructs


class DestructuringPattern(ASTNode):
    """Base class for destructuring patterns."""

    pass


class ArrayDestructuring(DestructuringPattern):
    """Array destructuring pattern like [a, b, ...rest]."""

    def __init__(
        self,
        elements: list[str],
        rest_element: str | None = None,
        line: int | None = None,
        column: int | None = None,
    ):
        super().__init__(line, column)
        self.elements = elements
        self.rest_element = rest_element

    def accept(self, visitor):
        return visitor.visit_array_destructuring(self)


class ObjectDestructuring(DestructuringPattern):
    """Object destructuring pattern like {a, b: newName, ...rest}."""

    def __init__(
        self,
        properties: dict[str, str],  # {original_key: new_variable_name}
        rest_element: str | None = None,
        line: int | None = None,
        column: int | None = None,
    ):
        super().__init__(line, column)
        self.properties = properties
        self.rest_element = rest_element

    def accept(self, visitor):
        return visitor.visit_object_destructuring(self)


class DestructuringAssignment(Statement):
    """Destructuring assignment statement."""

    def __init__(
        self,
        pattern: DestructuringPattern,
        value: Expression,
        line: int | None = None,
        column: int | None = None,
    ):
        super().__init__(line, column)
        self.pattern = pattern
        self.value = value

    def accept(self, visitor):
        return visitor.visit_destructuring_assignment(self)


class SpreadElement(Expression):
    """Spread element like ...array or ...object."""

    def __init__(
        self,
        argument: Expression,
        line: int | None = None,
        column: int | None = None,
    ):
        super().__init__(line, column)
        self.argument = argument

    def accept(self, visitor):
        return visitor.visit_spread_element(self)


class ArrowFunction(Expression):
    """Arrow function expression like (a, b) => a + b."""

    def __init__(
        self,
        parameters: list["Parameter"],
        body: Expression | Statement,
        is_async: bool = False,
        line: int | None = None,
        column: int | None = None,
    ):
        super().__init__(line, column)
        self.parameters = parameters
        self.body = body
        self.is_async = is_async

    def accept(self, visitor):
        return visitor.visit_arrow_function(self)


class MatchExpression(Expression):
    """Pattern matching expression."""

    def __init__(
        self,
        value: Expression,
        cases: list["MatchCase"],
        line: int | None = None,
        column: int | None = None,
    ):
        super().__init__(line, column)
        self.value = value
        self.cases = cases

    def accept(self, visitor):
        return visitor.visit_match_expression(self)


class MatchCase(ASTNode):
    """Single case in a match expression."""

    def __init__(
        self,
        pattern: Expression,
        guard: Expression | None,
        body: Expression,
        line: int | None = None,
        column: int | None = None,
    ):
        super().__init__(line, column)
        self.pattern = pattern
        self.guard = guard
        self.body = body

    def accept(self, visitor):
        return visitor.visit_match_case(self)


class PipelineExpression(Expression):
    """Pipeline expression like value |> func1 |> func2."""

    def __init__(
        self,
        value: Expression,
        operations: list[Expression],
        line: int | None = None,
        column: int | None = None,
    ):
        super().__init__(line, column)
        self.value = value
        self.operations = operations

    def accept(self, visitor):
        return visitor.visit_pipeline_expression(self)


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
    def visit_elif_clause(self, node: ElifClause):
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

    @abstractmethod
    def visit_try_statement(self, node: TryStatement):
        pass

    @abstractmethod
    def visit_except_clause(self, node: ExceptClause):
        pass

    @abstractmethod
    def visit_break_statement(self, node: BreakStatement):
        pass

    @abstractmethod
    def visit_continue_statement(self, node: ContinueStatement):
        pass

    @abstractmethod
    def visit_throw_statement(self, node: ThrowStatement):
        pass

    @abstractmethod
    def visit_ternary_expression(self, node: TernaryExpression):
        pass

    # Advanced language construct visitors
    @abstractmethod
    def visit_array_destructuring(self, node: ArrayDestructuring):
        pass

    @abstractmethod
    def visit_object_destructuring(self, node: ObjectDestructuring):
        pass

    @abstractmethod
    def visit_destructuring_assignment(self, node: DestructuringAssignment):
        pass

    @abstractmethod
    def visit_spread_element(self, node: SpreadElement):
        pass

    @abstractmethod
    def visit_arrow_function(self, node: ArrowFunction):
        pass

    @abstractmethod
    def visit_match_expression(self, node: MatchExpression):
        pass

    @abstractmethod
    def visit_match_case(self, node: MatchCase):
        pass

    @abstractmethod
    def visit_pipeline_expression(self, node: PipelineExpression):
        pass
