"""Example: Testing Async ML Execution with IntegrationTestHelper.

This example demonstrates how to use IntegrationTestHelper to test
async ML code execution in your Python applications.
"""

import pytest
from mlpy.integration.testing import IntegrationTestHelper


class TestAsyncExecutionExamples:
    """Examples of testing async ML execution."""

    @pytest.fixture
    def helper(self):
        """Create a test helper and clean up after each test."""
        helper = IntegrationTestHelper()
        yield helper
        helper.cleanup()

    @pytest.mark.anyio
    async def test_simple_arithmetic(self, helper):
        """Test simple arithmetic operations in ML."""
        await helper.assert_async_execution(
            ml_code="result = 2 + 2;",
            expected_result=4
        )

    @pytest.mark.anyio
    async def test_complex_calculation(self, helper):
        """Test complex mathematical calculations."""
        ml_code = """
        // Calculate compound interest
        principal = 1000;
        rate = 0.05;
        time = 3;
        amount = principal * ((1 + rate) ** time);
        """

        await helper.assert_async_execution(
            ml_code=ml_code,
            expected_result=1157.625,  # 1000 * (1.05 ** 3)
            timeout=5.0
        )

    @pytest.mark.anyio
    async def test_string_manipulation(self, helper):
        """Test string operations."""
        ml_code = """
        import string;
        text = "hello world";
        result = string.upper(text);
        """

        await helper.assert_async_execution(
            ml_code=ml_code,
            expected_result="HELLO WORLD"
        )

    @pytest.mark.anyio
    async def test_array_operations(self, helper):
        """Test array operations."""
        ml_code = """
        numbers = [1, 2, 3, 4, 5];
        doubled = [];
        for (i = 0; i < len(numbers); i = i + 1) {
            doubled[i] = numbers[i] * 2;
        }
        result = doubled;
        """

        await helper.assert_async_execution(
            ml_code=ml_code,
            expected_result=[2, 4, 6, 8, 10]
        )

    @pytest.mark.anyio
    async def test_multiple_executions(self, helper):
        """Test tracking multiple async executions."""
        # Execute multiple times
        await helper.assert_async_execution("result = 1;", expected_result=1)
        await helper.assert_async_execution("result = 2;", expected_result=2)
        await helper.assert_async_execution("result = 3;", expected_result=3)

        # Check execution history
        history = helper.get_execution_history()
        assert len(history) == 3
        assert history[0]["ml_code"] == "result = 1;"
        assert history[1]["ml_code"] == "result = 2;"
        assert history[2]["ml_code"] == "result = 3;"

    @pytest.mark.anyio
    async def test_execution_timing(self, helper):
        """Test that execution timing is tracked."""
        await helper.assert_async_execution("result = 100;", expected_result=100)

        history = helper.get_execution_history()
        assert len(history) == 1

        # Execution time should be tracked
        assert "execution_time" in history[0]
        assert history[0]["execution_time"] is not None
        assert isinstance(history[0]["execution_time"], (int, float))

    @pytest.mark.anyio
    async def test_function_definition_and_call(self, helper):
        """Test defining and calling ML functions."""
        ml_code = """
        function factorial(n) {
            if (n <= 1) {
                return 1;
            }
            return n * factorial(n - 1);
        }
        result = factorial(5);
        """

        await helper.assert_async_execution(
            ml_code=ml_code,
            expected_result=120  # 5! = 120
        )

    @pytest.mark.anyio
    async def test_object_manipulation(self, helper):
        """Test object creation and manipulation."""
        ml_code = """
        person = {
            "name": "Alice",
            "age": 30,
            "city": "New York"
        };
        result = person.age;
        """

        await helper.assert_async_execution(
            ml_code=ml_code,
            expected_result=30
        )


@pytest.mark.anyio
async def test_quick_async_test_without_helper():
    """Example: Quick async test without helper for simple cases."""
    from mlpy.integration.async_executor import async_ml_execute

    result = await async_ml_execute("result = 42;")

    assert result.success is True
    assert result.value == 42
    assert result.error is None


if __name__ == "__main__":
    # Run with: pytest test_async_execution_example.py -v
    pytest.main([__file__, "-v"])
