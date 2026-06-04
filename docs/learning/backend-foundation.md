# Backend Foundation Technologies

## SQLAlchemy 2.0

### What is it?

SQLAlchemy is a Python ORM (Object Relational Mapper) and database toolkit.

It allows us to interact with databases using Python objects instead of writing raw SQL for every operation.

Example:

Without ORM:

```sql
SELECT * FROM users;
```

With SQLAlchemy:

```python
users = session.execute(select(User))
```

---

### Why do we need it?

Without an ORM:

* Large amount of SQL code
* Harder maintenance
* Database-specific queries
* Repetitive CRUD operations

SQLAlchemy provides:

* Object-oriented database access
* Relationship management
* Query building
* Database abstraction

---

### What problem does it solve?

Bridges the gap between:

```text
Python Objects
        ↕
Database Tables
```

---

### Key Concepts

* Engine
* Session
* Models
* Relationships
* Transactions
* Query Builder

---

### Production Usage

Used to:

* Create database models
* Query data
* Manage relationships
* Handle transactions

---

### One-Line Summary

SQLAlchemy is the layer that allows Python code to communicate with PostgreSQL efficiently and safely.

---

# Alembic

### What is it?

Alembic is the database migration tool for SQLAlchemy.

It tracks and applies database schema changes over time.

---

### Why do we need it?

Databases evolve.

Example:

Today:

```text
users
├── id
├── email
```

Tomorrow:

```text
users
├── id
├── email
├── phone_number
```

Production databases cannot be manually edited every time.

Alembic manages these changes.

---

### What problem does it solve?

Database version control.

Similar to Git, but for database schemas.

---

### Key Concepts

* Migration
* Upgrade
* Downgrade
* Revision
* Version History

---

### Production Usage

Used whenever:

* New tables are added
* Columns change
* Indexes are added
* Constraints change

---

### One-Line Summary

Alembic keeps database schema changes consistent across development, staging, and production environments.

---

# Pydantic v2

### What is it?

Pydantic is a data validation and serialization library.

FastAPI uses Pydantic to validate incoming requests and generate API schemas.

---

### Why do we need it?

Clients can send invalid data.

Example:

```json
{
  "email": 123,
  "password": null
}
```

Pydantic validates the request before business logic runs.

---

### What problem does it solve?

Ensures application receives clean, correctly typed, and validated data.

---

### Key Concepts

* BaseModel
* Validation
* Serialization
* Deserialization
* Field Constraints

---

### Production Usage

Used for:

* Request validation
* Response serialization
* API documentation
* Data transformation

---

### One-Line Summary

Pydantic acts as the gatekeeper that validates and structures data entering and leaving the application.

---

# How They Work Together

```text
Client Request
        ↓
Pydantic
(Validate Data)
        ↓
FastAPI Endpoint
        ↓
SQLAlchemy
(Database Operations)
        ↓
PostgreSQL
```

Schema changes over time:

```text
SQLAlchemy Models
        ↓
Alembic Migration
        ↓
PostgreSQL Schema Update
```

---

# Quick Memory Tricks

### SQLAlchemy

```text
Python ↔ Database
```

### Alembic

```text
Database Version Control
```

### Pydantic

```text
Data Validation Layer
```

---

# Final Takeaway

SQLAlchemy manages data.

Alembic manages database schema changes.

Pydantic validates data.

Together they form the foundation of a production-grade FastAPI backend.
