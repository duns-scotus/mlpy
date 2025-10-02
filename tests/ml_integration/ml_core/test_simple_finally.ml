// Simple finally test
function test() {
    executed = false;

    try {
        x = 10;
    } finally {
        executed = true;
    }

    return executed;
}

x = test();
