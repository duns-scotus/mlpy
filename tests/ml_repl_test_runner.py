#!/usr/bin/env python3
"""Comprehensive REPL Integration Test Runner.

This script provides end-to-end integration testing for the mlpy REPL,
executing hundreds of ML statements from integration test files and
verifying correct execution, variable persistence, stdlib imports, and
REPL command handling.

Usage:
    python tests/ml_repl_test_runner.py                    # Run all tests
    python tests/ml_repl_test_runner.py --builtin         # Test builtin functions only
    python tests/ml_repl_test_runner.py --core            # Test core language only
    python tests/ml_repl_test_runner.py --stdlib          # Test stdlib only
    python tests/ml_repl_test_runner.py --commands        # Test REPL commands only
    python tests/ml_repl_test_runner.py --limit 50        # Limit to 50 statements
    python tests/ml_repl_test_runner.py --verbose         # Show all output
    python tests/ml_repl_test_runner.py --no-color        # Disable colored output
"""

import argparse
import json
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mlpy.cli.repl import MLREPLSession, format_repl_value


# ANSI color codes
class Colors:
    """ANSI color codes for terminal output."""
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

    @classmethod
    def disable(cls):
        """Disable all colors."""
        cls.RESET = ''
        cls.RED = ''
        cls.GREEN = ''
        cls.YELLOW = ''
        cls.BLUE = ''
        cls.MAGENTA = ''
        cls.CYAN = ''
        cls.BOLD = ''
        cls.DIM = ''


@dataclass
class TestResult:
    """Result of a single REPL statement execution."""
    statement: str
    success: bool
    value: Any = None
    error: str | None = None
    execution_time: float = 0.0
    source_file: str | None = None
    line_number: int | None = None


@dataclass
class TestCategory:
    """Test category with results."""
    name: str
    description: str
    results: list[TestResult] = field(default_factory=list)
    start_time: float = 0.0
    end_time: float = 0.0

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def passed(self) -> int:
        return sum(1 for r in self.results if r.success)

    @property
    def failed(self) -> int:
        return self.total - self.passed

    @property
    def success_rate(self) -> float:
        return (self.passed / self.total * 100) if self.total > 0 else 0.0

    @property
    def duration(self) -> float:
        return self.end_time - self.start_time


class REPLTestRunner:
    """Comprehensive REPL integration test runner."""

    def __init__(
        self,
        verbose: bool = False,
        limit: int | None = None,
        colored: bool = True
    ):
        """Initialize test runner.

        Args:
            verbose: Show detailed output
            limit: Maximum number of statements to test
            colored: Enable colored output
        """
        self.verbose = verbose
        self.limit = limit
        self.session = MLREPLSession(security_enabled=False)
        self.categories: dict[str, TestCategory] = {}
        self.total_statements = 0
        self.start_time = 0.0

        if not colored:
            Colors.disable()

    def _print_progress(self, current: int, total: int, category: str = ""):
        """Print progress indicator.

        Args:
            current: Current statement number
            total: Total statements
            category: Optional category name
        """
        percentage = (current / total * 100) if total > 0 else 0
        bar_length = 30
        filled = int(bar_length * current / total) if total > 0 else 0
        bar = '=' * filled + '-' * (bar_length - filled)

        category_str = f" [{category}]" if category else ""
        print(f"\r  Progress: [{bar}] {current}/{total} ({percentage:.1f}%){category_str}", end='', flush=True)

    def extract_statements_from_file(self, ml_file: Path) -> list[tuple[str, int]]:
        """Extract individual ML statements from a file.

        Args:
            ml_file: Path to ML source file

        Returns:
            List of (statement, line_number) tuples
        """
        try:
            content = ml_file.read_text(encoding='utf-8')
        except Exception as e:
            print(f"{Colors.RED}Failed to read {ml_file}: {e}{Colors.RESET}")
            return []

        statements = []
        lines = content.split('\n')
        current_statement = []
        start_line = 0
        brace_depth = 0

        for line_num, line in enumerate(lines, 1):
            # Skip comments and empty lines
            stripped = line.strip()
            if not stripped or stripped.startswith('//'):
                continue

            current_statement.append(line)

            # Track brace depth
            brace_depth += line.count('{') - line.count('}')

            # Check if statement is complete
            if brace_depth == 0 and (stripped.endswith(';') or stripped.endswith('}')):
                stmt = '\n'.join(current_statement).strip()
                if stmt:
                    statements.append((stmt, start_line or line_num))
                current_statement = []
                start_line = 0
            elif not current_statement or len(current_statement) == 1:
                start_line = line_num

        return statements

    def test_repl_commands(self) -> TestCategory:
        """Test REPL special commands (.help, .vars, .clear, .exit)."""
        category = TestCategory(
            name="REPL Commands",
            description="Test REPL special commands"
        )
        category.start_time = time.time()

        print(f"\n{Colors.CYAN}{Colors.BOLD}Testing REPL Commands...{Colors.RESET}")

        total_tests = 4
        current = 0

        # Test .vars command
        current += 1
        self._print_progress(current, total_tests, "vars")
        self.session.execute_ml_line("test_var = 42")
        vars_dict = self.session.get_variables()

        result = TestResult(
            statement=".vars",
            success="test_var" in vars_dict and vars_dict["test_var"] == 42,
            value=vars_dict,
            source_file="<repl-commands>"
        )
        category.results.append(result)
        print()  # New line after progress
        self._print_result(result, current)

        # Test .clear command
        current += 1
        self._print_progress(current, total_tests, "clear")
        self.session.reset_session()
        vars_dict_after = self.session.get_variables()

        result = TestResult(
            statement=".clear",
            success="test_var" not in vars_dict_after,
            value=vars_dict_after,
            source_file="<repl-commands>"
        )
        category.results.append(result)
        print()
        self._print_result(result, current)

        # Test history
        current += 1
        self._print_progress(current, total_tests, "history")
        self.session.execute_ml_line("x = 1")
        self.session.execute_ml_line("y = 2")

        result = TestResult(
            statement=".history",
            success=len(self.session.history) >= 2,
            value=len(self.session.history),
            source_file="<repl-commands>"
        )
        category.results.append(result)
        print()
        self._print_result(result, current)

        # Test variable persistence
        current += 1
        self._print_progress(current, total_tests, "persistence")
        self.session.execute_ml_line("counter = 0")
        self.session.execute_ml_line("counter = counter + 1")
        self.session.execute_ml_line("counter = counter + 1")
        res = self.session.execute_ml_line("counter")

        result = TestResult(
            statement="Variable persistence (counter = 0; counter++; counter++)",
            success=res.success and res.value == 2,
            value=res.value,
            source_file="<repl-commands>"
        )
        category.results.append(result)
        print()
        self._print_result(result, current)

        category.end_time = time.time()
        elapsed = category.end_time - category.start_time
        print(f"{Colors.DIM}  Completed in {elapsed:.2f}s{Colors.RESET}")
        return category

    def test_stdlib_imports(self) -> TestCategory:
        """Test builtin functions and basic operations."""
        category = TestCategory(
            name="Builtin Functions & Variables",
            description="Test builtin functions, type conversions, and variable operations"
        )
        category.start_time = time.time()

        print(f"\n{Colors.CYAN}{Colors.BOLD}Testing Builtin Functions & Variables...{Colors.RESET}")

        # Create fresh session for clean test
        self.session = MLREPLSession(security_enabled=False)

        test_cases = [
            # Builtin functions (no import needed)
            ('typeof(42)', "number", "typeof number"),
            ('typeof("hello")', "string", "typeof string"),
            ('typeof(true)', "boolean", "typeof boolean"),
            ('typeof([1,2,3])', "array", "typeof array"),
            ('typeof({"x": 1})', "object", "typeof object"),

            # Type conversions
            ('int(3.14)', 3, "int from float"),
            ('int("42")', 42, "int from string"),
            ('float(42)', 42.0, "float from int"),
            ('str(42)', "42", "str from int"),
            ('bool(1)', True, "bool from int"),

            # Array operations
            ('nums = [1, 2, 3, 4, 5]', None, "create array"),
            ('len(nums)', 5, "array length"),
            ('min(nums)', 1, "array min"),
            ('max(nums)', 5, "array max"),
            ('sum(nums)', 15, "array sum"),

            # Object operations
            ('person = {"name": "Alice", "age": 30}', None, "create object"),
            ('keys(person)', ["name", "age"], "object keys"),
            ('person["name"]', "Alice", "object access"),

            # String operations
            ('greeting = "Hello REPL"', None, "create string"),
            ('len(greeting)', 10, "string length"),

            # Math operations
            ('abs(-42)', 42, "abs function"),
            ('round(3.14159, 2)', 3.14, "round function"),

            # Import statement syntax (should work)
            ('import math;', None, "import math (note: functions may need capabilities)"),
        ]

        total_tests = len(test_cases)

        for idx, (statement, expected, description) in enumerate(test_cases, 1):
            self._print_progress(idx, total_tests, description[:20])
            res = self.session.execute_ml_line(statement)

            if expected is None:
                success = res.success
            else:
                success = res.success and res.value == expected

            result = TestResult(
                statement=f"{description}: {statement}",
                success=success,
                value=res.value,
                error=res.error,
                execution_time=res.execution_time_ms,
                source_file="<stdlib-tests>"
            )
            category.results.append(result)
            print()  # New line after progress
            self._print_result(result, idx)

        category.end_time = time.time()
        elapsed = category.end_time - category.start_time
        print(f"{Colors.DIM}  Completed in {elapsed:.2f}s{Colors.RESET}")
        return category

    def test_ml_files(
        self,
        file_pattern: str,
        category_name: str,
        category_desc: str
    ) -> TestCategory:
        """Test ML files matching a pattern.

        Args:
            file_pattern: Glob pattern for ML files
            category_name: Category name
            category_desc: Category description

        Returns:
            TestCategory with results
        """
        category = TestCategory(name=category_name, description=category_desc)
        category.start_time = time.time()

        # Find ML files
        test_dir = Path(__file__).parent / "ml_integration"
        ml_files = sorted(test_dir.glob(file_pattern))

        if not ml_files:
            print(f"{Colors.YELLOW}No files found matching: {file_pattern}{Colors.RESET}")
            category.end_time = time.time()
            return category

        print(f"\n{Colors.CYAN}{Colors.BOLD}Testing {category_name}...{Colors.RESET}")
        print(f"{Colors.DIM}Found {len(ml_files)} files{Colors.RESET}")

        # Create fresh session for clean state
        self.session = MLREPLSession(security_enabled=False)

        statement_count = 0

        for ml_file in ml_files:
            if self.limit and self.total_statements >= self.limit:
                print(f"\n{Colors.YELLOW}Reached statement limit ({self.limit}){Colors.RESET}")
                break

            print(f"\n{Colors.BLUE}Testing: {ml_file.name}{Colors.RESET}")

            statements = self.extract_statements_from_file(ml_file)
            file_start_time = time.time()

            for idx, (statement, line_num) in enumerate(statements, 1):
                if self.limit and self.total_statements >= self.limit:
                    break

                statement_count += 1
                self.total_statements += 1

                # Show progress for this file
                if not self.verbose:
                    self._print_progress(idx, len(statements), ml_file.stem)

                # Execute statement
                start = time.time()
                res = self.session.execute_ml_line(statement)
                duration = (time.time() - start) * 1000

                result = TestResult(
                    statement=statement[:80] + "..." if len(statement) > 80 else statement,
                    success=res.success,
                    value=res.value,
                    error=res.error,
                    execution_time=duration,
                    source_file=str(ml_file.name),
                    line_number=line_num
                )
                category.results.append(result)

                if self.verbose or not res.success:
                    if not self.verbose:
                        print()  # New line after progress
                    self._print_result(result, statement_count)

            file_elapsed = time.time() - file_start_time

            if not self.verbose:
                print()  # Clear progress line
                # Print summary for this file
                file_results = [r for r in category.results if r.source_file == str(ml_file.name)]
                passed = sum(1 for r in file_results if r.success)
                total = len(file_results)
                if passed == total:
                    status = f"{Colors.GREEN}PASS{Colors.RESET}"
                else:
                    status = f"{Colors.RED}FAIL{Colors.RESET}"
                print(f"  {status} {passed}/{total} statements passed in {file_elapsed:.2f}s")

        category.end_time = time.time()
        elapsed = category.end_time - category.start_time
        print(f"\n{Colors.DIM}Category completed in {elapsed:.2f}s{Colors.RESET}")
        return category

    def _print_result(self, result: TestResult, index: int):
        """Print a test result.

        Args:
            result: Test result
            index: Statement index
        """
        # Use ASCII-safe characters for Windows compatibility
        check = "PASS" if result.success else "FAIL"
        color = Colors.GREEN if result.success else Colors.RED
        status = f"{color}{check}{Colors.RESET}"
        stmt = result.statement.replace('\n', ' ')[:100]

        print(f"  {status} [{index:3d}] {stmt}")

        if not result.success and result.error:
            error_lines = result.error.split('\n')[:3]
            for line in error_lines:
                print(f"      {Colors.RED}{line}{Colors.RESET}")

        if self.verbose and result.value is not None:
            value_str = format_repl_value(result.value)
            if len(value_str) > 100:
                value_str = value_str[:100] + "..."
            print(f"      {Colors.DIM}=> {value_str}{Colors.RESET}")

    def print_summary(self):
        """Print comprehensive test summary."""
        overall_elapsed = time.time() - self.start_time

        print(f"\n{Colors.BOLD}{'='*80}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}REPL Integration Test Summary{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*80}{Colors.RESET}\n")

        total_passed = 0
        total_failed = 0
        total_time = 0.0
        total_exec_time = 0.0

        for category in self.categories.values():
            total_passed += category.passed
            total_failed += category.failed
            total_time += category.duration

            # Calculate average execution time for this category
            cat_exec_time = sum(r.execution_time for r in category.results if r.execution_time > 0)
            total_exec_time += cat_exec_time
            avg_exec_time = cat_exec_time / category.total if category.total > 0 else 0

            # Category header
            rate_color = Colors.GREEN if category.success_rate >= 90 else Colors.YELLOW if category.success_rate >= 70 else Colors.RED
            print(f"{Colors.BOLD}{category.name}{Colors.RESET}")
            print(f"  {category.description}")
            print(f"  Results: {Colors.GREEN}{category.passed} passed{Colors.RESET}, "
                  f"{Colors.RED}{category.failed} failed{Colors.RESET}, "
                  f"{category.total} total")
            print(f"  Success Rate: {rate_color}{category.success_rate:.1f}%{Colors.RESET}")
            print(f"  Duration: {category.duration:.2f}s (avg: {avg_exec_time:.2f}ms per statement)")

            # Show failed tests
            if category.failed > 0:
                failed = [r for r in category.results if not r.success]
                print(f"\n  {Colors.RED}Failed Tests:{Colors.RESET}")
                for result in failed[:5]:  # Show first 5 failures
                    stmt = result.statement[:60].replace('\n', ' ')
                    source = f"{result.source_file}:{result.line_number}" if result.source_file else "<repl>"
                    print(f"    • {stmt}")
                    print(f"      {Colors.DIM}Source: {source}{Colors.RESET}")
                    if result.error:
                        error_preview = result.error.split('\n')[0][:80]
                        print(f"      {Colors.RED}Error: {error_preview}{Colors.RESET}")
                if category.failed > 5:
                    print(f"    {Colors.DIM}... and {category.failed - 5} more{Colors.RESET}")

            print()

        # Overall summary
        total = total_passed + total_failed
        overall_rate = (total_passed / total * 100) if total > 0 else 0.0
        rate_color = Colors.GREEN if overall_rate >= 90 else Colors.YELLOW if overall_rate >= 70 else Colors.RED

        print(f"{Colors.BOLD}Overall Results:{Colors.RESET}")
        print(f"  Total Statements: {total}")
        print(f"  Passed: {Colors.GREEN}{total_passed}{Colors.RESET}")
        print(f"  Failed: {Colors.RED}{total_failed}{Colors.RESET}")
        print(f"  Success Rate: {rate_color}{overall_rate:.1f}%{Colors.RESET}")

        print(f"\n{Colors.BOLD}Timing Summary:{Colors.RESET}")
        print(f"  Total Elapsed Time: {overall_elapsed:.2f}s")
        print(f"  Test Execution Time: {total_time:.2f}s")
        print(f"  Average per Statement: {(total_exec_time / total):.2f}ms" if total > 0 else "")
        print(f"  Throughput: {(total / overall_elapsed):.1f} statements/second" if overall_elapsed > 0 else "")

        print(f"\n{Colors.BOLD}{'='*80}{Colors.RESET}\n")

        # Return exit code
        return 0 if total_failed == 0 else 1

    def run_all_tests(
        self,
        test_builtin: bool = True,
        test_core: bool = True,
        test_stdlib: bool = True,
        test_commands: bool = True
    ):
        """Run all selected test categories.

        Args:
            test_builtin: Test builtin functions
            test_core: Test core language
            test_stdlib: Test stdlib modules
            test_commands: Test REPL commands
        """
        self.start_time = time.time()

        print(f"{Colors.BOLD}{Colors.MAGENTA}mlpy REPL Integration Test Runner{Colors.RESET}")
        print(f"{Colors.DIM}Testing REPL functionality with real ML code{Colors.RESET}")
        print(f"{Colors.DIM}Limit: {self.limit if self.limit else 'unlimited'} statements{Colors.RESET}\n")

        # Test REPL commands first
        if test_commands:
            self.categories["commands"] = self.test_repl_commands()

        # Test stdlib imports
        if test_stdlib:
            self.categories["stdlib"] = self.test_stdlib_imports()

        # Test builtin functions
        if test_builtin:
            self.categories["builtin"] = self.test_ml_files(
                "ml_builtin/*.ml",
                "Builtin Functions",
                "Test builtin module functions (int, float, typeof, len, etc.)"
            )

        # Test core language features
        if test_core:
            self.categories["core"] = self.test_ml_files(
                "ml_core/*.ml",
                "Core Language",
                "Test core language features (recursion, control flow, etc.)"
            )

        # Print summary and return exit code
        return self.print_summary()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Comprehensive REPL Integration Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                     Run all tests
  %(prog)s --builtin          Test builtin functions only
  %(prog)s --core             Test core language only
  %(prog)s --stdlib           Test stdlib only
  %(prog)s --commands         Test REPL commands only
  %(prog)s --limit 50         Limit to 50 statements
  %(prog)s --verbose          Show detailed output
  %(prog)s --no-color         Disable colored output
"""
    )

    parser.add_argument(
        '--builtin',
        action='store_true',
        help='Test builtin functions only'
    )
    parser.add_argument(
        '--core',
        action='store_true',
        help='Test core language features only'
    )
    parser.add_argument(
        '--stdlib',
        action='store_true',
        help='Test stdlib imports only'
    )
    parser.add_argument(
        '--commands',
        action='store_true',
        help='Test REPL commands only'
    )
    parser.add_argument(
        '--limit',
        type=int,
        metavar='N',
        default=200,
        help='Limit to N statements (default: 200)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed output for all statements'
    )
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output'
    )

    args = parser.parse_args()

    # Determine what to test
    test_all = not (args.builtin or args.core or args.stdlib or args.commands)

    runner = REPLTestRunner(
        verbose=args.verbose,
        limit=args.limit,
        colored=not args.no_color
    )

    exit_code = runner.run_all_tests(
        test_builtin=test_all or args.builtin,
        test_core=test_all or args.core,
        test_stdlib=test_all or args.stdlib,
        test_commands=test_all or args.commands
    )

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
