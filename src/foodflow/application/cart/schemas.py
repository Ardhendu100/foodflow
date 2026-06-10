from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class AddToCartRequest(BaseModel):
    menu_item_id: UUID
    quantity: int = Field(gt=0)


class CartItemResponse(BaseModel):
    id: UUID
    menu_item_id: UUID
    quantity: int
    unit_price: Decimal

    model_config = {"from_attributes": True}


class CartResponse(BaseModel):
    cart_id: UUID
    restaurant_id: UUID

    items: list[CartItemResponse]

    total_amount: Decimal
