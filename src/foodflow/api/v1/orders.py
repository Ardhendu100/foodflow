from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from foodflow.application.order.service import OrderService
from foodflow.infrastructure.repositories.order_repository import OrderRepository
from foodflow.infrastructure.repositories.cart_repository import CartRepository
from foodflow.infrastructure.repositories.menu_repository import MenuRepository
from foodflow.infrastructure.repositories.restaurant_repository import (
    RestaurantRepository,
)
from foodflow.infrastructure.database.session import get_db
from foodflow.application.auth.dependencies import get_current_user
from foodflow.application.auth.permission import require_permission
from foodflow.application.order.schemas import OrderResponse, OrderListResponse
from foodflow.domain.models.user import User

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    db=Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission("order:create")),
):
    order_repo = OrderRepository(db)
    cart_repo = CartRepository(db)
    menu_repo = MenuRepository(db)
    restaurant_repo = RestaurantRepository(db)

    service = OrderService(order_repo, cart_repo, menu_repo, restaurant_repo)

    try:
        return service.checkout(current_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=OrderListResponse)
def list_my_orders(db=Depends(get_db), current_user: User = Depends(get_current_user)):
    order_repo = OrderRepository(db)
    cart_repo = CartRepository(db)
    menu_repo = MenuRepository(db)
    restaurant_repo = RestaurantRepository(db)

    service = OrderService(order_repo, cart_repo, menu_repo, restaurant_repo)

    return service.list_orders_for_user(current_user)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: UUID, db=Depends(get_db), current_user: User = Depends(get_current_user)
):
    order_repo = OrderRepository(db)
    cart_repo = CartRepository(db)
    menu_repo = MenuRepository(db)
    restaurant_repo = RestaurantRepository(db)

    service = OrderService(order_repo, cart_repo, menu_repo, restaurant_repo)

    try:
        order = service.get_order(order_id, current_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    return order


@router.patch("/{order_id}/confirm", response_model=OrderResponse)
def confirm_order(
    order_id: UUID,
    db=Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission("order:confirm")),
):
    order_repo = OrderRepository(db)
    cart_repo = CartRepository(db)
    menu_repo = MenuRepository(db)
    restaurant_repo = RestaurantRepository(db)

    service = OrderService(order_repo, cart_repo, menu_repo, restaurant_repo)

    try:
        return service.confirm_order(order_id, current_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{order_id}/reject", response_model=OrderResponse)
def reject_order(
    order_id: UUID,
    db=Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission("order:reject")),
):
    order_repo = OrderRepository(db)
    cart_repo = CartRepository(db)
    menu_repo = MenuRepository(db)
    restaurant_repo = RestaurantRepository(db)

    service = OrderService(order_repo, cart_repo, menu_repo, restaurant_repo)

    try:
        return service.reject_order(order_id, current_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{order_id}/preparing", response_model=OrderResponse)
def preparing(
    order_id: UUID,
    db=Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission("order:prepare")),
):
    order_repo = OrderRepository(db)
    cart_repo = CartRepository(db)
    menu_repo = MenuRepository(db)
    restaurant_repo = RestaurantRepository(db)

    service = OrderService(order_repo, cart_repo, menu_repo, restaurant_repo)

    try:
        return service.preparing(order_id, current_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{order_id}/ready", response_model=OrderResponse)
def ready(
    order_id: UUID,
    db=Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission("order:prepare")),
):
    order_repo = OrderRepository(db)
    cart_repo = CartRepository(db)
    menu_repo = MenuRepository(db)
    restaurant_repo = RestaurantRepository(db)

    service = OrderService(order_repo, cart_repo, menu_repo, restaurant_repo)

    try:
        return service.ready_for_pickup(order_id, current_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{order_id}/pickup", response_model=OrderResponse)
def pickup(
    order_id: UUID,
    db=Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission("order:pickup")),
):
    order_repo = OrderRepository(db)
    cart_repo = CartRepository(db)
    menu_repo = MenuRepository(db)
    restaurant_repo = RestaurantRepository(db)

    service = OrderService(order_repo, cart_repo, menu_repo, restaurant_repo)

    try:
        return service.pickup(order_id, current_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{order_id}/deliver", response_model=OrderResponse)
def deliver(
    order_id: UUID,
    db=Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission("order:deliver")),
):
    order_repo = OrderRepository(db)
    cart_repo = CartRepository(db)
    menu_repo = MenuRepository(db)
    restaurant_repo = RestaurantRepository(db)

    service = OrderService(order_repo, cart_repo, menu_repo, restaurant_repo)

    try:
        return service.deliver(order_id, current_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
