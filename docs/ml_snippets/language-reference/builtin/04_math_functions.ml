// ============================================
// Example: Math Functions
// Category: language-reference/builtin
// Demonstrates: abs(), min(), max(), round(), sum()
// ============================================

import console;

console.log("=== Math Functions ===\n");

// Example 1: abs() - Absolute value
console.log("Example 1: abs() - Absolute value");
console.log("abs(-5) = " + str(abs(-5)));          // 5
console.log("abs(3.14) = " + str(abs(3.14)));      // 3.14
console.log("abs(-2.5) = " + str(abs(-2.5)));      // 2.5
console.log("abs(0) = " + str(abs(0)));            // 0

// Example 2: min() - Find minimum
console.log("\nExample 2: min() - Find minimum");
console.log("min(1, 2, 3) = " + str(min(1, 2, 3)));
console.log("min([5, 2, 8, 1]) = " + str(min([5, 2, 8, 1])));
console.log("min(-10, 5) = " + str(min(-10, 5)));
console.log("min([100, 50, 25]) = " + str(min([100, 50, 25])));

// Example 3: max() - Find maximum
console.log("\nExample 3: max() - Find maximum");
console.log("max(1, 2, 3) = " + str(max(1, 2, 3)));
console.log("max([5, 2, 8, 1]) = " + str(max([5, 2, 8, 1])));
console.log("max(-10, 5) = " + str(max(-10, 5)));
console.log("max([100, 50, 25]) = " + str(max([100, 50, 25])));

// Example 4: round() - Round numbers
console.log("\nExample 4: round() - Round to precision");
console.log("round(3.14159) = " + str(round(3.14159)));
console.log("round(3.14159, 2) = " + str(round(3.14159, 2)));
console.log("round(3.14159, 4) = " + str(round(3.14159, 4)));
console.log("round(2.5) = " + str(round(2.5)));
console.log("round(2.71828, 3) = " + str(round(2.71828, 3)));

// Example 5: sum() - Sum values
console.log("\nExample 5: sum() - Sum array values");
console.log("sum([1, 2, 3]) = " + str(sum([1, 2, 3])));
console.log("sum([1.5, 2.5, 3.0]) = " + str(sum([1.5, 2.5, 3.0])));
console.log("sum([1, 2, 3], 10) = " + str(sum([1, 2, 3], 10)));  // With start value
console.log("sum([]) = " + str(sum([])));

// Example 6: Statistical calculations
console.log("\nExample 6: Statistical calculations");
numbers = [23, 45, 67, 12, 89, 34, 56];

total = sum(numbers);
count = len(numbers);
average = total / count;
minimum = min(numbers);
maximum = max(numbers);

console.log("Numbers: " + str(numbers));
console.log("Count: " + str(count));
console.log("Sum: " + str(total));
console.log("Average: " + str(round(average, 2)));
console.log("Minimum: " + str(minimum));
console.log("Maximum: " + str(maximum));
console.log("Range: " + str(maximum - minimum));

// Example 7: Temperature analysis
console.log("\nExample 7: Temperature analysis");
temperatures = [72, 68, 75, 71, 69, 73, 70];

avgTemp = sum(temperatures) / len(temperatures);
minTemp = min(temperatures);
maxTemp = max(temperatures);

console.log("Daily temperatures: " + str(temperatures));
console.log("Average: " + str(round(avgTemp, 1)) + "°F");
console.log("Coldest: " + str(minTemp) + "°F");
console.log("Warmest: " + str(maxTemp) + "°F");
console.log("Variation: " + str(maxTemp - minTemp) + "°F");

// Example 8: Distance calculation
console.log("\nExample 8: Distance calculations");
function distance(x1, y1, x2, y2) {
    dx = x2 - x1;
    dy = y2 - y1;
    // Using abs for component distances
    absX = abs(dx);
    absY = abs(dy);
    return absX + absY;  // Manhattan distance
}

points = [
    {x: 0, y: 0, name: "Origin"},
    {x: 3, y: 4, name: "Point A"},
    {x: -2, y: 5, name: "Point B"}
];

console.log("Distances from origin:");
for (point in points) {
    dist = distance(0, 0, point.x, point.y);
    console.log("  " + point.name + " (" + str(point.x) + ", " + str(point.y) + "): " + str(dist));
}

// Example 9: Financial calculations
console.log("\nExample 9: Financial calculations");
expenses = [120.50, 45.99, 200.00, 67.25, 89.99];

totalExpenses = sum(expenses);
avgExpense = totalExpenses / len(expenses);
largestExpense = max(expenses);
smallestExpense = min(expenses);

console.log("Expenses: " + str(expenses));
console.log("Total: $" + str(round(totalExpenses, 2)));
console.log("Average: $" + str(round(avgExpense, 2)));
console.log("Largest: $" + str(largestExpense));
console.log("Smallest: $" + str(smallestExpense));

// Example 10: Grade analysis
console.log("\nExample 10: Grade analysis");
scores = [85, 92, 78, 95, 88, 76, 91];

total = sum(scores);
count = len(scores);
average = total / count;
highest = max(scores);
lowest = min(scores);

console.log("Scores: " + str(scores));
console.log("Total points: " + str(total));
console.log("Average score: " + str(round(average, 1)));
console.log("Highest score: " + str(highest));
console.log("Lowest score: " + str(lowest));

// Determine letter grade
if (average >= 90) {
    letterGrade = "A";
} elif (average >= 80) {
    letterGrade = "B";
} elif (average >= 70) {
    letterGrade = "C";
} else {
    letterGrade = "D";
}
console.log("Letter grade: " + letterGrade);

// Example 11: Combining multiple math functions
console.log("\nExample 11: Data normalization");
data = [100, 150, 200, 125, 175];

minVal = min(data);
maxVal = max(data);
rangeVal = maxVal - minVal;

console.log("Original data: " + str(data));
console.log("Min: " + str(minVal) + ", Max: " + str(maxVal) + ", Range: " + str(rangeVal));

// Normalize to 0-1 range
normalized = [];
for (value in data) {
    if (rangeVal > 0) {
        normalizedValue = (value - minVal) / rangeVal;
        normalized = normalized + [round(normalizedValue, 2)];
    } else {
        normalized = normalized + [0.0];
    }
}

console.log("Normalized (0-1): " + str(normalized));

console.log("\n=== Math Functions Complete ===");
