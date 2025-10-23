// ============================================
// Example: Comprehensive Functions Example
// Category: language-reference/functions
// Demonstrates: All function concepts in a practical data processing pipeline
// ============================================

import console;
import functional;

console.log("=== Data Processing Pipeline ===\n");

// Sample dataset: Sales transactions
transactions = [
    {id: 1, product: "Laptop", amount: 1200, category: "Electronics", date: "2024-01"},
    {id: 2, product: "Coffee", amount: 5, category: "Food", date: "2024-01"},
    {id: 3, product: "Monitor", amount: 300, category: "Electronics", date: "2024-01"},
    {id: 4, product: "Sandwich", amount: 8, category: "Food", date: "2024-01"},
    {id: 5, product: "Mouse", amount: 25, category: "Electronics", date: "2024-02"},
    {id: 6, product: "Tea", amount: 3, category: "Food", date: "2024-02"},
    {id: 7, product: "Keyboard", amount: 75, category: "Electronics", date: "2024-02"},
    {id: 8, product: "Headphones", amount: 150, category: "Electronics", date: "2024-03"}
];

console.log("Processing " + str(len(transactions)) + " transactions...\n");

// Named function: Calculate statistics
function calculateStats(amounts) {
    if (len(amounts) == 0) {
        return {total: 0, average: 0, min: 0, max: 0};
    }

    total = 0;
    for (amount in amounts) {
        total = total + amount;
    }

    minVal = amounts[0];
    maxVal = amounts[0];
    for (amount in amounts) {
        if (amount < minVal) {
            minVal = amount;
        }
        if (amount > maxVal) {
            maxVal = amount;
        }
    }

    return {
        total: total,
        average: total / len(amounts),
        min: minVal,
        max: maxVal,
        count: len(amounts)
    };
}

// Arrow functions for filtering
isElectronics = fn(t) => t.category == "Electronics";
isFood = fn(t) => t.category == "Food";
isHighValue = fn(t) => t.amount >= 100;
isJanuary = fn(t) => t.date == "2024-01";

// Arrow functions for transformation
getAmount = fn(t) => t.amount;
getProduct = fn(t) => t.product;
getCategory = fn(t) => t.category;

// Closure: Create category filter factory
function makeCategoryFilter(category) {
    return fn(transaction) => transaction.category == category;
}

// Closure: Create discount calculator
function makeDiscountCalculator(percent) {
    return fn(amount) => amount * (100 - percent) / 100;
}

// Analysis 1: Overall statistics
console.log("=== Overall Statistics ===");
allAmounts = functional.map(getAmount, transactions);
stats = calculateStats(allAmounts);
console.log("Total transactions: " + str(stats.count));
console.log("Total revenue: $" + str(stats.total));
console.log("Average transaction: $" + str(stats.average));
console.log("Minimum: $" + str(stats.min));
console.log("Maximum: $" + str(stats.max));

// Analysis 2: Category breakdown using closures
console.log("\n=== Category Analysis ===");
categories = ["Electronics", "Food"];
for (category in categories) {
    filterFunc = makeCategoryFilter(category);
    categoryTrans = functional.filter(filterFunc, transactions);
    categoryAmounts = functional.map(getAmount, categoryTrans);
    categoryStats = calculateStats(categoryAmounts);

    console.log("\n" + category + ":");
    console.log("  Count: " + str(categoryStats.count));
    console.log("  Total: $" + str(categoryStats.total));
    console.log("  Average: $" + str(categoryStats.average));
}

// Analysis 3: High-value transactions
console.log("\n=== High-Value Transactions (>= $100) ===");
highValue = functional.filter(isHighValue, transactions);
console.log("Found " + str(len(highValue)) + " high-value transactions:");
for (trans in highValue) {
    console.log("  " + trans.product + ": $" + str(trans.amount));
}

// Analysis 4: Monthly breakdown
console.log("\n=== Monthly Revenue ===");
months = ["2024-01", "2024-02", "2024-03"];
for (month in months) {
    monthFilter = fn(t) => t.date == month;
    monthTrans = functional.filter(monthFilter, transactions);
    monthAmounts = functional.map(getAmount, monthTrans);
    monthStats = calculateStats(monthAmounts);

    console.log(month + ": $" + str(monthStats.total) + " (" + str(monthStats.count) + " transactions)");
}

// Analysis 5: Apply discounts using closures
console.log("\n=== Discount Scenarios ===");
discounts = [10, 20, 30];
electronicsFilter = makeCategoryFilter("Electronics");
electronics = functional.filter(electronicsFilter, transactions);
electronicsAmounts = functional.map(getAmount, electronics);

console.log("Electronics total: $" + str(calculateStats(electronicsAmounts).total));
for (discount in discounts) {
    discountFunc = makeDiscountCalculator(discount);
    discounted = functional.map(discountFunc, electronicsAmounts);
    newTotal = calculateStats(discounted).total;
    console.log("  With " + str(discount) + "% discount: $" + str(newTotal));
}

// Recursive function: Find transaction by ID
function findTransactionById(trans, targetId, index) {
    if (index >= len(trans)) {
        return null;
    }

    if (trans[index].id == targetId) {
        return trans[index];
    }

    return findTransactionById(trans, targetId, index + 1);
}

console.log("\n=== Transaction Lookup ===");
searchIds = [3, 7, 99];
for (searchId in searchIds) {
    found = findTransactionById(transactions, searchId, 0);
    if (found != null) {
        console.log("ID " + str(searchId) + ": " + found.product + " - $" + str(found.amount));
    } else {
        console.log("ID " + str(searchId) + ": Not found");
    }
}

// Higher-order function: Apply function to specific field
function processField(items, fieldGetter, processor) {
    values = functional.map(fieldGetter, items);
    return functional.map(processor, values);
}

console.log("\n=== Field Processing ===");
// Double all amounts
doubler = fn(x) => x * 2;
doubledAmounts = processField(transactions, getAmount, doubler);
console.log("Original amounts: " + str(functional.map(getAmount, transactions)));
console.log("Doubled amounts: " + str(doubledAmounts));

// Recursive function: Calculate compound growth
function compoundGrowth(principal, rate, years) {
    if (years == 0) {
        return principal;
    } else {
        return compoundGrowth(principal * (1 + rate), rate, years - 1);
    }
}

console.log("\n=== Growth Projection ===");
initialRevenue = stats.total;
growthRate = 0.10;  // 10% annual growth
console.log("Current revenue: $" + str(initialRevenue));
for (year in range(1, 4)) {
    projected = compoundGrowth(initialRevenue, growthRate, year);
    console.log("Year " + str(year) + " projection: $" + str(projected));
}

// Function composition: Chain multiple operations
console.log("\n=== Top Electronics Products ===");
electronicsOnly = functional.filter(isElectronics, transactions);
highValueElectronics = functional.filter(isHighValue, electronicsOnly);
productNames = functional.map(getProduct, highValueElectronics);
console.log("High-value electronics: " + str(productNames));

console.log("\n=== Data Processing Complete ===");
