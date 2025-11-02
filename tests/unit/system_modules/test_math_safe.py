"""
Tests for math_safe module - capability-controlled math operations.
"""

import math
import pytest
from unittest.mock import patch

from mlpy.runtime.capabilities.exceptions import CapabilityNotFoundError
from mlpy.runtime.system_modules.math_safe import SafeMath, math_safe


class TestSafeMathWithCapability:
    """Test SafeMath operations with proper capability."""

    @pytest.fixture
    def math_capability(self):
        """Mock math capability."""
        with patch('mlpy.runtime.capabilities.decorators.has_capability', return_value=True):
            yield

    def test_sqrt(self, math_capability):
        """Test square root calculation."""
        result = math_safe.sqrt(16)
        assert result == 4.0

    def test_pow(self, math_capability):
        """Test power calculation."""
        result = math_safe.pow(2, 3)
        assert result == 8.0

    def test_sin(self, math_capability):
        """Test sine calculation."""
        result = math_safe.sin(0)
        assert result == 0.0

    def test_cos(self, math_capability):
        """Test cosine calculation."""
        result = math_safe.cos(0)
        assert result == 1.0

    def test_tan(self, math_capability):
        """Test tangent calculation."""
        result = math_safe.tan(0)
        assert result == 0.0

    def test_log_default_base(self, math_capability):
        """Test logarithm with default base (e)."""
        result = math_safe.log(math.e)
        assert abs(result - 1.0) < 1e-10

    def test_log_custom_base(self, math_capability):
        """Test logarithm with custom base."""
        result = math_safe.log(100, 10)
        assert abs(result - 2.0) < 1e-10

    def test_exp(self, math_capability):
        """Test exponential calculation."""
        result = math_safe.exp(0)
        assert result == 1.0

    def test_factorial(self, math_capability):
        """Test factorial calculation."""
        assert math_safe.factorial(0) == 1
        assert math_safe.factorial(5) == 120

    def test_factorial_invalid_negative(self, math_capability):
        """Test factorial with negative number."""
        with pytest.raises(ValueError, match="non-negative integer"):
            math_safe.factorial(-1)

    def test_factorial_invalid_float(self, math_capability):
        """Test factorial with float."""
        with pytest.raises(ValueError, match="non-negative integer"):
            math_safe.factorial(3.5)

    def test_floor(self, math_capability):
        """Test floor function."""
        assert math_safe.floor(3.7) == 3
        assert math_safe.floor(-3.2) == -4

    def test_ceil(self, math_capability):
        """Test ceiling function."""
        assert math_safe.ceil(3.2) == 4
        assert math_safe.ceil(-3.7) == -3

    def test_abs(self, math_capability):
        """Test absolute value."""
        assert math_safe.abs(-5) == 5
        assert math_safe.abs(5) == 5
        assert math_safe.abs(-3.5) == 3.5

    def test_min(self, math_capability):
        """Test minimum function."""
        assert math_safe.min(1, 2, 3) == 1
        assert math_safe.min(5, -2, 10) == -2

    def test_max(self, math_capability):
        """Test maximum function."""
        assert math_safe.max(1, 2, 3) == 3
        assert math_safe.max(5, -2, 10) == 10

    def test_pi_constant(self, math_capability):
        """Test pi constant."""
        assert abs(math_safe.pi - 3.14159265) < 1e-7

    def test_e_constant(self, math_capability):
        """Test e constant."""
        assert abs(math_safe.e - 2.71828182) < 1e-7

    def test_tau_constant(self, math_capability):
        """Test tau constant (2π)."""
        assert abs(math_safe.tau - 6.28318530) < 1e-7


class TestSafeMathWithoutCapability:
    """Test SafeMath operations without capability (should fail)."""

    def test_sqrt_no_capability(self):
        """Test sqrt without capability raises error."""
        with pytest.raises(CapabilityNotFoundError):
            math_safe.sqrt(16)

    def test_pow_no_capability(self):
        """Test pow without capability raises error."""
        with pytest.raises(CapabilityNotFoundError):
            math_safe.pow(2, 3)

    def test_sin_no_capability(self):
        """Test sin without capability raises error."""
        with pytest.raises(CapabilityNotFoundError):
            math_safe.sin(0)

    def test_factorial_no_capability(self):
        """Test factorial without capability raises error."""
        with pytest.raises(CapabilityNotFoundError):
            math_safe.factorial(5)

    def test_floor_no_capability(self):
        """Test floor without capability raises error."""
        with pytest.raises(CapabilityNotFoundError):
            math_safe.floor(3.7)

    def test_ceil_no_capability(self):
        """Test ceil without capability raises error."""
        with pytest.raises(CapabilityNotFoundError):
            math_safe.ceil(3.2)

    def test_abs_no_capability(self):
        """Test abs without capability raises error."""
        with pytest.raises(CapabilityNotFoundError):
            math_safe.abs(-5)

    def test_min_no_capability(self):
        """Test min without capability raises error."""
        with pytest.raises(CapabilityNotFoundError):
            math_safe.min(1, 2, 3)

    def test_max_no_capability(self):
        """Test max without capability raises error."""
        with pytest.raises(CapabilityNotFoundError):
            math_safe.max(1, 2, 3)


class TestSafeMathModuleFunctions:
    """Test module-level convenience functions."""

    @pytest.fixture
    def math_capability(self):
        """Mock math capability."""
        with patch('mlpy.runtime.capabilities.decorators.has_capability', return_value=True):
            yield

    def test_module_sqrt(self, math_capability):
        """Test module-level sqrt function."""
        from mlpy.runtime.system_modules.math_safe import sqrt
        assert sqrt(25) == 5.0

    def test_module_pow(self, math_capability):
        """Test module-level pow function."""
        from mlpy.runtime.system_modules.math_safe import pow
        assert pow(3, 2) == 9.0

    def test_module_constants(self):
        """Test module-level constants."""
        from mlpy.runtime.system_modules.math_safe import pi, e, tau
        assert abs(pi - 3.14159265) < 1e-7
        assert abs(e - 2.71828182) < 1e-7
        assert abs(tau - 6.28318530) < 1e-7


class TestSafeMathClass:
    """Test SafeMath class functionality."""

    def test_safe_math_class_exists(self):
        """Test SafeMath class can be instantiated."""
        sm = SafeMath()
        assert sm is not None

    def test_safe_math_constants_via_properties(self):
        """Test SafeMath constants accessed via properties."""
        sm = SafeMath()
        assert abs(sm.pi - math.pi) < 1e-10
        assert abs(sm.e - math.e) < 1e-10
        assert abs(sm.tau - math.tau) < 1e-10
