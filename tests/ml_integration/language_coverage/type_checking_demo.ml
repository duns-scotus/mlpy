// Type Checking Demo - Phase 2 Test Cases
// Demonstrates various type checking scenarios for ML language

// Valid type scenarios
function add_numbers(a, b) {
    return a + b;
}

function concatenate_strings(s1, s2) {
    return s1 + s2;
}

function process_array(arr) {
    length = arr.length;
    first = arr[0];
    return first;
}

// Basic type inference tests
number_var = 42;
string_var = "hello";
boolean_var = true;
array_var = [1, 2, 3, 4];
object_var = {
    name: "test",
    value: 100,
    active: true
};

// Function call type checking
sum_result = add_numbers(10, 20);
concat_result = concatenate_strings("hello", " world");
array_result = process_array([1, 2, 3]);

// Array operations with type consistency
numbers = [1, 2, 3];
first_number = numbers[0];
numbers[1] = 999;

// Object property access
obj = {
    id: 1,
    name: "item",
    properties: {
        color: "blue",
        size: "large"
    }
};

item_id = obj.id;
item_name = obj.name;
item_color = obj.properties.color;

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
function calculate_area(width, height) {
    area = width * height;
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
mixed_addition = 5 + "text";  // Should be handled gracefully
comparison = number_var < 100;
logical_op = boolean_var && (number_var > 0);

// Nested function calls
function double_value(x) {
    return x * 2;
}

function apply_operation(value) {
    return double_value(value) + 10;
}

final_result = apply_operation(15);

// Array with consistent types
string_array = ["apple", "banana", "cherry"];
mixed_array = [1, "two", true];  // Mixed types

// Complex object with nested properties
complex_object = {
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

user_name = complex_object.user.profile.name;
user_theme = complex_object.user.profile.preferences.theme;
first_data_item = complex_object.data[0];
first_item_value = complex_object.data[0].value;

// Error handling with type checking
try {
    risky_operation = divide_numbers(10, 0);
} except (error) {
    console.log("Error occurred: " + error);
}

function divide_numbers(a, b) {
    if (b == 0) {
        throw { message: "Division by zero", code: 1001 };
    }
    return a / b;
}

// Type checking with Math operations
pi_value = Math.PI;
sqrt_result = Math.sqrt(16);
power_result = Math.pow(2, 8);

// String operations
message = "Hello World";
message_length = message.length;
uppercase_message = message.toUpperCase();

console.log("Type checking demo completed successfully");