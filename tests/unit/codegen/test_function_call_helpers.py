"""
Unit tests for function_call_helpers.py - Function call and lambda generation.

Tests cover:
- Lambda generation from function definitions
- Variable substitution in lambda bodies
- Function call wrapping and security validation
- Simple and member function calls
- Direct vs wrapped call decision logic
- Error handling for unknown functions
"""

import pytest
from unittest.mock import Mock, patch, MagicMock

from mlpy.ml.codegen.helpers.function_call_helpers import FunctionCallHelpersMixin
from mlpy.ml.grammar.ast_nodes import (
    FunctionDefinition,
    FunctionCall,
    ReturnStatement,
    AssignmentStatement,
    Identifier,
    Parameter,
    NumberLiteral,
    StringLiteral,
    BinaryExpression,
    MemberAccess,
    BlockStatement,
    ArrayAccess,
    UnaryExpression,
)


# Create a concrete test class that implements FunctionCallHelpersMixin
class TestFunctionCallHelper(FunctionCallHelpersMixin):
    """Test implementation of FunctionCallHelpersMixin."""

    def __init__(self):
        self.symbol_table = {
            'parameters': [],
            'variables': set(),
            'functions': set(),
            'imports': {'builtin'},
            'ml_builtins': {'print', 'len', 'typeof'}
        }
        self.function_registry = Mock()
        self.function_registry.is_allowed.return_value = True
        self.function_registry.is_allowed_builtin.return_value = False
        self.function_registry.is_user_defined.return_value = False
        self.function_registry.get_all_allowed_functions.return_value = []
        self.function_registry.get_call_category.return_value = "unknown"
        self.function_registry.get_module_functions.return_value = []
        self.function_registry.imported_modules = {}
        self.context = Mock()
        self.context.builtin_functions_used = set()
        self.output_lines = []

    def _generate_expression(self, expr):
        """Mock expression generation."""
        if isinstance(expr, Identifier):
            return expr.name
        elif isinstance(expr, NumberLiteral):
            return str(expr.value)
        elif isinstance(expr, StringLiteral):
            return f'"{expr.value}"'
        elif isinstance(expr, BinaryExpression):
            left = self._generate_expression(expr.left)
            right = self._generate_expression(expr.right)
            return f"({left} {expr.operator} {right})"
        elif isinstance(expr, UnaryExpression):
            operand = self._generate_expression(expr.operand)
            return f"{expr.operator}{operand}"
        elif isinstance(expr, FunctionCall):
            func_name = expr.function.name if hasattr(expr.function, 'name') else str(expr.function)
            args = ', '.join(self._generate_expression(arg) for arg in expr.arguments)
            return f"{func_name}({args})"
        elif isinstance(expr, MemberAccess):
            obj = self._generate_expression(expr.object)
            return f"{obj}.{expr.member}"
        else:
            return "expr"

    def _safe_identifier(self, name: str) -> str:
        """Mock safe identifier conversion."""
        return name

    def _emit_line(self, line: str):
        """Mock emit line."""
        self.output_lines.append(line)


class TestGenerateLambdaFromFunctionDef:
    """Test _generate_lambda_from_function_def method."""

    def test_lambda_single_return_statement(self):
        """Test lambda generation from single return statement."""
        helper = TestFunctionCallHelper()

        # function(x) { return x + 1; }
        func_def = FunctionDefinition(
            name=Identifier("temp", line=1, column=0),
            parameters=[Parameter("x", line=1, column=9)],
            body=[
                ReturnStatement(
                    value=BinaryExpression(
                        left=Identifier("x", line=1, column=18),
                        operator="+",
                        right=NumberLiteral(1, line=1, column=22),
                        line=1, column=20
                    ),
                    line=1, column=11
                )
            ],
            line=1, column=0
        )

        result = helper._generate_lambda_from_function_def(func_def)

        assert result == "lambda x: (x + 1)"

    def test_lambda_multiple_parameters(self):
        """Test lambda generation with multiple parameters."""
        helper = TestFunctionCallHelper()

        # function(a, b, c) { return a + b + c; }
        func_def = FunctionDefinition(
            name=Identifier("temp", line=1, column=0),
            parameters=[
                Parameter("a", line=1, column=9),
                Parameter("b", line=1, column=12),
                Parameter("c", line=1, column=15)
            ],
            body=[
                ReturnStatement(
                    value=BinaryExpression(
                        left=BinaryExpression(
                            left=Identifier("a", line=1, column=26),
                            operator="+",
                            right=Identifier("b", line=1, column=30),
                            line=1, column=28
                        ),
                        operator="+",
                        right=Identifier("c", line=1, column=34),
                        line=1, column=32
                    ),
                    line=1, column=19
                )
            ],
            line=1, column=0
        )

        result = helper._generate_lambda_from_function_def(func_def)

        assert result == "lambda a, b, c: ((a + b) + c)"

    def test_lambda_no_parameters(self):
        """Test lambda generation with no parameters."""
        helper = TestFunctionCallHelper()

        # function() { return 42; }
        func_def = FunctionDefinition(
            name=Identifier("temp", line=1, column=0),
            parameters=[],
            body=[
                ReturnStatement(
                    value=NumberLiteral(42, line=1, column=20),
                    line=1, column=13
                )
            ],
            line=1, column=0
        )

        result = helper._generate_lambda_from_function_def(func_def)

        assert result == "lambda : 42"

    def test_lambda_no_return_statement(self):
        """Test lambda generation when no return statement exists."""
        helper = TestFunctionCallHelper()

        # function(x) { }  (empty body, no return)
        func_def = FunctionDefinition(
            name=Identifier("temp", line=1, column=0),
            parameters=[Parameter("x", line=1, column=9)],
            body=[],
            line=1, column=0
        )

        result = helper._generate_lambda_from_function_def(func_def)

        assert result == "lambda x: None"

    def test_lambda_with_variable_substitution(self):
        """Test lambda generation with variable substitution."""
        helper = TestFunctionCallHelper()

        # function(x) { let doubled = x * 2; return doubled; }
        func_def = FunctionDefinition(
            name=Identifier("temp", line=1, column=0),
            parameters=[Parameter("x", line=1, column=9)],
            body=[
                AssignmentStatement(
                    target=Identifier("doubled", line=1, column=15),
                    value=BinaryExpression(
                        left=Identifier("x", line=1, column=25),
                        operator="*",
                        right=NumberLiteral(2, line=1, column=29),
                        line=1, column=27
                    ),
                    line=1, column=15
                ),
                ReturnStatement(
                    value=Identifier("doubled", line=1, column=40),
                    line=1, column=33
                )
            ],
            line=1, column=0
        )

        result = helper._generate_lambda_from_function_def(func_def)

        # Should substitute 'doubled' with 'x * 2'
        assert "lambda x:" in result
        assert "x" in result and "2" in result


class TestSubstituteVariablesInLambda:
    """Test _substitute_variables_in_lambda method."""

    def test_substitute_simple_variable(self):
        """Test substituting a simple variable."""
        helper = TestFunctionCallHelper()

        statements = [
            AssignmentStatement(
                target=Identifier("y", line=1, column=0),
                value=NumberLiteral(10, line=1, column=4),
                line=1, column=0
            )
        ]
        return_expr = Identifier("y", line=2, column=7)
        params = []

        result = helper._substitute_variables_in_lambda(statements, return_expr, params)

        assert result == "10"

    def test_substitute_with_parameter(self):
        """Test that parameters are not substituted."""
        helper = TestFunctionCallHelper()

        statements = [
            AssignmentStatement(
                target=Identifier("y", line=1, column=0),
                value=Identifier("x", line=1, column=4),
                line=1, column=0
            )
        ]
        return_expr = Identifier("y", line=2, column=7)
        params = ["x"]

        result = helper._substitute_variables_in_lambda(statements, return_expr, params)

        # Should substitute y with x, but x is a parameter so keep it
        assert result == "x"

    def test_substitute_fails_gracefully(self):
        """Test that substitution failures return None."""
        helper = TestFunctionCallHelper()

        statements = []
        return_expr = Identifier("unknown", line=1, column=0)
        params = []

        # Mock _substitute_expression to raise exception
        with patch.object(helper, '_substitute_expression', side_effect=Exception("Test error")):
            result = helper._substitute_variables_in_lambda(statements, return_expr, params)

        assert result is None


class TestSubstituteExpression:
    """Test _substitute_expression method."""

    def test_substitute_identifier_with_assignment(self):
        """Test substituting identifier with its assigned value."""
        helper = TestFunctionCallHelper()

        expr = Identifier("x", line=1, column=0)
        assignments = {"x": NumberLiteral(42, line=1, column=0)}
        param_names = set()

        result = helper._substitute_expression(expr, assignments, param_names, depth=0)

        assert isinstance(result, NumberLiteral)
        assert result.value == 42

    def test_substitute_identifier_parameter(self):
        """Test that parameter identifiers are not substituted."""
        helper = TestFunctionCallHelper()

        expr = Identifier("x", line=1, column=0)
        assignments = {"x": NumberLiteral(42, line=1, column=0)}
        param_names = {"x"}

        result = helper._substitute_expression(expr, assignments, param_names, depth=0)

        # Should return original identifier since it's a parameter
        assert isinstance(result, Identifier)
        assert result.name == "x"

    def test_substitute_binary_expression(self):
        """Test substituting both operands in binary expression."""
        helper = TestFunctionCallHelper()

        expr = BinaryExpression(
            left=Identifier("a", line=1, column=0),
            operator="+",
            right=Identifier("b", line=1, column=4),
            line=1, column=2
        )
        assignments = {
            "a": NumberLiteral(10, line=1, column=0),
            "b": NumberLiteral(20, line=1, column=0)
        }
        param_names = set()

        result = helper._substitute_expression(expr, assignments, param_names, depth=0)

        assert isinstance(result, BinaryExpression)
        assert isinstance(result.left, NumberLiteral)
        assert result.left.value == 10
        assert isinstance(result.right, NumberLiteral)
        assert result.right.value == 20

    def test_substitute_function_call_arguments(self):
        """Test substituting function call arguments."""
        helper = TestFunctionCallHelper()

        expr = FunctionCall(
            function=Identifier("foo", line=1, column=0),
            arguments=[
                Identifier("x", line=1, column=4),
                Identifier("y", line=1, column=7)
            ],
            line=1, column=0
        )
        assignments = {
            "x": NumberLiteral(1, line=1, column=0),
            "y": NumberLiteral(2, line=1, column=0)
        }
        param_names = set()

        result = helper._substitute_expression(expr, assignments, param_names, depth=0)

        assert isinstance(result, FunctionCall)
        assert len(result.arguments) == 2
        assert isinstance(result.arguments[0], NumberLiteral)
        assert result.arguments[0].value == 1

    def test_substitute_recursion_limit(self):
        """Test that recursion is limited to prevent infinite loops."""
        helper = TestFunctionCallHelper()

        expr = Identifier("x", line=1, column=0)
        assignments = {"x": Identifier("x", line=1, column=0)}  # Circular reference
        param_names = set()

        result = helper._substitute_expression(expr, assignments, param_names, depth=11)

        # Should return None when depth exceeds 10
        assert result is None


class TestShouldWrapCall:
    """Test _should_wrap_call method."""

    def test_should_wrap_identifier_not_builtin(self):
        """Test that non-builtin identifiers should be wrapped."""
        helper = TestFunctionCallHelper()

        func_expr = Identifier("customFunc", line=1, column=0)

        result = helper._should_wrap_call(func_expr)

        assert result is True

    def test_should_wrap_builtin(self):
        """Test that builtin functions should be wrapped."""
        helper = TestFunctionCallHelper()
        helper.function_registry.is_allowed_builtin.return_value = True

        func_expr = "print"

        result = helper._should_wrap_call(func_expr)

        # Builtins ARE wrapped for validation
        assert result is True

    def test_should_wrap_member_access(self):
        """Test that member access calls should be wrapped."""
        helper = TestFunctionCallHelper()

        func_expr = MemberAccess(
            object=Identifier("obj", line=1, column=0),
            member="method",
            line=1, column=0
        )

        result = helper._should_wrap_call(func_expr)

        assert result is True

    def test_should_not_wrap_user_defined_function(self):
        """Test that user-defined functions should not be wrapped."""
        helper = TestFunctionCallHelper()
        helper.function_registry.is_user_defined.return_value = True

        func_expr = "myFunc"

        result = helper._should_wrap_call(func_expr)

        # User-defined functions are trusted, don't wrap
        assert result is False


class TestGenerateSimpleFunctionCall:
    """Test _generate_simple_function_call method."""

    def test_simple_call_no_arguments(self):
        """Test simple function call with no arguments for user-defined function."""
        helper = TestFunctionCallHelper()
        helper.function_registry.is_user_defined.return_value = True

        result = helper._generate_simple_function_call("foo", [])

        assert result == "foo()"

    def test_simple_call_with_arguments(self):
        """Test simple function call with arguments for user-defined function."""
        helper = TestFunctionCallHelper()
        helper.function_registry.is_user_defined.return_value = True

        args = [
            NumberLiteral(42, line=1, column=0),
            StringLiteral("hello", line=1, column=0)
        ]

        result = helper._generate_simple_function_call("foo", args)

        assert "foo(" in result
        assert "42" in result
        assert '"hello"' in result

    def test_simple_call_builtin_tracked(self):
        """Test that builtin function usage is tracked."""
        helper = TestFunctionCallHelper()
        helper.function_registry.is_allowed_builtin.return_value = True

        result = helper._generate_simple_function_call("print", [])

        # Should route to builtin module
        assert "builtin.print" in result
        assert "print" in helper.context.builtin_functions_used


class TestGenerateMemberFunctionCall:
    """Test _generate_member_function_call method."""

    def test_member_call_simple(self):
        """Test simple member function call."""
        helper = TestFunctionCallHelper()

        member_access = MemberAccess(
            object=Identifier("obj", line=1, column=0),
            member="method",
            line=1, column=0
        )
        args = []

        result = helper._generate_member_function_call(member_access, args)

        assert "obj" in result
        assert "method" in result

    def test_member_call_with_arguments(self):
        """Test member function call with arguments."""
        helper = TestFunctionCallHelper()

        member_access = MemberAccess(
            object=Identifier("obj", line=1, column=0),
            member="calculate",
            line=1, column=0
        )
        args = [NumberLiteral(10, line=1, column=0), NumberLiteral(20, line=1, column=0)]

        result = helper._generate_member_function_call(member_access, args)

        assert "obj" in result
        assert "calculate" in result
        assert "10" in result
        assert "20" in result

    def test_member_call_nested(self):
        """Test nested member function call."""
        helper = TestFunctionCallHelper()

        # obj.inner.method()
        inner_access = MemberAccess(
            object=Identifier("obj", line=1, column=0),
            member="inner",
            line=1, column=0
        )
        member_access = MemberAccess(
            object=inner_access,
            member="method",
            line=1, column=0
        )
        args = []

        result = helper._generate_member_function_call(member_access, args)

        assert "obj" in result
        assert "inner" in result
        assert "method" in result


class TestGenerateDirectCall:
    """Test _generate_direct_call method."""

    def test_direct_call_simple_function(self):
        """Test direct call to simple function."""
        helper = TestFunctionCallHelper()

        # node.function is a string for user-defined functions
        node = FunctionCall(
            function="myFunc",
            arguments=[NumberLiteral(42, line=1, column=0)],
            line=1, column=0
        )

        result = helper._generate_direct_call(node)

        assert result == "myFunc(42)"

    def test_direct_call_with_identifier(self):
        """Test direct call with Identifier object (fallback case)."""
        helper = TestFunctionCallHelper()

        node = FunctionCall(
            function=Identifier("myFunc", line=1, column=0),
            arguments=[],
            line=1, column=0
        )

        result = helper._generate_direct_call(node)

        # Should convert Identifier to string
        assert "myFunc" in result or "<mlpy" in result  # May be string representation


class TestGenerateWrappedCall:
    """Test _generate_wrapped_call method."""

    def test_wrapped_call_simple_function(self):
        """Test wrapped call to simple function."""
        helper = TestFunctionCallHelper()

        node = FunctionCall(
            function=Identifier("unsafeFunc", line=1, column=0),
            arguments=[NumberLiteral(42, line=1, column=0)],
            line=1, column=0
        )

        result = helper._generate_wrapped_call(node)

        # Should wrap with _safe_call
        assert "_safe_call" in result
        assert "unsafeFunc" in result

    def test_wrapped_call_with_multiple_arguments(self):
        """Test wrapped call with multiple arguments."""
        helper = TestFunctionCallHelper()

        node = FunctionCall(
            function=Identifier("func", line=1, column=0),
            arguments=[
                NumberLiteral(1, line=1, column=0),
                NumberLiteral(2, line=1, column=0),
                NumberLiteral(3, line=1, column=0)
            ],
            line=1, column=0
        )

        result = helper._generate_wrapped_call(node)

        assert "_safe_call" in result
        assert "1" in result
        assert "2" in result
        assert "3" in result


class TestRaiseUnknownFunctionError:
    """Test _raise_unknown_function_error method."""

    def test_raise_unknown_function_error(self):
        """Test raising unknown function error."""
        helper = TestFunctionCallHelper()
        helper.function_registry.get_all_allowed_functions.return_value = ['knownFunc', 'anotherFunc']
        helper.function_registry.get_call_category.return_value = 'user-defined'

        with pytest.raises(Exception) as exc_info:
            helper._raise_unknown_function_error("unknownFunc", [])

        error_msg = str(exc_info.value)
        assert "unknownFunc" in error_msg
        assert "whitelist" in error_msg or "Unknown" in error_msg

    def test_raise_unknown_function_with_suggestions(self):
        """Test that error includes similar function suggestions."""
        helper = TestFunctionCallHelper()
        helper.function_registry.get_all_allowed_functions.return_value = ['calculateSum', 'calculateProduct']
        helper.function_registry.get_call_category.return_value = 'user-defined'

        with pytest.raises(Exception) as exc_info:
            helper._raise_unknown_function_error("calcSum", [])

        error_msg = str(exc_info.value)
        # Should suggest similar functions
        assert "calcSum" in error_msg


class TestRaiseUnknownModuleFunctionError:
    """Test _raise_unknown_module_function_error method."""

    def test_raise_unknown_module_function_error(self):
        """Test raising unknown module function error."""
        helper = TestFunctionCallHelper()

        # Mock module metadata
        mock_metadata = Mock()
        mock_metadata.functions = {'sqrt': Mock(), 'pow': Mock(), 'abs': Mock()}
        helper.function_registry.imported_modules = {'math': mock_metadata}

        with pytest.raises(Exception) as exc_info:
            helper._raise_unknown_module_function_error("math", "unknownOp", [])

        error_msg = str(exc_info.value)
        assert "math" in error_msg
        assert "unknownOp" in error_msg

    def test_raise_unknown_module_function_with_module_name(self):
        """Test error message includes module context."""
        helper = TestFunctionCallHelper()
        # No metadata for unknown module
        helper.function_registry.imported_modules = {}

        with pytest.raises(Exception) as exc_info:
            helper._raise_unknown_module_function_error("customModule", "missingFunc", [])

        error_msg = str(exc_info.value)
        assert "customModule" in error_msg
        assert "missingFunc" in error_msg


class TestGenerateFunctionCallWrapped:
    """Test _generate_function_call_wrapped method."""

    def test_function_call_wrapped_user_defined(self):
        """Test that user-defined functions are not wrapped."""
        helper = TestFunctionCallHelper()
        helper.function_registry.is_user_defined.return_value = True

        # node.function should be a string for user-defined functions
        node_user = FunctionCall(
            function="myFunc",
            arguments=[NumberLiteral(42, line=1, column=0)],
            line=1, column=0
        )

        result = helper._generate_function_call_wrapped(node_user)

        # Should generate direct call (no _safe_call wrapper)
        assert "_safe_call" not in result
        assert "myFunc" in result

    def test_function_call_wrapped_wraps_builtin(self):
        """Test that builtin functions are wrapped."""
        helper = TestFunctionCallHelper()
        helper.function_registry.is_allowed_builtin.return_value = True

        node_builtin = FunctionCall(
            function="print",
            arguments=[StringLiteral("hello", line=1, column=0)],
            line=1, column=0
        )

        result = helper._generate_function_call_wrapped(node_builtin)

        # Builtins should be wrapped
        assert "_safe_call" in result
