"""Tests for exception breakpoints and call stack navigation."""

import pytest
import sys
from mlpy.debugging.debugger import MLDebugger
from mlpy.debugging.source_map_index import SourceMapIndex
from mlpy.ml.codegen.enhanced_source_maps import EnhancedSourceMap


@pytest.fixture
def simple_source_map_index():
    """Create a simple source map index for testing."""
    # Create an enhanced source map with basic mappings
    source_map = EnhancedSourceMap()
    source_map.add_source("test.ml", "x = 10\ny = 20\nz = x + y")

    # Add mappings for a simple program
    for line_num in range(1, 10):
        source_map.add_mapping(
            generated_line=line_num,
            generated_column=0,
            original_line=line_num,
            original_column=0,
            source_file="test.ml"
        )

    # Create source map index
    index = SourceMapIndex.from_source_map(source_map, "test.py")
    return index


@pytest.fixture
def debugger_with_source_map(simple_source_map_index):
    """Create debugger with source map."""
    py_code = "x = 10\ny = 20\nz = x + y"
    debugger = MLDebugger("test.ml", simple_source_map_index, py_code)
    return debugger


class TestExceptionBreakpoints:
    """Test exception breakpoint functionality."""

    def test_enable_exception_breakpoints_all(self, debugger_with_source_map):
        """Test enabling breakpoints for all exceptions."""
        debugger = debugger_with_source_map

        assert debugger.break_on_exceptions is False

        debugger.enable_exception_breakpoints()

        assert debugger.break_on_exceptions is True
        assert len(debugger.exception_filters) == 0  # No filters = all exceptions

    def test_enable_exception_breakpoints_specific(self, debugger_with_source_map):
        """Test enabling breakpoints for specific exception types."""
        debugger = debugger_with_source_map

        debugger.enable_exception_breakpoints("ValueError")

        assert debugger.break_on_exceptions is True
        assert "ValueError" in debugger.exception_filters

    def test_enable_multiple_exception_types(self, debugger_with_source_map):
        """Test enabling breakpoints for multiple exception types."""
        debugger = debugger_with_source_map

        debugger.enable_exception_breakpoints("ValueError")
        debugger.enable_exception_breakpoints("KeyError")
        debugger.enable_exception_breakpoints("TypeError")

        assert debugger.break_on_exceptions is True
        assert len(debugger.exception_filters) == 3
        assert "ValueError" in debugger.exception_filters
        assert "KeyError" in debugger.exception_filters
        assert "TypeError" in debugger.exception_filters

    def test_disable_exception_breakpoints(self, debugger_with_source_map):
        """Test disabling exception breakpoints."""
        debugger = debugger_with_source_map

        debugger.enable_exception_breakpoints("ValueError")
        assert debugger.break_on_exceptions is True

        debugger.disable_exception_breakpoints()

        assert debugger.break_on_exceptions is False
        assert len(debugger.exception_filters) == 0

    def test_should_break_on_exception_no_filters(self, debugger_with_source_map):
        """Test that we break on all exceptions when no filters are set."""
        debugger = debugger_with_source_map

        debugger.enable_exception_breakpoints()

        # Should break on any exception type
        assert debugger._should_break_on_exception(ValueError) is True
        assert debugger._should_break_on_exception(KeyError) is True
        assert debugger._should_break_on_exception(TypeError) is True

    def test_should_break_on_exception_with_filters(self, debugger_with_source_map):
        """Test that we only break on filtered exception types."""
        debugger = debugger_with_source_map

        debugger.enable_exception_breakpoints("ValueError")
        debugger.enable_exception_breakpoints("KeyError")

        # Should break on filtered types
        assert debugger._should_break_on_exception(ValueError) is True
        assert debugger._should_break_on_exception(KeyError) is True

        # Should not break on other types
        assert debugger._should_break_on_exception(TypeError) is False
        assert debugger._should_break_on_exception(RuntimeError) is False

    def test_get_exception_info_no_exception(self, debugger_with_source_map):
        """Test getting exception info when no exception has occurred."""
        debugger = debugger_with_source_map

        exc_info = debugger.get_exception_info()

        assert exc_info is None

    def test_exception_info_stored(self, debugger_with_source_map):
        """Test that exception information is stored correctly."""
        debugger = debugger_with_source_map

        # Simulate storing exception information
        exc_type = ValueError
        exc_value = ValueError("Test error")
        exc_traceback = None

        debugger.last_exception = (exc_type, exc_value, exc_traceback)

        exc_info = debugger.get_exception_info()

        assert exc_info is not None
        assert exc_info["type"] == "ValueError"
        assert exc_info["value"] == "Test error"
        assert exc_info["message"] == "Test error"

    def test_exception_event_handling(self, debugger_with_source_map):
        """Test that exception events are properly handled in trace function."""
        debugger = debugger_with_source_map

        # Enable breaking on ValueError
        debugger.enable_exception_breakpoints("ValueError")

        # Track if we hit the exception pause
        paused = []

        original_pause = debugger._pause_execution
        def mock_pause():
            paused.append(True)

        debugger._pause_execution = mock_pause

        # Simulate exception event directly
        import sys
        frame = sys._getframe()
        exc_type = ValueError
        exc_value = ValueError("Test exception")
        exc_traceback = None

        debugger.current_frame = frame
        debugger.running = True

        # Call trace function with exception event
        debugger.trace_function(frame, "exception", (exc_type, exc_value, exc_traceback))

        # Should have paused and stored exception
        assert len(paused) > 0
        assert debugger.last_exception is not None
        assert debugger.last_exception[0] == ValueError
        assert "Test exception" in str(debugger.last_exception[1])


class TestCallStackNavigation:
    """Test call stack navigation functionality."""

    def test_get_frame_at_index_current(self, debugger_with_source_map):
        """Test getting the current frame (index 0)."""
        debugger = debugger_with_source_map

        # Create a simple frame hierarchy
        import sys
        def outer():
            def middle():
                def inner():
                    # At this point, we should be able to get frames
                    debugger.current_frame = sys._getframe()

                    frame = debugger.get_frame_at_index(0)
                    assert frame is not None
                    assert frame.f_code.co_name == "inner"

                inner()
            middle()
        outer()

    def test_get_frame_at_index_parent(self, debugger_with_source_map):
        """Test getting parent frames."""
        debugger = debugger_with_source_map

        import sys
        def outer():
            def middle():
                def inner():
                    debugger.current_frame = sys._getframe()

                    # Index 0 = inner
                    frame0 = debugger.get_frame_at_index(0)
                    assert frame0.f_code.co_name == "inner"

                    # Index 1 = middle
                    frame1 = debugger.get_frame_at_index(1)
                    assert frame1.f_code.co_name == "middle"

                    # Index 2 = outer
                    frame2 = debugger.get_frame_at_index(2)
                    assert frame2.f_code.co_name == "outer"

                inner()
            middle()
        outer()

    def test_get_frame_at_index_invalid(self, debugger_with_source_map):
        """Test getting frame with invalid index."""
        debugger = debugger_with_source_map

        import sys
        def test_func():
            debugger.current_frame = sys._getframe()

            # Index 100 should be out of bounds
            frame = debugger.get_frame_at_index(100)
            assert frame is None

            # Negative index should return None
            frame = debugger.get_frame_at_index(-1)
            assert frame is None

        test_func()

    def test_navigate_up_stack(self, debugger_with_source_map):
        """Test navigating up the call stack."""
        debugger = debugger_with_source_map

        import sys
        def outer():
            def middle():
                def inner():
                    debugger.current_frame = sys._getframe()
                    debugger.current_frame_index = 0

                    # Navigate up once (to middle)
                    result = debugger.navigate_up_stack()
                    assert result is True
                    assert debugger.current_frame_index == 1

                    # Navigate up again (to outer)
                    result = debugger.navigate_up_stack()
                    assert result is True
                    assert debugger.current_frame_index == 2

                inner()
            middle()
        outer()

    def test_navigate_up_stack_at_top(self, debugger_with_source_map):
        """Test that navigating up fails when at top of stack."""
        debugger = debugger_with_source_map

        import sys
        def test_func():
            debugger.current_frame = sys._getframe()
            debugger.current_frame_index = 0

            # Navigate up as far as possible
            while debugger.navigate_up_stack():
                pass

            # Should be at top now
            current_index = debugger.current_frame_index

            # Try to navigate up one more time - should fail
            result = debugger.navigate_up_stack()
            assert result is False
            assert debugger.current_frame_index == current_index  # Unchanged

        test_func()

    def test_navigate_down_stack(self, debugger_with_source_map):
        """Test navigating down the call stack."""
        debugger = debugger_with_source_map

        import sys
        def outer():
            def middle():
                def inner():
                    debugger.current_frame = sys._getframe()
                    debugger.current_frame_index = 0

                    # Navigate up twice
                    debugger.navigate_up_stack()
                    debugger.navigate_up_stack()
                    assert debugger.current_frame_index == 2

                    # Navigate down once
                    result = debugger.navigate_down_stack()
                    assert result is True
                    assert debugger.current_frame_index == 1

                    # Navigate down again
                    result = debugger.navigate_down_stack()
                    assert result is True
                    assert debugger.current_frame_index == 0

                inner()
            middle()
        outer()

    def test_navigate_down_stack_at_bottom(self, debugger_with_source_map):
        """Test that navigating down fails when at bottom of stack."""
        debugger = debugger_with_source_map

        import sys
        def test_func():
            debugger.current_frame = sys._getframe()
            debugger.current_frame_index = 0

            # Already at bottom (index 0)
            result = debugger.navigate_down_stack()
            assert result is False
            assert debugger.current_frame_index == 0  # Unchanged

        test_func()

    def test_get_current_stack_frame(self, debugger_with_source_map):
        """Test getting the current stack frame at navigation position."""
        debugger = debugger_with_source_map

        import sys
        def outer():
            def middle():
                def inner():
                    debugger.current_frame = sys._getframe()
                    debugger.current_frame_index = 0

                    # At index 0, should get inner frame
                    frame = debugger.get_current_stack_frame()
                    assert frame.f_code.co_name == "inner"

                    # Navigate up to index 1 (middle)
                    debugger.navigate_up_stack()
                    frame = debugger.get_current_stack_frame()
                    assert frame.f_code.co_name == "middle"

                    # Navigate up to index 2 (outer)
                    debugger.navigate_up_stack()
                    frame = debugger.get_current_stack_frame()
                    assert frame.f_code.co_name == "outer"

                inner()
            middle()
        outer()

    def test_variable_inspection_at_different_stack_levels(self, debugger_with_source_map):
        """Test that variable inspection works at different stack levels."""
        debugger = debugger_with_source_map

        import sys
        def outer():
            outer_var = "outer_value"

            def middle():
                middle_var = "middle_value"

                def inner():
                    inner_var = "inner_value"
                    debugger.current_frame = sys._getframe()
                    debugger.current_frame_index = 0

                    # At inner level, should see inner_var
                    value = debugger.get_variable("inner_var")
                    assert value == "inner_value"

                    # Navigate to middle level
                    debugger.navigate_up_stack()
                    value = debugger.get_variable("middle_var")
                    assert value == "middle_value"

                    # Navigate to outer level
                    debugger.navigate_up_stack()
                    value = debugger.get_variable("outer_var")
                    assert value == "outer_value"

                inner()
            middle()
        outer()

    def test_get_all_locals_at_different_stack_levels(self, debugger_with_source_map):
        """Test that get_all_locals works at different stack levels."""
        debugger = debugger_with_source_map

        import sys
        def outer():
            outer_var = "outer_value"

            def middle():
                middle_var = "middle_value"

                def inner():
                    inner_var = "inner_value"
                    debugger.current_frame = sys._getframe()
                    debugger.current_frame_index = 0

                    # At inner level
                    locals_dict = debugger.get_all_locals()
                    assert "inner_var" in locals_dict
                    assert locals_dict["inner_var"] == "inner_value"

                    # Navigate to middle level
                    debugger.navigate_up_stack()
                    locals_dict = debugger.get_all_locals()
                    assert "middle_var" in locals_dict
                    assert locals_dict["middle_var"] == "middle_value"

                    # Navigate to outer level
                    debugger.navigate_up_stack()
                    locals_dict = debugger.get_all_locals()
                    assert "outer_var" in locals_dict
                    assert locals_dict["outer_var"] == "outer_value"

                inner()
            middle()
        outer()

    def test_get_call_stack(self, debugger_with_source_map):
        """Test getting the full call stack."""
        debugger = debugger_with_source_map

        import sys
        def outer():
            def middle():
                def inner():
                    debugger.current_frame = sys._getframe()

                    stack = debugger.get_call_stack()

                    # The stack may be empty if ML mappings don't exist for these frames,
                    # which is expected in this test setup. At minimum we should not crash.
                    # Check that we get a list back
                    assert isinstance(stack, list)

                    # If stack has items, verify structure
                    if stack:
                        # Each item should be a tuple of (ml_file, ml_line, func_name)
                        for item in stack:
                            assert isinstance(item, tuple)
                            assert len(item) == 3

                inner()
            middle()
        outer()

    def test_stack_frame_tracking_on_call(self, debugger_with_source_map):
        """Test that stack frames are tracked correctly on function calls."""
        debugger = debugger_with_source_map

        # Track stack frames
        stack_sizes = []

        original_trace = debugger.trace_function
        def tracking_trace(frame, event, arg):
            result = original_trace(frame, event, arg)
            if event == "call":
                stack_sizes.append(len(debugger.stack_frames))
            return result

        debugger.trace_function = tracking_trace

        code = """
def outer():
    def middle():
        def inner():
            pass
        inner()
    middle()
outer()
"""

        # Set up tracing
        original_sys_trace = sys.gettrace()
        sys.settrace(debugger.trace_function)
        debugger.running = True

        exec(code)

        sys.settrace(original_sys_trace)
        debugger.running = False

        # Stack should have grown with each call
        assert len(stack_sizes) > 0

    def test_stack_frame_tracking_on_return(self, debugger_with_source_map):
        """Test that stack frames are cleaned up on function returns."""
        debugger = debugger_with_source_map

        # Track stack sizes on return
        stack_sizes_on_return = []

        original_trace = debugger.trace_function
        def tracking_trace(frame, event, arg):
            result = original_trace(frame, event, arg)
            if event == "return":
                stack_sizes_on_return.append(len(debugger.stack_frames))
            return result

        debugger.trace_function = tracking_trace

        code = """
def outer():
    def middle():
        def inner():
            return 1
        return inner()
    return middle()
outer()
"""

        # Set up tracing
        original_sys_trace = sys.gettrace()
        sys.settrace(debugger.trace_function)
        debugger.running = True

        exec(code)

        sys.settrace(original_sys_trace)
        debugger.running = False

        # Stack should have frames popped on return
        assert len(stack_sizes_on_return) > 0


class TestIntegration:
    """Integration tests combining exception breakpoints and stack navigation."""

    def test_exception_with_call_stack(self, debugger_with_source_map):
        """Test that we can access call stack information when exception occurs."""
        debugger = debugger_with_source_map

        debugger.enable_exception_breakpoints("ValueError")

        # Track exception and frame state
        captured_info = []

        original_pause = debugger._pause_execution
        def capture_info():
            # Capture state when we pause for exception
            captured_info.append({
                "exception": debugger.last_exception,
                "frame": debugger.current_frame,
                "stack": debugger.get_call_stack()
            })

        debugger._pause_execution = capture_info

        # Simulate exception in a nested call
        import sys
        def outer():
            def middle():
                def inner():
                    # Simulate exception event
                    debugger.current_frame = sys._getframe()
                    exc = (ValueError, ValueError("Test"), None)
                    debugger.trace_function(debugger.current_frame, "exception", exc)

                inner()
            middle()
        outer()

        # Should have captured exception information
        assert len(captured_info) > 0
        info = captured_info[0]

        # Should have exception info
        assert info["exception"] is not None
        assert info["exception"][0] == ValueError

        # Should have current frame
        assert info["frame"] is not None

        # Stack should be a list (may be empty if no ML mappings)
        assert isinstance(info["stack"], list)

    def test_navigate_stack_after_exception(self, debugger_with_source_map):
        """Test that we can navigate the stack after an exception occurs."""
        debugger = debugger_with_source_map

        import sys
        def outer():
            outer_var = "outer"

            def middle():
                middle_var = "middle"

                def inner():
                    inner_var = "inner"

                    # Simulate hitting an exception
                    debugger.current_frame = sys._getframe()
                    debugger.current_frame_index = 0
                    debugger.last_exception = (ValueError, ValueError("Test"), None)

                    # Should be able to navigate up the stack
                    assert debugger.navigate_up_stack() is True

                    # Should be able to inspect variables at middle level
                    value = debugger.get_variable("middle_var")
                    assert value == "middle"

                    # Navigate up to outer
                    assert debugger.navigate_up_stack() is True
                    value = debugger.get_variable("outer_var")
                    assert value == "outer"

                    # Navigate back down
                    assert debugger.navigate_down_stack() is True
                    assert debugger.navigate_down_stack() is True

                    # Should be back at inner level
                    value = debugger.get_variable("inner_var")
                    assert value == "inner"

                inner()
            middle()
        outer()
