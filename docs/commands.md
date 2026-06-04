# FoodFlow Bootstrap Commands

## Install UV

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
uv --version
```

---

## Create Virtual Environment

```bash
uv venv
source .venv/bin/activate
```

---

## Initialize Python Project

```bash
uv init --package
```

---

## Install Development Dependencies

```bash
uv add --dev ruff
uv add --dev pytest
uv add --dev pre-commit
```

---

## Install Pre-Commit Hooks

```bash
uv run pre-commit install
```

---

## Run Pre-Commit Checks

```bash
uv run pre-commit run --all-files
```

---

## Create Project Directories

```bash
mkdir -p tests
mkdir -p scripts
mkdir -p migrations
mkdir -p docs/learning
```

---

## Create Clean Architecture Structure

```bash
mkdir -p src/foodflow/api
mkdir -p src/foodflow/application
mkdir -p src/foodflow/domain
mkdir -p src/foodflow/infrastructure
mkdir -p src/foodflow/shared
```

---

## Create Application Entry Point

```bash
touch src/foodflow/main.py
```

---

## Install FastAPI Foundation

```bash
uv add fastapi
uv add uvicorn
uv add pydantic
uv add pydantic-settings
```

or

```bash
uv add fastapi uvicorn pydantic pydantic-settings
```

---

## Useful UV Commands

### Install Package

```bash
uv add <package>
```

### Install Dev Package

```bash
uv add --dev <package>
```

### Remove Package

```bash
uv remove <package>
```

### Run Command

```bash
uv run <command>
```

### Sync Environment

```bash
uv sync
```

### Show Installed Packages

```bash
uv pip list
```

### Show Dependency Tree

```bash
uv tree
```

### Update Dependencies

```bash
uv lock --upgrade
uv sync
```
---

## Verify Project Structure

```bash
tree -L 3
```
## PostgreSQL command

```bash
sudo -u postgres psql
```

```bash
CREATE DATABASE foodflow;
```

```bash
CREATE USER foodflow_user WITH PASSWORD 'foodflow_password';
```

```bash
GRANT ALL PRIVILEGES ON DATABASE foodflow TO foodflow_user;
```

```bash
psql -h localhost -U foodflow_user -d foodflow
```

## Install Database Dependencies

```bash
uv add sqlalchemy alembic "psycopg[binary]"
```
<!-- Why these above
SQLAlchemy-> Python ↔ Database ORM
Alembic -> Database Schema Version Control
psycopg -> psycopg
-->

# Alembic Commands Cheat Sheet

## Initialize Alembic

Create Alembic configuration and migration directory:

```bash
uv run alembic init migrations
```

Creates:

```text
alembic.ini
migrations/
├── env.py
├── versions/
├── script.py.mako
└── README
```

---

## Generate Migration

Generate migration from SQLAlchemy models:

```bash
uv run alembic revision --autogenerate -m "create auth tables"
```

Example:

```bash
uv run alembic revision --autogenerate -m "create auth tables"
```

Creates:

```text
migrations/versions/<revision_id>_create_auth_tables.py
```

---

## Apply Latest Migration

Apply all pending migrations:

```bash
uv run alembic upgrade head
```

---

## Check Current Migration Version

```bash
uv run alembic current
```

---

## Show Migration History

```bash
uv run alembic history
```

---

## Downgrade One Migration

```bash
uv run alembic downgrade -1
```

---

## Downgrade to Specific Revision

```bash
uv run alembic downgrade <revision_id>
```

Example:

```bash
uv run alembic downgrade d01edbe53a22
```

---

## Upgrade to Specific Revision

```bash
uv run alembic upgrade <revision_id>
```

Example:

```bash
uv run alembic upgrade d01edbe53a22
```

---

## View Generated Migration Files

```bash
ls migrations/versions
```

---

## Remove Migration File (Development Only)

```bash
rm migrations/versions/*.py
```

Use only before migrations are applied to a shared environment.

---

## Verify Tables in PostgreSQL

Open PostgreSQL:

```bash
psql -U <username> -d <database_name>
```
---

## Typical Development Workflow

```bash
# 1. Modify SQLAlchemy models

# 2. Generate migration
uv run alembic revision --autogenerate -m "describe change"

# 3. Review migration file

# 4. Apply migration
uv run alembic upgrade head

# 5. Verify tables/schema
```

---

## Learning Summary

SQLAlchemy Models
↓
Base.metadata
↓
Alembic Autogenerate
↓
Migration File
↓
Alembic Upgrade
↓
PostgreSQL Tables
