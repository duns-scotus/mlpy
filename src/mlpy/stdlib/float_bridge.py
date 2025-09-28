"""Python bridge implementations for ML float module."""

import math
from typing import Any


def float_to_string(value: float) -> str:
    """Convert float to string."""
    return str(value)


def float_to_int(value: float) -> int:
    """Convert float to integer (truncate decimal part)."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0


def float_to_bool(value: float) -> bool:
    """Convert float to boolean (0.0 = false, non-zero = true)."""
    return value != 0.0


def float_from_string(text: str) -> float:
    """Convert string to float. Returns 0.0 if conversion fails."""
    try:
        return float(text)
    except (ValueError, TypeError):
        return 0.0


def float_from_int(value: int) -> float:
    """Convert integer to float."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0


def float_from_bool(value: bool) -> float:
    """Convert boolean to float (true = 1.0, false = 0.0)."""
    return 1.0 if value else 0.0


def float_abs(value: float) -> float:
    """Get absolute value of float."""
    return abs(value)


def float_min(a: float, b: float) -> float:
    """Get minimum of two floats."""
    return min(a, b)


def float_max(a: float, b: float) -> float:
    """Get maximum of two floats."""
    return max(a, b)


def float_pow(base: float, exponent: float) -> float:
    """Raise float to power."""
    try:
        return pow(base, exponent)
    except (ValueError, OverflowError):
        return 0.0


def float_sqrt(value: float) -> float:
    """Get square root of float."""
    try:
        return math.sqrt(value)
    except (ValueError, TypeError):
        return 0.0


def float_floor(value: float) -> float:
    """Floor of float."""
    return math.floor(value)


def float_ceil(value: float) -> float:
    """Ceiling of float."""
    return math.ceil(value)


def float_round(value: float, digits: int = 0) -> float:
    """Round float to specified decimal places."""
    try:
        return round(value, digits)
    except (ValueError, TypeError):
        return 0.0


def float_is_positive(value: float) -> bool:
    """Check if float is positive."""
    return value > 0.0


def float_is_negative(value: float) -> bool:
    """Check if float is negative."""
    return value < 0.0


def float_is_zero(value: float) -> bool:
    """Check if float is zero."""
    return value == 0.0


def float_is_finite(value: float) -> bool:
    """Check if float is finite."""
    return math.isfinite(value)


def float_is_infinite(value: float) -> bool:
    """Check if float is infinite."""
    return math.isinf(value)


def float_is_nan(value: float) -> bool:
    """Check if float is NaN."""
    return math.isnan(value)


def float_clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp float value between min and max."""
    return max(min_val, min(max_val, value))


def float_sign(value: float) -> int:
    """Get sign of float (-1, 0, or 1)."""
    if value > 0.0:
        return 1
    elif value < 0.0:
        return -1
    else:
        return 0


def float_sin(value: float) -> float:
    """Sine of float (in radians)."""
    try:
        return math.sin(value)
    except (ValueError, TypeError):
        return 0.0


def float_cos(value: float) -> float:
    """Cosine of float (in radians)."""
    try:
        return math.cos(value)
    except (ValueError, TypeError):
        return 0.0


def float_tan(value: float) -> float:
    """Tangent of float (in radians)."""
    try:
        return math.tan(value)
    except (ValueError, TypeError):
        return 0.0


def float_log(value: float) -> float:
    """Natural logarithm of float."""
    try:
        return math.log(value)
    except (ValueError, TypeError):
        return 0.0


def float_log10(value: float) -> float:
    """Base-10 logarithm of float."""
    try:
        return math.log10(value)
    except (ValueError, TypeError):
        return 0.0


def float_exp(value: float) -> float:
    """e^value."""
    try:
        return math.exp(value)
    except (ValueError, OverflowError):
        return 0.0


class Float:
    """Float module interface for ML compatibility."""

    @staticmethod
    def toString(value: float) -> str:
        """Convert float to string."""
        return float_to_string(value)

    @staticmethod
    def toInt(value: float) -> int:
        """Convert float to integer."""
        return float_to_int(value)

    @staticmethod
    def toBool(value: float) -> bool:
        """Convert float to boolean."""
        return float_to_bool(value)

    @staticmethod
    def fromString(text: str) -> float:
        """Convert string to float."""
        return float_from_string(text)

    @staticmethod
    def fromInt(value: int) -> float:
        """Convert integer to float."""
        return float_from_int(value)

    @staticmethod
    def fromBool(value: bool) -> float:
        """Convert boolean to float."""
        return float_from_bool(value)

    @staticmethod
    def abs(value: float) -> float:
        """Get absolute value."""
        return float_abs(value)

    @staticmethod
    def min(a: float, b: float) -> float:
        """Get minimum of two values."""
        return float_min(a, b)

    @staticmethod
    def max(a: float, b: float) -> float:
        """Get maximum of two values."""
        return float_max(a, b)

    @staticmethod
    def pow(base: float, exponent: float) -> float:
        """Raise to power."""
        return float_pow(base, exponent)

    @staticmethod
    def sqrt(value: float) -> float:
        """Square root."""
        return float_sqrt(value)

    @staticmethod
    def floor(value: float) -> float:
        """Floor value."""
        return float_floor(value)

    @staticmethod
    def ceil(value: float) -> float:
        """Ceiling value."""
        return float_ceil(value)

    @staticmethod
    def round(value: float, digits: int = 0) -> float:
        """Round to decimal places."""
        return float_round(value, digits)

    @staticmethod
    def isPositive(value: float) -> bool:
        """Check if positive."""
        return float_is_positive(value)

    @staticmethod
    def isNegative(value: float) -> bool:
        """Check if negative."""
        return float_is_negative(value)

    @staticmethod
    def isZero(value: float) -> bool:
        """Check if zero."""
        return float_is_zero(value)

    @staticmethod
    def isFinite(value: float) -> bool:
        """Check if finite."""
        return float_is_finite(value)

    @staticmethod
    def isInfinite(value: float) -> bool:
        """Check if infinite."""
        return float_is_infinite(value)

    @staticmethod
    def isNaN(value: float) -> bool:
        """Check if NaN."""
        return float_is_nan(value)

    @staticmethod
    def clamp(value: float, min_val: float, max_val: float) -> float:
        """Clamp value between min and max."""
        return float_clamp(value, min_val, max_val)

    @staticmethod
    def sign(value: float) -> int:
        """Get sign of value."""
        return float_sign(value)

    # Trigonometric functions
    @staticmethod
    def sin(value: float) -> float:
        """Sine (radians)."""
        return float_sin(value)

    @staticmethod
    def cos(value: float) -> float:
        """Cosine (radians)."""
        return float_cos(value)

    @staticmethod
    def tan(value: float) -> float:
        """Tangent (radians)."""
        return float_tan(value)

    # Logarithmic functions
    @staticmethod
    def log(value: float) -> float:
        """Natural logarithm."""
        return float_log(value)

    @staticmethod
    def log10(value: float) -> float:
        """Base-10 logarithm."""
        return float_log10(value)

    @staticmethod
    def exp(value: float) -> float:
        """e^value."""
        return float_exp(value)

    # Snake_case aliases for ML compatibility
    @staticmethod
    def to_string(value: float) -> str:
        """Convert to string (snake_case alias)."""
        return float_to_string(value)

    @staticmethod
    def to_int(value: float) -> int:
        """Convert to integer (snake_case alias)."""
        return float_to_int(value)

    @staticmethod
    def to_bool(value: float) -> bool:
        """Convert to boolean (snake_case alias)."""
        return float_to_bool(value)

    @staticmethod
    def from_string(text: str) -> float:
        """Convert from string (snake_case alias)."""
        return float_from_string(text)

    @staticmethod
    def from_int(value: int) -> float:
        """Convert from integer (snake_case alias)."""
        return float_from_int(value)

    @staticmethod
    def from_bool(value: bool) -> float:
        """Convert from boolean (snake_case alias)."""
        return float_from_bool(value)

    @staticmethod
    def is_positive(value: float) -> bool:
        """Check if positive (snake_case alias)."""
        return float_is_positive(value)

    @staticmethod
    def is_negative(value: float) -> bool:
        """Check if negative (snake_case alias)."""
        return float_is_negative(value)

    @staticmethod
    def is_zero(value: float) -> bool:
        """Check if zero (snake_case alias)."""
        return float_is_zero(value)

    @staticmethod
    def is_finite(value: float) -> bool:
        """Check if finite (snake_case alias)."""
        return float_is_finite(value)

    @staticmethod
    def is_infinite(value: float) -> bool:
        """Check if infinite (snake_case alias)."""
        return float_is_infinite(value)

    @staticmethod
    def is_nan(value: float) -> bool:
        """Check if NaN (snake_case alias)."""
        return float_is_nan(value)


# Float object constructor - creates object with methods and properties
def create_float(value: float):
    """Create a float object with method access."""
    return {
        "value": value,

        # Conversion methods
        "toString": lambda: float_to_string(float_obj.value),
        "toInt": lambda: float_to_int(float_obj.value),
        "toBool": lambda: float_to_bool(float_obj.value),

        # Arithmetic methods
        "add": lambda other: create_float(float_obj.value + (other.value if hasattr(other, 'value') else other)),
        "subtract": lambda other: create_float(float_obj.value - (other.value if hasattr(other, 'value') else other)),
        "multiply": lambda other: create_float(float_obj.value * (other.value if hasattr(other, 'value') else other)),
        "divide": lambda other: create_float(float_obj.value / (other.value if hasattr(other, 'value') else other)),
        "mod": lambda other: create_float(float_obj.value % (other.value if hasattr(other, 'value') else other)),
        "pow": lambda exponent: create_float(float_pow(float_obj.value, exponent.value if hasattr(exponent, 'value') else exponent)),

        # Math methods
        "sqrt": lambda: create_float(float_sqrt(float_obj.value)),
        "floor": lambda: create_float(float_floor(float_obj.value)),
        "ceil": lambda: create_float(float_ceil(float_obj.value)),
        "round": lambda digits=0: create_float(float_round(float_obj.value, digits)),
        "abs": lambda: create_float(float_abs(float_obj.value)),

        # Trigonometric methods
        "sin": lambda: create_float(float_sin(float_obj.value)),
        "cos": lambda: create_float(float_cos(float_obj.value)),
        "tan": lambda: create_float(float_tan(float_obj.value)),

        # Logarithmic methods
        "log": lambda: create_float(float_log(float_obj.value)),
        "log10": lambda: create_float(float_log10(float_obj.value)),
        "exp": lambda: create_float(float_exp(float_obj.value)),

        # Comparison methods
        "equals": lambda other: float_obj.value == (other.value if hasattr(other, 'value') else other),
        "lessThan": lambda other: float_obj.value < (other.value if hasattr(other, 'value') else other),
        "greaterThan": lambda other: float_obj.value > (other.value if hasattr(other, 'value') else other),
        "lessThanOrEqual": lambda other: float_obj.value <= (other.value if hasattr(other, 'value') else other),
        "greaterThanOrEqual": lambda other: float_obj.value >= (other.value if hasattr(other, 'value') else other),

        # Utility methods
        "sign": lambda: float_sign(float_obj.value),
        "isPositive": lambda: float_is_positive(float_obj.value),
        "isNegative": lambda: float_is_negative(float_obj.value),
        "isZero": lambda: float_is_zero(float_obj.value),
        "isFinite": lambda: float_is_finite(float_obj.value),
        "isInfinite": lambda: float_is_infinite(float_obj.value),
        "isNaN": lambda: float_is_nan(float_obj.value),

        # Clamp method
        "clamp": lambda min_val, max_val: create_float(float_clamp(
            float_obj.value,
            min_val.value if hasattr(min_val, 'value') else min_val,
            max_val.value if hasattr(max_val, 'value') else max_val
        ))
    }


# Create global float instance for ML compatibility
float_module = Float()

# Export all bridge functions and the float object
__all__ = [
    "float_module",
    "create_float",
    "float_to_string",
    "float_to_int",
    "float_to_bool",
    "float_from_string",
    "float_from_int",
    "float_from_bool",
    "float_abs",
    "float_min",
    "float_max",
    "float_pow",
    "float_sqrt",
    "float_floor",
    "float_ceil",
    "float_round",
    "float_is_positive",
    "float_is_negative",
    "float_is_zero",
    "float_is_finite",
    "float_is_infinite",
    "float_is_nan",
    "float_clamp",
    "float_sign",
    "float_sin",
    "float_cos",
    "float_tan",
    "float_log",
    "float_log10",
    "float_exp",
]