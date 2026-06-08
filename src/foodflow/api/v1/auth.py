from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from foodflow.application.auth.schemas import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    UserResponse,
)
from foodflow.application.auth.service import AuthService
from foodflow.infrastructure.database.session import get_db
from foodflow.infrastructure.repositories.auth_repository import (
    AuthRepository,
)
from foodflow.application.auth.dependencies import (
    get_current_user,
)
from foodflow.domain.models.user import User


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    repository = AuthRepository(db)

    service = AuthService(repository)

    try:
        user = service.register_user(request)

        return {
            "message": "User registered successfully",
            "user_id": str(user.id),
            "email": user.email,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    repository = AuthRepository(db)

    service = AuthService(repository)

    try:
        return service.login_user(request)

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
        )


@router.post(
    "/refresh",
    response_model=TokenResponse,
)
def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    repository = AuthRepository(db)

    service = AuthService(repository)

    try:
        return service.refresh_access_token(request.refresh_token)

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
        )


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    """
    Get the currently authenticated user's profile.
    """
    return current_user
