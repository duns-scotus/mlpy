// Test finally with return value

function test_finally_with_return() {
    value = 0;

    try {
        value = 10;
        return value;
    } finally {
        value = 20;
    }

    return value;
}

result = test_finally_with_return();
