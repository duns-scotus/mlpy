import collections;
import math;

function testArrayOperations() {
    arr = [1, 2, 3];
    arr = collections.append(arr, 4);

    // Test if contains function works
    if (collections.contains(arr, 2)) {
        print("Contains works");
    }

    return arr;
}

function testConditionals() {
    x = 5;

    if (x < 10) {
        return "small";
    } else if (x < 20) {
        return "medium";
    } else {
        return "large";
    }
}

function testLoops() {
    i = 0;
    result = 0;

    while (i < 5) {
        result = result + i;
        i = i + 1;
    }

    return result;
}

function main() {
    arr = testArrayOperations();
    cond = testConditionals();
    loop_result = testLoops();

    print("Array length: " + collections.length(arr));
    print("Conditional: " + cond);
    print("Loop result: " + loop_result);

    return 0;
}