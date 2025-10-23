"""Unit tests for AsyncMLExecutor.

Tests async ML execution with thread pool, timeout handling,
error propagation, and security integration.
"""

import pytest
import asyncio
import time
from mlpy.integration import AsyncMLExecutor, AsyncMLResult, async_ml_execute


class TestAsyncMLResult:
    """Test AsyncMLResult dataclass."""

    def test_success_result(self):
        """Test creating a successful result."""
        result = AsyncMLResult(
            success=True,
            value=42,
            execution_time=0.5,
            transpile_time=0.1
        )

        assert result.success is True
        assert result.value == 42
        assert result.error is None
        assert result.execution_time == 0.5
        assert result.transpile_time == 0.1

    def test_error_result(self):
        """Test creating an error result."""
        result = AsyncMLResult(
            success=False,
            error="Test error",
            execution_time=0.3
        )

        assert result.success is False
        assert result.value is None
        assert result.error == "Test error"
        assert result.execution_time == 0.3


class TestAsyncMLExecutor:
    """Test AsyncMLExecutor class."""

    @pytest.fixture
    def executor(self):
        """Create test executor."""
        executor = AsyncMLExecutor(max_workers=2, strict_security=False)
        yield executor
        executor.shutdown()

    @pytest.mark.asyncio
    async def test_simple_execution(self, executor):
        """Test simple async ML execution."""
        result = await executor.execute('result = 2 + 2;')

        assert result.success is True
        assert result.value == 4
        assert result.error is None
        assert result.execution_time > 0
        assert result.transpile_time > 0

    @pytest.mark.asyncio
    async def test_execution_with_context(self, executor):
        """Test execution with context variables."""
        context = {'x': 10, 'y': 5}
        result = await executor.execute('result = x + y;', context=context)

        assert result.success is True
        assert result.value == 15

    @pytest.mark.asyncio
    async def test_execution_timeout(self, executor):
        """Test execution with timeout."""
        # This should timeout (simulate slow operation)
        ml_code = '''
i = 0;
while (i < 10000000) {
    i = i + 1;
}
result = i;
'''

        result = await executor.execute(ml_code, timeout=0.1)

        assert result.success is False
        assert "timeout" in result.error.lower()

    @pytest.mark.asyncio
    async def test_execution_with_error(self, executor):
        """Test execution that raises an error."""
        result = await executor.execute('result = undefined_variable;')

        assert result.success is False
        assert result.error is not None
        assert result.value is None

    @pytest.mark.asyncio
    async def test_concurrent_execution(self, executor):
        """Test concurrent execution of multiple ML scripts."""
        tasks = [
            executor.execute(f'result = {i} * 2;')
            for i in range(5)
        ]

        results = await asyncio.gather(*tasks)

        assert len(results) == 5
        for i, result in enumerate(results):
            assert result.success is True
            assert result.value == i * 2

    @pytest.mark.asyncio
    async def test_security_violation(self):
        """Test that security issues are caught."""
        executor = AsyncMLExecutor(max_workers=1, strict_security=True)

        try:
            # Code with security issue (if security analysis is working)
            result = await executor.execute('result = eval("malicious");')

            # Should either fail security check or execution
            assert result.success is False
            assert result.error is not None
        finally:
            executor.shutdown()

    @pytest.mark.asyncio
    async def test_no_result_variable(self, executor):
        """Test execution without result variable."""
        # Use a statement that doesn't set 'result' but is valid
        result = await executor.execute('x = 42;')

        # Should succeed but value is None (no result variable set)
        assert result.success is True
        assert result.value is None

    @pytest.mark.asyncio
    async def test_complex_ml_code(self, executor):
        """Test execution of complex ML code."""
        ml_code = '''
sum = 0;
i = 1;
while (i <= 10) {
    sum = sum + i;
    i = i + 1;
}
result = sum;
'''

        result = await executor.execute(ml_code)

        assert result.success is True
        assert result.value == 55  # Sum of 1 to 10

    @pytest.mark.asyncio
    async def test_execution_timing(self, executor):
        """Test that timing metrics are reasonable."""
        result = await executor.execute('result = 42;')

        assert result.success is True
        assert result.execution_time > 0
        assert result.transpile_time > 0
        assert result.transpile_time < result.execution_time


class TestAsyncMLExecutorWithExtensionPaths:
    """Test AsyncMLExecutor with custom extension paths."""

    @pytest.mark.asyncio
    async def test_extension_paths_parameter(self, tmp_path):
        """Test that extension paths are passed to transpiler."""
        ext_dir = tmp_path / "ext"
        ext_dir.mkdir()

        # Create simple test module
        (ext_dir / "test_bridge.py").write_text('''
from mlpy.stdlib.decorators import ml_module, ml_function

@ml_module(name="test", description="Test module")
class TestModule:
    @ml_function(description="Get value")
    def get_value(self):
        return 99

test = TestModule()
''')

        executor = AsyncMLExecutor(
            max_workers=1,
            strict_security=False,
            python_extension_paths=[str(ext_dir)]
        )

        try:
            # Try to use the custom module
            result = await executor.execute('import test; result = test.get_value();')

            # Should succeed if extension paths work
            assert result.success is True
            assert result.value == 99
        finally:
            executor.shutdown()


class TestConvenienceFunction:
    """Test async_ml_execute() convenience function."""

    @pytest.mark.asyncio
    async def test_simple_execute(self):
        """Test simple execution with convenience function."""
        result = await async_ml_execute('result = 3 * 4;')

        assert result.success is True
        assert result.value == 12

    @pytest.mark.asyncio
    async def test_execute_with_timeout(self):
        """Test execution with timeout using convenience function."""
        result = await async_ml_execute('result = 42;', timeout=5.0)

        assert result.success is True
        assert result.value == 42

    @pytest.mark.asyncio
    async def test_execute_with_context(self):
        """Test execution with context using convenience function."""
        context = {'a': 5, 'b': 3}
        result = await async_ml_execute('result = a * b;', context=context)

        assert result.success is True
        assert result.value == 15

    @pytest.mark.asyncio
    async def test_execute_with_security(self):
        """Test execution with strict security."""
        result = await async_ml_execute(
            'result = 42;',
            strict_security=True
        )

        assert result.success is True
        assert result.value == 42

    @pytest.mark.asyncio
    async def test_multiple_convenience_calls(self):
        """Test multiple convenience function calls."""
        results = await asyncio.gather(
            async_ml_execute('result = 1;'),
            async_ml_execute('result = 2;'),
            async_ml_execute('result = 3;')
        )

        assert len(results) == 3
        assert results[0].value == 1
        assert results[1].value == 2
        assert results[2].value == 3


class TestAsyncMLExecutorEdgeCases:
    """Test edge cases and error handling."""

    @pytest.fixture
    def executor(self):
        """Create test executor."""
        executor = AsyncMLExecutor(max_workers=1, strict_security=False)
        yield executor
        executor.shutdown()

    @pytest.mark.asyncio
    async def test_empty_code(self, executor):
        """Test execution with empty code."""
        result = await executor.execute('')

        # Should handle gracefully (either succeed with no result or error)
        assert isinstance(result, AsyncMLResult)

    @pytest.mark.asyncio
    async def test_invalid_syntax(self, executor):
        """Test execution with invalid ML syntax."""
        result = await executor.execute('this is not valid ML syntax}}')

        assert result.success is False
        assert result.error is not None

    @pytest.mark.asyncio
    async def test_shutdown_and_execute(self, executor):
        """Test execution after shutdown."""
        executor.shutdown()

        # Should handle gracefully or raise appropriate error
        with pytest.raises(Exception):
            await executor.execute('result = 42;')

    @pytest.mark.asyncio
    async def test_very_long_execution(self, executor):
        """Test execution that takes a reasonable amount of time."""
        ml_code = '''
sum = 0;
i = 0;
while (i < 1000) {
    sum = sum + i;
    i = i + 1;
}
result = sum;
'''

        result = await executor.execute(ml_code, timeout=10.0)

        assert result.success is True
        assert result.value == 499500  # Sum of 0 to 999


class TestAsyncMLExecutorPerformance:
    """Test performance characteristics of AsyncMLExecutor."""

    @pytest.fixture
    def executor(self):
        """Create test executor."""
        executor = AsyncMLExecutor(max_workers=4, strict_security=False)
        yield executor
        executor.shutdown()

    @pytest.mark.asyncio
    async def test_concurrent_performance(self, executor):
        """Test that concurrent execution is actually concurrent."""
        start_time = time.perf_counter()

        # Execute 10 tasks concurrently
        tasks = [
            executor.execute(f'result = {i};')
            for i in range(10)
        ]

        results = await asyncio.gather(*tasks)
        elapsed = time.perf_counter() - start_time

        # All should succeed
        assert all(r.success for r in results)

        # Should be much faster than sequential (< 1 second for simple operations)
        assert elapsed < 2.0

    @pytest.mark.asyncio
    async def test_transpiler_reuse(self, executor):
        """Test that transpiler is reused for performance."""
        # First execution (transpiler initialization)
        result1 = await executor.execute('result = 1;')

        # Second execution (transpiler reused)
        result2 = await executor.execute('result = 2;')

        # Both should succeed
        assert result1.success is True
        assert result2.success is True

        # Verify transpiler was reused (not None)
        assert executor._transpiler is not None
