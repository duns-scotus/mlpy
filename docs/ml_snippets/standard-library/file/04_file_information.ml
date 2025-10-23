// ============================================
// Example: File Information and Metadata
// Category: standard-library/file
// Demonstrates: size, modifiedTime, isFile, isDirectory
// ============================================

import console;
import file;

console.log("=== File Information and Metadata ===\n");

// ============================================
// File Size
// ============================================

console.log("=== size (get file size in bytes) ===");

// Create files of different sizes
file.write("small.txt", "Small");
file.write("medium.txt", "This is a medium-sized file with more content in it.");
file.write("large.txt", "This is a large file with even more content. " +
    "It has multiple sentences. " +
    "The content keeps going. " +
    "More and more text to make it larger.");

// Get file sizes
smallSize = file.size("small.txt");
mediumSize = file.size("medium.txt");
largeSize = file.size("large.txt");

console.log("File sizes:");
console.log("  small.txt: " + str(smallSize) + " bytes");
console.log("  medium.txt: " + str(mediumSize) + " bytes");
console.log("  large.txt: " + str(largeSize) + " bytes");

// Calculate size in KB
console.log("\nSizes in KB:");
console.log("  small.txt: " + str(smallSize / 1024) + " KB");
console.log("  medium.txt: " + str(mediumSize / 1024) + " KB");
console.log("  large.txt: " + str(largeSize / 1024) + " KB");

// ============================================
// Empty File Size
// ============================================

console.log("\n=== Empty File Size ===");

file.write("empty.txt", "");
emptySize = file.size("empty.txt");
console.log("empty.txt size: " + str(emptySize) + " bytes");
console.log("  Is empty: " + str(emptySize == 0));

// ============================================
// File Type Checking
// ============================================

console.log("\n=== isFile / isDirectory (type checking) ===");

// Create test file
file.write("testfile.txt", "Test content");

// Check if it's a file
isFileResult = file.isFile("testfile.txt");
console.log("testfile.txt is file: " + str(isFileResult));

// Note: We can't easily demonstrate isDirectory without actual directories
// in the sandbox environment, but we can show the API

console.log("\nType checking:");
console.log("  testfile.txt is file: " + str(file.isFile("testfile.txt")));

// ============================================
// Practical Example: File Size Monitoring
// ============================================

console.log("\n=== Practical: File Size Monitoring ===");

// Create log file
file.write("monitor.log", "Initial log entry\n");
initialSize = file.size("monitor.log");
console.log("Initial log size: " + str(initialSize) + " bytes");

// Add more entries
file.append("monitor.log", "Second log entry\n");
file.append("monitor.log", "Third log entry\n");
file.append("monitor.log", "Fourth log entry\n");

// Check new size
currentSize = file.size("monitor.log");
console.log("Current log size: " + str(currentSize) + " bytes");

// Calculate growth
growth = currentSize - initialSize;
console.log("Size growth: " + str(growth) + " bytes");

// ============================================
// Practical Example: Size-Based File Management
// ============================================

console.log("\n=== Practical: Size-Based Management ===");

// Create files of various sizes
file.write("doc1.txt", "Short");
file.write("doc2.txt", "This is a much longer document with more content");
file.write("doc3.txt", "Medium length document");

console.log("Checking file sizes:");

// Check each file
size1 = file.size("doc1.txt");
size2 = file.size("doc2.txt");
size3 = file.size("doc3.txt");

console.log("  doc1.txt: " + str(size1) + " bytes");
console.log("  doc2.txt: " + str(size2) + " bytes");
console.log("  doc3.txt: " + str(size3) + " bytes");

// Classify by size
threshold = 30;
console.log("\nClassification (threshold: " + str(threshold) + " bytes):");

if (size1 < threshold) {
    console.log("  doc1.txt: small");
} else {
    console.log("  doc1.txt: large");
}

if (size2 < threshold) {
    console.log("  doc2.txt: small");
} else {
    console.log("  doc2.txt: large");
}

if (size3 < threshold) {
    console.log("  doc3.txt: small");
} else {
    console.log("  doc3.txt: large");
}

// ============================================
// Practical Example: Storage Statistics
// ============================================

console.log("\n=== Practical: Storage Statistics ===");

// Create multiple files
file.write("data1.txt", "Data file 1 content");
file.write("data2.txt", "Data file 2 with more content");
file.write("data3.txt", "Data file 3 content");
file.write("data4.txt", "Data file 4 with even more content here");

// Calculate total storage
totalSize = 0;
totalSize = totalSize + file.size("data1.txt");
totalSize = totalSize + file.size("data2.txt");
totalSize = totalSize + file.size("data3.txt");
totalSize = totalSize + file.size("data4.txt");

console.log("Storage Statistics:");
console.log("  Number of files: 4");
console.log("  Total size: " + str(totalSize) + " bytes");
console.log("  Total size: " + str(totalSize / 1024) + " KB");
console.log("  Average size: " + str(totalSize / 4) + " bytes/file");

// ============================================
// Practical Example: File Comparison
// ============================================

console.log("\n=== Practical: File Comparison ===");

// Create two files
file.write("version1.txt", "Version 1 content");
file.write("version2.txt", "Version 2 content with additional information");

size_v1 = file.size("version1.txt");
size_v2 = file.size("version2.txt");

console.log("Comparing versions:");
console.log("  version1.txt: " + str(size_v1) + " bytes");
console.log("  version2.txt: " + str(size_v2) + " bytes");

if (size_v2 > size_v1) {
    diff = size_v2 - size_v1;
    console.log("  version2.txt is " + str(diff) + " bytes larger");
} elif (size_v1 > size_v2) {
    diff = size_v1 - size_v2;
    console.log("  version1.txt is " + str(diff) + " bytes larger");
} else {
    console.log("  Files are the same size");
}

// ============================================
// Practical Example: Quota Enforcement
// ============================================

console.log("\n=== Practical: Quota Enforcement ===");

quota = 200;
console.log("File quota: " + str(quota) + " bytes");

// Track usage
usedSpace = 0;

// Try to write files within quota
console.log("\nWriting files:");

// File 1
content1 = "First file content";
file.write("quota1.txt", content1);
size1 = file.size("quota1.txt");
usedSpace = usedSpace + size1;
console.log("  quota1.txt: " + str(size1) + " bytes (total: " + str(usedSpace) + "/" + str(quota) + ")");

// File 2
content2 = "Second file with more content";
file.write("quota2.txt", content2);
size2 = file.size("quota2.txt");
usedSpace = usedSpace + size2;
console.log("  quota2.txt: " + str(size2) + " bytes (total: " + str(usedSpace) + "/" + str(quota) + ")");

// Check quota
if (usedSpace < quota) {
    remaining = quota - usedSpace;
    console.log("\nQuota status: OK");
    console.log("  Used: " + str(usedSpace) + " bytes");
    console.log("  Remaining: " + str(remaining) + " bytes");
} else {
    console.log("\nQuota status: EXCEEDED");
    console.log("  Used: " + str(usedSpace) + " bytes");
    console.log("  Limit: " + str(quota) + " bytes");
}

// ============================================
// Practical Example: File Growth Tracking
// ============================================

console.log("\n=== Practical: File Growth Tracking ===");

// Create initial file
file.write("growth.log", "Initial");
snapshot1 = file.size("growth.log");
console.log("Snapshot 1: " + str(snapshot1) + " bytes");

// Append data
file.append("growth.log", " - Addition 1");
snapshot2 = file.size("growth.log");
console.log("Snapshot 2: " + str(snapshot2) + " bytes (+" + str(snapshot2 - snapshot1) + ")");

// Append more data
file.append("growth.log", " - Addition 2");
snapshot3 = file.size("growth.log");
console.log("Snapshot 3: " + str(snapshot3) + " bytes (+" + str(snapshot3 - snapshot2) + ")");

// Append even more data
file.append("growth.log", " - Addition 3");
snapshot4 = file.size("growth.log");
console.log("Snapshot 4: " + str(snapshot4) + " bytes (+" + str(snapshot4 - snapshot3) + ")");

// Total growth
totalGrowth = snapshot4 - snapshot1;
console.log("\nTotal growth: " + str(totalGrowth) + " bytes");
console.log("Growth rate: " + str(totalGrowth / 3) + " bytes per addition");

// ============================================
// Practical Example: Duplicate Detection
// ============================================

console.log("\n=== Practical: Duplicate Detection (by size) ===");

// Create files with same size
file.write("file_a.txt", "Same size");
file.write("file_b.txt", "Same size");
file.write("file_c.txt", "Different size content");

sizeA = file.size("file_a.txt");
sizeB = file.size("file_b.txt");
sizeC = file.size("file_c.txt");

console.log("File sizes:");
console.log("  file_a.txt: " + str(sizeA) + " bytes");
console.log("  file_b.txt: " + str(sizeB) + " bytes");
console.log("  file_c.txt: " + str(sizeC) + " bytes");

console.log("\nDuplicate detection:");
if (sizeA == sizeB) {
    console.log("  file_a.txt and file_b.txt: Potentially duplicate (same size)");
}
if (sizeA == sizeC) {
    console.log("  file_a.txt and file_c.txt: Potentially duplicate (same size)");
}
if (sizeB == sizeC) {
    console.log("  file_b.txt and file_c.txt: Potentially duplicate (same size)");
}

// ============================================
// Comprehensive File Info Display
// ============================================

console.log("\n=== Comprehensive File Information ===");

// Create sample file
sampleContent = "Sample file for comprehensive information display";
file.write("sample_info.txt", sampleContent);

console.log("File: sample_info.txt");

// Size
infoSize = file.size("sample_info.txt");
console.log("  Size: " + str(infoSize) + " bytes");
console.log("  Size: " + str(infoSize / 1024) + " KB");

// Type
console.log("  Is file: " + str(file.isFile("sample_info.txt")));

// Existence
console.log("  Exists: " + str(file.exists("sample_info.txt")));

// Content length
infoContent = file.read("sample_info.txt");
console.log("  Content length: " + str(len(infoContent)) + " chars");

console.log("\n=== File Information Complete ===");
