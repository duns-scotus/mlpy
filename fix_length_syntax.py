#!/usr/bin/env python3
"""Fix .length() to collections.length() in ML files."""

import re
import sys

def fix_length_syntax(content):
    """Replace array.length() with collections.length(array)."""
    # Pattern to match: identifier.length()
    # Captures the identifier before .length()
    pattern = r'(\w+)\.length\(\)'
    replacement = r'collections.length(\1)'
    return re.sub(pattern, replacement, content)

def main():
    filename = "tests/ml_integration/language_coverage/comprehensive_mathematical_operations.ml"

    # Read the file
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix the syntax
    fixed_content = fix_length_syntax(content)

    # Write back to file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(fixed_content)

    print(f"Fixed .length() patterns in {filename}")

if __name__ == "__main__":
    main()