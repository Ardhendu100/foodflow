# Database Design

## User

id
name
email
password_hash
is_active
created_at
updated_at

---

## Role

id
name

Examples:

admin
customer
restaurant_owner
delivery_partner

---

## Permission

id
name

---

## UserRole

user_id
role_id

---

## RolePermission

role_id
permission_id

---

# Relationships

User
↔ UserRole
↔ Role
↔ RolePermission
↔ Permission
