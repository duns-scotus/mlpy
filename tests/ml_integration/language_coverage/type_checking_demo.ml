// Type Checking Demo - Phase 2 Test Cases
// Demonstrates various type checking scenarios for ML language

// Valid type scenarios
function add_numbers(a: number, b: number) {
    return a + b;
}

function concatenate_strings(s1: string, s2: string) {
    return s1 + s2;
}

function process_array(arr: array) {
    let length = arr.length;
    let first = arr[0];
    return first;
}

// Basic type inference tests
let number_var = 42;
let string_var = "hello";
let boolean_var = true;
let array_var = [1, 2, 3, 4];
let object_var = {
    name: "test",
    value: 100,
    active: true
};

// Function call type checking
let sum_result = add_numbers(10, 20);
let concat_result = concatenate_strings("hello", " world");
let array_result = process_array([1, 2, 3]);

// Array operations with type consistency
let numbers = [1, 2, 3];
let first_number = numbers[0];
numbers[1] = 999;

// Object property access
let obj = {
    id: 1,
    name: "item",
    properties: {
        color: "blue",
        size: "large"
    }
};

let item_id = obj.id;
let item_name = obj.name;
let item_color = obj.properties.color;

// Control flow with type checking
if (number_var > 0) {
    console.log("Positive number");
} else {
    console.log("Non-positive number");
}

// Loop with type inference
for (item in array_var) {
    console.log(item);
}

while (number_var > 0) {
    number_var = number_var - 1;
}

// Function with return type inference
function calculate_area(width: number, height: number) {
    let area = width * height;
    return area;
}

function get_user_info() {
    return {
        id: 123,
        username: "testuser",
        active: true
    };
}

// Type coercion scenarios
let mixed_addition = 5 + "text";  // Should be handled gracefully
let comparison = number_var < 100;
let logical_op = boolean_var && (number_var > 0);

// Nested function calls
function double_value(x: number) {
    return x * 2;
}

function apply_operation(value: number) {
    return double_value(value) + 10;
}

let final_result = apply_operation(15);

// Array with consistent types
let string_array = ["apple", "banana", "cherry"];
let mixed_array = [1, "two", true];  // Mixed types

// Complex object with nested properties
let complex_object = {
    user: {
        profile: {
            name: "John Doe",
            age: 30,
            preferences: {
                theme: "dark",
                notifications: true
            }
        },
        settings: {
            privacy: "private",
            language: "en"
        }
    },
    data: [
        { key: "item1", value: 100 },
        { key: "item2", value: 200 }
    ]
};

let user_name = complex_object.user.profile.name;
let user_theme = complex_object.user.profile.preferences.theme;
let first_data_item = complex_object.data[0];
let first_item_value = complex_object.data[0].value;

// Error handling with type checking
try {
    let risky_operation = divide_numbers(10, 0);
} except (error) {
    console.log("Error occurred: " + error);
}

function divide_numbers(a: number, b: number) {
    if (b == 0) {
        throw { message: "Division by zero", code: 1001 };
    }
    return a / b;
}

// Type checking with Math operations
let pi_value = Math.PI;
let sqrt_result = Math.sqrt(16);
let power_result = Math.pow(2, 8);

// String operations
let message = "Hello World";
let message_length = message.length;
let uppercase_message = message.toUpperCase();

console.log("Type checking demo completed successfully");