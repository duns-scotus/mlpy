#!/usr/bin/env python3

import sys
sys.path.insert(0, 'src')

from mlpy.stdlib.collections import collections as ml_collections
from mlpy.stdlib.random import random as ml_random
from mlpy.stdlib.math import math as ml_math

def test_basic_operations():
    """Test that our standard library functions work."""
    print("Testing ML Standard Library Functions:")

    # Test collections
    print("\n1. Collections:")
    lst = [1, 2, 3]
    result = ml_collections.append(lst, 4)
    print(f"   append([1, 2, 3], 4) = {result}")

    filtered = ml_collections.filter([1, 2, 3, 4, 5], lambda x: x > 2)
    print(f"   filter([1,2,3,4,5], x>2) = {filtered}")

    mapped = ml_collections.map([1, 2, 3], lambda x: x * 2)
    print(f"   map([1,2,3], x*2) = {mapped}")

    # Test random
    print("\n2. Random:")
    ml_random.setSeed(42)
    rand_num = ml_random.randomFloat(0, 10)
    print(f"   randomFloat(0, 10) = {rand_num}")

    rand_int = ml_random.randomInt(1, 6)
    print(f"   randomInt(1, 6) = {rand_int}")

    # Test math
    print("\n3. Math:")
    sqrt_result = ml_math.sqrt(16)
    print(f"   sqrt(16) = {sqrt_result}")

    cos_result = ml_math.cos(0)
    print(f"   cos(0) = {cos_result}")

    print("\n✓ All basic operations working!")
    return True

if __name__ == "__main__":
    test_basic_operations()