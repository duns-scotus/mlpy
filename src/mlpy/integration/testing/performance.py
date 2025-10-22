"""Performance testing utilities for the Integration Toolkit.

Provides benchmarking tools for async ML execution, callback overhead,
and concurrent execution throughput.
"""

import asyncio
import statistics
import time
from typing import Dict, List

from mlpy.cli.repl import MLREPLSession
from mlpy.integration.async_executor import async_ml_execute
from mlpy.integration.ml_callback import ml_callback


class PerformanceTester:
    """Performance testing utilities for Integration Toolkit.

    This class provides methods to benchmark async execution, callbacks,
    and concurrent execution performance.

    Example:
        ```python
        tester = PerformanceTester()

        # Benchmark async execution
        results = await tester.benchmark_async_execution(
            "result = 2 + 2;",
            iterations=100
        )
        print(f"Mean: {results['mean']*1000:.2f}ms")

        # Benchmark concurrency
        results = await tester.benchmark_concurrent_executions(
            "result = 2 + 2;",
            concurrency=50
        )
        print(f"Throughput: {results['throughput']:.2f} exec/sec")
        ```
    """

    def __init__(self):
        """Initialize the performance tester."""
        self.metrics: List[Dict] = []

    async def benchmark_async_execution(
        self, ml_code: str, iterations: int = 100
    ) -> Dict[str, float]:
        """Benchmark async execution performance.

        Args:
            ml_code: ML code to execute
            iterations: Number of iterations to run

        Returns:
            Dictionary with performance metrics:
                - mean: Mean execution time (seconds)
                - median: Median execution time (seconds)
                - std_dev: Standard deviation (seconds)
                - min: Minimum execution time (seconds)
                - max: Maximum execution time (seconds)
                - iterations: Number of iterations performed
        """
        execution_times: List[float] = []

        for _ in range(iterations):
            start = time.perf_counter()
            result = await async_ml_execute(ml_code, timeout=30.0)
            end = time.perf_counter()
            if result.success:
                execution_times.append(end - start)
            else:
                # Skip failed executions in performance metrics
                continue

        results = {
            "mean": statistics.mean(execution_times),
            "median": statistics.median(execution_times),
            "std_dev": (
                statistics.stdev(execution_times) if len(execution_times) > 1 else 0.0
            ),
            "min": min(execution_times),
            "max": max(execution_times),
            "iterations": iterations,
        }

        self.metrics.append(
            {
                "type": "async_execution",
                "code": ml_code,
                "results": results,
                "timestamp": time.time(),
            }
        )

        return results

    async def benchmark_concurrent_executions(
        self, ml_code: str, concurrency: int = 10
    ) -> Dict[str, float]:
        """Benchmark concurrent execution performance.

        Args:
            ml_code: ML code to execute
            concurrency: Number of concurrent executions

        Returns:
            Dictionary with concurrency metrics:
                - total_time: Total time for all executions (seconds)
                - avg_per_execution: Average time per execution (seconds)
                - throughput: Executions per second
                - concurrency: Number of concurrent executions
        """
        start = time.perf_counter()

        tasks = [
            async_ml_execute(ml_code, timeout=30.0) for _ in range(concurrency)
        ]
        await asyncio.gather(*tasks)

        end = time.perf_counter()
        total_time = end - start

        results = {
            "total_time": total_time,
            "avg_per_execution": total_time / concurrency,
            "throughput": concurrency / total_time,
            "concurrency": concurrency,
        }

        self.metrics.append(
            {
                "type": "concurrent_execution",
                "code": ml_code,
                "results": results,
                "timestamp": time.time(),
            }
        )

        return results

    def benchmark_callback_overhead(
        self,
        session: MLREPLSession,
        function_name: str,
        args: tuple,
        iterations: int = 1000,
    ) -> Dict[str, float]:
        """Benchmark callback overhead.

        Args:
            session: REPL session containing the function
            function_name: Name of the ML function
            args: Arguments to pass to the function
            iterations: Number of iterations to run

        Returns:
            Dictionary with callback overhead metrics:
                - mean: Mean execution time (seconds)
                - median: Median execution time (seconds)
                - overhead_ms: Mean overhead in milliseconds
                - iterations: Number of iterations performed
        """
        callback = ml_callback(session, function_name)

        execution_times: List[float] = []
        for _ in range(iterations):
            start = time.perf_counter()
            callback(*args)
            end = time.perf_counter()
            execution_times.append(end - start)

        results = {
            "mean": statistics.mean(execution_times),
            "median": statistics.median(execution_times),
            "overhead_ms": statistics.mean(execution_times) * 1000,
            "iterations": iterations,
        }

        self.metrics.append(
            {
                "type": "callback_overhead",
                "function": function_name,
                "results": results,
                "timestamp": time.time(),
            }
        )

        return results

    async def benchmark_with_warmup(
        self, ml_code: str, warmup_iterations: int = 10, test_iterations: int = 100
    ) -> Dict[str, float]:
        """Benchmark with warmup iterations to stabilize JIT/caching.

        Args:
            ml_code: ML code to execute
            warmup_iterations: Number of warmup iterations
            test_iterations: Number of test iterations

        Returns:
            Performance metrics after warmup
        """
        # Warmup phase
        for _ in range(warmup_iterations):
            result = await async_ml_execute(ml_code, timeout=30.0)
            if not result.success:
                raise RuntimeError(f"Warmup execution failed: {result.error}")

        # Test phase
        return await self.benchmark_async_execution(ml_code, iterations=test_iterations)

    def get_metrics_summary(self) -> Dict:
        """Get summary of all collected metrics.

        Returns:
            Dictionary with metrics summary by type
        """
        summary = {
            "async_execution": [],
            "concurrent_execution": [],
            "callback_overhead": [],
        }

        for metric in self.metrics:
            metric_type = metric["type"]
            if metric_type in summary:
                summary[metric_type].append(metric)

        return summary

    def reset_metrics(self):
        """Clear all collected metrics."""
        self.metrics.clear()

    def compare_performance(
        self, baseline: Dict[str, float], current: Dict[str, float]
    ) -> Dict[str, float]:
        """Compare current performance against baseline.

        Args:
            baseline: Baseline performance metrics
            current: Current performance metrics

        Returns:
            Dictionary with performance comparison:
                - mean_diff: Difference in mean time (seconds)
                - mean_pct_change: Percentage change in mean time
                - median_diff: Difference in median time (seconds)
                - regression: True if current is slower than baseline
        """
        mean_diff = current["mean"] - baseline["mean"]
        mean_pct_change = (mean_diff / baseline["mean"]) * 100

        median_diff = current["median"] - baseline["median"]

        return {
            "mean_diff": mean_diff,
            "mean_pct_change": mean_pct_change,
            "median_diff": median_diff,
            "regression": mean_pct_change > 5.0,  # >5% slower is regression
        }


# Convenience function
async def quick_benchmark(ml_code: str, iterations: int = 100) -> Dict[str, float]:
    """Quick benchmark utility for ad-hoc performance testing.

    Args:
        ml_code: ML code to benchmark
        iterations: Number of iterations

    Returns:
        Performance metrics

    Example:
        ```python
        results = await quick_benchmark("result = 2 + 2;")
        print(f"Mean: {results['mean']*1000:.2f}ms")
        ```
    """
    tester = PerformanceTester()
    return await tester.benchmark_async_execution(ml_code, iterations=iterations)
