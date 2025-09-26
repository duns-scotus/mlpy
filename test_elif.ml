function test() {
    x = 15;

    if (x < 10) {
        return "small";
    } elif (x < 20) {
        return "medium";
    } else {
        return "large";
    }
}

function main() {
    result = test();
    print("Result: " + result);
    return 0;
}