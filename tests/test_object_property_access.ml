// Test file to verify object property access patterns
// Testing various ways objects access properties and methods

function main() {
    print("=== Testing Object Property Access ===");

    // Test 1: Basic object creation and property access
    print("Testing basic object operations:");
    test_obj = {
        name: "test",
        value: 42,
        active: true,
        timeout: 5000,
        nested: {
            inner: "data"
        }
    };

    try {
        print("Object name: " + test_obj.name);
        print("Object value: " + (test_obj.value + ""));
        print("Object active: " + (test_obj.active + ""));
        print("Object timeout: " + (test_obj.timeout + ""));
        print("Nested property: " + test_obj.nested.inner);
    } except (error) {
        print("Basic property access FAILED: " + (error + ""));
    }

    // Test 2: Dynamic property access
    print("Testing dynamic property access:");
    try {
        prop_name = "value";
        // This syntax might not work in ML
        // dynamic_value = test_obj[prop_name];
        // print("Dynamic access: " + (dynamic_value + ""));
        print("Dynamic access: Not testing - likely unsupported");
    } except (error) {
        print("Dynamic property access FAILED: " + (error + ""));
    }

    // Test 3: Property assignment
    print("Testing property assignment:");
    try {
        test_obj.name = "modified";
        test_obj.value = 100;
        test_obj.timeout = 10000;

        print("Modified name: " + test_obj.name);
        print("Modified value: " + (test_obj.value + ""));
        print("Modified timeout: " + (test_obj.timeout + ""));
    } except (error) {
        print("Property assignment FAILED: " + (error + ""));
    }

    // Test 4: Adding new properties
    print("Testing new property addition:");
    try {
        test_obj.new_property = "added";
        print("New property: " + test_obj.new_property);
    } except (error) {
        print("New property addition FAILED: " + (error + ""));
    }

    // Test 5: Object methods (function properties)
    print("Testing object methods:");
    calculator = {
        value: 0,
        add: function(x) {
            calculator.value = calculator.value + x;
            return calculator.value;
        },
        get_value: function() {
            return calculator.value;
        }
    };

    try {
        result1 = calculator.add(10);
        result2 = calculator.add(5);
        current = calculator.get_value();

        print("Calculator add(10): " + (result1 + ""));
        print("Calculator add(5): " + (result2 + ""));
        print("Calculator current value: " + (current + ""));
    } except (error) {
        print("Object methods FAILED: " + (error + ""));
    }

    // Test 6: Checking property existence
    print("Testing property existence:");
    try {
        // Different ways to check if property exists
        has_name = test_obj.name != null;
        has_missing = test_obj.missing_prop != null;

        print("Has name property: " + (has_name + ""));
        print("Has missing property: " + (has_missing + ""));
    } except (error) {
        print("Property existence check FAILED: " + (error + ""));
    }

    print("=== Object Property Access Test Complete ===");
}

main();