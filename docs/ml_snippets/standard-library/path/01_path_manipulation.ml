// ============================================
// Example: Path Manipulation Operations
// Category: standard-library/path
// Demonstrates: join, dirname, basename, extname, split, normalize, relative, absolute
// ============================================

import console;
import path;

console.log("=== Path Manipulation Operations ===\n");

// ============================================
// Path Joining
// ============================================

console.log("=== Path Joining ===");

p1 = path.join("home", "user", "documents");
console.log("Join segments: " + p1);

p2 = path.join("data", "files", "report.txt");
console.log("Join file path: " + p2);

p3 = path.join("src", "mlpy", "stdlib");
console.log("Join module path: " + p3);

// Cross-platform path joining
projectPath = path.join("projects", "mlpy", "src", "main.ml");
console.log("Project path: " + projectPath);

// ============================================
// Path Components
// ============================================

console.log("\n=== Path Components ===");

fullPath = "/home/user/documents/report.pdf";

dirName = path.dirname(fullPath);
console.log("Directory: " + dirName);

baseName = path.basename(fullPath);
console.log("Filename: " + baseName);

ext = path.extname(fullPath);
console.log("Extension: " + ext);

// Extract components from different paths
paths = [
    "/data/files/config.json",
    "/logs/app.log",
    "/src/module.ml"
];

i = 0;
while (i < len(paths)) {
    p = paths[i];
    console.log("\nPath: " + p);
    console.log("  Dir: " + path.dirname(p));
    console.log("  File: " + path.basename(p));
    console.log("  Ext: " + path.extname(p));
    i = i + 1;
}

// ============================================
// Path Splitting
// ============================================

console.log("\n=== Path Splitting ===");

testPath = "/home/user/documents/reports/2024/summary.pdf";
parts = path.split(testPath);

console.log("Original: " + testPath);
console.log("Parts (" + str(len(parts)) + " components):");
i = 0;
while (i < len(parts)) {
    console.log("  [" + str(i) + "] " + parts[i]);
    i = i + 1;
}

// Split and analyze multiple paths
console.log("\nPath Analysis:");
testPaths = [
    "/var/log/app.log",
    "src/mlpy/main.ml",
    "/home/user/.config/app/settings.json"
];

i = 0;
while (i < len(testPaths)) {
    p = testPaths[i];
    components = path.split(p);
    console.log("\n" + p + " -> " + str(len(components)) + " parts");
    i = i + 1;
}

// ============================================
// Path Normalization
// ============================================

console.log("\n=== Path Normalization ===");

// Normalize removes redundant separators and resolves . and ..
messyPath1 = "/home//user/./documents/../files/data.txt";
clean1 = path.normalize(messyPath1);
console.log("Messy: " + messyPath1);
console.log("Clean: " + clean1);

messyPath2 = "src/./mlpy/../stdlib/./path.ml";
clean2 = path.normalize(messyPath2);
console.log("\nMessy: " + messyPath2);
console.log("Clean: " + clean2);

// Normalize multiple paths
console.log("\nNormalization examples:");
messyPaths = [
    "/data//files///config.json",
    "./src/../lib/module.ml",
    "/home/user/./documents/./report.pdf"
];

i = 0;
while (i < len(messyPaths)) {
    messy = messyPaths[i];
    clean = path.normalize(messy);
    console.log("  " + messy + " -> " + clean);
    i = i + 1;
}

// ============================================
// Absolute Paths
// ============================================

console.log("\n=== Absolute Paths ===");

// Convert relative paths to absolute
rel1 = "data/files/config.json";
abs1 = path.absolute(rel1);
console.log("Relative: " + rel1);
console.log("Absolute: " + abs1);

rel2 = "../reports/summary.pdf";
abs2 = path.absolute(rel2);
console.log("\nRelative: " + rel2);
console.log("Absolute: " + abs2);

// Check if paths are absolute
console.log("\nAbsolute path checks:");
testPathsAbs = [
    "/home/user/file.txt",
    "relative/path.txt",
    "/var/log/app.log",
    "data/config.json"
];

i = 0;
while (i < len(testPathsAbs)) {
    p = testPathsAbs[i];
    isAbs = path.isAbsolute(p);
    console.log("  " + p + " -> " + str(isAbs));
    i = i + 1;
}

// ============================================
// Relative Paths
// ============================================

console.log("\n=== Relative Paths ===");

// Get relative path from one location to another
from1 = "/home/user/projects/mlpy/src";
to1 = "/home/user/projects/mlpy/docs/guide.md";
rel = path.relative(from1, to1);
console.log("From: " + from1);
console.log("To: " + to1);
console.log("Relative: " + rel);

// Different base directories
from2 = "/var/www/html";
to2 = "/var/www/html/assets/images/logo.png";
rel2 = path.relative(from2, to2);
console.log("\nFrom: " + from2);
console.log("To: " + to2);
console.log("Relative: " + rel2);

// ============================================
// Path Utilities
// ============================================

console.log("\n=== Path Utilities ===");

// Get current working directory
cwd = path.cwd();
console.log("Current directory: " + cwd);

// Get home directory
homeDir = path.home();
console.log("Home directory: " + homeDir);

// Get temp directory
tmpDir = path.tempDir();
console.log("Temp directory: " + tmpDir);

// Get OS-specific separators
sep = path.separator();
console.log("Path separator: '" + sep + "'");

delim = path.delimiter();
console.log("Path delimiter: '" + delim + "'");

// ============================================
// Building Paths with Utilities
// ============================================

console.log("\n=== Building Paths ===");

// Build config path in home directory
configPath = path.join(homeDir, ".config", "myapp", "settings.json");
console.log("Config path: " + configPath);

// Build temp file path
tempFile = path.join(tmpDir, "data-" + str(123) + ".tmp");
console.log("Temp file: " + tempFile);

// Build log path
logPath = path.join(cwd, "logs", "app.log");
console.log("Log path: " + logPath);

// ============================================
// Path Manipulation Pipeline
// ============================================

console.log("\n=== Path Pipeline ===");

// Complete path manipulation workflow
originalPath = "../data//files/./reports/../config.json";

console.log("Original: " + originalPath);

// Step 1: Normalize
normalized = path.normalize(originalPath);
console.log("1. Normalized: " + normalized);

// Step 2: Make absolute
absolute = path.absolute(normalized);
console.log("2. Absolute: " + absolute);

// Step 3: Extract components
dir = path.dirname(absolute);
file = path.basename(absolute);
extension = path.extname(absolute);

console.log("3. Components:");
console.log("   Directory: " + dir);
console.log("   Filename: " + file);
console.log("   Extension: " + extension);

// ============================================
// Working with Multiple Paths
// ============================================

console.log("\n=== Multiple Path Operations ===");

// Process array of paths
filePaths = [
    "src/main.ml",
    "lib/utils.ml",
    "tests/test_main.ml"
];

console.log("Converting to absolute paths:");
i = 0;
while (i < len(filePaths)) {
    rel = filePaths[i];
    abs = path.absolute(rel);
    console.log("  " + rel + " -> " + abs);
    i = i + 1;
}

// Extract all extensions
console.log("\nFile extensions:");
i = 0;
while (i < len(filePaths)) {
    p = filePaths[i];
    ext = path.extname(p);
    console.log("  " + p + " -> " + ext);
    i = i + 1;
}

// ============================================
// Path Validation Patterns
// ============================================

console.log("\n=== Path Validation ===");

// Check path properties
testPath2 = "/home/user/documents/report.pdf";

console.log("Path: " + testPath2);
console.log("  Is absolute: " + str(path.isAbsolute(testPath2)));
console.log("  Directory: " + path.dirname(testPath2));
console.log("  Filename: " + path.basename(testPath2));
console.log("  Extension: " + path.extname(testPath2));

// Build safe path
basePath = "/data/files";
userInput = "../../../etc/passwd";  // Potentially dangerous
safePath = path.normalize(path.join(basePath, userInput));
console.log("\nSafe path construction:");
console.log("  Base: " + basePath);
console.log("  Input: " + userInput);
console.log("  Safe result: " + safePath);

console.log("\n=== Path Manipulation Complete ===");
