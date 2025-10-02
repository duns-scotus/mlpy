#!/usr/bin/env python3
"""Unit tests for lambda function None handling."""

import pytest

from tests.helpers.repl_test_helper import REPLTestHelper


class TestLambdaNoneHandling:
    """Test that lambda functions handle None values correctly."""

    def test_simple_lambda_with_none_return(self):
        """Test arrow function that returns None."""
        repl = REPLTestHelper()

        repl.execute_ml("import functional;")
        repl.execute_ml("function test() { numbers = [1, 2, 3]; processed = functional.map(fn(x) => null, numbers); return processed; }")

        result = repl.execute_ml("test()")

        # Should return list of None values
        assert result == [None, None, None], f"Expected [None, None, None], got {result}"

    def test_lambda_processing_with_none_result(self):
        """Test lambda processing that can produce None values."""
        repl = REPLTestHelper()

        repl.execute_ml("import functional;")
        repl.execute_ml("function processItems(items) { processed = functional.map(fn(item) => item.valid ? item : null, items); return processed; }")

        repl.set_variable('items', [
            {'valid': True, 'value': 1},
            {'valid': False, 'value': 2},
            {'valid': True, 'value': 3}
        ])

        result = repl.execute_ml("processItems(items)")

        # Should return [item1, None, item3]
        assert len(result) == 3, f"Expected 3 items, got {len(result)}"
        assert result[0] is not None, "First item should not be None"
        assert result[1] is None, "Second item should be None"
        assert result[2] is not None, "Third item should not be None"

    def test_filter_with_none_values(self):
        """Test filtering array that might contain None values."""
        repl = REPLTestHelper()

        repl.execute_ml("import functional;")
        repl.execute_ml("function test() { items = [1, null, 3, null, 5]; filtered = functional.filter(fn(x) => x != null, items); return filtered; }")

        result = repl.execute_ml("test()")

        # Should successfully filter out None values
        assert result == [1, 3, 5], f"Expected [1, 3, 5], got {result}"

    def test_map_returning_none_then_filter(self):
        """Test that accessing properties on None correctly raises an error."""
        repl = REPLTestHelper()

        # Import functional
        repl.execute_ml("import functional;")

        # Define a function with the WRONG pattern (map to null, then filter accessing properties)
        repl.execute_ml("function processBuggyPattern(prey_population) { processed = functional.map(fn(prey) => prey.energy < 10 ? null : prey, prey_population); return functional.filter(fn(prey) => prey.energy > 0, processed); }")

        # Test with sample data
        repl.set_variable('prey_data', [
            {'energy': 15, 'name': 'prey1'},
            {'energy': 5, 'name': 'prey2'},  # This will become None after map
            {'energy': 20, 'name': 'prey3'}
        ])

        # This SHOULD fail with an error about accessing .energy on None
        repl.assert_ml_error("processBuggyPattern(prey_data)", "NoneType.*energy")

    def test_ecosystem_prey_behavior_pattern(self):
        """Test ecosystem pattern that maps to null then tries to filter - should error."""
        repl = REPLTestHelper()

        repl.execute_ml("import functional;")
        repl.execute_ml("function processPreyBehavior(prey_population, predator_population, environment, time_step) { alive_prey = functional.filter(fn(prey) => prey.energy > 0, prey_population); processed_prey = functional.map(fn(prey_individual) => null, alive_prey); return functional.filter(fn(prey) => prey.energy > 0, processed_prey); }")

        repl.set_variable('prey_data', [
            {'energy': 50, 'state': 'grazing'},
            {'energy': 30, 'state': 'fleeing'},
            {'energy': 80, 'state': 'grazing'}
        ])

        # This pattern is buggy - maps everything to null, then tries to access .energy on null
        repl.assert_ml_error("processPreyBehavior(prey_data, [], {}, 0.1)", "NoneType.*energy")

    def test_multistatement_function_in_map(self):
        """Test arrow function with expression in map."""
        repl = REPLTestHelper()

        repl.execute_ml("import functional;")
        repl.execute_ml("function processItems(items) { result = functional.map(fn(item) => (item * 2) + 1, items); return result; }")

        repl.set_variable('items', [1, 2, 3, 4, 5])

        result = repl.execute_ml("processItems(items)")

        # Should successfully process items
        assert result == [3, 5, 7, 9, 11], f"Expected [3, 5, 7, 9, 11], got {result}"

    def test_ecosystem_processPreyBehavior_pattern(self):
        """Test the exact pattern from ecosystem processPreyBehavior function."""
        repl = REPLTestHelper()

        repl.execute_ml("import functional;")

        repl.execute_ml("function updatePrey(prey_individual, time_step) { updated_prey = prey_individual; updated_prey.energy = updated_prey.energy - 1; updated_prey.age = updated_prey.age + time_step; return updated_prey; }")

        repl.execute_ml("function processPreyBehavior(prey_population, predators, environment, time_step) { alive_prey = functional.filter(fn(prey) => prey.energy > 0, prey_population); processed_prey = functional.map(fn(prey_individual) => updatePrey(prey_individual, time_step), alive_prey); return functional.filter(fn(prey) => prey.energy > 0, processed_prey); }")

        repl.set_variable('prey_data', [
            {'energy': 50, 'age': 1},
            {'energy': 1, 'age': 2},   # Will have 0 energy after update
            {'energy': 80, 'age': 3}
        ])

        result = repl.execute_ml("processPreyBehavior(prey_data, [], {}, 0.1)")

        # Should filter out prey with 0 or negative energy after update
        assert len(result) == 2, f"Expected 2 prey to survive, got {len(result)}"

    def test_none_safe_property_access(self):
        """Test that filtering None values before accessing properties works correctly."""
        repl = REPLTestHelper()

        repl.execute_ml("import functional;")
        repl.execute_ml("function safeProcess(items) { valid_items = functional.filter(fn(x) => x != null, items); return functional.map(fn(item) => item.value, valid_items); }")

        repl.set_variable('test_data', [
            {'value': 10},
            None,
            {'value': 20},
            None,
            {'value': 30}
        ])

        result = repl.execute_ml("safeProcess(test_data)")

        # Should successfully process only non-None items
        assert result == [10, 20, 30], f"Expected [10, 20, 30], got {result}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
