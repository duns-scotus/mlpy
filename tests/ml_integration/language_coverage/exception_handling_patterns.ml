// Exception Handling Patterns Test
// Comprehensive test of try-except-finally constructs and error handling patterns in ML

import string;
import datetime;
import regex;

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
                error: "Caught exception: " + error
            };
        }
    }

    // Test safe division
    print("Testing safe division:");
    result1 = safe_division(10, 2);
    result2 = safe_division(15, 3);
    result3 = safe_division(8, 0);
    result4 = safe_division(20, 4);

    print("10 / 2: " + (result1.success ? result1.value : result1.error));
    print("15 / 3: " + (result2.success ? result2.value : result2.error));
    print("8 / 0: " + (result3.success ? result3.value : result3.error));
    print("20 / 4: " + (result4.success ? result4.value : result4.error));

    return [result1, result2, result3, result4];
}

// Try-catch-finally patterns
function try_catch_finally_patterns() {
    print("\n=== Try-Catch-Finally Patterns ===");

    // Resource management with finally block
    function process_file_data(filename, data) {
        resource_opened = false;
        processing_log = [];

        try {
            // Simulate opening a resource
            processing_log[processing_log.length()] = "Opening file: " + filename;

            if (string.length(filename) == 0) {
                throw {
                    message: "Invalid filename",
                    type: "ValidationError",
                    severity: "medium"
                };
            }

            resource_opened = true;
            processing_log[processing_log.length()] = "File opened successfully";

            // Simulate processing data
            if (data == null || data.length() == 0) {
                throw {
                    message: "No data to process",
                    type: "DataError",
                    severity: "medium"
                };
            }

            processed_count = 0;
            i = 0;
            while (i < data.length()) {
                item = data[i];

                // Simulate processing that might fail
                if (typeof(item) == "string" && string.length(item) > 0) {
                    processed_count = processed_count + 1;
                } elif (typeof(item) == "number" && item > 0) {
                    processed_count = processed_count + 1;
                } else {
                    throw {
                        message: "Invalid data item at index " + i + ": " + item,
                        type: "DataValidationError",
                        severity: "medium",
                        index: i,
                        value: item
                    };
                }

                i = i + 1;
            }

            processing_log[processing_log.length()] = "Processed " + processed_count + " items successfully";

            return {
                success: true,
                processed_items: processed_count,
                log: processing_log,
                error: null
            };

        } except (error) {
            processing_log[processing_log.length()] = "Error occurred: " + error;

            return {
                success: false,
                processed_items: 0,
                log: processing_log,
                error: error
            };

        } finally {
            if (resource_opened) {
                processing_log[processing_log.length()] = "Closing file resource";
            }
            processing_log[processing_log.length()] = "Cleanup completed";
        }
    }

    // Test file processing scenarios
    print("Testing file processing with various scenarios:");

    valid_data = ["item1", "item2", 42, "item3", 17];
    invalid_data = ["valid", null, "another"];
    empty_data = [];

    scenario1 = process_file_data("data.txt", valid_data);
    scenario2 = process_file_data("", valid_data);
    scenario3 = process_file_data("test.txt", invalid_data);
    scenario4 = process_file_data("empty.txt", empty_data);

    scenarios = [scenario1, scenario2, scenario3, scenario4];
    scenario_names = ["Valid data", "Empty filename", "Invalid data", "Empty data"];

    j = 0;
    while (j < scenarios.length()) {
        scenario = scenarios[j];
        name = scenario_names[j];
        print("\nScenario: " + name);
        print("  Success: " + scenario.success);
        if (scenario.error != null) {
            print("  Error: " + scenario.error);
        }
        print("  Log entries: " + scenario.log.length());
        k = 0;
        while (k < scenario.log.length()) {
            print("    " + scenario.log[k]);
            k = k + 1;
        }
        j = j + 1;
    }

    return scenarios;
}

// Nested exception handling
function nested_exception_handling() {
    print("\n=== Nested Exception Handling ===");

    // Multi-level exception handling
    function complex_data_processor(input_data) {
        main_log = [];
        processed_results = [];
        total_errors = 0;

        try {
            main_log[main_log.length()] = "Starting complex data processing";

            if (input_data == null) {
                throw {
                    message: "Input data is null",
                    type: "ValidationError",
                    severity: "high"
                };
            }

            // Process each section of data
            i = 0;
            while (i < input_data.length()) {
                section = input_data[i];
                section_result = null;

                try {
                    main_log[main_log.length()] = "Processing section " + i;

                    if (section.type == "numeric") {
                        section_result = process_numeric_section(section);
                    } elif (section.type == "text") {
                        section_result = process_text_section(section);
                    } elif (section.type == "mixed") {
                        section_result = process_mixed_section(section);
                    } else {
                        throw {
                            message: "Unknown section type: " + section.type,
                            type: "ConfigurationError",
                            severity: "medium",
                            sectionType: section.type
                        };
                    }

                    processed_results[processed_results.length()] = section_result;
                    main_log[main_log.length()] = "Section " + i + " processed successfully";

                } except (section_error) {
                    main_log[main_log.length()] = "Error in section " + i + ": " + section_error;
                    total_errors = total_errors + 1;

                    // Add error result
                    processed_results[processed_results.length()] = {
                        success: false,
                        error: section_error,
                        section_index: i
                    };
                }

                i = i + 1;
            }

            main_log[main_log.length()] = "Processing completed. Errors: " + total_errors;

            return {
                success: total_errors == 0,
                results: processed_results,
                error_count: total_errors,
                log: main_log,
                error: null
            };

        } except (main_error) {
            main_log[main_log.length()] = "Main processing error: " + main_error;

            return {
                success: false,
                results: processed_results,
                error_count: total_errors + 1,
                log: main_log,
                error: main_error
            };
        }
    }

    // Helper functions for section processing
    function process_numeric_section(section) {
        try {
            if (section.data == null || section.data.length() == 0) {
                throw {
                    message: "No numeric data provided",
                    type: "DataError",
                    severity: "medium"
                };
            }

            sum = 0;
            count = 0;
            l = 0;
            while (l < section.data.length()) {
                item = section.data[l];
                if (typeof(item) != "number") {
                    throw {
                        message: "Non-numeric item found: " + item,
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
                message: "Numeric processing error: " + error,
                type: "ProcessingError",
                severity: "high",
                originalError: error
            };
        }
    }

    function process_text_section(section) {
        try {
            if (section.data == null || section.data.length() == 0) {
                throw {
                    message: "No text data provided",
                    type: "DataError",
                    severity: "medium"
                };
            }

            total_length = 0;
            word_count = 0;
            m = 0;
            while (m < section.data.length()) {
                item = section.data[m];
                if (typeof(item) != "string") {
                    throw {
                        message: "Non-string item found: " + item,
                        type: "ValidationError",
                        severity: "medium",
                        value: item
                    };
                }
                total_length = total_length + string.length(item);

                // Simple word counting
                words = string.split(item, " ");
                word_count = word_count + words.length();
                m = m + 1;
            }

            return {
                success: true,
                type: "text",
                total_length: total_length,
                word_count: word_count,
                item_count: section.data.length()
            };

        } except (error) {
            throw {
                message: "Text processing error: " + error,
                type: "ProcessingError",
                severity: "high",
                originalError: error
            };
        }
    }

    function process_mixed_section(section) {
        try {
            if (section.data == null || section.data.length() == 0) {
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
            while (n < section.data.length()) {
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
                total_items: section.data.length()
            };

        } except (error) {
            throw {
                message: "Mixed processing error: " + error,
                type: "ProcessingError",
                severity: "high",
                originalError: error
            };
        }
    }

    // Test complex data processing
    test_data = [
        {type: "numeric", data: [1, 2, 3, 4, 5]},
        {type: "text", data: ["hello world", "foo bar", "test string"]},
        {type: "mixed", data: ["text", 42, "more text", 17, true]},
        {type: "numeric", data: [10, "invalid", 30]},
        {type: "unknown", data: ["should", "fail"]},
        {type: "text", data: []}
    ];

    print("Testing complex nested exception handling:");
    result = complex_data_processor(test_data);

    print("Overall success: " + result.success);
    print("Error count: " + result.error_count);
    print("Results processed: " + result.results.length());

    print("\nProcessing log:");
    o = 0;
    while (o < result.log.length()) {
        print("  " + result.log[o]);
        o = o + 1;
    }

    return result;
}

// Exception propagation and chaining
function exception_propagation_chaining() {
    print("\n=== Exception Propagation and Chaining ===");

    // Chain of function calls with exception propagation
    function level1_function(input) {
        try {
            print("Level 1: Processing input");
            result = level2_function(input);
            print("Level 1: Completed successfully");
            return result;
        } except (error) {
            enhanced_error = "Level 1 error: " + error;
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
            enhanced_error = "Level 2 error: " + error;
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
            enhanced_error = "Level 3 error: " + error;
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
        print("Level 4: Final result calculated: " + result);
        return result;
    }

    // Test exception propagation with various inputs
    test_inputs = [
        {value: 5},      // Should succeed
        {value: -3},     // Should fail at level 4
        {value: 1500},   // Should fail at level 4
        {missing: 42},   // Should fail at level 3
        "not_object",    // Should fail at level 3
        null             // Should fail at level 2
    ];

    input_descriptions = [
        "Valid input (value: 5)",
        "Negative value (-3)",
        "Large value (1500)",
        "Missing value property",
        "String instead of object",
        "Null input"
    ];

    print("Testing exception propagation chain:");

    p = 0;
    while (p < test_inputs.length()) {
        input = test_inputs[p];
        description = input_descriptions[p];

        print("\n--- Test " + (p + 1) + ": " + description + " ---");

        try {
            result = level1_function(input);
            print("SUCCESS: Final result = " + result.level3_result);
        } except (final_error) {
            print("FINAL ERROR: " + final_error);
        }

        p = p + 1;
    }

    return test_inputs;
}

// Custom exception types and error handling
function custom_exception_types() {
    print("\n=== Custom Exception Types and Error Handling ===");

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
                validation_errors[validation_errors.length()] =
                    create_error("ValidationError", "Username is required", "USER_002", {field: "username"});
            } elif (string.length(user_data.username) < 3) {
                validation_errors[validation_errors.length()] =
                    create_error("ValidationError", "Username must be at least 3 characters", "USER_003", {field: "username", min_length: 3});
            } elif (!regex.is_alphanumeric_underscore(user_data.username)) {
                validation_errors[validation_errors.length()] =
                    create_error("ValidationError", "Username can only contain letters, numbers, and underscores", "USER_004", {field: "username"});
            }

            // Email validation
            if (user_data.email == null || string.length(user_data.email) == 0) {
                validation_errors[validation_errors.length()] =
                    create_error("ValidationError", "Email is required", "USER_005", {field: "email"});
            } elif (!regex.is_email(user_data.email)) {
                validation_errors[validation_errors.length()] =
                    create_error("ValidationError", "Invalid email format", "USER_006", {field: "email", value: user_data.email});
            }

            // Password validation
            if (user_data.password == null || string.length(user_data.password) == 0) {
                validation_errors[validation_errors.length()] =
                    create_error("ValidationError", "Password is required", "USER_007", {field: "password"});
            } elif (string.length(user_data.password) < 8) {
                validation_errors[validation_errors.length()] =
                    create_error("ValidationError", "Password must be at least 8 characters", "USER_008", {field: "password", min_length: 8});
            }

            // Age validation
            if (user_data.age != null) {
                if (typeof(user_data.age) != "number") {
                    validation_errors[validation_errors.length()] =
                        create_error("ValidationError", "Age must be a number", "USER_009", {field: "age", value: user_data.age});
                } elif (user_data.age < 13) {
                    validation_errors[validation_errors.length()] =
                        create_error("BusinessLogicError", "Users must be at least 13 years old", "USER_010", {field: "age", min_age: 13});
                } elif (user_data.age > 120) {
                    validation_errors[validation_errors.length()] =
                        create_error("ValidationError", "Invalid age value", "USER_011", {field: "age", max_age: 120});
                }
            }

            // If there are validation errors, throw them
            if (validation_errors.length() > 0) {
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
            user_id = "USER_" + datetime.timestamp();
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
    test_users = [
        {username: "john_doe", email: "john@example.com", password: "securepass123", age: 25},
        {username: "x", email: "invalid-email", password: "short", age: 12},
        {username: "admin", email: "admin@example.com", password: "adminpass123", age: 30},
        {username: "jane_smith", email: "blacklisted@example.com", password: "password123", age: 28},
        {email: "missing@username.com", password: "password123", age: 22},
        null
    ];

    user_descriptions = [
        "Valid user data",
        "Multiple validation errors",
        "Reserved username",
        "Blacklisted email",
        "Missing username",
        "Null user data"
    ];

    print("Testing custom exception handling:");

    q = 0;
    while (q < test_users.length()) {
        user = test_users[q];
        description = user_descriptions[q];

        print("\n--- Registration Test " + (q + 1) + ": " + description + " ---");

        result = handle_user_registration(user);

        if (result.success) {
            print("SUCCESS: User created with ID " + result.user_id);
        } else {
            error = result.error;
            print("FAILED: " + error.error_type + " - " + error.message + " (Code: " + error.error_code + ")");

            if (error.error_type == "MultipleValidationErrors") {
                print("Validation Errors:");
                r = 0;
                while (r < error.context.errors.length()) {
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
    print("\n=== Error Recovery and Fallback Strategies ===");

    // Service with multiple fallback strategies
    function resilient_data_service(request) {
        attempts_log = [];
        max_retries = 3;

        // Try primary service
        try {
            attempts_log[attempts_log.length()] = "Attempting primary service";
            result = call_primary_service(request);
            attempts_log[attempts_log.length()] = "Primary service succeeded";
            return {
                success: true,
                data: result,
                service_used: "primary",
                attempts: attempts_log
            };
        } except (primary_error) {
            attempts_log[attempts_log.length()] = "Primary service failed: " + primary_error;
        }

        // Try secondary service
        try {
            attempts_log[attempts_log.length()] = "Attempting secondary service";
            result = call_secondary_service(request);
            attempts_log[attempts_log.length()] = "Secondary service succeeded";
            return {
                success: true,
                data: result,
                service_used: "secondary",
                attempts: attempts_log
            };
        } except (secondary_error) {
            attempts_log[attempts_log.length()] = "Secondary service failed: " + secondary_error;
        }

        // Try cached data
        try {
            attempts_log[attempts_log.length()] = "Attempting cached data";
            result = get_cached_data(request);
            if (result != null) {
                attempts_log[attempts_log.length()] = "Cached data found";
                return {
                    success: true,
                    data: result,
                    service_used: "cache",
                    attempts: attempts_log
                };
            } else {
                attempts_log[attempts_log.length()] = "No cached data available";
            }
        } except (cache_error) {
            attempts_log[attempts_log.length()] = "Cache access failed: " + cache_error;
        }

        // Final fallback - default data
        attempts_log[attempts_log.length()] = "Using default fallback data";
        return {
            success: true,
            data: get_default_data(request),
            service_used: "default",
            attempts: attempts_log
        };
    }

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

    // Test resilient service with various scenarios
    test_requests = [
        {id: "normal_request"},
        {id: "fail_primary"},
        {id: "fail_secondary"},
        {id: "cached_only"},
        {id: "fail_all"}
    ];

    request_descriptions = [
        "Normal request (should use primary)",
        "Primary fails (should use secondary)",
        "Secondary fails (should use primary)",
        "Only cached data available",
        "All services fail (should use default)"
    ];

    print("Testing resilient data service:");

    s = 0;
    while (s < test_requests.length()) {
        request = test_requests[s];
        description = request_descriptions[s];

        print("\n--- Request " + (s + 1) + ": " + description + " ---");

        result = resilient_data_service(request);
        print("Service used: " + result.service_used);
        print("Data quality: " + result.data.quality);
        print("Attempts made:");

        t = 0;
        while (t < result.attempts.length()) {
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

    print("\n==============================================");
    print("  ALL EXCEPTION HANDLING TESTS COMPLETED");
    print("==============================================");

    return results;
}

// Execute comprehensive exception handling test
main();