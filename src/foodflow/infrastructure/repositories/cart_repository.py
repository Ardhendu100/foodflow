from uuid import UUID

from sqlalchemy.orm import Session

from foodflow.domain.models.cart import Cart
from foodflow.domain.models.cart_item import CartItem


class CartRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_cart(
        self,
        user_id: UUID,
    ) -> Cart | None:

        return self.db.query(Cart).filter(Cart.user_id == user_id).first()

    def get_cart_by_id(
        self,
        cart_id: UUID,
    ) -> Cart | None:
        return self.db.query(Cart).filter(Cart.id == cart_id).first()

    def delete_cart_item(
        self,
        item: CartItem,
    ):
        self.db.delete(item)
        self.db.commit()

    def create_cart(
        self,
        cart: Cart,
    ) -> Cart:

        self.db.add(cart)
        self.db.commit()
        self.db.refresh(cart)

        return cart

    def add_cart_item(
        self,
        item: CartItem,
    ) -> CartItem:

        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)

        return item

    def get_cart_item(
        self,
        cart_id: UUID,
        menu_item_id: UUID,
    ) -> CartItem | None:

        return (
            self.db.query(CartItem)
            .filter(
                CartItem.cart_id == cart_id,
                CartItem.menu_item_id == menu_item_id,
            )
            .first()
        )

    def update(self):
        self.db.commit()
