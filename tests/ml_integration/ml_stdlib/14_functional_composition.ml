// Test stdlib module: functional - Function composition
// Features tested: compose, pipe, curry, partial
// Module: functional

import functional;

function test_compose() {
    results = {};

    function double(x) { return x * 2; }
    function add_one(x) { return x + 1; }

    // Compose: right to left (add_one first, then double)
    composed = functional.compose(double, add_one);
    result = composed(5);

    results.value = result;                 // 12 ((5+1)*2)

    return results;
}

function test_pipe() {
    results = {};

    function double(x) { return x * 2; }
    function add_one(x) { return x + 1; }

    // Pipe: left to right (double first, then add_one)
    piped = functional.pipe(double, add_one);
    result = piped(5);

    results.value = result;                 // 11 ((5*2)+1)

    return results;
}

function test_curry2() {
    results = {};

    function add(a, b) { return a + b; }

    // Curry2 - two-argument curry
    curried = functional.curry2(add);
    add_five = curried(5);
    result = add_five(3);

    results.value = result;                 // 8

    return results;
}

function test_partition() {
    results = {};

    function is_even(x) { return x % 2 == 0; }
    arr = [1, 2, 3, 4, 5, 6];

    partitioned = functional.partition(arr, is_even);
    evens = partitioned[0];
    odds = partitioned[1];

    results.even_count = len(evens);        // 3
    results.odd_count = len(odds);          // 3

    return results;
}

function test_ifElse() {
    results = {};

    function is_positive(x) { return x > 0; }
    function double(x) { return x * 2; }
    function negate(x) { return -x; }

    // ifElse(predicate, onTrue, onFalse)
    transform = functional.ifElse(is_positive, double, negate);

    results.positive = transform(5);        // 10 (doubled)
    results.negative = transform(-5);       // 5 (negated)

    return results;
}

function test_times() {
    results = {};

    count = 0;
    function increment(i) {
        nonlocal count;
        count = count + 1;
        return count;
    }

    // Execute function N times
    result = functional.times(5, increment);

    results.final_count = count;            // 5
    results.result_len = len(result);       // 5

    return results;
}

function main() {
    all_results = {};

    all_results.compose = test_compose();
    all_results.pipe = test_pipe();
    all_results.curry = test_curry2();
    all_results.partition = test_partition();
    all_results.ifElse = test_ifElse();
    all_results.times = test_times();

    return all_results;
}

// Run tests
test_results = main();
