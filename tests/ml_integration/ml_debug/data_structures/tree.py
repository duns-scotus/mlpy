"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access, safe_method_call as _safe_method_call, get_safe_length

def create_node(value, left, right):
    node = {}
    node['value'] = value
    node['left'] = left
    node['right'] = right
    return node

def create_leaf(value):
    return create_node(value, {}, {})

def is_empty_node(node):
    return ((_safe_attr_access(node, 'value') == None) or (_safe_attr_access(node, 'value') == 0))

def tree_size(node):
    if is_empty_node(node):
        return 0
    left_size = tree_size(_safe_attr_access(node, 'left'))
    right_size = tree_size(_safe_attr_access(node, 'right'))
    return ((1 + left_size) + right_size)

def tree_height(node):
    if is_empty_node(node):
        return 0
    left_height = tree_height(_safe_attr_access(node, 'left'))
    right_height = tree_height(_safe_attr_access(node, 'right'))
    if (left_height > right_height):
        return (1 + left_height)
    else:
        return (1 + right_height)

def tree_sum(node):
    if is_empty_node(node):
        return 0
    left_sum = tree_sum(_safe_attr_access(node, 'left'))
    right_sum = tree_sum(_safe_attr_access(node, 'right'))
    return ((_safe_attr_access(node, 'value') + left_sum) + right_sum)

def tree_contains(node, target):
    if is_empty_node(node):
        return False
    if (_safe_attr_access(node, 'value') == target):
        return True
    found_left = tree_contains(_safe_attr_access(node, 'left'), target)
    if found_left:
        return True
    return tree_contains(_safe_attr_access(node, 'right'), target)

def tree_max(node):
    if is_empty_node(node):
        return 0
    max_val = _safe_attr_access(node, 'value')
    left_max = tree_max(_safe_attr_access(node, 'left'))
    if (left_max > max_val):
        max_val = left_max
    right_max = tree_max(_safe_attr_access(node, 'right'))
    if (right_max > max_val):
        max_val = right_max
    return max_val

# End of generated code