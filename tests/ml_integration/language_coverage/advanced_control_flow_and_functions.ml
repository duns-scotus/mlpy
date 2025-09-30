// Advanced Control Flow and Functions Test
// Demonstrates all control flow constructs and function patterns in ML

import string;
import collections;
import math;

// Basic control flow structures
function basic_control_flow() {
    print("=== Basic Control Flow Structures ===");

    // Simple if statement
    age = 25;
    if (age >= 18) {
        print("You are an adult");
    }

    // If-else statement
    temperature = 72;
    if (temperature > 80) {
        print("It's hot outside");
    } else {
        print("It's comfortable outside");
    }

    // If-elif-else chain
    score = 85;
    if (score >= 90) {
        grade = "A";
    } elif (score >= 80) {
        grade = "B";
    } elif (score >= 70) {
        grade = "C";
    } elif (score >= 60) {
        grade = "D";
    } else {
        grade = "F";
    }
    print("Grade for score " + string.toString(score) + ": " + grade);

    // Nested if statements
    weather = "sunny";
    temperature = 75;

    if (weather == "sunny") {
        if (temperature > 70) {
            activity = "go to the beach";
        } else {
            activity = "take a walk";
        }
    } else {
        if (temperature > 60) {
            activity = "stay inside and read";
        } else {
            activity = "stay warm inside";
        }
    }
    print("Weather: " + weather + ", Temperature: " + string.toString(temperature) + " -> " + activity);

    return {
        age_check: age >= 18,
        temperature_check: temperature,
        grade: grade,
        activity: activity
    };
}

// Loop constructs and patterns
function loop_constructs_patterns() {
    print("\n=== Loop Constructs and Patterns ===");

    // While loop with counter
    print("While loop counting to 5:");
    count = 1;
    while (count <= 5) {
        print("Count: " + string.toString(count));
        count = count + 1;
    }

    // While loop with array processing
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    sum = 0;
    i = 0;
    while (i < collections.length(numbers)) {
        sum = sum + numbers[i];
        i = i + 1;
    }
    print("Sum of numbers 1-10: " + string.toString(sum));

    // For-in loop with arrays
    print("\nFor-in loop with fruits:");
    fruits = ["apple", "banana", "cherry", "date"];
    for (fruit in fruits) {
        print("Fruit: " + fruit);
    }

    // For-in loop with string processing
    print("\nFor-in loop processing characters:");
    chars = string.to_chars("Hello");
    word = "";
    for (char in chars) {
        word = word + string.upper(char);
    }
    print("Uppercase word: " + word);

    // Nested loops - multiplication table
    print("\nNested loops - 3x3 multiplication table:");
    i = 1;
    while (i <= 3) {
        row = "";
        j = 1;
        while (j <= 3) {
            product = i * j;
            row = row + string.toString(product) + " ";
            j = j + 1;
        }
        print("Row " + string.toString(i) + ": " + row);
        i = i + 1;
    }

    // Loop with break and continue simulation
    print("\nLoop with conditional processing:");
    test_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    even_sum = 0;
    odd_count = 0;

    k = 0;
    while (k < collections.length(test_numbers)) {
        number = test_numbers[k];

        if (number % 2 == 0) {
            even_sum = even_sum + number;
            print("Even number found: " + string.toString(number));
        } else {
            odd_count = odd_count + 1;
            print("Odd number found: " + string.toString(number));
        }

        k = k + 1;
    }

    print("Even sum: " + string.toString(even_sum));
    print("Odd count: " + string.toString(odd_count));

    return {
        sum_1_to_10: sum,
        even_sum: even_sum,
        odd_count: odd_count,
        uppercase_word: word
    };
}

// Function definition patterns
function function_definition_patterns() {
    print("\n=== Function Definition Patterns ===");

    // Simple function with parameters
    function greet(name, greeting) {
        return greeting + ", " + name + "!";
    }

    message1 = greet("Alice", "Hello");
    message2 = greet("Bob", "Good morning");
    print("Greeting 1: " + message1);
    print("Greeting 2: " + message2);

    // Function with default behavior
    function calculate_area(length, width) {
        if (width == 0) {
            // Square
            return length * length;
        } else {
            // Rectangle
            return length * width;
        }
    }

    square_area = calculate_area(5, 0);
    rectangle_area = calculate_area(4, 6);
    print("Square area (5x5): " + string.toString(square_area));
    print("Rectangle area (4x6): " + string.toString(rectangle_area));

    // Function with multiple return points
    function classify_number(n) {
        if (n < 0) {
            return "negative";
        }
        if (n == 0) {
            return "zero";
        }
        if (n > 0 && n <= 100) {
            return "small positive";
        }
        return "large positive";
    }

    class1 = classify_number(-5);
    class2 = classify_number(0);
    class3 = classify_number(50);
    class4 = classify_number(200);

    print("Number classifications:");
    print("-5: " + class1);
    print("0: " + class2);
    print("50: " + class3);
    print("200: " + class4);

    // Function with complex logic
    function find_prime_factors(n) {
        factors = [];
        divisor = 2;

        while (divisor * divisor <= n) {
            while (n % divisor == 0) {
                factors = collections.append(factors, divisor);
                n = n / divisor;
            }
            divisor = divisor + 1;
        }

        if (n > 1) {
            factors = collections.append(factors, n);
        }

        return factors;
    }

    factors_12 = find_prime_factors(12);
    factors_17 = find_prime_factors(17);
    factors_24 = find_prime_factors(24);

    print("\nPrime factorization:");
    print("12: " + factors_12);
    print("17: " + factors_17);
    print("24: " + factors_24);

    return {
        greetings: [message1, message2],
        areas: {
            square: square_area,
            rectangle: rectangle_area
        },
        classifications: [class1, class2, class3, class4],
        prime_factors: {
            twelve: factors_12,
            seventeen: factors_17,
            twenty_four: factors_24
        }
    };
}

// Higher-order functions and function expressions
function higher_order_functions() {
    print("\n=== Higher-Order Functions and Function Expressions ===");

    // Function expressions
    add = fn(a, b) => a + b;

    multiply = fn(a, b) => a * b;

    subtract = fn(a, b) => a - b;

    divide = fn(a, b) => (b != 0) ? (a / b) : 0;

    // Function that takes function as parameter
    function apply_binary_operation(x, y, operation) {
        return operation(x, y);
    }

    result1 = apply_binary_operation(10, 5, add);
    result2 = apply_binary_operation(10, 5, multiply);
    result3 = apply_binary_operation(10, 5, subtract);
    result4 = apply_binary_operation(10, 5, divide);

    print("Binary operations on 10 and 5:");
    print("Add: " + string.toString(result1));
    print("Multiply: " + string.toString(result2));
    print("Subtract: " + string.toString(result3));
    print("Divide: " + string.toString(result4));

    // Function factory pattern
    function create_multiplier(factor) {
        return fn(x) => x * factor;
    }

    double = create_multiplier(2);
    triple = create_multiplier(3);
    times_ten = create_multiplier(10);

    doubled = double(7);
    tripled = triple(4);
    times_ten_result = times_ten(6);

    print("\nFunction factory results:");
    print("Double 7: " + doubled);
    print("Triple 4: " + tripled);
    print("Times 10 of 6: " + times_ten_result);

    // Array processing with function parameters
    function transform_array(arr, transformer) {
        result = [];
        i = 0;
        while (i < collections.length(arr)) {
            element = arr[i];
            transformed = transformer(element);
            result = collections.append(result, transformed);
            i = i + 1;
        }
        return result;
    }

    function square(x) {
        return x * x;
    }

    function cube(x) {
        return x * x * x;
    }

    numbers = [1, 2, 3, 4, 5];
    squared_numbers = transform_array(numbers, square);
    cubed_numbers = transform_array(numbers, cube);
    doubled_numbers = transform_array(numbers, double);

    print("\nArray transformations:");
    print("Original: " + numbers);
    print("Squared: " + squared_numbers);
    print("Cubed: " + cubed_numbers);
    print("Doubled: " + doubled_numbers);

    // Function composition
    function compose_functions(f, g) {
        return fn(x) => f(g(x));
    }

    function add_one(x) {
        return x + 1;
    }

    function multiply_by_two(x) {
        return x * 2;
    }

    // Compose: add_one(multiply_by_two(x))
    composed = compose_functions(add_one, multiply_by_two);
    composition_result = composed(5); // (5 * 2) + 1 = 11

    print("\nFunction composition:");
    print("Composed function on 5: " + composition_result);

    return {
        binary_ops: [result1, result2, result3, result4],
        factory_results: [doubled, tripled, times_ten_result],
        transformations: {
            squared: squared_numbers,
            cubed: cubed_numbers,
            doubled: doubled_numbers
        },
        composition_result: composition_result
    };
}

// Recursive functions and algorithms
function recursive_functions_algorithms() {
    print("\n=== Recursive Functions and Algorithms ===");

    // Simple recursion - factorial
    function factorial(n) {
        if (n <= 1) {
            return 1;
        } else {
            return n * factorial(n - 1);
        }
    }

    fact_5 = factorial(5);
    fact_7 = factorial(7);
    fact_0 = factorial(0);

    print("Factorial calculations:");
    print("5! = " + fact_5);
    print("7! = " + fact_7);
    print("0! = " + fact_0);

    // Fibonacci sequence
    function fibonacci(n) {
        if (n <= 1) {
            return n;
        } else {
            return fibonacci(n - 1) + fibonacci(n - 2);
        }
    }

    fib_sequence = [];
    i = 0;
    while (i < 10) {
        fib_value = fibonacci(i);
        fib_sequence = collections.append(fib_sequence, fib_value);
        i = i + 1;
    }

    print("Fibonacci sequence (first 10): " + fib_sequence);

    // Recursive array sum
    function recursive_sum(arr, index) {
        if (index >= collections.length(arr)) {
            return 0;
        } else {
            return arr[index] + recursive_sum(arr, index + 1);
        }
    }

    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    recursive_total = recursive_sum(numbers, 0);
    print("Recursive sum of 1-10: " + recursive_total);

    // Recursive string reversal
    function reverse_string_recursive(str, index) {
        if (index >= string.length(str)) {
            return "";
        } else {
            char = string.char_at(str, index);
            return reverse_string_recursive(str, index + 1) + char;
        }
    }

    original_string = "Hello World";
    reversed_string = reverse_string_recursive(original_string, 0);
    print("String reversal:");
    print("Original: " + original_string);
    print("Reversed: " + reversed_string);

    // Recursive tree traversal simulation
    function count_nodes(node) {
        if (node == null) {
            return 0;
        }

        left_count = 0;
        right_count = 0;

        if (node.left != null) {
            left_count = count_nodes(node.left);
        }

        if (node.right != null) {
            right_count = count_nodes(node.right);
        }

        return 1 + left_count + right_count;
    }

    // Create a simple binary tree
    tree = {
        value: 1,
        left: {
            value: 2,
            left: {
                value: 4,
                left: null,
                right: null
            },
            right: {
                value: 5,
                left: null,
                right: null
            }
        },
        right: {
            value: 3,
            left: null,
            right: {
                value: 6,
                left: null,
                right: null
            }
        }
    };

    node_count = count_nodes(tree);
    print("Binary tree node count: " + node_count);

    return {
        factorials: [fact_5, fact_7, fact_0],
        fibonacci: fib_sequence,
        recursive_sum: recursive_total,
        string_reversal: {
            original: original_string,
            reversed: reversed_string
        },
        tree_node_count: node_count
    };
}

// Exception handling and error management
function exception_handling_error_management() {
    print("\n=== Exception Handling and Error Management ===");

    // Try-catch pattern simulation with return values
    function safe_divide(a, b) {
        try {
            if (b == 0) {
                // Simulate throwing an exception
                return {
                    success: false,
                    error: "Division by zero",
                    value: null
                };
            }

            result = a / b;
            return {
                success: true,
                error: null,
                value: result
            };
        } except (error) {
            return {
                success: false,
                error: "Unknown error occurred",
                value: null
            };
        }
    }

    // Test safe division
    result1 = safe_divide(10, 2);
    result2 = safe_divide(10, 0);
    result3 = safe_divide(15, 3);

    print("Safe division results:");
    print("10 / 2: " + result1);
    print("10 / 0: " + result2);
    print("15 / 3: " + result3);

    // Error handling with validation
    function validate_and_process(input) {
        errors = [];

        try {
            // Validate input
            if (input.name == "" || input.name == null) {
                errors = collections.append(errors, "Name is required");
            }

            if (input.age < 0 || input.age > 150) {
                errors = collections.append(errors, "Age must be between 0 and 150");
            }

            if (collections.length(errors) > 0) {
                return {
                    success: false,
                    errors: errors,
                    data: null
                };
            }

            // Process valid input
            processed_data = {
                name: string.upper(input.name),
                age: input.age,
                age_group: input.age < 18 ? "minor" : "adult",
                valid: true
            };

            return {
                success: true,
                errors: [],
                data: processed_data
            };

        } except (error) {
            return {
                success: false,
                errors: ["Processing error occurred"],
                data: null
            };
        } finally {
            print("Validation attempt completed");
        }
    }

    valid_input = {
        name: "John Doe",
        age: 30
    };

    invalid_input = {
        name: "",
        age: -5
    };

    validation1 = validate_and_process(valid_input);
    validation2 = validate_and_process(invalid_input);

    print("Validation results:");
    print("Valid input result: " + validation1);
    print("Invalid input result: " + validation2);

    // Chain of operations with error handling
    function chain_operations(start_value) {
        function step1(value) {
            if (value < 0) {
                return {success: false, error: "Value cannot be negative", value: null};
            }
            return {success: true, error: null, value: value * 2};
        }

        function step2(value) {
            if (value > 100) {
                return {success: false, error: "Value too large", value: null};
            }
            return {success: true, error: null, value: value + 10};
        }

        function step3(value) {
            if (value % 2 != 0) {
                return {success: false, error: "Value must be even", value: null};
            }
            return {success: true, error: null, value: value / 2};
        }

        result1 = step1(start_value);
        if (!result1.success) {
            return result1;
        }

        result2 = step2(result1.value);
        if (!result2.success) {
            return result2;
        }

        result3 = step3(result2.value);
        return result3;
    }

    chain_result1 = chain_operations(5);  // Should succeed
    chain_result2 = chain_operations(50); // Should fail at step2
    chain_result3 = chain_operations(-1); // Should fail at step1

    print("\nChained operations:");
    print("Chain with 5: " + chain_result1);
    print("Chain with 50: " + chain_result2);
    print("Chain with -1: " + chain_result3);

    return {
        division_results: [result1, result2, result3],
        validation_results: [validation1, validation2],
        chain_results: [chain_result1, chain_result2, chain_result3]
    };
}

// Advanced algorithm implementations
function advanced_algorithm_implementations() {
    print("\n=== Advanced Algorithm Implementations ===");

    // Quick sort algorithm
    function quick_sort(arr) {
        if (collections.length(arr) <= 1) {
            return arr;
        }

        pivot = arr[0];
        less = [];
        equal = [];
        greater = [];

        i = 0;
        while (i < collections.length(arr)) {
            element = arr[i];
            if (element < pivot) {
                less = collections.append(less, element);
            } elif (element == pivot) {
                equal = collections.append(equal, element);
            } else {
                greater = collections.append(greater, element);
            }
            i = i + 1;
        }

        sorted_less = quick_sort(less);
        sorted_greater = quick_sort(greater);

        // Concatenate results
        result = sorted_less;
        j = 0;
        while (j < collections.length(equal)) {
            result = collections.append(result, equal[j]);
            j = j + 1;
        }
        k = 0;
        while (k < collections.length(sorted_greater)) {
            result = collections.append(result, sorted_greater[k]);
            k = k + 1;
        }

        return result;
    }

    unsorted = [64, 34, 25, 12, 22, 11, 90, 5];
    sorted_array = quick_sort(unsorted);

    print("Quick sort result:");
    print("Unsorted: " + unsorted);
    print("Sorted: " + sorted_array);

    // Greatest Common Divisor (Euclidean algorithm)
    function gcd(a, b) {
        while (b != 0) {
            temp = b;
            b = a % b;
            a = temp;
        }
        return a;
    }

    gcd_result1 = gcd(48, 18);
    gcd_result2 = gcd(17, 13);
    gcd_result3 = gcd(100, 25);

    print("\nGCD calculations:");
    print("GCD(48, 18) = " + gcd_result1);
    print("GCD(17, 13) = " + gcd_result2);
    print("GCD(100, 25) = " + gcd_result3);

    // Prime number generation (Sieve of Eratosthenes)
    function sieve_of_eratosthenes(limit) {
        is_prime = [];
        primes = [];

        // Initialize all numbers as potentially prime
        i = 0;
        while (i <= limit) {
            is_prime = collections.append(is_prime, true);
            i = i + 1;
        }

        is_prime[0] = false; // 0 is not prime
        is_prime[1] = false; // 1 is not prime

        p = 2;
        while (p * p <= limit) {
            if (is_prime[p]) {
                // Mark multiples of p as not prime
                multiple = p * p;
                while (multiple <= limit) {
                    is_prime[multiple] = false;
                    multiple = multiple + p;
                }
            }
            p = p + 1;
        }

        // Collect prime numbers
        i = 2;
        while (i <= limit) {
            if (is_prime[i]) {
                primes = collections.append(primes, i);
            }
            i = i + 1;
        }

        return primes;
    }

    primes_30 = sieve_of_eratosthenes(30);
    print("Prime numbers up to 30: " + primes_30);

    // Binary search tree operations
    function create_bst_node(value) {
        return {
            value: value,
            left: null,
            right: null
        };
    }

    function insert_bst(root, value) {
        if (root == null) {
            return create_bst_node(value);
        }

        if (value < root.value) {
            root.left = insert_bst(root.left, value);
        } elif (value > root.value) {
            root.right = insert_bst(root.right, value);
        }

        return root;
    }

    function search_bst(root, value) {
        if (root == null || root.value == value) {
            return root;
        }

        if (value < root.value) {
            return search_bst(root.left, value);
        } else {
            return search_bst(root.right, value);
        }
    }

    function inorder_traversal(root, result) {
        if (root != null) {
            inorder_traversal(root.left, result);
            result = collections.append(result, root.value);
            inorder_traversal(root.right, result);
        }
        return result;
    }

    // Build BST
    bst_root = null;
    bst_values = [50, 30, 70, 20, 40, 60, 80];

    i = 0;
    while (i < collections.length(bst_values)) {
        bst_root = insert_bst(bst_root, bst_values[i]);
        i = i + 1;
    }

    // Search for values
    search_found = search_bst(bst_root, 40);
    search_missing = search_bst(bst_root, 90);

    // Get sorted order
    traversal_result = inorder_traversal(bst_root, []);

    print("\nBinary Search Tree:");
    print("Inserted values: " + bst_values);
    print("Search for 40: " + (search_found != null ? "found" : "not found"));
    print("Search for 90: " + (search_missing != null ? "found" : "not found"));
    print("Inorder traversal: " + traversal_result);

    return {
        sorting: {
            unsorted: unsorted,
            sorted: sorted_array
        },
        gcd_results: [gcd_result1, gcd_result2, gcd_result3],
        primes: primes_30,
        bst: {
            inserted: bst_values,
            traversal: traversal_result,
            search_results: {
                found_40: search_found != null,
                found_90: search_missing != null
            }
        }
    };
}

// Main test runner
function main() {
    print("==============================================");
    print("  ADVANCED CONTROL FLOW AND FUNCTIONS TEST");
    print("==============================================");

    results = {};

    results.basic_control = basic_control_flow();
    results.loops = loop_constructs_patterns();
    results.functions = function_definition_patterns();
    results.higher_order = higher_order_functions();
    results.recursion = recursive_functions_algorithms();
    results.exceptions = exception_handling_error_management();
    results.algorithms = advanced_algorithm_implementations();

    print("\n==============================================");
    print("  ALL CONTROL FLOW AND FUNCTION TESTS COMPLETED");
    print("==============================================");

    return results;
}

// Execute all tests
main();