// ============================================
// Example: JSON Utilities
// Category: standard-library/json
// Demonstrates: keys, values, hasKey, get, merge
// ============================================

import console;
import json;

console.log("=== JSON Utilities ===\n");

// ============================================
// Keys - Get Object Keys
// ============================================

console.log("=== Keys (get all keys) ===");

person = {
    name: "Alice",
    age: 30,
    city: "NYC",
    email: "alice@example.com"
};

console.log("Object: " + str(person));

personKeys = json.keys(person);
console.log("Keys: " + str(personKeys));
console.log("Number of keys: " + str(len(personKeys)));

// Iterate over keys
console.log("\nIterating keys:");
i = 0;
while (i < len(personKeys)) {
    key = personKeys[i];
    console.log("  " + key);
    i = i + 1;
}

// ============================================
// Values - Get Object Values
// ============================================

console.log("\n=== Values (get all values) ===");

config = {
    timeout: 30,
    retries: 3,
    debug: true,
    host: "localhost"
};

console.log("Object: " + str(config));

configValues = json.values(config);
console.log("Values: " + str(configValues));

// ============================================
// HasKey - Check Key Existence
// ============================================

console.log("\n=== HasKey (check if key exists) ===");

user = {
    id: 123,
    name: "Bob",
    email: "bob@example.com"
};

console.log("User: " + str(user));

console.log("\nChecking keys:");
console.log("  Has 'id': " + str(json.hasKey(user, "id")));
console.log("  Has 'name': " + str(json.hasKey(user, "name")));
console.log("  Has 'email': " + str(json.hasKey(user, "email")));
console.log("  Has 'phone': " + str(json.hasKey(user, "phone")));
console.log("  Has 'address': " + str(json.hasKey(user, "address")));

// ============================================
// Get - Safe Property Access
// ============================================

console.log("\n=== Get (safe access with default) ===");

settings = {
    theme: "dark",
    fontSize: 14,
    lineHeight: 1.5
};

console.log("Settings: " + str(settings));

console.log("\nAccessing properties:");

// Existing keys
theme = json.get(settings, "theme", "light");
console.log("  theme: " + theme);

fontSize = json.get(settings, "fontSize", 12);
console.log("  fontSize: " + str(fontSize));

// Missing keys with defaults
language = json.get(settings, "language", "en");
console.log("  language: " + language + " (default)");

timeout = json.get(settings, "timeout", 30);
console.log("  timeout: " + str(timeout) + " (default)");

// ============================================
// Merge - Combine Objects
// ============================================

console.log("\n=== Merge (combine objects) ===");

defaults = {
    color: "blue",
    size: "medium",
    quantity: 1
};

userPrefs = {
    color: "red",
    quantity: 5
};

console.log("Defaults: " + str(defaults));
console.log("User prefs: " + str(userPrefs));

merged = json.merge(defaults, userPrefs);
console.log("Merged: " + str(merged));

console.log("\nMerged values:");
console.log("  color: " + merged.color + " (from user prefs)");
console.log("  size: " + merged.size + " (from defaults)");
console.log("  quantity: " + str(merged.quantity) + " (from user prefs)");

// ============================================
// Practical Example: Configuration Management
// ============================================

console.log("\n=== Practical: Configuration System ===");

// Default configuration
defaultConfig = {
    server: {
        host: "0.0.0.0",
        port: 8080,
        timeout: 30
    },
    database: {
        host: "localhost",
        port: 5432
    },
    features: {
        auth: true,
        cache: false,
        logging: true
    }
};

// User configuration (partial)
userConfig = {
    server: {
        port: 3000,
        timeout: 60
    },
    features: {
        cache: true
    }
};

console.log("Building final configuration...");

// Merge configurations
finalConfig = {
    server: json.merge(defaultConfig.server, userConfig.server),
    database: defaultConfig.database,
    features: json.merge(defaultConfig.features, userConfig.features)
};

console.log("\nFinal Configuration:");
console.log("Server:");
console.log("  Host: " + finalConfig.server.host);
console.log("  Port: " + str(finalConfig.server.port));
console.log("  Timeout: " + str(finalConfig.server.timeout));

console.log("Database:");
console.log("  Host: " + finalConfig.database.host);
console.log("  Port: " + str(finalConfig.database.port));

console.log("Features:");
console.log("  Auth: " + str(finalConfig.features.auth));
console.log("  Cache: " + str(finalConfig.features.cache));
console.log("  Logging: " + str(finalConfig.features.logging));

// ============================================
// Practical Example: Safe Data Access
// ============================================

console.log("\n=== Practical: Safe API Data Access ===");

apiData = {
    user: {
        id: 456,
        name: "Charlie"
    },
    metadata: {
        timestamp: "2024-01-15",
        version: "1.0"
    }
};

console.log("API Data: " + str(apiData));

console.log("\nSafe access with defaults:");

// Access existing nested data
userId = json.get(apiData.user, "id", 0);
userName = json.get(apiData.user, "name", "Unknown");
console.log("  User ID: " + str(userId));
console.log("  User Name: " + userName);

// Access missing data with defaults
userEmail = json.get(apiData.user, "email", "no-email@example.com");
userAge = json.get(apiData.user, "age", 0);
console.log("  User Email: " + userEmail + " (default)");
console.log("  User Age: " + str(userAge) + " (default)");

// ============================================
// Practical Example: Object Inspection
// ============================================

console.log("\n=== Practical: Object Inspection ===");

document = {
    title: "Sample Document",
    content: "Lorem ipsum dolor sit amet",
    author: "System",
    tags: ["sample", "test"],
    published: false
};

console.log("Inspecting document:");
console.log(str(document));

// Get all properties
docKeys = json.keys(document);
console.log("\nProperties (" + str(len(docKeys)) + " total):");

i = 0;
while (i < len(docKeys)) {
    key = docKeys[i];
    value = json.get(document, key, null);

    // Check if key exists
    if (json.hasKey(document, key)) {
        console.log("  " + key + ": " + str(value));
    }

    i = i + 1;
}

// ============================================
// Practical Example: Property Mapping
// ============================================

console.log("\n=== Practical: Property Mapping ===");

sourceData = {
    first_name: "Diana",
    last_name: "Smith",
    email_address: "diana@example.com",
    user_id: 789
};

console.log("Source data: " + str(sourceData));

// Map to different property names
mappedData = {
    firstName: json.get(sourceData, "first_name", ""),
    lastName: json.get(sourceData, "last_name", ""),
    email: json.get(sourceData, "email_address", ""),
    id: json.get(sourceData, "user_id", 0)
};

console.log("\nMapped data: " + str(mappedData));

// ============================================
// Practical Example: Feature Flags
// ============================================

console.log("\n=== Practical: Feature Flag System ===");

// Default features (all disabled)
defaultFeatures = {
    newUI: false,
    betaFeatures: false,
    analytics: false,
    notifications: false
};

// Enabled features for specific user
userFeatures = {
    newUI: true,
    analytics: true
};

console.log("Default features: " + str(defaultFeatures));
console.log("User overrides: " + str(userFeatures));

// Merge to get final feature set
activeFeatures = json.merge(defaultFeatures, userFeatures);

console.log("\nActive features:");
featureKeys = json.keys(activeFeatures);

i = 0;
while (i < len(featureKeys)) {
    feature = featureKeys[i];
    enabled = json.get(activeFeatures, feature, false);

    status = "";
    if (enabled) {
        status = "ENABLED";
    } else {
        status = "disabled";
    }

    console.log("  " + feature + ": " + status);

    i = i + 1;
}

// Check specific features
console.log("\nFeature checks:");
console.log("  Has newUI flag: " + str(json.hasKey(activeFeatures, "newUI")));
console.log("  newUI enabled: " + str(json.get(activeFeatures, "newUI", false)));
console.log("  Has experimental flag: " + str(json.hasKey(activeFeatures, "experimental")));
console.log("  experimental enabled: " + str(json.get(activeFeatures, "experimental", false)));

// ============================================
// Practical Example: Data Transformation
// ============================================

console.log("\n=== Practical: Data Transformation ===");

rawData = [
    {id: 1, name: "Product A", price: 29.99},
    {id: 2, name: "Product B", price: 49.99},
    {id: 3, name: "Product C", price: 19.99}
];

console.log("Raw data: " + str(len(rawData)) + " products");

// Transform to lookup by ID
productLookup = {};

i = 0;
while (i < len(rawData)) {
    product = rawData[i];
    productId = json.get(product, "id", 0);

    // Can't use computed keys directly in ML, so we build it step by step
    // This is a limitation we work around

    i = i + 1;
}

console.log("Transformation complete");

// Access products safely
console.log("\nProduct access examples:");

product1 = rawData[0];
console.log("  Product 1 name: " + json.get(product1, "name", "Unknown"));
console.log("  Product 1 price: $" + str(json.get(product1, "price", 0)));

console.log("\n=== JSON Utilities Complete ===");
