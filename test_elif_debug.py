#!/usr/bin/env python3
"""Debug elif transpilation issues."""

import sys
sys.path.insert(0, 'src')

from mlpy.ml.transpiler import MLTranspiler

def test_elif():
    transpiler = MLTranspiler()

    # Test with simple elif ML code
    code = '''
if (x < 10) {
    y = 1;
} elif (x < 20) {
    y = 2;
} else {
    y = 3;
}
'''

    print("Parsing...")
    try:
        ast, issues = transpiler.parse_with_security_analysis(code, "test_elif_debug.ml")
    except Exception as e:
        print(f"Parser exception: {e}")
        import traceback
        traceback.print_exc()
        return

    if ast is None:
        print("PARSING FAILED")
        for issue in issues:
            print(f"  - {issue.error.message}")
        return

    print("Parsing succeeded!")
    print(f"AST has {len(ast.items)} items")

    print("\nTranspiling...")
    python_code, trans_issues, source_map = transpiler.transpile_to_python(
        code, "test_elif_debug.ml", strict_security=False
    )

    if python_code:
        print("TRANSPILATION SUCCEEDED!")
        print("\nGenerated Python code:")
        print("=" * 50)
        print(python_code)
        print("=" * 50)

        # Write to file
        with open("test_elif_debug_output.py", "w") as f:
            f.write(python_code)
        print("Wrote output to test_elif_debug_output.py")
    else:
        print("TRANSPILATION FAILED")
        for issue in trans_issues:
            print(f"  - {issue.error.message}")

if __name__ == "__main__":
    test_elif()