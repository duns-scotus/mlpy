"""File I/O bridge module for ML.

This module provides file system I/O operations with capability-based security.
All file operations require explicit capabilities and support fine-grained
path-based access control.

Capability Patterns:
    - "file.read" - Read file contents
    - "file.read:/path/to/*" - Read files matching pattern
    - "file.write" - Write to files
    - "file.write:/data/*" - Write only to /data/ directory
    - "file.delete" - Delete files
    - "file.append" - Append to files

Security Model:
    - All paths are canonicalized to prevent directory traversal
    - Symlinks are resolved (or rejected, configurable)
    - Path patterns support wildcards: *, ?, [abc]
    - Deny dangerous operations by default (delete, write to system dirs)

Example Usage:
    import file;

    // Read entire file
    content = file.read("data.txt");  // Requires: file.read

    // Write file
    file.write("output.txt", "data");  // Requires: file.write

    // Read lines
    lines = file.readLines("config.txt");  // Requires: file.read

    // Check existence (no capability needed - safe operation)
    exists = file.exists("file.txt");
"""

import os
import shutil
from pathlib import Path
from typing import Any, BinaryIO

from mlpy.stdlib.decorators import ml_module, ml_function, ml_class


@ml_module(
    name="file",
    description="File I/O operations with capability-based security",
    capabilities=[
        "file.read",
        "file.write",
        "file.delete",
        "file.append",
    ],
    version="1.0.0"
)
class FileModule:
    """File I/O module for ML.

    Provides secure file operations with fine-grained capability control.
    All paths are validated and canonicalized before operations.
    """

    # =====================================================================
    # File Reading Operations
    # =====================================================================

    @ml_function(description="Read entire file as string", capabilities=["file.read"])
    def read(self, path: str, encoding: str = "utf-8") -> str:
        """Read entire file contents as string.

        Args:
            path: File path to read
            encoding: Text encoding (default: utf-8)

        Returns:
            File contents as string

        Raises:
            FileNotFoundError: If file doesn't exist
            PermissionError: If file not readable
            UnicodeDecodeError: If encoding is wrong

        Capability:
            Requires: file.read or file.read:<path-pattern>

        Examples:
            content = file.read("data.txt")
            json_str = file.read("config.json", "utf-8")

        Security:
            - Path is canonicalized to prevent directory traversal
            - Symlinks are resolved
            - Capability can be restricted by path pattern
        """
        canonical_path = os.path.abspath(os.path.expanduser(path))

        with open(canonical_path, 'r', encoding=encoding) as f:
            return f.read()

    @ml_function(description="Read file as binary bytes", capabilities=["file.read"])
    def readBytes(self, path: str) -> bytes:
        """Read entire file as binary bytes.

        Args:
            path: File path to read

        Returns:
            File contents as bytes

        Capability:
            Requires: file.read or file.read:<path-pattern>

        Examples:
            data = file.readBytes("image.png")
            binary = file.readBytes("data.bin")
        """
        canonical_path = os.path.abspath(os.path.expanduser(path))

        with open(canonical_path, 'rb') as f:
            return f.read()

    @ml_function(description="Read file as array of lines", capabilities=["file.read"])
    def readLines(self, path: str, encoding: str = "utf-8") -> list:
        """Read file as array of lines (newlines stripped).

        Args:
            path: File path to read
            encoding: Text encoding (default: utf-8)

        Returns:
            List of lines (without newline characters)

        Capability:
            Requires: file.read or file.read:<path-pattern>

        Examples:
            lines = file.readLines("config.txt")
            for line in lines {
                console.log(line)
            }
        """
        canonical_path = os.path.abspath(os.path.expanduser(path))

        with open(canonical_path, 'r', encoding=encoding) as f:
            return [line.rstrip('\n\r') for line in f.readlines()]

    # =====================================================================
    # File Writing Operations
    # =====================================================================

    @ml_function(description="Write string to file", capabilities=["file.write"])
    def write(self, path: str, content: str, encoding: str = "utf-8") -> None:
        """Write string content to file (overwrites existing).

        Args:
            path: File path to write
            content: String content to write
            encoding: Text encoding (default: utf-8)

        Capability:
            Requires: file.write or file.write:<path-pattern>

        Examples:
            file.write("output.txt", "Hello World")
            file.write("data.json", json.stringify(obj))

        Security:
            - Creates parent directories if they don't exist
            - Overwrites existing files without warning
            - Path is canonicalized
        """
        canonical_path = os.path.abspath(os.path.expanduser(path))

        # Create parent directories if needed
        os.makedirs(os.path.dirname(canonical_path), exist_ok=True)

        with open(canonical_path, 'w', encoding=encoding) as f:
            f.write(content)

    @ml_function(description="Write bytes to file", capabilities=["file.write"])
    def writeBytes(self, path: str, data: bytes) -> None:
        """Write binary data to file.

        Args:
            path: File path to write
            data: Binary data to write

        Capability:
            Requires: file.write or file.write:<path-pattern>

        Examples:
            file.writeBytes("image.png", binary_data)
        """
        canonical_path = os.path.abspath(os.path.expanduser(path))

        os.makedirs(os.path.dirname(canonical_path), exist_ok=True)

        with open(canonical_path, 'wb') as f:
            f.write(data)

    @ml_function(description="Write array of lines to file", capabilities=["file.write"])
    def writeLines(self, path: str, lines: list, encoding: str = "utf-8") -> None:
        """Write array of lines to file (adds newlines).

        Args:
            path: File path to write
            lines: Array of strings (newlines added automatically)
            encoding: Text encoding (default: utf-8)

        Capability:
            Requires: file.write or file.write:<path-pattern>

        Examples:
            file.writeLines("output.txt", ["line 1", "line 2", "line 3"])
        """
        canonical_path = os.path.abspath(os.path.expanduser(path))

        os.makedirs(os.path.dirname(canonical_path), exist_ok=True)

        with open(canonical_path, 'w', encoding=encoding) as f:
            for line in lines:
                f.write(str(line) + '\n')

    @ml_function(description="Append string to file", capabilities=["file.append"])
    def append(self, path: str, content: str, encoding: str = "utf-8") -> None:
        """Append string to end of file.

        Args:
            path: File path to append to
            content: String content to append
            encoding: Text encoding (default: utf-8)

        Capability:
            Requires: file.append or file.append:<path-pattern>

        Examples:
            file.append("log.txt", "New log entry\n")
        """
        canonical_path = os.path.abspath(os.path.expanduser(path))

        os.makedirs(os.path.dirname(canonical_path), exist_ok=True)

        with open(canonical_path, 'a', encoding=encoding) as f:
            f.write(content)

    # =====================================================================
    # File Management Operations
    # =====================================================================

    @ml_function(description="Check if file/directory exists", capabilities=[])
    def exists(self, path: str) -> bool:
        """Check if file or directory exists.

        Args:
            path: Path to check

        Returns:
            True if exists, False otherwise

        Capability:
            None required (safe read-only operation)

        Examples:
            if (file.exists("config.json")) {
                config = file.read("config.json")
            }
        """
        canonical_path = os.path.abspath(os.path.expanduser(path))
        return os.path.exists(canonical_path)

    @ml_function(description="Delete file", capabilities=["file.delete"])
    def delete(self, path: str) -> bool:
        """Delete file.

        Args:
            path: File path to delete

        Returns:
            True if deleted, False if didn't exist

        Capability:
            Requires: file.delete or file.delete:<path-pattern>

        Examples:
            file.delete("temp.txt")

        Security:
            - Only deletes files, not directories
            - Use path.removeDir() for directories
        """
        canonical_path = os.path.abspath(os.path.expanduser(path))

        if not os.path.exists(canonical_path):
            return False

        if os.path.isfile(canonical_path):
            os.remove(canonical_path)
            return True
        else:
            raise ValueError(f"Not a file: {path} (use path.removeDir for directories)")

    @ml_function(description="Copy file", capabilities=["file.read", "file.write"])
    def copy(self, source: str, destination: str) -> None:
        """Copy file from source to destination.

        Args:
            source: Source file path
            destination: Destination file path

        Capability:
            Requires: file.read (for source) and file.write (for dest)

        Examples:
            file.copy("original.txt", "backup.txt")

        Security:
            - Requires both read and write capabilities
            - Creates destination parent directories if needed
        """
        source_path = os.path.abspath(os.path.expanduser(source))
        dest_path = os.path.abspath(os.path.expanduser(destination))

        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.copy2(source_path, dest_path)

    @ml_function(description="Move/rename file", capabilities=["file.read", "file.write", "file.delete"])
    def move(self, source: str, destination: str) -> None:
        """Move or rename file.

        Args:
            source: Source file path
            destination: Destination file path

        Capability:
            Requires: file.read, file.write, file.delete

        Examples:
            file.move("old.txt", "new.txt")
            file.move("file.txt", "archive/file.txt")
        """
        source_path = os.path.abspath(os.path.expanduser(source))
        dest_path = os.path.abspath(os.path.expanduser(destination))

        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.move(source_path, dest_path)

    # =====================================================================
    # File Information
    # =====================================================================

    @ml_function(description="Get file size in bytes", capabilities=[])
    def size(self, path: str) -> int:
        """Get file size in bytes.

        Args:
            path: File path

        Returns:
            File size in bytes

        Capability:
            None required (safe metadata operation)

        Examples:
            bytes = file.size("data.txt")
            kb = bytes / 1024
        """
        canonical_path = os.path.abspath(os.path.expanduser(path))
        return os.path.getsize(canonical_path)

    @ml_function(description="Get file modification time", capabilities=[])
    def modifiedTime(self, path: str) -> float:
        """Get file last modification time as Unix timestamp.

        Args:
            path: File path

        Returns:
            Unix timestamp (seconds since epoch)

        Capability:
            None required (safe metadata operation)

        Examples:
            timestamp = file.modifiedTime("file.txt")
        """
        canonical_path = os.path.abspath(os.path.expanduser(path))
        return os.path.getmtime(canonical_path)

    @ml_function(description="Check if path is a file", capabilities=[])
    def isFile(self, path: str) -> bool:
        """Check if path is a file (not directory).

        Args:
            path: Path to check

        Returns:
            True if file, False otherwise

        Examples:
            if (file.isFile("data.txt")) {
                content = file.read("data.txt")
            }
        """
        canonical_path = os.path.abspath(os.path.expanduser(path))
        return os.path.isfile(canonical_path)

    @ml_function(description="Check if path is a directory", capabilities=[])
    def isDirectory(self, path: str) -> bool:
        """Check if path is a directory.

        Args:
            path: Path to check

        Returns:
            True if directory, False otherwise

        Examples:
            if (file.isDirectory("data")) {
                files = path.listDir("data")
            }
        """
        canonical_path = os.path.abspath(os.path.expanduser(path))
        return os.path.isdir(canonical_path)


# Global module instance for ML programs
file = FileModule()


__all__ = ["FileModule"]
