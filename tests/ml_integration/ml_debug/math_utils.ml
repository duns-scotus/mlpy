// Math utilities module for debugging tests
// Tests: function calls, arithmetic, conditionals

function abs(x) {
    if (x < 0) {
        return -x;
    } else {
        return x;
    }
}

function max(a, b) {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}

function min(a, b) {
    if (a < b) {
        return a;
    } else {
        return b;
    }
}

function clamp(value, min_val, max_val) {
    if (value < min_val) {
        return min_val;
    } elif (value > max_val) {
        return max_val;
    } else {
        return value;
    }
}

function is_even(n) {
    remainder = n - (n / 2) * 2;
    return remainder == 0;
}

function is_odd(n) {
    return !is_even(n);
}

function factorial(n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

function fibonacci(n) {
    if (n <= 1) {
        return n;
    } else {
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
}

function sum_range(start, end) {
    total = 0;
    i = start;
    while (i <= end) {
        total = total + i;
        i = i + 1;
    }
    return total;
}

function gcd(a, b) {
    if (b == 0) {
        return a;
    } else {
        remainder = a - (a / b) * b;
        return gcd(b, remainder);
    }
}
