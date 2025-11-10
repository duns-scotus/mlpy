// Test all env module functions end-to-end
// This validates the complete ML→Python transpilation pipeline for env operations

import env;
import console;

console.log("=== Testing env Module ===");

// Test 1: Basic get/set
console.log("[Test 1] Basic get/set operations");
env.set("TEST_VAR", "test_value");
value = env.get("TEST_VAR");
if (value == "test_value") {
    console.log("PASS: Basic get/set works");
} else {
    console.log("FAIL: FAILED: env.get() returned " + value);
}

// Test 2: Default values
console.log("[Test 2] Default values");
default_val = env.get("NONEXISTENT_VAR_12345", "default");
if (default_val == "default") {
    console.log("PASS: Default values work");
} else {
    console.log("FAIL: FAILED: env.get() with default returned " + default_val);
}

// Test 3: Type conversion - integer
console.log("[Test 3] Type conversion - integer");
env.set("TEST_INT", "42");
int_val = env.get_int("TEST_INT");
if (int_val == 42) {
    console.log("PASS: Integer conversion works: " + str(int_val));
} else {
    console.log("FAIL: FAILED: env.get_int() returned " + str(int_val));
}

// Test 4: Type conversion - boolean
console.log("[Test 4] Type conversion - boolean");
env.set("TEST_BOOL_TRUE", "true");
bool_val_true = env.get_bool("TEST_BOOL_TRUE");
if (bool_val_true == true) {
    console.log("PASS: Boolean true conversion works");
} else {
    console.log("FAIL: FAILED: env.get_bool() for true returned " + str(bool_val_true));
}

env.set("TEST_BOOL_FALSE", "false");
bool_val_false = env.get_bool("TEST_BOOL_FALSE");
if (bool_val_false == false) {
    console.log("PASS: Boolean false conversion works");
} else {
    console.log("FAIL: FAILED: env.get_bool() for false returned " + str(bool_val_false));
}

// Test 5: Type conversion - float
console.log("[Test 5] Type conversion - float");
env.set("TEST_FLOAT", "3.14");
float_val = env.get_float("TEST_FLOAT");
if (float_val == 3.14) {
    console.log("PASS: Float conversion works: " + str(float_val));
} else {
    console.log("FAIL: FAILED: env.get_float() returned " + str(float_val));
}

// Test 6: has() function
console.log("[Test 6] has() function");
env.set("TEST_HAS_VAR", "value");
has_result = env.has("TEST_HAS_VAR");
if (has_result == true) {
    console.log("PASS: has() works for existing var");
} else {
    console.log("FAIL: FAILED: env.has() for existing var returned " + str(has_result));
}

has_missing = env.has("DEFINITELY_NONEXISTENT_VAR_98765");
if (has_missing == false) {
    console.log("PASS: has() works for missing var");
} else {
    console.log("FAIL: FAILED: env.has() for missing var returned " + str(has_missing));
}

// Test 7: delete() function
console.log("[Test 7] delete() function");
env.set("TEST_DELETE_VAR", "will_be_deleted");
before_delete = env.has("TEST_DELETE_VAR");
if (before_delete == true) {
    env.delete("TEST_DELETE_VAR");
    after_delete = env.has("TEST_DELETE_VAR");
    if (after_delete == false) {
        console.log("PASS: delete() function works");
    } else {
        console.log("FAIL: FAILED: env.delete() did not remove variable");
    }
} else {
    console.log("FAIL: FAILED: Variable should exist before delete");
}

// Test 8: require() with missing variable (should throw)
console.log("[Test 8] require() error handling");
try {
    env.require("DEFINITELY_MISSING_VAR_FOR_REQUIRE_TEST");
    console.log("FAIL: FAILED: env.require() should have thrown");
} except (error) {
    console.log("PASS: env.require() correctly threw error for missing variable");
}

// Test 9: Integer with default
console.log("[Test 9] Integer with default");
int_default = env.get_int("MISSING_INT_VAR", 100);
if (int_default == 100) {
    console.log("PASS: Integer default value works");
} else {
    console.log("FAIL: FAILED: env.get_int() with default returned " + str(int_default));
}

// Test 10: Boolean with default
console.log("[Test 10] Boolean with default");
bool_default = env.get_bool("MISSING_BOOL_VAR", true);
if (bool_default == true) {
    console.log("PASS: Boolean default value works");
} else {
    console.log("FAIL: FAILED: env.get_bool() with default returned " + str(bool_default));
}

// Test 11: Float with default
console.log("[Test 11] Float with default");
float_default = env.get_float("MISSING_FLOAT_VAR", 2.5);
if (float_default == 2.5) {
    console.log("PASS: Float default value works");
} else {
    console.log("FAIL: FAILED: env.get_float() with default returned " + str(float_default));
}

// Test 12: Realistic configuration scenario
console.log("[Test 12] Realistic configuration scenario");
env.set("APP_NAME", "MyApp");
env.set("APP_PORT", "8080");
env.set("APP_DEBUG", "true");
env.set("APP_TIMEOUT", "30.5");

app_name = env.get("APP_NAME");
app_port = env.get_int("APP_PORT");
app_debug = env.get_bool("APP_DEBUG");
app_timeout = env.get_float("APP_TIMEOUT");

passed = true;
if (app_name != "MyApp") {
    console.log("FAIL: FAILED: App name mismatch");
    passed = false;
}
if (app_port != 8080) {
    console.log("FAIL: FAILED: App port mismatch");
    passed = false;
}
if (app_debug != true) {
    console.log("FAIL: FAILED: App debug mismatch");
    passed = false;
}
if (app_timeout != 30.5) {
    console.log("FAIL: FAILED: App timeout mismatch");
    passed = false;
}

if (passed) {
    console.log("PASS: Realistic configuration scenario works");
    console.log("  - Name: " + app_name);
    console.log("  - Port: " + str(app_port));
    console.log("  - Debug: " + str(app_debug));
    console.log("  - Timeout: " + str(app_timeout));
}

// Test 13: all() function returns dictionary
console.log("[Test 13] all() function");
all_vars = env.all();
if (typeof(all_vars) == "object") {
    console.log("PASS: all() function returns dictionary with " + str(len(all_vars)) + " variables");
} else {
    console.log("FAIL: FAILED: env.all() should return object");
}

// Cleanup test variables
console.log("[Cleanup] Removing test variables");
env.delete("TEST_VAR");
env.delete("TEST_INT");
env.delete("TEST_BOOL_TRUE");
env.delete("TEST_BOOL_FALSE");
env.delete("TEST_FLOAT");
env.delete("TEST_HAS_VAR");
env.delete("APP_NAME");
env.delete("APP_PORT");
env.delete("APP_DEBUG");
env.delete("APP_TIMEOUT");
console.log("PASS: Cleanup complete");

console.log("=== All env module tests passed! ===");
