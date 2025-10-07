// ============================================
// Example: File Management Operations
// Category: standard-library/file
// Demonstrates: exists, copy, move, delete
// ============================================

import console;
import file;

console.log("=== File Management Operations ===\n");

// ============================================
// File Existence Checking
// ============================================

console.log("=== exists (check file existence) ===");

// Create a test file
file.write("test_file.txt", "Test content");
console.log("Created test_file.txt");

// Check if file exists
if (file.exists("test_file.txt")) {
    console.log("  test_file.txt exists: true");
} else {
    console.log("  test_file.txt exists: false");
}

// Check non-existent file
if (file.exists("nonexistent.txt")) {
    console.log("  nonexistent.txt exists: true");
} else {
    console.log("  nonexistent.txt exists: false");
}

// ============================================
// File Copying
// ============================================

console.log("\n=== copy (duplicate files) ===");

// Create source file
file.write("original.txt", "Original content that will be copied");
console.log("Created original.txt");

// Copy file
file.copy("original.txt", "backup.txt");
console.log("Copied original.txt -> backup.txt");

// Verify both exist
console.log("  original.txt exists: " + str(file.exists("original.txt")));
console.log("  backup.txt exists: " + str(file.exists("backup.txt")));

// Read both files
originalContent = file.read("original.txt");
backupContent = file.read("backup.txt");
console.log("  Contents match: " + str(originalContent == backupContent));

// ============================================
// File Moving/Renaming
// ============================================

console.log("\n=== move (rename/relocate files) ===");

// Create file to move
file.write("old_name.txt", "Content to be moved");
console.log("Created old_name.txt");

// Verify original exists
console.log("  old_name.txt exists: " + str(file.exists("old_name.txt")));

// Rename file
file.move("old_name.txt", "new_name.txt");
console.log("Moved old_name.txt -> new_name.txt");

// Verify move completed
console.log("  old_name.txt exists: " + str(file.exists("old_name.txt")));
console.log("  new_name.txt exists: " + str(file.exists("new_name.txt")));

// ============================================
// File Deletion
// ============================================

console.log("\n=== delete (remove files) ===");

// Create file to delete
file.write("temporary.txt", "Temporary content");
console.log("Created temporary.txt");

// Verify exists
console.log("  temporary.txt exists: " + str(file.exists("temporary.txt")));

// Delete file
deleted = file.delete("temporary.txt");
console.log("Deleted temporary.txt: " + str(deleted));

// Verify deleted
console.log("  temporary.txt exists: " + str(file.exists("temporary.txt")));

// Try deleting non-existent file
deleted2 = file.delete("nonexistent.txt");
console.log("Delete nonexistent.txt: " + str(deleted2) + " (returns false)");

// ============================================
// Practical Example: Backup System
// ============================================

console.log("\n=== Practical: File Backup System ===");

// Create original data file
originalData = "Important data that needs backup\nLine 2\nLine 3\n";
file.write("data.txt", originalData);
console.log("Created data.txt");

// Create backup with timestamp suffix
file.copy("data.txt", "data_backup_20240115.txt");
console.log("Created backup: data_backup_20240115.txt");

// Verify backup
if (file.exists("data_backup_20240115.txt")) {
    backupData = file.read("data_backup_20240115.txt");
    originalData2 = file.read("data.txt");

    if (backupData == originalData2) {
        console.log("  Backup verified: Contents match");
    } else {
        console.log("  Backup error: Contents differ");
    }
}

// ============================================
// Practical Example: File Versioning
// ============================================

console.log("\n=== Practical: File Versioning ===");

// Create version 1
file.write("document.txt", "Version 1 content");
console.log("Created document.txt (v1)");

// Save version 1
file.copy("document.txt", "document_v1.txt");
console.log("Saved as document_v1.txt");

// Update to version 2
file.write("document.txt", "Version 2 content");
console.log("Updated document.txt (v2)");

// Save version 2
file.copy("document.txt", "document_v2.txt");
console.log("Saved as document_v2.txt");

// List all versions
console.log("\nVersions available:");
console.log("  document_v1.txt: " + str(file.exists("document_v1.txt")));
console.log("  document_v2.txt: " + str(file.exists("document_v2.txt")));
console.log("  document.txt (current): " + str(file.exists("document.txt")));

// ============================================
// Practical Example: Temporary File Cleanup
// ============================================

console.log("\n=== Practical: Temporary File Cleanup ===");

// Create temporary files
file.write("temp1.tmp", "Temp 1");
file.write("temp2.tmp", "Temp 2");
file.write("temp3.tmp", "Temp 3");
console.log("Created 3 temporary files");

// List before cleanup
console.log("\nBefore cleanup:");
console.log("  temp1.tmp: " + str(file.exists("temp1.tmp")));
console.log("  temp2.tmp: " + str(file.exists("temp2.tmp")));
console.log("  temp3.tmp: " + str(file.exists("temp3.tmp")));

// Cleanup temporary files
file.delete("temp1.tmp");
file.delete("temp2.tmp");
file.delete("temp3.tmp");
console.log("\nDeleted temporary files");

// List after cleanup
console.log("\nAfter cleanup:");
console.log("  temp1.tmp: " + str(file.exists("temp1.tmp")));
console.log("  temp2.tmp: " + str(file.exists("temp2.tmp")));
console.log("  temp3.tmp: " + str(file.exists("temp3.tmp")));

// ============================================
// Practical Example: File Migration
// ============================================

console.log("\n=== Practical: File Migration ===");

// Create old format file
file.write("old_format.dat", "Old format data");
console.log("Created old_format.dat");

// Migrate to new format (copy then delete old)
file.copy("old_format.dat", "new_format.json");
console.log("Copied to new_format.json");

// Verify migration
if (file.exists("new_format.json")) {
    console.log("  Migration successful");

    // Delete old format
    file.delete("old_format.dat");
    console.log("  Removed old format file");

    console.log("\nAfter migration:");
    console.log("  old_format.dat: " + str(file.exists("old_format.dat")));
    console.log("  new_format.json: " + str(file.exists("new_format.json")));
}

// ============================================
// Practical Example: Safe File Update
// ============================================

console.log("\n=== Practical: Safe File Update ===");

// Create important file
file.write("important.txt", "Critical data");
console.log("Created important.txt");

// Safe update process:
// 1. Create backup
// 2. Update original
// 3. Verify update
// 4. Delete backup on success

// Step 1: Backup
file.copy("important.txt", "important.txt.bak");
console.log("  Step 1: Created backup");

// Step 2: Update
file.write("important.txt", "Updated critical data");
console.log("  Step 2: Updated original");

// Step 3: Verify (simplified - just check exists)
if (file.exists("important.txt")) {
    console.log("  Step 3: Update verified");

    // Step 4: Cleanup backup
    file.delete("important.txt.bak");
    console.log("  Step 4: Removed backup");
}

console.log("\nSafe update complete");

// ============================================
// Practical Example: Archive System
// ============================================

console.log("\n=== Practical: Archive System ===");

// Create active file
file.write("active_log.txt", "Active log entry 1\nActive log entry 2\n");
console.log("Created active_log.txt");

// Archive old log (rename with date)
file.move("active_log.txt", "archived_log_20240115.txt");
console.log("Archived active_log.txt");

// Create new active log
file.write("active_log.txt", "New active log entry\n");
console.log("Created new active_log.txt");

// Verify archive system
console.log("\nArchive status:");
console.log("  active_log.txt: " + str(file.exists("active_log.txt")));
console.log("  archived_log_20240115.txt: " + str(file.exists("archived_log_20240115.txt")));

// ============================================
// Conditional File Operations
// ============================================

console.log("\n=== Conditional File Operations ===");

// Create files conditionally
targetFile = "conditional_test.txt";

if (!file.exists(targetFile)) {
    file.write(targetFile, "New file created");
    console.log("Created " + targetFile + " (didn't exist)");
} else {
    console.log(targetFile + " already exists, skipping");
}

// Try again (should skip)
if (!file.exists(targetFile)) {
    file.write(targetFile, "New file created");
    console.log("Created " + targetFile);
} else {
    console.log(targetFile + " already exists, skipping");
}

// ============================================
// Batch File Operations
// ============================================

console.log("\n=== Batch File Operations ===");

// Create multiple files
console.log("Creating batch files...");
file.write("batch1.txt", "Batch file 1");
file.write("batch2.txt", "Batch file 2");
file.write("batch3.txt", "Batch file 3");
console.log("  Created 3 batch files");

// Copy all files
console.log("\nCopying batch files...");
file.copy("batch1.txt", "batch1_copy.txt");
file.copy("batch2.txt", "batch2_copy.txt");
file.copy("batch3.txt", "batch3_copy.txt");
console.log("  Copied 3 files");

// Verify all exist
console.log("\nVerifying files:");
existCount = 0;

if (file.exists("batch1.txt")) {
    existCount = existCount + 1;
}
if (file.exists("batch2.txt")) {
    existCount = existCount + 1;
}
if (file.exists("batch3.txt")) {
    existCount = existCount + 1;
}
if (file.exists("batch1_copy.txt")) {
    existCount = existCount + 1;
}
if (file.exists("batch2_copy.txt")) {
    existCount = existCount + 1;
}
if (file.exists("batch3_copy.txt")) {
    existCount = existCount + 1;
}

console.log("  Total files exist: " + str(existCount) + "/6");

// Cleanup
console.log("\nCleaning up batch files...");
file.delete("batch1.txt");
file.delete("batch2.txt");
file.delete("batch3.txt");
file.delete("batch1_copy.txt");
file.delete("batch2_copy.txt");
file.delete("batch3_copy.txt");
console.log("  Deleted all batch files");

console.log("\n=== File Management Complete ===");
