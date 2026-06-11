from decimal import Decimal
from uuid import UUID
from typing import Optional

from foodflow.application.order.schemas import (
    OrderResponse,
    OrderListResponse,
)
from foodflow.domain.models.order import Order
from foodflow.domain.models.order_item import OrderItem
from foodflow.infrastructure.repositories.order_repository import OrderRepository
from foodflow.infrastructure.repositories.cart_repository import CartRepository
from foodflow.infrastructure.repositories.menu_repository import MenuRepository
from foodflow.infrastructure.repositories.restaurant_repository import (
    RestaurantRepository,
)
from foodflow.domain.models.user import User


class OrderService:
    VALID_TRANSITIONS = {
        "PENDING": {"CONFIRMED", "REJECTED", "CANCELLED"},
        "CONFIRMED": {"PREPARING"},
        "PREPARING": {"READY_FOR_PICKUP"},
        "READY_FOR_PICKUP": {"OUT_FOR_DELIVERY"},
        "OUT_FOR_DELIVERY": {"DELIVERED"},
    }

    def __init__(
        self,
        order_repo: OrderRepository,
        cart_repo: CartRepository,
        menu_repo: MenuRepository,
        restaurant_repo: RestaurantRepository,
    ):
        self.order_repo = order_repo
        self.cart_repo = cart_repo
        self.menu_repo = menu_repo
        self.restaurant_repo = restaurant_repo

    def checkout(self, user: User) -> OrderResponse:
        # Find user's cart
        cart = self.cart_repo.get_user_cart(user.id)

        if not cart:
            raise ValueError("Cart not found")

        if not cart.items or len(cart.items) == 0:
            raise ValueError("Cart is empty")

        # Calculate total and build order items
        total = Decimal("0")

        order = Order(
            customer_id=user.id,
            restaurant_id=cart.restaurant_id,
            status="PENDING",
            total_amount=Decimal("0"),
        )

        # Persist order (so we get an id) and then add items
        # We'll create order items and append to order.items before saving

        for ci in cart.items:
            menu_item = self.menu_repo.get_menu_item_by_id(ci.menu_item_id)

            if not menu_item:
                raise ValueError(f"Menu item not found: {ci.menu_item_id}")

            if not menu_item.is_available:
                raise ValueError(f"Menu item not available: {menu_item.id}")

            line_total = ci.unit_price * ci.quantity
            total += line_total

            oi = OrderItem(
                menu_item_id=menu_item.id,
                item_name=menu_item.name,
                item_price=menu_item.price,
                quantity=ci.quantity,
            )

            order.items.append(oi)

        order.total_amount = total

        created = self.order_repo.create_order(order)

        # Clear cart items
        for ci in list(cart.items):
            self.cart_repo.delete_cart_item(ci)

        return OrderResponse.from_orm(created)

    def get_order(self, order_id: UUID, user: User) -> Optional[OrderResponse]:
        order = self.order_repo.get_order_by_id(order_id)

        if not order:
            return None

        # allow customer or restaurant owner or admin to view
        if str(order.customer_id) != str(user.id):
            # check if user is restaurant owner
            if str(order.restaurant.owner_id) != str(user.id):
                # admin
                for ur in user.user_roles:
                    if ur.role.name == "Admin":
                        return OrderResponse.from_orm(order)

                raise ValueError("Permission denied")

        return OrderResponse.from_orm(order)

    def list_orders_for_user(self, user: User) -> OrderListResponse:
        items = self.order_repo.list_orders_for_user(user.id)

        return OrderListResponse(items=[OrderResponse.from_orm(i) for i in items])

    def _transition(self, order: Order, new_status: str):
        current = order.status

        allowed = self.VALID_TRANSITIONS.get(current, set())

        if new_status not in allowed:
            raise ValueError(f"Invalid status transition: {current} -> {new_status}")

        order.status = new_status

        return self.order_repo.update_order(order)

    def confirm_order(self, order_id: UUID, user: User) -> OrderResponse:
        order = self.order_repo.get_order_by_id(order_id)

        if not order:
            raise ValueError("Order not found")

        # only restaurant owner or admin
        if str(order.restaurant.owner_id) != str(user.id):
            for ur in user.user_roles:
                if ur.role.name == "Admin":
                    break
            else:
                raise ValueError("Permission denied")

        updated = self._transition(order, "CONFIRMED")

        return OrderResponse.from_orm(updated)

    def reject_order(self, order_id: UUID, user: User) -> OrderResponse:
        order = self.order_repo.get_order_by_id(order_id)

        if not order:
            raise ValueError("Order not found")

        if str(order.restaurant.owner_id) != str(user.id):
            for ur in user.user_roles:
                if ur.role.name == "Admin":
                    break
            else:
                raise ValueError("Permission denied")

        updated = self._transition(order, "REJECTED")

        return OrderResponse.from_orm(updated)

    def preparing(self, order_id: UUID, user: User) -> OrderResponse:
        order = self.order_repo.get_order_by_id(order_id)

        if not order:
            raise ValueError("Order not found")

        if str(order.restaurant.owner_id) != str(user.id):
            for ur in user.user_roles:
                if ur.role.name == "Admin":
                    break
            else:
                raise ValueError("Permission denied")

        updated = self._transition(order, "PREPARING")

        return OrderResponse.from_orm(updated)

    def ready_for_pickup(self, order_id: UUID, user: User) -> OrderResponse:
        order = self.order_repo.get_order_by_id(order_id)

        if not order:
            raise ValueError("Order not found")

        if str(order.restaurant.owner_id) != str(user.id):
            for ur in user.user_roles:
                if ur.role.name == "Admin":
                    break
            else:
                raise ValueError("Permission denied")

        updated = self._transition(order, "READY_FOR_PICKUP")

        return OrderResponse.from_orm(updated)

    def pickup(self, order_id: UUID, user: User) -> OrderResponse:
        order = self.order_repo.get_order_by_id(order_id)

        if not order:
            raise ValueError("Order not found")

        # Delivery partner check: permission should be enforced at API layer
        updated = self._transition(order, "OUT_FOR_DELIVERY")

        return OrderResponse.from_orm(updated)

    def deliver(self, order_id: UUID, user: User) -> OrderResponse:
        order = self.order_repo.get_order_by_id(order_id)

        if not order:
            raise ValueError("Order not found")

        updated = self._transition(order, "DELIVERED")

        return OrderResponse.from_orm(updated)
