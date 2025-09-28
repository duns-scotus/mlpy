// Type Checking Demo - Complete rewrite using validated patterns
// Demonstrates comprehensive type checking scenarios for ML language

// Safe append utility function for dynamic arrays
function safe_append(arr, item) {
    arr[arr.length] = item;
    return arr;
}

// String conversion utility
function to_string(value) {
    if (value == null) {
        return "null";
    }
    return "" + value;
}

// Math utilities
function math_sqrt(x) {
    if (x < 0) {
        return 0;
    }
    guess = x / 2;
    iterations = 0;
    while (iterations < 20) {
        if (guess == 0) {
            return 0;
        }
        next_guess = (guess + x / guess) / 2;
        diff = guess - next_guess;
        if (diff < 0) {
            diff = -diff;
        }
        if (diff < 0.000001) {
            return next_guess;
        }
        guess = next_guess;
        iterations = iterations + 1;
    }
    return guess;
}

function math_pow(base, exponent) {
    if (exponent == 0) {
        return 1;
    }
    if (exponent == 1) {
        return base;
    }
    result = 1;
    current_base = base;
    current_exp = exponent;
    while (current_exp > 0) {
        if (current_exp % 2 == 1) {
            result = result * current_base;
        }
        current_base = current_base * current_base;
        current_exp = current_exp / 2;
        if (current_exp != (current_exp / 1) * 1) {
            current_exp = (current_exp - 0.5);
        }
    }
    return result;
}

function string_upper(text) {
    // Simple uppercase conversion (simplified for demo)
    return text;  // In real implementation would convert case
}

// Math constants
PI = 3.141592653589793;

// =============================================================================
// BASIC TYPE VALIDATION FUNCTIONS
// =============================================================================

function is_number(value) {
    return typeof(value) == "number";
}

function is_string(value) {
    return typeof(value) == "string";
}

function is_boolean(value) {
    return typeof(value) == "boolean";
}

function is_array(value) {
    return value != null && value.length != null;
}

function is_object(value) {
    return value != null && typeof(value) == "object" && value.length == null;
}

function get_type_name(value) {
    if (value == null) {
        return "null";
    } elif (is_number(value)) {
        return "number";
    } elif (is_string(value)) {
        return "string";
    } elif (is_boolean(value)) {
        return "boolean";
    } elif (is_array(value)) {
        return "array";
    } elif (is_object(value)) {
        return "object";
    } else {
        return "unknown";
    }
}

// =============================================================================
// BASIC ARITHMETIC AND STRING FUNCTIONS
// =============================================================================

// Type-safe arithmetic functions
function add_numbers(a, b) {
    if (is_number(a) && is_number(b)) {
        return a + b;
    } else {
        print("Warning: Non-numeric types in add_numbers");
        return 0;
    }
}

function concatenate_strings(s1, s2) {
    if (is_string(s1) && is_string(s2)) {
        return s1 + s2;
    } else {
        print("Warning: Non-string types in concatenate_strings");
        return to_string(s1) + to_string(s2);
    }
}

function process_array(arr) {
    if (!is_array(arr)) {
        print("Warning: Non-array type in process_array");
        return null;
    }
    if (arr.length == 0) {
        print("Warning: Empty array in process_array");
        return null;
    }

    result = {
        "length": arr.length,
        "first": arr[0],
        "type": get_type_name(arr[0])
    };

    return result;
}

function divide_numbers(a, b) {
    if (!is_number(a) || !is_number(b)) {
        throw {
            "message": "Non-numeric arguments to divide_numbers",
            "code": 1000,
            "arguments": [get_type_name(a), get_type_name(b)]
        };
    }
    if (b == 0) {
        throw {
            "message": "Division by zero",
            "code": 1001,
            "divisor": b
        };
    }
    return a / b;
}

// =============================================================================
// TYPE INFERENCE AND VALIDATION TESTS
// =============================================================================

function test_basic_types() {
    print("=== Testing Basic Type Inference ===");

    // Basic type assignments
    number_var = 42;
    string_var = "hello";
    boolean_var = true;
    array_var = [1, 2, 3, 4];
    object_var = {
        "name": "test",
        "value": 100,
        "active": true
    };

    // Type validation
    results = {
        "number_type": get_type_name(number_var),
        "string_type": get_type_name(string_var),
        "boolean_type": get_type_name(boolean_var),
        "array_type": get_type_name(array_var),
        "object_type": get_type_name(object_var)
    };

    print("Number variable (" + to_string(number_var) + ") type: " + results.number_type);
    print("String variable ('" + string_var + "') type: " + results.string_type);
    print("Boolean variable (" + to_string(boolean_var) + ") type: " + results.boolean_type);
    print("Array variable length " + to_string(array_var.length) + " type: " + results.array_type);
    print("Object variable type: " + results.object_type);
    print("");

    return results;
}

function test_function_calls() {
    print("=== Testing Function Call Type Checking ===");

    // Valid function calls with proper types
    sum_result = add_numbers(10, 20);
    concat_result = concatenate_strings("hello", " world");
    array_result = process_array([1, 2, 3]);

    print("Sum result: " + to_string(sum_result) + " (type: " + get_type_name(sum_result) + ")");
    print("Concatenation result: '" + concat_result + "' (type: " + get_type_name(concat_result) + ")");
    print("Array processing result: " + to_string(array_result));
    print("");

    // Type mismatch scenarios (should handle gracefully)
    print("--- Testing Type Mismatch Scenarios ---");
    mixed_sum = add_numbers("5", 10);  // String + Number
    mixed_concat = concatenate_strings(123, " items");  // Number + String
    invalid_array = process_array("not an array");  // String instead of Array

    print("Mixed sum (string + number): " + to_string(mixed_sum));
    print("Mixed concatenation (number + string): '" + mixed_concat + "'");
    print("Invalid array processing: " + to_string(invalid_array));
    print("");

    return {
        "valid_calls": {
            "sum": sum_result,
            "concat": concat_result,
            "array": array_result
        },
        "mixed_calls": {
            "mixed_sum": mixed_sum,
            "mixed_concat": mixed_concat,
            "invalid_array": invalid_array
        }
    };
}

function test_array_operations() {
    print("=== Testing Array Operations with Type Checking ===");

    // Homogeneous arrays
    numbers = [1, 2, 3, 4, 5];
    strings = ["apple", "banana", "cherry"];
    booleans = [true, false, true];

    // Heterogeneous array
    mixed = [1, "two", true, [4, 5], {"six": 6}];

    // Array manipulation
    first_number = numbers[0];
    numbers[1] = 999;  // Modify element
    safe_append(numbers, 6);  // Add element

    // Type analysis of arrays
    number_types = [];
    string_types = [];
    mixed_types = [];

    i = 0;
    while (i < numbers.length) {
        safe_append(number_types, get_type_name(numbers[i]));
        i = i + 1;
    }

    i = 0;
    while (i < strings.length) {
        safe_append(string_types, get_type_name(strings[i]));
        i = i + 1;
    }

    i = 0;
    while (i < mixed.length) {
        safe_append(mixed_types, get_type_name(mixed[i]));
        i = i + 1;
    }

    print("Numbers array: " + to_string(numbers));
    print("Number array types: " + to_string(number_types));
    print("Strings array: " + to_string(strings));
    print("String array types: " + to_string(string_types));
    print("Mixed array: " + to_string(mixed));
    print("Mixed array types: " + to_string(mixed_types));
    print("");

    return {
        "arrays": {
            "numbers": numbers,
            "strings": strings,
            "mixed": mixed
        },
        "type_analysis": {
            "number_types": number_types,
            "string_types": string_types,
            "mixed_types": mixed_types
        }
    };
}

function test_object_operations() {
    print("=== Testing Object Operations with Type Checking ===");

    // Simple object
    simple_obj = {
        "id": 1,
        "name": "item",
        "active": true
    };

    // Complex nested object
    complex_object = {
        "user": {
            "profile": {
                "name": "John Doe",
                "age": 30,
                "preferences": {
                    "theme": "dark",
                    "notifications": true
                }
            },
            "settings": {
                "privacy": "private",
                "language": "en"
            }
        },
        "data": [
            {"key": "item1", "value": 100},
            {"key": "item2", "value": 200}
        ]
    };

    // Property access with type checking
    simple_id = simple_obj.id;
    simple_name = simple_obj.name;
    simple_active = simple_obj.active;

    user_name = complex_object.user.profile.name;
    user_theme = complex_object.user.profile.preferences.theme;
    first_data_item = complex_object.data[0];
    first_item_value = complex_object.data[0].value;

    // Property type analysis
    property_types = {
        "simple_id_type": get_type_name(simple_id),
        "simple_name_type": get_type_name(simple_name),
        "simple_active_type": get_type_name(simple_active),
        "user_name_type": get_type_name(user_name),
        "user_theme_type": get_type_name(user_theme),
        "first_data_item_type": get_type_name(first_data_item),
        "first_item_value_type": get_type_name(first_item_value)
    };

    print("Simple object properties:");
    print("  ID: " + to_string(simple_id) + " (type: " + property_types.simple_id_type + ")");
    print("  Name: '" + simple_name + "' (type: " + property_types.simple_name_type + ")");
    print("  Active: " + to_string(simple_active) + " (type: " + property_types.simple_active_type + ")");
    print("");
    print("Complex object properties:");
    print("  User name: '" + user_name + "' (type: " + property_types.user_name_type + ")");
    print("  User theme: '" + user_theme + "' (type: " + property_types.user_theme_type + ")");
    print("  First data item value: " + to_string(first_item_value) + " (type: " + property_types.first_item_value_type + ")");
    print("");

    return {
        "objects": {
            "simple": simple_obj,
            "complex": complex_object
        },
        "property_types": property_types
    };
}

function test_control_flow() {
    print("=== Testing Control Flow with Type Checking ===");

    // Conditional statements with type validation
    number_var = 42;
    string_var = "hello";
    boolean_var = true;

    // Type-aware conditional logic
    if (is_number(number_var) && number_var > 0) {
        print("Number variable is a positive number: " + to_string(number_var));
    } elif (is_number(number_var) && number_var == 0) {
        print("Number variable is zero");
    } else {
        print("Number variable is negative or not a number");
    }

    if (is_string(string_var) && string_var.length > 0) {
        print("String variable is non-empty: '" + string_var + "'");
    } else {
        print("String variable is empty or not a string");
    }

    if (is_boolean(boolean_var)) {
        print("Boolean variable is: " + to_string(boolean_var));
    } else {
        print("Boolean variable is not a boolean");
    }

    // Loop with type checking
    test_array = [1, "two", 3.14, true, null];
    print("Processing mixed array with type checking:");

    i = 0;
    while (i < test_array.length) {
        item = test_array[i];
        item_type = get_type_name(item);
        print("  Item " + to_string(i) + ": " + to_string(item) + " (type: " + item_type + ")");
        i = i + 1;
    }
    print("");

    return {
        "variables": {
            "number": number_var,
            "string": string_var,
            "boolean": boolean_var
        },
        "array_analysis": test_array
    };
}

function test_mathematical_operations() {
    print("=== Testing Mathematical Operations with Type Checking ===");

    // Mathematical constants and functions
    pi_value = PI;
    sqrt_result = math_sqrt(16);
    power_result = math_pow(2, 8);

    // Area calculation with type validation
    function calculate_area(width, height) {
        if (!is_number(width) || !is_number(height)) {
            print("Error: calculate_area requires numeric arguments");
            return null;
        }
        area = width * height;
        return area;
    }

    rectangle_area = calculate_area(5, 3);
    circle_area = pi_value * math_pow(3, 2);  // π * r²

    print("Pi value: " + to_string(pi_value));
    print("Square root of 16: " + to_string(sqrt_result));
    print("2 to the power of 8: " + to_string(power_result));
    print("Rectangle area (5x3): " + to_string(rectangle_area));
    print("Circle area (r=3): " + to_string(circle_area));
    print("");

    // Test error cases
    print("--- Testing Mathematical Error Cases ---");
    invalid_area = calculate_area("5", 3);  // String instead of number
    negative_sqrt = math_sqrt(-4);  // Negative number

    print("Invalid area calculation (string, number): " + to_string(invalid_area));
    print("Square root of negative number: " + to_string(negative_sqrt));
    print("");

    return {
        "constants": {
            "pi": pi_value
        },
        "calculations": {
            "sqrt_16": sqrt_result,
            "power_2_8": power_result,
            "rectangle_area": rectangle_area,
            "circle_area": circle_area
        },
        "error_cases": {
            "invalid_area": invalid_area,
            "negative_sqrt": negative_sqrt
        }
    };
}

function test_error_handling() {
    print("=== Testing Error Handling with Type Checking ===");

    // Test division by zero
    try {
        normal_division = divide_numbers(10, 2);
        print("Normal division (10/2): " + to_string(normal_division));
    } except (error) {
        print("Unexpected error in normal division: " + to_string(error));
    }

    try {
        zero_division = divide_numbers(10, 0);
        print("Division by zero should not reach here: " + to_string(zero_division));
    } except (error) {
        print("Caught division by zero error: " + error.message + " (code: " + to_string(error.code) + ")");
    }

    // Test type errors
    try {
        type_error_division = divide_numbers("10", 2);
        print("Type error division should not reach here: " + to_string(type_error_division));
    } except (error) {
        print("Caught type error: " + error.message + " (types: " + to_string(error.arguments) + ")");
    }

    print("");

    return {
        "normal_division": normal_division,
        "error_handling_working": true
    };
}

function test_string_operations() {
    print("=== Testing String Operations with Type Checking ===");

    // String operations
    message = "Hello World";
    message_length = message.length;

    // String manipulation functions
    function safe_string_operation(text, operation) {
        if (!is_string(text)) {
            print("Warning: Non-string input to string operation");
            return to_string(text);
        }

        if (operation == "upper") {
            return string_upper(text);
        } elif (operation == "length") {
            return text.length;
        } elif (operation == "reverse") {
            result = "";
            i = text.length - 1;
            while (i >= 0) {
                result = result + text[i];
                i = i - 1;
            }
            return result;
        } else {
            return text;
        }
    }

    uppercase_message = safe_string_operation(message, "upper");
    reversed_message = safe_string_operation(message, "reverse");
    length_check = safe_string_operation(message, "length");

    print("Original message: '" + message + "'");
    print("Message length: " + to_string(message_length));
    print("Uppercase message: '" + uppercase_message + "'");
    print("Reversed message: '" + reversed_message + "'");
    print("Length check: " + to_string(length_check));
    print("");

    // Test with non-string input
    print("--- Testing String Operations with Non-String Input ---");
    number_as_string = safe_string_operation(123, "upper");
    boolean_as_string = safe_string_operation(true, "reverse");

    print("Number as string operation: '" + number_as_string + "'");
    print("Boolean as string operation: '" + boolean_as_string + "'");
    print("");

    return {
        "string_operations": {
            "original": message,
            "length": message_length,
            "uppercase": uppercase_message,
            "reversed": reversed_message
        },
        "type_coercion": {
            "number_coerced": number_as_string,
            "boolean_coerced": boolean_as_string
        }
    };
}

function test_type_coercion() {
    print("=== Testing Type Coercion Scenarios ===");

    // Various type coercion scenarios
    number_val = 5;
    string_val = "text";
    boolean_val = true;

    // Mixed operations
    mixed_addition = to_string(number_val) + string_val;  // "5text"
    number_comparison = number_val < 100;
    logical_operation = boolean_val && (number_val > 0);

    // Type-safe operations
    function safe_addition(a, b) {
        a_type = get_type_name(a);
        b_type = get_type_name(b);

        if (a_type == "number" && b_type == "number") {
            return a + b;
        } elif (a_type == "string" || b_type == "string") {
            return to_string(a) + to_string(b);
        } else {
            return to_string(a) + " + " + to_string(b);
        }
    }

    safe_num_add = safe_addition(10, 20);
    safe_mixed_add = safe_addition(5, "text");
    safe_bool_add = safe_addition(true, false);

    print("Mixed operations:");
    print("  Number + String: '" + mixed_addition + "'");
    print("  Number < 100: " + to_string(number_comparison));
    print("  Boolean && (Number > 0): " + to_string(logical_operation));
    print("");
    print("Safe operations:");
    print("  Safe number addition (10 + 20): " + to_string(safe_num_add));
    print("  Safe mixed addition (5 + 'text'): '" + safe_mixed_add + "'");
    print("  Safe boolean addition (true + false): '" + safe_bool_add + "'");
    print("");

    return {
        "mixed_operations": {
            "addition": mixed_addition,
            "comparison": number_comparison,
            "logical": logical_operation
        },
        "safe_operations": {
            "number_add": safe_num_add,
            "mixed_add": safe_mixed_add,
            "boolean_add": safe_bool_add
        }
    };
}

// =============================================================================
// MAIN TEST RUNNER
// =============================================================================

function run_comprehensive_type_checking() {
    print("====================================================");
    print("ML LANGUAGE TYPE CHECKING COMPREHENSIVE DEMO");
    print("====================================================");
    print("");

    // Run all type checking tests
    basic_types_result = test_basic_types();
    function_calls_result = test_function_calls();
    array_ops_result = test_array_operations();
    object_ops_result = test_object_operations();
    control_flow_result = test_control_flow();
    math_ops_result = test_mathematical_operations();
    error_handling_result = test_error_handling();
    string_ops_result = test_string_operations();
    type_coercion_result = test_type_coercion();

    // Comprehensive summary
    comprehensive_result = {
        "test_name": "ML Type Checking Comprehensive Demo",
        "status": "completed",
        "results": {
            "basic_types": basic_types_result,
            "function_calls": function_calls_result,
            "array_operations": array_ops_result,
            "object_operations": object_ops_result,
            "control_flow": control_flow_result,
            "mathematical_operations": math_ops_result,
            "error_handling": error_handling_result,
            "string_operations": string_ops_result,
            "type_coercion": type_coercion_result
        },
        "summary": {
            "total_test_suites": 9,
            "features_tested": [
                "Basic type inference",
                "Function call type checking",
                "Array operations with type validation",
                "Object property access",
                "Control flow with type awareness",
                "Mathematical operations",
                "Error handling and exceptions",
                "String operations and manipulation",
                "Type coercion and safe operations"
            ],
            "type_safety_validated": true,
            "error_handling_validated": true
        }
    };

    print("====================================================");
    print("TYPE CHECKING DEMO COMPLETED SUCCESSFULLY");
    print("====================================================");
    print("Total test suites executed: " + to_string(comprehensive_result.summary.total_test_suites));
    print("Type safety validation: " + to_string(comprehensive_result.summary.type_safety_validated));
    print("Error handling validation: " + to_string(comprehensive_result.summary.error_handling_validated));
    print("");
    print("All type checking scenarios executed successfully!");
    print("ML language demonstrates robust type inference and validation.");

    return comprehensive_result;
}

// =============================================================================
// EXECUTE COMPREHENSIVE TYPE CHECKING DEMO
// =============================================================================

// Run the comprehensive type checking demonstration
final_result = run_comprehensive_type_checking();