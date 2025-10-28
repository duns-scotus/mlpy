"""Unit tests for math_bridge module migration."""

import pytest
import math as py_math
from mlpy.stdlib.math_bridge import Math, math
from mlpy.stdlib.decorators import get_module_metadata
from mlpy.stdlib.module_registry import get_registry


class TestMathModuleRegistration:
    """Test that Math module is properly registered."""

    def test_math_module_registered(self):
        """Test that math module is available in registry."""
        registry = get_registry()
        assert registry.is_available("math")
        math_instance = registry.get_module("math")
        assert math_instance is not None
        assert type(math_instance).__name__ == "Math"

    def test_math_module_metadata(self):
        """Test math module metadata is correct."""
        metadata = get_module_metadata("math")
        assert metadata is not None
        assert metadata.name == "math"
        assert metadata.description == "Mathematical operations and constants"
        assert "math.compute" in metadata.capabilities
        assert metadata.version == "1.0.0"

    def test_math_has_function_metadata(self):
        """Test that math module has registered functions."""
        metadata = get_module_metadata("math")

        # Check key methods are registered
        assert "sqrt" in metadata.functions
        assert "abs" in metadata.functions
        assert "sin" in metadata.functions
        assert "cos" in metadata.functions
        assert "tan" in metadata.functions
        assert "ln" in metadata.functions
        assert "log" in metadata.functions
        assert "exp" in metadata.functions
        assert "pow" in metadata.functions
        assert "floor" in metadata.functions
        assert "ceil" in metadata.functions
        assert "round" in metadata.functions
        assert "min" in metadata.functions
        assert "max" in metadata.functions

        # Should have 27 functions
        assert len(metadata.functions) == 27

    def test_math_function_capabilities(self):
        """Test that math functions have correct capabilities."""
        metadata = get_module_metadata("math")

        # All math functions require math.compute
        assert metadata.functions["sqrt"].capabilities == ["math.compute"]
        assert metadata.functions["sin"].capabilities == ["math.compute"]
        assert metadata.functions["pow"].capabilities == ["math.compute"]


class TestMathBasicOperations:
    """Test basic mathematical operations."""

    def test_sqrt(self):
        """Test square root function."""
        assert math.sqrt(4) == 2.0
        assert math.sqrt(9) == 3.0
        assert math.sqrt(0) == 0.0

    def test_sqrt_negative(self):
        """Test square root of negative returns 0."""
        assert math.sqrt(-1) == 0

    def test_abs(self):
        """Test absolute value function."""
        assert math.abs(5) == 5
        assert math.abs(-5) == 5
        assert math.abs(0) == 0

    def test_pow(self):
        """Test power function."""
        assert math.pow(2, 3) == 8
        assert math.pow(5, 2) == 25
        assert math.pow(10, 0) == 1

    def test_exp(self):
        """Test exponential function."""
        result = math.exp(1)
        assert abs(result - py_math.e) < 0.0001


class TestMathTrigonometry:
    """Test trigonometric functions."""

    def test_sin(self):
        """Test sine function."""
        assert abs(math.sin(0)) < 0.0001
        assert abs(math.sin(py_math.pi / 2) - 1) < 0.0001

    def test_cos(self):
        """Test cosine function."""
        assert abs(math.cos(0) - 1) < 0.0001
        assert abs(math.cos(py_math.pi)) - 1 < 0.0001

    def test_tan(self):
        """Test tangent function."""
        assert abs(math.tan(0)) < 0.0001
        assert abs(math.tan(py_math.pi / 4) - 1) < 0.0001


class TestMathLogarithms:
    """Test logarithmic functions."""

    def test_ln(self):
        """Test natural logarithm."""
        assert abs(math.ln(py_math.e) - 1) < 0.0001
        assert abs(math.ln(1)) < 0.0001

    def test_ln_invalid(self):
        """Test ln with invalid input returns error value."""
        assert math.ln(0) == -999
        assert math.ln(-1) == -999

    def test_log(self):
        """Test logarithm with base."""
        assert abs(math.log(100, 10) - 2) < 0.0001
        assert abs(math.log(8, 2) - 3) < 0.0001

    def test_log_invalid(self):
        """Test log with invalid input returns error value."""
        assert math.log(0, 10) == -999
        assert math.log(-1, 10) == -999
        assert math.log(10, 0) == -999


class TestMathRounding:
    """Test rounding functions."""

    def test_floor(self):
        """Test floor function."""
        assert math.floor(4.9) == 4
        assert math.floor(4.1) == 4
        assert math.floor(-4.1) == -5

    def test_ceil(self):
        """Test ceiling function."""
        assert math.ceil(4.1) == 5
        assert math.ceil(4.9) == 5
        assert math.ceil(-4.9) == -4

    def test_round(self):
        """Test rounding function."""
        assert math.round(4.5) == 4  # Python's round uses banker's rounding
        assert math.round(4.6) == 5
        assert math.round(4.4) == 4


class TestMathMinMax:
    """Test min/max functions."""

    def test_min(self):
        """Test minimum function."""
        assert math.min(5, 10) == 5
        assert math.min(-5, -10) == -10
        assert math.min(0, 0) == 0

    def test_max(self):
        """Test maximum function."""
        assert math.max(5, 10) == 10
        assert math.max(-5, -10) == -5
        assert math.max(0, 0) == 0


class TestMathAngleConversion:
    """Test angle conversion functions."""

    def test_deg_to_rad(self):
        """Test degrees to radians conversion."""
        assert abs(math.degToRad(180) - py_math.pi) < 0.0001
        assert abs(math.degToRad(90) - py_math.pi / 2) < 0.0001
        assert abs(math.degToRad(0)) < 0.0001

    def test_rad_to_deg(self):
        """Test radians to degrees conversion."""
        assert abs(math.radToDeg(py_math.pi) - 180) < 0.0001
        assert abs(math.radToDeg(py_math.pi / 2) - 90) < 0.0001
        assert abs(math.radToDeg(0)) < 0.0001


class TestMathConstants:
    """Test mathematical constants."""

    def test_pi_constant(self):
        """Test pi constant availability."""
        assert Math.pi == py_math.pi

    def test_e_constant(self):
        """Test e constant availability."""
        assert Math.e == py_math.e


class TestMathInstance:
    """Test global math instance."""

    def test_math_is_instance_of_math_class(self):
        """Test that math is an instance of Math."""
        assert isinstance(math, Math)

    def test_math_has_decorated_methods(self):
        """Test that math instance has decorated methods with metadata."""
        assert hasattr(math, "sqrt")
        assert hasattr(math, "sin")
        assert hasattr(math, "pow")

        # Check they have metadata
        assert hasattr(math.sqrt, "_ml_function_metadata")
        assert hasattr(math.sin, "_ml_function_metadata")
        assert hasattr(math.pow, "_ml_function_metadata")


class TestMathRandom:
    """Test random function."""

    def test_random_range(self):
        """Test random returns value in [0, 1)."""
        for _ in range(10):
            value = math.random()
            assert 0 <= value < 1


class TestMathErrorHandling:
    """Test error handling in math functions."""

    def test_exp_overflow(self):
        """Test exp returns inf on overflow."""
        result = math.exp(1000)  # Very large exponent causes overflow
        assert result == float("inf")

    def test_pow_overflow_positive(self):
        """Test pow returns inf on overflow with positive base."""
        # Python's pow can handle very large integers, so use float to trigger overflow
        result = math.pow(10.0, 10000)  # Very large power with float
        assert result == float("inf")

    def test_pow_zero_division(self):
        """Test pow handles zero division."""
        # Negative exponent with zero base causes ZeroDivisionError
        result = math.pow(0, -1)
        assert result == 0

    def test_factorial_negative(self):
        """Test factorial of negative number returns 0."""
        assert math.factorial(-1) == 0
        assert math.factorial(-5) == 0


class TestMathAdvancedTrig:
    """Test advanced trigonometric functions."""

    def test_asin(self):
        """Test arcsine function."""
        assert abs(math.asin(0)) < 0.0001
        assert abs(math.asin(1) - py_math.pi / 2) < 0.0001
        assert abs(math.asin(-1) + py_math.pi / 2) < 0.0001

    def test_acos(self):
        """Test arccosine function."""
        assert abs(math.acos(1)) < 0.0001
        assert abs(math.acos(0) - py_math.pi / 2) < 0.0001
        assert abs(math.acos(-1) - py_math.pi) < 0.0001

    def test_atan(self):
        """Test arctangent function."""
        assert abs(math.atan(0)) < 0.0001
        assert abs(math.atan(1) - py_math.pi / 4) < 0.0001

    def test_atan2(self):
        """Test two-argument arctangent."""
        assert abs(math.atan2(1, 1) - py_math.pi / 4) < 0.0001
        assert abs(math.atan2(1, 0) - py_math.pi / 2) < 0.0001
        assert abs(math.atan2(0, 1)) < 0.0001


class TestMathConversion:
    """Test angle conversion functions."""

    def test_radians(self):
        """Test radians conversion function."""
        result = math.radians(180)
        assert abs(result - py_math.pi) < 0.0001
        assert abs(math.radians(90) - py_math.pi / 2) < 0.0001

    def test_degrees(self):
        """Test degrees conversion function."""
        result = math.degrees(py_math.pi)
        assert abs(result - 180) < 0.0001
        assert abs(math.degrees(py_math.pi / 2) - 90) < 0.0001


class TestMathSign:
    """Test sign function."""

    def test_sign_positive(self):
        """Test sign of positive number."""
        assert math.sign(5) == 1
        assert math.sign(0.5) == 1
        assert math.sign(100) == 1

    def test_sign_negative(self):
        """Test sign of negative number."""
        assert math.sign(-5) == -1
        assert math.sign(-0.5) == -1
        assert math.sign(-100) == -1

    def test_sign_zero(self):
        """Test sign of zero."""
        assert math.sign(0) == 0
        assert math.sign(0.0) == 0


class TestMathNumberTheory:
    """Test number theory functions."""

    def test_gcd(self):
        """Test greatest common divisor."""
        assert math.gcd(12, 8) == 4
        assert math.gcd(21, 14) == 7
        assert math.gcd(17, 19) == 1  # Coprime numbers

    def test_lcm(self):
        """Test least common multiple."""
        assert math.lcm(12, 8) == 24
        assert math.lcm(21, 14) == 42
        assert math.lcm(5, 7) == 35


class TestMathHelperFunctions:
    """Test helper functions for ML bridge."""

    def test_sqrt_helper(self):
        """Test sqrt helper function."""
        from mlpy.stdlib.math_bridge import sqrt_helper

        assert sqrt_helper(16) == 4.0
        assert sqrt_helper(25) == 5.0

    def test_abs_helper(self):
        """Test abs helper function."""
        from mlpy.stdlib.math_bridge import abs_helper

        assert abs_helper(-10) == 10
        assert abs_helper(10) == 10

    def test_min_helper(self):
        """Test min helper function."""
        from mlpy.stdlib.math_bridge import min_helper

        assert min_helper(5, 10) == 5
        assert min_helper(10, 5) == 5

    def test_max_helper(self):
        """Test max helper function."""
        from mlpy.stdlib.math_bridge import max_helper

        assert max_helper(5, 10) == 10
        assert max_helper(10, 5) == 10
