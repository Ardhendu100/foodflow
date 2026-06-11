from uuid import UUID

from foodflow.application.payment.factory import (
    PaymentGatewayFactory,
)

from foodflow.domain.models.payment import Payment

from foodflow.infrastructure.repositories.order_repository import (
    OrderRepository,
)

from foodflow.infrastructure.repositories.payment_repository import (
    PaymentRepository,
)


class PaymentService:
    def __init__(
        self,
        payment_repository: PaymentRepository,
        order_repository: OrderRepository,
    ):
        self.payment_repository = payment_repository
        self.order_repository = order_repository

    def initiate_payment(
        self,
        order_id: UUID,
        gateway_name: str,
        payment_method: str,
    ):
        """
        Create payment and call payment gateway
        """

        order = self.order_repository.get_order_by_id(
            order_id,
        )

        if not order:
            raise ValueError("Order not found")

        existing_payment = self.payment_repository.get_payments_by_order_id(
            order_id,
        )

        if existing_payment:
            raise ValueError("Payment already exists for this order")

        gateway = PaymentGatewayFactory.get_gateway(gateway_name)

        gateway_response = gateway.create_payment(
            amount=float(order.total_amount),
            order_id=str(order.id),
        )

        payment = Payment(
            order_id=order.id,
            amount=order.total_amount,
            payment_method=payment_method,
            payment_provider=gateway_name,
            provider_order_id=gateway_response["provider_order_id"],
            status="PENDING",
        )

        return self.payment_repository.create_payment(
            payment,
        )

    def mark_payment_success(
        self,
        payment_id: UUID,
        transaction_id: str,
    ):
        payment = self.payment_repository.get_payment_by_id(
            payment_id,
        )

        if not payment:
            raise ValueError("Payment not found")

        payment.status = "SUCCESS"

        payment.transaction_id = transaction_id

        self.payment_repository.update_payment(
            payment,
        )

        order = payment.order

        order.status = "CONFIRMED"

        self.order_repository.update_order(
            order,
        )

        return payment

    def mark_payment_failed(
        self,
        payment_id: UUID,
    ):
        payment = self.payment_repository.get_payment_by_id(
            payment_id,
        )

        if not payment:
            raise ValueError("Payment not found")

        payment.status = "FAILED"

        return self.payment_repository.update_payment(
            payment,
        )

    def get_payment(
        self,
        payment_id: UUID,
    ):
        return self.payment_repository.get_payment_by_id(
            payment_id,
        )

    def verify_payment(
        self,
        payment_id: UUID,
        signature: str,
        transaction_id: str,
    ):
        """
        Verify payment using gateway
        """

        payment = self.payment_repository.get_payment_by_id(
            payment_id,
        )

        if not payment:
            raise ValueError("Payment not found")

        gateway = PaymentGatewayFactory.get_gateway(
            payment.payment_provider,
        )

        is_valid = gateway.verify_payment(
            provider_order_id=payment.provider_order_id,
            transaction_id=transaction_id,
            signature=signature,
        )

        if not is_valid:
            return self.mark_payment_failed(
                payment.id,
            )

        return self.mark_payment_success(
            payment.id,
            transaction_id,
        )
