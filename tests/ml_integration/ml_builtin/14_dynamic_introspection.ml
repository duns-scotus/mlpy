// Test builtin module: Dynamic introspection functions (SAFE)
// Features tested: hasattr(), getattr(), call()
// NO imports needed - builtin functions are auto-imported
// NOTE: These functions only work with SAFE attributes (whitelisted)

function test_hasattr_with_safe_attributes() {
    results = {};

    // Safe string attributes
    results.has_upper = hasattr("hello", "upper");              // Should return based on whitelist
    results.has_lower = hasattr("HELLO", "lower");              // Should return based on whitelist

    // Safe list attributes
    results.has_append = hasattr([1,2,3], "append");            // Should return based on whitelist

    // Unsafe attributes (should return false)
    results.has_class = hasattr("test", "__class__");           // false (blocked)
    results.has_dict = hasattr([], "__dict__");                 // false (blocked)

    return results;
}

function test_call_with_builtin_functions() {
    results = {};

    // Call builtin functions dynamically
    abs_func = abs;
    results.call_abs = call(abs_func, -5);                      // 5

    // Call with multiple arguments
    max_func = max;
    results.call_max = call(max_func, 10, 20, 30);              // 30

    min_func = min;
    results.call_min = call(min_func, 5, 2, 8);                 // 2

    return results;
}

function test_call_with_lambdas() {
    results = {};

    // Call lambda functions
    add = fn(x, y) => x + y;
    results.call_add = call(add, 10, 5);                        // 15

    multiply = fn(x, y) => x * y;
    results.call_multiply = call(multiply, 6, 7);               // 42

    return results;
}

function test_call_with_user_functions() {
    results = {};

    // Define functions to call
    function double(x) {
        return x * 2;
    }

    function triple(x) {
        return x * 3;
    }

    // Call them dynamically
    results.call_double = call(double, 21);                     // 42
    results.call_triple = call(triple, 14);                     // 42

    return results;
}

function test_dynamic_function_selection() {
    results = {};

    // Select function based on operation
    function select_operation(op_name) {
        if (op_name == "double") {
            return fn(x) => x * 2;
        } elif (op_name == "square") {
            return fn(x) => x * x;
        } elif (op_name == "negate") {
            return fn(x) => -x;
        } else {
            return fn(x) => x;
        }
    }

    // Use call to execute selected function
    double_fn = select_operation("double");
    results.double_result = call(double_fn, 10);                // 20

    square_fn = select_operation("square");
    results.square_result = call(square_fn, 5);                 // 25

    negate_fn = select_operation("negate");
    results.negate_result = call(negate_fn, 7);                 // -7

    return results;
}

function test_function_composition_with_call() {
    results = {};

    // Compose functions using call
    add_10 = fn(x) => x + 10;
    multiply_2 = fn(x) => x * 2;

    // Apply multiple operations
    val = 5;
    step1 = call(add_10, val);          // 15
    step2 = call(multiply_2, step1);    // 30

    results.step1 = step1;                                      // 15
    results.step2 = step2;                                      // 30

    return results;
}

function test_functional_programming_patterns() {
    results = {};

    // Higher-order function with call
    function apply_twice(func, value) {
        result = call(func, value);
        result = call(func, result);
        return result;
    }

    increment = fn(x) => x + 1;
    results.apply_twice_inc = apply_twice(increment, 10);       // 12

    double = fn(x) => x * 2;
    results.apply_twice_double = apply_twice(double, 3);        // 12

    return results;
}

function test_callable_check_before_call() {
    results = {};

    // Check if callable before calling
    func = fn(x) => x * 2;
    not_func = 42;

    if (callable(func)) {
        results.func_callable = true;                           // true
        results.func_result = call(func, 5);                    // 10
    }

    if (callable(not_func)) {
        results.not_func_callable = true;
    } else {
        results.not_func_callable = false;                      // false
    }

    return results;
}

function test_map_like_with_call() {
    results = {};

    // Implement map-like functionality with call
    numbers = [1, 2, 3, 4, 5];
    transform = fn(x) => x * x;

    transformed = [];
    for (n in numbers) {
        transformed = transformed + [call(transform, n)];
    }

    results.transformed = transformed;                          // [1, 4, 9, 16, 25]

    return results;
}

function test_filter_like_with_call() {
    results = {};

    // Implement filter-like functionality with call
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    is_even = fn(x) => (x - (x / 2) * 2) == 0;

    filtered = [];
    for (n in numbers) {
        if (call(is_even, n)) {
            filtered = filtered + [n];
        }
    }

    results.filtered = filtered;                                // [2, 4, 6, 8, 10]

    return results;
}

function test_reduce_like_with_call() {
    results = {};

    // Implement reduce-like functionality with call
    numbers = [1, 2, 3, 4, 5];
    add = fn(a, b) => a + b;

    accumulator = 0;
    for (n in numbers) {
        accumulator = call(add, accumulator, n);
    }

    results.sum = accumulator;                                  // 15

    return results;
}

function test_strategy_pattern_with_call() {
    results = {};

    // Strategy pattern: different algorithms
    strategies = {
        add: fn(a, b) => a + b,
        multiply: fn(a, b) => a * b,
        subtract: fn(a, b) => a - b
    };

    // Execute strategy
    result_add = call(strategies.add, 10, 5);
    result_multiply = call(strategies.multiply, 10, 5);
    result_subtract = call(strategies.subtract, 10, 5);

    results.add = result_add;                                   // 15
    results.multiply = result_multiply;                         // 50
    results.subtract = result_subtract;                         // 5

    return results;
}

function test_pipeline_with_call() {
    results = {};

    // Function pipeline
    operations = [
        fn(x) => x + 10,
        fn(x) => x * 2,
        fn(x) => x - 5
    ];

    value = 5;
    for (op in operations) {
        value = call(op, value);
    }

    results.final = value;                                      // 25 ((5+10)*2-5)

    return results;
}

function main() {
    all_results = {};

    all_results.hasattr_tests = test_hasattr_with_safe_attributes();
    all_results.call_builtins = test_call_with_builtin_functions();
    all_results.call_lambdas = test_call_with_lambdas();
    all_results.call_user_funcs = test_call_with_user_functions();
    all_results.dynamic_select = test_dynamic_function_selection();
    all_results.composition = test_function_composition_with_call();
    all_results.functional = test_functional_programming_patterns();
    all_results.callable_check = test_callable_check_before_call();
    all_results.map_like = test_map_like_with_call();
    all_results.filter_like = test_filter_like_with_call();
    all_results.reduce_like = test_reduce_like_with_call();
    all_results.strategy = test_strategy_pattern_with_call();
    all_results.pipeline = test_pipeline_with_call();

    return all_results;
}

// Run tests
test_results = main();
