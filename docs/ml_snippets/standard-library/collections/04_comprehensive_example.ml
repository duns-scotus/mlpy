// ============================================
// Comprehensive Example: Student Analytics System
// Category: standard-library/collections
// Demonstrates: Complete collections module in data analysis pipeline
// ============================================

import console;
import collections;

console.log("=== Student Analytics System ===\n");

// ============================================
// Dataset: Student Records
// ============================================

students = [
    {name: "Alice", grade: 92, age: 20, major: "CS"},
    {name: "Bob", grade: 78, age: 21, major: "Math"},
    {name: "Charlie", grade: 85, age: 19, major: "CS"},
    {name: "David", grade: 67, age: 22, major: "Physics"},
    {name: "Eve", grade: 95, age: 20, major: "Math"},
    {name: "Frank", grade: 88, age: 21, major: "CS"},
    {name: "Grace", grade: 72, age: 19, major: "Physics"},
    {name: "Henry", grade: 91, age: 20, major: "Math"}
];

console.log("Total students: " + str(collections.length(students)));

// ============================================
// Filter: Find High Achievers
// ============================================

console.log("\n=== High Achievers (Grade >= 90) ===");

function isHighAchiever(student) {
    return student.grade >= 90;
}

highAchievers = collections.filter(students, isHighAchiever);
console.log("Count: " + str(collections.length(highAchievers)));

function getStudentName(student) {
    return student.name;
}

achieverNames = collections.map(highAchievers, getStudentName);
console.log("Names: " + str(achieverNames));

// ============================================
// Group by Major
// ============================================

console.log("\n=== Students by Major ===");

function isCS(student) {
    return student.major == "CS";
}
function isMath(student) {
    return student.major == "Math";
}
function isPhysics(student) {
    return student.major == "Physics";
}

csStudents = collections.filter(students, isCS);
mathStudents = collections.filter(students, isMath);
physicsStudents = collections.filter(students, isPhysics);

console.log("CS: " + str(collections.length(csStudents)) + " students");
console.log("Math: " + str(collections.length(mathStudents)) + " students");
console.log("Physics: " + str(collections.length(physicsStudents)) + " students");

// ============================================
// Calculate Statistics
// ============================================

console.log("\n=== Grade Statistics ===");

function getGrade(student) {
    return student.grade;
}

allGrades = collections.map(students, getGrade);
console.log("All grades: " + str(allGrades));

// Calculate average using reduce
function sumGrades(acc, grade) {
    return acc + grade;
}

totalGrades = collections.reduce(allGrades, sumGrades, 0);
averageGrade = totalGrades / collections.length(allGrades);
console.log("Average grade: " + str(round(averageGrade, 2)));

// Find min and max
sortedGrades = collections.sort(allGrades);
lowestGrade = collections.first(sortedGrades);
highestGrade = collections.last(sortedGrades);
console.log("Lowest grade: " + str(lowestGrade));
console.log("Highest grade: " + str(highestGrade));

// ============================================
// Age Analysis
// ============================================

console.log("\n=== Age Distribution ===");

function getAge(student) {
    return student.age;
}

ages = collections.map(students, getAge);
uniqueAges = collections.unique(ages);
sortedAges = collections.sort(uniqueAges);

console.log("Age range: " + str(collections.first(sortedAges)) + "-" + str(collections.last(sortedAges)) + " years");
console.log("Unique ages: " + str(sortedAges));

// ============================================
// Pass/Fail Analysis
// ============================================

console.log("\n=== Pass/Fail Analysis ===");

passingGrade = 70;

function isPassing(student) {
    return student.grade >= 70;
}
function isFailing(student) {
    return student.grade < 70;
}

passingStudents = collections.filter(students, isPassing);
failingStudents = collections.filter(students, isFailing);

console.log("Passing: " + str(collections.length(passingStudents)) + "/" + str(collections.length(students)));
console.log("Failing: " + str(collections.length(failingStudents)) + "/" + str(collections.length(students)));

// Check if all passed
allPassed = collections.every(students, isPassing);
console.log("All passed? " + str(allPassed));

// Check if any failed
anyFailed = collections.some(students, isFailing);
console.log("Any failed? " + str(anyFailed));

// ============================================
// Top Performers
// ============================================

console.log("\n=== Top 3 Performers ===");

function byGrade(student) {
    return student.grade;
}

// Sort by grade descending (sort ascending, then reverse)
sortedByGrade = collections.sortBy(students, byGrade);
descendingGrade = collections.reverse(sortedByGrade);
topThree = collections.take(descendingGrade, 3);

i = 0;
while (i < collections.length(topThree)) {
    student = collections.get(topThree, i);
    rank = i + 1;
    console.log(str(rank) + ". " + student.name + " - " + str(student.grade) + " (" + student.major + ")");
    i = i + 1;
}

// ============================================
// Major Performance Comparison
// ============================================

console.log("\n=== Average Grade by Major ===");

csGrades = collections.map(csStudents, getGrade);
mathGrades = collections.map(mathStudents, getGrade);
physicsGrades = collections.map(physicsStudents, getGrade);

csAvg = collections.reduce(csGrades, sumGrades, 0) / collections.length(csGrades);
mathAvg = collections.reduce(mathGrades, sumGrades, 0) / collections.length(mathGrades);
physicsAvg = collections.reduce(physicsGrades, sumGrades, 0) / collections.length(physicsGrades);

console.log("CS average: " + str(round(csAvg, 1)));
console.log("Math average: " + str(round(mathAvg, 1)));
console.log("Physics average: " + str(round(physicsAvg, 1)));

// ============================================
// Data Transformation Pipeline
// ============================================

console.log("\n=== Data Transformation Pipeline ===");
console.log("Pipeline: Filter CS students -> Sort by grade -> Take top 2 -> Extract names");

// Step 1: Filter CS students
step1 = collections.filter(students, isCS);
console.log("Step 1 - CS students: " + str(collections.length(step1)));

// Step 2: Sort by grade
step2 = collections.sortBy(step1, byGrade);
step2 = collections.reverse(step2);
console.log("Step 2 - Sorted by grade");

// Step 3: Take top 2
step3 = collections.take(step2, 2);
console.log("Step 3 - Top 2 CS students");

// Step 4: Extract names
step4 = collections.map(step3, getStudentName);
console.log("Result: " + str(step4));

// ============================================
// Grade Distribution (Chunking)
// ============================================

console.log("\n=== Grade Distribution ===");

sortedAllGrades = collections.sort(allGrades);
console.log("Sorted grades: " + str(sortedAllGrades));

// Group into ranges
gradeRanges = collections.chunk(sortedAllGrades, 3);
console.log("Grouped by 3: " + str(gradeRanges));

// ============================================
// Student Lookup
// ============================================

console.log("\n=== Student Lookup ===");

function findAlice(student) {
    return student.name == "Alice";
}

alice = collections.find(students, findAlice);
if (alice != null) {
    console.log("Found: " + alice.name + ", Grade: " + str(alice.grade));
}

// Check if student exists
function isDavid(student) {
    return student.name == "David";
}
hasDavid = collections.some(students, isDavid);
console.log("Has student named David? " + str(hasDavid));

// ============================================
// Summary Report
// ============================================

console.log("\n=== Summary Report ===");
console.log("Total Students: " + str(collections.length(students)));
console.log("Average Grade: " + str(round(averageGrade, 2)));
console.log("Grade Range: " + str(lowestGrade) + " - " + str(highestGrade));
console.log("Passing Rate: " + str(round(collections.length(passingStudents) * 100 / collections.length(students), 1)) + "%");
console.log("High Achievers (>=90): " + str(collections.length(highAchievers)));
console.log("Top Performer: " + collections.first(topThree).name + " (" + str(collections.first(topThree).grade) + ")");

console.log("\n=== Student Analytics Complete ===");
