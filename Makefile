#!/usr/bin/env make

# Variables
PYTHON := python
POETRY := poetry
PROJECT_DIR := itf-py
SRC_DIR := src
TEST_DIR := tests
PACKAGE_NAME := itf_py

# Default target
.DEFAULT_GOAL := help

# Help target
.PHONY: help
help: ## Show this help message
	@echo "Available targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Installation
.PHONY: install
install: ## Install dependencies
	cd $(PROJECT_DIR) && $(POETRY) install

.PHONY: install-dev
install-dev: ## Install development dependencies
	cd $(PROJECT_DIR) && $(POETRY) install --with dev

# Testing
.PHONY: test
test: ## Run tests
	cd $(PROJECT_DIR) && $(POETRY) run pytest

.PHONY: test-verbose
test-verbose: ## Run tests with verbose output
	cd $(PROJECT_DIR) && $(POETRY) run pytest -v

.PHONY: test-cov
test-cov: ## Run tests with coverage
	cd $(PROJECT_DIR) && $(POETRY) run pytest --cov=$(SRC_DIR)/$(PACKAGE_NAME) --cov-report=term-missing

.PHONY: test-cov-html
test-cov-html: ## Run tests with HTML coverage report
	cd $(PROJECT_DIR) && $(POETRY) run pytest --cov=$(SRC_DIR)/$(PACKAGE_NAME) --cov-report=html
	@echo "Coverage report generated in $(PROJECT_DIR)/htmlcov/index.html"

.PHONY: test-cov-xml
test-cov-xml: ## Run tests with XML coverage report
	cd $(PROJECT_DIR) && $(POETRY) run pytest --cov=$(SRC_DIR)/$(PACKAGE_NAME) --cov-report=xml

# Code Quality
.PHONY: format
format: ## Format code with black and isort
	cd $(PROJECT_DIR) && $(POETRY) run black .
	cd $(PROJECT_DIR) && $(POETRY) run isort .

.PHONY: format-check
format-check: ## Check code formatting without changing files
	cd $(PROJECT_DIR) && $(POETRY) run black --check .
	cd $(PROJECT_DIR) && $(POETRY) run isort --check-only .

.PHONY: lint
lint: ## Run linting with flake8
	cd $(PROJECT_DIR) && $(POETRY) run flake8 $(SRC_DIR) $(TEST_DIR)

.PHONY: type-check
type-check: ## Run type checking with mypy
	cd $(PROJECT_DIR) && $(POETRY) run mypy $(SRC_DIR)

.PHONY: check
check: format-check lint type-check ## Run all code quality checks

.PHONY: fix
fix: format ## Fix code formatting issues

# Building
.PHONY: build
build: ## Build the package
	cd $(PROJECT_DIR) && $(POETRY) build

.PHONY: build-wheel
build-wheel: ## Build wheel distribution
	cd $(PROJECT_DIR) && $(POETRY) build -f wheel

.PHONY: build-sdist
build-sdist: ## Build source distribution
	cd $(PROJECT_DIR) && $(POETRY) build -f sdist

# Cleaning
.PHONY: clean
clean: ## Clean build artifacts and cache
	rm -rf $(PROJECT_DIR)/build/
	rm -rf $(PROJECT_DIR)/dist/
	rm -rf $(PROJECT_DIR)/*.egg-info/
	rm -rf $(PROJECT_DIR)/.pytest_cache/
	rm -rf $(PROJECT_DIR)/.coverage
	rm -rf $(PROJECT_DIR)/htmlcov/
	rm -rf $(PROJECT_DIR)/.mypy_cache/
	find $(PROJECT_DIR) -type d -name __pycache__ -delete
	find $(PROJECT_DIR) -type f -name "*.pyc" -delete

.PHONY: clean-all
clean-all: clean ## Clean everything including virtual environment
	cd $(PROJECT_DIR) && $(POETRY) env remove --all

# Development
.PHONY: dev
dev: install format test ## Set up development environment and run basic checks

.PHONY: ci
ci: check test-cov build ## Run full CI pipeline locally

.PHONY: pre-commit
pre-commit: format lint type-check test ## Run pre-commit checks

# Documentation
.PHONY: docs
docs: ## Generate documentation (placeholder)
	@echo "Documentation generation not yet implemented"

# Package management
.PHONY: lock
lock: ## Update poetry.lock
	cd $(PROJECT_DIR) && $(POETRY) lock

.PHONY: update
update: ## Update dependencies
	cd $(PROJECT_DIR) && $(POETRY) update

.PHONY: show
show: ## Show package information
	cd $(PROJECT_DIR) && $(POETRY) show

.PHONY: show-tree
show-tree: ## Show dependency tree
	cd $(PROJECT_DIR) && $(POETRY) show --tree

# Publishing (use with caution)
.PHONY: publish-test
publish-test: build ## Publish to test PyPI
	cd $(PROJECT_DIR) && $(POETRY) publish --repository testpypi

.PHONY: publish
publish: build ## Publish to PyPI
	cd $(PROJECT_DIR) && $(POETRY) publish

# Quick development commands
.PHONY: quick-test
quick-test: ## Quick test run (no coverage)
	cd $(PROJECT_DIR) && $(POETRY) run pytest -x

.PHONY: watch-test
watch-test: ## Run tests in watch mode (requires pytest-watch)
	cd $(PROJECT_DIR) && $(POETRY) run ptw

# Version management
.PHONY: version
version: ## Show current version
	cd $(PROJECT_DIR) && $(POETRY) version

.PHONY: version-patch
version-patch: ## Bump patch version
	cd $(PROJECT_DIR) && $(POETRY) version patch

.PHONY: version-minor
version-minor: ## Bump minor version
	cd $(PROJECT_DIR) && $(POETRY) version minor

.PHONY: version-major
version-major: ## Bump major version
	cd $(PROJECT_DIR) && $(POETRY) version major
