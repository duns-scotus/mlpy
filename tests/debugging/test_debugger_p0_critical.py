"""
Phase 1 (P0) Critical Debugger Tests

These tests validate the core debugger functionality that must work:
- Basic breakpoint operations
- Step over/into/out
- Variable inspection (local variables)
- Call stack management
- Source map ML→Python mapping
- Error handling (graceful failures)
"""

import os
import sys
from pathlib import Path

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from tests.debugging.debug_test_handler import DebugTestHandler, DebugState


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def handler():
    """Provide a clean DebugTestHandler instance."""
    return DebugTestHandler()


@pytest.fixture
def main_ml_file():
    """Path to main test ML file."""
    return "tests/ml_integration/ml_debug/main.ml"


@pytest.fixture
def loaded_handler(handler, main_ml_file):
    """Provide a handler with main.ml already loaded."""
    success, message = handler.load_program(main_ml_file)
    assert success, f"Failed to load program: {message}"
    return handler


# ============================================================================
# 1. Basic Breakpoint Operations (P0)
# ============================================================================

class TestBasicBreakpoints:
    """Test basic breakpoint operations."""

    def test_set_breakpoint_valid_line(self, loaded_handler):
        """Set breakpoint at valid line."""
        bp_id, is_pending = loaded_handler.set_breakpoint("main.ml", 170)

        assert bp_id > 0, f"Failed to set breakpoint: got bp_id={bp_id}"
        assert isinstance(is_pending, bool), "is_pending should be boolean"
        assert len(loaded_handler.breakpoints) == 1

    def test_set_multiple_breakpoints_same_file(self, loaded_handler):
        """Set multiple breakpoints in same file."""
        lines = [170, 200, 251]  # Changed from 250 (comment) to 251 (executable line)

        for line in lines:
            bp_id, is_pending = loaded_handler.set_breakpoint("main.ml", line)
            assert bp_id > 0, f"Failed to set breakpoint at line {line}"

        assert len(loaded_handler.breakpoints) == 3

    def test_remove_breakpoint(self, loaded_handler):
        """Remove breakpoint by ID."""
        # Set breakpoint
        bp_id, is_pending = loaded_handler.set_breakpoint("main.ml", 170)
        assert bp_id > 0

        bp_ids = list(loaded_handler.breakpoints.keys())
        assert len(bp_ids) == 1

        # Remove breakpoint
        success, message = loaded_handler.remove_breakpoint(bp_ids[0])
        assert success, f"Failed to remove breakpoint: {message}"
        assert len(loaded_handler.breakpoints) == 0

    def test_remove_nonexistent_breakpoint(self, loaded_handler):
        """Remove non-existent breakpoint should fail gracefully."""
        success, message = loaded_handler.remove_breakpoint(999)

        assert not success
        assert "not found" in message.lower()

    def test_set_breakpoint_without_loading_program(self, handler):
        """Set breakpoint without loading program should fail."""
        bp_id, is_pending = handler.set_breakpoint("main.ml", 100)

        assert bp_id == -1, "Should return -1 for bp_id when no program loaded"
        assert is_pending == False, "Should return False for is_pending when no program loaded"


# ============================================================================
# 2. Source Map Functionality (P0)
# ============================================================================

class TestSourceMaps:
    """Test source map functionality."""

    def test_source_map_generated(self, loaded_handler):
        """Verify source map is generated."""
        all_exist, status = loaded_handler.verify_source_maps_exist()

        assert all_exist, f"Missing source maps: {status}"
        assert status['ml_file'] is True
        assert status['py_file'] is True
        assert status['map_file'] is True
        assert status['source_map_index'] is True

    def test_source_map_ml_to_python_mapping(self, loaded_handler):
        """Test ML line to Python line mapping."""
        # Get source map index
        assert loaded_handler.source_map_index is not None

        # Test mapping for known line
        ml_file = loaded_handler.ml_file
        ml_line = 170  # Known line in test_arithmetic function

        py_line = loaded_handler.source_map_index.ml_line_to_first_py_line(ml_file, ml_line)

        # Should map to some Python line (not None)
        assert py_line is not None
        assert isinstance(py_line, int)
        assert py_line > 0

    def test_source_map_caching(self, handler, main_ml_file):
        """Test that source maps are cached and reused."""
        from pathlib import Path

        # First load
        success1, _ = handler.load_program(main_ml_file, force_retranspile=False)
        assert success1

        ml_path = Path(main_ml_file)
        map_path = ml_path.with_suffix('.py.map')

        # Get modification time
        mtime1 = map_path.stat().st_mtime if map_path.exists() else 0
        assert mtime1 > 0, "Source map file not created"

        # Second load (should use cache)
        handler2 = DebugTestHandler()
        success2, _ = handler2.load_program(main_ml_file, force_retranspile=False)
        assert success2

        # Modification time should be unchanged (cached)
        mtime2 = map_path.stat().st_mtime
        assert mtime1 == mtime2, "Source map was regenerated instead of using cache"

    def test_load_program_force_retranspile(self, handler, main_ml_file):
        """Test force retranspile option."""
        from pathlib import Path
        import time

        # First load
        success1, _ = handler.load_program(main_ml_file, force_retranspile=True)
        assert success1

        ml_path = Path(main_ml_file)
        map_path = ml_path.with_suffix('.py.map')
        mtime1 = map_path.stat().st_mtime

        # Wait to ensure different timestamp
        time.sleep(0.1)

        # Force retranspile
        handler2 = DebugTestHandler()
        success2, _ = handler2.load_program(main_ml_file, force_retranspile=True)
        assert success2

        mtime2 = map_path.stat().st_mtime

        # Modification time should be different (regenerated)
        assert mtime2 > mtime1, "Source map was not regenerated"


# ============================================================================
# 3. Variable Inspection (P0)
# ============================================================================

class TestVariableInspection:
    """Test variable inspection functionality."""

    def test_get_variables_initial_state(self, loaded_handler):
        """Get variables when no program running."""
        variables = loaded_handler.get_variables()

        # Should return empty dict or minimal variables
        assert isinstance(variables, dict)

    def test_get_call_stack_initial_state(self, loaded_handler):
        """Get call stack when no program running."""
        stack = loaded_handler.get_call_stack()

        # Should return empty list
        assert isinstance(stack, list)
        assert len(stack) == 0


# ============================================================================
# 4. Debug State Management (P0)
# ============================================================================

class TestDebugState:
    """Test debug state management."""

    def test_initial_state(self, handler):
        """Test initial debugger state."""
        state = handler.get_state()

        assert isinstance(state, DebugState)
        assert state.stopped is False
        assert state.current_file is None
        assert state.current_line is None
        assert len(state.call_stack) == 0

    def test_reset_handler(self, loaded_handler):
        """Test resetting handler state."""
        # Set some state
        loaded_handler.set_breakpoint("main.ml", 170)

        # Reset
        loaded_handler.reset()

        # State should be clean
        assert loaded_handler.debugger is None
        assert loaded_handler.ml_file is None
        assert len(loaded_handler.breakpoints) == 0

    def test_continue_execution_without_program(self, handler):
        """Continue execution without program loaded should fail."""
        success, message = handler.continue_execution()

        assert not success
        assert "no program loaded" in message.lower()

    def test_step_over_without_program(self, handler):
        """Step over without program loaded should fail."""
        success, message = handler.step_over()

        assert not success
        assert "no program loaded" in message.lower()

    def test_step_into_without_program(self, handler):
        """Step into without program loaded should fail."""
        success, message = handler.step_into()

        assert not success
        assert "no program loaded" in message.lower()

    def test_step_out_without_program(self, handler):
        """Step out without program loaded should fail."""
        success, message = handler.step_out()

        assert not success
        assert "no program loaded" in message.lower()


# ============================================================================
# 5. Error Handling and Edge Cases (P0)
# ============================================================================

class TestErrorHandling:
    """Test error handling and graceful failures."""

    def test_load_nonexistent_file(self, handler):
        """Load non-existent file should fail gracefully."""
        success, message = handler.load_program("nonexistent_file.ml")

        assert not success
        assert "not found" in message.lower()

    def test_load_invalid_ml_file(self, handler, tmp_path):
        """Load invalid ML file should fail gracefully."""
        # Create invalid ML file
        invalid_file = tmp_path / "invalid.ml"
        invalid_file.write_text("this is not valid ML code $$$ !!!")

        success, message = handler.load_program(str(invalid_file))

        assert not success
        assert "failed" in message.lower()

    def test_set_breakpoint_with_relative_path(self, loaded_handler):
        """Set breakpoint with relative file path."""
        # Should work with just filename
        bp_id, is_pending = loaded_handler.set_breakpoint("main.ml", 170)

        assert bp_id > 0, f"Failed with relative path: got bp_id={bp_id}"

    def test_evaluate_expression_without_program(self, handler):
        """Evaluate expression without program loaded should fail."""
        success, result = handler.evaluate_expression("x + 5")

        assert not success
        assert "no program loaded" in str(result).lower()

    def test_get_variables_invalid_frame(self, loaded_handler):
        """Get variables with invalid frame index."""
        variables = loaded_handler.get_variables(frame_index=999)

        # Should return empty dict gracefully
        assert isinstance(variables, dict)


# ============================================================================
# 6. Multi-File Support (P0)
# ============================================================================

class TestMultiFileSupport:
    """Test debugging with multiple files."""

    def test_load_different_files_sequentially(self, handler):
        """Load different ML files sequentially."""
        test_files = [
            "tests/ml_integration/ml_debug/main.ml",
            "tests/ml_integration/ml_debug/math_utils.ml",
            "tests/ml_integration/ml_debug/data_structures/list_ops.ml",
        ]

        for ml_file in test_files:
            handler.reset()
            success, message = handler.load_program(ml_file)

            assert success, f"Failed to load {ml_file}: {message}"

            # Verify source maps
            all_exist, status = handler.verify_source_maps_exist()
            assert all_exist, f"Missing source maps for {ml_file}: {status}"

    def test_load_file_in_subdirectory(self, handler):
        """Load ML file in subdirectory."""
        ml_file = "tests/ml_integration/ml_debug/data_structures/tree.ml"

        success, message = handler.load_program(ml_file)

        assert success, f"Failed to load file in subdirectory: {message}"

        # Should handle nested directory structure
        all_exist, status = handler.verify_source_maps_exist()
        assert all_exist


# ============================================================================
# 7. DebugTestHandler API (P0)
# ============================================================================

class TestDebugTestHandlerAPI:
    """Test DebugTestHandler API functionality."""

    def test_handler_instantiation(self):
        """Test creating DebugTestHandler instance."""
        handler = DebugTestHandler()

        assert handler is not None
        assert handler.debugger is None
        assert handler.ml_file is None
        assert len(handler.breakpoints) == 0

    def test_load_program_returns_tuple(self, handler, main_ml_file):
        """Load program should return (success, message) tuple."""
        result = handler.load_program(main_ml_file)

        assert isinstance(result, tuple)
        assert len(result) == 2
        success, message = result
        assert isinstance(success, bool)
        assert isinstance(message, str)

    def test_set_breakpoint_returns_tuple(self, loaded_handler):
        """Set breakpoint should return (bp_id, is_pending) tuple."""
        result = loaded_handler.set_breakpoint("main.ml", 170)

        assert isinstance(result, tuple)
        assert len(result) == 2
        bp_id, is_pending = result
        assert isinstance(bp_id, int)
        assert isinstance(is_pending, bool)
        assert bp_id > 0

    def test_verify_source_maps_returns_tuple(self, loaded_handler):
        """Verify source maps should return (all_exist, status) tuple."""
        result = loaded_handler.verify_source_maps_exist()

        assert isinstance(result, tuple)
        assert len(result) == 2
        all_exist, status = result
        assert isinstance(all_exist, bool)
        assert isinstance(status, dict)

    def test_get_state_returns_debug_state(self, handler):
        """Get state should return DebugState object."""
        state = handler.get_state()

        assert isinstance(state, DebugState)
        assert hasattr(state, 'stopped')
        assert hasattr(state, 'current_file')
        assert hasattr(state, 'current_line')
        assert hasattr(state, 'call_stack')
        assert hasattr(state, 'variables')


# ============================================================================
# 8. Integration Tests (P0)
# ============================================================================

class TestDebuggerIntegration:
    """Integration tests for complete debugging workflows."""

    def test_complete_load_breakpoint_workflow(self, handler, main_ml_file):
        """Test complete workflow: load → set breakpoint → verify."""
        # Load program
        success, message = handler.load_program(main_ml_file)
        assert success, f"Load failed: {message}"

        # Set breakpoint
        bp_id, is_pending = handler.set_breakpoint("main.ml", 170)
        assert bp_id > 0, f"Set breakpoint failed: got bp_id={bp_id}"

        # Verify source maps
        all_exist, status = handler.verify_source_maps_exist()
        assert all_exist, f"Source maps missing: {status}"

        # Verify breakpoint was set
        assert len(handler.breakpoints) == 1

    def test_multiple_files_with_breakpoints(self, handler):
        """Test loading multiple files and setting breakpoints in each."""
        files_and_lines = [
            ("tests/ml_integration/ml_debug/main.ml", 170),
            ("tests/ml_integration/ml_debug/math_utils.ml", 6),  # Line 6: return -x; statement
        ]

        for ml_file, line in files_and_lines:
            handler.reset()

            # Load file with force_retranspile to ensure fresh source maps
            success, _ = handler.load_program(ml_file, force_retranspile=True)
            assert success

            # Set breakpoint using basename for proper source map resolution
            bp_id, is_pending = handler.set_breakpoint(os.path.basename(ml_file), line)
            assert bp_id > 0, f"Failed to set breakpoint at {ml_file}:{line}"

            # Verify
            assert len(handler.breakpoints) == 1


# ============================================================================
# 9. Performance Tests (P0)
# ============================================================================

class TestDebuggerPerformance:
    """Basic performance tests for debugger."""

    def test_load_program_performance(self, handler, main_ml_file):
        """Test that loading program is reasonably fast."""
        import time

        start = time.time()
        success, _ = handler.load_program(main_ml_file)
        elapsed = time.time() - start

        assert success
        # Should load in under 5 seconds (includes transpilation)
        assert elapsed < 5.0, f"Load took {elapsed:.2f}s, expected < 5.0s"

    def test_set_breakpoint_performance(self, loaded_handler):
        """Test that setting breakpoints is fast."""
        import time

        # Use lines that are definitely executable (skip line 174 which is blank)
        lines = [169, 170, 171, 172, 173, 175, 176, 177, 178, 179]

        start = time.time()
        for line in lines:
            bp_id, is_pending = loaded_handler.set_breakpoint("main.ml", line)
            assert bp_id > 0, f"Failed to set breakpoint at line {line}"
        elapsed = time.time() - start

        # Should set 10 breakpoints in under 1 second
        assert elapsed < 1.0, f"Setting 10 breakpoints took {elapsed:.2f}s"

    def test_source_map_lookup_performance(self, loaded_handler):
        """Test that source map lookups are fast."""
        import time

        ml_file = loaded_handler.ml_file

        start = time.time()
        for _ in range(1000):
            loaded_handler.source_map_index.ml_line_to_first_py_line(ml_file, 170)
        elapsed = time.time() - start

        # 1000 lookups should take under 500ms (relaxed from 100ms for cross-platform compatibility)
        assert elapsed < 0.5, f"1000 source map lookups took {elapsed:.3f}s"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
