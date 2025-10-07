// ============================================
// Example: Data Processing
// Category: tutorial
// Demonstrates: Processing complex nested data structures
// ============================================

import console;

// Array of objects - student records
students = [
    {name: "Alice", grade: 85, subject: "Math"},
    {name: "Bob", grade: 92, subject: "Science"},
    {name: "Carol", grade: 78, subject: "Math"},
    {name: "Dave", grade: 88, subject: "Science"},
    {name: "Eve", grade: 95, subject: "Math"}
];

console.log("=== Student Records ===");
console.log("Total students: " + str(len(students)));

// Processing array of objects
console.log("");
console.log("=== All Students ===");
for (student in students) {
    console.log(student.name + ": " + str(student.grade) + " in " + student.subject);
}

// Filtering objects by property
function getHighScorers(studentList, threshold) {
    highScorers = [];
    for (student in studentList) {
        if (student.grade >= threshold) {
            highScorers = highScorers + [student];
        }
    }
    return highScorers;
}

console.log("");
console.log("=== High Scorers (>= 90) ===");
topStudents = getHighScorers(students, 90);
for (student in topStudents) {
    console.log(student.name + ": " + str(student.grade));
}

// Calculating statistics from objects
function calculateAverageGrade(studentList) {
    total = 0;
    count = len(studentList);
    for (student in studentList) {
        total = total + student.grade;
    }
    return total / count;
}

console.log("");
console.log("=== Grade Statistics ===");
average = calculateAverageGrade(students);
console.log("Average grade: " + str(average));

// Grouping by property
function groupBySubject(studentList) {
    mathStudents = [];
    scienceStudents = [];
    for (student in studentList) {
        if (student.subject == "Math") {
            mathStudents = mathStudents + [student];
        } else {
            scienceStudents = scienceStudents + [student];
        }
    }
    return {
        math: mathStudents,
        science: scienceStudents
    };
}

console.log("");
console.log("=== Students by Subject ===");
bySubject = groupBySubject(students);
console.log("Math students: " + str(len(bySubject.math)));
console.log("Science students: " + str(len(bySubject.science)));

// Object containing arrays
console.log("");
console.log("=== Course Information ===");
course = {
    name: "Introduction to ML",
    instructor: "Dr. Smith",
    students: ["Alice", "Bob", "Carol"],
    assignments: ["Homework 1", "Homework 2", "Project"],
    grades: [85, 90, 88]
};

console.log("Course: " + course.name);
console.log("Instructor: " + course.instructor);
console.log("Number of students: " + str(len(course.students)));
console.log("Number of assignments: " + str(len(course.assignments)));

// Processing nested data
console.log("");
console.log("=== Student Roster ===");
for (studentName in course.students) {
    console.log("- " + studentName);
}

// Complex nested structure
console.log("");
console.log("=== Department Data ===");
department = {
    name: "Computer Science",
    courses: [
        {
            code: "CS101",
            title: "Intro to Programming",
            enrolled: 45
        },
        {
            code: "CS201",
            title: "Data Structures",
            enrolled: 38
        },
        {
            code: "CS301",
            title: "Algorithms",
            enrolled: 32
        }
    ]
};

console.log("Department: " + department.name);
console.log("Courses offered: " + str(len(department.courses)));

totalEnrolled = 0;
for (course in department.courses) {
    console.log(course.code + " - " + course.title + ": " + str(course.enrolled) + " students");
    totalEnrolled = totalEnrolled + course.enrolled;
}
console.log("Total enrollment: " + str(totalEnrolled));

// Finding specific items in nested data
function findCourseByCode(courses, code) {
    for (course in courses) {
        if (course.code == code) {
            return course;
        }
    }
    return {code: "", title: "Not found", enrolled: 0};
}

console.log("");
console.log("=== Course Lookup ===");
found = findCourseByCode(department.courses, "CS201");
console.log("Found: " + found.code + " - " + found.title);
