"""Example: Performance Benchmarking with PerformanceTester.

This example demonstrates how to use PerformanceTester to benchmark
ML execution performance and identify optimization opportunities.
"""

import pytest
from mlpy.integration.testing import PerformanceTester, quick_benchmark


class TestPerformanceBenchmarkingExamples:
    """Examples of performance benchmarking."""

    @pytest.fixture
    def tester(self):
        """Create a performance tester."""
        return PerformanceTester()

    @pytest.mark.anyio
    async def test_benchmark_simple_execution(self, tester):
        """Benchmark simple ML execution."""
        results = await tester.benchmark_async_execution(
            ml_code="result = 2 + 2;",
            iterations=50
        )

        # Check results structure
        assert "mean" in results
        assert "median" in results
        assert "std_dev" in results
        assert "min" in results
        assert "max" in results

        # Verify performance metrics are reasonable
        assert results["mean"] > 0
        assert results["min"] <= results["mean"] <= results["max"]

        print(f"\nSimple Execution Benchmark:")
        print(f"  Mean: {results['mean'] * 1000:.2f}ms")
        print(f"  Median: {results['median'] * 1000:.2f}ms")
        print(f"  Std Dev: {results['std_dev'] * 1000:.2f}ms")
        print(f"  Range: {results['min'] * 1000:.2f}ms - {results['max'] * 1000:.2f}ms")

    @pytest.mark.anyio
    async def test_benchmark_complex_execution(self, tester):
        """Benchmark complex ML execution with loops."""
        ml_code = """
        total = 0;
        for (i = 0; i < 100; i = i + 1) {
            total = total + i;
        }
        result = total;
        """

        results = await tester.benchmark_async_execution(
            ml_code=ml_code,
            iterations=30
        )

        print(f"\nComplex Execution Benchmark:")
        print(f"  Mean: {results['mean'] * 1000:.2f}ms")
        print(f"  Iterations: {results['iterations']}")

    @pytest.mark.anyio
    async def test_benchmark_concurrent_executions(self, tester):
        """Benchmark concurrent ML executions."""
        results = await tester.benchmark_concurrent_executions(
            ml_code="result = 42;",
            concurrency=10
        )

        # Check results structure
        assert "total_time" in results
        assert "avg_per_execution" in results
        assert "throughput" in results
        assert "concurrency" in results

        print(f"\nConcurrent Execution Benchmark:")
        print(f"  Total Time: {results['total_time'] * 1000:.2f}ms")
        print(f"  Avg Per Execution: {results['avg_per_execution'] * 1000:.2f}ms")
        print(f"  Throughput: {results['throughput']:.2f} executions/sec")
        print(f"  Concurrency: {results['concurrency']}")

    @pytest.mark.anyio
    async def test_benchmark_callback_overhead(self, tester):
        """Benchmark ML callback overhead."""
        # Create REPL and define function
        from mlpy.cli.repl import MLREPLSession

        session = MLREPLSession(security_enabled=False)
        session.execute_ml_line("function simple(x) { return x; }")

        results = await tester.benchmark_callback_overhead(
            session=session,
            function_name="simple",
            args=(42,),
            kwargs={},
            iterations=100
        )

        # Verify results
        assert "mean" in results
        assert results["mean"] > 0

        print(f"\nCallback Overhead Benchmark:")
        print(f"  Mean: {results['mean'] * 1000:.2f}ms")
        print(f"  Median: {results['median'] * 1000:.2f}ms")

        # Cleanup
        session.cleanup()

    @pytest.mark.anyio
    async def test_compare_execution_methods(self, tester):
        """Compare performance of different execution methods."""
        from mlpy.cli.repl import MLREPLSession

        # Benchmark 1: Direct async execution
        async_results = await tester.benchmark_async_execution(
            ml_code="result = 100;",
            iterations=30
        )

        # Benchmark 2: Callback execution
        session = MLREPLSession(security_enabled=False)
        session.execute_ml_line("function return_value(x) { return x; }")

        callback_results = await tester.benchmark_callback_overhead(
            session=session,
            function_name="return_value",
            args=(100,),
            kwargs={},
            iterations=30
        )

        print(f"\nExecution Method Comparison:")
        print(f"  Async Execution - Mean: {async_results['mean'] * 1000:.2f}ms")
        print(f"  Callback Execution - Mean: {callback_results['mean'] * 1000:.2f}ms")

        # Cleanup
        session.cleanup()

    @pytest.mark.anyio
    async def test_benchmark_scalability(self, tester):
        """Test performance scalability with different concurrency levels."""
        ml_code = "result = 42;"

        concurrency_levels = [1, 5, 10, 20]
        results = []

        for concurrency in concurrency_levels:
            result = await tester.benchmark_concurrent_executions(
                ml_code=ml_code,
                concurrency=concurrency
            )
            results.append((concurrency, result))

        print(f"\nScalability Benchmark:")
        for concurrency, result in results:
            print(f"  Concurrency {concurrency}: {result['throughput']:.2f} exec/sec")

    @pytest.mark.anyio
    async def test_benchmark_with_statistics(self, tester):
        """Benchmark with detailed statistical analysis."""
        ml_code = """
        import math;
        result = math.sqrt(100);
        """

        results = await tester.benchmark_async_execution(
            ml_code=ml_code,
            iterations=50
        )

        # Calculate additional statistics
        mean = results["mean"]
        std_dev = results["std_dev"]
        coefficient_of_variation = (std_dev / mean) * 100 if mean > 0 else 0

        print(f"\nDetailed Statistical Analysis:")
        print(f"  Mean: {mean * 1000:.2f}ms")
        print(f"  Std Dev: {std_dev * 1000:.2f}ms")
        print(f"  Min: {results['min'] * 1000:.2f}ms")
        print(f"  Max: {results['max'] * 1000:.2f}ms")
        print(f"  Coefficient of Variation: {coefficient_of_variation:.2f}%")


@pytest.mark.anyio
async def test_quick_benchmark_utility():
    """Example: Using the quick_benchmark utility function."""
    ml_code = "result = 42;"

    # Quick benchmark with default iterations
    results = await quick_benchmark(ml_code)

    assert "mean" in results
    assert "median" in results

    print(f"\nQuick Benchmark Results:")
    print(f"  Mean: {results['mean'] * 1000:.2f}ms")
    print(f"  Median: {results['median'] * 1000:.2f}ms")


@pytest.mark.anyio
async def test_benchmark_for_optimization():
    """Example: Using benchmarks to guide optimization."""
    from mlpy.integration.testing import PerformanceTester

    tester = PerformanceTester()

    # Original implementation
    original_code = """
    result = 0;
    for (i = 0; i < 100; i = i + 1) {
        result = result + i;
    }
    """

    original_results = await tester.benchmark_async_execution(
        ml_code=original_code,
        iterations=30
    )

    # Optimized implementation (using mathematical formula)
    optimized_code = """
    n = 100;
    result = (n * (n - 1)) / 2;
    """

    optimized_results = await tester.benchmark_async_execution(
        ml_code=optimized_code,
        iterations=30
    )

    # Compare performance
    speedup = original_results["mean"] / optimized_results["mean"]

    print(f"\nOptimization Impact:")
    print(f"  Original: {original_results['mean'] * 1000:.2f}ms")
    print(f"  Optimized: {optimized_results['mean'] * 1000:.2f}ms")
    print(f"  Speedup: {speedup:.2f}x")


@pytest.mark.anyio
async def test_regression_testing():
    """Example: Using benchmarks for performance regression testing."""
    from mlpy.integration.testing import PerformanceTester

    tester = PerformanceTester()
    ml_code = "result = 42;"

    # Run benchmark
    results = await tester.benchmark_async_execution(ml_code, iterations=50)

    # Define performance threshold (e.g., should complete within 100ms)
    threshold_ms = 100
    actual_ms = results["mean"] * 1000

    print(f"\nRegression Test:")
    print(f"  Threshold: {threshold_ms}ms")
    print(f"  Actual: {actual_ms:.2f}ms")
    print(f"  Status: {'PASS' if actual_ms < threshold_ms else 'FAIL'}")

    # Assert performance is within acceptable range
    assert actual_ms < threshold_ms, f"Performance regression detected: {actual_ms:.2f}ms > {threshold_ms}ms"


if __name__ == "__main__":
    # Run with: pytest test_performance_example.py -v -s
    pytest.main([__file__, "-v", "-s"])
