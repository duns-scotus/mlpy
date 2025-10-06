"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

def test_finally_with_return():
    value = 0
    try:
        value = 10
        return value
    finally:
        value = 20
    return value

result = test_finally_with_return()

# End of generated code