"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

def with_logging(func):
    def wrapper(arg):
        log_entry = (str('Entering with arg: ') + str(arg))
        result = _safe_call(func, arg)
        log_exit = (str('Exiting with result: ') + str(result))
        return result
    return wrapper

def memoize(func):
    cache = {}
    cache_size = 0
    def wrapper(n):
        nonlocal cache, cache_size
        cached_result = None
        try:
            cached_result = cache[n]
        except Exception as e:
            pass
        finally:
            pass
        if (cached_result != None):
            return cached_result
        result = _safe_call(func, n)
        cache[n] = result
        cache_size = (cache_size + 1)
        return result
    return wrapper

def count_calls(func):
    call_count = 0
    def wrapper(arg):
        nonlocal call_count
        call_count = (call_count + 1)
        result = _safe_call(func, arg)
        return {'result': result, 'calls': call_count}
    return wrapper

def validate_positive(func):
    def wrapper(n):
        if (n < 0):
            return -1
        return _safe_call(func, n)
    return wrapper

def with_retry(func, max_attempts):
    def wrapper(n):
        attempts = 0
        last_error = None
        while (attempts < max_attempts):
            try:
                return _safe_call(func, n)
            except Exception as e:
                last_error = e
                attempts = (attempts + 1)
            finally:
                pass
        return {'error': last_error, 'attempts': attempts}
    return wrapper

def with_before_after(func, before_value, after_value):
    def wrapper(arg):
        result = ((before_value + _safe_call(func, arg)) + after_value)
        return result
    return wrapper

def double_result(func):
    def wrapper(arg):
        result = _safe_call(func, arg)
        return (result * 2)
    return wrapper

def only_if_even(func):
    def wrapper(n):
        remainder = (n - ((n / 2) * 2))
        if (remainder == 0):
            return _safe_call(func, n)
        else:
            return 0
    return wrapper

def compose_decorators(decorator1, decorator2):
    def combined(func):
        return _safe_call(decorator1, _safe_call(decorator2, func))
    return combined

def add_ten(x):
    return (x + 10)

def multiply_by_three(x):
    return (x * 3)

def square(x):
    return (x * x)

def factorial(n):
    if (n <= 1):
        return 1
    return (n * factorial((n - 1)))

def fibonacci(n):
    if (n <= 1):
        return n
    return (fibonacci((n - 1)) + fibonacci((n - 2)))

def curry_decorator(func):
    def curried(a):
        def apply_second(b):
            return _safe_call(func, a, b)
        return apply_second
    return curried

def add_two_args(a, b):
    return (a + b)

def partial_left(func, first_arg):
    def wrapper(second_arg):
        return _safe_call(func, first_arg, second_arg)
    return wrapper

def cache_with_limit(func, max_size):
    cache = {}
    cache_keys = []
    cache_size = 0
    def wrapper(n):
        nonlocal cache, cache_keys, cache_size
        cached = None
        try:
            cached = cache[n]
        except Exception as e:
            pass
        finally:
            pass
        if (cached != None):
            return cached
        result = _safe_call(func, n)
        if (cache_size >= max_size):
            cache = {}
            cache_keys = []
            cache_size = 0
        cache[n] = result
        cache_size = (cache_size + 1)
        return result
    return wrapper

def main():
    results = {}
    logged_add = with_logging(add_ten)
    results['logged'] = _safe_call(logged_add, 5)
    memo_fib = memoize(fibonacci)
    results['memo_fib_10'] = _safe_call(memo_fib, 10)
    results['memo_fib_10_again'] = _safe_call(memo_fib, 10)
    counted_square = count_calls(square)
    results['count1'] = _safe_call(counted_square, 5)
    results['count2'] = _safe_call(counted_square, 6)
    results['count3'] = _safe_call(counted_square, 7)
    validated_square = validate_positive(square)
    results['valid_positive'] = _safe_call(validated_square, 5)
    results['valid_negative'] = _safe_call(validated_square, -3)
    doubled_add = double_result(add_ten)
    results['doubled'] = _safe_call(doubled_add, 5)
    wrapped_square = with_before_after(square, 100, 1)
    results['wrapped'] = _safe_call(wrapped_square, 5)
    even_only_square = only_if_even(square)
    results['even_4'] = _safe_call(even_only_square, 4)
    results['odd_5'] = _safe_call(even_only_square, 5)
    curried_add = curry_decorator(add_two_args)
    add_5 = _safe_call(curried_add, 5)
    results['curried_5_3'] = _safe_call(add_5, 3)
    results['curried_5_7'] = _safe_call(add_5, 7)
    add_10_partial = partial_left(add_two_args, 10)
    results['partial_10_5'] = _safe_call(add_10_partial, 5)
    results['partial_10_20'] = _safe_call(add_10_partial, 20)
    def compose_valid_double(func):
        return validate_positive(double_result(func))
    composed = compose_valid_double(add_ten)
    results['composed_positive'] = _safe_call(composed, 5)
    results['composed_negative'] = _safe_call(composed, -3)
    limited_cache_square = cache_with_limit(square, 2)
    results['cache1'] = _safe_call(limited_cache_square, 5)
    results['cache2'] = _safe_call(limited_cache_square, 6)
    results['cache3'] = _safe_call(limited_cache_square, 5)
    results['cache4'] = _safe_call(limited_cache_square, 7)
    multi_decorated = double_result(validate_positive(add_ten))
    results['multi_pos'] = _safe_call(multi_decorated, 10)
    results['multi_neg'] = _safe_call(multi_decorated, -5)
    return results

test_results = main()

# End of generated code