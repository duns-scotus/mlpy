// Comprehensive slicing test - compare ML with Python
arr = [10, 20, 30, 40, 50];

// Basic positive slicing
case1 = arr[1:4];      // Expected: [20, 30, 40]
case2 = arr[0:3];      // Expected: [10, 20, 30]
case3 = arr[2:5];      // Expected: [30, 40, 50]

// Open-ended slicing
case4 = arr[:3];       // Expected: [10, 20, 30]
case5 = arr[2:];       // Expected: [30, 40, 50]
case6 = arr[:];        // Expected: [10, 20, 30, 40, 50]

// Negative indices
case7 = arr[-1:];      // Expected: [50] (last element)
case8 = arr[-2:];      // Expected: [40, 50] (last 2)
case9 = arr[-3:];      // Expected: [30, 40, 50] (last 3)
case10 = arr[:-1];     // Expected: [10, 20, 30, 40] (all but last)
case11 = arr[:-2];     // Expected: [10, 20, 30] (all but last 2)

// Negative start and end
case12 = arr[-3:-1];   // Expected: [30, 40] (from -3 to -1)
case13 = arr[-4:-2];   // Expected: [20, 30] (from -4 to -2)

// Step slicing
case14 = arr[::2];     // Expected: [10, 30, 50] (every 2nd)
case15 = arr[::3];     // Expected: [10, 40] (every 3rd)
case16 = arr[1::2];    // Expected: [20, 40] (from index 1, every 2nd)

// Reverse slicing
case17 = arr[::-1];    // Expected: [50, 40, 30, 20, 10] (reverse)
case18 = arr[::-2];    // Expected: [50, 30, 10] (reverse, every 2nd)

// Mixed negative indices and step
case19 = arr[-1::-1];  // Expected: [50, 40, 30, 20, 10] (from last, reverse)
case20 = arr[-2::-1];  // Expected: [40, 30, 20, 10] (from -2, reverse)

// Edge cases
case21 = arr[10:];     // Expected: [] (out of bounds)
case22 = arr[3:1];     // Expected: [] (start > end)
case23 = arr[0:0];     // Expected: [] (empty slice)
case24 = arr[5:10];    // Expected: [] (both out of bounds)

result = {
    case1: case1, case2: case2, case3: case3,
    case4: case4, case5: case5, case6: case6,
    case7: case7, case8: case8, case9: case9,
    case10: case10, case11: case11,
    case12: case12, case13: case13,
    case14: case14, case15: case15, case16: case16,
    case17: case17, case18: case18,
    case19: case19, case20: case20,
    case21: case21, case22: case22, case23: case23, case24: case24
};
