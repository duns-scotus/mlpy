#!/usr/bin/env python3
"""
Python Snippet Validator - Documentation Python Code Example Validation

Validates all Python code snippets in docs/py_snippets/ directory by checking
syntax and attempting execution.

Usage:
    python tests/py_snippet_validator.py                    # Validate all snippets
    python tests/py_snippet_validator.py --category embedding # Validate specific category
    python tests/py_snippet_validator.py --verbose          # Show detailed output
    python tests/py_snippet_validator.py --ci               # CI mode (fail fast)
"""

import argparse
import ast
import io
import subprocess
import sys
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional

# Set UTF-8 encoding for stdout/stderr on Windows
if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")


class ValidationStage(Enum):
    """Validation stage for Python snippets."""
    SYNTAX = "Syntax"
    IMPORTS = "Imports"
    EXECUTION = "Execution"


@dataclass
class PySnippetValidationResult:
    """Validation result for a single Python snippet."""
    file_path: Path
    category: str
    passed: bool = True
    failed_stage: Optional[ValidationStage] = None
    error: Optional[str] = None
    execution_time_ms: float = 0.0


class PySnippetValidator:
    """Validates Python code snippets for documentation."""

    def __init__(self, snippets_dir: Path, verbose: bool = False):
        self.snippets_dir = snippets_dir
        self.verbose = verbose

    def discover_snippets(self, category: Optional[str] = None) -> list[Path]:
        """Discover all Python snippet files."""
        if not self.snippets_dir.exists():
            return []

        if category:
            search_dir = self.snippets_dir / category
            if not search_dir.exists():
                return []
            snippets = sorted(search_dir.rglob("*.py"))
        else:
            snippets = sorted(self.snippets_dir.rglob("*.py"))

        return snippets

    def get_category(self, snippet_path: Path) -> str:
        """Extract category from snippet path."""
        relative_path = snippet_path.relative_to(self.snippets_dir)
        return str(relative_path.parts[0]) if relative_path.parts else "unknown"

    def validate_snippet(self, snippet_path: Path) -> PySnippetValidationResult:
        """Validate a single Python snippet."""
        result = PySnippetValidationResult(
            file_path=snippet_path,
            category=self.get_category(snippet_path)
        )

        if self.verbose:
            print(f"\nValidating: {snippet_path.relative_to(self.snippets_dir)}")

        start_time = time.time()

        # Read snippet code
        try:
            code = snippet_path.read_text(encoding="utf-8")
        except Exception as e:
            result.passed = False
            result.failed_stage = ValidationStage.SYNTAX
            result.error = f"Failed to read file: {e}"
            return result

        # Stage 1: Syntax Check
        try:
            ast.parse(code)
            if self.verbose:
                print(f"  ✅ Syntax check passed")
        except SyntaxError as e:
            result.passed = False
            result.failed_stage = ValidationStage.SYNTAX
            result.error = f"Syntax error at line {e.lineno}: {e.msg}"
            if self.verbose:
                print(f"  ❌ Syntax error: {e.msg}")
            result.execution_time_ms = (time.time() - start_time) * 1000
            return result

        # Stage 2: Import Check
        # Try to identify imports and check if modules are available
        try:
            imports = self._extract_imports(code)
            for module_name in imports:
                __import__(module_name)
            if self.verbose and imports:
                print(f"  ✅ Imports available: {', '.join(imports[:5])}")
        except ImportError as e:
            result.passed = False
            result.failed_stage = ValidationStage.IMPORTS
            result.error = f"Import error: {e}"
            if self.verbose:
                print(f"  ❌ Import error: {e}")
            result.execution_time_ms = (time.time() - start_time) * 1000
            return result

        # Stage 3: Execution
        # Run the snippet in a subprocess for isolation
        try:
            exec_result = subprocess.run(
                [sys.executable, str(snippet_path)],
                capture_output=True,
                text=True,
                timeout=10,  # 10 second timeout
                cwd=snippet_path.parent
            )

            if exec_result.returncode == 0:
                if self.verbose:
                    print(f"  ✅ Execution successful")
                    if exec_result.stdout.strip():
                        print(f"     Output: {exec_result.stdout.strip()[:100]}")
            else:
                result.passed = False
                result.failed_stage = ValidationStage.EXECUTION
                result.error = exec_result.stderr or "Execution failed with non-zero exit code"
                if self.verbose:
                    print(f"  ❌ Execution failed: {result.error[:200]}")

        except subprocess.TimeoutExpired:
            result.passed = False
            result.failed_stage = ValidationStage.EXECUTION
            result.error = "Execution timeout (>10s)"
            if self.verbose:
                print(f"  ❌ Execution timeout")
        except Exception as e:
            result.passed = False
            result.failed_stage = ValidationStage.EXECUTION
            result.error = str(e)
            if self.verbose:
                print(f"  ❌ Execution error: {e}")

        result.execution_time_ms = (time.time() - start_time) * 1000

        if self.verbose and result.passed:
            print(f"  ✅ PASS ({result.execution_time_ms:.1f}ms)")

        return result

    def _extract_imports(self, code: str) -> list[str]:
        """Extract import statements from Python code."""
        imports = []
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module.split('.')[0])
        except:
            pass
        return imports


def print_summary_report(results: list[PySnippetValidationResult]) -> None:
    """Print validation summary report."""
    total = len(results)
    passed = sum(1 for r in results if r.passed)
    failed = total - passed

    # Category breakdown
    categories = {}
    for result in results:
        cat = result.category
        if cat not in categories:
            categories[cat] = {"total": 0, "passed": 0}
        categories[cat]["total"] += 1
        if result.passed:
            categories[cat]["passed"] += 1

    print("\n" + "="*50)
    print("Python Snippet Validation Report")
    print("="*50)
    print(f"\nSummary:")
    print(f"  Total snippets: {total}")
    print(f"  Passed: {passed} ({passed/total*100:.1f}%)" if total > 0 else "  Passed: 0")
    print(f"  Failed: {failed} ({failed/total*100:.1f}%)" if total > 0 else "  Failed: 0")

    if categories:
        print(f"\nCategory Results:")
        for category, stats in sorted(categories.items()):
            pct = stats["passed"] / stats["total"] * 100 if stats["total"] > 0 else 0
            status = "✅" if stats["passed"] == stats["total"] else "❌"
            print(f"  {status} {category}: {stats['passed']}/{stats['total']} ({pct:.1f}%)")

    # Failed snippets details
    failed_results = [r for r in results if not r.passed]
    if failed_results:
        print(f"\nFailed Snippets:")
        for result in failed_results:
            relative_path = result.file_path.relative_to(result.file_path.parents[2])
            print(f"\n  ❌ {relative_path}")
            print(f"     Stage: {result.failed_stage.value if result.failed_stage else 'Unknown'}")
            if result.error:
                error_str = str(result.error)[:200]
                print(f"     Error: {error_str}")

    print("\n" + "="*50)


def main():
    parser = argparse.ArgumentParser(
        description="Validate Python code snippets in documentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tests/py_snippet_validator.py
  python tests/py_snippet_validator.py --category embedding
  python tests/py_snippet_validator.py --verbose
  python tests/py_snippet_validator.py --ci
        """
    )

    parser.add_argument(
        "--category",
        help="Validate specific category only (e.g., embedding, module-development)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed validation output"
    )
    parser.add_argument(
        "--ci",
        action="store_true",
        help="CI mode: fail fast and exit with non-zero on any failure"
    )
    parser.add_argument(
        "--snippets-dir",
        type=Path,
        default=Path(__file__).parent.parent / "docs" / "py_snippets",
        help="Directory containing Python snippets (default: docs/py_snippets)"
    )

    args = parser.parse_args()

    # Initialize validator
    validator = PySnippetValidator(args.snippets_dir, verbose=args.verbose)

    # Discover snippets
    snippets = validator.discover_snippets(args.category)

    if not snippets:
        if args.category:
            print(f"No Python snippets found in category: {args.category}")
        else:
            print(f"No Python snippets found in: {args.snippets_dir}")
        return 0

    print(f"Found {len(snippets)} Python snippet(s) to validate")
    if args.category:
        print(f"Category: {args.category}")

    # Validate all snippets
    results = []
    for snippet in snippets:
        result = validator.validate_snippet(snippet)
        results.append(result)

        # Fail fast in CI mode
        if args.ci and not result.passed:
            print(f"\n❌ FAILED: {snippet.relative_to(args.snippets_dir)}")
            print(f"Stage: {result.failed_stage.value if result.failed_stage else 'Unknown'}")
            sys.exit(1)

    # Print summary report
    if not args.verbose:
        print_summary_report(results)
    else:
        # Brief summary for verbose mode
        passed = sum(1 for r in results if r.passed)
        print(f"\n{'='*50}")
        print(f"Summary: {passed}/{len(results)} passed ({passed/len(results)*100:.1f}%)")
        print(f"{'='*50}")

    # Exit with appropriate code
    all_passed = all(r.passed for r in results)
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
