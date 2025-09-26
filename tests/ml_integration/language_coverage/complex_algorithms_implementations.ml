// Complex Algorithms Implementations Test
// Demonstrates sophisticated algorithms and computational patterns in ML

import string;
import datetime;

// Sorting algorithms
function sorting_algorithms() {
    print("=== Sorting Algorithms ===");

    // Bubble sort implementation
    function bubble_sort(arr) {
        sorted_array = [];
        n = arr.length();

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
        if (arr.length() <= 1) {
            return arr;
        }

        pivot_index = Math.floor(arr.length() / 2);
        pivot = arr[pivot_index];

        less = [];
        equal = [];
        greater = [];

        i = 0;
        while (i < arr.length()) {
            element = arr[i];
            if (element < pivot) {
                less[less.length()] = element;
            } elif (element == pivot) {
                equal[equal.length()] = element;
            } else {
                greater[greater.length()] = element;
            }
            i = i + 1;
        }

        sorted_less = quick_sort(less);
        sorted_greater = quick_sort(greater);

        // Concatenate results
        result = [];
        j = 0;
        while (j < sorted_less.length()) {
            result[result.length()] = sorted_less[j];
            j = j + 1;
        }
        k = 0;
        while (k < equal.length()) {
            result[result.length()] = equal[k];
            k = k + 1;
        }
        l = 0;
        while (l < sorted_greater.length()) {
            result[result.length()] = sorted_greater[l];
            l = l + 1;
        }

        return result;
    }

    // Merge sort implementation
    function merge_sort(arr) {
        if (arr.length() <= 1) {
            return arr;
        }

        mid = Math.floor(arr.length() / 2);
        left = [];
        right = [];

        // Split array
        i = 0;
        while (i < mid) {
            left[i] = arr[i];
            i = i + 1;
        }
        j = mid;
        while (j < arr.length()) {
            right[j - mid] = arr[j];
            j = j + 1;
        }

        sorted_left = merge_sort(left);
        sorted_right = merge_sort(right);

        return merge(sorted_left, sorted_right);
    }

    function merge(left, right) {
        result = [];
        left_idx = 0;
        right_idx = 0;

        while (left_idx < left.length() && right_idx < right.length()) {
            if (left[left_idx] <= right[right_idx]) {
                result[result.length()] = left[left_idx];
                left_idx = left_idx + 1;
            } else {
                result[result.length()] = right[right_idx];
                right_idx = right_idx + 1;
            }
        }

        // Add remaining elements
        while (left_idx < left.length()) {
            result[result.length()] = left[left_idx];
            left_idx = left_idx + 1;
        }
        while (right_idx < right.length()) {
            result[result.length()] = right[right_idx];
            right_idx = right_idx + 1;
        }

        return result;
    }

    // Test all sorting algorithms
    test_array = [64, 34, 25, 12, 22, 11, 90, 5, 77, 30];

    print("Original array: " + test_array);

    bubble_result = bubble_sort(test_array);
    print("Bubble sort: " + bubble_result);

    quick_result = quick_sort(test_array);
    print("Quick sort: " + quick_result);

    merge_result = merge_sort(test_array);
    print("Merge sort: " + merge_result);

    // Verify all algorithms produce same result
    match1 = arrays_equal(bubble_result, quick_result);
    match2 = arrays_equal(quick_result, merge_result);

    print("All algorithms match: " + (match1 && match2));

    return {
        original: test_array,
        bubble_sorted: bubble_result,
        quick_sorted: quick_result,
        merge_sorted: merge_result,
        all_match: match1 && match2
    };
}

// Search algorithms
function search_algorithms() {
    print("\n=== Search Algorithms ===");

    // Linear search
    function linear_search(arr, target) {
        i = 0;
        while (i < arr.length()) {
            if (arr[i] == target) {
                return i;
            }
            i = i + 1;
        }
        return -1;
    }

    // Binary search (requires sorted array)
    function binary_search(arr, target) {
        left = 0;
        right = arr.length() - 1;

        while (left <= right) {
            mid = Math.floor((left + right) / 2);

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

    // Interpolation search (for uniformly distributed data)
    function interpolation_search(arr, target) {
        left = 0;
        right = arr.length() - 1;

        while (left <= right && target >= arr[left] && target <= arr[right]) {
            if (left == right) {
                return arr[left] == target ? left : -1;
            }

            // Calculate position using interpolation formula
            pos = left + Math.floor(((target - arr[left]) * (right - left)) / (arr[right] - arr[left]));

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

    print("Sorted array: " + sorted_array);
    print("Search targets: " + search_targets);

    print("\nSearch results:");
    i = 0;
    while (i < search_targets.length()) {
        target = search_targets[i];

        linear_result = linear_search(sorted_array, target);
        binary_result = binary_search(sorted_array, target);
        interpolation_result = interpolation_search(sorted_array, target);

        print("Target " + target + ":");
        print("  Linear: " + linear_result);
        print("  Binary: " + binary_result);
        print("  Interpolation: " + interpolation_result);

        i = i + 1;
    }

    return {
        test_array: sorted_array,
        search_targets: search_targets,
        algorithms_tested: 3
    };
}

// Graph algorithms
function graph_algorithms() {
    print("\n=== Graph Algorithms ===");

    // Graph representation using adjacency lists
    function create_graph() {
        return {
            vertices: {},
            edges: {}
        };
    }

    function add_vertex(graph, vertex) {
        if (graph.vertices[vertex] == null) {
            graph.vertices[vertex] = true;
            graph.edges[vertex] = [];
        }
    }

    function add_edge(graph, from_vertex, to_vertex) {
        add_vertex(graph, from_vertex);
        add_vertex(graph, to_vertex);

        graph.edges[from_vertex][graph.edges[from_vertex].length()] = to_vertex;
    }

    // Depth-First Search (DFS)
    function dfs(graph, start_vertex, target_vertex) {
        visited = {};
        path = [];

        return dfs_recursive(graph, start_vertex, target_vertex, visited, path);
    }

    function dfs_recursive(graph, current, target, visited, path) {
        visited[current] = true;
        path[path.length()] = current;

        if (current == target) {
            return {found: true, path: path};
        }

        neighbors = graph.edges[current];
        if (neighbors != null) {
            i = 0;
            while (i < neighbors.length()) {
                neighbor = neighbors[i];
                if (visited[neighbor] != true) {
                    result = dfs_recursive(graph, neighbor, target, visited, path);
                    if (result.found) {
                        return result;
                    }
                }
                i = i + 1;
            }
        }

        // Backtrack
        path.pop();
        return {found: false, path: []};
    }

    // Breadth-First Search (BFS)
    function bfs(graph, start_vertex, target_vertex) {
        visited = {};
        queue = [start_vertex];
        parent = {};

        visited[start_vertex] = true;
        parent[start_vertex] = null;

        while (queue.length() > 0) {
            current = queue.shift();

            if (current == target_vertex) {
                // Reconstruct path
                path = [];
                node = current;
                while (node != null) {
                    path.unshift(node);
                    node = parent[node];
                }
                return {found: true, path: path};
            }

            neighbors = graph.edges[current];
            if (neighbors != null) {
                i = 0;
                while (i < neighbors.length()) {
                    neighbor = neighbors[i];
                    if (visited[neighbor] != true) {
                        visited[neighbor] = true;
                        parent[neighbor] = current;
                        queue[queue.length()] = neighbor;
                    }
                    i = i + 1;
                }
            }
        }

        return {found: false, path: []};
    }

    // Create test graph
    //     A --- B --- D
    //     |     |     |
    //     C --- E --- F
    //           |
    //           G

    graph = create_graph();
    add_edge(graph, "A", "B");
    add_edge(graph, "A", "C");
    add_edge(graph, "B", "D");
    add_edge(graph, "B", "E");
    add_edge(graph, "C", "E");
    add_edge(graph, "D", "F");
    add_edge(graph, "E", "F");
    add_edge(graph, "E", "G");

    print("Graph structure created (A-B-C-D-E-F-G)");

    // Test DFS and BFS
    dfs_result = dfs(graph, "A", "G");
    bfs_result = bfs(graph, "A", "G");

    print("Path from A to G:");
    print("  DFS: " + (dfs_result.found ? dfs_result.path : "Not found"));
    print("  BFS: " + (bfs_result.found ? bfs_result.path : "Not found"));

    return {
        graph_created: true,
        dfs_path: dfs_result.path,
        bfs_path: bfs_result.path,
        both_found: dfs_result.found && bfs_result.found
    };
}

// Dynamic programming algorithms
function dynamic_programming_algorithms() {
    print("\n=== Dynamic Programming Algorithms ===");

    // Fibonacci with memoization
    function fibonacci_memo(n, memo) {
        if (memo == null) memo = {};

        if (n <= 1) return n;
        if (memo[n] != null) return memo[n];

        memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo);
        return memo[n];
    }

    // Longest Common Subsequence (LCS)
    function longest_common_subsequence(str1, str2) {
        m = string.length(str1);
        n = string.length(str2);

        // Create DP table
        dp = [];
        i = 0;
        while (i <= m) {
            dp[i] = [];
            j = 0;
            while (j <= n) {
                dp[i][j] = 0;
                j = j + 1;
            }
            i = i + 1;
        }

        // Fill DP table
        i = 1;
        while (i <= m) {
            j = 1;
            while (j <= n) {
                if (string.char_at(str1, i - 1) == string.char_at(str2, j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                } else {
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
                }
                j = j + 1;
            }
            i = i + 1;
        }

        return dp[m][n];
    }

    function max(a, b) {
        return a > b ? a : b;
    }

    // Knapsack problem (0/1 knapsack)
    function knapsack(weights, values, capacity) {
        n = weights.length();

        // Create DP table
        dp = [];
        i = 0;
        while (i <= n) {
            dp[i] = [];
            j = 0;
            while (j <= capacity) {
                dp[i][j] = 0;
                j = j + 1;
            }
            i = i + 1;
        }

        // Fill DP table
        i = 1;
        while (i <= n) {
            w = 0;
            while (w <= capacity) {
                if (weights[i - 1] <= w) {
                    include_value = values[i - 1] + dp[i - 1][w - weights[i - 1]];
                    exclude_value = dp[i - 1][w];
                    dp[i][w] = max(include_value, exclude_value);
                } else {
                    dp[i][w] = dp[i - 1][w];
                }
                w = w + 1;
            }
            i = i + 1;
        }

        return dp[n][capacity];
    }

    // Coin change problem
    function coin_change(coins, amount) {
        dp = [];
        i = 0;
        while (i <= amount) {
            dp[i] = amount + 1; // Initialize with impossible value
            i = i + 1;
        }
        dp[0] = 0;

        i = 1;
        while (i <= amount) {
            j = 0;
            while (j < coins.length()) {
                coin = coins[j];
                if (coin <= i) {
                    dp[i] = min(dp[i], dp[i - coin] + 1);
                }
                j = j + 1;
            }
            i = i + 1;
        }

        return dp[amount] > amount ? -1 : dp[amount];
    }

    function min(a, b) {
        return a < b ? a : b;
    }

    // Test dynamic programming algorithms
    print("Fibonacci with memoization:");
    fib_numbers = [10, 15, 20];
    k = 0;
    while (k < fib_numbers.length()) {
        n = fib_numbers[k];
        result = fibonacci_memo(n, null);
        print("  fib(" + n + ") = " + result);
        k = k + 1;
    }

    print("\nLongest Common Subsequence:");
    lcs_test1 = longest_common_subsequence("ABCDGH", "AEDFHR");
    lcs_test2 = longest_common_subsequence("AGGTAB", "GXTXAYB");
    print("  LCS('ABCDGH', 'AEDFHR') = " + lcs_test1);
    print("  LCS('AGGTAB', 'GXTXAYB') = " + lcs_test2);

    print("\nKnapsack Problem:");
    weights = [10, 20, 30];
    values = [60, 100, 120];
    capacity = 50;
    knapsack_result = knapsack(weights, values, capacity);
    print("  Weights: " + weights + ", Values: " + values + ", Capacity: " + capacity);
    print("  Maximum value: " + knapsack_result);

    print("\nCoin Change Problem:");
    coins = [1, 3, 4];
    amounts = [6, 8, 11];
    l = 0;
    while (l < amounts.length()) {
        amount = amounts[l];
        coin_result = coin_change(coins, amount);
        print("  Amount " + amount + " requires " + coin_result + " coins");
        l = l + 1;
    }

    return {
        fibonacci_tested: fib_numbers,
        lcs_results: [lcs_test1, lcs_test2],
        knapsack_result: knapsack_result,
        coin_change_tested: amounts
    };
}

// String algorithms
function string_algorithms() {
    print("\n=== String Algorithms ===");

    // Naive string matching
    function naive_string_search(text, pattern) {
        matches = [];
        text_len = string.length(text);
        pattern_len = string.length(pattern);

        i = 0;
        while (i <= text_len - pattern_len) {
            j = 0;
            while (j < pattern_len && string.char_at(text, i + j) == string.char_at(pattern, j)) {
                j = j + 1;
            }

            if (j == pattern_len) {
                matches[matches.length()] = i;
            }
            i = i + 1;
        }

        return matches;
    }

    // Edit distance (Levenshtein distance)
    function edit_distance(str1, str2) {
        m = string.length(str1);
        n = string.length(str2);

        // Create DP table
        dp = [];
        i = 0;
        while (i <= m) {
            dp[i] = [];
            j = 0;
            while (j <= n) {
                if (i == 0) {
                    dp[i][j] = j;
                } elif (j == 0) {
                    dp[i][j] = i;
                } else {
                    dp[i][j] = 0;
                }
                j = j + 1;
            }
            i = i + 1;
        }

        // Fill DP table
        i = 1;
        while (i <= m) {
            j = 1;
            while (j <= n) {
                if (string.char_at(str1, i - 1) == string.char_at(str2, j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    dp[i][j] = 1 + min3(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]);
                }
                j = j + 1;
            }
            i = i + 1;
        }

        return dp[m][n];
    }

    function min3(a, b, c) {
        return min(min(a, b), c);
    }

    function min(a, b) {
        return a < b ? a : b;
    }

    // Palindrome check
    function is_palindrome(str) {
        left = 0;
        right = string.length(str) - 1;

        while (left < right) {
            if (string.char_at(str, left) != string.char_at(str, right)) {
                return false;
            }
            left = left + 1;
            right = right - 1;
        }

        return true;
    }

    // Test string algorithms
    print("String search algorithm:");
    search_text = "ababcabcabababc";
    search_pattern = "abab";
    matches = naive_string_search(search_text, search_pattern);
    print("  Text: '" + search_text + "'");
    print("  Pattern: '" + search_pattern + "'");
    print("  Matches at positions: " + matches);

    print("\nEdit distance calculations:");
    edit_pairs = [
        ["kitten", "sitting"],
        ["sunday", "saturday"],
        ["intention", "execution"]
    ];
    m = 0;
    while (m < edit_pairs.length()) {
        pair = edit_pairs[m];
        str1 = pair[0];
        str2 = pair[1];
        distance = edit_distance(str1, str2);
        print("  '" + str1 + "' vs '" + str2 + "': " + distance);
        m = m + 1;
    }

    print("\nPalindrome checks:");
    palindrome_tests = ["racecar", "hello", "madam", "abcba", "test"];
    n = 0;
    while (n < palindrome_tests.length()) {
        test_str = palindrome_tests[n];
        is_pal = is_palindrome(test_str);
        print("  '" + test_str + "': " + is_pal);
        n = n + 1;
    }

    return {
        string_search: matches,
        edit_distance_pairs: edit_pairs,
        palindrome_tests: palindrome_tests
    };
}

// Utility functions
function arrays_equal(arr1, arr2) {
    if (arr1.length() != arr2.length()) return false;

    i = 0;
    while (i < arr1.length()) {
        if (arr1[i] != arr2[i]) return false;
        i = i + 1;
    }

    return true;
}

// Math utility functions
Math = {
    floor: function(x) {
        return x >= 0 ? Math.int(x) : Math.int(x) - 1;
    },
    int: function(x) {
        return x >= 0 ? x - (x % 1) : x - (x % 1);
    }
};

// Array utility functions
Array.prototype.shift = function() {
    if (this.length() == 0) return null;
    first = this[0];
    i = 0;
    while (i < this.length() - 1) {
        this[i] = this[i + 1];
        i = i + 1;
    }
    this.pop();
    return first;
};

Array.prototype.unshift = function(item) {
    i = this.length();
    while (i > 0) {
        this[i] = this[i - 1];
        i = i - 1;
    }
    this[0] = item;
};

Array.prototype.pop = function() {
    if (this.length() == 0) return null;
    last = this[this.length() - 1];
    this.resize(this.length() - 1);
    return last;
};

// Main function to run all complex algorithm tests
function main() {
    print("==============================================");
    print("  COMPLEX ALGORITHMS IMPLEMENTATIONS TEST");
    print("==============================================");

    results = {};

    results.sorting = sorting_algorithms();
    results.searching = search_algorithms();
    results.graph = graph_algorithms();
    results.dynamic_programming = dynamic_programming_algorithms();
    results.string_algorithms = string_algorithms();

    print("\n==============================================");
    print("  ALL COMPLEX ALGORITHMS TESTS COMPLETED");
    print("==============================================");

    return results;
}

// Execute comprehensive complex algorithms test
main();