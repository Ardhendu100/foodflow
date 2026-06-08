# FoodFlow Architecture Decisions

## Project Goal

FoodFlow is a backend-focused food delivery platform built for learning System Design, Distributed Systems, and Production Backend Engineering.

---

# Why FastAPI?

## Decision

FastAPI

## Reasons

* High performance
* Async support
* Excellent type hints
* Modern Python ecosystem
* Great developer experience

## Tradeoffs

Pros:

* Fast development
* Built-in validation

Cons:

* Smaller ecosystem than Django

---

# Why PostgreSQL?

## Decision

PostgreSQL

## Reasons

* ACID transactions
* Strong consistency
* Excellent relational modeling
* Production proven

## Tradeoffs

Pros:

* Reliable
* Supports complex queries

Cons:

* Horizontal scaling is harder

---

# Why Redis?

## Decision

Redis

## Reasons

* Extremely fast
* Caching support
* Rate limiting support

---

# Why RabbitMQ?

## Decision

RabbitMQ

## Reasons

* Message queues
* Async processing
* Background tasks

---

# Why Start as a Monolith?

## Decision

Monolith First

## Reasons

* Faster development
* Easier debugging
* Easier deployment
* Learn business domain first

Future:
Monolith → Modular Monolith → Microservices

---

# Why Clean Architecture?

## Decision

Clean Architecture

## Reasons

* Separation of concerns
* Better testability
* Scales with project growth
* Easier migration to microservices

---

# Initial Architecture

Client
→ FastAPI
→ Application Layer
→ Domain Layer
→ Infrastructure Layer
→ PostgreSQL

Future:

Redis
RabbitMQ
WebSockets
Microservices
Kafka

## Current Structure
foodflow
│
├── api
├── application
├── domain
├── infrastructure
└── shared

Layer responsibilities:

- domain = business entities/models
- application = business rules/services
- infrastructure = database/repositories/external systems
- api = FastAPI routes/controllers
- shared = configuration/common utilities

<!-- Domain
what does the business look like
A food delivery company will always have:

User
Restaurant
Order
Menu

Whether:

FastAPI
Django
Node.js
Java

The business concepts stay the same.

That's why they belong in:

domain

The core of the system.
 -->

 <!-- Application
application/auth

Question:

What business rules should happen?

Example:

register_user()

Rule:

Email must be unique
Password must be hashed

Notice:

The service does NOT know:

PostgreSQL
FastAPI
HTTP

It only knows:

Business Rules
-->

<!-- Infrastructure
infrastructure/

Question:

HOW do we store and retrieve data?

Example:

AuthRepository

The service says:

Save this user

Repository says:

Okay, I'll use PostgreSQL

Tomorrow:
Infrastructure
infrastructure/

Question:

HOW do we store and retrieve data?

Example:

AuthRepository

The service says:

Save this user

Repository says:

Okay, I'll use PostgreSQL

Tomorrow:

 -->

 <!-- API
api/

Question:

How do outside clients communicate with us?
Think:

API is the receptionist.

Customer:

I want to register

Receptionist:

Sure, let me tell the Auth Service.
 -->

 <!-- Shared
shared/

Question:

What is used everywhere?

Example:

settings.py

Every layer needs:

DATABASE_URL
SECRET_KEY

So it goes into shared.
 -->

 ## Now the Magic Flow

When user registers:

POST /auth/register

Step 1

API receives request.

RegisterRequest

Step 2

API calls service.

auth_service.register_user()

Step 3

Service executes business rules.

Check email
Hash password

Step 4

Service creates User model.

User(...)

Step 5

Service asks repository:

save_user()

Step 6

Repository talks to PostgreSQL.

INSERT INTO users ...

Step 7

Repository returns User.

Step 8

Service returns response.

Step 9

API returns JSON.

Visualized:

Client
  │
  ▼
API Layer
  │
  ▼
Service Layer
  │
  ▼
Repository Layer
  │
  ▼
Database
Why is it called Clean Architecture?

Because dependencies flow inward.

Outer layers depend on inner layers.

API
 ↓
Application
 ↓
Domain

Never:

Domain
 ↓
FastAPI

Your User model does NOT know:

FastAPI
HTTP
JWT

Good.

Because business concepts shouldn't depend on frameworks.

The Real Test

Suppose tomorrow I tell you:

Remove FastAPI.
Use Django.

What changes?

api/      ← changes

What remains?

domain/
application/

Mostly unchanged.

Suppose tomorrow:

PostgreSQL → MongoDB

What changes?

repository/
database/

What remains?

service.py
domain/

unchanged.

This is the feeling you should develop:

Domain

"What exists in my business?"

User
Role
Permission
Service

"What rules govern them?"

Register user
Login user
Repository

"How do I save them?"

PostgreSQL
API

"How does the outside world talk to me?"

REST endpoints

Once this clicks, you stop thinking:

I am writing FastAPI code.

and start thinking:

I am designing a system.

That's the transition from learning a framework to learning backend architecture.
