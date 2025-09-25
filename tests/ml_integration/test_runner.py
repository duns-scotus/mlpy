#!/usr/bin/env python3
"""Comprehensive ML Integration Test Runner."""

import os
import sys
import time
import json
from typing import List, Dict, Any, Tuple
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

# Import the actual mlpy modules
from mlpy.ml.transpiler import MLTranspiler
from mlpy.ml.analysis.parallel_analyzer import ParallelSecurityAnalyzer
from mlpy.runtime.sandbox.sandbox import MLSandbox, SandboxConfig


class TestResult(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    SKIP = "SKIP"
    ERROR = "ERROR"


@dataclass
class TestCase:
    name: str
    file_path: str
    category: str
    expected_threats: int
    should_transpile: bool
    should_execute: bool
    description: str


@dataclass
class TestExecutionResult:
    test_case: TestCase
    result: TestResult
    execution_time_ms: float
    security_analysis: Dict[str, Any] = None
    transpilation_result: Tuple[str, List, Dict] = None
    execution_result: Any = None
    error_message: str = None
    threat_count: int = 0


class MLIntegrationTestRunner:
    """Comprehensive integration test runner for ML programs."""

    def __init__(self, test_directory: str):
        self.test_directory = Path(test_directory)
        self.transpiler = MLTranspiler()
        self.security_analyzer = ParallelSecurityAnalyzer(max_workers=3)
        self.results: List[TestExecutionResult] = []

        # Test categories and their properties
        self.test_categories = {
            "legitimate_programs": {
                "expected_threats": 0,
                "should_transpile": True,
                "should_execute": True,
            },
            "malicious_programs": {
                "expected_threats_min": 1,
                "should_transpile": False,  # Should be blocked
                "should_execute": False,
            },
            "edge_cases": {"expected_threats": 0, "should_transpile": True, "should_execute": True},
            "language_coverage": {
                "expected_threats": 0,
                "should_transpile": True,
                "should_execute": True,
            },
        }

    def discover_test_cases(self) -> List[TestCase]:
        """Discover all ML test files."""
        test_cases = []

        for category_dir in self.test_directory.iterdir():
            if not category_dir.is_dir():
                continue

            category = category_dir.name
            if category not in self.test_categories:
                continue

            category_config = self.test_categories[category]

            for ml_file in category_dir.glob("*.ml"):
                test_case = TestCase(
                    name=f"{category}::{ml_file.stem}",
                    file_path=str(ml_file),
                    category=category,
                    expected_threats=category_config.get("expected_threats", 0),
                    should_transpile=category_config.get("should_transpile", True),
                    should_execute=category_config.get("should_execute", True),
                    description=self._extract_description(ml_file),
                )
                test_cases.append(test_case)

        return sorted(test_cases, key=lambda tc: tc.name)

    def _extract_description(self, ml_file: Path) -> str:
        """Extract description from ML file comments."""
        try:
            with open(ml_file, "r", encoding="utf-8") as f:
                first_line = f.readline().strip()
                if first_line.startswith("//"):
                    return first_line[2:].strip()
        except:
            pass
        return f"ML test program: {ml_file.name}"

    def run_single_test(self, test_case: TestCase) -> TestExecutionResult:
        """Run a single ML test case through the complete pipeline."""
        print(f"  Running {test_case.name}...")

        start_time = time.time()
        result = TestExecutionResult(
            test_case=test_case,
            result=TestResult.ERROR,  # Default to ERROR, will be updated
            execution_time_ms=0.0,
        )

        try:
            # Step 1: Load ML source code
            with open(test_case.file_path, "r", encoding="utf-8") as f:
                ml_source = f.read()

            # Step 2: Security Analysis
            security_result = self.security_analyzer.analyze_parallel(
                ml_source, test_case.file_path
            )

            threat_count = (
                len(security_result.pattern_matches)
                + len(security_result.ast_violations)
                + len(security_result.data_flow_results.get("violations", []))
            )

            result.security_analysis = {
                "pattern_matches": len(security_result.pattern_matches),
                "ast_violations": len(security_result.ast_violations),
                "data_flow_violations": len(
                    security_result.data_flow_results.get("violations", [])
                ),
                "total_threats": threat_count,
                "analysis_time_ms": security_result.analysis_time * 1000,
            }
            result.threat_count = threat_count

            # Step 3: Validate Security Analysis Results
            if test_case.category == "malicious_programs":
                if threat_count == 0:
                    result.result = TestResult.FAIL
                    result.error_message = (
                        f"Expected threats but found none (should detect malicious code)"
                    )
                    return result
            elif test_case.category in ["legitimate_programs", "language_coverage", "edge_cases"]:
                if threat_count > 0:
                    result.result = TestResult.FAIL
                    result.error_message = (
                        f"Unexpected threats detected in legitimate code: {threat_count}"
                    )
                    return result

            # Step 4: Transpilation (only if should transpile)
            if test_case.should_transpile:
                try:
                    python_code, issues, source_map = self.transpiler.transpile_to_python(
                        ml_source, generate_source_maps=True
                    )

                    result.transpilation_result = (python_code, issues, source_map)

                    # Validate transpilation didn't introduce security issues
                    if self._validate_generated_python(python_code):
                        if test_case.should_execute:
                            # Step 5: Sandbox Execution
                            exec_result = self._execute_in_sandbox(python_code)
                            result.execution_result = exec_result

                        result.result = TestResult.PASS
                    else:
                        result.result = TestResult.FAIL
                        result.error_message = "Generated Python code contains security issues"

                except Exception as e:
                    if test_case.category == "malicious_programs":
                        # Malicious programs should fail transpilation
                        result.result = TestResult.PASS
                        result.error_message = f"Correctly blocked malicious program: {e}"
                    else:
                        result.result = TestResult.FAIL
                        result.error_message = f"Transpilation failed: {e}"
            else:
                # For malicious programs that shouldn't transpile
                result.result = TestResult.PASS

        except Exception as e:
            result.result = TestResult.ERROR
            result.error_message = f"Test execution error: {e}"

        finally:
            result.execution_time_ms = (time.time() - start_time) * 1000

        return result

    def _validate_generated_python(self, python_code: str) -> bool:
        """Validate that generated Python code is safe."""
        # Quick security check on generated Python
        dangerous_patterns = [
            "eval(",
            "exec(",
            "__import__",
            "getattr(",
            "setattr(",
            "__class__.__bases__",
            "__subclasses__",
            "subprocess.",
            "os.system",
            "open(",
            "__builtin__",
        ]

        # Handle None case (when transpilation is blocked due to security)
        if python_code is None:
            return False

        code_lower = python_code.lower()
        for pattern in dangerous_patterns:
            if pattern.lower() in code_lower:
                return False

        return True

    def _execute_in_sandbox(self, python_code: str) -> Dict[str, Any]:
        """Execute Python code in sandbox and return results."""
        try:
            config = SandboxConfig()

            with MLSandbox(config) as sandbox:
                result = sandbox.execute(python_code)

            return {
                "success": True,
                "result": result,
                "stdout": getattr(result, "stdout", ""),
                "stderr": getattr(result, "stderr", ""),
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def run_all_tests(self) -> Dict[str, Any]:
        """Run all discovered test cases."""
        print("=" * 70)
        print("ML INTEGRATION TEST SUITE")
        print("=" * 70)

        test_cases = self.discover_test_cases()
        print(
            f"Discovered {len(test_cases)} test cases across {len(self.test_categories)} categories"
        )

        # Run tests by category
        category_results = {}

        for category in self.test_categories.keys():
            category_tests = [tc for tc in test_cases if tc.category == category]
            if not category_tests:
                continue

            print(f"\n[{category.upper()}] Running {len(category_tests)} tests...")
            category_results[category] = []

            for test_case in category_tests:
                test_result = self.run_single_test(test_case)
                self.results.append(test_result)
                category_results[category].append(test_result)

                # Print immediate result
                status = test_result.result.value
                time_ms = test_result.execution_time_ms
                threats = test_result.threat_count

                if test_result.result == TestResult.PASS:
                    print(f"    [PASS] {test_case.name} ({time_ms:.1f}ms, {threats} threats)")
                else:
                    print(
                        f"    [FAIL] {test_case.name} ({time_ms:.1f}ms) - {test_result.error_message}"
                    )

        # Generate comprehensive report
        return self._generate_report(category_results)

    def _generate_report(
        self, category_results: Dict[str, List[TestExecutionResult]]
    ) -> Dict[str, Any]:
        """Generate comprehensive test report."""
        print("\n" + "=" * 70)
        print("TEST EXECUTION REPORT")
        print("=" * 70)

        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r.result == TestResult.PASS])
        failed_tests = len([r for r in self.results if r.result == TestResult.FAIL])
        error_tests = len([r for r in self.results if r.result == TestResult.ERROR])

        total_time = sum(r.execution_time_ms for r in self.results)
        avg_time = total_time / total_tests if total_tests > 0 else 0

        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ({passed_tests/total_tests*100:.1f}%)")
        print(f"Failed: {failed_tests} ({failed_tests/total_tests*100:.1f}%)")
        print(f"Errors: {error_tests} ({error_tests/total_tests*100:.1f}%)")
        print(f"Total Execution Time: {total_time:.1f}ms")
        print(f"Average Test Time: {avg_time:.1f}ms")

        # Category breakdown
        print(f"\nCategory Breakdown:")
        for category, results in category_results.items():
            cat_passed = len([r for r in results if r.result == TestResult.PASS])
            cat_total = len(results)
            print(f"  {category}: {cat_passed}/{cat_total} ({cat_passed/cat_total*100:.1f}%)")

        # Failed tests details
        failed_results = [r for r in self.results if r.result != TestResult.PASS]
        if failed_results:
            print(f"\nFailed/Error Tests:")
            for result in failed_results:
                print(f"  [FAIL] {result.test_case.name}: {result.error_message}")

        # Security analysis summary
        total_threats = sum(r.threat_count for r in self.results)
        malicious_results = [
            r for r in self.results if r.test_case.category == "malicious_programs"
        ]
        detected_malicious = len([r for r in malicious_results if r.threat_count > 0])

        print(f"\nSecurity Analysis Summary:")
        print(f"  Total Threats Detected: {total_threats}")
        if malicious_results:
            print(
                f"  Malicious Programs Detected: {detected_malicious}/{len(malicious_results)} ({detected_malicious/len(malicious_results)*100:.1f}%)"
            )

        # Overall assessment
        success_rate = passed_tests / total_tests if total_tests > 0 else 0
        if success_rate >= 0.95:
            status = "EXCELLENT"
        elif success_rate >= 0.90:
            status = "GOOD"
        elif success_rate >= 0.80:
            status = "ACCEPTABLE"
        else:
            status = "NEEDS_WORK"

        print(f"\nOverall Status: {status} ({success_rate*100:.1f}% success rate)")
        print("=" * 70)

        return {
            "summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "errors": error_tests,
                "success_rate": success_rate,
                "total_time_ms": total_time,
                "avg_time_ms": avg_time,
                "status": status,
            },
            "categories": {
                cat: {
                    "total": len(results),
                    "passed": len([r for r in results if r.result == TestResult.PASS]),
                    "failed": len([r for r in results if r.result == TestResult.FAIL]),
                    "errors": len([r for r in results if r.result == TestResult.ERROR]),
                }
                for cat, results in category_results.items()
            },
            "security_analysis": {
                "total_threats": total_threats,
                "malicious_detected": detected_malicious if malicious_results else 0,
                "malicious_total": len(malicious_results),
            },
            "detailed_results": [asdict(result) for result in self.results],
        }


def main():
    """Run ML integration test suite."""
    test_directory = os.path.dirname(__file__)

    if not os.path.exists(test_directory):
        print(f"Test directory not found: {test_directory}")
        print("Please create the test directory structure and ML test programs.")
        return 1

    runner = MLIntegrationTestRunner(test_directory)

    try:
        report = runner.run_all_tests()

        # Save detailed report
        with open("ml_integration_test_report.json", "w") as f:
            json.dump(report, f, indent=2, default=str)

        print(f"\nDetailed report saved to: ml_integration_test_report.json")

        # Return exit code based on success rate
        success_rate = report["summary"]["success_rate"]
        return 0 if success_rate >= 0.90 else 1

    except Exception as e:
        print(f"Test suite execution failed: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
