from foodflow.application.restaurant.schemas import (
    CreateRestaurantRequest,
    RestaurantResponse,
    PaginatedRestaurantsResponse,
)
from foodflow.domain.models.restaurant import Restaurant
from foodflow.infrastructure.repositories.restaurant_repository import (
    RestaurantRepository,
)


class RestaurantService:
    def __init__(self, repository: RestaurantRepository):
        self.repository = repository

    def create_restaurant(self, request: CreateRestaurantRequest) -> RestaurantResponse:
        restaurant = Restaurant(
            owner_id=request.owner_id,
            name=request.name,
            description=request.description,
            phone=request.phone,
            email=request.email,
        )

        created = self.repository.create_restaurant(restaurant)

        return RestaurantResponse.from_orm(created)

    def get_restaurant(self, restaurant_id):
        r = self.repository.get_restaurant_by_id(restaurant_id)

        if not r:
            return None

        return RestaurantResponse.from_orm(r)

    def list_restaurants(
        self, page: int = 1, per_page: int = 20, owner_id=None
    ) -> PaginatedRestaurantsResponse:
        items, total = self.repository.list_restaurants(
            page=page, per_page=per_page, owner_id=owner_id
        )

        return PaginatedRestaurantsResponse(
            items=[RestaurantResponse.from_orm(i) for i in items],
            total=total,
            page=page,
            per_page=per_page,
        )
