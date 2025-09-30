"""Migrate function(x) { return expr; } to fn(x) => expr"""
import re
import sys

def migrate_simple_function_expressions(content):
    """Convert simple function expressions with single return statement to arrow functions."""

    # Pattern: function(params) { return expr; }
    # This handles single-line returns
    pattern = r'function\(([^)]*)\)\s*\{\s*return\s+([^;]+);\s*\}'
    replacement = r'fn(\1) => \2'

    content = re.sub(pattern, replacement, content)

    return content

def migrate_file(filepath):
    """Migrate a single ML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    content = migrate_simple_function_expressions(content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[OK] Migrated: {filepath}")
        return True
    else:
        print(f"[--] No changes: {filepath}")
        return False

if __name__ == "__main__":
    files = [
        "tests/ml_integration/language_coverage/demo_functional_power.ml",
        "tests/ml_integration/language_coverage/test_functional_module.ml",
        "tests/ml_integration/language_coverage/test_import_system.ml",
        "tests/ml_integration/language_coverage/advanced_control_flow_and_functions.ml",
        "tests/ml_integration/language_coverage/complete_language_fundamentals.ml",
        "tests/ml_integration/language_coverage/comprehensive_object_operations_old.ml",
        "tests/ml_integration/language_coverage/sprint7_advanced_features.ml",
    ]

    migrated_count = 0
    for filepath in files:
        try:
            if migrate_file(filepath):
                migrated_count += 1
        except Exception as e:
            print(f"[ERROR] in {filepath}: {e}")

    print(f"\nMigrated {migrated_count} files")
