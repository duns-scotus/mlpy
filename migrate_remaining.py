"""Migrate remaining function expressions to arrow functions"""
import re

def migrate_all_function_expressions(content):
    """Convert all function expressions to arrow functions, handling various patterns."""

    # Pattern 1: Simple single-return function expressions
    # function(params) { return expr; }  ->  fn(params) => expr
    pattern1 = r'function\(([^)]*)\)\s*\{\s*return\s+([^;]+);\s*\}'
    content = re.sub(pattern1, r'fn(\1) => \2', content)

    # Pattern 2: Multi-statement function expressions with conditionals
    # These need manual review, but we can try to convert simple ones with ternary
    # function(params) { if (cond) { return a; } else { return b; } }
    pattern2 = r'function\(([^)]*)\)\s*\{\s*if\s*\(([^)]+)\)\s*\{\s*return\s+([^;]+);\s*\}\s*else\s*\{\s*return\s+([^;]+);\s*\}\s*\}'
    content = re.sub(pattern2, r'fn(\1) => (\2) ? (\3) : (\4)', content)

    # Pattern 3: Multi-line returns (wrapped expressions)
    # function(x) {\n    return expr\n}
    pattern3 = r'function\(([^)]*)\)\s*\{\s*return\s+([^}]+?)\s*;\s*\}'
    def replace_multiline(match):
        params = match.group(1)
        return_expr = match.group(2).strip()
        # Clean up the expression (remove extra whitespace)
        return_expr = re.sub(r'\s+', ' ', return_expr)
        return f'fn({params}) => {return_expr}'
    content = re.sub(pattern3, replace_multiline, content, flags=re.DOTALL)

    return content

def migrate_file(filepath):
    """Migrate a single ML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    content = migrate_all_function_expressions(content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        # Count changes
        original_count = len(re.findall(r'function\(', original_content))
        remaining_count = len(re.findall(r'function\(', content))
        fixed = original_count - remaining_count

        print(f"[OK] {filepath}")
        print(f"     Fixed {fixed} function expressions, {remaining_count} remain")
        return True
    else:
        print(f"[--] No changes: {filepath}")
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

    print(f"\nMigrated {migrated_count} files")
