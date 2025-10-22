"""
Demo: PySide6 ML Calculator Functions
Shows ML calculator working with CapabilityContext
"""
import sys
from pathlib import Path

# Add src to path so imports work properly
sys.path.insert(0, str(Path.cwd() / 'src'))

from mlpy.ml.transpiler import MLTranspiler
from mlpy.runtime.capabilities import CapabilityContext, create_capability_token
from mlpy.runtime.capabilities.context import capability_context

# Load the ML calculator code
ml_file = Path('examples/integration/gui/pyside6/ml_calculator.ml')
print('=== ML-Powered Calculator Demo ===\n')

transpiler = MLTranspiler()
with open(ml_file, encoding='utf-8') as f:
    ml_code = f.read()

# Transpile
python_code, issues, _ = transpiler.transpile_to_python(
    ml_code, source_file=str(ml_file), strict_security=False
)

# Execute to get functions
namespace = {}
exec(python_code, namespace)

# Extract functions
add = namespace['add']
subtract = namespace['subtract']
multiply = namespace['multiply']
divide = namespace['divide']
calculate_compound_interest = namespace['calculate_compound_interest']
fibonacci = namespace['fibonacci']
calculate_statistics = namespace['calculate_statistics']

print('Testing ML Calculator Functions (with CapabilityContext)\n')

# Test basic arithmetic (no capabilities needed)
print('--- Basic Arithmetic ---')
print(f'15 + 27 = {add(15, 27)}')
print(f'50 - 23 = {subtract(50, 23)}')
print(f'7 × 8 = {multiply(7, 8)}')
print(f'100 ÷ 4 = {divide(100, 4)}')
print(f'10 ÷ 0 = {divide(10, 0)} (safely handles division by zero)\n')

# Test compound interest (requires math capability)
print('--- Compound Interest Calculator ---')

# Create a capability context and add the math.compute capability
ctx = CapabilityContext(name="calculator_demo")
math_token = create_capability_token("math.compute", description="Math computation capability")
ctx.add_capability(math_token)

with capability_context(ctx):
    result = calculate_compound_interest(1000, 5, 3)
    print(f'Investment: ${result["principal"]}')
    print(f'Annual Rate: {result["rate"]}%')
    print(f'Years: {result["years"]}')
    print(f'Final Amount: ${result["amount"]:.2f}')
    print(f'Interest Earned: ${result["interest"]:.2f}\n')

# Test fibonacci (requires math capability)
print('--- Fibonacci Sequence ---')
with capability_context(ctx):
    for n in [5, 10, 15, 20]:
        result = fibonacci(n)
        print(f'Fibonacci({n}) = {result}')
    print()

# Test statistics (requires math capability)
print('--- Statistical Analysis ---')
test_data = [23, 45, 67, 12, 89, 34, 56, 78, 90, 45]
print(f'Dataset: {test_data}\n')

with capability_context(ctx):
    stats = calculate_statistics(test_data)
    print(f'Stats: {stats}')

print('\n=== All ML Calculator Functions Working! ===')
