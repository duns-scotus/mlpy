// ============================================
// Example: Directory Listing Operations
// Category: standard-library/path
// Demonstrates: listDir, glob, walk (requires path.read capability)
// ============================================

import console;
import path;

console.log("=== Directory Listing Operations ===\n");

console.log("Note: This example demonstrates directory listing APIs.");
console.log("Actual directory listing requires path.read capabilities.\n");

// ============================================
// Basic Directory Listing
// ============================================

console.log("=== Basic Directory Listing ===");

console.log("List directory contents:");
console.log("  files = path.listDir(\"/data\");");
console.log("  for file in files {");
console.log("    console.log(file);");
console.log("  }");

console.log("\nList current directory:");
console.log("  files = path.listDir(\".\");");

console.log("\nList specific directory:");
console.log("  files = path.listDir(\"/var/log\");");

// ============================================
// Directory Listing Patterns
// ============================================

console.log("\n=== Directory Listing Patterns ===");

console.log("Pattern 1: List and count files");
console.log("  files = path.listDir(\"/data\");");
console.log("  console.log(\"Found \" + str(len(files)) + \" files\");");

console.log("\nPattern 2: List and filter by extension");
console.log("  files = path.listDir(\"/data\");");
console.log("  i = 0;");
console.log("  while (i < len(files)) {");
console.log("    file = files[i];");
console.log("    if (path.extname(file) == \".json\") {");
console.log("      console.log(\"JSON file: \" + file);");
console.log("    }");
console.log("    i = i + 1;");
console.log("  }");

console.log("\nPattern 3: List and build full paths");
console.log("  baseDir = \"/data\";");
console.log("  files = path.listDir(baseDir);");
console.log("  i = 0;");
console.log("  while (i < len(files)) {");
console.log("    fullPath = path.join(baseDir, files[i]);");
console.log("    console.log(fullPath);");
console.log("    i = i + 1;");
console.log("  }");

// ============================================
// Glob Pattern Matching
// ============================================

console.log("\n=== Glob Pattern Matching ===");

console.log("Find all text files:");
console.log("  txtFiles = path.glob(\"*.txt\");");

console.log("\nFind all JSON files:");
console.log("  jsonFiles = path.glob(\"*.json\");");

console.log("\nFind files recursively:");
console.log("  allTxt = path.glob(\"**/*.txt\");");

console.log("\nFind files with specific pattern:");
console.log("  dataFiles = path.glob(\"data/file[0-9].txt\");");

// ============================================
// Glob Pattern Examples
// ============================================

console.log("\n=== Glob Pattern Examples ===");

patterns = [
    {pattern: "*.txt", desc: "All .txt files in current directory"},
    {pattern: "**/*.ml", desc: "All .ml files recursively"},
    {pattern: "data/*.json", desc: "All .json files in data/"},
    {pattern: "test_*.ml", desc: "All test files starting with test_"},
    {pattern: "file[0-9].txt", desc: "Files like file0.txt, file1.txt, etc."},
    {pattern: "**/*.{json,yaml}", desc: "All JSON and YAML files recursively"}
];

console.log("Common glob patterns:");
i = 0;
while (i < len(patterns)) {
    item = patterns[i];
    console.log("\n  Pattern: " + item.pattern);
    console.log("  Matches: " + item.desc);
    i = i + 1;
}

// ============================================
// Directory Tree Walking
// ============================================

console.log("\n=== Directory Tree Walking ===");

console.log("Walk entire directory tree:");
console.log("  allFiles = path.walk(\"/data\");");
console.log("  console.log(\"Found \" + str(len(allFiles)) + \" files\");");

console.log("\nWalk with depth limit:");
console.log("  shallowFiles = path.walk(\"/data\", 1);");
console.log("  // Only 1 level deep");

console.log("\nWalk and process files:");
console.log("  files = path.walk(\"/data\");");
console.log("  i = 0;");
console.log("  while (i < len(files)) {");
console.log("    file = files[i];");
console.log("    console.log(\"Processing: \" + file);");
console.log("    i = i + 1;");
console.log("  }");

// ============================================
// Recursive File Finding
// ============================================

console.log("\n=== Recursive File Finding ===");

console.log("Find all files in directory tree:");
console.log("  dataDir = \"/project/data\";");
console.log("  allFiles = path.walk(dataDir);");
console.log("  \n  console.log(\"Total files: \" + str(len(allFiles)));");

console.log("\nFind files with specific extension:");
console.log("  allFiles = path.walk(\"/project\");");
console.log("  mlFiles = [];");
console.log("  i = 0;");
console.log("  while (i < len(allFiles)) {");
console.log("    file = allFiles[i];");
console.log("    if (path.extname(file) == \".ml\") {");
console.log("      mlFiles = mlFiles + [file];");
console.log("    }");
console.log("    i = i + 1;");
console.log("  }");
console.log("  console.log(\"Found \" + str(len(mlFiles)) + \" ML files\");");

// ============================================
// Directory Statistics
// ============================================

console.log("\n=== Directory Statistics ===");

function analyzeDirectory(dirPath) {
    console.log("\nAnalyzing directory: " + dirPath);

    // This demonstrates the analysis pattern
    console.log("  Step 1: path.listDir(dirPath)");
    console.log("  Step 2: Count total files");
    console.log("  Step 3: Group by extension");
    console.log("  Step 4: Report statistics");
}

analyzeDirectory("/data");
analyzeDirectory("/logs");

// ============================================
// File Extension Grouping
// ============================================

console.log("\n=== File Extension Grouping ===");

console.log("Group files by extension:");
console.log("  files = path.listDir(\"/data\");");
console.log("  extensions = {};");
console.log("  \n  i = 0;");
console.log("  while (i < len(files)) {");
console.log("    file = files[i];");
console.log("    ext = path.extname(file);");
console.log("    \n    // Count by extension");
console.log("    if (ext == \".txt\") {");
console.log("      // txtCount++");
console.log("    } elif (ext == \".json\") {");
console.log("      // jsonCount++");
console.log("    }");
console.log("    i = i + 1;");
console.log("  }");

// ============================================
// Directory Comparison
// ============================================

console.log("\n=== Directory Comparison ===");

function compareDirectories(dir1, dir2) {
    console.log("\nComparing directories:");
    console.log("  Dir 1: " + dir1);
    console.log("  Dir 2: " + dir2);
    console.log("  \n  files1 = path.listDir(dir1);");
    console.log("  files2 = path.listDir(dir2);");
    console.log("  \n  console.log(\"Dir 1: \" + str(len(files1)) + \" files\");");
    console.log("  console.log(\"Dir 2: \" + str(len(files2)) + \" files\");");
}

compareDirectories("/data/v1", "/data/v2");

// ============================================
// Selective File Listing
// ============================================

console.log("\n=== Selective File Listing ===");

console.log("List only JSON files:");
console.log("  files = path.listDir(\"/config\");");
console.log("  jsonFiles = [];");
console.log("  \n  i = 0;");
console.log("  while (i < len(files)) {");
console.log("    file = files[i];");
console.log("    if (path.extname(file) == \".json\") {");
console.log("      jsonFiles = jsonFiles + [file];");
console.log("    }");
console.log("    i = i + 1;");
console.log("  }");
console.log("  \n  console.log(\"Found \" + str(len(jsonFiles)) + \" JSON files\");");

console.log("\nList files matching prefix:");
console.log("  files = path.listDir(\"/logs\");");
console.log("  appLogs = [];");
console.log("  \n  i = 0;");
console.log("  while (i < len(files)) {");
console.log("    file = files[i];");
console.log("    // Check if filename starts with 'app-'");
console.log("    // appLogs = appLogs + [file];");
console.log("    i = i + 1;");
console.log("  }");

// ============================================
// Large Directory Handling
// ============================================

console.log("\n=== Large Directory Handling ===");

console.log("Process large directory efficiently:");
console.log("  files = path.listDir(\"/large-dataset\");");
console.log("  console.log(\"Processing \" + str(len(files)) + \" files...\");");
console.log("  \n  batchSize = 100;");
console.log("  i = 0;");
console.log("  while (i < len(files)) {");
console.log("    // Process batch");
console.log("    batchEnd = i + batchSize;");
console.log("    if (batchEnd > len(files)) {");
console.log("      batchEnd = len(files);");
console.log("    }");
console.log("    \n    console.log(\"Processing batch \" + str(i) + \" to \" + str(batchEnd));");
console.log("    i = batchEnd;");
console.log("  }");

// ============================================
// Directory Tree Visualization
// ============================================

console.log("\n=== Directory Tree Visualization ===");

console.log("Build directory tree:");
console.log("  rootDir = \"/project\";");
console.log("  files = path.walk(rootDir, 2);  // 2 levels deep");
console.log("  \n  console.log(\"Directory tree:\");");
console.log("  i = 0;");
console.log("  while (i < len(files)) {");
console.log("    file = files[i];");
console.log("    depth = 0;  // Calculate depth from separators");
console.log("    indent = \"\";");
console.log("    \n    j = 0;");
console.log("    while (j < depth) {");
console.log("      indent = indent + \"  \";");
console.log("      j = j + 1;");
console.log("    }");
console.log("    \n    console.log(indent + \"- \" + file);");
console.log("    i = i + 1;");
console.log("  }");

// ============================================
// File Search Operations
// ============================================

console.log("\n=== File Search Operations ===");

function findFiles(dirPath, extension) {
    console.log("\nSearching for files:");
    console.log("  Directory: " + dirPath);
    console.log("  Extension: " + extension);
    console.log("  \n  // Use glob pattern");
    console.log("  pattern = \"**/*\" + extension;");
    console.log("  results = path.glob(pattern);");
    console.log("  console.log(\"Found \" + str(len(results)) + \" files\");");
}

findFiles("/project", ".ml");
findFiles("/data", ".json");

// ============================================
// Directory Monitoring Setup
// ============================================

console.log("\n=== Directory Monitoring ===");

console.log("Monitor directory for changes:");
console.log("  watchDir = \"/data\";");
console.log("  \n  // Take initial snapshot");
console.log("  initialFiles = path.listDir(watchDir);");
console.log("  console.log(\"Initial: \" + str(len(initialFiles)) + \" files\");");
console.log("  \n  // Later, compare");
console.log("  currentFiles = path.listDir(watchDir);");
console.log("  console.log(\"Current: \" + str(len(currentFiles)) + \" files\");");
console.log("  \n  if (len(currentFiles) != len(initialFiles)) {");
console.log("    console.log(\"Directory changed!\");");
console.log("  }");

// ============================================
// Best Practices
// ============================================

console.log("\n=== Directory Listing Best Practices ===");

console.log("1. Use listDir() for simple directory listings");
console.log("2. Use glob() for pattern-based file matching");
console.log("3. Use walk() for recursive directory traversal");
console.log("4. Filter results by extension using path.extname()");
console.log("5. Build full paths using path.join(baseDir, filename)");
console.log("6. Limit walk() depth for large directory trees");
console.log("7. Process large directories in batches");
console.log("8. Cache directory listings when possible");

// ============================================
// Common Patterns Summary
// ============================================

console.log("\n=== Common Patterns Summary ===");

console.log("\nFind all files of type:");
console.log("  files = path.glob(\"**/*.txt\");");

console.log("\nList directory with full paths:");
console.log("  names = path.listDir(dir);");
console.log("  paths = names.map(n => path.join(dir, n));");

console.log("\nCount files by extension:");
console.log("  files = path.walk(dir);");
console.log("  // Count files with each extension");

console.log("\nFind recent files:");
console.log("  files = path.listDir(dir);");
console.log("  // Filter by modification time");

console.log("\n=== Directory Listing Complete ===");
