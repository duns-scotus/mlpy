"""CLI commands for Integration Toolkit.

Provides command-line interface for validating and benchmarking ML integration.
"""

import asyncio
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

console = Console()


@click.group()
def integration():
    """Integration Toolkit commands for validation and benchmarking."""
    pass


@integration.command()
def validate():
    """Validate Integration Toolkit setup.

    Checks that all Integration Toolkit components are properly configured:
    - Module registry availability
    - Async executor readiness
    - Capability manager initialization

    Example:
        $ mlpy integration validate
    """
    console.print(Panel.fit(
        "[bold cyan]Validating Integration Toolkit...[/bold cyan]",
        border_style="cyan"
    ))

    all_valid = True
    results = []

    # Check 1: Module registry
    try:
        from mlpy.stdlib.module_registry import get_registry

        registry = get_registry()
        modules_dict = registry.get_all_modules()
        modules = list(modules_dict.values())

        # Count module types
        python_count = sum(1 for m in modules if m.module_type == "python_bridge")
        ml_count = sum(1 for m in modules if m.module_type == "ml_source")

        results.append({
            "component": "Module Registry",
            "status": "[OK] Ready",
            "details": f"{len(modules)} modules ({python_count} Python, {ml_count} ML)"
        })
    except Exception as e:
        results.append({
            "component": "Module Registry",
            "status": "[FAIL] Error",
            "details": str(e)
        })
        all_valid = False

    # Check 2: Async executor
    try:
        from mlpy.integration.async_executor import AsyncMLExecutor

        # Test instantiation
        executor = AsyncMLExecutor(max_workers=1)

        results.append({
            "component": "Async Executor",
            "status": "[OK] Ready",
            "details": "Thread pool initialized"
        })
    except Exception as e:
        results.append({
            "component": "Async Executor",
            "status": "[FAIL] Error",
            "details": str(e)
        })
        all_valid = False

    # Check 3: Capability manager
    try:
        from mlpy.runtime.capabilities.manager import get_capability_manager

        cap_manager = get_capability_manager()

        results.append({
            "component": "Capability Manager",
            "status": "[OK] Ready",
            "details": "Security system operational"
        })
    except Exception as e:
        results.append({
            "component": "Capability Manager",
            "status": "[FAIL] Error",
            "details": str(e)
        })
        all_valid = False

    # Check 4: ML Callback system
    try:
        from mlpy.integration.ml_callback import MLCallbackWrapper, MLCallbackRegistry

        results.append({
            "component": "Callback System",
            "status": "[OK] Ready",
            "details": "ML callbacks available"
        })
    except Exception as e:
        results.append({
            "component": "Callback System",
            "status": "[FAIL] Error",
            "details": str(e)
        })
        all_valid = False

    # Display results in a table
    table = Table(show_header=True, header_style="bold magenta", border_style="cyan")
    table.add_column("Component", style="cyan", width=20)
    table.add_column("Status", width=12)
    table.add_column("Details", style="dim")

    for result in results:
        status_style = "green" if "[OK]" in result["status"] else "red bold"
        table.add_row(
            result["component"],
            Text(result["status"], style=status_style),
            result["details"]
        )

    console.print(table)
    console.print()

    # Final verdict
    if all_valid:
        console.print(Panel.fit(
            "[bold green][OK] Integration Toolkit is properly configured![/bold green]",
            border_style="green"
        ))
        raise SystemExit(0)
    else:
        console.print(Panel.fit(
            "[bold red][FAIL] Integration Toolkit has configuration issues[/bold red]\n"
            "[yellow]Please check the error messages above[/yellow]",
            border_style="red"
        ))
        raise SystemExit(1)


@integration.command()
@click.argument('ml_file', type=click.Path(exists=True))
@click.option('--iterations', type=int, default=100, help='Number of iterations for benchmarking')
@click.option('--concurrency', type=int, default=1, help='Number of concurrent executions (async mode)')
@click.option('--warmup', type=int, default=10, help='Number of warmup iterations')
def benchmark(ml_file: str, iterations: int, concurrency: int, warmup: int):
    """Benchmark ML file execution performance.

    Measures transpilation and execution performance of ML code with
    statistical analysis. Supports both sequential and concurrent execution.

    Arguments:
        ML_FILE: Path to the .ml file to benchmark

    Options:
        --iterations N: Number of benchmark iterations (default: 100)
        --concurrency N: Concurrent executions for async mode (default: 1)
        --warmup N: Number of warmup iterations (default: 10)

    Examples:
        # Basic benchmark
        $ mlpy integration benchmark process_data.ml

        # High iteration count for precise timing
        $ mlpy integration benchmark process_data.ml --iterations 1000

        # Concurrent execution benchmark
        $ mlpy integration benchmark process_data.ml --concurrency 50
    """
    from mlpy.integration.testing.performance import PerformanceTester

    ml_path = Path(ml_file)

    console.print(Panel.fit(
        f"[bold cyan]Benchmarking ML File:[/bold cyan] {ml_path.name}",
        border_style="cyan"
    ))

    # Read ML code
    try:
        with open(ml_path, 'r', encoding='utf-8') as f:
            ml_code = f.read()
    except Exception as e:
        console.print(f"[bold red]Error reading file:[/bold red] {e}")
        raise SystemExit(1)

    # Create performance tester
    tester = PerformanceTester()

    # Run benchmark based on mode
    try:
        if concurrency > 1:
            # Concurrent benchmark
            console.print(f"\n[yellow]Running concurrent benchmark "
                         f"(concurrency={concurrency})...[/yellow]\n")

            results = asyncio.run(tester.benchmark_concurrent_executions(
                ml_code,
                concurrency=concurrency
            ))

            # Display concurrent results
            table = Table(show_header=True, header_style="bold magenta", border_style="cyan")
            table.add_column("Metric", style="cyan", width=25)
            table.add_column("Value", style="green bold", justify="right")

            table.add_row("Concurrent Executions", str(concurrency))
            table.add_row("Total Time", f"{results['total_time']:.3f}s")
            table.add_row("Throughput", f"{results['throughput']:.2f} exec/sec")
            table.add_row("Avg Execution Time", f"{results['avg_per_execution']*1000:.3f}ms")

            if 'errors' in results and results['errors'] > 0:
                table.add_row("Errors", f"[red]{results['errors']}[/red]")

            console.print(table)

        else:
            # Sequential benchmark with warmup
            if warmup > 0:
                console.print(f"[yellow]Running warmup ({warmup} iterations)...[/yellow]")
                asyncio.run(tester.benchmark_async_execution(ml_code, iterations=warmup))

            console.print(f"[yellow]Running benchmark ({iterations} iterations)...[/yellow]\n")

            results = asyncio.run(tester.benchmark_async_execution(
                ml_code,
                iterations=iterations
            ))

            # Display sequential results with statistics
            table = Table(show_header=True, header_style="bold magenta", border_style="cyan")
            table.add_column("Metric", style="cyan", width=25)
            table.add_column("Value", style="green bold", justify="right")

            table.add_row("Iterations", str(iterations))
            table.add_row("Mean Time", f"{results['mean']*1000:.3f}ms")
            table.add_row("Median Time", f"{results['median']*1000:.3f}ms")
            table.add_row("Std Deviation", f"{results['std_dev']*1000:.3f}ms")
            table.add_row("Min Time", f"{results['min']*1000:.3f}ms")
            table.add_row("Max Time", f"{results['max']*1000:.3f}ms")

            # Calculate percentiles if available
            if 'percentiles' in results:
                p95 = results['percentiles'].get('p95', 0) * 1000
                p99 = results['percentiles'].get('p99', 0) * 1000
                table.add_row("95th Percentile", f"{p95:.3f}ms")
                table.add_row("99th Percentile", f"{p99:.3f}ms")

            console.print(table)

        console.print()
        console.print(Panel.fit(
            "[bold green][OK] Benchmark completed successfully[/bold green]",
            border_style="green"
        ))

    except Exception as e:
        console.print(f"\n[bold red]Benchmark failed:[/bold red] {e}")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        raise SystemExit(1)


# Export the group for CLI integration
__all__ = ["integration"]
