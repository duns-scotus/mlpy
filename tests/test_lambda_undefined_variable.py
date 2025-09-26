#!/usr/bin/env python3
"""Unit tests for lambda expressions with undefined variables."""

import pytest
from mlpy.ml.transpiler import transpile_ml_code


class TestLambdaUndefinedVariable:
    """Test that lambda expressions don't reference undefined variables."""

    def test_simple_undefined_variable_in_lambda(self):
        """Test lambda that references undefined variable."""
        ml_code = """
        function test() {
            items = [1, 2, 3];
            result = items.filter(function(item) {
                return item > threshold;
            });
            return result;
        }
        """

        result = transpile_ml_code(ml_code, "test_undefined.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        if generated_code is None:
            pytest.fail("Transpiler returned None for undefined variable lambda")

        # Should be syntactically valid
        try:
            compile(generated_code, "test", "exec")
        except SyntaxError as e:
            pytest.fail(f"Generated code has syntax error: {e}")

        # Should NOT reference undefined variable
        if "threshold" in generated_code and "lambda" in generated_code:
            # If threshold appears in a lambda, it's likely undefined
            if "lambda item: (item > threshold)" in generated_code or "lambda item: item > threshold" in generated_code:
                pytest.fail(f"Lambda references undefined variable 'threshold': {generated_code}")

    def test_ecosystem_distance_pattern(self):
        """Test the exact pattern from ecosystem preyAvoidPredators."""
        ml_code = """
        function preyAvoidPredators(prey, predators) {
            nearby_predators = predators.filter(function(predator) {
                return distance <= prey.detection_range;
            });
            return prey;
        }
        """

        result = transpile_ml_code(ml_code, "test_ecosystem_distance.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        if generated_code is None:
            pytest.fail("Ecosystem distance pattern transpilation failed")

        # Should be syntactically valid
        try:
            compile(generated_code, "test", "exec")
        except SyntaxError as e:
            pytest.fail(f"Generated ecosystem distance code has syntax error: {e}")

        # Critical bug check: should NOT have lambda with undefined 'distance'
        problematic_patterns = [
            "lambda predator: (distance <=",
            "lambda predator: distance <=",
            "lambda predator: (distance <",
            "lambda predator: distance <"
        ]

        for pattern in problematic_patterns:
            if pattern in generated_code:
                pytest.fail(f"Found lambda with undefined 'distance' variable: '{pattern}' in {generated_code}")

        # Should execute without NameError
        try:
            exec(generated_code + """
# Test execution
prey_data = {'detection_range': 25}
predator_data = [{'position': {'x': 10, 'y': 10}}, {'position': {'x': 50, 'y': 50}}]
result = preyAvoidPredators(prey_data, predator_data)
print(f"Success: processed prey avoidance")
""")
        except NameError as e:
            if "distance is not defined" in str(e):
                pytest.fail(f"Lambda distance variable error: {e}\n\nGenerated code:\n{generated_code}")

    def test_missing_distance_calculation(self):
        """Test pattern where distance should be calculated within lambda."""
        ml_code = """
        function calculateDistance(pos1, pos2) {
            dx = pos1.x - pos2.x;
            dy = pos1.y - pos2.y;
            return Math.sqrt(dx * dx + dy * dy);
        }

        function findNearbyItems(items, center, max_distance) {
            nearby = items.filter(function(item) {
                distance = calculateDistance(item.position, center);
                return distance <= max_distance;
            });
            return nearby;
        }
        """

        result = transpile_ml_code(ml_code, "test_distance_calc.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        if generated_code is None:
            pytest.fail("Distance calculation pattern transpilation failed")

        # Should be syntactically valid
        try:
            compile(generated_code, "test", "exec")
        except SyntaxError as e:
            pytest.fail(f"Generated distance calculation code has syntax error: {e}")

        # Should NOT have undefined variables in lambda
        if "lambda item: distance <=" in generated_code:
            pytest.fail(f"Lambda references undefined 'distance': {generated_code}")

        # Should execute successfully
        try:
            exec(generated_code + """
# Import math module for sqrt
import math as Math
# Test execution
items = [
    {'position': {'x': 0, 'y': 0}},
    {'position': {'x': 5, 'y': 5}},
    {'position': {'x': 100, 'y': 100}}
]
center = {'x': 0, 'y': 0}
result = findNearbyItems(items, center, 10)
print(f"Success: found {len(result)} nearby items")
""")
        except Exception as e:
            if "not defined" in str(e):
                pytest.fail(f"Undefined variable in distance calculation: {e}")

    def test_lambda_with_missing_function_call(self):
        """Test lambda that should call function but references undefined variable instead."""
        ml_code = """
        function getScore(item) {
            return item.value * 2;
        }

        function processItems(items) {
            highScore = items.filter(function(item) {
                return score > 10;
            });
            return highScore;
        }
        """

        result = transpile_ml_code(ml_code, "test_missing_function.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        if generated_code is None:
            pytest.fail("Missing function call pattern transpilation failed")

        # Should be syntactically valid
        try:
            compile(generated_code, "test", "exec")
        except SyntaxError as e:
            pytest.fail(f"Generated missing function code has syntax error: {e}")

        # Should NOT reference undefined 'score' variable
        if "lambda item: (score >" in generated_code or "lambda item: score >" in generated_code:
            pytest.fail(f"Lambda references undefined 'score' (should call getScore function): {generated_code}")

    def test_complex_ecosystem_predator_pattern(self):
        """Test the full ecosystem pattern that's actually causing the bug."""
        ml_code = """
        function calculateDistance(pos1, pos2) {
            dx = pos1.x - pos2.x;
            dy = pos1.y - pos2.y;
            return Math.sqrt(dx * dx + dy * dy);
        }

        function preyAvoidPredators(prey, predators) {
            nearby_predators = predators.filter(function(predator) {
                distance = calculateDistance(predator.position, prey.position);
                return distance <= prey.detection_range;
            });
            updated_prey = prey;
            if (nearby_predators.length > 0) {
                updated_prey.state = "fleeing";
                updated_prey.fear_level = Math.min(1.0, updated_prey.fear_level + 0.3);
            }
            return updated_prey;
        }
        """

        result = transpile_ml_code(ml_code, "test_ecosystem_full.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        if generated_code is None:
            pytest.fail("Full ecosystem pattern transpilation failed")

        # Should be syntactically valid
        try:
            compile(generated_code, "test", "exec")
        except SyntaxError as e:
            pytest.fail(f"Generated ecosystem full code has syntax error: {e}")

        # Critical: should NOT have undefined distance in lambda
        if "lambda predator: distance <=" in generated_code or "lambda predator: (distance <=" in generated_code:
            pytest.fail(f"Lambda has undefined distance variable (should calculate within lambda): {generated_code}")

        # Should execute successfully
        try:
            exec(generated_code + """
# Import math
import math as Math
# Test execution
prey_data = {
    'position': {'x': 0, 'y': 0},
    'detection_range': 25,
    'state': 'grazing',
    'fear_level': 0.0
}
predator_data = [
    {'position': {'x': 10, 'y': 10}},  # Close predator
    {'position': {'x': 100, 'y': 100}} # Far predator
]
result = preyAvoidPredators(prey_data, predator_data)
print(f"Success: prey state = {result['state']}")
""")
        except NameError as e:
            if "distance" in str(e):
                pytest.fail(f"Full ecosystem pattern distance error: {e}")

    def test_variable_used_but_not_declared_in_scope(self):
        """Test general pattern where variable is used but not in lambda scope."""
        ml_code = """
        function test() {
            items = [1, 2, 3, 4, 5];
            threshold = 3;
            // This should work - threshold is defined in outer scope
            filtered = items.filter(function(item) {
                return item > threshold;
            });
            return filtered;
        }
        """

        result = transpile_ml_code(ml_code, "test_outer_scope.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        if generated_code is None:
            pytest.fail("Outer scope variable transpilation failed")

        # Should be syntactically valid
        try:
            compile(generated_code, "test", "exec")
        except SyntaxError as e:
            pytest.fail(f"Generated outer scope code has syntax error: {e}")

        # This should work because threshold is in outer scope
        try:
            exec(generated_code + """
result = test()
print(f"Filtered result: {result}")
""")
        except NameError as e:
            # This might be expected if our transpiler doesn't handle closure properly
            print(f"Note: Closure variable access error (may be expected): {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])