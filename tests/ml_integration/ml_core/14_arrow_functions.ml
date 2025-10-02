// Test core language: Arrow functions
// Features tested: arrow function syntax (fn(params) => expression/block)
// NO external function calls - pure language features only

// Test 1: Simple arrow function - single parameter, expression body
function test_simple_arrow() {
    double = fn(x) => x * 2;
    result = double(5);
    return result;  // Should be 10
}

// Test 2: Arrow function - multiple parameters
function test_arrow_multiple_params() {
    add = fn(a, b) => a + b;
    result = add(10, 20);
    return result;  // Should be 30
}

// Test 3: Arrow function - no parameters
function test_arrow_no_params() {
    get_ten = fn() => 10;
    result = get_ten();
    return result;  // Should be 10
}

// Test 4: Arrow function with expression (not block)
function test_arrow_expression() {
    square = fn(x) => x * x;
    val = square(7);
    return val;  // Should be 49
}

// Test 5: Arrow function in array map pattern
function test_arrow_map_pattern() {
    arr = [1, 2, 3, 4, 5];
    transformer = fn(x) => x * 3;

    result = [];
    i = 0;
    while (i < 5) {
        result = result + [transformer(arr[i])];
        i = i + 1;
    }

    return result;  // Should be [3, 6, 9, 12, 15]
}

// Test 6: Arrow function as argument
function apply_function(func, value) {
    return func(value);
}

function test_arrow_as_argument() {
    triple = fn(x) => x * 3;
    result = apply_function(triple, 10);
    return result;  // Should be 30
}

// Test 7: Arrow function returning arrow function (currying)
function test_arrow_currying() {
    make_adder = fn(x) => fn(y) => x + y;
    add_5 = make_adder(5);
    result = add_5(10);
    return result;  // Should be 15
}

// Test 8: Arrow function with conditional logic
function test_arrow_conditional() {
    abs_value = fn(x) => x < 0 ? 0 - x : x;

    results = {};
    results.positive = abs_value(10);   // 10
    results.negative = abs_value(-10);  // 10
    results.zero = abs_value(0);        // 0
    return results;
}

// Test 9: Arrow function with array operations
function test_arrow_array_ops() {
    get_first = fn(arr) => arr[0];
    get_last = fn(arr) => arr[4];  // Assuming length 5

    test_arr = [10, 20, 30, 40, 50];

    results = {};
    results.first = get_first(test_arr);  // 10
    results.last = get_last(test_arr);    // 50
    return results;
}

// Test 10: Arrow function with object operations
function test_arrow_object_ops() {
    get_x = fn(obj) => obj.x;
    get_y = fn(obj) => obj.y;

    point = {x: 100, y: 200};

    results = {};
    results.x_val = get_x(point);  // 100
    results.y_val = get_y(point);  // 200
    return results;
}

// Test 11: Arrow function in array filter pattern
function test_arrow_filter_pattern() {
    arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    is_even = fn(x) => x % 2 == 0;

    evens = [];
    i = 0;
    while (i < 10) {
        if (is_even(arr[i])) {
            evens = evens + [arr[i]];
        }
        i = i + 1;
    }

    return evens;  // Should be [2, 4, 6, 8, 10]
}

// Test 12: Arrow function with complex expression
function test_arrow_complex_expression() {
    // Calculate sum + product using a single expression
    calculate = fn(a, b) => (a + b) + (a * b);

    val = calculate(3, 4);
    return val;  // Should be 19 (7 + 12)
}

// Test 13: Array of arrow functions (dispatch table)
function test_arrow_dispatch() {
    operations = [
        fn(x) => x + 10,
        fn(x) => x * 2,
        fn(x) => x * x
    ];

    results = [];
    value = 5;

    i = 0;
    while (i < 3) {
        // Extract function to variable first, then call
        func = operations[i];
        result = func(value);
        results = results + [result];
        i = i + 1;
    }

    return results;  // Should be [15, 10, 25]
}

// Test 14: Arrow function composition
function compose(f, g) {
    return fn(x) => f(g(x));
}

function test_arrow_composition() {
    add_one = fn(x) => x + 1;
    double = fn(x) => x * 2;

    double_then_add_one = compose(add_one, double);
    result = double_then_add_one(5);  // (5 * 2) + 1 = 11

    return result;
}

// Test 15: Arrow function with logical operations
function test_arrow_logical() {
    and_fn = fn(a, b) => a && b;
    or_fn = fn(a, b) => a || b;
    not_fn = fn(a) => !a;

    results = {};
    results.and_true = and_fn(true, true);     // true
    results.and_false = and_fn(true, false);   // false
    results.or_true = or_fn(false, true);      // true
    results.or_false = or_fn(false, false);    // false
    results.not_true = not_fn(true);           // false
    results.not_false = not_fn(false);         // true

    return results;
}

// Main test function
function main() {
    results = {};

    results.simple = test_simple_arrow();
    results.multiple_params = test_arrow_multiple_params();
    results.no_params = test_arrow_no_params();
    results.expression = test_arrow_expression();
    results.map = test_arrow_map_pattern();
    results.as_arg = test_arrow_as_argument();
    results.currying = test_arrow_currying();
    results.conditional = test_arrow_conditional();
    results.array_ops = test_arrow_array_ops();
    results.object_ops = test_arrow_object_ops();
    results.filter = test_arrow_filter_pattern();
    results.complex_expr = test_arrow_complex_expression();
    results.dispatch = test_arrow_dispatch();
    results.composition = test_arrow_composition();
    results.logical = test_arrow_logical();

    return results;
}

// Run tests
test_results = main();
