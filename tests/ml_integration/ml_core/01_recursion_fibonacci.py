"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

def fibonacci_recursive(n):
    if (n <= 1):
        return n
    else:
        return (fibonacci_recursive((n - 1)) + fibonacci_recursive((n - 2)))

def fibonacci_iterative(n):
    if (n <= 1):
        return n
    a = 0
    b = 1
    i = 2
    while (i <= n):
        temp = (a + b)
        a = b
        b = temp
        i = (i + 1)
    return b

def fibonacci_tail_helper(n, a, b):
    if (n == 0):
        return a
    else:
        return fibonacci_tail_helper((n - 1), b, (a + b))

def fibonacci_tail(n):
    return fibonacci_tail_helper(n, 0, 1)

def factorial(n):
    if (n <= 1):
        return 1
    else:
        return (n * factorial((n - 1)))

def power(base, exp):
    if (exp == 0):
        return 1
    elif (exp == 1):
        return base
    else:
        return (base * power(base, (exp - 1)))

def gcd(a, b):
    if (b == 0):
        return a
    else:
        remainder = (a - ((a / b) * b))
        return gcd(b, remainder)

def sum_of_digits(n):
    if (n < 10):
        return n
    else:
        digit = (n - ((n / 10) * 10))
        remaining = (n / 10)
        return (digit + sum_of_digits(remaining))

def main():
    results = {}
    results['fib_10_rec'] = fibonacci_recursive(10)
    results['fib_10_iter'] = fibonacci_iterative(10)
    results['fib_10_tail'] = fibonacci_tail(10)
    results['fib_15'] = fibonacci_recursive(15)
    results['fib_20'] = fibonacci_iterative(20)
    results['fact_5'] = factorial(5)
    results['fact_7'] = factorial(7)
    results['fact_10'] = factorial(10)
    results['pow_2_5'] = power(2, 5)
    results['pow_3_4'] = power(3, 4)
    results['pow_5_3'] = power(5, 3)
    results['gcd_48_18'] = gcd(48, 18)
    results['gcd_100_35'] = gcd(100, 35)
    results['gcd_17_19'] = gcd(17, 19)
    results['sum_123'] = sum_of_digits(123)
    results['sum_9876'] = sum_of_digits(9876)
    results['sum_1000'] = sum_of_digits(1000)
    return results

test_results = main()

# End of generated code