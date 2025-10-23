// ============================================
// Example: Directory Management Operations
// Category: standard-library/path
// Demonstrates: createDir, removeDir, removeDirRecursive (requires path.write capability)
// ============================================

import console;
import path;

console.log("=== Directory Management Operations ===\n");

console.log("Note: This example demonstrates directory management APIs.");
console.log("Actual directory operations require path.write capabilities.\n");

// ============================================
// Creating Directories
// ============================================

console.log("=== Creating Directories ===");

console.log("Create single directory:");
console.log("  path.createDir(\"/data/output\");");

console.log("\nCreate directory with parents:");
console.log("  path.createDir(\"/data/reports/2024/january\", true);");
console.log("  // Creates all parent directories");

console.log("\nCreate directory (idempotent):");
console.log("  path.createDir(\"/data/cache\");");
console.log("  path.createDir(\"/data/cache\");  // Safe - no error if exists");

// ============================================
// Directory Creation Patterns
// ============================================

console.log("\n=== Directory Creation Patterns ===");

console.log("Pattern 1: Create project structure");
console.log("  projectDirs = [");
console.log("    \"/project/src\",");
console.log("    \"/project/tests\",");
console.log("    \"/project/docs\",");
console.log("    \"/project/build\"");
console.log("  ];");
console.log("  \n  i = 0;");
console.log("  while (i < len(projectDirs)) {");
console.log("    path.createDir(projectDirs[i], true);");
console.log("    i = i + 1;");
console.log("  }");

console.log("\nPattern 2: Create dated directories");
console.log("  baseDir = \"/logs\";");
console.log("  date = \"2024-01-15\";");
console.log("  logDir = path.join(baseDir, date);");
console.log("  path.createDir(logDir, true);");

console.log("\nPattern 3: Create user directories");
console.log("  userId = \"user123\";");
console.log("  userBase = path.join(\"/data/users\", userId);");
console.log("  path.createDir(path.join(userBase, \"files\"), true);");
console.log("  path.createDir(path.join(userBase, \"uploads\"), true);");
console.log("  path.createDir(path.join(userBase, \"cache\"), true);");

// ============================================
// Removing Empty Directories
// ============================================

console.log("\n=== Removing Empty Directories ===");

console.log("Remove empty directory:");
console.log("  path.removeDir(\"/tmp/empty\");");
console.log("  // Only works if directory is empty");

console.log("\nSafe removal pattern:");
console.log("  tempDir = \"/tmp/cache\";");
console.log("  if (path.exists(tempDir) && path.isDirectory(tempDir)) {");
console.log("    path.removeDir(tempDir);");
console.log("  }");

// ============================================
// Recursive Directory Removal
// ============================================

console.log("\n=== Recursive Directory Removal ===");

console.log("Remove directory and all contents:");
console.log("  path.removeDirRecursive(\"/tmp/data\");");
console.log("  // DANGEROUS: Removes everything inside!");

console.log("\nSafe recursive removal:");
console.log("  oldDir = \"/data/archive/2020\";");
console.log("  if (path.exists(oldDir)) {");
console.log("    console.log(\"Removing: \" + oldDir);");
console.log("    path.removeDirRecursive(oldDir);");
console.log("  }");

// ============================================
// Directory Lifecycle Management
// ============================================

console.log("\n=== Directory Lifecycle Management ===");

function setupWorkspace(workspaceId) {
    console.log("\nSetting up workspace: " + workspaceId);

    workspaceDir = path.join("/data/workspaces", workspaceId);
    console.log("  Creating: " + workspaceDir);

    // Create workspace structure
    dirs = [
        path.join(workspaceDir, "input"),
        path.join(workspaceDir, "output"),
        path.join(workspaceDir, "temp"),
        path.join(workspaceDir, "logs")
    ];

    console.log("  Creating " + str(len(dirs)) + " subdirectories...");

    i = 0;
    while (i < len(dirs)) {
        console.log("    - " + path.basename(dirs[i]));
        i = i + 1;
    }
}

setupWorkspace("ws-2024-001");

function cleanupWorkspace(workspaceId) {
    console.log("\nCleaning up workspace: " + workspaceId);

    workspaceDir = path.join("/data/workspaces", workspaceId);
    console.log("  Removing: " + workspaceDir);
    console.log("  path.removeDirRecursive(workspaceDir);");
}

cleanupWorkspace("ws-2024-001");

// ============================================
// Temporary Directory Management
// ============================================

console.log("\n=== Temporary Directory Management ===");

console.log("Create temporary directory:");
console.log("  tmpBase = path.tempDir();");
console.log("  sessionId = \"session-\" + str(12345);");
console.log("  tmpDir = path.join(tmpBase, sessionId);");
console.log("  \n  path.createDir(tmpDir, true);");
console.log("  console.log(\"Temp directory: \" + tmpDir);");

console.log("\nCleanup temporary directory:");
console.log("  if (path.exists(tmpDir)) {");
console.log("    path.removeDirRecursive(tmpDir);");
console.log("    console.log(\"Cleaned up: \" + tmpDir);");
console.log("  }");

// ============================================
// Archive Directory Management
// ============================================

console.log("\n=== Archive Directory Management ===");

console.log("Create archive structure:");
console.log("  year = \"2024\";");
console.log("  month = \"01\";");
console.log("  archiveDir = path.join(\"/archive\", year, month);");
console.log("  \n  path.createDir(archiveDir, true);");
console.log("  console.log(\"Archive: \" + archiveDir);");

console.log("\nRemove old archives:");
console.log("  oldYear = \"2020\";");
console.log("  oldArchive = path.join(\"/archive\", oldYear);");
console.log("  \n  if (path.exists(oldArchive)) {");
console.log("    console.log(\"Removing old archive: \" + oldArchive);");
console.log("    path.removeDirRecursive(oldArchive);");
console.log("  }");

// ============================================
// Backup Directory Management
// ============================================

console.log("\n=== Backup Directory Management ===");

function createBackupDir(timestamp) {
    console.log("\nCreating backup directory:");

    backupBase = "/backups";
    backupDir = path.join(backupBase, timestamp);

    console.log("  Base: " + backupBase);
    console.log("  Timestamp: " + timestamp);
    console.log("  Full path: " + backupDir);
    console.log("  \n  path.createDir(backupDir, true);");
}

createBackupDir("2024-01-15-1430");

function cleanOldBackups(keepDays) {
    console.log("\nCleaning old backups:");
    console.log("  Keep last " + str(keepDays) + " days");
    console.log("  \n  backups = path.listDir(\"/backups\");");
    console.log("  // Remove backups older than keepDays");
}

cleanOldBackups(7);

// ============================================
// User Data Directory Management
// ============================================

console.log("\n=== User Data Directory Management ===");

function createUserDirectory(username) {
    console.log("\nCreating user directory:");

    userBase = path.join("/data/users", username);
    console.log("  User: " + username);
    console.log("  Base: " + userBase);

    folders = ["documents", "uploads", "downloads", "cache"];
    console.log("  Creating " + str(len(folders)) + " folders:");

    i = 0;
    while (i < len(folders)) {
        folder = folders[i];
        fullPath = path.join(userBase, folder);
        console.log("    - " + folder + " -> " + fullPath);
        i = i + 1;
    }
}

createUserDirectory("alice");

function removeUserDirectory(username) {
    console.log("\nRemoving user directory:");

    userDir = path.join("/data/users", username);
    console.log("  User: " + username);
    console.log("  Directory: " + userDir);
    console.log("  \n  path.removeDirRecursive(userDir);");
}

removeUserDirectory("bob");

// ============================================
// Cache Directory Management
// ============================================

console.log("\n=== Cache Directory Management ===");

console.log("Setup cache directories:");
console.log("  cacheBase = \"/cache\";");
console.log("  cacheDirs = [");
console.log("    path.join(cacheBase, \"api\"),");
console.log("    path.join(cacheBase, \"images\"),");
console.log("    path.join(cacheBase, \"data\")");
console.log("  ];");
console.log("  \n  i = 0;");
console.log("  while (i < len(cacheDirs)) {");
console.log("    path.createDir(cacheDirs[i], true);");
console.log("    i = i + 1;");
console.log("  }");

console.log("\nClear cache:");
console.log("  cacheDir = \"/cache/api\";");
console.log("  if (path.exists(cacheDir)) {");
console.log("    path.removeDirRecursive(cacheDir);");
console.log("    path.createDir(cacheDir, true);  // Recreate empty");
console.log("  }");

// ============================================
// Output Directory Management
// ============================================

console.log("\n=== Output Directory Management ===");

console.log("Prepare output directory:");
console.log("  outputDir = \"/output/report-2024\";");
console.log("  \n  // Clean if exists");
console.log("  if (path.exists(outputDir)) {");
console.log("    path.removeDirRecursive(outputDir);");
console.log("  }");
console.log("  \n  // Create fresh");
console.log("  path.createDir(outputDir, true);");

// ============================================
// Build Directory Management
// ============================================

console.log("\n=== Build Directory Management ===");

console.log("Clean build directory:");
console.log("  buildDir = \"/project/build\";");
console.log("  \n  console.log(\"Cleaning build directory...\");");
console.log("  if (path.exists(buildDir)) {");
console.log("    path.removeDirRecursive(buildDir);");
console.log("  }");
console.log("  path.createDir(buildDir, true);");

console.log("\nCreate build subdirectories:");
console.log("  buildDirs = [");
console.log("    path.join(buildDir, \"lib\"),");
console.log("    path.join(buildDir, \"bin\"),");
console.log("    path.join(buildDir, \"dist\")");
console.log("  ];");
console.log("  \n  i = 0;");
console.log("  while (i < len(buildDirs)) {");
console.log("    path.createDir(buildDirs[i], true);");
console.log("    i = i + 1;");
console.log("  }");

// ============================================
// Log Directory Management
// ============================================

console.log("\n=== Log Directory Management ===");

function setupLogDirectories() {
    console.log("\nSetting up log directories:");

    logBase = "/var/log/app";
    logTypes = ["access", "error", "debug", "audit"];

    console.log("  Base: " + logBase);
    console.log("  Types: " + str(len(logTypes)));

    i = 0;
    while (i < len(logTypes)) {
        logType = logTypes[i];
        logDir = path.join(logBase, logType);
        console.log("    - " + logType + " -> " + logDir);
        i = i + 1;
    }
}

setupLogDirectories();

// ============================================
// Directory Safety Checks
// ============================================

console.log("\n=== Directory Safety Checks ===");

function safeRemoveDir(dirPath) {
    console.log("\nSafely removing directory:");
    console.log("  Path: " + dirPath);

    // Safety checks
    console.log("  1. Check if path is absolute");
    if (!path.isAbsolute(dirPath)) {
        console.log("     WARNING: Not absolute path!");
        return false;
    }

    console.log("  2. Check if directory exists");
    console.log("     path.exists(dirPath)");

    console.log("  3. Check if it's actually a directory");
    console.log("     path.isDirectory(dirPath)");

    console.log("  4. Proceed with removal");
    console.log("     path.removeDirRecursive(dirPath);");

    return true;
}

safeRemoveDir("/tmp/safe-to-delete");

// ============================================
// Batch Directory Operations
// ============================================

console.log("\n=== Batch Directory Operations ===");

console.log("Create multiple directories:");
console.log("  dirs = [");
console.log("    \"/data/input\",");
console.log("    \"/data/output\",");
console.log("    \"/data/archive\",");
console.log("    \"/data/temp\"");
console.log("  ];");
console.log("  \n  i = 0;");
console.log("  while (i < len(dirs)) {");
console.log("    path.createDir(dirs[i], true);");
console.log("    console.log(\"Created: \" + dirs[i]);");
console.log("    i = i + 1;");
console.log("  }");

console.log("\nRemove multiple directories:");
console.log("  oldDirs = [");
console.log("    \"/tmp/session-1\",");
console.log("    \"/tmp/session-2\",");
console.log("    \"/tmp/session-3\"");
console.log("  ];");
console.log("  \n  i = 0;");
console.log("  while (i < len(oldDirs)) {");
console.log("    dir = oldDirs[i];");
console.log("    if (path.exists(dir)) {");
console.log("      path.removeDirRecursive(dir);");
console.log("      console.log(\"Removed: \" + dir);");
console.log("    }");
console.log("    i = i + 1;");
console.log("  }");

// ============================================
// Best Practices
// ============================================

console.log("\n=== Directory Management Best Practices ===");

console.log("1. Use createDir() with parents=true for nested structures");
console.log("2. Check path.exists() before removing directories");
console.log("3. Use absolute paths for safety");
console.log("4. Be extremely cautious with removeDirRecursive()");
console.log("5. Create parent directories automatically");
console.log("6. Clean temporary directories after use");
console.log("7. Use path.join() to build directory paths");
console.log("8. Verify paths are directories with path.isDirectory()");

// ============================================
// Common Patterns Summary
// ============================================

console.log("\n=== Common Patterns Summary ===");

console.log("\nCreate directory structure:");
console.log("  path.createDir(\"/data/output/2024\", true);");

console.log("\nClean and recreate:");
console.log("  if (path.exists(dir)) path.removeDirRecursive(dir);");
console.log("  path.createDir(dir, true);");

console.log("\nSafe removal:");
console.log("  if (path.exists(dir) && path.isDirectory(dir)) {");
console.log("    path.removeDir(dir);  // or removeDirRecursive");
console.log("  }");

console.log("\nBatch creation:");
console.log("  dirs.forEach(d => path.createDir(d, true));");

console.log("\n=== Directory Management Complete ===");
