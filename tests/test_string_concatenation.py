#!/usr/bin/env python3
"""Unit tests for string concatenation type coercion."""

import pytest
from mlpy.ml.transpiler import transpile_ml_code


class TestStringConcatenation:
    """Test that string concatenation with numbers is properly transpiled."""

    def test_string_plus_integer(self):
        """Test string concatenation with integer."""
        ml_code = """
        function test() {
            count = 42;
            message = "Count: " + count;
            return message;
        }
        """

        result = transpile_ml_code(ml_code, "test_string_int.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should NOT contain runtime errors when executed
        assert "UNKNOWN_EXPRESSION" not in generated_code, "String concatenation not transpiled"

        # Should be syntactically valid Python
        try:
            compile(generated_code, "test", "exec")
        except SyntaxError as e:
            pytest.fail(f"Generated code has syntax error: {e}")

        # Should run without TypeError
        try:
            exec(generated_code)
        except TypeError as e:
            if "can only concatenate str" in str(e):
                pytest.fail(f"String concatenation not handling type coercion: {e}")

    def test_string_plus_object_property_integer(self):
        """Test string concatenation with object property (integer) - the ecosystem bug case."""
        ml_code = """
        function test() {
            config = {};
            config.initial_predators = 10;
            message = "Predators: " + config.initial_predators;
            return message;
        }
        """

        result = transpile_ml_code(ml_code, "test_object_concat.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # This should reveal the bug - dictionary access with integer values
        try:
            exec(generated_code)
        except TypeError as e:
            if "can only concatenate str" in str(e):
                pytest.fail(f"String concatenation with object property failing: {e}\n\nGenerated code:\n{generated_code}")

    def test_string_plus_float(self):
        """Test string concatenation with float."""
        ml_code = """
        function test() {
            price = 19.99;
            message = "Price: $" + price;
            return message;
        }
        """

        result = transpile_ml_code(ml_code, "test_string_float.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should run without TypeError
        try:
            exec(generated_code)
        except TypeError as e:
            if "can only concatenate str" in str(e):
                pytest.fail(f"String concatenation not handling float coercion: {e}")

    def test_multiple_string_concatenations(self):
        """Test multiple string concatenations with numbers."""
        ml_code = """
        function test() {
            x = 10;
            y = 20;
            result = "x: " + x + ", y: " + y;
            return result;
        }
        """

        result = transpile_ml_code(ml_code, "test_multiple_concat.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should run without TypeError
        try:
            exec(generated_code)
        except TypeError as e:
            if "can only concatenate str" in str(e):
                pytest.fail(f"Multiple string concatenation failing: {e}")

    def test_string_in_print_statement(self):
        """Test string concatenation in print statements (like the ecosystem bug)."""
        ml_code = """
        function test() {
            predators = 10;
            prey = 50;
            print("Predators: " + predators);
            print("Prey: " + prey);
            return true;
        }
        """

        result = transpile_ml_code(ml_code, "test_print_concat.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # This is the specific case from ecosystem simulation
        try:
            exec(generated_code)
        except TypeError as e:
            if "can only concatenate str" in str(e):
                pytest.fail(f"Print statement string concatenation failing: {e}")

    def test_string_plus_boolean(self):
        """Test string concatenation with boolean."""
        ml_code = """
        function test() {
            flag = true;
            message = "Status: " + flag;
            return message;
        }
        """

        result = transpile_ml_code(ml_code, "test_string_bool.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should run without TypeError
        try:
            exec(generated_code)
        except TypeError as e:
            if "can only concatenate str" in str(e):
                pytest.fail(f"String concatenation not handling boolean coercion: {e}")

    def test_number_plus_string(self):
        """Test number + string concatenation (reverse order)."""
        ml_code = """
        function test() {
            count = 5;
            message = count + " items";
            return message;
        }
        """

        result = transpile_ml_code(ml_code, "test_num_string.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should run without TypeError
        try:
            exec(generated_code)
        except TypeError as e:
            if "can only concatenate str" in str(e) or "unsupported operand type" in str(e):
                pytest.fail(f"Number + string concatenation failing: {e}")

    def test_complex_expression_concatenation(self):
        """Test string concatenation with complex expressions."""
        ml_code = """
        function test() {
            x = 10;
            y = 5;
            message = "Result: " + (x + y) + " total";
            return message;
        }
        """

        result = transpile_ml_code(ml_code, "test_complex_concat.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should run without TypeError
        try:
            exec(generated_code)
        except TypeError as e:
            if "can only concatenate str" in str(e):
                pytest.fail(f"Complex expression concatenation failing: {e}")

    def test_dictionary_access_string_concatenation(self):
        """Test string concatenation with dictionary access containing integers (the actual ecosystem bug)."""
        ml_code = """
        function test() {
            config = {};
            config.initial_predators = 10;
            config.initial_prey = 50;
            result = "Predators: " + config.initial_predators + ", Prey: " + config.initial_prey;
            return result;
        }
        """

        result = transpile_ml_code(ml_code, "test_dict_concat.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should NOT contain runtime errors when executed
        assert "UNKNOWN_EXPRESSION" not in generated_code, "Dictionary concatenation not transpiled"

        # Should be syntactically valid Python
        try:
            compile(generated_code, "test", "exec")
        except SyntaxError as e:
            pytest.fail(f"Generated code has syntax error: {e}")

        # This is the critical test - should run without TypeError
        # This will fail because the transpiler doesn't handle type coercion
        test_exec_code = generated_code + """
# Execute the test function
try:
    result = test()
    print(f"Success: {result}")
except TypeError as e:
    print(f"TypeError: {e}")
    raise e
"""

        try:
            exec(test_exec_code)
        except TypeError as e:
            if "can only concatenate str" in str(e):
                pytest.fail(f"Dictionary access string concatenation failing with TypeError: {e}\n\nGenerated code:\n{generated_code}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])