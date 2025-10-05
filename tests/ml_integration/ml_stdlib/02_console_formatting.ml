// Test stdlib module: console - Formatted output and edge cases
// Features tested: complex objects, nested structures, formatting
// Module: console

import console;

function test_complex_objects() {
    results = {};

    // Nested objects
    user = {
        name: "Alice",
        age: 30,
        address: {
            city: "Paris",
            zip: "75001"
        }
    };
    console.log("User object:", user);

    // Nested arrays
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]];
    console.log("Matrix:", matrix);

    // Mixed nesting
    complex = {
        id: 1,
        tags: ["tag1", "tag2"],
        metadata: {
            created: "2025-10-05",
            items: [10, 20, 30]
        }
    };
    console.log("Complex structure:", complex);

    results.complex_logged = true;
    return results;
}

function test_number_formats() {
    results = {};

    // Various number formats
    console.log("Integer:", 42);
    console.log("Float:", 3.14159);
    console.log("Negative:", -100);
    console.log("Zero:", 0);
    console.log("Large number:", 1000000);

    results.numbers_logged = true;
    return results;
}

function test_string_escapes() {
    results = {};

    // Strings with special characters
    console.log("Newline test:\nSecond line");
    console.log("Tab test:\tTabbed");
    console.log("Quote test: \"quoted\"");

    results.strings_logged = true;
    return results;
}

function test_logging_patterns() {
    results = {};

    // Pattern: Logging computation results
    sum = 10 + 20 + 30;
    console.log("Sum:", sum);

    // Pattern: Logging before/after
    console.debug("Before operation");
    value = 5 * 5;
    console.debug("After operation, result:", value);

    // Pattern: Error reporting
    error_code = 404;
    error_msg = "Not found";
    console.error("Error", error_code, "-", error_msg);

    results.patterns_tested = true;
    return results;
}

function test_loop_logging() {
    results = {};

    // Log in loop
    console.log("Starting loop...");
    i = 0;
    while (i < 3) {
        console.log("Iteration:", i);
        i = i + 1;
    }
    console.log("Loop complete");

    results.loop_logged = true;
    return results;
}

function test_conditional_logging() {
    results = {};

    // Conditional logging
    status = "success";
    if (status == "success") {
        console.info("Operation succeeded");
    } else {
        console.error("Operation failed");
    }

    level = 2;
    if (level == 1) {
        console.log("Level 1");
    } elif (level == 2) {
        console.log("Level 2 - matched");
    } else {
        console.log("Unknown level");
    }

    results.conditional_logged = true;
    return results;
}

function test_function_call_logging() {
    results = {};

    function process(data) {
        console.log("Processing:", data);
        return data * 2;
    }

    result = process(21);
    console.log("Result:", result);

    results.function_logged = true;
    return results;
}

function main() {
    all_results = {};

    console.log("=== Console Module Comprehensive Tests ===");

    all_results.complex = test_complex_objects();
    all_results.numbers = test_number_formats();
    all_results.strings = test_string_escapes();
    all_results.patterns = test_logging_patterns();
    all_results.loops = test_loop_logging();
    all_results.conditionals = test_conditional_logging();
    all_results.functions = test_function_call_logging();

    console.log("=== All Tests Complete ===");

    return all_results;
}

// Run tests
test_results = main();
