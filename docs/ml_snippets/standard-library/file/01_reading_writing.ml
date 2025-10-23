// ============================================
// Example: File Reading and Writing
// Category: standard-library/file
// Demonstrates: read, write, readBytes, writeBytes
// ============================================

import console;
import file;

console.log("=== File Reading and Writing ===\n");

// ============================================
// Basic Writing
// ============================================

console.log("=== Basic File Writing ===");

// Write simple text file
file.write("test_output.txt", "Hello from ML!");
console.log("Wrote: test_output.txt");

// Write multi-line content
content = "Line 1\nLine 2\nLine 3\n";
file.write("multiline.txt", content);
console.log("Wrote: multiline.txt with 3 lines");

// Write with explicit encoding
file.write("utf8_test.txt", "Encoded content", "utf-8");
console.log("Wrote: utf8_test.txt (UTF-8)");

// ============================================
// Basic Reading
// ============================================

console.log("\n=== Basic File Reading ===");

// Read text file
readContent = file.read("test_output.txt");
console.log("Read from test_output.txt:");
console.log("  Content: " + readContent);

// Read multi-line file
multiContent = file.read("multiline.txt");
console.log("\nRead from multiline.txt:");
console.log("  Content length: " + str(len(multiContent)) + " chars");
console.log("  Content: " + multiContent);

// ============================================
// Binary Operations
// ============================================

console.log("\n=== Binary File Operations ===");

// Create binary data (simulate)
binaryData = "Binary data content";
file.write("binary_test.bin", binaryData);
console.log("Created binary_test.bin");

// Read as text
textData = file.read("binary_test.bin");
console.log("Read as text: " + textData);

// ============================================
// Practical Example: Configuration Files
// ============================================

console.log("\n=== Practical: Configuration File ===");

// Create configuration
config = {
    "app_name": "MyApp",
    "version": "1.0.0",
    "debug": true,
    "max_connections": 100
};

// Note: In real ML we'd use json.stringify, here we'll format manually
configContent = "app_name=MyApp\nversion=1.0.0\ndebug=true\nmax_connections=100";
file.write("config.txt", configContent);
console.log("Wrote configuration to config.txt");

// Read configuration back
loadedConfig = file.read("config.txt");
console.log("\nLoaded configuration:");
console.log(loadedConfig);

// ============================================
// Practical Example: Log File
// ============================================

console.log("\n=== Practical: Log File ===");

// Create log entry
timestamp = "2024-01-15 10:30:00";
logEntry = "[" + timestamp + "] Application started\n";
file.write("app.log", logEntry);
console.log("Created app.log with initial entry");

// Read log
logContent = file.read("app.log");
console.log("\nLog contents:");
console.log(logContent);

// ============================================
// Practical Example: Data File
// ============================================

console.log("\n=== Practical: Data File ===");

// Simulate CSV data
csvData = "id,name,age\n1,Alice,30\n2,Bob,25\n3,Charlie,35\n";
file.write("users.csv", csvData);
console.log("Wrote CSV data to users.csv");

// Read and display
csvContent = file.read("users.csv");
console.log("\nCSV Content:");
console.log(csvContent);

// ============================================
// Overwriting Files
// ============================================

console.log("\n=== File Overwriting ===");

// Write initial content
file.write("overwrite_test.txt", "Initial content");
console.log("Initial write: overwrite_test.txt");

initial = file.read("overwrite_test.txt");
console.log("  Content: " + initial);

// Overwrite with new content
file.write("overwrite_test.txt", "New content");
console.log("\nOverwritten: overwrite_test.txt");

updated = file.read("overwrite_test.txt");
console.log("  Content: " + updated);

// ============================================
// Empty Files
// ============================================

console.log("\n=== Empty Files ===");

// Write empty file
file.write("empty.txt", "");
console.log("Created empty.txt");

emptyContent = file.read("empty.txt");
console.log("Read empty.txt:");
console.log("  Length: " + str(len(emptyContent)) + " chars");
console.log("  Is empty: " + str(len(emptyContent) == 0));

// ============================================
// Large Content
// ============================================

console.log("\n=== Large Content ===");

// Generate larger content
largeContent = "";
i = 0;
while (i < 100) {
    largeContent = largeContent + "Line " + str(i) + "\n";
    i = i + 1;
}

file.write("large.txt", largeContent);
console.log("Wrote large.txt with 100 lines");

// Read back
readLarge = file.read("large.txt");
console.log("Read large.txt:");
console.log("  Content length: " + str(len(readLarge)) + " chars");

// ============================================
// Multiple Files
// ============================================

console.log("\n=== Multiple Files ===");

// Create multiple files
file.write("file1.txt", "Content 1");
file.write("file2.txt", "Content 2");
file.write("file3.txt", "Content 3");
console.log("Created 3 files: file1.txt, file2.txt, file3.txt");

// Read all files
content1 = file.read("file1.txt");
content2 = file.read("file2.txt");
content3 = file.read("file3.txt");

console.log("\nRead all files:");
console.log("  file1.txt: " + content1);
console.log("  file2.txt: " + content2);
console.log("  file3.txt: " + content3);

// ============================================
// Round-Trip Test
// ============================================

console.log("\n=== Round-Trip Test ===");

originalContent = "Round-trip test content with special chars: !@#$%";
file.write("roundtrip.txt", originalContent);
console.log("Wrote: " + originalContent);

readBack = file.read("roundtrip.txt");
console.log("Read: " + readBack);

matches = originalContent == readBack;
console.log("Content matches: " + str(matches));

console.log("\n=== File Reading and Writing Complete ===");
