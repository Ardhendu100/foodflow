# UV Package Manager Notes

## What is UV?

UV is a modern Python package manager and project manager developed by Astral.

It is written in Rust and is designed to replace multiple traditional Python tools such as:

* pip
* venv
* virtualenv
* pip-tools
* poetry (partially)

UV provides:

* Virtual environment management
* Dependency management
* Package installation
* Lock file generation
* Project management

---

# Why Do We Need UV?

Traditional Python development typically looks like:

```bash
python -m venv .venv

source .venv/bin/activate

pip install fastapi

pip install sqlalchemy

pip freeze > requirements.txt
```

Problems:

* Slow dependency installation
* Multiple tools required
* Dependency conflicts can be difficult to resolve
* requirements.txt is not always reproducible
* Environment setup varies across teams

UV solves these issues with a single modern tool.

---

# Why UV Instead of pip?

## Traditional Approach

Tools required:

* pip
* venv
* requirements.txt

Example:

```bash
python -m venv .venv

source .venv/bin/activate

pip install fastapi

pip freeze > requirements.txt
```

---

## UV Approach

Example:

```bash
uv venv

uv add fastapi
```

Benefits:

* Faster
* Simpler
* Reproducible
* Modern dependency management

---

# Key Benefits of UV

## 1. Extremely Fast

UV is written in Rust.

Package installation and dependency resolution are significantly faster than pip.

---

## 2. Dependency Locking

UV generates:

```text
uv.lock
```

This ensures every developer uses the same dependency versions.

---

## 3. Single Tool

UV handles:

* Virtual environments
* Package installation
* Dependency resolution
* Project execution

---

## 4. Production Friendly

Modern backend teams increasingly prefer:

* UV
* Poetry
* PDM

over raw pip workflows.

---

# Common UV Commands

## Create Virtual Environment

```bash
uv venv
```

Creates:

```text
.venv/
```

Purpose:

Creates an isolated Python environment for the project.

---

## Install Package

```bash
uv add fastapi
```

Purpose:

Adds package to project dependencies and updates pyproject.toml.

---

## Install Development Dependency

```bash
uv add --dev pytest
```

Purpose:

Installs package only for development.

Examples:

* pytest
* ruff
* pre-commit

These are not required in production.

---

## Remove Package

```bash
uv remove fastapi
```

Purpose:

Removes dependency from project.

---

## Run Command Inside Environment

```bash
uv run python app.py
```

Purpose:

Executes command using project environment.

---

## Synchronize Environment

```bash
uv sync
```

Purpose:

Installs dependencies from pyproject.toml and uv.lock.

Useful when cloning a project.

---

# Understanding Development Dependencies

Development dependencies are tools used during development but not required by the running application.

Example:

```bash
uv add --dev ruff
uv add --dev pytest
uv add --dev pre-commit
```

---

# Ruff

Installation:

```bash
uv add --dev ruff
```

Purpose:

Fast Python linter and formatter.

Responsibilities:

* Detect code issues
* Enforce coding standards
* Format code

Examples:

* Unused imports
* Style violations
* Syntax improvements

Benefits:

* Extremely fast
* Replaces many linting tools
* Industry standard

---

# Pytest

Installation:

```bash
uv add --dev pytest
```

Purpose:

Testing framework.

Responsibilities:

* Unit tests
* Integration tests
* Regression tests

Example:

```python
def test_add():
    assert 1 + 1 == 2
```

Benefits:

* Simple syntax
* Powerful fixtures
* Industry standard

---

# Pre-Commit

Installation:

```bash
uv add --dev pre-commit
```

Purpose:

Runs automated checks before every Git commit.

Example workflow:

```bash
git commit -m "feature"
```

Before commit succeeds:

* Run Ruff
* Validate YAML
* Remove trailing spaces
* Check formatting

If checks fail:

```text
Commit Blocked
```

Benefits:

* Prevents bad code from entering repository
* Enforces team standards
* Improves code quality

---

# Development Workflow in FoodFlow

Create environment:

```bash
uv venv
```

Install dependencies:

```bash
uv add fastapi
uv add sqlalchemy
```

Install development tools:

```bash
uv add --dev ruff
uv add --dev pytest
uv add --dev pre-commit
```

Run application:

```bash
uv run python app.py
```

Run tests:

```bash
uv run pytest
```

Run linting:

```bash
uv run ruff check .
```

---

# Key Takeaways

* UV is a modern replacement for pip + venv workflows.
* UV is significantly faster than traditional tooling.
* UV simplifies dependency management.
* UV provides reproducible environments through lock files.
* Ruff is used for linting and formatting.
* Pytest is used for testing.
* Pre-commit enforces quality checks before commits.
* These tools are part of a production-grade Python development workflow.
