// Type Error Demo - Phase 2 Test Cases
// Contains intentional type errors to validate error detection

// Type mismatch in function parameters
function add_numbers(a: number, b: number) {
    return a + b;
}

// This should cause type errors
let wrong_call1 = add_numbers("hello", 42);      // String instead of number
let wrong_call2 = add_numbers(10, true);         // Boolean instead of number
let wrong_call3 = add_numbers([1, 2], 42);       // Array instead of number

// Undefined variable usage
let undefined_result = some_undefined_variable + 10;

// Array access on non-array
let not_array = "hello";
let invalid_access = not_array[0];  // Indexing string like array

// Property access on non-object
let not_object = 42;
let invalid_property = not_object.name;  // Property access on number

// Type mismatch in assignments
function get_string() {
    return "hello";
}

let number_var: number = get_string();  // String assigned to number variable

// Function call with wrong argument count
function three_params(a: number, b: number, c: number) {
    return a + b + c;
}

let wrong_args1 = three_params(1, 2);        // Too few arguments
let wrong_args2 = three_params(1, 2, 3, 4);  // Too many arguments

// Arithmetic operations on incompatible types
let text = "hello";
let number = 42;
let invalid_math = text * number;        // Cannot multiply string by number
let invalid_division = text / 2;         // Cannot divide string
let invalid_subtraction = text - 10;     // Cannot subtract from string

// Comparison of incompatible types
let array_comparison = [1, 2, 3] < 5;    // Cannot compare array to number
let object_comparison = {a: 1} > 10;     // Cannot compare object to number

// Return type mismatch
function should_return_number(): number {
    return "not a number";               // String returned from number function
}

function should_return_string(): string {
    return 42;                           // Number returned from string function
}

// Array operations with wrong types
let numbers = [1, 2, 3];
numbers[0] = "string";                   // Assigning string to number array element
numbers["invalid"] = 42;                 // Using string as array index

// Object property assignment with wrong types
let user = {
    name: "John",
    age: 30,
    active: true
};

user.age = "thirty";                     // String assigned to number property
user.active = "yes";                     // String assigned to boolean property

// Nested access on undefined
let maybe_object = null;
let nested_access = maybe_object.property.subproperty;  // Null property access

// Function calls on non-functions
let not_function = 42;
let invalid_call = not_function();       // Calling number as function

// Loop variable type issues
let string_array = ["a", "b", "c"];
for (item in string_array) {
    let math_result = item * 2;          // Multiplying string by number
}

// Mixed array with inconsistent operations
let mixed = [1, "two", true];
for (element in mixed) {
    let length = element.length;         // Not all elements have length property
}

console.log("Type error demo - many errors should be detected");