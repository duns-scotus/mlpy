// Test stdlib module: path - Path manipulation and filesystem operations
// Features tested: join, dirname, basename, extname, listDir, createDir, glob, walk
// Module: path (requires capabilities: path.read, path.write)

import path;
import file;

function test_path_join() {
    results = {};

    // Join path components
    results.simple = path.join("dir", "file.txt");
    results.nested = path.join("a", "b", "c", "file.txt");
    results.three = path.join("root", "sub", "file");

    // All should contain the components
    results.simple_ok = results.simple != "";          // true
    results.nested_ok = results.nested != "";          // true
    results.three_ok = results.three != "";            // true

    return results;
}

function test_path_components() {
    results = {};

    test_path = "/path/to/document.txt";

    // Get directory name
    dir = path.dirname(test_path);
    results.dirname = dir;                             // "/path/to"

    // Get file name
    base = path.basename(test_path);
    results.basename = base;                           // "document.txt"

    // Get extension
    ext = path.extname(test_path);
    results.extname = ext;                             // ".txt"

    // Split path
    parts = path.split(test_path);
    results.split_count = len(parts);                  // 2
    results.split_dir = parts[0];                      // "/path/to"
    results.split_file = parts[1];                     // "document.txt"

    return results;
}

function test_extension_extraction() {
    results = {};

    // Various file extensions
    results.txt_ext = path.extname("file.txt");        // ".txt"
    results.tar_gz = path.extname("archive.tar.gz");   // ".gz"
    results.no_ext = path.extname("README");           // ""
    results.hidden = path.extname(".gitignore");       // ".gitignore" or ""

    // Extension presence checks
    results.has_txt = results.txt_ext == ".txt";       // true
    results.has_gz = results.tar_gz == ".gz";          // true
    results.no_extension = results.no_ext == "";       // true

    return results;
}

function test_path_normalization() {
    results = {};

    // Normalize various paths
    results.with_dot = path.normalize("/path/./to/file");
    results.with_dotdot = path.normalize("/path/to/../file");
    results.multiple_sep = path.normalize("path//to///file");

    // All should be normalized (no dots, single separators)
    results.normalized_ok = len(results.with_dot) > 0;  // true

    return results;
}

function test_absolute_paths() {
    results = {};

    // Convert relative to absolute
    abs_path = path.absolute("relative/path.txt");

    // Should be absolute
    results.is_absolute = path.isAbsolute(abs_path);   // true
    results.has_content = len(abs_path) > 0;           // true

    // Check relative detection
    results.relative_detected = path.isAbsolute("relative/path") == false;  // true

    return results;
}

function test_system_paths() {
    results = {};

    // Get system paths
    cwd = path.cwd();
    home = path.home();
    temp = path.tempDir();

    // All should be non-empty absolute paths
    results.has_cwd = len(cwd) > 0;                    // true
    results.has_home = len(home) > 0;                  // true
    results.has_temp = len(temp) > 0;                  // true

    results.cwd_absolute = path.isAbsolute(cwd);       // true
    results.home_absolute = path.isAbsolute(home);     // true
    results.temp_absolute = path.isAbsolute(temp);     // true

    return results;
}

function test_path_separators() {
    results = {};

    // Get OS-specific separators
    sep = path.separator();
    delim = path.delimiter();

    // Should be valid separators
    results.has_separator = len(sep) > 0;              // true
    results.has_delimiter = len(delim) > 0;            // true

    // Common separators
    results.is_slash_or_backslash = (sep == "/" || sep == "\\");  // true
    results.is_colon_or_semicolon = (delim == ":" || delim == ";");  // true

    return results;
}

function test_create_directory() {
    results = {};

    temp = path.tempDir();
    test_dir = path.join(temp, "mlpy_test_dir");

    // Create directory
    path.createDir(test_dir);

    // Should exist
    results.created = path.exists(test_dir);           // true
    results.is_dir = path.isDirectory(test_dir);       // true
    results.not_file = path.isFile(test_dir) == false; // true

    // Create already exists (should not error)
    path.createDir(test_dir);
    results.still_exists = path.exists(test_dir);      // true

    // Clean up
    path.removeDir(test_dir);
    results.removed = path.exists(test_dir) == false;  // true

    return results;
}

function test_nested_directory_creation() {
    results = {};

    temp = path.tempDir();
    nested = path.join(temp, "mlpy_test_a", "b", "c", "d");

    // Create nested directories
    path.createDir(nested, true);

    // Should exist
    results.nested_created = path.exists(nested);      // true
    results.nested_is_dir = path.isDirectory(nested);  // true

    // Parent directories should exist too
    parent = path.join(temp, "mlpy_test_a", "b");
    results.parent_exists = path.exists(parent);       // true

    // Note: Cleanup of nested dirs requires recursive removal
    // We'll leave cleanup for now since removeDir only handles empty dirs

    return results;
}

function test_list_directory() {
    results = {};

    // Create test directory with files
    temp = path.tempDir();
    test_dir = path.join(temp, "mlpy_test_list");
    path.createDir(test_dir);

    // Create some files
    file.write(path.join(test_dir, "file1.txt"), "content");
    file.write(path.join(test_dir, "file2.txt"), "content");
    file.write(path.join(test_dir, "file3.md"), "content");

    // List directory
    files = path.listDir(test_dir);

    results.file_count = len(files);                   // 3
    results.has_files = len(files) > 0;                // true

    // Files should be in list (order may vary)
    has_file1 = false;
    has_file2 = false;
    has_file3 = false;

    for (f in files) {
        if (f == "file1.txt") { has_file1 = true; }
        if (f == "file2.txt") { has_file2 = true; }
        if (f == "file3.md") { has_file3 = true; }
    }

    results.found_file1 = has_file1;                   // true
    results.found_file2 = has_file2;                   // true
    results.found_file3 = has_file3;                   // true

    // Clean up
    file.delete(path.join(test_dir, "file1.txt"));
    file.delete(path.join(test_dir, "file2.txt"));
    file.delete(path.join(test_dir, "file3.md"));
    path.removeDir(test_dir);

    return results;
}

function test_glob_patterns() {
    results = {};

    // Create test files
    temp = path.tempDir();
    test_dir = path.join(temp, "mlpy_test_glob");
    path.createDir(test_dir);

    file.write(path.join(test_dir, "file1.txt"), "");
    file.write(path.join(test_dir, "file2.txt"), "");
    file.write(path.join(test_dir, "data.json"), "");
    file.write(path.join(test_dir, "README.md"), "");

    // Glob for .txt files
    pattern = path.join(test_dir, "*.txt");
    txt_files = path.glob(pattern);

    results.found_txt = len(txt_files);                // 2

    // Check files contain expected names
    has_txt = false;
    for (f in txt_files) {
        if (f != "") { has_txt = true; }
    }
    results.has_txt_files = has_txt;                   // true

    // Clean up
    file.delete(path.join(test_dir, "file1.txt"));
    file.delete(path.join(test_dir, "file2.txt"));
    file.delete(path.join(test_dir, "data.json"));
    file.delete(path.join(test_dir, "README.md"));
    path.removeDir(test_dir);

    return results;
}

function test_walk_directory() {
    results = {};

    // Create nested directory structure
    temp = path.tempDir();
    root = path.join(temp, "mlpy_test_walk");
    path.createDir(root);

    // Create files in root
    file.write(path.join(root, "root.txt"), "");

    // Create subdirectory with files
    sub = path.join(root, "subdir");
    path.createDir(sub);
    file.write(path.join(sub, "sub.txt"), "");

    // Walk directory tree
    all_files = path.walk(root);

    results.total_files = len(all_files);              // 2 (root.txt, subdir/sub.txt)
    results.found_files = len(all_files) > 0;          // true

    // Clean up
    file.delete(path.join(root, "root.txt"));
    file.delete(path.join(sub, "sub.txt"));
    path.removeDir(sub);
    path.removeDir(root);

    return results;
}

function test_exists_checks() {
    results = {};

    temp = path.tempDir();

    // Check temp directory exists
    results.temp_exists = path.exists(temp);           // true
    results.temp_is_dir = path.isDirectory(temp);      // true

    // Check nonexistent path
    nonexistent = path.join(temp, "mlpy_nonexistent_xyz123");
    results.not_exists = path.exists(nonexistent) == false;  // true

    // Create file and check
    test_file = path.join(temp, "mlpy_test_exists.txt");
    file.write(test_file, "test");

    results.file_exists = path.exists(test_file);      // true
    results.file_is_file = path.isFile(test_file);     // true
    results.file_not_dir = path.isDirectory(test_file) == false;  // true

    // Clean up
    file.delete(test_file);

    return results;
}

function test_relative_paths() {
    results = {};

    // Test relative path calculation
    from = "/a/b/c";
    to = "/a/b/d/e";

    rel = path.relative(from, to);
    results.has_relative = len(rel) > 0;               // true
    results.is_relative = path.isAbsolute(rel) == false;  // true

    return results;
}

function test_practical_path_building() {
    results = {};

    // Build paths for common scenarios
    temp = path.tempDir();

    // Data directory
    data_dir = path.join(temp, "mlpy_app_data");
    results.data_path = data_dir;

    // Log file path
    log_file = path.join(data_dir, "app.log");
    results.log_path = log_file;

    // Config file path
    config_file = path.join(data_dir, "config.json");
    results.config_path = config_file;

    // All paths should be non-empty
    results.has_data_path = len(data_dir) > 0;         // true
    results.has_log_path = len(log_file) > 0;          // true
    results.has_config_path = len(config_file) > 0;    // true

    return results;
}

function main() {
    all_results = {};

    all_results.join = test_path_join();
    all_results.components = test_path_components();
    all_results.extensions = test_extension_extraction();
    all_results.normalize = test_path_normalization();
    all_results.absolute = test_absolute_paths();
    all_results.system = test_system_paths();
    all_results.separators = test_path_separators();
    all_results.create_dir = test_create_directory();
    all_results.nested_dir = test_nested_directory_creation();
    all_results.list_dir = test_list_directory();
    all_results.glob = test_glob_patterns();
    all_results.walk = test_walk_directory();
    all_results.exists = test_exists_checks();
    all_results.relative = test_relative_paths();
    all_results.practical = test_practical_path_building();

    return all_results;
}

// Run tests
test_results = main();
