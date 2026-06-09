from uuid import UUID

from sqlalchemy.orm import Session

from foodflow.domain.models.menu_item import MenuItem


class MenuRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_menu_item(self, menu_item: MenuItem) -> MenuItem:
        self.db.add(menu_item)
        self.db.commit()
        self.db.refresh(menu_item)

        return menu_item

    def get_menu_item_by_id(self, menu_item_id: UUID) -> MenuItem | None:
        return self.db.query(MenuItem).filter(MenuItem.id == menu_item_id).first()

    def get_menu_items_by_restaurant(self, restaurant_id: UUID) -> list[MenuItem]:
        return (
            self.db.query(MenuItem)
            .filter(MenuItem.restaurant_id == restaurant_id)
            .all()
        )

    def list_menu_items_by_restaurant(
        self,
        restaurant_id: UUID,
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[list[MenuItem], int]:
        query = self.db.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id)

        total = query.count()

        items = (
            query.order_by(MenuItem.created_at.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

        return items, total

    def update_menu_item(self, menu_item: MenuItem) -> MenuItem:
        self.db.add(menu_item)
        self.db.commit()
        self.db.refresh(menu_item)

        return menu_item

    def delete_menu_item(self, menu_item: MenuItem) -> None:
        self.db.delete(menu_item)
        self.db.commit()
