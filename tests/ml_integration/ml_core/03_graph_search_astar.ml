// Test core language: A* pathfinding algorithm
// Features tested: dictionaries, arrays, while loops, function variables, complex logic
// NO external function calls - pure language features only

// Helper: get array length using try/except
function get_length(arr) {
    len = 0;
    try {
        i = 0;
        while (true) {
            temp = arr[i];
            i = i + 1;
            len = len + 1;
        }
    } except (e) {
        // Out of bounds
    }
    return len;
}

// Helper: append to array
function append(arr, item) {
    return arr + [item];
}

// Helper: check if array contains item
function array_contains(arr, item) {
    len = get_length(arr);
    i = 0;
    while (i < len) {
        if (arr[i] == item) {
            return true;
        }
        i = i + 1;
    }
    return false;
}

// Helper: remove first element from array
function array_shift(arr) {
    len = get_length(arr);
    if (len == 0) {
        return arr;
    }
    new_arr = [];
    i = 1;
    while (i < len) {
        new_arr = new_arr + [arr[i]];
        i = i + 1;
    }
    return new_arr;
}

// Helper: find minimum in array of nodes by f_score
function find_min_f_score_node(open_set, f_score) {
    len = get_length(open_set);
    if (len == 0) {
        return null;
    }

    min_node = open_set[0];
    min_score = f_score[min_node];

    i = 1;
    while (i < len) {
        node = open_set[i];
        score = f_score[node];
        if (score < min_score) {
            min_score = score;
            min_node = node;
        }
        i = i + 1;
    }

    return min_node;
}

// Helper: remove specific element from array
function array_remove(arr, element) {
    len = get_length(arr);
    new_arr = [];
    i = 0;
    while (i < len) {
        if (arr[i] != element) {
            new_arr = new_arr + [arr[i]];
        }
        i = i + 1;
    }
    return new_arr;
}

// Helper: Manhattan distance heuristic
function heuristic(node, goal) {
    dx = node.x - goal.x;
    dy = node.y - goal.y;
    if (dx < 0) {
        dx = 0 - dx;
    }
    if (dy < 0) {
        dy = 0 - dy;
    }
    return dx + dy;
}

// Helper: reconstruct path
function reconstruct_path(came_from, current) {
    path = [];
    path = append(path, current);

    while (came_from[current] != null) {
        current = came_from[current];
        path = append(path, current);
    }

    return path;
}

// Helper: get neighbors of a node in grid
function get_neighbors(node, grid_width, grid_height) {
    neighbors = [];

    // Up
    if (node.y > 0) {
        up = {x: node.x, y: node.y - 1};
        neighbors = append(neighbors, up);
    }

    // Down
    if (node.y < grid_height - 1) {
        down = {x: node.x, y: node.y + 1};
        neighbors = append(neighbors, down);
    }

    // Left
    if (node.x > 0) {
        left = {x: node.x - 1, y: node.y};
        neighbors = append(neighbors, left);
    }

    // Right
    if (node.x < grid_width - 1) {
        right = {x: node.x + 1, y: node.y};
        neighbors = append(neighbors, right);
    }

    return neighbors;
}

// Helper: nodes are equal
function nodes_equal(a, b) {
    return a.x == b.x && a.y == b.y;
}

// A* pathfinding algorithm
function astar(start, goal, grid_width, grid_height) {
    open_set = [];
    open_set = append(open_set, start);

    came_from = {};

    g_score = {};
    g_score[start] = 0;

    f_score = {};
    f_score[start] = heuristic(start, goal);

    closed_set = [];

    iterations = 0;
    max_iterations = 1000;

    while (get_length(open_set) > 0 && iterations < max_iterations) {
        iterations = iterations + 1;

        current = find_min_f_score_node(open_set, f_score);

        if (nodes_equal(current, goal)) {
            return {
                success: true,
                path: reconstruct_path(came_from, current),
                iterations: iterations
            };
        }

        open_set = array_remove(open_set, current);
        closed_set = append(closed_set, current);

        neighbors = get_neighbors(current, grid_width, grid_height);
        neighbor_len = get_length(neighbors);

        i = 0;
        while (i < neighbor_len) {
            neighbor = neighbors[i];

            // Check if in closed set
            in_closed = false;
            j = 0;
            closed_len = get_length(closed_set);
            while (j < closed_len) {
                if (nodes_equal(neighbor, closed_set[j])) {
                    in_closed = true;
                }
                j = j + 1;
            }

            if (in_closed) {
                i = i + 1;
            } else {
                tentative_g_score = g_score[current] + 1;

                neighbor_g_score = g_score[neighbor];
                if (neighbor_g_score == null) {
                    neighbor_g_score = 999999;
                }

                if (tentative_g_score < neighbor_g_score) {
                    came_from[neighbor] = current;
                    g_score[neighbor] = tentative_g_score;
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal);

                    // Check if neighbor in open_set
                    in_open = false;
                    k = 0;
                    open_len = get_length(open_set);
                    while (k < open_len) {
                        if (nodes_equal(neighbor, open_set[k])) {
                            in_open = true;
                        }
                        k = k + 1;
                    }

                    if (!in_open) {
                        open_set = append(open_set, neighbor);
                    }
                }

                i = i + 1;
            }
        }
    }

    return {
        success: false,
        path: [],
        iterations: iterations
    };
}

// Main test function
function main() {
    results = {};

    // Test 1: Simple path from (0,0) to (3,3)
    start1 = {x: 0, y: 0};
    goal1 = {x: 3, y: 3};
    results.test1 = astar(start1, goal1, 5, 5);

    // Test 2: Longer path
    start2 = {x: 0, y: 0};
    goal2 = {x: 7, y: 7};
    results.test2 = astar(start2, goal2, 10, 10);

    // Test 3: Start equals goal
    start3 = {x: 2, y: 2};
    goal3 = {x: 2, y: 2};
    results.test3 = astar(start3, goal3, 5, 5);

    // Test 4: Path across grid
    start4 = {x: 0, y: 4};
    goal4 = {x: 9, y: 0};
    results.test4 = astar(start4, goal4, 10, 5);

    return results;
}

// Run tests
test_results = main();
