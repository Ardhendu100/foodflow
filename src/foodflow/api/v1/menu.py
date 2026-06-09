from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from foodflow.application.menu.schemas import (
    CreateMenuItemRequest,
    UpdateMenuItemRequest,
    MenuItemResponse,
    PaginatedMenuItemsResponse,
)
from foodflow.application.menu.service import MenuService
from foodflow.infrastructure.database.session import get_db
from foodflow.infrastructure.repositories.menu_repository import MenuRepository
from foodflow.infrastructure.repositories.restaurant_repository import (
    RestaurantRepository,
)
from foodflow.application.auth.permission import require_permission
from foodflow.application.auth.dependencies import get_current_user
from foodflow.domain.models.user import User

router = APIRouter(prefix="/menu", tags=["Menu"])


@router.post("/", response_model=MenuItemResponse, status_code=status.HTTP_201_CREATED)
def create_menu(
    request: CreateMenuItemRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission("menu:create")),
):
    repo = MenuRepository(db)
    restaurant_repo = RestaurantRepository(db)
    service = MenuService(repo, restaurant_repo)

    try:
        return service.create_menu_item(request, current_user)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{menu_item_id}", response_model=MenuItemResponse)
def get_menu_item(menu_item_id: UUID, db: Session = Depends(get_db)):
    repo = MenuRepository(db)
    restaurant_repo = RestaurantRepository(db)
    service = MenuService(repo, restaurant_repo)

    item = service.get_menu_item(menu_item_id)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found"
        )

    return item


@router.get("/restaurant/{restaurant_id}", response_model=PaginatedMenuItemsResponse)
def list_by_restaurant(
    restaurant_id: UUID,
    page: int = 1,
    per_page: int = 20,
    db: Session = Depends(get_db),
):
    repo = MenuRepository(db)
    restaurant_repo = RestaurantRepository(db)
    service = MenuService(repo, restaurant_repo)
    return service.list_menu_items_by_restaurant(
        restaurant_id, page=page, per_page=per_page
    )


@router.put("/{menu_item_id}", response_model=MenuItemResponse)
def update_menu_item(
    menu_item_id: UUID,
    request: UpdateMenuItemRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission("menu:update")),
):
    repo = MenuRepository(db)
    restaurant_repo = RestaurantRepository(db)
    service = MenuService(repo, restaurant_repo)

    try:
        return service.update_menu_item(menu_item_id, request, current_user)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{menu_item_id}")
def delete_menu_item(
    menu_item_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission("menu:delete")),
):
    repo = MenuRepository(db)
    restaurant_repo = RestaurantRepository(db)
    service = MenuService(repo, restaurant_repo)

    try:
        service.delete_menu_item(menu_item_id, current_user)

        return {"message": "Menu item deleted"}

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
