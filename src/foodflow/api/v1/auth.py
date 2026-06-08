from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from foodflow.application.auth.schemas import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
)
from foodflow.application.auth.service import AuthService
from foodflow.infrastructure.database.session import get_db
from foodflow.infrastructure.repositories.auth_repository import (
    AuthRepository,
)

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
