"""
Performance benchmarks for ML integration examples
Measures transpilation overhead and execution performance
"""

import sys
import time
from pathlib import Path
from statistics import mean, stdev
import json

# Add mlpy to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.mlpy.ml.transpiler import MLTranspiler


class IntegrationBenchmark:
    """Benchmark ML integration performance"""

    def __init__(self):
        self.results = {}

    def benchmark_transpilation(self, ml_file: Path, name: str, iterations: int = 10):
        """Benchmark ML-to-Python transpilation time"""
        print(f"\n{'='*60}")
        print(f"Benchmarking Transpilation: {name}")
        print(f"{'='*60}")

        transpiler = MLTranspiler()
        with open(ml_file, encoding='utf-8') as f:
            ml_code = f.read()

        times = []
        for i in range(iterations):
            start = time.perf_counter()
            python_code, issues, source_map = transpiler.transpile_to_python(
                ml_code, source_file=str(ml_file), strict_security=False
            )
            end = time.perf_counter()

            if python_code is None:
                print(f"ERROR: Transpilation failed: {issues}")
                return None

            elapsed = (end - start) * 1000  # Convert to milliseconds
            times.append(elapsed)

        avg_time = mean(times)
        std_time = stdev(times) if len(times) > 1 else 0
        min_time = min(times)
        max_time = max(times)

        result = {
            "name": name,
            "ml_file_size": len(ml_code),
            "python_code_size": len(python_code),
            "iterations": iterations,
            "avg_time_ms": round(avg_time, 3),
            "std_dev_ms": round(std_time, 3),
            "min_time_ms": round(min_time, 3),
            "max_time_ms": round(max_time, 3),
        }

        self.results[f"transpilation_{name}"] = result

        print(f"ML Code Size: {len(ml_code):,} bytes")
        print(f"Python Code Size: {len(python_code):,} bytes")
        print(f"Compression Ratio: {len(python_code) / len(ml_code):.2f}x")
        print(f"\nTranspilation Performance:")
        print(f"  Average: {avg_time:.3f} ms")
        print(f"  Std Dev: {std_time:.3f} ms")
        print(f"  Min: {min_time:.3f} ms")
        print(f"  Max: {max_time:.3f} ms")

        return python_code

    def benchmark_function_calls(self, namespace: dict, name: str, iterations: int = 10000):
        """Benchmark ML function call overhead"""
        print(f"\n{'='*60}")
        print(f"Benchmarking Function Calls: {name}")
        print(f"{'='*60}")

        # Benchmark simple arithmetic (no capabilities needed)
        if "add" in namespace:
            times = []
            for _ in range(iterations):
                start = time.perf_counter()
                result = namespace["add"](5, 3)
                end = time.perf_counter()
                times.append((end - start) * 1_000_000)  # microseconds

            avg_time = mean(times)
            print(f"\nadd(5, 3) - Simple Arithmetic:")
            print(f"  Average: {avg_time:.3f} us per call")
            print(f"  Throughput: {1_000_000 / avg_time:,.0f} calls/second")

            self.results[f"{name}_add_call"] = {
                "function": "add",
                "iterations": iterations,
                "avg_time_us": round(avg_time, 3),
                "calls_per_second": round(1_000_000 / avg_time, 0)
            }

        # Benchmark division (no capabilities needed)
        if "divide" in namespace:
            times = []
            for _ in range(iterations):
                start = time.perf_counter()
                result = namespace["divide"](10, 2)
                end = time.perf_counter()
                times.append((end - start) * 1_000_000)  # microseconds

            avg_time = mean(times)
            print(f"\ndivide(10, 2) - Division with null check:")
            print(f"  Average: {avg_time:.3f} us per call")
            print(f"  Throughput: {1_000_000 / avg_time:,.0f} calls/second")

            self.results[f"{name}_divide_call"] = {
                "function": "divide",
                "iterations": iterations,
                "avg_time_us": round(avg_time, 3),
                "calls_per_second": round(1_000_000 / avg_time, 0)
            }

    def benchmark_ml_vs_python(self):
        """Compare ML implementation vs pure Python"""
        print(f"\n{'='*60}")
        print(f"Benchmarking ML vs Pure Python")
        print(f"{'='*60}")

        # Pure Python implementation
        def python_add(a, b):
            return a + b

        def python_fibonacci(n):
            if n <= 1:
                return n
            a, b, i = 0, 1, 2
            while i <= n:
                a, b = b, a + b
                i += 1
            return b

        # Load ML functions
        ml_file = Path(__file__).parent / "gui/pyside6/ml_calculator.ml"
        transpiler = MLTranspiler()
        with open(ml_file, encoding='utf-8') as f:
            ml_code = f.read()

        python_code, issues, source_map = transpiler.transpile_to_python(
            ml_code, source_file=str(ml_file), strict_security=False
        )

        namespace = {}
        exec(python_code, namespace)

        # Benchmark add function
        iterations = 100000
        print(f"\nBenchmarking add(5, 3) - {iterations} iterations:")

        # Python version
        start = time.perf_counter()
        for _ in range(iterations):
            result = python_add(5, 3)
        python_time = time.perf_counter() - start

        # ML version
        start = time.perf_counter()
        for _ in range(iterations):
            result = namespace["add"](5, 3)
        ml_time = time.perf_counter() - start

        overhead = ((ml_time - python_time) / python_time) * 100

        print(f"  Pure Python: {python_time*1000:.3f} ms")
        print(f"  ML Transpiled: {ml_time*1000:.3f} ms")
        print(f"  Overhead: {overhead:.1f}%")

        self.results["ml_vs_python_add"] = {
            "iterations": iterations,
            "python_time_ms": round(python_time * 1000, 3),
            "ml_time_ms": round(ml_time * 1000, 3),
            "overhead_percent": round(overhead, 1)
        }

        # Benchmark Fibonacci
        iterations = 10000
        n = 20
        print(f"\nBenchmarking fibonacci({n}) - {iterations} iterations:")

        # Python version
        start = time.perf_counter()
        for _ in range(iterations):
            result = python_fibonacci(n)
        python_time = time.perf_counter() - start

        # ML version
        start = time.perf_counter()
        for _ in range(iterations):
            result = namespace["fibonacci"](n)
        ml_time = time.perf_counter() - start

        overhead = ((ml_time - python_time) / python_time) * 100

        print(f"  Pure Python: {python_time*1000:.3f} ms")
        print(f"  ML Transpiled: {ml_time*1000:.3f} ms")
        print(f"  Overhead: {overhead:.1f}%")

        self.results["ml_vs_python_fibonacci"] = {
            "iterations": iterations,
            "n": n,
            "python_time_ms": round(python_time * 1000, 3),
            "ml_time_ms": round(ml_time * 1000, 3),
            "overhead_percent": round(overhead, 1)
        }

    def run_all_benchmarks(self):
        """Run all benchmarks"""
        print("\n" + "="*60)
        print("ML INTEGRATION PERFORMANCE BENCHMARKS")
        print("="*60)

        # Benchmark transpilation for each example
        examples = [
            (Path(__file__).parent / "gui/pyside6/ml_calculator.ml", "pyside6_calculator"),
            (Path(__file__).parent / "web/flask/ml_api.ml", "flask_api"),
            (Path(__file__).parent / "web/fastapi/ml_analytics.ml", "fastapi_analytics"),
        ]

        for ml_file, name in examples:
            python_code = self.benchmark_transpilation(ml_file, name)

            if python_code and name == "pyside6_calculator":
                # Benchmark function calls for calculator
                namespace = {}
                exec(python_code, namespace)
                self.benchmark_function_calls(namespace, name, iterations=10000)

        # ML vs Python comparison
        self.benchmark_ml_vs_python()

        # Print summary
        self.print_summary()

    def print_summary(self):
        """Print benchmark summary"""
        print(f"\n{'='*60}")
        print("BENCHMARK SUMMARY")
        print(f"{'='*60}")

        # Transpilation summary
        print("\n## Transpilation Performance:")
        for key, result in self.results.items():
            if key.startswith("transpilation_"):
                name = result["name"]
                avg = result["avg_time_ms"]
                size = result["ml_file_size"]
                print(f"  {name}: {avg:.3f} ms (ML: {size:,} bytes)")

        # Function call summary
        print("\n## Function Call Performance:")
        for key, result in self.results.items():
            if "_call" in key:
                func = result["function"]
                avg = result["avg_time_us"]
                throughput = result["calls_per_second"]
                print(f"  {func}(): {avg:.3f} us/call ({throughput:,.0f} calls/sec)")

        # ML vs Python summary
        print("\n## ML vs Pure Python:")
        for key, result in self.results.items():
            if key.startswith("ml_vs_python_"):
                func = key.replace("ml_vs_python_", "")
                overhead = result["overhead_percent"]
                print(f"  {func}: {overhead:.1f}% overhead")

        # Save results to JSON
        output_file = Path(__file__).parent / "benchmark_results.json"
        with open(output_file, "w") as f:
            json.dump(self.results, f, indent=2)
        print(f"\n[OK] Results saved to: {output_file}")


def main():
    """Run benchmarks"""
    benchmark = IntegrationBenchmark()
    benchmark.run_all_benchmarks()


if __name__ == "__main__":
    main()
