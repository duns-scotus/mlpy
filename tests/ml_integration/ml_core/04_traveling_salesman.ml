// Test core language: Traveling Salesman Problem (TSP)
// Features tested: recursion, permutations, arrays, nested loops, optimization
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
    len = get_length(arr);
    new_arr = [];
    i = 0;
    while (i < len) {
        new_arr[i] = arr[i];
        i = i + 1;
    }
    new_arr[len] = item;
    return new_arr;
}

// Helper: copy array
function copy_array(arr) {
    len = get_length(arr);
    new_arr = [];
    i = 0;
    while (i < len) {
        new_arr[i] = arr[i];
        i = i + 1;
    }
    return new_arr;
}

// Helper: calculate Euclidean distance
function distance(city1, city2) {
    dx = city1.x - city2.x;
    dy = city1.y - city2.y;
    // Return squared distance to avoid sqrt
    return dx * dx + dy * dy;
}

// Helper: calculate total tour distance
function tour_distance(cities, tour) {
    total = 0;
    tour_len = get_length(tour);
    i = 0;
    while (i < tour_len - 1) {
        city1 = cities[tour[i]];
        city2 = cities[tour[i + 1]];
        total = total + distance(city1, city2);
        i = i + 1;
    }
    // Add distance from last city back to first
    city1 = cities[tour[tour_len - 1]];
    city2 = cities[tour[0]];
    total = total + distance(city1, city2);
    return total;
}

// Helper: swap elements in array
function swap(arr, i, j) {
    temp = arr[i];
    arr[i] = arr[j];
    arr[j] = temp;
    return arr;
}

// Generate permutations recursively
function generate_permutations_helper(arr, start, result) {
    len = get_length(arr);

    if (start == len - 1) {
        result = append(result, copy_array(arr));
        return result;
    }

    i = start;
    while (i < len) {
        arr = swap(arr, start, i);
        result = generate_permutations_helper(arr, start + 1, result);
        arr = swap(arr, start, i);  // Backtrack
        i = i + 1;
    }

    return result;
}

// Generate all permutations
function generate_permutations(arr) {
    result = [];
    return generate_permutations_helper(copy_array(arr), 0, result);
}

// Brute force TSP - try all permutations
function tsp_brute_force(cities) {
    num_cities = get_length(cities);

    // Create initial tour [0, 1, 2, ...]
    initial_tour = [];
    i = 0;
    while (i < num_cities) {
        initial_tour = append(initial_tour, i);
        i = i + 1;
    }

    // Generate all permutations
    all_tours = generate_permutations(initial_tour);
    num_tours = get_length(all_tours);

    // Find best tour
    best_tour = all_tours[0];
    best_distance = tour_distance(cities, best_tour);

    i = 1;
    while (i < num_tours) {
        tour = all_tours[i];
        dist = tour_distance(cities, tour);
        if (dist < best_distance) {
            best_distance = dist;
            best_tour = tour;
        }
        i = i + 1;
    }

    return {
        tour: best_tour,
        distance: best_distance,
        tours_checked: num_tours
    };
}

// Nearest neighbor heuristic
function tsp_nearest_neighbor(cities) {
    num_cities = get_length(cities);

    if (num_cities == 0) {
        return {tour: [], distance: 0};
    }

    visited = [];
    i = 0;
    while (i < num_cities) {
        visited = append(visited, false);
        i = i + 1;
    }

    tour = [];
    current = 0;
    tour = append(tour, current);
    visited[current] = true;
    total_distance = 0;

    steps = 1;
    while (steps < num_cities) {
        nearest = -1;
        nearest_dist = 999999999;

        i = 0;
        while (i < num_cities) {
            if (!visited[i]) {
                dist = distance(cities[current], cities[i]);
                if (dist < nearest_dist) {
                    nearest_dist = dist;
                    nearest = i;
                }
            }
            i = i + 1;
        }

        if (nearest != -1) {
            tour = append(tour, nearest);
            visited[nearest] = true;
            total_distance = total_distance + nearest_dist;
            current = nearest;
        }

        steps = steps + 1;
    }

    // Add distance back to start
    total_distance = total_distance + distance(cities[current], cities[0]);

    return {
        tour: tour,
        distance: total_distance,
        heuristic: "nearest_neighbor"
    };
}

// 2-opt improvement heuristic
function tsp_2opt(cities, initial_tour) {
    tour = copy_array(initial_tour);
    tour_len = get_length(tour);
    improved = true;

    iterations = 0;
    max_iterations = 100;

    while (improved && iterations < max_iterations) {
        improved = false;
        iterations = iterations + 1;

        i = 1;
        while (i < tour_len - 1) {
            j = i + 1;
            while (j < tour_len) {
                // Calculate current distance
                city_i_minus_1 = cities[tour[i - 1]];
                city_i = cities[tour[i]];
                city_j = cities[tour[j]];
                city_j_next = cities[tour[(j + 1) - ((j + 1) / tour_len) * tour_len]];

                current_dist = distance(city_i_minus_1, city_i) + distance(city_j, city_j_next);

                // Calculate new distance after 2-opt swap
                new_dist = distance(city_i_minus_1, city_j) + distance(city_i, city_j_next);

                if (new_dist < current_dist) {
                    // Reverse tour[i:j]
                    left = i;
                    right = j;
                    while (left < right) {
                        tour = swap(tour, left, right);
                        left = left + 1;
                        right = right - 1;
                    }
                    improved = true;
                }

                j = j + 1;
            }
            i = i + 1;
        }
    }

    return {
        tour: tour,
        distance: tour_distance(cities, tour),
        iterations: iterations
    };
}

// Main test function
function main() {
    results = {};

    // Test 1: Small TSP instance (4 cities) - can use brute force
    cities_small = [];
    cities_small = append(cities_small, {x: 0, y: 0});
    cities_small = append(cities_small, {x: 1, y: 3});
    cities_small = append(cities_small, {x: 4, y: 2});
    cities_small = append(cities_small, {x: 3, y: 0});

    results.small_brute_force = tsp_brute_force(cities_small);
    results.small_nn = tsp_nearest_neighbor(cities_small);

    // Test 2: Medium TSP (6 cities) - use heuristics
    cities_medium = [];
    cities_medium = append(cities_medium, {x: 0, y: 0});
    cities_medium = append(cities_medium, {x: 2, y: 5});
    cities_medium = append(cities_medium, {x: 5, y: 4});
    cities_medium = append(cities_medium, {x: 7, y: 2});
    cities_medium = append(cities_medium, {x: 6, y: 0});
    cities_medium = append(cities_medium, {x: 3, y: 1});

    nn_result = tsp_nearest_neighbor(cities_medium);
    results.medium_nn = nn_result;
    results.medium_2opt = tsp_2opt(cities_medium, nn_result.tour);

    // Test 3: Compare nearest neighbor with 2-opt improvement
    cities_test = [];
    cities_test = append(cities_test, {x: 0, y: 0});
    cities_test = append(cities_test, {x: 1, y: 4});
    cities_test = append(cities_test, {x: 3, y: 5});
    cities_test = append(cities_test, {x: 5, y: 3});
    cities_test = append(cities_test, {x: 4, y: 1});

    nn_test = tsp_nearest_neighbor(cities_test);
    improved_test = tsp_2opt(cities_test, nn_test.tour);

    results.comparison = {
        nn_distance: nn_test.distance,
        improved_distance: improved_test.distance,
        improvement_iterations: improved_test.iterations
    };

    return results;
}

// Run tests
test_results = main();
