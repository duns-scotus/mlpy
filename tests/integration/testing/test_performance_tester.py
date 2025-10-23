"""Tests for PerformanceTester class."""

import asyncio
import pytest

from mlpy.integration.testing.performance import PerformanceTester, quick_benchmark
from mlpy.integration.testing.mocks import MockREPLSession


class TestPerformanceTester:
    """Tests for PerformanceTester."""

    def test_initialization(self):
        """Test performance tester initializes correctly."""
        tester = PerformanceTester()

        assert len(tester.metrics) == 0

    @pytest.mark.anyio
    async def test_benchmark_async_execution(self):
        """Test async execution benchmarking."""
        tester = PerformanceTester()

        # Use simple ML code for testing
        results = await tester.benchmark_async_execution(
            "result = 2 + 2;",
            iterations=5
        )

        assert "mean" in results
        assert "median" in results
        assert "std_dev" in results
        assert "min" in results
        assert "max" in results
        assert results["iterations"] == 5

        # Check metrics were recorded
        assert len(tester.metrics) == 1
        assert tester.metrics[0]["type"] == "async_execution"

    @pytest.mark.anyio
    async def test_benchmark_concurrent_executions(self):
        """Test concurrent execution benchmarking."""
        tester = PerformanceTester()

        results = await tester.benchmark_concurrent_executions(
            "result = 2 + 2;",
            concurrency=3
        )

        assert "total_time" in results
        assert "avg_per_execution" in results
        assert "throughput" in results
        assert results["concurrency"] == 3
        assert results["throughput"] > 0

        # Check metrics were recorded
        assert len(tester.metrics) == 1
        assert tester.metrics[0]["type"] == "concurrent_execution"

    def test_benchmark_callback_overhead(self):
        """Test callback overhead benchmarking."""
        tester = PerformanceTester()
        mock_session = MockREPLSession()

        # Setup mock function
        mock_session.execute_ml_line("function double(x) { return x * 2; }")

        results = tester.benchmark_callback_overhead(
            mock_session,
            "double",
            (5,),
            iterations=10
        )

        assert "mean" in results
        assert "median" in results
        assert "overhead_ms" in results
        assert results["iterations"] == 10

        # Check metrics were recorded
        assert len(tester.metrics) == 1
        assert tester.metrics[0]["type"] == "callback_overhead"

    @pytest.mark.anyio
    async def test_benchmark_with_warmup(self):
        """Test benchmarking with warmup iterations."""
        tester = PerformanceTester()

        results = await tester.benchmark_with_warmup(
            "result = 2 + 2;",
            warmup_iterations=2,
            test_iterations=3
        )

        assert "mean" in results
        assert results["iterations"] == 3

        # Only test iterations should be recorded in metrics
        assert len(tester.metrics) == 1

    def test_get_metrics_summary(self):
        """Test getting metrics summary."""
        tester = PerformanceTester()

        # Add some mock metrics
        tester.metrics.append({
            "type": "async_execution",
            "results": {"mean": 0.1}
        })
        tester.metrics.append({
            "type": "concurrent_execution",
            "results": {"throughput": 10}
        })

        summary = tester.get_metrics_summary()

        assert "async_execution" in summary
        assert "concurrent_execution" in summary
        assert "callback_overhead" in summary
        assert len(summary["async_execution"]) == 1
        assert len(summary["concurrent_execution"]) == 1

    def test_reset_metrics(self):
        """Test resetting metrics."""
        tester = PerformanceTester()

        tester.metrics.append({"type": "test"})
        assert len(tester.metrics) == 1

        tester.reset_metrics()
        assert len(tester.metrics) == 0

    def test_compare_performance(self):
        """Test performance comparison."""
        tester = PerformanceTester()

        baseline = {
            "mean": 0.1,
            "median": 0.09,
        }

        current = {
            "mean": 0.11,  # 10% slower
            "median": 0.095,
        }

        comparison = tester.compare_performance(baseline, current)

        assert "mean_diff" in comparison
        assert "mean_pct_change" in comparison
        assert "median_diff" in comparison
        assert "regression" in comparison

        assert comparison["mean_pct_change"] == pytest.approx(10.0, rel=0.1)
        assert comparison["regression"] is True

    def test_compare_performance_improvement(self):
        """Test performance comparison with improvement."""
        tester = PerformanceTester()

        baseline = {
            "mean": 0.1,
            "median": 0.09,
        }

        current = {
            "mean": 0.09,  # 10% faster
            "median": 0.085,
        }

        comparison = tester.compare_performance(baseline, current)

        assert comparison["mean_pct_change"] == pytest.approx(-10.0, rel=0.1)
        assert comparison["regression"] is False

    @pytest.mark.anyio
    async def test_quick_benchmark_function(self):
        """Test quick_benchmark convenience function."""
        results = await quick_benchmark("result = 1 + 1;", iterations=3)

        assert "mean" in results
        assert "median" in results
        assert results["iterations"] == 3

    @pytest.mark.anyio
    async def test_performance_metrics_accumulation(self):
        """Test that metrics accumulate correctly."""
        tester = PerformanceTester()

        # Run multiple benchmarks
        await tester.benchmark_async_execution("result = 1;", iterations=2)
        await tester.benchmark_concurrent_executions("result = 2;", concurrency=2)

        # Should have 2 metric entries
        assert len(tester.metrics) == 2

        # Check summary
        summary = tester.get_metrics_summary()
        assert len(summary["async_execution"]) == 1
        assert len(summary["concurrent_execution"]) == 1

    @pytest.mark.anyio
    async def test_benchmark_results_consistency(self):
        """Test that benchmark results are consistent."""
        tester = PerformanceTester()

        results = await tester.benchmark_async_execution(
            "result = 5;",
            iterations=5
        )

        # All timing metrics should be positive
        assert results["mean"] > 0
        assert results["median"] > 0
        assert results["min"] > 0
        assert results["max"] > 0
        assert results["std_dev"] >= 0

        # Min should be <= median <= max
        assert results["min"] <= results["median"]
        assert results["median"] <= results["max"]
