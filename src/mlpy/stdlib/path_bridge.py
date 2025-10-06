"""Path and filesystem bridge module for ML.

This module provides path manipulation and filesystem operations with
capability-based security. Separates path operations from file I/O for
better security granularity.

Capability Patterns:
    - "path.read" - List directories, check paths
    - "path.read:/data/*" - Read only /data/ directory structure
    - "path.write" - Create/remove directories
    - "path.write:/tmp/*" - Write only to /tmp/ directory

Security Model:
    - All paths are canonicalized
    - Prevents directory traversal attacks
    - Path patterns support wildcards
    - Metadata operations (join, dirname) require no capabilities

Example Usage:
    import path;

    // Path manipulation (no capabilities needed)
    full = path.join("dir", "subdir", "file.txt");
    dir = path.dirname("/path/to/file.txt");

    // Filesystem operations (capabilities required)
    files = path.listDir("/data");  // Requires: path.read
    path.createDir("/output");      // Requires: path.write
"""

import os
import glob
from pathlib import Path as PyPath
from typing import Any

from mlpy.stdlib.decorators import ml_module, ml_function


@ml_module(
    name="path",
    description="Path manipulation and filesystem operations",
    capabilities=[
        "path.read",
        "path.write",
    ],
    version="1.0.0"
)
class PathModule:
    """Path manipulation and filesystem operations.

    Provides both pure path operations (no capabilities) and filesystem
    operations (capabilities required).
    """

    # =====================================================================
    # Path Manipulation (No Capabilities Required)
    # =====================================================================

    @ml_function(description="Join path components", capabilities=[])
    def join(self, *parts: str) -> str:
        """Join path components into single path.

        Args:
            *parts: Path components to join

        Returns:
            Joined path with OS-appropriate separators

        Capability:
            None required (pure path operation)

        Examples:
            path.join("dir", "subdir", "file.txt")  // "dir/subdir/file.txt"
            path.join("/root", "data", "file")      // "/root/data/file"

        Security:
            - Does not access filesystem
            - Safe for all users
        """
        return os.path.join(*parts)

    @ml_function(description="Get directory name from path", capabilities=[])
    def dirname(self, path: str) -> str:
        """Get directory portion of path.

        Args:
            path: File path

        Returns:
            Directory path (everything before last separator)

        Examples:
            path.dirname("/path/to/file.txt")  // "/path/to"
            path.dirname("file.txt")           // ""
        """
        return os.path.dirname(path)

    @ml_function(description="Get filename from path", capabilities=[])
    def basename(self, path: str) -> str:
        """Get filename portion of path (last component).

        Args:
            path: File path

        Returns:
            Filename (everything after last separator)

        Examples:
            path.basename("/path/to/file.txt")  // "file.txt"
            path.basename("/path/to/dir/")      // "dir"
        """
        return os.path.basename(path)

    @ml_function(description="Get file extension", capabilities=[])
    def extname(self, path: str) -> str:
        """Get file extension including dot.

        Args:
            path: File path

        Returns:
            Extension including dot, or empty string

        Examples:
            path.extname("file.txt")      // ".txt"
            path.extname("archive.tar.gz") // ".gz"
            path.extname("README")        // ""
        """
        return os.path.splitext(path)[1]

    @ml_function(description="Split path into directory and filename", capabilities=[])
    def split(self, path: str) -> list:
        """Split path into directory and filename.

        Args:
            path: File path

        Returns:
            [directory, filename] array

        Examples:
            path.split("/path/to/file.txt")  // ["/path/to", "file.txt"]
        """
        return list(os.path.split(path))

    @ml_function(description="Convert to absolute path", capabilities=[])
    def absolute(self, path: str) -> str:
        """Convert relative path to absolute path.

        Args:
            path: Relative or absolute path

        Returns:
            Absolute path

        Examples:
            path.absolute("../data/file.txt")  // "/home/user/data/file.txt"
            path.absolute("file.txt")          // "/home/user/project/file.txt"

        Note:
            Uses current working directory for resolution
        """
        return os.path.abspath(os.path.expanduser(path))

    @ml_function(description="Normalize path", capabilities=[])
    def normalize(self, path: str) -> str:
        """Normalize path (resolve .., ., //).

        Args:
            path: Path to normalize

        Returns:
            Normalized path

        Examples:
            path.normalize("/path/./to/../file")  // "/path/file"
            path.normalize("//path//to//file")    // "/path/to/file"

        Security:
            - Removes directory traversal sequences
            - Collapses redundant separators
        """
        return os.path.normpath(path)

    @ml_function(description="Get relative path", capabilities=[])
    def relative(self, from_path: str, to_path: str) -> str:
        """Get relative path from one path to another.

        Args:
            from_path: Starting path
            to_path: Destination path

        Returns:
            Relative path from from_path to to_path

        Examples:
            path.relative("/a/b/c", "/a/b/d/e")  // "../d/e"
            path.relative("/a/b", "/a/b/c")      // "c"
        """
        return os.path.relpath(to_path, from_path)

    # =====================================================================
    # Filesystem Query Operations (No Write Capabilities)
    # =====================================================================

    @ml_function(description="Check if path exists", capabilities=[])
    def exists(self, path: str) -> bool:
        """Check if path exists.

        Args:
            path: Path to check

        Returns:
            True if exists, False otherwise

        Capability:
            None required (safe metadata operation)

        Examples:
            if (path.exists("/data/file.txt")) {
                content = file.read("/data/file.txt")
            }
        """
        canonical_path = os.path.abspath(os.path.expanduser(path))
        return os.path.exists(canonical_path)

    @ml_function(description="Check if path is a file", capabilities=[])
    def isFile(self, path: str) -> bool:
        """Check if path is a file.

        Args:
            path: Path to check

        Returns:
            True if file, False otherwise

        Examples:
            if (path.isFile("/data/file.txt")) {
                size = file.size("/data/file.txt")
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
            if (path.isDirectory("/data")) {
                files = path.listDir("/data")
            }
        """
        canonical_path = os.path.abspath(os.path.expanduser(path))
        return os.path.isdir(canonical_path)

    @ml_function(description="Check if path is absolute", capabilities=[])
    def isAbsolute(self, path: str) -> bool:
        """Check if path is absolute.

        Args:
            path: Path to check

        Returns:
            True if absolute, False if relative

        Examples:
            path.isAbsolute("/path/to/file")  // true
            path.isAbsolute("relative/path")  // false
        """
        return os.path.isabs(path)

    # =====================================================================
    # Directory Listing Operations (Requires path.read)
    # =====================================================================

    @ml_function(description="List directory contents", capabilities=["path.read"])
    def listDir(self, dir_path: str = ".") -> list:
        """List files and directories in directory.

        Args:
            dir_path: Directory path (default: current directory)

        Returns:
            Array of filenames (not full paths)

        Capability:
            Requires: path.read or path.read:<path-pattern>

        Examples:
            files = path.listDir("/data")
            for file in files {
                console.log(file)
            }

        Security:
            - Returns only names, not full paths
            - Does not traverse subdirectories
            - Sorted alphabetically
        """
        canonical_path = os.path.abspath(os.path.expanduser(dir_path))

        if not os.path.isdir(canonical_path):
            raise NotADirectoryError(f"Not a directory: {dir_path}")

        return sorted(os.listdir(canonical_path))

    @ml_function(description="List files matching glob pattern", capabilities=["path.read"])
    def glob(self, pattern: str) -> list:
        """List files matching glob pattern.

        Args:
            pattern: Glob pattern (*, ?, [abc], **)

        Returns:
            Array of matching file paths

        Capability:
            Requires: path.read or path.read:<path-pattern>

        Examples:
            txt_files = path.glob("*.txt")
            all_txt = path.glob("**/*.txt")  // Recursive
            specific = path.glob("data/file[0-9].txt")

        Patterns:
            * - matches any characters
            ? - matches single character
            [abc] - matches a, b, or c
            ** - matches directories recursively
        """
        # Convert to absolute pattern if relative
        if not os.path.isabs(pattern):
            pattern = os.path.join(os.getcwd(), pattern)

        return sorted(glob.glob(pattern, recursive=True))

    @ml_function(description="Walk directory tree", capabilities=["path.read"])
    def walk(self, dir_path: str, max_depth: int = -1) -> list:
        """Walk directory tree and list all files.

        Args:
            dir_path: Root directory to walk
            max_depth: Maximum depth (-1 for unlimited)

        Returns:
            Array of file paths (relative to dir_path)

        Capability:
            Requires: path.read or path.read:<path-pattern>

        Examples:
            all_files = path.walk("/data")
            shallow = path.walk("/data", 1)  // Only 1 level deep

        Security:
            - Respects max_depth limit
            - Returns relative paths for safety
        """
        canonical_path = os.path.abspath(os.path.expanduser(dir_path))
        all_files = []

        for root, dirs, files in os.walk(canonical_path):
            # Calculate current depth
            depth = root[len(canonical_path):].count(os.sep)

            if max_depth >= 0 and depth >= max_depth:
                # Don't descend further
                dirs[:] = []

            for filename in files:
                full_path = os.path.join(root, filename)
                rel_path = os.path.relpath(full_path, canonical_path)
                all_files.append(rel_path)

        return sorted(all_files)

    # =====================================================================
    # Directory Management (Requires path.write)
    # =====================================================================

    @ml_function(description="Create directory", capabilities=["path.write"])
    def createDir(self, dir_path: str, parents: bool = True) -> None:
        """Create directory (and parents if needed).

        Args:
            dir_path: Directory path to create
            parents: Create parent directories (default: true)

        Capability:
            Requires: path.write or path.write:<path-pattern>

        Examples:
            path.createDir("/data/output")
            path.createDir("/a/b/c/d", true)  // Creates all parents

        Security:
            - Creates parent directories by default
            - Silently succeeds if directory already exists
        """
        canonical_path = os.path.abspath(os.path.expanduser(dir_path))
        os.makedirs(canonical_path, exist_ok=True)

    @ml_function(description="Remove empty directory", capabilities=["path.write"])
    def removeDir(self, dir_path: str) -> None:
        """Remove directory (must be empty).

        Args:
            dir_path: Directory path to remove

        Capability:
            Requires: path.write or path.write:<path-pattern>

        Examples:
            path.removeDir("/tmp/empty")

        Security:
            - Only removes empty directories
            - Use removeDirRecursive() for non-empty directories
        """
        canonical_path = os.path.abspath(os.path.expanduser(dir_path))
        os.rmdir(canonical_path)

    @ml_function(description="Remove directory recursively", capabilities=["path.write"])
    def removeDirRecursive(self, dir_path: str) -> None:
        """Remove directory and all contents recursively.

        Args:
            dir_path: Directory path to remove

        Capability:
            Requires: path.write or path.write:<path-pattern>

        Examples:
            path.removeDirRecursive("/tmp/data")

        Security:
            - DANGEROUS: Removes all contents recursively
            - No confirmation or undo
            - Use with extreme caution
        """
        canonical_path = os.path.abspath(os.path.expanduser(dir_path))

        import shutil
        shutil.rmtree(canonical_path)

    # =====================================================================
    # Path Utility Functions
    # =====================================================================

    @ml_function(description="Get current working directory", capabilities=[])
    def cwd(self) -> str:
        """Get current working directory.

        Returns:
            Current working directory absolute path

        Capability:
            None required

        Examples:
            current = path.cwd()
            console.log("Working in: " + current)
        """
        return os.getcwd()

    @ml_function(description="Get home directory", capabilities=[])
    def home(self) -> str:
        """Get user home directory.

        Returns:
            User home directory path

        Capability:
            None required

        Examples:
            home_dir = path.home()
            config = path.join(home_dir, ".config", "app")
        """
        return str(PyPath.home())

    @ml_function(description="Get temporary directory", capabilities=[])
    def tempDir(self) -> str:
        """Get system temporary directory.

        Returns:
            Temporary directory path

        Capability:
            None required

        Examples:
            tmp = path.tempDir()
            temp_file = path.join(tmp, "data.tmp")
        """
        import tempfile
        return tempfile.gettempdir()

    @ml_function(description="Get path separator for OS", capabilities=[])
    def separator(self) -> str:
        """Get path separator for current OS.

        Returns:
            Path separator ("/" on Unix, "\\" on Windows)

        Examples:
            sep = path.separator()  // "/" or "\\"
        """
        return os.sep

    @ml_function(description="Get path delimiter for OS", capabilities=[])
    def delimiter(self) -> str:
        """Get path list delimiter for current OS.

        Returns:
            Path delimiter (":" on Unix, ";" on Windows)

        Examples:
            delim = path.delimiter()  // ":" or ";"
        """
        return os.pathsep


# Global module instance for ML programs
path = PathModule()


__all__ = ["PathModule"]
