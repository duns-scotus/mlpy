// Advanced Data Processing Pipeline - ML Language Demo
// Demonstrates data analysis, statistical computation, and processing workflows
// Using current ML language features: functions, objects, arrays, control flow

import collections;
import math;
import random;

// Data structure for sales records
function createSalesRecord(id, date, product, category, amount, quantity, region) {
    record = {};
    record.id = id;
    record.date = date;
    record.product = product;
    record.category = category;
    record.amount = amount;
    record.quantity = quantity;
    record.region = region;
    record.profit_margin = 0.0;
    return record;
}

// Statistical analysis results
function createAnalysisResult() {
    result = {};
    result.total_records = 0;
    result.total_revenue = 0.0;
    result.avg_sale_amount = 0.0;
    result.max_sale = 0.0;
    result.min_sale = 0.0;
    result.median_sale = 0.0;
    result.std_deviation = 0.0;
    result.category_breakdown = {};
    result.regional_performance = {};
    result.top_products = [];
    result.monthly_trends = {};
    return result;
}

// Generate sample sales data for testing
function generateSampleData(num_records) {
    products = ["Laptop", "Mouse", "Keyboard", "Monitor", "Headphones", "Webcam", "Tablet", "Phone", "Printer", "Scanner"];
    categories = ["Electronics", "Accessories", "Computing", "Mobile", "Office"];
    regions = ["North", "South", "East", "West", "Central"];

    data = [];

    i = 0;
    while (i < num_records) {
        // Generate realistic sales data
        product_idx = math.floor(random.randomFloat() * collections.length(products));
        category_idx = math.floor(random.randomFloat() * collections.length(categories));
        region_idx = math.floor(random.randomFloat() * collections.length(regions));

        product = products[product_idx];
        category = categories[category_idx];
        region = regions[region_idx];

        // Generate realistic amounts and quantities
        base_amount = random.randomFloat() * 2000 + 50; // $50-$2050
        quantity = math.floor(random.randomFloat() * 10) + 1; // 1-10 items
        amount = base_amount * quantity;

        // Generate date (simple day of year)
        date = math.floor(random.randomFloat() * 365) + 1;

        record = createSalesRecord(i + 1, date, product, category, amount, quantity, region);
        data = collections.append(data, record);

        i = i + 1;
    }

    return data;
}

// Core statistical functions
function calculateSum(data, field) {
    sum = 0.0;
    i = 0;
    while (i < collections.length(data)) {
        record = data[i];
        sum = sum + record[field];
        i = i + 1;
    }
    return sum;
}

function calculateAverage(data, field) {
    if (collections.length(data) == 0) {
        return 0.0;
    }
    sum = calculateSum(data, field);
    return sum / collections.length(data);
}

function findMinMax(data, field) {
    if (collections.length(data) == 0) {
        result = {};
        result.min = 0.0;
        result.max = 0.0;
        return result;
    }

    first_record = data[0];
    min_val = first_record[field];
    max_val = first_record[field];

    i = 1;
    while (i < collections.length(data)) {
        record = data[i];
        value = record[field];

        if (value < min_val) {
            min_val = value;
        } elif (value > max_val) {
            max_val = value;
        }

        i = i + 1;
    }

    result = {};
    result.min = min_val;
    result.max = max_val;
    return result;
}

function calculateMedian(data, field) {
    if (collections.length(data) == 0) {
        return 0.0;
    }

    // Extract values and sort them (simple bubble sort for demo)
    values = [];
    i = 0;
    while (i < collections.length(data)) {
        record = data[i];
        values = collections.append(values, record[field]);
        i = i + 1;
    }

    // Bubble sort
    sorted_values = bubbleSort(values);

    length = collections.length(sorted_values);
    if (length % 2 == 0) {
        // Even number of elements - average of middle two
        mid1 = sorted_values[length / 2 - 1];
        mid2 = sorted_values[length / 2];
        return (mid1 + mid2) / 2.0;
    } else {
        // Odd number of elements - middle element
        return sorted_values[math.floor(length / 2)];
    }
}

function bubbleSort(arr) {
    sorted_arr = collections.copy(arr);
    n = collections.length(sorted_arr);

    i = 0;
    while (i < n - 1) {
        j = 0;
        while (j < n - i - 1) {
            if (sorted_arr[j] > sorted_arr[j + 1]) {
                // Swap elements
                temp = sorted_arr[j];
                sorted_arr[j] = sorted_arr[j + 1];
                sorted_arr[j + 1] = temp;
            }
            j = j + 1;
        }
        i = i + 1;
    }

    return sorted_arr;
}

function calculateStandardDeviation(data, field) {
    if (collections.length(data) <= 1) {
        return 0.0;
    }

    mean = calculateAverage(data, field);
    variance_sum = 0.0;

    i = 0;
    while (i < collections.length(data)) {
        record = data[i];
        difference = record[field] - mean;
        variance_sum = variance_sum + (difference * difference);
        i = i + 1;
    }

    variance = variance_sum / (collections.length(data) - 1);
    return math.sqrt(variance);
}

// Data filtering and grouping
function filterByCategory(data, category) {
    filtered = [];
    i = 0;
    while (i < collections.length(data)) {
        record = data[i];
        if (record.category == category) {
            filtered = collections.append(filtered, record);
        }
        i = i + 1;
    }
    return filtered;
}

function filterByRegion(data, region) {
    filtered = [];
    i = 0;
    while (i < collections.length(data)) {
        record = data[i];
        if (record.region == region) {
            filtered = collections.append(filtered, record);
        }
        i = i + 1;
    }
    return filtered;
}

function filterByAmountRange(data, min_amount, max_amount) {
    filtered = [];
    i = 0;
    while (i < collections.length(data)) {
        record = data[i];
        if (record.amount >= min_amount && record.amount <= max_amount) {
            filtered = collections.append(filtered, record);
        }
        i = i + 1;
    }
    return filtered;
}

function groupByCategory(data) {
    groups = {};

    i = 0;
    while (i < collections.length(data)) {
        record = data[i];
        category = record.category;

        if (!collections.hasKey(groups, category)) {
            groups[category] = [];
        }

        groups[category] = collections.append(groups[category], record);
        i = i + 1;
    }

    return groups;
}

function groupByRegion(data) {
    groups = {};

    i = 0;
    while (i < collections.length(data)) {
        record = data[i];
        region = record.region;

        if (!collections.hasKey(groups, region)) {
            groups[region] = [];
        }

        groups[region] = collections.append(groups[region], record);
        i = i + 1;
    }

    return groups;
}

// Advanced analytics
function findTopProducts(data, top_n) {
    // Group by product and calculate total sales
    product_sales = {};

    i = 0;
    while (i < collections.length(data)) {
        record = data[i];
        product = record.product;

        if (!collections.hasKey(product_sales, product)) {
            product_sales[product] = 0.0;
        }

        product_sales[product] = product_sales[product] + record.amount;
        i = i + 1;
    }

    // Convert to sorted list
    products = [];
    product_keys = collections.keys(product_sales);

    i = 0;
    while (i < collections.length(product_keys)) {
        key = product_keys[i];
        product_info = {};
        product_info.name = key;
        product_info.total_sales = product_sales[key];
        products = collections.append(products, product_info);
        i = i + 1;
    }

    // Sort products by sales (simple selection sort)
    sorted_products = selectionSort(products);

    // Return top N
    top_products = [];
    count = math.min(top_n, collections.length(sorted_products));
    i = 0;
    while (i < count) {
        top_products = collections.append(top_products, sorted_products[i]);
        i = i + 1;
    }

    return top_products;
}

function selectionSort(products) {
    sorted_products = collections.copy(products);
    n = collections.length(sorted_products);

    i = 0;
    while (i < n - 1) {
        max_idx = i;
        j = i + 1;
        while (j < n) {
            if (sorted_products[j].total_sales > sorted_products[max_idx].total_sales) {
                max_idx = j;
            }
            j = j + 1;
        }

        // Swap elements
        if (max_idx != i) {
            temp = sorted_products[i];
            sorted_products[i] = sorted_products[max_idx];
            sorted_products[max_idx] = temp;
        }

        i = i + 1;
    }

    return sorted_products;
}

function analyzeMonthlyTrends(data) {
    monthly_data = {};

    i = 0;
    while (i < collections.length(data)) {
        record = data[i];
        month = math.floor((record.date - 1) / 30) + 1; // Approximate month

        if (!collections.hasKey(monthly_data, month)) {
            month_info = {};
            month_info.total_sales = 0.0;
            month_info.total_quantity = 0;
            month_info.transaction_count = 0;
            monthly_data[month] = month_info;
        }

        monthly_data[month].total_sales = monthly_data[month].total_sales + record.amount;
        monthly_data[month].total_quantity = monthly_data[month].total_quantity + record.quantity;
        monthly_data[month].transaction_count = monthly_data[month].transaction_count + 1;

        i = i + 1;
    }

    return monthly_data;
}

// Main data analysis pipeline
function performFullAnalysis(data) {
    print("Starting comprehensive data analysis...");

    result = createAnalysisResult();

    // Basic statistics
    result.total_records = collections.length(data);
    result.total_revenue = calculateSum(data, "amount");
    result.avg_sale_amount = calculateAverage(data, "amount");

    min_max = findMinMax(data, "amount");
    result.min_sale = min_max.min;
    result.max_sale = min_max.max;

    result.median_sale = calculateMedian(data, "amount");
    result.std_deviation = calculateStandardDeviation(data, "amount");

    print("Basic statistics calculated.");

    // Category analysis
    category_groups = groupByCategory(data);
    category_keys = collections.keys(category_groups);

    i = 0;
    while (i < collections.length(category_keys)) {
        category = category_keys[i];
        category_data = category_groups[category];

        category_stats = {};
        category_stats.total_sales = calculateSum(category_data, "amount");
        category_stats.avg_sale = calculateAverage(category_data, "amount");
        category_stats.transaction_count = collections.length(category_data);

        result.category_breakdown[category] = category_stats;
        i = i + 1;
    }

    print("Category analysis completed.");

    // Regional analysis
    regional_groups = groupByRegion(data);
    region_keys = collections.keys(regional_groups);

    i = 0;
    while (i < collections.length(region_keys)) {
        region = region_keys[i];
        region_data = regional_groups[region];

        region_stats = {};
        region_stats.total_sales = calculateSum(region_data, "amount");
        region_stats.avg_sale = calculateAverage(region_data, "amount");
        region_stats.transaction_count = collections.length(region_data);

        result.regional_performance[region] = region_stats;
        i = i + 1;
    }

    print("Regional analysis completed.");

    // Product analysis
    result.top_products = findTopProducts(data, 5);
    print("Top products analysis completed.");

    // Temporal analysis
    result.monthly_trends = analyzeMonthlyTrends(data);
    print("Monthly trends analysis completed.");

    return result;
}

// Report generation
function displayAnalysisReport(result) {
    print("=====================================");
    print("     COMPREHENSIVE DATA ANALYSIS     ");
    print("=====================================");
    print("");

    // Basic statistics
    print("=== BASIC STATISTICS ===");
    print("Total Records: " + result.total_records);
    print("Total Revenue: $" + formatCurrency(result.total_revenue));
    print("Average Sale: $" + formatCurrency(result.avg_sale_amount));
    print("Minimum Sale: $" + formatCurrency(result.min_sale));
    print("Maximum Sale: $" + formatCurrency(result.max_sale));
    print("Median Sale: $" + formatCurrency(result.median_sale));
    print("Standard Deviation: $" + formatCurrency(result.std_deviation));
    print("");

    // Category breakdown
    print("=== CATEGORY PERFORMANCE ===");
    category_keys = collections.keys(result.category_breakdown);
    i = 0;
    while (i < collections.length(category_keys)) {
        category = category_keys[i];
        stats = result.category_breakdown[category];

        print(category + ":");
        print("  Total Sales: $" + formatCurrency(stats.total_sales));
        print("  Avg Sale: $" + formatCurrency(stats.avg_sale));
        print("  Transactions: " + stats.transaction_count);
        print("");

        i = i + 1;
    }

    // Regional performance
    print("=== REGIONAL PERFORMANCE ===");
    region_keys = collections.keys(result.regional_performance);
    i = 0;
    while (i < collections.length(region_keys)) {
        region = region_keys[i];
        stats = result.regional_performance[region];

        print(region + " Region:");
        print("  Total Sales: $" + formatCurrency(stats.total_sales));
        print("  Avg Sale: $" + formatCurrency(stats.avg_sale));
        print("  Transactions: " + stats.transaction_count);
        print("");

        i = i + 1;
    }

    // Top products
    print("=== TOP PRODUCTS ===");
    i = 0;
    while (i < collections.length(result.top_products)) {
        product = result.top_products[i];
        rank = i + 1;
        print(rank + ". " + product.name + " - $" + formatCurrency(product.total_sales));
        i = i + 1;
    }
    print("");

    // Monthly trends
    print("=== MONTHLY TRENDS ===");
    month_keys = collections.keys(result.monthly_trends);
    month_keys = bubbleSort(month_keys); // Sort months

    i = 0;
    while (i < collections.length(month_keys)) {
        month = month_keys[i];
        trends = result.monthly_trends[month];

        print("Month " + month + ":");
        print("  Sales: $" + formatCurrency(trends.total_sales));
        print("  Transactions: " + trends.transaction_count);
        print("  Avg per Transaction: $" + formatCurrency(trends.total_sales / trends.transaction_count));
        print("");

        i = i + 1;
    }
}

function formatCurrency(amount) {
    // Simple currency formatting
    rounded = math.floor(amount * 100) / 100;
    return rounded;
}

// Advanced filtering and reporting
function performAdvancedAnalysis(data) {
    print("=== ADVANCED ANALYSIS ===");

    // High-value transactions (>$1000)
    high_value = filterByAmountRange(data, 1000.0, 999999.0);
    print("High-value transactions (>$1000): " + collections.length(high_value));

    if (collections.length(high_value) > 100) {
        print("Large number of high-value transactions detected");
    } elif (collections.length(high_value) > 10) {
        print("Moderate number of high-value transactions");
        hv_avg = calculateAverage(high_value, "amount");
        print("Average high-value transaction: $" + formatCurrency(hv_avg));
    } elif (collections.length(high_value) > 0) {
        print("Few high-value transactions found");
        hv_avg = calculateAverage(high_value, "amount");
        print("Average high-value transaction: $" + formatCurrency(hv_avg));
    } else {
        print("No high-value transactions found");
    }

    // Regional comparison
    print("");
    print("Regional Revenue Comparison:");
    regions = ["North", "South", "East", "West", "Central"];

    i = 0;
    while (i < collections.length(regions)) {
        region = regions[i];
        region_data = filterByRegion(data, region);

        if (collections.length(region_data) > 0) {
            total = calculateSum(region_data, "amount");
            avg = calculateAverage(region_data, "amount");
            print(region + ": $" + formatCurrency(total) + " (avg: $" + formatCurrency(avg) + ")");
        }

        i = i + 1;
    }

    // Category performance ranking
    print("");
    print("Category Performance Ranking:");
    categories = ["Electronics", "Accessories", "Computing", "Mobile", "Office"];

    category_totals = [];
    i = 0;
    while (i < collections.length(categories)) {
        category = categories[i];
        category_data = filterByCategory(data, category);

        if (collections.length(category_data) > 0) {
            total = calculateSum(category_data, "amount");

            cat_info = {};
            cat_info.name = category;
            cat_info.total = total;
            category_totals = collections.append(category_totals, cat_info);
        }

        i = i + 1;
    }

    // Sort by total (reuse selection sort logic)
    sorted_categories = selectionSort(category_totals);

    i = 0;
    while (i < collections.length(sorted_categories)) {
        cat = sorted_categories[i];
        rank = i + 1;
        print(rank + ". " + cat.name + ": $" + formatCurrency(cat.total));
        i = i + 1;
    }
}

// Main execution
function runDataProcessingDemo() {
    print("Advanced Data Processing Pipeline Demo");
    print("===================================");

    // Set random seed for reproducible results
    random.setSeed(42);

    // Generate sample dataset
    print("Generating sample sales data...");
    sample_data = generateSampleData(1000);
    print("Generated " + collections.length(sample_data) + " sales records");
    print("");

    // Perform comprehensive analysis
    analysis_result = performFullAnalysis(sample_data);

    // Display detailed report
    displayAnalysisReport(analysis_result);

    // Run advanced analytics
    performAdvancedAnalysis(sample_data);

    print("");
    print("=====================================");
    print("Data processing pipeline completed!");
    print("This demonstrates ML's capabilities for:");
    print("- Complex data structures and manipulation");
    print("- Statistical analysis and computation");
    print("- Grouping, filtering, and aggregation");
    print("- Sorting algorithms and data processing");
    print("- Report generation and formatting");
    print("=====================================");

    return collections.length(sample_data);
}

// Entry point
function main() {
    print("ML Advanced Data Processing Demo");
    print("===============================");

    records_processed = runDataProcessingDemo();

    print("");
    print("Successfully processed " + records_processed + " records!");
    print("Demonstrated advanced ML language features:");
    print("- Object creation and manipulation");
    print("- Array operations and algorithms");
    print("- Mathematical computations");
    print("- Control flow with if/elif/else");
    print("- Function composition and modularity");

    return 0;
}