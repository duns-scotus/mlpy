// Test builtin module: Reversed function
// Features tested: reversed()
// NO imports needed - builtin functions are auto-imported

function test_reversed_arrays() {
    results = {};

    // Basic array reversal
    results.reversed_123 = reversed([1, 2, 3]);                 // [3, 2, 1]
    results.reversed_5 = reversed([1, 2, 3, 4, 5]);             // [5, 4, 3, 2, 1]

    // Different types
    results.reversed_strings = reversed(["a", "b", "c"]);       // ["c", "b", "a"]
    results.reversed_mixed = reversed([1, "a", 2, "b"]);        // ["b", 2, "a", 1]

    // Single element
    results.reversed_single = reversed([42]);                   // [42]

    // Empty array
    results.reversed_empty = reversed([]);                      // []

    return results;
}

function test_reversed_strings() {
    results = {};

    // Reverse string (returns array of chars)
    results.reversed_hello = reversed("hello");                 // ['o', 'l', 'l', 'e', 'h']
    results.reversed_abc = reversed("abc");                     // ['c', 'b', 'a']

    // Single character
    results.reversed_single_char = reversed("x");               // ['x']

    // Empty string
    results.reversed_empty_str = reversed("");                  // []

    return results;
}

function test_reversed_with_iteration() {
    results = {};

    // Iterate in reverse
    numbers = [10, 20, 30, 40, 50];
    reversed_nums = reversed(numbers);

    sum_reversed = 0;
    for (n in reversed_nums) {
        sum_reversed = sum_reversed + n;
    }

    results.sum = sum_reversed;                                 // 150
    results.reversed_order = reversed_nums;                     // [50, 40, 30, 20, 10]

    return results;
}

function test_reversed_for_palindrome_check() {
    results = {};

    // Check if array is palindrome
    arr1 = [1, 2, 3, 2, 1];
    arr1_rev = reversed(arr1);

    is_palindrome = true;
    for (i in range(len(arr1))) {
        if (arr1[i] != arr1_rev[i]) {
            is_palindrome = false;
        }
    }

    results.palindrome_check = is_palindrome;                   // true

    // Non-palindrome
    arr2 = [1, 2, 3, 4, 5];
    arr2_rev = reversed(arr2);

    is_palindrome2 = true;
    for (i in range(len(arr2))) {
        if (arr2[i] != arr2_rev[i]) {
            is_palindrome2 = false;
        }
    }

    results.non_palindrome = is_palindrome2;                    // false

    return results;
}

function test_reversed_with_sorting() {
    results = {};

    // Reverse of sorted (descending order)
    nums = [3, 1, 4, 1, 5, 9, 2, 6];
    sorted_nums = sorted(nums);
    descending = reversed(sorted_nums);

    results.descending = descending;                            // [9, 6, 5, 4, 3, 2, 1, 1]
    results.first = descending[0];                              // 9
    results.last = descending[len(descending) - 1];             // 1

    return results;
}

function test_reversed_for_stack_operations() {
    results = {};

    // Simulate stack (LIFO) using reversed
    stack = [1, 2, 3, 4, 5];

    // Pop from end (get reversed, take first)
    reversed_stack = reversed(stack);
    top_element = reversed_stack[0];

    results.top = top_element;                                  // 5

    // Reverse order processing
    processed = [];
    for (item in reversed_stack) {
        processed = processed + [item * 2];
    }

    results.processed = processed;                              // [10, 8, 6, 4, 2]

    return results;
}

function test_reversed_with_range() {
    results = {};

    // Countdown using reversed range
    r = range(1, 11);  // [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    countdown = reversed(r);

    results.countdown = countdown;                              // [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    results.start = countdown[0];                               // 10
    results.end = countdown[len(countdown) - 1];                // 1

    return results;
}

function test_reversed_for_queue_reversal() {
    results = {};

    // Reverse a queue
    queue = ["first", "second", "third", "fourth"];
    reversed_queue = reversed(queue);

    results.original_first = queue[0];                          // "first"
    results.reversed_first = reversed_queue[0];                 // "fourth"

    results.queue_len = len(queue);                             // 4
    results.reversed_len = len(reversed_queue);                 // 4

    return results;
}

function test_reversed_twice() {
    results = {};

    // Reversing twice returns original order
    original = [1, 2, 3, 4, 5];
    once = reversed(original);
    twice = reversed(once);

    results.original = original;                                // [1, 2, 3, 4, 5]
    results.once = once;                                        // [5, 4, 3, 2, 1]
    results.twice = twice;                                      // [1, 2, 3, 4, 5]

    // Check equality
    matches = true;
    for (i in range(len(original))) {
        if (original[i] != twice[i]) {
            matches = false;
        }
    }

    results.matches_original = matches;                         // true

    return results;
}

function test_reversed_nested_arrays() {
    results = {};

    // Reverse array of arrays (outer only)
    nested = [[1, 2], [3, 4], [5, 6]];
    reversed_nested = reversed(nested);

    results.first_subarray = reversed_nested[0];                // [5, 6]
    results.last_subarray = reversed_nested[2];                 // [1, 2]

    return results;
}

function test_reversed_practical_uses() {
    results = {};

    // Recent history (most recent first)
    history = ["page1", "page2", "page3", "page4", "page5"];
    recent_first = reversed(history);

    results.most_recent = recent_first[0];                      // "page5"
    results.oldest = recent_first[len(recent_first) - 1];       // "page1"

    // Undo stack
    actions = ["action1", "action2", "action3"];
    undo_order = reversed(actions);

    results.last_action = undo_order[0];                        // "action3"

    // Backward iteration for animation
    frames = [0, 1, 2, 3, 4];
    reverse_frames = reversed(frames);

    results.frame_count = len(reverse_frames);                  // 5
    results.first_frame = reverse_frames[0];                    // 4

    return results;
}

function main() {
    all_results = {};

    all_results.arrays = test_reversed_arrays();
    all_results.strings = test_reversed_strings();
    all_results.iteration = test_reversed_with_iteration();
    all_results.palindrome = test_reversed_for_palindrome_check();
    all_results.sorting = test_reversed_with_sorting();
    all_results.stack = test_reversed_for_stack_operations();
    all_results.range_rev = test_reversed_with_range();
    all_results.queue = test_reversed_for_queue_reversal();
    all_results.twice = test_reversed_twice();
    all_results.nested = test_reversed_nested_arrays();
    all_results.practical = test_reversed_practical_uses();

    return all_results;
}

// Run tests
test_results = main();
