// Binary tree operations for debugging tests
// Tests: object structures, recursion, complex data

function create_node(value, left, right) {
    node = {};
    node.value = value;
    node.left = left;
    node.right = right;
    return node;
}

function create_leaf(value) {
    return create_node(value, {}, {});
}

function is_empty_node(node) {
    // Check if node is empty object
    return node.value == null || node.value == 0;
}

function tree_size(node) {
    if (is_empty_node(node)) {
        return 0;
    }

    left_size = tree_size(node.left);
    right_size = tree_size(node.right);
    return 1 + left_size + right_size;
}

function tree_height(node) {
    if (is_empty_node(node)) {
        return 0;
    }

    left_height = tree_height(node.left);
    right_height = tree_height(node.right);

    if (left_height > right_height) {
        return 1 + left_height;
    } else {
        return 1 + right_height;
    }
}

function tree_sum(node) {
    if (is_empty_node(node)) {
        return 0;
    }

    left_sum = tree_sum(node.left);
    right_sum = tree_sum(node.right);
    return node.value + left_sum + right_sum;
}

function tree_contains(node, target) {
    if (is_empty_node(node)) {
        return false;
    }

    if (node.value == target) {
        return true;
    }

    found_left = tree_contains(node.left, target);
    if (found_left) {
        return true;
    }

    return tree_contains(node.right, target);
}

function tree_max(node) {
    if (is_empty_node(node)) {
        return 0;
    }

    max_val = node.value;

    left_max = tree_max(node.left);
    if (left_max > max_val) {
        max_val = left_max;
    }

    right_max = tree_max(node.right);
    if (right_max > max_val) {
        max_val = right_max;
    }

    return max_val;
}
