// Test file to verify string access methods
// Testing both object.method() and module.function() approaches

import string;

function main() {
    print("=== Testing String Access Methods ===");

    test_text = "Hello World";

    // Test 1: Direct property access (like JavaScript)
    print("Testing direct property access:");
    try {
        // This might fail - testing if it works
        direct_length = test_text.length;
        print("Direct length access: " + string.toString(direct_length));
    } except (error) {
        print("Direct length access FAILED: " + string.toString(error));
    }

    // Test 2: Module function access (standard library)
    print("Testing module function access:");
    try {
        module_length = string.length(test_text);
        print("Module length access: " + string.toString(module_length));
    } except (error) {
        print("Module length access FAILED: " + string.toString(error));
    }

    // Test 3: Direct method calls (like JavaScript)
    print("Testing direct method calls:");
    try {
        // This might fail - testing if it works
        direct_upper = test_text.toUpperCase();
        print("Direct toUpperCase: " + direct_upper);
    } except (error) {
        print("Direct toUpperCase FAILED: " + string.toString(error));
    }

    // Test 4: Module method calls (standard library)
    print("Testing module method calls:");
    try {
        module_upper = string.upper(test_text);
        print("Module upper: " + module_upper);
    } except (error) {
        print("Module upper FAILED: " + string.toString(error));
    }

    // Test 5: Substring operations
    print("Testing substring operations:");
    try {
        // Direct substring method
        direct_sub = test_text.substring(0, 5);
        print("Direct substring: " + direct_sub);
    } except (error) {
        print("Direct substring FAILED: " + string.toString(error));
    }

    try {
        // Module substring function
        module_sub = string.substring(test_text, 0, 5);
        print("Module substring: " + module_sub);
    } except (error) {
        print("Module substring FAILED: " + string.toString(error));
    }

    // Test 6: indexOf operations
    print("Testing indexOf operations:");
    try {
        // Direct indexOf method
        direct_index = test_text.indexOf("o");
        print("Direct indexOf: " + string.toString(direct_index));
    } except (error) {
        print("Direct indexOf FAILED: " + string.toString(error));
    }

    try {
        // Module find function
        module_index = string.find(test_text, "o");
        print("Module find: " + string.toString(module_index));
    } except (error) {
        print("Module find FAILED: " + string.toString(error));
    }

    print("=== String Access Methods Test Complete ===");
}

main();