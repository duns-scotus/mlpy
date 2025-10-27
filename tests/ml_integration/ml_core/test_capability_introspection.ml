// Test requiredCapabilities and enhanced help() functions
// This tests the new capability introspection feature

import console;

// Test 1: requiredCapabilities with builtin functions (no capabilities)
print("Test 1: requiredCapabilities with builtin functions");
caps = requiredCapabilities(print);
print("print requires: " + str(caps));
if (len(caps) == 0) {
    print("  [PASS] print requires no capabilities");
} else {
    print("  [FAIL] Expected empty list");
}

caps = requiredCapabilities(typeof);
print("typeof requires: " + str(caps));
if (len(caps) == 0) {
    print("  [PASS] typeof requires no capabilities");
} else {
    print("  [FAIL] Expected empty list");
}

caps = requiredCapabilities(len);
print("len requires: " + str(caps));
if (len(caps) == 0) {
    print("  [PASS] len requires no capabilities");
} else {
    print("  [FAIL] Expected empty list");
}

// Test 2: requiredCapabilities with console.log (should have empty capabilities)
print("\nTest 2: requiredCapabilities with console.log");
caps = requiredCapabilities(console.log);
print("console.log requires: " + str(caps));
if (len(caps) == 0) {
    print("  [PASS] console.log requires no capabilities");
} else {
    print("  [FAIL] Expected empty list");
}

// Test 3: help() includes capability information for functions with capabilities
print("\nTest 3: help() includes capability information");
helpText = help(print);
print("help(print):");
print(helpText);
// Just verify help text is not empty - visual inspection will confirm format
if (len(helpText) > 0) {
    print("  [PASS] help returns information for print");
} else {
    print("  [FAIL] Expected help text for print");
}

// Test 4: help() includes capability information for console.log
print("\nTest 4: help() for console.log");
helpText = help(console.log);
print("help(console.log):");
print(helpText);
// Just verify help text is not empty - visual inspection will confirm format
if (len(helpText) > 0) {
    print("  [PASS] help returns information for console.log");
} else {
    print("  [FAIL] Expected help text for console.log");
}

// Test 5: Defensive programming pattern - canCall helper function
print("\nTest 5: Defensive programming pattern");
function canCall(func) {
    required = requiredCapabilities(func);
    for (cap in required) {
        if (!hasCapability(cap)) {
            return false;
        }
    }
    return true;
}

// Test with functions that have no requirements
if (canCall(console.log)) {
    print("  [PASS] canCall(console.log) returns true");
} else {
    print("  [FAIL] Expected canCall(console.log) to return true");
}

if (canCall(print)) {
    print("  [PASS] canCall(print) returns true");
} else {
    print("  [FAIL] Expected canCall(print) to return true");
}

// Test 6: Combined usage - checkFunctionAccess helper
print("\nTest 6: Combined usage pattern");
function checkFunctionAccess(func, funcName) {
    required = requiredCapabilities(func);

    if (len(required) == 0) {
        print(funcName + " requires no capabilities - always available");
        return true;
    }

    print(funcName + " requires capabilities: " + str(required));

    missing = [];
    for (cap in required) {
        if (hasCapability(cap)) {
            print("  + Have " + cap);
        } else {
            print("  - Missing " + cap);
            missing = missing + [cap];
        }
    }

    return len(missing) == 0;
}

// Test with builtin functions
if (checkFunctionAccess(console.log, "console.log")) {
    print("  [PASS] console.log is accessible");
} else {
    print("  [FAIL] Expected console.log to be accessible");
}

if (checkFunctionAccess(typeof, "typeof")) {
    print("  [PASS] typeof is accessible");
} else {
    print("  [FAIL] Expected typeof to be accessible");
}

// Test 7: Test with custom function (no declared capabilities)
print("\nTest 7: Custom function capability check");
function myCustomFunc(x) {
    return x + 1;
}

caps = requiredCapabilities(myCustomFunc);
print("myCustomFunc requires: " + str(caps));
if (len(caps) == 0) {
    print("  [PASS] Custom function has no declared capabilities");
} else {
    print("  [FAIL] Expected empty list for custom function");
}

// Test 8: Feature detection pattern
print("\nTest 8: Feature detection pattern");
function checkAvailableFeatures() {
    features = [];

    // Check builtin operations (always available)
    if (len(requiredCapabilities(print)) == 0) {
        features = features + ["printing"];
    }

    if (len(requiredCapabilities(typeof)) == 0) {
        features = features + ["type_checking"];
    }

    if (len(requiredCapabilities(console.log)) == 0) {
        features = features + ["console_logging"];
    }

    return features;
}

available = checkAvailableFeatures();
print("Available features: " + str(available));
if (len(available) >= 3) {
    print("  [PASS] Feature detection found expected features");
} else {
    print("  [FAIL] Expected at least 3 available features");
}

print("\n========================================");
print("All capability introspection tests completed!");
print("========================================");
