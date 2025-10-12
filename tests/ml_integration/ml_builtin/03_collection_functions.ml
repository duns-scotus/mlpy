// Test builtin module: Collection functions
// Features tested: len(), range(), enumerate()
// NO imports needed - builtin functions are auto-imported

function test_len_function() {
    results = {};

    // Length of strings
    results.len_hello = len("hello");           // 5
    results.len_empty_str = len("");            // 0
    results.len_long_str = len("Hello, World!"); // 13

    // Length of arrays
    results.len_array_5 = len([1, 2, 3, 4, 5]); // 5
    results.len_empty_array = len([]);          // 0
    results.len_nested = len([[1,2], [3,4]]);   // 2

    // Length of objects
    results.len_object_2 = len({a: 1, b: 2});   // 2
    results.len_empty_obj = len({});            // 0
    results.len_object_5 = len({a:1, b:2, c:3, d:4, e:5}); // 5

    return results;
}

function test_range_function() {
    results = {};

    // Range with single argument (0 to n)
    results.range_5 = range(5);                 // [0, 1, 2, 3, 4]
    results.range_3 = range(3);                 // [0, 1, 2]
    results.range_0 = range(0);                 // []
    results.range_1 = range(1);                 // [0]

    // Range with start and stop
    results.range_1_5 = range(1, 5);            // [1, 2, 3, 4]
    results.range_3_7 = range(3, 7);            // [3, 4, 5, 6]
    results.range_0_10 = range(0, 10);          // [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    // Range with start, stop, and step
    results.range_0_10_2 = range(0, 10, 2);     // [0, 2, 4, 6, 8]
    results.range_1_10_3 = range(1, 10, 3);     // [1, 4, 7]
    results.range_0_20_5 = range(0, 20, 5);     // [0, 5, 10, 15]

    return results;
}

function test_enumerate_function() {
    results = {};

    // Basic enumeration
    arr1 = ["a", "b", "c"];
    results.enum_abc = enumerate(arr1);         // [(0,'a'), (1,'b'), (2,'c')]

    // Enumeration with custom start
    arr2 = ["x", "y", "z"];
    results.enum_xyz_from_1 = enumerate(arr2, 1); // [(1,'x'), (2,'y'), (3,'z')]

    // Empty array
    results.enum_empty = enumerate([]);         // []

    // Numbers array
    arr3 = [10, 20, 30, 40];
    results.enum_numbers = enumerate(arr3);     // [(0,10), (1,20), (2,30), (3,40)]

    return results;
}

function test_len_in_loops() {
    results = {};

    // Use len to iterate
    arr = [10, 20, 30, 40, 50];
    arr_len = len(arr);
    sum = 0;
    i = 0;

    while (i < arr_len) {
        sum = sum + arr[i];
        i = i + 1;
    }

    results.sum_using_len = sum;                // 150
    results.array_length = arr_len;             // 5

    // Use len for string operations
    str = "hello";
    str_len = len(str);
    results.string_length = str_len;            // 5

    return results;
}

function test_range_in_loops() {
    results = {};

    // Sum using range
    sum = 0;
    for (i in range(10)) {
        sum = sum + i;
    }
    results.sum_0_to_9 = sum;                   // 45

    // Build array using range
    squares = [];
    for (n in range(1, 6)) {
        squares = squares + [(n * n)];
    }
    results.squares_1_to_5 = squares;           // [1, 4, 9, 16, 25]

    // Even numbers using range with step
    evens = [];
    for (n in range(0, 10, 2)) {
        evens = evens + [n];
    }
    results.evens_0_to_8 = evens;               // [0, 2, 4, 6, 8]

    return results;
}

function test_enumerate_in_loops() {
    print("Testing enumerate in loops...");
    results = {};

    // Use enumerate to get indices and values
    fruits = ["apple", "banana", "cherry"];
    fruit_map = {};

    for (pair in enumerate(fruits)) {
        idx = pair[0];
        fruit = pair[1];
        fruit_map[idx] = fruit;
    }

    results.fruit_0 = fruit_map[0];             // "apple"
    results.fruit_1 = fruit_map[1];             // "banana"
    results.fruit_2 = fruit_map[2];             // "cherry"

    // Use enumerate to find index
    numbers = [5, 10, 15, 20, 25];
    target = 15;
    found_index = -1;

    for (pair in enumerate(numbers)) {
        idx = pair[0];
        val = pair[1];
        if (val == target) {
            found_index = idx;
        }
    }

    results.found_index = found_index;          // 2

    return results;
}

function test_combined_functions() {
    results = {};

    // Create range, get length
    r = range(10, 20);
    results.range_len = len(r);                 // 10

    // Enumerate and get length
    arr = ["a", "b", "c", "d"];
    enum_arr = enumerate(arr);
    results.enum_len = len(enum_arr);           // 4

    // Range in enumerate (indirect)
    r2 = range(5);
    enum_r2 = enumerate(r2);
    results.enum_range_len = len(enum_r2);      // 5

    return results;
}

function main() {
    print("Testing builtin collection functions...");
    all_results = {};
    all_results.len_tests = test_len_function();
    all_results.range_tests = test_range_function();
    all_results.enumerate_tests = test_enumerate_function();
    all_results.len_loops = test_len_in_loops();
    all_results.range_loops = test_range_in_loops();
    all_results.enum_loops = test_enumerate_in_loops();
    all_results.combined = test_combined_functions();

    return all_results;
}

print("Hallo Welt!");
// Run tests
test_results = main();
