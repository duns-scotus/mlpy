// ============================================
// Example: Comprehensive Built-in Functions
// Category: language-reference/builtin
// Demonstrates: Multiple built-ins working together in practical application
// ============================================

import console;

console.log("=== Student Performance Analysis System ===\n");

// Student database
students = [
    {id: 1, name: "Alice Johnson", scores: [85, 92, 78, 95, 88]},
    {id: 2, name: "Bob Smith", scores: [72, 68, 75, 70, 73]},
    {id: 3, name: "Carol Davis", scores: [95, 98, 94, 96, 97]},
    {id: 4, name: "David Lee", scores: [45, 52, 48, 50, 47]},
    {id: 5, name: "Eve Martinez", scores: [88, 85, 90, 87, 89]}
];

// Function: Calculate statistics using math built-ins
function calculateStats(scores) {
    if (len(scores) == 0) {
        return null;
    }

    total = sum(scores);
    count = len(scores);
    average = total / count;
    minimum = min(scores);
    maximum = max(scores);

    return {
        total: total,
        count: count,
        average: round(average, 2),
        min: minimum,
        max: maximum,
        range: maximum - minimum
    };
}

// Function: Determine letter grade using conditional logic
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

// Function: Validate all scores using all()
function validateScores(scores) {
    validChecks = [];
    for (score in scores) {
        isValid = isinstance(score, "number") && score >= 0 && score <= 100;
        validChecks = validChecks + [isValid];
    }
    return all(validChecks);
}

// Function: Check if passing using any()
function hasPassingGrade(scores) {
    passingChecks = [];
    for (score in scores) {
        isPassing = score >= 60;
        passingChecks = passingChecks + [isPassing];
    }
    return any(passingChecks);
}

// Process each student
console.log("=== Individual Student Reports ===\n");

allStats = [];
for (student in students) {
    console.log("Student ID: " + str(student.id));
    console.log("Name: " + student.name);

    // Type checking
    if (!isinstance(student.scores, "array")) {
        console.log("ERROR: Invalid scores data");
        continue;
    }

    // Validation
    if (!validateScores(student.scores)) {
        console.log("ERROR: Invalid scores detected");
        continue;
    }

    // Statistics
    stats = calculateStats(student.scores);
    grade = getLetterGrade(stats.average);

    console.log("Scores: " + str(student.scores));
    console.log("Statistics:");
    console.log("  Total Points: " + str(stats.total));
    console.log("  Average: " + str(stats.average));
    console.log("  Min Score: " + str(stats.min));
    console.log("  Max Score: " + str(stats.max));
    console.log("  Range: " + str(stats.range));
    console.log("  Letter Grade: " + grade);
    console.log("  Passing: " + str(hasPassingGrade(student.scores)));
    console.log("");

    // Store for class analysis
    allStats = allStats + [{
        student: student,
        stats: stats,
        grade: grade
    }];
}

// Class-wide analysis
console.log("=== Class-Wide Analysis ===\n");

// Collect all averages
allAverages = [];
for (record in allStats) {
    allAverages = allAverages + [record.stats.average];
}

// Class statistics
classStats = calculateStats(allAverages);
console.log("Class Statistics:");
console.log("  Students: " + str(len(students)));
console.log("  Class Average: " + str(classStats.average));
console.log("  Highest Average: " + str(classStats.max));
console.log("  Lowest Average: " + str(classStats.min));

// Grade distribution using sorted()
console.log("\n=== Grade Distribution ===");
sortedByAverage = sorted(allAverages, true);  // Descending

gradeCount = {A: 0, B: 0, C: 0, D: 0, F: 0};
for (avg in allAverages) {
    grade = getLetterGrade(avg);
    if (grade == "A") {
        gradeCount.A = gradeCount.A + 1;
    } elif (grade == "B") {
        gradeCount.B = gradeCount.B + 1;
    } elif (grade == "C") {
        gradeCount.C = gradeCount.C + 1;
    } elif (grade == "D") {
        gradeCount.D = gradeCount.D + 1;
    } else {
        gradeCount.F = gradeCount.F + 1;
    }
}

console.log("A: " + str(gradeCount.A) + " students");
console.log("B: " + str(gradeCount.B) + " students");
console.log("C: " + str(gradeCount.C) + " students");
console.log("D: " + str(gradeCount.D) + " students");
console.log("F: " + str(gradeCount.F) + " students");

// Top performers
console.log("\n=== Top Performers ===");
topThree = sorted(allAverages, true);
if (len(topThree) > 3) {
    topThree = [topThree[0], topThree[1], topThree[2]];
}

rank = 1;
for (avg in topThree) {
    // Find student with this average
    for (record in allStats) {
        if (record.stats.average == avg) {
            console.log(str(rank) + ". " + record.student.name + " - " + str(avg) + " (" + record.grade + ")");
            rank = rank + 1;
            break;
        }
    }
}

// Students needing help
console.log("\n=== Students Needing Support ===");
needsHelp = [];
for (record in allStats) {
    if (record.stats.average < 70) {
        needsHelp = needsHelp + [record];
    }
}

if (len(needsHelp) == 0) {
    console.log("All students performing satisfactorily!");
} else {
    for (record in needsHelp) {
        console.log("  " + record.student.name + " - Average: " + str(record.stats.average));
    }
}

// Perfect scores analysis
console.log("\n=== Perfect Scores (100) ===");
perfectScoreCount = 0;
for (student in students) {
    studentHasPerfect = false;
    for (score in student.scores) {
        if (score == 100) {
            if (!studentHasPerfect) {
                console.log("  " + student.name);
                studentHasPerfect = true;
                perfectScoreCount = perfectScoreCount + 1;
            }
        }
    }
}

if (perfectScoreCount == 0) {
    console.log("  No perfect scores this period");
}

// Score improvement analysis
console.log("\n=== Score Trends ===");
for (student in students) {
    scores = student.scores;
    if (len(scores) >= 2) {
        firstScore = scores[0];
        lastScore = scores[len(scores) - 1];
        change = lastScore - firstScore;

        trend = "->";
        if (change > 0) {
            trend = "UP";
        } elif (change < 0) {
            trend = "DOWN";
        }

        console.log(student.name + ": " + str(firstScore) + " " + trend + " " + str(lastScore) + " (change: " + str(change) + ")");
    }
}

// Attendance and performance correlation
console.log("\n=== Data Validation Summary ===");
validDataCount = 0;
invalidDataCount = 0;

for (student in students) {
    if (validateScores(student.scores)) {
        validDataCount = validDataCount + 1;
    } else {
        invalidDataCount = invalidDataCount + 1;
    }
}

console.log("Valid records: " + str(validDataCount));
console.log("Invalid records: " + str(invalidDataCount));
console.log("Data quality: " + str(round((validDataCount * 100.0) / len(students), 1)) + "%");

// Format ID badges using string conversion
console.log("\n=== Student ID Badges ===");
for (student in students) {
    // Format ID as 4-digit string
    idStr = str(student.id);
    while (len(idStr) < 4) {
        idStr = "0" + idStr;
    }

    stats = null;
    for (record in allStats) {
        if (record.student.id == student.id) {
            stats = record.stats;
            break;
        }
    }

    if (stats != null) {
        badge = "ID-" + idStr + " | " + student.name + " | Grade: " + getLetterGrade(stats.average);
        console.log(badge);
    }
}

// Summary using type checking
console.log("\n=== System Summary ===");
console.log("Data types validated:");
console.log("  students is " + typeof(students));
console.log("  First student is " + typeof(students[0]));
console.log("  First student name is " + typeof(students[0].name));
console.log("  First student scores is " + typeof(students[0].scores));

// Final statistics
console.log("\n=== Final Report ===");
console.log("Total students processed: " + str(len(students)));
console.log("Total scores analyzed: " + str(len(students) * len(students[0].scores)));
console.log("Class average: " + str(classStats.average));
console.log("Passing rate: " + str(round((len(allStats) - len(needsHelp)) * 100.0 / len(allStats), 1)) + "%");

console.log("\n=== Analysis Complete ===");
