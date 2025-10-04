// Test builtin module: Type checking functions
// Features tested: typeof(), isinstance()
// NO imports needed - builtin functions are auto-imported

function test_typeof_primitives() {
    results = {};

    // Boolean type
    results.typeof_true = typeof(true);           // "boolean"
    results.typeof_false = typeof(false);         // "boolean"

    // Number type
    results.typeof_int = typeof(42);              // "number"
    results.typeof_float = typeof(3.14);          // "number"
    results.typeof_negative = typeof(-100);       // "number"
    results.typeof_zero = typeof(0);              // "number"

    // String type
    results.typeof_string = typeof("hello");      // "string"
    results.typeof_empty_str = typeof("");        // "string"

    // Array type
    results.typeof_array = typeof([1, 2, 3]);     // "array"
    results.typeof_empty_array = typeof([]);      // "array"

    // Object type
    results.typeof_object = typeof({a: 1, b: 2}); // "object"
    results.typeof_empty_obj = typeof({});        // "object"

    // Function type
    results.typeof_function = typeof(test_typeof_primitives); // "function"

    return results;
}

function test_isinstance_primitives() {
    results = {};

    // Boolean checks
    results.true_is_boolean = isinstance(true, "boolean");        // true
    results.false_is_boolean = isinstance(false, "boolean");      // true
    results.int_is_not_boolean = isinstance(42, "boolean");       // false

    // Number checks
    results.int_is_number = isinstance(42, "number");             // true
    results.float_is_number = isinstance(3.14, "number");         // true
    results.str_is_not_number = isinstance("42", "number");       // false

    // String checks
    results.str_is_string = isinstance("hello", "string");        // true
    results.int_is_not_string = isinstance(42, "string");         // false

    // Array checks
    results.array_is_array = isinstance([1,2,3], "array");        // true
    results.obj_is_not_array = isinstance({a:1}, "array");        // false

    // Object checks
    results.obj_is_object = isinstance({a: 1}, "object");         // true
    results.array_is_not_object = isinstance([1,2], "object");    // false

    // Function checks
    results.func_is_function = isinstance(test_isinstance_primitives, "function"); // true
    results.int_is_not_function = isinstance(42, "function");     // false

    return results;
}

function test_type_guards() {
    results = {};

    // Guard for number
    value = 42;
    if (typeof(value) == "number") {
        results.number_guard = true;
    } else {
        results.number_guard = false;
    }

    // Guard for string
    value2 = "hello";
    if (typeof(value2) == "string") {
        results.string_guard = true;
    } else {
        results.string_guard = false;
    }

    // Guard for array
    value3 = [1, 2, 3];
    if (typeof(value3) == "array") {
        results.array_guard = true;
    } else {
        results.array_guard = false;
    }

    // Guard for object
    value4 = {a: 1, b: 2};
    if (typeof(value4) == "object") {
        results.object_guard = true;
    } else {
        results.object_guard = false;
    }

    return results;
}

function process_by_type(value) {
    type_name = typeof(value);

    if (type_name == "number") {
        return value * 2;
    } elif (type_name == "string") {
        return value;
    } elif (type_name == "array") {
        return len(value);
    } elif (type_name == "object") {
        return len(keys(value));
    } elif (type_name == "boolean") {
        return int(value);
    } else {
        return "unknown";
    }
}

function test_polymorphic_function() {
    results = {};

    results.process_number = process_by_type(42);        // 84
    results.process_string = process_by_type("hello");   // "hello"
    results.process_array = process_by_type([1,2,3,4]);  // 4
    results.process_object = process_by_type({a:1, b:2, c:3}); // 3
    results.process_boolean = process_by_type(true);     // 1

    return results;
}

function test_type_checking_in_conditionals() {
    results = {};
    values = [42, "hello", true, [1,2,3], {a: 1}];

    number_count = 0;
    string_count = 0;
    boolean_count = 0;
    array_count = 0;
    object_count = 0;

    for (val in values) {
        t = typeof(val);
        if (t == "number") {
            number_count = number_count + 1;
        } elif (t == "string") {
            string_count = string_count + 1;
        } elif (t == "boolean") {
            boolean_count = boolean_count + 1;
        } elif (t == "array") {
            array_count = array_count + 1;
        } elif (t == "object") {
            object_count = object_count + 1;
        }
    }

    results.numbers = number_count;     // 1
    results.strings = string_count;     // 1
    results.booleans = boolean_count;   // 1
    results.arrays = array_count;       // 1
    results.objects = object_count;     // 1

    return results;
}

function main() {
    all_results = {};

    all_results.typeof_tests = test_typeof_primitives();
    all_results.isinstance_tests = test_isinstance_primitives();
    all_results.guards = test_type_guards();
    all_results.polymorphic = test_polymorphic_function();
    all_results.counting = test_type_checking_in_conditionals();

    return all_results;
}

// Run tests
test_results = main();
