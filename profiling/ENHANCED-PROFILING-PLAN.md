# 🎯 Enhanced Profiling System - Implementation Plan

**Date:** October 2025
**Status:** Planning Phase
**Priority:** High
**Estimated Time:** 1-2 days

---

## Executive Summary

Enhance the existing MLProfiler system with audience-specific reports, memory profiling, and flexible output options. The goal is to provide targeted performance insights for both **ML Developers** (who want to optimize the compiler/runtime) and **ML Users** (who want to optimize their code).

### Key Requirements

1. **5 Report Types:**
   - `--dev-summary`: Developer summary (performance optimization focus)
   - `--dev-details`: Developer details (overhead by pipeline category)
   - `--ml-summary`: User summary (ML code optimization focus) - **DEFAULT**
   - `--ml-details`: User details (ML functions grouped by module)
   - `--raw`: Raw cProfile output (for advanced analysis)

2. **Memory Profiling:** Add memory usage tracking to all reports

3. **Flexible Output:** `--profile-output` option to write reports to files

4. **Backward Compatibility:** Existing `--profile` flag continues to work

---

## Current State Analysis

### Existing Implementation (Phase 4)

**Files:**
- `src/mlpy/runtime/profiler.py` (620 LOC)
- `src/mlpy/cli/app.py` (CLI integration)

**Current Reports:**
1. Summary Report (what we now call "dev-summary")
2. MLPY Analysis Report (what we now call "dev-details")

**Current CLI:**
```bash
mlpy run example.ml --profile
# Always shows both reports
```

**Limitations:**
- ❌ No user-focused reports (ML code only)
- ❌ No memory profiling
- ❌ No report type selection
- ❌ No file output option
- ❌ Always shows developer-focused reports (not what users want)

---

## Target State

### New CLI Interface

```bash
# Default: ML user summary (what they want to see)
mlpy run example.ml --profile

# Explicit report types
mlpy run example.ml --profile --report ml-summary     # ML user summary (default)
mlpy run example.ml --profile --report ml-details     # ML functions by module
mlpy run example.ml --profile --report dev-summary    # Developer summary
mlpy run example.ml --profile --report dev-details    # Developer details
mlpy run example.ml --profile --report raw            # Raw cProfile

# Save to file
mlpy run example.ml --profile --profile-output performance.txt

# Multiple reports
mlpy run example.ml --profile --report ml-summary --report dev-summary

# All reports
mlpy run example.ml --profile --report all
```

---

## Report Type Specifications

### 1. `--ml-summary` (DEFAULT) ⭐

**Audience:** ML Users (want to optimize their code)

**Purpose:** Show only ML code performance, hide mlpy overhead

**Content:**
- Total execution time
- ML code execution time (exclude all overhead)
- **Top 10 ML Functions** (by time spent)
- **ML File Breakdown** (time per .ml file)
- **Memory Usage** (peak, per function)
- **Optimization Suggestions** (user code focus)

**Sample Output:**
```
======================================================================
ML CODE PERFORMANCE SUMMARY
======================================================================

Total Execution Time: 2.456s
ML Code Execution Time: 2.000s (81.5%)
mlpy Overhead: 0.456s (18.5%)

Memory Usage:
  Peak Memory: 45.2 MB
  ML Code Memory: 32.8 MB

Top ML Functions (by execution time):
+----------------------------------------+----------+----------+--------+----------+
| Function                               | Time     | % Total  | Calls  | Memory   |
+----------------------------------------+----------+----------+--------+----------+
| process_batch (data_processor.ml:25)   | 0.600s   |  30.0%   | 10,000 | 12.5 MB  |
| main (main.ml:42)                      | 0.550s   |  27.5%   |      1 | 8.2 MB   |
| transform_data (utils.ml:15)           | 0.250s   |  12.5%   |  5,000 | 6.3 MB   |
| validate (helpers.ml:30)               | 0.150s   |   7.5%   |  2,345 | 3.1 MB   |
+----------------------------------------+----------+----------+--------+----------+

ML Files (by execution time):
+---------------------+----------+----------+--------+----------+
| File                | Time     | % Total  | Calls  | Memory   |
+---------------------+----------+----------+--------+----------+
| data_processor.ml   | 0.700s   |  35.0%   | 10,000 | 15.2 MB  |
| main.ml             | 0.800s   |  40.0%   |  1,234 | 10.5 MB  |
| utils.ml            | 0.300s   |  15.0%   |  5,678 | 5.8 MB   |
| helpers.ml          | 0.200s   |  10.0%   |  2,345 | 3.3 MB   |
+---------------------+----------+----------+--------+----------+

OPTIMIZATION RECOMMENDATIONS:

▸ process_batch() (data_processor.ml:25) - 30.0% of execution time
  - This function is your main performance bottleneck
  - Consider: caching repeated calculations, reducing loop iterations
  - Memory: 12.5 MB used - check for unnecessary array copies

▸ main() (main.ml:42) - 27.5% of execution time
  - Second most expensive function
  - Review algorithm complexity - can this be optimized?

✓ Overall: Your ML code runs efficiently
  - mlpy overhead is minimal (18.5%)
  - Focus optimization efforts on top 2 functions
```

### 2. `--ml-details`

**Audience:** ML Users (detailed investigation)

**Purpose:** Show all ML functions grouped by module, hide mlpy internals

**Content:**
- All ML functions (not just top 10)
- Grouped by ML file/module
- Call counts, times, memory per function
- Hierarchical display (files → functions)

**Sample Output:**
```
======================================================================
ML CODE DETAILED ANALYSIS
======================================================================

Total Execution Time: 2.456s
ML Code Execution Time: 2.000s (81.5%)

┌──────────────────────────────────────────────────────────────────┐
│ data_processor.ml (0.700s, 35.0%, 12.5 MB)                       │
├──────────────────────────────────────────────────────────────────┤
| Function                Time     % File  Calls  Memory  Avg Time |
├──────────────────────────────────────────────────────────────────┤
| process_batch (line 25) 0.600s   85.7%  10,000  10.2 MB  0.060ms |
| validate_input (line 5) 0.050s    7.1%   1,000   1.5 MB  0.050ms |
| parse_record (line 15)  0.030s    4.3%   5,000   0.8 MB  0.006ms |
| format_output (line 35) 0.020s    2.9%   1,000   0.0 MB  0.020ms |
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│ main.ml (0.800s, 40.0%, 10.5 MB)                                 │
├──────────────────────────────────────────────────────────────────┤
| Function                Time     % File  Calls  Memory  Avg Time |
├──────────────────────────────────────────────────────────────────┤
| main (line 42)          0.550s   68.8%       1   8.0 MB  550.0ms |
| initialize (line 10)    0.150s   18.8%       1   1.5 MB  150.0ms |
| cleanup (line 80)       0.100s   12.5%       1   1.0 MB  100.0ms |
└──────────────────────────────────────────────────────────────────┘

[... more modules ...]
```

### 3. `--dev-summary`

**Audience:** ML Developers (mlpy contributors)

**Purpose:** Show mlpy overhead breakdown for performance optimization

**Content:**
- Current "Summary Report"
- All categories (including mlpy internals)
- Category percentages
- Top functions across all categories

**Sample Output:**
```
======================================================================
MLPY PERFORMANCE SUMMARY REPORT (Developer View)
======================================================================

Total Execution Time: 2.456s

Time Breakdown (by category):
+---------------------+----------+----------+
| Category            | Time     | % Total  |
+---------------------+----------+----------+
| Python Stdlib       | 0.456s   |  18.6%   |
| Parsing             | 0.045s   |   1.8%   |
| Transpilation       | 0.087s   |   3.5%   |
| Runtime Overhead    | 0.246s   |  10.0%   |
| ML Code Execution   | 2.000s   |  81.5%   |
| Sandbox Startup     | 0.050s   |   2.0%   |
| Security Analysis   | 0.028s   |   1.1%   |
+---------------------+----------+----------+

Memory Breakdown:
+---------------------+----------+
| Category            | Memory   |
+---------------------+----------+
| ML Code             | 32.8 MB  |
| Runtime Overhead    | 8.5 MB   |
| Parsing/Transpile   | 4.2 MB   |
| Total Peak          | 45.2 MB  |
+---------------------+----------+

[... rest of current summary report ...]
```

### 4. `--dev-details`

**Audience:** ML Developers (deep optimization)

**Purpose:** Show detailed mlpy internals breakdown

**Content:**
- Current "MLPY Analysis Report"
- Detailed per-category breakdown
- Top 10 functions per mlpy category
- Optimization recommendations for mlpy

**Sample Output:**
```
======================================================================
MLPY INTERNAL PERFORMANCE ANALYSIS (Developer View)
======================================================================

Total mlpy Overhead: 0.456s (18.6% of total)

┌──────────────────────────────────────────────────────────────────┐
│ RUNTIME OVERHEAD (0.246s, 10.0%, 8.5 MB)                         │
├──────────────────────────────────────────────────────────────────┤
| Function                           Time    Calls  Memory         |
├──────────────────────────────────────────────────────────────────┤
| safe_call                          0.120s  15,234  4.2 MB        |
| safe_attr_access                   0.080s  10,456  2.8 MB        |
| safe_method_call                   0.030s   3,890  1.2 MB        |
| check_capabilities                 0.016s   1,234  0.3 MB        |
└──────────────────────────────────────────────────────────────────┘

[... more categories ...]
```

### 5. `--raw`

**Audience:** Advanced users, automation

**Purpose:** Raw cProfile output for external tools

**Content:**
- Standard cProfile stats format
- All functions, no filtering
- Sortable by time/calls/name
- Machine-parseable

**Sample Output:**
```
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    10000    0.600    0.000    0.600    0.000 data_processor.py:25(process_batch)
        1    0.550    0.550    2.000    2.000 main.py:42(main)
     5678    0.300    0.000    0.300    0.000 utils.py:15(transform_data)
    15234    0.120    0.000    0.150    0.000 whitelist_validator.py:45(safe_call)
```

---

## Memory Profiling Design

### Approach: `tracemalloc` Integration

**Why tracemalloc?**
- Built into Python 3.4+
- <5% overhead (acceptable)
- Per-function memory tracking
- Peak memory detection

**Implementation:**
```python
import tracemalloc

class MLProfiler:
    def start(self):
        # Start time profiling
        self.profiler.enable()

        # Start memory profiling
        tracemalloc.start()
        self.memory_enabled = True

    def stop(self):
        # Stop time profiling
        self.profiler.disable()

        # Get memory snapshot
        if self.memory_enabled:
            self.memory_snapshot = tracemalloc.take_snapshot()
            tracemalloc.stop()

    def get_memory_stats(self) -> Dict[str, MemoryStats]:
        """Extract memory statistics per function."""
        if not self.memory_snapshot:
            return {}

        stats_by_file = defaultdict(lambda: {
            'peak': 0,
            'current': 0,
            'allocations': 0
        })

        for stat in self.memory_snapshot.statistics('lineno'):
            filename = stat.traceback[0].filename
            stats_by_file[filename]['peak'] = max(
                stats_by_file[filename]['peak'],
                stat.size
            )
            stats_by_file[filename]['current'] += stat.size
            stats_by_file[filename]['allocations'] += stat.count

        return dict(stats_by_file)
```

**Memory Metrics:**
- Peak memory usage (max during execution)
- Current memory usage (at end)
- Memory per function
- Memory per ML file
- Memory per category

---

## Implementation Steps

### Step 1: Enhance MLProfiler Class ✅

**File:** `src/mlpy/runtime/profiler.py`

**Changes:**
1. Add `tracemalloc` integration
2. Add `report_type` parameter to report methods
3. Implement 5 new report methods:
   - `generate_ml_summary_report()`
   - `generate_ml_details_report()`
   - `generate_dev_summary_report()` (rename current `generate_summary_report`)
   - `generate_dev_details_report()` (rename current `generate_mlpy_analysis_report`)
   - `generate_raw_report()`

**New Methods:**
```python
def generate_ml_summary_report(self) -> str:
    """Generate ML user-focused summary report."""
    # Filter to user_code category only
    # Show top 10 functions
    # Show ML file breakdown
    # Include memory stats
    # User-friendly recommendations
    pass

def generate_ml_details_report(self) -> str:
    """Generate ML user-focused detailed report."""
    # Group all user functions by ML file
    # Show hierarchical view
    # Include all functions, not just top 10
    # Memory per function
    pass

def generate_raw_report(self) -> str:
    """Generate raw cProfile output."""
    stats = self.get_stats()
    stream = StringIO()
    stats.print_stats()
    return stream.getvalue()
```

### Step 2: Update CLI Integration ✅

**File:** `src/mlpy/cli/app.py`

**Changes:**
1. Add `--report` option (multiple allowed)
2. Add `--profile-output` option
3. Change default behavior to `ml-summary`
4. Support multiple reports

**New CLI Options:**
```python
@click.option("--profile", is_flag=True, help="Enable performance profiling")
@click.option(
    "--report",
    type=click.Choice(["ml-summary", "ml-details", "dev-summary", "dev-details", "raw", "all"]),
    multiple=True,
    default=["ml-summary"],
    help="Profiling report type (default: ml-summary, can specify multiple)"
)
@click.option(
    "--profile-output",
    type=click.Path(),
    help="Save profiling report to file (default: print to console)"
)
def run(..., profile, report, profile_output):
    # ...
```

**Report Generation Logic:**
```python
if profile:
    ml_profiler = MLProfiler()
    ml_profiler.start()

    # ... run program ...

    ml_profiler.stop()

    # Generate requested reports
    reports = list(report) if report else ["ml-summary"]
    if "all" in reports:
        reports = ["ml-summary", "ml-details", "dev-summary", "dev-details", "raw"]

    output_lines = []

    for report_type in reports:
        if report_type == "ml-summary":
            output_lines.append(ml_profiler.generate_ml_summary_report())
        elif report_type == "ml-details":
            output_lines.append(ml_profiler.generate_ml_details_report())
        elif report_type == "dev-summary":
            output_lines.append(ml_profiler.generate_dev_summary_report())
        elif report_type == "dev-details":
            output_lines.append(ml_profiler.generate_dev_details_report())
        elif report_type == "raw":
            output_lines.append(ml_profiler.generate_raw_report())

        output_lines.append("\n" + "=" * 70 + "\n")

    output_text = "\n".join(output_lines)

    # Output to file or console
    if profile_output:
        Path(profile_output).write_text(output_text, encoding="utf-8")
        console.print(f"[green]Profiling report saved to {profile_output}[/green]")
    else:
        console.print(output_text)
```

### Step 3: Memory Profiling Integration ✅

**Changes to MLProfiler:**
```python
import tracemalloc
from dataclasses import dataclass

@dataclass
class MemoryStats:
    """Memory statistics for a function/file."""
    peak_bytes: int
    current_bytes: int
    allocations: int

    @property
    def peak_mb(self) -> float:
        return self.peak_bytes / (1024 * 1024)

    @property
    def current_mb(self) -> float:
        return self.current_bytes / (1024 * 1024)

class MLProfiler:
    def __init__(self, source_map_index=None):
        # ... existing code ...
        self.memory_enabled = False
        self.memory_snapshot = None
        self.memory_stats = {}

    def start(self):
        self.profiler.enable()
        self.enabled = True

        # Start memory profiling
        try:
            tracemalloc.start()
            self.memory_enabled = True
        except RuntimeError:
            # Already started
            pass

    def stop(self):
        self.profiler.disable()
        self.enabled = False

        # Capture memory snapshot
        if self.memory_enabled:
            self.memory_snapshot = tracemalloc.take_snapshot()
            self.memory_stats = self._compute_memory_stats()
            tracemalloc.stop()

    def _compute_memory_stats(self) -> Dict[str, MemoryStats]:
        """Compute memory stats per file/function."""
        # ... implementation ...
```

### Step 4: Testing ✅

**New Test File:** `tests/unit/profiling/test_enhanced_reports.py`

**Test Cases:**
1. ML Summary Report generation (10 tests)
2. ML Details Report generation (10 tests)
3. Dev Summary Report generation (5 tests)
4. Dev Details Report generation (5 tests)
5. Raw Report generation (3 tests)
6. Memory profiling integration (8 tests)
7. CLI integration (10 tests)
8. File output (5 tests)

**Total:** 56 new tests

### Step 5: Documentation ✅

**Update Files:**
1. `profiling/PROFILE-OPTIONS-REFERENCE.md` - Complete CLI reference
2. `docs/summaries/debug-progress.md` - Track Phase 4.5 implementation
3. `docs/source/user-guide/toolkit/debugging-profiling.rst` - User documentation

---

## Backward Compatibility

### Existing Behavior Preserved

**Old command:**
```bash
mlpy run example.ml --profile
```

**Old behavior:** Showed dev-summary + dev-details

**New behavior:** Shows ml-summary (more useful for users!)

**Migration:** Users who want old behavior use:
```bash
mlpy run example.ml --profile --report dev-summary --report dev-details
```

### API Compatibility

**Old methods still work:**
```python
profiler.generate_summary_report()  # Still works, now called dev-summary
profiler.generate_mlpy_analysis_report()  # Still works, now called dev-details
```

---

## Timeline Estimate

### Day 1: Core Implementation (6 hours)
- ✅ Memory profiling integration (2 hours)
- ✅ ML summary report generation (2 hours)
- ✅ ML details report generation (2 hours)

### Day 2: Finalization (6 hours)
- ✅ CLI integration and testing (2 hours)
- ✅ File output implementation (1 hour)
- ✅ Test suite (56 tests) (2 hours)
- ✅ Documentation updates (1 hour)

**Total Estimate:** 12 hours (1.5 days)

---

## Success Criteria

### Implementation Complete When:
- [ ] All 5 report types implemented
- [ ] Memory profiling working (<5% overhead)
- [ ] `--ml-summary` is default report
- [ ] `--profile-output` saves to files
- [ ] 56 new tests passing (100%)
- [ ] Documentation updated
- [ ] Backward compatibility verified

### User Acceptance:
- [ ] ML users see ML code performance (not mlpy overhead)
- [ ] ML developers see mlpy internals when needed
- [ ] Memory usage visible in all reports
- [ ] Reports can be saved to files
- [ ] Default behavior is user-friendly

---

## Risk Assessment

### Risk 1: Memory Profiling Overhead
**Risk:** tracemalloc adds >5% overhead

**Mitigation:**
- Benchmark with real programs
- Make memory profiling optional if overhead too high
- Document overhead in help text

**Likelihood:** Low (tracemalloc typically <5%)

### Risk 2: Report Complexity
**Risk:** Too many report types confuse users

**Mitigation:**
- Clear documentation
- Good defaults (ml-summary)
- Examples in help text

**Likelihood:** Low (clear purpose for each type)

### Risk 3: Backward Compatibility
**Risk:** Changing default breaks existing workflows

**Mitigation:**
- Document migration path
- Keep old report methods working
- Release notes explain changes

**Likelihood:** Low (easy migration)

---

## Next Steps

1. ✅ Review this plan
2. ✅ Get approval for approach
3. ✅ Start implementation (Step 1)
4. ✅ Update debug-progress.md as we progress

---

**Plan Status:** Ready for Implementation
**Approval Required:** Yes
**Next Action:** Begin Step 1 (Enhance MLProfiler)
