// ============================================
// Example: Type Checking and Dynamic Typing
// Category: standard-library/builtin
// Demonstrates: typeof(), isinstance()
// ============================================

print("=== Type Checking ===\n");

// typeof() - Get type of any value
print("Basic types:");
print("  typeof(true) = " + typeof(true));              // "boolean"
print("  typeof(42) = " + typeof(42));                  // "number"
print("  typeof(3.14) = " + typeof(3.14));              // "number"
print("  typeof(\"hello\") = " + typeof("hello"));      // "string"
print("  typeof([1,2,3]) = " + typeof([1,2,3]));        // "array"
print("  typeof({a: 1}) = " + typeof({a: 1}));          // "object"

// typeof() with functions
function greet(name) {
    return "Hello, " + name;
}
print("  typeof(greet) = " + typeof(greet));            // "function"

// isinstance() - Check specific type
print("\nisinstance() checks:");
value = 42;
print("  value = " + str(value));
print("  isinstance(value, \"number\") = " + str(isinstance(value, "number")));    // true
print("  isinstance(value, \"string\") = " + str(isinstance(value, "string")));    // false

text = "hello";
print("  text = \"" + text + "\"");
print("  isinstance(text, \"string\") = " + str(isinstance(text, "string")));      // true
print("  isinstance(text, \"number\") = " + str(isinstance(text, "number")));      // false

// Dynamic type checking in functions
print("\n=== Dynamic Type Processing ===");

function processValue(val) {
    type = typeof(val);

    if (type == "number") {
        return "Number: " + str(val * 2);
    } elif (type == "string") {
        return "String: " + val + "!";
    } elif (type == "boolean") {
        return "Boolean: " + str(!val);
    } elif (type == "array") {
        return "Array with " + str(len(val)) + " elements";
    } else {
        return "Unknown type: " + type;
    }
}

print(processValue(42));
print(processValue("hello"));
print(processValue(true));
print(processValue([1, 2, 3]));

// Type validation for function parameters
print("\n=== Type Validation ===");

function divide(a, b) {
    if (!isinstance(a, "number") || !isinstance(b, "number")) {
        return "Error: Both arguments must be numbers";
    }

    if (b == 0) {
        return "Error: Division by zero";
    }

    return a / b;
}

print("divide(10, 2) = " + str(divide(10, 2)));         // 5
print("divide(10, \"2\") = " + str(divide(10, "2")));   // Error message
print("divide(10, 0) = " + str(divide(10, 0)));         // Error message

// Polymorphic function using type checking
print("\n=== Polymorphic Function ===");

function stringify(value) {
    type = typeof(value);

    if (type == "array") {
        result = "[";
        i = 0;
        while (i < len(value)) {
            if (i > 0) {
                result = result + ", ";
            }
            result = result + stringify(value[i]);
            i = i + 1;
        }
        return result + "]";
    } elif (type == "object") {
        return "{object with " + str(len(keys(value))) + " properties}";
    } elif (type == "string") {
        return "\"" + value + "\"";
    } else {
        return str(value);
    }
}

print("Stringify numbers: " + stringify(42));
print("Stringify strings: " + stringify("hello"));
print("Stringify arrays: " + stringify([1, 2, 3]));
print("Stringify objects: " + stringify({a: 1, b: 2, c: 3}));

// Type-based routing
print("\n=== Type-Based Routing ===");

function handleData(data) {
    if (isinstance(data, "array")) {
        print("  Processing array of " + str(len(data)) + " items");
        total = sum(data);
        print("  Sum: " + str(total));
    } elif (isinstance(data, "object")) {
        print("  Processing object");
        objKeys = keys(data);
        print("  Keys: " + str(objKeys));
    } elif (isinstance(data, "string")) {
        print("  Processing string");
        print("  Length: " + str(len(data)));
        print("  Uppercase: " + data);
    } else {
        print("  Processing value: " + str(data));
    }
}

handleData([1, 2, 3, 4, 5]);
handleData({name: "Alice", age: 30});
handleData("Hello, World!");
handleData(42);

print("\n=== Type Checking Complete ===");
