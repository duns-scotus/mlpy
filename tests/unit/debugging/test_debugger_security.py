"""Security tests for debugger expression evaluation.

These tests verify that the debugger maintains sandbox security even when
evaluating conditions and watch expressions.
"""

import pytest
from mlpy.debugging.safe_expression_eval import SafeExpressionEvaluator
from mlpy.debugging.debugger import MLDebugger
from mlpy.debugging.source_map_index import SourceMapIndex
from mlpy.ml.codegen.enhanced_source_maps import EnhancedSourceMap, SourceMapping, SourceLocation


class TestSafeExpressionEvaluator:
    """Test the safe expression evaluator prevents security violations."""

    def test_simple_safe_expression(self):
        """Test that safe expressions work correctly."""
        evaluator = SafeExpressionEvaluator()

        local_vars = {"x": 10, "y": 20}
        global_vars = {}

        # Simple arithmetic
        value, success, error = evaluator.evaluate("x + y", local_vars, global_vars)
        assert success is True
        assert value == 30
        assert error == ""

    def test_comparison_expression(self):
        """Test comparison expressions."""
        evaluator = SafeExpressionEvaluator()

        local_vars = {"x": 10}
        global_vars = {}

        value, success, error = evaluator.evaluate("x > 5", local_vars, global_vars)
        assert success is True
        assert value is True

    def test_blocks_import(self):
        """Test that __import__ is blocked."""
        evaluator = SafeExpressionEvaluator()

        local_vars = {}
        global_vars = {}

        # Try to import os module
        value, success, error = evaluator.evaluate(
            "__import__('os').system('echo pwned')",
            local_vars,
            global_vars
        )

        # Should fail due to security violation
        assert success is False
        assert "error" in error.lower() or "security" in error.lower()

    def test_blocks_eval(self):
        """Test that eval is blocked."""
        evaluator = SafeExpressionEvaluator()

        local_vars = {}
        global_vars = {}

        # Try to use eval
        value, success, error = evaluator.evaluate(
            "eval('1+1')",
            local_vars,
            global_vars
        )

        # Should fail - eval not in safe builtins
        assert success is False

    def test_blocks_exec(self):
        """Test that exec is blocked."""
        evaluator = SafeExpressionEvaluator()

        local_vars = {}
        global_vars = {}

        # Try to use exec
        value, success, error = evaluator.evaluate(
            "exec('print(1)')",
            local_vars,
            global_vars
        )

        # Should fail - exec not in safe builtins
        assert success is False

    def test_blocks_open(self):
        """Test that open (file access) is blocked."""
        evaluator = SafeExpressionEvaluator()

        local_vars = {}
        global_vars = {}

        # Try to open a file
        value, success, error = evaluator.evaluate(
            "open('/etc/passwd').read()",
            local_vars,
            global_vars
        )

        # Should fail - open not in safe builtins
        assert success is False

    def test_blocks_dangerous_builtins(self):
        """Test that dangerous builtins are not available."""
        evaluator = SafeExpressionEvaluator()

        local_vars = {}
        global_vars = {}

        dangerous_funcs = [
            "compile('1+1', '<string>', 'eval')",
            "globals()",
            "locals()",
            "vars()",
            "__import__('sys')",
        ]

        for dangerous_expr in dangerous_funcs:
            value, success, error = evaluator.evaluate(
                dangerous_expr,
                local_vars,
                global_vars
            )
            assert success is False, f"Should block: {dangerous_expr}"

    def test_allows_safe_builtins(self):
        """Test that safe builtins are available."""
        evaluator = SafeExpressionEvaluator()

        local_vars = {"items": [1, 2, 3]}
        global_vars = {}

        safe_expressions = [
            ("len(items)", 3),
            ("max(items)", 3),
            ("min(items)", 1),
            ("sum(items)", 6),
            ("abs(-5)", 5),
            ("int('10')", 10),
            ("str(42)", "42"),
        ]

        for expr, expected in safe_expressions:
            value, success, error = evaluator.evaluate(expr, local_vars, global_vars)
            assert success is True, f"Should allow safe builtin: {expr}, error: {error}"
            assert value == expected

    def test_array_access(self):
        """Test that array access works."""
        evaluator = SafeExpressionEvaluator()

        local_vars = {"arr": [10, 20, 30]}
        global_vars = {}

        value, success, error = evaluator.evaluate("arr[1]", local_vars, global_vars)
        assert success is True
        assert value == 20

    def test_object_access(self):
        """Test that object/dict access works."""
        evaluator = SafeExpressionEvaluator()

        local_vars = {"obj": {"name": "test", "count": 42}}
        global_vars = {}

        value, success, error = evaluator.evaluate("obj['count']", local_vars, global_vars)
        assert success is True
        assert value == 42

    def test_invalid_syntax(self):
        """Test that invalid syntax is caught."""
        evaluator = SafeExpressionEvaluator()

        local_vars = {}
        global_vars = {}

        value, success, error = evaluator.evaluate("x >>> 10", local_vars, global_vars)
        assert success is False
        assert "error" in error.lower()


class TestDebuggerConditionSecurity:
    """Test that debugger conditions maintain security."""

    def test_conditional_breakpoint_blocks_import(self):
        """Test that conditional breakpoints can't import modules."""
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

        # Set breakpoint with malicious condition
        bp = debugger.set_breakpoint("test.ml", 5)
        bp.condition = "__import__('os').system('rm -rf /')"

        # Create frame
        class FakeFrame:
            f_locals = {}
            f_globals = {}

        debugger.current_frame = FakeFrame()

        # Try to evaluate condition - should fail securely
        result = debugger._evaluate_condition(bp.condition)

        # Should return False (don't break) and not execute the malicious code
        assert result is False

    def test_conditional_breakpoint_safe_expression(self):
        """Test that safe conditional expressions work."""
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
        bp.condition = "x > 10"

        class FakeFrame:
            f_locals = {"x": 15}
            f_globals = {}

        debugger.current_frame = FakeFrame()

        # Should evaluate safely
        result = debugger._evaluate_condition(bp.condition)
        assert result is True


class TestDebuggerWatchSecurity:
    """Test that watch expressions maintain security."""

    def test_watch_blocks_import(self):
        """Test that watch expressions can't import modules."""
        source_map = EnhancedSourceMap()
        index = SourceMapIndex.from_source_map(source_map, "test.py")
        debugger = MLDebugger("test.ml", index, "")

        class FakeFrame:
            f_locals = {}
            f_globals = {}

        debugger.current_frame = FakeFrame()

        # Add malicious watch
        watch_id = debugger.add_watch("__import__('sys').exit(0)")

        # Get watch values - should fail securely
        watch_values = debugger.get_watch_values()

        expression, value, success = watch_values[watch_id]
        assert success is False
        assert "Error" in str(value)

    def test_watch_safe_expression(self):
        """Test that safe watch expressions work."""
        source_map = EnhancedSourceMap()
        index = SourceMapIndex.from_source_map(source_map, "test.py")
        debugger = MLDebugger("test.ml", index, "")

        class FakeFrame:
            f_locals = {"x": 10, "y": 20}
            f_globals = {}

        debugger.current_frame = FakeFrame()

        # Add safe watch
        watch_id = debugger.add_watch("x + y")

        # Should evaluate safely
        watch_values = debugger.get_watch_values()

        expression, value, success = watch_values[watch_id]
        assert success is True
        assert value == 30
