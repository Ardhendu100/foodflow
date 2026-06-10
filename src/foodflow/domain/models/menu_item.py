from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from foodflow.infrastructure.database.base import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    restaurant_id: Mapped[UUID] = mapped_column(
        ForeignKey("restaurants.id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    price: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    image_url: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    # "veg" or "non-veg" - keep small enum-like values
    veg_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="veg",
    )

    preparation_time_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=10,
    )

    is_available: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    restaurant = relationship(
        "Restaurant",
        back_populates="menu_items",
    )

    cart_items = relationship(
        "CartItem",
        back_populates="menu_item",
    )
