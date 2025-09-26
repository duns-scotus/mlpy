"""Safe math module with capability-based access control."""

import builtins
import math
from typing import Union

from ..capabilities.decorators import capability_safe, requires_capability

Number = Union[int, float]


@capability_safe(["math"], strict=True)
class SafeMath:
    """Safe math operations that require math capability."""

    @staticmethod
    @requires_capability("math")
    def sqrt(x: Number) -> float:
        """Calculate square root with capability check."""
        return math.sqrt(x)

    @staticmethod
    @requires_capability("math")
    def pow(x: Number, y: Number) -> float:
        """Calculate power with capability check."""
        return math.pow(x, y)

    @staticmethod
    @requires_capability("math")
    def sin(x: Number) -> float:
        """Calculate sine with capability check."""
        return math.sin(x)

    @staticmethod
    @requires_capability("math")
    def cos(x: Number) -> float:
        """Calculate cosine with capability check."""
        return math.cos(x)

    @staticmethod
    @requires_capability("math")
    def tan(x: Number) -> float:
        """Calculate tangent with capability check."""
        return math.tan(x)

    @staticmethod
    @requires_capability("math")
    def log(x: Number, base: Number = math.e) -> float:
        """Calculate logarithm with capability check."""
        return math.log(x, base)

    @staticmethod
    @requires_capability("math")
    def exp(x: Number) -> float:
        """Calculate exponential with capability check."""
        return math.exp(x)

    @staticmethod
    @requires_capability("math")
    def factorial(x: int) -> int:
        """Calculate factorial with capability check."""
        if not isinstance(x, int) or x < 0:
            raise ValueError("Factorial requires non-negative integer")
        return math.factorial(x)

    @staticmethod
    @requires_capability("math")
    def floor(x: Number) -> int:
        """Calculate floor with capability check."""
        return math.floor(x)

    @staticmethod
    @requires_capability("math")
    def ceil(x: Number) -> int:
        """Calculate ceiling with capability check."""
        return math.ceil(x)

    @staticmethod
    @requires_capability("math")
    def abs(x: Number) -> Number:
        """Calculate absolute value with capability check."""
        return builtins.abs(x)

    @staticmethod
    @requires_capability("math")
    def min(*args: Number) -> Number:
        """Find minimum value with capability check."""
        return builtins.min(*args)

    @staticmethod
    @requires_capability("math")
    def max(*args: Number) -> Number:
        """Find maximum value with capability check."""
        return builtins.max(*args)

    # Mathematical constants (read-only, no capability required)
    @property
    def pi(self) -> float:
        """Mathematical constant π."""
        return math.pi

    @property
    def e(self) -> float:
        """Mathematical constant e."""
        return math.e

    @property
    def tau(self) -> float:
        """Mathematical constant τ (2π)."""
        return math.tau


# Create global instance
math_safe = SafeMath()

# Export individual functions for convenience
sqrt = math_safe.sqrt
pow = math_safe.pow
sin = math_safe.sin
cos = math_safe.cos
tan = math_safe.tan
log = math_safe.log
exp = math_safe.exp
factorial = math_safe.factorial
floor = math_safe.floor
ceil = math_safe.ceil
abs = math_safe.abs
min = math_safe.min
max = math_safe.max

# Constants
pi = math_safe.pi
e = math_safe.e
tau = math_safe.tau

# Module metadata
__all__ = [
    "SafeMath",
    "math_safe",
    "sqrt",
    "pow",
    "sin",
    "cos",
    "tan",
    "log",
    "exp",
    "factorial",
    "floor",
    "ceil",
    "abs",
    "min",
    "max",
    "pi",
    "e",
    "tau",
]
