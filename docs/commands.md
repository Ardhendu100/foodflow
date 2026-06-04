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
