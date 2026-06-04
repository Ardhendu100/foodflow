# SQLAlchemy 2.0

## What is SQLAlchemy?

SQLAlchemy is the most popular Python ORM (Object Relational Mapper) and database toolkit.

It allows developers to interact with databases using Python objects instead of writing raw SQL for every operation.

Example:

Without SQLAlchemy:

```sql
SELECT * FROM users WHERE email = 'john@example.com';
```

With SQLAlchemy:

```python
user = session.execute(
    select(User).where(User.email == "john@example.com")
)
```

SQLAlchemy generates the SQL query behind the scenes.

---

## Why do we need it?

As applications grow, writing raw SQL everywhere becomes difficult to manage.

Problems with raw SQL:

- Repetitive queries
- Harder maintenance
- Manual relationship handling
- More boilerplate code
- Database-specific syntax

SQLAlchemy solves these problems by:

- Mapping tables to Python classes
- Managing relationships automatically
- Handling transactions
- Generating SQL queries
- Improving code readability

---

# Core Concepts

## Engine

### What is it?

The Engine is SQLAlchemy's connection manager.

It knows:

- Which database to connect to
- How to connect
- How to manage connection pools

Example:

```python
engine = create_engine(DATABASE_URL)
```

Think of Engine as:

```text
Application
      ↓
    Engine
      ↓
 PostgreSQL
```

### Responsibility

- Database connection management
- Connection pooling
- SQL execution

---

## Session

### What is it?

A Session is a conversation with the database.

It tracks changes made to objects and manages transactions.

Example:

```python
session.add(user)
session.commit()
```

Without commit:

```text
Changes stay in memory only.
```

With commit:

```text
Changes are saved to database.
```

### Responsibility

- Persist data
- Update data
- Delete data
- Manage transactions

Think:

```text
Session = Database Conversation
```

---

## Model

### What is it?

A Model is a Python class that represents a database table.

Example:

```python
class User(Base):
    __tablename__ = "users"
```

Database:

```text
users table
```

Python:

```text
User class
```

### Responsibility

- Define table structure
- Define columns
- Define relationships

Think:

```text
Model = Table Blueprint
```

---

## Relationship

### What is it?

Relationships connect tables together.

Example:

```text
User
  ↓
Order
```

One user can have many orders.

```text
1 User → Many Orders
```

SQLAlchemy provides:

```python
relationship()
```

to manage these connections.

### Common Types

#### One-to-One

```text
User ↔ Profile
```

#### One-to-Many

```text
User → Orders
```

#### Many-to-Many

```text
Users ↔ Roles
```

---

## Transaction

### What is it?

A transaction ensures data consistency.

Example:

Order creation requires:

```text
Create Order
Update Inventory
Create Payment Record
```

All operations must succeed together.

If one fails:

```text
Rollback Everything
```

If all succeed:

```text
Commit Everything
```

### ACID Behavior

- Atomicity
- Consistency
- Isolation
- Durability

Think:

```text
Transaction = All Success or All Fail
```

---

# SQLAlchemy 2.0 Style

SQLAlchemy 2.0 introduced a cleaner and more explicit API.

Older style:

```python
session.query(User)
```

Modern style:

```python
session.execute(
    select(User)
)
```

Benefits:

- Better type hints
- Cleaner syntax
- Explicit query construction
- Improved async support
- Future-proof approach

All new projects should use SQLAlchemy 2.0 style.

---

# How it Fits in FastAPI

Typical request flow:

```text
Client Request
       ↓
FastAPI Endpoint
       ↓
Service Layer
       ↓
Repository Layer
       ↓
SQLAlchemy Session
       ↓
PostgreSQL
```

Example:

```text
POST /auth/register
        ↓
Auth Service
        ↓
User Repository
        ↓
SQLAlchemy
        ↓
PostgreSQL
```

SQLAlchemy acts as the bridge between FastAPI and the database.

---

# Where We Will Use SQLAlchemy in FoodFlow

### User Management

- User
- Role
- Permission

### Restaurant Management

- Restaurant
- Menu
- Category

### Order Management

- Cart
- Order
- Order Item

### Delivery Management

- Delivery Partner
- Delivery Assignment

---

# SQLAlchemy Workflow

```text
Define Models
       ↓
Generate Migration
       ↓
Apply Migration
       ↓
Create Session
       ↓
Perform CRUD Operations
       ↓
Commit Transaction
```

---

# One-Line Summary

SQLAlchemy is the ORM layer that translates Python objects into SQL queries and manages all database interactions in a clean, maintainable, and production-ready way.
