// ============================================
// Example: Error Reporting with Console
// Category: standard-library/console
// Demonstrates: Comprehensive error reporting patterns
// ============================================

import console;

console.log("=== Error Reporting Example ===\n");

// Example 1: Basic error reporting
console.log("Example 1: Basic error reporting");

function divideNumbers(a, b) {
    if (b == 0) {
        console.error("Division by zero error");
        console.error("  Attempted:", a, "/", b);
        return null;
    }
    return a / b;
}

result = divideNumbers(10, 2);
console.log("10 / 2 =", result);

result = divideNumbers(10, 0);
if (result == null) {
    console.log("Division failed");
}

// Example 2: Exception handling with logging
console.log("\nExample 2: Exception handling");

function processData(value) {
    try {
        console.debug("Processing value:", value);

        if (value < 0) {
            throw {message: "Negative value not allowed"};
        }

        result = value * 2;
        console.info("Processing successful:", result);
        return result;

    } except (err) {
        console.error("Error processing data");
        console.error("  Value:", value);
        console.error("  Error: Negative value not allowed");
        return null;
    }
}

values = [10, -5, 20];
for (val in values) {
    result = processData(val);
    if (result != null) {
        console.log("Result:", result);
    }
}

// Example 3: File operation errors
console.log("\nExample 3: File operation error simulation");

function loadConfig(filename) {
    console.info("Loading configuration from:", filename);

    // Simulate error conditions
    if (filename == "") {
        console.error("Empty filename provided");
        return null;
    }

    if (filename == "missing.conf") {
        console.error("File not found:", filename);
        console.warn("Using default configuration");
        return {setting: "default"};
    }

    console.info("Configuration loaded successfully");
    return {setting: "custom"};
}

files = ["config.conf", "", "missing.conf"];
for (file in files) {
    config = loadConfig(file);
    if (config != null) {
        console.log("Config:", config);
    }
}

// Example 4: Validation errors
console.log("\nExample 4: Data validation errors");

function validateUser(user) {
    errors = [];

    if (!user.name || user.name == "") {
        errors = errors + ["Name is required"];
    }

    if (user.age < 0 || user.age > 150) {
        errors = errors + ["Age must be between 0 and 150"];
    }

    if (len(errors) > 0) {
        console.error("Validation failed for user");
        for (error in errors) {
            console.error("  -", error);
        }
        return false;
    }

    console.info("User validation passed:", user.name);
    return true;
}

users = [
    {name: "Alice", age: 30},
    {name: "", age: 25},
    {name: "Bob", age: 200}
];

validCount = 0;
for (user in users) {
    if (validateUser(user)) {
        validCount = validCount + 1;
    }
}

console.log("Valid users:", validCount, "of", len(users));

// Example 5: Network error simulation
console.log("\nExample 5: Network error handling");

function fetchData(url) {
    console.info("Fetching data from:", url);

    // Simulate network errors
    if (url == "http://timeout.example") {
        console.error("Request timeout");
        console.error("  URL:", url);
        console.warn("Retrying...");
        return null;
    }

    if (url == "http://error.example") {
        console.error("Server error 500");
        console.error("  URL:", url);
        return null;
    }

    console.info("Data fetched successfully");
    return {data: "result"};
}

urls = [
    "http://success.example",
    "http://timeout.example",
    "http://error.example"
];

for (url in urls) {
    data = fetchData(url);
    if (data != null) {
        console.log("Retrieved:", data);
    } else {
        console.log("Failed to retrieve data");
    }
}

// Example 6: Cascading errors
console.log("\nExample 6: Cascading error handling");

function step1() {
    console.info("Step 1: Initializing");
    console.info("Step 1: Complete");
    return true;
}

function step2() {
    console.info("Step 2: Processing");
    console.error("Step 2: Failed - out of memory");
    return false;
}

function step3() {
    console.info("Step 3: Finalizing");
    console.info("Step 3: Complete");
    return true;
}

function runProcess() {
    console.info("=== Starting Process ===");

    if (!step1()) {
        console.error("Process aborted at step 1");
        return false;
    }

    if (!step2()) {
        console.error("Process aborted at step 2");
        console.warn("Rolling back changes");
        return false;
    }

    if (!step3()) {
        console.error("Process aborted at step 3");
        return false;
    }

    console.info("=== Process Complete ===");
    return true;
}

success = runProcess();
if (success) {
    console.log("Process succeeded");
} else {
    console.log("Process failed");
}

// Example 7: Error statistics
console.log("\nExample 7: Error tracking");

errorCount = 0;
warningCount = 0;

function logError(message) {
    nonlocal errorCount;
    console.error(message);
    errorCount = errorCount + 1;
}

function logWarning(message) {
    nonlocal warningCount;
    console.warn(message);
    warningCount = warningCount + 1;
}

logError("Critical error occurred");
logWarning("Low disk space");
logError("Database connection lost");
logWarning("Deprecated API used");
logWarning("Cache miss");

console.log("\n=== Error Summary ===");
console.log("Total errors:", errorCount);
console.log("Total warnings:", warningCount);

if (errorCount > 0) {
    console.error("Application has", errorCount, "errors");
}
if (warningCount > 0) {
    console.warn("Application has", warningCount, "warnings");
}

console.log("\n=== Error Reporting Complete ===");
