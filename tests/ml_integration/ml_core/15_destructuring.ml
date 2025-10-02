// Test core language: Destructuring patterns
// Features tested: array destructuring, object destructuring
// NO external function calls - pure language features only

// Test 1: Simple array destructuring
function test_array_destructuring() {
    arr = [10, 20, 30];
    [a, b, c] = arr;

    results = {};
    results.a = a;  // 10
    results.b = b;  // 20
    results.c = c;  // 30
    return results;
}

// Test 2: Array destructuring with exact match
function test_array_exact() {
    arr = [100, 200];
    [x, y] = arr;

    results = {};
    results.x = x;  // 100
    results.y = y;  // 200
    return results;
}

// Test 3: Object destructuring
function test_object_destructuring() {
    obj = {x: 10, y: 20, z: 30};
    {x, y, z} = obj;

    results = {};
    results.x = x;  // 10
    results.y = y;  // 20
    results.z = z;  // 30
    return results;
}

// Test 4: Object destructuring with exact match
function test_object_exact() {
    obj = {name: "Alice", age: 25};
    {name, age} = obj;

    results = {};
    results.name = name;    // "Alice"
    results.age = age;      // 25
    return results;
}

// Test 5: Destructuring in function
function swap(a, b) {
    temp = [b, a];
    [a, b] = temp;

    results = {};
    results.a = a;
    results.b = b;
    return results;
}

function test_swap() {
    return swap(10, 20);  // Should be {a: 20, b: 10}
}

// Test 6: Destructuring with expressions
function test_destructuring_expression() {
    [a, b] = [5 * 2, 10 + 5];

    results = {};
    results.a = a;  // 10
    results.b = b;  // 15
    return results;
}

// Test 7: Nested data with destructuring
function test_nested_destructuring() {
    point = {x: 100, y: 200};
    {x, y} = point;

    // Use destructured values
    sum = x + y;
    product = x * y;

    results = {};
    results.sum = sum;          // 300
    results.product = product;  // 20000
    return results;
}

// Test 8: Destructuring in loops
function test_destructuring_loop() {
    pairs = [
        [1, 2],
        [3, 4],
        [5, 6]
    ];

    sums = [];

    i = 0;
    while (i < 3) {
        [a, b] = pairs[i];
        sums = sums + [a + b];
        i = i + 1;
    }

    return sums;  // Should be [3, 7, 11]
}

// Test 9: Multiple destructuring assignments
function test_multiple_destructuring() {
    arr1 = [1, 2, 3];
    arr2 = [4, 5, 6];

    [a, b, c] = arr1;
    [d, e, f] = arr2;

    results = {};
    results.from_arr1 = a + b + c;  // 6
    results.from_arr2 = d + e + f;  // 15
    return results;
}

// Test 10: Destructuring with array building
function test_destructuring_build() {
    source = [10, 20];
    [first, second] = source;

    // Build new array from destructured values
    result = [first * 2, second * 2];

    return result;  // Should be [20, 40]
}

// Test 11: Object destructuring with different property names
function test_object_names() {
    data = {
        firstName: "John",
        lastName: "Doe",
        age: 30
    };

    {firstName, lastName, age} = data;

    results = {};
    results.firstName = firstName;
    results.lastName = lastName;
    results.age = age;
    return results;
}

// Test 12: Destructuring return values
function get_point() {
    return {x: 50, y: 100};
}

function test_destructuring_return() {
    {x, y} = get_point();

    results = {};
    results.x = x;  // 50
    results.y = y;  // 100
    return results;
}

// Test 13: Destructuring with calculations
function test_destructuring_calc() {
    [a, b, c] = [5, 10, 15];

    min_val = a < b ? a : b;
    min_val = min_val < c ? min_val : c;

    max_val = a > b ? a : b;
    max_val = max_val > c ? max_val : c;

    results = {};
    results.min = min_val;  // 5
    results.max = max_val;  // 15
    results.sum = a + b + c;  // 30
    return results;
}

// Main test function
function main() {
    results = {};

    results.array_basic = test_array_destructuring();
    results.array_exact = test_array_exact();
    results.object_basic = test_object_destructuring();
    results.object_exact = test_object_exact();
    results.swap = test_swap();
    results.expression = test_destructuring_expression();
    results.nested = test_nested_destructuring();
    results.loop = test_destructuring_loop();
    results.multiple = test_multiple_destructuring();
    results.build = test_destructuring_build();
    results.object_names = test_object_names();
    results.return_val = test_destructuring_return();
    results.calc = test_destructuring_calc();

    return results;
}

// Run tests
test_results = main();
