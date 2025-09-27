"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib.console_bridge import console
from mlpy.stdlib import getCurrentTime, processData

from mlpy.stdlib.string_bridge import string as ml_string

from mlpy.stdlib.datetime_bridge import datetime as ml_datetime

def stack_implementation():
    print('=== Stack Implementation and Operations ===')
    def create_stack():
        return {'items': [], 'top': 1}
    def push(stack, item):
        stack['top'] = (stack['top'] + 1)
        stack['items'][stack['top']] = item
    def pop(stack):
        if (stack['top'] == 1):
            return None
        item = stack['items'][stack['top']]
        stack['top'] = (stack['top'] - 1)
        return item
    def peek(stack):
        if (stack['top'] == 1):
            return None
        return stack['items'][stack['top']]
    def is_empty(stack):
        return (stack['top'] == 1)
    def stack_size(stack):
        return (stack['top'] + 1)
    stack = create_stack()
    print('Testing stack operations:')
    print((str('Initial stack empty: ') + str(is_empty(stack))))
    push(stack, 10)
    push(stack, 20)
    push(stack, 30)
    push(stack, 40)
    print('After pushing 10, 20, 30, 40:')
    print((str('  Stack size: ') + str(stack_size(stack))))
    print((str('  Top element: ') + str(peek(stack))))
    print('Popping elements:')
    while is_empty(stack):
        element = pop(stack)
        print((str((str((str('  Popped: ') + str(element))) + str(', Remaining size: '))) + str(stack_size(stack))))
    return {'stack_tested': True, 'operations': ['push', 'pop', 'peek', 'is_empty', 'size']}

def queue_implementation():
    print('\\n=== Queue Implementation and Operations ===')
    def create_queue():
        return {'items': [], 'front': 0, 'rear': 1, 'count': 0}
    def enqueue(queue, item):
        queue['rear'] = (queue['rear'] + 1)
        queue['items'][queue['rear']] = item
        queue['count'] = (queue['count'] + 1)
    def dequeue(queue):
        if (queue['count'] == 0):
            return None
        item = queue['items'][queue['front']]
        queue['front'] = (queue['front'] + 1)
        queue['count'] = (queue['count'] - 1)
        return item
    def queue_front(queue):
        if (queue['count'] == 0):
            return None
        return queue['items'][queue['front']]
    def queue_is_empty(queue):
        return (queue['count'] == 0)
    def queue_size(queue):
        return queue['count']
    queue = create_queue()
    print('Testing queue operations:')
    print((str('Initial queue empty: ') + str(queue_is_empty(queue))))
    enqueue(queue, 'A')
    enqueue(queue, 'B')
    enqueue(queue, 'C')
    enqueue(queue, 'D')
    print('After enqueuing A, B, C, D:')
    print((str('  Queue size: ') + str(queue_size(queue))))
    print((str('  Front element: ') + str(queue_front(queue))))
    print('Dequeuing elements:')
    while queue_is_empty(queue):
        element = dequeue(queue)
        print((str((str((str('  Dequeued: ') + str(element))) + str(', Remaining size: '))) + str(queue_size(queue))))
    return {'queue_tested': True, 'operations': ['enqueue', 'dequeue', 'front', 'is_empty', 'size']}

def linked_list_implementation():
    print('\\n=== Linked List Implementation ===')
    def create_node(data):
        return {'data': data, 'next': None}
    def create_linked_list():
        return {'head': None, 'size': 0}
    def insert_at_beginning(list, data):
        new_node = create_node(data)
        new_node['next'] = list['head']
        list['head'] = new_node
        list['size'] = (list['size'] + 1)
    def insert_at_end(list, data):
        new_node = create_node(data)
        if (list['head'] == None):
            list['head'] = new_node
        else:
            current = list['head']
            while (current['next'] != None):
                current = current['next']
            current['next'] = new_node
        list['size'] = (list['size'] + 1)
    def insert_at_position(list, position, data):
        if ((position < 0) or (position > list['size'])):
            return False
        if (position == 0):
            insert_at_beginning(list, data)
            return True
        new_node = create_node(data)
        current = list['head']
        i = 0
        while (i < (position - 1)):
            current = current['next']
            i = (i + 1)
        new_node['next'] = current['next']
        current['next'] = new_node
        list['size'] = (list['size'] + 1)
        return True
    def delete_at_position(list, position):
        if (((position < 0) or (position >= list['size'])) or (list['head'] == None)):
            return None
        if (position == 0):
            deleted_data = list['head']['data']
            list['head'] = list['head']['next']
            list['size'] = (list['size'] - 1)
            return deleted_data
        current = list['head']
        i = 0
        while (i < (position - 1)):
            current = current['next']
            i = (i + 1)
        if (current['next'] == None):
            return None
        deleted_data = current['next']['data']
        current['next'] = current['next']['next']
        list['size'] = (list['size'] - 1)
        return deleted_data
    def search(list, data):
        current = list['head']
        position = 0
        while (current != None):
            if (current['data'] == data):
                return position
            current = current['next']
            position = (position + 1)
        return 1
    def to_array(list):
        result = []
        current = list['head']
        index = 0
        while (current != None):
            result[index] = current['data']
            current = current['next']
            index = (index + 1)
        return result
    list = create_linked_list()
    print('Testing linked list operations:')
    insert_at_beginning(list, 30)
    insert_at_beginning(list, 20)
    insert_at_beginning(list, 10)
    print((str('After inserting 30, 20, 10 at beginning: ') + str(to_array(list))))
    insert_at_end(list, 40)
    insert_at_end(list, 50)
    print((str('After inserting 40, 50 at end: ') + str(to_array(list))))
    insert_at_position(list, 2, 25)
    print((str('After inserting 25 at position 2: ') + str(to_array(list))))
    search_result1 = search(list, 25)
    search_result2 = search(list, 100)
    print((str('Search for 25: position ') + str(search_result1)))
    print((str('Search for 100: position ') + str(search_result2)))
    deleted = delete_at_position(list, 1)
    print((str('Deleted element at position 1: ') + str(deleted)))
    print((str('List after deletion: ') + str(to_array(list))))
    return {'linked_list_tested': True, 'final_list': to_array(list), 'operations': ['insert_beginning', 'insert_end', 'insert_position', 'delete', 'search']}

def binary_search_tree_implementation():
    print('\\n=== Binary Search Tree Implementation ===')
    def create_bst_node(data):
        return {'data': data, 'left': None, 'right': None}
    def create_bst():
        return {'root': None, 'size': 0}
    def insert_bst(bst, data):
        bst['root'] = insert_node(bst['root'], data)
        bst['size'] = (bst['size'] + 1)
    def insert_node(node, data):
        if (node == None):
            return create_bst_node(data)
        if (data < node['data']):
            node['left'] = insert_node(node['left'], data)
        elif (data > node['data']):
            node['right'] = insert_node(node['right'], data)
        return node
    def search_bst(bst, data):
        return search_node(bst['root'], data)
    def search_node(node, data):
        if ((node == None) or (node['data'] == data)):
            return (node != None)
        if (data < node['data']):
            return search_node(node['left'], data)
        else:
            return search_node(node['right'], data)
    def inorder_traversal(bst):
        result = []
        inorder_helper(bst['root'], result)
        return result
    def inorder_helper(node, result):
        if (node != None):
            inorder_helper(node['left'], result)
            result[result['length']()] = node['data']
            inorder_helper(node['right'], result)
    def preorder_traversal(bst):
        result = []
        preorder_helper(bst['root'], result)
        return result
    def preorder_helper(node, result):
        if (node != None):
            result[result['length']()] = node['data']
            preorder_helper(node['left'], result)
            preorder_helper(node['right'], result)
    def postorder_traversal(bst):
        result = []
        postorder_helper(bst['root'], result)
        return result
    def postorder_helper(node, result):
        if (node != None):
            postorder_helper(node['left'], result)
            postorder_helper(node['right'], result)
            result[result['length']()] = node['data']
    def find_min(bst):
        if (bst['root'] == None):
            return None
        node = bst['root']
        while (node['left'] != None):
            node = node['left']
        return node['data']
    def find_max(bst):
        if (bst['root'] == None):
            return None
        node = bst['root']
        while (node['right'] != None):
            node = node['right']
        return node['data']
    bst = create_bst()
    print('Testing Binary Search Tree operations:')
    values_to_insert = [50, 30, 70, 20, 40, 60, 80, 10, 35, 65]
    i = 0
    while (i < values_to_insert['length']()):
        insert_bst(bst, values_to_insert[i])
        i = (i + 1)
    print((str('Inserted values: ') + str(values_to_insert)))
    print((str('BST size: ') + str(bst['size'])))
    inorder_result = inorder_traversal(bst)
    preorder_result = preorder_traversal(bst)
    postorder_result = postorder_traversal(bst)
    print((str('Inorder traversal (sorted): ') + str(inorder_result)))
    print((str('Preorder traversal: ') + str(preorder_result)))
    print((str('Postorder traversal: ') + str(postorder_result)))
    search_values = [35, 25, 80, 90]
    print('Search results:')
    j = 0
    while (j < search_values['length']()):
        value = search_values[j]
        found = search_bst(bst, value)
        print((str((str((str('  ') + str(value))) + str(': '))) + str('found' if found else 'not found')))
        j = (j + 1)
    min_value = find_min(bst)
    max_value = find_max(bst)
    print((str('Minimum value: ') + str(min_value)))
    print((str('Maximum value: ') + str(max_value)))
    return {'bst_tested': True, 'inserted_values': values_to_insert, 'inorder_result': inorder_result, 'min_value': min_value, 'max_value': max_value}

def hash_table_implementation():
    print('\\n=== Hash Table Implementation ===')
    def create_hash_table(size):
        table = {'buckets': [], 'size': size, 'count': 0}
        i = 0
        while (i < size):
            table['buckets'][i] = []
            i = (i + 1)
        return table
    def hash_function(key, table_size):
        hash = 0
        i = 0
        while (i < ml_string.length(key)):
            char_code = ml_string.char_code_at(key, i)
            hash = (((hash * 31) + char_code) % table_size)
            i = (i + 1)
        return (hash + table_size) if (hash < 0) else hash
    def put(table, key, value):
        index = hash_function(key, table['size'])
        bucket = table['buckets'][index]
        i = 0
        while (i < bucket['length']()):
            if (bucket[i]['key'] == key):
                bucket[i]['value'] = value
                return
            i = (i + 1)
        bucket[bucket['length']()] = {'key': key, 'value': value}
        table['count'] = (table['count'] + 1)
    def get(table, key):
        index = hash_function(key, table['size'])
        bucket = table['buckets'][index]
        i = 0
        while (i < bucket['length']()):
            if (bucket[i]['key'] == key):
                return bucket[i]['value']
            i = (i + 1)
        return None
    def remove(table, key):
        index = hash_function(key, table['size'])
        bucket = table['buckets'][index]
        i = 0
        while (i < bucket['length']()):
            if (bucket[i]['key'] == key):
                j = i
                while (j < (bucket['length']() - 1)):
                    bucket[j] = bucket[(j + 1)]
                    j = (j + 1)
                bucket['resize']((bucket['length']() - 1))
                table['count'] = (table['count'] - 1)
                return True
            i = (i + 1)
        return False
    def contains_key(table, key):
        return (get(table, key) != None)
    def get_all_keys(table):
        keys = []
        i = 0
        while (i < table['size']):
            bucket = table['buckets'][i]
            j = 0
            while (j < bucket['length']()):
                keys[keys['length']()] = bucket[j]['key']
                j = (j + 1)
            i = (i + 1)
        return keys
    hash_table = create_hash_table(10)
    print('Testing Hash Table operations:')
    put(hash_table, 'name', 'John Doe')
    put(hash_table, 'age', '30')
    put(hash_table, 'city', 'New York')
    put(hash_table, 'occupation', 'Engineer')
    put(hash_table, 'email', 'john@example.com')
    print('Added 5 key-value pairs')
    print((str('Hash table count: ') + str(hash_table['count'])))
    print('Retrieving values:')
    print((str('  name: ') + str(get(hash_table, 'name'))))
    print((str('  age: ') + str(get(hash_table, 'age'))))
    print((str('  city: ') + str(get(hash_table, 'city'))))
    print((str('  missing_key: ') + str(get(hash_table, 'missing_key'))))
    print('Key existence checks:')
    print((str("  Contains 'email': ") + str(contains_key(hash_table, 'email'))))
    print((str("  Contains 'phone': ") + str(contains_key(hash_table, 'phone'))))
    all_keys = get_all_keys(hash_table)
    print((str('All keys: ') + str(all_keys)))
    put(hash_table, 'age', '31')
    print((str('Updated age to 31: ') + str(get(hash_table, 'age'))))
    removed = remove(hash_table, 'city')
    print((str("Removed 'city': ") + str(removed)))
    print((str('Hash table count after removal: ') + str(hash_table['count'])))
    print((str('City value after removal: ') + str(get(hash_table, 'city'))))
    return {'hash_table_tested': True, 'final_count': hash_table['count'], 'all_keys': all_keys, 'operations': ['put', 'get', 'remove', 'contains_key', 'get_all_keys']}

def priority_queue_implementation():
    print('\\n=== Priority Queue (Heap) Implementation ===')
    def create_min_heap():
        return {'items': [], 'size': 0}
    def parent_index(i):
        return Math['floor'](((i - 1) / 2))
    def left_child_index(i):
        return ((2 * i) + 1)
    def right_child_index(i):
        return ((2 * i) + 2)
    def swap(heap, i, j):
        temp = heap['items'][i]
        heap['items'][i] = heap['items'][j]
        heap['items'][j] = temp
    def heapify_up(heap, index):
        if (index == 0):
            return
        parent_idx = parent_index(index)
        if (heap['items'][index] < heap['items'][parent_idx]):
            swap(heap, index, parent_idx)
            heapify_up(heap, parent_idx)
    def heapify_down(heap, index):
        smallest = index
        left = left_child_index(index)
        right = right_child_index(index)
        if ((left < heap['size']) and (heap['items'][left] < heap['items'][smallest])):
            smallest = left
        if ((right < heap['size']) and (heap['items'][right] < heap['items'][smallest])):
            smallest = right
        if (smallest != index):
            swap(heap, index, smallest)
            heapify_down(heap, smallest)
    def insert_heap(heap, value):
        heap['items'][heap['size']] = value
        heap['size'] = (heap['size'] + 1)
        heapify_up(heap, (heap['size'] - 1))
    def extract_min(heap):
        if (heap['size'] == 0):
            return None
        min_value = heap['items'][0]
        heap['items'][0] = heap['items'][(heap['size'] - 1)]
        heap['size'] = (heap['size'] - 1)
        if (heap['size'] > 0):
            heapify_down(heap, 0)
        return min_value
    def peek_min(heap):
        return heap['items'][0] if (heap['size'] > 0) else None
    def heap_to_array(heap):
        result = []
        i = 0
        while (i < heap['size']):
            result[i] = heap['items'][i]
            i = (i + 1)
        return result
    Math = {'floor': lambda x: Math['int'](x) if (x >= 0) else (Math['int'](x) - 1), 'int': lambda x: (x - (x % 1)) if (x >= 0) else (x - (x % 1))}
    min_heap = create_min_heap()
    print('Testing Priority Queue (Min-Heap) operations:')
    values_to_insert = [10, 4, 15, 20, 0, 30, 2, 6, 8, 12]
    print((str('Inserting values: ') + str(values_to_insert)))
    k = 0
    while (k < values_to_insert['length']()):
        insert_heap(min_heap, values_to_insert[k])
        print((str((str((str('  After inserting ') + str(values_to_insert[k]))) + str(': heap = '))) + str(heap_to_array(min_heap))))
        k = (k + 1)
    print((str('Final heap structure: ') + str(heap_to_array(min_heap))))
    print((str('Minimum element (peek): ') + str(peek_min(min_heap))))
    print('Extracting minimum elements:')
    extracted = []
    while (min_heap['size'] > 0):
        min_val = extract_min(min_heap)
        extracted[extracted['length']()] = min_val
        print((str((str((str('  Extracted: ') + str(min_val))) + str(', Remaining heap: '))) + str(heap_to_array(min_heap))))
    print((str('All extracted values (should be sorted): ') + str(extracted)))
    return {'priority_queue_tested': True, 'original_values': values_to_insert, 'sorted_extraction': extracted, 'operations': ['insert', 'extract_min', 'peek_min', 'heapify']}

def main():
    print('==============================================')
    print('  COMPREHENSIVE DATA STRUCTURES TEST')
    print('==============================================')
    results = {}
    results['stack'] = stack_implementation()
    results['queue'] = queue_implementation()
    results['linked_list'] = linked_list_implementation()
    results['binary_search_tree'] = binary_search_tree_implementation()
    results['hash_table'] = hash_table_implementation()
    results['priority_queue'] = priority_queue_implementation()
    print('\\n==============================================')
    print('  ALL DATA STRUCTURES TESTS COMPLETED')
    print('==============================================')
    return results

main()

# End of generated code