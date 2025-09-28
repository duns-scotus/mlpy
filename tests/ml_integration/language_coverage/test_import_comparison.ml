// Test different module imports to see which work
import string;
import collections;
import datetime;

// Test working modules
text = "hello world";
result1 = string.upper(text);
print("String works: " + result1);

arr = [1, 2, 3];
result2 = collections.append(arr, 4);
print("Collections works: " + string.toString(result2.length));

timestamp = datetime.createTimestamp(2024, 1, 1, 0, 0, 0);
print("DateTime works: " + string.toString(timestamp));

print("Working imports completed!");