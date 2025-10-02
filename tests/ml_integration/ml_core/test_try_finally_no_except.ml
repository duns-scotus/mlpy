// Test try/finally without except clause

value = 0;

try {
    value = 10;
} finally {
    value = value + 5;
}

result = value;
