// ============================================
// Example: Safe JSON Parsing
// Category: standard-library/json
// Demonstrates: safeParse with depth validation
// ============================================

import console;
import json;

console.log("=== Safe JSON Parsing ===\n");

// ============================================
// SafeParse - Depth-Limited Parsing
// ============================================

console.log("=== SafeParse (depth validation) ===");

// Shallow JSON (depth 1)
shallow = '{"name": "Alice", "age": 30}';
console.log("Shallow JSON: " + shallow);

shallowData = json.safeParse(shallow, 10);
console.log("Parsed successfully with depth limit 10");
console.log("Name: " + shallowData.name);

// Nested JSON (depth 3)
nested = '{"user": {"profile": {"name": "Bob", "age": 25}}}';
console.log("\nNested JSON (depth 3): " + nested);

nestedData = json.safeParse(nested, 10);
console.log("Parsed successfully with depth limit 10");
console.log("Name: " + nestedData.user.profile.name);

// ============================================
// Depth Limit Testing
// ============================================

console.log("\n=== Testing Depth Limits ===");

// Create moderately nested structure
moderate = '{"a": {"b": {"c": {"d": "value"}}}}';
console.log("Moderate nesting (depth 4):");
console.log(moderate);

console.log("\nTrying with depth limit 10:");
moderateData = json.safeParse(moderate, 10);
console.log("Success! Value: " + moderateData.a.b.c.d);

console.log("\nTrying with depth limit 5:");
moderateData2 = json.safeParse(moderate, 5);
console.log("Success with limit 5");

// ============================================
// Safe vs Regular Parse
// ============================================

console.log("\n=== Safe Parse vs Regular Parse ===");

testJson = '{"level1": {"level2": {"level3": {"data": "value"}}}}';
console.log("Test JSON: " + testJson);

// Regular parse - no depth checking
console.log("\nRegular parse:");
regularData = json.parse(testJson);
console.log("  Parsed: " + str(regularData));

// Safe parse with reasonable limit
console.log("\nSafe parse (limit 20):");
safeData = json.safeParse(testJson, 20);
console.log("  Parsed: " + str(safeData));

// ============================================
// Practical Example: API Response Validation
// ============================================

console.log("\n=== Practical: Validate API Responses ===");

// Simulate API response with reasonable nesting
apiResponse = '{"status": "success", "data": {"user": {"id": 123, "profile": {"name": "Charlie", "settings": {"theme": "dark"}}}}}';

console.log("API Response:");
console.log(apiResponse);

console.log("\nValidating with depth limit (prevents attacks):");

// Use safeParse to prevent deeply nested attacks
validatedResponse = json.safeParse(apiResponse, 20);

console.log("Validation passed!");
console.log("  Status: " + validatedResponse.status);
console.log("  User ID: " + str(validatedResponse.data.user.id));
console.log("  User Name: " + validatedResponse.data.user.profile.name);
console.log("  Theme: " + validatedResponse.data.user.profile.settings.theme);

// ============================================
// Practical Example: Configuration Loading
// ============================================

console.log("\n=== Practical: Safe Configuration Loading ===");

configJson = '{"app": {"name": "MyApp", "version": "1.0.0", "settings": {"database": {"host": "localhost", "port": 5432}}}}';

console.log("Loading configuration...");
console.log("Applying depth limit for security");

config = json.safeParse(configJson, 15);

console.log("\nConfiguration loaded:");
console.log("  App Name: " + config.app.name);
console.log("  Version: " + config.app.version);
console.log("  DB Host: " + config.app.settings.database.host);
console.log("  DB Port: " + str(config.app.settings.database.port));

// ============================================
// Practical Example: User Input Validation
// ============================================

console.log("\n=== Practical: Validate User Input ===");

function validateUserInput(jsonString, maxDepth) {
    console.log("\nValidating user input:");
    console.log("  Max depth: " + str(maxDepth));
    console.log("  Input length: " + str(len(jsonString)) + " chars");

    // First, check if valid JSON
    if (!json.validate(jsonString)) {
        console.log("  REJECTED: Invalid JSON syntax");
        return null;
    }

    // Parse with depth limit
    data = json.safeParse(jsonString, maxDepth);
    console.log("  ACCEPTED: Valid JSON within depth limit");

    return data;
}

// Test with valid input
validInput = '{"name": "Diana", "data": {"score": 95}}';
result1 = validateUserInput(validInput, 10);
if (result1 != null) {
    console.log("  Parsed name: " + result1.name);
}

// Test with moderately nested input
moderateInput = '{"a": {"b": {"c": "value"}}}';
result2 = validateUserInput(moderateInput, 10);

// ============================================
// Practical Example: Nested Array Data
// ============================================

console.log("\n=== Practical: Nested Array Structures ===");

nestedArrayJson = '{"items": [{"id": 1, "tags": ["a", "b"]}, {"id": 2, "tags": ["c", "d"]}]}';

console.log("Nested array structure:");
console.log(nestedArrayJson);

arrayData = json.safeParse(nestedArrayJson, 15);

console.log("\nProcessing items:");
i = 0;
while (i < len(arrayData.items)) {
    item = arrayData.items[i];
    console.log("  Item " + str(item.id) + " tags: " + str(item.tags));
    i = i + 1;
}

// ============================================
// Practical Example: Default Depth Limit
// ============================================

console.log("\n=== Practical: Default Depth Protection ===");

// Complex but reasonable structure
complexJson = '{"root": {"branch1": {"leaf": "value1"}, "branch2": {"leaf": "value2"}}}';

console.log("Complex structure:");
console.log(complexJson);

// Use default depth limit (100)
console.log("\nUsing default depth limit:");
complexData = json.safeParse(complexJson, 100);

console.log("Parsed successfully:");
console.log("  Branch1 leaf: " + complexData.root.branch1.leaf);
console.log("  Branch2 leaf: " + complexData.root.branch2.leaf);

// ============================================
// Security Best Practices
// ============================================

console.log("\n=== Security Best Practices ===");

console.log("Recommended depth limits by use case:");
console.log("  - User-generated content: 10-20");
console.log("  - API responses: 20-30");
console.log("  - Configuration files: 15-25");
console.log("  - Internal data: 50-100");

console.log("\nWhy depth limits matter:");
console.log("  - Prevents stack overflow attacks");
console.log("  - Protects against DoS via deeply nested JSON");
console.log("  - Ensures predictable parsing performance");
console.log("  - Validates data structure complexity");

// ============================================
// Practical Example: Error Handling
// ============================================

console.log("\n=== Practical: Robust Error Handling ===");

function safeLoadJson(jsonString, description) {
    console.log("\nLoading: " + description);

    // Validate first
    if (!json.validate(jsonString)) {
        console.log("  ERROR: Invalid JSON format");
        return null;
    }

    // Try safe parse with depth limit
    data = json.safeParse(jsonString, 20);
    console.log("  SUCCESS: Loaded and validated");

    return data;
}

// Test different scenarios
data1 = safeLoadJson('{"valid": true}', "Simple object");
data2 = safeLoadJson('{"user": {"profile": {"name": "Eve"}}}', "Nested user data");
data3 = safeLoadJson('{invalid}', "Malformed JSON");

// ============================================
// Practical Example: Batch Processing
// ============================================

console.log("\n=== Practical: Batch JSON Processing ===");

jsonBatch = [
    '{"id": 1, "status": "active"}',
    '{"id": 2, "status": "pending"}',
    '{"id": 3, "status": "active"}'
];

console.log("Processing batch of " + str(len(jsonBatch)) + " JSON strings:");

processed = 0;
i = 0;
while (i < len(jsonBatch)) {
    jsonStr = jsonBatch[i];

    // Validate and parse safely
    if (json.validate(jsonStr)) {
        data = json.safeParse(jsonStr, 10);
        console.log("  Item " + str(data.id) + ": " + data.status);
        processed = processed + 1;
    } else {
        console.log("  Item " + str(i + 1) + ": INVALID");
    }

    i = i + 1;
}

console.log("\nProcessed: " + str(processed) + "/" + str(len(jsonBatch)));

// ============================================
// Summary
// ============================================

console.log("\n=== Safe Parsing Summary ===");

console.log("Key benefits of safeParse:");
console.log("  1. Prevents deeply nested JSON attacks");
console.log("  2. Validates structure before full parsing");
console.log("  3. Configurable depth limits per use case");
console.log("  4. Same interface as regular parse");
console.log("  5. Essential for untrusted data");

console.log("\nWhen to use safeParse:");
console.log("  - Processing user-submitted JSON");
console.log("  - Parsing external API responses");
console.log("  - Loading configuration from files");
console.log("  - Any untrusted JSON source");

console.log("\n=== Safe JSON Parsing Complete ===");
