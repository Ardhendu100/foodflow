from foodflow.application.auth.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)


password = "Secret@123"

hashed = hash_password(password)

print("Original Password:", password)
print("Hashed Password:", hashed)

is_valid = verify_password(
    password,
    hashed,
)

print("Password Valid:", is_valid)

# Test JWT

payload = {
    "sub": "123",
    "email": "bapi@example.com",
}

access_token = create_access_token(payload)
refresh_token = create_refresh_token(payload)

print("Access Token:", access_token)
print("Refresh Token:", refresh_token)
