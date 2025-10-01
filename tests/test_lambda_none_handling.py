#!/usr/bin/env python3
"""Unit tests for lambda function None handling."""

import pytest

from mlpy.ml.transpiler import transpile_ml_code


class TestLambdaNoneHandling:
    """Test that lambda functions handle None values correctly."""

    def test_simple_lambda_with_none_return(self):
        """Test lambda function that returns None."""
        ml_code = """
        function test() {
            numbers = [1, 2, 3];
            processed = numbers.map(lambda x: null);
            return processed;
        }
        """

        result = transpile_ml_code(ml_code, "test_lambda_none.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should NOT contain 'null' - should be converted to 'None'
        assert (
            "null" not in generated_code
        ), f"Lambda null not converted to None. Code: {generated_code}"

        # Should be syntactically valid Python
        try:
            compile(generated_code, "test", "exec")
        except SyntaxError as e:
            pytest.fail(f"Generated code has syntax error: {e}")

    def test_lambda_processing_with_none_result(self):
        """Test lambda processing that can produce None values."""
        ml_code = """
        function processItems(items) {
            processed = items.map(lambda item: {
                if (item.valid) {
                    return item;
                }
                return null;
            });
            return processed;
        }
        """

        result = transpile_ml_code(ml_code, "test_lambda_process.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should be syntactically valid
        try:
            compile(generated_code, "test", "exec")
        except SyntaxError as e:
            pytest.fail(f"Generated lambda processing has syntax error: {e}")

    def test_filter_with_none_values(self):
        """Test filtering array that might contain None values."""
        ml_code = """
        function test() {
            items = [1, null, 3, null, 5];
            filtered = items.filter(lambda x: x != null);
            return filtered;
        }
        """

        result = transpile_ml_code(ml_code, "test_filter_none.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should handle None values in filter
        assert "null" not in generated_code, "null not converted to None in filter"

        # Should be syntactically valid
        try:
            compile(generated_code, "test", "exec")
        except SyntaxError as e:
            pytest.fail(f"Generated filter code has syntax error: {e}")

    def test_map_returning_none_then_filter(self):
        """Test the specific pattern: map returns None, then filter tries to access properties."""
        ml_code = """
        function processPreyBehavior(prey_population, predators, environment, time_step) {
            alive_prey = prey_population.filter(lambda prey: prey.energy > 0);
            processed_prey = alive_prey.map(lambda prey_individual: {
                // This function might return null for some prey
                if (prey_individual.energy < 10) {
                    return null;
                }
                return prey_individual;
            });
            // This should fail if processed_prey contains None values
            return processed_prey.filter(lambda prey: prey.energy > 0);
        }
        """

        result = transpile_ml_code(ml_code, "test_map_filter.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should be syntactically valid
        try:
            compile(generated_code, "test", "exec")
        except SyntaxError as e:
            pytest.fail(f"Generated map-filter code has syntax error: {e}")

        # This is the critical test - should handle None values gracefully
        # Let's test with sample data that would trigger the bug
        test_exec_code = (
            generated_code
            + """
# Test with sample data that triggers the None issue
try:
    prey_data = [
        {'energy': 15, 'name': 'prey1'},
        {'energy': 5, 'name': 'prey2'},  # This will become None after map
        {'energy': 20, 'name': 'prey3'}
    ]

    result = processPreyBehavior(prey_data, [], {}, 1)
    print(f"Success: {len(result)} prey survived processing")

except TypeError as e:
    if "'NoneType' object is not subscriptable" in str(e):
        print(f"TypeError: {e}")
        raise e
    else:
        raise e
"""
        )

        try:
            exec(test_exec_code)
        except TypeError as e:
            if "'NoneType' object is not subscriptable" in str(e):
                pytest.fail(
                    f"Map-filter pattern failing with NoneType error: {e}\n\nGenerated code:\n{generated_code}"
                )

    def test_ecosystem_prey_behavior_pattern(self):
        """Test the specific ecosystem prey behavior pattern that's failing."""
        ml_code = """
        function processPreyBehavior(prey_population, predator_population, environment, time_step) {
            alive_prey = prey_population.filter(lambda prey: prey.energy > 0);
            processed_prey = alive_prey.map(lambda prey_individual: null);
            return processed_prey.filter(lambda prey: prey.energy > 0);
        }
        """

        result = transpile_ml_code(ml_code, "test_ecosystem_prey.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should be syntactically valid
        try:
            compile(generated_code, "test", "exec")
        except SyntaxError as e:
            pytest.fail(f"Generated ecosystem prey code has syntax error: {e}")

        # This should reveal the exact bug from ecosystem simulation
        test_exec_code = (
            generated_code
            + """
# Import ml_collections for testing
import sys
sys.path.insert(0, '../../../../src')
from mlpy.stdlib.collections import collections as ml_collections

# Test with the exact ecosystem scenario
try:
    prey_data = [
        {'energy': 50, 'state': 'grazing'},
        {'energy': 30, 'state': 'fleeing'},
        {'energy': 80, 'state': 'grazing'}
    ]

    result = processPreyBehavior(prey_data, [], {}, 0.1)
    print(f"Success: processed {len(result)} prey")

except TypeError as e:
    if "'NoneType' object is not subscriptable" in str(e):
        print(f"Ecosystem TypeError: {e}")
        raise e
    else:
        raise e
"""
        )

        try:
            exec(test_exec_code)
        except TypeError as e:
            if "'NoneType' object is not subscriptable" in str(e):
                pytest.fail(
                    f"Ecosystem prey behavior failing with NoneType error: {e}\n\nGenerated code:\n{generated_code}"
                )

    def test_multistatement_function_in_map(self):
        """Test multi-statement function expression in map (the actual ecosystem bug)."""
        ml_code = """
        function processItems(items) {
            result = items.map(function(item) {
                processed = item * 2;
                validated = processed + 1;
                return validated;
            });
            return result;
        }
        """

        result = transpile_ml_code(ml_code, "test_multistatement_map.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should NOT be None (this is the bug we're catching)
        if generated_code is None:
            pytest.fail(
                "Transpiler returned None for multi-statement function - this is the bug we need to fix"
            )

        # Should be syntactically valid
        try:
            compile(generated_code, "test", "exec")
        except SyntaxError as e:
            pytest.fail(f"Generated multi-statement function has syntax error: {e}")

        # Should NOT convert to lambda that returns None
        assert (
            "lambda" not in generated_code
            or "lambda" in generated_code
            and ": None" not in generated_code
        ), "Multi-statement function incorrectly converted to lambda returning None"

    def test_ecosystem_processPreyBehavior_pattern(self):
        """Test the exact pattern from ecosystem processPreyBehavior function."""
        ml_code = """
        function processPreyBehavior(prey_population, predators, environment, time_step) {
            alive_prey = prey_population.filter(function(prey) {
                return prey.energy > 0;
            });

            processed_prey = alive_prey.map(function(prey_individual) {
                updated_prey = prey_individual;
                updated_prey.energy = updated_prey.energy - 1;
                updated_prey.age = updated_prey.age + time_step;
                return updated_prey;
            });

            return processed_prey.filter(function(prey) {
                return prey.energy > 0;
            });
        }
        """

        result = transpile_ml_code(ml_code, "test_ecosystem_behavior.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should NOT be None - this indicates the transpilation bug
        if generated_code is None:
            pytest.fail("Ecosystem processPreyBehavior transpilation failed - returned None")

        # Should be syntactically valid
        try:
            compile(generated_code, "test", "exec")
        except SyntaxError as e:
            pytest.fail(f"Generated ecosystem behavior has syntax error: {e}")

        # Critical test: should NOT have lambda returning None
        if "lambda prey_individual: None" in generated_code:
            pytest.fail(
                f"Multi-statement function converted to 'lambda: None' - this causes NoneType subscript errors!\n\nGenerated:\n{generated_code}"
            )

    def test_none_safe_property_access(self):
        """Test that None values don't cause subscript errors when used properly."""
        ml_code = """
        function safePrprocess(items) {
            // First filter out None values
            valid_items = items.filter(lambda x: x != null);
            // Then process the valid items
            return valid_items.map(lambda item: item.value);
        }
        """

        result = transpile_ml_code(ml_code, "test_none_safe.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        # Should handle None values safely
        test_exec_code = (
            generated_code
            + """
# Test with data containing None values
try:
    test_data = [
        {'value': 10},
        None,
        {'value': 20},
        None,
        {'value': 30}
    ]

    result = safePrprocess(test_data)
    print(f"Safe processing result: {result}")

except Exception as e:
    print(f"Error in safe processing: {e}")
    raise e
"""
        )

        try:
            exec(test_exec_code)
        except TypeError as e:
            if "'NoneType' object is not subscriptable" in str(e):
                pytest.fail(f"None-safe processing still failing: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
