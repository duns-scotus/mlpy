"""
Documentation Example Test Runner
Validates all example code in the documentation to ensure it works correctly.
"""

import os
import sys
import subprocess
import tempfile
import traceback
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

# Add mlpy to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

try:
    from mlpy.transpiler import MLTranspiler
    from mlpy.runtime.sandbox import SandboxManager
    from mlpy.ml.errors import MLError
except ImportError as e:
    print(f"Warning: Could not import mlpy modules: {e}")
    print("Some tests may be skipped.")
    MLTranspiler = None
    SandboxManager = None
    MLError = Exception


class TestResult(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    SKIP = "SKIP"
    ERROR = "ERROR"


@dataclass
class TestCase:
    name: str
    file_path: Path
    expected_output: Optional[str] = None
    should_fail: bool = False
    requires_capabilities: List[str] = None


@dataclass
class TestExecutionResult:
    test_case: TestCase
    result: TestResult
    message: str = ""
    output: str = ""
    error: str = ""
    execution_time: float = 0.0


class DocumentationTestRunner:
    """Test runner for documentation examples."""

    def __init__(self, examples_dir: Path):
        self.examples_dir = Path(examples_dir)
        self.transpiler = MLTranspiler() if MLTranspiler else None
        self.sandbox = SandboxManager() if SandboxManager else None
        self.results: List[TestExecutionResult] = []

    def discover_tests(self) -> List[TestCase]:
        """Discover all test cases from example files."""
        test_cases = []

        # ML files
        for ml_file in self.examples_dir.rglob("*.ml"):
            test_case = TestCase(
                name=f"ML:{ml_file.relative_to(self.examples_dir)}",
                file_path=ml_file,
                expected_output=self._extract_expected_output(ml_file)
            )
            test_cases.append(test_case)

        # Python integration examples
        for py_file in self.examples_dir.rglob("*.py"):
            if py_file.name.startswith("test_") or "test" in py_file.stem:
                continue  # Skip actual test files

            test_case = TestCase(
                name=f"PY:{py_file.relative_to(self.examples_dir)}",
                file_path=py_file,
                should_fail=False
            )
            test_cases.append(test_case)

        return test_cases

    def _extract_expected_output(self, file_path: Path) -> Optional[str]:
        """Extract expected output from ML file comments."""
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')

            expected_lines = []
            for line in lines:
                if '// Expected output:' in line:
                    expected_lines.append(line.split('// Expected output:', 1)[1].strip())
                elif line.strip().startswith('// Output:'):
                    expected_lines.append(line.split('// Output:', 1)[1].strip())

            return '\n'.join(expected_lines) if expected_lines else None

        except Exception:
            return None

    def run_ml_test(self, test_case: TestCase) -> TestExecutionResult:
        """Run a single ML test case."""
        import time

        start_time = time.time()

        if not self.transpiler:
            return TestExecutionResult(
                test_case=test_case,
                result=TestResult.SKIP,
                message="MLTranspiler not available",
                execution_time=time.time() - start_time
            )

        try:
            # Read ML file
            ml_code = test_case.file_path.read_text(encoding='utf-8')

            # Transpile ML to Python
            transpile_result = self.transpiler.transpile_string(ml_code)

            if not transpile_result.success:
                return TestExecutionResult(
                    test_case=test_case,
                    result=TestResult.FAIL,
                    message="Transpilation failed",
                    error='; '.join(transpile_result.errors),
                    execution_time=time.time() - start_time
                )

            # Execute in sandbox if available
            if self.sandbox:
                execution_result = self.sandbox.execute_code(transpile_result.python_code)

                if execution_result.success:
                    output = execution_result.output.strip()

                    # Check expected output if specified
                    if test_case.expected_output:
                        if test_case.expected_output in output:
                            result = TestResult.PASS
                            message = "Output matches expected"
                        else:
                            result = TestResult.FAIL
                            message = f"Output mismatch. Expected: '{test_case.expected_output}', Got: '{output}'"
                    else:
                        result = TestResult.PASS
                        message = "Execution successful"

                    return TestExecutionResult(
                        test_case=test_case,
                        result=result,
                        message=message,
                        output=output,
                        execution_time=time.time() - start_time
                    )
                else:
                    return TestExecutionResult(
                        test_case=test_case,
                        result=TestResult.FAIL,
                        message="Execution failed",
                        error=execution_result.error,
                        execution_time=time.time() - start_time
                    )
            else:
                # Just check transpilation success
                return TestExecutionResult(
                    test_case=test_case,
                    result=TestResult.PASS,
                    message="Transpilation successful (sandbox not available)",
                    output=transpile_result.python_code[:200] + "..." if len(transpile_result.python_code) > 200 else transpile_result.python_code,
                    execution_time=time.time() - start_time
                )

        except Exception as e:
            return TestExecutionResult(
                test_case=test_case,
                result=TestResult.ERROR,
                message="Unexpected error",
                error=str(e),
                execution_time=time.time() - start_time
            )

    def run_python_test(self, test_case: TestCase) -> TestExecutionResult:
        """Run a Python integration test."""
        import time

        start_time = time.time()

        try:
            # Run Python file as subprocess to avoid import conflicts
            result = subprocess.run(
                [sys.executable, str(test_case.file_path)],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=test_case.file_path.parent
            )

            if result.returncode == 0:
                return TestExecutionResult(
                    test_case=test_case,
                    result=TestResult.PASS,
                    message="Python execution successful",
                    output=result.stdout,
                    execution_time=time.time() - start_time
                )
            else:
                return TestExecutionResult(
                    test_case=test_case,
                    result=TestResult.FAIL,
                    message=f"Python execution failed (exit code {result.returncode})",
                    error=result.stderr,
                    execution_time=time.time() - start_time
                )

        except subprocess.TimeoutExpired:
            return TestExecutionResult(
                test_case=test_case,
                result=TestResult.ERROR,
                message="Test timeout (30s)",
                execution_time=time.time() - start_time
            )
        except Exception as e:
            return TestExecutionResult(
                test_case=test_case,
                result=TestResult.ERROR,
                message="Unexpected error",
                error=str(e),
                execution_time=time.time() - start_time
            )

    def run_test(self, test_case: TestCase) -> TestExecutionResult:
        """Run a single test case."""
        if test_case.file_path.suffix == '.ml':
            return self.run_ml_test(test_case)
        elif test_case.file_path.suffix == '.py':
            return self.run_python_test(test_case)
        else:
            return TestExecutionResult(
                test_case=test_case,
                result=TestResult.SKIP,
                message=f"Unsupported file type: {test_case.file_path.suffix}"
            )

    def run_all_tests(self) -> List[TestExecutionResult]:
        """Run all discovered tests."""
        test_cases = self.discover_tests()
        results = []

        print(f"Discovered {len(test_cases)} test cases")
        print("=" * 50)

        for i, test_case in enumerate(test_cases, 1):
            print(f"[{i:2d}/{len(test_cases):2d}] Running {test_case.name}... ", end="", flush=True)

            result = self.run_test(test_case)
            results.append(result)

            # Print result with color coding
            if result.result == TestResult.PASS:
                print("[OK]")
            elif result.result == TestResult.SKIP:
                print("[SKIP]")
            elif result.result == TestResult.FAIL:
                print("[FAIL]")
            else:
                print("[ERROR]")

            # Print details for failures and errors
            if result.result in [TestResult.FAIL, TestResult.ERROR]:
                print(f"     Message: {result.message}")
                if result.error:
                    print(f"     Error: {result.error}")
                print()

        self.results = results
        return results

    def print_summary(self):
        """Print test execution summary."""
        if not self.results:
            print("No test results available")
            return

        total = len(self.results)
        passed = sum(1 for r in self.results if r.result == TestResult.PASS)
        failed = sum(1 for r in self.results if r.result == TestResult.FAIL)
        errors = sum(1 for r in self.results if r.result == TestResult.ERROR)
        skipped = sum(1 for r in self.results if r.result == TestResult.SKIP)

        print("\n" + "=" * 50)
        print("TEST SUMMARY")
        print("=" * 50)
        print(f"Total:   {total:3d}")
        print(f"Passed:  {passed:3d}")
        print(f"Failed:  {failed:3d}")
        print(f"Errors:  {errors:3d}")
        print(f"Skipped: {skipped:3d}")

        if total > 0:
            success_rate = (passed / total) * 100
            print(f"Success Rate: {success_rate:.1f}%")

        total_time = sum(r.execution_time for r in self.results)
        print(f"Total Time: {total_time:.2f}s")

        # List failures and errors
        failures = [r for r in self.results if r.result in [TestResult.FAIL, TestResult.ERROR]]
        if failures:
            print(f"\nFAILURES AND ERRORS ({len(failures)}):")
            for result in failures:
                print(f"  {result.test_case.name}: {result.message}")


def main():
    """Main entry point for documentation test runner."""
    import argparse

    parser = argparse.ArgumentParser(description="Run documentation example tests")
    parser.add_argument(
        "--examples-dir",
        type=Path,
        default=Path(__file__).parent,
        help="Path to examples directory"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )

    args = parser.parse_args()

    print("Documentation Example Test Runner")
    print(f"Examples directory: {args.examples_dir}")
    print()

    runner = DocumentationTestRunner(args.examples_dir)
    results = runner.run_all_tests()
    runner.print_summary()

    # Exit with error code if any tests failed
    failed_count = sum(1 for r in results if r.result in [TestResult.FAIL, TestResult.ERROR])
    sys.exit(1 if failed_count > 0 else 0)


if __name__ == "__main__":
    main()