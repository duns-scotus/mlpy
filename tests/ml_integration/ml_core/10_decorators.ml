// Test core language: Function decorators and wrappers
// Features tested: higher-order functions, closures, function wrapping
// NO external function calls - pure language features only

// Simple logging decorator
function with_logging(func) {
    function wrapper(arg) {
        // Log entry (store in result)
        log_entry = "Entering with arg: " + arg;
        result = func(arg);
        log_exit = "Exiting with result: " + result;
        return result;
    }
    return wrapper;
}

// Memoization decorator
function memoize(func) {
    cache = {};
    cache_size = 0;

    function wrapper(n) {
        nonlocal cache, cache_size;

        // Check if result is cached
        cached_result = null;
        try {
            cached_result = cache[n];
        } except (e) {
            // Key doesn't exist
        }

        if (cached_result != null) {
            return cached_result;
        }

        // Compute and cache
        result = func(n);
        cache[n] = result;
        cache_size = cache_size + 1;
        return result;
    }

    return wrapper;
}

// Timing decorator (counts calls)
function count_calls(func) {
    call_count = 0;

    function wrapper(arg) {
        nonlocal call_count;
        call_count = call_count + 1;
        result = func(arg);
        return {result: result, calls: call_count};
    }

    return wrapper;
}

// Validation decorator
function validate_positive(func) {
    function wrapper(n) {
        if (n < 0) {
            return -1;  // Error value
        }
        return func(n);
    }
    return wrapper;
}

// Retry decorator (tries multiple times on failure)
function with_retry(func, max_attempts) {
    function wrapper(n) {
        attempts = 0;
        last_error = null;

        while (attempts < max_attempts) {
            try {
                return func(n);
            } except (e) {
                last_error = e;
                attempts = attempts + 1;
            }
        }

        return {error: last_error, attempts: attempts};
    }

    return wrapper;
}

// Before/After decorator
function with_before_after(func, before_value, after_value) {
    function wrapper(arg) {
        result = before_value + func(arg) + after_value;
        return result;
    }
    return wrapper;
}

// Transformation decorator (doubles the result)
function double_result(func) {
    function wrapper(arg) {
        result = func(arg);
        return result * 2;
    }
    return wrapper;
}

// Conditional execution decorator
function only_if_even(func) {
    function wrapper(n) {
        remainder = n - (n / 2) * 2;
        if (remainder == 0) {
            return func(n);
        } else {
            return 0;  // Don't execute for odd numbers
        }
    }
    return wrapper;
}

// Composition decorator
function compose_decorators(decorator1, decorator2) {
    function combined(func) {
        return decorator1(decorator2(func));
    }
    return combined;
}

// Test functions to be decorated
function add_ten(x) {
    return x + 10;
}

function multiply_by_three(x) {
    return x * 3;
}

function square(x) {
    return x * x;
}

function factorial(n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

function fibonacci(n) {
    if (n <= 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// Curry decorator - convert to curried version
function curry_decorator(func) {
    function curried(a) {
        function apply_second(b) {
            return func(a, b);
        }
        return apply_second;
    }
    return curried;
}

// Two-argument function for currying
function add_two_args(a, b) {
    return a + b;
}

// Partial application decorator
function partial_left(func, first_arg) {
    function wrapper(second_arg) {
        return func(first_arg, second_arg);
    }
    return wrapper;
}

// Cache with size limit decorator
function cache_with_limit(func, max_size) {
    cache = {};
    cache_keys = [];
    cache_size = 0;

    function wrapper(n) {
        nonlocal cache, cache_keys, cache_size;

        cached = null;
        try {
            cached = cache[n];
        } except (e) {
            // Key doesn't exist
        }

        if (cached != null) {
            return cached;
        }

        result = func(n);

        if (cache_size >= max_size) {
            // Remove oldest entry (simplified - just clear cache)
            cache = {};
            cache_keys = [];
            cache_size = 0;
        }

        cache[n] = result;
        cache_size = cache_size + 1;

        return result;
    }

    return wrapper;
}

// Main test function
function main() {
    results = {};

    // Test 1: Logging decorator
    logged_add = with_logging(add_ten);
    results.logged = logged_add(5);  // 15

    // Test 2: Memoization
    memo_fib = memoize(fibonacci);
    results.memo_fib_10 = memo_fib(10);
    results.memo_fib_10_again = memo_fib(10);  // Should use cache

    // Test 3: Call counting
    counted_square = count_calls(square);
    results.count1 = counted_square(5);
    results.count2 = counted_square(6);
    results.count3 = counted_square(7);

    // Test 4: Validation
    validated_square = validate_positive(square);
    results.valid_positive = validated_square(5);  // 25
    results.valid_negative = validated_square(-3); // -1 (error)

    // Test 5: Double result
    doubled_add = double_result(add_ten);
    results.doubled = doubled_add(5);  // (5+10)*2 = 30

    // Test 6: Before/After
    wrapped_square = with_before_after(square, 100, 1);
    results.wrapped = wrapped_square(5);  // 100 + 25 + 1 = 126

    // Test 7: Conditional execution
    even_only_square = only_if_even(square);
    results.even_4 = even_only_square(4);  // 16
    results.odd_5 = even_only_square(5);   // 0

    // Test 8: Currying
    curried_add = curry_decorator(add_two_args);
    add_5 = curried_add(5);
    results.curried_5_3 = add_5(3);  // 8
    results.curried_5_7 = add_5(7);  // 12

    // Test 9: Partial application
    add_10_partial = partial_left(add_two_args, 10);
    results.partial_10_5 = add_10_partial(5);   // 15
    results.partial_10_20 = add_10_partial(20); // 30

    // Test 10: Decorator composition
    // Apply validation then doubling
    function compose_valid_double(func) {
        return validate_positive(double_result(func));
    }

    composed = compose_valid_double(add_ten);
    results.composed_positive = composed(5);   // (5+10)*2 = 30
    results.composed_negative = composed(-3);  // -1 (validation fails)

    // Test 11: Cache with limit
    limited_cache_square = cache_with_limit(square, 2);
    results.cache1 = limited_cache_square(5);  // 25, cached
    results.cache2 = limited_cache_square(6);  // 36, cached
    results.cache3 = limited_cache_square(5);  // 25, from cache
    results.cache4 = limited_cache_square(7);  // 49, cache full - cleared

    // Test 12: Multiple decorators on same function
    multi_decorated = double_result(validate_positive(add_ten));
    results.multi_pos = multi_decorated(10);  // (10+10)*2 = 40
    results.multi_neg = multi_decorated(-5);  // -1 validation fails, then -2

    return results;
}

// Run tests
test_results = main();
