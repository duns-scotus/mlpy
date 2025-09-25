#!/usr/bin/env python3
"""Unit tests for null vs None transpilation."""

import pytest
from mlpy.ml.transpiler import transpile_ml_code


class TestNullNoneTranspilation:
    """Test that ML null values are properly transpiled to Python None."""

    def test_null_literal_assignment(self):
        """Test null literal in variable assignment."""
        ml_code = """
        function test() {
            target = null;
            return target;
        }
        """

        result = transpile_ml_code(ml_code, "test_null_literal.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should NOT contain 'null' - should be converted to 'None'
        assert "null" not in generated_code, f"ML 'null' not converted to Python 'None'. Code: {generated_code}"
        assert "None" in generated_code, "Python 'None' not found in generated code"

        # Should be syntactically valid Python
        try:
            compile(generated_code, "test", "exec")
        except SyntaxError as e:
            pytest.fail(f"Generated code has syntax error: {e}")

        # Should run without NameError
        try:
            exec(generated_code + "\nresult = test()\nprint(f'Result: {result}')")
        except NameError as e:
            if "null" in str(e):
                pytest.fail(f"null not converted to None, causing NameError: {e}\n\nGenerated code:\n{generated_code}")

    def test_null_comparison(self):
        """Test null in comparison operations."""
        ml_code = """
        function test() {
            value = getValue();
            if (value != null) {
                return "not null";
            }
            return "is null";
        }

        function getValue() {
            return null;
        }
        """

        result = transpile_ml_code(ml_code, "test_null_comparison.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should NOT contain 'null' as a literal (but 'null' inside strings is fine)
        # Check for patterns like "!= null", "return null"
        problematic_patterns = ["!= null", "== null", "return null", " = null"]
        for pattern in problematic_patterns:
            if pattern in generated_code:
                pytest.fail(f"Found ML 'null' literal pattern '{pattern}' not converted to 'None'. Code: {generated_code}")

        # Should run without NameError
        try:
            exec(generated_code + "\nresult = test()\nprint(f'Result: {result}')")
        except NameError as e:
            if "null" in str(e):
                pytest.fail(f"null not converted to None in comparison: {e}")

    def test_null_return_value(self):
        """Test null as return value."""
        ml_code = """
        function maybeGetValue(flag) {
            if (flag) {
                return 42;
            }
            return null;
        }
        """

        result = transpile_ml_code(ml_code, "test_null_return.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should NOT contain 'null'
        assert "null" not in generated_code, f"ML 'null' not converted to Python 'None'. Code: {generated_code}"

        # Should run without NameError
        try:
            exec(generated_code + "\nresult1 = maybeGetValue(True)\nresult2 = maybeGetValue(False)\nprint(f'Results: {result1}, {result2}')")
        except NameError as e:
            if "null" in str(e):
                pytest.fail(f"null not converted to None in return: {e}")

    def test_null_in_object_property(self):
        """Test null assigned to object property."""
        ml_code = """
        function test() {
            obj = {};
            obj.value = null;
            obj.target = null;
            return obj;
        }
        """

        result = transpile_ml_code(ml_code, "test_null_object.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should NOT contain 'null'
        assert "null" not in generated_code, f"ML 'null' not converted to Python 'None'. Code: {generated_code}"

        # Should run without NameError
        try:
            exec(generated_code + "\nresult = test()\nprint(f'Result: {result}')")
        except NameError as e:
            if "null" in str(e):
                pytest.fail(f"null not converted to None in object property: {e}")

    def test_null_in_function_argument(self):
        """Test null passed as function argument."""
        ml_code = """
        function processValue(val) {
            if (val == null) {
                return "received null";
            }
            return "received: " + val;
        }

        function test() {
            result1 = processValue(null);
            result2 = processValue("hello");
            return result1 + " | " + result2;
        }
        """

        result = transpile_ml_code(ml_code, "test_null_argument.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should NOT contain 'null' as a literal (but 'null' inside strings is fine)
        # Check for patterns like "== null", "processValue(null)"
        problematic_patterns = ["== null", "!= null", "(null)", " = null"]
        for pattern in problematic_patterns:
            if pattern in generated_code:
                pytest.fail(f"Found ML 'null' literal pattern '{pattern}' not converted to 'None'. Code: {generated_code}")

        # Should run without NameError
        try:
            exec(generated_code + "\nresult = test()\nprint(f'Result: {result}')")
        except NameError as e:
            if "null" in str(e):
                pytest.fail(f"null not converted to None in function argument: {e}")

    def test_multiple_null_occurrences(self):
        """Test multiple null occurrences in same function."""
        ml_code = """
        function test() {
            a = null;
            b = null;
            c = null;
            if (a == null && b != null) {
                return null;
            }
            return c;
        }
        """

        result = transpile_ml_code(ml_code, "test_multiple_null.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should NOT contain any 'null'
        assert "null" not in generated_code, f"ML 'null' not converted to Python 'None'. Code: {generated_code}"

        # Should contain multiple 'None'
        none_count = generated_code.count("None")
        assert none_count >= 4, f"Expected at least 4 'None' occurrences, found {none_count}"

        # Should run without NameError
        try:
            exec(generated_code + "\nresult = test()\nprint(f'Result: {result}')")
        except NameError as e:
            if "null" in str(e):
                pytest.fail(f"null not converted to None in multiple occurrences: {e}")

    def test_ecosystem_predator_target_case(self):
        """Test the specific case found in ecosystem simulation."""
        ml_code = """
        function createPredator(position, energy, speed, hunting_efficiency, detection_range) {
            predator = {};
            predator.position = position;
            predator.energy = energy;
            predator.speed = speed;
            predator.hunting_efficiency = hunting_efficiency;
            predator.detection_range = detection_range;
            predator.state = "patrolling";
            predator.age = 0;
            predator.last_meal = 0;
            predator.target = null;
            return predator;
        }
        """

        result = transpile_ml_code(ml_code, "test_ecosystem_null.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should NOT contain 'null' - this is the specific bug from ecosystem
        assert "null" not in generated_code, f"Ecosystem predator.target = null not converted. Code: {generated_code}"

        # Should contain 'None'
        assert "None" in generated_code, "Python 'None' not found for predator.target"

        # Should be syntactically valid
        try:
            compile(generated_code, "test", "exec")
        except SyntaxError as e:
            pytest.fail(f"Generated ecosystem null code has syntax error: {e}")

        # This is the critical test - should run without NameError
        test_exec_code = generated_code + """
# Test the predator creation
try:
    predator = createPredator({'x': 0, 'y': 0}, 100, 1.5, 0.4, 30)
    print(f"Success: predator.target = {predator['target']}")
except NameError as e:
    print(f"NameError: {e}")
    raise e
"""

        try:
            exec(test_exec_code)
        except NameError as e:
            if "null" in str(e):
                pytest.fail(f"Ecosystem predator.target = null failing with NameError: {e}\n\nGenerated code:\n{generated_code}")

    def test_null_in_conditional_expression(self):
        """Test null in ternary/conditional expressions."""
        ml_code = """
        function test() {
            flag = true;
            result = flag ? "value" : null;
            return result;
        }
        """

        result = transpile_ml_code(ml_code, "test_null_ternary.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should NOT contain 'null'
        assert "null" not in generated_code, f"ML 'null' not converted in ternary expression. Code: {generated_code}"

        # Should run without NameError
        try:
            exec(generated_code + "\nresult = test()\nprint(f'Result: {result}')")
        except NameError as e:
            if "null" in str(e):
                pytest.fail(f"null not converted to None in ternary: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])