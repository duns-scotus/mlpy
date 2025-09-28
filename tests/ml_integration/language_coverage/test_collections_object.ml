// Test how collections module works
import collections;
import string;

// Test collections functions
arr = [1, 2, 3];
new_arr = collections.append(arr, 4);
print("Collections append works: " + string.toString(new_arr.length));

print("Collections module access works!");