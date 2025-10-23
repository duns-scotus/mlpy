"""Unit tests for MLDebugger."""

import pytest
from mlpy.debugging.debugger import MLDebugger, Breakpoint, StepMode
from mlpy.debugging.source_map_index import SourceMapIndex
from mlpy.ml.codegen.enhanced_source_maps import (
    EnhancedSourceMap,
    SourceLocation,
    SourceMapping,
)


class TestBreakpointManagement:
    """Test breakpoint creation and management."""

    def test_set_valid_breakpoint(self):
        """Test setting breakpoint on executable line."""
        source_map = EnhancedSourceMap()
        source_map.mappings.append(
            SourceMapping(
                generated=SourceLocation(line=10, column=0),
                original=SourceLocation(line=5, column=0),
                source_file="test.ml",
            )
        )

        index = SourceMapIndex.from_source_map(source_map, "test.py")
        debugger = MLDebugger("test.ml", index, "# test code")

        # Set breakpoint
        bp = debugger.set_breakpoint("test.ml", 5)

        assert bp is not None
        assert bp.id == 1
        assert bp.ml_line == 5
        assert bp.enabled is True
        assert 10 in debugger._breakpoint_py_lines

    def test_set_invalid_breakpoint(self):
        """Test setting breakpoint on non-executable line."""
        source_map = EnhancedSourceMap()
        source_map.mappings.append(
            SourceMapping(
                generated=SourceLocation(line=10, column=0),
                original=SourceLocation(line=5, column=0),
                source_file="test.ml",
            )
        )

        index = SourceMapIndex.from_source_map(source_map, "test.py")
        debugger = MLDebugger("test.ml", index, "# test code")

        # Try to set breakpoint on non-executable line
        bp = debugger.set_breakpoint("test.ml", 99)

        assert bp is None
        assert len(debugger.breakpoints) == 0

    def test_delete_breakpoint(self):
        """Test deleting a breakpoint."""
        source_map = EnhancedSourceMap()
        source_map.mappings.append(
            SourceMapping(
                generated=SourceLocation(line=10, column=0),
                original=SourceLocation(line=5, column=0),
                source_file="test.ml",
            )
        )

        index = SourceMapIndex.from_source_map(source_map, "test.py")
        debugger = MLDebugger("test.ml", index, "# test code")

        bp = debugger.set_breakpoint("test.ml", 5)
        bp_id = bp.id

        # Delete breakpoint
        assert debugger.delete_breakpoint(bp_id) is True
        assert bp_id not in debugger.breakpoints
        assert 10 not in debugger._breakpoint_py_lines

    def test_enable_disable_breakpoint(self):
        """Test enabling and disabling breakpoints."""
        source_map = EnhancedSourceMap()
        source_map.mappings.append(
            SourceMapping(
                generated=SourceLocation(line=10, column=0),
                original=SourceLocation(line=5, column=0),
                source_file="test.ml",
            )
        )

        index = SourceMapIndex.from_source_map(source_map, "test.py")
        debugger = MLDebugger("test.ml", index, "# test code")

        bp = debugger.set_breakpoint("test.ml", 5)
        bp_id = bp.id

        # Disable
        assert debugger.disable_breakpoint(bp_id) is True
        assert debugger.breakpoints[bp_id].enabled is False
        assert 10 not in debugger._breakpoint_py_lines  # Removed from fast lookup

        # Enable
        assert debugger.enable_breakpoint(bp_id) is True
        assert debugger.breakpoints[bp_id].enabled is True
        assert 10 in debugger._breakpoint_py_lines  # Added back to fast lookup

    def test_multiple_breakpoints(self):
        """Test managing multiple breakpoints."""
        source_map = EnhancedSourceMap()
        for ml_line, py_line in [(5, 10), (6, 11), (8, 12)]:
            source_map.mappings.append(
                SourceMapping(
                    generated=SourceLocation(line=py_line, column=0),
                    original=SourceLocation(line=ml_line, column=0),
                    source_file="test.ml",
                )
            )

        index = SourceMapIndex.from_source_map(source_map, "test.py")
        debugger = MLDebugger("test.ml", index, "# test code")

        # Set multiple breakpoints
        bp1 = debugger.set_breakpoint("test.ml", 5)
        bp2 = debugger.set_breakpoint("test.ml", 6)
        bp3 = debugger.set_breakpoint("test.ml", 8)

        assert len(debugger.breakpoints) == 3
        assert bp1.id == 1
        assert bp2.id == 2
        assert bp3.id == 3
        assert debugger._breakpoint_py_lines == {10, 11, 12}


class TestVariableInspection:
    """Test variable inspection via live frames."""

    def test_get_variable_from_locals(self):
        """Test getting variable from local scope."""
        source_map = EnhancedSourceMap()
        source_map.mappings.append(
            SourceMapping(
                generated=SourceLocation(line=1, column=0),
                original=SourceLocation(line=1, column=0),
                source_file="test.ml",
            )
        )

        index = SourceMapIndex.from_source_map(source_map, "test.py")

        # Simple Python code with a variable
        py_code = """
x = 42
y = "hello"
"""

        debugger = MLDebugger("test.ml", index, py_code)

        # Manually set a frame (simulating paused execution)
        class FakeFrame:
            f_locals = {"x": 42, "y": "hello"}
            f_globals = {}
            f_back = None

        debugger.current_frame = FakeFrame()

        # Get variables
        assert debugger.get_variable("x") == 42
        assert debugger.get_variable("y") == "hello"
        assert debugger.get_variable("z") is None

    def test_get_all_locals(self):
        """Test getting all local variables."""
        source_map = EnhancedSourceMap()
        index = SourceMapIndex.from_source_map(source_map, "test.py")

        debugger = MLDebugger("test.ml", index, "")

        class FakeFrame:
            f_locals = {"x": 1, "y": 2, "__hidden__": 3, "_ml_internal": 4}
            f_globals = {}
            f_back = None

        debugger.current_frame = FakeFrame()

        locals_dict = debugger.get_all_locals()

        # Should filter out internal variables
        assert locals_dict == {"x": 1, "y": 2}

    def test_no_frame(self):
        """Test variable inspection with no current frame."""
        source_map = EnhancedSourceMap()
        index = SourceMapIndex.from_source_map(source_map, "test.py")

        debugger = MLDebugger("test.ml", index, "")

        assert debugger.get_variable("x") is None
        assert debugger.get_all_locals() == {}


class TestStepModes:
    """Test step execution modes."""

    def test_step_next_mode(self):
        """Test step next (step over) mode."""
        source_map = EnhancedSourceMap()
        for ml_line, py_line in [(5, 10), (6, 11)]:
            source_map.mappings.append(
                SourceMapping(
                    generated=SourceLocation(line=py_line, column=0),
                    original=SourceLocation(line=ml_line, column=0),
                    source_file="test.ml",
                )
            )

        index = SourceMapIndex.from_source_map(source_map, "test.py")
        debugger = MLDebugger("test.ml", index, "")

        # Simulate being paused at line 5
        debugger.current_ml_position = ("test.ml", 5, 0)

        # Activate step next
        debugger.step_next()

        assert debugger.step_mode == StepMode.NEXT
        assert debugger._step_start_ml_line == 5

        # Should break at line 6 (different ML line)
        assert debugger._should_break("test.ml", 6, 11) is True

        # Should not break at line 5 again
        assert debugger._should_break("test.ml", 5, 10) is False

    def test_continue_mode(self):
        """Test continue execution mode."""
        source_map = EnhancedSourceMap()
        index = SourceMapIndex.from_source_map(source_map, "test.py")

        debugger = MLDebugger("test.ml", index, "")

        # Set step mode
        debugger.step_mode = StepMode.NEXT

        # Continue should clear step mode
        debugger.continue_execution()

        assert debugger.step_mode == StepMode.NONE


class TestSourceDisplay:
    """Test source code context display."""

    @pytest.mark.skip(reason="Path handling on Windows needs adjustment")
    def test_show_source_context(self, tmp_path):
        """Test displaying source code around current line."""
        # Create a test ML file
        ml_file = tmp_path / "test.ml"
        ml_file.write_text("line 1\nline 2\nline 3\nline 4\nline 5\nline 6\nline 7\n")

        source_map = EnhancedSourceMap()
        source_map.mappings.append(
            SourceMapping(
                generated=SourceLocation(line=10, column=0),
                original=SourceLocation(line=4, column=0),
                source_file=str(ml_file),
            )
        )

        index = SourceMapIndex.from_source_map(source_map, "test.py")
        debugger = MLDebugger(str(ml_file), index, "")

        # Simulate being paused at line 4
        debugger.current_ml_position = (str(ml_file), 4, 0)

        # Get context
        context = debugger.show_source_context(lines_before=2, lines_after=2)

        # Should show lines 2-6 with line 4 marked
        assert "2 |" in context and "line 2" in context
        assert "3 |" in context and "line 3" in context
        assert "=> 4 |" in context and "line 4" in context
        assert "5 |" in context and "line 5" in context
        assert "6 |" in context and "line 6" in context

    def test_show_source_no_position(self):
        """Test displaying source when not paused."""
        source_map = EnhancedSourceMap()
        index = SourceMapIndex.from_source_map(source_map, "test.py")

        debugger = MLDebugger("test.ml", index, "")

        context = debugger.show_source_context()
        assert context == "Not currently paused"


class TestTraceFunction:
    """Test the trace function behavior."""

    def test_should_break_at_breakpoint(self):
        """Test that trace function identifies breakpoints."""
        source_map = EnhancedSourceMap()
        source_map.mappings.append(
            SourceMapping(
                generated=SourceLocation(line=10, column=0),
                original=SourceLocation(line=5, column=0),
                source_file="test.ml",
            )
        )

        index = SourceMapIndex.from_source_map(source_map, "test.py")
        debugger = MLDebugger("test.ml", index, "")

        # Set breakpoint
        debugger.set_breakpoint("test.ml", 5)

        # Should break at line 5/10
        assert debugger._should_break("test.ml", 5, 10) is True

        # Should not break at other lines
        assert debugger._should_break("test.ml", 6, 11) is False

    def test_breakpoint_hit_count(self):
        """Test that breakpoint hit counts are incremented."""
        source_map = EnhancedSourceMap()
        source_map.mappings.append(
            SourceMapping(
                generated=SourceLocation(line=10, column=0),
                original=SourceLocation(line=5, column=0),
                source_file="test.ml",
            )
        )

        index = SourceMapIndex.from_source_map(source_map, "test.py")
        debugger = MLDebugger("test.ml", index, "")

        bp = debugger.set_breakpoint("test.ml", 5)
        assert bp.hit_count == 0

        # Simulate hitting breakpoint
        debugger._should_break("test.ml", 5, 10)
        assert bp.hit_count == 1

        debugger._should_break("test.ml", 5, 10)
        assert bp.hit_count == 2

    def test_disabled_breakpoint_not_hit(self):
        """Test that disabled breakpoints don't trigger."""
        source_map = EnhancedSourceMap()
        source_map.mappings.append(
            SourceMapping(
                generated=SourceLocation(line=10, column=0),
                original=SourceLocation(line=5, column=0),
                source_file="test.ml",
            )
        )

        index = SourceMapIndex.from_source_map(source_map, "test.py")
        debugger = MLDebugger("test.ml", index, "")

        bp = debugger.set_breakpoint("test.ml", 5)
        debugger.disable_breakpoint(bp.id)

        # Should not break
        assert debugger._should_break("test.ml", 5, 10) is False
