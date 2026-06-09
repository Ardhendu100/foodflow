from fastapi.security import OAuth2PasswordBearer
from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from foodflow.application.auth.security import decode_token
from foodflow.infrastructure.database.session import get_db
from foodflow.infrastructure.repositories.auth_repository import AuthRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# without it, Authorization Header must be "Bearer <token>" instead of just "<token>" which is more common in mobile apps and other clients. with it, the header can be just "Authorization: <token>" and FastAPI will handle the "Bearer " prefix automatically. It is not Google Login, Facebook Login, or Apple Login specific. It is a general convention for how access tokens are sent in HTTP requests.


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """
    Validate access token and return authenticated user.
    """

    try:
        payload = decode_token(token)

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    repository = AuthRepository(db)

    user = repository.get_user_by_id(UUID(user_id))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user
