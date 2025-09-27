#!/usr/bin/env python3
"""
Transpile all ML test files and analyze the results.
"""

import os
import subprocess
from pathlib import Path
import time

def main():
    # Directory containing ML test files
    test_dir = Path("tests/ml_integration/language_coverage")
    output_dir = Path("transpiled_tests")

    # Create output directory
    output_dir.mkdir(exist_ok=True)

    # Find all .ml files
    ml_files = list(test_dir.glob("*.ml"))

    print(f"Found {len(ml_files)} ML files to transpile")
    print("=" * 60)

    successful_transpilations = []
    failed_transpilations = []

    for i, ml_file in enumerate(ml_files, 1):
        print(f"[{i:2d}/{len(ml_files)}] Transpiling {ml_file.name}...")

        # Output Python file
        py_file = output_dir / f"{ml_file.stem}.py"

        try:
            # Run mlpy transpile command
            result = subprocess.run([
                "mlpy", "transpile", str(ml_file), "-o", str(py_file)
            ], capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                print(f"    SUCCESS: {py_file}")
                successful_transpilations.append((ml_file, py_file))
            else:
                print(f"    FAILED: {result.stderr.strip()}")
                failed_transpilations.append((ml_file, result.stderr.strip()))

        except subprocess.TimeoutExpired:
            print(f"    TIMEOUT: Transpilation took longer than 30 seconds")
            failed_transpilations.append((ml_file, "Timeout"))
        except Exception as e:
            print(f"    EXCEPTION: {e}")
            failed_transpilations.append((ml_file, str(e)))

    # Summary
    print("\n" + "=" * 60)
    print("TRANSPILATION SUMMARY")
    print("=" * 60)
    print(f"Total files: {len(ml_files)}")
    print(f"Successful: {len(successful_transpilations)}")
    print(f"Failed: {len(failed_transpilations)}")
    print(f"Success rate: {len(successful_transpilations)/len(ml_files)*100:.1f}%")

    if failed_transpilations:
        print(f"\nFAILED TRANSPILATIONS:")
        for ml_file, error in failed_transpilations:
            print(f"  {ml_file.name}: {error}")

    if successful_transpilations:
        print(f"\nSUCCESSFUL TRANSPILATIONS:")
        for ml_file, py_file in successful_transpilations:
            print(f"  {ml_file.name} → {py_file}")

    return successful_transpilations, failed_transpilations

if __name__ == "__main__":
    successful, failed = main()