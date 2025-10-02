// Minimal test to isolate finally clause issue

executed = false;

try {
    x = 10;
} finally {
    executed = true;
}

result = executed;
