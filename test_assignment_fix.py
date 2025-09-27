"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib.console_bridge import console
from mlpy.stdlib import getCurrentTime, processData

from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access, get_safe_length

obj = {'name': 'John', 'age': 30}

obj['name'] = 'Jane'

obj['age'] = 25

name = _safe_attr_access(obj, 'name')

_safe_attr_access(console, 'log')('Name:', name)

# End of generated code