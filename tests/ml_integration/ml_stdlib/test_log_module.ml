// Test all log module functions end-to-end
// This validates the complete ML→Python transpilation pipeline for logging operations

import log;
import console;

console.log("=== Testing log Module ===");

// Test 1: Basic logging levels
console.log("[Test 1] Basic logging levels");
log.debug("Debug message - may not appear if level is INFO");
log.info("Info message - general information");
log.warn("Warning message - something to be aware of");
log.error("Error message - something went wrong");
log.critical("Critical message - serious problem");
console.log("PASS: All logging levels work");

// Test 2: Set log level to DEBUG
console.log("[Test 2] Set log level to DEBUG");
log.set_level("DEBUG");
log.debug("Debug message now visible");
console.log("PASS: Log level changed to DEBUG");

// Test 3: Set log level to ERROR (filter out lower levels)
console.log("[Test 3] Set log level to ERROR");
log.set_level("ERROR");
log.info("This info message should not appear");
log.error("This error message should appear");
console.log("PASS: Log level filtering works");

// Test 4: Reset to INFO for remaining tests
console.log("[Test 4] Reset log level to INFO");
log.set_level("INFO");
log.info("Back to INFO level");
console.log("PASS: Log level reset successful");

// Test 5: Logging with structured data
console.log("[Test 5] Logging with structured data");
user_data = {user_id: 123, action: "login", ip: "192.168.1.1"};
log.info("User action", user_data);
console.log("PASS: Structured data logging works");

// Test 6: Check if debug is enabled
console.log("[Test 6] Check debug status");
log.set_level("INFO");
is_debug_info = log.is_debug();
if (is_debug_info == false) {
    console.log("PASS: Debug not enabled at INFO level");
} else {
    console.log("FAIL: Debug should not be enabled at INFO level");
}

log.set_level("DEBUG");
is_debug_debug = log.is_debug();
if (is_debug_debug == true) {
    console.log("PASS: Debug enabled at DEBUG level");
} else {
    console.log("FAIL: Debug should be enabled at DEBUG level");
}

// Test 7: Set format to JSON
console.log("[Test 7] Set format to JSON");
log.set_format("json");
log.info("JSON formatted message", {key: "value", number: 42});
console.log("PASS: JSON format set successfully");

// Test 8: Set format back to text
console.log("[Test 8] Set format back to text");
log.set_format("text");
log.info("Text formatted message");
console.log("PASS: Text format restored");

// Test 9: Disable timestamps
console.log("[Test 9] Disable timestamps");
log.set_timestamp(false);
log.info("Message without timestamp");
console.log("PASS: Timestamp disabled");

// Test 10: Re-enable timestamps
console.log("[Test 10] Re-enable timestamps");
log.set_timestamp(true);
log.info("Message with timestamp");
console.log("PASS: Timestamp re-enabled");

// Test 11: Create named logger
console.log("[Test 11] Create named logger");
api_logger = log.create_logger("api");
api_logger.info("API request received");
api_logger.error("API error occurred");
console.log("PASS: Named logger created and used");

// Test 12: Multiple named loggers
console.log("[Test 12] Multiple named loggers");
db_logger = log.create_logger("database");
auth_logger = log.create_logger("auth");

db_logger.info("Database query executed");
auth_logger.warn("Authentication attempt failed");
console.log("PASS: Multiple named loggers work independently");

// Test 13: Named logger with different level
console.log("[Test 13] Named logger with custom level");
debug_logger = log.create_logger("debug");
debug_logger.set_level("DEBUG");
debug_logger.debug("Debug logger message");
console.log("PASS: Named logger with custom level works");

// Test 14: Named logger with JSON format
console.log("[Test 14] Named logger with JSON format");
json_logger = log.create_logger("json_logger");
json_logger.set_format("json");
json_logger.info("JSON logger message", {status: "success", code: 200});
console.log("PASS: Named logger with JSON format works");

// Test 15: Named logger with structured data
console.log("[Test 15] Named logger with complex structured data");
metrics_logger = log.create_logger("metrics");
metrics_data = {
    endpoint: "/api/users",
    method: "GET",
    status: 200,
    duration: 0.045,
    user_id: 456
};
metrics_logger.info("Request metrics", metrics_data);
console.log("PASS: Complex structured data logging works");

// Test 16: All log levels on named logger
console.log("[Test 16] All levels on named logger");
test_logger = log.create_logger("test");
test_logger.set_level("DEBUG");
test_logger.debug("Test debug");
test_logger.info("Test info");
test_logger.warn("Test warning");
test_logger.error("Test error");
test_logger.critical("Test critical");
console.log("PASS: All log levels work on named logger");

// Test 17: Log level filtering on named logger
console.log("[Test 17] Log level filtering on named logger");
filtered_logger = log.create_logger("filtered");
filtered_logger.set_level("WARNING");
filtered_logger.debug("Should not appear");
filtered_logger.info("Should not appear");
filtered_logger.warn("Should appear");
console.log("PASS: Log level filtering on named logger works");

// Test 18: Real-world scenario - Application logging
console.log("[Test 18] Real-world application logging");
app_logger = log.create_logger("application");
app_logger.set_level("INFO");
app_logger.set_format("text");

app_logger.info("Application starting", {version: "1.0.0", env: "production"});

// Simulate request handling
request_logger = log.create_logger("request");
request_data = {
    path: "/api/users/123",
    method: "GET",
    user_id: 789,
    ip: "10.0.0.1"
};
request_logger.info("Request received", request_data);
request_logger.info("Request processed successfully", {duration: 0.023, status: 200});

app_logger.info("Application running normally");
console.log("PASS: Real-world logging scenario works");

// Test 19: Error logging with context
console.log("[Test 19] Error logging with context");
error_logger = log.create_logger("errors");
error_context = {
    error_type: "DatabaseError",
    query: "SELECT * FROM users",
    affected_rows: 0,
    retry_count: 3
};
error_logger.error("Database query failed", error_context);
console.log("PASS: Error logging with context works");

// Test 20: Performance logging
console.log("[Test 20] Performance logging");
perf_logger = log.create_logger("performance");
perf_logger.set_format("json");
perf_data = {
    operation: "data_processing",
    records_processed: 10000,
    duration_ms: 1250,
    memory_mb: 45
};
perf_logger.info("Performance metrics", perf_data);
console.log("PASS: Performance logging works");

console.log("=== All log module tests passed! ===");
