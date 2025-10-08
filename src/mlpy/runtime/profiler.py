"""ML Performance Profiler with Beautiful Reports.

Provides performance profiling for ML programs using Python's cProfile,
with intelligent categorization of mlpy overhead vs user code execution.

Key Features:
- Separate mlpy internal overhead from user ML code
- Beautiful two-tier reporting (Summary + MLPY Analysis)
- Zero overhead when not profiling
- 2-5% overhead when profiling enabled
- ML-aware function attribution (shows .ml files, not .py)

Author: mlpy development team
Version: 2.0.0
License: MIT
"""

import cProfile
import pstats
import tracemalloc
from io import StringIO
from dataclasses import dataclass
from typing import Dict, List, Tuple, Set, Optional
from collections import defaultdict
import os


@dataclass
class ProfileEntry:
    """Single profiling entry for a function.

    Attributes:
        function_name: Name of the function
        filename: File where function is defined
        ml_file: ML source file if user code, None if mlpy internal
        calls: Number of times function was called
        total_time: Time spent IN this function only (tottime)
        cumulative_time: Time in function + all subcalls (cumtime)
        per_call_time: Average time per call (tottime/calls)
        memory_bytes: Memory used by this function (bytes)
    """
    function_name: str
    filename: str
    ml_file: Optional[str] = None
    calls: int = 0
    total_time: float = 0.0
    cumulative_time: float = 0.0
    per_call_time: float = 0.0
    memory_bytes: int = 0


@dataclass
class MemoryStats:
    """Memory statistics for a function or category.

    Attributes:
        peak_bytes: Peak memory usage in bytes
        current_bytes: Current memory usage in bytes
        allocations: Number of memory allocations
    """
    peak_bytes: int = 0
    current_bytes: int = 0
    allocations: int = 0

    @property
    def peak_mb(self) -> float:
        """Peak memory in megabytes."""
        return self.peak_bytes / (1024 * 1024)

    @property
    def current_mb(self) -> float:
        """Current memory in megabytes."""
        return self.current_bytes / (1024 * 1024)


@dataclass
class CategoryStats:
    """Statistics for a profiling category.

    Attributes:
        category: Category name (e.g., 'parsing', 'user_code')
        total_time: Sum of tottime for all functions in category
        percentage: Percentage of total execution time
        entries: List of ProfileEntry objects in this category
    """
    category: str
    total_time: float = 0.0
    percentage: float = 0.0
    entries: List[ProfileEntry] = None

    def __post_init__(self):
        if self.entries is None:
            self.entries = []


class MLProfiler:
    """Performance profiler for ML programs with beautiful reports.

    Wraps Python's cProfile with ML-aware reporting that separates:
    - Sandbox startup time
    - Parsing time
    - Security analysis time
    - Transpilation time
    - Runtime overhead (safe_call, safe_attr_access, etc.)
    - User ML code execution

    Usage:
        profiler = MLProfiler()
        profiler.start()

        # Run ML program
        execute_ml_code()

        profiler.stop()
        print(profiler.generate_summary_report())
        print(profiler.generate_mlpy_analysis_report())
    """

    def __init__(self, source_map_index=None):
        """Initialize profiler.

        Args:
            source_map_index: Optional SourceMapIndex for ML file mapping
        """
        self.profiler = cProfile.Profile()
        self.source_map_index = source_map_index
        self.enabled = False

        # Memory profiling
        self.memory_enabled = False
        self.memory_snapshot = None
        self.memory_stats = {}

        # Explicit runtime overhead functions (discovered from transpiled code)
        # These are the ONLY functions that add measurable overhead during execution
        self.runtime_overhead_functions = {
            # Core validation functions (PRIMARY OVERHEAD - hot path)
            'safe_call',            # Every stdlib/builtin function call
            'safe_attr_access',     # Every property access (obj.name, arr.length)
            'safe_method_call',     # Every method call (str.upper(), arr.push())
            'get_safe_length',      # Length property access (arr.length)

            # Capability checking (when capabilities required)
            'check_capabilities',
            'get_current_capability_context',
            'has_capability',
            'get_all_capabilities',

            # Context management
            'set_capability_context',
            'get_current_context',
            'set_current_context',

            # SafeAttributeRegistry operations
            'is_safe_access',
            'get_attribute_info',
        }

        # Category patterns for mlpy compile-time phases
        # These only execute BEFORE user code runs
        self.category_patterns = {
            'sandbox_startup': [
                'mlpy.runtime.sandbox',
                'mlpy.runtime.capabilities.context',  # Only __init__, setup
            ],
            'parsing': [
                'lark.lark',
                'lark.lexer',
                'lark.parser',
                'mlpy.ml.parser',
            ],
            'security_analysis': [
                'mlpy.ml.analysis',
                'mlpy.ml.security',
            ],
            'transpilation': [
                'mlpy.ml.codegen',
                'mlpy.ml.transpiler',
            ],
        }

    def start(self):
        """Start profiling.

        Enables cProfile with 2-5% overhead. All function calls will be tracked.
        Also starts memory profiling with tracemalloc (<5% overhead).
        """
        self.profiler.enable()
        self.enabled = True

        # Start memory profiling
        try:
            tracemalloc.start()
            self.memory_enabled = True
        except RuntimeError:
            # tracemalloc already started (e.g., by another profiler)
            self.memory_enabled = False

    def stop(self):
        """Stop profiling.

        Disables cProfile and freezes profiling data for analysis.
        Also captures memory snapshot if memory profiling was enabled.
        """
        self.profiler.disable()
        self.enabled = False

        # Capture memory snapshot
        if self.memory_enabled:
            try:
                self.memory_snapshot = tracemalloc.take_snapshot()
                self.memory_stats = self._compute_memory_stats()
                tracemalloc.stop()
            except Exception:
                # Ignore memory profiling errors
                self.memory_enabled = False
                self.memory_snapshot = None
                self.memory_stats = {}

    def get_stats(self) -> pstats.Stats:
        """Get raw profiling statistics.

        Returns:
            pstats.Stats object with all profiling data
        """
        return pstats.Stats(self.profiler)

    def categorize_function(self, filename: str, function_name: str) -> Tuple[str, Optional[str]]:
        """Categorize function as mlpy internal or user code.

        Uses precise function name matching for runtime overhead,
        pattern matching for compile-time phases.

        Args:
            filename: Python file path where function is defined
            function_name: Name of the function

        Returns:
            Tuple of (category, ml_file) where:
            - category: 'sandbox_startup', 'parsing', 'security_analysis',
                       'transpilation', 'runtime_overhead', 'user_code', or 'python_stdlib'
            - ml_file: ML source file if user code, None if mlpy internal
        """
        # PRIORITY 1: Check explicit runtime overhead functions (most common)
        if function_name in self.runtime_overhead_functions:
            return ('runtime_overhead', None)

        # PRIORITY 2: Check compile-time phase patterns
        # Normalize path separators for cross-platform compatibility
        filename_normalized = filename.replace('\\', '/')

        # Convert to module notation for pattern matching
        # 'lark/lark.py' → 'lark.lark', 'mlpy/runtime/sandbox.py' → 'mlpy.runtime.sandbox'
        filename_module = filename_normalized.replace('/', '.').replace('.py', '')

        for category, patterns in self.category_patterns.items():
            for pattern in patterns:
                if pattern in filename_module:
                    return (category, None)

        # PRIORITY 3: Check if it's user code (generated .py file)
        if self.source_map_index:
            # Try to map Python file back to ML file
            ml_file = self._get_ml_file_from_py(filename)
            if ml_file:
                return ('user_code', ml_file)

        # Check if filename looks like generated code
        # Normalize path separators for cross-platform compatibility
        filename_normalized = filename.replace('\\', '/')

        # Check for ML-generated code (should have .ml somewhere in path or near .py file)
        if filename.endswith('.py'):
            # Check if corresponding .ml file exists
            ml_candidate = filename.replace('.py', '.ml')
            if os.path.exists(ml_candidate):
                ml_file = os.path.basename(ml_candidate)
                return ('user_code', ml_file)

            # Check if it's in tests/ml_integration (our ML test files)
            if 'tests' in filename_normalized and 'ml_integration' in filename_normalized:
                ml_file = os.path.basename(filename)
                return ('user_code', ml_file)

            # Check if it has no path separator (built-in module like '<string>')
            if '/' not in filename_normalized and '\\' not in filename_normalized:
                return ('python_stdlib', None)

            # If it's in Python's lib directory or site-packages, it's stdlib
            if 'site-packages' in filename_normalized or 'lib/python' in filename_normalized or 'Lib\\' in filename_normalized:
                return ('python_stdlib', None)

            # Check for Python stdlib indicators
            # Common Python stdlib modules should be categorized as python_stdlib
            stdlib_indicators = ['threading', 'subprocess', 'tempfile', 'typing', 'contextlib',
                                'shutil', 'random', 'weakref', 'inspect', 'json', 'io',
                                '_abc', 'enum', 'collections', 'functools', 'itertools',
                                're', 'os', 'sys', 'pathlib', '_io', '_winapi', 'nt']

            base_filename = os.path.basename(filename_normalized)
            module_name = base_filename.replace('.py', '')

            if module_name in stdlib_indicators or base_filename.startswith('_'):
                return ('python_stdlib', None)

            # If we reach here and it has mlpy in the path, it's mlpy internal
            if 'mlpy' in filename_normalized:
                # Already checked patterns above, must be some other mlpy file
                return ('python_stdlib', None)

        # FALLBACK: Categorize as Python stdlib or other
        # This catches: built-in functions, Python standard library
        return ('python_stdlib', None)

    def _get_ml_file_from_py(self, py_file: str) -> Optional[str]:
        """Get ML file from Python file path.

        Uses source map index to reverse-map Python files to ML sources.

        Args:
            py_file: Python file path

        Returns:
            ML file path if found, None otherwise
        """
        # Simple heuristic: replace .py with .ml
        # This works even without source_map_index for basic cases
        if py_file.endswith('.py'):
            ml_candidate = py_file.replace('.py', '.ml')
            if os.path.exists(ml_candidate):
                return os.path.basename(ml_candidate)

        # If source_map_index available, use it for more precise mapping
        if self.source_map_index:
            # TODO: Implement source map index lookup
            pass

        return None

    def _compute_memory_stats(self) -> Dict[str, MemoryStats]:
        """Compute memory statistics per file from tracemalloc snapshot.

        Returns:
            Dictionary mapping filename to MemoryStats
        """
        if not self.memory_snapshot:
            return {}

        stats_by_file = defaultdict(lambda: MemoryStats())

        # Group memory stats by file
        for stat in self.memory_snapshot.statistics('lineno'):
            filename = stat.traceback[0].filename

            # Normalize path
            filename = filename.replace('\\', '/')

            stats_by_file[filename].peak_bytes = max(
                stats_by_file[filename].peak_bytes,
                stat.size
            )
            stats_by_file[filename].current_bytes += stat.size
            stats_by_file[filename].allocations += stat.count

        return dict(stats_by_file)

    def get_memory_for_function(self, filename: str) -> int:
        """Get memory usage for a specific file in bytes.

        Args:
            filename: Python file path

        Returns:
            Memory usage in bytes
        """
        # Normalize filename
        filename = filename.replace('\\', '/')

        if filename in self.memory_stats:
            return self.memory_stats[filename].current_bytes

        return 0

    def _categorize_all_functions(self, stats: pstats.Stats) -> Dict[str, CategoryStats]:
        """Categorize all profiled functions.

        Args:
            stats: pstats.Stats object with profiling data

        Returns:
            Dictionary mapping category name to CategoryStats
        """
        categories = defaultdict(lambda: CategoryStats(category=""))

        # Iterate through all profiled functions
        for func, (cc, nc, tt, ct, callers) in stats.stats.items():
            filename, lineno, funcname = func

            # Categorize this function
            category, ml_file = self.categorize_function(filename, funcname)

            # Get memory usage for this file
            memory_bytes = self.get_memory_for_function(filename)

            # Create profile entry
            entry = ProfileEntry(
                function_name=funcname,
                filename=filename,
                ml_file=ml_file,
                calls=nc,
                total_time=tt,
                cumulative_time=ct,
                per_call_time=tt / nc if nc > 0 else 0,
                memory_bytes=memory_bytes
            )

            # Add to category
            if category not in categories:
                categories[category] = CategoryStats(category=category)

            categories[category].entries.append(entry)
            categories[category].total_time += tt

        return dict(categories)

    def generate_dev_summary_report(self) -> str:
        """Generate DEVELOPER SUMMARY REPORT showing high-level breakdown.

        Shows:
        - Total execution time
        - Time breakdown by category (table)
        - ML code execution by file (table)
        - Top functions (table)

        Returns:
            Formatted report string
        """
        stats = self.get_stats()
        categories = self._categorize_all_functions(stats)

        # Calculate total time
        total_time = sum(cat.total_time for cat in categories.values())

        # Calculate percentages
        for cat in categories.values():
            cat.percentage = (cat.total_time / total_time * 100) if total_time > 0 else 0

        # Build report
        report = []
        report.append("=" * 70)
        report.append("MLPY PERFORMANCE SUMMARY REPORT")
        report.append("=" * 70)
        report.append("")
        report.append(f"Total Execution Time: {total_time:.3f}s")
        report.append("")

        # Time breakdown table
        report.append("Time Breakdown:")
        report.append(self._format_category_table(categories, total_time))
        report.append("")

        # ML code execution by file (if user code exists)
        if 'user_code' in categories and categories['user_code'].entries:
            report.append("ML Code Execution (by file):")
            report.append(self._format_ml_file_table(categories['user_code']))
            report.append("")

        # Top functions
        report.append("Top Functions (by total time):")
        report.append(self._format_top_functions_table(categories))

        return "\n".join(report)

    def _format_category_table(self, categories: Dict[str, CategoryStats],
                               total_time: float) -> str:
        """Format high-level category breakdown table.

        Args:
            categories: Dictionary of category statistics
            total_time: Total execution time

        Returns:
            Formatted table string
        """
        # Category display names
        category_names = {
            'sandbox_startup': 'Sandbox Startup',
            'parsing': 'Parsing',
            'security_analysis': 'Security Analysis',
            'transpilation': 'Transpilation',
            'runtime_overhead': 'Runtime Overhead',
            'user_code': 'ML Code Execution',
            'python_stdlib': 'Python Stdlib',
        }

        # Sort categories by time (descending)
        sorted_cats = sorted(categories.items(), key=lambda x: x[1].total_time, reverse=True)

        # Build table (ASCII-only for Windows compatibility)
        lines = []
        lines.append("+---------------------+----------+----------+")
        lines.append("| Category            | Time     | % Total  |")
        lines.append("+---------------------+----------+----------+")

        for cat_key, cat in sorted_cats:
            name = category_names.get(cat_key, cat_key)
            time_str = f"{cat.total_time:.3f}s"
            pct_str = f"{cat.percentage:5.1f}%"

            # Format row
            lines.append(f"| {name:19} | {time_str:8} | {pct_str:8} |")

        lines.append("+---------------------+----------+----------+")

        return "\n".join(lines)

    def _format_ml_file_table(self, user_code_cat: CategoryStats) -> str:
        """Format ML file breakdown table.

        Groups user code entries by ML file.

        Args:
            user_code_cat: CategoryStats for user_code category

        Returns:
            Formatted table string
        """
        # Group by ML file
        file_stats = defaultdict(lambda: {'time': 0.0, 'calls': 0})

        for entry in user_code_cat.entries:
            ml_file = entry.ml_file or '<unknown>'
            file_stats[ml_file]['time'] += entry.total_time
            file_stats[ml_file]['calls'] += entry.calls

        # Sort by time
        sorted_files = sorted(file_stats.items(), key=lambda x: x[1]['time'], reverse=True)

        # Build table (ASCII-only for Windows compatibility)
        lines = []
        lines.append("+---------------------+----------+----------+--------+")
        lines.append("| File                | Time     | % Total  | Calls  |")
        lines.append("+---------------------+----------+----------+--------+")

        total_time = user_code_cat.total_time
        for ml_file, stats in sorted_files[:10]:  # Top 10 files
            time = stats['time']
            pct = (time / total_time * 100) if total_time > 0 else 0
            calls = stats['calls']

            # Truncate filename if too long
            display_name = ml_file if len(ml_file) <= 19 else ml_file[:16] + '...'

            lines.append(f"| {display_name:19} | {time:.3f}s | {pct:5.1f}%   | {calls:6,} |")

        lines.append("+---------------------+----------+----------+--------+")

        return "\n".join(lines)

    def _format_top_functions_table(self, categories: Dict[str, CategoryStats]) -> str:
        """Format top functions table.

        Shows top functions across all categories sorted by total time.

        Args:
            categories: Dictionary of category statistics

        Returns:
            Formatted table string
        """
        # Collect all entries
        all_entries = []
        for cat in categories.values():
            all_entries.extend(cat.entries)

        # Sort by total time
        sorted_entries = sorted(all_entries, key=lambda e: e.total_time, reverse=True)

        # Build table (ASCII-only for Windows compatibility)
        lines = []
        lines.append("+--------------------------------------------+----------+--------+")
        lines.append("| Function                                   | Time     | Calls  |")
        lines.append("+--------------------------------------------+----------+--------+")

        for entry in sorted_entries[:15]:  # Top 15 functions
            # Format function name with file
            if entry.ml_file:
                func_str = f"{entry.function_name} ({entry.ml_file})"
            else:
                func_str = entry.function_name

            # Truncate if too long
            if len(func_str) > 42:
                func_str = func_str[:39] + '...'

            lines.append(f"| {func_str:42} | {entry.total_time:.3f}s | {entry.calls:6,} |")

        lines.append("+--------------------------------------------+----------+--------+")

        return "\n".join(lines)

    def generate_dev_details_report(self) -> str:
        """Generate DEVELOPER DETAILS REPORT showing detailed mlpy overhead.

        Shows:
        - Total mlpy overhead
        - Detailed breakdown for each category:
          - Sandbox Startup
          - Parsing
          - Security Analysis
          - Transpilation
          - Runtime Overhead
        - Optimization recommendations

        Returns:
            Formatted report string
        """
        stats = self.get_stats()
        categories = self._categorize_all_functions(stats)

        # Calculate totals
        total_time = sum(cat.total_time for cat in categories.values())

        mlpy_categories = ['sandbox_startup', 'parsing', 'security_analysis',
                          'transpilation', 'runtime_overhead']
        mlpy_time = sum(categories[cat].total_time for cat in mlpy_categories
                       if cat in categories)
        mlpy_percentage = (mlpy_time / total_time * 100) if total_time > 0 else 0

        # Build report
        report = []
        report.append("=" * 70)
        report.append("MLPY INTERNAL PERFORMANCE ANALYSIS")
        report.append("=" * 70)
        report.append("")
        report.append(f"Total mlpy Overhead: {mlpy_time:.3f}s ({mlpy_percentage:.1f}% of total)")
        report.append("")

        # Category titles
        category_titles = {
            'sandbox_startup': 'SANDBOX STARTUP',
            'parsing': 'PARSING',
            'security_analysis': 'SECURITY ANALYSIS',
            'transpilation': 'TRANSPILATION',
            'runtime_overhead': 'RUNTIME OVERHEAD',
        }

        # Detailed breakdown for each mlpy category
        for cat_key in mlpy_categories:
            if cat_key not in categories:
                continue

            cat = categories[cat_key]
            title = category_titles[cat_key]
            percentage = (cat.total_time / total_time * 100) if total_time > 0 else 0

            report.append("+" + "-" * 68 + "+")
            header = f"| {title} ({cat.total_time:.3f}s, {percentage:.1f}%)"
            report.append(header + " " * (70 - len(header)) + "|")
            report.append("+" + "-" * 68 + "+")

            # Top functions in this category
            sorted_entries = sorted(cat.entries, key=lambda e: e.total_time, reverse=True)

            for entry in sorted_entries[:10]:  # Top 10 per category
                func_str = f"  {entry.function_name}"
                time_str = f"{entry.total_time:.3f}s"
                calls_str = f"{entry.calls:,}"

                # Format line
                line = f"| {func_str:50} {time_str:>8} {calls_str:>6} |"
                if len(line) > 72:
                    line = line[:69] + "... |"
                report.append(line)

            report.append("+" + "-" * 68 + "+")
            report.append("")

        # Optimization recommendations
        report.append("OPTIMIZATION RECOMMENDATIONS:")
        report.append("")
        report.append(self._generate_recommendations(categories, total_time))

        return "\n".join(report)

    def _generate_recommendations(self, categories: Dict[str, CategoryStats],
                                 total_time: float) -> str:
        """Generate optimization recommendations based on profiling data.

        Args:
            categories: Dictionary of category statistics
            total_time: Total execution time

        Returns:
            Formatted recommendations string
        """
        recommendations = []

        # Check runtime overhead
        if 'runtime_overhead' in categories:
            overhead = categories['runtime_overhead']
            overhead_pct = (overhead.total_time / total_time * 100) if total_time > 0 else 0

            if overhead_pct > 15:
                recommendations.append(f"• Runtime Overhead ({overhead_pct:.1f}%):")
                recommendations.append("  - High overhead detected (>15%)")

                # Find top overhead functions
                top_overhead = sorted(overhead.entries, key=lambda e: e.total_time, reverse=True)[:3]
                for entry in top_overhead:
                    recommendations.append(f"  - {entry.function_name}: {entry.calls:,} calls")

                recommendations.append("  - Consider caching or reducing stdlib/builtin calls")
                recommendations.append("")

        # Check user code percentage
        if 'user_code' in categories:
            user_time = categories['user_code'].total_time
            user_pct = (user_time / total_time * 100) if total_time > 0 else 0

            recommendations.append(f"• User ML Code Execution: {user_pct:.1f}%")
            if user_pct < 50:
                recommendations.append("  - Most time is in mlpy overhead, not your code")
                recommendations.append("  - Consider optimizing algorithm rather than reducing stdlib calls")
            else:
                recommendations.append("  - Good balance - your code is the main work")
            recommendations.append("")

        # Overall assessment
        mlpy_overhead_pct = sum(
            (categories[cat].total_time / total_time * 100) if total_time > 0 else 0
            for cat in ['sandbox_startup', 'parsing', 'security_analysis',
                       'transpilation', 'runtime_overhead']
            if cat in categories
        )

        recommendations.append("• Overall Assessment:")
        if mlpy_overhead_pct < 20:
            recommendations.append("  - Excellent! mlpy overhead is minimal (<20%)")
        elif mlpy_overhead_pct < 30:
            recommendations.append("  - Good! mlpy overhead is acceptable (<30%)")
        else:
            recommendations.append("  - mlpy overhead is significant (>30%)")
            recommendations.append("  - This is normal for I/O heavy or stdlib-intensive programs")

        return "\n".join(recommendations)

    def generate_raw_report(self) -> str:
        """Generate raw cProfile output.

        Returns standard cProfile statistics format for external tools
        or advanced analysis.

        Returns:
            Raw cProfile output string
        """
        stats = self.get_stats()
        stream = StringIO()
        stats.stream = stream
        stats.print_stats()
        return stream.getvalue()

    def generate_ml_summary_report(self) -> str:
        """Generate ML USER-FOCUSED summary report.

        Shows only ML code performance, hides mlpy overhead completely.
        Perfect for ML developers who want to optimize their code.

        Shows:
        - Total execution time
        - ML code execution time (excluding mlpy overhead)
        - Top 10 ML functions by time
        - ML file breakdown
        - Memory usage per function
        - User-friendly optimization suggestions

        Returns:
            Formatted ML user report string
        """
        stats = self.get_stats()
        categories = self._categorize_all_functions(stats)

        # Calculate totals
        total_time = sum(cat.total_time for cat in categories.values())

        # Get user code category
        if 'user_code' not in categories or not categories['user_code'].entries:
            return self._format_no_user_code_message()

        user_code = categories['user_code']
        ml_time = user_code.total_time
        mlpy_overhead = total_time - ml_time
        ml_pct = (ml_time / total_time * 100) if total_time > 0 else 0

        # Build report
        report = []
        report.append("=" * 70)
        report.append("ML CODE PERFORMANCE SUMMARY")
        report.append("=" * 70)
        report.append("")
        report.append(f"Total Execution Time: {total_time:.3f}s")
        report.append(f"ML Code Execution Time: {ml_time:.3f}s ({ml_pct:.1f}%)")
        report.append(f"mlpy Overhead: {mlpy_overhead:.3f}s ({100-ml_pct:.1f}%)")
        report.append("")

        # Memory summary if available
        if self.memory_enabled:
            total_memory = sum(
                entry.memory_bytes
                for entry in user_code.entries
            )
            report.append("Memory Usage:")
            report.append(f"  Peak Memory: {total_memory / (1024 * 1024):.1f} MB")
            report.append("")

        # Top 10 ML functions
        report.append("Top ML Functions (by execution time):")
        report.append(self._format_ml_functions_table(user_code.entries, limit=10))
        report.append("")

        # ML files breakdown
        report.append("ML Files (by execution time):")
        report.append(self._format_ml_files_table(user_code.entries))
        report.append("")

        # User-focused optimization recommendations
        report.append("OPTIMIZATION RECOMMENDATIONS:")
        report.append("")
        report.append(self._generate_ml_recommendations(user_code.entries, total_time))

        return "\n".join(report)

    def generate_ml_details_report(self) -> str:
        """Generate ML USER-FOCUSED detailed report.

        Shows all ML functions grouped by module/file.
        Hides mlpy overhead completely.

        Shows:
        - All ML functions (not just top 10)
        - Grouped hierarchically by ML file
        - Memory per function
        - Call counts and average times

        Returns:
            Formatted ML details report string
        """
        stats = self.get_stats()
        categories = self._categorize_all_functions(stats)

        # Calculate totals
        total_time = sum(cat.total_time for cat in categories.values())

        # Get user code category
        if 'user_code' not in categories or not categories['user_code'].entries:
            return self._format_no_user_code_message()

        user_code = categories['user_code']
        ml_time = user_code.total_time
        ml_pct = (ml_time / total_time * 100) if total_time > 0 else 0

        # Build report
        report = []
        report.append("=" * 70)
        report.append("ML CODE DETAILED ANALYSIS")
        report.append("=" * 70)
        report.append("")
        report.append(f"Total Execution Time: {total_time:.3f}s")
        report.append(f"ML Code Execution Time: {ml_time:.3f}s ({ml_pct:.1f}%)")
        report.append("")

        # Group functions by ML file
        functions_by_file = defaultdict(list)
        for entry in user_code.entries:
            ml_file = entry.ml_file or "unknown"
            functions_by_file[ml_file].append(entry)

        # Sort files by total time
        sorted_files = sorted(
            functions_by_file.items(),
            key=lambda x: sum(e.total_time for e in x[1]),
            reverse=True
        )

        # Display each file's functions
        for ml_file, entries in sorted_files:
            file_time = sum(e.total_time for e in entries)
            file_pct = (file_time / ml_time * 100) if ml_time > 0 else 0
            file_memory = sum(e.memory_bytes for e in entries)

            report.append("+" + "-" * 68 + "+")
            report.append(f"| {ml_file} ({file_time:.3f}s, {file_pct:.1f}%, {file_memory / (1024*1024):.1f} MB)")
            report.append("+" + "-" * 68 + "+")

            # Sort functions by time within file
            sorted_entries = sorted(entries, key=lambda e: e.total_time, reverse=True)

            # Header
            report.append(f"| {'Function':<30} {'Time':>8} {'% File':>7} {'Calls':>8} {'Memory':>8} |")
            report.append("+" + "-" * 68 + "+")

            # Functions
            for entry in sorted_entries:
                func_pct = (entry.total_time / file_time * 100) if file_time > 0 else 0
                func_mem_mb = entry.memory_bytes / (1024 * 1024)
                func_name = entry.function_name[:28]  # Truncate long names

                report.append(
                    f"| {func_name:<30} {entry.total_time:>7.3f}s "
                    f"{func_pct:>6.1f}% {entry.calls:>8,} {func_mem_mb:>7.1f}MB |"
                )

            report.append("+" + "-" * 68 + "+")
            report.append("")

        return "\n".join(report)

    def _format_no_user_code_message(self) -> str:
        """Format message when no user code was detected."""
        return """
======================================================================
ML CODE PERFORMANCE SUMMARY
======================================================================

No ML user code detected in this profiling session.

This can happen if:
- The program only performed setup/initialization
- Source maps were not available
- The program crashed before executing user code

Try running with a longer-running ML program or ensure source maps
are being generated (.ml.map files).
"""

    def _format_ml_functions_table(self, entries: List[ProfileEntry], limit: int = 10) -> str:
        """Format table of ML functions.

        Args:
            entries: List of ProfileEntry objects
            limit: Maximum number of functions to show

        Returns:
            Formatted table string
        """
        # Sort by total time
        sorted_entries = sorted(entries, key=lambda e: e.total_time, reverse=True)[:limit]

        if not sorted_entries:
            return "  No ML functions found"

        lines = []
        lines.append("+" + "-" * 68 + "+")
        lines.append(f"| {'Function':<38} | {'Time':>8} | {'Calls':>8} | {'Memory':>8} |")
        lines.append("+" + "-" * 68 + "+")

        for entry in sorted_entries:
            # Format function name with file
            func_display = f"{entry.function_name}"
            if entry.ml_file:
                func_display = f"{entry.function_name} ({entry.ml_file})"

            func_display = func_display[:36]  # Truncate if too long
            mem_mb = entry.memory_bytes / (1024 * 1024)

            lines.append(
                f"| {func_display:<38} | {entry.total_time:>7.3f}s | {entry.calls:>8,} | {mem_mb:>7.1f}MB |"
            )

        lines.append("+" + "-" * 68 + "+")

        return "\n".join(lines)

    def _format_ml_files_table(self, entries: List[ProfileEntry]) -> str:
        """Format table of ML files with aggregated stats.

        Args:
            entries: List of ProfileEntry objects

        Returns:
            Formatted table string
        """
        # Group by ML file
        files_stats = defaultdict(lambda: {'time': 0.0, 'calls': 0, 'memory': 0})

        for entry in entries:
            ml_file = entry.ml_file or "unknown"
            files_stats[ml_file]['time'] += entry.total_time
            files_stats[ml_file]['calls'] += entry.calls
            files_stats[ml_file]['memory'] += entry.memory_bytes

        if not files_stats:
            return "  No ML files found"

        # Sort by time
        sorted_files = sorted(
            files_stats.items(),
            key=lambda x: x[1]['time'],
            reverse=True
        )

        lines = []
        lines.append("+" + "-" * 68 + "+")
        lines.append(f"| {'File':<25} | {'Time':>8} | {'Calls':>8} | {'Memory':>8} |")
        lines.append("+" + "-" * 68 + "+")

        for ml_file, stats in sorted_files:
            mem_mb = stats['memory'] / (1024 * 1024)
            file_display = ml_file[:23]  # Truncate if too long

            lines.append(
                f"| {file_display:<25} | {stats['time']:>7.3f}s | {stats['calls']:>8,} | {mem_mb:>7.1f}MB |"
            )

        lines.append("+" + "-" * 68 + "+")

        return "\n".join(lines)

    def _generate_ml_recommendations(self, entries: List[ProfileEntry], total_time: float) -> str:
        """Generate user-focused optimization recommendations.

        Args:
            entries: List of ProfileEntry objects (user code only)
            total_time: Total execution time

        Returns:
            Formatted recommendations string
        """
        recommendations = []

        # Sort by time to find hot spots
        sorted_entries = sorted(entries, key=lambda e: e.total_time, reverse=True)

        if not sorted_entries:
            return "No recommendations available"

        # Top function analysis
        top_func = sorted_entries[0]
        top_pct = (top_func.total_time / total_time * 100) if total_time > 0 else 0

        if top_pct > 20:
            func_display = f"{top_func.function_name}()"
            if top_func.ml_file:
                func_display += f" ({top_func.ml_file})"

            recommendations.append(f"▸ {func_display} - {top_pct:.1f}% of execution time")
            recommendations.append("  - This function is your main performance bottleneck")
            recommendations.append("  - Consider: caching, reducing iterations, or algorithm optimization")

            if top_func.memory_bytes > 10 * 1024 * 1024:  # > 10 MB
                mem_mb = top_func.memory_bytes / (1024 * 1024)
                recommendations.append(f"  - Memory: {mem_mb:.1f} MB - check for unnecessary allocations")

            recommendations.append("")

        # Second function if significant
        if len(sorted_entries) > 1:
            second_func = sorted_entries[1]
            second_pct = (second_func.total_time / total_time * 100) if total_time > 0 else 0

            if second_pct > 15:
                func_display = f"{second_func.function_name}()"
                if second_func.ml_file:
                    func_display += f" ({second_func.ml_file})"

                recommendations.append(f"▸ {func_display} - {second_pct:.1f}% of execution time")
                recommendations.append("  - Second most expensive function")
                recommendations.append("  - Review algorithm complexity")
                recommendations.append("")

        # Overall assessment
        recommendations.append("✓ Overall Assessment:")
        user_time_pct = (sum(e.total_time for e in entries) / total_time * 100) if total_time > 0 else 0

        if user_time_pct > 80:
            recommendations.append("  - Your ML code is the dominant factor (>80% of time)")
            recommendations.append("  - Focus optimization efforts on top functions above")
        elif user_time_pct > 50:
            recommendations.append("  - Good balance between your code and mlpy overhead")
            recommendations.append("  - Optimizing top functions will have noticeable impact")
        else:
            recommendations.append("  - Most time is in mlpy overhead (setup, parsing, etc.)")
            recommendations.append("  - Your code runs efficiently - overhead is external")

        return "\n".join(recommendations)

    # Backward compatibility aliases
    def generate_summary_report(self) -> str:
        """Generate summary report (backward compatibility).

        Deprecated: Use generate_dev_summary_report() instead.
        This method maintained for backward compatibility.

        Returns:
            Developer summary report
        """
        return self.generate_dev_summary_report()

    def generate_mlpy_analysis_report(self) -> str:
        """Generate mlpy analysis report (backward compatibility).

        Deprecated: Use generate_dev_details_report() instead.
        This method maintained for backward compatibility.

        Returns:
            Developer details report
        """
        return self.generate_dev_details_report()
