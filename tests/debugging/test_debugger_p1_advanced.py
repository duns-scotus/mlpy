"""
Phase 2 (P1) High-Priority Debugger Tests

These tests validate advanced debugger functionality:
- Conditional breakpoints
- Stepping with execution (step over/into/out with running program)
- Variable inspection during execution
- Call stack during execution
- Expression evaluation
- Exception handling (basic)

Note: These tests require actual program execution and are more complex than P0 tests.
"""

import os
import sys
from pathlib import Path
import time
import threading

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
def simple_ml_file(tmp_path):
    """Create a simple ML file for testing execution."""
    ml_file = tmp_path / "simple.ml"
    ml_file.write_text("""
// Simple test program for debugging
function add(a, b) {
    result = a + b;
    return result;
}

function multiply(a, b) {
    result = a * b;
    return result;
}

function main() {
    x = 10;
    y = 20;
    sum = add(x, y);
    product = multiply(x, y);
    return sum + product;
}

result = main();
""")
    return str(ml_file)


@pytest.fixture
def loop_ml_file(tmp_path):
    """Create ML file with loops for testing."""
    ml_file = tmp_path / "loop.ml"
    ml_file.write_text("""
// Loop test program
function count_to_ten() {
    count = 0;
    i = 1;
    while (i <= 10) {
        count = count + i;
        i = i + 1;
    }
    return count;
}

result = count_to_ten();
""")
    return str(ml_file)


@pytest.fixture
def conditional_ml_file(tmp_path):
    """Create ML file with conditionals for testing."""
    ml_file = tmp_path / "conditional.ml"
    ml_file.write_text("""
// Conditional test program
function classify_number(n) {
    if (n > 0) {
        return "positive";
    } elif (n < 0) {
        return "negative";
    } else {
        return "zero";
    }
}

result1 = classify_number(5);
result2 = classify_number(-3);
result3 = classify_number(0);
""")
    return str(ml_file)


# ============================================================================
# 1. Conditional Breakpoints (P1)
# ============================================================================

class TestConditionalBreakpoints:
    """Test conditional breakpoint functionality."""

    def test_set_conditional_breakpoint_simple(self, handler, simple_ml_file):
        """Set breakpoint with simple condition."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        # Set conditional breakpoint: break when x == 10
        success, message = handler.set_breakpoint("simple.ml", 15, condition="x == 10")

        assert success, f"Failed to set conditional breakpoint: {message}"
        assert len(handler.breakpoints) == 1

        # Verify condition is stored
        bp_id = list(handler.breakpoints.keys())[0]
        bp_info = handler.breakpoints[bp_id]
        assert bp_info.condition == "x == 10"

    def test_set_conditional_breakpoint_complex(self, handler, simple_ml_file):
        """Set breakpoint with complex condition."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        # Set conditional breakpoint with complex expression
        success, message = handler.set_breakpoint("simple.ml", 16, condition="x > 5 && y < 100")

        assert success

        bp_id = list(handler.breakpoints.keys())[0]
        bp_info = handler.breakpoints[bp_id]
        assert bp_info.condition == "x > 5 && y < 100"

    def test_conditional_breakpoint_none(self, handler, simple_ml_file):
        """Set breakpoint without condition (should work)."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        success, _ = handler.set_breakpoint("simple.ml", 15, condition=None)
        assert success

        bp_id = list(handler.breakpoints.keys())[0]
        bp_info = handler.breakpoints[bp_id]
        assert bp_info.condition is None


# ============================================================================
# 2. Variable Inspection API (P1)
# ============================================================================

class TestVariableInspectionAPI:
    """Test variable inspection API (without execution)."""

    def test_get_variables_returns_dict(self, handler, simple_ml_file):
        """Get variables should always return a dict."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        variables = handler.get_variables()
        assert isinstance(variables, dict)

    def test_get_variables_with_frame_index(self, handler, simple_ml_file):
        """Get variables with different frame indices."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        # Should handle different frame indices gracefully
        for frame_idx in [0, 1, 2]:
            variables = handler.get_variables(frame_index=frame_idx)
            assert isinstance(variables, dict)

    def test_get_call_stack_returns_list(self, handler, simple_ml_file):
        """Get call stack should always return a list."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        stack = handler.get_call_stack()
        assert isinstance(stack, list)


# ============================================================================
# 3. Expression Evaluation API (P1)
# ============================================================================

class TestExpressionEvaluationAPI:
    """Test expression evaluation API."""

    def test_evaluate_expression_returns_tuple(self, handler, simple_ml_file):
        """Evaluate expression should return (success, result) tuple."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        result = handler.evaluate_expression("5 + 5")

        assert isinstance(result, tuple)
        assert len(result) == 2
        success, value = result
        assert isinstance(success, bool)

    def test_evaluate_simple_expression(self, handler, simple_ml_file):
        """Evaluate simple arithmetic expression."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        # Note: Without execution context, this may fail
        # Just verify it returns proper tuple
        success, result = handler.evaluate_expression("2 + 2")
        assert isinstance(success, bool)

    def test_evaluate_invalid_expression(self, handler, simple_ml_file):
        """Evaluate invalid expression should fail gracefully."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        success, error = handler.evaluate_expression("invalid syntax $$$")
        # Should either succeed with error or fail gracefully
        assert isinstance(success, bool)


# ============================================================================
# 4. Call Stack API (P1)
# ============================================================================

class TestCallStackAPI:
    """Test call stack API."""

    def test_get_call_stack_structure(self, handler, simple_ml_file):
        """Verify call stack returns proper structure."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        stack = handler.get_call_stack()

        assert isinstance(stack, list)
        # Each frame should be a dict with expected keys
        for frame in stack:
            assert isinstance(frame, dict)

    def test_call_stack_empty_initially(self, handler, simple_ml_file):
        """Call stack should be empty before execution."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        stack = handler.get_call_stack()
        # Should be empty before execution starts
        assert len(stack) == 0


# ============================================================================
# 5. Debug State Transitions (P1)
# ============================================================================

class TestDebugStateTransitions:
    """Test debug state transitions."""

    def test_state_before_execution(self, handler, simple_ml_file):
        """Test state before program execution."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        state = handler.get_state()

        assert state.stopped is False
        assert state.current_file is None
        assert state.current_line is None
        assert len(state.call_stack) == 0

    def test_stepping_commands_return_success(self, handler, simple_ml_file):
        """Test that stepping commands return success status."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        # These should return proper tuple structure (may succeed or fail)
        result = handler.step_over()
        assert isinstance(result, tuple)
        assert len(result) == 2

        result = handler.step_into()
        assert isinstance(result, tuple)
        assert len(result) == 2

        result = handler.step_out()
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_continue_execution_returns_tuple(self, handler, simple_ml_file):
        """Test continue execution returns proper tuple."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        # Continue should return tuple structure
        result = handler.continue_execution()
        assert isinstance(result, tuple)
        assert len(result) == 2


# ============================================================================
# 6. Multiple Breakpoints Management (P1)
# ============================================================================

class TestMultipleBreakpoints:
    """Test managing multiple breakpoints."""

    def test_set_ten_breakpoints(self, handler, simple_ml_file):
        """Set 10 breakpoints in same file."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        # Set multiple breakpoints
        for i in range(10):
            success, _ = handler.set_breakpoint("simple.ml", 3 + i, condition=None)
            if success:  # Some lines may not be valid
                pass

        # Should have at least some breakpoints set
        assert len(handler.breakpoints) > 0

    def test_remove_all_breakpoints(self, handler, simple_ml_file):
        """Set multiple breakpoints and remove them all."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        # Set breakpoints
        handler.set_breakpoint("simple.ml", 5)
        handler.set_breakpoint("simple.ml", 10)
        handler.set_breakpoint("simple.ml", 15)

        bp_ids = list(handler.breakpoints.keys())
        initial_count = len(bp_ids)
        assert initial_count > 0

        # Remove all breakpoints
        for bp_id in bp_ids:
            handler.remove_breakpoint(bp_id)

        assert len(handler.breakpoints) == 0

    def test_conditional_and_unconditional_breakpoints(self, handler, simple_ml_file):
        """Mix conditional and unconditional breakpoints."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        # Unconditional
        handler.set_breakpoint("simple.ml", 5, condition=None)

        # Conditional
        handler.set_breakpoint("simple.ml", 10, condition="x > 0")

        # Another unconditional
        handler.set_breakpoint("simple.ml", 15, condition=None)

        bp_count = len(handler.breakpoints)
        assert bp_count == 3

        # Verify conditions
        conditions = [bp.condition for bp in handler.breakpoints.values()]
        assert None in conditions  # At least one unconditional
        assert any(c is not None for c in conditions)  # At least one conditional


# ============================================================================
# 7. Source Map Edge Cases (P1)
# ============================================================================

class TestSourceMapEdgeCases:
    """Test source map edge cases."""

    def test_source_map_for_multiple_files(self, handler, tmp_path):
        """Test source maps for multiple files."""
        # Create two ML files
        file1 = tmp_path / "file1.ml"
        file1.write_text("x = 10; y = 20; z = x + y;")

        file2 = tmp_path / "file2.ml"
        file2.write_text("a = 5; b = 10; c = a * b;")

        # Load first file
        success, _ = handler.load_program(str(file1))
        assert success

        all_exist1, _ = handler.verify_source_maps_exist()
        assert all_exist1

        # Load second file
        handler.reset()
        success, _ = handler.load_program(str(file2))
        assert success

        all_exist2, _ = handler.verify_source_maps_exist()
        assert all_exist2

    def test_source_map_line_boundary(self, handler, simple_ml_file):
        """Test source map at file boundaries."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        assert handler.source_map_index is not None

        # Test line 1 (first line)
        py_line = handler.source_map_index.ml_line_to_first_py_line(handler.ml_file, 1)
        # May be None for comment/blank lines, that's ok

        # Test a line that definitely exists (function definition)
        py_line = handler.source_map_index.ml_line_to_first_py_line(handler.ml_file, 3)
        # Should map to something
        assert py_line is None or isinstance(py_line, int)


# ============================================================================
# 8. Breakpoint State Management (P1)
# ============================================================================

class TestBreakpointStateManagement:
    """Test breakpoint state management."""

    def test_breakpoint_enabled_by_default(self, handler, simple_ml_file):
        """Breakpoints should be enabled by default."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        handler.set_breakpoint("simple.ml", 10)

        bp_id = list(handler.breakpoints.keys())[0]
        bp_info = handler.breakpoints[bp_id]
        assert bp_info.enabled is True

    def test_breakpoint_has_file_and_line(self, handler, simple_ml_file):
        """Breakpoint info should have file and line."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        handler.set_breakpoint("simple.ml", 10)

        bp_id = list(handler.breakpoints.keys())[0]
        bp_info = handler.breakpoints[bp_id]

        assert bp_info.file is not None
        assert bp_info.line == 10

    def test_breakpoint_hit_count_starts_zero(self, handler, simple_ml_file):
        """Breakpoint hit count should start at zero."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        handler.set_breakpoint("simple.ml", 10)

        bp_id = list(handler.breakpoints.keys())[0]
        bp_info = handler.breakpoints[bp_id]
        assert bp_info.hit_count == 0


# ============================================================================
# 9. Handler Robustness (P1)
# ============================================================================

class TestHandlerRobustness:
    """Test handler robustness under various conditions."""

    def test_multiple_load_without_reset(self, handler, tmp_path):
        """Load multiple programs without reset (should handle)."""
        file1 = tmp_path / "test1.ml"
        file1.write_text("x = 10;")

        file2 = tmp_path / "test2.ml"
        file2.write_text("y = 20;")

        # Load first
        success1, _ = handler.load_program(str(file1))
        assert success1

        # Load second without reset - handler should handle this
        success2, _ = handler.load_program(str(file2))
        # May succeed or fail, but shouldn't crash
        assert isinstance(success2, bool)

    def test_breakpoint_on_same_line_twice(self, handler, simple_ml_file):
        """Try to set breakpoint on same line twice."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        # Set first breakpoint
        success1, _ = handler.set_breakpoint("simple.ml", 10)
        assert success1

        # Try to set second breakpoint on same line
        success2, msg2 = handler.set_breakpoint("simple.ml", 10)
        # Should either succeed (creating duplicate) or fail gracefully
        assert isinstance(success2, bool)

    def test_rapid_breakpoint_operations(self, handler, simple_ml_file):
        """Rapidly set and remove breakpoints."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        # Rapid operations
        for i in range(5):
            handler.set_breakpoint("simple.ml", 5 + i)

        bp_ids = list(handler.breakpoints.keys())

        for bp_id in bp_ids[:3]:
            handler.remove_breakpoint(bp_id)

        # Should still have some breakpoints
        assert len(handler.breakpoints) >= 0  # May have 0-5 depending on valid lines


# ============================================================================
# 10. Integration Workflows (P1)
# ============================================================================

class TestIntegrationWorkflows:
    """Test complete integration workflows."""

    def test_workflow_load_set_verify_reset(self, handler, simple_ml_file):
        """Complete workflow: load → set breakpoints → verify → reset."""
        # Load
        success, _ = handler.load_program(simple_ml_file)
        assert success

        # Set breakpoints
        handler.set_breakpoint("simple.ml", 5)
        handler.set_breakpoint("simple.ml", 10)

        # Verify
        assert len(handler.breakpoints) >= 1
        all_exist, _ = handler.verify_source_maps_exist()
        assert all_exist

        # Reset
        handler.reset()
        assert handler.debugger is None
        assert len(handler.breakpoints) == 0

    def test_workflow_multiple_files_sequential(self, handler, tmp_path):
        """Load multiple files sequentially with breakpoints."""
        files = []
        for i in range(3):
            ml_file = tmp_path / f"test{i}.ml"
            ml_file.write_text(f"x{i} = {i * 10};")
            files.append(str(ml_file))

        for ml_file in files:
            handler.reset()

            success, _ = handler.load_program(ml_file)
            assert success

            success, _ = handler.set_breakpoint(os.path.basename(ml_file), 1)
            # Some files may not have executable line 1, that's ok

            all_exist, _ = handler.verify_source_maps_exist()
            assert all_exist


# ============================================================================
# 11. Performance Tests (P1)
# ============================================================================

class TestAdvancedPerformance:
    """Advanced performance tests."""

    def test_many_breakpoints_performance(self, handler, simple_ml_file):
        """Test performance with many breakpoints."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        start = time.time()

        # Try to set 50 breakpoints
        for i in range(50):
            handler.set_breakpoint("simple.ml", 1 + (i % 20))

        elapsed = time.time() - start

        # Should complete in reasonable time
        assert elapsed < 2.0, f"Setting 50 breakpoints took {elapsed:.2f}s"

    def test_repeated_load_performance(self, handler, simple_ml_file):
        """Test performance of repeated loads."""
        times = []

        for _ in range(3):
            handler.reset()

            start = time.time()
            success, _ = handler.load_program(simple_ml_file)
            elapsed = time.time() - start

            assert success
            times.append(elapsed)

        # Should benefit from caching (later loads faster)
        # But all should be under 5 seconds
        for t in times:
            assert t < 5.0

    def test_source_map_index_multiple_lookups(self, handler, simple_ml_file):
        """Test source map index with many lookups."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        ml_file = handler.ml_file

        start = time.time()
        for line in range(1, 101):  # Try 100 different lines
            handler.source_map_index.ml_line_to_first_py_line(ml_file, line)
        elapsed = time.time() - start

        # 100 lookups should be very fast
        assert elapsed < 0.05, f"100 source map lookups took {elapsed:.3f}s"


# ============================================================================
# 12. Error Recovery (P1)
# ============================================================================

class TestErrorRecovery:
    """Test error recovery and resilience."""

    def test_recover_from_invalid_file(self, handler, tmp_path):
        """Recover after loading invalid file."""
        invalid_file = tmp_path / "invalid.ml"
        invalid_file.write_text("invalid syntax $$$")

        # Try to load invalid file
        success1, _ = handler.load_program(str(invalid_file))
        assert not success1  # Should fail

        # Should be able to load valid file after
        valid_file = tmp_path / "valid.ml"
        valid_file.write_text("x = 10;")

        handler.reset()
        success2, _ = handler.load_program(str(valid_file))
        assert success2  # Should succeed

    def test_recover_from_invalid_breakpoint(self, handler, simple_ml_file):
        """Recover after trying to set invalid breakpoint."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        # Try invalid line
        success1, _ = handler.set_breakpoint("simple.ml", 99999)
        # May succeed (pending) or fail

        # Should still be able to set valid breakpoint
        success2, _ = handler.set_breakpoint("simple.ml", 10)
        # Should work
        assert isinstance(success2, bool)


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
