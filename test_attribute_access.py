"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib.console_bridge import console
from mlpy.stdlib import getCurrentTime, processData

from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access, get_safe_length

text = 'Hello World'

upper_text = _safe_attr_access(text, 'upper')()

text_length = _safe_attr_access(text, 'length')

arr = [1, 2, 3]

arr_length = _safe_attr_access(arr, 'length')

_safe_attr_access(arr, 'append')(4)

obj = {'name': 'John', 'age': 30}

name = _safe_attr_access(obj, 'name')

_safe_attr_access(console, 'log')('Text:', text)

_safe_attr_access(console, 'log')('Upper:', upper_text)

_safe_attr_access(console, 'log')('Text length:', text_length)

_safe_attr_access(console, 'log')('Array:', arr)

_safe_attr_access(console, 'log')('Array length:', arr_length)

_safe_attr_access(console, 'log')('Name:', name)

# End of generated code