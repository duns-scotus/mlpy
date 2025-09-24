"""Parallel security analysis engine for improved performance."""

import ast
import concurrent.futures
import threading
import time
from dataclasses import dataclass
from typing import Any

from .ast_analyzer import ASTSecurityAnalyzer, SecurityViolation
from .data_flow_tracker import DataFlowTracker
from .pattern_detector import AdvancedPatternDetector, PatternMatch


@dataclass
class AnalysisResult:
    """Combined analysis result from parallel processing."""

    pattern_matches: list[PatternMatch]
    ast_violations: list[SecurityViolation]
    data_flow_results: dict[str, Any]
    analysis_time: float
    cache_hits: int
    cache_misses: int


class ParallelSecurityAnalyzer:
    """High-performance parallel security analyzer."""

    def __init__(self, max_workers: int = 3):
        """Initialize parallel analyzer."""
        self.max_workers = max_workers

        # Thread-local storage for analyzers to avoid shared state issues
        self._thread_local = threading.local()

        # Analysis cache for performance
        self._cache_lock = threading.RLock()
        self._pattern_cache: dict[str, list[PatternMatch]] = {}
        self._ast_cache: dict[str, list[SecurityViolation]] = {}
        self._flow_cache: dict[str, dict[str, Any]] = {}

        # Performance metrics
        self.cache_hits = 0
        self.cache_misses = 0

    def _get_analyzers(
        self,
    ) -> tuple[AdvancedPatternDetector, ASTSecurityAnalyzer, DataFlowTracker]:
        """Get thread-local analyzer instances."""
        if not hasattr(self._thread_local, "analyzers"):
            detector = AdvancedPatternDetector()
            ast_analyzer = ASTSecurityAnalyzer(detector)
            flow_tracker = DataFlowTracker()

            self._thread_local.analyzers = (detector, ast_analyzer, flow_tracker)

        return self._thread_local.analyzers

    def _get_cache_key(self, code: str, filename: str | None = None) -> str:
        """Generate cache key for code analysis."""
        # Use hash of code content for cache key
        import hashlib

        content_hash = hashlib.md5(code.encode("utf-8")).hexdigest()
        return f"{filename or 'unnamed'}:{content_hash}"

    def analyze_parallel(
        self, code: str, filename: str | None = None, enable_cache: bool = True
    ) -> AnalysisResult:
        """Perform parallel security analysis."""
        start_time = time.time()

        cache_key = self._get_cache_key(code, filename) if enable_cache else None

        # Check cache first
        if enable_cache and cache_key:
            cached_result = self._check_cache(cache_key)
            if cached_result:
                self.cache_hits += 1
                return cached_result

        self.cache_misses += 1

        # Prepare AST once for all analyzers
        try:
            ast_tree = ast.parse(code)
        except SyntaxError:
            # If code has syntax errors, only run pattern detection
            return self._analyze_with_syntax_error(code, filename, start_time)

        # Run analyses in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit parallel tasks
            pattern_future = executor.submit(self._analyze_patterns, code, filename)
            ast_future = executor.submit(self._analyze_ast, ast_tree, code, filename)
            flow_future = executor.submit(self._analyze_data_flow, ast_tree, code, filename)

            # Collect results
            pattern_matches = pattern_future.result()
            ast_violations = ast_future.result()
            data_flow_results = flow_future.result()

        analysis_time = time.time() - start_time

        result = AnalysisResult(
            pattern_matches=pattern_matches,
            ast_violations=ast_violations,
            data_flow_results=data_flow_results,
            analysis_time=analysis_time,
            cache_hits=self.cache_hits,
            cache_misses=self.cache_misses,
        )

        # Cache the result
        if enable_cache and cache_key:
            self._store_cache(cache_key, result)

        return result

    def _analyze_patterns(self, code: str, filename: str | None) -> list[PatternMatch]:
        """Run pattern analysis in separate thread."""
        detector, _, _ = self._get_analyzers()
        return detector.scan_code(code, filename)

    def _analyze_ast(
        self, ast_tree: ast.AST, code: str, filename: str | None
    ) -> list[SecurityViolation]:
        """Run AST analysis in separate thread."""
        _, ast_analyzer, _ = self._get_analyzers()
        return ast_analyzer.analyze(ast_tree, code, filename)

    def _analyze_data_flow(
        self, ast_tree: ast.AST, code: str, filename: str | None
    ) -> dict[str, Any]:
        """Run data flow analysis in separate thread."""
        _, _, flow_tracker = self._get_analyzers()
        return flow_tracker.track_data_flows(ast_tree, code, filename)

    def _analyze_with_syntax_error(
        self, code: str, filename: str | None, start_time: float
    ) -> AnalysisResult:
        """Handle analysis when code has syntax errors."""
        detector, _, _ = self._get_analyzers()
        pattern_matches = detector.scan_code(code, filename)

        return AnalysisResult(
            pattern_matches=pattern_matches,
            ast_violations=[],
            data_flow_results={"summary": {}, "violations": []},
            analysis_time=time.time() - start_time,
            cache_hits=self.cache_hits,
            cache_misses=self.cache_misses,
        )

    def _check_cache(self, cache_key: str) -> AnalysisResult | None:
        """Check if analysis result is cached."""
        with self._cache_lock:
            pattern_matches = self._pattern_cache.get(cache_key)
            ast_violations = self._ast_cache.get(cache_key)
            flow_results = self._flow_cache.get(cache_key)

            if (
                pattern_matches is not None
                and ast_violations is not None
                and flow_results is not None
            ):
                return AnalysisResult(
                    pattern_matches=pattern_matches,
                    ast_violations=ast_violations,
                    data_flow_results=flow_results,
                    analysis_time=0.0,  # Cached result
                    cache_hits=self.cache_hits,
                    cache_misses=self.cache_misses,
                )

        return None

    def _store_cache(self, cache_key: str, result: AnalysisResult) -> None:
        """Store analysis result in cache."""
        with self._cache_lock:
            self._pattern_cache[cache_key] = result.pattern_matches
            self._ast_cache[cache_key] = result.ast_violations
            self._flow_cache[cache_key] = result.data_flow_results

            # Limit cache size to prevent memory issues
            max_cache_size = 1000
            if len(self._pattern_cache) > max_cache_size:
                # Remove oldest entries (simplified LRU)
                keys_to_remove = list(self._pattern_cache.keys())[:100]
                for key in keys_to_remove:
                    self._pattern_cache.pop(key, None)
                    self._ast_cache.pop(key, None)
                    self._flow_cache.pop(key, None)

    def analyze_batch(
        self, code_samples: list[tuple[str, str | None]], enable_cache: bool = True
    ) -> list[AnalysisResult]:
        """Analyze multiple code samples in parallel."""
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers * 2) as executor:
            futures = [
                executor.submit(self.analyze_parallel, code, filename, enable_cache)
                for code, filename in code_samples
            ]

            results = []
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    # Handle individual analysis failures gracefully
                    results.append(
                        AnalysisResult(
                            pattern_matches=[],
                            ast_violations=[],
                            data_flow_results={"error": str(e)},
                            analysis_time=0.0,
                            cache_hits=0,
                            cache_misses=1,
                        )
                    )

            return results

    def get_cache_statistics(self) -> dict[str, Any]:
        """Get cache performance statistics."""
        with self._cache_lock:
            total_requests = self.cache_hits + self.cache_misses
            hit_rate = (self.cache_hits / total_requests) if total_requests > 0 else 0.0

            return {
                "cache_hits": self.cache_hits,
                "cache_misses": self.cache_misses,
                "hit_rate": hit_rate,
                "cached_patterns": len(self._pattern_cache),
                "cached_ast_results": len(self._ast_cache),
                "cached_flow_results": len(self._flow_cache),
            }

    def clear_cache(self) -> None:
        """Clear all cached analysis results."""
        with self._cache_lock:
            self._pattern_cache.clear()
            self._ast_cache.clear()
            self._flow_cache.clear()
            self.cache_hits = 0
            self.cache_misses = 0

    def create_comprehensive_report(self, result: AnalysisResult) -> dict[str, Any]:
        """Create comprehensive security report from analysis result."""
        # Count threats by severity
        threat_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}

        for match in result.pattern_matches:
            severity = match.pattern.threat_level.value
            threat_counts[severity] = threat_counts.get(severity, 0) + 1

        for violation in result.ast_violations:
            severity = violation.severity.value
            threat_counts[severity] = threat_counts.get(severity, 0) + 1

        total_threats = len(result.pattern_matches) + len(result.ast_violations)

        flow_violations = len(result.data_flow_results.get("violations", []))
        total_threats += flow_violations

        return {
            "summary": {
                "total_threats": total_threats,
                "pattern_matches": len(result.pattern_matches),
                "ast_violations": len(result.ast_violations),
                "data_flow_violations": flow_violations,
                "analysis_time": result.analysis_time,
                "performance": {
                    "cache_hits": result.cache_hits,
                    "cache_misses": result.cache_misses,
                },
            },
            "threat_breakdown": threat_counts,
            "data_flow_summary": result.data_flow_results.get("summary", {}),
            "recommendations": self._generate_recommendations(result),
        }

    def _generate_recommendations(self, result: AnalysisResult) -> list[str]:
        """Generate security recommendations based on analysis results."""
        recommendations = set()

        # Pattern-based recommendations
        for match in result.pattern_matches:
            if match.pattern.mitigation:
                recommendations.add(match.pattern.mitigation)

        # AST-based recommendations
        for violation in result.ast_violations:
            if violation.recommendation:
                recommendations.add(violation.recommendation)

        # Data flow recommendations
        flow_violations = result.data_flow_results.get("violations", [])
        if flow_violations:
            recommendations.add("Implement input validation and sanitization for tainted data")
            recommendations.add("Use parameterized queries to prevent injection attacks")

        return list(recommendations)[:10]  # Limit to top 10 recommendations
