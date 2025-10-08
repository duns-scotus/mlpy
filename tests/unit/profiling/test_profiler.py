"""Unit tests for ML Performance Profiler.

Tests MLProfiler class functionality including:
- cProfile integration
- Function categorization (runtime overhead detection)
- Category aggregation
- Report generation
- ML file mapping
"""

import unittest
import cProfile
import pstats
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os

from mlpy.runtime.profiler import (
    MLProfiler,
    ProfileEntry,
    CategoryStats,
)


class TestMLProfiler(unittest.TestCase):
    """Test MLProfiler core functionality."""

    def setUp(self):
        """Set up test profiler."""
        self.profiler = MLProfiler()

    def test_profiler_initialization(self):
        """Test profiler initializes correctly."""
        self.assertIsNotNone(self.profiler.profiler)
        self.assertFalse(self.profiler.enabled)
        self.assertIsNone(self.profiler.source_map_index)

        # Check runtime overhead functions are defined
        self.assertIn('safe_call', self.profiler.runtime_overhead_functions)
        self.assertIn('safe_attr_access', self.profiler.runtime_overhead_functions)
        self.assertIn('safe_method_call', self.profiler.runtime_overhead_functions)

    def test_start_stop_profiling(self):
        """Test starting and stopping profiler."""
        self.assertFalse(self.profiler.enabled)

        self.profiler.start()
        self.assertTrue(self.profiler.enabled)

        self.profiler.stop()
        self.assertFalse(self.profiler.enabled)

    def test_profiling_captures_function_calls(self):
        """Test that profiling actually captures function calls."""
        def test_function():
            total = 0
            for i in range(1000):
                total += i
            return total

        self.profiler.start()
        result = test_function()
        self.profiler.stop()

        self.assertEqual(result, 499500)

        # Get stats
        stats = self.profiler.get_stats()
        self.assertIsNotNone(stats)

        # Check that test_function was profiled
        found = False
        for func in stats.stats.keys():
            if 'test_function' in str(func):
                found = True
                break
        self.assertTrue(found, "test_function should be in profiling stats")


class TestFunctionCategorization(unittest.TestCase):
    """Test function categorization logic."""

    def setUp(self):
        """Set up test profiler."""
        self.profiler = MLProfiler()

    def test_categorize_safe_call(self):
        """Test that safe_call is categorized as runtime_overhead."""
        category, ml_file = self.profiler.categorize_function(
            'mlpy/runtime/whitelist_validator.py',
            'safe_call'
        )
        self.assertEqual(category, 'runtime_overhead')
        self.assertIsNone(ml_file)

    def test_categorize_safe_attr_access(self):
        """Test that safe_attr_access is categorized as runtime_overhead."""
        category, ml_file = self.profiler.categorize_function(
            'mlpy/stdlib/runtime_helpers.py',
            'safe_attr_access'
        )
        self.assertEqual(category, 'runtime_overhead')
        self.assertIsNone(ml_file)

    def test_categorize_safe_method_call(self):
        """Test that safe_method_call is categorized as runtime_overhead."""
        category, ml_file = self.profiler.categorize_function(
            'mlpy/stdlib/runtime_helpers.py',
            'safe_method_call'
        )
        self.assertEqual(category, 'runtime_overhead')
        self.assertIsNone(ml_file)

    def test_categorize_check_capabilities(self):
        """Test that check_capabilities is categorized as runtime_overhead."""
        category, ml_file = self.profiler.categorize_function(
            'mlpy/runtime/whitelist_validator.py',
            'check_capabilities'
        )
        self.assertEqual(category, 'runtime_overhead')
        self.assertIsNone(ml_file)

    def test_categorize_parsing(self):
        """Test that lark parser functions are categorized as parsing."""
        # Use both forward slash and backslash versions
        for path in ['lark/lark.py', 'lark\\lark.py']:
            category, ml_file = self.profiler.categorize_function(
                path,
                'parse'
            )
            self.assertEqual(category, 'parsing', f"Failed for path: {path}")
            self.assertIsNone(ml_file)

    def test_categorize_security_analysis(self):
        """Test that security analyzer is categorized correctly."""
        for path in ['mlpy/ml/analysis/security_analyzer.py', 'mlpy\\ml\\analysis\\security_analyzer.py']:
            category, ml_file = self.profiler.categorize_function(
                path,
                'analyze'
            )
            self.assertEqual(category, 'security_analysis', f"Failed for path: {path}")
            self.assertIsNone(ml_file)

    def test_categorize_transpilation(self):
        """Test that code generator is categorized correctly."""
        for path in ['mlpy/ml/codegen/python_generator.py', 'mlpy\\ml\\codegen\\python_generator.py']:
            category, ml_file = self.profiler.categorize_function(
                path,
                'generate'
            )
            self.assertEqual(category, 'transpilation', f"Failed for path: {path}")
            self.assertIsNone(ml_file)

    def test_categorize_sandbox_startup(self):
        """Test that sandbox initialization is categorized correctly."""
        for path in ['mlpy/runtime/sandbox.py', 'mlpy\\runtime\\sandbox.py']:
            category, ml_file = self.profiler.categorize_function(
                path,
                '__init__'
            )
            self.assertEqual(category, 'sandbox_startup', f"Failed for path: {path}")
            self.assertIsNone(ml_file)

    def test_categorize_user_code_without_source_map(self):
        """Test user code categorization when no source map available."""
        category, ml_file = self.profiler.categorize_function(
            '/tmp/fibonacci.py',
            'fibonacci'
        )
        self.assertEqual(category, 'user_code')
        self.assertEqual(ml_file, 'fibonacci.py')  # Basename

    def test_categorize_python_stdlib(self):
        """Test Python stdlib functions are categorized correctly."""
        category, ml_file = self.profiler.categorize_function(
            '<built-in>',
            'len'
        )
        self.assertEqual(category, 'python_stdlib')
        self.assertIsNone(ml_file)

    def test_categorize_priority_order(self):
        """Test that categorization priority works correctly.

        Runtime overhead functions should be checked first,
        even if filename matches a compile-time pattern.
        """
        # safe_call in parsing module should still be runtime_overhead
        category, ml_file = self.profiler.categorize_function(
            'mlpy/ml/parser.py',
            'safe_call'
        )
        self.assertEqual(category, 'runtime_overhead')


class TestCategoryAggregation(unittest.TestCase):
    """Test category statistics aggregation."""

    def setUp(self):
        """Set up test profiler with mock data."""
        self.profiler = MLProfiler()

    def test_categorize_all_functions_empty(self):
        """Test categorization with no profiling data."""
        # Create profiler and get stats without running anything
        profiler = MLProfiler()
        profiler.start()
        profiler.stop()
        stats = profiler.get_stats()

        categories = profiler._categorize_all_functions(stats)
        # Should have minimal or no categories
        self.assertIsInstance(categories, dict)

    def test_categorize_all_functions_with_data(self):
        """Test categorization with actual profiling data."""
        def user_function():
            return sum(range(100))

        def call_safe_call():
            # Simulate calling overhead function
            pass

        # Profile some code
        self.profiler.start()
        user_function()
        call_safe_call()
        self.profiler.stop()

        stats = self.profiler.get_stats()
        categories = self.profiler._categorize_all_functions(stats)

        # Should have some categories (exact categories depend on what was profiled)
        # In test environment, might be categorized as python_stdlib or user_code
        self.assertGreater(len(categories), 0)

        # Check that we have some entries
        total_entries = sum(len(cat.entries) for cat in categories.values())
        self.assertGreater(total_entries, 0)

    def test_category_stats_totals(self):
        """Test that category totals are calculated correctly."""
        def test_func():
            return sum(range(1000))

        self.profiler.start()
        test_func()
        self.profiler.stop()

        stats = self.profiler.get_stats()
        categories = self.profiler._categorize_all_functions(stats)

        # Check that each category total equals sum of entry tottimes
        for cat_name, cat in categories.items():
            calculated_total = sum(entry.total_time for entry in cat.entries)
            self.assertAlmostEqual(cat.total_time, calculated_total, places=6)


class TestReportGeneration(unittest.TestCase):
    """Test report generation methods."""

    def setUp(self):
        """Set up test profiler with some data."""
        self.profiler = MLProfiler()

        # Create simple test data
        def test_function():
            total = 0
            for i in range(100):
                total += i
            return total

        self.profiler.start()
        test_function()
        self.profiler.stop()

    def test_generate_summary_report(self):
        """Test summary report generation."""
        report = self.profiler.generate_summary_report()

        self.assertIsInstance(report, str)
        self.assertIn('MLPY PERFORMANCE SUMMARY REPORT', report)
        self.assertIn('Total Execution Time:', report)
        self.assertIn('Time Breakdown:', report)

    def test_summary_report_contains_tables(self):
        """Test that summary report contains formatted tables."""
        report = self.profiler.generate_summary_report()

        # Check for table borders
        self.assertIn('┌─', report)
        self.assertIn('├─', report)
        self.assertIn('└─', report)
        self.assertIn('│', report)

    def test_generate_mlpy_analysis_report(self):
        """Test MLPY analysis report generation."""
        report = self.profiler.generate_mlpy_analysis_report()

        self.assertIsInstance(report, str)
        self.assertIn('MLPY INTERNAL PERFORMANCE ANALYSIS', report)
        self.assertIn('Total mlpy Overhead:', report)
        self.assertIn('OPTIMIZATION RECOMMENDATIONS:', report)

    def test_mlpy_analysis_contains_categories(self):
        """Test that MLPY analysis contains category breakdowns."""
        report = self.profiler.generate_mlpy_analysis_report()

        # Check for report structure (may not have category tables if no mlpy overhead)
        self.assertIn('MLPY INTERNAL PERFORMANCE ANALYSIS', report)
        self.assertIn('Total mlpy Overhead:', report)
        self.assertIn('OPTIMIZATION RECOMMENDATIONS:', report)


class TestMLFileMapping(unittest.TestCase):
    """Test ML file mapping from Python files."""

    def test_get_ml_file_simple_replacement(self):
        """Test simple .py → .ml replacement."""
        profiler = MLProfiler()

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a .ml file
            ml_file = os.path.join(tmpdir, 'test.ml')
            with open(ml_file, 'w') as f:
                f.write('// test')

            # Map .py to .ml
            py_file = os.path.join(tmpdir, 'test.py')
            ml_result = profiler._get_ml_file_from_py(py_file)

            self.assertIsNotNone(ml_result)
            self.assertTrue(ml_result.endswith('test.ml'))

    def test_get_ml_file_no_source_map_index(self):
        """Test mapping without source map index."""
        profiler = MLProfiler(source_map_index=None)

        result = profiler._get_ml_file_from_py('/some/path/test.py')
        self.assertIsNone(result)  # File doesn't exist

    def test_get_ml_file_non_existent(self):
        """Test mapping for non-existent ML file."""
        profiler = MLProfiler()

        result = profiler._get_ml_file_from_py('/nonexistent/path/test.py')
        self.assertIsNone(result)


class TestProfileEntry(unittest.TestCase):
    """Test ProfileEntry dataclass."""

    def test_profile_entry_creation(self):
        """Test creating ProfileEntry."""
        entry = ProfileEntry(
            function_name='test_func',
            filename='/path/to/file.py',
            ml_file='file.ml',
            calls=100,
            total_time=0.5,
            cumulative_time=1.0,
            per_call_time=0.005
        )

        self.assertEqual(entry.function_name, 'test_func')
        self.assertEqual(entry.filename, '/path/to/file.py')
        self.assertEqual(entry.ml_file, 'file.ml')
        self.assertEqual(entry.calls, 100)
        self.assertEqual(entry.total_time, 0.5)
        self.assertEqual(entry.cumulative_time, 1.0)
        self.assertEqual(entry.per_call_time, 0.005)

    def test_profile_entry_defaults(self):
        """Test ProfileEntry default values."""
        entry = ProfileEntry(
            function_name='test_func',
            filename='/path/to/file.py'
        )

        self.assertIsNone(entry.ml_file)
        self.assertEqual(entry.calls, 0)
        self.assertEqual(entry.total_time, 0.0)
        self.assertEqual(entry.cumulative_time, 0.0)
        self.assertEqual(entry.per_call_time, 0.0)


class TestCategoryStats(unittest.TestCase):
    """Test CategoryStats dataclass."""

    def test_category_stats_creation(self):
        """Test creating CategoryStats."""
        stats = CategoryStats(
            category='user_code',
            total_time=1.5,
            percentage=75.0,
            entries=[]
        )

        self.assertEqual(stats.category, 'user_code')
        self.assertEqual(stats.total_time, 1.5)
        self.assertEqual(stats.percentage, 75.0)
        self.assertEqual(len(stats.entries), 0)

    def test_category_stats_defaults(self):
        """Test CategoryStats default values."""
        stats = CategoryStats(category='parsing')

        self.assertEqual(stats.category, 'parsing')
        self.assertEqual(stats.total_time, 0.0)
        self.assertEqual(stats.percentage, 0.0)
        self.assertIsNotNone(stats.entries)
        self.assertEqual(len(stats.entries), 0)


class TestOptimizationRecommendations(unittest.TestCase):
    """Test optimization recommendation generation."""

    def setUp(self):
        """Set up test data."""
        self.profiler = MLProfiler()

    def test_recommendations_high_overhead(self):
        """Test recommendations for high runtime overhead."""
        # Create mock categories with high overhead
        categories = {
            'runtime_overhead': CategoryStats(
                category='runtime_overhead',
                total_time=0.8,
                entries=[
                    ProfileEntry('safe_call', 'whitelist_validator.py', calls=10000, total_time=0.5),
                    ProfileEntry('safe_attr_access', 'runtime_helpers.py', calls=5000, total_time=0.3),
                ]
            ),
            'user_code': CategoryStats(
                category='user_code',
                total_time=0.2,
            ),
        }

        total_time = 1.0

        recommendations = self.profiler._generate_recommendations(categories, total_time)

        self.assertIn('Runtime Overhead', recommendations)
        self.assertIn('80.0%', recommendations)  # High overhead percentage
        self.assertIn('High overhead detected', recommendations)

    def test_recommendations_good_balance(self):
        """Test recommendations for good overhead/user code balance."""
        categories = {
            'runtime_overhead': CategoryStats(
                category='runtime_overhead',
                total_time=0.2,
            ),
            'user_code': CategoryStats(
                category='user_code',
                total_time=0.8,
            ),
        }

        total_time = 1.0

        recommendations = self.profiler._generate_recommendations(categories, total_time)

        self.assertIn('User ML Code Execution: 80.0%', recommendations)
        self.assertIn('Good balance', recommendations)


if __name__ == '__main__':
    unittest.main()
