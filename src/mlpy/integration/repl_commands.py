"""Integration Toolkit REPL commands.

Provides specialized REPL commands for integration development and testing:
- .async - Run async ML code in REPL
- .callback - Create Python callbacks from ML functions
- .benchmark - Run performance benchmarks

These commands are designed to be integrated into the main ML REPL for
enhanced development and testing workflows.
"""

import asyncio
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mlpy.cli.repl import MLREPLSession


def handle_async_command(session: "MLREPLSession", ml_code: str) -> None:
    """Execute ML code asynchronously and display results.

    This command allows testing async ML execution directly in the REPL,
    useful for integration testing and debugging async workflows.

    Args:
        session: Current REPL session
        ml_code: ML code to execute asynchronously

    Example:
        ml> .async result = calculate_long_running_task();
        Executing async...
        => 42
        Execution time: 1.234s
    """
    from mlpy.integration.async_executor import async_ml_execute

    if not ml_code:
        print("Usage: .async <ml_code>")
        print("Example: .async result = heavy_computation();")
        return

    print("Executing async...")
    start = time.perf_counter()

    # Run async execution
    try:
        result = asyncio.run(async_ml_execute(ml_code, timeout=30.0))

        end = time.perf_counter()
        execution_time = end - start

        if result.success:
            if result.value is not None:
                print(f"=> {result.value}")
            print(f"Execution time: {execution_time:.3f}s")
            if hasattr(result, "transpile_time") and result.transpile_time:
                print(f"Transpile time: {result.transpile_time:.3f}s")
        else:
            print(f"Error: {result.error}")
            print(f"Execution time: {execution_time:.3f}s")

    except asyncio.TimeoutError:
        print("Error: Async execution timed out (30s limit)")
    except Exception as e:
        print(f"Error: {e}")


def handle_callback_command(session: "MLREPLSession", function_name: str) -> None:
    """Create a Python callback from an ML function.

    This command creates a Python callable that wraps an ML function,
    allowing it to be called from Python code with automatic type conversion.

    The callback is stored in the REPL namespace for immediate use.

    Args:
        session: Current REPL session
        function_name: Name of ML function to wrap

    Example:
        ml> function double(x) { return x * 2; }
        ml> .callback double
        Callback 'double' created successfully!
        You can now call it from Python: double(5)

        ml> .py print(double(21))
        42
    """
    from mlpy.integration.ml_callback import ml_callback

    if not function_name:
        print("Usage: .callback <function_name>")
        print("Example: .callback calculate_total")
        return

    # Check if function exists in session namespace
    if function_name not in session.python_namespace:
        print(f"Error: Function '{function_name}' not found")
        print("Define the function first, then create a callback")
        print(f"\nExample:")
        print(f"  ml> function {function_name}(x) {{ return x * 2; }}")
        print(f"  ml> .callback {function_name}")
        return

    try:
        # Create callback wrapper
        callback = ml_callback(session, function_name)

        # Store callback in namespace with _callback suffix
        callback_name = f"{function_name}_callback"
        session.python_namespace[callback_name] = callback

        print(f"Callback '{callback_name}' created successfully!")
        print(f"Usage: {callback_name}(arg1, arg2, ...)")
        print(f"\nYou can also use it in Python code:")
        print(f"  result = {callback_name}(42)")

    except Exception as e:
        print(f"Error creating callback: {e}")


def handle_benchmark_command(session: "MLREPLSession", ml_code: str, iterations_str: str = "") -> None:
    """Run performance benchmark on ML code.

    This command executes ML code multiple times and provides statistical
    performance metrics (mean, median, std dev, min, max).

    Args:
        session: Current REPL session
        ml_code: ML code to benchmark
        iterations_str: Number of iterations (default: 100)

    Example:
        ml> .benchmark result = fibonacci(20);
        Running benchmark (100 iterations)...
        Mean:   12.5ms
        Median: 12.3ms
        Std Dev: 0.8ms
        Min:    11.2ms
        Max:    15.1ms

        ml> .benchmark result = fibonacci(20); 50
        Running benchmark (50 iterations)...
        ...
    """
    from mlpy.integration.testing import PerformanceTester

    if not ml_code:
        print("Usage: .benchmark <ml_code> [iterations]")
        print("Example: .benchmark result = calculate(100);")
        print("Example: .benchmark result = calculate(100); 50")
        return

    # Parse iterations
    try:
        iterations = int(iterations_str) if iterations_str else 100
        if iterations < 1:
            print("Error: Iterations must be >= 1")
            return
    except ValueError:
        print(f"Error: Invalid iterations value: {iterations_str}")
        return

    print(f"Running benchmark ({iterations} iterations)...")

    tester = PerformanceTester()

    try:
        # Run benchmark
        results = asyncio.run(
            tester.benchmark_async_execution(ml_code, iterations=iterations)
        )

        # Display results
        print(f"\nBenchmark Results:")
        print(f"  Mean:   {results['mean'] * 1000:.2f}ms")
        print(f"  Median: {results['median'] * 1000:.2f}ms")
        print(f"  Std Dev: {results['std_dev'] * 1000:.2f}ms")
        print(f"  Min:    {results['min'] * 1000:.2f}ms")
        print(f"  Max:    {results['max'] * 1000:.2f}ms")

        # Calculate coefficient of variation
        if results["mean"] > 0:
            cv = (results["std_dev"] / results["mean"]) * 100
            print(f"  CV:     {cv:.1f}%")

        print(f"\n  Total iterations: {iterations}")
        print(f"  Successful: {iterations}")

    except asyncio.TimeoutError:
        print("Error: Benchmark timed out")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


def print_integration_help():
    """Print help for Integration Toolkit REPL commands."""
    print(
        """
Integration Toolkit Commands:
  .async <code>            Execute ML code asynchronously
  .callback <function>     Create Python callback from ML function
  .benchmark <code> [N]    Benchmark ML code (default: 100 iterations)

Examples:
  ml> .async result = fetch_data();
  Executing async...
  => {"status": "success"}
  Execution time: 0.123s

  ml> function double(x) { return x * 2; }
  ml> .callback double
  Callback 'double_callback' created successfully!

  ml> .benchmark result = fibonacci(20);
  Running benchmark (100 iterations)...
  Mean: 12.5ms

  ml> .benchmark result = fibonacci(20); 50
  Running benchmark (50 iterations)...
  Mean: 12.3ms

Use .help to see all available commands.
"""
    )


# Command registry for integration commands
INTEGRATION_COMMANDS = {
    "async": handle_async_command,
    "callback": handle_callback_command,
    "benchmark": handle_benchmark_command,
}


def dispatch_integration_command(session: "MLREPLSession", command_line: str) -> bool:
    """Dispatch an integration command.

    Args:
        session: Current REPL session
        command_line: Full command line (including .)

    Returns:
        True if command was handled, False if unknown

    Example:
        >>> dispatch_integration_command(session, ".async result = 42;")
        True
        >>> dispatch_integration_command(session, ".unknown")
        False
    """
    if not command_line.startswith("."):
        return False

    # Parse command and arguments
    parts = command_line[1:].strip().split(None, 1)
    if not parts:
        return False

    command = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""

    # Handle special cases where args need parsing
    if command == "benchmark" and ";" in args:
        # Parse: .benchmark code; iterations
        code_part, iterations_part = args.rsplit(";", 1)
        code = code_part.strip()
        iterations = iterations_part.strip()
        INTEGRATION_COMMANDS["benchmark"](session, code, iterations)
        return True

    elif command in INTEGRATION_COMMANDS:
        INTEGRATION_COMMANDS[command](session, args)
        return True

    return False
