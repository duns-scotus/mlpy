"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib import console, getCurrentTime, processData

from mlpy.stdlib.collections import collections as ml_collections

from mlpy.stdlib.math import math as ml_math

from mlpy.stdlib.random import random as ml_random

def createSalesRecord(id, date, product, category, amount, quantity, region):
    record = {}
    record['id'] = id
    record['date'] = date
    record['product'] = product
    record['category'] = category
    record['amount'] = amount
    record['quantity'] = quantity
    record['region'] = region
    record['profit_margin'] = 0.0
    return record

def createAnalysisResult():
    result = {}
    result['total_records'] = 0
    result['total_revenue'] = 0.0
    result['avg_sale_amount'] = 0.0
    result['max_sale'] = 0.0
    result['min_sale'] = 0.0
    result['median_sale'] = 0.0
    result['std_deviation'] = 0.0
    result['category_breakdown'] = {}
    result['regional_performance'] = {}
    result['top_products'] = []
    result['monthly_trends'] = {}
    return result

def generateSampleData(num_records):
    products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones', 'Webcam', 'Tablet', 'Phone', 'Printer', 'Scanner']
    categories = ['Electronics', 'Accessories', 'Computing', 'Mobile', 'Office']
    regions = ['North', 'South', 'East', 'West', 'Central']
    data = []
    i = 0
    while (i < num_records):
        product_idx = ml_math.floor((ml_random.randomFloat() * ml_collections.length(products)))
        category_idx = ml_math.floor((ml_random.randomFloat() * ml_collections.length(categories)))
        region_idx = ml_math.floor((ml_random.randomFloat() * ml_collections.length(regions)))
        product = products[product_idx]
        category = categories[category_idx]
        region = regions[region_idx]
        base_amount = ((ml_random.randomFloat() * 2000) + 50)
        quantity = (ml_math.floor((ml_random.randomFloat() * 10)) + 1)
        amount = (base_amount * quantity)
        date = (ml_math.floor((ml_random.randomFloat() * 365)) + 1)
        record = createSalesRecord((i + 1), date, product, category, amount, quantity, region)
        data = ml_collections.append(data, record)
        i = (i + 1)
    return data

def calculateSum(data, field):
    sum = 0.0
    i = 0
    while (i < ml_collections.length(data)):
        record = data[i]
        sum = (sum + record[field])
        i = (i + 1)
    return sum

def calculateAverage(data, field):
    if (ml_collections.length(data) == 0):
        return 0.0
    sum = calculateSum(data, field)
    return (sum / ml_collections.length(data))

def findMinMax(data, field):
    if (ml_collections.length(data) == 0):
        result = {}
        result['min'] = 0.0
        result['max'] = 0.0
        return result
    first_record = data[0]
    min_val = first_record[field]
    max_val = first_record[field]
    i = 1
    while (i < ml_collections.length(data)):
        record = data[i]
        value = record[field]
        if (value < min_val):
            min_val = value
        elif (value > max_val):
            max_val = value
        i = (i + 1)
    result = {}
    result['min'] = min_val
    result['max'] = max_val
    return result

def calculateMedian(data, field):
    if (ml_collections.length(data) == 0):
        return 0.0
    values = []
    i = 0
    while (i < ml_collections.length(data)):
        record = data[i]
        values = ml_collections.append(values, record[field])
        i = (i + 1)
    sorted_values = bubbleSort(values)
    length = ml_collections.length(sorted_values)
    if ((length % 2) == 0):
        mid1 = sorted_values[((length / 2) - 1)]
        mid2 = sorted_values[(length / 2)]
        return ((mid1 + mid2) / 2.0)
    else:
        return sorted_values[ml_math.floor((length / 2))]

def bubbleSort(arr):
    sorted_arr = ml_collections.copy(arr)
    n = ml_collections.length(sorted_arr)
    i = 0
    while (i < (n - 1)):
        j = 0
        while (j < ((n - i) - 1)):
            if (sorted_arr[j] > sorted_arr[(j + 1)]):
                temp = sorted_arr[j]
                sorted_arr[j] = sorted_arr[(j + 1)]
                sorted_arr[(j + 1)] = temp
            j = (j + 1)
        i = (i + 1)
    return sorted_arr

def calculateStandardDeviation(data, field):
    if (ml_collections.length(data) <= 1):
        return 0.0
    mean = calculateAverage(data, field)
    variance_sum = 0.0
    i = 0
    while (i < ml_collections.length(data)):
        record = data[i]
        difference = (record[field] - mean)
        variance_sum = (variance_sum + (difference * difference))
        i = (i + 1)
    variance = (variance_sum / (ml_collections.length(data) - 1))
    return ml_math.sqrt(variance)

def filterByCategory(data, category):
    filtered = []
    i = 0
    while (i < ml_collections.length(data)):
        record = data[i]
        if (record['category'] == category):
            filtered = ml_collections.append(filtered, record)
        i = (i + 1)
    return filtered

def filterByRegion(data, region):
    filtered = []
    i = 0
    while (i < ml_collections.length(data)):
        record = data[i]
        if (record['region'] == region):
            filtered = ml_collections.append(filtered, record)
        i = (i + 1)
    return filtered

def filterByAmountRange(data, min_amount, max_amount):
    filtered = []
    i = 0
    while (i < ml_collections.length(data)):
        record = data[i]
        if ((record['amount'] >= min_amount) and (record['amount'] <= max_amount)):
            filtered = ml_collections.append(filtered, record)
        i = (i + 1)
    return filtered

def groupByCategory(data):
    groups = {}
    i = 0
    while (i < ml_collections.length(data)):
        record = data[i]
        category = record['category']
        if ml_collections.hasKey(groups, category):
            groups[category] = []
        groups[category] = ml_collections.append(groups[category], record)
        i = (i + 1)
    return groups

def groupByRegion(data):
    groups = {}
    i = 0
    while (i < ml_collections.length(data)):
        record = data[i]
        region = record['region']
        if ml_collections.hasKey(groups, region):
            groups[region] = []
        groups[region] = ml_collections.append(groups[region], record)
        i = (i + 1)
    return groups

def findTopProducts(data, top_n):
    product_sales = {}
    i = 0
    while (i < ml_collections.length(data)):
        record = data[i]
        product = record['product']
        if ml_collections.hasKey(product_sales, product):
            product_sales[product] = 0.0
        product_sales[product] = (product_sales[product] + record['amount'])
        i = (i + 1)
    products = []
    product_keys = ml_collections.keys(product_sales)
    i = 0
    while (i < ml_collections.length(product_keys)):
        key = product_keys[i]
        product_info = {}
        product_info['name'] = key
        product_info['total_sales'] = product_sales[key]
        products = ml_collections.append(products, product_info)
        i = (i + 1)
    sorted_products = selectionSort(products)
    top_products = []
    count = ml_math.min(top_n, ml_collections.length(sorted_products))
    i = 0
    while (i < count):
        top_products = ml_collections.append(top_products, sorted_products[i])
        i = (i + 1)
    return top_products

def selectionSort(products):
    sorted_products = ml_collections.copy(products)
    n = ml_collections.length(sorted_products)
    i = 0
    while (i < (n - 1)):
        max_idx = i
        j = (i + 1)
        while (j < n):
            if (sorted_products[j]['total_sales'] > sorted_products[max_idx]['total_sales']):
                max_idx = j
            j = (j + 1)
        if (max_idx != i):
            temp = sorted_products[i]
            sorted_products[i] = sorted_products[max_idx]
            sorted_products[max_idx] = temp
        i = (i + 1)
    return sorted_products

def analyzeMonthlyTrends(data):
    monthly_data = {}
    i = 0
    while (i < ml_collections.length(data)):
        record = data[i]
        month = (ml_math.floor(((record['date'] - 1) / 30)) + 1)
        if ml_collections.hasKey(monthly_data, month):
            month_info = {}
            month_info['total_sales'] = 0.0
            month_info['total_quantity'] = 0
            month_info['transaction_count'] = 0
            monthly_data[month] = month_info
        monthly_data[month]['total_sales'] = (monthly_data[month]['total_sales'] + record['amount'])
        monthly_data[month]['total_quantity'] = (monthly_data[month]['total_quantity'] + record['quantity'])
        monthly_data[month]['transaction_count'] = (monthly_data[month]['transaction_count'] + 1)
        i = (i + 1)
    return monthly_data

def performFullAnalysis(data):
    print('Starting comprehensive data analysis...')
    result = createAnalysisResult()
    result['total_records'] = ml_collections.length(data)
    result['total_revenue'] = calculateSum(data, 'amount')
    result['avg_sale_amount'] = calculateAverage(data, 'amount')
    min_max = findMinMax(data, 'amount')
    result['min_sale'] = min_max['min']
    result['max_sale'] = min_max['max']
    result['median_sale'] = calculateMedian(data, 'amount')
    result['std_deviation'] = calculateStandardDeviation(data, 'amount')
    print('Basic statistics calculated.')
    category_groups = groupByCategory(data)
    category_keys = ml_collections.keys(category_groups)
    i = 0
    while (i < ml_collections.length(category_keys)):
        category = category_keys[i]
        category_data = category_groups[category]
        category_stats = {}
        category_stats['total_sales'] = calculateSum(category_data, 'amount')
        category_stats['avg_sale'] = calculateAverage(category_data, 'amount')
        category_stats['transaction_count'] = ml_collections.length(category_data)
        result['category_breakdown'][category] = category_stats
        i = (i + 1)
    print('Category analysis completed.')
    regional_groups = groupByRegion(data)
    region_keys = ml_collections.keys(regional_groups)
    i = 0
    while (i < ml_collections.length(region_keys)):
        region = region_keys[i]
        region_data = regional_groups[region]
        region_stats = {}
        region_stats['total_sales'] = calculateSum(region_data, 'amount')
        region_stats['avg_sale'] = calculateAverage(region_data, 'amount')
        region_stats['transaction_count'] = ml_collections.length(region_data)
        result['regional_performance'][region] = region_stats
        i = (i + 1)
    print('Regional analysis completed.')
    result['top_products'] = findTopProducts(data, 5)
    print('Top products analysis completed.')
    result['monthly_trends'] = analyzeMonthlyTrends(data)
    print('Monthly trends analysis completed.')
    return result

def displayAnalysisReport(result):
    print('=====================================')
    print('     COMPREHENSIVE DATA ANALYSIS     ')
    print('=====================================')
    print('')
    print('=== BASIC STATISTICS ===')
    print((str('Total Records: ') + str(result['total_records'])))
    print((str('Total Revenue: $') + str(formatCurrency(result['total_revenue']))))
    print((str('Average Sale: $') + str(formatCurrency(result['avg_sale_amount']))))
    print((str('Minimum Sale: $') + str(formatCurrency(result['min_sale']))))
    print((str('Maximum Sale: $') + str(formatCurrency(result['max_sale']))))
    print((str('Median Sale: $') + str(formatCurrency(result['median_sale']))))
    print((str('Standard Deviation: $') + str(formatCurrency(result['std_deviation']))))
    print('')
    print('=== CATEGORY PERFORMANCE ===')
    category_keys = ml_collections.keys(result['category_breakdown'])
    i = 0
    while (i < ml_collections.length(category_keys)):
        category = category_keys[i]
        stats = result['category_breakdown'][category]
        print((str(category) + str(':')))
        print((str('  Total Sales: $') + str(formatCurrency(stats['total_sales']))))
        print((str('  Avg Sale: $') + str(formatCurrency(stats['avg_sale']))))
        print((str('  Transactions: ') + str(stats['transaction_count'])))
        print('')
        i = (i + 1)
    print('=== REGIONAL PERFORMANCE ===')
    region_keys = ml_collections.keys(result['regional_performance'])
    i = 0
    while (i < ml_collections.length(region_keys)):
        region = region_keys[i]
        stats = result['regional_performance'][region]
        print((str(region) + str(' Region:')))
        print((str('  Total Sales: $') + str(formatCurrency(stats['total_sales']))))
        print((str('  Avg Sale: $') + str(formatCurrency(stats['avg_sale']))))
        print((str('  Transactions: ') + str(stats['transaction_count'])))
        print('')
        i = (i + 1)
    print('=== TOP PRODUCTS ===')
    i = 0
    while (i < ml_collections.length(result['top_products'])):
        product = result['top_products'][i]
        rank = (i + 1)
        print((str((str((str((str(rank) + str('. '))) + str(product['name']))) + str(' - $'))) + str(formatCurrency(product['total_sales']))))
        i = (i + 1)
    print('')
    print('=== MONTHLY TRENDS ===')
    month_keys = ml_collections.keys(result['monthly_trends'])
    month_keys = bubbleSort(month_keys)
    i = 0
    while (i < ml_collections.length(month_keys)):
        month = month_keys[i]
        trends = result['monthly_trends'][month]
        print((str((str('Month ') + str(month))) + str(':')))
        print((str('  Sales: $') + str(formatCurrency(trends['total_sales']))))
        print((str('  Transactions: ') + str(trends['transaction_count'])))
        print((str('  Avg per Transaction: $') + str(formatCurrency((trends['total_sales'] / trends['transaction_count'])))))
        print('')
        i = (i + 1)

def formatCurrency(amount):
    rounded = (ml_math.floor((amount * 100)) / 100)
    return rounded

def performAdvancedAnalysis(data):
    print('=== ADVANCED ANALYSIS ===')
    high_value = filterByAmountRange(data, 1000.0, 999999.0)
    print((str('High-value transactions (>$1000): ') + str(ml_collections.length(high_value))))
    if (ml_collections.length(high_value) > 100):
        print('Large number of high-value transactions detected')
    elif (ml_collections.length(high_value) > 10):
        print('Moderate number of high-value transactions')
        hv_avg = calculateAverage(high_value, 'amount')
        print((str('Average high-value transaction: $') + str(formatCurrency(hv_avg))))
    elif (ml_collections.length(high_value) > 0):
        print('Few high-value transactions found')
        hv_avg = calculateAverage(high_value, 'amount')
        print((str('Average high-value transaction: $') + str(formatCurrency(hv_avg))))
    else:
        print('No high-value transactions found')
    print('')
    print('Regional Revenue Comparison:')
    regions = ['North', 'South', 'East', 'West', 'Central']
    i = 0
    while (i < ml_collections.length(regions)):
        region = regions[i]
        region_data = filterByRegion(data, region)
        if (ml_collections.length(region_data) > 0):
            total = calculateSum(region_data, 'amount')
            avg = calculateAverage(region_data, 'amount')
            print((str((str((str((str((str(region) + str(': $'))) + str(formatCurrency(total)))) + str(' (avg: $'))) + str(formatCurrency(avg)))) + str(')')))
        i = (i + 1)
    print('')
    print('Category Performance Ranking:')
    categories = ['Electronics', 'Accessories', 'Computing', 'Mobile', 'Office']
    category_totals = []
    i = 0
    while (i < ml_collections.length(categories)):
        category = categories[i]
        category_data = filterByCategory(data, category)
        if (ml_collections.length(category_data) > 0):
            total = calculateSum(category_data, 'amount')
            cat_info = {}
            cat_info['name'] = category
            cat_info['total'] = total
            category_totals = ml_collections.append(category_totals, cat_info)
        i = (i + 1)
    sorted_categories = selectionSort(category_totals)
    i = 0
    while (i < ml_collections.length(sorted_categories)):
        cat = sorted_categories[i]
        rank = (i + 1)
        print((str((str((str((str(rank) + str('. '))) + str(cat['name']))) + str(': $'))) + str(formatCurrency(cat['total']))))
        i = (i + 1)

def runDataProcessingDemo():
    print('Advanced Data Processing Pipeline Demo')
    print('===================================')
    ml_random.setSeed(42)
    print('Generating sample sales data...')
    sample_data = generateSampleData(1000)
    print((str((str('Generated ') + str(ml_collections.length(sample_data)))) + str(' sales records')))
    print('')
    analysis_result = performFullAnalysis(sample_data)
    displayAnalysisReport(analysis_result)
    performAdvancedAnalysis(sample_data)
    print('')
    print('=====================================')
    print('Data processing pipeline completed!')
    print("This demonstrates ML's capabilities for:")
    print('- Complex data structures and manipulation')
    print('- Statistical analysis and computation')
    print('- Grouping, filtering, and aggregation')
    print('- Sorting algorithms and data processing')
    print('- Report generation and formatting')
    print('=====================================')
    return ml_collections.length(sample_data)

def main():
    print('ML Advanced Data Processing Demo')
    print('===============================')
    records_processed = runDataProcessingDemo()
    print('')
    print((str((str('Successfully processed ') + str(records_processed))) + str(' records!')))
    print('Demonstrated advanced ML language features:')
    print('- Object creation and manipulation')
    print('- Array operations and algorithms')
    print('- Mathematical computations')
    print('- Control flow with if/elif/else')
    print('- Function composition and modularity')
    return 0

# End of generated code