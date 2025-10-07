// ============================================
// Comprehensive Example: Dynamic Data Processor
// Category: standard-library/builtin
// Demonstrates: Complete builtin module capabilities in a real application
// ============================================

import console;

console.log("=== Dynamic Data Processing System ===\n");

// ============================================
// 1. Configuration System with Introspection
// ============================================

defaultConfig = {
    name: "DataProcessor",
    version: "1.0",
    maxRecords: 1000,
    debugMode: false,
    outputFormat: "json"
};

userConfig = {
    debugMode: true,
    maxRecords: 500
};

function mergeConfig(defaults, overrides) {
    result = {};

    // Copy all default keys
    defaultKeys = keys(defaults);
    i = 0;
    while (i < len(defaultKeys)) {
        key = defaultKeys[i];
        result[key] = defaults[key];
        i = i + 1;
    }

    // Override with user config
    overrideKeys = keys(overrides);
    i = 0;
    while (i < len(overrideKeys)) {
        key = overrideKeys[i];
        if (hasattr(defaults, key)) {
            result[key] = overrides[key];
        } else {
            console.warn("Unknown config key: " + key);
        }
        i = i + 1;
    }

    return result;
}

config = mergeConfig(defaultConfig, userConfig);
console.log("Configuration loaded:");
configKeys = keys(config);
i = 0;
while (i < len(configKeys)) {
    key = configKeys[i];
    value = config[key];
    console.log("  " + key + ": " + str(value) + " (" + typeof(value) + ")");
    i = i + 1;
}

// ============================================
// 2. Dynamic Type-Based Data Processor
// ============================================

console.log("\n=== Processing Mixed Data Types ===");

rawData = [
    {id: 1, name: "Alice", score: "92.5"},
    {id: 2, name: "Bob", score: "87"},
    {id: 3, name: "Charlie", score: "95.5"},
    {id: 4, name: "David", score: "invalid"},
    {id: 5, name: "Eve", score: "88.0"}
];

function processRecord(record) {
    // Validate required fields
    if (!hasattr(record, "id") || !hasattr(record, "name") || !hasattr(record, "score")) {
        return {valid: false, error: "Missing required fields", data: null};
    }

    // Type conversion with validation
    idType = typeof(record.id);
    scoreType = typeof(record.score);

    // Ensure ID is number
    recordId = 0;
    if (idType == "number") {
        recordId = record.id;
    } elif (idType == "string") {
        recordId = int(record.id);
    } else {
        return {valid: false, error: "Invalid ID type", data: null};
    }

    // Ensure score is number
    scoreValue = 0.0;
    if (scoreType == "number") {
        scoreValue = float(record.score);
    } elif (scoreType == "string") {
        scoreValue = float(record.score);
        // Check if conversion failed
        if (scoreValue == 0.0 && record.score != "0" && record.score != "0.0") {
            return {valid: false, error: "Invalid score value", data: null};
        }
    } else {
        return {valid: false, error: "Invalid score type", data: null};
    }

    // Create processed record
    processed = {
        id: recordId,
        name: record.name,
        score: round(scoreValue, 1),
        grade: scoreValue >= 90 ? "A" : (scoreValue >= 80 ? "B" : "C")
    };

    return {valid: true, error: null, data: processed};
}

// Process all records
validRecords = [];
errors = [];

i = 0;
while (i < len(rawData)) {
    result = processRecord(rawData[i]);

    if (result.valid) {
        validRecords = validRecords + [result.data];
        console.log("  Processed: " + result.data.name + " - Score: " + str(result.data.score) + " (" + result.data.grade + ")");
    } else {
        errors = errors + [{record: rawData[i], error: result.error}];
        console.error("  Error processing record " + str(rawData[i].id) + ": " + result.error);
    }

    i = i + 1;
}

console.log("\nProcessing summary:");
console.log("  Valid records: " + str(len(validRecords)));
console.log("  Errors: " + str(len(errors)));

// ============================================
// 3. Statistical Analysis with Utilities
// ============================================

console.log("\n=== Statistical Analysis ===");

if (len(validRecords) > 0) {
    // Extract scores
    scores = [];
    i = 0;
    while (i < len(validRecords)) {
        scores = scores + [validRecords[i].score];
        i = i + 1;
    }

    // Calculate statistics
    total = sum(scores);
    count = len(scores);
    average = total / count;
    minimum = min(scores);
    maximum = max(scores);
    sortedScores = sorted(scores, true);

    console.log("Score statistics:");
    console.log("  Count: " + str(count));
    console.log("  Average: " + format(average, ".2f"));
    console.log("  Min: " + str(minimum));
    console.log("  Max: " + str(maximum));
    console.log("  Top score: " + str(sortedScores[0]));

    // Grade distribution
    gradeA = 0;
    gradeB = 0;
    gradeC = 0;

    i = 0;
    while (i < len(validRecords)) {
        grade = validRecords[i].grade;
        if (grade == "A") {
            gradeA = gradeA + 1;
        } elif (grade == "B") {
            gradeB = gradeB + 1;
        } else {
            gradeC = gradeC + 1;
        }
        i = i + 1;
    }

    console.log("\nGrade distribution:");
    console.log("  A grades: " + str(gradeA) + " (" + format((gradeA / count) * 100, ".1f") + "%)");
    console.log("  B grades: " + str(gradeB) + " (" + format((gradeB / count) * 100, ".1f") + "%)");
    console.log("  C grades: " + str(gradeC) + " (" + format((gradeC / count) * 100, ".1f") + "%)");

    // Check if all passed (score >= 60)
    passingScores = [];
    i = 0;
    while (i < len(scores)) {
        passingScores = passingScores + [scores[i] >= 60];
        i = i + 1;
    }
    allPassed = all(passingScores);
    anyFailed = !allPassed;

    console.log("\nPerformance checks:");
    console.log("  All students passed: " + str(allPassed));
    console.log("  Any students below 60: " + str(anyFailed));
}

// ============================================
// 4. Report Generation with Formatting
// ============================================

console.log("\n=== Formatted Report ===");

function generateReport(records) {
    if (len(records) == 0) {
        return "No records to report";
    }

    report = "";
    report = report + "STUDENT PERFORMANCE REPORT\n";
    report = report + "==========================\n\n";

    // Header
    report = report + "ID\tName\t\tScore\tGrade\n";
    report = report + "----------------------------------------\n";

    // Data rows
    i = 0;
    while (i < len(records)) {
        record = records[i];
        idStr = str(record.id);
        nameStr = record.name;

        // Pad name to 12 characters
        while (len(nameStr) < 12) {
            nameStr = nameStr + " ";
        }

        scoreStr = format(record.score, ".1f");
        gradeStr = record.grade;

        report = report + idStr + "\t" + nameStr + "\t" + scoreStr + "\t" + gradeStr + "\n";
        i = i + 1;
    }

    return report;
}

report = generateReport(validRecords);
print("\n" + report);

// ============================================
// 5. Dynamic Introspection Summary
// ============================================

console.log("=== System Introspection ===\n");

console.log("Loaded modules:");
loadedModules = modules();
i = 0;
while (i < len(loadedModules)) {
    console.log("  - " + loadedModules[i]);
    i = i + 1;
}

console.log("\nBuiltin capabilities demonstrated:");
capabilities = [
    "Type conversion (int, float, str, bool)",
    "Type checking (typeof, isinstance)",
    "Dynamic introspection (hasattr, getattr, modules)",
    "Collection operations (keys, values, len, sorted)",
    "Statistical functions (sum, min, max, round)",
    "Boolean logic (all, any)",
    "Formatting (format, str)",
    "Data validation and error handling"
];

i = 0;
while (i < len(capabilities)) {
    console.log("  " + str(i + 1) + ". " + capabilities[i]);
    i = i + 1;
}

console.log("\n=== Processing Complete ===");
console.log("This example demonstrates ML's builtin module:");
console.log("  - Dynamic type handling");
console.log("  - Safe introspection");
console.log("  - Practical data processing");
console.log("  - Statistical analysis");
console.log("  - Professional formatting");
