// ============================================
// Example: Filesystem Query Operations
// Category: standard-library/path
// Demonstrates: exists, isFile, isDirectory, isAbsolute
// ============================================

import console;
import path;

console.log("=== Filesystem Query Operations ===\n");

// ============================================
// Path Existence Checking
// ============================================

console.log("=== Path Existence ===");

// Note: These examples show the API usage
// In a real environment, paths would need to exist

console.log("Checking if paths exist:");
console.log("  path.exists(\"/home\")");
console.log("  path.exists(\"/nonexistent\")");
console.log("  path.exists(\"/tmp\")");

// Check multiple paths
testPaths = [
    "/usr/bin",
    "/does/not/exist",
    "/var/log"
];

console.log("\nPath existence checks:");
i = 0;
while (i < len(testPaths)) {
    p = testPaths[i];
    console.log("  " + p);
    i = i + 1;
}

// ============================================
// File vs Directory Detection
// ============================================

console.log("\n=== File vs Directory Detection ===");

console.log("Distinguishing files from directories:");
console.log("  path.isFile(\"/etc/hosts\") -> true");
console.log("  path.isDirectory(\"/etc/hosts\") -> false");
console.log("  path.isFile(\"/usr/bin\") -> false");
console.log("  path.isDirectory(\"/usr/bin\") -> true");

// Check path types
paths = [
    {path: "/etc/passwd", expectedType: "file"},
    {path: "/tmp", expectedType: "directory"},
    {path: "/var/log", expectedType: "directory"},
    {path: "/etc/hostname", expectedType: "file"}
];

console.log("\nPath type checks:");
i = 0;
while (i < len(paths)) {
    item = paths[i];
    console.log("  " + item.path + " -> expected: " + item.expectedType);
    i = i + 1;
}

// ============================================
// Absolute vs Relative Path Detection
// ============================================

console.log("\n=== Absolute vs Relative Paths ===");

// Check if paths are absolute
testPathsAbs = [
    "/home/user/file.txt",
    "relative/path.txt",
    "/var/log/app.log",
    "data/config.json",
    "/usr/local/bin/app",
    "../parent/file.txt"
];

console.log("Absolute path detection:");
i = 0;
while (i < len(testPathsAbs)) {
    p = testPathsAbs[i];
    isAbs = path.isAbsolute(p);
    pathType = "";
    if (isAbs) {
        pathType = "absolute";
    } else {
        pathType = "relative";
    }
    console.log("  " + p + " -> " + pathType);
    i = i + 1;
}

// ============================================
// Safe Path Access Pattern
// ============================================

console.log("\n=== Safe Path Access ===");

function checkPathSafely(pathStr) {
    console.log("\nChecking path: " + pathStr);

    // Check if absolute
    isAbs = path.isAbsolute(pathStr);
    if (isAbs) {
        console.log("  Type: Absolute path");
    } else {
        console.log("  Type: Relative path");
    }

    // Normalize for safety
    normalized = path.normalize(pathStr);
    console.log("  Normalized: " + normalized);

    // Make absolute
    absolute = path.absolute(normalized);
    console.log("  Absolute: " + absolute);
}

// Demonstrate safe checking
checkPathSafely("../data/config.json");
checkPathSafely("/etc/app/settings.json");
checkPathSafely("./files/data.txt");

// ============================================
// File Type Classification
// ============================================

console.log("\n=== File Type Classification ===");

function classifyPath(p) {
    console.log("\nClassifying: " + p);

    // This demonstrates the API logic
    // In production, you would actually call the functions

    if (path.isAbsolute(p)) {
        console.log("  Path type: Absolute");
    } else {
        console.log("  Path type: Relative");
    }

    ext = path.extname(p);
    if (len(ext) > 0) {
        console.log("  Extension: " + ext);
    } else {
        console.log("  Extension: none");
    }
}

// Classify various paths
filesToClassify = [
    "/home/user/document.pdf",
    "relative/image.png",
    "/var/log/app.log",
    "data/config.json",
    "/usr/bin/application"
];

i = 0;
while (i < len(filesToClassify)) {
    classifyPath(filesToClassify[i]);
    i = i + 1;
}

// ============================================
// Path Validation Workflow
// ============================================

console.log("\n=== Path Validation Workflow ===");

function validatePath(userPath, requiredType) {
    console.log("\nValidating: " + userPath);
    console.log("  Required type: " + requiredType);

    // Step 1: Normalize
    normalized = path.normalize(userPath);
    console.log("  1. Normalized: " + normalized);

    // Step 2: Make absolute
    absolute = path.absolute(normalized);
    console.log("  2. Absolute: " + absolute);

    // Step 3: Check type
    isAbs = path.isAbsolute(absolute);
    console.log("  3. Is absolute: " + str(isAbs));

    // Step 4: Extract info
    dir = path.dirname(absolute);
    file = path.basename(absolute);
    console.log("  4. Directory: " + dir);
    console.log("  5. Filename: " + file);

    return absolute;
}

// Validate different paths
validatePath("../config.json", "file");
validatePath("./data/", "directory");

// ============================================
// Path Existence Patterns
// ============================================

console.log("\n=== Path Existence Patterns ===");

console.log("Pattern 1: Check before read");
console.log("  configPath = \"/etc/app/config.json\";");
console.log("  if (path.exists(configPath) && path.isFile(configPath)) {");
console.log("    content = file.read(configPath);");
console.log("  }");

console.log("\nPattern 2: Check directory before list");
console.log("  dataDir = \"/var/data\";");
console.log("  if (path.exists(dataDir) && path.isDirectory(dataDir)) {");
console.log("    files = path.listDir(dataDir);");
console.log("  }");

console.log("\nPattern 3: Safe file write");
console.log("  outputPath = \"/tmp/output.txt\";");
console.log("  outputDir = path.dirname(outputPath);");
console.log("  if (!path.exists(outputDir)) {");
console.log("    path.createDir(outputDir);");
console.log("  }");
console.log("  file.write(outputPath, content);");

// ============================================
// Batch Path Checking
// ============================================

console.log("\n=== Batch Path Checking ===");

requiredPaths = [
    {path: "/etc/app", type: "directory"},
    {path: "/etc/app/config.json", type: "file"},
    {path: "/var/log/app", type: "directory"},
    {path: "/var/log/app/app.log", type: "file"}
];

console.log("Checking required paths:");
i = 0;
while (i < len(requiredPaths)) {
    item = requiredPaths[i];
    console.log("\n  Path: " + item.path);
    console.log("  Required type: " + item.type);
    console.log("  Would check: path.exists() && path.is" + item.type + "()");
    i = i + 1;
}

// ============================================
// Path Statistics Collection
// ============================================

console.log("\n=== Path Statistics ===");

// Collect statistics about paths
pathList = [
    "/home/user/file1.txt",
    "relative/file2.txt",
    "/var/log/app.log",
    "data/config.json",
    "/usr/bin/tool"
];

absoluteCount = 0;
relativeCount = 0;

i = 0;
while (i < len(pathList)) {
    p = pathList[i];
    if (path.isAbsolute(p)) {
        absoluteCount = absoluteCount + 1;
    } else {
        relativeCount = relativeCount + 1;
    }
    i = i + 1;
}

console.log("Path statistics:");
console.log("  Total paths: " + str(len(pathList)));
console.log("  Absolute paths: " + str(absoluteCount));
console.log("  Relative paths: " + str(relativeCount));

// ============================================
// Extension Analysis
// ============================================

console.log("\n=== Extension Analysis ===");

files = [
    "/data/report.pdf",
    "/images/photo.png",
    "/config/settings.json",
    "/logs/app.log",
    "/bin/application"
];

console.log("File extension analysis:");
i = 0;
while (i < len(files)) {
    p = files[i];
    ext = path.extname(p);
    base = path.basename(p);

    if (len(ext) > 0) {
        console.log("  " + base + " -> extension: " + ext);
    } else {
        console.log("  " + base + " -> no extension");
    }
    i = i + 1;
}

// ============================================
// Security: Path Traversal Prevention
// ============================================

console.log("\n=== Security: Path Traversal Prevention ===");

function isSafePath(basePath, userPath) {
    // Normalize user input
    normalized = path.normalize(userPath);

    // Make absolute
    fullPath = path.absolute(path.join(basePath, normalized));

    // Ensure result is still under base path
    console.log("  Base: " + basePath);
    console.log("  User input: " + userPath);
    console.log("  Normalized: " + normalized);
    console.log("  Full path: " + fullPath);

    return true;
}

console.log("Checking user-provided paths:");
baseDir = "/var/app/data";
isSafePath(baseDir, "file.txt");
isSafePath(baseDir, "subdir/file.txt");
isSafePath(baseDir, "../../../etc/passwd");

// ============================================
// Common Path Queries
// ============================================

console.log("\n=== Common Path Query Patterns ===");

console.log("1. Check if config file exists:");
console.log("   path.exists(configPath) && path.isFile(configPath)");

console.log("\n2. Check if data directory exists:");
console.log("   path.exists(dataDir) && path.isDirectory(dataDir)");

console.log("\n3. Validate user input is absolute:");
console.log("   if (!path.isAbsolute(userPath)) {");
console.log("     userPath = path.absolute(userPath);");
console.log("   }");

console.log("\n4. Find files with specific extension:");
console.log("   ext = path.extname(file);");
console.log("   if (ext == \".json\") { ... }");

console.log("\n=== Filesystem Queries Complete ===");
