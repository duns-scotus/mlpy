// Test core language: Nested dictionary transformation
// Features tested: dictionaries, recursion, type checking, nested structures
// NO external function calls - pure language features only

// Helper: get array length using try/except
function get_length(arr) {
    len = 0;
    try {
        i = 0;
        while (true) {
            temp = arr[i];
            i = i + 1;
            len = len + 1;
        }
    } except (e) {
        // Out of bounds
    }
    return len;
}

// Helper: check if value is an array
function is_array(x) {
    try {
        n = x[0];  // If indexing works, it's an array
        return true;
    } except (e) {
        return false;  // If exception, not an array
    }
}

// Helper: check if value is a number
function is_number(x) {
    test = x + 0;  // Try arithmetic
    return test == x || test != test;  // Equal to itself or NaN
}

// Helper: simple type checking (returns "array", "number", or "other")
function get_type(value) {
    if (is_array(value)) {
        return "array";
    }
    if (is_number(value)) {
        return "number";
    }
    return "other";  // strings, objects, etc.
}

// Deep clone dictionary/object
function deep_clone(obj) {
    obj_type = get_type(obj);

    if (obj_type == "array") {
        result = [];
        len = get_length(obj);
        i = 0;
        while (i < len) {
            result = result + [deep_clone(obj[i])];
            i = i + 1;
        }
        return result;
    }

    // For numbers, strings, objects - just return as is
    return obj;
}

// Transform nested dictionary - multiply all numbers by factor
function transform_multiply(obj, factor) {
    obj_type = get_type(obj);

    if (obj_type == "number") {
        return obj * factor;
    }

    if (obj_type == "array") {
        result = [];
        len = get_length(obj);
        i = 0;
        while (i < len) {
            result = result + [transform_multiply(obj[i], factor)];
            i = i + 1;
        }
        return result;
    }

    // For strings, objects, etc. - return as is
    return obj;
}

// Transform: capitalize string values
function transform_capitalize(obj) {
    obj_type = get_type(obj);

    if (obj_type == "array") {
        result = [];
        len = get_length(obj);
        i = 0;
        while (i < len) {
            result = result + [transform_capitalize(obj[i])];
            i = i + 1;
        }
        return result;
    }

    // For numbers, strings, objects - return as is
    return obj;
}

// Flatten nested structure into array
function flatten(obj, result) {
    obj_type = get_type(obj);

    if (obj_type == "array") {
        len = get_length(obj);
        i = 0;
        while (i < len) {
            result = flatten(obj[i], result);
            i = i + 1;
        }
        return result;
    }

    // If not array, append to result (numbers, strings, etc.)
    result = result + [obj];
    return result;
}

// Map function over nested structure
function map_nested(obj, func) {
    obj_type = get_type(obj);

    if (obj_type == "array") {
        result = [];
        len = get_length(obj);
        i = 0;
        while (i < len) {
            result = result + [map_nested(obj[i], func)];
            i = i + 1;
        }
        return result;
    }

    if (obj_type == "number") {
        return func(obj);
    }

    // For strings, objects - return as is
    return obj;
}

// Filter numbers greater than threshold
function filter_numbers(obj, threshold, result) {
    obj_type = get_type(obj);

    if (obj_type == "number") {
        if (obj > threshold) {
            result = result + [obj];
        }
        return result;
    }

    if (obj_type == "array") {
        len = get_length(obj);
        i = 0;
        while (i < len) {
            result = filter_numbers(obj[i], threshold, result);
            i = i + 1;
        }
        return result;
    }

    return result;
}

// Sum all numbers in nested structure
function sum_all_numbers(obj) {
    obj_type = get_type(obj);

    if (obj_type == "number") {
        return obj;
    }

    if (obj_type == "array") {
        sum = 0;
        len = get_length(obj);
        i = 0;
        while (i < len) {
            sum = sum + sum_all_numbers(obj[i]);
            i = i + 1;
        }
        return sum;
    }

    return 0;
}

// Count depth of nested structure
function max_depth(obj) {
    obj_type = get_type(obj);

    if (obj_type == "array") {
        max = 0;
        len = get_length(obj);
        i = 0;
        while (i < len) {
            depth = max_depth(obj[i]);
            if (depth > max) {
                max = depth;
            }
            i = i + 1;
        }
        return max + 1;
    }

    return 0;
}

// Main test function
function main() {
    results = {};

    // Test 1: Flatten nested arrays
    nested1 = [1, [2, 3], [[4, 5], 6], 7];
    results.flatten1 = flatten(nested1, []);

    // Test 2: More complex nesting
    nested2 = [[[1, 2]], [3, [4, [5, 6]]], 7];
    results.flatten2 = flatten(nested2, []);

    // Test 3: Map function - double all numbers
    function double(x) {
        return x * 2;
    }

    test_array = [1, [2, 3], [4, [5, 6]]];
    results.mapped = map_nested(test_array, double);

    // Test 4: Sum all numbers in nested structure
    sum_test = [1, [2, 3], [[4, 5], 6]];
    results.sum = sum_all_numbers(sum_test);

    // Test 5: Filter numbers > 3
    filter_test = [1, [2, 5], [[3, 7], 9], 2];
    results.filtered = filter_numbers(filter_test, 3, []);

    // Test 6: Calculate max depth
    depth_test1 = [1, 2, 3];
    depth_test2 = [1, [2, 3]];
    depth_test3 = [1, [2, [3, [4]]]];

    results.depth1 = max_depth(depth_test1);
    results.depth2 = max_depth(depth_test2);
    results.depth3 = max_depth(depth_test3);

    // Test 7: Complex nested structure
    complex = [
        1,
        [2, 3],
        [
            [4, 5],
            [6, [7, 8]]
        ],
        9
    ];

    results.complex_flatten = flatten(complex, []);
    results.complex_sum = sum_all_numbers(complex);
    results.complex_depth = max_depth(complex);

    // Test 8: Transform with custom function
    function triple(x) {
        return x * 3;
    }

    transform_test = [1, [2, [3, 4]], 5];
    results.tripled = map_nested(transform_test, triple);

    return results;
}

// Run tests
test_results = main();
