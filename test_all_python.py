#!/usr/bin/env python3
"""
Test all generated Python files to identify execution errors.
"""

import os
import subprocess
from pathlib import Path
import time

def main():
    # Directory containing transpiled Python files
    transpiled_dir = Path("transpiled_tests")

    # Find all .py files
    py_files = list(transpiled_dir.glob("*.py"))

    print(f"Found {len(py_files)} Python files to test")
    print("=" * 80)

    successful_executions = []
    failed_executions = []

    for i, py_file in enumerate(py_files, 1):
        print(f"[{i:2d}/{len(py_files)}] Testing {py_file.name}...")

        try:
            # Run the Python file
            result = subprocess.run([
                "python", str(py_file)
            ], capture_output=True, text=True, timeout=10, cwd=str(Path.cwd()))

            if result.returncode == 0:
                print(f"    SUCCESS: Executed without errors")
                print(f"    Output: {result.stdout[:100]}..." if result.stdout else "    Output: (no output)")
                successful_executions.append((py_file, result.stdout))
            else:
                print(f"    FAILED: Exit code {result.returncode}")
                error_msg = result.stderr.strip()
                print(f"    Error: {error_msg[:200]}..." if len(error_msg) > 200 else f"    Error: {error_msg}")
                failed_executions.append((py_file, error_msg))

        except subprocess.TimeoutExpired:
            print(f"    TIMEOUT: Execution took longer than 10 seconds")
            failed_executions.append((py_file, "Timeout"))
        except Exception as e:
            print(f"    EXCEPTION: {e}")
            failed_executions.append((py_file, str(e)))

        print()

    # Summary
    print("\n" + "=" * 80)
    print("EXECUTION SUMMARY")
    print("=" * 80)
    print(f"Total files: {len(py_files)}")
    print(f"Successful: {len(successful_executions)}")
    print(f"Failed: {len(failed_executions)}")
    print(f"Success rate: {len(successful_executions)/len(py_files)*100:.1f}%")

    if failed_executions:
        print(f"\nFAILED EXECUTIONS:")
        print("-" * 60)
        for py_file, error in failed_executions:
            print(f"\n{py_file.name}:")
            print(f"  Error: {error}")

    if successful_executions:
        print(f"\nSUCCESSFUL EXECUTIONS:")
        print("-" * 60)
        for py_file, output in successful_executions:
            print(f"{py_file.name}: OK")

    # Analyze common error patterns
    if failed_executions:
        print(f"\nERROR PATTERN ANALYSIS:")
        print("-" * 60)

        error_patterns = {}
        for py_file, error in failed_executions:
            # Extract key error types
            if "list assignment index out of range" in error:
                error_patterns.setdefault("Array Index Assignment", []).append(py_file.name)
            elif "ImportError" in error or "ModuleNotFoundError" in error:
                error_patterns.setdefault("Import Errors", []).append(py_file.name)
            elif "AttributeError" in error:
                error_patterns.setdefault("Attribute Errors", []).append(py_file.name)
            elif "NameError" in error:
                error_patterns.setdefault("Name Errors", []).append(py_file.name)
            elif "TypeError" in error:
                error_patterns.setdefault("Type Errors", []).append(py_file.name)
            elif "SyntaxError" in error:
                error_patterns.setdefault("Syntax Errors", []).append(py_file.name)
            else:
                error_patterns.setdefault("Other Errors", []).append(py_file.name)

        for pattern, files in error_patterns.items():
            print(f"\n{pattern} ({len(files)} files):")
            for file in files:
                print(f"  - {file}")

    return successful_executions, failed_executions

if __name__ == "__main__":
    successful, failed = main()