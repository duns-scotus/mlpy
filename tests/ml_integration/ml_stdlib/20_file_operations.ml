// Test stdlib module: file - File I/O operations
// Features tested: read, write, readLines, writeLines, append, delete, copy, exists
// Module: file (requires capabilities: file.read, file.write, file.append, file.delete)

import file;
import path;

function test_write_and_read() {
    results = {};

    // Write text file
    test_path = path.join(path.tempDir(), "mlpy_test_file.txt");
    file.write(test_path, "Hello from ML!");

    // Read it back
    content = file.read(test_path);
    results.content_matches = content == "Hello from ML!";

    // Check it exists
    results.file_exists = file.exists(test_path);

    // Clean up
    file.delete(test_path);
    results.file_deleted = file.exists(test_path) == false;

    return results;
}

function test_read_write_lines() {
    results = {};

    test_path = path.join(path.tempDir(), "mlpy_test_lines.txt");

    // Write array of lines
    lines = ["First line", "Second line", "Third line"];
    file.writeLines(test_path, lines);

    // Read lines back
    read_lines = file.readLines(test_path);

    results.line_count = len(read_lines);              // 3
    if (len(read_lines) > 0) { results.first_line = read_lines[0]; }
    if (len(read_lines) > 1) { results.second_line = read_lines[1]; }
    if (len(read_lines) > 2) { results.third_line = read_lines[2]; }

    // Clean up
    file.delete(test_path);

    return results;
}

function test_append_operation() {
    results = {};

    test_path = path.join(path.tempDir(), "mlpy_test_append.txt");

    // Write initial content
    file.write(test_path, "Line 1\n");

    // Append more content
    file.append(test_path, "Line 2\n");
    file.append(test_path, "Line 3\n");

    // Read all lines
    lines = file.readLines(test_path);

    results.total_lines = len(lines);                  // 3

    // Defensive indexing to avoid errors
    if (len(lines) > 0) { results.first = lines[0]; }
    if (len(lines) > 1) { results.second = lines[1]; }
    if (len(lines) > 2) { results.third = lines[2]; }

    // Clean up
    file.delete(test_path);

    return results;
}

function test_file_metadata() {
    results = {};

    test_path = path.join(path.tempDir(), "mlpy_test_metadata.txt");
    content = "Test content for metadata";

    // Write file
    file.write(test_path, content);

    // Get size
    size = file.size(test_path);
    results.has_size = size > 0;                       // true
    results.size_matches = size == len(content);       // true

    // Get modification time
    mtime = file.modifiedTime(test_path);
    results.has_mtime = mtime > 0;                     // true

    // Check type
    results.is_file = file.isFile(test_path);          // true
    results.is_not_dir = file.isDirectory(test_path) == false;  // true

    // Clean up
    file.delete(test_path);

    return results;
}

function test_copy_file() {
    results = {};

    temp_dir = path.tempDir();
    source = path.join(temp_dir, "mlpy_test_source.txt");
    dest = path.join(temp_dir, "mlpy_test_dest.txt");

    // Write source file
    file.write(source, "Original content");

    // Copy it
    file.copy(source, dest);

    // Both should exist
    results.source_exists = file.exists(source);       // true
    results.dest_exists = file.exists(dest);           // true

    // Read destination
    dest_content = file.read(dest);
    results.content_copied = dest_content == "Original content";  // true

    // Clean up
    file.delete(source);
    file.delete(dest);

    return results;
}

function test_move_file() {
    results = {};

    temp_dir = path.tempDir();
    source = path.join(temp_dir, "mlpy_test_move_src.txt");
    dest = path.join(temp_dir, "mlpy_test_move_dst.txt");

    // Write source file
    file.write(source, "Content to move");

    // Move it
    file.move(source, dest);

    // Source should not exist, dest should
    results.source_gone = file.exists(source) == false;  // true
    results.dest_exists = file.exists(dest);             // true

    // Read destination
    dest_content = file.read(dest);
    results.content_moved = dest_content == "Content to move";  // true

    // Clean up
    file.delete(dest);

    return results;
}

function test_nested_directories() {
    results = {};

    // Write to nested path (should create directories)
    temp_dir = path.tempDir();
    nested_path = path.join(temp_dir, "mlpy_test_a", "b", "c", "file.txt");

    file.write(nested_path, "Nested file content");

    // Should exist
    results.file_created = file.exists(nested_path);   // true

    // Read it back
    content = file.read(nested_path);
    results.content_ok = content == "Nested file content";  // true

    // Check directory exists
    dir_path = path.join(temp_dir, "mlpy_test_a", "b", "c");
    results.dir_exists = file.isDirectory(dir_path);   // true

    // Clean up (delete file, directory cleanup handled separately)
    file.delete(nested_path);

    return results;
}

function test_delete_operations() {
    results = {};

    temp_dir = path.tempDir();
    test_file = path.join(temp_dir, "mlpy_test_delete.txt");

    // Create file
    file.write(test_file, "To be deleted");
    results.created = file.exists(test_file);          // true

    // Delete it
    deleted = file.delete(test_file);
    results.delete_returned_true = deleted;            // true
    results.file_gone = file.exists(test_file) == false;  // true

    // Delete nonexistent returns false
    deleted_again = file.delete(test_file);
    results.delete_nonexistent_false = deleted_again == false;  // true

    return results;
}

function test_multiple_operations() {
    results = {};

    temp_dir = path.tempDir();

    // Create multiple files
    file1 = path.join(temp_dir, "mlpy_multi_1.txt");
    file2 = path.join(temp_dir, "mlpy_multi_2.txt");
    file3 = path.join(temp_dir, "mlpy_multi_3.txt");

    file.write(file1, "File 1");
    file.write(file2, "File 2");
    file.write(file3, "File 3");

    // All exist
    count = 0;
    if (file.exists(file1)) { count = count + 1; }
    if (file.exists(file2)) { count = count + 1; }
    if (file.exists(file3)) { count = count + 1; }

    results.all_created = count == 3;                  // true

    // Read all
    content1 = file.read(file1);
    content2 = file.read(file2);
    content3 = file.read(file3);

    results.all_readable = (
        content1 == "File 1" &&
        content2 == "File 2" &&
        content3 == "File 3"
    );                                                  // true

    // Clean up all
    file.delete(file1);
    file.delete(file2);
    file.delete(file3);

    count_after = 0;
    if (file.exists(file1)) { count_after = count_after + 1; }
    if (file.exists(file2)) { count_after = count_after + 1; }
    if (file.exists(file3)) { count_after = count_after + 1; }

    results.all_deleted = count_after == 0;            // true

    return results;
}

function test_log_file_pattern() {
    results = {};

    // Simulate log file usage
    temp_dir = path.tempDir();
    log_path = path.join(temp_dir, "mlpy_test_app.log");

    // Write initial log entry
    file.write(log_path, "[INFO] Application started\n");

    // Append more entries
    file.append(log_path, "[DEBUG] Processing data\n");
    file.append(log_path, "[INFO] Task completed\n");
    file.append(log_path, "[WARN] Low memory\n");

    // Read all log lines
    log_lines = file.readLines(log_path);

    results.log_count = len(log_lines);                // 4
    if (len(log_lines) > 0) { results.first_entry = log_lines[0]; }
    if (len(log_lines) > 3) { results.last_entry = log_lines[3]; }

    // Check log file size
    log_size = file.size(log_path);
    results.log_has_size = log_size > 0;               // true

    // Clean up
    file.delete(log_path);

    return results;
}

function test_config_file_pattern() {
    results = {};

    // Simulate config file management
    temp_dir = path.tempDir();
    config_path = path.join(temp_dir, "mlpy_test_config.txt");

    // Write configuration
    config_lines = [
        "app.name=MyApp",
        "app.version=1.0.0",
        "app.port=8080",
        "app.debug=false"
    ];

    file.writeLines(config_path, config_lines);

    // Read configuration
    loaded_config = file.readLines(config_path);

    results.config_count = len(loaded_config);         // 4
    if (len(loaded_config) > 0) { results.has_name = loaded_config[0] == "app.name=MyApp"; }
    if (len(loaded_config) > 1) { results.has_version = loaded_config[1] == "app.version=1.0.0"; }
    if (len(loaded_config) > 2) { results.has_port = loaded_config[2] == "app.port=8080"; }

    // Clean up
    file.delete(config_path);

    return results;
}

function test_backup_pattern() {
    results = {};

    temp_dir = path.tempDir();
    original = path.join(temp_dir, "mlpy_test_data.txt");
    backup = path.join(temp_dir, "mlpy_test_data.txt.bak");

    // Write original file
    file.write(original, "Important data v1");

    // Create backup
    file.copy(original, backup);

    // Modify original
    file.write(original, "Important data v2");

    // Both files exist
    results.original_exists = file.exists(original);   // true
    results.backup_exists = file.exists(backup);       // true

    // Contents different
    original_content = file.read(original);
    backup_content = file.read(backup);

    results.original_updated = original_content == "Important data v2";  // true
    results.backup_preserved = backup_content == "Important data v1";    // true

    // Clean up
    file.delete(original);
    file.delete(backup);

    return results;
}

function main() {
    all_results = {};

    all_results.write_read = test_write_and_read();
    all_results.lines = test_read_write_lines();
    all_results.append = test_append_operation();
    all_results.metadata = test_file_metadata();
    all_results.copy = test_copy_file();
    all_results.move = test_move_file();
    all_results.nested = test_nested_directories();
    all_results.delete = test_delete_operations();
    all_results.multiple = test_multiple_operations();
    all_results.log_pattern = test_log_file_pattern();
    all_results.config_pattern = test_config_file_pattern();
    all_results.backup_pattern = test_backup_pattern();

    return all_results;
}

// Run tests
test_results = main();
