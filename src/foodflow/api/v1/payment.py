from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from foodflow.application.payment.schemas import (
    CreatePaymentRequest,
    PaymentSuccessRequest,
)

from foodflow.application.payment.service import (
    PaymentService,
)

from foodflow.infrastructure.database.session import (
    get_db,
)

from foodflow.infrastructure.repositories.order_repository import (
    OrderRepository,
)

from foodflow.infrastructure.repositories.payment_repository import (
    PaymentRepository,
)

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


def get_payment_service(
    db: Session = Depends(get_db),
):
    payment_repository = PaymentRepository(db)

    order_repository = OrderRepository(db)

    return PaymentService(
        payment_repository=payment_repository,
        order_repository=order_repository,
    )


@router.post("")
def create_payment(
    request: CreatePaymentRequest,
    service: PaymentService = Depends(
        get_payment_service,
    ),
):
    return service.initiate_payment(
        order_id=request.order_id,
        gateway_name=request.gateway,
        payment_method=request.payment_method,
    )


@router.post("/{payment_id}/success")
def payment_success(
    payment_id: str,
    request: PaymentSuccessRequest,
    service: PaymentService = Depends(
        get_payment_service,
    ),
):
    return service.verify_payment(
        payment_id=payment_id,
        transaction_id=request.transaction_id,
        signature=request.signature,
    )


@router.post("/{payment_id}/failed")
def payment_failed(
    payment_id: str,
    service: PaymentService = Depends(
        get_payment_service,
    ),
):
    return service.mark_payment_failed(
        payment_id=payment_id,
    )


@router.get("/{payment_id}")
def get_payment(
    payment_id: str,
    service: PaymentService = Depends(
        get_payment_service,
    ),
):
    return service.get_payment(
        payment_id,
    )
