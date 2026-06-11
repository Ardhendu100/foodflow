from foodflow.application.payment.gateways.fake_gateway import FakeGateway
from foodflow.application.payment.gateways.razorpay_gateway import RazorpayGateway
from foodflow.application.payment.gateways.stripe_gateway import StripeGateway


# Factory centralizes gateway creation.
class PaymentGatewayFactory:
    @staticmethod
    def get_gateway(
        gateway_name: str,
    ):

        gateway_name = gateway_name.lower()

        if gateway_name == "fake":
            return FakeGateway()

        if gateway_name == "razorpay":
            return RazorpayGateway()

        if gateway_name == "stripe":
            return StripeGateway()

        raise ValueError(f"Unsupported gateway: {gateway_name}")
