#!/usr/bin/env python3
"""
Debug script to test the same broken Python code in both execution environments.
"""

from mlpy.runtime.sandbox import MLSandbox, SandboxConfig
from mlpy.ml.transpiler import execute_ml_code_sandbox

# Create minimal broken Python code that should fail
broken_python_code = '''
# This should fail with "list assignment index out of range"
pow_results = []
pow_results[0] = 42
print("This should not print")
'''

print("Testing broken Python code in both execution environments:")
print("=" * 60)
print("Code to test:")
print(broken_python_code)
print("=" * 60)

# Test 1: ml_test_runner method (MLSandbox directly)
print("\n1. TESTING: MLSandbox (ml_test_runner method)")
print("-" * 40)
try:
    config = SandboxConfig()
    with MLSandbox(config) as sandbox:
        result = sandbox.execute(broken_python_code)

    print(f"Success: {getattr(result, 'success', 'unknown')}")
    print(f"Return value: {getattr(result, 'return_value', 'none')}")
    print(f"Stdout: '{getattr(result, 'stdout', '')}'")
    print(f"Stderr: '{getattr(result, 'stderr', '')}'")
    print(f"Error: {getattr(result, 'error', 'none')}")
    print("MLSandbox execution: COMPLETED")

except Exception as e:
    print(f"MLSandbox execution: FAILED with exception: {e}")

# Test 2: CLI method (execute_ml_code_sandbox)
print("\n2. TESTING: execute_ml_code_sandbox (CLI method)")
print("-" * 40)
try:
    # We need to provide ML source code, not Python code
    # So let's use minimal ML that generates the same broken Python
    ml_source = '''
pow_results = [];
pow_results[0] = 42;
print("This should not print");
'''

    result, issues = execute_ml_code_sandbox(
        ml_source, source_file="test.ml", strict_security=True
    )

    print(f"Result object: {result}")
    if result:
        print(f"Success: {result.success}")
        print(f"Return value: {result.return_value}")
        print(f"Stdout: '{result.stdout}'")
        print(f"Stderr: '{result.stderr}'")
        print(f"Error: {result.error}")
    print(f"Issues: {len(issues)}")
    print("execute_ml_code_sandbox: COMPLETED")

except Exception as e:
    print(f"execute_ml_code_sandbox: FAILED with exception: {e}")

print("\n" + "=" * 60)
print("CONCLUSION: This will show us if the execution environments behave differently")