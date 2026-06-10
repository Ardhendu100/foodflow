from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from foodflow.infrastructure.database.base import Base


class CartItem(Base):
    __tablename__ = "cart_items"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    cart_id: Mapped[UUID] = mapped_column(
        ForeignKey("carts.id"),
        nullable=False,
    )

    menu_item_id: Mapped[UUID] = mapped_column(
        ForeignKey("menu_items.id"),
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
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

    cart = relationship(
        "Cart",
        back_populates="items",
    )

    menu_item = relationship(
        "MenuItem",
        back_populates="cart_items",
    )
