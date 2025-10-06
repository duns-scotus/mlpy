"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

def test_slicing():
    arr = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    slice1 = arr[1:4]
    slice2 = arr[0:3]
    slice3 = arr[:5]
    slice4 = arr[3:]
    slice5 = arr[:]
    last = arr[-1]
    second_last = arr[-2]
    slice6 = arr[-3:-1]
    slice7 = arr[-5:]
    slice8 = arr[::2]
    slice9 = arr[1::2]
    slice10 = arr[::-1]
    return {'slice1': slice1, 'slice2': slice2, 'slice3': slice3, 'slice4': slice4, 'slice5': slice5, 'last': last, 'second_last': second_last, 'slice6': slice6, 'slice7': slice7, 'slice8': slice8, 'slice9': slice9, 'slice10': slice10}

result = test_slicing()

# End of generated code