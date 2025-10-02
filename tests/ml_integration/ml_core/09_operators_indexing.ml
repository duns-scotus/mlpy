// Test core language: All operators and indexing
// Features tested: arithmetic, comparison, logical, bitwise, indexing, slicing
// NO external function calls - pure language features only

// Helper: get array length
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

// Test arithmetic operators
function test_arithmetic() {
    a = 10;
    b = 3;

    return {
        add: a + b,          // 13
        subtract: a - b,     // 7
        multiply: a * b,     // 30
        divide: a / b,       // 3 (integer division)
        modulo: a - (a / b) * b,  // 1 (manual modulo)
        negate: -a,          // -10
        complex: (a + b) * 2 - b  // 23
    };
}

// Test comparison operators
function test_comparison() {
    a = 5;
    b = 3;
    c = 5;

    return {
        equal: a == c,           // true
        not_equal: a != b,       // true (using !=)
        greater: a > b,          // true
        less: b < a,             // true
        greater_equal: a >= c,   // true
        less_equal: b <= a,      // true
        chain: a > b && b > 0    // true
    };
}

// Test logical operators
function test_logical() {
    return {
        and_true: true && true,         // true
        and_false: true && false,       // false
        or_true: false || true,         // true
        or_false: false || false,       // false
        not_true: !false,               // true
        not_false: !true,               // false
        complex: (5 > 3) && (2 < 4),   // true
        short_circuit: true || (1 / 0 == 0)  // should short-circuit before division
    };
}

// Test increment/decrement patterns
function test_inc_dec() {
    a = 10;
    b = a + 1;  // Increment
    c = a - 1;  // Decrement

    a = a + 1;  // In-place increment
    d = a;      // 11

    a = a - 1;  // In-place decrement
    e = a;      // 10

    return {
        inc: b,      // 11
        dec: c,      // 9
        after_inc: d, // 11
        after_dec: e  // 10
    };
}

// Test compound assignments (simulated)
function test_compound() {
    a = 5;
    a = a + 3;   // +=
    add_result = a;

    a = a - 2;   // -=
    sub_result = a;

    a = a * 4;   // *=
    mul_result = a;

    a = a / 2;   // /=
    div_result = a;

    return {
        add: add_result,  // 8
        sub: sub_result,  // 6
        mul: mul_result,  // 24
        div: div_result   // 12
    };
}

// Test array indexing
function test_array_indexing() {
    arr = [10, 20, 30, 40, 50];

    return {
        first: arr[0],     // 10
        second: arr[1],    // 20
        third: arr[2],     // 30
        last: arr[4],      // 50
        middle: arr[2]     // 30
    };
}

// Test array assignment
function test_array_assignment() {
    arr = [1, 2, 3, 4, 5];

    arr[0] = 10;
    arr[2] = 30;
    arr[4] = 50;

    return {
        modified: arr,
        first: arr[0],   // 10
        third: arr[2],   // 30
        fifth: arr[4]    // 50
    };
}

// Test nested array indexing
function test_nested_indexing() {
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ];

    return {
        row0_col0: matrix[0][0],  // 1
        row0_col2: matrix[0][2],  // 3
        row1_col1: matrix[1][1],  // 5
        row2_col0: matrix[2][0],  // 7
        row2_col2: matrix[2][2]   // 9
    };
}

// Test object property access
function test_object_access() {
    obj = {
        name: "test",
        value: 42,
        nested: {
            inner: 100
        }
    };

    return {
        name: obj.name,              // "test"
        value: obj.value,            // 42
        nested_inner: obj.nested.inner  // 100
    };
}

// Test object property assignment
function test_object_assignment() {
    obj = {x: 1, y: 2, z: 3};

    obj.x = 10;
    obj.y = 20;
    obj.z = 30;

    return {
        modified: obj,
        x: obj.x,  // 10
        y: obj.y,  // 20
        z: obj.z   // 30
    };
}

// Test mixed indexing (array of objects)
function test_mixed_indexing() {
    data = [
        {id: 1, value: 10},
        {id: 2, value: 20},
        {id: 3, value: 30}
    ];

    return {
        first_id: data[0].id,       // 1
        second_value: data[1].value, // 20
        third_id: data[2].id        // 3
    };
}

// Test operator precedence
function test_precedence() {
    return {
        mult_first: 2 + 3 * 4,           // 14
        parens: (2 + 3) * 4,             // 20
        complex: 10 + 5 * 2 - 3,         // 17
        with_parens: (10 + 5) * (2 - 3), // -15
        logical: 5 > 3 && 2 < 4,         // true
        compare_arith: 2 + 3 > 4         // true (5 > 4)
    };
}

// Test ternary operator
function test_ternary() {
    a = 10;
    b = 5;

    max = a > b ? a : b;
    min = a < b ? a : b;
    equal = a == b ? "equal" : "not equal";

    nested = a > b ? (a > 15 ? "very large" : "medium") : "small";

    return {
        max: max,           // 10
        min: min,           // 5
        equal: equal,       // "not equal"
        nested: nested      // "medium"
    };
}

// Test string concatenation
function test_string_ops() {
    str1 = "Hello";
    str2 = "World";
    num = 42;

    return {
        concat: str1 + " " + str2,  // "Hello World"
        with_num: str1 + " " + num, // "Hello 42" (if supported)
        repeated: str1 + str1       // "HelloHello"
    };
}

// Test boundary conditions
function test_boundaries() {
    arr = [1, 2, 3];

    // Test accessing boundaries
    first = arr[0];
    last = arr[2];

    // Test with calculations
    len = 3;
    calculated_last = arr[len - 1];

    return {
        first: first,
        last: last,
        calculated: calculated_last,
        zero_index: arr[0],
        max_index: arr[2]
    };
}

// Test expression evaluation order
function test_evaluation_order() {
    counter = 0;

    function increment() {
        counter = counter + 1;
        return counter;
    }

    // Each call should increment
    a = increment();  // 1
    b = increment();  // 2
    c = increment();  // 3

    return {
        a: a,
        b: b,
        c: c,
        counter: counter
    };
}

// Main test function
function main() {
    results = {};

    results.arithmetic = test_arithmetic();
    results.comparison = test_comparison();
    results.logical = test_logical();
    results.inc_dec = test_inc_dec();
    results.compound = test_compound();
    results.array_index = test_array_indexing();
    results.array_assign = test_array_assignment();
    results.nested_index = test_nested_indexing();
    results.object_access = test_object_access();
    results.object_assign = test_object_assignment();
    results.mixed_index = test_mixed_indexing();
    results.precedence = test_precedence();
    results.ternary = test_ternary();
    results.string_ops = test_string_ops();
    results.boundaries = test_boundaries();
    results.eval_order = test_evaluation_order();

    return results;
}

// Run tests
test_results = main();
