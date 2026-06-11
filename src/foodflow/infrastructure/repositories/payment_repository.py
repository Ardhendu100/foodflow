from uuid import UUID

from sqlalchemy.orm import Session

from foodflow.domain.models.payment import Payment


class PaymentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_payment(
        self,
        payment: Payment,
    ) -> Payment:
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)

        return payment

    def get_payment_by_id(
        self,
        payment_id: UUID,
    ) -> Payment | None:
        return self.db.query(Payment).filter(Payment.id == payment_id).first()

    def get_payments_by_order_id(
        self,
        order_id: UUID,
    ) -> list[Payment]:
        return self.db.query(Payment).filter(Payment.order_id == order_id).all()

    def update_payment(
        self,
        payment: Payment,
    ) -> Payment:
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)

        return payment
