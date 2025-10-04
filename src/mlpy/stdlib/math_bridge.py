"""ML Math Standard Library - Python Implementation."""

import math as py_math
from mlpy.stdlib.decorators import ml_module, ml_function


@ml_module(
    name="math",
    description="Mathematical operations and constants",
    capabilities=["math.compute"],
    version="1.0.0"
)
class Math:
    """ML math operations implemented in Python."""

    # Mathematical constants
    pi = py_math.pi
    e = py_math.e

    @ml_function(description="Square root", capabilities=["math.compute"])
    def sqrt(self, x: float) -> float:
        """Square root function."""
        if x < 0:
            return 0  # Error case for ML compatibility
        return py_math.sqrt(x)

    @ml_function(description="Absolute value", capabilities=["math.compute"])
    def abs(self, x: float) -> float:
        """Absolute value function."""
        return abs(x)

    @ml_function(description="Sine function", capabilities=["math.compute"])
    def sin(self, x: float) -> float:
        """Sine function."""
        return py_math.sin(x)

    @ml_function(description="Cosine function", capabilities=["math.compute"])
    def cos(self, x: float) -> float:
        """Cosine function."""
        return py_math.cos(x)

    @ml_function(description="Tangent function", capabilities=["math.compute"])
    def tan(self, x: float) -> float:
        """Tangent function."""
        return py_math.tan(x)

    @ml_function(description="Natural logarithm", capabilities=["math.compute"])
    def ln(self, x: float) -> float:
        """Natural logarithm."""
        if x <= 0:
            return -999  # Error case for ML compatibility
        return py_math.log(x)

    @ml_function(description="Logarithm with base", capabilities=["math.compute"])
    def log(self, x: float, base: float = 10) -> float:
        """Logarithm with specified base."""
        if x <= 0 or base <= 0 or base == 1:
            return -999  # Error case
        return py_math.log(x, base)

    @ml_function(description="Exponential (e^x)", capabilities=["math.compute"])
    def exp(self, x: float) -> float:
        """Exponential function (e^x)."""
        try:
            return py_math.exp(x)
        except OverflowError:
            return float("inf")

    @ml_function(description="Power (x^y)", capabilities=["math.compute"])
    def pow(self, x: float, y: float) -> float:
        """Power function (x^y)."""
        try:
            return pow(x, y)
        except (OverflowError, ZeroDivisionError):
            return float("inf") if x > 0 else 0

    @ml_function(description="Floor function", capabilities=["math.compute"])
    def floor(self, x: float) -> int:
        """Floor function."""
        return py_math.floor(x)

    @ml_function(description="Ceiling function", capabilities=["math.compute"])
    def ceil(self, x: float) -> int:
        """Ceiling function."""
        return py_math.ceil(x)

    @ml_function(description="Round to nearest integer", capabilities=["math.compute"])
    def round(self, x: float) -> int:
        """Round to nearest integer."""
        return round(x)

    @ml_function(description="Minimum of two values", capabilities=["math.compute"])
    def min(self, a: float, b: float) -> float:
        """Minimum of two values."""
        return min(a, b)

    @ml_function(description="Maximum of two values", capabilities=["math.compute"])
    def max(self, a: float, b: float) -> float:
        """Maximum of two values."""
        return max(a, b)

    @ml_function(description="Random number [0,1)", capabilities=["math.compute"])
    def random(self, ) -> float:
        """Random number between 0 and 1."""
        import random

        return random.random()

    @ml_function(description="Convert degrees to radians", capabilities=["math.compute"])
    def degToRad(self, degrees: float) -> float:
        """Convert degrees to radians."""
        return py_math.radians(degrees)

    @ml_function(description="Convert radians to degrees", capabilities=["math.compute"])
    def radToDeg(self, radians: float) -> float:
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
