// Comprehensive test of new ML language features
// Tests: try/except/finally, break/continue, dictionary assignments

function errorHandlingDemo() {
    result = {};

    try {
        // Simulate risky operation
        data = processData("input");
        result["status"] = "success";
        result["data"] = data;
    } except (ValueError) {
        result["status"] = "value_error";
        result["error"] = "Invalid input data";
    } except {
        result["status"] = "unknown_error";
        result["error"] = "Unexpected error occurred";
    } finally {
        result["timestamp"] = getCurrentTime();
    }

    return result;
}

function loopControlDemo() {
    results = [];
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

    for (num in numbers) {
        // Skip even numbers
        if (num % 2 == 0) {
            continue;
        }

        // Stop at 7
        if (num == 7) {
            break;
        }

        // Process odd numbers less than 7
        results[num] = num * num;
    }

    return results;
}

function dictionaryDemo() {
    config = {"name": "app", "version": 1.0};

    // Dictionary assignments
    config["debug"] = true;
    config["max_users"] = 100;
    config["features"] = ["auth", "api", "db"];

    // Nested dictionary access
    config["database"] = {};
    config["database"]["host"] = "localhost";
    config["database"]["port"] = 5432;

    return config;
}

function combinedDemo() {
    settings = dictionaryDemo();

    try {
        processed = loopControlDemo();
        settings["processed_data"] = processed;

        for (key in ["name", "version", "debug"]) {
            if (key == "version") {
                continue;
            }

            if (settings[key] == null) {
                break;
            }
        }

    } except {
        settings["error"] = "Processing failed";
    } finally {
        settings["complete"] = true;
    }

    return settings;
}