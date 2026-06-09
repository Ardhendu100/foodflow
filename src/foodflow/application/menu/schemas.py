from pydantic import BaseModel, Field, AnyUrl
from typing import Optional
from uuid import UUID
from datetime import datetime
from decimal import Decimal


class PaginatedMenuItemsResponse(BaseModel):
    items: list["MenuItemResponse"]
    total: int
    page: int
    per_page: int

    model_config = {"from_attributes": True}


class CreateMenuItemRequest(BaseModel):
    restaurant_id: UUID
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    price: Decimal = Field(gt=0)
    image_url: Optional[AnyUrl] = None
    veg_type: Optional[str] = Field(default="veg", pattern="^(veg|non-veg)$")
    preparation_time_minutes: Optional[int] = Field(default=10, gt=0)


class UpdateMenuItemRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    price: Optional[Decimal] = Field(default=None, gt=0)
    image_url: Optional[AnyUrl] = None
    is_available: Optional[bool] = None
    veg_type: Optional[str] = Field(default=None, pattern="^(veg|non-veg)$")
    preparation_time_minutes: Optional[int] = Field(default=None, gt=0)


class MenuItemResponse(BaseModel):
    id: UUID
    restaurant_id: UUID
    name: str
    description: Optional[str]
    price: Decimal
    image_url: Optional[AnyUrl]
    is_available: bool
    veg_type: str
    preparation_time_minutes: int
    created_at: datetime

    model_config = {"from_attributes": True}
