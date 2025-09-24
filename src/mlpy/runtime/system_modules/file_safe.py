"""Safe file operations with capability-based access control."""

import os
import pathlib
from contextlib import contextmanager
from typing import Union

from ..capabilities.decorators import capability_safe, requires_capability
from ..capabilities.exceptions import CapabilityNotFoundError
from ..capabilities.manager import has_capability, use_capability

PathLike = Union[str, pathlib.Path]


@capability_safe(["file"], strict=True)
class SafeFile:
    """Safe file operations that require file capabilities."""

    @staticmethod
    def _validate_file_access(file_path: PathLike, operation: str) -> str:
        """Validate file access and return normalized path."""
        path_str = str(file_path)

        # Check capability
        if not has_capability("file", path_str, operation):
            raise CapabilityNotFoundError("file", path_str)

        return path_str

    @staticmethod
    @contextmanager
    def open(file_path: PathLike, mode: str = "r", encoding: str = "utf-8", **kwargs):
        """Safe file opening with capability validation."""
        path_str = str(file_path)

        # Determine operation from mode
        if "r" in mode:
            operation = "read"
        elif "w" in mode or "a" in mode:
            operation = "write"
        else:
            operation = "read"  # Default to read

        # Validate access
        SafeFile._validate_file_access(path_str, operation)

        # Use the capability
        use_capability("file", path_str, operation)

        # Open file with standard library
        file_handle = open(file_path, mode, encoding=encoding, **kwargs)

        try:
            yield file_handle
        finally:
            file_handle.close()

    @staticmethod
    @requires_capability("file", auto_use=False)
    def read_text(file_path: PathLike, encoding: str = "utf-8") -> str:
        """Read entire text file with capability validation."""
        path_str = SafeFile._validate_file_access(file_path, "read")
        use_capability("file", path_str, "read")

        with open(file_path, "r", encoding=encoding) as f:
            return f.read()

    @staticmethod
    @requires_capability("file", auto_use=False)
    def write_text(file_path: PathLike, content: str, encoding: str = "utf-8") -> None:
        """Write text to file with capability validation."""
        path_str = SafeFile._validate_file_access(file_path, "write")
        use_capability("file", path_str, "write")

        with open(file_path, "w", encoding=encoding) as f:
            f.write(content)

    @staticmethod
    @requires_capability("file", auto_use=False)
    def read_bytes(file_path: PathLike) -> bytes:
        """Read entire binary file with capability validation."""
        path_str = SafeFile._validate_file_access(file_path, "read")
        use_capability("file", path_str, "read")

        with open(file_path, "rb") as f:
            return f.read()

    @staticmethod
    @requires_capability("file", auto_use=False)
    def write_bytes(file_path: PathLike, content: bytes) -> None:
        """Write bytes to file with capability validation."""
        path_str = SafeFile._validate_file_access(file_path, "write")
        use_capability("file", path_str, "write")

        with open(file_path, "wb") as f:
            f.write(content)

    @staticmethod
    @requires_capability("file", auto_use=False)
    def exists(file_path: PathLike) -> bool:
        """Check if file exists with capability validation."""
        path_str = SafeFile._validate_file_access(file_path, "read")
        use_capability("file", path_str, "read")

        return os.path.exists(file_path)

    @staticmethod
    @requires_capability("file", auto_use=False)
    def is_file(file_path: PathLike) -> bool:
        """Check if path is a file with capability validation."""
        path_str = SafeFile._validate_file_access(file_path, "read")
        use_capability("file", path_str, "read")

        return os.path.isfile(file_path)

    @staticmethod
    @requires_capability("file", auto_use=False)
    def is_directory(file_path: PathLike) -> bool:
        """Check if path is a directory with capability validation."""
        path_str = SafeFile._validate_file_access(file_path, "read")
        use_capability("file", path_str, "read")

        return os.path.isdir(file_path)

    @staticmethod
    @requires_capability("file", auto_use=False)
    def get_size(file_path: PathLike) -> int:
        """Get file size with capability validation."""
        path_str = SafeFile._validate_file_access(file_path, "read")
        use_capability("file", path_str, "read")

        return os.path.getsize(file_path)

    @staticmethod
    @requires_capability("file", auto_use=False)
    def list_directory(dir_path: PathLike) -> list[str]:
        """List directory contents with capability validation."""
        path_str = SafeFile._validate_file_access(dir_path, "read")
        use_capability("file", path_str, "read")

        return os.listdir(dir_path)

    @staticmethod
    @requires_capability("file", auto_use=False)
    def create_directory(dir_path: PathLike, parents: bool = False) -> None:
        """Create directory with capability validation."""
        path_str = SafeFile._validate_file_access(dir_path, "write")
        use_capability("file", path_str, "write")

        if parents:
            os.makedirs(dir_path, exist_ok=True)
        else:
            os.mkdir(dir_path)

    @staticmethod
    @requires_capability("file", auto_use=False)
    def remove_file(file_path: PathLike) -> None:
        """Remove file with capability validation."""
        path_str = SafeFile._validate_file_access(file_path, "write")
        use_capability("file", path_str, "write")

        os.remove(file_path)

    @staticmethod
    @requires_capability("file", auto_use=False)
    def copy_file(src_path: PathLike, dst_path: PathLike) -> None:
        """Copy file with capability validation for both source and destination."""
        src_str = SafeFile._validate_file_access(src_path, "read")
        dst_str = SafeFile._validate_file_access(dst_path, "write")

        use_capability("file", src_str, "read")
        use_capability("file", dst_str, "write")

        import shutil

        shutil.copy2(src_path, dst_path)

    @staticmethod
    @requires_capability("file", auto_use=False)
    def move_file(src_path: PathLike, dst_path: PathLike) -> None:
        """Move file with capability validation."""
        src_str = SafeFile._validate_file_access(src_path, "write")
        dst_str = SafeFile._validate_file_access(dst_path, "write")

        use_capability("file", src_str, "write")
        use_capability("file", dst_str, "write")

        import shutil

        shutil.move(src_path, dst_path)


# Create global instance
file_safe = SafeFile()

# Export functions for convenience
open = file_safe.open
read_text = file_safe.read_text
write_text = file_safe.write_text
read_bytes = file_safe.read_bytes
write_bytes = file_safe.write_bytes
exists = file_safe.exists
is_file = file_safe.is_file
is_directory = file_safe.is_directory
get_size = file_safe.get_size
list_directory = file_safe.list_directory
create_directory = file_safe.create_directory
remove_file = file_safe.remove_file
copy_file = file_safe.copy_file
move_file = file_safe.move_file

# Module metadata
__all__ = [
    "SafeFile",
    "file_safe",
    "open",
    "read_text",
    "write_text",
    "read_bytes",
    "write_bytes",
    "exists",
    "is_file",
    "is_directory",
    "get_size",
    "list_directory",
    "create_directory",
    "remove_file",
    "copy_file",
    "move_file",
]
