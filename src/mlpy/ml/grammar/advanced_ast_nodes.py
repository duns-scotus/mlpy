"""
Advanced AST nodes for Sprint 7 language constructs.
Extends the base AST with pattern matching, enhanced types, and advanced functions.
"""

from dataclasses import dataclass
from typing import Any, List, Optional, Union

from .ast_nodes import ASTNode, Expression, Statement, Type


# Pattern Matching System
@dataclass
class MatchExpression(Expression):
    """Match expression with pattern arms."""

    expression: Expression
    arms: List['MatchArm']

    def accept(self, visitor):
        return visitor.visit_match_expression(self)


@dataclass
class MatchArm(ASTNode):
    """Single arm of a match expression."""

    pattern: 'Pattern'
    guard: Optional[Expression] = None  # when clause
    body: Expression = None

    def accept(self, visitor):
        return visitor.visit_match_arm(self)


@dataclass
class Pattern(ASTNode):
    """Base class for all patterns."""

    def accept(self, visitor):
        return visitor.visit_pattern(self)


@dataclass
class LiteralPattern(Pattern):
    """Pattern that matches a literal value."""

    value: Any

    def accept(self, visitor):
        return visitor.visit_literal_pattern(self)


@dataclass
class IdentifierPattern(Pattern):
    """Pattern that binds to an identifier."""

    name: str

    def accept(self, visitor):
        return visitor.visit_identifier_pattern(self)


@dataclass
class ArrayPattern(Pattern):
    """Pattern that matches array structure."""

    elements: List[Pattern]
    rest: Optional[str] = None  # rest pattern identifier

    def accept(self, visitor):
        return visitor.visit_array_pattern(self)


@dataclass
class ObjectPattern(Pattern):
    """Pattern that matches object structure."""

    fields: List['ObjectPatternField']

    def accept(self, visitor):
        return visitor.visit_object_pattern(self)


@dataclass
class ObjectPatternField(ASTNode):
    """Field in object pattern."""

    name: str
    pattern: Optional[Pattern] = None  # None means bind to same name

    def accept(self, visitor):
        return visitor.visit_object_pattern_field(self)


@dataclass
class ConstructorPattern(Pattern):
    """Pattern that matches constructor calls."""

    constructor: str
    parameters: List[Pattern]

    def accept(self, visitor):
        return visitor.visit_constructor_pattern(self)


@dataclass
class RangePattern(Pattern):
    """Pattern that matches numeric ranges."""

    start: Expression
    end: Expression

    def accept(self, visitor):
        return visitor.visit_range_pattern(self)


@dataclass
class TypePattern(Pattern):
    """Pattern that matches based on type."""

    identifier: str
    type_expr: 'TypeExpression'

    def accept(self, visitor):
        return visitor.visit_type_pattern(self)


# Enhanced Type System
@dataclass
class TypeExpression(ASTNode):
    """Base class for type expressions."""

    def accept(self, visitor):
        return visitor.visit_type_expression(self)


@dataclass
class PrimitiveType(TypeExpression):
    """Primitive type like number, string, boolean."""

    name: str

    def accept(self, visitor):
        return visitor.visit_primitive_type(self)


@dataclass
class GenericType(TypeExpression):
    """Generic type with type parameters."""

    name: str
    type_parameters: List[TypeExpression]

    def accept(self, visitor):
        return visitor.visit_generic_type(self)


@dataclass
class FunctionType(TypeExpression):
    """Function type signature."""

    parameter_types: List[TypeExpression]
    return_type: TypeExpression

    def accept(self, visitor):
        return visitor.visit_function_type(self)


@dataclass
class UnionType(TypeExpression):
    """Union of multiple types."""

    types: List[TypeExpression]

    def accept(self, visitor):
        return visitor.visit_union_type(self)


@dataclass
class OptionalType(TypeExpression):
    """Optional/nullable type."""

    inner_type: TypeExpression

    def accept(self, visitor):
        return visitor.visit_optional_type(self)


@dataclass
class ArrayType(TypeExpression):
    """Array type with element type."""

    element_type: TypeExpression

    def accept(self, visitor):
        return visitor.visit_array_type(self)


# Advanced Function Constructs
@dataclass
class GenericFunction(Statement):
    """Function with generic type parameters."""

    type_parameters: List['TypeParameter']
    name: str
    parameters: List['Parameter']
    return_type: Optional[TypeExpression]
    body: List[Statement]

    def accept(self, visitor):
        return visitor.visit_generic_function(self)


@dataclass
class TypeParameter(ASTNode):
    """Generic type parameter."""

    name: str
    constraint: Optional[TypeExpression] = None  # extends clause

    def accept(self, visitor):
        return visitor.visit_type_parameter(self)


@dataclass
class PartialApplication(Expression):
    """Partial function application."""

    expression: Expression
    function: str

    def accept(self, visitor):
        return visitor.visit_partial_application(self)


@dataclass
class PipelineExpression(Expression):
    """Pipeline operator expression."""

    left: Expression
    right: Expression

    def accept(self, visitor):
        return visitor.visit_pipeline_expression(self)


@dataclass
class CompositionExpression(Expression):
    """Function composition expression."""

    left: Expression
    right: Expression

    def accept(self, visitor):
        return visitor.visit_composition_expression(self)


# Async/Await
@dataclass
class AsyncFunction(Statement):
    """Async function definition."""

    name: str
    parameters: List['Parameter']
    return_type: Optional[TypeExpression]
    body: List[Statement]

    def accept(self, visitor):
        return visitor.visit_async_function(self)


@dataclass
class AwaitExpression(Expression):
    """Await expression."""

    expression: Expression

    def accept(self, visitor):
        return visitor.visit_await_expression(self)


# Advanced Literals
@dataclass
class TupleLiteral(Expression):
    """Tuple literal."""

    elements: List[Expression]

    def accept(self, visitor):
        return visitor.visit_tuple_literal(self)


@dataclass
class SetLiteral(Expression):
    """Set literal."""

    elements: List[Expression]

    def accept(self, visitor):
        return visitor.visit_set_literal(self)


@dataclass
class MapLiteral(Expression):
    """Map literal."""

    entries: List['MapEntry']

    def accept(self, visitor):
        return visitor.visit_map_literal(self)


@dataclass
class MapEntry(ASTNode):
    """Map entry (key-value pair)."""

    key: Expression
    value: Expression

    def accept(self, visitor):
        return visitor.visit_map_entry(self)


# Comprehensions
@dataclass
class ArrayComprehension(Expression):
    """Array comprehension."""

    expression: Expression
    variable: str
    iterable: Expression
    condition: Optional[Expression] = None

    def accept(self, visitor):
        return visitor.visit_array_comprehension(self)


@dataclass
class ObjectComprehension(Expression):
    """Object comprehension."""

    key_expression: Expression
    value_expression: Expression
    variable: str
    iterable: Expression
    condition: Optional[Expression] = None

    def accept(self, visitor):
        return visitor.visit_object_comprehension(self)


# Module System Enhancements
@dataclass
class ExportStatement(Statement):
    """Export statement."""

    item: Union[Statement, Expression]

    def accept(self, visitor):
        return visitor.visit_export_statement(self)


@dataclass
class TypeDefinition(Statement):
    """Type alias definition."""

    name: str
    type_expression: Optional[TypeExpression] = None
    properties: Optional[List['TypeProperty']] = None

    def accept(self, visitor):
        return visitor.visit_type_definition(self)


@dataclass
class TypeProperty(ASTNode):
    """Property in type definition."""

    name: str
    type_expression: TypeExpression

    def accept(self, visitor):
        return visitor.visit_type_property(self)


@dataclass
class InterfaceDefinition(Statement):
    """Interface definition."""

    name: str
    members: List['InterfaceMember']

    def accept(self, visitor):
        return visitor.visit_interface_definition(self)


@dataclass
class InterfaceMember(ASTNode):
    """Member of interface."""

    name: str
    type_expression: TypeExpression
    parameters: Optional[List['Parameter']] = None  # for methods

    def accept(self, visitor):
        return visitor.visit_interface_member(self)


# Error Handling Enhancements
@dataclass
class ResultType(TypeExpression):
    """Result<T, E> type."""

    value_type: TypeExpression
    error_type: TypeExpression

    def accept(self, visitor):
        return visitor.visit_result_type(self)


@dataclass
class OptionType(TypeExpression):
    """Option<T> type."""

    inner_type: TypeExpression

    def accept(self, visitor):
        return visitor.visit_option_type(self)


@dataclass
class ErrorPropagation(Expression):
    """Error propagation operator (?)."""

    expression: Expression

    def accept(self, visitor):
        return visitor.visit_error_propagation(self)


# Capability-Based Features
@dataclass
class CapabilityFunction(Statement):
    """Function with capability requirements."""

    capabilities: List[str]
    function: 'Function'

    def accept(self, visitor):
        return visitor.visit_capability_function(self)


@dataclass
class SecureImport(Statement):
    """Secure import with capability checking."""

    import_statement: 'ImportStatement'

    def accept(self, visitor):
        return visitor.visit_secure_import(self)


@dataclass
class SandboxBlock(Statement):
    """Sandboxed execution block."""

    statements: List[Statement]

    def accept(self, visitor):
        return visitor.visit_sandbox_block(self)


# Metaprogramming (Limited)
@dataclass
class MacroDefinition(Statement):
    """Macro definition (limited for security)."""

    name: str
    parameters: List['Parameter']
    body: List[Any]  # Macro body tokens

    def accept(self, visitor):
        return visitor.visit_macro_definition(self)


@dataclass
class MacroCall(Expression):
    """Macro invocation."""

    name: str
    arguments: List[Expression]

    def accept(self, visitor):
        return visitor.visit_macro_call(self)


# Visitor base class extension
class AdvancedASTVisitor:
    """Extended visitor for advanced AST nodes."""

    # Pattern Matching
    def visit_match_expression(self, node: MatchExpression):
        pass

    def visit_match_arm(self, node: MatchArm):
        pass

    def visit_pattern(self, node: Pattern):
        pass

    def visit_literal_pattern(self, node: LiteralPattern):
        pass

    def visit_identifier_pattern(self, node: IdentifierPattern):
        pass

    def visit_array_pattern(self, node: ArrayPattern):
        pass

    def visit_object_pattern(self, node: ObjectPattern):
        pass

    def visit_object_pattern_field(self, node: ObjectPatternField):
        pass

    def visit_constructor_pattern(self, node: ConstructorPattern):
        pass

    def visit_range_pattern(self, node: RangePattern):
        pass

    def visit_type_pattern(self, node: TypePattern):
        pass

    # Enhanced Type System
    def visit_type_expression(self, node: TypeExpression):
        pass

    def visit_primitive_type(self, node: PrimitiveType):
        pass

    def visit_generic_type(self, node: GenericType):
        pass

    def visit_function_type(self, node: FunctionType):
        pass

    def visit_union_type(self, node: UnionType):
        pass

    def visit_optional_type(self, node: OptionalType):
        pass

    def visit_array_type(self, node: ArrayType):
        pass

    # Advanced Functions
    def visit_generic_function(self, node: GenericFunction):
        pass

    def visit_type_parameter(self, node: TypeParameter):
        pass

    def visit_partial_application(self, node: PartialApplication):
        pass

    def visit_pipeline_expression(self, node: PipelineExpression):
        pass

    def visit_composition_expression(self, node: CompositionExpression):
        pass

    # Async/Await
    def visit_async_function(self, node: AsyncFunction):
        pass

    def visit_await_expression(self, node: AwaitExpression):
        pass

    # Advanced Literals
    def visit_tuple_literal(self, node: TupleLiteral):
        pass

    def visit_set_literal(self, node: SetLiteral):
        pass

    def visit_map_literal(self, node: MapLiteral):
        pass

    def visit_map_entry(self, node: MapEntry):
        pass

    # Comprehensions
    def visit_array_comprehension(self, node: ArrayComprehension):
        pass

    def visit_object_comprehension(self, node: ObjectComprehension):
        pass

    # Module System
    def visit_export_statement(self, node: ExportStatement):
        pass

    def visit_type_definition(self, node: TypeDefinition):
        pass

    def visit_type_property(self, node: TypeProperty):
        pass

    def visit_interface_definition(self, node: InterfaceDefinition):
        pass

    def visit_interface_member(self, node: InterfaceMember):
        pass

    # Error Handling
    def visit_result_type(self, node: ResultType):
        pass

    def visit_option_type(self, node: OptionType):
        pass

    def visit_error_propagation(self, node: ErrorPropagation):
        pass

    # Capability Features
    def visit_capability_function(self, node: CapabilityFunction):
        pass

    def visit_secure_import(self, node: SecureImport):
        pass

    def visit_sandbox_block(self, node: SandboxBlock):
        pass

    # Metaprogramming
    def visit_macro_definition(self, node: MacroDefinition):
        pass

    def visit_macro_call(self, node: MacroCall):
        pass