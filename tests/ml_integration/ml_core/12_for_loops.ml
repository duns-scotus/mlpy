// Test core language: For loops with break and continue
// Features tested: for loops, break, continue, loop control
// NO external function calls - pure language features only

// Test 1: Basic for loop iteration
function test_basic_for() {
    arr = [1, 2, 3, 4, 5];
    sum = 0;

    for (item in arr) {
        sum = sum + item;
    }

    return sum;  // Should be 15
}

// Test 2: For loop with break
function test_for_break() {
    arr = [1, 2, 3, 4, 5];
    sum = 0;

    for (item in arr) {
        if (item == 3) {
            break;
        }
        sum = sum + item;
    }

    return sum;  // Should be 3 (1 + 2, stops before 3)
}

// Test 3: For loop with continue
function test_for_continue() {
    arr = [1, 2, 3, 4, 5];
    sum = 0;

    for (item in arr) {
        if (item == 3) {
            continue;
        }
        sum = sum + item;
    }

    return sum;  // Should be 12 (1 + 2 + 4 + 5, skips 3)
}

// Test 4: Nested for loops
function test_nested_for() {
    outer = [1, 2, 3];
    inner = [10, 20];
    total = 0;

    for (o in outer) {
        for (i in inner) {
            total = total + (o * i);
        }
    }

    return total;  // Should be 180 (1*10 + 1*20 + 2*10 + 2*20 + 3*10 + 3*20)
}

// Test 5: Break in nested for loop (breaks inner only)
function test_nested_break() {
    outer = [1, 2, 3];
    inner = [10, 20, 30];
    results = [];

    for (o in outer) {
        for (i in inner) {
            if (i == 20) {
                break;  // Break inner loop only
            }
            results = results + [(o * i)];
        }
    }

    return results;  // Should be [10, 20, 30]
}

// Test 6: Continue in nested for loop
function test_nested_continue() {
    outer = [1, 2, 3];
    inner = [10, 20, 30];
    results = [];

    for (o in outer) {
        if (o == 2) {
            continue;  // Skip outer iteration when o == 2
        }
        for (i in inner) {
            results = results + [(o * i)];
        }
    }

    return results;  // Should be [10, 20, 30, 30, 60, 90]
}

// Test 7: For loop over empty array
function test_for_empty() {
    arr = [];
    count = 0;

    for (item in arr) {
        count = count + 1;
    }

    return count;  // Should be 0
}

// Test 8: For loop building array
function test_for_build_array() {
    source = [1, 2, 3, 4, 5];
    doubled = [];

    for (num in source) {
        doubled = doubled + [(num * 2)];
    }

    return doubled;  // Should be [2, 4, 6, 8, 10]
}

// Main test function
function main() {
    results = {};

    results.basic = test_basic_for();
    results.break_test = test_for_break();
    results.continue_test = test_for_continue();
    results.nested = test_nested_for();
    results.nested_break = test_nested_break();
    results.nested_continue = test_nested_continue();
    results.empty = test_for_empty();
    results.build_array = test_for_build_array();

    return results;
}

// Run tests
test_results = main();
