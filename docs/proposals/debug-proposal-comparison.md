# Debug Proposal Comparison: Original vs Revised

## TL;DR

**Original Proposal:** AST instrumentation approach (25 days)
**Revised Proposal:** sys.settrace() approach (18 days, simpler, zero production overhead)

**Recommendation:** Use revised proposal with sys.settrace() + cProfile

---

## Key Changes

### 1. Core Technology Shift

| Aspect | Original (AST) | Revised (settrace) |
|--------|----------------|-------------------|
| **Mechanism** | Inject debug hooks into generated Python | Use Python's sys.settrace() |
| **Code Changes** | Modify transpiler output | No code modification |
| **Implementation** | 500-800 LOC | 200-300 LOC |
| **Complexity** | High (AST transformation) | Low (trace callbacks) |

### 2. Performance Profile

| Mode | Original (AST) | Revised (settrace) |
|------|----------------|-------------------|
| **Production** | 1-3% overhead OR dual build | 0% overhead ✅ |
| **Debugging** | 2-5% overhead | 10-15% overhead |
| **Decision** | Accept overhead OR maintain 2 builds | Pay only when debugging ✅ |

**Key Insight:** The revised approach has ZERO overhead when not debugging because you just don't call `sys.settrace()`. Same Python code runs at full speed!

### 3. Implementation Timeline

| Phase | Original | Revised | Difference |
|-------|----------|---------|------------|
| Source Mapping | 3 days | 2 days | -1 (Sprint 7 done) |
| CLI Debugger | 4 days | 3 days | -1 (simpler) |
| Runtime Hooks | 4 days | N/A | -4 (use settrace) |
| Advanced CLI | 3 days | 4 days | +1 (more features) |
| DAP Server | 4 days | 6 days | +2 (not reduced) |
| VS Code | 3 days | 3 days | 0 |
| **Profiling** | Not included | 2 days | +2 (easy win!) |
| **Total** | **25 days** | **18 days** | **-7 days** |

### 4. New Addition: cProfile Profiling

**Original proposal:** No profiling strategy
**Revised proposal:** cProfile integration (5-minute implementation!)

```bash
$ mlpy run --profile example.ml

=== Profiling Results ===
   ncalls  tottime  percall  cumtime  percall function
      100    0.003    0.000    0.015    0.000 fibonacci
        1    0.000    0.000    0.015    0.015 <module>
```

**Overhead:** 2-5% when `--profile` used, 0% otherwise

---

## Technical Differences

### Variable Inspection

**Original (AST):**
```python
# Hook captures locals() - a SNAPSHOT
__debug_hooks__.line_executed('main.ml', 4, locals())
result = x + y  # result NOT in snapshot yet!

# Problem: Need hook AFTER line to capture result
result = x + y
__debug_hooks__.line_executed('main.ml', 4, locals())  # Now has result
# But this breaks "stop BEFORE executing" semantics
```

**Revised (settrace):**
```python
# Trace function gets LIVE frame
def trace_function(frame, event, arg):
    if event == 'line':
        # frame.f_locals is LIVE - always current
        result = frame.f_locals.get('result')  # Works!
        # Can even MODIFY variables:
        frame.f_locals['result'] = new_value  # Advanced feature
```

### Breakpoint Semantics

**Original (AST):**
- Must inject hooks at exact AST locations
- Complex logic to handle control flow
- Risk of hooks interfering with program logic

**Revised (settrace):**
- Python handles all control flow
- Just check "should break here?"
- Standard debugger semantics (like pdb, gdb)

### Code Generation Impact

**Original (AST):**
```python
# PythonGenerator must be modified heavily
class PythonGenerator:
    def visit_Assignment(self, node):
        py_node = self._create_assignment(node)

        # Add debug instrumentation
        if self.debug_mode:
            py_node = self._wrap_with_hooks(py_node)
            py_node = self._add_line_tracking(py_node)
            py_node = self._inject_variable_capture(py_node)

        return py_node
```

**Revised (settrace):**
```python
# PythonGenerator unchanged - just ensure source maps
class PythonGenerator:
    def visit_Assignment(self, node):
        py_node = self._create_assignment(node)

        # Only need to record mapping (already done in Sprint 7!)
        self.source_map.add_mapping(...)

        return py_node  # Clean, no debug hooks
```

---

## Advantages of Revised Approach

### For Developers

1. **No Recompilation:** Debug existing transpiled code without retranspiling
2. **Zero Production Overhead:** Same code runs full speed in production
3. **Quick Toggle:** Can switch between debug/run instantly
4. **Live Variables:** Can inspect and modify variables during debugging
5. **Standard Semantics:** Familiar debugging experience (like Python's pdb)

### For Implementation

1. **Simpler Code:** 200-300 LOC vs 500-800 LOC
2. **Faster PoC:** Working debugger in 3 days vs 2 weeks
3. **Less Maintenance:** No coupling to grammar changes
4. **Fewer Bugs:** Less complex code = fewer edge cases
5. **Proven Approach:** Python's pdb, debugpy use the same mechanism

### For Testing

1. **Isolated Testing:** Test debugger separately from code generation
2. **No Transpiler Changes:** Don't risk breaking existing functionality
3. **Easy Validation:** Compare to pdb behavior
4. **Performance Testing:** Easy to measure overhead (toggle settrace on/off)

---

## Disadvantages of Revised Approach

### Overhead During Debugging

**Original:** 2-5% overhead when debugging
**Revised:** 10-15% overhead when debugging

**Analysis:** This is acceptable because:
- Developers expect debugging to be slower
- Only happens during active debugging session
- Python's pdb has similar overhead (users accept it)
- Can optimize later if needed (hybrid approach)

### Can't Optimize for "No Breakpoints" Case

**Original:** Can conditionally compile hooks only for lines with breakpoints
**Revised:** Trace function fires for ALL lines (though can optimize fast path)

**Analysis:** Not a real issue because:
- Fast path is very fast (set membership check)
- Only happens during debugging (0% overhead when not debugging)
- Acceptable tradeoff for simplicity

---

## Decision Framework

### Choose Revised Proposal (settrace) if:

✅ **Zero production overhead is critical** (it is for mlpy)
✅ **Want faster implementation** (PoC in 3 days)
✅ **Prefer simpler codebase** (easier to maintain)
✅ **10-15% debug overhead is acceptable** (it is)
✅ **Want easy-win profiling** (cProfile integration)

### Choose Original Proposal (AST) if:

❌ **Need <5% debug overhead** (unlikely requirement)
❌ **Have AST expertise on team** (we do, but still not worth it)
❌ **Want custom instrumentation** (can add later if needed)

---

## Implementation Roadmap: Revised Proposal

### Week 1: PoC (Days 1-3)

**Goal:** Working REPL debugger

**Tasks:**
- Day 1: Source map index (SourceMapIndex class)
- Day 2: Core debugger (settrace integration, breakpoints)
- Day 3: REPL interface (commands, UI)

**Deliverable:** `mlpy debug example.ml` works!

### Week 2: Enhancement (Days 4-7)

**Goal:** Professional features

**Tasks:**
- Conditional breakpoints
- Call stack navigation
- Watch expressions
- Better variable formatting

**Deliverable:** Feature-complete CLI debugger

### Week 3: Profiling (Days 8-9)

**Goal:** Zero-effort profiling

**Tasks:**
- cProfile integration (5 minutes!)
- ML function name translation (1 day)
- CLI flags and output formatting (1 day)

**Deliverable:** `mlpy run --profile example.ml` works!

### Week 4-5: DAP and VS Code (Days 10-18)

**Goal:** IDE integration

**Tasks:**
- DAP protocol implementation (6 days)
- VS Code extension enhancement (3 days)

**Deliverable:** Debug ML in VS Code!

---

## Profiling Bonus: Why It's Easy

Python's `cProfile` is **built-in** and works with **zero code modification**:

```python
import cProfile

# That's it! Wrap your code:
profiler = cProfile.Profile()
profiler.enable()

# Run ML program
exec(compiled_python_code)

profiler.disable()
profiler.print_stats()
```

**Output:**
```
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
      100    0.003    0.000    0.015    0.000 fibonacci.py:15(fibonacci)
        1    0.000    0.000    0.015    0.015 fibonacci.py:1(<module>)
```

**To get ML function names:** Just translate using source map!

**Overhead:** 2-5% (much better than settrace's 10-15%)

**Why it's different from debugging:**
- `sys.setprofile()` only fires on function call/return (not every line)
- Much lower overhead than `sys.settrace()`
- Perfect for profiling (don't need line-level granularity)

---

## Conclusion

**Recommendation: Implement Revised Proposal**

**Rationale:**
1. **Zero production overhead** is killer feature
2. **Simpler implementation** = faster delivery, easier maintenance
3. **Proven approach** = lower risk
4. **Easy-win profiling** = bonus value
5. **10-15% debug overhead** is acceptable industry standard

**Next Steps:**
1. Approve revised proposal
2. Start with Phase 1 PoC (3 days)
3. Validate with real ML programs
4. Continue to enhancement phases

**Risk Mitigation:**
- If 15% overhead is unacceptable → can optimize or add minimal instrumentation
- If settrace has issues → can fall back to AST approach (but unlikely)
- PoC will validate approach quickly (3 days vs committing to 2 weeks)

---

## Appendix: Code Size Comparison

### Original Approach (AST Instrumentation)

```
src/mlpy/debugging/
├── debug_info.py              (150 LOC) - Debug info structures
├── instrumentation.py         (300 LOC) - AST transformation
├── runtime_hooks.py           (200 LOC) - Hook implementations
├── source_mapping.py          (150 LOC) - Source map generation
├── breakpoint_manager.py      (100 LOC) - Breakpoint logic
├── variable_inspector.py      (150 LOC) - Variable inspection
├── debug_session.py           (200 LOC) - Session management
└── cli_debugger.py            (150 LOC) - CLI interface

Total: ~1,400 LOC
```

### Revised Approach (sys.settrace)

```
src/mlpy/debugging/
├── source_map_index.py        ( 80 LOC) - Bidirectional index
├── debugger.py                (150 LOC) - Core debugger + settrace
├── repl.py                    (100 LOC) - REPL interface
└── profiler.py                ( 50 LOC) - cProfile wrapper

src/mlpy/ml/codegen/
└── enhanced_source_maps.py    (Existing from Sprint 7)

Total: ~380 LOC
```

**Difference:** 1,400 LOC vs 380 LOC = **73% less code!**
