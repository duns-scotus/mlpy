// Test builtin module: Iterator functions
// Features tested: iter(), next()
// NO imports needed - builtin functions are auto-imported

function test_basic_iteration() {
    results = {};

    // Create iterator from array
    arr = [1, 2, 3];
    it = iter(arr);

    // Get elements one by one
    results.first = next(it);           // 1
    results.second = next(it);          // 2
    results.third = next(it);           // 3

    return results;
}

function test_next_with_default() {
    results = {};

    // Create iterator
    arr = [10, 20];
    it = iter(arr);

    // Consume all elements
    results.val1 = next(it);                    // 10
    results.val2 = next(it);                    // 20

    // Iterator exhausted - use default
    results.val3 = next(it, "done");            // "done"
    results.val4 = next(it, null);              // null
    results.val5 = next(it, -1);                // -1

    return results;
}

function test_string_iteration() {
    results = {};

    // Iterate over string characters
    text = "abc";
    it = iter(text);

    results.char1 = next(it);           // "a"
    results.char2 = next(it);           // "b"
    results.char3 = next(it);           // "c"
    results.char4 = next(it, "END");    // "END" (exhausted)

    return results;
}

function test_empty_iteration() {
    results = {};

    // Empty array iterator
    empty = [];
    it = iter(empty);

    // Immediately exhausted
    results.first_attempt = next(it, "empty");  // "empty"
    results.second_attempt = next(it, "still_empty");  // "still_empty"

    return results;
}

function test_manual_sum() {
    results = {};

    // Calculate sum manually using iterator
    numbers = [1, 2, 3, 4, 5];
    it = iter(numbers);

    total = 0;
    val = next(it, null);
    while (val != null) {
        total = total + val;
        val = next(it, null);
    }

    results.sum = total;                // 15
    results.expected = sum(numbers);    // 15

    return results;
}

function test_partial_consumption() {
    results = {};

    // Take first N elements from iterator
    data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100];
    it = iter(data);

    // Take only first 3 elements
    first_three = [];
    first_three = first_three + [next(it)];
    first_three = first_three + [next(it)];
    first_three = first_three + [next(it)];

    results.first_three = first_three;  // [10, 20, 30]
    results.count = len(first_three);   // 3

    // Iterator still has more elements
    results.fourth = next(it);          // 40
    results.fifth = next(it);           // 50

    return results;
}

function test_multiple_iterators() {
    results = {};

    // Multiple independent iterators over same array
    arr = [1, 2, 3];

    it1 = iter(arr);
    it2 = iter(arr);

    // Each iterator maintains its own state
    results.it1_first = next(it1);      // 1
    results.it2_first = next(it2);      // 1

    results.it1_second = next(it1);     // 2
    results.it2_second = next(it2);     // 2

    // Advance only it1
    results.it1_third = next(it1);      // 3
    results.it1_done = next(it1, "DONE");  // "DONE"

    // it2 still has one element
    results.it2_third = next(it2);      // 3
    results.it2_done = next(it2, "DONE");  // "DONE"

    return results;
}

function test_collect_from_iterator() {
    results = {};

    // Manually collect elements into array
    source = [100, 200, 300, 400];
    it = iter(source);

    collected = [];
    val = next(it, null);
    while (val != null) {
        collected = collected + [val];
        val = next(it, null);
    }

    results.collected = collected;      // [100, 200, 300, 400]
    results.length = len(collected);    // 4
    results.matches_source = len(collected) == len(source);  // true

    return results;
}

function test_filter_with_iterator() {
    results = {};

    // Filter even numbers using iterator
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    it = iter(numbers);

    evens = [];
    val = next(it, null);
    while (val != null) {
        if (val % 2 == 0) {
            evens = evens + [val];
        }
        val = next(it, null);
    }

    results.evens = evens;              // [2, 4, 6, 8, 10]
    results.count = len(evens);         // 5

    return results;
}

function test_transform_with_iterator() {
    results = {};

    // Transform elements using iterator
    numbers = [1, 2, 3, 4, 5];
    it = iter(numbers);

    squared = [];
    val = next(it, null);
    while (val != null) {
        squared = squared + [val * val];
        val = next(it, null);
    }

    results.squared = squared;          // [1, 4, 9, 16, 25]
    results.first = squared[0];         // 1
    results.last = squared[len(squared) - 1];  // 25

    return results;
}

function test_zip_with_iterators() {
    results = {};

    // Manually zip two arrays using iterators
    arr1 = [1, 2, 3];
    arr2 = ["a", "b", "c"];

    it1 = iter(arr1);
    it2 = iter(arr2);

    pairs = [];
    val1 = next(it1, null);
    val2 = next(it2, null);

    while (val1 != null && val2 != null) {
        pairs = pairs + [[val1, val2]];
        val1 = next(it1, null);
        val2 = next(it2, null);
    }

    results.pairs = pairs;              // [[1, "a"], [2, "b"], [3, "c"]]
    results.count = len(pairs);         // 3
    results.first_pair = pairs[0];      // [1, "a"]

    return results;
}

function test_take_while() {
    results = {};

    // Take elements while condition is true
    numbers = [1, 2, 3, 4, 5, 6, 7, 8];
    it = iter(numbers);

    less_than_5 = [];
    val = next(it, null);

    while (val != null && val < 5) {
        less_than_5 = less_than_5 + [val];
        val = next(it, null);
    }

    results.taken = less_than_5;        // [1, 2, 3, 4]
    results.count = len(less_than_5);   // 4
    results.stopped_at = val;           // 5

    return results;
}

function test_find_first() {
    results = {};

    // Find first element matching condition
    numbers = [1, 3, 5, 8, 10, 11];
    it = iter(numbers);

    found = null;
    val = next(it, null);

    while (val != null) {
        if (val % 2 == 0) {
            found = val;
            val = null;  // Break loop
        } elif (val != null) {
            val = next(it, null);
        }
    }

    results.first_even = found;         // 8

    return results;
}

function test_enumerate_manual() {
    results = {};

    // Manually enumerate using iterator
    items = ["a", "b", "c"];
    it = iter(items);

    indexed = [];
    index = 0;
    val = next(it, null);

    while (val != null) {
        indexed = indexed + [[index, val]];
        index = index + 1;
        val = next(it, null);
    }

    results.indexed = indexed;          // [[0, "a"], [1, "b"], [2, "c"]]
    results.count = len(indexed);       // 3

    return results;
}

function test_range_iteration() {
    results = {};

    // Iterate over range
    r = range(5);  // [0, 1, 2, 3, 4]
    it = iter(r);

    sum_val = 0;
    count = 0;

    val = next(it, null);
    while (val != null) {
        sum_val = sum_val + val;
        count = count + 1;
        val = next(it, null);
    }

    results.sum = sum_val;              // 10
    results.count = count;              // 5

    return results;
}

function test_nested_iteration() {
    results = {};

    // Nested arrays - iterate outer
    nested = [[1, 2], [3, 4], [5, 6]];
    outer_it = iter(nested);

    flattened = [];
    outer_val = next(outer_it, null);

    while (outer_val != null) {
        // Iterate inner array
        inner_it = iter(outer_val);
        inner_val = next(inner_it, null);

        while (inner_val != null) {
            flattened = flattened + [inner_val];
            inner_val = next(inner_it, null);
        }

        outer_val = next(outer_it, null);
    }

    results.flattened = flattened;      // [1, 2, 3, 4, 5, 6]
    results.count = len(flattened);     // 6

    return results;
}

function test_iterator_state_persistence() {
    results = {};

    // Iterator maintains state between calls
    numbers = [10, 20, 30, 40, 50];
    it = iter(numbers);

    // First batch
    batch1 = [];
    batch1 = batch1 + [next(it)];
    batch1 = batch1 + [next(it)];

    results.batch1 = batch1;            // [10, 20]

    // Second batch (continues from where we left off)
    batch2 = [];
    batch2 = batch2 + [next(it)];
    batch2 = batch2 + [next(it)];

    results.batch2 = batch2;            // [30, 40]

    // Remaining
    results.remaining = next(it);       // 50
    results.exhausted = next(it, "NONE");  // "NONE"

    return results;
}

function test_chunking_with_iterator() {
    results = {};

    // Create chunks of size 2
    data = [1, 2, 3, 4, 5, 6, 7, 8];
    it = iter(data);

    chunks = [];
    val = next(it, null);

    while (val != null) {
        chunk = [val];
        next_val = next(it, null);

        if (next_val != null) {
            chunk = chunk + [next_val];
        }

        chunks = chunks + [chunk];
        val = next(it, null);
    }

    results.chunks = chunks;            // [[1, 2], [3, 4], [5, 6], [7, 8]]
    results.chunk_count = len(chunks);  // 4
    results.first_chunk = chunks[0];    // [1, 2]

    return results;
}

function main() {
    all_results = {};

    all_results.basic = test_basic_iteration();
    all_results.with_default = test_next_with_default();
    all_results.string_iter = test_string_iteration();
    all_results.empty = test_empty_iteration();
    all_results.manual_sum = test_manual_sum();
    all_results.partial = test_partial_consumption();
    all_results.multiple = test_multiple_iterators();
    all_results.collect = test_collect_from_iterator();
    all_results.filter = test_filter_with_iterator();
    all_results.transform = test_transform_with_iterator();
    all_results.zip_manual = test_zip_with_iterators();
    all_results.take_while = test_take_while();
    all_results.find_first = test_find_first();
    all_results.enumerate = test_enumerate_manual();
    all_results.range_iter = test_range_iteration();
    all_results.nested = test_nested_iteration();
    all_results.state = test_iterator_state_persistence();
    all_results.chunking = test_chunking_with_iterator();

    return all_results;
}

// Run tests
test_results = main();
