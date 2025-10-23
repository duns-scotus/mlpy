// ============================================
// Example: Debug Logging
// Category: standard-library/console
// Demonstrates: Detailed debugging output
// ============================================

import console;

console.log("=== Debug Logging Example ===\n");

// Example 1: Variable inspection
console.log("Example 1: Variable inspection");
x = 10;
y = 20;
z = x + y;

console.debug("x =", x);
console.debug("y =", y);
console.debug("z = x + y =", z);

// Example 2: Function call tracing
console.log("\nExample 2: Function call tracing");

function calculateArea(width, height) {
    console.debug("calculateArea called");
    console.debug("  width:", width);
    console.debug("  height:", height);

    area = width * height;
    console.debug("  result:", area);

    return area;
}

result1 = calculateArea(10, 5);
console.log("Area:", result1);

result2 = calculateArea(7, 3);
console.log("Area:", result2);

// Example 3: Loop debugging
console.log("\nExample 3: Loop debugging");
total = 0;
numbers = [1, 2, 3, 4, 5];

console.debug("Starting loop through", len(numbers), "numbers");
for (num in numbers) {
    console.debug("Processing number:", num);
    total = total + num;
    console.debug("  Running total:", total);
}
console.log("Final total:", total);

// Example 4: Conditional debugging
console.log("\nExample 4: Conditional debugging");

function processValue(value) {
    console.debug("processValue called with:", value);

    if (value < 0) {
        console.debug("  Branch: negative value");
        console.warn("Negative value detected:", value);
        return 0;
    } elif (value == 0) {
        console.debug("  Branch: zero value");
        return 0;
    } else {
        console.debug("  Branch: positive value");
        return value * 2;
    }
}

values = [-5, 0, 10, 3];
console.log("Processing values:", values);

for (val in values) {
    result = processValue(val);
    console.log("Result for", val, ":", result);
}

// Example 5: Data structure debugging
console.log("\nExample 5: Data structure debugging");

users = [
    {name: "Alice", age: 30, active: true},
    {name: "Bob", age: 25, active: false},
    {name: "Carol", age: 35, active: true}
];

console.debug("Processing", len(users), "users");
for (user in users) {
    console.debug("User:", user.name);
    console.debug("  Age:", user.age);
    console.debug("  Active:", user.active);

    if (user.active) {
        console.log("Active user:", user.name);
    } else {
        console.warn("Inactive user:", user.name);
    }
}

// Example 6: State tracking
console.log("\nExample 6: State tracking");

state = {
    count: 0,
    status: "idle"
};

console.debug("Initial state:", state);

function updateState(newCount, newStatus) {
    console.debug("updateState called");
    console.debug("  Old count:", state.count);
    console.debug("  New count:", newCount);
    console.debug("  Old status:", state.status);
    console.debug("  New status:", newStatus);

    state.count = newCount;
    state.status = newStatus;

    console.debug("  Updated state:", state);
}

updateState(5, "processing");
console.log("State:", state);

updateState(10, "complete");
console.log("State:", state);

// Example 7: Algorithm debugging
console.log("\nExample 7: Algorithm debugging - Binary search");

function binarySearch(arr, target) {
    console.debug("binarySearch called");
    console.debug("  Array:", arr);
    console.debug("  Target:", target);

    left = 0;
    right = len(arr) - 1;

    while (left <= right) {
        mid = (left + right) // 2;
        console.debug("  left:", left, "mid:", mid, "right:", right);
        console.debug("  mid value:", arr[mid]);

        if (arr[mid] == target) {
            console.debug("  Found at index:", mid);
            return mid;
        } elif (arr[mid] < target) {
            console.debug("  Search right half");
            left = mid + 1;
        } else {
            console.debug("  Search left half");
            right = mid - 1;
        }
    }

    console.debug("  Not found");
    return -1;
}

sortedArray = [1, 3, 5, 7, 9, 11, 13, 15];
searchTarget = 9;

console.log("Searching for", searchTarget, "in", sortedArray);
index = binarySearch(sortedArray, searchTarget);
console.log("Found at index:", index);

console.log("\n=== Debug Logging Complete ===");
