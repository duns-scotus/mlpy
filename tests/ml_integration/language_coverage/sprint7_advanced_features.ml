// Sprint 7: Advanced ML Language Features Demonstration
// Tests current language capabilities and demonstrates working ML code

// Current ML Object Support
person_data = {
    name: "Alice",
    age: 30,
    email: "alice@example.com"
};

// Function that demonstrates conditional logic (simulating pattern matching)
function processValue(input, type_hint) {
    if (type_hint == "number") {
        if (input > 100) {
            return "Large number: " + input;
        } elif (input > 0) {
            return "Small number: " + input;
        } else {
            return "Zero or negative: " + input;
        }
    } elif (type_hint == "string") {
        return "Text: " + input;
    } else {
        return "Unknown type";
    }
}

// Current array manipulation (simulating array comprehensions)
function createSquares(numbers) {
    squares = [];
    i = 0;
    while (i < numbers.length()) {
        value = numbers[i];
        if (value > 2) {
            squares.push(value * value);
        }
        i = i + 1;
    }
    return squares;
}

// Error handling with explicit checks (simulating Result types)
function divide(a, b) {
    if (b == 0) {
        return {
            success: false,
            error: "Division by zero error"
        };
    } else {
        return {
            success: true,
            value: a / b
        };
    }
}

// Complex calculation with error propagation
function complexCalculation(x, y) {
    result1 = divide(x, 2);
    if (!result1.success) {
        return result1;
    }

    result2 = divide(y, 3);
    if (!result2.success) {
        return result2;
    }

    return {
        success: true,
        value: result1.value + result2.value
    };
}

// Demonstration of current ML capabilities
function main_demo() {
    // Test conditional processing
    print("Processing number 150:");
    print(processValue(150, "number"));

    print("Processing string 'hello':");
    print(processValue("hello", "string"));

    // Test array operations
    numbers = [1, 2, 3, 4, 5];
    squares = createSquares(numbers);
    print("Original numbers: " + numbers);
    print("Filtered squares: " + squares);

    // Test error handling
    print("Testing division:");
    safe_result = complexCalculation(10, 6);
    if (safe_result.success) {
        print("Result: " + safe_result.value);
    } else {
        print("Error: " + safe_result.error);
    }

    // Test object access
    print("Person data:");
    print("Name: " + person_data.name);
    print("Age: " + person_data.age);
    print("Email: " + person_data.email);

    print("Advanced ML features demonstration complete!");
}

// Run the demonstration
main_demo();