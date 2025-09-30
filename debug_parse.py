from mlpy.ml.transpiler import MLTranspiler
import traceback

t = MLTranspiler()

# Test math module
print("=" * 60)
print("Testing math module import:")
print("=" * 60)
try:
    with open('test_math.ml') as f:
        code = f.read()
    print("ML Code:")
    print(code)
    print("\nParsing...")
    ast, issues = t.parse_with_security_analysis(code, 'test_math.ml')
    print(f"Parse success: {ast is not None}")
    print(f"Issues: {len(issues)}")
    if issues:
        for issue in issues:
            print(f"  - {issue}")

    if ast:
        from mlpy.ml.codegen.python_generator import generate_python_code
        python_code = generate_python_code(ast)
        print("\nGenerated Python:")
        print(python_code)
except Exception as e:
    print(f"ERROR: {e}")
    traceback.print_exc()

print("\n" + "=" * 60)
print("Testing datetime module import:")
print("=" * 60)
try:
    with open('test_imports.ml') as f:
        code = f.read()
    print("ML Code:")
    print(code)
    print("\nParsing...")
    ast, issues = t.parse_with_security_analysis(code, 'test_imports.ml')
    print(f"Parse success: {ast is not None}")
    print(f"Issues: {len(issues)}")
    if issues:
        for issue in issues:
            print(f"  - {issue}")

    if ast:
        from mlpy.ml.codegen.python_generator import generate_python_code
        python_code = generate_python_code(ast)
        print("\nGenerated Python:")
        print(python_code)
except Exception as e:
    print(f"ERROR: {e}")
    traceback.print_exc()
