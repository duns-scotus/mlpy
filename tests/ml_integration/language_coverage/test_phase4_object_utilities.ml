// Phase 4 Test: Object Utilities and Validation
import collections;
import string;

function test_object_copying() {
    print("=== Object Copying ===");

    original = {
        name: "John",
        age: 30,
        settings: {theme: "dark", lang: "en"}
    };

    // Manual shallow copy
    copy = {
        name: original.name,
        age: original.age,
        settings: original.settings
    };

    // Modify copy
    copy.name = "Jane";
    copy.age = 25;

    print("Original: " + original.name + ", age: " + string.toString(original.age));
    print("Copy: " + copy.name + ", age: " + string.toString(copy.age));

    return {original: original, copy: copy};
}

function test_object_merging() {
    print("=== Object Merging ===");

    base = {name: "App", version: "1.0", debug: false};
    override = {version: "2.0", debug: true, port: 8080};

    // Manual merge
    merged = {
        name: base.name,
        version: override.version,  // Override wins
        debug: override.debug,      // Override wins
        port: override.port         // New property
    };

    print("Merged version: " + merged.version);
    print("Merged debug: " + string.toString(merged.debug));
    print("Merged port: " + string.toString(merged.port));

    return merged;
}

function test_object_validation() {
    print("=== Object Validation ===");

    function validate_user(user) {
        errors = [];

        // Check required fields
        if (user.name == null || user.name == "") {
            errors = collections.append(errors, "Name is required");
        }

        if (user.email == null || user.email == "") {
            errors = collections.append(errors, "Email is required");
        }

        if (user.age < 0 || user.age > 150) {
            errors = collections.append(errors, "Age must be between 0 and 150");
        }

        return {
            valid: errors.length == 0,
            errors: errors,
            error_count: errors.length
        };
    }

    valid_user = {name: "Alice", email: "alice@example.com", age: 30};
    invalid_user = {name: "", email: "bad", age: -5};

    result1 = validate_user(valid_user);
    result2 = validate_user(invalid_user);

    print("Valid user check: " + string.toString(result1.valid));
    print("Invalid user errors: " + string.toString(result2.error_count));

    return {valid: result1, invalid: result2};
}

function test_object_serialization() {
    print("=== Object Serialization ===");

    user = {
        id: 123,
        name: "John Doe",
        active: true,
        score: 95.5
    };

    // Manual object to string
    serialized = "{" +
        "id:" + string.toString(user.id) + "," +
        "name:'" + user.name + "'," +
        "active:" + string.toString(user.active) + "," +
        "score:" + string.toString(user.score) +
        "}";

    print("Serialized: " + serialized);

    // Create summary object
    summary = {
        type: "user",
        data: serialized,
        length: string.length(serialized)
    };

    print("Summary type: " + summary.type);
    return summary;
}

// Run tests
test_object_copying();
test_object_merging();
test_object_validation();
test_object_serialization();