"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin

from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access, safe_method_call as _safe_method_call, get_safe_length

def append(arr, element):
    return (arr + [element])

def create_node(x, y, g, h, parent):
    return {'x': x, 'y': y, 'g': g, 'h': h, 'f': (g + h), 'parent': parent}

def manhattan_distance(x1, y1, x2, y2):
    dx = (x1 - x2)
    dy = (y1 - y2)
    if (dx < 0):
        dx = (-dx)
    if (dy < 0):
        dy = (-dy)
    return (dx + dy)

def euclidean_distance(x1, y1, x2, y2):
    dx = (x1 - x2)
    dy = (y1 - y2)
    return _safe_call(sqrt, ((dx * dx) + (dy * dy)))

def contains_position(list, x, y):
    i = 0
    while (i < _safe_call(builtin.len, list)):
        node = list[i]
        if (_safe_attr_access(node, 'x') == x):
            if (_safe_attr_access(node, 'y') == y):
                return True
        i = (i + 1)
    return False

def find_lowest_f(open_list):
    if (_safe_call(builtin.len, open_list) == 0):
        return None
    lowest_idx = 0
    lowest_f = _safe_attr_access(open_list[0], 'f')
    i = 1
    while (i < _safe_call(builtin.len, open_list)):
        if (_safe_attr_access(open_list[i], 'f') < lowest_f):
            lowest_f = _safe_attr_access(open_list[i], 'f')
            lowest_idx = i
        i = (i + 1)
    return lowest_idx

def remove_at(arr, idx):
    result = []
    i = 0
    while (i < _safe_call(builtin.len, arr)):
        if (i != idx):
            result = append(result, arr[i])
        i = (i + 1)
    return result

def get_neighbors(x, y, grid):
    neighbors = []
    directions = [{'dx': 0, 'dy': -1}, {'dx': 1, 'dy': 0}, {'dx': 0, 'dy': 1}, {'dx': -1, 'dy': 0}]
    height = _safe_call(builtin.len, grid)
    width = _safe_call(builtin.len, grid[0])
    i = 0
    while (i < _safe_call(builtin.len, directions)):
        dir = directions[i]
        new_x = (x + _safe_attr_access(dir, 'dx'))
        new_y = (y + _safe_attr_access(dir, 'dy'))
        if (new_x >= 0):
            if (new_x < width):
                if (new_y >= 0):
                    if (new_y < height):
                        if (grid[new_y][new_x] == 0):
                            neighbors = append(neighbors, {'x': new_x, 'y': new_y})
        i = (i + 1)
    return neighbors

def reconstruct_path(end_node):
    path = []
    current = end_node
    while (current != None):
        path = append(path, {'x': _safe_attr_access(current, 'x'), 'y': _safe_attr_access(current, 'y')})
        current = _safe_attr_access(current, 'parent')
    reversed = []
    i = (_safe_call(builtin.len, path) - 1)
    while (i >= 0):
        reversed = append(reversed, path[i])
        i = (i - 1)
    return reversed

def find_path(grid, start_x, start_y, end_x, end_y):
    open_list = []
    closed_list = []
    h = manhattan_distance(start_x, start_y, end_x, end_y)
    start_node = create_node(start_x, start_y, 0, h, None)
    open_list = append(open_list, start_node)
    while (_safe_call(builtin.len, open_list) > 0):
        current_idx = find_lowest_f(open_list)
        current = open_list[current_idx]
        if (_safe_attr_access(current, 'x') == end_x):
            if (_safe_attr_access(current, 'y') == end_y):
                return reconstruct_path(current)
        open_list = remove_at(open_list, current_idx)
        closed_list = append(closed_list, current)
        neighbors = get_neighbors(_safe_attr_access(current, 'x'), _safe_attr_access(current, 'y'), grid)
        i = 0
        while (i < _safe_call(builtin.len, neighbors)):
            neighbor = neighbors[i]
            nx = _safe_attr_access(neighbor, 'x')
            ny = _safe_attr_access(neighbor, 'y')
            if (contains_position(closed_list, nx, ny) == False):
                g = (_safe_attr_access(current, 'g') + 1)
                h = manhattan_distance(nx, ny, end_x, end_y)
                in_open = contains_position(open_list, nx, ny)
                if (in_open == False):
                    new_node = create_node(nx, ny, g, h, current)
                    open_list = append(open_list, new_node)
            i = (i + 1)
    return []

def path_length(path):
    return _safe_call(builtin.len, path)

def path_cost(path):
    if (_safe_call(builtin.len, path) <= 1):
        return 0
    return (_safe_call(builtin.len, path) - 1)

# End of generated code