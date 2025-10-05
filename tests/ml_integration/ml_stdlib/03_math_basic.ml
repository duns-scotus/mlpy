// Test stdlib module: math - Basic mathematical operations
// Features tested: abs(), ceil(), floor(), round(), sqrt(), pow(), constants
// Module: math

import math;

function test_basic_functions() {
    results = {};

    // Absolute value
    results.abs_positive = math.abs(42);        // 42
    results.abs_negative = math.abs(-42);       // 42
    results.abs_zero = math.abs(0);             // 0
    results.abs_float = math.abs(-3.14);        // 3.14

    // Ceiling
    results.ceil_positive = math.ceil(3.2);     // 4
    results.ceil_negative = math.ceil(-3.2);    // -3
    results.ceil_whole = math.ceil(5.0);        // 5

    // Floor
    results.floor_positive = math.floor(3.8);   // 3
    results.floor_negative = math.floor(-3.8);  // -4
    results.floor_whole = math.floor(5.0);      // 5

    // Round
    results.round_up = math.round(3.6);         // 4
    results.round_down = math.round(3.4);       // 3
    results.round_half = math.round(3.5);       // 4
    results.round_negative = math.round(-3.5);  // -4

    return results;
}

function test_sqrt_function() {
    results = {};

    // Square root
    results.sqrt_4 = math.sqrt(4.0);            // 2.0
    results.sqrt_9 = math.sqrt(9.0);            // 3.0
    results.sqrt_16 = math.sqrt(16.0);          // 4.0
    results.sqrt_2 = math.sqrt(2.0);            // ~1.414

    return results;
}

function test_pow_function() {
    results = {};

    // Power function
    results.pow_2_3 = math.pow(2.0, 3.0);       // 8.0
    results.pow_3_2 = math.pow(3.0, 2.0);       // 9.0
    results.pow_5_0 = math.pow(5.0, 0.0);       // 1.0
    results.pow_2_neg = math.pow(2.0, -1.0);    // 0.5
    results.pow_10_2 = math.pow(10.0, 2.0);     // 100.0

    return results;
}

function test_constants() {
    results = {};

    // Math constants
    pi = math.pi();
    e = math.e();

    results.has_pi = pi > 3.14 && pi < 3.15;
    results.has_e = e > 2.71 && e < 2.72;

    // Use constants in calculations
    results.pi_times_2 = math.round(pi * 2.0);  // 6
    results.e_squared = math.round(math.pow(e, 2.0));  // 7

    return results;
}

function test_min_max() {
    results = {};

    // Min and max
    results.min_2_5 = math.min(2.0, 5.0);       // 2.0
    results.min_neg = math.min(-5.0, -2.0);     // -5.0
    results.max_2_5 = math.max(2.0, 5.0);       // 5.0
    results.max_neg = math.max(-5.0, -2.0);     // -2.0

    return results;
}

function test_sign_function() {
    results = {};

    // Sign function
    results.sign_positive = math.sign(42.0);    // 1
    results.sign_negative = math.sign(-42.0);   // -1
    results.sign_zero = math.sign(0.0);         // 0

    return results;
}

function test_practical_calculations() {
    results = {};

    // Circle area: π * r²
    radius = 5.0;
    area = math.pi() * math.pow(radius, 2.0);
    results.circle_area = math.round(area);     // 79

    // Pythagorean theorem: √(a² + b²)
    a = 3.0;
    b = 4.0;
    c = math.sqrt(math.pow(a, 2.0) + math.pow(b, 2.0));
    results.hypotenuse = c;                     // 5.0

    // Distance formula
    x1 = 0.0;
    y1 = 0.0;
    x2 = 3.0;
    y2 = 4.0;
    dist = math.sqrt(math.pow(x2 - x1, 2.0) + math.pow(y2 - y1, 2.0));
    results.distance = dist;                    // 5.0

    return results;
}

function main() {
    all_results = {};

    all_results.basic = test_basic_functions();
    all_results.sqrt = test_sqrt_function();
    all_results.pow = test_pow_function();
    all_results.constants = test_constants();
    all_results.minmax = test_min_max();
    all_results.sign = test_sign_function();
    all_results.practical = test_practical_calculations();

    return all_results;
}

// Run tests
test_results = main();
