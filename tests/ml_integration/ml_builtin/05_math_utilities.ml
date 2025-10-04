// Test builtin module: Math utility functions
// Features tested: abs(), min(), max(), round()
// NO imports needed - builtin functions are auto-imported

function test_abs_function() {
    results = {};

    // Absolute value of positive numbers
    results.abs_5 = abs(5);             // 5
    results.abs_3_14 = abs(3.14);       // 3.14

    // Absolute value of negative numbers
    results.abs_neg_5 = abs(-5);        // 5
    results.abs_neg_3_14 = abs(-3.14);  // 3.14

    // Absolute value of zero
    results.abs_zero = abs(0);          // 0
    results.abs_zero_float = abs(0.0);  // 0.0

    // Large numbers
    results.abs_large_pos = abs(10000); // 10000
    results.abs_large_neg = abs(-10000); // 10000

    return results;
}

function test_min_function() {
    results = {};

    // Minimum of multiple arguments
    results.min_1_2_3 = min(1, 2, 3);           // 1
    results.min_5_2_8 = min(5, 2, 8);           // 2
    results.min_neg = min(-5, -2, -8);          // -8
    results.min_mixed = min(10, -5, 0, 3);      // -5

    // Minimum of array
    results.min_array_1 = min([3, 1, 4, 1, 5]); // 1
    results.min_array_2 = min([10, 20, 5, 15]); // 5
    results.min_array_neg = min([-1, -5, -3]);  // -5

    // Single value
    results.min_single = min(42);               // 42

    return results;
}

function test_max_function() {
    results = {};

    // Maximum of multiple arguments
    results.max_1_2_3 = max(1, 2, 3);           // 3
    results.max_5_2_8 = max(5, 2, 8);           // 8
    results.max_neg = max(-5, -2, -8);          // -2
    results.max_mixed = max(10, -5, 0, 3);      // 10

    // Maximum of array
    results.max_array_1 = max([3, 1, 4, 1, 5]); // 5
    results.max_array_2 = max([10, 20, 5, 15]); // 20
    results.max_array_neg = max([-1, -5, -3]);  // -1

    // Single value
    results.max_single = max(42);               // 42

    return results;
}

function test_round_function() {
    results = {};

    // Round with no precision (default 0)
    results.round_3_14 = round(3.14);           // 3.0
    results.round_3_5 = round(3.5);             // 4.0
    results.round_2_7 = round(2.7);             // 3.0
    results.round_neg_2_3 = round(-2.3);        // -2.0
    results.round_neg_2_7 = round(-2.7);        // -3.0

    // Round with precision
    results.round_3_14159_2 = round(3.14159, 2); // 3.14
    results.round_2_71828_3 = round(2.71828, 3); // 2.718
    results.round_123_456_1 = round(123.456, 1); // 123.5

    // Round integers (no change)
    results.round_int = round(42);              // 42.0
    results.round_zero = round(0);              // 0.0

    return results;
}

function test_math_combinations() {
    results = {};

    // abs of min
    numbers1 = [-5, -2, -8, -1];
    min_val = min(numbers1);
    results.abs_min = abs(min_val);             // 8

    // abs of max (negative numbers)
    numbers2 = [-10, -5, -3, -7];
    max_val = max(numbers2);
    results.abs_max = abs(max_val);             // 3

    // round of max
    floats = [3.14, 2.71, 1.41, 2.23];
    max_float = max(floats);
    results.round_max = round(max_float, 1);    // 3.1

    // min/max range
    values = [1, 5, 3, 9, 2, 7];
    min_v = min(values);
    max_v = max(values);
    results.range_min_max = max_v - min_v;      // 8

    return results;
}

function test_math_in_algorithms() {
    results = {};

    // Find absolute differences
    x = 10;
    y = 15;
    diff = abs(x - y);
    results.abs_diff = diff;                    // 5

    // Clamp value between min and max
    value = 150;
    min_bound = 0;
    max_bound = 100;
    clamped = max(min_bound, min(value, max_bound));
    results.clamped = clamped;                  // 100

    // Round to nearest 10
    num = 47;
    rounded_tens = round(num / 10) * 10;
    results.round_tens = rounded_tens;          // 50.0

    return results;
}

function test_distance_calculation() {
    results = {};

    // Manhattan distance (1D)
    x1 = 5;
    x2 = 12;
    manhattan = abs(x1 - x2);
    results.manhattan_1d = manhattan;           // 7

    // Sum of absolute values
    values = [-5, 3, -2, 7, -1];
    sum_abs = 0;
    for (v in values) {
        sum_abs = sum_abs + abs(v);
    }
    results.sum_abs = sum_abs;                  // 18

    return results;
}

function test_statistical_operations() {
    results = {};

    // Find range (max - min)
    data = [23, 45, 12, 67, 34, 89, 11];
    data_min = min(data);
    data_max = max(data);
    data_range = data_max - data_min;
    results.range = data_range;                 // 78

    // Round averages
    sum_val = 0;
    count = len(data);
    for (val in data) {
        sum_val = sum_val + val;
    }
    average = sum_val / count;
    results.avg_rounded = round(average, 1);    // Should be around 40.1

    return results;
}

function main() {
    all_results = {};

    all_results.abs_tests = test_abs_function();
    all_results.min_tests = test_min_function();
    all_results.max_tests = test_max_function();
    all_results.round_tests = test_round_function();
    all_results.combinations = test_math_combinations();
    all_results.algorithms = test_math_in_algorithms();
    all_results.distance = test_distance_calculation();
    all_results.statistics = test_statistical_operations();

    return all_results;
}

// Run tests
test_results = main();
