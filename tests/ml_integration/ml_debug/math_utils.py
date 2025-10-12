"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

def abs(x):
    if (x < 0):
        return (-x)
    else:
        return x

def max(a, b):
    if (a > b):
        return a
    else:
        return b

def min(a, b):
    if (a < b):
        return a
    else:
        return b

def clamp(value, min_val, max_val):
    if (value < min_val):
        return min_val
    elif (value > max_val):
        return max_val
    else:
        return value

def is_even(n):
    remainder = (n - ((n / 2) * 2))
    return (remainder == 0)

def is_odd(n):
    return (not is_even(n))

def factorial(n):
    if (n <= 1):
        return 1
    else:
        return (n * factorial((n - 1)))

def fibonacci(n):
    if (n <= 1):
        return n
    else:
        return (fibonacci((n - 1)) + fibonacci((n - 2)))

def sum_range(start, end):
    total = 0
    i = start
    while (i <= end):
        total = (total + i)
        i = (i + 1)
    return total

def gcd(a, b):
    if (b == 0):
        return a
    else:
        remainder = (a - ((a / b) * b))
        return gcd(b, remainder)

# End of generated code