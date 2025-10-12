#!/usr/bin/env python3
"""Benchmark parsing performance with and without compiled grammar.

This script measures the cold-start parsing overhead difference between
using the pre-compiled grammar vs. compiling from .lark file.
"""

import time
from pathlib import Path

def benchmark_without_compiled():
    """Benchmark parsing without compiled grammar."""
    # Temporarily rename compiled grammar if it exists
    grammar_dir = Path(__file__).parent.parent / "src" / "mlpy" / "ml" / "grammar"
    compiled_path = grammar_dir / "ml_parser.compiled"
    backup_path = grammar_dir / "ml_parser.compiled.backup"

    # Backup compiled grammar
    if compiled_path.exists():
        compiled_path.rename(backup_path)

    try:
        # Force reimport to reload parser without compiled grammar
        import sys
        if 'mlpy.ml.grammar.parser' in sys.modules:
            del sys.modules['mlpy.ml.grammar.parser']
        if 'mlpy.ml.grammar.ast_nodes' in sys.modules:
            del sys.modules['mlpy.ml.grammar.ast_nodes']

        # Import and time parsing
        start = time.perf_counter()
        from mlpy.ml.grammar.parser import MLParser
        parser = MLParser()

        # Parse a simple program to trigger parser initialization
        code = """
        function fibonacci(n) {
            if (n <= 1) {
                return n;
            }
            return fibonacci(n - 1) + fibonacci(n - 2);
        }
        """
        parser.parse(code)
        elapsed = time.perf_counter() - start

        return elapsed

    finally:
        # Restore compiled grammar
        if backup_path.exists():
            backup_path.rename(compiled_path)


def benchmark_with_compiled():
    """Benchmark parsing with compiled grammar."""
    import sys
    # Force reimport to reload parser with compiled grammar
    if 'mlpy.ml.grammar.parser' in sys.modules:
        del sys.modules['mlpy.ml.grammar.parser']
    if 'mlpy.ml.grammar.ast_nodes' in sys.modules:
        del sys.modules['mlpy.ml.grammar.ast_nodes']

    # Import and time parsing
    start = time.perf_counter()
    from mlpy.ml.grammar.parser import MLParser
    parser = MLParser()

    # Parse the same program
    code = """
    function fibonacci(n) {
        if (n <= 1) {
            return n;
        }
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
    """
    parser.parse(code)
    elapsed = time.perf_counter() - start

    return elapsed


def main():
    """Run benchmark comparison."""
    print("=" * 60)
    print("Parser Cold-Start Performance Benchmark")
    print("=" * 60)
    print()

    # Check if compiled grammar exists
    grammar_dir = Path(__file__).parent.parent / "src" / "mlpy" / "ml" / "grammar"
    compiled_path = grammar_dir / "ml_parser.compiled"

    if not compiled_path.exists():
        print("[-] Compiled grammar not found!")
        print(f"    Run: python -m scripts.compile_grammar")
        return 1

    print("[*] Benchmarking WITHOUT compiled grammar (from .lark)...")
    time_without = benchmark_without_compiled()
    print(f"    Time: {time_without*1000:.1f} ms")
    print()

    print("[*] Benchmarking WITH compiled grammar...")
    time_with = benchmark_with_compiled()
    print(f"    Time: {time_with*1000:.1f} ms")
    print()

    # Calculate speedup
    speedup = time_without / time_with
    reduction = ((time_without - time_with) / time_without) * 100

    print("=" * 60)
    print("Results:")
    print("=" * 60)
    print(f"  Without compiled grammar:  {time_without*1000:>7.1f} ms")
    print(f"  With compiled grammar:     {time_with*1000:>7.1f} ms")
    print(f"  Speedup:                   {speedup:>7.2f}x faster")
    print(f"  Time saved:                {(time_without - time_with)*1000:>7.1f} ms ({reduction:.1f}% reduction)")
    print()

    if speedup >= 2.0:
        print("[+] SUCCESS: Compiled grammar provides significant speedup!")
    elif speedup >= 1.3:
        print("[+] GOOD: Compiled grammar provides moderate speedup")
    else:
        print("[!] WARNING: Speedup lower than expected")

    print()
    print("Note: This measures cold-start parser initialization only.")
    print("      The transpilation cache already eliminates re-parsing on warm starts.")

    return 0


if __name__ == "__main__":
    exit(main())
