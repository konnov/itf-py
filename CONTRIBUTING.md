# Contributing

## Development

This project uses a Makefile for common development tasks. Run `make help` to see all available commands:

```bash
make test          # Run tests
make test-cov      # Run tests with coverage
make format        # Format code with black and isort
make lint          # Run linting with flake8
make check         # Run all code quality checks
make ci            # Run full CI pipeline locally
make build         # Build the package
```

For a complete list of available commands, run:

```bash
make help
```

## GitHub Actions CI/CD

### CI Workflow (`.github/workflows/ci.yml`)

Runs on every push and pull request to `main` and `develop` branches.

**Jobs:**

1. **Test** - Runs on Python 3.11
   - Installs dependencies with Poetry
   - Runs pytest with coverage reporting
   - Uploads coverage to Codecov

2. **Lint** - Code quality checks
   - Black code formatting check
   - isort import sorting check
   - flake8 linting
   - mypy type checking

3. **Build** - Package building
   - Builds the package with Poetry
   - Uploads build artifacts

### Auto-format Workflow (`.github/workflows/format.yml`)

Runs on manual trigger or weekly schedule.

- Automatically formats code with Black
- Sorts imports with isort
- Commits changes back to the repository

## Local Development

Install development dependencies:

```bash
cd itf-py
poetry install
```

Run the same checks locally:

```bash
# Run tests with coverage
poetry run pytest --cov=src/itf_py --cov-report=term-missing

# Format code
poetry run black .
poetry run isort .

# Check formatting (without changing files)
poetry run black --check .
poetry run isort --check-only .

# Lint code
poetry run flake8 src tests

# Type check
poetry run mypy src
```

## Configuration

### pyproject.toml

All tool configurations are centralized in `pyproject.toml`:

- **black**: Line length 88, Python 3.11+ target
- **isort**: Black-compatible profile, line length 88
- **mypy**: Strict type checking enabled
- **pytest**: Test discovery and strict configuration
- **flake8**: Configured via `.flake8` file (88 char line length, ignores E203, W503, E712, E711)

### Dependencies

Development dependencies include:
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `black` - Code formatting
- `isort` - Import sorting
- `flake8` - Linting
- `mypy` - Type checking
