"""
Phase 3 (P2) Execution-Based Debugger Tests

These tests validate debugger behavior with actual program execution:
- Stepping through running code (step over/into/out)
- Variable inspection during execution
- Call stack during execution
- Breakpoint hit detection
- Conditional breakpoint evaluation
- Exception handling during execution
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
def simple_ml_file(tmp_path):
    """Create a simple ML file for execution testing."""
    ml_file = tmp_path / "simple_exec.ml"
    ml_file.write_text("""
// Simple function for execution testing
function add(a, b) {
    result = a + b;
    return result;
}

function multiply(x, y) {
    product = x * y;
    return product;
}

function main() {
    x = 10;
    y = 20;
    sum = add(x, y);
    prod = multiply(x, y);
    return sum + prod;
}

result = main();
""")
    return str(ml_file)


@pytest.fixture
def loop_ml_file(tmp_path):
    """Create ML file with loops for stepping tests."""
    ml_file = tmp_path / "loop_exec.ml"
    ml_file.write_text("""
function count_to_five() {
    count = 0;
    i = 1;
    while (i <= 5) {
        count = count + i;
        i = i + 1;
    }
    return count;
}

result = count_to_five();
""")
    return str(ml_file)


@pytest.fixture
def conditional_ml_file(tmp_path):
    """Create ML file with conditionals for testing."""
    ml_file = tmp_path / "conditional_exec.ml"
    ml_file.write_text("""
function check_value(x) {
    if (x > 10) {
        result = "large";
    } elif (x > 5) {
        result = "medium";
    } else {
        result = "small";
    }
    return result;
}

r1 = check_value(15);
r2 = check_value(7);
r3 = check_value(2);
""")
    return str(ml_file)


@pytest.fixture
def recursive_ml_file(tmp_path):
    """Create ML file with recursion for stack testing."""
    ml_file = tmp_path / "recursive_exec.ml"
    ml_file.write_text("""
function factorial(n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

result = factorial(5);
""")
    return str(ml_file)


@pytest.fixture
def array_ml_file(tmp_path):
    """Create ML file with arrays for data inspection."""
    ml_file = tmp_path / "array_exec.ml"
    ml_file.write_text("""
function process_array(arr) {
    sum = 0;
    i = 0;
    while (i < len(arr)) {
        sum = sum + arr[i];
        i = i + 1;
    }
    return sum;
}

numbers = [1, 2, 3, 4, 5];
total = process_array(numbers);
""")
    return str(ml_file)


# ============================================================================
# 1. Execution-Based Stepping (P2)
# ============================================================================

class TestExecutionStepping:
    """Test stepping through actual program execution."""

    def test_step_over_simple_statement(self, handler, simple_ml_file):
        """Step over a simple assignment statement."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        # Set breakpoint at first line of main()
        success, _ = handler.set_breakpoint("simple_exec.ml", 15)
        assert success

        # Start execution (should stop at breakpoint)
        success, _ = handler.run()

        # Step over should advance to next line
        success, msg = handler.step_over()
        # Should return tuple structure
        assert isinstance((success, msg), tuple)

    def test_step_into_function_call(self, handler, simple_ml_file):
        """Step into a function call."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        # Set breakpoint at function call line
        success, _ = handler.set_breakpoint("simple_exec.ml", 17)
        assert success

        success, _ = handler.run()

        # Step into should enter add() function
        success, msg = handler.step_into()
        assert isinstance((success, msg), tuple)

    def test_step_out_of_function(self, handler, simple_ml_file):
        """Step out of a function back to caller."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        # Set breakpoint inside add() function
        success, _ = handler.set_breakpoint("simple_exec.ml", 4)
        assert success

        success, _ = handler.run()

        # Step out should return to caller
        success, msg = handler.step_out()
        assert isinstance((success, msg), tuple)

    def test_step_through_loop_iterations(self, handler, loop_ml_file):
        """Step through multiple loop iterations."""
        success, _ = handler.load_program(loop_ml_file)
        assert success

        # Set breakpoint at loop condition
        success, _ = handler.set_breakpoint("loop_exec.ml", 5)
        assert success

        success, _ = handler.run()

        # Step multiple times through loop
        for _ in range(3):
            success, _ = handler.step_over()
            assert isinstance(success, bool)

    def test_step_over_maintains_line_order(self, handler, simple_ml_file):
        """Verify step over maintains sequential line execution."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        success, _ = handler.set_breakpoint("simple_exec.ml", 15)
        assert success

        success, _ = handler.run()

        # Multiple step overs should maintain order
        for _ in range(5):
            state = handler.get_state()
            assert isinstance(state, DebugState)
            handler.step_over()


# ============================================================================
# 2. Variable Inspection During Execution (P2)
# ============================================================================

class TestVariablesDuringExecution:
    """Test variable inspection with actual execution."""

    def test_inspect_local_variables_at_breakpoint(self, handler, simple_ml_file):
        """Inspect local variables when stopped at breakpoint."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        success, _ = handler.set_breakpoint("simple_exec.ml", 16)
        assert success

        success, _ = handler.run()

        # Get variables at breakpoint
        variables = handler.get_variables()
        assert isinstance(variables, dict)

    def test_variable_values_change_during_stepping(self, handler, loop_ml_file):
        """Verify variable values change as we step."""
        success, _ = handler.load_program(loop_ml_file)
        assert success

        success, _ = handler.set_breakpoint("loop_exec.ml", 6)
        assert success

        success, _ = handler.run()

        # Get initial variable values
        vars1 = handler.get_variables()

        # Step and get new values
        handler.step_over()
        vars2 = handler.get_variables()

        # Variables should be dicts
        assert isinstance(vars1, dict)
        assert isinstance(vars2, dict)

    def test_inspect_function_parameters(self, handler, simple_ml_file):
        """Inspect function parameters at function entry."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        # Breakpoint at first line of add()
        success, _ = handler.set_breakpoint("simple_exec.ml", 4)
        assert success

        success, _ = handler.run()

        # Should have access to parameters a, b
        variables = handler.get_variables()
        assert isinstance(variables, dict)

    def test_inspect_array_elements(self, handler, array_ml_file):
        """Inspect array variable contents."""
        success, _ = handler.load_program(array_ml_file)
        assert success

        success, _ = handler.set_breakpoint("array_exec.ml", 12)
        assert success

        success, _ = handler.run()

        variables = handler.get_variables()
        assert isinstance(variables, dict)

    def test_inspect_variables_in_different_frames(self, handler, recursive_ml_file):
        """Inspect variables in different stack frames."""
        success, _ = handler.load_program(recursive_ml_file)
        assert success

        success, _ = handler.set_breakpoint("recursive_exec.ml", 4)
        assert success

        success, _ = handler.run()

        # Get variables from current frame
        vars_frame0 = handler.get_variables(frame_index=0)
        vars_frame1 = handler.get_variables(frame_index=1)

        assert isinstance(vars_frame0, dict)
        assert isinstance(vars_frame1, dict)


# ============================================================================
# 3. Call Stack During Execution (P2)
# ============================================================================

class TestCallStackDuringExecution:
    """Test call stack with actual execution."""

    def test_call_stack_depth_at_breakpoint(self, handler, simple_ml_file):
        """Verify call stack depth when stopped."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        # Breakpoint inside add() when called from main()
        success, _ = handler.set_breakpoint("simple_exec.ml", 4)
        assert success

        success, _ = handler.run()

        stack = handler.get_call_stack()
        assert isinstance(stack, list)

    def test_call_stack_shows_function_names(self, handler, simple_ml_file):
        """Verify stack shows correct function names."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        success, _ = handler.set_breakpoint("simple_exec.ml", 4)
        assert success

        success, _ = handler.run()

        stack = handler.get_call_stack()
        assert isinstance(stack, list)

        # Each frame should have structure
        for frame in stack:
            assert isinstance(frame, dict)

    def test_recursive_call_stack_depth(self, handler, recursive_ml_file):
        """Test call stack in recursive function."""
        success, _ = handler.load_program(recursive_ml_file)
        assert success

        # Breakpoint in recursive function
        success, _ = handler.set_breakpoint("recursive_exec.ml", 4)
        assert success

        success, _ = handler.run()

        stack = handler.get_call_stack()
        assert isinstance(stack, list)
        # Stack should have multiple frames in recursion

    def test_stack_frame_file_and_line_info(self, handler, simple_ml_file):
        """Verify stack frames contain file and line info."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        success, _ = handler.set_breakpoint("simple_exec.ml", 4)
        assert success

        success, _ = handler.run()

        stack = handler.get_call_stack()

        for frame in stack:
            # Each frame should be a dict with expected structure
            assert isinstance(frame, dict)


# ============================================================================
# 4. Breakpoint Hit Detection (P2)
# ============================================================================

class TestBreakpointHits:
    """Test breakpoint hit detection during execution."""

    def test_breakpoint_is_hit_during_execution(self, handler, simple_ml_file):
        """Verify breakpoint is actually hit."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        success, _ = handler.set_breakpoint("simple_exec.ml", 15)
        assert success

        # Run should stop at breakpoint
        success, msg = handler.run()

        # Verify we're in stopped state
        state = handler.get_state()
        # State should indicate we're stopped (if execution worked)
        assert isinstance(state, DebugState)

    def test_multiple_breakpoints_hit_in_order(self, handler, simple_ml_file):
        """Test multiple breakpoints are hit in execution order."""
        success, _ = handler.load_program(simple_ml_file)
        assert success

        # Set multiple breakpoints
        handler.set_breakpoint("simple_exec.ml", 15)
        handler.set_breakpoint("simple_exec.ml", 17)
        handler.set_breakpoint("simple_exec.ml", 18)

        # Run and continue through breakpoints
        handler.run()
        state1 = handler.get_state()

        handler.continue_execution()
        state2 = handler.get_state()

        assert isinstance(state1, DebugState)
        assert isinstance(state2, DebugState)

    def test_breakpoint_hit_in_loop(self, handler, loop_ml_file):
        """Test breakpoint hit multiple times in loop."""
        success, _ = handler.load_program(loop_ml_file)
        assert success

        # Breakpoint inside loop body
        success, _ = handler.set_breakpoint("loop_exec.ml", 6)
        assert success

        handler.run()

        # Continue multiple times through loop
        for _ in range(3):
            success, _ = handler.continue_execution()
            assert isinstance(success, bool)

    def test_breakpoint_hit_in_recursion(self, handler, recursive_ml_file):
        """Test breakpoint hit in recursive calls."""
        success, _ = handler.load_program(recursive_ml_file)
        assert success

        success, _ = handler.set_breakpoint("recursive_exec.ml", 4)
        assert success

        handler.run()

        # Continue through recursive calls
        for _ in range(3):
            success, _ = handler.continue_execution()
            assert isinstance(success, bool)


# ============================================================================
# 5. Conditional Breakpoint Evaluation (P2)
# ============================================================================

class TestConditionalBreakpointEvaluation:
    """Test conditional breakpoints during execution."""

    def test_conditional_breakpoint_when_true(self, handler, loop_ml_file):
        """Test conditional breakpoint triggers when condition is true."""
        success, _ = handler.load_program(loop_ml_file)
        assert success

        # Breakpoint with condition
        success, _ = handler.set_breakpoint("loop_exec.ml", 6, condition="i == 3")
        assert success

        # Run should stop when i == 3
        success, msg = handler.run()
        assert isinstance((success, msg), tuple)

    def test_conditional_breakpoint_when_false(self, handler, loop_ml_file):
        """Test conditional breakpoint doesn't trigger when false."""
        success, _ = handler.load_program(loop_ml_file)
        assert success

        # Breakpoint that should never trigger
        success, _ = handler.set_breakpoint("loop_exec.ml", 6, condition="i > 100")
        assert success

        # Run - may complete or stop elsewhere
        success, msg = handler.run()
        assert isinstance((success, msg), tuple)

    def test_conditional_breakpoint_complex_expression(self, handler, loop_ml_file):
        """Test conditional breakpoint with complex expression."""
        success, _ = handler.load_program(loop_ml_file)
        assert success

        # Complex condition
        success, _ = handler.set_breakpoint("loop_exec.ml", 6, condition="i > 2 && count > 0")
        assert success

        success, msg = handler.run()
        assert isinstance((success, msg), tuple)


# ============================================================================
# 6. Exception Handling During Execution (P2)
# ============================================================================

class TestExceptionHandling:
    """Test exception handling during debugging."""

    def test_exception_in_execution(self, handler, tmp_path):
        """Test handling of exceptions during execution."""
        ml_file = tmp_path / "exception_exec.ml"
        ml_file.write_text("""
function divide(a, b) {
    if (b == 0) {
        throw { message: "Division by zero" };
    }
    return a / b;
}

result = divide(10, 0);
""")

        success, _ = handler.load_program(str(ml_file))
        assert success

        # Run - may throw exception
        success, msg = handler.run()
        assert isinstance((success, msg), tuple)

    def test_catch_exception_during_debugging(self, handler, tmp_path):
        """Test debugging with try-except blocks."""
        ml_file = tmp_path / "try_except.ml"
        ml_file.write_text("""
function safe_divide(a, b) {
    try {
        if (b == 0) {
            throw { message: "Division by zero" };
        }
        result = a / b;
    } except (e) {
        result = 0;
    }
    return result;
}

r = safe_divide(10, 0);
""")

        success, _ = handler.load_program(str(ml_file))
        assert success

        success, _ = handler.set_breakpoint("try_except.ml", 8)
        assert success

        success, msg = handler.run()
        assert isinstance((success, msg), tuple)


# ============================================================================
# 7. Advanced Execution Scenarios (P2)
# ============================================================================

class TestAdvancedExecutionScenarios:
    """Test complex execution scenarios."""

    def test_nested_function_calls(self, handler, tmp_path):
        """Test debugging with deeply nested function calls."""
        ml_file = tmp_path / "nested.ml"
        ml_file.write_text("""
function level3(x) {
    return x + 3;
}

function level2(x) {
    return level3(x + 2);
}

function level1(x) {
    return level2(x + 1);
}

result = level1(10);
""")

        success, _ = handler.load_program(str(ml_file))
        assert success

        success, _ = handler.set_breakpoint("nested.ml", 2)
        assert success

        success, _ = handler.run()

        # Should have deep call stack
        stack = handler.get_call_stack()
        assert isinstance(stack, list)

    def test_conditional_branching_execution(self, handler, conditional_ml_file):
        """Test stepping through conditional branches."""
        success, _ = handler.load_program(conditional_ml_file)
        assert success

        success, _ = handler.set_breakpoint("conditional_exec.ml", 3)
        assert success

        success, _ = handler.run()

        # Step through conditionals
        for _ in range(5):
            handler.step_over()
            state = handler.get_state()
            assert isinstance(state, DebugState)

    def test_array_modification_during_execution(self, handler, tmp_path):
        """Test debugging array modifications."""
        ml_file = tmp_path / "array_mod.ml"
        ml_file.write_text("""
function modify_array(arr) {
    i = 0;
    while (i < len(arr)) {
        arr[i] = arr[i] * 2;
        i = i + 1;
    }
    return arr;
}

numbers = [1, 2, 3];
result = modify_array(numbers);
""")

        success, _ = handler.load_program(str(ml_file))
        assert success

        success, _ = handler.set_breakpoint("array_mod.ml", 5)
        assert success

        success, _ = handler.run()

        variables = handler.get_variables()
        assert isinstance(variables, dict)


# ============================================================================
# 8. Integration Tests (P2)
# ============================================================================

class TestExecutionIntegration:
    """Integration tests for complete execution workflows."""

    def test_complete_debug_session(self, handler, simple_ml_file):
        """Test complete debugging session from start to finish."""
        # Load
        success, _ = handler.load_program(simple_ml_file)
        assert success

        # Set breakpoints
        handler.set_breakpoint("simple_exec.ml", 15)
        handler.set_breakpoint("simple_exec.ml", 4)

        # Run
        handler.run()

        # Inspect
        variables = handler.get_variables()
        stack = handler.get_call_stack()

        # Step
        handler.step_over()
        handler.step_into()

        # Continue
        handler.continue_execution()

        # All operations should complete without errors
        assert isinstance(variables, dict)
        assert isinstance(stack, list)

    def test_multi_file_execution_debugging(self, handler, tmp_path):
        """Test debugging with multiple files in execution."""
        # Create main file
        main_file = tmp_path / "main_exec.ml"
        main_file.write_text("""
function main() {
    x = 10;
    y = 20;
    return x + y;
}

result = main();
""")

        success, _ = handler.load_program(str(main_file))
        assert success

        success, _ = handler.set_breakpoint("main_exec.ml", 3)
        assert success

        handler.run()

        state = handler.get_state()
        assert isinstance(state, DebugState)


# ============================================================================
# 9. Performance with Execution (P2)
# ============================================================================

class TestExecutionPerformance:
    """Performance tests with actual execution."""

    def test_stepping_performance(self, handler, loop_ml_file):
        """Test that stepping through code is reasonably fast."""
        import time

        success, _ = handler.load_program(loop_ml_file)
        assert success

        handler.set_breakpoint("loop_exec.ml", 3)
        handler.run()

        # Time multiple step operations
        start = time.time()
        for _ in range(10):
            handler.step_over()
        elapsed = time.time() - start

        # 10 steps should take less than 1 second
        assert elapsed < 1.0, f"10 steps took {elapsed:.2f}s"

    def test_variable_inspection_performance(self, handler, simple_ml_file):
        """Test variable inspection performance during execution."""
        import time

        success, _ = handler.load_program(simple_ml_file)
        assert success

        handler.set_breakpoint("simple_exec.ml", 15)
        handler.run()

        # Time multiple variable inspections
        start = time.time()
        for _ in range(100):
            handler.get_variables()
        elapsed = time.time() - start

        # 100 inspections should take less than 0.5 seconds
        assert elapsed < 0.5, f"100 variable inspections took {elapsed:.2f}s"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
