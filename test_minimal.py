#!/usr/bin/env python3

from mlpy.stdlib.collections import collections

def test_function():
    alive_prey = collections.filter([1, 2, 3], lambda x: x > 1)
    return alive_prey

print("Testing minimal case...")
result = test_function()
print(f"Result: {result}")