// Type Error Demo - Phase 2 Test Cases
// Contains intentional type errors to validate error detection

// Type mismatch in function parameters
function add_numbers(a, b) {
    return a + b;
}

// This should cause type errors
wrong_call1 = add_numbers("hello", 42);      // String instead of number
wrong_call2 = add_numbers(10, true);         // Boolean instead of number
wrong_call3 = add_numbers([1, 2], 42);       // Array instead of number

// Undefined variable usage
undefined_result = some_undefined_variable + 10;

// Array access on non-array
not_array = "hello";
invalid_access = not_array[0];  // Indexing string like array

// Property access on non-object
not_object = 42;
invalid_property = not_object.name;  // Property access on number

// Type mismatch in assignments
function get_string() {
    return "hello";
}

number_var = get_string();  // String assigned to number variable

// Function call with wrong argument count
function three_params(a, b, c) {
    return a + b + c;
}

wrong_args1 = three_params(1, 2);        // Too few arguments
wrong_args2 = three_params(1, 2, 3, 4);  // Too many arguments

// Arithmetic operations on incompatible types
text = "hello";
number = 42;
invalid_math = text * number;        // Cannot multiply string by number
invalid_division = text / 2;         // Cannot divide string
invalid_subtraction = text - 10;     // Cannot subtract from string

// Comparison of incompatible types
array_comparison = [1, 2, 3] < 5;    // Cannot compare array to number
object_comparison = {a: 1} > 10;     // Cannot compare object to number

// Return type mismatch
function should_return_number() {
    return "not a number";               // String returned from number function
}

function should_return_string() {
    return 42;                           // Number returned from string function
}

// Array operations with wrong types
numbers = [1, 2, 3];
numbers[0] = "string";                   // Assigning string to number array element
numbers["invalid"] = 42;                 // Using string as array index

// Object property assignment with wrong types
user = {
    name: "John",
    age: 30,
    active: true
};

user.age = "thirty";                     // String assigned to number property
user.active = "yes";                     // String assigned to boolean property

// Nested access on undefined
maybe_object = null;
nested_access = maybe_object.property.subproperty;  // Null property access

// Function calls on non-functions
not_function = 42;
invalid_call = not_function();       // Calling number as function

// Loop variable type issues
string_array = ["a", "b", "c"];
for (item in string_array) {
    math_result = item * 2;          // Multiplying string by number
}

// Mixed array with inconsistent operations
mixed = [1, "two", true];
for (element in mixed) {
    length = element.length;         // Not all elements have length property
}

console.log("Type error demo - many errors should be detected");