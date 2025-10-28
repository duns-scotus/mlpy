#!/usr/bin/env python3
"""Unit tests for lambda expressions with undefined variables."""

import pytest

from tests.helpers.repl_test_helper import REPLTestHelper


class TestLambdaUndefinedVariable:
    """Test that lambda expressions don't reference undefined variables."""

    def test_simple_undefined_variable_in_lambda(self):
        """Test arrow function that references undefined variable."""
        repl = REPLTestHelper()

        repl.execute_ml("import functional;")
        repl.execute_ml("function test() { items = [1, 2, 3]; result = functional.filter(fn(item) => item > threshold, items); return result; }")

        # This should fail at runtime because threshold is not defined
        repl.assert_ml_error("test()", "threshold.*not defined")

    def test_ecosystem_distance_pattern(self):
        """Test the exact pattern from ecosystem preyAvoidPredators."""
        repl = REPLTestHelper()

        repl.execute_ml("import functional;")
        repl.execute_ml("function preyAvoidPredators(prey, predators) { nearby_predators = functional.filter(fn(predator) => distance <= prey.detection_range, predators); return prey; }")

        repl.set_variable('prey_data', {'detection_range': 25})
        repl.set_variable('predator_data', [{'position': {'x': 10, 'y': 10}}, {'position': {'x': 50, 'y': 50}}])

        # This should fail because distance is not defined
        repl.assert_ml_error("preyAvoidPredators(prey_data, predator_data)", "distance.*not defined")

    def test_missing_distance_calculation(self):
        """Test pattern where distance calculation is in arrow function."""
        repl = REPLTestHelper()

        repl.execute_ml("import functional;")
        repl.execute_ml("import math;")
        repl.execute_ml("function calculateDistance(pos1, pos2) { dx = pos1.x - pos2.x; dy = pos1.y - pos2.y; return math.sqrt(dx * dx + dy * dy); }")
        repl.execute_ml("function findNearbyItems(items, center, max_distance) { nearby = functional.filter(fn(item) => calculateDistance(item.position, center) <= max_distance, items); return nearby; }")

        repl.set_variable('items', [
            {'position': {'x': 0, 'y': 0}},
            {'position': {'x': 5, 'y': 5}},
            {'position': {'x': 100, 'y': 100}}
        ])
        repl.set_variable('center', {'x': 0, 'y': 0})

        result = repl.execute_ml("findNearbyItems(items, center, 10)")

        # Should find items within distance 10
        assert len(result) >= 1, f"Expected to find nearby items, got {result}"

    def test_lambda_with_missing_function_call(self):
        """Test arrow function that references undefined variable instead of calling function."""
        repl = REPLTestHelper()

        repl.execute_ml("import functional;")
        repl.execute_ml("function getScore(item) { return item.value * 2; }")
        repl.execute_ml("function processItems(items) { highScore = functional.filter(fn(item) => score > 10, items); return highScore; }")

        repl.set_variable('items', [{'value': 5}, {'value': 10}, {'value': 15}])

        # This should fail because score is not defined (should be getScore(item) > 10)
        repl.assert_ml_error("processItems(items)", "score.*not defined")

    def test_complex_ecosystem_predator_pattern(self):
        """Test the full ecosystem pattern with arrow function."""
        repl = REPLTestHelper()

        repl.execute_ml("import functional;")
        repl.execute_ml("import math;")
        repl.execute_ml("function calculateDistance(pos1, pos2) { dx = pos1.x - pos2.x; dy = pos1.y - pos2.y; return math.sqrt(dx * dx + dy * dy); }")
        repl.execute_ml("function preyAvoidPredators(prey, predators) { nearby_predators = functional.filter(fn(predator) => calculateDistance(predator.position, prey.position) <= prey.detection_range, predators); updated_prey = prey; if (nearby_predators.length > 0) { updated_prey.state = 'fleeing'; updated_prey.fear_level = math.min(1.0, updated_prey.fear_level + 0.3); } return updated_prey; }")

        repl.set_variable('prey_data', {
            'position': {'x': 0, 'y': 0},
            'detection_range': 25,
            'state': 'grazing',
            'fear_level': 0.0
        })
        repl.set_variable('predator_data', [
            {'position': {'x': 10, 'y': 10}},  # Close predator
            {'position': {'x': 100, 'y': 100}}  # Far predator
        ])

        result = repl.execute_ml("preyAvoidPredators(prey_data, predator_data)")

        # Should detect close predator and change state to fleeing
        assert result['state'] == 'fleeing', f"Expected state 'fleeing', got {result['state']}"

    def test_variable_used_but_not_declared_in_scope(self):
        """Test general pattern where variable is used from outer scope in arrow function."""
        repl = REPLTestHelper()

        repl.execute_ml("import functional;")
        repl.execute_ml("function test() { items = [1, 2, 3, 4, 5]; threshold = 3; filtered = functional.filter(fn(item) => item > threshold, items); return filtered; }")

        result = repl.execute_ml("test()")

        # This should work - threshold is defined in outer scope and closures should capture it
        assert result == [4, 5], f"Expected [4, 5], got {result}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
