from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CreatePaymentRequest(BaseModel):
    order_id: UUID
    gateway: str = "fake"
    payment_method: str = "UPI"


class PaymentResponse(BaseModel):
    id: UUID
    order_id: UUID

    amount: float

    status: str

    payment_method: str
    payment_provider: str

    transaction_id: str | None = None

    created_at: datetime

    class Config:
        from_attributes = True


class PaymentSuccessRequest(BaseModel):
    transaction_id: str
    signature: str
