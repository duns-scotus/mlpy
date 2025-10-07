// ============================================
// Comprehensive Example: E-commerce Order Processing
// Category: standard-library/functional
// Demonstrates: Complete functional programming pipeline
// ============================================

import console;
import functional;

console.log("=== E-commerce Order Processing System ===\n");

// ============================================
// Dataset: Customer Orders
// ============================================

orders = [
    {id: 1001, customer: "Alice", amount: 150, status: "pending", items: 3},
    {id: 1002, customer: "Bob", amount: 45, status: "shipped", items: 1},
    {id: 1003, customer: "Charlie", amount: 320, status: "pending", items: 5},
    {id: 1004, customer: "Diana", amount: 89, status: "delivered", items: 2},
    {id: 1005, customer: "Eve", amount: 210, status: "pending", items: 4},
    {id: 1006, customer: "Frank", amount: 35, status: "cancelled", items: 1},
    {id: 1007, customer: "Grace", amount: 180, status: "shipped", items: 3},
    {id: 1008, customer: "Henry", amount: 95, status: "delivered", items: 2},
    {id: 1009, customer: "Ivy", amount: 270, status: "pending", items: 6},
    {id: 1010, customer: "Jack", amount: 120, status: "shipped", items: 2}
];

console.log("Total orders: " + str(len(orders)) + "\n");

// ============================================
// Function Composition: Order Processing
// ============================================

console.log("=== Order Processing Pipeline ===");

// Helper functions
function getAmount(order) {
    return order.amount;
}

function isPending(order) {
    return order.status == "pending";
}

function isShipped(order) {
    return order.status == "shipped";
}

function isDelivered(order) {
    return order.status == "delivered";
}

function isLargeOrder(order) {
    return order.amount >= 150;
}

// Group orders by status
function getStatus(order) {
    return order.status;
}

groupedByStatus = functional.groupBy(getStatus, orders);
console.log("Orders by status: " + str(groupedByStatus));

// ============================================
// Filter and Map: Pending Orders
// ============================================

console.log("\n=== Pending Orders Analysis ===");

pendingOrders = functional.filter(isPending, orders);
console.log("Pending orders: " + str(len(pendingOrders)));

pendingAmounts = functional.map(getAmount, pendingOrders);
console.log("Pending amounts: " + str(pendingAmounts));

// Calculate total pending revenue
function add(a, b) {
    return a + b;
}

totalPending = functional.reduce(add, pendingAmounts, 0);
console.log("Total pending revenue: $" + str(totalPending));

// ============================================
// Partition: Large vs Small Orders
// ============================================

console.log("\n=== Order Size Analysis ===");

partitioned = functional.partition(isLargeOrder, orders);
largeOrders = partitioned[0];
smallOrders = partitioned[1];

console.log("Large orders (>=$150): " + str(len(largeOrders)));
console.log("Small orders (<$150): " + str(len(smallOrders)));

// Average order values
function calculateAverage(orderList) {
    if (len(orderList) == 0) {
        return 0;
    }
    amounts = functional.map(getAmount, orderList);
    total = functional.reduce(add, amounts, 0);
    return total / len(orderList);
}

avgLarge = calculateAverage(largeOrders);
avgSmall = calculateAverage(smallOrders);

console.log("Average large order: $" + str(round(avgLarge, 2)));
console.log("Average small order: $" + str(round(avgSmall, 2)));

// ============================================
// Composition: Priority Processing
// ============================================

console.log("\n=== Priority Processing ===");

function isPendingAndLarge(order) {
    return isPending(order) && isLargeOrder(order);
}

priorityOrders = functional.filter(isPendingAndLarge, orders);
console.log("High-priority orders (pending + large): " + str(len(priorityOrders)));

// Extract customer names
function getCustomer(order) {
    return order.customer;
}

priorityCustomers = functional.map(getCustomer, priorityOrders);
console.log("Priority customers: " + str(priorityCustomers));

// ============================================
// Statistical Analysis with Juxt
// ============================================

console.log("\n=== Revenue Statistics ===");

function minOrder(orderList) {
    amounts = functional.map(getAmount, orderList);
    smallest = amounts[0];
    i = 1;
    while (i < len(amounts)) {
        if (amounts[i] < smallest) {
            smallest = amounts[i];
        }
        i = i + 1;
    }
    return smallest;
}

function maxOrder(orderList) {
    amounts = functional.map(getAmount, orderList);
    largest = amounts[0];
    i = 1;
    while (i < len(amounts)) {
        if (amounts[i] > largest) {
            largest = amounts[i];
        }
        i = i + 1;
    }
    return largest;
}

function totalRevenue(orderList) {
    amounts = functional.map(getAmount, orderList);
    return functional.reduce(add, amounts, 0);
}

function countOrders(orderList) {
    return len(orderList);
}

// Apply all statistics
stats = functional.juxt([minOrder, maxOrder, totalRevenue, countOrders]);
results = stats(orders);

console.log("Min order: $" + str(results[0]));
console.log("Max order: $" + str(results[1]));
console.log("Total revenue: $" + str(results[2]));
console.log("Order count: " + str(results[3]));
console.log("Average order: $" + str(round(results[2] / results[3], 2)));

// ============================================
// Conditional Processing with IfElse
// ============================================

console.log("\n=== Shipping Cost Calculation ===");

function applyDiscount(amount) {
    return amount * 0.9;  // 10% discount
}

function applyShipping(amount) {
    return amount + 10;  // $10 shipping
}

// Free shipping for orders >= $100, else add shipping
function qualifiesForFreeShipping(amount) {
    return amount >= 100;
}

calculateFinal = functional.ifElse(
    qualifiesForFreeShipping,
    applyDiscount,
    applyShipping
);

testAmounts = [50, 120, 85, 200, 95];
console.log("Test amounts: " + str(testAmounts));

finalAmounts = functional.map(calculateFinal, testAmounts);
console.log("Final amounts: " + str(finalAmounts));

// ============================================
// Multi-Condition Status Classification
// ============================================

console.log("\n=== Order Status Classification ===");

function statusPending(order) {
    return order.status == "pending";
}

function statusShipped(order) {
    return order.status == "shipped";
}

function statusDelivered(order) {
    return order.status == "delivered";
}

function urgent(order) {
    return "URGENT: " + order.customer;
}

function inTransit(order) {
    return "In Transit: " + order.customer;
}

function complete(order) {
    return "Complete: " + order.customer;
}

function other(order) {
    return "Other: " + order.customer;
}

statusConditions = [
    [statusPending, urgent],
    [statusShipped, inTransit],
    [statusDelivered, complete]
];

classifyOrder = functional.cond(statusConditions);

// Classify first 5 orders
firstFive = functional.take(5, orders);
classifications = functional.map(classifyOrder, firstFive);

console.log("Order classifications:");
i = 0;
while (i < len(classifications)) {
    console.log("  " + str(classifications[i]));
    i = i + 1;
}

// ============================================
// Data Transformation Pipeline
// ============================================

console.log("\n=== Complete Processing Pipeline ===");
console.log("Pipeline: Filter pending -> Filter large -> Sort -> Take top 3");

// Step 1: Filter pending
step1 = functional.filter(isPending, orders);
console.log("Step 1 - Pending orders: " + str(len(step1)));

// Step 2: Filter large
step2 = functional.filter(isLargeOrder, step1);
console.log("Step 2 - Large pending orders: " + str(len(step2)));

// Step 3: Extract amounts
step3 = functional.map(getAmount, step2);
console.log("Step 3 - Amounts: " + str(step3));

// Step 4: Take top (already large, so just show them)
console.log("Result: " + str(step3));

// ============================================
// Batch Processing with Chunk
// ============================================

console.log("\n=== Batch Processing ===");

batchSize = 3;
batches = functional.chunk(batchSize, orders);

console.log("Processing " + str(len(orders)) + " orders in batches of " + str(batchSize));
console.log("Number of batches: " + str(len(batches)));

// Process each batch
i = 0;
while (i < len(batches)) {
    batch = batches[i];
    batchRevenue = totalRevenue(batch);
    console.log("Batch " + str(i + 1) + ": " + str(len(batch)) + " orders, $" + str(batchRevenue));
    i = i + 1;
}

// ============================================
// Memoization for Performance
// ============================================

console.log("\n=== Performance Optimization ===");

function expensiveCalculation(n) {
    // Simulate expensive computation
    return n * n * n;
}

// Memoize the calculation
memoizedCalc = functional.memoize(expensiveCalculation);

// First call: computes
result1 = memoizedCalc(10);
console.log("First call (10^3): " + str(result1));

// Second call with same argument: cached
result2 = memoizedCalc(10);
console.log("Second call (10^3): " + str(result2) + " (cached)");

// Different argument: computes
result3 = memoizedCalc(5);
console.log("Third call (5^3): " + str(result3));

// ============================================
// Summary Report
// ============================================

console.log("\n=== Summary Report ===");

// Count by status using partition and filter
pending = functional.filter(isPending, orders);
shipped = functional.filter(isShipped, orders);
delivered = functional.filter(isDelivered, orders);

console.log("Order Status:");
console.log("  Pending: " + str(len(pending)));
console.log("  Shipped: " + str(len(shipped)));
console.log("  Delivered: " + str(len(delivered)));

// Revenue by status
pendingRev = totalRevenue(pending);
shippedRev = totalRevenue(shipped);
deliveredRev = totalRevenue(delivered);

console.log("\nRevenue by Status:");
console.log("  Pending: $" + str(pendingRev));
console.log("  Shipped: $" + str(shippedRev));
console.log("  Delivered: $" + str(deliveredRev));
console.log("  Total: $" + str(pendingRev + shippedRev + deliveredRev));

// High-value customers
highValueOrders = functional.filter(isLargeOrder, orders);
highValueCustomers = functional.map(getCustomer, highValueOrders);
uniqueHighValue = functional.unique(highValueCustomers);

console.log("\nHigh-value customers: " + str(uniqueHighValue));

console.log("\n=== Order Processing Complete ===");
