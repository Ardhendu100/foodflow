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
