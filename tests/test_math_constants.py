#!/usr/bin/env python3
"""Unit tests for Math module constants and functions."""

import pytest
from mlpy.ml.transpiler import transpile_ml_code


class TestMathConstants:
    """Test that Math module constants are available and work correctly."""

    def _setup_execution_environment(self):
        """Set up the execution environment for generated code to access mlpy modules."""
        import sys
        import os

        # Add the source directory to the path for this test
        src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
        if src_path not in sys.path:
            sys.path.insert(0, os.path.abspath(src_path))

    def test_math_pi_constant(self):
        """Test that math.pi is available and transpiles correctly."""
        ml_code = """
        import math;

        function test() {
            circumference = 2 * math.pi * 5;  // radius = 5
            return circumference;
        }
        """

        result = transpile_ml_code(ml_code, "test_math_pi.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        if generated_code is None:
            pytest.fail("Transpiler failed for math.pi usage")

        # Should be syntactically valid
        try:
            compile(generated_code, "test", "exec")
        except SyntaxError as e:
            pytest.fail(f"Generated code has syntax error: {e}")

        # Should execute without AttributeError
        try:
            # Set up execution environment
            self._setup_execution_environment()

            # The generated code already has the correct imports, just run it
            test_code = generated_code + """
result = test()
expected = 2 * 3.14159 * 5  # approximately 31.4159
print(f"Circumference: {result}")
assert abs(result - expected) < 0.01, f"Expected ~{expected}, got {result}"
"""
            # Execute in global namespace to allow imports to work
            global_namespace = {}
            local_namespace = {}
            exec(test_code, global_namespace, local_namespace)
        except AttributeError as e:
            if "'Math' object has no attribute 'pi'" in str(e):
                pytest.fail(f"Math.pi not available: {e}\n\nGenerated code:\n{generated_code}")
            else:
                raise e

    def test_math_e_constant(self):
        """Test that math.e (Euler's number) is available."""
        ml_code = """
        import math;

        function test() {
            exponential = math.e * 2;
            return exponential;
        }
        """

        result = transpile_ml_code(ml_code, "test_math_e.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        if generated_code is None:
            pytest.fail("Transpiler failed for math.e usage")

        # Should execute without AttributeError
        try:
            # Set up execution environment
            self._setup_execution_environment()

            import math as _math_module  # Standard library math for verification
            test_code = generated_code + """
result = test()
expected = _math_module.e * 2  # approximately 5.436564
print(f"Exponential: {result}")
assert abs(result - expected) < 0.01, f"Expected ~{expected}, got {result}"
"""
            exec(test_code)
        except AttributeError as e:
            if "'Math' object has no attribute 'e'" in str(e):
                pytest.fail(f"Math.e not available: {e}")

    def test_ecosystem_angle_calculation_pattern(self):
        """Test the exact pattern from ecosystem simulation that's failing."""
        ml_code = """
        import math;
        import random;

        function preyMove(prey, time_step) {
            new_position = {};
            new_position.x = prey.position.x;
            new_position.y = prey.position.y;

            // This is the line that fails in ecosystem simulation
            angle = random.randomFloat(0, 2 * math.pi);
            speed_multiplier = prey.state == "fleeing" ? 2.0 : 1.0;
            distance = prey.speed * speed_multiplier * time_step;

            new_position.x = new_position.x + math.cos(angle) * distance;
            new_position.y = new_position.y + math.sin(angle) * distance;

            return new_position;
        }
        """

        result = transpile_ml_code(ml_code, "test_ecosystem_math.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        if generated_code is None:
            pytest.fail("Ecosystem math pattern transpilation failed")

        # Should be syntactically valid
        try:
            compile(generated_code, "test", "exec")
        except SyntaxError as e:
            pytest.fail(f"Generated ecosystem math code has syntax error: {e}")

        # Critical test: should execute without Math.pi AttributeError
        try:
            # Set up execution environment
            self._setup_execution_environment()

            test_code = generated_code + """
# Test with sample prey data
prey_data = {
    'x': 10.0,
    'y': 5.0,
    'speed': 1.5
}
result = preyMove(prey_data, 0.1)
print(f"Success: new position = ({result['x']:.2f}, {result['y']:.2f})")
"""
            exec(test_code)
        except AttributeError as e:
            if "'Math' object has no attribute 'pi'" in str(e):
                pytest.fail(f"Ecosystem math.pi error: {e}\n\nGenerated code:\n{generated_code}")
            else:
                raise e

    def test_math_trigonometric_functions(self):
        """Test that math trigonometric functions work with constants."""
        ml_code = """
        import math;

        function test() {
            // Test sin, cos with pi/2
            half_pi = math.pi / 2;
            sin_result = math.sin(half_pi);  // Should be ~1
            cos_result = math.cos(half_pi);  // Should be ~0

            result = {};
            result.sin = sin_result;
            result.cos = cos_result;
            return result;
        }
        """

        result = transpile_ml_code(ml_code, "test_math_trig.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        if generated_code is None:
            pytest.fail("Math trigonometric functions transpilation failed")

        # Should execute successfully
        try:
            # Set up execution environment
            self._setup_execution_environment()

            test_code = generated_code + """
result = test()
print(f"sin(π/2) = {result['sin']:.3f}, cos(π/2) = {result['cos']:.3f}")
assert abs(result['sin'] - 1.0) < 0.01, f"sin(π/2) should be ~1, got {result['sin']}"
assert abs(result['cos']) < 0.01, f"cos(π/2) should be ~0, got {result['cos']}"
"""
            exec(test_code)
        except AttributeError as e:
            if "pi" in str(e) or "sin" in str(e) or "cos" in str(e):
                pytest.fail(f"Math function/constant error: {e}")

    def test_math_constants_in_expressions(self):
        """Test math constants used in complex expressions."""
        ml_code = """
        import math;

        function calculateCircleArea(radius) {
            area = math.pi * radius * radius;
            return area;
        }

        function test() {
            areas = [];
            radii = [1, 2, 3, 5];

            i = 0;
            while (i < radii.length) {
                radius = radii[i];
                area = calculateCircleArea(radius);
                areas = areas.concat([area]);
                i = i + 1;
            }

            return areas;
        }
        """

        result = transpile_ml_code(ml_code, "test_math_expressions.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        if generated_code is None:
            pytest.fail("Math constants in expressions transpilation failed")

        # Should execute successfully
        try:
            # Set up execution environment
            self._setup_execution_environment()

            import math as _math_module  # Standard library math for verification
            test_code = generated_code + """
areas = test()
print(f"Circle areas: {areas}")
# Check first area (radius=1): π * 1^2 = π ≈ 3.14159
assert abs(areas[0] - _math_module.pi) < 0.01, f"Area of radius 1 should be ~π, got {areas[0]}"
"""
            exec(test_code)
        except AttributeError as e:
            if "pi" in str(e):
                pytest.fail(f"Math.pi in expression error: {e}")

    def test_all_common_math_constants(self):
        """Test that all commonly needed math constants are available."""
        ml_code = """
        import math;

        function test() {
            constants = {};
            constants.pi = math.pi;
            constants.e = math.e;
            // Add more constants as needed
            return constants;
        }
        """

        result = transpile_ml_code(ml_code, "test_all_constants.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        if generated_code is None:
            pytest.fail("All math constants transpilation failed")

        # Should execute successfully with all constants
        try:
            # Set up execution environment
            self._setup_execution_environment()

            import math as _math_module  # Standard library math for verification
            test_code = generated_code + """
constants = test()
print(f"Available constants: {list(constants.keys())}")
assert 'pi' in constants, "math.pi should be available"
assert 'e' in constants, "math.e should be available"
assert abs(constants['pi'] - _math_module.pi) < 0.01, f"pi should be ~{_math_module.pi}, got {constants['pi']}"
assert abs(constants['e'] - _math_module.e) < 0.01, f"e should be ~{_math_module.e}, got {constants['e']}"
"""
            exec(test_code)
        except AttributeError as e:
            pytest.fail(f"Math constants availability error: {e}")

    def test_math_functions_with_constants(self):
        """Test that math functions work correctly with constants."""
        ml_code = """
        import math;

        function test() {
            results = {};

            // Test functions that commonly use constants
            results.sqrt_pi = math.sqrt(math.pi);
            results.log_e = math.log(math.e);  // Should be 1
            results.pow_e_2 = math.pow(math.e, 2);

            return results;
        }
        """

        result = transpile_ml_code(ml_code, "test_math_funcs_constants.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        if generated_code is None:
            pytest.fail("Math functions with constants transpilation failed")

        # Should execute successfully
        try:
            # Set up execution environment
            self._setup_execution_environment()

            import math as _math_module  # Standard library math for verification
            test_code = generated_code + """
results = test()
print(f"Math function results: {results}")
assert abs(results['log_e'] - 1.0) < 0.01, f"log(e) should be 1, got {results['log_e']}"
assert abs(results['sqrt_pi'] - _math_module.sqrt(_math_module.pi)) < 0.01, f"sqrt(π) should be ~{_math_module.sqrt(_math_module.pi):.3f}, got {results['sqrt_pi']}"
"""
            exec(test_code)
        except AttributeError as e:
            pytest.fail(f"Math functions with constants error: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])