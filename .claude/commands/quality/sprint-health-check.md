# Sprint Quality Health Check

Analyze code quality metrics across the current sprint with focus on mlpy v2.0 quality gates and performance targets.

Usage: `/quality:sprint-health-check`

## Quality Metrics for mlpy v2.0

### 1. Test Coverage Requirements
- **Core Compiler Components**: Minimum 95% coverage
- **Security Components**: 100% coverage for security-critical paths
- **Performance Components**: 90%+ coverage with benchmark validation
- **CLI Components**: 85%+ coverage with integration tests

### 2. Security Coverage Standards
- **Zero Vulnerabilities**: No security issues in security test suite
- **Exploit Prevention**: 100% dangerous operation blocking
- **Capability System**: Full capability boundary validation
- **Sandbox Security**: Complete process isolation verification

### 3. Performance Targets
- **Transpilation Speed**: <10ms for typical programs (<1000 lines)
- **Security Analysis**: <5% overhead of total transpilation time
- **Memory Usage**: <128MB peak memory during transpilation
- **Cache Effectiveness**: 90%+ cache hit rate for repeated operations

### 4. Code Quality Standards
- **Black + Ruff**: 100% compliance with formatting and linting
- **MyPy Strict**: Full type annotation coverage with strict checking
- **Documentation**: All public APIs documented with examples
- **Import Organization**: Clean import structure following PEP 8

## Health Check Process

### 1. Test Coverage Analysis
```bash
# Generate comprehensive coverage report
nox -s tests -- --cov-report=html --cov-report=term-missing

# Core component coverage verification
pytest tests/unit/ml/ --cov=src/mlpy/ml --cov-fail-under=95
pytest tests/unit/runtime/ --cov=src/mlpy/runtime --cov-fail-under=95
pytest tests/security/ --cov=src/mlpy --cov-fail-under=100

# Coverage report analysis
open htmlcov/index.html  # Review detailed coverage
```

### 2. Security Audit Execution
```bash
# Comprehensive security analysis
nox -s security --verbose

# Security test suite
pytest tests/security/ -v --tb=short

# Static security analysis
bandit -r src/mlpy/ -f json -o security_report.json

# mlpy-specific security audit
mlpy audit examples/ --format json > mlpy_security_audit.json
```

### 3. Performance Benchmarking
```bash
# Run performance benchmark suite
nox -s benchmarks --verbose

# Transpilation speed benchmarks
pytest benchmarks/test_transpilation_speed.py --benchmark-save=current

# Memory usage analysis
python -m memory_profiler benchmarks/memory_benchmark.py

# Compare against baseline
pytest benchmarks/ --benchmark-compare=baseline
```

### 4. Code Quality Validation
```bash
# Code formatting verification
nox -s format --check

# Linting analysis
nox -s lint --verbose

# Type checking validation
nox -s type-check --verbose

# Import organization check
isort --check-only --diff src/ tests/
```

## mlpy-Specific Quality Checks

### 1. ML Grammar Validation
```bash
# Lark grammar syntax verification
python -c "from lark import Lark; Lark(open('src/mlpy/ml/grammar/ml.lark').read())"

# Grammar completeness test
python tests/grammar/test_grammar_completeness.py

# Parse tree validation
mlpy parse examples/comprehensive.ml --format json
```

### 2. Security Analysis Coverage
```bash
# Dangerous operation detection coverage
pytest tests/security/test_dangerous_operations.py -v

# Capability system validation
pytest tests/security/test_capability_system.py -v

# Security boundary testing
pytest tests/security/test_security_boundaries.py -v
```

### 3. Source Map Accuracy
```bash
# Source map generation testing
pytest tests/integration/test_source_maps.py -v

# ML ↔ Python mapping validation
python scripts/validate_source_maps.py examples/

# Debug mapping accuracy
mlpy transpile examples/complex.ml --sourcemap --debug
```

### 4. CLI Integration Testing
```bash
# CLI command testing
pytest tests/cli/ -v

# CLI integration with core components
pytest tests/integration/test_cli_integration.py -v

# CLI performance testing
time mlpy transpile examples/large_program.ml
```

## Quality Dashboard Generation

### Health Check Report Format
```
📊 mlpy v2.0 Sprint Quality Health Check
═══════════════════════════════════════

🎯 Overall Quality Score: 94/100 (A)

📈 Test Coverage Analysis:
✅ Core Components:        96% (target: 95%) ✅
✅ Security Components:    100% (target: 100%) ✅
✅ Runtime Components:     94% (target: 90%) ✅
❌ CLI Components:         83% (target: 85%) ❌

🛡️ Security Analysis:
✅ Dangerous Operations:   100% blocked ✅
✅ Capability System:      All boundaries validated ✅
✅ Exploit Prevention:     47/47 tests passing ✅
✅ Security Boundaries:    No leakage detected ✅

🚀 Performance Metrics:
✅ Transpilation Speed:    2.3ms avg (target: <10ms) ✅
✅ Security Overhead:      1.8% (target: <5%) ✅
✅ Memory Usage:           89MB peak (target: <128MB) ✅
✅ Cache Hit Rate:         94% (target: >90%) ✅

🔧 Code Quality:
✅ Black Formatting:       100% compliant ✅
✅ Ruff Linting:          100% compliant ✅
✅ MyPy Type Checking:     98% coverage ✅
✅ Documentation:          92% API coverage ✅

⚠️ Issues Requiring Attention:
1. CLI test coverage below threshold (83% vs 85% target)
   - Missing tests: CLI error handling, profile reporting
   - Impact: Medium
   - ETA to fix: 2 hours

2. MyPy type coverage gap (98% vs 100% target)
   - Missing annotations: 3 functions in runtime/profiling
   - Impact: Low
   - ETA to fix: 30 minutes

🎯 Recommendations:
1. Add integration tests for CLI error scenarios
2. Complete type annotations in profiling module
3. Expand documentation examples for capability system
4. Consider adding performance regression testing to CI
```

### Trend Analysis
```
📈 Quality Trends (Last 5 Sprints):
════════════════════════════════════

Test Coverage:     89% → 91% → 93% → 95% → 96% ⬆️
Security Score:    95% → 98% → 99% → 100% → 100% ✅
Performance:       15ms → 12ms → 8ms → 5ms → 2.3ms ⬆️
Code Quality:      92% → 95% → 97% → 99% → 99% ⬆️

🏆 Sprint Achievements:
- Achieved target transpilation speed (<10ms)
- Maintained 100% security test coverage
- Improved overall quality score by 5 points
- Zero critical issues for 3 consecutive sprints
```

## Automated Quality Monitoring

### 1. Continuous Quality Validation
```yaml
# .github/workflows/quality-check.yml
name: Quality Health Check
on: [push, pull_request]

jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python 3.12
        uses: actions/setup-python@v4
        with:
          python-version: "3.12"

      - name: Run Quality Health Check
        run: |
          pip install -e .[dev]
          nox -s tests -- --cov-fail-under=95
          nox -s security
          nox -s lint
          nox -s type-check
```

### 2. Quality Gate Enforcement
```python
# scripts/quality_gate.py
def enforce_quality_gates():
    """Enforce quality gates for sprint completion."""
    results = run_quality_check()

    # Critical gates that block sprint completion
    assert results.test_coverage >= 95, "Test coverage below minimum"
    assert results.security_score == 100, "Security issues detected"
    assert results.performance_regression == 0, "Performance regression detected"
    assert results.code_quality_score >= 95, "Code quality below threshold"

    print("✅ All quality gates passed - Sprint ready for completion")
```

### 3. Quality Metrics Collection
```python
# Store quality metrics for trend analysis
quality_metrics = {
    "timestamp": datetime.now(),
    "sprint": "Sprint 3",
    "test_coverage": 96.2,
    "security_score": 100.0,
    "performance_score": 98.7,
    "code_quality_score": 99.1,
    "issues_count": 2,
    "critical_issues": 0
}

# Save to metrics database
save_quality_metrics(quality_metrics)
```

## Quality Improvement Recommendations

### Short-term Actions (This Sprint)
1. **CLI Test Coverage**: Add missing integration tests
2. **Type Annotations**: Complete mypy coverage to 100%
3. **Documentation**: Add examples for remaining APIs
4. **Performance**: Add regression testing to CI pipeline

### Medium-term Actions (Next Sprint)
1. **Security Hardening**: Expand exploit prevention test suite
2. **Performance Optimization**: Profile and optimize hot paths
3. **Documentation**: Complete user guides and tutorials
4. **Testing**: Add end-to-end testing scenarios

### Long-term Actions (Future Sprints)
1. **Quality Automation**: Implement automatic quality gate enforcement
2. **Metrics Dashboard**: Create real-time quality monitoring
3. **Benchmarking**: Establish industry benchmark comparisons
4. **Security Auditing**: Schedule regular external security audits

**Focus: Maintaining high quality standards while ensuring continuous improvement and sprint velocity.**