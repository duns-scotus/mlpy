#!/usr/bin/env python3
"""
Compare transpilation outputs between CLI and ml_test_runner methods.
"""

from mlpy.ml.transpiler import MLTranspiler, execute_ml_code_sandbox, transpile_ml_file
from pathlib import Path

def main():
    # Test file
    test_file = "tests/ml_integration/language_coverage/comprehensive_mathematical_operations.ml"

    print("=" * 80)
    print("TRANSPILER METHOD COMPARISON")
    print("=" * 80)

    # Read source
    source_code = Path(test_file).read_text(encoding='utf-8')
    print(f"Source file: {test_file}")
    print(f"Source length: {len(source_code)} characters")
    print()

    # Method 1: MLTranspiler.transpile_to_python (used by ml_test_runner)
    print("METHOD 1: MLTranspiler.transpile_to_python() [ml_test_runner method]")
    print("-" * 60)
    try:
        transpiler = MLTranspiler()
        python_code1, issues1, source_map1 = transpiler.transpile_to_python(
            source_code, generate_source_maps=True
        )
        print(f"SUCCESS: Generated {len(python_code1) if python_code1 else 0} chars of Python")
        print(f"Issues found: {len(issues1)}")

        # Show first few lines with array assignments
        if python_code1:
            lines = python_code1.split('\n')
            print("\nFirst occurrence of 'pow_results[0]':")
            for i, line in enumerate(lines):
                if 'pow_results[0]' in line:
                    print(f"  Line {i+1}: {line.strip()}")
                    break

            print("\nFirst occurrence of array length access:")
            for i, line in enumerate(lines):
                if "['length']()" in line:
                    print(f"  Line {i+1}: {line.strip()}")
                    break

    except Exception as e:
        print(f"FAILED: {e}")
        python_code1 = None

    print()

    # Method 2: transpile_ml_file (used by CLI transpile command)
    print("METHOD 2: transpile_ml_file() [CLI transpile method]")
    print("-" * 60)
    try:
        python_code2, issues2, source_map2 = transpile_ml_file(
            test_file, None, strict_security=True, generate_source_maps=True
        )
        print(f"SUCCESS: Generated {len(python_code2) if python_code2 else 0} chars of Python")
        print(f"Issues found: {len(issues2)}")

        # Show first few lines with array assignments
        if python_code2:
            lines = python_code2.split('\n')
            print("\nFirst occurrence of 'pow_results[0]':")
            for i, line in enumerate(lines):
                if 'pow_results[0]' in line:
                    print(f"  Line {i+1}: {line.strip()}")
                    break

            print("\nFirst occurrence of array length access:")
            for i, line in enumerate(lines):
                if "['length']()" in line:
                    print(f"  Line {i+1}: {line.strip()}")
                    break

    except Exception as e:
        print(f"FAILED: {e}")
        python_code2 = None

    print()

    # Method 3: execute_ml_code_sandbox (used by CLI run command)
    print("METHOD 3: execute_ml_code_sandbox() [CLI run method]")
    print("-" * 60)
    try:
        result, issues3 = execute_ml_code_sandbox(
            source_code, source_file=test_file, strict_security=True
        )
        print(f"Execution result: {result.success if result else 'Failed to start'}")
        print(f"Issues found: {len(issues3)}")
        if result and result.error:
            print(f"Error: {result.error}")

    except Exception as e:
        print(f"FAILED: {e}")

    print()

    # Compare outputs
    print("COMPARISON RESULTS")
    print("-" * 60)
    if python_code1 and python_code2:
        if python_code1 == python_code2:
            print("SUCCESS: MLTranspiler and transpile_ml_file produce IDENTICAL output")
        else:
            print("DIFFERENCE: MLTranspiler and transpile_ml_file produce DIFFERENT output")
            print(f"   MLTranspiler length: {len(python_code1)}")
            print(f"   transpile_ml_file length: {len(python_code2)}")

            # Find first difference
            lines1 = python_code1.split('\n')
            lines2 = python_code2.split('\n')
            for i, (line1, line2) in enumerate(zip(lines1, lines2)):
                if line1 != line2:
                    print(f"   First difference at line {i+1}:")
                    print(f"     MLTranspiler: {line1}")
                    print(f"     transpile_ml_file: {line2}")
                    break
    else:
        print("FAILED: Unable to compare - one or both methods failed")

if __name__ == "__main__":
    main()