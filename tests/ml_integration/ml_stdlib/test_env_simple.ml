// Simple test for env module
import env;
import console;

console.log("Testing env module...");

env.set("TEST_VAR", "test_value");
value = env.get("TEST_VAR");
console.log("Got value: " + value);

console.log("Test complete!");
