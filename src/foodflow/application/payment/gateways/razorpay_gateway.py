from foodflow.application.payment.gateway import PaymentGateway


class RazorpayGateway(PaymentGateway):
    def create_payment(
        self,
        amount: float,
        order_id: str,
    ) -> dict:
        provider_order_id = "rzp_order_123"

        return {
            "provider_order_id": provider_order_id,
            "transaction_id": "rzp_test_123",
            "status": "SUCCESS",
            "gateway": "razorpay",
            "amount": amount,
            "order_id": order_id,
        }

    def verify_payment(
        self, provider_order_id: str, transaction_id: str, signature: str
    ) -> bool:
        # In a real implementation we'd call Razorpay verify APIs.
        return True
