import collections;

function test() {
    arr = [1, 2, 3];

    // Test the contains function specifically
    result = collections.contains(arr, 2);

    return result;
}

function main() {
    result = test();
    print("Contains result: " + result);
    return 0;
}