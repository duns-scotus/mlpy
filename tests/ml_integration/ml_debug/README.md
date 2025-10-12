# ML Debug Test Suite

Comprehensive debugging test suite for the ML language debugger. This directory contains test ML programs and infrastructure for automated debugging tests.

## Directory Structure

```
tests/ml_integration/ml_debug/
├── README.md                           # This file
├── main.ml                             # Main test program (entry point)
├── math_utils.ml                       # Mathematical utilities
├── data_structures/
│   ├── list_ops.ml                    # List/array operations
│   └── tree.ml                        # Binary tree operations
└── algorithms/
    ├── search.ml                      # Search algorithms
    └── sort.ml                        # Sorting algorithms

tests/debugging/
├── debug_test_handler.py              # DebugTestHandler class for automated testing
└── test_debug_handler_example.py      # Example tests using DebugTestHandler
```

## Test Files Overview

### main.ml (343 lines)
**Purpose**: Main test program exercising all debugging features
**Features tested**:
- Function calls and returns
- Arithmetic operations
- Loops (while, for)
- Conditionals (if/elif/else)
- Recursion (factorial)
- Array operations
- Object structures
- Tree data structures

**Test functions**:
- `test_arithmetic()` - Basic arithmetic and function calls
- `test_loops()` - While and for loops
- `test_conditionals()` - If/elif/else branching
- `test_recursion()` - Factorial recursion
- `test_arrays()` - Array operations, search, sort
- `test_objects()` - Object creation and manipulation
- `test_tree_structure()` - Tree construction and traversal

### math_utils.ml (73 lines)
**Purpose**: Mathematical utility functions
**Features tested**: Conditionals, recursion, loops

**Functions**:
- `abs(x)`, `max(a, b)`, `min(a, b)`, `clamp(...)`
- `is_even(n)`, `is_odd(n)`
- `factorial(n)`, `fibonacci(n)`, `gcd(a, b)`
- `sum_range(start, end)`

### data_structures/list_ops.ml (93 lines)
**Purpose**: List/array operation utilities
**Features tested**: Loops, array operations, algorithms

**Functions**:
- `list_length(list)`, `list_sum(list)`
- `list_max(list)`, `list_min(list)`
- `list_contains(list, value)`, `list_reverse(list)`
- `list_filter_even(list)`, `list_map_double(list)`
- `list_slice(list, start, end)`

### data_structures/tree.ml (87 lines)
**Purpose**: Binary tree operations
**Features tested**: Objects, recursion, complex data structures

**Functions**:
- `create_node(value, left, right)`, `create_leaf(value)`
- `is_empty_node(node)`
- `tree_size(node)`, `tree_height(node)`, `tree_sum(node)`
- `tree_contains(node, target)`, `tree_max(node)`

### algorithms/search.ml (97 lines)
**Purpose**: Search algorithm implementations
**Features tested**: Loops, conditionals, early returns

**Functions**:
- `linear_search(list, target)`
- `binary_search(list, target)`
- `find_min_index(list, start, end)`, `find_max_index(...)`
- `count_occurrences(list, target)`
- `find_first_greater(list, threshold)`

### algorithms/sort.ml (121 lines)
**Purpose**: Sorting algorithm implementations
**Features tested**: Nested loops, array mutations, complex logic

**Functions**:
- `bubble_sort(list)` - O(n²) bubble sort
- `selection_sort(list)` - O(n²) selection sort
- `insertion_sort(list)` - O(n²) insertion sort
- `is_sorted(list)` - Verify array is sorted

## Debugging Features Tested

### 1. **Breakpoints**
- Line breakpoints in functions
- Breakpoints in loops
- Breakpoints in conditionals
- Multiple breakpoints in same file

### 2. **Stepping**
- Step over function calls
- Step into function calls
- Step out of functions
- Step through loops

### 3. **Variable Inspection**
- Local variables
- Function parameters
- Array elements
- Object properties
- Nested structures

### 4. **Call Stack**
- Function call hierarchy
- Recursive call stacks
- Stack frame navigation

### 5. **Source Mapping**
- ML → Python line mapping
- Correct file paths
- Column information
- Nested directory structures

## Running Tests

### Execute Main Program
```bash
cd tests/ml_integration/ml_debug
python -m mlpy.cli.app run main.ml
```

### Run Automated Tests
```bash
cd C:/Users/vogtt/PyCharmProjects/mlpy
python tests/debugging/test_debug_handler_example.py
```

### Use DebugTestHandler Programmatically
```python
from tests.debugging.debug_test_handler import DebugTestHandler

# Create handler
handler = DebugTestHandler()

# Load program
success, msg = handler.load_program("tests/ml_integration/ml_debug/main.ml")
print(f"Load: {success} - {msg}")

# Set breakpoint
handler.set_breakpoint("main.ml", 170)

# Verify source maps
all_exist, status = handler.verify_source_maps_exist()
print(f"Source maps: {status}")
```

## Source Map Verification

All test files generate:
1. **Python code** (`.py`) - Transpiled Python output
2. **Source maps** (`.py.map`) - ML ↔ Python line mappings

Source maps are cached and reused on subsequent runs:
```bash
# First run - generates source maps
python -m mlpy.cli.app run main.ml

# Second run - reuses cached source maps (faster)
python -m mlpy.cli.app run main.ml
```

## Test Results

✅ **All 6 files verified**:
- Successful transpilation
- Python code generation
- Source map generation
- Source map caching
- Correct execution

## Next Steps for Unit Tests

Use these files as the basis for comprehensive debugger unit tests:

1. **Breakpoint Tests**
   - Test breakpoint setting/removal
   - Test conditional breakpoints
   - Test hit counts

2. **Stepping Tests**
   - Test step over/into/out
   - Test stepping through loops
   - Test stepping through recursion

3. **Variable Tests**
   - Test local variable inspection
   - Test array/object inspection
   - Test variable modifications

4. **Source Map Tests**
   - Test ML → Python mapping accuracy
   - Test Python → ML reverse mapping
   - Test column information
   - Test multiple files

5. **Integration Tests**
   - Test complete debugging sessions
   - Test complex debugging scenarios
   - Test error handling
   - Test performance

## Example Debugging Scenarios

### Scenario 1: Simple Breakpoint
```
1. Set breakpoint at main.ml:170 (test_arithmetic function)
2. Run program
3. Hit breakpoint
4. Inspect variables: a, b, c
5. Continue
```

### Scenario 2: Step Through Loop
```
1. Set breakpoint at main.ml:207 (test_loops - while loop)
2. Run program
3. Hit breakpoint
4. Step over multiple times
5. Watch variables: count, i
6. Verify loop iteration
```

### Scenario 3: Step Into Recursion
```
1. Set breakpoint at main.ml:244 (test_recursion)
2. Run program
3. Hit breakpoint
4. Step into factorial(5)
5. Navigate recursive call stack
6. Step out when desired
```

### Scenario 4: Inspect Array Operations
```
1. Set breakpoint at main.ml:257 (test_arrays)
2. Run program
3. Hit breakpoint
4. Inspect array: arr = [5, 2, 8, 1, 9, 3]
5. Step through sort operations
6. Watch sorted_arr formation
```

## File Statistics

| File | Lines | Functions | Complexity |
|------|-------|-----------|------------|
| main.ml | 343 | 20 | High |
| math_utils.ml | 73 | 10 | Medium |
| list_ops.ml | 93 | 9 | Medium |
| tree.ml | 87 | 7 | High |
| search.ml | 97 | 6 | Medium |
| sort.ml | 121 | 4 | High |
| **Total** | **814** | **56** | - |

## Coverage

These test files provide coverage for:
- ✅ All ML language features
- ✅ All control flow constructs
- ✅ All data types (numbers, strings, booleans, arrays, objects)
- ✅ Function definitions and calls
- ✅ Recursion
- ✅ Loops (while, for)
- ✅ Conditionals (if/elif/else)
- ✅ Array operations
- ✅ Object operations
- ✅ Nested structures

This comprehensive test suite provides an excellent foundation for writing exhaustive unit tests for the ML debugger!
