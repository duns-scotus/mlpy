// ============================================
// Example: Comprehensive File Processing System
// Category: standard-library/file
// Demonstrates: Complete file I/O workflows, data processing, backup systems
// ============================================

import console;
import file;

console.log("=== Comprehensive File Processing System ===\n");

// ============================================
// System 1: Configuration Manager
// ============================================

console.log("=== Configuration Manager ===");

function saveConfig(filename, appName, version, debug, maxConn) {
    configLines = [
        "# Application Configuration",
        "app_name=" + appName,
        "version=" + version,
        "debug=" + str(debug),
        "max_connections=" + str(maxConn)
    ];

    file.writeLines(filename, configLines);
    console.log("  Saved configuration to " + filename);
}

function loadConfig(filename) {
    if (!file.exists(filename)) {
        console.log("  Config file not found: " + filename);
        return null;
    }

    lines = file.readLines(filename);
    console.log("  Loaded " + str(len(lines)) + " configuration lines");

    return lines;
}

// Create and save configuration
saveConfig("app_config.txt", "MyApp", "1.0.0", true, 100);

// Load configuration
configData = loadConfig("app_config.txt");
if (configData != null) {
    console.log("  Configuration loaded successfully");
}

// ============================================
// System 2: Data Logger
// ============================================

console.log("\n=== Data Logger ===");

function initializeLog(logFile) {
    if (!file.exists(logFile)) {
        file.write(logFile, "");
        console.log("  Initialized new log: " + logFile);
    } else {
        console.log("  Log exists: " + logFile);
    }
}

function logMessage(logFile, level, message) {
    entry = "[" + level + "] " + message + "\n";
    file.append(logFile, entry);
}

function getLogSize(logFile) {
    if (file.exists(logFile)) {
        return file.size(logFile);
    }
    return 0;
}

// Initialize logging system
logFilename = "application.log";
initializeLog(logFilename);

// Log various messages
logMessage(logFilename, "INFO", "Application started");
logMessage(logFilename, "INFO", "User logged in");
logMessage(logFilename, "WARN", "High memory usage detected");
logMessage(logFilename, "INFO", "Data processed successfully");
logMessage(logFilename, "ERROR", "Connection timeout");

// Check log size
logSize = getLogSize(logFilename);
console.log("  Current log size: " + str(logSize) + " bytes");

// Display log
logContents = file.read(logFilename);
console.log("\n  Log contents:");
console.log(logContents);

// ============================================
// System 3: Backup Manager
// ============================================

console.log("=== Backup Manager ===");

function createBackup(sourceFile, backupSuffix) {
    if (!file.exists(sourceFile)) {
        console.log("  Source file not found: " + sourceFile);
        return false;
    }

    backupFile = sourceFile + backupSuffix;
    file.copy(sourceFile, backupFile);
    console.log("  Backup created: " + backupFile);

    return true;
}

function verifyBackup(sourceFile, backupFile) {
    if (!file.exists(sourceFile) || !file.exists(backupFile)) {
        return false;
    }

    sourceSize = file.size(sourceFile);
    backupSize = file.size(backupFile);

    return sourceSize == backupSize;
}

// Create important data file
file.write("important_data.txt", "Critical business data\nLine 2\nLine 3\n");
console.log("  Created important_data.txt");

// Create backup
backupCreated = createBackup("important_data.txt", ".backup");

// Verify backup
if (backupCreated) {
    verified = verifyBackup("important_data.txt", "important_data.txt.backup");
    console.log("  Backup verified: " + str(verified));
}

// ============================================
// System 4: CSV Data Processor
// ============================================

console.log("\n=== CSV Data Processor ===");

function createCSV(filename, headers, rows) {
    lines = [];
    lines = lines + [headers];

    i = 0;
    while (i < len(rows)) {
        lines = lines + [rows[i]];
        i = i + 1;
    }

    file.writeLines(filename, lines);
    console.log("  Created CSV: " + filename);
}

function readCSV(filename) {
    if (!file.exists(filename)) {
        console.log("  CSV not found: " + filename);
        return null;
    }

    lines = file.readLines(filename);
    console.log("  Read CSV: " + str(len(lines)) + " lines");

    return lines;
}

function countCSVRecords(filename) {
    data = readCSV(filename);
    if (data == null) {
        return 0;
    }

    // Subtract 1 for header row
    recordCount = len(data) - 1;
    if (recordCount < 0) {
        recordCount = 0;
    }

    return recordCount;
}

// Create sample CSV
console.log("  Creating employee CSV...");
csvHeaders = "id,name,department,salary";
csvRows = [
    "1,Alice,Engineering,95000",
    "2,Bob,Marketing,75000",
    "3,Charlie,Engineering,88000",
    "4,Diana,Sales,82000"
];
createCSV("employees.csv", csvHeaders, csvRows);

// Process CSV
csvData = readCSV("employees.csv");
recordCount = countCSVRecords("employees.csv");
console.log("  Employee records: " + str(recordCount));

// ============================================
// System 5: File Archive System
// ============================================

console.log("\n=== File Archive System ===");

function archiveFile(filename, archiveSuffix) {
    if (!file.exists(filename)) {
        console.log("  File not found: " + filename);
        return false;
    }

    archiveName = filename + archiveSuffix;
    file.move(filename, archiveName);
    console.log("  Archived: " + filename + " -> " + archiveName);

    return true;
}

function listArchives(baseFilename) {
    // In a real system, we'd scan directory
    // Here we'll just check a few known archives
    archives = [
        baseFilename + ".archive1",
        baseFilename + ".archive2",
        baseFilename + ".archive3"
    ];

    found = 0;
    i = 0;
    while (i < len(archives)) {
        if (file.exists(archives[i])) {
            found = found + 1;
        }
        i = i + 1;
    }

    return found;
}

// Create files to archive
file.write("report.txt", "Q1 Report data");
console.log("  Created report.txt");

// Archive the file
archiveFile("report.txt", ".archive1");

// Create new current report
file.write("report.txt", "Q2 Report data");
console.log("  Created new report.txt");

// Archive again
archiveFile("report.txt", ".archive2");

// Check archives
archiveCount = listArchives("report.txt");
console.log("  Total archives: " + str(archiveCount));

// ============================================
// System 6: Data Export System
// ============================================

console.log("\n=== Data Export System ===");

function exportData(data, format, filename) {
    if (format == "txt") {
        // Plain text export
        file.writeLines(filename, data);
        console.log("  Exported as TXT: " + filename);
    } elif (format == "csv") {
        // CSV export (simplified)
        file.writeLines(filename, data);
        console.log("  Exported as CSV: " + filename);
    } else {
        console.log("  Unknown format: " + format);
        return false;
    }

    return true;
}

function getExportSize(filename) {
    if (file.exists(filename)) {
        size = file.size(filename);
        console.log("  Export size: " + str(size) + " bytes");
        return size;
    }
    return 0;
}

// Prepare data for export
exportData1 = ["User 1", "User 2", "User 3", "User 4", "User 5"];

// Export as TXT
exportData(exportData1, "txt", "users_export.txt");
getExportSize("users_export.txt");

// Export as CSV
csvExportData = ["id,name", "1,User1", "2,User2", "3,User3"];
exportData(csvExportData, "csv", "users_export.csv");
getExportSize("users_export.csv");

// ============================================
// System 7: Log Rotation System
// ============================================

console.log("\n=== Log Rotation System ===");

function rotateLog(logFile, maxSize) {
    if (!file.exists(logFile)) {
        console.log("  Log file not found: " + logFile);
        return false;
    }

    currentSize = file.size(logFile);
    console.log("  Current log size: " + str(currentSize) + " bytes");

    if (currentSize >= maxSize) {
        // Rotate: move current log to archive
        archiveName = logFile + ".old";

        // Delete old archive if exists
        if (file.exists(archiveName)) {
            file.delete(archiveName);
        }

        // Move current log to archive
        file.move(logFile, archiveName);
        console.log("  Rotated: " + logFile + " -> " + archiveName);

        // Create new empty log
        file.write(logFile, "");
        console.log("  Created new: " + logFile);

        return true;
    } else {
        console.log("  Rotation not needed (size < " + str(maxSize) + ")");
        return false;
    }
}

// Create log and add entries
file.write("rotation_test.log", "");
i = 0;
while (i < 10) {
    file.append("rotation_test.log", "Log entry " + str(i) + "\n");
    i = i + 1;
}

console.log("  Created test log with 10 entries");

// Try rotation with high threshold (shouldn't rotate)
rotateLog("rotation_test.log", 1000);

// Try rotation with low threshold (should rotate)
rotateLog("rotation_test.log", 50);

// ============================================
// System 8: File Statistics Dashboard
// ============================================

console.log("\n=== File Statistics Dashboard ===");

function generateStatistics() {
    console.log("  File System Statistics:");

    // Count files we've created
    testFiles = [
        "app_config.txt",
        "application.log",
        "important_data.txt",
        "employees.csv",
        "users_export.txt",
        "users_export.csv"
    ];

    totalFiles = 0;
    totalSize = 0;
    largestSize = 0;
    largestFile = "";

    i = 0;
    while (i < len(testFiles)) {
        filename = testFiles[i];

        if (file.exists(filename)) {
            totalFiles = totalFiles + 1;
            size = file.size(filename);
            totalSize = totalSize + size;

            if (size > largestSize) {
                largestSize = size;
                largestFile = filename;
            }
        }

        i = i + 1;
    }

    console.log("\n  Files tracked: " + str(totalFiles));
    console.log("  Total size: " + str(totalSize) + " bytes");

    if (totalFiles > 0) {
        avgSize = totalSize / totalFiles;
        console.log("  Average size: " + str(avgSize) + " bytes");
    }

    if (largestFile != "") {
        console.log("  Largest file: " + largestFile + " (" + str(largestSize) + " bytes)");
    }
}

generateStatistics();

// ============================================
// System 9: Data Validation System
// ============================================

console.log("\n=== Data Validation System ===");

function validateDataFile(filename, minSize, maxSize) {
    console.log("  Validating: " + filename);

    // Check existence
    if (!file.exists(filename)) {
        console.log("    FAIL: File does not exist");
        return false;
    }

    // Check type
    if (!file.isFile(filename)) {
        console.log("    FAIL: Not a file");
        return false;
    }

    // Check size
    size = file.size(filename);
    if (size < minSize) {
        console.log("    FAIL: Too small (" + str(size) + " < " + str(minSize) + ")");
        return false;
    }

    if (size > maxSize) {
        console.log("    FAIL: Too large (" + str(size) + " > " + str(maxSize) + ")");
        return false;
    }

    console.log("    PASS: Valid file (" + str(size) + " bytes)");
    return true;
}

// Create test files
file.write("valid_data.txt", "This is valid data");
file.write("too_small.txt", "x");
file.write("too_large.txt", "This is a very large file with lots and lots of content that exceeds the maximum size limit");

// Validate files
validateDataFile("valid_data.txt", 10, 100);
validateDataFile("too_small.txt", 10, 100);
validateDataFile("too_large.txt", 10, 50);

// ============================================
// System 10: Cleanup Manager
// ============================================

console.log("\n=== Cleanup Manager ===");

function cleanupTemporaryFiles() {
    console.log("  Cleaning up temporary files...");

    // List of temp files to clean
    tempFiles = [
        "test_output.txt",
        "multiline.txt",
        "binary_test.bin",
        "config.txt",
        "empty.txt"
    ];

    cleaned = 0;
    i = 0;
    while (i < len(tempFiles)) {
        filename = tempFiles[i];

        if (file.exists(filename)) {
            file.delete(filename);
            cleaned = cleaned + 1;
        }

        i = i + 1;
    }

    console.log("  Cleaned " + str(cleaned) + " temporary files");
}

// Perform cleanup
cleanupTemporaryFiles();

// ============================================
// Summary
// ============================================

console.log("\n=== System Summary ===");

console.log("Demonstrated systems:");
console.log("  1. Configuration Manager - Save/load app settings");
console.log("  2. Data Logger - Structured logging with levels");
console.log("  3. Backup Manager - File backup and verification");
console.log("  4. CSV Processor - Structured data import/export");
console.log("  5. Archive System - Historical file management");
console.log("  6. Export System - Multi-format data export");
console.log("  7. Log Rotation - Size-based log management");
console.log("  8. Statistics Dashboard - File system analytics");
console.log("  9. Validation System - Data integrity checks");
console.log("  10. Cleanup Manager - Temporary file management");

console.log("\nCapabilities demonstrated:");
console.log("  - Reading: text, lines, binary");
console.log("  - Writing: text, lines, append");
console.log("  - Management: copy, move, delete, exists");
console.log("  - Information: size, type checking");
console.log("  - Workflows: backup, archive, rotation, validation");

console.log("\n=== Comprehensive File Processing Complete ===");
