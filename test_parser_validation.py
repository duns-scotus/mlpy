#!/usr/bin/env python3
"""
Systematic validation of all ML test files created.
Tests each file with the ML parser to identify syntax errors vs parser issues.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any
import json
import time

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from mlpy.ml.grammar.parser import MLParser


def test_file_parsing(file_path: str) -> Dict[str, Any]:
    """Test a single ML file with the parser."""
    parser = MLParser()

    try:
        print(f"Testing: {file_path}")

        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        line_count = len(content.splitlines())
        char_count = len(content)

        # Try to parse
        start_time = time.perf_counter()
        ast = parser.parse_file(file_path)
        parse_time = time.perf_counter() - start_time

        print(f"  [PASS] Parsed successfully ({parse_time:.3f}s, {line_count} lines, {char_count} chars)")

        return {
            "file": file_path,
            "status": "PASS",
            "line_count": line_count,
            "char_count": char_count,
            "parse_time": parse_time,
            "ast_type": type(ast).__name__,
            "error": None
        }

    except Exception as e:
        print(f"  [FAIL] {type(e).__name__}: {str(e)}")

        # Try to read file stats even if parsing fails
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            line_count = len(content.splitlines())
            char_count = len(content)
        except:
            line_count = 0
            char_count = 0

        return {
            "file": file_path,
            "status": "FAIL",
            "line_count": line_count,
            "char_count": char_count,
            "parse_time": 0,
            "ast_type": None,
            "error": {
                "type": type(e).__name__,
                "message": str(e)
            }
        }


def find_test_files() -> List[str]:
    """Find all ML test files created."""
    test_files = []

    # Find files in language_coverage directory
    lang_coverage_dir = Path("tests/ml_integration/language_coverage")
    if lang_coverage_dir.exists():
        for file_path in lang_coverage_dir.glob("*.ml"):
            test_files.append(str(file_path))

    # Find example files
    examples_dir = Path("examples")
    if examples_dir.exists():
        for file_path in examples_dir.glob("*.ml"):
            test_files.append(str(file_path))

    return sorted(test_files)


def analyze_results(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze test results and identify patterns."""

    passed = [r for r in results if r["status"] == "PASS"]
    failed = [r for r in results if r["status"] == "FAIL"]

    # Analyze error patterns
    error_patterns = {}
    for result in failed:
        if result["error"]:
            error_type = result["error"]["type"]
            error_msg = result["error"]["message"]

            if error_type not in error_patterns:
                error_patterns[error_type] = []
            error_patterns[error_type].append({
                "file": result["file"],
                "message": error_msg
            })

    # Calculate statistics
    total_lines = sum(r["line_count"] for r in results)
    total_chars = sum(r["char_count"] for r in results)
    avg_parse_time = sum(r["parse_time"] for r in passed) / len(passed) if passed else 0

    return {
        "summary": {
            "total_files": len(results),
            "passed": len(passed),
            "failed": len(failed),
            "pass_rate": len(passed) / len(results) * 100 if results else 0,
            "total_lines": total_lines,
            "total_chars": total_chars,
            "avg_parse_time": avg_parse_time
        },
        "passed_files": [r["file"] for r in passed],
        "failed_files": [r["file"] for r in failed],
        "error_patterns": error_patterns,
        "detailed_results": results
    }


def main():
    """Main testing function."""
    print("=" * 60)
    print("ML TEST FILES PARSER VALIDATION")
    print("=" * 60)

    # Find all test files
    test_files = find_test_files()

    if not test_files:
        print("[ERROR] No ML test files found!")
        return

    print(f"Found {len(test_files)} ML test files to validate\n")

    # Test each file
    results = []
    for file_path in test_files:
        result = test_file_parsing(file_path)
        results.append(result)

    print("\n" + "=" * 60)
    print("PARSER VALIDATION SUMMARY")
    print("=" * 60)

    # Analyze results
    analysis = analyze_results(results)
    summary = analysis["summary"]

    print(f"Total files tested: {summary['total_files']}")
    print(f"Passed: {summary['passed']}")
    print(f"Failed: {summary['failed']}")
    print(f"Pass rate: {summary['pass_rate']:.1f}%")
    print(f"Total lines of code: {summary['total_lines']:,}")
    print(f"Total characters: {summary['total_chars']:,}")
    print(f"Average parse time: {summary['avg_parse_time']:.3f}s")

    if analysis["failed_files"]:
        print(f"\n[FAILED FILES] ({len(analysis['failed_files'])}):")
        for file_path in analysis["failed_files"]:
            print(f"  - {file_path}")

    if analysis["error_patterns"]:
        print(f"\n[ERROR PATTERNS]:")
        for error_type, errors in analysis["error_patterns"].items():
            print(f"  {error_type}: {len(errors)} occurrences")
            for error in errors[:3]:  # Show first 3 examples
                file_name = os.path.basename(error["file"])
                print(f"    - {file_name}: {error['message'][:100]}...")
            if len(errors) > 3:
                print(f"    ... and {len(errors) - 3} more")

    # Save detailed results
    with open("parser_validation_results.json", "w") as f:
        json.dump(analysis, f, indent=2)

    print(f"\n[REPORT] Detailed results saved to: parser_validation_results.json")

    return analysis


if __name__ == "__main__":
    main()