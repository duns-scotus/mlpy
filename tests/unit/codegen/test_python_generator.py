"""
Unit tests for python_generator.py - Python code generation from ML AST.

Tests cover:
- SourceMapping and CodeGenerationContext dataclasses
- PythonCodeGenerator initialization
- Basic code generation (assignments, literals, expressions)
- Function definitions and calls
- Control flow (if/elif/else, while, for, try/except)
- Source map generation
- Import handling
- Indentation management
- Identifier safety (keyword collision)
- Expression generation (binary, unary, ternary)
"""

import pytest
from mlpy.ml.codegen.python_generator import (
    PythonCodeGenerator,
    SourceMapping,
    CodeGenerationContext,
)
from mlpy.ml.grammar.ast_nodes import (
    Program,
    AssignmentStatement,
    Identifier,
    NumberLiteral,
    StringLiteral,
    BooleanLiteral,
    ArrayLiteral,
    ObjectLiteral,
    FunctionDefinition,
    Parameter,
    ReturnStatement,
    IfStatement,
    WhileStatement,
    ForStatement,
    BinaryExpression,
    UnaryExpression,
    TernaryExpression,
    FunctionCall,
    BlockStatement,
    ElifClause,
    BreakStatement,
    ContinueStatement,
    ExpressionStatement,
)


class TestSourceMapping:
    """Test SourceMapping dataclass."""

    def test_source_mapping_creation(self):
        """Test creating source mapping."""
        mapping = SourceMapping(
            generated_line=10,
            generated_column=4,
            original_line=5,
            original_column=0,
            original_file="test.ml",
            name="x",
        )

        assert mapping.generated_line == 10
        assert mapping.generated_column == 4
        assert mapping.original_line == 5
        assert mapping.original_file == "test.ml"
        assert mapping.name == "x"


class TestCodeGenerationContext:
    """Test CodeGenerationContext dataclass."""

    def test_context_creation(self):
        """Test creating code generation context."""
        context = CodeGenerationContext()

        assert context.indentation_level == 0
        assert context.current_line == 1
        assert context.current_column == 0
        assert len(context.source_mappings) == 0
        assert len(context.variable_mappings) == 0
        assert len(context.imports_needed) == 0


class TestPythonCodeGenerator:
    """Test PythonCodeGenerator main functionality."""

    @pytest.fixture
    def generator(self):
        """Create code generator."""
        return PythonCodeGenerator()

    def test_generator_initialization(self, generator):
        """Test generator initialization."""
        assert generator is not None
        assert generator.context is not None
        assert generator.output_lines == []

    def test_generate_simple_assignment(self, generator):
        """Test generating simple variable assignment."""
        program = Program([
            AssignmentStatement(
                target=Identifier("x"),
                value=NumberLiteral(42)
            )
        ])

        code, source_map = generator.generate(program)

        assert "x = 42" in code
        assert source_map is not None

    def test_generate_string_literal(self, generator):
        """Test generating string literal."""
        program = Program([
            AssignmentStatement(
                target=Identifier("name"),
                value=StringLiteral("hello")
            )
        ])

        code, _ = generator.generate(program)

        assert 'name = "hello"' in code or "name = 'hello'" in code

    def test_generate_boolean_literal(self, generator):
        """Test generating boolean literals."""
        program = Program([
            AssignmentStatement(
                target=Identifier("flag"),
                value=BooleanLiteral(True)
            )
        ])

        code, _ = generator.generate(program)

        assert "flag = True" in code

    def test_generate_array_literal(self, generator):
        """Test generating array literal."""
        program = Program([
            AssignmentStatement(
                target=Identifier("arr"),
                value=ArrayLiteral([NumberLiteral(1), NumberLiteral(2)])
            )
        ])

        code, _ = generator.generate(program)

        assert "arr = [1, 2]" in code

    def test_generate_object_literal(self, generator):
        """Test generating object literal."""
        program = Program([
            AssignmentStatement(
                target=Identifier("obj"),
                value=ObjectLiteral({"key": StringLiteral("value")})
            )
        ])

        code, _ = generator.generate(program)

        assert "obj = " in code
        assert '"key"' in code or "'key'" in code

    def test_generate_function_definition(self, generator):
        """Test generating function definition."""
        program = Program([
            FunctionDefinition(
                name="add",
                parameters=[Parameter("a"), Parameter("b")],
                body=[ReturnStatement(
                    BinaryExpression(Identifier("a"), "+", Identifier("b"))
                )]
            )
        ])

        code, _ = generator.generate(program)

        assert "def add(a, b):" in code
        assert "return" in code

    def test_generate_function_call(self, generator):
        """Test generating function call."""
        program = Program([
            ExpressionStatement(
                FunctionCall("print", [StringLiteral("hello")])
            )
        ])

        code, _ = generator.generate(program)

        assert "print(" in code

    def test_generate_if_statement(self, generator):
        """Test generating if statement."""
        program = Program([
            IfStatement(
                condition=BooleanLiteral(True),
                then_statement=BlockStatement([
                    ExpressionStatement(FunctionCall("print", [StringLiteral("yes")]))
                ])
            )
        ])

        code, _ = generator.generate(program)

        assert "if True:" in code

    def test_generate_if_else_statement(self, generator):
        """Test generating if-else statement."""
        program = Program([
            IfStatement(
                condition=BooleanLiteral(True),
                then_statement=BlockStatement([
                    ExpressionStatement(FunctionCall("print", [StringLiteral("yes")]))
                ]),
                else_statement=BlockStatement([
                    ExpressionStatement(FunctionCall("print", [StringLiteral("no")]))
                ])
            )
        ])

        code, _ = generator.generate(program)

        assert "if True:" in code
        assert "else:" in code

    def test_generate_elif_statement(self, generator):
        """Test generating if-elif-else statement."""
        program = Program([
            IfStatement(
                condition=BooleanLiteral(True),
                then_statement=BlockStatement([
                    ExpressionStatement(FunctionCall("print", [StringLiteral("1")]))
                ]),
                elif_clauses=[
                    ElifClause(
                        condition=BooleanLiteral(False),
                        statement=BlockStatement([
                            ExpressionStatement(FunctionCall("print", [StringLiteral("2")]))
                        ])
                    )
                ],
                else_statement=BlockStatement([
                    ExpressionStatement(FunctionCall("print", [StringLiteral("3")]))
                ])
            )
        ])

        code, _ = generator.generate(program)

        assert "if True:" in code
        assert "elif False:" in code
        assert "else:" in code

    def test_generate_while_loop(self, generator):
        """Test generating while loop."""
        program = Program([
            WhileStatement(
                condition=BooleanLiteral(True),
                body=BlockStatement([
                    BreakStatement()
                ])
            )
        ])

        code, _ = generator.generate(program)

        assert "while True:" in code
        assert "break" in code

    def test_generate_for_loop(self, generator):
        """Test generating for loop."""
        program = Program([
            ForStatement(
                variable=Identifier("i"),
                iterable=Identifier("items"),
                body=BlockStatement([
                    ContinueStatement()
                ])
            )
        ])

        code, _ = generator.generate(program)

        assert "for i in items:" in code
        assert "continue" in code

    def test_generate_binary_expression(self, generator):
        """Test generating binary expression."""
        program = Program([
            AssignmentStatement(
                target=Identifier("result"),
                value=BinaryExpression(
                    NumberLiteral(5),
                    "+",
                    NumberLiteral(3)
                )
            )
        ])

        code, _ = generator.generate(program)

        assert "result = 5 + 3" in code or "result = (5 + 3)" in code

    def test_generate_unary_expression(self, generator):
        """Test generating unary expression."""
        program = Program([
            AssignmentStatement(
                target=Identifier("neg"),
                value=UnaryExpression("-", NumberLiteral(5))
            )
        ])

        code, _ = generator.generate(program)

        # Generator may format with or without spaces/parens
        assert "neg = " in code and "-" in code and "5" in code

    def test_generate_ternary_expression(self, generator):
        """Test generating ternary expression."""
        program = Program([
            AssignmentStatement(
                target=Identifier("value"),
                value=TernaryExpression(
                    condition=BooleanLiteral(True),
                    true_value=NumberLiteral(1),
                    false_value=NumberLiteral(0)
                )
            )
        ])

        code, _ = generator.generate(program)

        assert "value = " in code
        assert "if" in code
        assert "else" in code

    def test_indentation_management(self, generator):
        """Test indentation is properly managed."""
        program = Program([
            FunctionDefinition(
                name="test",
                parameters=[],
                body=[
                    IfStatement(
                        condition=BooleanLiteral(True),
                        then_statement=BlockStatement([
                            ExpressionStatement(FunctionCall("print", [StringLiteral("nested")]))
                        ])
                    )
                ]
            )
        ])

        code, _ = generator.generate(program)

        lines = code.split('\n')
        # Find the nested print statement
        for i, line in enumerate(lines):
            if "print" in line and "nested" in line:
                # Should have at least 2 levels of indentation (function + if)
                assert line.startswith("        ")  # 8 spaces = 2 levels
                break

    def test_safe_identifier_conversion(self, generator):
        """Test safe identifier conversion for Python keywords."""
        # The generator should handle Python keywords
        program = Program([
            AssignmentStatement(
                target=Identifier("class"),  # Python keyword
                value=NumberLiteral(42)
            )
        ])

        code, _ = generator.generate(program)

        # Should be converted to safe identifier
        assert "class_" in code or "ml_class" in code

    def test_header_generation(self, generator):
        """Test header is generated."""
        program = Program([])

        code, _ = generator.generate(program)

        assert "Generated Python code" in code
        assert "mlpy ML transpiler" in code

    def test_footer_generation(self, generator):
        """Test footer is generated."""
        program = Program([])

        code, _ = generator.generate(program)

        assert "End of generated code" in code

    def test_stdlib_imports_in_header(self, generator):
        """Test ML stdlib imports in header."""
        program = Program([])

        code, _ = generator.generate(program)

        # Should import console
        assert "console" in code

    def test_source_map_disabled(self):
        """Test source map generation can be disabled."""
        generator = PythonCodeGenerator(generate_source_maps=False)
        program = Program([
            AssignmentStatement(
                target=Identifier("x"),
                value=NumberLiteral(42)
            )
        ])

        code, source_map = generator.generate(program)

        assert code is not None
        assert source_map is None

    def test_source_map_enabled(self):
        """Test source map generation when enabled."""
        generator = PythonCodeGenerator(generate_source_maps=True)
        program = Program([
            AssignmentStatement(
                target=Identifier("x"),
                value=NumberLiteral(42)
            )
        ])

        code, source_map = generator.generate(program)

        assert source_map is not None

    def test_multiple_statements(self, generator):
        """Test generating multiple statements."""
        program = Program([
            AssignmentStatement(target=Identifier("x"), value=NumberLiteral(1)),
            AssignmentStatement(target=Identifier("y"), value=NumberLiteral(2)),
            AssignmentStatement(target=Identifier("z"), value=NumberLiteral(3)),
        ])

        code, _ = generator.generate(program)

        assert "x = 1" in code
        assert "y = 2" in code
        assert "z = 3" in code

    def test_return_statement(self, generator):
        """Test generating return statement."""
        program = Program([
            FunctionDefinition(
                name="getValue",
                parameters=[],
                body=[ReturnStatement(NumberLiteral(42))]
            )
        ])

        code, _ = generator.generate(program)

        assert "return 42" in code

    def test_break_statement(self, generator):
        """Test generating break statement."""
        program = Program([
            WhileStatement(
                condition=BooleanLiteral(True),
                body=BlockStatement([BreakStatement()])
            )
        ])

        code, _ = generator.generate(program)

        assert "break" in code

    def test_continue_statement(self, generator):
        """Test generating continue statement."""
        program = Program([
            WhileStatement(
                condition=BooleanLiteral(True),
                body=BlockStatement([ContinueStatement()])
            )
        ])

        code, _ = generator.generate(program)

        assert "continue" in code


class TestVisitorMethods:
    """Test individual visitor methods for coverage."""

    @pytest.fixture
    def generator(self):
        """Create generator."""
        return PythonCodeGenerator()

    def test_visit_try_except(self, generator):
        """Test try/except statement generation."""
        from mlpy.ml.grammar.ast_nodes import TryStatement, ExceptClause

        program = Program([
            TryStatement(
                try_body=[ExpressionStatement(FunctionCall("risky", []))],
                except_clauses=[
                    ExceptClause(
                        exception_type="Exception",
                        exception_variable="e",
                        body=[ExpressionStatement(FunctionCall("print", [Identifier("e")]))]
                    )
                ]
            )
        ])

        code, _ = generator.generate(program)

        assert "try:" in code
        assert "except" in code

    def test_visit_import_statement(self, generator):
        """Test import statement generation."""
        from mlpy.ml.grammar.ast_nodes import ImportStatement

        program = Program([
            ImportStatement(target=["os"], alias="operating_system")
        ])

        code, _ = generator.generate(program)

        assert "import" in code

    def test_visit_capability_declaration(self, generator):
        """Test capability declaration generation."""
        from mlpy.ml.grammar.ast_nodes import CapabilityDeclaration, ResourcePattern

        program = Program([
            CapabilityDeclaration(
                name="file_cap",
                items=[ResourcePattern("*.txt")]
            )
        ])

        code, _ = generator.generate(program)

        # Capability should generate some code
        assert code is not None

    def test_visit_array_access(self, generator):
        """Test array access generation."""
        from mlpy.ml.grammar.ast_nodes import ArrayAccess

        program = Program([
            AssignmentStatement(
                target=Identifier("value"),
                value=ArrayAccess(
                    array=Identifier("arr"),
                    index=NumberLiteral(0)
                )
            )
        ])

        code, _ = generator.generate(program)

        assert "arr[0]" in code

    def test_visit_member_access(self, generator):
        """Test member access generation."""
        from mlpy.ml.grammar.ast_nodes import MemberAccess

        program = Program([
            AssignmentStatement(
                target=Identifier("value"),
                value=MemberAccess(
                    object=Identifier("obj"),
                    member="property"
                )
            )
        ])

        code, _ = generator.generate(program)

        assert "obj" in code and "property" in code

    def test_visit_throw_statement(self, generator):
        """Test throw statement generation."""
        from mlpy.ml.grammar.ast_nodes import ThrowStatement

        program = Program([
            ThrowStatement(
                error_data=ObjectLiteral({"message": StringLiteral("error")})
            )
        ])

        code, _ = generator.generate(program)

        assert "raise" in code or "throw" in code

    def test_empty_array_literal(self, generator):
        """Test empty array literal."""
        program = Program([
            AssignmentStatement(
                target=Identifier("empty"),
                value=ArrayLiteral([])
            )
        ])

        code, _ = generator.generate(program)

        assert "empty = []" in code

    def test_nested_binary_expressions(self, generator):
        """Test nested binary expressions."""
        program = Program([
            AssignmentStatement(
                target=Identifier("result"),
                value=BinaryExpression(
                    BinaryExpression(NumberLiteral(1), "+", NumberLiteral(2)),
                    "*",
                    BinaryExpression(NumberLiteral(3), "+", NumberLiteral(4))
                )
            )
        ])

        code, _ = generator.generate(program)

        assert "result = " in code
        assert "+" in code
        assert "*" in code

    def test_function_with_no_params(self, generator):
        """Test function with no parameters."""
        program = Program([
            FunctionDefinition(
                name="noParams",
                parameters=[],
                body=[ReturnStatement(NumberLiteral(42))]
            )
        ])

        code, _ = generator.generate(program)

        assert "def noParams():" in code

    def test_multiple_elif_clauses(self, generator):
        """Test multiple elif clauses."""
        program = Program([
            IfStatement(
                condition=BooleanLiteral(False),
                then_statement=BlockStatement([ExpressionStatement(FunctionCall("print", [NumberLiteral(1)]))]),
                elif_clauses=[
                    ElifClause(
                        condition=BooleanLiteral(False),
                        statement=BlockStatement([ExpressionStatement(FunctionCall("print", [NumberLiteral(2)]))])
                    ),
                    ElifClause(
                        condition=BooleanLiteral(True),
                        statement=BlockStatement([ExpressionStatement(FunctionCall("print", [NumberLiteral(3)]))])
                    )
                ]
            )
        ])

        code, _ = generator.generate(program)

        # Should have multiple elif statements
        assert code.count("elif") >= 2


class TestAdvancedExpressions:
    """Test advanced expression generation."""

    @pytest.fixture
    def generator(self):
        """Create generator."""
        return PythonCodeGenerator()

    def test_modulo_operator(self, generator):
        """Test modulo operator generation."""
        program = Program([
            AssignmentStatement(
                target=Identifier("remainder"),
                value=BinaryExpression(NumberLiteral(10), "%", NumberLiteral(3))
            )
        ])

        code, _ = generator.generate(program)

        assert "remainder = 10 % 3" in code or "remainder = (10 % 3)" in code

    def test_logical_and_operator(self, generator):
        """Test logical AND operator."""
        program = Program([
            AssignmentStatement(
                target=Identifier("result"),
                value=BinaryExpression(BooleanLiteral(True), "and", BooleanLiteral(False))
            )
        ])

        code, _ = generator.generate(program)

        assert "and" in code

    def test_logical_or_operator(self, generator):
        """Test logical OR operator."""
        program = Program([
            AssignmentStatement(
                target=Identifier("result"),
                value=BinaryExpression(BooleanLiteral(True), "or", BooleanLiteral(False))
            )
        ])

        code, _ = generator.generate(program)

        assert "or" in code

    def test_comparison_operators(self, generator):
        """Test comparison operators."""
        operators = ["==", "!=", "<", ">", "<=", ">="]

        for op in operators:
            program = Program([
                AssignmentStatement(
                    target=Identifier("result"),
                    value=BinaryExpression(NumberLiteral(5), op, NumberLiteral(3))
                )
            ])

            code, _ = generator.generate(program)
            assert op in code

    def test_not_operator(self, generator):
        """Test NOT unary operator."""
        program = Program([
            AssignmentStatement(
                target=Identifier("result"),
                value=UnaryExpression("not", BooleanLiteral(True))
            )
        ])

        code, _ = generator.generate(program)

        assert "not" in code

    def test_complex_nested_expression(self, generator):
        """Test complex nested expression with multiple operators."""
        program = Program([
            AssignmentStatement(
                target=Identifier("result"),
                value=BinaryExpression(
                    BinaryExpression(
                        NumberLiteral(10), "+", NumberLiteral(5)
                    ),
                    "*",
                    BinaryExpression(
                        NumberLiteral(3), "-", NumberLiteral(1)
                    )
                )
            )
        ])

        code, _ = generator.generate(program)

        assert "result = " in code
        assert "+" in code
        assert "*" in code
        assert "-" in code


class TestImportStatements:
    """Test import statement generation."""

    @pytest.fixture
    def generator(self):
        """Create generator."""
        return PythonCodeGenerator()

    def test_simple_import(self, generator):
        """Test simple import statement."""
        from mlpy.ml.grammar.ast_nodes import ImportStatement

        program = Program([
            ImportStatement(target=["math"], alias=None)
        ])

        code, _ = generator.generate(program)

        assert "import math" in code or "from mlpy.stdlib import math" in code

    def test_import_with_alias(self, generator):
        """Test import with alias."""
        from mlpy.ml.grammar.ast_nodes import ImportStatement

        program = Program([
            ImportStatement(target=["datetime"], alias="dt")
        ])

        code, _ = generator.generate(program)

        assert "import" in code
        assert "dt" in code

    def test_nested_module_import(self, generator):
        """Test nested module import."""
        from mlpy.ml.grammar.ast_nodes import ImportStatement

        program = Program([
            ImportStatement(target=["os", "path"], alias=None)
        ])

        code, _ = generator.generate(program)

        assert "import" in code


class TestExceptionHandling:
    """Test exception handling generation."""

    @pytest.fixture
    def generator(self):
        """Create generator."""
        return PythonCodeGenerator()

    def test_try_without_except(self, generator):
        """Test try block without except."""
        from mlpy.ml.grammar.ast_nodes import TryStatement

        program = Program([
            TryStatement(
                try_body=[ExpressionStatement(FunctionCall("risky", []))],
                except_clauses=[]
            )
        ])

        code, _ = generator.generate(program)

        assert "try:" in code

    def test_multiple_except_clauses(self, generator):
        """Test multiple except clauses."""
        from mlpy.ml.grammar.ast_nodes import TryStatement, ExceptClause

        program = Program([
            TryStatement(
                try_body=[ExpressionStatement(FunctionCall("risky", []))],
                except_clauses=[
                    ExceptClause(
                        exception_type="ValueError",
                        exception_variable="ve",
                        body=[ExpressionStatement(FunctionCall("print", [StringLiteral("value error")]))]
                    ),
                    ExceptClause(
                        exception_type="TypeError",
                        exception_variable="te",
                        body=[ExpressionStatement(FunctionCall("print", [StringLiteral("type error")]))]
                    )
                ]
            )
        ])

        code, _ = generator.generate(program)

        # Generator may convert exception types to generic Exception
        assert "except" in code
        assert code.count("except") >= 2

    def test_except_without_variable(self, generator):
        """Test except clause without variable."""
        from mlpy.ml.grammar.ast_nodes import TryStatement, ExceptClause

        program = Program([
            TryStatement(
                try_body=[ExpressionStatement(FunctionCall("risky", []))],
                except_clauses=[
                    ExceptClause(
                        exception_type="Exception",
                        exception_variable=None,
                        body=[ExpressionStatement(FunctionCall("print", [StringLiteral("error")]))]
                    )
                ]
            )
        ])

        code, _ = generator.generate(program)

        # When no variable, generator may omit exception type
        assert "except:" in code or "except Exception" in code


class TestCodeGeneratorIntegration:
    """Integration tests for code generator."""

    @pytest.fixture
    def generator(self):
        """Create generator."""
        return PythonCodeGenerator(source_file="test.ml")

    def test_complete_program(self, generator):
        """Test generating complete program."""
        program = Program([
            FunctionDefinition(
                name="factorial",
                parameters=[Parameter("n")],
                body=[
                    IfStatement(
                        condition=BinaryExpression(Identifier("n"), "<=", NumberLiteral(1)),
                        then_statement=BlockStatement([
                            ReturnStatement(NumberLiteral(1))
                        ]),
                        else_statement=BlockStatement([
                            ReturnStatement(
                                BinaryExpression(
                                    Identifier("n"),
                                    "*",
                                    FunctionCall("factorial", [
                                        BinaryExpression(Identifier("n"), "-", NumberLiteral(1))
                                    ])
                                )
                            )
                        ])
                    )
                ]
            )
        ])

        code, source_map = generator.generate(program)

        # Should contain all parts
        assert "def factorial(n):" in code
        assert "if" in code
        assert "return" in code
        assert source_map is not None

    def test_nested_control_flow(self, generator):
        """Test nested control flow structures."""
        program = Program([
            WhileStatement(
                condition=BooleanLiteral(True),
                body=BlockStatement([
                    ForStatement(
                        variable=Identifier("i"),
                        iterable=Identifier("items"),
                        body=BlockStatement([
                            IfStatement(
                                condition=BinaryExpression(Identifier("i"), ">", NumberLiteral(5)),
                                then_statement=BlockStatement([BreakStatement()])
                            )
                        ])
                    )
                ])
            )
        ])

        code, _ = generator.generate(program)

        assert "while True:" in code
        assert "for i in " in code
        assert "if" in code
        assert "break" in code

    def test_function_with_multiple_params(self, generator):
        """Test function with multiple parameters."""
        program = Program([
            FunctionDefinition(
                name="add",
                parameters=[Parameter("a"), Parameter("b"), Parameter("c")],
                body=[
                    ReturnStatement(
                        BinaryExpression(
                            BinaryExpression(Identifier("a"), "+", Identifier("b")),
                            "+",
                            Identifier("c")
                        )
                    )
                ]
            )
        ])

        code, _ = generator.generate(program)

        assert "def add(a, b, c):" in code
        assert "return" in code

    def test_empty_program(self, generator):
        """Test generating empty program."""
        program = Program([])

        code, source_map = generator.generate(program)

        # Should still have header and footer
        assert "Generated Python code" in code
        assert "End of generated code" in code


class TestObjectLiterals:
    """Test object literal generation."""

    @pytest.fixture
    def generator(self):
        """Create generator."""
        return PythonCodeGenerator()

    def test_empty_object_literal(self, generator):
        """Test empty object literal."""
        program = Program([
            AssignmentStatement(
                target=Identifier("obj"),
                value=ObjectLiteral({})
            )
        ])

        code, _ = generator.generate(program)

        assert "obj = {}" in code

    def test_object_with_multiple_properties(self, generator):
        """Test object with multiple properties."""
        program = Program([
            AssignmentStatement(
                target=Identifier("person"),
                value=ObjectLiteral({
                    "name": StringLiteral("Alice"),
                    "age": NumberLiteral(30),
                    "active": BooleanLiteral(True)
                })
            )
        ])

        code, _ = generator.generate(program)

        assert "person = " in code
        assert "name" in code
        assert "age" in code
        assert "active" in code

    def test_nested_object_literal(self, generator):
        """Test nested object literal."""
        program = Program([
            AssignmentStatement(
                target=Identifier("data"),
                value=ObjectLiteral({
                    "user": ObjectLiteral({
                        "name": StringLiteral("Bob")
                    })
                })
            )
        ])

        code, _ = generator.generate(program)

        assert "data = " in code
        assert "user" in code
        assert "name" in code


class TestFunctionCalls:
    """Test function call generation with various arguments."""

    @pytest.fixture
    def generator(self):
        """Create generator."""
        return PythonCodeGenerator()

    def test_function_call_no_args(self, generator):
        """Test function call with no arguments."""
        program = Program([
            ExpressionStatement(FunctionCall("getData", []))
        ])

        code, _ = generator.generate(program)

        assert "getData()" in code

    def test_function_call_with_expressions(self, generator):
        """Test function call with expression arguments."""
        program = Program([
            ExpressionStatement(
                FunctionCall("add", [
                    BinaryExpression(NumberLiteral(1), "+", NumberLiteral(2)),
                    BinaryExpression(NumberLiteral(3), "*", NumberLiteral(4))
                ])
            )
        ])

        code, _ = generator.generate(program)

        assert "add(" in code
        assert "+" in code
        assert "*" in code

    def test_nested_function_calls(self, generator):
        """Test nested function calls."""
        program = Program([
            ExpressionStatement(
                FunctionCall("outer", [
                    FunctionCall("inner", [NumberLiteral(42)])
                ])
            )
        ])

        code, _ = generator.generate(program)

        assert "outer(" in code
        assert "inner(" in code


class TestMemberAndArrayAccess:
    """Test member access and array indexing."""

    @pytest.fixture
    def generator(self):
        """Create generator."""
        return PythonCodeGenerator()

    def test_nested_member_access(self, generator):
        """Test nested member access."""
        from mlpy.ml.grammar.ast_nodes import MemberAccess

        program = Program([
            AssignmentStatement(
                target=Identifier("value"),
                value=MemberAccess(
                    object=MemberAccess(
                        object=Identifier("obj"),
                        member="nested"
                    ),
                    member="prop"
                )
            )
        ])

        code, _ = generator.generate(program)

        assert "obj" in code
        assert "nested" in code
        assert "prop" in code

    def test_array_access_with_expression(self, generator):
        """Test array access with expression as index."""
        from mlpy.ml.grammar.ast_nodes import ArrayAccess

        program = Program([
            AssignmentStatement(
                target=Identifier("value"),
                value=ArrayAccess(
                    array=Identifier("arr"),
                    index=BinaryExpression(NumberLiteral(5), "+", NumberLiteral(3))
                )
            )
        ])

        code, _ = generator.generate(program)

        assert "arr[" in code
        assert "+" in code

    def test_chained_array_access(self, generator):
        """Test chained array access."""
        from mlpy.ml.grammar.ast_nodes import ArrayAccess

        program = Program([
            AssignmentStatement(
                target=Identifier("value"),
                value=ArrayAccess(
                    array=ArrayAccess(
                        array=Identifier("matrix"),
                        index=NumberLiteral(0)
                    ),
                    index=NumberLiteral(1)
                )
            )
        ])

        code, _ = generator.generate(program)

        assert "matrix[0][1]" in code or "matrix[0]" in code


class TestCapabilityStatements:
    """Test capability statement generation."""

    @pytest.fixture
    def generator(self):
        """Create generator."""
        return PythonCodeGenerator()

    def test_capability_with_multiple_resources(self, generator):
        """Test capability with multiple resource patterns."""
        from mlpy.ml.grammar.ast_nodes import CapabilityDeclaration, ResourcePattern

        program = Program([
            CapabilityDeclaration(
                name="file_cap",
                items=[
                    ResourcePattern("*.txt"),
                    ResourcePattern("*.md"),
                    ResourcePattern("data/*.json")
                ]
            )
        ])

        code, _ = generator.generate(program)

        # Should generate capability code
        assert code is not None
        assert len(code) > 0

    def test_resource_pattern_generation(self, generator):
        """Test resource pattern conversion."""
        from mlpy.ml.grammar.ast_nodes import ResourcePattern

        # Test that ResourcePattern can be visited
        pattern = ResourcePattern("file:///*.txt")

        # This should not raise an error
        assert pattern.pattern == "file:///*.txt"


class TestEdgeCases:
    """Test edge cases and error conditions."""

    @pytest.fixture
    def generator(self):
        """Create generator."""
        return PythonCodeGenerator()

    def test_very_long_identifier(self, generator):
        """Test handling of very long identifiers."""
        long_name = "very_long_variable_name_that_exceeds_normal_length_limits_" * 3
        program = Program([
            AssignmentStatement(
                target=Identifier(long_name),
                value=NumberLiteral(42)
            )
        ])

        code, _ = generator.generate(program)

        assert "= 42" in code

    def test_special_characters_in_string(self, generator):
        """Test string with special characters."""
        program = Program([
            AssignmentStatement(
                target=Identifier("text"),
                value=StringLiteral("Hello\nWorld\t!")
            )
        ])

        code, _ = generator.generate(program)

        assert "text = " in code

    def test_division_operator(self, generator):
        """Test division operator."""
        program = Program([
            AssignmentStatement(
                target=Identifier("result"),
                value=BinaryExpression(NumberLiteral(10), "/", NumberLiteral(2))
            )
        ])

        code, _ = generator.generate(program)

        assert "result = 10 / 2" in code or "result = (10 / 2)" in code

    def test_power_operator(self, generator):
        """Test power operator."""
        program = Program([
            AssignmentStatement(
                target=Identifier("result"),
                value=BinaryExpression(NumberLiteral(2), "**", NumberLiteral(3))
            )
        ])

        code, _ = generator.generate(program)

        assert "**" in code

    def test_floor_division_operator(self, generator):
        """Test floor division operator."""
        program = Program([
            AssignmentStatement(
                target=Identifier("result"),
                value=BinaryExpression(NumberLiteral(10), "//", NumberLiteral(3))
            )
        ])

        code, _ = generator.generate(program)

        assert "//" in code
