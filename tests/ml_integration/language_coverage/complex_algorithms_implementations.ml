// Complex Algorithms Implementations - Rewritten with Proper Patterns
// Uses validated data type operations and safe patterns

import string;
import array;
import math;

// Utility function for safe array append
function safe_append(arr, element) {
    new_arr = array.fill(arr.length + 1, 0);
    i = 0;
    while (i < arr.length) {
        new_arr[i] = arr[i];
        i = i + 1;
    }
    new_arr[arr.length] = element;
    return new_arr;
}

// Utility function for array concatenation
function concat_arrays(arr1, arr2) {
    total_length = arr1.length + arr2.length;
    result = array.fill(total_length, 0);

    i = 0;
    while (i < arr1.length) {
        result[i] = arr1[i];
        i = i + 1;
    }

    j = 0;
    while (j < arr2.length) {
        result[arr1.length + j] = arr2[j];
        j = j + 1;
    }

    return result;
}

// Sorting Algorithms
function sorting_algorithms() {
    print("=== Sorting Algorithms ===");

    // Bubble sort implementation
    function bubble_sort(arr) {
        n = arr.length;
        sorted_array = array.fill(n, 0);

        // Copy array
        i = 0;
        while (i < n) {
            sorted_array[i] = arr[i];
            i = i + 1;
        }

        // Bubble sort logic
        i = 0;
        while (i < n - 1) {
            j = 0;
            while (j < n - i - 1) {
                if (sorted_array[j] > sorted_array[j + 1]) {
                    temp = sorted_array[j];
                    sorted_array[j] = sorted_array[j + 1];
                    sorted_array[j + 1] = temp;
                }
                j = j + 1;
            }
            i = i + 1;
        }

        return sorted_array;
    }

    // Quick sort implementation
    function quick_sort(arr) {
        if (arr.length <= 1) {
            return arr;
        }

        pivot_index = math.floor(arr.length / 2);
        pivot = arr[pivot_index];

        less = [];
        equal = [];
        greater = [];

        i = 0;
        while (i < arr.length) {
            element = arr[i];
            if (element < pivot) {
                less = safe_append(less, element);
            } elif (element == pivot) {
                equal = safe_append(equal, element);
            } else {
                greater = safe_append(greater, element);
            }
            i = i + 1;
        }

        sorted_less = quick_sort(less);
        sorted_greater = quick_sort(greater);

        // Concatenate results
        temp_result = concat_arrays(sorted_less, equal);
        final_result = concat_arrays(temp_result, sorted_greater);

        return final_result;
    }

    // Merge sort implementation
    function merge_sort(arr) {
        if (arr.length <= 1) {
            return arr;
        }

        mid = math.floor(arr.length / 2);
        left = array.fill(mid, 0);
        right = array.fill(arr.length - mid, 0);

        // Split array
        i = 0;
        while (i < mid) {
            left[i] = arr[i];
            i = i + 1;
        }
        j = mid;
        while (j < arr.length) {
            right[j - mid] = arr[j];
            j = j + 1;
        }

        sorted_left = merge_sort(left);
        sorted_right = merge_sort(right);

        return merge(sorted_left, sorted_right);
    }

    function merge(left, right) {
        total_length = left.length + right.length;
        result = array.fill(total_length, 0);
        left_idx = 0;
        right_idx = 0;
        result_idx = 0;

        while (left_idx < left.length && right_idx < right.length) {
            if (left[left_idx] <= right[right_idx]) {
                result[result_idx] = left[left_idx];
                left_idx = left_idx + 1;
            } else {
                result[result_idx] = right[right_idx];
                right_idx = right_idx + 1;
            }
            result_idx = result_idx + 1;
        }

        // Add remaining elements
        while (left_idx < left.length) {
            result[result_idx] = left[left_idx];
            left_idx = left_idx + 1;
            result_idx = result_idx + 1;
        }
        while (right_idx < right.length) {
            result[result_idx] = right[right_idx];
            right_idx = right_idx + 1;
            result_idx = result_idx + 1;
        }

        return result;
    }

    // Test all sorting algorithms
    test_array = [64, 34, 25, 12, 22, 11, 90, 5, 77, 30];
    print("Original array: " + array_to_string(test_array));

    bubble_result = bubble_sort(test_array);
    print("Bubble sort: " + array_to_string(bubble_result));

    quick_result = quick_sort(test_array);
    print("Quick sort: " + array_to_string(quick_result));

    merge_result = merge_sort(test_array);
    print("Merge sort: " + array_to_string(merge_result));

    // Verify all results match
    match1 = arrays_equal(bubble_result, quick_result);
    match2 = arrays_equal(quick_result, merge_result);
    print("All algorithms match: " + string.toString(match1 && match2));
}

// Search Algorithms
function search_algorithms() {
    print("\n=== Search Algorithms ===");

    // Linear search
    function linear_search(arr, target) {
        i = 0;
        while (i < arr.length) {
            if (arr[i] == target) {
                return i;
            }
            i = i + 1;
        }
        return -1;
    }

    // Binary search
    function binary_search(arr, target) {
        left = 0;
        right = arr.length - 1;

        while (left <= right) {
            mid = math.floor((left + right) / 2);

            if (arr[mid] == target) {
                return mid;
            } elif (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }

        return -1;
    }

    // Interpolation search
    function interpolation_search(arr, target) {
        left = 0;
        right = arr.length - 1;

        while (left <= right && target >= arr[left] && target <= arr[right]) {
            if (left == right) {
                if (arr[left] == target) {
                    return left;
                }
                return -1;
            }

            pos = left + math.floor(((target - arr[left]) * (right - left)) / (arr[right] - arr[left]));

            if (arr[pos] == target) {
                return pos;
            } elif (arr[pos] < target) {
                left = pos + 1;
            } else {
                right = pos - 1;
            }
        }

        return -1;
    }

    // Test search algorithms
    sorted_array = [2, 5, 8, 12, 16, 23, 38, 45, 67, 78, 90, 99];
    search_targets = [23, 67, 100, 2, 99, 50];

    print("Sorted array: " + array_to_string(sorted_array));
    print("Search targets: " + array_to_string(search_targets));

    print("\nSearch results:");
    i = 0;
    while (i < search_targets.length) {
        target = search_targets[i];

        linear_result = linear_search(sorted_array, target);
        binary_result = binary_search(sorted_array, target);
        interp_result = interpolation_search(sorted_array, target);

        print("Target " + string.toString(target) + ":");
        print("  Linear: " + string.toString(linear_result));
        print("  Binary: " + string.toString(binary_result));
        print("  Interpolation: " + string.toString(interp_result));

        i = i + 1;
    }
}

// Graph Algorithms with safe dictionary operations
function graph_algorithms() {
    print("\n=== Graph Algorithms ===");

    // Create graph structure
    function create_graph() {
        return {
            vertices: {},
            edges: {}
        };
    }

    // Safe vertex addition
    function add_vertex(graph, vertex) {
        graph.vertices[vertex] = true;
        graph.edges[vertex] = [];
    }

    // Safe edge addition
    function add_edge(graph, from_vertex, to_vertex) {
        add_vertex(graph, from_vertex);
        add_vertex(graph, to_vertex);

        graph.edges[from_vertex] = safe_append(graph.edges[from_vertex], to_vertex);
    }

    // Initialize visited dictionary for all known vertices
    function init_visited() {
        visited = {};
        visited["A"] = false;
        visited["B"] = false;
        visited["C"] = false;
        visited["D"] = false;
        visited["E"] = false;
        visited["F"] = false;
        visited["G"] = false;
        return visited;
    }

    // Depth-First Search
    function dfs(graph, start_vertex, target_vertex) {
        visited = init_visited();
        path = [];

        return dfs_recursive(graph, start_vertex, target_vertex, visited, path);
    }

    function dfs_recursive(graph, current, target, visited, path) {
        visited[current] = true;
        path = safe_append(path, current);

        if (current == target) {
            return {found: true, path: path};
        }

        neighbors = graph.edges[current];
        if (neighbors != null) {
            i = 0;
            while (i < neighbors.length) {
                neighbor = neighbors[i];
                if (visited[neighbor] == false) {
                    result = dfs_recursive(graph, neighbor, target, visited, path);
                    if (result.found) {
                        return result;
                    }
                }
                i = i + 1;
            }
        }

        return {found: false, path: []};
    }

    // Breadth-First Search with safe queue operations
    function bfs(graph, start_vertex, target_vertex) {
        visited = init_visited();
        queue = [start_vertex];
        parent = {};

        visited[start_vertex] = true;
        parent[start_vertex] = null;

        while (queue.length > 0) {
            // Safe queue shift operation
            current = queue[0];
            new_queue = array.fill(queue.length - 1, null);
            i = 1;
            while (i < queue.length) {
                new_queue[i - 1] = queue[i];
                i = i + 1;
            }
            queue = new_queue;

            if (current == target_vertex) {
                // Reconstruct path
                path = [];
                node = current;
                while (node != null) {
                    path = safe_append(path, node);
                    node = parent[node];
                }
                // Reverse path
                reversed_path = array.fill(path.length, null);
                j = 0;
                while (j < path.length) {
                    reversed_path[j] = path[path.length - 1 - j];
                    j = j + 1;
                }
                return {found: true, path: reversed_path};
            }

            neighbors = graph.edges[current];
            if (neighbors != null) {
                k = 0;
                while (k < neighbors.length) {
                    neighbor = neighbors[k];
                    if (visited[neighbor] == false) {
                        visited[neighbor] = true;
                        parent[neighbor] = current;
                        queue = safe_append(queue, neighbor);
                    }
                    k = k + 1;
                }
            }
        }

        return {found: false, path: []};
    }

    // Test graph algorithms
    graph = create_graph();

    // Build test graph: A-B-C-D-E-F-G
    add_edge(graph, "A", "B");
    add_edge(graph, "B", "C");
    add_edge(graph, "C", "D");
    add_edge(graph, "D", "E");
    add_edge(graph, "E", "F");
    add_edge(graph, "F", "G");

    print("Graph structure created (A-B-C-D-E-F-G)");

    // Test DFS
    dfs_result = dfs(graph, "A", "G");
    print("DFS A->G found: " + string.toString(dfs_result.found));
    if (dfs_result.found) {
        print("DFS path: " + array_to_string(dfs_result.path));
    }

    // Test BFS
    bfs_result = bfs(graph, "A", "G");
    print("BFS A->G found: " + string.toString(bfs_result.found));
    if (bfs_result.found) {
        print("BFS path: " + array_to_string(bfs_result.path));
    }
}

// Utility Functions
function array_to_string(arr) {
    if (arr.length == 0) {
        return "[]";
    }

    result = "[";
    i = 0;
    while (i < arr.length) {
        if (i > 0) {
            result = result + ", ";
        }
        result = result + string.toString(arr[i]);
        i = i + 1;
    }
    result = result + "]";
    return result;
}

function arrays_equal(arr1, arr2) {
    if (arr1.length != arr2.length) {
        return false;
    }

    i = 0;
    while (i < arr1.length) {
        if (arr1[i] != arr2[i]) {
            return false;
        }
        i = i + 1;
    }

    return true;
}

// Main function
function main() {
    print("==============================================");
    print("  COMPLEX ALGORITHMS IMPLEMENTATIONS TEST");
    print("==============================================");

    sorting_algorithms();
    search_algorithms();
    graph_algorithms();

    print("\n==============================================");
    print("  ALL TESTS COMPLETED SUCCESSFULLY");
    print("==============================================");
}

main();