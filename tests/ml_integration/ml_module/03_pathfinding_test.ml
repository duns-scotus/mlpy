// Test: User Module Import - A* Pathfinding
// Tests importing and using the a_star.ml pathfinding module

import user_modules.a_star;

function test_manhattan_distance() {
    dist = user_modules.a_star.manhattan_distance(0, 0, 3, 4);

    print("Testing manhattan_distance:");
    print("  From (0,0) to (3,4): " + str(dist));

    if (dist == 7) {
        return true;
    }
    return false;
}

function test_simple_pathfinding() {
    // Create simple 5x5 grid (0 = walkable, 1 = wall)
    grid = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0]
    ];

    print("Testing simple pathfinding:");
    print("  Grid: 5x5 with some walls");
    print("  Start: (0, 0)");
    print("  Goal: (4, 4)");

    path = user_modules.a_star.find_path(grid, 0, 0, 4, 4);

    print("  Path length: " + str(len(path)));

    if (len(path) > 0) {
        // Check start
        if (path[0].x == 0) {
            if (path[0].y == 0) {
                // Check end
                last_idx = len(path) - 1;
                if (path[last_idx].x == 4) {
                    if (path[last_idx].y == 4) {
                        return true;
                    }
                }
            }
        }
    }
    return false;
}

function test_no_path() {
    // Create grid with no path
    grid = [
        [0, 0, 0],
        [1, 1, 1],
        [0, 0, 0]
    ];

    print("Testing no path scenario:");
    print("  Grid with wall blocking path");
    print("  Start: (0, 0)");
    print("  Goal: (2, 2)");

    path = user_modules.a_star.find_path(grid, 0, 0, 2, 2);

    print("  Path length: " + str(len(path)));

    if (len(path) == 0) {
        return true;
    }
    return false;
}

function test_path_cost() {
    // Create simple path
    grid = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ];

    print("Testing path cost calculation:");

    path = user_modules.a_star.find_path(grid, 0, 0, 2, 2);

    if (len(path) > 0) {
        cost = user_modules.a_star.path_cost(path);
        length = user_modules.a_star.path_length(path);

        print("  Path length: " + str(length));
        print("  Path cost: " + str(cost));

        if (cost == length - 1) {
            return true;
        }
    }
    return false;
}

function test_complex_maze() {
    // More complex maze
    grid = [
        [0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0]
    ];

    print("Testing complex maze:");
    print("  Grid: 7x5 with multiple walls");
    print("  Start: (0, 0)");
    print("  Goal: (6, 4)");

    path = user_modules.a_star.find_path(grid, 0, 0, 6, 4);

    print("  Path found: " + str(len(path) > 0));
    print("  Path length: " + str(len(path)));

    if (len(path) > 0) {
        // Verify start and end
        if (path[0].x == 0) {
            if (path[0].y == 0) {
                last_idx = len(path) - 1;
                if (path[last_idx].x == 6) {
                    if (path[last_idx].y == 4) {
                        return true;
                    }
                }
            }
        }
    }
    return false;
}

function main() {
    print("===== User Module Test: a_star.ml =====");
    print("");

    test1 = test_manhattan_distance();
    print("Test 1 (manhattan_distance): " + str(test1));
    print("");

    test2 = test_simple_pathfinding();
    print("Test 2 (simple_pathfinding): " + str(test2));
    print("");

    test3 = test_no_path();
    print("Test 3 (no_path): " + str(test3));
    print("");

    test4 = test_path_cost();
    print("Test 4 (path_cost): " + str(test4));
    print("");

    test5 = test_complex_maze();
    print("Test 5 (complex_maze): " + str(test5));
    print("");

    // Count passing tests
    passed = 0;
    if (test1) { passed = passed + 1; }
    if (test2) { passed = passed + 1; }
    if (test3) { passed = passed + 1; }
    if (test4) { passed = passed + 1; }
    if (test5) { passed = passed + 1; }

    print("===== Summary =====");
    print("Tests passed: " + str(passed) + "/5");

    if (passed == 5) {
        print("All tests PASSED!");
        return 0;
    } else {
        print("Some tests FAILED!");
        return 1;
    }
}

main();
