from uuid import uuid4

from foodflow.application.payment.gateway import PaymentGateway


class FakeGateway(PaymentGateway):
    def create_payment(
        self,
        amount: float,
        order_id: str,
    ) -> dict:
        provider_order_id = str(uuid4())

        return {
            "provider_order_id": provider_order_id,
            "transaction_id": str(uuid4()),
            "status": "SUCCESS",
            "gateway": "fake",
            "amount": amount,
            "order_id": order_id,
        }

    def verify_payment(
        self, provider_order_id: str, transaction_id: str, signature: str
    ) -> bool:
        # Fake gateway always verifies successfully in this test implementation
        return True
