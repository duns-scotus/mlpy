// Test stdlib module: console - Basic output functions
// Features tested: log(), error(), warn(), info(), debug()
// Module: console

import console;

function test_log_function() {
    results = {};

    // Basic logging
    console.log("Test log message");
    console.log("Multiple", "arguments", "in", "log");
    console.log("Number:", 42);
    console.log("Boolean:", true);

    results.log_executed = true;
    return results;
}

function test_error_function() {
    results = {};

    // Error logging
    console.error("Test error message");
    console.error("Error with number:", 404);
    console.error("Error with boolean:", false);

    results.error_executed = true;
    return results;
}

function test_warn_function() {
    results = {};

    // Warning logging
    console.warn("Test warning message");
    console.warn("Warning:", "multiple", "args");

    results.warn_executed = true;
    return results;
}

function test_info_function() {
    results = {};

    // Info logging
    console.info("Test info message");
    console.info("Info:", 123, true, "string");

    results.info_executed = true;
    return results;
}

function test_debug_function() {
    results = {};

    // Debug logging
    console.debug("Test debug message");
    console.debug("Debug value:", 3.14);

    results.debug_executed = true;
    return results;
}

function test_mixed_output() {
    results = {};

    // Mix different log levels
    console.log("Starting process...");
    console.info("Process initialized");
    console.warn("Low memory warning");
    console.error("Critical error occurred");
    console.debug("Debug: variable value = 42");

    results.mixed_executed = true;
    return results;
}

function test_special_values() {
    results = {};

    // Test with arrays
    arr = [1, 2, 3];
    console.log("Array:", arr);

    // Test with objects
    obj = {name: "test", value: 42};
    console.log("Object:", obj);

    // Test with empty values
    console.log("Empty string:", "");
    console.log("Zero:", 0);
    console.log("False:", false);

    results.special_values_tested = true;
    return results;
}

function main() {
    all_results = {};

    all_results.log_tests = test_log_function();
    all_results.error_tests = test_error_function();
    all_results.warn_tests = test_warn_function();
    all_results.info_tests = test_info_function();
    all_results.debug_tests = test_debug_function();
    all_results.mixed_tests = test_mixed_output();
    all_results.special_tests = test_special_values();

    return all_results;
}

// Run tests
test_results = main();
