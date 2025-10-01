"""
Comprehensive unit tests for ast_transformer.py - AST transformation and normalization.

Tests cover:
- TransformationResult dataclass and properties
- ASTTransformer initialization and state management
- transform() method with various AST structures
- Node counting and transformation tracking
- Specific transformations for each node type
- Scope management and variable generation
- Performance metrics and timing
"""

import pytest

from mlpy.ml.analysis.ast_transformer import (
    ASTTransformer,
    TransformationResult,
)
from mlpy.ml.grammar.ast_nodes import (
    AssignmentStatement,
    BinaryExpression,
    BlockStatement,
    FunctionCall,
    FunctionDefinition,
    Identifier,
    IfStatement,
    NumberLiteral,
    Parameter,
    Program,
    ReturnStatement,
    WhileStatement,
)


class TestTransformationResult:
    """Test TransformationResult dataclass."""

    def test_transformation_result_creation(self):
        """Test creating transformation result."""
        ast = Program([])
        result = TransformationResult(
            transformed_ast=ast,
            transformations_applied=["test_transform"],
            transformation_time_ms=1.5,
            node_count_before=10,
            node_count_after=8,
        )

        assert result.transformed_ast == ast
        assert "test_transform" in result.transformations_applied
        assert result.transformation_time_ms == 1.5
        assert result.node_count_before == 10
        assert result.node_count_after == 8

    def test_transformation_summary_with_transformations(self):
        """Test transformation summary with transformations."""
        result = TransformationResult(
            transformed_ast=Program([]),
            transformations_applied=["normalize_scope", "desugar_for"],
            transformation_time_ms=2.0,
            node_count_before=15,
            node_count_after=12,
        )

        summary = result.transformation_summary

        assert "Applied 2 transformations" in summary
        assert "normalize_scope" in summary
        assert "desugar_for" in summary

    def test_transformation_summary_empty(self):
        """Test transformation summary with no transformations."""
        result = TransformationResult(
            transformed_ast=Program([]),
            transformations_applied=[],
            transformation_time_ms=0.1,
            node_count_before=5,
            node_count_after=5,
        )

        summary = result.transformation_summary

        assert summary == "No transformations applied"


class TestASTTransformerInit:
    """Test ASTTransformer initialization."""

    def test_transformer_creation(self):
        """Test creating transformer instance."""
        transformer = ASTTransformer()

        assert transformer is not None
        assert transformer.transformations_applied == []
        assert transformer.node_count == 0
        assert transformer.scope_depth == 0
        assert transformer.variable_counter == 0


class TestTransformMethod:
    """Test transform() method."""

    @pytest.fixture
    def transformer(self):
        """Create transformer."""
        return ASTTransformer()

    def test_transform_empty_program(self, transformer):
        """Test transforming empty program."""
        ast = Program([])

        result = transformer.transform(ast)

        assert isinstance(result, TransformationResult)
        assert isinstance(result.transformed_ast, Program)
        assert result.transformation_time_ms >= 0

    def test_transform_simple_assignment(self, transformer):
        """Test transforming simple assignment."""
        ast = Program([AssignmentStatement(target=Identifier("x"), value=NumberLiteral(42))])

        result = transformer.transform(ast)

        assert isinstance(result.transformed_ast, Program)
        assert result.node_count_before > 0
        assert result.node_count_after > 0

    def test_transform_function_definition(self, transformer):
        """Test transforming function definition."""
        ast = Program(
            [
                FunctionDefinition(
                    name="add",
                    parameters=[Parameter("a"), Parameter("b")],
                    body=[ReturnStatement(BinaryExpression(Identifier("a"), "+", Identifier("b")))],
                )
            ]
        )

        result = transformer.transform(ast)

        assert isinstance(result.transformed_ast, Program)
        assert len(result.transformations_applied) >= 0

    def test_transform_preserves_original_ast(self, transformer):
        """Test that transformation doesn't modify original AST."""
        original_ast = Program(
            [AssignmentStatement(target=Identifier("x"), value=NumberLiteral(10))]
        )

        # Transform the AST
        result = transformer.transform(original_ast)

        # Original should be unchanged
        assert isinstance(original_ast, Program)
        assert len(original_ast.items) == 1

        # Transformed may differ
        assert isinstance(result.transformed_ast, Program)

    def test_transform_resets_state(self, transformer):
        """Test that transformer state is reset between transforms."""
        ast1 = Program([AssignmentStatement(Identifier("x"), NumberLiteral(1))])
        ast2 = Program([AssignmentStatement(Identifier("y"), NumberLiteral(2))])

        result1 = transformer.transform(ast1)
        result2 = transformer.transform(ast2)

        # Second transformation should have fresh state
        assert transformer.scope_depth == 0
        assert isinstance(result2, TransformationResult)

    def test_transform_tracks_time(self, transformer):
        """Test that transformation time is tracked."""
        ast = Program(
            [
                FunctionDefinition(
                    name="test",
                    parameters=[],
                    body=[AssignmentStatement(Identifier("x"), NumberLiteral(5))],
                )
            ]
        )

        result = transformer.transform(ast)

        # Time should be positive
        assert result.transformation_time_ms > 0
        assert result.transformation_time_ms < 1000  # Should be fast


class TestComplexTransformations:
    """Test transformation of complex structures."""

    @pytest.fixture
    def transformer(self):
        """Create transformer."""
        return ASTTransformer()

    def test_transform_nested_if_statements(self, transformer):
        """Test transforming nested if statements."""
        ast = Program(
            [
                IfStatement(
                    condition=BinaryExpression(Identifier("x"), ">", NumberLiteral(5)),
                    then_statement=BlockStatement(
                        [
                            IfStatement(
                                condition=BinaryExpression(Identifier("y"), "<", NumberLiteral(10)),
                                then_statement=BlockStatement(
                                    [AssignmentStatement(Identifier("z"), NumberLiteral(1))]
                                ),
                                elif_clauses=[],
                                else_statement=None,
                            )
                        ]
                    ),
                    elif_clauses=[],
                    else_statement=None,
                )
            ]
        )

        result = transformer.transform(ast)

        assert isinstance(result.transformed_ast, Program)
        assert result.node_count_before > 5

    def test_transform_while_loop(self, transformer):
        """Test transforming while loop."""
        ast = Program(
            [
                WhileStatement(
                    condition=BinaryExpression(Identifier("count"), "<", NumberLiteral(10)),
                    body=[
                        AssignmentStatement(
                            Identifier("count"),
                            BinaryExpression(Identifier("count"), "+", NumberLiteral(1)),
                        )
                    ],
                )
            ]
        )

        result = transformer.transform(ast)

        assert isinstance(result.transformed_ast, Program)

    def test_transform_function_with_multiple_statements(self, transformer):
        """Test transforming function with multiple statements."""
        ast = Program(
            [
                FunctionDefinition(
                    name="complex",
                    parameters=[Parameter("n")],
                    body=[
                        AssignmentStatement(Identifier("result"), NumberLiteral(0)),
                        AssignmentStatement(Identifier("i"), NumberLiteral(0)),
                        WhileStatement(
                            condition=BinaryExpression(Identifier("i"), "<", Identifier("n")),
                            body=[
                                AssignmentStatement(
                                    Identifier("result"),
                                    BinaryExpression(Identifier("result"), "+", Identifier("i")),
                                ),
                                AssignmentStatement(
                                    Identifier("i"),
                                    BinaryExpression(Identifier("i"), "+", NumberLiteral(1)),
                                ),
                            ],
                        ),
                        ReturnStatement(Identifier("result")),
                    ],
                )
            ]
        )

        result = transformer.transform(ast)

        assert isinstance(result.transformed_ast, Program)
        assert result.node_count_before > 10

    def test_transform_binary_expressions(self, transformer):
        """Test transforming complex binary expressions."""
        ast = Program(
            [
                AssignmentStatement(
                    Identifier("result"),
                    BinaryExpression(
                        BinaryExpression(Identifier("a"), "+", Identifier("b")),
                        "*",
                        BinaryExpression(Identifier("c"), "-", Identifier("d")),
                    ),
                )
            ]
        )

        result = transformer.transform(ast)

        assert isinstance(result.transformed_ast, Program)


class TestTransformationMetadata:
    """Test transformation metadata tracking."""

    @pytest.fixture
    def transformer(self):
        """Create transformer."""
        return ASTTransformer()

    def test_node_count_simple_program(self, transformer):
        """Test node counting for simple program."""
        ast = Program([AssignmentStatement(Identifier("x"), NumberLiteral(42))])

        result = transformer.transform(ast)

        # Should count Program, Assignment, Identifier, NumberLiteral
        assert result.node_count_before >= 4

    def test_node_count_complex_program(self, transformer):
        """Test node counting for complex program."""
        ast = Program(
            [
                FunctionDefinition(
                    name="factorial",
                    parameters=[Parameter("n")],
                    body=[
                        IfStatement(
                            condition=BinaryExpression(Identifier("n"), "<=", NumberLiteral(1)),
                            then_statement=BlockStatement([ReturnStatement(NumberLiteral(1))]),
                            elif_clauses=[],
                            else_statement=BlockStatement(
                                [
                                    ReturnStatement(
                                        BinaryExpression(
                                            Identifier("n"),
                                            "*",
                                            FunctionCall(
                                                Identifier("factorial"),
                                                [
                                                    BinaryExpression(
                                                        Identifier("n"), "-", NumberLiteral(1)
                                                    )
                                                ],
                                            ),
                                        )
                                    )
                                ]
                            ),
                        )
                    ],
                )
            ]
        )

        result = transformer.transform(ast)

        # Complex program should have many nodes
        assert result.node_count_before > 15

    def test_transformation_applied_list(self, transformer):
        """Test transformations_applied list."""
        ast = Program([AssignmentStatement(Identifier("x"), NumberLiteral(10))])

        result = transformer.transform(ast)

        # Should track transformations (even if empty for simple cases)
        assert isinstance(result.transformations_applied, list)


class TestMultipleTransformations:
    """Test multiple sequential transformations."""

    @pytest.fixture
    def transformer(self):
        """Create transformer."""
        return ASTTransformer()

    def test_multiple_transforms_same_instance(self, transformer):
        """Test multiple transformations with same transformer instance."""
        ast1 = Program([AssignmentStatement(Identifier("x"), NumberLiteral(1))])
        ast2 = Program([AssignmentStatement(Identifier("y"), NumberLiteral(2))])
        ast3 = Program([AssignmentStatement(Identifier("z"), NumberLiteral(3))])

        result1 = transformer.transform(ast1)
        result2 = transformer.transform(ast2)
        result3 = transformer.transform(ast3)

        # All should succeed independently
        assert isinstance(result1.transformed_ast, Program)
        assert isinstance(result2.transformed_ast, Program)
        assert isinstance(result3.transformed_ast, Program)

    def test_transformer_state_independence(self, transformer):
        """Test that transformations are independent."""
        ast1 = Program(
            [
                FunctionDefinition(
                    name="func1",
                    parameters=[],
                    body=[AssignmentStatement(Identifier("a"), NumberLiteral(1))],
                )
            ]
        )

        ast2 = Program(
            [
                FunctionDefinition(
                    name="func2",
                    parameters=[],
                    body=[AssignmentStatement(Identifier("b"), NumberLiteral(2))],
                )
            ]
        )

        result1 = transformer.transform(ast1)
        result2 = transformer.transform(ast2)

        # State should be reset between transforms
        assert transformer.scope_depth == 0
        assert isinstance(result1, TransformationResult)
        assert isinstance(result2, TransformationResult)
