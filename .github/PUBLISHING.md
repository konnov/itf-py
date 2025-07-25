# PyPI Publishing Setup Guide

This guide explains how to set up automated publishing to PyPI for the itf-py package.

## Prerequisites

### 1. PyPI Account Setup

1. Create accounts on both:
   - [PyPI](https://pypi.org/account/register/) (production)
   - [TestPyPI](https://test.pypi.org/account/register/) (testing)

2. Enable 2FA on both accounts (required for publishing)

### 2. GitHub Repository Setup

#### Option A: Trusted Publishing (Recommended - No API tokens needed)

1. Go to your PyPI account settings
2. Navigate to "Publishing" → "Add a new publisher"
3. Select "GitHub Actions"
4. Fill in:
   - **PyPI Project Name**: `itf-py`
   - **Owner**: `konnov` 
   - **Repository name**: `itf-py`
   - **Workflow name**: `publish.yml`
   - **Environment name**: `pypi`

5. Repeat the same setup for TestPyPI with environment name `testpypi`

#### Option B: API Tokens (Alternative)

If you prefer using API tokens instead of trusted publishing:

1. Generate API tokens:
   - PyPI: Account settings → API tokens → "Add API token"
   - TestPyPI: Account settings → API tokens → "Add API token"

2. Add secrets to your GitHub repository:
   - Go to repository Settings → Secrets and variables → Actions
   - Add secrets:
     - `PYPI_API_TOKEN`: Your PyPI API token
     - `TEST_PYPI_API_TOKEN`: Your TestPyPI API token

3. Update the publish workflow to use tokens instead of trusted publishing.

## How to Use

### 1. Testing (TestPyPI)

To test publishing without affecting the real PyPI:

```bash
# Manual trigger via GitHub UI
Go to Actions → Publish to PyPI → Run workflow
Select "testpypi" environment
```

### 2. Creating Releases

Two ways to create releases:

#### Option A: Manual Release Workflow

```bash
# Go to Actions → Release → Run workflow
# Choose version bump: patch/minor/major
# Choose if it's a prerelease
```

This will:
1. Bump the version in `pyproject.toml`
2. Commit and push the change
3. Create a git tag
4. Create a GitHub release
5. Automatically trigger PyPI publishing

#### Option B: Manual Git Tags

```bash
# Bump version locally
cd itf-py
poetry version patch  # or minor/major

# Commit and push
git add pyproject.toml
git commit -m "🔖 Bump version to $(poetry version --short)"
git push

# Create and push tag
git tag "v$(poetry version --short)"
git push origin "v$(poetry version --short)"

# Create GitHub release manually
```

## Workflow Files

The repository includes two workflows:

### `.github/workflows/publish.yml`
- **Triggered by**: GitHub releases, manual workflow dispatch
- **Purpose**: Publishes package to PyPI/TestPyPI
- **Features**: 
  - Runs tests before publishing
  - Supports both trusted publishing and API tokens
  - Can publish to TestPyPI for testing

### `.github/workflows/release.yml`
- **Triggered by**: Manual workflow dispatch
- **Purpose**: Creates releases and bumps versions
- **Features**:
  - Automated version bumping
  - Changelog generation
  - GitHub release creation

## Security

- ✅ Uses trusted publishing (no API tokens stored in repo)
- ✅ Runs tests before publishing
- ✅ Requires manual approval for releases
- ✅ Supports environment protection rules

## Troubleshooting

### Common Issues

1. **"Project does not exist"**: Make sure you've created the project on PyPI first
2. **"Invalid credentials"**: Check trusted publishing setup or API token
3. **"File already exists"**: Version already published, bump version number
4. **"Insufficient permissions"**: Check repository secrets and permissions

### Testing the Setup

1. First, test with TestPyPI:
   ```bash
   # Run publish workflow with testpypi environment
   ```

2. Install from TestPyPI to verify:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ itf-py
   ```

3. If successful, proceed with real PyPI release

## Package Installation

After publishing, users can install with:

```bash
pip install itf-py
```

## Version Management

The project uses semantic versioning (semver):
- **patch**: Bug fixes (0.1.0 → 0.1.1)
- **minor**: New features (0.1.0 → 0.2.0)  
- **major**: Breaking changes (0.1.0 → 1.0.0)
