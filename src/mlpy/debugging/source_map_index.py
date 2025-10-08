"""Bidirectional ML↔Python source position lookup for debugging.

This module provides fast O(1) lookups between ML source positions and
generated Python positions, enabling the debugger to map between the two
representations seamlessly.
"""

from collections import defaultdict
from dataclasses import dataclass
from typing import Optional

from mlpy.ml.codegen.enhanced_source_maps import EnhancedSourceMap


@dataclass
class SourceMapIndex:
    """Fast bidirectional source position lookup.

    This class builds lookup indexes from EnhancedSourceMap to enable
    O(1) position translation between ML and Python code.

    Attributes:
        ml_to_py: Maps (ml_file, ml_line) to list of Python lines
        py_to_ml: Maps (py_file, py_line) to (ml_file, ml_line, ml_col)
        py_file: Path to the generated Python file
    """

    # Forward lookup: (ml_file, ml_line) → [py_lines]
    ml_to_py: dict[tuple[str, int], list[int]]

    # Reverse lookup: (py_file, py_line) → (ml_file, ml_line, ml_col)
    py_to_ml: dict[tuple[str, int], tuple[str, int, int]]

    # Generated Python filename
    py_file: str

    @classmethod
    def from_source_map(
        cls, source_map: EnhancedSourceMap, py_file: str
    ) -> "SourceMapIndex":
        """Build lookup index from enhanced source map.

        Args:
            source_map: Enhanced source map from transpilation
            py_file: Path to generated Python file

        Returns:
            Indexed source map for fast O(1) lookups
        """
        ml_to_py = defaultdict(list)
        py_to_ml = {}

        for mapping in source_map.mappings:
            if mapping.original and mapping.source_file:
                # Forward lookup: ML → Python
                ml_key = (mapping.source_file, mapping.original.line)
                py_line = mapping.generated.line

                # Avoid duplicates
                if py_line not in ml_to_py[ml_key]:
                    ml_to_py[ml_key].append(py_line)

                # Reverse lookup: Python → ML
                py_key = (py_file, py_line)
                py_to_ml[py_key] = (
                    mapping.source_file,
                    mapping.original.line,
                    mapping.original.column,
                )

        # Sort Python lines for each ML line (to get first line consistently)
        for ml_key in ml_to_py:
            ml_to_py[ml_key].sort()

        return cls(ml_to_py=dict(ml_to_py), py_to_ml=py_to_ml, py_file=py_file)

    def ml_line_to_first_py_line(self, ml_file: str, ml_line: int) -> Optional[int]:
        """Get first Python line for an ML line (for breakpoints).

        When a single ML statement generates multiple Python lines,
        this returns the first one, which is where breakpoints should
        be set.

        Args:
            ml_file: ML source file path
            ml_line: ML line number (1-indexed)

        Returns:
            First Python line number, or None if line not executable
        """
        py_lines = self.ml_to_py.get((ml_file, ml_line), [])
        return py_lines[0] if py_lines else None

    def ml_line_to_all_py_lines(self, ml_file: str, ml_line: int) -> list[int]:
        """Get all Python lines for an ML line.

        Useful for complex statements that generate multiple Python lines.

        Args:
            ml_file: ML source file path
            ml_line: ML line number (1-indexed)

        Returns:
            List of Python line numbers (may be empty)
        """
        return self.ml_to_py.get((ml_file, ml_line), [])

    def py_line_to_ml(
        self, py_file: str, py_line: int
    ) -> Optional[tuple[str, int, int]]:
        """Get ML position for a Python line.

        Args:
            py_file: Python file path
            py_line: Python line number (1-indexed)

        Returns:
            Tuple of (ml_file, ml_line, ml_col) or None if no mapping
        """
        return self.py_to_ml.get((py_file, py_line))

    def is_ml_line_executable(self, ml_file: str, ml_line: int) -> bool:
        """Check if ML line is executable (has Python mapping).

        Args:
            ml_file: ML source file path
            ml_line: ML line number (1-indexed)

        Returns:
            True if line has generated Python code
        """
        return (ml_file, ml_line) in self.ml_to_py

    def get_next_ml_line(self, ml_file: str, current_ml_line: int) -> Optional[int]:
        """Get next executable ML line after current line.

        Useful for implementing "step to next line" functionality.

        Args:
            ml_file: ML source file path
            current_ml_line: Current ML line number

        Returns:
            Next executable ML line number, or None if at end of file
        """
        # Get all ML lines in this file
        ml_lines = sorted(
            set(ml_line for (mf, ml_line) in self.ml_to_py.keys() if mf == ml_file)
        )

        # Find next line after current
        for ml_line in ml_lines:
            if ml_line > current_ml_line:
                return ml_line

        return None  # No next line (end of file)

    def get_ml_line_count(self, ml_file: str) -> int:
        """Get count of executable ML lines in a file.

        Args:
            ml_file: ML source file path

        Returns:
            Number of executable lines
        """
        return len([key for key in self.ml_to_py.keys() if key[0] == ml_file])

    def get_all_ml_files(self) -> list[str]:
        """Get list of all ML source files in this index.

        Returns:
            List of ML source file paths
        """
        return sorted(set(ml_file for (ml_file, _) in self.ml_to_py.keys()))
