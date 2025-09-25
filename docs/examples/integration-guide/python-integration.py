"""
Python Integration Example
Demonstrates how to integrate mlpy transpiler into Python applications
"""

from mlpy.transpiler import MLTranspiler
from mlpy.runtime.sandbox import SandboxManager
from mlpy.ml.errors import MLError

def integrate_ml_code():
    """Example of integrating ML code into Python application."""

    # Initialize transpiler
    transpiler = MLTranspiler()

    # ML source code
    ml_code = '''
    // Simple ML computation
    function calculate_interest(principal, rate, time) {
        return principal * rate * time / 100
    }

    // Calculate compound interest
    principal = 1000
    rate = 5
    time = 2

    simple_interest = calculate_interest(principal, rate, time)
    compound_interest = principal * ((1 + rate/100) ** time - 1)

    print("Simple Interest: " + simple_interest)
    print("Compound Interest: " + compound_interest)
    '''

    try:
        # Transpile ML to Python
        result = transpiler.transpile_string(ml_code)

        if result.success:
            print("Transpilation successful!")
            print("Generated Python code:")
            print(result.python_code)

            # Execute in sandbox for security
            sandbox = SandboxManager()
            execution_result = sandbox.execute_code(result.python_code)

            if execution_result.success:
                print("\nExecution output:")
                print(execution_result.output)
            else:
                print(f"Execution failed: {execution_result.error}")

        else:
            print("Transpilation failed:")
            for error in result.errors:
                print(f"  - {error}")

    except MLError as e:
        print(f"ML Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def batch_transpile_files():
    """Example of batch transpiling multiple ML files."""

    import os
    from pathlib import Path

    transpiler = MLTranspiler()
    ml_files = Path("examples").glob("**/*.ml")

    results = {}

    for ml_file in ml_files:
        print(f"Processing {ml_file}...")

        try:
            result = transpiler.transpile_file(str(ml_file))
            results[str(ml_file)] = result

            if result.success:
                # Save transpiled Python file
                py_file = ml_file.with_suffix('.py')
                py_file.write_text(result.python_code)
                print(f"  -> Generated {py_file}")
            else:
                print(f"  -> Failed: {', '.join(result.errors)}")

        except Exception as e:
            print(f"  -> Error: {e}")

    return results

if __name__ == "__main__":
    print("=== ML Integration Example ===")
    integrate_ml_code()

    print("\n=== Batch Processing Example ===")
    batch_transpile_files()