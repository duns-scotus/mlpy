# ML Debugger Unit Test Plan

Exhaustive list of debugging features requiring unit tests.

## 1. Breakpoint Management

### 1.1 Basic Breakpoint Operations
- [ ] Set breakpoint at valid line
- [ ] Set breakpoint at invalid line (should fail gracefully)
- [ ] Set breakpoint at non-executable line (comment, blank)
- [ ] Set multiple breakpoints in same file
- [ ] Set breakpoints in multiple files
- [ ] Remove breakpoint by ID
- [ ] Remove non-existent breakpoint (should fail gracefully)
- [ ] Clear all breakpoints
- [ ] List all active breakpoints

### 1.2 Conditional Breakpoints
- [ ] Set breakpoint with simple condition (e.g., `x > 10`)
- [ ] Set breakpoint with complex condition (e.g., `arr[i] == target && i > 0`)
- [ ] Conditional breakpoint that evaluates to true (should break)
- [ ] Conditional breakpoint that evaluates to false (should not break)
- [ ] Invalid condition expression (should fail gracefully)
- [ ] Condition with undefined variables (should handle error)

### 1.3 Breakpoint States
- [ ] Enable breakpoint
- [ ] Disable breakpoint
- [ ] Disabled breakpoint should not trigger
- [ ] Re-enable previously disabled breakpoint
- [ ] Verify breakpoint (has valid Python mapping)
- [ ] Pending breakpoint (file not yet loaded)

### 1.4 Breakpoint Hit Counting
- [ ] Track hit count for breakpoint
- [ ] Hit count increments on each hit
- [ ] Hit count with condition (only count when condition is true)
- [ ] Reset hit count
- [ ] Hit count breakpoint (break after N hits)

### 1.5 Breakpoint Source Mapping
- [ ] Breakpoint maps ML line to correct Python line(s)
- [ ] Breakpoint on ML line that maps to multiple Python lines
- [ ] Breakpoint on ML line with no Python mapping (should handle)
- [ ] Breakpoint in nested directory structure
- [ ] Breakpoint with relative file path
- [ ] Breakpoint with absolute file path

## 2. Stepping Operations

### 2.1 Step Over (Next)
- [ ] Step over simple statement
- [ ] Step over function call (should not enter function)
- [ ] Step over in loop (advance to next iteration)
- [ ] Step over at end of function (should return to caller)
- [ ] Step over with no more lines (program ends)
- [ ] Step over multiple times in sequence

### 2.2 Step Into
- [ ] Step into function call
- [ ] Step into recursive function call
- [ ] Step into nested function call (3+ levels deep)
- [ ] Step into builtin function (should skip or handle gracefully)
- [ ] Step into with no function call (acts like step over)
- [ ] Step into lambda/arrow function

### 2.3 Step Out
- [ ] Step out of function (return to caller)
- [ ] Step out of recursive function (return one level)
- [ ] Step out at top level (program ends)
- [ ] Step out with no return statement
- [ ] Step out with exception in function
- [ ] Step out with multiple return paths

### 2.4 Step Depth Tracking
- [ ] Verify call depth increases on function entry
- [ ] Verify call depth decreases on function exit
- [ ] Verify call depth with recursion (increments each call)
- [ ] Verify call depth resets after program ends
- [ ] Step over maintains same depth
- [ ] Step into increases depth
- [ ] Step out decreases depth

### 2.5 Step Edge Cases
- [ ] Step at program start (first executable line)
- [ ] Step at program end (last line)
- [ ] Step in infinite loop (should not hang)
- [ ] Step with exception thrown
- [ ] Step in try-except block
- [ ] Step through conditional branches (if/elif/else)

## 3. Variable Inspection

### 3.1 Local Variables
- [ ] Get local variables at breakpoint
- [ ] Local variable values are correct
- [ ] Local variable appears after assignment
- [ ] Local variable updated after reassignment
- [ ] Local variable in nested scope
- [ ] No local variables in scope (empty dict)

### 3.2 Function Parameters
- [ ] Inspect function parameters
- [ ] Parameters have correct values
- [ ] Parameters with default values
- [ ] Modified parameter values
- [ ] Multiple parameters

### 3.3 Global Variables
- [ ] Get global variables
- [ ] Filter Python internals (__name__, __builtins__, etc.)
- [ ] User-defined globals
- [ ] Module-level variables

### 3.4 Variable Types
- [ ] Inspect number variable
- [ ] Inspect string variable
- [ ] Inspect boolean variable
- [ ] Inspect array variable
- [ ] Inspect object/dict variable
- [ ] Inspect null/None variable
- [ ] Inspect function variable

### 3.5 Complex Variables
- [ ] Inspect nested array (array of arrays)
- [ ] Inspect nested object (object with object properties)
- [ ] Inspect array of objects
- [ ] Inspect object with array properties
- [ ] Inspect large array (100+ elements)
- [ ] Inspect large object (100+ properties)
- [ ] Inspect circular reference (should handle gracefully)

### 3.6 Variable Formatting
- [ ] Format number (integer, float, scientific notation)
- [ ] Format string (with escapes, quotes)
- [ ] Format boolean (true/false)
- [ ] Format array (truncate if too long)
- [ ] Format object (show properties)
- [ ] Format null/undefined

## 4. Call Stack Management

### 4.1 Stack Frame Operations
- [ ] Get call stack
- [ ] Call stack has correct depth
- [ ] Stack frames have correct ML file paths
- [ ] Stack frames have correct ML line numbers
- [ ] Stack frames have correct function names
- [ ] Stack frames ordered correctly (top to bottom)

### 4.2 Stack Navigation
- [ ] Get variables from frame 0 (current)
- [ ] Get variables from frame 1 (caller)
- [ ] Get variables from frame N (N levels up)
- [ ] Navigate stack in recursive function
- [ ] Invalid frame index (should handle gracefully)

### 4.3 Stack Content
- [ ] Top frame shows current function
- [ ] Bottom frame shows main/module level
- [ ] Stack shows intermediate functions
- [ ] Stack frame includes file and line
- [ ] Stack frame includes function name
- [ ] Anonymous function in stack (lambda)

### 4.4 Stack Edge Cases
- [ ] Empty stack (program not running)
- [ ] Single frame (top level)
- [ ] Deep stack (20+ frames)
- [ ] Stack with recursion (repeated function names)

## 5. Expression Evaluation

### 5.1 Basic Expressions
- [ ] Evaluate simple variable (e.g., `x`)
- [ ] Evaluate arithmetic expression (e.g., `x + 5`)
- [ ] Evaluate comparison (e.g., `x > 10`)
- [ ] Evaluate logical expression (e.g., `x > 0 && y < 100`)
- [ ] Evaluate string concatenation
- [ ] Evaluate boolean expression

### 5.2 Variable Access
- [ ] Evaluate local variable
- [ ] Evaluate parameter
- [ ] Evaluate global variable
- [ ] Undefined variable (should report error)
- [ ] Variable in different frame

### 5.3 Complex Expressions
- [ ] Evaluate array access (e.g., `arr[0]`)
- [ ] Evaluate object property (e.g., `obj.name`)
- [ ] Evaluate nested access (e.g., `arr[0].value`)
- [ ] Evaluate function call in expression
- [ ] Evaluate ternary operator
- [ ] Evaluate with parentheses

### 5.4 Expression Evaluation Safety
- [ ] Reject dangerous expressions (eval, exec)
- [ ] Reject system access (os.system)
- [ ] Reject import statements
- [ ] Reject file operations
- [ ] Limit expression complexity
- [ ] Timeout long-running expressions

### 5.5 Expression Errors
- [ ] Syntax error in expression
- [ ] Runtime error in expression (e.g., division by zero)
- [ ] Type error in expression
- [ ] Index out of bounds
- [ ] Null pointer access
- [ ] Circular reference in expression

## 6. Source Map Functionality

### 6.1 ML to Python Mapping
- [ ] Map ML line to Python line
- [ ] Map ML line to multiple Python lines
- [ ] Map ML line in nested directory
- [ ] ML line with no Python mapping (comment, blank)
- [ ] Invalid ML line number
- [ ] ML file not in source map

### 6.2 Python to ML Mapping
- [ ] Map Python line to ML line
- [ ] Map Python line to ML position (file, line, column)
- [ ] Generated Python line (no ML source)
- [ ] Invalid Python line number
- [ ] Python file not in source map

### 6.3 Source Map Loading
- [ ] Load source map from file (.py.map)
- [ ] Parse JSON source map format
- [ ] Parse enhanced source map format
- [ ] Invalid source map JSON (should handle gracefully)
- [ ] Missing source map file (should handle gracefully)
- [ ] Corrupted source map file

### 6.4 Source Map Caching
- [ ] Source map loaded once per file
- [ ] Source map reused on subsequent loads
- [ ] Source map updated when file changes
- [ ] Cache invalidation when source changes
- [ ] Multiple source maps for multiple files

### 6.5 Source Map Index
- [ ] Build index from source map
- [ ] Index ML line lookups (fast O(1) access)
- [ ] Index Python line lookups
- [ ] Index with multiple ML files
- [ ] Index with nested directory structure

## 7. Exception Handling

### 7.1 Exception Breakpoints
- [ ] Break on all exceptions
- [ ] Break on uncaught exceptions only
- [ ] Don't break on caught exceptions (try-except)
- [ ] Exception breakpoint shows exception info
- [ ] Exception breakpoint shows stack trace

### 7.2 Exception Information
- [ ] Get exception type
- [ ] Get exception message
- [ ] Get exception stack trace
- [ ] Map exception stack to ML source
- [ ] Show variables at exception point

### 7.3 Exception Edge Cases
- [ ] Exception in main code
- [ ] Exception in function
- [ ] Exception in recursive function
- [ ] Exception in loop
- [ ] Exception in try-except-finally

## 8. Debug State Management

### 8.1 Debugger Lifecycle
- [ ] Start debugger
- [ ] Stop debugger
- [ ] Restart debugger
- [ ] Multiple start/stop cycles
- [ ] Clean up on stop

### 8.2 Execution State
- [ ] Program not started (initial state)
- [ ] Program running
- [ ] Program paused at breakpoint
- [ ] Program paused after step
- [ ] Program completed
- [ ] Program terminated with error

### 8.3 State Transitions
- [ ] Transition from stopped to running
- [ ] Transition from running to paused
- [ ] Transition from paused to running (continue)
- [ ] Transition from paused to running (step)
- [ ] Invalid state transitions (should be rejected)

### 8.4 Trace Function
- [ ] Trace function installed on start
- [ ] Trace function called on every line
- [ ] Trace function called on function entry (call event)
- [ ] Trace function called on function exit (return event)
- [ ] Trace function called on exception
- [ ] Trace function removed on stop
- [ ] Trace function performance (should be fast)

## 9. Multi-File Debugging

### 9.1 Multiple Files
- [ ] Debug program with multiple ML files
- [ ] Set breakpoints in different files
- [ ] Step between files (function calls)
- [ ] Stack trace shows multiple files
- [ ] Source maps for all files loaded

### 9.2 Module Structure
- [ ] Debug in nested directory structure
- [ ] Debug with relative imports
- [ ] Debug with absolute imports
- [ ] Debug main file importing modules

### 9.3 File Path Handling
- [ ] Handle absolute file paths
- [ ] Handle relative file paths
- [ ] Handle Windows paths (backslashes)
- [ ] Handle Unix paths (forward slashes)
- [ ] Normalize paths correctly
- [ ] Case-sensitive vs case-insensitive paths

## 10. Integration with DAP Server

### 10.1 DAP Protocol Messages
- [ ] Initialize request/response
- [ ] Launch request/response
- [ ] SetBreakpoints request/response
- [ ] Continue request/response
- [ ] Next request/response
- [ ] StepIn request/response
- [ ] StepOut request/response
- [ ] StackTrace request/response
- [ ] Scopes request/response
- [ ] Variables request/response
- [ ] Evaluate request/response
- [ ] Disconnect request/response

### 10.2 DAP Events
- [ ] Stopped event (breakpoint)
- [ ] Stopped event (step)
- [ ] Stopped event (exception)
- [ ] Continued event
- [ ] Terminated event
- [ ] Output event (stdout)
- [ ] Output event (stderr)

### 10.3 DAP State Synchronization
- [ ] Debugger state matches DAP state
- [ ] Breakpoint IDs consistent
- [ ] Thread IDs consistent
- [ ] Frame IDs consistent
- [ ] Variable references consistent

## 11. Performance

### 11.1 Performance Benchmarks
- [ ] Breakpoint hit latency < 10ms
- [ ] Step operation latency < 5ms
- [ ] Variable inspection < 5ms
- [ ] Source map lookup < 1ms
- [ ] Expression evaluation < 10ms

### 11.2 Scalability
- [ ] Debug large program (1000+ lines)
- [ ] Debug program with many functions (100+)
- [ ] Debug with many breakpoints (50+)
- [ ] Debug with deep recursion (100+ levels)
- [ ] Debug with large arrays (10000+ elements)

### 11.3 Memory Usage
- [ ] Debugger memory overhead < 10MB
- [ ] Source map memory reasonable
- [ ] No memory leaks on multiple runs
- [ ] Clean up resources on stop

## 12. Error Handling and Edge Cases

### 12.1 File Errors
- [ ] ML file not found
- [ ] ML file cannot be read (permissions)
- [ ] ML file is empty
- [ ] ML file has syntax errors
- [ ] Python file cannot be written
- [ ] Source map cannot be written

### 12.2 Transpilation Errors
- [ ] Transpilation fails (syntax error)
- [ ] Transpilation fails (semantic error)
- [ ] Transpilation timeout
- [ ] Security issues detected
- [ ] Handle gracefully, report error

### 12.3 Runtime Errors
- [ ] Null pointer access
- [ ] Division by zero
- [ ] Index out of bounds
- [ ] Stack overflow (deep recursion)
- [ ] Infinite loop (timeout)
- [ ] Out of memory

### 12.4 Debugger Errors
- [ ] Breakpoint at invalid location
- [ ] Step when program not running
- [ ] Get variables when no frame
- [ ] Evaluate expression in invalid context
- [ ] All errors handled gracefully, not crash

## 13. Special Language Features

### 13.1 Control Flow
- [ ] Debug if statement
- [ ] Debug elif chain
- [ ] Debug else branch
- [ ] Debug while loop
- [ ] Debug for loop
- [ ] Debug nested loops
- [ ] Debug break statement
- [ ] Debug continue statement

### 13.2 Functions
- [ ] Debug function definition
- [ ] Debug function call
- [ ] Debug function return
- [ ] Debug recursive function
- [ ] Debug nested function calls
- [ ] Debug function with no return
- [ ] Debug function with multiple returns

### 13.3 Data Structures
- [ ] Debug array creation
- [ ] Debug array access
- [ ] Debug array mutation
- [ ] Debug object creation
- [ ] Debug object property access
- [ ] Debug object property mutation
- [ ] Debug nested structures

### 13.4 Advanced Features
- [ ] Debug try-except block
- [ ] Debug try-except-finally
- [ ] Debug throw statement
- [ ] Debug nonlocal statement
- [ ] Debug arrow functions (if supported)
- [ ] Debug destructuring (if supported)

## 14. User Experience

### 14.1 Debugging Session Flow
- [ ] Complete workflow: load → breakpoint → run → hit → inspect → step → continue → finish
- [ ] Multiple debugging sessions in sequence
- [ ] Restart program during debug
- [ ] Change breakpoints during debug
- [ ] Evaluate expressions during debug

### 14.2 Debugging Information Quality
- [ ] Error messages are clear and helpful
- [ ] Stack traces are readable
- [ ] Variable formatting is user-friendly
- [ ] File paths are correct and readable
- [ ] Function names are accurate

### 14.3 Robustness
- [ ] Debugger doesn't crash on any input
- [ ] Graceful degradation on errors
- [ ] Recover from exceptions
- [ ] Clean state after errors
- [ ] Safe to reuse handler after errors

---

## Test Statistics

**Total test categories**: 14
**Total test subcategories**: 71
**Total individual test cases**: 300+

## Priority Levels

### P0 - Critical (Must Have)
- Basic breakpoint operations
- Step over/into/out
- Variable inspection (local variables)
- Call stack management
- Source map ML→Python mapping
- Error handling (graceful failures)

### P1 - High Priority
- Conditional breakpoints
- Expression evaluation
- Exception handling
- Multi-file debugging
- DAP protocol integration
- Performance benchmarks

### P2 - Medium Priority
- Breakpoint hit counting
- Complex variable inspection
- Stack navigation
- Python→ML mapping
- Source map caching
- Edge cases

### P3 - Nice to Have
- Advanced expression evaluation safety
- Deep performance optimization tests
- Extreme edge cases
- User experience validation tests

## Implementation Approach

1. **Phase 1**: Implement P0 tests (core functionality)
2. **Phase 2**: Implement P1 tests (advanced features)
3. **Phase 3**: Implement P2 tests (completeness)
4. **Phase 4**: Implement P3 tests (polish)

Each phase should achieve >95% pass rate before moving to next phase.

## Test Framework

All tests will use:
- **Handler**: `DebugTestHandler` class
- **Test Files**: `tests/ml_integration/ml_debug/*.ml`
- **Framework**: Python `unittest` or `pytest`
- **Assertions**: Standard assert statements
- **Coverage**: Track with `pytest-cov` or similar

## Expected Outcomes

- Comprehensive test coverage (>95%)
- All critical debugger features validated
- Confidence in debugger reliability
- Foundation for regression testing
- Documentation of expected behavior
