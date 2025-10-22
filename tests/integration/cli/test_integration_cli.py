"""Unit tests for Integration Toolkit CLI commands."""

import pytest
from pathlib import Path
from click.testing import CliRunner
from mlpy.integration.cli_commands import integration


class TestIntegrationValidateCommand:
    """Tests for 'mlpy integration validate' command."""

    def test_validate_success(self):
        """Test validate command with properly configured toolkit."""
        runner = CliRunner()
        result = runner.invoke(integration, ['validate'])

        # Should succeed with exit code 0
        assert result.exit_code == 0
        assert "[OK]" in result.output
        assert "Module Registry" in result.output
        assert "Async Executor" in result.output
        assert "Capability Manager" in result.output
        assert "Callback System" in result.output
        assert "properly configured" in result.output

    def test_validate_displays_module_counts(self):
        """Test that validate displays module counts."""
        runner = CliRunner()
        result = runner.invoke(integration, ['validate'])

        assert "modules" in result.output.lower()

    def test_validate_checks_all_components(self):
        """Test that validate checks all required components."""
        runner = CliRunner()
        result = runner.invoke(integration, ['validate'])

        # All four components should be listed
        components = ["Module Registry", "Async Executor", "Capability Manager", "Callback System"]
        for component in components:
            assert component in result.output


class TestIntegrationBenchmarkCommand:
    """Tests for 'mlpy integration benchmark' command."""

    @pytest.fixture
    def simple_ml_file(self, tmp_path):
        """Create a simple ML file for testing."""
        ml_file = tmp_path / "test.ml"
        ml_file.write_text("result = 2 + 2;", encoding='utf-8')
        return str(ml_file)

    @pytest.fixture
    def fibonacci_ml_file(self, tmp_path):
        """Create a fibonacci ML file for testing."""
        ml_file = tmp_path / "fibonacci.ml"
        ml_file.write_text("""
function fibonacci(n) {
    if (n <= 1) {
        return n;
    } else {
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
}

result = fibonacci(5);
""", encoding='utf-8')
        return str(ml_file)

    def test_benchmark_basic(self, simple_ml_file):
        """Test basic benchmark command."""
        runner = CliRunner()
        result = runner.invoke(integration, ['benchmark', simple_ml_file, '--iterations', '10', '--warmup', '0'])

        assert result.exit_code == 0
        assert "[OK]" in result.output
        assert "Mean Time" in result.output
        assert "Median Time" in result.output
        assert "Std Deviation" in result.output

    def test_benchmark_with_iterations(self, simple_ml_file):
        """Test benchmark with custom iteration count."""
        runner = CliRunner()
        result = runner.invoke(integration, ['benchmark', simple_ml_file, '--iterations', '25', '--warmup', '0'])

        assert result.exit_code == 0
        assert "Iterations" in result.output
        assert "25" in result.output

    def test_benchmark_concurrent(self, simple_ml_file):
        """Test concurrent benchmark mode."""
        runner = CliRunner()
        result = runner.invoke(integration, ['benchmark', simple_ml_file, '--concurrency', '5'])

        assert result.exit_code == 0
        assert "Concurrent Executions" in result.output
        assert "Throughput" in result.output
        assert "exec/sec" in result.output

    def test_benchmark_with_warmup(self, simple_ml_file):
        """Test benchmark with warmup iterations."""
        runner = CliRunner()
        result = runner.invoke(integration, ['benchmark', simple_ml_file, '--iterations', '20', '--warmup', '5'])

        assert result.exit_code == 0
        assert "warmup" in result.output.lower()

    def test_benchmark_nonexistent_file(self):
        """Test benchmark with non-existent file."""
        runner = CliRunner()
        result = runner.invoke(integration, ['benchmark', 'nonexistent.ml'])

        # Should fail with non-zero exit code
        assert result.exit_code != 0

    def test_benchmark_shows_statistics(self, fibonacci_ml_file):
        """Test that benchmark shows detailed statistics."""
        runner = CliRunner()
        result = runner.invoke(integration, ['benchmark', fibonacci_ml_file, '--iterations', '15', '--warmup', '0'])

        assert result.exit_code == 0
        assert "Mean Time" in result.output
        assert "Median Time" in result.output
        assert "Std Deviation" in result.output
        assert "Min Time" in result.output
        assert "Max Time" in result.output
        assert "ms" in result.output

    def test_benchmark_concurrent_throughput(self, simple_ml_file):
        """Test concurrent benchmark calculates throughput correctly."""
        runner = CliRunner()
        result = runner.invoke(integration, ['benchmark', simple_ml_file, '--concurrency', '10'])

        assert result.exit_code == 0
        assert "Throughput" in result.output
        # Should show throughput > 0
        assert "exec/sec" in result.output


class TestIntegrationCommandHelp:
    """Tests for integration command help text."""

    def test_integration_group_help(self):
        """Test integration group help text."""
        runner = CliRunner()
        result = runner.invoke(integration, ['--help'])

        assert result.exit_code == 0
        assert "Integration Toolkit commands" in result.output
        assert "validate" in result.output
        assert "benchmark" in result.output

    def test_validate_help(self):
        """Test validate command help text."""
        runner = CliRunner()
        result = runner.invoke(integration, ['validate', '--help'])

        assert result.exit_code == 0
        assert "Validate Integration Toolkit setup" in result.output

    def test_benchmark_help(self):
        """Test benchmark command help text."""
        runner = CliRunner()
        result = runner.invoke(integration, ['benchmark', '--help'])

        assert result.exit_code == 0
        assert "Benchmark ML file execution" in result.output
        assert "--iterations" in result.output
        assert "--concurrency" in result.output
        assert "--warmup" in result.output


class TestIntegrationCommandOptions:
    """Tests for command options and flags."""

    @pytest.fixture
    def simple_ml_file(self, tmp_path):
        """Create a simple ML file for testing."""
        ml_file = tmp_path / "test.ml"
        ml_file.write_text("result = 2 + 2;", encoding='utf-8')
        return str(ml_file)

    def test_benchmark_default_iterations(self, simple_ml_file):
        """Test benchmark with default iterations (100)."""
        runner = CliRunner()
        result = runner.invoke(integration, ['benchmark', simple_ml_file, '--warmup', '0'])

        # With warmup disabled, should show 100 iterations
        assert result.exit_code == 0

    def test_benchmark_custom_concurrency(self, simple_ml_file):
        """Test benchmark with various concurrency levels."""
        runner = CliRunner()

        # Test with concurrency=1 (sequential)
        result1 = runner.invoke(integration, ['benchmark', simple_ml_file, '--concurrency', '1'])
        assert result1.exit_code == 0

        # Test with concurrency=20
        result2 = runner.invoke(integration, ['benchmark', simple_ml_file, '--concurrency', '20'])
        assert result2.exit_code == 0
        assert "20" in result2.output


class TestIntegrationCommandErrorHandling:
    """Tests for error handling in integration commands."""

    def test_benchmark_invalid_ml_file(self, tmp_path):
        """Test benchmark with invalid ML syntax."""
        ml_file = tmp_path / "invalid.ml"
        ml_file.write_text("this is not valid ML syntax @#$%", encoding='utf-8')

        runner = CliRunner()
        result = runner.invoke(integration, ['benchmark', str(ml_file), '--iterations', '1', '--warmup', '0'])

        # Should handle error gracefully
        assert "Benchmark failed" in result.output or result.exit_code != 0

    def test_benchmark_missing_file_argument(self):
        """Test benchmark without required file argument."""
        runner = CliRunner()
        result = runner.invoke(integration, ['benchmark'])

        # Should show error about missing argument
        assert result.exit_code != 0
        assert "Missing argument" in result.output or "Usage:" in result.output
