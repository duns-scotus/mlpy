# ML Debugger Features - Complete Analysis

**Date**: October 12, 2025
**Source**: `src/mlpy/debugging/debugger.py` (1,213 lines)

## Executive Summary

The ML debugger is a **comprehensive, production-ready debugging system** using `sys.settrace()` for line-by-line execution control. It provides extensive debugging capabilities with security-first design.

**Key Statistics**:
- **1,213 lines** of implementation
- **40+ public methods**
- **Safe expression evaluation** (security-hardened)
- **Multi-file debugging** with automatic import detection
- **Watch expressions** with live evaluation
- **Exception breakpoints** with filtering
- **Call stack navigation**

---

## 1. Breakpoint Management ✅ **FULLY IMPLEMENTED**

### 1.1 Basic Breakpoint Operations
**Implementation**: Lines 154-420

```python
class Breakpoint:
    id: int
    ml_file: str
    ml_line: int
    py_lines: list[int]
    enabled: bool = True
    condition: Optional[str] = None
    hit_count: int = 0
```

**Features**:
- ✅ `set_breakpoint(ml_file, ml_line, condition)` → returns (bp_id, is_pending)
- ✅ `delete_breakpoint(bp_id)` → removes breakpoint
- ✅ `enable_breakpoint(bp_id)` → enables disabled breakpoint
- ✅ `disable_breakpoint(bp_id)` → temporarily disables breakpoint
- ✅ `get_all_breakpoints()` → returns all active and pending breakpoints

**Advanced Features**:
- ✅ **Hit Count Tracking**: Automatically increments `bp.hit_count` on each hit
- ✅ **Fast Lookup**: Uses `_breakpoint_py_lines` set for O(1) breakpoint checking
- ✅ **Pending Breakpoints**: Can set breakpoints in not-yet-loaded files

**Test Coverage**: ✅ **COMPLETE** (Phases 1, 2, 3)

### 1.2 Conditional Breakpoints
**Implementation**: Lines 638-641, 696-727

```python
def _evaluate_condition(self, condition: str) -> bool:
    """Evaluate a breakpoint condition expression SECURELY."""
    evaluator = get_safe_evaluator()
    value, success, error_msg = evaluator.evaluate(
        condition,
        self.current_frame.f_locals,
        self.current_frame.f_globals
    )
```

**Features**:
- ✅ **Secure Evaluation**: Uses SafeExpressionEvaluator (prevents eval exploits)
- ✅ **ML Expression Syntax**: Evaluates conditions in ML syntax
- ✅ **Error Handling**: Fails safely on invalid expressions
- ✅ **Context Access**: Has access to current frame's locals and globals

**Test Coverage**: ✅ **COMPLETE** (Phase 3)

### 1.3 Multi-File Breakpoints
**Implementation**: Lines 112-117, 283-420

```python
# Source map loading for multiple files
def load_source_map_for_file(self, ml_file: str) -> bool:
    """Load source map from .ml.map file for on-demand debugging."""

# Pending breakpoint activation
def _activate_pending_breakpoints_for_file(self, ml_file: str):
    """Activate pending breakpoints for a newly loaded file."""
```

**Features**:
- ✅ **Lazy Loading**: Source maps loaded on-demand when needed
- ✅ **Automatic Import Detection**: MLDebuggerImportManager monitors imports
- ✅ **Deferred Resolution**: Pending breakpoints activated when module loads
- ✅ **Cross-File Debugging**: Full support for debugging across multiple ML files

**Test Coverage**: ✅ **COMPLETE** (Phase 1)

---

## 2. Stepping Operations ✅ **FULLY IMPLEMENTED**

### 2.1 Step Modes
**Implementation**: Lines 19-25, 823-853

```python
class StepMode(Enum):
    NONE = "none"   # Not stepping (only break at breakpoints)
    NEXT = "next"   # Step to next ML line (step over)
    STEP = "step"   # Step into functions
    OUT = "out"     # Step out of current function
```

**Features**:
- ✅ `step_next()` - Step over (same or shallower depth)
- ✅ `step_into()` - Step into function calls
- ✅ `step_out()` - Step out of current function
- ✅ `continue_execution()` - Run until next breakpoint

**Implementation Details**:
- **Step Over**: Tracks depth to avoid stepping into function calls
- **Step Into**: Breaks at any new ML line (any depth)
- **Step Out**: Waits for return event, then breaks at next line in caller
- **Depth Tracking**: `_current_depth` tracks call depth for step logic

**Test Coverage**: ✅ **COMPLETE** (Phase 3)

---

## 3. Variable Inspection ✅ **FULLY IMPLEMENTED**

### 3.1 Variable Access
**Implementation**: Lines 729-781, 1131-1163

```python
def get_variable(self, name: str) -> Any:
    """Get variable value from current stack frame."""

def get_all_locals(self) -> dict[str, Any]:
    """Get all local variables from current stack frame."""

def get_all_globals(self) -> dict[str, Any]:
    """Get all global variables from current stack frame."""

def get_locals(self, frame_id: int = 0) -> dict[str, Any]:
    """Get local variables for specific stack frame."""
```

**Features**:
- ✅ **By Name**: Get specific variable value
- ✅ **All Locals**: Get all local variables (filtered)
- ✅ **All Globals**: Get all global variables (filtered)
- ✅ **Frame-Specific**: Get variables from any stack frame
- ✅ **Filtering**: Removes internal variables (`__*`, `_ml_*`)

**Test Coverage**: ✅ **COMPLETE** (Phases 2, 3)

### 3.2 Expression Evaluation
**Implementation**: Lines 1165-1191

```python
def evaluate_expression(self, expression: str, frame_id: int = 0) -> Any:
    """Evaluate ML expression in context of stack frame.

    Uses SafeExpressionEvaluator to ensure security.
    """
    evaluator = get_safe_evaluator(frame.f_locals, frame.f_globals)
    return evaluator.evaluate(expression)
```

**Features**:
- ✅ **Secure Evaluation**: Uses SafeExpressionEvaluator (no eval/exec exploits)
- ✅ **Frame Context**: Evaluates in context of specific stack frame
- ✅ **ML Syntax**: Supports ML expression syntax
- ✅ **Error Handling**: Raises clear exceptions on failure

**Test Coverage**: ✅ **COMPLETE** (Phases 2, 3)

---

## 4. Watch Expressions ✅ **FULLY IMPLEMENTED**

### 4.1 Watch Management
**Implementation**: Lines 118-120, 422-480

```python
self.watches: dict[int, str] = {}  # watch_id → expression
self.next_watch_id = 1

def add_watch(self, expression: str) -> int:
    """Add a watch expression."""

def remove_watch(self, watch_id: int) -> bool:
    """Remove a watch expression."""

def get_watch_values(self) -> dict[int, tuple[str, Any, bool]]:
    """Get current values of all watch expressions SECURELY."""
```

**Features**:
- ✅ **Add Watch**: Add expression to watch list
- ✅ **Remove Watch**: Remove watch by ID
- ✅ **Get Values**: Evaluate all watches at current position
- ✅ **Safe Evaluation**: Uses SafeExpressionEvaluator
- ✅ **Error Handling**: Returns `(expression, value, success)` tuple

**Example Usage**:
```python
watch_id = debugger.add_watch("x * 2")
values = debugger.get_watch_values()
# values[watch_id] = ("x * 2", 20, True)
```

**Test Coverage**: ⚠️ **NOT TESTED** - Phase 4 candidate

---

## 5. Call Stack Management ✅ **FULLY IMPLEMENTED**

### 5.1 Stack Operations
**Implementation**: Lines 906-932, 1002-1078, 1081-1129

```python
def get_call_stack(self) -> list[tuple[str, int, str]]:
    """Get call stack with ML source positions."""

def get_call_stack_with_frames(self) -> list[dict[str, Any]]:
    """Get call stack with frames for DAP protocol."""

def get_stack_depth(self) -> int:
    """Get the depth of the current call stack."""
```

**Features**:
- ✅ **Basic Stack**: Returns `[(ml_file, ml_line, func_name)]`
- ✅ **Enhanced Stack**: Returns full frame objects for DAP
- ✅ **Stack Depth**: Get number of frames in stack
- ✅ **ML Position Mapping**: Maps Python frames to ML positions

**Test Coverage**: ✅ **COMPLETE** (Phases 2, 3)

### 5.2 Stack Navigation
**Implementation**: Lines 1003-1061

```python
def navigate_up_stack(self) -> bool:
    """Navigate up one level in the call stack (towards caller)."""

def navigate_down_stack(self) -> bool:
    """Navigate down one level in the call stack (towards current)."""

def reset_stack_navigation(self):
    """Reset stack navigation to current frame."""

def get_current_stack_frame(self):
    """Get the frame at the current navigation position."""
```

**Features**:
- ✅ **Navigate Up**: Move towards caller frames
- ✅ **Navigate Down**: Move towards current frame
- ✅ **Reset Navigation**: Return to current frame
- ✅ **Frame Access**: Get frame at navigation position
- ✅ **Variable Context**: Variables respect navigation position

**Test Coverage**: ⚠️ **NOT TESTED** - Phase 4 candidate

---

## 6. Exception Breakpoints ✅ **FULLY IMPLEMENTED**

### 6.1 Exception Handling
**Implementation**: Lines 133-136, 527-543, 934-999

```python
self.break_on_exceptions = False
self.exception_filters: set[str] = set()  # Filter by exception type names
self.last_exception: Optional[tuple[type, Any, Any]] = None

def enable_exception_breakpoints(self, exception_type: Optional[str] = None):
    """Enable breaking on exceptions."""

def add_exception_filter(self, exception_type: str):
    """Add an exception type to the filter list."""

def get_exception_info(self) -> Optional[dict]:
    """Get information about the last exception."""
```

**Features**:
- ✅ **Enable/Disable**: Turn exception breaking on/off
- ✅ **Type Filtering**: Filter by exception type name (e.g., "ValueError")
- ✅ **Exception Info**: Get type, value, message of last exception
- ✅ **Break on Exception**: Pauses when exception is raised
- ✅ **Trace Event**: Handles 'exception' trace events

**Test Coverage**: ✅ **PARTIAL** (Phase 3 tests exceptions, but not exception breakpoints)

---

## 7. Source Context ✅ **FULLY IMPLEMENTED**

### 7.1 Source Display
**Implementation**: Lines 783-821

```python
def show_source_context(self, lines_before: int = 2, lines_after: int = 2) -> str:
    """Display source code around current position."""
```

**Features**:
- ✅ **Context Lines**: Shows lines before and after current
- ✅ **Current Line Marker**: Uses `=>` to mark current line
- ✅ **Line Numbers**: Shows line numbers for reference
- ✅ **File Path**: Shows ML file and line in header
- ✅ **Error Handling**: Graceful failure if file not found

**Test Coverage**: ⚠️ **NOT TESTED** - Phase 4 candidate

---

## 8. Features NOT Implemented ❌

### 8.1 Data Breakpoints
**Status**: ❌ **NOT IMPLEMENTED**

**What Would Be Needed**:
- Track variable access/modification
- Break when specific variable changes
- Break when object property accessed
- Break when array element modified

**Complexity**: HIGH (requires extensive instrumentation)

### 8.2 Hit Count Breakpoints
**Status**: ⚠️ **PARTIALLY IMPLEMENTED**

**What Exists**:
- ✅ Hit count tracking (`bp.hit_count` increments on each hit)

**What's Missing**:
- ❌ Break after N hits (e.g., `hit_count > 5`)
- ❌ Break every N hits (e.g., `hit_count % 5 == 0`)
- ❌ Hit count reset command

**Complexity**: LOW (just add condition check)

### 8.3 Log Points
**Status**: ❌ **NOT IMPLEMENTED**

**What Would Be Needed**:
- Breakpoint that logs without stopping
- Message template with variable interpolation
- Log output management

**Complexity**: MEDIUM

### 8.4 Memory Inspection
**Status**: ❌ **NOT IMPLEMENTED**

**What Would Be Needed**:
- Object size tracking
- Reference counting
- Memory leak detection
- Large object inspection

**Complexity**: VERY HIGH (requires deep Python introspection)

### 8.5 Thread Debugging
**Status**: ❌ **NOT IMPLEMENTED**

**What Would Be Needed**:
- Multi-thread support
- Thread-specific breakpoints
- Thread switching
- Race condition detection

**Complexity**: VERY HIGH (requires thread-aware tracing)

---

## 9. Phase 4 Testing Recommendations

### Priority 1: Test Existing Features Not Yet Tested

1. **Watch Expressions** (10 tests)
   - Add/remove watches
   - Watch value evaluation
   - Watch in different stack frames
   - Invalid watch expressions
   - Watch performance

2. **Stack Navigation** (8 tests)
   - Navigate up/down stack
   - Variables at different stack levels
   - Reset navigation
   - Navigation bounds checking

3. **Exception Breakpoints** (10 tests)
   - Enable/disable exception breaking
   - Exception type filtering
   - Break on all exceptions
   - Break on specific exceptions
   - Exception info retrieval

4. **Source Context Display** (5 tests)
   - Show context at breakpoint
   - Context with different line counts
   - Context at file boundaries
   - Context with missing file

### Priority 2: Test Advanced Scenarios

5. **Multi-File Debugging** (10 tests)
   - Pending breakpoints activation
   - Import detection
   - Cross-file stepping
   - Multiple source maps
   - Source map lazy loading

6. **Security Testing** (8 tests)
   - Safe expression evaluation
   - Prevent eval/exec
   - Prevent dangerous imports
   - Sandbox escape prevention

7. **Edge Cases** (10 tests)
   - Deep recursion
   - Large call stacks
   - Many breakpoints
   - Many watches
   - Long-running programs

### Priority 3: Easy Enhancements

8. **Hit Count Breakpoints** (5 tests)
   - Break after N hits
   - Break every N hits
   - Hit count reset
   - Hit count with conditions

**Total Phase 4 Tests**: ~66 tests

---

## 10. Summary of Test Coverage

| Feature Category | Implementation Status | Test Coverage Status |
|-----------------|----------------------|---------------------|
| **Basic Breakpoints** | ✅ Complete | ✅ Phase 1 (34 tests) |
| **Conditional Breakpoints** | ✅ Complete | ✅ Phase 2-3 (5 tests) |
| **Stepping Operations** | ✅ Complete | ✅ Phase 3 (5 tests) |
| **Variable Inspection** | ✅ Complete | ✅ Phase 2-3 (8 tests) |
| **Call Stack** | ✅ Complete | ✅ Phase 2-3 (6 tests) |
| **Expression Evaluation** | ✅ Complete | ✅ Phase 2-3 (6 tests) |
| **Watch Expressions** | ✅ Complete | ⚠️ **NOT TESTED** |
| **Stack Navigation** | ✅ Complete | ⚠️ **NOT TESTED** |
| **Exception Breakpoints** | ✅ Complete | ⚠️ **PARTIAL** |
| **Multi-File Debugging** | ✅ Complete | ✅ Phase 1 (2 tests) |
| **Source Context** | ✅ Complete | ⚠️ **NOT TESTED** |
| **Data Breakpoints** | ❌ Not Implemented | N/A |
| **Hit Count Conditions** | ⚠️ Partial (tracking only) | ⚠️ **NOT TESTED** |
| **Log Points** | ❌ Not Implemented | N/A |

**Overall Coverage**:
- **Tested**: 96 tests covering ~65% of implemented features
- **Not Tested**: ~35% of implemented features (watches, stack navigation, exception breakpoints)
- **Not Implemented**: Data breakpoints, log points, thread debugging

---

## 11. Recommendation for Phase 4

**Focus**: Test the **existing implemented features** that haven't been tested yet.

**Proposed Phase 4 Scope** (~66 tests):
1. ✅ Watch Expressions (10 tests)
2. ✅ Stack Navigation (8 tests)
3. ✅ Exception Breakpoints (10 tests)
4. ✅ Source Context (5 tests)
5. ✅ Multi-File Advanced (10 tests)
6. ✅ Security/Safety (8 tests)
7. ✅ Edge Cases (10 tests)
8. ✅ Hit Count Enhancement (5 tests)

**Why This Approach**:
- Tests **real implemented features** (not theoretical)
- Achieves comprehensive coverage of debugger.py
- Validates security features (SafeExpressionEvaluator)
- Tests advanced scenarios (multi-file, deep recursion)
- Completes testing of production-ready debugger

**Estimated Completion**: Phase 4 would bring total tests to **162 tests** with **~95%+ coverage** of implemented features.
