from typing import Optional
from uuid import UUID

from foodflow.application.menu.schemas import (
    CreateMenuItemRequest,
    UpdateMenuItemRequest,
    MenuItemResponse,
    PaginatedMenuItemsResponse,
)
from foodflow.domain.models.menu_item import MenuItem
from foodflow.domain.models.restaurant import Restaurant
from foodflow.domain.models.user import User
from foodflow.infrastructure.repositories.menu_repository import (
    MenuRepository,
)


class MenuService:
    def __init__(self, repository: MenuRepository, restaurant_repo):
        self.repository = repository
        self.restaurant_repo = restaurant_repo

    def create_menu_item(
        self, request: CreateMenuItemRequest, current_user: User
    ) -> MenuItemResponse:
        # Business rule: restaurant must exist
        restaurant = self.restaurant_repo.get_restaurant_by_id(request.restaurant_id)

        if not restaurant:
            raise ValueError("Restaurant not found")

        # Authorization: only owner or admin can create
        if not self._is_owner_or_admin(restaurant, current_user):
            raise ValueError("Permission denied: not restaurant owner or admin")

        if request.price <= 0:
            raise ValueError("Price must be positive")

        item = MenuItem(
            restaurant_id=request.restaurant_id,
            name=request.name,
            description=request.description,
            price=request.price,
            image_url=str(request.image_url) if request.image_url is not None else None,
            veg_type=request.veg_type or "veg",
            preparation_time_minutes=request.preparation_time_minutes or 10,
        )

        created = self.repository.create_menu_item(item)

        return MenuItemResponse.from_orm(created)

    def get_menu_item(self, menu_item_id: UUID) -> Optional[MenuItemResponse]:
        item = self.repository.get_menu_item_by_id(menu_item_id)

        if not item:
            return None

        return MenuItemResponse.from_orm(item)

    def list_menu_items_by_restaurant(
        self, restaurant_id: UUID, page: int = 1, per_page: int = 20
    ) -> PaginatedMenuItemsResponse:
        items, total = self.repository.list_menu_items_by_restaurant(
            restaurant_id, page=page, per_page=per_page
        )

        return PaginatedMenuItemsResponse(
            items=[MenuItemResponse.from_orm(i) for i in items],
            total=total,
            page=page,
            per_page=per_page,
        )

    def update_menu_item(
        self, menu_item_id: UUID, request: UpdateMenuItemRequest, current_user: User
    ) -> MenuItemResponse:
        item = self.repository.get_menu_item_by_id(menu_item_id)

        if not item:
            raise ValueError("Menu item not found")

        # Ownership check
        restaurant = self.restaurant_repo.get_restaurant_by_id(item.restaurant_id)

        if not self._is_owner_or_admin(restaurant, current_user):
            raise ValueError("Permission denied: not restaurant owner or admin")

        # Prevent changing restaurant_id
        if getattr(request, "restaurant_id", None):
            raise ValueError("Cannot change restaurant_id of a menu item")

        # Apply updates
        if request.name is not None:
            item.name = request.name

        if request.description is not None:
            item.description = request.description

        if request.price is not None:
            if request.price <= 0:
                raise ValueError("Price must be positive")
            item.price = request.price

        if request.image_url is not None:
            item.image_url = (
                str(request.image_url) if request.image_url is not None else None
            )

        if request.is_available is not None:
            item.is_available = request.is_available

        if request.veg_type is not None:
            item.veg_type = request.veg_type

        if request.preparation_time_minutes is not None:
            item.preparation_time_minutes = request.preparation_time_minutes

        updated = self.repository.update_menu_item(item)

        return MenuItemResponse.from_orm(updated)

    def delete_menu_item(self, menu_item_id: UUID, current_user: User) -> None:
        item = self.repository.get_menu_item_by_id(menu_item_id)

        if not item:
            raise ValueError("Menu item not found")

        restaurant = self.restaurant_repo.get_restaurant_by_id(item.restaurant_id)

        if not self._is_owner_or_admin(restaurant, current_user):
            raise ValueError("Permission denied: not restaurant owner or admin")

        self.repository.delete_menu_item(item)

    def _is_owner_or_admin(self, restaurant: Restaurant, user: User) -> bool:
        # Admin role check via permissions
        # Admin bypass can be implemented by checking role/permission in the user object
        # Here we check for a role named 'Admin' as a simple approach
        for ur in user.user_roles:
            if ur.role.name == "Admin":
                return True

        return str(restaurant.owner_id) == str(user.id)
