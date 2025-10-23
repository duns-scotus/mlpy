"""Literal visitor methods for Python code generation.

This module contains visitor methods for all literal AST nodes in the ML language.
All literal generation is handled by the _generate_expression() method in the
ExpressionHelpersMixin, so these methods are stubs that satisfy the visitor pattern.

Part of the modular code generator architecture (Phase 3d).
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mlpy.ml.grammar.ast_nodes import (
        Literal,
        NumberLiteral,
        StringLiteral,
        BooleanLiteral,
        ArrayLiteral,
        ObjectLiteral,
    )


class LiteralVisitorsMixin:
    """Mixin providing visitor methods for literal AST nodes.

    This mixin handles all literal value nodes in the ML AST. The actual code
    generation logic is implemented in ExpressionHelpersMixin._generate_expression(),
    so these visitor methods are stubs that allow the visitor pattern to work correctly.

    Literal types supported:
    - Number literals: integers, floats, scientific notation
    - String literals: single/double quoted strings with escape sequences
    - Boolean literals: true/false
    - Array literals: [1, 2, 3]
    - Object literals: {key: value, ...}
    - Special literals: null, undefined

    Note: This class is designed to be used as a mixin in the PythonCodeGenerator
    class hierarchy. It depends on ExpressionHelpersMixin being in the MRO.
    """

    def visit_literal(self, node: "Literal"):
        """Visit a generic literal node.

        Generic literal nodes are typically not used directly; instead, specific
        literal types (number, string, boolean, etc.) are used in the AST.

        Args:
            node: Generic Literal AST node

        Note:
            Actual code generation is handled by _generate_expression() in
            ExpressionHelpersMixin.
        """
        pass  # Handled by _generate_expression

    def visit_number_literal(self, node: "NumberLiteral"):
        """Visit a number literal node.

        Number literals include:
        - Integers: 42, -17, 0
        - Floats: 3.14, -0.5, 2.0
        - Scientific notation: 1e6, 2.5e-3, 6.022e23

        Args:
            node: NumberLiteral AST node with 'value' field

        Example:
            ML: 42
            Python: 42

            ML: 3.14
            Python: 3.14

            ML: 1.5e6
            Python: 1500000.0

        Note:
            Actual code generation is handled by _generate_expression() in
            ExpressionHelpersMixin.
        """
        pass  # Handled by _generate_expression

    def visit_string_literal(self, node: "StringLiteral"):
        """Visit a string literal node.

        String literals support:
        - Single quotes: 'hello'
        - Double quotes: "world"
        - Escape sequences: \n, \t, \\, \', \"
        - Unicode: \u0041, \U0001F600

        Args:
            node: StringLiteral AST node with 'value' field

        Example:
            ML: "hello world"
            Python: "hello world"

            ML: 'it\'s a test'
            Python: "it's a test"

        Note:
            Actual code generation is handled by _generate_expression() in
            ExpressionHelpersMixin. String escaping is handled there.
        """
        pass  # Handled by _generate_expression

    def visit_boolean_literal(self, node: "BooleanLiteral"):
        """Visit a boolean literal node.

        Boolean literals are ML keywords that map to Python booleans:
        - ML 'true' -> Python 'True'
        - ML 'false' -> Python 'False'

        Args:
            node: BooleanLiteral AST node with 'value' field (bool)

        Example:
            ML: true
            Python: True

            ML: false
            Python: False

        Note:
            Actual code generation is handled by _generate_expression() in
            ExpressionHelpersMixin.
        """
        pass  # Handled by _generate_expression

    def visit_array_literal(self, node: "ArrayLiteral"):
        """Visit an array literal node.

        Array literals create Python lists:
        - Empty arrays: []
        - Homogeneous: [1, 2, 3]
        - Heterogeneous: [1, "two", true, null]
        - Nested: [[1, 2], [3, 4]]
        - With expressions: [x + 1, y * 2]

        Args:
            node: ArrayLiteral AST node with 'elements' field (list of expressions)

        Example:
            ML: [1, 2, 3]
            Python: [1, 2, 3]

            ML: [x, y + 1, f(z)]
            Python: [x, y + 1, f(z)]

            ML: []
            Python: []

        Note:
            Actual code generation is handled by _generate_expression() in
            ExpressionHelpersMixin. Each element is recursively processed.
        """
        pass  # Handled by _generate_expression

    def visit_object_literal(self, node: "ObjectLiteral"):
        """Visit an object literal node.

        Object literals create Python dictionaries:
        - Empty objects: {}
        - String keys: {name: "Alice", age: 30}
        - Computed keys: {[key]: value}
        - Nested objects: {user: {name: "Bob"}}
        - With expressions: {x: a + b, y: f(c)}

        Args:
            node: ObjectLiteral AST node with 'properties' field (list of key-value pairs)

        Example:
            ML: {name: "Alice", age: 30}
            Python: {"name": "Alice", "age": 30}

            ML: {x: 1, y: x + 1}
            Python: {"x": 1, "y": x + 1}

            ML: {}
            Python: {}

        Note:
            Actual code generation is handled by _generate_expression() in
            ExpressionHelpersMixin. All keys are converted to strings, values
            are recursively processed.
        """
        pass  # Handled by _generate_expression
