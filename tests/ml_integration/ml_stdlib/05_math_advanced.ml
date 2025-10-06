// Test stdlib module: math - Advanced mathematical functions
// Features tested: log(), log10(), exp(), factorial(), gcd(), lcm()
// Module: math

import math;

function test_logarithms() {
    results = {};

    // Natural logarithm (base e)
    e = math.e;
    results.ln_e = math.round(math.ln(e));         // 1
    results.ln_1 = math.round(math.ln(1.0));       // 0
    results.ln_10 = math.round(math.ln(10.0));     // 2

    // Logarithm base 10
    results.log10_1 = math.round(math.log(1.0, 10.0));      // 0
    results.log10_10 = math.round(math.log(10.0, 10.0));    // 1
    results.log10_100 = math.round(math.log(100.0, 10.0));  // 2
    results.log10_1000 = math.round(math.log(1000.0, 10.0)); // 3

    return results;
}

function test_exponential() {
    results = {};

    // Exponential function (e^x)
    results.exp_0 = math.round(math.exp(0.0));      // 1
    results.exp_1 = math.round(math.exp(1.0));      // 3 (e ≈ 2.718)
    results.exp_2 = math.round(math.exp(2.0));      // 7 (e² ≈ 7.389)

    // Verify exp and log are inverses
    value = 5.0;
    exp_then_log = math.log(math.exp(value));
    results.exp_log_inverse = math.round(exp_then_log);  // 5

    return results;
}

function test_factorial() {
    results = {};

    // Factorial function
    results.fact_0 = math.factorial(0);             // 1
    results.fact_1 = math.factorial(1);             // 1
    results.fact_2 = math.factorial(2);             // 2
    results.fact_3 = math.factorial(3);             // 6
    results.fact_4 = math.factorial(4);             // 24
    results.fact_5 = math.factorial(5);             // 120
    results.fact_6 = math.factorial(6);             // 720

    return results;
}

function test_gcd() {
    results = {};

    // Greatest Common Divisor
    results.gcd_12_8 = math.gcd(12, 8);             // 4
    results.gcd_15_25 = math.gcd(15, 25);           // 5
    results.gcd_7_13 = math.gcd(7, 13);             // 1 (coprime)
    results.gcd_100_50 = math.gcd(100, 50);         // 50
    results.gcd_same = math.gcd(42, 42);            // 42

    return results;
}

function test_lcm() {
    results = {};

    // Least Common Multiple
    results.lcm_4_6 = math.lcm(4, 6);               // 12
    results.lcm_3_5 = math.lcm(3, 5);               // 15
    results.lcm_12_8 = math.lcm(12, 8);             // 24
    results.lcm_7_13 = math.lcm(7, 13);             // 91
    results.lcm_same = math.lcm(5, 5);              // 5

    return results;
}

function test_gcd_lcm_relation() {
    results = {};

    // For any two numbers a and b: gcd(a,b) * lcm(a,b) = a * b
    a = 12;
    b = 18;
    gcd_val = math.gcd(a, b);
    lcm_val = math.lcm(a, b);
    product = gcd_val * lcm_val;
    expected = a * b;

    results.gcd_value = gcd_val;                    // 6
    results.lcm_value = lcm_val;                    // 36
    results.relation_holds = product == expected;   // true

    return results;
}

function test_growth_decay() {
    results = {};

    // Exponential growth: A = P * e^(rt)
    // Double your money at 10% interest compounded continuously
    principal = 1000.0;
    rate = 0.10;
    time = 7.0;  // years to double

    amount = principal * math.exp(rate * time);
    results.compound_growth = math.round(amount);   // ~2014

    // Half-life decay: N = N0 * e^(-λt)
    // Carbon-14 half-life simulation
    initial = 100.0;
    decay_rate = 0.693;  // ln(2) / half_life (simplified)
    time_periods = 1.0;

    remaining = initial * math.exp(-decay_rate * time_periods);
    results.decay_amount = math.round(remaining);   // ~50

    return results;
}

function test_statistical_functions() {
    results = {};

    // Use logarithms for very large number calculations
    // log(a*b) = log(a) + log(b)
    log_a = math.log(1000.0);
    log_b = math.log(500.0);
    log_product = log_a + log_b;
    product = math.exp(log_product);
    results.log_multiply = math.round(product / 1000.0);  // 500

    // Use factorial for combinatorics
    // C(5,2) = 5! / (2! * (5-2)!) = 120 / (2 * 6) = 10
    n = 5;
    k = 2;
    numerator = math.factorial(n);
    denominator = math.factorial(k) * math.factorial(n - k);
    combinations = numerator / denominator;
    results.combinations = combinations;            // 10

    return results;
}

function main() {
    all_results = {};

    all_results.logarithms = test_logarithms();
    all_results.exponential = test_exponential();
    all_results.factorial = test_factorial();
    all_results.gcd = test_gcd();
    all_results.lcm = test_lcm();
    all_results.gcd_lcm = test_gcd_lcm_relation();
    all_results.growth = test_growth_decay();
    all_results.statistics = test_statistical_functions();

    return all_results;
}

// Run tests
test_results = main();
