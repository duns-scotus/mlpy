"""
Example: Basic ML Code Execution
Category: embedding
Demonstrates: How to execute ML code from Python
"""

import sys
from pathlib import Path

# Add src to path for example
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

from mlpy.ml.transpiler import MLTranspiler


def main():
    """Execute simple ML code."""

    # ML code to execute
    ml_code = """
    x = 10;
    y = 20;
    result = x + y;
    """

    # Create transpiler
    transpiler = MLTranspiler()

    # Transpile ML code to Python
    python_code, issues, source_map = transpiler.transpile_to_python(ml_code)

    # Execute generated Python code
    namespace = {}
    exec(python_code, namespace)

    # Get result
    result = namespace.get('result')
    print(f"Result: {result}")
    assert result == 30, f"Expected 30, got {result}"

    print("✅ Example completed successfully")


if __name__ == "__main__":
    main()
