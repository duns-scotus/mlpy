// Test core language: All control structures
// Features tested: if/elif/else, while, for, try/except/finally, break/continue
// NO external function calls - pure language features only

// Helper: get array length
function get_length(arr) {
    len = 0;
    try {
        i = 0;
        while (true) {
            temp = arr[i];
            i = i + 1;
            len = len + 1;
        }
    } except (e) {
        // Out of bounds
    }
    return len;
}

// Test if/elif/else
function test_conditionals(value) {
    if (value < 0) {
        return "negative";
    } elif (value == 0) {
        return "zero";
    } elif (value < 10) {
        return "small";
    } elif (value < 100) {
        return "medium";
    } else {
        return "large";
    }
}

// Test nested if/else
function test_nested_if(a, b) {
    if (a > 0) {
        if (b > 0) {
            return "both positive";
        } else {
            return "a positive, b non-positive";
        }
    } else {
        if (b > 0) {
            return "a non-positive, b positive";
        } else {
            return "both non-positive";
        }
    }
}

// Test while loop
function test_while_loop(n) {
    sum = 0;
    i = 1;
    while (i <= n) {
        sum = sum + i;
        i = i + 1;
    }
    return sum;
}

// Test while with break (simulated with condition)
function test_while_break(limit) {
    sum = 0;
    i = 0;
    found = false;

    while (i < 1000 && !found) {
        sum = sum + i;
        if (sum >= limit) {
            found = true;
        }
        i = i + 1;
    }

    return {sum: sum, iterations: i};
}

// Test while with continue (simulated with if)
function test_while_continue(n) {
    sum = 0;
    i = 0;

    while (i < n) {
        i = i + 1;
        // Skip odd numbers (simulate continue)
        remainder = i - (i / 2) * 2;
        if (remainder == 1) {
            // Do nothing (continue)
        } else {
            sum = sum + i;
        }
    }

    return sum;
}

// Test for-in loop (array iteration)
function test_for_loop(arr) {
    sum = 0;

    for (val in arr) {
        sum = sum + val;
    }

    return sum;
}

// Test nested loops
function test_nested_loops(rows, cols) {
    count = 0;
    i = 0;

    while (i < rows) {
        j = 0;
        while (j < cols) {
            count = count + 1;
            j = j + 1;
        }
        i = i + 1;
    }

    return count;
}

// Test try/except
function test_try_except(value) {
    result = {success: false, value: 0, error: null};

    try {
        if (value == 0) {
            throw {message: "Zero not allowed", code: 100};
        }
        result.value = 100 / value;
        result.success = true;
    } except (e) {
        result.error = e;
        result.value = -1;
    }

    return result;
}

// Test try/except/finally
function test_try_finally() {
    result = {steps: [], final_value: 0};

    try {
        result.steps[0] = "try block";
        x = 10;
        result.final_value = x * 2;
    } except (e) {
        result.steps[1] = "except block";
        result.final_value = -1;
    } finally {
        result.steps[2] = "finally block";
        result.final_value = result.final_value + 1;
    }

    return result;
}

// Test nested try/except
function test_nested_try() {
    result = {outer: null, inner: null};

    try {
        result.outer = "outer try";

        try {
            result.inner = "inner try";
            x = 1 / 0;  // This will work in ML
            result.inner = "inner success";
        } except (inner_error) {
            result.inner = "inner caught";
        }

        result.outer = "outer success";
    } except (outer_error) {
        result.outer = "outer caught";
    }

    return result;
}

// Test complex control flow
function test_complex_flow(arr) {
    len = get_length(arr);
    positive_count = 0;
    negative_count = 0;
    zero_count = 0;
    sum = 0;

    i = 0;
    while (i < len) {
        value = arr[i];

        if (value > 0) {
            positive_count = positive_count + 1;
            sum = sum + value;
        } elif (value < 0) {
            negative_count = negative_count + 1;
            // Don't add negative values to sum
        } else {
            zero_count = zero_count + 1;
        }

        i = i + 1;
    }

    return {
        positive: positive_count,
        negative: negative_count,
        zeros: zero_count,
        sum: sum
    };
}

// Test early return in loops
function test_early_return(arr, target) {
    len = get_length(arr);
    i = 0;

    while (i < len) {
        if (arr[i] == target) {
            return {found: true, index: i};
        }
        i = i + 1;
    }

    return {found: false, index: -1};
}

// Test ternary operator (if available, otherwise use if/else)
function test_ternary(a, b) {
    max = a > b ? a : b;
    min = a < b ? a : b;

    return {max: max, min: min};
}

// Test switch-like pattern using if/elif
function test_switch(day) {
    if (day == 1) {
        return "Monday";
    } elif (day == 2) {
        return "Tuesday";
    } elif (day == 3) {
        return "Wednesday";
    } elif (day == 4) {
        return "Thursday";
    } elif (day == 5) {
        return "Friday";
    } elif (day == 6) {
        return "Saturday";
    } elif (day == 7) {
        return "Sunday";
    } else {
        return "Invalid";
    }
}

// Main test function
function main() {
    results = {};

    // Test 1: Conditionals
    results.cond_neg = test_conditionals(-5);
    results.cond_zero = test_conditionals(0);
    results.cond_small = test_conditionals(7);
    results.cond_medium = test_conditionals(50);
    results.cond_large = test_conditionals(200);

    // Test 2: Nested if
    results.nested_pp = test_nested_if(5, 3);
    results.nested_pn = test_nested_if(5, -3);
    results.nested_np = test_nested_if(-5, 3);
    results.nested_nn = test_nested_if(-5, -3);

    // Test 3: While loop
    results.while_10 = test_while_loop(10);
    results.while_100 = test_while_loop(100);

    // Test 4: While with break
    results.break_50 = test_while_break(50);
    results.break_200 = test_while_break(200);

    // Test 5: While with continue
    results.continue_10 = test_while_continue(10);
    results.continue_20 = test_while_continue(20);

    // Test 6: For-in loop
    for_arr1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    for_arr2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20];
    results.for_10 = test_for_loop(for_arr1);
    results.for_20 = test_for_loop(for_arr2);

    // Test 7: Nested loops
    results.nested_3x3 = test_nested_loops(3, 3);
    results.nested_5x4 = test_nested_loops(5, 4);

    // Test 8: Try/except
    results.try_normal = test_try_except(5);
    results.try_zero = test_try_except(0);

    // Test 9: Try/finally
    results.try_finally = test_try_finally();

    // Test 10: Nested try
    results.nested_try = test_nested_try();

    // Test 11: Complex flow
    test_arr = [5, -3, 0, 8, -1, 0, 12];
    results.complex = test_complex_flow(test_arr);

    // Test 12: Early return
    search_arr = [10, 20, 30, 40, 50];
    results.found = test_early_return(search_arr, 30);
    results.not_found = test_early_return(search_arr, 99);

    // Test 13: Ternary
    results.ternary_5_3 = test_ternary(5, 3);
    results.ternary_2_8 = test_ternary(2, 8);

    // Test 14: Switch pattern
    results.day_1 = test_switch(1);
    results.day_5 = test_switch(5);
    results.day_7 = test_switch(7);
    results.day_invalid = test_switch(99);

    return results;
}

// Run tests
test_results = main();
