"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access, safe_method_call as _safe_method_call, get_safe_length

def get_length(arr):
    len = 0
    try:
        i = 0
        while True:
            temp = arr[i]
            i = (i + 1)
            len = (len + 1)
    except Exception as e:
        pass
    finally:
        pass
    return len

def append(arr, item):
    return (arr + [item])

def array_contains(arr, item):
    len = get_length(arr)
    i = 0
    while (i < len):
        if (arr[i] == item):
            return True
        i = (i + 1)
    return False

def array_shift(arr):
    len = get_length(arr)
    if (len == 0):
        return arr
    new_arr = []
    i = 1
    while (i < len):
        new_arr = (new_arr + [arr[i]])
        i = (i + 1)
    return new_arr

def find_min_f_score_node(open_set, f_score):
    len = get_length(open_set)
    if (len == 0):
        return None
    min_node = open_set[0]
    min_score = dict_get(f_score, node_to_key(min_node), 999999)
    i = 1
    while (i < len):
        node = open_set[i]
        score = dict_get(f_score, node_to_key(node), 999999)
        if (score < min_score):
            min_score = score
            min_node = node
        i = (i + 1)
    return min_node

def array_remove(arr, element):
    len = get_length(arr)
    new_arr = []
    i = 0
    while (i < len):
        if (arr[i] != element):
            new_arr = (new_arr + [arr[i]])
        i = (i + 1)
    return new_arr

def node_to_key(node):
    return (str((str((str('') + str(_safe_attr_access(node, 'x')))) + str(','))) + str(_safe_attr_access(node, 'y')))

def dict_get(dict, key, default_val):
    try:
        val = dict[key]
        if (val == None):
            return default_val
        return val
    except Exception as e:
        return default_val
    finally:
        pass

def heuristic(node, goal):
    dx = (_safe_attr_access(node, 'x') - _safe_attr_access(goal, 'x'))
    dy = (_safe_attr_access(node, 'y') - _safe_attr_access(goal, 'y'))
    if (dx < 0):
        dx = (0 - dx)
    if (dy < 0):
        dy = (0 - dy)
    return (dx + dy)

def reconstruct_path(came_from, current):
    path = []
    path = append(path, current)
    prev = dict_get(came_from, node_to_key(current), None)
    while (prev != None):
        current = prev
        path = append(path, current)
        prev = dict_get(came_from, node_to_key(current), None)
    return path

def get_neighbors(node, grid_width, grid_height):
    neighbors = []
    if (_safe_attr_access(node, 'y') > 0):
        up = {'x': _safe_attr_access(node, 'x'), 'y': (_safe_attr_access(node, 'y') - 1)}
        neighbors = append(neighbors, up)
    if (_safe_attr_access(node, 'y') < (grid_height - 1)):
        down = {'x': _safe_attr_access(node, 'x'), 'y': (_safe_attr_access(node, 'y') + 1)}
        neighbors = append(neighbors, down)
    if (_safe_attr_access(node, 'x') > 0):
        left = {'x': (_safe_attr_access(node, 'x') - 1), 'y': _safe_attr_access(node, 'y')}
        neighbors = append(neighbors, left)
    if (_safe_attr_access(node, 'x') < (grid_width - 1)):
        right = {'x': (_safe_attr_access(node, 'x') + 1), 'y': _safe_attr_access(node, 'y')}
        neighbors = append(neighbors, right)
    return neighbors

def nodes_equal(a, b):
    return ((_safe_attr_access(a, 'x') == _safe_attr_access(b, 'x')) and (_safe_attr_access(a, 'y') == _safe_attr_access(b, 'y')))

def astar(start, goal, grid_width, grid_height):
    open_set = []
    open_set = append(open_set, start)
    came_from = {}
    g_score = {}
    g_score[node_to_key(start)] = 0
    f_score = {}
    f_score[node_to_key(start)] = heuristic(start, goal)
    closed_set = []
    iterations = 0
    max_iterations = 1000
    while ((get_length(open_set) > 0) and (iterations < max_iterations)):
        iterations = (iterations + 1)
        current = find_min_f_score_node(open_set, f_score)
        if nodes_equal(current, goal):
            return {'success': True, 'path': reconstruct_path(came_from, current), 'iterations': iterations}
        open_set = array_remove(open_set, current)
        closed_set = append(closed_set, current)
        neighbors = get_neighbors(current, grid_width, grid_height)
        neighbor_len = get_length(neighbors)
        i = 0
        while (i < neighbor_len):
            neighbor = neighbors[i]
            in_closed = False
            j = 0
            closed_len = get_length(closed_set)
            while (j < closed_len):
                if nodes_equal(neighbor, closed_set[j]):
                    in_closed = True
                j = (j + 1)
            if in_closed:
                i = (i + 1)
            else:
                current_key = node_to_key(current)
                current_g = dict_get(g_score, current_key, 0)
                tentative_g_score = (current_g + 1)
                neighbor_key = node_to_key(neighbor)
                neighbor_g_score = dict_get(g_score, neighbor_key, 999999)
                if (tentative_g_score < neighbor_g_score):
                    came_from[node_to_key(neighbor)] = current
                    g_score[node_to_key(neighbor)] = tentative_g_score
                    f_score[node_to_key(neighbor)] = (tentative_g_score + heuristic(neighbor, goal))
                    in_open = False
                    k = 0
                    open_len = get_length(open_set)
                    while (k < open_len):
                        if nodes_equal(neighbor, open_set[k]):
                            in_open = True
                        k = (k + 1)
                    if (not in_open):
                        open_set = append(open_set, neighbor)
                i = (i + 1)
    return {'success': False, 'path': [], 'iterations': iterations}

def main():
    results = {}
    start1 = {'x': 0, 'y': 0}
    goal1 = {'x': 3, 'y': 3}
    results['test1'] = astar(start1, goal1, 5, 5)
    start2 = {'x': 0, 'y': 0}
    goal2 = {'x': 7, 'y': 7}
    results['test2'] = astar(start2, goal2, 10, 10)
    start3 = {'x': 2, 'y': 2}
    goal3 = {'x': 2, 'y': 2}
    results['test3'] = astar(start3, goal3, 5, 5)
    start4 = {'x': 0, 'y': 4}
    goal4 = {'x': 9, 'y': 0}
    results['test4'] = astar(start4, goal4, 10, 5)
    return results

test_results = main()

# End of generated code