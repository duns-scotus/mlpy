function test() {
    items = [1, 2, 3];
    result = items.filter(function(item) {
        distance = item * 2;
        return distance > 3;
    });
    return result;
}