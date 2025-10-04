// Test builtin module: Predicate functions
// Features tested: callable(), all(), any()
// NO imports needed - builtin functions are auto-imported

function test_callable_function() {
    results = {};

    // Test with functions
    results.func_is_callable = callable(test_callable_function);    // true

    // Test with non-callables
    results.int_not_callable = callable(42);                       // false
    results.str_not_callable = callable("hello");                  // false
    results.array_not_callable = callable([1, 2, 3]);              // false
    results.obj_not_callable = callable({a: 1});                   // false
    results.bool_not_callable = callable(true);                    // false

    return results;
}

function test_all_function() {
    results = {};

    // All true values
    results.all_true = all([true, true, true]);                    // true
    results.all_numbers = all([1, 2, 3, 4, 5]);                    // true
    results.all_strings = all(["a", "b", "c"]);                    // true

    // With at least one false value
    results.one_false = all([true, false, true]);                  // false
    results.one_zero = all([1, 2, 0, 4]);                          // false
    results.one_empty_str = all(["a", "", "c"]);                   // false

    // Edge cases
    results.all_empty = all([]);                                   // true (vacuous truth)
    results.all_single_true = all([true]);                         // true
    results.all_single_false = all([false]);                       // false

    return results;
}

function test_any_function() {
    results = {};

    // At least one true value
    results.one_true = any([false, false, true]);                  // true
    results.one_number = any([0, 0, 1]);                           // true
    results.one_string = any(["", "", "a"]);                       // true

    // All false values
    results.all_false = any([false, false, false]);                // false
    results.all_zeros = any([0, 0, 0]);                            // false
    results.all_empty_strs = any(["", "", ""]);                    // false

    // All true values
    results.all_true = any([true, true, true]);                    // true
    results.all_numbers = any([1, 2, 3]);                          // true

    // Edge cases
    results.any_empty = any([]);                                   // false
    results.any_single_true = any([true]);                         // true
    results.any_single_false = any([false]);                       // false

    return results;
}

function test_all_with_mixed_types() {
    results = {};

    // Mixed truthy values
    results.mixed_truthy = all([1, "hello", true, [1]]);           // true

    // Mixed with one falsy
    results.mixed_with_zero = all([1, "hello", 0]);                // false
    results.mixed_with_empty_str = all([1, "", true]);             // false
    results.mixed_with_false = all([1, "x", false]);               // false
    results.mixed_with_empty_arr = all([1, "x", []]);              // false

    return results;
}

function test_any_with_mixed_types() {
    results = {};

    // All falsy except one
    results.one_truthy = any([0, "", false, [], 1]);               // true

    // All falsy
    results.all_falsy = any([0, "", false, []]);                   // false

    return results;
}

function test_all_in_validation() {
    results = {};

    // Validate all positive
    numbers1 = [5, 10, 15, 20];
    checks1 = [];
    for (n in numbers1) {
        checks1 = checks1 + [n > 0];
    }
    results.all_positive = all(checks1);                           // true

    // Validate all even
    numbers2 = [2, 4, 6, 8];
    checks2 = [];
    for (n in numbers2) {
        is_even = (n - (n / 2) * 2) == 0;
        checks2 = checks2 + [is_even];
    }
    results.all_even = all(checks2);                               // true

    // Not all even
    numbers3 = [2, 4, 5, 8];
    checks3 = [];
    for (n in numbers3) {
        is_even = (n - (n / 2) * 2) == 0;
        checks3 = checks3 + [is_even];
    }
    results.not_all_even = all(checks3);                           // false

    return results;
}

function test_any_in_search() {
    results = {};

    // Check if any element matches
    numbers1 = [1, 2, 3, 4, 5];
    target1 = 3;
    matches1 = [];
    for (n in numbers1) {
        matches1 = matches1 + [n == target1];
    }
    results.found_3 = any(matches1);                               // true

    // Check if any element matches (not found)
    numbers2 = [1, 2, 4, 5];
    target2 = 3;
    matches2 = [];
    for (n in numbers2) {
        matches2 = matches2 + [n == target2];
    }
    results.not_found_3 = any(matches2);                           // false

    // Check if any element > threshold
    values = [5, 3, 2, 1, 8];
    threshold = 7;
    checks = [];
    for (v in values) {
        checks = checks + [v > threshold];
    }
    results.any_above_threshold = any(checks);                     // true

    return results;
}

function test_combining_all_and_any() {
    results = {};

    // All true AND at least one specific condition
    values = [2, 4, 6, 8];

    all_positive = true;
    for (v in values) {
        if (v <= 0) {
            all_positive = false;
        }
    }

    any_above_5 = false;
    for (v in values) {
        if (v > 5) {
            any_above_5 = true;
        }
    }

    results.all_pos_and_any_high = all_positive && any_above_5;    // true

    return results;
}

function test_short_circuit_behavior() {
    results = {};

    // all() should return false as soon as it finds a false
    large_list = [];
    for (i in range(1000)) {
        large_list = large_list + [true];
    }
    large_list = large_list + [false];  // Add one false

    results.all_with_false_at_end = all(large_list);               // false

    // any() should return true as soon as it finds a true
    large_list2 = [];
    for (i in range(1000)) {
        large_list2 = large_list2 + [false];
    }
    large_list2 = [true] + large_list2;  // Add one true at start

    results.any_with_true_at_start = any(large_list2);             // true

    return results;
}

function test_practical_use_cases() {
    results = {};

    // Validate form data
    username = "alice";
    password = "pass123";
    email = "alice@example.com";

    validations = [
        len(username) > 0,
        len(password) >= 6,
        len(email) > 0
    ];

    results.form_valid = all(validations);                         // true

    // Check if any error occurred
    errors = [false, false, false, false];
    results.has_errors = any(errors);                              // false

    errors_with_one = [false, true, false];
    results.has_errors_2 = any(errors_with_one);                   // true

    return results;
}

function main() {
    all_results = {};

    all_results.callable_tests = test_callable_function();
    all_results.all_tests = test_all_function();
    all_results.any_tests = test_any_function();
    all_results.all_mixed = test_all_with_mixed_types();
    all_results.any_mixed = test_any_with_mixed_types();
    all_results.validation = test_all_in_validation();
    all_results.search = test_any_in_search();
    all_results.combining = test_combining_all_and_any();
    all_results.short_circuit = test_short_circuit_behavior();
    all_results.practical = test_practical_use_cases();

    return all_results;
}

// Run tests
test_results = main();
