"""
Unit tests for parallel_analyzer.py - Parallel security analysis engine.

Tests cover:
- AnalysisResult dataclass
- ParallelSecurityAnalyzer initialization and configuration
- Parallel analysis execution
- Thread-local analyzer instances
- Cache mechanism (hits, misses, storage, retrieval)
- Batch analysis of multiple code samples
- Syntax error handling
- Comprehensive report generation
- Performance metrics and statistics
"""

import ast
import pytest
from mlpy.ml.analysis.parallel_analyzer import (
    ParallelSecurityAnalyzer,
    AnalysisResult,
)
from mlpy.ml.analysis.pattern_detector import PatternMatch, SecurityPattern, ThreatLevel


class TestAnalysisResult:
    """Test AnalysisResult dataclass."""

    def test_result_creation(self):
        """Test creating analysis result."""
        result = AnalysisResult(
            pattern_matches=[],
            ast_violations=[],
            data_flow_results={},
            analysis_time=0.5,
            cache_hits=0,
            cache_misses=1,
        )

        assert result.pattern_matches == []
        assert result.ast_violations == []
        assert result.data_flow_results == {}
        assert result.analysis_time == 0.5
        assert result.cache_hits == 0
        assert result.cache_misses == 1


class TestParallelSecurityAnalyzer:
    """Test ParallelSecurityAnalyzer main functionality."""

    @pytest.fixture
    def analyzer(self):
        """Create parallel analyzer."""
        return ParallelSecurityAnalyzer(max_workers=2)

    def test_analyzer_initialization(self, analyzer):
        """Test analyzer initialization."""
        assert analyzer is not None
        assert analyzer.max_workers == 2
        assert analyzer.cache_hits == 0
        assert analyzer.cache_misses == 0

    def test_analyze_safe_code(self, analyzer):
        """Test analyzing safe code."""
        code = """
x = 42
y = x + 10
print(y)
"""
        result = analyzer.analyze_parallel(code)

        assert isinstance(result, AnalysisResult)
        assert result.analysis_time >= 0

        # Safe code should have minimal violations
        critical_patterns = [m for m in result.pattern_matches if m.pattern.threat_level == ThreatLevel.CRITICAL]
        critical_ast = [v for v in result.ast_violations if v.severity == ThreatLevel.CRITICAL]
        assert len(critical_patterns) == 0
        assert len(critical_ast) == 0

    def test_analyze_dangerous_code(self, analyzer):
        """Test analyzing dangerous code."""
        code = """
import os
result = eval(user_input)
"""
        result = analyzer.analyze_parallel(code)

        # Should detect violations
        total_issues = len(result.pattern_matches) + len(result.ast_violations)
        assert total_issues > 0

    def test_thread_local_analyzers(self, analyzer):
        """Test thread-local analyzer instances."""
        # Get analyzers in main thread
        analyzers1 = analyzer._get_analyzers()
        analyzers2 = analyzer._get_analyzers()

        # Should return same instance in same thread
        assert analyzers1 is analyzers2

    def test_cache_key_generation(self, analyzer):
        """Test cache key generation."""
        code1 = "x = 42"
        code2 = "y = 10"

        key1 = analyzer._get_cache_key(code1, "test.py")
        key2 = analyzer._get_cache_key(code1, "test.py")
        key3 = analyzer._get_cache_key(code2, "test.py")

        # Same code should generate same key
        assert key1 == key2

        # Different code should generate different key
        assert key1 != key3

    def test_cache_hit(self, analyzer):
        """Test cache hit on second analysis."""
        code = "x = 42"

        # First analysis - cache miss
        result1 = analyzer.analyze_parallel(code, enable_cache=True)
        assert analyzer.cache_misses == 1
        assert analyzer.cache_hits == 0

        # Second analysis - cache hit
        result2 = analyzer.analyze_parallel(code, enable_cache=True)
        assert analyzer.cache_hits == 1

        # Results should have same content
        assert len(result1.pattern_matches) == len(result2.pattern_matches)
        assert len(result1.ast_violations) == len(result2.ast_violations)

    def test_cache_disabled(self, analyzer):
        """Test analysis with cache disabled."""
        code = "x = 42"

        result1 = analyzer.analyze_parallel(code, enable_cache=False)
        result2 = analyzer.analyze_parallel(code, enable_cache=False)

        # Should not use cache (hits should be 0)
        # Note: cache_misses still increments when cache is disabled
        assert analyzer.cache_hits == 0

    def test_syntax_error_handling(self, analyzer):
        """Test handling code with syntax errors."""
        code = "def broken("  # Invalid syntax

        result = analyzer.analyze_parallel(code)

        # Should return result without crashing
        assert isinstance(result, AnalysisResult)
        # AST analysis should be empty due to syntax error
        assert len(result.ast_violations) == 0

    def test_analyze_batch(self, analyzer):
        """Test batch analysis of multiple files."""
        samples = [
            ("x = 42", "file1.py"),
            ("y = 10", "file2.py"),
            ("eval(x)", "file3.py"),
        ]

        results = analyzer.analyze_batch(samples)

        # Should return results for all samples
        assert len(results) == 3
        assert all(isinstance(r, AnalysisResult) for r in results)

    def test_cache_statistics(self, analyzer):
        """Test cache statistics."""
        code = "x = 42"

        # Perform some analyses
        analyzer.analyze_parallel(code, enable_cache=True)
        analyzer.analyze_parallel(code, enable_cache=True)

        stats = analyzer.get_cache_statistics()

        assert "cache_hits" in stats
        assert "cache_misses" in stats
        assert "hit_rate" in stats
        assert stats["cache_hits"] > 0

    def test_cache_hit_rate_calculation(self, analyzer):
        """Test cache hit rate calculation."""
        code1 = "x = 42"
        code2 = "y = 10"

        # One cache miss
        analyzer.analyze_parallel(code1, enable_cache=True)

        # One cache hit
        analyzer.analyze_parallel(code1, enable_cache=True)

        # Another cache miss
        analyzer.analyze_parallel(code2, enable_cache=True)

        stats = analyzer.get_cache_statistics()

        # Hit rate should be 1/(1+2) = 0.333...
        assert stats["hit_rate"] > 0
        assert stats["hit_rate"] < 1

    def test_clear_cache(self, analyzer):
        """Test clearing cache."""
        code = "x = 42"

        # Fill cache
        analyzer.analyze_parallel(code, enable_cache=True)
        assert analyzer.cache_hits + analyzer.cache_misses > 0

        # Clear cache
        analyzer.clear_cache()

        assert analyzer.cache_hits == 0
        assert analyzer.cache_misses == 0

        stats = analyzer.get_cache_statistics()
        assert stats["cached_patterns"] == 0
        assert stats["cached_ast_results"] == 0

    def test_comprehensive_report(self, analyzer):
        """Test comprehensive report generation."""
        code = """
import os
eval(code)
"""
        result = analyzer.analyze_parallel(code)
        report = analyzer.create_comprehensive_report(result)

        assert isinstance(report, dict)
        assert "summary" in report
        assert "threat_breakdown" in report
        assert "recommendations" in report

    def test_report_threat_counts(self, analyzer):
        """Test threat counting in report."""
        code = "eval(x)"
        result = analyzer.analyze_parallel(code)
        report = analyzer.create_comprehensive_report(result)

        threat_breakdown = report["threat_breakdown"]
        assert isinstance(threat_breakdown, dict)
        assert "critical" in threat_breakdown

    def test_report_summary_structure(self, analyzer):
        """Test report summary structure."""
        code = "x = 42"
        result = analyzer.analyze_parallel(code)
        report = analyzer.create_comprehensive_report(result)

        summary = report["summary"]
        assert "total_threats" in summary
        assert "pattern_matches" in summary
        assert "ast_violations" in summary
        assert "analysis_time" in summary
        assert "performance" in summary

    def test_recommendations_generation(self, analyzer):
        """Test security recommendations generation."""
        code = """
user_input = input()
eval(user_input)
"""
        result = analyzer.analyze_parallel(code)
        report = analyzer.create_comprehensive_report(result)

        recommendations = report["recommendations"]
        assert isinstance(recommendations, list)
        # Should have some recommendations for dangerous code
        assert len(recommendations) > 0

    def test_recommendations_limit(self, analyzer):
        """Test recommendations are limited to top 10."""
        code = """
import os
import sys
import subprocess
eval(x)
exec(y)
compile(z)
"""
        result = analyzer.analyze_parallel(code)
        recommendations = analyzer._generate_recommendations(result)

        # Should limit to 10 recommendations max
        assert len(recommendations) <= 10

    def test_parallel_execution(self, analyzer):
        """Test that analysis runs in parallel."""
        code = "x = 42"

        # Run analysis
        result = analyzer.analyze_parallel(code)

        # Should complete successfully
        assert result.analysis_time >= 0

    def test_max_workers_configuration(self):
        """Test configuring max workers."""
        analyzer1 = ParallelSecurityAnalyzer(max_workers=1)
        analyzer2 = ParallelSecurityAnalyzer(max_workers=4)

        assert analyzer1.max_workers == 1
        assert analyzer2.max_workers == 4

    def test_filename_in_cache_key(self, analyzer):
        """Test filename affects cache key."""
        code = "x = 42"

        key1 = analyzer._get_cache_key(code, "file1.py")
        key2 = analyzer._get_cache_key(code, "file2.py")

        # Different filenames should create different keys
        assert key1 != key2

    def test_batch_error_handling(self, analyzer):
        """Test batch analysis handles errors gracefully."""
        samples = [
            ("x = 42", "good.py"),
            ("def broken(", "bad.py"),  # Syntax error
        ]

        results = analyzer.analyze_batch(samples)

        # Should return results for all, even with errors
        assert len(results) == 2

    def test_cache_size_limit(self, analyzer):
        """Test cache size limiting."""
        # This is a stress test - skip in normal runs
        # Fill cache beyond limit
        for i in range(50):
            code = f"x = {i}"
            analyzer.analyze_parallel(code, enable_cache=True)

        # Cache should still be functional
        stats = analyzer.get_cache_statistics()
        assert stats["cached_patterns"] <= 1000


class TestParallelAnalyzerIntegration:
    """Integration tests for parallel analyzer."""

    @pytest.fixture
    def analyzer(self):
        """Create analyzer."""
        return ParallelSecurityAnalyzer(max_workers=3)

    def test_full_analysis_pipeline(self, analyzer):
        """Test complete analysis pipeline."""
        code = """
import subprocess
user_input = input()
subprocess.call(user_input)
"""
        result = analyzer.analyze_parallel(code)

        # Should detect multiple types of issues
        assert len(result.pattern_matches) > 0 or len(result.ast_violations) > 0

        # Should have data flow results
        assert isinstance(result.data_flow_results, dict)

    def test_report_with_violations(self, analyzer):
        """Test report generation with violations."""
        code = """
eval(code)
exec(code)
import os
"""
        result = analyzer.analyze_parallel(code)
        report = analyzer.create_comprehensive_report(result)

        # Should have detected threats
        assert report["summary"]["total_threats"] > 0

        # Should have threat breakdown
        breakdown = report["threat_breakdown"]
        total_counted = sum(breakdown.values())
        assert total_counted > 0

    def test_cache_performance_benefit(self, analyzer):
        """Test cache provides performance benefit."""
        code = "x = 42"

        # First run (uncached)
        result1 = analyzer.analyze_parallel(code, enable_cache=True)
        time1 = result1.analysis_time

        # Second run (cached)
        result2 = analyzer.analyze_parallel(code, enable_cache=True)
        time2 = result2.analysis_time

        # Cached result should be instant (0.0)
        assert time2 == 0.0
        assert time1 > time2

    def test_batch_parallel_processing(self, analyzer):
        """Test batch processing uses parallelization."""
        samples = [
            ("x = 1", "f1.py"),
            ("x = 2", "f2.py"),
            ("x = 3", "f3.py"),
            ("x = 4", "f4.py"),
        ]

        results = analyzer.analyze_batch(samples, enable_cache=False)

        # All should complete
        assert len(results) == 4
        assert all(r.analysis_time >= 0 for r in results)

    def test_data_flow_integration(self, analyzer):
        """Test data flow analysis integration."""
        code = """
user_input = input()
data = user_input
eval(data)
"""
        result = analyzer.analyze_parallel(code)

        # Should have data flow results
        assert "summary" in result.data_flow_results or "violations" in result.data_flow_results
