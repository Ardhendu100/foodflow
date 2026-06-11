from pydantic import BaseModel
from typing import List
from uuid import UUID
from datetime import datetime
from decimal import Decimal


class OrderItemResponse(BaseModel):
    id: UUID
    menu_item_id: UUID
    item_name: str
    item_price: Decimal
    quantity: int
    created_at: datetime

    model_config = {"from_attributes": True}


class OrderResponse(BaseModel):
    id: UUID
    customer_id: UUID
    restaurant_id: UUID
    status: str
    total_amount: Decimal
    items: List[OrderItemResponse]
    created_at: datetime

    model_config = {"from_attributes": True}


class CreateOrderResponse(BaseModel):
    order: OrderResponse


class OrderListResponse(BaseModel):
    items: List[OrderResponse]
