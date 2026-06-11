from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from foodflow.infrastructure.database.base import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    order_id: Mapped[UUID] = mapped_column(
        ForeignKey("orders.id"),
        nullable=False,
    )

    menu_item_id: Mapped[UUID] = mapped_column(
        ForeignKey("menu_items.id"),
        nullable=False,
    )

    item_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    item_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )

    order = relationship(
        "Order",
        back_populates="items",
    )

    menu_item = relationship(
        "MenuItem",
        back_populates="order_items",
    )
