#!/usr/bin/env python3
"""Unit tests for standard library function resolution."""

import pytest
from mlpy.ml.transpiler import transpile_ml_code


class TestStandardLibraryResolution:
    """Test that standard library functions are properly resolved during transpilation."""

    def test_collections_import_resolution(self):
        """Test that collections module functions are resolved."""
        ml_code = """
        import collections;

        function testCollections() {
            list = [1, 2, 3];
            result = collections.append(list, 4);
            return result;
        }
        """

        result = transpile_ml_code(ml_code, "test_collections.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should NOT contain unknown identifiers
        assert "ml_unknown_identifier" not in generated_code, "Collections functions not resolved"

        # Should contain proper function calls
        assert "collections.append" in generated_code, "Collections.append not properly resolved"

    def test_random_import_resolution(self):
        """Test that random module functions are resolved."""
        ml_code = """
        import random;

        function testRandom() {
            num = random.randomInt(1, 10);
            return num;
        }
        """

        result = transpile_ml_code(ml_code, "test_random.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should NOT contain unknown identifiers
        assert "ml_unknown_identifier" not in generated_code, "Random functions not resolved"

        # Should contain proper function calls
        assert "random.randomInt" in generated_code, "random.randomInt not properly resolved"

    def test_math_import_resolution(self):
        """Test that math module functions are resolved."""
        ml_code = """
        import math;

        function testMath() {
            result = math.sqrt(16);
            return result;
        }
        """

        result = transpile_ml_code(ml_code, "test_math.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should NOT contain unknown identifiers
        assert "ml_unknown_identifier" not in generated_code, "Math functions not resolved"

        # Should contain proper function calls
        assert "math.sqrt" in generated_code, "math.sqrt not properly resolved"

    def test_multiple_imports_resolution(self):
        """Test that multiple standard library imports work together."""
        ml_code = """
        import collections;
        import random;
        import math;

        function testMultiple() {
            list = [1, 2, 3];
            extended = collections.append(list, 4);
            randomNum = random.random();
            sqrtResult = math.sqrt(25);
            return extended;
        }
        """

        result = transpile_ml_code(ml_code, "test_multiple.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should NOT contain ANY unknown identifiers
        unknown_count = generated_code.count("ml_unknown_identifier")
        assert unknown_count == 0, f"Found {unknown_count} unresolved functions in multi-import code"

        # Should contain all proper function calls
        assert "collections.append" in generated_code, "collections.append not resolved"
        assert "random.random" in generated_code, "random.random not resolved"
        assert "math.sqrt" in generated_code, "math.sqrt not resolved"

    def test_function_chaining_resolution(self):
        """Test that chained standard library function calls work."""
        ml_code = """
        import collections;
        import math;

        function testChaining() {
            numbers = [1, 4, 9, 16];
            squared = collections.map(numbers, math.sqrt);
            return squared;
        }
        """

        result = transpile_ml_code(ml_code, "test_chaining.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should NOT contain unknown identifiers
        assert "ml_unknown_identifier" not in generated_code, "Function chaining not resolved"

        # Should contain proper function calls
        assert "collections.map" in generated_code, "collections.map not resolved"
        assert "math.sqrt" in generated_code, "math.sqrt not resolved in function argument"

    def test_nested_function_calls_resolution(self):
        """Test that nested standard library calls are resolved."""
        ml_code = """
        import collections;
        import random;

        function testNested() {
            list = [1, 2, 3];
            randomElement = random.choice(collections.append(list, 4));
            return randomElement;
        }
        """

        result = transpile_ml_code(ml_code, "test_nested.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should NOT contain unknown identifiers
        assert "ml_unknown_identifier" not in generated_code, "Nested function calls not resolved"

        # Should contain both function calls
        assert "collections.append" in generated_code, "collections.append not resolved in nested call"
        assert "random.choice" in generated_code, "random.choice not resolved"

    def test_ecosystem_simulation_resolution(self):
        """Test that the ecosystem simulation has all functions resolved."""
        # Read the actual ecosystem simulation
        with open("docs/examples/advanced/ecosystem-sim/main.ml", "r") as f:
            ml_code = f.read()

        result = transpile_ml_code(ml_code, "ecosystem_main.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # This is the critical test - ecosystem should have ZERO unknown identifiers
        unknown_count = generated_code.count("ml_unknown_identifier")

        if unknown_count > 0:
            # Extract some examples for debugging
            lines = generated_code.split('\n')
            unknown_lines = [line.strip() for line in lines if 'ml_unknown_identifier' in line][:10]
            error_msg = f"Ecosystem simulation has {unknown_count} unresolved functions. Examples:\n"
            error_msg += "\n".join(f"  - {line}" for line in unknown_lines)
            pytest.fail(error_msg)

        # Should contain proper standard library calls
        assert "collections." in generated_code or "random." in generated_code or "math." in generated_code, \
            "No standard library functions found in ecosystem simulation"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])