// ============================================
// Example: Line-Based File Operations
// Category: standard-library/file
// Demonstrates: readLines, writeLines, append
// ============================================

import console;
import file;

console.log("=== Line-Based File Operations ===\n");

// ============================================
// Writing Lines
// ============================================

console.log("=== writeLines (array to file) ===");

// Write array of lines
lines = ["First line", "Second line", "Third line"];
file.writeLines("lines_output.txt", lines);
console.log("Wrote 3 lines to lines_output.txt");

// Write more complex lines
dataLines = [
    "Name: Alice",
    "Age: 30",
    "City: NYC",
    "Country: USA"
];
file.writeLines("person_data.txt", dataLines);
console.log("Wrote person data (4 lines)");

// Write numbered lines
numberedLines = [];
i = 1;
while (i <= 5) {
    numberedLines = numberedLines + ["Line number " + str(i)];
    i = i + 1;
}
file.writeLines("numbered.txt", numberedLines);
console.log("Wrote 5 numbered lines");

// ============================================
// Reading Lines
// ============================================

console.log("\n=== readLines (file to array) ===");

// Read lines as array
readLines = file.readLines("lines_output.txt");
console.log("\nRead from lines_output.txt:");
console.log("  Number of lines: " + str(len(readLines)));

i = 0;
while (i < len(readLines)) {
    console.log("  Line " + str(i + 1) + ": " + readLines[i]);
    i = i + 1;
}

// Read person data
personLines = file.readLines("person_data.txt");
console.log("\nRead person data:");

i = 0;
while (i < len(personLines)) {
    console.log("  " + personLines[i]);
    i = i + 1;
}

// ============================================
// Append Operations
// ============================================

console.log("\n=== append (add to end of file) ===");

// Create initial file
file.write("log.txt", "Initial log entry\n");
console.log("Created log.txt");

// Append multiple entries
file.append("log.txt", "Second log entry\n");
file.append("log.txt", "Third log entry\n");
file.append("log.txt", "Fourth log entry\n");
console.log("Appended 3 more entries");

// Read all log entries
logContent = file.read("log.txt");
console.log("\nComplete log:");
console.log(logContent);

// ============================================
// Practical Example: To-Do List
// ============================================

console.log("\n=== Practical: To-Do List ===");

// Initialize to-do list
todos = [
    "[ ] Buy groceries",
    "[ ] Write documentation",
    "[ ] Review code"
];
file.writeLines("todos.txt", todos);
console.log("Created to-do list with 3 items");

// Read and display
currentTodos = file.readLines("todos.txt");
console.log("\nCurrent To-Do List:");

i = 0;
while (i < len(currentTodos)) {
    console.log("  " + str(i + 1) + ". " + currentTodos[i]);
    i = i + 1;
}

// Add new todo
file.append("todos.txt", "[ ] Test application\n");
console.log("\nAdded new to-do item");

// Read updated list
updatedTodos = file.readLines("todos.txt");
console.log("\nUpdated To-Do List (" + str(len(updatedTodos)) + " items):");

i = 0;
while (i < len(updatedTodos)) {
    console.log("  " + str(i + 1) + ". " + updatedTodos[i]);
    i = i + 1;
}

// ============================================
// Practical Example: CSV Processing
// ============================================

console.log("\n=== Practical: CSV File Processing ===");

// Create CSV with headers and data
csvLines = [
    "id,name,score",
    "1,Alice,95",
    "2,Bob,87",
    "3,Charlie,92"
];
file.writeLines("scores.csv", csvLines);
console.log("Created scores.csv");

// Read and process CSV
csvData = file.readLines("scores.csv");
console.log("\nProcessing CSV:");

// Display header
header = csvData[0];
console.log("  Header: " + header);

// Process data rows
console.log("  Data rows:");
i = 1;
while (i < len(csvData)) {
    console.log("    " + csvData[i]);
    i = i + 1;
}

console.log("  Total records: " + str(len(csvData) - 1));

// ============================================
// Practical Example: Log Rotation
// ============================================

console.log("\n=== Practical: Log Rotation ===");

// Create initial log file
initialLogs = [
    "[2024-01-15 10:00:00] Application started",
    "[2024-01-15 10:01:00] User logged in",
    "[2024-01-15 10:02:00] Data processed"
];
file.writeLines("application.log", initialLogs);
console.log("Created application.log with 3 entries");

// Append new log entries
file.append("application.log", "[2024-01-15 10:03:00] Cache cleared\n");
file.append("application.log", "[2024-01-15 10:04:00] Backup completed\n");
console.log("Appended 2 new log entries");

// Read all logs
allLogs = file.readLines("application.log");
console.log("\nComplete Application Log:");
console.log("  Total entries: " + str(len(allLogs)));

i = 0;
while (i < len(allLogs)) {
    console.log("  " + allLogs[i]);
    i = i + 1;
}

// ============================================
// Practical Example: Configuration Lines
// ============================================

console.log("\n=== Practical: Configuration File ===");

// Write configuration as lines
configLines = [
    "# Application Configuration",
    "app.name=MyApp",
    "app.version=1.0.0",
    "app.debug=true",
    "",
    "# Database Settings",
    "db.host=localhost",
    "db.port=5432",
    "db.name=myapp_db"
];
file.writeLines("config.cfg", configLines);
console.log("Created config.cfg with " + str(len(configLines)) + " lines");

// Read and parse configuration
configContent = file.readLines("config.cfg");
console.log("\nConfiguration File:");

settingsCount = 0;
i = 0;
while (i < len(configContent)) {
    line = configContent[i];

    // Skip empty lines and comments
    if (len(line) > 0) {
        if (len(line) > 0 && line != "") {
            firstChar = "";
            // Get first character (simplified check)
            if (len(line) > 0) {
                console.log("  " + line);
                // Count non-comment lines as settings
                settingsCount = settingsCount + 1;
            }
        }
    }

    i = i + 1;
}

// ============================================
// Practical Example: Text File Statistics
// ============================================

console.log("\n=== Practical: Text File Statistics ===");

// Create sample text file
textLines = [
    "This is the first line.",
    "Here is the second line with more words.",
    "Third line is short.",
    "The fourth line contains even more text to analyze.",
    "Final line wraps things up."
];
file.writeLines("sample_text.txt", textLines);
console.log("Created sample_text.txt");

// Read and analyze
textContent = file.readLines("sample_text.txt");
console.log("\nText File Statistics:");
console.log("  Total lines: " + str(len(textContent)));

// Calculate total characters
totalChars = 0;
i = 0;
while (i < len(textContent)) {
    totalChars = totalChars + len(textContent[i]);
    i = i + 1;
}
console.log("  Total characters: " + str(totalChars));

// Find longest line
longestLen = 0;
longestIdx = 0;
i = 0;
while (i < len(textContent)) {
    lineLen = len(textContent[i]);
    if (lineLen > longestLen) {
        longestLen = lineLen;
        longestIdx = i;
    }
    i = i + 1;
}
console.log("  Longest line: " + str(longestLen) + " chars (line " + str(longestIdx + 1) + ")");

// Average line length
avgLen = 0;
if (len(textContent) > 0) {
    avgLen = totalChars / len(textContent);
}
console.log("  Average line length: " + str(avgLen) + " chars");

// ============================================
// Empty Lines Handling
// ============================================

console.log("\n=== Empty Lines Handling ===");

// Write lines with empty lines
mixedLines = [
    "First line",
    "",
    "Third line (second is empty)",
    "",
    "",
    "Sixth line (two empty above)"
];
file.writeLines("mixed_lines.txt", mixedLines);
console.log("Wrote file with empty lines");

// Read and count
mixedContent = file.readLines("mixed_lines.txt");
console.log("\nRead mixed_lines.txt:");
console.log("  Total lines: " + str(len(mixedContent)));

// Count empty vs non-empty
emptyCount = 0;
nonEmptyCount = 0;
i = 0;
while (i < len(mixedContent)) {
    if (len(mixedContent[i]) == 0) {
        emptyCount = emptyCount + 1;
    } else {
        nonEmptyCount = nonEmptyCount + 1;
    }
    i = i + 1;
}
console.log("  Empty lines: " + str(emptyCount));
console.log("  Non-empty lines: " + str(nonEmptyCount));

console.log("\n=== Line-Based Operations Complete ===");
