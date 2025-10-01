"""Unit tests for the ML language parser."""

import pytest

from mlpy.ml.errors.exceptions import MLParseError, MLSyntaxError
from mlpy.ml.grammar.ast_nodes import *
from mlpy.ml.grammar.parser import MLParser, parse_ml_code


class TestMLParser:
    """Test the ML language parser."""

    def setup_method(self):
        """Set up test fixtures."""
        self.parser = MLParser()

    def test_empty_program(self):
        """Test parsing empty program."""
        result = self.parser.parse("")
        assert isinstance(result, Program)
        assert len(result.items) == 0

    def test_simple_assignment(self):
        """Test parsing simple assignment."""
        code = "x = 42;"
        result = self.parser.parse(code)

        assert isinstance(result, Program)
        assert len(result.items) == 1

        stmt = result.items[0]
        assert isinstance(stmt, AssignmentStatement)
        assert stmt.target.name == "x"
        assert isinstance(stmt.value, NumberLiteral)
        assert stmt.value.value == 42

    def test_function_definition(self):
        """Test parsing function definition."""
        code = """
        function add(a, b) {
            return a + b;
        }
        """
        result = self.parser.parse(code)

        assert isinstance(result, Program)
        assert len(result.items) == 1

        func = result.items[0]
        assert isinstance(func, FunctionDefinition)
        assert func.name.name == "add"
        assert len(func.parameters) == 2
        assert func.parameters[0].name == "a"
        assert func.parameters[1].name == "b"
        assert len(func.body) == 1

        return_stmt = func.body[0]
        assert isinstance(return_stmt, ReturnStatement)
        assert isinstance(return_stmt.value, BinaryExpression)

    def test_function_call(self):
        """Test parsing function call."""
        code = 'result = calculate(10, "test");'
        result = self.parser.parse(code)

        assert isinstance(result, Program)
        assert len(result.items) == 1

        stmt = result.items[0]
        assert isinstance(stmt, AssignmentStatement)
        assert isinstance(stmt.value, FunctionCall)
        assert stmt.value.function == "calculate"
        assert len(stmt.value.arguments) == 2

    def test_capability_declaration(self):
        """Test parsing capability declaration."""
        code = """
        capability FileAccess {
            resource "/tmp/*";
            allow read "/etc/config";
        }
        """
        result = self.parser.parse(code)

        assert isinstance(result, Program)
        assert len(result.items) == 1

        cap = result.items[0]
        assert isinstance(cap, CapabilityDeclaration)
        assert cap.name == "FileAccess"
        assert len(cap.items) == 2

        resource = cap.items[0]
        assert isinstance(resource, ResourcePattern)
        assert resource.pattern == "/tmp/*"

        permission = cap.items[1]
        assert isinstance(permission, PermissionGrant)
        assert permission.permission_type == "read"
        assert permission.target == "/etc/config"

    def test_import_statement(self):
        """Test parsing import statements."""
        code = "import math.functions as mathlib;"
        result = self.parser.parse(code)

        assert isinstance(result, Program)
        assert len(result.items) == 1

        import_stmt = result.items[0]
        assert isinstance(import_stmt, ImportStatement)
        assert import_stmt.target == ["math", "functions"]
        assert import_stmt.alias == "mathlib"

    def test_control_flow(self):
        """Test parsing control flow statements."""
        code = """
        if (x > 0) {
            y = x * 2;
        } else {
            y = 0;
        }

        while (i < 10) {
            i = i + 1;
        }

        for (item in items) {
            process(item);
        }
        """
        result = self.parser.parse(code)

        assert isinstance(result, Program)
        assert len(result.items) == 3

        # Test if statement
        if_stmt = result.items[0]
        assert isinstance(if_stmt, IfStatement)
        assert isinstance(if_stmt.condition, BinaryExpression)
        assert isinstance(if_stmt.then_statement, BlockStatement)
        assert isinstance(if_stmt.else_statement, BlockStatement)

        # Test while statement
        while_stmt = result.items[1]
        assert isinstance(while_stmt, WhileStatement)
        assert isinstance(while_stmt.condition, BinaryExpression)
        assert isinstance(while_stmt.body, BlockStatement)

        # Test for statement
        for_stmt = result.items[2]
        assert isinstance(for_stmt, ForStatement)
        assert for_stmt.variable.name == "item"
        assert isinstance(for_stmt.iterable, Identifier)
        assert isinstance(for_stmt.body, BlockStatement)

    def test_expressions(self):
        """Test parsing various expressions."""
        code = """
        a = 1 + 2 * 3;
        b = !flag && (x == y);
        c = obj.property;
        d = arr[index];
        e = func(arg1, arg2);
        """
        result = self.parser.parse(code)

        assert isinstance(result, Program)
        assert len(result.items) == 5

        # Binary arithmetic
        stmt_a = result.items[0]
        assert isinstance(stmt_a.value, BinaryExpression)

        # Logical operations
        stmt_b = result.items[1]
        assert isinstance(stmt_b.value, BinaryExpression)

        # Member access
        stmt_c = result.items[2]
        assert isinstance(stmt_c.value, MemberAccess)

        # Array access
        stmt_d = result.items[3]
        assert isinstance(stmt_d.value, ArrayAccess)

        # Function call
        stmt_e = result.items[4]
        assert isinstance(stmt_e.value, FunctionCall)

    def test_literals(self):
        """Test parsing different literal types."""
        code = """
        num = 42.5;
        str = "hello world";
        bool = true;
        arr = [1, 2, 3];
        obj = {"key": "value", "num": 42};
        """
        result = self.parser.parse(code)

        assert isinstance(result, Program)
        assert len(result.items) == 5

        # Number literal
        assert isinstance(result.items[0].value, NumberLiteral)
        assert result.items[0].value.value == 42.5

        # String literal
        assert isinstance(result.items[1].value, StringLiteral)
        assert result.items[1].value.value == "hello world"

        # Boolean literal
        assert isinstance(result.items[2].value, BooleanLiteral)
        assert result.items[2].value.value is True

        # Array literal
        assert isinstance(result.items[3].value, ArrayLiteral)
        assert len(result.items[3].value.elements) == 3

        # Object literal
        assert isinstance(result.items[4].value, ObjectLiteral)
        assert len(result.items[4].value.properties) == 2

    def test_syntax_errors(self):
        """Test handling of syntax errors."""
        with pytest.raises(MLSyntaxError):
            self.parser.parse("function incomplete(")

        with pytest.raises(MLSyntaxError):
            self.parser.parse("x = y +")

        with pytest.raises(MLSyntaxError):
            self.parser.parse("if (condition { missing_paren();")

    def test_parse_file_not_found(self):
        """Test error handling for non-existent file."""
        with pytest.raises(MLParseError):
            self.parser.parse_file("non_existent_file.ml")

    def test_comments_ignored(self):
        """Test that comments are properly ignored."""
        code = """
        // This is a comment
        x = 42; // End of line comment
        // Another comment
        """
        result = self.parser.parse(code)

        assert isinstance(result, Program)
        assert len(result.items) == 1
        assert isinstance(result.items[0], AssignmentStatement)

    def test_global_parse_functions(self):
        """Test global convenience functions."""
        code = "x = 42;"

        result = parse_ml_code(code)
        assert isinstance(result, Program)
        assert len(result.items) == 1

    def test_operator_precedence(self):
        """Test operator precedence is handled correctly."""
        code = "result = a + b * c == d && e || f;"
        result = self.parser.parse(code)

        assert isinstance(result, Program)
        stmt = result.items[0]
        assert isinstance(stmt, AssignmentStatement)

        # The expression should be parsed with correct precedence
        expr = stmt.value
        assert isinstance(expr, BinaryExpression)
        assert expr.operator == "||"

    def test_nested_structures(self):
        """Test parsing nested structures."""
        code = """
        function outer() {
            function inner(x) {
                if (x > 0) {
                    for (i in range) {
                        result[i] = process(data[i]);
                    }
                }
                return result;
            }
            return inner;
        }
        """
        result = self.parser.parse(code)

        assert isinstance(result, Program)
        assert len(result.items) == 1

        outer_func = result.items[0]
        assert isinstance(outer_func, FunctionDefinition)
        assert outer_func.name.name == "outer"

        # Check that nested structures are parsed correctly
        assert len(outer_func.body) == 2  # inner function + return statement
