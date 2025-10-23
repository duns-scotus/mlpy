// ============================================
// Example: JSON Parsing and Serialization
// Category: standard-library/json
// Demonstrates: parse, stringify, prettyPrint
// ============================================

import console;
import json;

console.log("=== JSON Parsing and Serialization ===\n");

// ============================================
// Parse - JSON String to Object
// ============================================

console.log("=== Parse (string to object) ===");

// Parse object
jsonStr1 = '{"name": "Alice", "age": 30, "city": "NYC"}';
console.log("JSON string: " + jsonStr1);

person = json.parse(jsonStr1);
console.log("Parsed object:");
console.log("  Name: " + person.name);
console.log("  Age: " + str(person.age));
console.log("  City: " + person.city);

// Parse array
jsonStr2 = '[1, 2, 3, 4, 5]';
console.log("\nJSON array: " + jsonStr2);

numbers = json.parse(jsonStr2);
console.log("Parsed array: " + str(numbers));
console.log("First element: " + str(numbers[0]));

// Parse nested structure
jsonStr3 = '{"user": {"name": "Bob", "scores": [85, 92, 78]}, "active": true}';
console.log("\nNested JSON: " + jsonStr3);

data = json.parse(jsonStr3);
console.log("User name: " + data.user.name);
console.log("Scores: " + str(data.user.scores));
console.log("Active: " + str(data.active));

// Parse primitives
console.log("\n=== Parse Primitives ===");

numJson = "42";
parsedNum = json.parse(numJson);
console.log("Number: " + str(parsedNum));

boolJson = "true";
parsedBool = json.parse(boolJson);
console.log("Boolean: " + str(parsedBool));

strJson = '"hello world"';
parsedStr = json.parse(strJson);
console.log("String: " + parsedStr);

// ============================================
// Stringify - Object to JSON String
// ============================================

console.log("\n=== Stringify (object to string) ===");

// Stringify object
user = {
    name: "Charlie",
    age: 25,
    email: "charlie@example.com"
};

userJson = json.stringify(user);
console.log("Object: " + str(user));
console.log("JSON: " + userJson);

// Stringify array
items = ["apple", "banana", "cherry"];
itemsJson = json.stringify(items);
console.log("\nArray: " + str(items));
console.log("JSON: " + itemsJson);

// Stringify nested
config = {
    server: {
        host: "localhost",
        port: 8080
    },
    enabled: true,
    features: ["auth", "cache", "logging"]
};

configJson = json.stringify(config);
console.log("\nNested object JSON:");
console.log(configJson);

// ============================================
// Pretty Print - Formatted JSON
// ============================================

console.log("\n=== Pretty Print (formatted) ===");

settings = {
    theme: "dark",
    fontSize: 14,
    notifications: {
        email: true,
        push: false,
        sms: true
    },
    languages: ["en", "es", "fr"]
};

console.log("Compact JSON:");
console.log(json.stringify(settings));

console.log("\nPretty printed (2 spaces):");
prettyJson2 = json.prettyPrint(settings, 2);
console.log(prettyJson2);

console.log("\nPretty printed (4 spaces):");
prettyJson4 = json.prettyPrint(settings, 4);
console.log(prettyJson4);

// ============================================
// Round-Trip - Parse and Stringify
// ============================================

console.log("\n=== Round-Trip Conversion ===");

original = {
    id: 123,
    title: "Test Document",
    tags: ["test", "example"],
    metadata: {
        created: "2024-01-01",
        author: "System"
    }
};

console.log("Original object: " + str(original));

// Convert to JSON
jsonString = json.stringify(original);
console.log("As JSON: " + jsonString);

// Parse back to object
restored = json.parse(jsonString);
console.log("Restored object: " + str(restored));
console.log("Title matches: " + str(restored.title == original.title));
console.log("ID matches: " + str(restored.id == original.id));

// ============================================
// Practical Example: API Response
// ============================================

console.log("\n=== Practical: API Response Processing ===");

// Simulate API response
apiResponse = '{"status": "success", "data": {"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}], "total": 2}, "timestamp": "2024-01-15T10:30:00Z"}';

console.log("API Response JSON:");
console.log(apiResponse);

// Parse response
response = json.parse(apiResponse);

console.log("\nParsed Response:");
console.log("  Status: " + response.status);
console.log("  Total users: " + str(response.data.total));
console.log("  Timestamp: " + response.timestamp);

console.log("\nUsers:");
i = 0;
while (i < len(response.data.users)) {
    user = response.data.users[i];
    console.log("  - ID: " + str(user.id) + ", Name: " + user.name);
    i = i + 1;
}

// ============================================
// Practical Example: Configuration Files
// ============================================

console.log("\n=== Practical: Configuration Management ===");

// Create configuration
appConfig = {
    app: {
        name: "MyApp",
        version: "1.0.0",
        debug: false
    },
    database: {
        host: "db.example.com",
        port: 5432,
        name: "myapp_db"
    },
    features: {
        authentication: true,
        analytics: true,
        cache: false
    }
};

console.log("Application Configuration:");
configString = json.prettyPrint(appConfig, 2);
console.log(configString);

// Simulate saving and loading
console.log("\nSimulate save/load:");
savedConfig = json.stringify(appConfig);
console.log("Saved as: " + str(len(savedConfig)) + " characters");

loadedConfig = json.parse(savedConfig);
console.log("Loaded app name: " + loadedConfig.app.name);
console.log("Database host: " + loadedConfig.database.host);
console.log("Auth enabled: " + str(loadedConfig.features.authentication));

// ============================================
// Practical Example: Data Export
// ============================================

console.log("\n=== Practical: Data Export ===");

// Generate report data
reportData = {
    report: "Monthly Sales",
    period: "2024-01",
    summary: {
        totalSales: 15000,
        transactions: 145,
        averageValue: 103.45
    },
    topProducts: [
        {name: "Product A", sales: 5000},
        {name: "Product B", sales: 4500},
        {name: "Product C", sales: 3000}
    ]
};

console.log("Exporting report data...");
exportJson = json.prettyPrint(reportData, 2);
console.log(exportJson);

console.log("\nReport Summary:");
console.log("  Total Sales: $" + str(reportData.summary.totalSales));
console.log("  Transactions: " + str(reportData.summary.transactions));
console.log("  Average Value: $" + str(reportData.summary.averageValue));

console.log("\n=== JSON Parsing and Serialization Complete ===");
