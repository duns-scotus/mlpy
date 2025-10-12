#!/usr/bin/env python3
"""Compile ML grammar to optimize cold-start parsing performance.

This script pre-compiles the Lark grammar to eliminate the expensive
compute_includes_lookback phase that takes 800ms on every cold start.

Usage:
    python -m scripts.compile_grammar

Output:
    src/mlpy/ml/grammar/ml_parser.compiled
"""

from pathlib import Path
from lark import Lark

def main():
    """Compile the ML grammar and save it."""
    # Locate grammar file
    project_root = Path(__file__).parent.parent
    grammar_path = project_root / "src" / "mlpy" / "ml" / "grammar" / "ml.lark"
    output_path = project_root / "src" / "mlpy" / "ml" / "grammar" / "ml_parser.compiled"

    if not grammar_path.exists():
        print(f"[-] Grammar file not found: {grammar_path}")
        return 1

    print(f"[*] Compiling grammar: {grammar_path}")

    # Load and compile grammar with same settings as runtime
    parser = Lark.open(
        grammar_path,
        parser="lalr",              # Fast LALR(1) parser
        propagate_positions=True,   # For error reporting and source maps
        maybe_placeholders=False,   # Strict parsing
        debug=False,                # Production mode
    )

    # Save compiled parser
    print(f"[*] Saving compiled parser: {output_path}")
    with output_path.open('wb') as f:
        parser.save(f)

    # Verify it loads correctly
    print("[*] Verifying compiled parser...")
    with output_path.open('rb') as f:
        test_parser = Lark.load(f)

    # Test with simple ML code
    test_code = '''
    function test(x) {
        return x + 1;
    }
    '''
    try:
        test_parser.parse(test_code)
        print("[+] Compiled parser works correctly!")
    except Exception as e:
        print(f"[-] Compiled parser verification failed: {e}")
        return 1

    # Show file size
    size_kb = output_path.stat().st_size / 1024
    print(f"[*] Compiled parser size: {size_kb:.1f} KB")
    print()
    print("[+] Grammar compilation complete!")
    print(f"    Expected speedup: 60-80% faster cold-start parsing")
    print(f"    (Eliminates 800ms compute_includes_lookback overhead)")

    return 0

if __name__ == "__main__":
    exit(main())
