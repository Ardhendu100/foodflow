from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID


class CreateRestaurantRequest(BaseModel):
    owner_id: UUID
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    phone: str = Field(min_length=5, max_length=20)
    email: EmailStr


class RestaurantResponse(BaseModel):
    id: UUID
    owner_id: UUID
    name: str
    description: Optional[str]
    phone: str
    email: EmailStr
    is_active: bool
    is_verified: bool

    class Config:
        from_attributes = True


class PaginatedRestaurantsResponse(BaseModel):
    items: list[RestaurantResponse]
    total: int
    page: int
    per_page: int

    class Config:
        from_attributes = True
