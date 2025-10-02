// Test core language: Complete exception handling
// Features tested: throw statements, finally clause, try/except/finally
// NO external function calls - pure language features only

// Test 1: Basic throw statement
function test_basic_throw() {
    result = null;

    try {
        throw {
            message: "Test error",
            type: "TestError"
        };
    } except (e) {
        result = "caught";
    }

    return result;  // Should be "caught"
}

// Test 2: Throw with detailed error info
function test_detailed_throw() {
    result = null;

    try {
        throw {
            message: "Division by zero",
            type: "MathError",
            severity: "high",
            code: 500
        };
    } except (e) {
        result = "error_caught";
    }

    return result;  // Should be "error_caught"
}

// Test 3: Finally clause execution
function test_finally_basic() {
    executed = false;

    try {
        x = 10;
    } finally {
        executed = true;
    }

    return executed;  // Should be true
}

// Test 4: Finally with exception
function test_finally_with_exception() {
    cleanup = false;

    try {
        throw {
            message: "Test error",
            type: "Error"
        };
    } except (e) {
        // Handle error
    } finally {
        cleanup = true;
    }

    return cleanup;  // Should be true
}

// Test 5: Try/except/finally all together
function test_complete_exception() {
    results = {};
    results.caught = false;
    results.finally_run = false;

    try {
        throw {
            message: "Complete test",
            type: "TestError"
        };
    } except (e) {
        results.caught = true;
    } finally {
        results.finally_run = true;
    }

    return results;  // Should be {caught: true, finally_run: true}
}

// Test 6: Finally without exception
function test_finally_no_exception() {
    count = 0;

    try {
        count = count + 1;
    } finally {
        count = count + 10;
    }

    return count;  // Should be 11
}

// Test 7: Nested try/finally
function test_nested_finally() {
    outer = false;
    inner = false;

    try {
        try {
            x = 5;
        } finally {
            inner = true;
        }
    } finally {
        outer = true;
    }

    results = {};
    results.inner = inner;  // true
    results.outer = outer;  // true
    return results;
}

// Test 8: Throw in conditional
function divide(a, b) {
    if (b == 0) {
        throw {
            message: "Division by zero",
            type: "MathError"
        };
    }
    return a / b;
}

function test_conditional_throw() {
    result = null;

    try {
        result = divide(10, 0);
    } except (e) {
        result = "error";
    }

    return result;  // Should be "error"
}

// Test 9: Finally with return value
function test_finally_with_return() {
    value = 0;

    try {
        value = 10;
        return value;
    } finally {
        value = 20;  // This changes value but doesn't affect return
    }

    return value;  // This shouldn't be reached
}

// Test 10: Multiple except clauses (if supported)
function test_multiple_operations() {
    results = [];

    // Test 1: No error
    try {
        x = 10;
    } except (e) {
        results = results + ["error1"];
    } finally {
        results = results + ["finally1"];
    }

    // Test 2: With error
    try {
        throw {
            message: "Error",
            type: "TestError"
        };
    } except (e) {
        results = results + ["error2"];
    } finally {
        results = results + ["finally2"];
    }

    return results;  // Should be ["finally1", "error2", "finally2"]
}

// Test 11: Finally with variable updates
function test_finally_variable_update() {
    counter = 0;
    status = "initial";

    try {
        counter = counter + 5;
        status = "try";
    } finally {
        counter = counter + 3;
        status = "finally";
    }

    results = {};
    results.counter = counter;  // 8
    results.status = status;    // "finally"
    return results;
}

// Test 12: Throw in loop
function test_throw_in_loop() {
    results = [];

    i = 0;
    while (i < 5) {
        try {
            if (i == 3) {
                throw {
                    message: "Stop at 3",
                    type: "StopError"
                };
            }
            results = results + [i];
        } except (e) {
            results = results + ["error"];
        }
        i = i + 1;
    }

    return results;  // Should be [0, 1, 2, "error", 4]
}

// Test 13: Finally ensures cleanup
function test_finally_cleanup() {
    resource_open = false;
    resource_closed = false;

    try {
        resource_open = true;
        throw {
            message: "Operation failed",
            type: "Error"
        };
    } except (e) {
        // Handle error
    } finally {
        resource_closed = true;
    }

    results = {};
    results.opened = resource_open;    // true
    results.closed = resource_closed;  // true
    return results;
}

// Test 14: Empty finally block
function test_empty_finally() {
    value = 10;

    try {
        value = value + 5;
    } finally {
        // Empty finally block (should emit pass)
    }

    return value;  // Should be 15
}

// Test 15: Throw with complex error object
function test_complex_error() {
    result = null;

    try {
        throw {
            message: "Complex error",
            type: "ValidationError",
            severity: "medium",
            code: 400,
            details: "Field validation failed"
        };
    } except (e) {
        result = "caught_complex";
    }

    return result;  // Should be "caught_complex"
}

// Main test function
function main() {
    results = {};

    results.basic_throw = test_basic_throw();
    results.detailed_throw = test_detailed_throw();
    results.finally_basic = test_finally_basic();
    results.finally_exception = test_finally_with_exception();
    results.complete = test_complete_exception();
    results.finally_no_exc = test_finally_no_exception();
    results.nested_finally = test_nested_finally();
    results.conditional_throw = test_conditional_throw();
    results.finally_return = test_finally_with_return();
    results.multiple_ops = test_multiple_operations();
    results.var_update = test_finally_variable_update();
    results.throw_loop = test_throw_in_loop();
    results.cleanup = test_finally_cleanup();
    results.empty_finally = test_empty_finally();
    results.complex_error = test_complex_error();

    return results;
}

// Run tests
test_results = main();
