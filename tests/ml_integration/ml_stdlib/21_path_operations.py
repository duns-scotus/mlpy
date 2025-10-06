"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin

from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access, safe_method_call as _safe_method_call, get_safe_length

from mlpy.stdlib.path_bridge import path

from mlpy.stdlib.file_bridge import file

def test_path_join():
    results = {}
    results['simple'] = _safe_call(path.join, 'dir', 'file.txt')
    results['nested'] = _safe_call(path.join, 'a', 'b', 'c', 'file.txt')
    results['three'] = _safe_call(path.join, 'root', 'sub', 'file')
    results['simple_ok'] = (_safe_attr_access(results, 'simple') != '')
    results['nested_ok'] = (_safe_attr_access(results, 'nested') != '')
    results['three_ok'] = (_safe_attr_access(results, 'three') != '')
    return results

def test_path_components():
    results = {}
    test_path = '/path/to/document.txt'
    dir = _safe_call(path.dirname, test_path)
    results['dirname'] = dir
    base = _safe_call(path.basename, test_path)
    results['basename'] = base
    ext = _safe_call(path.extname, test_path)
    results['extname'] = ext
    parts = _safe_call(path.split, test_path)
    results['split_count'] = _safe_call(builtin.len, parts)
    results['split_dir'] = parts[0]
    results['split_file'] = parts[1]
    return results

def test_extension_extraction():
    results = {}
    results['txt_ext'] = _safe_call(path.extname, 'file.txt')
    results['tar_gz'] = _safe_call(path.extname, 'archive.tar.gz')
    results['no_ext'] = _safe_call(path.extname, 'README')
    results['hidden'] = _safe_call(path.extname, '.gitignore')
    results['has_txt'] = (_safe_attr_access(results, 'txt_ext') == '.txt')
    results['has_gz'] = (_safe_attr_access(results, 'tar_gz') == '.gz')
    results['no_extension'] = (_safe_attr_access(results, 'no_ext') == '')
    return results

def test_path_normalization():
    results = {}
    results['with_dot'] = _safe_call(path.normalize, '/path/./to/file')
    results['with_dotdot'] = _safe_call(path.normalize, '/path/to/../file')
    results['multiple_sep'] = _safe_call(path.normalize, 'path//to///file')
    results['normalized_ok'] = (_safe_call(builtin.len, _safe_attr_access(results, 'with_dot')) > 0)
    return results

def test_absolute_paths():
    results = {}
    abs_path = _safe_call(path.absolute, 'relative/path.txt')
    results['is_absolute'] = _safe_call(path.isAbsolute, abs_path)
    results['has_content'] = (_safe_call(builtin.len, abs_path) > 0)
    results['relative_detected'] = (_safe_call(path.isAbsolute, 'relative/path') == False)
    return results

def test_system_paths():
    results = {}
    cwd = _safe_call(path.cwd)
    home = _safe_call(path.home)
    temp = _safe_call(path.tempDir)
    results['has_cwd'] = (_safe_call(builtin.len, cwd) > 0)
    results['has_home'] = (_safe_call(builtin.len, home) > 0)
    results['has_temp'] = (_safe_call(builtin.len, temp) > 0)
    results['cwd_absolute'] = _safe_call(path.isAbsolute, cwd)
    results['home_absolute'] = _safe_call(path.isAbsolute, home)
    results['temp_absolute'] = _safe_call(path.isAbsolute, temp)
    return results

def test_path_separators():
    results = {}
    sep = _safe_call(path.separator)
    delim = _safe_call(path.delimiter)
    results['has_separator'] = (_safe_call(builtin.len, sep) > 0)
    results['has_delimiter'] = (_safe_call(builtin.len, delim) > 0)
    results['is_slash_or_backslash'] = ((sep == '/') or (sep == '\\\\'))
    results['is_colon_or_semicolon'] = ((delim == ':') or (delim == ';'))
    return results

def test_create_directory():
    results = {}
    temp = _safe_call(path.tempDir)
    test_dir = _safe_call(path.join, temp, 'mlpy_test_dir')
    _safe_call(path.createDir, test_dir)
    results['created'] = _safe_call(path.exists, test_dir)
    results['is_dir'] = _safe_call(path.isDirectory, test_dir)
    results['not_file'] = (_safe_call(path.isFile, test_dir) == False)
    _safe_call(path.createDir, test_dir)
    results['still_exists'] = _safe_call(path.exists, test_dir)
    _safe_call(path.removeDir, test_dir)
    results['removed'] = (_safe_call(path.exists, test_dir) == False)
    return results

def test_nested_directory_creation():
    results = {}
    temp = _safe_call(path.tempDir)
    nested = _safe_call(path.join, temp, 'mlpy_test_a', 'b', 'c', 'd')
    _safe_call(path.createDir, nested, True)
    results['nested_created'] = _safe_call(path.exists, nested)
    results['nested_is_dir'] = _safe_call(path.isDirectory, nested)
    parent = _safe_call(path.join, temp, 'mlpy_test_a', 'b')
    results['parent_exists'] = _safe_call(path.exists, parent)
    return results

def test_list_directory():
    results = {}
    temp = _safe_call(path.tempDir)
    test_dir = _safe_call(path.join, temp, 'mlpy_test_list')
    _safe_call(path.createDir, test_dir)
    _safe_call(file.write, _safe_call(path.join, test_dir, 'file1.txt'), 'content')
    _safe_call(file.write, _safe_call(path.join, test_dir, 'file2.txt'), 'content')
    _safe_call(file.write, _safe_call(path.join, test_dir, 'file3.md'), 'content')
    files = _safe_call(path.listDir, test_dir)
    results['file_count'] = _safe_call(builtin.len, files)
    results['has_files'] = (_safe_call(builtin.len, files) > 0)
    has_file1 = False
    has_file2 = False
    has_file3 = False
    for f in files:
        if (f == 'file1.txt'):
            has_file1 = True
        if (f == 'file2.txt'):
            has_file2 = True
        if (f == 'file3.md'):
            has_file3 = True
    results['found_file1'] = has_file1
    results['found_file2'] = has_file2
    results['found_file3'] = has_file3
    _safe_call(file.delete, _safe_call(path.join, test_dir, 'file1.txt'))
    _safe_call(file.delete, _safe_call(path.join, test_dir, 'file2.txt'))
    _safe_call(file.delete, _safe_call(path.join, test_dir, 'file3.md'))
    _safe_call(path.removeDir, test_dir)
    return results

def test_glob_patterns():
    results = {}
    temp = _safe_call(path.tempDir)
    test_dir = _safe_call(path.join, temp, 'mlpy_test_glob')
    _safe_call(path.createDir, test_dir)
    _safe_call(file.write, _safe_call(path.join, test_dir, 'file1.txt'), '')
    _safe_call(file.write, _safe_call(path.join, test_dir, 'file2.txt'), '')
    _safe_call(file.write, _safe_call(path.join, test_dir, 'data.json'), '')
    _safe_call(file.write, _safe_call(path.join, test_dir, 'README.md'), '')
    pattern = _safe_call(path.join, test_dir, '*.txt')
    txt_files = _safe_call(path.glob, pattern)
    results['found_txt'] = _safe_call(builtin.len, txt_files)
    has_txt = False
    for f in txt_files:
        if (f != ''):
            has_txt = True
    results['has_txt_files'] = has_txt
    _safe_call(file.delete, _safe_call(path.join, test_dir, 'file1.txt'))
    _safe_call(file.delete, _safe_call(path.join, test_dir, 'file2.txt'))
    _safe_call(file.delete, _safe_call(path.join, test_dir, 'data.json'))
    _safe_call(file.delete, _safe_call(path.join, test_dir, 'README.md'))
    _safe_call(path.removeDir, test_dir)
    return results

def test_walk_directory():
    results = {}
    temp = _safe_call(path.tempDir)
    root = _safe_call(path.join, temp, 'mlpy_test_walk')
    _safe_call(path.createDir, root)
    _safe_call(file.write, _safe_call(path.join, root, 'root.txt'), '')
    sub = _safe_call(path.join, root, 'subdir')
    _safe_call(path.createDir, sub)
    _safe_call(file.write, _safe_call(path.join, sub, 'sub.txt'), '')
    all_files = _safe_call(path.walk, root)
    results['total_files'] = _safe_call(builtin.len, all_files)
    results['found_files'] = (_safe_call(builtin.len, all_files) > 0)
    _safe_call(file.delete, _safe_call(path.join, root, 'root.txt'))
    _safe_call(file.delete, _safe_call(path.join, sub, 'sub.txt'))
    _safe_call(path.removeDir, sub)
    _safe_call(path.removeDir, root)
    return results

def test_exists_checks():
    results = {}
    temp = _safe_call(path.tempDir)
    results['temp_exists'] = _safe_call(path.exists, temp)
    results['temp_is_dir'] = _safe_call(path.isDirectory, temp)
    nonexistent = _safe_call(path.join, temp, 'mlpy_nonexistent_xyz123')
    results['not_exists'] = (_safe_call(path.exists, nonexistent) == False)
    test_file = _safe_call(path.join, temp, 'mlpy_test_exists.txt')
    _safe_call(file.write, test_file, 'test')
    results['file_exists'] = _safe_call(path.exists, test_file)
    results['file_is_file'] = _safe_call(path.isFile, test_file)
    results['file_not_dir'] = (_safe_call(path.isDirectory, test_file) == False)
    _safe_call(file.delete, test_file)
    return results

def test_relative_paths():
    results = {}
    ml_from = '/a/b/c'
    to = '/a/b/d/e'
    rel = _safe_call(path.relative, ml_from, to)
    results['has_relative'] = (_safe_call(builtin.len, rel) > 0)
    results['is_relative'] = (_safe_call(path.isAbsolute, rel) == False)
    return results

def test_practical_path_building():
    results = {}
    temp = _safe_call(path.tempDir)
    data_dir = _safe_call(path.join, temp, 'mlpy_app_data')
    results['data_path'] = data_dir
    log_file = _safe_call(path.join, data_dir, 'app.log')
    results['log_path'] = log_file
    config_file = _safe_call(path.join, data_dir, 'config.json')
    results['config_path'] = config_file
    results['has_data_path'] = (_safe_call(builtin.len, data_dir) > 0)
    results['has_log_path'] = (_safe_call(builtin.len, log_file) > 0)
    results['has_config_path'] = (_safe_call(builtin.len, config_file) > 0)
    return results

def main():
    all_results = {}
    all_results['join'] = test_path_join()
    all_results['components'] = test_path_components()
    all_results['extensions'] = test_extension_extraction()
    all_results['normalize'] = test_path_normalization()
    all_results['absolute'] = test_absolute_paths()
    all_results['system'] = test_system_paths()
    all_results['separators'] = test_path_separators()
    all_results['create_dir'] = test_create_directory()
    all_results['nested_dir'] = test_nested_directory_creation()
    all_results['list_dir'] = test_list_directory()
    all_results['glob'] = test_glob_patterns()
    all_results['walk'] = test_walk_directory()
    all_results['exists'] = test_exists_checks()
    all_results['relative'] = test_relative_paths()
    all_results['practical'] = test_practical_path_building()
    return all_results

test_results = main()

# End of generated code