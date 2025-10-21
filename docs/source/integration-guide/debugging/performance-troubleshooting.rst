Performance Troubleshooting
===========================

.. note::
   **Chapter Summary:** Comprehensive guide to identifying, analyzing, and resolving performance bottlenecks in ML-Python integration.

.. contents:: In This Chapter
   :local:
   :depth: 2

Overview
--------

Performance is critical for production ML integrations. This chapter provides systematic approaches to identifying bottlenecks, profiling execution, optimizing code, and achieving production-grade performance.

**What You'll Learn:**

* Performance bottleneck identification techniques
* ML execution profiling and analysis
* Memory profiling and optimization
* Transpilation performance optimization
* Caching strategies
* Benchmarking and performance testing
* Real-world case studies and solutions

**Prerequisites:**

* Understanding of ML execution model
* Familiarity with Python profiling tools
* Basic knowledge of performance concepts

Performance Bottleneck Identification
--------------------------------------

Common Performance Issues
^^^^^^^^^^^^^^^^^^^^^^^^^

**Issue 1: Slow Transpilation**

**Symptom:**

.. code-block:: python

   import time

   start = time.perf_counter()
   result = transpile_ml_code(large_ml_file)
   end = time.perf_counter()

   print(f"Transpilation took {(end - start) * 1000:.2f}ms")
   # Output: Transpilation took 2500.00ms (very slow!)

**Diagnosis:**

.. code-block:: python

   from mlpy.ml.transpiler import MLTranspiler

   transpiler = MLTranspiler()

   # Profile transpilation stages
   import cProfile
   import pstats

   profiler = cProfile.Profile()
   profiler.enable()

   result = transpiler.transpile(ml_code)

   profiler.disable()
   stats = pstats.Stats(profiler)
   stats.sort_stats('cumulative')
   stats.print_stats(10)

**Common Causes:**

1. **Large ML files** - Files > 10,000 lines take longer to parse
2. **Complex grammar** - Deeply nested structures slow parsing
3. **Inefficient AST traversal** - Multiple passes over AST
4. **No caching** - Re-transpiling unchanged code

**Solutions:**

1. **Split large files** into modules:

   .. code-block:: ml

      // Instead of one 10,000 line file:
      // main.ml (10,000 lines)

      // Split into modules:
      // main.ml (100 lines)
      import validators;
      import processors;
      import formatters;

2. **Enable transpilation caching**:

   .. code-block:: python

      from mlpy.ml.transpiler import MLTranspiler

      transpiler = MLTranspiler(cache_enabled=True)

      # First call: transpiles and caches
      result1 = transpiler.transpile(ml_code)  # 2500ms

      # Second call: uses cache
      result2 = transpiler.transpile(ml_code)  # 5ms

3. **Pre-transpile during build**:

   .. code-block:: python

      # build.py - Run during deployment
      from pathlib import Path
      from mlpy.ml.transpiler import MLTranspiler

      transpiler = MLTranspiler()

      for ml_file in Path('src/ml').glob('**/*.ml'):
          with open(ml_file) as f:
              ml_code = f.read()

          # Transpile and cache
          result = transpiler.transpile(ml_code)

          # Save transpiled Python
          py_file = ml_file.with_suffix('.py')
          with open(py_file, 'w') as f:
              f.write(result.python_code)

**Issue 2: Slow Execution**

**Symptom:**

.. code-block:: python

   ml_code = """
   function processLargeDataset(data) {
       result = [];
       for (i = 0; i < data.length; i = i + 1) {
           for (j = 0; j < data[i].length; j = j + 1) {
               result.push(data[i][j] * 2);
           }
       }
       return result;
   }

   result = processLargeDataset(data);
   """

   # Execution takes 5000ms for 10,000 items (too slow!)

**Diagnosis:**

.. code-block:: python

   from mlpy.integration.testing.performance import PerformanceTester

   tester = PerformanceTester()

   # Benchmark execution
   results = await tester.benchmark_async_execution(
       ml_code,
       iterations=100
   )

   print(f"Mean: {results['mean']*1000:.2f}ms")
   print(f"Median: {results['median']*1000:.2f}ms")
   print(f"Std Dev: {results['std_dev']*1000:.2f}ms")

**Common Causes:**

1. **Inefficient algorithms** - O(n²) when O(n) possible
2. **Repeated calculations** - Computing same values multiple times
3. **Large data transfers** - Passing huge datasets between Python/ML
4. **No vectorization** - Processing items one at a time

**Solutions:**

1. **Optimize algorithm complexity**:

   .. code-block:: ml

      // Bad: O(n²)
      function removeDuplicates(arr) {
          result = [];
          for (i = 0; i < arr.length; i = i + 1) {
              found = false;
              for (j = 0; j < result.length; j = j + 1) {
                  if (arr[i] == result[j]) {
                      found = true;
                      break;
                  }
              }
              if (!found) {
                  result.push(arr[i]);
              }
          }
          return result;
      }

      // Good: O(n) using object
      function removeDuplicates(arr) {
          seen = {};
          result = [];
          for (i = 0; i < arr.length; i = i + 1) {
              if (!seen[arr[i]]) {
                  seen[arr[i]] = true;
                  result.push(arr[i]);
              }
          }
          return result;
      }

2. **Cache computed values**:

   .. code-block:: ml

      // Without caching
      function fibonacci(n) {
          if (n <= 1) return n;
          return fibonacci(n - 1) + fibonacci(n - 2);
      }

      // With memoization
      fibCache = {};
      function fibonacci(n) {
          if (n <= 1) return n;

          if (fibCache[n]) {
              return fibCache[n];
          }

          result = fibonacci(n - 1) + fibonacci(n - 2);
          fibCache[n] = result;
          return result;
      }

3. **Process data in Python** (when appropriate):

   .. code-block:: python

      # Bad: Process in ML
      data = list(range(1000000))
      result = execute_ml_code_sandbox(
          "result = data.map(x => x * 2);",
          context={'data': data}
      )  # Slow!

      # Good: Process in Python
      data = list(range(1000000))
      result = [x * 2 for x in data]  # Fast!

      # Use ML only for business logic
      ml_result = execute_ml_code_sandbox(
          "function applyBusinessRule(x) { return x > threshold ? x : 0; }",
          context={'threshold': 1000}
      )

**Issue 3: Memory Leaks**

**Symptom:**

.. code-block:: python

   import psutil
   import os

   process = psutil.Process(os.getpid())

   for i in range(10000):
       result = execute_ml_code_sandbox(f"result = {i} * 2;")

       if i % 1000 == 0:
           mem = process.memory_info().rss / 1024 / 1024
           print(f"Iteration {i}: Memory = {mem:.2f} MB")

   # Output shows memory growing continuously

**Diagnosis:**

.. code-block:: python

   from memory_profiler import profile

   @profile
   def test_memory_leak():
       for i in range(1000):
           result = execute_ml_code_sandbox(f"result = {i} * 2;")

   test_memory_leak()

**Common Causes:**

1. **Accumulating contexts** - Not clearing execution contexts
2. **Circular references** - Python garbage collection issues
3. **Large cached data** - Unbounded caches
4. **Unclosed resources** - File handles, connections

**Solutions:**

1. **Clear contexts explicitly**:

   .. code-block:: python

      from mlpy.ml.transpiler import MLTranspiler

      transpiler = MLTranspiler()

      for i in range(10000):
          context = {}  # Fresh context each iteration
          transpiler.execute(f"result = {i} * 2;", context)
          result = context['result']
          # Context cleared when out of scope

2. **Use context managers**:

   .. code-block:: python

      from contextlib import contextmanager

      @contextmanager
      def ml_execution_context():
          transpiler = MLTranspiler()
          context = {}
          try:
              yield (transpiler, context)
          finally:
              # Cleanup
              context.clear()
              del transpiler

      for i in range(10000):
          with ml_execution_context() as (transpiler, context):
              transpiler.execute(f"result = {i} * 2;", context)
              result = context['result']

3. **Limit cache sizes**:

   .. code-block:: python

      from functools import lru_cache

      @lru_cache(maxsize=100)  # Limit cache to 100 entries
      def transpile_cached(ml_code_hash):
          return transpiler.transpile(ml_code)

4. **Force garbage collection** (if needed):

   .. code-block:: python

      import gc

      for i in range(10000):
          result = execute_ml_code_sandbox(f"result = {i} * 2;")

          if i % 1000 == 0:
              gc.collect()  # Force cleanup

Profiling ML Execution
-----------------------

Time Profiling
^^^^^^^^^^^^^^

**Basic Timing:**

.. code-block:: python

   import time

   def profile_ml_execution(ml_code, iterations=100):
       """Profile ML execution time."""
       times = []

       for _ in range(iterations):
           start = time.perf_counter()
           result = execute_ml_code_sandbox(ml_code)
           end = time.perf_counter()
           times.append(end - start)

       import statistics

       return {
           'mean': statistics.mean(times),
           'median': statistics.median(times),
           'min': min(times),
           'max': max(times),
           'std_dev': statistics.stdev(times) if len(times) > 1 else 0
       }

   # Usage
   stats = profile_ml_execution("result = fibonacci(20);", iterations=100)
   print(f"Mean: {stats['mean']*1000:.2f}ms")
   print(f"Std Dev: {stats['std_dev']*1000:.2f}ms")

**Detailed Profiling with cProfile:**

.. code-block:: python

   import cProfile
   import pstats
   from io import StringIO

   def profile_detailed(ml_code):
       """Detailed profiling with cProfile."""
       profiler = cProfile.Profile()
       profiler.enable()

       result = execute_ml_code_sandbox(ml_code)

       profiler.disable()

       # Capture stats
       s = StringIO()
       stats = pstats.Stats(profiler, stream=s)
       stats.sort_stats('cumulative')
       stats.print_stats(20)

       print(s.getvalue())
       return result

**Line-by-Line Profiling:**

.. code-block:: python

   from line_profiler import LineProfiler

   def profile_line_by_line():
       """Profile line by line."""
       from mlpy.ml.transpiler import MLTranspiler

       profiler = LineProfiler()

       # Add functions to profile
       profiler.add_function(MLTranspiler.transpile)
       profiler.add_function(MLTranspiler.execute)

       transpiler = MLTranspiler()

       profiler.enable()
       result = transpiler.execute(ml_code, {})
       profiler.disable()

       profiler.print_stats()

**Integration Toolkit Performance Testing:**

.. code-block:: python

   from mlpy.integration.testing.performance import PerformanceTester
   import asyncio

   async def benchmark_ml_code():
       """Comprehensive performance benchmarking."""
       tester = PerformanceTester()

       ml_code = """
       function processData(items) {
           result = [];
           for (i = 0; i < items.length; i = i + 1) {
               result.push(items[i] * 2);
           }
           return result;
       }

       result = processData(data);
       """

       # Sequential benchmark
       sequential_results = await tester.benchmark_async_execution(
           ml_code,
           iterations=100
       )

       print("Sequential Execution:")
       print(f"  Mean: {sequential_results['mean']*1000:.2f}ms")
       print(f"  Median: {sequential_results['median']*1000:.2f}ms")
       print(f"  Std Dev: {sequential_results['std_dev']*1000:.2f}ms")

       # Concurrent benchmark
       concurrent_results = await tester.benchmark_concurrent_executions(
           ml_code,
           concurrency=50
       )

       print("\nConcurrent Execution (50 concurrent):")
       print(f"  Throughput: {concurrent_results['throughput']:.2f} exec/sec")
       print(f"  Total Time: {concurrent_results['total_time']:.2f}s")
       print(f"  Avg Time: {concurrent_results['avg_per_execution']*1000:.2f}ms")

   # Run benchmark
   asyncio.run(benchmark_ml_code())

Memory Profiling
^^^^^^^^^^^^^^^^

**Basic Memory Tracking:**

.. code-block:: python

   import psutil
   import os

   def profile_memory(ml_code, iterations=1000):
       """Profile memory usage."""
       process = psutil.Process(os.getpid())

       initial_mem = process.memory_info().rss / 1024 / 1024
       print(f"Initial memory: {initial_mem:.2f} MB")

       for i in range(iterations):
           result = execute_ml_code_sandbox(ml_code)

           if i % 100 == 0:
               current_mem = process.memory_info().rss / 1024 / 1024
               delta = current_mem - initial_mem
               print(f"Iteration {i}: {current_mem:.2f} MB (+{delta:.2f} MB)")

       final_mem = process.memory_info().rss / 1024 / 1024
       print(f"Final memory: {final_mem:.2f} MB")
       print(f"Total increase: {final_mem - initial_mem:.2f} MB")

**Memory Profiler:**

.. code-block:: python

   from memory_profiler import profile

   @profile
   def memory_intensive_ml():
       """Profile memory-intensive ML operations."""
       large_data = list(range(1000000))

       result = execute_ml_code_sandbox(
           """
           function processLarge(data) {
               result = [];
               for (i = 0; i < data.length; i = i + 1) {
                   result.push(data[i] * 2);
               }
               return result;
           }

           result = processLarge(data);
           """,
           context={'data': large_data}
       )

       return result

   # Run with: python -m memory_profiler script.py

**Tracemalloc (Python built-in):**

.. code-block:: python

   import tracemalloc

   def profile_memory_allocations(ml_code):
       """Profile memory allocations with tracemalloc."""
       tracemalloc.start()

       # Take snapshot before
       snapshot1 = tracemalloc.take_snapshot()

       # Execute ML code
       for _ in range(1000):
           result = execute_ml_code_sandbox(ml_code)

       # Take snapshot after
       snapshot2 = tracemalloc.take_snapshot()

       # Compare snapshots
       top_stats = snapshot2.compare_to(snapshot1, 'lineno')

       print("Top 10 memory allocations:")
       for stat in top_stats[:10]:
           print(stat)

       tracemalloc.stop()

**Module Registry Memory Report:**

.. code-block:: python

   from mlpy.stdlib.module_registry import get_registry

   registry = get_registry()
   memory_report = registry.get_memory_report()

   print("Module Memory Usage:")
   print(f"  Python Bridge Modules: {memory_report['python_bridge_total_mb']:.2f} MB")
   print(f"  ML Source Modules: {memory_report['ml_source_total_mb']:.2f} MB")
   print(f"  Total: {memory_report['total_mb']:.2f} MB")

   print("\nPer-Module Breakdown:")
   for module_name, size_mb in memory_report['modules'].items():
       print(f"  {module_name}: {size_mb:.2f} MB")

Optimization Strategies
-----------------------

Code-Level Optimizations
^^^^^^^^^^^^^^^^^^^^^^^^

**1. Reduce Function Call Overhead:**

.. code-block:: ml

   // Bad: Many small function calls
   function processItem(item) {
       return transformItem(validateItem(normalizeItem(item)));
   }

   result = [];
   for (i = 0; i < items.length; i = i + 1) {
       result.push(processItem(items[i]));
   }

   // Good: Inline processing
   result = [];
   for (i = 0; i < items.length; i = i + 1) {
       // Normalize
       normalized = items[i].trim().toLowerCase();

       // Validate
       if (normalized.length > 0) {
           // Transform
           transformed = normalized + "_processed";
           result.push(transformed);
       }
   }

**2. Minimize Object Creation:**

.. code-block:: ml

   // Bad: Creates many temporary objects
   function processData(items) {
       return items
           .map(x => {value: x})
           .filter(obj => obj.value > 0)
           .map(obj => obj.value * 2);
   }

   // Good: Single pass with minimal objects
   function processData(items) {
       result = [];
       for (i = 0; i < items.length; i = i + 1) {
           if (items[i] > 0) {
               result.push(items[i] * 2);
           }
       }
       return result;
   }

**3. Use Efficient Data Structures:**

.. code-block:: ml

   // Bad: Array lookup - O(n)
   function contains(arr, value) {
       for (i = 0; i < arr.length; i = i + 1) {
           if (arr[i] == value) return true;
       }
       return false;
   }

   // Good: Object lookup - O(1)
   function buildLookup(arr) {
       lookup = {};
       for (i = 0; i < arr.length; i = i + 1) {
           lookup[arr[i]] = true;
       }
       return lookup;
   }

   function contains(lookup, value) {
       return lookup[value] == true;
   }

**4. Lazy Evaluation:**

.. code-block:: ml

   // Bad: Eager evaluation
   function processAll(items) {
       step1 = items.map(x => expensiveOp1(x));
       step2 = step1.map(x => expensiveOp2(x));
       step3 = step2.map(x => expensiveOp3(x));
       return step3;
   }

   // Good: Lazy evaluation
   function* processLazy(items) {
       for (i = 0; i < items.length; i = i + 1) {
           yield expensiveOp3(expensiveOp2(expensiveOp1(items[i])));
       }
   }

Caching Strategies
^^^^^^^^^^^^^^^^^^

**Transpilation Caching:**

.. code-block:: python

   from functools import lru_cache
   import hashlib

   @lru_cache(maxsize=1000)
   def transpile_cached(ml_code_hash):
       """Cache transpiled code."""
       from mlpy.ml.transpiler import MLTranspiler

       # Retrieve original code (simplified)
       ml_code = code_store.get(ml_code_hash)

       transpiler = MLTranspiler()
       return transpiler.transpile(ml_code)

   def execute_with_cache(ml_code):
       """Execute with transpilation caching."""
       # Hash the code
       code_hash = hashlib.sha256(ml_code.encode()).hexdigest()

       # Get cached transpilation
       result = transpile_cached(code_hash)

       # Execute (transpilation cached)
       context = {}
       exec(result.python_code, context)
       return context.get('result')

**Result Caching:**

.. code-block:: python

   from functools import lru_cache

   @lru_cache(maxsize=1000)
   def execute_pure_function(func_name, *args):
       """Cache results of pure ML functions."""
       ml_code = f"result = {func_name}({', '.join(map(str, args))});"
       return execute_ml_code_sandbox(ml_code)

   # Usage
   result1 = execute_pure_function('fibonacci', 20)  # Computed
   result2 = execute_pure_function('fibonacci', 20)  # Cached!

**Module Caching:**

.. code-block:: python

   from mlpy.stdlib.module_registry import get_registry

   registry = get_registry()

   # Modules are automatically cached after first load
   module1 = registry.get_module('math')  # Loads and caches
   module2 = registry.get_module('math')  # Returns cached

   # Check cache performance
   perf_summary = registry.get_performance_summary()
   print(f"Cache hit rate: {perf_summary['cache_hit_rate']:.1%}")

**Application-Level Caching:**

.. code-block:: python

   import redis
   import json

   redis_client = redis.Redis(host='localhost', port=6379)

   def execute_with_redis_cache(ml_code, ttl=3600):
       """Cache ML execution results in Redis."""
       import hashlib

       # Generate cache key
       cache_key = f"ml_result:{hashlib.sha256(ml_code.encode()).hexdigest()}"

       # Check cache
       cached = redis_client.get(cache_key)
       if cached:
           print("Cache hit!")
           return json.loads(cached)

       # Execute
       result = execute_ml_code_sandbox(ml_code)

       # Store in cache
       redis_client.setex(cache_key, ttl, json.dumps(result))

       return result

Parallel Processing
^^^^^^^^^^^^^^^^^^^

**Concurrent Execution:**

.. code-block:: python

   from mlpy.integration import AsyncMLExecutor
   import asyncio

   async def process_batch_parallel(items):
       """Process items in parallel."""
       executor = AsyncMLExecutor(max_workers=10)

       ml_code = "function process(x) { return x * 2; }"

       # Create tasks for parallel execution
       tasks = [
           executor.execute(f"{ml_code}; result = process({item});")
           for item in items
       ]

       # Execute in parallel
       results = await asyncio.gather(*tasks)

       return [r.value for r in results if r.success]

   # Usage
   items = list(range(1000))
   results = asyncio.run(process_batch_parallel(items))

**Process Pool (CPU-bound):**

.. code-block:: python

   from concurrent.futures import ProcessPoolExecutor
   from functools import partial

   def execute_ml_worker(ml_code):
       """Worker function for process pool."""
       return execute_ml_code_sandbox(ml_code)

   def process_batch_multiprocess(ml_codes, max_workers=4):
       """Process multiple ML codes using multiple processes."""
       with ProcessPoolExecutor(max_workers=max_workers) as executor:
           results = list(executor.map(execute_ml_worker, ml_codes))

       return results

   # Usage
   ml_codes = [f"result = fibonacci({i});" for i in range(100)]
   results = process_batch_multiprocess(ml_codes, max_workers=4)

**Batching:**

.. code-block:: python

   def process_in_batches(items, batch_size=100):
       """Process items in batches for better performance."""
       ml_code = """
       function processBatch(items) {
           result = [];
           for (i = 0; i < items.length; i = i + 1) {
               result.push(items[i] * 2);
           }
           return result;
       }

       result = processBatch(items);
       """

       results = []
       for i in range(0, len(items), batch_size):
           batch = items[i:i+batch_size]
           batch_result = execute_ml_code_sandbox(ml_code, context={'items': batch})
           results.extend(batch_result)

       return results

Benchmarking Tools
------------------

CLI Benchmarking
^^^^^^^^^^^^^^^^

**Using Integration Toolkit CLI:**

.. code-block:: bash

   # Basic benchmark
   $ mlpy integration benchmark mycode.ml

   # Custom iterations
   $ mlpy integration benchmark mycode.ml --iterations 1000

   # Concurrent benchmark
   $ mlpy integration benchmark mycode.ml --concurrency 50

   # With warmup
   $ mlpy integration benchmark mycode.ml --iterations 500 --warmup 20

**Output Example:**

.. code-block:: text

   +--------------------------------------+
   | Metric                    |    Value |
   |---------------------------+----------|
   | Iterations                |     1000 |
   | Mean Time                 | 25.687ms |
   | Median Time               | 25.224ms |
   | Std Deviation             |  5.168ms |
   | Min Time                  | 17.948ms |
   | Max Time                  | 44.653ms |
   | 95th Percentile           | 32.150ms |
   | 99th Percentile           | 39.800ms |
   +--------------------------------------+

Automated Benchmarking
^^^^^^^^^^^^^^^^^^^^^^

**Continuous Performance Monitoring:**

.. code-block:: python

   import time
   from dataclasses import dataclass
   from typing import List

   @dataclass
   class BenchmarkResult:
       name: str
       mean_ms: float
       median_ms: float
       min_ms: float
       max_ms: float
       std_dev_ms: float

   class BenchmarkSuite:
       """Automated benchmark suite for ML code."""

       def __init__(self):
           self.results: List[BenchmarkResult] = []

       def benchmark(self, name: str, ml_code: str, iterations: int = 100):
           """Run a benchmark."""
           times = []

           for _ in range(iterations):
               start = time.perf_counter()
               result = execute_ml_code_sandbox(ml_code)
               end = time.perf_counter()
               times.append((end - start) * 1000)  # ms

           import statistics

           result = BenchmarkResult(
               name=name,
               mean_ms=statistics.mean(times),
               median_ms=statistics.median(times),
               min_ms=min(times),
               max_ms=max(times),
               std_dev_ms=statistics.stdev(times) if len(times) > 1 else 0
           )

           self.results.append(result)
           return result

       def report(self):
           """Generate benchmark report."""
           print("=" * 70)
           print("BENCHMARK REPORT")
           print("=" * 70)

           for result in self.results:
               print(f"\n{result.name}:")
               print(f"  Mean:    {result.mean_ms:8.2f}ms")
               print(f"  Median:  {result.median_ms:8.2f}ms")
               print(f"  Min:     {result.min_ms:8.2f}ms")
               print(f"  Max:     {result.max_ms:8.2f}ms")
               print(f"  Std Dev: {result.std_dev_ms:8.2f}ms")

   # Usage
   suite = BenchmarkSuite()

   suite.benchmark("Simple arithmetic", "result = 2 + 2;")
   suite.benchmark("Fibonacci(20)", "result = fibonacci(20);")
   suite.benchmark("Array processing", """
       arr = [1, 2, 3, 4, 5];
       result = arr.map(x => x * 2);
   """)

   suite.report()

**Performance Regression Detection:**

.. code-block:: python

   import json
   from pathlib import Path

   class RegressionDetector:
       """Detect performance regressions."""

       def __init__(self, baseline_file='benchmarks.json'):
           self.baseline_file = Path(baseline_file)
           self.baseline = self.load_baseline()

       def load_baseline(self):
           """Load baseline benchmarks."""
           if self.baseline_file.exists():
               with open(self.baseline_file) as f:
                   return json.load(f)
           return {}

       def save_baseline(self):
           """Save current results as baseline."""
           with open(self.baseline_file, 'w') as f:
               json.dump(self.baseline, f, indent=2)

       def check_regression(self, name: str, current_ms: float, threshold_pct: float = 10.0):
           """Check for performance regression."""
           if name not in self.baseline:
               print(f"[NEW] {name}: {current_ms:.2f}ms (no baseline)")
               self.baseline[name] = current_ms
               return False

           baseline_ms = self.baseline[name]
           diff_pct = ((current_ms - baseline_ms) / baseline_ms) * 100

           if diff_pct > threshold_pct:
               print(f"[REGRESSION] {name}: {current_ms:.2f}ms "
                     f"(+{diff_pct:.1f}% vs baseline {baseline_ms:.2f}ms)")
               return True
           elif diff_pct < -threshold_pct:
               print(f"[IMPROVEMENT] {name}: {current_ms:.2f}ms "
                     f"({diff_pct:.1f}% vs baseline {baseline_ms:.2f}ms)")
               # Update baseline with improvement
               self.baseline[name] = current_ms
               return False
           else:
               print(f"[OK] {name}: {current_ms:.2f}ms "
                     f"({diff_pct:+.1f}% vs baseline)")
               return False

   # Usage in CI/CD
   detector = RegressionDetector()

   result = profile_ml_execution("result = fibonacci(20);")
   has_regression = detector.check_regression("fibonacci_20", result['mean'] * 1000)

   if has_regression:
       print("Performance regression detected!")
       sys.exit(1)

   detector.save_baseline()

Case Studies
------------

Case Study 1: Slow Data Processing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Problem:**

Processing 100,000 records takes 45 seconds.

.. code-block:: python

   data = load_records(100000)  # List of dicts

   ml_code = """
   function processRecord(record) {
       // Complex validation and transformation
       return transformedRecord;
   }

   result = data.map(record => processRecord(record));
   """

   # Takes 45 seconds!

**Analysis:**

1. **Profile the execution:**

   .. code-block:: python

      # Profile shows:
      # - 80% time spent in type conversion (Python ↔ ML)
      # - 15% time in ML execution
      # - 5% time in other operations

2. **Identified bottleneck:** Data marshalling overhead

**Solution:**

Process in batches to reduce marshalling overhead:

.. code-block:: python

   def process_in_batches(data, batch_size=1000):
       """Process data in batches."""
       ml_code = """
       function processBatch(records) {
           result = [];
           for (i = 0; i < records.length; i = i + 1) {
               result.push(processRecord(records[i]));
           }
           return result;
       }

       result = processBatch(records);
       """

       results = []
       for i in range(0, len(data), batch_size):
           batch = data[i:i+batch_size]
           batch_result = execute_ml_code_sandbox(
               ml_code,
               context={'records': batch}
           )
           results.extend(batch_result)

       return results

   # New execution time: 8 seconds (5.6x speedup!)

Case Study 2: Memory Leak in Long-Running Service
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Problem:**

Flask service memory grows from 100MB to 2GB over 24 hours.

.. code-block:: python

   @app.route('/process', methods=['POST'])
   def process():
       data = request.json
       result = execute_ml_code_sandbox(ml_code, context=data)
       return jsonify(result)

   # Memory grows with each request

**Analysis:**

1. **Memory profiling shows:** Contexts accumulating in transpiler

2. **Root cause:** Using global transpiler with persistent contexts

**Solution:**

Create fresh transpiler instances with explicit cleanup:

.. code-block:: python

   @app.route('/process', methods=['POST'])
   def process():
       data = request.json

       # Create fresh transpiler per request
       from mlpy.ml.transpiler import MLTranspiler
       transpiler = MLTranspiler()

       try:
           context = {}
           transpiler.execute(ml_code, context)
           result = context['result']
           return jsonify(result)
       finally:
           # Explicit cleanup
           del transpiler
           del context

   # Memory now stable at ~120MB

Case Study 3: Slow Transpilation on Cold Start
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Problem:**

First request to serverless function takes 3 seconds (transpilation overhead).

**Analysis:**

.. code-block:: python

   # Cold start breakdown:
   # - Function initialization: 0.2s
   # - ML transpilation: 2.5s
   # - Execution: 0.3s
   # Total: 3.0s

**Solution:**

Pre-transpile during container build:

.. code-block:: dockerfile

   # Dockerfile
   FROM python:3.12

   COPY requirements.txt .
   RUN pip install -r requirements.txt

   COPY ml_code/ /app/ml_code/

   # Pre-transpile ML code during build
   RUN python -c "
   from pathlib import Path
   from mlpy.ml.transpiler import MLTranspiler
   import pickle

   transpiler = MLTranspiler()

   for ml_file in Path('/app/ml_code').glob('**/*.ml'):
       with open(ml_file) as f:
           ml_code = f.read()

       # Transpile and cache
       result = transpiler.transpile(ml_code)

       # Save transpiled code
       cache_file = ml_file.with_suffix('.pyc')
       with open(cache_file, 'wb') as f:
           pickle.dump(result, f)
   "

   COPY app.py /app/
   CMD ["python", "/app/app.py"]

.. code-block:: python

   # app.py - Load pre-transpiled code
   import pickle
   from pathlib import Path

   # Load at module level (before requests)
   transpiled_cache = {}
   for cache_file in Path('/app/ml_code').glob('**/*.pyc'):
       with open(cache_file, 'rb') as f:
           transpiled_cache[cache_file.stem] = pickle.load(f)

   @app.route('/process')
   def process():
       # Use pre-transpiled code
       result = transpiled_cache['process_data']
       # Execute directly (no transpilation needed)
       # ...

   # New cold start: 0.5s (6x faster!)

Summary
-------

**Key Takeaways:**

* Profile before optimizing - identify actual bottlenecks
* Common bottlenecks: transpilation, data marshalling, inefficient algorithms
* Optimization strategies: caching, batching, parallel processing, code optimization
* Use benchmarking tools to track performance over time
* Monitor for regressions in CI/CD pipeline

**Performance Best Practices:**

1. **Measure First:** Always profile before optimizing
2. **Cache Aggressively:** Transpilation, results, modules
3. **Batch Operations:** Reduce marshalling overhead
4. **Optimize Algorithms:** O(n) beats O(n²) every time
5. **Parallel Processing:** Use async for I/O-bound, multiprocess for CPU-bound
6. **Monitor Production:** Track performance metrics continuously

**Next Steps:**

* Read :doc:`security-debugging` for security performance considerations
* See :doc:`common-issues` for specific performance issues
* Check :doc:`/integration-guide/testing/performance-testing` for testing strategies

----

**Related Documentation:**

* :doc:`/integration-guide/patterns/async-integration` - Async performance patterns
* :doc:`/integration-guide/testing/performance-testing` - Performance test suite
* :doc:`/user-guide/toolkit/cli-reference` - Benchmarking CLI commands
