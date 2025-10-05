// Test stdlib module: collections - Basic list operations
// Features tested: map, filter, reduce, unique, flatten, zip
// Module: collections

import collections;

function test_map() {
    results = {};

    // Map with simple function
    function double(x) { return x * 2; }
    arr = [1, 2, 3, 4];
    doubled = collections.map(arr, double);

    results.count = len(doubled);           // 4
    results.first = doubled[0];             // 2
    results.last = doubled[3];              // 8

    return results;
}

function test_filter() {
    results = {};

    // Filter even numbers
    function is_even(x) { return x % 2 == 0; }
    arr = [1, 2, 3, 4, 5, 6];
    evens = collections.filter(arr, is_even);

    results.count = len(evens);             // 3
    results.first = evens[0];               // 2

    return results;
}

function test_reduce() {
    results = {};

    // Sum with reduce
    function add(acc, x) { return acc + x; }
    arr = [1, 2, 3, 4, 5];
    sum = collections.reduce(arr, add, 0);

    results.sum = sum;                      // 15

    // Product with reduce
    function multiply(acc, x) { return acc * x; }
    product = collections.reduce(arr, multiply, 1);

    results.product = product;              // 120

    return results;
}

function test_unique() {
    results = {};

    arr = [1, 2, 2, 3, 3, 3, 4];
    uniq = collections.unique(arr);

    results.count = len(uniq);              // 4
    results.has_duplicates = len(uniq) < len(arr);

    return results;
}

function test_flatten() {
    results = {};

    nested = [[1, 2], [3, 4], [5, 6]];
    flat = collections.flatten(nested);

    results.count = len(flat);              // 6
    results.first = flat[0];                // 1
    results.last = flat[5];                 // 6

    return results;
}

function test_zip() {
    results = {};

    arr1 = [1, 2, 3];
    arr2 = ["a", "b", "c"];
    zipped = collections.zip(arr1, arr2);

    results.count = len(zipped);            // 3
    results.first = zipped[0];              // [1, "a"]

    return results;
}

function main() {
    all_results = {};

    all_results.map = test_map();
    all_results.filter = test_filter();
    all_results.reduce = test_reduce();
    all_results.unique = test_unique();
    all_results.flatten = test_flatten();
    all_results.zip = test_zip();

    return all_results;
}

// Run tests
test_results = main();
