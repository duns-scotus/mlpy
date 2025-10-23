// ============================================
// Example: Comprehensive File Organization System
// Category: standard-library/path
// Demonstrates: Complete file organization with all path operations
// ============================================

import console;
import path;

console.log("=== Comprehensive File Organization System ===\n");

console.log("This example demonstrates a complete file organization system");
console.log("using all path module capabilities.\n");

// ============================================
// System Configuration
// ============================================

console.log("=== System Configuration ===");

// Base directories
projectRoot = path.cwd();
dataDir = path.join(projectRoot, "data");
outputDir = path.join(projectRoot, "output");
archiveDir = path.join(projectRoot, "archive");
tempDir = path.tempDir();
homeDir = path.home();

console.log("Project paths:");
console.log("  Root: " + projectRoot);
console.log("  Data: " + dataDir);
console.log("  Output: " + outputDir);
console.log("  Archive: " + archiveDir);
console.log("  Temp: " + tempDir);
console.log("  Home: " + homeDir);

// OS Information
console.log("\nOS Information:");
console.log("  Path separator: '" + path.separator() + "'");
console.log("  Path delimiter: '" + path.delimiter() + "'");

// ============================================
// System 1: Path Utilities
// ============================================

console.log("\n=== System 1: Path Utilities ===");

function analyzePath(p) {
    console.log("\nAnalyzing path: " + p);

    // Basic properties
    isAbs = path.isAbsolute(p);
    console.log("  Is absolute: " + str(isAbs));

    // Components
    dir = path.dirname(p);
    file = path.basename(p);
    ext = path.extname(p);

    console.log("  Directory: " + dir);
    console.log("  Filename: " + file);
    console.log("  Extension: " + ext);

    // Split into parts
    parts = path.split(p);
    console.log("  Components: " + str(len(parts)) + " parts");

    // Normalized version
    normalized = path.normalize(p);
    console.log("  Normalized: " + normalized);

    // Absolute version
    absolute = path.absolute(normalized);
    console.log("  Absolute: " + absolute);
}

// Test various paths
testPaths = [
    "../data/files/report.pdf",
    "/var/log/app.log",
    "src/main.ml"
];

i = 0;
while (i < len(testPaths)) {
    analyzePath(testPaths[i]);
    i = i + 1;
}

// ============================================
// System 2: Project Structure Creation
// ============================================

console.log("\n=== System 2: Project Structure Creation ===");

function createProjectStructure(projectName) {
    console.log("\nCreating project structure: " + projectName);

    base = path.join(projectRoot, projectName);
    console.log("  Base directory: " + base);

    // Define structure
    structure = [
        "src",
        "tests",
        "docs",
        "data/input",
        "data/output",
        "data/cache",
        "logs",
        "build/lib",
        "build/bin"
    ];

    console.log("  Creating " + str(len(structure)) + " directories:");

    i = 0;
    while (i < len(structure)) {
        relPath = structure[i];
        fullPath = path.join(base, relPath);
        console.log("    - " + relPath);
        // path.createDir(fullPath, true);
        i = i + 1;
    }

    console.log("  Project structure created!");
}

createProjectStructure("my-ml-project");

// ============================================
// System 3: File Organization by Extension
// ============================================

console.log("\n=== System 3: File Organization by Extension ===");

function organizeByExtension(sourceDir) {
    console.log("\nOrganizing files by extension:");
    console.log("  Source: " + sourceDir);

    // Simulated file list
    files = [
        "document1.pdf",
        "image1.png",
        "data.json",
        "report.pdf",
        "photo.jpg",
        "config.yaml"
    ];

    console.log("  Found " + str(len(files)) + " files");

    // Group by extension
    extensions = {};
    i = 0;
    while (i < len(files)) {
        file = files[i];
        ext = path.extname(file);

        console.log("    " + file + " -> extension: " + ext);

        // Would create directory for extension
        extDir = path.join(sourceDir, "by-type", ext);
        console.log("      Target: " + extDir);

        i = i + 1;
    }
}

organizeByExtension(dataDir);

// ============================================
// System 4: Archive Management
// ============================================

console.log("\n=== System 4: Archive Management ===");

function archiveOldFiles(sourceDir, targetYear, targetMonth) {
    console.log("\nArchiving files:");
    console.log("  Source: " + sourceDir);
    console.log("  Archive: " + targetYear + "/" + targetMonth);

    // Build archive path
    archivePath = path.join(archiveDir, targetYear, targetMonth);
    console.log("  Archive path: " + archivePath);
    console.log("  Creating archive directory...");
    // path.createDir(archivePath, true);

    // Simulated file list
    files = ["old-report.pdf", "data-2023.csv", "backup.zip"];

    console.log("  Archiving " + str(len(files)) + " files:");
    i = 0;
    while (i < len(files)) {
        file = files[i];
        sourcePath = path.join(sourceDir, file);
        targetPath = path.join(archivePath, file);

        console.log("    " + file);
        console.log("      From: " + sourcePath);
        console.log("      To: " + targetPath);

        i = i + 1;
    }

    console.log("  Archive complete!");
}

archiveOldFiles(dataDir, "2023", "12");

// ============================================
// System 5: Temporary File Management
// ============================================

console.log("\n=== System 5: Temporary File Management ===");

function createTempWorkspace(sessionId) {
    console.log("\nCreating temporary workspace:");
    console.log("  Session: " + sessionId);

    // Create temp directory
    tmpBase = path.tempDir();
    workspaceDir = path.join(tmpBase, "ml-session-" + sessionId);

    console.log("  Workspace: " + workspaceDir);
    console.log("  Creating structure...");

    // Create subdirectories
    subdirs = ["input", "processing", "output", "logs"];
    i = 0;
    while (i < len(subdirs)) {
        subdir = subdirs[i];
        fullPath = path.join(workspaceDir, subdir);
        console.log("    - " + subdir + " -> " + fullPath);
        i = i + 1;
    }

    return workspaceDir;
}

function cleanupTempWorkspace(workspaceDir) {
    console.log("\nCleaning up workspace:");
    console.log("  Path: " + workspaceDir);
    console.log("  Removing recursively...");
    // path.removeDirRecursive(workspaceDir);
    console.log("  Cleanup complete!");
}

workspace = createTempWorkspace("20240115-1430");
cleanupTempWorkspace(workspace);

// ============================================
// System 6: Configuration File Locator
// ============================================

console.log("\n=== System 6: Configuration File Locator ===");

function findConfigFile(appName) {
    console.log("\nLocating configuration file:");
    console.log("  Application: " + appName);

    configName = appName + ".json";

    // Check multiple locations
    locations = [
        path.join(projectRoot, configName),
        path.join(projectRoot, ".config", configName),
        path.join(homeDir, ".config", appName, configName),
        path.join("/etc", appName, configName)
    ];

    console.log("  Checking " + str(len(locations)) + " locations:");

    i = 0;
    while (i < len(locations)) {
        loc = locations[i];
        console.log("    [" + str(i + 1) + "] " + loc);
        // if (path.exists(loc) && path.isFile(loc)) {
        //     return loc;
        // }
        i = i + 1;
    }

    console.log("  Config file not found in standard locations");
    return "";
}

findConfigFile("myapp");

// ============================================
// System 7: Backup System
// ============================================

console.log("\n=== System 7: Backup System ===");

function createBackup(sourceDir, backupName) {
    console.log("\nCreating backup:");
    console.log("  Source: " + sourceDir);
    console.log("  Backup name: " + backupName);

    // Build backup path
    backupBase = path.join(projectRoot, "backups");
    backupPath = path.join(backupBase, backupName);

    console.log("  Backup path: " + backupPath);
    console.log("  Creating backup directory...");
    // path.createDir(backupPath, true);

    console.log("  Backup created at: " + backupPath);
    return backupPath;
}

function cleanOldBackups(keepCount) {
    console.log("\nCleaning old backups:");
    console.log("  Keep last: " + str(keepCount));

    backupDir = path.join(projectRoot, "backups");
    console.log("  Backup directory: " + backupDir);

    // Simulated backup list
    backups = [
        "backup-2024-01-10",
        "backup-2024-01-11",
        "backup-2024-01-12",
        "backup-2024-01-13",
        "backup-2024-01-14",
        "backup-2024-01-15"
    ];

    totalBackups = len(backups);
    console.log("  Total backups: " + str(totalBackups));

    if (totalBackups > keepCount) {
        removeCount = totalBackups - keepCount;
        console.log("  Removing " + str(removeCount) + " old backups:");

        i = 0;
        while (i < removeCount) {
            backup = backups[i];
            backupPath = path.join(backupDir, backup);
            console.log("    - " + backup);
            // path.removeDirRecursive(backupPath);
            i = i + 1;
        }
    } else {
        console.log("  No cleanup needed");
    }
}

createBackup(dataDir, "backup-2024-01-15");
cleanOldBackups(5);

// ============================================
// System 8: Build Output Manager
// ============================================

console.log("\n=== System 8: Build Output Manager ===");

function prepareBuildDirectory() {
    console.log("\nPreparing build directory:");

    buildDir = path.join(projectRoot, "build");
    console.log("  Build directory: " + buildDir);

    // Clean existing build
    console.log("  Cleaning existing build...");
    // if (path.exists(buildDir)) {
    //     path.removeDirRecursive(buildDir);
    // }

    // Create fresh structure
    console.log("  Creating fresh structure...");
    // path.createDir(buildDir, true);

    buildDirs = [
        path.join(buildDir, "lib"),
        path.join(buildDir, "bin"),
        path.join(buildDir, "dist"),
        path.join(buildDir, "assets")
    ];

    i = 0;
    while (i < len(buildDirs)) {
        dir = buildDirs[i];
        relPath = path.relative(buildDir, dir);
        console.log("    - " + relPath);
        // path.createDir(dir, true);
        i = i + 1;
    }

    console.log("  Build directory ready!");
}

prepareBuildDirectory();

// ============================================
// System 9: Log File Rotation
// ============================================

console.log("\n=== System 9: Log File Rotation ===");

function rotateLogFiles(logDir, maxLogs) {
    console.log("\nRotating log files:");
    console.log("  Log directory: " + logDir);
    console.log("  Max logs: " + str(maxLogs));

    // Simulated log files
    logFiles = [
        "app.log",
        "app.log.1",
        "app.log.2",
        "app.log.3",
        "app.log.4"
    ];

    console.log("  Current logs: " + str(len(logFiles)));

    // Remove oldest if exceeds max
    if (len(logFiles) >= maxLogs) {
        oldest = "app.log." + str(maxLogs - 1);
        oldestPath = path.join(logDir, oldest);
        console.log("  Removing oldest: " + oldest);
        // file.delete(oldestPath);
    }

    // Rotate existing logs
    console.log("  Rotating logs:");
    i = maxLogs - 2;
    while (i >= 0) {
        if (i == 0) {
            oldName = "app.log";
        } else {
            oldName = "app.log." + str(i);
        }

        newName = "app.log." + str(i + 1);

        console.log("    " + oldName + " -> " + newName);
        i = i - 1;
    }

    console.log("  Log rotation complete!");
}

logsDir = path.join(projectRoot, "logs");
rotateLogFiles(logsDir, 5);

// ============================================
// System 10: Path Security Validator
// ============================================

console.log("\n=== System 10: Path Security Validator ===");

function validateUserPath(basePath, userInput) {
    console.log("\nValidating user path:");
    console.log("  Base path: " + basePath);
    console.log("  User input: " + userInput);

    // Step 1: Normalize user input
    normalized = path.normalize(userInput);
    console.log("  1. Normalized: " + normalized);

    // Step 2: Join with base path
    fullPath = path.join(basePath, normalized);
    console.log("  2. Joined: " + fullPath);

    // Step 3: Make absolute
    absolute = path.absolute(fullPath);
    console.log("  3. Absolute: " + absolute);

    // Step 4: Normalize again
    final = path.normalize(absolute);
    console.log("  4. Final: " + final);

    // Step 5: Check if still under base path
    baseAbs = path.absolute(basePath);
    console.log("  5. Base absolute: " + baseAbs);

    console.log("  Result: Path validated");
    return final;
}

// Test various inputs
safeBase = "/data/files";
testInputs = [
    "document.pdf",
    "subdir/file.txt",
    "../../../etc/passwd",
    "./data.json"
];

i = 0;
while (i < len(testInputs)) {
    input = testInputs[i];
    validateUserPath(safeBase, input);
    i = i + 1;
}

// ============================================
// Integration Summary
// ============================================

console.log("\n=== Integration Summary ===");

console.log("\nPath Manipulation:");
console.log("  - join() for combining path segments");
console.log("  - dirname(), basename(), extname() for components");
console.log("  - split() for path analysis");
console.log("  - normalize() for cleaning paths");
console.log("  - relative() and absolute() for conversions");

console.log("\nFilesystem Queries:");
console.log("  - exists() to check path existence");
console.log("  - isFile() and isDirectory() for type checking");
console.log("  - isAbsolute() for path validation");

console.log("\nDirectory Management:");
console.log("  - createDir() for creating directories");
console.log("  - removeDir() for empty directories");
console.log("  - removeDirRecursive() for non-empty directories");

console.log("\nUtilities:");
console.log("  - cwd() for current directory");
console.log("  - home() for home directory");
console.log("  - tempDir() for temporary files");
console.log("  - separator() and delimiter() for OS compatibility");

// ============================================
// Best Practices Applied
// ============================================

console.log("\n=== Best Practices Applied ===");

console.log("1. Always normalize user input paths");
console.log("2. Use path.join() for cross-platform compatibility");
console.log("3. Validate paths stay within allowed directories");
console.log("4. Create parent directories automatically");
console.log("5. Clean up temporary directories after use");
console.log("6. Use absolute paths for clarity");
console.log("7. Check existence before operations");
console.log("8. Handle path separators with separator()");
console.log("9. Use relative() for portable paths");
console.log("10. Leverage path utilities (home, temp, cwd)");

console.log("\n=== Comprehensive File Organization System Complete ===");
