// Comprehensive Data Structures Test - Rewritten with Working Patterns
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

// Utility function for array to string conversion
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

// Stack implementation and operations
function stack_implementation() {
    print("=== Stack Implementation and Operations ===");

    // Stack using array
    function create_stack() {
        return {
            items: array.fill(100, null),  // Pre-allocate space
            top: -1,
            max_size: 100
        };
    }

    function push(stack, item) {
        if (stack.top < stack.max_size - 1) {
            stack.top = stack.top + 1;
            stack.items[stack.top] = item;
            return true;
        }
        return false;
    }

    function pop(stack) {
        if (stack.top == -1) {
            return null;
        }
        item = stack.items[stack.top];
        stack.items[stack.top] = null;
        stack.top = stack.top - 1;
        return item;
    }

    function peek(stack) {
        if (stack.top == -1) {
            return null;
        }
        return stack.items[stack.top];
    }

    function is_empty(stack) {
        return stack.top == -1;
    }

    function stack_size(stack) {
        return stack.top + 1;
    }

    // Test stack operations
    stack = create_stack();

    print("Testing stack operations:");
    print("Initial stack empty: " + string.toString(is_empty(stack)));

    // Push operations
    push(stack, 10);
    push(stack, 20);
    push(stack, 30);
    push(stack, 40);

    print("After pushing 10, 20, 30, 40:");
    print("  Stack size: " + string.toString(stack_size(stack)));
    print("  Top element: " + string.toString(peek(stack)));

    // Pop operations
    print("Popping elements:");
    while (!is_empty(stack)) {
        element = pop(stack);
        print("  Popped: " + string.toString(element) + ", Remaining size: " + string.toString(stack_size(stack)));
    }

    return {
        stack_tested: true,
        operations: ["push", "pop", "peek", "is_empty", "size"]
    };
}

// Queue implementation and operations
function queue_implementation() {
    print("\n=== Queue Implementation and Operations ===");

    // Queue using array with front and rear pointers
    function create_queue() {
        return {
            items: array.fill(100, null),  // Pre-allocate space
            front: 0,
            rear: -1,
            count: 0,
            max_size: 100
        };
    }

    function enqueue(queue, item) {
        if (queue.count < queue.max_size) {
            queue.rear = queue.rear + 1;
            queue.items[queue.rear] = item;
            queue.count = queue.count + 1;
            return true;
        }
        return false;
    }

    function dequeue(queue) {
        if (queue.count == 0) {
            return null;
        }
        item = queue.items[queue.front];
        queue.items[queue.front] = null;
        queue.front = queue.front + 1;
        queue.count = queue.count - 1;
        return item;
    }

    function queue_front(queue) {
        if (queue.count == 0) {
            return null;
        }
        return queue.items[queue.front];
    }

    function queue_is_empty(queue) {
        return queue.count == 0;
    }

    function queue_size(queue) {
        return queue.count;
    }

    // Test queue operations
    queue = create_queue();

    print("Testing queue operations:");
    print("Initial queue empty: " + string.toString(queue_is_empty(queue)));

    // Enqueue operations
    enqueue(queue, "A");
    enqueue(queue, "B");
    enqueue(queue, "C");
    enqueue(queue, "D");

    print("After enqueuing A, B, C, D:");
    print("  Queue size: " + string.toString(queue_size(queue)));
    print("  Front element: " + string.toString(queue_front(queue)));

    // Dequeue operations
    print("Dequeuing elements:");
    while (!queue_is_empty(queue)) {
        element = dequeue(queue);
        print("  Dequeued: " + string.toString(element) + ", Remaining size: " + string.toString(queue_size(queue)));
    }

    return {
        queue_tested: true,
        operations: ["enqueue", "dequeue", "front", "is_empty", "size"]
    };
}

// Linked list implementation
function linked_list_implementation() {
    print("\n=== Linked List Implementation ===");

    // Node structure
    function create_node(data) {
        return {
            data: data,
            next: null
        };
    }

    // Linked list structure
    function create_linked_list() {
        return {
            head: null,
            size: 0
        };
    }

    function insert_at_beginning(list, data) {
        new_node = create_node(data);
        new_node.next = list.head;
        list.head = new_node;
        list.size = list.size + 1;
    }

    function insert_at_end(list, data) {
        new_node = create_node(data);

        if (list.head == null) {
            list.head = new_node;
        } else {
            current = list.head;
            while (current.next != null) {
                current = current.next;
            }
            current.next = new_node;
        }
        list.size = list.size + 1;
    }

    function insert_at_position(list, position, data) {
        if (position < 0 || position > list.size) {
            return false;
        }

        if (position == 0) {
            insert_at_beginning(list, data);
            return true;
        }

        new_node = create_node(data);
        current = list.head;
        i = 0;
        while (i < position - 1) {
            current = current.next;
            i = i + 1;
        }

        new_node.next = current.next;
        current.next = new_node;
        list.size = list.size + 1;
        return true;
    }

    function delete_at_position(list, position) {
        if (position < 0 || position >= list.size || list.head == null) {
            return null;
        }

        if (position == 0) {
            deleted_data = list.head.data;
            list.head = list.head.next;
            list.size = list.size - 1;
            return deleted_data;
        }

        current = list.head;
        i = 0;
        while (i < position - 1) {
            current = current.next;
            i = i + 1;
        }

        if (current.next == null) {
            return null;
        }

        deleted_data = current.next.data;
        current.next = current.next.next;
        list.size = list.size - 1;
        return deleted_data;
    }

    function search(list, data) {
        current = list.head;
        position = 0;

        while (current != null) {
            if (current.data == data) {
                return position;
            }
            current = current.next;
            position = position + 1;
        }

        return -1;
    }

    function to_array(list) {
        result = array.fill(list.size, null);
        current = list.head;
        index = 0;

        while (current != null && index < list.size) {
            result[index] = current.data;
            current = current.next;
            index = index + 1;
        }

        return result;
    }

    // Test linked list operations
    list = create_linked_list();

    print("Testing linked list operations:");

    // Insert at beginning
    insert_at_beginning(list, 30);
    insert_at_beginning(list, 20);
    insert_at_beginning(list, 10);
    print("After inserting 30, 20, 10 at beginning: " + array_to_string(to_array(list)));

    // Insert at end
    insert_at_end(list, 40);
    insert_at_end(list, 50);
    print("After inserting 40, 50 at end: " + array_to_string(to_array(list)));

    // Insert at position
    insert_at_position(list, 2, 25);
    print("After inserting 25 at position 2: " + array_to_string(to_array(list)));

    // Search operations
    search_result1 = search(list, 25);
    search_result2 = search(list, 100);
    print("Search for 25: position " + string.toString(search_result1));
    print("Search for 100: position " + string.toString(search_result2));

    // Delete operations
    deleted = delete_at_position(list, 1);
    print("Deleted element at position 1: " + string.toString(deleted));
    print("List after deletion: " + array_to_string(to_array(list)));

    return {
        linked_list_tested: true,
        final_list: to_array(list),
        operations: ["insert_beginning", "insert_end", "insert_position", "delete", "search"]
    };
}

// Binary Search Tree implementation
function binary_search_tree_implementation() {
    print("\n=== Binary Search Tree Implementation ===");

    // BST Node structure
    function create_bst_node(data) {
        return {
            data: data,
            left: null,
            right: null
        };
    }

    // BST structure
    function create_bst() {
        return {
            root: null,
            size: 0
        };
    }

    function insert_bst(bst, data) {
        bst.root = insert_node(bst.root, data);
        bst.size = bst.size + 1;
    }

    function insert_node(node, data) {
        if (node == null) {
            return create_bst_node(data);
        }

        if (data < node.data) {
            node.left = insert_node(node.left, data);
        } elif (data > node.data) {
            node.right = insert_node(node.right, data);
        }

        return node;
    }

    function search_bst(bst, data) {
        return search_node(bst.root, data);
    }

    function search_node(node, data) {
        if (node == null || node.data == data) {
            return node != null;
        }

        if (data < node.data) {
            return search_node(node.left, data);
        } else {
            return search_node(node.right, data);
        }
    }

    function inorder_traversal(bst) {
        result = [];
        inorder_helper(bst.root, result);
        return result;
    }

    function inorder_helper(node, result) {
        if (node != null) {
            inorder_helper(node.left, result);
            result = safe_append(result, node.data);
            inorder_helper(node.right, result);
        }
    }

    function preorder_traversal(bst) {
        result = [];
        preorder_helper(bst.root, result);
        return result;
    }

    function preorder_helper(node, result) {
        if (node != null) {
            result = safe_append(result, node.data);
            preorder_helper(node.left, result);
            preorder_helper(node.right, result);
        }
    }

    function postorder_traversal(bst) {
        result = [];
        postorder_helper(bst.root, result);
        return result;
    }

    function postorder_helper(node, result) {
        if (node != null) {
            postorder_helper(node.left, result);
            postorder_helper(node.right, result);
            result = safe_append(result, node.data);
        }
    }

    function find_min(bst) {
        if (bst.root == null) {
            return null;
        }
        node = bst.root;
        while (node.left != null) {
            node = node.left;
        }
        return node.data;
    }

    function find_max(bst) {
        if (bst.root == null) {
            return null;
        }
        node = bst.root;
        while (node.right != null) {
            node = node.right;
        }
        return node.data;
    }

    // Test BST operations
    bst = create_bst();

    print("Testing Binary Search Tree operations:");

    // Insert operations
    values_to_insert = [50, 30, 70, 20, 40, 60, 80, 10, 35, 65];
    i = 0;
    while (i < values_to_insert.length) {
        insert_bst(bst, values_to_insert[i]);
        i = i + 1;
    }

    print("Inserted values: " + array_to_string(values_to_insert));
    print("BST size: " + string.toString(bst.size));

    // Traversal operations
    inorder_result = inorder_traversal(bst);
    preorder_result = preorder_traversal(bst);
    postorder_result = postorder_traversal(bst);

    print("Inorder traversal (sorted): " + array_to_string(inorder_result));
    print("Preorder traversal: " + array_to_string(preorder_result));
    print("Postorder traversal: " + array_to_string(postorder_result));

    // Search operations
    search_values = [35, 25, 80, 90];
    print("Search results:");
    j = 0;
    while (j < search_values.length) {
        value = search_values[j];
        found = search_bst(bst, value);
        print("  " + string.toString(value) + ": " + (found ? "found" : "not found"));
        j = j + 1;
    }

    // Min and Max
    min_value = find_min(bst);
    max_value = find_max(bst);
    print("Minimum value: " + string.toString(min_value));
    print("Maximum value: " + string.toString(max_value));

    return {
        bst_tested: true,
        inserted_values: values_to_insert,
        inorder_result: inorder_result,
        min_value: min_value,
        max_value: max_value
    };
}

// Hash table implementation
function hash_table_implementation() {
    print("\n=== Hash Table Implementation ===");

    // Hash table with chaining for collision resolution
    function create_hash_table(size) {
        table = {
            buckets: array.fill(size, null),
            size: size,
            count: 0
        };

        i = 0;
        while (i < size) {
            table.buckets[i] = [];
            i = i + 1;
        }

        return table;
    }

    function hash_function(key, table_size) {
        hash = 0;
        i = 0;
        while (i < string.length(key)) {
            char_code = string.char_code_at(key, i);
            hash = (hash * 31 + char_code) % table_size;
            i = i + 1;
        }
        return hash < 0 ? hash + table_size : hash;
    }

    function put(table, key, value) {
        index = hash_function(key, table.size);
        bucket = table.buckets[index];

        // Check if key already exists
        i = 0;
        while (i < bucket.length) {
            if (bucket[i].key == key) {
                bucket[i].value = value; // Update existing
                return;
            }
            i = i + 1;
        }

        // Add new key-value pair using safe append
        new_entry = {key: key, value: value};
        table.buckets[index] = safe_append(bucket, new_entry);
        table.count = table.count + 1;
    }

    function get(table, key) {
        index = hash_function(key, table.size);
        bucket = table.buckets[index];

        i = 0;
        while (i < bucket.length) {
            if (bucket[i].key == key) {
                return bucket[i].value;
            }
            i = i + 1;
        }

        return null; // Key not found
    }

    function remove(table, key) {
        index = hash_function(key, table.size);
        bucket = table.buckets[index];

        i = 0;
        while (i < bucket.length) {
            if (bucket[i].key == key) {
                // Create new bucket without the removed item
                new_bucket = array.fill(bucket.length - 1, null);
                new_index = 0;
                j = 0;
                while (j < bucket.length) {
                    if (j != i) {
                        new_bucket[new_index] = bucket[j];
                        new_index = new_index + 1;
                    }
                    j = j + 1;
                }
                table.buckets[index] = new_bucket;
                table.count = table.count - 1;
                return true;
            }
            i = i + 1;
        }

        return false; // Key not found
    }

    function contains_key(table, key) {
        return get(table, key) != null;
    }

    function get_all_keys(table) {
        keys = [];
        i = 0;
        while (i < table.size) {
            bucket = table.buckets[i];
            j = 0;
            while (j < bucket.length) {
                keys = safe_append(keys, bucket[j].key);
                j = j + 1;
            }
            i = i + 1;
        }
        return keys;
    }

    // Test hash table operations
    hash_table = create_hash_table(10);

    print("Testing Hash Table operations:");

    // Put operations
    put(hash_table, "name", "John Doe");
    put(hash_table, "age", "30");
    put(hash_table, "city", "New York");
    put(hash_table, "occupation", "Engineer");
    put(hash_table, "email", "john@example.com");

    print("Added 5 key-value pairs");
    print("Hash table count: " + string.toString(hash_table.count));

    // Get operations
    print("Retrieving values:");
    print("  name: " + string.toString(get(hash_table, "name")));
    print("  age: " + string.toString(get(hash_table, "age")));
    print("  city: " + string.toString(get(hash_table, "city")));
    print("  missing_key: " + string.toString(get(hash_table, "missing_key")));

    // Contains key check
    print("Key existence checks:");
    print("  Contains 'email': " + string.toString(contains_key(hash_table, "email")));
    print("  Contains 'phone': " + string.toString(contains_key(hash_table, "phone")));

    // Get all keys
    all_keys = get_all_keys(hash_table);
    print("All keys: " + array_to_string(all_keys));

    // Update existing key
    put(hash_table, "age", "31");
    print("Updated age to 31: " + string.toString(get(hash_table, "age")));

    // Remove operation
    removed = remove(hash_table, "city");
    print("Removed 'city': " + string.toString(removed));
    print("Hash table count after removal: " + string.toString(hash_table.count));
    print("City value after removal: " + string.toString(get(hash_table, "city")));

    return {
        hash_table_tested: true,
        final_count: hash_table.count,
        all_keys: all_keys,
        operations: ["put", "get", "remove", "contains_key", "get_all_keys"]
    };
}

// Priority Queue (Heap) implementation
function priority_queue_implementation() {
    print("\n=== Priority Queue (Heap) Implementation ===");

    // Min-heap implementation
    function create_min_heap() {
        return {
            items: array.fill(100, null),  // Pre-allocate space
            size: 0
        };
    }

    function parent_index(i) {
        return math.floor((i - 1) / 2);
    }

    function left_child_index(i) {
        return 2 * i + 1;
    }

    function right_child_index(i) {
        return 2 * i + 2;
    }

    function swap(heap, i, j) {
        temp = heap.items[i];
        heap.items[i] = heap.items[j];
        heap.items[j] = temp;
    }

    function heapify_up(heap, index) {
        if (index == 0) {
            return;
        }

        parent_idx = parent_index(index);
        if (heap.items[index] < heap.items[parent_idx]) {
            swap(heap, index, parent_idx);
            heapify_up(heap, parent_idx);
        }
    }

    function heapify_down(heap, index) {
        smallest = index;
        left = left_child_index(index);
        right = right_child_index(index);

        if (left < heap.size && heap.items[left] < heap.items[smallest]) {
            smallest = left;
        }

        if (right < heap.size && heap.items[right] < heap.items[smallest]) {
            smallest = right;
        }

        if (smallest != index) {
            swap(heap, index, smallest);
            heapify_down(heap, smallest);
        }
    }

    function insert_heap(heap, value) {
        if (heap.size < 100) {  // Check bounds
            heap.items[heap.size] = value;
            heap.size = heap.size + 1;
            heapify_up(heap, heap.size - 1);
            return true;
        }
        return false;
    }

    function extract_min(heap) {
        if (heap.size == 0) {
            return null;
        }

        min_value = heap.items[0];
        heap.items[0] = heap.items[heap.size - 1];
        heap.items[heap.size - 1] = null;
        heap.size = heap.size - 1;

        if (heap.size > 0) {
            heapify_down(heap, 0);
        }

        return min_value;
    }

    function peek_min(heap) {
        return heap.size > 0 ? heap.items[0] : null;
    }

    function heap_to_array(heap) {
        result = array.fill(heap.size, null);
        i = 0;
        while (i < heap.size) {
            result[i] = heap.items[i];
            i = i + 1;
        }
        return result;
    }

    // Test priority queue operations
    min_heap = create_min_heap();

    print("Testing Priority Queue (Min-Heap) operations:");

    // Insert operations
    values_to_insert = [10, 4, 15, 20, 0, 30, 2, 6, 8, 12];
    print("Inserting values: " + array_to_string(values_to_insert));

    k = 0;
    while (k < values_to_insert.length) {
        insert_heap(min_heap, values_to_insert[k]);
        print("  After inserting " + string.toString(values_to_insert[k]) + ": heap = " + array_to_string(heap_to_array(min_heap)));
        k = k + 1;
    }

    print("Final heap structure: " + array_to_string(heap_to_array(min_heap)));
    print("Minimum element (peek): " + string.toString(peek_min(min_heap)));

    // Extract min operations
    print("Extracting minimum elements:");
    extracted = [];
    while (min_heap.size > 0) {
        min_val = extract_min(min_heap);
        extracted = safe_append(extracted, min_val);
        print("  Extracted: " + string.toString(min_val) + ", Remaining heap: " + array_to_string(heap_to_array(min_heap)));
    }

    print("All extracted values (should be sorted): " + array_to_string(extracted));

    return {
        priority_queue_tested: true,
        original_values: values_to_insert,
        sorted_extraction: extracted,
        operations: ["insert", "extract_min", "peek_min", "heapify"]
    };
}

// Main function to run all data structure tests
function main() {
    print("==============================================");
    print("  COMPREHENSIVE DATA STRUCTURES TEST");
    print("==============================================");

    results = {
        stack: null,
        queue: null,
        linked_list: null,
        binary_search_tree: null,
        hash_table: null,
        priority_queue: null
    };

    results.stack = stack_implementation();
    results.queue = queue_implementation();
    results.linked_list = linked_list_implementation();
    results.binary_search_tree = binary_search_tree_implementation();
    results.hash_table = hash_table_implementation();
    results.priority_queue = priority_queue_implementation();

    print("\n==============================================");
    print("  ALL DATA STRUCTURES TESTS COMPLETED");
    print("==============================================");

    return results;
}

// Execute comprehensive data structures test
main();