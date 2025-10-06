// a_star.ml - A* Pathfinding Algorithm
// Efficient pathfinding algorithm for grid-based maps

// Helper: Append element to array (returns concatenated array)
function append(arr, element) {
    return arr + [element];
}

// Node structure for A* algorithm
function create_node(x, y, g, h, parent) {
    return {
        "x": x,
        "y": y,
        "g": g,
        "h": h,
        "f": g + h,
        "parent": parent
    };
}

// Calculate Manhattan distance heuristic
function manhattan_distance(x1, y1, x2, y2) {
    dx = x1 - x2;
    dy = y1 - y2;
    if (dx < 0) {
        dx = -dx;
    }
    if (dy < 0) {
        dy = -dy;
    }
    return dx + dy;
}

// Calculate Euclidean distance heuristic
function euclidean_distance(x1, y1, x2, y2) {
    dx = x1 - x2;
    dy = y1 - y2;
    return sqrt(dx * dx + dy * dy);
}

// Check if position is in list
function contains_position(list, x, y) {
    i = 0;
    while (i < len(list)) {
        node = list[i];
        if (node.x == x) {
            if (node.y == y) {
                return true;
            }
        }
        i = i + 1;
    }
    return false;
}

// Find node with lowest f score
function find_lowest_f(open_list) {
    if (len(open_list) == 0) {
        return null;
    }

    lowest_idx = 0;
    lowest_f = open_list[0].f;

    i = 1;
    while (i < len(open_list)) {
        if (open_list[i].f < lowest_f) {
            lowest_f = open_list[i].f;
            lowest_idx = i;
        }
        i = i + 1;
    }

    return lowest_idx;
}

// Remove element from array by index
function remove_at(arr, idx) {
    result = [];
    i = 0;
    while (i < len(arr)) {
        if (i != idx) {
            result = append(result, arr[i]);
        }
        i = i + 1;
    }
    return result;
}

// Get valid neighbors (4-directional movement)
function get_neighbors(x, y, grid) {
    neighbors = [];
    directions = [
        {"dx": 0, "dy": -1},
        {"dx": 1, "dy": 0},
        {"dx": 0, "dy": 1},
        {"dx": -1, "dy": 0}
    ];

    height = len(grid);
    width = len(grid[0]);

    i = 0;
    while (i < len(directions)) {
        dir = directions[i];
        new_x = x + dir.dx;
        new_y = y + dir.dy;

        // Check bounds
        if (new_x >= 0) {
            if (new_x < width) {
                if (new_y >= 0) {
                    if (new_y < height) {
                        // Check if walkable (0 = walkable, 1 = wall)
                        if (grid[new_y][new_x] == 0) {
                            neighbors = append(neighbors, {"x": new_x, "y": new_y});
                        }
                    }
                }
            }
        }

        i = i + 1;
    }

    return neighbors;
}

// Reconstruct path from end to start
function reconstruct_path(end_node) {
    path = [];
    current = end_node;

    while (current != null) {
        path = append(path, {"x": current.x, "y": current.y});
        current = current.parent;
    }

    // Reverse path to get start -> end
    reversed = [];
    i = len(path) - 1;
    while (i >= 0) {
        reversed = append(reversed, path[i]);
        i = i - 1;
    }

    return reversed;
}

// A* pathfinding algorithm
function find_path(grid, start_x, start_y, end_x, end_y) {
    // Initialize open and closed lists
    open_list = [];
    closed_list = [];

    // Create start node
    h = manhattan_distance(start_x, start_y, end_x, end_y);
    start_node = create_node(start_x, start_y, 0, h, null);
    open_list = append(open_list, start_node);

    // Main loop
    while (len(open_list) > 0) {
        // Get node with lowest f score
        current_idx = find_lowest_f(open_list);
        current = open_list[current_idx];

        // Check if reached goal
        if (current.x == end_x) {
            if (current.y == end_y) {
                return reconstruct_path(current);
            }
        }

        // Move current from open to closed
        open_list = remove_at(open_list, current_idx);
        closed_list = append(closed_list, current);

        // Check neighbors
        neighbors = get_neighbors(current.x, current.y, grid);
        i = 0;
        while (i < len(neighbors)) {
            neighbor = neighbors[i];
            nx = neighbor.x;
            ny = neighbor.y;

            // Skip if in closed list
            if (contains_position(closed_list, nx, ny) == false) {
                // Calculate costs
                g = current.g + 1;
                h = manhattan_distance(nx, ny, end_x, end_y);

                // Check if in open list
                in_open = contains_position(open_list, nx, ny);

                if (in_open == false) {
                    // Add to open list
                    new_node = create_node(nx, ny, g, h, current);
                    open_list = append(open_list, new_node);
                }
            }

            i = i + 1;
        }
    }

    // No path found
    return [];
}

// Calculate path length
function path_length(path) {
    return len(path);
}

// Get path cost (same as length for uniform cost)
function path_cost(path) {
    if (len(path) <= 1) {
        return 0;
    }
    return len(path) - 1;
}
