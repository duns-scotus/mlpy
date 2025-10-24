"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin

def test():
    abs_func = builtin.abs
    result = _safe_call(builtin.call, abs_func, -42)
    return result

test()

# End of generated code