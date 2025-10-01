"""
Sprint 7: Current performance baseline measurement and optimization opportunities.
Focus on understanding actual performance characteristics rather than strict thresholds.
"""

import statistics
import time

from mlpy.ml.transpiler import MLTranspiler


class PerformanceProfiler:
    """Measure current performance and identify optimization opportunities."""

    def __init__(self):
        self.transpiler = MLTranspiler()
        self.measurements = {}

    def measure_operation(self, name: str, operation_func, iterations: int = 10):
        """Measure operation performance with statistical analysis."""
        times = []
        success_count = 0

        for i in range(iterations):
            try:
                start = time.perf_counter()
                result = operation_func()
                end = time.perf_counter()

                times.append((end - start) * 1000)  # Convert to milliseconds
                if result is not None:
                    success_count += 1
            except Exception as e:
                print(f"  Iteration {i+1} failed: {e}")

        if times:
            self.measurements[name] = {
                "mean_ms": statistics.mean(times),
                "median_ms": statistics.median(times),
                "min_ms": min(times),
                "max_ms": max(times),
                "stdev_ms": statistics.stdev(times) if len(times) > 1 else 0,
                "success_rate": success_count / iterations,
                "total_iterations": iterations,
            }
        else:
            self.measurements[name] = {"error": "All iterations failed"}

        return self.measurements[name]

    def print_results(self):
        """Print formatted performance results."""
        print("\n" + "=" * 80)
        print("SPRINT 7: PERFORMANCE BASELINE MEASUREMENTS")
        print("=" * 80)

        for name, result in self.measurements.items():
            if "error" in result:
                print(f"\n[ERROR] {name}: {result['error']}")
            else:
                success_mark = "[OK]" if result["success_rate"] == 1.0 else "[WARN]"
                print(f"\n{success_mark} {name.upper()}:")
                print(f"  Mean: {result['mean_ms']:.2f}ms")
                print(f"  Median: {result['median_ms']:.2f}ms")
                print(f"  Range: {result['min_ms']:.2f}ms - {result['max_ms']:.2f}ms")
                print(f"  Std Dev: {result['stdev_ms']:.2f}ms")
                print(f"  Success Rate: {result['success_rate']*100:.1f}%")


def profile_current_performance():
    """Profile current mlpy transpiler performance."""
    profiler = PerformanceProfiler()

    # Test programs of increasing complexity (corrected ML syntax)
    test_programs = {
        "simple": "x = 42; print(x);",
        "control_flow": """
function factorial(n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}
print(factorial(5));
""",
        "data_structures": """
data = [1, 2, 3, 4, 5];
person = {
    name: "Alice",
    age: 30
};
print(data[0] + person.age);
""",
        "complex": """
// Advanced ML features
function Point(x, y) {
    return {
        x: x,
        y: y,
        distance: function(other) {
            dx = this.x - other.x;
            dy = this.y - other.y;
            return dx * dx + dy * dy;
        }
    };
}

points = [Point(0, 0), Point(3, 4)];
origin = Point(0, 0);

for (i = 0; i < len(points); i = i + 1) {
    print("Distance:", points[i].distance(origin));
}
""",
    }

    print("Profiling mlpy transpiler performance...")

    # Profile each operation type
    for prog_name, program in test_programs.items():
        print(f"\nProfiling {prog_name} program...")

        # Parsing performance
        def parse_op():
            ast, issues = profiler.transpiler.parse_with_security_analysis(program)
            return ast

        profiler.measure_operation(f"parse_{prog_name}", parse_op, iterations=20)

        # Security analysis performance
        def security_op():
            return profiler.transpiler.validate_security_only(program)

        profiler.measure_operation(f"security_{prog_name}", security_op, iterations=20)

        # Full transpilation performance
        def transpile_op():
            python_code, issues, source_map = profiler.transpiler.transpile_to_python(program)
            return python_code

        profiler.measure_operation(f"transpile_{prog_name}", transpile_op, iterations=10)

    # Profile scalability
    print("\nProfiling scalability...")
    for size in [10, 50, 100]:
        large_program = "\n".join([f"var_{i} = {i};" for i in range(size)])

        def scale_op():
            python_code, _, _ = profiler.transpiler.transpile_to_python(large_program)
            return python_code

        profiler.measure_operation(f"scale_{size}_vars", scale_op, iterations=5)

    # Print comprehensive results
    profiler.print_results()

    # Identify optimization opportunities
    print("\n" + "=" * 80)
    print("OPTIMIZATION OPPORTUNITIES")
    print("=" * 80)

    # Find slowest operations
    slow_ops = []
    for name, result in profiler.measurements.items():
        if "mean_ms" in result and result["mean_ms"] > 50:
            slow_ops.append((name, result["mean_ms"]))

    if slow_ops:
        slow_ops.sort(key=lambda x: x[1], reverse=True)
        print("\n[SLOW] Slowest operations (>50ms average):")
        for name, avg_time in slow_ops[:5]:
            print(f"  {name}: {avg_time:.2f}ms")

    # Find operations with high variance
    high_variance = []
    for name, result in profiler.measurements.items():
        if "stdev_ms" in result and result["stdev_ms"] > 10:
            high_variance.append((name, result["stdev_ms"]))

    if high_variance:
        high_variance.sort(key=lambda x: x[1], reverse=True)
        print("\n[VARIANCE] High variance operations (>10ms std dev):")
        for name, std_dev in high_variance[:5]:
            print(f"  {name}: +/-{std_dev:.2f}ms")

    # Check success rates
    failed_ops = []
    for name, result in profiler.measurements.items():
        if "success_rate" in result and result["success_rate"] < 1.0:
            failed_ops.append((name, result["success_rate"]))

    if failed_ops:
        print("\n[FAILED] Operations with failures:")
        for name, success_rate in failed_ops:
            print(f"  {name}: {success_rate*100:.1f}% success rate")

    return profiler.measurements


if __name__ == "__main__":
    measurements = profile_current_performance()

    print("\n" + "=" * 80)
    print("SPRINT 7 PERFORMANCE BASELINE ESTABLISHED")
    print("=" * 80)
    print("[OK] Performance measurements complete")
    print("[OK] Optimization opportunities identified")
    print("[OK] Ready for performance improvements")
