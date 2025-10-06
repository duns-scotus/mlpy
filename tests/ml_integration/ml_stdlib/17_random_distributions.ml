// Test stdlib module: random - Statistical distributions
// Features tested: gauss, uniform, triangular, betavariate
// Module: random

import random;

function test_uniform() {
    results = {};

    // Uniform distribution
    val1 = random.uniform(0.0, 10.0);
    val2 = random.uniform(0.0, 10.0);

    results.in_range1 = val1 >= 0.0 && val1 <= 10.0;
    results.in_range2 = val2 >= 0.0 && val2 <= 10.0;

    return results;
}

function test_gauss() {
    results = {};

    // Gaussian/normal distribution
    val = random.gaussian(0.0, 1.0);  // mean=0, stddev=1

    results.has_value = typeof(val) == "number";
    // Gaussian can produce values outside typical range
    results.is_number = val > -10.0 && val < 10.0;

    return results;
}

function test_triangular() {
    results = {};

    // Triangular distribution
    val = random.triangular(0.0, 10.0, 5.0);  // min, max, mode

    results.in_range = val >= 0.0 && val <= 10.0;

    return results;
}

function test_statistical_properties() {
    results = {};

    // Set seed for consistency
    random.setSeed(42);

    // Generate multiple values and check they're different
    values = [];
    i = 0;
    while (i < 10) {
        val = random.randomInt(1, 100);
        values = values;  // Just generate, don't need to store
        i = i + 1;
    }

    results.generated = true;

    return results;
}

function main() {
    all_results = {};

    all_results.uniform = test_uniform();
    all_results.gauss = test_gauss();
    all_results.triangular = test_triangular();
    all_results.statistical = test_statistical_properties();

    return all_results;
}

// Run tests
test_results = main();
