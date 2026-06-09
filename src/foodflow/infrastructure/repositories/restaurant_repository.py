from uuid import UUID

from sqlalchemy.orm import Session

from foodflow.domain.models.restaurant import Restaurant


class RestaurantRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_restaurant(self, restaurant: Restaurant) -> Restaurant:
        self.db.add(restaurant)
        self.db.commit()
        self.db.refresh(restaurant)

        return restaurant

    def get_restaurant_by_id(self, restaurant_id: UUID) -> Restaurant | None:
        return self.db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()

    def list_restaurants(
        self,
        page: int = 1,
        per_page: int = 20,
        owner_id: UUID | None = None,
    ) -> tuple[list[Restaurant], int]:
        """
        Returns a tuple of (restaurants, total_count).
        """
        query = self.db.query(Restaurant)

        if owner_id:
            query = query.filter(Restaurant.owner_id == owner_id)

        total = query.count()

        items = (
            query.order_by(Restaurant.created_at.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

        return items, total
