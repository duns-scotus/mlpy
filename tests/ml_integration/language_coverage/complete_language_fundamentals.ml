// Complete Language Fundamentals Test - Covers all basic ML constructs
// This test demonstrates ML language basics that every programmer should know

// All basic literal types
number_int = 42;
number_float = 3.14159;
number_scientific = 1.5e6;
number_negative = -273.15;

string_double = "Hello, World!";
string_single = 'Single quotes work too';
string_escape = "Line 1\nLine 2\tTabbed";
string_empty = "";

boolean_true = true;
boolean_false = false;

// Array literals with mixed types
empty_array = [];
number_array = [1, 2, 3, 4, 5];
string_array = ["apple", "banana", "cherry", "date"];
mixed_array = [1, "two", true, 4.0, false];
nested_array = [[1, 2], [3, 4], [5, 6]];

// Object literals with various property types
empty_object = {};
person = {
    name: "Alice Johnson",
    age: 30,
    active: true,
    salary: 75000.0,
    skills: ["JavaScript", "Python", "ML"]
};

complex_object = {
    id: 1001,
    metadata: {
        created: "2024-01-01",
        updated: "2024-03-15",
        version: 1.2
    },
    settings: {
        theme: "dark",
        notifications: true,
        preferences: {
            language: "en",
            timezone: "UTC"
        }
    }
};

// All arithmetic operations
function arithmetic_operations() {
    a = 20;
    b = 8;

    addition = a + b;
    subtraction = a - b;
    multiplication = a * b;
    division = a / b;
    modulo = a % b;

    print("Arithmetic Results:");
    print("Addition: " + addition);
    print("Subtraction: " + subtraction);
    print("Multiplication: " + multiplication);
    print("Division: " + division);
    print("Modulo: " + modulo);

    // Unary operations
    negative = -a;
    positive = +b;
    print("Negative: " + negative);
    print("Positive: " + positive);

    return {
        add: addition,
        sub: subtraction,
        mul: multiplication,
        div: division,
        mod: modulo
    };
}

// All comparison operations
function comparison_operations() {
    x = 10;
    y = 20;
    z = 10;

    equal = x == z;
    not_equal = x != y;
    less_than = x < y;
    greater_than = y > x;
    less_equal = x <= z;
    greater_equal = y >= x;

    print("Comparison Results:");
    print("Equal (10 == 10): " + equal);
    print("Not Equal (10 != 20): " + not_equal);
    print("Less Than (10 < 20): " + less_than);
    print("Greater Than (20 > 10): " + greater_than);
    print("Less or Equal (10 <= 10): " + less_equal);
    print("Greater or Equal (20 >= 10): " + greater_equal);

    return {
        eq: equal,
        ne: not_equal,
        lt: less_than,
        gt: greater_than,
        le: less_equal,
        ge: greater_equal
    };
}

// All logical operations
function logical_operations() {
    p = true;
    q = false;
    r = true;

    and_result = p && q;
    or_result = p || q;
    not_result = !p;

    complex_and = (p && r) && !q;
    complex_or = (p || q) && r;

    print("Logical Operations:");
    print("AND (true && false): " + and_result);
    print("OR (true || false): " + or_result);
    print("NOT (!true): " + not_result);
    print("Complex AND: " + complex_and);
    print("Complex OR: " + complex_or);

    return {
        and: and_result,
        or: or_result,
        not: not_result,
        complex_and: complex_and,
        complex_or: complex_or
    };
}

// Ternary conditional operator
function ternary_operations() {
    age = 25;
    is_adult = age >= 18 ? "adult" : "minor";

    score = 85;
    grade = score >= 90 ? "A" :
            score >= 80 ? "B" :
            score >= 70 ? "C" :
            score >= 60 ? "D" : "F";

    weather = "sunny";
    activity = weather == "sunny" ? "go to beach" :
               weather == "rainy" ? "stay inside" : "go for a walk";

    print("Ternary Results:");
    print("Age status: " + is_adult);
    print("Grade: " + grade);
    print("Activity: " + activity);

    return {
        status: is_adult,
        grade: grade,
        activity: activity
    };
}

// Variable assignments and scoping
function variable_scoping() {
    global_var = "I'm global";

    function inner_function() {
        local_var = "I'm local";
        modified_global = global_var + " (modified in function)";
        return local_var;
    }

    function_result = inner_function();

    print("Scoping Test:");
    print("Global variable: " + global_var);
    print("Function result: " + function_result);

    return {
        global: global_var,
        local: function_result
    };
}

// Array and object access patterns
function access_patterns() {
    numbers = [10, 20, 30, 40, 50];
    employee = {
        name: "Bob Smith",
        department: "Engineering",
        skills: ["Java", "Python", "Go"]
    };

    // Array access
    first_number = numbers[0];
    last_number = numbers[4];

    // Object member access
    emp_name = employee.name;
    emp_dept = employee.department;
    first_skill = employee.skills[0];

    print("Access Patterns:");
    print("First number: " + first_number);
    print("Last number: " + last_number);
    print("Employee name: " + emp_name);
    print("Employee department: " + emp_dept);
    print("First skill: " + first_skill);

    // Modify through access
    numbers[2] = 999;
    employee.department = "DevOps";

    print("After modifications:");
    print("Modified number: " + numbers[2]);
    print("Modified department: " + employee.department);

    return {
        numbers: numbers,
        employee: employee
    };
}

// Function expressions and first-class functions
function higher_order_functions() {
    // Function expression
    multiply = function(a, b) {
        return a * b;
    };

    // Function as argument
    function apply_operation(x, y, operation) {
        return operation(x, y);
    }

    result1 = apply_operation(5, 3, multiply);

    // Function returning function
    function create_adder(n) {
        return function(x) {
            return x + n;
        };
    }

    add_ten = create_adder(10);
    result2 = add_ten(5);

    print("Higher-order functions:");
    print("Apply operation result: " + result1);
    print("Created adder result: " + result2);

    return {
        multiply_result: result1,
        adder_result: result2
    };
}

// Complex expression evaluation
function complex_expressions() {
    x = 5;
    y = 10;
    z = 15;

    // Complex arithmetic
    complex1 = (x + y) * z - (x * y);
    complex2 = x * (y + z) / (x + 1);
    complex3 = (x > y) ? (x + z) : (y + z);

    // Complex logical
    complex4 = (x < y && y < z) || (x == 5);
    complex5 = !(x > y) && (z > y);

    // Mixed operations
    complex6 = (x + y > 10) ? "high" : "low";
    complex7 = x * 2 + y / 2 - z % 4;

    print("Complex Expressions:");
    print("Complex arithmetic 1: " + complex1);
    print("Complex arithmetic 2: " + complex2);
    print("Complex conditional: " + complex3);
    print("Complex logical 1: " + complex4);
    print("Complex logical 2: " + complex5);
    print("Mixed conditional: " + complex6);
    print("Mixed arithmetic: " + complex7);

    return {
        c1: complex1,
        c2: complex2,
        c3: complex3,
        c4: complex4,
        c5: complex5,
        c6: complex6,
        c7: complex7
    };
}

// Main execution function
function main() {
    print("=== ML Language Fundamentals Test ===");
    print("");

    print("Testing arithmetic operations:");
    arith_results = arithmetic_operations();
    print("");

    print("Testing comparison operations:");
    comp_results = comparison_operations();
    print("");

    print("Testing logical operations:");
    logic_results = logical_operations();
    print("");

    print("Testing ternary operations:");
    ternary_results = ternary_operations();
    print("");

    print("Testing variable scoping:");
    scope_results = variable_scoping();
    print("");

    print("Testing access patterns:");
    access_results = access_patterns();
    print("");

    print("Testing higher-order functions:");
    hof_results = higher_order_functions();
    print("");

    print("Testing complex expressions:");
    complex_results = complex_expressions();
    print("");

    print("=== All Fundamental Tests Complete ===");

    return {
        arithmetic: arith_results,
        comparisons: comp_results,
        logical: logic_results,
        ternary: ternary_results,
        scoping: scope_results,
        access: access_results,
        functions: hof_results,
        complex: complex_results
    };
}

// Execute the test
main();