"""Tests for safe file operations with capability-based access control."""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, mock_open, MagicMock

from mlpy.runtime.system_modules.file_safe import SafeFile
from mlpy.runtime.capabilities.exceptions import CapabilityNotFoundError


class TestFileAccessValidation:
    """Test file access validation."""

    @patch('mlpy.runtime.system_modules.file_safe.has_capability')
    def test_validate_file_access_with_valid_capability(self, mock_has_cap):
        """Test validation succeeds with valid capability."""
        mock_has_cap.return_value = True

        result = SafeFile._validate_file_access("/tmp/test.txt", "read")

        assert result == "/tmp/test.txt"
        mock_has_cap.assert_called_once_with("file", "/tmp/test.txt", "read")

    @patch('mlpy.runtime.system_modules.file_safe.has_capability')
    def test_validate_file_access_without_capability(self, mock_has_cap):
        """Test validation fails without capability."""
        mock_has_cap.return_value = False

        with pytest.raises(CapabilityNotFoundError) as exc_info:
            SafeFile._validate_file_access("/tmp/test.txt", "read")

        assert "file" in str(exc_info.value)
        assert "/tmp/test.txt" in str(exc_info.value)

    @patch('mlpy.runtime.system_modules.file_safe.has_capability')
    def test_validate_file_access_with_pathlib(self, mock_has_cap):
        """Test validation works with pathlib.Path objects."""
        mock_has_cap.return_value = True

        result = SafeFile._validate_file_access(Path("/tmp/test.txt"), "write")

        # Windows converts forward slashes to backslashes
        expected = str(Path("/tmp/test.txt"))
        assert result == expected
        mock_has_cap.assert_called_once_with("file", expected, "write")


class TestSafeFileOpen:
    """Test SafeFile.open() context manager."""

    @patch('mlpy.runtime.system_modules.file_safe.use_capability')
    @patch('mlpy.runtime.system_modules.file_safe.has_capability')
    def test_open_read_mode(self, mock_has_cap, mock_use_cap):
        """Test opening file in read mode."""
        mock_has_cap.return_value = True

        # Mock builtins.open within the function scope
        mock_file = mock_open(read_data="test content")
        with patch('builtins.open', mock_file):
            with SafeFile.open("/tmp/test.txt", "r") as f:
                content = f.read()

            assert content == "test content"
            mock_has_cap.assert_called_once_with("file", "/tmp/test.txt", "read")
            mock_use_cap.assert_called_once_with("file", "/tmp/test.txt", "read")

    @patch('mlpy.runtime.system_modules.file_safe.use_capability')
    @patch('mlpy.runtime.system_modules.file_safe.has_capability')
    def test_open_write_mode(self, mock_has_cap, mock_use_cap):
        """Test opening file in write mode."""
        mock_has_cap.return_value = True

        mock_file = mock_open()
        with patch('builtins.open', mock_file):
            with SafeFile.open("/tmp/test.txt", "w") as f:
                f.write("new content")

            mock_has_cap.assert_called_once_with("file", "/tmp/test.txt", "write")
            mock_use_cap.assert_called_once_with("file", "/tmp/test.txt", "write")

    @patch('mlpy.runtime.system_modules.file_safe.use_capability')
    @patch('mlpy.runtime.system_modules.file_safe.has_capability')
    def test_open_append_mode(self, mock_has_cap, mock_use_cap):
        """Test opening file in append mode."""
        mock_has_cap.return_value = True

        mock_file = mock_open()
        with patch('builtins.open', mock_file):
            with SafeFile.open("/tmp/test.txt", "a") as f:
                f.write("appended content")

            mock_has_cap.assert_called_once_with("file", "/tmp/test.txt", "write")
            mock_use_cap.assert_called_once_with("file", "/tmp/test.txt", "write")

    @patch('mlpy.runtime.system_modules.file_safe.has_capability')
    def test_open_without_capability(self, mock_has_cap):
        """Test open fails without capability."""
        mock_has_cap.return_value = False

        with pytest.raises(CapabilityNotFoundError):
            with SafeFile.open("/tmp/test.txt", "r"):
                pass

    @patch('mlpy.runtime.system_modules.file_safe.use_capability')
    @patch('mlpy.runtime.system_modules.file_safe.has_capability')
    def test_open_with_custom_encoding(self, mock_has_cap, mock_use_cap):
        """Test open with custom encoding."""
        mock_has_cap.return_value = True

        mock_file = mock_open()
        with patch('builtins.open', mock_file):
            with SafeFile.open("/tmp/test.txt", "r", encoding="latin-1"):
                pass

            # Verify open was called with correct encoding
            mock_file.assert_called_once()
            call_kwargs = mock_file.call_args[1]
            assert call_kwargs['encoding'] == "latin-1"


class TestReadText:
    """Test SafeFile.read_text()."""

    @patch('mlpy.runtime.capabilities.context.get_current_context')
    @patch('mlpy.runtime.system_modules.file_safe.use_capability')
    @patch('mlpy.runtime.system_modules.file_safe.has_capability')
    @patch('builtins.open', new_callable=mock_open, read_data="Hello World")
    def test_read_text_success(self, mock_file, mock_has_cap, mock_use_cap, mock_get_ctx):
        """Test reading text file."""
        mock_has_cap.return_value = True
        # Mock capability context for decorator
        mock_ctx = Mock()
        mock_ctx.has_capability.return_value = True
        mock_get_ctx.return_value = mock_ctx

        content = SafeFile.read_text("/tmp/test.txt")

        assert content == "Hello World"
        mock_has_cap.assert_called_once_with("file", "/tmp/test.txt", "read")
        mock_use_cap.assert_called_once_with("file", "/tmp/test.txt", "read")

    @patch('mlpy.runtime.system_modules.file_safe.has_capability')
    def test_read_text_without_capability(self, mock_has_cap):
        """Test read_text fails without capability."""
        mock_has_cap.return_value = False

        with pytest.raises(CapabilityNotFoundError):
            SafeFile.read_text("/tmp/test.txt")

    @patch('mlpy.runtime.capabilities.context.get_current_context')
    @patch('mlpy.runtime.system_modules.file_safe.use_capability')
    @patch('mlpy.runtime.system_modules.file_safe.has_capability')
    @patch('builtins.open', new_callable=mock_open, read_data="UTF-8 text")
    def test_read_text_with_custom_encoding(self, mock_file, mock_has_cap, mock_use_cap, mock_get_ctx):
        """Test read_text with custom encoding."""
        mock_has_cap.return_value = True
        mock_ctx = Mock()
        mock_ctx.has_capability.return_value = True
        mock_get_ctx.return_value = mock_ctx

        SafeFile.read_text("/tmp/test.txt", encoding="latin-1")

        call_kwargs = mock_file.call_args[1]
        assert call_kwargs['encoding'] == "latin-1"


class TestWriteText:
    """Test SafeFile.write_text()."""

    @patch('mlpy.runtime.capabilities.context.get_current_context')
    @patch('mlpy.runtime.system_modules.file_safe.use_capability')
    @patch('mlpy.runtime.system_modules.file_safe.has_capability')
    @patch('builtins.open', new_callable=mock_open)
    def test_write_text_success(self, mock_file, mock_has_cap, mock_use_cap, mock_get_ctx):
        """Test writing text file."""
        mock_has_cap.return_value = True
        mock_ctx = Mock()
        mock_ctx.has_capability.return_value = True
        mock_get_ctx.return_value = mock_ctx

        SafeFile.write_text("/tmp/test.txt", "Hello World")

        mock_has_cap.assert_called_once_with("file", "/tmp/test.txt", "write")
        mock_use_cap.assert_called_once_with("file", "/tmp/test.txt", "write")
        mock_file().write.assert_called_once_with("Hello World")

    @patch('mlpy.runtime.system_modules.file_safe.has_capability')
    def test_write_text_without_capability(self, mock_has_cap):
        """Test write_text fails without capability."""
        mock_has_cap.return_value = False

        with pytest.raises(CapabilityNotFoundError):
            SafeFile.write_text("/tmp/test.txt", "content")


class TestReadBytes:
    """Test SafeFile.read_bytes()."""

    @patch('mlpy.runtime.capabilities.context.get_current_context')
    @patch('mlpy.runtime.system_modules.file_safe.use_capability')
    @patch('mlpy.runtime.system_modules.file_safe.has_capability')
    @patch('builtins.open', new_callable=mock_open, read_data=b"binary data")
    def test_read_bytes_success(self, mock_file, mock_has_cap, mock_use_cap, mock_get_ctx):
        """Test reading binary file."""
        mock_has_cap.return_value = True
        mock_ctx = Mock()
        mock_ctx.has_capability.return_value = True
        mock_get_ctx.return_value = mock_ctx

        content = SafeFile.read_bytes("/tmp/test.bin")

        assert content == b"binary data"
        mock_has_cap.assert_called_once_with("file", "/tmp/test.bin", "read")
        mock_use_cap.assert_called_once_with("file", "/tmp/test.bin", "read")

    @patch('mlpy.runtime.system_modules.file_safe.has_capability')
    def test_read_bytes_without_capability(self, mock_has_cap):
        """Test read_bytes fails without capability."""
        mock_has_cap.return_value = False

        with pytest.raises(CapabilityNotFoundError):
            SafeFile.read_bytes("/tmp/test.bin")


class TestWriteBytes:
    """Test SafeFile.write_bytes()."""

    @patch('mlpy.runtime.capabilities.context.get_current_context')
    @patch('mlpy.runtime.system_modules.file_safe.use_capability')
    @patch('mlpy.runtime.system_modules.file_safe.has_capability')
    @patch('builtins.open', new_callable=mock_open)
    def test_write_bytes_success(self, mock_file, mock_has_cap, mock_use_cap, mock_get_ctx):
        """Test writing binary file."""
        mock_has_cap.return_value = True
        mock_ctx = Mock()
        mock_ctx.has_capability.return_value = True
        mock_get_ctx.return_value = mock_ctx

        SafeFile.write_bytes("/tmp/test.bin", b"binary data")

        mock_has_cap.assert_called_once_with("file", "/tmp/test.bin", "write")
        mock_use_cap.assert_called_once_with("file", "/tmp/test.bin", "write")
        mock_file().write.assert_called_once_with(b"binary data")

    @patch('mlpy.runtime.system_modules.file_safe.has_capability')
    def test_write_bytes_without_capability(self, mock_has_cap):
        """Test write_bytes fails without capability."""
        mock_has_cap.return_value = False

        with pytest.raises(CapabilityNotFoundError):
            SafeFile.write_bytes("/tmp/test.bin", b"data")


class TestFileSystemOperations:
    """Test file system query operations."""

    @patch('mlpy.runtime.capabilities.context.get_current_context')
    @patch('mlpy.runtime.system_modules.file_safe.use_capability')
    @patch('mlpy.runtime.system_modules.file_safe.has_capability')
    @patch('os.path.exists')
    def test_exists(self, mock_exists, mock_has_cap, mock_use_cap, mock_get_ctx):
        """Test checking if file exists."""
        mock_has_cap.return_value = True
        mock_exists.return_value = True
        mock_ctx = Mock()
        mock_ctx.has_capability.return_value = True
        mock_get_ctx.return_value = mock_ctx

        result = SafeFile.exists("/tmp/test.txt")

        assert result is True
        mock_has_cap.assert_called_once_with("file", "/tmp/test.txt", "read")

    @patch('mlpy.runtime.capabilities.context.get_current_context')
    @patch('mlpy.runtime.system_modules.file_safe.use_capability')
    @patch('mlpy.runtime.system_modules.file_safe.has_capability')
    @patch('os.path.isfile')
    def test_is_file(self, mock_isfile, mock_has_cap, mock_use_cap, mock_get_ctx):
        """Test checking if path is a file."""
        mock_has_cap.return_value = True
        mock_isfile.return_value = True
        mock_ctx = Mock()
        mock_ctx.has_capability.return_value = True
        mock_get_ctx.return_value = mock_ctx

        result = SafeFile.is_file("/tmp/test.txt")

        assert result is True
        mock_has_cap.assert_called_once_with("file", "/tmp/test.txt", "read")

    @patch('mlpy.runtime.capabilities.context.get_current_context')
    @patch('mlpy.runtime.system_modules.file_safe.use_capability')
    @patch('mlpy.runtime.system_modules.file_safe.has_capability')
    @patch('os.path.isdir')
    def test_is_directory(self, mock_isdir, mock_has_cap, mock_use_cap, mock_get_ctx):
        """Test checking if path is a directory."""
        mock_has_cap.return_value = True
        mock_isdir.return_value = True
        mock_ctx = Mock()
        mock_ctx.has_capability.return_value = True
        mock_get_ctx.return_value = mock_ctx

        result = SafeFile.is_directory("/tmp/")

        assert result is True
        mock_has_cap.assert_called_once_with("file", "/tmp/", "read")

    @patch('mlpy.runtime.capabilities.context.get_current_context')
    @patch('mlpy.runtime.system_modules.file_safe.use_capability')
    @patch('mlpy.runtime.system_modules.file_safe.has_capability')
    @patch('os.path.getsize')
    def test_get_size(self, mock_getsize, mock_has_cap, mock_use_cap, mock_get_ctx):
        """Test getting file size."""
        mock_has_cap.return_value = True
        mock_getsize.return_value = 1024
        mock_ctx = Mock()
        mock_ctx.has_capability.return_value = True
        mock_get_ctx.return_value = mock_ctx

        result = SafeFile.get_size("/tmp/test.txt")

        assert result == 1024
        mock_has_cap.assert_called_once_with("file", "/tmp/test.txt", "read")


class TestDirectoryOperations:
    """Test directory operations."""

    @patch('mlpy.runtime.capabilities.context.get_current_context')
    @patch('mlpy.runtime.system_modules.file_safe.use_capability')
    @patch('mlpy.runtime.system_modules.file_safe.has_capability')
    @patch('os.listdir')
    def test_list_directory(self, mock_listdir, mock_has_cap, mock_use_cap, mock_get_ctx):
        """Test listing directory contents."""
        mock_has_cap.return_value = True
        mock_listdir.return_value = ["file1.txt", "file2.txt"]
        mock_ctx = Mock()
        mock_ctx.has_capability.return_value = True
        mock_get_ctx.return_value = mock_ctx

        result = SafeFile.list_directory("/tmp/")

        assert result == ["file1.txt", "file2.txt"]
        mock_has_cap.assert_called_once_with("file", "/tmp/", "read")

    @patch('mlpy.runtime.capabilities.context.get_current_context')
    @patch('mlpy.runtime.system_modules.file_safe.use_capability')
    @patch('mlpy.runtime.system_modules.file_safe.has_capability')
    @patch('os.mkdir')
    def test_create_directory_simple(self, mock_mkdir, mock_has_cap, mock_use_cap, mock_get_ctx):
        """Test creating directory without parents."""
        mock_has_cap.return_value = True
        mock_ctx = Mock()
        mock_ctx.has_capability.return_value = True
        mock_get_ctx.return_value = mock_ctx

        SafeFile.create_directory("/tmp/newdir", parents=False)

        mock_has_cap.assert_called_once_with("file", "/tmp/newdir", "write")
        mock_mkdir.assert_called_once_with("/tmp/newdir")

    @patch('mlpy.runtime.capabilities.context.get_current_context')
    @patch('mlpy.runtime.system_modules.file_safe.use_capability')
    @patch('mlpy.runtime.system_modules.file_safe.has_capability')
    @patch('os.makedirs')
    def test_create_directory_with_parents(self, mock_makedirs, mock_has_cap, mock_use_cap, mock_get_ctx):
        """Test creating directory with parents."""
        mock_has_cap.return_value = True
        mock_ctx = Mock()
        mock_ctx.has_capability.return_value = True
        mock_get_ctx.return_value = mock_ctx

        SafeFile.create_directory("/tmp/path/to/newdir", parents=True)

        mock_has_cap.assert_called_once_with("file", "/tmp/path/to/newdir", "write")
        mock_makedirs.assert_called_once_with("/tmp/path/to/newdir", exist_ok=True)


class TestFileModificationOperations:
    """Test file modification operations."""

    @patch('mlpy.runtime.capabilities.context.get_current_context')
    @patch('mlpy.runtime.system_modules.file_safe.use_capability')
    @patch('mlpy.runtime.system_modules.file_safe.has_capability')
    @patch('os.remove')
    def test_remove_file(self, mock_remove, mock_has_cap, mock_use_cap, mock_get_ctx):
        """Test removing file."""
        mock_has_cap.return_value = True
        mock_ctx = Mock()
        mock_ctx.has_capability.return_value = True
        mock_get_ctx.return_value = mock_ctx

        SafeFile.remove_file("/tmp/test.txt")

        mock_has_cap.assert_called_once_with("file", "/tmp/test.txt", "write")
        mock_remove.assert_called_once_with("/tmp/test.txt")

    @patch('mlpy.runtime.capabilities.context.get_current_context')
    @patch('mlpy.runtime.system_modules.file_safe.use_capability')
    @patch('mlpy.runtime.system_modules.file_safe.has_capability')
    @patch('shutil.copy2')
    def test_copy_file(self, mock_copy, mock_has_cap, mock_use_cap, mock_get_ctx):
        """Test copying file."""
        mock_has_cap.return_value = True
        mock_ctx = Mock()
        mock_ctx.has_capability.return_value = True
        mock_get_ctx.return_value = mock_ctx

        SafeFile.copy_file("/tmp/source.txt", "/tmp/dest.txt")

        # Should check both source (read) and destination (write)
        assert mock_has_cap.call_count == 2
        mock_has_cap.assert_any_call("file", "/tmp/source.txt", "read")
        mock_has_cap.assert_any_call("file", "/tmp/dest.txt", "write")

        assert mock_use_cap.call_count == 2
        mock_use_cap.assert_any_call("file", "/tmp/source.txt", "read")
        mock_use_cap.assert_any_call("file", "/tmp/dest.txt", "write")

        mock_copy.assert_called_once_with("/tmp/source.txt", "/tmp/dest.txt")

    @patch('mlpy.runtime.capabilities.context.get_current_context')
    @patch('mlpy.runtime.system_modules.file_safe.use_capability')
    @patch('mlpy.runtime.system_modules.file_safe.has_capability')
    @patch('shutil.move')
    def test_move_file(self, mock_move, mock_has_cap, mock_use_cap, mock_get_ctx):
        """Test moving file."""
        mock_has_cap.return_value = True
        mock_ctx = Mock()
        mock_ctx.has_capability.return_value = True
        mock_get_ctx.return_value = mock_ctx

        SafeFile.move_file("/tmp/source.txt", "/tmp/dest.txt")

        # Should check both source and destination (write for both)
        assert mock_has_cap.call_count == 2
        mock_has_cap.assert_any_call("file", "/tmp/source.txt", "write")
        mock_has_cap.assert_any_call("file", "/tmp/dest.txt", "write")

        mock_move.assert_called_once_with("/tmp/source.txt", "/tmp/dest.txt")

    @patch('mlpy.runtime.system_modules.file_safe.has_capability')
    def test_copy_file_missing_source_capability(self, mock_has_cap):
        """Test copy fails without source read capability."""
        # First call (source read) fails, second wouldn't be reached
        mock_has_cap.side_effect = [False, True]

        with pytest.raises(CapabilityNotFoundError):
            SafeFile.copy_file("/tmp/source.txt", "/tmp/dest.txt")

    @patch('mlpy.runtime.system_modules.file_safe.has_capability')
    def test_copy_file_missing_dest_capability(self, mock_has_cap):
        """Test copy fails without destination write capability."""
        # First call (source read) succeeds, second (dest write) fails
        mock_has_cap.side_effect = [True, False]

        with pytest.raises(CapabilityNotFoundError):
            SafeFile.copy_file("/tmp/source.txt", "/tmp/dest.txt")


class TestModuleExports:
    """Test module-level exports and convenience functions."""

    def test_global_instance_exists(self):
        """Test global file_safe instance exists."""
        from mlpy.runtime.system_modules.file_safe import file_safe

        assert file_safe is not None
        # Just check it exists, not the type (decorator may wrap it)

    def test_convenience_functions_exported(self):
        """Test convenience functions are exported."""
        from mlpy.runtime.system_modules import file_safe

        # Verify all key functions are exported
        assert hasattr(file_safe, 'open')
        assert hasattr(file_safe, 'read_text')
        assert hasattr(file_safe, 'write_text')
        assert hasattr(file_safe, 'read_bytes')
        assert hasattr(file_safe, 'write_bytes')
        assert hasattr(file_safe, 'exists')
        assert hasattr(file_safe, 'is_file')
        assert hasattr(file_safe, 'is_directory')
        assert hasattr(file_safe, 'list_directory')
        assert hasattr(file_safe, 'create_directory')
        assert hasattr(file_safe, 'remove_file')
        assert hasattr(file_safe, 'copy_file')
        assert hasattr(file_safe, 'move_file')
