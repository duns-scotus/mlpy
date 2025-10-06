// Test stdlib module: functional - Advanced functional operations
// Features tested: zipWith, takeWhile, juxt, cond
// Module: functional

import functional;

function test_zipWith() {
    results = {};

    function add(a, b) { return a + b; }
    arr1 = [1, 2, 3];
    arr2 = [10, 20, 30];

    // Zip with custom combiner
    combined = functional.zipWith(add, arr1, arr2);

    results.count = len(combined);          // 3
    results.first = combined[0];            // 11
    results.last = combined[2];             // 33

    return results;
}

function test_takeWhile() {
    results = {};

    function less_than_5(x) { return x < 5; }
    arr = [1, 2, 3, 4, 5, 6, 7];

    taken = functional.takeWhile(less_than_5, arr);

    results.count = len(taken);             // 4
    results.last = taken[3];                // 4

    return results;
}

function test_juxt() {
    results = {};

    function double(x) { return x * 2; }
    function square(x) { return x * x; }
    function add_ten(x) { return x + 10; }

    // Apply multiple functions to same input
    juxted = functional.juxt([double, square, add_ten]);
    result = juxted(5);

    results.double = result[0];             // 10
    results.square = result[1];             // 25
    results.plus_ten = result[2];           // 15

    return results;
}

function test_cond() {
    results = {};

    function is_zero(x) { return x == 0; }
    function is_positive(x) { return x > 0; }
    function is_negative(x) { return x < 0; }

    function return_zero(x) { return "zero"; }
    function return_positive(x) { return "positive"; }
    function return_negative(x) { return "negative"; }

    // Cond: multi-condition dispatcher
    classifier = functional.cond([
        [is_zero, return_zero],
        [is_positive, return_positive],
        [is_negative, return_negative]
    ]);

    results.zero = classifier(0);           // "zero"
    results.pos = classifier(5);            // "positive"
    results.neg = classifier(-3);           // "negative"

    return results;
}

function main() {
    all_results = {};

    all_results.zipWith = test_zipWith();
    all_results.takeWhile = test_takeWhile();
    all_results.juxt = test_juxt();
    all_results.cond = test_cond();

    return all_results;
}

// Run tests
test_results = main();
