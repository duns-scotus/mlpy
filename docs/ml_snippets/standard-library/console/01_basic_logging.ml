// ============================================
// Example: Basic Console Logging
// Category: standard-library/console
// Demonstrates: log(), info(), debug(), warn(), error()
// ============================================

import console;

console.log("=== Basic Console Logging ===\n");

// Example 1: console.log() - General output
console.log("Example 1: console.log() - General output");
console.log("Hello, World!");
console.log("Simple message");
console.log("Multiple", "arguments", "work", "fine");

// Example 2: console.info() - Informational messages
console.log("\nExample 2: console.info() - Informational messages");
console.info("Application started");
console.info("Configuration loaded");
console.info("Ready to process requests");

// Example 3: console.debug() - Debug output
console.log("\nExample 3: console.debug() - Debug output");
x = 42;
y = "test";
console.debug("Variable x:", x);
console.debug("Variable y:", y);
console.debug("Debug information here");

// Example 4: console.warn() - Warnings
console.log("\nExample 4: console.warn() - Warnings");
console.warn("This is a warning message");
console.warn("Deprecated function used");
console.warn("Low disk space");

// Example 5: console.error() - Errors
console.log("\nExample 5: console.error() - Errors");
console.error("This is an error message");
console.error("File not found");
console.error("Connection failed");

// Example 6: All methods with values
console.log("\nExample 6: Logging different types");
count = 100;
name = "Alice";
active = true;

console.log("Count:", count);
console.info("User:", name);
console.debug("Active status:", active);
console.warn("Count exceeds:", 50);
console.error("Invalid count:", -1);

// Example 7: Numeric values
console.log("\nExample 7: Logging numbers");
console.log("Integer:", 42);
console.log("Float:", 3.14);
console.log("Calculation:", 10 * 5);
console.info("Progress:", 75, "percent");

// Example 8: Arrays and objects
console.log("\nExample 8: Logging collections");
numbers = [1, 2, 3, 4, 5];
person = {name: "Bob", age: 30};

console.log("Array:", numbers);
console.log("Object:", person);
console.info("Array length:", len(numbers));
console.debug("Person name:", person.name);

console.log("\n=== Basic Logging Complete ===");
