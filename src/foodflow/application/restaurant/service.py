from foodflow.application.restaurant.schemas import (
    CreateRestaurantRequest,
    RestaurantResponse,
    PaginatedRestaurantsResponse,
)
from foodflow.domain.models.restaurant import Restaurant
from foodflow.infrastructure.repositories.restaurant_repository import (
    RestaurantRepository,
)
from foodflow.infrastructure.cache.cache_service import (
    CacheService,
)


class RestaurantService:
    def __init__(self, repository: RestaurantRepository, cache: CacheService):
        self.repository = repository
        self.cache = cache

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

        cache_key = f"restaurant:list:{page}:{per_page}"

        cached = self.cache.get(cache_key)

        if cached:
            print("----Cache HIT ---------")

            return PaginatedRestaurantsResponse(**cached)
        print("----Cache MISS ---------")

        items, total = self.repository.list_restaurants(
            page=page, per_page=per_page, owner_id=owner_id
        )

        response = PaginatedRestaurantsResponse(
            items=[RestaurantResponse.from_orm(i) for i in items],
            total=total,
            page=page,
            per_page=per_page,
        )

        self.cache.set(
            cache_key,
            response.model_dump(
                mode="json",
            ),
            ttl=300,
        )

        return response
