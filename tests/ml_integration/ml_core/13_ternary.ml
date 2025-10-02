// Test core language: Ternary operator
// Features tested: ternary conditional expressions (condition ? true_val : false_val)
// NO external function calls - pure language features only

// Test 1: Simple ternary with numbers
function test_simple_ternary() {
    x = 10;
    result = x > 5 ? 100 : 200;
    return result;  // Should be 100
}

// Test 2: Ternary with false condition
function test_ternary_false() {
    x = 3;
    result = x > 5 ? 100 : 200;
    return result;  // Should be 200
}

// Test 3: Ternary in arithmetic expression
function test_ternary_in_expression() {
    x = 7;
    result = (x > 5 ? 10 : 20) + 5;
    return result;  // Should be 15 (10 + 5)
}

// Test 4: Nested ternary
function test_nested_ternary() {
    x = 15;
    result = x > 20 ? "large" : x > 10 ? "medium" : "small";
    return result;  // Should be "medium"
}

// Test 5: Ternary with comparison results
function test_ternary_comparison() {
    a = 10;
    b = 20;
    max = a > b ? a : b;
    return max;  // Should be 20
}

// Test 6: Ternary in return statement
function test_ternary_return(x) {
    return x % 2 == 0 ? "even" : "odd";
}

// Test 7: Ternary with arrays
function test_ternary_arrays() {
    condition = true;
    result = condition ? [1, 2, 3] : [4, 5, 6];
    return result;  // Should be [1, 2, 3]
}

// Test 8: Ternary with objects
function test_ternary_objects() {
    flag = false;
    result = flag ? {x: 1, y: 2} : {x: 3, y: 4};
    return result;  // Should be {x: 3, y: 4}
}

// Test 9: Multiple ternary expressions in one statement
function test_multiple_ternary() {
    x = 10;
    y = 5;
    a = x > 5 ? 1 : 0;
    b = y > 5 ? 1 : 0;
    return a + b;  // Should be 1 (1 + 0)
}

// Test 10: Ternary with logical operators
function test_ternary_logical() {
    x = 10;
    y = 20;
    result = x > 5 && y > 15 ? "both" : "not both";
    return result;  // Should be "both"
}

// Test 11: Ternary chain (like if-elif-else)
function test_ternary_chain() {
    score = 75;
    grade = score >= 90 ? "A" :
            score >= 80 ? "B" :
            score >= 70 ? "C" :
            score >= 60 ? "D" : "F";
    return grade;  // Should be "C"
}

// Test 12: Ternary with null values
function test_ternary_null() {
    x = null;
    result = x == null ? "is null" : "not null";
    return result;  // Should be "is null"
}

// Test 13: Ternary in loop
function test_ternary_in_loop() {
    arr = [1, 2, 3, 4, 5];
    result = [];

    for (num in arr) {
        val = num % 2 == 0 ? num * 2 : num * 3;
        result = result + [val];
    }

    return result;  // Should be [3, 4, 9, 8, 15]
}

// Test 14: Absolute value using ternary
function abs_value(x) {
    return x < 0 ? 0 - x : x;
}

function test_abs_value() {
    results = {};
    results.positive = abs_value(5);    // 5
    results.negative = abs_value(-5);   // 5
    results.zero = abs_value(0);        // 0
    return results;
}

// Test 15: Min/max using ternary
function min(a, b) {
    return a < b ? a : b;
}

function max(a, b) {
    return a > b ? a : b;
}

function test_min_max() {
    results = {};
    results.min_val = min(10, 20);  // 10
    results.max_val = max(10, 20);  // 20
    return results;
}

// Main test function
function main() {
    results = {};

    results.simple = test_simple_ternary();
    results.false_cond = test_ternary_false();
    results.in_expression = test_ternary_in_expression();
    results.nested = test_nested_ternary();
    results.comparison = test_ternary_comparison();
    results.return_even = test_ternary_return(10);
    results.return_odd = test_ternary_return(7);
    results.arrays = test_ternary_arrays();
    results.objects = test_ternary_objects();
    results.multiple = test_multiple_ternary();
    results.logical = test_ternary_logical();
    results.chain = test_ternary_chain();
    results.null_check = test_ternary_null();
    results.in_loop = test_ternary_in_loop();
    results.abs = test_abs_value();
    results.minmax = test_min_max();

    return results;
}

// Run tests
test_results = main();
