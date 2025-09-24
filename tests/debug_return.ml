// Minimal test case for return statement placement bug
function testReturn(x) {
    if (x > 5) {
        value = x * 2;
        return value;
    } else {
        return x + 1;
    }
}