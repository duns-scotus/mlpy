// ============================================
// Example: Introspection and Discovery
// Category: standard-library/builtin
// Demonstrates: help(), methods(), modules(), hasattr(), getattr(), callable()
// ============================================

import console;
import math;
import regex;

console.log("=== Introspection: Discovering the Language ===\n");

// modules() - See what's imported
console.log("Loaded modules:");
loadedModules = modules();
i = 0;
while (i < len(loadedModules)) {
    console.log("  - " + loadedModules[i]);
    i = i + 1;
}

// methods() - Explore what a value can do
console.log("\n=== Discovering Methods ===");

text = "hello";
console.log("String methods:");
stringMethods = methods(text);
console.log("  Available: " + str(len(stringMethods)) + " methods");
console.log("  Examples: upper, lower, split, replace, startswith");

numbers = [1, 2, 3];
console.log("\nArray methods:");
arrayMethods = methods(numbers);
console.log("  Available: " + str(len(arrayMethods)) + " methods");

// callable() - Check if something can be called
console.log("\n=== Checking Callability ===");

function greet() {
    return "Hello!";
}

console.log("Is greet() callable? " + str(callable(greet)));        // true
console.log("Is 42 callable? " + str(callable(42)));                // false
console.log("Is 'hello' callable? " + str(callable("hello")));      // false
console.log("Is print callable? " + str(callable(print)));          // true

// hasattr() - Safe attribute checking
console.log("\n=== Safe Attribute Checking ===");

person = {name: "Alice", age: 30, city: "NYC"};

console.log("Does object have 'name'? " + str(hasattr(person, "name")));     // true
console.log("Does object have 'email'? " + str(hasattr(person, "email")));   // false

// getattr() - Safe attribute access
console.log("\n=== Safe Attribute Access ===");

// Access existing attribute
name = getattr(person, "name", "Unknown");
console.log("Name: " + name);  // "Alice"

// Access missing attribute with default
email = getattr(person, "email", "no-email@example.com");
console.log("Email: " + email);  // default value

country = getattr(person, "country", "USA");
console.log("Country: " + country);  // default value

// Dynamic method discovery and invocation
console.log("\n=== Dynamic Programming ===");

function exploreObject(obj, objName) {
    console.log("\nExploring: " + objName);
    console.log("Type: " + typeof(obj));

    if (typeof(obj) == "object") {
        objKeys = keys(obj);
        console.log("Properties (" + str(len(objKeys)) + "):");
        i = 0;
        while (i < len(objKeys)) {
            key = objKeys[i];
            value = obj[key];
            console.log("  " + key + ": " + str(value) + " (" + typeof(value) + ")");
            i = i + 1;
        }
    } elif (typeof(obj) == "array") {
        console.log("Array length: " + str(len(obj)));
        console.log("First element: " + str(obj[0]));
        console.log("Last element: " + str(obj[len(obj) - 1]));
    } elif (typeof(obj) == "string") {
        console.log("String length: " + str(len(obj)));
        console.log("Content: \"" + obj + "\"");
    } elif (typeof(obj) == "number") {
        console.log("Value: " + str(obj));
        console.log("Is positive: " + str(obj > 0));
    } elif (typeof(obj) == "function") {
        console.log("This is a callable function");
        console.log("Callable: " + str(callable(obj)));
    }
}

exploreObject(person, "person");
exploreObject([10, 20, 30], "numbers");
exploreObject("Dynamic ML!", "message");
exploreObject(42, "number");
exploreObject(greet, "greet function");

// Using introspection for validation
console.log("\n=== Validation with Introspection ===");

function validatePerson(p) {
    errors = [];

    if (!hasattr(p, "name")) {
        errors = errors + ["Missing required field: name"];
    }

    if (!hasattr(p, "age")) {
        errors = errors + ["Missing required field: age"];
    } elif (!isinstance(p.age, "number")) {
        errors = errors + ["Field 'age' must be a number"];
    }

    if (len(errors) > 0) {
        return {valid: false, errors: errors};
    }

    return {valid: true, errors: []};
}

validPerson = {name: "Bob", age: 25};
invalidPerson = {name: "Charlie"};

result1 = validatePerson(validPerson);
console.log("Valid person: " + str(result1.valid));

result2 = validatePerson(invalidPerson);
console.log("Invalid person: " + str(result2.valid));
if (len(result2.errors) > 0) {
    console.log("Errors:");
    i = 0;
    while (i < len(result2.errors)) {
        console.log("  - " + result2.errors[i]);
        i = i + 1;
    }
}

// Discovery-based object merging
console.log("\n=== Dynamic Object Merging ===");

defaults = {theme: "light", language: "en", pageSize: 10};
userPrefs = {theme: "dark", pageSize: 20};

function mergeObjects(base, overrides) {
    result = {};

    // Copy base properties
    baseKeys = keys(base);
    i = 0;
    while (i < len(baseKeys)) {
        key = baseKeys[i];
        result[key] = base[key];
        i = i + 1;
    }

    // Override with user preferences
    overrideKeys = keys(overrides);
    i = 0;
    while (i < len(overrideKeys)) {
        key = overrideKeys[i];
        result[key] = overrides[key];
        i = i + 1;
    }

    return result;
}

finalConfig = mergeObjects(defaults, userPrefs);
console.log("Final configuration:");
configKeys = keys(finalConfig);
i = 0;
while (i < len(configKeys)) {
    key = configKeys[i];
    console.log("  " + key + ": " + str(finalConfig[key]));
    i = i + 1;
}

console.log("\n=== Introspection Complete ===");
