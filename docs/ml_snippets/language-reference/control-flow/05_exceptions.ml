// ============================================
// Example: Exception Handling
// Category: language-reference/control-flow
// Demonstrates: try/except/finally, throw
// ============================================

import console;

// Basic try-except
console.log("Basic exception handling:");
try {
    x = 10;
    y = 0;
    if (y == 0) {
        throw {message: "Division by zero"};
    }
    result = x / y;
} except (err) {
    console.log("Error caught: Division by zero");
    result = null;
}

// Try-except-finally
console.log("\nWith finally block:");
status = "";
try {
    value = 42;
    if (value > 40) {
        throw {message: "Value too large"};
    }
    status = "success";
} except (err) {
    console.log("Error: Value too large");
    status = "failed";
} finally {
    console.log("Status: " + status);
    console.log("Cleanup complete");
}

// Function with error handling
function safeDivide(a, b) {
    if (b == 0) {
        throw {message: "Cannot divide by zero"};
    }
    return a / b;
}

console.log("\nFunction with exception:");
try {
    result1 = safeDivide(10, 2);
    console.log("10 / 2 = " + str(result1));

    result2 = safeDivide(10, 0);
    console.log("10 / 0 = " + str(result2));
} except (err) {
    console.log("Division error: Cannot divide by zero");
}

// Validating input
function processAge(age) {
    if (age < 0) {
        throw {message: "Age cannot be negative"};
    }
    if (age > 150) {
        throw {message: "Age unrealistic"};
    }
    return age;
}

console.log("\nInput validation:");
ages = [25, -5, 200, 30];
for (age in ages) {
    try {
        validAge = processAge(age);
        console.log("Valid age: " + str(validAge));
    } except (err) {
        console.log("Invalid age " + str(age));
    }
}

// Nested try-except
console.log("\nNested exception handling:");
try {
    console.log("Outer try block");
    try {
        console.log("Inner try block");
        throw {message: "Inner error"};
    } except (err) {
        console.log("Inner except: caught error");
    }
    console.log("After inner try-except");
} except (err) {
    console.log("Outer except: caught error");
}

console.log("\nAll exception handling complete");
