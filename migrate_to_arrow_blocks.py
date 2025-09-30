"""Migrate function expressions to arrow functions with block bodies"""
import re

def migrate_to_arrow_functions(content):
    """Convert function(...) { ... } to fn(...) => { ... }"""

    # Pattern: function(params) { body }
    # This matches multi-line function expressions
    pattern = r'\bfunction\s*\(([^)]*)\)\s*\{'
    replacement = r'fn(\1) => {'

    content = re.sub(pattern, replacement, content)

    return content

def migrate_file(filepath):
    """Migrate a single ML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    content = migrate_to_arrow_functions(content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        # Count changes
        original_count = len(re.findall(r'\bfunction\s*\(', original_content))
        remaining_count = len(re.findall(r'\bfunction\s*\(', content))
        fixed = original_count - remaining_count

        print(f"[OK] {filepath}")
        print(f"     Converted {fixed} function expressions to arrow functions")
        return True
    else:
        print(f"[--] No changes needed: {filepath}")
        return False

if __name__ == "__main__":
    files = [
        "tests/ml_integration/language_coverage/demo_functional_power.ml",
        "tests/ml_integration/language_coverage/test_functional_module.ml",
        "tests/ml_integration/language_coverage/test_import_system.ml",
        "tests/ml_integration/language_coverage/comprehensive_object_operations_old.ml",
    ]

    migrated_count = 0
    for filepath in files:
        try:
            if migrate_file(filepath):
                migrated_count += 1
        except Exception as e:
            print(f"[ERROR] in {filepath}: {e}")
            import traceback
            traceback.print_exc()

    print(f"\nMigrated {migrated_count} files")
