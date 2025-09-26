"""ML Math Standard Library - Python Implementation."""

import math as py_math
from typing import Any


class Math:
    """ML math operations implemented in Python."""

    # Mathematical constants
    pi = py_math.pi
    e = py_math.e

    @staticmethod
    def sqrt(x: float) -> float:
        """Square root function."""
        if x < 0:
            return 0  # Error case for ML compatibility
        return py_math.sqrt(x)

    @staticmethod
    def abs(x: float) -> float:
        """Absolute value function."""
        return abs(x)

    @staticmethod
    def sin(x: float) -> float:
        """Sine function."""
        return py_math.sin(x)

    @staticmethod
    def cos(x: float) -> float:
        """Cosine function."""
        return py_math.cos(x)

    @staticmethod
    def tan(x: float) -> float:
        """Tangent function."""
        return py_math.tan(x)

    @staticmethod
    def ln(x: float) -> float:
        """Natural logarithm."""
        if x <= 0:
            return -999  # Error case for ML compatibility
        return py_math.log(x)

    @staticmethod
    def log(x: float, base: float = 10) -> float:
        """Logarithm with specified base."""
        if x <= 0 or base <= 0 or base == 1:
            return -999  # Error case
        return py_math.log(x, base)

    @staticmethod
    def exp(x: float) -> float:
        """Exponential function (e^x)."""
        try:
            return py_math.exp(x)
        except OverflowError:
            return float('inf')

    @staticmethod
    def pow(x: float, y: float) -> float:
        """Power function (x^y)."""
        try:
            return pow(x, y)
        except (OverflowError, ZeroDivisionError):
            return float('inf') if x > 0 else 0

    @staticmethod
    def floor(x: float) -> int:
        """Floor function."""
        return py_math.floor(x)

    @staticmethod
    def ceil(x: float) -> int:
        """Ceiling function."""
        return py_math.ceil(x)

    @staticmethod
    def round(x: float) -> int:
        """Round to nearest integer."""
        return round(x)

    @staticmethod
    def min(a: float, b: float) -> float:
        """Minimum of two values."""
        return min(a, b)

    @staticmethod
    def max(a: float, b: float) -> float:
        """Maximum of two values."""
        return max(a, b)

    @staticmethod
    def random() -> float:
        """Random number between 0 and 1."""
        import random
        return random.random()

    @staticmethod
    def degToRad(degrees: float) -> float:
        """Convert degrees to radians."""
        return py_math.radians(degrees)

    @staticmethod
    def radToDeg(radians: float) -> float:
        """Convert radians to degrees."""
        return py_math.degrees(radians)


# Global math instance for ML programs
math = Math()

# Constants
pi = py_math.pi
e = py_math.e

# Helper functions for ML bridge
def sqrt_helper(x: float) -> float:
    """Helper function for square root."""
    return math.sqrt(x)

def abs_helper(x: float) -> float:
    """Helper function for absolute value."""
    return math.abs(x)

def min_helper(a: float, b: float) -> float:
    """Helper function for minimum."""
    return math.min(a, b)

def max_helper(a: float, b: float) -> float:
    """Helper function for maximum."""
    return math.max(a, b)