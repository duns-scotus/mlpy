#!/usr/bin/env python3
"""Unit tests for ternary expression transpilation."""

import pytest
from mlpy.ml.transpiler import transpile_ml_code


class TestTernaryExpressions:
    """Test that ternary/conditional expressions are properly transpiled."""

    def test_simple_ternary_expression(self):
        """Test basic ternary expression."""
        ml_code = """
        function testTernary() {
            x = 5;
            result = x > 3 ? "big" : "small";
            return result;
        }
        """

        result = transpile_ml_code(ml_code, "test_ternary.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should NOT contain unknown expressions
        assert "UNKNOWN_EXPRESSION" not in generated_code, "Ternary expression not transpiled"

        # Should contain valid Python ternary syntax (flexible with quotes)
        assert ("'big' if (x > 3) else 'small'" in generated_code or
                '"big" if (x > 3) else "small"' in generated_code or
                "('big' if (x > 3) else 'small')" in generated_code or
                '("big" if (x > 3) else "small")' in generated_code), \
               "Ternary not converted to Python conditional expression"

    def test_nested_ternary_expressions(self):
        """Test nested ternary expressions."""
        ml_code = """
        function testNested() {
            score = 85;
            grade = score >= 90 ? "A" : score >= 80 ? "B" : "C";
            return grade;
        }
        """

        result = transpile_ml_code(ml_code, "test_nested.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should NOT contain unknown expressions
        assert "UNKNOWN_EXPRESSION" not in generated_code, "Nested ternary not transpiled"

        # Should contain properly nested conditional expressions
        assert (("'A' if" in generated_code or '"A" if' in generated_code) and
                ("'B' if" in generated_code or '"B" if' in generated_code)), \
               "Nested ternary not properly converted"

    def test_ternary_with_function_calls(self):
        """Test ternary expression with function calls."""
        ml_code = """
        function getValue() {
            return 42;
        }

        function testTernaryWithCalls() {
            flag = true;
            result = flag ? getValue() : 0;
            return result;
        }
        """

        result = transpile_ml_code(ml_code, "test_ternary_calls.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should NOT contain unknown expressions
        assert "UNKNOWN_EXPRESSION" not in generated_code, "Ternary with function calls not transpiled"

        # Should contain valid function call in conditional
        assert "getValue()" in generated_code, "Function call in ternary not preserved"

    def test_ternary_in_assignment(self):
        """Test ternary expression used in variable assignment."""
        ml_code = """
        function testAssignment() {
            temperature = 25;
            weather = temperature > 20 ? "warm" : "cold";
            return weather;
        }
        """

        result = transpile_ml_code(ml_code, "test_ternary_assignment.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should NOT contain unknown expressions
        assert "UNKNOWN_EXPRESSION" not in generated_code, "Ternary in assignment not transpiled"

        # Should be syntactically valid Python
        # Try to compile it
        try:
            compile(generated_code, "test", "exec")
        except SyntaxError as e:
            pytest.fail(f"Generated code has syntax error: {e}")

    def test_ternary_in_function_argument(self):
        """Test ternary expression as function argument."""
        ml_code = """
        function processValue(val) {
            return val * 2;
        }

        function testTernaryArg() {
            x = 10;
            result = processValue(x > 5 ? x : 1);
            return result;
        }
        """

        result = transpile_ml_code(ml_code, "test_ternary_arg.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should NOT contain unknown expressions
        assert "UNKNOWN_EXPRESSION" not in generated_code, "Ternary as function argument not transpiled"

        # Should contain valid function call with conditional argument
        assert "processValue(" in generated_code, "Function call not preserved"

    def test_ternary_with_complex_conditions(self):
        """Test ternary with complex boolean conditions."""
        ml_code = """
        function testComplex() {
            a = 5;
            b = 10;
            c = 3;
            result = (a > b && b > c) ? "all good" : "something wrong";
            return result;
        }
        """

        result = transpile_ml_code(ml_code, "test_complex_ternary.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should NOT contain unknown expressions
        assert "UNKNOWN_EXPRESSION" not in generated_code, "Complex ternary not transpiled"

        # Should handle logical operators properly
        assert "and" in generated_code or "&&" in generated_code, "Logical operators not handled"

    def test_ternary_with_arithmetic(self):
        """Test ternary expression with arithmetic operations."""
        ml_code = """
        function testArithmetic() {
            x = 10;
            y = 5;
            max_value = x > y ? x + 1 : y - 1;
            return max_value;
        }
        """

        result = transpile_ml_code(ml_code, "test_arithmetic_ternary.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should NOT contain unknown expressions
        assert "UNKNOWN_EXPRESSION" not in generated_code, "Arithmetic ternary not transpiled"

        # Should preserve arithmetic operations
        assert "+" in generated_code and "-" in generated_code, "Arithmetic operations not preserved"

    def test_ecosystem_ternary_case(self):
        """Test the specific ternary case found in ecosystem simulation."""
        ml_code = """
        function preyMove(prey, time_step) {
            speed_multiplier = prey.state == "fleeing" ? 2.0 : 1.0;
            return speed_multiplier;
        }
        """

        result = transpile_ml_code(ml_code, "test_ecosystem_ternary.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should NOT contain unknown expressions
        assert "UNKNOWN_EXPRESSION" not in generated_code, f"Ecosystem ternary not transpiled. Code: {generated_code}"
        assert "TernaryExpression" not in generated_code, "TernaryExpression not converted to Python"

        # Should be syntactically valid
        try:
            compile(generated_code, "test", "exec")
        except SyntaxError as e:
            pytest.fail(f"Generated ecosystem ternary has syntax error: {e}\n\nCode:\n{generated_code}")

    def test_multiple_ternary_expressions(self):
        """Test multiple ternary expressions in same function."""
        ml_code = """
        function testMultiple() {
            x = 10;
            y = 20;
            first = x > 5 ? "big" : "small";
            second = y < 30 ? "normal" : "huge";
            return first + second;
        }
        """

        result = transpile_ml_code(ml_code, "test_multiple_ternary.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should NOT contain unknown expressions
        assert "UNKNOWN_EXPRESSION" not in generated_code, "Multiple ternary expressions not transpiled"

        # Should have two conditional expressions
        condition_count = generated_code.count(" if ") + generated_code.count("(if ")
        assert condition_count >= 2, f"Expected at least 2 conditional expressions, found {condition_count}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])