"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.ml.errors.exceptions import MLUserException

def test():
    result = None
    try:
        raise MLUserException({'message': 'Test error'})
    except Exception as e:
        result = 'caught'
    finally:
        pass
    return result

x = test()

# End of generated code