// Test builtin module: Print function
// Features tested: print()
// NO imports needed - builtin functions are auto-imported

function test_print_numbers() {
    results = {};

    // Print integers
    print(42);
    print(0);
    print(-100);

    // Print floats
    print(3.14);
    print(0.0);
    print(-2.5);

    results.printed_numbers = true;
    return results;
}

function test_print_booleans() {
    results = {};

    // Print booleans (should print lowercase: true, false)
    print(true);
    print(false);

    results.printed_booleans = true;
    return results;
}

function test_print_strings() {
    results = {};

    // Print strings
    print("Hello, World!");
    print("");
    print("ML is awesome");

    results.printed_strings = true;
    return results;
}

function test_print_arrays() {
    results = {};

    // Print arrays
    print([1, 2, 3, 4, 5]);
    print([]);
    print(["a", "b", "c"]);
    print([true, false]);

    results.printed_arrays = true;
    return results;
}

function test_print_objects() {
    results = {};

    // Print objects
    print({a: 1, b: 2});
    print({});
    print({name: "Alice", age: 30});

    results.printed_objects = true;
    return results;
}

function test_print_multiple_values() {
    results = {};

    // Print multiple values
    print("Number:", 42);
    print("Boolean:", true);
    print("String:", "hello");
    print("Array:", [1, 2, 3]);
    print("Object:", {x: 10, y: 20});

    results.printed_multiple = true;
    return results;
}

function test_print_computations() {
    results = {};

    // Print computation results
    print("2 + 2 =", 2 + 2);
    print("10 * 5 =", 10 * 5);
    print("100 / 4 =", 100 / 4);

    // Print expressions
    x = 10;
    y = 20;
    print("x + y =", x + y);

    results.printed_computations = true;
    return results;
}

function test_print_in_loops() {
    results = {};

    // Print in for loop
    for (i in range(1, 6)) {
        print("Number:", i);
    }

    // Print array elements
    fruits = ["apple", "banana", "cherry"];
    for (fruit in fruits) {
        print("Fruit:", fruit);
    }

    results.printed_in_loops = true;
    return results;
}

function test_print_conditionals() {
    results = {};

    // Print based on conditions
    x = 10;

    if (x > 0) {
        print("x is positive");
    } elif (x < 0) {
        print("x is negative");
    } else {
        print("x is zero");
    }

    // Print type information
    value = 42;
    t = typeof(value);
    print("Type of", value, "is", t);

    results.printed_conditionals = true;
    return results;
}

function test_print_formatted_output() {
    results = {};

    // Formatted output patterns
    name = "Alice";
    age = 30;
    print("Name:", name, "Age:", age);

    // Table-like output
    print("ID | Name  | Value");
    print("1  | Item1 | 100");
    print("2  | Item2 | 200");

    // Progress indicators
    for (i in range(5)) {
        print("Progress:", i + 1, "/ 5");
    }

    results.printed_formatted = true;
    return results;
}

function main() {
    all_results = {};

    // Header
    print("=== Builtin Print Function Tests ===");
    print("");

    print("Test 1: Printing numbers");
    all_results.numbers = test_print_numbers();

    print("");
    print("Test 2: Printing booleans");
    all_results.booleans = test_print_booleans();

    print("");
    print("Test 3: Printing strings");
    all_results.strings = test_print_strings();

    print("");
    print("Test 4: Printing arrays");
    all_results.arrays = test_print_arrays();

    print("");
    print("Test 5: Printing objects");
    all_results.objects = test_print_objects();

    print("");
    print("Test 6: Printing multiple values");
    all_results.multiple = test_print_multiple_values();

    print("");
    print("Test 7: Printing computations");
    all_results.computations = test_print_computations();

    print("");
    print("Test 8: Printing in loops");
    all_results.loops = test_print_in_loops();

    print("");
    print("Test 9: Printing with conditionals");
    all_results.conditionals = test_print_conditionals();

    print("");
    print("Test 10: Formatted output");
    all_results.formatted = test_print_formatted_output();

    print("");
    print("=== All Tests Complete ===");

    return all_results;
}

// Run tests
test_results = main();
