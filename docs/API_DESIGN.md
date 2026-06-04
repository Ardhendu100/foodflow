# API Design

## Authentication

### Register

POST /api/v1/auth/register

Request:

{
"name": "John",
"email": "[john@example.com](mailto:john@example.com)",
"password": "secret"
}

Response:

{
"id": 1,
"email": "[john@example.com](mailto:john@example.com)"
}

---

### Login

POST /api/v1/auth/login

Request:

{
"email": "[john@example.com](mailto:john@example.com)",
"password": "secret"
}

Response:

{
"access_token": "...",
"refresh_token": "..."
}

---

### Logout

POST /api/v1/auth/logout

---

### Refresh Token

POST /api/v1/auth/refresh

---

## User APIs

GET /api/v1/users/me

PATCH /api/v1/users/me

---

## Health Check

GET /health
