// List operations module for debugging tests
// Tests: array operations, loops, nested structures

function list_length(list) {
    count = 0;
    for (item in list) {
        count = count + 1;
    }
    return count;
}

function list_sum(list) {
    total = 0;
    for (item in list) {
        total = total + item;
    }
    return total;
}

function list_max(list) {
    if (list_length(list) == 0) {
        return 0;
    }

    max_val = list[0];
    for (item in list) {
        if (item > max_val) {
            max_val = item;
        }
    }
    return max_val;
}

function list_min(list) {
    if (list_length(list) == 0) {
        return 0;
    }

    min_val = list[0];
    for (item in list) {
        if (item < min_val) {
            min_val = item;
        }
    }
    return min_val;
}

function list_contains(list, value) {
    for (item in list) {
        if (item == value) {
            return true;
        }
    }
    return false;
}

function list_reverse(list) {
    len = list_length(list);
    result = [];
    i = len - 1;
    while (i >= 0) {
        result = result + [list[i]];
        i = i - 1;
    }
    return result;
}

function list_filter_even(list) {
    result = [];
    for (item in list) {
        remainder = item - (item / 2) * 2;
        if (remainder == 0) {
            result = result + [item];
        }
    }
    return result;
}

function list_map_double(list) {
    result = [];
    for (item in list) {
        result = result + [item * 2];
    }
    return result;
}

function list_slice(list, start, end) {
    result = [];
    i = start;
    while (i < end) {
        if (i >= 0 && i < list_length(list)) {
            result = result + [list[i]];
        }
        i = i + 1;
    }
    return result;
}
