#!/usr/bin/env python3
"""
REPL Doctest Runner - Documentation REPL Transcript Validation

Executes and verifies REPL transcript files in docs/repl_snippets/ directory
by running commands through ML REPL and comparing actual vs expected outputs.

Usage:
    python tests/repl_doctest_runner.py                       # Run all transcripts
    python tests/repl_doctest_runner.py --category tutorial   # Run specific category
    python tests/repl_doctest_runner.py --verbose             # Show detailed output
    python tests/repl_doctest_runner.py --ci                  # CI mode (fail fast)

Transcript Format (doctest-style):
    # Comment or section header
    ml> x = 10;
    ml> x + 20
    30
    ml> .vars
    Variables in scope:
      x: 10
"""

import argparse
import io
import re
import sys
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional

# Set UTF-8 encoding for stdout/stderr on Windows
if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mlpy.cli.repl import MLREPLSession


class CommandType(Enum):
    """Type of REPL command."""
    ML_CODE = "ml_code"        # Regular ML code: ml> x = 10;
    REPL_CMD = "repl_cmd"      # REPL commands: ml> .vars
    COMMENT = "comment"        # Comments: # Some comment
    OUTPUT = "output"          # Expected output lines


@dataclass
class TranscriptCommand:
    """A single command in a transcript."""
    line_no: int
    type: CommandType
    content: str
    expected_output: list[str] = field(default_factory=list)


@dataclass
class TranscriptValidationResult:
    """Validation result for a single REPL transcript."""
    file_path: Path
    category: str
    passed: bool = True
    failed_line: Optional[int] = None
    failed_command: Optional[str] = None
    expected: Optional[str] = None
    actual: Optional[str] = None
    error: Optional[str] = None
    total_time_ms: float = 0.0
    commands_executed: int = 0


class REPLDoctestRunner:
    """Runs and validates REPL transcript files."""

    def __init__(self, snippets_dir: Path, verbose: bool = False):
        self.snippets_dir = snippets_dir
        self.verbose = verbose
        self.repl_session: Optional[MLREPLSession] = None

    def discover_transcripts(self, category: Optional[str] = None) -> list[Path]:
        """Discover all transcript files."""
        if not self.snippets_dir.exists():
            return []

        if category:
            search_dir = self.snippets_dir / category
            if not search_dir.exists():
                return []
            transcripts = sorted(search_dir.rglob("*.transcript"))
        else:
            transcripts = sorted(self.snippets_dir.rglob("*.transcript"))

        return transcripts

    def get_category(self, transcript_path: Path) -> str:
        """Extract category from transcript path."""
        relative_path = transcript_path.relative_to(self.snippets_dir)
        return str(relative_path.parts[0]) if relative_path.parts else "unknown"

    def parse_transcript(self, transcript_path: Path) -> list[TranscriptCommand]:
        """Parse a transcript file into commands."""
        commands = []
        lines = transcript_path.read_text(encoding="utf-8").splitlines()

        i = 0
        while i < len(lines):
            line = lines[i]
            line_no = i + 1

            # Skip empty lines
            if not line.strip():
                i += 1
                continue

            # Comments (start with #)
            if line.startswith("#"):
                commands.append(TranscriptCommand(
                    line_no=line_no,
                    type=CommandType.COMMENT,
                    content=line
                ))
                i += 1
                continue

            # REPL prompt (ml>)
            if line.startswith("ml>"):
                # Extract command after prompt
                cmd_content = line[3:].strip()

                # Check if it's a REPL special command (.vars, .grant, etc.)
                if cmd_content.startswith("."):
                    cmd_type = CommandType.REPL_CMD
                else:
                    cmd_type = CommandType.ML_CODE

                # Collect expected output (lines that don't start with ml> or #)
                expected_output = []
                j = i + 1
                while j < len(lines):
                    next_line = lines[j]
                    if next_line.startswith("ml>") or next_line.startswith("#") or not next_line.strip():
                        break
                    expected_output.append(next_line)
                    j += 1

                commands.append(TranscriptCommand(
                    line_no=line_no,
                    type=cmd_type,
                    content=cmd_content,
                    expected_output=expected_output
                ))

                i = j  # Skip to next command
                continue

            # Unexpected line format
            i += 1

        return commands

    def execute_transcript(self, transcript_path: Path) -> TranscriptValidationResult:
        """Execute a transcript and validate outputs."""
        result = TranscriptValidationResult(
            file_path=transcript_path,
            category=self.get_category(transcript_path)
        )

        if self.verbose:
            print(f"\nExecuting: {transcript_path.relative_to(self.snippets_dir)}")

        start_time = time.time()

        try:
            # Parse transcript
            commands = self.parse_transcript(transcript_path)

            # Create fresh REPL session for this transcript
            self.repl_session = MLREPLSession(security_enabled=False, profile=False)

            # Execute each command
            for cmd in commands:
                if cmd.type == CommandType.COMMENT:
                    if self.verbose:
                        print(f"  {cmd.content}")
                    continue

                if cmd.type == CommandType.ML_CODE:
                    # Execute ML code
                    exec_result = self.repl_session.execute_ml_line(cmd.content)
                    result.commands_executed += 1

                    if self.verbose:
                        print(f"  ml> {cmd.content}")

                    if not exec_result.success:
                        result.passed = False
                        result.failed_line = cmd.line_no
                        result.failed_command = cmd.content
                        result.error = exec_result.error
                        if self.verbose:
                            print(f"    ❌ Error: {exec_result.error}")
                        break

                    # Check expected output
                    if cmd.expected_output:
                        # Get actual output value
                        actual = str(exec_result.value) if exec_result.value is not None else ""
                        expected = "\n".join(cmd.expected_output).strip()

                        if actual.strip() != expected.strip():
                            result.passed = False
                            result.failed_line = cmd.line_no
                            result.failed_command = cmd.content
                            result.expected = expected
                            result.actual = actual
                            if self.verbose:
                                print(f"    ❌ Expected: {expected}")
                                print(f"       Actual:   {actual}")
                            break

                        if self.verbose and actual:
                            print(f"    {actual}")

                elif cmd.type == CommandType.REPL_CMD:
                    # Handle REPL special commands
                    result.commands_executed += 1

                    if self.verbose:
                        print(f"  ml> {cmd.content}")

                    # For now, skip special commands (not implemented in programmatic use)
                    # In a full implementation, we'd handle .vars, .grant, .reset, etc.
                    if self.verbose:
                        print(f"    ⏭️  Skipped (REPL command)")
                    continue

        except Exception as e:
            result.passed = False
            result.error = str(e)
            if self.verbose:
                print(f"  ❌ Exception: {e}")

        result.total_time_ms = (time.time() - start_time) * 1000

        if self.verbose and result.passed:
            print(f"  ✅ PASS ({result.commands_executed} commands, {result.total_time_ms:.1f}ms)")

        return result


def print_summary_report(results: list[TranscriptValidationResult]) -> None:
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
    print("REPL Transcript Validation Report")
    print("="*50)
    print(f"\nSummary:")
    print(f"  Total transcripts: {total}")
    print(f"  Passed: {passed} ({passed/total*100:.1f}%)" if total > 0 else "  Passed: 0")
    print(f"  Failed: {failed} ({failed/total*100:.1f}%)" if total > 0 else "  Failed: 0")

    if categories:
        print(f"\nCategory Results:")
        for category, stats in sorted(categories.items()):
            pct = stats["passed"] / stats["total"] * 100 if stats["total"] > 0 else 0
            status = "✅" if stats["passed"] == stats["total"] else "❌"
            print(f"  {status} {category}: {stats['passed']}/{stats['total']} ({pct:.1f}%)")

    # Failed transcripts details
    failed_results = [r for r in results if not r.passed]
    if failed_results:
        print(f"\nFailed Transcripts:")
        for result in failed_results:
            relative_path = result.file_path.relative_to(result.file_path.parents[2])
            print(f"\n  ❌ {relative_path}")
            if result.failed_line:
                print(f"     Line {result.failed_line}: {result.failed_command}")
            if result.expected and result.actual:
                print(f"     Expected: {result.expected[:100]}")
                print(f"     Actual:   {result.actual[:100]}")
            elif result.error:
                error_str = str(result.error)[:200]
                print(f"     Error: {error_str}")

    print("\n" + "="*50)


def main():
    parser = argparse.ArgumentParser(
        description="Run and validate REPL transcript files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tests/repl_doctest_runner.py
  python tests/repl_doctest_runner.py --category tutorial
  python tests/repl_doctest_runner.py --verbose
  python tests/repl_doctest_runner.py --ci
        """
    )

    parser.add_argument(
        "--category",
        help="Run specific category only (e.g., tutorial, stdlib, advanced)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed execution output"
    )
    parser.add_argument(
        "--ci",
        action="store_true",
        help="CI mode: fail fast and exit with non-zero on any failure"
    )
    parser.add_argument(
        "--snippets-dir",
        type=Path,
        default=Path(__file__).parent.parent / "docs" / "repl_snippets",
        help="Directory containing REPL transcripts (default: docs/repl_snippets)"
    )

    args = parser.parse_args()

    # Initialize runner
    runner = REPLDoctestRunner(args.snippets_dir, verbose=args.verbose)

    # Discover transcripts
    transcripts = runner.discover_transcripts(args.category)

    if not transcripts:
        if args.category:
            print(f"No REPL transcripts found in category: {args.category}")
        else:
            print(f"No REPL transcripts found in: {args.snippets_dir}")
        return 0

    print(f"Found {len(transcripts)} REPL transcript(s) to validate")
    if args.category:
        print(f"Category: {args.category}")

    # Execute all transcripts
    results = []
    for transcript in transcripts:
        result = runner.execute_transcript(transcript)
        results.append(result)

        # Fail fast in CI mode
        if args.ci and not result.passed:
            print(f"\n❌ FAILED: {transcript.relative_to(args.snippets_dir)}")
            if result.failed_line:
                print(f"Line {result.failed_line}: {result.failed_command}")
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
