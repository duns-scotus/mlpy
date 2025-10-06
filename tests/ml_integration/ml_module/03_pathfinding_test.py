"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin

from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access, safe_method_call as _safe_method_call, get_safe_length

# ============================================================================
# User Module Definitions (Inline)
# ============================================================================

# Module: user_modules.a_star
class user_modules:
    _ml_user_module = True
    a_star = None
# --- Begin User Module: user_modules.a_star ---
def _umod_user_modules_a_star_append(arr, element):
    return (arr + [element])
def _umod_user_modules_a_star_create_node(x, y, g, h, parent):
    return {'x': x, 'y': y, 'g': g, 'h': h, 'f': (g + h), 'parent': parent}
def _umod_user_modules_a_star_manhattan_distance(x1, y1, x2, y2):
    dx = (x1 - x2)
    dy = (y1 - y2)
    if (dx < 0):
        dx = (-dx)
    if (dy < 0):
        dy = (-dy)
    return (dx + dy)
def _umod_user_modules_a_star_euclidean_distance(x1, y1, x2, y2):
    dx = (x1 - x2)
    dy = (y1 - y2)
    return _safe_call(sqrt, ((dx * dx) + (dy * dy)))
def _umod_user_modules_a_star_contains_position(list, x, y):
    i = 0
    while (i < _safe_call(builtin.len, list)):
        node = list[i]
        if (_safe_attr_access(node, 'x') == x):
            if (_safe_attr_access(node, 'y') == y):
                return True
        i = (i + 1)
    return False
def _umod_user_modules_a_star_find_lowest_f(open_list):
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
def _umod_user_modules_a_star_remove_at(arr, idx):
    result = []
    i = 0
    while (i < _safe_call(builtin.len, arr)):
        if (i != idx):
            result = _umod_user_modules_a_star_append(result, arr[i])
        i = (i + 1)
    return result
def _umod_user_modules_a_star_get_neighbors(x, y, grid):
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
                            neighbors = _umod_user_modules_a_star_append(neighbors, {'x': new_x, 'y': new_y})
        i = (i + 1)
    return neighbors
def _umod_user_modules_a_star_reconstruct_path(end_node):
    path = []
    current = end_node
    while (current != None):
        path = _umod_user_modules_a_star_append(path, {'x': _safe_attr_access(current, 'x'), 'y': _safe_attr_access(current, 'y')})
        current = _safe_attr_access(current, 'parent')
    reversed = []
    i = (_safe_call(builtin.len, path) - 1)
    while (i >= 0):
        reversed = _umod_user_modules_a_star_append(reversed, path[i])
        i = (i - 1)
    return reversed
def _umod_user_modules_a_star_find_path(grid, start_x, start_y, end_x, end_y):
    open_list = []
    closed_list = []
    h = _umod_user_modules_a_star_manhattan_distance(start_x, start_y, end_x, end_y)
    start_node = _umod_user_modules_a_star_create_node(start_x, start_y, 0, h, None)
    open_list = _umod_user_modules_a_star_append(open_list, start_node)
    while (_safe_call(builtin.len, open_list) > 0):
        current_idx = _umod_user_modules_a_star_find_lowest_f(open_list)
        current = open_list[current_idx]
        if (_safe_attr_access(current, 'x') == end_x):
            if (_safe_attr_access(current, 'y') == end_y):
                return _umod_user_modules_a_star_reconstruct_path(current)
        open_list = _umod_user_modules_a_star_remove_at(open_list, current_idx)
        closed_list = _umod_user_modules_a_star_append(closed_list, current)
        neighbors = _umod_user_modules_a_star_get_neighbors(_safe_attr_access(current, 'x'), _safe_attr_access(current, 'y'), grid)
        i = 0
        while (i < _safe_call(builtin.len, neighbors)):
            neighbor = neighbors[i]
            nx = _safe_attr_access(neighbor, 'x')
            ny = _safe_attr_access(neighbor, 'y')
            if (_umod_user_modules_a_star_contains_position(closed_list, nx, ny) == False):
                g = (_safe_attr_access(current, 'g') + 1)
                h = _umod_user_modules_a_star_manhattan_distance(nx, ny, end_x, end_y)
                in_open = _umod_user_modules_a_star_contains_position(open_list, nx, ny)
                if (in_open == False):
                    new_node = _umod_user_modules_a_star_create_node(nx, ny, g, h, current)
                    open_list = _umod_user_modules_a_star_append(open_list, new_node)
            i = (i + 1)
    return []
def _umod_user_modules_a_star_path_length(path):
    return _safe_call(builtin.len, path)
def _umod_user_modules_a_star_path_cost(path):
    if (_safe_call(builtin.len, path) <= 1):
        return 0
    return (_safe_call(builtin.len, path) - 1)

class _ModuleNamespace:
    _ml_user_module = True
    pass

user_modules_a_star = _ModuleNamespace()
user_modules_a_star.append = _umod_user_modules_a_star_append
user_modules_a_star.create_node = _umod_user_modules_a_star_create_node
user_modules_a_star.manhattan_distance = _umod_user_modules_a_star_manhattan_distance
user_modules_a_star.euclidean_distance = _umod_user_modules_a_star_euclidean_distance
user_modules_a_star.contains_position = _umod_user_modules_a_star_contains_position
user_modules_a_star.find_lowest_f = _umod_user_modules_a_star_find_lowest_f
user_modules_a_star.remove_at = _umod_user_modules_a_star_remove_at
user_modules_a_star.get_neighbors = _umod_user_modules_a_star_get_neighbors
user_modules_a_star.reconstruct_path = _umod_user_modules_a_star_reconstruct_path
user_modules_a_star.find_path = _umod_user_modules_a_star_find_path
user_modules_a_star.path_length = _umod_user_modules_a_star_path_length
user_modules_a_star.path_cost = _umod_user_modules_a_star_path_cost
# --- End User Module: user_modules.a_star ---

user_modules = user_modules()
user_modules.a_star = user_modules_a_star

# ============================================================================
# Main Program Code
# ============================================================================


def test_manhattan_distance():
    dist = _safe_method_call(_safe_attr_access(user_modules, 'a_star'), 'manhattan_distance', 0, 0, 3, 4)
    _safe_call(builtin.print, 'Testing manhattan_distance:')
    _safe_call(builtin.print, (str('  From (0,0) to (3,4): ') + str(_safe_call(builtin.str, dist))))
    if (dist == 7):
        return True
    return False

def test_simple_pathfinding():
    grid = [[0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 0, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 0, 0, 0]]
    _safe_call(builtin.print, 'Testing simple pathfinding:')
    _safe_call(builtin.print, '  Grid: 5x5 with some walls')
    _safe_call(builtin.print, '  Start: (0, 0)')
    _safe_call(builtin.print, '  Goal: (4, 4)')
    path = _safe_method_call(_safe_attr_access(user_modules, 'a_star'), 'find_path', grid, 0, 0, 4, 4)
    _safe_call(builtin.print, (str('  Path length: ') + str(_safe_call(builtin.str, _safe_call(builtin.len, path)))))
    if (_safe_call(builtin.len, path) > 0):
        if (_safe_attr_access(path[0], 'x') == 0):
            if (_safe_attr_access(path[0], 'y') == 0):
                last_idx = (_safe_call(builtin.len, path) - 1)
                if (_safe_attr_access(path[last_idx], 'x') == 4):
                    if (_safe_attr_access(path[last_idx], 'y') == 4):
                        return True
    return False

def test_no_path():
    grid = [[0, 0, 0], [1, 1, 1], [0, 0, 0]]
    _safe_call(builtin.print, 'Testing no path scenario:')
    _safe_call(builtin.print, '  Grid with wall blocking path')
    _safe_call(builtin.print, '  Start: (0, 0)')
    _safe_call(builtin.print, '  Goal: (2, 2)')
    path = _safe_method_call(_safe_attr_access(user_modules, 'a_star'), 'find_path', grid, 0, 0, 2, 2)
    _safe_call(builtin.print, (str('  Path length: ') + str(_safe_call(builtin.str, _safe_call(builtin.len, path)))))
    if (_safe_call(builtin.len, path) == 0):
        return True
    return False

def test_path_cost():
    grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    _safe_call(builtin.print, 'Testing path cost calculation:')
    path = _safe_method_call(_safe_attr_access(user_modules, 'a_star'), 'find_path', grid, 0, 0, 2, 2)
    if (_safe_call(builtin.len, path) > 0):
        cost = _safe_method_call(_safe_attr_access(user_modules, 'a_star'), 'path_cost', path)
        length = _safe_method_call(_safe_attr_access(user_modules, 'a_star'), 'path_length', path)
        _safe_call(builtin.print, (str('  Path length: ') + str(_safe_call(builtin.str, length))))
        _safe_call(builtin.print, (str('  Path cost: ') + str(_safe_call(builtin.str, cost))))
        if (cost == (length - 1)):
            return True
    return False

def test_complex_maze():
    grid = [[0, 0, 0, 1, 0, 0, 0], [0, 1, 0, 1, 0, 1, 0], [0, 1, 0, 0, 0, 1, 0], [0, 1, 1, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0]]
    _safe_call(builtin.print, 'Testing complex maze:')
    _safe_call(builtin.print, '  Grid: 7x5 with multiple walls')
    _safe_call(builtin.print, '  Start: (0, 0)')
    _safe_call(builtin.print, '  Goal: (6, 4)')
    path = _safe_method_call(_safe_attr_access(user_modules, 'a_star'), 'find_path', grid, 0, 0, 6, 4)
    _safe_call(builtin.print, (str('  Path found: ') + str(_safe_call(builtin.str, (_safe_call(builtin.len, path) > 0)))))
    _safe_call(builtin.print, (str('  Path length: ') + str(_safe_call(builtin.str, _safe_call(builtin.len, path)))))
    if (_safe_call(builtin.len, path) > 0):
        if (_safe_attr_access(path[0], 'x') == 0):
            if (_safe_attr_access(path[0], 'y') == 0):
                last_idx = (_safe_call(builtin.len, path) - 1)
                if (_safe_attr_access(path[last_idx], 'x') == 6):
                    if (_safe_attr_access(path[last_idx], 'y') == 4):
                        return True
    return False

def main():
    _safe_call(builtin.print, '===== User Module Test: a_star.ml =====')
    _safe_call(builtin.print, '')
    test1 = test_manhattan_distance()
    _safe_call(builtin.print, (str('Test 1 (manhattan_distance): ') + str(_safe_call(builtin.str, test1))))
    _safe_call(builtin.print, '')
    test2 = test_simple_pathfinding()
    _safe_call(builtin.print, (str('Test 2 (simple_pathfinding): ') + str(_safe_call(builtin.str, test2))))
    _safe_call(builtin.print, '')
    test3 = test_no_path()
    _safe_call(builtin.print, (str('Test 3 (no_path): ') + str(_safe_call(builtin.str, test3))))
    _safe_call(builtin.print, '')
    test4 = test_path_cost()
    _safe_call(builtin.print, (str('Test 4 (path_cost): ') + str(_safe_call(builtin.str, test4))))
    _safe_call(builtin.print, '')
    test5 = test_complex_maze()
    _safe_call(builtin.print, (str('Test 5 (complex_maze): ') + str(_safe_call(builtin.str, test5))))
    _safe_call(builtin.print, '')
    passed = 0
    if test1:
        passed = (passed + 1)
    if test2:
        passed = (passed + 1)
    if test3:
        passed = (passed + 1)
    if test4:
        passed = (passed + 1)
    if test5:
        passed = (passed + 1)
    _safe_call(builtin.print, '===== Summary =====')
    _safe_call(builtin.print, (str((str('Tests passed: ') + str(_safe_call(builtin.str, passed)))) + str('/5')))
    if (passed == 5):
        _safe_call(builtin.print, 'All tests PASSED!')
        return 0
    else:
        _safe_call(builtin.print, 'Some tests FAILED!')
        return 1

main()

# End of generated code