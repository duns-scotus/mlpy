"""Unit tests for path_bridge module."""

import pytest
import os
import tempfile
from pathlib import Path as PyPath

from mlpy.stdlib.path_bridge import PathModule, path as path_module
from mlpy.stdlib.decorators import get_module_metadata, _MODULE_REGISTRY


class TestPathModuleRegistration:
    """Test that Path module is properly registered with decorators."""

    def test_path_module_registered(self):
        """Test that path module is in global registry."""
        assert "path" in _MODULE_REGISTRY
        assert _MODULE_REGISTRY["path"] == PathModule

    def test_path_module_metadata(self):
        """Test path module metadata is correct."""
        metadata = get_module_metadata("path")
        assert metadata is not None
        assert metadata.name == "path"
        assert metadata.description == "Path manipulation and filesystem operations"
        assert "path.read" in metadata.capabilities
        assert "path.write" in metadata.capabilities
        assert metadata.version == "1.0.0"

    def test_path_has_function_metadata(self):
        """Test that path module has registered functions."""
        metadata = get_module_metadata("path")

        # Check key methods are registered
        assert "join" in metadata.functions
        assert "dirname" in metadata.functions
        assert "basename" in metadata.functions
        assert "extname" in metadata.functions
        assert "split" in metadata.functions
        assert "absolute" in metadata.functions
        assert "normalize" in metadata.functions
        assert "relative" in metadata.functions
        assert "exists" in metadata.functions
        assert "isFile" in metadata.functions
        assert "isDirectory" in metadata.functions
        assert "listDir" in metadata.functions
        assert "glob" in metadata.functions
        assert "walk" in metadata.functions
        assert "createDir" in metadata.functions
        assert "removeDir" in metadata.functions

        # Should have 23 functions
        assert len(metadata.functions) == 23

    def test_path_function_capabilities(self):
        """Test that path functions have correct capabilities."""
        metadata = get_module_metadata("path")

        # Pure path operations require no capabilities
        assert metadata.functions["join"].capabilities == []
        assert metadata.functions["dirname"].capabilities == []
        assert metadata.functions["basename"].capabilities == []
        assert metadata.functions["exists"].capabilities == []

        # Directory listing requires path.read
        assert metadata.functions["listDir"].capabilities == ["path.read"]
        assert metadata.functions["glob"].capabilities == ["path.read"]
        assert metadata.functions["walk"].capabilities == ["path.read"]

        # Directory management requires path.write
        assert metadata.functions["createDir"].capabilities == ["path.write"]
        assert metadata.functions["removeDir"].capabilities == ["path.write"]


class TestPathManipulation:
    """Test pure path manipulation operations (no filesystem access)."""

    def test_join_paths(self):
        """Test joining path components."""
        result = path_module.join("dir", "subdir", "file.txt")
        expected = os.path.join("dir", "subdir", "file.txt")
        assert result == expected

    def test_join_with_absolute(self):
        """Test joining with absolute path."""
        if os.name == 'nt':  # Windows
            result = path_module.join("C:", "Users", "test")
            assert "C:" in result
        else:  # Unix
            result = path_module.join("/", "home", "test")
            assert result == "/home/test"

    def test_dirname(self):
        """Test getting directory name."""
        result = path_module.dirname("/path/to/file.txt")
        assert result == "/path/to"

    def test_dirname_no_dir(self):
        """Test dirname with no directory."""
        result = path_module.dirname("file.txt")
        assert result == ""

    def test_basename(self):
        """Test getting basename."""
        result = path_module.basename("/path/to/file.txt")
        assert result == "file.txt"

    def test_basename_directory(self):
        """Test basename of directory."""
        # Without trailing slash
        result = path_module.basename("/path/to/dir")
        assert result == "dir"

        # With trailing slash may return empty on some platforms
        result_slash = path_module.basename("/path/to/dir/")
        assert result_slash in ["dir", ""]  # Platform dependent

    def test_extname(self):
        """Test getting file extension."""
        assert path_module.extname("file.txt") == ".txt"
        assert path_module.extname("archive.tar.gz") == ".gz"
        assert path_module.extname("README") == ""
        assert path_module.extname(".hidden") == ""

    def test_split_path(self):
        """Test splitting path."""
        result = path_module.split("/path/to/file.txt")
        assert result == ["/path/to", "file.txt"]

    def test_absolute_path(self):
        """Test converting to absolute path."""
        result = path_module.absolute("test.txt")
        assert os.path.isabs(result)
        assert "test.txt" in result

    def test_normalize_path(self):
        """Test normalizing path."""
        result = path_module.normalize("/path/./to/../file.txt")
        assert result == os.path.normpath("/path/./to/../file.txt")
        assert "/path/file.txt" in result or "\\path\\file.txt" in result

    def test_relative_path(self):
        """Test getting relative path."""
        result = path_module.relative("/a/b/c", "/a/b/d/e")
        expected = os.path.relpath("/a/b/d/e", "/a/b/c")
        assert result == expected

    def test_is_absolute(self):
        """Test checking if path is absolute."""
        if os.name == 'nt':  # Windows
            assert path_module.isAbsolute("C:\\path\\to\\file") is True
            assert path_module.isAbsolute("relative\\path") is False
        else:  # Unix
            assert path_module.isAbsolute("/path/to/file") is True
            assert path_module.isAbsolute("relative/path") is False


class TestPathQueries:
    """Test filesystem query operations (metadata, no write)."""

    def test_exists_true(self, tmp_path):
        """Test exists returns True for existing path."""
        test_file = tmp_path / "file.txt"
        test_file.write_text("content", encoding="utf-8")

        assert path_module.exists(str(test_file)) is True

    def test_exists_false(self, tmp_path):
        """Test exists returns False for nonexistent path."""
        assert path_module.exists(str(tmp_path / "nonexistent")) is False

    def test_is_file_true(self, tmp_path):
        """Test isFile returns True for file."""
        test_file = tmp_path / "file.txt"
        test_file.write_text("content", encoding="utf-8")

        assert path_module.isFile(str(test_file)) is True

    def test_is_file_false_for_directory(self, tmp_path):
        """Test isFile returns False for directory."""
        assert path_module.isFile(str(tmp_path)) is False

    def test_is_directory_true(self, tmp_path):
        """Test isDirectory returns True for directory."""
        assert path_module.isDirectory(str(tmp_path)) is True

    def test_is_directory_false_for_file(self, tmp_path):
        """Test isDirectory returns False for file."""
        test_file = tmp_path / "file.txt"
        test_file.write_text("content", encoding="utf-8")

        assert path_module.isDirectory(str(test_file)) is False


class TestDirectoryListing:
    """Test directory listing operations (require path.read capability)."""

    def test_list_dir(self, tmp_path):
        """Test listing directory contents."""
        # Create test files
        (tmp_path / "file1.txt").write_text("content", encoding="utf-8")
        (tmp_path / "file2.txt").write_text("content", encoding="utf-8")
        (tmp_path / "subdir").mkdir()

        files = path_module.listDir(str(tmp_path))

        assert "file1.txt" in files
        assert "file2.txt" in files
        assert "subdir" in files
        assert len(files) == 3

    def test_list_dir_sorted(self, tmp_path):
        """Test listDir returns sorted results."""
        (tmp_path / "c.txt").write_text("", encoding="utf-8")
        (tmp_path / "a.txt").write_text("", encoding="utf-8")
        (tmp_path / "b.txt").write_text("", encoding="utf-8")

        files = path_module.listDir(str(tmp_path))

        assert files == ["a.txt", "b.txt", "c.txt"]

    def test_list_dir_error_on_file(self, tmp_path):
        """Test listDir raises error on file."""
        test_file = tmp_path / "file.txt"
        test_file.write_text("content", encoding="utf-8")

        with pytest.raises(NotADirectoryError):
            path_module.listDir(str(test_file))

    def test_glob_pattern(self, tmp_path):
        """Test glob pattern matching."""
        (tmp_path / "file1.txt").write_text("", encoding="utf-8")
        (tmp_path / "file2.txt").write_text("", encoding="utf-8")
        (tmp_path / "file.md").write_text("", encoding="utf-8")

        pattern = str(tmp_path / "*.txt")
        files = path_module.glob(pattern)

        assert len(files) == 2
        assert any("file1.txt" in f for f in files)
        assert any("file2.txt" in f for f in files)

    def test_glob_recursive(self, tmp_path):
        """Test recursive glob pattern."""
        (tmp_path / "file.txt").write_text("", encoding="utf-8")
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "file.txt").write_text("", encoding="utf-8")

        pattern = str(tmp_path / "**" / "*.txt")
        files = path_module.glob(pattern)

        assert len(files) == 2

    def test_walk_directory(self, tmp_path):
        """Test walking directory tree."""
        # Create directory structure
        (tmp_path / "file1.txt").write_text("", encoding="utf-8")
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "file2.txt").write_text("", encoding="utf-8")
        nested = subdir / "nested"
        nested.mkdir()
        (nested / "file3.txt").write_text("", encoding="utf-8")

        files = path_module.walk(str(tmp_path))

        assert len(files) == 3
        assert "file1.txt" in files
        assert any("file2.txt" in f for f in files)
        assert any("file3.txt" in f for f in files)

    def test_walk_with_max_depth(self, tmp_path):
        """Test walking with max depth limit."""
        (tmp_path / "file1.txt").write_text("", encoding="utf-8")
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "file2.txt").write_text("", encoding="utf-8")
        nested = subdir / "nested"
        nested.mkdir()
        (nested / "file3.txt").write_text("", encoding="utf-8")

        files = path_module.walk(str(tmp_path), max_depth=1)

        # Should only get file1.txt and file2.txt, not file3.txt
        assert len(files) == 2
        assert "file1.txt" in files
        assert any("file2.txt" in f for f in files)
        assert not any("file3.txt" in f for f in files)


class TestDirectoryManagement:
    """Test directory management operations (require path.write capability)."""

    def test_create_dir(self, tmp_path):
        """Test creating directory."""
        new_dir = tmp_path / "newdir"
        path_module.createDir(str(new_dir))

        assert new_dir.exists()
        assert new_dir.is_dir()

    def test_create_dir_with_parents(self, tmp_path):
        """Test creating directory with parents."""
        nested_dir = tmp_path / "a" / "b" / "c"
        path_module.createDir(str(nested_dir), parents=True)

        assert nested_dir.exists()
        assert nested_dir.is_dir()

    def test_create_dir_already_exists(self, tmp_path):
        """Test creating directory that already exists."""
        test_dir = tmp_path / "dir"
        test_dir.mkdir()

        # Should not raise error
        path_module.createDir(str(test_dir))
        assert test_dir.exists()

    def test_remove_empty_dir(self, tmp_path):
        """Test removing empty directory."""
        test_dir = tmp_path / "emptydir"
        test_dir.mkdir()

        path_module.removeDir(str(test_dir))
        assert not test_dir.exists()

    def test_remove_non_empty_dir_fails(self, tmp_path):
        """Test removing non-empty directory fails."""
        test_dir = tmp_path / "dir"
        test_dir.mkdir()
        (test_dir / "file.txt").write_text("content", encoding="utf-8")

        with pytest.raises(OSError):
            path_module.removeDir(str(test_dir))

    def test_remove_dir_recursive(self, tmp_path):
        """Test removing directory recursively."""
        test_dir = tmp_path / "dir"
        test_dir.mkdir()
        (test_dir / "file.txt").write_text("content", encoding="utf-8")
        subdir = test_dir / "subdir"
        subdir.mkdir()
        (subdir / "file2.txt").write_text("content", encoding="utf-8")

        path_module.removeDirRecursive(str(test_dir))
        assert not test_dir.exists()


class TestPathUtilities:
    """Test path utility functions."""

    def test_cwd(self):
        """Test getting current working directory."""
        cwd = path_module.cwd()
        assert os.path.isabs(cwd)
        assert cwd == os.getcwd()

    def test_home(self):
        """Test getting home directory."""
        home = path_module.home()
        assert os.path.isabs(home)
        assert home == str(PyPath.home())

    def test_temp_dir(self):
        """Test getting temp directory."""
        temp = path_module.tempDir()
        assert os.path.isabs(temp)
        assert os.path.exists(temp)

    def test_separator(self):
        """Test getting path separator."""
        sep = path_module.separator()
        assert sep == os.sep
        assert sep in ['/', '\\']

    def test_delimiter(self):
        """Test getting path delimiter."""
        delim = path_module.delimiter()
        assert delim == os.pathsep
        assert delim in [':', ';']
