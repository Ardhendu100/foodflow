from uuid import UUID

from sqlalchemy.orm import Session

from foodflow.domain.models.order import Order


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_order(self, order: Order) -> Order:
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)

        return order

    def get_order_by_id(self, order_id: UUID) -> Order | None:
        return self.db.query(Order).filter(Order.id == order_id).first()

    def list_orders_for_user(self, user_id: UUID) -> list[Order]:
        return (
            self.db.query(Order)
            .filter(Order.customer_id == user_id)
            .order_by(Order.created_at.desc())
            .all()
        )

    def list_orders_for_restaurant(self, restaurant_id: UUID) -> list[Order]:
        return (
            self.db.query(Order)
            .filter(Order.restaurant_id == restaurant_id)
            .order_by(Order.created_at.desc())
            .all()
        )

    def update_order(self, order: Order) -> Order:
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)

        return order
