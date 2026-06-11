from abc import ABC, abstractmethod


class PaymentGateway(ABC):
    @abstractmethod
    def create_payment(
        self,
        amount: float,
        order_id: str,
    ) -> dict:
        pass

    @abstractmethod
    def verify_payment(
        self, provider_order_id: str, transaction_id: str, signature: str
    ) -> bool:
        pass
