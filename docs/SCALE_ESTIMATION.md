# Initial Scale Estimation

## Users

1000 users

## Restaurants

100 restaurants

## Delivery Partners

200 partners

## Daily Orders

500 orders/day

---

# Read Traffic

Restaurant listing

Menu browsing

Order tracking

High Read Traffic

---

# Write Traffic

Order placement

Delivery status updates

Moderate Write Traffic

---

# Initial Conclusions

Single PostgreSQL instance is enough.

No need for microservices initially.

No need for Kafka initially.

Monolith is sufficient.

Future additions:

Redis
RabbitMQ
WebSockets
Kafka
