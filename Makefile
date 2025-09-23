# Makefile for mlpy v2.0 Development
.PHONY: help install dev-install lint format test test-security test-performance docs docs-live clean setup-dev build

# Default target
help: ## Show this help message
	@echo "mlpy v2.0 Development Commands"
	@echo "==============================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Installation
install: ## Install production dependencies
	pip install -e .

dev-install: ## Install development dependencies
	pip install -e .[dev,lsp,dap,docs]
	pre-commit install

# Development
setup-dev: dev-install ## Set up complete development environment
	nox -s setup_dev

# Code quality
lint: ## Run code linting
	nox -s lint

format: ## Format code
	nox -s format

mypy: ## Run type checking
	nox -s mypy

# Testing
test: ## Run all tests
	nox -s tests

test-unit: ## Run unit tests only
	nox -s tests -- tests/unit/

test-integration: ## Run integration tests only
	nox -s tests -- tests/integration/

test-security: ## Run security tests
	nox -s tests_security

test-performance: ## Run performance tests
	nox -s tests_performance

test-coverage: ## Run tests with detailed coverage report
	nox -s tests -- --cov-report=html --cov-report=term

# Security
security: ## Run security checks
	nox -s security

# Documentation
docs: ## Build documentation
	nox -s docs

# Build and distribution
build: ## Build distribution packages
	python -m build

clean: ## Clean build artifacts and caches
	nox -s clean

# Utilities
validate-env: ## Validate development environment
	python --version
	pip list | grep -E "(pytest|black|ruff|mypy|nox)"

check-deps: ## Check for dependency updates
	pip list --outdated

# CI/CD simulation
ci-test: ## Run full CI test suite locally
	nox -s lint mypy tests security

# Release preparation
pre-release: clean lint mypy test security docs build ## Prepare for release
	@echo "✅ Pre-release checks passed!"