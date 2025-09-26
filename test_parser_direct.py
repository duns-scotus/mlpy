#!/usr/bin/env python3
"""Test parser directly."""

import sys
sys.path.insert(0, 'src')

from mlpy.ml.grammar.parser import MLParser

def test_parser():
    parser = MLParser()

    # Test simple elif
    code = '''
if (x < 10) {
    y = 1;
} elif (x < 20) {
    y = 2;
}
'''

    print("Testing elif parsing directly...")
    try:
        ast = parser.parse(code, "test.ml")
        if ast:
            print("SUCCESS: Parsing worked!")
            print(f"AST: {ast}")

            # Test transpilation directly
            print("\nTesting transpilation...")
            from mlpy.ml.codegen.python_generator import generate_python_code

            python_code, source_map = generate_python_code(ast, "test.ml", False)
            if python_code:
                print("SUCCESS: Transpilation worked!")
                print("Generated Python:")
                print("=" * 40)
                print(python_code)
                print("=" * 40)
            else:
                print("FAILED: Transpilation returned None")

            # Test security analysis
            print("\nTesting security analysis...")
            from mlpy.ml.analysis.security_analyzer import SecurityAnalyzer
            analyzer = SecurityAnalyzer("test.ml")
            issues = analyzer.analyze(ast)
            print(f"Security analysis found {len(issues)} issues")
            for issue in issues:
                print(f"  - {issue.error.message}")
        else:
            print("FAILED: Parser returned None")
    except Exception as e:
        print(f"EXCEPTION: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_parser()