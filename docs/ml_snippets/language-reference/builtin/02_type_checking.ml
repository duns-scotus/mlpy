// ============================================
// Example: Type Checking Functions
// Category: language-reference/builtin
// Demonstrates: typeof(), isinstance()
// ============================================

import console;

console.log("=== Type Checking Functions ===\n");

// Example 1: typeof() - Basic type checking
console.log("Example 1: typeof() - Get type of value");
console.log("typeof(true) = \"" + typeof(true) + "\"");
console.log("typeof(42) = \"" + typeof(42) + "\"");
console.log("typeof(3.14) = \"" + typeof(3.14) + "\"");
console.log("typeof(\"hello\") = \"" + typeof("hello") + "\"");
console.log("typeof([1, 2, 3]) = \"" + typeof([1, 2, 3]) + "\"");
console.log("typeof({a: 1, b: 2}) = \"" + typeof({a: 1, b: 2}) + "\"");

// Example 2: typeof() with functions
console.log("\nExample 2: typeof() with functions");
function namedFunc() {
    return 42;
}
arrowFunc = fn(x) => x * 2;

console.log("typeof(namedFunc) = \"" + typeof(namedFunc) + "\"");
console.log("typeof(arrowFunc) = \"" + typeof(arrowFunc) + "\"");

// Example 3: isinstance() - Type validation
console.log("\nExample 3: isinstance() - Check specific type");
value = 42;
console.log("value = " + str(value));
console.log("isinstance(value, \"number\") = " + str(isinstance(value, "number")));
console.log("isinstance(value, \"string\") = " + str(isinstance(value, "string")));
console.log("isinstance(value, \"boolean\") = " + str(isinstance(value, "boolean")));

// Example 4: Type-based conditional logic
console.log("\nExample 4: Type-based conditional logic");
function processValue(val) {
    if (typeof(val) == "number") {
        return val * 2;
    } elif (typeof(val) == "string") {
        return val + val;
    } elif (typeof(val) == "array") {
        return len(val);
    } else {
        return null;
    }
}

console.log("processValue(21) = " + str(processValue(21)));          // 42
console.log("processValue(\"Hi\") = " + str(processValue("Hi")));    // "HiHi"
console.log("processValue([1,2,3]) = " + str(processValue([1,2,3])));  // 3
console.log("processValue(true) = " + str(processValue(true)));      // null

// Example 5: Type validation for function parameters
console.log("\nExample 5: Type validation in functions");
function addNumbers(a, b) {
    // Validate both parameters are numbers
    if (!isinstance(a, "number")) {
        throw {message: "First parameter must be a number"};
    }
    if (!isinstance(b, "number")) {
        throw {message: "Second parameter must be a number"};
    }
    return a + b;
}

try {
    result = addNumbers(10, 20);
    console.log("addNumbers(10, 20) = " + str(result));
} except (err) {
    console.log("Error: Invalid parameters");
}

try {
    result = addNumbers(10, "20");
    console.log("addNumbers(10, \"20\") = " + str(result));
} except (err) {
    console.log("Error caught: Second parameter must be a number");
}

// Example 6: Type-safe data processor
console.log("\nExample 6: Type-safe data processor");
function processData(data) {
    results = {
        numbers: 0,
        strings: 0,
        arrays: 0,
        objects: 0,
        booleans: 0,
        others: 0
    };

    for (item in data) {
        itemType = typeof(item);

        if (itemType == "number") {
            results.numbers = results.numbers + 1;
        } elif (itemType == "string") {
            results.strings = results.strings + 1;
        } elif (itemType == "array") {
            results.arrays = results.arrays + 1;
        } elif (itemType == "object") {
            results.objects = results.objects + 1;
        } elif (itemType == "boolean") {
            results.booleans = results.booleans + 1;
        } else {
            results.others = results.others + 1;
        }
    }

    return results;
}

mixedData = [42, "hello", [1, 2], true, {a: 1}, 3.14, "world", false];
stats = processData(mixedData);

console.log("Data type statistics:");
console.log("  Numbers: " + str(stats.numbers));
console.log("  Strings: " + str(stats.strings));
console.log("  Arrays: " + str(stats.arrays));
console.log("  Objects: " + str(stats.objects));
console.log("  Booleans: " + str(stats.booleans));
console.log("  Others: " + str(stats.others));

// Example 7: Type-based formatter
console.log("\nExample 7: Type-based formatter");
function formatValue(value) {
    valueType = typeof(value);

    if (valueType == "string") {
        return "\"" + value + "\"";
    } elif (valueType == "boolean") {
        return str(value);
    } elif (valueType == "array") {
        return "[" + str(len(value)) + " items]";
    } elif (valueType == "object") {
        return "{" + str(len(keys(value))) + " keys}";
    } elif (valueType == "number") {
        return str(value);
    } else {
        return "<" + valueType + ">";
    }
}

values = [42, "hello", true, [1, 2, 3], {a: 1, b: 2}];
console.log("Formatted values:");
for (val in values) {
    console.log("  " + formatValue(val));
}

// Example 8: Type guard pattern
console.log("\nExample 8: Type guard pattern");
function isNumber(value) {
    return isinstance(value, "number");
}

function isString(value) {
    return isinstance(value, "string");
}

function isArray(value) {
    return isinstance(value, "array");
}

testValues = [42, "text", [1, 2], true, null];
for (val in testValues) {
    console.log("Value: " + str(val));
    console.log("  Is number? " + str(isNumber(val)));
    console.log("  Is string? " + str(isString(val)));
    console.log("  Is array? " + str(isArray(val)));
}

console.log("\n=== Type Checking Complete ===");
