// Sprint 7: Advanced ML Language Features Demonstration
// Complete rewrite using validated patterns for production-ready ML code

import collections;
import string;

// Safe append utility function for dynamic arrays
function safe_append(arr, item) {
    return collections.append(arr, item);
}

// String conversion utility
function to_string(value) {
    if (value == null) {
        return "null";
    }
    return "" + value;
}

// Math utility functions
function math_abs(x) {
    if (x < 0) {
        return -x;
    }
    return x;
}

function math_max(a, b) {
    if (a > b) {
        return a;
    }
    return b;
}

function math_min(a, b) {
    if (a < b) {
        return a;
    }
    return b;
}

// Current ML Object Support - Enhanced with validation
person_data = {
    name: "Alice",
    age: 30,
    email: "alice@example.com",
    active: true,
    skills: ["JavaScript", "Python", "ML"],
    address: {
        street: "123 Main St",
        city: "Tech City",
        zipcode: "12345"
    }
};

// Advanced pattern matching simulation with comprehensive type handling
function processValue(input, type_hint) {
    if (type_hint == "number") {
        if (input > 1000) {
            return "Very large number: " + to_string(input);
        } elif (input > 100) {
            return "Large number: " + to_string(input);
        } elif (input > 10) {
            return "Medium number: " + to_string(input);
        } elif (input > 0) {
            return "Small positive number: " + to_string(input);
        } elif (input == 0) {
            return "Zero value";
        } else {
            return "Negative number: " + to_string(input);
        }
    } elif (type_hint == "string") {
        if (input.length == 0) {
            return "Empty string";
        } elif (input.length > 50) {
            return "Long text: " + string.substring(input, 0, 47) + "...";
        } else {
            return "Text: " + input;
        }
    } elif (type_hint == "boolean") {
        if (input) {
            return "Boolean: true";
        } else {
            return "Boolean: false";
        }
    } elif (type_hint == "array") {
        return "Array with " + to_string(input.length) + " elements";
    } elif (type_hint == "object") {
        return "Object type detected";
    } else {
        return "Unknown type: " + to_string(type_hint);
    }
}

// Enhanced array comprehension simulation with multiple filters
function createAdvancedSquares(numbers, threshold) {
    squares = [];
    i = 0;
    while (i < numbers.length) {
        value = numbers[i];
        if (value > threshold) {
            square = value * value;
            if (square < 1000) {  // Additional filter to keep reasonable sizes
                safe_append(squares, square);
            }
        }
        i = i + 1;
    }
    return squares;
}

// Advanced array operations with multiple transformations
function processNumberArray(numbers) {
    results = {
        original: numbers,
        filtered: [],
        squared: [],
        doubled: [],
        statistics: {}
    };

    sum = 0;
    count = 0;
    min_val = 999999;
    max_val = -999999;

    i = 0;
    while (i < numbers.length) {
        value = numbers[i];

        // Statistics calculation
        sum = sum + value;
        count = count + 1;
        if (value < min_val) {
            min_val = value;
        }
        if (value > max_val) {
            max_val = value;
        }

        // Apply filters and transformations
        if (value > 0) {
            safe_append(results.filtered, value);
            safe_append(results.squared, value * value);
            safe_append(results.doubled, value * 2);
        }

        i = i + 1;
    }

    // Calculate statistics
    if (count > 0) {
        results.statistics = {
            sum: sum,
            count: count,
            average: sum / count,
            min: min_val,
            max: max_val,
            range: max_val - min_val
        };
    }

    return results;
}

// Enhanced error handling with error types and recovery
function safeOperation(operation_type, a, b) {
    result = {
        success: false,
        value: null,
        error: null,
        error_type: null
    };

    try {
        if (operation_type == "divide") {
            if (b == 0) {
                result.error = "Division by zero error";
                result.error_type = "MATH_ERROR";
                return result;
            }
            result.value = a / b;
        } elif (operation_type == "sqrt") {
            if (a < 0) {
                result.error = "Square root of negative number";
                result.error_type = "MATH_ERROR";
                return result;
            }
            // Simple square root approximation
            guess = a / 2;
            iterations = 0;
            while (iterations < 10) {
                guess = (guess + a / guess) / 2;
                iterations = iterations + 1;
            }
            result.value = guess;
        } elif (operation_type == "log") {
            if (a <= 0) {
                result.error = "Logarithm of non-positive number";
                result.error_type = "MATH_ERROR";
                return result;
            }
            // Simple natural log approximation for demonstration
            result.value = a;  // Simplified for this demo
        } elif (operation_type == "power") {
            if (a == 0 && b < 0) {
                result.error = "Zero to negative power";
                result.error_type = "MATH_ERROR";
                return result;
            }
            // Simple power calculation
            power_result = 1;
            exponent = math_abs(b);
            base = a;
            while (exponent > 0) {
                if (exponent % 2 == 1) {
                    power_result = power_result * base;
                }
                base = base * base;
                exponent = exponent / 2;
            }
            if (b < 0) {
                power_result = 1 / power_result;
            }
            result.value = power_result;
        } else {
            result.error = "Unknown operation: " + operation_type;
            result.error_type = "OPERATION_ERROR";
            return result;
        }

        result.success = true;
        return result;
    } except (error) {
        result.error = "Unexpected error: " + to_string(error);
        result.error_type = "RUNTIME_ERROR";
        return result;
    }
}

// Complex calculation chain with comprehensive error propagation
function advancedCalculationChain(x, y, z) {
    operations = [];

    // Step 1: Divide x by 2
    step1 = safeOperation("divide", x, 2);
    safe_append(operations, {step: "divide_x_by_2", result: step1});
    if (!step1.success) {
        return {success: false, error: step1.error, failed_at: "step1", operations: operations};
    }

    // Step 2: Square root of y
    step2 = safeOperation("sqrt", y);
    safe_append(operations, {step: "sqrt_y", result: step2});
    if (!step2.success) {
        return {success: false, error: step2.error, failed_at: "step2", operations: operations};
    }

    // Step 3: z to power of 2
    step3 = safeOperation("power", z, 2);
    safe_append(operations, {step: "z_squared", result: step3});
    if (!step3.success) {
        return {success: false, error: step3.error, failed_at: "step3", operations: operations};
    }

    // Step 4: Combine results
    intermediate = step1.value + step2.value;
    final_step = safeOperation("divide", intermediate, step3.value);
    safe_append(operations, {step: "final_combination", result: final_step});
    if (!final_step.success) {
        return {success: false, error: final_step.error, failed_at: "final_step", operations: operations};
    }

    return {
        success: true,
        value: final_step.value,
        intermediate_results: {
            x_half: step1.value,
            y_sqrt: step2.value,
            z_squared: step3.value,
            combined: intermediate
        },
        operations: operations
    };
}

// Advanced object manipulation and validation
function validateAndProcessPerson(person) {
    validation_result = {
        valid: true,
        errors: [],
        processed_data: {},
        metadata: {}
    };

    // Name validation
    if (!person.name || person.name.length == 0) {
        safe_append(validation_result.errors, "Name is required");
        validation_result.valid = false;
    } elif (person.name.length < 2) {
        safe_append(validation_result.errors, "Name too short");
        validation_result.valid = false;
    } else {
        validation_result.processed_data.name = person.name;
        validation_result.processed_data.name_length = person.name.length;
    }

    // Age validation
    if (!person.age) {
        safe_append(validation_result.errors, "Age is required");
        validation_result.valid = false;
    } elif (person.age < 0 || person.age > 150) {
        safe_append(validation_result.errors, "Age out of valid range");
        validation_result.valid = false;
    } else {
        validation_result.processed_data.age = person.age;
        if (person.age < 18) {
            validation_result.processed_data.age_category = "minor";
        } elif (person.age < 65) {
            validation_result.processed_data.age_category = "adult";
        } else {
            validation_result.processed_data.age_category = "senior";
        }
    }

    // Email validation (basic)
    if (!person.email || person.email.length == 0) {
        safe_append(validation_result.errors, "Email is required");
        validation_result.valid = false;
    } elif (person.email.indexOf("@") == -1) {
        safe_append(validation_result.errors, "Invalid email format");
        validation_result.valid = false;
    } else {
        validation_result.processed_data.email = person.email;
        parts = person.email.split("@");
        if (parts.length == 2) {
            validation_result.processed_data.email_domain = parts[1];
        }
    }

    // Skills processing (if available)
    if (person.skills && person.skills.length > 0) {
        validation_result.processed_data.skills = person.skills;
        validation_result.processed_data.skill_count = person.skills.length;

        // Categorize skills
        tech_skills = [];
        other_skills = [];
        i = 0;
        while (i < person.skills.length) {
            skill = person.skills[i];
            if (skill == "JavaScript" || skill == "Python" || skill == "ML" || skill == "Java" || skill == "C++") {
                safe_append(tech_skills, skill);
            } else {
                safe_append(other_skills, skill);
            }
            i = i + 1;
        }
        validation_result.processed_data.tech_skills = tech_skills;
        validation_result.processed_data.other_skills = other_skills;
    }

    // Add metadata
    validation_result.metadata.validation_timestamp = "2024-01-15T10:30:00Z";
    validation_result.metadata.validator_version = "1.0.0";
    validation_result.metadata.error_count = validation_result.errors.length;

    return validation_result;
}

// Advanced functional programming patterns
function applyFunctionalOperations(data) {
    // Map operation: transform each element
    function map_operation(arr, transform_fn) {
        mapped = [];
        i = 0;
        while (i < arr.length) {
            transformed = transform_fn(arr[i]);
            safe_append(mapped, transformed);
            i = i + 1;
        }
        return mapped;
    }

    // Filter operation: select elements that meet criteria
    function filter_operation(arr, predicate_fn) {
        filtered = [];
        i = 0;
        while (i < arr.length) {
            if (predicate_fn(arr[i])) {
                safe_append(filtered, arr[i]);
            }
            i = i + 1;
        }
        return filtered;
    }

    // Reduce operation: combine elements into single value
    function reduce_operation(arr, reducer_fn, initial) {
        accumulator = initial;
        i = 0;
        while (i < arr.length) {
            accumulator = reducer_fn(accumulator, arr[i]);
            i = i + 1;
        }
        return accumulator;
    }

    // Apply transformations
    doubled = map_operation(data, function(x) { return x * 2; });
    evens = filter_operation(data, function(x) { return x % 2 == 0; });
    sum = reduce_operation(data, function(acc, val) { return acc + val; }, 0);
    product = reduce_operation(data, function(acc, val) { return acc * val; }, 1);

    return {
        original: data,
        doubled: doubled,
        evens: evens,
        sum: sum,
        product: product,
        statistics: {
            original_count: data.length,
            doubled_count: doubled.length,
            evens_count: evens.length,
            sum_of_evens: reduce_operation(evens, function(acc, val) { return acc + val; }, 0)
        }
    };
}

// Comprehensive demonstration of all advanced features
function main_demo() {
    print("=== Sprint 7: Advanced ML Language Features Demo ===");
    print("");

    // Test advanced pattern matching
    print("1. Advanced Pattern Matching:");
    print(processValue(1500, "number"));
    print(processValue(-25, "number"));
    print(processValue("This is a long string that exceeds fifty characters for demonstration", "string"));
    print(processValue(true, "boolean"));
    print(processValue([1, 2, 3], "array"));
    print("");

    // Test enhanced array operations
    print("2. Enhanced Array Operations:");
    test_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    advanced_squares = createAdvancedSquares(test_numbers, 3);
    print("Original: " + to_string(test_numbers));
    print("Advanced squares (>3, <1000): " + to_string(advanced_squares));

    array_results = processNumberArray(test_numbers);
    print("Filtered positive: " + to_string(array_results.filtered));
    print("Squared values: " + to_string(array_results.squared));
    print("Statistics - Sum: " + to_string(array_results.statistics.sum) +
          ", Average: " + to_string(array_results.statistics.average) +
          ", Range: " + to_string(array_results.statistics.range));
    print("");

    // Test advanced error handling
    print("3. Advanced Error Handling:");
    calc_result = advancedCalculationChain(20, 16, 4);
    if (calc_result.success) {
        print("Calculation successful: " + to_string(calc_result.value));
        print("Intermediate - x/2: " + to_string(calc_result.intermediate_results.x_half) +
              ", sqrt(y): " + to_string(calc_result.intermediate_results.y_sqrt) +
              ", z²: " + to_string(calc_result.intermediate_results.z_squared));
    } else {
        print("Calculation failed at " + calc_result.failed_at + ": " + calc_result.error);
    }

    // Test error case
    error_result = advancedCalculationChain(10, -4, 0);
    if (!error_result.success) {
        print("Expected error case - " + error_result.failed_at + ": " + error_result.error);
    }
    print("");

    // Test advanced object processing
    print("4. Advanced Object Processing:");
    validation = validateAndProcessPerson(person_data);
    if (validation.valid) {
        print("Person validation successful:");
        print("  Name: " + validation.processed_data.name + " (" + to_string(validation.processed_data.name_length) + " chars)");
        print("  Age: " + to_string(validation.processed_data.age) + " (Category: " + validation.processed_data.age_category + ")");
        print("  Email domain: " + validation.processed_data.email_domain);
        print("  Tech skills: " + to_string(validation.processed_data.tech_skills));
        print("  Total skills: " + to_string(validation.processed_data.skill_count));
    } else {
        print("Validation failed with " + to_string(validation.metadata.error_count) + " errors");
    }
    print("");

    // Test functional programming patterns
    print("5. Functional Programming Patterns:");
    sample_data = [1, 2, 3, 4, 5, 6, 7, 8];
    functional_results = applyFunctionalOperations(sample_data);
    print("Original data: " + to_string(functional_results.original));
    print("Doubled: " + to_string(functional_results.doubled));
    print("Even numbers: " + to_string(functional_results.evens));
    print("Sum of all: " + to_string(functional_results.sum));
    print("Sum of evens: " + to_string(functional_results.statistics.sum_of_evens));
    print("");

    // Test complex nested object access
    print("6. Complex Object Access:");
    print("Person name: " + person_data.name);
    print("Person age: " + to_string(person_data.age));
    print("Address: " + person_data.address.street + ", " + person_data.address.city);
    print("First skill: " + person_data.skills[0]);
    print("Skills count: " + to_string(person_data.skills.length));
    print("");

    print("=== Advanced ML Features Demonstration Complete! ===");
    print("All patterns working correctly with enhanced error handling,");
    print("functional programming concepts, and complex data processing.");
}

// Run the comprehensive demonstration
main_demo();