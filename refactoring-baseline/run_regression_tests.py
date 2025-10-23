#!/usr/bin/env python3
"""
Automated Regression Test Script for Codegen Refactoring

This script runs all critical tests and compares results against baseline.
Run this after each phase of the refactoring to ensure no regressions.

Usage:
    python refactoring-baseline/run_regression_tests.py
"""

import subprocess
import sys
from pathlib import Path

# ANSI color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def run_command(cmd, description):
    """Run a command and return success status."""
    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}Running: {description}{RESET}")
    print(f"{BLUE}{'='*70}{RESET}")

    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )

    print(result.stdout)
    if result.stderr:
        print(result.stderr)

    return result.returncode == 0

def main():
    """Run all regression tests."""
    print(f"\n{BLUE}{'='*70}")
    print("CODEGEN REFACTORING - REGRESSION TEST SUITE")
    print(f"{'='*70}{RESET}\n")

    tests = [
        {
            'name': 'Unit Tests (Codegen)',
            'cmd': 'python -m pytest tests/unit/codegen/ -v --tb=short --no-cov',
            'critical': True,
            'expected_pass': 238,
        },
        {
            'name': 'Integration Tests (ML Programs)',
            'cmd': 'python tests/ml_test_runner.py --full',
            'critical': True,
            'expected_pass': 69,
        },
        {
            'name': 'Transpiler Tests (API Usage)',
            'cmd': 'python -m pytest tests/unit/transpiler/ -v --tb=short --no-cov -k "not slow"',
            'critical': False,
        },
        {
            'name': 'Import Compatibility Test',
            'cmd': 'python -c "from mlpy.ml.codegen import PythonCodeGenerator, generate_python_code; from mlpy.ml.codegen.python_generator import PythonCodeGenerator, generate_python_code, SourceMapping, CodeGenerationContext; print(\'All imports successful!\')"',
            'critical': True,
        },
    ]

    results = []
    for test in tests:
        success = run_command(test['cmd'], test['name'])
        results.append({
            'name': test['name'],
            'success': success,
            'critical': test.get('critical', False)
        })

        if success:
            print(f"{GREEN}[PASS] {test['name']}{RESET}")
        else:
            print(f"{RED}[FAIL] {test['name']}{RESET}")
            if test.get('critical'):
                print(f"{RED}CRITICAL TEST FAILED - REFACTORING MAY HAVE BROKEN SOMETHING{RESET}")

    # Summary
    print(f"\n{BLUE}{'='*70}")
    print("REGRESSION TEST SUMMARY")
    print(f"{'='*70}{RESET}\n")

    total = len(results)
    passed = sum(1 for r in results if r['success'])
    failed = total - passed
    critical_failed = sum(1 for r in results if not r['success'] and r['critical'])

    print(f"Total Tests: {total}")
    print(f"{GREEN}Passed: {passed}{RESET}")
    print(f"{RED}Failed: {failed}{RESET}")

    if critical_failed > 0:
        print(f"\n{RED}{'='*70}")
        print(f"CRITICAL: {critical_failed} critical test(s) failed!")
        print(f"RECOMMENDATION: Revert changes and investigate")
        print(f"Rollback command: git reset --hard baseline-before-codegen-refactor")
        print(f"{'='*70}{RESET}\n")
        return 1

    if failed == 0:
        print(f"\n{GREEN}{'='*70}")
        print("ALL TESTS PASSED - REFACTORING SAFE TO CONTINUE")
        print(f"{'='*70}{RESET}\n")
        return 0
    else:
        print(f"\n{YELLOW}{'='*70}")
        print(f"WARNING: {failed} non-critical test(s) failed")
        print("Review failures before continuing")
        print(f"{'='*70}{RESET}\n")
        return 0

if __name__ == '__main__':
    sys.exit(main())
