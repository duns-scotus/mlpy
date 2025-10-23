// ============================================
// Example: Operators and Expressions
// Category: tutorial
// Demonstrates: Arithmetic, comparison, and logical operators
// ============================================

import console;

// Arithmetic operators
a = 15;
b = 4;

console.log("=== Arithmetic Operators ===");
console.log(str(a) + " + " + str(b) + " = " + str(a + b));
console.log(str(a) + " - " + str(b) + " = " + str(a - b));
console.log(str(a) + " * " + str(b) + " = " + str(a * b));
console.log(str(a) + " / " + str(b) + " = " + str(a / b));
console.log(str(a) + " % " + str(b) + " = " + str(a % b));

// Comparison operators
x = 10;
y = 20;

console.log("");
console.log("=== Comparison Operators ===");
console.log(str(x) + " == " + str(y) + " is " + str(x == y));
console.log(str(x) + " != " + str(y) + " is " + str(x != y));
console.log(str(x) + " < " + str(y) + " is " + str(x < y));
console.log(str(x) + " > " + str(y) + " is " + str(x > y));

// Logical operators
hasAccount = true;
isVerified = false;

console.log("");
console.log("=== Logical Operators ===");
console.log("Has account: " + str(hasAccount));
console.log("Is verified: " + str(isVerified));
console.log("Can login: " + str(hasAccount && isVerified));
console.log("Show warning: " + str(hasAccount && !isVerified));

// Practical example: calculating a discount
price = 100;
quantity = 3;
isVIP = true;

subtotal = price * quantity;
vipDiscount = 0.1;
regularDiscount = 0.05;

// Apply discount based on VIP status
discount = isVIP && vipDiscount || regularDiscount;
total = subtotal - (subtotal * discount);

console.log("");
console.log("=== Order Calculation ===");
console.log("Price: $" + str(price));
console.log("Quantity: " + str(quantity));
console.log("Subtotal: $" + str(subtotal));
console.log("VIP Customer: " + str(isVIP));
console.log("Discount: " + str(discount * 100) + "%");
console.log("Total: $" + str(total));
