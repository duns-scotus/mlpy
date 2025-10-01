"""Python bridge implementations for ML int module."""



def int_to_string(value: int) -> str:
    """Convert integer to string."""
    return str(value)


def int_to_float(value: int) -> float:
    """Convert integer to float."""
    return float(value)


def int_to_bool(value: int) -> bool:
    """Convert integer to boolean (0 = false, non-zero = true)."""
    return value != 0


def int_from_string(text: str) -> int:
    """Convert string to integer. Returns 0 if conversion fails."""
    try:
        return int(text)
    except (ValueError, TypeError):
        return 0


def int_from_float(value: float) -> int:
    """Convert float to integer (truncate decimal part)."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0


def int_from_bool(value: bool) -> int:
    """Convert boolean to integer (true = 1, false = 0)."""
    return 1 if value else 0


def int_abs(value: int) -> int:
    """Get absolute value of integer."""
    return abs(value)


def int_min(a: int, b: int) -> int:
    """Get minimum of two integers."""
    return min(a, b)


def int_max(a: int, b: int) -> int:
    """Get maximum of two integers."""
    return max(a, b)


def int_pow(base: int, exponent: int) -> int:
    """Raise integer to power."""
    try:
        return int(pow(base, exponent))
    except (ValueError, OverflowError):
        return 0


def int_is_even(value: int) -> bool:
    """Check if integer is even."""
    return value % 2 == 0


def int_is_odd(value: int) -> bool:
    """Check if integer is odd."""
    return value % 2 != 0


def int_is_positive(value: int) -> bool:
    """Check if integer is positive."""
    return value > 0


def int_is_negative(value: int) -> bool:
    """Check if integer is negative."""
    return value < 0


def int_is_zero(value: int) -> bool:
    """Check if integer is zero."""
    return value == 0


def int_clamp(value: int, min_val: int, max_val: int) -> int:
    """Clamp integer value between min and max."""
    return max(min_val, min(max_val, value))


def int_sign(value: int) -> int:
    """Get sign of integer (-1, 0, or 1)."""
    if value > 0:
        return 1
    elif value < 0:
        return -1
    else:
        return 0


class Int:
    """Int module interface for ML compatibility."""

    @staticmethod
    def toString(value: int) -> str:
        """Convert integer to string."""
        return int_to_string(value)

    @staticmethod
    def toFloat(value: int) -> float:
        """Convert integer to float."""
        return int_to_float(value)

    @staticmethod
    def toBool(value: int) -> bool:
        """Convert integer to boolean."""
        return int_to_bool(value)

    @staticmethod
    def fromString(text: str) -> int:
        """Convert string to integer."""
        return int_from_string(text)

    @staticmethod
    def fromFloat(value: float) -> int:
        """Convert float to integer."""
        return int_from_float(value)

    @staticmethod
    def fromBool(value: bool) -> int:
        """Convert boolean to integer."""
        return int_from_bool(value)

    @staticmethod
    def abs(value: int) -> int:
        """Get absolute value."""
        return int_abs(value)

    @staticmethod
    def min(a: int, b: int) -> int:
        """Get minimum of two values."""
        return int_min(a, b)

    @staticmethod
    def max(a: int, b: int) -> int:
        """Get maximum of two values."""
        return int_max(a, b)

    @staticmethod
    def pow(base: int, exponent: int) -> int:
        """Raise to power."""
        return int_pow(base, exponent)

    @staticmethod
    def isEven(value: int) -> bool:
        """Check if even."""
        return int_is_even(value)

    @staticmethod
    def isOdd(value: int) -> bool:
        """Check if odd."""
        return int_is_odd(value)

    @staticmethod
    def isPositive(value: int) -> bool:
        """Check if positive."""
        return int_is_positive(value)

    @staticmethod
    def isNegative(value: int) -> bool:
        """Check if negative."""
        return int_is_negative(value)

    @staticmethod
    def isZero(value: int) -> bool:
        """Check if zero."""
        return int_is_zero(value)

    @staticmethod
    def clamp(value: int, min_val: int, max_val: int) -> int:
        """Clamp value between min and max."""
        return int_clamp(value, min_val, max_val)

    @staticmethod
    def sign(value: int) -> int:
        """Get sign of value."""
        return int_sign(value)

    # Snake_case aliases for ML compatibility
    @staticmethod
    def to_string(value: int) -> str:
        """Convert to string (snake_case alias)."""
        return int_to_string(value)

    @staticmethod
    def to_float(value: int) -> float:
        """Convert to float (snake_case alias)."""
        return int_to_float(value)

    @staticmethod
    def to_bool(value: int) -> bool:
        """Convert to boolean (snake_case alias)."""
        return int_to_bool(value)

    @staticmethod
    def from_string(text: str) -> int:
        """Convert from string (snake_case alias)."""
        return int_from_string(text)

    @staticmethod
    def from_float(value: float) -> int:
        """Convert from float (snake_case alias)."""
        return int_from_float(value)

    @staticmethod
    def from_bool(value: bool) -> int:
        """Convert from boolean (snake_case alias)."""
        return int_from_bool(value)

    @staticmethod
    def is_even(value: int) -> bool:
        """Check if even (snake_case alias)."""
        return int_is_even(value)

    @staticmethod
    def is_odd(value: int) -> bool:
        """Check if odd (snake_case alias)."""
        return int_is_odd(value)

    @staticmethod
    def is_positive(value: int) -> bool:
        """Check if positive (snake_case alias)."""
        return int_is_positive(value)

    @staticmethod
    def is_negative(value: int) -> bool:
        """Check if negative (snake_case alias)."""
        return int_is_negative(value)

    @staticmethod
    def is_zero(value: int) -> bool:
        """Check if zero (snake_case alias)."""
        return int_is_zero(value)


# Integer object constructor - creates object with methods and properties
def create_int(value: int):
    """Create an integer object with method access."""
    return {
        "value": value,
        # Conversion methods
        "toString": lambda: int_to_string(int_obj.value),
        "toFloat": lambda: int_to_float(int_obj.value),
        "toBool": lambda: int_to_bool(int_obj.value),
        # Arithmetic methods
        "add": lambda other: create_int(
            int_obj.value + (other.value if hasattr(other, "value") else other)
        ),
        "subtract": lambda other: create_int(
            int_obj.value - (other.value if hasattr(other, "value") else other)
        ),
        "multiply": lambda other: create_int(
            int_obj.value * (other.value if hasattr(other, "value") else other)
        ),
        "divide": lambda other: create_int(
            int_obj.value // (other.value if hasattr(other, "value") else other)
        ),
        "mod": lambda other: create_int(
            int_obj.value % (other.value if hasattr(other, "value") else other)
        ),
        "pow": lambda exponent: create_int(
            int_pow(int_obj.value, exponent.value if hasattr(exponent, "value") else exponent)
        ),
        # Comparison methods
        "equals": lambda other: int_obj.value
        == (other.value if hasattr(other, "value") else other),
        "lessThan": lambda other: int_obj.value
        < (other.value if hasattr(other, "value") else other),
        "greaterThan": lambda other: int_obj.value
        > (other.value if hasattr(other, "value") else other),
        "lessThanOrEqual": lambda other: int_obj.value
        <= (other.value if hasattr(other, "value") else other),
        "greaterThanOrEqual": lambda other: int_obj.value
        >= (other.value if hasattr(other, "value") else other),
        # Utility methods
        "abs": lambda: create_int(int_abs(int_obj.value)),
        "sign": lambda: int_sign(int_obj.value),
        "isEven": lambda: int_is_even(int_obj.value),
        "isOdd": lambda: int_is_odd(int_obj.value),
        "isPositive": lambda: int_is_positive(int_obj.value),
        "isNegative": lambda: int_is_negative(int_obj.value),
        "isZero": lambda: int_is_zero(int_obj.value),
        # Clamp method
        "clamp": lambda min_val, max_val: create_int(
            int_clamp(
                int_obj.value,
                min_val.value if hasattr(min_val, "value") else min_val,
                max_val.value if hasattr(max_val, "value") else max_val,
            )
        ),
    }


# Create global int instance for ML compatibility
int_module = Int()

# Export all bridge functions and the int object
__all__ = [
    "int_module",
    "create_int",
    "int_to_string",
    "int_to_float",
    "int_to_bool",
    "int_from_string",
    "int_from_float",
    "int_from_bool",
    "int_abs",
    "int_min",
    "int_max",
    "int_pow",
    "int_is_even",
    "int_is_odd",
    "int_is_positive",
    "int_is_negative",
    "int_is_zero",
    "int_clamp",
    "int_sign",
]
