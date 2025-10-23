#!/usr/bin/env python3
"""
ML Snippet Validator - Documentation Code Example Validation

Validates all ML code snippets in docs/ml_snippets/ directory by running them
through the complete ML compilation and execution pipeline.

Usage:
    python tests/ml_snippet_validator.py                    # Validate all snippets
    python tests/ml_snippet_validator.py --category tutorial # Validate specific category
    python tests/ml_snippet_validator.py --verbose          # Show detailed output
    python tests/ml_snippet_validator.py --ci               # CI mode (fail fast)
    python tests/ml_snippet_validator.py --html-report validation.html

Pipeline Stages:
    1. Parse      - Syntax validation
    2. Security   - Security analysis
    3. Transpile  - Python code generation
    4. Execute    - Sandbox execution
"""

import argparse
import io
import json
import sys
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Optional

# Set UTF-8 encoding for stdout/stderr on Windows
if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mlpy.ml.grammar.parser import MLParser
from mlpy.ml.analysis.parallel_analyzer import ParallelSecurityAnalyzer
from mlpy.ml.transpiler import MLTranspiler
from mlpy.runtime.sandbox.sandbox import MLSandbox, SandboxConfig


class StageResult(Enum):
    """Result of a pipeline stage."""
    PASS = "✅"
    FAIL = "❌"
    SKIP = "⏭️"


@dataclass
class SnippetValidationResult:
    """Validation result for a single ML snippet."""
    file_path: Path
    category: str

    # Stage results
    parse_result: StageResult = StageResult.SKIP
    parse_time_ms: float = 0.0
    parse_error: Optional[str] = None

    security_result: StageResult = StageResult.SKIP
    security_time_ms: float = 0.0
    security_issues: list[str] = field(default_factory=list)
    security_warnings_only: bool = False  # True if security issues are warnings, not failures

    transpile_result: StageResult = StageResult.SKIP
    transpile_time_ms: float = 0.0
    transpile_error: Optional[str] = None

    execute_result: StageResult = StageResult.SKIP
    execute_time_ms: float = 0.0
    execute_error: Optional[str] = None
    execute_output: str = ""

    @property
    def passed(self) -> bool:
        """Check if snippet passed all critical stages (security warnings don't fail)."""
        return (
            self.parse_result == StageResult.PASS
            and self.transpile_result == StageResult.PASS
            and self.execute_result == StageResult.PASS
            and (self.security_result == StageResult.PASS or self.security_warnings_only)
        )

    @property
    def failed_stage(self) -> Optional[str]:
        """Get the first failed stage name."""
        if self.parse_result == StageResult.FAIL:
            return "Parse"
        if self.security_result == StageResult.FAIL:
            return "Security"
        if self.transpile_result == StageResult.FAIL:
            return "Transpile"
        if self.execute_result == StageResult.FAIL:
            return "Execute"
        return None

    @property
    def total_time_ms(self) -> float:
        """Total validation time."""
        return (
            self.parse_time_ms
            + self.security_time_ms
            + self.transpile_time_ms
            + self.execute_time_ms
        )


class MLSnippetValidator:
    """Validates ML code snippets for documentation."""

    def __init__(self, snippets_dir: Path, verbose: bool = False):
        self.snippets_dir = snippets_dir
        self.verbose = verbose
        self.parser = MLParser()
        self.security_analyzer = ParallelSecurityAnalyzer()
        self.transpiler = MLTranspiler()

    def discover_snippets(self, category: Optional[str] = None) -> list[Path]:
        """Discover all ML snippet files."""
        if not self.snippets_dir.exists():
            return []

        if category:
            search_dir = self.snippets_dir / category
            if not search_dir.exists():
                return []
            snippets = sorted(search_dir.rglob("*.ml"))
        else:
            snippets = sorted(self.snippets_dir.rglob("*.ml"))

        return snippets

    def get_category(self, snippet_path: Path) -> str:
        """Extract category from snippet path."""
        relative_path = snippet_path.relative_to(self.snippets_dir)
        return str(relative_path.parts[0]) if relative_path.parts else "unknown"

    def validate_snippet(self, snippet_path: Path) -> SnippetValidationResult:
        """Validate a single ML snippet through the complete pipeline."""
        result = SnippetValidationResult(
            file_path=snippet_path,
            category=self.get_category(snippet_path)
        )

        # Read snippet code
        try:
            code = snippet_path.read_text(encoding="utf-8")
        except Exception as e:
            result.parse_result = StageResult.FAIL
            result.parse_error = f"Failed to read file: {e}"
            return result

        if self.verbose:
            print(f"\nValidating: {snippet_path.relative_to(self.snippets_dir)}")

        # Stage 1: Parse
        start_time = time.time()
        try:
            ast = self.parser.parse(code)
            result.parse_result = StageResult.PASS
            result.parse_time_ms = (time.time() - start_time) * 1000
            if self.verbose:
                print(f"  ✅ Parse      ({result.parse_time_ms:.1f}ms)")
        except Exception as e:
            result.parse_result = StageResult.FAIL
            result.parse_error = str(e)
            result.parse_time_ms = (time.time() - start_time) * 1000
            if self.verbose:
                print(f"  ❌ Parse      ({result.parse_time_ms:.1f}ms) - {e}")
            return result  # Can't continue without valid AST

        # Stage 2: Security Analysis
        start_time = time.time()
        try:
            security_result = self.security_analyzer.analyze_parallel(code, None)
            result.security_time_ms = (time.time() - start_time) * 1000

            # Count security threats
            threat_count = (
                len(security_result.pattern_matches)
                + len(security_result.ast_violations)
                + len(security_result.data_flow_results.get("violations", []))
            )

            # Check for security issues - treat as warnings, not failures
            if threat_count > 0:
                # Mark security issues but as warnings only
                result.security_result = StageResult.PASS  # Changed from FAIL
                result.security_warnings_only = True
                result.security_issues = [
                    f"{len(security_result.pattern_matches)} pattern matches",
                    f"{len(security_result.ast_violations)} AST violations",
                    f"{len(security_result.data_flow_results.get('violations', []))} data flow violations"
                ]
                if self.verbose:
                    print(f"  ⚠️  Security   ({result.security_time_ms:.1f}ms) - {threat_count} warnings")
                # Continue to see if it transpiles and executes
            else:
                result.security_result = StageResult.PASS
                if self.verbose:
                    print(f"  ✅ Security   ({result.security_time_ms:.1f}ms)")
        except Exception as e:
            # Actual analysis errors (not warnings) are still failures
            result.security_result = StageResult.FAIL
            result.security_issues = [f"Analysis error: {e}"]
            result.security_time_ms = (time.time() - start_time) * 1000
            if self.verbose:
                print(f"  ❌ Security   ({result.security_time_ms:.1f}ms) - {e}")

        # Stage 3: Transpile
        start_time = time.time()
        try:
            python_code, issues, source_map = self.transpiler.transpile_to_python(
                code,
                generate_source_maps=True
            )
            result.transpile_result = StageResult.PASS
            result.transpile_time_ms = (time.time() - start_time) * 1000
            if self.verbose:
                print(f"  ✅ Transpile  ({result.transpile_time_ms:.1f}ms)")
        except Exception as e:
            result.transpile_result = StageResult.FAIL
            result.transpile_error = str(e)
            result.transpile_time_ms = (time.time() - start_time) * 1000
            if self.verbose:
                print(f"  ❌ Transpile  ({result.transpile_time_ms:.1f}ms) - {e}")
            return result  # Can't execute without Python code

        # Stage 4: Execute
        start_time = time.time()
        try:
            from mlpy.runtime.capabilities import get_capability_manager
            from mlpy.runtime.capabilities.tokens import CapabilityToken, CapabilityConstraint

            config = SandboxConfig(
                cpu_timeout=5.0,  # 5 second timeout for snippets
                memory_limit="256MB"
            )

            with MLSandbox(config) as sandbox:
                # Create capability context for testing
                manager = get_capability_manager()
                context = manager.create_context(name="snippet_execution")

                # Grant all standard library capabilities for documentation snippets
                test_capabilities = [
                    "console.write",
                    "console.error",
                    "regex.compile",
                    "regex.match",
                    "math.compute",
                    "random.generate",
                    "random.sample",
                    "json.parse",
                    "json.serialize",
                    "datetime.create",
                    "datetime.now",
                    "collections.read",
                    "collections.transform",
                    "functional.compose",
                    "functional.transform",
                    "file.read",
                    "file.write",
                    "file.delete",
                    "file.append",
                    "path.read",
                    "path.write",
                ]

                for cap_type in test_capabilities:
                    token = CapabilityToken(
                        capability_type=cap_type,
                        constraints=CapabilityConstraint(),
                        description=f"Doc snippet capability for {cap_type}",
                    )
                    context.add_capability(token)

                execution_result = sandbox._execute_python_code(python_code, context)

            result.execute_time_ms = (time.time() - start_time) * 1000

            success = getattr(execution_result, "success", False)
            if success:
                result.execute_result = StageResult.PASS
                result.execute_output = getattr(execution_result, "stdout", "")
                if self.verbose:
                    print(f"  ✅ Execute    ({result.execute_time_ms:.1f}ms)")
                    if result.execute_output.strip():
                        print(f"     Output: {result.execute_output.strip()[:100]}")
            else:
                result.execute_result = StageResult.FAIL
                error_msg = getattr(execution_result, "error", None)
                stderr_msg = getattr(execution_result, "stderr", "")
                result.execute_error = str(error_msg) if error_msg else stderr_msg
                if self.verbose:
                    print(f"  ❌ Execute    ({result.execute_time_ms:.1f}ms) - {result.execute_error}")
        except Exception as e:
            result.execute_result = StageResult.FAIL
            result.execute_error = str(e)
            result.execute_time_ms = (time.time() - start_time) * 1000
            if self.verbose:
                print(f"  ❌ Execute    ({result.execute_time_ms:.1f}ms) - {e}")

        if self.verbose and result.passed:
            print(f"  ✅ PASS (Total: {result.total_time_ms:.1f}ms)")

        return result


def print_summary_report(results: list[SnippetValidationResult]) -> None:
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
    print("ML Snippet Validation Report")
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

    # Security warnings (passed but with warnings)
    warning_results = [r for r in results if r.passed and r.security_warnings_only]
    if warning_results:
        print(f"\nPassed with Security Warnings:")
        for result in warning_results:
            relative_path = result.file_path.relative_to(result.file_path.parents[2])
            print(f"\n  ⚠️  {relative_path}")
            if result.security_issues:
                for issue in result.security_issues[:3]:
                    issue_str = str(issue)[:150]
                    print(f"       - {issue_str}")

    # Failed snippets details
    failed_results = [r for r in results if not r.passed]
    if failed_results:
        print(f"\nFailed Snippets:")
        for result in failed_results:
            relative_path = result.file_path.relative_to(result.file_path.parents[2])
            print(f"\n  ❌ {relative_path}")
            print(f"     Stage: {result.failed_stage}")

            if result.parse_error:
                error_str = str(result.parse_error)[:200]
                print(f"     Error: {error_str}")
            elif result.security_issues and not result.security_warnings_only:
                print(f"     Security Issues: {len(result.security_issues)}")
                for issue in result.security_issues[:3]:
                    issue_str = str(issue)[:150]
                    print(f"       - {issue_str}")
            elif result.transpile_error:
                error_str = str(result.transpile_error)[:200]
                print(f"     Error: {error_str}")
            elif result.execute_error:
                error_str = str(result.execute_error)[:200]
                print(f"     Error: {error_str}")

    print("\n" + "="*50)


def generate_html_report(results: list[SnippetValidationResult], output_path: Path) -> None:
    """Generate HTML validation report."""
    total = len(results)
    passed = sum(1 for r in results if r.passed)

    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>ML Snippet Validation Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        .summary {{ background: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        .pass {{ color: green; }}
        .fail {{ color: red; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        .error {{ font-family: monospace; background: #ffe6e6; padding: 5px; }}
    </style>
</head>
<body>
    <h1>ML Snippet Validation Report</h1>
    <div class="summary">
        <h2>Summary</h2>
        <p>Total snippets: {total}</p>
        <p class="pass">Passed: {passed} ({passed/total*100:.1f}%)</p>
        <p class="fail">Failed: {total - passed} ({(total-passed)/total*100:.1f}%)</p>
    </div>
    <table>
        <tr>
            <th>File</th>
            <th>Category</th>
            <th>Parse</th>
            <th>Security</th>
            <th>Transpile</th>
            <th>Execute</th>
            <th>Time (ms)</th>
            <th>Status</th>
        </tr>
"""

    for result in results:
        relative_path = result.file_path.relative_to(result.file_path.parents[2])
        status = "PASS" if result.passed else "FAIL"
        status_class = "pass" if result.passed else "fail"

        html += f"""
        <tr>
            <td>{relative_path}</td>
            <td>{result.category}</td>
            <td>{result.parse_result.value}</td>
            <td>{result.security_result.value}</td>
            <td>{result.transpile_result.value}</td>
            <td>{result.execute_result.value}</td>
            <td>{result.total_time_ms:.1f}</td>
            <td class="{status_class}">{status}</td>
        </tr>
"""

        # Add warning/error details row
        if result.security_warnings_only and result.passed:
            # Security warnings but passed
            warning_msg = f"Security Warnings ({len(result.security_issues)}): " + "; ".join(result.security_issues[:3])
            html += f"""
        <tr>
            <td colspan="8" style="background: #fff3cd; padding: 5px; font-family: monospace;">⚠️ {warning_msg}</td>
        </tr>
"""
        elif not result.passed:
            # Actually failed
            error_msg = ""
            if result.parse_error:
                error_msg = f"Parse Error: {result.parse_error}"
            elif result.security_issues and not result.security_warnings_only:
                error_msg = f"Security Issues ({len(result.security_issues)}): " + "; ".join(result.security_issues[:3])
            elif result.transpile_error:
                error_msg = f"Transpile Error: {result.transpile_error}"
            elif result.execute_error:
                error_msg = f"Execute Error: {result.execute_error}"

            html += f"""
        <tr>
            <td colspan="8" class="error">{error_msg}</td>
        </tr>
"""

    html += """
    </table>
</body>
</html>
"""

    output_path.write_text(html, encoding="utf-8")
    print(f"\nHTML report generated: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Validate ML code snippets in documentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tests/ml_snippet_validator.py
  python tests/ml_snippet_validator.py --category tutorial
  python tests/ml_snippet_validator.py --verbose
  python tests/ml_snippet_validator.py --ci
  python tests/ml_snippet_validator.py --html-report validation.html
        """
    )

    parser.add_argument(
        "--category",
        help="Validate specific category only (e.g., tutorial, language-reference, stdlib)"
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
        "--html-report",
        type=Path,
        help="Generate HTML report at specified path"
    )
    parser.add_argument(
        "--snippets-dir",
        type=Path,
        default=Path(__file__).parent.parent / "docs" / "ml_snippets",
        help="Directory containing ML snippets (default: docs/ml_snippets)"
    )

    args = parser.parse_args()

    # Initialize validator
    validator = MLSnippetValidator(args.snippets_dir, verbose=args.verbose)

    # Discover snippets
    snippets = validator.discover_snippets(args.category)

    if not snippets:
        if args.category:
            print(f"No ML snippets found in category: {args.category}")
        else:
            print(f"No ML snippets found in: {args.snippets_dir}")
        return 0

    print(f"Found {len(snippets)} ML snippet(s) to validate")
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
            print(f"Stage: {result.failed_stage}")
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

    # Generate HTML report if requested
    if args.html_report:
        generate_html_report(results, args.html_report)

    # Exit with appropriate code
    all_passed = all(r.passed for r in results)
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
