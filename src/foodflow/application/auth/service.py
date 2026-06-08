from foodflow.application.auth.schemas import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
)
from foodflow.application.auth.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from foodflow.domain.models.user import User
from foodflow.infrastructure.repositories.auth_repository import (
    AuthRepository,
)
from uuid import UUID


class AuthService:
    def __init__(
        self,
        repository: AuthRepository,
    ):
        self.repository = repository

    def register_user(
        self,
        request: RegisterRequest,
    ) -> User:
        """
        Register a new user.
        """

        existing_user = self.repository.get_user_by_email(request.email)

        if existing_user:
            raise ValueError("User with this email already exists")

        hashed_password = hash_password(request.password)

        user = User(
            full_name=request.full_name,
            email=request.email,
            phone=request.phone,
            password_hash=hashed_password,
        )

        return self.repository.create_user(user)

    def login_user(
        self,
        request: LoginRequest,
    ) -> TokenResponse:
        """
        Authenticate a user and generate JWT tokens.
        """

        user = self.repository.get_user_by_email(request.email)

        if not user:
            raise ValueError("Invalid email or password")

        is_valid_password = verify_password(
            request.password,
            user.password_hash,
        )

        if not is_valid_password:
            raise ValueError("Invalid email or password")

        access_token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
            }
        )

        refresh_token = create_refresh_token(
            {
                "sub": str(user.id),
            }
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )

    def refresh_access_token(
        self,
        refresh_token: str,
    ) -> TokenResponse:
        """
        Generate new access and refresh tokens.
        """

        payload = decode_token(refresh_token)

        token_type = payload.get("type")

        if token_type != "refresh":
            raise ValueError("Invalid refresh token")

        user_id = payload.get("sub")

        if not user_id:
            raise ValueError("Invalid token payload")

        user = self.repository.get_user_by_id(UUID(user_id))

        if not user:
            raise ValueError("User not found")

        new_access_token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
            }
        )

        new_refresh_token = create_refresh_token(
            {
                "sub": str(user.id),
                "email": user.email,
            }
        )

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
        )
