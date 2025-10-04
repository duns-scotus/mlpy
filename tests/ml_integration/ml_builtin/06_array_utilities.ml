// Test builtin module: Array utility functions
// Features tested: zip(), sorted()
// NO imports needed - builtin functions are auto-imported

function test_zip_function() {
    results = {};

    // Zip two arrays
    arr1 = [1, 2, 3];
    arr2 = ["a", "b", "c"];
    results.zip_nums_letters = zip(arr1, arr2); // [(1,'a'), (2,'b'), (3,'c')]

    // Zip three arrays
    arr3 = [10, 20, 30];
    arr4 = [100, 200, 300];
    arr5 = [1000, 2000, 3000];
    results.zip_three = zip(arr3, arr4, arr5);  // [(10,100,1000), (20,200,2000), (30,300,3000)]

    // Zip arrays of different lengths (shortest wins)
    short = [1, 2];
    long = ["a", "b", "c", "d"];
    results.zip_different = zip(short, long);   // [(1,'a'), (2,'b')]

    // Zip with booleans
    bools = [true, false, true];
    nums = [1, 0, 1];
    results.zip_bools = zip(bools, nums);       // [(true,1), (false,0), (true,1)]

    return results;
}

function test_sorted_function() {
    results = {};

    // Sort integers ascending
    nums1 = [3, 1, 4, 1, 5, 9, 2, 6];
    results.sorted_asc = sorted(nums1);         // [1, 1, 2, 3, 4, 5, 6, 9]

    // Sort integers descending
    nums2 = [3, 1, 4, 1, 5, 9, 2, 6];
    results.sorted_desc = sorted(nums2, true);  // [9, 6, 5, 4, 3, 2, 1, 1]

    // Sort strings
    words = ["zebra", "apple", "mango", "banana"];
    results.sorted_strings = sorted(words);     // ["apple", "banana", "mango", "zebra"]

    // Sort negative numbers
    negs = [-5, -1, -3, -2, -4];
    results.sorted_negs = sorted(negs);         // [-5, -4, -3, -2, -1]

    // Sort mixed positive and negative
    mixed = [3, -1, 4, -2, 0, 5];
    results.sorted_mixed = sorted(mixed);       // [-2, -1, 0, 3, 4, 5]

    // Sort floats
    floats = [3.14, 2.71, 1.41, 2.23, 0.57];
    results.sorted_floats = sorted(floats);     // [0.57, 1.41, 2.23, 2.71, 3.14]

    // Empty array
    results.sorted_empty = sorted([]);          // []

    // Single element
    results.sorted_single = sorted([42]);       // [42]

    return results;
}

function test_zip_and_iterate() {
    results = {};

    // Iterate over zipped arrays
    names = ["Alice", "Bob", "Charlie"];
    ages = [30, 25, 35];
    zipped = zip(names, ages);

    person_info = {};
    for (pair in zipped) {
        name = pair[0];
        age = pair[1];
        person_info[name] = age;
    }

    results.alice_age = person_info["Alice"];   // 30
    results.bob_age = person_info["Bob"];       // 25
    results.charlie_age = person_info["Charlie"]; // 35

    // Sum paired values
    arr_a = [1, 2, 3, 4];
    arr_b = [10, 20, 30, 40];
    zipped2 = zip(arr_a, arr_b);

    pair_sums = [];
    for (pair in zipped2) {
        sum_val = pair[0] + pair[1];
        pair_sums = pair_sums + [sum_val];
    }

    results.pair_sums = pair_sums;              // [11, 22, 33, 44]

    return results;
}

function test_sorted_and_process() {
    results = {};

    // Sort then process
    scores = [85, 92, 78, 95, 88];
    sorted_scores = sorted(scores);

    // Get top 3
    top_3 = [];
    count = 0;
    for (score in sorted(scores, true)) {
        if (count < 3) {
            top_3 = top_3 + [score];
            count = count + 1;
        }
    }

    results.top_3 = top_3;                      // [95, 92, 88]

    // Get median (middle value)
    sorted_s = sorted(scores);
    mid_idx = len(sorted_s) // 2;
    results.median = sorted_s[mid_idx];         // 88

    return results;
}

function test_combining_zip_and_sorted() {
    results = {};

    // Zip and sort by first element
    ids = [3, 1, 4, 2];
    names = ["Charlie", "Alice", "David", "Bob"];

    // Create pairs
    pairs = zip(ids, names);
    results.zipped_pairs = pairs;               // [(3,'Charlie'), (1,'Alice'), (4,'David'), (2,'Bob')]

    // Note: Direct sorting of tuples works in Python
    // For ML, we would need a custom sort implementation
    // Here we just verify the pairs are created correctly

    return results;
}

function test_parallel_arrays() {
    results = {};

    // Parallel array processing
    quantities = [10, 5, 8, 3];
    prices = [2.50, 5.00, 3.25, 10.00];

    // Calculate total cost for each item
    zipped = zip(quantities, prices);
    costs = [];

    for (pair in zipped) {
        qty = pair[0];
        price = pair[1];
        cost = qty * price;
        costs = costs + [cost];
    }

    results.item_costs = costs;                 // [25.0, 25.0, 26.0, 30.0]

    // Total cost
    total = 0;
    for (c in costs) {
        total = total + c;
    }
    results.total_cost = total;                 // 106.0

    return results;
}

function test_sorting_for_ranking() {
    results = {};

    // Rank students by score
    scores = [85, 95, 78, 92, 88];

    // Sort descending for ranking
    sorted_desc = sorted(scores, true);
    results.ranked = sorted_desc;               // [95, 92, 88, 85, 78]

    // Find position of score 88
    position = 0;
    for (s in sorted_desc) {
        position = position + 1;
        if (s == 88) {
            break;
        }
    }

    results.score_88_rank = position;           // 3

    return results;
}

function test_edge_cases() {
    results = {};

    // Zip with empty arrays
    results.zip_empty_1 = zip([], [1, 2, 3]);   // []
    results.zip_empty_2 = zip([1, 2], []);      // []
    results.zip_both_empty = zip([], []);       // []

    // Sort already sorted
    already_sorted = [1, 2, 3, 4, 5];
    results.sort_sorted = sorted(already_sorted); // [1, 2, 3, 4, 5]

    // Sort reverse sorted
    reverse_sorted = [5, 4, 3, 2, 1];
    results.sort_reverse = sorted(reverse_sorted); // [1, 2, 3, 4, 5]

    // Sort duplicates
    dups = [3, 1, 2, 3, 1, 2];
    results.sort_dups = sorted(dups);           // [1, 1, 2, 2, 3, 3]

    return results;
}

function main() {
    all_results = {};

    all_results.zip_tests = test_zip_function();
    all_results.sorted_tests = test_sorted_function();
    all_results.zip_iterate = test_zip_and_iterate();
    all_results.sorted_process = test_sorted_and_process();
    all_results.zip_sorted_combo = test_combining_zip_and_sorted();
    all_results.parallel_arrays = test_parallel_arrays();
    all_results.ranking = test_sorting_for_ranking();
    all_results.edge_cases = test_edge_cases();

    return all_results;
}

// Run tests
test_results = main();
