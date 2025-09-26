#!/usr/bin/env python3

# Test if the standard library imports work
print("Testing imports...")

try:
    import sys
    sys.path.insert(0, 'src')

    from mlpy.stdlib import collections, random, math
    print("SUCCESS: Successfully imported stdlib modules")

    # Test basic function calls
    result = collections.append([1, 2], 3)
    print(f"SUCCESS: collections.append([1, 2], 3) = {result}")

    num = random.random()
    print(f"SUCCESS: random.random() = {num}")

    sqrt_val = math.sqrt(16)
    print(f"SUCCESS: math.sqrt(16) = {sqrt_val}")

except Exception as e:
    print(f"FAILED: Import failed: {e}")
    import traceback
    traceback.print_exc()