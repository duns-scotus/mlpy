// ============================================
// Example: Comprehensive Console Logging
// Category: standard-library/console
// Demonstrates: All console features in a practical application
// ============================================

import console;

console.info("=== Data Processing Application ===\n");

// Global configuration
config = {
    debug: true,
    maxRetries: 3,
    batchSize: 10
};

// Statistics tracking
stats = {
    processed: 0,
    failed: 0,
    warnings: 0,
    errors: 0
};

// Initialization
console.info("=== Initialization ===");
console.info("Loading configuration...");
console.debug("Config:", config);
console.info("Configuration loaded");

console.info("Initializing data processor...");
console.debug("Batch size:", config.batchSize);
console.debug("Max retries:", config.maxRetries);
console.info("Data processor ready");

// Data validation function
function validateRecord(record) {
    if (config.debug) {
        console.debug("Validating record:", record);
    }

    errors = [];

    if (!record.id || record.id <= 0) {
        errors = errors + ["Invalid ID"];
    }

    if (!record.value || typeof(record.value) != "number") {
        errors = errors + ["Invalid value"];
    } elif (record.value < 0) {
        console.warn("Negative value in record", record.id);
        stats.warnings = stats.warnings + 1;
    }

    if (len(errors) > 0) {
        console.error("Validation failed for record", record.id);
        for (error in errors) {
            console.error("  -", error);
        }
        stats.errors = stats.errors + 1;
        return false;
    }

    if (config.debug) {
        console.debug("Record", record.id, "validated successfully");
    }

    return true;
}

// Data processing function
function processRecord(record) {
    console.info("Processing record", record.id);

    if (!validateRecord(record)) {
        console.error("Skipping invalid record", record.id);
        stats.failed = stats.failed + 1;
        return false;
    }

    try {
        // Simulate processing
        if (config.debug) {
            console.debug("Applying transformation to record", record.id);
        }

        result = record.value * 2;

        if (config.debug) {
            console.debug("Original value:", record.value);
            console.debug("Processed value:", result);
        }

        console.info("Record", record.id, "processed successfully");
        stats.processed = stats.processed + 1;
        return true;

    } except (err) {
        console.error("Exception processing record", record.id);
        console.error("Error: Processing failed");
        stats.errors = stats.errors + 1;
        stats.failed = stats.failed + 1;
        return false;
    }
}

// Batch processing function
function processBatch(records) {
    batchSize = len(records);
    console.info("=== Processing Batch ===");
    console.info("Batch size:", batchSize);

    if (config.debug) {
        console.debug("Records in batch:", batchSize);
    }

    successCount = 0;
    failCount = 0;

    for (record in records) {
        if (processRecord(record)) {
            successCount = successCount + 1;
        } else {
            failCount = failCount + 1;
        }

        // Progress indicator
        if ((successCount + failCount) % 5 == 0) {
            progress = (successCount + failCount) * 100 / batchSize;
            console.info("Progress:", progress, "%");
        }
    }

    console.log("\n=== Batch Summary ===");
    console.info("Successful:", successCount);

    if (failCount > 0) {
        console.warn("Failed:", failCount);
    }

    if (failCount > batchSize / 2) {
        console.error("Batch failure rate exceeds 50%");
    }

    return successCount;
}

// Sample data with various conditions
records = [
    {id: 1, value: 10},
    {id: 2, value: 20},
    {id: 3, value: -5},    // Warning: negative
    {id: 0, value: 30},    // Error: invalid ID
    {id: 5, value: 40},
    {id: 6, value: 50},
    {id: 7, value: null},  // Error: invalid value
    {id: 8, value: 60},
    {id: 9, value: 70},
    {id: 10, value: 80}
];

// Process all records
console.log("\n=== Main Processing ===");
successfulRecords = processBatch(records);

// Final statistics
console.log("\n=== Application Statistics ===");
console.info("Total records:", len(records));
console.info("Successfully processed:", stats.processed);

if (stats.failed > 0) {
    console.warn("Failed to process:", stats.failed);
}

if (stats.warnings > 0) {
    console.warn("Total warnings:", stats.warnings);
}

if (stats.errors > 0) {
    console.error("Total errors:", stats.errors);
}

// Success rate calculation
successRate = (stats.processed * 100) / len(records);
console.info("Success rate:", str(round(successRate, 1)) + "%");

if (successRate < 50) {
    console.error("Success rate below acceptable threshold");
} elif (successRate < 80) {
    console.warn("Success rate could be improved");
} else {
    console.info("Success rate acceptable");
}

// Shutdown sequence
console.log("\n=== Shutdown ===");
console.info("Saving statistics...");

if (config.debug) {
    console.debug("Stats:", stats);
}

console.info("Statistics saved");
console.info("Cleanup complete");
console.info("=== Application Terminated ===");
