// Main program for debugging test suite
// Tests: module integration, complex workflows, multiple function calls

// Note: In current ML, imports don't work between test files
// So we'll include all functionality inline for now

// Math utilities
function abs(x) {
    if (x < 0) {
        return -x;
    }
    return x;
}

function max(a, b) {
    if (a > b) {
        return a;
    }
    return b;
}

function factorial(n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

// List operations
function list_length(list) {
    count = 0;
    for (item in list) {
        count = count + 1;
    }
    return count;
}

function list_sum(list) {
    total = 0;
    for (item in list) {
        total = total + item;
    }
    return total;
}

function list_max(list) {
    if (list_length(list) == 0) {
        return 0;
    }
    max_val = list[0];
    for (item in list) {
        if (item > max_val) {
            max_val = item;
        }
    }
    return max_val;
}

// Search algorithms
function linear_search(list, target) {
    i = 0;
    len = list_length(list);

    while (i < len) {
        if (list[i] == target) {
            return i;
        }
        i = i + 1;
    }
    return -1;
}

function binary_search(list, target) {
    left = 0;
    right = list_length(list) - 1;

    while (left <= right) {
        mid = (left + right) // 2;  // Use integer division

        if (list[mid] == target) {
            return mid;
        } elif (list[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    return -1;
}

// Sorting algorithms
function bubble_sort(list) {
    len = list_length(list);

    // Make a copy
    result = [];
    for (item in list) {
        result = result + [item];
    }

    i = 0;
    while (i < len - 1) {
        j = 0;
        while (j < len - i - 1) {
            if (result[j] > result[j + 1]) {
                // Swap
                temp = result[j];
                result[j] = result[j + 1];
                result[j + 1] = temp;
            }
            j = j + 1;
        }
        i = i + 1;
    }
    return result;
}

// Tree operations
function create_node(value, left, right) {
    node = {};
    node.value = value;
    node.left = left;
    node.right = right;
    node.is_leaf = false;
    return node;
}

function create_empty_node() {
    node = {};
    node.value = 0;
    node.left = {};
    node.right = {};
    node.is_leaf = true;
    return node;
}

function is_empty_node(node) {
    // Check if node has no value property (empty dict)
    if (node == {}) {
        return true;
    }
    return false;
}

function tree_sum(node) {
    // Check if empty dict
    has_value = false;
    if (node.value != 0) {
        has_value = true;
    }
    if (node.value == 0) {
        has_value = true;
    }

    if (!has_value) {
        return 0;
    }

    left_sum = tree_sum(node.left);
    right_sum = tree_sum(node.right);
    return node.value + left_sum + right_sum;
}

// Test functions that exercise debugging features
function test_arithmetic() {
    results = {};

    // Basic operations - good for step-through
    a = 10;
    b = 20;
    c = a + b;
    d = c * 2;
    e = d - 5;

    results.sum = c;
    results.product = d;
    results.difference = e;
    results.abs_neg = abs(-42);
    results.max_val = max(100, 50);

    return results;
}

function test_loops() {
    results = {};

    // Simple while loop
    count = 0;
    i = 1;
    while (i <= 10) {
        count = count + i;
        i = i + 1;
    }
    results.while_sum = count;

    // For loop with array
    numbers = [1, 2, 3, 4, 5];
    total = 0;
    for (num in numbers) {
        total = total + num;
    }
    results.for_sum = total;

    return results;
}

function test_conditionals() {
    results = {};

    // If-elif-else chain
    score = 85;
    grade = "";

    if (score >= 90) {
        grade = "A";
    } elif (score >= 80) {
        grade = "B";
    } elif (score >= 70) {
        grade = "C";
    } else {
        grade = "F";
    }

    results.grade = grade;
    results.score = score;

    return results;
}

function test_recursion() {
    results = {};

    // Factorial
    results.fact_5 = factorial(5);
    results.fact_7 = factorial(7);

    return results;
}

function test_arrays() {
    results = {};

    // Array operations
    arr = [5, 2, 8, 1, 9, 3];

    results.length = list_length(arr);
    results.sum = list_sum(arr);
    results.max = list_max(arr);

    // Search
    results.find_8 = linear_search(arr, 8);
    results.find_99 = linear_search(arr, 99);

    // Sort
    sorted_arr = bubble_sort(arr);
    results.sorted = sorted_arr;
    results.sorted_first = sorted_arr[0];
    results.sorted_last = sorted_arr[list_length(sorted_arr) - 1];

    // Binary search on sorted array
    results.bin_search_5 = binary_search(sorted_arr, 5);

    return results;
}

function test_objects() {
    results = {};

    // Create objects
    person = {};
    person.name = "Alice";
    person.age = 30;
    person.active = true;

    results.person_name = person.name;
    results.person_age = person.age;

    // Nested objects
    point = {};
    point.x = 10;
    point.y = 20;

    results.point_x = point.x;
    results.point_y = point.y;
    results.distance = abs(point.x) + abs(point.y);

    return results;
}

function test_tree_structure() {
    results = {};

    // Build a simple tree without empty nodes
    //    10
    //   /  \
    //  5   15

    empty1 = {};
    empty1.value = 0;
    empty1.left = {};
    empty1.right = {};

    empty2 = {};
    empty2.value = 0;
    empty2.left = {};
    empty2.right = {};

    left = create_node(5, empty1, empty1);
    right = create_node(15, empty2, empty2);
    root = create_node(10, left, right);

    // Just sum the values directly
    results.root_value = root.value;
    results.left_value = root.left.value;
    results.right_value = root.right.value;
    results.manual_sum = root.value + root.left.value + root.right.value;

    return results;
}

function main() {
    print("=== ML Debugging Test Suite ===");

    all_results = {};

    // Run all tests
    print("Testing arithmetic...");
    all_results.arithmetic = test_arithmetic();

    print("Testing loops...");
    all_results.loops = test_loops();

    print("Testing conditionals...");
    all_results.conditionals = test_conditionals();

    print("Testing recursion...");
    all_results.recursion = test_recursion();

    print("Testing arrays...");
    all_results.arrays = test_arrays();

    print("Testing objects...");
    all_results.objects = test_objects();

    print("Testing tree structures...");
    all_results.trees = test_tree_structure();

    print("=== All tests completed ===");

    return all_results;
}

// Execute main
test_results = main();
