from decimal import Decimal
from uuid import UUID

from foodflow.application.cart.schemas import (
    AddToCartRequest,
    CartItemResponse,
    CartResponse,
)
from foodflow.domain.models.cart import Cart
from foodflow.domain.models.cart_item import CartItem
from foodflow.infrastructure.repositories.cart_repository import (
    CartRepository,
)
from foodflow.infrastructure.repositories.menu_repository import (
    MenuRepository,
)


class CartService:
    def __init__(
        self,
        cart_repository: CartRepository,
        menu_repository: MenuRepository,
    ):
        self.cart_repository = cart_repository
        self.menu_repository = menu_repository

    def add_to_cart(
        self,
        user_id: UUID,
        request: AddToCartRequest,
    ):

        menu_item = self.menu_repository.get_menu_item_by_id(
            request.menu_item_id,
        )

        if not menu_item:
            raise ValueError("Menu item not found")

        if not menu_item.is_available:
            raise ValueError("Menu item is not available")

        cart = self.cart_repository.get_user_cart(
            user_id,
        )

        # Create cart if missing
        if not cart:
            cart = Cart(
                user_id=user_id,
                restaurant_id=menu_item.restaurant_id,
            )

            cart = self.cart_repository.create_cart(cart)

        # One restaurant per cart
        if cart.restaurant_id != menu_item.restaurant_id:
            raise ValueError("Cart already contains items from another restaurant")

        existing_item = self.cart_repository.get_cart_item(
            cart.id,
            menu_item.id,
        )

        if existing_item:
            existing_item.quantity += request.quantity

            self.cart_repository.update()

            return

        cart_item = CartItem(
            cart_id=cart.id,
            menu_item_id=menu_item.id,
            quantity=request.quantity,
            unit_price=menu_item.price,
        )

        self.cart_repository.add_cart_item(
            cart_item,
        )

    def get_cart(
        self,
        user_id: UUID,
    ) -> CartResponse:

        cart = self.cart_repository.get_user_cart(
            user_id,
        )

        if not cart:
            raise ValueError("Cart is empty")

        total_amount = Decimal("0")

        items = []

        for item in cart.items:
            total_amount += item.unit_price * item.quantity

            items.append(
                CartItemResponse.model_validate(
                    item,
                )
            )

        return CartResponse(
            cart_id=cart.id,
            restaurant_id=cart.restaurant_id,
            items=items,
            total_amount=total_amount,
        )
