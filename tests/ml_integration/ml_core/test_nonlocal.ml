// Test nonlocal statement

function create_counter(initial) {
    count = initial;

    function increment() {
        nonlocal count;
        count = count + 1;
        return count;
    }

    return increment;
}

counter = create_counter(10);
result1 = counter();
result2 = counter();
result3 = counter();
