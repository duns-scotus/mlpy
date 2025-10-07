// ============================================
// Example: JSON Validation and Type Checking
// Category: standard-library/json
// Demonstrates: validate, isObject, isArray, isString, isNumber, isBoolean, isNull
// ============================================

import console;
import json;

console.log("=== JSON Validation and Type Checking ===\n");

// ============================================
// Validate - Check JSON Syntax
// ============================================

console.log("=== Validate JSON Strings ===");

// Valid JSON
valid1 = '{"name": "Alice", "age": 30}';
console.log("String: " + valid1);
console.log("Valid: " + str(json.validate(valid1)));

valid2 = '[1, 2, 3, 4, 5]';
console.log("\nString: " + valid2);
console.log("Valid: " + str(json.validate(valid2)));

valid3 = '"hello world"';
console.log("\nString: " + valid3);
console.log("Valid: " + str(json.validate(valid3)));

valid4 = 'true';
console.log("\nString: " + valid4);
console.log("Valid: " + str(json.validate(valid4)));

// Invalid JSON
console.log("\n=== Invalid JSON ===");

invalid1 = '{name: "Alice"}';  // Missing quotes on key
console.log("String: " + invalid1);
console.log("Valid: " + str(json.validate(invalid1)));

invalid2 = '{"name": "Alice",}';  // Trailing comma
console.log("\nString: " + invalid2);
console.log("Valid: " + str(json.validate(invalid2)));

invalid3 = "{incomplete";
console.log("\nString: " + invalid3);
console.log("Valid: " + str(json.validate(invalid3)));

// ============================================
// Type Checking - isObject
// ============================================

console.log("\n=== isObject (check for objects) ===");

obj = {name: "Alice", age: 30};
arr = [1, 2, 3];
strVal = "hello";
num = 42;

console.log("Object {name: 'Alice', age: 30}:");
console.log("  isObject: " + str(json.isObject(obj)));

console.log("Array [1, 2, 3]:");
console.log("  isObject: " + str(json.isObject(arr)));

console.log("String 'hello':");
console.log("  isObject: " + str(json.isObject(strVal)));

// ============================================
// Type Checking - isArray
// ============================================

console.log("\n=== isArray (check for arrays) ===");

console.log("Array [1, 2, 3]:");
console.log("  isArray: " + str(json.isArray(arr)));

console.log("Object {name: 'Alice'}:");
console.log("  isArray: " + str(json.isArray(obj)));

console.log("String 'hello':");
console.log("  isArray: " + str(json.isArray(strVal)));

// ============================================
// Type Checking - isString
// ============================================

console.log("\n=== isString (check for strings) ===");

console.log("String 'hello':");
console.log("  isString: " + str(json.isString(strVal)));

console.log("Number 42:");
console.log("  isString: " + str(json.isString(num)));

console.log("Object:");
console.log("  isString: " + str(json.isString(obj)));

// ============================================
// Type Checking - isNumber
// ============================================

console.log("\n=== isNumber (check for numbers) ===");

integer = 42;
floatNum = 3.14;
boolVal = true;
strVal = "123";

console.log("Integer 42:");
console.log("  isNumber: " + str(json.isNumber(integer)));

console.log("Float 3.14:");
console.log("  isNumber: " + str(json.isNumber(floatNum)));

console.log("Boolean true:");
console.log("  isNumber: " + str(json.isNumber(boolVal)));

console.log("String '123':");
console.log("  isNumber: " + str(json.isNumber(strVal)));

// ============================================
// Type Checking - isBoolean
// ============================================

console.log("\n=== isBoolean (check for booleans) ===");

console.log("Boolean true:");
console.log("  isBoolean: " + str(json.isBoolean(true)));

console.log("Boolean false:");
console.log("  isBoolean: " + str(json.isBoolean(false)));

console.log("Number 1:");
console.log("  isBoolean: " + str(json.isBoolean(1)));

console.log("Number 0:");
console.log("  isBoolean: " + str(json.isBoolean(0)));

// ============================================
// Type Checking - isNull
// ============================================

console.log("\n=== isNull (check for null) ===");

nullVal = null;
zeroVal = 0;
emptyStr = "";
falseBool = false;

console.log("null:");
console.log("  isNull: " + str(json.isNull(nullVal)));

console.log("0:");
console.log("  isNull: " + str(json.isNull(zeroVal)));

console.log("Empty string:");
console.log("  isNull: " + str(json.isNull(emptyStr)));

console.log("false:");
console.log("  isNull: " + str(json.isNull(falseBool)));

// ============================================
// Practical Example: Safe Data Processing
// ============================================

console.log("\n=== Practical: Safe Data Processing ===");

function processUserData(jsonString) {
    console.log("\nProcessing: " + jsonString);

    // Validate before parsing
    if (!json.validate(jsonString)) {
        console.log("  ERROR: Invalid JSON");
        return null;
    }

    // Parse data
    data = json.parse(jsonString);

    // Type check and process
    if (json.isObject(data)) {
        console.log("  Type: Object");

        // Check for expected fields
        if (json.isString(data.name)) {
            console.log("  Name: " + data.name);
        } else {
            console.log("  Name: Invalid or missing");
        }

        if (json.isNumber(data.age)) {
            console.log("  Age: " + str(data.age));
        } else {
            console.log("  Age: Invalid or missing");
        }
    } elif (json.isArray(data)) {
        console.log("  Type: Array");
        console.log("  Length: " + str(len(data)));
    } else {
        console.log("  Type: Primitive value");
        console.log("  Value: " + str(data));
    }

    return data;
}

// Test with valid data
processUserData('{"name": "Alice", "age": 30}');
processUserData('[1, 2, 3, 4, 5]');
processUserData('"hello"');

// Test with invalid data
processUserData('{invalid json}');

// Test with missing fields
processUserData('{"name": "Bob"}');

// ============================================
// Practical Example: Type-Safe API Response
// ============================================

console.log("\n=== Practical: Type-Safe API Handling ===");

apiResponseJson = '{"status": "success", "data": {"count": 42, "items": ["a", "b", "c"]}, "error": null}';

console.log("API Response:");
console.log(apiResponseJson);

// Parse and validate
if (json.validate(apiResponseJson)) {
    response = json.parse(apiResponseJson);

    console.log("\nResponse Analysis:");

    // Check status
    if (json.isString(response.status)) {
        console.log("  Status: " + response.status);
    }

    // Check data
    if (json.isObject(response.data)) {
        console.log("  Data is object: Yes");

        if (json.isNumber(response.data.count)) {
            console.log("    Count: " + str(response.data.count));
        }

        if (json.isArray(response.data.items)) {
            console.log("    Items is array: Yes");
            console.log("    Items length: " + str(len(response.data.items)));
        }
    }

    // Check error
    if (json.isNull(response.error)) {
        console.log("  Error: null (no error)");
    } elif (json.isString(response.error)) {
        console.log("  Error message: " + response.error);
    }
}

// ============================================
// Practical Example: Dynamic Type Routing
// ============================================

console.log("\n=== Practical: Dynamic Type Routing ===");

function routeByType(value) {
    if (json.isObject(value)) {
        console.log("  Routing to object handler");
        console.log("  Keys: " + str(json.keys(value)));
    } elif (json.isArray(value)) {
        console.log("  Routing to array handler");
        console.log("  Length: " + str(len(value)));
    } elif (json.isString(value)) {
        console.log("  Routing to string handler");
        console.log("  Value: " + value);
    } elif (json.isNumber(value)) {
        console.log("  Routing to number handler");
        console.log("  Value: " + str(value));
    } elif (json.isBoolean(value)) {
        console.log("  Routing to boolean handler");
        console.log("  Value: " + str(value));
    } elif (json.isNull(value)) {
        console.log("  Routing to null handler");
    } else {
        console.log("  Unknown type");
    }
}

console.log("\nRouting different types:");

console.log("Type: object");
routeByType({x: 1, y: 2});

console.log("\nType: array");
routeByType([1, 2, 3]);

console.log("\nType: string");
routeByType("hello");

console.log("\nType: number");
routeByType(42);

console.log("\nType: boolean");
routeByType(true);

console.log("\nType: null");
routeByType(null);

// ============================================
// Practical Example: Data Validation
// ============================================

console.log("\n=== Practical: Schema Validation ===");

function validateUser(user) {
    console.log("\nValidating user: " + str(user));

    errors = [];

    // Must be object
    if (!json.isObject(user)) {
        errors = errors + ["User must be an object"];
        console.log("  Errors: " + str(errors));
        return false;
    }

    // Name must be string
    if (!json.isString(user.name)) {
        errors = errors + ["name must be a string"];
    }

    // Age must be number
    if (!json.isNumber(user.age)) {
        errors = errors + ["age must be a number"];
    }

    // Active must be boolean
    if (!json.isBoolean(user.active)) {
        errors = errors + ["active must be a boolean"];
    }

    if (len(errors) > 0) {
        console.log("  Validation failed:");
        i = 0;
        while (i < len(errors)) {
            console.log("    - " + errors[i]);
            i = i + 1;
        }
        return false;
    }

    console.log("  Validation passed!");
    return true;
}

// Test validation
validUser = {name: "Alice", age: 30, active: true};
validateUser(validUser);

invalidUser1 = {name: 123, age: 30, active: true};
validateUser(invalidUser1);

invalidUser2 = {name: "Bob", age: "thirty", active: true};
validateUser(invalidUser2);

console.log("\n=== JSON Validation and Type Checking Complete ===");
