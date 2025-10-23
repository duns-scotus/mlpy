"""Unit tests for SourceMapIndex."""

import pytest
from mlpy.debugging.source_map_index import SourceMapIndex
from mlpy.ml.codegen.enhanced_source_maps import (
    EnhancedSourceMap,
    SourceLocation,
    SourceMapping,
)


class TestSourceMapIndex:
    """Test SourceMapIndex bidirectional lookups."""

    def test_basic_bidirectional_lookup(self):
        """Test basic ML→Python and Python→ML lookups."""
        source_map = EnhancedSourceMap()

        # Add mappings
        source_map.mappings.append(
            SourceMapping(
                generated=SourceLocation(line=10, column=0),
                original=SourceLocation(line=5, column=0),
                source_file="test.ml",
                node_type="assignment",
            )
        )

        source_map.mappings.append(
            SourceMapping(
                generated=SourceLocation(line=11, column=0),
                original=SourceLocation(line=6, column=0),
                source_file="test.ml",
                node_type="return_statement",
            )
        )

        # Build index
        index = SourceMapIndex.from_source_map(source_map, "test.py")

        # Test forward lookup
        assert index.ml_line_to_first_py_line("test.ml", 5) == 10
        assert index.ml_line_to_first_py_line("test.ml", 6) == 11

        # Test reverse lookup
        assert index.py_line_to_ml("test.py", 10) == ("test.ml", 5, 0)
        assert index.py_line_to_ml("test.py", 11) == ("test.ml", 6, 0)

    def test_invalid_lookups(self):
        """Test lookups for non-existent positions."""
        source_map = EnhancedSourceMap()

        source_map.mappings.append(
            SourceMapping(
                generated=SourceLocation(line=10, column=0),
                original=SourceLocation(line=5, column=0),
                source_file="test.ml",
            )
        )

        index = SourceMapIndex.from_source_map(source_map, "test.py")

        # Test invalid ML line
        assert index.ml_line_to_first_py_line("test.ml", 99) is None
        assert index.ml_line_to_all_py_lines("test.ml", 99) == []

        # Test invalid Python line
        assert index.py_line_to_ml("test.py", 99) is None

        # Test invalid file
        assert index.ml_line_to_first_py_line("other.ml", 5) is None

    def test_multi_line_statement(self):
        """Test ML line that generates multiple Python lines."""
        source_map = EnhancedSourceMap()

        # ML line 5 generates Python lines 10, 11, 12
        for py_line in [10, 11, 12]:
            source_map.mappings.append(
                SourceMapping(
                    generated=SourceLocation(line=py_line, column=0),
                    original=SourceLocation(line=5, column=0),
                    source_file="test.ml",
                    node_type="complex_expression",
                )
            )

        index = SourceMapIndex.from_source_map(source_map, "test.py")

        # Should get first Python line (for breakpoints)
        assert index.ml_line_to_first_py_line("test.ml", 5) == 10

        # Should get all Python lines
        assert index.ml_line_to_all_py_lines("test.ml", 5) == [10, 11, 12]

        # All Python lines map back to same ML line
        assert index.py_line_to_ml("test.py", 10) == ("test.ml", 5, 0)
        assert index.py_line_to_ml("test.py", 11) == ("test.ml", 5, 0)
        assert index.py_line_to_ml("test.py", 12) == ("test.ml", 5, 0)

    def test_multi_line_statement_unsorted(self):
        """Test that Python lines are sorted even if added out of order."""
        source_map = EnhancedSourceMap()

        # Add Python lines out of order
        for py_line in [12, 10, 11]:
            source_map.mappings.append(
                SourceMapping(
                    generated=SourceLocation(line=py_line, column=0),
                    original=SourceLocation(line=5, column=0),
                    source_file="test.ml",
                )
            )

        index = SourceMapIndex.from_source_map(source_map, "test.py")

        # Should still get lowest line first
        assert index.ml_line_to_first_py_line("test.ml", 5) == 10

        # Should be sorted
        assert index.ml_line_to_all_py_lines("test.ml", 5) == [10, 11, 12]

    def test_next_ml_line(self):
        """Test finding next executable ML line."""
        source_map = EnhancedSourceMap()

        # Add non-consecutive ML lines (comments/whitespace skipped)
        for ml_line, py_line in [(5, 10), (7, 11), (10, 12)]:
            source_map.mappings.append(
                SourceMapping(
                    generated=SourceLocation(line=py_line, column=0),
                    original=SourceLocation(line=ml_line, column=0),
                    source_file="test.ml",
                )
            )

        index = SourceMapIndex.from_source_map(source_map, "test.py")

        # Test next line navigation
        assert index.get_next_ml_line("test.ml", 5) == 7
        assert index.get_next_ml_line("test.ml", 7) == 10
        assert index.get_next_ml_line("test.ml", 10) is None  # End of file

        # Test from before first line
        assert index.get_next_ml_line("test.ml", 1) == 5

    def test_is_executable(self):
        """Test checking if ML line is executable."""
        source_map = EnhancedSourceMap()

        source_map.mappings.append(
            SourceMapping(
                generated=SourceLocation(line=10, column=0),
                original=SourceLocation(line=5, column=0),
                source_file="test.ml",
            )
        )

        index = SourceMapIndex.from_source_map(source_map, "test.py")

        # Line 5 is executable
        assert index.is_ml_line_executable("test.ml", 5) is True

        # Other lines are not
        assert index.is_ml_line_executable("test.ml", 1) is False
        assert index.is_ml_line_executable("test.ml", 6) is False

    def test_multiple_files(self):
        """Test handling multiple ML source files."""
        source_map = EnhancedSourceMap()

        # File 1
        source_map.mappings.append(
            SourceMapping(
                generated=SourceLocation(line=10, column=0),
                original=SourceLocation(line=5, column=0),
                source_file="file1.ml",
            )
        )

        # File 2
        source_map.mappings.append(
            SourceMapping(
                generated=SourceLocation(line=20, column=0),
                original=SourceLocation(line=5, column=0),
                source_file="file2.ml",
            )
        )

        index = SourceMapIndex.from_source_map(source_map, "combined.py")

        # Each file's line 5 maps to different Python line
        assert index.ml_line_to_first_py_line("file1.ml", 5) == 10
        assert index.ml_line_to_first_py_line("file2.ml", 5) == 20

        # Reverse lookups distinguish files
        assert index.py_line_to_ml("combined.py", 10) == ("file1.ml", 5, 0)
        assert index.py_line_to_ml("combined.py", 20) == ("file2.ml", 5, 0)

    def test_column_preservation(self):
        """Test that column information is preserved."""
        source_map = EnhancedSourceMap()

        source_map.mappings.append(
            SourceMapping(
                generated=SourceLocation(line=10, column=4),
                original=SourceLocation(line=5, column=8),
                source_file="test.ml",
            )
        )

        index = SourceMapIndex.from_source_map(source_map, "test.py")

        # Column should be preserved in reverse lookup
        ml_file, ml_line, ml_col = index.py_line_to_ml("test.py", 10)
        assert ml_col == 8

    def test_empty_source_map(self):
        """Test handling empty source map."""
        source_map = EnhancedSourceMap()
        index = SourceMapIndex.from_source_map(source_map, "test.py")

        # All lookups should return None/empty
        assert index.ml_line_to_first_py_line("test.ml", 1) is None
        assert index.ml_line_to_all_py_lines("test.ml", 1) == []
        assert index.py_line_to_ml("test.py", 1) is None
        assert index.is_ml_line_executable("test.ml", 1) is False
        assert index.get_next_ml_line("test.ml", 1) is None

    def test_get_ml_line_count(self):
        """Test counting executable ML lines."""
        source_map = EnhancedSourceMap()

        # Add 3 executable lines
        for ml_line, py_line in [(5, 10), (6, 11), (8, 12)]:
            source_map.mappings.append(
                SourceMapping(
                    generated=SourceLocation(line=py_line, column=0),
                    original=SourceLocation(line=ml_line, column=0),
                    source_file="test.ml",
                )
            )

        index = SourceMapIndex.from_source_map(source_map, "test.py")

        assert index.get_ml_line_count("test.ml") == 3
        assert index.get_ml_line_count("other.ml") == 0

    def test_get_all_ml_files(self):
        """Test getting all ML source files."""
        source_map = EnhancedSourceMap()

        # Add mappings for multiple files
        for file_name in ["file1.ml", "file2.ml", "file3.ml"]:
            source_map.mappings.append(
                SourceMapping(
                    generated=SourceLocation(line=10, column=0),
                    original=SourceLocation(line=5, column=0),
                    source_file=file_name,
                )
            )

        index = SourceMapIndex.from_source_map(source_map, "test.py")

        files = index.get_all_ml_files()
        assert len(files) == 3
        assert "file1.ml" in files
        assert "file2.ml" in files
        assert "file3.ml" in files

    def test_duplicate_python_lines_filtered(self):
        """Test that duplicate Python lines for same ML line are filtered."""
        source_map = EnhancedSourceMap()

        # Add same mapping twice (shouldn't happen but be defensive)
        for _ in range(2):
            source_map.mappings.append(
                SourceMapping(
                    generated=SourceLocation(line=10, column=0),
                    original=SourceLocation(line=5, column=0),
                    source_file="test.ml",
                )
            )

        index = SourceMapIndex.from_source_map(source_map, "test.py")

        # Should only have one Python line
        assert index.ml_line_to_all_py_lines("test.ml", 5) == [10]
