// Test stdlib module: collections - Advanced operations
// Features tested: sort, reverse, take, drop, chunk, groupBy
// Module: collections

import collections;

function test_sort() {
    results = {};

    arr = [3, 1, 4, 1, 5, 9, 2];
    sorted_arr = collections.sort(arr);

    results.count = len(sorted_arr);        // 7
    results.first = sorted_arr[0];          // 1
    results.last = sorted_arr[6];           // 9

    return results;
}

function test_reverse() {
    results = {};

    arr = [1, 2, 3, 4, 5];
    reversed_arr = collections.reverse(arr);

    results.first = reversed_arr[0];        // 5
    results.last = reversed_arr[4];         // 1

    return results;
}

function test_take() {
    results = {};

    arr = [1, 2, 3, 4, 5, 6, 7, 8, 9];
    first_three = collections.take(arr, 3);

    results.count = len(first_three);       // 3
    results.first = first_three[0];         // 1
    results.last = first_three[2];          // 3

    return results;
}

function test_drop() {
    results = {};

    arr = [1, 2, 3, 4, 5];
    after_drop = collections.drop(arr, 2);

    results.count = len(after_drop);        // 3
    results.first = after_drop[0];          // 3

    return results;
}

function test_chunk() {
    results = {};

    arr = [1, 2, 3, 4, 5, 6, 7, 8];
    chunks = collections.chunk(arr, 3);

    results.chunk_count = len(chunks);      // 3
    results.first_chunk_len = len(chunks[0]); // 3
    results.last_chunk_len = len(chunks[2]);  // 2

    return results;
}

function test_every() {
    results = {};

    function is_positive(x) { return x > 0; }
    arr1 = [1, 2, 3, 4];
    arr2 = [1, -2, 3, 4];

    results.all_positive = collections.every(arr1, is_positive);  // true
    results.not_all = collections.every(arr2, is_positive);       // false

    return results;
}

function test_some() {
    results = {};

    function is_even(x) { return x % 2 == 0; }
    arr1 = [1, 3, 5, 7];
    arr2 = [1, 2, 3];

    results.no_evens = collections.some(arr1, is_even);   // false
    results.has_even = collections.some(arr2, is_even);   // true

    return results;
}

function test_find() {
    results = {};

    function greater_than_5(x) { return x > 5; }
    arr = [1, 3, 5, 7, 9];
    found = collections.find(arr, greater_than_5);

    results.found = found;                  // 7

    return results;
}

function main() {
    all_results = {};

    all_results.sort = test_sort();
    all_results.reverse = test_reverse();
    all_results.take = test_take();
    all_results.drop = test_drop();
    all_results.chunk = test_chunk();
    all_results.every = test_every();
    all_results.some = test_some();
    all_results.find = test_find();

    return all_results;
}

// Run tests
test_results = main();
