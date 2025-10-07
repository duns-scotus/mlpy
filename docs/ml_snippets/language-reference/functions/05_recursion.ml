// ============================================
// Example: Recursive Functions
// Category: language-reference/functions
// Demonstrates: Recursion patterns, base cases, recursive algorithms
// ============================================

import console;

console.log("=== Recursive Functions ===\n");

// Example 1: Factorial
console.log("Example 1: Factorial");
function factorial(n) {
    if (n <= 1) {
        return 1;  // Base case
    } else {
        return n * factorial(n - 1);  // Recursive case
    }
}

console.log("factorial(5) = " + str(factorial(5)));      // 120
console.log("factorial(0) = " + str(factorial(0)));      // 1
console.log("factorial(7) = " + str(factorial(7)));      // 5040

// Example 2: Fibonacci sequence
console.log("\nExample 2: Fibonacci");
function fibonacci(n) {
    if (n <= 1) {
        return n;
    } else {
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
}

console.log("Fibonacci sequence (first 10):");
for (i in range(10)) {
    console.log("  fib(" + str(i) + ") = " + str(fibonacci(i)));
}

// Example 3: Sum of array using recursion
console.log("\nExample 3: Recursive array sum");
function sumArrayRecursive(arr, index) {
    if (index >= len(arr)) {
        return 0;  // Base case: end of array
    } else {
        return arr[index] + sumArrayRecursive(arr, index + 1);
    }
}

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
total = sumArrayRecursive(numbers, 0);
console.log("Sum of " + str(numbers) + " = " + str(total));

// Example 4: Power function using recursion
console.log("\nExample 4: Power calculation");
function power(base, exponent) {
    if (exponent == 0) {
        return 1;
    } elif (exponent < 0) {
        return 1 / power(base, -exponent);
    } else {
        return base * power(base, exponent - 1);
    }
}

console.log("2^5 = " + str(power(2, 5)));              // 32
console.log("3^4 = " + str(power(3, 4)));              // 81
console.log("5^0 = " + str(power(5, 0)));              // 1

// Example 5: Counting digits
console.log("\nExample 5: Count digits recursively");
function countDigits(n) {
    absN = n;
    if (n < 0) {
        absN = -n;
    }

    if (absN < 10) {
        return 1;
    } else {
        return 1 + countDigits(absN // 10);
    }
}

console.log("Digits in 12345: " + str(countDigits(12345)));
console.log("Digits in 999: " + str(countDigits(999)));
console.log("Digits in 7: " + str(countDigits(7)));

// Example 6: Find maximum in array recursively
console.log("\nExample 6: Find maximum recursively");
function findMax(arr, index, currentMax) {
    if (index >= len(arr)) {
        return currentMax;
    }

    newMax = currentMax;
    if (arr[index] > currentMax) {
        newMax = arr[index];
    }

    return findMax(arr, index + 1, newMax);
}

values = [3, 7, 2, 9, 1, 5, 8];
maxValue = findMax(values, 0, values[0]);
console.log("Maximum in " + str(values) + " = " + str(maxValue));

// Example 7: String reversal using recursion
console.log("\nExample 7: Reverse string recursively");
function reverseString(text, index) {
    if (index >= len(text)) {
        return "";
    } else {
        return reverseString(text, index + 1) + text[index];
    }
}

original = "Hello";
reversed = reverseString(original, 0);
console.log("Original: " + original);
console.log("Reversed: " + reversed);

// Example 8: Greatest Common Divisor (Euclidean algorithm)
console.log("\nExample 8: GCD using recursion");
function gcd(a, b) {
    if (b == 0) {
        return a;
    } else {
        return gcd(b, a % b);
    }
}

console.log("gcd(48, 18) = " + str(gcd(48, 18)));      // 6
console.log("gcd(100, 35) = " + str(gcd(100, 35)));    // 5
console.log("gcd(17, 13) = " + str(gcd(17, 13)));      // 1

// Example 9: Palindrome check using recursion
console.log("\nExample 9: Palindrome check");
function isPalindrome(text, left, right) {
    if (left >= right) {
        return true;
    }

    if (text[left] != text[right]) {
        return false;
    }

    return isPalindrome(text, left + 1, right - 1);
}

words = ["radar", "hello", "level", "world", "noon"];
for (word in words) {
    isPalin = isPalindrome(word, 0, len(word) - 1);
    console.log(word + " is palindrome: " + str(isPalin));
}

// Example 10: Binary search (recursive)
console.log("\nExample 10: Binary search");
function binarySearch(arr, target, left, right) {
    if (left > right) {
        return -1;  // Not found
    }

    mid = (left + right) // 2;

    if (arr[mid] == target) {
        return mid;
    } elif (arr[mid] > target) {
        return binarySearch(arr, target, left, mid - 1);
    } else {
        return binarySearch(arr, target, mid + 1, right);
    }
}

sortedArray = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19];
console.log("Searching in: " + str(sortedArray));
console.log("Index of 7: " + str(binarySearch(sortedArray, 7, 0, len(sortedArray) - 1)));
console.log("Index of 15: " + str(binarySearch(sortedArray, 15, 0, len(sortedArray) - 1)));
console.log("Index of 20: " + str(binarySearch(sortedArray, 20, 0, len(sortedArray) - 1)));

console.log("\n=== Recursion Complete ===");
