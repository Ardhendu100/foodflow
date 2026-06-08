from pydantic import BaseModel, EmailStr, Field
from uuid import UUID


class RegisterRequest(BaseModel):
    full_name: str = Field(
        min_length=2,
        max_length=255,
    )

    email: EmailStr

    phone: str = Field(
        min_length=10,
        max_length=20,
    )

    password: str = Field(
        min_length=8,
        max_length=128,
    )


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class UserResponse(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    phone: str

    model_config = {
        "from_attributes": True,  # you are returning a SQLAlchemy model `User`, but FastAPI expects UserResponse, so this tells Pydantic to read values from model attributes.
    }
