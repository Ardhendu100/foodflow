from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from foodflow.application.restaurant.schemas import (
    CreateRestaurantRequest,
    RestaurantResponse,
    PaginatedRestaurantsResponse,
)
from foodflow.application.restaurant.service import RestaurantService
from foodflow.infrastructure.database.session import get_db
from foodflow.infrastructure.repositories.restaurant_repository import (
    RestaurantRepository,
)

from foodflow.application.auth.permission import (
    require_permission,
)

router = APIRouter(
    prefix="/restaurants",
    tags=["Restaurants"],
)


@router.post(
    "/", response_model=RestaurantResponse, status_code=status.HTTP_201_CREATED
)
def create_restaurant(
    request: CreateRestaurantRequest,
    db: Session = Depends(get_db),
    _: None = Depends(require_permission("restaurant:create")),
):
    repository = RestaurantRepository(db)
    service = RestaurantService(repository)

    try:
        return service.create_restaurant(request)

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )


@router.get("/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant(restaurant_id: str, db: Session = Depends(get_db)):
    repository = RestaurantRepository(db)
    service = RestaurantService(repository)

    r = service.get_restaurant(restaurant_id)

    if not r:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found"
        )

    return r


@router.get("/", response_model=PaginatedRestaurantsResponse)
def list_restaurants(
    page: int = 1,
    per_page: int = 20,
    owner_id: str | None = None,
    db: Session = Depends(get_db),
):
    repository = RestaurantRepository(db)
    service = RestaurantService(repository)

    owner_uuid = None
    if owner_id:
        owner_uuid = owner_id

    return service.list_restaurants(page=page, per_page=per_page, owner_id=owner_uuid)
