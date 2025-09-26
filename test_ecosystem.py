#!/usr/bin/env python3

from mlpy.ml.transpiler import transpile_ml_code

def test_ecosystem():
    with open('docs/examples/advanced/ecosystem-sim/main.ml', 'r') as f:
        source = f.read()

    result = transpile_ml_code(source, 'main.ml')

    # Handle if result is a tuple
    if isinstance(result, tuple):
        generated_code = result[0]
        print(f"Result is tuple with {len(result)} elements")
    else:
        generated_code = result

    print(f"Generated code length: {len(generated_code)}")
    print("First 500 chars:")
    print(generated_code[:500])
    print("\n" + "="*50 + "\n")

    # Check for unknown identifiers
    unknown_count = generated_code.count('ml_unknown_identifier')
    if unknown_count > 0:
        print(f"WARNING: Found {unknown_count} unknown identifiers in generated code")

        # Show some examples
        lines = generated_code.split('\n')
        unknown_lines = [line for line in lines if 'ml_unknown_identifier' in line][:5]
        print("Example unknown identifier lines:")
        for line in unknown_lines:
            print(f"  {line.strip()}")
    else:
        print("SUCCESS: No unknown identifiers found!")

    # Try to save the generated Python code
    with open('docs/examples/advanced/ecosystem-sim/main.py', 'w') as f:
        f.write(generated_code)
    print("Generated Python code saved to main.py")

if __name__ == "__main__":
    test_ecosystem()