// Comprehensive Object Operations Test - All ML Object Patterns
import collections;
import string;
import datetime;

// === HELPER FUNCTIONS ===
function safe_upsert(arr, pos, item) {
    if (pos < arr.length) {
        new_arr = [];
        i = 0;
        while (i < arr.length) {
            if (i == pos) {
                new_arr = collections.append(new_arr, item);
            } else {
                new_arr = collections.append(new_arr, arr[i]);
            }
            i = i + 1;
        }
        return new_arr;
    } else {
        return collections.append(arr, item);
    }
}

function safe_append(arr, item) {
    return collections.append(arr, item);
}

function object_to_string(obj) {
    if (obj == null) {
        return "null";
    }
    return "[Object]";
}

// === PHASE 1: BASIC OBJECT OPERATIONS ===
function object_creation_basics() {
    print("=== Object Creation and Basics ===");

    // Simple object creation
    empty_object = {};
    person = {name: "John Doe", age: 30, active: true, salary: 50000.0};
    student = {
        name: "Alice Johnson",
        grades: [95, 87, 92, 88],
        courses: ["Math", "Science", "History"],
        active: true
    };
    company = {
        name: "Tech Corp",
        founded: 2010,
        address: {
            street: "123 Main St",
            city: "Anytown",
            state: "CA",
            zip: "12345"
        },
        employees: {
            total: 150,
            departments: ["Engineering", "Sales", "Marketing"]
        }
    };

    print("Empty object: " + object_to_string(empty_object));
    print("Person name: " + person.name + ", age: " + string.toString(person.age));
    print("Student name: " + student.name + ", grade count: " + string.toString(student.grades.length));
    print("Company: " + company.name + " (founded " + string.toString(company.founded) + ")");

    return {empty: empty_object, person: person, student: student, company: company};
}

function object_property_access() {
    print("\n=== Object Property Access and Modification ===");

    employee = {
        id: 1001,
        name: "Bob Smith",
        department: "Engineering",
        skills: ["Python", "Java", "JavaScript"],
        active: true,
        salary: 75000,
        contact: {
            email: "bob@company.com",
            phone: "555-0123"
        }
    };

    print("Original employee: " + employee.name + " (" + string.toString(employee.id) + ")");

    // Property access
    emp_name = employee.name;
    emp_id = employee.id;
    emp_department = employee.department;
    emp_active = employee.active;

    print("\nProperty Access:");
    print("Name: " + emp_name);
    print("ID: " + string.toString(emp_id));
    print("Department: " + emp_department);
    print("Active: " + string.toString(emp_active));

    // Nested object access
    emp_email = employee.contact.email;
    emp_phone = employee.contact.phone;
    print("Email: " + emp_email);
    print("Phone: " + emp_phone);

    // Array access
    first_skill = employee.skills[0];
    skill_count = employee.skills.length;
    print("First skill: " + first_skill);
    print("Number of skills: " + string.toString(skill_count));

    // Property modification
    employee.department = "DevOps";
    employee.salary = 80000;
    employee.active = false;

    print("\nAfter modifications:");
    print("New department: " + employee.department);
    print("New salary: " + string.toString(employee.salary));
    print("Active status: " + string.toString(employee.active));

    // Nested property modification
    employee.contact.email = "bob.smith@newcompany.com";
    employee.skills[0] = "Go";

    print("New email: " + employee.contact.email);
    print("Modified first skill: " + employee.skills[0]);

    return {
        original_name: emp_name,
        modified_employee: employee,
        contact_info: {email: emp_email, phone: emp_phone}
    };
}

function object_composition_relationships() {
    print("\n=== Object Composition and Relationships ===");

    address = {street: "456 Oak Ave", city: "Springfield", state: "IL", zip: "62701"};
    contact_info = {email: "contact@example.com", phone: "555-0199", fax: "555-0198"};
    person = {name: "Sarah Wilson", age: 28, address: address, contact: contact_info};

    project1 = {name: "Website Redesign", status: "active", lead: person};
    project2 = {name: "Mobile App", status: "planning", lead: person};

    print("Person: " + person.name + " (age " + string.toString(person.age) + ")");
    print("Project 1: " + project1.name + " - " + project1.status);
    print("Project 2: " + project2.name + " - " + project2.status);

    // Shared object modification
    person.age = 29;
    print("\nAfter modifying shared person's age:");
    print("Person age: " + string.toString(person.age));
    print("Project 1 lead age: " + string.toString(project1.lead.age));
    print("Project 2 lead age: " + string.toString(project2.lead.age));

    // Object with function references
    calculator = {
        value: 0,
        name: "BasicCalculator",
        version: 1.0
    };

    // Simulate methods with separate functions
    function calc_add(calc, x) {
        calc.value = calc.value + x;
        return calc.value;
    }

    function calc_multiply(calc, x) {
        calc.value = calc.value * x;
        return calc.value;
    }

    function calc_reset(calc) {
        calc.value = 0;
        return calc.value;
    }

    print("\nCalculator object with methods:");
    print("Initial value: " + string.toString(calculator.value));

    calculator.value = 10;
    result1 = calc_add(calculator, 10);
    print("After add(10): " + string.toString(result1));

    result2 = calc_multiply(calculator, 3);
    print("After multiply(3): " + string.toString(result2));

    result3 = calc_reset(calculator);
    print("After reset(): " + string.toString(result3));

    return {
        person: person,
        projects: [project1, project2],
        calculator: calculator,
        shared_modification_test: "passed"
    };
}

// === PHASE 2: STANDARD LIBRARY OBJECT INTEGRATION ===
function stdlib_object_integration() {
    print("\n=== Standard Library Object Integration ===");

    // DateTime objects
    print("DateTime Objects:");
    meeting_start = datetime.createTimestamp(2024, 3, 15, 14, 30, 0);
    meeting_end = datetime.addTimedelta(meeting_start, 0, 2, 0);
    day_start = datetime.startOfDay(meeting_start);

    event = {
        name: "Sprint Planning",
        start_time: meeting_start,
        end_time: meeting_end,
        duration: meeting_end - meeting_start,
        type: "meeting"
    };

    print("Event: " + event.name);
    print("Start: " + string.toString(event.start_time));
    print("Duration: " + string.toString(event.duration) + " seconds");

    // String pattern objects
    print("\nString Pattern Objects:");
    email_validator = {
        pattern: "@",
        name: "EmailValidator",
        description: "Simple email validation"
    };

    phone_validator = {
        pattern: "-",
        name: "PhoneValidator",
        description: "Simple phone validation"
    };

    test_email = "user@company.com";
    test_phone = "555-123-4567";

    email_valid = string.contains(test_email, email_validator.pattern);
    phone_valid = string.contains(test_phone, phone_validator.pattern);

    validation_results = {
        email_test: {
            input: test_email,
            valid: email_valid,
            validator: email_validator.name
        },
        phone_test: {
            input: test_phone,
            valid: phone_valid,
            validator: phone_validator.name
        }
    };

    print("Email validation: " + string.toString(validation_results.email_test.valid));
    print("Phone validation: " + string.toString(validation_results.phone_test.valid));

    return {event: event, validators: {email: email_validator, phone: phone_validator}, results: validation_results};
}

// === PHASE 3: PRACTICAL OBJECT PATTERNS ===
function practical_object_patterns() {
    print("\n=== Practical Object Patterns ===");

    // Configuration objects
    print("Configuration Management:");
    default_config = {
        timeout: 5000,
        retries: 3,
        debug: false,
        api_version: "v1",
        max_connections: 100
    };

    user_config = {
        timeout: 8000,
        debug: true,
        custom_header: "X-App-Version"
    };

    // Manual configuration merging
    final_config = {
        timeout: user_config.timeout,  // Use user preference
        retries: default_config.retries,  // Use default
        debug: user_config.debug,  // Use user preference
        api_version: default_config.api_version,  // Use default
        max_connections: default_config.max_connections,  // Use default
        custom_header: user_config.custom_header  // New from user
    };

    print("Final timeout: " + string.toString(final_config.timeout));
    print("Debug enabled: " + string.toString(final_config.debug));
    print("API version: " + final_config.api_version);

    // Result objects for error handling
    print("\nResult Objects:");
    function create_success_result(data) {
        return {
            success: true,
            data: data,
            error: null,
            timestamp: datetime.createTimestamp(2024, 3, 15, 10, 0, 0),
            type: "success"
        };
    }

    function create_error_result(message) {
        return {
            success: false,
            data: null,
            error: message,
            timestamp: datetime.createTimestamp(2024, 3, 15, 10, 0, 0),
            type: "error"
        };
    }

    api_success = create_success_result("Data retrieved successfully");
    api_error = create_error_result("Network timeout occurred");

    print("Success result: " + string.toString(api_success.success));
    print("Error message: " + api_error.error);

    // Collection management objects
    print("\nCollection Management:");
    user_collection = {
        items: [],
        count: 0,
        name: "UserDatabase",
        max_size: 1000
    };

    // Add users to collection
    user1 = {id: 1, name: "Alice Admin", role: "admin", active: true};
    user2 = {id: 2, name: "Bob User", role: "user", active: true};
    user3 = {id: 3, name: "Carol Manager", role: "manager", active: false};

    user_collection.items = safe_append(user_collection.items, user1);
    user_collection.count = user_collection.count + 1;

    user_collection.items = safe_append(user_collection.items, user2);
    user_collection.count = user_collection.count + 1;

    user_collection.items = safe_append(user_collection.items, user3);
    user_collection.count = user_collection.count + 1;

    print("Collection: " + user_collection.name);
    print("User count: " + string.toString(user_collection.count));
    print("First user: " + user_collection.items[0].name + " (" + user_collection.items[0].role + ")");
    print("Max capacity: " + string.toString(user_collection.max_size));

    return {
        config: final_config,
        results: {success: api_success, error: api_error},
        collection: user_collection
    };
}

// === PHASE 4: OBJECT UTILITIES AND VALIDATION ===
function object_utilities_validation() {
    print("\n=== Object Utilities and Validation ===");

    // Object copying
    print("Object Copying:");
    original = {
        name: "DataProcessor",
        version: 2.1,
        settings: {
            batch_size: 100,
            timeout: 30000,
            retry_enabled: true
        },
        modules: ["parser", "validator", "transformer"]
    };

    // Manual shallow copy
    copy = {
        name: original.name,
        version: original.version,
        settings: original.settings,  // Shared reference
        modules: original.modules    // Shared reference
    };

    // Modify copy
    copy.name = "DataProcessorV2";
    copy.version = 2.2;

    print("Original: " + original.name + " v" + string.toString(original.version));
    print("Copy: " + copy.name + " v" + string.toString(copy.version));
    print("Settings shared: " + string.toString(copy.settings.batch_size == original.settings.batch_size));

    // Object merging
    print("\nObject Merging:");
    base_api = {name: "CoreAPI", version: "1.0", endpoints: 25, secure: true};
    extension_api = {version: "1.1", endpoints: 30, features: ["auth", "cache"], beta: true};

    merged_api = {
        name: base_api.name,  // Keep base
        version: extension_api.version,  // Override with extension
        endpoints: extension_api.endpoints,  // Override with extension
        secure: base_api.secure,  // Keep base
        features: extension_api.features,  // New from extension
        beta: extension_api.beta  // New from extension
    };

    print("Merged API: " + merged_api.name + " v" + merged_api.version);
    print("Endpoints: " + string.toString(merged_api.endpoints));
    print("Features: " + string.toString(merged_api.features.length));

    // Object validation
    print("\nObject Validation:");
    function validate_user_profile(profile) {
        errors = [];

        // Required field validation
        if (profile.name == null || profile.name == "") {
            errors = safe_append(errors, "Name is required");
        }

        if (profile.email == null || profile.email == "") {
            errors = safe_append(errors, "Email is required");
        }

        if (profile.age == null || profile.age < 18 || profile.age > 120) {
            errors = safe_append(errors, "Age must be between 18 and 120");
        }

        // Email format validation (simple)
        if (profile.email != null && !string.contains(profile.email, "@")) {
            errors = safe_append(errors, "Invalid email format");
        }

        return {
            valid: errors.length == 0,
            errors: errors,
            error_count: errors.length,
            validated_at: datetime.createTimestamp(2024, 3, 15, 12, 0, 0)
        };
    }

    valid_profile = {
        name: "Alice Johnson",
        email: "alice@company.com",
        age: 30,
        department: "Engineering"
    };

    invalid_profile = {
        name: "",
        email: "invalid-email",
        age: 15,
        department: "Marketing"
    };

    validation1 = validate_user_profile(valid_profile);
    validation2 = validate_user_profile(invalid_profile);

    print("Valid profile check: " + string.toString(validation1.valid) + " (errors: " + string.toString(validation1.error_count) + ")");
    print("Invalid profile check: " + string.toString(validation2.valid) + " (errors: " + string.toString(validation2.error_count) + ")");

    // Object serialization
    print("\nObject Serialization:");
    product = {
        id: 12345,
        name: "Wireless Headphones",
        price: 99.99,
        in_stock: true,
        categories: ["electronics", "audio"],
        rating: 4.5
    };

    // Manual serialization to string
    serialized = "{" +
        "id:" + string.toString(product.id) + "," +
        "name:'" + product.name + "'," +
        "price:" + string.toString(product.price) + "," +
        "in_stock:" + string.toString(product.in_stock) + "," +
        "categories:" + string.toString(product.categories.length) + " items," +
        "rating:" + string.toString(product.rating) +
        "}";

    print("Product serialized: " + serialized);

    // Create metadata object
    serialization_info = {
        original_object: "product",
        serialized_length: string.length(serialized),
        format: "custom_string",
        created_at: datetime.createTimestamp(2024, 3, 15, 15, 30, 0)
    };

    print("Serialization length: " + string.toString(serialization_info.serialized_length) + " characters");

    return {
        original: original,
        copy: copy,
        merged: merged_api,
        validations: {valid: validation1, invalid: validation2},
        serialization: serialization_info
    };
}

// === MAIN EXECUTION FUNCTION ===
function main() {
    print("========================================");
    print("  COMPREHENSIVE OBJECT OPERATIONS TEST");
    print("========================================");

    results = {
        creation: null,
        access: null,
        composition: null,
        stdlib_integration: null,
        practical_patterns: null,
        utilities: null
    };

    // Execute all test phases
    results.creation = object_creation_basics();
    results.access = object_property_access();
    results.composition = object_composition_relationships();
    results.stdlib_integration = stdlib_object_integration();
    results.practical_patterns = practical_object_patterns();
    results.utilities = object_utilities_validation();

    print("\n========================================");
    print("  ALL OBJECT TESTS COMPLETED");
    print("========================================");

    return results;
}

// Execute the comprehensive test
main();