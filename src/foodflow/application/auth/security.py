# This file is responsible for handling security-related functions, such as password hashing and verification.

from passlib.context import CryptContext  #  passlib is used for Password hashing
from foodflow.shared.config.settings import (
    settings,
)  # Importing settings for configuration values
from datetime import (
    datetime,
    timedelta,
    timezone,
)  # For handling token expiration times
from jose import jwt, JWTError  # For creating and verifying JSON Web Tokens (JWTs)

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS

# Password hashing configuration
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    """
    Hash a plain text password before storing it in the database.
    """
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a plain password against its stored hash.
    """
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


def create_access_token(
    data: dict,
) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "type": "access"})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def create_refresh_token(
    data: dict,
) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update(
        {
            "exp": expire,
            "type": "refresh",
        }
    )

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def decode_token(
    token: str,
) -> dict:
    """
    Decode and validate a JWT token.
    """

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        return payload

    except JWTError:
        raise ValueError("Invalid or expired token")
