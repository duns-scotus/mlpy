"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

arr = [10, 20, 30, 40, 50]

slice1 = arr[1:3]

slice2 = arr[:2]

slice3 = arr[2:]

result = {'arr': arr, 'slice1': slice1, 'slice2': slice2, 'slice3': slice3}

# End of generated code