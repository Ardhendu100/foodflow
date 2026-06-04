# System Design Notes

## Layered Architecture

### What?


→ Presentation Layer --- This layer talks to the outside world.(Requet->Return)
→ Service Layer  --- This is the brain of the application.
→ Repository layer ---- This layer talks to the database.
→ Database --- This is where data lives.

Controller receives → Service thinks → Repository fetches → Database stores.

src
|
├── controller
│    └── BookController
│
├── service
│    └── BookService
│
├── repository
│    └── BookRepository
│
├── entity
│    └── Book
│
└── dto

### Pros

* Easy to understand
* Easy to implement

### Cons

* Can become tightly coupled

### FoodFlow Usage

Used initially for understanding architecture.

---

## Clean Architecture

### What?

Clean Architecture puts business logic in independent classes (Use Cases) so that frameworks, databases, and external services can change without affecting the core business rules.

Presentation
→ Application
→ Domain
→ Infrastructure

app/

├── entities/
│   └── user.py
│
├── usecases/   This is the business logic.
│   └── register_user.py
│
├── repositories/   Just a contract. doesn't care how data are saved
│   ├── interface.py
│   └── postgres.py
│
├── api/
│   └── routes.py
│
└── main.py

### Pros

* Highly maintainable
* Testable
* Scalable

### Cons

* More complexity

### FoodFlow Usage

Primary architecture style.

---

## Monolith

### Pros

* Fast development
* Easy deployment

### Cons

* Harder to scale later

---

## Microservices

### Pros

* Independent scaling
* Better team ownership

### Cons

* Distributed system complexity

---

## Event Driven Architecture

Producer
→ Queue
→ Consumer

Example:

Order Created
→ Notification Service
→ Analytics Service
→ Delivery Service


DDD (Domain-Driven Design) is an approach where software is designed around the business domain and business language. Instead of focusing first on databases or frameworks, it focuses on modeling real business concepts such as Orders, Payments, Customers, and their rules.
