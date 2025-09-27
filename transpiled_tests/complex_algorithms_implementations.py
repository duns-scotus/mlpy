"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib.console_bridge import console
from mlpy.stdlib import getCurrentTime, processData

from mlpy.stdlib.string_bridge import string as ml_string

from mlpy.stdlib.datetime_bridge import datetime as ml_datetime

def sorting_algorithms():
    print('=== Sorting Algorithms ===')
    def bubble_sort(arr):
        sorted_array = []
        n = arr['length']()
        i = 0
        while (i < n):
            sorted_array[i] = arr[i]
            i = (i + 1)
        i = 0
        while (i < (n - 1)):
            j = 0
            while (j < ((n - i) - 1)):
                if (sorted_array[j] > sorted_array[(j + 1)]):
                    temp = sorted_array[j]
                    sorted_array[j] = sorted_array[(j + 1)]
                    sorted_array[(j + 1)] = temp
                j = (j + 1)
            i = (i + 1)
        return sorted_array
    def quick_sort(arr):
        if (arr['length']() <= 1):
            return arr
        pivot_index = Math['floor']((arr['length']() / 2))
        pivot = arr[pivot_index]
        less = []
        equal = []
        greater = []
        i = 0
        while (i < arr['length']()):
            element = arr[i]
            if (element < pivot):
                less[less['length']()] = element
            elif (element == pivot):
                equal[equal['length']()] = element
            else:
                greater[greater['length']()] = element
            i = (i + 1)
        sorted_less = quick_sort(less)
        sorted_greater = quick_sort(greater)
        result = []
        j = 0
        while (j < sorted_less['length']()):
            result[result['length']()] = sorted_less[j]
            j = (j + 1)
        k = 0
        while (k < equal['length']()):
            result[result['length']()] = equal[k]
            k = (k + 1)
        l = 0
        while (l < sorted_greater['length']()):
            result[result['length']()] = sorted_greater[l]
            l = (l + 1)
        return result
    def merge_sort(arr):
        if (arr['length']() <= 1):
            return arr
        mid = Math['floor']((arr['length']() / 2))
        left = []
        right = []
        i = 0
        while (i < mid):
            left[i] = arr[i]
            i = (i + 1)
        j = mid
        while (j < arr['length']()):
            right[(j - mid)] = arr[j]
            j = (j + 1)
        sorted_left = merge_sort(left)
        sorted_right = merge_sort(right)
        return merge(sorted_left, sorted_right)
    def merge(left, right):
        result = []
        left_idx = 0
        right_idx = 0
        while ((left_idx < left['length']()) and (right_idx < right['length']())):
            if (left[left_idx] <= right[right_idx]):
                result[result['length']()] = left[left_idx]
                left_idx = (left_idx + 1)
            else:
                result[result['length']()] = right[right_idx]
                right_idx = (right_idx + 1)
        while (left_idx < left['length']()):
            result[result['length']()] = left[left_idx]
            left_idx = (left_idx + 1)
        while (right_idx < right['length']()):
            result[result['length']()] = right[right_idx]
            right_idx = (right_idx + 1)
        return result
    test_array = [64, 34, 25, 12, 22, 11, 90, 5, 77, 30]
    print((str('Original array: ') + str(test_array)))
    bubble_result = bubble_sort(test_array)
    print((str('Bubble sort: ') + str(bubble_result)))
    quick_result = quick_sort(test_array)
    print((str('Quick sort: ') + str(quick_result)))
    merge_result = merge_sort(test_array)
    print((str('Merge sort: ') + str(merge_result)))
    match1 = arrays_equal(bubble_result, quick_result)
    match2 = arrays_equal(quick_result, merge_result)
    print((str('All algorithms match: ') + str((match1 and match2))))
    return {'original': test_array, 'bubble_sorted': bubble_result, 'quick_sorted': quick_result, 'merge_sorted': merge_result, 'all_match': (match1 and match2)}

def search_algorithms():
    print('\\n=== Search Algorithms ===')
    def linear_search(arr, target):
        i = 0
        while (i < arr['length']()):
            if (arr[i] == target):
                return i
            i = (i + 1)
        return 1
    def binary_search(arr, target):
        left = 0
        right = (arr['length']() - 1)
        while (left <= right):
            mid = Math['floor'](((left + right) / 2))
            if (arr[mid] == target):
                return mid
            elif (arr[mid] < target):
                left = (mid + 1)
            else:
                right = (mid - 1)
        return 1
    def interpolation_search(arr, target):
        left = 0
        right = (arr['length']() - 1)
        while (((left <= right) and (target >= arr[left])) and (target <= arr[right])):
            if (left == right):
                return left if (arr[left] == target) else 1
            pos = (left + Math['floor']((((target - arr[left]) * (right - left)) / (arr[right] - arr[left]))))
            if (arr[pos] == target):
                return pos
            elif (arr[pos] < target):
                left = (pos + 1)
            else:
                right = (pos - 1)
        return 1
    sorted_array = [2, 5, 8, 12, 16, 23, 38, 45, 67, 78, 90, 99]
    search_targets = [23, 67, 100, 2, 99, 50]
    print((str('Sorted array: ') + str(sorted_array)))
    print((str('Search targets: ') + str(search_targets)))
    print('\\nSearch results:')
    i = 0
    while (i < search_targets['length']()):
        target = search_targets[i]
        linear_result = linear_search(sorted_array, target)
        binary_result = binary_search(sorted_array, target)
        interpolation_result = interpolation_search(sorted_array, target)
        print((str((str('Target ') + str(target))) + str(':')))
        print((str('  Linear: ') + str(linear_result)))
        print((str('  Binary: ') + str(binary_result)))
        print((str('  Interpolation: ') + str(interpolation_result)))
        i = (i + 1)
    return {'test_array': sorted_array, 'search_targets': search_targets, 'algorithms_tested': 3}

def graph_algorithms():
    print('\\n=== Graph Algorithms ===')
    def create_graph():
        return {'vertices': {}, 'edges': {}}
    def add_vertex(graph, vertex):
        if (graph['vertices'][vertex] == None):
            graph['vertices'][vertex] = True
            graph['edges'][vertex] = []
    def add_edge(graph, from_vertex, to_vertex):
        add_vertex(graph, from_vertex)
        add_vertex(graph, to_vertex)
        graph['edges'][from_vertex][graph['edges'][from_vertex]['length']()] = to_vertex
    def dfs(graph, start_vertex, target_vertex):
        visited = {}
        path = []
        return dfs_recursive(graph, start_vertex, target_vertex, visited, path)
    def dfs_recursive(graph, current, target, visited, path):
        visited[current] = True
        path[path['length']()] = current
        if (current == target):
            return {'found': True, 'path': path}
        neighbors = graph['edges'][current]
        if (neighbors != None):
            i = 0
            while (i < neighbors['length']()):
                neighbor = neighbors[i]
                if (visited[neighbor] != True):
                    result = dfs_recursive(graph, neighbor, target, visited, path)
                    if result['found']:
                        return result
                i = (i + 1)
        path['pop']()
        return {'found': False, 'path': []}
    def bfs(graph, start_vertex, target_vertex):
        visited = {}
        queue = [start_vertex]
        parent = {}
        visited[start_vertex] = True
        parent[start_vertex] = None
        while (queue['length']() > 0):
            current = queue['shift']()
            if (current == target_vertex):
                path = []
                node = current
                while (node != None):
                    path['unshift'](node)
                    node = parent[node]
                return {'found': True, 'path': path}
            neighbors = graph['edges'][current]
            if (neighbors != None):
                i = 0
                while (i < neighbors['length']()):
                    neighbor = neighbors[i]
                    if (visited[neighbor] != True):
                        visited[neighbor] = True
                        parent[neighbor] = current
                        queue[queue['length']()] = neighbor
                    i = (i + 1)
        return {'found': False, 'path': []}
    graph = create_graph()
    add_edge(graph, 'A', 'B')
    add_edge(graph, 'A', 'C')
    add_edge(graph, 'B', 'D')
    add_edge(graph, 'B', 'E')
    add_edge(graph, 'C', 'E')
    add_edge(graph, 'D', 'F')
    add_edge(graph, 'E', 'F')
    add_edge(graph, 'E', 'G')
    print('Graph structure created (A-B-C-D-E-F-G)')
    dfs_result = dfs(graph, 'A', 'G')
    bfs_result = bfs(graph, 'A', 'G')
    print('Path from A to G:')
    print((str('  DFS: ') + str(dfs_result['path'] if dfs_result['found'] else 'Not found')))
    print((str('  BFS: ') + str(bfs_result['path'] if bfs_result['found'] else 'Not found')))
    return {'graph_created': True, 'dfs_path': dfs_result['path'], 'bfs_path': bfs_result['path'], 'both_found': (dfs_result['found'] and bfs_result['found'])}

def dynamic_programming_algorithms():
    print('\\n=== Dynamic Programming Algorithms ===')
    def fibonacci_memo(n, memo):
        if (memo == None):
            memo = {}
        if (n <= 1):
            return n
        if (memo[n] != None):
            return memo[n]
        memo[n] = (fibonacci_memo((n - 1), memo) + fibonacci_memo((n - 2), memo))
        return memo[n]
    def longest_common_subsequence(str1, str2):
        m = ml_string.length(str1)
        n = ml_string.length(str2)
        dp = []
        i = 0
        while (i <= m):
            dp[i] = []
            j = 0
            while (j <= n):
                dp[i][j] = 0
                j = (j + 1)
            i = (i + 1)
        i = 1
        while (i <= m):
            j = 1
            while (j <= n):
                if (ml_string.char_at(str1, (i - 1)) == ml_string.char_at(str2, (j - 1))):
                    dp[i][j] = (dp[(i - 1)][(j - 1)] + 1)
                else:
                    dp[i][j] = max(dp[(i - 1)][j], dp[i][(j - 1)])
                j = (j + 1)
            i = (i + 1)
        return dp[m][n]
    def max(a, b):
        return a if (a > b) else b
    def knapsack(weights, values, capacity):
        n = weights['length']()
        dp = []
        i = 0
        while (i <= n):
            dp[i] = []
            j = 0
            while (j <= capacity):
                dp[i][j] = 0
                j = (j + 1)
            i = (i + 1)
        i = 1
        while (i <= n):
            w = 0
            while (w <= capacity):
                if (weights[(i - 1)] <= w):
                    include_value = (values[(i - 1)] + dp[(i - 1)][(w - weights[(i - 1)])])
                    exclude_value = dp[(i - 1)][w]
                    dp[i][w] = max(include_value, exclude_value)
                else:
                    dp[i][w] = dp[(i - 1)][w]
                w = (w + 1)
            i = (i + 1)
        return dp[n][capacity]
    def coin_change(coins, amount):
        dp = []
        i = 0
        while (i <= amount):
            dp[i] = (amount + 1)
            i = (i + 1)
        dp[0] = 0
        i = 1
        while (i <= amount):
            j = 0
            while (j < coins['length']()):
                coin = coins[j]
                if (coin <= i):
                    dp[i] = min(dp[i], (dp[(i - coin)] + 1))
                j = (j + 1)
            i = (i + 1)
        return 1 if (dp[amount] > amount) else dp[amount]
    def min(a, b):
        return a if (a < b) else b
    print('Fibonacci with memoization:')
    fib_numbers = [10, 15, 20]
    k = 0
    while (k < fib_numbers['length']()):
        n = fib_numbers[k]
        result = fibonacci_memo(n, None)
        print((str((str((str('  fib(') + str(n))) + str(') = '))) + str(result)))
        k = (k + 1)
    print('\\nLongest Common Subsequence:')
    lcs_test1 = longest_common_subsequence('ABCDGH', 'AEDFHR')
    lcs_test2 = longest_common_subsequence('AGGTAB', 'GXTXAYB')
    print((str("  LCS('ABCDGH', 'AEDFHR') = ") + str(lcs_test1)))
    print((str("  LCS('AGGTAB', 'GXTXAYB') = ") + str(lcs_test2)))
    print('\\nKnapsack Problem:')
    weights = [10, 20, 30]
    values = [60, 100, 120]
    capacity = 50
    knapsack_result = knapsack(weights, values, capacity)
    print((str((str((str((str((str('  Weights: ') + str(weights))) + str(', Values: '))) + str(values))) + str(', Capacity: '))) + str(capacity)))
    print((str('  Maximum value: ') + str(knapsack_result)))
    print('\\nCoin Change Problem:')
    coins = [1, 3, 4]
    amounts = [6, 8, 11]
    l = 0
    while (l < amounts['length']()):
        amount = amounts[l]
        coin_result = coin_change(coins, amount)
        print((str((str((str((str('  Amount ') + str(amount))) + str(' requires '))) + str(coin_result))) + str(' coins')))
        l = (l + 1)
    return {'fibonacci_tested': fib_numbers, 'lcs_results': [lcs_test1, lcs_test2], 'knapsack_result': knapsack_result, 'coin_change_tested': amounts}

def string_algorithms():
    print('\\n=== String Algorithms ===')
    def naive_string_search(text, pattern):
        matches = []
        text_len = ml_string.length(text)
        pattern_len = ml_string.length(pattern)
        i = 0
        while (i <= (text_len - pattern_len)):
            j = 0
            while ((j < pattern_len) and (ml_string.char_at(text, (i + j)) == ml_string.char_at(pattern, j))):
                j = (j + 1)
            if (j == pattern_len):
                matches[matches['length']()] = i
            i = (i + 1)
        return matches
    def edit_distance(str1, str2):
        m = ml_string.length(str1)
        n = ml_string.length(str2)
        dp = []
        i = 0
        while (i <= m):
            dp[i] = []
            j = 0
            while (j <= n):
                if (i == 0):
                    dp[i][j] = j
                elif (j == 0):
                    dp[i][j] = i
                else:
                    dp[i][j] = 0
                j = (j + 1)
            i = (i + 1)
        i = 1
        while (i <= m):
            j = 1
            while (j <= n):
                if (ml_string.char_at(str1, (i - 1)) == ml_string.char_at(str2, (j - 1))):
                    dp[i][j] = dp[(i - 1)][(j - 1)]
                else:
                    dp[i][j] = (1 + min3(dp[(i - 1)][j], dp[i][(j - 1)], dp[(i - 1)][(j - 1)]))
                j = (j + 1)
            i = (i + 1)
        return dp[m][n]
    def min3(a, b, c):
        return min(min(a, b), c)
    def min(a, b):
        return a if (a < b) else b
    def is_palindrome(str):
        left = 0
        right = (ml_string.length(str) - 1)
        while (left < right):
            if (ml_string.char_at(str, left) != ml_string.char_at(str, right)):
                return False
            left = (left + 1)
            right = (right - 1)
        return True
    print('String search algorithm:')
    search_text = 'ababcabcabababc'
    search_pattern = 'abab'
    matches = naive_string_search(search_text, search_pattern)
    print((str((str("  Text: '") + str(search_text))) + str("'")))
    print((str((str("  Pattern: '") + str(search_pattern))) + str("'")))
    print((str('  Matches at positions: ') + str(matches)))
    print('\\nEdit distance calculations:')
    edit_pairs = [['kitten', 'sitting'], ['sunday', 'saturday'], ['intention', 'execution']]
    m = 0
    while (m < edit_pairs['length']()):
        pair = edit_pairs[m]
        str1 = pair[0]
        str2 = pair[1]
        distance = edit_distance(str1, str2)
        print((str((str((str((str((str("  '") + str(str1))) + str("' vs '"))) + str(str2))) + str("': "))) + str(distance)))
        m = (m + 1)
    print('\\nPalindrome checks:')
    palindrome_tests = ['racecar', 'hello', 'madam', 'abcba', 'test']
    n = 0
    while (n < palindrome_tests['length']()):
        test_str = palindrome_tests[n]
        is_pal = is_palindrome(test_str)
        print((str((str((str("  '") + str(test_str))) + str("': "))) + str(is_pal)))
        n = (n + 1)
    return {'string_search': matches, 'edit_distance_pairs': edit_pairs, 'palindrome_tests': palindrome_tests}

def arrays_equal(arr1, arr2):
    if (arr1['length']() != arr2['length']()):
        return False
    i = 0
    while (i < arr1['length']()):
        if (arr1[i] != arr2[i]):
            return False
        i = (i + 1)
    return True

Math = {'floor': lambda x: Math['int'](x) if (x >= 0) else (Math['int'](x) - 1), 'int': lambda x: (x - (x % 1)) if (x >= 0) else (x - (x % 1))}

Array['prototype']['shift'] = lambda : this[0]

Array['prototype']['unshift'] = lambda item: None

Array['prototype']['pop'] = lambda : this[(this['length']() - 1)]

def main():
    print('==============================================')
    print('  COMPLEX ALGORITHMS IMPLEMENTATIONS TEST')
    print('==============================================')
    results = {}
    results['sorting'] = sorting_algorithms()
    results['searching'] = search_algorithms()
    results['graph'] = graph_algorithms()
    results['dynamic_programming'] = dynamic_programming_algorithms()
    results['string_algorithms'] = string_algorithms()
    print('\\n==============================================')
    print('  ALL COMPLEX ALGORITHMS TESTS COMPLETED')
    print('==============================================')
    return results

main()

# End of generated code