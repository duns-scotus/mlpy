"""Nox configuration for mlpy development tasks."""

import nox

# Supported Python versions
PYTHON_VERSIONS = ["3.12"]
DEFAULT_PYTHON = "3.12"

# Session configuration
nox.options.sessions = ["lint", "mypy", "tests", "docs"]
nox.options.reuse_existing_virtualenvs = True


@nox.session(python=DEFAULT_PYTHON)
def lint(session):
    """Run code linting with ruff and black."""
    session.install("ruff", "black")

    session.log("🔍 Running ruff linter...")
    session.run("ruff", "check", "src", "tests")

    session.log("🎨 Running black formatter...")
    session.run("black", "--check", "--diff", "src", "tests")


@nox.session(python=DEFAULT_PYTHON)
def format(session):
    """Format code with black and ruff."""
    session.install("ruff", "black")

    session.log("🎨 Formatting with black...")
    session.run("black", "src", "tests")

    session.log("🔧 Fixing with ruff...")
    session.run("ruff", "check", "--fix", "src", "tests")


@nox.session(python=DEFAULT_PYTHON)
def mypy(session):
    """Run type checking with mypy."""
    session.install("-e", ".[dev]")

    session.log("🔍 Running mypy type checker...")
    session.run("mypy", "src/mlpy")


@nox.session(python=PYTHON_VERSIONS)
def tests(session):
    """Run the test suite."""
    session.install("-e", ".[dev]")

    session.log("🧪 Running test suite...")
    session.run(
        "pytest",
        "--cov=src/mlpy",
        "--cov-report=html",
        "--cov-report=term-missing",
        "--cov-fail-under=95",
        *session.posargs
    )


@nox.session(python=DEFAULT_PYTHON)
def tests_security(session):
    """Run security-focused tests."""
    session.install("-e", ".[dev]")

    session.log("🔒 Running security tests...")
    session.run("pytest", "tests/security/", "-v", "--tb=short")


@nox.session(python=DEFAULT_PYTHON)
def tests_performance(session):
    """Run performance benchmarks."""
    session.install("-e", ".[dev]")

    session.log("⚡ Running performance tests...")
    session.run("pytest", "tests/performance/", "-v", "--tb=short")


@nox.session(python=DEFAULT_PYTHON)
def docs(session):
    """Build documentation."""
    session.install("-e", ".[docs]")

    session.log("📚 Building documentation...")
    session.run("sphinx-build", "-b", "html", "docs/source", "docs/build/html")


@nox.session(python=DEFAULT_PYTHON)
def security(session):
    """Run security checks."""
    session.install("-e", ".[dev]")

    session.log("🔒 Running bandit security scanner...")
    session.run("bandit", "-r", "src/", "-f", "json", "-o", "bandit-report.json")
    session.run("bandit", "-r", "src/")

    session.log("🔒 Running safety dependency scanner...")
    session.run("safety", "check", "--json", "--output", "safety-report.json")
    session.run("safety", "check")


@nox.session(python=DEFAULT_PYTHON)
def clean(session):
    """Clean build artifacts and caches."""
    import shutil
    import glob
    import os

    session.log("🧹 Cleaning build artifacts...")

    # Directories to remove
    dirs_to_remove = [
        "build", "dist", "*.egg-info",
        ".pytest_cache", ".coverage", "htmlcov",
        ".mypy_cache", ".ruff_cache",
        "docs/build", ".nox"
    ]

    for pattern in dirs_to_remove:
        for path in glob.glob(pattern):
            if os.path.isdir(path):
                shutil.rmtree(path)
                session.log(f"Removed directory: {path}")
            elif os.path.isfile(path):
                os.remove(path)
                session.log(f"Removed file: {path}")


@nox.session(python=DEFAULT_PYTHON)
def setup_dev(session):
    """Set up development environment."""
    session.log("🛠️ Setting up development environment...")

    # Install development dependencies
    session.install("-e", ".[dev,lsp,dap,docs]")

    # Install pre-commit hooks
    session.run("pre-commit", "install")

    # Create necessary directories
    import os
    os.makedirs("benchmarks/results", exist_ok=True)
    os.makedirs("docs/build", exist_ok=True)
    os.makedirs(".mlpy_cache", exist_ok=True)

    session.log("✅ Development environment setup complete!")