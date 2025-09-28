// Exception Handling Patterns Test
// Comprehensive test of try-except-finally constructs and error handling patterns in ML

import string;
import datetime;
import regex;
import collections;

// Utility function to safely append to arrays
function safe_append(arr, item) {
    return collections.append(arr, item);
}

// Utility function to safely convert values to strings
function to_string(value) {
    if (typeof(value) == "string") {
        return value;
    } elif (typeof(value) == "number") {
        return value + "";
    } elif (typeof(value) == "boolean") {
        return value ? "true" : "false";
    } else {
        return "[object]";
    }
}

// Basic exception handling patterns
function basic_exception_handling() {
    print("=== Basic Exception Handling Patterns ===");

    // Simple try-except block
    function safe_division(a, b) {
        try {
            if (b == 0) {
                throw {
                    message: "Division by zero error",
                    type: "MathError",
                    severity: "high"
                };
            }
            result = a / b;
            return {
                success: true,
                value: result,
                error: null
            };
        } except (error) {
            return {
                success: false,
                value: null,
                error: "Caught exception: " + to_string(error)
            };
        }
    }

    // Test safe division
    print("Testing safe division:");
    result1 = safe_division(10, 2);
    result2 = safe_division(15, 3);
    result3 = safe_division(8, 0);
    result4 = safe_division(20, 4);

    print("10 / 2: " + (result1.success ? to_string(result1.value) : result1.error));
    print("15 / 3: " + (result2.success ? to_string(result2.value) : result2.error));
    print("8 / 0: " + (result3.success ? to_string(result3.value) : result3.error));
    print("20 / 4: " + (result4.success ? to_string(result4.value) : result4.error));

    results = [];
    safe_append(results, result1);
    safe_append(results, result2);
    safe_append(results, result3);
    safe_append(results, result4);

    return results;
}

// Try-catch-finally patterns
function try_catch_finally_patterns() {
    print("");
    print("=== Try-Catch-Finally Patterns ===");

    // Resource management with finally block
    function process_file_data(filename, data) {
        resource_opened = false;
        processing_log = [];

        try {
            // Simulate opening a resource
            safe_append(processing_log, "Opening file: " + filename);

            if (string.length(filename) == 0) {
                throw {
                    message: "Invalid filename",
                    type: "ValidationError",
                    severity: "medium"
                };
            }

            resource_opened = true;
            safe_append(processing_log, "File opened successfully");

            // Simulate processing data
            if (data == null || data.length == 0) {
                throw {
                    message: "No data to process",
                    type: "DataError",
                    severity: "medium"
                };
            }

            processed_count = 0;
            i = 0;
            while (i < data.length) {
                item = data[i];

                // Simulate processing that might fail
                if (typeof(item) == "string" && string.length(item) > 0) {
                    processed_count = processed_count + 1;
                } elif (typeof(item) == "number" && item > 0) {
                    processed_count = processed_count + 1;
                } else {
                    throw {
                        message: "Invalid data item at index " + to_string(i) + ": " + to_string(item),
                        type: "DataValidationError",
                        severity: "medium",
                        index: i,
                        value: item
                    };
                }

                i = i + 1;
            }

            safe_append(processing_log, "Processed " + to_string(processed_count) + " items successfully");

            return {
                success: true,
                processed_items: processed_count,
                log: processing_log,
                error: null
            };

        } except (error) {
            safe_append(processing_log, "Error occurred: " + to_string(error));

            return {
                success: false,
                processed_items: 0,
                log: processing_log,
                error: error
            };

        } finally {
            if (resource_opened) {
                safe_append(processing_log, "Closing file resource");
            }
            safe_append(processing_log, "Cleanup completed");
        }
    }

    // Test file processing scenarios
    print("Testing file processing with various scenarios:");

    valid_data = [];
    safe_append(valid_data, "item1");
    safe_append(valid_data, "item2");
    safe_append(valid_data, 42);
    safe_append(valid_data, "item3");
    safe_append(valid_data, 17);

    invalid_data = [];
    safe_append(invalid_data, "valid");
    safe_append(invalid_data, null);
    safe_append(invalid_data, "another");

    empty_data = [];

    scenario1 = process_file_data("data.txt", valid_data);
    scenario2 = process_file_data("", valid_data);
    scenario3 = process_file_data("test.txt", invalid_data);
    scenario4 = process_file_data("empty.txt", empty_data);

    scenarios = [];
    safe_append(scenarios, scenario1);
    safe_append(scenarios, scenario2);
    safe_append(scenarios, scenario3);
    safe_append(scenarios, scenario4);

    scenario_names = [];
    safe_append(scenario_names, "Valid data");
    safe_append(scenario_names, "Empty filename");
    safe_append(scenario_names, "Invalid data");
    safe_append(scenario_names, "Empty data");

    j = 0;
    while (j < scenarios.length) {
        scenario = scenarios[j];
        name = scenario_names[j];
        print("");
        print("Scenario: " + name);
        print("  Success: " + to_string(scenario.success));
        if (scenario.error != null) {
            print("  Error: " + to_string(scenario.error));
        }
        print("  Log entries: " + to_string(scenario.log.length));
        k = 0;
        while (k < scenario.log.length) {
            print("    " + scenario.log[k]);
            k = k + 1;
        }
        j = j + 1;
    }

    return scenarios;
}

// Nested exception handling
function nested_exception_handling() {
    print("");
    print("=== Nested Exception Handling ===");

    // Helper functions for section processing
    function process_numeric_section(section) {
        try {
            if (section.data == null || section.data.length == 0) {
                throw {
                    message: "No numeric data provided",
                    type: "DataError",
                    severity: "medium"
                };
            }

            sum = 0;
            count = 0;
            l = 0;
            while (l < section.data.length) {
                item = section.data[l];
                if (typeof(item) != "number") {
                    throw {
                        message: "Non-numeric item found: " + to_string(item),
                        type: "ValidationError",
                        severity: "medium",
                        value: item
                    };
                }
                sum = sum + item;
                count = count + 1;
                l = l + 1;
            }

            average = sum / count;

            return {
                success: true,
                type: "numeric",
                sum: sum,
                count: count,
                average: average
            };

        } except (error) {
            throw {
                message: "Numeric processing error: " + to_string(error),
                type: "ProcessingError",
                severity: "high",
                originalError: error
            };
        }
    }

    function process_text_section(section) {
        try {
            if (section.data == null || section.data.length == 0) {
                throw {
                    message: "No text data provided",
                    type: "DataError",
                    severity: "medium"
                };
            }

            total_length = 0;
            word_count = 0;
            m = 0;
            while (m < section.data.length) {
                item = section.data[m];
                if (typeof(item) != "string") {
                    throw {
                        message: "Non-string item found: " + to_string(item),
                        type: "ValidationError",
                        severity: "medium",
                        value: item
                    };
                }
                total_length = total_length + string.length(item);

                // Simple word counting
                words = string.split(item, " ");
                word_count = word_count + words.length;
                m = m + 1;
            }

            return {
                success: true,
                type: "text",
                total_length: total_length,
                word_count: word_count,
                item_count: section.data.length
            };

        } except (error) {
            throw {
                message: "Text processing error: " + to_string(error),
                type: "ProcessingError",
                severity: "high",
                originalError: error
            };
        }
    }

    function process_mixed_section(section) {
        try {
            if (section.data == null || section.data.length == 0) {
                throw {
                    message: "No mixed data provided",
                    type: "DataError",
                    severity: "medium"
                };
            }

            string_count = 0;
            number_count = 0;
            other_count = 0;

            n = 0;
            while (n < section.data.length) {
                item = section.data[n];
                item_type = typeof(item);

                if (item_type == "string") {
                    string_count = string_count + 1;
                } elif (item_type == "number") {
                    number_count = number_count + 1;
                } else {
                    other_count = other_count + 1;
                }
                n = n + 1;
            }

            return {
                success: true,
                type: "mixed",
                string_count: string_count,
                number_count: number_count,
                other_count: other_count,
                total_items: section.data.length
            };

        } except (error) {
            throw {
                message: "Mixed processing error: " + to_string(error),
                type: "ProcessingError",
                severity: "high",
                originalError: error
            };
        }
    }

    // Multi-level exception handling
    function complex_data_processor(input_data) {
        main_log = [];
        processed_results = [];
        total_errors = 0;

        try {
            safe_append(main_log, "Starting complex data processing");

            if (input_data == null) {
                throw {
                    message: "Input data is null",
                    type: "ValidationError",
                    severity: "high"
                };
            }

            // Process each section of data
            i = 0;
            while (i < input_data.length) {
                section = input_data[i];
                section_result = null;

                try {
                    safe_append(main_log, "Processing section " + to_string(i));

                    if (section.type == "numeric") {
                        section_result = process_numeric_section(section);
                    } elif (section.type == "text") {
                        section_result = process_text_section(section);
                    } elif (section.type == "mixed") {
                        section_result = process_mixed_section(section);
                    } else {
                        throw {
                            message: "Unknown section type: " + to_string(section.type),
                            type: "ConfigurationError",
                            severity: "medium",
                            sectionType: section.type
                        };
                    }

                    safe_append(processed_results, section_result);
                    safe_append(main_log, "Section " + to_string(i) + " processed successfully");

                } except (section_error) {
                    safe_append(main_log, "Error in section " + to_string(i) + ": " + to_string(section_error));
                    total_errors = total_errors + 1;

                    // Add error result
                    safe_append(processed_results, {
                        success: false,
                        error: section_error,
                        section_index: i
                    });
                }

                i = i + 1;
            }

            safe_append(main_log, "Processing completed. Errors: " + to_string(total_errors));

            return {
                success: total_errors == 0,
                results: processed_results,
                error_count: total_errors,
                log: main_log,
                error: null
            };

        } except (main_error) {
            safe_append(main_log, "Main processing error: " + to_string(main_error));

            return {
                success: false,
                results: processed_results,
                error_count: total_errors + 1,
                log: main_log,
                error: main_error
            };
        }
    }

    // Test complex data processing
    test_data = [];

    numeric_section = {type: "numeric", data: []};
    safe_append(numeric_section.data, 1);
    safe_append(numeric_section.data, 2);
    safe_append(numeric_section.data, 3);
    safe_append(numeric_section.data, 4);
    safe_append(numeric_section.data, 5);
    safe_append(test_data, numeric_section);

    text_section = {type: "text", data: []};
    safe_append(text_section.data, "hello world");
    safe_append(text_section.data, "foo bar");
    safe_append(text_section.data, "test string");
    safe_append(test_data, text_section);

    mixed_section = {type: "mixed", data: []};
    safe_append(mixed_section.data, "text");
    safe_append(mixed_section.data, 42);
    safe_append(mixed_section.data, "more text");
    safe_append(mixed_section.data, 17);
    safe_append(mixed_section.data, true);
    safe_append(test_data, mixed_section);

    invalid_numeric_section = {type: "numeric", data: []};
    safe_append(invalid_numeric_section.data, 10);
    safe_append(invalid_numeric_section.data, "invalid");
    safe_append(invalid_numeric_section.data, 30);
    safe_append(test_data, invalid_numeric_section);

    unknown_section = {type: "unknown", data: []};
    safe_append(unknown_section.data, "should");
    safe_append(unknown_section.data, "fail");
    safe_append(test_data, unknown_section);

    empty_text_section = {type: "text", data: []};
    safe_append(test_data, empty_text_section);

    print("Testing complex nested exception handling:");
    result = complex_data_processor(test_data);

    print("Overall success: " + to_string(result.success));
    print("Error count: " + to_string(result.error_count));
    print("Results processed: " + to_string(result.results.length));

    print("");
    print("Processing log:");
    o = 0;
    while (o < result.log.length) {
        print("  " + result.log[o]);
        o = o + 1;
    }

    return result;
}

// Exception propagation and chaining
function exception_propagation_chaining() {
    print("");
    print("=== Exception Propagation and Chaining ===");

    function level4_function(value) {
        print("Level 4: Final processing");

        if (value < 0) {
            throw {
                message: "Value cannot be negative at level 4",
                type: "ValidationError",
                severity: "medium",
                level: 4
            };
        }

        if (value > 1000) {
            throw {
                message: "Value too large at level 4",
                type: "ValidationError",
                severity: "medium",
                level: 4
            };
        }

        result = value * value + 10;
        print("Level 4: Final result calculated: " + to_string(result));
        return result;
    }

    function level3_function(input) {
        try {
            print("Level 3: Core processing");

            if (typeof(input) != "object") {
                throw {
                    message: "Input must be object at level 3",
                    type: "ValidationError",
                    severity: "high",
                    level: 3
                };
            }

            if (input.value == null) {
                throw {
                    message: "Input.value is required at level 3",
                    type: "ValidationError",
                    severity: "high",
                    level: 3,
                    field: "value"
                };
            }

            result = level4_function(input.value);
            print("Level 3: Core processing completed");
            return {
                level3_result: result,
                processed_by: "level3"
            };
        } except (error) {
            enhanced_error = "Level 3 error: " + to_string(error);
            print("Level 3: Caught and re-throwing - " + enhanced_error);
            throw {
                message: enhanced_error,
                type: "Level3Error",
                severity: "high",
                level: 3,
                originalError: error
            };
        }
    }

    function level2_function(input) {
        try {
            print("Level 2: Validating input");
            if (input == null) {
                throw {
                    message: "Input is null at level 2",
                    type: "ValidationError",
                    severity: "high",
                    level: 2
                };
            }

            result = level3_function(input);
            print("Level 2: Validation passed");
            return result;
        } except (error) {
            enhanced_error = "Level 2 error: " + to_string(error);
            print("Level 2: Caught and re-throwing - " + enhanced_error);
            throw {
                message: enhanced_error,
                type: "Level2Error",
                severity: "high",
                level: 2,
                originalError: error
            };
        }
    }

    // Chain of function calls with exception propagation
    function level1_function(input) {
        try {
            print("Level 1: Processing input");
            result = level2_function(input);
            print("Level 1: Completed successfully");
            return result;
        } except (error) {
            enhanced_error = "Level 1 error: " + to_string(error);
            print("Level 1: Caught and re-throwing - " + enhanced_error);
            throw {
                message: enhanced_error,
                type: "Level1Error",
                severity: "high",
                level: 1,
                originalError: error
            };
        }
    }

    // Test exception propagation with various inputs
    test_inputs = [];
    safe_append(test_inputs, {value: 5});      // Should succeed
    safe_append(test_inputs, {value: -3});     // Should fail at level 4
    safe_append(test_inputs, {value: 1500});   // Should fail at level 4
    safe_append(test_inputs, {missing: 42});   // Should fail at level 3
    safe_append(test_inputs, "not_object");    // Should fail at level 3
    safe_append(test_inputs, null);            // Should fail at level 2

    input_descriptions = [];
    safe_append(input_descriptions, "Valid input (value: 5)");
    safe_append(input_descriptions, "Negative value (-3)");
    safe_append(input_descriptions, "Large value (1500)");
    safe_append(input_descriptions, "Missing value property");
    safe_append(input_descriptions, "String instead of object");
    safe_append(input_descriptions, "Null input");

    print("Testing exception propagation chain:");

    p = 0;
    while (p < test_inputs.length) {
        input = test_inputs[p];
        description = input_descriptions[p];

        print("");
        print("--- Test " + to_string(p + 1) + ": " + description + " ---");

        try {
            result = level1_function(input);
            print("SUCCESS: Final result = " + to_string(result.level3_result));
        } except (final_error) {
            print("FINAL ERROR: " + to_string(final_error));
        }

        p = p + 1;
    }

    return test_inputs;
}

// Custom exception types and error handling
function custom_exception_types() {
    print("");
    print("=== Custom Exception Types and Error Handling ===");

    // Error classification and handling
    function create_error(type, message, code, context) {
        return {
            error_type: type,
            message: message,
            error_code: code,
            context: context,
            timestamp: datetime.now()
        };
    }

    function handle_user_registration(user_data) {
        validation_errors = [];

        try {
            // Validate user data with specific error types
            if (user_data == null) {
                throw {
                    error_type: "ValidationError",
                    message: "User data is required",
                    error_code: "USER_001",
                    context: {},
                    timestamp: datetime.now()
                };
            }

            // Username validation
            if (user_data.username == null || string.length(user_data.username) == 0) {
                safe_append(validation_errors,
                    create_error("ValidationError", "Username is required", "USER_002", {field: "username"}));
            } elif (string.length(user_data.username) < 3) {
                safe_append(validation_errors,
                    create_error("ValidationError", "Username must be at least 3 characters", "USER_003", {field: "username", min_length: 3}));
            } elif (!regex.is_alphanumeric_underscore(user_data.username)) {
                safe_append(validation_errors,
                    create_error("ValidationError", "Username can only contain letters, numbers, and underscores", "USER_004", {field: "username"}));
            }

            // Email validation
            if (user_data.email == null || string.length(user_data.email) == 0) {
                safe_append(validation_errors,
                    create_error("ValidationError", "Email is required", "USER_005", {field: "email"}));
            } elif (!regex.is_email(user_data.email)) {
                safe_append(validation_errors,
                    create_error("ValidationError", "Invalid email format", "USER_006", {field: "email", value: user_data.email}));
            }

            // Password validation
            if (user_data.password == null || string.length(user_data.password) == 0) {
                safe_append(validation_errors,
                    create_error("ValidationError", "Password is required", "USER_007", {field: "password"}));
            } elif (string.length(user_data.password) < 8) {
                safe_append(validation_errors,
                    create_error("ValidationError", "Password must be at least 8 characters", "USER_008", {field: "password", min_length: 8}));
            }

            // Age validation
            if (user_data.age != null) {
                if (typeof(user_data.age) != "number") {
                    safe_append(validation_errors,
                        create_error("ValidationError", "Age must be a number", "USER_009", {field: "age", value: user_data.age}));
                } elif (user_data.age < 13) {
                    safe_append(validation_errors,
                        create_error("BusinessLogicError", "Users must be at least 13 years old", "USER_010", {field: "age", min_age: 13}));
                } elif (user_data.age > 120) {
                    safe_append(validation_errors,
                        create_error("ValidationError", "Invalid age value", "USER_011", {field: "age", max_age: 120}));
                }
            }

            // If there are validation errors, throw them
            if (validation_errors.length > 0) {
                throw {
                    error_type: "MultipleValidationErrors",
                    message: "User data validation failed",
                    error_code: "USER_100",
                    context: {errors: validation_errors},
                    timestamp: datetime.now()
                };
            }

            // Simulate business logic that might fail
            if (user_data.username == "admin" || user_data.username == "root") {
                throw {
                    error_type: "BusinessLogicError",
                    message: "Reserved username not allowed",
                    error_code: "USER_200",
                    context: {username: user_data.username},
                    timestamp: datetime.now()
                };
            }

            // Simulate external service call that might fail
            if (user_data.email == "blacklisted@example.com") {
                throw {
                    error_type: "ExternalServiceError",
                    message: "Email domain is blacklisted",
                    error_code: "USER_300",
                    context: {service: "email_validation", email: user_data.email},
                    timestamp: datetime.now()
                };
            }

            // Success case
            user_id = "USER_" + to_string(datetime.timestamp());
            return {
                success: true,
                user_id: user_id,
                username: user_data.username,
                email: user_data.email,
                created_at: datetime.now()
            };

        } except (error) {
            return {
                success: false,
                error: error,
                user_id: null
            };
        }
    }

    // Test user registration with various scenarios
    test_users = [];
    safe_append(test_users, {username: "john_doe", email: "john@example.com", password: "securepass123", age: 25});
    safe_append(test_users, {username: "x", email: "invalid-email", password: "short", age: 12});
    safe_append(test_users, {username: "admin", email: "admin@example.com", password: "adminpass123", age: 30});
    safe_append(test_users, {username: "jane_smith", email: "blacklisted@example.com", password: "password123", age: 28});
    safe_append(test_users, {email: "missing@username.com", password: "password123", age: 22});
    safe_append(test_users, null);

    user_descriptions = [];
    safe_append(user_descriptions, "Valid user data");
    safe_append(user_descriptions, "Multiple validation errors");
    safe_append(user_descriptions, "Reserved username");
    safe_append(user_descriptions, "Blacklisted email");
    safe_append(user_descriptions, "Missing username");
    safe_append(user_descriptions, "Null user data");

    print("Testing custom exception handling:");

    q = 0;
    while (q < test_users.length) {
        user = test_users[q];
        description = user_descriptions[q];

        print("");
        print("--- Registration Test " + to_string(q + 1) + ": " + description + " ---");

        result = handle_user_registration(user);

        if (result.success) {
            print("SUCCESS: User created with ID " + result.user_id);
        } else {
            error = result.error;
            print("FAILED: " + error.error_type + " - " + error.message + " (Code: " + error.error_code + ")");

            if (error.error_type == "MultipleValidationErrors") {
                print("Validation Errors:");
                r = 0;
                while (r < error.context.errors.length) {
                    val_error = error.context.errors[r];
                    print("  - " + val_error.message + " (Code: " + val_error.error_code + ")");
                    r = r + 1;
                }
            }
        }

        q = q + 1;
    }

    return test_users;
}

// Error recovery and fallback strategies
function error_recovery_fallback() {
    print("");
    print("=== Error Recovery and Fallback Strategies ===");

    // Mock service implementations
    function call_primary_service(request) {
        if (request.id == "fail_primary") {
            throw {
                message: "Primary service unavailable",
                type: "ServiceError",
                severity: "high",
                service: "primary"
            };
        }
        if (request.id == "fail_all") {
            throw {
                message: "Primary service error",
                type: "ServiceError",
                severity: "high",
                service: "primary"
            };
        }
        return {
            source: "primary",
            data: "Primary data for " + request.id,
            quality: "high"
        };
    }

    function call_secondary_service(request) {
        if (request.id == "fail_all") {
            throw {
                message: "Secondary service error",
                type: "ServiceError",
                severity: "medium",
                service: "secondary"
            };
        }
        if (request.id == "fail_secondary") {
            throw {
                message: "Secondary service unavailable",
                type: "ServiceError",
                severity: "medium",
                service: "secondary"
            };
        }
        return {
            source: "secondary",
            data: "Secondary data for " + request.id,
            quality: "medium"
        };
    }

    function get_cached_data(request) {
        if (request.id == "fail_all") {
            return null; // No cached data
        }
        if (request.id == "cached_only") {
            return {
                source: "cache",
                data: "Cached data for " + request.id,
                quality: "cached"
            };
        }
        return null;
    }

    function get_default_data(request) {
        return {
            source: "default",
            data: "Default data for " + request.id,
            quality: "low"
        };
    }

    // Service with multiple fallback strategies
    function resilient_data_service(request) {
        attempts_log = [];
        max_retries = 3;

        // Try primary service
        try {
            safe_append(attempts_log, "Attempting primary service");
            result = call_primary_service(request);
            safe_append(attempts_log, "Primary service succeeded");
            return {
                success: true,
                data: result,
                service_used: "primary",
                attempts: attempts_log
            };
        } except (primary_error) {
            safe_append(attempts_log, "Primary service failed: " + to_string(primary_error));
        }

        // Try secondary service
        try {
            safe_append(attempts_log, "Attempting secondary service");
            result = call_secondary_service(request);
            safe_append(attempts_log, "Secondary service succeeded");
            return {
                success: true,
                data: result,
                service_used: "secondary",
                attempts: attempts_log
            };
        } except (secondary_error) {
            safe_append(attempts_log, "Secondary service failed: " + to_string(secondary_error));
        }

        // Try cached data
        try {
            safe_append(attempts_log, "Attempting cached data");
            result = get_cached_data(request);
            if (result != null) {
                safe_append(attempts_log, "Cached data found");
                return {
                    success: true,
                    data: result,
                    service_used: "cache",
                    attempts: attempts_log
                };
            } else {
                safe_append(attempts_log, "No cached data available");
            }
        } except (cache_error) {
            safe_append(attempts_log, "Cache access failed: " + to_string(cache_error));
        }

        // Final fallback - default data
        safe_append(attempts_log, "Using default fallback data");
        return {
            success: true,
            data: get_default_data(request),
            service_used: "default",
            attempts: attempts_log
        };
    }

    // Test resilient service with various scenarios
    test_requests = [];
    safe_append(test_requests, {id: "normal_request"});
    safe_append(test_requests, {id: "fail_primary"});
    safe_append(test_requests, {id: "fail_secondary"});
    safe_append(test_requests, {id: "cached_only"});
    safe_append(test_requests, {id: "fail_all"});

    request_descriptions = [];
    safe_append(request_descriptions, "Normal request (should use primary)");
    safe_append(request_descriptions, "Primary fails (should use secondary)");
    safe_append(request_descriptions, "Secondary fails (should use primary)");
    safe_append(request_descriptions, "Only cached data available");
    safe_append(request_descriptions, "All services fail (should use default)");

    print("Testing resilient data service:");

    s = 0;
    while (s < test_requests.length) {
        request = test_requests[s];
        description = request_descriptions[s];

        print("");
        print("--- Request " + to_string(s + 1) + ": " + description + " ---");

        result = resilient_data_service(request);
        print("Service used: " + result.service_used);
        print("Data quality: " + result.data.quality);
        print("Attempts made:");

        t = 0;
        while (t < result.attempts.length) {
            print("  " + result.attempts[t]);
            t = t + 1;
        }

        s = s + 1;
    }

    return test_requests;
}

// Main function to run all exception handling tests
function main() {
    print("==============================================");
    print("  EXCEPTION HANDLING PATTERNS TEST");
    print("==============================================");

    results = {};

    results.basic = basic_exception_handling();
    results.try_catch_finally = try_catch_finally_patterns();
    results.nested = nested_exception_handling();
    results.propagation = exception_propagation_chaining();
    results.custom_types = custom_exception_types();
    results.recovery = error_recovery_fallback();

    print("");
    print("==============================================");
    print("  ALL EXCEPTION HANDLING TESTS COMPLETED");
    print("==============================================");

    return results;
}

// Execute comprehensive exception handling test
main();