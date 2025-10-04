// Test builtin module: Sum function
// Features tested: sum()
// NO imports needed - builtin functions are auto-imported

function test_sum_integers() {
    results = {};

    // Sum positive integers
    results.sum_1_to_5 = sum([1, 2, 3, 4, 5]);                  // 15
    results.sum_evens = sum([2, 4, 6, 8, 10]);                  // 30

    // Sum with negative integers
    results.sum_with_neg = sum([10, -5, 3, -2]);                // 6
    results.sum_all_neg = sum([-1, -2, -3, -4]);                // -10

    // Sum with zero
    results.sum_with_zero = sum([1, 0, 2, 0, 3]);               // 6
    results.sum_only_zeros = sum([0, 0, 0]);                    // 0

    // Empty list
    results.sum_empty = sum([]);                                 // 0

    // Single element
    results.sum_single = sum([42]);                              // 42

    return results;
}

function test_sum_floats() {
    results = {};

    // Sum floats
    results.sum_floats = sum([1.5, 2.5, 3.0]);                  // 7.0
    results.sum_decimals = sum([0.1, 0.2, 0.3]);                // 0.6 (approx)

    // Mixed int and float
    results.sum_mixed = sum([1, 2.5, 3, 4.5]);                  // 11.0

    return results;
}

function test_sum_with_start() {
    results = {};

    // Sum with start value
    results.sum_start_10 = sum([1, 2, 3], 10);                  // 16
    results.sum_start_100 = sum([5, 10, 15], 100);              // 130

    // Start with negative
    results.sum_start_neg = sum([10, 20], -5);                  // 25

    // Start with float
    results.sum_start_float = sum([1, 2, 3], 0.5);              // 6.5

    return results;
}

function test_sum_in_calculations() {
    results = {};

    // Calculate average
    values = [10, 20, 30, 40, 50];
    total = sum(values);
    count = len(values);
    average = total / count;

    results.total = total;                                       // 150
    results.count = count;                                       // 5
    results.average = average;                                   // 30.0

    // Calculate percentage
    scores = [85, 90, 95];
    total_score = sum(scores);
    max_possible = 100 * len(scores);
    percentage = (total_score / max_possible) * 100;

    results.total_score = total_score;                           // 270
    results.percentage = round(percentage, 1);                   // 90.0

    return results;
}

function test_sum_with_filtering() {
    results = {};

    // Sum only positive numbers
    numbers = [5, -3, 8, -2, 10, -1];
    positives = [];
    for (n in numbers) {
        if (n > 0) {
            positives = positives + [n];
        }
    }
    results.sum_positives = sum(positives);                      // 23

    // Sum only even numbers
    numbers2 = [1, 2, 3, 4, 5, 6, 7, 8];
    evens = [];
    for (n in numbers2) {
        if ((n - (n / 2) * 2) == 0) {
            evens = evens + [n];
        }
    }
    results.sum_evens = sum(evens);                              // 20

    return results;
}

function test_sum_in_loops() {
    results = {};

    // Cumulative sums
    values = [1, 2, 3, 4, 5];
    cumulative = [];

    for (i in range(len(values))) {
        // Get slice up to i+1
        slice_vals = [];
        for (j in range(i + 1)) {
            slice_vals = slice_vals + [values[j]];
        }
        cumulative = cumulative + [sum(slice_vals)];
    }

    results.cumulative = cumulative;                             // [1, 3, 6, 10, 15]

    return results;
}

function test_sum_for_statistics() {
    results = {};

    // Calculate variance (simplified)
    data = [10, 12, 14, 16, 18];

    // Mean
    total = sum(data);
    count = len(data);
    mean = total / count;

    results.mean = mean;                                         // 14.0

    // Sum of squared differences
    squared_diffs = [];
    for (val in data) {
        diff = val - mean;
        squared_diffs = squared_diffs + [(diff * diff)];
    }

    sum_squared_diffs = sum(squared_diffs);
    results.sum_squared_diffs = sum_squared_diffs;               // 40.0

    return results;
}

function test_sum_with_transformations() {
    results = {};

    // Sum of squares
    numbers = [1, 2, 3, 4, 5];
    squares = [];
    for (n in numbers) {
        squares = squares + [(n * n)];
    }
    results.sum_of_squares = sum(squares);                       // 55

    // Sum of absolute values
    values = [-5, 3, -2, 7, -1];
    abs_values = [];
    for (v in values) {
        abs_values = abs_values + [abs(v)];
    }
    results.sum_of_abs = sum(abs_values);                        // 18

    return results;
}

function test_sum_edge_cases() {
    results = {};

    // Very large sum
    large_nums = [];
    for (i in range(100)) {
        large_nums = large_nums + [100];
    }
    results.large_sum = sum(large_nums);                         // 10000

    // Single large number
    results.single_large = sum([1000000]);                       // 1000000

    // Mix of very large and very small
    results.mixed_scale = sum([1000000, 1, 2, 3]);               // 1000006

    return results;
}

function test_practical_use_cases() {
    results = {};

    // Shopping cart total
    prices = [19.99, 24.99, 9.99, 15.00];
    subtotal = sum(prices);
    tax = subtotal * 0.08;
    total = subtotal + tax;

    results.subtotal = round(subtotal, 2);                       // 69.97
    results.total = round(total, 2);                             // 75.57

    // Grade calculation
    assignments = [85, 90, 88, 92];
    midterm = 78;
    final = 85;

    assignment_avg = sum(assignments) / len(assignments);
    overall = (assignment_avg * 0.5) + (midterm * 0.25) + (final * 0.25);

    results.assignment_avg = round(assignment_avg, 1);           // 88.8
    results.overall = round(overall, 1);                         // 85.1

    return results;
}

function main() {
    all_results = {};

    all_results.integers = test_sum_integers();
    all_results.floats = test_sum_floats();
    all_results.with_start = test_sum_with_start();
    all_results.calculations = test_sum_in_calculations();
    all_results.filtering = test_sum_with_filtering();
    all_results.loops = test_sum_in_loops();
    all_results.statistics = test_sum_for_statistics();
    all_results.transformations = test_sum_with_transformations();
    all_results.edge_cases = test_sum_edge_cases();
    all_results.practical = test_practical_use_cases();

    return all_results;
}

// Run tests
test_results = main();
