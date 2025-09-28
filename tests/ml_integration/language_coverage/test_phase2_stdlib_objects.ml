// Phase 2 Test: Standard Library Objects
import datetime;
import collections;
import string;

function test_datetime_objects() {
    print("=== DateTime Objects ===");

    // Create datetime objects (timestamps) - using camelCase methods
    now = datetime.createTimestamp(2024, 1, 15, 10, 30, 0);
    birthday = datetime.createTimestamp(1990, 5, 15, 0, 0, 0);

    // DateTime object manipulation - using camelCase methods
    tomorrow = datetime.addTimedelta(now, 1, 0, 0);
    start_of_day = datetime.startOfDay(now);

    print("Now timestamp: " + string.toString(now));
    print("Tomorrow: " + string.toString(tomorrow));
    print("Start of day: " + string.toString(start_of_day));

    // Create event object with datetime
    event = {
        name: "Meeting",
        start_time: now,
        end_time: tomorrow,
        duration: tomorrow - now
    };

    print("Event: " + event.name);
    return event;
}

function test_string_objects() {
    print("=== String Pattern Objects ===");

    // Create string pattern objects (simpler than regex)
    email_pattern = {
        pattern: "@",  // Simple pattern for demo
        name: "email_validator"
    };

    phone_pattern = {
        pattern: "-",  // Simple pattern for demo
        name: "phone_validator"
    };

    // Test patterns using string functions
    test_email = "user@example.com";
    test_phone = "555-123-4567";

    email_valid = string.contains(test_email, email_pattern.pattern);
    phone_valid = string.contains(test_phone, phone_pattern.pattern);

    print("Email contains @: " + string.toString(email_valid));
    print("Phone contains -: " + string.toString(phone_valid));

    return {email: email_pattern, phone: phone_pattern};
}

function test_function_objects() {
    print("=== Function Objects ===");

    // Functions as object properties
    calculator = {
        name: "BasicCalculator",
        version: 1.0,
        operations: []
    };

    // Simulate function calls (since direct function properties are complex)
    function calc_add(a, b) {
        return a + b;
    }

    function calc_multiply(a, b) {
        return a * b;
    }

    // Use function objects
    sum = calc_add(5, 3);
    product = calc_multiply(4, 7);

    print("Calculator: " + calculator.name);
    print("Sum: " + string.toString(sum));
    print("Product: " + string.toString(product));

    return calculator;
}

// Run tests
test_datetime_objects();
test_string_objects();
test_function_objects();