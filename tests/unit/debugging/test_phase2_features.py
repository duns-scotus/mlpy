"""Unit tests for Phase 2 debugging features."""

import pytest
from mlpy.debugging.debugger import MLDebugger, Breakpoint
from mlpy.debugging.source_map_index import SourceMapIndex
from mlpy.ml.codegen.enhanced_source_maps import (
    EnhancedSourceMap,
    SourceLocation,
    SourceMapping,
)


class TestConditionalBreakpoints:
    """Test conditional breakpoint functionality."""

    def test_breakpoint_with_simple_condition(self):
        """Test breakpoint that breaks only when condition is true."""
        # Create source map
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

        # Set breakpoint with condition
        bp = debugger.set_breakpoint("test.ml", 5)
        assert bp is not None
        bp.condition = "x > 10"

        # Create fake frame with x = 5
        class FakeFrame:
            f_locals = {"x": 5}
            f_globals = {}

        debugger.current_frame = FakeFrame()

        # Condition should evaluate to False
        assert debugger._evaluate_condition("x > 10") is False

        # Update x to 15
        FakeFrame.f_locals["x"] = 15

        # Condition should evaluate to True
        assert debugger._evaluate_condition("x > 10") is True

    def test_breakpoint_with_complex_condition(self):
        """Test breakpoint with complex boolean expression."""
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

        # Create fake frame
        class FakeFrame:
            f_locals = {"count": 5, "flag": True, "name": "test"}
            f_globals = {}

        debugger.current_frame = FakeFrame()

        # Test complex condition (using ML syntax: &&, ||, !)
        assert debugger._evaluate_condition("count > 3 && flag") is True
        assert debugger._evaluate_condition("count < 3 || name == 'test'") is True
        assert debugger._evaluate_condition("count == 5 && !flag") is False

    def test_condition_with_invalid_expression(self):
        """Test that invalid conditions don't crash the debugger."""
        source_map = EnhancedSourceMap()
        index = SourceMapIndex.from_source_map(source_map, "test.py")
        debugger = MLDebugger("test.ml", index, "")

        class FakeFrame:
            f_locals = {"x": 10}
            f_globals = {}

        debugger.current_frame = FakeFrame()

        # Invalid Python syntax - should return False
        assert debugger._evaluate_condition("x >>>  10") is False

        # Undefined variable - should return False
        assert debugger._evaluate_condition("undefined_var > 5") is False

    def test_condition_evaluation_in_should_break(self):
        """Test that conditions are evaluated during breakpoint checking."""
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

        # Set conditional breakpoint
        bp = debugger.set_breakpoint("test.ml", 5)
        bp.condition = "x == 42"

        # Create frame with x = 10
        class FakeFrame:
            f_locals = {"x": 10}
            f_globals = {}

        debugger.current_frame = FakeFrame()

        # Should NOT break (condition false)
        assert debugger._should_break("test.ml", 5, 10) is False

        # Update x to 42
        FakeFrame.f_locals["x"] = 42

        # Should break (condition true)
        assert debugger._should_break("test.ml", 5, 10) is True
        assert bp.hit_count == 1

    def test_unconditional_breakpoint_still_works(self):
        """Test that breakpoints without conditions still work."""
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

        # Set unconditional breakpoint
        bp = debugger.set_breakpoint("test.ml", 5)
        assert bp.condition is None

        # Should break regardless of frame state
        assert debugger._should_break("test.ml", 5, 10) is True
        assert bp.hit_count == 1

    def test_removing_condition_from_breakpoint(self):
        """Test that conditions can be removed from breakpoints."""
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

        # Set breakpoint with condition
        bp = debugger.set_breakpoint("test.ml", 5)
        bp.condition = "x > 10"

        # Remove condition
        bp.condition = None

        # Should break unconditionally
        assert debugger._should_break("test.ml", 5, 10) is True


class TestWatchExpressions:
    """Test watch expression functionality."""

    def test_add_watch(self):
        """Test adding a watch expression."""
        source_map = EnhancedSourceMap()
        index = SourceMapIndex.from_source_map(source_map, "test.py")
        debugger = MLDebugger("test.ml", index, "")

        # Add watch
        watch_id = debugger.add_watch("x")
        assert watch_id == 1
        assert 1 in debugger.watches
        assert debugger.watches[1] == "x"

        # Add another watch
        watch_id2 = debugger.add_watch("y + 10")
        assert watch_id2 == 2
        assert len(debugger.watches) == 2

    def test_remove_watch(self):
        """Test removing a watch expression."""
        source_map = EnhancedSourceMap()
        index = SourceMapIndex.from_source_map(source_map, "test.py")
        debugger = MLDebugger("test.ml", index, "")

        # Add watches
        watch_id1 = debugger.add_watch("x")
        watch_id2 = debugger.add_watch("y")

        # Remove first watch
        assert debugger.remove_watch(watch_id1) is True
        assert watch_id1 not in debugger.watches
        assert watch_id2 in debugger.watches

        # Try to remove non-existent watch
        assert debugger.remove_watch(999) is False

    def test_get_watch_values(self):
        """Test getting current values of watch expressions."""
        source_map = EnhancedSourceMap()
        index = SourceMapIndex.from_source_map(source_map, "test.py")
        debugger = MLDebugger("test.ml", index, "")

        # Create fake frame
        class FakeFrame:
            f_locals = {"x": 10, "y": 20}
            f_globals = {}

        debugger.current_frame = FakeFrame()

        # Add watches
        watch_id1 = debugger.add_watch("x")
        watch_id2 = debugger.add_watch("y * 2")

        # Get values
        watch_values = debugger.get_watch_values()

        assert len(watch_values) == 2
        assert watch_values[watch_id1] == ("x", 10, True)
        assert watch_values[watch_id2] == ("y * 2", 40, True)

    def test_watch_with_invalid_expression(self):
        """Test watch with invalid expression."""
        source_map = EnhancedSourceMap()
        index = SourceMapIndex.from_source_map(source_map, "test.py")
        debugger = MLDebugger("test.ml", index, "")

        class FakeFrame:
            f_locals = {"x": 10}
            f_globals = {}

        debugger.current_frame = FakeFrame()

        # Add watch with invalid syntax
        watch_id = debugger.add_watch("x >>>  10")

        # Get values - should not crash
        watch_values = debugger.get_watch_values()
        expression, value, success = watch_values[watch_id]

        assert success is False
        assert "<Error:" in str(value)

    def test_watch_with_undefined_variable(self):
        """Test watch with undefined variable."""
        source_map = EnhancedSourceMap()
        index = SourceMapIndex.from_source_map(source_map, "test.py")
        debugger = MLDebugger("test.ml", index, "")

        class FakeFrame:
            f_locals = {"x": 10}
            f_globals = {}

        debugger.current_frame = FakeFrame()

        # Add watch with undefined variable
        watch_id = debugger.add_watch("undefined_var")

        # Get values - should handle gracefully
        watch_values = debugger.get_watch_values()
        expression, value, success = watch_values[watch_id]

        assert success is False
        assert "Error" in str(value)


class TestEnhancedVariableFormatting:
    """Test enhanced variable formatting (placeholder for implementation)."""

    @pytest.mark.skip(reason="Enhanced formatting not yet implemented")
    def test_format_ml_object(self):
        """Test formatting ML object."""
        pass

    @pytest.mark.skip(reason="Enhanced formatting not yet implemented")
    def test_format_ml_array(self):
        """Test formatting ML array."""
        pass


class TestExceptionBreakpoints:
    """Test exception breakpoints (placeholder for implementation)."""

    @pytest.mark.skip(reason="Exception breakpoints not yet implemented")
    def test_break_on_exception(self):
        """Test breaking when exception is raised."""
        pass


class TestEnhancedCallStack:
    """Test enhanced call stack navigation (placeholder for implementation)."""

    @pytest.mark.skip(reason="Enhanced call stack not yet implemented")
    def test_navigate_call_stack(self):
        """Test navigating up and down call stack."""
        pass
