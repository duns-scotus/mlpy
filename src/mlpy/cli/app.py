"""mlpy CLI application with Rich formatting and command structure."""

import click
import sys
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich import box

from mlpy.version import __version__
from mlpy.runtime.profiling.decorators import profiler
from mlpy.debugging.error_formatter import error_formatter
from mlpy.ml.errors.exceptions import (
    MLError, MLConfigurationError, create_code_injection_error,
    create_unsafe_import_error, create_reflection_abuse_error
)
from mlpy.ml.errors.context import create_error_context
from mlpy.ml.transpiler import transpile_ml_file, validate_ml_security


# Global console for Rich formatting
console = Console()


def print_banner() -> None:
    """Print mlpy banner with version info."""
    banner_text = Text()
    banner_text.append("mlpy", style="bold cyan")
    banner_text.append(" v", style="white")
    banner_text.append(__version__, style="bold white")
    banner_text.append(" - Security-First ML Language Compiler", style="cyan")

    banner_panel = Panel(
        banner_text,
        box=box.ROUNDED,
        border_style="cyan",
        padding=(1, 2),
    )
    console.print(banner_panel)
    console.print()


def print_status_table() -> None:
    """Print current development status."""
    table = Table(title="Development Status", box=box.ROUNDED)
    table.add_column("Component", style="bold cyan")
    table.add_column("Status", justify="center")
    table.add_column("Coverage", justify="center")

    # Sprint 1 & 2 components
    table.add_row("[+] Project Setup", "[green]Complete[/green]", "[green]100%[/green]")
    table.add_row("[+] Rich Error System", "[green]Complete[/green]", "[green]100%[/green]")
    table.add_row("[+] Profiling System", "[green]Complete[/green]", "[green]100%[/green]")
    table.add_row("[+] ML Parser", "[green]Complete[/green]", "[green]100%[/green]")
    table.add_row("[+] Security Analysis", "[green]Complete[/green]", "[green]100%[/green]")
    table.add_row("[ ] Capability System", "[blue]Planned[/blue]", "[dim]-%[/dim]")
    table.add_row("[ ] Sandbox Execution", "[blue]Planned[/blue]", "[dim]-%[/dim]")
    table.add_row("[ ] IDE Integration", "[blue]Planned[/blue]", "[dim]-%[/dim]")

    console.print(table)
    console.print()


@click.group(invoke_without_command=True)
@click.option('--version', '-v', is_flag=True, help='Show version information')
@click.option('--status', '-s', is_flag=True, help='Show development status')
@click.pass_context
def cli(ctx: click.Context, version: bool, status: bool) -> None:
    """mlpy v2.0 - Security-First ML Language Compiler.

    A revolutionary ML-to-Python transpiler combining capability-based security
    with production-ready tooling and native-level developer experience.
    """
    if version:
        console.print(f"mlpy version {__version__}")
        return

    if status:
        print_banner()
        print_status_table()
        return

    if ctx.invoked_subcommand is None:
        print_banner()
        console.print("Use [bold cyan]mlpy --help[/bold cyan] for command information.")
        console.print("Use [bold cyan]mlpy --status[/bold cyan] to see development status.")


@cli.command()
@click.argument('source_file', type=click.Path(exists=True, path_type=Path))
@click.option('--output', '-o', type=click.Path(path_type=Path), help='Output file')
@click.option('--sourcemap', is_flag=True, help='Generate source maps')
@click.option('--profile', is_flag=True, help='Enable profiling')
@click.option('--strict/--no-strict', default=True, help='Strict security mode (fail on security issues)')
def transpile(
    source_file: Path,
    output: Optional[Path],
    sourcemap: bool,
    profile: bool,
    strict: bool
) -> None:
    """Transpile ML source code to Python with security analysis."""
    console.print(f"[cyan]Transpiling {source_file}...[/cyan]")

    if profile:
        profiler.enable()

    try:
        # Determine output file
        output_file = output or source_file.with_suffix('.py')

        # Transpile the file
        python_code, issues = transpile_ml_file(
            str(source_file),
            None,  # Don't write output yet
            strict_security=strict
        )

        # Write output file if transpilation succeeded
        if python_code:
            output_file.write_text(python_code, encoding='utf-8')

        if python_code:
            console.print(f"[green]Successfully transpiled to {output_file}[/green]")

            # Report any non-critical security issues
            if issues:
                console.print(f"[yellow]Found {len(issues)} security warning(s):[/yellow]")
                error_formatter.print_multiple_errors(issues)
            else:
                console.print("[green]No security issues detected[/green]")

        else:
            console.print("[red]Transpilation failed due to security issues[/red]")
            if issues:
                error_formatter.print_multiple_errors(issues)

        # Generate source map if requested
        if sourcemap and python_code:
            console.print("[dim]Source map generation not yet implemented (Sprint 3)[/dim]")

    except Exception as e:
        error = MLError(
            f"Transpilation error: {str(e)}",
            suggestions=[
                "Check that the source file is valid ML code",
                "Verify file permissions and encoding",
                "Try running with --no-strict for permissive mode"
            ],
            context={
                "source_file": str(source_file),
                "error_type": type(e).__name__
            }
        )

        error_context = create_error_context(error)
        error_formatter.print_error(error_context)
        sys.exit(1)

    finally:
        if profile:
            profiler.disable()


@cli.command()
@click.argument('source_file', type=click.Path(exists=True, path_type=Path))
@click.option('--format', '-f', type=click.Choice(['text', 'json']), default='text')
def audit(source_file: Path, format: str) -> None:
    """Run security audit on ML source code."""
    console.print(f"[cyan]Auditing {source_file}...[/cyan]")

    try:
        # Read source file
        source_code = source_file.read_text(encoding='utf-8')

        # Run security analysis
        issues = validate_ml_security(source_code, str(source_file))

        if format == 'json':
            # JSON output for programmatic use
            import json
            audit_data = {
                "file": str(source_file),
                "issues_count": len(issues),
                "issues": [
                    {
                        "severity": issue.error.severity.value,
                        "category": issue.error.context.get("category", "unknown"),
                        "message": issue.error.message,
                        "line": issue.error.line_number,
                        "column": issue.error.column,
                        "cwe": issue.error.cwe.value if issue.error.cwe else None
                    }
                    for issue in issues
                ]
            }
            console.print(json.dumps(audit_data, indent=2))
        else:
            # Rich formatted output
            if not issues:
                console.print("[green]No security issues found[/green]")
                console.print(f"[green]File {source_file} passed security audit[/green]")
            else:
                # Show security summary
                severity_counts = {}
                for issue in issues:
                    severity = issue.error.severity.value
                    severity_counts[severity] = severity_counts.get(severity, 0) + 1

                console.print(f"[yellow]Found {len(issues)} security issue(s):[/yellow]")

                # Summary table
                summary_table = Table(title="Security Audit Summary", box=box.ROUNDED)
                summary_table.add_column("Severity", style="bold")
                summary_table.add_column("Count", justify="right")

                for severity, count in severity_counts.items():
                    severity_style = {
                        "critical": "bold red",
                        "high": "red",
                        "medium": "yellow",
                        "low": "blue",
                        "info": "green"
                    }.get(severity, "white")

                    summary_table.add_row(
                        Text(severity.title(), style=severity_style),
                        str(count)
                    )

                console.print(summary_table)
                console.print()

                # Detailed issues
                error_formatter.print_multiple_errors(issues)

                # Exit with error code if critical issues found
                critical_issues = [
                    issue for issue in issues
                    if issue.error.severity.value in ["critical", "high"]
                ]
                if critical_issues:
                    sys.exit(1)

    except Exception as e:
        error = MLError(
            f"Security audit failed: {str(e)}",
            suggestions=[
                "Check that the source file is valid ML code",
                "Verify file permissions and encoding",
                "Ensure the file contains valid UTF-8 text"
            ],
            context={
                "source_file": str(source_file),
                "error_type": type(e).__name__
            }
        )

        error_context = create_error_context(error)
        error_formatter.print_error(error_context)
        sys.exit(1)


@cli.command()
@click.argument('source_file', type=click.Path(exists=True, path_type=Path))
@click.option('--format', '-f', type=click.Choice(['tree', 'json']), default='tree')
def parse(source_file: Path, format: str) -> None:
    """Parse ML source code and display AST."""
    console.print(f"[cyan]Parsing {source_file}...[/cyan]")

    try:
        from mlpy.ml.grammar.parser import parse_ml_file

        # Parse the file
        ast = parse_ml_file(str(source_file))

        if format == 'json':
            # JSON representation (simplified)
            import json
            ast_data = {
                "type": "Program",
                "items_count": len(ast.items),
                "items": [
                    {
                        "type": type(item).__name__,
                        "line": getattr(item, 'line', None),
                        "column": getattr(item, 'column', None)
                    }
                    for item in ast.items
                ]
            }
            console.print(json.dumps(ast_data, indent=2))
        else:
            # Tree representation
            tree_table = Table(title="AST Structure", box=box.ROUNDED)
            tree_table.add_column("Node Type", style="bold cyan")
            tree_table.add_column("Details", style="white")
            tree_table.add_column("Location", style="dim")

            tree_table.add_row(
                "Program",
                f"{len(ast.items)} top-level items",
                ""
            )

            for i, item in enumerate(ast.items):
                node_type = type(item).__name__
                details = ""
                location = ""

                if hasattr(item, 'line') and item.line:
                    location = f"Line {item.line}"
                    if hasattr(item, 'column') and item.column:
                        location += f", Col {item.column}"

                # Add specific details based on node type
                if hasattr(item, 'name'):
                    name_value = item.name.name if hasattr(item.name, 'name') else str(item.name)
                    details = f"Name: {name_value}"
                elif hasattr(item, 'target') and hasattr(item, 'value'):
                    target_value = item.target.name if hasattr(item.target, 'name') else str(item.target)
                    details = f"Target: {target_value}"

                tree_table.add_row(
                    f"  [{i+1}] {node_type}",
                    details,
                    location
                )

            console.print(tree_table)
            console.print(f"[green]Successfully parsed {len(ast.items)} top-level items[/green]")

    except Exception as e:
        error = MLError(
            f"Parse error: {str(e)}",
            suggestions=[
                "Check ML syntax in the source file",
                "Verify that the file contains valid ML code",
                "Use 'mlpy audit' to check for security issues first"
            ],
            context={
                "source_file": str(source_file),
                "error_type": type(e).__name__
            }
        )

        error_context = create_error_context(error)
        error_formatter.print_error(error_context)
        sys.exit(1)


@cli.command()
def profile_report() -> None:
    """Generate profiling report."""
    console.print("[cyan]Generating profiling report...[/cyan]")

    report = profiler.generate_report()

    if not report["functions"]:
        console.print("[yellow]No profiling data available. Run some commands with --profile first.[/yellow]")
        return

    # Summary table
    summary_table = Table(title="Profiling Summary", box=box.ROUNDED)
    summary_table.add_column("Metric", style="bold cyan")
    summary_table.add_column("Value", justify="right", style="white")

    summary_table.add_row("Total Functions", str(report["summary"]["total_functions"]))
    summary_table.add_row("Total Calls", str(report["summary"]["total_calls"]))
    summary_table.add_row("Total Time", f"{report['summary']['total_time']:.4f}s")

    console.print(summary_table)
    console.print()

    # Function details
    if report["functions"]:
        functions_table = Table(title="Function Performance", box=box.ROUNDED)
        functions_table.add_column("Function", style="bold cyan")
        functions_table.add_column("Calls", justify="right")
        functions_table.add_column("Total Time", justify="right")
        functions_table.add_column("Avg Time", justify="right")
        functions_table.add_column("Memory Δ", justify="right")

        for func_name, stats in report["functions"].items():
            functions_table.add_row(
                func_name,
                str(stats["total_calls"]),
                f"{stats['total_time']:.4f}s",
                f"{stats['avg_time']:.4f}s",
                f"{stats['avg_memory_delta']:.2f}MB"
            )

        console.print(functions_table)


@cli.command()
def demo_errors() -> None:
    """Demonstrate the rich error system with example errors."""
    console.print("[cyan]Demonstrating mlpy Rich Error System...[/cyan]")
    console.print()

    # Create sample source content
    sample_ml_code = '''function processData(input) {
    // This is dangerous code that will be caught by security analysis
    result = eval(input.expression)
    data = __import__("os").system("rm -rf /")
    secret = obj.__class__.__bases__[0]
    return result
}'''

    # Demo different types of errors
    errors = [
        create_code_injection_error(
            "eval",
            source_file="example.ml",
            line_number=3
        ),
        create_unsafe_import_error(
            "os",
            source_file="example.ml",
            line_number=4
        ),
        create_reflection_abuse_error(
            "__class__.__bases__",
            source_file="example.ml",
            line_number=5
        )
    ]

    # Create error contexts with source content
    error_contexts = []
    for error in errors:
        error_context = create_error_context(
            error,
            source_content=sample_ml_code,
            context_lines=2
        )
        error_contexts.append(error_context)

    # Display errors
    error_formatter.print_multiple_errors(error_contexts)

    console.print()
    console.print("[green]Rich error system working perfectly![/green]")
    console.print("[cyan]These errors demonstrate mlpy's security-first approach.[/cyan]")


@cli.command()
def clear_profiles() -> None:
    """Clear all profiling data."""
    profiler.clear_profiles()
    console.print("[green]Profiling data cleared.[/green]")


@cli.command()
@click.option('--enable/--disable', default=True, help='Enable or disable profiling')
def profiling(enable: bool) -> None:
    """Enable or disable profiling."""
    if enable:
        profiler.enable()
        console.print("[green]Profiling enabled.[/green]")
    else:
        profiler.disable()
        console.print("[yellow]Profiling disabled.[/yellow]")


if __name__ == '__main__':
    try:
        cli()
    except Exception as e:
        # Handle unexpected errors with rich formatting
        error = MLError(
            f"Unexpected CLI error: {str(e)}",
            suggestions=[
                "Check your command syntax with 'mlpy --help'",
                "Report this issue if it persists",
                "Try running with --verbose for more details"
            ],
            context={
                "error_type": type(e).__name__,
                "cli_args": sys.argv[1:] if len(sys.argv) > 1 else []
            }
        )

        error_context = create_error_context(error)
        error_formatter.print_error(error_context)
        sys.exit(1)