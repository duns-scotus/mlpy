from mlpy.ml.transpiler import MLTranspiler

t = MLTranspiler()
code = open('tests/ml_integration/language_coverage/test_functional_module.ml').read()
python_code, _, _ = t.transpile_to_python(code, 'test_functional_module.ml')

lines = python_code.split('\n')
for i, line in enumerate(lines):
    if 'evens' in line.lower():
        print(f'{i+1:4}: {line}')
