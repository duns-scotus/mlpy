// ============================================
// Example: I/O Functions
// Category: language-reference/builtin
// Demonstrates: print() (input() shown but not executed for automation)
// ============================================

import console;

console.log("=== I/O Functions ===\n");

// Example 1: print() - Basic printing
console.log("Example 1: print() - Basic output");
print("Hello, World!");
print("ML", "supports", "multiple", "arguments");
print("The answer is:", 42);

// Example 2: print() with different types
console.log("\nExample 2: print() with different types");
print("Number:", 42);
print("Float:", 3.14);
print("Boolean:", true);
print("Boolean:", false);
print("Array:", [1, 2, 3]);
print("Object:", {name: "Alice", age: 30});

// Example 3: print() vs console.log()
console.log("\nExample 3: print() vs console.log()");
console.log("This is console.log()");
print("This is print()");
console.log("Both output to console");

// Example 4: Formatted output with print()
console.log("\nExample 4: Formatted output");
name = "Alice";
age = 30;
city = "New York";

print("Name:", name);
print("Age:", age);
print("City:", city);
print("Full info:", name, "is", age, "years old and lives in", city);

// Example 5: Print tables
console.log("\nExample 5: Creating formatted tables");
print("=== Multiplication Table ===");
for (i in range(1, 6)) {
    line = str(i) + " x 5 = " + str(i * 5);
    print(line);
}

// Example 6: Progress indicators
console.log("\nExample 6: Progress indicators");
print("Processing items:");
items = ["file1.txt", "file2.txt", "file3.txt"];
for (item in items) {
    print("  Processing:", item);
}
print("Complete!");

// Example 7: Error and success messages
console.log("\nExample 7: Status messages");
function processData(data, validate) {
    if (validate) {
        print("[OK] Data validation passed");
        print("  Processing", len(data), "items");
        return true;
    } else {
        print("[FAIL] Data validation failed");
        return false;
    }
}

processData([1, 2, 3], true);
processData([], false);

// Example 8: Menu display
console.log("\nExample 8: Menu display");
print("=== Main Menu ===");
print("1. Start Game");
print("2. Load Game");
print("3. Settings");
print("4. Exit");
print("=================");

// Example 9: Report generation
console.log("\nExample 9: Report generation");
scores = [85, 92, 78, 95, 88];
print("=== Score Report ===");
print("Total scores:", len(scores));
print("Highest:", max(scores));
print("Lowest:", min(scores));
print("Average:", sum(scores) / len(scores));
print("====================");

// Example 10: Debug output
console.log("\nExample 10: Debug information");
function debugInfo(variable) {
    print("Debug Info:");
    print("  Value:", variable);
    print("  Type:", typeof(variable));
    print("  String:", str(variable));
    if (typeof(variable) == "array" || typeof(variable) == "string") {
        print("  Length:", len(variable));
    }
}

debugInfo(42);
debugInfo("hello");
debugInfo([1, 2, 3]);

// Example 11: Boolean output formatting
console.log("\nExample 11: Boolean formatting");
print("true prints as:", true);   // Lowercase "true"
print("false prints as:", false); // Lowercase "false"

conditions = [
    {test: "5 > 3", result: 5 > 3},
    {test: "10 == 10", result: 10 == 10},
    {test: "7 < 5", result: 7 < 5}
];

print("\nCondition Results:");
for (cond in conditions) {
    print(" ", cond.test, "=>", cond.result);
}

// Example 12: Data listing
console.log("\nExample 12: Data listing");
users = [
    {name: "Alice", role: "Admin"},
    {name: "Bob", role: "User"},
    {name: "Carol", role: "User"}
];

print("=== User List ===");
for (user in users) {
    print(user.name, "-", user.role);
}

// Example 13: Multi-line output
console.log("\nExample 13: Multi-line formatted output");
function displayBox(title, content) {
    border = "=" * 40;
    print(border);
    print(title);
    print(border);
    for (line in content) {
        print(line);
    }
    print(border);
}

displayBox("System Information", [
    "Version: 1.0.0",
    "Platform: ML Runtime",
    "Status: Active"
]);

// Note about input() function
console.log("\nNote: input() function for interactive input");
console.log("The input() function reads user input from console:");
console.log("  name = input(\"Enter your name: \");");
console.log("  age = input(\"Enter your age: \");");
console.log("  ageNum = int(age);  // Convert to number");
console.log("");
console.log("input() always returns a string.");
console.log("Use int() or float() to convert to numbers.");
console.log("");
console.log("Example interactive program structure:");
console.log("  name = input(\"Name: \");");
console.log("  print(\"Hello,\", name);");

// Example 14: Practical output formatting
console.log("\nExample 14: Receipt formatting");
function printReceipt(items, prices) {
    print("=== Receipt ===");

    total = 0;
    for (pair in zip(items, prices)) {
        item = pair[0];
        price = pair[1];
        print(item, "-", "$" + str(price));
        total = total + price;
    }

    print("---------------");
    print("Total: $" + str(total));
    print("===============");
}

printReceipt(
    ["Coffee", "Sandwich", "Cookie"],
    [3.50, 7.99, 2.50]
);

console.log("\n=== I/O Functions Complete ===");
