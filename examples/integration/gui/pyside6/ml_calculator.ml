// ML Calculator - Business logic in ML, UI in PySide6
// This demonstrates ML functions used as GUI callbacks

import math;

function add(a, b) {
    return a + b;
}

function subtract(a, b) {
    return a - b;
}

function multiply(a, b) {
    return a * b;
}

function divide(a, b) {
    if (b == 0) {
        return null;  // Division by zero
    }
    return a / b;
}

// More complex calculation with multiple steps
function calculate_compound_interest(principal, rate, years) {
    // Formula: A = P(1 + r)^t
    rate_decimal = rate / 100;
    amount = principal * math.pow(1 + rate_decimal, years);
    interest = amount - principal;

    return {
        amount: amount,
        interest: interest,
        principal: principal,
        rate: rate,
        years: years
    };
}

// Simulate a long-running calculation
function fibonacci(n) {
    if (n <= 1) {
        return n;
    }

    a = 0;
    b = 1;
    i = 2;

    while (i <= n) {
        temp = a + b;
        a = b;
        b = temp;
        i = i + 1;
    }

    return b;
}

// Array processing example
function calculate_statistics(numbers) {
    if (len(numbers) == 0) {
        return null;
    }

    // Calculate sum
    sum = 0;
    i = 0;
    while (i < len(numbers)) {
        sum = sum + numbers[i];
        i = i + 1;
    }

    // Calculate mean
    mean = sum / len(numbers);

    // Find min and max
    min_val = numbers[0];
    max_val = numbers[0];
    i = 1;
    while (i < len(numbers)) {
        if (numbers[i] < min_val) {
            min_val = numbers[i];
        }
        if (numbers[i] > max_val) {
            max_val = numbers[i];
        }
        i = i + 1;
    }

    return {
        count: len(numbers),
        sum: sum,
        mean: mean,
        min: min_val,
        max: max_val
    };
}
