"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

def create_counter(initial):
    count = initial
    def increment():
        nonlocal count
        count = (count + 1)
        return count
    return increment

counter = create_counter(10)

result1 = _safe_call(counter)

result2 = _safe_call(counter)

result3 = _safe_call(counter)

# End of generated code