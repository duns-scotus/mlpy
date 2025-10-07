// ============================================
// Example: Comprehensive Control Flow
// Category: language-reference/control-flow
// Demonstrates: Multiple control flow patterns in practical context
// ============================================

import console;

console.log("=== Student Grade Analysis System ===\n");

// Student data
students = [
    {name: "Alice", scores: [85, 90, 78, 92]},
    {name: "Bob", scores: [70, 75, 68, 72]},
    {name: "Carol", scores: [95, 98, 94, 96]},
    {name: "David", scores: [45, 50, 48, 52]},
    {name: "Eve", scores: [88, 85, 90, 87]}
];

// Function to calculate average
function calculateAverage(scores) {
    if (len(scores) == 0) {
        throw {message: "Cannot calculate average of empty scores"};
    }

    totalVal = 0;
    for (score in scores) {
        totalVal = totalVal + score;
    }
    return totalVal / len(scores);
}

// Function to determine letter grade
function getLetterGrade(average) {
    if (average >= 90) {
        return "A";
    } elif (average >= 80) {
        return "B";
    } elif (average >= 70) {
        return "C";
    } elif (average >= 60) {
        return "D";
    } else {
        return "F";
    }
}

// Process each student
console.log("Student Report:");
console.log("=" * 50);

passCount = 0;
failCount = 0;
highestAverage = 0;
topStudent = "";

for (student in students) {
    try {
        // Calculate average
        average = calculateAverage(student.scores);

        // Determine grade
        grade = getLetterGrade(average);

        // Track pass/fail
        if (average >= 60) {
            passCount = passCount + 1;
        } else {
            failCount = failCount + 1;
        }

        // Track top student
        if (average > highestAverage) {
            highestAverage = average;
            topStudent = student.name;
        }

        // Print student report
        console.log(student.name + ":");
        console.log("  Scores: " + str(student.scores));
        console.log("  Average: " + str(average));
        console.log("  Grade: " + grade);
        console.log("");

    } except (err) {
        console.log("Error processing " + student.name);
        failCount = failCount + 1;
    }
}

// Summary statistics
console.log("=" * 50);
console.log("Summary:");
console.log("  Total students: " + str(len(students)));
console.log("  Passed: " + str(passCount));
console.log("  Failed: " + str(failCount));
console.log("  Top student: " + topStudent + " (" + str(highestAverage) + ")");

// Find students who need improvement
console.log("\nStudents needing improvement:");
needsHelp = [];
for (student in students) {
    average = calculateAverage(student.scores);
    if (average < 70) {
        needsHelp = needsHelp + [student.name];
    }
}

if (len(needsHelp) == 0) {
    console.log("  All students performing well!");
} else {
    for (name in needsHelp) {
        console.log("  - " + name);
    }
}

// Check for perfect scores
console.log("\nPerfect scores (100):");
foundPerfect = false;
for (student in students) {
    for (score in student.scores) {
        if (score == 100) {
            console.log("  " + student.name);
            foundPerfect = true;
            break;
        }
    }
}

if (!foundPerfect) {
    console.log("  No perfect scores this period");
}

console.log("\n=== Analysis Complete ===");
