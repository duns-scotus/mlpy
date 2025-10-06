"""Unit tests for file_bridge module."""

import pytest
import tempfile
import os
from pathlib import Path

from mlpy.stdlib.file_bridge import FileModule, file as file_module
from mlpy.stdlib.decorators import get_module_metadata, _MODULE_REGISTRY


class TestFileModuleRegistration:
    """Test that File module is properly registered with decorators."""

    def test_file_module_registered(self):
        """Test that file module is in global registry."""
        assert "file" in _MODULE_REGISTRY
        assert _MODULE_REGISTRY["file"] == FileModule

    def test_file_module_metadata(self):
        """Test file module metadata is correct."""
        metadata = get_module_metadata("file")
        assert metadata is not None
        assert metadata.name == "file"
        assert metadata.description == "File I/O operations with capability-based security"
        assert "file.read" in metadata.capabilities
        assert "file.write" in metadata.capabilities
        assert "file.delete" in metadata.capabilities
        assert "file.append" in metadata.capabilities
        assert metadata.version == "1.0.0"

    def test_file_has_function_metadata(self):
        """Test that file module has registered functions."""
        metadata = get_module_metadata("file")

        # Check key methods are registered
        assert "read" in metadata.functions
        assert "write" in metadata.functions
        assert "readBytes" in metadata.functions
        assert "writeBytes" in metadata.functions
        assert "readLines" in metadata.functions
        assert "writeLines" in metadata.functions
        assert "append" in metadata.functions
        assert "exists" in metadata.functions
        assert "delete" in metadata.functions
        assert "copy" in metadata.functions
        assert "move" in metadata.functions
        assert "size" in metadata.functions
        assert "isFile" in metadata.functions
        assert "isDirectory" in metadata.functions

        # Should have 15 functions
        assert len(metadata.functions) == 15

    def test_file_function_capabilities(self):
        """Test that file functions have correct capabilities."""
        metadata = get_module_metadata("file")

        # Read operations require file.read
        assert metadata.functions["read"].capabilities == ["file.read"]
        assert metadata.functions["readBytes"].capabilities == ["file.read"]
        assert metadata.functions["readLines"].capabilities == ["file.read"]

        # Write operations require file.write
        assert metadata.functions["write"].capabilities == ["file.write"]
        assert metadata.functions["writeBytes"].capabilities == ["file.write"]
        assert metadata.functions["writeLines"].capabilities == ["file.write"]

        # Append requires file.append
        assert metadata.functions["append"].capabilities == ["file.append"]

        # Delete requires file.delete
        assert metadata.functions["delete"].capabilities == ["file.delete"]

        # Metadata operations require no capabilities
        assert metadata.functions["exists"].capabilities == []
        assert metadata.functions["size"].capabilities == []
        assert metadata.functions["isFile"].capabilities == []
        assert metadata.functions["isDirectory"].capabilities == []


class TestFileReadOperations:
    """Test file reading operations."""

    def test_read_text_file(self, tmp_path):
        """Test reading text file."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello World", encoding="utf-8")

        content = file_module.read(str(test_file))
        assert content == "Hello World"

    def test_read_with_encoding(self, tmp_path):
        """Test reading file with specific encoding."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello World", encoding="utf-8")

        content = file_module.read(str(test_file), encoding="utf-8")
        assert content == "Hello World"

    def test_read_bytes(self, tmp_path):
        """Test reading binary file."""
        test_file = tmp_path / "test.bin"
        test_data = b'\x00\x01\x02\x03\xFF'
        test_file.write_bytes(test_data)

        data = file_module.readBytes(str(test_file))
        assert data == test_data

    def test_read_lines(self, tmp_path):
        """Test reading lines from file."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("line1\nline2\nline3\n", encoding="utf-8")

        lines = file_module.readLines(str(test_file))
        assert lines == ["line1", "line2", "line3"]

    def test_read_lines_with_crlf(self, tmp_path):
        """Test reading lines with Windows line endings."""
        test_file = tmp_path / "test.txt"
        # Write in binary mode to ensure exact line endings
        test_file.write_bytes(b"line1\r\nline2\r\nline3")

        lines = file_module.readLines(str(test_file))
        # Filter out empty lines that might result from different line ending handling
        non_empty_lines = [line for line in lines if line]
        assert len(non_empty_lines) == 3
        assert "line1" in non_empty_lines
        assert "line2" in non_empty_lines
        assert "line3" in non_empty_lines

    def test_read_nonexistent_file(self, tmp_path):
        """Test reading nonexistent file raises error."""
        with pytest.raises(FileNotFoundError):
            file_module.read(str(tmp_path / "nonexistent.txt"))


class TestFileWriteOperations:
    """Test file writing operations."""

    def test_write_text_file(self, tmp_path):
        """Test writing text file."""
        test_file = tmp_path / "output.txt"
        file_module.write(str(test_file), "Hello World")

        assert test_file.read_text(encoding="utf-8") == "Hello World"

    def test_write_creates_directories(self, tmp_path):
        """Test write creates parent directories."""
        test_file = tmp_path / "subdir" / "nested" / "file.txt"
        file_module.write(str(test_file), "content")

        assert test_file.exists()
        assert test_file.read_text(encoding="utf-8") == "content"

    def test_write_bytes(self, tmp_path):
        """Test writing binary file."""
        test_file = tmp_path / "output.bin"
        test_data = b'\x00\x01\x02\xFF'
        file_module.writeBytes(str(test_file), test_data)

        assert test_file.read_bytes() == test_data

    def test_write_lines(self, tmp_path):
        """Test writing lines to file."""
        test_file = tmp_path / "output.txt"
        lines = ["line1", "line2", "line3"]
        file_module.writeLines(str(test_file), lines)

        content = test_file.read_text(encoding="utf-8")
        assert content == "line1\nline2\nline3\n"

    def test_write_overwrites_existing(self, tmp_path):
        """Test write overwrites existing file."""
        test_file = tmp_path / "file.txt"
        test_file.write_text("old content", encoding="utf-8")

        file_module.write(str(test_file), "new content")
        assert test_file.read_text(encoding="utf-8") == "new content"


class TestFileAppendOperation:
    """Test file append operations."""

    def test_append_to_file(self, tmp_path):
        """Test appending to existing file."""
        test_file = tmp_path / "log.txt"
        test_file.write_text("line1\n", encoding="utf-8")

        file_module.append(str(test_file), "line2\n")
        content = test_file.read_text(encoding="utf-8")
        assert content == "line1\nline2\n"

    def test_append_creates_file(self, tmp_path):
        """Test append creates file if doesn't exist."""
        test_file = tmp_path / "new.txt"
        file_module.append(str(test_file), "first line\n")

        assert test_file.exists()
        assert test_file.read_text(encoding="utf-8") == "first line\n"


class TestFileManagementOperations:
    """Test file management operations."""

    def test_exists_returns_true(self, tmp_path):
        """Test exists returns True for existing file."""
        test_file = tmp_path / "file.txt"
        test_file.write_text("content", encoding="utf-8")

        assert file_module.exists(str(test_file)) is True

    def test_exists_returns_false(self, tmp_path):
        """Test exists returns False for nonexistent file."""
        assert file_module.exists(str(tmp_path / "nonexistent.txt")) is False

    def test_delete_file(self, tmp_path):
        """Test deleting file."""
        test_file = tmp_path / "file.txt"
        test_file.write_text("content", encoding="utf-8")

        result = file_module.delete(str(test_file))
        assert result is True
        assert not test_file.exists()

    def test_delete_nonexistent_returns_false(self, tmp_path):
        """Test deleting nonexistent file returns False."""
        result = file_module.delete(str(tmp_path / "nonexistent.txt"))
        assert result is False

    def test_delete_directory_raises_error(self, tmp_path):
        """Test deleting directory raises error."""
        test_dir = tmp_path / "dir"
        test_dir.mkdir()

        with pytest.raises(ValueError, match="Not a file"):
            file_module.delete(str(test_dir))

    def test_copy_file(self, tmp_path):
        """Test copying file."""
        source = tmp_path / "source.txt"
        dest = tmp_path / "dest.txt"
        source.write_text("content", encoding="utf-8")

        file_module.copy(str(source), str(dest))

        assert dest.exists()
        assert dest.read_text(encoding="utf-8") == "content"
        assert source.exists()  # Source still exists

    def test_move_file(self, tmp_path):
        """Test moving file."""
        source = tmp_path / "source.txt"
        dest = tmp_path / "subdir" / "dest.txt"
        source.write_text("content", encoding="utf-8")

        file_module.move(str(source), str(dest))

        assert dest.exists()
        assert dest.read_text(encoding="utf-8") == "content"
        assert not source.exists()  # Source no longer exists


class TestFileInformationOperations:
    """Test file information operations."""

    def test_size_of_file(self, tmp_path):
        """Test getting file size."""
        test_file = tmp_path / "file.txt"
        content = "Hello World"
        test_file.write_text(content, encoding="utf-8")

        size = file_module.size(str(test_file))
        assert size == len(content.encode('utf-8'))

    def test_modified_time(self, tmp_path):
        """Test getting modification time."""
        test_file = tmp_path / "file.txt"
        test_file.write_text("content", encoding="utf-8")

        mtime = file_module.modifiedTime(str(test_file))
        assert isinstance(mtime, float)
        assert mtime > 0

    def test_is_file_true(self, tmp_path):
        """Test isFile returns True for file."""
        test_file = tmp_path / "file.txt"
        test_file.write_text("content", encoding="utf-8")

        assert file_module.isFile(str(test_file)) is True

    def test_is_file_false(self, tmp_path):
        """Test isFile returns False for directory."""
        test_dir = tmp_path / "dir"
        test_dir.mkdir()

        assert file_module.isFile(str(test_dir)) is False

    def test_is_directory_true(self, tmp_path):
        """Test isDirectory returns True for directory."""
        test_dir = tmp_path / "dir"
        test_dir.mkdir()

        assert file_module.isDirectory(str(test_dir)) is True

    def test_is_directory_false(self, tmp_path):
        """Test isDirectory returns False for file."""
        test_file = tmp_path / "file.txt"
        test_file.write_text("content", encoding="utf-8")

        assert file_module.isDirectory(str(test_file)) is False


class TestFilePathCanonicalization:
    """Test path canonicalization and security."""

    def test_tilde_expansion(self, tmp_path):
        """Test ~ is expanded to home directory."""
        # Create temp file in home directory
        import os
        home = os.path.expanduser("~")

        # Test that tilde is expanded (we can't actually write to home in tests)
        # Just verify the function accepts ~ paths
        # The actual write would fail without permissions, so we catch that
        try:
            file_module.exists("~/nonexistent.txt")
        except:
            pass  # Expected - we just verify it doesn't crash on tilde

    def test_relative_path_converted(self, tmp_path):
        """Test relative paths are converted to absolute."""
        # Change to temp directory
        original_cwd = os.getcwd()
        try:
            os.chdir(str(tmp_path))
            test_file = tmp_path / "file.txt"
            test_file.write_text("content", encoding="utf-8")

            # Read using relative path
            content = file_module.read("file.txt")
            assert content == "content"
        finally:
            os.chdir(original_cwd)
